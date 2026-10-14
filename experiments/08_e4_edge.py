"""Step 8, experiment E4: latency, memory, M1 scaling and (with a meter) energy on this machine.

    uv run python experiments/08_e4_edge.py --setting icu --source demo --smoke --device laptop
    uv run python experiments/08_e4_edge.py --setting icu --source full --device pi5 --meter-log meter.csv

Run the same command on each board; ``--device`` names the output folder. The meter log is a
CSV with ``timestamp`` (epoch seconds) and ``watts``.

Memory: ``process_peak_mb`` is the process high-water mark after each block (what the board
must hold). ``artifacts_load_peak_mb`` and ``check_pass_peak_mb`` are traced peaks of loading
the gateway and of one untimed pass over the benchmark, to show where the memory goes.
"""

from __future__ import annotations

import time
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from _common import PRIMARY_MODEL, add_run_arg, main_guard, parser, setup

from agentic_gateway.assembly import Artifacts, load_config
from agentic_gateway.benchmark import full_factory
from agentic_gateway.edge import (
    energy_mj,
    m1_scaling,
    machine,
    peak_rss_mb,
    summarise,
    time_actions,
    traced_peak_mb,
)
from agentic_gateway.workspace import write_json


def main() -> int:
    p = parser("E4: edge measurements.")
    p.add_argument("--device", required=True, help="name of this machine, e.g. laptop, pi5")
    p.add_argument("--repeats", type=int, default=5)
    p.add_argument("--warmup", type=int, default=100)
    p.add_argument("--meter-log", type=Path, default=None)
    p.add_argument("--sizes", default="1000,5000,20000,50000")
    add_run_arg(p)
    args = p.parse_args()
    ws, setting, _ = setup(args)
    started = time.time()
    cfg = load_config(ws.require("configs", "gateway_frozen.json"))
    bench = joblib.load(ws.require("benchmark", "test.joblib"))
    trajectories = bench["clean"] + bench["faulty"]
    loaded: dict[str, Artifacts] = {}
    load_mb = traced_peak_mb(lambda: loaded.setdefault("art", Artifacts(ws, PRIMARY_MODEL)))
    art = loaded["art"]

    variants = {"full": cfg, "full_without_m1": cfg.without("local_calibration")}
    results = {"machine": machine(), "artifacts_load_peak_mb": load_mb, "variants": {}}
    for label, variant in variants.items():
        factory = full_factory(art, variant, "test")
        actions, window = time_actions(trajectories, factory,
                                       repeats=args.repeats, warmup=args.warmup)
        process_mb = peak_rss_mb()

        def one_pass(factory=factory) -> None:
            for t in trajectories:
                gate = factory(t.fault.context if t.fault else "normal")
                for s in t.steps:
                    gate.check(s)

        actions.to_parquet(ws.path("e4", args.device, f"actions_{label}.parquet"), index=False)
        table = summarise(actions)
        table.to_csv(ws.path("e4", args.device, f"latency_{label}.csv"), index=False)
        results["variants"][label] = {
            "latency": table.to_dict(orient="records"),
            "energy_mj_per_action": energy_mj(args.meter_log, window, len(actions)),
            "window": window,
            "process_peak_mb": process_mb,
            "check_pass_peak_mb": traced_peak_mb(one_pass),
        }
        row = table[table["tool"] == "all"].iloc[0]
        print(f"{label:<16} p50 {row['p50_ms']:.3f} ms  p95 {row['p95_ms']:.3f} ms  "
              f"p99 {row['p99_ms']:.3f} ms over {len(actions)} actions; "
              f"process peak {process_mb:.0f} MiB")

    # M1 scaling: reference sizes up to what this workspace has, bootstrapped beyond it
    preds = pd.read_parquet(ws.require("predictions", f"{PRIMARY_MODEL}.parquet"))
    cohort = pd.read_parquet(ws.require("cohort.parquet")).set_index("case_id", drop=False)
    ref = preds[preds["part"] == "reference"]
    x = art.embedder.transform(cohort.loc[ref["case_id"], list(setting.features)])
    sizes = [int(s) for s in args.sizes.split(",")]
    rng = np.random.default_rng(args.seed)
    need = max(sizes)
    boot = rng.integers(0, len(ref), need) if need > len(ref) else np.arange(len(ref))
    queries = x[rng.integers(0, len(x), min(200, len(x)))]
    scaling = m1_scaling(x[boot], ref["prob"].to_numpy()[boot], ref["y"].to_numpy()[boot],
                         art.embedder.metric, sizes, queries, cfg.local_min_neighbors)
    scaling["resampled"] = scaling["reference_size"] > len(ref)
    scaling.to_csv(ws.path("e4", args.device, "m1_scaling.csv"), index=False)
    results["m1_scaling"] = scaling.to_dict(orient="records")
    print(scaling.round(3).to_string(index=False))

    results["process_peak_mb"] = peak_rss_mb()
    write_json(ws.path("e4", args.device, "summary_e4.json"), results)
    ws.record(f"08_e4_edge_{args.device}", vars(args), {"device": args.device}, started)
    return 0


if __name__ == "__main__":
    main_guard(main)
