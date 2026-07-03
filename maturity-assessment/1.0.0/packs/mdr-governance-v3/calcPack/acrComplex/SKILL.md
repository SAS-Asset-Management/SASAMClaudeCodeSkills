# Calc engine: ACR — Complex Method

Reference implementation of the Complex ACR calculation profile from the MDR
standard, Section 4.5.6.2 (Equations 4, 5, 6). Used for asset subclasses where
the asset is decomposed into elements (construction, linear, or component
element definitions) and renewal decisions consider the distribution of element
conditions, not just the worst defect.

## When to invoke

- A franchisee submission contains assets scored under the Complex ACR method
  (element decomposed subclasses per MDR standard Section 8; see
  `calcPack/methodIndex.yaml` for routing).
- A declared asset level `ACR` needs validating against the underlying element
  and defect data.

## Method (MDR standard Section 4.5.6.2)

For each element:

1. Assign DCR_raw per the subclass DCR table for each defect.
2. Adjust for component criticality (Equation 4): `DCR_cc = DCR_raw` when
   `CC < 3`; `DCR_raw + 1` when `CC >= 3` or CC is unassigned.
3. Adjust DCR_cc for renewal mode using Table 9 to give DCR_adjust.
4. `AECR = max(DCR_adjust)` across the element's defects (Equation 5).
5. Floor: an element with no defects, or AECR of 0, takes AECR = 1.
6. Inaccessible elements take AECR = -1 and are excluded from the rollup.

For the asset:

7. Take the CDF of AECR values (excluding -1).
8. `ACR` is the AECR at the 80th percentile (Equation 6).

## 80th percentile interpretation

This engine implements the inverse empirical CDF at the 0.80 threshold: ACR is
the smallest AECR value `v` such that the proportion of inspected elements
with AECR at or below `v` is at least 0.80. With `n` inspected elements and
AECRs sorted ascending, the zero based index is `ceil(0.80 * n) - 1`. AECRs
are integer scores, so no interpolation is applied. If the standard's Figure 6
is read to imply a different quantile convention, this needs review.

The rationale in the standard: complex assets are renewed in targeted partial
renewals, so a single bad element should not condemn the whole asset — the
rollup considers the distribution of condition across elements.

## Files

| File | Purpose |
| --- | --- |
| `calculate.py` | `acr_complex(elements)`, `aecr_for_element(defects)`, percentile helper, CSV ingest, CLI |
| `tests/test_calculate.py` | Equations 4, 5, 6, percentile boundaries, worked examples, fixture validation |
| `tests/fixtures/workedExamples.json` | Scenario set with expected AECR distributions and ACRs |
| `tests/fixtures/sampleAsset.csv` | Synthetic Acme Rail joined element and defect sample |

## Usage

```bash
python3 calculate.py aecr --defects "3,4,3;2,1,2"
python3 calculate.py compute --spec assets/spec.json
python3 calculate.py validate path/to/submission.csv --report discrepancyReport.csv
```

`compute` and `aecr` print `key: value` lines. `validate` checks declared ACR
per asset and declared AECR per element, writes a discrepancy CSV, and exits 0
when clean, 1 otherwise.

## Report ready examples

`report_examples(discrepancies, max_n=2)` surfaces one asset level and one
element level discrepancy where both exist, so the reviewer can quote a top
down and a bottom up failure mode. Each example carries ids, declared and
computed values, direction, an MDR citation, and a quote ready narrative.

## Dependencies

Consumes the sibling `defectScoring` engine (loaded by file path) for per
defect DCR_cc and DCR_adjust under the complex rule.

## Source citations

- Equation 4 (DCR_cc, Complex) — MDR §4.5.6.2 (p22)
- Equation 5 (AECR = max DCR_adjust) — MDR §4.5.6.2 (p22)
- Equation 6 (ACR = AECR at the 80th percentile) — MDR §4.5.6.2 (p22)
- Table 9 (RMC adjustment) — MDR §4.5.5 (p20)
- Element definitions — MDR §4.5.1 (pp16 to 18)

## Out of scope

Subclasses with bespoke statistical AECR paths from continuous measurements
(MDR standard Sections 8.2 and 8.3) — declared as not implemented in the pack
coverage manifest.
