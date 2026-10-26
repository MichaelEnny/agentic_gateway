# Quality of predictions each gate let through (icu, full)

Passed: trajectories with no interception, acted on without clinician review. Coverage: Mondrian conformal at the frozen level.

## clean trajectories

| method | passed n | ECE | Brier | AUROC | coverage | stopped n | ECE | coverage |
|---|---|---|---|---|---|---|---|---|
| no_gate | 1076 | 0.036 | 0.084 | 0.875 | 0.869 | 0 | nan | nan |
| output_only | 827 | 0.008 | 0.040 | 0.815 | 0.960 | 249 | 0.128 | 0.566 |
| confidence | 947 | 0.019 | 0.061 | 0.840 | 0.930 | 129 | 0.161 | 0.419 |
| pooled_conformal | 1010 | 0.021 | 0.071 | 0.843 | 0.899 | 66 | 0.257 | 0.409 |
| full | 0 | nan | nan | nan | nan | 1076 | 0.036 | 0.869 |
| minus_local_calibration | 0 | nan | nan | nan | nan | 1076 | 0.036 | 0.869 |
| minus_subgroup_gap | 0 | nan | nan | nan | nan | 1076 | 0.036 | 0.869 |
| minus_conformal | 0 | nan | nan | nan | nan | 1076 | 0.036 | 0.869 |
| minus_drift | 950 | 0.030 | 0.071 | 0.872 | 0.908 | 126 | 0.165 | 0.571 |
| minus_timing | 0 | nan | nan | nan | nan | 1076 | 0.036 | 0.869 |
| minus_argcheck | 0 | nan | nan | nan | nan | 1076 | 0.036 | 0.869 |

## faulty trajectories

| method | passed n | ECE | Brier | AUROC | coverage | stopped n | ECE | coverage |
|---|---|---|---|---|---|---|---|---|
| no_gate | 4802 | 0.085 | 0.129 | 0.681 | 0.736 | 0 | nan | nan |
| output_only | 3308 | 0.137 | 0.078 | 0.598 | 0.826 | 1494 | 0.107 | 0.537 |
| confidence | 2438 | 0.026 | 0.091 | 0.786 | 0.890 | 2364 | 0.157 | 0.577 |
| pooled_conformal | 3547 | 0.066 | 0.101 | 0.636 | 0.843 | 1255 | 0.143 | 0.432 |
| full | 0 | nan | nan | nan | nan | 4802 | 0.085 | 0.736 |
| minus_local_calibration | 0 | nan | nan | nan | nan | 4802 | 0.085 | 0.736 |
| minus_subgroup_gap | 0 | nan | nan | nan | nan | 4802 | 0.085 | 0.736 |
| minus_conformal | 0 | nan | nan | nan | nan | 4802 | 0.085 | 0.736 |
| minus_drift | 2621 | 0.044 | 0.090 | 0.714 | 0.900 | 2181 | 0.137 | 0.538 |
| minus_timing | 0 | nan | nan | nan | nan | 4802 | 0.085 | 0.736 |
| minus_argcheck | 0 | nan | nan | nan | nan | 4802 | 0.085 | 0.736 |

## all trajectories

| method | passed n | ECE | Brier | AUROC | coverage | stopped n | ECE | coverage |
|---|---|---|---|---|---|---|---|---|
| no_gate | 5878 | 0.068 | 0.121 | 0.713 | 0.760 | 0 | nan | nan |
| output_only | 4135 | 0.111 | 0.070 | 0.623 | 0.852 | 1743 | 0.102 | 0.541 |
| confidence | 3385 | 0.024 | 0.083 | 0.803 | 0.901 | 2493 | 0.141 | 0.568 |
| pooled_conformal | 4557 | 0.053 | 0.094 | 0.682 | 0.856 | 1321 | 0.123 | 0.431 |
| full | 0 | nan | nan | nan | nan | 5878 | 0.068 | 0.760 |
| minus_local_calibration | 0 | nan | nan | nan | nan | 5878 | 0.068 | 0.760 |
| minus_subgroup_gap | 0 | nan | nan | nan | nan | 5878 | 0.068 | 0.760 |
| minus_conformal | 0 | nan | nan | nan | nan | 5878 | 0.068 | 0.760 |
| minus_drift | 3571 | 0.033 | 0.084 | 0.756 | 0.902 | 2307 | 0.124 | 0.540 |
| minus_timing | 0 | nan | nan | nan | nan | 5878 | 0.068 | 0.760 |
| minus_argcheck | 0 | nan | nan | nan | nan | 5878 | 0.068 | 0.760 |
