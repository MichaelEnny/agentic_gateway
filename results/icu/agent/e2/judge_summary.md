# LLM-as-judge, 30 patients, 492 trajectories (icu, full)

Policy: llm; clean trajectories: 1076; faulty: {'sparse': 1076, 'subgroup': 1076, 'uncertainty': 1076, 'drift': 1076, 'duplicate': 249, 'ungrounded': 249}

## clean: false_intervention

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |
| output_only | 90 | 0.233 | 0.100 to 0.400 | -0.767 | 0.005 |
| confidence | 90 | 0.100 | 0.000 to 0.233 | -0.900 | 0.005 |
| pooled_conformal | 90 | 0.100 | 0.000 to 0.233 | -0.900 | 0.005 |
| full | 90 | 1.000 | 1.000 to 1.000 | +nan | nan |
| llm_judge | 90 | 0.100 | 0.000 to 0.200 | -0.900 | 0.005 |

## drift: early

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |
| output_only | 90 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |
| confidence | 90 | 0.100 | 0.000 to 0.233 | -0.900 | 0.005 |
| pooled_conformal | 90 | 0.067 | 0.000 to 0.167 | -0.933 | 0.005 |
| full | 90 | 1.000 | 1.000 to 1.000 | +nan | nan |
| llm_judge | 90 | 0.033 | 0.000 to 0.100 | -0.967 | 0.005 |

## drift: eir

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |
| output_only | 90 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |
| confidence | 90 | 0.100 | 0.000 to 0.233 | -0.900 | 0.005 |
| pooled_conformal | 90 | 0.067 | 0.000 to 0.167 | -0.933 | 0.005 |
| full | 90 | 1.000 | 1.000 to 1.000 | +nan | nan |
| llm_judge | 90 | 0.033 | 0.000 to 0.100 | -0.967 | 0.005 |

## drift: intercepted

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |
| output_only | 90 | 0.233 | 0.100 to 0.400 | -0.767 | 0.005 |
| confidence | 90 | 0.100 | 0.000 to 0.201 | -0.900 | 0.005 |
| pooled_conformal | 90 | 0.067 | 0.000 to 0.167 | -0.933 | 0.005 |
| full | 90 | 1.000 | 1.000 to 1.000 | +nan | nan |
| llm_judge | 90 | 0.100 | 0.000 to 0.233 | -0.900 | 0.005 |

## drift: intervention_gap

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 21 | 2.000 | 2.000 to 2.000 | +2.000 | 0.004 |
| confidence | 9 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 6 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 90 | 0.000 | 0.000 to 0.000 | +nan | nan |
| llm_judge | 9 | 1.333 | 0.000 to 2.000 | +1.333 | 0.532 |

## drift: premature

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| output_only | 90 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| confidence | 90 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 90 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 90 | 0.000 | 0.000 to 0.000 | +nan | nan |
| llm_judge | 90 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## drift: steps_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -0.500 | 0.005 |
| output_only | 90 | 0.000 | 0.000 to 0.000 | -0.500 | 0.005 |
| confidence | 90 | 0.050 | 0.000 to 0.117 | -0.450 | 0.005 |
| pooled_conformal | 90 | 0.033 | 0.000 to 0.083 | -0.467 | 0.005 |
| full | 90 | 0.500 | 0.500 to 0.500 | +nan | nan |
| llm_judge | 90 | 0.017 | 0.000 to 0.050 | -0.483 | 0.005 |

## drift: steps_to_intercept

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 21 | 2.000 | 2.000 to 2.000 | +2.000 | 0.004 |
| confidence | 9 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 6 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 90 | 0.000 | 0.000 to 0.000 | +nan | nan |
| llm_judge | 9 | 1.333 | 0.000 to 2.000 | +1.333 | 0.463 |

## drift: tokens_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -0.549 | 0.005 |
| output_only | 90 | 0.000 | 0.000 to 0.000 | -0.549 | 0.005 |
| confidence | 90 | 0.056 | 0.000 to 0.130 | -0.493 | 0.005 |
| pooled_conformal | 90 | 0.037 | 0.000 to 0.093 | -0.512 | 0.005 |
| full | 90 | 0.549 | 0.548 to 0.551 | +nan | nan |
| llm_judge | 90 | 0.018 | 0.000 to 0.055 | -0.531 | 0.005 |

