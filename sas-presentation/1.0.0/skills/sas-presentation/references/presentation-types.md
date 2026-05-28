# Presentation Types Reference

This document defines the 17 supported presentation types. Each type specifies its own section structure, typical slide count, layout style, tone, and key components. When the user requests a presentation, identify the appropriate type during discovery and follow its structure.

---

## Type Selection Guide

During the discovery interview, determine the presentation type based on:

1. **Purpose**: What is the user trying to achieve?
2. **Audience**: Who will consume this?
3. **Format**: How will it be delivered?

If the user does not specify a type, default to **Presentation** (standard narrative deck).

**Remote delivery note:** For any type delivered over Microsoft Teams or Zoom (webinars, remote client workshops, investor updates over video), recommend the presenter switch the deck to **share mode** before joining the call — this is a codec friendly theme that compensates for video compression. See the "Sharing over Microsoft Teams or Zoom" section in SKILL.md.

---

## Type Definitions

### 1. Presentation

**Standard narrative deck using the Situation → Complication → Resolution arc. TED-style: more talking, less content.**

| Attribute | Value |
|-----------|-------|
| Typical Slide Count | 6–12 |
| Primary Layout | Mixed (question slides / full-bleed images / split / stat / breather) |
| Tone | Professional, story-driven |
| Use Case | Conference talks; client workshops; advisory presentations; strategy sessions |
| Binary Background | Recommended |
| Word Limit | 10 words or fewer per slide |
| Key Points | 3 maximum |

**Sections:**

| Section | data-section | Footer Label | Act | Purpose |
|---------|-------------|--------------|-----|---------|
| Title | `title` | TITLE | — | Orient. Establish credibility. No agenda. |
| Situation (Hook) | `situation` | SITUATION | 1 | Earn the next 20 minutes. Open with tension. |
| Complication | `complication` | COMPLICATION | 2 | Introduce tension — the "but." |
| Evidence | `evidence` | EVIDENCE | 2 | Prove it with data or imagery. |
| Decisions | `decisions` | DECISIONS | 3 | Deliver the answer — the "therefore." |
| Recommendation | `recommendation` | RECOMMENDATION | 3 | What the audience should DO. |

**Slide Type Selection per Section:**

| Section | Recommended Slide Types |
|---------|------------------------|
| Title | Title slide (`.title-slide`) |
| Situation | Question slide (`.slide-question`) or Stat slide (`.slide-stat`) |
| Complication | Question slide, Breather (`.slide-breather`), or Standard split |
| Evidence | Stat slide, Full bleed image (`.slide-fullbleed`), or Standard split with chart |
| Decisions | Standard split or Question slide |
| Recommendation | Card grid (3 items max) or Standard split |
| Close | Contributions (`.slide-contributions`) — never "Thank You" or "Questions?" |

**Key Components:** Speaker notes with transition cues (press S); question slides; breather slides; stat slides; full-bleed images; contributions close; progressive reveals (fragments)

**Reveal.js Overrides:** `plugins: [RevealNotes]`

---

### 2. Report

**Detailed findings and analysis document in slide format.**

| Attribute | Value |
|-----------|-------|
| Typical Slide Count | 15–30 |
| Primary Layout | Text-heavy with supporting charts |
| Tone | Formal / Analytical |
| Use Case | Maturity assessments; audit findings; analytical deep-dives |
| Binary Background | Optional |

**Sections:**

| Section | data-section | Footer Label |
|---------|-------------|--------------|
| Title | `title` | TITLE |
| Executive Summary | `executive-summary` | EXECUTIVE SUMMARY |
| Methodology | `methodology` | METHODOLOGY |
| Findings (grouped by theme) | `findings` | FINDINGS |
| Analysis | `analysis` | ANALYSIS |
| Recommendations | `recommendations` | RECOMMENDATIONS |
| Appendix | `appendix` | APPENDIX |

**Key Components:** Tables (`.ref-table`); charts; callout boxes (`.card`); numbered findings; appendix slides

