"""
vic_tenders_scraper.py
----------------------
Scrapes open tenders from tenders.vic.gov.au and outputs structured JSON.
Designed to run daily via cron on the Dell R740.

Usage:
    python vic_tenders_scraper.py                      # print JSON to stdout
    python vic_tenders_scraper.py --output tenders.json
    python vic_tenders_scraper.py --keywords "asset management,maintenance,rolling stock"
    python vic_tenders_scraper.py --new-only            # only tenders opened in last 24h
    python vic_tenders_scraper.py --notify email@example.com

Requirements:
    pip install cloudscraper beautifulsoup4 lxml
"""

import cloudscraper
from bs4 import BeautifulSoup
import json
import re
import time
import argparse
import smtplib
import logging
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

# ── Configuration ─────────────────────────────────────────────────────────────

BASE_URL = "https://www.tenders.vic.gov.au"
SEARCH_URL = f"{BASE_URL}/tender/search"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-AU,en;q=0.9",
    "Referer": f"{BASE_URL}/tender/search?preset=open",
}

# Keywords relevant to marcov's asset management focus
# Note: These cast a wide net for initial filtering. Scoring matrix determines actual fit.
# Keywords are grouped by priority - higher priority = more likely to be relevant.
MARCOV_KEYWORDS = [
    # HIGH PRIORITY - Core asset management terms
    "asset management",
    "asset strategy",
    "asset plan",
    "asset data",
    "asset performance",
    "asset lifecycle",
    "ISO 55001",
    "GFMAM",
    "maturity assessment",
    "asset register",
    "asset information",

    # HIGH PRIORITY - Reliability & maintenance strategy
    "reliability",
    "RCM",
    "FMEA",
    "root cause analysis",
    "maintenance strategy",
    "maintenance optimisation",
    "predictive maintenance",
    "condition monitoring",
    "condition assessment",
    "condition based maintenance",
    "criticality analysis",

    # HIGH PRIORITY - Analytics & AI for assets
    "analytics",
    "data analytics",
    "advanced analytics",
    "artificial intelligence",
    "machine learning",
    "predictive model",
    "data science",
    "decision support",

    # MEDIUM PRIORITY - Systems & data
    "CMMS",
    "EAM",
    "Maximo",
    "SAP PM",
    "data management",
    "data quality",
    "master data",

    # MEDIUM PRIORITY - Rail/rolling stock (core sector - but careful of procurement)
    "rolling stock",
    "fleet management",
    "rail",
    "tram",
    "train",
    "locomotive",

    # MEDIUM PRIORITY - Other target sectors
    "water",  # Careful: many construction tenders
    "energy",

    # LOWER PRIORITY - General advisory (high false positive rate)
    "consulting",
    "advisory",
    "strategy review",
    "business case",
    "diagnostic",
    "assessment",  # Be careful - can match "environmental assessment" etc.
]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


# ── Core scraping ──────────────────────────────────────────────────────────────

def get_session() -> cloudscraper.CloudScraper:
    """Create a cloudscraper session that bypasses Cloudflare protection."""
    session = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'darwin',
            'desktop': True
        }
    )
    session.headers.update(HEADERS)
    return session


def fetch_page(session: cloudscraper.CloudScraper, page: int = 1) -> BeautifulSoup:
    """
    Fetch a single page of open tenders.
    Page 1 is a GET; subsequent pages require posting back with the CSRF token.
    """
    if page == 1:
        resp = session.get(
            SEARCH_URL,
            params={"preset": "open"},
            timeout=30,
        )
    else:
        # Grab CSRF token from the current session (set during page 1 fetch)
        csrf = session.cookies.get("XSRF-TOKEN") or _extract_csrf(session)
        resp = session.post(
            SEARCH_URL,
            params={"preset": "open"},
            data={
                "_csrf": csrf,
                "page": str(page),
                "preset": "open",
            },
            timeout=30,
        )

    resp.raise_for_status()
    return BeautifulSoup(resp.text, "lxml")