## duplicate: early

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 21 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| output_only | 21 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| confidence | 21 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 21 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 21 | 0.000 | 0.000 to 0.000 | +nan | nan |
| llm_judge | 21 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## duplicate: eir

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 21 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |
| output_only | 21 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| confidence | 21 | 0.429 | 0.143 to 0.857 | -0.571 | 0.018 |
| pooled_conformal | 21 | 0.429 | 0.143 to 0.857 | -0.571 | 0.018 |
| full | 21 | 1.000 | 1.000 to 1.000 | +nan | nan |
| llm_judge | 21 | 0.143 | 0.000 to 0.429 | -0.857 | 0.005 |

## duplicate: intercepted

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 21 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| output_only | 21 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| confidence | 21 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 21 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 21 | 0.000 | 0.000 to 0.000 | +nan | nan |
| llm_judge | 21 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## duplicate: intervention_gap

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 21 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| confidence | 9 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 9 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 21 | 0.000 | 0.000 to 0.000 | +nan | nan |
| llm_judge | 3 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## duplicate: premature

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 21 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |
| output_only | 21 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| confidence | 21 | 0.429 | 0.143 to 0.714 | -0.571 | 0.027 |
| pooled_conformal | 21 | 0.429 | 0.143 to 0.714 | -0.571 | 0.027 |
| full | 21 | 1.000 | 1.000 to 1.000 | +nan | nan |
| llm_judge | 21 | 0.143 | 0.000 to 0.429 | -0.857 | 0.005 |

## duplicate: steps_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 21 | 0.000 | 0.000 to 0.000 | -0.600 | 0.005 |
| output_only | 21 | 0.200 | 0.200 to 0.200 | -0.400 | 0.005 |
| confidence | 21 | 0.257 | 0.086 to 0.514 | -0.343 | 0.010 |
| pooled_conformal | 21 | 0.257 | 0.086 to 0.514 | -0.343 | 0.010 |
| full | 21 | 0.600 | 0.600 to 0.600 | +nan | nan |
| llm_judge | 21 | 0.029 | 0.000 to 0.086 | -0.571 | 0.005 |

## duplicate: tokens_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 21 | 0.000 | 0.000 to 0.000 | -0.657 | 0.005 |
| output_only | 21 | 0.227 | 0.227 to 0.227 | -0.430 | 0.005 |
| confidence | 21 | 0.281 | 0.094 to 0.469 | -0.376 | 0.010 |
| pooled_conformal | 21 | 0.281 | 0.094 to 0.469 | -0.376 | 0.010 |
| full | 21 | 0.657 | 0.657 to 0.657 | +nan | nan |
| llm_judge | 21 | 0.032 | 0.000 to 0.097 | -0.625 | 0.005 |

## sparse: early

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |
| output_only | 90 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |
| confidence | 90 | 0.811 | 0.733 to 0.878 | -0.189 | 0.005 |
| pooled_conformal | 90 | 0.467 | 0.344 to 0.589 | -0.533 | 0.005 |
| full | 90 | 1.000 | 1.000 to 1.000 | +nan | nan |
| llm_judge | 90 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |

## sparse: eir

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |
| output_only | 90 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |
| confidence | 90 | 0.811 | 0.733 to 0.878 | -0.189 | 0.005 |
| pooled_conformal | 90 | 0.467 | 0.344 to 0.589 | -0.533 | 0.005 |
| full | 90 | 1.000 | 1.000 to 1.000 | +nan | nan |
| llm_judge | 90 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |

## sparse: intercepted

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |
| output_only | 90 | 0.233 | 0.100 to 0.400 | -0.767 | 0.005 |
| confidence | 90 | 0.811 | 0.733 to 0.889 | -0.189 | 0.005 |
| pooled_conformal | 90 | 0.467 | 0.344 to 0.589 | -0.533 | 0.005 |
| full | 90 | 1.000 | 1.000 to 1.000 | +nan | nan |
| llm_judge | 90 | 0.244 | 0.111 to 0.389 | -0.756 | 0.005 |

