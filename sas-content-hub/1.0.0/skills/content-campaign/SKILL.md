---
name: content-campaign
description: This skill should be used when the user asks to "run a content campaign", "create a campaign", "build a content pipeline", "artefact to article to LinkedIn", "end-to-end content", "publish a campaign", or wants to orchestrate the full SAS-AM content pipeline from downloadable artefact through to LinkedIn promotion. Coordinates sas-presentation, email-gate, webflow-content-creator, linkedin-post-generator, and nano-banana-2 as a single workflow.
---

# SAS-AM Content Campaign Orchestrator

Orchestrate the full SAS-AM content pipeline from a single brief — creating a downloadable artefact, gating it behind email capture, publishing a supporting article to Webflow, and promoting it on LinkedIn.

## Pipeline Overview

```
Brief → Artefact → Gate → Article → LinkedIn Post
         ↓                  ↓            ↓
   sas-presentation    nano-banana-2   nano-banana-2
   (dependency)        (hero image)    (social image)
```

| Stage | Skill | Output |
|-------|-------|--------|
| 1. Artefact | `sas-presentation` (dependency) | Interactive HTML (scorecard, checklist, template) |
| 2. Gate | `email-gate` (this plugin) | Webflow embed HTML with lead capture → Cortex4 |
| 3. Article | `webflow-content-creator` (this plugin) | SEO-optimised article on sas-am.com/resources |
| 4. Promotion | `linkedin-post-generator` (this plugin) | LinkedIn post promoting the article |
| Images | `nano-banana-2` (dependency) | Hero image (article) + social graphic (LinkedIn) |

---

## Campaign Interview

Conduct the interview in order, one question at a time. Gather the full brief before starting any production.

### Q1: Campaign Topic

> "What is the core topic or theme for this campaign?"
>
> A) Maintenance strategy / planning
> B) Asset condition / monitoring
> C) AI / ML for asset management
> D) Risk and reliability
> E) Maturity assessment
> F) Something else — describe it

### Q2: Target Sector

> "Which sector is this campaign targeting?"
>
> A) Local Government
> B) Water
> C) Resources & Minerals
> D) Transport
> E) Health
> F) Defence
> G) Cross-sector (general)

### Q3: Artefact Type

> "What downloadable artefact will anchor this campaign?"
>
> A) Interactive scorecard / benchmarking tool
> B) Audit checklist
> C) Business case template
> D) Maturity assessment
> E) Technical guide / how-to
> F) Something else — describe it

### Q4: Artefact Details

> "Describe the artefact in more detail:
> - What will it help the reader do?
> - How many sections or questions should it have?
> - Any specific scoring or methodology?"

### Q5: Key Evidence

> "What real evidence, stories, or data do you have for the article?
> - Client outcomes or project results (with permission)
> - Industry statistics
> - Personal experience or observations
> - Contrarian viewpoints or myths to bust"

### Q6: CTA Goal

> "What is the ultimate call-to-action for this campaign?"
>
> A) Book a diagnostic conversation
> B) Request a maturity assessment
> C) Download the artefact (top of funnel only)
> D) Contact us for a proposal
> E) Something else

### Q7: Urgency & Timeline

> "Any timing considerations?"
>
> A) Tied to an event, conference, or tender
> B) Seasonal relevance (end of financial year, budget cycle)
> C) No specific timing — evergreen content
> D) Other — describe

---

## Production Workflow

After completing the interview, execute each stage sequentially. Present the output of each stage to the user for approval before proceeding to the next.

### Stage 1: Create Artefact

Invoke `/sas-presentation` (external dependency) with the artefact brief from Q3–Q4.

**Input to sas-presentation:**
- Presentation type based on artefact type (scorecard, checklist, template)
- Topic and sector from Q1–Q2
- Methodology and sections from Q4

**Output:** Interactive HTML file saved to the working directory.

**Gate check:** Present the artefact to the user. Ask: "Does this artefact look right? Any adjustments before we gate it?"

### Stage 2: Generate Email Gate

