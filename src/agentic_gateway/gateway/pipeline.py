"""ReliabilityGateway: evaluates the five signals for one prediction and fuses them.

The order follows the claim: M1 to M4 assess reliability, M5 assesses timing, then fusion.
All five are always computed, even when an earlier one already stops the action, so every
trace row carries every signal; the leave-one-out ablation and the per-signal cost figures
need that. Short-circuiting is a deployment optimisation to measure separately.
"""

from __future__ import annotations

import time
from collections.abc import Callable

from .config import GatewayConfig
from .conformal import MondrianConformal
from .decision import fuse, grade
from .drift import DriftStateReader
from .local_calibration import LocalCalibration
from .scdi import SCDITable
from .timing import AlertHistory, TimingRule
from .types import SIGNALS, Decision, GatingDecision, PredictionRequest, SignalResult, Status


class ReliabilityGateway:
    def __init__(
        self,
        config: GatewayConfig,
        local: LocalCalibration,
        scdi: SCDITable,
        conformal: MondrianConformal,
        drift: DriftStateReader,
        history: AlertHistory | None = None,
    ) -> None:
        self.config = config
        self.local = local
        self.scdi = scdi
        self.conformal = conformal
        self.drift = drift
        self.history = history if history is not None else AlertHistory()
        self.timing = TimingRule(config.cooldown_s, config.risk_tier_cuts, self.history)
        self._checks: dict[str, Callable[[PredictionRequest], SignalResult]] = {
            "local_calibration": self._local,
            "subgroup_gap": self._subgroup_gap,
            "conformal": self._conformal,
            "drift": self._drift,
            "timing": self._timing,
        }

    def evaluate(self, request: PredictionRequest, commit: bool = True) -> GatingDecision:
        """Decide on one prediction. With ``commit``, an allowed prediction starts a cooldown."""
        start = time.perf_counter_ns()
        signals: dict[str, SignalResult] = {}
        for name in SIGNALS:
            if name in self.config.disabled:
                signals[name] = SignalResult(name, Status.DISABLED)
                continue
            t0 = time.perf_counter_ns()
            result = self._checks[name](request)
            signals[name] = SignalResult(
                result.name, result.status, result.value, result.threshold,
                time.perf_counter_ns() - t0, result.detail,
            )
        decision, caveat, reasons = fuse(signals, self.config)
        latency = time.perf_counter_ns() - start

        if commit and decision is Decision.ALLOW and "timing" not in self.config.disabled:
            tier = int(signals["timing"].value)  # type: ignore[arg-type]
            self.history.record(request.patient_id, request.timestamp, tier)
        return GatingDecision(decision, caveat, reasons, signals, latency)

    # -- M1 ------------------------------------------------------------------------------
    def _local(self, request: PredictionRequest) -> SignalResult:
        c = self.config
        r = self.local.evaluate(request.embedding)
        status = grade(r.value, c.local_threshold, c.caveat_margin)
        if r.sparse and c.local_sparse_is_breach:
            status = Status.BREACH
        return SignalResult(
            "local_calibration", status, r.value, c.local_threshold,
            detail={"n_neighbors": r.n_neighbors, "steps": r.steps, "sparse": r.sparse,
                    "kth_distance": r.kth_distance},
        )

    # -- M2 ------------------------------------------------------------------------------
    def _subgroup_gap(self, request: PredictionRequest) -> SignalResult:
        c = self.config
        value = self.scdi.lookup(request.group)
        if value is None:
            detail: dict = {"group": request.group}
            if c.scdi_small_group_caveat and request.group in self.scdi.excluded:
                detail.update(not_assessable=True, n=self.scdi.excluded[request.group])
            return SignalResult("subgroup_gap", Status.UNAVAILABLE, None, c.scdi_threshold,
                                detail=detail)
        return SignalResult(
            "subgroup_gap", grade(value, c.scdi_threshold, c.caveat_margin), value,
            c.scdi_threshold, detail={"group": request.group},
        )

    # -- M3 ------------------------------------------------------------------------------
    def _conformal(self, request: PredictionRequest) -> SignalResult:
        c = self.config
        r = self.conformal.predict(request.probability, request.group)
        too_wide = r.set_size > c.conformal_max_set_size
        empty = r.set_size == 0 and c.conformal_empty_is_breach
        return SignalResult(
            "conformal", Status.BREACH if too_wide or empty else Status.OK,
            float(r.set_size), float(c.conformal_max_set_size),
            detail={"set": r.prediction_set, "quantile": r.quantile, "source": r.source},
        )

    # -- M4 ------------------------------------------------------------------------------
    def _drift(self, request: PredictionRequest) -> SignalResult:
        state = self.drift.read(now=request.timestamp, max_age_s=self.config.drift_max_age_s)
        if state is None:
            return SignalResult("drift", Status.UNAVAILABLE, detail={"state": "missing_or_stale"})
        status = {"none": Status.OK, "warning": Status.NEAR, "critical": Status.BREACH}[
            state.state
        ]
        return SignalResult(
            "drift", status, float(("none", "warning", "critical").index(state.state)),
            detail={"state": state.state, "computed_at": state.computed_at},
        )

    # -- M5 ------------------------------------------------------------------------------
    def _timing(self, request: PredictionRequest) -> SignalResult:
        r = self.timing.evaluate(request.patient_id, request.timestamp, request.probability)
        return SignalResult(
            "timing", Status.BREACH if r.suppress else Status.OK, float(r.tier),
            detail={"last_tier": r.last_tier, "seconds_since_last": r.seconds_since_last},
        )
