# Changelog

All notable changes to SASAMClaudeCodeSkills will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
