---
name: sas-amp
description: Develop a comprehensive, ISO 55001-aligned Asset Management Plan with dual HTML and DOCX output
allowed-tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep", "Agent", "WebSearch", "WebFetch", "Skill"]
argument-hint: "[organisation name or 'resume' to continue a previous session]"
---

# Asset Management Plan Development

Develop a comprehensive Asset Management Plan (AMP) aligned to ISO 55001:2024, producing both an interactive HTML presentation and a professionally branded DOCX document.

## Startup

1. Create the working directory structure:
   ```
   ./sas-amp-working/research/
   ./sas-amp-working/data/cleaned/
   ./sas-amp-working/data/charts/
   ./sas-amp-working/drafts/sections/
   ./sas-amp-working/output/
   ```

2. If the argument is "resume", check for an existing `./sas-amp-working/` directory and restore context from any existing drafts and research files. Summarise progress so far and ask what to work on next.

3. If the argument contains an organisation name, record it and begin the adaptive intake process.

4. If no argument is provided, ask:
   > What organisation is this Asset Management Plan for? If you have any data, documents, or context to share, go ahead and provide it all now — I'll analyse what you have before asking questions.

## Adaptive Intake Process

Accept whatever the user provides — data files, context, existing plans, strategic documents — and analyse it thoroughly before asking any questions.

After initial analysis:
1. Summarise what has been understood from the provided materials
2. Identify which AMP sections have sufficient information and which have gaps
3. Present the gap analysis to the user as a checklist

## Research Phase

Dispatch the `amp-researcher` agent to gather:
- Regulatory and legislative context for the organisation's jurisdiction and sector
- Industry benchmarks (useful lives, maintenance cost ratios, condition scales, LoS benchmarks)
- Organisational context (annual reports, strategic plans, publicly available data)

Research runs in the background while the interview continues.

## Interview Phase

For each identified gap, conduct targeted interviews:
- Ask **one question at a time**
- Provide **multiple-choice options** (A, B, C, D) where possible
- Wait for the user's answer before proceeding
- Never ask for information already provided or discoverable through research
- Periodically summarise understanding and confirm

## Data Analysis Phase

When the user provides quantitative data, dispatch the `amp-data-analyst` agent to:
- Clean and normalise data
- Profile assets (age, condition, criticality distributions)
- Perform LCC/NPV calculations
- Generate renewal forecasting models
- Produce both D3.js charts (for HTML) and static images (for DOCX)

## Section Drafting

Draft each AMP section individually, in order:
1. Executive Summary (drafted last, after all other sections)
2. Introduction
3. Levels of Service
4. Future Demand
5. Asset Lifecycle Management
6. Risk Management
7. Financial Summary
8. Asset Management Practices
9. Improvement and Monitoring
10. Appendices

After drafting each section, dispatch the `amp-asset-context-reviewer` agent to review it through the asset owner's perspective. Incorporate feedback before proceeding.

Save each completed section to `./sas-amp-working/drafts/sections/`.

## Output Generation

Once all sections are drafted and reviewed:

### HTML Presentation
Invoke the `/sas-presentation` skill with:
- Type: `standard-narrative`
- Content: All AMP sections
- Charts: D3.js interactive versions
- Branding: SAS-AM (auto-applied by skill)

Save to `./sas-amp-working/output/amp-presentation.html`

### DOCX Document
Run the document generation script:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/generateDocx.py \
  --sections-dir ./sas-amp-working/drafts/sections/ \
  --charts-dir ./sas-amp-working/data/charts/ \
  --output ./sas-amp-working/output/amp-document.docx \
  --org-name "<organisation name>" \
  --date "<current date>"
```

Save to `./sas-amp-working/output/amp-document.docx`

## Session Management

The working directory persists between sessions. If the user returns and says "resume", restore full context from existing files and continue where left off.

Periodically save progress — after each section is drafted, the state is recoverable.
