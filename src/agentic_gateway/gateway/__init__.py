"""Gateway core: the five reliability signals (M1-M5) and the fusion rule.

Built from the filed patent specification and ``patent/code/PRD.md``. Typical use:

    local = LocalCalibration(...).fit(ref_emb, ref_prob, ref_y)          # reference split
    scdi = compute_scdi_table(val_y, val_prob, val_group)                # validation split
    conformal = MondrianConformal(0.9).fit(cal_y, cal_prob, cal_group)   # conformal split
    drift = DriftStateReader("drift_state.json")                         # background job output
    gateway = ReliabilityGateway(GatewayConfig(), local, scdi, conformal, drift)
    decision = gateway.evaluate(PredictionRequest(...))
"""

from .config import GatewayConfig
from .conformal import MondrianConformal
from .drift import DriftState, DriftStateReader, run_drift_job
from .embeddings import Embedder, embedder_for
from .local_calibration import LocalCalibration
from .pipeline import ReliabilityGateway
from .scdi import SCDITable, compute_scdi_table, scdi_null_threshold
from .subgroups import age_band, group_labels
from .timing import AlertHistory, TimingRule, risk_tier
from .types import Decision, GatingDecision, PredictionRequest, SignalResult, Status

__all__ = [
    "AlertHistory",
    "Decision",
    "DriftState",
    "DriftStateReader",
    "Embedder",
    "GatewayConfig",
    "GatingDecision",
    "LocalCalibration",
    "MondrianConformal",
    "PredictionRequest",
    "ReliabilityGateway",
    "SCDITable",
    "SignalResult",
    "Status",
    "TimingRule",
    "age_band",
    "compute_scdi_table",
    "embedder_for",
    "group_labels",
    "risk_tier",
    "run_drift_job",
    "scdi_null_threshold",
]
