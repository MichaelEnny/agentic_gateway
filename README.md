# agentic_gateway

Code for the planned *Electronics* (MDPI) Special Issue paper "A Step-Level Reliability Gateway for Agentic Clinical Decision Support: Architecture and Edge Deployment". The plan is in `../paper_plan.md`.

## Status

| Part | Folder | State |
|---|---|---|
| Gateway core, signals M1 to M5 and fusion | `src/agentic_gateway/gateway/` | Built, unit tests on synthetic data |
| Cohorts and splits | `src/agentic_gateway/data/` | Built |
| Agent harness | `src/agentic_gateway/agent/` | Built, including the LLM-as-judge baseline; only the scripted policy has run. LLM prompts written, not yet tried on a real model |
| Fault-injection benchmark | `src/agentic_gateway/benchmark/` | Built |
| Edge measurement harness | `src/agentic_gateway/edge/` | Built; laptop smoke run only |
| Experiment configs and scripts | `experiments/` | Built; steps 1 to 10 (10 = figures) run end to end on both demos in smoke mode |

153 tests: the gateway core and metrics, and the agent, judge, benchmark, live-rerun, quality, edge and figure modules (on a synthetic cohort with the ED column layout).

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

Thresholds marked PLACEHOLDER in `config.py` must be set on the tuning split and frozen before the test split is used. `GatewayConfig().without("conformal")` gives the leave-one-out variants for the ablation.

## Data

No PhysioNet data, or anything derived from it, goes in this folder or in git; `.gitignore` excludes `data/`, `runs/`, CSV and Parquet. Do not send credentialed data to hosted LLM APIs.

## Running the study

See `EXPERIMENT_GUIDE.md`.
