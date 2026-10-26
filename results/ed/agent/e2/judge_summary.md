# LLM-as-judge, 30 patients, 534 trajectories (ed, full)

Policy: llm; clean trajectories: 1075; faulty: {'sparse': 1075, 'subgroup': 1075, 'uncertainty': 1075, 'drift': 1075, 'duplicate': 444, 'ungrounded': 444}

## clean: false_intervention

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -0.100 | 0.380 |
| output_only | 90 | 0.100 | 0.000 to 0.200 | +0.000 | 1.000 |
| confidence | 90 | 0.200 | 0.067 to 0.333 | +0.100 | 0.380 |
| pooled_conformal | 90 | 0.200 | 0.067 to 0.333 | +0.100 | 0.380 |
| full | 90 | 0.100 | 0.000 to 0.200 | +nan | nan |
| llm_judge | 90 | 0.233 | 0.100 to 0.400 | +0.133 | 0.522 |

## drift: early

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |
| output_only | 90 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |
| confidence | 90 | 0.133 | 0.033 to 0.267 | -0.867 | 0.005 |
| pooled_conformal | 90 | 0.167 | 0.033 to 0.300 | -0.833 | 0.005 |
| full | 90 | 1.000 | 1.000 to 1.000 | +nan | nan |
| llm_judge | 90 | 0.233 | 0.100 to 0.400 | -0.767 | 0.005 |

## drift: eir

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |
| output_only | 90 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |
| confidence | 90 | 0.133 | 0.033 to 0.267 | -0.867 | 0.005 |
| pooled_conformal | 90 | 0.167 | 0.033 to 0.300 | -0.833 | 0.005 |
| full | 90 | 1.000 | 1.000 to 1.000 | +nan | nan |
| llm_judge | 90 | 0.233 | 0.100 to 0.400 | -0.767 | 0.005 |

## drift: intercepted

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |
| output_only | 90 | 0.467 | 0.300 to 0.633 | -0.533 | 0.005 |
| confidence | 90 | 0.133 | 0.033 to 0.267 | -0.867 | 0.005 |
| pooled_conformal | 90 | 0.167 | 0.067 to 0.300 | -0.833 | 0.005 |
| full | 90 | 1.000 | 1.000 to 1.000 | +nan | nan |
| llm_judge | 90 | 0.233 | 0.100 to 0.400 | -0.767 | 0.005 |

## drift: intervention_gap

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 42 | 2.000 | 2.000 to 2.000 | +2.000 | 0.004 |
| confidence | 12 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 15 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 90 | 0.000 | 0.000 to 0.000 | +nan | nan |
| llm_judge | 21 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

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
| confidence | 90 | 0.067 | 0.017 to 0.133 | -0.433 | 0.005 |
| pooled_conformal | 90 | 0.083 | 0.017 to 0.150 | -0.417 | 0.005 |
| full | 90 | 0.500 | 0.500 to 0.500 | +nan | nan |
| llm_judge | 90 | 0.117 | 0.050 to 0.200 | -0.383 | 0.005 |

## drift: steps_to_intercept

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 42 | 2.000 | 2.000 to 2.000 | +2.000 | 0.004 |
| confidence | 12 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 15 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 90 | 0.000 | 0.000 to 0.000 | +nan | nan |
| llm_judge | 21 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## drift: tokens_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -0.544 | 0.005 |
| output_only | 90 | 0.000 | 0.000 to 0.000 | -0.544 | 0.005 |
| confidence | 90 | 0.073 | 0.018 to 0.146 | -0.471 | 0.005 |
| pooled_conformal | 90 | 0.091 | 0.018 to 0.165 | -0.453 | 0.005 |
| full | 90 | 0.544 | 0.543 to 0.545 | +nan | nan |
| llm_judge | 90 | 0.126 | 0.054 to 0.217 | -0.418 | 0.005 |

## duplicate: early

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 42 | 0.000 | 0.000 to 0.000 | -0.786 | 0.005 |
| output_only | 42 | 0.786 | 0.571 to 1.000 | +0.000 | 1.000 |
| confidence | 42 | 0.000 | 0.000 to 0.000 | -0.786 | 0.005 |
| pooled_conformal | 42 | 0.000 | 0.000 to 0.000 | -0.786 | 0.005 |
| full | 42 | 0.786 | 0.571 to 1.000 | +nan | nan |
| llm_judge | 42 | 0.000 | 0.000 to 0.000 | -0.786 | 0.005 |

