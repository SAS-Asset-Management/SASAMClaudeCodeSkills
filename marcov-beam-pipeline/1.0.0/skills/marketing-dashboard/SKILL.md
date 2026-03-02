---
name: MBP:marketing-dashboard
description: Aggregate Google Ads, LinkedIn Ads, and website analytics into a unified cross-channel marketing report. Use when the user wants to compare channel performance, optimise budget allocation, analyse attribution, or connect marketing activity to the BEAM sales pipeline. Reads output from MBP:google-ads, MBP:linkedin-ads, MBP:website-analytics, MBP:seo, and MBP:content-intel. Part of the Marcov Beam Pipeline.
---

# Cross-Channel Marketing Dashboard Skill

Aggregate performance data from all marketing channels into a unified view. This is the **aggregation layer** — it answers the question: *"Where should we spend our next marketing dollar?"*

## Overview

This skill helps you:

- **Compare channels side by side**: Google Ads vs LinkedIn Ads vs Organic in a single normalised view
- **Optimise budget allocation**: Data-driven recommendations on where to shift spend for maximum return
- **Analyse attribution**: Reconcile platform-reported conversions with GA4, identify over-counting and multi-touch paths
- **Bridge marketing to sales**: Connect marketing activity to active BEAM engagements and calculate marketing-influenced pipeline value
- **Report to stakeholders**: Generate executive-ready cross-channel reports with clear findings and prioritised actions

## Data Sources

This skill reads the output from other Marcov Beam Pipeline skills:

| Source | File | Required |
|--------|------|----------|
| Google Ads | `.marketing/google-ads/latest.json` | Yes (or manual) |
| LinkedIn Ads | `.marketing/linkedin-ads/latest.json` | Yes (or manual) |
| Website Analytics | `.marketing/website/latest.json` | Yes (or manual) |
| SEO | `.marketing/seo/latest.json` | Optional |
| Content Intelligence | `.marketing/content-intel/latest.json` | Optional |
| BEAM Engagements | `.beam/engagements/*.json` | Optional |

## Invocation Examples

```
/marketing-dashboard                              # Full cross-channel report
/marketing-dashboard budget                       # Budget optimisation focus
/marketing-dashboard attribution                  # Attribution analysis focus
/marketing-dashboard beam                         # BEAM pipeline bridge only
/marketing-dashboard last 90 days                 # Specific reporting period
/marketing-dashboard compare Google vs LinkedIn   # Head-to-head comparison
```

---

## Data Source Detection

Before beginning analysis, check for available data sources.

### Detection Sequence

1. Check for `.marketing/google-ads/latest.json`
2. Check for `.marketing/linkedin-ads/latest.json`
3. Check for `.marketing/website/latest.json`
4. Check for `.marketing/seo/latest.json` (optional — enriches organic analysis)
5. Check for `.marketing/content-intel/latest.json` (optional — enriches content performance)
6. Check for `.beam/engagements/` directory (optional — enables pipeline bridge)

### If Data Sources Are Missing

**If any of the three required sources are missing**, guide the user:

```
I need data from at least one paid channel and website analytics to build a cross-channel report.

Missing sources:
- Google Ads → Run MBP:google-ads first, or provide a summary manually
- LinkedIn Ads → Run MBP:linkedin-ads first, or provide a summary manually
- Website Analytics → Run MBP:website-analytics first, or provide a summary manually

Which would you like to do?
1. Run the missing skill(s) now
2. Provide summary data manually
3. Proceed with available data only (partial report)
```

### Manual Data Entry Fallback

If the user opts to provide data manually, accept summary-level metrics per channel:

- **Paid channels**: Spend, impressions, clicks, conversions, conversion value (AUD)
- **Organic/website**: Sessions, users, goal completions, conversion paths
- **SEO**: Organic traffic, keyword rankings, domain authority changes
- **Content**: Content pieces published, engagement metrics, traffic driven

---

## Discovery Interview

Before generating the report, gather context to tailor the analysis.

### Questions to Ask

1. **Budget & Allocation**
   - What is the total monthly marketing budget across all channels?
   - What is the current budget split? (e.g., 60% Google, 30% LinkedIn, 10% content)

2. **Objectives & Targets**
   - What is the primary marketing objective? (Lead volume, lead quality, brand awareness, pipeline value)
   - What is the acceptable cost per lead?
   - What is the acceptable cost per opportunity?

