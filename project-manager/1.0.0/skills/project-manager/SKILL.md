---
name: project-manager
description: marcov.GATE project delivery framework. Use when the user wants to create, manage, track, or review a project. Handles project setup, phase progression, gate reviews, visual dashboards, client status reports, and portfolio sweeps across all repos. Integrates with beam-selling for seamless sales-to-delivery handoff. Supports advisory, software, and hybrid project types at micro/standard/major tiers.
---

# marcov.GATE — Project Delivery Skill

**GATE = Governed Advancement Through Evidence**

A stage-gated hybrid delivery framework for advisory and software projects. Extends the marcov.BEAM philosophy ("earn the right to advance") from sales into delivery. When BEAM Stage 5 (Commit) closes a deal, marcov.GATE takes over.

## Subcommands

```
/project-manager new <client> <project>     — Start new project
/project-manager status [project]           — Show current status
/project-manager gate-review [project]      — Run evidence-gated phase advancement
/project-manager dashboard [project]        — Generate per-project visual dashboard
/project-manager portfolio                  — Sweep all repos, generate master board
/project-manager report <project>           — Generate client-ready status page
/project-manager update [project]           — Update project state interactively
/project-manager close <project>            — Run close-out process
/project-manager list                       — List all discovered projects
```

If no subcommand is provided, show the list above and ask which action to take.

---

## The 5-Phase Lifecycle

```
[1. Inception] → [2. Discovery] → [3. Development] → [4. Delivery] → [5. Close]
```

| Phase | Purpose | Advisory Deliverable | Software Deliverable |
|-------|---------|---------------------|---------------------|
| **1. Inception** | Scope & mobilise | Scope document, project plan | Product vision, high-level requirements |
| **2. Discovery** | Investigate & validate | Data analysis, gap assessment | Detailed requirements, architecture |
| **3. Development** | Create & iterate | Draft report/analysis | Working software (iterative sprints) |
| **4. Delivery** | Finalise & accept | Final report, presentation | Deployed solution, user training |
| **5. Close & Extend** | Learn & grow | Recommendations for next engagement | Support handover, enhancement roadmap |

### Scaling Tiers

| Tier | Value | Duration | Phase Handling | Gate Formality |
|------|-------|----------|---------------|----------------|
| **Micro** | $20K–$50K | 2–4 weeks | Phases 1+2 combined, Phases 4+5 combined | 3 lightweight gates |
| **Standard** | $50K–$200K | 1–3 months | All 5 phases | 5 standard gates |
| **Major** | $200K–$2M | 3–12+ months | All 5 phases + PRINCE2 overlay | 5 formal gates + interim reviews |

---

## Subcommand Workflows

### `/project-manager new`

**Purpose**: Initialise a new project with `.project-status.json` in the repo root.

**Workflow:**

1. **Accept input**: Client name and project name from args, or interview.

2. **BEAM Ingest**: Check for `.beam/` directory in the current repo and parent directories. If a BEAM engagement matching the client name exists:
   - Read the BEAM state JSON file
   - Extract: client name, industry, sector, key stakeholders, diagnosed problems (Stage 2), agreed scope (Stage 3), proposal details (Stage 4), pricing model, contract value
   - Display: "Ingested BEAM engagement data for [client]. [X] fields pre-populated."
   - If no match found, proceed with manual input

3. **Interview** (one question at a time, multiple choice):
   - **Project type**: Advisory / Software / Hybrid
   - **Tier** (if not auto-detected from contract value): Micro / Standard / Major
   - **Sector**: Rail / Transport / Water / Energy / Mining / Health / Local Government / Defence / Other
   - **Pricing model**: Fixed price / Time & materials / Hybrid
   - **Contract value** (if not from BEAM): Dollar amount
   - **Start date**: Date or "today"
   - **Target end date**: Date
   - **Lead consultant**: Name and role
   - **Key stakeholders**: Name, role, organisation (can add multiple)
   - **Key deliverables**: Name and phase assignment

4. **Generate `.project-status.json`**: Write to the current repo root using the schema defined in `references/project-status-schema.json`. Validate against the schema before writing.

5. **Generate initial dashboard**: Produce a project dashboard HTML file in the repo (e.g., `PROJECT_DASHBOARD.html`). Use the template from `templates/project-dashboard.html` and populate with the new project data.

