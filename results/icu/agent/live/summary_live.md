# RQ2 live reruns (icu, full)

Policy: llm; cases: 30; seeds: [0, 1, 2]

## completed

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| output_only | 90 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| confidence | 90 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| pooled_conformal | 90 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| full | 90 | 1.000 | 1.000 to 1.000 | +nan | nan |

## same_decision

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 1.000 | 1.000 to 1.000 | +0.233 | 0.008 |
| output_only | 90 | 0.767 | 0.600 to 0.900 | +0.000 | 1.000 |
| confidence | 90 | 0.900 | 0.799 to 1.000 | +0.133 | 0.093 |
| pooled_conformal | 90 | 0.900 | 0.799 to 1.000 | +0.133 | 0.093 |
| full | 90 | 0.767 | 0.600 to 0.900 | +nan | nan |

## alert_lost

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 21 | 0.000 | 0.000 to 0.000 | -1.000 | 0.004 |
| output_only | 21 | 1.000 | 1.000 to 1.000 | +0.000 | 1.000 |
| confidence | 21 | 0.429 | 0.143 to 0.857 | -0.571 | 0.027 |
| pooled_conformal | 21 | 0.429 | 0.143 to 0.857 | -0.571 | 0.027 |
| full | 21 | 1.000 | 1.000 to 1.000 | +nan | nan |

## referred

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -1.000 | 0.004 |
| output_only | 90 | 0.233 | 0.100 to 0.400 | -0.767 | 0.004 |
| confidence | 90 | 0.100 | 0.000 to 0.233 | -0.900 | 0.004 |
| pooled_conformal | 90 | 0.100 | 0.000 to 0.233 | -0.900 | 0.004 |
| full | 90 | 1.000 | 1.000 to 1.000 | +nan | nan |
