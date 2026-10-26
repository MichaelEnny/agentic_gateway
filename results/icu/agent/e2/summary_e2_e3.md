# E2/E3 replay (icu, full)

Policy: llm; clean trajectories: 1076; faulty: {'sparse': 1076, 'subgroup': 1076, 'uncertainty': 1076, 'drift': 1076, 'duplicate': 249, 'ungrounded': 249}

## clean: false_intervention

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1076 | 0.000 | 0.000 to 0.000 | -1.000 | 0.010 |
| output_only | 1076 | 0.231 | 0.189 to 0.276 | -0.769 | 0.010 |
| confidence | 1076 | 0.120 | 0.086 to 0.156 | -0.880 | 0.010 |
| pooled_conformal | 1076 | 0.061 | 0.039 to 0.089 | -0.939 | 0.010 |
| full | 1076 | 1.000 | 1.000 to 1.000 | +nan | nan |
| minus_local_calibration | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_conformal | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_drift | 1076 | 0.117 | 0.086 to 0.153 | -0.883 | 0.010 |
| minus_timing | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_argcheck | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |

## drift: early

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1076 | 0.000 | 0.000 to 0.000 | -1.000 | 0.010 |
| output_only | 1076 | 0.000 | 0.000 to 0.000 | -1.000 | 0.010 |
| confidence | 1076 | 0.112 | 0.081 to 0.145 | -0.888 | 0.010 |
| pooled_conformal | 1076 | 0.059 | 0.036 to 0.084 | -0.941 | 0.010 |
| full | 1076 | 1.000 | 1.000 to 1.000 | +nan | nan |
| minus_local_calibration | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_conformal | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_drift | 1076 | 0.103 | 0.072 to 0.136 | -0.897 | 0.010 |
| minus_timing | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_argcheck | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |

## drift: eir

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1076 | 0.000 | 0.000 to 0.000 | -1.000 | 0.010 |
| output_only | 1076 | 0.000 | 0.000 to 0.000 | -1.000 | 0.010 |
| confidence | 1076 | 0.112 | 0.078 to 0.148 | -0.888 | 0.010 |
| pooled_conformal | 1076 | 0.059 | 0.036 to 0.084 | -0.941 | 0.010 |
| full | 1076 | 1.000 | 1.000 to 1.000 | +nan | nan |
| minus_local_calibration | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_conformal | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_drift | 1076 | 0.103 | 0.072 to 0.136 | -0.897 | 0.010 |
| minus_timing | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_argcheck | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |

## drift: intercepted

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1076 | 0.000 | 0.000 to 0.000 | -1.000 | 0.010 |
| output_only | 1076 | 0.231 | 0.188 to 0.276 | -0.769 | 0.010 |
| confidence | 1076 | 0.112 | 0.081 to 0.145 | -0.888 | 0.010 |
| pooled_conformal | 1076 | 0.059 | 0.036 to 0.084 | -0.941 | 0.010 |
| full | 1076 | 1.000 | 1.000 to 1.000 | +nan | nan |
| minus_local_calibration | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_conformal | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_drift | 1076 | 0.103 | 0.072 to 0.136 | -0.897 | 0.010 |
| minus_timing | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_argcheck | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |

## drift: intervention_gap

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 249 | 2.000 | 2.000 to 2.000 | +2.000 | 0.009 |
| confidence | 120 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 63 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 1076 | 0.000 | 0.000 to 0.000 | +nan | nan |
| minus_local_calibration | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_conformal | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_drift | 111 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_timing | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_argcheck | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## drift: premature

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| output_only | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| confidence | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 1076 | 0.000 | 0.000 to 0.000 | +nan | nan |
| minus_local_calibration | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_conformal | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_drift | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_timing | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_argcheck | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## drift: steps_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1076 | 0.000 | 0.000 to 0.000 | -0.500 | 0.010 |
| output_only | 1076 | 0.000 | 0.000 to 0.000 | -0.500 | 0.010 |
| confidence | 1076 | 0.056 | 0.040 to 0.072 | -0.444 | 0.010 |
| pooled_conformal | 1076 | 0.029 | 0.018 to 0.042 | -0.471 | 0.010 |
| full | 1076 | 0.500 | 0.500 to 0.500 | +nan | nan |
| minus_local_calibration | 1076 | 0.500 | 0.500 to 0.500 | +0.000 | 1.000 |
| minus_subgroup_gap | 1076 | 0.500 | 0.500 to 0.500 | +0.000 | 1.000 |
| minus_conformal | 1076 | 0.500 | 0.500 to 0.500 | +0.000 | 1.000 |
| minus_drift | 1076 | 0.052 | 0.036 to 0.067 | -0.448 | 0.010 |
| minus_timing | 1076 | 0.500 | 0.500 to 0.500 | +0.000 | 1.000 |
| minus_argcheck | 1076 | 0.500 | 0.500 to 0.500 | +0.000 | 1.000 |

