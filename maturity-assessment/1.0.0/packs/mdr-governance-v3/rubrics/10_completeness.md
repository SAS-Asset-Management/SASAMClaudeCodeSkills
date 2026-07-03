# 10 — Completeness

## Definition

Record level completeness — the proportion of expected condition and defect records actually captured and submitted relative to the defined population of in scope assets. Covers both record count completeness and field level completeness within each record.

## Evidence Types

- A defined expected population by asset count, defect type, and period
- Actual submitted record count against that population
- Field fill rates per column within a submitted dataset
- Documented reasons for missing records or fields
- A reconciliation between source systems and the MDR submission

## Maturity Ratings

| Level | Rubric |
| --- | --- |
| 0 | The expected population is not defined and completeness is unknown. |
| 1 | Submissions are made with no check against an expected count and missing fields are common. |
| 2 | The expected population is partially defined, fill rates are spot checked, and there is no systematic reconciliation. |
| 3 | The population is defined per submission type and record and field level completeness is measured and reported each cycle. |
| 4 | Completeness trends are monitored, root cause analysis is applied to missing data, and targets are set and tracked. |
| 5 | Completeness validation is automated on ingestion with closed loop remediation and external benchmarking. |

## Scoring Notes

- Cross references 03_submissionCompleteness, which operates at the submission package level; this subject is about record and field completeness within each submission.
- Key artefact types: submitted datasets, data supply plan appendices, capture frequency forecasts.
- A file of the right name and format can still be materially incomplete; compare row counts against supply plan expectations.
