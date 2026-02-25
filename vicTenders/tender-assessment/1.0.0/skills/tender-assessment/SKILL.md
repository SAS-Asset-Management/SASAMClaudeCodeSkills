---
name: tender-assessment
description: Scrape Victorian government tenders, score alignment to marcov capabilities, and generate pursuit packages for qualified opportunities
---

# Tender Assessment Skill

Automated tender discovery, alignment scoring, and pursuit package generation for marcov's government tender opportunities.

## Overview

This skill provides an end-to-end tender assessment workflow:

1. **Scrape** - Fetch current open tenders from tenders.vic.gov.au
2. **Score** - Apply weighted alignment matrix against marcov's capabilities
3. **Shortlist** - Identify tenders ≥80% aligned
4. **Deep Assess** - Generate full pursuit packages for shortlisted opportunities

### What This Skill Delivers

- Shortlist report with all assessed tenders and recommendations
- Full pursuit packages for high-alignment opportunities including:
  - Go/No-Go recommendation with rationale
  - Competitive positioning and win themes
  - Draft response outline
  - Team requirements
  - Risk matrix
  - Pricing considerations

---

## Reference Files

Load these before processing:

- **Company Profile**: `references/company-profile.md` - marcov's capabilities, industries, constraints
- **Scoring Matrix**: `references/scoring-matrix.md` - Weighted alignment criteria
- **Pursuit Package Template**: `references/pursuit-package-template.md` - Deep assessment output format
- **Shortlist Report Template**: `references/shortlist-report-template.md` - Summary report format

---

## Discovery Process

Before running the assessment, confirm the following with the user:

### Required Context

1. **Scraper location**: Where is `vic_tenders_scraper.py` located?
   - Default: Current working directory
   - May need full path

2. **Keyword filtering**: Use default marcov keywords or custom?
   - Default keywords cover asset management, reliability, rail, etc.
   - User may want to add/remove keywords

3. **New tenders only?**:
   - `--new-only` flag for last 24 hours
   - `--track-new` to compare against previously seen
   - Or all currently open tenders

4. **Output preferences**:
   - Shortlist report only
   - Shortlist + pursuit packages for all ≥80%
   - Shortlist + pursuit packages for top N only

### Skip Discovery If

User provides explicit instructions like:
- "Run the tender assessment on all current tenders"
- "Assess new tenders from today"
- "Generate pursuit packages for the top 3 aligned tenders"

---

## Workflow

### Phase 1: Scrape Tenders

Execute the Victorian tenders scraper to get current open opportunities.

```bash
# Default: All open tenders with marcov keywords
python vic_tenders_scraper.py --all-keywords --pretty

# New tenders only (last 24h)
python vic_tenders_scraper.py --all-keywords --new-only --pretty

# Track genuinely new (vs previously seen)
python vic_tenders_scraper.py --all-keywords --track-new --pretty
```

**Output**: JSON array of tender objects with:
- `id`, `rfx_number`, `title`, `issuer`
- `categories` (UNSPSC)
- `date_opened`, `date_closing`
- `url` (link to tender detail page)
- `matched_keywords` (if keyword filtering applied)

### Phase 2: Initial Assessment (Scoring)

For each tender, calculate alignment score using the weighted matrix:

| Dimension | Weight | Assessment Basis |
|-----------|--------|------------------|
| Domain Fit | 30 pts | Keywords, title, categories vs marcov services |
| Industry Match | 25 pts | Issuer, sector vs marcov target industries |
| Service Type | 20 pts | Tender type, scope vs marcov offerings |
| Strategic Value | 15 pts | Client tier, sector priority, reference potential |
| Competitive Position | 10 pts | Relationship, incumbent status, differentiators |

#### Scoring Guidelines

**Domain Fit** (30 points):
- 30: Direct match to core service (RCM, ISO 55001, asset strategy, predictive maintenance)
- 25: Adjacent service (CMMS, condition monitoring, reliability)
- 20: Related domain (data analytics for assets, maintenance optimisation)
- 15: Tangential but achievable (general consulting in our industries)
- 10: Requires stretch or partnering
- 0: Outside domain entirely

**Industry Match** (25 points):
- 25: Rail, rolling stock, tram, public transport
- 22: Water, wastewater, utilities
- 20: Energy (generation, T&D)
- 18: Mining, resources
- 15: Healthcare facilities
- 12: Local government
- 10: Defence, federal
- 5: Other
- 0: Outside scope (IT, construction, retail)

**Service Type** (20 points):
- 20: Advisory/strategy (consulting, review, assessment)
- 18: Technical analysis (RCM, FMEA, reliability studies)
- 15: Implementation support (change management, training)
- 12: Hybrid advisory + operational
- 8: Managed services
- 5: Labour hire
- 0: Not applicable (construction, manufacturing)

**Strategic Value** (15 points):
- 15: Opens new Tier 1 client, reference project, growth sector
- 12: Strengthens existing relationship or sector presence
- 8: Profitable but no strategic uplift
- 4: Keeps team busy, no lasting benefit
- 0: Could damage brand or distract

**Competitive Position** (10 points):
- 10: Known to client, no incumbent, our niche
- 8: Some relationship, weak incumbent
- 6: Open competition, level field
- 4: Strong incumbent, we're unknown
- 2: Incumbent has advantage, no differentiator
- 0: Wired for competitor, missing credentials

### Phase 3: Categorise Results

Based on total score:

| Score | Category | Action |
|-------|----------|--------|
| ≥80 | **Shortlisted** | Generate full pursuit package |
| 60-79 | **Flagged** | Include in report for manual review |
| <60 | **Declined** | Log with reason, no further action |

#### Override Triggers

