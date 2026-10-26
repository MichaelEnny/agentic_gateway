# E2/E3 replay (ed, full)

Policy: llm; clean trajectories: 1075; faulty: {'sparse': 1075, 'subgroup': 1075, 'uncertainty': 1075, 'drift': 1075, 'duplicate': 444, 'ungrounded': 444}

## clean: false_intervention

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1075 | 0.000 | 0.000 to 0.000 | -0.070 | 0.010 |
| output_only | 1075 | 0.070 | 0.044 to 0.098 | +0.000 | 1.000 |
| confidence | 1075 | 0.047 | 0.028 to 0.073 | -0.022 | 0.456 |
| pooled_conformal | 1075 | 0.073 | 0.047 to 0.101 | +0.003 | 1.000 |
| full | 1075 | 0.070 | 0.044 to 0.098 | +nan | nan |
| minus_local_calibration | 1075 | 0.070 | 0.044 to 0.098 | +0.000 | 1.000 |
| minus_subgroup_gap | 1075 | 0.070 | 0.044 to 0.098 | +0.000 | 1.000 |
| minus_conformal | 1075 | 0.003 | 0.000 to 0.008 | -0.067 | 0.010 |
| minus_drift | 1075 | 0.070 | 0.044 to 0.098 | +0.000 | 1.000 |
| minus_timing | 1075 | 0.070 | 0.044 to 0.098 | +0.000 | 1.000 |
| minus_argcheck | 1075 | 0.070 | 0.044 to 0.098 | +0.000 | 1.000 |

## drift: early

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1075 | 0.000 | 0.000 to 0.000 | -1.000 | 0.010 |
| output_only | 1075 | 0.000 | 0.000 to 0.000 | -1.000 | 0.010 |
| confidence | 1075 | 0.042 | 0.022 to 0.064 | -0.958 | 0.010 |
| pooled_conformal | 1075 | 0.070 | 0.045 to 0.098 | -0.930 | 0.010 |
| full | 1075 | 1.000 | 1.000 to 1.000 | +nan | nan |
| minus_local_calibration | 1075 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 1075 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_conformal | 1075 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_drift | 1075 | 0.061 | 0.039 to 0.087 | -0.939 | 0.010 |
| minus_timing | 1075 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_argcheck | 1075 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |

## drift: eir

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1075 | 0.000 | 0.000 to 0.000 | -1.000 | 0.010 |
| output_only | 1075 | 0.000 | 0.000 to 0.000 | -1.000 | 0.010 |
| confidence | 1075 | 0.042 | 0.022 to 0.064 | -0.958 | 0.010 |
| pooled_conformal | 1075 | 0.070 | 0.045 to 0.095 | -0.930 | 0.010 |
| full | 1075 | 1.000 | 1.000 to 1.000 | +nan | nan |
| minus_local_calibration | 1075 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 1075 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_conformal | 1075 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_drift | 1075 | 0.061 | 0.036 to 0.087 | -0.939 | 0.010 |
| minus_timing | 1075 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_argcheck | 1075 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |

## drift: intercepted

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1075 | 0.000 | 0.000 to 0.000 | -1.000 | 0.010 |
| output_only | 1075 | 0.413 | 0.363 to 0.464 | -0.587 | 0.010 |
| confidence | 1075 | 0.042 | 0.022 to 0.064 | -0.958 | 0.010 |
| pooled_conformal | 1075 | 0.070 | 0.045 to 0.098 | -0.930 | 0.010 |
| full | 1075 | 1.000 | 1.000 to 1.000 | +nan | nan |
| minus_local_calibration | 1075 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 1075 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_conformal | 1075 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_drift | 1075 | 0.061 | 0.036 to 0.089 | -0.939 | 0.010 |
| minus_timing | 1075 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_argcheck | 1075 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |

## drift: intervention_gap

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 444 | 2.000 | 2.000 to 2.000 | +2.000 | 0.009 |
| confidence | 45 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 75 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 1075 | 0.000 | 0.000 to 0.000 | +nan | nan |
| minus_local_calibration | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_conformal | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_drift | 66 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_timing | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_argcheck | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## drift: premature

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| output_only | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| confidence | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 1075 | 0.000 | 0.000 to 0.000 | +nan | nan |
| minus_local_calibration | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_conformal | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_drift | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_timing | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_argcheck | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## drift: steps_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1075 | 0.000 | 0.000 to 0.000 | -0.500 | 0.010 |
| output_only | 1075 | 0.000 | 0.000 to 0.000 | -0.500 | 0.010 |
| confidence | 1075 | 0.021 | 0.011 to 0.032 | -0.479 | 0.010 |
| pooled_conformal | 1075 | 0.035 | 0.022 to 0.049 | -0.465 | 0.010 |
| full | 1075 | 0.500 | 0.500 to 0.500 | +nan | nan |
| minus_local_calibration | 1075 | 0.500 | 0.500 to 0.500 | +0.000 | 1.000 |
| minus_subgroup_gap | 1075 | 0.500 | 0.500 to 0.500 | +0.000 | 1.000 |
| minus_conformal | 1075 | 0.500 | 0.500 to 0.500 | +0.000 | 1.000 |
| minus_drift | 1075 | 0.031 | 0.018 to 0.043 | -0.469 | 0.010 |
| minus_timing | 1075 | 0.500 | 0.500 to 0.500 | +0.000 | 1.000 |
| minus_argcheck | 1075 | 0.500 | 0.500 to 0.500 | +0.000 | 1.000 |

