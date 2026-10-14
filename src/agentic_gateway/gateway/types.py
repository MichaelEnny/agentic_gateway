"""Data types shared by the five signal modules, the fusion rule and the pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

import numpy as np
from numpy.typing import NDArray


class Status(str, Enum):
    """Outcome of one signal for one request."""

    OK = "ok"
    NEAR = "near"  # within the caveat margin of the threshold, not past it
    BREACH = "breach"
    UNAVAILABLE = "unavailable"  # could not be computed (unknown subgroup, stale cache, ...)
    DISABLED = "disabled"  # switched off for an ablation run


class Decision(str, Enum):
    """What the gateway does with the proposed action.

    Mapping to the patent's display-control outputs (spec para. [0032]):
    ALLOW without caveat = display; ALLOW with caveat = display with caveat;
    DEFER and BLOCK are both forms of suppression. DEFER routes the action to a clinician,
    BLOCK drops it.
    """

    ALLOW = "allow"
    DEFER = "defer"
    BLOCK = "block"


SIGNALS: tuple[str, ...] = (
    "local_calibration",  # M1
    "subgroup_gap",  # M2, SCDI lookup
    "conformal",  # M3, Mondrian set size
    "drift",  # M4, cached state
    "timing",  # M5, cooldown / escalation
)


@dataclass(frozen=True)
class PredictionRequest:
    """One risk prediction that an agent action produces or consumes.

    ``timestamp`` is in seconds on any monotone clock the caller chooses (trajectory time in
    the benchmark, epoch seconds in a live run). ``group`` is the subgroup label used by both
    M2 and M3, built with :func:`agentic_gateway.gateway.subgroups.group_labels`.
    """

    patient_id: str
    timestamp: float
    probability: float
    embedding: NDArray[np.float64]
    group: str

    def __post_init__(self) -> None:
        if not 0.0 <= self.probability <= 1.0 or not np.isfinite(self.probability):
            raise ValueError(f"probability must lie in [0, 1], got {self.probability}")


@dataclass(frozen=True)
class SignalResult:
    name: str
    status: Status
    value: float | None = None
    threshold: float | None = None
    latency_ns: int = 0
    detail: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class GatingDecision:
    decision: Decision
    caveat: bool
    reasons: tuple[str, ...]
    signals: dict[str, SignalResult]
    latency_ns: int

    def to_record(self) -> dict[str, Any]:
        """Flat dict for the trace log."""
        record: dict[str, Any] = {
            "decision": self.decision.value,
            "caveat": self.caveat,
            "reasons": "; ".join(self.reasons),
            "latency_ns": self.latency_ns,
        }
        for name, result in self.signals.items():
            record[f"{name}.status"] = result.status.value
            record[f"{name}.value"] = result.value
            record[f"{name}.latency_ns"] = result.latency_ns
        return record
