---
name: webflow-content-creator
description: This skill should be used when the user wants to create, write, draft, or publish SAS-AM branded blog articles and case studies to the Webflow CMS at www.sas-am.com/resources. It supports Local Government, Water, Resources & Minerals, Transport, Health, and Defence sectors. It integrates with nano-banana-2 for hero images and publishes via the webflowPublish.py script.
---

# SAS-AM Webflow Content Creator

Create compelling, SEO-optimised content for the SAS-AM website and publish directly to Webflow CMS. Write like a knowledgeable peer who has spent time on the tools, understands asset management realities, and can translate complex concepts into actionable insights.

## Capabilities

- **Interview first** — gather real stories, evidence, and outcomes before writing
- **Create articles** — thought leadership, technical insights, industry analysis
- **Create case studies** — client success stories with measurable outcomes
- **Generate hero images** — via nano-banana-2 integration
- **Publish to Webflow** — draft or live via `webflowPublish.py`
- **Stay on-brand** — Australian English, SAS-AM voice, no fabrication

## Input

Accept a **topic, brief, or content type** as the primary input. Also work from research dossiers or existing material.

```
/webflow-content-creator Write an article about AI readiness for asset managers
/webflow-content-creator Case study: Mining company predictive maintenance success
/webflow-content-creator Promote our new risk assessment service
```

---

## Workflow

### Step 1: Interview (Mandatory)

Never draft content without interviewing the user first. Never invent stories, quotes, statistics, outcomes, or client experiences. Every claim, number, and narrative element must come directly from the user's answers or verified research.

Follow the full interview process in `references/interview-guide.md`. Ask **one question at a time** and provide multiple-choice options where possible.

### Step 2: Draft Content

Based on content type, apply the appropriate template:

- **Article**: follow `references/article-template.md`
- **Case Study**: follow `references/case-study-template.md`

Apply all voice, tone, and language rules from `references/voice-and-brand.md`. Tailor sector-specific messaging using `references/sector-guidelines.md`. Validate SEO elements against `references/seo-checklist.md`.

See `references/example-content.md` for tone and quality benchmarks.

#### Article Length Guidelines

| Type | Word Count | When to Use |
|------|------------|-------------|
| **Short insight** | 500-800 words | Single focused idea, quick read |
| **Standard article** | 800-1200 words | Full exploration of topic |
| **Deep dive** | 1200-2000 words | Technical content, comprehensive guides |

### Step 3: Generate Hero Image (Optional)

If the user does not have an existing image, offer to generate one via nano-banana-2.

Analyse the content to derive an image prompt, then invoke:

```
/nano-banana-2 "[generated prompt]" --aspect 16:9
```

nano-banana-2 will generate at 16:9 aspect ratio (optimal for Webflow cards), apply SAS watermark, compress via Squoosh to 1000px wide under 200KB JPG, and return a file path for upload.

### Step 4: Review Draft

Present the complete draft for review:

```
=== DRAFT PREVIEW ===

[Content preview with all sections]

=== END PREVIEW ===

Questions:
- Does this capture your intent?
- Any facts or figures to adjust?
- Ready to proceed to Webflow, or need revisions?
```

### Step 5: Publish to Webflow

Use `${CLAUDE_PLUGIN_ROOT}/skills/webflow-content-creator/scripts/webflowPublish.py` for all CMS operations. The `WEBFLOW_TOKEN` environment variable must be set.

#### Publishing Sequence

**Phase 1 — Discover site and collection:**

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/webflow-content-creator/scripts/webflowPublish.py sites
python3 ${CLAUDE_PLUGIN_ROOT}/skills/webflow-content-creator/scripts/webflowPublish.py collections <site_id>
```

**Phase 2 — Create CMS item with hero image:**

The `create` command auto-detects image fields containing local file paths, uploads them to Webflow Assets, and wires the resulting `fileId` into the CMS item automatically. Pass the nano-banana-2 output path directly:

```json
{
  "name": "Article Title",
  "slug": "article-title",
  "featured-image": { "file": "./generated-images/hero_final.jpg", "alt": "Hero image description" },
  "body-content": "<p>Article HTML content...</p>",
  ...
}
```

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/webflow-content-creator/scripts/webflowPublish.py create <collection_id> '<json_payload>' --site=<site_id>
```

The script will upload the image to Webflow Assets, get the `fileId`, and set it on the CMS item in one step. The `--site` flag tells the script which site to upload the asset to.

Required fields: `name`, `slug`, `sector`, `content-type`, `topic-tags`, `featured-image` (object with `file` path + `alt`), `description`, `body-content`, `seo-title`, `seo-description`, `publish-date`.

**Phase 4 — Publish live (after user confirmation):**

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/webflow-content-creator/scripts/webflowPublish.py publish <collection_id> '<json_payload>'
```

#### Script Command Reference

| Command | Usage |
|---------|-------|
| `sites` | List available Webflow sites |
| `collections <site_id>` | List CMS collections for a site |
| `items <collection_id>` | List existing items in a collection |
| `create <collection_id> <json>` | Create new CMS item (draft) |
| `publish <collection_id> <json>` | Create and publish immediately |
| `update <collection_id> <item_id> <json>` | Update existing item |
| `upload-asset <site_id> <file_path>` | Upload image asset |

#### Error Handling

| Error | Action |
|-------|--------|
| `WEBFLOW_TOKEN` not set | Instruct the user to set the environment variable |
| Site not found | Run `sites` command and ask the user to confirm |
| Collection not found | Run `collections` command and ask the user to select |
| Field validation error | Report the specific field and show the expected format from `references/cms-schema.json` |
| Asset upload failure | Retry once, then fall back to a placeholder |
| Publishing failure | Save content locally and provide a recovery path |

---

## Quality Checklist

Run before presenting final content:

- [ ] Australian English spelling throughout (organisation, behaviour, analyse, colour, centre)
- [ ] Active voice predominant
- [ ] Opening hook is compelling
- [ ] Every story, quote, and statistic traces to the user interview — nothing fabricated
- [ ] No banned words or phrases (see `references/voice-and-brand.md`)
- [ ] SEO title under 60 characters
- [ ] Meta description under 160 characters
- [ ] Primary keyword in H1 and first paragraph
- [ ] Heading hierarchy is logical (H1 > H2 > H3)
- [ ] Hero image ready (provided or generated)
- [ ] Slug is URL-friendly
- [ ] All required CMS fields populated per `references/cms-schema.json`

---

## Skill Integration Dependencies

### sas-presentation

Use sas-presentation to create downloadable artefacts (slide decks, one-pagers) that complement published articles. When a user wants a presentation version of their content, invoke `/sas-presentation` after the article is drafted.

### nano-banana-2

Use nano-banana-2 for hero image generation. Derive image prompts from the finalised content topic and invoke with `--aspect 16:9`. See Step 3 above for the full process.

### email-gate

Use email-gate when the user wants to gate a downloadable resource behind an email capture form. After creating a downloadable artefact via sas-presentation, invoke `/email-gate` to generate the gated landing page link for inclusion in the article's CTA.

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/interview-guide.md` | Full interview process and question sets |
| `references/voice-and-brand.md` | Voice, tone, language rules, brand positioning, content themes |
| `references/article-template.md` | Article structure template |
| `references/case-study-template.md` | Case study STAR framework template |
| `references/cms-schema.json` | Webflow CMS field mapping and validation rules |
| `references/seo-checklist.md` | SEO optimisation checklist |
| `references/sector-guidelines.md` | Sector-specific messaging guidelines |
| `references/example-content.md` | Example article and case study for tone reference |
