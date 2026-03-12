---
name: webflow-content-creator
description: Create and publish SAS-AM branded blog articles and case studies to Webflow CMS. Supports Local Government, Water, Resources & Minerals, Transport, Health, and Defence sectors. Integrates with b2b-research-agent for research, nano-banana-2 for hero images, and Webflow MCP for direct CMS publishing. Use when the user wants to create, write, draft, or publish website content for www.sas-am.com/resources.
---

# SAS-AM Webflow Content Creator

Create compelling, SEO-optimised content for the SAS-AM website and publish directly to Webflow CMS. Write like a knowledgeable peer who's spent time on the tools, understands asset management realities, and can translate complex concepts into actionable insights.

## Overview

This skill helps you:

- **Interview first** — gather real stories, evidence, and outcomes before writing
- **Create articles** — thought leadership, technical insights, industry analysis
- **Create case studies** — client success stories with measurable outcomes
- **Generate hero images** — via nano-banana-2 integration
- **Pull research** — from b2b-research-agent dossiers
- **Publish to Webflow** — draft or live via MCP integration
- **Stay on-brand** — Australian English, SAS-AM voice, no fabrication

---

## Input

This skill accepts a **topic, brief, or content type** as its primary input. It can also work from research dossiers or existing material.

### Invocation Examples

```
/webflow-content-creator Write an article about AI readiness for asset managers
/webflow-content-creator Case study: Mining company predictive maintenance success
/webflow-content-creator Article based on b2b-research-agent research for [company]
/webflow-content-creator Promote our new risk assessment service
/webflow-content-creator Technical article on Power Law Process for reliability
```

---

## Interview (MANDATORY — No Drafting Without It)

The skill MUST interview the user before drafting any content. This is non-negotiable.

### Why This Matters

**The skill never invents stories, quotes, statistics, outcomes, or client experiences.** Every claim, number, and narrative element must come directly from the user's interview answers or verified research. If the user hasn't provided evidence, the skill does not fabricate it.

### Content Type Selection

Ask first:

> "What type of content are you creating?
> 1. **Article** — thought leadership, technical insight, industry analysis
> 2. **Case Study** — client success story with measurable outcomes"

### Common Interview Questions (Both Types)

| Question | Purpose |
|----------|---------|
| **Core topic** | "What is the main topic or insight for this content?" |
| **Primary sector** | "Which sector is most relevant? (Local Government, Water, Resources & Minerals, Transport, Health, Defence)" |
| **Topic tags** | "Which tags apply? (AI, Asset Management System, Technical, Insight, Asset Condition, Machine Learning, Advisory)" |
| **Target audience** | "Who is the primary reader? (executives, technical practitioners, asset managers, decision-makers)" |
| **Key takeaway** | "What single insight should readers remember after reading?" |
| **CTA goal** | "What action should readers take? (contact us, download resource, explore related content)" |
| **Research available** | "Do you have existing research from b2b-research-agent to incorporate?" |
| **Hero image** | "Do you have an image, or should I generate one using nano-banana-2?" |

### Article-Specific Questions

| Question | Purpose |
|----------|---------|
| **Content angle** | "Is this educational (how-to), opinion (thought leadership), analytical (data-driven), or news (industry update)?" |
| **Supporting evidence** | "What data, studies, or sources support this? The skill will not fabricate statistics." |
| **Related content** | "Are there existing SAS-AM articles this should link to?" |
| **Technical depth** | "Should this be accessible to all readers or go deep technically?" |

### Case Study-Specific Questions

| Question | Purpose |
|----------|---------|
| **Client identification** | "Can you name the client, or should this be anonymised (e.g., 'a major water utility')?" |
| **The challenge** | "What specific problem were they facing before engagement?" |
| **The solution** | "What did SAS-AM do? Which services/approaches were applied?" |
| **The outcomes** | "What measurable results were achieved? (Must be specific: %, $, timeframes)" |
| **Client testimonial** | "Do you have a quote from the client? (If not, content will avoid fabricated quotes)" |
| **Publication permission** | "Has the client approved publication? (Required for named case studies)" |
| **Timeline** | "What was the project timeline?" |

### Handling Pushback

If the user says "just draft something" or tries to skip the interview:

> "I need real material to work with — the best content comes from real experiences, not invented ones. Let me ask you a few quick questions to surface the good stuff. This takes 2 minutes and makes the difference between generic content and something that genuinely resonates with your audience."

### After the Interview

Catalogue what real material was gathered:

