---
name: campaigns
description: View campaign performance metrics for LinkedIn and Google Ads, including UTM parameter breakdown.
---

# Campaign Performance

Analyse marketing campaign performance using UTM-tagged traffic data.

## Campaign Analysis Queries

### All Campaigns Summary
```bash
sqlite3 -header -column "/Users/sasreliability/Documents/Repos/Website Analytics/website_analytics.db" "
SELECT
  Campaign,
  Source,
  Medium,
  SUM(\"Total Users\") as Users,
  SUM(Sessions) as Sessions,
  ROUND(AVG(\"Engagement Rate\") * 100, 1) || '%' as 'Engagement',
  ROUND(AVG(\"Bounce Rate\") * 100, 1) || '%' as 'Bounce Rate'
FROM user_data
WHERE Date >= date('now', '-30 days')
  AND Campaign IS NOT NULL
  AND Campaign != ''
  AND Campaign != '(not set)'
GROUP BY Campaign, Source, Medium
ORDER BY Users DESC
LIMIT 20;
"
```

### Traffic by Source/Medium
```bash
sqlite3 -header -column "/Users/sasreliability/Documents/Repos/Website Analytics/website_analytics.db" "
SELECT
  Source || ' / ' || Medium as 'Source / Medium',
  SUM(\"Total Users\") as Users,
  ROUND(SUM(\"Total Users\") * 100.0 / (SELECT SUM(\"Total Users\") FROM user_data WHERE Date >= date('now', '-30 days')), 1) || '%' as Share,
  ROUND(AVG(\"Engagement Rate\") * 100, 1) || '%' as 'Engagement'
FROM user_data
WHERE Date >= date('now', '-30 days')
GROUP BY Source, Medium
ORDER BY Users DESC
LIMIT 15;
"
```

### LinkedIn Campaign Performance
```bash
sqlite3 -header -column "/Users/sasreliability/Documents/Repos/Website Analytics/website_analytics.db" "
SELECT
  Campaign,
  SUM(\"Total Users\") as Users,
  SUM(Sessions) as Sessions,
  ROUND(AVG(\"Engagement Rate\") * 100, 1) || '%' as 'Engagement',
  ROUND(AVG(\"Average Session Duration (secs)\"), 0) || 's' as 'Avg Duration'
FROM user_data
WHERE Date >= date('now', '-30 days')
  AND (Source LIKE '%linkedin%' OR Medium LIKE '%social%')
  AND Campaign IS NOT NULL
  AND Campaign != ''
GROUP BY Campaign
ORDER BY Users DESC;
"
```

### Google Ads Performance
```bash
sqlite3 -header -column "/Users/sasreliability/Documents/Repos/Website Analytics/website_analytics.db" "
SELECT
  Campaign,
  SUM(\"Total Users\") as Users,
  SUM(Sessions) as Sessions,
  ROUND(AVG(\"Engagement Rate\") * 100, 1) || '%' as 'Engagement',
  ROUND(AVG(\"Bounce Rate\") * 100, 1) || '%' as 'Bounce Rate'
FROM user_data
WHERE Date >= date('now', '-30 days')
  AND (Source = 'google' AND Medium IN ('cpc', 'ppc', 'paid'))
  AND Campaign IS NOT NULL
GROUP BY Campaign
ORDER BY Users DESC;
"
```

### Organic vs Paid Comparison
```bash
sqlite3 -header -column "/Users/sasreliability/Documents/Repos/Website Analytics/website_analytics.db" "
SELECT
  CASE
    WHEN Medium IN ('cpc', 'ppc', 'paid', 'paid_social', 'display') THEN 'Paid'
    WHEN Medium IN ('organic', 'referral') THEN 'Organic'
    WHEN Medium = '(none)' THEN 'Direct'
    ELSE 'Other'
  END as Channel,
  SUM(\"Total Users\") as Users,
  ROUND(AVG(\"Engagement Rate\") * 100, 1) || '%' as 'Engagement',
  ROUND(AVG(\"Bounce Rate\") * 100, 1) || '%' as 'Bounce Rate'
FROM user_data
WHERE Date >= date('now', '-30 days')
GROUP BY Channel
ORDER BY Users DESC;
"
```

### Campaign Trend Over Time
```bash
sqlite3 -header -column "/Users/sasreliability/Documents/Repos/Website Analytics/website_analytics.db" "
SELECT
  strftime('%Y-%W', Date) as Week,
  SUM(CASE WHEN Medium IN ('cpc', 'ppc', 'paid', 'paid_social') THEN \"Total Users\" ELSE 0 END) as 'Paid Users',
  SUM(CASE WHEN Medium = 'organic' THEN \"Total Users\" ELSE 0 END) as 'Organic Users',
  SUM(CASE WHEN Source = 'linkedin' THEN \"Total Users\" ELSE 0 END) as 'LinkedIn Users'
FROM user_data
WHERE Date >= date('now', '-90 days')
GROUP BY strftime('%Y-%W', Date)
ORDER BY Week DESC;
"
```

## UTM Parameter Reference

Ensure campaigns use consistent UTM tagging:

| Parameter | Description | Example Values |
|-----------|-------------|----------------|
| `utm_source` | Traffic origin | `google`, `linkedin`, `newsletter` |
| `utm_medium` | Marketing medium | `cpc`, `paid_social`, `email`, `organic` |
| `utm_campaign` | Campaign name | `brand-awareness-q1`, `retargeting-mar` |
| `utm_content` | Ad/creative variant | `banner-v1`, `carousel-a` |
| `utm_term` | Paid keyword | `asset management software` |

## Dashboard Link

For visual campaign analysis:
```bash
open http://localhost:8000/d/campaign-performance
```
