# AMP Template Structure

Comprehensive section by section guide for developing an Asset Management Plan. This structure combines the SMEC AMP Template and NAMS.PLUS AMP Template, adapted for sector agnostic use.

> **Knowledge Graph Integration:** Each section below includes a `Graph Query` block listing the seed nodes to query in `amp-knowledge-graph.json` before drafting. See `graph-queries.md` for full query methodology.

## Section 1: Executive Summary

**Purpose:** Provide a standalone overview of the entire AMP that decision-makers can read without going deeper.

**Content:**
- **Context** — 2-3 sentences on the organisation, the community/operations served, and the assets covered
- **The Asset Portfolio** — What assets are included, their total replacement value
- **What Does It Cost?** — Total projected 10-year cost (operations + maintenance + renewal + upgrade); average annual cost; available funding; sustainability ratio; funding gap
- **What We Will Do** — Key actions and investments planned within the planning period
- **What We Cannot Do** — Services or works that cannot be provided under current funding
- **Managing the Risks** — Top 3-5 risks and high-level mitigation approach
- **Confidence Levels** — Data confidence rating (High/Medium/Low) and what it means
- **Value and Outcomes** — A short outcomes statement naming the organisational value and outcomes the plan delivers against the asset management objectives. Frame it against the dimensions of asset value (financial, service/level of service, risk reduction, compliance, sustainability and stakeholder outcomes) rather than expenditure alone. This closes the line of sight from purpose through to realised value and maps to IAM Anatomy v4 box 10 (Value & Outcomes).
- **The Next Steps** — Priority actions arising from the plan
- **Key Chart** — Single chart showing projected expenditure vs available funding over 10 years

**Graph Query:** Seed nodes `iso55001_cl623`, `def_amp`, `samp_concept`, `concept_iam_value_dimensions`, `iam_group10_value`. Extract the planning hierarchy and ISO definition of an AMP. The graph shows AMP sits between SAMP (strategic direction) and operational plans — the executive summary should reflect this cascade positioning. Use `concept_iam_value_dimensions` (the Shamrock dimensions of asset value) and `iam_group10_value` (IAM Value & Outcomes capability) to frame the outcomes statement so the summary closes on the value the plan realises, not just what it costs.

**Notes:** Draft this section LAST after all other sections are complete. It should be no more than 2-3 pages.

## Section 2: Introduction

**Purpose:** Establish the purpose, scope, and organisational context of the AMP.

**Content:**
- **Background** — Why this AMP exists, what it covers, organisational context
- **Function of the AMP** — Role of the AMP in the organisation's planning framework
- **Plan Structure and Framework** — Key elements, planning timeframe (typically 10 years), review cycle
- **Organisational Commitment** — How AM is positioned and supported within the organisation
- **Strategic Linkages** — Links to corporate strategy, other AMPs, policies, standards (show diagram if possible)
- **Stakeholders** — Key stakeholders, their interests, and how this plan addresses them
- **AM Maturity / Improvement Progress** — Current AM maturity level and progress since last plan

**ISO 55001 alignment:** Clauses 4.1, 4.2, 4.3, 5.1, 5.2, 5.3, 6.2.1

**Graph Query:** Seed nodes `iso55001_cl41`, `iso55001_cl42`, `iso55001_cl43`, `amaf`, `gfmam_landscape_v3`, `iam_anatomy_v4`. The graph connects AMAF to ISO 55000 (aligned), Victorian Standing Directions (enforced by), and asset life cycle (structured around). Establish the regulatory cascade: Victorian legislation → AMAF → ISO 55001 → this AMP. Query IAM Anatomy v4 for the 10 Capabilities (10-box model, July 2024) framing, and GFMAM Landscape v3.0 for the 7 Subject Areas.

## Section 3: Levels of Service

**Purpose:** Define what the assets are expected to deliver, from both community/customer and technical perspectives.

**Content:**
- **Customer/Community Expectations** — Results of research, consultation, contractual specifications
- **Strategic and Corporate Goals** — Relevant organisational goals and their impact on AM
- **Legislative Requirements** — Applicable legislation, regulations, standards, codes of practice
- **Community/Customer Levels of Service** — What outcomes stakeholders expect (qualitative and quantitative)
  - Table format: Service attribute | Current performance | Target performance | Gap
- **Technical Levels of Service** — How community LoS translate to technical/operational measures
  - Table format: Technical measure | Current | Target | Method of measurement

