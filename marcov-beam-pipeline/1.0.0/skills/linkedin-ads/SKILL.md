---
name: MBP:linkedin-ads
description: Analyse LinkedIn Campaign Manager performance. Use when the user wants to review LinkedIn Ads data, optimise B2B audience targeting, assess lead quality, evaluate campaign ROI, or generate performance reports. Supports live data via MCP (linkedin-ads MCP servers) and CSV export upload as fallback. Part of the Marcov Beam Pipeline.
---

# LinkedIn Ads Performance Analysis

Analyse LinkedIn Campaign Manager data to assess B2B campaign performance, audience targeting effectiveness, lead quality, and return on investment. Produces a structured Markdown report and normalised metrics JSON for integration with MBP:marketing-dashboard.

## Overview

This skill helps you:

- **Audit LinkedIn Ads performance** — spend, impressions, clicks, conversions, and cost-per-lead across campaigns
- **Evaluate audience targeting** — which job functions, seniority levels, company sizes, and industries are converting best
- **Assess lead quality** — Lead Gen Form performance, completion rates, and downstream lead qualification
- **Check conversion tracking health** — Insight Tag status, Conversions API (CAPI) configuration, attribution gaps
- **Generate strategic recommendations** — audience refinement, creative optimisation, budget reallocation, and tracking improvements
- **Feed the marketing dashboard** — output normalised metrics JSON to `.marketing/linkedin-ads/latest.json` for cross-channel reporting

---

## Input

This skill accepts a **request to analyse LinkedIn Ads performance** as its primary input. The user may provide a specific account, campaign, date range, or simply ask for a general review. Data can come from live MCP connection or CSV exports from Campaign Manager.

### Invocation Examples

```
/linkedin-ads Review our LinkedIn Ads performance for the last 30 days
/linkedin-ads Analyse lead gen campaign performance for Q1 2026
/linkedin-ads Which audience segments are converting best?
/linkedin-ads Audit our conversion tracking setup
/linkedin-ads Compare Lead Gen Forms vs website landing page conversions
/linkedin-ads Generate a performance report for the utilities campaign
```

---

## Data Source Detection (CRITICAL — Do This First)

Before any analysis, determine where the data is coming from. Check in this order:

### Option 1: LinkedIn Ads MCP Server (Preferred)

Check whether a LinkedIn Ads MCP server is available in the current environment.

**Detection steps:**
1. Check for MCP server configuration referencing LinkedIn Ads or LinkedIn Marketing API
2. If available, confirm the connection is live and authenticated
3. Query available ad accounts and confirm which account(s) to analyse

**If MCP is available:** Use it as the primary data source. You can pull real-time data including campaigns, creatives, demographics, conversions, and Lead Gen Form submissions.

### Option 2: CSV Export Upload (Fallback)

If no MCP server is available, ask the user to export data from LinkedIn Campaign Manager.

**Required exports (guide the user):**

| Export | Where to Find It | What It Contains |
|---|---|---|
| **Campaign Performance** | Campaign Manager > Campaigns > Export | Spend, impressions, clicks, conversions by campaign |
| **Demographics** | Campaign Manager > Demographics > Export | Job function, seniority, company size, industry breakdowns |
| **Ad Performance** | Campaign Manager > Ads > Export | Per-ad metrics including creative format |
| **Lead Gen Forms** | Campaign Manager > Account Assets > Lead Gen Forms > Download | Form submissions, completion rates |
| **Conversions** | Campaign Manager > Conversion Tracking > Export | Conversion event definitions and counts |

**Tell the user:**

> "I don't have a live connection to your LinkedIn Ads account. Could you export the following CSVs from Campaign Manager? I need at minimum the Campaign Performance export. Demographics and Lead Gen Form exports are strongly recommended for a thorough analysis."

### Option 3: Manual Data Entry

If exports are not possible, the user can provide key metrics verbally or paste data from the Campaign Manager UI. Flag that analysis depth will be limited.

---

## Discovery Interview (CRITICAL)

**Before analysing any data, you MUST conduct a discovery interview to understand the account context and goals.** Adapt questions based on what the user has already provided.

### Questions to Ask

