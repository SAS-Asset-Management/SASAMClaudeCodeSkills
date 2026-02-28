# Marketing Analytics Suite — Implementation Plan

**Date:** 2026-02-28
**Scope:** 4 Claude Code skills for unified marketing intelligence
**Architecture:** Separate per-platform skills + cross-channel aggregator
**Data approach:** MCP-first with CSV/export fallback
**Output:** Strategic recommendation reports (Markdown) feeding into BEAM pipeline

---

## Suite Overview

| Skill | Slash Command | Purpose |
|---|---|---|
| **google-ads-analytics** | `/google-ads-analytics` | Google Ads campaign performance analysis and optimisation recommendations |
| **linkedin-ads-analytics** | `/linkedin-ads-analytics` | LinkedIn Campaign Manager performance analysis and audience insights |
| **website-analytics** | `/website-analytics` | GA4 website traffic, conversion, and attribution analysis |
| **marketing-dashboard** | `/marketing-dashboard` | Cross-channel aggregation, comparison, budget optimisation, and BEAM pipeline attribution |

### Skill Dependencies
```
google-ads-analytics ──┐
                       ├──► marketing-dashboard ──► beam-selling
linkedin-ads-analytics ┤                         ──► push-notifications
                       │
website-analytics ─────┘
```

- Each platform skill operates independently (can be invoked alone)
- `marketing-dashboard` reads outputs from platform skills and produces unified analysis
- Results feed into BEAM selling pipeline (marketing-influenced deals)
- Anomaly alerts and performance digests can trigger push-notifications

---

## Skill 1: google-ads-analytics

### Directory Structure
```
google-ads-analytics/1.0.0/
├── .claude-plugin/plugin.json
└── skills/google-ads-analytics/
    ├── SKILL.md
    └── references/
        ├── google-ads-report-template.md
        ├── gaql-query-library.md
        ├── mcp-setup-guide.md
        └── csv-export-guide.md
```

### plugin.json
```json
{
  "name": "google-ads-analytics",
  "description": "Analyse Google Ads campaign performance using MCP or exported data. Produces strategic recommendations for budget allocation, keyword optimisation, ad copy improvements, and conversion rate optimisation. Supports GAQL queries for live data and CSV/Excel uploads for offline analysis.",
  "version": "1.0.0",
  "author": { "name": "SAS-AM" },
  "license": "MIT",
  "keywords": ["google-ads", "ppc", "sem", "advertising", "analytics", "campaign-optimisation", "marketing"]
}
```

### SKILL.md Outline

**YAML Frontmatter:**
```yaml
---
name: google-ads-analytics
description: Analyse Google Ads campaign performance. Use when the user wants to review Google Ads data, optimise campaigns, assess keyword performance, evaluate ad spend efficiency, or generate performance reports. Supports live data via MCP (mcp-google-ads) and CSV/Excel export upload as fallback.
---
```

**Sections:**

1. **Overview** — What the skill does, when to use it, what it produces

2. **Data Source Detection** (CRITICAL — run first)
   - Check if `google-ads` MCP server is available (attempt a lightweight tool call)
   - If MCP available → use live GAQL queries
   - If not → ask user for exported data (CSV/Excel from Google Ads UI)
   - Guide for CSV export: Google Ads → Reports → Download → CSV

3. **Discovery Interview** (before analysis)
   - What Google Ads account/campaigns are we analysing?
   - What's the primary campaign objective? (Lead generation, brand awareness, website traffic, sales)
   - What's the current monthly budget?
   - What conversion actions are set up? (Form submissions, phone calls, purchases)
   - What's the target CPA (cost per acquisition) or ROAS?
   - How long have these campaigns been running?
   - Are there specific concerns? (Rising costs, declining conversions, wasted spend)

