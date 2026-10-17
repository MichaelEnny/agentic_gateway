from __future__ import annotations

import numpy as np
import pytest

from agentic_gateway.gateway import (
    Decision,
    DriftState,
    DriftStateReader,
    GatewayConfig,
    LocalCalibration,
    MondrianConformal,
    PredictionRequest,
    ReliabilityGateway,
    SCDITable,
    SignalResult,
    Status,
)
from agentic_gateway.gateway.decision import fuse, grade


def _scdi(a: float = 0.05, b: float = 0.05) -> SCDITable:
    return SCDITable(scdi={"A": a, "B": b}, subgroup_ece={}, subgroup_n={}, overall_ece=0.05,
                     computed_at=0.0, excluded={})


def _gateway(reference, calibration, *, drift="none", scdi=None, config=None):
    local = LocalCalibration(min_neighbors=30, metric="euclidean").fit(
        reference[["e0", "e1"]].to_numpy(), reference["probability"], reference["label"]
    )
    conformal = MondrianConformal(0.9).fit(
        calibration["label"], calibration["probability"], calibration["group"]
    )
    reader = DriftStateReader(state=DriftState(state=drift, computed_at=0.0, window="w",
                                               alpha=0.05))
    return ReliabilityGateway(config or GatewayConfig(local_threshold=0.15), local,
                              scdi or _scdi(), conformal, reader)


def _request(t=60.0, p=0.05, where=(10.0, 10.0), group="A", pid="p1"):
    return PredictionRequest(pid, t, p, np.array(where), group)


# -- fusion --------------------------------------------------------------------------------


def test_grade_bands():
    assert grade(0.20, 0.15, 0.2) is Status.BREACH
    assert grade(0.13, 0.15, 0.2) is Status.NEAR
    assert grade(0.11, 0.15, 0.2) is Status.OK


def _sig(name, status, **detail):
    return SignalResult(name, status, detail=detail)


def test_fuse_block_beats_defer_and_caveat_only_when_allowed():
    cfg = GatewayConfig()
    decision, caveat, reasons = fuse(
        {"conformal": _sig("conformal", Status.BREACH),
         "timing": _sig("timing", Status.BREACH),
         "subgroup_gap": _sig("subgroup_gap", Status.NEAR)}, cfg)
    assert decision is Decision.BLOCK and not caveat and len(reasons) == 3

    decision, caveat, _ = fuse({"subgroup_gap": _sig("subgroup_gap", Status.NEAR)}, cfg)
    assert decision is Decision.ALLOW and caveat


def test_fuse_unavailable_is_fail_closed_by_default():
    sig = {"drift": _sig("drift", Status.UNAVAILABLE)}
    assert fuse(sig, GatewayConfig())[0] is Decision.DEFER
    open_cfg = GatewayConfig(fail_closed=False)
    assert fuse(sig, open_cfg)[:2] == (Decision.ALLOW, True)


def test_fuse_drift_critical_can_be_made_to_block():
    sig = {"drift": _sig("drift", Status.BREACH, state="critical")}
    assert fuse(sig, GatewayConfig())[0] is Decision.DEFER
    cfg = GatewayConfig(block_on=frozenset({"timing", "drift_critical"}))
    assert fuse(sig, cfg)[0] is Decision.BLOCK


def test_config_rejects_unknown_signal_and_builds_ablation():
    with pytest.raises(ValueError):
        GatewayConfig(disabled=frozenset({"nope"}))
    cfg = GatewayConfig().without("conformal").without("timing")
    assert cfg.disabled == {"conformal", "timing"}
    assert GatewayConfig.from_dict({"disabled": ["drift"]}).disabled == {"drift"}


# -- end to end ----------------------------------------------------------------------------


def test_clean_request_is_allowed_with_all_signals_logged(reference, calibration):
    gw = _gateway(reference, calibration)
    out = gw.evaluate(_request())
    assert out.decision is Decision.ALLOW, out.reasons
    assert set(out.signals) == {"local_calibration", "subgroup_gap", "conformal", "drift",
                                "timing"}
    assert out.latency_ns > 0 and all(s.latency_ns > 0 for s in out.signals.values())
    record = out.to_record()
    assert record["decision"] == "allow" and "conformal.status" in record


