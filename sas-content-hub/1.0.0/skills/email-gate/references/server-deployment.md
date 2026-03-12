# Cortex4 Server Deployment Reference

Server-side deployment details for gated download assets.

## Architecture

```
Webflow page (article)
  -> Custom Code Embed (gate snippet HTML)
       -> Cloudflare Turnstile (bot protection)
            -> POST https://gate.sas-am.com/gate
                 -> sas-gate FastAPI container (cortext4)
                      |- Upserts contact in PostgreSQL (sas-db)
                      |- Records download in downloads table
                      -> Returns signed HMAC download URL (15-min expiry)
                           -> GET https://gate.sas-am.com/download/{token}
                                -> Streams the HTML/PDF file to the user
```

## Server Details

| Component | Detail |
|-----------|--------|
| Host | `cortext4@cortext-t4` (Tailscale) |
| Password | `iso55001:2024` |
| Project dir | `/home/cortext4/docker/clientDatabase/` |
| App container | `sas-gate` (FastAPI, port 8000) |
| DB container | `sas-db` (Postgres 16, port 5435) |
| DB creds | user=`sas`, db=`sas` |
| Docker compose service | `app` (maps to sas-gate container) |
| Cloudflare tunnel | `maturity-tool-tunnel` via `maturityplottingtool_cloudflare` network |
| Public URL | `https://gate.sas-am.com` |
| Turnstile site key | `0x4AAAAAACfsXoEwP0T4dL86` |

## Deployment Script

Use `scripts/deployGate.py` to automate the full deployment:

```bash
# Deploy a new gated asset
python3 ${CLAUDE_PLUGIN_ROOT}/skills/email-gate/scripts/deployGate.py deploy \
  ./myArtefact.html \
  my-resource-slug \
  "Human-Readable Resource Title"

# Dry run (preview without changes)
python3 ${CLAUDE_PLUGIN_ROOT}/skills/email-gate/scripts/deployGate.py deploy \
  ./myArtefact.html \
  my-resource-slug \
  "Human-Readable Resource Title" \
  --dry-run

# List registered resources
python3 ${CLAUDE_PLUGIN_ROOT}/skills/email-gate/scripts/deployGate.py list

# Check recent downloads
python3 ${CLAUDE_PLUGIN_ROOT}/skills/email-gate/scripts/deployGate.py downloads
python3 ${CLAUDE_PLUGIN_ROOT}/skills/email-gate/scripts/deployGate.py downloads --slug my-resource-slug

# Verify server connectivity
python3 ${CLAUDE_PLUGIN_ROOT}/skills/email-gate/scripts/deployGate.py verify
```

## Manual Process (if script fails)

### Step 1: Copy asset to server

```bash
sshpass -p 'iso55001:2024' scp \
  ./myArtefact.html \
  cortext4@cortext-t4:/home/cortext4/docker/clientDatabase/app/assets/my-resource-slug.html
```

### Step 2: Read current resources.json

```bash
sshpass -p 'iso55001:2024' ssh cortext4@cortext-t4 \
  "cat /home/cortext4/docker/clientDatabase/app/assets/resources.json"
```

### Step 3: Add entry and write back

Add to the JSON array:
```json
{
  "slug": "my-resource-slug",
  "label": "Human-Readable Resource Title",
  "file": "assets/my-resource-slug.html",
  "active": true
}
```

### Step 4: Restart container

```bash
sshpass -p 'iso55001:2024' ssh cortext4@cortext-t4 \
  "cd /home/cortext4/docker/clientDatabase && docker compose restart app"
```

### Step 5: Verify

```bash
sshpass -p 'iso55001:2024' ssh cortext4@cortext-t4 \
  "cd /home/cortext4/docker/clientDatabase && docker compose ps"
```

## Current Resources

| Slug | Label | File |
|------|-------|------|
| `sample-guide` | Sample Guide (Placeholder) | `assets/sample-guide.pdf` |
| `maintenance-business-case` | Maintenance Improvement Business Case Template | `assets/maintenance-business-case.html` |
| `pm-effectiveness-checklist` | PM Effectiveness Audit Checklist | `assets/pm-effectiveness-checklist.html` |
| `internal-benchmarking-scorecard` | Internal Maintenance Benchmarking Scorecard | `assets/internal-benchmarking-scorecard.html` |

## Monitoring Downloads

```bash
# Recent downloads (all resources)
python3 ${CLAUDE_PLUGIN_ROOT}/skills/email-gate/scripts/deployGate.py downloads

# Downloads for a specific resource
python3 ${CLAUDE_PLUGIN_ROOT}/skills/email-gate/scripts/deployGate.py downloads --slug maintenance-business-case

# All contacts (leads) — manual query
sshpass -p 'iso55001:2024' ssh cortext4@cortext-t4 \
  "docker exec sas-db psql -U sas -d sas -c \
  \"SELECT first_name, last_name, email, job_title, organisation, source, created_at \
  FROM contacts ORDER BY created_at DESC LIMIT 20;\""
```

## API Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/gate` | Submit lead + get download token |
| GET | `/download/{token}` | Stream the asset (15-min, single-use) |
| GET | `/admin/leads` | All leads with download history (requires `X-Admin-Key`) |
| GET | `/admin/contacts` | All contacts |

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `sshpass` not found | Not installed | `brew install hudochenkov/sshpass/sshpass` |
| SSH connection refused | Tailscale not running or host offline | Check `tailscale status`, ensure cortext-t4 is online |
| Turnstile widget missing | Script not loaded or site key wrong | Check `data-sitekey="0x4AAAAAACfsXoEwP0T4dL86"` |
| "Resource not found" on submit | Slug not in resources.json or container not restarted | Run `deployGate.py list` to check, restart if needed |
| Download link 404 | Token expired (15-min) or file path wrong | Re-submit form; check `file` path in resources.json |
| Form submits but no DB record | Turnstile verification failing server-side | Check logs: `docker logs sas-gate` |
