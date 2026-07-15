# Rendering Modes — Fixed Stage & Zero Dependency Export

> **v2 update:** the **default engine is now `deck-stage`** (see `deckStageRecipes.md`) — a standalone 1920×1080 fixed-stage web component with an icon rail, count-ups, a presenter camera cameo, and native one-page-per-slide print. The Reveal.js material below is retained as the **legacy** path (existing decks and the print-first case-study / A4 / proposal templates). Both engines share the fixed-stage discipline described here.

Two ways to render a SAS-AM deck. Reveal.js is the legacy engine. Zero dependency (now the deck-stage single-file variant) is for offline, air gapped, or CDN blocked delivery. Both obey the same fixed stage discipline.

marcov-revealjs-standards v1.0.0 compliance is preserved in both modes: brand colours (SAS Blue `#002244`, SAS Green `#69BE28`), flat design (no box shadows), light/dark theming via CSS variables, WCAG 2.1 AA, and the presentation philosophy rules all still apply.

---

## The Fixed Stage Principle

Every deck is authored at ONE canvas size and the whole canvas is scaled uniformly to the viewport. Content is never reflowed per device. On a narrow screen the stage letterboxes (bars top and bottom) or pillarboxes (bars left and right) rather than rearranging slide content. This is what guarantees a slide looks identical on a boardroom projector and a phone.

| Mode | Canvas | Scaling mechanism |
|------|--------|-------------------|
| **Reveal.js (default)** | 1760 × 990 | Reveal's own transform scaler (`width`/`height`/`minScale`/`maxScale` in the config). Already a fixed stage — do not fight it with your own responsive slide rules. |
| **Zero dependency** | 1920 × 1080 | The `deckScale()` function below sets `transform: scale()` on `.deck-stage`. |

### The "never use display:none to switch slides" rule (BOTH MODES)

Slide visibility is controlled by the framework (Reveal) or by an `.active` / `.visible` class toggling `visibility`, `opacity`, and `pointer-events`. **Never** switch whole slides with `display:none` / `display:block`.

Why: a later layout rule such as `.slide-content { display: flex; }` will override a `display:none` and make every slide visible at once. `visibility`/`opacity` cannot be clobbered this way.

> This rule targets whole slide (`<section>`) switching only. The existing dual theme image swap (`.logo-light` / `.logo-dark` using `display`) is unaffected — that toggles images inside a slide, not the slide itself.

---

## Zero Dependency Single File Mode

A single self contained `.html` file. All CSS and JS inline. No Reveal.js, no Font Awesome, no CDN. Fonts fall back to a high quality system stack (see note). The file opens anywhere, including offline and inside a locked down client environment.

**When to offer it:** the user says the deck must work offline, on an air gapped machine, on a client site that blocks external CDNs, or "just send me one file that always works". Otherwise the Reveal.js build stays the default because it gives fragments, speaker view, hash routing, and the full plugin set.

**What you lose vs Reveal.js:** speaker/presenter view (press S), fragment step animations, hash deep links, the Notes plugin. Speaker notes still travel in the file as HTML comments or a hidden `<aside>` for the record.

### Fixed stage base CSS (include in full)

```css
/* === FIXED 16:9 STAGE — MANDATORY FOR ZERO DEPENDENCY MODE === */
html, body {
  width: 100%; height: 100%; margin: 0;
  overflow: hidden;
  background: var(--stage-bg, #002244); /* SAS Blue letterbox bars */
}
.deck-viewport { position: fixed; inset: 0; overflow: hidden; background: var(--stage-bg, #002244); }
/* JS sets transform: translate(...) scale(...) on .deck-stage */
.deck-stage {
  position: absolute; left: 0; top: 0;
  width: 1920px; height: 1080px;
  overflow: hidden; transform-origin: 0 0;
  background: var(--slide-bg, #ffffff);
}
.slide {
  position: absolute; inset: 0;
  width: 1920px; height: 1080px;
  overflow: hidden;
  visibility: hidden; opacity: 0; pointer-events: none;
  background: var(--slide-bg, #ffffff);
  transition: opacity .4s ease;
}
.slide.active { visibility: visible; opacity: 1; pointer-events: auto; z-index: 1; }
img, video, canvas, svg { max-width: 100%; max-height: 100%; }
.deck-controls { position: fixed; left: 50%; bottom: 22px; transform: translateX(-50%); z-index: 1000; }

/* Reduced motion (mandatory) */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: .01ms !important; transition-duration: .01ms !important; }
}

/* Print one fixed size slide per page */
@media print {
  html, body { width: 1920px; height: auto; overflow: visible; background: #fff; }
  .deck-viewport { position: static; overflow: visible; background: #fff; }
  .deck-stage { position: static; width: auto; height: auto; transform: none !important; background: none; }
  .slide {
    position: relative; visibility: visible !important; opacity: 1 !important; pointer-events: auto !important;
    width: 1920px; height: 1080px; break-after: page; page-break-after: always;
  }
  .slide:last-child { break-after: auto; page-break-after: auto; }
  .deck-controls { display: none !important; }
  * { box-shadow: none !important; } /* flat design — no shadow halos in PDF */
}
```

