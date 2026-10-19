"""Patient-disjoint split into five parts.

| part      | used for                                                              |
|-----------|-----------------------------------------------------------------------|
| fit       | training the risk models, nothing else                                |
| reference | M1 neighbour index, M2 SCDI table, drift reference window             |
| conformal | M3 per-subgroup quantiles                                             |
| tune      | choosing thresholds; the tuning benchmark                             |
| test      | opened once, after thresholds are frozen                              |

The test part is held out by time (ED: the latest ``period``) or by site (ICU: whole
hospitals), so it differs from the development parts the way a deployment would. The other
four are drawn at random by patient from what is left.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

PARTS = ("fit", "reference", "conformal", "tune", "test")
DEFAULT_SHARES = {"fit": 0.60, "reference": 0.15, "conformal": 0.10, "tune": 0.15}


def _period_start(label: str) -> int:
    return int(str(label).split("-")[0].strip())


def holdout_by_period(cohort: pd.DataFrame) -> pd.Series:
    periods = sorted(cohort["period"].dropna().unique(), key=_period_start)
    if len(periods) < 2:
        raise ValueError(f"a temporal split needs two periods, found {periods}")
    return cohort["period"] == periods[-1]


def holdout_by_site(cohort: pd.DataFrame, *, share: float, min_events: int,
                 seed: int) -> pd.Series:
    by_site = cohort.groupby("site")["y"].agg(["sum", "count"])
    eligible = by_site[(by_site["sum"] >= min_events)
                       & (by_site["count"] - by_site["sum"] >= min_events)].index
    if len(eligible) == 0:
        raise ValueError(f"no site has {min_events} events and {min_events} non-events")
    rng = np.random.default_rng(seed)
    n = max(1, round(share * cohort["site"].nunique()))
    chosen = rng.choice(np.sort(eligible.to_numpy()), size=min(n, len(eligible)), replace=False)
    return cohort["site"].isin(chosen)


def assign_parts(cohort: pd.DataFrame, is_test: pd.Series, *, seed: int,
                 shares: dict[str, float] | None = None) -> pd.Series:
    shares = shares or DEFAULT_SHARES
    if abs(sum(shares.values()) - 1.0) > 1e-9:
        raise ValueError("shares must sum to 1")
    part = pd.Series("test", index=cohort.index, dtype=object)
    test_patients = set(cohort.loc[is_test, "patient_id"])
    dev = cohort.loc[~is_test & ~cohort["patient_id"].isin(test_patients)]
    patients = np.sort(dev["patient_id"].unique())
    rng = np.random.default_rng(seed)
    rng.shuffle(patients)
    bounds = np.cumsum([round(shares[k] * len(patients)) for k in DEFAULT_SHARES])
    bounds[-1] = len(patients)
    start = 0
    for name, stop in zip(DEFAULT_SHARES, bounds):
        chosen = set(patients[start:stop])
        part[dev.index[dev["patient_id"].isin(chosen)]] = name
        start = stop
    # a patient with stays in both test and development keeps only the test stays
    part[~is_test & cohort["patient_id"].isin(test_patients)] = "dropped"
    _assert_disjoint(cohort, part)
    return part


def _assert_disjoint(cohort: pd.DataFrame, part: pd.Series) -> None:
    owners = cohort.assign(part=part)[part != "dropped"].groupby("patient_id")["part"].nunique()
    shared = owners[owners > 1]
    if len(shared):
        raise AssertionError(f"{len(shared)} patients appear in more than one part")


def summarise(cohort: pd.DataFrame, part: pd.Series) -> dict[str, dict]:
    frame = cohort.assign(part=part)
    out = {}
    for name in (*PARTS, "dropped"):
        rows = frame[frame["part"] == name]
        if rows.empty:
            continue
        out[name] = {
            "cases": int(len(rows)),
            "patients": int(rows["patient_id"].nunique()),
            "events": int(rows["y"].sum()),
            "event_rate": round(float(rows["y"].mean()), 4),
            "periods": sorted(map(str, rows["period"].unique()))[:10],
            "sites": int(rows["site"].nunique()),
        }
    return out
