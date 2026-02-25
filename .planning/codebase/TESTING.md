# Testing Patterns

**Analysis Date:** 2026-02-25

## Test Framework

**Status:** Not detected

**Runner:**
- No test runner configuration found (no `pytest.ini`, `jest.config.*`, `vitest.config.*`)
- No test framework imports detected in codebase

**Assertion Library:**
- No assertion library in use (no unittest, pytest, or similar)

**Test Execution:**
- No test scripts in `package.json` or `setup.py`
- No automated test execution configured

**Run Commands:**
- Not applicable - no test suite currently exists

## Test File Organization

**Location:**
- No test files detected in codebase
- No `tests/` directory structure
- No `*.test.py` or `*.spec.py` files found

**Naming:**
- Not applicable

**Structure:**
- Not applicable

## Testing Status

**Current Approach:**
The codebase has zero automated test coverage. Functions are currently tested only through manual/CLI execution.

**Manual Testing Evidence:**
Module docstrings include CLI usage examples showing how to manually test:

From `vic_tenders_scraper.py` (lines 7-12):
```
Usage:
    python vic_tenders_scraper.py                      # print JSON to stdout
    python vic_tenders_scraper.py --output tenders.json
    python vic_tenders_scraper.py --keywords "asset management,maintenance,rolling stock"
    python vic_tenders_scraper.py --new-only            # only tenders opened in last 24h
    python vic_tenders_scraper.py --notify email@example.com
```

From `assess_tenders.py` (lines 8-11):
```
Usage:
    python assess_tenders.py                          # All open tenders
    python assess_tenders.py --opened-today           # Today's new tenders only
    python assess_tenders.py --output assessment.json # Save to file
    python assess_tenders.py --pretty                 # Pretty-print output
```

## Code Designed for Manual Testing

The codebase is structured to be manually testable:

**CLI Arguments:** Both modules have extensive argument parsing allowing different execution modes:
- `vic_tenders_scraper.py`: `--keywords`, `--new-only`, `--track-new`, `--notify`, `--pretty`, `--opened-today`, etc.
- `assess_tenders.py`: `--output`, `--pretty`, `--opened-today`, `--opened-from`, `--opened-to`, `--no-keywords`

**Logging Output:** Structured logging allows visibility into execution:
```python
log.info("Starting tender assessment...")
log.info(f"Scraped {total_scraped} tenders")
log.info(f"After keyword filter: {len(tenders)} tenders")
log.info(f"Assessment complete. Shortlisted: {summary['shortlisted']}, Review: {summary['flagged_for_review']}")
```

**JSON Output:** Both modules output JSON that can be validated:
```python
output_json = json.dumps(result, indent=indent, ensure_ascii=False, default=str)
if args.output:
    with open(args.output, 'w') as f:
        f.write(output_json)
```

## Testable Functions

Functions are designed with testability in mind, even without a test framework:

**Pure Functions (Stateless):**
- `score_tender(tender: dict) -> dict` - Takes dict, returns score dict with no side effects
- `analyze_tender(tender: dict, scoring: dict) -> dict` - Deterministic analysis
- `generate_shortlist_details(tender: dict, scoring: dict) -> dict` - Deterministic detail generation
- `calculate_statistics(tenders: list, assessments: list) -> dict` - Aggregation function
- `parse_tenders(soup: BeautifulSoup) -> list[dict]` - Parsing only, no mutations
- `filter_by_keywords(tenders: list[dict], keywords: list[str]) -> list[dict]` - Pure filter
- `filter_new_only(tenders: list[dict], hours: int = 24) -> list[dict]` - Pure filter with date logic

**Functions with I/O (Side effects):**
- `scrape_all_tenders(delay: float, date_from: str, date_to: str) -> list[dict]` - Network I/O
- `send_email_alert(tenders: list[dict], recipient: str, ...) -> None` - Email I/O
- `load_seen_ids(state_file: str) -> set` - File I/O
- `save_seen_ids(ids: set, state_file: str) -> None` - File I/O

## Recommended Test Strategy

### Unit Test Targets

**High Priority - Pure Functions:**
1. `score_tender()` - Test scoring logic, auto-decline patterns, point calculations
2. `analyze_tender()` - Test urgency classification, fit summary generation
3. `filter_by_keywords()` - Test keyword matching, case sensitivity
4. `calculate_statistics()` - Test aggregation, distribution binning
5. `parse_tenders()` - Test HTML parsing with various tender formats

**Medium Priority - Parsing:**
- `parse_total_pages()` - Regex pattern extraction
- `parse_total_records()` - Regex pattern extraction
- `filter_new_only()` - Date comparison logic

**Low Priority - I/O:**
- `load_seen_ids()` / `save_seen_ids()` - File round-trip only
- `send_email_alert()` - Would require mock SMTP

### Test Data Strategy

**Fixtures Needed:**
1. Sample tender dictionaries (minimum viable tender object):
```python
{
    'title': 'Asset Management Strategy Review',
    'issuer': 'Metro Trains Melbourne',
    'tender_type': 'Request for Proposal',
    'date_closing': 'Wed, 11 March 2026 2:00 pm',
    'categories': ['Asset Management'],
    'url': 'https://tenders.vic.gov.au/tender/detail?id=12345',
}
```

2. BeautifulSoup HTML fixtures for parser testing
3. Scoring matrix test cases (edge cases for boundary conditions)

### Framework Recommendation

**pytest** is recommended for test adoption:
- Already implicit in Python standards
- Fixture support for complex test data
- Parameterization for testing multiple scoring cases
- Plugin ecosystem for coverage reporting

**Minimum Test Setup:**
```bash
pip install pytest pytest-cov
pytest tests/ --cov=. --cov-report=html
```

## Test Coverage Gaps

**Currently Untested:**
- All `score_tender()` logic (most critical business logic)
- All `analyze_tender()` logic
- Date parsing with various formats
- HTML parsing from tenders.vic.gov.au
- Keyword filtering logic
- Statistics aggregation
- CLI argument parsing and orchestration

**Critical Gaps:**
- No validation of scoring dimension calculations
- No verification of auto-decline patterns
- No regression tests for tender scraping changes
- No error handling validation (except graceful fallbacks)

**Risk Areas:**
- `score_tender()` has 100+ lines of scoring logic with no test validation
- Regex patterns in `vic_tenders_scraper.py` for date/page parsing are untested
- Multiple hardcoded keyword lists and tier client lists have no validation

---

*Testing analysis: 2026-02-25*