4. **Analysis Workflow**

   **Phase 1: Account Overview**
   - Account-level spend, impressions, clicks, conversions (last 30 days)
   - Campaign-level breakdown with performance comparison
   - Budget utilisation and pacing
   - GAQL: `SELECT campaign.name, campaign.status, metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions, metrics.conversions_value FROM campaign WHERE segments.date DURING LAST_30_DAYS ORDER BY metrics.cost_micros DESC`

   **Phase 2: Campaign Deep-Dive**
   - For each active campaign:
     - Performance trend (daily/weekly)
     - Ad group performance breakdown
     - Top keywords by spend, conversions, and wasted spend
     - Search term analysis (actual queries triggering ads)
     - Quality Score distribution
     - Impression share and lost IS (budget vs rank)
   - GAQL examples provided in `references/gaql-query-library.md`

   **Phase 3: Efficiency Analysis**
   - Cost per conversion by campaign/ad group
   - ROAS calculation and trend
   - Wasted spend identification (clicks with no conversions, low QS keywords)
   - Budget allocation efficiency (are high-performing campaigns budget-constrained?)
   - Device performance comparison (mobile vs desktop conversion rates)
   - Geographic performance (which regions convert best?)

   **Phase 4: Competitive Position**
   - Impression share analysis
   - Search lost IS (budget) → indicates campaigns that could benefit from more budget
   - Search lost IS (rank) → indicates need for bid/quality improvements
   - Auction insights (if available via MCP)

   **Phase 5: Strategic Recommendations**
   Generate recommendations in four categories:
   - **Budget Reallocation:** Move spend from underperforming to high-ROAS campaigns
   - **Keyword Optimisation:** Negative keyword additions, match type adjustments, new keyword opportunities
   - **Ad Copy & Creative:** RSA headline/description improvements based on performance data
   - **Bid Strategy:** Manual vs automated bidding recommendations, target CPA/ROAS adjustments

5. **Output Format**
   - Structured Markdown report using `references/google-ads-report-template.md`
   - Saved as `google-ads-report-{date}.md` in working directory
   - Summary metrics table at top for quick reference
   - Each recommendation has: Finding → Impact → Action → Priority (Critical/High/Medium/Low)

6. **State & Integration**
   - Save report output for `marketing-dashboard` consumption
   - Save as `.marketing/google-ads/latest.json` (normalised metrics JSON)
   - Trigger push-notification if anomalies detected (optional)

### Reference Files

**gaql-query-library.md** — Pre-built GAQL queries for common analyses:
- Account summary (30/60/90 days)
- Campaign performance with daily segments
- Keyword performance with quality score
- Search term report
- Device segmentation
- Geographic performance
- Conversion action breakdown
- Landing page performance
- Budget vs actual spend
- Impression share analysis

**google-ads-report-template.md** — Markdown report template:
- Executive Summary (spend, conversions, ROAS, trend direction)
- Campaign Performance Table
- Top/Bottom Performers
- Wasted Spend Analysis
- Keyword Insights
- Recommendations (prioritised)
- Next Review Date

**mcp-setup-guide.md** — How to set up MCP for Google Ads:
- Google Cloud Console project setup
- OAuth consent screen configuration
- Developer token application
- MCP server installation (cohnen/mcp-google-ads)
- Claude Code MCP configuration
- Testing the connection

**csv-export-guide.md** — How to export data from Google Ads UI:
- Campaigns report export
- Keywords report export
- Search terms report export
- Which columns to include for each export

---

## Skill 2: linkedin-ads-analytics

### Directory Structure
```
linkedin-ads-analytics/1.0.0/
├── .claude-plugin/plugin.json
└── skills/linkedin-ads-analytics/
    ├── SKILL.md
    └── references/
        ├── linkedin-ads-report-template.md
        ├── api-query-library.md
        ├── mcp-setup-guide.md
        ├── csv-export-guide.md
        └── audience-targeting-guide.md
```

