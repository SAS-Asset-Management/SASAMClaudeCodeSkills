---
name: website-analytics
description: Provide expertise for the SAS-AM Website Analytics system. Use when the user asks about:
- Google Analytics or Search Console data collection
- Microsoft Clarity UX analytics (heatmaps, rage clicks, dead clicks, session recordings)
- SQLite database queries for analytics data
- Grafana dashboard configuration or troubleshooting
- Data pipeline issues, cron jobs, or automation
- SEO keyword analysis or SERP ranking
- API authentication with Google services or Clarity
- Analytics metrics interpretation (bounce rate, CTR, impressions, scroll depth)
- Docker container issues with Grafana
- LinkedIn or Google Ads campaign tracking
- UTM parameters and attribution
---

# Website Analytics Skill

You are an expert in the SAS-AM Website Analytics system. Data is collected from Google Analytics 4, Google Search Console and Microsoft Clarity, stored in SQLite, and visualised through a Grafana container — all running on the cortext4 server. The Mac repo is a development copy.

## System Architecture (production lives on cortext4)

```
┌─────────────────┐    ┌─────────────────────┐    ┌──────────────────────────┐
│ Google APIs     │    │  cron @ 05:28 daily │    │  cortext4 SQLite         │
│ (GA4 + Console) │ ─► │  run-data-collection│ ─► │  ~/docker/                │
│ MS Clarity API  │    │  -server.sh         │    │  websiteAnalytics/       │
│                 │    │                     │    │  website_analytics.db    │
└─────────────────┘    └─────────────────────┘    └──────────────┬───────────┘
                                                                 │
                                  ┌─────────────────────────────┐│
                                  │  cortext4 Docker:           ││
                                  │  websiteanalytics_grafana   │◄┘
                                  │  (no ports exposed)         │
                                  └──────────────┬──────────────┘
                                                 │
                          ┌──────────────────────▼─────────────────────┐
                          │  nginx + Cloudflare tunnel (sidecar)       │
                          │  https://team.sas-am.com/tools/analytics/  │
                          └────────────────────────────────────────────┘
```

## Source of truth

| Asset | Production (use this) | Dev copy |
| --- | --- | --- |
| Database | `cortext4:~/docker/websiteAnalytics/website_analytics.db` | `/Users/sasreliability/Documents/Repos/Website Analytics/website_analytics.db` (sync via `scp`) |
| Grafana | `https://team.sas-am.com/tools/analytics/` (live) | `docker compose up -d` locally on `:8000` (dev only — usually stale) |
| Cron | cortext4, runs `~/docker/websiteAnalytics/scripts/run-data-collection-server.sh` daily 05:28 UTC | none |
| Code | `cortext4:~/docker/websiteAnalytics/` | `/Users/sasreliability/Documents/Repos/Website Analytics/` (manual sync, may drift) |

**Always check the cortext4 database, not the local Mac copy** unless you have just synced it. The Mac copy is frequently weeks stale.

## Grafana access

