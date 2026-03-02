---
name: MBP:website-analytics
description: Analyse website performance using GA4 data. Use when the user wants to review website traffic, assess content performance, track conversion paths, measure marketing channel effectiveness, or understand user behaviour. Supports live data via GA4 MCP and CSV/export upload as fallback. Part of the Marcov Beam Pipeline — serves as the attribution truth layer connecting ads to business outcomes.
---

# Website Analytics Skill

Analyse website performance and user behaviour using Google Analytics 4 (GA4) data. This skill serves as the **attribution truth layer** in the Marcov Beam Pipeline — all paid channels (Google Ads, LinkedIn Ads) and organic channels drive traffic to the website, and GA4 is where attribution happens. Without reliable website analytics, every other marketing skill is flying blind.

## Core Philosophy: Attribution Truth Layer

Website analytics sits at the centre of the MBP marketing stack. Every dollar spent on Google Ads, every LinkedIn campaign, every SEO improvement, and every piece of content ultimately drives users to the website. GA4 is where you answer the question: **"Did it work?"**

This skill connects upstream channel spend (MBP:google-ads, MBP:linkedin-ads) to downstream business outcomes (leads, conversions, pipeline). It provides the attribution data that MBP:marketing-dashboard needs to calculate true cost-per-acquisition and return on ad spend across all channels.

### What This Skill Answers

- **Which channels actually drive conversions?** — Not just traffic, but qualified actions
- **Which content converts vs which content only attracts?** — Page views are vanity; conversions are sanity
- **Where do users drop off?** — Funnel leakage identification
- **Is paid traffic quality improving or declining?** — Session quality by source
- **What is the true multi-touch attribution path?** — First touch vs last touch vs assisted

---

## Overview

This skill helps you:

- **Assess traffic health** — sessions, users, new vs returning, device and geographic breakdown
- **Attribute acquisition sources** — organic search, paid search (Google Ads), paid social (LinkedIn Ads), direct, referral, email
- **Evaluate content performance** — top pages by engagement, conversion, and traffic; blog vs service pages
- **Analyse conversion funnels** — visit-to-engage-to-convert paths, drop-off points, conversion rate by source
- **Understand user behaviour** — engagement rate trends, pages per session, exit pages, returning user patterns
- **Generate actionable recommendations** — SEO opportunities, CRO improvements, content strategy, channel optimisation

---

## Input

This skill accepts a **website analytics review request** as its primary input. It can work from live GA4 data (via MCP), exported CSVs from the GA4 UI, or Looker Studio exports.

### Invocation Examples

```
/website-analytics Review last month's website performance
/website-analytics How is our Google Ads traffic converting?
/website-analytics Which blog posts drive the most conversions?
/website-analytics Full website analytics review for February 2026
/website-analytics Compare organic vs paid traffic quality
/website-analytics Analyse conversion paths from LinkedIn campaigns
```

---

## Data Source Detection (CRITICAL)

Before beginning any analysis, detect available data sources in this priority order:

### Priority 1: GA4 MCP (Live Data)

Check whether a GA4 MCP server is available. If it is:
- Use the GA4 Data API via MCP for live queries
- Confirm the GA4 property ID with the user
- Verify date ranges and available dimensions/metrics
- Refer to `references/ga4-query-library.md` for common query patterns

### Priority 2: GA4 UI Exports / Looker Studio Exports

If no MCP is available, ask the user to provide data:
- **GA4 UI exports** — CSV or Excel files exported from GA4 reports (Acquisition, Engagement, Monetisation, Retention)
- **Looker Studio exports** — CSV exports from custom Looker Studio dashboards
- **Google Sheets** — shared analytics dashboards

### Priority 3: Manual Data Entry

As a last resort, the user can provide key metrics manually. In this case, focus the analysis on what is available and clearly note the limitations.

### Data Source Confirmation

Always confirm with the user:

> "I'll need access to your GA4 data. Do you have a GA4 MCP server connected, or would you prefer to upload CSV exports from the GA4 UI? If uploading, I'll need at minimum: traffic acquisition report, engagement report, and conversions report for the period you want to analyse."

---

## Discovery Process (CRITICAL)

**Before analysing any data, you MUST conduct a discovery interview to understand the website, its goals, and the marketing context.**

### Questions to Ask

1. **Website & Property**
   - What is the website URL?
   - What is the GA4 property ID? (format: `123456789`)
   - Are there multiple properties or data streams? (e.g., separate blog subdomain)
   - What is the reporting time zone?

