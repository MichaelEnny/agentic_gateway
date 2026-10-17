"""Step 6 counts stopping signals apart from caveat-only ones."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))
reason_counts = importlib.import_module("06_e1_static").reason_counts


def test_caveat_reasons_are_not_counted_as_stops():
    decisions = ["defer", "defer", "allow", "allow", "block"]
    reasons = ["subgroup_gap:near; drift:breach",
               "subgroup_gap:not_assessable; conformal:breach; drift:breach",
               "subgroup_gap:near",
               "",
               "argument:mismatch(hr_mean)"]
    stops, caveats = reason_counts(decisions, reasons)
    assert stops == {"drift": 2, "conformal": 1, "argument": 1}
    assert caveats == {"subgroup_gap": 3}


def test_unavailable_stops_only_when_the_prediction_was_stopped():
    stops, caveats = reason_counts(["defer", "allow"],
                                   ["subgroup_gap:unavailable", "drift:unavailable"])
    assert stops == {"subgroup_gap": 1} and caveats == {"drift": 1}
