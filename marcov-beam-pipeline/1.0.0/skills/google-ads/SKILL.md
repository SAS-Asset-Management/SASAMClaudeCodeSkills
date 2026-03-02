---
name: MBP:google-ads
description: Analyse Google Ads campaign performance. Use when the user wants to review Google Ads data, optimise campaigns, assess keyword performance, evaluate ad spend efficiency, or generate performance reports. Supports live data via MCP (mcp-google-ads) and CSV/Excel export upload as fallback. Part of the Marcov Beam Pipeline.
---

# Google Ads Analysis Skill

Analyse Google Ads campaign performance and produce strategic recommendations for budget allocation, keyword optimisation, ad copy improvements, and conversion rate optimisation.

## Overview

This skill provides comprehensive Google Ads performance analysis across five phases:

1. **Account Overview** — Aggregate spend, impressions, clicks, conversions, and budget pacing
2. **Campaign Deep-Dive** — Per-campaign performance, ad group breakdown, keyword and search term analysis
3. **Efficiency Analysis** — Cost per conversion, ROAS, wasted spend identification, device and geographic performance
4. **Competitive Position** — Impression share analysis and lost IS diagnostics
5. **Strategic Recommendations** — Prioritised actions across budget, keywords, ad copy, and bid strategy

The output is a structured Markdown report with normalised metrics JSON for cross-channel aggregation via MBP:marketing-dashboard.

---

## Data Source Detection (Run First)

Before beginning any analysis, determine the data source. Follow this sequence:

### Step 1: Check for MCP Server

Attempt a lightweight tool call to the `mcp-google-ads` server (cohnen/mcp-google-ads). For example, try listing accessible customer accounts:

```
Tool: google-ads / get_accounts
```

**If MCP is available:**
- Confirm the accessible account(s) with the user
- Use live GAQL (Google Ads Query Language) queries for all analysis phases
- Proceed to Discovery Interview

**If MCP is NOT available:**
- Inform the user that the live MCP connection is unavailable
- Ask the user to provide exported data from the Google Ads UI
- Provide the CSV export guide below

### Step 2: CSV Export Guide (Fallback)

If MCP is unavailable, guide the user through exporting data:

```
To export campaign data from Google Ads:

1. Sign in to ads.google.com
2. Navigate to Campaigns (or Keywords, or Search Terms — depending on what you need)
3. Set the date range to the period you want to analyse (e.g., Last 30 days)
4. Add relevant columns:
   - Campaign, Ad group, Status
   - Impressions, Clicks, CTR, Avg. CPC, Cost
   - Conversions, Conv. rate, Cost / conv., Conv. value
   - Search impr. share, Search lost IS (budget), Search lost IS (rank)
   - Quality Score (keyword reports only)
5. Click the download icon (three dots menu → Download)
6. Select CSV or Excel format
7. Provide the downloaded file(s) here

Recommended exports:
- Campaign report (last 30 days)
- Keyword report (last 30 days)
- Search terms report (last 30 days)
```

### Step 3: Data Validation

Regardless of source, validate the data before proceeding:

- Confirm the date range covered
- Check that key metrics are present (impressions, clicks, cost, conversions)
- Verify currency (costs from MCP are in micros — divide by 1,000,000)
- Note any campaigns or metrics that may be missing or filtered out

---

## Discovery Interview (CRITICAL)

**Before analysing any data, you MUST conduct a discovery interview to understand the account context and the user's objectives.**

### Questions to Ask

1. **Account & Campaigns**
   - What Google Ads account or campaigns are we analysing?
   - How many campaigns are active? What types? (Search, Display, Shopping, Video, Performance Max)
   - Are there any campaigns we should exclude from analysis? (e.g., brand-only campaigns assessed separately)

2. **Campaign Objective**
   - What is the primary campaign objective?
     - Lead generation (form submissions, phone calls)
     - Brand awareness (impressions, reach)
     - Website traffic (clicks, sessions)
     - Sales / e-commerce (purchases, revenue)
   - Are different campaigns targeting different objectives?

3. **Budget**
   - What is the current monthly Google Ads budget?
   - Is the budget shared across campaigns or allocated per campaign?
   - Has the budget changed recently? If so, when and by how much?

4. **Conversion Tracking**
   - What conversion actions are set up in Google Ads?
     - Form submissions
     - Phone calls (call tracking or click-to-call)
     - Purchases / transactions
     - Other (e.g., PDF downloads, chat initiations)
   - Are conversion values assigned? If so, how are they calculated?
   - Is the attribution model set to data-driven, last-click, or another model?

