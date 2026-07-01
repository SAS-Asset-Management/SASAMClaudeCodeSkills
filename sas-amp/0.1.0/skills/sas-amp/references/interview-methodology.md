# Adaptive Interview Methodology for AMP Development

Guide for conducting targeted, gap-driven interviews when developing Asset Management Plans.

## Core Principles

1. **Analyse first, ask later** — Exhaust what can be learned from provided materials and research before asking a single question
2. **One question at a time** — Never present a list of all questions upfront
3. **Multiple-choice where possible** — Offer A, B, C, D options to reduce cognitive load and accelerate the process
4. **Only ask about gaps** — Never ask for information already provided or discoverable through research
5. **Adapt depth to maturity** — Simpler questions for organisations new to AM, more detailed for mature ones
6. **Validate periodically** — Summarise understanding every 3-5 questions and confirm

## Intake Phase

When the user first engages, accept everything they provide before asking questions:

1. Ask: *"What organisation is this AMP for? Go ahead and share any data, documents, or context you have — I'll analyse it all before asking questions."*
2. Receive and catalogue all materials
3. Save client documents to `sas-amp-working/research/client-docs/`
4. **Extract client graph** — graphify the client documents to identify what standards they reference, what commitments they've made, what asset classes they cover
5. **Merge with standards graph** — compose client graph with `amp-knowledge-graph.json`
6. **Run graph gap analysis** — compare ISO 55001 clause requirements and AMAF mandatory requirements against what the client documents evidence
7. Present a **graph informed gap analysis** (see below)
8. Begin research phase targeting graph identified gaps
9. Start interviews only for gaps that research cannot fill

## Gap Analysis Template

After merging client documents with the standards graph and running compliance checks:

```
## AMP Readiness Assessment (Graph Informed)

| Section | Standards | Client Evidence | Research | Gap | Interview Needed? |
|---------|-----------|----------------|----------|-----|-------------------|
| Introduction | 4.1, 4.2, 4.3, 5.1-5.3 | AM Policy found, SAMP exists | Org context gathered | Strategic linkages unclear | Yes — Q4 |
| Levels of Service | 4.5, 6.2.2 | Contract KPIs found | Benchmarks gathered | Community LoS not defined | Yes — Q6, Q7 |
| Future Demand | 4.1, 6.1.3 | — | Population data found | Asset specific demand unknown | Yes — Q9, Q10 |
| Lifecycle Mgmt | 6.2.3, 8.1 | Asset register provided | Useful life benchmarks | Condition data, renewal criteria | Yes — Q11, Q12 |
| Risk Management | 6.1.1, 6.1.2 | Risk register found | — | Covered by client docs | No |
| Financial Summary | 6.2.3(h), 7.1 | LTFP provided | — | Renewal gap not quantified | Data analysis needed |
| AM Practices | 7.2-7.7, 8.3 | CMMS identified | — | Work mgmt process unknown | Yes — Q18 |
| Improvement | 9.1-10.3 | Maturity assessment exists | — | Improvement plan outdated | Yes — Q19 |
```

The key difference: the **Standards** column comes from the knowledge graph (ISO 55001 clauses per section), and **Client Evidence** comes from the client graph overlay. Only the remaining **Gap** column drives interviews.

## Interview Sequences by Section

### Section 2: Introduction — Scoping Questions

**Q1: Organisation and Assets**
> What type of organisation is [name]?
> - A) Local government / council
> - B) State government agency
> - C) Private sector / corporate
> - D) Government-owned corporation
> - E) Other (please describe)

**Q2: Asset Classes**
> Which asset classes should this AMP cover?
> - A) A single asset class (e.g., roads only, buildings only)
> - B) Multiple related asset classes (e.g., all transport assets)
> - C) All asset classes across the organisation
> - D) Specific assets you'll tell me about

**Q3: Planning Timeframe**
> What planning timeframe should the AMP cover?
> - A) 10 years (standard)
> - B) 20 years (long-term infrastructure)
> - C) 5 years (short-term operational focus)
> - D) Other specific period

**Q4: Strategic Context**
> Does [name] have an existing AM policy or strategy that this AMP should align with?
> - A) Yes — I can share it
> - B) Yes, but I don't have it available right now
> - C) No — this is a first-generation plan
> - D) Not sure

**Q5: AM Maturity**
> How would you describe [name]'s current asset management maturity?
> - A) Getting started — limited formal AM processes
> - B) Developing — some processes in place, significant gaps
> - C) Competent — systematic approach, good data, room for improvement
> - D) Advanced — mature processes, strong data, continuous improvement culture

### Section 3: Levels of Service

**Q6: Customer Expectations**
> How well understood are stakeholder expectations for these assets?
> - A) Formal customer research/surveys have been conducted
> - B) Contractual/regulatory service standards are defined
> - C) Informal understanding based on complaints and feedback
> - D) Not well understood — this is an area to develop

**Q7: Current Performance**
> How would you rate the current performance of these assets against expectations?
> - A) Meeting or exceeding expectations
> - B) Mostly meeting expectations with some gaps
> - C) Significant gaps between performance and expectations
> - D) Not measured systematically

**Q8: Key Service Priorities**
> What are the top 3 priorities for these assets? (Select up to 3)
> - A) Safety and compliance
> - B) Reliability / availability
> - C) Cost efficiency
> - D) Environmental sustainability
> - E) Customer satisfaction
> - F) Growth / capacity
> - G) Other (please specify)