## sparse: intervention_gap

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 21 | 2.000 | 2.000 to 2.000 | +2.000 | 0.004 |
| confidence | 73 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 42 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 90 | 0.000 | 0.000 to 0.000 | +nan | nan |
| llm_judge | 22 | 2.000 | 2.000 to 2.000 | +2.000 | 0.004 |

## sparse: premature

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| output_only | 90 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| confidence | 90 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 90 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 90 | 0.000 | 0.000 to 0.000 | +nan | nan |
| llm_judge | 90 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## sparse: steps_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -0.500 | 0.005 |
| output_only | 90 | 0.000 | 0.000 to 0.000 | -0.500 | 0.005 |
| confidence | 90 | 0.406 | 0.367 to 0.439 | -0.094 | 0.005 |
| pooled_conformal | 90 | 0.233 | 0.172 to 0.294 | -0.267 | 0.005 |
| full | 90 | 0.500 | 0.500 to 0.500 | +nan | nan |
| llm_judge | 90 | 0.000 | 0.000 to 0.000 | -0.500 | 0.005 |

## sparse: steps_to_intercept

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 21 | 2.000 | 2.000 to 2.000 | +2.000 | 0.004 |
| confidence | 73 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 42 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 90 | 0.000 | 0.000 to 0.000 | +nan | nan |
| llm_judge | 22 | 2.000 | 2.000 to 2.000 | +2.000 | 0.004 |

## sparse: tokens_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -0.549 | 0.005 |
| output_only | 90 | 0.000 | 0.000 to 0.000 | -0.549 | 0.005 |
| confidence | 90 | 0.446 | 0.403 to 0.488 | -0.104 | 0.005 |
| pooled_conformal | 90 | 0.256 | 0.189 to 0.329 | -0.293 | 0.005 |
| full | 90 | 0.549 | 0.548 to 0.551 | +nan | nan |
| llm_judge | 90 | 0.000 | 0.000 to 0.000 | -0.549 | 0.005 |

## subgroup: early

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |
| output_only | 90 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |
| confidence | 90 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| pooled_conformal | 90 | 0.500 | 0.333 to 0.700 | -0.500 | 0.005 |
| full | 90 | 1.000 | 1.000 to 1.000 | +nan | nan |
| llm_judge | 90 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |

## subgroup: eir

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |
| output_only | 90 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |
| confidence | 90 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| pooled_conformal | 90 | 0.500 | 0.333 to 0.700 | -0.500 | 0.005 |
| full | 90 | 1.000 | 1.000 to 1.000 | +nan | nan |
| llm_judge | 90 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |

## subgroup: intercepted

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |
| output_only | 90 | 0.233 | 0.100 to 0.400 | -0.767 | 0.005 |
| confidence | 90 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| pooled_conformal | 90 | 0.500 | 0.333 to 0.667 | -0.500 | 0.005 |
| full | 90 | 1.000 | 1.000 to 1.000 | +nan | nan |
| llm_judge | 90 | 0.144 | 0.044 to 0.267 | -0.856 | 0.005 |

## subgroup: intervention_gap

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 21 | 2.000 | 2.000 to 2.000 | +2.000 | 0.004 |
| confidence | 90 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 45 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 90 | 0.000 | 0.000 to 0.000 | +nan | nan |
| llm_judge | 13 | 2.000 | 2.000 to 2.000 | +2.000 | 0.004 |

## subgroup: premature

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| output_only | 90 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| confidence | 90 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 90 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 90 | 0.000 | 0.000 to 0.000 | +nan | nan |
| llm_judge | 90 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## subgroup: steps_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -0.500 | 0.005 |
| output_only | 90 | 0.000 | 0.000 to 0.000 | -0.500 | 0.005 |
| confidence | 90 | 0.500 | 0.500 to 0.500 | +0.000 | 1.000 |
| pooled_conformal | 90 | 0.250 | 0.167 to 0.333 | -0.250 | 0.005 |
| full | 90 | 0.500 | 0.500 to 0.500 | +nan | nan |
| llm_judge | 90 | 0.000 | 0.000 to 0.000 | -0.500 | 0.005 |

