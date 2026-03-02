# GAQL Query Library

Pre-built Google Ads Query Language (GAQL) queries for use with the `mcp-google-ads` MCP server (`cohnen/mcp-google-ads`). These queries cover the most common analysis tasks referenced throughout MBP:google-ads.

---

## How to Use This Library

### MCP Tool Call

All queries in this library are executed via the MCP tool:

```
Tool: google-ads / search
Parameters:
  customer_id: "1234567890"   (the Google Ads account ID, no dashes)
  query: "<GAQL query>"
```

Copy the GAQL query from the relevant section below, adjust the date range and filters as required, and pass it as the `query` parameter.

### Cost Micros

All monetary values returned by the Google Ads API are in **micros** — the currency amount multiplied by 1,000,000.

```
cost_micros = 12450000000   ->   $12,450.00 AUD
average_cpc = 840000        ->   $0.84 AUD
```

**Always divide by 1,000,000 before presenting monetary values.** The normalised JSON output must use currency values, not micros.

### Date Range Options

GAQL uses the `DURING` clause for predefined date ranges or `BETWEEN` for custom ranges. All queries in this library default to `LAST_30_DAYS`. Replace as needed:

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
| `TODAY` | Today only |
| `YESTERDAY` | Yesterday only |

For custom date ranges:

```sql
WHERE segments.date BETWEEN '2026-01-01' AND '2026-01-31'
```

### Impression Share Values

Impression share metrics are **decimals** between 0.0 and 1.0 (not percentages). A value of `0.65` means 65% impression share.

### Quality Score

Quality Score is a **keyword-level** metric only (integer 1–10). Components are rated: `BELOW_AVERAGE`, `AVERAGE`, or `ABOVE_AVERAGE`.

### Segment Fields

Including a `segments.*` field in the SELECT clause automatically segments all metrics in the response. For example, adding `segments.date` produces one row per entity per day.

### Removed Entities

All queries in this library exclude removed entities by default using status filters (`!= 'REMOVED'` or `= 'ENABLED'`).

---

## 1. Account Summary

**Purpose:** High-level account performance aggregated across all campaigns for the specified period. Use this as the starting point for any analysis to establish baseline metrics.

**MCP tool call:** `google-ads / search`

```sql
SELECT
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.cost_micros,
  metrics.average_cpc,
  metrics.conversions,
  metrics.conversions_value,
  metrics.cost_per_conversion,
  metrics.value_per_conversion
FROM customer
WHERE segments.date DURING LAST_30_DAYS
```

**Use in:** Phase 1 — Account Overview

**Notes:**
- Querying from the `customer` resource returns account-level aggregates (a single row).
- For period-over-period comparison, run this query twice with different date ranges and calculate deltas.
- `metrics.ctr` and `metrics.cost_per_conversion` are pre-calculated by the API — no need to derive them manually.
- To break this down by campaign, use query 1b below.

### 1b. Campaign-Level Overview

**Purpose:** Campaign-level breakdown with spend, impressions, clicks, conversions, and ROAS for the analysis period.

**MCP tool call:** `google-ads / search`

```sql
SELECT
  campaign.name,
  campaign.status,
  campaign.advertising_channel_type,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.cost_micros,
  metrics.average_cpc,
  metrics.conversions,
  metrics.conversions_value,
  metrics.cost_per_conversion,
  campaign.campaign_budget
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status != 'REMOVED'
ORDER BY metrics.cost_micros DESC
```

**Notes:**
- ROAS is calculated downstream: `metrics.conversions_value / (metrics.cost_micros / 1,000,000)`.
- `campaign.advertising_channel_type` values include: `SEARCH`, `DISPLAY`, `SHOPPING`, `VIDEO`, `MULTI_CHANNEL` (Performance Max).
- Change `LAST_30_DAYS` to `LAST_7_DAYS`, `THIS_MONTH`, `LAST_MONTH`, etc. as needed.

---

## 2. Campaign Performance with Daily Segments

**Purpose:** Campaign-level metrics broken out by date for daily trend analysis. Use this to identify sudden spikes, drops, or gradual performance shifts.

