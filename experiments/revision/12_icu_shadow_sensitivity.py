"""Round 2, comment 3: what the round-1 ICU shadow refresh did not evaluate.

Part A, shadow-window length. The round-1 shadow window held 18,943 held-out-hospital patients
(half of those outside the benchmark sample, drawn within each hospital). Here windows of
250 to 18,943 patients are drawn from that same pool, within hospital and in proportion to its
size, 20 times per size (once at the full size). For each draw we record:
  * the calibration recheck: ECE on the shadow window minus ECE on the reference split < 0.05;
  * the drift state of the live window (the same 19,315 patients as in round 1) against the
    shadow window as reference: critical means the gateway still defers every request;
  * the drift state of the live window with the unit error of the drift fault: critical means the
    drift fault is still caught at its step.
With M1-M3 frozen, these two states determine the gateway's false intervention from drift (all or
none) and its drift-fault detection, so no trajectory replay is needed for Part A. The drift job
uses 200 bootstrap resamples for the calibration tests (500 in round 1).

Part B, recalibrating M3 (and M2) on the shadow window. With the full 18,943-patient shadow
window (the round-1 draw) as reference for M4, the ICU test trajectories are replayed with
  B0 frozen M1-M3 (round 1 "M4 shadow refresh");
  B1 Mondrian conformal quantiles refitted on the shadow window (coverage 0.90 as frozen);
  B2 B1 plus the M2 complement gap recomputed on the shadow window (threshold as in round 1);
and Mondrian coverage per subgroup on the live window is computed for frozen and shadow quantiles.
Reference-refresh governance (who approves a refresh, when it is repeated) is not something a
retrospective replay can evaluate and is not attempted.
"""
from __future__ import annotations

import importlib
import json
import sys

from common import OUT as R1OUT
from common import (
    VariantArtifacts,
    frozen,
    full_factory,
    np,
    pd,
    run_variants,
    trajectories,
    wide,
    with_cfg,
    without,
    workspace,
)

from agentic_gateway.data.settings import SETTINGS
from agentic_gateway.gateway import SCDITable
from agentic_gateway.gateway.drift import DriftState, run_drift_job
from agentic_gateway.metrics import ece
from agentic_gateway.models import load_model

dv = importlib.import_module("01_drift_variants")
OUT = R1OUT
SIZES = (250, 500, 1000, 2000, 4000, 8000, 18943)
REPS = 20


