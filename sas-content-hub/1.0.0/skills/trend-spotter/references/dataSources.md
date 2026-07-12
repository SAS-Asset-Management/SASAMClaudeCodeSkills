# Trend Spotter — Data Sourcing

The most important honesty rule in this skill: **report only what you can actually source, and always show which tier it came from.** A trend tool that fabricates engagement numbers is worse than useless — it produces confident, wrong strategy. Read this file before every run.

## Discovery step (run first, every time)

Native connectors change over time. At the start of a scan, run a `ToolSearch` for each platform and for analytics:

```
ToolSearch "youtube data api videos search"
ToolSearch "reddit posts subreddit search"
ToolSearch "linkedin posts api"
ToolSearch "x twitter posts search"
ToolSearch "website analytics search console ga4"
```

If a native MCP connector is now present, prefer it and say so in the report. If not, fall back to the reliable tier below and flag the gap.

## Tier 1 — Reliable today

| Source | What it gives | Notes |
| --- | --- | --- |
| **SAS-AM website-analytics stack** (GA4, Search Console, Microsoft Clarity on Cortex4) | Ground truth for OUR owned properties — traffic, referrals from social, SERP position, on page behaviour | Own domain only. Use the `website-analytics` skill. This is how a trend translates into measured SAS-AM outcomes, not how you measure a competitor. |
| **socialContentEngine `linkedin-post-analyser`** (local skill, `performance.db` + `postClassifications.json`) | SAS-AM's own LinkedIn post performance — top performers, format breakdown, hook archetypes, per post deep dive | This is OUR baseline. Use it to compare "what's trending out there" against "what already works for us". |
| **`WebSearch` / `WebFetch`** | Public, openly indexed posts, articles, YouTube video pages, Reddit threads, creator blogs | Reliable for CONTENT (the hook, the topic, the format). Usually NOT reliable for exact engagement counts on third party social posts. |
| **`claude-in-chrome`** browser automation | Reading a feed the USER is already logged into (their LinkedIn / YouTube / X / Reddit session) | Session based and user driven. Still ToS sensitive. Surface what you are about to read, let the user drive login, never store credentials, never automate mass extraction. |

## Tier 2 — Aspirational / gated (name it, do not pretend)

| Source | Status | To enable |
| --- | --- | --- |
| LinkedIn API | Not connected as MCP here. LinkedIn's API does not expose competitor post analytics anyway — only your own authorised org/page. | Would only ever surface OUR own page metrics, and only after OAuth. |
| YouTube Data API | Not connected. Would give reliable public view/like/comment counts and publish dates for any channel. | Add via the MCP_DOCKER `mcp-add` flow and consent an API key before use. |
| Reddit API | Not connected. Would give reliable score, comment count, and upvote ratio per post. | Same — add + consent before it can supply numbers. |
| X API | Not connected. Paid tiers gate most useful post metrics. | Same — add + consent; note the cost gate. |

## Per platform reality

- **LinkedIn (primary).** No open API for third party post analytics. Reactions, comment counts and reposts are usually VISIBLE on the post itself (readable via WebFetch of a public post URL or via the user's logged in session). View counts are generally NOT exposed on other people's posts — do not invent them. Rank LinkedIn outliers on comments and reposts, and mark the metric basis.
- **YouTube.** The most measurable platform even without the API — view, like and comment counts are public on the watch page. WebFetch/WebSearch can read them; the Data API is cleaner if connected.
- **Reddit.** Score and comment count are public per thread. Good for topic level demand signal in r/AssetManagement, r/reliability, r/maintenance, r/engineering and similar.
- **X.** Least reliable without the paid API. Treat any X figure as low confidence unless the API is connected.

## Confidence tiers (tag every metric)

- **High** — from a native API or the user's own logged in read of an exact on platform count.
- **Medium** — an exact count read from a public page (e.g. YouTube view count, a visible LinkedIn comment count).
- **Low** — inferred, partial, or platform estimated signal; small sample. Always disclose and prefer not to rank on it alone.

## ToS and privacy rules

- Prefer official and MCP data. Prefer the user's own session over anonymous scraping.
- Never bulk scrape, never bypass rate limits, never defeat bot detection.
- Do not compile personal data on individuals beyond what a public professional post shows.
- If the only way to get a number would break a platform's terms, do not get it — report the metric as "not available" and rank on what is permissible.