2. **Conversion Actions**
   - What are the key conversion actions? (contact form submission, demo request, whitepaper download, newsletter signup, phone call click, chat initiation)
   - Are these configured as GA4 conversion events?
   - What event names are used? (e.g., `generate_lead`, `form_submit`, `file_download`)
   - Is there a primary conversion vs secondary conversions?

3. **Channel Tagging & Attribution**
   - Are Google Ads linked to GA4? (auto-tagging via `gclid`)
   - Are LinkedIn Ads tagged with UTM parameters? (see `shared/utm-taxonomy.md`)
   - Are email campaigns tagged with UTMs?
   - Are there any other paid channels running?
   - What attribution model is configured in GA4? (data-driven, last click, etc.)

4. **Content Structure**
   - What are the main content pillars on the website? (e.g., asset management, data quality, AI readiness)
   - Is there a blog or resource section? What URL pattern? (e.g., `/blog/`, `/resources/`, `/insights/`)
   - Are there gated content assets? (whitepapers, guides behind forms)
   - Are events or webinars promoted on the website?

5. **Business Context**
   - What is the primary business goal? (lead generation, thought leadership, service awareness, event registrations)
   - What is the target audience? (industry, role, geography)
   - What does a "good month" look like? (target sessions, target leads, target conversion rate)
   - What period should this analysis cover?

6. **Known Issues**
   - Any recent website changes? (redesign, new pages, changed URLs)
   - Any tracking issues you are aware of? (consent banner blocking, missing events)
   - Have there been changes to GA4 configuration recently?

### If the User Provides Data Without Context

If the user uploads a CSV or provides raw data without answering discovery questions, proceed with what can be determined from the data itself. Clearly note assumptions and flag where missing context limits the analysis.

---

## Analysis Workflow

### Phase 1: Traffic Overview

Establish the baseline picture of website performance for the analysis period.

**Metrics to extract:**

| Metric | Description |
|---|---|
| Total sessions | All sessions in the period |
| Total users | Unique users (based on GA4 user model) |
| New users | First-time visitors |
| Returning users | Users with prior sessions |
| New vs returning ratio | Percentage split |
| Sessions per user | Average session frequency |
| Average engagement time | Time actively engaged per session |
| Engagement rate | Percentage of engaged sessions (GA4 definition: lasted > 10s, had conversion event, or had 2+ page views) |
| Pages per session | Average page depth |
| Device breakdown | Desktop vs mobile vs tablet (sessions and conversion rate per device) |
| Geographic breakdown | Top countries and cities by sessions |

**Period comparisons:**
- Compare to previous period (e.g., this month vs last month)
- Compare to same period last year (if data available)
- Flag significant changes (>15% movement) with directional indicators

**Key questions to answer:**
- Is overall traffic growing, stable, or declining?
- What is the new-to-returning user ratio? (healthy B2B is typically 60-70% new)
- Is engagement rate improving? (benchmark: >55% is good for B2B)
- Are mobile users being underserved? (compare mobile vs desktop engagement rate)

---

### Phase 2: Acquisition Source Analysis

Break down traffic by how users arrive at the website. This is where attribution to paid channels happens.

**Source/medium breakdown:**

| Source / Medium | Sessions | Users | New Users | Engagement Rate | Conversions | Conv. Rate |
|---|---|---|---|---|---|---|
| google / organic | | | | | | |
| google / cpc | | | | | | |
| linkedin / paid_social | | | | | | |
| (direct) / (none) | | | | | | |
| referral sites | | | | | | |
| email / newsletter | | | | | | |

**GA4 Default Channel Groupings:**
- **Organic Search** — unpaid search engine traffic (primarily Google, also Bing)
- **Paid Search** — Google Ads search campaigns (identified by `gclid` auto-tagging or `utm_medium=cpc`)
- **Paid Social** — LinkedIn Ads and other paid social (identified by UTM parameters: `utm_source=linkedin`, `utm_medium=paid_social`)
- **Organic Social** — unpaid LinkedIn posts, Reddit, other social
- **Direct** — no referrer, bookmarks, typed URLs
- **Referral** — inbound links from other websites
- **Email** — tagged email campaign links (`utm_medium=email`)
- **Display** — Google Display Network campaigns

