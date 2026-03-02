---
name: MBP:content-intel
description: Discover and score content opportunities from Reddit and community platforms. Use when the user wants to identify trending topics, score content gaps, generate content briefs, or prioritise what to write next. Scrapes relevant subreddits, scores topics against SAS-AM service lines, and produces prioritised content briefs that feed into MBP:linkedin-post, MBP:seo, MBP:google-ads, and MBP:linkedin-ads. Part of the Marcov Beam Pipeline.
---

# Content Intelligence Skill

Discover what your target audience is actually asking about on Reddit and community platforms, score those topics against SAS-AM's services, identify content gaps, and generate actionable content briefs. You're not guessing what to write — you're listening to the market and responding with authority.

## Overview

This skill helps you:

- **Discover real questions** — find what asset management professionals are actually asking on Reddit, forums, and community platforms
- **Score and prioritise** — rate each topic across Frequency, SAS-AM Relevance, and Content Gap to produce a priority tier
- **Generate content briefs** — create actionable briefs for Critical and High priority topics with content angles, format recommendations, and service tie-ins
- **Feed the pipeline** — output formatted for MBP:linkedin-post, MBP:seo, MBP:google-ads, and MBP:linkedin-ads
- **Deliver a branded report** — interactive HTML report with filtering, sorting, and detail modals using SAS-AM branding

---

## Input

This skill accepts a **topic area, service line focus, or campaign theme** as its primary input. It can also run broad discovery across all SAS-AM service lines with no specific input.

### Invocation Examples

```
/content-intel Discover content opportunities for our AI readiness campaign
/content-intel What should we write about next for reliability engineering?
/content-intel Scan Reddit for edge AI and sovereign data topics
/content-intel Run a full content gap analysis across all service lines
/content-intel Find trending maintenance questions in mining subreddits
```

---

## Discovery Interview (CRITICAL)

**Before scanning any platforms, you MUST conduct a discovery interview to understand the content strategy context.**

### Questions to Ask

1. **Service Line Focus**
   - What service lines should we prioritise? (AI/ML, data quality, reliability engineering, ISO 55001/maturity, edge/sovereign AI, mining, workforce)
   - Are there specific campaigns or themes to align content with?

2. **Existing Coverage**
   - Are there topics we've already covered well? (avoid duplication)
   - Do you have a content calendar or list of published articles we should cross-reference?

3. **Format Preferences**
   - Preferred content formats? (Pillar articles, LinkedIn posts, carousels, case studies, quick insights)
   - Any formats that have performed particularly well recently?

4. **Audience Context**
   - What subreddits are most relevant to your audience?
   - Any specific industries or verticals to focus on? (mining, water, transport, energy)

5. **Competitive Landscape**
   - Any competitors whose content presence we should assess?
   - Are there thought leaders or publications dominating specific topics?

6. **Campaign Alignment**
   - Is this for a specific campaign launch, or general pipeline building?
   - Any upcoming events, webinars, or product launches to align with?

### If No Input Is Provided

If the user invokes the skill without a specific focus, run broad discovery across all SAS-AM service line categories and all default subreddits. Note this in the report and recommend narrowing scope for follow-up runs.

---

## Default Subreddits

| Subreddit | Relevance |
|---|---|
| r/ReliabilityEngineering | Core audience — RCM, FMEA, CBM discussions |
| r/MaintenanceProfessionals | Practitioner questions, day-to-day pain points |
| r/mining | Mining maintenance, harsh environment operations |
| r/AssetManagement | Asset management strategy and frameworks (if active) |
| r/dataengineering | Data quality, pipelines, CMMS data discussions |
| r/LocalLLaMA | Edge AI, on-premises models, data sovereignty overlap |
| r/sysadmin | Infrastructure management, monitoring, operational tech |
| r/MachineLearning | AI applications, predictive maintenance, ML deployment |

Add or replace subreddits based on the discovery interview. If the user identifies industry-specific forums, Slack communities, or Stack Exchange sites, include those in the scan.

---

## SAS-AM Service Line Categories

All discovered topics must be categorised into one of these service lines:

