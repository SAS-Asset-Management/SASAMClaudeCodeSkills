# GA4 Query Library

Common GA4 Data API queries for MBP:website-analytics. Use these patterns when querying GA4 via MCP or as a guide for which GA4 UI reports to export.

These queries use the GA4 Data API v1 (also known as the Google Analytics Data API). When using via MCP, adapt the format to match the MCP server's expected input structure.

---

## 1. Traffic by Source / Medium

The foundational acquisition query. Breaks down all sessions by how users arrived.

### GA4 Data API Request

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
    { "name": "sessionDefaultChannelGroup" }
  ],
  "metrics": [
    { "name": "sessions" },
    { "name": "totalUsers" },
    { "name": "newUsers" },
    { "name": "engagementRate" },
    { "name": "engagedSessions" },
    { "name": "averageSessionDuration" },
    { "name": "screenPageViewsPerSession" },
    { "name": "conversions" }
  ],
  "orderBys": [
    {
      "metric": { "metricName": "sessions" },
      "desc": true
    }
  ],
  "limit": 25
}
```

### GA4 UI Equivalent

**Reports > Acquisition > Traffic acquisition**
- Primary dimension: Session source / medium
- Secondary dimension: Session default channel group
- Columns: Sessions, Users, New users, Engagement rate, Conversions

### What to Look For

- Verify `google / cpc` traffic exists if Google Ads campaigns are running
- Verify `linkedin / paid_social` traffic exists if LinkedIn Ads campaigns are running (requires UTM tagging)
- Check proportion of `(direct) / (none)` — if >30% of total, investigate untagged campaigns
- Compare source/medium values against `shared/utm-taxonomy.md` for consistency

---

## 2. Traffic by Default Channel Group (Summary)

Higher-level view that groups sources into standard channel categories.

### GA4 Data API Request

```json
{
  "dateRanges": [
    {
      "startDate": "2026-02-01",
      "endDate": "2026-02-28"
    },
    {
      "startDate": "2026-01-01",
      "endDate": "2026-01-31"
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
    { "name": "userConversionRate" }
  ],
  "orderBys": [
    {
      "metric": { "metricName": "sessions" },
      "desc": true
    }
  ]
}
```

### Notes

- Using two date ranges returns both current and comparison period data in a single query
- GA4 default channel groups: Organic Search, Paid Search, Paid Social, Organic Social, Direct, Referral, Email, Display, Video, Affiliates, Cross-network
- Channel grouping rules are applied by GA4 based on source, medium, and campaign parameters

---

## 3. Content Performance (Top Pages)

Identifies which pages drive traffic, engagement, and conversions.

### GA4 Data API Request

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
    { "name": "averageSessionDuration" },
    { "name": "conversions" },
    { "name": "userConversionRate" }
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

### GA4 UI Equivalent

**Reports > Engagement > Pages and screens**
- Primary dimension: Page path and screen class
- Columns: Views, Users, Engagement rate, Average engagement time, Conversions

### Variant: Blog Content Only

Add a dimension filter to isolate blog content:

```json
{
  "dimensionFilter": {
    "filter": {
      "fieldName": "pagePath",
      "stringFilter": {
        "matchType": "BEGINS_WITH",
        "value": "/blog/"
      }
    }
  }
}
```

Adjust the path prefix (`/blog/`, `/insights/`, `/resources/`) to match the website's URL structure.

---

## 4. Landing Page Analysis

Which pages users enter the site on, and how those entry points convert.

### GA4 Data API Request

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
    { "name": "newUsers" },
    { "name": "engagementRate" },
    { "name": "averageSessionDuration" },
    { "name": "screenPageViewsPerSession" },
    { "name": "conversions" },
    { "name": "userConversionRate" }
  ],
  "orderBys": [
    {
      "metric": { "metricName": "sessions" },
      "desc": true
    }
  ],
  "limit": 30
}
```

### GA4 UI Equivalent

**Reports > Engagement > Landing page**
- Primary dimension: Landing page
- Columns: Sessions, Users, New users, Engagement rate, Conversions

### Variant: Landing Pages by Source

Combine landing page with source to understand which channels drive traffic to which entry points:

```json
{
  "dimensions": [
    { "name": "landingPage" },
    { "name": "sessionSource" },
    { "name": "sessionMedium" }
  ],
  "metrics": [
    { "name": "sessions" },
    { "name": "conversions" },
    { "name": "userConversionRate" }
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

---

## 5. Conversion Events

Breaks down conversions by event name — essential for understanding which conversion actions are firing.

### GA4 Data API Request

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
    { "name": "eventCountPerUser" }
  ],
  "dimensionFilter": {
    "filter": {
      "fieldName": "eventName",
      "inListFilter": {
        "values": ["generate_lead", "form_submit", "file_download", "sign_up", "purchase"]
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

### Notes

- Adjust the `inListFilter` values to match the website's actual conversion event names
- GA4 marks events as conversions in the admin settings — only marked events appear in the `conversions` metric
- Common conversion event names: `generate_lead`, `form_submit`, `file_download`, `sign_up`, `purchase`, `contact`, `book_demo`

### Variant: Conversions by Source

```json
{
  "dimensions": [
    { "name": "eventName" },
    { "name": "sessionSource" },
    { "name": "sessionMedium" }
  ],
  "metrics": [
    { "name": "eventCount" },
    { "name": "totalUsers" }
  ],
  "dimensionFilter": {
    "filter": {
      "fieldName": "eventName",
      "inListFilter": {
        "values": ["generate_lead", "form_submit", "file_download"]
      }
    }
  },
  "orderBys": [
    {
      "metric": { "metricName": "eventCount" },
      "desc": true
    }
  ],
  "limit": 30
}
```

---

## 6. Conversion Paths (Multi-Touch Attribution)

Understand the sequence of channels users interact with before converting.

### GA4 Data API Request

```json
{
  "dateRanges": [
    {
      "startDate": "2026-02-01",
      "endDate": "2026-02-28"
    }
  ],
  "dimensions": [
    { "name": "sessionDefaultChannelGroup" }
  ],
  "metrics": [
    { "name": "conversions" },
    { "name": "totalUsers" },
    { "name": "sessions" }
  ],
  "orderBys": [
    {
      "metric": { "metricName": "conversions" },
      "desc": true
    }
  ]
}
```

### GA4 UI Equivalent

**Advertising > Attribution > Conversion paths**
- Shows the sequence of channels in conversion paths
- Toggle between first touch, last touch, and data-driven attribution models

### Notes

- Full path analysis requires the GA4 Advertising workspace, which needs linked Google Ads
- For LinkedIn attribution in multi-touch paths, UTM-tagged traffic must be present — without UTMs, LinkedIn will appear under Organic Social or Referral, breaking the attribution chain
- Conversion path data may be subject to thresholding in low-volume properties

---

## 7. Device Breakdown

Understand how traffic and conversions differ across device categories.

### GA4 Data API Request

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
    { "name": "engagementRate" },
    { "name": "averageSessionDuration" },
    { "name": "screenPageViewsPerSession" },
    { "name": "conversions" },
    { "name": "userConversionRate" }
  ],
  "orderBys": [
    {
      "metric": { "metricName": "sessions" },
      "desc": true
    }
  ]
}
```

### Variant: Device by Source

Cross-reference device with source to identify channel-specific device patterns (e.g., LinkedIn social traffic is predominantly mobile):

```json
{
  "dimensions": [
    { "name": "deviceCategory" },
    { "name": "sessionDefaultChannelGroup" }
  ],
  "metrics": [
    { "name": "sessions" },
    { "name": "engagementRate" },
    { "name": "conversions" }
  ],
  "orderBys": [
    {
      "metric": { "metricName": "sessions" },
      "desc": true
    }
  ]
}
```

---

## 8. Geographic Analysis

Identify where users are located — important for B2B targeting validation.

### GA4 Data API Request

```json
{
  "dateRanges": [
    {
      "startDate": "2026-02-01",
      "endDate": "2026-02-28"
    }
  ],
  "dimensions": [
    { "name": "country" },
    { "name": "city" }
  ],
  "metrics": [
    { "name": "sessions" },
    { "name": "totalUsers" },
    { "name": "engagementRate" },
    { "name": "conversions" }
  ],
  "orderBys": [
    {
      "metric": { "metricName": "sessions" },
      "desc": true
    }
  ],
  "limit": 30
}
```

### Variant: Country-Level Only

```json
{
  "dimensions": [
    { "name": "country" }
  ],
  "metrics": [
    { "name": "sessions" },
    { "name": "totalUsers" },
    { "name": "engagementRate" },
    { "name": "conversions" },
    { "name": "userConversionRate" }
  ],
  "orderBys": [
    {
      "metric": { "metricName": "sessions" },
      "desc": true
    }
  ],
  "limit": 15
}
```

### What to Look For

- For Australian-focused B2B, the majority of converting traffic should come from Australia
- High volumes of traffic from unexpected geographies may indicate bot traffic or irrelevant ad targeting
- City-level data helps validate whether traffic aligns with target industry geographies (e.g., mining-heavy regions)

---

## 9. New vs Returning Users

Compare behaviour between first-time and returning visitors.

### GA4 Data API Request

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
    { "name": "averageSessionDuration" },
    { "name": "screenPageViewsPerSession" },
    { "name": "conversions" },
    { "name": "userConversionRate" }
  ]
}
```

### What to Look For

- Returning users typically have 2-3x higher conversion rates than new users in B2B
- If new user conversion rate is very low, the site may need better first-visit CTAs or trust signals
- The ratio of new-to-returning indicates whether the site is growing its audience (high new %) or retaining well (high returning %)

---

## 10. Traffic Trend Over Time

Track session and conversion trends across the analysis period.

### GA4 Data API Request (Daily)

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
    { "name": "engagementRate" },
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

### Variant: Weekly Aggregation

```json
{
  "dimensions": [
    { "name": "isoYearIsoWeek" }
  ],
  "metrics": [
    { "name": "sessions" },
    { "name": "totalUsers" },
    { "name": "engagementRate" },
    { "name": "conversions" }
  ],
  "orderBys": [
    {
      "dimension": { "dimensionName": "isoYearIsoWeek" },
      "desc": false
    }
  ]
}
```

### Variant: Monthly Aggregation (for longer periods)

```json
{
  "dimensions": [
    { "name": "yearMonth" }
  ],
  "metrics": [
    { "name": "sessions" },
    { "name": "totalUsers" },
    { "name": "newUsers" },
    { "name": "engagementRate" },
    { "name": "conversions" },
    { "name": "userConversionRate" }
  ],
  "orderBys": [
    {
      "dimension": { "dimensionName": "yearMonth" },
      "desc": false
    }
  ]
}
```

---

## 11. UTM Campaign Performance

Analyse performance of specifically tagged campaigns. Critical for LinkedIn Ads attribution.

### GA4 Data API Request

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
    { "name": "sessionSource" },
    { "name": "sessionMedium" }
  ],
  "metrics": [
    { "name": "sessions" },
    { "name": "totalUsers" },
    { "name": "engagementRate" },
    { "name": "conversions" },
    { "name": "userConversionRate" }
  ],
  "dimensionFilter": {
    "notExpression": {
      "filter": {
        "fieldName": "sessionCampaignName",
        "stringFilter": {
          "matchType": "EXACT",
          "value": "(not set)"
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
  "limit": 30
}
```

