# Changelog

All notable changes to SASAMClaudeCodeSkills will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
