# Peer-review analyses (post hoc)

These scripts produce the analyses added during peer review of the *Electronics* manuscript (electronics-4688310): Sections 3.13 and 4.5, Tables 9–14, Figures 8–10 and Supplementary Tables S4–S6. They replay the trajectories stored by steps 4 and 7 of the main pipeline through modified gateways. No agent is re-run, nothing in `src/` is changed, and the frozen primary analysis is not affected.

Every analysis here was designed after the held-out results were known, so all of it is **post hoc**. Wherever a threshold or a configuration had to be chosen, it was chosen on the tune split with the original objective, and the test split was replayed once. The frozen configurations in `experiments/configs/` remain the system the paper evaluates.

## Prerequisites

Run the main pipeline first (steps 1 to 7 in `experiments/README.md`) for both settings, with the run names `qwen7b-ed-full-reduced-v1` and `qwen7b-icu-full-reduced-v1`. The scripts read the stored benchmarks, predictions, fitted artifacts and frozen configurations from `runs/`.

## Scripts

Run them from this folder with the project environment (`uv run python <script>` or `.venv/Scripts/python.exe <script>`). Each script takes an optional setting (`ed` or `icu`); without one, it runs both.

| Script | Round | Reviewer question | What it does |
|---|---|---|---|
| `01_drift_variants.py` | 1 | Input-PSI drift rule; ICU blanket deferral | Outcome-anchored M4 rule; ICU shadow window with calibration recheck and drift-reference refresh |
| `02_m1_m3_net_benefit.py` | 1 | Value of M1 and M3 | Without M1 / M3, M3 coverage levels, net benefit by harm weight and fault weighting, M1 sole-stop counts |
| `03_m2_alternatives.py` | 1 | SCDI denominator | SCDI detectability per subgroup; absolute gap and one-sided complement gap with permutation thresholds |
| `04_independent_faults.py` | 1 | Faults designed around the signals | Four faults not aimed at any signal; search for errors the agent made unprompted |
| `05_revised_config.py` | 1 | – | Tune-selected revised configuration replayed on the test split |
| `06_make_tables.py` | 1 | – | LaTeX rows of Tables 9–11 from the outputs |
| `10_independent_faults_ci.py` | 2 | Independent faults with clustering | Detection compared with the stop rate of the same clean trajectories; patient-clustered bootstrap |
| `11_m3_sensitivity.py` | 2 | Basis of the harm weight and fault weights | M3 stop vs caveat over lambda and fault weights; bootstrap of the break-even lambda; random (Dirichlet) weights; caveat rate |
| `12_icu_shadow_sensitivity.py` | 2 | Shadow-period length and recalibration | `a`: shadow windows of 250 to 18,943 patients, 20 draws each (slow); `b`: M3 and M2 refitted on the shadow window |
| `99_export_results.py` | – | – | Copies the aggregate outputs to `results/revision/` after screening them |

Run order: `01` before `02`, `04`, `05` and `12` (they use its ICU shadow drift states); `03` before `04` and `05`; `02` and `04` before `10` and `11`.

## Outputs and data protection

Raw outputs go to `runs/revision/`, which git ignores. The replay rows (`*_rows.parquet`) hold patient and stay identifiers derived from credentialed data and must not be shared. `99_export_results.py` copies only aggregate files (JSON reports, per-method summaries, per-subgroup and per-draw tables, drift test statistics) to `results/revision/`. It stops if a file contains an integer of six or more digits, the form of MIMIC and eICU identifiers, or a home-folder path. The files in `results/revision/` are the results reported in the manuscript; rerunning the scripts on the same stored runs reproduces them exactly.
