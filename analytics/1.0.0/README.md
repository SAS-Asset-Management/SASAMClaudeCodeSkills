# Analytics Plugin for Claude Code

Website Analytics integration for SAS-AM. Provides access to GA4 and Search Console data via Grafana dashboards, data collection pipelines, and database queries.

## Features

- **Dashboard Management** - Start, stop, restart Grafana; open specific dashboards
- **Data Collection** - Run incremental or full data pulls from Google APIs
- **Analytics Reports** - Generate comprehensive traffic and SEO reports
- **Campaign Analysis** - Track LinkedIn, Google Ads, and UTM-tagged campaigns
- **SEO Insights** - Keyword rankings, CTR analysis, and optimisation opportunities

## Installation

This plugin is part of the SASAMClaudeCodeSkills package. If installed via the marketplace, it's automatically available.

### Manual Installation

```bash
# Copy to Claude Code skills directory
cp -r analytics ~/.claude/SASAMClaudeCodeSkills/
```

## Available Commands

| Command | Description |
|---------|-------------|
| `/analytics.status` | Check system health, database stats, and Grafana status |
| `/analytics.collect` | Run data collection from Google Analytics and Search Console |
| `/analytics.dashboard` | Manage Grafana container and open dashboards |
| `/analytics.report` | Generate analytics summary report |
| `/analytics.seo` | Run SEO keyword analysis |
| `/analytics.campaigns` | View campaign performance metrics |

## Agents

### analytics-advisor

An autonomous agent that diagnoses analytics issues, interprets data, and provides recommendations. Automatically invoked when discussing:

- Dashboard problems or missing data
- API authentication errors
- SEO analysis requests
- Campaign performance questions
- Data collection troubleshooting

## Dashboard Access

| Dashboard | URL |
|-----------|-----|
| Traffic Overview | http://localhost:8000/d/traffic-overview |
| Search Performance | http://localhost:8000/d/search-performance |
| Page Performance | http://localhost:8000/d/page-performance |
| User Experience | http://localhost:8000/d/user-experience |
| Campaign Performance | http://localhost:8000/d/campaign-performance |

**Credentials**: admin / admin123

## Project Location

The Website Analytics project is located at:
```
/Users/sasreliability/Documents/Repos/Website Analytics/
```

## Dependencies

- Docker (for Grafana)
- Python 3.x with virtual environment
- Google Cloud service account (`SAS.json`)
- SQLite database (`website_analytics.db`)

## Version History

- **1.0.0** - Initial release with dashboards, data collection, and reporting commands