**Reveal.js Overrides:** None — use defaults

---

### 3. One Pager

**Single-topic or single-service summary — concise and scannable.**

| Attribute | Value |
|-----------|-------|
| Typical Slide Count | 1–3 |
| Primary Layout | Dense single-slide or short scroll |
| Tone | Punchy / Direct |
| Use Case | Service summaries; leave-behinds; event handouts |
| Binary Background | Skip |

**Sections:**

| Section | data-section | Footer Label |
|---------|-------------|--------------|
| Title / Hook | `hook` | HOOK |
| Problem Statement | `problem` | PROBLEM |
| Solution Overview | `solution` | SOLUTION |
| Key Benefits (3–4) | `benefits` | BENEFITS |
| Evidence / Proof Point | `evidence` | EVIDENCE |
| Call to Action | `cta` | CTA |

**Key Components:** Icon grids (`.card-grid`); stat callouts; single compelling visual; contact strip

**Reveal.js Overrides:** `loop: true` (kiosk mode)

---

### 4. Dashboard

**Metrics and KPI display with at-a-glance insights.**

| Attribute | Value |
|-----------|-------|
| Typical Slide Count | 3–8 |
| Primary Layout | Grid / Card-based |
| Tone | Data-driven / Clean |
| Use Case | Monthly reporting; operational reviews; portfolio health checks |
| Binary Background | Skip |

**Sections:**

| Section | data-section | Footer Label |
|---------|-------------|--------------|
| Title | `title` | TITLE |
| KPI Summary Bar | `kpi-summary` | KPI SUMMARY |
| Trend Charts | `trends` | TRENDS |
| Status Indicators | `status` | STATUS |
| Detailed Breakdowns | `detail` | DETAIL |
| Commentary | `commentary` | COMMENTARY |

**Key Components:** KPI cards (`.card` with stat callouts); traffic lights (`.badge` with RAG); sparklines; bar/line charts; RAG status indicators

**Reveal.js Overrides:** `transition: 'fade'`

---

### 5. Chart

**Standalone data visualisation piece focused on a single dataset or insight.**

| Attribute | Value |
|-----------|-------|
| Typical Slide Count | 1–3 |
| Primary Layout | Centred visual with minimal text |
| Tone | Minimal / Impactful |
| Use Case | LinkedIn posts; presentation inserts; data storytelling |
| Binary Background | Skip |

**Sections:**

| Section | data-section | Footer Label |
|---------|-------------|--------------|
| Title | `title` | TITLE |
| Context Statement | `context` | CONTEXT |
| Primary Visualisation | `visualisation` | VISUALISATION |
| Supporting Detail | `detail` | DETAIL |
| Source / Notes | `source` | SOURCE |

**Key Components:** D3/Chart.js embeds; annotation layers; legend; source citation

**Reveal.js Overrides:** None — use defaults

---

### 6. Resume / CV

**Personal or team member profile highlighting experience and credentials.**

| Attribute | Value |
|-----------|-------|
| Typical Slide Count | 3–6 |
| Primary Layout | Split layout (sidebar + main) |
| Tone | Professional / Personal |
| Use Case | Tender submissions; team capability evidence; recruitment |
| Binary Background | Skip |

**Sections:**

| Section | data-section | Footer Label |
|---------|-------------|--------------|
| Header (name / role / contact) | `header` | PROFILE |
| Professional Summary | `summary` | SUMMARY |
| Key Skills | `skills` | SKILLS |
| Experience | `experience` | EXPERIENCE |
| Qualifications / Certifications | `qualifications` | QUALIFICATIONS |
| Notable Projects | `projects` | PROJECTS |

**Key Components:** Photo placeholder; skill bars/tags (`.badge`); timeline layout; logo strip

**Reveal.js Overrides:** None — use defaults

---

### 7. Proposal

**Scoped engagement offer with clear deliverables and commercials.**

| Attribute | Value |
|-----------|-------|
| Typical Slide Count | 10–15 |
| Primary Layout | Mixed (narrative + structured) |
| Tone | Persuasive / Professional |
| Use Case | Client proposals; tender responses; partnership offers |
| Binary Background | Optional |

