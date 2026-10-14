"""Quality of the predictions a gate lets through, and how often conformal sets are ambiguous.

* :func:`set_size_shares`: for each coverage level, the share of conformal prediction sets
  holding both labels (ambiguous: M3 breaches) or no label (also a breach), overall and per
  subgroup, for Mondrian and pooled conformal. Explains how often M3 alone defers (guide 6.1).
* :func:`prediction_quality`: ECE, Brier, AUROC and conformal coverage of a set of predictions.
* :func:`passed_quality`: per gating method, the quality of the risk predictions in
  trajectories the gate let through (no interception, so the case was acted on without
  clinician review) against those it stopped. The plan's "downstream quality" metric.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any

import numpy as np
import pandas as pd

from .gateway.conformal import MondrianConformal
from .metrics import auroc, brier, ece

ConformalFor = Callable[[float, bool], MondrianConformal]  # (coverage, pooled) -> fitted


def _sizes(conformal: MondrianConformal, probs: np.ndarray, groups: np.ndarray,
           pooled: bool) -> np.ndarray:
    return np.array([conformal.predict(float(p), "all" if pooled else str(g)).set_size
                     for p, g in zip(probs, groups)])


def _shares(sizes: np.ndarray) -> dict[str, Any]:
    n = int(sizes.size)
    return {"n": n,
            "two_label": float((sizes == 2).mean()) if n else float("nan"),
            "empty": float((sizes == 0).mean()) if n else float("nan")}


def set_size_shares(conformal_for: ConformalFor, coverages: Iterable[float],
                    probs: np.ndarray, groups: np.ndarray) -> dict[str, Any]:
    """{coverage: {"mondrian"|"pooled": {"_all": shares, group: shares, ...}}}."""
    probs, groups = np.asarray(probs, dtype=float), np.asarray(groups).astype(str)
    out: dict[str, Any] = {}
    for coverage in coverages:
        level: dict[str, Any] = {}
        for label, pooled in (("mondrian", False), ("pooled", True)):
            sizes = _sizes(conformal_for(coverage, pooled), probs, groups, pooled)
            per = {"_all": _shares(sizes)}
            for g in sorted(set(groups)):
                per[g] = _shares(sizes[groups == g])
            level[label] = per
        out[f"{coverage:.2f}"] = level
    return out


def prediction_quality(y: np.ndarray, p: np.ndarray, groups: np.ndarray,
                       conformal: MondrianConformal | None = None) -> dict[str, Any]:
    y, p = np.asarray(y, dtype=float), np.asarray(p, dtype=float)
    groups = np.asarray(groups).astype(str)
    if y.size == 0:
        return {"n": 0, "ece": float("nan"), "brier": float("nan"), "auroc": float("nan")}
    out: dict[str, Any] = {"n": int(y.size), "ece": ece(y, p), "brier": brier(y, p),
                           "auroc": auroc(y, p)}
    if conformal is not None:
        hits = np.array([int(t) in conformal.predict(float(q), str(g)).prediction_set
                         for t, q, g in zip(y, p, groups)])
        out["coverage"] = {"_all": float(hits.mean())}
        for g in sorted(set(groups)):
            mask = groups == g
            out["coverage"][g] = {"n": int(mask.sum()), "coverage": float(hits[mask].mean())}
    return out


def passed_quality(rows: pd.DataFrame, conformal: MondrianConformal) -> dict[str, Any]:
    """{method: {"clean"|"faulty"|"all": {"passed": quality, "stopped": quality}}}.

    ``rows`` are replay rows with ``risk_prob``, ``y``, ``group``, ``kind`` and
    ``intercept_step``. A trajectory passed if nothing in it was intercepted. Trajectories
    without a risk prediction are left out. For data faults the prediction is the faulty one,
    which is the point: a gate that lets faulty predictions through will show it here."""
    df = rows[rows["risk_prob"].notna()]
    out: dict[str, Any] = {}
    for method, part in df.groupby("method", sort=False):
        per: dict[str, Any] = {}
        subsets = {"clean": part[part["kind"] == "clean"],
                   "faulty": part[part["kind"] != "clean"], "all": part}
        for name, sub in subsets.items():
            passed = sub["intercept_step"] < 0
            per[name] = {
                label: prediction_quality(s["y"].to_numpy(), s["risk_prob"].to_numpy(),
                                          s["group"].to_numpy(), conformal)
                for label, s in (("passed", sub[passed]), ("stopped", sub[~passed]))}
        out[str(method)] = per
    return out
