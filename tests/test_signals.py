from __future__ import annotations

import math

import numpy as np
import pandas as pd
import pytest
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB

from agentic_gateway.gateway import (
    AlertHistory,
    DriftState,
    DriftStateReader,
    LocalCalibration,
    MondrianConformal,
    SCDITable,
    TimingRule,
    age_band,
    compute_scdi_table,
    embedder_for,
    group_labels,
    risk_tier,
    run_drift_job,
)
from agentic_gateway.metrics import ece

# -- M1 ------------------------------------------------------------------------------------


def _local(ref: pd.DataFrame, metric: str = "euclidean") -> LocalCalibration:
    return LocalCalibration(min_neighbors=30, metric=metric).fit(
        ref[["e0", "e1"]].to_numpy(), ref["probability"].to_numpy(), ref["label"].to_numpy()
    )


def test_local_signal_higher_in_miscalibrated_region(reference):
    m1 = _local(reference)
    inside = m1.evaluate(np.array([15.0, 15.0]))
    outside = m1.evaluate(np.array([10.0, 10.0]))
    assert inside.n_neighbors >= 30 and outside.n_neighbors >= 30
    assert inside.value > outside.value + 0.2


def test_local_flags_sparse_patient_and_expands(reference):
    m1 = _local(reference)
    far = m1.evaluate(np.array([22.0, 2.0]))
    typical = m1.evaluate(np.array([10.0, 10.0]))
    assert far.sparse and not typical.sparse
    assert far.steps > typical.steps
    assert far.n_neighbors >= 30


def test_local_cosine_metric_runs(reference):
    result = _local(reference, metric="cosine").evaluate(np.array([10.0, 10.5]))
    assert result.n_neighbors >= 30 and 0.0 <= result.value <= 1.0


def test_local_rejects_tiny_reference():
    with pytest.raises(ValueError):
        LocalCalibration(min_neighbors=30).fit(np.zeros((10, 2)), np.zeros(10), np.zeros(10))


# -- M2 ------------------------------------------------------------------------------------


def test_scdi_definition_matches_spec(calibration):
    y, p, g = (calibration[c].to_numpy() for c in ("label", "probability", "group"))
    table = compute_scdi_table(y, p, g, min_size=50)
    e_a, e_b, overall = ece(y[g == "A"], p[g == "A"]), ece(y[g == "B"], p[g == "B"]), ece(y, p)
    expected = abs(e_a - e_b) / overall
    assert table.lookup("A") == pytest.approx(expected)
    assert table.lookup("B") == pytest.approx(expected)
    assert table.lookup("C") is None


