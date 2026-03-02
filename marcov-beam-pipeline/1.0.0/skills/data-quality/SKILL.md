---
name: MBP:data-quality
description: Analyse raw data quality using the ABS Data Quality Framework (7 dimensions). Use when the user asks to assess data quality, review a dataset, check data fitness for purpose, produce a data quality report, or evaluate data before analysis. Generates a structured markdown report covering institutional environment, relevance, timeliness, accuracy, coherence, interpretability, and accessibility.
---

# Data Quality Analysis Skill

Analyse raw data against the Australian Bureau of Statistics (ABS) Data Quality Framework and produce a structured quality report. Based on ABS Catalogue No. 1520.0 — ABS Data Quality Framework, May 2009.

## Overview

This skill assesses data quality across the seven dimensions of the ABS Data Quality Framework:

1. **Institutional Environment** — Who collected the data and under what authority?
2. **Relevance** — Does the data measure what we need it to measure?
3. **Timeliness** — How current is the data?
4. **Accuracy** — How well does the data describe reality?
5. **Coherence** — Is the data internally consistent and comparable with other sources?
6. **Interpretability** — Can users understand and correctly use the data?
7. **Accessibility** — Can users find and access the data in a suitable format?

The output is a standalone markdown report that can be used directly or populated into a formal quality declaration document.

---

## Discovery Process (CRITICAL)

**Before analysing any dataset, you MUST conduct a discovery interview to understand the data and its context.**

### Questions to Ask

1. **Data Source & Ownership**
   - What is the dataset? (file path, URL, database table, API endpoint)
   - Who collected or produced this data?
   - Under what authority or mandate was it collected? (legislation, contract, internal policy)
   - Is there existing documentation or a data dictionary?

2. **Purpose & Intended Use**
   - What will this data be used for? (analysis, reporting, integration, modelling, decision-making)
   - Who are the intended users of this data?
   - What decisions will be informed by this data?
   - Are there specific questions this data needs to answer?

3. **Data Context**
   - What is the reference period? (when does the data relate to?)
   - When was the data collected or extracted?
   - How frequently is this data updated?
   - Has the data been through any prior cleaning or transformation?

4. **Known Issues**
   - Are there any known data quality concerns?
   - Have there been changes in collection methodology over time?
   - Are there known gaps or exclusions in the population/sample?

5. **Quality Expectations**
   - What level of quality is required for the intended use?
   - Are there specific dimensions of quality that are more critical than others?
   - Is there a downstream formal report or quality declaration this will feed into?

### If the User Provides a File Directly

If the user provides a data file without context, proceed with what can be determined from the data itself and clearly note assumptions and unknowns in the report. Mark dimensions that cannot be assessed without external context as "Unable to assess — requires additional context" and list the specific information needed.

---

## Analysis Workflow

### Phase 1: Data Ingestion & Profiling

Load and inspect the data to establish a foundational understanding:

1. **Read the data** — Load the file (CSV, Excel, JSON, Parquet, database query result, etc.)
2. **Schema inspection** — Document column names, data types, and structure
3. **Row/record counts** — Total records, unique records, duplicate detection
4. **Descriptive statistics** — For numeric fields: min, max, mean, median, std dev, quartiles
5. **Value distributions** — For categorical fields: unique values, frequency counts, top values
6. **Missing data analysis** — Null/blank counts and percentages per column
7. **Sample records** — Display first few rows and any anomalous rows

### Phase 1b: Column-Level Quality Scorecard

After initial profiling, compute a per-column quality scorecard. This quantifies six quality metrics for every column, producing a single table that gives the user an immediate, measurable view of data quality before the narrative dimension assessments.

#### The Six Column Metrics