3. **BEAM Context**
   - Are there active BEAM engagements that marketing is supporting?
   - Should we correlate marketing touchpoints with specific deals?

4. **Reporting Parameters**
   - What reporting period? (Last 30 / 60 / 90 days)
   - Are there any upcoming campaigns or planned budget changes?
   - Who is the audience for this report? (Marketing team, executive leadership, board)

### If the User Skips Discovery

Proceed with sensible defaults:
- Reporting period: last 30 days
- Objective: blended (lead volume + efficiency)
- Currency: AUD
- Include all available data sources

---

## Analysis Phases

### Phase 1: Cross-Channel Performance Summary

Build a unified, side-by-side view of all channels with normalised metrics.

**Actions:**

1. Load data from all detected sources
2. Normalise all currency values to AUD
3. Align metric definitions across platforms:
   - "Conversions" = platform-reported conversions (note: definitions vary)
   - "Cost per Conversion" = spend / conversions
   - "Conversion Rate" = conversions / clicks (paid) or conversions / sessions (organic)
   - "ROAS" = conversion value / spend (paid channels only)
4. Build the cross-channel summary table

**Output Table:**

| Metric | Google Ads | LinkedIn Ads | Organic (Web) | SEO | Content | **Total** |
|--------|-----------|-------------|---------------|-----|---------|-----------|
| Spend | $X | $X | — | — | $X | $X |
| Impressions | X | X | — | X | X | X |
| Clicks / Sessions | X | X | X | X | X | X |
| Conversions | X | X | X | — | — | X |
| Conversion Value | $X | $X | $X | — | — | $X |
| Cost per Conversion | $X | $X | — | — | — | $X |
| Conversion Rate | X% | X% | X% | — | — | X% |
| ROAS | X.Xx | X.Xx | — | — | — | X.Xx |
| Channel Contribution | X% | X% | X% | X% | X% | 100% |

**Channel Contribution Calculation:**
```
Channel contribution % = channel conversions / total conversions * 100
```

---

### Phase 2: Channel Efficiency Comparison

Compare channels on a like-for-like basis to identify the most efficient performers.

**Efficiency Table:**

| Metric | Google Ads | LinkedIn Ads | Organic | Best Performer |
|--------|-----------|-------------|---------|----------------|
| Cost per Conversion | $X | $X | $X | [Channel] |
| Conversion Rate | X% | X% | X% | [Channel] |
| ROAS | X.Xx | X.Xx | — | [Channel] |
| Cost per Click/Session | $X | $X | — | [Channel] |
| Impression to Click Rate | X% | X% | — | [Channel] |

**Analysis Points:**

- Identify the most efficient channel per conversion type (leads, opportunities, revenue)
- Calculate quality-adjusted efficiency if lead quality data is available:
  ```
  Quality-adjusted CPA = Cost per Conversion / Lead-to-Opportunity Rate
  ```
- Flag channels where efficiency has improved or declined vs prior period
- Note significant differences between platforms (e.g., LinkedIn higher CPA but better lead quality)

---

### Phase 3: Attribution & Overlap Analysis

Reconcile platform-reported conversions with GA4-reported conversions to understand the true picture.

**Attribution Reconciliation Table:**

| Metric | Google (Platform) | Google (GA4) | LinkedIn (Platform) | LinkedIn (GA4) | Variance |
|--------|------------------|-------------|--------------------|--------------------|----------|
| Conversions | X | X | X | X | X% |
| Conv Value | $X | $X | $X | $X | X% |

**Analysis Points:**

1. **Over-counting estimation**: Platforms typically over-report by 15-40%. Calculate the total platform-reported conversions vs GA4-reported conversions
   ```
   Over-count ratio = (Sum of platform conversions - GA4 total conversions) / GA4 total conversions
   ```

2. **Multi-touch attribution from GA4 conversion paths**:
   - First-touch channel distribution (what starts journeys?)
   - Last-touch channel distribution (what closes journeys?)
   - Assisted conversions by channel (what supports journeys?)

3. **Channel Overlap**:
   - What percentage of converting users touched multiple paid channels?
   - Common conversion paths (e.g., LinkedIn impression → Google search → conversion)

