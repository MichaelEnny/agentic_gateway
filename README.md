# agentic_gateway

Code for the paper "A Step-Level Reliability Gateway for Agentic Clinical Decision Support: Architecture and Edge Deployment" by Michael O. Eniolade, submitted to the *Electronics* (MDPI) Special Issue "Agentic AI Systems: Architectures, Edge Intelligence, and Real-World Applications".

The gateway sits between a clinical LLM agent and its tools. Before each proposed action runs, it allows the action, defers it to a clinician or blocks it, using five run-time signals (local calibration, subgroup calibration gap, group-conditional conformal sets, drift state, alert timing) and a check that alerts quote tool outputs correctly.

## Contents

| Part | Folder |
|---|---|
| Gateway core, signals M1 to M5 and fusion | `src/agentic_gateway/gateway/` |
| Cohorts and splits (MIMIC-IV-ED, eICU-CRD) | `src/agentic_gateway/data/` |
| Agent harness, local LLM policy and LLM-as-judge baseline | `src/agentic_gateway/agent/` |
| Fault-injection benchmark | `src/agentic_gateway/benchmark/` |
| Edge measurement harness | `src/agentic_gateway/edge/` |
| Experiment scripts, steps 1 to 11, and frozen configs | `experiments/` |
| Aggregate results behind the paper | `results/` |

The test suite has 181 tests.

## Setup

```
uv sync --extra dev --extra figures   # figures only needed for step 10
uv run pytest
```

The project does not depend on medtrustops; cohorts are built in `src/agentic_gateway/data/`.

## Gateway core

Each proposed action that produces or uses a risk prediction becomes a `PredictionRequest` (patient id, time, probability, embedding vector, subgroup label). `ReliabilityGateway.evaluate` returns a `GatingDecision`, which is ALLOW (with or without a caveat), DEFER to a clinician, or BLOCK. It also returns every signal's status, value and latency.

| Module | File | Run time vs offline | Definition |
|---|---|---|---|
| M1 local calibration | `local_calibration.py` | run time | Neighbourhood radius grows until it holds at least 30 reference patients. Signal = \|mean predicted - observed rate\| in that neighbourhood. Sparsity is reported. |
| M2 subgroup gap (SCDI) | `scdi.py` | offline table, run-time lookup | SCDI_g = max_h \|ECE_g - ECE_h\| / overall ECE (spec para. [0021]), threshold 0.15 |
| M3 Mondrian conformal | `conformal.py` | quantiles offline, set at run time | One LAC quantile per subgroup. A set of both labels, or an empty set, is a breach. A subgroup too small for the target coverage gets the full set. |
| M4 drift | `drift.py` | background job, cached JSON | KS / chi-square per feature, KS on outputs, bootstrap test on ECE change (overall and per subgroup), with BH across all tests. PSI and KL are reported as effect sizes. A missing or stale cache counts as unavailable. |
| M5 timing | `timing.py` | run time | Suppress if inside the cooldown and the risk tier has not risen. Only allowed predictions start a cooldown. |
| Embeddings | `embeddings.py` | | Leaf indices (Hamming) for tree models, coef * x for LR, per-feature log-likelihood for NB, or a hook for a neural network |
| Fusion | `decision.py` | | Any breach stops the action. Timing breaches BLOCK, others DEFER. Signals within 20% of the threshold add a caveat. Unavailable signals stop the action (fail-closed). |

Thresholds marked PLACEHOLDER in `config.py` are defaults only. The values used in the paper were chosen on the tune split and frozen before the test split was opened; they are in `experiments/configs/gateway_frozen_ed_qwen7b-ed-full-reduced-v1.json` and `experiments/configs/gateway_frozen_icu_qwen7b-icu-full-reduced-v1.json`. `GatewayConfig().without("conformal")` gives the leave-one-out variants for the ablation.

## Data

The full runs use MIMIC-IV-ED 2.2, the `hosp` module of MIMIC-IV, and eICU-CRD 2.0. All three are available from PhysioNet to credentialed users who have signed the data use agreements. The open-access demo subsets (MIMIC-IV-ED demo 2.2, MIMIC-IV demo 2.2 and eICU-CRD demo 2.0.1) are enough to test the pipeline.

