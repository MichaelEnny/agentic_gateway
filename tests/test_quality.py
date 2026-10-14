"""Conformal set-size shares (E1) and the quality of predictions a gate lets through (E2)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from agentic_gateway.agent import NoCheck, StepGate
from agentic_gateway.benchmark import replay_one
from agentic_gateway.gateway import MondrianConformal
from agentic_gateway.metrics import ece
from agentic_gateway.quality import passed_quality, prediction_quality, set_size_shares


@pytest.fixture(scope="module")
def fitted(calibration):
    cache = {}

    def conformal_for(coverage, pooled=False):
        key = (coverage, pooled)
        if key not in cache:
            groups = ["all"] * len(calibration) if pooled else calibration["group"]
            cache[key] = MondrianConformal(coverage).fit(
                calibration["label"], calibration["probability"], groups)
        return cache[key]

    return conformal_for


def test_set_size_shares_by_level_method_and_group(fitted, reference):
    out = set_size_shares(fitted, (0.8, 0.95), reference["probability"].to_numpy(),
                          reference["group"].to_numpy())
    assert set(out) == {"0.80", "0.95"}
    for level in out.values():
        assert set(level) == {"mondrian", "pooled"}
        for per in level.values():
            assert set(per) == {"_all", "A", "B"}
            assert per["_all"]["n"] == len(reference)
            assert per["A"]["n"] + per["B"]["n"] == len(reference)
            assert 0 <= per["_all"]["two_label"] + per["_all"]["empty"] <= 1
    # higher coverage -> bigger sets: more two-label, fewer empty
    lo, hi = out["0.80"]["mondrian"]["_all"], out["0.95"]["mondrian"]["_all"]
    assert hi["two_label"] >= lo["two_label"] and hi["empty"] <= lo["empty"]


def test_set_size_shares_match_a_direct_count(fitted, reference):
    probs, groups = reference["probability"].to_numpy(), reference["group"].to_numpy()
    out = set_size_shares(fitted, (0.9,), probs, groups)["0.90"]["mondrian"]["_all"]
    sizes = [fitted(0.9).predict(float(p), str(g)).set_size for p, g in zip(probs, groups)]
    assert out["two_label"] == pytest.approx(np.mean(np.array(sizes) == 2))
    assert out["empty"] == pytest.approx(np.mean(np.array(sizes) == 0))


def test_prediction_quality(fitted, reference):
    y, p = reference["label"].to_numpy(), reference["probability"].to_numpy()
    g = reference["group"].to_numpy()
    q = prediction_quality(y, p, g, fitted(0.9))
    assert q["n"] == len(y) and q["ece"] == pytest.approx(ece(y, p))
    assert 0 <= q["coverage"]["_all"] <= 1 and set(q["coverage"]) == {"_all", "A", "B"}
    assert "coverage" not in prediction_quality(y, p, g)
    empty = prediction_quality(np.array([]), np.array([]), np.array([]))
    assert empty["n"] == 0 and np.isnan(empty["ece"])


def test_passed_quality_splits_passed_and_stopped(fitted):
    rows = pd.DataFrame({
        "method": ["full"] * 6,
        "kind": ["clean", "clean", "clean", "drift", "drift", "drift"],
        "intercept_step": [-1, -1, 1, -1, 1, 2],
        "y": [0, 1, 1, 0, 1, 0],
        "risk_prob": [0.1, 0.9, 0.5, 0.8, 0.2, np.nan],  # last has no risk prediction
        "group": ["A", "B", "A", "B", "A", "B"],
    })
    q = passed_quality(rows, fitted(0.9))["full"]
    assert q["clean"]["passed"]["n"] == 2 and q["clean"]["stopped"]["n"] == 1
    assert q["faulty"]["passed"]["n"] == 1 and q["faulty"]["stopped"]["n"] == 1
    assert q["all"]["passed"]["n"] == 3 and q["all"]["stopped"]["n"] == 2
    assert q["clean"]["passed"]["ece"] == pytest.approx(ece([0, 1], [0.1, 0.9]))


def test_replay_rows_carry_the_risk_prediction(make_tools, clinical):
    from agentic_gateway.agent import ScriptedPolicy, run_episode

    tools, setting = make_tools(), clinical[0]
    row = tools.cases.loc["c1"]
    traj, _ = run_episode(ScriptedPolicy(cited=setting.cited), tools, "c1", setting="ed",
                          seed=0, y=int(row["y"]), group=str(row["group"]),
                          patient_id=str(row["patient_id"]))
    out = replay_one(traj, lambda context: StepGate(NoCheck(), mode="none"))
    assert out["y"] == int(row["y"]) and out["risk_step"] == 1
    assert out["risk_prob"] == pytest.approx(traj.first("risk_score").hidden["probability"])
