"""StepGate: the check applied to every action an agent proposes.

Per tool:

* every tool: structural check (known tool, required arguments present) -> BLOCK on failure;
* ``risk_score``: the prediction check (the five-signal gateway with timing excluded, or a
  baseline) -> its decision. The decision is remembered as the risk's reliability tag;
* ``draft_alert``:
    - argument check: quoted fields must equal the record, and the risk must equal the last
      risk returned -> BLOCK on mismatch. Outside the five patented signals; ablated alone;
    - tag check: an alert built on a risk that was deferred or blocked -> DEFER;
    - output-only mode: the prediction check runs here instead of at ``risk_score``;
    - M5 timing: cooldown without escalation -> BLOCK. An allowed alert starts a cooldown.

The most severe outcome wins (BLOCK > DEFER > ALLOW).
"""

from __future__ import annotations

import math
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Protocol

import numpy as np

from ..gateway.pipeline import ReliabilityGateway
from ..gateway.timing import AlertHistory, TimingRule
from ..gateway.types import Decision, PredictionRequest
from .tools import REQUIRED_ARGS
from .types import Step

SEVERITY = {Decision.ALLOW: 0, Decision.DEFER: 1, Decision.BLOCK: 2}


@dataclass(frozen=True)
class CheckResult:
    decision: Decision
    reasons: tuple[str, ...] = ()
    record: dict[str, Any] = field(default_factory=dict)
    caveat: bool = False


class PredictionCheck(Protocol):
    name: str

    def __call__(self, prob: float, embedding: np.ndarray, group: str, patient_id: str,
                 clock: float) -> CheckResult: ...


@dataclass
class GatewayCheck:
    gateway: ReliabilityGateway  # its config must have "timing" disabled
    name: str = "gateway"

    def __post_init__(self) -> None:
        if "timing" not in self.gateway.config.disabled:
            raise ValueError("the prediction check runs M1-M4; timing belongs to draft_alert")

    def __call__(self, prob, embedding, group, patient_id, clock) -> CheckResult:
        out = self.gateway.evaluate(
            PredictionRequest(patient_id, clock, prob, embedding, group), commit=False)
        return CheckResult(out.decision, out.reasons, out.to_record(), out.caveat)


@dataclass
class ConfidenceCheck:
    """Single confidence threshold: defer when min(p, 1 - p) exceeds ``cut``."""

    cut: float
    name: str = "confidence"

    def __call__(self, prob, embedding, group, patient_id, clock) -> CheckResult:
        if min(prob, 1.0 - prob) > self.cut:
            return CheckResult(Decision.DEFER, ("confidence:breach",))
        return CheckResult(Decision.ALLOW)


@dataclass
class NoCheck:
    name: str = "none"

    def __call__(self, prob, embedding, group, patient_id, clock) -> CheckResult:
        return CheckResult(Decision.ALLOW)


@dataclass(frozen=True)
class StepVerdict:
    decision: Decision
    reasons: tuple[str, ...]
    latency_ns: int
    record: dict[str, Any]


def _same(a: Any, b: Any) -> bool:
    def missing(v: Any) -> bool:
        return v is None or (isinstance(v, float) and math.isnan(v))

    if missing(a) or missing(b):
        return missing(a) and missing(b)
    try:
        return abs(float(a) - float(b)) <= 1e-6 * max(1.0, abs(float(b)))
    except (TypeError, ValueError):
        return str(a) == str(b)


class StepGate:
    def __init__(self, prediction: PredictionCheck, *, mode: str = "step",
                 timing: TimingRule | None = None, argcheck: bool = True,
                 judge: Callable[[Step, list[Step]], bool] | None = None) -> None:
        if mode not in ("step", "output_only", "none"):
            raise ValueError(f"unknown mode {mode!r}")
        self.prediction = prediction
        self.mode = mode
        self.timing = timing
        self.argcheck = argcheck
        self.judge = judge
        self.reset()

    def reset(self) -> None:
        self.record: dict[str, Any] | None = None
        self.risk: dict[str, Any] | None = None  # hidden data of the last risk_score
        self.risk_tag: Decision = Decision.ALLOW
        self.history: list[Step] = []
        if self.timing is not None:
            self.timing.history.clear()

    def check(self, step: Step) -> StepVerdict:
        t0 = time.perf_counter_ns()
        decision, reasons, record = self._check(step)
        verdict = StepVerdict(decision, tuple(reasons), time.perf_counter_ns() - t0, record)
        # Remember what the agent saw, whatever the decision, for later argument checks.
        if step.tool == "fetch_record" and isinstance(step.output, dict):
            self.record = step.output
        if step.tool == "risk_score":
            self.risk, self.risk_tag = step.hidden, decision
        self.history.append(step)
        return verdict

    def _check(self, step: Step) -> tuple[Decision, list[str], dict[str, Any]]:
        if self.mode == "none":
            return Decision.ALLOW, [], {}
        required = REQUIRED_ARGS.get(step.tool)
        if required is None or any(k not in step.args for k in required):
            return Decision.BLOCK, ["structural:invalid_call"], {}

        outcome, reasons, record = Decision.ALLOW, [], {}

        def worse(d: Decision, why: list[str] | tuple[str, ...]) -> None:
            nonlocal outcome
            if SEVERITY[d] > SEVERITY[outcome]:
                outcome = d
            if d is not Decision.ALLOW:
                reasons.extend(why)

        if step.tool == "risk_score" and self.mode == "step" and step.hidden:
            res = self._predict(step.hidden, step.clock)
            record = res.record
            worse(res.decision, res.reasons)

        if step.tool == "draft_alert":
            if self.argcheck:
                worse(*self._arguments(step))
            if self.mode == "step" and self.risk_tag is not Decision.ALLOW:
                worse(Decision.DEFER, ["tag:risk_withheld"])
            if self.mode == "output_only" and self.risk:
                res = self._predict(self.risk, step.clock)
                record = res.record
                worse(res.decision, res.reasons)
            if self.timing is not None and self.risk:
                t = self.timing.evaluate(str(step.args["patient_id"]), step.clock,
                                         float(self.risk["probability"]))
                record = {**record, "timing.tier": t.tier, "timing.suppress": t.suppress}
                if t.suppress:
                    worse(Decision.BLOCK, ["timing:breach"])
                elif outcome is Decision.ALLOW:
                    self.timing.history.record(str(step.args["patient_id"]), step.clock, t.tier)

        if self.judge is not None and not self.judge(step, self.history):
            worse(Decision.DEFER, ["judge:unsafe"])
        return outcome, reasons, record

    def _predict(self, hidden: dict[str, Any], clock: float) -> CheckResult:
        return self.prediction(float(hidden["probability"]), hidden["embedding"],
                               str(hidden["group"]), str(hidden.get("patient_id", "")), clock)

    def _arguments(self, step: Step) -> tuple[Decision, list[str]]:
        if self.record is None or self.risk is None:
            return Decision.BLOCK, ["argument:no_source"]
        cited = step.args.get("cited") or {}
        if not isinstance(cited, dict):
            return Decision.BLOCK, ["argument:malformed"]
        bad = [k for k, v in cited.items() if k not in self.record or not _same(v, self.record[k])]
        risk_ok = _same(round(float(step.args["risk"]), 4), round(self.risk["probability"], 4))
        if bad or not risk_ok:
            return Decision.BLOCK, [f"argument:mismatch({','.join(bad) or 'risk'})"]
        return Decision.ALLOW, []


def new_timing(cooldown_s: float, cuts: tuple[float, ...]) -> TimingRule:
    return TimingRule(cooldown_s, cuts, AlertHistory())