1. **Account Context**
   - Which LinkedIn Ad Account(s) should I analyse? (Account name or ID)
   - How long has this account been running campaigns?
   - Who manages the account day-to-day? (In-house, agency, or consultant)

2. **Campaign Objectives**
   - What campaign objectives are in use? (Lead generation, website visits, brand awareness, engagement, video views)
   - Which objective is the primary focus right now?
   - Are there different objectives for different audience segments?

3. **Lead Generation Setup**
   - Are Lead Gen Forms being used? (Native LinkedIn forms vs website landing pages)
   - If Lead Gen Forms: what fields are collected? (Name, email, job title, company, custom questions)
   - Where do form submissions go? (CRM integration, CSV download, marketing automation)
   - Are website conversion events also tracked alongside Lead Gen Forms?

4. **Audience Targeting**
   - What audience targeting is configured? (Job titles, job functions, seniority, company size, industries)
   - Are there multiple audience segments running in parallel?
   - Are you targeting specific companies or account lists?

5. **Budget & Spend**
   - What is the monthly LinkedIn Ads budget? (AUD)
   - How is budget allocated across campaigns/objectives?
   - Has budget changed recently? (increases, cuts, pauses)

6. **Lead Quality Definition**
   - What does a "good lead" look like for your business?
   - What job titles, seniority levels, or company types are most valuable?
   - Do you track lead-to-opportunity or lead-to-customer conversion rates?
   - What is an acceptable cost per qualified lead?

7. **Matched Audiences**
   - Are Matched Audiences being used? (Website retargeting, CRM contact lists, account lists, lookalike audiences)
   - Is a website retargeting audience active? (Requires Insight Tag)
   - Have you uploaded company account lists or contact lists?

8. **Tracking & Attribution**
   - Is the LinkedIn Insight Tag installed on your website?
   - Is the Conversions API (CAPI) configured? (Server-side tracking)
   - Do you also track LinkedIn traffic in GA4? (UTM parameters)
   - Are there known gaps in conversion tracking?

9. **Goals for This Analysis**
   - What are you hoping to learn from this analysis?
   - Are there specific concerns or hypotheses you want tested?
   - Is there a decision this analysis needs to inform? (Budget change, audience shift, creative refresh)

### If the User Provides Data Without Context

If the user uploads CSV exports without answering discovery questions, proceed with what can be inferred from the data itself. Clearly note assumptions in the report and flag where additional context would improve the analysis. Mark any assessment that depends on missing context as "Requires additional context" and specify what information is needed.

---

## Analysis Phases

Execute these phases sequentially. Each phase builds on the previous. Present findings incrementally — do not wait until all phases are complete to share results.

### Phase 1: Account Overview

**Objective:** Establish baseline performance for the analysis period (default: last 30 days).

**Metrics to capture:**

| Metric | What to Report |
|---|---|
| **Total Spend** | AUD spend for the period |
| **Impressions** | Total impressions served |
| **Clicks** | Total clicks (landing page clicks preferred over total clicks) |
| **CTR** | Click-through rate (clicks / impressions) |
| **Average CPC** | Cost per click |
| **Conversions** | Total conversions (all types) |
| **Conversion Rate** | Conversions / clicks |
| **Cost per Conversion** | Spend / conversions |
| **Leads** | Lead Gen Form submissions (if applicable) |
| **Cost per Lead (CPL)** | Spend / leads |
| **Engagement Rate** | (Clicks + likes + comments + shares + follows) / impressions |

**Campaign-level breakdown:**

For each active campaign, report:
- Campaign name and objective
- Status (active, paused, completed)
- Budget (daily or lifetime)
- Spend, impressions, clicks, CTR, CPC, conversions, CPL
- Pacing: is the campaign spending its full budget? (underspend may indicate audience saturation)

**Period-over-period comparison (if data available):**
- Current 30 days vs previous 30 days
- Flag significant changes (>20% movement in any key metric)

**LinkedIn Benchmarks for Context:**