| Metric | Definition | How to Calculate | Scale |
|---|---|---|---|
| **Completeness** | Proportion of non-null, non-blank values | `(total - nulls - blanks) / total * 100` | 0–100% |
| **Validity** | Proportion of values that conform to the expected domain (type, range, format) | `valid_values / non_null_values * 100` | 0–100% |
| **Consistency** | Proportion of values that match the dominant format/pattern within the column | `values_matching_dominant_pattern / non_null_values * 100` | 0–100% |
| **Uniqueness** | Proportion of distinct values relative to total non-null values | `unique_values / non_null_values * 100` | 0–100% |
| **Timeliness** | For date/time columns: recency score based on how current the most recent value is. For non-date columns: mark as N/A | See timeliness calculation below | 0–100% or N/A |
| **Accuracy** | Proportion of values that are plausible (not impossible, not extreme outliers) | `(non_null - impossible - outliers) / non_null * 100` | 0–100% |

#### Metric Calculation Details

**Completeness:**
```python
completeness = (len(df) - df[col].isna().sum() - (df[col] == '').sum()) / len(df) * 100
```
- Count both `NaN`/`None` AND empty strings/whitespace-only values as incomplete
- For numeric columns, also count sentinel values (e.g., -999, 9999) if identified as placeholders

**Validity:**
Assess whether values conform to the expected domain for the column type:
- **Numeric columns**: values within a plausible range (not negative where impossible, within min/max bounds if known)
- **Date columns**: valid date format, not in the future (unless expected), not before a reasonable minimum
- **Categorical columns**: values belong to the expected set of categories (if known), or are not obviously erroneous
- **String columns**: values match expected format (e.g., email regex, phone pattern, postcode format)
- **Identifier columns**: values match the expected pattern (e.g., `WO-YYYY-NNNNN`)

```python
# Example for a numeric column that should be positive
valid = df[col].dropna().between(0, upper_bound).sum()
validity = valid / df[col].notna().sum() * 100
```

**Consistency:**
Detect the dominant format/pattern and measure adherence:
- **Date columns**: what percentage use the same date format? (e.g., YYYY-MM-DD vs DD/MM/YYYY vs mixed)
- **Categorical columns**: case consistency (e.g., "Active" vs "active" vs "ACTIVE"), trailing spaces, encoding issues
- **Numeric columns**: consistent precision/decimal places, consistent units
- **String columns**: consistent casing convention, consistent delimiters

```python
# Example: check case consistency for a categorical column
values = df[col].dropna()
dominant_case = values.apply(str.title)  # or str.lower, str.upper
consistency = (values == dominant_case).sum() / len(values) * 100
```

**Uniqueness:**
```python
uniqueness = df[col].nunique() / df[col].notna().sum() * 100
```
- For identifier/key columns, uniqueness should be 100% — flag if not
- For categorical columns, low uniqueness is expected and normal — interpret in context
- This metric is informational; low uniqueness is not inherently bad

**Timeliness:**
Only applicable to date/datetime columns. Calculate as a recency score:
```python
# For date columns: how recent is the most recent value?
if col is date type:
    max_date = df[col].max()
    days_since = (assessment_date - max_date).days
    # Score: 100% if within 30 days, decaying linearly to 0% at 365+ days
    timeliness = max(0, 100 - (days_since / 365 * 100))
else:
    timeliness = "N/A"
```

**Accuracy:**
Combine impossible value detection and outlier detection:
```python
non_null = df[col].notna().sum()
impossible = count_impossible_values(df[col])  # domain-specific rules
outliers = count_outliers_iqr(df[col])          # IQR method for numeric
accuracy = (non_null - impossible - outliers) / non_null * 100
```

Impossible value rules (apply based on column semantics):
- Ages: negative or > 150
- Dates: before 1900 or after assessment date (unless future dates are valid)
- Percentages: < 0 or > 100
- Costs/prices: negative (unless refunds are valid)
- Hours: negative or exceeding plausible maximums
- Counts: negative or non-integer

#### Column Quality Scorecard Table

Present the results in this format:

```markdown
| Column | Completeness | Validity | Consistency | Uniqueness | Timeliness | Accuracy | Issues |
|---|---|---|---|---|---|---|---|
| column_name | 98.5% | 99.2% | 100.0% | 45.3% | N/A | 97.8% | 23 outliers |
```