**MCP tool call:** `google-ads / search`

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
- Including `segments.date` in SELECT automatically segments all metrics by day — one row per campaign per day.
- For a 30-day period with 10 campaigns, expect up to 300 rows.
- GAQL does not natively support weekly grouping — aggregate daily data downstream if weekly trends are needed.
- Use this data to plot daily trends and flag any day-over-day change exceeding 20% as potentially anomalous.
- For a shorter trend window, change to `LAST_7_DAYS` or `LAST_14_DAYS`.

---

## 3. Ad Group Performance

**Purpose:** Ad group breakdown within campaigns to identify top and bottom performing ad groups and ad groups with spend but zero conversions.

**MCP tool call:** `google-ads / search`

```sql
SELECT
  campaign.name,
  ad_group.name,
  ad_group.status,
  ad_group.type,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.cost_micros,
  metrics.average_cpc,
  metrics.conversions,
  metrics.conversions_value,
  metrics.cost_per_conversion
FROM ad_group
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
  AND ad_group.status = 'ENABLED'
ORDER BY metrics.cost_micros DESC
```

**Use in:** Phase 2 — Ad group breakdown within campaigns

**Notes:**
- `ad_group.type` values include: `SEARCH_STANDARD`, `DISPLAY_STANDARD`, `SHOPPING_PRODUCT_ADS`, `VIDEO_BUMPER`, and others.
- To find ad groups with spend but zero conversions, filter results downstream where `metrics.cost_micros > 0` and `metrics.conversions = 0`.
- Sort by `metrics.cost_per_conversion ASC` to find the most efficient ad groups for potential budget increases.

---

## 4. Keyword Performance with Quality Score

**Purpose:** Keyword-level metrics including Quality Score and its component ratings. Use this for Quality Score distribution analysis, identifying low-QS keywords, and finding high-performing keywords.

**MCP tool call:** `google-ads / search`

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
  metrics.ctr,
  metrics.cost_micros,
  metrics.average_cpc,
  metrics.conversions,
  metrics.conversions_value,
  metrics.cost_per_conversion
FROM keyword_view
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
  AND ad_group.status = 'ENABLED'
  AND ad_group_criterion.status = 'ENABLED'
ORDER BY metrics.cost_micros DESC
```

**Use in:** Phase 2 — Top keywords, Quality Score distribution

**Notes:**
- Quality Score components:
  - `creative_quality_score` = Ad Relevance: `BELOW_AVERAGE`, `AVERAGE`, `ABOVE_AVERAGE`
  - `search_predicted_ctr` = Expected CTR: `BELOW_AVERAGE`, `AVERAGE`, `ABOVE_AVERAGE`
  - `post_click_quality_score` = Landing Page Experience: `BELOW_AVERAGE`, `AVERAGE`, `ABOVE_AVERAGE`
- Quality Score itself is an integer 1–10.
- Keywords with no impressions may not have Quality Score data.
- `ad_group_criterion.keyword.match_type` values: `EXACT`, `PHRASE`, `BROAD`.

### 4b. Low Quality Score Keywords

**Purpose:** Identify keywords with Quality Score below 5 that are dragging down campaign efficiency and ad rank.

**MCP tool call:** `google-ads / search`

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

**Notes:**
- Keywords with QS 1–3 are strong candidates for pausing, rewriting ad copy, or improving landing pages.
- Cross-reference component ratings to determine the root cause: ad relevance, expected CTR, or landing page experience.
- Keywords with QS < 5 that also have zero conversions should be flagged in the wasted spend analysis.

---

## 5. Search Term Report

**Purpose:** Actual search queries typed by users that triggered your ads. Use this to identify irrelevant search terms consuming budget, find high-performing terms to add as keywords, and build negative keyword lists.

**MCP tool call:** `google-ads / search`

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
  metrics.ctr,
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
- `search_term_view.search_term` is the actual query the user typed.
- `segments.keyword.info.text` is the keyword that matched.
- `search_term_view.status` values: `ADDED` (already a keyword), `EXCLUDED` (already a negative), `ADDED_EXCLUDED`, `NONE` (not yet added or excluded).
- Focus on terms with status `NONE` — these are the ones needing action.
- For large accounts, add `LIMIT 100` to keep result sets manageable.

### 5b. Wasted Search Terms (Cost, No Conversions)

**Purpose:** Identify search terms that are consuming budget without generating any conversions — prime candidates for negative keywords.

**MCP tool call:** `google-ads / search`

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

**Notes:**
- Sum the `cost_micros` column (divided by 1,000,000) to quantify total wasted spend on non-converting search terms.
- Group results by theme to build negative keyword lists (e.g., all "free"-related terms, all "jobs"-related terms).

---

## 6. Device Segmentation

**Purpose:** Campaign performance broken out by device type (desktop, mobile, tablet) to identify device-level bid adjustment opportunities.

**MCP tool call:** `google-ads / search`

```sql
SELECT
  campaign.name,
  segments.device,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.cost_micros,
  metrics.average_cpc,
  metrics.conversions,
  metrics.conversions_value,
  metrics.cost_per_conversion
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
ORDER BY campaign.name ASC, segments.device ASC
```

**Use in:** Phase 3 — Device performance analysis

**Notes:**
- Device values: `DESKTOP`, `MOBILE`, `TABLET`, `CONNECTED_TV`, `OTHER`.
- Compare conversion rates and CPA across devices within each campaign.
- If mobile CPA is significantly higher than desktop (e.g., 2x+), consider a negative bid adjustment on mobile.
- If mobile has a stronger conversion rate, consider increasing mobile bid adjustments.
- To see account-wide device breakdown, query from `customer` instead of `campaign` and include `segments.device`.

---

## 7. Geographic Performance

**Purpose:** Performance by geographic location to identify high-performing and underperforming regions. Use this for location bid adjustments and exclusion recommendations.

**MCP tool call:** `google-ads / search`

### 7a. Geographic View (User Location and Area of Interest)

```sql
SELECT
  campaign.name,
  geographic_view.country_criterion_id,
  geographic_view.location_type,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
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
- For Australian campaigns, filter for `LOCATION_OF_PRESENCE` to get the most accurate geographic breakdown.