## drift: steps_to_intercept

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 444 | 2.000 | 2.000 to 2.000 | +2.000 | 0.009 |
| confidence | 45 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 75 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 1075 | 0.000 | 0.000 to 0.000 | +nan | nan |
| minus_local_calibration | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_conformal | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_drift | 66 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_timing | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_argcheck | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## drift: tokens_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1075 | 0.000 | 0.000 to 0.000 | -0.544 | 0.010 |
| output_only | 1075 | 0.000 | 0.000 to 0.000 | -0.544 | 0.010 |
| confidence | 1075 | 0.023 | 0.012 to 0.035 | -0.521 | 0.010 |
| pooled_conformal | 1075 | 0.038 | 0.025 to 0.052 | -0.506 | 0.010 |
| full | 1075 | 0.544 | 0.544 to 0.544 | +nan | nan |
| minus_local_calibration | 1075 | 0.544 | 0.544 to 0.544 | +0.000 | 1.000 |
| minus_subgroup_gap | 1075 | 0.544 | 0.544 to 0.544 | +0.000 | 1.000 |
| minus_conformal | 1075 | 0.544 | 0.544 to 0.544 | +0.000 | 1.000 |
| minus_drift | 1075 | 0.034 | 0.021 to 0.047 | -0.510 | 0.010 |
| minus_timing | 1075 | 0.544 | 0.544 to 0.544 | +0.000 | 1.000 |
| minus_argcheck | 1075 | 0.544 | 0.544 to 0.544 | +0.000 | 1.000 |

## duplicate: early

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 444 | 0.000 | 0.000 to 0.000 | -0.831 | 0.010 |
| output_only | 444 | 0.831 | 0.764 to 0.892 | +0.000 | 1.000 |
| confidence | 444 | 0.000 | 0.000 to 0.000 | -0.831 | 0.010 |
| pooled_conformal | 444 | 0.000 | 0.000 to 0.000 | -0.831 | 0.010 |
| full | 444 | 0.831 | 0.764 to 0.892 | +nan | nan |
| minus_local_calibration | 444 | 0.831 | 0.764 to 0.892 | +0.000 | 1.000 |
| minus_subgroup_gap | 444 | 0.831 | 0.764 to 0.892 | +0.000 | 1.000 |
| minus_conformal | 444 | 0.993 | 0.980 to 1.000 | +0.162 | 0.010 |
| minus_drift | 444 | 0.831 | 0.764 to 0.892 | +0.000 | 1.000 |
| minus_timing | 444 | 0.000 | 0.000 to 0.000 | -0.831 | 0.010 |
| minus_argcheck | 444 | 0.831 | 0.764 to 0.892 | +0.000 | 1.000 |

## duplicate: eir

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 444 | 0.000 | 0.000 to 0.000 | -1.000 | 0.010 |
| output_only | 444 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| confidence | 444 | 0.115 | 0.068 to 0.169 | -0.885 | 0.010 |
| pooled_conformal | 444 | 0.176 | 0.115 to 0.236 | -0.824 | 0.010 |
| full | 444 | 1.000 | 1.000 to 1.000 | +nan | nan |
| minus_local_calibration | 444 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 444 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_conformal | 444 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_drift | 444 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_timing | 444 | 0.169 | 0.115 to 0.230 | -0.831 | 0.010 |
| minus_argcheck | 444 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |

## duplicate: intercepted

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 444 | 0.000 | 0.000 to 0.000 | -0.831 | 0.010 |
| output_only | 444 | 0.831 | 0.777 to 0.892 | +0.000 | 1.000 |
| confidence | 444 | 0.000 | 0.000 to 0.000 | -0.831 | 0.010 |
| pooled_conformal | 444 | 0.000 | 0.000 to 0.000 | -0.831 | 0.010 |
| full | 444 | 0.831 | 0.777 to 0.892 | +nan | nan |
| minus_local_calibration | 444 | 0.831 | 0.777 to 0.892 | +0.000 | 1.000 |
| minus_subgroup_gap | 444 | 0.831 | 0.777 to 0.892 | +0.000 | 1.000 |
| minus_conformal | 444 | 0.993 | 0.980 to 1.000 | +0.162 | 0.010 |
| minus_drift | 444 | 0.831 | 0.777 to 0.892 | +0.000 | 1.000 |
| minus_timing | 444 | 0.000 | 0.000 to 0.000 | -0.831 | 0.010 |
| minus_argcheck | 444 | 0.831 | 0.777 to 0.892 | +0.000 | 1.000 |

