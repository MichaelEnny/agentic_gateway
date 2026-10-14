"""Six fault types, injected into copies of clean trajectories at recorded steps.

| kind        | what changes                                                   | aimed at       |
|-------------|----------------------------------------------------------------|----------------|
| sparse      | numeric fields moved 6 SD from the reference median            | M1             |
| subgroup    | a model update adds 0.25 to the risk of the patient's subgroup | M2 (and M3)    |
| uncertainty | key fields blanked before scoring                              | M3             |
| drift       | one field recorded in the wrong unit, stream-wide              | M4             |
| duplicate   | the alert is sent again 10 minutes later at the same tier      | M5             |
| ungrounded  | a vital sign quoted in the alert differs from the record       | argument check |

Data faults change the record and/or the risk; the agent's later steps are kept as they were
but quote the faulty values, as an agent reading the faulty output would. ``Fault.effect``
says whether the injected risk is actually worse for this patient (> 0) or not.
"""

from __future__ import annotations

import zlib
from collections.abc import Callable
from typing import Any

import numpy as np
import pandas as pd

from ..agent.tools import ClinicalTools
from ..agent.types import Fault, Step, Trajectory
from ..data.settings import Setting
from ..gateway.timing import risk_tier

KINDS = ("sparse", "subgroup", "uncertainty", "drift", "duplicate", "ungrounded")
SUBGROUP_SHIFT = 0.25
SPARSE_SD = 6.0
DUPLICATE_DELAY_S = 600.0


def _rescore(traj: Trajectory, tools: ClinicalTools, edit: Callable[[dict], None],
             prob_map: Callable[[float], float] | None = None) -> tuple[float, float] | None:
    """Apply ``edit`` to the fetched record, rescore, and propagate. Returns (old, new) risk."""
    fetch, risk = traj.first("fetch_record"), traj.first("risk_score")
    if fetch is None or risk is None or not risk.hidden:
        return None
    record = dict(fetch.output)
    edit(record)
    prob, emb = tools.score_record(record)
    if prob_map is not None:
        prob = prob_map(prob)
    old = float(risk.hidden["probability"])
    tier = risk_tier(prob, tools.tier_cuts)
    fetch.output = record
    risk.output = {**risk.output, "probability": round(prob, 4), "risk_tier": tier}
    risk.hidden = {**risk.hidden, "probability": prob, "embedding": emb, "tier": tier}
    for step in traj.steps:
        if step.tool == "draft_alert":
            step.args["risk"] = round(prob, 4)
            step.args["cited"] = {k: record.get(k) for k in step.args.get("cited", {})}
    return old, prob


def _effect(y: int, old: float, new: float) -> float:
    return abs(new - y) - abs(old - y)


def inject(clean: Trajectory, kind: str, tools: ClinicalTools, setting: Setting,
           reference: pd.DataFrame) -> Trajectory | None:
    """Return a faulty copy of ``clean``, or None when the fault does not apply to it."""
    traj = clean.copy()
    risk = traj.first("risk_score")
    alert = traj.first("draft_alert")
    risk_index = risk.index if risk else -1
    fetch_index = traj.first("fetch_record").index if traj.first("fetch_record") else -1
    detail: dict[str, Any] = {}

    if kind == "sparse":
        med = reference[list(setting.numeric)].median()
        sd = reference[list(setting.numeric)].std()
        rng = np.random.default_rng(zlib.crc32(traj.trajectory_id.encode()))

        def edit(r: dict) -> None:
            for f in setting.numeric:
                if f != "age" and np.isfinite(sd[f]) and sd[f] > 0:
                    r[f] = float(med[f] + rng.choice([-1, 1]) * SPARSE_SD * sd[f])

        moved = _rescore(traj, tools, edit)
        context, step, origin = "normal", risk_index, fetch_index
    elif kind == "subgroup":
        moved = _rescore(traj, tools, lambda r: None,
                         lambda p: float(min(1.0, p + SUBGROUP_SHIFT)))
        context, step, origin = f"subgroup:{traj.group}", risk_index, risk_index
    elif kind == "uncertainty":
        def edit(r: dict) -> None:
            for f in setting.uncertainty_blank:
                r[f] = None

        moved = _rescore(traj, tools, edit)
        detail["blanked"] = list(setting.uncertainty_blank)
        context, step, origin = "normal", risk_index, fetch_index
    elif kind == "drift":
        field_, mult, offset = setting.unit_shift

        def edit(r: dict) -> None:
            if r.get(field_) is not None:
                r[field_] = float(r[field_]) * mult + offset

        moved = _rescore(traj, tools, edit)
        detail["field"] = field_
        context, step, origin = "drift", risk_index, fetch_index
    elif kind == "duplicate":
        if alert is None:
            return None
        dup = Step(alert.index + 1, alert.tool, dict(alert.args), dict(alert.output),
                   alert.clock + DUPLICATE_DELAY_S, dict(alert.hidden),
                   tokens=alert.tokens)  # resending costs another agent call
        traj.steps.insert(alert.index + 1, dup)
        for i, s in enumerate(traj.steps):
            s.index = i
        return _finish(traj, Fault(kind, dup.index, dup.index))
    elif kind == "ungrounded":
        if alert is None or not alert.args.get("cited"):
            return None
        name = next(iter(alert.args["cited"]))
        value = alert.args["cited"][name]
        alert.args["cited"] = {**alert.args["cited"],
                               name: (float(value) + 40.0) if value is not None else 999.0}
        return _finish(traj, Fault(kind, alert.index, alert.index, detail={"field": name}))
    else:
        raise ValueError(f"unknown fault {kind!r}")

    if moved is None:
        return None
    old, new = moved
    detail.update({"p_clean": old, "p_fault": new})
    return _finish(traj, Fault(kind, step, origin, context, _effect(traj.y, old, new), detail))


def _finish(traj: Trajectory, fault: Fault) -> Trajectory:
    traj.fault = fault
    traj.trajectory_id = f"{traj.trajectory_id}-{fault.kind}"
    return traj