| Category | Includes |
|---|---|
| **AI & ML** | Predictive maintenance, ML deployment, AI pilots, data science for maintenance, algorithm selection |
| **Data Quality** | CMMS data governance, failure taxonomies, data readiness, master data management, data migration |
| **Edge & Sovereign AI** | On-premises AI, data sovereignty, AMiPU platform, air-gapped environments, local inference |
| **Reliability Engineering** | RCM, FMEA, condition-based maintenance, criticality analysis, failure mode analysis |
| **Maturity & ISO 55001** | Asset management maturity assessments, gap assessments, frameworks, certification readiness |
| **Mining & Heavy Industry** | Mining maintenance, energy transition, harsh environment monitoring, mobile fleet management |
| **Workforce** | Knowledge capture, skills gaps, technician retention, succession planning, training programmes |

---

## Scoring Framework

Each discovered topic is scored across three dimensions, each rated 1 to 5.

### Dimension Definitions

| Dimension | 1 (Low) | 3 (Medium) | 5 (High) |
|---|---|---|---|
| **Frequency** | Rare niche discussion, single thread | Periodic discussion across 1-2 subreddits | Constant high-traffic threads across multiple subreddits |
| **SAS-AM Relevance** | Tangentially related to asset management | Related to a SAS-AM service line but not a core offering | Directly maps to a core SAS-AM service, audience, or content theme |
| **Content Gap** | Well-covered by competitors and existing content | Some coverage exists but quality is inconsistent | High demand, low quality answers — significant opportunity to own the space |

### Priority Tiers

| Total Score (3-15) | Priority Tier | Action |
|---|---|---|
| 13-15 | **Critical** | Act now — create content this week |
| 10-12 | **High** | Schedule this month — strong opportunity |
| 7-9 | **Medium** | Add to content calendar — worth covering |
| 3-6 | **Low** | Monitor — watch for rising interest |

### Scoring Rules

- Score each dimension independently — do not let one dimension inflate another
- Be honest about relevance — if a topic is popular but we can't credibly speak to it, score Relevance low
- Content Gap rewards topics where existing answers are poor, outdated, or vendor-biased
- A score of 5 on Content Gap means "the audience is frustrated by the quality of available answers"
- Document the evidence for each score (link to threads, upvote counts, answer quality)

---

## Analysis Workflow

### Phase 1: Topic Discovery

Search relevant subreddits and community platforms for recurring questions, pain points, and debates.

**Search strategies:**

1. **Direct subreddit search** — search each default (or custom) subreddit for keywords related to SAS-AM service lines
2. **Web search** — use `site:reddit.com` queries for broader discovery beyond subscribed subreddits
3. **Trending detection** — look for threads with high upvotes, high comment counts, or recent activity spikes
4. **Cross-post patterns** — topics that appear across multiple subreddits indicate broader interest

**What to look for:**

- Repeated questions (same question asked in different ways, different subreddits)
- Unanswered threads or threads with low-quality answers
- High-upvote questions with vendor-biased or superficial answers
- Debates and disagreements (signal audience confusion — opportunity to clarify)
- "How do I..." and "What's the best..." question patterns
- Complaints about tools, processes, or standards (pain points)
- Requests for recommendations or comparisons

**For each discovered topic, capture:**

- Original question or thread title (verbatim)
- Subreddit(s) where it appeared
- Approximate upvote count and comment count
- Quality of existing answers (poor / adequate / good)
- Date range of discussions (recent vs recurring)
- URL(s) to representative threads

### Phase 2: Topic Scoring

Score each discovered topic across the three dimensions.

1. **Assign scores** — rate Frequency, SAS-AM Relevance, and Content Gap (each 1-5)
2. **Calculate total** — sum the three scores (3-15)
3. **Assign priority tier** — Critical (13-15), High (10-12), Medium (7-9), Low (3-6)
4. **Categorise** — assign each topic to the most relevant SAS-AM service line category
5. **Rank** — sort by total score descending, then by Content Gap score as tiebreaker

### Phase 3: Content Brief Generation

For each **Critical** and **High** priority topic, generate a detailed content brief using the template in `references/content-brief-template.md`.

Each brief includes:

- **Topic title** — attention-grabbing, specific, practitioner-focused
- **Original Reddit question** — verbatim quote from the source thread
- **Priority score breakdown** — Frequency / Relevance / Gap / Total with tier
- **Category** — SAS-AM service line
- **Content angle** — our unique take, grounded in SAS-AM expertise and brand voice
- **Suggested format** — pillar article, LinkedIn post type (SLAY, confession, this-not-that, etc.), carousel, case study
- **SAS-AM service tie-in** — which specific service or capability this maps to
- **Target distribution channels** — subreddits, LinkedIn, website, email newsletter
- **Recommended UTMs** — campaign/source/medium parameters for tracking
- **Strategic notes** — why this matters, competitive advantage, timing considerations

### Phase 4: Cross-Skill Recommendations

Generate specific outputs formatted for downstream MBP skills:

**For MBP:linkedin-post:**
- Topic briefs formatted as post prompts
- Recommended post format (SLAY, confession, this-not-that, myth-vs-reality, quick insight, etc.)
- Hook suggestions based on the original audience question

**For MBP:seo:**
- Keyword targets derived from topic themes and original question language
- Long-tail keyword variations from natural question phrasing
- Content cluster suggestions grouping related topics

**For MBP:google-ads:**
- Recommended keyword themes for paid campaigns
- Negative keyword suggestions (irrelevant variants discovered during research)
- Ad copy angle suggestions based on pain points discovered

**For MBP:linkedin-ads:**
- Audience/messaging recommendations based on pain points discovered
- Job title and industry targeting suggestions
- Ad creative themes aligned with highest-priority topics

### Phase 5: Report Generation

Generate a branded interactive HTML report using the template in `references/topic-prioritiser-template.html`.

**Report features:**