## duplicate: intervention_gap

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 444 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| confidence | 51 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 78 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 444 | 0.000 | 0.000 to 0.000 | +nan | nan |
| minus_local_calibration | 444 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 444 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_conformal | 444 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_drift | 444 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_timing | 75 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_argcheck | 444 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## duplicate: premature

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 444 | 0.000 | 0.000 to 0.000 | -0.169 | 0.010 |
| output_only | 444 | 0.169 | 0.115 to 0.236 | +0.000 | 1.000 |
| confidence | 444 | 0.115 | 0.068 to 0.169 | -0.054 | 0.400 |
| pooled_conformal | 444 | 0.176 | 0.115 to 0.237 | +0.007 | 1.000 |
| full | 444 | 0.169 | 0.115 to 0.236 | +nan | nan |
| minus_local_calibration | 444 | 0.169 | 0.115 to 0.236 | +0.000 | 1.000 |
| minus_subgroup_gap | 444 | 0.169 | 0.115 to 0.236 | +0.000 | 1.000 |
| minus_conformal | 444 | 0.007 | 0.000 to 0.020 | -0.162 | 0.010 |
| minus_drift | 444 | 0.169 | 0.115 to 0.236 | +0.000 | 1.000 |
| minus_timing | 444 | 0.169 | 0.115 to 0.236 | +0.000 | 1.000 |
| minus_argcheck | 444 | 0.169 | 0.115 to 0.236 | +0.000 | 1.000 |

## duplicate: steps_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 444 | 0.000 | 0.000 to 0.000 | -0.101 | 0.010 |
| output_only | 444 | 0.034 | 0.022 to 0.046 | -0.068 | 0.010 |
| confidence | 444 | 0.069 | 0.036 to 0.101 | -0.032 | 0.357 |
| pooled_conformal | 444 | 0.105 | 0.069 to 0.142 | +0.004 | 1.000 |
| full | 444 | 0.101 | 0.065 to 0.138 | +nan | nan |
| minus_local_calibration | 444 | 0.101 | 0.065 to 0.138 | +0.000 | 1.000 |
| minus_subgroup_gap | 444 | 0.101 | 0.065 to 0.138 | +0.000 | 1.000 |
| minus_conformal | 444 | 0.004 | 0.000 to 0.012 | -0.097 | 0.010 |
| minus_drift | 444 | 0.101 | 0.065 to 0.138 | +0.000 | 1.000 |
| minus_timing | 444 | 0.101 | 0.065 to 0.138 | +0.000 | 1.000 |
| minus_argcheck | 444 | 0.101 | 0.065 to 0.138 | +0.000 | 1.000 |

## duplicate: steps_to_intercept

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 369 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| confidence | 0 | nan | nan to nan | +nan | nan |
| pooled_conformal | 0 | nan | nan to nan | +nan | nan |
| full | 369 | 0.000 | 0.000 to 0.000 | +nan | nan |
| minus_local_calibration | 369 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 369 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_conformal | 441 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_drift | 369 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_timing | 0 | nan | nan to nan | +nan | nan |
| minus_argcheck | 369 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## duplicate: tokens_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 444 | 0.000 | 0.000 to 0.000 | -0.110 | 0.010 |
| output_only | 444 | 0.038 | 0.024 to 0.051 | -0.072 | 0.010 |
| confidence | 444 | 0.075 | 0.044 to 0.110 | -0.035 | 0.329 |
| pooled_conformal | 444 | 0.114 | 0.079 to 0.154 | +0.004 | 1.000 |
| full | 444 | 0.110 | 0.070 to 0.149 | +nan | nan |
| minus_local_calibration | 444 | 0.110 | 0.070 to 0.149 | +0.000 | 1.000 |
| minus_subgroup_gap | 444 | 0.110 | 0.070 to 0.149 | +0.000 | 1.000 |
| minus_conformal | 444 | 0.004 | 0.000 to 0.013 | -0.105 | 0.010 |
| minus_drift | 444 | 0.110 | 0.070 to 0.149 | +0.000 | 1.000 |
| minus_timing | 444 | 0.110 | 0.070 to 0.149 | +0.000 | 1.000 |
| minus_argcheck | 444 | 0.110 | 0.070 to 0.149 | +0.000 | 1.000 |

## sparse: early

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1075 | 0.000 | 0.000 to 0.000 | -0.141 | 0.010 |
| output_only | 1075 | 0.000 | 0.000 to 0.000 | -0.141 | 0.010 |
| confidence | 1075 | 0.105 | 0.087 to 0.125 | -0.036 | 0.010 |
| pooled_conformal | 1075 | 0.182 | 0.159 to 0.207 | +0.041 | 0.010 |
| full | 1075 | 0.141 | 0.119 to 0.165 | +nan | nan |
| minus_local_calibration | 1075 | 0.141 | 0.119 to 0.165 | +0.000 | 1.000 |
| minus_subgroup_gap | 1075 | 0.141 | 0.119 to 0.165 | +0.000 | 1.000 |
| minus_conformal | 1075 | 0.000 | 0.000 to 0.000 | -0.141 | 0.010 |
| minus_drift | 1075 | 0.141 | 0.119 to 0.165 | +0.000 | 1.000 |
| minus_timing | 1075 | 0.141 | 0.119 to 0.165 | +0.000 | 1.000 |
| minus_argcheck | 1075 | 0.141 | 0.119 to 0.165 | +0.000 | 1.000 |

