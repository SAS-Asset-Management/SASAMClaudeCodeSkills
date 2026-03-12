# Webflow Content Creator

Create and publish SAS-AM branded blog articles and case studies directly to Webflow CMS.

## Overview

This skill helps you create high-quality content for the SAS-AM website (www.sas-am.com/resources) and publish it directly to Webflow CMS.

**Content Types:**
- **Articles** — Thought leadership, technical insights, industry analysis
- **Case Studies** — Client success stories with measurable outcomes

**Integrations:**
- **Webflow MCP** — Direct CMS publishing via the Webflow API
- **nano-banana-2** — AI-generated hero images
- **b2b-research-agent** — Research-backed content

## Usage

```bash
# Create an article
/webflow-content-creator Write an article about AI readiness for asset managers

# Create a case study
/webflow-content-creator Case study: Water utility predictive maintenance

# Create content from research
/webflow-content-creator Article based on my b2b-research-agent output
```

## Supported Sectors

- Local Government
- Water
- Resources & Minerals
- Transport
- Health
- Defence

## Topic Tags

- AI
- Asset Management System
- Technical
- Insight
- Asset Condition
- Machine Learning
- Advisory

## Prerequisites

1. **Webflow MCP** enabled in Claude Code settings
2. **WEBFLOW_TOKEN** environment variable configured
3. Access to the SAS-AM Webflow site

## Workflow

1. **Interview** — Gather content requirements, sector, tags, and source material
2. **Research** (optional) — Pull insights from b2b-research-agent
3. **Draft** — Generate SEO-optimised content following SAS-AM voice
4. **Image** (optional) — Generate hero image via nano-banana-2
5. **Publish** — Push to Webflow as draft or live

## Voice & Tone

Content follows SAS-AM brand guidelines:
- Australian English (organisation, behaviour, analyse)
- Conversational but professional
- Technical accuracy with practical application
- No fabricated stories, quotes, or statistics

## Version

1.0.0
