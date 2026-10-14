"""The agent's four clinical tools, backed by the prepared split and the saved risk model.

Tools read only the prepared case table, never the raw database, and run on this machine.
``risk_score`` returns the probability and tier to the agent; the embedding and subgroup go
into ``hidden`` for the gateway and are not shown to the LLM.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np
import pandas as pd

from ..data.settings import Setting
from ..gateway.embeddings import Embedder
from ..gateway.timing import risk_tier

TOOL_SCHEMAS: list[dict[str, Any]] = [
    {"type": "function", "function": {
        "name": "fetch_record",
        "description": "Return the structured triage or admission record for a case.",
        "parameters": {"type": "object", "properties": {"case_id": {"type": "string"}},
                       "required": ["case_id"]}}},
    {"type": "function", "function": {
        "name": "risk_score",
        "description": "Return the risk model's probability and risk tier (0-3) for a case.",
        "parameters": {"type": "object", "properties": {"case_id": {"type": "string"}},
                       "required": ["case_id"]}}},
    {"type": "function", "function": {
        "name": "prior_alerts",
        "description": "List alerts already sent for this patient in this session.",
        "parameters": {"type": "object", "properties": {"patient_id": {"type": "string"}},
                       "required": ["patient_id"]}}},
    {"type": "function", "function": {
        "name": "draft_alert",
        "description": "Send an alert to the clinical team. Quote the vital signs you relied "
                       "on exactly as they appear in the record.",
        "parameters": {"type": "object", "properties": {
            "patient_id": {"type": "string"},
            "risk": {"type": "number", "description": "probability from risk_score"},
            "cited": {"type": "object", "description": "field name -> value from the record"},
            "text": {"type": "string"}},
            "required": ["patient_id", "risk", "cited", "text"]}}},
    {"type": "function", "function": {
        "name": "close_case",
        "description": "Finish the review without an alert, with a short note.",
        "parameters": {"type": "object", "properties": {
            "case_id": {"type": "string"}, "note": {"type": "string"}},
            "required": ["case_id", "note"]}}},
]

REQUIRED_ARGS = {t["function"]["name"]: tuple(t["function"]["parameters"]["required"])
                 for t in TOOL_SCHEMAS}


def _clean(value: Any) -> Any:
    if isinstance(value, (float, np.floating)) and math.isnan(float(value)):
        return None
    if isinstance(value, np.generic):
        return value.item()
    return value


class ClinicalTools:
    def __init__(self, setting: Setting, cases: pd.DataFrame, model: Any, embedder: Embedder,
                 group_col: str = "group", tier_cuts: tuple[float, ...] = (0.1, 0.3, 0.6)):
        self.setting = setting
        self.cases = cases.set_index("case_id", drop=False)
        self.model = model
        self.embedder = embedder
        self.group_col = group_col
        self.tier_cuts = tier_cuts
        self.alerts: dict[str, list[dict[str, Any]]] = {}

    def reset(self) -> None:
        self.alerts = {}

    # -- scoring, shared with fault injection --------------------------------------------
    def record_of(self, case_id: str) -> dict[str, Any]:
        row = self.cases.loc[case_id]
        record = {"case_id": case_id, "patient_id": str(row["patient_id"])}
        record.update({f: _clean(row[f]) for f in self.setting.features})
        return record

    def score_record(self, record: dict[str, Any]) -> tuple[float, np.ndarray]:
        frame = pd.DataFrame([{f: record.get(f) for f in self.setting.features}])
        for f in self.setting.numeric:
            frame[f] = pd.to_numeric(frame[f], errors="coerce").astype(float)
        prob = float(self.model.predict_proba(frame)[0, 1])
        return prob, self.embedder.transform(frame)[0]

    # -- tools ---------------------------------------------------------------------------
    def call(self, tool: str, args: dict[str, Any]) -> tuple[Any, dict[str, Any]]:
        """Run one tool. Returns (output shown to the agent, hidden data for the gateway)."""
        if tool == "fetch_record":
            return self.record_of(str(args["case_id"])), {}
        if tool == "risk_score":
            case_id = str(args["case_id"])
            prob, emb = self.score_record(self.record_of(case_id))
            tier = risk_tier(prob, self.tier_cuts)
            group = str(self.cases.loc[case_id, self.group_col])
            pid = str(self.cases.loc[case_id, "patient_id"])
            return ({"case_id": case_id, "probability": round(prob, 4), "risk_tier": tier},
                    {"probability": prob, "embedding": emb, "group": group, "tier": tier,
                     "patient_id": pid})
        if tool == "prior_alerts":
            return list(self.alerts.get(str(args["patient_id"]), [])), {}
        if tool == "draft_alert":
            pid = str(args["patient_id"])
            alert = {"alert_id": f"{pid}-{len(self.alerts.get(pid, [])) + 1}",
                     "risk": args.get("risk"), "text": args.get("text", "")}
            self.alerts.setdefault(pid, []).append(alert)
            return {"sent": True, **alert}, {}
        if tool == "close_case":
            return {"closed": True}, {}
        raise KeyError(f"unknown tool {tool!r}")