## drift: steps_to_intercept

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 249 | 2.000 | 2.000 to 2.000 | +2.000 | 0.009 |
| confidence | 120 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 63 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 1076 | 0.000 | 0.000 to 0.000 | +nan | nan |
| minus_local_calibration | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_conformal | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_drift | 111 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_timing | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_argcheck | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## drift: tokens_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1076 | 0.000 | 0.000 to 0.000 | -0.549 | 0.010 |
| output_only | 1076 | 0.000 | 0.000 to 0.000 | -0.549 | 0.010 |
| confidence | 1076 | 0.062 | 0.045 to 0.081 | -0.487 | 0.010 |
| pooled_conformal | 1076 | 0.033 | 0.020 to 0.048 | -0.516 | 0.010 |
| full | 1076 | 0.549 | 0.549 to 0.549 | +nan | nan |
| minus_local_calibration | 1076 | 0.549 | 0.549 to 0.549 | +0.000 | 1.000 |
| minus_subgroup_gap | 1076 | 0.549 | 0.549 to 0.549 | +0.000 | 1.000 |
| minus_conformal | 1076 | 0.549 | 0.549 to 0.549 | +0.000 | 1.000 |
| minus_drift | 1076 | 0.057 | 0.040 to 0.076 | -0.492 | 0.010 |
| minus_timing | 1076 | 0.549 | 0.549 to 0.549 | +0.000 | 1.000 |
| minus_argcheck | 1076 | 0.549 | 0.549 to 0.549 | +0.000 | 1.000 |

## duplicate: early

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| output_only | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| confidence | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 249 | 0.000 | 0.000 to 0.000 | +nan | nan |
| minus_local_calibration | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_conformal | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_drift | 249 | 0.602 | 0.506 to 0.711 | +0.602 | 0.010 |
| minus_timing | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_argcheck | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## duplicate: eir

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 249 | 0.000 | 0.000 to 0.000 | -1.000 | 0.010 |
| output_only | 249 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| confidence | 249 | 0.518 | 0.410 to 0.627 | -0.482 | 0.010 |
| pooled_conformal | 249 | 0.265 | 0.181 to 0.361 | -0.735 | 0.010 |
| full | 249 | 1.000 | 1.000 to 1.000 | +nan | nan |
| minus_local_calibration | 249 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 249 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_conformal | 249 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_drift | 249 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_timing | 249 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_argcheck | 249 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |

## duplicate: intercepted

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| output_only | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| confidence | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 249 | 0.000 | 0.000 to 0.000 | +nan | nan |
| minus_local_calibration | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_conformal | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_drift | 249 | 0.602 | 0.494 to 0.711 | +0.602 | 0.010 |
| minus_timing | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_argcheck | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## duplicate: intervention_gap

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| confidence | 129 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 66 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 249 | 0.000 | 0.000 to 0.000 | +nan | nan |
| minus_local_calibration | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_conformal | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_drift | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_timing | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_argcheck | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## duplicate: premature

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 249 | 0.000 | 0.000 to 0.000 | -1.000 | 0.010 |
| output_only | 249 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| confidence | 249 | 0.518 | 0.410 to 0.627 | -0.482 | 0.010 |
| pooled_conformal | 249 | 0.265 | 0.169 to 0.361 | -0.735 | 0.010 |
| full | 249 | 1.000 | 1.000 to 1.000 | +nan | nan |
| minus_local_calibration | 249 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 249 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_conformal | 249 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_drift | 249 | 0.398 | 0.289 to 0.494 | -0.602 | 0.010 |
| minus_timing | 249 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_argcheck | 249 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |

## duplicate: steps_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 249 | 0.000 | 0.000 to 0.000 | -0.600 | 0.010 |
| output_only | 249 | 0.200 | 0.200 to 0.200 | -0.400 | 0.010 |
| confidence | 249 | 0.311 | 0.246 to 0.376 | -0.289 | 0.010 |
| pooled_conformal | 249 | 0.159 | 0.108 to 0.217 | -0.441 | 0.010 |
| full | 249 | 0.600 | 0.600 to 0.600 | +nan | nan |
| minus_local_calibration | 249 | 0.600 | 0.600 to 0.600 | +0.000 | 1.000 |
| minus_subgroup_gap | 249 | 0.600 | 0.600 to 0.600 | +0.000 | 1.000 |
| minus_conformal | 249 | 0.600 | 0.600 to 0.600 | +0.000 | 1.000 |
| minus_drift | 249 | 0.229 | 0.169 to 0.292 | -0.371 | 0.010 |
| minus_timing | 249 | 0.600 | 0.600 to 0.600 | +0.000 | 1.000 |
| minus_argcheck | 249 | 0.600 | 0.600 to 0.600 | +0.000 | 1.000 |

## duplicate: steps_to_intercept

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 0 | nan | nan to nan | +nan | nan |
| confidence | 0 | nan | nan to nan | +nan | nan |
| pooled_conformal | 0 | nan | nan to nan | +nan | nan |
| full | 0 | nan | nan to nan | +nan | nan |
| minus_local_calibration | 0 | nan | nan to nan | +nan | nan |
| minus_subgroup_gap | 0 | nan | nan to nan | +nan | nan |
| minus_conformal | 0 | nan | nan to nan | +nan | nan |
| minus_drift | 150 | 0.000 | 0.000 to 0.000 | +nan | nan |
| minus_timing | 0 | nan | nan to nan | +nan | nan |
| minus_argcheck | 0 | nan | nan to nan | +nan | nan |

## duplicate: tokens_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 249 | 0.000 | 0.000 to 0.000 | -0.656 | 0.010 |
| output_only | 249 | 0.226 | 0.226 to 0.226 | -0.430 | 0.010 |
| confidence | 249 | 0.340 | 0.269 to 0.411 | -0.316 | 0.010 |
| pooled_conformal | 249 | 0.174 | 0.119 to 0.237 | -0.482 | 0.010 |
| full | 249 | 0.656 | 0.656 to 0.656 | +nan | nan |
| minus_local_calibration | 249 | 0.656 | 0.656 to 0.656 | +0.000 | 1.000 |
| minus_subgroup_gap | 249 | 0.656 | 0.656 to 0.656 | +0.000 | 1.000 |
| minus_conformal | 249 | 0.656 | 0.656 to 0.656 | +0.000 | 1.000 |
| minus_drift | 249 | 0.251 | 0.182 to 0.319 | -0.405 | 0.010 |
| minus_timing | 249 | 0.656 | 0.656 to 0.656 | +0.000 | 1.000 |
| minus_argcheck | 249 | 0.656 | 0.656 to 0.656 | +0.000 | 1.000 |

## sparse: early

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1076 | 0.000 | 0.000 to 0.000 | -1.000 | 0.010 |
| output_only | 1076 | 0.000 | 0.000 to 0.000 | -1.000 | 0.010 |
| confidence | 1076 | 0.809 | 0.783 to 0.835 | -0.191 | 0.010 |
| pooled_conformal | 1076 | 0.520 | 0.490 to 0.552 | -0.480 | 0.010 |
| full | 1076 | 1.000 | 1.000 to 1.000 | +nan | nan |
| minus_local_calibration | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_conformal | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_drift | 1076 | 0.570 | 0.534 to 0.606 | -0.430 | 0.010 |
| minus_timing | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_argcheck | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |

## sparse: eir

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1076 | 0.000 | 0.000 to 0.000 | -1.000 | 0.010 |
| output_only | 1076 | 0.000 | 0.000 to 0.000 | -1.000 | 0.010 |
| confidence | 1076 | 0.809 | 0.782 to 0.835 | -0.191 | 0.010 |
| pooled_conformal | 1076 | 0.520 | 0.492 to 0.552 | -0.480 | 0.010 |
| full | 1076 | 1.000 | 1.000 to 1.000 | +nan | nan |
| minus_local_calibration | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_conformal | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_drift | 1076 | 0.570 | 0.535 to 0.607 | -0.430 | 0.010 |
| minus_timing | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_argcheck | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |

## sparse: intercepted

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1076 | 0.000 | 0.000 to 0.000 | -1.000 | 0.010 |
| output_only | 1076 | 0.231 | 0.189 to 0.277 | -0.769 | 0.010 |
| confidence | 1076 | 0.809 | 0.784 to 0.835 | -0.191 | 0.010 |
| pooled_conformal | 1076 | 0.520 | 0.491 to 0.552 | -0.480 | 0.010 |
| full | 1076 | 1.000 | 1.000 to 1.000 | +nan | nan |
| minus_local_calibration | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_conformal | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_drift | 1076 | 0.570 | 0.532 to 0.606 | -0.430 | 0.010 |
| minus_timing | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_argcheck | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |

## sparse: intervention_gap

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 249 | 2.000 | 2.000 to 2.000 | +2.000 | 0.009 |
| confidence | 871 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 560 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 1076 | 0.000 | 0.000 to 0.000 | +nan | nan |
| minus_local_calibration | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_conformal | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_drift | 613 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_timing | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_argcheck | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## sparse: premature

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| output_only | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| confidence | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 1076 | 0.000 | 0.000 to 0.000 | +nan | nan |
| minus_local_calibration | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_conformal | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_drift | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_timing | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_argcheck | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## sparse: steps_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1076 | 0.000 | 0.000 to 0.000 | -0.500 | 0.010 |
| output_only | 1076 | 0.000 | 0.000 to 0.000 | -0.500 | 0.010 |
| confidence | 1076 | 0.405 | 0.392 to 0.418 | -0.095 | 0.010 |
| pooled_conformal | 1076 | 0.260 | 0.245 to 0.275 | -0.240 | 0.010 |
| full | 1076 | 0.500 | 0.500 to 0.500 | +nan | nan |
| minus_local_calibration | 1076 | 0.500 | 0.500 to 0.500 | +0.000 | 1.000 |
| minus_subgroup_gap | 1076 | 0.500 | 0.500 to 0.500 | +0.000 | 1.000 |
| minus_conformal | 1076 | 0.500 | 0.500 to 0.500 | +0.000 | 1.000 |
| minus_drift | 1076 | 0.285 | 0.266 to 0.303 | -0.215 | 0.010 |
| minus_timing | 1076 | 0.500 | 0.500 to 0.500 | +0.000 | 1.000 |
| minus_argcheck | 1076 | 0.500 | 0.500 to 0.500 | +0.000 | 1.000 |

## sparse: steps_to_intercept

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 249 | 2.000 | 2.000 to 2.000 | +2.000 | 0.009 |
| confidence | 871 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 560 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 1076 | 0.000 | 0.000 to 0.000 | +nan | nan |
| minus_local_calibration | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_conformal | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_drift | 613 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_timing | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_argcheck | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## sparse: tokens_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1076 | 0.000 | 0.000 to 0.000 | -0.549 | 0.010 |
| output_only | 1076 | 0.000 | 0.000 to 0.000 | -0.549 | 0.010 |
| confidence | 1076 | 0.444 | 0.430 to 0.458 | -0.104 | 0.010 |
| pooled_conformal | 1076 | 0.286 | 0.269 to 0.303 | -0.263 | 0.010 |
| full | 1076 | 0.549 | 0.548 to 0.549 | +nan | nan |
| minus_local_calibration | 1076 | 0.549 | 0.548 to 0.549 | +0.000 | 1.000 |
| minus_subgroup_gap | 1076 | 0.549 | 0.548 to 0.549 | +0.000 | 1.000 |
| minus_conformal | 1076 | 0.549 | 0.548 to 0.549 | +0.000 | 1.000 |
| minus_drift | 1076 | 0.313 | 0.293 to 0.333 | -0.236 | 0.010 |
| minus_timing | 1076 | 0.549 | 0.548 to 0.549 | +0.000 | 1.000 |
| minus_argcheck | 1076 | 0.549 | 0.548 to 0.549 | +0.000 | 1.000 |

