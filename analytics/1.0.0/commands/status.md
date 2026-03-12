---
name: status
description: Show database health, last update timestamps, row counts per table, cron job status, and Grafana container state.
---

# Analytics Status Check

Run a comprehensive health check of the Website Analytics system.

## Steps

1. **Check database health and row counts**
```bash
sqlite3 "/Users/sasreliability/Documents/Repos/Website Analytics/website_analytics.db" \
  "SELECT 'user_data' as table_name, COUNT(*) as rows, MAX(Date) as last_update FROM user_data
   UNION ALL SELECT 'console_data', COUNT(*), MAX(Date) FROM console_data
   UNION ALL SELECT 'page_data', COUNT(*), MAX(Date) FROM page_data
   UNION ALL SELECT 'website_data', COUNT(*), MAX(Date) FROM website_data;"
```

2. **Check Grafana container status**
```bash
docker ps --filter "name=website-analytics-grafana" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

3. **Check cron job configuration**
```bash
crontab -l 2>/dev/null | grep -i "analytics\|website" || echo "No analytics cron jobs found"
```

4. **Check last data collection log**
```bash
if [ -f "/Users/sasreliability/Documents/Repos/Website Analytics/logs/data-collection.log" ]; then
  tail -5 "/Users/sasreliability/Documents/Repos/Website Analytics/logs/data-collection.log"
else
  echo "No collection log found"
fi
```

5. **Verify Grafana datasource health**
```bash
curl -s -u admin:admin123 "http://localhost:8000/api/datasources/1/health" 2>/dev/null || echo "Grafana not reachable"
```

Present the results in a clear summary format showing system health status.