**Sections:**

| Section | data-section | Footer Label |
|---------|-------------|--------------|
| Title | `title` | TITLE |
| About Us | `about` | ABOUT US |
| Understanding of Need | `need` | THE NEED |
| Proposed Approach | `approach` | APPROACH |
| Scope & Deliverables | `scope` | SCOPE |
| Timeline | `timeline` | TIMELINE |
| Team | `team` | TEAM |
| Investment | `investment` | INVESTMENT |
| Terms | `terms` | TERMS |
| Next Steps | `nextsteps` | NEXT STEPS |

**Key Components:** Pricing tables (`.ref-table`); Gantt/timeline visuals; team bios (`.card`); scope matrix; T&Cs slide

**Reveal.js Overrides:** None — use defaults

---

### 8. Capability Brochure

**Full firm overview showcasing services and track record.**

| Attribute | Value |
|-----------|-------|
| Typical Slide Count | 8–12 |
| Primary Layout | Visual-heavy / Magazine-style |
| Tone | Confident / Aspirational |
| Use Case | Business development; conference handouts; website content |
| Binary Background | Recommended |

**Sections:**

| Section | data-section | Footer Label |
|---------|-------------|--------------|
| Title | `title` | TITLE |
| Who We Are | `about` | WHO WE ARE |
| Our Approach | `approach` | OUR APPROACH |
| Service Lines | `services` | SERVICES |
| Key Differentiators | `differentiators` | DIFFERENTIATORS |
| Case Study Highlights | `casestudies` | CASE STUDIES |
| Client Logos | `clients` | CLIENTS |
| Team | `team` | TEAM |
| Contact | `contact` | CONTACT |

**Key Components:** Logo grids (`.card-grid`); service cards (`.card`); stat callouts; testimonial quotes; team photos

**Reveal.js Overrides:** None — use defaults

---

### 9. Case Study

**Project outcome narrative demonstrating value delivered.**

> **Choose the format before you start:**
> - **Screen deck** (BD meetings, webinar, live present) → use the Reveal.js scaffold with the sections below
> - **Downloadable PDF artefact** (website resource, email attachment, tender evidence) → use the **print-first template** at `references/case-study-template.md`. Do NOT try to export a Reveal.js deck via Chrome headless — aspect ratio mismatch produces letterboxed, shrunk output. For Reveal → PDF, use `npx decktape reveal presentation.html output.pdf` instead.

| Attribute | Value |
|-----------|-------|
| Typical Slide Count | 6–10 (deck) · 8 pages (print artefact) |
| Primary Layout | Storytelling (problem → solution → result) |
| Tone | Narrative / Evidence-based |
| Use Case | BD meetings; website content; tender evidence |
| Binary Background | Optional (deck only — never print) |

**Sections:**

| Section | data-section | Footer Label |
|---------|-------------|--------------|
| Title | `title` | TITLE |
| Client Context | `context` | CLIENT CONTEXT |
| Challenge | `challenge` | CHALLENGE |
| Approach | `approach` | APPROACH |
| Solution | `solution` | SOLUTION |
| Results / Outcomes | `results` | RESULTS |
| Key Metrics | `metrics` | KEY METRICS |
| Testimonial | `testimonial` | TESTIMONIAL |
| Lessons Learned | `lessons` | LESSONS |

**Key Components:** Before/after outcomes grid; metric stat tiles (4 up); vertical timeline with numbered phase nodes; testimonial quote card with avatar; 2×2 lessons grid; back-cover CTA with 3-item contact grid.

**SVG Logo Alignment Rules (apply to both deck and print):**
- Use width-based sizing with `height: auto` — never set both width and height on an SVG (distorts it)
- SAS primary logo: `viewBox 0 0 371 53` (7:1 horizontal lockup) — load from Webflow CDN
- For white rendering on dark backgrounds: `filter: brightness(0) invert(1)`
- For client wordmarks: strip any decorative swoosh/background shapes from the source SVG, set all paths to `fill="currentColor"`, inline the SVG in HTML (not `<img src>`), and tint via CSS `color:`
- Anti-pattern: `background: white` wrappers around client logos, translucent `rgba(255,255,255,0.08)` logo boxes

