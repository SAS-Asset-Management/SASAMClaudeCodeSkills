# AMP Knowledge Graph — Section Query Reference

The file `references/amp-knowledge-graph.json` contains a 183 node knowledge graph extracted from the SAS Technical Resource Library. It maps ISO 55001 clauses, AMAF mandatory requirements, IAM Anatomy subjects, GFMAM Landscape subject areas, Downer AMS templates, NAMS.PLUS templates, and sector guidance into a single connected structure.

## How to Query

Load the graph with NetworkX, then traverse for context before drafting each section:

```python
import json
from networkx.readwrite import json_graph
from pathlib import Path

graph_path = Path('${CLAUDE_PLUGIN_ROOT}/skills/sas-amp/references/amp-knowledge-graph.json')
data = json.loads(graph_path.read_text())
G = json_graph.node_link_graph(data)
```

### Query Pattern

For each section, run BFS from the relevant seed nodes to depth 2. Collect node labels, edge relations, and source files. Use the results to inform section content — cite source documents, adopt terminology from the standards, and ensure nothing is missed.

```python
def query_section(G, seed_ids, depth=2):
    """BFS from seed nodes, return subgraph context."""
    visited = set(seed_ids)
    frontier = set(seed_ids)
    edges = []
    for _ in range(depth):
        next_f = set()
        for n in frontier:
            for nb in G.neighbors(n):
                if nb not in visited:
                    next_f.add(nb)
                    edges.append((n, nb, G.edges[n, nb]))
        visited.update(next_f)
        frontier = next_f
    return {
        'nodes': {n: G.nodes[n] for n in visited if n in G},
        'edges': edges
    }
```

---

## Section Queries

### Section 1: Executive Summary

Draft LAST. Query the graph for the overall planning hierarchy and confidence concepts:

**Seed nodes:** `iso55001_cl623`, `def_amp`, `samp_concept`

**What to extract:**
- The ISO 55001 definition of an AMP (node `def_amp`)
- The SAMP → AMP → Lifecycle Plan → Maintenance Plan hierarchy
- What "confidence levels" means in the context of AM planning

**Graph insight:** The graph shows AMP sits between SAMP (strategic direction) and operational plans (maintenance, lifecycle). The executive summary should reflect this positioning — it's not a standalone document, it's part of a cascade.

---

### Section 2: Introduction

**Seed nodes:** `iso55001_cl41`, `iso55001_cl42`, `iso55001_cl43`, `amaf`, `gfmam_landscape_v3`, `iam_anatomy_v4`

**What to extract:**
- ISO 55001 Clause 4.1 (context), 4.2 (stakeholders), 4.3 (scope) requirements
- AMAF alignment requirements and which mandatory requirements apply
- How the IAM Anatomy v4 frames AM (6 Groups, 39 Subjects)
- How the GFMAM Landscape v3.0 frames AM (7 Subject Areas)

**Graph insight:** The graph connects AMAF to ISO 55000 (aligned), Victorian Standing Directions (enforced by), and asset life cycle (structured around). The introduction should establish this regulatory cascade: Victorian legislation → AMAF → ISO 55001 → this AMP.

---

### Section 3: Levels of Service

**Seed nodes:** `iso55001_cl622`, `amaf_mandatory_3_2_2_strategy`, `concept_lg_amp_los`

**What to extract:**
- ISO 55001 Clause 6.2.2 (AM objectives — must be measurable, aligned, monitored)
- AMAF requirement 3.2.2 (AM strategy covering whole lifecycle on portfolio basis)
- Local government LoS framework (community vs technical measures)
- IAM Subject Group 5 (Strategy and Planning) guidance on service levels

**Graph insight:** The graph reveals LoS is where customer expectations meet technical reality. The local government node (`framework_lg_amp_structure`) shows a specific pattern: community LoS → technical LoS → gap analysis → improvement programme. This structure works across sectors.

---

### Section 4: Future Demand

**Seed nodes:** `iso55001_cl41`, `iso55001_cl613`, `concept_lg_demand_forecasting`

**What to extract:**
- ISO 55001 Clause 4.1 (external/internal issues including climate change)
- ISO 55001 Clause 6.1.3 (opportunities)
- Local government demand forecasting approach (3 scenario model)
- How demand connects to asset creation/expansion decisions

**Graph insight:** The graph links demand to both risk (6.1.2) and opportunity (6.1.3). Demand forecasting isn't just about growth — it's about understanding what changes (technology, regulation, climate) will require different assets or different performance from existing ones.

---

### Section 5: Asset Lifecycle Management

**Seed nodes:** `iso55001_cl81`, `iso55001_cl623`, `maint_fw_area4`, `maint_fw_area3`, `concept_iam_lifecycle_value_realisation`, `concept_iam_decision_making_techniques_scale`

