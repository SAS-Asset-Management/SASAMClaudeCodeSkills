# Resources Showcase — Cite Our Own Content

Decks should point the audience back to SAS-AM's published thinking. During the build, search the website's `/resources` section (the Webflow blog + case-study CMS at `sas-am.com/resources`) for pages relevant to the deck's **subject and sector**, then showcase the **two most relevant** on a single slide — each as a **featured card with a hero image and a QR code**.

This turns a deck into a funnel: the audience can scan a QR straight to the article, and the deck demonstrates depth without cramming it onto slides.

## The rule (hard)

- **Maximum TWO resources**, on one slide, side by side. Never more.
- **Both are rendered as hero + QR cards** — a white card with the article's hero image on top, the title below, and a navy QR code (encoding the article URL) overlapping the hero's bottom-right with a "Scan to read" label. **There is no text-list variant** — do not fall back to a list of links.
- If only one strong match exists, show one card. If none fit, omit the slide (see honesty rules).

## When to do it

- Any deck with a subject and sector (almost all). Do it in Phase 3 of discovery, after the type and subject are known, before building the closing/CTA.
- Skip only for internal-only decks (meeting minutes, project status) where external reading would be noise — or when a search genuinely returns nothing relevant (say so, do not invent resources).

## How to search — tool options, in order of preference