**Reveal.js Overrides:** None — use defaults
**Print template:** See `references/case-study-template.md` for full component CSS blueprints, `@page` rules, and the Chrome headless export command.

---

### 10. Pitch Deck

**Concise storytelling arc for investor or partner conversations.**

| Attribute | Value |
|-----------|-------|
| Typical Slide Count | 8–12 |
| Primary Layout | Full-bleed / High-impact visuals |
| Tone | Bold / Compelling |
| Use Case | Investor pitches; partnership discussions; accelerator applications |
| Binary Background | Recommended |

**Sections:**

| Section | data-section | Footer Label |
|---------|-------------|--------------|
| Title | `title` | TITLE |
| The Problem | `problem` | THE PROBLEM |
| The Opportunity | `opportunity` | OPPORTUNITY |
| Our Solution | `solution` | OUR SOLUTION |
| How It Works | `howitworks` | HOW IT WORKS |
| Traction / Evidence | `traction` | TRACTION |
| Business Model | `model` | MODEL |
| Team | `team` | TEAM |
| The Ask | `ask` | THE ASK |
| Contact | `contact` | CONTACT |

**Key Components:** Large typography; single-stat slides; demo screenshots; team grid (`.card-grid`)

**Reveal.js Overrides:** None — use defaults

---

### 11. Executive Briefing

**Short high-signal update for senior stakeholders.**

| Attribute | Value |
|-----------|-------|
| Typical Slide Count | 4–7 |
| Primary Layout | Clean / Sparse with emphasis on key messages |
| Tone | Direct / Authoritative |
| Use Case | Board updates; sponsor briefings; steering committee reports |
| Binary Background | Skip |

**Sections:**

| Section | data-section | Footer Label |
|---------|-------------|--------------|
| Title | `title` | TITLE |
| Situation Summary | `situation` | SITUATION |
| Key Decisions Required | `decisions` | DECISIONS |
| Supporting Evidence (2–3 points) | `evidence` | EVIDENCE |
| Recommended Action | `recommendation` | RECOMMENDATION |
| Timeline | `timeline` | TIMELINE |

**Key Components:** Decision matrix (`.ref-table`); RAG summary (`.badge`); single-page risk register; action table

**Reveal.js Overrides:** None — use defaults

---

### 12. Workshop / Training

**Interactive slides with exercises and progressive reveals.**

| Attribute | Value |
|-----------|-------|
| Typical Slide Count | 10–25 |
| Primary Layout | Mixed (instructional + interactive) |
| Tone | Engaging / Educational |
| Use Case | Client workshops; internal training; conference tutorials |
| Binary Background | Skip |

**Sections:**

| Section | data-section | Footer Label |
|---------|-------------|--------------|
| Title | `title` | TITLE |
| Learning Objectives | `objectives` | OBJECTIVES |
| Concept Intro | `concept` | CONCEPT |
| Worked Example | `example` | EXAMPLE |
| Exercise / Activity | `exercise` | EXERCISE |
| Group Discussion Prompt | `discussion` | DISCUSSION |
| Key Takeaways | `takeaways` | TAKEAWAYS |
| Resources | `resources` | RESOURCES |

**Key Components:** Fragment reveals; exercise prompts (`.card` with `.badge-required`); timer embeds; recap slides; handout links

**Reveal.js Overrides:** `help: true`, `showSlideNumber: 'all'`

---

### 13. Project Status Update

**Milestone and risk-focused project health check.**

| Attribute | Value |
|-----------|-------|
| Typical Slide Count | 5–8 |
| Primary Layout | Structured / Tabular |
| Tone | Factual / Concise |
| Use Case | Weekly/monthly project reporting; PMO updates; client check-ins |
| Binary Background | Skip |

