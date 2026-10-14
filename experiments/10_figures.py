"""Step 10: the paper's figures from the outputs of steps 6 to 9.

    uv sync --extra figures
    uv run python experiments/10_figures.py --setting icu --source demo --smoke

Writes ``figures/<name>.{pdf,png,csv}`` in the workspace. Each figure is drawn when its inputs
exist and skipped (and listed) otherwise, so it can run after any subset of steps. The CSV
beside each figure holds exactly the values plotted.

The architecture figure is a drawing, not data, and is not made here.
"""

from __future__ import annotations

import time

import pandas as pd
from _common import PRIMARY_MODEL, main_guard, parser, setup

from agentic_gateway import figures
from agentic_gateway.workspace import read_json, write_json

SIGNALS = ("local_calibration", "subgroup_gap", "conformal", "drift")  # timing: not per call


def main() -> int:
    p = parser("Draw the paper figures.")
    p.add_argument("--model", default=PRIMARY_MODEL, help="model for the E1 coverage figure")
    args = p.parse_args()
    ws, _, params = setup(args)
    started = time.time()
    root = ws.root
    out = root / "figures"
    made, skipped = [], {}

    def need(*parts: str):  # type: ignore[no-untyped-def]
        path = root.joinpath(*parts)
        return path if path.exists() else None

    replay_rows = need("e2", "replay_rows.parquet")
    if replay_rows:
        rows = pd.read_parquet(replay_rows)
        figures.interception_outcomes(rows, out / "fig_interception_outcomes")
        figures.tradeoff(rows, out / "fig_tradeoff")
        made += ["fig_interception_outcomes", "fig_tradeoff"]
        latency = _signal_latency(root)
        figures.ablation(rows, out / "fig_ablation", latency, n_boot=params.analysis_boot,
                         seed=args.seed)
        made.append("fig_ablation")
        if latency is None:
            skipped["fig_ablation (latency panel)"] = "no e4/<device>/latency_full.csv"
    else:
        for name in ("fig_interception_outcomes", "fig_tradeoff", "fig_ablation"):
            skipped[name] = "no e2/replay_rows.parquet (step 7)"

    devices = sorted(d.name for d in (root / "e4").iterdir()) if (root / "e4").exists() else []
    actions = {d: {v: pd.read_parquet(f) for v in ("full", "full_without_m1")
                   if (f := root / "e4" / d / f"actions_{v}.parquet").exists()}
               for d in devices}
    actions = {d: a for d, a in actions.items() if a}
    if actions:
        figures.edge_latency(actions, out / "fig_edge_latency")
        made.append("fig_edge_latency")
    else:
        skipped["fig_edge_latency"] = "no e4/<device>/actions_*.parquet (step 8)"
    scaling = {d: pd.read_csv(f) for d in devices
               if (f := root / "e4" / d / "m1_scaling.csv").exists()}
    if scaling:
        figures.m1_scaling(dict(list(scaling.items())[:3]), out / "fig_m1_scaling")
        made.append("fig_m1_scaling")
    else:
        skipped["fig_m1_scaling"] = "no e4/<device>/m1_scaling.csv (step 8)"

    e1 = need("e1", "summary_e1.json")
    if e1 and args.model in (s := read_json(e1)):
        figures.subgroup_coverage(s[args.model]["conformal_coverage"],
                                  out / "fig_subgroup_coverage")
        made.append("fig_subgroup_coverage")
    else:
        skipped["fig_subgroup_coverage"] = f"no E1 summary for {args.model} (step 6)"

    live = need("live", "summary_live.csv")
    if live:
        figures.live_completion(pd.read_csv(live), out / "fig_live_completion")
        made.append("fig_live_completion")
    else:
        skipped["fig_live_completion"] = "no live/summary_live.csv (step 9)"

    quality = need("e2", "passed_quality.json")
    if quality:
        figures.passed_quality(read_json(quality), out / "fig_passed_quality")
        made.append("fig_passed_quality")
    else:
        skipped["fig_passed_quality"] = "no e2/passed_quality.json (step 7)"

    write_json(out / "index.json", {"made": made, "skipped": skipped,
                                    "demo": ws.source == "demo"})
    ws.record("10_figures", vars(args), {"made": made, "skipped": skipped}, started)
    print(f"made {len(made)}: {', '.join(made)}")
    for name, why in skipped.items():
        print(f"skipped {name}: {why}")
    if ws.source == "demo":
        print("demo data: these figures check the drawing code only")
    return 0


def _signal_latency(root) -> dict[str, float] | None:  # type: ignore[no-untyped-def]
    """Median per-signal latency on risk_score actions, from the first device's step 8."""
    e4 = root / "e4"
    files = sorted(e4.glob("*/latency_full.csv")) if e4.exists() else []
    if not files:
        return None
    table = pd.read_csv(files[0]).set_index("tool")
    row = table.loc["risk_score"] if "risk_score" in table.index else table.loc["all"]
    return {s: float(row[f"{s}_p50_ms"]) for s in SIGNALS if f"{s}_p50_ms" in row.index}


if __name__ == "__main__":
    main_guard(main)
