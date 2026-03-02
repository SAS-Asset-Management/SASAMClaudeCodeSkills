# SEO Skill Integration — Assessment & MBP Fit

**Date:** 2026-02-28
**Context:** User asked to review `scrivo21/claude-seo`. That repo doesn't exist yet. Assessed 3 existing Claude SEO skill repos for fork/integrate potential into the Marcov Beam Pipeline (MBP).

---

## Candidates Assessed

| Repo | Stars | Skills | MCP Support | License | Best For |
|---|---|---|---|---|---|
| **AgriciDaniel/claude-seo** | 1.4k | 12 sub-skills + 6 subagents | Ahrefs, Semrush, GSC, PageSpeed, DataForSEO | MIT | Comprehensive SEO — technical audits, E-E-A-T, GEO, schema, programmatic SEO |
| **mangollc/claude-seo-skill** | — | 6 skill areas | Firecrawl | MIT | Agency-focused — local SEO, AEO, GBP management |
| **huifer/claude-code-seo** | — | 7 skills, 27+ commands | — | — | Next.js-specific — 100-point scoring, bilingual (Chinese/English) |

### Recommendation: Fork AgriciDaniel/claude-seo

**Why:**
- Most comprehensive (12 sub-skills covering everything)
- Already has MCP integrations for major SEO tools (Ahrefs, Semrush, GSC)
- Production-ready with security hardening (v1.2.0)
- MIT license — free to fork and modify
- Python-based — matches SAS-AM's existing Python skills (tender-assessment)
- Has NO marketing/ads integration — we add that (competitive advantage)
- Parallel subagent architecture — handles large audits efficiently
- Quality gates built-in — prevents bad recommendations at scale

---

## AgriciDaniel/claude-seo Feature Map

### 13 Commands
| Command | What It Does |
|---|---|
| `/seo audit <url>` | Full site audit — crawls up to 500 pages, delegates to 6 parallel subagents |
| `/seo page <url>` | Deep single-page analysis (on-page, content quality, technical, schema, images, CWV) |
| `/seo technical <url>` | 8-category technical audit (crawlability, indexability, security, mobile, CWV, schema, JS rendering) |
| `/seo content <url>` | E-E-A-T scoring + content quality + AI citation readiness |
| `/seo schema <url>` | Schema.org detection, validation, and generation (JSON-LD/Microdata/RDFa) |
| `/seo images <url>` | Alt text, file size, format, lazy loading, CLS prevention |
| `/seo sitemap <url>` | XML sitemap validation or generation with industry templates |
| `/seo geo <url>` | Generative Engine Optimization — AI Overviews, ChatGPT, Perplexity visibility |
| `/seo plan <type>` | Strategic planning (saas, local, ecommerce, publisher, agency) |
| `/seo programmatic <url>` | Programmatic SEO at scale — data-driven page generation |
| `/seo competitor-pages <url>` | X vs Y comparison page generation with schema |
| `/seo hreflang <url>` | International SEO — hreflang validation and generation |

### MCP Integrations
| MCP Server | Data Source | What It Provides |
|---|---|---|
| Ahrefs (`@ahrefs/mcp`) | Ahrefs API | Backlinks, keywords, site audit, competitive analysis |
| Semrush (`https://mcp.semrush.com/v1/mcp`) | Semrush API | Domain analytics, keyword research, backlinks |
| Google Search Console (`mcp-server-gsc`) | GSC API | Search performance, URL inspection, sitemaps |
| PageSpeed Insights (`mcp-server-pagespeed`) | PSI API | Lighthouse audits, CWV metrics |
| DataForSEO (`dataforseo-mcp-server`) | DataForSEO API | SERP data, keyword data, backlinks |

### Key Scores & Metrics
- **SEO Health Score:** 0-100 (weighted: Technical 25%, Content 25%, On-Page 20%, Schema 10%, CWV 10%, Images 5%, AI Readiness 5%)
- **E-E-A-T Score:** 0-100 (Experience 20%, Expertise 25%, Authoritativeness 25%, Trustworthiness 30%)
- **GEO Readiness Score:** 0-100 (Citability 25%, Structural Readability 20%, Multi-Modal 15%, Authority 20%, Technical Access 20%)
- **Core Web Vitals:** LCP (<2.5s), INP (<200ms), CLS (<0.1)

---

## How SEO Fits Into the MBP Measurement Chain

