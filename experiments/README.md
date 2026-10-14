# experiments

Numbered scripts, run in order, one setting at a time. Each takes `--setting {ed,icu}`, `--source {demo,full}` (default `demo`), `--smoke` and `--seed` (default 42). `--source full` is refused while `../DATA_ACCESS.md` says credentialed analysis may not begin; `--smoke` is refused with `--source full`.

```
uv run python experiments/01_prepare_data.py --setting ed --source demo --smoke
```

| Step | Script | Does | Main outputs (in `runs/<setting>_<source>[_smoke]/`) |
|---|---|---|---|
| 1 | `01_prepare_data.py` | Cohort, subgroup labels, five patient-disjoint parts | `cohort.parquet`, `summary_data.json` |
| 2 | `02_train_models.py` | LR and RF on `fit`; scores every part | `models/`, `predictions/`, `summary_models.json` |
| 3 | `03_fit_gateway.py` | M1 index, SCDI tables and null threshold, drift states | `gateway/<model>/`, `summary_gateway.json` |
| 4 | `04_build_benchmark.py` | Agent in observe mode on sampled `tune` and `test` cases; six injected faults. `--policy {scripted,llm}` | `benchmark/{tune,test}.joblib`, `summary_benchmark.json` |
| 5 | `05_tune_thresholds.py` | Grid on the tune benchmark; freezes thresholds. `--fd-cap` (default 0.10) | `configs/gateway_frozen.json`, `tuning/grid.csv` |
| 6 | `06_e1_static.py` | E1: gateway on every static test prediction | `e1/` |
| 7 | `07_e2_e3_replay.py` | E2 methods and E3 ablation, replayed on the test benchmark. `--judge-model` adds the LLM-as-judge baseline on a paired subset (`--judge-patients`) | `e2/` |
| 8 | `08_e4_edge.py` | E4: latency, M1 scaling, energy with a meter. `--device` names the output folder | `e4/<device>/` |
| 9 | `09_live_completion.py` | RQ2: live gated reruns on clean test cases; task completion against the ungated run. Same `--policy` options as step 4; `--live-patients` caps the cost | `live/` |
| 10 | `10_figures.py` | The paper's figures from steps 6 to 9; skips any whose inputs are missing. Needs `uv sync --extra figures` | `figures/` |

| RQ | Answered by |
|---|---|
| RQ1 interception timing | step 7 |
| RQ2 cost on clean trajectories | steps 7 and 9 |
| RQ3 signal ablation vs cost | steps 7 and 8 |
| RQ4 edge feasibility | step 8 |
| Supporting: static predictions | step 6 |

Steps 1 to 3 write to `runs/<setting>_<source>[_smoke]/`. Steps 4 to 10 take `--run NAME` (default `scripted`) and write to `agent_<NAME>/` inside it, so each agent run (scripted, or each LLM) keeps its own results. Use the same `--run` for every step of a run.

Every step writes `records/<step>.json` with its arguments, outputs, timing and versions. Steps 6 to 8 read only `configs/gateway_frozen.json`; commit a copy of it before looking at test results.

`_common.py` holds the shared command line and the `FULL` and `SMOKE` parameter sets. `configs/` holds the dataset paths (`paths.json`) and the starting gateway values (`gateway_base.json`).

## Before the paper runs

- `--judge-model` (step 7) reads `prompts/judge.txt` and needs the same local server.
- `--policy llm` reads `prompts/system_{ed,icu}.txt` and needs a local OpenAI-compatible server (LM Studio, `http://localhost:1234/v1`) and its own `--run` name. Start with `--max-cases 5`. The full first-run checklist is section 8.7 of the guide. The prompts have not yet been tried on a real model.
- Both demos have run end to end with `--policy scripted --smoke`. Those numbers check the plumbing and mean nothing.

Details, design choices and open items: `../EXPERIMENT_GUIDE.md`.