```
=== Material Inventory ===

GATHERED:
- Core topic: [identified]
- Sector: [selected]
- Tags: [selected]
- Story/anecdote: yes/no
- Measurable outcomes: yes/no
- Client quote: yes/no
- Supporting research: yes/no
- Image: provided/generate/placeholder

CONTENT TYPE: Article / Case Study
READY TO DRAFT: Yes / No (list missing essentials)
```

---

## Voice & Tone

### Core Characteristics

| Trait | What it means | What it doesn't mean |
|-------|---------------|----------------------|
| **Upbeat** | Optimistic about technology's potential, energised by solving problems | Sycophantic, fake positivity, ignoring real challenges |
| **Clear & Concise** | Get to the point, respect the reader's time, no waffle | Dumbed down, oversimplified, missing nuance |
| **Tech Forward** | Embrace AI/ML, analytics — grounded in practical application | Buzzword-heavy, hype-driven, technology for its own sake |
| **Insightful** | Offer genuine value, perspectives others haven't considered | Stating the obvious, regurgitating common knowledge |
| **Playful** | Occasional wit, relatable analogies, don't take ourselves too seriously | Unprofessional, silly, undermining credibility |
| **Conversational** | Write like explaining to a smart colleague over coffee | Overly formal, academic, stiff corporate-speak |

### Language Rules

- **Australian English always**: organisation, favour, analyse, colour, centre, behaviour, programme (for initiatives, program for software)
- **Active voice**: "AI identifies failure patterns" not "Failure patterns are identified by AI"
- **Plain language**: "fix" not "remediate", "use" not "utilise", "help" not "facilitate"
- **Contractions welcome**: "you'll", "we've", "it's", "don't"
- **No jargon without context**: If using technical terms, ensure meaning is clear
- **Metric system**: kilometres, tonnes, degrees Celsius

### Words & Phrases to Use

- "Here's the thing..."
- "In practice..."
- "What we've found is..."
- "The honest answer is..."
- "Let's be real..."
- "Worth noting..."
- "The good news is..."
- "Quick win:"
- "Pro tip:"

### Words & Phrases to Avoid

- "Leverage" (use "use" or "apply")
- "Synergy" / "synergistic"
- "Cutting-edge" / "bleeding-edge"
- "Best-in-class"
- "Holistic" (overused — be specific)
- "Journey" (unless actually travelling)
- "Solutions" as a standalone noun
- "Stakeholders" (say who you mean)
- "Going forward" (say "next" or "from here")
- "At the end of the day"
- "It goes without saying"
- "Learnings" (use "lessons" or "what we learned")
- "I'm excited to share..."
- "In today's fast-paced world..."

---

## Brand Positioning

### Who We Are

SAS-AM is an Australian asset management consulting firm specialising in:

- **Advanced Analytics & AI/ML** for predictive maintenance and decision support
- **Maturity Assessments** aligned to ISO 55001, AI/ML and GFMAM frameworks
- **Reliability Engineering** including RCM, FMEA, root cause analysis
- **Edge/Sovereign AI Solutions** via the AMiPU platform
- **Risk & Resilience** including supply chain risk and climate adaptation

### Who We Serve

- Asset owners and operators in **transport, water, energy, mining, healthcare, and local government**
- Technical decision-makers: asset managers, reliability engineers, maintenance managers
- Senior leaders seeking innovation, cost optimisation, and compliance
- Organisations moving from reactive to predictive asset management

### Our Differentiators

1. **Practitioner-led**: We've worked on the tools, not just in boardrooms
2. **AI with purpose**: Technology that solves real problems, not innovation theatre
3. **Sovereign capability**: Offline AI that keeps sensitive data where it belongs
4. **Vendor-neutral**: We recommend what works, not what pays commission
5. **Community focus**: Better assets mean better services for Australians

---

## Content Themes (2026)

### Core Themes

1. **AI & Advanced Analytics** — Practical AI/ML applications, predictive maintenance, condition monitoring
2. **Maturity & Compliance** — ISO 55001, GFMAM frameworks, data quality, governance
3. **Risk & Reliability** — RCM, FMEA, root cause analysis, criticality, risk-based decisions
4. **Sovereign AI** — Edge computing, data sovereignty, offline capability, security
5. **Community Impact** — Sustainability, ESG, sector-specific challenges

### Sector Focus

