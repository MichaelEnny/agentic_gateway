# E1: gateway on static test predictions (ed, full)

## logistic_regression

n = 74265

| outcome | share |
|---|---|
| defer | 1.000 |

| set | n | ECE | Brier | AUROC |
|---|---|---|---|---|
| allowed | 0 | nan | nan | nan |
| stopped | 74265 | 0.038 | 0.165 | 0.828 |

Share of conformal sets with both labels (M3 cannot decide) or none, by coverage level

| coverage | Mondrian two-label | Mondrian empty | pooled two-label | pooled empty |
|---|---|---|---|---|
| 0.80 | 0.122 | 0.005 | 0.120 | 0.000 |
| 0.85 | 0.229 | 0.002 | 0.232 | 0.000 |
| 0.90 | 0.355 | 0.000 | 0.360 | 0.000 |
| 0.95 | 0.527 | 0.000 | 0.535 | 0.000 |

Conformal coverage, target 0.80

| group | n | Mondrian | pooled |
|---|---|---|---|
| Asian|F | 2542 | 0.831 | 0.845 |
| Asian|M | 2293 | 0.777 | 0.816 |
| Black|F | 6064 | 0.818 | 0.843 |
| Black|M | 5115 | 0.832 | 0.821 |
| Hispanic|F | 2459 | 0.803 | 0.848 |
| Hispanic|M | 2018 | 0.831 | 0.833 |
| Other|F | 2920 | 0.786 | 0.827 |
| Other|M | 2564 | 0.780 | 0.821 |
| White|F | 23402 | 0.811 | 0.802 |
| White|M | 22335 | 0.810 | 0.788 |
| __unknown__ | 2553 | 0.769 | 0.910 |
| _all | 74265 | 0.809 | 0.812 |

Signals that stopped a prediction (one prediction can have several): {'subgroup_gap': 74265, 'conformal': 9425, 'local_calibration': 680}

Caveat-only signals (near the threshold, or subgroup not assessable), counted over all predictions: {'drift': 74265, 'local_calibration': 1468}

## random_forest

n = 74265

| outcome | share |
|---|---|
| caveat | 0.879 |
| defer | 0.121 |

| set | n | ECE | Brier | AUROC |
|---|---|---|---|---|
| allowed | 65263 | 0.032 | 0.150 | 0.848 |
| stopped | 9002 | 0.078 | 0.248 | 0.563 |

Share of conformal sets with both labels (M3 cannot decide) or none, by coverage level

| coverage | Mondrian two-label | Mondrian empty | pooled two-label | pooled empty |
|---|---|---|---|---|
| 0.80 | 0.114 | 0.007 | 0.109 | 0.000 |
| 0.85 | 0.219 | 0.002 | 0.217 | 0.000 |
| 0.90 | 0.342 | 0.000 | 0.343 | 0.000 |
| 0.95 | 0.514 | 0.000 | 0.515 | 0.000 |

Conformal coverage, target 0.80

| group | n | Mondrian | pooled |
|---|---|---|---|
| Asian|F | 2542 | 0.826 | 0.844 |
| Asian|M | 2293 | 0.769 | 0.815 |
| Black|F | 6064 | 0.821 | 0.844 |
| Black|M | 5115 | 0.833 | 0.824 |
| Hispanic|F | 2459 | 0.803 | 0.845 |
| Hispanic|M | 2018 | 0.848 | 0.838 |
| Other|F | 2920 | 0.793 | 0.827 |
| Other|M | 2564 | 0.766 | 0.826 |
| White|F | 23402 | 0.809 | 0.801 |
| White|M | 22335 | 0.812 | 0.788 |
| __unknown__ | 2553 | 0.798 | 0.915 |
| _all | 74265 | 0.810 | 0.812 |

Signals that stopped a prediction (one prediction can have several): {'conformal': 8945, 'local_calibration': 80}

Caveat-only signals (near the threshold, or subgroup not assessable), counted over all predictions: {'drift': 74265, 'local_calibration': 281}
