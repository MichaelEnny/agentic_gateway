"""Replay stored trajectories through a gating method.

Replay instead of rerunning the agent: every method sees exactly the same actions, so
differences between methods are not differences between LLM samples. The first action that is
not allowed is the interception; the trajectory stops there (handed to a clinician).

Token columns feed StepShield's Tokens Saved: ``tokens_total`` is what the agent spent on the
whole trajectory, ``tokens_to_intercept`` what it had spent up to and including the
intercepted step (the whole trajectory when nothing was intercepted, as in StepShield's code).
Both are missing when the policy reports no tokens.
"""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd

from ..agent.types import Step, Trajectory
from ..gateway.types import Decision
from .methods import GateFactory


def replay_one(traj: Trajectory, factory: GateFactory) -> dict:
    context = traj.fault.context if traj.fault else "normal"
    gate = factory(context)
    gate.reset()
    intercept, decision, reasons, latency = -1, "allow", "", 0
    for step in traj.steps:
        verdict = gate.check(step)
        latency += verdict.latency_ns
        if verdict.decision is not Decision.ALLOW:
            intercept, decision = step.index, verdict.decision.value
            reasons = "; ".join(verdict.reasons)
            break
    fault = traj.fault
    total, upto = _tokens(traj.steps, intercept)
    risk = traj.first("risk_score")
    risk_prob = float(risk.hidden["probability"]) if risk and risk.hidden else float("nan")
    return {
        "trajectory_id": traj.trajectory_id,
        "case_id": traj.case_id,
        "patient_id": traj.patient_id,
        "group": traj.group,
        "seed": traj.seed,
        "kind": traj.kind,
        "y": traj.y,
        "risk_step": risk.index if risk else -1,
        "risk_prob": risk_prob,
        "fault_step": fault.step if fault else -1,
        "fault_effect": fault.effect if fault else None,
        "n_steps": len(traj.steps),
        "intercept_step": intercept,
        "decision": decision,
        "reasons": reasons,
        "gate_latency_ns": latency,
        "tokens_total": total,
        "tokens_to_intercept": upto,
    }


def _tokens(steps: list[Step], intercept: int) -> tuple[float, float]:
    if not steps or any(s.tokens is None for s in steps):
        return float("nan"), float("nan")
    total = float(sum(s.tokens for s in steps))  # type: ignore[misc]
    stop = intercept if intercept >= 0 else len(steps) - 1
    return total, float(sum(s.tokens for s in steps[: stop + 1]))  # type: ignore[misc]


def replay(trajectories: Iterable[Trajectory], factories: dict[str, GateFactory]) -> pd.DataFrame:
    rows = []
    trajectories = list(trajectories)
    for name, factory in factories.items():
        for traj in trajectories:
            rows.append({"method": name, **replay_one(traj, factory)})
    return pd.DataFrame(rows)
