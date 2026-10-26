# Quality of predictions each gate let through (ed, full)

Passed: trajectories with no interception, acted on without clinician review. Coverage: Mondrian conformal at the frozen level.

## clean trajectories

| method | passed n | ECE | Brier | AUROC | coverage | stopped n | ECE | coverage |
|---|---|---|---|---|---|---|---|---|
| no_gate | 90 | 0.209 | 0.177 | 0.853 | 0.800 | 0 | nan | nan |
| output_only | 81 | 0.174 | 0.167 | 0.833 | 0.778 | 9 | 0.521 | 1.000 |
| confidence | 72 | 0.180 | 0.156 | 0.800 | 0.792 | 18 | 0.513 | 0.833 |
| pooled_conformal | 72 | 0.180 | 0.156 | 0.800 | 0.792 | 18 | 0.513 | 0.833 |
| full | 81 | 0.174 | 0.167 | 0.833 | 0.778 | 9 | 0.521 | 1.000 |
| llm_judge | 69 | 0.235 | 0.206 | 0.778 | 0.783 | 21 | 0.175 | 0.857 |

## faulty trajectories

| method | passed n | ECE | Brier | AUROC | coverage | stopped n | ECE | coverage |
|---|---|---|---|---|---|---|---|---|
| no_gate | 444 | 0.098 | 0.199 | 0.778 | 0.727 | 0 | nan | nan |
| output_only | 280 | 0.092 | 0.219 | 0.675 | 0.661 | 164 | 0.271 | 0.841 |
| confidence | 375 | 0.080 | 0.189 | 0.777 | 0.717 | 69 | 0.389 | 0.783 |
| pooled_conformal | 350 | 0.091 | 0.185 | 0.782 | 0.729 | 94 | 0.307 | 0.723 |
| full | 184 | 0.103 | 0.233 | 0.675 | 0.609 | 260 | 0.181 | 0.812 |
| llm_judge | 238 | 0.179 | 0.184 | 0.808 | 0.782 | 206 | 0.101 | 0.665 |

## all trajectories

| method | passed n | ECE | Brier | AUROC | coverage | stopped n | ECE | coverage |
|---|---|---|---|---|---|---|---|---|
| no_gate | 534 | 0.116 | 0.196 | 0.792 | 0.740 | 0 | nan | nan |
| output_only | 361 | 0.075 | 0.207 | 0.718 | 0.687 | 173 | 0.284 | 0.850 |
| confidence | 447 | 0.095 | 0.184 | 0.785 | 0.729 | 87 | 0.415 | 0.793 |
| pooled_conformal | 422 | 0.105 | 0.180 | 0.789 | 0.739 | 112 | 0.340 | 0.741 |
| full | 265 | 0.089 | 0.213 | 0.733 | 0.660 | 269 | 0.192 | 0.818 |
| llm_judge | 307 | 0.188 | 0.189 | 0.802 | 0.782 | 227 | 0.108 | 0.683 |