| Sector | Key Themes |
|--------|------------|
| **Local Government** | Community assets, limited budgets, regulatory compliance, long-term planning |
| **Water** | Critical infrastructure, pump stations, treatment plants, climate resilience |
| **Resources & Minerals** | Heavy equipment, production optimisation, safety-critical systems |
| **Transport** | Fleet management, infrastructure networks, service reliability |
| **Health** | Medical equipment, facility management, compliance, patient safety |
| **Defence** | Security requirements, sovereign capability, mission-critical systems |

---

## Article Format

### Structure Template

```
# [HEADLINE]

**Sector**: [PRIMARY_SECTOR] | **Topics**: [TOPIC_TAGS]

---

## The Hook (50-100 words)
[Opening paragraph that captures attention and establishes relevance.
Ask a provocative question, state a surprising fact, or name a common frustration.]

## The Context (100-200 words)
[Setting the scene — why this matters now, what's changing in the industry.
Connect to reader's current challenges.]

## The Core Content (400-800 words)

### [Key Point 1]
[Detailed explanation with evidence]

### [Key Point 2]
[Detailed explanation with evidence]

### [Key Point 3] (if applicable)
[Detailed explanation with evidence]

## The Practical Application (150-250 words)
[How readers can apply this information — actionable takeaways.
Be specific: "Do this tomorrow" not "consider doing this eventually."]

## The Connection (50-100 words)
[Call to action — what to do next, related resources, contact.
Make the next step clear and easy.]

---

**About SAS-AM**: SAS Asset Management is an Australian consulting firm...
**Related Resources**: [Links to related content]
```

### Article Length Guidelines

| Type | Word Count | When to Use |
|------|------------|-------------|
| **Short insight** | 500-800 words | Single focused idea, quick read |
| **Standard article** | 800-1200 words | Full exploration of topic |
| **Deep dive** | 1200-2000 words | Technical content, comprehensive guides |

---

## Case Study Format

### Structure Template (STAR Framework)

```
# [HEADLINE — Outcome-Focused]

**Sector**: [PRIMARY_SECTOR] | **Type**: Case Study | **Topics**: [TOPIC_TAGS]

---

## Executive Summary (50-100 words)
[One-paragraph summary: who, what challenge, what outcome.
Lead with the result to hook the reader.]

## The Challenge (150-250 words)
[What problem the client faced — specific, evidenced]

**Pain Points:**
- [Pain point 1]
- [Pain point 2]
- [Business impact]

## The Approach (200-300 words)
[What SAS-AM did — methodology, services applied]

**Key Phases:**
1. [Phase 1: Description]
2. [Phase 2: Description]
3. [Phase 3: Description]

**Key Differentiators:**
- [What made SAS-AM's approach different]

## The Outcomes (150-250 words)
[Measurable results achieved — be specific]

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| [Metric 1] | [Before] | [After] | [% or $ improvement] |
| [Metric 2] | [Before] | [After] | [% or $ improvement] |

> "[Client quote if available]" — [Name], [Title]

## Key Learnings (100-150 words)
[What others can learn from this project — transferable insights]

## Ready to Achieve Similar Results? (50-75 words)
[CTA — contact, consultation, related services]

---

**Project Details**: [Sector], [Timeline], [Services Applied]
```

### Case Study Rules

1. **Never fabricate outcomes** — all numbers must come from the user
2. **Anonymous is fine** — "a major water utility" works when names aren't approved
3. **No quotes without permission** — skip the testimonial section if none provided
4. **Specific beats impressive** — "reduced downtime by 23%" beats "significantly reduced downtime"
5. **Show the method** — readers want to understand HOW, not just WHAT

---

## SEO Guidelines

### Title Tag (max 60 characters)

- Include primary keyword
- Include sector if relevant
- Include SAS-AM for brand
- Example: "AI Readiness for Water Utilities | SAS-AM"

### Meta Description (max 160 characters)

- Summarise the value proposition
- Include a call to action
- Example: "Learn the 5 steps water utilities need to become AI-ready. Practical guidance from SAS-AM's asset management experts."

### Heading Hierarchy

```
H1: One per page — the main title
H2: Major sections (3-5 per article)
H3: Subsections within H2s
```

### Keyword Strategy

- Primary keyword in H1 and first paragraph
- Secondary keywords in H2s naturally
- Related terms throughout body
- Don't keyword stuff — readability first

### Internal Linking

- Link to related SAS-AM content where relevant
- Use descriptive anchor text (not "click here")
- 2-4 internal links per article

### Image Alt Text

