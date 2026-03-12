---
name: report
description: Generate analytics summary report from the database. Query key metrics, trends, and produce formatted output.
arguments:
  - name: period
    description: Time period - '7d', '30d', '90d', or 'ytd'
    required: false
---

# Analytics Report

Generate a comprehensive analytics report from the Website Analytics database.

## Report Queries

### Traffic Summary (Last 30 Days)
```bash
sqlite3 -header -column "/Users/sasreliability/Documents/Repos/Website Analytics/website_analytics.db" "
SELECT
  SUM(\"Total Users\") as 'Total Users',
  SUM(\"New Users\") as 'New Users',
  SUM(\"Sessions\") as 'Sessions',
  ROUND(AVG(\"Engagement Rate\") * 100, 1) || '%' as 'Avg Engagement',
  ROUND(AVG(\"Bounce Rate\") * 100, 1) || '%' as 'Avg Bounce Rate',
  ROUND(AVG(\"Average Session Duration (secs)\"), 0) || 's' as 'Avg Duration'
FROM user_data
WHERE Date >= date('now', '-30 days');
"
```

### Top Traffic Sources
```bash
sqlite3 -header -column "/Users/sasreliability/Documents/Repos/Website Analytics/website_analytics.db" "
SELECT
  Source,
  SUM(\"Total Users\") as Users,
  ROUND(AVG(\"Engagement Rate\") * 100, 1) || '%' as 'Engagement'
FROM user_data
WHERE Date >= date('now', '-30 days') AND Source IS NOT NULL
GROUP BY Source
ORDER BY Users DESC
LIMIT 10;
"
```

### Top Pages by Views
```bash
sqlite3 -header -column "/Users/sasreliability/Documents/Repos/Website Analytics/website_analytics.db" "
SELECT
  \"Page Title\",
  SUM(\"Page Views\") as Views,
  COUNT(DISTINCT DATE(Date)) as Days
FROM page_data
WHERE Date >= date('now', '-30 days')
GROUP BY \"Page Title\"
ORDER BY Views DESC
LIMIT 10;
"
```

### Search Performance
```bash
sqlite3 -header -column "/Users/sasreliability/Documents/Repos/Website Analytics/website_analytics.db" "
SELECT
  SUM(Clicks) as 'Total Clicks',
  SUM(Impressions) as 'Total Impressions',
  ROUND(SUM(Clicks) * 100.0 / SUM(Impressions), 2) || '%' as 'CTR',
  ROUND(AVG(Position), 1) as 'Avg Position'
FROM console_data
WHERE Date >= date('now', '-30 days');
"
```

### Top Search Queries
```bash
sqlite3 -header -column "/Users/sasreliability/Documents/Repos/Website Analytics/website_analytics.db" "
SELECT
  Query,
  SUM(Clicks) as Clicks,
  SUM(Impressions) as Impressions,
  ROUND(AVG(Position), 1) as 'Avg Pos'
FROM console_data
WHERE Date >= date('now', '-30 days') AND Query IS NOT NULL
GROUP BY Query
ORDER BY Clicks DESC
LIMIT 15;
"
```

### Device Breakdown
```bash
sqlite3 -header -column "/Users/sasreliability/Documents/Repos/Website Analytics/website_analytics.db" "
SELECT
  \"Device Category\",
  SUM(\"Total Users\") as Users,
  ROUND(SUM(\"Total Users\") * 100.0 / (SELECT SUM(\"Total Users\") FROM user_data WHERE Date >= date('now', '-30 days')), 1) || '%' as 'Share'
FROM user_data
WHERE Date >= date('now', '-30 days') AND \"Device Category\" IS NOT NULL
GROUP BY \"Device Category\"
ORDER BY Users DESC;
"
```

### Geographic Distribution
```bash
sqlite3 -header -column "/Users/sasreliability/Documents/Repos/Website Analytics/website_analytics.db" "
SELECT
  Country,
  SUM(\"Total Users\") as Users
FROM user_data
WHERE Date >= date('now', '-30 days') AND Country IS NOT NULL AND Country != ''
GROUP BY Country
ORDER BY Users DESC
LIMIT 10;
"
```

## Output Format

Present the report with clear sections:
1. **Executive Summary** - Key metrics at a glance
2. **Traffic Analysis** - Sources, trends, geography
3. **Content Performance** - Top pages, engagement
4. **Search Visibility** - Rankings, CTR, top queries
5. **Recommendations** - Actionable insights