Put the files where `experiments/configs/paths.json` expects them, under `datasets/`, or point the `AGW_PATHS` environment variable to your own copy of that file. Nothing derived from the data goes into git: `.gitignore` excludes `data/`, `datasets/`, `runs/`, Parquet, model and cache files. Do not send credentialed data to hosted LLM APIs; the agent client accepts only a server on localhost.

## Running the study

The scripts in `experiments/` run in order, one setting at a time (`--setting ed` or `--setting icu`). Steps 1 to 3 write to `runs/<setting>_<source>/`. Steps 4 to 10 belong to one agent run, named with `--run`, and write to `agent_<run>/` inside that folder. Every step writes a record of its arguments, outputs and software versions to `records/`. `experiments/README.md` describes each step and its outputs.

1. Check the pipeline on the demo data with the scripted agent. `--smoke` lowers the minimum sample sizes so the small demos run; its numbers mean nothing.

   ```
   for s in 01_prepare_data 02_train_models 03_fit_gateway 04_build_benchmark             05_tune_thresholds 06_e1_static 07_e2_e3_replay 09_live_completion 10_figures; do
     uv run python experiments/$s.py --setting ed --source demo --smoke
   done
   uv run python experiments/08_e4_edge.py --setting ed --source demo --smoke --device laptop
   ```

2. For the LLM agent, start a local OpenAI-compatible server (the paper used LM Studio with Qwen2.5-7B-Instruct, Q4_K_M GGUF, 4096-token context) at `http://localhost:1234/v1`.

3. Build the cohort, models, gateway artifacts and benchmark, then tune and freeze the thresholds on the tune split:

   ```
   S=ed; RUN=qwen7b-ed-full-reduced-v1; M=<server model id>; F=<path to the .gguf file>
   uv run python experiments/01_prepare_data.py    --setting $S --source full
   uv run python experiments/02_train_models.py    --setting $S --source full
   uv run python experiments/03_fit_gateway.py     --setting $S --source full
   uv run python experiments/04_build_benchmark.py --setting $S --source full --run $RUN --policy llm --llm-model $M --llm-model-file $F
   uv run python experiments/05_tune_thresholds.py --setting $S --source full --run $RUN --fd-cap 0.10
   ```

4. Check `runs/${S}_full/agent_${RUN}/configs/gateway_frozen.json` (`_meta.cap_met` should be true) and keep a copy before opening the test split. The thresholds used in the paper are in `experiments/configs/`.

5. Evaluate on the test split:

   ```
   uv run python experiments/06_e1_static.py       --setting $S --source full --run $RUN
   uv run python experiments/07_e2_e3_replay.py    --setting $S --source full --run $RUN --judge-model $M --judge-patients 30
   uv run python experiments/09_live_completion.py --setting $S --source full --run $RUN --policy llm --llm-model $M --llm-model-file $F --live-patients 30
   uv run python experiments/10_figures.py         --setting $S --source full --run $RUN
   ```

6. Measure the gateway on each device with step 8. On an edge board, copy `runs/<setting>_full/` to the device first. It holds patient-level data, so keep it in encrypted storage.

   ```
   uv run python experiments/08_e4_edge.py --setting $S --source full --run $RUN --device pi5
   ```

7. Export the aggregate results with `uv run python experiments/11_export_results.py`.

Repeat steps 3 to 6 with `S=icu` and `RUN=qwen7b-icu-full-reduced-v1` for the intensive care setting. The full runs use three agent seeds and 360 sampled cases per split; these are the `FULL` settings in `experiments/_common.py`.

## Results

`results/` holds the aggregate numbers behind the paper: summary statistics, confidence intervals, tuning grids, frozen thresholds, edge latency and run records with model and system-prompt hashes. It contains no patient-level data. It is produced by `experiments/11_export_results.py`; see `results/README.md`.

## License

The code is released under the MIT License (see `LICENSE`). A patent application related to the gateway is pending.