**What to extract:**
- ISO 55001 Clause 8.1 (operational planning including lifecycle management — creation through disposal)
- ISO 55001 Clause 6.2.3 (the AMP clause — processes/methods over asset life cycles)
- GFMAM Maintenance Framework areas: Area 3 (Maintenance Tactics), Area 4 (Maintenance Strategy Development)
- IAM Subject 8 (Lifecycle Value Realisation) — whole of life approach, CAPEX/OPEX/TOTEX
- IAM Subjects 6/7 (Capital Investment and Ops/Maintenance Decision Making)
- Downer lifecycle plan methodology (DG-AM-GU006) — renewal, replacement, continue maintenance strategies
- Worked examples: Spotless hospital LCMP ($800M, 50,000+ assets), numerical lifecycle plan with 7 level hierarchy

**Graph insight:** This is the densest section of the graph. The Maintenance Framework's 9 areas feed directly into AMP Section 5.2 (maintenance planning). The IAM's decision making techniques scale (from engineering judgement through to full optimisation) helps the drafter choose the right analytical depth for the client's maturity level.

---

### Section 6: Risk Management

**Seed nodes:** `iso55001_cl612`, `iso55001_cl611`, `amaf_mandatory_3_1_5`

**What to extract:**
- ISO 55001 Clause 6.1.2 (risk assessment — identify, analyse, evaluate, determine criticality)
- ISO 55001 Clause 6.1.1 (general actions to address risks and opportunities)
- AMAF requirement 3.1.5 (if present — risk related requirements)
- ISO 55002 guidance on the 8 step risk assessment method

**Graph insight:** The graph shows risk connects to both planning (6.1) and operations (8.1). The ISO 55002 node contains a structured 8 step risk assessment process that should inform the AMP's risk methodology.

---

### Section 7: Financial Summary

**Seed nodes:** `iso55001_cl623`, `iso55001_cl71`, `concept_iam_capex_opex_totex`, `concept_iam_lifecycle_cost_elements`

**What to extract:**
- ISO 55001 Clause 6.2.3(h) (financial and non financial implications)
- ISO 55001 Clause 7.1 (resources)
- IAM CAPEX/OPEX/TOTEX guidance — total cost of ownership
- IAM lifecycle cost elements breakdown
- Downer lifecycle plan financial methodology
- Local government financial sustainability framework (sustainability ratio)

**Graph insight:** The graph connects financial planning to both the AMP clause (6.2.3) and resource provision (7.1). The IAM's TOTEX concept bridges the traditional capex/opex split — the AMP should present total cost of ownership, not just budget line items.

---

### Section 8: Asset Management Practices

**Seed nodes:** `iso55001_cl76`, `amaf_mandatory_3_4_3_info`, `maint_fw_area8`, `maint_fw_area9`

**What to extract:**
- ISO 55001 Clause 7.6 (data and information — specifications, collection, quality)
- AMAF information management requirements
- GFMAM Maintenance Framework Area 8 (Maintenance Support Systems), Area 9 (Maintenance Improvement)
- How AM practices connect to the AMAF mandatory requirements for information, monitoring, maintenance

**Graph insight:** The graph reveals AM practices is where the "how" lives. The Maintenance Framework's support systems area (Area 8) maps directly to the CMMS/EAM, GIS, and data management content of this section.

---

### Section 9: Improvement and Monitoring

**Seed nodes:** `iso55001_cl91`, `amaf_mandatory_3_1_4_perf`, `amaf_mandatory_3_4_2_monitor`, `concept_audit_evidence_for_amp`

**What to extract:**
- ISO 55001 Clauses 9.1 (monitoring), 9.2 (audit), 9.3 (management review), 10.1-10.3 (improvement)
- AMAF performance and monitoring requirements
- What auditors look for as evidence of AM planning (audit complexity categories, asset sampling)
- GFMAM Maintenance Framework Area 9 (Maintenance Improvement)

**Graph insight:** The audit evidence node reveals what an ISO 55001 auditor expects from an AMP — this should guide what gets documented. The graph shows the feedback loop: monitor → evaluate → improve → monitor.

---

### Section 10: Appendices

No specific graph query needed. Appendices are data driven. Use the graph to verify terminology consistency — ensure the glossary aligns with ISO 55000:2024 definitions (nodes `def_amp`, `def_samp`, `def_ams`, `def_asset_management`, `def_am_objectives`, `def_level_of_service`).

---

## Cross Cutting Queries

### AMAF Compliance Check

Query all AMAF mandatory requirement nodes to build a compliance matrix:

```python
amaf_nodes = [n for n in G.nodes() if 'amaf_mandatory' in n]
for n in amaf_nodes:
    label = G.nodes[n].get('label', n)
    neighbors = [(G.nodes[nb].get('label',''), G.edges[n,nb].get('relation',''))
                 for nb in G.neighbors(n)]
    print(f'{label}: {neighbors}')
```

### IAM 39 Subjects Coverage

Query IAM subject group nodes to ensure the AMP addresses all relevant subjects:

```python
iam_nodes = [n for n in G.nodes() if 'iam_anatomy' in n or 'iam_group' in n]
```

### GFMAM Landscape Alignment

Query GFMAM subject area nodes to verify Landscape coverage:

```python
gfmam_nodes = [n for n in G.nodes() if 'gfmam_sa' in n or 'gfmam_landscape' in n]
```

### Maintenance Framework Alignment

Query all 9 maintenance framework areas for Section 5 (maintenance planning):

```python
maint_fw = [n for n in G.nodes() if 'maint_fw_area' in n]
```
