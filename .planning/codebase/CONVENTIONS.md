# Coding Conventions

**Analysis Date:** 2026-02-25

## Naming Patterns

**Files:**
- lowercase_with_underscores format for Python modules (e.g., `vic_tenders_scraper.py`, `assess_tenders.py`)
- Files are descriptive of their purpose

**Functions:**
- snake_case naming convention (e.g., `score_tender()`, `parse_tenders()`, `filter_by_keywords()`)
- Private/internal functions prefixed with underscore (e.g., `_extract_csrf()`)
- Clear, descriptive names that indicate purpose

**Variables:**
- snake_case naming (e.g., `total_scraped`, `date_closing`, `domain_score`)
- Dictionary keys use snake_case (e.g., `date_opened`, `tender_type`, `auto_decline_reason`)
- Constants use UPPER_CASE (e.g., `SCORING_VERSION`, `MARCOV_KEYWORDS`, `AUTO_DECLINE_TITLE`)

**Types:**
- Type hints used sparingly but consistently when present (e.g., `def get_session() -> cloudscraper.CloudScraper:`)
- Return type annotations on complex functions (e.g., `-> dict`, `-> list[dict]`, `-> int`)

## Code Style

**Formatting:**
- No explicit formatter configuration detected (no `.prettierrc`, `black` config, or `pyproject.toml`)
- Follows PEP 8 style implicitly with 4-space indentation
- Line length appears pragmatic, not strictly enforced (up to ~100+ characters observed)
- Blank lines separate logical sections within functions

**Linting:**
- No linting configuration detected (no `.eslintrc`, `.flake8`, or `pyproject.toml`)
- Code follows general Python best practices by convention

## Import Organization

**Order:**
1. Standard library imports (e.g., `json`, `re`, `argparse`, `logging`, `datetime`)
2. Standard library submodule imports (e.g., `from datetime import datetime, timedelta`)
3. Third-party library imports (e.g., `cloudscraper`, `BeautifulSoup`)
4. Local/relative imports (e.g., `from vic_tenders_scraper import ...`)

**Path Aliases:**
- No path aliases detected; direct module imports from same directory
- Relative imports used for inter-module dependencies

**Example from `assess_tenders.py`:**
```python
import json
import re
import argparse
import logging
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path

from vic_tenders_scraper import (
    scrape_all_tenders,
    filter_by_keywords,
    MARCOV_KEYWORDS,
)
```

## Error Handling

**Patterns:**
- try/except blocks used for date parsing with graceful fallback (line 294 in `assess_tenders.py`):
```python
try:
    closing = datetime.strptime(closing_str, "%a, %d %B %Y %I:%M %p")
    days = (closing - datetime.now()).days
    analysis['days_until_closing'] = days
    # ...
except ValueError:
    pass  # Gracefully skip invalid dates
```

- Exception suppression with `pass` for non-critical parsing (lines 356-357 in `vic_tenders_scraper.py`):
```python
try:
    opened = datetime.strptime(date_str, "%a, %d %B %Y %I:%M %p")
    if opened >= cutoff:
        new.append(t)
except ValueError:
    pass  # skip if can't parse
```

- HTTP error handling with `raise_for_status()` (line 165 in `vic_tenders_scraper.py`):
```python
resp.raise_for_status()
```

- Exception catching with fallback in email sending (lines 429-436 in `vic_tenders_scraper.py`):
```python
try:
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.sendmail(sender, [recipient], msg.as_string())
    log.info(f"Email sent to {recipient}")
except Exception as e:
    log.error(f"Email failed: {e}")
    print("\n" + body)  # Fallback to stdout
```

## Logging

**Framework:** Python's built-in `logging` module

**Configuration:**
```python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)
```

**Patterns:**
- Centralized logging setup in each module at module level
- Logger retrieved with `log = logging.getLogger(__name__)`
- Used for progress tracking: `log.info("Fetching page 1 ...")`
- Used for status summary: `log.info(f"Assessment complete. Shortlisted: {summary['shortlisted']}")`
- Used for error reporting: `log.error(f"Email failed: {e}")`
- Timestamps format: `"%Y-%m-%d %H:%M:%S"` (e.g., "2026-02-25 14:30:45")

## Comments

**When to Comment:**
- Docstring at module level explaining purpose, usage, and requirements (both files start with multi-line docstrings)
- Function-level docstrings for complex functions describing purpose and arguments
- Inline comments sparingly, using visual separators for logical sections

**Docstring Style:**
- Triple-quoted docstrings immediately following function definition
- Includes description and argument documentation when helpful
- Example from `score_tender()` (line 97-101):
```python
def score_tender(tender: dict) -> dict:
    """
    Score a tender against the alignment matrix.
    Returns full scoring breakdown with rationale.
    """
```

- Detailed usage docstrings at module level
- Example from `vic_tenders_scraper.py` (lines 1-16):
```python
"""
vic_tenders_scraper.py
----------------------
Scrapes open tenders from tenders.vic.gov.au and outputs structured JSON.
Designed to run daily via cron on the Dell R740.

Usage:
    python vic_tenders_scraper.py                      # print JSON to stdout
    python vic_tenders_scraper.py --output tenders.json
    ...
"""
```

**Section Headers:**
- Visual ASCII separators for major code sections (e.g., `# ── Scoring Configuration ──────`)
- Consistent dashing style to mark logical boundaries

## Function Design

**Size:** Functions vary from simple 3-5 line utilities to 40+ line orchestrators
- Helper functions kept focused on single responsibility
- Main orchestrators like `run_assessment()` are longer but well-sectioned

**Parameters:**
- Typically 1-3 required parameters; optional parameters use defaults
- Example: `scrape_all_tenders(delay: float = 2.0, date_from: str = None, date_to: str = None)`
- Dictionaries passed for complex object types rather than multiple params

**Return Values:**
- Consistent return types per function
- Score/assessment functions return `dict` with structured fields
- Filter/parse functions return `list[dict]`
- Stateless functions (pure) preferred where possible
- Functions that mutate state (e.g., file writing) are clearly named and documented

## Module Design

**Exports:**
- Functions intended for import are at module level without underscore prefix
- Main orchestrators (`run_assessment()`, `scrape_all_tenders()`) are public
- Helper utilities (`_extract_csrf()`) prefixed with underscore
- Constants exported at module level (e.g., `MARCOV_KEYWORDS`, `SCORING_VERSION`)

**Barrel Files:**
- Not used; direct imports from specific modules
- Cross-module imports explicit: `from vic_tenders_scraper import (...)`

**Main Entry Point:**
- Standard `if __name__ == "__main__":` pattern for CLI execution
- `main()` function handles argument parsing and orchestration
- Returns exit code (0 for success)

---

*Convention analysis: 2026-02-25*
