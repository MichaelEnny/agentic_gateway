# E1: gateway on static test predictions (icu, full)

## logistic_regression

n = 38258

| outcome | share |
|---|---|
| defer | 1.000 |

| set | n | ECE | Brier | AUROC |
|---|---|---|---|---|
| allowed | 0 | nan | nan | nan |
| stopped | 38258 | 0.016 | 0.078 | 0.817 |

Share of conformal sets with both labels (M3 cannot decide) or none, by coverage level

| coverage | Mondrian two-label | Mondrian empty | pooled two-label | pooled empty |
|---|---|---|---|---|
| 0.80 | 0.000 | 0.167 | 0.000 | 0.167 |
| 0.85 | 0.000 | 0.106 | 0.000 | 0.106 |
| 0.90 | 0.002 | 0.035 | 0.000 | 0.035 |
| 0.95 | 0.115 | 0.001 | 0.105 | 0.000 |

Conformal coverage, target 0.90

| group | n | Mondrian | pooled |
|---|---|---|---|
| Asian|Female | 195 | 0.897 | 0.882 |
| Asian|Male | 228 | 0.833 | 0.851 |
| Black|Female | 2362 | 0.822 | 0.870 |
| Black|Male | 2688 | 0.878 | 0.878 |
| Hispanic|Female | 507 | 0.919 | 0.866 |
| Hispanic|Male | 641 | 0.856 | 0.867 |
| Other|Female | 117 | 0.949 | 0.863 |
| Other|Male | 104 | 0.875 | 0.827 |
| White|Female | 13478 | 0.888 | 0.879 |
| White|Male | 16418 | 0.881 | 0.886 |
| __unknown__ | 1520 | 0.895 | 0.874 |
| _all | 38258 | 0.880 | 0.880 |

Signals that stopped a prediction (one prediction can have several): {'subgroup_gap': 37396, 'drift': 38258, 'local_calibration': 2681, 'conformal': 1407}

Caveat-only signals (near the threshold, or subgroup not assessable), counted over all predictions: {'local_calibration': 1585, 'subgroup_gap': 862}

## random_forest

n = 38258

| outcome | share |
|---|---|
| defer | 1.000 |

| set | n | ECE | Brier | AUROC |
|---|---|---|---|---|
| allowed | 0 | nan | nan | nan |
| stopped | 38258 | 0.017 | 0.079 | 0.821 |

Share of conformal sets with both labels (M3 cannot decide) or none, by coverage level

| coverage | Mondrian two-label | Mondrian empty | pooled two-label | pooled empty |
|---|---|---|---|---|
| 0.80 | 0.000 | 0.167 | 0.000 | 0.164 |
| 0.85 | 0.000 | 0.109 | 0.000 | 0.106 |
| 0.90 | 0.002 | 0.036 | 0.000 | 0.039 |
| 0.95 | 0.112 | 0.003 | 0.104 | 0.000 |

Conformal coverage, target 0.90

| group | n | Mondrian | pooled |
|---|---|---|---|
| Asian|Female | 195 | 0.908 | 0.867 |
| Asian|Male | 228 | 0.820 | 0.842 |
| Black|Female | 2362 | 0.831 | 0.868 |
| Black|Male | 2688 | 0.875 | 0.875 |
| Hispanic|Female | 507 | 0.909 | 0.860 |
| Hispanic|Male | 641 | 0.850 | 0.856 |
| Other|Female | 117 | 0.957 | 0.846 |
| Other|Male | 104 | 0.904 | 0.788 |
| White|Female | 13478 | 0.889 | 0.879 |
| White|Male | 16418 | 0.880 | 0.883 |
| __unknown__ | 1520 | 0.881 | 0.866 |
| _all | 38258 | 0.880 | 0.878 |

Signals that stopped a prediction (one prediction can have several): {'drift': 38258, 'conformal': 1462, 'local_calibration': 879}

Caveat-only signals (near the threshold, or subgroup not assessable), counted over all predictions: {'subgroup_gap': 34520, 'local_calibration': 466}