## duplicate: eir

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 42 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |
| output_only | 42 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| confidence | 42 | 0.429 | 0.143 to 0.643 | -0.571 | 0.005 |
| pooled_conformal | 42 | 0.429 | 0.143 to 0.643 | -0.571 | 0.005 |
| full | 42 | 1.000 | 1.000 to 1.000 | +nan | nan |
| llm_judge | 42 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |

## duplicate: intercepted

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 42 | 0.000 | 0.000 to 0.000 | -0.786 | 0.005 |
| output_only | 42 | 0.786 | 0.571 to 1.000 | +0.000 | 1.000 |
| confidence | 42 | 0.000 | 0.000 to 0.000 | -0.786 | 0.005 |
| pooled_conformal | 42 | 0.000 | 0.000 to 0.000 | -0.786 | 0.005 |
| full | 42 | 0.786 | 0.571 to 1.000 | +nan | nan |
| llm_judge | 42 | 0.000 | 0.000 to 0.000 | -0.786 | 0.005 |

## duplicate: intervention_gap

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 42 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| confidence | 18 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 18 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 42 | 0.000 | 0.000 to 0.000 | +nan | nan |
| llm_judge | 0 | nan | nan to nan | +nan | nan |

## duplicate: premature

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 42 | 0.000 | 0.000 to 0.000 | -0.214 | 0.315 |
| output_only | 42 | 0.214 | 0.000 to 0.429 | +0.000 | 1.000 |
| confidence | 42 | 0.429 | 0.214 to 0.714 | +0.214 | 0.315 |
| pooled_conformal | 42 | 0.429 | 0.214 to 0.714 | +0.214 | 0.315 |
| full | 42 | 0.214 | 0.000 to 0.429 | +nan | nan |
| llm_judge | 42 | 0.000 | 0.000 to 0.000 | -0.214 | 0.315 |

## duplicate: steps_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 42 | 0.000 | 0.000 to 0.000 | -0.129 | 0.345 |
| output_only | 42 | 0.043 | 0.000 to 0.086 | -0.086 | 0.345 |
| confidence | 42 | 0.257 | 0.129 to 0.386 | +0.129 | 0.345 |
| pooled_conformal | 42 | 0.257 | 0.129 to 0.386 | +0.129 | 0.345 |
| full | 42 | 0.129 | 0.000 to 0.257 | +nan | nan |
| llm_judge | 42 | 0.000 | 0.000 to 0.000 | -0.129 | 0.345 |

## duplicate: steps_to_intercept

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 33 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| confidence | 0 | nan | nan to nan | +nan | nan |
| pooled_conformal | 0 | nan | nan to nan | +nan | nan |
| full | 33 | 0.000 | 0.000 to 0.000 | +nan | nan |
| llm_judge | 0 | nan | nan to nan | +nan | nan |

## duplicate: tokens_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 42 | 0.000 | 0.000 to 0.000 | -0.139 | 0.275 |
| output_only | 42 | 0.048 | 0.000 to 0.096 | -0.091 | 0.275 |
| confidence | 42 | 0.278 | 0.139 to 0.464 | +0.139 | 0.275 |
| pooled_conformal | 42 | 0.278 | 0.139 to 0.464 | +0.139 | 0.275 |
| full | 42 | 0.139 | 0.000 to 0.278 | +nan | nan |
| llm_judge | 42 | 0.000 | 0.000 to 0.000 | -0.139 | 0.275 |

## sparse: early

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -0.156 | 0.005 |
| output_only | 90 | 0.000 | 0.000 to 0.000 | -0.156 | 0.005 |
| confidence | 90 | 0.100 | 0.044 to 0.156 | -0.056 | 0.024 |
| pooled_conformal | 90 | 0.244 | 0.167 to 0.322 | +0.089 | 0.005 |
| full | 90 | 0.156 | 0.089 to 0.222 | +nan | nan |
| llm_judge | 90 | 0.011 | 0.000 to 0.033 | -0.144 | 0.005 |

## sparse: eir

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -0.156 | 0.005 |
| output_only | 90 | 0.000 | 0.000 to 0.000 | -0.156 | 0.005 |
| confidence | 90 | 0.100 | 0.044 to 0.156 | -0.056 | 0.018 |
| pooled_conformal | 90 | 0.244 | 0.167 to 0.333 | +0.089 | 0.005 |
| full | 90 | 0.156 | 0.089 to 0.222 | +nan | nan |
| llm_judge | 90 | 0.733 | 0.633 to 0.822 | +0.578 | 0.005 |