- Use colour-coded indicators in the Issues column to highlight problems
- Bold any metric below the thresholds defined below

#### Quality Thresholds

| Metric | HIGH (Green) | ADEQUATE (Amber) | LOW (Red) |
|---|---|---|---|
| Completeness | >= 95% | 80–94% | < 80% |
| Validity | >= 98% | 90–97% | < 90% |
| Consistency | >= 95% | 80–94% | < 80% |
| Uniqueness | Context-dependent | Context-dependent | Context-dependent |
| Timeliness | >= 80% | 50–79% | < 50% |
| Accuracy | >= 95% | 85–94% | < 85% |

**Note on Uniqueness**: Uniqueness thresholds depend on the column's role:
- **Primary key / identifier**: should be 100% — anything less indicates duplicates
- **Categorical / classification**: low uniqueness is expected (e.g., 5 asset classes across 12,000 rows = 0.04%)
- **Free text / measurement**: moderate to high uniqueness is normal

#### Column Quality Summary Score

After computing all six metrics per column, derive a summary score for each column:

```
Column Score = weighted average of applicable metrics
```

Default weights (adjustable based on user priorities):
- Completeness: 30%
- Validity: 25%
- Accuracy: 25%
- Consistency: 15%
- Uniqueness: 5% (only for identifier columns, otherwise 0% and redistribute)
- Timeliness: 0% for non-date columns (redistribute to others)

Present an overall dataset quality score as the average of all column scores.

#### Python Code for Column Scorecard

```python
import pandas as pd
import numpy as np

def column_quality_scorecard(df, date_cols=None, id_cols=None, assessment_date=None):
    """Compute per-column quality metrics for a DataFrame."""
    if assessment_date is None:
        assessment_date = pd.Timestamp.now()
    if date_cols is None:
        date_cols = []
    if id_cols is None:
        id_cols = []

    results = []

    for col in df.columns:
        n = len(df)
        non_null = df[col].notna().sum()
        nulls = df[col].isna().sum()

        # Completeness
        blanks = 0
        if df[col].dtype == 'object':
            blanks = df[col].fillna('').apply(lambda x: str(x).strip() == '').sum() - nulls
            blanks = max(blanks, 0)
        completeness = (n - nulls - blanks) / n * 100 if n > 0 else 0

        # Uniqueness
        uniqueness = df[col].nunique() / non_null * 100 if non_null > 0 else 0

        # Validity, Consistency, Accuracy — compute per data type
        validity = np.nan
        consistency = np.nan
        accuracy = np.nan
        timeliness = "N/A"
        issues = []

        if pd.api.types.is_numeric_dtype(df[col]):
            vals = df[col].dropna()
            # Validity: check for negative values in columns that should be positive
            # (apply domain-specific rules as needed)
            validity = 100.0  # default; override with domain rules

            # Consistency: check precision consistency
            if len(vals) > 0:
                decimals = vals.apply(lambda x: len(str(x).split('.')[-1]) if '.' in str(x) else 0)
                dominant = decimals.mode().iloc[0] if len(decimals.mode()) > 0 else 0
                consistency = (decimals == dominant).sum() / len(vals) * 100

            # Accuracy: IQR outlier detection
            if len(vals) > 0:
                q1, q3 = vals.quantile(0.25), vals.quantile(0.75)
                iqr = q3 - q1
                outlier_count = ((vals < q1 - 1.5 * iqr) | (vals > q3 + 1.5 * iqr)).sum()
                negative_count = (vals < 0).sum()
                accuracy = (len(vals) - outlier_count) / len(vals) * 100
                if outlier_count > 0:
                    issues.append(f"{outlier_count} outliers")
                if negative_count > 0:
                    issues.append(f"{negative_count} negatives")

        elif col in date_cols or pd.api.types.is_datetime64_any_dtype(df[col]):
            vals = pd.to_datetime(df[col], errors='coerce').dropna()
            valid_dates = len(vals)
            attempted = df[col].notna().sum()
            validity = valid_dates / attempted * 100 if attempted > 0 else 0
            consistency = 100.0  # after parsing; pre-parse format consistency requires string analysis

            # Timeliness
            if len(vals) > 0:
                days_since = (assessment_date - vals.max()).days
                timeliness = f"{max(0, 100 - (days_since / 365 * 100)):.0f}%"

            # Accuracy: future dates, implausible past dates
            future = (vals > assessment_date).sum()
            accuracy = (len(vals) - future) / len(vals) * 100 if len(vals) > 0 else 0
            if future > 0:
                issues.append(f"{future} future dates")

        elif df[col].dtype == 'object':
            vals = df[col].dropna()
            if len(vals) > 0:
                # Validity: non-empty strings
                valid = vals.apply(lambda x: str(x).strip() != '').sum()
                validity = valid / len(vals) * 100

                # Consistency: case consistency check
                title_match = (vals == vals.str.title()).sum()
                lower_match = (vals == vals.str.lower()).sum()
                upper_match = (vals == vals.str.upper()).sum()
                best_match = max(title_match, lower_match, upper_match)
                consistency = best_match / len(vals) * 100

                accuracy = 100.0  # default for strings; override with domain rules

        # Identifier uniqueness check
        if col in id_cols and uniqueness < 100:
            issues.append(f"Duplicate IDs ({100 - uniqueness:.1f}%)")

        if nulls > 0:
            issues.append(f"{nulls} nulls ({nulls/n*100:.1f}%)")

        results.append({
            'Column': col,
            'Completeness': f"{completeness:.1f}%",
            'Validity': f"{validity:.1f}%" if not np.isnan(validity) else "—",
            'Consistency': f"{consistency:.1f}%" if not np.isnan(consistency) else "—",
            'Uniqueness': f"{uniqueness:.1f}%",
            'Timeliness': timeliness,
            'Accuracy': f"{accuracy:.1f}%" if not np.isnan(accuracy) else "—",
            'Issues': "; ".join(issues) if issues else "—"
        })

    return pd.DataFrame(results)
```

