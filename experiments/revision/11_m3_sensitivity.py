"""Round 2, comment 4: sensitivity of the M3 stop-versus-caveat choice to the harm weight and the
fault weights, with patient-clustered uncertainty, and the rate at which M3 would attach a caveat.

Inputs: the stored round-1 replay rows ``m1m3_{setting}_{part}_rows.parquet`` (ED frozen drift
state; ICU test uses the shadow-refreshed drift state, ICU tune the frozen one, as in round 1).
Methods compared: "full" (M3 stops) and "without M3 (= M3 as caveat)".

For fault weights w and harm weight lambda,
    Delta(lambda, w) = NB_stop - NB_caveat
                     = sum_f w_f (early_stop_f - early_cav_f) / sum_f w_f - lambda (FI_stop - FI_cav).
M3 as a stop is preferred where Delta > 0. The break-even lambda* = (weighted early gain) / (FI gain).

Analyses
1. Grid: lambda in [0, 2] (step 0.01) x weight of the two M3-target faults (sparse, uncertainty)
   in {1, 1.5, 2, 3, 4, 5}, other faults weight 1; plus a data-fault-priority family (four data
   faults weighted 1..5, alert faults 1). Point estimates of Delta and lambda*.
2. Patient-clustered bootstrap (2000 resamples, seed 42) of lambda* for each weighting, and of
   Delta at lambda in {0.1, 0.25, 0.5, 1}.
3. Random weights: for each lambda, the share of 10,000 Dirichlet(1, ..., 1) fault-weight vectors
   for which the stop is preferred (point estimates).
4. Caveat rate: share of clean and faulty trajectories whose risk_score check had an M3 breach
   in the full gateway, i.e. the trajectories that would carry an M3 caveat if M3 were a caveat.
"""
from __future__ import annotations

import json

import numpy as np
import pandas as pd
from common import OUT

R1 = OUT  # round-1 replay rows (02, 04) and round-2 outputs share runs/revision/
FAULTS = ("drift", "subgroup", "sparse", "uncertainty", "duplicate", "ungrounded")
STOP, CAV = "full", "without M3 (= M3 as caveat)"
N_BOOT, SEED = 2000, 42
LAMS = np.round(np.arange(0, 2.0001, 0.01), 2)


def weights_m3(k):
    return {f: (k if f in ("sparse", "uncertainty") else 1.0) for f in FAULTS}


def weights_data(k):
    return {f: (k if f in ("drift", "subgroup", "sparse", "uncertainty") else 1.0) for f in FAULTS}


def per_patient(rows: pd.DataFrame):
    """Per patient: sums and counts of early (by fault kind) and FI, for both methods."""
    r = rows[rows.method.isin([STOP, CAV])].copy()
    r["early"] = (r.intercept_step == r.fault_step).astype(float)
    r["fi"] = (r.intercept_step >= 0).astype(float)
    pats = np.unique(r.patient_id)
    idx = {p: i for i, p in enumerate(pats)}
    cols = [f"{m}|{k}" for m in (STOP, CAV) for k in (*FAULTS, "clean")]
    S = np.zeros((len(pats), len(cols)))
    N = np.zeros((len(pats), len(cols)))
    for (m, k), g in r.groupby(["method", "kind"]):
        c = cols.index(f"{m}|{k}")
        v = g.fi if k == "clean" else g.early
        pi = g.patient_id.map(idx).to_numpy()
        np.add.at(S[:, c], pi, v.to_numpy())
        np.add.at(N[:, c], pi, 1.0)
    return cols, S, N


def rates(cols, S, N, w=None):
    """Rates per column for patient weights w (bootstrap counts) or all patients."""
    if w is None:
        s, n = S.sum(0), N.sum(0)
    else:
        s, n = w @ S, w @ N
    return dict(zip(cols, s / n))


def delta_parts(rt):
    de = {f: rt[f"{STOP}|{f}"] - rt[f"{CAV}|{f}"] for f in FAULTS}
    dfi = rt[f"{STOP}|clean"] - rt[f"{CAV}|clean"]
    return de, dfi


def lam_star(de, dfi, w):
    gain = sum(w[f] * de[f] for f in FAULTS) / sum(w.values())
    if dfi <= 0:
        return np.inf if gain > 0 else -np.inf
    return gain / dfi


