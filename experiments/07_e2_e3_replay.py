"""Step 7, experiments E2 (methods) and E3 (leave-one-out ablation) on the test benchmark.

    uv run python experiments/07_e2_e3_replay.py --setting ed --source demo --smoke
    uv run python experiments/07_e2_e3_replay.py --setting ed --judge-model qwen2.5-7b-instruct

Every method replays the same stored trajectories. Writes the per-trajectory rows, the
summary table with patient-clustered bootstrap intervals and Holm-adjusted paired tests
against the full gateway, and a Markdown digest.

With ``--judge-model``, the LLM-as-judge baseline also runs, through a local server. It costs
one LLM call per distinct step, so it runs on all trajectories of ``--judge-patients``
patients drawn with the seed (0 = every patient), and is compared there, paired, with the
main methods. Its results go to separate ``judge_*`` files; the main table is unchanged.
"""

from __future__ import annotations

import time

import joblib
import numpy as np
import pandas as pd
from _common import PRIMARY_MODEL, PROMPTS, add_run_arg, main_guard, parser, setup

from agentic_gateway.agent import LLMJudge
from agentic_gateway.agent.episode import TASKS
from agentic_gateway.assembly import Artifacts, load_config
from agentic_gateway.benchmark import methods, replay, summarise
from agentic_gateway.quality import passed_quality
from agentic_gateway.workspace import read_json, write_json


def main() -> int:
    p = parser("E2/E3: replay the test benchmark through every method.")
    p.add_argument("--judge-model", default="", help="run the LLM-as-judge baseline")
    p.add_argument("--judge-url", default="http://localhost:1234/v1")
    p.add_argument("--judge-patients", type=int, default=100,
                   help="patients whose trajectories the judge reviews; 0 = all")
    add_run_arg(p)
    args = p.parse_args()
    ws, _, params = setup(args)
    started = time.time()
    judge = None
    if args.judge_model:  # check the server before the long main replay
        judge = LLMJudge.from_prompt_file(
            args.judge_model, PROMPTS / "judge.txt", TASKS[ws.setting],
            base_url=args.judge_url, cache_path=ws.path("e2", "judge_cache.jsonl"))
        if not judge.available():
            raise SystemExit(f"no LLM server at {args.judge_url}; start LM Studio's server")
    frozen_path = ws.require("configs", "gateway_frozen.json")
    cfg = load_config(frozen_path)
    cut = read_json(frozen_path)["_meta"]["confidence_cut"]
    bench = joblib.load(ws.require("benchmark", "test.joblib"))
    trajectories = bench["clean"] + bench["faulty"]

    art = Artifacts(ws, PRIMARY_MODEL)
    factories = methods(art, cfg, "test", cut)
    rows = replay(trajectories, factories)
    rows.to_parquet(ws.path("e2", "replay_rows.parquet"), index=False)

    table = summarise(rows, n_boot=params.analysis_boot, seed=args.seed)
    table.to_csv(ws.path("e2", "summary_e2_e3.csv"), index=False)
    headline = _headline(table)
    write_json(ws.path("e2", "headline.json"), headline)
    _markdown(ws, table, bench["manifest"])
    quality = passed_quality(rows, art.conformal(cfg.conformal_coverage))
    write_json(ws.path("e2", "passed_quality.json"), quality)
    _quality_markdown(ws, quality, "passed_quality.md")
    outputs = {"methods": list(factories), "trajectories": len(trajectories)}
    print(pd.DataFrame(headline).T.round(3).to_string())

    if judge is not None:
        outputs["judge"] = _run_judge(judge, args, ws, params, art, cfg, cut, trajectories,
                                      bench["manifest"])
    ws.record("07_e2_e3_replay", vars(args), outputs, started)
    return 0


JUDGE_COMPARED = ("no_gate", "output_only", "confidence", "pooled_conformal", "full")


