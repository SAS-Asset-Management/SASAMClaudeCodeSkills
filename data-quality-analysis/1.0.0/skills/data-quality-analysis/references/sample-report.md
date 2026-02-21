# Data Quality Report

**Dataset**: fleet_maintenance_records.csv
**Source**: SAS-AM Asset Management Platform (EAM export)
**Date of Assessment**: 2026-02-21
**Analyst**: Claude Code (data-quality-analysis skill)
**Intended Use**: Predictive maintenance modelling for heavy vehicle fleet

---

## Executive Summary

The fleet maintenance records dataset contains 12,847 records across 23 columns covering maintenance events for a heavy vehicle fleet from January 2022 to December 2025. The data is generally fit for purpose but has notable gaps in accuracy and interpretability that should be addressed before use in predictive modelling.

Key concerns are a 22% missing rate in the `failure_mode` column (critical for the intended predictive model), inconsistent units in the `operating_hours` field, and several coded fields without a data dictionary.

### Quality Rating Summary

| Dimension | Rating | Key Finding |
|---|---|---|
| 1. Institutional Environment | ADEQUATE | Known source (EAM system), but no documented data governance process |
| 2. Relevance | HIGH | Data directly covers the target fleet and maintenance concepts needed |
| 3. Timeliness | HIGH | Data is current to December 2025, extracted January 2026 |
| 4. Accuracy | LOW | 22% missing in key field, 147 impossible values, 312 duplicates |
| 5. Coherence | ADEQUATE | Mostly internally consistent but `cost_aud` totals don't match summary records |
| 6. Interpretability | LOW | 6 coded columns with no data dictionary, cryptic column names |
| 7. Accessibility | HIGH | Standard CSV format, UTF-8 encoded, 4.2 MB file size |
| **Overall** | **CONDITIONAL** | **Suitable for exploratory analysis; requires cleaning before predictive modelling** |

---

## Data Profile

### Overview

| Attribute | Value |
|---|---|
| File format | CSV (comma-delimited) |
| File size | 4.2 MB |
| Total records | 12,847 |
| Total columns | 23 |
| Duplicate rows | 312 (2.4%) |
| Date range | 2022-01-03 to 2025-12-18 |

### Schema

| Column | Data Type | Non-null Count | Null % | Unique Values | Sample Values |
|---|---|---|---|---|---|
| work_order_id | string | 12,847 | 0.0% | 12,535 | WO-2024-00142, WO-2024-00143 |
| asset_id | string | 12,847 | 0.0% | 487 | HV-001, HV-002, HV-489 |
| asset_class | string | 12,847 | 0.0% | 5 | Truck, Excavator, Loader, Grader, Roller |
| event_date | date | 12,831 | 0.1% | 1,289 | 2024-06-15, 2024-07-22 |
| completion_date | date | 12,104 | 5.8% | 1,156 | 2024-06-17, 2024-07-25 |
| maintenance_type | string | 12,847 | 0.0% | 3 | Preventive, Corrective, Emergency |
| failure_mode | string | 10,021 | 22.0% | 48 | Engine overheating, Hydraulic leak |
| priority | int | 12,847 | 0.0% | 4 | 1, 2, 3, 4 |
| operating_hours | float | 11,903 | 7.3% | 8,421 | 1250.5, 3400.0, 87200.0 |
| cost_aud | float | 12,512 | 2.6% | 4,891 | 450.00, 12350.75, 0.00 |
| technician_code | string | 12,847 | 0.0% | 34 | T01, T02, T34 |
| location_code | string | 12,801 | 0.4% | 12 | LOC-A, LOC-B, LOC-M |
| parts_used | string | 9,245 | 28.0% | 892 | "Filter, Oil; Belt, Drive" |

### Descriptive Statistics (Numeric Columns)

