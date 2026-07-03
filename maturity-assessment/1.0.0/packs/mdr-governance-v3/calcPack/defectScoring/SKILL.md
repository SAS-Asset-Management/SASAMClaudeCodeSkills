# Calc engine: Defect Scoring (DCR_raw to DCR_cc to DCR_adjust)

Reference implementation of the defect level condition rating cascade from the
MDR standard, Sections 4.5.2 to 4.5.5 (Equations 2 and 4, Table 9). Validates
any declared defect score against the standard.

## When to invoke

- A franchisee submission contains `DCR_raw`, `DCR_cc`, `DCR_adjust` columns
  and the declared outputs need confirming as arithmetically consistent with
  the inputs (Component Criticality, Renewal Mode Criteria).
- A discrepancy is suspected between declared and recomputed defect scores.
- Building a regression truth table for `acrSimple` or `acrComplex` (both
  consume this engine).

Do not use this engine to compute the asset level ACR directly — that is the
job of `acrSimple` or `acrComplex`. This engine stops at `DCR_adjust`.

## Inputs (per defect)

| Field | Type | Range | Source |
| --- | --- | --- | --- |
| DCR_raw | int | 1 to 4 | Subclass specific DCR table, MDR standard Section 8 |
| CC | int | 1 to 4 (or None) | MDR standard Table 7 General Criticality Ratings, or subclass override |
| RMC | int | 1 to 3 | MDR standard Table 8 Renewal Mode Criteria |
| method | enum | simple or complex | MDR standard Sections 4.5.6.1 versus 4.5.6.2 — different DCR_cc formulas |

The standard uses two different DCR_cc formulas depending on the scoring
method; they diverge when `CC < 3`:

- Simple method (Equation 2): `DCR_cc = 0` if `CC < 3`, else `DCR_raw + 1`
- Complex method (Equation 4): `DCR_cc = DCR_raw` if `CC < 3`, else `DCR_raw + 1`

Components without a criticality rating: `DCR_cc = DCR_raw + 1` under both
methods.

## Calculation cascade

### Step 1 — DCR_cc

Simple method (Equation 2): `DCR_cc = 0` when `CC < 3`; otherwise
`DCR_raw + 1`; `DCR_raw + 1` when CC is None.

Complex method (Equation 4): `DCR_cc = DCR_raw` when `CC < 3`; otherwise
`DCR_raw + 1`; `DCR_raw + 1` when CC is None.

### Step 2 — DCR_adjust (MDR standard Table 9)

| DCR_cc | RMC=1 | RMC=2 | RMC=3 |
| --- | --- | --- | --- |
| 1 | 0 | 0 | 1 |
| 2 | 0 | 1 | 2 |
| 3 | 0 | 2 | 3 |
| 4 | 0 | 2 | 4 |
| 5 | 0 | 3 | 5 |

`DCR_cc = 0` is not present in Table 9; where the Simple method drives
`DCR_cc` to 0 (CC < 3), the cascade short circuits to `DCR_adjust = 0` — the
defect cannot drive renewal regardless of RMC.

## Files

| File | Purpose |
| --- | --- |
| `calculate.py` | Pure stdlib reference implementation — `score_defect`, `score_dataframe`, CLI |
| `tests/test_calculate.py` | Pytest harness — full truth table, Table 9 lookup, edge cases |
| `tests/fixtures/truthTable.csv` | Exhaustive 120 row (DCR_raw, CC, RMC, method) truth table |
| `tests/fixtures/sampleSubmissionComplex.csv` | Synthetic Acme Rail sample for end to end validation |

## Usage

```bash
python3 calculate.py compute --dcr 3 --cc 4 --rmc 2 --method complex
python3 calculate.py validate path/to/defects.csv --method complex --report discrepancyReport.csv
```

`compute` prints `key: value` lines. `validate` compares declared `DCR_cc` and
`DCR_adjust` against recomputed values, writes a discrepancy CSV (one row per
disagreement), and exits 0 when clean, 1 otherwise.

## Report ready examples

`report_examples(discrepancies, method, max_n=2)` returns up to two
representative discrepancies in narrative form, suitable for direct quotation
in the maturity report. Selection: largest absolute DCR_adjust delta first,
with a tie breaker preferring distinct error kinds (one DCR_cc driven, one
DCR_adjust only). Each example carries the defect id, declared and computed
values, severity, an MDR citation, and a one sentence quote ready narrative.

## Out of scope

- Subclass specific DCR_raw rules (the subclass tables in MDR standard
  Section 8 that turn a physical observation into the 1 to 4 raw value).
- Statistical DCR derivation for the continuous measurement subclasses (MDR
  standard Sections 8.2 and 8.3) — declared as not implemented in the pack
  coverage manifest.

## Source citations

- Equation 2 — MDR §4.5.6.1 step 3 (p21)
- Equation 4 — MDR §4.5.6.2 step 2 (p22)
- Table 9 (impact of RMC on DCR) — MDR §4.5.5 (p20)
- Defect level data template — MDR §10 (p360)