### plugin.json
```json
{
  "name": "linkedin-ads-analytics",
  "description": "Analyse LinkedIn Campaign Manager performance using MCP or exported data. Produces strategic recommendations for audience targeting, content strategy, budget allocation, and B2B lead generation optimisation. Supports live data via MCP and CSV export upload.",
  "version": "1.0.0",
  "author": { "name": "SAS-AM" },
  "license": "MIT",
  "keywords": ["linkedin-ads", "campaign-manager", "b2b", "advertising", "social-advertising", "lead-generation", "marketing"]
}
```

### SKILL.md Outline

**Sections:**

1. **Overview** — LinkedIn Ads analysis for B2B marketing, audience insights, professional targeting optimisation

2. **Data Source Detection**
   - Check for LinkedIn Ads MCP server availability
   - If available → use API queries
   - If not → ask for Campaign Manager CSV exports
   - Guide: Campaign Manager → Reporting → Export

3. **Discovery Interview**
   - Which LinkedIn Ad Account(s) are we analysing?
   - What campaign objectives are in use? (Lead generation, website visits, brand awareness, engagement, video views)
   - Are Lead Gen Forms being used? (LinkedIn native forms vs website landing pages)
   - What audience targeting is configured? (Job titles, seniority, company size, industries)
   - What's the monthly LinkedIn ad budget?
   - What does a "good lead" look like for SAS-AM?
   - Are Matched Audiences (retargeting, account lists, contact lists) being used?
   - Is the Insight Tag installed on the website?
   - Is Conversions API (CAPI) configured?

4. **Analysis Workflow**

   **Phase 1: Account Overview**
   - Total spend, impressions, clicks, conversions (last 30 days)
   - Campaign-level breakdown
   - Campaign group performance comparison
   - Budget pacing and utilisation

   **Phase 2: Audience Performance**
   - Demographic breakdown: job function, seniority, company size, industry
   - Which professional segments convert best?
   - Cost per lead by audience segment
   - Matched Audience vs prospecting performance comparison
   - Audience overlap and saturation indicators

   **Phase 3: Creative & Content Analysis**
   - Ad format performance comparison (single image, carousel, video, text, message ads)
   - Top-performing ad copy themes
   - Lead Gen Form completion rates vs website landing page conversion rates
   - Creative fatigue indicators (declining CTR over time)

   **Phase 4: Conversion & Attribution**
   - Conversion tracking health check (Insight Tag + CAPI status)
   - Conversion types and volumes
   - View-through vs click-through attribution breakdown
   - LinkedIn-reported conversions vs GA4-reported conversions (if GA4 data available)

   **Phase 5: B2B-Specific Insights**
   - Account-based marketing alignment (are target accounts being reached?)
   - Lead quality assessment (if lead data available)
   - Funnel stage alignment (awareness campaigns reaching top-of-funnel, conversion campaigns reaching ready buyers)
   - Integration with B2B Research Agent prospects

   **Phase 6: Strategic Recommendations**
   - **Audience Refinement:** Tighten or expand targeting based on performance data
   - **Content Strategy:** What ad formats and messages resonate with asset management professionals
   - **Budget Optimisation:** Shift spend to highest-performing campaigns/audiences
   - **Conversion Tracking:** Improvements to tracking setup (CAPI, Insight Tag, UTM consistency)
   - **LinkedIn + Organic Synergy:** Connect with linkedin-post-generator insights

5. **Output Format**
   - Structured Markdown report using `references/linkedin-ads-report-template.md`
   - Save as `linkedin-ads-report-{date}.md`
   - Save normalised metrics as `.marketing/linkedin-ads/latest.json`

6. **LinkedIn-Specific Context**
   - Higher CPCs than Google Ads (typical for B2B LinkedIn: $5-15 AUD)
   - Value is in professional targeting precision, not volume
   - Lead quality often higher than other platforms for B2B
   - Longer consideration cycles — optimise for pipeline, not immediate conversions

### Reference Files

**linkedin-ads-report-template.md** — Markdown template with:
- Executive Summary (spend, leads, CPL, engagement rate)
- Campaign Performance Table
- Audience Demographic Breakdown
- Creative Performance Comparison
- Lead Quality Assessment
- Recommendations (prioritised)

