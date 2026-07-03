# Calc engine: ACR — Simple Method

Reference implementation of the Simple ACR calculation profile from the MDR
standard, Section 4.5.6.1 (Equations 1, 2, 3). Used for asset subclasses where
the renewal decision is driven by the worst single defect rather than a
portfolio of defects (small assets, single asset configurations).

## When to invoke

- A franchisee submission contains assets scored under the Simple ACR method
  (the subclass definitions in MDR standard Section 8 identify which
  subclasses qualify; see `calcPack/methodIndex.yaml` for routing).
- A declared `ACR` value needs validating against the inputs (DCR_raw, CC, RMC
  across all defects on the asset).

## Method (MDR standard Section 4.5.6.1)

1. No defects means ACR = 1 (Equation 1).
2. For each defect, assign DCR_raw per the subclass DCR table (Section 8).
3. Adjust DCR_raw for component criticality (Equation 2): `DCR_cc = 0` when
   `CC < 3`; `DCR_raw + 1` when `CC >= 3` or CC is unassigned.
4. Adjust DCR_cc for renewal mode using Table 9 to give DCR_adjust.
5. `ACR = max(DCR_adjust)` across all defects (Equation 3).
6. If the maximum is 0, ACR = 1 — assets always carry a floor of 1.

The rationale in the standard: for small scale asset types the renewal trigger
is the severity of the worst defect, not the population of defects.

## Files

| File | Purpose |
| --- | --- |
| `calculate.py` | `acr_simple(defects)` plus CSV ingest and validate CLI |
| `tests/test_calculate.py` | Equation 1, Equation 3, boundary cases, fixture validation |
| `tests/fixtures/workedExamples.csv` | Scenario table derived from the standard's equations |
| `tests/fixtures/sampleAsset.csv` | Synthetic Acme Rail defect table for end to end validation |

## Usage

```bash
python3 calculate.py compute --defects '3,4,3;2,1,2;1,4,1'   # DCR_raw,CC,RMC triples
python3 calculate.py validate path/to/submission.csv --report discrepancyReport.csv
```

`compute` prints `key: value` lines with a per defect trace. `validate` groups
rows by `asset_survey_id`, compares declared to computed ACR, writes a
discrepancy CSV, and exits 0 when clean, 1 otherwise.

## Report ready examples

`report_examples(discrepancies, max_n=2)` returns up to two representative ACR
discrepancies ranked by the absolute declared to computed delta, each with the
asset id, direction (overstated or understated), an MDR citation, and a quote
ready narrative.

## Dependencies

Consumes the sibling `defectScoring` engine (loaded by file path) for per
defect DCR_cc and DCR_adjust.

## Source citations

- Equation 1 (no defects means ACR = 1) — MDR §4.5.6.1 (p21)
- Equation 2 (DCR_cc, Simple) — MDR §4.5.6.1 (p21)
- Equation 3 (ACR = max DCR_adjust) — MDR §4.5.6.1 (p21)
- Table 9 (RMC adjustment) — MDR §4.5.5 (p20)