5. **Targets**
   - What is the target CPA (cost per acquisition)?
   - What is the target ROAS (return on ad spend)?
   - Are there specific KPIs being reported upstream? (e.g., board reporting, client SLAs)

6. **History & Context**
   - How long have these campaigns been running?
   - Have there been recent changes to campaign structure, bidding strategy, or landing pages?
   - Is there seasonal variation in performance? (e.g., financial year cycles, industry events)

7. **Specific Concerns**
   - Are there specific concerns prompting this analysis?
     - Rising cost per click or cost per conversion
     - Declining conversion rates
     - Wasted spend on irrelevant search terms
     - Poor Quality Scores
     - Competitors appearing more frequently
     - Budget running out before end of day/month

### If the User Provides Data Without Context

If the user provides raw data without answering discovery questions, proceed with what can be determined from the data itself. Clearly note assumptions in the report and flag dimensions that require additional context for a complete assessment.

---

## Analysis Workflow

### Phase 1: Account Overview

Establish the high-level performance picture for the analysis period (default: last 30 days).

**Metrics to gather:**

| Metric | Description |
|---|---|
| Total Spend | Sum of cost across all campaigns (convert from micros if MCP) |
| Total Impressions | Sum of impressions |
| Total Clicks | Sum of clicks |
| Overall CTR | Clicks / Impressions |
| Average CPC | Total Spend / Total Clicks |
| Total Conversions | Sum of conversions |
| Conversion Rate | Conversions / Clicks |
| Cost per Conversion | Total Spend / Total Conversions |
| Total Conversion Value | Sum of conversion value |
| ROAS | Total Conversion Value / Total Spend |

**Campaign-level breakdown:**

For each campaign, report: name, status, type, spend, impressions, clicks, CTR, CPC, conversions, conversion rate, CPA, conversion value, ROAS.

**Budget pacing:**

- Compare actual spend vs daily budget * days elapsed
- Flag campaigns that are consistently limited by budget
- Flag campaigns that are significantly underspending

**Example GAQL query (MCP):**

```sql
SELECT
  campaign.name,
  campaign.status,
  campaign.advertising_channel_type,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value,
  metrics.average_cpc,
  campaign.campaign_budget
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status != 'REMOVED'
ORDER BY metrics.cost_micros DESC
```

---

### Phase 2: Campaign Deep-Dive

For each active campaign, analyse the following:

**2a. Performance Trend**

- Daily or weekly spend, clicks, conversions over the analysis period
- Identify trends: improving, declining, or stable
- Flag any sudden changes (spikes or drops)

**Example GAQL query:**

```sql
SELECT
  campaign.name,
  segments.date,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
ORDER BY segments.date ASC
```

**2b. Ad Group Breakdown**

- Performance by ad group within each campaign
- Identify top and bottom performing ad groups
- Check for ad groups with spend but zero conversions

**Example GAQL query:**

```sql
SELECT
  campaign.name,
  ad_group.name,
  ad_group.status,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value,
  metrics.average_cpc
FROM ad_group
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
  AND ad_group.status = 'ENABLED'
ORDER BY metrics.cost_micros DESC
```

**2c. Top Keywords by Spend and Conversions**

- Top 20 keywords by spend
- Top 20 keywords by conversions
- Keywords with high spend and zero conversions (wasted spend candidates)
- Keywords with low CPA (scale opportunities)

**2d. Search Term Analysis**

- Review actual search terms triggering ads
- Identify irrelevant search terms consuming budget
- Identify high-performing search terms not yet added as keywords
- Recommend negative keyword additions

**2e. Quality Score Distribution**

- Distribution of Quality Scores across keywords (1-10 scale)
- Average Quality Score by campaign and ad group
- Keywords with Quality Score below 5 (improvement targets)
- Quality Score components where available: expected CTR, ad relevance, landing page experience

**2f. Impression Share**

- Search impression share per campaign
- Search lost IS (budget) — percentage of impressions lost due to insufficient budget
- Search lost IS (rank) — percentage of impressions lost due to ad rank (bid + quality)

---

### Phase 3: Efficiency Analysis

**3a. Cost per Conversion Analysis**

- CPA by campaign, ad group, and keyword
- Identify campaigns/ad groups where CPA exceeds the target
- Trend CPA over the analysis period — is it improving or worsening?

**3b. ROAS Calculation**

- ROAS by campaign: conversion value / spend
- Compare against target ROAS
- Identify campaigns delivering above-target and below-target ROAS
- If conversion values are not set, note this limitation and focus on CPA

**3c. Wasted Spend Identification**

Quantify spend that is not generating value:

| Wasted Spend Category | How to Identify |
|---|---|
| Keywords with zero conversions | Spend > $0, Conversions = 0, over 30+ days |
| Low Quality Score keywords | QS <= 3, still accruing spend |
| Irrelevant search terms | Search terms report — no conversion, low relevance |
| High CPA keywords | CPA > 3x target CPA |
| Paused campaigns still spending | Status anomalies |

Sum the total wasted spend and express as a percentage of total spend.

**3d. Budget Allocation Efficiency**

- Are high-performing campaigns (low CPA, high ROAS) budget-constrained?
- Are underperforming campaigns consuming disproportionate budget?
- Calculate the potential impact of reallocating budget from low to high performers

**3e. Device Performance**

- Breakdown by device: desktop, mobile, tablet
- Conversion rate by device
- CPA by device
- Identify devices where bid adjustments may be warranted

**Example GAQL query:**

```sql
SELECT
  campaign.name,
  segments.device,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
```

**3f. Geographic Performance**

- Performance by location (country, state/region, city — depending on targeting granularity)
- Identify high-performing and underperforming geographic areas
- Recommend location bid adjustments or exclusions

**Example GAQL query:**

```sql
SELECT
  campaign.name,
  geographic_view.country_criterion_id,
  geographic_view.location_type,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value
FROM geographic_view
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
ORDER BY metrics.cost_micros DESC
```

---

### Phase 4: Competitive Position

**4a. Impression Share Analysis**

| Metric | Meaning | Action Lever |
|---|---|---|
| Search Impression Share | % of eligible impressions actually received | Overall competitiveness |
| Search Lost IS (Budget) | % of impressions lost because budget ran out | Increase budget or narrow targeting |
| Search Lost IS (Rank) | % of impressions lost because ad rank was too low | Improve bids, Quality Score, or ad relevance |
| Search Exact Match IS | Impression share for exact match keywords only | Keyword-level competitiveness |

**Example GAQL query:**

```sql
SELECT
  campaign.name,
  metrics.search_impression_share,
  metrics.search_budget_lost_impression_share,
  metrics.search_rank_lost_impression_share,
  metrics.search_exact_match_impression_share
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
  AND campaign.advertising_channel_type = 'SEARCH'
ORDER BY metrics.search_budget_lost_impression_share DESC
```

**4b. Budget-Constrained Campaigns**

- Campaigns with Search Lost IS (Budget) > 10% are budget-constrained
- Calculate the estimated additional conversions if budget were increased
- Prioritise campaigns with low CPA + high lost IS (budget) for budget increases

**4c. Rank-Constrained Campaigns**

- Campaigns with Search Lost IS (Rank) > 20% need quality or bid improvements
- Cross-reference with Quality Score data — is the issue bid-related or quality-related?
- Recommend specific actions: raise bids, improve ad relevance, improve landing page experience

---

### Phase 5: Strategic Recommendations

Generate actionable recommendations in four categories. Each recommendation must follow the structure:

```
**Finding:** [What the data shows]
**Impact:** [Quantified or estimated business impact]
**Action:** [Specific steps to take]
**Priority:** [Critical / High / Medium / Low]
```

**5a. Budget Reallocation**

- Shift spend from underperforming campaigns to high-ROAS campaigns
- Increase budgets for budget-constrained campaigns with strong efficiency
- Reduce or pause budgets for campaigns with sustained poor performance
- Consider cross-channel budget shifts (reference MBP:linkedin-ads data if available)

**5b. Keyword Optimisation**

- Add negative keywords based on search term analysis
- Adjust match types (e.g., move high-performing broad match to phrase or exact)
- Pause or remove zero-conversion keywords with significant spend
- Identify new keyword opportunities from high-performing search terms
- Address low Quality Score keywords (improve ad relevance, landing pages)

**5c. Ad Copy and Creative**

- Review RSA (Responsive Search Ad) headline and description performance
- Identify ad groups with limited ad variations
- Recommend headline/description improvements based on top-performing assets
- Check ad strength scores and flag weak ads
- Ensure ads align with landing page messaging

**5d. Bid Strategy Optimisation**

- Assess current bid strategy (manual CPC, maximise conversions, target CPA, target ROAS)
- Recommend strategy changes based on data maturity and conversion volume
  - < 15 conversions/month: manual CPC or maximise clicks
  - 15-30 conversions/month: maximise conversions
  - 30+ conversions/month: target CPA or target ROAS
- Recommend target CPA/ROAS values based on actual performance data
- Device and location bid adjustments based on Phase 3 analysis

---

## Output

### Primary Report

Generate a structured Markdown report saved as `google-ads-report-{YYYY-MM-DD}.md`.

