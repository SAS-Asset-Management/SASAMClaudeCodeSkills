# Architecture

**Analysis Date:** 2026-02-25

## Pattern Overview

**Overall:** Plugin-based skill composition model — each skill is an autonomous Claude Code task/agent that handles a specific business workflow. Skills are loosely coupled, referenced through standards (JSON schemas, templates, file paths), and can be invoked independently or chained together through shared input/output formats.

**Key Characteristics:**
- **Modular skill design** — Each skill (`beam-selling`, `b2b-research-agent`, `data-quality-analysis`, etc.) encapsulates a complete workflow
- **Frontmatter-driven discovery** — Skills use YAML frontmatter (name, description) for registration and invocation
- **Reference templates** — Each skill includes `references/` directory with templates, schemas, and guidance documents
- **Local state persistence** — Skills save engagement/project state locally (`.beam/`, session logs, JSON files) to survive context resets
- **Evidence-gated progression** — BEAM selling skill enforces gate criteria; other skills follow structured discovery/assessment patterns
- **No build step** — Presentations are standalone HTML; Python scripts are executed directly; Markdown is rendered as-is

## Layers

**Skill Layer:**
- Purpose: Individual Claude Code tasks that guide users through structured workflows
- Location: Each skill lives in `{skill-name}/1.0.0/skills/{skill-name}/SKILL.md`
- Contains: SKILL.md (main instructions), references/ (templates, examples, config)
- Depends on: Reference templates, reference files, local file system for state persistence
- Used by: Claude Code agent invocations via `/skill-name` command

**Plugin/Registration Layer:**
- Purpose: Make skills discoverable and invokable as slash commands
- Location: `{skill-name}/1.0.0/.claude-plugin/plugin.json`
- Contains: Plugin metadata (name, description, version, keywords)
- Depends on: `register-commands.sh` to copy SKILL.md files to `~/.claude/commands/`
- Used by: Claude Code command registry (looks up skills in `~/.claude/commands/`)

**Reference/Template Layer:**
- Purpose: Provide structured guidance, output schemas, and example data
- Location: `{skill-name}/1.0.0/skills/{skill-name}/references/`
- Contains: Markdown templates, JSON schemas, HTML dashboards, example reports
- Examples:
  - `beam-selling/references/beam-state-template.json` — JSON schema for engagement state
  - `beam-selling/references/kanban-board-template.html` — Interactive kanban dashboard template
  - `b2b-research-agent/references/prospect-dossier-template.md` — Dossier structure
  - `data-quality-analysis/references/report-template.md` — Quality assessment report format
- Used by: Skill instructions when generating outputs

**State Persistence Layer:**
- Purpose: Store and resume long-running engagements across sessions
- Location: Hidden `.beam/` directory in working directory; skill-specific session logs
- Contains:
  - `.beam/engagements/<company>.json` — Complete engagement state for BEAM sales
  - `.beam/sessions/<company>-<date>.md` — Session logs with learnings and next steps
  - `.beam/engagements/<company>-kanban.html` — Regenerated at each session end
  - `.beam/config.json` — Seller company context (cached after first input)
- Used by: BEAM selling skill for resuming engagements; other skills for multi-session projects

**Git Hook Layer:**
- Purpose: Auto-register commands when repository changes
- Location: `.hooks/` directory
- Contains: `post-checkout`, `post-merge` scripts
- Used by: Git to trigger `register-commands.sh` after pull/checkout/merge

## Data Flow

**Skill Invocation Flow:**

1. **User calls `/beam-selling Acme Corp`**
2. **Skill initialization checks for existing state** in `.beam/engagements/acme-corp.json`
3. **If resuming**: Load JSON state + most recent session log, display resume summary, ask for offline updates
4. **If new**: Ask discovery questions (seller context, problem domain, engagement goal)
5. **Skill runs the session** — guides user through stage activities, captures evidence, assesses gates
6. **At session end, auto-dump**:
   - Update engagement JSON with new evidence, gate status, win probability, activity log
   - Regenerate kanban HTML by injecting JSON as `BEAM_DATA` variable
   - Write session log with learnings and next steps
7. **Print resume hint** so user can pick up next time

**Research-to-Sales Flow (B2B Research → BEAM Selling):**

1. **User calls `/b2b-research-agent [Company]`**
2. **Skill conducts discovery** about seller's offering, problem domain, engagement goal
3. **Skill researches company** — financials, org structure, decision-makers, pain points
4. **Skill produces HTML dossier** with BEAM Stage 1 readiness assessment
5. **User calls `/beam-selling [Company]` with dossier available**
6. **BEAM skill detects research output**, ingests it as Stage 1 foundation
7. **User progresses through Stages 2-6**, with BEAM skill guiding stage-by-stage

**State Management:**

- **Engagement state** lives in `.beam/engagements/<company>.json` — single source of truth
- **Session context** lives in markdown session logs — human-readable narrative
- **Kanban dashboard** regenerated from JSON at every session end — UI reflects JSON state
- **All state is local** — no cloud sync; user owns all data

## Key Abstractions

