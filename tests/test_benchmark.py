"""Fault-injection benchmark: sampling, the six faults, replay, methods and the statistics."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from agentic_gateway.agent import NoCheck, ScriptedPolicy, StepGate, run_episode
from agentic_gateway.agent.gate import CheckResult
from agentic_gateway.benchmark import (
    KINDS,
    build,
    config_to_dict,
    inject,
    pooled_faults,
    replay,
    replay_one,
    sample_cases,
    summarise,
)
from agentic_gateway.benchmark.analysis import per_trajectory
from agentic_gateway.benchmark.faults import DUPLICATE_DELAY_S, SUBGROUP_SHIFT
from agentic_gateway.gateway import Decision, GatewayConfig

DATA_FAULTS = ("sparse", "subgroup", "uncertainty", "drift")


def clean_trajectory(tools, setting, case="c1", seed=0):
    row = tools.cases.loc[case]
    traj, _ = run_episode(ScriptedPolicy(cited=setting.cited), tools, case, setting="ed",
                          seed=seed, y=int(row["y"]), group=str(row["group"]),
                          patient_id=str(row["patient_id"]))
    return traj


@pytest.fixture
def alerting(make_tools, clinical):
    """Tools, setting, reference part, and a clean trajectory that ends in an alert."""
    setting, cohort = clinical[0], clinical[1]
    tools = make_tools("always_alert")
    return tools, setting, cohort.iloc[100:], clean_trajectory(tools, setting)


# -- sampling ----------------------------------------------------------------------------------


def test_sample_cases_takes_one_case_per_patient_and_a_minimum_per_group():
    rng = np.random.default_rng(0)
    cases = pd.DataFrame({
        "case_id": [f"c{i}" for i in range(600)],
        "patient_id": [f"p{i // 2}" for i in range(600)],  # two stays per patient
        "group": rng.choice(["A", "B", "C"], 600, p=[0.8, 0.15, 0.05]),
    })
    sample = sample_cases(cases, 60, min_per_group=10, seed=1)
    assert len(sample) == 60
    assert sample["patient_id"].is_unique
    assert sample["group"].value_counts().min() >= 10
    # weight = population share / sample share: oversampled small groups get weights below 1
    weights = sample.groupby("group")["weight"].first()
    assert weights["C"] < 1 < weights["A"]
    assert (sample["weight"] * sample["group"].map(
        sample["group"].value_counts(normalize=True))).groupby(sample["group"]).first() \
        .sum() == pytest.approx(1.0)


def test_sample_cases_is_reproducible():
    cases = pd.DataFrame({"case_id": range(100), "patient_id": range(100),
                          "group": ["A", "B"] * 50})
    a = sample_cases(cases, 20, min_per_group=5, seed=7)
    b = sample_cases(cases, 20, min_per_group=5, seed=7)
    pd.testing.assert_frame_equal(a, b)


# -- faults ------------------------------------------------------------------------------------


@pytest.mark.parametrize("kind", DATA_FAULTS)
def test_data_faults_rescore_and_propagate_into_the_alert(alerting, kind):
    tools, setting, reference, clean = alerting
    bad = inject(clean, kind, tools, setting, reference)
    risk, alert = bad.first("risk_score"), bad.first("draft_alert")
    assert bad.fault.kind == kind and bad.kind == kind
    assert bad.fault.step == risk.index
    assert bad.trajectory_id == f"{clean.trajectory_id}-{kind}"
    assert risk.hidden["probability"] == pytest.approx(bad.fault.detail["p_fault"])
    assert risk.output["probability"] == round(risk.hidden["probability"], 4)
    # the agent's later steps quote the faulty values, as they would after reading them
    assert alert.args["risk"] == risk.output["probability"]
    record = bad.first("fetch_record").output
    assert alert.args["cited"] == {k: record.get(k) for k in alert.args["cited"]}
    y, p0, p1 = bad.y, bad.fault.detail["p_clean"], bad.fault.detail["p_fault"]
    assert bad.fault.effect == pytest.approx(abs(p1 - y) - abs(p0 - y))


def test_faults_leave_the_clean_trajectory_untouched(alerting):
    tools, setting, reference, clean = alerting
    before = (clean.first("fetch_record").output.copy(), dict(clean.first("draft_alert").args),
              clean.first("risk_score").hidden["probability"], len(clean.steps))
    for kind in KINDS:
        inject(clean, kind, tools, setting, reference)
    after = (clean.first("fetch_record").output, clean.first("draft_alert").args,
             clean.first("risk_score").hidden["probability"], len(clean.steps))
    assert before == after and clean.fault is None


def test_subgroup_fault_raises_the_risk_and_sets_the_context(alerting):
    tools, setting, reference, clean = alerting
    bad = inject(clean, "subgroup", tools, setting, reference)
    p0 = clean.first("risk_score").hidden["probability"]
    assert bad.first("risk_score").hidden["probability"] == pytest.approx(
        min(1.0, p0 + SUBGROUP_SHIFT))
    assert bad.fault.context == f"subgroup:{clean.group}"


def test_record_faults_change_the_record(alerting):
    tools, setting, reference, clean = alerting
    record = clean.first("fetch_record").output
    sparse = inject(clean, "sparse", tools, setting, reference).first("fetch_record").output
    assert sparse["age"] == record["age"]
    assert all(sparse[f] != record[f] for f in setting.numeric if f != "age")
    blank = inject(clean, "uncertainty", tools, setting, reference).first("fetch_record").output
    assert all(blank[f] is None for f in setting.uncertainty_blank)
    field, mult, offset = setting.unit_shift
    drift = inject(clean, "drift", tools, setting, reference)
    assert drift.first("fetch_record").output[field] == pytest.approx(
        record[field] * mult + offset)
    assert drift.fault.context == "drift"


def test_duplicate_fault_resends_the_alert_later(alerting):
    tools, setting, reference, clean = alerting
    bad = inject(clean, "duplicate", tools, setting, reference)
    first, second = [s for s in bad.steps if s.tool == "draft_alert"]
    assert len(bad.steps) == len(clean.steps) + 1
    assert [s.index for s in bad.steps] == list(range(len(bad.steps)))
    assert second.index == first.index + 1 == bad.fault.step
    assert second.clock == first.clock + DUPLICATE_DELAY_S
    assert second.args == first.args


def test_ungrounded_fault_misquotes_one_vital(alerting):
    tools, setting, reference, clean = alerting
    bad = inject(clean, "ungrounded", tools, setting, reference)
    field = bad.fault.detail["field"]
    clean_cited = clean.first("draft_alert").args["cited"]
    bad_cited = bad.first("draft_alert").args["cited"]
    assert bad_cited[field] != clean_cited[field]
    assert {k: v for k, v in bad_cited.items() if k != field} == \
        {k: v for k, v in clean_cited.items() if k != field}
    assert bad.fault.step == bad.first("draft_alert").index


def test_alert_faults_do_not_apply_without_an_alert(make_tools, clinical):
    tools = make_tools("never_alert")
    clean = clean_trajectory(tools, clinical[0])
    for kind in ("duplicate", "ungrounded"):
        assert inject(clean, kind, tools, clinical[0], clinical[1]) is None
    with pytest.raises(ValueError):
        inject(clean, "cosmic_ray", tools, clinical[0], clinical[1])


# -- build -------------------------------------------------------------------------------------


def test_build_runs_every_case_and_seed_and_counts_faults(make_tools, clinical):
    setting, cohort = clinical[0], clinical[1]
    tools = make_tools("normal")
    sample = cohort.iloc[:12]
    bench = build(tools, ScriptedPolicy(cited=setting.cited), sample, setting,
                  cohort.iloc[100:], seeds=[0, 1])
    m = bench["manifest"]
    assert m["clean_trajectories"] == 24 and m["incomplete_runs"] == 0
    assert m["completion_rate"] == 1.0
    alerts = m["alerts_in_clean"]
    for kind in DATA_FAULTS:
        assert m["faulty_trajectories"][kind] == 24
    for kind in ("duplicate", "ungrounded"):
        assert m["faulty_trajectories"].get(kind, 0) == alerts
        assert m["fault_not_applicable"].get(kind, 0) == 24 - alerts
    assert set(m["share_where_fault_made_risk_worse"]) <= set(DATA_FAULTS)
    assert len(bench["faulty"]) == sum(m["faulty_trajectories"].values())


# -- replay ------------------------------------------------------------------------------------


class RiskCheck:
    """Stops every risk_score; remembers the contexts it was built for."""

    name = "stop"

    def __init__(self, decision=Decision.DEFER):
        self.decision = decision

    def __call__(self, prob, embedding, group, patient_id, clock):
        return CheckResult(self.decision, ("stop:breach",))


def test_replay_reports_the_first_interception_and_stops(alerting):
    *_, clean = alerting
    row = replay_one(clean, lambda context: StepGate(RiskCheck()))
    assert row["intercept_step"] == clean.first("risk_score").index
    assert row["decision"] == "defer" and row["reasons"] == "stop:breach"
    assert row["kind"] == "clean" and row["fault_step"] == -1
    open_row = replay_one(clean, lambda context: StepGate(NoCheck(), mode="none"))
    assert open_row["intercept_step"] == -1 and open_row["decision"] == "allow"


def test_replay_builds_each_gate_for_the_fault_context(alerting):
    tools, setting, reference, clean = alerting
    seen = []

    def factory(context):
        seen.append(context)
        return StepGate(NoCheck(), mode="none")

    trajectories = [clean, inject(clean, "drift", tools, setting, reference),
                    inject(clean, "subgroup", tools, setting, reference)]
    rows = replay(trajectories, {"a": factory, "b": factory})
    assert len(rows) == 6 and list(rows["method"]) == ["a"] * 3 + ["b"] * 3
    assert seen == ["normal", "drift", f"subgroup:{clean.group}"] * 2


def test_argument_check_catches_the_ungrounded_fault_on_replay(alerting):
    tools, setting, reference, clean = alerting
    bad = inject(clean, "ungrounded", tools, setting, reference)
    row = replay_one(bad, lambda context: StepGate(NoCheck()))
    assert row["intercept_step"] == bad.fault.step
    assert replay_one(clean, lambda context: StepGate(NoCheck()))["intercept_step"] == -1


# -- metrics and statistics --------------------------------------------------------------------


def rows_frame(entries):
    cols = ("method", "trajectory_id", "patient_id", "kind", "fault_step", "intercept_step")
    return pd.DataFrame([dict(zip(cols, e)) for e in entries])


def test_per_trajectory_definitions():
    df = per_trajectory(rows_frame([
        ("m", "t1", "p1", "sparse", 2, 2),   # early
        ("m", "t2", "p2", "sparse", 2, 4),   # intercepted late
        ("m", "t3", "p3", "sparse", 2, 1),   # premature
        ("m", "t4", "p4", "sparse", 2, -1),  # missed
        ("m", "t5", "p5", "clean", -1, 0),   # false intervention
        ("m", "t6", "p6", "clean", -1, -1),  # clean pass
    ])).set_index("trajectory_id")
    assert list(df["intercepted"][:4]) == [1, 1, 0, 0]
    assert list(df["early"][:4]) == [1, 0, 0, 0]
    assert list(df["premature"][:4]) == [0, 0, 1, 0]
    assert df.loc["t2", "steps_to_intercept"] == 2 and df.loc["t1", "steps_to_intercept"] == 0
    assert np.isnan(df.loc["t3", "steps_to_intercept"])
    assert list(df["false_intervention"][4:]) == [1, 0]
    assert df.loc[["t5", "t6"], "early"].isna().all()
    assert df.loc[["t1", "t2"], "false_intervention"].isna().all()


def paired_rows(n=40, full_rate=0.8, other_rate=0.2, seed=0):
    rng = np.random.default_rng(seed)
    entries = []
    for i in range(n):
        for method, rate in (("full", full_rate), ("weak", other_rate)):
            hit = rng.uniform() < rate
            entries.append((method, f"t{i}", f"p{i // 2}", "sparse", 1, 1 if hit else -1))
            entries.append((method, f"c{i}", f"p{i // 2}", "clean", -1, -1))
    return rows_frame(entries)


def test_summarise_gives_intervals_paired_differences_and_holm():
    table = summarise(paired_rows(), n_boot=400, seed=0)
    early = table[(table["kind"] == "sparse") & (table["metric"] == "early")] \
        .set_index("method")
    assert (early["ci_low"] <= early["estimate"]).all()
    assert (early["estimate"] <= early["ci_high"]).all()
    assert np.isnan(early.loc["full", "diff_vs_ref"])
    weak = early.loc["weak"]
    assert weak["diff_vs_ref"] == pytest.approx(weak["estimate"] - early.loc["full", "estimate"])
    assert weak["diff_high"] < 0 and weak["p_vs_ref"] < 0.05
    assert weak["p_holm"] >= weak["p_vs_ref"]
    clean = table[table["kind"] == "clean"]
    assert set(clean["metric"]) == {"false_intervention"}
    assert (clean["estimate"] == 0).all()


def test_summarise_resamples_patients_not_trajectories():
    # two patients, each with many identical trajectories: the CI must reflect 2 clusters
    entries = [("full", f"a{i}", "pA", "sparse", 1, 1) for i in range(50)]
    entries += [("full", f"b{i}", "pB", "sparse", 1, -1) for i in range(50)]
    table = summarise(rows_frame(entries), n_boot=500, seed=0)
    row = table[(table["metric"] == "early")].iloc[0]
    assert row["estimate"] == pytest.approx(0.5)
    assert row["ci_low"] == pytest.approx(0.0) and row["ci_high"] == pytest.approx(1.0)


def test_pooled_faults_averages_over_fault_types():
    out = pooled_faults(paired_rows(full_rate=1.0, other_rate=0.0))
    assert out.loc["full", "early"] == 1.0 and out.loc["weak", "early"] == 0.0
    assert (out["false_intervention"] == 0).all()


# -- methods -----------------------------------------------------------------------------------


def test_config_round_trips_through_its_dict():
    cfg = GatewayConfig(local_threshold=0.125, risk_tier_cuts=(0.05, 0.15, 0.3)) \
        .without("drift")
    assert GatewayConfig.from_dict(config_to_dict(cfg)) == cfg


# -- StepShield temporal metrics (ICML 2026, eqs. 1-3) and token accounting ------------------


def stepshield_rows():
    """Five faulty trajectories of 5 steps, fault at step 2, 100 tokens per step."""
    entries = [  # (trajectory, intercept step)
        ("t_early", 2), ("t_premature", 1), ("t_late", 4), ("t_missed", -1), ("t_first", 0)]
    rows = []
    for tid, i in entries:
        upto = 500.0 if i < 0 else 100.0 * (i + 1)
        rows.append({"method": "m", "trajectory_id": tid, "patient_id": tid, "kind": "drift",
                     "fault_step": 2, "intercept_step": i, "n_steps": 5,
                     "tokens_total": 500.0, "tokens_to_intercept": upto})
    rows.append({"method": "m", "trajectory_id": "c", "patient_id": "c", "kind": "clean",
                 "fault_step": -1, "intercept_step": 3, "n_steps": 5, "tokens_total": 500.0,
                 "tokens_to_intercept": 400.0})
    return pd.DataFrame(rows)


def test_eir_counts_detection_at_or_before_the_violation():
    df = per_trajectory(stepshield_rows()).set_index("trajectory_id")
    assert df.loc["t_early", "eir"] == 1 and df.loc["t_premature", "eir"] == 1
    assert df.loc["t_first", "eir"] == 1
    assert df.loc["t_late", "eir"] == 0 and df.loc["t_missed", "eir"] == 0
    faulty = df[df["kind"] != "clean"]
    assert (faulty["eir"] == faulty["early"] + faulty["premature"]).all()
    assert np.isnan(df.loc["c", "eir"])


def test_intervention_gap_is_zero_when_early_and_skips_missed():
    df = per_trajectory(stepshield_rows()).set_index("trajectory_id")
    assert df.loc["t_early", "intervention_gap"] == 0
    assert df.loc["t_premature", "intervention_gap"] == 0  # max(0, i - f)
    assert df.loc["t_late", "intervention_gap"] == 2
    assert np.isnan(df.loc["t_missed", "intervention_gap"])


def test_tokens_and_steps_saved():
    df = per_trajectory(stepshield_rows()).set_index("trajectory_id")
    # stopped at step 2 of 5 (0-based): 3 steps of tokens spent, 2 saved
    assert df.loc["t_early", "tokens_saved"] == pytest.approx(0.4)
    assert df.loc["t_early", "steps_saved"] == pytest.approx(0.4)
    assert df.loc["t_first", "tokens_saved"] == pytest.approx(0.8)
    assert df.loc["t_missed", "tokens_saved"] == 0 and df.loc["t_missed", "steps_saved"] == 0
    assert np.isnan(df.loc["c", "tokens_saved"])


def test_tokens_saved_is_missing_without_token_counts():
    rows = stepshield_rows().drop(columns=["tokens_total", "tokens_to_intercept"])
    df = per_trajectory(rows)
    assert df["tokens_saved"].isna().all() and df["steps_saved"].notna().any()
    table = summarise(rows, n_boot=50, seed=0)
    assert "tokens_saved" not in set(table["metric"])
    assert {"eir", "intervention_gap", "steps_saved"} <= set(table["metric"])


def test_summarise_reports_the_stepshield_metrics():
    table = summarise(stepshield_rows(), n_boot=50, seed=0).set_index("metric")
    drift = table[table["kind"] == "drift"]
    assert drift.loc["eir", "estimate"] == pytest.approx(3 / 5)
    assert drift.loc["intervention_gap", "estimate"] == pytest.approx(2 / 4)
    assert drift.loc["tokens_saved", "estimate"] == pytest.approx((0.4 + 0.6 + 0.0 + 0 + 0.8)
                                                                  / 5)


def test_replay_reports_tokens_to_the_interception(alerting):
    *_, clean = alerting
    traj = clean.copy()
    for s, t in zip(traj.steps, (100, 150, 200, 250)):
        s.tokens = t
    stopped = replay_one(traj, lambda context: StepGate(RiskCheck()))
    assert stopped["tokens_total"] == 700 and stopped["tokens_to_intercept"] == 250
    passed = replay_one(traj, lambda context: StepGate(NoCheck(), mode="none"))
    assert passed["tokens_to_intercept"] == passed["tokens_total"] == 700
    assert np.isnan(replay_one(clean, lambda c: StepGate(NoCheck()))["tokens_total"])


def test_duplicate_fault_charges_the_resent_alert(alerting):
    tools, setting, reference, clean = alerting
    traj = clean.copy()
    for s in traj.steps:
        s.tokens = 100
    bad = inject(traj, "duplicate", tools, setting, reference)
    assert [s.tokens for s in bad.steps] == [100] * 5



def test_build_reports_progress_once_per_episode(make_tools, clinical):
    setting, cohort = clinical[0], clinical[1]
    seen = []
    build(make_tools("normal"), ScriptedPolicy(cited=setting.cited), cohort.iloc[:3], setting,
          cohort.iloc[100:], seeds=[0, 1], kinds=("drift",), progress=seen.append)
    assert len(seen) == 6 and all(t.completed for t in seen)
