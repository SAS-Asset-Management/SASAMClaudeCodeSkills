"""Export the executive summary to PDF.

CLI:
  python3 exportPdf.py --repo <engagementRoot>

Captures <repo>/deliverable/summary.html to <repo>/deliverable/summary.pdf.

Two capture paths, tried in order:

1. Playwright (preferred, the only permitted third party dependency in
   the whole plugin, and only in this file). Loads the file URL, waits
   for network idle, then polls until every .plot-container has
   rendered children before printing A4 with margins and a page number
   footer. Install with:
     pip install playwright && playwright install chromium

2. Headless Chromium CLI fallback. Probes common binary locations and
   invokes:
     <chrome> --headless=new --disable-gpu --print-to-pdf=<out>
              --no-pdf-header-footer --virtual-time-budget=30000 <fileUrl>
   The virtual time budget gives Plotly up to 30 seconds to render the
   charts before capture. This path has no explicit render poll, so
   verify the plots are not blank rectangles after export.

When neither path is available the export degrades gracefully with an
actionable message rather than a stack trace.
"""

import argparse
import os
import shutil
import subprocess
import sys

CHROMIUM_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome",
    "chromium",
    "chromium-browser",
]

WAIT_FOR_PLOTS = (
    "Array.from(document.querySelectorAll('.plot-container'))"
    ".every(el => el.children.length > 0)"
)

FOOTER_TEMPLATE = (
    '<div style="font-size:9px; width:100%; text-align:center; '
    'color:#6b7588;">Maturity Assessment '
    '<span class="pageNumber"></span> / <span class="totalPages"></span>'
    "</div>"
)


def exportWithPlaywright(htmlPath, pdfPath):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.goto("file://{}".format(htmlPath), wait_until="networkidle")
        page.wait_for_function(WAIT_FOR_PLOTS, timeout=30000)
        page.emulate_media(media="print")
        page.pdf(
            path=pdfPath,
            format="A4",
            margin={
                "top": "22mm",
                "right": "18mm",
                "bottom": "22mm",
                "left": "18mm",
            },
            print_background=True,
            display_header_footer=True,
            footer_template=FOOTER_TEMPLATE,
            header_template="<div></div>",
        )
        browser.close()


def findChromium():
    for candidate in CHROMIUM_CANDIDATES:
        if os.path.isabs(candidate):
            if os.path.isfile(candidate):
                return candidate
        else:
            resolved = shutil.which(candidate)
            if resolved:
                return resolved
    return None


def exportWithChromiumCli(binary, htmlPath, pdfPath):
    command = [
        binary,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--print-to-pdf={}".format(pdfPath),
        "--virtual-time-budget=30000",
        "file://{}".format(htmlPath),
    ]
    subprocess.run(command, check=True, capture_output=True)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Capture summary.html to summary.pdf via headless Chromium."
    )
    parser.add_argument("--repo", required=True, help="Engagement repo root")
    args = parser.parse_args(argv)

    repoRoot = os.path.abspath(args.repo)
    htmlPath = os.path.join(repoRoot, "deliverable", "summary.html")
    pdfPath = os.path.join(repoRoot, "deliverable", "summary.pdf")

    if not os.path.isfile(htmlPath):
        print(
            "ERROR: {} not found. Run buildDashboard.py first:\n"
            "  python3 buildDashboard.py --repo {}".format(htmlPath, repoRoot),
            file=sys.stderr,
        )
        return 1

    try:
        exportWithPlaywright(htmlPath, pdfPath)
        print("Wrote {} (Playwright capture).".format(pdfPath))
        return 0
    except ImportError:
        pass
    except Exception as error:
        print(
            "Playwright capture failed ({}); trying the Chromium CLI "
            "fallback.".format(error),
            file=sys.stderr,
        )

    binary = findChromium()
    if binary:
        try:
            exportWithChromiumCli(binary, htmlPath, pdfPath)
            print("Wrote {} (headless Chromium CLI capture).".format(pdfPath))
            print(
                "Note: the CLI path has no render poll — open the PDF and "
                "confirm no plot is a blank rectangle."
            )
            return 0
        except subprocess.CalledProcessError as error:
            print(
                "Chromium CLI capture failed (exit {}).".format(error.returncode),
                file=sys.stderr,
            )

    print(
        "ERROR: no PDF capture path is available. Install one of:\n"
        "  1. Playwright (preferred): pip install playwright && "
        "playwright install chromium\n"
        "  2. Google Chrome or Chromium on PATH (probed: {}).".format(
            ", ".join(CHROMIUM_CANDIDATES)
        ),
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