**api-query-library.md** — Common LinkedIn API queries/patterns

**audience-targeting-guide.md** — LinkedIn targeting best practices for B2B asset management:
- Job titles: Asset Manager, Maintenance Manager, Reliability Engineer, Operations Manager, CTO, CIO
- Industries: Utilities, Mining, Manufacturing, Transport, Government
- Seniority: Director, VP, C-Suite for decision-makers; Manager for influencers
- Company size: 200+ employees
- Matched Audiences: Website retargeting, CRM contact lists, account lists

---

## Skill 3: website-analytics

### Directory Structure
```
website-analytics/1.0.0/
├── .claude-plugin/plugin.json
└── skills/website-analytics/
    ├── SKILL.md
    └── references/
        ├── website-report-template.md
        ├── ga4-query-library.md
        ├── mcp-setup-guide.md
        ├── csv-export-guide.md
        └── utm-taxonomy.md
```

### plugin.json
```json
{
  "name": "website-analytics",
  "description": "Analyse website performance using GA4 data via MCP or exported reports. Assess traffic sources, user behaviour, conversion paths, and content performance. Identifies which marketing channels drive the most valuable website engagement and conversions.",
  "version": "1.0.0",
  "author": { "name": "SAS-AM" },
  "license": "MIT",
  "keywords": ["ga4", "google-analytics", "website", "traffic", "conversions", "seo", "content-performance", "attribution"]
}
```

### SKILL.md Outline

**Sections:**

1. **Overview** — Website analytics as the "truth layer" connecting ads to business outcomes

2. **Data Source Detection**
   - Check for GA4 MCP server
   - If not → ask for GA4 data exports (Explorations → Export, or Looker Studio exports)
   - Alternative: Google Sheets add-on exports, BigQuery exports

3. **Discovery Interview**
   - What website(s) are we analysing? (URL, GA4 property ID)
   - What are the key conversion actions? (Contact form, demo request, whitepaper download, newsletter signup)
   - Are Google Ads and LinkedIn Ads linked/tagged? (Auto-tagging, UTM parameters)
   - What content pillars exist on the website? (Maps to linkedin-post-generator pillar posts)
   - What's the primary business goal for the website? (Lead generation, thought leadership, service awareness)
   - Is there a blog/resource section? What topics perform best?
   - Are events/webinars tracked?

4. **Analysis Workflow**

   **Phase 1: Traffic Overview**
   - Total sessions, users, new vs returning (last 30 days + trend)
   - Traffic source breakdown: organic search, direct, referral, paid search, paid social, email, other
   - Channel grouping performance comparison
   - Device breakdown (desktop vs mobile engagement and conversion rates)

   **Phase 2: Acquisition Source Analysis**
   - Organic search: top landing pages, search queries (if Search Console linked)
   - Paid search (Google Ads): campaign → landing page → conversion mapping
   - Paid social (LinkedIn): UTM-tagged traffic → engagement → conversion mapping
   - Direct: % of traffic, likely brand awareness indicator
   - Referral: which external sites drive traffic

   **Phase 3: Content Performance**
   - Top pages by sessions, engagement, and conversions
   - Blog/resource content performance ranking
   - Pillar content vs general content performance comparison
   - Content that drives conversions vs content that only drives traffic
   - Bounce rate and engagement rate by content section

   **Phase 4: Conversion Analysis**
   - Conversion funnel: Visit → Engage → Convert
   - Conversion rate by traffic source (which channels convert best?)
   - Conversion paths (multi-touch attribution via GA4 attribution reports)
   - Landing page conversion performance
   - Form submission analysis (if event tracking is set up)

   **Phase 5: User Behaviour**
   - Engagement rate and session duration trends
   - Pages per session by traffic source
   - Exit pages (where are users leaving?)
   - User flow analysis (common navigation paths)
   - New vs returning user behaviour differences

   **Phase 6: Strategic Recommendations**
   - **SEO Opportunities:** Content gaps, underperforming pages to optimise
   - **Conversion Optimisation:** Landing page improvements, form optimisation
   - **Content Strategy:** Which topics drive engagement and conversions, what to create more of
   - **Channel Optimisation:** Where to invest more (channels with best conversion rates)
   - **Tracking Improvements:** Missing events, UTM gaps, conversion action setup

