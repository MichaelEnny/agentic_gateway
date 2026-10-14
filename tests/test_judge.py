"""LLM-as-judge baseline: reply parsing, the prompt it sends, caching, and use in the gate.
No server is needed: the chat call is replaced."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from agentic_gateway.agent import LLMJudge, NoCheck, ScriptedPolicy, StepGate, run_episode
from agentic_gateway.agent.episode import TASKS
from agentic_gateway.agent.judge import parse_verdict
from agentic_gateway.benchmark import inject, replay_one
from agentic_gateway.gateway import Decision

PROMPT = Path(__file__).resolve().parents[1] / "experiments" / "prompts" / "judge.txt"


def make_judge(replies, tmp_path=None, **kw):
    """Judge whose chat call returns ``replies(prompt)`` and counts calls."""
    judge = LLMJudge(model="m", system_prompt="sys", task=TASKS["ed"],
                     cache_path=tmp_path / "cache.jsonl" if tmp_path else None, **kw)
    calls = []

    def chat(prompt):
        calls.append(prompt)
        return replies(prompt)

    judge._chat = chat  # type: ignore[method-assign]
    return judge, calls


def trajectory(tools, setting, case="c1"):
    row = tools.cases.loc[case]
    traj, _ = run_episode(ScriptedPolicy(cited=setting.cited), tools, case, setting="ed",
                          seed=0, y=int(row["y"]), group=str(row["group"]),
                          patient_id=str(row["patient_id"]))
    return traj


# -- parsing -------------------------------------------------------------------------------


@pytest.mark.parametrize("reply, expected", [
    ('{"decision": "allow", "reason": "consistent"}', "allow"),
    ('Here you go:\n{"decision": "DEFER", "reason": "odd unit"}', "defer"),
    ('<think>maybe {"decision": "allow"}</think>{"decision": "defer", "reason": "x"}', "defer"),
    ("I would defer this action.", "defer"),
    ("ALLOW", "allow"),
    ('{"decision": "approve"}', None),
    ("", None),
])
def test_parse_verdict(reply, expected):
    assert parse_verdict(reply)[0] == expected


def test_parse_verdict_keeps_the_reason():
    assert parse_verdict('{"decision": "defer", "reason": "temp in C"}') == ("defer",
                                                                             "temp in C")


# -- the judge -------------------------------------------------------------------------------


def test_judge_refuses_hosted_endpoints():
    with pytest.raises(ValueError):
        LLMJudge(model="m", system_prompt="", task="", base_url="https://api.example.com/v1")


def test_prompt_shows_the_trace_and_the_proposed_result(make_tools, clinical):
    traj = trajectory(make_tools(), clinical[0])
    judge, _ = make_judge(lambda p: '{"decision": "allow"}')
    text = judge.render(traj.steps[3], traj.steps[:3])
    assert "Review the triage of emergency department stay c1" in text
    assert "1. fetch_record(" in text and "3. prior_alerts(" in text
    assert "Proposed action: draft_alert(" in text
    assert '"sent": true' in text
    assert "embedding" not in text  # the gateway's hidden data is not shown
    first = judge.render(traj.steps[0], [])
    assert "Actions so far:\n(none)" in first


def test_judge_defers_unparseable_replies_and_counts_them():
    judge, _ = make_judge(lambda p: "no idea")
    step = trajectory_free_step()
    assert judge(step, []) is False
    assert judge.stats["unparseable"] == 1 and judge.stats["defer"] == 1
    lenient, _ = make_judge(lambda p: "no idea", fail_closed=False)
    assert lenient(step, []) is True


def trajectory_free_step():
    from agentic_gateway.agent import Step

    return Step(0, "fetch_record", {"case_id": "c1"}, {"case_id": "c1"}, 0.0)


def test_judge_caches_in_memory_and_on_disk(tmp_path):
    step = trajectory_free_step()
    judge, calls = make_judge(lambda p: '{"decision": "allow", "reason": "ok"}', tmp_path)
    assert judge(step, []) and judge(step, [])
    assert len(calls) == 1 and judge.stats["cached"] == 1
    lines = (tmp_path / "cache.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1 and json.loads(lines[0])["decision"] == "allow"

    again, calls2 = make_judge(lambda p: '{"decision": "defer"}', tmp_path)
    assert again(step, []) is True  # served from the file, not the new reply
    assert calls2 == []


def test_cache_key_changes_with_the_model_and_prompt(tmp_path):
    step = trajectory_free_step()
    judge, _ = make_judge(lambda p: '{"decision": "allow"}', tmp_path)
    judge(step, [])
    other, calls = make_judge(lambda p: '{"decision": "allow"}', tmp_path, seed=1)
    other(step, [])
    assert len(calls) == 1


def test_describe_reports_counts_and_latency():
    judge, _ = make_judge(lambda p: '{"decision": "allow"}')
    judge(trajectory_free_step(), [])
    info = judge.describe()
    assert info["stats"] == {"allow": 1} and info["uncached_calls"] == 1
    assert info["call_p50_ms"] is not None and len(info["system_prompt_sha256"]) == 64


def test_committed_judge_prompt_asks_for_json():
    text = PROMPT.read_text(encoding="utf-8")
    assert '"decision"' in text and "allow" in text and "defer" in text


# -- in the gate -------------------------------------------------------------------------------


def test_judge_as_a_gating_method_catches_what_it_is_told_to(make_tools, clinical):
    tools, setting = make_tools(), clinical[0]
    clean = trajectory(tools, setting)
    bad = inject(clean, "ungrounded", tools, setting, clinical[1].iloc[100:])
    record = clean.first("fetch_record").output

    def replies(prompt):
        # a judge that compares the quoted values with the record, as the prompt asks
        proposed = prompt.split("Proposed action: ", 1)[1].splitlines()[0]
        mismatch = False
        if proposed.startswith("draft_alert("):
            args = json.loads(proposed[len("draft_alert("):-1])
            mismatch = any(record[k] != v for k, v in args["cited"].items())
        return json.dumps({"decision": "defer" if mismatch else "allow", "reason": ""})

    judge, _ = make_judge(replies)

    def factory(context):
        return StepGate(NoCheck(), argcheck=False, judge=judge)

    assert replay_one(clean, factory)["intercept_step"] == -1
    row = replay_one(bad, factory)
    assert row["intercept_step"] == bad.fault.step and row["decision"] == Decision.DEFER.value
    assert "judge:unsafe" in row["reasons"]
