# Codebase Structure

**Analysis Date:** 2026-02-25

## Directory Layout

```
SASAMClaudeCodeSkills/
├── README.md                          # Project overview, skill descriptions, setup instructions
├── setup.sh                           # Initial setup: installs git hooks and registers commands
├── register-commands.sh               # Registers all SKILL.md files as ~/.claude/commands/
├── .hooks/                            # Git hooks for auto-registration
│   ├── post-checkout                  # Triggers register-commands.sh after branch changes
│   └── post-merge                     # Triggers register-commands.sh after merges
├── .planning/                         # Planning and analysis documents
│   └── codebase/                      # Architecture and structure analysis (this directory)
│       ├── ARCHITECTURE.md
│       └── STRUCTURE.md
├── .claude-plugin/                    # Root plugin metadata
│   └── marketplace.json               # Plugin marketplace listing for all skills
│
├── sas-presentation/1.0.0/            # SAS-AM branded presentation skill
│   ├── README.md                      # Skill overview and usage
│   ├── .claude-plugin/
│   │   ├── plugin.json                # Plugin metadata (name, version, keywords)
│   │   └── marketplace.json
│   └── skills/sas-presentation/
│       ├── SKILL.md                   # Main skill instructions (discovery, narrative structure, technical specs)
│       └── references/                # Reveal.js template, CSS, brand guidelines
│           ├── reveal.html            # Reveal.js base template with SAS branding
│           └── [assets]/              # Images, logos (light/dark variants)
│
├── b2b-research-agent/1.0.0/          # B2B prospect research and qualification skill
│   ├── README.md
│   ├── .claude-plugin/
│   │   ├── plugin.json
│   │   └── marketplace.json
│   └── skills/b2b-research-agent/
│       ├── SKILL.md                   # Main skill: discovery questions, research phases, BEAM Stage 1 readiness
│       └── references/
│           ├── prospect-dossier-template.md         # Output structure for research findings
│           ├── event-brief-template.md              # Pre-conference engagement planning
│           ├── outreach-templates.md                # Email and call script templates
│           └── pipeline-template.md                 # Prospect list formatting
│
├── beam-selling/1.0.0/                # marcov.BEAM evidence-gated sales pipeline
│   ├── README.md
│   ├── .claude-plugin/
│   │   ├── plugin.json
│   │   └── marketplace.json
│   └── skills/beam-selling/
│       ├── SKILL.md                   # Core skill (1129 lines): 6-stage pipeline, gate criteria, state mgmt, kanban board
│       └── references/
│           ├── beam-state-template.json             # Engagement JSON schema (metadata, stages, stakeholders, activity log)
│           ├── kanban-board-template.html           # Interactive dashboard (injected with BEAM_DATA variable)
│           ├── engagement-tracker-template.md       # Session log structure
│           ├── stage-gate-checklist.md              # Gate criteria summary
│           ├── spin-question-bank.md                # SPIN questions by stage and topic
│           └── proposal-template.md                 # Proposal structure (exec summary, findings, solution, investment)
│
├── data-quality-analysis/1.0.0/       # ABS Data Quality Framework assessment
│   ├── README.md
│   ├── .claude-plugin/
│   │   ├── plugin.json
│   │   └── marketplace.json
│   └── skills/data-quality-analysis/
│       ├── SKILL.md                   # Main skill: discovery, ABS 7 dimensions, analysis workflow, report generation
│       └── references/
│           ├── report-template.md                   # Quality assessment output format
│           └── sample-report.md                     # Example completed report
│
├── linkedin-post-generator/1.0.0/     # LinkedIn content generation for SAS-AM voice
│   ├── README.md
│   ├── .claude-plugin/
│   │   └── plugin.json
│   └── skills/linkedin-post-generator/
│       ├── SKILL.md                   # Main skill: voice & tone, post types, hooks, CTAs
│       └── references/
│           ├── pillar-post-template.md             # Article promotion post format
│           └── insight-post-template.md            # Standalone thought leadership format
│
├── vicTenders/tender-assessment/1.0.0/ # Victorian government tender assessment
│   ├── README.md
│   ├── assess_tenders.py              # Python script for alignment scoring and pursuit generation
│   ├── vic_tenders_scraper.py         # Scraper for tenders.vic.gov.au
│   ├── .claude-plugin/
│   │   └── plugin.json
│   └── skills/tender-assessment/
│       ├── SKILL.md                   # Main skill: scraping, scoring matrix, pursuit packages
│       └── references/
│           ├── company-profile.md                   # marcov capabilities and constraints
│           ├── scoring-matrix.md                    # Weighted alignment criteria
│           ├── shortlist-report-template.md         # Tender assessment summary
│           ├── pursuit-package-template.md          # Full go/no-go analysis template
│           ├── output-schema.json                   # Expected output structure
│           └── sample-output.json                   # Example tender assessment results
│
└── test-reports/                      # Test case results and example outputs
    └── bega-cheese/                   # Example test case (B2B research output)
```

