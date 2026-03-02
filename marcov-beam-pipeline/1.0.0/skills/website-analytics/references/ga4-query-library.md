# GA4 Data API Query Library

Pre-built Google Analytics 4 (GA4) Data API v1 query patterns for use with the GA4 MCP server. These queries cover the most common analysis tasks in MBP:website-analytics, organised by the analysis phases defined in the skill.

## Important Notes

- **API endpoint**: All queries use the GA4 Data API v1 `RunReport` method (`POST https://analyticsdata.googleapis.com/v1beta/properties/{propertyId}:runReport`)
- **Property ID**: Replace `{{GA4_PROPERTY_ID}}` with the numeric GA4 property ID (e.g., `123456789`)
- **Date ranges**: Use `startDate` and `endDate` in `YYYY-MM-DD` format, or relative values like `today`, `yesterday`, `7daysAgo`, `30daysAgo`
- **Metric values**: Rates (engagement rate, conversion rate) are returned as decimals (0.62 = 62%). Counts are integers.
- **Dimension scopes**: GA4 dimensions have scopes (event, session, user). Mixing scopes in a single query can produce unexpected results. Session-scoped dimensions (e.g., `sessionSource`) are preferred for acquisition analysis.
- **Row limits**: The API returns a maximum of 10,000 rows by default. Use `limit` and `offset` for pagination if needed.
- **Thresholding**: GA4 may apply data thresholding to protect user privacy, particularly for small segments. If rows are missing, this is the likely cause.
- **MCP tool mapping**: Where a GA4 MCP server is available, these request bodies can be passed directly to the `runReport` tool. Confirm the exact tool name with the connected MCP server (see the MCP Tool Mapping section at the end of this document).
- **Quota**: The GA4 Data API has quota limits per property. Avoid running unnecessary queries; batch analysis where possible.

---

## 1. Traffic Overview

High-level website performance metrics for the analysis period. Use this as the starting point for every website review.

**Use in:** Phase 1 -- Traffic Overview

```json
{
  "dateRanges": [
    {
      "startDate": "2026-02-01",
      "endDate": "2026-02-28",
      "name": "current_period"
    },
    {
      "startDate": "2026-01-01",
      "endDate": "2026-01-31",
      "name": "previous_period"
    }
  ],
  "metrics": [
    { "name": "sessions" },
    { "name": "totalUsers" },
    { "name": "newUsers" },
    { "name": "engagementRate" },
    { "name": "engagedSessions" },
    { "name": "screenPageViewsPerSession" },
    { "name": "averageSessionDuration" },
    { "name": "userEngagementDuration" },
    { "name": "conversions" }
  ]
}
```

**GA4 UI equivalent:** Reports > Life cycle > Acquisition > Overview

**Notes:**
- Including two date ranges in a single request returns both periods side by side, enabling period-over-period comparison without separate queries
- `engagementRate` is the proportion of engaged sessions (lasted >10s, had a conversion event, or had 2+ page views)
- `screenPageViewsPerSession` replaces the Universal Analytics "pages per session" metric
- `userEngagementDuration` is the total active time users spent on the site (in seconds)
- `averageSessionDuration` includes idle time; `userEngagementDuration` per session is more meaningful for B2B analysis
- No dimensions are specified -- this returns a single aggregated row per date range
- **Scope:** Requires read access to the GA4 property. No special scopes beyond standard reporting.

---

## 2. Acquisition Source/Medium

Traffic breakdown by session source and medium, with engagement and conversion metrics. This is the primary attribution query.

**Use in:** Phase 2 -- Acquisition Source Analysis

```json
{
  "dateRanges": [
    {
      "startDate": "2026-02-01",
      "endDate": "2026-02-28"
    }
  ],
  "dimensions": [
    { "name": "sessionSource" },
    { "name": "sessionMedium" }
  ],
  "metrics": [
    { "name": "sessions" },
    { "name": "totalUsers" },
    { "name": "newUsers" },
    { "name": "engagementRate" },
    { "name": "engagedSessions" },
    { "name": "averageSessionDuration" },
    { "name": "conversions" },
    { "name": "sessionConversionRate" }
  ],
  "orderBys": [
    {
      "metric": { "metricName": "sessions" },
      "desc": true
    }
  ],
  "limit": 50
}
```

**GA4 UI equivalent:** Reports > Acquisition > Traffic acquisition (primary dimension: Session source / medium)

**Notes:**
- `sessionSource` and `sessionMedium` are session-scoped dimensions -- they attribute the source/medium to the session that brought the user
- Common source/medium combinations to look for:
  - `google / organic` -- organic search traffic
  - `google / cpc` -- Google Ads paid search (auto-tagged via `gclid`)
  - `linkedin / paid_social` -- LinkedIn Ads (UTM-tagged per `shared/utm-taxonomy.md`)
  - `(direct) / (none)` -- direct traffic (no referrer detected)
  - `linkedin.com / referral` -- untagged LinkedIn traffic (potential UTM issue)
- If `linkedin.com / referral` appears with significant volume while LinkedIn Ads are running, flag this as a UTM tagging failure -- see `shared/utm-taxonomy.md`
- Cross-reference `google / cpc` sessions with Google Ads click data from MBP:google-ads to verify tracking integrity
- **Scope:** Standard GA4 reporting access

---

## 3. Channel Grouping

Performance by GA4 default channel group. Provides a higher-level view than source/medium, useful for executive summaries.

**Use in:** Phase 2 -- Acquisition Source Analysis (channel-level summary)

```json
{
  "dateRanges": [
    {
      "startDate": "2026-02-01",
      "endDate": "2026-02-28",
      "name": "current_period"
    },
    {
      "startDate": "2026-01-01",
      "endDate": "2026-01-31",
      "name": "previous_period"
    }
  ],
  "dimensions": [
    { "name": "sessionDefaultChannelGroup" }
  ],
  "metrics": [
    { "name": "sessions" },
    { "name": "totalUsers" },
    { "name": "newUsers" },
    { "name": "engagementRate" },
    { "name": "conversions" },
    { "name": "sessionConversionRate" }
  ],
  "orderBys": [
    {
      "metric": { "metricName": "sessions" },
      "desc": true
    }
  ]
}
```

**GA4 UI equivalent:** Reports > Acquisition > Traffic acquisition (primary dimension: Session default channel group)

