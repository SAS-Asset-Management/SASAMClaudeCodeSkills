---
name: sas-presentation
description: Create polished marcov / SAS-AM branded Reveal.js presentations. Use when the user asks to create slides, a presentation, a deck, or a slideshow. Supports 17 presentation types — from standard narrative decks to dashboards, proposals, and meeting minutes. Implements SAS brand guidelines with light/dark mode and professional layouts. Generates standalone HTML + CSS with no build step required. Complies with marcov-revealjs-standards v1.0.0.
---

# SAS-AM Presentation Skill

Create professional HTML presentations using Reveal.js with SAS-AM brand guidelines. The output is a standalone HTML file that can be opened directly in any browser, shared via USB, or hosted on any static file server.

## SAS-AM Tagline

Every presentation MUST include the SAS-AM tagline on at least one slide (typically the title slide, closing slide, or an "About Us" section):

> "At SAS-AM we help organisations understand their strengths and weaknesses, model and predict the future, and make the right decisions through audit and benchmarking, advanced analytics and deep advisory services."

## Overview

This skill creates presentations following the marcov / SAS-AM communication style, which features:

- **17 Presentation Types**: Standard presentations, reports, dashboards, proposals, pitch decks, and more
- **SAS Brand Colours**: SAS Blue (#002244) and SAS Green (#69BE28)
- **Light/Dark Mode Toggle**: Built-in theme switching with localStorage persistence
- **Type-Specific Structures**: Each type has its own section layout, tone, and component set
- **Professional Typography**: Source Sans Pro + Source Code Pro font families
- **Static Footer Navigation**: Section progress indicator with keyboard-accessible theme toggle
- **Dual-Theme Assets**: Support for light/dark image variants
- **WCAG 2.1 AA Compliance**: Focus indicators, reduced motion, screen reader support
- **marcov Standards Compliant**: All output follows marcov-revealjs-standards v1.0.0

## Supported Presentation Types

| Type | Slides | Layout | Best For |
|------|--------|--------|----------|
| **Presentation** | 10–20 | Mixed (split / full-bleed) | Conference talks, workshops, strategy sessions |
| **Report** | 15–30 | Text-heavy with charts | Maturity assessments, audit findings, deep-dives |
| **One Pager** | 1–3 | Dense single-slide | Service summaries, leave-behinds, handouts |
| **Dashboard** | 3–8 | Grid / Card-based | Monthly reporting, operational reviews |
| **Chart** | 1–3 | Centred visual | LinkedIn posts, data storytelling |
| **Resume / CV** | 3–6 | Split (sidebar + main) | Tender submissions, team profiles |
| **Proposal** | 10–15 | Mixed (narrative + structured) | Client proposals, tender responses |
| **Capability Brochure** | 8–12 | Visual-heavy / Magazine | Business development, conference handouts |
| **Case Study** | 6–10 | Storytelling arc | BD meetings, tender evidence |
| **Pitch Deck** | 8–12 | Full-bleed / High-impact | Investor pitches, partnership discussions |
| **Executive Briefing** | 4–7 | Clean / Sparse | Board updates, sponsor briefings |
| **Workshop / Training** | 10–25 | Mixed (instructional) | Client workshops, training, tutorials |
| **Project Status Update** | 5–8 | Structured / Tabular | Weekly/monthly project reporting |
| **Technical Architecture** | 6–12 | Diagram-centric | Solution design reviews, system docs |
| **Roadmap / Timeline** | 5–10 | Horizontal timeline | Product roadmaps, transformation plans |
| **Comparison Matrix** | 4–8 | Grid / Table-centric | Technology selection, vendor evaluation |
| **Meeting Minutes** | 3–6 | Structured / List-based | Post-meeting distribution, governance |

For full type definitions including sections, components, and Reveal.js overrides, see `references/presentation-types.md`.

## Discovery Process (CRITICAL)

**Before creating any presentation, you MUST conduct a discovery interview. The goal is to identify the right presentation type and gather content requirements.**

### Phase 1: Identify the Presentation Type

Ask these questions to determine the best type:

1. **What is the primary purpose of this document?**
   - Telling a story / persuading → **Presentation**, **Pitch Deck**, **Case Study**
   - Presenting data or findings → **Report**, **Dashboard**, **Chart**
   - Proposing or selling → **Proposal**, **Capability Brochure**
   - Tracking or reporting → **Project Status Update**, **Meeting Minutes**
   - Teaching or training → **Workshop / Training**
   - Documenting or comparing → **Technical Architecture**, **Comparison Matrix**, **Roadmap / Timeline**
   - Profiling people or services → **Resume / CV**, **One Pager**
   - Briefing leadership → **Executive Briefing**

2. **Who is the primary audience?**
   - Senior executives / board → **Executive Briefing**, **Dashboard**
   - Investors or partners → **Pitch Deck**
   - Clients (commercial) → **Proposal**, **Capability Brochure**, **Case Study**
   - Internal team → **Project Status Update**, **Meeting Minutes**, **Workshop**
   - Conference / public → **Presentation**, **One Pager**
   - Technical reviewers → **Technical Architecture**, **Comparison Matrix**

3. **How many slides do you expect? (or how much content do you have?)**
   - 1–3 slides → **One Pager**, **Chart**, **Executive Briefing**
   - 5–10 slides → **Dashboard**, **Case Study**, **Pitch Deck**, **Roadmap**
   - 10–20 slides → **Presentation**, **Proposal**, **Capability Brochure**
   - 15–30 slides → **Report**, **Workshop / Training**

4. **What is the dominant content format?**
   - Narrative text with visuals → **Presentation**, **Case Study**, **Pitch Deck**
   - Tables, metrics, KPIs → **Dashboard**, **Report**, **Project Status Update**
   - Diagrams and architecture → **Technical Architecture**
   - Comparison grids → **Comparison Matrix**
   - Lists, actions, decisions → **Meeting Minutes**
   - Timeline / phases → **Roadmap / Timeline**

Once the type is determined, confirm with the user: _"Based on what you've described, I'd recommend a **[Type]** format — it uses [key characteristic]. Does that sound right?"_

### Phase 2: Gather Content Details

5. **Topic & Key Message**
   - What is this about?
   - What is the single most important takeaway?
   - Is there a specific call-to-action?

6. **Delivery Context**
   - Where will this be presented? (conference, boardroom, webinar, shared via USB/email)
   - How much time do you have? (affects slide count)
   - Will you be presenting live or is it for self-navigation?

7. **Branding**
   - Should we use marcov / SAS-AM branding (default) or a client's brand?
   - If client branding, what are their brand colours?

8. **Visual Assets**
   - Do you have specific images, diagrams, or visualisations to include?
   - Should I create conceptual SVG diagrams?
   - Do you need a QR code for the closing slide?

9. **Content Outline**
   - Do you have existing content, bullet points, or a rough outline?
   - What are the key sections or topics to cover?
   - (Show the user the section list for the selected type and ask if they want to add/remove/reorder any)

### Default Narrative Structure (for "Presentation" type)

The default **Presentation** type uses this proven 7-section structure:

| Section | Purpose | Example |
|---------|---------|---------|
| **OPENING** | Hook the audience, reframe the problem | "Your Million-Dollar EAM System Might Just Be A Very Expensive Filing Cabinet" |
| **THE CONTEXT** | Establish the current situation | "Siloed failures - one truck breaks down but the fleet learns nothing" |
| **THE PROBLEM** | Identify specific pain points | "Cloud analytics can't make split-second decisions" |
| **THE SOLUTION** | Present your answer | "Edge Federated Machine Learning" |
| **THE IMPLEMENTATION** | Show how it works practically | "Start small. One asset class. One location." |
| **THE FUTURE** | Vision and possibilities | "Maintenance schedules that write themselves" |
| **THE CONNECTION** | Call to action | "Ready to make your assets intelligent?" |

Other types have their own section structures — see `references/presentation-types.md` for the full mapping.

---

## File Structure

A SAS presentation consists of:

```
presentation-folder/
├── presentation.html    # Main presentation file
├── styles.css           # Custom theme styles
└── assets/              # Images (PNG, JPG, SVG)
    ├── sas-logo-light.svg   # Light mode logo (transparent background)
    ├── sas-logo-dark.png    # Dark mode logo
    └── [slide-images]-blue.png / -green.png
```

## Bundled Logo Assets

This skill includes official SAS-AM logo files in the `references/assets/` directory:

- **`sas-logo-light.svg`** - Green arrow logo for **light mode** (transparent background SVG)
- **`sas-logo-dark.png`** - Green arrow logo for **dark mode**

### Logo Behaviour

The CSS automatically switches logos based on the current theme:
- **Light mode**: Displays elements with class `logo-light`
- **Dark mode**: Displays elements with class `logo-dark`

### Copying Logos to Your Presentation

When creating a new presentation, copy the bundled logos to your presentation's `assets/` folder:

```bash
# From the skill's references/assets directory
cp sas-logo-light.svg /path/to/your-presentation/assets/
cp sas-logo-dark.png /path/to/your-presentation/assets/
```

Or reference them directly in your HTML using the bundled paths during development.

---

## Technical Specifications

### HTML Document Structure (marcov Standards)

Every presentation MUST include these required elements:

- `<!DOCTYPE html>` declaration
- `lang="en-AU"` on `<html>`
- `data-theme="light"` default attribute
- `charset="UTF-8"`
- Viewport meta tag
- Description and author meta tags
- Title with `| marcov` suffix

```html
<!DOCTYPE html>
<html lang="en-AU" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Description of the presentation">
  <meta name="author" content="marcov / SAS Asset Management">
  <title>Presentation Title | marcov</title>

  <!-- Reveal.js -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css">

  <!-- Font Awesome -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@300;400;600;700&family=Source+Code+Pro:wght@400;600&display=swap" rel="stylesheet">

  <!-- marcov Styles -->
  <link rel="stylesheet" href="styles.css">
</head>
```

See `references/scaffold-template.html` for the complete scaffold including JavaScript.

### Structural Rules

- Each slide is a `<section>` element
- Every `<section>` requires a unique `id`
- Every `<section>` requires a `data-section` attribute
- Horizontal slides: top-level `<section>`. Vertical sub-slides: nested `<section>` within parent
- `<h1>` — title slide only (one per deck)
- `<h2>` — slide titles. `<h3>` — card/section headings. `<h4>` — sub-headings. Never skip heading levels
- All `<img>` tags must have `alt` text. Decorative images: `alt="" role="presentation"`
- Inline SVGs preferred over image files
- CSS variables for all theme-aware colours — no hardcoded values
- All JS at bottom of `<body>`
- No build step — open-in-browser ready

### Reveal.js Configuration

All types inherit this base configuration:

```javascript
Reveal.initialize({
  hash: true,
  hashOneBasedIndex: false,
  respondToHashChanges: true,
  history: false,
  slideNumber: 'c/t',
  showSlideNumber: 'speaker',
  center: false,
  width: 1920,
  height: 1080,
  margin: 0,
  minScale: 0.2,
  maxScale: 2.0,
  transition: 'slide',
  transitionSpeed: 'default',
  backgroundTransition: 'fade',
  keyboard: true,
  touch: true,
  loop: false,
  embedded: false,
  help: true,
  mouseWheel: false,
  hideInactiveCursor: true,
  hideCursorTime: 3000,
  fragments: true,
  fragmentInURL: true,
  pdfMaxPagesPerSlide: 1,
  pdfSeparateFragments: false,
});
```

**Per-Type Overrides** (apply only when the type specifies them):

| Type | Override |
|------|----------|
| Dashboard | `transition: 'fade'` |
| Workshop / Training | `help: true`, `showSlideNumber: 'all'` |
| One Pager | `loop: true` (kiosk mode) |
| Project Status Update | `transition: 'fade'` |

### Theme Management

Three states: `light` (default), `dark`, `system` (follows OS preference). Storage key: `marcov-presentation-theme`.

The `data-theme` attribute is applied to `<html>`, `<body>`, and `.reveal-viewport`. All colours use CSS custom properties.

### Footer Navigation

- Section map built once on Reveal `ready` event
- Active section highlighted with accent colour
- Click any section to jump to its first slide
- Keyboard accessible: `tabindex="0"`, `role="button"`, Enter/Space activation
- Footer positioned `fixed` outside Reveal container

---

## Slide Types

### 1. Title Slide

The opening slide with logo, main title, subtitle, and author.

```html
<section id="title" class="title-slide" data-section="opening">
  <div class="title-content">
    <img src="assets/sas-logo-light.svg" alt="SAS Logo" class="title-logo logo-light">
    <img src="assets/sas-logo-dark.png" alt="SAS Logo" class="title-logo logo-dark">
    <h1>From Worthless Data to Intelligent Assets</h1>
    <h2>Edge Federated ML in Real Work Asset Management</h2>
    <p class="author">Shane Scriven – Founder + Managing Director SAS-AM</p>
  </div>
</section>
```

**Typography:**
- `<h1>`: 64px, weight 300, text-primary colour
- `<h2>`: 36px, weight 400, accent colour (SAS Green)
- `.author`: 24px, text-muted colour

---

### 2. Standard Content Slide

Two-column layout with content on left, image/visual on right.

```html
<section id="unique-id" data-section="opening">
  <div class="slide-layout with-image">
    <!-- Optional: Logo in top-right -->
    <img src="assets/sas-logo-light.svg" alt="SAS Logo" class="slide-logo logo-light">
    <img src="assets/sas-logo-dark.png" alt="SAS Logo" class="slide-logo logo-dark">

    <div class="slide-header">
      <span class="section-tag">OPENING</span>
    </div>

    <div class="slide-body split">
      <div class="slide-content">
        <h2 class="slide-title">REFRAMING ASSET DATA</h2>
        <p class="slide-subtitle">Your Million-Dollar EAM System Might Just Be A Very Expensive Filing Cabinet</p>
      </div>
      <div class="slide-image">
        <img src="assets/visual-blue.png" alt="Description" class="logo-light">
        <img src="assets/visual-green.png" alt="Description" class="logo-dark">
      </div>
    </div>
  </div>
</section>
```

**Typography:**
- `.section-tag`: 14px, weight 600, uppercase, letter-spacing 2px, accent colour
- `.slide-title`: 72px, weight 700, uppercase, letter-spacing -1px, max-width 50%
- `.slide-subtitle`: 36px, weight 300, text-secondary colour

---

### 3. Slide with SVG Diagram

For conceptual diagrams, use inline SVG with CSS variables for theme support.

```html
<section id="concept" data-section="solution">
  <div class="slide-layout">
    <div class="slide-header">
      <span class="section-tag">THE SOLUTION</span>
    </div>
    <div class="slide-body split">
      <div class="slide-content">
        <h2 class="slide-title">EDGE FEDERATED ML</h2>
        <p class="slide-subtitle">Place The Intelligence On The Asset</p>
      </div>
      <div class="slide-image">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="600" height="400">
          <!-- Use CSS variables for theme-aware colours -->
          <rect fill="var(--bg-tertiary)" stroke="var(--card-border)" .../>
          <circle fill="var(--accent)" .../>
          <text fill="var(--text-primary)" font-family="Arial, sans-serif">...</text>

          <!-- Animated elements -->
          <circle r="5" fill="var(--accent)">
            <animate attributeName="cy" values="0;100;0" dur="2s" repeatCount="indefinite"/>
          </circle>
        </svg>
      </div>
    </div>
  </div>
</section>
```

---

### 4. Step Animation Slide (Fragment Transitions)

Progressive reveal using Reveal.js fragments.

```html
<section id="process" data-section="solution">
  <div class="slide-layout">
    <div class="slide-header">
      <span class="section-tag">THE SOLUTION</span>
    </div>
    <div class="slide-body split">
      <div class="slide-content">
        <h2 class="slide-title">ON-ASSET TRAINING</h2>
        <p class="slide-subtitle">Train a local ML model where the data is generated</p>
      </div>
      <div class="slide-image diagram-container">
        <!-- Step 1: Visible by default, fades out when advancing -->
        <div class="federated-diagram step-1 fragment fade-out" data-fragment-index="1">
          <img src="assets/step-1-blue.png" class="logo-light">
          <img src="assets/step-1-green.png" class="logo-dark">
        </div>

        <!-- Step 2: Fades in, then out -->
        <div class="federated-diagram step-2 fragment fade-in-then-out" data-fragment-index="1">
          <img src="assets/step-2-blue.png" class="logo-light">
          <img src="assets/step-2-green.png" class="logo-dark">
        </div>

        <!-- Step 3: Final state, fades in and stays -->
        <div class="federated-diagram step-3 fragment fade-in" data-fragment-index="2">
          <img src="assets/step-3-blue.png" class="logo-light">
          <img src="assets/step-3-green.png" class="logo-dark">
        </div>
      </div>
    </div>
  </div>
</section>
```

---

### 5. Closing/CTA Slide

Call-to-action with QR code and branding.

```html
<section id="closing" data-section="connection">
  <div class="slide-layout closing">
    <div class="slide-header">
      <span class="section-tag">THE CONNECTION</span>
    </div>
    <div class="slide-body centered">
      <h2 class="closing-headline">Ready To Make Your Assets Intelligent?</h2>

      <div class="qr-wrapper">
        <div class="qr-container">
          <div class="qr-glow"></div>
          <img src="assets/qr-code.png" alt="QR Code" class="qr-code">
        </div>
        <div class="qr-cta">
          <span class="qr-action">SCAN TO CONNECT</span>
          <p class="qr-label">Learn more about Edge AI in Asset Management</p>
        </div>
      </div>

      <div class="closing-branding">
        <img src="assets/sas-logo-light.svg" alt="SAS Logo" class="closing-logo logo-light">
        <img src="assets/sas-logo-dark.png" alt="SAS Logo" class="closing-logo logo-dark">
        <p class="closing-search"><i class="fas fa-search"></i> EDGE AI ASSET MANAGEMENT</p>
      </div>
    </div>
  </div>
</section>
```

---

## Colour System

### Light Mode (Default)

```css
:root,
:root[data-theme="light"] {
  /* SAS Brand Colours */
  --sas-green: #69BE28;
  --sas-blue: #002244;

  /* Backgrounds */
  --bg-primary: #ffffff;
  --bg-secondary: #f7f7f7;
  --bg-tertiary: #ededed;

  /* Text - ALL text is SAS Blue in light mode */
  --text-primary: #002244;
  --text-secondary: #334466;
  --text-muted: #6b7280;

  /* Accent */
  --accent: #69BE28;
  --accent-hover: #5AA822;

  /* Cards and containers */
  --card-bg: rgba(255, 255, 255, 0.95);
  --card-border: rgba(0, 34, 68, 0.15);

  /* Footer */
  --footer-bg: #f7f7f7;
  --footer-border: #ededed;

  /* Shadows */
  --shadow-sm: 0 2px 8px rgba(0, 34, 68, 0.08);
  --shadow-md: 0 4px 16px rgba(0, 34, 68, 0.12);
  --shadow-lg: 0 8px 24px rgba(0, 34, 68, 0.15);

  /* Focus */
  --focus-ring: 0 0 0 3px rgba(105, 190, 40, 0.5);

  /* Code */
  --code-bg: #f0f4f8;
  --code-text: #1e3a5f;
}
```

### Dark Mode

```css
:root[data-theme="dark"] {
  /* SAS Brand (adjusted for dark) */
  --sas-green: #7AD33B;
  --sas-blue: #1a4d7a;

  /* Backgrounds */
  --bg-primary: #0a0f1a;
  --bg-secondary: #141d2b;
  --bg-tertiary: #1e2a3d;

  /* Text */
  --text-primary: #f4fbff;
  --text-secondary: #d1e3ed;
  --text-muted: #8ba3b5;

  /* Accent */
  --accent: #69BE28;
  --accent-hover: #7AD33B;

  /* Cards and containers */
  --card-bg: rgba(20, 29, 43, 0.9);
  --card-border: rgba(255, 255, 255, 0.08);

  /* Footer */
  --footer-bg: #141d2b;
  --footer-border: #1e2a3d;

  /* Shadows */
  --shadow-sm: 0 2px 8px rgba(0, 10, 28, 0.3);
  --shadow-md: 0 4px 16px rgba(0, 10, 28, 0.4);
  --shadow-lg: 0 14px 30px rgba(0, 10, 28, 0.5);

  /* Focus */
  --focus-ring: 0 0 0 3px rgba(105, 190, 40, 0.4);

  /* Code */
  --code-bg: #1a2332;
  --code-text: #d1e3ed;
}
```

---

## Typography Specifications

| Element | Font Size | Weight | Colour | Other |
|---------|-----------|--------|--------|-------|
| Title Slide h1 | 64px | 300 | text-primary | line-height 1.2 |
| Title Slide h2 | 36px | 400 | accent | - |
| Author | 24px | 400 | text-muted | - |
| Section Tag | 14px | 600 | accent | uppercase, letter-spacing 2px |
| Slide Title | 72px | 700 | text-primary | uppercase, letter-spacing -1px, max-width 50% |
| Slide Subtitle | 36px | 300 | text-secondary | line-height 1.4 |
| Footer Nav | 11px | 600 | text-muted | uppercase, letter-spacing 1.5px |

**Font Families:**
- Source Sans Pro (300, 400, 600, 700 weights) — body text, headings
- Source Code Pro (400, 600 weights) — code blocks, inline code, keyboard badges

---

## Asset Naming Convention

### Dual-Theme Images

For images that need different variants in light/dark mode:

```
assets/
├── visual-blue.png     # Light mode (blue-tinted)
├── visual-green.png    # Dark mode (green-tinted)
├── diagram-blue.png
├── diagram-green.png
└── ...
```

Use CSS classes to show/hide:

```html
<img src="assets/visual-blue.png" class="logo-light">
<img src="assets/visual-green.png" class="logo-dark">
```

```css
:root[data-theme="light"] .logo-light { display: block !important; }
:root[data-theme="light"] .logo-dark { display: none !important; }
:root[data-theme="dark"] .logo-light { display: none !important; }
:root[data-theme="dark"] .logo-dark { display: block !important; }
```

### Single-Theme Images

For images that work in both themes (photos, memes):

```html
<img src="assets/photo.png" alt="Description">
```

---

## Layout Specifications

### Slide Dimensions

- **Width**: 1920px
- **Height**: 1080px
- **Aspect Ratio**: 16:9
- **Padding**: 60px

### Split Layout

- **Gap**: 60px between content and image
- **Content**: flex: 1
- **Image**: flex: 1, max-width 600px, max-height 500px

### Logo Placement

- **Slide Logo**: Position absolute, top 30px, right 40px, width 80px
- **Title Logo**: Width 150px, centered, margin-bottom 60px

---

## Animation Features

### Binary Background

Subtle falling binary code animation:

```css
@keyframes binaryFall {
  0% { transform: translateY(-100%); }
  100% { transform: translateY(100vh); }
}

.binary-column {
  position: absolute;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  animation: binaryFall linear infinite;
}

/* Light mode - very subtle */
:root[data-theme="light"] .binary-column {
  color: rgba(0, 34, 68, 0.04);
}

/* Dark mode */
:root[data-theme="dark"] .binary-column {
  color: rgba(255, 255, 255, 0.03);
}
```

### QR Code Pulse

```css
@keyframes qrPulse {
  0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.3; }
  50% { transform: translate(-50%, -50%) scale(1.1); opacity: 0.5; }
}

.qr-glow {
  animation: qrPulse 2s ease-in-out infinite;
  background: radial-gradient(circle, var(--accent) 0%, transparent 70%);
}
```

### SVG Animations

Use `<animate>` elements for data flow visualisations:

```svg
<circle r="5" fill="var(--accent)">
  <animate attributeName="cy" values="0;100;0" dur="2.5s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="1;0;1" dur="2.5s" repeatCount="indefinite"/>
</circle>
```

---

## Reusable Components

These CSS components are available in `base-styles.css` for use across all presentation types:

| Component | CSS Class | Use For |
|-----------|-----------|---------|
| Card | `.card` | Content container with border and shadow |
| Card Grid | `.card-grid` + `.card-grid-2/3/4` | Responsive grid of cards |
| Table | `.ref-table` | Styled data table with accent headers |
| Checklist | `.checklist` + `.check-icon` | Lists with check/square icons |
| Badge | `.badge` + `.badge-required/recommended/optional` | Status indicator labels (RAG) |
| Code Block | `.code-block` | Monospace code display |
| Inline Code | `.code-inline` | Inline monospace text |
| Keyboard Key | `.kbd` | Keyboard shortcut badge |
| Split Layout | `.split-layout` | Two-column responsive layout |
| Scroll Container | `.scroll-y` | Scrollable content area for overflow |
| Section Tag | `.ref-section-tag` | Section label (uppercase, accent colour) |
| Title | `.ref-title` | Large slide heading (56px) |
| Subtitle | `.ref-subtitle` | Secondary heading (28px) |
| Body Text | `.ref-body` | Standard body copy (22px) |
| Small Text | `.ref-small` | Fine print / captions (16px) |
| Screen Reader | `.sr-only` | Visually hidden but accessible text |

### Chart & Data Visualisation Components

A full library of inline SVG chart patterns is available in `references/chart-components.html`. All charts are theme-aware (light/dark), accessible (`role="img"` + `aria-label`), and interactive (hover highlights with sibling dimming via `.chart-interactive`).

| # | Chart Type | CSS Classes | Best For |
|---|-----------|-------------|----------|
| 1 | Horizontal Bar | `.chart-bar` | Ranked categorical comparisons |
| 2 | Grouped Bar | `.chart-bar` + legend | Side-by-side multi-series comparison |
| 3 | Stacked Bar | `.chart-bar` | Composition of totals |
| 4 | Line Chart | `.chart-line`, `.chart-point` | Trends over time |
| 5 | Area Chart | `.chart-area`, `.chart-line` | Volume/magnitude trends |
| 6 | Sparkline | `.chart-sparkline`, `.chart-sparkline-line` | Inline KPI trend indicators |
| 7 | Donut | `.chart-slice` | Proportions of a whole (max 6 segments) |
| 8 | Waterfall | `.chart-bar` | Cumulative positive/negative changes |
| 9 | Treemap | `.chart-treemap-cell` | Hierarchical proportional data |
| 10 | Radar / Spider | `.chart-radar-*`, `.chart-point` | Multi-dimension comparison (5-8 axes) |
| 11 | Heatmap / Matrix | `.chart-cell` | Two-dimension intensity mapping |
| 12 | Gauge | `.chart-gauge-bg`, `.chart-gauge-fill` | Single KPI vs target |
| 13 | Scatter | `.chart-point` | Correlation between two variables |
| 14 | Bubble | `.chart-bubble` | Three-variable comparison (x, y, size) |
| 15 | RAG Status Grid | `.chart-rag-grid`, `.rag-item` | Red/Amber/Green health dashboards |
| 16 | Progress Bars | `.chart-progress-*` | Completion / utilisation rates |
| 17 | Quadrant | `.chart-quadrant-*`, `.chart-point` | Strategic classification (2x2) |
| 18 | Funnel | `.chart-funnel-segment` | Sequential stage drop-off |
| 19 | Sankey | `.chart-sankey-node`, `.chart-sankey-link` | Flow and transformation between stages |
| 20 | Distribution | `.chart-distribution-area` | Probability density / frequency curves |
| 21 | Violin Plot | `.chart-violin-half`, `.chart-violin-box` | Distribution shape + box plot combined |
| 22 | Circular Bar | `.chart-circular-bar`, `.chart-circular-track` | Radial KPI completion with centre value |
| 23 | Chord Diagram | `.chart-chord-arc`, `.chart-chord-ribbon` | Relationship flow between entities |
| 24 | Network Diagram | `.chart-network-node`, `.chart-network-link` | Entity relationship / dependency mapping |

**Chart interactivity pattern:**
- Add `class="chart-interactive"` to the parent `<svg>` to enable sibling dimming on hover
- Place `<g class="chart-svg-tooltip">` immediately after each data element for no-JS tooltip fallback
- Use `--chart-1` through `--chart-6` for the categorical colour palette (theme-aware)
- Always include `role="img"` and `aria-label` on the SVG element

---

## Workflow

### Step 1: Discovery Interview

Conduct the discovery interview to:
1. **Identify the presentation type** using Phase 1 questions (purpose, audience, slide count, content format)
2. **Confirm the type** with the user
3. **Gather content details** using Phase 2 questions (topic, delivery context, branding, assets, outline)
4. **Review the section structure** for the selected type (from `references/presentation-types.md`) and confirm any additions or removals

### Step 2: Create Presentation Structure

1. Create a new directory for the presentation
2. Copy `base-styles.css` from references as `styles.css`
3. Create `presentation.html` using the scaffold template — adapt the sections and footer nav items to match the selected presentation type
4. Create `assets/` directory
5. Copy logo assets from `references/assets/`

### Step 3: Build Content Slides

Work through slides incrementally:
1. Create title slide
2. Build out each section following the type's section structure
3. Add section-appropriate `data-section` attributes (matching `references/presentation-types.md`)
4. Update footer nav items to match the sections
5. Apply any type-specific Reveal.js overrides
6. Include dual-theme images where needed
7. Use the appropriate reusable components (cards, tables, badges, etc.) for the type
8. Add charts and data visualisations from `references/chart-components.html` where needed — copy the inline SVG pattern and adjust data values

### Step 4: Review and Refine

1. Test navigation in browser
2. Verify light/dark mode toggle
3. Check all images load correctly
4. Ensure footer navigation tracks correctly
5. Run the pre-delivery checklist (see below)

### Step 5: Export (Optional)

For PDF export:
```bash
npx decktape reveal "presentation.html" output.pdf
```

For screenshots:
```bash
npx decktape reveal "presentation.html" output.pdf --screenshots --screenshots-directory screenshots/
```

---

## Content Writing Guidelines

### Headlines (Slide Titles)

- **Format**: ALL CAPS, punchy, memorable
- **Length**: 2-5 words
- **Style**: Action-oriented or provocative
- **Examples**:
  - "REFRAMING ASSET DATA"
  - "SILOED FAILURES"
  - "REAL-TIME ACTION"

### Subtitles

- **Format**: Title Case, explanatory
- **Length**: One sentence (10-20 words)
- **Style**: Expands on the headline with a specific insight
- **Examples**:
  - "Your Million-Dollar EAM System Might Just Be A Very Expensive Filing Cabinet"
  - "Every Sensor Reading Into Your EAM Represents A Missed Opportunity"

### Section Tags

- **Format**: ALL CAPS
- **Options**: OPENING, THE CONTEXT, THE PROBLEM, THE SOLUTION, THE IMPLEMENTATION, THE FUTURE, THE CONNECTION

---

## Responsive Considerations

```css
@media screen and (max-width: 1400px) {
  .slide-title { font-size: 56px; }
  .slide-subtitle { font-size: 28px; }
  .title-slide h1 { font-size: 48px; }
  .title-slide h2 { font-size: 28px; }
  .ref-title { font-size: 44px; }
  .ref-subtitle { font-size: 24px; }
  .card-grid-3 { grid-template-columns: repeat(2, 1fr); }
}

@media screen and (max-width: 1000px) {
  .slide-body.split { flex-direction: column; }
  .slide-image { max-height: 300px; }
  .nav-items { gap: 15px; }
  .nav-item { font-size: 10px; }
  .split-layout { flex-direction: column; }
  .card-grid-2, .card-grid-3, .card-grid-4 { grid-template-columns: 1fr; }
}
```

---

## Print Styles

```css
@media print {
  .static-footer { display: none; }
  .binary-background { display: none; }
  .reveal .slides section { page-break-after: always; }
}
```

---

## Accessibility (WCAG 2.1 AA)

All presentations must meet these minimum standards:

### Colour Contrast
- **Normal text:** 4.5:1 minimum ratio
- **Large text (≥24px / 18.67px bold):** 3:1 minimum
- **UI components:** 3:1 against adjacent colours
- Test both light and dark themes independently

### Keyboard Access
- All interactive elements focusable via Tab
- Visible focus indicators using `--focus-ring` variable
- Never use `outline: none` without a replacement
- Custom buttons: `role="button"` + `tabindex="0"`
- Enter and Space activate custom controls

### Screen Readers
- `lang="en-AU"` on `<html>`
- Descriptive `alt` on all images
- Decorative images: `alt="" role="presentation"`
- `aria-label` on icon-only buttons
- Use `.sr-only` class for visually hidden labels
- `aria-hidden="true"` on binary background columns

### Typography Access
- Minimum body text: 16px (24px on slides)
- Line height ≥ 1.4 for body copy
- Max line length: ~75 characters
- No justified text — use left-aligned

### Reduced Motion (Mandatory)

This rule MUST appear in every stylesheet:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

### Semantic HTML
- Use `<nav>`, `<main>`, `<footer>` landmarks
- Headings in sequential order (h1 → h2 → h3)
- Lists for list content (`<ul>`/`<ol>`)
- Tables for tabular data (with `<th>` headers)
- `<button>` for actions, `<a>` for navigation

---

## Dependencies (CDN)

All loaded from CDN — no npm install required:

- **Reveal.js 5.1.0**: Presentation framework
- **Font Awesome 6.5.1**: Icons
- **Google Fonts**: Source Sans Pro (300, 400, 600, 700) + Source Code Pro (400, 600)

---

## Client Branding (Non-SAS)

When creating presentations for clients:

1. **Ask for brand colours** during discovery
2. **Replace CSS variables** in styles.css
3. **Update logos** in assets/
4. **Adjust footer** navigation if needed

Example (Yarra Trams):
```css
:root[data-theme="light"] {
  --brand-primary: #007b4b;  /* Yarra Green */
  --accent: #69BE28;         /* Keep SAS Green for buttons */
  --text-primary: #1a1a1a;
}
```

---

## Pre-Delivery Checklist

### HTML Compliance
- [ ] `<!DOCTYPE html>` declared
- [ ] `lang="en-AU"` set
- [ ] UTF-8 charset
- [ ] Viewport meta present
- [ ] Description and author meta tags present
- [ ] Title with `| marcov` suffix
- [ ] All slides have unique IDs
- [ ] All slides have `data-section` attributes
- [ ] Heading hierarchy correct (h1 → h2 → h3, no skips)
- [ ] No hardcoded colours (all via CSS variables)

### Accessibility
- [ ] All images have alt text
- [ ] Colour contrast passes 4.5:1
- [ ] Focus indicators visible
- [ ] ARIA labels on icon-only buttons
- [ ] Reduced motion rule present in stylesheet
- [ ] Keyboard navigation works
- [ ] Binary background columns have `aria-hidden="true"`

### Functionality
- [ ] Light/dark toggle works
- [ ] Footer nav tracks correctly
- [ ] Footer nav items match the presentation type's sections
- [ ] All fragments animate
- [ ] Hash URLs resolve
- [ ] Opens standalone in browser
- [ ] Australian English spelling used
- [ ] PDF export tested (if needed)

### Content
- [ ] Discovery interview completed
- [ ] Presentation type identified and confirmed
- [ ] Section structure follows the type definition
- [ ] Tone matches the type (formal, punchy, narrative, etc.)
- [ ] SAS-AM tagline included on at least one slide
