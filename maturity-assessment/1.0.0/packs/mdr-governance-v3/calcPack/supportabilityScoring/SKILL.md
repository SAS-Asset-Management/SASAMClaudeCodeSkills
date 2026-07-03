# Calc engine: Supportability Scoring (TTI_SUP to SCR)

Reference implementation of the Supportability Condition Rating (SCR)
calculation profile from the MDR standard, Section 4.6 (Equation 7, Figure 7).
Computes the obsolescence horizon for a system from per component
questionnaire outputs, then maps that horizon onto the 1 to 5 SCR banding.

## When to invoke

- A franchisee submission contains supportability data (questionnaire outputs
  feeding the supportability data template) and the declared SCR needs
  validating against the inputs.
- A discrepancy is suspected between declared and recomputed SCR for a system
  grouping.

## Method (MDR standard Section 4.6)

For each component in the system grouping:

1. From the questionnaire, determine `TSE_time` (years to supportability
   expiry) and `S_years` (years of available spares stock), both at least 0.
2. Compute Time to Intervention (Equation 7): `TTI_SUP = TSE_time + S_years`.

For the system:

3. System `TTI_SUP = min(component TTI_SUP)` — the worst supportability
   horizon governs the system rating.
4. Map system TTI_SUP onto the SCR banding (Figure 7):

| SCR | Condition |
| --- | --- |
| 1 | TTI_SUP > 20 years |
| 2 | 14 < TTI_SUP <= 20 years |
| 3 | 8 < TTI_SUP <= 14 years |
| 4 | 3 < TTI_SUP <= 8 years |
| 5 | TTI_SUP <= 3 years |

Banding is right inclusive at the break points 3, 8, 14, and 20 years: a
system with TTI_SUP exactly 20 scores SCR 2, exactly 14 scores 3, exactly 8
scores 4, and exactly 3 scores 5. Components with no obsolescence inputs are
excluded from the rollup.

## Files

| File | Purpose |
| --- | --- |
| `calculate.py` | `tti_sup`, `scr_band`, `scr_for_system`, `validate_csv`, `report_examples`, CLI |
| `tests/test_calculate.py` | Equation 7, Figure 7 banding, boundary cases, fixture validation |
| `tests/fixtures/workedExamples.csv` | Scenario table with expected TTI_SUP and SCR values |
| `tests/fixtures/sampleSystem.csv` | Synthetic Acme Rail system sample with declared SCRs |

## Usage

```bash
python3 calculate.py compute --components "displayPanel,12,5;backlight,4.5,1.5;pcb,8,3"
python3 calculate.py validate path/to/supportability.csv --report discrepancyReport.csv
```

`compute` prints `key: value` lines with a per component trace. `validate`
groups by `system_id`, compares declared to computed SCR, writes a discrepancy
CSV, and exits 0 when clean, 1 otherwise.

## Report ready examples

`report_examples(discrepancies, max_n=2)` returns up to two representative SCR
discrepancies ranked by the declared to computed delta, each naming the
binding component with its TSE_time and S_years, the direction, an MDR
citation, and a quote ready narrative.

## Dependencies

Pure stdlib — no external dependencies.

## Source citations

- Equation 7 (TTI_SUP = TSE_time + S_years) — MDR §4.6 (p24)
- Figure 7 (SCR banding) — MDR §4.6 (p24)
- TTI_SUP description — MDR §4.6 Table 11 (p23)
- Supportability questionnaire — MDR §9 (p339)
- Supportability data template — MDR §10 (p372)

## Out of scope

The questionnaire logic itself, which translates raw component support,
contract, and spares answers into TSE_time and S_years — this engine consumes
the questionnaire outputs as inputs. Software and physical components differ
only in the questionnaire wording; the TTI_SUP and SCR calculation is
identical for both.
