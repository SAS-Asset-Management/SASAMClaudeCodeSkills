---
name: website-analytics
description: Provide expertise for the SAS-AM Website Analytics system. Use when the user asks about:
- Google Analytics or Search Console data collection
- SQLite database queries for analytics data
- Grafana dashboard configuration or troubleshooting
- Data pipeline issues, cron jobs, or automation
- SEO keyword analysis or SERP ranking
- API authentication with Google services
- Analytics metrics interpretation (bounce rate, CTR, impressions)
- Docker container issues with Grafana
- LinkedIn or Google Ads campaign tracking
- UTM parameters and attribution
---

# Website Analytics Skill

You are an expert in the SAS-AM Website Analytics system. This system collects data from Google Analytics 4 (GA4) and Google Search Console, stores it in SQLite, and visualises it through Docker-based Grafana dashboards.

## System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Google APIs     │ -> │ Python Scripts  │ -> │ SQLite Database │
│ (GA4 + Console) │    │ (Data Collection)│    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
┌─────────────────┐    ┌─────────────────┐             │
│ Grafana         │ <- │ Docker Container│ <-----------┘
│ Dashboards      │    │                 │
└─────────────────┘    └─────────────────┘
```

## Project Location

The Website Analytics project is located at:
```
/Users/sasreliability/Documents/Repos/Website Analytics/
```

## Available Dashboards

Access Grafana at **http://localhost:8000** (credentials: admin / admin123)

| Dashboard | URL | Purpose |
|-----------|-----|---------|
| **Traffic Overview** | `/d/traffic-overview` | User metrics, device breakdown, geographic data |
| **Search Performance** | `/d/search-performance` | Keyword rankings, CTR, search trends |
| **Page Performance** | `/d/page-performance` | Page views, session data, referrer analysis |
| **User Experience** | `/d/user-experience` | Engagement metrics, bounce rate, session duration |
| **Campaign Performance** | `/d/campaign-performance` | LinkedIn/Google Ads tracking, UTM analysis |

## Database Schema

The SQLite database (`website_analytics.db`) contains these tables:

### console_data (~120k rows)
Google Search Console metrics:
- `Date`, `Page`, `Query`, `Device`, `Country`
- `Clicks`, `Impressions`, `CTR`, `Position`

### user_data (~21k rows)
Google Analytics user behaviour:
- `Date`, `Source`, `Medium`, `Campaign`, `Country`, `Device Category`
- `Total Users`, `New Users`, `Sessions`
- `Engagement Rate`, `Bounce Rate`, `Average Session Duration (secs)`

### page_data (~11k rows)
Page performance metrics:
- `Date`, `Page Title`, `Page Path`, `Referrer`
- `Page Views`, `Sessions`, `Engagement Time`

### website_data (~7k rows)
Consolidated analytics combining all sources.

### meta_table
Update tracking and metadata.

## Key Commands

### Data Collection
```bash
# Full data collection (GA4 + Search Console)
cd "/Users/sasreliability/Documents/Repos/Website Analytics"
python3 "automated data pull.py"

# Via cron job (runs daily at 5:28 AM)
./scripts/run-data-collection.sh
```

### Dashboard Management
```bash
# Start Grafana
docker compose up -d

# Restart after changes
docker compose restart grafana

# View logs
docker compose logs -f grafana

# Open dashboard
open http://localhost:8000
```

### Database Queries
```bash
# Check table counts
sqlite3 website_analytics.db "SELECT 'console_data' as tbl, COUNT(*) as rows FROM console_data UNION ALL SELECT 'user_data', COUNT(*) FROM user_data UNION ALL SELECT 'page_data', COUNT(*) FROM page_data;"

# Check latest data date
sqlite3 website_analytics.db "SELECT MAX(Date) FROM user_data;"

# Test dashboard queries
python3 scripts/test-queries.py
```

## SQLite Query Format for Grafana

The frser-sqlite-datasource plugin requires specific query formatting:

### Time Series Queries
```sql
SELECT
  strftime('%Y-%m-%dT%H:%M:%SZ', Date) as time,
  SUM("Page Views") as "Page Views"
FROM page_data
WHERE Date >= date('now', '-${period}')
GROUP BY DATE(Date)
ORDER BY time;
```

**Important**: Use `timeColumns: ["time"]` in the target configuration.

### Stat Panel Queries
```sql
SELECT SUM("Total Users") as value
FROM user_data
WHERE Date >= date('now', '-${period}');
```

### Table Queries
```sql
SELECT Country, SUM("Total Users") as Users
FROM user_data
WHERE Date >= date('now', '-30 days')
GROUP BY Country
ORDER BY Users DESC
LIMIT 10;
```

## Common Issues & Solutions

### No Data in Dashboards
1. Check if Grafana is running: `docker compose ps`
2. Verify database has recent data: `sqlite3 website_analytics.db "SELECT MAX(Date) FROM user_data;"`
3. Test queries: `python3 scripts/test-queries.py`
4. Check datasource UID matches: `website-analytics-sqlite`

### API Authentication Errors
1. Verify `SAS.json` service account file exists
2. Check Google API quotas in Cloud Console
3. Ensure service account has access to GA4 property and Search Console

### Grafana Login Issues
```bash
# Reset admin password
docker compose exec grafana grafana cli admin reset-admin-password newpassword

# Restart to clear lockouts
docker compose restart grafana
```

## Key Metrics Explained

| Metric | Description | Good Value |
|--------|-------------|------------|
| **Engagement Rate** | % of sessions with engagement (>10s, conversion, or 2+ pages) | >50% |
| **Bounce Rate** | % of single-page sessions | <50% |
| **CTR** | Search Console click-through rate | >3% |
| **Average Position** | Search ranking position | <10 |
| **Session Duration** | Time spent on site (in seconds) | >60s |

## Integration with Other Skills

### linkedin-post-generator
Track which LinkedIn posts drive traffic via UTM parameters:
- `utm_source=linkedin`
- `utm_medium=organic` or `utm_medium=paid_social`

### b2b-research-agent
Identify high-traffic pages that indicate prospect interest areas.

### push-notifications
Set up alerts for traffic anomalies or milestone achievements.

## Files Reference

| File | Purpose |
|------|---------|
| `automated data pull.py` | Main data collection orchestrator |
| `Website_Analytics.py` | SEO analysis tools |
| `website_analytics.db` | SQLite database |
| `grafana/dashboards/*.json` | Dashboard definitions |
| `grafana/provisioning/` | Grafana auto-provisioning config |
| `scripts/setup.sh` | Initial setup script |
| `scripts/update-data.sh` | Data refresh with Grafana restart |
| `docker-compose.yml` | Docker configuration |
| `Dockerfile` | Grafana container build |
