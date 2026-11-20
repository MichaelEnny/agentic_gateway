"""Shared helpers for the peer-review analyses (rounds 1 and 2, electronics-4688310).

All analyses replay the stored tune/test benchmarks of the original study through gateway
variants. Nothing in the original pipeline is modified; outputs go to runs/revision/. Every variant is post hoc (decided after the reviews) and is reported
as such in the revised manuscript.
"""

from __future__ import annotations

import json
import sys
import time
from dataclasses import replace
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "experiments"))

import joblib
import numpy as np
import pandas as pd

from agentic_gateway.assembly import Artifacts, load_config
from agentic_gateway.benchmark import replay, summarise
from agentic_gateway.benchmark.analysis import per_trajectory
from agentic_gateway.benchmark.methods import full_factory, methods
from agentic_gateway.gateway import GatewayConfig
from agentic_gateway.workspace import Workspace, read_json

# Raw outputs (replay rows hold patient identifiers) go under runs/, which git ignores.
# Aggregate results are copied to results/revision/ by 99_export_results.py.
OUT = REPO / "runs" / "revision"
OUT.mkdir(parents=True, exist_ok=True)
RUN = {"ed": "qwen7b-ed-full-reduced-v1", "icu": "qwen7b-icu-full-reduced-v1"}
FAULTS = ("drift", "subgroup", "sparse", "uncertainty", "duplicate", "ungrounded")
N_BOOT = 2000
SEED = 42


class VariantArtifacts(Artifacts):
    """Artifacts whose drift states and SCDI tables can be replaced per variant."""

    def __init__(self, ws: Workspace, model_name: str, *, drift_override=None,
                 scdi_transform=None, cache_local: bool = True) -> None:
        super().__init__(ws, model_name, cache_local=cache_local)
        self.drift_override = drift_override or {}
        self.scdi_transform = scdi_transform

    def drift(self, name):  # type: ignore[override]
        if name in self.drift_override:
            return self.drift_override[name]
        return super().drift(name)

    def scdi(self, name):  # type: ignore[override]
        table = super().scdi(name)
        return self.scdi_transform(name, table) if self.scdi_transform else table


def workspace(setting: str) -> Workspace:
    return Workspace(setting, "full", False, RUN[setting])


def frozen(setting: str) -> tuple[GatewayConfig, float, dict]:
    ws = workspace(setting)
    path = ws.require("configs", "gateway_frozen.json")
    meta = read_json(path)["_meta"]
    return load_config(path), meta["confidence_cut"], meta


def bench(setting: str, part: str) -> dict:
    return joblib.load(workspace(setting).require("benchmark", f"{part}.joblib"))


def trajectories(setting: str, part: str) -> list:
    b = bench(setting, part)
    return b["clean"] + b["faulty"]


def with_cfg(cfg: GatewayConfig, **changes) -> GatewayConfig:
    return replace(cfg, **changes)


def without(cfg: GatewayConfig, *signals: str) -> GatewayConfig:
    for s in signals:
        cfg = cfg.without(s)
    return cfg


def run_variants(trajs: list, factories: dict, *, label: str, n_boot: int = N_BOOT,
                 reference: str | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    t0 = time.time()
    rows = replay(trajs, factories)
    ref = reference or next(iter(factories))
    table = summarise(rows, n_boot=n_boot, seed=SEED, reference=ref)
    rows.to_parquet(OUT / f"{label}_rows.parquet", index=False)
    table.to_csv(OUT / f"{label}_summary.csv", index=False)
    print(f"[{label}] {len(trajs)} trajectories x {len(factories)} methods "
          f"in {time.time() - t0:.0f}s")
    return rows, table


def wide(table: pd.DataFrame, metric: str = "early", kinds=FAULTS) -> pd.DataFrame:
    """Methods x fault types, plus the mean over faults and false intervention."""
    t = table[(table["metric"] == metric) & table["kind"].isin(kinds)]
    w = t.pivot(index="method", columns="kind", values="estimate")
    w = w.reindex(columns=[k for k in kinds if k in w.columns])
    w["mean_" + metric] = w.mean(axis=1)
    fi = table[table["metric"] == "false_intervention"].set_index("method")
    w["false_intervention"] = fi["estimate"]
    w["fi_low"], w["fi_high"] = fi["ci_low"], fi["ci_high"]
    order = list(dict.fromkeys(table["method"]))
    return w.reindex(order)


def save_json(obj, name: str) -> None:
    def default(o):
        if isinstance(o, (np.floating, np.integer)):
            return o.item()
        return str(o)
    (OUT / name).write_text(json.dumps(obj, indent=2, default=default), encoding="utf-8")


__all__ = [
    "FAULTS",
    "OUT",
    "REPO",
    "VariantArtifacts",
    "bench",
    "frozen",
    "full_factory",
    "methods",
    "np",
    "pd",
    "per_trajectory",
    "replay",
    "run_variants",
    "save_json",
    "summarise",
    "trajectories",
    "wide",
    "with_cfg",
    "without",
    "workspace",
]
