# Consumer research and experiment design

## Separate the buyers

A distributor assesses margin, service level, and inventory risk. A restaurant buyer assesses cost per plated portion, kitchen throughput, preparation consistency, and diner response. A diner assesses taste, texture, price, and identity. A favorable survey response from one population is not a purchase decision from another.

## Qualitative discovery

Recruit chefs, procurement managers, and distributors across target account types; use a purposive sample and disclose recruitment. Ask about the last alternative-protein purchase, menu removal, rejection reasons, delivery constraints, and actual purchase quantities before presenting the concept. Request anonymized purchase documentation when consent permits. Code interview evidence against a published rubric, retain disconfirming examples, and avoid interpreting interview counts as population prevalence.

Interview guide:

1. Which whole-cut alternatives have you purchased in the last three months, at what pack format and delivered price?
2. What determines removal from or addition to your menu?
3. What are acceptable cook loss, preparation time, shelf life, and storage requirements?
4. What would trigger a second order? What evidence would stop you ordering?
5. Who signs off, and what certification, ingredient, and supplier documents are required?

## Sensory pilot

Compare the printed product with a relevant conventional meat benchmark and a nonprinted alternative. Standardize portion, temperature, seasoning, and cooking endpoint. Randomize serving order; blind branding where feasible; disclose allergens and obtain consent. Record diet pattern and prior alternative-protein exposure without claiming representative segmentation from a convenience sample.

Predeclare one primary endpoint, such as paired overall liking difference, and a smallest commercially meaningful difference. Treat texture, juiciness, aftertaste, and purchase intent as secondary endpoints. Analyze paired differences or a mixed model with participant effects and order covariates; do not apply an independent-samples test to repeated measures. Report effect sizes and intervals, missingness, exclusions, and multiplicity handling. A sensory result is not a shelf-life or safety study.

## Price and positioning experiment

Randomize a genuine posted-price offer across comparable account groups or time blocks, with assignment recorded before outcomes. If randomization occurs at restaurant level, account for clustering. Hold availability and fulfillment constant or explicitly model them. Do not infer willingness to pay from hypothetical survey premiums alone.

Primary commercial metric: contribution per eligible account exposed, including zero-purchase accounts. Report conversion, kilograms/order, repeat order, realized net price, cancellations, refunds, and contribution separately. Price elasticity requires enough randomized price variation and a demand model with credible uncertainty; a few arbitrary price points do not establish a stable elasticity.

A concept-label test can compare “plant-based whole cut” with a truthful printing explanation using identical food. This isolates framing from recipe only if all other treatment elements are held constant. Do not use misleading product descriptions.

## Repeat-order cohorts

Define an account's cohort by first paid delivery. Denominator: all accounts with a complete follow-up window. Measure a second paid delivery within 30 or 60 days, reorder quantity, and net contribution; exclude samples from paid conversion. Display immature cohorts separately. Track customer-level repeated measures and distinguish churn from an account temporarily unable to order.

## Sample-size and stopping rules

Choose power, effect size, baseline variance, cluster correlation, and a maximum observation period before launch. Estimate variance through a small operational pilot, then calculate sample size for the main experiment. Do not invent a required n from the Bitkom survey. Predeclare stopping rules for quality issues, cost limits, and statistical monitoring; repeated unadjusted peeking inflates false positives.

## Practical dataset

Use pseudonymous account and participant IDs. Collect treatment assignment, exposure date, SKU/batch, channel, invoice and deduction values, delivery quantity, returned quantity, preparation details, and response timestamps. Preserve consent and retention rules outside the analytical tables. No personal identifiers are necessary for portfolio examples. Schema and sample analytical queries are in `sql/research.sql`; no fabricated customer results are included.
