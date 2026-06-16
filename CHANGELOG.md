# Changelog

All notable changes to SASAMClaudeCodeSkills will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.20.1] - 2026-06-16

### Fixed
- **generate-manifest.sh** now sources its file list from `git ls-files` (tracked files only) instead of walking the filesystem with `find`. The old approach swept untracked local cruft into the release manifest — `.notifications/config.json` (gitignored) and `sasam-local-patches/.../marketplace.json` (the `/sasam-update` backup dir) — producing phantom entries that fail integrity checks for any user who lacks those local dirs. The extension allow-list and path exclusions are preserved. Regenerated the manifest (232 → 230 real, tracked files).
- **marketplace.json** — the `sasam-core` registry entry still advertised `1.0.0` with the pre-loopBuilder description after the plugin bumped to `1.1.0` in 1.20.0. Updated version, description, keywords and tags to match `plugin.json`, so consumers discovering/installing the plugin see consistent metadata.

## [1.20.0] - 2026-06-16

### Added
- **sasam-core / `/loopBuilder`** New skill — designs a well-formed autonomous agent loop for a given subject, then launches it. Built on the Cherny "write loops, not prompts" / Karpathy "autonomy slider" framing: move up a level of abstraction from hand-prompting each step to specifying **outcomes plus verification** and letting the agent run the `context → decide → tool → result` cycle until a stop condition trips. The skill is **inspect-first** — it scans the working directory (repo shape, runnable test/build commands, available skills + tools, git state) and drafts a candidate loop against the five-part anatomy (**goal · context · action policy · verification · stop condition**) before asking the user anything, then confirms only the gaps. It **refuses to launch** without all four mandatory guardrails — explicit stop condition, iteration/budget cap, verification method, and a no-progress/drift detector — directly countering the dominant failure mode (expensive drift, infinite retries). The **design picks the substrate**: an in-session `/loop` for supervised single-prompt cycles, or a multi-agent `Workflow` for parallel fan-out/verify loops (no cron path — loops run now). A **pre-launch gate** renders the full design (approve / edit / cancel) before any autonomous work starts, and the skill pushes back honestly when a task isn't loop-shaped (no verifiable end-state, single-pass work, undefinable stop condition). `sasam-core/1.0.0/skills/loopBuilder/SKILL.md`. sasam-core plugin bumped `1.0.0 → 1.1.0`.

## [1.19.0] - 2026-06-16

### Added
- **ensemble — local-stdio MCP server.** New `ensemble/1.0.0/mcp/ensemble_mcp_server.py` (FastMCP, stdio; `+ requirements.txt + README.md`) gives a tethered consultant's Claude Code session first-class read+write `ensemble_*` tools over the Ensemble operational API — instead of every skill hand-rolling HTTP. It runs **locally** on the consultant's box and calls the Tailscale-only API; secrets (api_url/api_key/import_key/verify_tls) are read from `~/.ensemble/config.json` (the established per-user state file, mode 0600), **never** from the repo-shared `.mcp.json`. Tool catalogue spans approvals (list/transition), HMI tasks (list/assign/update), projects + gate decisions, opportunities + CRM, issue-flags, imports (beam-lead + proposal) and research (submit/list/results). HTTP errors are returned verbatim (a 422 invalid-transition or a 403 scope rejection is actionable, not silent). The server **complements** the git-queue → PR → tier-gate handoff (the audited deliverable path) — it never submits deliverables. Declared per-engagement via the template's `.mcp.json` (launched with `uv run --with mcp --with httpx`). Approvals/research/import-beam-lead tools work today (X-API-Key / X-Import-Key); the hmi/projects/crm/issue-flags tools are gated on theEnsembles' hardened-auth backend change (typed `Principal`/`get_principal` + default-deny route allowlist + per-engagement scoping), and `ensemble_import_proposal` awaits the backend `POST /import/proposal` route. Ensemble plugin bumped `1.2.0 → 1.3.0`.