**Notes:**
- LoS should have both primary outputs (availability, reliability, capacity) and secondary considerations (HSE, cost, environmental)
- Include the desired vs current gap analysis — this drives the improvement program
- Where possible, benchmark LoS against comparable organisations

**ISO 55001 alignment:** Clauses 4.2, 4.5, 6.2.2

**Graph Query:** Seed nodes `iso55001_cl622`, `amaf_mandatory_3_2_2_strategy`, `concept_lg_amp_los`. The graph reveals LoS is where customer expectations meet technical reality. The local government node shows a specific pattern: community LoS → technical LoS → gap analysis → improvement programme. Query IAM Subject Group 5 (Strategy and Planning) for service level guidance.

## Section 4: Future Demand

**Purpose:** Forecast how demand for the assets and services will change over the planning period.

**Content:**
- **Demand Drivers** — Population growth, economic activity, regulatory changes, climate, technology
- **Demand Forecast** — Quantified projections (ideally with low/medium/high scenarios)
- **Changes in Technology** — How new technology may affect asset requirements or useful lives
- **Changes in Legislation** — Anticipated regulatory changes and their impact
- **Demand Impact on Assets** — How forecast changes affect asset utilisation, capacity, and condition
- **Demand Management Plan** — Non-asset solutions to manage demand (education, pricing, policy)
- **Asset Programs to Meet Demand** — Capital works or operational changes required
- **Sustainability and ESG** — How environmental, social and governance factors and sustainable development shape demand and asset decisions: decarbonisation and energy transition, climate adaptation and resilience, resource efficiency and circular economy, and any ESG or sustainability commitments the organisation has made. Treat this as a demand and objective driver, not an afterthought. This maps to IAM Strategy & Planning sub subject 7.5.2 (Sustainable Development). A standalone sustainability section can be used instead where the organisation's ESG commitments are material enough to warrant it.

**Notes:**
- Link demand forecasts to credible sources (government projections, industry forecasts)
- Distinguish between growth demand (new assets) and change demand (different standards)
- Include sensitivity analysis for key demand assumptions

**ISO 55001 alignment:** Clauses 4.1, 6.1, 6.2.3

**Graph Query:** Seed nodes `iso55001_cl41`, `iso55001_cl613`, `concept_lg_demand_forecasting`, `iam_group4_strategy`. The graph links demand to both risk (6.1.2) and opportunity (6.1.3). Query the local government 3 scenario model for demand forecasting structure. Query `iam_group4_strategy` (Strategy & Planning) for the Demand Analysis (7.5.1) and Sustainable Development (7.5.2) sub subjects that inform the demand forecast and the sustainability and ESG treatment.

## Section 5: Asset Lifecycle Management

**Purpose:** Detail how assets will be managed across their full lifecycle — this is the core technical section.

**Content:**

### 5.1 Background Data — Asset Classification and Description
- **Physical parameters** — Asset mix, age profiles, location, design capacity vs actual capacity
- **Condition** — Current condition profile, assessment methodology, condition grading scale, remaining life estimates
- **Valuation** — Replacement values by asset class, depreciated values, valuation methodology
- **Criticality** — Criticality framework, criticality distribution, high-criticality assets

### 5.2 Routine Operations and Maintenance Plan
- **Preventive Maintenance** — Planned maintenance programs, basis for frequencies, condition-based triggers
- **Corrective Maintenance** — Response standards, prioritisation, authority for works
- **Breakdown/Reactive Maintenance** — Definition, authority, emergency response
- **Maintenance Costs** — Historical and forecast costs by maintenance type
- **Standards and Procedures** — Applicable standards, specifications, maintenance procedures
- **Organisation and Responsibility** — Maintenance structure, RACI, resource requirements

### 5.3 Renewal/Replacement Plan
- **Renewal criteria** — How renewal decisions are made (condition trigger, age-based, risk-based)
- **Renewal standards** — What standard assets are renewed to (like-for-like, modern equivalent)
- **10-year renewal program** — Year-by-year renewal expenditure forecast
- **Renewal modelling assumptions** — Useful lives, condition deterioration, intervention triggers

### 5.4 Creation/Acquisition/Expansion Plan
- **Project ranking methodology** — How new/upgrade projects are prioritised
- **Planned capital works** — Committed and proposed projects with estimated costs
- **Impact on existing resources** — How new assets affect ongoing maintenance and operations