- Describe what's in the image
- Include keyword if natural
- Keep under 125 characters
- Example: "Maintenance engineer analysing predictive analytics dashboard on tablet"

---

## Webflow MCP Integration

### Prerequisites

Before publishing, verify:

1. **WEBFLOW_TOKEN** environment variable is set
2. **Webflow MCP** is enabled in Claude Code settings
3. Access to the SAS-AM Webflow site

### Available MCP Tools

| Tool | Purpose |
|------|---------|
| `mcp__webflow__sites_list` | List available Webflow sites |
| `mcp__webflow__collections_list` | List CMS collections for a site |
| `mcp__webflow__collections_items_list_items` | List existing items in a collection |
| `mcp__webflow__collections_items_create_item` | Create new CMS item (draft) |
| `mcp__webflow__collections_items_create_item_live` | Create and publish immediately |
| `mcp__webflow__assets` | Upload images/media |

### Publishing Workflow

```
Phase 1: Site Discovery
1. Call sites_list to find sas-am.com site
2. Extract site_id

Phase 2: Collection Discovery
1. Call collections_list with site_id
2. Identify the Resources collection (for articles/case studies)
3. Note field schema for validation

Phase 3: Asset Upload (if hero image generated)
1. Upload hero image via assets endpoint
2. Retrieve asset URL for CMS item

Phase 4: Create Content Item
1. Prepare CMS payload with all required fields
2. Call collections_items_create_item with isDraft: true
3. Return item_id and preview URL for review

Phase 5: Publish (after user review)
1. User confirms content is ready
2. Call collections_items_publish_items
3. Confirm live URL
```

### CMS Field Mapping

Reference the schema in `references/cms-schema.json` for exact field names and types.

Required fields:
- `name` — Article/case study title
- `slug` — URL-friendly version of title
- `sector` — Primary sector (single select)
- `content-type` — "Article" or "Case Study"
- `topic-tags` — Array of tags
- `featured-image` — Hero image URL
- `description` — Meta description (max 160 chars)
- `body-content` — Full content (Rich Text)
- `seo-title` — Title tag (max 60 chars)
- `seo-description` — Meta description

### Error Handling

| Error | Action |
|-------|--------|
| Site not found | List available sites, ask user to confirm |
| Collection not found | List collections, ask user to select |
| Field validation error | Report specific field, show expected format |
| Asset upload failure | Retry or use placeholder |
| Publishing failure | Save content locally, provide recovery path |

---

## nano-banana-2 Integration

### When to Generate Images

Offer hero image generation when:

- User doesn't have an existing image
- Content is finalised and approved
- Topic has clear visual potential

### Prompt Generation

Analyse the content to derive an image prompt:

```
[SCENE derived from content topic]
[SETTING — industrial, office, outdoor, etc.]
[EMOTIONAL TONE — professional, dramatic, optimistic]
```

### Example Prompt Derivations

| Content Topic | Image Prompt |
|---------------|--------------|
| Water utility AI implementation | "Water treatment facility control room with digital monitoring displays, professional engineer analysing data, dramatic industrial lighting" |
| Mining maintenance success | "Heavy mining equipment with modern sensors and data cables, Australian outback setting, golden hour lighting" |
| Asset management maturity | "Professional team reviewing analytics dashboard in modern boardroom, collaborative atmosphere, natural lighting" |

### Calling nano-banana-2

```
/nano-banana-2 "[generated prompt]" --aspect 16:9
```

The skill will:
1. Generate at 16:9 aspect ratio (optimal for Webflow cards)
2. Apply SAS watermark (adaptive light/dark)
3. Compress via Squoosh to 1000px wide, under 200KB JPG
4. Return file path for upload to Webflow

---

## b2b-research-agent Integration

### When to Use Research

Invoke b2b-research-agent when:

- User requests research-backed content
- Content involves industry trends or statistics
- Writing about a specific company or sector

### Research Handoff Pattern

1. User indicates research is needed during interview
2. Invoke: `/b2b-research-agent [topic or company]`
3. Research dossier returned with evidence-tiered findings
4. Incorporate findings with proper attribution
5. All statistics cite sources

### Citation Requirements

Research-sourced content must include:

- Source attribution
- Publication date for recency validation
- Link to source where available

### Integration Example

```
=== Research Integration ===

Source: b2b-research-agent dossier for [Company]
Date: [Date]

Key findings incorporated:
- [Finding 1] — cited in paragraph 3
- [Finding 2] — cited in outcomes section
- [Statistic] — attributed to [Source]
```

---

