---
name: sas-content-hub
description: >
  SAS-AM unified content hub. Use when the user says "content hub", "sas content hub", "run a content campaign",
  "create a campaign", "build a content pipeline", "artefact to article to LinkedIn", "end-to-end content",
  "publish a campaign", or wants to orchestrate the full SAS-AM content pipeline. Routes to the appropriate
  sub-skill: content-campaign (orchestrator), email-gate, webflow-content-creator, or linkedin-post-generator.
---

# SAS-AM Content Hub

Unified entry point for SAS-AM content workflows. Choose a workflow below or describe what you need and the hub will route you.

## Available Workflows

| Command | Skill | What it does |
|---------|-------|-------------|
| `/content-campaign` | content-campaign | Full pipeline: artefact → gate → article → LinkedIn |
| `/webflow-content-creator` | webflow-content-creator | Publish a blog article or case study to Webflow |
| `/linkedin-post-generator` | linkedin-post-generator | Create a LinkedIn post in SAS-AM brand voice |
| `/email-gate` | email-gate | Create an email-gated download for a content artefact |

## Quick Start

**What would you like to do?**

A) Run a full content campaign (artefact → article → LinkedIn)
B) Publish an article or case study to Webflow
C) Create a LinkedIn post
D) Set up an email-gated download
E) Something else — describe your content need

Wait for the user's selection, then invoke the corresponding skill:
- A → Follow the `/content-campaign` workflow
- B → Follow the `/webflow-content-creator` workflow
- C → Follow the `/linkedin-post-generator` workflow
- D → Follow the `/email-gate` workflow
- E → Ask a clarifying question, then route accordingly