## sparse: eir

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1075 | 0.000 | 0.000 to 0.000 | -0.141 | 0.010 |
| output_only | 1075 | 0.000 | 0.000 to 0.000 | -0.141 | 0.010 |
| confidence | 1075 | 0.105 | 0.087 to 0.125 | -0.036 | 0.010 |
| pooled_conformal | 1075 | 0.182 | 0.159 to 0.208 | +0.041 | 0.010 |
| full | 1075 | 0.141 | 0.118 to 0.165 | +nan | nan |
| minus_local_calibration | 1075 | 0.141 | 0.118 to 0.165 | +0.000 | 1.000 |
| minus_subgroup_gap | 1075 | 0.141 | 0.118 to 0.165 | +0.000 | 1.000 |
| minus_conformal | 1075 | 0.000 | 0.000 to 0.000 | -0.141 | 0.010 |
| minus_drift | 1075 | 0.141 | 0.118 to 0.165 | +0.000 | 1.000 |
| minus_timing | 1075 | 0.141 | 0.118 to 0.165 | +0.000 | 1.000 |
| minus_argcheck | 1075 | 0.141 | 0.118 to 0.165 | +0.000 | 1.000 |

## sparse: intercepted

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1075 | 0.000 | 0.000 to 0.000 | -0.141 | 0.010 |
| output_only | 1075 | 0.073 | 0.055 to 0.091 | -0.069 | 0.010 |
| confidence | 1075 | 0.105 | 0.087 to 0.126 | -0.036 | 0.010 |
| pooled_conformal | 1075 | 0.182 | 0.159 to 0.206 | +0.041 | 0.010 |
| full | 1075 | 0.141 | 0.118 to 0.165 | +nan | nan |
| minus_local_calibration | 1075 | 0.141 | 0.118 to 0.165 | +0.000 | 1.000 |
| minus_subgroup_gap | 1075 | 0.141 | 0.118 to 0.165 | +0.000 | 1.000 |
| minus_conformal | 1075 | 0.000 | 0.000 to 0.000 | -0.141 | 0.010 |
| minus_drift | 1075 | 0.141 | 0.118 to 0.165 | +0.000 | 1.000 |
| minus_timing | 1075 | 0.141 | 0.118 to 0.165 | +0.000 | 1.000 |
| minus_argcheck | 1075 | 0.141 | 0.118 to 0.165 | +0.000 | 1.000 |

## sparse: intervention_gap

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 78 | 2.000 | 2.000 to 2.000 | +2.000 | 0.008 |
| confidence | 113 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 196 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 152 | 0.000 | 0.000 to 0.000 | +nan | nan |
| minus_local_calibration | 152 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 152 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_conformal | 0 | nan | nan to nan | +nan | nan |
| minus_drift | 152 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_timing | 152 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_argcheck | 152 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## sparse: premature

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| output_only | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| confidence | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 1075 | 0.000 | 0.000 to 0.000 | +nan | nan |
| minus_local_calibration | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_conformal | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_drift | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_timing | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_argcheck | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## sparse: steps_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1075 | 0.000 | 0.000 to 0.000 | -0.071 | 0.010 |
| output_only | 1075 | 0.000 | 0.000 to 0.000 | -0.071 | 0.010 |
| confidence | 1075 | 0.053 | 0.043 to 0.063 | -0.018 | 0.012 |
| pooled_conformal | 1075 | 0.091 | 0.079 to 0.104 | +0.020 | 0.010 |
| full | 1075 | 0.071 | 0.059 to 0.082 | +nan | nan |
| minus_local_calibration | 1075 | 0.071 | 0.059 to 0.082 | +0.000 | 1.000 |
| minus_subgroup_gap | 1075 | 0.071 | 0.059 to 0.082 | +0.000 | 1.000 |
| minus_conformal | 1075 | 0.000 | 0.000 to 0.000 | -0.071 | 0.010 |
| minus_drift | 1075 | 0.071 | 0.059 to 0.082 | +0.000 | 1.000 |
| minus_timing | 1075 | 0.071 | 0.059 to 0.082 | +0.000 | 1.000 |
| minus_argcheck | 1075 | 0.071 | 0.059 to 0.082 | +0.000 | 1.000 |

## sparse: steps_to_intercept

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 78 | 2.000 | 2.000 to 2.000 | +2.000 | 0.008 |
| confidence | 113 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 196 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 152 | 0.000 | 0.000 to 0.000 | +nan | nan |
| minus_local_calibration | 152 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 152 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_conformal | 0 | nan | nan to nan | +nan | nan |
| minus_drift | 152 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_timing | 152 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_argcheck | 152 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## sparse: tokens_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1075 | 0.000 | 0.000 to 0.000 | -0.077 | 0.010 |
| output_only | 1075 | 0.000 | 0.000 to 0.000 | -0.077 | 0.010 |
| confidence | 1075 | 0.057 | 0.047 to 0.068 | -0.020 | 0.010 |
| pooled_conformal | 1075 | 0.099 | 0.086 to 0.113 | +0.022 | 0.010 |
| full | 1075 | 0.077 | 0.065 to 0.090 | +nan | nan |
| minus_local_calibration | 1075 | 0.077 | 0.065 to 0.090 | +0.000 | 1.000 |
| minus_subgroup_gap | 1075 | 0.077 | 0.065 to 0.090 | +0.000 | 1.000 |
| minus_conformal | 1075 | 0.000 | 0.000 to 0.000 | -0.077 | 0.010 |
| minus_drift | 1075 | 0.077 | 0.065 to 0.090 | +0.000 | 1.000 |
| minus_timing | 1075 | 0.077 | 0.065 to 0.090 | +0.000 | 1.000 |
| minus_argcheck | 1075 | 0.077 | 0.065 to 0.090 | +0.000 | 1.000 |

