# Plot Catalogue

Canonical list of every chart permitted in a maturity assessment deliverable. A plot that is not in this catalogue does not belong in any deliverable. Authoring a new chart type requires a deliberate catalogue change — an update to this file agreed with the assessor before the chart is drafted. The `plotBlocker` hook enforces this closed set: the only render function names permitted in any generated surface are `renderDomainRadar`, `renderSubjectConfidence`, `renderRunTrend`, and `renderPeerPercentile`.

## Global rules

- **JS rendered only.** Every plot is authored and rendered in the browser via Plotly.js. No Python plot rasterisation — no matplotlib, seaborn, plotnine, pylab, altair, or Chart.js. The PDF export captures the live HTML through headless Chromium so the JS plots render into print at export time.
- **Vendoring.** Plotly.js is vendored locally at `deliverable/vendor/plotly.min.js` and inlined into every generated surface. No CDN reference at runtime, no `fetch()`. The deliverable works offline from `file://`.
- **One source of truth.** Every data binding reads the engagement `scoreLedger.json`, embedded as an inline JSON script tag. No plot may synthesise a numeric value — if the ledger does not carry it, the plot omits it.
- **Score colour ramp.** Scores 0 to 5 use a single ramp: red at 0 (`#B83232`), amber at 2 (`#D99424`), SAS green at 4 and above (`#69BE28`). The same ramp is used across every score plot for reader continuity. Brand base is SAS navy `#002244`.
- **Confidence signal.** Confidence is shown by opacity or hatch pattern — never by colour alone. High = solid fill (opacity 1.0). Medium = opacity 0.7. Low = opacity 0.45.
- **Every plot has**: a title, axis labels, a legend where multi series, at least one annotation calling out the most important data point, alt text on the container (`aria-label` on the `.plot-container` div), and a one sentence active voice caption underneath stating what the reader should take from the plot. Captions are not optional.
- **Accessibility.** Minimum 12pt label size. Colour never used alone to convey meaning — always paired with opacity, shape, label, or position.
- **Containers.** Each chart is embedded via `<div id="plot-<plotId>" class="plot-container" aria-label="…">` and rendered by its named function on page load. PDF exporters wait for every `.plot-container` to have children before capture.

## Plot inventory

### 1. domainRadar

| Contract row | Value |
| --- | --- |
| Purpose | Immediate shape read of maturity across the pack's taxonomy domains. |
| Data binding | `scoreLedger.json → subjects.<subjectId>.final.score`, grouped by `pack.yaml → taxonomy.domains` — one axis per domain, value = mean of the non null subject finals in that domain. |
| Type | Plotly `scatterpolar` with filled area. |
| Colour rule | SAS navy `#002244` fill at 20 percent opacity, SAS green `#69BE28` line at 2px. Minimum sustained ring in muted grey dotted line. |
| Annotation requirement | A dotted reference ring at the pack `minimumSustained` level, plus a callout on the domain furthest below that ring: "{Domain name}: {mean}". |
| Where it appears | Dashboard (full size, top of scorecard); summary (compact, headline section). |
| Caption pattern | "Mean maturity score by domain against the minimum sustained level of {minimumSustained}. {Lowest domain} sits furthest below the ring." |

Render function: `renderDomainRadar`.

### 2. subjectConfidence

| Contract row | Value |
| --- | --- |
| Purpose | Show every subject's final score with its confidence interval and evidence strength in one frame. |
| Data binding | `scoreLedger.json → subjects.<subjectId>.final.score` (bar length), `subjects.<subjectId>.final.ci` (error bars), `subjects.<subjectId>.final.confidence` (bar opacity). |
| Type | Plotly horizontal `bar`, one bar per subject, x axis 0 to 5. |
| Colour rule | Each bar coloured by the score ramp at its score. Confidence via opacity only — High opaque (1.0), Medium 0.7, Low 0.45 — never colour alone. |
| Annotation requirement | Error bars from `final.ci` on every bar, plus a callout on the lowest scoring subject: "{Subject}: {score}". |
| Where it appears | Dashboard (full size, scorecard body); summary (flagged subjects excerpt). |
| Caption pattern | "Final score per subject with 95 percent confidence interval. Bar opacity signals evidence confidence; {lowest subject} carries the lowest score at {score}." |

Render function: `renderSubjectConfidence`.

### 3. runTrend

| Contract row | Value |
| --- | --- |
| Purpose | Show how flagged or changed subjects moved across scoring runs. |
| Data binding | `scoreLedger.json → subjects.<subjectId>.history[]` (run, score) for every subject whose `flag` is non null or whose history contains more than one distinct score; run dates from `scoreLedger.json → runs[]`. |
| Type | Plotly `scatter` lines with markers, one trace per qualifying subject, x = run number, y = score. |
| Colour rule | Line colour by the score ramp at the subject's latest score; markers solid. |
| Annotation requirement | A direction annotation (lifts, holds, lowers) on each trace's final point, drawn from the latest history entry's driver text. |
| Where it appears | Dashboard (scorecard body, below subjectConfidence); omitted entirely when no subject qualifies. |
| Caption pattern | "Score movement across runs for flagged or changed subjects. {Subject} moved {direction} between run {a} and run {b}." |

Render function: `renderRunTrend`.

### 4. peerPercentile

| Contract row | Value |
| --- | --- |
| Purpose | Position each subject's engagement score against the de identified cohort percentiles. |
| Data binding | `scoreLedger.json → subjects.<subjectId>.final.score` versus `deliverable/benchmark.json → <subjectId>.{p25, p50, p75}`; cohort size from `<subjectId>.cohortSize`. |
| Type | Plotly grouped `bar` per subject: engagement score alongside cohort p25, p50, and p75. |
| Colour rule | Engagement bar in SAS green `#69BE28`; cohort percentile bars in three navy tints of `#002244` (lightest p25, darkest p75). |
| Annotation requirement | Cohort size noted in the legend or a corner annotation ("cohort of {n}"), plus a callout on the subject furthest above or below its cohort median. |
| Where it appears | Dashboard only, and **only when `deliverable/benchmark.json` exists** in the engagement. When the file is absent the plot is omitted entirely — never fabricated. |
| Caption pattern | "Engagement score against cohort percentiles per subject. {Subject} sits {above/below} the cohort median by {delta} points." |

Render function: `renderPeerPercentile`.

## File format conventions

- Each plot is authored once as a JS function inside the generated HTML (the builder inlines the functions from the template), keyed by the render function names above.
- Data bindings read the inlined `ledger` object (a verbatim embed of `scoreLedger.json`). Do not fetch at runtime.
- No static PNGs and no `plots/` output directory. If a third party needs a plot as an image, screenshot the rendered HTML or export from Plotly's built in modebar.
