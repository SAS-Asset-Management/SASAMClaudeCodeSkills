# Deliverable pipeline

The canonical deliverable is an interactive self contained HTML dashboard plus a PDF executive summary, both rendered from the engagement's `scoreLedger.json`. One source of truth, two surfaces. No number is synthesised — everything binds to the ledger or is omitted.

```
scoreLedger.json ──▶ reportGate.py (open or DRAFT)
                 ──▶ buildDashboard.py ──▶ deliverable/dashboard.html
                                       ──▶ deliverable/summary.html
                 ──▶ exportPdf.py      ──▶ deliverable/summary.pdf
```

## CLI invocations

All paths are engagement relative; `<root>` is the engagement repo root.

```bash
# 1. Check the gate (exit 0 when open, 1 when closed, reasons listed)
python3 reportGate.py --repo <root>

# 2. Render both HTML surfaces into <root>/deliverable/
python3 buildDashboard.py --repo <root>

# 3. Capture summary.html to summary.pdf (Playwright preferred,
#    headless Chromium CLI fallback)
python3 exportPdf.py --repo <root>
```

## The report gate

`reportGate.evaluateGate(ledger, pack) -> {"open": bool, "reasons": [str]}`. The gate opens only when every taxonomy subject has a non null `final.score`, every subject with a say or do score has both set, and no dispute has status `open`. A closed gate stamps a fixed position DRAFT banner (listing every reason) on both surfaces — the render still completes, but it is visibly not the deliverable of record.

## Surfaces

- **dashboard.html** — header with brand tokens from `engagement.yaml`, a KPI strip (overall mean, subjects scored N of M, flags, open disputes), the four catalogue plots, and a per subject drill down table (score, confidence, CI, tag mix, evidence artefacts, history). Displayed dates are DD/MM/YYYY; the ledger keeps ISO 8601 at rest.
- **summary.html** — print oriented: document control, headline maturity position, domain narrative bound from section writer drafts at `<root>/deliverable/draft/NN_*.md` when present, flagged outlier subjects auto surfaced from ledger flags, key findings with say versus do provenance, and an improvement roadmap placeholder.

Both surfaces inline all CSS (templates/reportStyles.css), all JS, the vendored Plotly bundle, and the ledger as an inline JSON script tag. No `fetch()`, no CDN reference at runtime — they open offline from `file://`.

## Plots

The closed catalogue lives at `plotCatalogue.md` — exactly four plots (domainRadar, subjectConfidence, runTrend, peerPercentile) with fixed render function names enforced by the `plotBlocker` hook. A plot not in the catalogue does not belong in any deliverable.

## The vendor step

Plotly is vendored at `vendor/plotly.min.js` (see `vendor/README.md` for the exact version, licence, and fetch command). If the file is missing, `buildDashboard.py` fails loudly and quotes the fetch command — it never falls back to a CDN.

## Benchmark input (opt in)

`<root>/deliverable/benchmark.json`, shaped:

```json
{
  "<subjectId>": { "p25": 1.5, "p50": 2.5, "p75": 3.5, "cohortSize": 14 }
}
```

When present, the peerPercentile plot renders each subject against its cohort percentiles. When absent, the plot is omitted entirely — never faked. Cohort data exists only because engagements opt in: only de identified, homogenised subject scores ever leave an engagement for the benchmark store, and only when the engagement sets `deliverable.benchmark: cohort` in `engagement.yaml`. Raw evidence never leaves the engagement repo.

## PDF export

`exportPdf.py` prefers Playwright (the only permitted third party dependency in the whole plugin, and only in that file): file URL, `networkidle`, then a poll that every `.plot-container` has rendered children, then A4 with margins and a page number footer. The fallback invokes a headless Chromium binary directly (`--headless=new --print-to-pdf --virtual-time-budget=30000`, probing the macOS Google Chrome path, `google-chrome`, then `chromium`). When neither is available it prints an actionable install message.

## Tests

See `tests/README.md`. Run with:

```bash
python3 -m pytest deliverable/tests -q --import-mode=importlib
```