- Summary cards showing Critical/High/Medium/Low counts and top score
- Scoring key explaining the framework
- Filterable and sortable topic table (filter by category, priority, search by keyword)
- Detail modal on row click showing full content brief
- SAS-AM branding (SAS Blue #002244, SAS Green #69BE28, DM Sans font)
- Light/dark mode toggle with localStorage persistence
- Print-friendly layout

**Also generate:**

- `content-briefs-{date}.md` — markdown content briefs for all Critical and High topics
- `.marketing/content-intel/latest.json` — normalised data for MBP:marketing-dashboard

---

## Output Files

| File | Format | Purpose |
|---|---|---|
| `content-intel-report-{date}.html` | HTML | Primary deliverable — branded interactive report |
| `content-briefs-{date}.md` | Markdown | Content briefs for Critical and High topics |
| `.marketing/content-intel/latest.json` | JSON | Normalised pipeline data for MBP:marketing-dashboard |

### JSON Output Schema

The `.marketing/content-intel/latest.json` file must follow this structure:

```json
{
  "generated": "2026-03-02T10:00:00Z",
  "skill": "MBP:content-intel",
  "summary": {
    "total_topics": 24,
    "critical": 3,
    "high": 7,
    "medium": 10,
    "low": 4,
    "top_score": 15,
    "categories_covered": ["AI & ML", "Data Quality", "Reliability Engineering"]
  },
  "topics": [
    {
      "id": 1,
      "title": "Topic title here",
      "question": "Original Reddit question verbatim",
      "category": "AI & ML",
      "scores": {
        "frequency": 5,
        "relevance": 5,
        "gap": 5,
        "total": 15
      },
      "priority": "Critical",
      "content_angle": "Our unique take on this topic",
      "suggested_format": "Pillar article",
      "service_tie_in": "Predictive maintenance consulting",
      "subreddits": ["r/ReliabilityEngineering", "r/MachineLearning"],
      "thread_urls": ["https://reddit.com/r/..."],
      "strategic_notes": "Why this matters and competitive advantage"
    }
  ],
  "cross_skill": {
    "linkedin_post_prompts": [],
    "seo_keywords": [],
    "google_ads_themes": [],
    "linkedin_ads_audiences": []
  }
}
```

---

## Integration with MBP Pipeline

### Upstream Dependencies

| Source | What It Provides |
|---|---|
| `shared/brand-voice.md` | Tone and language rules for content angle writing |
| `shared/sas-branding.md` | Visual branding for HTML report styling |
| Discovery interview | Service line focus, campaign context, audience preferences |

### Downstream Consumers

| Consumer | What It Receives |
|---|---|
| **MBP:linkedin-post** | Topic briefs formatted as post prompts with recommended format and hook suggestions |
| **MBP:seo** | Keyword targets, long-tail variations, content cluster suggestions |
| **MBP:google-ads** | Keyword themes, negative keyword suggestions, ad copy angles |
| **MBP:linkedin-ads** | Audience recommendations, job title targeting, ad creative themes |
| **MBP:marketing-dashboard** | Normalised JSON data for pipeline visibility and reporting |

### Pipeline Usage Pattern

```
MBP:content-intel (discover & score)
    |
    +---> MBP:linkedin-post (create posts from top briefs)
    +---> MBP:seo (optimise website content for discovered keywords)
    +---> MBP:google-ads (build paid campaigns around pain points)
    +---> MBP:linkedin-ads (target audiences experiencing discovered problems)
    +---> MBP:marketing-dashboard (aggregate pipeline metrics)
```

---

## Content Guidelines

### Australian English

Use Australian English spelling throughout all outputs:

- analyse (not analyze)
- organisation (not organization)
- colour (not color)
- prioritise (not prioritize)
- programme (not program, unless referring to software)
- licence (noun) / license (verb)
- centre (not center)
- categorise (not categorize)

### Brand Voice (per shared/brand-voice.md)

- Sound like a **knowledgeable peer** — someone who has spent time on the tools
- **No emojis** — ever
- **No hashtags** — in any output
- **No corporate waffle** — say "fix" not "remediate", say "check" not "perform a validation exercise"
- **Active voice** — "We assessed the content landscape" not "The content landscape was assessed"
- **Evidence over opinion** — back claims with thread links, upvote counts, or specific observations
- **Short sentences** — aim for 15-20 words average
- **Contractions are fine** — "we've", "it's", "don't"

### Content Angle Writing

When writing the content angle for a brief, follow these rules:

1. **Lead with the audience's pain** — not our capability
2. **Be specific** — "Why your FMEA worksheets aren't reducing failures" not "Asset management best practices"
3. **Take a position** — if we have a defensible contrarian view, lead with it
4. **Reference the original question** — show we heard them
5. **Tie to evidence** — connect to SAS-AM's real-world experience

---

## Report Template Usage

### HTML Report

The HTML report uses the template at `references/topic-prioritiser-template.html`.

**To generate:**

1. Copy the template
2. Prepare the topics array as a JavaScript object matching the `DATA_SCHEMA` in the template
3. Replace `<!-- INJECT_DATA_HERE -->` with `const TOPICS_DATA = [...]` containing all scored topics
4. Update the report title and date in the header
5. Save as `content-intel-report-{date}.html`

The template handles:
- Rendering the topic table from the injected data
- Filtering by category and priority tier
- Text search across topic titles and questions
- Sorting by any column
- Opening detail modals on row click
- Summary card calculations
- Light/dark mode toggle

### Markdown Briefs

Use the template at `references/content-brief-template.md` for each content brief. Concatenate all briefs into a single file (`content-briefs-{date}.md`) with horizontal rules between entries.

---

## Checklist

Before delivering the report, verify:

- [ ] Discovery interview completed (or assumptions clearly documented)
- [ ] All relevant subreddits scanned (default + any custom additions)
- [ ] Each topic scored across all three dimensions with evidence documented
- [ ] Priority tiers correctly assigned based on total scores
- [ ] Topics categorised into SAS-AM service line categories
- [ ] Content briefs generated for all Critical and High priority topics
- [ ] Content angles follow brand voice guidelines
- [ ] Cross-skill recommendations generated for linkedin-post, seo, google-ads, linkedin-ads
- [ ] HTML report generated using the template with data correctly injected
- [ ] Markdown briefs file generated
- [ ] JSON output file generated for marketing-dashboard
- [ ] Australian English spelling used throughout all outputs
- [ ] No emojis, no hashtags, no corporate waffle in any output
- [ ] All thread URLs included as evidence
- [ ] Light/dark mode toggle works in HTML report
- [ ] Filter and sort controls work in HTML report
- [ ] Detail modals open correctly on row click
