# Data dictionary and provenance

| File | Grain | Status | Use |
|---|---|---|---|
| evidence_ledger.csv | One source and supported claim bundle | Reviewed primary/company sources except explicitly blocked L01 | Research provenance |
| assumptions.json | One named scenario configuration plus simulation settings | Illustrative analyst assumptions | Commercial model only |
| consumer_surveys.csv | One published marginal statistic per study/year/group/metric | Bitkom scope corrected to primary release | Descriptive context; not respondent microdata |
| companies.csv | One inherited company profile | Historical, partly unverified | Leads for dated competitive research; not market share |
| market_estimates.csv | One inherited publisher estimate | Unverified legacy scope/methodology | Evidence-quality comparison only |
| timeline.csv | One inherited reported event | Mixed historical and planned milestones | Historical research leads |
| us_state_laws.csv | One selected inherited state/bill record | Historical and incomplete | Not current 50-state legal status |

`sample_size` on survey subgroup rows is the total 2025 study size, not the subgroup denominator; see `sample_size_note`. Separate marginal percentages must not be summed as mutually exclusive categories. Dates in the evidence ledger are review dates, not necessarily publication dates.

Results are generated from assumptions only. `scenarios.csv` contains one annual steady-state result per named scenario; `annual_cashflows.csv` one scenario-year; `price_utilization.csv` one invoice-price/availability pair; `simulation.csv` one illustrative input draw. All money is constant USD, mass kg, timing annual unless a field says days or weeks. Blank break-even or payback fields mean not defined / not achieved, not zero.

No private or personal data are included. Research sources remain owned by their respective publishers; links and paraphrases are provided rather than copied articles.
