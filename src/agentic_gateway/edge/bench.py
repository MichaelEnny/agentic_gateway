"""Latency, memory and (with an external meter) energy of the gate on this machine.

Run the same command on each board. Energy needs a logging power meter: pass its CSV
(``timestamp`` in epoch seconds, ``watts``) and the window of each measurement block is
integrated. Without a meter, energy is reported as missing, never estimated.

Memory is reported two ways:

* :func:`peak_rss_mb`: the operating system's high-water mark for the whole process. It never
  goes down, so it bounds what the board must have, but it includes Python, numpy and sklearn.
* :func:`traced_peak_mb`: the peak of Python and numpy allocations while one block runs,
  measured with ``tracemalloc``. It isolates one component (for example the M1 index at one
  reference size). Tracing slows code down, so it runs apart from the latency measurements.
"""

from __future__ import annotations

import gc
import os
import platform
import sys
import time
import tracemalloc
from collections.abc import Callable
from pathlib import Path

import numpy as np
import pandas as pd
import psutil

from ..agent.types import Trajectory
from ..benchmark.methods import GateFactory
from ..gateway import LocalCalibration

MEMORY_QUERIES = 20  # queries traced for memory; tracing is slow, and one query's peak is enough


def peak_rss_mb() -> float:
    """Peak resident memory of this process so far, in MiB (Windows peak working set, or
    ``ru_maxrss`` on Linux and macOS)."""
    info = psutil.Process(os.getpid()).memory_info()
    if hasattr(info, "peak_wset"):
        return info.peak_wset / 2**20
    import resource  # not on Windows

    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return peak / 2**20 if sys.platform == "darwin" else peak / 2**10  # bytes vs KiB


def traced_peak_mb(block: Callable[[], object]) -> float:
    """Peak MiB of Python and numpy allocations made while ``block`` runs."""
    gc.collect()
    already = tracemalloc.is_tracing()
    if not already:
        tracemalloc.start()
    try:
        tracemalloc.reset_peak()
        base = tracemalloc.get_traced_memory()[0]
        block()
        return (tracemalloc.get_traced_memory()[1] - base) / 2**20
    finally:
        if not already:
            tracemalloc.stop()


def time_actions(trajectories: list[Trajectory], factory: GateFactory, *, repeats: int,
                 warmup: int) -> tuple[pd.DataFrame, tuple[float, float]]:
    """Check every step of every trajectory ``repeats`` times. One row per gated action."""
    rows = []
    steps = [(t, s) for t in trajectories for s in t.steps]
    gates = {}
    for t, s in steps[:warmup]:
        gates.setdefault(t.trajectory_id, factory(t.fault.context if t.fault else "normal"))
        gates[t.trajectory_id].check(s)
    gc.collect()
    started = time.time()
    for r in range(repeats):
        for t in trajectories:
            gate = factory(t.fault.context if t.fault else "normal")
            gate.reset()
            for s in t.steps:
                v = gate.check(s)
                row = {"repeat": r, "trajectory_id": t.trajectory_id, "tool": s.tool,
                       "decision": v.decision.value, "latency_ns": v.latency_ns}
                for key, value in v.record.items():
                    if key.endswith(".latency_ns"):
                        row[key] = value
                rows.append(row)
    return pd.DataFrame(rows), (started, time.time())


def m1_scaling(embeddings: np.ndarray, probs: np.ndarray, labels: np.ndarray, metric: str,
               sizes: list[int], queries: np.ndarray, min_neighbors: int,
               seed: int = 0) -> pd.DataFrame:
    """M1 latency and memory against the size of the reference cohort.

    Memory, measured in untimed passes after the latency loop:

    * ``fit_peak_mb``: traced peak while building the index. Building is offline (step 3), and
      sklearn computes neighbour distances in chunks of up to ``working_memory`` (1 GiB by
      default), so this can be large without mattering at the bedside;
    * ``query_peak_mb``: traced peak while answering ``MEMORY_QUERIES`` queries on the built
      index, which is the run-time cost;
    * ``process_peak_mb``: the process high-water mark so far (includes every earlier fit)."""
    rng = np.random.default_rng(seed)
    out = []
    for n in sizes:
        if n > len(embeddings):
            continue
        idx = rng.choice(len(embeddings), n, replace=False)
        local = LocalCalibration(min_neighbors=min_neighbors, metric=metric).fit(
            embeddings[idx], probs[idx], labels[idx])
        lat = []
        for q in queries:
            t0 = time.perf_counter_ns()
            local.evaluate(q)
            lat.append(time.perf_counter_ns() - t0)
        lat = np.array(lat) / 1e6
        del local

        built: dict[str, LocalCalibration] = {}

        def fit(idx=idx, built=built) -> None:
            built["m1"] = LocalCalibration(min_neighbors=min_neighbors, metric=metric).fit(
                embeddings[idx], probs[idx], labels[idx])

        def query(built=built) -> None:
            for q in queries[:MEMORY_QUERIES]:
                built["m1"].evaluate(q)

        fit_mb = traced_peak_mb(fit)
        query_mb = traced_peak_mb(query)
        built.clear()
        out.append({"reference_size": n, "p50_ms": np.median(lat),
                    "p95_ms": np.percentile(lat, 95), "fit_peak_mb": fit_mb,
                    "query_peak_mb": query_mb, "process_peak_mb": peak_rss_mb()})
    return pd.DataFrame(out)


def energy_mj(meter_csv: Path | None, window: tuple[float, float], n_actions: int) -> float:
    if meter_csv is None or n_actions == 0:
        return float("nan")
    m = pd.read_csv(meter_csv)
    m = m[(m["timestamp"] >= window[0]) & (m["timestamp"] <= window[1])].sort_values("timestamp")
    if len(m) < 2:
        return float("nan")
    joules = np.trapezoid(m["watts"].to_numpy(), m["timestamp"].to_numpy())
    return float(joules * 1000 / n_actions)


def summarise(actions: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for tool, part in [("all", actions), *actions.groupby("tool")]:
        lat = part["latency_ns"].to_numpy() / 1e6
        row = {"tool": tool, "n": len(part), "p50_ms": np.median(lat),
               "p95_ms": np.percentile(lat, 95), "p99_ms": np.percentile(lat, 99)}
        for col in [c for c in part.columns if c.endswith(".latency_ns")]:
            vals = part[col].dropna().to_numpy() / 1e6
            if vals.size:
                row[f"{col.split('.')[0]}_p50_ms"] = np.median(vals)
        rows.append(row)
    return pd.DataFrame(rows)


def machine() -> dict:
    return {"platform": platform.platform(), "machine": platform.machine(),
            "processor": platform.processor(), "cpus": os.cpu_count(),
            "ram_gb": round(psutil.virtual_memory().total / 2**30, 1)}
