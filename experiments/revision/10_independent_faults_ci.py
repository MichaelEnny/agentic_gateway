"""Round 2, comment 1: the independent-fault result as a paired, patient-clustered contrast.

Uses the stored replay rows of round 1 (``newfaults_{setting}_rows.parquet``): every clean held-out
trajectory t and its four independent-fault copies ``t-<kind>``, replayed through each method.
Nothing is re-run.

For each method, setting and fault kind (and pooled over the four kinds):

* early     share of faulty copies stopped at the fault step (the risk_score step);
* fi        false intervention: share of the clean trajectories with any stop;
* fi_risk   share of the clean trajectories stopped at the risk_score step, the step at which the
            faulty copies are scored as early. This is the like-for-like base rate;
* excess    early - fi_risk, paired on the clean trajectory the copy was built from;
* gained    share of copies stopped early whose clean source was NOT stopped at risk_score, and
  lost      the reverse (clean source stopped, copy not stopped). excess = gained - lost.

All intervals are 95% percentile intervals from 2000 bootstrap resamples of patients (each patient
contributes up to three seeds and four fault copies per seed), seed 42.
"""
from __future__ import annotations

import json

import numpy as np
import pandas as pd
from common import OUT

R1 = OUT  # round-1 replay rows (02, 04) and round-2 outputs share runs/revision/
NEW = ("decimal_slip", "inverted_output", "stale_risk", "field_dropout")
METHODS = ("full", "minus_conformal", "revised configuration", "output_only", "confidence",
           "pooled_conformal")
N_BOOT, SEED = 2000, 42


def paired_frame(rows: pd.DataFrame, method: str) -> pd.DataFrame:
    r = rows[rows.method == method]
    clean = r[r.kind == "clean"].set_index("trajectory_id")
    clean_stop = clean.intercept_step >= 0
    clean_stop_risk = clean.intercept_step.eq(clean.risk_step)
    f = r[r.kind != "clean"].copy()
    f["src"] = [t.rsplit("-", 1)[0] if t.rsplit("-", 1)[1] in NEW else t for t in f.trajectory_id]
    # trajectory ids are "<case>-s<seed>-<kind>"; kinds contain underscores, not hyphens
    f["src"] = f.apply(lambda x: x.trajectory_id[: -(len(x.kind) + 1)], axis=1)
    f["early"] = (f.intercept_step == f.fault_step).astype(float)
    f["c_fi"] = clean_stop.reindex(f.src).to_numpy(float)
    f["c_fi_risk"] = clean_stop_risk.reindex(f.src).to_numpy(float)
    assert f.c_fi.notna().all(), "unpaired faulty trajectory"
    f["gained"] = ((f.early == 1) & (f.c_fi_risk == 0)).astype(float)
    f["lost"] = ((f.early == 0) & (f.c_fi_risk == 1)).astype(float)
    return f


def boot(f: pd.DataFrame, cols: list[str], rng) -> tuple[np.ndarray, np.ndarray]:
    pid = f.patient_id.to_numpy()
    uniq, inv = np.unique(pid, return_inverse=True)
    sums = np.zeros((len(uniq), len(cols)))
    np.add.at(sums, inv, f[cols].to_numpy(float))
    cnt = np.bincount(inv, minlength=len(uniq)).astype(float)
    point = sums.sum(0) / cnt.sum()
    out = np.empty((N_BOOT, len(cols)))
    for b in range(N_BOOT):
        w = np.bincount(rng.integers(0, len(uniq), len(uniq)), minlength=len(uniq))
        out[b] = (w @ sums) / (w @ cnt)
    return point, out


def main() -> dict:
    report: dict = {}
    for setting in ("ed", "icu"):
        rows = pd.read_parquet(R1 / f"newfaults_{setting}_rows.parquet")
        rep = {"n_patients": int(rows.patient_id.nunique()),
               "n_clean": int(((rows.method == "full") & (rows.kind == "clean")).sum())}
        for method in METHODS:
            f = paired_frame(rows, method)
            rng = np.random.default_rng(SEED)
            res = {}
            for kind in (*NEW, "pooled"):
                part = f if kind == "pooled" else f[f.kind == kind]
                part = part.assign(excess=part.early - part.c_fi_risk)
                cols = ["early", "c_fi", "c_fi_risk", "excess", "gained", "lost"]
                point, bs = boot(part, cols, rng)
                lo, hi = np.percentile(bs, [2.5, 97.5], axis=0)
                d = bs[:, cols.index("excess")]
                p = min(1.0, 2 * (min((d <= 0).sum(), (d >= 0).sum()) + 1) / (d.size + 1))
                res[kind] = {c: {"est": round(float(point[i]), 4), "lo": round(float(lo[i]), 4),
                                 "hi": round(float(hi[i]), 4)} for i, c in enumerate(cols)}
                res[kind]["n"] = len(part)
                res[kind]["p_excess"] = round(p, 4)
            rep[method] = res
        report[setting] = rep
        print(setting, rep["n_patients"], "patients")
        for m in METHODS:
            r = rep[m]["pooled"]
            print(f"  {m:24s} early {r['early']['est']:.3f} ({r['early']['lo']:.3f}-{r['early']['hi']:.3f})"
                  f"  FI {r['c_fi']['est']:.3f} ({r['c_fi']['lo']:.3f}-{r['c_fi']['hi']:.3f})"
                  f"  FI@risk {r['c_fi_risk']['est']:.3f}  excess {r['excess']['est']:+.3f}"
                  f" ({r['excess']['lo']:+.3f} to {r['excess']['hi']:+.3f}) p={r['p_excess']}"
                  f"  gained {r['gained']['est']:.3f} lost {r['lost']['est']:.3f}")
    (OUT / "r2_independent_faults_ci.json").write_text(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    main()
