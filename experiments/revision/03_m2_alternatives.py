"""Reviewer 2, comment 3: the overall-ECE denominator of SCDI.

1. Detectability per subgroup under the frozen SCDI: the subgroup's SCDI on the reference
   table and on its own degraded table (+0.25 risk), and whether the degraded value exceeds the
   frozen threshold. Undetectable subgroups and their share of subgroup-fault trajectories.
2. Two statistics that do not divide by the overall ECE:
     D_g = max_h |ECE_g - ECE_h|          (absolute gap, ECE units)
     C_g = ECE_g - ECE_(not g)            (one-sided gap to the rest of the population)
   Threshold = k x 95th percentile of the permutation maximum (200 label shuffles, as for
   SCDI); k chosen on the tune split by the original objective (max interception with false
   intervention <= 0.10), every other frozen value unchanged. Then replayed on test.
"""

from __future__ import annotations

import sys

from common import (
    OUT,
    VariantArtifacts,
    frozen,
    full_factory,
    np,
    pd,
    per_trajectory,
    run_variants,
    save_json,
    trajectories,
    wide,
    with_cfg,
    workspace,
)

from agentic_gateway.benchmark.faults import SUBGROUP_SHIFT
from agentic_gateway.gateway.scdi import SCDITable
from agentic_gateway.metrics import ece
from agentic_gateway.workspace import subgroup_file


def shadow_override(setting):
    """ICU test: the shadow-refreshed drift state (01_drift_variants.py), so M4 does not
    defer every request and the M2 comparison is visible."""
    if setting != "icu":
        return None
    from agentic_gateway.gateway.drift import DriftState
    d = OUT / "drift_states"
    return {"test": DriftState.load(d / "icu_test_shadow.json"),
            "test_shifted": DriftState.load(d / "icu_test_shifted_shadow.json")}


GRID = (1.0, 1.25, 1.5, 2.0, 2.5, 3.0)
MIN_SIZE = 50


def stats_for(y, p, g, kind):
    groups = [x for x in sorted(set(g)) if (g == x).sum() >= MIN_SIZE]
    e = {x: ece(y[g == x], p[g == x]) for x in groups}
    if kind == "D":
        vals = np.array(list(e.values()))
        return {x: float(np.abs(vals - e[x]).max()) for x in groups}
    return {x: float(e[x] - ece(y[g != x], p[g != x])) for x in groups}


def null(y, p, g, kind, rng, n=200):
    m = [max(stats_for(y, p, rng.permutation(g), kind).values()) for _ in range(n)]
    return float(np.quantile(m, 0.95))