| Metric | B2B Benchmark (Australia) | Notes |
|---|---|---|
| CTR (Sponsored Content) | 0.40% – 0.65% | Single image ads typically higher than carousel |
| CPC | AUD $5 – $15 | Higher than Google Ads; reflects targeting precision |
| CPL (Lead Gen Forms) | AUD $30 – $80 | Varies significantly by industry and seniority targeted |
| Engagement Rate | 0.50% – 1.50% | Thought leadership content tends to outperform promotional |
| Lead Gen Form Completion Rate | 10% – 15% | Native forms convert better than website landing pages |

---

### Phase 2: Audience Performance

**Objective:** Determine which audience segments are driving the best results — and which are wasting budget.

**Demographic breakdown analysis:**

| Dimension | What to Analyse |
|---|---|
| **Job Function** | Which functions generate the most leads/conversions? (Engineering, Operations, IT, Finance, General Management) |
| **Seniority** | Which levels convert best? (Director, VP, C-Suite, Manager, Senior) |
| **Company Size** | Which company sizes are responding? (1-50, 51-200, 201-500, 501-1000, 1001-5000, 5001-10000, 10001+) |
| **Industry** | Which industries are highest-performing? (Utilities, Mining, Manufacturing, Government, Transport) |
| **Company Name** | (If available) Which specific companies are engaging? |
| **Location** | Geographic distribution of engagement |

**For each demographic dimension, calculate:**
- Impression share (% of total impressions)
- Click share (% of total clicks)
- Conversion share (% of total conversions)
- CPL by segment
- Conversion rate by segment
- Index: (segment conversion rate / overall conversion rate) * 100 — values >100 indicate above-average performance

**Matched Audience vs Prospecting comparison:**

If the account uses Matched Audiences (retargeting, contact lists, account lists), compare:

| Metric | Matched Audiences | Prospecting | Delta |
|---|---|---|---|
| CTR | | | |
| CPC | | | |
| Conversion Rate | | | |
| CPL | | | |

Matched Audiences typically outperform prospecting on conversion metrics. The key question is whether the CPL premium for prospecting is justified by pipeline volume.

**Audience saturation indicators:**
- Frequency: if average frequency exceeds 4-5x per member per month, the audience may be fatigued
- Audience size: if the audience is below 50,000 members, expect higher CPCs and potential delivery issues
- Impression growth: declining impressions with stable budget suggests audience exhaustion

---

### Phase 3: Creative & Content Analysis

**Objective:** Evaluate which ad formats, creative approaches, and messaging themes are performing best.

**Ad format performance comparison:**

| Format | Impressions | Clicks | CTR | Conversions | CPL | Notes |
|---|---|---|---|---|---|---|
| Single Image | | | | | | Typically highest CTR |
| Carousel | | | | | | Good for multi-point messaging |
| Video | | | | | | Strong for awareness; track view-through |
| Message Ads (InMail) | | | | | | Higher CPL but often higher intent |
| Text Ads | | | | | | Low cost, low volume |
| Document Ads | | | | | | Good for thought leadership |
| Conversation Ads | | | | | | Multiple CTA paths |

**Creative analysis (where ad-level data is available):**

- **Top-performing ads**: Rank by conversion rate and CPL. What themes or messages do the top 5 share?
- **Ad copy themes**: Identify recurring language, value propositions, or hooks in high-performing ads
- **Visual patterns**: Note any creative patterns (photography vs illustration, people vs abstract, dark vs light)
- **CTA effectiveness**: Which call-to-action buttons perform best? (Learn More, Download, Sign Up, Register)

**Lead Gen Form analysis (if applicable):**

| Metric | Value | Benchmark |
|---|---|---|
| Form open rate | | 3–5% of impressions |
| Form completion rate | | 10–15% of opens |
| Submissions | | |
| Cost per submission | | AUD $30–$80 |
| Drop-off fields | | Which fields cause abandonment? |

**Lead Gen Form vs Website Landing Page comparison:**

If both are in use, compare:
- Conversion rate (form completion vs landing page conversion)
- CPL
- Lead quality (if downstream data is available)
- Volume

Lead Gen Forms typically have higher conversion rates due to auto-populated LinkedIn profile fields, but landing pages may capture more intent signals and allow richer qualification.

**Creative fatigue indicators:**
- CTR decline over time for the same creative
- Frequency exceeding 3x for the same ad
- Engagement rate declining while impressions remain stable
- Recommended creative refresh cycle: every 4–6 weeks

