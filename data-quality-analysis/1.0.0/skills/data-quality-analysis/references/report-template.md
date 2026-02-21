# Data Quality Report

**Dataset**: {{DATASET_NAME}}
**Source**: {{DATA_SOURCE}}
**Date of Assessment**: {{ASSESSMENT_DATE}}
**Analyst**: {{ANALYST_NAME}}
**Intended Use**: {{INTENDED_USE}}

---

## Executive Summary

{{EXECUTIVE_SUMMARY}}

### Quality Rating Summary

| Dimension | Rating | Key Finding |
|---|---|---|
| 1. Institutional Environment | {{IE_RATING}} | {{IE_FINDING}} |
| 2. Relevance | {{REL_RATING}} | {{REL_FINDING}} |
| 3. Timeliness | {{TIME_RATING}} | {{TIME_FINDING}} |
| 4. Accuracy | {{ACC_RATING}} | {{ACC_FINDING}} |
| 5. Coherence | {{COH_RATING}} | {{COH_FINDING}} |
| 6. Interpretability | {{INT_RATING}} | {{INT_FINDING}} |
| 7. Accessibility | {{ACS_RATING}} | {{ACS_FINDING}} |
| **Overall** | **{{OVERALL_RATING}}** | **{{OVERALL_FINDING}}** |

---

## Data Profile

### Overview

| Attribute | Value |
|---|---|
| File format | {{FILE_FORMAT}} |
| File size | {{FILE_SIZE}} |
| Total records | {{TOTAL_RECORDS}} |
| Total columns | {{TOTAL_COLUMNS}} |
| Duplicate rows | {{DUPLICATE_ROWS}} |
| Date range | {{DATE_RANGE}} |

### Schema

| Column | Data Type | Non-null Count | Null % | Unique Values | Sample Values |
|---|---|---|---|---|---|
| {{COLUMN_NAME}} | {{DATA_TYPE}} | {{NON_NULL}} | {{NULL_PCT}} | {{UNIQUE}} | {{SAMPLES}} |

### Descriptive Statistics (Numeric Columns)

| Column | Min | Max | Mean | Median | Std Dev | Q1 | Q3 |
|---|---|---|---|---|---|---|---|
| {{COLUMN_NAME}} | {{MIN}} | {{MAX}} | {{MEAN}} | {{MEDIAN}} | {{STD}} | {{Q1}} | {{Q3}} |

### Missing Data Summary

| Column | Missing Count | Missing % | Pattern Notes |
|---|---|---|---|
| {{COLUMN_NAME}} | {{MISSING_COUNT}} | {{MISSING_PCT}} | {{PATTERN}} |

---

## Dimension Assessments

### 1. Institutional Environment

**Rating**: {{IE_RATING}}

#### Assessment

{{IE_ASSESSMENT}}

#### Evidence

{{IE_EVIDENCE}}

#### Risks

{{IE_RISKS}}

#### Recommendations

{{IE_RECOMMENDATIONS}}

---

### 2. Relevance

**Rating**: {{REL_RATING}}

#### Assessment

{{REL_ASSESSMENT}}

#### Evidence

{{REL_EVIDENCE}}

#### Risks

{{REL_RISKS}}

#### Recommendations

{{REL_RECOMMENDATIONS}}

---

### 3. Timeliness

**Rating**: {{TIME_RATING}}

#### Assessment

{{TIME_ASSESSMENT}}

#### Evidence

{{TIME_EVIDENCE}}

#### Risks

{{TIME_RISKS}}

#### Recommendations

{{TIME_RECOMMENDATIONS}}

---

### 4. Accuracy

**Rating**: {{ACC_RATING}}

#### Assessment

{{ACC_ASSESSMENT}}

#### Evidence

{{ACC_EVIDENCE}}

#### Risks

{{ACC_RISKS}}

#### Recommendations

{{ACC_RECOMMENDATIONS}}

---

### 5. Coherence

**Rating**: {{COH_RATING}}

#### Assessment

{{COH_ASSESSMENT}}

#### Evidence

{{COH_EVIDENCE}}

#### Risks

{{COH_RISKS}}

#### Recommendations

{{COH_RECOMMENDATIONS}}

---

### 6. Interpretability

**Rating**: {{INT_RATING}}

#### Assessment

{{INT_ASSESSMENT}}

#### Evidence

{{INT_EVIDENCE}}

#### Risks

{{INT_RISKS}}

#### Recommendations

{{INT_RECOMMENDATIONS}}

---

### 7. Accessibility

**Rating**: {{ACS_RATING}}

#### Assessment

{{ACS_ASSESSMENT}}

#### Evidence

{{ACS_EVIDENCE}}

#### Risks

{{ACS_RISKS}}

#### Recommendations

{{ACS_RECOMMENDATIONS}}

---

## Overall Quality Rating

**Rating**: {{OVERALL_RATING}}

{{OVERALL_ASSESSMENT}}

---

## Recommendations

### Critical (Address Before Use)

{{CRITICAL_RECOMMENDATIONS}}

### Important (Address to Improve Quality)

{{IMPORTANT_RECOMMENDATIONS}}

### Minor (Desirable Improvements)

{{MINOR_RECOMMENDATIONS}}

---

## Appendix

### A. Profiling Code

```python
{{PROFILING_CODE}}
```

### B. Detailed Statistics

{{DETAILED_STATISTICS}}

### C. Framework Reference

This assessment was conducted using the Australian Bureau of Statistics Data Quality Framework (ABS Catalogue No. 1520.0, May 2009). The framework comprises seven dimensions of quality: institutional environment, relevance, timeliness, accuracy, coherence, interpretability, and accessibility.

For more information: https://www.abs.gov.au/websitedbs/D3310114.nsf/home/Quality:+The+ABS+data+quality+framework
