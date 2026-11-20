"""Reviewer 2, comments 1 and 2: what M1 and M3 add, and a net-benefit analysis.

Variants (each on tune and test): full; without M1; without M3 (identical in stopping
behaviour to treating a two-label or empty conformal set as a caveat); without M1 and M3;
M3 at coverage 0.85, 0.90, 0.95. ED uses the frozen gateway; ICU uses the shadow-refreshed
drift state from 01_drift_variants.py (so M4 is not stopping everything).

Net benefit per gated trajectory, for a harm weight lambda on a false intervention:
    NB(lambda, w) = sum_f w_f * early_f / sum_f w_f  -  lambda * false_intervention
Weightings: equal; "data-fault priority" (four data faults x2); "M3-target priority"
(sparse and uncertainty x3). M1 unique catches: stops whose only stopping reason is M1.
"""

from __future__ import annotations

import sys

from common import (
    OUT,
    VariantArtifacts,
    frozen,
    full_factory,
    per_trajectory,
    run_variants,
    save_json,
    trajectories,
    wide,
    with_cfg,
    without,
    workspace,
)

from agentic_gateway.gateway.drift import DriftState

WEIGHTS = {
    "equal": dict.fromkeys(("drift", "subgroup", "sparse", "uncertainty", "duplicate",
                            "ungrounded"), 1.0),
    "data_priority": {"drift": 2, "subgroup": 2, "sparse": 2, "uncertainty": 2,
                      "duplicate": 1, "ungrounded": 1},
    "m3_target_priority": {"drift": 1, "subgroup": 1, "sparse": 3, "uncertainty": 3,
                           "duplicate": 1, "ungrounded": 1},
}
LAMBDAS = (0.0, 0.25, 0.5, 1.0, 2.0)


def artifacts(setting):
    ws = workspace(setting)
    if setting == "icu":
        d = OUT / "drift_states"
        override = {"test": DriftState.load(d / "icu_test_shadow.json"),
                    "test_shifted": DriftState.load(d / "icu_test_shifted_shadow.json")}
        return VariantArtifacts(ws, "random_forest", drift_override=override)
    return VariantArtifacts(ws, "random_forest")


def net_benefit(w):
    out = {}
    for wname, weights in WEIGHTS.items():
        tot = sum(weights.values())
        early = sum(w[k] * v for k, v in weights.items()) / tot
        for lam in LAMBDAS:
            out[f"NB_{wname}_l{lam}"] = early - lam * w["false_intervention"]
    return out


def main(setting: str) -> None:
    cfg, cut, _ = frozen(setting)
    report = {"setting": setting}
    for part in ("tune", "test"):
        art = artifacts(setting) if part == "test" else VariantArtifacts(workspace(setting),
                                                                         "random_forest")
        variants = {
            "full": cfg,
            "without M1": without(cfg, "local_calibration"),
            "without M3 (= M3 as caveat)": without(cfg, "conformal"),
            "without M1 and M3": without(cfg, "local_calibration", "conformal"),
        }
        for cov in (0.85, 0.90, 0.95):
            if abs(cov - cfg.conformal_coverage) > 1e-9:
                variants[f"M3 coverage {cov:.2f}"] = with_cfg(cfg, conformal_coverage=cov)
        factories = {k: full_factory(art, c, part) for k, c in variants.items()}
        rows, table = run_variants(trajectories(setting, part), factories,
                                   label=f"m1m3_{setting}_{part}")
        w = wide(table)
        nb = w.apply(net_benefit, axis=1, result_type="expand")
        w = w.join(nb)
        print(part, "\n", w.iloc[:, :10].round(3).to_string())
        # M1 unique catches in the full gateway
        full = per_trajectory(rows[rows["method"] == "full"])
        stops = full[full["intercept_step"] >= 0]
        reasons = stops["reasons"].fillna("")
        breach = reasons.str.findall(r"(\w+):(?:breach|unavailable)")
        only_m1 = breach.apply(lambda r: set(r) == {"local_calibration"})
        any_m1 = breach.apply(lambda r: "local_calibration" in r)
        report[part] = {
            "table": w.round(4).to_dict(orient="index"),
            "m1_any_breach_at_stop_by_kind": stops[any_m1].groupby("kind").size().to_dict(),
            "m1_only_reason_by_kind": stops[only_m1].groupby("kind").size().to_dict(),
            "m1_only_early_by_kind": stops[only_m1 & (stops["early"] == 1)]
            .groupby("kind").size().to_dict(),
            "n_by_kind": full.groupby("kind").size().to_dict(),
        }
    save_json(report, f"m1m3_{setting}.json")


if __name__ == "__main__":
    for s in sys.argv[1:] or ("ed", "icu"):
        main(s)