### 7b. Location View (Targeted Locations)

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

**Notes:**
- This shows performance for explicitly targeted locations (set in campaign location targeting).
- To resolve `geo_target_constant` IDs to location names, query the `geo_target_constant` resource:

```sql
SELECT
  geo_target_constant.name,
  geo_target_constant.canonical_name,
  geo_target_constant.country_code,
  geo_target_constant.target_type
FROM geo_target_constant
WHERE geo_target_constant.id = {{CRITERION_ID}}
```

- `target_type` values include: `Country`, `State`, `City`, `Postal Code`, etc.
- Australian state-level criterion IDs for reference: NSW (20034), VIC (20035), QLD (20036), WA (20037), SA (20038), TAS (20039), ACT (20040), NT (20041).

---

## 8. Impression Share Analysis

**Purpose:** Competitive metrics showing what percentage of eligible impressions you are receiving and why the rest are being lost (budget vs rank). Critical for diagnosing competitiveness.

**MCP tool call:** `google-ads / search`

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
- All impression share metrics are decimals (0.0–1.0):
  - `search_impression_share`: % of eligible impressions you received
  - `search_budget_lost_impression_share`: % lost due to budget constraints
  - `search_rank_lost_impression_share`: % lost due to ad rank (bid + quality)
  - `search_exact_match_impression_share`: IS for exact match keywords only
  - `search_top_impression_share`: % of impressions shown above organic results
  - `search_absolute_top_impression_share`: % of impressions shown as the very first ad
- For Display campaigns, use `content_impression_share`, `content_budget_lost_impression_share`, `content_rank_lost_impression_share` instead.
- Campaigns with `search_budget_lost_impression_share > 0.10` and low CPA are the strongest candidates for budget increases.
- Campaigns with `search_rank_lost_impression_share > 0.20` need either higher bids or Quality Score improvements.

### 8b. Impression Share with Quality Score Cross-Reference

**Purpose:** Diagnose whether rank-based impression loss is due to low bids or poor Quality Scores.

**MCP tool call:** `google-ads / search`

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

**Notes:**
- If the lowest-QS keywords belong to campaigns with high `search_rank_lost_impression_share`, the rank loss is primarily quality-driven.
- If QS is generally acceptable (6+) but rank loss is still high, the issue is likely bid-related.

---

