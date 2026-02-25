# Technology Stack

**Analysis Date:** 2026-02-25

## Languages

**Primary:**
- Python 3 - Data processing, web scraping, and tender assessment utilities
- HTML5 - Presentation generation and web-based reports
- JavaScript - Client-side interactions, theme switching, Reveal.js integration
- CSS3 - Styling for presentations and reports
- Markdown - Skill definitions and documentation

**Secondary:**
- Bash - Setup scripts, command registration, git hooks
- JSON - Configuration, state management, data serialization
- YAML - Skill frontmatter metadata

## Runtime

**Environment:**
- Python 3.x (required for `vic_tenders_scraper.py` and `assess_tenders.py`)
- Modern web browser (for HTML presentation playback and report viewing)
- Node.js ecosystem (for Claude Code plugin system integration)

**Package Manager:**
- pip (Python package management)
- No lockfile detected - uses `requirements.txt` approach
- No npm/Node dependencies required for skills themselves

## Frameworks

**Core:**
- Claude Code Plugin System - Skill registration and execution framework
- Reveal.js - HTML-based presentation framework with themes and transitions
- BeautifulSoup4 - HTML/XML parsing for web scraping
- Cloudscraper - Cloudflare anti-bot bypass for web scraping

**Build/Dev:**
- Bash scripts for setup and registration
- Git hooks for automatic command registration
- No traditional build system (static HTML/CSS output)

## Key Dependencies

**Critical:**
- `cloudscraper` - Bypasses Cloudflare protection on tenders.vic.gov.au
- `beautifulsoup4` - Parses HTML tender pages from Victorian tenders portal
- `lxml` - HTML/XML parsing backend for BeautifulSoup

**Infrastructure:**
- `smtplib` (stdlib) - Email notifications for tender alerts
- `json` (stdlib) - Data serialization for assessments and tenders
- `logging` (stdlib) - Application logging
- `datetime` (stdlib) - Date/time handling for tender date filtering
- `pathlib` (stdlib) - File system operations
- `argparse` (stdlib) - CLI argument parsing

## Configuration

**Environment:**
- SMTP configuration (host, port) for email notifications - defaults to `localhost:25`
- Email sender address: `noreply@marcov.com.au` (configurable via `--notify` flag)
- No environment variables detected in exploration (no .env files present)

**Build:**
- No build configuration files (`webpack.config`, `tsconfig.json`, etc.)
- Reveal.js and assets embedded directly in generated HTML
- Python CLI tools use standard argparse configuration

## Python Dependencies

Based on `vic_tenders_scraper.py` imports:

```
cloudscraper       # Cloudflare bypass for scraping
beautifulsoup4     # HTML parsing
lxml               # XML/HTML backend
```

No `requirements.txt` file detected in repository, but usage indicates these three packages are essential.

## Platform Requirements

**Development:**
- Git (for version control and hook registration)
- Python 3.x installation
- Bash shell (for setup scripts)
- Read/write access to `~/.claude/commands/` directory for command registration

**Production:**
- Python 3.x runtime with pip-installed dependencies
- Network access to:
  - `https://www.tenders.vic.gov.au` (web scraping target)
  - SMTP server (for email notifications)
- Write access to local filesystem for state files (`seen_tender_ids.json`, `.beam/` directory)

## Deployment

**Skills Distribution:**
- Skills deployed as Claude Code plugins via `~/.claude/commands/` directory
- Each skill includes SKILL.md (Markdown with YAML frontmatter)
- Supporting files (`references/`, generated HTML reports) referenced with absolute paths
- Git-based auto-registration via post-checkout and post-merge hooks

**Installation:**
- Setup via `setup.sh` script:
  1. Installs git hooks to `.git/hooks/`
  2. Registers all SKILL.md files as slash commands
  3. Generates command files in `~/.claude/commands/`
- Manual re-registration via `register-commands.sh`

## Storage

**Local State:**
- `.beam/` hidden directory - Stores engagement state for beam-selling skill (JSON format)
- `seen_tender_ids.json` - Tracks previously scraped tender IDs for deduplication
- No database required

**Session Persistence:**
- HTML presentations use localStorage for theme preference (light/dark mode)
- Command state persisted across Claude Code sessions via local `.beam/` files

## Monitoring

**Logging:**
- Python standard `logging` module with configurable levels
- Log format: `%(asctime)s %(levelname)s %(message)s`
- Outputs to stdout/stderr by default

**Email Alerts:**
- SMTP-based tender notifications sent to specified email address
- Configurable SMTP host (default: localhost)
- Fallback to stdout if SMTP fails

---

*Stack analysis: 2026-02-25*