## sparse: intercepted

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -0.156 | 0.005 |
| output_only | 90 | 0.089 | 0.033 to 0.156 | -0.067 | 0.009 |
| confidence | 90 | 0.100 | 0.044 to 0.156 | -0.056 | 0.074 |
| pooled_conformal | 90 | 0.244 | 0.167 to 0.322 | +0.089 | 0.008 |
| full | 90 | 0.156 | 0.100 to 0.222 | +nan | nan |
| llm_judge | 90 | 0.189 | 0.111 to 0.278 | +0.033 | 0.607 |

## sparse: intervention_gap

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 8 | 2.000 | 2.000 to 2.000 | +2.000 | 0.004 |
| confidence | 9 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 22 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 14 | 0.000 | 0.000 to 0.000 | +nan | nan |
| llm_judge | 82 | 0.390 | 0.213 to 0.585 | +0.390 | 0.004 |

## sparse: premature

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| output_only | 90 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| confidence | 90 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 90 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 90 | 0.000 | 0.000 to 0.000 | +nan | nan |
| llm_judge | 90 | 0.722 | 0.622 to 0.822 | +0.722 | 0.005 |

## sparse: steps_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -0.078 | 0.005 |
| output_only | 90 | 0.000 | 0.000 to 0.000 | -0.078 | 0.005 |
| confidence | 90 | 0.050 | 0.022 to 0.078 | -0.028 | 0.039 |
| pooled_conformal | 90 | 0.122 | 0.083 to 0.161 | +0.044 | 0.006 |
| full | 90 | 0.078 | 0.044 to 0.117 | +nan | nan |
| llm_judge | 90 | 0.547 | 0.472 to 0.617 | +0.469 | 0.005 |

## sparse: steps_to_intercept

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 8 | 2.000 | 2.000 to 2.000 | +2.000 | 0.004 |
| confidence | 9 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 22 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 14 | 0.000 | 0.000 to 0.000 | +nan | nan |
| llm_judge | 17 | 1.882 | 1.600 to 2.000 | +1.882 | 0.004 |

## sparse: tokens_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -0.085 | 0.005 |
| output_only | 90 | 0.000 | 0.000 to 0.000 | -0.085 | 0.005 |
| confidence | 90 | 0.054 | 0.024 to 0.085 | -0.030 | 0.026 |
| pooled_conformal | 90 | 0.133 | 0.091 to 0.181 | +0.048 | 0.005 |
| full | 90 | 0.085 | 0.048 to 0.121 | +nan | nan |
| llm_judge | 90 | 0.577 | 0.498 to 0.650 | +0.492 | 0.005 |

## subgroup: early

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -0.733 | 0.005 |
| output_only | 90 | 0.000 | 0.000 to 0.000 | -0.733 | 0.005 |
| confidence | 90 | 0.100 | 0.000 to 0.200 | -0.633 | 0.005 |
| pooled_conformal | 90 | 0.167 | 0.033 to 0.300 | -0.567 | 0.005 |
| full | 90 | 0.733 | 0.567 to 0.867 | +nan | nan |
| llm_judge | 90 | 0.000 | 0.000 to 0.000 | -0.733 | 0.005 |

## subgroup: eir

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -0.733 | 0.005 |
| output_only | 90 | 0.000 | 0.000 to 0.000 | -0.733 | 0.005 |
| confidence | 90 | 0.100 | 0.000 to 0.200 | -0.633 | 0.005 |
| pooled_conformal | 90 | 0.167 | 0.033 to 0.300 | -0.567 | 0.005 |
| full | 90 | 0.733 | 0.567 to 0.867 | +nan | nan |
| llm_judge | 90 | 0.000 | 0.000 to 0.000 | -0.733 | 0.005 |

## subgroup: intercepted

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -0.733 | 0.005 |
| output_only | 90 | 0.267 | 0.133 to 0.433 | -0.467 | 0.005 |
| confidence | 90 | 0.100 | 0.000 to 0.233 | -0.633 | 0.005 |
| pooled_conformal | 90 | 0.167 | 0.033 to 0.300 | -0.567 | 0.005 |
| full | 90 | 0.733 | 0.567 to 0.867 | +nan | nan |
| llm_judge | 90 | 0.511 | 0.333 to 0.678 | -0.222 | 0.027 |

## subgroup: intervention_gap

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 24 | 2.000 | 2.000 to 2.000 | +2.000 | 0.004 |
| confidence | 9 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 15 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 66 | 0.000 | 0.000 to 0.000 | +nan | nan |
| llm_judge | 46 | 2.000 | 2.000 to 2.000 | +2.000 | 0.004 |

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
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -0.367 | 0.005 |
| output_only | 90 | 0.000 | 0.000 to 0.000 | -0.367 | 0.005 |
| confidence | 90 | 0.050 | 0.000 to 0.117 | -0.317 | 0.005 |
| pooled_conformal | 90 | 0.083 | 0.017 to 0.150 | -0.283 | 0.005 |
| full | 90 | 0.367 | 0.283 to 0.433 | +nan | nan |
| llm_judge | 90 | 0.000 | 0.000 to 0.000 | -0.367 | 0.005 |