6. **Display summary**: Show phase pipeline, key dates, team, and deliverables in the terminal.

### `/project-manager status`

**Purpose**: Display current project status in the terminal.

**Workflow:**

1. Read `.project-status.json` from the current repo root
2. Display:
   - Phase pipeline (visual ASCII pipeline showing completed/current/upcoming phases)
   - RAG status with explanation
   - Current gate status and evidence items
   - Open risks (count and top risk)
   - Upcoming milestones
   - Days until target end date
   - Last updated date

**ASCII Pipeline Format:**
```
  [1 ✓] ——— [2 ✓] ——— [3 ●] ——— [4 ○] ——— [5 ○]
  Inception  Discovery  Development  Delivery  Close
```

### `/project-manager gate-review`

**Purpose**: Evaluate whether the current phase gate criteria are met and advance if earned.

**Critical Principle**: The skill is the gatekeeper, not the user. The user does not self-certify gates. The skill independently assesses evidence quality.

**Workflow:**

1. Read `.project-status.json` and identify current phase
2. Load gate criteria from `references/gate-criteria.md` for the current phase and tier
3. For each gate criterion:
   - Ask the user to provide evidence (what was done, where is the artefact, who validated it)
   - Assess whether the evidence meets the minimum bar
   - Record verdict: Met / Partially Met / Not Met
4. Calculate gate outcome:
   - **All criteria met → ADVANCE**: Update phase to next, record gate as passed with date and evidence
   - **Some criteria partially met → HOLD**: Explain what is missing, do not advance, record as held
   - **Critical criteria not met → ESCALATE**: Flag blockers, suggest mitigations, record as escalated
5. Update `.project-status.json` with gate outcome
6. Generate gate review report HTML from `templates/gate-review-report.html`
7. If advanced, regenerate dashboard

### `/project-manager dashboard`

**Purpose**: Generate or regenerate the per-project visual dashboard.

**Workflow:**

1. Read `.project-status.json` from current repo
2. Generate `PROJECT_DASHBOARD.html` using the template from `templates/project-dashboard.html`
3. The HTML file is self-contained (inline CSS from `templates/base-styles.css`, inline JS)
4. Three tabs:
   - **Progress**: Phase pipeline, gate status, risk heat map, milestones timeline, RAG indicator
   - **Full Dashboard**: Progress tab PLUS budget tracker, resource allocation, deliverables checklist, stakeholder map, action items
   - **Client Report**: SAS-AM branded status page suitable for direct client delivery

**Data injection**: Read the `.project-status.json` and inject as a `const PROJECT_DATA = {...}` JavaScript variable in the HTML. All rendering is client-side from this data.

### `/project-manager portfolio`

**Purpose**: Sweep all repos for `.project-status.json` files and generate a master portfolio dashboard.

**Workflow:**

1. Dispatch the `portfolio-sweep` agent (see `agents/portfolio-sweep.md`)
2. The agent runs `scripts/sweepProjects.py` which:
   - Scans `~/Documents/Repos/**/.project-status.json`
   - Validates each file against the schema
   - Aggregates into a portfolio data structure
3. Generate `PORTFOLIO_DASHBOARD.html` using `templates/portfolio-dashboard.html`
4. Save to `~/Documents/Repos/personalProgramManager/data/portfolio-dashboard.html`
5. Display summary in terminal: total projects, by phase, by RAG, stale projects (>14 days since update)

### `/project-manager report`

**Purpose**: Generate a polished, SAS-AM branded client status report.

**Workflow:**

1. Read `.project-status.json`
2. Interview for report-specific content (one question at a time):
   - Key decisions made this reporting period
   - Key achievements this period
   - Issues or blockers to escalate
   - Next steps and upcoming milestones
3. Generate `CLIENT_STATUS_REPORT.html` using `templates/client-status-report.html`
4. The report includes:
   - SAS-AM branded header with logos (light/dark mode CDN URLs)
   - Report metadata (date, project name, client, prepared by)
   - Phase progress visual
   - Key decisions and achievements
   - Risk summary (open risks with mitigations)
   - Upcoming milestones
   - Next steps
   - Professional footer
5. Report is print-ready (print styles included)

### `/project-manager update`

**Purpose**: Interactively update project state.

**Workflow:**