## subgroup: early

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1075 | 0.000 | 0.000 to 0.000 | -0.852 | 0.010 |
| output_only | 1075 | 0.000 | 0.000 to 0.000 | -0.852 | 0.010 |
| confidence | 1075 | 0.119 | 0.084 to 0.155 | -0.733 | 0.010 |
| pooled_conformal | 1075 | 0.191 | 0.150 to 0.233 | -0.661 | 0.010 |
| full | 1075 | 0.852 | 0.813 to 0.889 | +nan | nan |
| minus_local_calibration | 1075 | 0.852 | 0.813 to 0.889 | +0.000 | 1.000 |
| minus_subgroup_gap | 1075 | 0.143 | 0.108 to 0.179 | -0.709 | 0.010 |
| minus_conformal | 1075 | 0.794 | 0.750 to 0.836 | -0.058 | 0.010 |
| minus_drift | 1075 | 0.852 | 0.813 to 0.889 | +0.000 | 1.000 |
| minus_timing | 1075 | 0.852 | 0.813 to 0.889 | +0.000 | 1.000 |
| minus_argcheck | 1075 | 0.852 | 0.813 to 0.889 | +0.000 | 1.000 |

## subgroup: eir

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1075 | 0.000 | 0.000 to 0.000 | -0.852 | 0.010 |
| output_only | 1075 | 0.000 | 0.000 to 0.000 | -0.852 | 0.010 |
| confidence | 1075 | 0.119 | 0.088 to 0.154 | -0.733 | 0.010 |
| pooled_conformal | 1075 | 0.191 | 0.152 to 0.232 | -0.661 | 0.010 |
| full | 1075 | 0.852 | 0.813 to 0.888 | +nan | nan |
| minus_local_calibration | 1075 | 0.852 | 0.813 to 0.888 | +0.000 | 1.000 |
| minus_subgroup_gap | 1075 | 0.143 | 0.108 to 0.180 | -0.709 | 0.010 |
| minus_conformal | 1075 | 0.794 | 0.750 to 0.836 | -0.058 | 0.010 |
| minus_drift | 1075 | 0.852 | 0.813 to 0.888 | +0.000 | 1.000 |
| minus_timing | 1075 | 0.852 | 0.813 to 0.888 | +0.000 | 1.000 |
| minus_argcheck | 1075 | 0.852 | 0.813 to 0.888 | +0.000 | 1.000 |

## subgroup: intercepted

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1075 | 0.000 | 0.000 to 0.000 | -0.852 | 0.010 |
| output_only | 1075 | 0.318 | 0.273 to 0.366 | -0.534 | 0.010 |
| confidence | 1075 | 0.119 | 0.086 to 0.151 | -0.733 | 0.010 |
| pooled_conformal | 1075 | 0.191 | 0.151 to 0.229 | -0.661 | 0.010 |
| full | 1075 | 0.852 | 0.813 to 0.886 | +nan | nan |
| minus_local_calibration | 1075 | 0.852 | 0.813 to 0.886 | +0.000 | 1.000 |
| minus_subgroup_gap | 1075 | 0.143 | 0.109 to 0.179 | -0.709 | 0.010 |
| minus_conformal | 1075 | 0.794 | 0.749 to 0.836 | -0.058 | 0.010 |
| minus_drift | 1075 | 0.852 | 0.813 to 0.886 | +0.000 | 1.000 |
| minus_timing | 1075 | 0.852 | 0.813 to 0.886 | +0.000 | 1.000 |
| minus_argcheck | 1075 | 0.852 | 0.813 to 0.886 | +0.000 | 1.000 |

## subgroup: intervention_gap

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 342 | 2.000 | 2.000 to 2.000 | +2.000 | 0.009 |
| confidence | 128 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 205 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 916 | 0.000 | 0.000 to 0.000 | +nan | nan |
| minus_local_calibration | 916 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 154 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_conformal | 854 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_drift | 916 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_timing | 916 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_argcheck | 916 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## subgroup: premature

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| output_only | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| confidence | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 1075 | 0.000 | 0.000 to 0.000 | +nan | nan |
| minus_local_calibration | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_conformal | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_drift | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_timing | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_argcheck | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## subgroup: steps_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1075 | 0.000 | 0.000 to 0.000 | -0.426 | 0.010 |
| output_only | 1075 | 0.000 | 0.000 to 0.000 | -0.426 | 0.010 |
| confidence | 1075 | 0.060 | 0.044 to 0.077 | -0.367 | 0.010 |
| pooled_conformal | 1075 | 0.095 | 0.076 to 0.115 | -0.331 | 0.010 |
| full | 1075 | 0.426 | 0.407 to 0.444 | +nan | nan |
| minus_local_calibration | 1075 | 0.426 | 0.407 to 0.444 | +0.000 | 1.000 |
| minus_subgroup_gap | 1075 | 0.072 | 0.055 to 0.091 | -0.354 | 0.010 |
| minus_conformal | 1075 | 0.397 | 0.377 to 0.417 | -0.029 | 0.010 |
| minus_drift | 1075 | 0.426 | 0.407 to 0.444 | +0.000 | 1.000 |
| minus_timing | 1075 | 0.426 | 0.407 to 0.444 | +0.000 | 1.000 |
| minus_argcheck | 1075 | 0.426 | 0.407 to 0.444 | +0.000 | 1.000 |