5. **Output Format**
   - Structured Markdown report using `references/website-report-template.md`
   - Save as `website-report-{date}.md`
   - Save normalised metrics as `.marketing/website/latest.json`

### Reference Files

**website-report-template.md** — Markdown template

**ga4-query-library.md** — Common GA4 Data API queries

**utm-taxonomy.md** — UTM parameter conventions for SAS-AM:
```
Source values:    google, linkedin, newsletter, event, partner
Medium values:    cpc, paid_social, organic_social, email, referral, display
Campaign format:  {platform}-{objective}-{audience}-{date}
Content format:   {ad-group-or-creative-id}
Term format:      {keyword} (Google Ads only)
```

---

## Skill 4: marketing-dashboard

### Directory Structure
```
marketing-dashboard/1.0.0/
├── .claude-plugin/plugin.json
└── skills/marketing-dashboard/
    ├── SKILL.md
    └── references/
        ├── cross-channel-report-template.md
        ├── budget-optimisation-template.md
        ├── attribution-analysis-template.md
        ├── beam-marketing-bridge-template.md
        └── normalised-metrics-schema.json
```

### plugin.json
```json
{
  "name": "marketing-dashboard",
  "description": "Aggregate Google Ads, LinkedIn Ads, and website analytics into a unified cross-channel marketing report. Compares channel performance, recommends budget allocation, analyses attribution, and connects marketing activity to BEAM sales pipeline. Reads output from google-ads-analytics, linkedin-ads-analytics, and website-analytics skills.",
  "version": "1.0.0",
  "author": { "name": "SAS-AM" },
  "license": "MIT",
  "keywords": ["marketing", "cross-channel", "attribution", "budget-optimisation", "dashboard", "roi", "pipeline"]
}
```

### SKILL.md Outline

**Sections:**

1. **Overview** — The aggregation layer. Joins data from platform skills into a unified marketing picture. Answers: "Where should we spend our next marketing dollar?"

2. **Data Source Detection**
   - Check for `.marketing/google-ads/latest.json` (output from google-ads-analytics)
   - Check for `.marketing/linkedin-ads/latest.json` (output from linkedin-ads-analytics)
   - Check for `.marketing/website/latest.json` (output from website-analytics)
   - If any are missing → guide user to run the relevant platform skill first
   - Alternative: accept manually provided summary data

3. **Discovery Interview**
   - What's the total monthly marketing budget across all channels?
   - What's the current budget split? (e.g., 60% Google Ads, 30% LinkedIn, 10% content)
   - What's the primary marketing objective? (Lead volume, lead quality, brand awareness, pipeline value)
   - What's an acceptable cost per lead / cost per opportunity?
   - Are there active BEAM engagements that marketing is supporting?
   - What reporting period should we analyse? (Last 30/60/90 days)
   - Are there upcoming campaigns or budget changes planned?