**Sections:**

| Section | data-section | Footer Label |
|---------|-------------|--------------|
| Title | `title` | TITLE |
| Status Summary (RAG) | `status` | STATUS |
| Milestones & Progress | `milestones` | MILESTONES |
| Risks & Issues | `risks` | RISKS |
| Actions & Owners | `actions` | ACTIONS |
| Budget / Resource Snapshot | `budget` | BUDGET |
| Next Period Focus | `nextperiod` | NEXT PERIOD |

**Key Components:** RAG indicators (`.badge`); milestone tracker; risk register table (`.ref-table`); action log; burn-down chart

**Reveal.js Overrides:** `transition: 'fade'`

---

### 14. Technical Architecture

**System diagrams and data flow documentation.**

| Attribute | Value |
|-----------|-------|
| Typical Slide Count | 6–12 |
| Primary Layout | Diagram-centric with supporting text |
| Tone | Technical / Precise |
| Use Case | Solution design reviews; technical proposals; system documentation |
| Binary Background | Recommended |

**Sections:**

| Section | data-section | Footer Label |
|---------|-------------|--------------|
| Title | `title` | TITLE |
| Architecture Overview | `overview` | OVERVIEW |
| Component Breakdown | `components` | COMPONENTS |
| Data Flow | `dataflow` | DATA FLOW |
| Integration Points | `integration` | INTEGRATION |
| Technology Stack | `techstack` | TECH STACK |
| Security / Compliance | `security` | SECURITY |
| Deployment View | `deployment` | DEPLOYMENT |

**Key Components:** Mermaid/D3 diagrams; component cards (`.card`); API flow diagrams; stack logos (`.card-grid`); network topology SVGs

**Reveal.js Overrides:** None — use defaults

---

### 15. Roadmap / Timeline

**Phased delivery view for products or projects.**

| Attribute | Value |
|-----------|-------|
| Typical Slide Count | 5–10 |
| Primary Layout | Horizontal timeline / Swim-lane |
| Tone | Strategic / Forward-looking |
| Use Case | Product roadmaps; transformation plans; client delivery plans |
| Binary Background | Optional |

**Sections:**

| Section | data-section | Footer Label |
|---------|-------------|--------------|
| Title | `title` | TITLE |
| Vision / Objective | `vision` | VISION |
| Current State | `currentstate` | CURRENT STATE |
| Phase Breakdown (3–5 phases) | `phases` | PHASES |
| Key Milestones | `milestones` | MILESTONES |
| Dependencies | `dependencies` | DEPENDENCIES |
| Success Criteria | `success` | SUCCESS CRITERIA |

**Key Components:** Timeline visualisation (inline SVG); phase cards (`.card`); milestone markers; dependency arrows; swim-lanes

**Reveal.js Overrides:** None — use defaults

---

### 16. Comparison Matrix

**Side-by-side evaluation of options or competitors.**

| Attribute | Value |
|-----------|-------|
| Typical Slide Count | 4–8 |
| Primary Layout | Grid / Table-centric |
| Tone | Objective / Analytical |
| Use Case | Technology selection; vendor evaluation; option analysis |
| Binary Background | Skip |

**Sections:**

| Section | data-section | Footer Label |
|---------|-------------|--------------|
| Title | `title` | TITLE |
| Evaluation Context | `context` | CONTEXT |
| Criteria Definition | `criteria` | CRITERIA |
| Comparison Table / Grid | `comparison` | COMPARISON |
| Analysis & Commentary | `analysis` | ANALYSIS |
| Recommendation | `recommendation` | RECOMMENDATION |

**Key Components:** Weighted scoring table (`.ref-table`); feature tick matrix; radar charts; pros/cons cards (`.card-grid`); winner highlight

**Reveal.js Overrides:** None — use defaults

---

### 17. Meeting Minutes

**Structured record of decisions and actions from a meeting.**

| Attribute | Value |
|-----------|-------|
| Typical Slide Count | 3–6 |
| Primary Layout | Structured / List-based |
| Tone | Factual / Clear |
| Use Case | Post-meeting distribution; project governance; audit trail |
| Binary Background | Skip |

