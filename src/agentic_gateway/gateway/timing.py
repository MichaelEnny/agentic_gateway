"""M5: cooldown and risk-tier escalation rule (spec para. [0029]).

    if time_since_last_alert(patient) < cooldown and current_tier <= last_shown_tier:
        suppress
    else:
        continue

The history records only predictions that were actually shown (allowed). A deferred or blocked
prediction never reached the clinician, so it must not start a cooldown.
"""

from __future__ import annotations

import bisect
from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class TimingResult:
    suppress: bool
    tier: int
    last_tier: int | None
    seconds_since_last: float | None


def risk_tier(probability: float, cuts: Sequence[float]) -> int:
    """0 for the lowest tier; a probability equal to a cut belongs to the higher tier."""
    return bisect.bisect_right(list(cuts), probability)


class AlertHistory:
    """In-memory store of the last shown alert per patient."""

    def __init__(self) -> None:
        self._last: dict[str, tuple[float, int]] = {}

    def last(self, patient_id: str) -> tuple[float, int] | None:
        return self._last.get(patient_id)

    def record(self, patient_id: str, timestamp: float, tier: int) -> None:
        self._last[patient_id] = (timestamp, tier)

    def clear(self) -> None:
        self._last.clear()


class TimingRule:
    def __init__(self, cooldown_s: float, cuts: Sequence[float], history: AlertHistory) -> None:
        self.cooldown_s = cooldown_s
        self.cuts = tuple(cuts)
        self.history = history

    def evaluate(self, patient_id: str, timestamp: float, probability: float) -> TimingResult:
        tier = risk_tier(probability, self.cuts)
        last = self.history.last(patient_id)
        if last is None:
            return TimingResult(False, tier, None, None)
        last_time, last_tier = last
        since = timestamp - last_time
        suppress = 0.0 <= since < self.cooldown_s and tier <= last_tier
        return TimingResult(suppress, tier, last_tier, since)