### Changed
- **ensemble / `/init-engagement`** The placeholder-fill loop now also renders **`.claude/CLAUDE.md`** (the engagement working-agreement doc shipped by the template's new `.claude/` scaffold), so its `{{project_name}}`/`{{scope_tag}}`/`{{founder_handle}}`/`{{tailnet}}` tokens fill at init like the root `CLAUDE.md`/`.ensemble/project.json`/`.lfsconfig`. Without this a new engagement would render the working-guide with raw `{{…}}` placeholders.

## [1.18.0] - 2026-06-15

### Added
- **sasdocx (SASdocX)** New plugin — a SAS-AM on-brand document generator that learns a company's existing Word, PowerPoint or Excel template once into a reusable **Brand Profile**, then generates unlimited on-brand `.docx`/`.pptx`/`.xlsx` from it, with **off-brand output impossible by construction** (no generator writes a literal style name, hex colour or font — those live only in the profile, and `verify` refuses anything the template doesn't contain). Ships **three skills over one shared OOXML engine** — `/sasdocx` (Word), `/saspptx` (PowerPoint), `/sasxlsx` (Excel) — each exposing the same verbs `extract → comprehend (optional, model-driven) → verify → generate`, plus the learning verbs `learn`/`propose-overrides`/`refine`. The deterministic core runs fully offline (no model required); model-assisted verbs sit on top, fail-closed. Excel fills preserve formulas and brand number formats; Word/PowerPoint follow the template's real structural order, masters and layouts. Vendored at `sasdocx/0.10.0/` with the Python engine (`scripts/sasdockit/`, launched via `scripts/cli.py`), reference docs, synthetic example templates, and the full 936-test suite (verified green after rebrand). Requires Python ≥ 3.10 (`python-docx`, `python-pptx`, `openpyxl`, `lxml`, `Pillow`); optional LibreOffice + Poppler enable the visual QA gate (`python sasdocx/0.10.0/scripts/cli.py doctor`).

### Attribution
- **sasdocx** is a SAS-AM rebrand of the MIT-licensed [`brand-docs`](https://github.com/ferdinandobons/brand-docs) project by Ferdinando Bonsegna. Product names, command/skill identifiers (`sasdocx`/`saspptx`/`sasxlsx`), the engine package (`sasdockit`), env var (`SASDOCX_ROOT`) and user-facing text were renamed; the original MIT `LICENSE`, `NOTICE` and `CITATION.cff` are retained in full.

## [1.17.0] - 2026-06-13

### Added
- **ensemble / `/publish-presentation`** New consultant command — publishes a finished conference deck (a `sas-presentation` reveal.js build) straight to the SAS-AM **contentLibrary** container, so it goes live in the `team.sas-am.com` content library alongside the existing catalogue (maximoLive2025, AMPEAK2024, …). Unlike `/handoff` (work *for* the fleet) and `/submit` (engagement work *in*), this is a **direct publish** over Tailscale — no engagement repo, no GitHub control plane, no poller. It reuses the contentLibrary app's existing `POST /api/presentations/create` API (the tailnet is the trust boundary, like the data plane). The skill **flattens** the deck to a single self-contained HTML (inlines local CSS/JS/images/fonts as `data:` URIs; CDN/remote refs stay remote — the publish API stores one file), runs a **warn-only QA** pass (Australian English, SAS palette `#002244`/`#69BE28`, the SAS-AM tagline, `<img>` alt text, slide count, and any surviving local refs that would 404), pre-flights endpoint reachability, refuses on an id collision (the API can't overwrite), then POSTs the deck. Endpoint defaults to the baked tailnet URL (`cortex-t4.<tailnet>.ts.net:8081`), overridable via `presentations_endpoint` in `~/.ensemble/config.json`. Not engagement-scoped (no `/tether` required). `--dry-run` flattens + QAs without publishing. Verified end-to-end against the live container (publish → render → catalogue entry → cleanup). `publish-presentation/{SKILL.md,publish_presentation.sh,flatten_assets.py,presentation_qa.py}`; bash + python3 stdlib + `curl`. Ensemble plugin bumped `1.1.0 → 1.2.0`.

