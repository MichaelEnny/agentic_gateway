"""M1: local calibration among the patient's nearest neighbours in embedding space.

Signal (spec para. [0020]): |mean predicted probability of the neighbours - observed outcome
rate of the neighbours|. The neighbourhood is a radius around the patient that grows until it
holds at least ``min_neighbors`` reference patients (the claim's adaptive expansion).

The starting radius is the median, over the reference cohort, of each patient's distance to its
``min_neighbors``-th neighbour, so a typical patient is satisfied on the first step and a patient
in a sparse region needs more steps. The number of steps is reported as a sparsity measure.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray
from sklearn.neighbors import NearestNeighbors


@dataclass(frozen=True)
class LocalCalibrationResult:
    value: float
    n_neighbors: int
    radius: float
    steps: int
    kth_distance: float
    sparse: bool


class LocalCalibration:
    def __init__(
        self,
        min_neighbors: int = 30,
        metric: str = "cosine",
        growth: float = 1.5,
        max_steps: int = 20,
        sparse_quantile: float = 0.95,
    ) -> None:
        if growth <= 1.0:
            raise ValueError("growth must exceed 1")
        self.min_neighbors = min_neighbors
        self.metric = metric
        self.growth = growth
        self.max_steps = max_steps
        self.sparse_quantile = sparse_quantile
        self._index: NearestNeighbors | None = None

    def fit(
        self,
        embeddings: NDArray[np.float64],
        probabilities: NDArray[np.float64],
        labels: NDArray[np.float64],
    ) -> LocalCalibration:
        """Index the reference cohort: its embeddings, model outputs and observed outcomes."""
        x = np.asarray(embeddings, dtype=np.float64)
        p = np.asarray(probabilities, dtype=np.float64).ravel()
        y = np.asarray(labels, dtype=np.float64).ravel()
        if x.ndim != 2 or not (x.shape[0] == p.size == y.size):
            raise ValueError("embeddings must be 2-D with one row per probability and label")
        if x.shape[0] <= self.min_neighbors:
            raise ValueError(
                f"reference cohort has {x.shape[0]} rows; needs more than {self.min_neighbors}"
            )
        self._index = NearestNeighbors(metric=self.metric, algorithm="brute").fit(x)
        self._probs = p
        self._labels = y

        # Leave-one-out distance to the k-th neighbour: column 0 is the point itself.
        dist, _ = self._index.kneighbors(x, n_neighbors=self.min_neighbors + 1)
        kth = dist[:, -1]
        self.base_radius_ = float(np.median(kth))
        self.sparse_radius_ = float(np.quantile(kth, self.sparse_quantile))
        if self.base_radius_ <= 0.0:
            # Many duplicate embeddings (common with leaf indices); any positive start works.
            positive = kth[kth > 0]
            self.base_radius_ = float(positive.min()) if positive.size else 1e-12
        return self

    def evaluate(self, embedding: NDArray[np.float64]) -> LocalCalibrationResult:
        if self._index is None:
            raise RuntimeError("call fit() first")
        q = np.asarray(embedding, dtype=np.float64).reshape(1, -1)

        kth_distance = float(
            self._index.kneighbors(q, n_neighbors=self.min_neighbors)[0][0, -1]
        )
        radius = self.base_radius_
        steps = 0
        while radius < kth_distance and steps < self.max_steps:
            radius *= self.growth
            steps += 1
        if radius < kth_distance:
            # Step budget exhausted: fall back to exactly the k nearest neighbours.
            idx = self._index.kneighbors(q, n_neighbors=self.min_neighbors)[1][0]
            radius = kth_distance
        else:
            idx = self._index.radius_neighbors(q, radius=radius)[1][0]

        value = abs(float(self._probs[idx].mean()) - float(self._labels[idx].mean()))
        return LocalCalibrationResult(
            value=value,
            n_neighbors=int(idx.size),
            radius=radius,
            steps=steps,
            kth_distance=kth_distance,
            sparse=kth_distance > self.sparse_radius_,
        )
