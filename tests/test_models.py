"""Saved models predict on one thread (see agentic_gateway.models.for_prediction)."""

from __future__ import annotations

import warnings

import joblib
import numpy as np

from agentic_gateway.data.settings import ED
from agentic_gateway.models import load_model, make_model


def test_load_model_predicts_single_threaded_with_identical_results(clinical, tmp_path):
    _, cohort, model, _ = clinical
    x = cohort[list(ED.features)]
    assert model[-1].n_jobs == -1  # fitting stays parallel
    before = model.predict_proba(x)
    joblib.dump(model, tmp_path / "rf.joblib")
    loaded = load_model(tmp_path / "rf.joblib")
    assert loaded[-1].n_jobs == 1
    with warnings.catch_warnings():
        warnings.simplefilter("error")  # no parallel/delayed warning on predict
        after = loaded.predict_proba(x)
    # summation order across trees differs between threads: equal to rounding
    np.testing.assert_allclose(before, after, rtol=0, atol=1e-12)


def test_load_model_leaves_models_without_n_jobs_alone(tmp_path):
    lr = make_model("logistic_regression", ED)
    joblib.dump(lr, tmp_path / "lr.joblib")
    assert load_model(tmp_path / "lr.joblib")[-1].get_params()["max_iter"] == 5000
