"""Benchmark construction: sample cases, run the agent in observe mode, inject faults."""

from __future__ import annotations

from collections import Counter
from collections.abc import Callable

import numpy as np
import pandas as pd

from ..agent.episode import run_episode
from ..agent.policy import Policy
from ..agent.tools import ClinicalTools
from ..agent.types import Trajectory
from ..data.settings import Setting
from .faults import KINDS, inject


def sample_cases(cases: pd.DataFrame, n: int, *, min_per_group: int, seed: int) -> pd.DataFrame:
    """Stratified by subgroup: each group gets ``min_per_group`` (or all it has), the rest is
    drawn in proportion. One case per patient, so trajectories are independent across patients
    apart from the seeds. Returns the sample with a ``weight`` column (population/sample)."""
    rng = np.random.default_rng(seed)
    one = cases.sample(frac=1.0, random_state=seed).drop_duplicates("patient_id")
    chosen = []
    for _, g in one.groupby("group", sort=True):
        chosen.append(g.head(min_per_group))
    base = pd.concat(chosen)
    rest = one.drop(base.index)
    extra = max(0, n - len(base))
    if extra and len(rest):
        base = pd.concat([base, rest.iloc[rng.permutation(len(rest))[:extra]]])
    base = base.copy()
    share_pop = one["group"].value_counts(normalize=True)
    share_smp = base["group"].value_counts(normalize=True)
    base["weight"] = base["group"].map(share_pop / share_smp)
    return base.reset_index(drop=True)


def build(tools: ClinicalTools, policy: Policy, sample: pd.DataFrame, setting: Setting,
          reference: pd.DataFrame, *, seeds: list[int],
          kinds: tuple[str, ...] = KINDS,
          progress: Callable[[Trajectory], None] | None = None) -> dict:
    clean: list[Trajectory] = []
    incomplete = 0
    for row in sample.itertuples():
        for seed in seeds:
            traj, _ = run_episode(policy, tools, str(row.case_id), setting=setting.name,
                                  seed=seed, y=int(row.y), group=str(row.group),
                                  patient_id=str(row.patient_id))
            if progress is not None:
                progress(traj)
            if traj.completed and traj.first("risk_score") is not None:
                clean.append(traj)
            else:
                incomplete += 1

    faulty: list[Trajectory] = []
    not_applicable: Counter[str] = Counter()
    for traj in clean:
        for kind in kinds:
            bad = inject(traj, kind, tools, setting, reference)
            if bad is None:
                not_applicable[kind] += 1
            else:
                faulty.append(bad)

    effects = pd.DataFrame([{"kind": t.fault.kind, "effect": t.fault.effect}
                            for t in faulty if t.fault and t.fault.effect is not None])
    worse = (effects.assign(worse=effects["effect"] > 0).groupby("kind")["worse"].mean()
             .round(3).to_dict()) if not effects.empty else {}
    manifest = {
        "cases": len(sample),
        "seeds": seeds,
        "policy": policy.name,
        "clean_trajectories": len(clean),
        "incomplete_runs": incomplete,
        "completion_rate": round(len(clean) / max(1, len(clean) + incomplete), 4),
        "faulty_trajectories": dict(Counter(t.kind for t in faulty)),
        "fault_not_applicable": dict(not_applicable),
        "share_where_fault_made_risk_worse": worse,
        "alerts_in_clean": sum(t.first("draft_alert") is not None for t in clean),
    }
    return {"clean": clean, "faulty": faulty, "manifest": manifest}
