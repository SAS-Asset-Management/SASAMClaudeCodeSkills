# GAQL Query Library

Pre-built Google Ads Query Language (GAQL) queries for use with the `mcp-google-ads` MCP server. These queries cover the most common analysis tasks in MBP:google-ads.

## Important Notes

- **Cost values** are returned in micros (divide by 1,000,000 for currency)
- **Impression share** values are decimals (0.0-1.0), not percentages
- **Quality Score** is only available at the keyword level
- **Date ranges** use the `DURING` clause with predefined constants or `BETWEEN` for custom ranges
- **Removed entities** are excluded by default using status filters
- **Segment fields** in the SELECT clause automatically segment all metrics in the response

---

## 1. Account Summary

High-level account performance aggregated across all campaigns for the specified period.

```sql
SELECT
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value,
  metrics.average_cpc,
  metrics.ctr,
  metrics.cost_per_conversion,
  metrics.value_per_conversion
FROM customer
WHERE segments.date DURING LAST_30_DAYS
```

**Use in:** Phase 1 — Account Overview

**Notes:**
- Querying from `customer` resource returns account-level aggregates
- Change `DURING LAST_30_DAYS` to `DURING LAST_7_DAYS`, `DURING THIS_MONTH`, etc. as needed
- For period-over-period comparison, run twice with different date ranges

---

## 2. Campaign Performance with Daily Segments

Campaign-level metrics broken out by date for trend analysis.

```sql
SELECT
  campaign.name,
  campaign.status,
  campaign.advertising_channel_type,
  segments.date,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value,
  metrics.average_cpc
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status != 'REMOVED'
ORDER BY campaign.name ASC, segments.date ASC
```

**Use in:** Phase 2 — Campaign Deep-Dive (performance trend)

**Notes:**
- Including `segments.date` in SELECT automatically segments all metrics by day
- Results will have one row per campaign per day
- Use this to plot daily trends and identify sudden changes
- For weekly aggregation, process the daily data downstream (GAQL does not natively support weekly grouping)

---

## 3. Keyword Performance with Quality Score

Keyword-level metrics including Quality Score and its component ratings.

```sql
SELECT
  campaign.name,
  ad_group.name,
  ad_group_criterion.keyword.text,
  ad_group_criterion.keyword.match_type,
  ad_group_criterion.status,
  ad_group_criterion.quality_info.quality_score,
  ad_group_criterion.quality_info.creative_quality_score,
  ad_group_criterion.quality_info.search_predicted_ctr,
  ad_group_criterion.quality_info.post_click_quality_score,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value,
  metrics.average_cpc
FROM keyword_view
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
  AND ad_group.status = 'ENABLED'
  AND ad_group_criterion.status = 'ENABLED'
ORDER BY metrics.cost_micros DESC
```

**Use in:** Phase 2 — Top keywords, Quality Score distribution

**Notes:**
- Quality Score components use these values:
  - `creative_quality_score` (Ad Relevance): BELOW_AVERAGE, AVERAGE, ABOVE_AVERAGE
  - `search_predicted_ctr` (Expected CTR): BELOW_AVERAGE, AVERAGE, ABOVE_AVERAGE
  - `post_click_quality_score` (Landing Page Experience): BELOW_AVERAGE, AVERAGE, ABOVE_AVERAGE
- Quality Score itself is an integer 1-10
- Keywords with no impressions may not have Quality Score data
- To find low Quality Score keywords specifically:

```sql
SELECT
  campaign.name,
  ad_group.name,
  ad_group_criterion.keyword.text,
  ad_group_criterion.keyword.match_type,
  ad_group_criterion.quality_info.quality_score,
  ad_group_criterion.quality_info.creative_quality_score,
  ad_group_criterion.quality_info.search_predicted_ctr,
  ad_group_criterion.quality_info.post_click_quality_score,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions
FROM keyword_view
WHERE segments.date DURING LAST_30_DAYS
  AND ad_group_criterion.quality_info.quality_score < 5
  AND campaign.status = 'ENABLED'
  AND ad_group.status = 'ENABLED'
  AND ad_group_criterion.status = 'ENABLED'
ORDER BY ad_group_criterion.quality_info.quality_score ASC
```

