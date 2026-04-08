---
name: clarity
description: Collect and query Microsoft Clarity UX analytics. Use 'collect' to pull latest data, 'status' to check tables, or 'query' to explore stored data.
arguments:
  - name: action
    description: "Action to perform: 'collect' (pull from API), 'status' (check DB), 'query' (explore data), 'setup' (show setup instructions)"
    required: false
---

# Microsoft Clarity Analytics

Manage Microsoft Clarity UX analytics data for sas-am.com.

## Architecture

```
Clarity Dashboard (sas-am.com)
  └─ Data Export API (Bearer token, 10 req/day)
       └─ clarityCollect.py
            └─ website_analytics.db (3 tables: clarity_traffic, clarity_engagement, clarity_pages)
```

## Actions

### collect — Pull latest data from Clarity API

```bash
cd "/Users/sasreliability/Documents/Repos/Website Analytics"
source websiteAnalyticsVenv/bin/activate
python3 clarityCollect.py
```

The script pulls 3 days of data across 8 dimension combinations (Device, Source+Medium, URL, Country, Browser, OS, Channel, and overall). Uses 8 of the 10 daily API calls.

### status — Check Clarity data in the database

```bash
cd "/Users/sasreliability/Documents/Repos/Website Analytics"
sqlite3 website_analytics.db "
SELECT 'clarity_traffic' as tbl, COUNT(*) as rows, MIN(collected_date) as earliest, MAX(collected_date) as latest FROM clarity_traffic
UNION ALL
SELECT 'clarity_engagement', COUNT(*), MIN(collected_date), MAX(collected_date) FROM clarity_engagement
UNION ALL
SELECT 'clarity_pages', COUNT(*), MIN(collected_date), MAX(collected_date) FROM clarity_pages;
"
```

### query — Explore Clarity data

**Overall traffic summary (last 7 days):**
```sql
SELECT collected_date, SUM(total_sessions) as sessions, SUM(distinct_users) as users, SUM(bot_sessions) as bots
FROM clarity_traffic
WHERE dimension_type = 'overall'
GROUP BY collected_date
ORDER BY collected_date DESC
LIMIT 7;
```

**UX issues (dead clicks, rage clicks, quickbacks):**
```sql
SELECT collected_date, SUM(dead_clicks) as dead, SUM(rage_clicks) as rage, SUM(quickbacks) as quickbacks, SUM(script_errors) as errors
FROM clarity_engagement
WHERE dimension_type = 'overall'
GROUP BY collected_date
ORDER BY collected_date DESC
LIMIT 7;
```

**Traffic by device:**
```sql
SELECT dimension_value as device, total_sessions as sessions, distinct_users as users, pages_per_session
FROM clarity_traffic
WHERE dimension_type = 'Device' AND collected_date = (SELECT MAX(collected_date) FROM clarity_traffic)
ORDER BY total_sessions DESC;
```

**Traffic by source + medium:**
```sql
SELECT dimension_value as source, total_sessions as sessions, distinct_users as users
FROM clarity_traffic
WHERE dimension_type = 'Source+Medium' AND collected_date = (SELECT MAX(collected_date) FROM clarity_traffic)
ORDER BY total_sessions DESC
LIMIT 15;
```

**Top pages by sessions:**
```sql
SELECT page_url, page_title, sessions, scroll_depth, engagement_time
FROM clarity_pages
WHERE collected_date = (SELECT MAX(collected_date) FROM clarity_pages)
ORDER BY sessions DESC
LIMIT 20;
```

**Pages with UX problems (rage clicks or dead clicks by URL):**
```sql
SELECT dimension_value as url, dead_clicks, rage_clicks, quickbacks, scroll_depth
FROM clarity_engagement
WHERE dimension_type = 'URL' AND collected_date = (SELECT MAX(collected_date) FROM clarity_engagement)
AND (dead_clicks > 0 OR rage_clicks > 0 OR quickbacks > 0)
ORDER BY rage_clicks DESC
LIMIT 20;
```

### setup — First time configuration

1. Log in to [Microsoft Clarity](https://clarity.microsoft.com/)
2. Open the sas-am.com project
3. Go to **Settings > Data Export > Generate new API token**
4. Copy the token
5. Add to `.env` in the Website Analytics project:
   ```
   CLARITY_API_TOKEN=your_token_here
   ```
6. Run the first collection:
   ```bash
   cd "/Users/sasreliability/Documents/Repos/Website Analytics"
   source websiteAnalyticsVenv/bin/activate
   python3 clarityCollect.py
   ```

## Database Schema

### clarity_traffic
| Column | Type | Description |
|--------|------|-------------|
| collected_date | TEXT | Date of collection (YYYY-MM-DD) |
| dimension_type | TEXT | Dimension grouping (overall, Device, Source+Medium, etc.) |
| dimension_value | TEXT | Dimension value (e.g., "Mobile", "google", "Australia") |
| total_sessions | INTEGER | Total session count |
| bot_sessions | INTEGER | Bot session count |
| distinct_users | INTEGER | Distinct user count |
| pages_per_session | REAL | Average pages per session |

### clarity_engagement
| Column | Type | Description |
|--------|------|-------------|
| collected_date | TEXT | Date of collection |
| dimension_type | TEXT | Dimension grouping |
| dimension_value | TEXT | Dimension value |
| scroll_depth | REAL | Average scroll depth |
| engagement_time | REAL | Average engagement time |
| dead_clicks | INTEGER | Clicks on non interactive elements |
| rage_clicks | INTEGER | Rapid repeated clicks (frustration signal) |
| excessive_scrolls | INTEGER | Excessive scrolling events |
| quickbacks | INTEGER | Quick navigation away (bounce signal) |
| script_errors | INTEGER | JavaScript error count |
| error_clicks | INTEGER | Clicks resulting in errors |

### clarity_pages
| Column | Type | Description |
|--------|------|-------------|
| collected_date | TEXT | Date of collection |
| page_url | TEXT | Page URL |
| page_title | TEXT | Page title |
| sessions | INTEGER | Session count for page |
| scroll_depth | REAL | Average scroll depth |
| engagement_time | REAL | Average engagement time |

## Rate Limits

- **10 API requests per project per day** (the collection script uses 8)
- Data covers the **last 1 to 3 days** only — daily collection builds history
- Max **1,000 rows** per response, no pagination
- Results are in **UTC timezone**