---

### Phase 4: Conversion & Attribution

**Objective:** Assess the health and completeness of conversion tracking, and evaluate attribution data.

**Tracking health check:**

| Component | Status | Notes |
|---|---|---|
| **Insight Tag** | Installed / Not installed / Unknown | Required for website conversions and retargeting |
| **Insight Tag — pages firing** | All pages / Some pages / Unknown | Partial installation misses conversion events |
| **Conversions API (CAPI)** | Configured / Not configured / Unknown | Server-side tracking; more reliable than browser-only |
| **Conversion events defined** | List events | e.g., form submission, demo request, page visit |
| **Attribution window** | Current setting | LinkedIn default: 30-day click, 7-day view |
| **UTM parameters** | Consistent / Inconsistent / Missing | Required for GA4 cross-referencing |

**If Insight Tag is not installed or CAPI is not configured:**

> "Your conversion tracking has gaps. Without the Insight Tag, you cannot track website conversions or build retargeting audiences. Without CAPI, you are relying solely on browser-based tracking, which is increasingly unreliable due to ad blockers and cookie restrictions. I recommend addressing tracking as a priority before optimising campaigns — you cannot optimise what you cannot measure."

**Conversion type breakdown:**

| Conversion Type | Count | % of Total | Cost per Conversion |
|---|---|---|---|
| Lead Gen Form submissions | | | |
| Website form completions | | | |
| Content downloads | | | |
| Page visits (key pages) | | | |
| Other custom events | | | |

**Attribution analysis:**

- **View-through vs click-through conversions**: What proportion of conversions are view-through? LinkedIn's default 7-day view-through window can inflate conversion counts
- **LinkedIn-reported vs GA4-reported conversions**: If GA4 data is available, compare. Discrepancies are normal but gaps >30% warrant investigation
- **Attribution model impact**: Note that LinkedIn uses last-touch attribution within its own platform. Multi-touch attribution (via GA4 or a dedicated attribution tool) gives a more complete picture

**Common attribution discrepancies and causes:**

| Discrepancy | Likely Cause | Resolution |
|---|---|---|
| LinkedIn reports more conversions than GA4 | View-through conversions included in LinkedIn; UTMs missing or broken | Review attribution window; audit UTMs |
| GA4 reports more conversions than LinkedIn | Conversions happening outside attribution window; LinkedIn tag not firing on all pages | Extend attribution window; audit Insight Tag |
| CPL seems too low | View-through conversions inflating denominator | Filter to click-through conversions only for CPL calculation |

---

### Phase 5: B2B-Specific Insights

**Objective:** Assess LinkedIn Ads performance through a B2B lens — lead quality, account-based alignment, and funnel positioning.

**Account-Based Marketing (ABM) alignment:**

If account lists or company targeting is in use:
- Which target accounts are engaging? (Impressions, clicks, conversions by company)
- What is the engagement rate among target accounts vs general audience?
- Are decision-makers within target accounts seeing and engaging with ads?
- Recommendation: upload CRM account lists as Matched Audiences for ABM campaigns

**Lead quality assessment:**

Go beyond volume and CPL to assess the quality of leads generated:

| Quality Indicator | How to Assess |
|---|---|
| **Job title relevance** | Do leads match target personas? (e.g., Asset Manager, Reliability Engineer, CTO) |
| **Seniority match** | Are leads at the right decision-making level? |
| **Company fit** | Do leads come from target industries and company sizes? |
| **Form completion quality** | Are custom question responses substantive or low-effort? |
| **Downstream progression** | If CRM data is available: lead-to-MQL, MQL-to-SQL, SQL-to-opportunity rates |

**Lead quality scoring framework:**

| Score | Definition | Action |
|---|---|---|
| **A — High Quality** | Right title, right seniority, right company, substantive responses | Prioritise for sales follow-up |
| **B — Moderate Quality** | Partially matches ICP; may need nurturing | Add to nurture sequence |
| **C — Low Quality** | Wrong seniority, wrong industry, or minimal engagement | Review targeting; may indicate audience leakage |
| **D — Disqualified** | Competitor, student, job seeker, or spam | Exclude from targeting; add to suppression list |