**Upgrade to review even if <80**:
- Strategic target client (Tier 1 government agency)
- Value >$500K
- Opens door to growth sector (water, defence)

**Flag for review even if ≥80**:
- Closing <7 days (resource risk)
- Estimated value <$20K (effort vs return)
- Requires unverified certifications

### Phase 4: Generate Shortlist Report

Create summary report using `references/shortlist-report-template.md`:

1. Dashboard with counts and metrics
2. Shortlisted tenders with quick assessments
3. Flagged tenders with review rationale
4. Auto-declined tenders with reasons
5. Upcoming deadline warnings
6. Recommended actions

### Phase 5: Deep Assessment (Pursuit Packages)

For each shortlisted tender (≥80%):

#### 5.1 Fetch Full Tender Details

Use WebFetch to retrieve the tender detail page:

```
URL: {tender.url}
Prompt: Extract all tender details including:
- Full description and scope of work
- Mandatory requirements
- Evaluation criteria
- Contract value (if stated)
- Contract duration
- Key dates (briefing, Q&A, submission)
- Required certifications or qualifications
- Incumbent information (if mentioned)
- Any attachments or documents referenced
```

#### 5.2 Generate Pursuit Package

Using `references/pursuit-package-template.md`, create comprehensive assessment:

1. **Executive Summary**: Recommendation, win probability, strategic importance
2. **Opportunity Overview**: Scope, dates, deliverables
3. **Go/No-Go Analysis**: Reasons to pursue, reasons for caution
4. **Competitive Positioning**: Differentiators, win themes, competitor analysis
5. **Response Strategy**: Approach, key points, weaknesses to address
6. **Draft Response Outline**: Proposed structure, proof points
7. **Team Requirements**: Proposed team, capacity check, subcontracting needs
8. **Risk Assessment**: Bid risks, delivery risks, commercial risks
9. **Pricing Considerations**: Preliminary estimate, pricing strategy
10. **Next Steps**: Immediate actions, response timeline

---

## Output Formats

### Option 1: Shortlist Report Only

Generate `tender-shortlist-[DATE].md` with:
- Summary dashboard
- Categorised tender list
- Quick assessments
- Recommended actions

### Option 2: Full Assessment Package

Generate:
1. `tender-shortlist-[DATE].md` - Summary report
2. `pursuit-[RFX_NUMBER].md` - One file per shortlisted tender

### Option 3: HTML Report

Generate interactive HTML with:
- Filterable tender table
- Expandable assessment cards
- Deadline countdown timers

---

## Example Usage

### Basic Assessment
```
User: "Run tender assessment"
Action:
1. Run scraper with default keywords
2. Score all tenders
3. Generate shortlist report
4. Generate pursuit packages for ≥80% aligned
```

### New Tenders Only
```
User: "Check for new tenders today"
Action:
1. Run scraper with --new-only flag
2. Score new tenders only
3. Generate shortlist report
```

### Specific Tender Deep Dive
```
User: "Generate a pursuit package for tender RFT-12345"
Action:
1. Fetch tender details from URL
2. Score against matrix
3. Generate full pursuit package regardless of score
```

---

## Company Profile Summary

**marcov** (SAS Asset Management) specialises in:

### Core Services
- Asset management strategy (ISO 55001, GFMAM)
- Reliability engineering (RCM, FMEA, RCA)
- Predictive maintenance and analytics
- CMMS/EAM advisory (Maximo, SAP PM)
- Condition monitoring strategy

### Target Industries (Priority)
1. Rail & rolling stock
2. Public transport (tram, bus)
3. Water & wastewater
4. Energy (generation, T&D)
5. Mining & resources
6. Healthcare facilities
7. Local government
8. Defence

### Constraints
- Team: ~11 FTE
- Sweet spot: $50K-$500K contracts
- Geographic: Victoria primary, national capability
- Capacity: 8-12 concurrent projects

### Differentiators
- Practitioner-led (worked in maintenance roles)
- Technology/vendor agnostic
- Sovereign AI capability (edge/on-premise)
- Deep ISO 55001 and GFMAM expertise
- Rail specialism

See `references/company-profile.md` for full details.

---

## Scoring Matrix Quick Reference

| Dimension | Weight | Top Score Criteria |
|-----------|--------|-------------------|
| Domain Fit | 30 | Direct match to core service |
| Industry Match | 25 | Rail/transport sector |
| Service Type | 20 | Advisory/strategy work |
| Strategic Value | 15 | Opens Tier 1 client or growth sector |
| Competitive Position | 10 | Known to client, our niche |

**Pass threshold**: ≥80 points

See `references/scoring-matrix.md` for full rubric.

---

## Integration Notes

### Scraper Location
The skill expects `vic_tenders_scraper.py` to be accessible. If not in the current directory, ask the user for the path.

### State Management
The scraper supports `--track-new` with a state file (`seen_tender_ids.json`) to identify genuinely new tenders. This persists across runs.

### API Usage
Deep assessment uses Claude API (via the skill execution context) to:
- Interpret tender requirements
- Generate pursuit strategy
- Draft response outlines

No external API keys required beyond the Claude Code session.

---

## Error Handling

### Scraper Fails
- Check network connectivity
- Verify tenders.vic.gov.au is accessible
- Review scraper logs for specific errors

### WebFetch Fails
- Tender detail page may require authentication
- Fall back to public information only
- Flag for manual document download

### Insufficient Information
- If tender details are sparse, generate partial pursuit package
- Flag gaps requiring manual research
- Note limitations in output

---

*This skill is designed for marcov's Victorian government tender pipeline. Adjust the company profile and scoring matrix for different organisations or jurisdictions.*
