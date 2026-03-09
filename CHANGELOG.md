# Changelog

All notable changes to SASAMClaudeCodeSkills will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