## Workflow

### Step 1: Interview (MANDATORY)

Run the content type selection, then the appropriate interview questions. Do not proceed until material is gathered.

### Step 2: Research (If Needed)

If user requested research integration:

1. Call `/b2b-research-agent [topic or company]`
2. Review dossier findings
3. Extract relevant evidence for content

### Step 3: Generate Draft

Based on content type:

- **Article**: Follow article template structure
- **Case Study**: Follow STAR framework structure

Apply all voice, tone, and SEO guidelines.

### Step 4: Generate Hero Image (Optional)

If user requested image generation:

1. Derive image prompt from content
2. Call `/nano-banana-2` with 16:9 aspect ratio
3. Present image for approval

### Step 5: Review Draft

Present the complete draft:

```
=== DRAFT PREVIEW ===

[Content preview with all sections]

=== END PREVIEW ===

Questions:
- Does this capture your intent?
- Any facts or figures to adjust?
- Ready to proceed to Webflow, or need revisions?
```

### Step 6: Webflow Publishing

If user approves:

1. Connect to Webflow MCP
2. Upload hero image (if generated)
3. Create CMS item as draft
4. Provide preview URL
5. Await user confirmation
6. Publish live (if confirmed)

```
=== PUBLISHED ===

Status: Live
URL: [live URL]
Preview took: [X] seconds

Content is now visible on www.sas-am.com/resources
```

---

## Quality Checklist

Before presenting final content, verify:

### Content Quality

- [ ] Australian English spelling (organisation, behaviour, analyse, colour, centre)
- [ ] Active voice predominant
- [ ] Opening hook is compelling — would YOU keep reading?
- [ ] Clear value proposition for the reader
- [ ] Technical claims are accurate and achievable
- [ ] No banned words or phrases used
- [ ] Tone is conversational, not corporate
- [ ] Every story, quote, and statistic traces to user interview — nothing fabricated

### SEO Quality

- [ ] SEO title under 60 characters
- [ ] Meta description under 160 characters
- [ ] Primary keyword in H1 and first paragraph
- [ ] Heading hierarchy is logical (H1 > H2 > H3)
- [ ] Alt text prepared for hero image
- [ ] Internal links to related content included

### CMS Readiness

- [ ] Sector selected (single)
- [ ] Topic tags selected (multiple)
- [ ] Content type set (Article or Case Study)
- [ ] Hero image ready (provided or generated)
- [ ] Slug is URL-friendly
- [ ] All required fields populated

---

## Commands

The skill responds to these in-session commands:

| Command | Action |
|---------|--------|
| `interview` | Run the discovery interview |
| `article` | Create a new article |
| `case-study` | Create a new case study |
| `research [topic]` | Invoke b2b-research-agent |
| `draft` | Generate content without publishing |
| `image` | Generate hero image via nano-banana-2 |
| `seo` | Generate/regenerate SEO metadata |
| `preview` | Show formatted content preview |
| `checklist` | Run quality checklist |
| `publish-draft` | Create draft in Webflow CMS |
| `publish-live` | Publish directly to live site |
| `status` | Check Webflow connection status |
| `sectors` | List available sectors |
| `tags` | List available topic tags |

---

## Example Content

### Example Article

```
# Why Your AI Pilot Failed: Data Quality is the Hidden Killer

**Sector**: Resources & Minerals | **Topics**: AI, Machine Learning, Asset Management System

---

Most AI projects in asset management don't fail because of bad algorithms.

They fail because of data.

Specifically, they fail because organisations underestimate what "AI-ready data" actually means — and overestimate how close they are to having it.

After working on dozens of implementations across mining, water, and transport, we've seen the same pattern emerge:

## The Four Data Quality Killers

### 1. Inconsistent CMMS Records

Your maintenance management system is only as good as the data going into it. When work orders use free text instead of structured fields, when failure codes are applied inconsistently, when one site does things differently from another — the AI has nothing reliable to learn from.

### 2. Disconnected Sensor Data

Many organisations have invested in condition monitoring systems. Vibration sensors, temperature probes, flow meters. But the data sits in its own silo, disconnected from asset hierarchies and maintenance history. The AI can't connect cause and effect.

### 3. Missing Failure History

AI learns from patterns. If you don't have reliable records of what failed, when it failed, and why — there's no pattern to learn. "Equipment failed" isn't useful. "Bearing failure due to inadequate lubrication after 18 months of operation" is.

### 4. No Data Ownership

Here's the one that kills most projects: nobody owns data quality as an ongoing discipline. It's everyone's job, which means it's nobody's job. Cleanup projects come and go, but the underlying behaviours don't change.

## What Actually Works

The organisations successfully using AI started with what they had and improved the data as part of the AI project, not before it.

Focus on:

- **Critical assets only** — don't try to clean everything
- **Target failure modes** — pick the failures that cost you the most
- **2-3 years of history** — not decades
- **One data quality owner** — not a committee

## The Honest Answer

AI readiness is 80% data work and 20% model work. The "we're not ready" story feels safe. But it's often a way to avoid the harder conversation: "we don't know where to start."

Start small. Pick one critical asset. Clean that data. Build one model. Learn.

---

**Ready to assess your AI readiness?** Contact SAS-AM for a practical assessment that identifies your quickest wins.

**Related**: [5 Signs Your Data Isn't AI-Ready], [The ISO 55001 Data Quality Connection]
```

