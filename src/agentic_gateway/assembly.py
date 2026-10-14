"""Load the fitted pieces from a workspace and assemble gateways for each run.

A *context* is the deployment state a trajectory runs under:

* ``normal``: the SCDI table and drift state computed for the part being evaluated;
* ``subgroup:<g>``: a model update degraded subgroup ``g`` and the offline SCDI job has seen it;
* ``drift``: the drift job ran on a window with a unit error in one field.

The contexts exist so that faults which are properties of the deployment (a degraded
subgroup, a drifted input stream) can be injected the way they would occur.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from .data.settings import SETTINGS, Setting
from .gateway import (
    DriftState,
    DriftStateReader,
    GatewayConfig,
    LocalCalibration,
    MondrianConformal,
    ReliabilityGateway,
    SCDITable,
)
from .gateway.embeddings import embedder_for
from .workspace import Workspace, read_json


def load_config(path: Path) -> GatewayConfig:
    values = read_json(path)
    values.pop("_meta", None)
    return GatewayConfig.from_dict(values)


@dataclass
class Artifacts:
    ws: Workspace
    model_name: str
    setting: Setting = field(init=False)
    model: Any = field(init=False)
    local: LocalCalibration = field(init=False)
    conformal_frame: pd.DataFrame = field(init=False)
    _conformal: dict[tuple[float, bool], MondrianConformal] = field(default_factory=dict)
    _scdi: dict[str, SCDITable] = field(default_factory=dict)
    _drift: dict[str, DriftState] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.setting = SETTINGS[self.ws.setting]
        self.model = joblib.load(self.ws.require("models", f"{self.model_name}.joblib"))
        self.embedder = embedder_for(self.model)
        self.local = joblib.load(self.ws.require("gateway", self.model_name, "local.joblib"))
        preds = pd.read_parquet(self.ws.require("predictions", f"{self.model_name}.parquet"))
        self.conformal_frame = preds[preds["part"] == "conformal"]

    def conformal(self, coverage: float, pooled: bool = False) -> MondrianConformal:
        key = (round(coverage, 6), pooled)
        if key not in self._conformal:
            f = self.conformal_frame
            groups = ["all"] * len(f) if pooled else f["group"]
            self._conformal[key] = MondrianConformal(coverage, pooled_fallback=self.ws.smoke) \
                .fit(f["y"], f["prob"], groups)
        return self._conformal[key]

    def scdi(self, name: str) -> SCDITable:
        if name not in self._scdi:
            self._scdi[name] = SCDITable.load(
                self.ws.require("gateway", self.model_name, "scdi", f"{name}.json"))
        return self._scdi[name]

    def drift(self, name: str) -> DriftState:
        if name not in self._drift:
            self._drift[name] = DriftState.load(
                self.ws.require("gateway", self.model_name, "drift", f"{name}.json"))
        return self._drift[name]

    def gateway(self, cfg: GatewayConfig, context: str, part: str, *,
                pooled: bool = False) -> ReliabilityGateway:
        """Gateway for one context. ``part`` picks the drift window (tune or test)."""
        scdi_name = context.replace(":", "_") if context.startswith("subgroup:") else "reference"
        drift_name = f"{part}_shifted" if context == "drift" else part
        conformal = self.conformal(cfg.conformal_coverage, pooled)
        if pooled:
            conformal = _AllGroups(conformal)
        return ReliabilityGateway(cfg, self.local, self.scdi(scdi_name), conformal,
                                  DriftStateReader(state=self.drift(drift_name)))


class _AllGroups:
    """Pooled conformal: every patient is looked up as the single group 'all'."""

    def __init__(self, inner: MondrianConformal) -> None:
        self.inner = inner

    def predict(self, probability: float, group: str):  # type: ignore[no-untyped-def]
        return self.inner.predict(probability, "all")