## subgroup: early

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1076 | 0.000 | 0.000 to 0.000 | -1.000 | 0.010 |
| output_only | 1076 | 0.000 | 0.000 to 0.000 | -1.000 | 0.010 |
| confidence | 1076 | 0.997 | 0.992 to 1.000 | -0.003 | 1.000 |
| pooled_conformal | 1076 | 0.454 | 0.404 to 0.505 | -0.546 | 0.010 |
| full | 1076 | 1.000 | 1.000 to 1.000 | +nan | nan |
| minus_local_calibration | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_conformal | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_drift | 1076 | 0.844 | 0.807 to 0.880 | -0.156 | 0.010 |
| minus_timing | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_argcheck | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |

## subgroup: eir

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1076 | 0.000 | 0.000 to 0.000 | -1.000 | 0.010 |
| output_only | 1076 | 0.000 | 0.000 to 0.000 | -1.000 | 0.010 |
| confidence | 1076 | 0.997 | 0.992 to 1.000 | -0.003 | 1.000 |
| pooled_conformal | 1076 | 0.454 | 0.405 to 0.507 | -0.546 | 0.010 |
| full | 1076 | 1.000 | 1.000 to 1.000 | +nan | nan |
| minus_local_calibration | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_conformal | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_drift | 1076 | 0.844 | 0.805 to 0.880 | -0.156 | 0.010 |
| minus_timing | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_argcheck | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |

## subgroup: intercepted

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1076 | 0.000 | 0.000 to 0.000 | -1.000 | 0.010 |
| output_only | 1076 | 0.231 | 0.189 to 0.276 | -0.769 | 0.010 |
| confidence | 1076 | 0.997 | 0.992 to 1.000 | -0.003 | 1.000 |
| pooled_conformal | 1076 | 0.454 | 0.403 to 0.508 | -0.546 | 0.010 |
| full | 1076 | 1.000 | 1.000 to 1.000 | +nan | nan |
| minus_local_calibration | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_conformal | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_drift | 1076 | 0.844 | 0.807 to 0.880 | -0.156 | 0.010 |
| minus_timing | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_argcheck | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |

## subgroup: intervention_gap

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 249 | 2.000 | 2.000 to 2.000 | +2.000 | 0.009 |
| confidence | 1073 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 488 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 1076 | 0.000 | 0.000 to 0.000 | +nan | nan |
| minus_local_calibration | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_conformal | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_drift | 908 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_timing | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_argcheck | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## subgroup: premature

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| output_only | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| confidence | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 1076 | 0.000 | 0.000 to 0.000 | +nan | nan |
| minus_local_calibration | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_conformal | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_drift | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_timing | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_argcheck | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## subgroup: steps_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1076 | 0.000 | 0.000 to 0.000 | -0.500 | 0.010 |
| output_only | 1076 | 0.000 | 0.000 to 0.000 | -0.500 | 0.010 |
| confidence | 1076 | 0.499 | 0.496 to 0.500 | -0.001 | 1.000 |
| pooled_conformal | 1076 | 0.227 | 0.201 to 0.252 | -0.273 | 0.010 |
| full | 1076 | 0.500 | 0.500 to 0.500 | +nan | nan |
| minus_local_calibration | 1076 | 0.500 | 0.500 to 0.500 | +0.000 | 1.000 |
| minus_subgroup_gap | 1076 | 0.500 | 0.500 to 0.500 | +0.000 | 1.000 |
| minus_conformal | 1076 | 0.500 | 0.500 to 0.500 | +0.000 | 1.000 |
| minus_drift | 1076 | 0.422 | 0.402 to 0.440 | -0.078 | 0.010 |
| minus_timing | 1076 | 0.500 | 0.500 to 0.500 | +0.000 | 1.000 |
| minus_argcheck | 1076 | 0.500 | 0.500 to 0.500 | +0.000 | 1.000 |

