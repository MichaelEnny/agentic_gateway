# Quality of predictions each gate let through (ed, full)

Passed: trajectories with no interception, acted on without clinician review. Coverage: Mondrian conformal at the frozen level.

## clean trajectories

| method | passed n | ECE | Brier | AUROC | coverage | stopped n | ECE | coverage |
|---|---|---|---|---|---|---|---|---|
| no_gate | 1075 | 0.051 | 0.140 | 0.853 | 0.846 | 0 | nan | nan |
| output_only | 1000 | 0.050 | 0.131 | 0.849 | 0.840 | 75 | 0.191 | 0.920 |
| confidence | 1024 | 0.041 | 0.134 | 0.848 | 0.844 | 51 | 0.272 | 0.882 |
| pooled_conformal | 997 | 0.039 | 0.131 | 0.846 | 0.843 | 78 | 0.241 | 0.885 |
| full | 1000 | 0.050 | 0.131 | 0.849 | 0.840 | 75 | 0.191 | 0.920 |
| minus_local_calibration | 1000 | 0.050 | 0.131 | 0.849 | 0.840 | 75 | 0.191 | 0.920 |
| minus_subgroup_gap | 1000 | 0.050 | 0.131 | 0.849 | 0.840 | 75 | 0.191 | 0.920 |
| minus_conformal | 1072 | 0.052 | 0.139 | 0.854 | 0.845 | 3 | 0.443 | 1.000 |
| minus_drift | 1000 | 0.050 | 0.131 | 0.849 | 0.840 | 75 | 0.191 | 0.920 |
| minus_timing | 1000 | 0.050 | 0.131 | 0.849 | 0.840 | 75 | 0.191 | 0.920 |
| minus_argcheck | 1000 | 0.050 | 0.131 | 0.849 | 0.840 | 75 | 0.191 | 0.920 |

## faulty trajectories

| method | passed n | ECE | Brier | AUROC | coverage | stopped n | ECE | coverage |
|---|---|---|---|---|---|---|---|---|
| no_gate | 5188 | 0.060 | 0.188 | 0.772 | 0.755 | 0 | nan | nan |
| output_only | 3358 | 0.112 | 0.181 | 0.706 | 0.756 | 1830 | 0.059 | 0.752 |
| confidence | 4755 | 0.062 | 0.182 | 0.782 | 0.758 | 433 | 0.033 | 0.723 |
| pooled_conformal | 4466 | 0.064 | 0.178 | 0.788 | 0.759 | 722 | 0.031 | 0.733 |
| full | 2073 | 0.081 | 0.200 | 0.724 | 0.697 | 3115 | 0.061 | 0.794 |
| minus_local_calibration | 2079 | 0.080 | 0.200 | 0.723 | 0.696 | 3109 | 0.061 | 0.794 |
| minus_subgroup_gap | 2835 | 0.122 | 0.196 | 0.746 | 0.715 | 2353 | 0.038 | 0.803 |
| minus_conformal | 2365 | 0.079 | 0.207 | 0.709 | 0.710 | 2823 | 0.065 | 0.793 |
| minus_drift | 3082 | 0.049 | 0.179 | 0.765 | 0.737 | 2106 | 0.084 | 0.782 |
| minus_timing | 2442 | 0.062 | 0.196 | 0.750 | 0.710 | 2746 | 0.068 | 0.795 |
| minus_argcheck | 2442 | 0.062 | 0.196 | 0.750 | 0.710 | 2746 | 0.068 | 0.795 |

## all trajectories

| method | passed n | ECE | Brier | AUROC | coverage | stopped n | ECE | coverage |
|---|---|---|---|---|---|---|---|---|
| no_gate | 6263 | 0.047 | 0.179 | 0.787 | 0.771 | 0 | nan | nan |
| output_only | 4358 | 0.086 | 0.170 | 0.743 | 0.776 | 1905 | 0.064 | 0.759 |
| confidence | 5779 | 0.051 | 0.173 | 0.795 | 0.773 | 484 | 0.026 | 0.740 |
| pooled_conformal | 5463 | 0.053 | 0.169 | 0.800 | 0.774 | 800 | 0.034 | 0.748 |
| full | 3073 | 0.054 | 0.178 | 0.768 | 0.744 | 3190 | 0.055 | 0.797 |
| minus_local_calibration | 3079 | 0.054 | 0.178 | 0.767 | 0.743 | 3184 | 0.055 | 0.797 |
| minus_subgroup_gap | 3835 | 0.090 | 0.179 | 0.771 | 0.748 | 2428 | 0.036 | 0.806 |
| minus_conformal | 3437 | 0.050 | 0.186 | 0.758 | 0.752 | 2826 | 0.065 | 0.793 |
| minus_drift | 4082 | 0.037 | 0.167 | 0.788 | 0.762 | 2181 | 0.075 | 0.787 |
| minus_timing | 3442 | 0.043 | 0.177 | 0.783 | 0.748 | 2821 | 0.061 | 0.799 |
| minus_argcheck | 3442 | 0.043 | 0.177 | 0.783 | 0.748 | 2821 | 0.061 | 0.799 |