**BEAM Pipeline:**
- Purpose: Define a 6-stage evidence-gated sales process
- Examples: `beam-selling/SKILL.md` lines 56-341 define each stage (Qualify → Diagnose → Align → Propose → Commit → Deliver)
- Pattern: Each stage has gate criteria, minimum evidence bar (Specificity/Source/Recency tests), SPIN questions, and required evidence documentation
- Gate enforcement is non-negotiable — skill refuses advancement without evidence

**Evidence & Gate Assessment:**
- Purpose: Ensure progression is earned, not claimed
- Pattern: User provides evidence → skill runs three quality tests → verdict (PASS/INSUFFICIENT/MISSING)
- Example gate from Stage 1: `beam-selling/SKILL.md` lines 88-101 show gate "Access to authority" with examples of accepted vs rejected evidence
- Used across BEAM skill for every stage transition

**Kanban as Engagement Dashboard:**
- Purpose: Visual tracking of activities, evidence, blockers, questions across all 6 BEAM stages
- Pattern: JSON kanban array (each card has id, type, status, notes, gate_ref) → injected into HTML template → standalone file
- Card types: Research, Meeting, Evidence, Document, Stakeholder, Blocker, Question
- Regenerated at every session end so it always reflects current engagement state
- Example: `beam-selling/references/kanban-board-template.html` with JavaScript that reads `BEAM_DATA` variable

**Skill Reference Template Pattern:**
- Purpose: Provide reusable, copy-paste-able templates and guidance
- Pattern: Each skill has `references/` directory with templates in multiple formats (JSON, Markdown, HTML)
- Examples:
  - `beam-selling/references/spin-question-bank.md` — Library of SPIN questions
  - `b2b-research-agent/references/outreach-templates.md` — Email and call templates
  - `data-quality-analysis/references/report-template.md` — Quality assessment structure
- Users copy/adapt templates rather than building from scratch

**Local Engagement Persistence:**
- Purpose: Survive context resets and multi-session workflows
- Pattern: JSON state file + session logs + regenerated HTML dashboard
- Example: `.beam/engagements/acme-corp.json` contains all engagement metadata, stage progress, stakeholders, evidence, win probability, activity log
- Session logs are appended, never overwritten — full audit trail

## Entry Points

**Main Repository Entry:**
- Location: `README.md`
- Triggers: User cloning repo or viewing project
- Responsibilities: Describe all 5 skills, show installation steps (setup.sh, register-commands.sh), explain usage patterns

**Skill Registration:**
- Location: `register-commands.sh`
- Triggers: `setup.sh` or git hooks (post-checkout, post-merge)
- Responsibilities: Find all SKILL.md files, extract skill name from YAML frontmatter, copy to `~/.claude/commands/` with absolute paths resolved

**Individual Skill Entry Points:**
- Location: Each `{skill-name}/1.0.0/skills/{skill-name}/SKILL.md`
- Triggers: User invocation like `/beam-selling Acme Corp` or `/b2b-research-agent Research BHP`
- Responsibilities: Run discovery (if needed), conduct workflow (stage-by-stage for BEAM, research phases for B2B, etc.), generate outputs, save state

**Tender Assessment Entry:**
- Location: `vicTenders/tender-assessment/1.0.0/skills/tender-assessment/SKILL.md`
- Triggers: `/tender-assessment` or direct Python execution
- Responsibilities: Scrape tenders.vic.gov.au, score alignment, generate pursuit packages
- Supported by: `vic_tenders_scraper.py` and `assess_tenders.py` for execution

## Error Handling

**Strategy:** Graceful degradation with explicit messaging. Skills do not fail silently; they document blockers and ask for resolution.

**Patterns:**

1. **Missing Evidence** — BEAM skill marks gate as INSUFFICIENT or MISSING, explains what's needed, refuses advancement
2. **Missing References** — If a template or reference file is not found, skill reports the missing path and suggests remediation
3. **State Not Found** — B2B Research or BEAM Selling skill checks for `.beam/` directory; if not found, starts fresh or offers to create
4. **User Pushback on Gates** — BEAM skill responds with specific gap identification and guided questions (see `beam-selling/SKILL.md` lines 775-792)
5. **Data Quality Issues** — Data Quality Analysis skill marks dimensions as "UNABLE TO ASSESS" with specific info needed rather than forcing a rating

## Cross-Cutting Concerns

**Logging:** Each skill maintains session logs (`{skill-name}-{date}.md`) in `.beam/sessions/` or equivalent. Logs include what was covered, key learnings, evidence collected, gate progress, decisions made, and next steps.

**Validation:** Gate criteria validation in BEAM skill is strict — three tests (Specificity, Source, Recency) must pass. Other skills have discovery questions that validate user understanding before proceeding.

**Authentication:** Not applicable — all skills are Claude-native, no external authentication. External integrations (tender scraper hitting tenders.vic.gov.au) are read-only web requests.

**Persistence:** All multi-session state is stored locally in working directory. No cloud backend. User is responsible for backing up `.beam/` directory.

**Template Customization:** Users can modify reference templates in-place (e.g., edit `beam-selling/references/spin-question-bank.md` to add domain-specific questions). Changes persist in repo for future use.

---

*Architecture analysis: 2026-02-25*