**Sections:**

| Section | data-section | Footer Label |
|---------|-------------|--------------|
| Title (meeting name / date) | `title` | TITLE |
| Attendees | `attendees` | ATTENDEES |
| Agenda Items | `agenda` | AGENDA |
| Discussion Summary (by topic) | `discussion` | DISCUSSION |
| Decisions Made | `decisions` | DECISIONS |
| Action Items (owner / due date) | `actions` | ACTIONS |
| Next Meeting | `nextmeeting` | NEXT MEETING |

**Key Components:** Attendee list; decision log (`.ref-table`); action table with RAG (`.badge`); agenda checklist (`.checklist`); follow-up dates

**Reveal.js Overrides:** None — use defaults

---

### 18. A4 Document

**Print-ready single-page HTML document formatted for A4 paper. Used when the output needs to be emailed, printed, or saved as a PDF — not presented on a screen.**

> **Critical distinction:** This type does NOT use Reveal.js. It is a standalone HTML document with `@media print` styles and `@page { size: A4 portrait; }`. Use `playwright pdf` to export to PDF. Do NOT attempt to use decktape or Reveal.js export — they produce letterboxed output.

| Attribute | Value |
|-----------|-------|
| Typical Page Count | 1–4 A4 pages |
| Primary Layout | Single-column with numbered sections |
| Tone | Formal / Professional |
| Use Case | Proposal letters; executive summaries; leave-behind documents; PDFs for email |
| Binary Background | None (print document) |
| Font | Inter (Google Fonts) |

**Sections:**

| Section | Purpose |
|---------|---------|
| Cover | Logo, document type pill, title, subtitle, metadata (date, reference, prepared for), tagline |
| Numbered Sections | Body content with `.section-number` badge and `.section-title` heading |
| Pricing Table | `.pricing-wrap` — dark header, highlight row, total row |
| Value Comparison | `.value-compare` — two coloured blocks (navy vs green) with label, amount, sub-label |
| Signature Block | `.sig-block` — two-column grid with sign-off lines |
| Document Footer | Brand name, contact, tagline. Separated by green top border. |

**Key CSS Components:**

| Class | Purpose |
|-------|---------|
| `.page` | A4 container: `width: 210mm`, `padding: 16mm 18mm`, white background, centred |
| `.cover` | Header section with green bottom border |
| `.doc-type` | Green pill badge (e.g. "Partner Proposal") |
| `.section` | Numbered content block |
| `.section-number` | Green circle with white number |
| `.stat-row` / `.stat-card` | Horizontal stat tiles with large green value |
| `.feature-list` | Checklist with green tick prefix |
| `.steps` / `.step` | Numbered process steps in light cards |
| `.two-col` | Two-column grid for lists |
| `.pricing-wrap` | Full-width bordered pricing table |
| `.callout` | Green left-border callout box |
| `.value-compare` | Side-by-side navy/green value blocks |
| `.terms-list` | Two-column term/value list |
| `.next-steps` / `.ns-item` | Numbered next steps with green circle |
| `.sig-block` | Two-column signature grid |
| `.doc-footer` | Footer with brand and tagline |

**SAS Brand Variables (A4 Document):**

```css
:root {
  --sas-navy: #002244;
  --sas-green: #69BE28;
  --sas-green-light: rgba(105, 190, 40, 0.1);
  --sas-green-border: rgba(105, 190, 40, 0.3);
  --text-primary: #002244;
  --text-secondary: #334466;
  --text-muted: #6b7280;
  --bg-secondary: #f7f8fa;
  --border: #e2e6ea;
}
```

**Critical Print CSS — Colour Rendering:**

Chromium (used by Playwright) strips background colours, gradients, and fills by default when generating PDFs. Every A4 document MUST include this in the `@media print` block or backgrounds will be lost:

```css
@media print {
  *, *::before, *::after {
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
    color-adjust: exact !important;
  }
}
```