### 5.5 Optimisation Planning
- **Current optimisation initiatives** — Programs improving utilisation or performance
- **Planned optimisation** — Agreed initiatives with timelines and resource requirements

### 5.6 Disposal Plan
- **Planned disposals** — Assets identified for disposal (timing, method, cost/recovery)
- **Decommissioning requirements** — Environmental, safety, regulatory obligations

**ISO 55001 alignment:** Clauses 4.5.3, 6.2.3, 7.6, 8.1

**Graph Query:** Seed nodes `iso55001_cl81`, `iso55001_cl623`, `maint_fw_area4`, `maint_fw_area3`, `concept_iam_lifecycle_value_realisation`, `concept_iam_decision_making_techniques_scale`. This is the densest section of the graph. Query the Maintenance Framework's 9 areas for maintenance planning content. Query IAM Subjects 6/7 (Capital and Ops Decision Making) for investment appraisal methods. Query IAM Subject 8 (Lifecycle Value Realisation) for whole of life costing. Query Downer GU006 for lifecycle plan methodology (renewal, replacement, continue maintenance). Reference worked examples: Spotless hospital LCMP ($800M, 50,000+ assets) and the numerical lifecycle plan with 7 level hierarchy.

## Section 6: Risk Management

**Purpose:** Identify, assess, and plan mitigation for risks to the assets and the services they support.

**Content:**
- **Risk Framework** — Methodology used (e.g., ISO 31000 aligned), likelihood and consequence scales
- **Risk Appetite** — The risk appetite and tolerance the plan works within, inherited from the SAMP. State it explicitly so treatment decisions and residual risk acceptance trace back to the organisation's agreed appetite rather than being made ad hoc.
- **Risk Identification** — Key risks to assets, services, safety, environment, compliance, reputation
- **Risk Assessment** — Risk register with likelihood, consequence, inherent risk, controls, residual risk
- **Risk Mitigation Strategies** — Actions to treat high and extreme risks
- **Resilience and Contingency Planning** — Contingency plans and resilience analysis for high consequence and low likelihood events; how the organisation maintains or restores service when assets are disrupted (IAM Strategy & Planning sub subject 7.5.6, Contingency Planning and Resilience Analysis)
- **Incident Management and Response** — How asset related incidents are detected, escalated, responded to and learned from, and how response feeds back into the risk register and lifecycle plans (IAM Life Cycle Delivery sub subject 7.7.6, Incident Management and Response)
- **Service Consequences** — What happens if key assets fail (impact on levels of service)

**Notes:**
- Risk table format: Risk | Likelihood | Consequence | Rating | Controls | Residual Rating | Treatment
- Include both asset risks (failure, deterioration) and service risks (demand exceeds capacity, regulatory change)
- Link risks to specific lifecycle actions (maintenance, renewal, upgrade)

**ISO 55001 alignment:** Clauses 6.1.1, 6.1.2, 6.1.3

**Graph Query:** Seed nodes `iso55001_cl612`, `iso55001_cl611`, `amaf_mandatory_3_1_5`. Query the ISO 55002 8 step risk assessment process node. The graph shows risk connects to both planning (6.1) and operations (8.1) — the AMP should demonstrate this bidirectional link.

## Section 7: Financial Summary

**Purpose:** Present the financial outlook for managing the asset portfolio over the planning period.

**Content:**
- **Financial Statements and Projections** — 10-year expenditure forecast broken down by:
  - Operations (opex)
  - Maintenance (opex)
  - Renewal/replacement (capex)
  - Upgrade/new/expansion (capex)
  - Disposal
- **Funding Strategy** — How expenditure will be funded (rates, grants, borrowings, reserves, developer contributions)
- **Sustainability Ratio** — Required expenditure vs available funding (target: >95%)
- **Valuation Forecasts** — Projected replacement value, depreciated value, and annual depreciation over the planning period
- **Key Assumptions** — Discount rate, inflation rate, growth assumptions, unit rates
- **Forecast Reliability and Confidence** — Data confidence by category; sensitivity to key assumptions

**Key Charts:**
- Projected expenditure by type vs available funding (10-year bar/line chart)
- Renewal gap analysis (required renewal vs funded renewal)
- Asset value trajectory (replacement value and written-down value over time)
- Expenditure breakdown by category (pie/treemap)

**ISO 55001 alignment:** Clauses 6.2.3(h), 7.1

