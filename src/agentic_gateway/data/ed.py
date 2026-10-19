"""Emergency department cohort from MIMIC-IV-ED, one row per stay.

Protocol (fixed here, reported in the paper's Methods):

* Outcome: ``disposition == "ADMITTED"``.
* Excluded, outcome not observable: transfer to another hospital, death in the department,
  disposition ``OTHER`` or missing. Patients who left before being seen, eloped or left
  against advice stay in as not admitted, because the model runs at triage, before anyone
  knows who will leave.
* Excluded: age under 18, or no ``patients`` row (age and period unknown).
* Predictors: what is recorded at triage and arrival only (``triage`` and ``edstays``). Repeat
  vitals from ``vitalsign`` are not used: they have timestamps after triage. The chief
  complaint free text is not used in this paper.
* Implausible vital signs are set to missing, with the count recorded.
* Period: ``anchor_year_group``. MIMIC shifts each patient's dates by a different offset, so
  ``intime`` cannot order patients in calendar time; the anchor year group can.
"""

from __future__ import annotations

import re

import numpy as np
import pandas as pd

from ..gateway.subgroups import age_band
from .access import Source

UNOBSERVABLE = {"TRANSFER", "EXPIRED", "OTHER"}

PLAUSIBLE = {
    "temperature": (90.0, 110.0),  # Fahrenheit
    "heartrate": (20.0, 250.0),
    "resprate": (4.0, 70.0),
    "o2sat": (50.0, 100.0),
    "sbp": (40.0, 300.0),
    "dbp": (20.0, 200.0),
    "pain": (0.0, 10.0),
    "acuity": (1.0, 5.0),
}


def race_group(value: object) -> object:
    """Collapse MIMIC's combined race field. Declined or unknown becomes missing."""
    if not isinstance(value, str):
        return np.nan
    v = value.upper()
    if v.startswith("WHITE") or v == "PORTUGUESE":
        return "White"
    if v.startswith("BLACK"):
        return "Black"
    if v.startswith("HISPANIC") or v.startswith("SOUTH AMERICAN"):
        return "Hispanic"
    if v.startswith("ASIAN"):
        return "Asian"
    if v in {"UNKNOWN", "UNABLE TO OBTAIN", "PATIENT DECLINED TO ANSWER"}:
        return np.nan
    return "Other"


def _first_number(value: object) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        match = re.search(r"\d+(\.\d+)?", value)
        if match:
            return float(match.group())
    return np.nan


def build(source: Source) -> tuple[pd.DataFrame, dict]:
    stays = pd.read_csv(source.path("ed", "edstays"), parse_dates=["intime"])
    triage = pd.read_csv(source.path("ed", "triage"))
    patients = pd.read_csv(
        source.path("hosp", "patients"),
        usecols=["subject_id", "anchor_age", "anchor_year", "anchor_year_group"],
    )
    flow: dict[str, int] = {"ed_stays": len(stays)}

    df = stays.merge(triage.drop(columns=["subject_id"]), on="stay_id", how="left")
    df = df[~df["disposition"].isin(UNOBSERVABLE) & df["disposition"].notna()]
    flow["after_unobservable_outcome"] = len(df)

    df = df.merge(patients, on="subject_id", how="inner")
    flow["after_patients_link"] = len(df)
    df["age"] = df["anchor_age"] + (df["intime"].dt.year - df["anchor_year"])
    df = df[df["age"] >= 18]
    flow["after_adults_only"] = len(df)

    df["pain"] = df["pain"].map(_first_number)
    implausible: dict[str, int] = {}
    for col, (lo, hi) in PLAUSIBLE.items():
        values = pd.to_numeric(df[col], errors="coerce")
        bad = values.notna() & ((values < lo) | (values > hi))
        implausible[col] = int(bad.sum())
        df[col] = values.mask(bad)

    out = pd.DataFrame(
        {
            "case_id": df["stay_id"].astype(str),
            "patient_id": df["subject_id"].astype(str),
            "period": df["anchor_year_group"].astype(str),
            "site": "mimic",
            "y": (df["disposition"] == "ADMITTED").astype(int),
            "age": df["age"].astype(float),
            "temperature": df["temperature"],
            "heartrate": df["heartrate"],
            "resprate": df["resprate"],
            "o2sat": df["o2sat"],
            "sbp": df["sbp"],
            "dbp": df["dbp"],
            "pain": df["pain"],
            "acuity": df["acuity"],
            "arrival_transport": df["arrival_transport"].fillna("UNKNOWN"),
            "race_group": df["race"].map(race_group),
            "gender": df["gender"],
            "age_band": age_band(df["age"].to_numpy(), cuts=(45.0, 65.0)).to_numpy(),
        }
    ).reset_index(drop=True)
    flow["final"] = len(out)
    flow["admitted"] = int(out["y"].sum())
    return out, {"flow": flow, "implausible_set_missing": implausible}