def main(setting: str) -> None:
    cfg, cut, meta = frozen(setting)
    ws = workspace(setting)
    preds = pd.read_parquet(ws.require("predictions", "random_forest.parquet"))
    ref = preds[preds["part"] == "reference"]
    y, p, g = ref["y"].to_numpy(float), ref["prob"].to_numpy(float), ref["group"].to_numpy(object)
    groups = sorted(set(g))
    base = VariantArtifacts(ws, "random_forest")
    report = {"setting": setting, "scdi_threshold": cfg.scdi_threshold}

    # 1. detectability under SCDI
    rows = []
    bench_test = trajectories(setting, "test")
    sub = pd.Series([t.group for t in bench_test if t.kind == "subgroup"]).value_counts()
    ref_tab = base.scdi("reference")
    for x in groups:
        deg = base.scdi(subgroup_file(x))
        rows.append({"group": x, "n_reference": int((g == x).sum()),
                     "ece_ref": ref_tab.subgroup_ece.get(x), "scdi_ref": ref_tab.scdi.get(x),
                     "ece_degraded": deg.subgroup_ece.get(x),
                     "overall_ece_degraded": deg.overall_ece,
                     "scdi_degraded": deg.scdi.get(x),
                     "scdi_rises": (deg.scdi.get(x) or 0) > (ref_tab.scdi.get(x) or 0),
                     "detectable": (deg.scdi.get(x) or 0) > cfg.scdi_threshold,
                     "test_subgroup_fault_trajs": int(sub.get(x, 0))})
    det = pd.DataFrame(rows)
    det.to_csv(OUT / f"m2_detectability_{setting}.csv", index=False)
    print(det.round(3).to_string())

    # 2. alternative statistics: precompute per context
    rng = np.random.default_rng(42)
    contexts = {"reference": p}
    for x in groups:
        contexts[subgroup_file(x)] = np.where(g == x, np.minimum(1.0, p + SUBGROUP_SHIFT), p)
    alt = {}
    for kind in ("D", "C"):
        nl = null(y, p, g, kind, rng)
        values = {name: stats_for(y, pp, g, kind) for name, pp in contexts.items()}
        alt[kind] = {"null": nl, "values": values}
        print(kind, "null", round(nl, 4))

    def transform_for(kind):
        def tf(name, table: SCDITable) -> SCDITable:
            v = alt[kind]["values"][name]
            return SCDITable(scdi=v, subgroup_ece=table.subgroup_ece, subgroup_n=table.subgroup_n,
                             overall_ece=table.overall_ece, computed_at=table.computed_at,
                             excluded=table.excluded)
        return tf

    report["alt"] = {}
    for kind, label in (("D", "absolute gap"), ("C", "one-sided complement gap")):
        art_tune = VariantArtifacts(ws, "random_forest", scdi_transform=transform_for(kind))
        nl = alt[kind]["null"]
        facs = {f"k={k}": full_factory(art_tune, with_cfg(cfg, scdi_threshold=k * nl), "tune")
                for k in GRID}
        _, tt = run_variants(trajectories(setting, "tune"), facs, label=f"m2_{kind}_{setting}_tune")
        pooled = per_trajectory(pd.read_parquet(OUT / f"m2_{kind}_{setting}_tune_rows.parquet"))
        inter = pooled[pooled.kind != "clean"].groupby("method")["intercepted"].mean()
        fi = pooled[pooled.kind == "clean"].groupby("method")["false_intervention"].mean()
        ok = fi[fi <= 0.10].index
        chosen = inter[ok].idxmax() if len(ok) else fi.idxmin()
        k = float(chosen.split("=")[1])
        thr = k * nl
        print(kind, "tune choice", chosen, "thr", thr, "\n", pd.concat([inter, fi], axis=1))
        det[f"{kind}_ref"] = det["group"].map(alt[kind]["values"]["reference"])
        det[f"{kind}_degraded"] = [alt[kind]["values"][subgroup_file(x)].get(x) for x in det.group]
        det[f"{kind}_detectable"] = det[f"{kind}_degraded"] > thr
        det[f"{kind}_flags_clean_group"] = det[f"{kind}_ref"] > thr
        ov = shadow_override(setting)
        base_t = VariantArtifacts(ws, "random_forest", drift_override=ov)
        art_t = VariantArtifacts(ws, "random_forest", drift_override=ov,
                                 scdi_transform=transform_for(kind))
        facs = {"full (SCDI, frozen)": full_factory(base_t, cfg, "test"),
                f"full (M2 = {label})": full_factory(art_t, with_cfg(cfg, scdi_threshold=thr),
                                                     "test")}
        _, table = run_variants(trajectories(setting, "test"), facs,
                                label=f"m2_{kind}_{setting}_test")
        w = wide(table)
        print(w.round(3).to_string())
        report["alt"][kind] = {"label": label, "null": nl, "k": k, "threshold": thr,
                               "tune": pd.concat([inter, fi], axis=1).round(4).to_dict(),
                               "test": w.round(4).to_dict(orient="index")}
    det.to_csv(OUT / f"m2_detectability_{setting}.csv", index=False)
    report["detectability"] = det.round(4).to_dict(orient="records")
    save_json(report, f"m2_alternatives_{setting}.json")


if __name__ == "__main__":
    for s in sys.argv[1:] or ("ed", "icu"):
        main(s)