**Notes:**
- `sessionDefaultChannelGroup` returns GA4's built-in channel groupings: Organic Search, Paid Search, Paid Social, Organic Social, Direct, Referral, Email, Display, etc.
- GA4 assigns channels based on source, medium, and campaign parameters -- see the SKILL.md channel grouping table for the full mapping
- Including two date ranges enables period-over-period comparison at the channel level
- If "Unassigned" appears as a channel with significant volume, investigate UTM parameter configuration
- Direct traffic exceeding 30% of total sessions warrants investigation -- it often masks untagged campaign traffic
- **Scope:** Standard GA4 reporting access

---

## 4. Landing Page Performance

Entry pages with session counts, engagement metrics, and conversions. Identifies which pages attract visitors and which convert them.

**Use in:** Phase 3 -- Content Performance (landing page analysis)

```json
{
  "dateRanges": [
    {
      "startDate": "2026-02-01",
      "endDate": "2026-02-28"
    }
  ],
  "dimensions": [
    { "name": "landingPage" }
  ],
  "metrics": [
    { "name": "sessions" },
    { "name": "totalUsers" },
    { "name": "engagementRate" },
    { "name": "averageSessionDuration" },
    { "name": "conversions" },
    { "name": "sessionConversionRate" }
  ],
  "orderBys": [
    {
      "metric": { "metricName": "sessions" },
      "desc": true
    }
  ],
  "limit": 50
}
```

**GA4 UI equivalent:** Reports > Engagement > Landing page

**Notes:**
- `landingPage` is the page path (e.g., `/blog/iso-55001-readiness-checklist`) of the first page viewed in a session
- Landing pages with high sessions but low conversion rate are strong CRO candidates -- review CTA placement, form visibility, and content relevance
- Landing pages with high conversion rate but low sessions represent scaling opportunities -- consider driving more traffic via paid or organic channels
- To see landing page performance by source, add `sessionSource` and `sessionMedium` dimensions (see query 4a below)
- Cross-reference with Google Ads landing page data from MBP:google-ads to compare paid landing page performance
- **Scope:** Standard GA4 reporting access

### 4a. Landing Page by Source/Medium

Combines landing page with acquisition source to answer: "Which pages convert best for each traffic source?"

```json
{
  "dateRanges": [
    {
      "startDate": "2026-02-01",
      "endDate": "2026-02-28"
    }
  ],
  "dimensions": [
    { "name": "landingPage" },
    { "name": "sessionSource" },
    { "name": "sessionMedium" }
  ],
  "metrics": [
    { "name": "sessions" },
    { "name": "engagementRate" },
    { "name": "conversions" },
    { "name": "sessionConversionRate" }
  ],
  "orderBys": [
    {
      "metric": { "metricName": "sessions" },
      "desc": true
    }
  ],
  "limit": 100
}
```

**Notes:**
- This query produces a high row count -- use `limit` to focus on the most trafficked combinations
- Particularly useful for comparing paid landing page performance (e.g., `google / cpc` sessions on `/services/asset-management`) against organic entry performance on the same page

---

## 5. Content Performance (Page Path)

Page-level performance across all sessions (not just landing page views). Shows which content users engage with during their visit.

**Use in:** Phase 3 -- Content Performance (page-level analysis)

```json
{
  "dateRanges": [
    {
      "startDate": "2026-02-01",
      "endDate": "2026-02-28"
    }
  ],
  "dimensions": [
    { "name": "pagePath" }
  ],
  "metrics": [
    { "name": "screenPageViews" },
    { "name": "sessions" },
    { "name": "totalUsers" },
    { "name": "engagementRate" },
    { "name": "userEngagementDuration" },
    { "name": "conversions" }
  ],
  "orderBys": [
    {
      "metric": { "metricName": "screenPageViews" },
      "desc": true
    }
  ],
  "limit": 50
}
```

**GA4 UI equivalent:** Reports > Engagement > Pages and screens

**Notes:**
- `pagePath` includes all pages viewed during a session, not just the entry page -- this differs from `landingPage`
- `screenPageViews` counts total page views (including repeat views within a session)
- `userEngagementDuration` on a per-page basis shows how long users actively spent on that page
- Use URL patterns to categorise content:
  - `/blog/*` or `/insights/*` -- blog and thought leadership content
  - `/services/*` -- service offering pages
  - `/resources/*` -- downloadable resources (whitepapers, guides)
  - `/contact` or `/get-in-touch` -- conversion pages
- Pages with high views but low engagement duration may indicate thin content or poor relevance to search intent
- **Scope:** Standard GA4 reporting access

### 5a. Content Performance by Page Title

Use page title instead of path for more readable results, especially when URL structures are not descriptive.

```json
{
  "dateRanges": [
    {
      "startDate": "2026-02-01",
      "endDate": "2026-02-28"
    }
  ],
  "dimensions": [
    { "name": "pageTitle" },
    { "name": "pagePath" }
  ],
  "metrics": [
    { "name": "screenPageViews" },
    { "name": "sessions" },
    { "name": "engagementRate" },
    { "name": "userEngagementDuration" },
    { "name": "conversions" }
  ],
  "orderBys": [
    {
      "metric": { "metricName": "screenPageViews" },
      "desc": true
    }
  ],
  "limit": 50
}
```

### 5b. Blog Content Only

Isolate blog or insight content using a dimension filter on the page path prefix.

```json
{
  "dateRanges": [
    {
      "startDate": "2026-02-01",
      "endDate": "2026-02-28"
    }
  ],
  "dimensions": [
    { "name": "pagePath" }
  ],
  "metrics": [
    { "name": "screenPageViews" },
    { "name": "sessions" },
    { "name": "engagementRate" },
    { "name": "userEngagementDuration" },
    { "name": "conversions" }
  ],
  "dimensionFilter": {
    "filter": {
      "fieldName": "pagePath",
      "stringFilter": {
        "value": "/blog/",
        "matchType": "BEGINS_WITH"
      }
    }
  },
  "orderBys": [
    {
      "metric": { "metricName": "screenPageViews" },
      "desc": true
    }
  ],
  "limit": 30
}
```

**Notes:**
- Adjust the path prefix (`/blog/`, `/insights/`, `/resources/`) to match the website's URL structure
- Compare blog content performance against service pages to assess whether content marketing is contributing to conversions or only to awareness

---

## 6. Device Category Breakdown

Desktop vs mobile vs tablet performance. Critical for identifying device-specific conversion rate gaps.

**Use in:** Phase 1 -- Traffic Overview (device breakdown); Phase 5 -- User Behaviour

