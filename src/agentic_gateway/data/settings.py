"""The two clinical settings: which columns are what.

Every cohort table has the same identity columns, so the rest of the pipeline is
setting-agnostic: ``case_id``, ``patient_id``, ``period``, ``site``, ``y`` plus the model
features and the audit attributes. Audit attributes describe who is scored and define the
subgroups; they are never model inputs (age is the one deliberate exception, used as both).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Setting:
    name: str
    question: str
    numeric: tuple[str, ...]
    categorical: tuple[str, ...]
    audit: tuple[str, ...]
    default_groups: tuple[str, ...]  # subgroup columns for M2 and M3
    cited: tuple[str, ...]  # record fields the agent quotes in an alert
    uncertainty_blank: tuple[str, ...]  # fields blanked by the high-uncertainty fault
    unit_shift: tuple[str, float, float]  # (field, multiplier, offset) for the drift fault

    @property
    def features(self) -> tuple[str, ...]:
        return (*self.numeric, *self.categorical)


ED = Setting(
    name="ed",
    question="At the end of triage, will this emergency department patient be admitted?",
    numeric=("age", "temperature", "heartrate", "resprate", "o2sat", "sbp", "dbp", "pain",
             "acuity"),
    categorical=("arrival_transport",),
    audit=("race_group", "gender", "age_band"),
    default_groups=("race_group", "gender"),
    cited=("sbp", "heartrate", "o2sat"),
    uncertainty_blank=("acuity", "o2sat", "sbp"),
    unit_shift=("temperature", 5.0 / 9.0, -32.0 * 5.0 / 9.0),  # recorded in Celsius, not F
)

ICU = Setting(
    name="icu",
    question="At 24 hours after ICU admission, will this patient die before hospital discharge?",
    numeric=("age", "admissionweight", "verbal", "motor", "eyes", "ventday1", "readmit",
             "hr_mean", "hr_max", "rr_mean", "rr_max", "sao2_min", "map_min", "map_mean"),
    categorical=("unittype", "unitadmitsource"),
    audit=("ethnicity_group", "gender", "age_band"),
    default_groups=("ethnicity_group", "gender"),
    cited=("hr_mean", "sao2_min", "map_min"),
    uncertainty_blank=("motor", "verbal", "eyes"),
    unit_shift=("admissionweight", 2.20462, 0.0),  # recorded in pounds, not kg
)

SETTINGS = {"ed": ED, "icu": ICU}
