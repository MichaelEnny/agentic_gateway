"""Step 5 selection rule and the M1 cache it uses."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from agentic_gateway.assembly import _CachedLocal
from agentic_gateway.gateway import LocalCalibration

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))
select = importlib.import_module("05_tune_thresholds").select


def _grid(rows):
    return pd.DataFrame(rows, columns=["local_threshold", "conformal_coverage", "scdi_multiple",
                                       "scdi_threshold", "intercepted", "false_intervention"])


def test_select_best_interception_under_cap():
    grid = _grid([
        (0.10, 0.8, 1.0, 2.4, 0.95, 0.50),  # most faults caught, but over the cap
        (0.10, 0.8, 2.0, 4.8, 0.80, 0.08),
        (0.10, 0.8, 3.0, 7.2, 0.70, 0.05),
    ])
    best, cap_met = select(grid, 0.10)
    assert cap_met and best["scdi_threshold"] == 4.8


def test_select_ties_go_to_scdi_closest_to_null():
    grid = _grid([
        (0.10, 0.8, 2.5, 6.0, 0.80, 0.08),
        (0.10, 0.8, 2.0, 4.8, 0.80, 0.08),
    ])
    best, _ = select(grid, 0.10)
    assert best["scdi_multiple"] == 2.0


def test_select_reports_cap_not_met():
    grid = _grid([
        (0.10, 0.8, 1.0, 2.4, 0.95, 0.60),
        (0.20, 0.8, 1.0, 2.4, 0.90, 0.40),
    ])
    best, cap_met = select(grid, 0.10)
    assert not cap_met and best["false_intervention"] == 0.40


def test_cached_local_matches_uncached_and_searches_once():
    rng = np.random.default_rng(0)
    x = rng.normal(size=(300, 2))
    local = LocalCalibration(min_neighbors=20, metric="euclidean").fit(
        x, rng.uniform(size=300), rng.integers(0, 2, 300).astype(float))
    calls = {"n": 0}
    inner = local.evaluate

    def counted(e):  # type: ignore[no-untyped-def]
        calls["n"] += 1
        return inner(e)

    local.evaluate = counted  # type: ignore[method-assign]
    cached = _CachedLocal(local)
    q = np.array([0.3, -0.2])
    first, again = cached.evaluate(q), cached.evaluate(q.copy())
    assert first == again == inner(q)
    assert calls["n"] == 1
    assert cached.min_neighbors == 20  # other attributes pass through
