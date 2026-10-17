"""Grading of individual signals and the rule that fuses them into one decision.

The rule is a conjunction (spec para. [0031], rule-based embodiment):

* any breach, or any unavailable signal when fail-closed, stops the action. It is BLOCKED if the
  signal is listed in ``config.block_on`` and DEFERRED to a clinician otherwise. BLOCK wins over
  DEFER when both apply;
* an unavailable signal marked ``not_assessable`` (a subgroup too small for the SCDI table,
  with ``scdi_small_group_caveat`` on) gives a caveat instead of stopping;
* otherwise any signal within the caveat margin allows the action with a caveat;
* otherwise the action is allowed.

A score never overrides a failed gate, which is why the baseline with a weighted score lives in
the experiments, not here.
"""

from __future__ import annotations

from collections.abc import Mapping

from .config import GatewayConfig
from .types import Decision, SignalResult, Status


def grade(value: float, threshold: float, margin: float) -> Status:
    """Higher is worse. NEAR means within ``margin`` (a fraction) below the threshold."""
    if value > threshold:
        return Status.BREACH
    if value > threshold * (1.0 - margin):
        return Status.NEAR
    return Status.OK


def fuse(
    signals: Mapping[str, SignalResult], config: GatewayConfig
) -> tuple[Decision, bool, tuple[str, ...]]:
    decision = Decision.ALLOW
    reasons: list[str] = []
    caveat = False

    for name, result in signals.items():
        if result.status is Status.DISABLED:
            continue
        if result.detail.get("not_assessable"):
            caveat = True
            reasons.append(f"{name}:not_assessable")
            continue
        stops = result.status is Status.BREACH or (
            result.status is Status.UNAVAILABLE and config.fail_closed
        )
        if stops:
            key = name
            if name == "drift" and result.detail.get("state") == "critical":
                key = "drift_critical"
            if config.breach_decision(key) is Decision.BLOCK:
                decision = Decision.BLOCK
            elif decision is Decision.ALLOW:
                decision = Decision.DEFER
            reasons.append(f"{name}:{result.status.value}")
        elif result.status in (Status.NEAR, Status.UNAVAILABLE):
            caveat = True
            reasons.append(f"{name}:{result.status.value}")

    if decision is not Decision.ALLOW:
        caveat = False
    return decision, caveat, tuple(reasons)
