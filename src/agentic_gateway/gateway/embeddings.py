"""Embedding vectors for M1, taken from the risk model itself (PRD section 3, Module 1).

| Model family                  | Embedding                              | Metric   |
|-------------------------------|----------------------------------------|----------|
| sklearn tree ensembles        | leaf index per tree (``.apply``)       | hamming  |
| XGBoost / LightGBM            | leaf index per tree (``pred_leaf``)    | hamming  |
| LogisticRegression            | per-feature contribution ``coef * x``  | cosine   |
| GaussianNB                    | per-feature log-likelihood difference  | cosine   |
| Neural network                | penultimate activations (pass a hook)  | cosine   |

Leaf indices are labels, not magnitudes, so they use Hamming distance: the share of trees in
which two patients land in different leaves. Cosine on leaf indices would be meaningless.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True)
class Embedder:
    transform: Callable[[NDArray[np.float64]], NDArray[np.float64]]
    metric: str
    kind: str


def _dense(x: object) -> NDArray[np.float64]:
    """ColumnTransformer output can be sparse (the complaint text features)."""
    return np.asarray(x.toarray() if hasattr(x, "toarray") else x, dtype=np.float64)


def _leaf_matrix(leaves: NDArray) -> NDArray[np.float64]:
    leaves = np.asarray(leaves)
    return leaves.reshape(leaves.shape[0], -1).astype(np.float64)


def embedder_for(model: object, hook: Callable[[NDArray[np.float64]], NDArray[np.float64]]
                 | None = None) -> Embedder:
    """Pick the embedding for a fitted model. ``hook`` overrides it (e.g. a NN layer)."""
    if hook is not None:
        return Embedder(hook, "cosine", "hook")

    if hasattr(model, "steps"):
        # sklearn Pipeline (the ED and ICU models in agentic_gateway.models): run the fitted preprocessing,
        # then take the embedding from the final estimator.
        prefix, inner = model[:-1], embedder_for(model[-1])
        return Embedder(lambda x: inner.transform(_dense(prefix.transform(x))), inner.metric,
                        inner.kind)

    name = type(model).__name__
    if name == "HistGradientBoostingClassifier":
        raise TypeError(
            "HistGradientBoostingClassifier exposes no public leaf indices; use random forest, "
            "XGBoost or LightGBM for the tree embedding, or pass hook="
        )
    if name in {"XGBClassifier", "XGBRegressor"}:
        return Embedder(lambda x: _leaf_matrix(model.apply(x)), "hamming", "xgboost_leaf")
    if name in {"LGBMClassifier", "LGBMRegressor"}:
        return Embedder(
            lambda x: _leaf_matrix(model.predict(x, pred_leaf=True)), "hamming", "lightgbm_leaf"
        )
    if hasattr(model, "estimators_") and hasattr(model, "apply"):
        return Embedder(lambda x: _leaf_matrix(model.apply(x)), "hamming", "sklearn_leaf")
    if name == "LogisticRegression":
        coef = np.asarray(model.coef_, dtype=np.float64)
        if coef.shape[0] != 1:
            raise ValueError("only binary logistic regression is supported")
        return Embedder(lambda x: np.asarray(x, dtype=np.float64) * coef[0], "cosine",
                        "lr_contribution")
    if name == "GaussianNB":
        return Embedder(lambda x: _nb_contributions(model, x), "cosine", "nb_loglik")
    raise TypeError(f"no embedding rule for {name}; pass hook=")


def _nb_contributions(model: object, x: NDArray[np.float64]) -> NDArray[np.float64]:
    """Per-feature log p(x_j | y=1) - log p(x_j | y=0) for a binary GaussianNB."""
    x = np.asarray(x, dtype=np.float64)
    mu, var = model.theta_, model.var_  # type: ignore[attr-defined]
    if mu.shape[0] != 2:
        raise ValueError("only binary GaussianNB is supported")
    loglik = -0.5 * (np.log(2 * np.pi * var[:, None, :]) + (x[None] - mu[:, None, :]) ** 2
                     / var[:, None, :])
    return loglik[1] - loglik[0]
