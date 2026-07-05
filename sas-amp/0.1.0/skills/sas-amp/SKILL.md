---
name: sas-amp
description: This skill should be used when the user asks to create, develop, draft, or review an asset management plan (AMP), mentions "sas-amp", requests an ISO 55001-aligned plan, or discusses AMP sections such as levels of service, demand forecasting, renewal planning, lifecycle costing, or financial projections. Covers any sector or asset class.
version: 0.1.0
---

# Asset Management Plan Development Tool

To produce comprehensive, ISO 55001:2024-aligned Asset Management Plans, conduct adaptive user interviews, autonomous research, and data analysis, then generate professional output in both HTML presentation and branded DOCX formats.

## Workflow Overview

The AMP development process follows an adaptive, gap-driven methodology rather than a rigid linear sequence. The overall flow is:

1. **Intake** — Accept whatever the user provides upfront (data files, context, documents, partial plans). Save client documents to `sas-amp-working/research/client-docs/`.
2. **Knowledge Graph Load + Client Overlay** — Load the standards graph. If client documents were provided, extract a client graph and merge with standards. Run gap analysis. See `references/client-integration.md` for the full process.
3. **Analysis** — Present gap analysis showing what standards require vs what client documents already cover. Prioritise gaps by severity (ISO 55001 Clause 6.2.3 and 8.1 are high priority).
4. **Research** — Dispatch `amp-researcher` agent targeting **graph identified gaps** — not generic research, but specific questions the gap analysis raised.
5. **Interview** — Conduct targeted interviews only for gaps the graph and research could not resolve (one question at a time, multiple choice where possible).
6. **Data Analysis** — Process quantitative data through `amp-data-analyst`. Enrich the merged graph with data summary nodes linked to relevant standard clauses.
7. **Drafting** — Write each AMP section by querying the **merged graph** (standards + client + data) for section context. Review with `amp-asset-context-reviewer`.
8. **Output Generation** — Produce both HTML presentation (via `/sas-presentation`) and DOCX (via `generateDocx.py`)

## Working Directory

Create `./sas-amp-working/` in the current project directory at session start. Structure:

```
sas-amp-working/
  research/
    client-docs/             # Client provided documents (policies, plans, reports)
    client-graph.json        # Extracted graph from client documents
    merged-graph.json        # Standards + client + data merged graph
    gap-analysis.md          # Graph informed gap analysis output
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

## AMP Knowledge Graph

The skill ships with a 183 node knowledge graph (`references/amp-knowledge-graph.json`) extracted from the SAS Technical Resource Library. It encodes:

- **ISO 55001:2024** clause level requirements (Clauses 4.1 through 10.3)
- **ISO 55000:2024** definitions (AMP, SAMP, AMS, LoS, AM objectives)
- **ISO 55002:2014** guidance for AMP development (Clause 6.2.2 detail)
- **AMAF** mandatory requirements mapped to ISO 55001 equivalents
- **IAM Anatomy v4** (10 Capabilities / 10-box model, July 2024) mapped to AMP content areas
- **GFMAM Landscape v3.0** (7 Subject Areas) mapped to AMP inputs
- **GFMAM Maintenance Framework** (9 Areas) mapped to maintenance planning
- **Downer AMS** AMP guide, template, lifecycle plan methodology
- **NAMS.PLUS / SMEC** template structures for local government
- **GFMAM Certification Guidance** — what auditors expect as evidence
- **IAM SSG Subjects 6/7/8** — decision making, lifecycle value realisation
- **MTM SAMP** — real world SAMP to AMP cascade example

### Mandatory Graph Query Before Drafting

Before drafting each AMP section, **you must** query the graph for that section's context. The file `references/graph-queries.md` specifies the seed nodes and extraction patterns for each of the 10 sections. This ensures every section is grounded in the standards, uses correct terminology, and addresses all applicable requirements.

**Load pattern:**

```python
import json
from networkx.readwrite import json_graph
from pathlib import Path