| Column | Min | Max | Mean | Median | Std Dev | Q1 | Q3 |
|---|---|---|---|---|---|---|---|
| operating_hours | -12.0 | 87,200.0 | 4,521.3 | 3,890.0 | 2,104.7 | 2,650.0 | 5,780.0 |
| cost_aud | 0.00 | 245,000.00 | 2,847.50 | 890.00 | 8,421.30 | 285.00 | 2,450.00 |
| priority | 1 | 4 | 2.1 | 2 | 0.9 | 1 | 3 |

### Missing Data Summary

| Column | Missing Count | Missing % | Pattern Notes |
|---|---|---|---|
| failure_mode | 2,826 | 22.0% | Predominantly missing for "Preventive" maintenance type (systematic) |
| parts_used | 3,602 | 28.0% | Missing across all maintenance types (possibly not recorded) |
| operating_hours | 944 | 7.3% | Concentrated in 2022 records (early data collection period) |
| completion_date | 743 | 5.8% | 89% of missing are "Emergency" type (work orders still open?) |
| cost_aud | 335 | 2.6% | Scattered, no clear pattern |
| event_date | 16 | 0.1% | Appears random |
| location_code | 46 | 0.4% | All from a single technician (T17) |

---

## Column-Level Quality Scorecard

Per-column quality metrics quantified across six dimensions. Thresholds: **HIGH** >= 95% | **ADEQUATE** 80–94% | **LOW** < 80% (validity: 98/90; accuracy: 95/85).

### Scorecard

| Column | Completeness | Validity | Consistency | Uniqueness | Timeliness | Accuracy | Issues |
|---|---|---|---|---|---|---|---|
| work_order_id | 100.0% | 100.0% | 100.0% | 97.6% | N/A | 100.0% | Duplicate IDs (2.4%) |
| asset_id | 100.0% | 100.0% | 100.0% | 3.8% | N/A | 100.0% | — |
| asset_class | 100.0% | 100.0% | 100.0% | 0.04% | N/A | 100.0% | — |
| event_date | 99.9% | 99.9% | 100.0% | 10.0% | 95% | 99.9% | 16 nulls (0.1%) |
| completion_date | 94.2% | 99.7% | 100.0% | 9.0% | 92% | **99.4%** | 743 nulls (5.8%); 34 before event_date |
| maintenance_type | 100.0% | 100.0% | 100.0% | 0.02% | N/A | 100.0% | — |
| failure_mode | **78.0%** | 95.2% | **72.4%** | 0.5% | N/A | 95.2% | 2,826 nulls (22.0%); inconsistent casing |
| priority | 100.0% | 100.0% | 100.0% | 0.03% | N/A | 100.0% | — |
| operating_hours | 92.7% | **98.1%** | **88.3%** | 65.5% | N/A | **87.6%** | 944 nulls (7.3%); 23 negatives; 124 extreme values |
| cost_aud | 97.4% | 99.5% | 96.8% | 38.1% | N/A | **93.2%** | 335 nulls (2.6%); 6 implausible outliers |
| technician_code | 100.0% | 100.0% | 100.0% | 0.3% | N/A | 100.0% | — |
| location_code | 99.6% | 100.0% | 100.0% | 0.09% | N/A | 100.0% | 46 nulls (0.4%); all from T17 |
| parts_used | **72.0%** | 98.7% | **76.3%** | 6.9% | N/A | 98.7% | 3,602 nulls (28.0%); inconsistent delimiters |

### Column Summary Scores

Weighted: Completeness 30% | Validity 25% | Accuracy 25% | Consistency 15% | Uniqueness 5%.

| Column | Summary Score | Rating |
|---|---|---|
| work_order_id | 99.9% | HIGH |
| asset_id | 100.0% | HIGH |
| asset_class | 100.0% | HIGH |
| event_date | 99.9% | HIGH |
| completion_date | 97.3% | HIGH |
| maintenance_type | 100.0% | HIGH |
| failure_mode | 84.7% | ADEQUATE |
| priority | 100.0% | HIGH |
| operating_hours | 91.6% | ADEQUATE |
| cost_aud | 96.3% | HIGH |
| technician_code | 100.0% | HIGH |
| location_code | 99.9% | HIGH |
| parts_used | 83.4% | ADEQUATE |

