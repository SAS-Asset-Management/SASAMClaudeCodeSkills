# Client Integration — Knowledge Graph Overlay

How to merge client specific documents and data with the standards knowledge graph to produce AMPs grounded in both ISO 55001 requirements and the client's actual reality.

## Overview

The AMP knowledge graph (`amp-knowledge-graph.json`) encodes **what should be in an AMP** — standards, frameworks, best practice. Client data provides **what is** — actual asset condition, actual costs, actual performance. The AMP bridges the two.

Two integration layers:

| Layer | Input | Method | Output |
|-------|-------|--------|--------|
| **Documents** | Client policies, existing plans, org context, contracts | Graphify extraction → merge | Client overlay graph with org specific nodes |
| **Data** | Asset registers, condition, maintenance history, financials | amp-data-analyst → graph enrichment | Quantitative nodes linked to AMP sections |

## Layer 1: Client Document Graph

### Step 1 — Collect Client Documents

Ask the user to provide any of:

- Existing SAMP or AM policy
- Previous AMPs (even outdated ones)
- Annual reports or corporate plans
- Asset management system documentation
- Regulatory licences or compliance obligations
- Maintenance contracts or service level agreements
- Organisational structure / RACI charts
- Risk registers
- Long term financial plans (LTFP)
- Condition assessment reports
- Any internal standards or procedures

Save to `sas-amp-working/research/client-docs/`.

### Step 2 — Extract Client Graph

Run graphify on the client documents folder:

```python
import subprocess, json
from pathlib import Path

client_docs = Path('sas-amp-working/research/client-docs/')
if any(client_docs.iterdir()):
    # Use graphify detect + extract (simplified — no full pipeline needed)
    # Dispatch a subagent to extract entities and relationships from client docs
    # Save to sas-amp-working/research/client-graph.json
    pass
```

Alternatively, dispatch a general purpose subagent with graphify extraction instructions targeting the client docs. The subagent should extract:

- **Organisation nodes** — the client entity, divisions, subsidiaries, partners
- **Asset class nodes** — what asset types appear in the documents
- **Policy/strategy nodes** — existing commitments, objectives, targets
- **People/role nodes** — key stakeholders, decision makers, responsible officers
- **Standard/regulation nodes** — what standards the client already references
- **System nodes** — what CMMS/EAM/GIS they use
- **Financial nodes** — budget figures, funding sources, valuation data
- **Risk nodes** — identified risks from existing registers
- **LoS nodes** — any existing service level definitions
- **Gap nodes** — acknowledged gaps or improvement items from previous plans

Save to `sas-amp-working/research/client-graph.json`.

### Step 3 — Merge with Standards Graph

```python
import json
import networkx as nx
from networkx.readwrite import json_graph
from pathlib import Path

# Load standards graph
standards_path = Path('${CLAUDE_PLUGIN_ROOT}/skills/sas-amp/references/amp-knowledge-graph.json')
standards_data = json.loads(standards_path.read_text())
G_standards = json_graph.node_link_graph(standards_data)

# Load client graph
client_path = Path('sas-amp-working/research/client-graph.json')
if client_path.exists():
    client_data = json.loads(client_path.read_text())
    G_client = json_graph.node_link_graph(client_data)

    # Merge — client nodes overlay onto standards
    G_merged = nx.compose(G_standards, G_client)

    # Save merged graph for section queries
    merged_data = json_graph.node_link_data(G_merged)
    Path('sas-amp-working/research/merged-graph.json').write_text(json.dumps(merged_data))
else:
    # No client docs — use standards graph alone
    G_merged = G_standards
```

### Step 4 — Bridge Edges

After merging, create bridge edges between client nodes and standards nodes:

- If the client has an existing AM Policy → edge to `iso55001_cl52` (Policy clause)
- If the client references ISO 55001 → edge to `iso55001` standard node
- If the client has a SAMP → edge to `samp_concept` and `iso55001_cl621`
- If the client has existing LoS → edge to `iso55001_cl622` and `concept_lg_amp_los`
- If the client uses a specific CMMS → edge to `maint_fw_area8` (Support Systems)
- If the client operates under AMAF → edge to `amaf` and relevant mandatory requirements

These bridge edges are what make gap analysis possible — they show where the client's reality connects to what the standards require, and where the gaps are.

## Layer 2: Client Data Enrichment

### After Data Analysis

When the `amp-data-analyst` agent processes client data files (asset registers, condition data, maintenance costs, financials), its outputs should be linked to the merged graph:

| Data Analysis Output | Link To Graph Node | Edge Type |
|---------------------|-------------------|-----------|
| Asset age distribution | `iso55001_cl81` (lifecycle management) | `evidences` |
| Condition profile | `iso55001_cl76` (data and information) | `evidences` |
| Renewal cost forecast | `iso55001_cl623` (AMP clause — financial implications) | `quantifies` |
| Maintenance cost breakdown | `maint_fw_area4` (Maintenance Strategy) | `quantifies` |
| Criticality distribution | `iso55001_cl612` (Risk — determine criticality) | `evidences` |
| LCC analysis | `concept_iam_lifecycle_cost_elements` | `quantifies` |
| NPV calculations | `concept_iam_capex_opex_totex` | `quantifies` |
| Sustainability ratio | Financial section seeds | `quantifies` |

