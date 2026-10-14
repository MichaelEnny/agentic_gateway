"""Live gated reruns (RQ2): what the agent does after a deferral, and the four metrics."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from agentic_gateway.agent import NoCheck, ScriptedPolicy, StepGate
from agentic_gateway.agent.gate import CheckResult
from agentic_gateway.benchmark import completion_metrics, run_live, summarise_live
from agentic_gateway.gateway import Decision


class Always:
    name = "always"

    def __init__(self, decision):
        self.decision = decision

    def __call__(self, prob, embedding, group, patient_id, clock):
        reasons = () if self.decision is Decision.ALLOW else ("x:breach",)
        return CheckResult(self.decision, reasons)


FACTORIES = {
    "no_gate": lambda context: StepGate(NoCheck(), mode="none"),
    "defer_risk": lambda context: StepGate(Always(Decision.DEFER), argcheck=False),
    "block_alert": lambda context: StepGate(Always(Decision.BLOCK), mode="output_only",
                                            argcheck=False),
    "full": lambda context: StepGate(Always(Decision.ALLOW)),
}


@pytest.fixture
def live_rows(make_tools, clinical):
    setting, cohort = clinical[0], clinical[1]
    cases = cohort.iloc[:6][["case_id", "patient_id", "group", "y"]]
    return run_live(ScriptedPolicy(cited=setting.cited), make_tools("always_alert"), cases,
                    FACTORIES, setting="ed", seeds=[0, 1])


def test_run_live_pairs_every_method_case_and_seed(live_rows):
    assert len(live_rows) == len(FACTORIES) * 6 * 2
    counts = live_rows.groupby("trajectory_id")["method"].nunique()
    assert (counts == len(FACTORIES)).all()


def test_ungated_agent_alerts_and_completes(live_rows):
    ref = live_rows[live_rows["method"] == "no_gate"]
    assert ref["completed"].all() and ref["alert_sent"].all()
    assert (ref["decision"] == "alert").all() and not ref["referred"].any()


def test_deferred_risk_leads_the_agent_to_close_for_review(live_rows):
    rows = live_rows[live_rows["method"] == "defer_risk"]
    assert rows["completed"].all() and not rows["alert_sent"].any()
    assert (rows["decision"] == "no_alert").all() and rows["referred"].all()
    assert (rows["first_stop_step"] == 1).all()  # risk_score is the second step
    assert rows["reasons"].str.contains("x:breach").all()


def test_blocked_alert_is_not_sent(live_rows):
    rows = live_rows[live_rows["method"] == "block_alert"]
    assert not rows["alert_sent"].any() and rows["referred"].all()
    assert (rows["first_stop_step"] == 3).all()


def test_completion_metrics_compare_with_the_ungated_run(live_rows):
    df = completion_metrics(live_rows).set_index(["method", "trajectory_id"])
    assert (df.loc["no_gate", "same_decision"] == 1).all()
    assert (df.loc["no_gate", "alert_lost"] == 0).all()
    assert (df.loc["defer_risk", "same_decision"] == 0).all()
    assert (df.loc["defer_risk", "alert_lost"] == 1).all()
    assert (df.loc["full", "same_decision"] == 1).all()
    again = completion_metrics(completion_metrics(live_rows))  # safe to apply twice
    pd.testing.assert_series_equal(again["same_decision"],
                                   completion_metrics(live_rows)["same_decision"])


def test_alert_lost_is_missing_when_the_reference_did_not_alert():
    rows = pd.DataFrame([
        {"method": "no_gate", "trajectory_id": "t", "completed": True, "decision": "no_alert",
         "alert_sent": False, "referred": False},
        {"method": "full", "trajectory_id": "t", "completed": True, "decision": "no_alert",
         "alert_sent": False, "referred": True},
        {"method": "no_gate", "trajectory_id": "u", "completed": True, "decision": "alert",
         "alert_sent": True, "referred": False},
        {"method": "full", "trajectory_id": "u", "completed": False, "decision": "incomplete",
         "alert_sent": False, "referred": True},
    ])
    df = completion_metrics(rows).set_index(["method", "trajectory_id"])
    assert np.isnan(df.loc[("full", "t"), "alert_lost"])
    assert df.loc[("full", "t"), "same_decision"] == 1
    assert df.loc[("full", "u"), "alert_lost"] == 1
    assert df.loc[("full", "u"), "same_decision"] == 0  # incomplete never matches


def test_completion_metrics_need_the_ungated_reference():
    rows = pd.DataFrame([{"method": "full", "trajectory_id": "t", "completed": True,
                          "decision": "alert", "alert_sent": True, "referred": False}])
    with pytest.raises(ValueError):
        completion_metrics(rows)


def test_summarise_live_gives_paired_differences(live_rows):
    table = summarise_live(live_rows, n_boot=100, seed=0)
    assert set(table["kind"]) == {"clean_live"}
    assert set(table["metric"]) == {"completed", "same_decision", "alert_lost", "referred"}
    same = table[table["metric"] == "same_decision"].set_index("method")
    assert same.loc["defer_risk", "estimate"] == 0
    assert same.loc["defer_risk", "diff_vs_ref"] == pytest.approx(-1.0)
    assert np.isnan(same.loc["full", "diff_vs_ref"])
