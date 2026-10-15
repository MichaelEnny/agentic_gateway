"""Risk models. Baselines on purpose: the paper studies the gate, not the model.

Both models are sklearn Pipelines so that :func:`agentic_gateway.gateway.embedder_for` can run
the fitted preprocessing before taking the embedding. Gradient boosting with
HistGradientBoosting is not used because it exposes no leaf indices for M1.
"""

from __future__ import annotations

from typing import Any

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .data.settings import Setting

MODELS = ("logistic_regression", "random_forest")


def preprocessor(setting: Setting, *, scale: bool) -> ColumnTransformer:
    numeric = [("impute", SimpleImputer(strategy="median", add_indicator=True))]
    if scale:
        numeric.append(("scale", StandardScaler()))
    categorical = [
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", min_frequency=5,
                                 sparse_output=False)),
    ]
    return ColumnTransformer(
        [("num", Pipeline(numeric), list(setting.numeric)),
         ("cat", Pipeline(categorical), list(setting.categorical))],
        verbose_feature_names_out=False,
    )


def make_model(name: str, setting: Setting, *, seed: int = 42, smoke: bool = False) -> Any:
    if name == "logistic_regression":
        return Pipeline([("features", preprocessor(setting, scale=True)),
                         ("model", LogisticRegression(max_iter=5000))])
    if name == "random_forest":
        return Pipeline([
            ("features", preprocessor(setting, scale=False)),
            ("model", RandomForestClassifier(
                n_estimators=100 if smoke else 300,
                min_samples_leaf=5 if smoke else 20,  # library default 1 overfits
                n_jobs=-1, random_state=seed)),
        ])
    raise ValueError(f"unknown model {name!r}")


def for_prediction(model: Any) -> Any:
    """Predict on one thread. Fitting stays parallel (``n_jobs=-1``), but scikit-learn's
    threaded predict calls ``warnings.resetwarnings()`` in each worker, and on Python 3.14
    without free threading the workers share one filter list: they race, the list can end
    up empty, and every later prediction then warns that ``delayed`` was used without
    ``Parallel``. Results agree to rounding (trees are summed in another order); a single
    row is also faster on one thread. Models saved before this change are fixed on load."""
    steps = model.steps if hasattr(model, "steps") else [(None, model)]
    for _, est in steps:
        if "n_jobs" in getattr(est, "get_params", dict)():
            est.set_params(n_jobs=1)
    return model


def load_model(path: Any) -> Any:
    import joblib

    return for_prediction(joblib.load(path))