def test_scdi_three_groups_is_per_group_max():
    rng = np.random.default_rng(0)
    n = 3000
    g = np.array(["A", "B", "C"] * (n // 3))
    true_p = rng.uniform(0.1, 0.9, n)
    y = (rng.uniform(size=n) < true_p).astype(float)
    p = true_p + np.select([g == "A", g == "B"], [0.0, 0.05], 0.3)
    p = np.clip(p, 0, 1)
    table = compute_scdi_table(y, p, g)
    e = table.subgroup_ece
    assert table.scdi["A"] == pytest.approx(
        max(abs(e["A"] - e["B"]), abs(e["A"] - e["C"])) / table.overall_ece
    )
    # The middle group's worst gap is smaller than either extreme group's.
    assert table.scdi["B"] < table.scdi["C"]


def test_scdi_excludes_small_groups_and_round_trips(calibration, tmp_path):
    y, p = calibration["label"].to_numpy(), calibration["probability"].to_numpy()
    g = calibration["group"].to_numpy().copy()
    g[:10] = "tiny"
    table = compute_scdi_table(y, p, g, min_size=50, computed_at=123.0)
    assert "tiny" in table.excluded and table.lookup("tiny") is None
    table.save(tmp_path / "scdi.json")
    assert SCDITable.load(tmp_path / "scdi.json") == table


# -- M3 ------------------------------------------------------------------------------------


def test_mondrian_coverage_holds_per_group(calibration, reference):
    m3 = MondrianConformal(coverage=0.9).fit(
        calibration["label"], calibration["probability"], calibration["group"]
    )
    results = m3.predict_many(reference["probability"].to_numpy(), reference["group"])
    covered = np.array(
        [int(y) in r.prediction_set for y, r in zip(reference["label"], results)]
    )
    for name in ("A", "B"):
        mask = (reference["group"] == name).to_numpy()
        assert covered[mask].mean() >= 0.87, name


def test_mondrian_small_group_gets_full_set_or_pooled(calibration):
    g = calibration["group"].to_numpy().copy()
    g[:5] = "tiny"
    strict = MondrianConformal(0.9).fit(calibration["label"], calibration["probability"], g)
    loose = MondrianConformal(0.9, pooled_fallback=True).fit(
        calibration["label"], calibration["probability"], g
    )
    assert strict.predict(0.5, "tiny").prediction_set == (0, 1)
    assert strict.predict(0.5, "tiny").source == "full_set"
    assert loose.predict(0.5, "tiny").source == "pooled_fallback"
    assert strict.predict(0.5, "never_seen").set_size == 2


# -- M4 ------------------------------------------------------------------------------------


def _windows(shift: float, miscal: float, seed: int = 0):
    rng = np.random.default_rng(seed)

    def window(n, s, m):
        x = rng.normal(s, 1.0, n)
        true_p = 1 / (1 + np.exp(-x))
        y = (rng.uniform(size=n) < true_p).astype(float)
        return pd.DataFrame({"x": x, "sex": rng.choice(["F", "M"], n),
                             "probability": np.clip(true_p + m, 0, 1), "label": y,
                             "group": rng.choice(["A", "B"], n)})

    return window(1500, 0.0, 0.0), window(1500, shift, miscal)


def test_drift_none_when_windows_match():
    ref, cur = _windows(0.0, 0.0)
    state = run_drift_job(ref, cur, features=["x", "sex"], n_boot=200)
    assert state.state == "none"
    assert {t.family for t in state.tests} == {"input", "output", "calibration"}


def test_drift_critical_on_large_covariate_shift():
    ref, cur = _windows(1.5, 0.0)
    state = run_drift_job(ref, cur, features=["x", "sex"], n_boot=200)
    assert state.state == "critical"
    x_test = next(t for t in state.tests if t.target == "x")
    assert x_test.rejected and x_test.psi > 0.25


def test_drift_critical_on_calibration_drift_only():
    ref, cur = _windows(0.0, 0.2)
    state = run_drift_job(ref, cur, features=["x"], n_boot=300)
    overall = next(t for t in state.tests if t.target == "ece:overall")
    assert overall.rejected and overall.delta > 0
    assert state.state == "critical"


def test_drift_skips_calibration_without_labels():
    ref, cur = _windows(0.0, 0.0)
    cur["label"] = np.nan
    state = run_drift_job(ref, cur, features=["x"], n_boot=50)
    assert all(t.family != "calibration" for t in state.tests)


def test_drift_reader_staleness_and_reload(tmp_path):
    ref, cur = _windows(0.0, 0.0)
    state = run_drift_job(ref, cur, features=["x"], n_boot=50, computed_at=1000.0)
    path = tmp_path / "drift.json"
    reader = DriftStateReader(path)
    assert reader.read(now=1000.0, max_age_s=60) is None  # no file yet
    state.save(path)
    loaded = reader.read(now=1030.0, max_age_s=60)
    assert loaded is not None and loaded.state == state.state
    assert reader.read(now=2000.0, max_age_s=60) is None  # stale
    assert DriftState.load(path).tests[0].target == "x"


# -- M5 ------------------------------------------------------------------------------------


def test_risk_tier_boundaries():
    cuts = (0.1, 0.3, 0.6)
    assert [risk_tier(p, cuts) for p in (0.0, 0.1, 0.29, 0.3, 0.99)] == [0, 1, 1, 2, 3]


def test_timing_rule_matches_spec_pseudocode():
    history = AlertHistory()
    rule = TimingRule(cooldown_s=3600, cuts=(0.1, 0.3, 0.6), history=history)
    assert not rule.evaluate("p1", 0, 0.4).suppress  # no history
    history.record("p1", 0, 2)
    assert rule.evaluate("p1", 600, 0.4).suppress  # same tier, inside cooldown
    assert rule.evaluate("p1", 600, 0.2).suppress  # lower tier, inside cooldown
    assert not rule.evaluate("p1", 600, 0.7).suppress  # escalation overrides cooldown
    assert not rule.evaluate("p1", 3600, 0.4).suppress  # cooldown elapsed
    assert not rule.evaluate("p2", 600, 0.4).suppress  # other patient


# -- shared helpers ------------------------------------------------------------------------


def test_group_labels_intersection_and_unknown():
    frame = pd.DataFrame({"sex": ["F", "M", None], "age": [70, 40, 50]})
    frame["age_band"] = age_band(frame["age"])
    labels = group_labels(frame, ["sex", "age_band"])
    assert labels.tolist() == ["F|65+", "M|<65", "__unknown__"]


@pytest.mark.parametrize(
    ("model", "metric"),
    [
        (LogisticRegression(), "cosine"),
        (GaussianNB(), "cosine"),
        (RandomForestClassifier(n_estimators=5, random_state=0), "hamming"),
    ],
)
def test_embedders(model, metric, reference):
    x = reference[["e0", "e1"]].to_numpy()
    model.fit(x, reference["label"])
    emb = embedder_for(model)
    out = emb.transform(x[:7])
    assert emb.metric == metric and out.shape[0] == 7 and np.isfinite(out).all()
    if metric == "cosine":
        assert out.shape[1] == 2


def test_pipeline_embedder_applies_preprocessing(reference):
    from sklearn.ensemble import HistGradientBoostingClassifier
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    x = reference[["e0", "e1"]].to_numpy()
    pipe = make_pipeline(StandardScaler(), LogisticRegression()).fit(x, reference["label"])
    contrib = embedder_for(pipe).transform(x[:5])
    lr = pipe[-1]
    assert np.allclose(contrib.sum(axis=1) + lr.intercept_[0], pipe.decision_function(x[:5]))

    hgb = make_pipeline(StandardScaler(), HistGradientBoostingClassifier(max_iter=5))
    with pytest.raises(TypeError, match="leaf"):
        embedder_for(hgb.fit(x, reference["label"]))


def test_lr_contributions_sum_to_logit(reference):
    x = reference[["e0", "e1"]].to_numpy()
    lr = LogisticRegression().fit(x, reference["label"])
    contrib = embedder_for(lr).transform(x[:5])
    logit = contrib.sum(axis=1) + lr.intercept_[0]
    assert np.allclose(logit, lr.decision_function(x[:5]))
    assert not math.isnan(logit[0])


def test_scdi_null_threshold_separates_chance_from_planted_gap():
    from agentic_gateway.gateway import scdi_null_threshold

    rng = np.random.default_rng(3)
    n = 4000
    true_p = rng.uniform(0.05, 0.6, n)
    y = (rng.uniform(size=n) < true_p).astype(float)
    p = np.clip(true_p + rng.normal(0, 0.03, n), 0, 1)
    g = rng.choice(list("ABCD"), n)

    null = scdi_null_threshold(y, p, g, n_permutations=100)
    assert null > 0.15  # chance alone exceeds the patent's example threshold
    assert max(compute_scdi_table(y, p, g).scdi.values()) <= null * 1.5

    planted = p.copy()
    planted[g == "D"] = np.clip(planted[g == "D"] + 0.2, 0, 1)
    assert compute_scdi_table(y, planted, g).scdi["D"] > null