1. Read `.project-status.json`
2. Ask what to update (one question, multiple choice):
   - A. Overall RAG status
   - B. Percent complete
   - C. Add/update a risk
   - D. Add/update a deliverable
   - E. Add/update a milestone
   - F. Add/update an action item
   - G. Update team allocation
   - H. Update dates
3. Walk through the selected update with interview questions
4. Write updated `.project-status.json`
5. Set `lastUpdated` to today's date

### `/project-manager close`

**Purpose**: Run the close-out process for a completed project.

**Workflow:**

1. Read `.project-status.json` — verify all prior gates are passed
2. Walk through close-out checklist from `references/closeout-template.md`:
   - All deliverables accepted?
   - Final invoice submitted?
   - Lessons learned captured?
   - Client feedback collected?
   - Handover documentation complete?
   - Next opportunity identified?
3. Update `.project-status.json`:
   - Set Phase 5 gate to passed
   - Set phaseStatus to "completed"
   - Set percentComplete to 100
4. Generate final dashboard
5. Append a summary row to the weekly work notes at `/Users/sasreliability/Documents/Repos/teamMeeting/.note.md`

### `/project-manager list`

**Purpose**: List all projects discovered on the machine.

**Workflow:**

1. Run `scripts/sweepProjects.py` in list mode
2. Display table of all found projects:
   ```
   | Client        | Project         | Phase       | RAG    | % | Tier     | Repo Path |
   |---------------|-----------------|-------------|--------|---|----------|-----------|
   | Yarra Trams   | MDR Review      | Development | Green  | 65| Standard | ~/Repos/ytMdrReview |
   | Dept Health   | Condition PoC   | Discovery   | Amber  | 30| Major    | ~/Repos/deptHealth  |
   ```

---

## State File: `.project-status.json`

Lives in the root of each project repository. This is the canonical state file that the sweep agent discovers.

**Schema**: See `references/project-status-schema.json` for the full JSON Schema.

**Key fields:**
- `schema`: Always `"marcov-gate-v1"`
- `project`: Identity, type, tier, pricing, sector
- `status`: Current phase, RAG, percent complete, dates
- `gates`: Array of 3-5 gates with status, date, evidence
- `risks`: Array of risks with likelihood/impact/mitigation
- `team`: Array of team members with allocation
- `deliverables`: Array of deliverables with phase and status
- `milestones`: Array of milestones with dates and invoice amounts
- `actions`: Array of action items with owners and dates
- `stakeholders`: Array of stakeholders with influence level
- `beamSource`: BEAM engagement ID (if originated from BEAM)

---

## BEAM Integration

When `/project-manager new` detects a `.beam/` directory:

1. **Search**: Look for `.beam/` in the current directory, then walk up parent directories
2. **Match**: Find BEAM state JSON files, match by company name (case insensitive, fuzzy)
3. **Extract** from the BEAM state:
   - `engagement.company_name` → `project.client`
   - `b2b_research.fit_score` → context for risk assessment
   - `stages.2_diagnose.findings` → informs Discovery phase scope
   - `stages.3_align.agreed_scope` → populates project scope and deliverables
   - `stages.4_propose.proposal` → contract value, pricing model, timeline
   - `buying_committee` → populates stakeholders array
   - `engagement.current_stage` → verify deal is at Stage 5+ (warn if earlier)
4. **Warn** if the BEAM engagement is not at Stage 5 (Commit) or later — the deal may not be closed yet

---

## Visual Output Standards

All generated HTML files follow SAS-AM standards:

- **Self-contained**: Single HTML file with inline CSS and JS (no external dependencies except CDN fonts/icons)
- **Light/dark mode**: Toggle button in header, respects system preference, persists to localStorage
- **SAS colour palette**: Uses CSS custom properties from `templates/base-styles.css`
- **Logos**: Webflow CDN URLs (light: `https://cdn.prod.website-files.com/653497186047abfdf821b2fc/69a77a2f0e9f223c5f196bd3_sas-logo.jpg`, dark: `https://cdn.prod.website-files.com/653497186047abfdf821b2fc/69a777cb2f01269a5c7f073e_sas-logo-lightmode.png`)
- **Font**: Source Sans Pro from Google Fonts CDN
- **Icons**: Font Awesome 6 from CDN
- **Responsive**: Mobile-first breakpoints (640px, 768px, 1024px, 1280px)
- **Accessible**: WCAG 2.1 AA contrast ratios, focus states, ARIA labels, keyboard navigation
- **Print-ready**: Print styles hide nav/filters, force light backgrounds
- **Reduced motion**: Respects `prefers-reduced-motion`
- **Australian English**: All labels, headings, and descriptions use Australian English (organisation, colour, programme, etc.)
- **Date format**: DD/MM/YYYY for display

