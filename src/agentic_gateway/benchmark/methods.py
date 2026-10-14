"""The gating methods compared in the paper, as factories: context -> fresh StepGate.

| method            | prediction check at risk_score      | alert checks                      |
|-------------------|-------------------------------------|-----------------------------------|
| no_gate           | none                                | none                              |
| output_only       | full gateway, but at the final step | arguments, timing                 |
| confidence        | min(p, 1-p) > cut                   | none                              |
| pooled_conformal  | M3 with one pooled quantile only    | none                              |
| full              | M1-M4                               | arguments, tags, timing (M5)      |
| minus_<signal>    | full without one signal             | as full (minus timing if removed) |
| minus_argcheck    | M1-M4                               | tags, timing                      |
| llm_judge         | none; a local LLM reviews each step | none (structural check only)      |

``llm_judge`` is added only when a judge is passed: it needs a local LLM server and one call
per new step, so step 7 runs it on a paired subset of trajectories.

The confidence cut is chosen on the tune part so that it defers as many clean trajectories as
the full gateway does there. The comparison is then between methods that cost the same.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import fields

from ..agent.gate import ConfidenceCheck, GatewayCheck, NoCheck, StepGate, new_timing
from ..agent.judge import LLMJudge
from ..assembly import Artifacts
from ..gateway import GatewayConfig
from ..gateway.types import SIGNALS

GateFactory = Callable[[str], StepGate]
PREDICTION_SIGNALS = tuple(s for s in SIGNALS if s != "timing")


def _prediction_cfg(cfg: GatewayConfig) -> GatewayConfig:
    return cfg if "timing" in cfg.disabled else cfg.without("timing")


def full_factory(art: Artifacts, cfg: GatewayConfig, part: str, *, mode: str = "step",
                 argcheck: bool = True) -> GateFactory:
    pcfg = _prediction_cfg(cfg)
    timing_on = "timing" not in cfg.disabled

    def make(context: str) -> StepGate:
        check = GatewayCheck(art.gateway(pcfg, context, part))
        timing = new_timing(cfg.cooldown_s, cfg.risk_tier_cuts) if timing_on else None
        return StepGate(check, mode=mode, timing=timing, argcheck=argcheck)

    return make


def methods(art: Artifacts, cfg: GatewayConfig, part: str, confidence_cut: float,
            *, ablations: bool = True, judge: LLMJudge | None = None
            ) -> dict[str, GateFactory]:
    out: dict[str, GateFactory] = {
        "no_gate": lambda context: StepGate(NoCheck(), mode="none"),
        "output_only": full_factory(art, cfg, part, mode="output_only"),
        "confidence": lambda context: StepGate(ConfidenceCheck(confidence_cut),
                                               argcheck=False),
    }

    pooled_cfg = GatewayConfig.from_dict(
        {**_as_dict(cfg), "disabled": [s for s in SIGNALS if s != "conformal"]})

    def pooled(context: str) -> StepGate:
        return StepGate(GatewayCheck(art.gateway(pooled_cfg, context, part, pooled=True)),
                        argcheck=False)

    out["pooled_conformal"] = pooled
    out["full"] = full_factory(art, cfg, part)
    if ablations:
        for signal in SIGNALS:
            out[f"minus_{signal}"] = full_factory(art, cfg.without(signal), part)
        out["minus_argcheck"] = full_factory(art, cfg, part, argcheck=False)
    if judge is not None:
        out["llm_judge"] = lambda context: StepGate(NoCheck(), argcheck=False, judge=judge)
    return out


def _as_dict(cfg: GatewayConfig) -> dict:
    values = {f.name: getattr(cfg, f.name) for f in fields(cfg)}
    values["block_on"] = sorted(values["block_on"])
    values["disabled"] = sorted(values["disabled"])
    values["risk_tier_cuts"] = list(values["risk_tier_cuts"])
    return values


config_to_dict = _as_dict