4. **Analysis Workflow**

   **Phase 1: Cross-Channel Performance Summary**
   - Side-by-side metrics table: Google Ads vs LinkedIn Ads vs Organic
   - Normalised to common currency (AUD) and common metric definitions
   - Total marketing spend, total conversions, blended cost per conversion
   - Channel contribution to total conversions (pie chart breakdown in Markdown table)

   **Phase 2: Channel Efficiency Comparison**
   | Metric | Google Ads | LinkedIn Ads | Organic/Website |
   |---|---|---|---|
   | Spend | $X | $Y | $0 |
   | Conversions | A | B | C |
   | Cost per Conversion | $X/A | $Y/B | $0 |
   | Conversion Rate | % | % | % |
   | ROAS | ratio | ratio | N/A |

   - Identify most efficient channel per conversion type
   - Compare CPC, CPL, CPA across channels
   - Quality-adjusted comparison (if lead quality data available)

   **Phase 3: Attribution & Overlap Analysis**
   - Platform-reported conversions vs GA4-reported conversions
   - Over-counting estimation (sum of platform conversions vs GA4 total)
   - Multi-touch attribution insights from GA4 conversion paths
   - First-touch vs last-touch attribution by channel
   - Assisted conversions (channels that contribute but don't get last-click credit)

   **Phase 4: Budget Optimisation Recommendations**
   Using marginal efficiency analysis:
   - Which channel has the lowest marginal cost per conversion?
   - Are any channels budget-constrained (Google: impression share lost to budget)?
   - Are any channels showing diminishing returns (rising CPA with increased spend)?
   - Recommended budget reallocation with expected impact

   Format:
   ```markdown
   ### Budget Recommendation

   | Channel | Current Monthly | Recommended | Change | Expected Impact |
   |---|---|---|---|---|
   | Google Ads | $3,000 | $3,500 | +$500 | +8 conversions (capturing lost IS) |
   | LinkedIn Ads | $2,000 | $1,800 | -$200 | -1 conversion (diminishing returns in audience X) |
   | Content/SEO | $500 | $700 | +$200 | Long-term organic growth |
   ```

   **Phase 5: Funnel Analysis**
   - Full-funnel view: Awareness → Consideration → Conversion by channel
   - Where each channel contributes most in the funnel
   - Funnel drop-off points (high clicks but low conversions)
   - Channel synergy patterns (e.g., LinkedIn awareness → Google search → conversion)

   **Phase 6: BEAM Pipeline Bridge** (unique to SAS-AM)
   - If `.beam/engagements/` exists, correlate marketing data with active deals
   - For each BEAM engagement:
     - Was this prospect reached by marketing campaigns?
     - What marketing touchpoints occurred before/during the sales engagement?
     - Which campaigns influenced this deal?
   - Marketing-influenced pipeline value calculation
   - Marketing ROI = pipeline value influenced / total marketing spend

   **Phase 7: Executive Summary & Next Actions**
   - 3-5 key findings (most important insights)
   - 3-5 prioritised actions (what to do next)
   - Recommended review cadence (weekly/fortnightly/monthly)
   - Suggested agenda for next marketing review

5. **Output Format**
   - Primary: `cross-channel-report-{date}.md` using `references/cross-channel-report-template.md`
   - Optional: `budget-recommendation-{date}.md` using `references/budget-optimisation-template.md`
   - Optional: `beam-marketing-attribution-{date}.md` using `references/beam-marketing-bridge-template.md`
   - All saved in working directory

6. **Push Notification Integration**
   - If push-notifications skill is available, offer to send:
     - Weekly performance digest to Teams channel
     - Budget pacing alerts
     - Performance anomaly notifications

### Reference Files

**cross-channel-report-template.md:**
```markdown
# Cross-Channel Marketing Report — {period}

## Executive Summary
- **Total Spend:** ${total_spend} AUD
- **Total Conversions:** {total_conversions}
- **Blended CPA:** ${blended_cpa} AUD
- **Blended ROAS:** {blended_roas}x
- **Period:** {start_date} to {end_date}

### Key Findings
1. {finding_1}
2. {finding_2}
3. {finding_3}

### Priority Actions
1. {action_1} — **{priority}**
2. {action_2} — **{priority}**
3. {action_3} — **{priority}**

---

## Channel Performance Comparison
| Metric | Google Ads | LinkedIn Ads | Organic/Website | Total |
|---|---|---|---|---|
| Spend | | | | |
| Impressions | | | | |
| Clicks | | | | |
| CTR | | | | |
| Conversions | | | | |
| Conv. Rate | | | | |
| CPA | | | | |
| ROAS | | | | |

## Channel Efficiency Analysis
{analysis}

## Attribution Analysis
{attribution}

## Budget Optimisation
{budget_recommendations}

## Funnel Analysis
{funnel}

## BEAM Pipeline Attribution
{beam_bridge}

## Recommendations
### Critical
{critical_recommendations}

### High Priority
{high_recommendations}

### Improvement Opportunities
{improvement_recommendations}

---
*Report generated: {date} | Next review: {next_review_date}*
```

**normalised-metrics-schema.json:**
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "platform": { "enum": ["google-ads", "linkedin-ads", "website"] },
    "period": {
      "type": "object",
      "properties": {
        "start": { "type": "string", "format": "date" },
        "end": { "type": "string", "format": "date" }
      }
    },
    "currency": { "type": "string", "default": "AUD" },
    "metrics": {
      "type": "object",
      "properties": {
        "spend": { "type": "number" },
        "impressions": { "type": "integer" },
        "clicks": { "type": "integer" },
        "ctr": { "type": "number" },
        "cpc": { "type": "number" },
        "conversions": { "type": "number" },
        "conversion_rate": { "type": "number" },
        "cost_per_conversion": { "type": "number" },
        "conversion_value": { "type": "number" },
        "roas": { "type": "number" }
      }
    },
    "campaigns": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "status": { "type": "string" },
          "objective": { "type": "string" },
          "spend": { "type": "number" },
          "impressions": { "type": "integer" },
          "clicks": { "type": "integer" },
          "conversions": { "type": "number" },
          "cpa": { "type": "number" }
        }
      }
    },
    "generated_at": { "type": "string", "format": "date-time" }
  }
}
```

**beam-marketing-bridge-template.md** — Template for connecting marketing data to BEAM engagements

**budget-optimisation-template.md** — Detailed budget recommendation template with scenario modelling

---

## Implementation Sequence

### Phase 1: Foundation (google-ads-analytics + linkedin-ads-analytics)
1. Create directory structures for both skills
2. Write SKILL.md files with full workflow instructions
3. Create reference templates (report templates, query libraries)
4. Create MCP setup guides and CSV export guides
5. Define normalised metrics JSON schema (shared across skills)
6. Create `.marketing/` state directory convention

### Phase 2: Website Layer (website-analytics)
1. Create directory structure
2. Write SKILL.md with GA4 analysis workflow
3. Create UTM taxonomy reference
4. Create report template
5. Ensure UTM conventions align with Google Ads and LinkedIn Ads naming

### Phase 3: Aggregation (marketing-dashboard)
1. Create directory structure
2. Write SKILL.md with cross-channel aggregation logic
3. Create cross-channel report template
4. Create budget optimisation template
5. Create BEAM pipeline bridge template
6. Define push-notification integration patterns

### Phase 4: Integration & Registration
1. Update `marketplace.json` with all 4 new plugins
2. Update `register-commands.sh` compatibility (should auto-detect)
3. Update `.planning/codebase/` documents (STRUCTURE, ARCHITECTURE, INTEGRATIONS, STACK)
4. Test skill registration and invocation

---

## State Management Convention

All marketing analytics skills share a common state directory:

```
.marketing/
├── google-ads/
│   ├── latest.json          # Most recent normalised metrics
│   └── history/
│       └── 2026-02-28.json  # Historical snapshots
├── linkedin-ads/
│   ├── latest.json
│   └── history/
│       └── 2026-02-28.json
├── website/
│   ├── latest.json
│   └── history/
│       └── 2026-02-28.json
└── config.json              # Shared config (budget targets, CPA goals, review cadence)
```

### config.json Schema
```json
{
  "total_monthly_budget": 5500,
  "currency": "AUD",
  "budget_split": {
    "google-ads": 3000,
    "linkedin-ads": 2000,
    "content-seo": 500
  },
  "targets": {
    "max_cpa": 150,
    "min_roas": 3.0,
    "monthly_lead_target": 30
  },
  "review_cadence": "fortnightly",
  "beam_integration": true,
  "push_notifications": {
    "enabled": false,
    "teams_webhook": null,
    "alert_thresholds": {
      "cpa_increase_pct": 25,
      "conversion_drop_pct": 30,
      "budget_pacing_threshold": 0.9
    }
  }
}
```

---

## marketplace.json Additions

```json
{
  "name": "google-ads-analytics",
  "source": "./google-ads-analytics/1.0.0",
  "description": "Analyse Google Ads campaign performance using MCP or exported data. Produces strategic recommendations for budget allocation, keyword optimisation, and conversion rate optimisation.",
  "version": "1.0.0",
  "license": "MIT",
  "keywords": ["google-ads", "ppc", "sem", "advertising", "analytics", "campaign-optimisation"],
  "category": "marketing-analytics",
  "tags": ["google-ads", "ppc", "analytics", "marketing"]
},
{
  "name": "linkedin-ads-analytics",
  "source": "./linkedin-ads-analytics/1.0.0",
  "description": "Analyse LinkedIn Campaign Manager performance using MCP or exported data. Produces strategic recommendations for audience targeting, content strategy, and B2B lead generation optimisation.",
  "version": "1.0.0",
  "license": "MIT",
  "keywords": ["linkedin-ads", "campaign-manager", "b2b", "advertising", "lead-generation"],
  "category": "marketing-analytics",
  "tags": ["linkedin-ads", "b2b", "analytics", "marketing"]
},
{
  "name": "website-analytics",
  "source": "./website-analytics/1.0.0",
  "description": "Analyse website performance using GA4 data via MCP or exports. Assess traffic sources, user behaviour, conversion paths, and content performance to connect marketing activity to business outcomes.",
  "version": "1.0.0",
  "license": "MIT",
  "keywords": ["ga4", "google-analytics", "website", "traffic", "conversions", "seo", "attribution"],
  "category": "marketing-analytics",
  "tags": ["ga4", "website", "analytics", "marketing"]
},
{
  "name": "marketing-dashboard",
  "source": "./marketing-dashboard/1.0.0",
  "description": "Aggregate Google Ads, LinkedIn Ads, and website analytics into unified cross-channel marketing reports. Compare channel performance, optimise budget allocation, analyse attribution, and connect marketing to BEAM sales pipeline.",
  "version": "1.0.0",
  "license": "MIT",
  "keywords": ["marketing", "cross-channel", "attribution", "budget-optimisation", "dashboard", "roi", "pipeline"],
  "category": "marketing-analytics",
  "tags": ["marketing", "cross-channel", "dashboard", "pipeline"]
}
```

---

## MCP Server Recommendations

### Minimum Viable Setup
1. **Google Ads:** `cohnen/mcp-google-ads` — Python, read-only, GAQL support
2. **LinkedIn Ads:** `CData/linkedin-ads-mcp-server-by-cdata` — read-only, mature
3. **GA4:** Direct Python scripts or community MCP server

### Simplified Alternative
- **`amekala/ads-mcp`** — single MCP covering Google + LinkedIn + Meta + TikTok
- Trade-off: less depth per platform but simpler setup and maintenance

### Prerequisites
| Platform | Requirements |
|---|---|
| Google Ads | Google Cloud project, OAuth consent screen, developer token, Google Ads account |
| LinkedIn Ads | LinkedIn Developer app, Marketing API access (Development tier minimum), ad account ID |
| GA4 | Google Cloud project, GA4 property, service account or OAuth credentials |

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| MCP servers not maintained | Medium | High | CSV fallback in every skill; recommend most stable MCPs |
| API rate limits blocking analysis | Low | Medium | Batch queries, cache results in `.marketing/` |
| Attribution data mismatch | High | Medium | Clear documentation of attribution methodology and caveats |
| Token/credential management | Medium | Medium | MCP handles credentials; never store in skill files |
| Platform API changes | Medium | Low | Version-pinned MCP servers; query libraries can be updated independently |
| User doesn't have all platforms | Low | Low | Each skill works independently; marketing-dashboard handles partial data |

---

*Implementation plan: 2026-02-28*