## [1.16.1] - 2026-06-13

### Fixed
- **ensemble / `/init-engagement`** Fixed a template-propagation race: `gh repo create --template` populates the new repo's scaffold **asynchronously**, so the immediate `git clone` could land an empty repo (no `CLAUDE.md`/`.ensemble/project.json`/`scripts/`), which then silently produced an unscaffolded, unprotected engagement. The skill now waits (polls the contents API) for a sentinel template file to appear before cloning, re-pulls if the working clone is still empty, and hard-fails with a re-run hint rather than proceeding without a scaffold. Verified end-to-end (repo created from template, scaffold filled, `queue`+protected `main` with the `tier-gate` check, registry row, tether).

## [1.16.0] - 2026-06-13

### Added
- **ensemble / `/init-engagement`** New consultant command — the onboarding step the protocol was missing. `/tether` and `/handoff` both assume the engagement already exists; when it doesn't, the consultant hit a dead-end (the v1.2 spec's founder-tier `init-project` was never built). `/init-engagement` stands a new engagement up end-to-end: creates `<owner>/sasam-<scope_tag>` from the `sasam-engagement-template`; fills the scaffold (root `CLAUDE.md` from `templates/CLAUDE.md.tmpl`, `.ensemble/project.json`, `.lfsconfig`) and pushes `main`; applies the two-branch model via the repo's `scripts/apply-branch-protection.sh` (the `queue` mailbox + protected `main` + the `tier-gate` required check + `tier:*` labels); registers `{uuid,name,scope_tag,repo,status:active}` in `sasam-registry`; and tethers the session so `/handoff` works immediately. Idempotent / re-runnable (every external mutation is create-if-not-exists); `--dry-run` previews with no changes; `--cleanup <scope_tag>` tears down a throwaway. Founder-run (needs org-admin `gh` + registry push). `init-engagement/{SKILL.md,init_engagement.sh,init_engagement_state.py}`; bash + python3 stdlib + `gh`/`git`. Ensemble plugin bumped `1.0.0 → 1.1.0`.

### Changed
- **ensemble** Dead-end abort messages are now actionable — `ens_require_tethered` (no `.ensemble/project.json`) and `/tether`'s no-match / empty-registry paths now point to `/init-engagement` to stand one up.

## [1.15.0] - 2026-06-13

### Added
- **handoff-proposal** New standalone plugin/skill — the proposal sibling of `import-beam-leads`. Hands an externally-authored proposal **into** the Ensemble opportunities pipeline (the reverse of the normal flow, where a proposal is an *output* of a stage-4 deal). A consultant points it at a finished proposal — a **PDF**, single-page **HTML**, or **structured JSON** (`proposal_sections` / `client_problem_map` / `timeline_weeks` / `case_study_references`) — for a company; the stdlib-only `handoff_proposal.py` base64s the artefact and POSTs to the Ensemble's `POST /api/import/proposal` intake over **Tailscale** (`ENSEMBLE_API_URL` + `ENSEMBLE_IMPORT_KEY`, sent as `X-Import-Key`). The intake finds-or-creates the opportunity by company, advances it to the BEAM **"Propose"** stage (never regressing a Commit/Deliver deal), and attaches the proposal as a `PENDING_APPROVAL` proposal — visible on the opportunity's **Proposals** rail and in the founder's approval queue, with the inbound handoff recorded as a radar-replay beam. Idempotent on company; `--dry-run` previews the body before sending. Pairs with theEnsembles `POST /api/import/proposal` (PR #142). `handoff-proposal/{SKILL.md,handoff_proposal.py}`; stdlib `urllib` only — no pip install.

## [1.14.1] - 2026-06-11

