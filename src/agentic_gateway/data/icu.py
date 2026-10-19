"""ICU cohort from eICU-CRD, one row per patient.

Protocol (fixed here, reported in the paper's Methods):

* Unit: the first ICU stay of each patient's first hospital stay (``uniquepid``). Later stays
  are conditioned on surviving earlier ones.
* Prediction time: 24 hours after ICU admission. Excluded: stays shorter than 24 hours
  (death or discharge before the prediction is made), age under 18, missing discharge status.
* Outcome: ``hospitaldischargestatus == "Expired"``.
* Predictors: demographics and admission fields from ``patient``; non-laboratory APACHE
  variables from ``apachePredVar`` (Glasgow coma scale components, ventilation on day 1,
  readmission); vital signs from ``vitalPeriodic`` summarised over the first 24 hours.
  Laboratory values are not used. ``diedinhospital`` in ``apachePredVar`` is the outcome
  and is never read.
* eICU codes a missing GCS component as -1; set to missing.
* Site: ``hospitalid``. Period: ``hospitaldischargeyear``.
"""

from __future__ import annotations

import pandas as pd

from ..gateway.subgroups import age_band
from .access import Source

FIRST_DAY_MIN = 24 * 60
VITALS = {"heartrate": "hr", "respiration": "rr", "sao2": "sao2", "systemicmean": "map"}
APACHE = ("verbal", "motor", "eyes", "ventday1", "readmit")
ETHNICITY = {
    "Caucasian": "White",
    "African American": "Black",
    "Hispanic": "Hispanic",
    "Asian": "Asian",
    "Native American": "Other",
}


def _first_day_vitals(path, stays: set[int], chunksize: int = 2_000_000) -> pd.DataFrame:
    """Mean, min and max over the first 24 h; read in chunks (the full file is ~1.8 GB)."""
    cols = ["patientunitstayid", "observationoffset", *VITALS]
    parts = []
    for chunk in pd.read_csv(path, usecols=cols, chunksize=chunksize):
        chunk = chunk[chunk["patientunitstayid"].isin(stays)]
        chunk = chunk[(chunk["observationoffset"] >= 0)
                      & (chunk["observationoffset"] < FIRST_DAY_MIN)]
        if not chunk.empty:
            parts.append(chunk.drop(columns="observationoffset"))
    if not parts:
        return pd.DataFrame(columns=["patientunitstayid"])
    v = pd.concat(parts).groupby("patientunitstayid").agg(["mean", "min", "max"])
    v.columns = [f"{VITALS[name]}_{stat}" for name, stat in v.columns]
    return v.reset_index()


def build(source: Source) -> tuple[pd.DataFrame, dict]:
    p = pd.read_csv(source.path("eicu", "patient"))
    flow: dict[str, int] = {"unit_stays": len(p), "patients": int(p["uniquepid"].nunique())}

    p = p.sort_values(["uniquepid", "hospitaldischargeyear", "patienthealthsystemstayid",
                       "unitvisitnumber"])
    p = p.drop_duplicates("uniquepid", keep="first")
    flow["first_stay_per_patient"] = len(p)

    p["age_num"] = pd.to_numeric(p["age"].replace({"> 89": "90"}), errors="coerce")
    p = p[p["hospitaldischargestatus"].isin(["Alive", "Expired"])]
    flow["after_known_outcome"] = len(p)
    p = p[p["age_num"] >= 18]
    flow["after_adults_only"] = len(p)
    p = p[p["unitdischargeoffset"] >= FIRST_DAY_MIN]
    flow["after_24h_in_unit"] = len(p)

    apache = pd.read_csv(source.path("eicu", "apachePredVar"),
                         usecols=["patientunitstayid", *APACHE])
    for col in ("verbal", "motor", "eyes"):
        apache[col] = apache[col].where(apache[col] >= 0)
    vitals = _first_day_vitals(source.path("eicu", "vitalPeriodic"),
                               set(p["patientunitstayid"]))
    df = p.merge(apache, on="patientunitstayid", how="left").merge(
        vitals, on="patientunitstayid", how="left")

    out = pd.DataFrame(
        {
            "case_id": df["patientunitstayid"].astype(str),
            "patient_id": df["uniquepid"].astype(str),
            "period": df["hospitaldischargeyear"].astype(str),
            "site": df["hospitalid"].astype(str),
            "y": (df["hospitaldischargestatus"] == "Expired").astype(int),
            "age": df["age_num"].astype(float),
            "admissionweight": df["admissionweight"].where(df["admissionweight"].between(25, 350)),
            **{c: df[c] for c in APACHE},
            "hr_mean": df.get("hr_mean"), "hr_max": df.get("hr_max"),
            "rr_mean": df.get("rr_mean"), "rr_max": df.get("rr_max"),
            "sao2_min": df.get("sao2_min"),
            "map_min": df.get("map_min"), "map_mean": df.get("map_mean"),
            "unittype": df["unittype"].fillna("UNKNOWN"),
            "unitadmitsource": df["unitadmitsource"].fillna("UNKNOWN"),
            "ethnicity_group": df["ethnicity"].map(ETHNICITY),
            "gender": df["gender"].where(df["gender"].isin(["Male", "Female"])),
            "age_band": age_band(df["age_num"].to_numpy(), cuts=(45.0, 65.0)).to_numpy(),
        }
    ).reset_index(drop=True)
    for col in ("hr_mean", "hr_max", "rr_mean", "rr_max", "sao2_min", "map_min", "map_mean"):
        out[col] = pd.to_numeric(out[col], errors="coerce").astype(float)
    flow["final"] = len(out)
    flow["died"] = int(out["y"].sum())
    flow["hospitals"] = int(out["site"].nunique())
    flow["missing_apache"] = int(out["motor"].isna().sum())
    flow["missing_vitals"] = int(out["hr_mean"].isna().sum())
    return out, {"flow": flow, "note": "laboratory values not used"}
