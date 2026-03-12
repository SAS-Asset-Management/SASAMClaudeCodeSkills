---
name: collect
description: Run Google Analytics and Search Console data collection. Use --full for complete 365-day refresh, default is incremental update.
arguments:
  - name: mode
    description: Collection mode - 'incremental' (default) or 'full' for complete refresh
    required: false
---

# Data Collection

Run the data collection pipeline to fetch latest analytics data from Google APIs.

## Execution

```bash
cd "/Users/sasreliability/Documents/Repos/Website Analytics"

# Activate virtual environment if exists
if [ -d "website_analytics_venv" ]; then
  source website_analytics_venv/bin/activate
fi

# Run data collection
python3 "automated data pull.py"
```

## Post-Collection

After collection completes:

1. **Verify new data**
```bash
sqlite3 website_analytics.db "SELECT MAX(Date) as latest_data FROM user_data;"
```

2. **Restart Grafana to refresh dashboards** (optional)
```bash
docker compose restart grafana
```

3. **Open dashboard to verify**
```bash
open http://localhost:8000/d/traffic-overview
```

## Notes

- The script automatically detects the last collection date and fetches only new data (incremental)
- For a full 365-day refresh, modify the date range in the script
- API quotas: GA4 has generous limits; Search Console allows 1,200 requests/minute
- Collection typically takes 2-5 minutes depending on data volume
