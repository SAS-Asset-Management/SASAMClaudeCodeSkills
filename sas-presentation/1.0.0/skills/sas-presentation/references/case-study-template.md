# Case Study Template (Print-First Pattern)

Purpose-built HTML → PDF case study artefact for client-facing downloads.

**IMPORTANT:** Reveal.js decks are for screen viewing. For downloadable PDF case studies, use this print-first pattern. Do NOT try to export Reveal.js to PDF via Chrome headless — aspect ratio mismatch (1760×990 landscape canvas vs A4 portrait paper) produces shrunk, letterboxed output. Either use `npx decktape reveal …` for deck-based PDFs, or use this template for a true print artefact.

## When to use which

| Artefact | Tool |
|----------|------|
| Screen presentation (BD meeting, webinar) | Reveal.js via `scaffold-template.html` |
| Downloadable PDF case study (website, email attachment) | **This template** (purpose-built print HTML) |
| Interactive web page on sas-am.com/resources | Webflow CMS rich text + Embed blocks |

---

## Page structure (A4 portrait, 8 pages)

1. **Cover** — full-bleed hero + dark navy gradient + SAS SVG top-left + client wordmark top-right + headline + metadata strip
2. **Executive summary** — 4 stat tiles + summary paragraph
3. **The Challenge** — pain points panel + pull quote
4. **The Approach (Phases 1 & 2)** — vertical timeline with numbered nodes
5. **The Approach (Phase 3)** — timeline continues + key differentiator banner
6. **The Outcomes** — before/after comparison grid (3-column: metric | before | after)
7. **Testimonial + Lessons** — quote card + 2×2 lessons grid
8. **Back cover / CTA** — dark navy + hero at 8% opacity + SAS SVG + contact grid + tagline

---

## SVG logo alignment rules (critical)

SVG logos have fixed `viewBox` aspect ratios. Forcing both `width` and `height` will distort them. Always:

```css
/* Width-based sizing, height auto → aspect ratio preserved */
.sas-logo-primary {
  width: 200px;
  height: auto;      /* NEVER set fixed height if width is set */
  max-height: 36px;  /* Safety cap — SAS logo is 371×53, so 200px wide ≈ 28.6px tall */
}
```

**SAS primary logo SVG** (Webflow CDN): `https://s3.amazonaws.com/webflow-prod-assets/653497186047abfdf821b2fc/65349e886047abfdf8265bde_SAS-Logo-RGB-Colour-PrimaryAlt-Med%201.svg`

- viewBox: `0 0 371 53` (≈7:1 horizontal lockup)
- Has hard-coded `#002244` and `#69BE28` fills
- To render white on dark backgrounds: `filter: brightness(0) invert(1);`

**Client wordmark pattern (GeelongPort example):**

- Strip any decorative background shapes from the source SVG — keep wordmark only
- Set all paths to `fill="currentColor"` — lets CSS `color:` drive the tint
- Inline the SVG in HTML (not via `<img src>`) so `currentColor` actually cascades
- Tint for context: `color: #ffffff` on navy, `color: var(--sas-blue)` on light