**Funnel stage alignment:**

Map campaigns to funnel stages and assess whether the right content is reaching the right stage:

| Funnel Stage | Appropriate Objectives | Content Types | KPIs |
|---|---|---|---|
| **Awareness** | Brand awareness, video views | Thought leadership, industry insights, video | Reach, video views, engagement rate |
| **Consideration** | Website visits, engagement | Case studies, whitepapers, webinar promos | CTR, website visits, content downloads |
| **Conversion** | Lead generation | Demo requests, consultation offers, lead magnets | Leads, CPL, form completion rate |
| **Retention** | Website visits (retargeting) | Customer success stories, product updates | Engagement rate, repeat visits |

**Integration with MBP:b2b-research:**

If MBP:b2b-research has produced prospect dossiers or pipeline data:
- Cross-reference LinkedIn Ads engagement data with target account lists from b2b-research
- Identify target accounts that are engaging with ads but have not yet been contacted
- Flag high-value accounts showing ad engagement as warm outreach opportunities
- Recommend audience list updates based on new b2b-research prospect lists

---

### Phase 6: Strategic Recommendations

**Objective:** Translate analysis findings into prioritised, actionable recommendations.

Structure recommendations into these categories:

#### 6.1 Audience Refinement

Based on Phase 2 findings:
- **Expand**: Audience segments with strong CPL and conversion rate that could receive more budget
- **Contract**: Segments with high spend and low conversion that should be reduced or excluded
- **Test**: New audience combinations worth testing (e.g., lookalike audiences from high-quality leads)
- **Exclude**: Job titles, seniority levels, or industries that consistently produce low-quality leads

Refer to `references/audience-targeting-guide.md` for B2B targeting best practices specific to asset management.

#### 6.2 Content & Creative Strategy

Based on Phase 3 findings:
- Ad format recommendations (shift budget toward best-performing formats)
- Creative refresh schedule (flag any creatives running >6 weeks)
- Messaging themes to double down on vs retire
- Lead Gen Form optimisation (field reduction, pre-fill improvements, custom question refinement)
- A/B testing priorities for the next cycle

#### 6.3 Budget Optimisation

Based on Phase 1 and Phase 2 findings:
- Campaign-level budget reallocation recommendations
- Bid strategy adjustments (manual vs automated bidding)
- Dayparting or scheduling recommendations (if data supports it)
- Pacing issues: campaigns underspending (audience too narrow) or overspending (audience too broad)

#### 6.4 Conversion Tracking Improvements

Based on Phase 4 findings:
- Insight Tag installation or verification steps
- CAPI setup recommendations
- Attribution window adjustments
- UTM parameter standardisation (reference `shared/utm-taxonomy.md`)
- GA4 integration verification

#### 6.5 LinkedIn + Organic Synergy

Recommendations for aligning paid LinkedIn Ads with organic LinkedIn presence:
- Retarget users who engaged with organic posts (Company Page engagement audiences)
- Use top-performing ad copy themes as organic post topics (feed insights to MBP:linkedin-post)
- Amplify high-performing organic posts with paid boost (Sponsored Content from Page)
- Employee advocacy: encourage team members to share content that ads are promoting
- Align ad campaign themes with the content calendar managed by MBP:linkedin-post

---

## LinkedIn-Specific Context

Include this context when interpreting results and making recommendations. LinkedIn Ads operate differently from Google Ads and other social platforms.

### Cost Expectations

- **CPCs are higher than Google Ads** — AUD $5–$15 is typical for B2B targeting in Australia. This is not a problem; it reflects the precision of professional targeting
- **CPLs are higher than Facebook/Instagram** — but lead quality is typically significantly higher for B2B
- **The value is in targeting precision, not volume** — LinkedIn is the only platform where you can target by job title, seniority, company size, and industry simultaneously
- **Budget efficiency improves with audience refinement** — broad audiences waste spend on irrelevant professionals

### B2B Consideration Cycles

- **Longer sales cycles** — B2B asset management deals often take 3–12 months from first touch to close
- **Multiple stakeholders** — decisions involve technical evaluators, financial approvers, and end users
- **Attribution is harder** — the person who clicks the ad may not be the person who signs the contract
- **Retargeting is essential** — LinkedIn's Matched Audiences allow you to stay visible throughout the consideration period