## 9. Ad Performance (RSA Assets)

**Purpose:** Evaluate Responsive Search Ad (RSA) performance including ad strength scores, and identify top-performing and underperforming headlines and descriptions.

**MCP tool call:** `google-ads / search`

### 9a. RSA-Level Performance

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
  metrics.ctr,
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
- `ad_group_ad.ad_strength` values: `UNSPECIFIED`, `UNKNOWN`, `PENDING`, `NO_ADS`, `POOR`, `AVERAGE`, `GOOD`, `EXCELLENT`.
- Ads with `POOR` ad strength should be prioritised for improvement.
- Headlines and descriptions are returned as arrays of text assets with pinning information.

### 9b. Individual Asset Performance

**Purpose:** See how each individual headline and description is performing within RSAs.

**MCP tool call:** `google-ads / search`

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

**Notes:**
- `performance_label` values: `PENDING`, `LEARNING`, `LOW`, `GOOD`, `BEST`.
- Assets rated `LOW` should be replaced with new variations.
- Assets rated `BEST` should be used as models for new copy across other ad groups.
- Assets in `PENDING` or `LEARNING` need more impressions before a performance verdict can be made.

---

## 10. Conversion Action Breakdown

**Purpose:** Performance broken out by individual conversion actions configured in the account. Use this to understand the conversion mix, verify primary vs secondary action configuration, and calculate CPA by conversion type.

**MCP tool call:** `google-ads / search`

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
- `metrics.conversions` includes only **primary** conversion actions (those marked "Include in Conversions").
- `metrics.all_conversions` includes **both** primary and secondary conversion actions.
- `segments.conversion_action_category` values include: `DEFAULT`, `PAGE_VIEW`, `PURCHASE`, `SIGNUP`, `LEAD`, `DOWNLOAD`, `ADD_TO_CART`, `BEGIN_CHECKOUT`, `SUBSCRIBE_PAID`, `PHONE_CALL_LEAD`, `IMPORTED_LEAD`, `SUBMIT_LEAD_FORM`, `BOOK_APPOINTMENT`, `REQUEST_QUOTE`, `GET_DIRECTIONS`, `OUTBOUND_CLICK`, `CONTACT`, `ENGAGEMENT`, `STORE_VISIT`, `STORE_SALE`.
- If `metrics.all_conversions` is significantly higher than `metrics.conversions`, investigate whether secondary actions should be promoted to primary (or vice versa).

---

## 11. Budget Pacing

**Purpose:** Compare campaign budget configuration against actual spend to identify budget-limited campaigns (underspending opportunities) and campaigns that are consistently exhausting their budget.

**MCP tool call:** `google-ads / search`

### 11a. Budget vs Actual Spend (Period)

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
- `campaign_budget.amount_micros` is the daily budget in micros (divide by 1,000,000 for currency).
- `campaign_budget.delivery_method`: `STANDARD` (spread evenly) or `ACCELERATED` (spend as fast as possible).
- `campaign_budget.period`: `DAILY` (default) or custom.
- `campaign_budget.total_amount_micros` is set for campaigns with a total budget cap.
- **Pacing calculation:** compare `metrics.cost_micros` (actual spend over period) against `campaign_budget.amount_micros * days_in_period`.
- Campaigns spending **less than 80%** of budget may have targeting, bid, or ad approval issues.
- Campaigns consistently hitting budget limits are candidates for budget increases (if CPA is acceptable).

### 11b. Single-Day Budget Utilisation

**Purpose:** Snapshot of today's budget utilisation to see which campaigns have spent their daily budget.

**MCP tool call:** `google-ads / search`

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

**Notes:**
- Run this mid-afternoon to assess whether campaigns are on track to exhaust their daily budget.
- Campaigns where `metrics.cost_micros` is already close to `campaign_budget.amount_micros` by midday are strongly budget-constrained.

---

## 12. Zero Conversion Keywords (Wasted Spend)

**Purpose:** Identify keywords that have accrued spend but generated zero conversions over the analysis period. These represent the clearest wasted spend and are candidates for pausing, match type changes, or landing page improvements.

**MCP tool call:** `google-ads / search`

