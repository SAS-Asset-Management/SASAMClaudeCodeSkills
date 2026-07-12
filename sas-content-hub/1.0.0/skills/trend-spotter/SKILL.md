---
name: trend-spotter
description: Surface what is working in the audience's feed RIGHT NOW and turn it into ready to use hooks for the SAS-AM content pipeline. Use when the user wants to "spot trends", "what's working on LinkedIn", "find viral hooks", "run a competitor trend scan", "trend spotter", "reverse engineer a competitor's best posts", "what's the algorithm rewarding", "find outlier posts", "scan creators", or wants trend intelligence before drafting content. Pulls recent posts for a set of creators or a topic, scores each post against THAT creator's own baseline, flags the outliers that significantly overperformed, reverse engineers each outlier's hook, format, topic and angle, and hands a ranked trend report plus reusable hook templates into linkedin-post-generator and content-campaign. Platforms: LinkedIn (primary for asset management professionals), plus X, YouTube and Reddit.
---

# SAS-AM Trend Spotter

Find what is overperforming in your audience's feed right now, understand WHY, and convert it into hooks and formats the SAS-AM pipeline can use the same day. This skill is the front of the funnel — it decides what to say. `linkedin-post-generator` and `content-campaign` decide how to say it.

The core idea: the algorithm is a live experiment running on every creator at once. A post that beats a creator's own typical numbers is a signal that the algorithm — and the audience — is rewarding that hook, format or angle. Those overperformers are the outliers. Outliers are the trend.

## When to Use

- "What's working on LinkedIn in asset management right now?"
- "Run a competitor trend scan on Assetivity and two others."
- "Find me viral hooks I can adapt for a reliability post."
- "Reverse engineer the best posts from these five creators."
- "What's the algorithm rewarding this month — before I draft anything?"

Do NOT use this to draft the finished post — that is `linkedin-post-generator`. Trend Spotter stops at the hook and format brief, then hands off.

## What This Skill Refuses to Do

- **Never invent numbers.** Every performance figure must come from a real source (see `references/dataSources.md`). If a figure cannot be sourced, it is reported as "not available", never estimated and never fabricated.
- **Never scrape in violation of a platform's terms.** Raw scraping is brittle and ToS sensitive. This skill prefers official and MCP data sources and the user's own logged in browser session, and is explicit about what is reliable versus aspirational.
- **Never present a low confidence read as fact.** Small samples and unofficial data get a confidence flag.

## Inputs — Intake Interview

Interview the user one question at a time, multiple choice where possible, waiting for each answer (SAS house style). Do not ask everything at once.

**Q1 — Target of the scan**
> "What should I scan?"
> A) A named set of creators or competitors (you give me the handles or names)
> B) A topic or niche (I find who is winning in that space)
> C) Both — seed creators plus a topic to widen the net

Default competitor example if the user wants a starting point: **Assetivity** (the recurring SAS-AM competitor, per `sas-seo`). Offer it, do not assume it.

**Q2 — Platform(s)**
> "Which platform(s)?"
> A) LinkedIn only (default — SAS-AM's audience of asset management professionals lives here)
> B) LinkedIn plus X
> C) Add YouTube (for long form / thought leadership creators)
> D) Add Reddit (for r/AssetManagement, r/reliability, r/maintenance and similar)
> E) All of the above

**Q3 — Timeframe**
> "How far back should I look? (Default: last 30 days.)"
> A) Last 30 days (default)
> B) Last 7 days (fast moving / newsjacking)
> C) Last 90 days (slower B2B cadence, more posts per creator)

**Q4 — Angle bias (optional)**
> "Any SAS-AM theme to weight toward? (AI & analytics, maturity & compliance, risk & reliability, sovereign AI, community impact — or no bias.)"

**Q5 — Output intent**
> "What do you want out of this?"
> A) A ranked trend report only (I will decide what to write later)
> B) Report plus a handoff brief straight into linkedin-post-generator
> C) Report plus kick off a full content-campaign around the strongest trend

Record the answers. Q5 determines the handoff (see Handoff Contract).

## Method — Baseline, Outlier, Reverse Engineer

Full maths and worked examples live in `references/outlierMethod.md`. The shape:

1. **Pull recent posts** for each creator within the timeframe (via the sources in `references/dataSources.md`). Capture, per post: the hook (first line), format, topic, angle, post date, and the available engagement metrics (reactions, comments, reposts, views where exposed).

2. **Compute each creator's own baseline.** Trends are relative, not absolute — a 400-reaction post is only impressive against a creator who normally gets 80. For each creator, compute a central tendency (median is preferred over mean because engagement is heavily skewed) of an engagement measure across their in window posts. Comments are weighted more heavily than reactions because they are the stronger algorithmic and intent signal.

3. **Flag the outliers.** A post is an outlier when it beats the creator's own baseline by a set multiple (default: performance score >= 2x the creator's median, or top decile of their in window posts, whichever is stricter on small samples). Outliers — not raw top posts — are the output, because they control for audience size and reveal what the algorithm rewarded for THAT creator.

4. **Reverse engineer each outlier.** For every flagged post, decompose:
   - **Hook** — the first line and the psychological trigger it pulls (map to the trigger taxonomy in `linkedin-post-generator`: uncomfortable truth, specific number, permission to fail, confrontation, open loop, status threat, shared enemy).
   - **Format** — story-led, contrarian comparison, myth-bust, list/carousel, confession, data-as-hero, transformation.
   - **Topic & angle** — what it was about and the specific stance taken.
   - **Why it worked** — a one line hypothesis tying the hook and format to the overperformance.

