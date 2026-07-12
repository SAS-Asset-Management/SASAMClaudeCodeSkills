# Resources Showcase — Cite Our Own Content

Decks should point the audience back to SAS-AM's published thinking. During the build, search the website's `/resources` section (the Webflow blog + case-study CMS at `sas-am.com/resources`) for pages relevant to the deck's **subject and sector**, then showcase the two to four best matches — as a "Further reading" slide, or as resource callouts on related content slides.

This turns a deck into a funnel: the audience leaves with named articles and URLs they can read next, and the deck demonstrates depth without cramming it onto slides.

## When to do it

- Any deck with a subject and sector (which is almost all of them). Do it in Phase 3 of discovery, after the type and subject are known, before building the closing/CTA.
- Skip only for internal-only decks (meeting minutes, project status) where external reading would be noise — or when a search genuinely returns nothing relevant (say so, do not invent resources).

## How to search — tool options, in order of preference

1. **Webflow MCP CMS tools (preferred when connected).** The `/resources` content lives in a Webflow CMS collection. Use the Webflow MCP to list and read it:
   - `collections_list` on the SAS-AM site to find the Resources / blog / case-study collection(s).
   - `collections_items_list_items` to pull item titles, slugs, categories/sector fields, and summaries.
   - Filter items whose title, category, sector, or summary matches the deck subject/sector.
   - Build each URL as `https://www.sas-am.com/resources/<slug>` (confirm the live path pattern from the item's fields; case studies may sit under a different folder).
   - Site and Resources-collection IDs are recorded in the operator's memory note `reference_webflow_site.md` — use them to target the right collection directly.
2. **WebFetch (no MCP needed).** Fetch `https://www.sas-am.com/resources` and read the listing; follow into candidate articles to confirm relevance and capture the exact title + URL.
3. **WebSearch (discovery / fallback).** Query `site:sas-am.com/resources <subject/sector keywords>` to surface indexed pages, then WebFetch each hit to confirm.

Prefer the MCP when available (structured, current, includes drafts/fields); fall back to WebFetch/WebSearch otherwise. Always confirm the **live URL resolves** before putting it on a slide — never show a guessed or 404 link.

## Matching heuristic

Rank candidates by, in order: exact sector match (Water, Transport, Local Government, Resources & Minerals, Health, Defence) → subject/topic match (the deck's one-sentence theme) → recency → format fit (a case study for a BD deck, a explainer article for a teaching deck). Keep 2–4. More than four reads as a link dump.

## Slide: "Further reading" (recommended pattern)

A light slide, navy logo top-left, 2–4 resource cards. Title + one-line descriptor + visible URL. White cards with a green cap and hairline border (flat, PDF-safe — same rule as KPI tiles).

```html
<section id="resources" class="slide bg-mesh" data-section="recommendation">
  <img class="logo logo-tl" alt="SAS Asset Management" src="[NAVY_LOGO_URI]">
  <div style="margin-top:34px;">
    <p class="kicker">Further reading</p>
    <h2>More from SAS-AM on this</h2>
  </div>
  <div class="reslist stagger">
    <a class="rescard" href="https://www.sas-am.com/resources/condition-led-maintenance" target="_blank" rel="noopener">
      <span class="restype">Article</span>
      <span class="restitle">Condition-led maintenance in water utilities</span>
      <span class="resurl">sas-am.com/resources/condition-led-maintenance</span>
    </a>
    <a class="rescard" href="https://www.sas-am.com/resources/rail-reliability-case-study" target="_blank" rel="noopener">
      <span class="restype">Case study</span>
      <span class="restitle">Cutting unplanned rail downtime 37%</span>
      <span class="resurl">sas-am.com/resources/rail-reliability-case-study</span>
    </a>
  </div>
  <aside class="notes">
    Point them to the two most relevant reads. Offer to send the links after.
    Timing: ~30 seconds — this is a leave-behind slide, not a talking point.
  </aside>
</section>
```

```css
.reslist{display:grid;grid-template-columns:repeat(2,1fr);gap:40px;margin-top:30px;}
.rescard{display:flex;flex-direction:column;gap:12px;text-decoration:none;
  background:#fff;border:1.5px solid var(--line);border-left:7px solid var(--sas-green);
  border-radius:14px;padding:40px 44px;}
.rescard .restype{font-family:'Source Code Pro',monospace;font-size:20px;color:var(--sas-green);font-weight:600;letter-spacing:1px;text-transform:uppercase;}
.rescard .restitle{font-size:34px;font-weight:900;color:var(--ink);line-height:1.2;}
.rescard .resurl{font-size:22px;color:var(--muted);font-weight:700;}
```

## Alternative: inline resource callout

On a content slide that discusses a topic we have written about, add a small callout instead of a whole slide:

```html
<p class="rescallout">Read more · <a href="https://www.sas-am.com/resources/<slug>">Condition-led maintenance</a></p>
```
```css
.rescallout{font-size:22px;color:var(--muted);font-weight:700;margin-top:22px;}
.rescallout a{color:var(--sas-green);text-decoration:none;font-weight:900;}
```

## Honesty rules

- Only cite pages that exist and resolve. Confirm each URL before it goes on a slide.
- Do not fabricate titles, slugs, or metrics from a resource — quote the real title.
- If nothing on `/resources` fits the subject, omit the showcase and tell the user ("no directly relevant /resources pages found") rather than padding with loosely related links.
- The showcase is brand-safe and flat (white cards, green cap, hairline border, no shadow); it exports cleanly to PDF under the same white-with-border rule.
