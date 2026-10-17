"""Gateway thresholds and fusion policy.

Defaults marked PATENT come from the filed specification. Defaults marked PLACEHOLDER are
starting values only; the paper plan requires choosing them on the tuning split and freezing
them before the test split is touched.
"""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import Any

from .types import SIGNALS, Decision


@dataclass(frozen=True)
class GatewayConfig:
    # M1, local calibration
    local_threshold: float = 0.10  # PLACEHOLDER
    local_min_neighbors: int = 30  # PATENT: minimum sample size 30-50
    local_metric: str = "cosine"  # PATENT: cosine similarity (dependent claim 3)
    local_growth: float = 1.5  # radius multiplier per expansion step
    local_max_steps: int = 20
    local_sparse_quantile: float = 0.95  # sparse if the k-th neighbour is beyond this quantile
    local_sparse_is_breach: bool = False  # report sparsity; breach on it only if asked

    # M2, SCDI lookup
    scdi_threshold: float = 0.15  # PATENT, spec para. [0021]
    # A subgroup left out of the SCDI table only because it is below the minimum size cannot
    # be assessed. True: caveat ("not_assessable") instead of the fail-closed stop. Unknown
    # subgroups and every other unavailable signal still stop the action.
    scdi_small_group_caveat: bool = False

    # M3, Mondrian conformal
    conformal_coverage: float = 0.90  # PLACEHOLDER
    conformal_max_set_size: int = 1  # binary task: a set of both labels is too uncertain
    conformal_empty_is_breach: bool = True  # an empty set means no label is plausible

    # M4, cached drift state
    drift_max_age_s: float = 2 * 3600.0  # spec runs the job hourly; allow one missed run

    # M5, timing
    cooldown_s: float = 4 * 3600.0  # PLACEHOLDER
    risk_tier_cuts: tuple[float, ...] = (0.10, 0.30, 0.60)  # PLACEHOLDER, tiers 0..3

    # Fusion
    caveat_margin: float = 0.20  # PRD open question 1: "near" = within 20% of the threshold
    fail_closed: bool = True  # an UNAVAILABLE signal counts as a breach
    # Breach of these signals blocks the action; breach of any other signal defers it.
    # A duplicate alert is dropped; an unreliable prediction goes to a clinician instead.
    # Add "drift_critical" to drop actions while the model is in critical drift.
    block_on: frozenset[str] = frozenset({"timing"})
    disabled: frozenset[str] = field(default_factory=frozenset)  # for leave-one-out ablation

    def __post_init__(self) -> None:
        unknown = set(self.disabled) - set(SIGNALS)
        if unknown:
            raise ValueError(f"unknown signals in disabled: {sorted(unknown)}")
        if self.local_min_neighbors < 1:
            raise ValueError("local_min_neighbors must be at least 1")
        if not 0.0 < self.conformal_coverage < 1.0:
            raise ValueError("conformal_coverage must lie in (0, 1)")
        if list(self.risk_tier_cuts) != sorted(self.risk_tier_cuts):
            raise ValueError("risk_tier_cuts must be increasing")

    @classmethod
    def from_dict(cls, values: dict[str, Any]) -> GatewayConfig:
        known = {f.name for f in fields(cls)}
        unknown = set(values) - known
        if unknown:
            raise ValueError(f"unknown config keys: {sorted(unknown)}")
        coerced = dict(values)
        for key in ("block_on", "disabled"):
            if key in coerced:
                coerced[key] = frozenset(coerced[key])
        if "risk_tier_cuts" in coerced:
            coerced["risk_tier_cuts"] = tuple(coerced["risk_tier_cuts"])
        return cls(**coerced)

    def without(self, signal: str) -> GatewayConfig:
        """Copy with one more signal disabled, for leave-one-out runs."""
        values = {f.name: getattr(self, f.name) for f in fields(self)}
        values["disabled"] = frozenset(self.disabled | {signal})
        return GatewayConfig(**values)

    def breach_decision(self, signal: str) -> Decision:
        return Decision.BLOCK if signal in self.block_on else Decision.DEFER