## subgroup: steps_to_intercept

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 24 | 2.000 | 2.000 to 2.000 | +2.000 | 0.004 |
| confidence | 9 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 15 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 66 | 0.000 | 0.000 to 0.000 | +nan | nan |
| llm_judge | 46 | 2.000 | 2.000 to 2.000 | +2.000 | 0.004 |

## subgroup: tokens_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -0.399 | 0.005 |
| output_only | 90 | 0.000 | 0.000 to 0.000 | -0.399 | 0.005 |
| confidence | 90 | 0.054 | 0.000 to 0.126 | -0.345 | 0.005 |
| pooled_conformal | 90 | 0.090 | 0.018 to 0.162 | -0.308 | 0.005 |
| full | 90 | 0.399 | 0.309 to 0.489 | +nan | nan |
| llm_judge | 90 | 0.000 | 0.000 to 0.000 | -0.399 | 0.005 |

## uncertainty: early

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -0.067 | 1.000 |
| output_only | 90 | 0.000 | 0.000 to 0.000 | -0.067 | 1.000 |
| confidence | 90 | 0.033 | 0.000 to 0.100 | -0.033 | 1.000 |
| pooled_conformal | 90 | 0.067 | 0.000 to 0.167 | +0.000 | 1.000 |
| full | 90 | 0.067 | 0.000 to 0.167 | +nan | nan |
| llm_judge | 90 | 0.100 | 0.000 to 0.233 | +0.033 | 1.000 |

## uncertainty: eir

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -0.067 | 0.905 |
| output_only | 90 | 0.000 | 0.000 to 0.000 | -0.067 | 0.905 |
| confidence | 90 | 0.033 | 0.000 to 0.100 | -0.033 | 1.000 |
| pooled_conformal | 90 | 0.067 | 0.000 to 0.167 | +0.000 | 1.000 |
| full | 90 | 0.067 | 0.000 to 0.167 | +nan | nan |
| llm_judge | 90 | 0.200 | 0.067 to 0.333 | +0.133 | 0.905 |

## uncertainty: intercepted

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -0.067 | 0.972 |
| output_only | 90 | 0.067 | 0.000 to 0.167 | +0.000 | 1.000 |
| confidence | 90 | 0.033 | 0.000 to 0.100 | -0.033 | 1.000 |
| pooled_conformal | 90 | 0.067 | 0.000 to 0.167 | +0.000 | 1.000 |
| full | 90 | 0.067 | 0.000 to 0.167 | +nan | nan |
| llm_judge | 90 | 0.467 | 0.289 to 0.644 | +0.400 | 0.005 |

## uncertainty: intervention_gap

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 6 | 2.000 | 2.000 to 2.000 | +2.000 | 0.005 |
| confidence | 3 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 6 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 6 | 0.000 | 0.000 to 0.000 | +nan | nan |
| llm_judge | 51 | 1.294 | 0.800 to 1.755 | +1.294 | 0.005 |

## uncertainty: premature

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| output_only | 90 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| confidence | 90 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 90 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 90 | 0.000 | 0.000 to 0.000 | +nan | nan |
| llm_judge | 90 | 0.100 | 0.000 to 0.233 | +0.100 | 0.430 |

## uncertainty: steps_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -0.033 | 0.916 |
| output_only | 90 | 0.000 | 0.000 to 0.000 | -0.033 | 0.916 |
| confidence | 90 | 0.017 | 0.000 to 0.050 | -0.017 | 1.000 |
| pooled_conformal | 90 | 0.033 | 0.000 to 0.083 | +0.000 | 1.000 |
| full | 90 | 0.033 | 0.000 to 0.083 | +nan | nan |
| llm_judge | 90 | 0.125 | 0.042 to 0.217 | +0.092 | 0.625 |

## uncertainty: steps_to_intercept

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 6 | 2.000 | 2.000 to 2.000 | +2.000 | 0.005 |
| confidence | 3 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 6 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 6 | 0.000 | 0.000 to 0.000 | +nan | nan |
| llm_judge | 42 | 1.571 | 1.143 to 2.000 | +1.571 | 0.005 |

