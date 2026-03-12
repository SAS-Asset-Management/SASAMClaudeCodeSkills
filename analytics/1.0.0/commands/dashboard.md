---
name: dashboard
description: Manage Grafana dashboard container - start, stop, restart, or open in browser.
arguments:
  - name: action
    description: Action to perform - 'start', 'stop', 'restart', 'open', 'logs', or 'status'
    required: false
---

# Dashboard Management

Control the Grafana dashboard container and access dashboards.

## Available Actions

### Start Grafana
```bash
cd "/Users/sasreliability/Documents/Repos/Website Analytics"
docker compose up -d
```

### Stop Grafana
```bash
cd "/Users/sasreliability/Documents/Repos/Website Analytics"
docker compose down
```

### Restart Grafana
```bash
cd "/Users/sasreliability/Documents/Repos/Website Analytics"
docker compose restart grafana
```

### View Logs
```bash
cd "/Users/sasreliability/Documents/Repos/Website Analytics"
docker compose logs -f grafana --tail=50
```

### Check Status
```bash
docker ps --filter "name=website-analytics-grafana" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

## Dashboard URLs

Open in browser:

| Dashboard | Command |
|-----------|---------|
| **Traffic Overview** | `open http://localhost:8000/d/traffic-overview` |
| **Search Performance** | `open http://localhost:8000/d/search-performance` |
| **Page Performance** | `open http://localhost:8000/d/page-performance` |
| **User Experience** | `open http://localhost:8000/d/user-experience` |
| **Campaign Performance** | `open http://localhost:8000/d/campaign-performance` |

## Credentials

- **URL**: http://localhost:8000
- **Username**: admin
- **Password**: admin123

## Troubleshooting

If dashboards show no data:
1. Check datasource: `curl -s -u admin:admin123 http://localhost:8000/api/datasources/1/health`
2. Test queries: `python3 scripts/test-queries.py`
3. Verify database mount in docker-compose.yml