4. **Adjusted Performance**:
   - Recalculate CPA and ROAS using GA4 attribution rather than platform-reported numbers
   - Present both views: platform-reported vs GA4-adjusted

---

### Phase 4: Budget Optimisation Recommendations

Use marginal efficiency analysis to recommend budget reallocation.

**Marginal Efficiency Assessment:**

1. **Which channel has the lowest marginal cost per conversion?**
   - If a channel is converting well below target CPA, it likely has room for more spend

2. **Budget-constrained channels**:
   - Google: Check impression share lost to budget (from Google Ads data)
   - LinkedIn: Check if daily budgets are hitting caps consistently
   - If impression share is lost to budget, the channel could convert more with additional spend

3. **Diminishing returns channels**:
   - Channels where CPA has been rising period-over-period
   - Channels where frequency is high and incremental conversions are declining

4. **Recommended reallocation table**:

| Channel | Current Spend | Current % | Recommended Spend | Recommended % | Change | Expected Impact |
|---------|--------------|-----------|-------------------|---------------|--------|-----------------|
| Google Ads | $X | X% | $X | X% | +/-$X | +/- X conversions |
| LinkedIn Ads | $X | X% | $X | X% | +/-$X | +/- X conversions |
| Content/SEO | $X | X% | $X | X% | +/-$X | +/- X sessions |
| **Total** | **$X** | **100%** | **$X** | **100%** | **$0** | — |

**Rules for Recommendations:**

