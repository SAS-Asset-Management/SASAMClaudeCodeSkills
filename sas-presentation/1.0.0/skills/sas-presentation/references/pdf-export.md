# Headless Chromium PDF Export

Turn a fixed-stage deck into a clean, one-slide-per-page A-grade PDF with headless Chromium's `--print-to-pdf`. This path works for both the Reveal.js build and the zero dependency single file deck, because both author each slide at a fixed 16:9 canvas.

The whole trick is a hardened `@media print` block that (a) forces exact brand colour, (b) reveals every slide, (c) un-fades the entrance stagger and forces bar/chart fills to full, (d) hides furniture, and (e) turns any panel that is normally tinted into **white with a border** — never a grey fill. Grey boxes and shadow halos are the two recurring PDF defects; the guardrails below kill both unconditionally.

## The command

```bash
# 1920×1080 landscape, one slide per page, backgrounds preserved
chrome --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="deck.pdf" "presentation.html"
```

Notes:
- On macOS use the full binary path: `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"`. `chromium` / `google-chrome` also work.
- Older Chrome builds use `--print-to-pdf-no-header` instead of `--no-pdf-header-footer`.
- Page size comes from the CSS `@page` rule, not a CLI flag — see below.
- `npx decktape reveal presentation.html deck.pdf` remains an alternative for Reveal decks, but `--print-to-pdf` with the guardrail CSS gives the most faithful brand colour.

## Guardrail CSS — include in every deck

```css
/* === PDF EXPORT (headless Chromium --print-to-pdf) ===
   Force exact colour (no washed brand), kill shadows and grey-box artefacts,
   one 16:9 slide per page, reveal every slide. */
@page{ size:1920px 1080px; margin:0; }
@media print{
  html,body{width:1920px;height:auto;overflow:visible;background:#fff;}
  *{ -webkit-print-color-adjust:exact !important; print-color-adjust:exact !important;
     box-shadow:none !important; text-shadow:none !important; }
  .deck-viewport{position:static;overflow:visible;background:#fff;}
  .deck-stage{position:static;width:auto;height:auto;transform:none !important;background:none;}
  .slide{position:relative;visibility:visible !important;opacity:1 !important;pointer-events:auto !important;
    width:1920px;height:1080px;break-after:page;page-break-after:always;transform:none !important;}
  .slide:last-child{break-after:auto;page-break-after:auto;}
  .slide .stagger>*{opacity:1 !important;transform:none !important;}  /* no half-faded reveals in PDF */
  .bar .fill{height:var(--h) !important;}                             /* bars drawn, not zero-height */
  .navrail,.deck-controls{display:none !important;}                   /* furniture off in PDF */
  /* Any normally-tinted panel becomes white-with-border — never a grey fill */
  .kpi,.card,.panel{background:#fff !important;border:1.5px solid #d7e0e8 !important;}
  .kpi{border-top:7px solid #69BE28 !important;}
}
```

## The grey-box / shadow guardrails, itemised

| Guardrail | Why |
|-----------|-----|
| `print-color-adjust:exact` | Without it Chromium strips background colours/gradients to save ink — navy slides print white, green marks vanish. |
| `box-shadow:none` + `text-shadow:none` | Shadows render as grey halos/smears in PDF. SAS decks are flat anyway — enforce it. |
| Reveal every slide (`opacity/visibility !important`) | Only the active slide is visible on screen; print must show all. |
| Un-fade stagger (`.stagger>*{opacity:1}`) | Otherwise slides you never advanced to export half-faded. |
| Force bar/chart fills (`.bar .fill{height:var(--h)}`) | CSS-animated bars sit at height:0 until activated; print them at full value. |
| Panels → white + border | Tinted/grey panel fills band and muddy under print. White with a hairline border reads crisp. Never ship grey fills to PDF. |
| Hide `.navrail` / `.deck-controls` | On-screen furniture is noise in a printed page. |

## Verify the PDF (part of the RENDER VERIFY GATE)

After exporting, open the PDF (or screenshot a page) and check specifically for:
- **No grey boxes** — every panel is white with a border or a genuine brand fill, not a flat grey rectangle.
- **No shadow halos** around cards, tiles, or text.
- Brand colour intact — navy backgrounds are navy, green marks are green (not washed to pale).
- Every slide present, one per page, bars/charts drawn at full value, no half-faded content.
- Nav rail and on-screen controls absent.

If any grey box or shadow survives, the culprit is almost always a panel whose tint was not overridden — add it to the white-with-border rule and re-export.