def _extract_csrf(session: cloudscraper.CloudScraper) -> str:
    """Extract _csrf token from the stored page HTML (fallback)."""
    # Usually stored in session after page 1 fetch via hidden input
    # If needed, re-fetch page 1 and pull from form
    resp = session.get(SEARCH_URL, params={"preset": "open"}, timeout=30)
    soup = BeautifulSoup(resp.text, "lxml")
    csrf_input = soup.find("input", {"name": "_csrf"})
    return csrf_input["value"] if csrf_input else ""


def parse_total_pages(soup: BeautifulSoup) -> int:
    """Extract total page count from pagination text like 'Pages: 1 2 3'."""
    text = soup.get_text()
    match = re.search(r"Pages:\s*([\d\s]+)Records:", text)
    if match:
        page_numbers = re.findall(r"\d+", match.group(1))
        return int(page_numbers[-1]) if page_numbers else 1
    return 1


def parse_total_records(soup: BeautifulSoup) -> int:
    """Extract total record count e.g. 'Records: 1 - 25 of 69'."""
    text = soup.get_text()
    match = re.search(r"of\s+(\d+)", text)
    return int(match.group(1)) if match else 0


def parse_tenders(soup: BeautifulSoup) -> list[dict]:
    """Parse all tender rows from a results page."""
    tenders = []
    rows = soup.select("tbody tr")

    for row in rows:
        cells = row.select("td")
        if len(cells) < 3:
            continue

        # Cell 0: RFx number, status, type
        cell0_text = cells[0].get_text("\n", strip=True)
        cell0_lines = [l.strip() for l in cell0_text.split("\n") if l.strip()]

        rfx_number = cell0_lines[0] if len(cell0_lines) > 0 else ""
        status = cell0_lines[1] if len(cell0_lines) > 1 else ""
        tender_type = cell0_lines[2] if len(cell0_lines) > 2 else ""

        # Cell 1: Title, issuer, UNSPSC categories, link
        title_link = cells[1].find("a")
        title = title_link.get_text(strip=True) if title_link else ""
        detail_url = BASE_URL + title_link["href"] if title_link and title_link.get("href") else ""

        # Extract tender ID from URL
        tender_id = ""
        if detail_url:
            id_match = re.search(r"id=(\d+)", detail_url)
            tender_id = id_match.group(1) if id_match else ""

        # Issuer
        cell1_text = cells[1].get_text("\n", strip=True)
        issuer_match = re.search(r"Issued by:\s*(.+?)(?:\n|UNSPSC|$)", cell1_text)
        issuer = issuer_match.group(1).strip() if issuer_match else ""

        # UNSPSC categories
        unspsc_matches = re.findall(r"UNSPSC(?:\s+\d+)?:\s*(.+?)(?=\n|UNSPSC|$)", cell1_text)
        categories = [u.strip() for u in unspsc_matches if u.strip()]

        # Cell 2: Opened and Closing dates
        cell2_text = cells[2].get_text("\n", strip=True)
        opened_match = re.search(r"Opened\s+(.+?)(?=Closing|$)", cell2_text, re.DOTALL)
        closing_match = re.search(r"Closing\s+(.+?)$", cell2_text, re.DOTALL)

        date_opened_str = opened_match.group(1).strip() if opened_match else ""
        date_closing_str = closing_match.group(1).strip() if closing_match else ""

        tender = {
            "id": tender_id,
            "rfx_number": rfx_number,
            "status": status,
            "tender_type": tender_type,
            "title": title,
            "issuer": issuer,
            "categories": categories,
            "date_opened": date_opened_str,
            "date_closing": date_closing_str,
            "url": detail_url,
            "scraped_at": datetime.now().isoformat(),
        }
        tenders.append(tender)

    return tenders


