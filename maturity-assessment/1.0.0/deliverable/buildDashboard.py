"""Build the maturity assessment deliverable surfaces from the score ledger.

CLI:
  python3 buildDashboard.py --repo <engagementRoot>

Reads engagement.yaml, the resolved pack, scoreLedger.json, and the
optional <repo>/deliverable/benchmark.json, then renders TWO fully self
contained HTML files into <repo>/deliverable/:

  dashboard.html — the interactive scorecard (KPI strip, the four
                   catalogue plots, per subject drill down table)
  summary.html   — the print oriented executive summary (document
                   control, headline, domain narrative, flagged
                   outliers, key findings, roadmap placeholder)

One source of truth: every number binds to the ledger or is omitted.
Nothing is synthesised. Plotly is inlined from vendor/plotly.min.js —
the build fails loudly if the vendor file is missing. No fetch(), no
CDN URL at runtime; both surfaces work offline from file://.

The report gate (reportGate.evaluateGate) decides whether a fixed
position DRAFT banner is stamped on both surfaces.
"""

import argparse
import html
import importlib.util
import json
import os
import re
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))

FOOTER_TAGLINE = (
    "SAS Asset Management — we provide advanced analytics, expert asset "
    "management services and maturity assessments to help asset owners "
    "realise their value."
)

VENDOR_FETCH_COMMAND = (
    "curl -sfo vendor/plotly.min.js https://cdn.plot.ly/plotly-2.35.3.min.js"
)

RAMP = [(0.0, "#B83232"), (2.0, "#D99424"), (4.0, "#69BE28"), (5.0, "#4F8B1D")]


# ── module loading ───────────────────────────────────────────────────