### Phase 2: Dimension-by-Dimension Assessment

Assess each of the seven ABS DQF dimensions systematically. For each dimension, provide:

- **Assessment** — A clear narrative assessment
- **Evidence** — Specific findings from the data that support the assessment
- **Rating** — One of: HIGH | ADEQUATE | LOW | UNABLE TO ASSESS
- **Risks** — Identified risks if this dimension is weak
- **Recommendations** — Specific actions to improve quality in this dimension

---

## The Seven Dimensions — Assessment Guide

### Dimension 1: Institutional Environment

*The institutional and organisational factors that influence the credibility and trustworthiness of the data.*

Assess the following (where information is available):

| Sub-element | What to Assess |
|---|---|
| **Mandate for data collection** | Is there a legal, regulatory, or organisational mandate for collecting this data? What legislation, policy, or contract governs the collection? |
| **Adequacy of resources** | Were sufficient resources (staff, systems, budget) available to collect and maintain the data to the required standard? |
| **Quality commitment** | Are there documented quality assurance processes? Is there evidence of data validation, review, or quality control during collection? |
| **Statistical confidentiality** | Are there privacy or confidentiality considerations? Has personally identifiable information (PII) been appropriately handled? Is the data de-identified where required? |

**What to look for in the data itself:**
- Metadata headers or source attribution within the file
- Evidence of data governance (version numbers, timestamps, author fields)
- PII exposure (names, addresses, email addresses, phone numbers, tax file numbers, etc.)
- Signs of automated vs manual data entry (consistency patterns)

**Rating guidance:**
- **HIGH** — Clear provenance, authoritative source, documented governance, no PII concerns
- **ADEQUATE** — Source is known but governance documentation is incomplete
- **LOW** — Unknown source, no governance evidence, PII exposed, or questionable authority
- **UNABLE TO ASSESS** — Insufficient context provided

---

### Dimension 2: Relevance

*How well the data meets the needs of users in terms of concepts measured and populations represented.*

Assess the following:

| Sub-element | What to Assess |
|---|---|
| **Scope and coverage** | Does the data cover the target population? Who or what is included and excluded? Are exclusions likely to cause bias? |
| **Concepts and classifications** | Do the variables/fields measure the right concepts? Are classifications and categories appropriate for the intended use? |
| **Reference period** | Does the reference period align with the user's analytical needs? |
| **User needs alignment** | Does the data contain the fields necessary to answer the user's questions? Are there critical gaps? |

**What to look for in the data itself:**
- Column names and whether they map to the concepts the user needs
- Coverage gaps — are expected categories, time periods, or geographic regions missing?
- Proxy measures — are any fields indirect measures of what is actually needed?
- Granularity — is the data at the right level of detail (e.g., individual vs aggregated)?

**Rating guidance:**
- **HIGH** — Data directly measures required concepts, covers target population, correct reference period
- **ADEQUATE** — Mostly relevant but with minor gaps in coverage or concepts
- **LOW** — Significant misalignment between data content and user needs
- **UNABLE TO ASSESS** — User needs not yet defined

---

### Dimension 3: Timeliness

*The delay between the reference period and data availability, and the currency of the data.*

Assess the following:

| Sub-element | What to Assess |
|---|---|
| **Reference period** | What period does the data relate to? |
| **Collection/extraction date** | When was the data actually collected or extracted? |
| **Lag** | What is the delay between the reference period and the data being made available? |
| **Update frequency** | How often is the data refreshed? Is this sufficient for the intended use? |
| **Currency for intended use** | Is the data current enough for the decisions it will inform? |

**What to look for in the data itself:**
- Date/timestamp columns — most recent and oldest values
- File metadata — creation date, last modified date
- Gaps in time series — missing periods that suggest delays or interruptions
- Stale records — entries that appear outdated relative to the reference period

**Rating guidance:**
- **HIGH** — Data is current, lag is minimal and acceptable for intended use
- **ADEQUATE** — Some delay but still within acceptable bounds for the use case
- **LOW** — Significant lag, data may be too outdated for reliable analysis
- **UNABLE TO ASSESS** — Reference period or extraction dates unknown

---

### Dimension 4: Accuracy

*How well the data correctly describes the phenomena it was designed to measure.*

This is typically the most data-intensive dimension to assess. Evaluate:

| Sub-element | What to Assess |
|---|---|
| **Sampling error** | If the data is a sample, what is the sampling method? What is the margin of error? Is the sample size adequate? |
| **Non-sampling error** | Errors from collection, processing, or coverage — not related to sampling |
| **Coverage error** | Are units in the target population missing from or incorrectly included in the data? |
| **Non-response error** | What proportion of expected responses are missing? Is there a pattern to non-response (systematic bias)? |
| **Response/measurement error** | Are there signs of incorrect values from respondents or measurement instruments? |
| **Processing error** | Are there signs of errors introduced during data entry, coding, editing, or transformation? |

**What to look for in the data itself:**
- **Missing values** — Count and percentage per column; patterns in missingness (MCAR, MAR, MNAR)
- **Outliers** — Values that fall outside expected ranges (use IQR method, z-scores, or domain knowledge)
- **Impossible values** — Negative ages, future dates, percentages > 100%, etc.
- **Duplicates** — Exact duplicate rows or duplicate keys
- **Internal consistency** — Do related fields agree? (e.g., start date before end date, totals matching sum of parts)
- **Data type violations** — Numeric fields containing text, date fields with inconsistent formats
- **Truncation/rounding** — Evidence of precision loss
- **Default/sentinel values** — Suspicious repeated values (e.g., 9999, 0, "N/A", "TBD")

**Rating guidance:**
- **HIGH** — Low missing data (<5%), no impossible values, few outliers, internally consistent
- **ADEQUATE** — Some missing data (5-15%), minor inconsistencies, outliers present but explainable
- **LOW** — High missing data (>15%), impossible values found, significant inconsistencies, unexplained outliers
- **UNABLE TO ASSESS** — Insufficient domain knowledge to evaluate accuracy