## uncertainty: tokens_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -0.037 | 1.000 |
| output_only | 90 | 0.000 | 0.000 to 0.000 | -0.037 | 1.000 |
| confidence | 90 | 0.018 | 0.000 to 0.055 | -0.018 | 1.000 |
| pooled_conformal | 90 | 0.037 | 0.000 to 0.091 | +0.000 | 1.000 |
| full | 90 | 0.037 | 0.000 to 0.091 | +nan | nan |
| llm_judge | 90 | 0.133 | 0.044 to 0.231 | +0.096 | 0.475 |

## ungrounded: early

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 42 | 0.000 | 0.000 to 0.000 | -0.786 | 0.005 |
| output_only | 42 | 1.000 | 1.000 to 1.000 | +0.214 | 0.081 |
| confidence | 42 | 0.000 | 0.000 to 0.000 | -0.786 | 0.005 |
| pooled_conformal | 42 | 0.000 | 0.000 to 0.000 | -0.786 | 0.005 |
| full | 42 | 0.786 | 0.571 to 1.000 | +nan | nan |
| llm_judge | 42 | 0.143 | 0.048 to 0.262 | -0.643 | 0.005 |

## ungrounded: eir

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 42 | 0.000 | 0.000 to 0.000 | -1.000 | 0.005 |
| output_only | 42 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| confidence | 42 | 0.429 | 0.214 to 0.714 | -0.571 | 0.005 |
| pooled_conformal | 42 | 0.429 | 0.214 to 0.714 | -0.571 | 0.005 |
| full | 42 | 1.000 | 1.000 to 1.000 | +nan | nan |
| llm_judge | 42 | 0.143 | 0.048 to 0.262 | -0.857 | 0.005 |

## ungrounded: intercepted

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 42 | 0.000 | 0.000 to 0.000 | -0.786 | 0.005 |
| output_only | 42 | 1.000 | 1.000 to 1.000 | +0.214 | 0.071 |
| confidence | 42 | 0.000 | 0.000 to 0.000 | -0.786 | 0.005 |
| pooled_conformal | 42 | 0.000 | 0.000 to 0.000 | -0.786 | 0.005 |
| full | 42 | 0.786 | 0.571 to 1.000 | +nan | nan |
| llm_judge | 42 | 0.143 | 0.048 to 0.238 | -0.643 | 0.005 |

## ungrounded: intervention_gap

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 42 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| confidence | 18 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| pooled_conformal | 18 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| full | 42 | 0.000 | 0.000 to 0.000 | +nan | nan |
| llm_judge | 6 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## ungrounded: premature

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 42 | 0.000 | 0.000 to 0.000 | -0.214 | 0.315 |
| output_only | 42 | 0.000 | 0.000 to 0.000 | -0.214 | 0.315 |
| confidence | 42 | 0.429 | 0.214 to 0.714 | +0.214 | 0.315 |
| pooled_conformal | 42 | 0.429 | 0.214 to 0.714 | +0.214 | 0.315 |
| full | 42 | 0.214 | 0.000 to 0.429 | +nan | nan |
| llm_judge | 42 | 0.000 | 0.000 to 0.000 | -0.214 | 0.315 |

## ungrounded: steps_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 42 | 0.000 | 0.000 to 0.000 | -0.107 | 0.325 |
| output_only | 42 | 0.000 | 0.000 to 0.000 | -0.107 | 0.325 |
| confidence | 42 | 0.214 | 0.071 to 0.321 | +0.107 | 0.325 |
| pooled_conformal | 42 | 0.214 | 0.071 to 0.321 | +0.107 | 0.325 |
| full | 42 | 0.107 | 0.000 to 0.214 | +nan | nan |
| llm_judge | 42 | 0.000 | 0.000 to 0.000 | -0.107 | 0.325 |

## ungrounded: steps_to_intercept

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 0 | nan | nan to nan | +nan | nan |
| output_only | 42 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |
| confidence | 0 | nan | nan to nan | +nan | nan |
| pooled_conformal | 0 | nan | nan to nan | +nan | nan |
| full | 33 | 0.000 | 0.000 to 0.000 | +nan | nan |
| llm_judge | 6 | 0.000 | 0.000 to 0.000 | +0.000 | 1.000 |

## ungrounded: tokens_saved

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 42 | 0.000 | 0.000 to 0.000 | -0.117 | 0.285 |
| output_only | 42 | 0.000 | 0.000 to 0.000 | -0.117 | 0.285 |
| confidence | 42 | 0.235 | 0.078 to 0.392 | +0.118 | 0.285 |
| pooled_conformal | 42 | 0.235 | 0.078 to 0.392 | +0.118 | 0.285 |
| full | 42 | 0.117 | 0.000 to 0.235 | +nan | nan |
| llm_judge | 42 | 0.000 | 0.000 to 0.000 | -0.117 | 0.285 |