### Fixed
- **ensemble** Hardening from GitHub Copilot's PR review across `/tether`, `/submit`, and the onboarding deck. `/tether`: option parsing shifts by two only when a value is present (a trailing `--query`/`--mode`/`--dir` shows guidance instead of aborting), and `tether_state.py` usage lists the new `list` subcommand. `/submit`: `requested_by` never falls back to `git config user.name` (a name with spaces would make `tier-gate` unsatisfiable) — it requires a valid GitHub login; refuses a stale local `handoffs/outbox/<id>/`; errors when two artefacts share a filename; propagates `submit_state.py`'s own exit code; and fails loudly (no false "PR opened") when `gh pr create` fails; the summary uses its placeholder when evidence is empty. Onboarding deck: the display-only terminal no longer shows a copy cursor, and clipboard copy guards for a missing Clipboard API with an off-screen textarea fallback.

## [1.14.0] - 2026-06-11

### Added
- **ensemble / `/submit`** New consultant command to land work the consultant did **themselves** (offline, in a workshop) as a **reviewed deliverable**. Where `/handoff` queues work *for* the fleet, `/submit` brings finished work *in*: it interviews the consultant, matches the work to the engagement's **deliverables** ("Lars's delivery page" — reads `.ensemble/deliverables.json` when present, otherwise a free interview), and opens a **PR into `main`** carrying a self-contained result set under `handoffs/outbox/<id>/` — a schema-valid `packet.md` (so `tier-gate` reads the right review tier + requester), a human `summary.md`, a structured `submission.json` of the deliverable claims, and the artefact(s) (with a >10MB-non-LFS guard). Defaults to the `full` review tier (the submitter approves). `submit/{submit.sh,submit_state.py,SKILL.md}`; stdlib/bash + `gh`/`git` only.

## [1.13.1] - 2026-06-11

### Fixed
- **ensemble / `/tether`** Made the first tether seamless for a brand-new consultant — three first-run walls removed. **Registry auto-config:** `registry_repo` now defaults to the SAS-AM shared registry (`SAS-Asset-Management/sasam-registry`) and is persisted, so there's no manual `~/.ensemble/config.json` step. **No SSH keys:** the skill runs `gh auth setup-git` before cloning, so private engagement repos clone over HTTPS via the GitHub CLI credential helper — `gh auth login` (already in onboarding) is sufficient. **No-arg listing:** `/tether` with no engagement name (or `--list` / `*` / `all`) now lists the engagements you can tether to instead of erroring. **Auto-mode:** clone-vs-remote is auto-detected (remote if the cwd is a git repo, else clone) — the skill no longer asks. **Forgiving match:** engagement resolution is punctuation/spacing-insensitive with token-subset matching, so `transurban WCX NCX` resolves `Transurban WCX/NCX` / `transurban-wcx-ncx`.

## [1.13.0] - 2026-06-11