## subgroup: steps_to_intercept

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 342 | 2.000 | 2.000 to 2.000 | +2.000 | 0.009 |
| confidence | 128 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 205 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 916 | 0.000 | 0.000 to 0.000 | +nan | nan |
| minus_local_calibration | 916 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 154 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_conformal | 854 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_drift | 916 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_timing | 916 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_argcheck | 916 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## subgroup: tokens_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1075 | 0.000 | 0.000 to 0.000 | -0.463 | 0.010 |
| output_only | 1075 | 0.000 | 0.000 to 0.000 | -0.463 | 0.010 |
| confidence | 1075 | 0.064 | 0.048 to 0.083 | -0.399 | 0.010 |
| pooled_conformal | 1075 | 0.103 | 0.082 to 0.126 | -0.360 | 0.010 |
| full | 1075 | 0.463 | 0.443 to 0.483 | +nan | nan |
| minus_local_calibration | 1075 | 0.463 | 0.443 to 0.483 | +0.000 | 1.000 |
| minus_subgroup_gap | 1075 | 0.078 | 0.059 to 0.099 | -0.386 | 0.010 |
| minus_conformal | 1075 | 0.432 | 0.409 to 0.454 | -0.031 | 0.010 |
| minus_drift | 1075 | 0.463 | 0.443 to 0.483 | +0.000 | 1.000 |
| minus_timing | 1075 | 0.463 | 0.443 to 0.483 | +0.000 | 1.000 |
| minus_argcheck | 1075 | 0.463 | 0.443 to 0.483 | +0.000 | 1.000 |

## uncertainty: early

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1075 | 0.000 | 0.000 to 0.000 | -0.078 | 0.010 |
| output_only | 1075 | 0.000 | 0.000 to 0.000 | -0.078 | 0.010 |
| confidence | 1075 | 0.042 | 0.022 to 0.064 | -0.036 | 0.021 |
| pooled_conformal | 1075 | 0.084 | 0.056 to 0.112 | +0.006 | 1.000 |
| full | 1075 | 0.078 | 0.050 to 0.106 | +nan | nan |
| minus_local_calibration | 1075 | 0.073 | 0.047 to 0.100 | -0.006 | 1.000 |
| minus_subgroup_gap | 1075 | 0.078 | 0.050 to 0.106 | +0.000 | 1.000 |
| minus_conformal | 1075 | 0.006 | 0.000 to 0.014 | -0.073 | 0.010 |
| minus_drift | 1075 | 0.078 | 0.050 to 0.106 | +0.000 | 1.000 |
| minus_timing | 1075 | 0.078 | 0.050 to 0.106 | +0.000 | 1.000 |
| minus_argcheck | 1075 | 0.078 | 0.050 to 0.106 | +0.000 | 1.000 |

## uncertainty: eir

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1075 | 0.000 | 0.000 to 0.000 | -0.078 | 0.010 |
| output_only | 1075 | 0.000 | 0.000 to 0.000 | -0.078 | 0.010 |
| confidence | 1075 | 0.042 | 0.022 to 0.062 | -0.036 | 0.021 |
| pooled_conformal | 1075 | 0.084 | 0.056 to 0.114 | +0.006 | 1.000 |
| full | 1075 | 0.078 | 0.053 to 0.106 | +nan | nan |
| minus_local_calibration | 1075 | 0.073 | 0.047 to 0.100 | -0.006 | 1.000 |
| minus_subgroup_gap | 1075 | 0.078 | 0.053 to 0.106 | +0.000 | 1.000 |
| minus_conformal | 1075 | 0.006 | 0.000 to 0.014 | -0.073 | 0.010 |
| minus_drift | 1075 | 0.078 | 0.053 to 0.106 | +0.000 | 1.000 |
| minus_timing | 1075 | 0.078 | 0.053 to 0.106 | +0.000 | 1.000 |
| minus_argcheck | 1075 | 0.078 | 0.053 to 0.106 | +0.000 | 1.000 |

## uncertainty: intercepted

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1075 | 0.000 | 0.000 to 0.000 | -0.078 | 0.010 |
| output_only | 1075 | 0.073 | 0.047 to 0.100 | -0.006 | 1.000 |
| confidence | 1075 | 0.042 | 0.022 to 0.064 | -0.036 | 0.032 |
| pooled_conformal | 1075 | 0.084 | 0.056 to 0.114 | +0.006 | 1.000 |
| full | 1075 | 0.078 | 0.050 to 0.106 | +nan | nan |
| minus_local_calibration | 1075 | 0.073 | 0.047 to 0.100 | -0.006 | 1.000 |
| minus_subgroup_gap | 1075 | 0.078 | 0.050 to 0.106 | +0.000 | 1.000 |
| minus_conformal | 1075 | 0.006 | 0.000 to 0.014 | -0.073 | 0.010 |
| minus_drift | 1075 | 0.078 | 0.050 to 0.106 | +0.000 | 1.000 |
| minus_timing | 1075 | 0.078 | 0.050 to 0.106 | +0.000 | 1.000 |
| minus_argcheck | 1075 | 0.078 | 0.050 to 0.106 | +0.000 | 1.000 |