### Lead Quality Over Volume

- **Fewer, better leads** — 10 leads from the right decision-makers outperform 100 leads from the wrong ones
- **Lead Gen Forms vs website forms** — LinkedIn Lead Gen Forms have higher completion rates but may capture lower-intent leads (less friction = less qualification)
- **Custom questions are critical** — adding a qualifying question to Lead Gen Forms (e.g., "What is your biggest asset management challenge?") helps filter quality

### Platform-Specific Quirks

- **Audience size minimum**: 300 members for targeting (1,000+ recommended for meaningful delivery)
- **Frequency caps**: LinkedIn does not offer manual frequency caps; monitor frequency and rotate creative to manage fatigue
- **Conversion tracking lag**: LinkedIn conversion data can take up to 48 hours to appear
- **Demographic data is modelled**: LinkedIn's demographic reporting is based on member profile data, which may be incomplete or outdated
- **Campaign budget optimisation (CBO)**: LinkedIn's CBO distributes budget across ad sets automatically; useful for testing but reduces manual control

---

## Output

### Primary Output: Markdown Report

Generate a structured Markdown report following the template in `references/linkedin-ads-report-template.md`. The report must include all six analysis phases with findings, data tables, and recommendations.

### Secondary Output: Normalised Metrics JSON

Write normalised metrics to `.marketing/linkedin-ads/latest.json` using the schema defined in `shared/normalised-metrics-schema.json`.

**Example output:**

```json
{
  "platform": "linkedin-ads",
  "period": {
    "start": "2026-02-01",
    "end": "2026-02-28"
  },
  "currency": "AUD",
  "metrics": {
    "spend": 4250.00,
    "impressions": 85000,
    "clicks": 1275,
    "ctr": 0.015,
    "cpc": 3.33,
    "conversions": 42,
    "conversion_rate": 0.033,
    "cost_per_conversion": 101.19,
    "conversion_value": 0,
    "roas": 0,
    "engagement_rate": 0.018
  },
  "campaigns": [
    {
      "name": "linkedin-leadgen-utilities-202602",
      "status": "active",
      "objective": "lead_generation",
      "spend": 2800.00,
      "impressions": 56000,
      "clicks": 840,
      "conversions": 28,
      "cpa": 100.00
    },
    {
      "name": "linkedin-brand-assetmgmt-202602",
      "status": "active",
      "objective": "brand_awareness",
      "spend": 1450.00,
      "impressions": 29000,
      "clicks": 435,
      "conversions": 14,
      "cpa": 103.57
    }
  ],
  "top_performers": [
    {
      "name": "linkedin-leadgen-utilities-202602",
      "type": "campaign",
      "metric_value": 0.033,
      "metric_name": "conversion_rate"
    }
  ],
  "issues": [
    {
      "severity": "high",
      "description": "Conversions API (CAPI) not configured — relying on browser-only tracking",
      "recommendation": "Implement CAPI for server-side conversion tracking to improve data accuracy"
    },
    {
      "severity": "medium",
      "description": "UTM parameters inconsistent across campaigns",
      "recommendation": "Standardise UTMs per shared/utm-taxonomy.md for accurate cross-channel attribution"
    }
  ],
  "generated_at": "2026-03-02T10:00:00+11:00"
}
```

### Output File Location

```
.marketing/
  linkedin-ads/
    latest.json              # Normalised metrics (schema: shared/normalised-metrics-schema.json)
    report-YYYY-MM-DD.md     # Full analysis report
```

---

## Integration with Other MBP Skills

| Skill | Integration |
|---|---|
| **MBP:marketing-dashboard** | Consumes `latest.json` for cross-channel reporting. LinkedIn Ads data appears alongside Google Ads, website analytics, and SEO metrics |
| **MBP:linkedin-post** | Feed top-performing ad themes to organic content strategy. Recommend boosting high-performing organic posts. Align paid and organic calendars |
| **MBP:b2b-research** | Cross-reference target account engagement. Update audience lists from prospect research. Identify warm outreach candidates showing ad engagement |
| **MBP:website-analytics** | Validate LinkedIn-reported conversions against GA4 data. Assess post-click behaviour of LinkedIn Ads traffic |
| **MBP:content-intel** | Inform content strategy based on which topics drive best ad engagement. Recommend content formats based on ad format performance |
| **shared/utm-taxonomy.md** | All LinkedIn Ads campaigns must use standardised UTM parameters for cross-channel attribution |
| **shared/normalised-metrics-schema.json** | Output JSON conforms to this schema for dashboard consumption |