def analyse(setting, part):
    rows = pd.read_parquet(R1 / f"m1m3_{setting}_{part}_rows.parquet")
    cols, S, N = per_patient(rows)
    rt = rates(cols, S, N)
    de, dfi = delta_parts(rt)
    res = {"early_gain_by_fault": {f: round(de[f], 4) for f in FAULTS},
           "fi_stop": round(rt[f"{STOP}|clean"], 4), "fi_caveat": round(rt[f"{CAV}|clean"], 4),
           "fi_gain": round(dfi, 4)}
    fams = {**{f"m3x{k:g}": weights_m3(k) for k in (1, 1.5, 2, 3, 4, 5)},
            **{f"datax{k:g}": weights_data(k) for k in (2, 3, 4, 5)}}
    rng = np.random.default_rng(SEED)
    npat = S.shape[0]
    bw = np.stack([np.bincount(rng.integers(0, npat, npat), minlength=npat) for _ in range(N_BOOT)])
    boot_parts = [delta_parts(rates(cols, S, N, w)) for w in bw]
    res["families"] = {}
    for name, w in fams.items():
        ls = lam_star(de, dfi, w)
        bl = np.array([lam_star(d, f, w) for d, f in boot_parts])
        fin = bl[np.isfinite(bl)]
        entry = {"lambda_star": round(float(ls), 3),
                 "lambda_star_ci": [round(float(x), 3) for x in np.percentile(bl, [2.5, 97.5])],
                 "share_boot_lambda_star_le0": round(float((bl <= 0).mean()), 3),
                 "share_boot_finite": round(float(fin.size / bl.size), 3)}
        for lam in (0.1, 0.25, 0.5, 1.0):
            dd = np.array([sum(w[f] * d[f] for f in FAULTS) / sum(w.values()) - lam * fi
                           for d, fi in boot_parts])
            point = sum(w[f] * de[f] for f in FAULTS) / sum(w.values()) - lam * dfi
            entry[f"delta_l{lam:g}"] = {"est": round(float(point), 4),
                                        "lo": round(float(np.percentile(dd, 2.5)), 4),
                                        "hi": round(float(np.percentile(dd, 97.5)), 4),
                                        "p_stop_better": round(float((dd > 0).mean()), 3)}
        res["families"][name] = entry
    # grid for the figure: Delta over lambda x M3-target weight
    ks = np.array([1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])
    grid = np.array([[sum(weights_m3(k)[f] * de[f] for f in FAULTS) / sum(weights_m3(k).values())
                      - lam * dfi for lam in LAMS] for k in ks])
    res["grid"] = {"lambda": LAMS.tolist(), "m3_weight": ks.tolist(), "delta": grid.round(5).tolist()}
    # random Dirichlet weights
    W = np.random.default_rng(SEED).dirichlet(np.ones(len(FAULTS)), 10000)
    g = W @ np.array([de[f] for f in FAULTS])
    res["dirichlet_share_stop_preferred"] = {f"{lam:g}": round(float((g - lam * dfi > 0).mean()), 3)
                                             for lam in (0, 0.1, 0.25, 0.5, 0.75, 1, 1.5, 2)}
    # caveat rate: M3 breach at the risk_score step under the full gateway
    full = rows[rows.method == STOP]
    at_risk = full.intercept_step.eq(full.risk_step)
    m3 = at_risk & full.reasons.fillna("").str.contains("conformal:breach")
    res["m3_breach_rate"] = {k: round(float(m3[full.kind == k].mean()), 4)
                             for k in ("clean", *FAULTS)}
    res["drift_near_rate_clean"] = round(float(
        full[full.kind == "clean"].reasons.fillna("").str.contains("drift:near").mean()), 4)
    return res


def main():
    report = {}
    for s in ("ed", "icu"):
        for p in ("tune", "test"):
            r = analyse(s, p)
            report[f"{s}_{p}"] = r
            print(f"== {s} {p}: FI stop {r['fi_stop']} caveat {r['fi_caveat']}; gains {r['early_gain_by_fault']}")
            for n, e in r["families"].items():
                print(f"   {n:8s} l*={e['lambda_star']:7.3f} CI {e['lambda_star_ci']} "
                      f"d@0.5={e['delta_l0.5']['est']:+.4f} ({e['delta_l0.5']['lo']:+.4f},{e['delta_l0.5']['hi']:+.4f})")
            print("   dirichlet", r["dirichlet_share_stop_preferred"])
            print("   m3 breach", r["m3_breach_rate"])
    (OUT / "r2_m3_sensitivity.json").write_text(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