### Example Case Study

```
# Gold Mining Maintenance: 23% Reduction in Unplanned Downtime

**Sector**: Resources & Minerals | **Type**: Case Study | **Topics**: Asset Condition, Machine Learning, Advisory

---

## Executive Summary

A major Australian gold producer reduced unplanned equipment downtime by 23% across their processing facility by implementing condition-based maintenance with predictive analytics. The project delivered $1.4M in annual savings within 12 months.

## The Challenge

The client operated a gold processing facility with over 200 rotating assets including crushers, mills, and conveyors. Their maintenance approach was predominantly calendar-based, with fixed intervals regardless of actual equipment condition.

**Pain Points:**
- 15% unplanned downtime on critical crushing equipment
- $6M annual maintenance spend with limited visibility into effectiveness
- Reactive culture — fixing failures rather than preventing them
- Sensor data existed but wasn't connected to maintenance decisions

## The Approach

SAS-AM partnered with the maintenance and reliability teams over 8 months to implement a practical condition-based maintenance programme.

**Phase 1: Critical Asset Identification (2 months)**
- Mapped all assets by criticality using risk-based methodology
- Identified 35 critical rotating assets for initial focus
- Documented dominant failure modes for each asset type

**Phase 2: Data Integration (3 months)**
- Connected existing vibration monitoring to asset hierarchy
- Cleaned CMMS data for target assets
- Built initial condition indicators

**Phase 3: Predictive Model Development (3 months)**
- Developed failure prediction models for top 10 failure modes
- Integrated predictions into daily planning workflow
- Trained maintenance planners on interpreting recommendations

**Key Differentiator:** The maintenance team was involved from day one. They helped define what "useful" meant and shaped the system around their actual decision-making process.

## The Outcomes

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Unplanned downtime | 15% | 11.5% | 23% reduction |
| Maintenance spend | $6M | $4.6M | $1.4M annual savings |
| Bearing failures | 42/year | 28/year | 33% reduction |
| Planner time on reactive work | 60% | 35% | 42% reduction |

> "The difference is we're now making decisions based on what the equipment is telling us, not what the calendar says. The maintenance team trusts the system because they helped build it." — Maintenance Manager

## Key Learnings

1. **Start narrow** — 35 critical assets, not 200+ total assets
2. **Use existing sensors** — no major capital investment required
3. **Involve the team** — buy-in comes from participation, not presentations
4. **Connect to decisions** — predictions are useless without action pathways

## Ready to Achieve Similar Results?

Contact SAS-AM for a practical assessment of your predictive maintenance opportunity. We start with what you have and build from there.

---

**Project Details**: Resources & Minerals, 8 months, Reliability Engineering + Advanced Analytics
```

---

## Reference Files

- `references/article-template.md` — Article structure template
- `references/case-study-template.md` — Case study STAR framework template
- `references/cms-schema.json` — Webflow CMS field mapping
- `references/seo-checklist.md` — SEO optimisation checklist
- `references/sector-guidelines.md` — Sector-specific messaging guidelines

---

## Final Notes

- **Be genuinely helpful**: Every piece of content should leave the reader better off
- **Respect intelligence**: Our audience are professionals — don't patronise
- **Stay grounded**: We're practitioners, not academics or pure theorists
- **Show personality**: It's okay to have opinions and express them
- **Build trust**: Consistency, accuracy, and honesty compound over time
- **One piece, one idea**: Don't try to cover everything — depth beats breadth

When in doubt, ask: "Would a senior asset management professional find this valuable and credible?" If yes, publish. If not, revise.