def _loadModule(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _pluginRoot():
    return os.environ.get("CLAUDE_PLUGIN_ROOT") or os.path.dirname(HERE)


def _loadConfigLoader():
    loaderPath = os.path.join(_pluginRoot(), "engine", "configLoader.py")
    if not os.path.isfile(loaderPath):
        raise FileNotFoundError(
            "engine configLoader not found at {}".format(loaderPath)
        )
    return _loadModule("configLoader", loaderPath)


def _loadReportGate():
    return _loadModule("reportGate", os.path.join(HERE, "reportGate.py"))


# ── small helpers ────────────────────────────────────────────────────

def isoToDisplay(value):
    """ISO 8601 (YYYY-MM-DD) to display format DD/MM/YYYY."""
    text = str(value)
    match = re.match(r"^(\d{4})-(\d{2})-(\d{2})", text)
    if not match:
        return text
    return "{}/{}/{}".format(match.group(3), match.group(2), match.group(1))


def rampColour(score):
    if score is None:
        return "#9AA4B2"

    def channel(hexColour, i):
        return int(hexColour[i:i + 2], 16)

    def mix(a, b, t):
        parts = []
        for i in (1, 3, 5):
            parts.append(
                "{:02x}".format(
                    round(channel(a, i) + (channel(b, i) - channel(a, i)) * t)
                )
            )
        return "#" + "".join(parts)

    s = max(0.0, min(5.0, float(score)))
    for i in range(len(RAMP) - 1):
        lo, hi = RAMP[i], RAMP[i + 1]
        if s <= hi[0]:
            return mix(lo[1], hi[1], (s - lo[0]) / (hi[0] - lo[0]))
    return RAMP[-1][1]


def subjectDisplayName(subjectId):
    number, _, raw = subjectId.partition("_")
    words = re.sub(r"([A-Z])", r" \1", raw).lower().strip()
    return "{} {}".format(number, words.capitalize()) if words else subjectId


def escape(value):
    return html.escape(str(value), quote=True)


def taxonomySubjects(pack):
    subjects = []
    for domain in (pack.get("taxonomy", {}) or {}).get("domains", []) or []:
        subjects.extend(domain.get("subjects", []) or [])
    return subjects


def markdownToHtml(text):
    """Minimal markdown rendering for section drafts: headings, lists,
    paragraphs. Content is escaped; no raw HTML passes through."""
    lines = text.splitlines()
    out = []
    inList = False
    paragraph = []

    def flushParagraph():
        if paragraph:
            out.append("<p>{}</p>".format(" ".join(paragraph)))
            del paragraph[:]

    def closeList():
        nonlocal inList
        if inList:
            out.append("</ul>")
            inList = False

    for line in lines:
        stripped = line.strip()
        heading = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if heading:
            flushParagraph()
            closeList()
            level = min(len(heading.group(1)) + 2, 4)
            out.append(
                "<h{0}>{1}</h{0}>".format(level, escape(heading.group(2)))
            )
        elif stripped.startswith("- "):
            flushParagraph()
            if not inList:
                out.append("<ul>")
                inList = True
            out.append("<li>{}</li>".format(escape(stripped[2:])))
        elif stripped == "":
            flushParagraph()
            closeList()
        else:
            closeList()
            paragraph.append(escape(stripped))
    flushParagraph()
    closeList()
    return "\n".join(out)


# ── HTML fragments ───────────────────────────────────────────────────

def buildDraftBadge(gate):
    if gate["open"]:
        return "", ""
    items = "".join(
        "<li>{}</li>".format(escape(reason)) for reason in gate["reasons"]
    )
    badge = (
        '<div class="draft-badge" role="alert"><strong>Draft</strong>'
        "The report gate is closed — this render is not the deliverable "
        "of record.<ul>{}</ul></div>"
        '<div class="draft-spacer"></div>'
    ).format(items)
    return badge, "has-draft-badge"


def kpiCard(value, label):
    return (
        '<div class="kpi-card"><div class="kpi-value">{}</div>'
        '<div class="kpi-label">{}</div></div>'
    ).format(escape(value), escape(label))


def buildKpiStrip(ledger, pack):
    subjects = ledger.get("subjects", {}) or {}
    taxonomy = taxonomySubjects(pack)
    finals = [
        rec.get("final", {}).get("score")
        for rec in subjects.values()
        if rec.get("final", {}).get("score") is not None
    ]
    overall = "{:.1f}".format(sum(finals) / len(finals)) if finals else "—"
    scored = sum(
        1
        for sid in taxonomy
        if (subjects.get(sid) or {}).get("final", {}).get("score") is not None
    )
    flags = sum(1 for rec in subjects.values() if rec.get("flag"))
    openDisputes = sum(
        1
        for rec in subjects.values()
        for dispute in rec.get("disputes", []) or []
        if dispute.get("status") == "open"
    )
    return "\n".join(
        [
            kpiCard(overall, "Overall mean score"),
            kpiCard("{} of {}".format(scored, len(taxonomy)), "Subjects scored"),
            kpiCard(flags, "Flagged outliers"),
            kpiCard(openDisputes, "Open disputes"),
        ]
    )


def buildSubjectTable(ledger, pack):
    subjects = ledger.get("subjects", {}) or {}
    order = taxonomySubjects(pack)
    for sid in sorted(subjects):
        if sid not in order:
            order.append(sid)

    rows = []
    for sid in order:
        rec = subjects.get(sid)
        if rec is None:
            rows.append(
                "<tr><td>{}</td><td colspan=\"7\"><em>Not yet in the "
                "ledger</em></td></tr>".format(escape(subjectDisplayName(sid)))
            )
            continue
        final = rec.get("final", {}) or {}
        score = final.get("score")
        confidence = final.get("confidence")
        ci = final.get("ci")
        scoreCell = (
            '<span class="score-chip conf-{}" style="background:{}">{}</span>'.format(
                escape(confidence or "Medium"), rampColour(score), escape(score)
            )
            if score is not None
            else "—"
        )
        ciCell = (
            "[{:.1f}, {:.1f}]".format(ci[0], ci[1]) if ci else "—"
        )
        tagCounts = {"Direct": 0, "Indirect": 0, "None": 0}
        artefacts = []
        for evidence in rec.get("evidence", []) or []:
            tag = evidence.get("tag")
            if tag in tagCounts:
                tagCounts[tag] += 1
            artefact = evidence.get("artefact")
            if artefact and artefact not in artefacts:
                artefacts.append(artefact)
        tagMix = "D {Direct} · I {Indirect} · N {None}".format(**tagCounts)
        artefactList = (
            "<ul class=\"evidence-list\">{}</ul>".format(
                "".join("<li>{}</li>".format(escape(a)) for a in artefacts)
            )
            if artefacts
            else "—"
        )
        historyBits = [
            "run {}: {} ({})".format(
                escape(h.get("run")), escape(h.get("score")),
                escape(h.get("driver", ""))
            )
            for h in rec.get("history", []) or []
        ]
        historyCell = (
            '<div class="history-note">{}</div>'.format("<br>".join(historyBits))
            if historyBits
            else "—"
        )
        flagCell = (
            '<span class="flag-pill">{}</span>'.format(escape(rec["flag"]))
            if rec.get("flag")
            else ""
        )
        rows.append(
            "<tr><td>{name} {flag}</td><td>{score}</td><td>{conf}</td>"
            "<td>{ci}</td><td>{tags}</td><td>{artefacts}</td>"
            "<td>{history}</td></tr>".format(
                name=escape(subjectDisplayName(sid)),
                flag=flagCell,
                score=scoreCell,
                conf=escape(confidence or "—"),
                ci=escape(ciCell),
                tags=escape(tagMix),
                artefacts=artefactList,
                history=historyCell,
            )
        )

    return (
        '<table class="subject-table">'
        "<thead><tr><th>Subject</th><th>Score</th><th>Confidence</th>"
        "<th>95% CI</th><th>Tag mix</th><th>Evidence artefacts</th>"
        "<th>History</th></tr></thead><tbody>{}</tbody></table>"
    ).format("".join(rows))


def buildDocumentControl(engagement, ledger, pack, gate, buildDate):
    eng = engagement.get("engagement", {}) or {}
    runs = ledger.get("runs", []) or []
    lastRun = runs[-1] if runs else None
    rows = [
        ("Client", eng.get("client", "—")),
        ("Engagement code", eng.get("code", "—")),
        ("Independent reviewer", eng.get("reviewer", "—")),
        ("Commenced", isoToDisplay(eng.get("start", "—"))),
        ("Framework pack", "{} v{}".format(pack.get("title", pack.get("id", "—")), pack.get("version", "—"))),
        ("Scale", ledger.get("scale", "—")),
        ("Scoring runs", len(runs)),
        (
            "Latest run",
            "run {} on {}".format(lastRun.get("run"), isoToDisplay(lastRun.get("date")))
            if lastRun
            else "—",
        ),
        ("Rendered", buildDate),
        ("Status", "Final" if gate["open"] else "DRAFT — report gate closed"),
    ]
    body = "".join(
        "<tr><th>{}</th><td>{}</td></tr>".format(escape(k), escape(v))
        for k, v in rows
    )
    return "<table><tbody>{}</tbody></table>".format(body)


def buildHeadline(ledger, pack):
    subjects = ledger.get("subjects", {}) or {}
    taxonomy = taxonomySubjects(pack)
    finals = [
        rec.get("final", {}).get("score")
        for rec in subjects.values()
        if rec.get("final", {}).get("score") is not None
    ]
    if not finals:
        return (
            '<div class="headline-card"><p class="placeholder-note">No final '
            "scores are in the ledger yet — the headline renders once "
            "aggregation has run.</p></div>"
        )
    mean = sum(finals) / len(finals)
    levels = (pack.get("scale", {}) or {}).get("levels", {}) or {}
    band = levels.get(int(mean), levels.get(str(int(mean)), ""))
    bandText = " ({})".format(band) if band else ""
    scored = sum(
        1
        for sid in taxonomy
        if (subjects.get(sid) or {}).get("final", {}).get("score") is not None
    )
    return (
        '<div class="headline-card">The organisation\'s overall maturity '
        "position is <strong>{:.1f}{}</strong> across {} of {} subjects "
        "scored, against a minimum sustained level of {}.</div>"
    ).format(mean, escape(bandText), scored, len(taxonomy), escape(pack.get("minimumSustained", "—")))


def buildSections(sectionTemplate, repoRoot):
    draftDir = os.path.join(repoRoot, "deliverable", "draft")
    blocks = []
    if os.path.isdir(draftDir):
        for name in sorted(os.listdir(draftDir)):
            if not re.match(r"^\d{2}_.*\.md$", name):
                continue
            with open(os.path.join(draftDir, name), "r", encoding="utf-8") as handle:
                rendered = markdownToHtml(handle.read())
            blocks.append(
                sectionTemplate.replace("{{sectionNN}}", rendered).replace(
                    "{sectionNN}", rendered
                )
            )
    if not blocks:
        return (
            '<p class="placeholder-note">Domain narrative pending — section '
            "writer drafts will appear here once filed at "
            "deliverable/draft/NN_sectionName.md.</p>"
        )
    return "\n".join(blocks)


def buildFlaggedSubjects(ledger):
    subjects = ledger.get("subjects", {}) or {}
    items = []
    for sid in sorted(subjects):
        rec = subjects[sid]
        if not rec.get("flag"):
            continue
        final = rec.get("final", {}) or {}
        label = (
            "below the sustained band" if rec["flag"] == "lowOutlier"
            else "above the sustained band"
        )
        items.append(
            "<li><strong>{}</strong> — score {} ({}), {}.</li>".format(
                escape(subjectDisplayName(sid)),
                escape(final.get("score", "—")),
                escape(final.get("confidence", "—")),
                escape(label),
            )
        )
    if not items:
        return "<p>No subject is flagged as an outlier in the current ledger.</p>"
    return "<ul>{}</ul>".format("".join(items))


def buildKeyFindings(ledger):
    subjects = ledger.get("subjects", {}) or {}
    items = []
    for sid in sorted(subjects):
        rec = subjects[sid]
        sayScore = rec.get("sayScore")
        doScore = rec.get("doScore")
        if sayScore is None or doScore is None:
            continue
        delta = doScore - sayScore
        direction = (
            "practice runs ahead of documentation" if delta > 0
            else "documentation runs ahead of practice" if delta < 0
            else "documentation and practice align"
        )
        items.append(
            "<li><strong>{}</strong> — say {} versus do {}: {} "
            '<span class="finding-say-do">(dual sourced from the say and do '
            "evidence in the ledger)</span></li>".format(
                escape(subjectDisplayName(sid)),
                escape(sayScore),
                escape(doScore),
                escape(direction),
            )
        )
    if not items:
        return (
            '<p class="placeholder-note">Key findings render once subjects '
            "carry both a say score and a do score in the ledger.</p>"
        )
    return "<ul>{}</ul>".format("".join(items))


ROADMAP_PLACEHOLDER = (
    '<p class="placeholder-note">Improvement roadmap pending — the assessor '
    "drafts the prioritised improvement actions once findings are reconciled."
    "</p>"
)


# ── assembly ─────────────────────────────────────────────────────────

def _readFile(path):
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def _loadVendorPlotly():
    vendorPath = os.path.join(HERE, "vendor", "plotly.min.js")
    if not os.path.isfile(vendorPath):
        raise FileNotFoundError(
            "Vendored Plotly bundle missing at {}. The deliverable must be "
            "self contained — no CDN fallback exists. Fetch it with:\n"
            "  {}\n(run from the plugin deliverable/ directory; see "
            "vendor/README.md).".format(vendorPath, VENDOR_FETCH_COMMAND)
        )
    return _readFile(vendorPath)


def _extractSectionTemplate(template):
    match = re.search(
        r"sectionTemplateBegin\n(.*?)\n\s*sectionTemplateEnd", template, re.S
    )
    if match:
        return match.group(1)
    return '<section class="summary-section">\n{{sectionNN}}\n</section>'


def _substitute(template, tokens):
    for key, value in tokens.items():
        template = template.replace("{{" + key + "}}", value)
    return template


def build(repoRoot):
    repoRoot = os.path.abspath(repoRoot)
    configLoader = _loadConfigLoader()
    reportGate = _loadReportGate()

    engagement = configLoader.loadEngagement(repoRoot)
    _, pack = configLoader.resolvePack(repoRoot, _pluginRoot())

    ledgerPath = os.path.join(repoRoot, "scoreLedger.json")
    with open(ledgerPath, "r", encoding="utf-8") as handle:
        ledger = json.load(handle)

    benchmark = None
    benchmarkPath = os.path.join(repoRoot, "deliverable", "benchmark.json")
    if os.path.isfile(benchmarkPath):
        with open(benchmarkPath, "r", encoding="utf-8") as handle:
            benchmark = json.load(handle)

    gate = reportGate.evaluateGate(ledger, pack)
    draftBadge, bodyClass = buildDraftBadge(gate)

    plotlyJs = _loadVendorPlotly()
    styles = _readFile(os.path.join(HERE, "templates", "reportStyles.css"))

    eng = engagement.get("engagement", {}) or {}
    brand = engagement.get("brand", {}) or {}
    buildDate = isoToDisplay(date.today().isoformat())

    meta = {
        "domains": (pack.get("taxonomy", {}) or {}).get("domains", []),
        "minimumSustained": pack.get("minimumSustained"),
        "scaleLevels": (pack.get("scale", {}) or {}).get("levels", {}),
    }

    ledgerJson = json.dumps(ledger, indent=2).replace("</", "<\\/")
    metaJson = json.dumps(meta).replace("</", "<\\/")
    benchmarkJson = (
        json.dumps(benchmark).replace("</", "<\\/") if benchmark else "null"
    )

    subjects = ledger.get("subjects", {}) or {}
    anyTrend = any(
        rec.get("flag")
        or len({h.get("score") for h in rec.get("history", []) or []}) > 1
        for rec in subjects.values()
    )
    runTrendSection = ""
    if anyTrend:
        runTrendSection = (
            "  <h2>Score movement across runs</h2>\n"
            '  <div class="plot-block">\n'
            '    <div id="plot-runTrend" class="plot-container" aria-label='
            '"Line chart of score movement across scoring runs for flagged '
            'or changed subjects"></div>\n'
            '    <p class="plot-caption" id="caption-runTrend"></p>\n'
            "  </div>"
        )

    peerPercentileSection = ""
    if benchmark:
        peerPercentileSection = (
            "  <h2>Peer benchmark</h2>\n"
            '  <div class="plot-block">\n'
            '    <div id="plot-peerPercentile" class="plot-container" '
            'aria-label="Grouped bar chart of engagement scores against '
            'cohort percentiles per subject"></div>\n'
            '    <p class="plot-caption" id="caption-peerPercentile"></p>\n'
            "  </div>"
        )

    common = {
        "styles": styles,
        "bodyClass": bodyClass,
        "draftBadge": draftBadge,
        "logoName": escape(brand.get("logo", "SAS AM")),
        "reportTitle": escape(brand.get("reportTitle", "Maturity Assessment")),
        "client": escape(eng.get("client", "—")),
        "engagementCode": escape(eng.get("code", "—")),
        "footerTagline": escape(FOOTER_TAGLINE),
        "plotlyJs": plotlyJs,
        "ledgerJson": ledgerJson,
        "metaJson": metaJson,
    }

    dashboardTokens = dict(common)
    dashboardTokens.update(
        {
            "startDate": isoToDisplay(eng.get("start", "—")),
            "buildDate": buildDate,
            "kpiStrip": buildKpiStrip(ledger, pack),
            "runTrendSection": runTrendSection,
            "peerPercentileSection": peerPercentileSection,
            "subjectTable": buildSubjectTable(ledger, pack),
            "benchmarkJson": benchmarkJson,
        }
    )
    dashboardTemplate = _readFile(
        os.path.join(HERE, "templates", "dashboardTemplate.html")
    )
    dashboardHtml = _substitute(dashboardTemplate, dashboardTokens)

    summaryTemplate = _readFile(
        os.path.join(HERE, "templates", "summaryTemplate.html")
    )
    sectionTemplate = _extractSectionTemplate(summaryTemplate)
    summaryTokens = dict(common)
    summaryTokens.update(
        {
            "documentControl": buildDocumentControl(
                engagement, ledger, pack, gate, buildDate
            ),
            "headline": buildHeadline(ledger, pack),
            "sections": buildSections(sectionTemplate, repoRoot),
            "flaggedSubjects": buildFlaggedSubjects(ledger),
            "keyFindings": buildKeyFindings(ledger),
            "roadmap": ROADMAP_PLACEHOLDER,
        }
    )
    summaryHtml = _substitute(summaryTemplate, summaryTokens)

    outDir = os.path.join(repoRoot, "deliverable")
    os.makedirs(outDir, exist_ok=True)
    dashboardPath = os.path.join(outDir, "dashboard.html")
    summaryPath = os.path.join(outDir, "summary.html")
    with open(dashboardPath, "w", encoding="utf-8") as handle:
        handle.write(dashboardHtml)
    with open(summaryPath, "w", encoding="utf-8") as handle:
        handle.write(summaryHtml)

    return {
        "dashboard": dashboardPath,
        "summary": summaryPath,
        "gate": gate,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Render dashboard.html and summary.html from the score ledger."
    )
    parser.add_argument("--repo", required=True, help="Engagement repo root")
    args = parser.parse_args(argv)
    try:
        result = build(args.repo)
    except FileNotFoundError as error:
        print("ERROR: {}".format(error), file=sys.stderr)
        return 1
    print("Wrote {}".format(result["dashboard"]))
    print("Wrote {}".format(result["summary"]))
    if result["gate"]["open"]:
        print("Report gate OPEN — rendered clean.")
    else:
        print(
            "Report gate CLOSED — DRAFT badge stamped ({} reasons).".format(
                len(result["gate"]["reasons"])
            )
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