SEO is the **organic engine** that complements paid ads. Currently the MBP chain covers:

```
PAID:     b2b-research → Google/LinkedIn Ads → Website → BEAM pipeline
ORGANIC:  ??? → ??? → Website → BEAM pipeline
```

With SEO integrated:

```
PAID:     b2b-research → Google/LinkedIn Ads → Website → BEAM pipeline
ORGANIC:  SEO strategy → Content optimisation → Organic traffic → Website → BEAM pipeline
          ↑                                      ↑
          │                                      │
          └── keyword research informs both paid AND organic strategy
              content performance feeds back to ad messaging
```

### Specific Integration Points

| MBP Skill | SEO Integration | Measurement Value |
|---|---|---|
| **MBP:google-ads** | SEO keyword data reveals organic/paid keyword overlap. Stop paying for keywords you rank #1 organically. | Save wasted ad spend on terms with strong organic presence |
| **MBP:linkedin-ads** | E-E-A-T score of landing pages affects ad quality and conversion rate. Higher-quality pages = better ad ROI. | Measure landing page quality impact on ad conversion rates |
| **MBP:website-analytics** | Organic traffic is the largest traffic source for most B2B sites. SEO audit findings explain traffic changes. | Attribute organic traffic growth/decline to specific SEO actions |
| **MBP:linkedin-post** | GEO analysis reveals what content structures get cited by AI search. Inform post topics from organic search demand. | Content topics driven by search demand, not guesswork |
| **MBP:marketing-dashboard** | Organic channel becomes measurable alongside paid channels. True marketing ROI includes SEO investment. | Full-channel attribution: paid + organic + direct |
| **MBP:b2b-research** | Competitor SEO analysis reveals what prospects are searching for. Informs targeting intelligence. | Research-informed content strategy |
| **MBP:beam-selling** | High-ranking content builds trust before sales conversations. Prospects who read SEO-optimised articles arrive more educated. | Measure content-influenced pipeline |
| **MBP:presentation** | SEO insights feed into pitch content (e.g., "your site scores 42/100 — we can help") | SEO audit as a sales tool |

### The Full MBP Chain with SEO

```
RESEARCH        MARKETING (PAID)        MARKETING (ORGANIC)     WEBSITE              SALES
────────        ────────────────        ───────────────────     ───────              ─────
MBP:b2b-research  MBP:google-ads        MBP:seo                MBP:website-analytics  MBP:beam-selling
MBP:tender        MBP:linkedin-ads      MBP:linkedin-post                              │
                  MBP:linkedin-post                                                     │
                       │                       │                      │                 │
                       │  Campaign             │  SEO strategy        │  All traffic     │  Pipeline
                       │  performance          │  + content quality   │  + conversions   │  progression
                       ▼                       ▼                      ▼                 ▼
                ┌──────────────────────────────────────────────────────────────────────────┐
                │                     MBP:marketing-dashboard                              │
                │  Attribution: Paid spend vs Organic investment vs Pipeline value         │
                │  Keyword overlap: Stop paying for organic #1 rankings                   │
                │  Content ROI: Which articles drive the most pipeline value?              │
                │  SEO health: Is the site technically sound for both users and AI?        │
                └──────────────────────────────────────────────────────────────────────────┘
```

---

## Proposed MBP Integration: MBP:seo

### Approach: Fork + Adapt

1. **Fork** `AgriciDaniel/claude-seo` to `scrivo21/claude-seo`
2. **Restructure** to match MBP skill convention (SKILL.md + references/)
3. **Rename** commands from `/seo <subcommand>` to `/MBP:seo <subcommand>`
4. **Add integrations** that don't exist in the original:
   - Organic/paid keyword overlap analysis (reads MBP:google-ads output)
   - Landing page quality scoring for ad campaigns (feeds MBP:linkedin-ads, MBP:google-ads)
   - Content performance correlation with GA4 data (reads MBP:website-analytics output)
   - SEO health score written to `.marketing/seo/latest.json` for dashboard aggregation
5. **Add to marketing-dashboard** as an organic channel alongside paid channels
6. **Add SAS-AM context**: Asset management industry keyword templates, B2B SEO strategy template

### MBP Directory Addition

