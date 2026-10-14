"""Statistical building blocks used by the gateway and the analysis.

Self-contained on purpose: this repository is released with the paper and depends on nothing
unpublished. Every function here has a closed-form check in ``tests/test_metrics.py``.
"""

from __future__ import annotations

import math
from collections.abc import Sequence

import numpy as np
from numpy.typing import ArrayLike, NDArray

ECE_BINS = 10
_EPS = 1e-9  # guards ceil() against 0.9 * 10 = 9.000000000000002


def _arrays(y: ArrayLike, p: ArrayLike) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    y = np.asarray(y, dtype=np.float64).ravel()
    p = np.asarray(p, dtype=np.float64).ravel()
    if y.size != p.size:
        raise ValueError("labels and probabilities differ in length")
    if p.size and (np.any(p < 0) or np.any(p > 1) or not np.all(np.isfinite(p))):
        raise ValueError("probabilities must be finite and lie in [0, 1]")
    return y, p


def ece(y: ArrayLike, p: ArrayLike, n_bins: int = ECE_BINS) -> float:
    """Expected calibration error with equal-width bins.

    Sum over bins of |sum of probabilities - number of events|, divided by n. Bins are
    half-open on the right except the last, so p = 1 falls in the top bin.
    """
    y, p = _arrays(y, p)
    if y.size == 0:
        return 0.0
    idx = np.minimum((p * n_bins).astype(int), n_bins - 1)
    prob_sums = np.bincount(idx, weights=p, minlength=n_bins)
    event_sums = np.bincount(idx, weights=y, minlength=n_bins)
    return float(np.abs(prob_sums - event_sums).sum() / y.size)


def brier(y: ArrayLike, p: ArrayLike) -> float:
    y, p = _arrays(y, p)
    return float(np.mean((p - y) ** 2)) if y.size else float("nan")


def auroc(y: ArrayLike, p: ArrayLike) -> float:
    """Mann-Whitney AUROC with ties counted as one half; NaN if one class is absent."""
    y, p = _arrays(y, p)
    pos, neg = p[y == 1], p[y == 0]
    if pos.size == 0 or neg.size == 0:
        return float("nan")
    order = np.argsort(np.concatenate([pos, neg]), kind="mergesort")
    ranks = np.empty(order.size)
    values = np.concatenate([pos, neg])[order]
    # average ranks over ties
    i = 0
    while i < values.size:
        j = i
        while j + 1 < values.size and values[j + 1] == values[i]:
            j += 1
        ranks[order[i : j + 1]] = (i + j) / 2.0 + 1.0
        i = j + 1
    rank_pos = ranks[: pos.size].sum()
    return float((rank_pos - pos.size * (pos.size + 1) / 2) / (pos.size * neg.size))


# -- conformal ---------------------------------------------------------------------------


def nonconformity(y: ArrayLike, p: ArrayLike) -> NDArray[np.float64]:
    """LAC score of the observed label: 1 - p(observed label)."""
    y, p = _arrays(y, p)
    return np.where(y == 1.0, 1.0 - p, p)


def minimum_calibration_size(coverage: float) -> int:
    """Smallest n for which split conformal can attain ``coverage`` at all."""
    n = 1
    while math.ceil((n + 1) * coverage - _EPS) > n:
        n += 1
    return n


def conformal_quantile(scores: ArrayLike, coverage: float) -> tuple[float, str]:
    """Finite-sample-corrected split-conformal threshold.

    Returns the ceil((n + 1) * coverage)-th smallest score. When that rank exceeds n no finite
    threshold attains the coverage; the function returns 1.0 (every label admitted, since LAC
    scores lie in [0, 1]) and a note saying so.
    """
    s = np.sort(np.asarray(scores, dtype=np.float64).ravel())
    if s.size == 0:
        raise ValueError("no calibration scores")
    rank = math.ceil((s.size + 1) * coverage - _EPS)
    if rank > s.size:
        return 1.0, f"{s.size} scores cannot attain {coverage:.0%} coverage"
    return float(s[rank - 1]), ""


# -- drift -------------------------------------------------------------------------------


def reference_edges(values: ArrayLike, n_bins: int = 10) -> NDArray[np.float64]:
    """Equal-mass bin edges from the reference window, open at both ends.

    Interior edges are reference quantiles taken at observed values; duplicates (ties) are
    dropped, so a heavily tied feature gets fewer bins. Outer edges are infinite so values
    outside the reference range are counted, not lost.
    """
    v = np.asarray(values, dtype=np.float64)
    v = v[np.isfinite(v)]
    if v.size == 0:
        raise ValueError("no finite reference values")
    inner = np.quantile(v, np.linspace(0, 1, n_bins + 1)[1:-1], method="lower")
    inner = np.unique(inner[inner > v.min()])
    return np.concatenate([[-np.inf], inner, [np.inf]])


def psi(reference: NDArray[np.float64], current: NDArray[np.float64]) -> float:
    """Population stability index between two proportion vectors (no zeros)."""
    return float(np.sum((current - reference) * np.log(current / reference)))


def kl_divergence(reference: NDArray[np.float64], current: NDArray[np.float64]) -> float:
    """KL(current || reference) in nats."""
    return float(np.sum(current * np.log(current / reference)))


def benjamini_hochberg(p_values: Sequence[float]) -> NDArray[np.float64]:
    """BH-adjusted p-values. NaN entries are not tests: passed through, not counted."""
    p = np.asarray(list(p_values), dtype=np.float64)
    out = np.full(p.shape, np.nan)
    ok = np.flatnonzero(np.isfinite(p))
    m = ok.size
    if m == 0:
        return out
    order = np.argsort(p[ok], kind="stable")
    scaled = p[ok][order] * m / np.arange(1, m + 1)
    adjusted = np.minimum(np.minimum.accumulate(scaled[::-1])[::-1], 1.0)
    out[ok[order]] = adjusted
    return out


def holm(p_values: Sequence[float]) -> NDArray[np.float64]:
    """Holm step-down adjusted p-values; NaN passed through."""
    p = np.asarray(list(p_values), dtype=np.float64)
    out = np.full(p.shape, np.nan)
    ok = np.flatnonzero(np.isfinite(p))
    m = ok.size
    if m == 0:
        return out
    order = np.argsort(p[ok], kind="stable")
    scaled = p[ok][order] * (m - np.arange(m))
    adjusted = np.minimum(np.maximum.accumulate(scaled), 1.0)
    out[ok[order]] = adjusted
    return out