### Section 4: Future Demand

**Q9: Demand Trends**
> What is the primary demand trend affecting these assets?
> - A) Growing — increasing demand for services
> - B) Stable — steady state
> - C) Declining — reducing demand
> - D) Changing — not more/less, but different requirements
> - E) Mixed — varies by asset class or location

**Q10: Key Change Drivers**
> What external factors are most likely to impact these assets in the next 10 years?
> - A) Population/demographic change
> - B) Regulatory or legislative change
> - C) Climate change / environmental
> - D) Technology change
> - E) Economic / funding pressures
> - F) Multiple (tell me which)

### Section 5: Asset Lifecycle Management

**Q11: Data Availability**
> What asset data do you have available?
> - A) Comprehensive asset register with condition and financial data
> - B) Asset register with basic attributes (no condition)
> - C) Financial records only (valuations, depreciation schedules)
> - D) Limited — mostly informal knowledge
> - E) I'll share what I have and you can assess it

**Q12: Condition Assessment**
> How is asset condition assessed?
> - A) Formal condition assessments on a regular cycle
> - B) Condition recorded opportunistically (during maintenance)
> - C) Age-based assumptions used as proxy for condition
> - D) No systematic condition assessment

**Q13: Maintenance Approach**
> How is maintenance currently managed?
> - A) Primarily preventive/planned maintenance with CMMS
> - B) Mix of planned and reactive, with basic work management
> - C) Primarily reactive / breakdown maintenance
> - D) Outsourced to contractors

### Section 6: Risk Management

**Q14: Risk Framework**
> Does [name] have an established risk management framework?
> - A) Yes — formal risk framework with registers and reviews
> - B) Partially — some risk identification but not systematic
> - C) No — risk management is informal
> - D) Yes, but it doesn't specifically cover asset risks

**Q15: Key Risks**
> What are the biggest risks associated with these assets? (Open question — describe in your own words)

### Section 7: Financial Summary

**Q16: Financial Data**
> What financial information is available for these assets?
> - A) Detailed budgets and actuals for operations, maintenance, and capital
> - B) High-level budgets only (total opex, total capex)
> - C) Valuation/depreciation data from financial statements
> - D) Limited financial data available

**Q17: Funding Outlook**
> How would you describe the funding outlook for these assets?
> - A) Adequately funded — budgets generally meet needs
> - B) Under-funded — known gap between needs and budgets
> - C) Significantly under-funded — major backlog building
> - D) Not clear — funding adequacy hasn't been assessed

### Section 8-9: AM Practices and Improvement

**Q18: AM Systems**
> What systems are used to manage these assets?
> - A) Enterprise Asset Management (EAM) system — tell me which
> - B) CMMS (Computerised Maintenance Management System) — tell me which
> - C) Spreadsheets and documents
> - D) Minimal — mostly paper-based or informal

**Q18a: Organisational Culture, Change Readiness and Competence**
> How ready is the organisation — its people, culture and skills — to deliver the practices this plan will rely on?
> - A) Strong — the right skills are in place and there is an established asset management culture
> - B) Developing — some capability and buy in, with known skills or resourcing gaps
> - C) Early — asset management is new to most of the organisation; significant change management needed
> - D) Constrained — capability or culture is a recognised barrier and needs a deliberate uplift plan
> - E) Not sure — this has not been assessed

*(Covers IAM Anatomy v4 box 6 — Organisation & People: organisational arrangements, culture, competence management and change management. A weak answer here should surface as an action in the Section 9 improvement programme.)*

**Q19: Improvement Priorities**
> If you could improve one aspect of how these assets are managed, what would it be?
> (Open question — this often reveals the most important gaps)

## Adaptive Question Selection

Not all questions above will be asked. Select based on:

1. **Skip if graph resolved** — If the merged graph (standards + client) already provides the answer. For example, if the client's SAMP defines AM objectives, skip Q4 (strategic context) and instead validate what the graph found.
2. **Skip if research resolved** — If the amp-researcher found the answer from public sources
3. **Skip if irrelevant** — If the organisation's context makes a question irrelevant
4. **Prioritise by gap severity** — Ask about high severity gaps first (ISO 55001 Clause 6.2.3 and 8.1 gaps are critical; Clause 10.x gaps can wait)
5. **Go deeper if needed** — If an answer reveals complexity, ask follow-up questions
6. **Adjust language** — Match terminology to the user's sector and familiarity. If the client graph reveals their terminology (e.g., they say "asset renewal" not "capital replacement"), use their language in questions.

## Validation Checkpoints

After every 3-5 questions, present a summary:

> *"Let me confirm what I understand so far:*
> - *[Organisation name] is a [type] in [jurisdiction]*
> - *The AMP covers [asset classes] with a replacement value of approximately [value]*
> - *Current AM maturity is [level] with [key gap]*
> - *The main priorities are [priorities]*
>
> *Is that right? Anything to correct or add?"*

## Handling Uncertainty

When users aren't sure about an answer:
- Offer to research it (dispatch amp-researcher)
- Suggest reasonable assumptions with confidence caveats
- Flag it as a data gap in the improvement program
- Never force an answer — "Not sure" is a valid response that gets documented