### Notes

- Filters out `(not set)` campaigns to focus on deliberately tagged traffic
- Campaign names should follow the convention in `shared/utm-taxonomy.md`: `{platform}-{objective}-{audience}-{YYYYMM}`
- Cross-reference campaign names with MBP:google-ads and MBP:linkedin-ads data to validate consistency

---

## 12. Exit Pages

Identify where users leave the site. Useful for finding content or UX problems.

### GA4 Data API Request

GA4 does not have a direct "exit page" dimension in the Data API like Universal Analytics did. Instead, approximate exit analysis by looking at pages with low engagement:

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
    { "name": "averageSessionDuration" },
    { "name": "bounceRate" }
  ],
  "orderBys": [
    {
      "metric": { "metricName": "bounceRate" },
      "desc": true
    }
  ],
  "limit": 20
}
```

### GA4 UI Equivalent

Use the **Explore** workspace in GA4:
1. Create a Free Form exploration
2. Add `Page path` as a dimension
3. Add `Exits` and `Exit rate` as metrics (available in Explore but not the standard Data API)
4. Sort by exits descending

### Notes

- In GA4, `bounceRate` is the inverse of `engagementRate` (bounceRate = 1 - engagementRate)
- High bounce/exit rates on confirmation or thank-you pages are expected and not a concern
- Focus investigation on service pages, blog posts, and landing pages with unexpectedly high exit rates

---

## Query Tips

### Date Range Patterns

```json
// Last 30 days
{ "startDate": "30daysAgo", "endDate": "yesterday" }

