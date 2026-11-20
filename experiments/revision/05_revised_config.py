"""Tune-selected revised configuration replayed on the original six-fault test benchmark.

ED: without M1, M3 as a caveat (no stop), M2 = one-sided complement gap (threshold from tune).
ICU: without M1, M2 = one-sided complement gap, M4 shadow-refreshed state.
Choices follow the tune-split net-benefit analysis (equal fault weights, lambda = 0.5) and the
tune-selected M2 threshold. Post hoc; reported as a secondary analysis.
"""
import importlib
import sys

from common import (
    OUT,
    VariantArtifacts,
    frozen,
    full_factory,
    run_variants,
    save_json,
    trajectories,
    wide,
    with_cfg,
    without,
    workspace,
)

nf = importlib.import_module("04_independent_faults")
from agentic_gateway.gateway.drift import DriftState


def main(setting):
    cfg, cut, _ = frozen(setting)
    ws = workspace(setting)
    ov = None
    if setting == "icu":
        d = OUT / "drift_states"
        ov = {"test": DriftState.load(d / "icu_test_shadow.json"),
              "test_shifted": DriftState.load(d / "icu_test_shifted_shadow.json")}
    tf, thr = nf.complement_gap_transform(setting)
    base = VariantArtifacts(ws, "random_forest", drift_override=ov)
    art = VariantArtifacts(ws, "random_forest", drift_override=ov, scdi_transform=tf)
    rev = without(with_cfg(cfg, scdi_threshold=thr), "local_calibration")
    if setting == "ed":
        rev = without(rev, "conformal")
    facs = {"full": full_factory(base, cfg, "test"),
            "revised configuration": full_factory(art, rev, "test")}
    _, table = run_variants(trajectories(setting, "test"), facs, label=f"revised_{setting}")
    w = wide(table)
    print(w.round(3).to_string())
    ci = table[table.metric.isin(["early", "false_intervention"])][
        ["kind", "metric", "method", "estimate", "ci_low", "ci_high", "diff_vs_ref", "diff_low",
         "diff_high", "p_holm"]]
    print(ci.round(3).to_string())
    save_json({"wide": w.round(4).to_dict(orient="index"),
               "ci": ci.round(4).to_dict(orient="records")}, f"revised_{setting}.json")


for s in sys.argv[1:] or ("ed", "icu"):
    main(s)