def scrape_all_tenders(delay: float = 2.0, date_from: str = None, date_to: str = None) -> list[dict]:
    """
    Scrape all pages of open tenders and return combined list.

    Args:
        delay: Seconds to wait between page requests
        date_from: Optional opening date filter (DD/MM/YYYY format)
        date_to: Optional opening date filter (DD/MM/YYYY format)
    """
    session = get_session()
    all_tenders = []

    # Build search parameters
    params = {
        "tenderState": "OPEN",
        "groupBy": "NONE",
    }

    if date_from:
        params["openingDateFrom"] = date_from
        log.info(f"Filtering tenders opened from: {date_from}")
    if date_to:
        params["openingDateTo"] = date_to
        log.info(f"Filtering tenders opened to: {date_to}")

    if not date_from and not date_to:
        # Use preset=open for all open tenders
        params = {"preset": "open"}

    log.info("Fetching page 1 ...")
    resp = session.get(SEARCH_URL, params=params, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")

    # Store CSRF for subsequent pages
    csrf_input = soup.find("input", {"name": "_csrf"})
    if csrf_input:
        session._csrf = csrf_input["value"]

    total_pages = parse_total_pages(soup)
    total_records = parse_total_records(soup)
    log.info(f"Found {total_records} tenders across {total_pages} pages")

    all_tenders.extend(parse_tenders(soup))

    for page in range(2, total_pages + 1):
        time.sleep(delay)  # be polite
        log.info(f"Fetching page {page} of {total_pages} ...")

        # Use GET with page parameter
        page_params = {**params, "page": page}
        resp = session.get(
            SEARCH_URL,
            params=page_params,
            timeout=30,
        )
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")
        page_tenders = parse_tenders(soup)
        log.info(f"  → {len(page_tenders)} tenders parsed")
        all_tenders.extend(page_tenders)

    log.info(f"Total scraped: {len(all_tenders)} tenders")
    return all_tenders


# ── Filtering ──────────────────────────────────────────────────────────────────

def filter_by_keywords(tenders: list[dict], keywords: list[str]) -> list[dict]:
    """Return tenders where title, issuer, or categories match any keyword."""
    keywords_lower = [k.lower() for k in keywords]
    matched = []
    for t in tenders:
        searchable = " ".join([
            t.get("title", ""),
            t.get("issuer", ""),
            " ".join(t.get("categories", [])),
        ]).lower()
        matched_kws = [kw for kw in keywords_lower if kw in searchable]
        if matched_kws:
            t["matched_keywords"] = matched_kws
            matched.append(t)
    return matched


def filter_new_only(tenders: list[dict], hours: int = 24) -> list[dict]:
    """Return tenders opened within the last N hours."""
    cutoff = datetime.now() - timedelta(hours=hours)
    new = []
    for t in tenders:
        date_str = t.get("date_opened", "")
        # Parse format like "Fri, 21 February 2026 10:10 am"
        try:
            opened = datetime.strptime(date_str, "%a, %d %B %Y %I:%M %p")
            if opened >= cutoff:
                new.append(t)
        except ValueError:
            pass  # skip if can't parse
    return new


# ── Persistence (track seen tenders to detect new ones) ───────────────────────

def load_seen_ids(state_file: str) -> set:
    p = Path(state_file)
    if p.exists():
        with open(p) as f:
            return set(json.load(f))
    return set()


def save_seen_ids(ids: set, state_file: str):
    with open(state_file, "w") as f:
        json.dump(list(ids), f)


def find_genuinely_new(tenders: list[dict], state_file: str = "seen_tender_ids.json") -> list[dict]:
    """Compare against previously seen IDs to find truly new tenders."""
    seen = load_seen_ids(state_file)
    new_tenders = [t for t in tenders if t["id"] not in seen]
    all_ids = seen | {t["id"] for t in tenders}
    save_seen_ids(all_ids, state_file)
    return new_tenders


# ── Notification ───────────────────────────────────────────────────────────────

def send_email_alert(
    tenders: list[dict],
    recipient: str,
    smtp_host: str = "localhost",
    smtp_port: int = 25,
    sender: str = "noreply@marcov.com.au",
):
    """Send a plain-text email summary of matched tenders."""
    if not tenders:
        return

    subject = f"[marcov] {len(tenders)} new VIC tender{'s' if len(tenders) > 1 else ''} – {datetime.now().strftime('%d %b %Y')}"

    body_lines = [
        f"marcov Tender Alert – {datetime.now().strftime('%A, %d %B %Y')}",
        f"Found {len(tenders)} relevant open tenders on tenders.vic.gov.au",
        "=" * 60,
        "",
    ]
    for t in tenders:
        body_lines += [
            f"Title:    {t['title']}",
            f"Issuer:   {t['issuer']}",
            f"Type:     {t['tender_type']}",
            f"RFx No.:  {t['rfx_number']}",
            f"Opened:   {t['date_opened']}",
            f"Closes:   {t['date_closing']}",
            f"Keywords: {', '.join(t.get('matched_keywords', []))}",
            f"URL:      {t['url']}",
            "",
            "-" * 60,
            "",
        ]

    body = "\n".join(body_lines)

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.sendmail(sender, [recipient], msg.as_string())
        log.info(f"Email sent to {recipient}")
    except Exception as e:
        log.error(f"Email failed: {e}")
        # Fallback: print to stdout
        print("\n" + body)


# ── CLI ────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Scrape open tenders from tenders.vic.gov.au"
    )
    parser.add_argument("--output", "-o", help="Write JSON output to file")
    parser.add_argument(
        "--keywords", "-k",
        help="Comma-separated keywords to filter by (default: marcov preset)",
        default=None,
    )
    parser.add_argument(
        "--all-keywords",
        action="store_true",
        help="Use marcov's full keyword list",
    )
    parser.add_argument(
        "--new-only",
        action="store_true",
        help="Only show tenders opened in last 24h",
    )
    parser.add_argument(
        "--track-new",
        action="store_true",
        help="Use state file to detect tenders not seen before",
    )
    parser.add_argument(
        "--state-file",
        default="seen_tender_ids.json",
        help="Path to state file for --track-new (default: seen_tender_ids.json)",
    )
    parser.add_argument(
        "--notify",
        metavar="EMAIL",
        help="Send email alert to this address",
    )
    parser.add_argument(
        "--smtp-host",
        default="localhost",
        help="SMTP server host (default: localhost)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=2.0,
        help="Seconds to wait between page requests (default: 2.0)",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON output",
    )
    parser.add_argument(
        "--opened-today",
        action="store_true",
        help="Only fetch tenders opened today (uses server-side filtering)",
    )
    parser.add_argument(
        "--opened-from",
        metavar="DD/MM/YYYY",
        help="Filter tenders opened from this date (server-side)",
    )
    parser.add_argument(
        "--opened-to",
        metavar="DD/MM/YYYY",
        help="Filter tenders opened to this date (server-side)",
    )

    args = parser.parse_args()

    # Determine keywords
    keywords = None
    if args.keywords:
        keywords = [k.strip() for k in args.keywords.split(",")]
    elif args.all_keywords:
        keywords = MARCOV_KEYWORDS

    # Determine date filtering
    date_from = None
    date_to = None
    if args.opened_today:
        today = datetime.now().strftime("%d/%m/%Y")
        date_from = today
        date_to = today
    elif args.opened_from or args.opened_to:
        date_from = args.opened_from
        date_to = args.opened_to

    # Scrape
    tenders = scrape_all_tenders(delay=args.delay, date_from=date_from, date_to=date_to)

    # Apply filters
    if args.new_only:
        tenders = filter_new_only(tenders, hours=24)
        log.info(f"After --new-only filter: {len(tenders)} tenders")

    if args.track_new:
        tenders = find_genuinely_new(tenders, state_file=args.state_file)
        log.info(f"After --track-new filter: {len(tenders)} new tenders")

    if keywords:
        tenders = filter_by_keywords(tenders, keywords)
        log.info(f"After keyword filter: {len(tenders)} tenders")

    # Output
    indent = 2 if args.pretty else None
    output_json = json.dumps(tenders, indent=indent, ensure_ascii=False)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output_json)
        log.info(f"Wrote {len(tenders)} tenders to {args.output}")
    else:
        print(output_json)

    # Notify
    if args.notify and tenders:
        send_email_alert(tenders, recipient=args.notify, smtp_host=args.smtp_host)

    return 0


if __name__ == "__main__":
    exit(main())