def _run_judge(judge, args, ws, params, art, cfg, cut, trajectories,  # type: ignore[no-untyped-def]
               manifest) -> dict:
    patients = sorted({t.patient_id for t in trajectories})
    if args.judge_patients and args.judge_patients < len(patients):
        rng = np.random.default_rng(args.seed)
        patients = sorted(rng.choice(patients, args.judge_patients, replace=False))
    chosen = set(patients)
    subset = [t for t in trajectories if t.patient_id in chosen]

    factories = methods(art, cfg, "test", cut, ablations=False, judge=judge)
    factories = {k: v for k, v in factories.items() if k in (*JUDGE_COMPARED, "llm_judge")}
    rows = replay(subset, factories)
    rows.to_parquet(ws.path("e2", "judge_rows.parquet"), index=False)
    table = summarise(rows, n_boot=params.analysis_boot, seed=args.seed)
    table.to_csv(ws.path("e2", "judge_summary.csv"), index=False)
    _markdown(ws, table, manifest, name="judge_summary.md",
              title=f"LLM-as-judge, {len(chosen)} patients, {len(subset)} trajectories")
    quality = passed_quality(rows, art.conformal(cfg.conformal_coverage))
    write_json(ws.path("e2", "judge_passed_quality.json"), quality)
    _quality_markdown(ws, quality, "judge_passed_quality.md")
    info = {**judge.describe(), "patients": len(chosen), "trajectories": len(subset)}
    write_json(ws.path("e2", "judge_headline.json"),
               {"judge": info, "methods": _headline(table)})
    print(pd.DataFrame(_headline(table)).T.round(3).to_string())
    print(f"judge: {info['stats']}; {info['uncached_calls']} new calls, "
          f"p50 {info['call_p50_ms']} ms")
    return info


def _headline(table: pd.DataFrame) -> dict:
    """Pooled view per method: each fault-type metric averaged over fault types, and false
    intervention on clean trajectories."""
    def mean_over_faults(metric: str) -> pd.Series:
        return table[table["metric"] == metric].groupby("method")["estimate"].mean()

    early = mean_over_faults("early")
    pooled = {m: mean_over_faults(m) for m in (
        "intercepted", "early", "eir", "intervention_gap", "steps_saved", "tokens_saved")}
    fi = table[(table["metric"] == "false_intervention")].set_index("method")["estimate"]
    return {m: {**{f"{k}_mean_over_faults": v.get(m) for k, v in pooled.items()},
                "false_intervention": fi.get(m)} for m in early.index}


def _quality_markdown(ws, quality: dict, name: str) -> None:  # type: ignore[no-untyped-def]
    lines = [(f"# Quality of predictions each gate let through ({ws.setting}, {ws.source}"
              f"{', smoke' if ws.smoke else ''})"), "",
             ("Passed: trajectories with no interception, acted on without clinician review. "
              "Coverage: Mondrian conformal at the frozen level."), ""]
    for subset in ("clean", "faulty", "all"):
        lines += [f"## {subset} trajectories", "",
                  ("| method | passed n | ECE | Brier | AUROC | coverage | stopped n | ECE | "
                   "coverage |"), "|---|---|---|---|---|---|---|---|---|"]
        for method, per in quality.items():
            p, s = per[subset]["passed"], per[subset]["stopped"]
            pc = p.get("coverage", {}).get("_all", float("nan"))
            sc = s.get("coverage", {}).get("_all", float("nan"))
            lines.append(f"| {method} | {p['n']} | {p['ece']:.3f} | {p['brier']:.3f} | "
                         f"{p['auroc']:.3f} | {pc:.3f} | {s['n']} | {s['ece']:.3f} | "
                         f"{sc:.3f} |")
        lines.append("")
    ws.path("e2", name).write_text("\n".join(lines), encoding="utf-8")


def _markdown(ws, table: pd.DataFrame, manifest: dict, *,  # type: ignore[no-untyped-def]
              name: str = "summary_e2_e3.md", title: str = "E2/E3 replay") -> None:
    lines = [f"# {title} ({ws.setting}, {ws.source}{', smoke' if ws.smoke else ''})", ""]
    if ws.source == "demo":
        lines += ["**Demo data: these numbers test the code only.**", ""]
    lines += [(f"Policy: {manifest['policy']}; clean trajectories: "
               f"{manifest['clean_trajectories']}; faulty: {manifest['faulty_trajectories']}"),
              ""]
    for (kind, metric), part in table.groupby(["kind", "metric"], sort=True):
        lines += [f"## {kind}: {metric}", "",
                  "| method | n | estimate | 95% CI | diff vs full | Holm p |",
                  "|---|---|---|---|---|---|"]
        for r in part.itertuples():
            lines.append(f"| {r.method} | {r.n} | {r.estimate:.3f} | {r.ci_low:.3f} to "
                         f"{r.ci_high:.3f} | {r.diff_vs_ref:+.3f} | {r.p_holm:.3f} |")
        lines.append("")
    ws.path("e2", name).write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main_guard(main)