**Critical attribution checks:**
1. **Google Ads traffic** — Verify that `google / cpc` traffic aligns with Google Ads click data from MBP:google-ads. Significant discrepancies indicate tracking issues.
2. **LinkedIn Ads traffic** — Verify that `linkedin / paid_social` traffic exists. If LinkedIn Ads are running (per MBP:linkedin-ads) but no tagged traffic appears, UTM tagging is broken. Flag this as critical.
3. **Direct traffic proportion** — If direct traffic is >30%, investigate whether UTM parameters are being stripped or missing. High direct traffic often masks untagged campaign traffic.
4. **UTM consistency** — Check that UTM values follow the conventions in `shared/utm-taxonomy.md`. Flag non-standard values.

**Key questions to answer:**
- Which channel drives the most sessions? The most conversions?
- What is the conversion rate by channel? (paid should convert higher than organic if targeting is right)
- Is there a channel with high traffic but low conversion rate? (quality problem)
- Is there a channel with low traffic but high conversion rate? (scaling opportunity)

---

### Phase 3: Content Performance

Analyse which pages and content types drive engagement and conversions.

**Top pages analysis:**

| Page | Sessions | Avg. Engagement Time | Engagement Rate | Conversions | Conv. Rate |
|---|---|---|---|---|---|
| / (homepage) | | | | | |
| /services/* | | | | | |
| /blog/* | | | | | |
| /contact | | | | | |
| /resources/* | | | | | |

**Content categorisation:**
- **Service pages** — core offering pages (what the business does)
- **Blog/insight content** — thought leadership, educational content
- **Landing pages** — campaign-specific pages for paid traffic
- **Resource/gated content** — whitepapers, guides, downloadable assets
- **Conversion pages** — contact, demo request, quote request forms

**Content performance dimensions:**
1. **Traffic drivers** — pages that attract the most sessions (awareness value)
2. **Engagement drivers** — pages with highest engagement time and rate (consideration value)
3. **Conversion drivers** — pages that generate the most conversions (revenue value)
4. **Content that converts vs content that only drives traffic** — critical distinction. A blog post with 5,000 sessions and 0 conversions is performing differently from a service page with 200 sessions and 15 conversions.

**Blog/resource section deep-dive (if applicable):**
- Top blog posts by sessions, engagement, and conversions
- Content pillar performance — which topics perform best?
- Content recency — are newer posts outperforming older ones? (freshness signal)
- Blog-to-conversion path — do blog readers navigate to service/contact pages?

**Key questions to answer:**
- Which content pillars drive the most qualified traffic?
- Is blog content contributing to conversions, or only to vanity metrics?
- Which landing pages have the highest conversion rate? The lowest?
- Are there high-traffic pages with poor engagement? (content quality issue)

---

### Phase 4: Conversion Analysis

Deep-dive into the conversion funnel and attribution paths.

**Conversion funnel:**

```
Visit (Sessions)
  └──▶ Engage (Engaged Sessions)
         └──▶ Convert (Conversion Events)
```

| Funnel Stage | Count | Rate | Drop-off |
|---|---|---|---|
| Sessions | {{SESSIONS}} | 100% | — |
| Engaged sessions | {{ENGAGED}} | {{ENG_RATE}} | {{DROP_1}} |
| Conversions | {{CONVERSIONS}} | {{CONV_RATE}} | {{DROP_2}} |

**Conversion rate by source:**

| Source | Sessions | Conversions | Conv. Rate | vs Site Average |
|---|---|---|---|---|
| google / organic | | | | |
| google / cpc | | | | |
| linkedin / paid_social | | | | |
| (direct) / (none) | | | | |
| referral | | | | |

**Landing page conversion performance:**
- Which landing pages have the highest entry-to-conversion rate?
- Which landing pages have high traffic but zero conversions? (wasted opportunity)
- Are paid campaign landing pages outperforming organic entry pages?

**Multi-touch attribution (if data available):**
- First-touch attribution — which channels introduce users?
- Last-touch attribution — which channels close conversions?
- Assisted conversions — which channels appear in the path but are not the last touch?
- Typical conversion path length (number of sessions before converting)
- Average time to conversion (days from first visit to conversion)

**Key questions to answer:**
- What is the overall site conversion rate? Is it improving?
- Which source delivers the best conversion rate? The worst?
- How many touchpoints does a typical conversion require?
- Are there sources that frequently assist but rarely get last-touch credit?

---

### Phase 5: User Behaviour

Understand how users interact with the website and where they disengage.

**Engagement trends:**
- Engagement rate over time (weekly or monthly trend line)
- Pages per session trend — are users exploring more or less over time?
- Average engagement time trend — are sessions getting deeper?

**Behaviour by source:**
- Pages per session by source/medium — do paid users explore less than organic?
- Engagement rate by source — quality signal per channel
- Return visit rate by source — which channels bring users back?

**New vs returning user behaviour:**

| Behaviour Metric | New Users | Returning Users | Delta |
|---|---|---|---|
| Sessions | | | |
| Engagement rate | | | |
| Pages per session | | | |
| Avg. engagement time | | | |
| Conversion rate | | | |

**Exit page analysis:**
- Top exit pages — where do users leave the site?
- Exit rate by section — are users leaving from service pages (bad) or confirmation pages (expected)?
- High-engagement pages with high exit rate — potential CRO opportunities

**Key questions to answer:**
- Are returning users significantly more likely to convert? (nurture value)
- Which channels bring back returning users? (brand building effectiveness)
- Are there pages where users consistently disengage? (UX or content problem)
- Is mobile user behaviour significantly different from desktop? (responsive experience quality)

---

### Phase 6: Recommendations

Synthesise findings into actionable recommendations across five categories.

#### 1. SEO Opportunities
- Pages ranking on page 2 that could move to page 1 with optimisation
- High-traffic blog content that could be updated for freshness
- Content gaps identified from search query data (if available via Search Console integration)
- Internal linking opportunities to boost key conversion pages

#### 2. Conversion Rate Optimisation (CRO)
- Landing pages with high traffic but low conversion rate — form placement, CTA clarity, social proof
- Funnel drop-off points — where are users abandoning the conversion path?
- Mobile conversion rate vs desktop — if significantly lower, mobile UX needs attention
- Exit pages that should not be exit pages — content or navigation improvements

#### 3. Content Strategy
- Content pillars that drive conversions vs those that only drive traffic
- Blog topics to double down on (high engagement + conversion contribution)
- Content types to deprioritise (high effort, low performance)
- New content opportunities based on user behaviour patterns

#### 4. Channel Optimisation
- Channels with high conversion rate that deserve more budget
- Channels with declining quality — review targeting and messaging
- UTM tagging gaps — channels where attribution is unclear
- Cross-channel synergies — e.g., organic search users who later convert via direct

#### 5. Tracking Improvements
- Missing or misconfigured conversion events
- UTM parameter inconsistencies (reference `shared/utm-taxonomy.md`)
- High direct traffic suggesting untagged campaigns
- Consent banner impact on data collection
- Recommended GA4 configuration changes

---

## GA4-Specific Notes

### Sessions vs Users

GA4 distinguishes between sessions and users:
- A **session** starts when a user opens the site and ends after 30 minutes of inactivity or at midnight
- A **user** can have multiple sessions across multiple days/devices
- Always report both metrics — sessions for volume, users for reach
- **Sessions per user** indicates return visit frequency (higher is generally better for B2B)

### Engagement Rate (Replaces Bounce Rate)

GA4 replaced the Universal Analytics bounce rate with **engagement rate**:
- An **engaged session** lasted longer than 10 seconds, had a conversion event, or had 2+ page/screen views
- Engagement rate = engaged sessions / total sessions
- This is the inverse of bounce rate but measured differently — do not compare directly to UA bounce rate
- B2B benchmark: 55-70% engagement rate is healthy

### Default Channel Groupings

GA4 assigns traffic to default channel groups based on source, medium, and campaign parameters:

| Channel Group | Source/Medium Pattern |
|---|---|
| Organic Search | Source matches a search engine AND medium = `organic` |
| Paid Search | Medium matches `cpc`, `ppc`, or `paid search`; OR source is a search engine with gclid |
| Paid Social | Medium matches `paid_social`, `paidsocial`, or `paid social`; AND source matches a social network |
| Organic Social | Source matches a social network AND medium = `organic` or similar |
| Direct | Source = `(direct)` AND medium = `(none)` |
| Referral | Medium = `referral` |
| Email | Medium = `email` |
| Display | Medium = `display`, `banner`, or `cpm` |

### UTM Parameters for Attribution

UTM parameters are the primary mechanism for attributing traffic from channels that do not have automatic integration with GA4:

- **Google Ads** — uses auto-tagging (`gclid` parameter) by default. UTMs are optional but recommended as backup.
- **LinkedIn Ads** — requires manual UTM tagging. Without UTMs, LinkedIn traffic appears as `linkedin.com / referral` and is indistinguishable from organic LinkedIn traffic. Follow `shared/utm-taxonomy.md` conventions.
- **Email campaigns** — require UTM tagging for proper attribution
- **Partner/referral links** — should use UTMs to distinguish from general referral traffic

### Auto-Tagging (gclid) for Google Ads

When Google Ads auto-tagging is enabled:
- GA4 automatically attributes traffic to the correct Google Ads campaign, ad group, and keyword
- This provides richer data than UTM parameters alone (includes cost data, search terms, quality score context)
- Auto-tagging and manual UTM tagging can coexist — GA4 uses auto-tagging when both are present
- If auto-tagging is disabled, Google Ads traffic may appear as `google / organic` — this is a critical tracking failure

---

## Output

### Markdown Report

Generate a comprehensive markdown report following the template in `references/website-report-template.md`. The report should be standalone and readable without access to the raw data.

### Normalised Metrics JSON

Write normalised metrics to `.marketing/website/latest.json` following the schema in `shared/normalised-metrics-schema.json`.

**Website-specific fields in the normalised output:**

```json
{
  "platform": "website",
  "period": {
    "start": "2026-02-01",
    "end": "2026-02-28"
  },
  "currency": "AUD",
  "metrics": {
    "sessions": 4250,
    "clicks": 4250,
    "engagement_rate": 0.62,
    "conversions": 85,
    "conversion_rate": 0.02
  },
  "campaigns": [
    {
      "name": "google / organic",
      "status": "active",
      "objective": "organic_acquisition",
      "impressions": null,
      "clicks": 1800,
      "conversions": 35,
      "cpa": null
    },
    {
      "name": "google / cpc",
      "status": "active",
      "objective": "paid_acquisition",
      "clicks": 950,
      "conversions": 25,
      "cpa": null
    }
  ],
  "top_performers": [
    {
      "name": "/blog/iso-55001-readiness-checklist",
      "type": "page",
      "metric_value": 0.045,
      "metric_name": "conversion_rate"
    }
  ],
  "issues": [
    {
      "severity": "high",
      "description": "LinkedIn Ads traffic appearing as referral — UTM tagging not applied",
      "recommendation": "Apply UTM parameters to all LinkedIn Ads campaigns per shared/utm-taxonomy.md"
    }
  ],
  "generated_at": "2026-02-28T14:30:00+11:00"
}
```

Also write a snapshot to `.marketing/website/history/{YYYY-MM-DD}.json` for trend tracking. History files are immutable — never overwrite a previous snapshot.

---

## Integration with MBP Skills

### Feeds Into

| Skill | What It Receives | Purpose |
|---|---|---|
| MBP:marketing-dashboard | `.marketing/website/latest.json` | Attribution truth layer — connects ad spend to business outcomes |
| MBP:marketing-dashboard | Conversion data by source | Calculates true cross-channel CPA and ROAS |

### Receives From

| Skill | What It Provides | Purpose |
|---|---|---|
| MBP:google-ads | Campaign spend and click data | Cross-reference with GA4 session/conversion data for Google Ads attribution |
| MBP:linkedin-ads | Campaign spend and click data | Cross-reference with GA4 UTM-tagged traffic for LinkedIn attribution |
| MBP:seo | SEO health and keyword data | Context for organic search traffic analysis |
| MBP:content-intel | Content pillar taxonomy | Framework for categorising content performance |

### Shared References

- `shared/utm-taxonomy.md` — UTM parameter conventions for cross-channel attribution
- `shared/normalised-metrics-schema.json` — Output schema for `.marketing/website/latest.json`

---

## Guardrails

1. **Never fabricate data** — if a metric is unavailable, say so. Do not estimate sessions, users, or conversion rates without explicit data.
2. **Always state the data source** — "Based on GA4 data for 1-28 Feb 2026" or "Based on exported CSV from GA4 UI". Never leave the data provenance ambiguous.
3. **Flag tracking gaps** — if direct traffic is suspiciously high, if LinkedIn traffic is untagged, if conversion events appear misconfigured — call it out. Tracking integrity is more valuable than a polished report.
4. **Compare fairly** — when comparing channels, account for volume differences. A channel with 50 sessions and 5 conversions (10% rate) is not necessarily better than one with 2,000 sessions and 80 conversions (4% rate).
5. **Australian English throughout** — analyse, behaviour, organisation, optimisation, colour, centre, programme (unless referring to software).
6. **Recommend, do not implement** — this skill analyses and recommends. It does not make changes to GA4 configuration, website content, or campaign settings.
7. **Privacy-conscious** — never expose individual user data, IP addresses, or personally identifiable information in reports. Work only with aggregate metrics.
8. **Acknowledge GA4 limitations** — consent banners reduce data completeness, thresholding may hide low-volume segments, data-driven attribution is a model not ground truth. Be transparent about these constraints.