```json
{
  "dateRanges": [
    {
      "startDate": "2026-02-01",
      "endDate": "2026-02-28"
    }
  ],
  "dimensions": [
    { "name": "deviceCategory" }
  ],
  "metrics": [
    { "name": "sessions" },
    { "name": "totalUsers" },
    { "name": "newUsers" },
    { "name": "engagementRate" },
    { "name": "screenPageViewsPerSession" },
    { "name": "averageSessionDuration" },
    { "name": "conversions" },
    { "name": "sessionConversionRate" }
  ],
  "orderBys": [
    {
      "metric": { "metricName": "sessions" },
      "desc": true
    }
  ]
}
```

**GA4 UI equivalent:** Reports > Tech > Tech overview (device category card)

**Notes:**
- `deviceCategory` returns: `desktop`, `mobile`, `tablet`
- For B2B websites, desktop typically dominates sessions and has a higher conversion rate
- If mobile conversion rate is significantly lower than desktop (e.g., >50% difference), investigate mobile UX -- form usability, page load speed, CTA visibility
- **Scope:** Standard GA4 reporting access

### 6a. Device by Source/Medium

Cross-reference device category with traffic source to identify channel-specific device patterns.

```json
{
  "dateRanges": [
    {
      "startDate": "2026-02-01",
      "endDate": "2026-02-28"
    }
  ],
  "dimensions": [
    { "name": "deviceCategory" },
    { "name": "sessionSource" },
    { "name": "sessionMedium" }
  ],
  "metrics": [
    { "name": "sessions" },
    { "name": "engagementRate" },
    { "name": "conversions" },
    { "name": "sessionConversionRate" }
  ],
  "orderBys": [
    {
      "metric": { "metricName": "sessions" },
      "desc": true
    }
  ],
  "limit": 50
}
```

**Notes:**
- LinkedIn Ads traffic often skews heavily mobile (users browsing the LinkedIn feed on phones) -- compare mobile vs desktop conversion rate for `linkedin / paid_social` specifically
- Google Ads traffic device split depends on campaign targeting -- cross-reference with device bid adjustments from MBP:google-ads

---

## 7. Geographic Performance

Country and city level traffic and conversion data. Essential for businesses targeting specific geographic markets.

**Use in:** Phase 1 -- Traffic Overview (geographic breakdown)

### 7a. Country-Level Performance

```json
{
  "dateRanges": [
    {
      "startDate": "2026-02-01",
      "endDate": "2026-02-28"
    }
  ],
  "dimensions": [
    { "name": "country" }
  ],
  "metrics": [
    { "name": "sessions" },
    { "name": "totalUsers" },
    { "name": "engagementRate" },
    { "name": "conversions" },
    { "name": "sessionConversionRate" }
  ],
  "orderBys": [
    {
      "metric": { "metricName": "sessions" },
      "desc": true
    }
  ],
  "limit": 20
}
```

### 7b. City-Level Performance (Filtered to Target Country)

```json
{
  "dateRanges": [
    {
      "startDate": "2026-02-01",
      "endDate": "2026-02-28"
    }
  ],
  "dimensions": [
    { "name": "city" }
  ],
  "metrics": [
    { "name": "sessions" },
    { "name": "totalUsers" },
    { "name": "engagementRate" },
    { "name": "conversions" },
    { "name": "sessionConversionRate" }
  ],
  "dimensionFilter": {
    "filter": {
      "fieldName": "country",
      "stringFilter": {
        "value": "Australia",
        "matchType": "EXACT"
      }
    }
  },
  "orderBys": [
    {
      "metric": { "metricName": "sessions" },
      "desc": true
    }
  ],
  "limit": 20
}
```

**GA4 UI equivalent:** Reports > User attributes > Demographic details (primary dimension: Country or City)

**Notes:**
- `country` and `city` are user-scoped dimensions based on IP geolocation
- For Australian-focused businesses, filter to Australia and examine city-level distribution (Sydney, Melbourne, Brisbane, Perth, Adelaide)
- Sessions from unexpected countries with zero conversions may indicate bot traffic or irrelevant ad targeting
- If Google Ads campaigns are geo-targeted to Australia but GA4 shows significant traffic from other countries, investigate campaign location settings (are they set to "presence" or "presence or interest"?)
- City-level data is subject to GA4 thresholding -- small cities may be grouped into "(not set)"
- **Scope:** Standard GA4 reporting access

---

## 8. New vs Returning Users

Behavioural comparison between first-time and returning visitors. Key for understanding nurture effectiveness.

**Use in:** Phase 5 -- User Behaviour (new vs returning analysis)

```json
{
  "dateRanges": [
    {
      "startDate": "2026-02-01",
      "endDate": "2026-02-28"
    }
  ],
  "dimensions": [
    { "name": "newVsReturning" }
  ],
  "metrics": [
    { "name": "sessions" },
    { "name": "totalUsers" },
    { "name": "engagementRate" },
    { "name": "screenPageViewsPerSession" },
    { "name": "averageSessionDuration" },
    { "name": "userEngagementDuration" },
    { "name": "conversions" },
    { "name": "sessionConversionRate" }
  ]
}
```

**GA4 UI equivalent:** Reports > Retention > Overview (new vs returning users card)

**Notes:**
- `newVsReturning` returns two values: `new` and `returning`
- In B2B contexts, returning users typically have significantly higher conversion rates -- they have already evaluated the brand and are further along the decision-making journey
- A healthy B2B website typically has 60-70% new users (indicating ongoing acquisition) with returning users converting at 2-3x the rate of new users
- If returning user conversion rate is not meaningfully higher than new users, the website may lack effective nurture paths (e.g., no email capture, no retargeting, weak content journey)
- **Scope:** Standard GA4 reporting access

### 8a. Returning Users by Source

Identifies which channels bring users back for repeat visits.

```json
{
  "dateRanges": [
    {
      "startDate": "2026-02-01",
      "endDate": "2026-02-28"
    }
  ],
  "dimensions": [
    { "name": "newVsReturning" },
    { "name": "sessionSource" },
    { "name": "sessionMedium" }
  ],
  "metrics": [
    { "name": "sessions" },
    { "name": "engagementRate" },
    { "name": "conversions" },
    { "name": "sessionConversionRate" }
  ],
  "dimensionFilter": {
    "filter": {
      "fieldName": "newVsReturning",
      "stringFilter": {
        "value": "returning",
        "matchType": "EXACT"
      }
    }
  },
  "orderBys": [
    {
      "metric": { "metricName": "sessions" },
      "desc": true
    }
  ],
  "limit": 20
}
```