---

## 4. Search Term Report

Actual search queries that triggered ads, with performance metrics.

```sql
SELECT
  campaign.name,
  ad_group.name,
  search_term_view.search_term,
  search_term_view.status,
  segments.keyword.info.text,
  segments.keyword.info.match_type,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value
FROM search_term_view
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
  AND metrics.impressions > 0
ORDER BY metrics.cost_micros DESC
```

**Use in:** Phase 2 — Search term analysis, negative keyword identification

**Notes:**
- `search_term_view.search_term` is the actual query the user typed
- `segments.keyword.info.text` is the keyword that matched
- `search_term_view.status` indicates: ADDED, EXCLUDED, ADDED_EXCLUDED, NONE
- For identifying wasted spend, filter for search terms with cost but zero conversions:

```sql
SELECT
  campaign.name,
  ad_group.name,
  search_term_view.search_term,
  segments.keyword.info.text,
  segments.keyword.info.match_type,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions
FROM search_term_view
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
  AND metrics.cost_micros > 0
  AND metrics.conversions = 0
ORDER BY metrics.cost_micros DESC
LIMIT 50
```

---

## 5. Device Segmentation

Campaign performance broken out by device type.

```sql
SELECT
  campaign.name,
  segments.device,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value,
  metrics.average_cpc,
  metrics.ctr,
  metrics.cost_per_conversion
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
ORDER BY campaign.name ASC, segments.device ASC
```

**Use in:** Phase 3 — Device performance analysis

**Notes:**
- Device values: `DESKTOP`, `MOBILE`, `TABLET`, `CONNECTED_TV`, `OTHER`
- Compare conversion rates across devices to identify bid adjustment opportunities
- If mobile CPA is significantly higher than desktop, consider negative bid adjustments on mobile (or vice versa)

---

## 6. Geographic Performance

Performance by geographic location (user location or location of interest).

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
LIMIT 50
```

**Use in:** Phase 3 — Geographic performance analysis

**Notes:**
- `geographic_view.location_type` differentiates between:
  - `AREA_OF_INTEREST` — user searched for this location
  - `LOCATION_OF_PRESENCE` — user is physically in this location
- For Australian campaigns, a more useful geo breakdown uses the user location report:

```sql
SELECT
  campaign.name,
  campaign_criterion.location.geo_target_constant,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value
FROM location_view
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
ORDER BY metrics.cost_micros DESC
```

- To resolve `geo_target_constant` IDs to location names, use the geo target constant resource:

```sql
SELECT
  geo_target_constant.name,
  geo_target_constant.canonical_name,
  geo_target_constant.country_code,
  geo_target_constant.target_type
FROM geo_target_constant
WHERE geo_target_constant.id = {{CRITERION_ID}}
```

---

## 7. Conversion Action Breakdown

Performance broken out by individual conversion actions configured in the account.

```sql
SELECT
  campaign.name,
  segments.conversion_action_name,
  segments.conversion_action,
  segments.conversion_action_category,
  metrics.conversions,
  metrics.conversions_value,
  metrics.all_conversions,
  metrics.all_conversions_value,
  metrics.cost_micros
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
ORDER BY campaign.name ASC, metrics.conversions DESC
```

**Use in:** Phase 1 — Understanding conversion mix; Phase 3 — CPA by conversion type

**Notes:**
- `metrics.conversions` includes only primary conversion actions
- `metrics.all_conversions` includes both primary and secondary conversion actions
- `segments.conversion_action_category` values include: DEFAULT, PAGE_VIEW, PURCHASE, SIGNUP, LEAD, DOWNLOAD, ADD_TO_CART, BEGIN_CHECKOUT, SUBSCRIBE_PAID, PHONE_CALL_LEAD, IMPORTED_LEAD, SUBMIT_LEAD_FORM, BOOK_APPOINTMENT, REQUEST_QUOTE, GET_DIRECTIONS, OUTBOUND_CLICK, CONTACT, ENGAGEMENT, STORE_VISIT, STORE_SALE
- This query helps identify which conversion actions are driving performance and whether primary vs secondary actions are configured correctly

---

## 8. Landing Page Performance

Performance by final URL (landing page).

```sql
SELECT
  landing_page_view.unexpanded_final_url,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value,
  metrics.average_cpc,
  metrics.mobile_friendly_clicks_percentage,
  metrics.speed_score