**Overall Dataset Quality Score**: 96.4% (HIGH)

*Note: The overall dataset score is high because the majority of columns are clean. However, the three ADEQUATE columns (`failure_mode`, `operating_hours`, `parts_used`) are critical for the intended predictive modelling use case — the overall score should be interpreted alongside the intended use.*

### Metric Definitions

| Metric | Definition |
|---|---|
| **Completeness** | % of non-null, non-blank values |
| **Validity** | % of values conforming to expected type, range, and format |
| **Consistency** | % of values matching the dominant format/pattern within the column |
| **Uniqueness** | % of distinct values relative to non-null total |
| **Timeliness** | Recency score for date columns (100% = within 30 days); N/A for non-date columns |
| **Accuracy** | % of values that are plausible (excluding impossible values and statistical outliers) |

---

## Dimension Assessments

### 1. Institutional Environment

**Rating**: ADEQUATE

#### Assessment

The data originates from the organisation's enterprise asset management (EAM) system, which is the authoritative source for maintenance records. The EAM platform enforces some data validation at entry (mandatory fields for work order ID, asset ID, maintenance type). However, there is no documented data governance framework, no evidence of periodic data quality audits, and no formal data steward assigned to this dataset.

#### Evidence

- Source system is identified (EAM platform export)
- Mandatory fields (work_order_id, asset_id, maintenance_type) have zero nulls, indicating system-enforced constraints
- No metadata header or version information in the file
- No PII detected in the dataset

#### Risks

- Without documented governance, data quality may degrade over time as staff change
- No audit trail for corrections or amendments to records

#### Recommendations

- Document the data governance process for EAM exports
- Assign a data steward responsible for maintenance data quality
- Add export metadata (extraction date, system version, filters applied) to future exports

---

### 2. Relevance

**Rating**: HIGH

#### Assessment