**Notes:**
- Returning users arriving via `(direct) / (none)` have likely bookmarked the site or typed the URL -- a strong brand signal
- Returning users from `google / organic` may be searching for the brand name specifically -- check branded search terms in MBP:seo
- Returning users from `email / newsletter` or `email / nurture` indicate effective email marketing

---

## 9. Conversion Events

Event-level breakdown of conversion actions. Shows which conversion types are firing and at what volume.

**Use in:** Phase 4 -- Conversion Analysis

```json
{
  "dateRanges": [
    {
      "startDate": "2026-02-01",
      "endDate": "2026-02-28"
    }
  ],
  "dimensions": [
    { "name": "eventName" }
  ],
  "metrics": [
    { "name": "eventCount" },
    { "name": "totalUsers" },
    { "name": "eventCountPerUser" },
    { "name": "conversions" }
  ],
  "dimensionFilter": {
    "filter": {
      "fieldName": "isConversionEvent",
      "stringFilter": {
        "value": "true",
        "matchType": "EXACT"
      }
    }
  },
  "orderBys": [
    {
      "metric": { "metricName": "eventCount" },
      "desc": true
    }
  ]
}
```

**GA4 UI equivalent:** Reports > Engagement > Conversions

**Notes:**
- `isConversionEvent` filters to only events marked as conversions in the GA4 property configuration
- Common GA4 conversion event names: `generate_lead`, `form_submit`, `file_download`, `purchase`, `sign_up`, `contact`, `phone_call_click`
- `eventCount` is the total number of times the event fired; `conversions` counts each event once per session (deduplicated)
- If no conversion events appear, the GA4 property may not have conversion events configured -- flag this as a critical tracking issue
- `eventCountPerUser` helps identify repeat conversions (e.g., a user downloading multiple resources)
- **Scope:** Standard GA4 reporting access. Conversion event marking is configured in GA4 Admin > Events.

### 9a. Conversions by Source/Medium

Combines conversion event data with acquisition source to show which channels drive which conversion types.

```json
{
  "dateRanges": [
    {
      "startDate": "2026-02-01",
      "endDate": "2026-02-28"
    }
  ],
  "dimensions": [
    { "name": "eventName" },
    { "name": "sessionSource" },
    { "name": "sessionMedium" }
  ],
  "metrics": [
    { "name": "eventCount" },
    { "name": "conversions" },
    { "name": "totalUsers" }
  ],
  "dimensionFilter": {
    "filter": {
      "fieldName": "isConversionEvent",
      "stringFilter": {
        "value": "true",
        "matchType": "EXACT"
      }
    }
  },
  "orderBys": [
    {
      "metric": { "metricName": "conversions" },
      "desc": true
    }
  ],
  "limit": 50
}
```

**Notes:**
- This query answers: "Which channels drive which types of conversions?"
- For example, Google Ads may drive `form_submit` conversions (high-intent search) while LinkedIn Ads may drive `file_download` conversions (content engagement)
- Understanding conversion type by channel helps calibrate expectations -- not all channels produce the same conversion type

---

## 10. UTM Campaign Performance

Traffic and conversions broken down by UTM parameters. Essential for evaluating tagged marketing campaigns.

**Use in:** Phase 2 -- Acquisition Source Analysis (campaign-level)

### 10a. Full UTM Breakdown

```json
{
  "dateRanges": [
    {
      "startDate": "2026-02-01",
      "endDate": "2026-02-28"
    }
  ],
  "dimensions": [
    { "name": "sessionSource" },
    { "name": "sessionMedium" },
    { "name": "sessionCampaignName" }
  ],
  "metrics": [
    { "name": "sessions" },
    { "name": "totalUsers" },
    { "name": "newUsers" },
    { "name": "engagementRate" },
    { "name": "conversions" },
    { "name": "sessionConversionRate" }
  ],
  "dimensionFilter": {
    "notExpression": {
      "filter": {
        "fieldName": "sessionCampaignName",
        "stringFilter": {
          "value": "(not set)",
          "matchType": "EXACT"
        }
      }
    }
  },
  "orderBys": [
    {
      "metric": { "metricName": "sessions" },
      "desc": true
    }
  ],
  "limit": 50
}
```

### 10b. UTM Content (Ad/Creative Level)

```json
{
  "dateRanges": [
    {
      "startDate": "2026-02-01",
      "endDate": "2026-02-28"
    }
  ],
  "dimensions": [
    { "name": "sessionSource" },
    { "name": "sessionMedium" },
    { "name": "sessionCampaignName" },
    { "name": "sessionManualAdContent" }
  ],
  "metrics": [
    { "name": "sessions" },
    { "name": "engagementRate" },
    { "name": "conversions" },
    { "name": "sessionConversionRate" }
  ],
  "orderBys": [
    {
      "metric": { "metricName": "sessions" },
      "desc": true
    }
  ],
  "limit": 100
}
```

**GA4 UI equivalent:** Reports > Acquisition > Traffic acquisition (add secondary dimension: Session campaign)

**Notes:**
- `sessionCampaignName` maps to the `utm_campaign` parameter -- should follow the naming convention `{platform}-{objective}-{audience}-{YYYYMM}` per `shared/utm-taxonomy.md`
- `sessionManualAdContent` maps to the `utm_content` parameter -- identifies the specific creative or ad variant
- Campaigns appearing as `(not set)` indicate traffic without UTM campaign tagging
- The `notExpression` filter in query 10a removes `(not set)` campaigns to focus on deliberately tagged traffic
- Validate that campaign names follow the `shared/utm-taxonomy.md` naming convention. Non-standard names make cross-channel reporting in MBP:marketing-dashboard unreliable.
- For Google Ads, auto-tagged campaigns will populate `sessionCampaignName` with the Google Ads campaign name automatically (no UTM required)
- For LinkedIn Ads, `sessionCampaignName` is only populated if `utm_campaign` is set in the ad creative URL -- verify this is configured
- **Scope:** Standard GA4 reporting access

---

## 11. Google Ads Integration

GA4 sessions and conversions from Google Ads specifically. Use this to cross-reference with MBP:google-ads platform data.

**Use in:** Phase 2 -- Acquisition Source Analysis (Google Ads attribution check)