Invoke the `email-gate` skill (this plugin) to create the gated download form.

**Input to email-gate:**
- Artefact title from Q3
- Description from Q4
- Resource slug derived from title
- Icon type matching artefact type
- File path to the artefact from Stage 1

**Output:** Gate HTML snippet ready for Webflow embed.

**Gate check:** Present the gate HTML to the user. Ask: "Happy with the gate form? The resource slug will be `{slug}` and leads go to Cortex4."

### Stage 3: Generate Hero Image

Invoke `/nano-banana-2` (external dependency) to create the hero image for the article.

**Input to nano-banana-2:**
- Prompt derived from the campaign topic and sector
- Aspect ratio: 16:9 (article hero)
- Size: 2K
- Style: professional, SAS-AM brand-appropriate

**Output:** Watermarked hero image (JPG).

**Gate check:** Present the image. Ask: "Does this hero image work for the article? Want to regenerate or adjust the prompt?"

### Stage 4: Write Article

Invoke the `webflow-content-creator` skill (this plugin) with the full campaign context.

**Input to webflow-content-creator:**
- Topic and sector from Q1–Q2
- Evidence and stories from Q5
- CTA from Q6
- Reference to the gated artefact (embed the gate HTML in the article body)
- Hero image from Stage 3
- Content type: Article
- Tags derived from topic

The article should:
- Lead with the problem the artefact solves
- Provide genuine insight (not just a sales pitch for the download)
- Embed the email gate HTML as a Webflow Custom Code Embed block within the article body
- Include a clear CTA at the end

**Output:** Article content ready for Webflow CMS.

**Gate check:** Present the article draft. Ask: "Ready to publish, or want to adjust the content?"

### Stage 5: Publish to Webflow

Use `webflowPublish.py` to publish the article and upload the hero image.

```bash
# Create CMS item — pass the nano-banana-2 image path directly.
# The script auto-uploads the image to Webflow Assets and wires it into the CMS item.
python3 ${CLAUDE_PLUGIN_ROOT}/skills/webflow-content-creator/scripts/webflowPublish.py create <collection_id> '{
  "name": "Article Title",
  "slug": "article-title",
  "featured-image": { "file": "./generated-images/hero_final.jpg", "alt": "Hero image alt text" },
  "body-content": "<p>Article HTML...</p>",
  ...
}' --site=<site_id>
```

**Gate check:** Ask: "Article is in draft on Webflow. Publish live now, or review in Webflow first?"

### Stage 6: Create LinkedIn Post

Invoke the `linkedin-post-generator` skill (this plugin) to promote the article.

**Input to linkedin-post-generator:**
- The published article URL
- Campaign topic and key insights from Q5
- All interview material (stories, confessions, contrasts, myths, data)
- CTA: drive traffic to the article (which gates the artefact)

The skill will produce all eligible post formats in parallel via subagents, then recommend the strongest.

**Output:** LinkedIn post ready to publish.

**Gate check:** Present the recommended post. Ask: "Ready to publish on LinkedIn, or want to switch formats or adjust?"

---

## Campaign Summary

After all stages complete, present a campaign summary:

```
=== Campaign Complete ===

Topic: [campaign topic]
Sector: [target sector]

Artefact: [title] → [file path]
Gate: [resource slug] → leads to Cortex4
Article: [title] → [Webflow URL or draft status]
LinkedIn: [format used] → [ready to post]
Hero Image: [file path]

Lead Capture: gate.sas-am.com → Cortex4 client DB
CTA: [chosen CTA]
```

---

## Dependencies

This skill requires the following external plugins to be installed:

| Plugin | Purpose | Required |
|--------|---------|----------|
| `sas-presentation` | Creates downloadable artefacts (HTML presentations, scorecards) | Yes |
| `nano-banana-2` | Generates hero images and social graphics | Yes |

If a dependency is not installed, warn the user and offer to skip that stage (e.g., use an existing artefact or manually provided image).

---

## Reference Files

- **`references/campaign-checklist.md`** — Pre-flight checklist for each campaign stage