---

### Dimension 5: Coherence

*The internal consistency of the data and its comparability with other sources over time.*

Assess the following:

| Sub-element | What to Assess |
|---|---|
| **Internal coherence** | Are aggregations consistent? Do sub-totals sum to totals? Are cross-tabulations consistent? |
| **Temporal coherence** | Is the data consistent over time? Have definitions, classifications, or methods changed between periods? |
| **Cross-source coherence** | Does this data align with other related datasets or published statistics? |
| **Standards alignment** | Does the data use recognised standards, classifications, or coding schemes? (e.g., ANZSIC, ANZSCO, ISO country codes) |

**What to look for in the data itself:**
- Columns that should sum to a total — do they?
- Categories that change names or codes across records or time periods
- Inconsistent units of measurement within the same field
- Fields that contradict each other within the same record
- Comparison with known benchmarks (e.g., ABS published totals, industry standards)

**Rating guidance:**
- **HIGH** — Internally consistent, uses recognised standards, aligns with external sources
- **ADEQUATE** — Minor inconsistencies, mostly uses standards but with some deviations
- **LOW** — Significant internal inconsistencies, no standards used, contradicts external sources
- **UNABLE TO ASSESS** — No external benchmarks available for comparison

---

### Dimension 6: Interpretability

*The availability of information needed to understand and correctly use the data.*

Assess the following:

| Sub-element | What to Assess |
|---|---|
| **Concepts and definitions** | Are all variables clearly defined? Is there a data dictionary? |
| **Classifications and coding** | Are classification schemes documented? Are codes explained? |
| **Collection methodology** | Is the data collection method documented? (survey instrument, administrative form, sensor, etc.) |
| **Data processing** | Are transformations, derivations, and cleaning steps documented? |
| **Known limitations** | Are caveats, limitations, and appropriate use cases documented? |

**What to look for in the data itself:**
- Column naming clarity — are names self-explanatory or cryptic?
- Coded values without a lookup table (e.g., "1", "2", "3" with no label)
- Units of measurement — are they specified? (kg, tonnes, AUD, USD, metres)
- Presence of a header row, metadata rows, or embedded documentation
- Consistency of naming conventions across columns

**Rating guidance:**
- **HIGH** — Comprehensive data dictionary, clear naming, documented methodology and limitations
- **ADEQUATE** — Partial documentation, mostly understandable but some fields need clarification
- **LOW** — No documentation, cryptic column names, unexplained codes, unknown methodology
- **UNABLE TO ASSESS** — Cannot determine without additional metadata

---

### Dimension 7: Accessibility

*The ease with which users can find and access the data in a suitable format.*

Assess the following:

| Sub-element | What to Assess |
|---|---|
| **Discoverability** | Can users easily find that this data exists? Is it catalogued or registered? |
| **Format suitability** | Is the data in a machine-readable, open format? (CSV, JSON, Parquet vs proprietary formats) |
| **Access conditions** | Are there restrictions on access? (authentication, licensing, cost, approvals) |
| **Technical accessibility** | Can the data be easily loaded into common tools? (file size, encoding, structure) |
| **Documentation accessibility** | Is supporting documentation co-located with the data? |

**What to look for in the data itself:**
- File format — open standard or proprietary?
- File size — manageable or requires special handling?
- Encoding — UTF-8 or problematic encoding?
- Structure — well-structured tabular data or requires significant parsing?
- Embedded formatting issues — merged cells in Excel, inconsistent delimiters in CSV

**Rating guidance:**
- **HIGH** — Open format, easily loadable, well-structured, documentation available alongside data
- **ADEQUATE** — Accessible format but minor structural issues, documentation exists but is separate
- **LOW** — Proprietary format, difficult to parse, poorly structured, no documentation
- **UNABLE TO ASSESS** — Data access method unknown

---

## Report Generation

After completing the assessment, generate a **standalone HTML report** using the template in `references/report-template.html`. The report uses SAS-AM branding with light/dark mode, colour-coded scorecard cells, a sidebar navigation, and a print-friendly layout.

