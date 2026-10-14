"""M4: background drift job that writes a cached state, and the reader the gateway calls.

The job (spec paras. [0026]-[0027]) tests three families of hypotheses against a reference
window and corrects them together with Benjamini-Hochberg:

* input drift, one test per feature: two-sample KS for numeric, chi-square for categorical;
* output drift: KS on the predicted probabilities;
* calibration drift: bootstrap test of the change in ECE, overall and per subgroup. Skipped
  (p = NaN, which BH excludes) when outcomes for the current window are not yet known.

PSI and KL are recorded for every input and output test as effect sizes. The state is:

* ``critical`` if any calibration hypothesis is rejected, or any rejected input/output test has
  PSI >= ``psi_critical``;
* ``warning`` if anything else is rejected;
* ``none`` otherwise.

The gateway never runs any of this on the request path; it reads the cached JSON.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd
from numpy.typing import NDArray
from scipy import stats

from ..metrics import benjamini_hochberg, ece, kl_divergence, psi, reference_edges

SCHEMA_VERSION = 1
STATES = ("none", "warning", "critical")
_EPS = 1e-6  # floor on bin proportions so PSI and KL stay finite


@dataclass(frozen=True)
class DriftTest:
    family: str  # "input", "output" or "calibration"
    target: str  # feature name, "probability", or "ece:<group>"
    p_value: float
    q_value: float
    rejected: bool
    psi: float | None = None
    kl: float | None = None
    delta: float | None = None  # ECE change for calibration tests


@dataclass(frozen=True)
class DriftState:
    state: str
    computed_at: float
    window: str
    alpha: float
    tests: list[DriftTest] = field(default_factory=list)

    def save(self, path: str | Path) -> None:
        payload = {"schema_version": SCHEMA_VERSION, **asdict(self)}
        Path(path).write_text(json.dumps(payload, indent=2, allow_nan=True), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> DriftState:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        version = payload.pop("schema_version", None)
        if version != SCHEMA_VERSION:
            raise ValueError(f"drift state schema {version}, expected {SCHEMA_VERSION}")
        tests = [DriftTest(**t) for t in payload.pop("tests")]
        return cls(tests=tests, **payload)


def _proportions(ref: NDArray[np.float64], cur: NDArray[np.float64], edges: NDArray[np.float64]):
    r = np.histogram(ref, bins=edges)[0].astype(np.float64)
    c = np.histogram(cur, bins=edges)[0].astype(np.float64)
    return _smooth(r), _smooth(c), r, c


def _smooth(counts: NDArray[np.float64]) -> NDArray[np.float64]:
    share = np.maximum(counts / max(counts.sum(), 1.0), _EPS)
    return share / share.sum()


def _numeric_test(ref: NDArray[np.float64], cur: NDArray[np.float64], n_bins: int):
    edges = reference_edges(ref, n_bins)
    r, c, _, _ = _proportions(ref, cur, edges)
    p_value = float(stats.ks_2samp(ref, cur).pvalue)
    return p_value, psi(r, c), kl_divergence(r, c)


def _categorical_test(ref: pd.Series, cur: pd.Series):
    levels = sorted(set(ref.astype(str)) | set(cur.astype(str)))
    rc = np.array([(ref.astype(str) == v).sum() for v in levels], dtype=np.float64)
    cc = np.array([(cur.astype(str) == v).sum() for v in levels], dtype=np.float64)
    if len(levels) < 2:
        p_value = 1.0
    else:
        p_value = float(stats.chi2_contingency(np.vstack([rc, cc]) + 0.5)[1])
    r, c = _smooth(rc), _smooth(cc)
    return p_value, psi(r, c), kl_divergence(r, c)


def _ece_change_test(
    y_ref, p_ref, y_cur, p_cur, n_boot: int, rng: np.random.Generator
) -> tuple[float, float]:
    """Two-sided bootstrap p-value for ECE(current) - ECE(reference) = 0."""
    observed = ece(y_cur, p_cur) - ece(y_ref, p_ref)
    diffs = np.empty(n_boot)
    for b in range(n_boot):
        i = rng.integers(0, y_ref.size, y_ref.size)
        j = rng.integers(0, y_cur.size, y_cur.size)
        diffs[b] = ece(y_cur[j], p_cur[j]) - ece(y_ref[i], p_ref[i])
    # Share of resamples on the other side of zero, doubled, with the +1 correction.
    tail = min((diffs <= 0).sum(), (diffs >= 0).sum())
    return float(min(1.0, 2.0 * (tail + 1) / (n_boot + 1))), float(observed)


def run_drift_job(
    reference: pd.DataFrame,
    current: pd.DataFrame,
    *,
    features: list[str],
    probability: str = "probability",
    label: str | None = "label",
    group: str | None = "group",
    alpha: float = 0.05,
    psi_critical: float = 0.25,
    n_bins: int = 10,
    n_boot: int = 500,
    min_group_size: int = 50,
    computed_at: float = 0.0,
    window: str = "",
    seed: int = 0,
) -> DriftState:
    """Compare ``current`` against ``reference`` and return the state to cache."""
    rng = np.random.default_rng(seed)
    raw: list[dict] = []

    for name in features:
        ref, cur = reference[name].dropna(), current[name].dropna()
        if ref.empty or cur.empty:
            raw.append({"family": "input", "target": name, "p_value": math.nan})
            continue
        if pd.api.types.is_numeric_dtype(ref) and ref.nunique() > 2:
            p_value, s, k = _numeric_test(ref.to_numpy(float), cur.to_numpy(float), n_bins)
        else:
            p_value, s, k = _categorical_test(ref, cur)
        raw.append({"family": "input", "target": name, "p_value": p_value, "psi": s, "kl": k})

    p_value, s, k = _numeric_test(
        reference[probability].to_numpy(float), current[probability].to_numpy(float), n_bins
    )
    raw.append({"family": "output", "target": "probability", "p_value": p_value, "psi": s, "kl": k})

    labelled = label is not None and current[label].notna().any()
    if labelled:
        ref_l = reference.dropna(subset=[label])
        cur_l = current.dropna(subset=[label])
        slices: list[tuple[str, pd.DataFrame, pd.DataFrame]] = [("overall", ref_l, cur_l)]
        if group is not None:
            for g in sorted(set(ref_l[group]) & set(cur_l[group])):
                r_g, c_g = ref_l[ref_l[group] == g], cur_l[cur_l[group] == g]
                if len(r_g) >= min_group_size and len(c_g) >= min_group_size:
                    slices.append((str(g), r_g, c_g))
        for name, r, c in slices:
            p_value, delta = _ece_change_test(
                r[label].to_numpy(float),
                r[probability].to_numpy(float),
                c[label].to_numpy(float),
                c[probability].to_numpy(float),
                n_boot,
                rng,
            )
            raw.append(
                {"family": "calibration", "target": f"ece:{name}", "p_value": p_value,
                 "delta": delta}
            )

    q_values = benjamini_hochberg([t["p_value"] for t in raw])
    tests = [
        DriftTest(
            q_value=float(q),
            rejected=bool(np.isfinite(q) and q <= alpha),
            **t,
        )
        for t, q in zip(raw, q_values)
    ]

    rejected = [t for t in tests if t.rejected]
    # A rejected calibration test only escalates when ECE got worse; improvement is not harm.
    critical = any(t.family == "calibration" and (t.delta or 0.0) > 0 for t in rejected) or any(
        t.psi is not None and t.psi >= psi_critical for t in rejected
    )
    state = "critical" if critical else ("warning" if rejected else "none")
    return DriftState(state=state, computed_at=computed_at, window=window, alpha=alpha,
                      tests=tests)


class DriftStateReader:
    """Request-path reader. Returns the cached state, or None if missing or stale."""

    def __init__(self, path: str | Path | None = None, state: DriftState | None = None) -> None:
        if (path is None) == (state is None):
            raise ValueError("give exactly one of path or state")
        self.path = Path(path) if path is not None else None
        self._state = state
        self._mtime: float | None = None

    def read(self, now: float, max_age_s: float) -> DriftState | None:
        if self.path is not None:
            if not self.path.exists():
                return None
            mtime = self.path.stat().st_mtime
            if mtime != self._mtime:  # reload only when the background job rewrote the file
                self._state = DriftState.load(self.path)
                self._mtime = mtime
        state = self._state
        if state is None or now - state.computed_at > max_age_s or state.state not in STATES:
            return None
        return state