### Added
- **ensemble** New consultant workflow plugin packaging the five SAS-AM Ensemble engagement commands — **`/tether`** (bind the session to an engagement repo: clone/remote-add, fetch `main`+`queue`, orient), **`/handoff`** (write a task packet and fast-forward push it to the engagement's `queue` branch for the Norbert-poller to claim; results return as a PR into `main`), **`/sync`** (read-only catch-up: merged results to collect, PRs awaiting review, bounced packets, claims in flight), **`/collect`** (pull merged result sets from `main`, materialise + sha256-verify LFS deliverables, record what was collected), and **`/status`** (registry-wide view across every tethered engagement — open packets, claims with age, open PRs by review tier, last poll heartbeat). Ships a **SessionStart hook** (`hooks/hooks.json` → `skills/hooks/session-start-ensemble.sh`) that prints a hard-time-boxed, read-only `/sync` greeting only inside a tethered engagement repo and is otherwise silent. Bundles the shared `_lib` (stdlib-only bash + Python helpers for packet parsing, schema validation, repo resolution, and `~/.ensemble` state I/O), a reference copy of `schemas/packet.schema.json`, and the "0 → 100" reveal.js onboarding deck. Sourced from the `theEnsembles` monorepo (`deploy/skills/ensemble/`); stdlib/bash + `gh`/`git`/`git-lfs` only, no pip installs, Australian English throughout.

## [1.12.0] - 2026-06-10

### Added
- **sas-am-docs** New asset-management document suite — a composable hub that authors the full ISO 55001 document family (**SAMP, AMP, TMP, RCM**) over a shared, code-grounded analytics engine (`sas-am-engine`). Implements the strategic-to-tactical line of sight (SAMP → AMP → TMP, with RCM/FMECA feeding maintenance tactics) with sub-skills `sas-samp`, `sas-tmp`, `sas-rcm`, an engine guide (`_engine-guide/ENGINE.md`), an enterprise-brain citation hook, and a bundled standards library (ISO 55000 line-of-sight, ISO 55001 clause map, SAE JA1011 / IEC 60812 / ISO 14224 reliability map). Owned by `larsFrederickson`; every document's numbers are computed from real audit/financial data, not estimated. The engine re-derives the reference LHG dataset byte-identically and renders professional, paginated A4 HTML + PDF.

## [1.11.0] - 2026-06-09

### Changed
- **nano-banana-2** Restructured the brand prompt architect into a **router** with four mode sub-files. The earlier abstraction-based modes (Node Network, Structured Progression, Order from Chaos) are removed entirely — they produced glowy tech-icon clichés. Subjects are now always **stylised, simplified real objects**, never pure abstraction.
- **nano-banana-2** New brand frame copy: "clean, sophisticated, intentional — the look of a high-end consultancy report or quality editorial publication. Flat with crisp clean edges; no outer glow, no halo, no soft luminous bloom, no glassy or frosted texture, no glossy 3D render." Green appears only as a precise, deliberate accent — never as a glow, haze, gradient field, starburst, or background light.

### Added
- **nano-banana-2** Four mode sub-files in `modes/`:
  - **Mode 1 — Editorial Diagram** (`mode-1-editorial-diagram.md`): explaining a concept, process, or relationship. Default mode.
  - **Mode 2 — Technical Line** (`mode-2-technical-line.md`): FMECA, reliability, asset hierarchies, Maximo data structure, equipment teardowns.
  - **Mode 3 — Data as Hero** (`mode-3-data-as-hero.md`): maturity assessments, Weibull, fleet simulation, analytics results.
  - **Mode 4 — Architectural** (`mode-4-architectural.md`): sector positioning, infrastructure, "who we serve".
- **nano-banana-2** Each mode sub-file contains: when-to-use criteria, the prompt template with `[FIXED BRAND FRAME]` placeholder, slot definitions, and one fully assembled worked example.
- **nano-banana-2** Plugin version bumped to 1.3.0.
- **b2b-research-agent** Fit-to-services, scope options, and build-out (Phase 6): the skill now assesses fit against our SAS-AM service lines, targets Director-level and above decision-makers, pitches a range of 2–4 engagement scopes each with a win probability, and asks which scope to build out through interview (handing off to beam-selling).
- **b2b-research-agent** Site Locations: a new research step that finds the prospect's physical sites (head office + operational facilities) with addresses and approximate coordinates, surfaced as a Site Locations table in the dossier and **plotted on an interactive map** (Leaflet + OpenStreetMap, no API key) in the HTML report. The map self-removes when there are no plottable sites. Wired into `report-template.html` and `prospect-dossier-template.md`.

## [1.10.0] - 2026-05-19

### Added
- **nano-banana-2** SAS-AM Brand Prompt Architect — primary mode that assembles a single natural-language image prompt from a piece of written content (LinkedIn post, blog article, slide topic, Webflow page). Separates a FIXED brand frame (visual style, colour, lighting, negative instruction) from VARIABLE per-image content (subject metaphor, composition directive, aspect, open-space region).
- **nano-banana-2** Three composition modes selected automatically from the source subject:
  - **A — Node Network:** connectivity, ML, multi-agent, federated, data flow → luminous nodes joined by fine threads
  - **B — Structured Progression:** maturity assessments, frameworks, governance, roadmaps → layered geometric tiers
  - **C — Order from Chaos:** data quality, analytics, diagnostics, raw-to-insight → particles resolving into a crystalline lattice
- **nano-banana-2** Aspect ratio handled as plain language inside the prompt body (no CLI flags): default `a wide 16:9 landscape composition`, plus `a square 1:1` and `a tall 4:5 portrait`.
- **nano-banana-2** Three worked examples in SKILL.md covering all three modes (edge federated ML, Yarra Trams MR5 governance maturity, worthless-data-to-intelligent-assets).

### Changed
- **nano-banana-2** Frontmatter description updated so the skill triggers on requests to generate image prompts, social or blog or presentation imagery, or SAS-AM visuals from written content.
- **nano-banana-2** Hyper-realistic photographic enhancement is now opt-in only (`--photoreal` or explicit user request), not the default. SAS-AM imagery routes through the Brand Prompt Architect.
- **nano-banana-2** Plugin version bumped to 1.2.0 to reflect the new primary mode.

## [1.9.1] - 2026-04-15

### Changed
- **sas-presentation** Share mode now uses the same Reveal canvas (1760 by 990) and `.reveal` font size as light/dark — text size matches across all three modes. The earlier 1440 by 810 share canvas made share mode text noticeably larger than the other modes.

## [1.9.0] - 2026-04-15

### Added
- **sas-presentation** New `share` theme mode, designed to survive Microsoft Teams and Zoom screen share compression:
  - Codec friendly colour palette: off white background (`#fafbfc`), darkened accent green (`#4F9A1E`), solid (non alpha) text colours, doubled shadow opacity, 2px borders
  - Decorative low alpha elements disabled: binary rain background hidden, full bleed gradient overlays replaced with solid scrims, QR radial glow replaced with solid outline
  - Subpixel antialiasing disabled in share mode (4:2:0 chroma subsampling destroys it anyway)
  - Reveal canvas shrinks to 1440 by 810 in share mode so text scales larger on the receiver's screen
  - Theme toggle now cycles light → dark → share → light with dedicated broadcast icon
  - URL param `?mode=share` auto activates share mode and persists to localStorage
  - New SKILL.md section "Sharing over Microsoft Teams or Zoom" documents root causes of washout (chroma subsampling, bitrate adaptation, gamut conversion) and call side settings (Teams "Optimize for video clips" off, Zoom "Optimize for video" off)

### Changed
- **sas-presentation** Default Reveal slide canvas shrunk from 1920 by 1080 to 1760 by 990 — globally increases apparent text size by ~9 percent for better readability in all modes
- **sas-presentation** Base `.reveal` font size bumped from 24px to 28px, cascading to elements without explicit sizes

## [1.8.0] - 2026-04-13

### Changed
- **sas-presentation** Major refactor of presentation philosophy and slide guidance (v2.0.0 standards)
  - Added **Presentation Philosophy** preamble with 10 non-negotiable rules (one idea, rule of three, 10 word limit, no bullet lists, tease don't tell, unexpected opening, S→C→R arc, closing echoes opening, contributions final slide, dead laptop test)
  - Restructured default Presentation type from 7-section narrative to **Situation → Complication → Resolution** three-act arc
  - New footer nav labels: TITLE | SITUATION | COMPLICATION | EVIDENCE | DECISIONS | RECOMMENDATION
  - **Louder headings**: title slide h1 increased from 64px/300 to 96px/700 (bold, commanding)
  - **Louder nav bar**: footer nav items increased from 11px/600 to 13px/700 with stronger default colour and thicker active underline
  - Title slide h2 updated from 36px/400 to 40px/500
  - Google Fonts now loads weight 500 for subtitle typography

### Added
- **sas-presentation** 5 new slide types with full CSS and HTML templates:
  - **Question slide** (`.slide-question`) — provocative centred text, tease with slide, tell with voice
  - **Full bleed image slide** (`.slide-fullbleed`) — edge to edge image with optional gradient overlay
  - **Breather slide** (`.slide-breather`) — dark blank slide to pull focus back to speaker
  - **Stat / single number slide** (`.slide-stat`) — bold 160px number with context label
  - **Contributions slide** (`.slide-contributions`) — numbered list of what was accomplished, replaces "Thank You" close
- **sas-presentation** Reveal.js **Speaker Notes** fully integrated:
  - RevealNotes plugin loaded from CDN in scaffold template
  - Every scaffold slide includes `<aside class="notes">` with transition cues, timing, and recovery phrases
  - Speaker view opens with S key — shows current slide, next preview, notes, and timer
  - SKILL.md documents speaker notes structure (transition phrase, key stat, timing, recovery)
- **sas-presentation** Tighter discovery process with 5 new Phase 2 questions:
  - One sentence test (enforces single idea)
  - Rule of three (caps supporting points)
  - Hook question (feeds opening slide)
  - Sensory detail request (feeds storytelling)
  - The ask (feeds close/recommendation)
- **sas-presentation** Content writing guidelines expanded:
  - 10 word rule enforcement with counting methodology
  - Slide selection guide (maps intent to slide type)
  - "What NOT to put on a slide" table with banned items and alternatives
  - Word count audit step added to workflow
- **sas-presentation** Pre-delivery checklist expanded with presentation philosophy and speaker notes sections

## [1.7.0] - 2026-04-08

### Added
- **sas-presentation** Winston Prompts reference — 5 AI prompts faithfully sourced from Patrick Winston's MIT "How to Speak" framework
  - Prompt 1: Start Any Presentation Right (empowerment promise, cycling, fence building, verbal punctuation, 7 second rule)
  - Prompt 2: Eliminate Your Slide Crimes (laser pointer hell, tennis match effect, contributions final slide, blackboard advantage)
  - Prompt 3: Make Your Ideas Unforgettable (Star framework: Symbol, Slogan, Surprise, Salient idea, Story)
  - Prompt 4: Structure Any Talk That Persuades (VSN-C framework: Vision, Steps, News, Contributions with salute ending)
  - Prompt 5: Use Props and Stories to Teach Anything (empathetic mirroring, blackboard advantage, prop retention)
  - All principles verified against MIT OpenCourseWare source material and Winston's *Make It Clear*

## [1.6.0] - 2026-03-31

### Added
- **project-manager** New plugin — marcov.GATE project delivery framework (v1.0.0)
  - Stage-gated hybrid methodology: 5 phases (Inception, Discovery, Development, Delivery, Close) with evidence-gated advancement
  - GATE = Governed Advancement Through Evidence — extends marcov.BEAM from sales into delivery
  - `/project-manager` slash command with 9 subcommands (new, status, gate-review, dashboard, portfolio, report, update, close, list)
  - `portfolio-sweep` agent — discovers `.project-status.json` across all repos, generates master board
  - `sweepProjects.py` — Python script for repo scanning, validation, and aggregation
  - 4 interactive HTML dashboard templates (220KB total):
    - Portfolio kanban board with filters, stats, stale project alerts
    - Per-project 3-tab dashboard (progress, full dashboard, client report)
    - Client status report (print-ready, SAS-AM branded)
    - Gate review report with verdict banner, donut chart, evidence table
  - 7 reference templates: gate criteria (scaled by tier), inception, discovery, gate-review, closeout, risk register, PRINCE2 mapping
  - `.project-status.json` schema (marcov-gate-v1) for decentralised project state
  - BEAM auto-ingest: reads `.beam/` engagement data when creating new projects
  - Three scaling tiers: micro ($20K–$50K), standard ($50K–$200K), major ($200K–$2M)
  - PRINCE2 terminology overlay for Victorian Government compatibility
  - All visuals: light/dark mode, SAS-AM colour palette, WCAG 2.1 AA, print styles

## [1.5.0] - 2026-03-23

### Added
- **sas-amp** New plugin — Asset Management Plan development tool (v0.1.0)
  - Core skill with ISO 55001:2024 alignment, AMP template structure, adaptive interview methodology
  - `/sas-amp` slash command for starting AMP development sessions
  - `amp-researcher` agent — regulatory, benchmark, and organisational web research
  - `amp-data-analyst` agent — data cleaning, LCC/NPV analysis, chart generation (7 chart types)
  - `amp-asset-context-reviewer` agent (Opus) — per-section review through asset owner perspective
  - `amp-document-generator` agent — branded DOCX output via python-docx
  - `generateDocx.py` — SAS-AM branded document generation with cover page, ToC, tables
  - `generateCharts.py` — matplotlib charts + D3.js specs for dual HTML/DOCX output
  - `dataUtils.py` — data cleaning, profiling, renewal forecasting, quality assessment CLI
  - 4 reference files: ISO mapping, AMP template structure, data analysis patterns, interview methodology
  - Registered in marketplace.json

## [1.4.1] - 2026-03-23

### Fixed
- **b2b-research-agent** Score number text invisible on score cards — green text on green background from conflicting CSS rules
- **b2b-research-agent** Logos broken in dossier reports — replaced local asset paths with Webflow CDN URLs
- **b2b-research-agent** Added logo theme toggling CSS — correct logo shown per light/dark mode

## [1.4.0] - 2026-03-12

### Marketplace
- **Added** sas-content-hub to marketplace registry
- **Added** webflow-content-creator to marketplace registry
- **Added** analytics to marketplace registry
- **Added** fmeca to marketplace registry

## [1.3.0] - 2026-03-12

### Wiki & Documentation
- **Added** wiki pages for sas-content-hub, webflow-content-creator, website-analytics, fmeca
- **Updated** master wiki hub from 9 to 13 skills

### Server Deployment Automation
- **Added** `deployGate.py` — automates SCP, resources.json registration, container restart on cortext4
- **Added** `server-deployment.md` reference with full architecture and troubleshooting
- **Updated** email-gate SKILL.md with automated deployment step
- **Updated** content-campaign SKILL.md with Stage 2b for Cortex4 asset deployment

### New Plugins
- **Added** analytics plugin (website-analytics skill, analytics-advisor agent, 6 commands)
- **Added** webflow-content-creator plugin (standalone)
- **Added** fmeca skill (5 workflows, 4 sector taxonomies)

## [1.2.0] - 2026-03-09

### Wiki Documentation
- **Added** master wiki hub (`wiki.html`) with skill catalogue and navigation
- **Added** wiki page for sas-presentation skill
- **Added** wiki page for data-quality-analysis skill
- **Added** wiki page for b2b-research-agent skill
- **Added** wiki page for beam-selling skill
- **Added** wiki page for linkedin-post-generator skill
- **Added** wiki page for tender-assessment skill
- **Added** wiki page for push-notifications skill
- **Added** wiki page for nano-banana-2 skill
- **Added** wiki page for sasam-update (sasam-core) skill

## [1.1.0] - 2026-02-27

### nano-banana-2
- **Added** mandatory post-processing with SAS logo watermark
- **Added** `post-process.js` script for automated watermarking
- **Changed** config storage to global `~/.claude/skills/nano-banana-2/`
- **Changed** prominent warning section requiring post-processing
- **Fixed** watermark not being applied during generation

### Infrastructure
- **Added** VERSION file for marketplace versioning
- **Added** CHANGELOG.md for release tracking
- **Added** `/sasam-update` skill for update management
- **Added** File manifest for integrity tracking

## [1.0.0] - 2026-02-22

### Initial Release
- **Added** sas-presentation - Reveal.js presentations with SAS branding
- **Added** data-quality-analysis - ABS Data Quality Framework assessments
- **Added** b2b-research-agent - B2B prospect research and intelligence
- **Added** beam-selling - BEAM evidence-gated sales lifecycle
- **Added** linkedin-post-generator - LinkedIn content in SAS-AM voice
- **Added** tender-assessment - Victorian government tender scoring
- **Added** push-notifications - Teams webhook and desktop notifications
- **Added** nano-banana-2 - Google Gemini image generation
