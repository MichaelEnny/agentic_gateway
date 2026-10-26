# RQ2 live reruns (ed, full)

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
| no_gate | 90 | 1.000 | 1.000 to 1.000 | +0.100 | 0.268 |
| output_only | 90 | 0.900 | 0.800 to 1.000 | +0.000 | 1.000 |
| confidence | 90 | 0.800 | 0.633 to 0.933 | -0.100 | 0.268 |
| pooled_conformal | 90 | 0.800 | 0.633 to 0.933 | -0.100 | 0.268 |
| full | 90 | 0.900 | 0.800 to 1.000 | +nan | nan |

## alert_lost

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 42 | 0.000 | 0.000 to 0.000 | -0.214 | 0.264 |
| output_only | 42 | 0.214 | 0.000 to 0.429 | +0.000 | 1.000 |
| confidence | 42 | 0.429 | 0.143 to 0.714 | +0.214 | 0.264 |
| pooled_conformal | 42 | 0.429 | 0.143 to 0.714 | +0.214 | 0.264 |
| full | 42 | 0.214 | 0.000 to 0.429 | +nan | nan |

## referred

| method | n | estimate | 95% CI | diff vs full | Holm p |
|---|---|---|---|---|---|
| no_gate | 90 | 0.000 | 0.000 to 0.000 | -0.100 | 0.296 |
| output_only | 90 | 0.100 | 0.000 to 0.233 | +0.000 | 1.000 |
| confidence | 90 | 0.200 | 0.067 to 0.367 | +0.100 | 0.296 |
| pooled_conformal | 90 | 0.200 | 0.067 to 0.367 | +0.100 | 0.296 |
| full | 90 | 0.100 | 0.000 to 0.233 | +nan | nan |
