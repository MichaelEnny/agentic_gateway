"""Step 4: run the agent in observe mode on sampled cases, then inject the six faults.

    uv run python experiments/04_build_benchmark.py --setting ed --source demo --smoke
    uv run python experiments/04_build_benchmark.py --setting ed --policy llm --llm-model qwen2.5-7b-instruct

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
    p.add_argument("--parts", default="tune,test")
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
        bench = build(tools, policy, sample, setting, reference, seeds=list(params.seeds))
        bench["manifest"]["part"] = part
        bench["manifest"]["agent"] = agent
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


if __name__ == "__main__":
    main_guard(main)
