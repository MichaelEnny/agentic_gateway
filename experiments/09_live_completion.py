"""Step 9, RQ2: live gated reruns on clean test cases, to measure task completion.

    uv run python experiments/09_live_completion.py --setting ed --source demo --smoke
    uv run python experiments/09_live_completion.py --setting ed --run qwen7b --policy llm --llm-model <id> --llm-model-file <gguf> --live-patients 100

Replay (step 7) stops a trajectory at its first interception. Here the agent runs live with
each gate, sees "withheld" when a step is stopped, and decides what to do next. Every case and
seed also runs with no gate, which is the reference decision. See
``agentic_gateway.benchmark.live`` for the four metrics.

Cases are the test benchmark's sample (step 4), limited to ``--live-patients`` patients drawn
with the seed (0 = all). Use the same policy as step 4. Each method reruns the agent, so with
an LLM this costs (methods x cases x seeds) episodes.
"""

from __future__ import annotations

import time

import joblib
import numpy as np
import pandas as pd
from _common import (
    PRIMARY_MODEL,
    PROMPTS,
    add_policy_args,
    add_run_arg,
    main_guard,
    make_policy,
    parser,
    setup,
)

from agentic_gateway.agent import ClinicalTools, LLMJudge
from agentic_gateway.agent.episode import TASKS
from agentic_gateway.assembly import Artifacts, load_config
from agentic_gateway.benchmark import completion_metrics, methods, run_live, summarise_live
from agentic_gateway.workspace import read_json, write_json

LIVE_METHODS = ("no_gate", "output_only", "confidence", "pooled_conformal", "full")


def main() -> int:
    p = parser("RQ2: live gated reruns for task completion.")
    add_policy_args(p)
    add_run_arg(p)
    p.add_argument("--live-patients", type=int, default=100,
                   help="patients from the test sample to rerun; 0 = all")
    p.add_argument("--judge-model", default="", help="also rerun with the LLM-as-judge gate")
    p.add_argument("--judge-url", default="http://localhost:1234/v1")
    args = p.parse_args()
    ws, setting, params = setup(args)
    started = time.time()

    policy, agent = make_policy(args, setting)
    built_with = read_json(ws.require("summary_benchmark.json"))["test"]["agent"]
    for key in ("policy", "model", "model_file_sha256", "system_prompt_sha256"):
        if key in built_with and built_with.get(key) != agent.get(key):
            raise SystemExit(f"run {args.run!r} was built by step 4 with {key}="
                             f"{built_with.get(key)!r}, not {agent.get(key)!r}; use the same "
                             "agent, or another --run")
    judge = None
    if args.judge_model:
        judge = LLMJudge.from_prompt_file(
            args.judge_model, PROMPTS / "judge.txt", TASKS[setting.name],
            base_url=args.judge_url, cache_path=ws.path("live", "judge_cache.jsonl"))
        if not judge.available():
            raise SystemExit(f"no LLM server at {args.judge_url}; start LM Studio's server")

    frozen_path = ws.require("configs", "gateway_frozen.json")
    cfg = load_config(frozen_path)
    cut = read_json(frozen_path)["_meta"]["confidence_cut"]
    cohort = pd.read_parquet(ws.require("cohort.parquet")).set_index("case_id", drop=False)
    sample = pd.read_csv(ws.require("benchmark", "test_sample.csv"), dtype={"case_id": str,
                                                                            "patient_id": str})
    if args.live_patients and args.live_patients < sample["patient_id"].nunique():
        rng = np.random.default_rng(args.seed)
        keep = rng.choice(np.sort(sample["patient_id"].unique()), args.live_patients,
                          replace=False)
        sample = sample[sample["patient_id"].isin(keep)]
    cases = cohort.loc[sample["case_id"], ["case_id", "patient_id", "group", "y"]]

    model = joblib.load(ws.require("models", f"{PRIMARY_MODEL}.joblib"))
    art = Artifacts(ws, PRIMARY_MODEL)
    tools = ClinicalTools(setting, cohort.reset_index(drop=True), model, art.embedder,
                          tier_cuts=tuple(cfg.risk_tier_cuts))
    factories = methods(art, cfg, "test", cut, ablations=False, judge=judge)
    keep_methods = (*LIVE_METHODS, "llm_judge") if judge else LIVE_METHODS
    factories = {k: factories[k] for k in keep_methods}

    rows = run_live(policy, tools, cases, factories, setting=setting.name,
                    seeds=params.seeds)
    rows = completion_metrics(rows)
    rows.to_parquet(ws.path("live", "live_rows.parquet"), index=False)
    table = summarise_live(rows, n_boot=params.analysis_boot, seed=args.seed)
    table.to_csv(ws.path("live", "summary_live.csv"), index=False)

    headline = {m: {k: float(v) for k, v in rows[rows["method"] == m][
        ["completed", "same_decision", "alert_lost", "referred"]].mean().items()}
        for m in factories}
    summary = {"agent": agent, "cases": len(cases), "seeds": list(params.seeds),
               "methods": headline}
    if judge is not None:
        summary["judge"] = judge.describe()
    write_json(ws.path("live", "summary_live.json"), summary)
    _markdown(ws, table, summary)
    ws.record("09_live_completion", vars(args), summary, started)
    print(pd.DataFrame(headline).T.round(3).to_string())
    return 0


def _markdown(ws, table: pd.DataFrame, summary: dict) -> None:  # type: ignore[no-untyped-def]
    lines = [f"# RQ2 live reruns ({ws.setting}, {ws.source}{', smoke' if ws.smoke else ''})",
             ""]
    if ws.source == "demo":
        lines += ["**Demo data: these numbers test the code only.**", ""]
    lines += [(f"Policy: {summary['agent']['policy']}; cases: {summary['cases']}; "
               f"seeds: {summary['seeds']}"), ""]
    for metric, part in table.groupby("metric", sort=False):
        lines += [f"## {metric}", "",
                  "| method | n | estimate | 95% CI | diff vs full | Holm p |",
                  "|---|---|---|---|---|---|"]
        for r in part.itertuples():
            lines.append(f"| {r.method} | {r.n} | {r.estimate:.3f} | {r.ci_low:.3f} to "
                         f"{r.ci_high:.3f} | {r.diff_vs_ref:+.3f} | {r.p_holm:.3f} |")
        lines.append("")
    ws.path("live", "summary_live.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main_guard(main)
