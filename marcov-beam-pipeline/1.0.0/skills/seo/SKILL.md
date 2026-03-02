---
name: MBP:seo
description: Comprehensive SEO analysis for the SAS-AM website. Use when the user wants to run a technical SEO audit, assess content quality (E-E-A-T), optimise for AI search engines (GEO), validate schema markup, analyse sitemaps, or plan SEO strategy. Based on AgriciDaniel/claude-seo with MBP-specific integrations for keyword overlap analysis, ad landing page quality, and content ROI measurement. Part of the Marcov Beam Pipeline.
---

# MBP:seo — SEO Analysis & Optimisation

Comprehensive SEO analysis that connects organic search performance to the broader marketing pipeline. Built on AgriciDaniel/claude-seo with additional MBP integrations.

## Overview

This skill provides:

- **Technical SEO audits** — crawlability, indexability, security, mobile, Core Web Vitals, schema, JS rendering
- **E-E-A-T content quality** — Experience, Expertise, Authoritativeness, Trustworthiness scoring
- **Generative Engine Optimisation (GEO)** — visibility in Google AI Overviews, ChatGPT, Perplexity
- **Schema markup** — detection, validation, and generation of JSON-LD structured data
- **Sitemap analysis** — XML validation, generation, and quality gates
- **Image optimisation** — alt text, file size, format, lazy loading, CLS prevention
- **Strategic planning** — industry-specific SEO strategies (SaaS, local, ecommerce, publisher, agency)
- **MBP integrations** — keyword overlap with Google Ads, landing page quality for ad campaigns, content ROI measurement

## Prerequisites

This skill requires the AgriciDaniel/claude-seo installation. If not installed:

```bash
curl -fsSL https://raw.githubusercontent.com/AgriciDaniel/claude-seo/main/install.sh | bash
```

**Optional MCP servers** for live data:
- Ahrefs (`@ahrefs/mcp`) — backlinks, keywords, site audit
- Semrush (`https://mcp.semrush.com/v1/mcp`) — domain analytics, keyword research
- Google Search Console (`mcp-server-gsc`) — search performance, URL inspection

---

## Commands

### Core SEO Commands (from AgriciDaniel/claude-seo)

| Command | What It Does |
|---|---|
| `/MBP:seo audit <url>` | Full site audit — crawls up to 500 pages, delegates to 6 parallel subagents |
| `/MBP:seo page <url>` | Deep single-page analysis (on-page, content, technical, schema, images, CWV) |
| `/MBP:seo technical <url>` | 8-category technical audit |
| `/MBP:seo content <url>` | E-E-A-T scoring + content quality + AI citation readiness |
| `/MBP:seo schema <url>` | Schema.org detection, validation, and generation |
| `/MBP:seo images <url>` | Image optimisation analysis |
| `/MBP:seo sitemap <url>` | XML sitemap validation or generation |
| `/MBP:seo geo <url>` | GEO — AI search engine visibility optimisation |
| `/MBP:seo plan <type>` | Strategic SEO planning (saas, local, ecommerce, publisher, agency) |
| `/MBP:seo programmatic <url>` | Programmatic SEO at scale |
| `/MBP:seo competitor-pages <url>` | X vs Y comparison page generation |
| `/MBP:seo hreflang <url>` | International SEO — hreflang validation |

### MBP Integration Commands (new)

| Command | What It Does |
|---|---|
| `/MBP:seo keyword-overlap` | Compare organic keyword rankings with MBP:google-ads paid keywords. Find terms where you rank #1 organically but still pay for clicks — eliminate waste. Find terms where organic is weak but paid performs — invest in SEO for those. |
| `/MBP:seo landing-quality` | Score the landing pages used in Google Ads and LinkedIn Ads campaigns for SEO quality. Higher-quality pages = better ad Quality Score = lower CPC = higher ROAS. |
| `/MBP:seo content-roi` | Correlate SEO content scores with GA4 traffic and conversion data from MBP:website-analytics. Which content drives the most organic traffic and conversions? What's the ROI of SEO investment? |

---

## MBP Integration: Keyword Overlap Analysis

### Purpose
Identify where paid and organic search overlap to optimise spend.

### Data Sources
- MBP:google-ads output (`.marketing/google-ads/latest.json`) — paid keywords and performance
- Ahrefs/Semrush MCP (if available) — organic keyword rankings
- Google Search Console MCP (if available) — organic search queries

### Analysis
1. Extract top paid keywords from Google Ads data
2. Check organic ranking position for each paid keyword
3. Categorise:
   - **Organic #1-3 + Paying:** Stop paying — you already own this SERP. Redirect budget.
   - **Organic #4-10 + Paying:** Consider reducing bids — organic is close to dominating.
   - **Organic #11+ + Paying well:** Invest in SEO for these terms — long-term cost reduction.
   - **No organic presence + Paying:** Pure paid dependency — create content targeting these terms.

### Output
```markdown
## Keyword Overlap Analysis

| Keyword | Organic Position | Paid CPC | Monthly Paid Spend | Action |
|---|---|---|---|---|
| asset management consultant | #2 | $8.50 | $340 | STOP PAYING — redirect $340/mo |
| ISO 55001 assessment | #15 | $4.20 | $168 | SEO INVEST — create pillar article |
| predictive maintenance mining | Not ranking | $12.00 | $480 | CONTENT GAP — build organic presence |

**Estimated monthly savings from overlap elimination: $510**
```