The dataset directly covers the target population (the organisation's heavy vehicle fleet) and the key concepts needed for predictive maintenance modelling: asset identification, maintenance events, failure modes, operating hours, and costs. The reference period (2022-2025) provides four years of history, which is sufficient for model training.

#### Evidence

- All 487 fleet assets are represented in the data
- Five asset classes align with the fleet register
- Maintenance types cover the three categories required (preventive, corrective, emergency)
- 48 distinct failure modes captured

#### Risks

- The 22% missing rate in `failure_mode` reduces the effective dataset for supervised learning
- `parts_used` is a free-text field that will require parsing/standardisation

#### Recommendations

- Investigate whether missing `failure_mode` values can be retrospectively populated from technician notes or related systems
- Standardise the `parts_used` field using the organisation's parts catalogue codes

---

### 3. Timeliness

**Rating**: HIGH

#### Assessment

The data covers the reference period January 2022 to December 2025 and was extracted in January 2026, representing a lag of approximately one month. This is acceptable for the intended predictive modelling use case, which does not require real-time data.

#### Evidence

- Most recent `event_date`: 2025-12-18
- File creation date: 2026-01-08
- Extraction lag: ~3 weeks
- No gaps in the monthly distribution of records

#### Risks

- If the model is deployed for real-time predictions, a more frequent data pipeline will be needed

#### Recommendations

- For production deployment, establish an automated daily or weekly export pipeline
- Document the expected refresh frequency in the data catalogue

---

### 4. Accuracy

**Rating**: LOW

#### Assessment

Several accuracy issues were identified that require remediation before the data can be used for predictive modelling. There are impossible values in `operating_hours` (negative values and implausibly high values), 312 duplicate records, and systematic missingness in the `failure_mode` field that introduces bias.

#### Evidence

- **Impossible values**: 23 records have negative `operating_hours` (min: -12.0); 124 records exceed 50,000 hours (implausible for the asset age)
- **Duplicates**: 312 exact duplicate rows (2.4% of total records) — likely a data extraction issue
- **Systematic missingness**: `failure_mode` is missing for 82% of "Preventive" maintenance records — this is expected (no failure for planned maintenance) but needs to be handled explicitly in modelling
- **Outliers in cost**: 18 records with `cost_aud` > $100,000 — 12 appear legitimate (major overhauls), 6 appear to be data entry errors (costs of $245,000 for routine filter changes)
- **Date inconsistencies**: 34 records where `completion_date` is before `event_date`

#### Risks

- Negative operating hours will cause errors in feature engineering
- Duplicate records will inflate maintenance frequency calculations
- Biased missingness in `failure_mode` will produce a biased predictive model if not addressed
- Cost outliers will skew financial analysis

#### Recommendations

- Remove or correct 312 duplicate rows
- Investigate and correct 23 negative `operating_hours` values
- Cap or investigate 124 records with `operating_hours` > 50,000
- Fix 34 records where completion date precedes event date
- Investigate 6 cost outliers on routine maintenance work orders
- For `failure_mode` missingness: explicitly code preventive maintenance records as "N/A — Planned" rather than leaving them null

---

### 5. Coherence

**Rating**: ADEQUATE

#### Assessment

The data is mostly internally coherent with some notable exceptions. Asset class values are consistent throughout, and maintenance type distributions are plausible. However, cost totals for some work orders do not reconcile with summary records, and there is an inconsistency in `operating_hours` units between older and newer records.

#### Evidence

- Asset classes are consistent across all records (5 distinct values matching fleet register)
- Maintenance type distribution is plausible: Preventive 45%, Corrective 42%, Emergency 13%
- `operating_hours` appears to be recorded in different units for pre-2023 records (some appear to be in minutes rather than hours)
- 89 records have `cost_aud = 0.00` for corrective maintenance — inconsistent with having parts listed

#### Risks

- Mixed units in `operating_hours` will produce incorrect model features
- Zero-cost corrective records may indicate incomplete cost capture

#### Recommendations

- Investigate the `operating_hours` unit inconsistency for pre-2023 records and normalise to a single unit
- Review zero-cost corrective maintenance records to determine if costs were not captured

---

### 6. Interpretability

**Rating**: LOW

#### Assessment

The dataset lacks a data dictionary and several columns use coded values without documentation. While some column names are self-explanatory (`event_date`, `cost_aud`), others require domain knowledge or documentation to interpret correctly (`priority` codes, `technician_code`, `location_code`).

#### Evidence

- No data dictionary provided with the export
- `priority` uses codes 1-4 with no label (is 1 highest or lowest priority?)
- `technician_code` (T01-T34) has no mapping to names or roles
- `location_code` (LOC-A through LOC-M) has no mapping to physical locations
- `failure_mode` values appear to be free-text with inconsistent capitalisation ("Engine overheating" vs "engine overheating" vs "ENGINE OVERHEATING")
- Units for `operating_hours` not specified in column name or header
- Units for `cost_aud` are implied by column name (AUD) but not explicitly documented

#### Risks

- Without knowing the priority scale direction, any priority-based analysis could be inverted
- Coded fields cannot be used meaningfully in analysis without lookup tables
- Inconsistent `failure_mode` text will inflate the number of categories

#### Recommendations

- Create and maintain a data dictionary for all EAM exports
- Provide lookup tables for `priority`, `technician_code`, and `location_code`
- Standardise `failure_mode` values (consistent casing, controlled vocabulary)
- Include units of measurement in column names or a metadata header

---

### 7. Accessibility

**Rating**: HIGH

#### Assessment

The data is provided as a standard CSV file with UTF-8 encoding, readily loadable in all common data analysis tools. File size is manageable (4.2 MB) and the structure is clean tabular data with a header row.

#### Evidence

- Format: CSV with comma delimiter and standard quoting
- Encoding: UTF-8 (verified, no encoding errors on load)
- File size: 4.2 MB (loads in under 1 second in pandas)
- Structure: single header row, consistent number of columns per row
- No merged cells, embedded images, or complex formatting

#### Risks

- The `parts_used` column contains embedded semicolons within quoted strings, which could cause parsing issues with naive CSV readers

#### Recommendations

- Retain CSV as the export format — it is widely accessible
- Consider also providing a Parquet export for large-scale analytical use
- Co-locate the data dictionary with the data file in future exports

---

## Overall Quality Rating

**Rating**: CONDITIONAL

The dataset is suitable for exploratory analysis and descriptive reporting in its current state. However, it requires cleaning and enrichment before it can be reliably used for predictive maintenance modelling. The critical issues are:

1. Duplicate records must be removed
2. Impossible values in `operating_hours` must be corrected
3. The `failure_mode` missingness pattern must be addressed in the modelling strategy
4. A data dictionary must be created for coded fields

Once these issues are resolved, the dataset quality rating would improve to ADEQUATE.

---

## Recommendations

### Critical (Address Before Use)

1. **Remove 312 duplicate rows** — Deduplicate on `work_order_id` or full row match
2. **Correct impossible `operating_hours` values** — Fix 23 negative values and investigate 124 values exceeding 50,000
3. **Fix 34 date inconsistencies** — Where `completion_date` precedes `event_date`
4. **Create a data dictionary** — Document all columns, codes, and units

### Important (Address to Improve Quality)

5. **Standardise `failure_mode` values** — Normalise casing, consolidate synonyms, apply a controlled vocabulary
6. **Investigate `operating_hours` unit inconsistency** — Pre-2023 records may use different units
7. **Investigate 6 cost outliers** — Verify $100k+ costs on routine work orders
8. **Populate missing `failure_mode`** — Explicitly code preventive maintenance as "N/A — Planned"

### Minor (Desirable Improvements)

9. **Add export metadata** — Include extraction date, system version, and filters in future exports
10. **Provide lookup tables** — For `technician_code`, `location_code`, and `priority`
11. **Automate the export pipeline** — For production model deployment

---

## Appendix

### A. Profiling Code

```python
import pandas as pd
import numpy as np

df = pd.read_csv("fleet_maintenance_records.csv")

# Schema and shape
print(f"Shape: {df.shape}")
print(df.dtypes)
print(df.describe(include='all'))

# Missing data
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
print(pd.DataFrame({'missing_count': missing, 'missing_pct': missing_pct}).sort_values('missing_pct', ascending=False))

# Duplicates
print(f"Duplicate rows: {df.duplicated().sum()}")

# Date validation
df['event_date'] = pd.to_datetime(df['event_date'])
df['completion_date'] = pd.to_datetime(df['completion_date'])
date_issues = df[df['completion_date'] < df['event_date']]
print(f"Completion before event: {len(date_issues)}")

# Operating hours validation
print(f"Negative operating_hours: {(df['operating_hours'] < 0).sum()}")
print(f"Operating_hours > 50000: {(df['operating_hours'] > 50000).sum()}")

# Cost outliers
q1 = df['cost_aud'].quantile(0.25)
q3 = df['cost_aud'].quantile(0.75)
iqr = q3 - q1
outliers = df[(df['cost_aud'] > q3 + 1.5 * iqr)]
print(f"Cost outliers (IQR method): {len(outliers)}")
```

### B. Detailed Statistics

*See profiling code output for full statistical tables.*

### C. Framework Reference

This assessment was conducted using the Australian Bureau of Statistics Data Quality Framework (ABS Catalogue No. 1520.0, May 2009). The framework comprises seven dimensions of quality: institutional environment, relevance, timeliness, accuracy, coherence, interpretability, and accessibility.

For more information: https://www.abs.gov.au/websitedbs/D3310114.nsf/home/Quality:+The+ABS+data+quality+framework