Without this, coloured table headers, stat tiles, callout boxes, and value blocks all render as plain grey or white.

**Page Margin Pattern:**

Use `@page` margins rather than padding on the container. This ensures margins apply consistently on every page — not just page one:

```css
.page {
  width: 100%;
  margin: 0;
  padding: 0;  /* No padding — margins handled by @page */
  box-shadow: none;
}

@page {
  size: A4 portrait;
  margin: 16mm 18mm;
}
```

**Section Break Control:**

Prevent orphaned headings and broken components:

```css
.section        { break-inside: avoid; page-break-inside: avoid; }
.section-header { break-after: avoid;  page-break-after: avoid; }
.pricing-wrap   { break-inside: avoid; page-break-inside: avoid; }
.sig-block      { break-inside: avoid; page-break-inside: avoid; }
```

**PDF Export:**

```bash
playwright pdf "file:///absolute/path/to/document.html" output.pdf --paper-format A4 --wait-for-timeout 3000
```

**Template Reference:** `references/proposal-a4-template.html` — a complete working A4 proposal document with all components. Copy and adapt content; do not modify the CSS structure.

**Reveal.js Overrides:** Not applicable — this type does not use Reveal.js.

---

## Component Reference

All presentation types share these reusable CSS components from `base-styles.css`:

| Component | CSS Class | Purpose |
|-----------|-----------|---------|
| Question Slide | `.slide-question` | Provocative question, centred. Tease with slide, tell with voice. |
| Full Bleed Image | `.slide-fullbleed` | Single powerful image, edge to edge |
| Breather (Dark Blank) | `.slide-breather` | Pure dark background, focus returns to speaker |
| Stat / Single Number | `.slide-stat` | One bold number with context label |
| Contributions (Final) | `.slide-contributions` + `.contributions-list` | What was accomplished. Stays visible during Q&A. |
| Card | `.card` | Content container with border and shadow |
| Card Grid | `.card-grid` + `.card-grid-2/3/4` | Responsive grid of cards (3 max per slide) |
| Table | `.ref-table` | Styled data table with accent headers |
| Checklist | `.checklist` | List with check/square icons |
| Badge | `.badge` + `.badge-required/recommended/optional` | Status indicator labels |
| Code Block | `.code-block` | Monospace code display |
| Inline Code | `.code-inline` | Inline monospace text |
| Keyboard Key | `.kbd` | Keyboard shortcut badge |
| Split Layout | `.split-layout` | Two-column responsive layout |
| Scroll Container | `.scroll-y` | Scrollable content area |
| Section Tag | `.ref-section-tag` | Section label (uppercase, accent) |
| Title | `.ref-title` | Large slide heading |
| Subtitle | `.ref-subtitle` | Secondary heading |
| Body Text | `.ref-body` | Standard body copy |
| Small Text | `.ref-small` | Fine print / captions |

---

## Reveal.js Default Configuration

All types inherit this base configuration. The Notes plugin is always included for speaker view (press S to open). Type-specific overrides are noted in each type definition above.

```javascript
Reveal.initialize({
  // Plugins
  plugins: [RevealNotes],

  // Navigation
  hash: true,
  hashOneBasedIndex: false,
  respondToHashChanges: true,
  history: false,

  // Display
  slideNumber: 'c/t',
  showSlideNumber: 'speaker',
  center: false,

  // Dimensions (16:9)
  width: 1920,
  height: 1080,
  margin: 0,
  minScale: 0.2,
  maxScale: 2.0,

  // Transitions
  transition: 'slide',
  transitionSpeed: 'default',
  backgroundTransition: 'fade',

  // Interaction
  keyboard: true,
  touch: true,
  loop: false,
  embedded: false,
  help: true,
  mouseWheel: false,
  hideInactiveCursor: true,
  hideCursorTime: 3000,

  // Fragments
  fragments: true,
  fragmentInURL: true,

  // PDF Export
  pdfMaxPagesPerSlide: 1,
  pdfSeparateFragments: false,
});
```