1. **Webflow MCP CMS tools (preferred when connected).** The `/resources` content lives in a Webflow CMS collection. Use the Webflow MCP to list and read it:
   - `collections_list` on the SAS-AM site to find the Resources / blog / case-study collection(s).
   - `collections_items_list_items` to pull item titles, slugs, categories/sector fields, summaries, **and the hero image URL** (needed for the card).
   - Filter items whose title, category, sector, or summary matches the deck subject/sector.
   - Build each URL as `https://www.sas-am.com/resources/<slug>` (confirm the live path pattern from the item's fields; case studies may sit under a different folder).
   - Site and Resources-collection IDs are recorded in the operator's memory note `reference_webflow_site.md` — use them to target the right collection directly.
2. **WebFetch (no MCP needed).** Fetch `https://www.sas-am.com/resources` and read the listing; follow into the two candidate articles to confirm relevance and capture the exact title, URL, and hero image URL.
3. **WebSearch (discovery / fallback).** Query `site:sas-am.com/resources <subject/sector keywords>`, then WebFetch each hit to confirm.

Prefer the MCP when available. Always confirm the **live URL resolves** before putting it on a slide — never show a guessed or 404 link.

## Matching heuristic

Rank candidates by, in order: exact sector match (Water, Transport, Local Government, Resources & Minerals, Health, Defence) → subject/topic match (the deck's one-sentence theme) → recency → format fit (a case study for a BD deck, an explainer article for a teaching deck). **Keep the top two.**

## Building each card — assets to prepare

For each of the (at most) two resources you need two base64 assets: the **hero image** and the **QR code**.

### Hero image (fetch + downscale + base64)

```bash
# Fetch the article hero, downscale to card width (~760px is plenty for a 372px-tall card at 2x), base64-embed.
curl -fsSL "<hero-image-url>" -o /tmp/hero.jpg
sips -Z 760 /tmp/hero.jpg --out /tmp/hero_small.jpg >/dev/null   # downscale, keeps aspect
printf 'data:image/jpeg;base64,%s' "$(base64 -i /tmp/hero_small.jpg)" > /tmp/hero.datauri
```
Embed the resulting `data:image/jpeg;base64,...` string as the `.reshero > img` `src`. If the article has no usable hero, fall back to a brand-tinted SVG (navy→green gradient) rather than a grey box.

### QR code (generate locally, navy on white, base64)

Generate the QR **locally** encoding the exact article URL — do not call a remote QR service.

```bash
# Primary: qrencode (SVG, navy foreground, white background, quiet margin 2)
qrencode -t SVG -m 2 --foreground=002244 --background=ffffff -o /tmp/qr.svg "https://www.sas-am.com/resources/<slug>"
printf 'data:image/svg+xml;base64,%s' "$(base64 -i /tmp/qr.svg)" > /tmp/qr.datauri
```

```python
# Fallback: python qrcode (or segno) if qrencode is not installed
import qrcode, base64, io
img = qrcode.make("https://www.sas-am.com/resources/<slug>")   # default black on white
buf = io.BytesIO(); img.save(buf, format="PNG")
print("data:image/png;base64," + base64.b64encode(buf.getvalue()).decode())
# segno equivalent: segno.make(url).save("qr.svg", dark="#002244", light="#ffffff", border=2)
```

The QR foreground is SAS Blue `#002244` on white so it reads as brand, not raw black. Keep the quiet margin (qrencode `-m 2`) or scanners struggle. Embed as the `.resqr > img` `src`.

## The slide (two hero + QR cards)

```html
<section id="resources" class="slide bg-mesh" data-section="recommendation">
  <img class="logo logo-tl logo-light" alt="SAS Asset Management" src="[NAVY_LOGO_URI]">
  <img class="logo logo-tl logo-dark"  alt="SAS Asset Management" src="[WHITE_LOGO_URI]">
  <div style="margin-top:34px;">
    <p class="kicker">Further reading</p>
    <h2>Related from our resource library</h2>
  </div>
  <div class="resrow stagger">
    <div class="rescard">
      <div class="reshero">
        <img src="data:image/jpeg;base64,[HERO_1]" alt="">
        <div class="resqr"><img src="data:image/svg+xml;base64,[QR_1]" alt="QR to article"><span>Scan to read</span></div>
      </div>
      <div class="restitle">12,000 Assets, One Standard: How GeelongPort Connected Condition Data</div>
      <div class="resmeta">Case study · Transport · sas-am.com/resources</div>
    </div>
    <div class="rescard">
      <div class="reshero">
        <img src="data:image/jpeg;base64,[HERO_2]" alt="">
        <div class="resqr"><img src="data:image/svg+xml;base64,[QR_2]" alt="QR to article"><span>Scan to read</span></div>
      </div>
      <div class="restitle">What 3,126 Work Orders Taught Us About Your FMEA</div>
      <div class="resmeta">Article · Predictive Maintenance · sas-am.com/resources</div>
    </div>
  </div>
  <aside class="notes">
    Point them to the two most relevant reads; invite them to scan now or after.
    Timing: ~30 seconds — a leave-behind slide, not a talking point.
  </aside>
</section>
```

## The exact card CSS (from the reference deck)

```css
/* keep the row clear of the right nav rail — see nav-rail.md */
.resrow{display:grid;grid-template-columns:1fr 1fr;gap:88px;margin-top:44px;align-items:start;margin-right:172px;}
.rescard{background:#fff;border:1.5px solid var(--line);border-radius:18px;overflow:visible;}
.reshero{position:relative;height:372px;border-radius:18px 18px 0 0;}
.reshero>img{width:100%;height:372px;object-fit:cover;border-radius:18px 18px 0 0;display:block;}
/* QR overlaps the hero's bottom-right; the title reserves right padding (214px) so text never runs under it */
.resqr{position:absolute;right:24px;bottom:-46px;background:#fff;border:1.5px solid var(--line);
  border-radius:14px;padding:13px 13px 7px;width:170px;text-align:center;}
.resqr img{width:144px;height:144px;display:block;}
.resqr span{font-size:14px;font-weight:900;color:var(--sas-blue);letter-spacing:.6px;display:block;
  margin-top:5px;text-transform:uppercase;}
.restitle{font-size:31px;font-weight:900;color:var(--sas-blue);line-height:1.2;padding:34px 214px 6px 34px;}
.resmeta{font-size:21px;font-weight:800;color:var(--sas-green);padding:0 34px 30px;}
```

Notes:
- The card is white with a hairline border and rounded corners — flat, no shadow. `overflow:visible` is required so the QR can hang below the hero (`bottom:-46px`).
- `.restitle` reserves `214px` of right padding so the title never runs under the overlapping QR.
- `.resmeta` uses the format `Type · Sector · sas-am.com/resources` (green, weight 800).

## PDF export

The cards are already white with a border, so they survive PDF export under the standard guardrails (see `references/pdf-export.md`). Hero images and QR codes are base64-embedded, so they print with `print-color-adjust:exact`. Confirm in the PDF check that both QR codes render sharp (not blurred) and no grey box appears behind a card.

## Honesty rules

- Only cite pages that exist and resolve. Confirm each URL (and generate its QR from that exact URL) before it goes on a slide.
- Do not fabricate titles, slugs, or metrics — quote the real title and category.
- If nothing on `/resources` fits, omit the slide and tell the user ("no directly relevant /resources pages found") rather than padding with a loosely related second card.