// This month
{ "startDate": "2026-03-01", "endDate": "2026-03-02" }

// Comparison: current vs previous period
[
  { "startDate": "2026-02-01", "endDate": "2026-02-28" },
  { "startDate": "2026-01-01", "endDate": "2026-01-31" }
]
```

### Common Dimension Filters

```json
// Filter to a specific source
{
  "filter": {
    "fieldName": "sessionSource",
    "stringFilter": {
      "matchType": "EXACT",
      "value": "google"
    }
  }
}

// Filter to paid traffic only
{
  "filter": {
    "fieldName": "sessionDefaultChannelGroup",
    "inListFilter": {
      "values": ["Paid Search", "Paid Social", "Display"]
    }
  }
}

// Filter to Australian traffic only
{
  "filter": {
    "fieldName": "country",
    "stringFilter": {
      "matchType": "EXACT",
      "value": "Australia"
    }
  }
}
```

### Metric Definitions Reference

| GA4 Metric | API Name | Description |
|---|---|---|
| Sessions | `sessions` | Total number of sessions |
| Total users | `totalUsers` | Total unique users |
| New users | `newUsers` | First-time users |
| Engagement rate | `engagementRate` | Engaged sessions / total sessions |
| Bounce rate | `bounceRate` | 1 - engagement rate |
| Avg. session duration | `averageSessionDuration` | Average time per session (seconds) |
| Pages per session | `screenPageViewsPerSession` | Average page views per session |
| Conversions | `conversions` | Total conversion events (all marked conversion events) |
| User conversion rate | `userConversionRate` | Converting users / total users |
| Page views | `screenPageViews` | Total page views |
| Event count | `eventCount` | Total event occurrences |

### Dimension Definitions Reference

| GA4 Dimension | API Name | Description |
|---|---|---|
| Source | `sessionSource` | Traffic source (e.g., google, linkedin) |
| Medium | `sessionMedium` | Traffic medium (e.g., organic, cpc, paid_social) |
| Channel group | `sessionDefaultChannelGroup` | GA4 default channel grouping |
| Campaign | `sessionCampaignName` | UTM campaign or Google Ads campaign name |
| Page path | `pagePath` | URL path of the page |
| Landing page | `landingPage` | First page of the session |
| Device | `deviceCategory` | desktop, mobile, or tablet |
| Country | `country` | User's country |
| City | `city` | User's city |
| Date | `date` | Date in YYYYMMDD format |
| New vs returning | `newVsReturning` | `new` or `returning` |
| Event name | `eventName` | Name of the GA4 event |

---

*Reference document for MBP:website-analytics. See `shared/utm-taxonomy.md` for UTM parameter conventions used across all MBP marketing skills.*
