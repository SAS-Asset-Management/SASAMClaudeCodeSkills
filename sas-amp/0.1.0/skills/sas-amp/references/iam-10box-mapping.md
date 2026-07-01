# IAM Anatomy v4 — 10-Box Capability to AMP Section Mapping

This reference maps each of the ten capabilities of the IAM Anatomy of Asset Management v4 (the 10-box model, July 2024) to the Asset Management Plan section(s) that cover it, together with the sub subjects that sit inside each box and the line of sight each box contributes.

It is the IAM counterpart to `iso55001-amp-mapping.md`. Use the two together: the ISO mapping grounds each section in clause language, and this mapping confirms the AMP addresses every capability of the anatomy. The ten `iam_group*` nodes in `amp-knowledge-graph.json` carry these boxes; query them for the **IAM 10-box coverage matrix** cross cutting check described in `SKILL.md` and `graph-queries.md`.

## The 10-Box Model at a Glance

The anatomy arranges asset management as a single connected picture rather than a list. Read it three ways:

- **Top down line of sight** — Purpose & Context sets direction, Leadership & Governance authorises it, Strategy & Planning and Decision Making convert it into intent, and Life Cycle Delivery executes it. This is the ISO 55001 line of sight from organisational objectives to asset activity.
- **Enablers from the base** — Organisation & People, Information Management and Risk Management enable every layer above them; they are cross cutting rather than sequential.
- **Left to right value chain** — people through process through delivery through outcomes; Value & Outcomes closes the chain by reporting the value realised.
- **Three concentric PDCA loops** — plan, do, check, act at strategic, tactical and operational levels, with the inner Life Cycle Delivery ring running Acquire/Create → Operate → Maintain → Renew/Dispose.

## Mapping Table

| IAM Box (10-box model) | Sub subjects | AMP Section(s) | Line of Sight | Graph Node |
|---|---|---|---|---|
| 1. Purpose & Context | Organisational Purpose and Context; Stakeholder Management | 2. Introduction; 3. Levels of Service | Sets the direction the whole plan serves — why the assets exist and for whom | `iam_group1_context` |
| 2. Leadership & Governance | AM Leadership; AM Policy; AM System; AM Assurance and Audit; Technical Standards and Legislation | 2. Introduction; 8. AM Practices | Authorises and governs the plan — policy, the AM system, assurance and the standards it must meet | `iam_group2_governance` |
| 3. Strategy & Planning | Demand Analysis; Sustainable Development; AM Strategy and Objectives; Planning; Shutdown and Outage Strategy and Planning; Contingency Planning and Resilience Analysis; Resource Strategy and Management; Supply Chain Management; Life Cycle Value Realisation; Asset Costing and Valuation | 3. Levels of Service; 4. Future Demand; 5. Lifecycle; 7. Financial | Turns organisational intent into asset management objectives, demand response, resourcing and whole of life value | `iam_group4_strategy` |
| 4. Asset Management Decision Making | Decision Making | 3. Levels of Service; 5. Lifecycle; 7. Financial | Provides the decision criteria and methods that select options across the plan | `iam_group5_decision` |
| 5. Life Cycle Delivery | Asset Creation and Acquisition; Systems Engineering; Integrated Reliability; Asset Operations; Maintenance Delivery; Incident Management and Response; Asset Repurposing and Disposal | 5. Asset Lifecycle Management; 6. Risk Management | Executes the plan across the inner ring: acquire or create, operate, maintain, renew or dispose | `iam_group6_lifecycle` |
| 6. Organisation & People | Organisational Arrangements; Organisational Culture; Competence Management; Organisational Change Management | 8. AM Practices | Enabler — the organisation, culture, competence and change readiness that deliver the plan | `iam_group3_people` |
| 7. Information Management | AM Data and Information Strategy; Knowledge Management; Data and Information Standards; Data and Information Management; Data and Information Systems; Configuration Management | 5. Lifecycle; 8. AM Practices | Enabler — the data, systems and configuration control that make decisions evidence based | `iam_group7_info` |
| 8. Risk Management | Risk (assessment, appetite, treatment) | 6. Risk Management | Enabler — risk assessment, the appetite inherited from the SAMP, and treatment that runs through every layer | `iam_group8_risk` |
| 9. Review & Continual Improvement | Monitoring; Continuous Improvement; Management of Change | 9. Improvement and Monitoring | Checks and improves — the PDCA feedback loop that keeps the plan effective | `iam_group9_review` |
| 10. Value & Outcomes | Outcomes and Impacts | 1. Executive Summary; 3. Levels of Service; 9. Improvement and Monitoring | Closes the line of sight — reports the value and outcomes realised against the objectives | `iam_group10_value` |