### Data Summary Nodes

Create summary nodes for key data findings and add them to the merged graph:

```python
# Example: add asset portfolio summary node
G_merged.add_node('client_asset_portfolio', **{
    'label': f'{org_name} Asset Portfolio',
    'file_type': 'data',
    'total_assets': total_count,
    'replacement_value': total_rv,
    'avg_condition': avg_condition,
    'avg_remaining_life': avg_rl,
})
G_merged.add_edge('client_asset_portfolio', 'iso55001_cl623',
    relation='evidences', confidence='EXTRACTED', confidence_score=1.0)
```

## Gap Analysis Queries

### Compliance Gap Analysis

After merging, query the graph to identify what the standards require vs what the client already has:

```python
def compliance_gaps(G, framework='iso55001'):
    """Find standard requirements with no client evidence."""
    gaps = []
    requirement_nodes = [n for n in G.nodes()
                        if n.startswith(framework)]
    for req in requirement_nodes:
        neighbors = list(G.neighbors(req))
        has_client_evidence = any(
            G.nodes[nb].get('source', '') == 'client'
            or 'client_' in nb
            for nb in neighbors
        )
        if not has_client_evidence:
            gaps.append({
                'requirement': G.nodes[req].get('label', req),
                'node_id': req,
                'severity': 'high' if '6.2.3' in req or '8.1' in req else 'medium'
            })
    return sorted(gaps, key=lambda g: g['severity'])
```

### AMAF Compliance Check

```python
def amaf_gaps(G):
    """Find AMAF mandatory requirements not evidenced by client docs."""
    amaf_nodes = [n for n in G.nodes() if 'amaf_mandatory' in n]
    gaps = []
    for req in amaf_nodes:
        neighbors = list(G.neighbors(req))
        has_evidence = any('client_' in nb for nb in neighbors)
        if not has_evidence:
            gaps.append(G.nodes[req].get('label', req))
    return gaps
```

### Interview Prioritisation

Use gap analysis results to prioritise interview questions:

```python
def prioritise_interviews(gaps, existing_questions):
    """Map gaps to interview questions, skip what's already covered."""
    priority = []
    for gap in gaps:
        # Find which AMP section this gap maps to
        section = map_requirement_to_section(gap['requirement'])
        # Find the interview question for that section
        question = existing_questions.get(section)
        if question and section not in already_answered:
            priority.append({
                'section': section,
                'question': question,
                'reason': f"Gap in {gap['requirement']}",
                'severity': gap['severity']
            })
    return sorted(priority, key=lambda p: p['severity'])
```

## Workflow Integration

The client integration slots into the existing workflow at steps 2 and 3:

```
1. Intake          → Receive client materials
2. Graph Load      → Load standards graph
   2a. Extract     → Graphify client documents → client-graph.json
   2b. Merge       → Compose standards + client → merged-graph.json
   2c. Gap         → Run compliance_gaps() and amaf_gaps()
3. Research        → amp-researcher fills gaps from web (now targeted by graph gaps)
4. Interview       → Only ask about gaps the graph can't resolve
5. Data Analysis   → amp-data-analyst processes quantitative data
   5a. Enrich      → Add data summary nodes to merged graph
6. Drafting        → Query merged graph (standards + client + data) per section
7. Review          → Reviewer checks against merged graph requirements
8. Output          → Generate HTML + DOCX
```

## Merged Graph Query Pattern

When drafting sections, the merged graph query returns three types of results:

1. **Standards context** (from `amp-knowledge-graph.json`) — what the ISO/AMAF/IAM requires
2. **Client context** (from `client-graph.json`) — what the client already has, their terminology, their existing commitments
3. **Data context** (from data enrichment) — quantitative evidence about the client's assets

The drafter uses all three:
- Standards context → ensures compliance
- Client context → ensures authenticity (uses their language, references their policies)
- Data context → ensures the plan is evidence based, not aspirational

## Example: Drafting Section 3 (Levels of Service)

```
Graph query returns:
  STANDARDS: ISO 55001 Clause 6.2.2 requires measurable objectives aligned with org objectives
  STANDARDS: AMAF 3.2.2 requires AM strategy covering whole lifecycle on portfolio basis
  STANDARDS: IAM recommends community LoS → technical LoS → gap analysis pattern
  CLIENT: Client's existing SAMP defines 4 strategic AM objectives
  CLIENT: Client's annual report commits to "safe, reliable, and sustainable infrastructure"
  CLIENT: Client's maintenance contract defines 12 KPIs for service delivery
  DATA: Current condition profile shows 23% of assets below intervention level
  DATA: Customer satisfaction survey score: 7.2/10 (from research)

Drafter produces: Section that uses the client's own 4 objectives as LoS framework,
  translates the 12 contract KPIs into technical LoS measures, identifies the 23%
  condition gap as a service risk, and benchmarks the 7.2/10 satisfaction against
  comparable organisations from the research brief.
```

This is the difference between a template AMP and a plan that reads like it was written by someone who understands the client's business.