```
marcov-beam-pipeline/1.0.0/
└── skills/
    └── seo/
        ├── SKILL.md                         # name: MBP:seo
        ├── requirements.txt                 # Python deps (beautifulsoup4, requests, lxml, playwright)
        ├── scripts/
        │   ├── fetch_page.py
        │   ├── parse_html.py
        │   ├── analyze_visual.py
        │   └── capture_screenshot.py
        ├── agents/                          # 6 subagents for parallel audit
        │   ├── seo-technical.md
        │   ├── seo-content.md
        │   ├── seo-schema.md
        │   ├── seo-sitemap.md
        │   ├── seo-performance.md
        │   └── seo-visual.md
        └── references/
            ├── eeat-framework.md
            ├── cwv-thresholds.md
            ├── schema-types.md
            ├── quality-gates.md
            ├── seo-report-template.md       # NEW: MBP-formatted report
            ├── keyword-overlap-template.md   # NEW: Organic/paid overlap analysis
            └── industry-templates/
                ├── asset-management.md       # NEW: SAS-AM specific SEO strategy
                ├── saas.md
                ├── local-service.md
                ├── ecommerce.md
                ├── publisher.md
                └── agency.md
```

### New Commands Under MBP:seo

All original commands preserved, plus new MBP integrations:

| Command | Original? | What It Does |
|---|---|---|
| `/MBP:seo audit <url>` | Yes | Full site audit with 6 parallel subagents |
| `/MBP:seo page <url>` | Yes | Deep single-page analysis |
| `/MBP:seo technical <url>` | Yes | 8-category technical audit |
| `/MBP:seo content <url>` | Yes | E-E-A-T + content quality |
| `/MBP:seo schema <url>` | Yes | Schema detection/validation/generation |
| `/MBP:seo images <url>` | Yes | Image optimisation analysis |
| `/MBP:seo sitemap <url>` | Yes | XML sitemap analysis/generation |
| `/MBP:seo geo <url>` | Yes | AI search optimisation (GEO) |
| `/MBP:seo plan <type>` | Yes | Strategic SEO planning |
| `/MBP:seo programmatic <url>` | Yes | Programmatic SEO at scale |
| `/MBP:seo competitor-pages <url>` | Yes | X vs Y comparison pages |
| `/MBP:seo hreflang <url>` | Yes | International SEO (hreflang) |
| `/MBP:seo keyword-overlap` | **NEW** | Compare organic rankings with Google Ads keywords — find waste |
| `/MBP:seo landing-quality` | **NEW** | Score ad landing pages for SEO quality — improve ad conversion |
| `/MBP:seo content-roi` | **NEW** | Correlate content SEO scores with GA4 traffic and conversions |

### State Output

```
.marketing/
└── seo/
    ├── latest.json              # SEO health score, top issues, keyword data
    └── history/{date}.json      # Historical snapshots for trend tracking
```

---

## Updated MBP Skill Count: 13

| # | Command | Category | Status |
|---|---|---|---|
| 1 | `/MBP:b2b-research` | Research | Existing (migrate) |
| 2 | `/MBP:beam-selling` | Sales | Existing (migrate) |
| 3 | `/MBP:google-ads` | Marketing | New |
| 4 | `/MBP:linkedin-ads` | Marketing | New |
| 5 | `/MBP:website-analytics` | Marketing | New |
| 6 | `/MBP:marketing-dashboard` | Marketing | New |
| 7 | `/MBP:seo` | Marketing (Organic) | New (fork AgriciDaniel/claude-seo) |
| 8 | `/MBP:linkedin-post` | Content | Existing (migrate) |
| 9 | `/MBP:presentation` | Content | Existing (migrate) |
| 10 | `/MBP:tender` | Research | Existing (migrate) |
| 11 | `/MBP:data-quality` | Analytics | Existing (migrate) |
| 12 | `/MBP:nano-banana` | Content | Existing (migrate) |
| 13 | `/MBP:notifications` | Integration | Existing (migrate) |

---

## Implementation Priority

1. **Fork** `AgriciDaniel/claude-seo` → `scrivo21/claude-seo`
2. **Build** 4 marketing analytics skills (google-ads, linkedin-ads, website-analytics, marketing-dashboard)
3. **Integrate** SEO into marketing-dashboard as organic channel
4. **Add** 3 new MBP-specific SEO commands (keyword-overlap, landing-quality, content-roi)
5. **Migrate** 8 existing skills into MBP namespace
6. **Test** full measurement chain: research → ads + SEO → website → pipeline

---

*SEO integration assessment: 2026-02-28*