## uncertainty: intervention_gap

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 78 | 2.000 | 2.000 to 2.000 | +2.000 | 0.009 |
| confidence | 45 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 90 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 84 | 0.000 | 0.000 to 0.000 | +nan | nan |
| minus_local_calibration | 78 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 84 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_conformal | 6 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_drift | 84 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_timing | 84 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_argcheck | 84 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## uncertainty: premature

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| output_only | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| confidence | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 1075 | 0.000 | 0.000 to 0.000 | +nan | nan |
| minus_local_calibration | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_conformal | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_drift | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_timing | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_argcheck | 1075 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## uncertainty: steps_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1075 | 0.000 | 0.000 to 0.000 | -0.039 | 0.010 |
| output_only | 1075 | 0.000 | 0.000 to 0.000 | -0.039 | 0.010 |
| confidence | 1075 | 0.021 | 0.011 to 0.032 | -0.018 | 0.014 |
| pooled_conformal | 1075 | 0.042 | 0.028 to 0.057 | +0.003 | 1.000 |
| full | 1075 | 0.039 | 0.026 to 0.053 | +nan | nan |
| minus_local_calibration | 1075 | 0.036 | 0.024 to 0.050 | -0.003 | 1.000 |
| minus_subgroup_gap | 1075 | 0.039 | 0.026 to 0.053 | +0.000 | 1.000 |
| minus_conformal | 1075 | 0.003 | 0.000 to 0.007 | -0.036 | 0.010 |
| minus_drift | 1075 | 0.039 | 0.026 to 0.053 | +0.000 | 1.000 |
| minus_timing | 1075 | 0.039 | 0.026 to 0.053 | +0.000 | 1.000 |
| minus_argcheck | 1075 | 0.039 | 0.026 to 0.053 | +0.000 | 1.000 |

## uncertainty: steps_to_intercept

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 78 | 2.000 | 2.000 to 2.000 | +2.000 | 0.009 |
| confidence | 45 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 90 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 84 | 0.000 | 0.000 to 0.000 | +nan | nan |
| minus_local_calibration | 78 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 84 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_conformal | 6 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_drift | 84 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_timing | 84 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_argcheck | 84 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## uncertainty: tokens_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1075 | 0.000 | 0.000 to 0.000 | -0.043 | 0.010 |
| output_only | 1075 | 0.000 | 0.000 to 0.000 | -0.043 | 0.010 |
| confidence | 1075 | 0.023 | 0.012 to 0.035 | -0.020 | 0.010 |
| pooled_conformal | 1075 | 0.046 | 0.031 to 0.063 | +0.003 | 1.000 |
| full | 1075 | 0.043 | 0.029 to 0.058 | +nan | nan |
| minus_local_calibration | 1075 | 0.040 | 0.026 to 0.055 | -0.003 | 1.000 |
| minus_subgroup_gap | 1075 | 0.043 | 0.029 to 0.058 | +0.000 | 1.000 |
| minus_conformal | 1075 | 0.003 | 0.000 to 0.008 | -0.040 | 0.010 |
| minus_drift | 1075 | 0.043 | 0.029 to 0.058 | +0.000 | 1.000 |
| minus_timing | 1075 | 0.043 | 0.029 to 0.058 | +0.000 | 1.000 |
| minus_argcheck | 1075 | 0.043 | 0.029 to 0.058 | +0.000 | 1.000 |

## ungrounded: early

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 444 | 0.000 | 0.000 to 0.000 | -0.831 | 0.010 |
| output_only | 444 | 1.000 | 1.000 to 1.000 | +0.169 | 0.010 |
| confidence | 444 | 0.000 | 0.000 to 0.000 | -0.831 | 0.010 |
| pooled_conformal | 444 | 0.000 | 0.000 to 0.000 | -0.831 | 0.010 |
| full | 444 | 0.831 | 0.770 to 0.892 | +nan | nan |
| minus_local_calibration | 444 | 0.831 | 0.770 to 0.892 | +0.000 | 1.000 |
| minus_subgroup_gap | 444 | 0.831 | 0.770 to 0.892 | +0.000 | 1.000 |
| minus_conformal | 444 | 0.993 | 0.980 to 1.000 | +0.162 | 0.010 |
| minus_drift | 444 | 0.831 | 0.770 to 0.892 | +0.000 | 1.000 |
| minus_timing | 444 | 0.831 | 0.770 to 0.892 | +0.000 | 1.000 |
| minus_argcheck | 444 | 0.000 | 0.000 to 0.000 | -0.831 | 0.010 |

## ungrounded: eir

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 444 | 0.000 | 0.000 to 0.000 | -1.000 | 0.010 |
| output_only | 444 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| confidence | 444 | 0.115 | 0.068 to 0.169 | -0.885 | 0.010 |
| pooled_conformal | 444 | 0.176 | 0.115 to 0.243 | -0.824 | 0.010 |
| full | 444 | 1.000 | 1.000 to 1.000 | +nan | nan |
| minus_local_calibration | 444 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 444 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_conformal | 444 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_drift | 444 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_timing | 444 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_argcheck | 444 | 0.169 | 0.108 to 0.230 | -0.831 | 0.010 |