---

## Content Guidelines

### Australian English

Use Australian English spelling throughout:
- analyse (not analyze)
- optimise (not optimize)
- organisation (not organization)
- colour (not color)
- programme (for initiatives; program for software)
- licence (noun) / license (verb)
- centre (not center)
- behaviour (not behavior)
- prioritise (not prioritize)
- recognised (not recognized)

### Tone

- **Professional and evidence-based** — every finding must be supported by data
- **Actionable** — recommendations must be specific and practical, not generic "consider improving"
- **Proportionate** — focus attention on the levers that will have the most impact
- **Honest** — if the data is insufficient for a reliable conclusion, say so
- **No vendor hype** — do not overstate LinkedIn's effectiveness. Acknowledge limitations and trade-offs

### Numbers and Currency

- All monetary values in AUD unless explicitly stated otherwise
- Use two decimal places for currency (AUD $4,250.00)
- Use percentage with one decimal place (CTR: 1.5%)
- Use commas for thousands separators (85,000 impressions)

---

## Workflow Summary

### Step 1: Data Source Detection

Check for LinkedIn Ads MCP server. If unavailable, request CSV exports from Campaign Manager. Confirm which data sources are available before proceeding.

### Step 2: Discovery Interview

Conduct the discovery interview to understand account context, objectives, budget, lead quality definition, tracking setup, and goals for the analysis.

### Step 3: Phase 1 — Account Overview

Analyse aggregate and campaign-level performance metrics. Establish baselines and flag significant period-over-period changes.

### Step 4: Phase 2 — Audience Performance

Break down performance by demographic dimensions. Identify top-performing and underperforming segments. Compare Matched Audiences vs prospecting.

### Step 5: Phase 3 — Creative & Content Analysis

Evaluate ad format performance, creative themes, Lead Gen Form effectiveness, and creative fatigue indicators.

### Step 6: Phase 4 — Conversion & Attribution

Audit tracking health (Insight Tag, CAPI, UTMs). Analyse conversion types, attribution models, and cross-platform discrepancies.

### Step 7: Phase 5 — B2B-Specific Insights

Assess ABM alignment, lead quality, funnel stage mapping, and integration with MBP:b2b-research prospect data.

### Step 8: Phase 6 — Strategic Recommendations

Compile prioritised recommendations across audience, creative, budget, tracking, and organic synergy.

### Step 9: Report & Output

Generate the Markdown report using `references/linkedin-ads-report-template.md`. Write normalised metrics JSON to `.marketing/linkedin-ads/latest.json`. Present key findings and top recommendations to the user.

---

## Checklist

Before delivering the report, verify:

- [ ] Data source confirmed (MCP or CSV exports)
- [ ] Discovery interview completed (or assumptions clearly documented)
- [ ] Phase 1: Account overview metrics compiled with period-over-period comparison
- [ ] Phase 2: Demographic breakdown analysed with segment-level CPL and conversion rates
- [ ] Phase 3: Ad format and creative performance compared; Lead Gen Form metrics included
- [ ] Phase 4: Tracking health assessed (Insight Tag, CAPI, UTMs, attribution)
- [ ] Phase 5: B2B-specific insights included (lead quality, ABM, funnel alignment)
- [ ] Phase 6: Recommendations are prioritised, specific, and actionable
- [ ] Normalised metrics JSON written to `.marketing/linkedin-ads/latest.json`
- [ ] JSON conforms to `shared/normalised-metrics-schema.json`
- [ ] UTM conventions align with `shared/utm-taxonomy.md`
- [ ] All monetary values reported in AUD
- [ ] Australian English spelling used throughout
- [ ] Benchmarks provided for context on key metrics
- [ ] Report follows `references/linkedin-ads-report-template.md` structure
