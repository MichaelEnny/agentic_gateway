"""Step 6, experiment E1: the gateway on every test prediction, no agent.

    uv run python experiments/06_e1_static.py --setting ed --source demo --smoke

Questions: what share is allowed, caveated, deferred (overall and per subgroup); which signal
causes deferrals; are allowed predictions better calibrated than deferred ones; does Mondrian
conformal hold coverage per subgroup where pooled conformal does not.
"""

from __future__ import annotations

import time
from collections import Counter

import numpy as np
import pandas as pd
from _common import COVERAGE_GRID, main_guard, parser, setup

from agentic_gateway.assembly import Artifacts, load_config
from agentic_gateway.gateway import PredictionRequest
from agentic_gateway.metrics import auroc, brier, ece
from agentic_gateway.models import MODELS
from agentic_gateway.quality import set_size_shares
from agentic_gateway.workspace import write_json


def main() -> int:
    p = parser("E1: gateway on static test predictions.")
    p.add_argument("--models", default=",".join(MODELS))
    args = p.parse_args()
    ws, setting, _ = setup(args)
    started = time.time()
    cfg = load_config(ws.require("configs", "gateway_frozen.json")).without("timing")
    cohort = pd.read_parquet(ws.require("cohort.parquet")).set_index("case_id", drop=False)
    summary = {}

    for name in args.models.split(","):
        art = Artifacts(ws, name)
        gateway = art.gateway(cfg, "normal", "test")
        preds = pd.read_parquet(ws.require("predictions", f"{name}.parquet"))
        test = preds[preds["part"] == "test"].reset_index(drop=True)
        emb = art.embedder.transform(cohort.loc[test["case_id"], list(setting.features)])
        rows = []
        for i, r in enumerate(test.itertuples()):
            out = gateway.evaluate(PredictionRequest(str(r.patient_id), 0.0, float(r.prob),
                                                     emb[i], str(r.group)), commit=False)
            label = "caveat" if out.decision.value == "allow" and out.caveat else out.decision.value
            rows.append({"case_id": r.case_id, "group": r.group, "y": r.y, "prob": r.prob,
                         "outcome": label, **out.to_record()})
        dec = pd.DataFrame(rows)
        dec.to_parquet(ws.path("e1", f"{name}_decisions.parquet"), index=False)

        allowed = dec["outcome"].isin(["allow", "caveat"])
        reasons = Counter(r.split(":")[0] for rs in dec["reasons"] for r in rs.split("; ") if r)
        by_group = (dec.groupby("group")["outcome"].value_counts(normalize=True).unstack(
            fill_value=0).round(3).to_dict(orient="index"))
        coverage = _coverage(art, cfg.conformal_coverage, test)
        summary[name] = {
            "n": len(dec),
            "outcomes": dec["outcome"].value_counts(normalize=True).round(4).to_dict(),
            "outcomes_by_group": by_group,
            "stop_reasons": dict(reasons),
            "allowed": _quality(dec[allowed]),
            "stopped": _quality(dec[~allowed]),
            "conformal_coverage": coverage,
            "conformal_set_sizes": set_size_shares(art.conformal, COVERAGE_GRID,
                                                   test["prob"].to_numpy(),
                                                   test["group"].to_numpy()),
        }
        s = summary[name]
        print(f"{name}: {s['outcomes']}; ECE allowed {s['allowed']['ece']:.3f} vs stopped "
              f"{s['stopped']['ece']:.3f}")
    write_json(ws.path("e1", "summary_e1.json"), summary)
    _markdown(ws.path("e1", "summary_e1.md"), summary, ws)
    ws.record("06_e1_static", vars(args), {"models": list(summary)}, started)
    return 0


def _quality(d: pd.DataFrame) -> dict:
    if d.empty:
        return {"n": 0, "ece": float("nan"), "brier": float("nan"), "auroc": float("nan")}
    return {"n": len(d), "ece": ece(d["y"], d["prob"]), "brier": brier(d["y"], d["prob"]),
            "auroc": auroc(d["y"], d["prob"])}


def _coverage(art: Artifacts, coverage: float, test: pd.DataFrame) -> dict:
    out = {}
    for label, pooled in (("mondrian", False), ("pooled", True)):
        conf = art.conformal(coverage, pooled)
        hits = np.array([int(y) in conf.predict(float(p), "all" if pooled else str(g))
                         .prediction_set for y, p, g in zip(test["y"], test["prob"], test["group"])])
        out[label] = {g: {"n": int((test["group"] == g).sum()),
                          "coverage": float(hits[(test["group"] == g).to_numpy()].mean())}
                      for g in sorted(test["group"].unique())}
        out[label]["_all"] = {"n": len(test), "coverage": float(hits.mean())}
    out["target"] = coverage
    return out


def _markdown(path, summary: dict, ws) -> None:  # type: ignore[no-untyped-def]
    lines = [(f"# E1: gateway on static test predictions ({ws.setting}, {ws.source}"
              f"{', smoke' if ws.smoke else ''})"), ""]
    if ws.source == "demo":
        lines += ["**Demo data: these numbers describe no population.**", ""]
    for name, s in summary.items():
        lines += [f"## {name}", "", f"n = {s['n']}", "",
                  "| outcome | share |", "|---|---|"]
        lines += [f"| {k} | {v:.3f} |" for k, v in s["outcomes"].items()]
        lines += ["", "| set | n | ECE | Brier | AUROC |", "|---|---|---|---|---|"]
        for k in ("allowed", "stopped"):
            q = s[k]
            lines.append(f"| {k} | {q['n']} | {q['ece']:.3f} | {q['brier']:.3f} | "
                         f"{q['auroc']:.3f} |")
        lines += ["", ("Share of conformal sets with both labels (M3 cannot decide) or none, "
                       "by coverage level"), "",
                  ("| coverage | Mondrian two-label | Mondrian empty | pooled two-label | "
                   "pooled empty |"), "|---|---|---|---|---|"]
        for level, v in s["conformal_set_sizes"].items():
            m, pl = v["mondrian"]["_all"], v["pooled"]["_all"]
            lines.append(f"| {level} | {m['two_label']:.3f} | {m['empty']:.3f} | "
                         f"{pl['two_label']:.3f} | {pl['empty']:.3f} |")
        cov = s["conformal_coverage"]
        lines += ["", f"Conformal coverage, target {cov['target']:.2f}", "",
                  "| group | n | Mondrian | pooled |", "|---|---|---|---|"]
        for g, m in cov["mondrian"].items():
            lines.append(f"| {g} | {m['n']} | {m['coverage']:.3f} | "
                         f"{cov['pooled'][g]['coverage']:.3f} |")
        lines += ["", f"Stop reasons: {s['stop_reasons']}", ""]
    path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main_guard(main)