**Production:** [https://team.sas-am.com/tools/analytics/](https://team.sas-am.com/tools/analytics/) — login Shane's SSO via the team portal.

**Available dashboards:**

| Dashboard | URL fragment | Purpose |
|-----------|--------------|---------|
| Traffic Overview | `/d/traffic-overview` | User metrics, device breakdown, geographic data |
| Search Performance | `/d/search-performance` | Keyword rankings, CTR, search trends |
| Page Performance | `/d/page-performance` | Page views, session data, referrer analysis |
| User Experience | `/d/user-experience` | Engagement metrics, bounce rate, session duration |
| Campaign Performance | `/d/campaign-performance` | LinkedIn/Google Ads tracking, UTM analysis |

## Database Schema (verified against the live cortext4 DB)

The SQLite database `website_analytics.db` contains:

### `page_data`
Per page metrics from GA4. **Note:** there is no `Page Path` column — use `Landing Page` for the URL path.
```
Referrer            TEXT
Country             TEXT
City                TEXT
Date                TIMESTAMP
Page Title          TEXT
Landing Page        TEXT       -- the URL path (not "Page Path")
Medium              TEXT
Page Views          INTEGER
Session Duration (secs) INTEGER
Referrer Type       TEXT
Event Type          TEXT
Event Count         INTEGER
Page Type           TEXT
Data Table          TEXT
```

### `user_data`
GA4 user behaviour. **Note:** there is no `Sessions` column — Total Users + Engagement Rate are the headline metrics. Campaign / Campaign Content / Campaign Term are populated from UTM parameters.
```
Country             TEXT
Event Type          TEXT
City                TEXT
Date                TIMESTAMP
Device Category     TEXT
Landing Page        TEXT
Medium              TEXT
New vs Returning User TEXT
Average Session Duration (secs) REAL
Bounce Rate         REAL
Engagement Rate     REAL
New Users           INTEGER
Total Users         INTEGER
Page Views          INTEGER
Returning Users     INTEGER
Page Type           TEXT
Source              TEXT
Data Table          TEXT
Campaign            TEXT
Campaign Content    TEXT
Campaign Term       TEXT
```

### `console_data`
Google Search Console. **Note:** no `CTR` column — compute as `Clicks * 1.0 / Impressions`.
```
Page                TEXT
Date                TIMESTAMP
Device              TEXT
Country             TEXT
Query               TEXT
Clicks              INTEGER
Impressions         INTEGER
Position            REAL
Page Type           TEXT
Data Table          TEXT
Medium              TEXT
Source              TEXT
```

### `website_data`
Consolidated view that joins user, page and campaign data. Most reporting queries should hit this table; raw tables only when you need a column the join drops.

### `clarity_traffic`
MS Clarity traffic by dimension (page, country, device, etc).
```
collected_date      TEXT
dimension_type      TEXT
dimension_value     TEXT
total_sessions      INTEGER
bot_sessions        INTEGER
distinct_users      INTEGER
pages_per_session   REAL
```

### `clarity_engagement`
UX quality signals — the most useful Clarity table for spotting friction.
```
collected_date      TEXT
dimension_type      TEXT
dimension_value     TEXT
scroll_depth        REAL
engagement_time     REAL
dead_clicks         INTEGER
rage_clicks         INTEGER
excessive_scrolls   INTEGER
quickbacks          INTEGER
script_errors       INTEGER
error_clicks        INTEGER
```

### `clarity_pages`
Per page Clarity metrics.
```
collected_date      TEXT
page_url            TEXT       -- full URL including https://
page_title          TEXT
sessions            INTEGER
scroll_depth        REAL
engagement_time     REAL
```

### `meta_table`
Update tracking and metadata for the cron pipeline.

## Working with the data

### Quickest path: query cortext4 directly

The server doesn't have `sqlite3` installed at the binary level, but Python's `sqlite3` module is available:

```bash
ssh cortext4 "python3 -c \"
import sqlite3
c = sqlite3.connect('/home/cortext4/docker/websiteAnalytics/website_analytics.db')
for row in c.execute('SELECT MAX(Date), COUNT(*) FROM user_data'):
    print(row)
\""
```

For one-off interactive work, prefer to sync the DB locally first.

### Sync the DB to local for richer querying

```bash
scp cortext4:~/docker/websiteAnalytics/website_analytics.db \
    "/Users/sasreliability/Documents/Repos/Website Analytics/website_analytics.db"
```

The DB is ~40 MB — the sync takes a few seconds over Tailscale. After syncing, query locally with `sqlite3` against the path. The local copy is also what a local Grafana (`docker compose up -d`) reads from.

### Trigger a fresh data pull on the server (between cron runs)

```bash
ssh cortext4 "cd ~/docker/websiteAnalytics && bash scripts/run-data-collection-server.sh"
```

The server script: pulls GA4 + Search Console + Clarity, appends to SQLite, restarts the Grafana container. Idempotent — safe to run on demand.

### Investigate the cron pipeline

Cron entry: runs `~/docker/websiteAnalytics/scripts/run-data-collection-server.sh` daily at 05:28 UTC.

```bash
ssh cortext4 "tail -50 ~/docker/websiteAnalytics/logs/data-collection.log"
ssh cortext4 "crontab -l | grep -i analytic"
```

If the log shows recent successful runs ("Data Collection Completed Successfully") but the DB still looks stale to a local user, the issue is the local copy hasn't been synced — not the pipeline.

## Useful query templates (use the verified schema)

### Top resources pages — last 14 days
```sql
SELECT
  REPLACE("Landing Page", '/resources/', '') AS slug,
  SUM("Page Views") AS views
FROM page_data
WHERE "Landing Page" LIKE '/resources/%'
  AND Date >= date('now', '-14 days')
GROUP BY "Landing Page"
ORDER BY views DESC
LIMIT 15;
```

### LinkedIn-driven traffic, daily
```sql
SELECT Date,
  SUM("Total Users") AS users,
  ROUND(AVG("Engagement Rate") * 100, 1) AS engage_pct,
  ROUND(AVG("Bounce Rate") * 100, 1) AS bounce_pct
FROM user_data
WHERE LOWER(Source) LIKE '%linkedin%'
  AND Date >= date('now', '-30 days')
GROUP BY Date
ORDER BY Date DESC;
```

### Top traffic sources, last 7 days
```sql
SELECT Source, Medium, Campaign,
  SUM("Total Users") AS users,
  SUM("New Users") AS new_users
FROM user_data
WHERE Date >= date('now', '-7 days')
GROUP BY Source, Medium, Campaign
ORDER BY users DESC
LIMIT 20;
```

### Search queries driving clicks to /resources/, with computed CTR
```sql
SELECT Query,
  SUM(Clicks) AS clicks,
  SUM(Impressions) AS impressions,
  ROUND(SUM(Clicks) * 100.0 / NULLIF(SUM(Impressions), 0), 2) AS ctr_pct,
  ROUND(AVG(Position), 1) AS avg_position
FROM console_data
WHERE Page LIKE '%/resources/%'
  AND Date >= date('now', '-30 days')
GROUP BY Query
HAVING clicks > 0
ORDER BY clicks DESC
LIMIT 20;
```

### Clarity friction signals — pages with rage clicks or dead clicks
```sql
SELECT dimension_value AS page_or_dim,
  SUM(dead_clicks) AS dead,
  SUM(rage_clicks) AS rage,
  SUM(quickbacks) AS quickbacks,
  SUM(error_clicks) AS errors
FROM clarity_engagement
WHERE collected_date >= date('now', '-7 days')
GROUP BY dimension_value
HAVING dead > 0 OR rage > 0
ORDER BY rage DESC, dead DESC
LIMIT 15;
```

## SQLite Query Format for Grafana

The frser-sqlite-datasource plugin requires specific query formatting:

### Time series queries
```sql
SELECT
  strftime('%Y-%m-%dT%H:%M:%SZ', Date) as time,
  SUM("Page Views") as "Page Views"
FROM page_data
WHERE Date >= date('now', '-${period}')
GROUP BY DATE(Date)
ORDER BY time;
```

Set `timeColumns: ["time"]` in the target configuration.

### Stat panel queries
```sql
SELECT SUM("Total Users") as value
FROM user_data
WHERE Date >= date('now', '-${period}');
```

### Table queries
```sql
SELECT Country, SUM("Total Users") as Users
FROM user_data
WHERE Date >= date('now', '-30 days')
GROUP BY Country
ORDER BY Users DESC
LIMIT 10;
```

## Common Issues & Solutions

### Local DB looks stale
You are looking at the dev copy on the Mac, not production. Sync from cortext4:
```bash
scp cortext4:~/docker/websiteAnalytics/website_analytics.db \
    "/Users/sasreliability/Documents/Repos/Website Analytics/website_analytics.db"
```

### Production DB looks stale
Cron has stopped. Check the log and re-run the pipeline:
```bash
ssh cortext4 "tail -50 ~/docker/websiteAnalytics/logs/data-collection.log"
ssh cortext4 "cd ~/docker/websiteAnalytics && bash scripts/run-data-collection-server.sh"
```

### Grafana login issues at team.sas-am.com
Production Grafana is behind the team portal SSO — login via the portal, not directly. If the portal route is broken, check the nginx sidecar and Cloudflare tunnel container in `~/docker/` on cortext4.

### Local Grafana shows no data
The local container is a dev tool, not the production view. Either sync the DB first (above) or just use the production Grafana at https://team.sas-am.com/tools/analytics/.

### Schema query returns "no such column"
The published SAS-AM schema differs from what naive GA4-tutorial queries expect. Specifically:
- `page_data` has `Landing Page`, not `Page Path`
- `user_data` has no `Sessions` column — use `Total Users` or `Page Views`
- `console_data` has no `CTR` column — compute as `Clicks * 100.0 / Impressions`

## Key Metrics Explained

| Metric | Description | Good Value |
|--------|-------------|------------|
| Engagement Rate | % of sessions with engagement (>10s, conversion, or 2+ pages) | >50% |
| Bounce Rate | % of single-page sessions | <50% |
| CTR | Search Console click-through rate (computed from Clicks/Impressions) | >3% |
| Average Position | Search ranking position | <10 |
| Session Duration | Average time spent on site (in seconds) | >60s |
| Scroll Depth (Clarity) | Average % scrolled on a page | >60% |
| Rage Clicks (Clarity) | Repeated rapid clicks suggesting frustration | <1 per session |

## Integration with Other Skills

### linkedin-post-generator
Track which LinkedIn posts drive traffic. UTM convention:
- `utm_source=linkedin`
- `utm_medium=organic_social` or `paid_social`
- `utm_campaign=<campaign-slug>` matching the `campaign` field in `analytics/performance.db` `content_registry` table

The `Campaign` column in `user_data` and `website_data` is what these queries filter on.

### linkedin content campaign measurement workflow
1. After each LinkedIn post is published, run `python3 analytics/register.py link <id> <url>` in the linkedinContentCreation repo (separate DB).
2. Wait 1–7 days for engagement and traffic to accumulate.
3. Sync the analytics DB from cortext4.
4. Query `user_data` filtered on the `Campaign` slug to attribute web sessions to the LinkedIn post.
5. Cross reference with engagement/impressions from the LinkedIn-side `content_registry` to compute downstream-traffic-per-impression.

### b2b-research-agent
High-traffic pages indicate prospect interest areas. Use the Resources page top-15 query to surface the topics drawing the most engaged sessions in the last 30 days.

### push-notifications
Set up alerts for traffic anomalies (week-on-week drop > 30%) or milestone achievements (first 100 LinkedIn-driven sessions on a new article).

## Files Reference (on cortext4)

| File | Purpose |
|------|---------|
| `~/docker/websiteAnalytics/automated data pull.py` | GA4 + Search Console collector |
| `~/docker/websiteAnalytics/clarityCollect.py` | MS Clarity collector |
| `~/docker/websiteAnalytics/website_analytics.db` | Production SQLite database |
| `~/docker/websiteAnalytics/scripts/run-data-collection-server.sh` | Daily orchestrator (cron + on-demand) |
| `~/docker/websiteAnalytics/logs/data-collection.log` | Cron run log — first stop when something looks broken |
| `~/docker/websiteAnalytics/grafana/dashboards/*.json` | Dashboard definitions |
| `~/docker/websiteAnalytics/grafana/provisioning/` | Grafana auto-provisioning config |
| `~/docker/websiteAnalytics/docker-compose.yml` | Production Docker config (no exposed ports — uses team portal nginx + Cloudflare tunnel) |
| `~/docker/websiteAnalytics/SAS.json` | GA4 + Search Console service account credentials |