```json
{
  "dateRanges": [
    {
      "startDate": "2026-02-01",
      "endDate": "2026-02-28"
    }
  ],
  "dimensions": [
    { "name": "sessionSource" },
    { "name": "sessionMedium" },
    { "name": "sessionCampaignName" }
  ],
  "metrics": [
    { "name": "sessions" },
    { "name": "totalUsers" },
    { "name": "engagementRate" },
    { "name": "engagedSessions" },
    { "name": "conversions" },
    { "name": "sessionConversionRate" }
  ],
  "dimensionFilter": {
    "andGroup": {
      "expressions": [
        {
          "filter": {
            "fieldName": "sessionSource",
            "stringFilter": {
              "value": "google",
              "matchType": "EXACT"
            }
          }
        },
        {
          "filter": {
            "fieldName": "sessionMedium",
            "stringFilter": {
              "value": "cpc",
              "matchType": "EXACT"
            }
          }
        }
      ]
    }
  },
  "orderBys": [
    {
      "metric": { "metricName": "sessions" },
      "desc": true
    }
  ]
}
```

**Notes:**
- This query isolates `google / cpc` traffic, which corresponds to Google Ads paid search campaigns
- **Critical cross-reference**: Compare total `sessions` from this query with total clicks from the Google Ads platform (via MBP:google-ads). A discrepancy of <15% is normal. Discrepancy >25% indicates tracking issues:
  - GA4 sessions < Google Ads clicks: page load failures, consent banner blocking, redirect chain dropping the `gclid` parameter, or slow pages where users abandon before GA4 loads
  - GA4 sessions > Google Ads clicks: rare, but possible if users bookmark and return to the auto-tagged URL
- If this query returns zero rows but Google Ads campaigns are running, auto-tagging (`gclid`) may be disabled -- this is a critical tracking failure. Flag it as a high-severity issue.
- Campaign names in GA4 come from the Google Ads campaign name when auto-tagging is active -- they should match exactly
- **Scope:** Requires Google Ads to be linked to the GA4 property for auto-tagging. Standard GA4 reporting access.

### 11a. Google Ads with Landing Page

Shows which Google Ads campaigns are sending traffic to which landing pages and how those pages convert.

```json
{
  "dateRanges": [
    {
      "startDate": "2026-02-01",
      "endDate": "2026-02-28"
    }
  ],
  "dimensions": [
    { "name": "sessionCampaignName" },
    { "name": "landingPage" }
  ],
  "metrics": [
    { "name": "sessions" },
    { "name": "engagementRate" },
    { "name": "conversions" },
    { "name": "sessionConversionRate" }
  ],
  "dimensionFilter": {
    "andGroup": {
      "expressions": [
        {
          "filter": {
            "fieldName": "sessionSource",
            "stringFilter": {
              "value": "google",
              "matchType": "EXACT"
            }
          }
        },
        {
          "filter": {
            "fieldName": "sessionMedium",
            "stringFilter": {
              "value": "cpc",
              "matchType": "EXACT"
            }
          }
        }
      ]
    }
  },
  "orderBys": [
    {
      "metric": { "metricName": "sessions" },
      "desc": true
    }
  ],
  "limit": 50
}
```

**Notes:**
- Cross-reference with landing page performance data from MBP:google-ads (GAQL query 8 in the GAQL query library) to compare platform-reported and GA4-reported metrics

---

## 12. LinkedIn Attribution

Sessions from LinkedIn Ads traffic, identified via UTM parameters. Since LinkedIn does not have native GA4 integration like Google Ads, UTM tagging is the sole attribution mechanism.

**Use in:** Phase 2 -- Acquisition Source Analysis (LinkedIn Ads attribution check)

### 12a. LinkedIn Paid Social Traffic

```json
{
  "dateRanges": [
    {
      "startDate": "2026-02-01",
      "endDate": "2026-02-28"
    }
  ],
  "dimensions": [
    { "name": "sessionSource" },
    { "name": "sessionMedium" },
    { "name": "sessionCampaignName" },
    { "name": "sessionManualAdContent" }
  ],
  "metrics": [
    { "name": "sessions" },
    { "name": "totalUsers" },
    { "name": "newUsers" },
    { "name": "engagementRate" },
    { "name": "conversions" },
    { "name": "sessionConversionRate" }
  ],
  "dimensionFilter": {
    "andGroup": {
      "expressions": [
        {
          "filter": {
            "fieldName": "sessionSource",
            "stringFilter": {
              "value": "linkedin",
              "matchType": "EXACT"
            }
          }
        },
        {
          "filter": {
            "fieldName": "sessionMedium",
            "stringFilter": {
              "value": "paid_social",
              "matchType": "EXACT"
            }
          }
        }
      ]
    }
  },
  "orderBys": [
    {
      "metric": { "metricName": "sessions" },
      "desc": true
    }
  ]
}
```

### 12b. All LinkedIn Traffic (Paid + Organic + Referral)

Use this query to understand the full picture of LinkedIn-originated traffic, including untagged sessions.

```json
{
  "dateRanges": [
    {
      "startDate": "2026-02-01",
      "endDate": "2026-02-28"
    }
  ],
  "dimensions": [
    { "name": "sessionSource" },
    { "name": "sessionMedium" },
    { "name": "sessionCampaignName" }
  ],
  "metrics": [
    { "name": "sessions" },
    { "name": "totalUsers" },
    { "name": "engagementRate" },
    { "name": "conversions" },
    { "name": "sessionConversionRate" }
  ],
  "dimensionFilter": {
    "orGroup": {
      "expressions": [
        {
          "filter": {
            "fieldName": "sessionSource",
            "stringFilter": {
              "value": "linkedin",
              "matchType": "EXACT"
            }
          }
        },
        {
          "filter": {
            "fieldName": "sessionSource",
            "stringFilter": {
              "value": "linkedin.com",
              "matchType": "EXACT"
            }
          }
        }
      ]
    }
  },
  "orderBys": [
    {
      "metric": { "metricName": "sessions" },
      "desc": true
    }
  ]
}
```

**Notes:**
- LinkedIn traffic can appear under multiple source values depending on tagging:
  - `linkedin / paid_social` -- correctly UTM-tagged LinkedIn Ads traffic (per `shared/utm-taxonomy.md`)
  - `linkedin / organic_social` -- UTM-tagged organic LinkedIn posts
  - `linkedin.com / referral` -- untagged LinkedIn traffic (could be organic OR paid with missing UTMs)