## Box Summaries

### Box 1 — Purpose & Context

The organisation understands why it holds assets, the internal and external context it operates in, and the stakeholders it serves. The AMP demonstrates this in the Introduction (context and scope) and the Levels of Service section (stakeholder needs translated into measurable targets).

### Box 2 — Leadership & Governance

Leadership sets the AM policy, establishes the AM system, and provides assurance that it works, within the technical standards and legislation that apply. The Introduction documents leadership commitment, policy alignment and roles; AM Practices covers the assurance, audit and standards machinery.

### Box 3 — Strategy & Planning

The largest box. It converts organisational objectives into asset management objectives and the plans, resources, supply chain, sustainability response and whole of life value approach that deliver them. It spreads across Levels of Service, Future Demand, Lifecycle and Financial sections. Sustainable Development is treated explicitly in Future Demand and the sustainability sub block, and Asset Costing and Valuation anchors the Financial Summary.

### Box 4 — Asset Management Decision Making

The decision criteria and analytical methods used to choose between options — from engineering judgement through to full optimisation. It informs the renewal, maintenance and investment choices in Lifecycle and Financial, and the level of service trade offs in Section 3.

### Box 5 — Life Cycle Delivery

The inner ring of the anatomy: acquire or create, operate, maintain, renew or dispose, with systems engineering, integrated reliability and incident management and response alongside. This is the primary home of Section 5, with incident management and response also informing the Risk section.

### Box 6 — Organisation & People

An enabler. Organisational arrangements, culture, competence and change management determine whether the plan can actually be delivered. Covered in AM Practices, including the culture, change readiness and competence content.

### Box 7 — Information Management

An enabler. Data and information strategy, standards, management, systems, knowledge and configuration management make the plan evidence based. Covered in AM Practices (systems and data governance) and drawn on throughout Section 5 for asset data.

### Box 8 — Risk Management

An enabler that runs through every layer. Risk assessment, the risk appetite inherited from the SAMP, and risk treatment. The Risk Management section is its primary home, but risk also shapes lifecycle, financial and level of service decisions.

### Box 9 — Review & Continual Improvement

The check and act of the PDCA loop: monitoring, continuous improvement and management of change. The Improvement and Monitoring section is its home, closing the feedback loop monitor → evaluate → improve → monitor.

### Box 10 — Value & Outcomes

Closes the line of sight. The plan states the value and outcomes it realises against the asset management objectives, framed against the dimensions of asset value (financial, service, risk, compliance, sustainability, stakeholder). It appears as an outcomes statement in the Executive Summary and again as value realised in the Improvement and Monitoring section, and is elaborated by the `concept_iam_value_dimensions` node.

## Coverage Check

Run the IAM 10-box coverage matrix at engagement start and again before finalisation. For each of the ten boxes, query the corresponding `iam_group*` node, then judge whether the drafted AMP covers it **well**, **thinly**, or **not at all**, and record the finding. Boxes that are enablers (People, Information, Risk) are the ones most often left thin, so give them explicit attention. No box should finish the engagement missing.

## Traceability Approach

When drafting a section, note in an alignment line which IAM boxes the section addresses, in the same light touch style used for ISO 55001 clauses. Example:

> *This section addresses IAM Anatomy v4 boxes 3 (Strategy & Planning) and 4 (Decision Making) by translating organisational objectives into asset management objectives and the decision criteria used to prioritise investment.*