---

## MBP Integration: Landing Page Quality

### Purpose
Score ad campaign landing pages for SEO quality factors that directly impact ad performance.

### Data Sources
- MBP:google-ads output — landing page URLs from campaigns
- MBP:linkedin-ads output — destination URLs from campaigns
- SEO audit engine — page-level quality scoring

### Analysis
For each landing page used in paid campaigns:
1. Run E-E-A-T analysis
2. Check Core Web Vitals (LCP, INP, CLS)
3. Validate schema markup
4. Assess content quality and relevance
5. Score overall SEO health

### Impact on Ads
- Google Ads Quality Score is influenced by landing page experience
- Better landing page = higher Quality Score = lower CPC = more clicks for same budget
- LinkedIn Ads relevance score also considers landing page quality

---

## MBP Integration: Content ROI

### Purpose
Measure the return on SEO investment by correlating content quality scores with traffic and conversion data.

### Data Sources
- MBP:website-analytics output (`.marketing/website/latest.json`) — page-level traffic and conversions
- SEO content scores — E-E-A-T, GEO readiness, technical health per page

### Analysis
1. Pull top pages from GA4 data (by organic traffic)
2. Score each page for SEO quality
3. Correlate: do higher-scoring pages drive more traffic and conversions?
4. Identify underperforming pages with high traffic but low SEO scores (quick wins)
5. Identify high-quality pages with low traffic (promotion opportunities)

### Output
```markdown
## Content ROI Analysis

| Page | SEO Score | Monthly Organic Sessions | Conversions | Conv. Rate | Action |
|---|---|---|---|---|---|
| /iso-55001-maturity | 89 | 340 | 12 | 3.5% | SCALE — promote via MBP:linkedin-ads |
| /services/data-quality | 42 | 180 | 2 | 1.1% | OPTIMISE — low SEO score hurting conversions |
| /blog/ai-maintenance | 78 | 15 | 0 | 0% | PROMOTE — quality content not getting traffic |
```

---

## State Output

After any analysis, save normalised metrics to `.marketing/seo/latest.json`:

```json
{
  "platform": "seo",
  "period": { "start": "2026-02-01", "end": "2026-02-28" },
  "metrics": {
    "seo_health_score": 72,
    "eeat_score": 68,
    "geo_readiness_score": 55
  },
  "issues": [
    { "severity": "critical", "description": "Missing schema markup on 12 pages", "recommendation": "Add Organization and Article schema" },
    { "severity": "high", "description": "CLS > 0.25 on mobile for 3 landing pages", "recommendation": "Fix image dimensions and font loading" }
  ],
  "top_performers": [
    { "name": "/iso-55001-maturity", "type": "page", "metric_value": 89, "metric_name": "seo_score" }
  ],
  "generated_at": "2026-02-28T14:30:00Z"
}
```

---

## Technical SEO Audit Categories

The 8-category technical audit covers:

1. **Crawlability** — robots.txt, sitemap referencing, noindex detection, crawl depth, JS rendering, AI crawler management (GPTBot, ClaudeBot, PerplexityBot)
2. **Indexability** — canonical tags, duplicate content, thin content, pagination, hreflang, index bloat
3. **Security** — HTTPS, SSL certificate, security headers (CSP, HSTS, X-Frame-Options)
4. **URL Structure** — clean URLs, logical hierarchy, redirect chains, character limits, trailing slash consistency
5. **Mobile Optimisation** — responsive design, viewport meta, touch targets (48x48px), font size (min 16px)
6. **Core Web Vitals** — LCP (<2.5s), INP (<200ms), CLS (<0.1), using 75th percentile field data
7. **Structured Data** — JSON-LD detection/validation, Google-supported type checking, deprecation warnings
8. **JavaScript Rendering** — SSR vs CSR detection, SPA framework identification

---

## E-E-A-T Scoring (September 2025 QRG Update)

| Dimension | Weight | Signals |
|---|---|---|
| Experience | 20% | First-hand knowledge, original photos, case studies, before/after results |
| Expertise | 25% | Author credentials, technical accuracy, evidence-based claims, specialist vocabulary |
| Authoritativeness | 25% | External citations, brand mentions, industry recognition, publication history |
| Trustworthiness | 30% | Contact info, privacy policy, HTTPS, transparency, customer reviews |

**Important:** E-E-A-T now applies to ALL competitive queries, not just YMYL.

---

## GEO Scoring (Generative Engine Optimisation)

| Factor | Weight | What It Measures |
|---|---|---|
| Citability | 25% | Optimal passage length (134-167 words), quotable facts, self-contained blocks |
| Structural Readability | 20% | Clean heading hierarchy, question-based headings, lists/tables |
| Multi-Modal Content | 15% | Text + images, video, infographics, interactive elements |
| Authority & Brand | 20% | Author credentials, citations, Wikipedia/Reddit/YouTube presence |
| Technical Access | 20% | Server-side rendering, AI crawler access, llms.txt compliance |

---

## Content Guidelines

- Use Australian English throughout all reports and recommendations
- Reference `shared/brand-voice.md` for tone and language rules
- Reference `shared/sas-branding.md` for report visual styling
- All monetary values in AUD