## ungrounded: intercepted

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 444 | 0.000 | 0.000 to 0.000 | -0.831 | 0.010 |
| output_only | 444 | 1.000 | 1.000 to 1.000 | +0.169 | 0.010 |
| confidence | 444 | 0.000 | 0.000 to 0.000 | -0.831 | 0.010 |
| pooled_conformal | 444 | 0.000 | 0.000 to 0.000 | -0.831 | 0.010 |
| full | 444 | 0.831 | 0.764 to 0.885 | +nan | nan |
| minus_local_calibration | 444 | 0.831 | 0.764 to 0.885 | +0.000 | 1.000 |
| minus_subgroup_gap | 444 | 0.831 | 0.764 to 0.885 | +0.000 | 1.000 |
| minus_conformal | 444 | 0.993 | 0.980 to 1.000 | +0.162 | 0.010 |
| minus_drift | 444 | 0.831 | 0.764 to 0.885 | +0.000 | 1.000 |
| minus_timing | 444 | 0.831 | 0.764 to 0.885 | +0.000 | 1.000 |
| minus_argcheck | 444 | 0.000 | 0.000 to 0.000 | -0.831 | 0.010 |

## ungrounded: intervention_gap

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 444 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| confidence | 51 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 78 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 444 | 0.000 | 0.000 to 0.000 | +nan | nan |
| minus_local_calibration | 444 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 444 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_conformal | 444 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_drift | 444 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_timing | 444 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_argcheck | 75 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## ungrounded: premature

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 444 | 0.000 | 0.000 to 0.000 | -0.169 | 0.010 |
| output_only | 444 | 0.000 | 0.000 to 0.000 | -0.169 | 0.010 |
| confidence | 444 | 0.115 | 0.068 to 0.169 | -0.054 | 0.280 |
| pooled_conformal | 444 | 0.176 | 0.115 to 0.243 | +0.007 | 1.000 |
| full | 444 | 0.169 | 0.115 to 0.230 | +nan | nan |
| minus_local_calibration | 444 | 0.169 | 0.115 to 0.230 | +0.000 | 1.000 |
| minus_subgroup_gap | 444 | 0.169 | 0.115 to 0.230 | +0.000 | 1.000 |
| minus_conformal | 444 | 0.007 | 0.000 to 0.020 | -0.162 | 0.010 |
| minus_drift | 444 | 0.169 | 0.115 to 0.230 | +0.000 | 1.000 |
| minus_timing | 444 | 0.169 | 0.115 to 0.230 | +0.000 | 1.000 |
| minus_argcheck | 444 | 0.169 | 0.115 to 0.230 | +0.000 | 1.000 |

## ungrounded: steps_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 444 | 0.000 | 0.000 to 0.000 | -0.084 | 0.010 |
| output_only | 444 | 0.000 | 0.000 to 0.000 | -0.084 | 0.010 |
| confidence | 444 | 0.057 | 0.034 to 0.084 | -0.027 | 0.406 |
| pooled_conformal | 444 | 0.088 | 0.061 to 0.122 | +0.003 | 1.000 |
| full | 444 | 0.084 | 0.057 to 0.118 | +nan | nan |
| minus_local_calibration | 444 | 0.084 | 0.057 to 0.118 | +0.000 | 1.000 |
| minus_subgroup_gap | 444 | 0.084 | 0.057 to 0.118 | +0.000 | 1.000 |
| minus_conformal | 444 | 0.003 | 0.000 to 0.010 | -0.081 | 0.010 |
| minus_drift | 444 | 0.084 | 0.057 to 0.118 | +0.000 | 1.000 |
| minus_timing | 444 | 0.084 | 0.057 to 0.118 | +0.000 | 1.000 |
| minus_argcheck | 444 | 0.084 | 0.057 to 0.118 | +0.000 | 1.000 |

## ungrounded: steps_to_intercept

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 444 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| confidence | 0 | nan | nan to nan | +nan | nan |
| pooled_conformal | 0 | nan | nan to nan | +nan | nan |
| full | 369 | 0.000 | 0.000 to 0.000 | +nan | nan |
| minus_local_calibration | 369 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 369 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_conformal | 441 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_drift | 369 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_timing | 369 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_argcheck | 0 | nan | nan to nan | +nan | nan |

## ungrounded: tokens_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 444 | 0.000 | 0.000 to 0.000 | -0.093 | 0.010 |
| output_only | 444 | 0.000 | 0.000 to 0.000 | -0.093 | 0.010 |
| confidence | 444 | 0.063 | 0.037 to 0.093 | -0.030 | 0.357 |
| pooled_conformal | 444 | 0.096 | 0.067 to 0.130 | +0.004 | 1.000 |
| full | 444 | 0.093 | 0.063 to 0.126 | +nan | nan |
| minus_local_calibration | 444 | 0.093 | 0.063 to 0.126 | +0.000 | 1.000 |
| minus_subgroup_gap | 444 | 0.093 | 0.063 to 0.126 | +0.000 | 1.000 |
| minus_conformal | 444 | 0.004 | 0.000 to 0.011 | -0.089 | 0.010 |
| minus_drift | 444 | 0.093 | 0.063 to 0.126 | +0.000 | 1.000 |
| minus_timing | 444 | 0.093 | 0.063 to 0.126 | +0.000 | 1.000 |
| minus_argcheck | 444 | 0.093 | 0.063 to 0.126 | +0.000 | 1.000 |
