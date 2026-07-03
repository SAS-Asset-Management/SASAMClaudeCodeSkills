# 24 — Data Currency

## Definition

The recency of the most recent assessment record held for each asset. Measured as the age of the current condition record against the defined target interval for that asset class. Covers the portfolio view of how current the network condition picture is.

## Evidence Types

- Last assessed date per asset
- Target interval per asset class
- Age distribution of condition records
- Count or proportion of assets with stale records
- Remediation plan for assets with expired records

## Maturity Ratings

| Level | Rubric |
| --- | --- |
| 0 | The last assessed date is not captured and currency is unknown. |
| 1 | The last assessed date is held in some systems with no currency reporting. |
| 2 | Currency is reported for core asset classes and a significant proportion of records are stale. |
| 3 | Currency is measured across all in scope assets against target intervals and stale records are flagged and remediated on cycle. |
| 4 | Currency is trended, root causes of stale records are analysed, and targeted recovery programmes run. |
| 5 | A near current condition picture is maintained continuously and stale records are exceptional and visible. |

## Scoring Notes

- Cross references 15_timeliness, 23_assessmentFrequency, and 21_assetSubclassCoverage — currency is the portfolio expression of all three.
- Key artefact types: submitted datasets inspected for last assessed dates, inspection data extracts, defect registers.
- An average age can look reasonable while a long tail of very stale assets hides in the distribution; look at the tail, not just the mean.