## subgroup: steps_to_intercept

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 21 | 2.000 | 2.000 to 2.000 | +2.000 | 0.004 |
| confidence | 90 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 45 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 90 | 0.000 | 0.000 to 0.000 | +nan | nan |
| llm_judge | 13 | 2.000 | 2.000 to 2.000 | +2.000 | 0.004 |

## subgroup: tokens_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -0.549 | 0.005 |
| output_only | 90 | 0.000 | 0.000 to 0.000 | -0.549 | 0.005 |
| confidence | 90 | 0.549 | 0.548 to 0.551 | +0.000 | 1.000 |
| pooled_conformal | 90 | 0.276 | 0.182 to 0.368 | -0.273 | 0.005 |
| full | 90 | 0.549 | 0.548 to 0.551 | +nan | nan |
| llm_judge | 90 | 0.000 | 0.000 to 0.000 | -0.549 | 0.005 |

## uncertainty: early

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |
| output_only | 90 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |
| confidence | 90 | 0.033 | 0.000 to 0.100 | -0.967 | 0.005 |
| pooled_conformal | 90 | 0.033 | 0.000 to 0.100 | -0.967 | 0.005 |
| full | 90 | 1.000 | 1.000 to 1.000 | +nan | nan |
| llm_judge | 90 | 0.067 | 0.000 to 0.167 | -0.933 | 0.005 |

## uncertainty: eir

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |
| output_only | 90 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |
| confidence | 90 | 0.033 | 0.000 to 0.100 | -0.967 | 0.005 |
| pooled_conformal | 90 | 0.033 | 0.000 to 0.100 | -0.967 | 0.005 |
| full | 90 | 1.000 | 1.000 to 1.000 | +nan | nan |
| llm_judge | 90 | 0.067 | 0.000 to 0.167 | -0.933 | 0.005 |

## uncertainty: intercepted

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |
| output_only | 90 | 0.233 | 0.100 to 0.400 | -0.767 | 0.005 |
| confidence | 90 | 0.033 | 0.000 to 0.100 | -0.967 | 0.005 |
| pooled_conformal | 90 | 0.033 | 0.000 to 0.100 | -0.967 | 0.005 |
| full | 90 | 1.000 | 1.000 to 1.000 | +nan | nan |
| llm_judge | 90 | 0.100 | 0.011 to 0.211 | -0.900 | 0.005 |

## uncertainty: intervention_gap

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 21 | 2.000 | 2.000 to 2.000 | +2.000 | 0.004 |
| confidence | 3 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 3 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 90 | 0.000 | 0.000 to 0.000 | +nan | nan |
| llm_judge | 9 | 0.667 | 0.000 to 2.000 | +0.667 | 0.611 |

## uncertainty: premature

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| output_only | 90 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| confidence | 90 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 90 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 90 | 0.000 | 0.000 to 0.000 | +nan | nan |
| llm_judge | 90 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## uncertainty: steps_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -0.500 | 0.005 |
| output_only | 90 | 0.000 | 0.000 to 0.000 | -0.500 | 0.005 |
| confidence | 90 | 0.017 | 0.000 to 0.050 | -0.483 | 0.005 |
| pooled_conformal | 90 | 0.017 | 0.000 to 0.050 | -0.483 | 0.005 |
| full | 90 | 0.500 | 0.500 to 0.500 | +nan | nan |
| llm_judge | 90 | 0.033 | 0.000 to 0.083 | -0.467 | 0.005 |

## uncertainty: steps_to_intercept

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 21 | 2.000 | 2.000 to 2.000 | +2.000 | 0.004 |
| confidence | 3 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 3 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 90 | 0.000 | 0.000 to 0.000 | +nan | nan |
| llm_judge | 9 | 0.667 | 0.000 to 2.000 | +0.667 | 0.708 |

