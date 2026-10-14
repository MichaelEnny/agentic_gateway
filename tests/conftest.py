"""Synthetic cohort with a planted miscalibrated region and a planted miscalibrated subgroup.

* Embeddings: 2-D points. Patients in the cluster around (5, 5) get probabilities 0.4 too high.
* Subgroup "B" gets probabilities 0.25 too high everywhere; subgroup "A" is calibrated.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest


def make_cohort(n: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    main = rng.normal(0.0, 1.0, size=(n, 2))
    n_cluster = n // 10
    main[:n_cluster] = rng.normal(5.0, 0.3, size=(n_cluster, 2))
    true_p = rng.uniform(0.05, 0.6, size=n)
    y = (rng.uniform(size=n) < true_p).astype(float)
    group = np.where(rng.uniform(size=n) < 0.5, "A", "B")
    prob = true_p.copy()
    prob[:n_cluster] += 0.4
    prob[group == "B"] += 0.25
    prob = np.clip(prob, 0.001, 0.999)
    # Cosine similarity ignores scale, so shift away from the origin before using it.
    emb = main + 10.0
    return pd.DataFrame(
        {"e0": emb[:, 0], "e1": emb[:, 1], "probability": prob, "label": y, "group": group,
         "in_cluster": np.arange(n) < n_cluster}
    )


@pytest.fixture(scope="session")
def reference() -> pd.DataFrame:
    return make_cohort(2000, seed=1)


@pytest.fixture(scope="session")
def calibration() -> pd.DataFrame:
    return make_cohort(2000, seed=2)


# -- agent, benchmark and edge tests ---------------------------------------------------------


def make_clinical_cohort(n: int, seed: int) -> pd.DataFrame:
    """Synthetic ED-layout cohort: one stay per patient, admission driven by acuity and SBP."""
    rng = np.random.default_rng(seed)
    acuity = rng.integers(1, 6, n).astype(float)
    sbp = rng.normal(130.0, 20.0, n)
    frame = pd.DataFrame({
        "case_id": [f"c{i}" for i in range(n)],
        "patient_id": [f"p{i}" for i in range(n)],
        "period": "2011 - 2013",
        "site": "s0",
        "age": rng.integers(18, 90, n).astype(float),
        "temperature": rng.normal(98.4, 0.8, n),
        "heartrate": rng.normal(85.0, 15.0, n),
        "resprate": rng.normal(17.0, 2.0, n),
        "o2sat": np.clip(rng.normal(97.0, 2.0, n), 80.0, 100.0),
        "sbp": sbp,
        "dbp": rng.normal(80.0, 10.0, n),
        "pain": rng.integers(0, 11, n).astype(float),
        "acuity": acuity,
        "arrival_transport": rng.choice(["WALK IN", "AMBULANCE"], n),
        "group": rng.choice(["A", "B", "C"], n, p=[0.6, 0.3, 0.1]),
    })
    logit = 2.0 - 1.2 * acuity + 0.02 * (sbp - 130.0)
    frame["y"] = (rng.uniform(size=n) < 1 / (1 + np.exp(-logit))).astype(int)
    frame.loc[0, "o2sat"] = np.nan  # one missing value, to check NaN -> None in records
    return frame


@pytest.fixture(scope="session")
def clinical():
    """(setting, cohort, fitted RF pipeline, embedder) on the ED column layout."""
    from agentic_gateway.data.settings import ED
    from agentic_gateway.gateway import embedder_for
    from agentic_gateway.models import make_model

    cohort = make_clinical_cohort(300, seed=3)
    model = make_model("random_forest", ED, seed=0, smoke=True)
    model.fit(cohort[list(ED.features)], cohort["y"])
    return ED, cohort, model, embedder_for(model)


@pytest.fixture
def make_tools(clinical):
    """Fresh ClinicalTools. Tier cuts: ``always_alert`` puts every risk in tier 3,
    ``never_alert`` in tier 0, ``normal`` uses the ED starting cuts."""
    from agentic_gateway.agent import ClinicalTools

    setting, cohort, model, emb = clinical

    def make(tiers: str = "always_alert"):
        cuts = {"always_alert": (0.0, 0.0, 0.0), "never_alert": (2.0, 2.0, 2.0),
                "normal": (0.1, 0.3, 0.6)}[tiers]
        return ClinicalTools(setting, cohort, model, emb, tier_cuts=cuts)

    return make
