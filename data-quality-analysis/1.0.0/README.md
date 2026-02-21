# Data Quality Analysis Skill

Analyse raw data quality using the Australian Bureau of Statistics (ABS) Data Quality Framework and produce a structured markdown report.

## Overview

Based on the ABS Data Quality Framework (Catalogue No. 1520.0, May 2009), this skill assesses data across seven dimensions:

1. **Institutional Environment** — Source credibility and governance
2. **Relevance** — Fitness of concepts and coverage for intended use
3. **Timeliness** — Currency of the data relative to the reference period
4. **Accuracy** — How well the data describes reality (missing values, outliers, duplicates, consistency)
5. **Coherence** — Internal consistency and comparability with other sources
6. **Interpretability** — Availability of metadata and documentation
7. **Accessibility** — Ease of access and format suitability

## What It Does

- Conducts a discovery interview to understand data context and intended use
- Profiles the dataset (schema, statistics, missing data, duplicates, outliers)
- Assesses each of the seven quality dimensions with evidence-based ratings
- Generates a structured markdown report with ratings, risks, and recommendations
- Provides an overall quality rating and prioritised action items

## Output

A standalone markdown file (`data-quality-report.md`) containing:

- Executive summary with quality rating table
- Data profile with schema and statistics
- Seven dimension assessments with ratings (HIGH / ADEQUATE / LOW / UNABLE TO ASSESS)
- Prioritised recommendations (Critical / Important / Minor)
- Appendix with profiling code for reproducibility

## Usage

Ask Claude Code to assess a dataset:

```
Analyse the data quality of sales_data.csv
```

```
Run a data quality assessment on the customer database export
```

```
/data-quality-analysis Review this dataset before we start the analysis
```

## Supported Formats

CSV, Excel, JSON, Parquet, Feather, XML, SQLite, SAS (.sas7bdat), Stata (.dta), SPSS (.sav), and more.

## Framework Reference

Australian Bureau of Statistics, *ABS Data Quality Framework*, Catalogue No. 1520.0, May 2009.
https://www.abs.gov.au/websitedbs/D3310114.nsf/home/Quality:+The+ABS+data+quality+framework

## Licence

MIT

## Author

SAS-AM
