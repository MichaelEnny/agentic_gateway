# Quality of predictions each gate let through (icu, full)

Passed: trajectories with no interception, acted on without clinician review. Coverage: Mondrian conformal at the frozen level.

## clean trajectories

| method | passed n | ECE | Brier | AUROC | coverage | stopped n | ECE | coverage |
|---|---|---|---|---|---|---|---|---|
| no_gate | 90 | 0.095 | 0.041 | 0.964 | 0.933 | 0 | nan | nan |
| output_only | 69 | 0.052 | 0.004 | nan | 1.000 | 21 | 0.234 | 0.714 |
| confidence | 81 | 0.071 | 0.008 | nan | 1.000 | 9 | 0.308 | 0.333 |
| pooled_conformal | 81 | 0.071 | 0.008 | nan | 1.000 | 9 | 0.308 | 0.333 |
| full | 0 | nan | nan | nan | nan | 90 | 0.095 | 0.933 |
| llm_judge | 81 | 0.079 | 0.029 | 0.962 | 0.963 | 9 | 0.237 | 0.667 |

## faulty trajectories

| method | passed n | ECE | Brier | AUROC | coverage | stopped n | ECE | coverage |
|---|---|---|---|---|---|---|---|---|
| no_gate | 402 | 0.129 | 0.094 | 0.770 | 0.776 | 0 | nan | nan |
| output_only | 276 | 0.178 | 0.050 | nan | 0.837 | 126 | 0.122 | 0.643 |
| confidence | 209 | 0.061 | 0.034 | 0.856 | 0.967 | 193 | 0.202 | 0.570 |
| pooled_conformal | 288 | 0.103 | 0.053 | 0.752 | 0.910 | 114 | 0.194 | 0.439 |
| full | 0 | nan | nan | nan | nan | 402 | 0.129 | 0.776 |
| llm_judge | 335 | 0.148 | 0.079 | 0.746 | 0.824 | 67 | 0.093 | 0.537 |

## all trajectories

| method | passed n | ECE | Brier | AUROC | coverage | stopped n | ECE | coverage |
|---|---|---|---|---|---|---|---|---|
| no_gate | 492 | 0.111 | 0.084 | 0.810 | 0.805 | 0 | nan | nan |
| output_only | 345 | 0.152 | 0.041 | nan | 0.870 | 147 | 0.130 | 0.653 |
| confidence | 290 | 0.064 | 0.027 | 0.875 | 0.976 | 202 | 0.179 | 0.559 |
| pooled_conformal | 369 | 0.096 | 0.043 | 0.798 | 0.930 | 123 | 0.157 | 0.431 |
| full | 0 | nan | nan | nan | nan | 492 | 0.111 | 0.805 |
| llm_judge | 416 | 0.131 | 0.069 | 0.798 | 0.851 | 76 | 0.106 | 0.553 |
