# External Integrations

**Analysis Date:** 2026-02-25

## APIs & External Services

**Web Scraping:**
- **tenders.vic.gov.au** - Victorian government tender portal
  - SDK/Client: `cloudscraper` + `beautifulsoup4`
  - Auth: None (public access, Cloudflare protection bypassed via cloudscraper)
  - Data scraped: Tender listings, RFx numbers, issuer names, opening/closing dates, tender types, UNSPSC categories
  - Rate limiting: 2 second delay between page requests (configurable via `--delay` flag)
  - Location: `vicTenders/tender-assessment/1.0.0/vic_tenders_scraper.py`

## Data Storage

**Databases:**
- None (not applicable - no persistent database)

**File Storage:**
- **Local filesystem only** - All state stored as JSON files in working directory or `.beam/` hidden directory
- State files:
  - `seen_tender_ids.json` - Tracks tender IDs to detect new submissions (persists across script runs)
  - `.beam/` directory - Stores engagement state for beam-selling skill as JSON format

**Caching:**
- Tender state file (`seen_tender_ids.json`) acts as cache/deduplication mechanism
- No caching server (Redis, Memcached) used
- Browser localStorage used for presentation theme preference (light/dark mode toggle)

## Authentication & Identity

**Auth Provider:**
- None - No authentication required for public APIs
- tenders.vic.gov.au is publicly accessible
- SMTP email alerts use basic SMTP (no authentication detected in code)

**Authorization:**
- Cloud Scraper handles Cloudflare anti-bot challenge automatically
- No API keys, tokens, or credentials required

## Monitoring & Observability

**Error Tracking:**
- None detected - No integration with Sentry, Datadog, or similar

**Logs:**
- Python standard logging module (INFO level by default)
- Log format: `[TIMESTAMP] [LEVEL] [MESSAGE]`
- Example output:
  ```
  2026-02-25 12:00:00  INFO  Starting tender assessment...
  2026-02-25 12:00:01  INFO  Scraping tenders...
  2026-02-25 12:00:15  INFO  Scraped 125 tenders
  ```
- Logged to stdout/stderr (no file logging configured)

**Metrics:**
- Statistics calculated within assessment output (by_issuer, by_tender_type, by_decision, score_distribution)
- Statistics output as JSON in comprehensive assessment report

## Notifications

**Email Alerts:**
- **SMTP-based email notifications** for matched tenders
- Implementation: `vic_tenders_scraper.py:send_email_alert()`
- Configuration:
  - SMTP Host: `localhost` (default, configurable via `--smtp-host`)
  - SMTP Port: `25` (default)
  - Sender: `noreply@marcov.com.au` (hardcoded)
  - Recipient: Specified via `--notify EMAIL` flag
- Triggered when: `--notify email@example.com` flag provided and matching tenders found
- Fallback: If SMTP connection fails, prints alert to stdout
- Email content: Plain text summary of matched tenders with title, issuer, dates, keywords, URL

**Webhook/Callbacks:**
- None detected

## CI/CD & Deployment

**Hosting:**
- Deployed as Claude Code plugins (local to Claude Code environment)
- No cloud hosting platform (AWS, Azure, GCP) detected
- Skills registered in `~/.claude/commands/` directory

**CI Pipeline:**
- Git hooks (post-checkout, post-merge) auto-register commands after git operations
- No external CI service (GitHub Actions, GitLab CI) detected
- Manual registration available via `register-commands.sh`

**Version Control:**
- Git-based (MIT license)
- Plugin versioning in `plugin.json`: all current skills at 1.0.0

## Environment Configuration

**Required Environment Variables:**
- None detected - All configuration via CLI flags or defaults

**CLI Flags (from vic_tenders_scraper.py):**
```
--output, -o FILE              # Write JSON output to file
--keywords, -k KEYWORDS        # Comma-separated keywords to filter by
--new-only                     # Only tenders opened in last 24h
--track-new                    # Detect genuinely new tenders (vs. seen before)
--state-file PATH              # Path to JSON state file (default: seen_tender_ids.json)
--notify EMAIL                 # Send email alert to recipient
--smtp-host HOST               # SMTP server host (default: localhost)
--delay SECONDS                # Wait between page requests (default: 2.0)
--pretty                       # Pretty-print JSON output
--opened-today                 # Only tenders opened today
--opened-from DD/MM/YYYY       # Filter from date (server-side)
--opened-to DD/MM/YYYY         # Filter to date (server-side)
```

**CLI Flags (from assess_tenders.py):**
```
--output, -o FILE              # Write JSON output to file
--pretty                       # Pretty-print JSON output
--opened-today                 # Only today's tenders
--opened-from DD/MM/YYYY       # Opening date from
--opened-to DD/MM/YYYY         # Opening date to
--no-keywords                  # Skip keyword filtering
```

**Secrets Location:**
- No secrets detected
- SMTP password: Not implemented (basic SMTP, no auth)
- API keys: None required

## Data Filtering & Keywords

**Tender Keyword Lists:**
- `MARCOV_KEYWORDS` in `vic_tenders_scraper.py` defines 40+ asset management related terms
- Keywords grouped by priority (HIGH, MEDIUM, LOWER)
- Filtering case-insensitive, partial match on title/issuer/categories

**Auto-Decline Patterns:**
- Title patterns: construction, procurement, supply, maintenance service, clinical, hazardous materials, property, etc. (38 patterns)
- Issuer patterns: educational and healthcare institutions (6 patterns)
- Location: `assess_tenders.py` lines 44-73

**High-Value Indicators:**
- Asset management terms: "ISO 55001", "GFMAM", "asset management", "asset strategy"
- Reliability terms: "RCM", "FMEA", "predictive maintenance", "condition monitoring"
- Data/Analytics terms: "predictive model", "predictive analytics", "data analytics"
- Location: `assess_tenders.py` lines 76-88

## Scoring Matrix

**Integration with Tender Assessment:**
- Weighted scoring system (5 dimensions = 100 points max):
  1. Domain Fit (30 points)
  2. Industry Match (25 points)
  3. Service Type (20 points)
  4. Strategic Value (15 points)
  5. Competitive Position (10 points)

- Tier 1 clients (Metro Trains, Melbourne Water, Yarra Valley Water, V/Line): 25 points
- Tier 2 clients (Yarra Trams, Barwon Water, AusNet, Gippsland Water): up to 22 points
- Decision thresholds:
  - ≥80 points: SHORTLIST (pursue)
  - 60-79 points: REVIEW (manual assessment)
  - <60 points or auto-decline patterns: DECLINE

## Integrations Summary

| Component | Type | Purpose | Status |
|-----------|------|---------|--------|
| tenders.vic.gov.au | Web API (scraping) | Tender discovery | Active |
| BeautifulSoup4 | Parser | HTML extraction | Active |
| Cloudscraper | Library | Cloudflare bypass | Active |
| SMTP | Email protocol | Tender alerts | Configurable |
| localStorage | Browser API | Theme persistence | Active (presentations) |
| Reveal.js | Framework | Presentation rendering | Embedded |
| Claude Code | Plugin system | Skill execution | Active |

---

*Integration audit: 2026-02-25*