### Vanilla stage scaler + slide switcher (inline before `</body>`)

```javascript
/* === FIXED STAGE SCALER — letterbox/pillarbox, never reflow === */
const stage = document.querySelector('.deck-stage');
const DESIGN_W = 1920, DESIGN_H = 1080;
function deckScale() {
  const scale = Math.min(window.innerWidth / DESIGN_W, window.innerHeight / DESIGN_H);
  const x = (window.innerWidth  - DESIGN_W * scale) / 2;
  const y = (window.innerHeight - DESIGN_H * scale) / 2;
  stage.style.transform = `translate(${x}px, ${y}px) scale(${scale})`;
}
window.addEventListener('resize', deckScale);
deckScale();

/* === SLIDE SWITCHER — .active only, never display:none === */
const slides = [...document.querySelectorAll('.slide')];
let i = 0;
function show(n) {
  i = Math.max(0, Math.min(slides.length - 1, n));
  slides.forEach((s, k) => s.classList.toggle('active', k === i));
  location.hash = 'slide-' + (i + 1);
}
document.addEventListener('keydown', (e) => {
  if (['ArrowRight', 'ArrowDown', ' ', 'PageDown'].includes(e.key)) { e.preventDefault(); show(i + 1); }
  if (['ArrowLeft', 'ArrowUp', 'PageUp'].includes(e.key)) { e.preventDefault(); show(i - 1); }
  if (e.key === 'Home') show(0);
  if (e.key === 'End') show(slides.length - 1);
});
/* Touch swipe */
let tx = 0;
addEventListener('touchstart', e => tx = e.touches[0].clientX, { passive: true });
addEventListener('touchend', e => {
  const dx = e.changedTouches[0].clientX - tx;
  if (Math.abs(dx) > 50) show(i + (dx < 0 ? 1 : -1));
}, { passive: true });
/* Deep link on load */
const m = location.hash.match(/slide-(\d+)/);
show(m ? (+m[1] - 1) : 0);
```

### Document shell

Same marcov head requirements as the Reveal build (`<!DOCTYPE html>`, `lang="en-AU"`, `data-theme="light"`, charset, viewport, description + author meta, `| marcov` title). Body:

```html
<body>
  <div class="deck-viewport">
    <div class="deck-stage">
      <section class="slide active" id="slide-1" data-section="title"> ... </section>
      <section class="slide" id="slide-2" data-section="situation"> ... </section>
      <!-- more slides -->
    </div>
  </div>
  <nav class="deck-controls" aria-label="Slide navigation"> ... </nav>
  <script> /* scaler + switcher from above */ </script>
</body>
```

**Fonts:** the Reveal build uses Google Fonts (Source Sans Pro / Source Code Pro). For a truly offline file, either (a) keep the Google Fonts `<link>` and accept it degrades gracefully to the fallback stack when offline, or (b) inline the fonts as base64 `@font-face` if the user needs pixel identical type with no network at all. Default fallback stack: `'Source Sans Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`.

**Theme + brand:** reuse the exact `:root[data-theme="light"]` / `[data-theme="dark"]` colour blocks from `base-styles.css` (or the Colour System section of `SKILL.md`). Inline them in the `<style>` block. Brand, flat design, and contrast rules are identical to the Reveal build.

### Render verify

Run the full RENDER VERIFY GATE (multi viewport + panel overlap) from `SKILL.md`. The zero dependency file is not exempt — screenshot it at 1280×720 and one phone viewport before handing it over.
