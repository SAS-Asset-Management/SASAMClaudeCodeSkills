---
name: sas-amp
description: This skill should be used when the user asks to create, develop, draft, or review an asset management plan (AMP), mentions "sas-amp", requests an ISO 55001-aligned plan, or discusses AMP sections such as levels of service, demand forecasting, renewal planning, lifecycle costing, or financial projections. Covers any sector or asset class.
version: 0.1.0
---

# Asset Management Plan Development Tool

To produce comprehensive, ISO 55001:2024-aligned Asset Management Plans, conduct adaptive user interviews, autonomous research, and data analysis, then generate professional output in both HTML presentation and branded DOCX formats.

## Workflow Overview

The AMP development process follows an adaptive, gap-driven methodology rather than a rigid linear sequence. The overall flow is:

1. **Intake** — Accept whatever the user provides upfront (data files, context, documents, partial plans)
2. **Analysis** — Assess what is covered and what is missing against the full AMP structure
3. **Research** — Dispatch the `amp-researcher` agent to gather regulatory, benchmark, and organisational context
4. **Interview** — Conduct targeted interviews only for identified gaps (one question at a time, multiple-choice where possible)
5. **Data Analysis** — Process any quantitative data through the `amp-data-analyst` agent
6. **Drafting** — Write each AMP section, with per-section review by `amp-asset-context-reviewer`
7. **Output Generation** — Produce both HTML presentation (via `/sas-presentation`) and DOCX (via `generateDocx.py`)

## Working Directory

Create `./sas-amp-working/` in the current project directory at session start. Structure:

```
sas-amp-working/
  research/
    regulatory.md
    benchmarks.md
    organisational.md
    research-brief.md        # Consolidated summary for other agents
  data/
    cleaned/                 # Normalised data files
    charts/                  # Generated chart images (PNG for DOCX)
  drafts/
    sections/                # Individual section drafts
  output/
    amp-presentation.html    # Final HTML presentation
    amp-document.docx        # Final DOCX document
```

## AMP Structure

The plan follows a combined structure drawing from both the SMEC AMP Template and NAMS.PLUS AMP Template, aligned to ISO 55001:2024. Refer to `references/amp-template-structure.md` for the full section-by-section breakdown with guidance notes.

### Core Sections

1. **Executive Summary** — Context, costs, what will/won't be done, risks, confidence, next steps
2. **Introduction** — Purpose, background, plan framework, organisational commitment, strategic linkages
3. **Levels of Service** — Customer expectations, strategic goals, legislative requirements, desired vs current LoS (community + technical)
4. **Future Demand** — Demand drivers, forecast, technology/legislation changes, demand management, impact on assets
5. **Asset Lifecycle Management** — Classification, condition, valuation, criticality, maintenance plan, renewal/replacement, creation/acquisition, optimisation, disposal
6. **Risk Management** — Risk identification, assessment, mitigation strategies
7. **Financial Summary** — 10-year projections (opex + capex), funding strategy, valuation forecasts, key assumptions, confidence levels
8. **Asset Management Practices** — Systems, processes, work management, supply chain
9. **Improvement and Monitoring** — Performance measures, improvement program, monitoring/review
10. **Appendices** — Cost profiles, condition assessments, data tables, glossary

## ISO 55001:2024 Alignment

Every section of the AMP maps to specific ISO 55001:2024 clauses. Refer to `references/iso55001-amp-mapping.md` for the complete clause-by-clause mapping table. Ensure each section explicitly demonstrates how it addresses the relevant ISO requirements.

## Research Phase

Dispatch the `amp-researcher` agent early in the process with these parameters:
- **Organisation name** and sector/industry
- **Jurisdiction** (for regulatory context)
- **Asset class(es)** covered by the AMP

The researcher produces structured files in `sas-amp-working/research/` and a consolidated `research-brief.md`. All other agents should read `research-brief.md` before performing their work.

## Data Analysis

When the user provides quantitative data (asset registers, condition data, maintenance histories, financial records), dispatch the `amp-data-analyst` agent. It handles:

- **Data cleaning and normalisation** — Handle messy formats, missing values, inconsistent naming
- **Asset profiling** — Age distribution, condition distribution, criticality breakdown
- **Financial analysis** — NPV calculations, renewal cost forecasting, straight-line depreciation
- **Lifecycle costing** — Basic LCC analysis with discount rates
- **Chart generation** — D3.js interactive charts for HTML, matplotlib/plotly static images for DOCX

Refer to `references/data-analysis-patterns.md` for methodology details.

## Per-Section Drafting with Context Review

Draft each major section individually. After drafting each section, dispatch the `amp-asset-context-reviewer` agent with:
- The drafted section content
- The `research-brief.md`
- All user interview responses collected so far

The reviewer validates the section reads authentically for the specific organisation and asset class, flags generic language, and challenges unsupported assumptions. Incorporate feedback before moving to the next section.

## Output Generation

### HTML Presentation

Invoke the `/sas-presentation` skill with presentation type `standard-narrative`. The presentation mirrors the full AMP structure with:
- D3.js interactive charts embedded inline
- SAS-AM branding (light/dark mode)
- One section per slide group
- Data tables and key metrics as card layouts

### DOCX Document

Run the `generateDocx.py` script at `${CLAUDE_PLUGIN_ROOT}/scripts/generateDocx.py`. Pass:
- All section draft files from `sas-amp-working/drafts/sections/`
- Chart images from `sas-amp-working/data/charts/`
- Organisation metadata (name, logo path if provided, date, version)

The script produces a branded SAS-AM document with:
- Cover page with organisation name and SAS-AM branding
- Auto-generated table of contents
- Consistent heading styles (SAS Blue `#002244`)
- Embedded chart images
- Professional table formatting
- Document control section

## Interview Methodology

Follow the adaptive interview approach described in `references/interview-methodology.md`. Key principles:

- **One question at a time**, with multiple-choice options (A, B, C, D) where possible
- **Start with what you have** — analyse provided materials before asking questions
- **Only ask about gaps** — never ask for information already provided or discoverable through research
- **Adapt depth to maturity** — ask simpler questions for organisations new to AM, more detailed for mature organisations
- **Validate understanding** — periodically summarise what has been gathered and confirm with the user

## Sector Adaptation

Adapt the plan to any sector. Adjust terminology, benchmarks, and emphasis based on the identified sector:

| Sector | Key Emphasis | Typical Assets |
|--------|-------------|----------------|
| Local Government | Community LoS, rates sustainability, LTFP alignment | Roads, drainage, buildings, parks |
| Water/Wastewater | Regulatory compliance, public health, environmental | Pipes, pumps, treatment plants |
| Transport | Safety, availability, service frequency | Rolling stock, track, signals, stations |
| Resources/Mining | Production uptime, safety, environmental | Processing plant, mobile fleet, conveyors |
| Health | Clinical outcomes, safety, compliance | Building services, medical equipment |
| Defence | Capability, readiness, security | Platforms, weapons systems, facilities |

## Additional Resources

### Reference Files

- **`references/amp-template-structure.md`** — Full section-by-section AMP structure with guidance notes
- **`references/iso55001-amp-mapping.md`** — ISO 55001:2024 clause summaries and AMP section mapping
- **`references/data-analysis-patterns.md`** — LCC, NPV, renewal modelling, chart specifications
- **`references/interview-methodology.md`** — Adaptive interview process and question bank

### Scripts

- **`${CLAUDE_PLUGIN_ROOT}/scripts/generateDocx.py`** — DOCX generation with SAS-AM branding
- **`${CLAUDE_PLUGIN_ROOT}/scripts/generateCharts.py`** — Static chart generation for DOCX embedding
- **`${CLAUDE_PLUGIN_ROOT}/scripts/dataUtils.py`** — Data cleaning, LCC calculations, NPV utilities

### Brand Assets

- **`references/assets/sas-logo-light.svg`** — SAS-AM logo (light mode)
- **`references/assets/sas-logo-dark.png`** — SAS-AM logo (dark mode)
