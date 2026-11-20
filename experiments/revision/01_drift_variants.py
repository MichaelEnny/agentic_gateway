"""Reviewer 2, comment 4: M4 variants.

V1 "outcome-anchored" rule: a rejected input test can only give `warning`; `critical` needs a
rejected output test with PSI >= 0.25 or a rejected calibration test with ECE worse by >= 0.05.
States are reclassified from the stored test results (no test is rerun).

Shadow refresh (ICU only): half of the held-out-hospital patients who are not in the
benchmark sample (stratified by hospital) form a shadow window with known outcomes. The model's
calibration is rechecked on it, and it replaces the drift reference; the drift job is then
rerun on the remaining patients (and on the same window with the unit error, for the drift
fault). M1-M3 keep their frozen artifacts.
"""

from __future__ import annotations

import sys
from dataclasses import replace

from common import (
    OUT,
    VariantArtifacts,
    frozen,
    full_factory,
    np,
    pd,
    run_variants,
    save_json,
    trajectories,
    wide,
    without,
    workspace,
)

from agentic_gateway.data.settings import SETTINGS
from agentic_gateway.gateway.drift import DriftState, run_drift_job
from agentic_gateway.metrics import ece
from agentic_gateway.models import load_model

STATES_DIR = OUT / "drift_states"
STATES_DIR.mkdir(exist_ok=True)


def reclassify(state: DriftState, psi_crit=0.25, ece_crit=0.05) -> DriftState:
    rejected = [t for t in state.tests if t.rejected]
    critical = any(t.family == "output" and (t.psi or 0) >= psi_crit for t in rejected) or any(
        t.family == "calibration" and (t.delta or 0) >= ece_crit for t in rejected)
    new = "critical" if critical else ("warning" if rejected else "none")
    return replace(state, state=new, window=state.window + "|outcome_anchored")


def window(cohort, preds, setting):
    frame = cohort.loc[preds["case_id"], list(setting.features)].reset_index(drop=True)
    frame["probability"] = preds["prob"].to_numpy()
    frame["label"] = preds["y"].to_numpy()
    frame["group"] = preds["group"].to_numpy()
    return frame


def shadow_states(setting_name: str) -> tuple[dict, dict]:
    ws = workspace(setting_name)
    setting = SETTINGS[setting_name]
    cohort = pd.read_parquet(ws.require("cohort.parquet")).set_index("case_id", drop=False)
    preds = pd.read_parquet(ws.require("predictions", "random_forest.parquet"))
    model = load_model(ws.require("models", "random_forest.joblib"))
    test = preds[preds["part"] == "test"].copy()
    test["site"] = cohort.loc[test["case_id"], "site"].to_numpy()
    test["patient_id"] = cohort.loc[test["case_id"], "patient_id"].to_numpy()
    sample = pd.read_csv(ws.require("benchmark", "test_sample.csv"))
    in_bench = test["patient_id"].astype(str).isin(sample["patient_id"].astype(str))
    rng = np.random.default_rng(42)
    shadow_mask = np.zeros(len(test), bool)
    pool = test[~in_bench]
    for _, idx in pool.groupby("site").groups.items():
        idx = np.asarray(list(idx))
        take = rng.choice(idx, len(idx) // 2, replace=False)
        shadow_mask[test.index.get_indexer(take)] = True
    shadow, live = test[shadow_mask], test[~shadow_mask]
    ref = preds[preds["part"] == "reference"]
    info = {
        "n_shadow": len(shadow), "n_live": len(live),
        "n_live_benchmark_patients": int(in_bench.sum()),
        "ece_reference": ece(ref["y"], ref["prob"]),
        "ece_shadow": ece(shadow["y"], shadow["prob"]),
        "ece_live": ece(live["y"], live["prob"]),
        "event_rate_shadow": float(shadow["y"].mean()),
    }
    info["calibration_recheck_pass"] = bool(info["ece_shadow"] - info["ece_reference"] < 0.05)
    reference = window(cohort, shadow, setting)
    current = window(cohort, live, setting)
    field, mult, offset = setting.unit_shift
    shifted = current.copy()
    shifted[field] = shifted[field] * mult + offset
    shifted["probability"] = model.predict_proba(shifted[list(setting.features)])[:, 1]
    out = {}
    for label, w in (("test", current), ("test_shifted", shifted)):
        st = run_drift_job(reference, w, features=list(setting.features), n_boot=500,
                           min_group_size=50, ece_critical=0.05, computed_at=0.0,
                           window=f"{label}|shadow_refresh", seed=42)
        st.save(STATES_DIR / f"{setting_name}_{label}_shadow.json")
        out[label] = st
        rej = [t for t in st.tests if t.rejected]
        info[f"{label}_state"] = st.state
        info[f"{label}_rejected"] = [(t.family, t.target, round(t.psi, 3) if t.psi else None,
                                      round(t.delta, 4) if t.delta else None) for t in rej]
    return out, info


def main(setting: str) -> None:
    cfg, cut, meta = frozen(setting)
    ws = workspace(setting)
    base = VariantArtifacts(ws, "random_forest")
    report: dict = {"setting": setting, "states": {}}
    anchored = {}
    for name in ("tune", "tune_shifted", "test", "test_shifted"):
        orig = base.drift(name)
        anchored[name] = reclassify(orig)
        anchored[name].save(STATES_DIR / f"{setting}_{name}_anchored.json")
        report["states"][name] = {"frozen": orig.state, "outcome_anchored": anchored[name].state}

    variants = {"full (frozen)": (base, cfg)}
    variants["without M4"] = (base, without(cfg, "drift"))
    variants["M4 outcome-anchored"] = (VariantArtifacts(ws, "random_forest",
                                                        drift_override=anchored), cfg)
    if setting == "icu":
        shadow, info = shadow_states(setting)
        report["shadow"] = info
        variants["M4 shadow refresh"] = (VariantArtifacts(ws, "random_forest",
                                                          drift_override=shadow), cfg)
        both = {k: reclassify(v) for k, v in shadow.items()}
        report["shadow"]["anchored_states"] = {k: v.state for k, v in both.items()}
        variants["M4 shadow + anchored"] = (VariantArtifacts(ws, "random_forest",
                                                             drift_override=both), cfg)

    factories = {k: full_factory(a, c, "test") for k, (a, c) in variants.items()}
    _, table = run_variants(trajectories(setting, "test"), factories,
                            label=f"drift_variants_{setting}_test")
    w = wide(table)
    print(w.round(3).to_string())
    report["test"] = w.round(4).to_dict(orient="index")
    # Tune split under the outcome-anchored rule (did the rule change the tune picture?)
    tf = {k: full_factory(a, c, "tune") for k, (a, c) in variants.items()
          if k in ("full (frozen)", "M4 outcome-anchored", "without M4")}
    _, ttable = run_variants(trajectories(setting, "tune"), tf,
                             label=f"drift_variants_{setting}_tune")
    report["tune"] = wide(ttable).round(4).to_dict(orient="index")
    print(wide(ttable).round(3).to_string())
    save_json(report, f"drift_variants_{setting}.json")


if __name__ == "__main__":
    for s in sys.argv[1:] or ("ed", "icu"):
        main(s)
