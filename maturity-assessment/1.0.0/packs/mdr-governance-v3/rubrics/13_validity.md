# 13 — Validity

## Definition

The extent to which field values conform to the allowed range, permitted code set, or specified data type defined in the MDR schema. Covers type checks, range checks, referential integrity, and the schema documentation that defines what is valid.

## Evidence Types

- A schema or data dictionary with allowed types, ranges, and code sets
- Validation rules or scripts applied to submitted data
- Validation report or exception log with counts
- Referential integrity checks against master asset lists
- Remediation records where invalid values were corrected

## Maturity Ratings

| Level | Rubric |
| --- | --- |
| 0 | No schema exists and any value is accepted. |
| 1 | A schema exists informally with no automated checks. |
| 2 | A partial schema exists with some validation on load, and out of range values remain in submissions. |
| 3 | A full schema is published, validation is automated on ingestion, and exceptions are reported and remediated before submission. |
| 4 | Validity metrics are trended, schema updates are version controlled, and root causes of invalid values are analysed. |
| 5 | The schema is jointly managed with the receiving authority and validation runs at source capture, not just on submission. |

## Scoring Notes

- Cross references 02_dataFormatCompliance at the file level and 12_consistency on code usage.
- Key artefact types: interface definition document, data supply plan appendices, minimum data requirement specifications, submitted datasets.
- A value that is valid in isolation may still be invalid against the asset class it is applied to; check referential rules, not just column level rules.
