# Tender Alignment Scoring Matrix

## Overview

This matrix defines how tenders are scored against marcov's capabilities and strategic priorities. The total score determines whether a tender passes to deep assessment.

**Pass threshold**: ≥80% alignment (≥80 points out of 100)

---

## Scoring Dimensions

### 1. Domain Fit (30 points max)

How well does the tender's subject matter align with marcov's core expertise?

| Score | Criteria |
|-------|----------|
| 30 | **Perfect fit**: Directly matches core service (RCM, ISO 55001, predictive maintenance, asset strategy) |
| 25 | **Strong fit**: Adjacent service we deliver (CMMS, condition monitoring, reliability analysis) |
| 20 | **Good fit**: Related domain where we have capability (data analytics for assets, maintenance optimisation) |
| 15 | **Moderate fit**: Tangential but achievable (general consulting in our industries) |
| 10 | **Weak fit**: Requires stretch or partnering (new service area) |
| 0 | **No fit**: Outside our domain entirely |

**Keywords indicating high domain fit**:
- asset management, asset strategy, asset plan
- reliability, RCM, FMEA, RCA, root cause
- maintenance, preventive, predictive, condition-based
- ISO 55001, GFMAM, maturity assessment
- CMMS, EAM, Maximo, SAP PM
- rolling stock, fleet management
- condition monitoring, vibration, oil analysis

---

### 2. Industry Match (25 points max)

Is this in a sector where we have track record and relationships?

| Score | Industry |
|-------|----------|
| 25 | Rail, rolling stock, tram, public transport |
| 22 | Water, wastewater, utilities |
| 20 | Energy (generation, transmission, distribution) |
| 18 | Mining, resources |
| 15 | Healthcare facilities, hospitals |
| 12 | Local government, councils |
| 10 | Defence, federal government |
| 5 | Other (case-by-case) |
| 0 | Outside scope (IT, pure construction, retail) |

---

### 3. Service Type Match (20 points max)

Is the tender asking for the type of work we do?

**CRITICAL**: If Service Type = 0, the tender is an AUTO-DECLINE regardless of other scores.

| Score | Service Type |
|-------|--------------|
| 20 | **Advisory/Strategy**: Consulting, review, assessment, strategy development, business case |
| 18 | **Technical Analysis**: RCM, FMEA, reliability studies, condition assessment, analytics |
| 15 | **Implementation Support**: Change management, training, system configuration |
| 0 | **Managed Services**: Ongoing operational maintenance services - NOT OUR MODEL |
| 0 | **Labour Hire**: Staff augmentation - NOT OUR MODEL |
| 0 | **Construction**: Building, installation, upgrades, renewals - NOT OUR MODEL |
| 0 | **Procurement**: Supply, purchase, delivery of goods - NOT OUR MODEL |
| 0 | **IT/Software**: Platform development, IT infrastructure - NOT OUR CORE |
| 0 | **RFI (general)**: Information gathering without clear advisory scope - LOW VALUE |

---

### 4. Strategic Value (15 points max)

Does winning this tender advance marcov's strategic objectives?

| Score | Strategic Factor |
|-------|------------------|
| 15 | **High strategic value**: Opens new Tier 1 client, reference project, or growth sector (water, defence) |
| 12 | **Good strategic value**: Strengthens existing relationship or sector presence |
| 8 | **Moderate strategic value**: Profitable work but no strategic uplift |
| 4 | **Low strategic value**: Keeps team busy but no lasting benefit |
| 0 | **No strategic value**: Could damage brand or distract from priorities |

---

### 5. Competitive Position (10 points max)

What is our likely win probability based on competitive factors?

| Score | Position |
|-------|----------|
| 10 | **Strong position**: Known to client, no incumbent, our niche |
| 8 | **Good position**: Some relationship, incumbent is weak |
| 6 | **Neutral position**: Open competition, level playing field |
| 4 | **Challenging position**: Strong incumbent, we're unknown |
| 2 | **Difficult position**: Incumbent has advantage, we have no differentiator |
| 0 | **Unwinnable**: Wired for competitor, mandatory credentials we lack |

---

## Scoring Process

### Phase 1: Initial Screen (Automated)
For each tender from the scraper, calculate:

```
Total Score = Domain Fit + Industry Match + Service Type + Strategic Value + Competitive Position
```

### Phase 2: Threshold Filter
- **≥80 points**: Pass to deep assessment
- **60-79 points**: Flag for manual review
- **<60 points**: Auto-decline (log reason)

### Phase 3: Deep Assessment
For tenders scoring ≥80, generate full pursuit package.

---

## Scoring Output Format

```json
{
  "tender_id": "12345",
  "title": "Asset Management Strategy Review",
  "total_score": 85,
  "threshold_met": true,
  "scores": {
    "domain_fit": { "score": 30, "max": 30, "rationale": "Direct match - asset management strategy" },
    "industry_match": { "score": 25, "max": 25, "rationale": "Rail sector - core strength" },
    "service_type": { "score": 20, "max": 20, "rationale": "Advisory/strategy work" },
    "strategic_value": { "score": 8, "max": 15, "rationale": "Existing client, no major strategic uplift" },
    "competitive_position": { "score": 2, "max": 10, "rationale": "Incumbent has strong relationship" }
  },
  "recommendation": "PURSUE",
  "flags": ["incumbent_risk"]
}
```

---

## Manual Override Triggers

Even if score is <80, flag for review if:
- Tender is from a strategic target client (Tier 1)
- Value is >$500K (worth pursuing for revenue)
- Opens door to new sector we're targeting
- Competitor we want to displace is incumbent

Even if score is ≥80, flag for review if:
- Closing date is <7 days (resource constraints)
- Estimated value is <$20K (may not be worth effort)
- Requires certifications we need to verify

---

*This scoring matrix drives the initial assessment phase of the tender-assessment skill.*
