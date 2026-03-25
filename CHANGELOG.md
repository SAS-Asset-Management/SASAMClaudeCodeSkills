# Changelog

All notable changes to SASAMClaudeCodeSkills will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