## Directory Purposes

**Root Level:**
- Purpose: Project metadata and setup automation
- Contains: README, setup scripts, git hooks, main plugin config
- Key files: `register-commands.sh` (command registration logic)

**Each Skill Directory** (e.g., `beam-selling/1.0.0/`):
- Purpose: Encapsulate a single Claude Code task/agent
- Contains: Plugin metadata, skill instructions, reference templates
- Key files: `SKILL.md` (the executable skill), `plugin.json` (registration metadata)

**`skills/{skill-name}/` Subdirectory:**
- Purpose: Actual skill implementation and supporting materials
- Contains: `SKILL.md` (main skill instructions) and `references/` (templates)

**`references/` Subdirectory in Each Skill:**
- Purpose: Provide templates, examples, schemas, and guidance documents
- Examples:
  - `beam-selling/references/beam-state-template.json` — JSON schema for engagement state
  - `beam-selling/references/spin-question-bank.md` — Library of SPIN questions
  - `b2b-research-agent/references/prospect-dossier-template.md` — Dossier structure

**`.beam/` Directory** (created at runtime in user's working directory):
- Purpose: Persistent engagement and session state
- Contains:
  - `engagements/{company}.json` — Complete engagement state for a BEAM sales opportunity
  - `engagements/{company}-kanban.html` — Regenerated dashboard at every session end
  - `sessions/{company}-{date}.md` — Session logs with learnings and next steps
  - `config.json` — Seller company info (cached)

## Key File Locations

**Entry Points:**

- `README.md`: Project overview, skill descriptions, installation instructions
- `setup.sh`: Initial setup script (calls `register-commands.sh`)
- `register-commands.sh`: Finds all SKILL.md files and copies to `~/.claude/commands/`
- `./hooks/post-checkout` and `post-merge`: Git hooks that trigger auto-registration

**Skill Instructions:**

- `sas-presentation/1.0.0/skills/sas-presentation/SKILL.md`: Create Reveal.js presentations
- `b2b-research-agent/1.0.0/skills/b2b-research-agent/SKILL.md`: Research B2B prospects
- `beam-selling/1.0.0/skills/beam-selling/SKILL.md`: Guide 6-stage sales pipeline (1129 lines)
- `data-quality-analysis/1.0.0/skills/data-quality-analysis/SKILL.md`: Assess data using ABS framework
- `linkedin-post-generator/1.0.0/skills/linkedin-post-generator/SKILL.md`: Write branded posts
- `vicTenders/tender-assessment/1.0.0/skills/tender-assessment/SKILL.md`: Assess government tenders

**Core Reference Files:**

- `beam-selling/1.0.0/skills/beam-selling/references/beam-state-template.json`: Engagement state schema
- `beam-selling/1.0.0/skills/beam-selling/references/kanban-board-template.html`: Dashboard template
- `beam-selling/1.0.0/skills/beam-selling/references/spin-question-bank.md`: SPIN question library
- `b2b-research-agent/1.0.0/skills/b2b-research-agent/references/prospect-dossier-template.md`: Dossier structure
- `data-quality-analysis/1.0.0/skills/data-quality-analysis/references/report-template.md`: Quality report format

**Python Scripts:**

- `vicTenders/tender-assessment/1.0.0/vic_tenders_scraper.py`: Scrapes tenders.vic.gov.au
- `vicTenders/tender-assessment/1.0.0/assess_tenders.py`: Scores tenders and generates pursuit packages

## Naming Conventions

**Files:**
- `SKILL.md` — Main skill instructions (YAML frontmatter + Markdown content)
- `plugin.json` — Plugin metadata in JSON format
- `README.md` — Documentation for each skill or directory
- `{descriptor}-template.md` or `{descriptor}-template.json` or `{descriptor}-template.html` — Templates for output generation
- `{descriptor}-schema.json` — JSON schema defining output structure
- `sample-{descriptor}.json` or `sample-output.json` — Example/reference output

**Directories:**
- `{skill-name}/` — Skill root (e.g., `beam-selling/`, `b2b-research-agent/`)
- `1.0.0/` — Version directory (semantic versioning)
- `.claude-plugin/` — Plugin metadata
- `skills/{skill-name}/` — Skill implementation
- `references/` — Templates and supporting materials
- `.beam/` — Runtime state (created by BEAM skill in working directory)
- `.hooks/` — Git hooks for auto-registration

## Where to Add New Code

**New Skill:**
1. Create directory: `{new-skill-name}/1.0.0/skills/{new-skill-name}/`
2. Create `SKILL.md` with YAML frontmatter (name, description)
3. Create `references/` subdirectory with any templates
4. Create `1.0.0/.claude-plugin/plugin.json` with metadata
5. Running `register-commands.sh` will automatically register it

**New Template or Reference:**
1. Add file to `{skill-name}/1.0.0/skills/{skill-name}/references/`
2. Reference it in SKILL.md as: `references/{filename}.md` or `\`references/{filename}.json\``
3. `register-commands.sh` will convert relative references to absolute paths when registering

**New Skill Variant or Feature:**
- Modify the relevant `SKILL.md` file
- Add new templates to `references/`
- No code compilation needed — changes take effect on next invocation

**Testing/Examples:**
- Add to `test-reports/{client-name}/` directory with example outputs
- These serve as reference implementations and test cases

## Special Directories

**`.planning/codebase/`:**
- Purpose: Architecture and structure analysis documents
- Generated: By `/gsd:map-codebase` command
- Committed: Yes, to git (documents how the codebase is structured)
- Contains: ARCHITECTURE.md, STRUCTURE.md, CONVENTIONS.md, TESTING.md, STACK.md, INTEGRATIONS.md, CONCERNS.md

**`.beam/`:**
- Purpose: Runtime engagement and session state (created in user's working directory)
- Generated: Yes, by `beam-selling` skill at runtime
- Committed: No, local-only (user should back up manually)
- Contains:
  - Engagement JSON files (one per prospect)
  - Session logs (Markdown)
  - Regenerated kanban HTML
  - Seller config (cached)

**`.hooks/`:**
- Purpose: Git hooks for auto-registration
- Generated: No (pre-committed)
- Committed: Yes
- Contains: `post-checkout`, `post-merge` scripts that call `register-commands.sh`

**`.claude-plugin/`:**
- Purpose: Plugin marketplace and registration metadata
- Generated: No (pre-committed)
- Committed: Yes
- Contains: `plugin.json` with name, version, description, keywords; `marketplace.json` with listing info

**`test-reports/`:**
- Purpose: Example outputs and test case results
- Generated: By running skills with test inputs
- Committed: Yes (examples for future reference)
- Contains: Example client dossiers, research outputs, assessment reports

## Default Behavior and Paths

**Command Registration:**
- Default location for registered commands: `~/.claude/commands/{skill-name}.md`
- Triggered by: `setup.sh` → `register-commands.sh`
- Auto-triggered by: Git hooks (post-checkout, post-merge)

**Engagement State Location:**
- Default: `.beam/` directory in user's current working directory
- Path format: `.beam/engagements/{company-slug}.json`
- Cannot be overridden — BEAM skill always uses `.beam/` in cwd

**Template Paths in Registered Commands:**
- Original: `references/template.md` (relative)
- Registered: `/full/path/to/skill/references/template.md` (absolute)
- Conversion: Done by `register-commands.sh` using sed

---

*Structure analysis: 2026-02-25*
