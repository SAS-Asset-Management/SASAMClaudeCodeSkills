# 12 — Consistency

## Definition

The extent to which codes, units, reference values, and terminology are applied consistently across records, submissions, asset classes, and source systems. Covers controlled vocabularies, reference data management, and reconciliation between systems contributing to MDR submissions.

## Evidence Types

- A reference data dictionary or controlled value list
- Unit of measure standard applied across fields
- Cross system reconciliation of code sets between the asset management system and field capture tools
- Audit of code usage across submissions
- Change control records for reference data updates

## Maturity Ratings

| Level | Rubric |
| --- | --- |
| 0 | Free text is used throughout and no reference data exists. |
| 1 | Some reference lists exist but are duplicated across systems and drift apart. |
| 2 | Reference data is defined for core fields but inconsistencies persist between the asset management system, the master data store, and field capture tools. |
| 3 | A single controlled vocabulary per field applies across every MDR submission and is reconciled across source systems. |
| 4 | A reference data governance group operates change control and monitors usage for drift. |
| 5 | Reference data is a managed master data asset, integrated with supplier and MDR exchange schemas. |

## Scoring Notes

- Cross references 13_validity — consistency underpins validity — and 02_dataFormatCompliance.
- Key artefact types: interface definition document, interface mapping register, master data extracts.
- Consistency within a single file does not mean consistency across the full submission set; check codes, asset identifiers, and units across every submitted file.