def pools():
    ws = workspace("icu")
    st = SETTINGS["icu"]
    cohort = pd.read_parquet(ws.require("cohort.parquet")).set_index("case_id", drop=False)
    preds = pd.read_parquet(ws.require("predictions", "random_forest.parquet"))
    model = load_model(ws.require("models", "random_forest.joblib"))
    test = preds[preds["part"] == "test"].copy()
    test["site"] = cohort.loc[test["case_id"], "site"].to_numpy()
    test["patient_id"] = cohort.loc[test["case_id"], "patient_id"].to_numpy()
    sample = pd.read_csv(ws.require("benchmark", "test_sample.csv"))
    in_bench = test["patient_id"].astype(str).isin(sample["patient_id"].astype(str))
    # identical draw to round 1 (01_drift_variants.shadow_states)
    rng = np.random.default_rng(42)
    mask = np.zeros(len(test), bool)
    for _, idx in test[~in_bench].groupby("site").groups.items():
        idx = np.asarray(list(idx))
        take = rng.choice(idx, len(idx) // 2, replace=False)
        mask[test.index.get_indexer(take)] = True
    shadow, live = test[mask], test[~mask]
    ref = preds[preds["part"] == "reference"]
    return ws, st, cohort, preds, model, shadow, live, ref


def subsample(shadow, n, rng):
    if n >= len(shadow):
        return shadow
    frac = n / len(shadow)
    parts = []
    for _, g in shadow.groupby("site"):
        k = max(1, int(round(len(g) * frac)))
        parts.append(g.sample(n=min(k, len(g)), random_state=int(rng.integers(1 << 31))))
    return pd.concat(parts)


def part_a(st, cohort, model, shadow, live, ref):
    current = dv.window(cohort, live, st)
    field, mult, offset = st.unit_shift
    shifted = current.copy()
    shifted[field] = shifted[field] * mult + offset
    shifted["probability"] = model.predict_proba(shifted[list(st.features)])[:, 1]
    ece_ref = ece(ref["y"], ref["prob"])
    rng = np.random.default_rng(2026)
    recs = []
    for n in SIZES:
        for r in range(1 if n >= len(shadow) else REPS):
            sh = subsample(shadow, n, rng)
            reference = dv.window(cohort, sh, st)
            e = ece(sh["y"], sh["prob"])
            rec = {"n": len(sh), "rep": r, "ece_shadow": float(e),
                   "recheck_pass": bool(e - ece_ref < 0.05), "events": int(sh["y"].sum())}
            for lab, w in (("live", current), ("shifted", shifted)):
                s = run_drift_job(reference, w, features=list(st.features), n_boot=200,
                                  min_group_size=50, ece_critical=0.05, computed_at=0.0,
                                  window=lab, seed=42 + r)
                rej = [t for t in s.tests if t.rejected]
                rec[f"{lab}_state"] = s.state
                rec[f"{lab}_critical_tests"] = [
                    t.target for t in rej
                    if (t.psi is not None and t.psi >= 0.25)
                    or (t.family == "calibration" and (t.delta or 0) >= 0.05)]
            recs.append(rec)
            print(n, r, rec["recheck_pass"], rec["live_state"], rec["shifted_state"],
                  rec["live_critical_tests"], flush=True)
    df = pd.DataFrame(recs)
    df.to_csv(OUT / "r2_shadow_length_draws.csv", index=False)
    summ = df.groupby("n").agg(
        draws=("rep", "size"), events_median=("events", "median"),
        ece_median=("ece_shadow", "median"), ece_max=("ece_shadow", "max"),
        recheck_pass=("recheck_pass", "mean"),
        live_not_critical=("live_state", lambda s: float((s != "critical").mean())),
        live_none=("live_state", lambda s: float((s == "none").mean())),
        shifted_critical=("shifted_state", lambda s: float((s == "critical").mean())))
    summ["usable"] = df.assign(u=(df.recheck_pass & (df.live_state != "critical")
                                  & (df.shifted_state == "critical"))).groupby("n")["u"].mean()
    print(summ.round(3).to_string())
    return summ.reset_index().round(4).to_dict(orient="records"), float(ece_ref)


def mondrian_coverage(conf, frame):
    out = {}
    for g, d in frame.groupby("group"):
        res = [conf.predict(float(p), g) for p in d["prob"]]
        cov = np.mean([int(y) in r.prediction_set for y, r in zip(d["y"], res)])
        two = np.mean([r.set_size == 2 for r in res])
        out[g] = {"n": len(d), "coverage": round(float(cov), 4), "two_label": round(float(two), 4)}
    return out


def part_b(ws, shadow, live):
    cfg, _, _ = frozen("icu")
    d = R1OUT / "drift_states"
    ov = {"test": DriftState.load(d / "icu_test_shadow.json"),
          "test_shifted": DriftState.load(d / "icu_test_shifted_shadow.json")}

    class ShadowConformal(VariantArtifacts):
        def __post_init__(self):
            super().__post_init__()
            self.conformal_frame = shadow

    base = VariantArtifacts(ws, "random_forest", drift_override=ov)
    sc = ShadowConformal(ws, "random_forest", drift_override=ov)
    # M2 complement gap on the shadow window (same transform as round 1, other data)
    m2 = importlib.import_module("03_m2_alternatives")
    from agentic_gateway.benchmark.faults import SUBGROUP_SHIFT
    from agentic_gateway.workspace import subgroup_file
    y, p, g = shadow["y"].to_numpy(float), shadow["prob"].to_numpy(float), shadow["group"].to_numpy(object)
    ctx = {"reference": p}
    for x in sorted(set(g)):
        ctx[subgroup_file(x)] = np.where(g == x, np.minimum(1.0, p + SUBGROUP_SHIFT), p)
    vals = {n: m2.stats_for(y, pp, g, "C") for n, pp in ctx.items()}
    thr = json.loads((R1OUT / "m2_alternatives_icu.json").read_text())["alt"]["C"]["threshold"]

    def tf(name, table):
        v = vals.get(name, vals["reference"])
        return SCDITable(scdi=v, subgroup_ece=table.subgroup_ece, subgroup_n=table.subgroup_n,
                         overall_ece=table.overall_ece, computed_at=table.computed_at,
                         excluded=table.excluded)

    class ShadowBoth(ShadowConformal):
        pass
    sb = ShadowBoth(ws, "random_forest", drift_override=ov, scdi_transform=tf)
    cfg_c = with_cfg(cfg, scdi_threshold=thr)
    facs = {"B0 shadow M4, frozen M1-M3": full_factory(base, cfg, "test"),
            "B1 + M3 refitted on shadow": full_factory(sc, cfg, "test"),
            "B2 + M2 complement gap on shadow": full_factory(sb, cfg_c, "test"),
            "B2 without M1": full_factory(sb, without(cfg_c, "local_calibration"), "test")}
    _, table = run_variants(trajectories("icu", "test"), facs, label="r2_icu_shadow_recal")
    w = wide(table)
    print(w.round(3).to_string())
    cov = {"frozen": mondrian_coverage(base.conformal(cfg.conformal_coverage), live),
           "shadow": mondrian_coverage(sc.conformal(cfg.conformal_coverage), live)}
    return w.round(4).to_dict(orient="index"), cov, {k: {kk: round(float(vv), 4) for kk, vv in v.items()}
                                                     for k, v in vals.items() if k == "reference"}


def main():
    ws, st, cohort, preds, model, shadow, live, ref = pools()
    report = {"n_shadow_pool": len(shadow), "n_live": len(live),
              "hospitals": int(shadow["site"].nunique())}
    if "a" in sys.argv[1:] or len(sys.argv) == 1:
        report["length"], report["ece_reference"] = part_a(st, cohort, model, shadow, live, ref)
    if "b" in sys.argv[1:] or len(sys.argv) == 1:
        report["recal"], report["coverage_live"], report["m2_shadow_reference"] = part_b(ws, shadow, live)
    name = OUT / "r2_icu_shadow_sensitivity.json"
    old = json.loads(name.read_text()) if name.exists() else {}
    old.update(report)
    name.write_text(json.dumps(old, indent=1, default=str))


if __name__ == "__main__":
    main()