## subgroup: steps_to_intercept

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 249 | 2.000 | 2.000 to 2.000 | +2.000 | 0.009 |
| confidence | 1073 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 488 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 1076 | 0.000 | 0.000 to 0.000 | +nan | nan |
| minus_local_calibration | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_conformal | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_drift | 908 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_timing | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_argcheck | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## subgroup: tokens_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1076 | 0.000 | 0.000 to 0.000 | -0.549 | 0.010 |
| output_only | 1076 | 0.000 | 0.000 to 0.000 | -0.549 | 0.010 |
| confidence | 1076 | 0.547 | 0.544 to 0.549 | -0.002 | 1.000 |
| pooled_conformal | 1076 | 0.250 | 0.224 to 0.278 | -0.299 | 0.010 |
| full | 1076 | 0.549 | 0.549 to 0.549 | +nan | nan |
| minus_local_calibration | 1076 | 0.549 | 0.549 to 0.549 | +0.000 | 1.000 |
| minus_subgroup_gap | 1076 | 0.549 | 0.549 to 0.549 | +0.000 | 1.000 |
| minus_conformal | 1076 | 0.549 | 0.549 to 0.549 | +0.000 | 1.000 |
| minus_drift | 1076 | 0.463 | 0.442 to 0.483 | -0.085 | 0.010 |
| minus_timing | 1076 | 0.549 | 0.549 to 0.549 | +0.000 | 1.000 |
| minus_argcheck | 1076 | 0.549 | 0.549 to 0.549 | +0.000 | 1.000 |

## uncertainty: early

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1076 | 0.000 | 0.000 to 0.000 | -1.000 | 0.010 |
| output_only | 1076 | 0.000 | 0.000 to 0.000 | -1.000 | 0.010 |
| confidence | 1076 | 0.039 | 0.022 to 0.061 | -0.961 | 0.010 |
| pooled_conformal | 1076 | 0.011 | 0.003 to 0.025 | -0.989 | 0.010 |
| full | 1076 | 1.000 | 1.000 to 1.000 | +nan | nan |
| minus_local_calibration | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_conformal | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_drift | 1076 | 0.047 | 0.028 to 0.072 | -0.953 | 0.010 |
| minus_timing | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_argcheck | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |

## uncertainty: eir

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1076 | 0.000 | 0.000 to 0.000 | -1.000 | 0.010 |
| output_only | 1076 | 0.000 | 0.000 to 0.000 | -1.000 | 0.010 |
| confidence | 1076 | 0.039 | 0.020 to 0.059 | -0.961 | 0.010 |
| pooled_conformal | 1076 | 0.011 | 0.003 to 0.022 | -0.989 | 0.010 |
| full | 1076 | 1.000 | 1.000 to 1.000 | +nan | nan |
| minus_local_calibration | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_conformal | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_drift | 1076 | 0.047 | 0.028 to 0.070 | -0.953 | 0.010 |
| minus_timing | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_argcheck | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |

## uncertainty: intercepted

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1076 | 0.000 | 0.000 to 0.000 | -1.000 | 0.010 |
| output_only | 1076 | 0.231 | 0.186 to 0.278 | -0.769 | 0.010 |
| confidence | 1076 | 0.039 | 0.020 to 0.059 | -0.961 | 0.010 |
| pooled_conformal | 1076 | 0.011 | 0.003 to 0.022 | -0.989 | 0.010 |
| full | 1076 | 1.000 | 1.000 to 1.000 | +nan | nan |
| minus_local_calibration | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_conformal | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_drift | 1076 | 0.047 | 0.028 to 0.070 | -0.953 | 0.010 |
| minus_timing | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_argcheck | 1076 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |

