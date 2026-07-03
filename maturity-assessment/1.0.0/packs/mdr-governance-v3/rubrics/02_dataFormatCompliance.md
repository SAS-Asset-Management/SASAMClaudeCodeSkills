# 02 — Data Format Compliance

## Definition

The degree to which submitted MDR data conforms to the interface definition, published schemas, field types, codes, units, and file formats nominated by the receiving authority. Covers structural validity, not semantic accuracy (see 12_consistency and 13_validity for those).

## Evidence Types

- Interface definition document or data schema
- CSV, XML, or JSON schema definitions
- Pre submission validation routines or scripts
- Rejection notices or format feedback from the receiving authority
- Interface mapping between source systems and the MDR specification

## Maturity Ratings

| Level | Rubric |
| --- | --- |
| 0 | No defined format exists, submissions arrive in varying shapes, and rejections by the receiving authority are frequent. |
| 1 | An interface definition exists but is inconsistently applied, with format decisions taken per submission. |
| 2 | The interface definition is mostly applied, format checks are manual, and some fields still deviate from the specification. |
| 3 | All submissions conform to the current interface definition, pre submission validation is carried out, and the interface definition version is tracked. |
| 4 | Automated schema validation runs in the submission pipeline, no format defects have occurred over 12 months, and version change is managed proactively. |
| 5 | The organisation contributes to the evolution of the receiving authority's interface definition and formats are generated automatically from source systems with no manual transformation. |

## Scoring Notes

- Key artefact types: interface definition document, interface mapping register, data supply plan appendix.
- Distinguish format compliance (structural) from data quality (semantic — see the 10_completeness to 15_timeliness subjects).
- A format error that causes a rejection by the receiving authority is stronger evidence than a self declared internal validation pass.
