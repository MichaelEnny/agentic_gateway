"""M3: group-conditional (Mondrian) split conformal prediction sets for a binary outcome.

Each subgroup gets its own nonconformity quantile (spec para. [0023]), so the coverage
guarantee holds within the patient's subgroup rather than only on average over everyone.
Nonconformity is the LAC score 1 - p(label), from ``agentic_gateway.metrics``, so pooled and
Mondrian results in the paper use the same score.

A subgroup too small to attain the target coverage gets the threshold 1.0, which puts both
labels in every set. That is the honest answer: there is not enough calibration data to be
confident, and the gateway defers. ``pooled_fallback=True`` uses the pooled quantile instead;
the paper must report which option was used.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from ..metrics import conformal_quantile, minimum_calibration_size, nonconformity


@dataclass(frozen=True)
class ConformalResult:
    prediction_set: tuple[int, ...]
    set_size: int
    quantile: float
    source: str  # "group", "pooled_fallback" or "full_set"
    n_calibration: int


class MondrianConformal:
    def __init__(self, coverage: float = 0.90, pooled_fallback: bool = False) -> None:
        self.coverage = coverage
        self.pooled_fallback = pooled_fallback
        self.quantiles_: dict[str, float] = {}
        self.sizes_: dict[str, int] = {}
        self.notes_: dict[str, str] = {}
        self.pooled_quantile_: float | None = None

    def fit(
        self,
        labels: NDArray[np.float64],
        probabilities: NDArray[np.float64],
        groups: NDArray[np.str_] | list[str],
    ) -> MondrianConformal:
        """Calibrate on the conformal-calibration split only."""
        y = np.asarray(labels, dtype=np.float64).ravel()
        p = np.asarray(probabilities, dtype=np.float64).ravel()
        g = np.asarray(groups, dtype=object).ravel()
        if not (y.size == p.size == g.size):
            raise ValueError("labels, probabilities and groups must have the same length")

        scores = nonconformity(y, p)
        self.pooled_quantile_, _ = conformal_quantile(scores, self.coverage)
        floor = minimum_calibration_size(self.coverage)
        self.min_size_ = floor
        for name in sorted(set(g.tolist())):
            mask = g == name
            n = int(mask.sum())
            self.sizes_[str(name)] = n
            if n < floor:
                self.notes_[str(name)] = f"{n} < {floor} needed for {self.coverage:.0%} coverage"
                continue
            q, note = conformal_quantile(scores[mask], self.coverage)
            self.quantiles_[str(name)] = q
            if note:
                self.notes_[str(name)] = note
        return self

    def predict(self, probability: float, group: str) -> ConformalResult:
        if self.pooled_quantile_ is None:
            raise RuntimeError("call fit() first")
        if group in self.quantiles_:
            q, source = self.quantiles_[group], "group"
        elif self.pooled_fallback:
            q, source = self.pooled_quantile_, "pooled_fallback"
        else:
            q, source = 1.0, "full_set"

        # Score of label 1 is 1 - p, score of label 0 is p. A label is in the set when its
        # score does not exceed the quantile.
        members = tuple(
            label for label, score in ((0, probability), (1, 1.0 - probability)) if score <= q
        )
        return ConformalResult(
            prediction_set=members,
            set_size=len(members),
            quantile=float(q),
            source=source,
            n_calibration=self.sizes_.get(group, 0),
        )

    def predict_many(
        self, probabilities: NDArray[np.float64], groups: NDArray[np.str_] | list[str]
    ) -> list[ConformalResult]:
        return [self.predict(float(p), str(g)) for p, g in zip(probabilities, groups)]