Use the report template from `references/google-ads-report-template.md` as the structural guide. The report must include:

- Executive Summary with headline metrics and trend direction
- Campaign Performance Table
- Top and Bottom Performers
- Wasted Spend Analysis (quantified)
- Keyword Insights
- Impression Share Analysis
- Recommendations (prioritised: Critical, High, Medium, Low)
- Next Review Date

### Normalised Metrics JSON

Save normalised metrics to `.marketing/google-ads/latest.json` following the schema in `shared/normalised-metrics-schema.json`.

**Key mapping notes:**

| Google Ads Field | Normalised Field | Transformation |
|---|---|---|
| `metrics.cost_micros` | `spend` | Divide by 1,000,000 |
| `metrics.impressions` | `impressions` | Direct |
| `metrics.clicks` | `clicks` | Direct |
| `metrics.conversions` | `conversions` | Direct (may be fractional with data-driven attribution) |
| `metrics.conversions_value` | `conversion_value` | Direct |
| Calculated | `ctr` | clicks / impressions |
| Calculated | `cpc` | spend / clicks |
| Calculated | `conversion_rate` | conversions / clicks |
| Calculated | `cost_per_conversion` | spend / conversions |
| Calculated | `roas` | conversion_value / spend |

**Platform value:** `"google-ads"`

**Example normalised output:**

```json
{
  "platform": "google-ads",
  "period": {
    "start": "2026-02-01",
    "end": "2026-02-28"
  },
  "currency": "AUD",
  "metrics": {
    "spend": 12450.00,
    "impressions": 485230,
    "clicks": 14820,
    "ctr": 0.0305,
    "cpc": 0.84,
    "conversions": 312,
    "conversion_rate": 0.021,
    "cost_per_conversion": 39.90,
    "conversion_value": 62400.00,
    "roas": 5.01
  },
  "campaigns": [
    {
      "name": "Search - Asset Management",
      "status": "active",
      "objective": "lead_generation",
      "spend": 5200.00,
      "impressions": 185000,
      "clicks": 6400,
      "conversions": 156,
      "cpa": 33.33,
      "roas": 6.2
    }
  ],
  "top_performers": [
    {
      "name": "iso 55001 assessment",
      "type": "keyword",
      "metric_value": 8.4,
      "metric_name": "roas"
    }
  ],
  "issues": [
    {
      "severity": "high",
      "description": "Campaign 'Display - Awareness' has spent $2,340 with zero conversions in 30 days",
      "recommendation": "Pause campaign and reallocate budget to Search - Asset Management"
    }
  ],
  "generated_at": "2026-03-02T10:30:00+11:00"
}
```

---

## Integration with Other MBP Skills

| Skill | Integration |
|---|---|
| **MBP:marketing-dashboard** | Output `latest.json` feeds cross-channel comparison. Google Ads data is aggregated alongside LinkedIn Ads, website analytics, and SEO data. |
| **MBP:notifications** | Trigger notifications for anomalies: sudden CPA spikes, budget exhaustion, conversion drops, impression share declines. |
| **MBP:linkedin-ads** | Cross-reference LinkedIn Ads performance when making budget reallocation recommendations. If Google Ads CPA is significantly lower than LinkedIn, recommend shifting budget to Google (and vice versa). |
| **shared/utm-taxonomy.md** | Validate that Google Ads campaigns follow the UTM convention: `utm_source=google`, `utm_medium=cpc` (search) or `utm_medium=display`. Campaign names should follow `{platform}-{objective}-{audience}-{YYYYMM}` format. |
| **shared/normalised-metrics-schema.json** | All JSON output must conform to this schema. Platform value is `"google-ads"`. |

---

## Important Notes on Google Ads Data

### Cost Micros

All cost values returned by the Google Ads API (and MCP) are in **micros** — that is, the actual currency amount multiplied by 1,000,000.

```
cost_micros = 12450000000  →  $12,450.00 AUD
average_cpc = 840000       →  $0.84 AUD
```

**Always divide by 1,000,000 before presenting monetary values.** The normalised JSON output must use currency values, not micros.

### GAQL Date Ranges

GAQL uses the `DURING` clause for date ranges with predefined constants:

| Constant | Period |
|---|---|
| `LAST_7_DAYS` | Previous 7 days (excluding today) |
| `LAST_14_DAYS` | Previous 14 days |
| `LAST_30_DAYS` | Previous 30 days |
| `LAST_90_DAYS` | Previous 90 days |
| `THIS_MONTH` | Current calendar month to date |
| `LAST_MONTH` | Previous calendar month |
| `THIS_QUARTER` | Current quarter to date |
| `LAST_QUARTER` | Previous quarter |