## uncertainty: intervention_gap

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 249 | 2.000 | 2.000 to 2.000 | +2.000 | 0.009 |
| confidence | 42 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 12 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 1076 | 0.000 | 0.000 to 0.000 | +nan | nan |
| minus_local_calibration | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_conformal | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_drift | 51 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_timing | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_argcheck | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## uncertainty: premature

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| output_only | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| confidence | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 1076 | 0.000 | 0.000 to 0.000 | +nan | nan |
| minus_local_calibration | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_conformal | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_drift | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_timing | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_argcheck | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## uncertainty: steps_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1076 | 0.000 | 0.000 to 0.000 | -0.500 | 0.010 |
| output_only | 1076 | 0.000 | 0.000 to 0.000 | -0.500 | 0.010 |
| confidence | 1076 | 0.020 | 0.010 to 0.031 | -0.480 | 0.010 |
| pooled_conformal | 1076 | 0.006 | 0.001 to 0.011 | -0.494 | 0.010 |
| full | 1076 | 0.500 | 0.500 to 0.500 | +nan | nan |
| minus_local_calibration | 1076 | 0.500 | 0.500 to 0.500 | +0.000 | 1.000 |
| minus_subgroup_gap | 1076 | 0.500 | 0.500 to 0.500 | +0.000 | 1.000 |
| minus_conformal | 1076 | 0.500 | 0.500 to 0.500 | +0.000 | 1.000 |
| minus_drift | 1076 | 0.024 | 0.014 to 0.035 | -0.476 | 0.010 |
| minus_timing | 1076 | 0.500 | 0.500 to 0.500 | +0.000 | 1.000 |
| minus_argcheck | 1076 | 0.500 | 0.500 to 0.500 | +0.000 | 1.000 |

## uncertainty: steps_to_intercept

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 249 | 2.000 | 2.000 to 2.000 | +2.000 | 0.009 |
| confidence | 42 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 12 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 1076 | 0.000 | 0.000 to 0.000 | +nan | nan |
| minus_local_calibration | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_conformal | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_drift | 51 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_timing | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_argcheck | 1076 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## uncertainty: tokens_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 1076 | 0.000 | 0.000 to 0.000 | -0.549 | 0.010 |
| output_only | 1076 | 0.000 | 0.000 to 0.000 | -0.549 | 0.010 |
| confidence | 1076 | 0.022 | 0.011 to 0.034 | -0.527 | 0.010 |
| pooled_conformal | 1076 | 0.006 | 0.002 to 0.012 | -0.543 | 0.010 |
| full | 1076 | 0.549 | 0.548 to 0.549 | +nan | nan |
| minus_local_calibration | 1076 | 0.549 | 0.548 to 0.549 | +0.000 | 1.000 |
| minus_subgroup_gap | 1076 | 0.549 | 0.548 to 0.549 | +0.000 | 1.000 |
| minus_conformal | 1076 | 0.549 | 0.548 to 0.549 | +0.000 | 1.000 |
| minus_drift | 1076 | 0.026 | 0.014 to 0.040 | -0.523 | 0.010 |
| minus_timing | 1076 | 0.549 | 0.548 to 0.549 | +0.000 | 1.000 |
| minus_argcheck | 1076 | 0.549 | 0.548 to 0.549 | +0.000 | 1.000 |

## ungrounded: early

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| output_only | 249 | 1.000 | 1.000 to 1.000 | +1.000 | 0.010 |
| confidence | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 249 | 0.000 | 0.000 to 0.000 | +nan | nan |
| minus_local_calibration | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_conformal | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_drift | 249 | 0.627 | 0.518 to 0.735 | +0.627 | 0.010 |
| minus_timing | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_argcheck | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## ungrounded: eir

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 249 | 0.000 | 0.000 to 0.000 | -1.000 | 0.010 |
| output_only | 249 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| confidence | 249 | 0.518 | 0.410 to 0.627 | -0.482 | 0.010 |
| pooled_conformal | 249 | 0.265 | 0.169 to 0.361 | -0.735 | 0.010 |
| full | 249 | 1.000 | 1.000 to 1.000 | +nan | nan |
| minus_local_calibration | 249 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 249 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_conformal | 249 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_drift | 249 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_timing | 249 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_argcheck | 249 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |

