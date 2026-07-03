# 11 — Uniqueness

## Definition

The absence of duplicate defect and condition records within and across MDR submissions. Covers primary key definition, deduplication rules, and reconciliation of apparent duplicates that are in fact legitimate recurrences.

## Evidence Types

- Primary key definition for each record type
- Deduplication rules or procedures
- Duplicate detection reports and counts
- A rule set distinguishing duplicates from legitimate recurrences
- Reconciliation records where duplicates were identified and resolved

## Maturity Ratings

| Level | Rubric |
| --- | --- |
| 0 | No primary key exists and duplicates are unknown and unmanaged. |
| 1 | Duplicate detection is ad hoc and occurs only when problems surface. |
| 2 | A primary key is defined in some datasets and manual deduplication runs on some submissions. |
| 3 | Every MDR submission has a defined key, automated duplicate checks run pre submission, and the rules are documented. |
| 4 | Duplicate root causes are tracked to system, process, or assessor, with targeted remediation. |
| 5 | Cross system master data prevents duplicates at source and improvement continues against a measured duplicate rate. |

## Scoring Notes

- Cross references 10_completeness and 13_validity — duplicates inflate apparent completeness and distort validity metrics.
- Key artefact types: submitted datasets, defect registers, deduplication rule documentation.
- Repeat defects on the same asset are not duplicates if the inspection dates differ; the rule set must handle recurrence cleanly.