For custom date ranges, use:
```sql
WHERE segments.date BETWEEN '2026-01-01' AND '2026-01-31'
```

### Quality Score

- Quality Score is a **keyword-level** metric only (not available at campaign or ad group level)
- Scale: 1 (worst) to 10 (best)
- Components: Expected CTR, Ad Relevance, Landing Page Experience
- Each component is rated: BELOW_AVERAGE, AVERAGE, or ABOVE_AVERAGE
- Quality Score is a snapshot — it reflects current assessment, not historical
- Historical Quality Score requires selecting `historical_quality_score` in GAQL

### Impression Share Metrics

- Impression share values are **decimals** between 0.0 and 1.0 (not percentages)
- `0.65` means 65% impression share
- `search_budget_lost_impression_share` of `0.15` means 15% of eligible impressions were lost due to budget
- These metrics are only available for Search and Shopping campaigns

### Conversion Attribution

- Default attribution model in Google Ads is now **data-driven attribution** (DDA)
- Under DDA, conversions may be **fractional** (e.g., 0.4 conversions attributed to a keyword)
- Conversion values may similarly be fractional
- When reporting, do not round fractional conversions — present as-is to preserve attribution accuracy
- Note the attribution model in the report so the user understands the methodology

---

## Pre-Delivery Checklist

Before delivering the report, verify:

- [ ] Data source confirmed (MCP or CSV) and data validated
- [ ] Discovery interview completed (or assumptions documented)
- [ ] All five analysis phases completed
- [ ] Account Overview includes headline metrics and budget pacing
- [ ] Campaign Deep-Dive covers ad groups, keywords, search terms, Quality Scores, impression share
- [ ] Efficiency Analysis quantifies wasted spend and identifies optimisation opportunities
- [ ] Competitive Position analysis includes impression share diagnostics
- [ ] Recommendations follow Finding → Impact → Action → Priority format
- [ ] Recommendations are categorised: Budget, Keywords, Ad Copy, Bid Strategy
- [ ] Priorities assigned: Critical, High, Medium, Low
- [ ] Cost values converted from micros to currency (if MCP source)
- [ ] Report saved as `google-ads-report-{YYYY-MM-DD}.md`
- [ ] Normalised JSON saved to `.marketing/google-ads/latest.json`
- [ ] JSON conforms to `shared/normalised-metrics-schema.json`
- [ ] UTM conventions validated against `shared/utm-taxonomy.md`
- [ ] Australian English spelling used throughout
- [ ] Next review date set in report

---

## Content Guidelines

### Australian English

Use Australian English spelling throughout:
- analyse (not analyze)
- optimise (not optimize)
- organisation (not organization)
- colour (not color)
- prioritise (not prioritize)
- behaviour (not behavior)
- centre (not center)
- licence (noun) / license (verb)
- maximise (not maximize)

### Tone

- Professional and data-driven
- Evidence-based — every recommendation must cite specific data points
- Actionable — recommendations include specific steps, not vague guidance
- Proportionate — focus on the changes with the greatest potential impact first
- Honest — if performance is poor, say so clearly; do not soften bad news

### Metric Formatting

- Currency: `$12,450.00` (include currency code if ambiguous, e.g., `$12,450.00 AUD`)
- Percentages: `3.05%` (one or two decimal places)
- Large numbers: Use commas as thousands separators (`485,230 impressions`)
- ROAS: Express as a multiple (`5.01x`) or ratio (`5.01:1`)
- Quality Score: Integer only (`QS: 7/10`)
- Dates: `DD MMM YYYY` format (`02 Mar 2026`)

---

## Reference Files

- `references/google-ads-report-template.md` — Report structure template
- `references/gaql-query-library.md` — Pre-built GAQL queries for common analysis tasks

---

## GAQL Quick Reference

See `references/gaql-query-library.md` for the complete query library. Key queries used in each phase:

| Phase | Query Purpose | Reference |
|---|---|---|
| Phase 1 | Account summary by campaign | `gaql-query-library.md` — Account Summary |
| Phase 2 | Daily campaign trends | `gaql-query-library.md` — Campaign Performance with Daily Segments |
| Phase 2 | Keyword performance with QS | `gaql-query-library.md` — Keyword Performance with Quality Score |
| Phase 2 | Search term report | `gaql-query-library.md` — Search Term Report |
| Phase 3 | Device segmentation | `gaql-query-library.md` — Device Segmentation |
| Phase 3 | Geographic performance | `gaql-query-library.md` — Geographic Performance |
| Phase 4 | Impression share analysis | `gaql-query-library.md` — Impression Share Analysis |