- **Critical check**: If LinkedIn Ads are actively running (per MBP:linkedin-ads) but `linkedin / paid_social` shows zero or minimal sessions, UTM tagging is broken. Meanwhile, if `linkedin.com / referral` shows high traffic, those are likely your paid sessions appearing as unattributed referral traffic.
- Compare `linkedin / paid_social` sessions with LinkedIn Ads platform click data from MBP:linkedin-ads. Discrepancy >30% is concerning for LinkedIn due to mobile app redirect chain losses.
- Campaign names should follow `{platform}-{objective}-{audience}-{YYYYMM}` format per `shared/utm-taxonomy.md` (e.g., `linkedin-leadgen-utilities-202602`)
- **Scope:** Standard GA4 reporting access. Requires UTM parameters to be applied to all LinkedIn Ads campaigns.

---

## 13. Conversion Paths

Multi-touch attribution data showing the sequence of channels users interact with before converting. Requires the GA4 property to have sufficient conversion volume for path analysis.

**Use in:** Phase 4 -- Conversion Analysis (multi-touch attribution)

### 13a. First User Source/Medium (First Touch Attribution)

```json
{
  "dateRanges": [
    {
      "startDate": "2026-02-01",
      "endDate": "2026-02-28"
    }
  ],
  "dimensions": [
    { "name": "firstUserSource" },
    { "name": "firstUserMedium" }
  ],
  "metrics": [
    { "name": "sessions" },
    { "name": "totalUsers" },
    { "name": "conversions" },
    { "name": "sessionConversionRate" }
  ],
  "orderBys": [
    {
      "metric": { "metricName": "conversions" },
      "desc": true
    }
  ],
  "limit": 20
}
```

### 13b. Last Touch Attribution (Session Source of Converting Sessions)

Run this alongside 13a and compare to identify channels that introduce users (first touch) vs channels that close conversions (last touch).

```json
{
  "dateRanges": [
    {
      "startDate": "2026-02-01",
      "endDate": "2026-02-28"
    }
  ],
  "dimensions": [
    { "name": "sessionSource" },
    { "name": "sessionMedium" }
  ],
  "metrics": [
    { "name": "conversions" },
    { "name": "totalUsers" }
  ],
  "metricFilter": {
    "filter": {
      "fieldName": "conversions",
      "numericFilter": {
        "operation": "GREATER_THAN",
        "value": {
          "int64Value": "0"
        }
      }
    }
  },
  "orderBys": [
    {
      "metric": { "metricName": "conversions" },
      "desc": true
    }
  ],
  "limit": 20
}
```

### 13c. Session Count Before Conversion

Shows how many sessions users had before converting, indicating typical conversion path length.

```json
{
  "dateRanges": [
    {
      "startDate": "2026-02-01",
      "endDate": "2026-02-28"
    }
  ],
  "dimensions": [
    { "name": "sessionNumber" }
  ],
  "metrics": [
    { "name": "conversions" },
    { "name": "sessions" }
  ],
  "metricFilter": {
    "filter": {
      "fieldName": "conversions",
      "numericFilter": {
        "operation": "GREATER_THAN",
        "value": {
          "int64Value": "0"
        }
      }
    }
  },
  "orderBys": [
    {
      "dimension": { "dimensionName": "sessionNumber" },
      "desc": false
    }
  ],
  "limit": 20
}
```

**GA4 UI equivalent:** Advertising > Attribution > Conversion paths (for full path visualisation)

**Notes:**
- `firstUserSource` and `firstUserMedium` are user-scoped dimensions -- they record the source/medium of the user's very first visit, regardless of which session they are currently in
- `sessionSource` and `sessionMedium` are session-scoped -- they record the source/medium of the current session
- Comparing first touch vs last touch reveals the "assist" role of channels:
  - A channel with many first touches but few last touches is an **introducer** (e.g., Paid Social often introduces users who later convert via Direct or Organic Search)
  - A channel with few first touches but many last touches is a **closer** (e.g., Direct traffic, branded organic search)
- `sessionNumber` indicates how many sessions the user has had. If most conversions occur on session 1, the conversion path is short. If conversions cluster around sessions 3-5, there is a multi-visit consideration phase -- nurture and retargeting are important.
- For more granular path analysis, consider using the GA4 UI Advertising section (attribution paths) or the GA4 Data API `runFunnelReport` method, which is not covered in this library
- **Scope:** Full conversion path data in the GA4 UI Advertising section requires Google Ads to be linked. The Data API queries above work with standard reporting access.

---

## 14. Engagement Trends

Daily and weekly engagement rate and session trends for identifying patterns and anomalies over time.

**Use in:** Phase 5 -- User Behaviour (engagement trends)

### 14a. Daily Session and Engagement Trend

```json
{
  "dateRanges": [
    {
      "startDate": "2026-02-01",
      "endDate": "2026-02-28"
    }
  ],
  "dimensions": [
    { "name": "date" }
  ],
  "metrics": [
    { "name": "sessions" },
    { "name": "totalUsers" },
    { "name": "newUsers" },
    { "name": "engagementRate" },
    { "name": "engagedSessions" },
    { "name": "screenPageViewsPerSession" },
    { "name": "conversions" }
  ],
  "orderBys": [
    {
      "dimension": { "dimensionName": "date" },
      "desc": false
    }
  ]
}
```

### 14b. Weekly Session and Engagement Trend

```json
{
  "dateRanges": [
    {
      "startDate": "2026-02-01",
      "endDate": "2026-02-28"
    }
  ],
  "dimensions": [
    { "name": "isoYearIsoWeek" }
  ],
  "metrics": [
    { "name": "sessions" },
    { "name": "totalUsers" },
    { "name": "newUsers" },
    { "name": "engagementRate" },
    { "name": "engagedSessions" },
    { "name": "conversions" },
    { "name": "sessionConversionRate" }
  ],
  "orderBys": [
    {
      "dimension": { "dimensionName": "isoYearIsoWeek" },
      "desc": false
    }
  ]
}
```

### 14c. Day of Week Pattern

Aggregated day-of-week performance across the analysis period. Identifies which days of the week drive the most engagement and conversions.

```json
{
  "dateRanges": [
    {
      "startDate": "2026-02-01",
      "endDate": "2026-02-28"
    }
  ],
  "dimensions": [
    { "name": "dayOfWeekName" }
  ],
  "metrics": [
    { "name": "sessions" },
    { "name": "engagementRate" },
    { "name": "conversions" },
    { "name": "sessionConversionRate" }
  ]
}
```