**Anti-pattern — remove:**
- `background: white` wrappers around client logos (the "BG" the client didn't want)
- `background: rgba(255,255,255,0.08)` translucent boxes
- Setting both `width` and `height` attributes on an SVG element

---

## CSS variable palette

```css
:root {
  --sas-blue: #002244;
  --sas-green: #69BE28;
  --green-accent: #69BE28;
  --navy-deep: #001630;

  --white: #ffffff;
  --off-white: #fafbfc;
  --bg-grey: #f5f7fa;
  --bg-secondary: #f7fafc;

  --text-primary: #002244;
  --text-secondary: #2d3748;
  --text-muted: #718096;
  --border: #e2e8f0;

  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 14px;

  --shadow-sm: 0 2px 8px rgba(0, 34, 68, 0.08);
  --shadow-md: 0 4px 16px rgba(0, 34, 68, 0.12);
}
```

---

## Print CSS foundation

```css
@page {
  size: A4 portrait;
  margin: 0;
}

@page :first { margin: 0; }

html, body {
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
  margin: 0;
  padding: 0;
  font-family: 'Inter', system-ui, sans-serif;
  color: var(--text-secondary);
  background: var(--white);
}

.page {
  page-break-after: always;
  break-after: page;
  page-break-inside: avoid;
  width: 210mm;
  height: 297mm;
  position: relative;
  overflow: hidden;
}

.page:last-child { page-break-after: auto; }

/* Running header from page 2 onwards */
.doc-header {
  position: absolute;
  top: 6mm;
  left: 12mm;
  right: 12mm;
  display: flex;
  justify-content: space-between;
  font-size: 7pt;
  color: var(--text-muted);
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.page-num {
  position: absolute;
  bottom: 8mm;
  right: 16mm;
  font-size: 8pt;
  color: var(--text-muted);
}

/* Avoid orphan headings */
h1, h2, h3, h4 { page-break-after: avoid; break-after: avoid-page; }

/* Hide screen-only elements in print */
@media print { .no-print { display: none !important; } }
```

---

## Key component blueprints

### Cover (page 1)

```html
<section class="page page-cover">
  <div class="cover-hero" style="background-image:url('hero.jpg')"></div>
  <div class="cover-gradient"></div>

  <div class="cover-topbar">
    <!-- SAS primary SVG — inverted white on navy -->
    <img src="sas-primary.svg" alt="SAS Asset Management" class="cover-sas-logo">
    <!-- Client wordmark — inline SVG with currentColor, tinted white -->
    <div class="cover-client-logo">
      <svg viewBox="0 0 200 30" xmlns="http://www.w3.org/2000/svg">
        <g fill="currentColor"><!-- paths --></g>
      </svg>
    </div>
  </div>

  <div class="cover-text-block">
    <div class="cover-eyebrow">Case Study</div>
    <h1 class="cover-headline">Headline,<br>Two Lines</h1>
    <p class="cover-subhead">Subhead extending the headline with a specific insight.</p>
  </div>

  <div class="cover-strip" role="table">
    <div class="strip-item"><div class="strip-label">Client</div><div class="strip-value">Name</div></div>
    <div class="strip-item"><div class="strip-label">Sector</div><div class="strip-value">Industry</div></div>
    <div class="strip-item"><div class="strip-label">Duration</div><div class="strip-value">X months</div></div>
    <div class="strip-item"><div class="strip-label">Services</div><div class="strip-value">What was delivered</div></div>
    <div class="strip-item"><div class="strip-label">Author</div><div class="strip-value">SAS Asset Management</div></div>
  </div>
</section>
```

```css
.page-cover { color: var(--white); }
.cover-hero { position: absolute; inset: 0; background-size: cover; background-position: center; z-index: 1; }
.cover-gradient { position: absolute; inset: 0; background: linear-gradient(135deg, rgba(0,34,68,0.92), rgba(0,34,68,0.75) 55%, rgba(0,34,68,0.95)); z-index: 2; }
.cover-topbar { position: absolute; top: 9mm; left: 0; right: 0; z-index: 10; display: flex; justify-content: space-between; padding: 9mm 12mm 0; }
.cover-sas-logo { width: 180px; height: auto; filter: brightness(0) invert(1); }
.cover-client-logo { color: #ffffff; }
.cover-client-logo svg { height: 26px; width: auto; display: block; }
.cover-eyebrow { font-size: 11pt; letter-spacing: 0.25em; text-transform: uppercase; color: var(--sas-green); margin-bottom: 4mm; }
.cover-headline { font-size: 54pt; font-weight: 700; line-height: 1.02; letter-spacing: -0.02em; margin: 0 0 4mm; }
.cover-subhead { font-size: 15pt; font-weight: 300; line-height: 1.3; max-width: 160mm; color: rgba(255,255,255,0.85); }
.cover-strip { display: grid; grid-template-columns: repeat(5, 1fr); gap: 6mm; padding: 5mm 0 0; border-top: 1px solid rgba(105,190,40,0.35); }
.strip-label { font-size: 6.5pt; letter-spacing: 0.2em; text-transform: uppercase; color: var(--sas-green); font-weight: 600; margin-bottom: 1mm; }
.strip-value { font-size: 9pt; font-weight: 500; color: var(--white); line-height: 1.35; }
```

### Stat tiles (4 up)

```css
.stat-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 5mm; margin: 6mm 0; }
.stat-tile {
  background: var(--bg-grey);
  border-left: 4px solid var(--sas-green);
  border-radius: var(--radius-md);
  padding: 6mm;
  box-shadow: var(--shadow-sm);
}
.stat-tile .num { font-size: 28pt; font-weight: 700; color: var(--sas-blue); line-height: 1; letter-spacing: -0.02em; margin-bottom: 2mm; }
.stat-tile .lbl { font-size: 7.5pt; font-weight: 600; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.1em; }
```

### Vertical timeline (phases)

```css
.timeline { position: relative; padding-left: 22mm; margin-top: 5mm; }
.timeline::before {
  content: "";
  position: absolute;
  left: 8mm; top: 0; bottom: 0;
  width: 1.2mm;
  background: linear-gradient(180deg, var(--sas-blue) 0%, var(--sas-green) 100%);
  border-radius: 1mm;
}
.phase { position: relative; padding-bottom: 6mm; }
.phase .node {
  position: absolute; left: -18mm; top: 0;
  width: 14mm; height: 14mm;
  border-radius: 50%;
  background: var(--sas-blue);
  color: var(--white);
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 14pt;
  border: 1mm solid var(--white);
  box-shadow: 0 2mm 4mm rgba(0,34,68,0.25);
}
.phase:nth-child(2) .node { background: #1a4874; }
.phase:nth-child(3) .node { background: var(--sas-green); }
.phase-card {
  background: var(--bg-grey);
  border-left: 4px solid var(--sas-green);
  border-radius: var(--radius-md);
  padding: 5mm 6mm;
}
.phase-card .badge { font-size: 7pt; font-weight: 600; color: var(--sas-green); text-transform: uppercase; letter-spacing: 0.15em; }
.phase-card h3 { font-size: 13pt; color: var(--sas-blue); margin: 1mm 0 2mm; }
.phase-card p { font-size: 9.5pt; color: var(--text-secondary); line-height: 1.5; margin: 0; }
.phase-card .finding {
  margin-top: 3mm; padding: 3mm;
  background: var(--white);
  border-radius: var(--radius-sm);
  font-size: 8.5pt; color: var(--sas-blue);
}
.phase-card .finding strong { color: var(--sas-green); }
```

### Before/After outcomes grid (3 columns)

```css
.outcomes {
  display: grid;
  grid-template-columns: 1.4fr 1fr 1.4fr;
  gap: 3mm;
  margin-top: 4mm;
}
.outcomes .head {
  font-size: 7pt; font-weight: 700; color: var(--text-muted);
  text-transform: uppercase; letter-spacing: 0.15em;
  padding-bottom: 2mm; border-bottom: 2px solid var(--sas-green);
}
.outcomes .head.before { color: #c53030; }
.outcomes .head.after { color: #3d7a18; }
.outcomes .cell {
  padding: 4mm 5mm;
  border-radius: var(--radius-sm);
  font-size: 9pt; line-height: 1.4;
}
.outcomes .cell.metric { background: var(--sas-blue); color: var(--white); font-weight: 600; }
.outcomes .cell.before { background: rgba(197,48,48,0.08); color: var(--text-primary); }
.outcomes .cell.after  { background: rgba(105,190,40,0.12); color: var(--text-primary); font-weight: 500; }
```

### Testimonial card

```css
.quote {
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
  padding: 10mm 12mm;
  position: relative;
  box-shadow: var(--shadow-md);
  margin: 4mm 0;
}
.quote::before {
  content: "\201C";
  position: absolute; top: -6mm; left: 8mm;
  width: 16mm; height: 16mm;
  background: var(--sas-green);
  color: var(--white);
  font-family: Georgia, serif;
  font-size: 40pt; font-weight: 700; line-height: 1;
  border-radius: 50%;
  display: flex; align-items: flex-end; justify-content: center;
  padding-bottom: 2mm;
  box-shadow: 0 3mm 6mm rgba(105,190,40,0.35);
}
.quote-text { font-size: 13pt; font-weight: 500; line-height: 1.5; color: var(--sas-blue); font-style: italic; margin: 0 0 6mm; }
.quote-author { display: flex; align-items: center; gap: 4mm; padding-top: 4mm; border-top: 2px solid var(--border); }
.quote-avatar {
  width: 14mm; height: 14mm; border-radius: 50%;
  background: var(--sas-blue); color: var(--white);
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 11pt;
  flex-shrink: 0;
}
.quote-author .name { font-size: 11pt; font-weight: 700; color: var(--sas-blue); margin: 0; }
.quote-author .role { font-size: 8.5pt; color: var(--text-muted); margin: 1mm 0 0; }
```

### Back cover / CTA

```css
.page-back { background: var(--sas-blue); color: var(--white); }
.back-hero-bg { position: absolute; inset: 0; background-size: cover; opacity: 0.08; z-index: 0; }
.back-inner { position: relative; z-index: 2; display: flex; flex-direction: column; height: 100%; padding: 14mm 16mm 12mm; }
.back-cover-sas-logo { width: 200px; height: auto; filter: brightness(0) invert(1); display: block; }
.back-cta-heading { font-size: 26pt; font-weight: 900; line-height: 1.15; letter-spacing: -0.02em; margin-bottom: 5mm; }
.back-contact-grid {
  display: flex;
  border: 1.5px solid rgba(105,190,40,0.5);
  border-radius: var(--radius-lg);
  overflow: hidden;
  max-width: 140mm;
  margin: 0 auto;
}
.back-contact-item { flex: 1; padding: 5mm 6mm; text-align: center; border-right: 1px solid rgba(105,190,40,0.3); }
.back-contact-item:last-child { border-right: none; }
.bc-label { font-size: 6.5pt; font-weight: 600; letter-spacing: 0.2em; text-transform: uppercase; color: var(--sas-green); margin-bottom: 1.5mm; }
.bc-value { font-size: 8.5pt; font-weight: 500; color: var(--white); }
.back-footer { border-top: 1px solid rgba(255,255,255,0.15); padding-top: 5mm; text-align: center; font-size: 7.5pt; color: rgba(255,255,255,0.55); line-height: 1.6; }
```

**Contact defaults:**

- Email: `hello@sas-am.com` (not `info@`)
- Website: `sas-am.com`
- Location: `Melbourne, Australia`
- Tagline: "**SAS Asset Management** — We provide advanced analytics, expert asset management services and maturity assessments to help asset owners realise their value."

---

## PDF export command

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --no-pdf-header-footer \
  --virtual-time-budget=10000 \
  --print-to-pdf=output.pdf \
  "file:///path/to/case-study.html"
```

Expected: 8 pages, ≥900 KB (full-colour, full-fidelity), A4 portrait.

**Do NOT** pass `--window-size` or `--paper-width/--paper-height` for this template — the `@page { size: A4 portrait }` CSS rule handles sizing. Chrome's default A4 portrait matches exactly.

---

## Content rules (applied verbatim to all case studies)

- Australian English throughout (organisation, standardise, centre, colour, analyse)
- No hyphens in prose — use em dashes `—` or restructure (SAS-AM brand hyphen allowed)
- Every claim, number, and quote must trace to user interview or verified material — never fabricate
- Testimonials require name + title + organisation attribution; skip the block if no approved quote
- Before/After table: if exact numbers aren't available, use directional language ("reduced by approximately…")
