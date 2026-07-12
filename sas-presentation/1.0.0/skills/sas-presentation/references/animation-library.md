# Animation Library — Effect to Feeling

Match motion to the intended feeling. Every snippet is rebranded to SAS Blue `#002244` and SAS Green `#69BE28`, is flat design safe (no `box-shadow` — atmosphere comes from gradients, borders, and background contrast), theme aware via CSS variables, and respects `prefers-reduced-motion`.

Motion is subtraction by default. One well orchestrated slide load with staggered reveals beats scattered micro interactions. Reveal.js fragments remain the tool for step by step builds; these snippets are for entrance polish and atmosphere.

---

## Effect to Feeling Guide

| Feeling | Motion | Brand visual cues (flat, no shadow) |
|---------|--------|-------------------------------------|
| **Authoritative / Executive** | Fast subtle fades (200–300ms), no bounce | Navy `#002244` ground, generous negative space, one green accent rule, precise alignment |
| **Data / Evidence** | Bars/lines draw in (600–900ms), numbers count up | White or off white ground, green data marks, thin navy gridlines |
| **Dramatic / Cinematic** | Slow fade + scale (0.94 → 1, 1–1.4s) | Dark navy full bleed, single green focal element, wide letter spacing |
| **Techy / Systems** | Grid reveal, radial halo (gradient, not shadow), draw-on SVG paths | Navy grid pattern, green nodes, Source Code Pro accents |
| **Editorial / Narrative** | Staggered text reveals, image and text interplay | Strong type hierarchy, green pull rule, asymmetric split |
| **Calm / Reflective (breather)** | Very slow gentle fade only | Pure navy, one line of text, no decoration |

Pick ONE feeling per deck and hold it. Mixing three feelings across a deck is the fastest route to the generic "AI slop" look the quality directives warn against.

---

## Brand Tokens Used Below

```css
:root {
  --sas-blue: #002244;
  --sas-green: #69BE28;
  --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
}
```

## Entrance Animations

```css
/* Fade + slide up — the versatile default */
.reveal-up { opacity: 0; transform: translateY(30px);
  transition: opacity .6s var(--ease-out-expo), transform .6s var(--ease-out-expo); }
.visible .reveal-up, .slide.active .reveal-up { opacity: 1; transform: translateY(0); }

/* Scale in — for hero numbers and title marks */
.reveal-scale { opacity: 0; transform: scale(.94);
  transition: opacity .6s, transform .6s var(--ease-out-expo); }
.visible .reveal-scale, .slide.active .reveal-scale { opacity: 1; transform: scale(1); }

/* Blur in — cinematic settle */
.reveal-blur { opacity: 0; filter: blur(10px);
  transition: opacity .8s, filter .8s var(--ease-out-expo); }
.visible .reveal-blur, .slide.active .reveal-blur { opacity: 1; filter: blur(0); }

/* Staggered children — one load, many marks. Set delays inline or with :nth-child */
.stagger > * { opacity: 0; transform: translateY(20px);
  transition: opacity .5s var(--ease-out-expo), transform .5s var(--ease-out-expo); }
.slide.active .stagger > * { opacity: 1; transform: translateY(0); }
.slide.active .stagger > *:nth-child(1) { transition-delay: .05s; }
.slide.active .stagger > *:nth-child(2) { transition-delay: .15s; }
.slide.active .stagger > *:nth-child(3) { transition-delay: .25s; }
```

## Atmospheric Backgrounds (flat safe — no box-shadow)

```css
/* Brand gradient mesh — depth without a flat dead fill. Navy + green, low alpha */
.bg-mesh {
  background:
    radial-gradient(ellipse at 18% 82%, rgba(105,190,40,0.10) 0%, transparent 52%),
    radial-gradient(ellipse at 82% 12%, rgba(0,34,68,0.14) 0%, transparent 55%),
    var(--bg-primary);
}

/* Green focal halo — replaces neon glow the flat safe way (gradient, not box-shadow) */
.focal-halo { position: relative; }
.focal-halo::before {
  content: ""; position: absolute; inset: -18%; z-index: -1;
  background: radial-gradient(circle, rgba(105,190,40,0.22) 0%, transparent 70%);
}

/* Navy structural grid — techy/systems feeling */
.bg-grid {
  background-image:
    linear-gradient(rgba(0,34,68,0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,34,68,0.05) 1px, transparent 1px);
  background-size: 56px 56px;
}
:root[data-theme="dark"] .bg-grid {
  background-image:
    linear-gradient(rgba(255,255,255,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.04) 1px, transparent 1px);
}
```

## Data Motion

```css
/* Draw-on bar (grows from baseline on slide activate) */
.chart-bar-anim { transform: scaleY(0); transform-origin: bottom; transition: transform .8s var(--ease-out-expo); }
.slide.active .chart-bar-anim { transform: scaleY(1); }
```

```svg
<!-- Draw-on line: animate stroke-dashoffset to 0 -->
<path d="M0,180 L120,120 L240,140 L360,60" fill="none"
      stroke="#69BE28" stroke-width="4"
      stroke-dasharray="600" stroke-dashoffset="600">
  <animate attributeName="stroke-dashoffset" from="600" to="0" dur="1s" fill="freeze"/>
</path>
```

```javascript
/* Count-up for a stat number. Honour reduced motion by snapping to the final value. */
function countUp(el, to, dur = 1000, prefix = '', suffix = '') {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) { el.textContent = prefix + to + suffix; return; }
  const start = performance.now();
  (function tick(now) {
    const p = Math.min((now - start) / dur, 1);
    el.textContent = prefix + Math.round(to * (0.5 - Math.cos(Math.PI * p) / 2)) + suffix;
    if (p < 1) requestAnimationFrame(tick);
  })(start);
}
```

## Reduced Motion (mandatory in every deck)

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: .01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: .01ms !important;
    scroll-behavior: auto !important;
  }
}
```

## What to avoid

- Bounce / spring easing on an executive or evidence deck — reads as unserious.
- Motion on more than a couple of elements per slide. Stagger a group, do not animate everything.
- Any `box-shadow` based glow. SAS decks are flat; use the radial gradient halo above.
- Looping attention grabbers behind text (fast binary rain, spinning marks) — they subtract attention. Keep the existing binary background at its documented low alpha or omit it.