## ungrounded: intercepted

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| output_only | 249 | 1.000 | 1.000 to 1.000 | +1.000 | 0.010 |
| confidence | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 249 | 0.000 | 0.000 to 0.000 | +nan | nan |
| minus_local_calibration | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_conformal | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_drift | 249 | 0.627 | 0.518 to 0.723 | +0.627 | 0.010 |
| minus_timing | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_argcheck | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## ungrounded: intervention_gap

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| confidence | 129 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 66 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 249 | 0.000 | 0.000 to 0.000 | +nan | nan |
| minus_local_calibration | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_conformal | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_drift | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_timing | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| minus_argcheck | 249 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## ungrounded: premature

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 249 | 0.000 | 0.000 to 0.000 | -1.000 | 0.010 |
| output_only | 249 | 0.000 | 0.000 to 0.000 | -1.000 | 0.010 |
| confidence | 249 | 0.518 | 0.410 to 0.614 | -0.482 | 0.010 |
| pooled_conformal | 249 | 0.265 | 0.181 to 0.361 | -0.735 | 0.010 |
| full | 249 | 1.000 | 1.000 to 1.000 | +nan | nan |
| minus_local_calibration | 249 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_subgroup_gap | 249 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_conformal | 249 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_drift | 249 | 0.373 | 0.277 to 0.482 | -0.627 | 0.010 |
| minus_timing | 249 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| minus_argcheck | 249 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |

## ungrounded: steps_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 249 | 0.000 | 0.000 to 0.000 | -0.500 | 0.010 |
| output_only | 249 | 0.000 | 0.000 to 0.000 | -0.500 | 0.010 |
| confidence | 249 | 0.259 | 0.205 to 0.313 | -0.241 | 0.010 |
| pooled_conformal | 249 | 0.133 | 0.090 to 0.181 | -0.367 | 0.010 |
| full | 249 | 0.500 | 0.500 to 0.500 | +nan | nan |
| minus_local_calibration | 249 | 0.500 | 0.500 to 0.500 | +0.000 | 1.000 |
| minus_subgroup_gap | 249 | 0.500 | 0.500 to 0.500 | +0.000 | 1.000 |
| minus_conformal | 249 | 0.500 | 0.500 to 0.500 | +0.000 | 1.000 |
| minus_drift | 249 | 0.187 | 0.139 to 0.235 | -0.313 | 0.010 |
| minus_timing | 249 | 0.500 | 0.500 to 0.500 | +0.000 | 1.000 |
| minus_argcheck | 249 | 0.500 | 0.500 to 0.500 | +0.000 | 1.000 |

## ungrounded: steps_to_intercept

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 249 | 0.000 | 0.000 to 0.000 | +nan | nan |
| confidence | 0 | nan | nan to nan | +nan | nan |
| pooled_conformal | 0 | nan | nan to nan | +nan | nan |
| full | 0 | nan | nan to nan | +nan | nan |
| minus_local_calibration | 0 | nan | nan to nan | +nan | nan |
| minus_subgroup_gap | 0 | nan | nan to nan | +nan | nan |
| minus_conformal | 0 | nan | nan to nan | +nan | nan |
| minus_drift | 156 | 0.000 | 0.000 to 0.000 | +nan | nan |
| minus_timing | 0 | nan | nan to nan | +nan | nan |
| minus_argcheck | 0 | nan | nan to nan | +nan | nan |

## ungrounded: tokens_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 249 | 0.000 | 0.000 to 0.000 | -0.555 | 0.010 |
| output_only | 249 | 0.000 | 0.000 to 0.000 | -0.555 | 0.010 |
| confidence | 249 | 0.288 | 0.228 to 0.348 | -0.267 | 0.010 |
| pooled_conformal | 249 | 0.147 | 0.100 to 0.201 | -0.408 | 0.010 |
| full | 249 | 0.555 | 0.555 to 0.556 | +nan | nan |
| minus_local_calibration | 249 | 0.555 | 0.555 to 0.556 | +0.000 | 1.000 |
| minus_subgroup_gap | 249 | 0.555 | 0.555 to 0.556 | +0.000 | 1.000 |
| minus_conformal | 249 | 0.555 | 0.555 to 0.556 | +0.000 | 1.000 |
| minus_drift | 249 | 0.208 | 0.154 to 0.268 | -0.348 | 0.010 |
| minus_timing | 249 | 0.555 | 0.555 to 0.556 | +0.000 | 1.000 |
| minus_argcheck | 249 | 0.555 | 0.555 to 0.556 | +0.000 | 1.000 |