## uncertainty: tokens_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -0.549 | 0.005 |
| output_only | 90 | 0.000 | 0.000 to 0.000 | -0.549 | 0.005 |
| confidence | 90 | 0.019 | 0.000 to 0.056 | -0.530 | 0.005 |
| pooled_conformal | 90 | 0.019 | 0.000 to 0.056 | -0.530 | 0.005 |
| full | 90 | 0.549 | 0.548 to 0.551 | +nan | nan |
| llm_judge | 90 | 0.036 | 0.000 to 0.091 | -0.513 | 0.005 |

## ungrounded: early

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 21 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| output_only | 21 | 1.000 | 1.000 to 1.000 | +1.000 | 0.005 |
| confidence | 21 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 21 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 21 | 0.000 | 0.000 to 0.000 | +nan | nan |
| llm_judge | 21 | 0.524 | 0.190 to 0.810 | +0.524 | 0.008 |

## ungrounded: eir

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 21 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |
| output_only | 21 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| confidence | 21 | 0.429 | 0.143 to 0.857 | -0.571 | 0.024 |
| pooled_conformal | 21 | 0.429 | 0.143 to 0.857 | -0.571 | 0.024 |
| full | 21 | 1.000 | 1.000 to 1.000 | +nan | nan |
| llm_judge | 21 | 0.524 | 0.190 to 0.810 | -0.476 | 0.024 |

## ungrounded: intercepted

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 21 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| output_only | 21 | 1.000 | 1.000 to 1.000 | +1.000 | 0.005 |
| confidence | 21 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 21 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 21 | 0.000 | 0.000 to 0.000 | +nan | nan |
| llm_judge | 21 | 0.524 | 0.190 to 0.810 | +0.524 | 0.008 |

## ungrounded: intervention_gap

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 21 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| confidence | 9 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 9 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 21 | 0.000 | 0.000 to 0.000 | +nan | nan |
| llm_judge | 11 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## ungrounded: premature

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 21 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |
| output_only | 21 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |
| confidence | 21 | 0.429 | 0.143 to 0.857 | -0.571 | 0.024 |
| pooled_conformal | 21 | 0.429 | 0.143 to 0.857 | -0.571 | 0.024 |
| full | 21 | 1.000 | 1.000 to 1.000 | +nan | nan |
| llm_judge | 21 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |

## ungrounded: steps_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 21 | 0.000 | 0.000 to 0.000 | -0.500 | 0.005 |
| output_only | 21 | 0.000 | 0.000 to 0.000 | -0.500 | 0.005 |
| confidence | 21 | 0.214 | 0.071 to 0.429 | -0.286 | 0.016 |
| pooled_conformal | 21 | 0.214 | 0.071 to 0.429 | -0.286 | 0.016 |
| full | 21 | 0.500 | 0.500 to 0.500 | +nan | nan |
| llm_judge | 21 | 0.000 | 0.000 to 0.000 | -0.500 | 0.005 |

## ungrounded: steps_to_intercept

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 21 | 0.000 | 0.000 to 0.000 | +nan | nan |
| confidence | 0 | nan | nan to nan | +nan | nan |
| pooled_conformal | 0 | nan | nan to nan | +nan | nan |
| full | 0 | nan | nan to nan | +nan | nan |
| llm_judge | 11 | 0.000 | 0.000 to 0.000 | +nan | nan |

## ungrounded: tokens_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 21 | 0.000 | 0.000 to 0.000 | -0.556 | 0.005 |
| output_only | 21 | 0.000 | 0.000 to 0.000 | -0.556 | 0.005 |
| confidence | 21 | 0.238 | 0.079 to 0.476 | -0.318 | 0.018 |
| pooled_conformal | 21 | 0.238 | 0.079 to 0.476 | -0.318 | 0.018 |
| full | 21 | 0.556 | 0.556 to 0.557 | +nan | nan |
| llm_judge | 21 | 0.000 | 0.000 to 0.000 | -0.556 | 0.005 |
