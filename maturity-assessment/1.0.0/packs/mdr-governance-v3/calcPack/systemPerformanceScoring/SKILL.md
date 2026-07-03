# Calc engine: System Performance Scoring (power law NHPP to SPCR)

Reference implementation of the System Performance Condition Rating (SPCR)
calculation profile from the MDR standard, Section 4.7 (Equations 8 to 12,
Table 12). Fits the Crow AMSAA power law non homogeneous Poisson process to a
stream of failure timestamps for a system grouping, then maps the trend
significance onto the 1 to 5 SPCR banding.

## When to invoke

- A franchisee submission contains failure event data (system performance data
  template) and the declared SPCR for a system grouping needs validating.
- A discrepancy is suspected between declared and recomputed beta, chi
  squared, p, or SPCR.

## Method (MDR standard Section 4.7)

For a system grouping (an asset subclass, an asset type, or a make and model):

1. Collect every functional failure event over the study window.
2. Convert each failure timestamp to `t_i` years since the window start.
3. Define `t_k = max(t_i)` and `m` as the number of failures.
4. Fit the power law model (Equation 8): `M(t) = theta * t^beta`.
5. Beta estimate (Equation 10): `beta = m / (m * ln(t_k) - sum(ln(t_i)))`.
6. Theta estimate (Equation 9): `theta = m / t_k^beta`.
7. If `beta <= 1`, SPCR = 1 (stable or improving); skip the trend test.
8. Trend statistic (Equation 11): `chi2 = 2 * sum_{i=1..m-1} ln(t_k / t_i)`
   with `df = 2 * (m - 1)`.
9. Two sided p value (Equation 12, read as the smaller tail of the chi squared
   CDF): `p = min(F, 1 - F)` where `F = chi2_cdf(chi2, df)`.
10. Map (beta, p) onto SPCR using Table 12:

| SPCR | Condition | Narrative |
| --- | --- | --- |
| 1 | p >= 0.20 or beta <= 1 | No significant evidence, improving, or stable |
| 2 | beta > 1 and 0.20 > p >= 0.10 | Weak evidence of an increase in failure rate |
| 3 | beta > 1 and 0.10 > p >= 0.05 | Some evidence of an increase |
| 4 | beta > 1 and 0.05 > p >= 0.02 | Evidence of an increase |
| 5 | beta > 1 and p < 0.02 | Strong evidence of an increase |

Groups with fewer than two failures floor to SPCR 1 with an insufficient data
rule string.

## Files

| File | Purpose |
| --- | --- |
| `calculate.py` | `fit_power_law`, `spcr_from_failures`, `validate_csv`, `report_examples`, CLI |
| `tests/test_calculate.py` | Equations 9 to 12, Table 12 banding, edge cases, fixture validation |
| `tests/fixtures/workedExamples.json` | Synthetic failure streams with expected beta, chi squared, p, SPCR |
| `tests/fixtures/sampleGroups.csv` | Synthetic Acme Rail failure groups with declared SPCRs |

## Usage

```bash
python3 calculate.py compute --failures "1.2,3.4,5.0,7.1,8.5"
python3 calculate.py validate path/to/failures.csv --report discrepancyReport.csv
```

`compute` prints `key: value` lines. `validate` groups failure rows, compares
declared to computed SPCR, writes a discrepancy CSV, and exits 0 when clean, 1
otherwise.

## Report ready examples

`report_examples(discrepancies, max_n=2)` returns up to two representative
SPCR discrepancies ranked by the declared to computed delta, each with the fit
diagnostics (m, t_k, beta, chi squared, df, p), the matched Table 12 rule, an
MDR citation, and a quote ready narrative.

## Dependencies

Pure stdlib. The chi squared CDF is computed in closed form because the
degrees of freedom, `df = 2(m - 1)`, are always even:
`F(x; 2k) = 1 - exp(-x/2) * sum_{i=0}^{k-1} (x/2)^i / i!`.

## Source citations

- Equation 8 (power law model) — MDR §4.7 (p25)
- Equation 9 (theta estimate) — MDR §4.7 (p25)
- Equation 10 (beta estimate) — MDR §4.7 (p25)
- Equation 11 (chi squared trend statistic) — MDR §4.7 (p26)
- Equation 12 (p value as the smaller tail) — MDR §4.7 (p26)
- Table 12 (SPCR banding) — MDR §4.7 (p26)
- System performance data template — MDR §10 (p379)

## Known interpretations

- The standard writes Equation 12 as `p = min(chi2, 1 - chi2)`, which is non
  standard notation; this engine interprets it as the smaller tail probability
  of the chi squared CDF. If a worked example in the standard implies a
  different convention, this needs review.
- The beta estimator uses the biased maximum likelihood form exactly as the
  standard specifies; the unbiased small sample form is deliberately not
  substituted.
- Continuous measurement subclasses with bespoke statistical paths (MDR
  standard Sections 8.2 and 8.3) are out of scope — declared in the pack
  coverage manifest.
