"""Agent harness: tools, policies, the step gate and episodes, on a synthetic ED cohort."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from agentic_gateway.agent import (
    ConfidenceCheck,
    GatewayCheck,
    LLMPolicy,
    NoCheck,
    ScriptedPolicy,
    Step,
    StepGate,
    new_timing,
    run_episode,
)
from agentic_gateway.agent.episode import STEP_SECONDS, WITHHELD
from agentic_gateway.agent.gate import CheckResult
from agentic_gateway.gateway import Decision, GatewayConfig

PROMPTS = Path(__file__).resolve().parents[1] / "experiments" / "prompts"


def episode(tools, setting, case="c1", gate=None, seed=0):
    row = tools.cases.loc[case]
    return run_episode(ScriptedPolicy(cited=setting.cited), tools, case, setting="ed",
                       seed=seed, y=int(row["y"]), group=str(row["group"]),
                       patient_id=str(row["patient_id"]), gate=gate)


class FixedCheck:
    """Prediction check that returns the same decision every time and counts its calls."""

    name = "fixed"

    def __init__(self, decision=Decision.ALLOW, record=None):
        self.decision, self.record, self.calls = decision, record or {}, 0

    def __call__(self, prob, embedding, group, patient_id, clock):
        self.calls += 1
        reasons = () if self.decision is Decision.ALLOW else ("fixed:breach",)
        return CheckResult(self.decision, reasons, dict(self.record))


def steps_of(make_tools, clinical, tiers="always_alert"):
    traj, _ = episode(make_tools(tiers), clinical[0])
    return traj.steps


def cooldown_gate(check=None):
    return StepGate(check or FixedCheck(), timing=new_timing(3600.0, (0.0, 0.0, 0.0)))


# -- tools ---------------------------------------------------------------------------------


def test_risk_score_hides_embedding_and_group_from_the_agent(make_tools):
    tools = make_tools("normal")
    shown, hidden = tools.call("risk_score", {"case_id": "c1"})
    assert set(shown) == {"case_id", "probability", "risk_tier"}
    assert shown["probability"] == round(hidden["probability"], 4)
    assert {"embedding", "group", "patient_id", "tier"} <= set(hidden)
    assert hidden["group"] == tools.cases.loc["c1", "group"]
    assert isinstance(hidden["embedding"], np.ndarray)


def test_record_turns_missing_values_into_none(make_tools):
    record, _ = make_tools().call("fetch_record", {"case_id": "c0"})
    assert record["o2sat"] is None
    assert record["patient_id"] == "p0"
    json.dumps(record)  # the LLM receives it as JSON


def test_alerts_are_listed_and_cleared_by_reset(make_tools):
    tools = make_tools()
    assert tools.call("prior_alerts", {"patient_id": "p1"})[0] == []
    sent, _ = tools.call("draft_alert", {"patient_id": "p1", "risk": 0.5, "cited": {},
                                         "text": "x"})
    assert sent["sent"] and sent["alert_id"] == "p1-1"
    assert len(tools.call("prior_alerts", {"patient_id": "p1"})[0]) == 1
    tools.reset()
    assert tools.call("prior_alerts", {"patient_id": "p1"})[0] == []


def test_unknown_tool_raises(make_tools):
    with pytest.raises(KeyError):
        make_tools().call("order_labs", {})


def test_scoring_an_edited_record_changes_the_risk(make_tools):
    tools = make_tools()
    record = tools.record_of("c1")
    p0, e0 = tools.score_record(record)
    p1, e1 = tools.score_record({**record, "acuity": 6.0 - record["acuity"], "sbp": 60.0})
    assert p0 != p1 and not np.array_equal(e0, e1)


# -- scripted policy and observe-mode episodes -------------------------------------------------


def test_scripted_episode_alerts_when_tier_is_high(make_tools, clinical):
    traj, verdicts = episode(make_tools("always_alert"), clinical[0])
    assert [s.tool for s in traj.steps] == ["fetch_record", "risk_score", "prior_alerts",
                                            "draft_alert"]
    assert traj.completed and verdicts == []
    assert [s.clock for s in traj.steps] == [i * STEP_SECONDS for i in range(4)]
    alert = traj.first("draft_alert")
    record = traj.first("fetch_record").output
    assert alert.args["risk"] == traj.first("risk_score").output["probability"]
    assert alert.args["cited"] == {f: record[f] for f in clinical[0].cited}


def test_scripted_episode_closes_when_tier_is_low(make_tools, clinical):
    traj, _ = episode(make_tools("never_alert"), clinical[0])
    assert traj.steps[-1].tool == "close_case" and traj.completed
    assert traj.first("draft_alert") is None


# -- step gate -------------------------------------------------------------------------------


def test_clean_trajectory_passes_every_check(make_tools, clinical):
    gate = cooldown_gate()
    verdicts = [gate.check(s) for s in steps_of(make_tools, clinical)]
    assert [v.decision for v in verdicts] == [Decision.ALLOW] * 4


def test_structural_check_blocks_unknown_tools_and_missing_arguments():
    gate = StepGate(NoCheck())
    assert gate.check(Step(0, "order_labs", {}, None, 0.0)).decision is Decision.BLOCK
    v = gate.check(Step(1, "fetch_record", {}, None, 60.0))
    assert v.decision is Decision.BLOCK and v.reasons == ("structural:invalid_call",)


def test_argument_check_blocks_a_misquoted_vital(make_tools, clinical):
    steps = steps_of(make_tools, clinical)
    name = clinical[0].cited[0]
    steps[3].args["cited"][name] = 999.0
    gate = StepGate(FixedCheck())
    verdict = [gate.check(s) for s in steps][-1]
    assert verdict.decision is Decision.BLOCK
    assert verdict.reasons == (f"argument:mismatch({name})",)


def test_argument_check_blocks_a_changed_risk(make_tools, clinical):
    steps = steps_of(make_tools, clinical)
    steps[3].args["risk"] = min(1.0, steps[3].args["risk"] + 0.1)
    gate = StepGate(FixedCheck())
    verdict = [gate.check(s) for s in steps][-1]
    assert verdict.decision is Decision.BLOCK and verdict.reasons == ("argument:mismatch(risk)",)


def test_argument_check_treats_missing_values_as_equal_only_to_missing(make_tools, clinical):
    traj, _ = episode(make_tools(), clinical[0], case="c0")  # c0 has o2sat missing
    alert = traj.first("draft_alert")
    assert alert.args["cited"]["o2sat"] is None
    gate = StepGate(FixedCheck())
    assert [gate.check(s) for s in traj.steps][-1].decision is Decision.ALLOW
    alert.args["cited"]["o2sat"] = 97.0
    gate.reset()
    assert [gate.check(s) for s in traj.steps][-1].decision is Decision.BLOCK


def test_argument_check_blocks_an_alert_with_no_record_or_risk(make_tools, clinical):
    alert = steps_of(make_tools, clinical)[3]
    verdict = StepGate(FixedCheck()).check(alert)
    assert verdict.decision is Decision.BLOCK and verdict.reasons == ("argument:no_source",)


def test_argument_check_can_be_switched_off(make_tools, clinical):
    steps = steps_of(make_tools, clinical)
    steps[3].args["cited"] = {clinical[0].cited[0]: 999.0}
    gate = StepGate(FixedCheck(), argcheck=False)
    assert [gate.check(s) for s in steps][-1].decision is Decision.ALLOW


def test_deferred_risk_taints_the_alert_built_on_it(make_tools, clinical):
    gate = StepGate(FixedCheck(Decision.DEFER))
    verdicts = [gate.check(s) for s in steps_of(make_tools, clinical)]
    assert verdicts[1].decision is Decision.DEFER
    assert verdicts[3].decision is Decision.DEFER
    assert "tag:risk_withheld" in verdicts[3].reasons


def test_output_only_mode_checks_the_prediction_at_the_alert_only(make_tools, clinical):
    check = FixedCheck(Decision.DEFER)
    gate = StepGate(check, mode="output_only")
    verdicts = [gate.check(s) for s in steps_of(make_tools, clinical)]
    assert [v.decision for v in verdicts] == [Decision.ALLOW] * 3 + [Decision.DEFER]
    assert check.calls == 1
    assert "tag:risk_withheld" not in verdicts[3].reasons


def test_prediction_record_is_passed_through(make_tools, clinical):
    gate = StepGate(FixedCheck(record={"local_calibration.latency_ns": 5}))
    verdicts = [gate.check(s) for s in steps_of(make_tools, clinical)]
    assert verdicts[1].record == {"local_calibration.latency_ns": 5}
    assert all(v.latency_ns >= 0 for v in verdicts)


def test_timing_blocks_a_repeat_alert_inside_the_cooldown(make_tools, clinical):
    steps = steps_of(make_tools, clinical)
    gate = cooldown_gate()
    for s in steps:
        gate.check(s)
    repeat = Step(4, "draft_alert", dict(steps[3].args), None, steps[3].clock + 600.0)
    verdict = gate.check(repeat)
    assert verdict.decision is Decision.BLOCK and verdict.reasons == ("timing:breach",)
    later = Step(5, "draft_alert", dict(steps[3].args), None, steps[3].clock + 7200.0)
    assert gate.check(later).decision is Decision.ALLOW


def test_a_stopped_alert_does_not_start_a_cooldown(make_tools, clinical):
    steps = steps_of(make_tools, clinical)
    good_args = dict(steps[3].args)
    steps[3].args["risk"] = min(1.0, steps[3].args["risk"] + 0.1)  # argument check blocks
    gate = cooldown_gate()
    assert [gate.check(s) for s in steps][-1].decision is Decision.BLOCK
    retry = Step(4, "draft_alert", good_args, None, steps[3].clock + 60.0)
    assert gate.check(retry).decision is Decision.ALLOW


def test_reset_clears_the_cooldown_history(make_tools, clinical):
    steps = steps_of(make_tools, clinical)
    gate = cooldown_gate()
    for s in steps:
        gate.check(s)
    gate.reset()
    assert [gate.check(s) for s in steps][-1].decision is Decision.ALLOW


def test_mode_none_allows_everything():
    gate = StepGate(FixedCheck(Decision.BLOCK), mode="none")
    assert gate.check(Step(0, "order_labs", {}, None, 0.0)).decision is Decision.ALLOW
    with pytest.raises(ValueError):
        StepGate(NoCheck(), mode="sometimes")


def test_judge_can_defer_an_action(make_tools, clinical):
    gate = StepGate(FixedCheck(), judge=lambda step, history: step.tool != "draft_alert")
    verdicts = [gate.check(s) for s in steps_of(make_tools, clinical)]
    assert verdicts[3].decision is Decision.DEFER and "judge:unsafe" in verdicts[3].reasons


def test_confidence_check_defers_uncertain_probabilities():
    check = ConfidenceCheck(cut=0.3)
    emb = np.zeros(2)
    assert check(0.5, emb, "A", "p", 0.0).decision is Decision.DEFER
    assert check(0.05, emb, "A", "p", 0.0).decision is Decision.ALLOW
    assert check(0.95, emb, "A", "p", 0.0).decision is Decision.ALLOW


def test_gateway_check_requires_timing_to_be_disabled():
    class Stub:
        config = GatewayConfig()

    with pytest.raises(ValueError):
        GatewayCheck(Stub())  # type: ignore[arg-type]


# -- gated (live) episodes ---------------------------------------------------------------------


def test_withheld_risk_makes_the_scripted_agent_close_the_case(make_tools, clinical):
    gate = StepGate(FixedCheck(Decision.DEFER))
    traj, verdicts = episode(make_tools(), clinical[0], gate=gate)
    assert traj.first("risk_score").output is WITHHELD
    assert traj.steps[-1].tool == "close_case" and traj.completed
    assert traj.first("draft_alert") is None
    assert verdicts[1].decision is Decision.DEFER


def test_a_stopped_alert_is_never_sent_and_the_case_is_closed(make_tools, clinical):
    tools = make_tools()
    gate = StepGate(FixedCheck(Decision.BLOCK), mode="output_only")
    traj, _ = episode(tools, clinical[0], gate=gate)
    assert [s.tool for s in traj.steps][-2:] == ["draft_alert", "close_case"]
    assert traj.steps[-2].output is WITHHELD
    assert "clinician review" in traj.steps[-1].args["note"] and traj.completed
    assert tools.alerts.get("p1", []) == []


# -- LLM policy (no server: the chat call is replaced) ---------------------------------------


def test_llm_policy_refuses_hosted_endpoints():
    with pytest.raises(ValueError):
        LLMPolicy(model="m", base_url="https://api.example.com/v1")
    LLMPolicy(model="m", base_url="http://127.0.0.1:1234/v1")


def tool_message(name, arguments, call_id="x1"):
    return {"role": "assistant", "content": None,
            "tool_calls": [{"id": call_id, "type": "function",
                            "function": {"name": name, "arguments": arguments}}]}


def test_llm_policy_parses_calls_and_returns_tool_output(monkeypatch):
    policy = LLMPolicy(model="m", system_prompt="sys")
    replies = iter([tool_message("fetch_record", '{"case_id": "c1"}', "a"),
                    tool_message("risk_score", "not json", "b"),
                    {"role": "assistant", "content": "done"}])
    monkeypatch.setattr(policy, "_chat", lambda: next(replies))
    policy.start("c1", "task text", seed=3)
    assert policy.next(None) == ("fetch_record", {"case_id": "c1"})
    name, args = policy.next({"case_id": "c1", "age": 50})
    assert name == "risk_score" and args == {"_unparseable": "not json"}
    tool_msg = policy._messages[3]
    assert tool_msg["role"] == "tool" and tool_msg["tool_call_id"] == "a"
    assert json.loads(tool_msg["content"]) == {"case_id": "c1", "age": 50}
    assert policy.next({"probability": 0.2}) is None  # no tool call ends the episode
    assert policy._messages[0] == {"role": "system", "content": "sys"}


def test_llm_policy_stops_at_max_steps(monkeypatch):
    policy = LLMPolicy(model="m", max_steps=2)
    monkeypatch.setattr(policy, "_chat",
                        lambda: tool_message("fetch_record", '{"case_id": "c1"}'))
    policy.start("c1", "task", seed=0)
    assert policy.next(None) is not None
    assert policy.next({}) is not None
    assert policy.next({}) is None


@pytest.mark.parametrize("name", ["ed", "icu"])
def test_prompts_name_the_fields_the_argument_check_compares(name):
    from agentic_gateway.data.settings import SETTINGS

    policy = LLMPolicy.from_prompt_file("m", PROMPTS / f"system_{name}.txt")
    for field in SETTINGS[name].cited:
        assert field in policy.system_prompt


def test_policies_describe_what_the_paper_must_report(tmp_path):
    import hashlib

    weights = tmp_path / "model.gguf"
    weights.write_bytes(b"not really weights")
    policy = LLMPolicy(model="m", system_prompt="sys", base_url="http://127.0.0.1:9/v1")
    info = policy.describe(weights)
    assert info["model_file_sha256"] == hashlib.sha256(b"not really weights").hexdigest()
    assert info["system_prompt_sha256"] == hashlib.sha256(b"sys").hexdigest()
    assert info["temperature"] == 0.2 and info["max_steps"] == 10
    assert info["server_model"] is None  # nothing listens on port 9
    assert policy.describe()["model_file_sha256"] is None
    assert ScriptedPolicy(cited=("sbp",)).describe() == {
        "policy": "scripted", "cited": ["sbp"], "alert_tier": 2}


def test_server_model_keeps_only_the_reported_fields(monkeypatch):
    import io
    import urllib.request

    seen = []

    def fake_urlopen(url, timeout):
        seen.append(url)
        body = {"id": "qwen", "quantization": "Q4_K_M", "arch": "qwen2", "state": "loaded"}
        return io.BytesIO(json.dumps(body).encode())

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    info = LLMPolicy(model="qwen").server_model()
    assert seen == ["http://localhost:1234/api/v0/models/qwen"]
    assert info == {"id": "qwen", "arch": "qwen2", "quantization": "Q4_K_M"}


def test_llm_policy_records_tokens_from_the_server_usage(monkeypatch):
    import io
    import urllib.request

    reply = {"choices": [{"message": tool_message("fetch_record", '{"case_id": "c1"}')}],
             "usage": {"prompt_tokens": 300, "completion_tokens": 20, "total_tokens": 320}}
    monkeypatch.setattr(urllib.request, "urlopen",
                        lambda req, timeout: io.BytesIO(json.dumps(reply).encode()))
    policy = LLMPolicy(model="m")
    policy.start("c1", "task", seed=0)
    assert policy.next(None) == ("fetch_record", {"case_id": "c1"})
    assert policy.last_tokens == 320
    del reply["usage"]
    policy.next({})
    assert policy.last_tokens is None  # a server without usage leaves it missing


def test_episode_attaches_the_policy_tokens_to_each_step(make_tools, clinical):
    class CountingPolicy(ScriptedPolicy):
        def next(self, last_output):
            self.last_tokens = 10 * (self._state["stage"] + 1)
            return super().next(last_output)

    tools, setting = make_tools(), clinical[0]
    row = tools.cases.loc["c1"]
    traj, _ = run_episode(CountingPolicy(cited=setting.cited), tools, "c1", setting="ed",
                          seed=0, y=int(row["y"]), group=str(row["group"]),
                          patient_id=str(row["patient_id"]))
    assert [s.tokens for s in traj.steps] == [10, 20, 30, 40]
    scripted, _ = episode(tools, setting)
    assert all(s.tokens is None for s in scripted.steps)