- Never recommend increasing total spend unless the user specifically asks for growth scenarios
- Base reallocation on marginal efficiency, not average efficiency
- Consider lead quality, not just volume
- Account for minimum viable spend per channel (e.g., don't recommend $500/month on LinkedIn if the minimum effective budget is $2,000)
- Flag if any channel should be paused entirely (with rationale)

---

### Phase 5: Funnel Analysis

Map the full marketing funnel by channel to identify where each contributes most and where prospects drop off.

**Full-Funnel View:**

| Stage | Google Ads | LinkedIn Ads | Organic | Total | Drop-off |
|-------|-----------|-------------|---------|-------|----------|
| Awareness (Impressions) | X | X | X | X | — |
| Interest (Clicks/Sessions) | X | X | X | X | X% |
| Consideration (Engaged Sessions) | X | X | X | X | X% |
| Conversion (Leads) | X | X | X | X | X% |
| Qualification (MQLs) | X | X | X | X | X% |
| Opportunity (SQLs) | X | X | X | X | X% |

**Analysis Points:**

1. **Channel strength by funnel stage**:
   - Which channel drives the most awareness? (Typically LinkedIn for B2B)
   - Which channel drives the most conversions? (Typically Google for intent-based)
   - Which channel has the best lead quality? (Highest MQL-to-SQL rate)

2. **Funnel drop-off analysis**:
   - Biggest drop-off point per channel
   - Overall funnel conversion rate (impressions to opportunity)
   - Channel-specific funnel conversion rates

3. **Channel synergy patterns**:
   - Does LinkedIn awareness lead to Google search conversions?
   - Does content engagement correlate with paid conversion rates?
   - Are there cross-channel sequences that outperform single-channel journeys?

---

### Phase 6: BEAM Pipeline Bridge (Unique to SAS-AM)

Connect marketing activity to active BEAM sales engagements. This is the bridge between marketing spend and pipeline value.

**Prerequisites:**
- `.beam/engagements/` directory exists with engagement JSON files
- At least one marketing data source is available

**Process:**

1. Load all engagement files from `.beam/engagements/*.json`
2. For each engagement, search marketing data for matching company/contact touchpoints
3. Map marketing touchpoints to engagement timeline:
   - Was this prospect reached by paid advertising before the engagement started?
   - What content did they engage with?
   - What was the first marketing touchpoint? (First-touch attribution)
   - What touchpoints occurred during the engagement? (Engagement nurture)

4. Calculate marketing-influenced pipeline:
   ```
   Marketing-influenced pipeline = Sum of deal values where marketing touchpoints occurred
   Marketing ROI = Marketing-influenced pipeline value / Total marketing spend
   ```

5. **Write back to BEAM**: Add a `marketing_attribution` object into each relevant `.beam/engagements/*.json` file:

```json
{
  "marketing_attribution": {
    "first_touch_channel": "LinkedIn Ads",
    "first_touch_date": "2026-01-15",
    "first_touch_campaign": "Data Engineering Decision Makers",
    "touchpoints": [
      {
        "date": "2026-01-15",
        "channel": "LinkedIn Ads",
        "type": "ad_click",
        "campaign": "Data Engineering Decision Makers"
      },
      {
        "date": "2026-01-22",
        "channel": "Organic",
        "type": "website_visit",
        "pages": ["case-studies/rail-asset-management"]
      },
      {
        "date": "2026-02-01",
        "channel": "Google Ads",
        "type": "ad_click",
        "campaign": "Asset Management Software"
      }
    ],
    "total_marketing_spend_attributed": 450.00,
    "attribution_model": "linear",
    "last_updated": "2026-03-02T10:00:00Z"
  }
}
```

**Marketing-Influenced Deals Table:**

| Company | BEAM Stage | Deal Value | First Touch | Marketing Spend | ROI |
|---------|-----------|------------|-------------|-----------------|-----|
| [Company] | [Stage] | $X | [Channel] | $X | X.Xx |
| **Total** | — | **$X** | — | **$X** | **X.Xx** |

---

### Phase 7: Executive Summary & Next Actions

Synthesise all findings into an actionable executive summary.

**Key Findings** (3-5 bullet points):
- Identify the single most important insight from the analysis
- Highlight the biggest efficiency win or gap
- Note any attribution discrepancies that change the picture
- Flag any channel that is significantly over- or under-performing
- Connect marketing performance to pipeline outcomes (if BEAM data available)

**Prioritised Actions** (3-5 items):
- Each action should be specific, measurable, and time-bound
- Rank by expected impact (highest first)
- Include owner where appropriate
- Distinguish between quick wins (this week) and strategic changes (this month/quarter)

**Recommended Review Cadence:**
- Weekly: Budget pacing check, anomaly review
- Fortnightly: Channel efficiency comparison, CPA trends
- Monthly: Full cross-channel report (this report)
- Quarterly: Strategic review, budget reallocation, objective reassessment

**Suggested Agenda for Next Marketing Review:**
1. Review key metrics vs targets (5 min)
2. Channel efficiency trends (10 min)
3. Attribution findings (10 min)
4. Budget reallocation decisions (15 min)
5. BEAM pipeline bridge update (10 min)
6. Actions and owners (10 min)

---

## Output Files

### Primary Output

- `cross-channel-report-{date}.md` — Full cross-channel marketing report
  - Use template: `references/cross-channel-report-template.md`
  - Date format: YYYY-MM-DD (e.g., `cross-channel-report-2026-03-02.md`)

### Optional Outputs

- `budget-recommendation-{date}.md` — Detailed budget optimisation recommendation
  - Use template: `references/budget-optimisation-template.md`
  - Generate when budget reallocation is a key focus or significant changes are recommended

- `beam-marketing-attribution-{date}.md` — BEAM pipeline attribution report
  - Use template: `references/beam-marketing-bridge-template.md`
  - Generate when `.beam/engagements/` data is available

### Output Location

Save all reports to the current working directory unless the user specifies otherwise.

---

## Push Notification Integration

If MBP:notifications is configured (`.notifications/config.json` exists), offer to send:

| Notification | Trigger | Type | Message Format |
|-------------|---------|------|----------------|
| Weekly digest | Scheduled | info | "Marketing weekly: $X spend, X conversions, $X CPA" |
| Budget pacing alert | Budget >90% spent with >7 days remaining | warning | "Google Ads budget pacing ahead — 92% spent with 12 days remaining" |
| Anomaly alert | CPA spikes >50% or conversions drop >30% | error | "LinkedIn Ads CPA spike: $X → $X (+65%). Investigate." |
| Report complete | Cross-channel report generated | success | "Cross-channel report generated — blended CPA $X, ROAS X.Xx" |

---

## Data Schemas

### Expected Input: Google Ads (`latest.json`)

```json
{
  "platform": "google_ads",
  "period": { "start": "2026-02-01", "end": "2026-02-28" },
  "currency": "AUD",
  "account_summary": {
    "total_spend": 5000.00,
    "total_impressions": 125000,
    "total_clicks": 3750,
    "total_conversions": 45,
    "total_conversion_value": 22500.00,
    "impression_share": 0.72,
    "impression_share_lost_budget": 0.15,
    "impression_share_lost_rank": 0.13
  },
  "campaigns": []
}
```

### Expected Input: LinkedIn Ads (`latest.json`)

```json
{
  "platform": "linkedin_ads",
  "period": { "start": "2026-02-01", "end": "2026-02-28" },
  "currency": "AUD",
  "account_summary": {
    "total_spend": 3000.00,
    "total_impressions": 85000,
    "total_clicks": 1200,
    "total_conversions": 18,
    "total_conversion_value": 14400.00
  },
  "campaigns": []
}
```

### Expected Input: Website Analytics (`latest.json`)

```json
{
  "platform": "ga4",
  "period": { "start": "2026-02-01", "end": "2026-02-28" },
  "summary": {
    "total_sessions": 8500,
    "total_users": 6200,
    "organic_sessions": 4100,
    "paid_sessions": 2800,
    "direct_sessions": 1600,
    "goal_completions": 72,
    "conversion_rate": 0.0085
  },
  "channel_breakdown": [],
  "conversion_paths": []
}
```

---

## Metric Definitions

To ensure consistency across channels, apply these standard definitions:

| Metric | Definition | Notes |
|--------|-----------|-------|
| **Spend** | Total cost in AUD for the reporting period | Convert from USD/other using period average rate if needed |
| **Impressions** | Number of times an ad or page was shown | Organic impressions = search impressions from GSC |
| **Clicks** | Paid: ad clicks. Organic: click-throughs from search | Not equivalent — note in report |
| **Sessions** | GA4 sessions attributed to the channel | More reliable than platform clicks for cross-channel |
| **Conversions** | Actions defined as valuable (leads, sign-ups, enquiries) | Platform definitions vary — document per channel |
| **Conversion Value** | Monetary value assigned to conversions | May be actual revenue or assigned value |
| **CPA (Cost per Acquisition)** | Spend / Conversions | Only for paid channels |
| **ROAS (Return on Ad Spend)** | Conversion Value / Spend | Only for paid channels |
| **Conversion Rate** | Paid: Conversions / Clicks. Organic: Conversions / Sessions | Note the denominator difference |
| **CTR (Click-Through Rate)** | Clicks / Impressions | Paid channels only |
| **Impression Share** | Impressions / Total eligible impressions | Google Ads specific |

---

## Content Guidelines

### Australian English

Use Australian English spelling throughout:
- analyse (not analyze)
- optimise (not optimize)
- organisation (not organization)
- colour (not color)
- centre (not center)
- programme (not program, unless referring to software)
- licence (noun) / license (verb)
- behaviour (not behavior)
- favour (not favor)
- recognise (not recognize)

### Currency

- Default currency is AUD
- Always prefix currency values with the dollar sign: $5,000.00
- Use comma separators for thousands: $12,500.00
- If source data is in another currency, convert to AUD and note the exchange rate used

### Tone

- Professional and data-driven
- Evidence-based — every recommendation must be supported by data
- Actionable — focus on what to do, not just what happened
- Proportionate — highlight what matters most, do not bury the lead
- Honest — if the data is insufficient for a confident recommendation, say so

---

## Pre-Delivery Checklist

Before delivering the report, verify:

- [ ] All available data sources loaded and validated
- [ ] Currency normalised to AUD across all channels
- [ ] Metric definitions applied consistently
- [ ] Cross-channel summary table is complete and totals check out
- [ ] Channel efficiency comparison includes all active channels
- [ ] Attribution analysis reconciles platform vs GA4 numbers
- [ ] Budget recommendations sum to the same total (reallocation, not growth — unless requested)
- [ ] Funnel analysis covers awareness through to conversion (and opportunity if data available)
- [ ] BEAM pipeline bridge completed (if engagement data available)
- [ ] Executive summary contains 3-5 key findings and 3-5 prioritised actions
- [ ] All percentages, ratios, and calculated fields are mathematically correct
- [ ] Report date and reporting period are clearly stated
- [ ] Australian English spelling used throughout
- [ ] Report saved with correct filename format

---

## Reference Files

- `references/cross-channel-report-template.md` — Full report template with all sections
- `references/budget-optimisation-template.md` — Detailed budget reallocation template
- `references/beam-marketing-bridge-template.md` — BEAM pipeline attribution template
