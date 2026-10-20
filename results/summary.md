# Illustrative model results

Generated from `data/assumptions.json`. These are hypothetical scenarios, not observed company performance or forecasts.

| Case | Sold kg/year | Binding constraint | Unit contribution | Annual operating contribution | Five-year NPV | Break-even feasible |
|---|---:|---|---:|---:|---:|---|
| downside | 41,472 | demand | $1.31/kg | $-495,864 | $-3,368,841 | False |
| base | 86,400 | demand | $7.18/kg | $120,352 | $-1,538,589 | True |
| upside | 124,032 | capacity | $12.57/kg | $1,108,495 | $1,257,240 | True |

## Interpreting the scenarios

Changes across cases reflect multiple assumptions together; this is not a causal decomposition. NPV includes initial and maintenance capital, the five-year ramp, working-capital changes and final recovery, with no terminal business value.

Simulation operating contribution p10 / median / p90: $-245,678 / $3,090 / $295,531. Positive operating contribution occurs in 50.6% of illustrative draws. This frequency depends on the chosen independent distributions; it is not a validated probability of success.
