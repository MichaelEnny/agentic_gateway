"""Step 4: run the agent in observe mode on sampled cases, then inject the six faults.

    uv run python experiments/04_build_benchmark.py --setting ed --source demo --smoke
    uv run python experiments/04_build_benchmark.py --setting ed --source demo --smoke --run qwen7b-test --policy llm --llm-model <id> --llm-model-file <gguf> --max-cases 5 --parts test

Builds one benchmark for the tune part and one for the test part. The test benchmark is only
read by steps 6 to 8, after the thresholds are frozen.
"""

from __future__ import annotations

import time

import joblib
import pandas as pd
from _common import (
    PRIMARY_MODEL,
    add_policy_args,
    add_run_arg,
    base_config,
    main_guard,
    make_policy,
    parser,
    setup,
)

from agentic_gateway.agent import ClinicalTools
from agentic_gateway.benchmark import build, sample_cases
from agentic_gateway.gateway import embedder_for
from agentic_gateway.workspace import write_json


def main() -> int:
    p = parser("Build the fault-injection benchmark.")
    add_policy_args(p)
    add_run_arg(p)
    p.add_argument("--parts", default="tune,test")
    p.add_argument("--max-cases", type=int, default=0,
                   help="cap the cases per part, for a quick first test (0 = no cap); "
                        "such a run is marked as capped and is not a benchmark for the paper")
    args = p.parse_args()
    ws, setting, params = setup(args)
    started = time.time()

    cohort = pd.read_parquet(ws.require("cohort.parquet"))
    model = joblib.load(ws.require("models", f"{PRIMARY_MODEL}.joblib"))
    cfg = base_config(params, setting)
    tools = ClinicalTools(setting, cohort, model, embedder_for(model),
                          tier_cuts=tuple(cfg["risk_tier_cuts"]))
    policy, agent = make_policy(args, setting)

    reference = cohort[cohort["part"] == "reference"]
    manifests = {}
    for part in args.parts.split(","):
        cases = cohort[cohort["part"] == part]
        sample = sample_cases(cases, params.bench_cases,
                              min_per_group=params.bench_min_per_group, seed=args.seed)
        if args.max_cases:
            sample = sample.head(args.max_cases)
        bench = build(tools, policy, sample, setting, reference, seeds=list(params.seeds),
                      progress=_progress(part, len(sample) * len(params.seeds)))
        bench["manifest"]["part"] = part
        bench["manifest"]["agent"] = agent
        bench["manifest"]["max_cases"] = args.max_cases or None
        joblib.dump(bench, ws.path("benchmark", f"{part}.joblib"))
        sample[["case_id", "patient_id", "group", "weight"]].to_csv(
            ws.path("benchmark", f"{part}_sample.csv"), index=False)
        manifests[part] = bench["manifest"]
        m = bench["manifest"]
        print(f"{part}: {m['clean_trajectories']} clean, {sum(m['faulty_trajectories'].values())} "
              f"faulty, completion {m['completion_rate']:.2f}, alerts {m['alerts_in_clean']}")
    write_json(ws.path("summary_benchmark.json"), manifests)
    ws.record("04_build_benchmark", vars(args), manifests, started)
    return 0


def _progress(part: str, total: int):  # type: ignore[no-untyped-def]
    """Print one line per episode: what the agent did and how long it took."""
    state = {"n": 0, "t": time.time()}

    def report(traj) -> None:  # type: ignore[no-untyped-def]
        state["n"] += 1
        now = time.time()
        tools = " > ".join(s.tool for s in traj.steps) or "(no tool call)"
        print(f"  {part} {state['n']}/{total} {traj.trajectory_id}: "
              f"{'completed' if traj.completed else 'INCOMPLETE'} in {now - state['t']:.1f} s "
              f"| {tools}", flush=True)
        state["t"] = now

    return report


if __name__ == "__main__":
    main_guard(main)
