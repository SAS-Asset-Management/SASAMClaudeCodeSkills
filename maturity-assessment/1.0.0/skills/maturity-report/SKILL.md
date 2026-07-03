---
name: maturity-report
description: Assemble the engagement deliverables — the interactive dashboard and the PDF executive summary, both rendered from scoreLedger.json. Use when the assessor says "build the report", "generate the deliverable", "assemble the dashboard", "refresh the report", or "export the PDF". Consumes the ledger, the findings in findings/, and the pack's reportSpec, and produces deliverable/dashboard.html, deliverable/summary.html, and deliverable/summary.pdf, gated by orchestrate check and reportGate semantics with a visible DRAFT badge whenever the gate is closed. This skill never originates scores.
version: 1.0.0
---

# Maturity Report Skill

This skill composes the engagement's billable deliverables from the score ledger. It does not originate content: every number traces to `scoreLedger.json`, every narrative claim traces to a finding or a review, and every chart comes from the closed plot catalogue. Gate first, aggregate, fan out, QA, render — with the assessor pausing at the two most sensitive points.

## Workflow

Execute the phases in order. Do not compress or reorder. Resume from the last completed phase on a partial build — never rerun a completed phase silently.

### 1. Bootstrap the engagement context

- Load `engagement.yaml` from the engagement repo root (brand tokens, deliverable options, benchmark setting). Stop if absent.
- Resolve the framework pack: engagement `packs/<packId>/` overlay first, then `${CLAUDE_PLUGIN_ROOT}/packs/<packId>/`.
- Read `pack.yaml` for the taxonomy, scale, and `minimumSustained`. Never assume a subject count or a domain count.
- Read the pack's `reportSpec/qaRules.yaml` (brand, banned phrasings, citation format) and enumerate the section specs under `reportSpec/sections/`.

### 2. Gate check — before any drafting

Run:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/engine/orchestrate.py --repo <root> check
```

and consult the `deliverable/reportGate.py` semantics: the gate is open only when every taxonomy subject has a non null final score in the ledger, every subject with a findings file has both a sayScore and a doScore (dual sourced), and no dispute is open. **A closed gate does not block the build — it stamps a visible DRAFT badge on every surface** (dashboard, summary, PDF cover, executive summary). Never suppress the badge and never paper over a gate reason: report the reasons to the assessor verbatim.

### 3. Aggregate — assessor pause one

Confirm the ledger is current: if evidence records have changed since the last engine run, rerun `python3 ${CLAUDE_PLUGIN_ROOT}/engine/aggregate.py --repo <engagementRoot>` first. Then present the aggregation to the assessor — final scores, confidence intervals, flags (`lowOutlier` below 2, `highOutlier` above 4), run over run deltas — and **pause for their review before any drafting**. The outlier flags are narrative hotspots: they must surface in the executive summary, never disappear into the per subject roll up.

### 4. Draft — fan out the section writers

Fan out one `section-writer` agent invocation per section spec, in parallel where sections are independent. Each writer reads ONLY its own `reportSpec/sections/NN_*.md` spec plus the upstream sources that spec names — one invocation, one section, clean context. Every numeric figure a writer uses comes from `scoreLedger.json`; no synthesised figures, no recomputation from prose. Recommendations carry no delivery horizons, no dates, and no owners.

After drafting, **pause for the assessor's review of the executive summary and the overall maturity narrative** — assessor pause two. These sections never go to render without a human check.

### 5. QA — detection only

Run the `report-qa` agent over the drafts. It produces a punch list (block, flag, info) citing file and line — it never silently edits. The checks are **semantic, not just grep**: the paraphrase lesson stands — a banned concept reworded as a synonym must still be caught, so the QA pass asks whether the text expresses the banned concept, not merely whether the banned string appears. The pack's `reportSpec/qaRules.yaml` supplies the banned phrasings, brand rules, and the citation format. The assessor dispositions every punch list item.

### 6. Render the dashboard and summary

Charts come ONLY from the closed catalogue at `${CLAUDE_PLUGIN_ROOT}/deliverable/plotCatalogue.md` — exactly four plots: domainRadar, subjectConfidence, runTrend, peerPercentile. **A chart not in the catalogue requires a discussion with the assessor — never a silent addition.** Plots are JS rendered with the locally vendored library; no CDN, no fetch at runtime. Confidence is shown by opacity or hatch, never by colour alone. The peerPercentile plot renders only when `deliverable/benchmark.json` exists — when absent it is omitted, never faked.

Build:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/deliverable/buildDashboard.py --repo <root>
```

which writes `deliverable/dashboard.html` and `deliverable/summary.html` into the engagement.

### 7. Export the PDF

Export `deliverable/summary.pdf` with `${CLAUDE_PLUGIN_ROOT}/deliverable/exportPdf.py` — a headless Chromium capture of the live render, so the JS charts print natively. Do not build a Python plot rasteriser and do not substitute another PDF pipeline.

### 8. Hand over

Give the assessor a short handover: deliverable paths, report version and date, whether the DRAFT badge is in effect and why, open disputes and unresolved findings still outstanding, and the recommended review workshop participants.

## Guardrails

- Never score or rescore from this skill. Scores come from the ledger via maturity-score and maturity-reconcile; if a score looks wrong, fix the evidence and rerun the engine — never adjust it inside the report.
- Gate first, always: `python3 ${CLAUDE_PLUGIN_ROOT}/engine/orchestrate.py --repo <root> check` plus the reportGate semantics. A closed gate stamps a visible DRAFT badge on every surface — never suppress it.
- Every numeric figure traces to `scoreLedger.json`. No synthesised figures, no recomputation from prose.
- One section writer invocation per section, each reading only its own section spec.
- Two mandatory assessor pauses: after aggregation, and after drafting the executive summary and overall maturity narrative.
- QA is detection only and semantic — a banned concept reworded as a synonym must still be caught. The QA agent never edits; the assessor dispositions.
- Charts come only from the closed plot catalogue (domainRadar, subjectConfidence, runTrend, peerPercentile). A new chart type requires a discussion, never a silent addition. The peerPercentile plot is omitted, never faked, when benchmark data is absent.
- Subjects flagged `lowOutlier` or `highOutlier` surface in the executive summary — never hidden in the roll up. Low confidence is a legitimate state and is shown, not suppressed.
- Recommendations carry no delivery horizons, no dates, and no owners.
- Never reference a subject, artefact, or finding not present in its source location. The report is an evidence register, not an essay.
- Never assume the subject count — enumerate from the pack taxonomy.
- Australian English throughout. No hyphens in prose — em dashes or rephrase. No emojis. DD/MM/YYYY displayed dates. Quality and traceability override speed — if in doubt, stop and ask.
- **Agent fallback.** If a named delegate agent is not an available subagent type in this session, execute its instruction file from the plugin's `agents/` directory inline and record in the output that it ran inline.

## Invocation

Trigger this skill on any of the following:

- "Build the report"
- "Generate the deliverable"
- "Assemble the dashboard"
- "Refresh the report"
- "Export the PDF"

On trigger, execute the eight phases in order. Do not compress or reorder them. Resume from the last completed phase if the build is partial; never rerun a completed phase silently.
