---
name: seo
description: Run SEO keyword analysis using Google Trends data. Analyse keyword performance, correlations, and competitor rankings.
---

# SEO Analysis

Analyse search performance and keyword opportunities using Search Console data.

## Analysis Queries

### Top Performing Keywords
```bash
sqlite3 -header -column "/Users/sasreliability/Documents/Repos/Website Analytics/website_analytics.db" "
SELECT
  Query as Keyword,
  SUM(Clicks) as Clicks,
  SUM(Impressions) as Impressions,
  ROUND(SUM(Clicks) * 100.0 / SUM(Impressions), 2) as 'CTR %',
  ROUND(AVG(Position), 1) as 'Avg Position'
FROM console_data
WHERE Date >= date('now', '-30 days')
  AND Query IS NOT NULL
  AND Query != ''
GROUP BY Query
HAVING SUM(Impressions) > 10
ORDER BY Clicks DESC
LIMIT 20;
"
```

### High Impression / Low Click Keywords (Opportunities)
```bash
sqlite3 -header -column "/Users/sasreliability/Documents/Repos/Website Analytics/website_analytics.db" "
SELECT
  Query as Keyword,
  SUM(Impressions) as Impressions,
  SUM(Clicks) as Clicks,
  ROUND(SUM(Clicks) * 100.0 / SUM(Impressions), 2) as 'CTR %',
  ROUND(AVG(Position), 1) as 'Avg Position'
FROM console_data
WHERE Date >= date('now', '-30 days')
  AND Query IS NOT NULL
  AND Position <= 20
  AND Query != ''
GROUP BY Query
HAVING SUM(Impressions) > 50 AND SUM(Clicks) < 5
ORDER BY Impressions DESC
LIMIT 15;
"
```

These are keywords with visibility but low clicks - prime candidates for meta title/description optimisation.

### Position 4-10 Keywords (Quick Wins)
```bash
sqlite3 -header -column "/Users/sasreliability/Documents/Repos/Website Analytics/website_analytics.db" "
SELECT
  Query as Keyword,
  ROUND(AVG(Position), 1) as 'Avg Position',
  SUM(Impressions) as Impressions,
  SUM(Clicks) as Clicks
FROM console_data
WHERE Date >= date('now', '-30 days')
  AND Query IS NOT NULL
  AND Query != ''
GROUP BY Query
HAVING AVG(Position) BETWEEN 4 AND 10 AND SUM(Impressions) > 30
ORDER BY Impressions DESC
LIMIT 15;
"
```

These keywords are close to page 1 top positions - small ranking improvements yield big traffic gains.

### Top Landing Pages by Search Traffic
```bash
sqlite3 -header -column "/Users/sasreliability/Documents/Repos/Website Analytics/website_analytics.db" "
SELECT
  Page,
  SUM(Clicks) as Clicks,
  SUM(Impressions) as Impressions,
  ROUND(SUM(Clicks) * 100.0 / SUM(Impressions), 2) as 'CTR %',
  COUNT(DISTINCT Query) as 'Unique Keywords'
FROM console_data
WHERE Date >= date('now', '-30 days')
GROUP BY Page
ORDER BY Clicks DESC
LIMIT 15;
"
```

### Search Trends Over Time
```bash
sqlite3 -header -column "/Users/sasreliability/Documents/Repos/Website Analytics/website_analytics.db" "
SELECT
  strftime('%Y-%W', Date) as Week,
  SUM(Clicks) as Clicks,
  SUM(Impressions) as Impressions,
  ROUND(AVG(Position), 1) as 'Avg Position'
FROM console_data
WHERE Date >= date('now', '-90 days')
GROUP BY strftime('%Y-%W', Date)
ORDER BY Week DESC;
"
```

## SEO Recommendations

Based on the analysis, provide recommendations for:
1. **Content optimisation** - Pages to update for better rankings
2. **Meta improvements** - Titles/descriptions for low-CTR keywords
3. **New content** - Gap analysis for unranked relevant terms
4. **Technical fixes** - Pages with crawl or indexing issues
