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
| Experiment and Raspberry Pi 5 setup guides | `docs/` |

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

No PhysioNet data, or anything derived from it, goes in this folder or in git; `.gitignore` excludes `data/`, `runs/`, CSV and Parquet. Do not send credentialed data to hosted LLM APIs.

## Running the study

See `docs/EXPERIMENT_GUIDE_REDUCED_ED_ICU.md` for the full run order and `docs/PI5_EDGE_SETUP_UPDATED.md` for the Raspberry Pi 5 measurements. Full-data runs need credentialed PhysioNet access to MIMIC-IV, MIMIC-IV-ED and eICU-CRD.

## Results

`results/` holds the aggregate numbers behind the paper: summary statistics, confidence intervals, tuning grids, frozen thresholds, edge latency and run records with model and system-prompt hashes. It contains no patient-level data. It is produced by `experiments/11_export_results.py`; see `results/README.md`.

## License

The code is released under the MIT License (see `LICENSE`). A patent application related to the gateway is pending.
