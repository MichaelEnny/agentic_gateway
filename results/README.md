# Aggregate results

Aggregate outputs behind the paper "A Step-Level Reliability Gateway for Agentic Clinical Decision Support: Architecture and Edge Deployment" (Electronics, MDPI, submitted 2026).

This folder holds summary numbers only. It contains no patient-level data. The cohorts, predictions, agent trajectories, fitted models, neighbour indexes and LLM-judge caches are derived from MIMIC-IV, MIMIC-IV-ED and eICU-CRD, and the PhysioNet data use agreements do not allow sharing them. Credentialed PhysioNet users can regenerate them with `experiments/01_prepare_data.py` to `experiments/10_figures.py`.

The folder is produced by `experiments/11_export_results.py`, which copies an allowlist of files from `runs/`, refuses any file that contains a patient identifier, and suppresses demographic subgroup cells with fewer than 10 patients (those cells keep `"n": "<10"` and lose their other values). `MANIFEST.json` lists every file with its source path, the SHA-256 of the source and the SHA-256 of the exported copy.

## Layout

| Path | Contents |
|---|---|
| `ed/`, `icu/` | Emergency department (MIMIC-IV-ED) and intensive care (eICU-CRD) settings |
| `*/summary_data.json`, `summary_models.json`, `summary_gateway.json` | Cohort sizes, model performance, fitted gateway summaries |
| `*/records/` | Run records for steps 1 to 10: arguments, software versions, commits, model and system-prompt SHA-256 hashes |
| `*/gateway/*/scdi/`, `*/gateway/*/drift/` | Subgroup calibration tables (SCDI) and drift states |
| `*/agent/configs/gateway_frozen.json` | Thresholds frozen on the tune split |
| `*/agent/tuning/`, `*/agent/tuning_attempt1/` | Tuning grids, including the first attempt described as a protocol deviation |
| `*/agent/e1/` | Static analysis of single predictions |
| `*/agent/e2/` | Replay results: interception, timing, false intervention, ablation, LLM judge, quality of passed predictions, with confidence intervals and Holm-adjusted p-values |
| `*/agent/e4/` | Edge latency, M1 scaling and memory on the laptop and the Raspberry Pi 5 |
| `*/agent/live/` | Live gated reruns |
| `*/agent/figures/` | Data behind each figure (CSV) |
| `edge_logs/` | Raspberry Pi 5 machine description, temperature and clock log; laptop CPU-load log |
