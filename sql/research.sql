-- SQLite-compatible proposed schema. No customer records or experimental results are supplied.
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS sources (
 source_id TEXT PRIMARY KEY, title TEXT NOT NULL, url TEXT NOT NULL,
 evidence_class TEXT NOT NULL, reviewed_on TEXT NOT NULL, limitations TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS claims (
 claim_id TEXT PRIMARY KEY, source_id TEXT NOT NULL REFERENCES sources(source_id),
 claim_text TEXT NOT NULL, geography TEXT, product_scope TEXT,
 period_start TEXT, period_end TEXT, verification_status TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS accounts (
 account_id TEXT PRIMARY KEY, segment TEXT NOT NULL, territory TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS deliveries (
 delivery_id TEXT PRIMARY KEY, account_id TEXT NOT NULL REFERENCES accounts(account_id),
 delivered_on TEXT NOT NULL, sku TEXT NOT NULL,
 sold_kg REAL NOT NULL CHECK(sold_kg>0),
 net_revenue_usd REAL NOT NULL, variable_cost_usd REAL NOT NULL,
 is_paid INTEGER NOT NULL CHECK(is_paid IN (0,1))
);
-- 60-day paid reorder, mature cohorts only. Supply a fixed :as_of date (YYYY-MM-DD).
-- Multiple deliveries on the same date do not count as a later reorder.
WITH first_paid AS (
 SELECT account_id,MIN(delivered_on) AS first_date
 FROM deliveries WHERE is_paid=1 AND delivered_on<=:as_of GROUP BY account_id
), mature AS (
 SELECT * FROM first_paid WHERE date(first_date,'+60 days')<=date(:as_of)
), outcomes AS (
 SELECT m.account_id,m.first_date,
 EXISTS(SELECT 1 FROM deliveries d WHERE d.account_id=m.account_id AND d.is_paid=1
 AND d.delivered_on>m.first_date AND date(d.delivered_on)<=date(m.first_date,'+60 days')) AS reordered
 FROM mature m
)
SELECT substr(first_date,1,7) AS first_delivery_month,COUNT(*) AS mature_accounts,
 SUM(reordered) AS reordered_accounts,AVG(reordered*1.0) AS reorder_rate
FROM outcomes GROUP BY 1;
-- Contribution weighted by sold kilograms; do not average per-delivery margin percentages.
SELECT sku,SUM(sold_kg) AS kg,SUM(net_revenue_usd) AS revenue_usd,
 SUM(net_revenue_usd-variable_cost_usd)/NULLIF(SUM(sold_kg),0) AS contribution_usd_per_kg
FROM deliveries WHERE is_paid=1 GROUP BY sku;