def test_miscalibrated_region_is_deferred(reference, calibration):
    out = _gateway(reference, calibration).evaluate(_request(where=(15.0, 15.0)))
    assert out.decision is Decision.DEFER
    assert out.signals["local_calibration"].status is Status.BREACH


def test_subgroup_gap_and_unknown_group(reference, calibration):
    gw = _gateway(reference, calibration, scdi=_scdi(b=0.9))
    assert gw.evaluate(_request(group="B")).signals["subgroup_gap"].status is Status.BREACH
    unknown = gw.evaluate(_request(group="Z", pid="p2"))
    assert unknown.signals["subgroup_gap"].status is Status.UNAVAILABLE
    assert unknown.signals["conformal"].detail["source"] == "full_set"
    assert unknown.decision is Decision.DEFER


def test_ambiguous_probability_has_two_label_set(reference, calibration):
    out = _gateway(reference, calibration).evaluate(_request(p=0.5))
    assert out.signals["conformal"].value == 2.0
    assert out.decision is Decision.DEFER


def test_drift_states(reference, calibration):
    warn = _gateway(reference, calibration, drift="warning").evaluate(_request())
    assert warn.decision is Decision.ALLOW and warn.caveat
    crit = _gateway(reference, calibration, drift="critical").evaluate(_request())
    assert crit.decision is Decision.DEFER


def test_duplicate_alert_blocked_but_deferred_one_does_not_start_cooldown(reference,
                                                                          calibration):
    gw = _gateway(reference, calibration)
    assert gw.evaluate(_request(t=0.0)).decision is Decision.ALLOW
    dup = gw.evaluate(_request(t=600.0))
    assert dup.decision is Decision.BLOCK and dup.signals["timing"].status is Status.BREACH

    # A deferred prediction for another patient leaves no history behind.
    assert gw.evaluate(_request(t=0.0, p=0.5, pid="p9")).decision is Decision.DEFER
    assert gw.history.last("p9") is None


def test_ablation_disables_signal(reference, calibration):
    cfg = GatewayConfig(local_threshold=0.15).without("local_calibration")
    out = _gateway(reference, calibration, config=cfg).evaluate(_request(where=(15.0, 15.0)))
    assert out.signals["local_calibration"].status is Status.DISABLED
    assert out.decision is Decision.ALLOW


def test_small_subgroup_is_caveat_only_when_enabled(reference, calibration):
    table = SCDITable(scdi={"A": 0.05}, subgroup_ece={}, subgroup_n={}, overall_ece=0.05,
                      computed_at=0.0, excluded={"B": 12})
    strict = _gateway(reference, calibration, scdi=table)
    assert strict.evaluate(_request(group="B")).decision is Decision.DEFER

    cfg = GatewayConfig(local_threshold=0.15, scdi_small_group_caveat=True)
    gw = _gateway(reference, calibration, scdi=table, config=cfg)
    small = gw.evaluate(_request(group="B"))
    assert small.signals["subgroup_gap"].status is Status.UNAVAILABLE
    assert small.signals["subgroup_gap"].detail == {"group": "B", "not_assessable": True, "n": 12}
    assert small.decision is Decision.ALLOW and small.caveat
    assert "subgroup_gap:not_assessable" in small.reasons
    # A subgroup the table never saw is still unknown, not small: it stays fail-closed.
    assert gw.evaluate(_request(group="Z", pid="p2")).decision is Decision.DEFER


def test_not_assessable_does_not_hide_another_breach():
    sig = {"subgroup_gap": _sig("subgroup_gap", Status.UNAVAILABLE, not_assessable=True),
           "conformal": _sig("conformal", Status.BREACH)}
    decision, caveat, reasons = fuse(sig, GatewayConfig())
    assert decision is Decision.DEFER and not caveat
    assert reasons == ("subgroup_gap:not_assessable", "conformal:breach")