### 14d. Hourly Pattern

Aggregated hour-of-day performance. Useful for identifying peak activity windows for ad scheduling.

```json
{
  "dateRanges": [
    {
      "startDate": "2026-02-01",
      "endDate": "2026-02-28"
    }
  ],
  "dimensions": [
    { "name": "hour" }
  ],
  "metrics": [
    { "name": "sessions" },
    { "name": "engagementRate" },
    { "name": "conversions" }
  ],
  "orderBys": [
    {
      "dimension": { "dimensionName": "hour" },
      "desc": false
    }
  ]
}
```

**Notes:**
- `date` dimension returns dates in `YYYYMMDD` format (e.g., `20260201`)
- `isoYearIsoWeek` returns week numbers in `YYYYWW` format (e.g., `202606` for week 6 of 2026) -- useful for smoothing out daily volatility
- `dayOfWeekName` returns the day name (e.g., `Monday`, `Tuesday`) -- aggregated across all weeks in the date range
- `hour` returns the hour of day in the GA4 property's configured time zone (0-23)
- **Daily trends** reveal sudden spikes or drops -- correlate with campaign launches, content publications, or external events
- **Weekly trends** smooth out day-of-week effects and show the underlying growth or decline trajectory
- **Day-of-week patterns** are valuable for B2B: business days typically show higher quality traffic than weekends. If weekend traffic has very low engagement, consider scheduling Google Ads to reduce weekend spend (cross-reference with MBP:google-ads)
- **Hourly patterns** help identify peak activity windows -- useful for ad scheduling and content publication timing
- **Scope:** Standard GA4 reporting access

---

## Custom Date Range Patterns

For any of the above queries, adapt the `dateRanges` field to suit the analysis period.

```json
{
  "dateRanges": [
    { "startDate": "30daysAgo", "endDate": "yesterday" }
  ]
}
```

```json
{
  "dateRanges": [
    { "startDate": "7daysAgo", "endDate": "yesterday" }
  ]
}
```

```json
{
  "dateRanges": [
    { "startDate": "2026-02-01", "endDate": "2026-02-28" }
  ]
}
```

```json
{
  "dateRanges": [
    { "startDate": "2026-02-01", "endDate": "2026-02-28", "name": "current" },
    { "startDate": "2026-01-01", "endDate": "2026-01-31", "name": "previous" }
  ]
}
```

```json
{
  "dateRanges": [
    { "startDate": "2026-02-01", "endDate": "2026-02-28", "name": "current" },
    { "startDate": "2025-02-01", "endDate": "2025-02-28", "name": "year_ago" }
  ]
}
```

```json
{
  "dateRanges": [
    { "startDate": "2026-01-01", "endDate": "today" }
  ]
}
```

**Notes:**
- Relative date values (`today`, `yesterday`, `7daysAgo`, `30daysAgo`) are calculated based on the GA4 property's configured time zone
- Named date ranges (`"name": "current"`) allow you to distinguish between periods in the API response -- each row will include a `dateRange` field indicating which period it belongs to
- When comparing periods, ensure the date ranges cover the same number of days for fair comparison. A 31-day month vs a 28-day month will skew absolute counts.
- For period-over-period delta calculations:
  - Absolute change: `current_value - previous_value`
  - Percentage change: `(current_value - previous_value) / previous_value * 100`
  - For rates (engagement rate, conversion rate): use percentage point change, not percentage change (e.g., 62% to 58% is a 4 percentage point decline, not a 6.5% decline)

---

## Dimension Filter Patterns

Common filter patterns reusable across any query in this library.

### Filter by Specific Page Path Prefix

```json
{
  "dimensionFilter": {
    "filter": {
      "fieldName": "pagePath",
      "stringFilter": {
        "value": "/blog/",
        "matchType": "BEGINS_WITH"
      }
    }
  }
}
```

### Filter by Multiple Sources (OR Logic)

```json
{
  "dimensionFilter": {
    "orGroup": {
      "expressions": [
        {
          "filter": {
            "fieldName": "sessionSource",
            "stringFilter": {
              "value": "google",
              "matchType": "EXACT"
            }
          }
        },
        {
          "filter": {
            "fieldName": "sessionSource",
            "stringFilter": {
              "value": "bing",
              "matchType": "EXACT"
            }
          }
        }
      ]
    }
  }
}
```

### Filter by Source AND Medium (AND Logic)

```json
{
  "dimensionFilter": {
    "andGroup": {
      "expressions": [
        {
          "filter": {
            "fieldName": "sessionSource",
            "stringFilter": {
              "value": "google",
              "matchType": "EXACT"
            }
          }
        },
        {
          "filter": {
            "fieldName": "sessionMedium",
            "stringFilter": {
              "value": "cpc",
              "matchType": "EXACT"
            }
          }
        }
      ]
    }
  }
}
```

### Exclude Direct Traffic

```json
{
  "dimensionFilter": {
    "notExpression": {
      "filter": {
        "fieldName": "sessionSource",
        "stringFilter": {
          "value": "(direct)",
          "matchType": "EXACT"
        }
      }
    }
  }
}
```

### Filter to Paid Channels Only

```json
{
  "dimensionFilter": {
    "filter": {
      "fieldName": "sessionDefaultChannelGroup",
      "inListFilter": {
        "values": ["Paid Search", "Paid Social", "Display"]
      }
    }
  }
}
```

### Filter to Australian Traffic Only

```json
{
  "dimensionFilter": {
    "filter": {
      "fieldName": "country",
      "stringFilter": {
        "value": "Australia",
        "matchType": "EXACT"
      }
    }
  }
}
```

### Filter by Regex (Page Path Pattern)

```json
{
  "dimensionFilter": {
    "filter": {
      "fieldName": "pagePath",
      "stringFilter": {
        "value": "^/services/(asset-management|data-quality|consulting)",
        "matchType": "FULL_REGEXP"
      }
    }
  }
}
```

**Notes:**
- `matchType` values: `EXACT`, `BEGINS_WITH`, `ENDS_WITH`, `CONTAINS`, `FULL_REGEXP`, `PARTIAL_REGEXP`
- Filters can be nested using `andGroup`, `orGroup`, and `notExpression` for complex logic
- Dimension filters reduce the data before aggregation -- this is more efficient than fetching all data and filtering downstream
- Regex filters (`FULL_REGEXP`, `PARTIAL_REGEXP`) follow RE2 syntax