graph_path = Path('${CLAUDE_PLUGIN_ROOT}/skills/sas-amp/references/amp-knowledge-graph.json')
data = json.loads(graph_path.read_text())
G = json_graph.node_link_graph(data)
```

Then for each section, run the queries specified in `references/graph-queries.md`. Use the results to:
1. **Ground the section** in ISO 55001 clause language
2. **Check AMAF compliance** by verifying all mandatory requirements are addressed
3. **Adopt IAM/GFMAM terminology** where it adds precision
4. **Reference source documents** the client can verify
5. **Ensure nothing is missed** that the standards require

### Cross Cutting Graph Queries

Run these once at the start of any AMP engagement:

- **AMAF compliance matrix** — query all `amaf_mandatory_*` nodes to build a requirements checklist
- **IAM 10-box coverage matrix** — query the ten `iam_group*` capability nodes and, for each of the ten boxes (Purpose & Context, Leadership & Governance, Strategy & Planning, Decision Making, Life Cycle Delivery, Organisation & People, Information Management, Risk Management, Review & Continual Improvement, Value & Outcomes), report coverage as **well covered**, **thin**, or **missing** across the drafted AMP sections. Run this at engagement start alongside the AMAF compliance matrix and re-run before finalisation so no capability is left unaddressed. See `references/iam-10box-mapping.md` for the box to section mapping and the line of sight logic.
- **GFMAM Landscape alignment** — query `gfmam_sa*` nodes for subject area coverage
- **Maintenance Framework alignment** — query `maint_fw_area*` nodes for Section 5 coverage

## AMP Structure

The plan follows a combined structure drawing from both the SMEC AMP Template and NAMS.PLUS AMP Template, aligned to ISO 55001:2024. Refer to `references/amp-template-structure.md` for the full section by section breakdown with guidance notes.

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

## Client Document Integration

When the user provides client documents (policies, existing plans, reports, contracts), follow the process in `references/client-integration.md`:

1. Save documents to `sas-amp-working/research/client-docs/`
2. Extract a client graph using graphify or a targeted subagent
3. Merge with the standards graph: `nx.compose(G_standards, G_client)`
4. Create bridge edges between client nodes and standard requirement nodes
5. Run compliance gap analysis and AMAF gap analysis
6. Present gap analysis to user before starting interviews

The merged graph (`sas-amp-working/research/merged-graph.json`) replaces `amp-knowledge-graph.json` for all subsequent section queries. If no client documents are provided, use the standards graph directly.

## Research Phase

Dispatch the `amp-researcher` agent after the graph gap analysis with these parameters:
- **Organisation name** and sector/industry
- **Jurisdiction** (for regulatory context)
- **Asset class(es)** covered by the AMP
- **Graph identified gaps** — specific requirements where neither client documents nor the standards graph provide enough context

The researcher produces structured files in `sas-amp-working/research/` and a consolidated `research-brief.md`. The research brief should specifically address the gaps identified by the graph analysis. All other agents should read `research-brief.md` before performing their work.

## Data Analysis and Graph Enrichment

When the user provides quantitative data (asset registers, condition data, maintenance histories, financial records), dispatch the `amp-data-analyst` agent. It handles:

- **Data cleaning and normalisation** — Handle messy formats, missing values, inconsistent naming
- **Asset profiling** — Age distribution, condition distribution, criticality breakdown
- **Financial analysis** — NPV calculations, renewal cost forecasting, straight-line depreciation
- **Lifecycle costing** — Basic LCC analysis with discount rates
- **Chart generation** — D3.js interactive charts for HTML, matplotlib/plotly static images for DOCX

After data analysis completes, **enrich the merged graph** with data summary nodes. See `references/client-integration.md` Layer 2 for the enrichment pattern. Key linkages:

| Analysis Output | Links To | Edge |
|----------------|----------|------|
| Asset portfolio summary | `iso55001_cl623` | `evidences` |
| Condition profile | `iso55001_cl76` | `evidences` |
| Renewal forecast | `iso55001_cl623` (financial implications) | `quantifies` |
| Maintenance costs | `maint_fw_area4` | `quantifies` |
| Criticality distribution | `iso55001_cl612` | `evidences` |
| LCC results | `concept_iam_lifecycle_cost_elements` | `quantifies` |

This means section queries now return three layers: standards requirements, client context, and quantitative evidence.

Refer to `references/data-analysis-patterns.md` for methodology details.

## Per-Section Drafting with Graph Query and Context Review

For each major section, follow this three step process:

### Step 1 — Query the Knowledge Graph

Before writing a single word, run the graph queries specified in `references/graph-queries.md` for the current section. This returns:
- The **ISO 55001 clause requirements** the section must address
- The **AMAF mandatory requirements** the section satisfies
- The **IAM/GFMAM subject guidance** that informs the content
- **Template structures** from Downer, NAMS.PLUS, and SMEC for that section
- **Audit evidence expectations** — what an ISO 55001 auditor looks for

Collect the query results into section context. Do not draft without this step.

### Step 2 — Draft the Section

Write the section using:
- The graph query results (standards grounding)
- The `research-brief.md` (organisational context)
- User interview responses (client specifics)
- Data analysis outputs (quantitative evidence)

Every section should:
- Use terminology consistent with ISO 55000:2024 definitions (verify against graph nodes `def_amp`, `def_samp`, etc.)
- Include an ISO 55001 alignment note citing the specific clause(s) addressed
- Address all AMAF mandatory requirements identified by the graph query
- Reflect IAM/GFMAM subject guidance where it adds depth

### Step 3 — Context Review

After drafting, dispatch the `amp-asset-context-reviewer` agent with:
- The drafted section content
- The graph query results for that section (so the reviewer can verify standards coverage)
- The `research-brief.md`
- All user interview responses collected so far

The reviewer validates the section reads authentically for the specific organisation and asset class, flags generic language, challenges unsupported assumptions, and **verifies all graph identified requirements are addressed**. Incorporate feedback before moving to the next section.

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

**Sector conditional capabilities:** Some IAM Anatomy v4 sub subjects apply only in certain sectors. In particular, **Shutdown and Outage Strategy and Planning** (Strategy & Planning sub subject 7.5.5) is required for process and network sectors — Water/Wastewater, Transport, Resources/Mining — where planned shutdowns and outages drive lifecycle activity, and is generally not applicable to buildings or roads. Include it where the asset base has scheduled shutdowns or outages; note it as not applicable otherwise rather than forcing generic content.

## Additional Resources

### Reference Files

- **`references/amp-knowledge-graph.json`** — 183 node knowledge graph (ISO 55001, AMAF, IAM, GFMAM, templates). **Query before drafting each section.**
- **`references/graph-queries.md`** — Section by section graph query guide with seed nodes and extraction patterns
- **`references/client-integration.md`** — How to merge client documents and data with the standards graph for gap analysis and context enrichment
- **`references/amp-template-structure.md`** — Full section by section AMP structure with guidance notes
- **`references/iso55001-amp-mapping.md`** — ISO 55001:2024 clause summaries and AMP section mapping
- **`references/iam-10box-mapping.md`** — IAM Anatomy v4 (10-box model, July 2024) capability to AMP section mapping with sub subjects and line of sight; basis for the 10-box coverage matrix
- **`references/data-analysis-patterns.md`** — LCC, NPV, renewal modelling, chart specifications
- **`references/interview-methodology.md`** — Adaptive, graph informed interview process and question bank

### Scripts

- **`${CLAUDE_PLUGIN_ROOT}/scripts/generateDocx.py`** — DOCX generation with SAS-AM branding
- **`${CLAUDE_PLUGIN_ROOT}/scripts/generateCharts.py`** — Static chart generation for DOCX embedding
- **`${CLAUDE_PLUGIN_ROOT}/scripts/dataUtils.py`** — Data cleaning, LCC calculations, NPV utilities

### Brand Assets

- **`references/assets/sas-logo-light.svg`** — SAS-AM logo (light mode)
- **`references/assets/sas-logo-dark.png`** — SAS-AM logo (dark mode)
