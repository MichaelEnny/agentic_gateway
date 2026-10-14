"""Live gated reruns: the cost of gating on clean cases when the agent reacts to a deferral.

Replay (``replay.py``) stops a trajectory at the first interception, so it cannot say what the
agent does next. Here the agent runs live with the gate active: a stopped step returns the
"withheld" message, and the agent carries on (the prompts tell it to close the case for
clinician review). Every case and seed also runs with ``no_gate``, which is the reference
decision for that run.

Per run (one case, one seed, one method):

| metric        | definition                                                                  |
|---------------|-----------------------------------------------------------------------------|
| completed     | ended with an allowed ``draft_alert`` or ``close_case``                     |
| same_decision | completed, with the same decision (alert or no alert) as the no_gate run    |
| alert_lost    | the no_gate run sent an alert and this run did not (missing if no_gate did  |
|               | not alert)                                                                  |
| referred      | at least one step was withheld: the case went to a clinician                |

Only clean cases: faults are injected into recorded trajectories and cannot be replayed live.
"""

from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pandas as pd

from ..agent.episode import run_episode
from ..agent.policy import Policy
from ..agent.tools import ClinicalTools
from ..gateway.types import Decision
from .analysis import bootstrap_table
from .methods import GateFactory

LIVE_METRICS = ("completed", "same_decision", "alert_lost", "referred")
TERMINAL = ("draft_alert", "close_case")


def run_live(policy: Policy, tools: ClinicalTools, cases: pd.DataFrame,
             factories: dict[str, GateFactory], *, setting: str,
             seeds: Iterable[int]) -> pd.DataFrame:
    """One row per (method, case, seed). ``cases`` needs case_id, patient_id, group, y."""
    rows = []
    seeds = list(seeds)
    for method, factory in factories.items():
        for case in cases.itertuples():
            for seed in seeds:
                traj, verdicts = run_episode(
                    policy, tools, str(case.case_id), setting=setting, seed=seed,
                    y=int(case.y), group=str(case.group), patient_id=str(case.patient_id),
                    gate=factory("normal"))
                stopped = [v for v in verdicts if v.decision is not Decision.ALLOW]
                first_stop = next((i for i, v in enumerate(verdicts)
                                   if v.decision is not Decision.ALLOW), -1)
                last = traj.steps[-1].tool if traj.steps else None
                tokens = [s.tokens for s in traj.steps]
                rows.append({
                    "method": method,
                    "trajectory_id": traj.trajectory_id,
                    "case_id": traj.case_id,
                    "patient_id": traj.patient_id,
                    "group": traj.group,
                    "seed": seed,
                    "n_steps": len(traj.steps),
                    "completed": bool(traj.completed and last in TERMINAL),
                    "decision": _decision(traj.completed, last),
                    "alert_sent": bool(tools.alerts.get(traj.patient_id)),
                    "referred": bool(stopped),
                    "first_stop_step": first_stop,
                    "reasons": "; ".join(r for v in stopped for r in v.reasons),
                    "gate_latency_ns": int(sum(v.latency_ns for v in verdicts)),
                    "tokens_total": float(sum(tokens)) if tokens and None not in tokens
                    else float("nan"),
                })
    return pd.DataFrame(rows)


def _decision(completed: bool, last: str | None) -> str:
    if not completed:
        return "incomplete"
    return "alert" if last == "draft_alert" else "no_alert"


def completion_metrics(rows: pd.DataFrame, reference: str = "no_gate") -> pd.DataFrame:
    """Add same_decision and alert_lost, comparing each run with the ``reference`` run of the
    same case and seed. Safe to apply twice."""
    if reference not in set(rows["method"]):
        raise ValueError(f"the live reruns need a {reference!r} run as the reference decision")
    ref = rows[rows["method"] == reference].set_index("trajectory_id")
    df = rows.copy()
    completed = df["completed"].astype(bool)
    ref_decision = df["trajectory_id"].map(ref["decision"])
    ref_alert = df["trajectory_id"].map(ref["alert_sent"]).astype(bool)
    df["same_decision"] = (completed & (df["decision"] == ref_decision)).astype(float)
    df["alert_lost"] = np.where(ref_alert, ~df["alert_sent"].astype(bool), np.nan)
    for m in ("completed", "referred"):
        df[m] = df[m].astype(float)
    return df


def summarise_live(rows: pd.DataFrame, *, n_boot: int = 2000, seed: int = 0,
                   reference: str = "full") -> pd.DataFrame:
    """Bootstrap table of the four live metrics, kind ``clean_live``, paired against
    ``reference``."""
    df = completion_metrics(rows)
    metrics = [m for m in LIVE_METRICS if df[m].notna().any()]
    return bootstrap_table([("clean_live", df, metrics)], list(dict.fromkeys(df["method"])),
                           n_boot=n_boot, seed=seed, reference=reference)