**Graph Query:** Seed nodes `iso55001_cl623`, `iso55001_cl71`, `concept_iam_capex_opex_totex`, `concept_iam_lifecycle_cost_elements`. The IAM's TOTEX concept bridges the traditional capex/opex split. Query the local government financial sustainability framework for the sustainability ratio approach. The AMP should present total cost of ownership, not just budget line items.

## Section 8: Asset Management Practices

**Purpose:** Describe the systems, processes, and capabilities that support AM delivery.

**Content:**
- **AM Framework** — How AM is structured in the organisation
- **Organisation, Culture and Competence** — Organisational arrangements and roles; the asset management competence needs of the workforce and how they are met; organisational culture and change readiness — how prepared the organisation is to adopt the practices this plan depends on, and how change will be managed. This maps to IAM Anatomy v4 box 6 (Organisation & People) — organisational arrangements, culture, competence management and organisational change management.
- **IT Systems** — CMMS/EAM, GIS, document management, financial systems
- **Work Management** — How work is planned, scheduled, executed, and closed
- **Data Management** — How asset data is collected, stored, and quality-assured
- **Configuration Management** — How the integrity of asset configuration and its records is controlled as assets and their information change over time (IAM Information Management sub subject 7.8.6)
- **Cost Control and Budgeting** — How AM costs are tracked and budgets developed
- **Supply Chain** — Procurement, contractor management, materials supply
- **Continuous Improvement** — How AM practices are reviewed and improved

**ISO 55001 alignment:** Clauses 4.4, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 8.3

**Graph Query:** Seed nodes `iso55001_cl76`, `iso55001_cl71`, `amaf_mandatory_3_4_3_info`, `maint_fw_area8`, `maint_fw_area9`, `iam_group3_people`, `iam_group7_info`. The Maintenance Framework's support systems area (Area 8) maps directly to CMMS/EAM, GIS, and data management content. Query AMAF information management requirements for Victorian compliance. Query `iam_group3_people` (Organisation & People) for the organisation, culture, competence and change readiness content, and `iam_group7_info` (Information Management) for data standards, systems and configuration management.

## Section 9: Improvement and Monitoring

**Purpose:** Define how the AMP will be measured, monitored, and improved.

**Content:**
- **Performance Measures** — KPIs used to assess AMP effectiveness (availability, reliability, utilisation, cost ratios, LoS achievement, risk exposure, HSE)
- **AM Maturity Assessment** — Current maturity scores and targets
- **Improvement Program** — Prioritised actions to address shortcomings, with owner, timeline, and resources
- **Monitoring and Review Process** — How and when the AMP is reviewed, who is responsible, what triggers an update
- **Audit Program** — Internal and external audit schedule
- **Value and Outcomes Realised** — An outcomes statement that closes the plan: state the organisational value and outcomes delivered against the asset management objectives, how they are measured, and how continual improvement will sustain them. This mirrors the Executive Summary outcomes statement and completes the line of sight from purpose to realised value, addressing IAM Anatomy v4 box 10 (Value & Outcomes).

**ISO 55001 alignment:** Clauses 9.1, 9.2, 9.3, 10.1, 10.2, 10.3

**Graph Query:** Seed nodes `iso55001_cl91`, `amaf_mandatory_3_1_4_perf`, `amaf_mandatory_3_4_2_monitor`, `concept_audit_evidence_for_amp`, `iam_group10_value`, `concept_iam_value_dimensions`. Query what auditors look for as evidence of AM planning (complexity categories, asset sampling). The graph shows the feedback loop: monitor → evaluate → improve → monitor. The GFMAM Maintenance Framework Area 9 (Maintenance Improvement) informs the improvement programme structure. Use `iam_group10_value` and `concept_iam_value_dimensions` to frame the outcomes realised so the plan reports value delivered against objectives, not just activity completed.

## Section 10: Appendices

**Typical appendices:**
- A: Maintenance response levels of service
- B: 10-year capital renewal program
- C: 10-year upgrade/expansion/new capital program
- D: Budgeted expenditures in long-term financial plan
- E: Condition assessment summaries
- F: Risk register (full)
- G: Asset register summary
- H: Abbreviations and glossary

## File Naming Convention

When saving section drafts to `sas-amp-working/drafts/sections/`, use this naming:

```
01-executive-summary.md
02-introduction.md
03-levels-of-service.md
04-future-demand.md
05-asset-lifecycle-management.md
06-risk-management.md
07-financial-summary.md
08-asset-management-practices.md
09-improvement-monitoring.md
10-appendices.md
```
