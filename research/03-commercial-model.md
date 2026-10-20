# Commercial model: demand, production, and capital

## Scope and input status

The reusable model represents a hypothetical US plant-based printed whole-cut manufacturer serving foodservice accounts. Every numeric input in `data/assumptions.json` is **illustrative**. These values are chosen to exercise business constraints and demonstrate the method; none is a supplier quote or estimated company operating result. Do not use the outputs as a forecast or published TAM.

The annual account universe is an assumed prospect list for one territory, not all US restaurants. No German openness percentage enters the model. Inputs use constant US dollars, kilograms, hours, and annual periods. The model excludes taxes, financing, depreciation, grants, terminal value, and residual equipment value. NPV is a simplified unlevered pretax project metric.

## Formula dictionary

| Measure | Formula / definition |
|---|---|
| Territory demand ceiling | eligible accounts × kg/account/week × selling weeks |
| Serviceable demand | territory demand ceiling × serviceable fraction |
| Obtainable demand | serviceable demand × capture fraction |
| Scheduled annual hours | shifts/day × hours/shift × production days |
| Technical saleable capacity | kg/running-hour × scheduled hours × availability × performance × quality yield |
| Sold kg | min(obtainable demand, technical saleable capacity) |
| Net realized price | invoice price/kg × (1 − channel deduction fraction) |
| Variable cost per sold kg | input and conversion cost/kg ÷ quality yield + packaging/logistics/kg |
| Unit contribution | net price − variable cost per sold kg |
| Operating contribution | sold kg × unit contribution − annual cash fixed cost |
| Operating break-even kg | fixed cost ÷ unit contribution, only if unit contribution > 0 |
| Working capital | revenue × receivable days/365 + variable COGS × (inventory days − payable days)/365 |
| Annual free cash flow | operating contribution − change in working capital − capital expenditure |
| Project NPV | − initial capital + sum(year t free cash flow ÷ (1 + discount rate)^t) |

Quality yield reduces both available output and increases the pre-yield cost allocated to good units. The pre-yield cost is material plus variable conversion; post-yield packaging/logistics is charged only to sold good kilograms. This deliberately excludes raw-material use for unsold manufactured stock: production is assumed to follow sales with no finished-goods accumulation other than the working-capital approximation. Add inventory mass-balance logic before modeling build-ahead production.

## Cases and diagnostics

Downside/base/upside vary account capture, net price, process availability, yield, variable inputs, fixed cost, and initial capital together. They are designed scenarios with no assigned probabilities. Review `results/scenarios.csv` for bottleneck, revenue, contribution, and break-even feasibility. Break-even is feasible only if both demand and technical capacity exceed required volume.

The two-dimensional sensitivity holds the base configuration constant and varies invoice price and availability. It does not hold volume constant: availability affects output only when capacity constrains sales. Flat regions are meaningful evidence that another constraint controls the result.

## Uncertainty exploration

A fixed-seed simulation draws triangular distributions for price, capture, availability, and input cost within declared ranges. Other inputs remain base-case values. Inputs are independent by design; this is a limitation because premium price may reduce adoption and supplier cost can correlate with scale. Report quantiles and the fraction of draws above zero as **model-implied under these assumptions**, never as a calibrated probability of market success.

Use the coherent downside case alongside the simulation to avoid treating independent draws as a comprehensive stress test. Prioritize collecting evidence on the inputs that change the decision; wider distributions do not repair missing market evidence.

## Capital and cash

The five-year case applies a declared revenue/volume ramp to steady-state sold volume, holds fixed costs constant, adds maintenance capital annually, and recovers working capital at the end of year five. Year-one working capital starts at zero; its increase is charged in year one. Terminal working-capital recovery assumes orderly collection/liquidation at book value. There is no salvage value and no terminal business value. Capital estimates must include installation, facilities, testing, and contingency before use in an investment case.

Simple payback uses undiscounted cumulative free cash flow after initial capital and is absent if recovery does not occur within the horizon. It is not the same as accounting break-even. A positive operating contribution can coexist with negative NPV.

## Validation and replacement plan

Obtain a written foodservice price and channel deduction schedule; measured weekly reorder quantity; a complete delivered ingredient bill; repeated line trials including sanitation; product-specific yield and rejection data; equipment and installation quotes; buyer payment terms; and validated shelf life. Attach source IDs to each replacement assumption. A spreadsheet or notebook result is no stronger than these inputs.