### Theme Toggle Script

Include in all HTML outputs:

```javascript
(function() {
  const STORAGE_KEY = 'marcov-gate-theme';
  function getSystemTheme() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  function setTheme(theme) {
    const resolved = theme === 'system' ? getSystemTheme() : theme;
    document.documentElement.setAttribute('data-theme', resolved);
    localStorage.setItem(STORAGE_KEY, theme);
  }
  function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme') || 'light';
    setTheme(current === 'light' ? 'dark' : 'light');
  }
  setTheme(localStorage.getItem(STORAGE_KEY) || 'system');
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    if (localStorage.getItem(STORAGE_KEY) === 'system') setTheme('system');
  });
  window.toggleTheme = toggleTheme;
})();
```

---

## Gate Criteria by Phase

Detailed gate criteria are in `references/gate-criteria.md`. Summary:

### Gate 1: Inception → Discovery
- Scope document signed or approved
- Stakeholders identified and mapped
- Project plan with timeline and milestones agreed
- Team mobilised and allocated
- Risks initially assessed

### Gate 2: Discovery → Development
- Data collected and validated
- Gaps/requirements identified and documented
- Findings presented to and validated by client
- Architecture/approach confirmed (software projects)
- Discovery report delivered

### Gate 3: Development → Delivery
- Draft deliverables reviewed by client
- Feedback incorporated
- Quality review completed internally
- Working software demonstrated (software projects)
- No critical risks unmitigated

### Gate 4: Delivery → Close
- Final deliverables accepted by client
- User training completed (software projects)
- Deployment verified (software projects)
- Final presentation delivered (advisory projects)
- Invoice submitted

### Gate 5: Close
- Lessons learned captured
- Client feedback collected
- Handover documentation complete
- Next opportunity identified (if applicable)
- Project archived

---

## PRINCE2 Overlay (Major Tier, Government Clients)

For major tier projects with government clients, map marcov.GATE terminology to PRINCE2:

| marcov.GATE | PRINCE2 Equivalent |
|-------------|-------------------|
| Inception | Initiation Stage |
| Discovery | Specialist Stage 1 |
| Development | Specialist Stage 2 |
| Delivery | Final Delivery Stage |
| Close | Closing a Project |
| Gate Review | End Stage Assessment |
| `.project-status.json` | Highlight Report |
| Risk Register | Risk Register |
| Project Plan | Stage Plan |

See `references/prince2-mapping.md` for full mapping including documentation products.

---

## Templates Directory

The `templates/` directory contains HTML template files. When generating output:

1. Read the template file
2. Read `templates/base-styles.css` for the shared stylesheet
3. Inject the CSS inline into the `<style>` block
4. Inject project data as a `const PROJECT_DATA = {...}` or `const PORTFOLIO_DATA = [...]` JavaScript variable
5. Write the complete self-contained HTML file to the project repo

### Available Templates

| Template | Purpose | Output Filename |
|----------|---------|-----------------|
| `portfolio-dashboard.html` | Master kanban board across all projects | `PORTFOLIO_DASHBOARD.html` |
| `project-dashboard.html` | Per-project 3-tab dashboard | `PROJECT_DASHBOARD.html` |
| `client-status-report.html` | Branded client-facing status page | `CLIENT_STATUS_REPORT.html` |
| `gate-review-report.html` | Gate review outcome report | `GATE_REVIEW_[phase].html` |

---

## File Discovery Pattern

The `.project-status.json` file enables portfolio-level discovery:

1. **Location**: Root of each project repository
2. **Discovery path**: `~/Documents/Repos/**/.project-status.json`
3. **Sweep agent**: `agents/portfolio-sweep.md` dispatches `scripts/sweepProjects.py`
4. **Staleness**: Projects not updated in 14+ days are flagged
5. **Aggregation**: All discovered projects rendered into the portfolio dashboard

This pattern mirrors the existing `.note.md` pattern (weekly work notes at a well-known path) and `taskInbox.md` (task capture at a central path), but is decentralised — each repo owns its own state.