### Output Format

The primary output is a **single HTML file** (`data-quality-report.html`) that:
- Can be opened directly in any browser
- Uses CDN fonts (Source Sans Pro, Source Code Pro) and icons (Font Awesome) — no build step
- Includes light/dark mode toggle with localStorage persistence
- Has a print button for PDF export via browser print dialog
- Uses the SAS-AM colour system (SAS Blue #002244 / SAS Green #69BE28)
- Colour-codes scorecard cells: green (HIGH), amber (ADEQUATE), red (LOW)

### Report Structure

The HTML report follows this layout:

1. **Fixed Header** — Report title, theme toggle, print button
2. **Sidebar Navigation** — Jump links to all sections and dimensions
3. **Report Title Section** — Title, subtitle, metadata (dataset, source, date, intended use)
4. **Executive Summary** — Overall score ring, rating badge, dimension summary table
5. **Data Profile** — Stat cards (records, columns, duplicates, etc.) and schema table
6. **Column-Level Quality Scorecard** — Per-column metrics table with colour-coded cells, column summary scores, overall dataset score
7. **Dimension Assessments** (x7) — Cards with assessment, evidence, risks, recommendations
8. **Recommendations** — Grouped as Critical / Important / Minor with numbered items
9. **Appendix** — Profiling code block and ABS framework reference

### Overall Quality Rating

Derive an overall quality rating based on the seven dimension ratings:

| Overall Rating | Criteria |
|---|---|
| **HIGH** | All dimensions rated HIGH or ADEQUATE, with no more than one ADEQUATE |
| **ADEQUATE** | Majority of dimensions rated ADEQUATE or above, no more than one LOW |
| **LOW** | Two or more dimensions rated LOW |
| **CONDITIONAL** | Quality is acceptable for some uses but not others — specify conditions |

### HTML Rating Classes

Use these CSS classes for rating badges and scorecard cells:

| Rating | Badge Class | Cell Class |
|---|---|---|
| HIGH | `rating rating-high` | `cell-high` |
| ADEQUATE | `rating rating-adequate` | `cell-adequate` |
| LOW | `rating rating-low` | `cell-low` |
| UNABLE TO ASSESS | `rating rating-unable` | `cell-na` |

### Score Ring Calculation

The overall score ring in the executive summary uses an SVG circle with `stroke-dashoffset`:

```
circumference = 2 * π * 42 = 264
offset = circumference * (1 - score / 100)
```

For example, a score of 96.4% → offset = 264 * (1 - 0.964) = 9.5

Set `stroke` colour based on rating: `var(--rating-high)` for HIGH, `var(--rating-adequate)` for ADEQUATE, etc.

---

## Workflow Summary

### Step 1: Discovery

Conduct the discovery interview to understand:
- What the data is and where it comes from
- What the user intends to do with it
- What quality concerns exist
- What documentation is available

### Step 2: Data Profiling & Column Scorecard

Load and profile the data:
1. Inspect schema and data types
2. Calculate descriptive statistics
3. Analyse missing data patterns
4. Detect outliers and anomalies
5. Check for duplicates
6. Validate data types and formats
7. **Compute the column-level quality scorecard** (completeness, validity, consistency, uniqueness, timeliness, accuracy per column)
8. Calculate column summary scores and overall dataset quality score

Use Python (pandas, numpy) or the appropriate tool for the data format. Write analysis code in a script file or notebook for reproducibility.

### Step 3: Dimension Assessment

Work through each of the seven dimensions systematically:
- Combine data profiling results with contextual information from discovery
- Assign a rating for each dimension
- Document evidence, risks, and recommendations

### Step 4: Report Generation

Generate the HTML report:
1. Copy the report template from `references/report-template.html`
2. Replace all `{{PLACEHOLDER}}` values with findings
3. Populate scorecard table rows with colour-coded CSS classes (`cell-high`, `cell-adequate`, `cell-low`)
4. Populate dimension cards with assessment, evidence, risks, and recommendations
5. Populate recommendation items grouped by severity
6. Calculate the score ring offset: `264 * (1 - score / 100)`
7. Save as `data-quality-report.html` (or a user-specified filename)

### Step 5: Review & Handover

1. Present the report to the user
2. Highlight critical findings and risks
3. Discuss recommendations and next steps
4. Clarify if the report will feed into a formal quality declaration

---

## Technical Notes

### Supported Data Formats

The skill should handle any data format the user provides:

- **Tabular**: CSV, TSV, Excel (.xlsx, .xls), Parquet, Feather, ORC
- **Structured**: JSON, JSONL, XML
- **Database**: SQL query results, SQLite files
- **Other**: Fixed-width files, SAS datasets (.sas7bdat), Stata (.dta), SPSS (.sav)

### Python Libraries for Profiling

When writing profiling code, prefer these libraries:

```python
import pandas as pd
import numpy as np

# Load data
df = pd.read_csv("data.csv")  # or appropriate reader

# Schema
print(df.dtypes)
print(df.shape)

# Descriptive statistics
print(df.describe(include='all'))

# Missing data
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
print(pd.DataFrame({'missing_count': missing, 'missing_pct': missing_pct}))

# Duplicates
print(f"Duplicate rows: {df.duplicated().sum()}")

# Value distributions for categorical columns
for col in df.select_dtypes(include='object').columns:
    print(f"\n{col}:")
    print(df[col].value_counts().head(10))
```

### Handling Large Datasets

For datasets too large to load fully into memory:
- Use chunked reading (`pd.read_csv(..., chunksize=10000)`)
- Profile a representative sample first
- Note in the report that profiling was done on a sample and state the sample size

---

## Content Guidelines

### Australian English

Use Australian English spelling throughout:
- analyse (not analyze)
- organisation (not organization)
- colour (not color)
- programme (not program, unless referring to software)
- licence (noun) / license (verb)
- centre (not center)

### Tone

- Professional and objective
- Evidence-based — every finding must be supported by data
- Actionable — recommendations should be specific and practical
- Proportionate — focus attention on the dimensions that matter most for the intended use

### Ratings

- Be honest about quality — do not inflate ratings
- Use "UNABLE TO ASSESS" when genuine uncertainty exists rather than guessing
- Always explain the rationale for each rating
- Consider the intended use when assessing fitness for purpose

---

## Framework Reference

**Source**: Australian Bureau of Statistics, *ABS Data Quality Framework*, Catalogue No. 1520.0, May 2009.

The ABS DQF was developed based on:
- Statistics Canada Quality Assurance Framework
- European Statistics Code of Practice

**Key principle**: Quality is fitness for purpose. The same dataset may be high quality for one use and low quality for another. Always assess quality relative to the intended use.

**Trade-offs**: There are inherent trade-offs between dimensions. For example:
- Timeliness vs Accuracy — releasing data faster may reduce time for quality checks
- Accuracy vs Accessibility — more detailed data may be harder to access due to confidentiality
- Relevance vs Coherence — tailoring data to specific needs may reduce comparability

---

## Checklist

Before delivering the report, verify:

- [ ] Discovery interview completed (or assumptions clearly documented)
- [ ] Data successfully loaded and profiled
- [ ] Column-level quality scorecard computed with all six metrics
- [ ] Column summary scores and overall dataset quality score calculated
- [ ] All seven dimensions assessed with ratings
- [ ] Evidence provided for each assessment
- [ ] Risks identified for each dimension
- [ ] Recommendations are specific and actionable
- [ ] Rating summary table included in executive summary
- [ ] Overall quality rating derived and justified
- [ ] Australian English spelling used throughout
- [ ] Report saved as standalone HTML file
- [ ] Light/dark mode toggle works correctly
- [ ] Scorecard cells are colour-coded (green/amber/red)
- [ ] Score ring displays correct percentage and offset
- [ ] Sidebar navigation links to all sections
- [ ] Print layout renders cleanly (test with Ctrl+P)
- [ ] Any analysis code saved for reproducibility