---

## Metric Filter Patterns

Filter rows based on metric values in the response. Metric filters are applied after aggregation.

### Only Show High-Traffic Pages (Minimum Sessions Threshold)

```json
{
  "metricFilter": {
    "filter": {
      "fieldName": "sessions",
      "numericFilter": {
        "operation": "GREATER_THAN_OR_EQUAL",
        "value": {
          "int64Value": "10"
        }
      }
    }
  }
}
```

### Only Show Converting Sources

```json
{
  "metricFilter": {
    "filter": {
      "fieldName": "conversions",
      "numericFilter": {
        "operation": "GREATER_THAN",
        "value": {
          "int64Value": "0"
        }
      }
    }
  }
}
```

**Notes:**
- Metric filters are applied after aggregation -- they filter rows from the result set rather than filtering raw data
- `numericFilter.operation` values: `EQUAL`, `LESS_THAN`, `LESS_THAN_OR_EQUAL`, `GREATER_THAN`, `GREATER_THAN_OR_EQUAL`
- Use metric filters to remove noise from reports (e.g., pages with only 1-2 sessions that are not statistically meaningful)

---

## GA4 Dimension Reference

Quick reference for commonly used GA4 dimensions across the queries in this library.

| Dimension | Scope | Description | Example Values |
|---|---|---|---|
| `sessionSource` | Session | Traffic source for the session | `google`, `linkedin`, `(direct)`, `linkedin.com` |
| `sessionMedium` | Session | Traffic medium for the session | `organic`, `cpc`, `paid_social`, `referral`, `(none)` |
| `sessionCampaignName` | Session | Campaign name (from UTM or auto-tag) | `linkedin-leadgen-utilities-202602`, `(not set)` |
| `sessionManualAdContent` | Session | UTM content parameter (`utm_content`) | `iso55001-awareness-v2`, `(not set)` |
| `sessionDefaultChannelGroup` | Session | GA4 default channel group | `Organic Search`, `Paid Search`, `Paid Social`, `Direct` |
| `firstUserSource` | User | Source of the user's first ever session | `google`, `linkedin` |
| `firstUserMedium` | User | Medium of the user's first ever session | `organic`, `cpc`, `paid_social` |
| `newVsReturning` | Session | Whether the user is new or returning | `new`, `returning` |
| `deviceCategory` | Session | Device type | `desktop`, `mobile`, `tablet` |
| `country` | User | User's country (from IP geolocation) | `Australia`, `United States` |
| `city` | User | User's city (from IP geolocation) | `Sydney`, `Melbourne`, `Brisbane` |
| `pagePath` | Event | Page URL path | `/blog/iso-55001-guide`, `/services/` |
| `pageTitle` | Event | HTML page title | `ISO 55001 Readiness Guide` |
| `landingPage` | Session | First page viewed in the session | `/`, `/blog/data-quality-tips` |
| `eventName` | Event | GA4 event name | `page_view`, `form_submit`, `file_download` |
| `isConversionEvent` | Event | Whether the event is marked as conversion | `true`, `false` |
| `date` | Event | Date in `YYYYMMDD` format | `20260201` |
| `isoYearIsoWeek` | Event | ISO year and week number | `202606` |
| `yearMonth` | Event | Year and month in `YYYYMM` format | `202602` |
| `dayOfWeekName` | Event | Day of the week name | `Monday`, `Tuesday` |
| `hour` | Event | Hour of day (0-23) | `9`, `14`, `22` |
| `sessionNumber` | Session | The ordinal session number for the user | `1`, `2`, `5` |

---

## GA4 Metric Reference

Quick reference for commonly used GA4 metrics across the queries in this library.

| Metric | Type | Description |
|---|---|---|
| `sessions` | Integer | Total number of sessions |
| `totalUsers` | Integer | Total unique users |
| `newUsers` | Integer | Users visiting for the first time |
| `engagementRate` | Decimal | Proportion of engaged sessions (>10s, conversion, or 2+ pages) |
| `engagedSessions` | Integer | Number of engaged sessions |
| `bounceRate` | Decimal | Proportion of non-engaged sessions (inverse of engagement rate) |
| `averageSessionDuration` | Seconds | Average session length (includes idle time) |
| `userEngagementDuration` | Seconds | Total active engagement time |
| `screenPageViews` | Integer | Total page views |
| `screenPageViewsPerSession` | Decimal | Average pages viewed per session |
| `conversions` | Integer | Total conversion events (deduplicated per session) |
| `sessionConversionRate` | Decimal | Proportion of sessions with at least one conversion |
| `eventCount` | Integer | Total event count |
| `eventCountPerUser` | Decimal | Average events per user |

---

## MCP Tool Mapping

When a GA4 MCP server is connected, the query bodies above can be passed to the MCP tool that corresponds to the `RunReport` endpoint. The exact tool name depends on the MCP server implementation.

| MCP Server | Likely Tool Name | Notes |
|---|---|---|
| GA4 Data API MCP (generic) | `runReport` or `run_report` | Pass the full JSON body as the request parameter |
| Custom GA4 MCP | Varies | Check available tools with the MCP server; look for a tool that accepts `dimensions`, `metrics`, and `dateRanges` parameters |

**Usage pattern:**
1. Confirm GA4 property ID with the user
2. Check which MCP tools are available
3. Adapt the query body from this library to match the MCP tool's expected parameter format
4. Execute the query and parse the response

**Response parsing:**
- The API returns rows with `dimensionValues` and `metricValues` arrays
- Dimension values are strings; metric values may be strings representing integers or decimals
- An empty response (no rows) may indicate: no data for the date range, dimension filter too restrictive, or GA4 thresholding applied

---

## Rate Limiting and Best Practices

- The GA4 Data API has per-property quota limits (typically 200 requests per minute, varying by property tier)
- Batch related analysis into fewer, broader queries where possible rather than running many narrow queries
- Use `limit` to constrain result sets -- start with 50 rows and expand only if needed
- For large date ranges with daily segments, be mindful of result set size (e.g., 28 days * 50 source/mediums = 1,400 rows)
- Cache results within a single analysis session -- do not re-run the same query multiple times
- If quota errors occur, wait 60 seconds before retrying

---

*Reference document for MBP:website-analytics. See `shared/utm-taxonomy.md` for UTM parameter conventions used across all MBP marketing skills.*