FROM landing_page_view
WHERE segments.date DURING LAST_30_DAYS
  AND metrics.clicks > 0
ORDER BY metrics.cost_micros DESC
LIMIT 30
```

**Use in:** Phase 3 — Efficiency Analysis; Phase 5 — Ad Copy and Creative recommendations

**Notes:**
- `landing_page_view.unexpanded_final_url` shows the base URL without query parameters
- `metrics.mobile_friendly_clicks_percentage` indicates the proportion of clicks where the landing page was mobile-friendly
- `metrics.speed_score` is a 1-10 score indicating page load speed
- Landing pages with high spend but low conversion rates are strong optimisation candidates
- Cross-reference with Quality Score landing page experience component

---

## 9. Budget vs Actual Spend

Campaign budget configuration compared to actual spend.

```sql
SELECT
  campaign.name,
  campaign.status,
  campaign_budget.amount_micros,
  campaign_budget.delivery_method,
  campaign_budget.period,
  campaign_budget.total_amount_micros,
  metrics.cost_micros,
  metrics.impressions,
  metrics.clicks,
  metrics.conversions
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
ORDER BY metrics.cost_micros DESC
```

**Use in:** Phase 1 — Budget pacing analysis

**Notes:**
- `campaign_budget.amount_micros` is the daily budget in micros
- `campaign_budget.delivery_method`: STANDARD (spread evenly) or ACCELERATED (spend as fast as possible)
- `campaign_budget.period`: DAILY (default) or custom
- `campaign_budget.total_amount_micros` is set for campaigns with a total budget cap
- To calculate pacing: compare `metrics.cost_micros` (actual spend over period) against `campaign_budget.amount_micros * days_in_period`
- Campaigns spending less than 80% of budget may have targeting or bid issues
- Campaigns consistently hitting budget limits are candidates for budget increases (if CPA is acceptable)

**For a single-day snapshot of budget utilisation:**

```sql
SELECT
  campaign.name,
  campaign_budget.amount_micros,
  metrics.cost_micros
FROM campaign
WHERE segments.date DURING TODAY
  AND campaign.status = 'ENABLED'
ORDER BY metrics.cost_micros DESC
```

---

## 10. Impression Share Analysis

Competitive metrics showing impression share and lost impression share by source.

```sql
SELECT
  campaign.name,
  campaign.advertising_channel_type,
  metrics.impressions,
  metrics.search_impression_share,
  metrics.search_budget_lost_impression_share,
  metrics.search_rank_lost_impression_share,
  metrics.search_exact_match_impression_share,
  metrics.search_top_impression_share,
  metrics.search_absolute_top_impression_share,
  metrics.cost_micros,
  metrics.conversions
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
  AND campaign.advertising_channel_type = 'SEARCH'
ORDER BY metrics.search_budget_lost_impression_share DESC
```

**Use in:** Phase 4 — Competitive Position analysis

**Notes:**
- All impression share metrics are decimals (0.0-1.0):
  - `search_impression_share`: % of eligible impressions you received
  - `search_budget_lost_impression_share`: % lost due to budget constraints
  - `search_rank_lost_impression_share`: % lost due to ad rank (bid + quality)
  - `search_exact_match_impression_share`: IS for exact match keywords only
  - `search_top_impression_share`: % of impressions shown above organic results
  - `search_absolute_top_impression_share`: % of impressions shown as the very first ad
- For Display campaigns, use `content_impression_share`, `content_budget_lost_impression_share`, `content_rank_lost_impression_share` instead
- Campaigns with high `search_budget_lost_impression_share` and low CPA are the strongest candidates for budget increases
- Campaigns with high `search_rank_lost_impression_share` need either higher bids or Quality Score improvements

**To diagnose rank loss — cross-reference with Quality Score:**

```sql
SELECT
  campaign.name,
  ad_group.name,
  ad_group_criterion.keyword.text,
  ad_group_criterion.quality_info.quality_score,
  ad_group_criterion.quality_info.creative_quality_score,
  ad_group_criterion.quality_info.search_predicted_ctr,
  ad_group_criterion.quality_info.post_click_quality_score,
  metrics.average_cpc,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros
FROM keyword_view
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
  AND ad_group.status = 'ENABLED'
  AND ad_group_criterion.status = 'ENABLED'
  AND ad_group_criterion.quality_info.quality_score IS NOT NULL
ORDER BY ad_group_criterion.quality_info.quality_score ASC
LIMIT 30
```

---

## Ad Group Performance

Supplementary query for ad group level breakdown within campaigns.

```sql
SELECT
  campaign.name,
  ad_group.name,
  ad_group.status,
  ad_group.type,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value,
  metrics.average_cpc,
  metrics.ctr,
  metrics.cost_per_conversion
FROM ad_group
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
  AND ad_group.status = 'ENABLED'
ORDER BY metrics.cost_micros DESC
```

**Use in:** Phase 2 — Ad group breakdown within campaigns

---

## Ad Performance (RSA Assets)

Query responsive search ad asset performance to identify top-performing headlines and descriptions.

```sql
SELECT
  campaign.name,
  ad_group.name,
  ad_group_ad.ad.responsive_search_ad.headlines,
  ad_group_ad.ad.responsive_search_ad.descriptions,
  ad_group_ad.ad.final_urls,
  ad_group_ad.ad_strength,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value
FROM ad_group_ad
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
  AND ad_group.status = 'ENABLED'
  AND ad_group_ad.status = 'ENABLED'
  AND ad_group_ad.ad.type = 'RESPONSIVE_SEARCH_AD'
ORDER BY metrics.impressions DESC
```

**Use in:** Phase 5 — Ad Copy and Creative recommendations

**Notes:**
- `ad_group_ad.ad_strength` values: UNSPECIFIED, UNKNOWN, PENDING, NO_ADS, POOR, AVERAGE, GOOD, EXCELLENT
- For individual asset performance, use the `ad_group_ad_asset_view` resource:

```sql
SELECT
  campaign.name,
  ad_group.name,
  ad_group_ad_asset_view.field_type,
  asset.text_asset.text,
  ad_group_ad_asset_view.performance_label
FROM ad_group_ad_asset_view
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
  AND ad_group.status = 'ENABLED'
  AND ad_group_ad_asset_view.field_type IN ('HEADLINE', 'DESCRIPTION')
ORDER BY ad_group_ad_asset_view.performance_label ASC
```

- `performance_label` values: PENDING, LEARNING, LOW, GOOD, BEST
- Assets rated LOW should be replaced; assets rated BEST should be used as models for new copy

---

## Custom Date Range Template

For any of the above queries, replace the `DURING` clause with a custom date range:

```sql
-- Custom date range
WHERE segments.date BETWEEN '2026-01-01' AND '2026-01-31'

-- Last month
WHERE segments.date DURING LAST_MONTH

-- This quarter to date
WHERE segments.date DURING THIS_QUARTER

-- Year to date (custom)
WHERE segments.date BETWEEN '2026-01-01' AND '2026-03-02'
```

---

## Period-over-Period Comparison Pattern

To compare two periods, run any query twice with different date ranges and compare the results:

```
Query 1: WHERE segments.date DURING LAST_30_DAYS       (current period)
Query 2: WHERE segments.date BETWEEN '2026-01-01' AND '2026-01-30'  (previous period)
```

Calculate deltas:
- Absolute change: `current_value - previous_value`
- Percentage change: `(current_value - previous_value) / previous_value * 100`
- For rates (CTR, conversion rate): use percentage point change, not percentage change

---

## Rate Limiting and Pagination

- The MCP server may impose rate limits on queries
- For large accounts, use `LIMIT` and `OFFSET` to paginate results if needed
- Start with `LIMIT 100` for initial analysis and expand if the account has more entities
- When querying with daily segments over long periods, be mindful of result set size (e.g., 30 campaigns * 30 days = 900 rows)