5. **Cluster and rank.** Group outliers by recurring hook trigger, format and topic. A pattern that appears across multiple creators is a stronger trend than a one off. Rank by: cross creator recurrence, outlier strength (multiple over baseline), and fit to the SAS-AM audience and themes.

## Data Sourcing — Reliable vs Aspirational (Be Honest)

The single biggest failure mode of a trend tool is confidently reporting numbers it cannot actually get. Read `references/dataSources.md` before every run and state which tier each figure came from. Summary:

- **Reliable today**
  - SAS-AM's own owned data — the website-analytics stack (GA4, Search Console, Clarity on Cortex4) and the socialContentEngine `linkedin-post-analyser` for SAS-AM's own LinkedIn post performance. This is the ground truth for OUR baseline.
  - `WebSearch` / `WebFetch` for public posts, articles, YouTube video pages, and Reddit threads that are openly indexed.
  - `claude-in-chrome` browser automation to read a feed the USER is already logged into (their LinkedIn, YouTube, X, Reddit session). Session based, user driven, and still ToS sensitive — surface what you are about to do and let the user drive the login.
- **Aspirational / gated (call out, do not pretend)**
  - Native platform APIs — LinkedIn API, YouTube Data API, Reddit API, X API. None are connected as MCP in this environment today. If one is needed, it must be added (e.g. via the MCP_DOCKER `mcp-add` flow) and consented before it can supply numbers.
- **Discovery each run** — run a `ToolSearch` for "youtube", "reddit", "linkedin", "x twitter", "analytics" MCP at the start of a scan. If a native connector has since been added, prefer it and say so. If not, fall back to the reliable tier and flag any platform where only public/estimated signal is available.

When a platform exposes no reliable count (common for LinkedIn view counts on other people's posts), rank by the signal you CAN see (comments and reposts are usually visible) and mark the metric basis in the report.

## Outputs

Three artefacts, templates in `references/outputTemplates.md`:

1. **Ranked trend report** (markdown) — the top outliers with, for each: creator, platform, date, the metric basis and confidence tier, multiple over that creator's baseline, the reverse engineered hook/format/topic/angle, and the one line why it worked. Followed by the clustered trend ranking (what is recurring across creators).

2. **Reusable hook & format templates** — each strong trend abstracted into a reusable pattern and then adapted to SAS-AM voice (Australian English, no emojis, no hashtags, practitioner tone, no fabricated stories). Each template names: the trigger, the skeleton, an SAS-AM-flavoured example hook, and which `linkedin-post-generator` format it maps to.

3. **Handoff brief** — a compact block the next skill consumes directly (see below).

## Handoff Contract

Trend Spotter feeds the existing pipeline. It never duplicates drafting, voice or publishing logic — it supplies the brief those skills already know how to consume.

- **To `linkedin-post-generator`** (Q5 = B): emit a brief containing the chosen trend's topic, the recommended format(s) mapped to that skill's format library, 2–3 adapted candidate hooks, and the source outliers as evidence. The user still runs the mandatory interview in `linkedin-post-generator` to supply the real story/data — Trend Spotter supplies the angle and hook, never invented anecdotes or numbers.
- **To `content-campaign`** (Q5 = C): emit the trend as the campaign topic (its Q1) and a suggested sector (its Q2), plus the hook templates as raw material for the LinkedIn stage. `content-campaign` orchestrates artefact → gate → article → LinkedIn from there.
- **Handoff brief shape** (also in `references/outputTemplates.md`):

```
=== Trend Handoff ===
Trend: <one line description of the winning pattern>
Recommended format(s): <mapped to linkedin-post-generator formats>
Candidate hooks (SAS-AM voice):
  1. <hook>
  2. <hook>
Source outliers (evidence): <creator/platform/date + why it worked>
Suggested SAS-AM theme/sector: <from Q4 / audience fit>
Next skill: /linkedin-post-generator  (or  /content-campaign)
```

## Workflow

1. **Intake interview** (Q1–Q5), one question at a time.
2. **Discover sources** — `ToolSearch` for any native social/analytics MCP; otherwise confirm the reliable tier (own analytics + WebSearch/WebFetch + claude-in-chrome). Tell the user which tier this run will use and where the honesty limits are.
3. **Collect** recent posts per creator/topic within the timeframe. Record hook, format, topic, angle, date, metrics, and the metric basis + confidence tier per post.
4. **Baseline + outlier detection** per `references/outlierMethod.md`.
5. **Reverse engineer** each outlier; cluster and rank.
6. **Write** the ranked trend report and the reusable hook/format templates (`references/outputTemplates.md`).
7. **Adapt to SAS-AM voice** — every candidate hook obeys the `linkedin-post-generator` voice rules. No hyphens in prose (use em dashes or restructure), Australian English, no emojis, no hashtags.
8. **Hand off** per Q5. Present the handoff brief and offer to invoke the next skill.

## Guardrails

- Australian English throughout. No hyphens in prose. No emojis. No hashtags.
- Every number is sourced or marked "not available". Confidence tier is always shown.
- Outliers are relative to each creator's own baseline, never raw follower count leaders.
- The skill produces angles and hooks, not fabricated stories or statistics — those come from the user in the downstream interview.
- Reverse engineering means learning the pattern, not copying a competitor's words. Adapted hooks must be original SAS-AM phrasing.

## Reference Files

- **`references/dataSources.md`** — the reliable versus aspirational sourcing tiers, the per platform picture, the MCP discovery step, and the ToS honesty rules.
- **`references/outlierMethod.md`** — baseline computation, the outlier threshold, the weighting of comments over reactions, small sample handling, and worked examples.
- **`references/outputTemplates.md`** — the ranked trend report layout, the hook/format template layout, and the handoff brief block.
