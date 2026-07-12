# Right-Side Navigation Rail

A very subtle vertical progress rail pinned to the right edge. It shows the audience **where we are** and **where we are going** — section labels with nodes: the current section green and labelled, past sections filled and dimmed, upcoming sections faint hollow rings. It is quiet by design (low opacity, only the current label fully shown) so it never competes with the slide.

Light/dark aware. Furniture only — it carries `aria-hidden="true"` and is hidden entirely in PDF export. Optional but recommended for decks of 5+ sections; skip it on 1–3 slide one-pagers.

## CSS

```css
/* === SUBTLE RIGHT-SIDE NAVIGATION RAIL — where we are + where we're going === */
.navrail{position:absolute;top:0;right:0;height:1080px;width:300px;pointer-events:none;z-index:5;
  display:flex;flex-direction:column;justify-content:center;gap:34px;padding-right:56px;align-items:flex-end;}
.navrail .seg{display:flex;align-items:center;gap:18px;opacity:.30;
  transition:opacity .5s var(--ease),transform .5s var(--ease);transform:translateX(6px);}
.navrail .seg .lab{font-size:20px;font-weight:700;letter-spacing:.5px;color:var(--muted);white-space:nowrap;
  opacity:0;transform:translateX(10px);transition:opacity .5s var(--ease),transform .5s var(--ease);}
.navrail .seg .node{width:11px;height:11px;border-radius:50%;background:transparent;
  border:2px solid var(--muted);flex:0 0 auto;transition:all .5s var(--ease);}
.navrail .seg.done{opacity:.5;}                                   /* past: filled + dimmed */
.navrail .seg.done .node{background:var(--muted);border-color:var(--muted);}
.navrail .seg.current{opacity:1;transform:translateX(0);}          /* now: green + labelled */
.navrail .seg.current .node{background:var(--sas-green);border-color:var(--sas-green);width:14px;height:14px;}
.navrail .seg.current .lab{opacity:1;transform:translateX(0);color:var(--sas-green);font-weight:900;}
/* On navy / dark slides the rail text + nodes go light */
.navy .navrail .seg .lab,.bg-grid-navy .navrail .seg .lab,
:root[data-theme="dark"] .navrail .seg .lab{color:#9fb3c7;}
.navy .navrail .seg .node,.bg-grid-navy .navrail .seg .node,
:root[data-theme="dark"] .navrail .seg .node{border-color:#7f97ad;}
.navy .navrail .seg.done .node,.bg-grid-navy .navrail .seg.done .node,
:root[data-theme="dark"] .navrail .seg.done .node{background:#7f97ad;}
.navy .navrail .seg.current .lab,.bg-grid-navy .navrail .seg.current .lab,
:root[data-theme="dark"] .navrail .seg.current .lab{color:var(--sas-green);}
```

Upcoming sections need no extra class — the base `.seg` (faint, hollow node, hidden label) is the upcoming state.

## Markup — one `.seg` per section, in order

```html
<nav class="navrail" id="navrail" aria-hidden="true">
  <div class="seg" data-i="0"><span class="lab">Overview</span><span class="node"></span></div>
  <div class="seg" data-i="1"><span class="lab">The Problem</span><span class="node"></span></div>
  <div class="seg" data-i="2"><span class="lab">Outcomes</span><span class="node"></span></div>
  <div class="seg" data-i="3"><span class="lab">Where the Risk Is</span><span class="node"></span></div>
  <div class="seg" data-i="4"><span class="lab">Approach</span><span class="node"></span></div>
  <div class="seg" data-i="5"><span class="lab">Next Steps</span><span class="node"></span></div>
</nav>
```

Keep labels to 1–3 words. Map one `.seg` per slide (or per section — if several slides share a `data-section`, map the rail to sections and advance the current node when the section changes).

## JS wiring

In the deck's `show(n)` slide switcher, toggle `current` / `done` on the segments:

```javascript
const segs = [...document.querySelectorAll('.navrail .seg')];
function updateRail(i){
  segs.forEach((s,k)=>{ s.classList.toggle('current', k===i); s.classList.toggle('done', k<i); });
}
// call updateRail(i) inside show(n), alongside the slide .active toggle
```

## Right gutter for wide content (MANDATORY when the rail is present)

The rail lives in a 300px column pinned to the right edge. Any **edge-to-edge wide content** — KPI rows, bar charts, column grids, resource card rows — must reserve a right gutter so it never slides under or crowds the rail. Reserve ~172px:

```css
/* keep wide content clear of the right nav rail */
.kpis, .bars, .cols, .resrow { margin-right: 172px; }
```

Add any other full-width block class you introduce to this rule. Narrow content (headings, single statements, question text, stat blocks) does not need the gutter — only content that would otherwise run to the right edge. If a deck has no nav rail, the gutter is optional.

## Reveal.js note

The reference implementation is the zero dependency single file deck (see `references/rendering-modes.md`), where `show(n)` already exists. In a Reveal.js deck, drive the rail from the `slidechanged` event instead: `Reveal.on('slidechanged', e => updateRail(e.indexh))`. The existing footer section nav still applies; the rail complements it, it does not replace it.

## PDF / print

The rail is presentation furniture. The PDF export block hides it: `.navrail{display:none !important;}` (see `references/pdf-export.md`).