```sql
SELECT
  campaign.name,
  ad_group.name,
  ad_group_criterion.keyword.text,
  ad_group_criterion.keyword.match_type,
  ad_group_criterion.quality_info.quality_score,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.cost_micros,
  metrics.average_cpc,
  metrics.conversions
FROM keyword_view
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
  AND ad_group.status = 'ENABLED'
  AND ad_group_criterion.status = 'ENABLED'
  AND metrics.cost_micros > 0
  AND metrics.conversions = 0
ORDER BY metrics.cost_micros DESC
LIMIT 50
```

**Use in:** Phase 3 — Wasted Spend Identification

**Notes:**
- Sum the `cost_micros` column (divided by 1,000,000) to quantify total wasted spend on non-converting keywords.
- Cross-reference Quality Score: keywords with zero conversions AND QS below 5 are the strongest candidates for pausing.
- Keywords with zero conversions but high CTR may have a landing page issue rather than a keyword relevance issue.
- For a more conservative view, extend the date range to `LAST_90_DAYS` — keywords with zero conversions over 90 days are more confidently "wasted".
- Consider match type: broad match keywords with zero conversions may be matching to irrelevant search terms (check query 5 — Search Term Report).

### 12b. Zero Conversion Keywords with Significant Spend

**Purpose:** Narrower view focusing only on keywords where wasted spend exceeds a meaningful threshold (e.g., cost exceeds the account's average CPA).

**MCP tool call:** `google-ads / search`

```sql
SELECT
  campaign.name,
  ad_group.name,
  ad_group_criterion.keyword.text,
  ad_group_criterion.keyword.match_type,
  ad_group_criterion.quality_info.quality_score,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions
FROM keyword_view
WHERE segments.date DURING LAST_90_DAYS
  AND campaign.status = 'ENABLED'
  AND ad_group.status = 'ENABLED'
  AND ad_group_criterion.status = 'ENABLED'
  AND metrics.cost_micros > 0
  AND metrics.conversions = 0
ORDER BY metrics.cost_micros DESC
LIMIT 25
```

**Notes:**
- Using `LAST_90_DAYS` gives a larger sample for more confident wasted spend identification.
- After retrieving results, filter downstream for keywords where spend exceeds the account's average CPA (from query 1). If a keyword has spent more than one CPA's worth without converting, it is definitively underperforming.

---

## 13. Top Performing Keywords

**Purpose:** Identify the highest-performing keywords by ROAS (or conversion rate) to find scaling opportunities and model successful keyword strategies.

**MCP tool call:** `google-ads / search`

### 13a. Top Keywords by ROAS

```sql
SELECT
  campaign.name,
  ad_group.name,
  ad_group_criterion.keyword.text,
  ad_group_criterion.keyword.match_type,
  ad_group_criterion.quality_info.quality_score,
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
  AND metrics.conversions > 0
ORDER BY metrics.conversions_value DESC
LIMIT 25
```

**Use in:** Phase 2 — Top keywords; Phase 5 — Keyword optimisation recommendations

**Notes:**
- ROAS is calculated downstream: `metrics.conversions_value / (metrics.cost_micros / 1,000,000)`.
- GAQL does not support calculated fields in ORDER BY, so we sort by `conversions_value DESC` as a proxy. Filter and re-sort downstream for true ROAS ranking.
- Top ROAS keywords that are budget-constrained (belonging to campaigns with high `search_budget_lost_impression_share`) are prime candidates for increased investment.
- Check if these keywords are exact match — if they are phrase or broad, consider adding the exact match variant for tighter control.

### 13b. Top Keywords by Conversion Rate

```sql
SELECT
  campaign.name,
  ad_group.name,
  ad_group_criterion.keyword.text,
  ad_group_criterion.keyword.match_type,
  ad_group_criterion.quality_info.quality_score,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value,
  metrics.cost_per_conversion
FROM keyword_view
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
  AND ad_group.status = 'ENABLED'
  AND ad_group_criterion.status = 'ENABLED'
  AND metrics.clicks > 10
  AND metrics.conversions > 0
ORDER BY metrics.cost_per_conversion ASC
LIMIT 25
```

**Notes:**
- The `metrics.clicks > 10` filter ensures we only surface keywords with enough data to be statistically meaningful.
- Sorting by `cost_per_conversion ASC` surfaces the most efficient keywords first.
- Conversion rate is calculated downstream: `metrics.conversions / metrics.clicks`.
- Keywords with high conversion rates but low impression volume may benefit from bid increases to capture more traffic.

---

## 14. Change History

**Purpose:** Review recent changes made to the account (campaigns, ad groups, ads, keywords, bids, budgets) to understand what has been modified and correlate changes with performance shifts.

**MCP tool call:** `google-ads / search`

### 14a. Recent Campaign and Ad Group Changes

```sql
SELECT
  change_status.resource_name,
  change_status.resource_type,
  change_status.resource_status,
  change_status.last_change_date_time,
  campaign.name,
  ad_group.name
FROM change_status
WHERE change_status.last_change_date_time DURING LAST_14_DAYS
  AND change_status.resource_type IN (
    'CAMPAIGN',
    'AD_GROUP',
    'AD_GROUP_AD',
    'AD_GROUP_CRITERION',
    'CAMPAIGN_CRITERION',
    'CAMPAIGN_BUDGET'
  )
ORDER BY change_status.last_change_date_time DESC
LIMIT 50
```

**Use in:** Phase 2 — Correlating performance changes with account modifications; Phase 5 — Context for recommendations

**Notes:**
- `change_status.resource_type` values include: `AD_GROUP`, `AD_GROUP_AD`, `AD_GROUP_CRITERION`, `CAMPAIGN`, `CAMPAIGN_CRITERION`, `CAMPAIGN_BUDGET`, `AD_GROUP_BID_MODIFIER`, `FEED`, `FEED_ITEM`, and others.
- `change_status.resource_status` values: `ENABLED`, `PAUSED`, `REMOVED`.
- `change_status.last_change_date_time` is a timestamp — use this to correlate with performance spikes or drops observed in query 2 (daily trends).
- Change history is limited to the last 90 days in the Google Ads API.
- For large accounts with frequent changes, narrow the date range to `LAST_7_DAYS` or filter to specific resource types.

### 14b. Change Events (Detailed)

```sql
SELECT
  change_event.change_date_time,
  change_event.change_resource_type,
  change_event.change_resource_name,
  change_event.user_email,
  change_event.client_type,
  change_event.old_resource,
  change_event.new_resource,
  change_event.resource_change_operation,
  campaign.name,
  ad_group.name
FROM change_event
WHERE change_event.change_date_time DURING LAST_14_DAYS
  AND change_event.change_resource_type IN (
    'CAMPAIGN',
    'AD_GROUP',
    'AD_GROUP_AD',
    'AD_GROUP_CRITERION',
    'CAMPAIGN_BUDGET'
  )
ORDER BY change_event.change_date_time DESC
LIMIT 50
```

**Notes:**
- `change_event` provides more detail than `change_status`, including the user who made the change and the old/new resource values.
- `change_event.client_type` values: `GOOGLE_ADS_WEB_CLIENT`, `GOOGLE_ADS_AUTOMATED_RULE`, `GOOGLE_ADS_SCRIPTS`, `GOOGLE_ADS_BULK_UPLOAD`, `GOOGLE_ADS_API`, `GOOGLE_ADS_EDITOR`, `GOOGLE_ADS_MOBILE_APP`, `GOOGLE_ADS_RECOMMENDATIONS`, `SEARCH_ADS_360`, and others.
- This is particularly useful for identifying automated changes (rules, scripts, Smart Bidding adjustments) vs manual changes.
- `resource_change_operation` values: `CREATE`, `UPDATE`, `REMOVE`.
- The `change_event` resource may not be available in all API versions — fall back to `change_status` if unavailable.

---

## Supplementary Queries

### Landing Page Performance

**Purpose:** Performance by final URL (landing page) to identify pages with high spend but low conversion rates.

**MCP tool call:** `google-ads / search`

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

**Notes:**
- `landing_page_view.unexpanded_final_url` shows the base URL without query parameters.
- `metrics.mobile_friendly_clicks_percentage` indicates the proportion of clicks where the landing page was deemed mobile-friendly.
- `metrics.speed_score` is a 1–10 score indicating page load speed.
- Landing pages with high spend but low conversion rates are strong optimisation candidates.
- Cross-reference with Quality Score landing page experience component from query 4.

---

## Utility Patterns

### Period-over-Period Comparison

To compare two periods, run any query twice with different date ranges and calculate deltas:

```
Query 1: WHERE segments.date DURING LAST_30_DAYS         (current period)
Query 2: WHERE segments.date DURING LAST_MONTH            (previous period)
```

Or with custom ranges:

```
Query 1: WHERE segments.date BETWEEN '2026-02-01' AND '2026-02-28'   (current)
Query 2: WHERE segments.date BETWEEN '2026-01-01' AND '2026-01-31'   (previous)
```

Calculate deltas:
- **Absolute change:** `current_value - previous_value`
- **Percentage change:** `(current_value - previous_value) / previous_value * 100`
- **For rates** (CTR, conversion rate): use percentage point change, not percentage change

### Custom Date Range Template

For any query in this library, replace the `DURING` clause:

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

### Rate Limiting and Pagination

- The MCP server may impose rate limits on queries.
- For large accounts, use `LIMIT` and `OFFSET` to paginate results if needed.
- Start with `LIMIT 100` for initial analysis and expand if the account has more entities.
- When querying with daily segments over long periods, be mindful of result set size (e.g., 30 campaigns x 30 days = 900 rows).

---

## Quick Reference: Query to Analysis Phase Mapping

| # | Query | Analysis Phase | SKILL.md Section |
|---|---|---|---|
| 1 | Account Summary | Phase 1 — Account Overview | Phase 1: Account Overview |
| 1b | Campaign-Level Overview | Phase 1 — Account Overview | Phase 1: Campaign-level breakdown |
| 2 | Campaign Performance with Daily Segments | Phase 2 — Campaign Deep-Dive | Phase 2a: Performance Trend |
| 3 | Ad Group Performance | Phase 2 — Campaign Deep-Dive | Phase 2b: Ad Group Breakdown |
| 4 | Keyword Performance with Quality Score | Phase 2 — Campaign Deep-Dive | Phase 2c/2e: Keywords and Quality Score |
| 4b | Low Quality Score Keywords | Phase 2 — Campaign Deep-Dive | Phase 2e: Quality Score Distribution |
| 5 | Search Term Report | Phase 2 — Campaign Deep-Dive | Phase 2d: Search Term Analysis |
| 5b | Wasted Search Terms | Phase 3 — Efficiency Analysis | Phase 3c: Wasted Spend Identification |
| 6 | Device Segmentation | Phase 3 — Efficiency Analysis | Phase 3e: Device Performance |
| 7 | Geographic Performance | Phase 3 — Efficiency Analysis | Phase 3f: Geographic Performance |
| 8 | Impression Share Analysis | Phase 4 — Competitive Position | Phase 4a: Impression Share Analysis |
| 8b | Impression Share + Quality Score | Phase 4 — Competitive Position | Phase 4c: Rank-Constrained Campaigns |
| 9 | Ad Performance (RSA Assets) | Phase 5 — Strategic Recommendations | Phase 5c: Ad Copy and Creative |
| 9b | Individual Asset Performance | Phase 5 — Strategic Recommendations | Phase 5c: Ad Copy and Creative |
| 10 | Conversion Action Breakdown | Phase 1 / Phase 3 | Phase 1 and Phase 3a |
| 11 | Budget Pacing | Phase 1 — Account Overview | Phase 1: Budget pacing |
| 11b | Single-Day Budget Utilisation | Phase 1 — Account Overview | Phase 1: Budget pacing |
| 12 | Zero Conversion Keywords | Phase 3 — Efficiency Analysis | Phase 3c: Wasted Spend Identification |
| 12b | Zero Conv. Keywords (Significant Spend) | Phase 3 — Efficiency Analysis | Phase 3c: Wasted Spend Identification |
| 13 | Top Keywords by ROAS | Phase 2 / Phase 5 | Phase 2c and Phase 5b |
| 13b | Top Keywords by Conversion Rate | Phase 2 / Phase 5 | Phase 2c and Phase 5b |
| 14 | Change History (Status) | Phase 2 / Phase 5 | Phase 2a and context |
| 14b | Change History (Events) | Phase 2 / Phase 5 | Phase 2a and context |
