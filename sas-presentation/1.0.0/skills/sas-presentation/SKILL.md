---
name: sas-presentation
description: Create polished marcov / SAS-AM branded Reveal.js presentations. Use when the user asks to create slides, a presentation, a deck, or a slideshow. Supports 17 presentation types — from standard narrative decks to dashboards, proposals, and meeting minutes. Implements SAS brand guidelines with light/dark mode and professional layouts. Generates standalone HTML + CSS with no build step required. Complies with marcov-revealjs-standards v1.0.0.
---

# SAS-AM Presentation Skill

Create professional HTML presentations using Reveal.js with SAS-AM brand guidelines. The output is a standalone HTML file that can be opened directly in any browser, shared via USB, or hosted on any static file server.

## SAS-AM Tagline

Every presentation MUST include the SAS-AM tagline on at least one slide (typically the title slide, closing slide, or an "About Us" section):

> "At SAS-AM we help organisations understand their strengths and weaknesses, model and predict the future, and make the right decisions through audit and benchmarking, advanced analytics and deep advisory services."

## Presentation Philosophy

**You are the medium. The slides are optional scenery.**

Every presentation built by this skill follows these non-negotiable rules. They override all other guidance when there is a conflict.

### The Rules

| # | Rule | Enforcement |
|---|------|-------------|
| 01 | **One idea per talk** | The entire deck must be summarisable in a single sentence. If it needs three, you have three talks. |
| 02 | **Three key points maximum** | Human working memory holds three things comfortably. Not four. Not six. Three. |
| 03 | **10 words or fewer per slide** | Audience should glance and absorb in 3 seconds. If it takes longer, split the slide or move content to speaker notes. |
| 04 | **No bullet point lists** | Bullet lists make the audience read instead of listen. Use single statements, full bleed images, data charts, or cards (3 max). |
| 05 | **Tease with slides, tell with your voice** | The slide poses the question or shows the image. The speaker delivers the answer. If the slide contains everything you would say, you do not need to be in the room. |
| 06 | **Start with something unexpected** | Never open with your name, title, or an agenda slide. Open with tension: a surprising fact, a short personal story, or a question the audience did not know they wanted answered. |
| 07 | **Situation → Complication → Resolution** | The default B2B arc. Link acts with "but" and "therefore." This maps to: "Most clients do X [situation]. But this means Y [complication]. Therefore, we build Z [resolution]." |
| 08 | **Closing echoes opening** | The hook and payoff must mirror each other. The audience should feel the circle close. |
| 09 | **Final slide = Contributions** | Never end with "Thank You" or "Questions?" — those are weak closes. End with what you accomplished. This slide stays visible during Q&A (10+ minutes). |
| 10 | **Dead laptop test** | Could you deliver this talk if your laptop died on the way in? If not, the slides carry too much weight. Build the talk first; add slides only where they genuinely add something you cannot say with words. |

### Alternate Logic with Emotion

Data earns trust. Stories earn belief. Alternate between the two throughout your talk. A sharp data point followed by a human example, followed by another data point. This is Nancy Duarte's "sparkline": what is vs. what could be.

### Speaker Notes, Not Scripts

Do not memorise word for word — you will sound like a robot reading a teleprompter. Memorise the six or so transitions between ideas. The content fills itself in naturally once you know your transitions cold. Speaker notes in `<aside class="notes">` should contain:

- The transition phrase into this slide (e.g. "Which leads to the real problem...")
- One key statistic or story beat to deliver verbally
- Approximate timing
- Recovery phrase if you lose your place (repeating your last sentence almost always acts as a memory jogger — the audience will think you are emphasising)

### Sensory Storytelling

Do not say "it was a difficult situation." Say "it was 2am, the control room smelled of burnt coffee, and every phone in the building was ringing at once." Sensory detail is the difference between a fact and a memory. During discovery, always ask: "Can you describe a specific moment — time, place, what you saw or heard?"

---

## Overview

This skill creates presentations following the marcov / SAS-AM communication style, which features:

- **17 Presentation Types**: Standard presentations, reports, dashboards, proposals, pitch decks, and more
- **SAS Brand Colours**: SAS Blue (#002244) and SAS Green (#69BE28)
- **Light/Dark Mode Toggle**: Built-in theme switching with localStorage persistence
- **Type-Specific Structures**: Each type has its own section layout, tone, and component set
- **Professional Typography**: Source Sans Pro + Source Code Pro font families
- **Static Footer Navigation**: Section progress indicator with keyboard-accessible theme toggle
- **Dual-Theme Assets**: Support for light/dark image variants
- **Speaker Notes with Presenter View**: Reveal.js Notes plugin with transition cues, timing, and recovery phrases (press S to open)
- **WCAG 2.1 AA Compliance**: Focus indicators, reduced motion, screen reader support
- **marcov Standards Compliant**: All output follows marcov-revealjs-standards v2.0.0

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

5. **The One Sentence Test** (CRITICAL)
   - _"What is the ONE sentence summary of your entire talk?"_ — If the answer takes more than two sentences, keep cutting. This enforces Rule 01 (one idea per talk).

6. **The Rule of Three**
   - _"Give me three points that support that idea — no more."_ — These become the three content sections. If they give four, ask which one to cut.

7. **The Hook**
   - _"What is the most surprising thing about this topic? Something that would make someone stop scrolling."_ — This becomes the opening slide. It must not be the speaker's name, title, or an agenda.

8. **Sensory Detail**
   - _"Can you describe a specific moment — time, place, what you saw or heard?"_ — This feeds the storytelling component. Even data heavy presentations need one human moment.

9. **The Ask**
   - _"What should the audience DO differently after this?"_ — This becomes the Contributions/Recommendation slide. If the answer is vague, push for specifics.

10. **Delivery Context**
    - Where will this be presented? (conference, boardroom, webinar, shared via USB/email)
    - How much time do you have? (affects slide count)
    - Will you be presenting live or is it for self navigation?

11. **Branding**
    - Should we use marcov / SAS-AM branding (default) or a client's brand?
    - If client branding, what are their brand colours?

12. **Visual Assets**
    - Do you have specific images, diagrams, or visualisations to include?
    - Should I create conceptual SVG diagrams?
    - Do you have photos from site visits, workshops, or real moments? (these are always better than stock)

13. **Content Outline**
    - Do you have existing content, bullet points, or a rough outline?
    - (Show the user the section list for the selected type and ask if they want to add/remove/reorder any)

### Phase 3: Data & Visualisation Planning

If the presentation includes data, metrics, or KPIs, walk the user through chart selection and data sourcing. This phase should happen after content details are gathered but before building begins.

#### Step A: Identify What Needs Visualising

For each slide or section that involves data, ask:

10. **What are you trying to show with this data?**

    Use the answer to suggest chart types from this decision tree:

    | You want to show… | Recommended charts |
    |---|---|
    | **Ranking** — which is biggest/smallest | Horizontal Bar, Treemap |
    | **Comparison** — side by side across categories | Grouped Bar, Radar/Spider |
    | **Composition** — parts of a whole | Stacked Bar, Donut, Treemap |
    | **Trend over time** — how something changes | Line, Area, Sparkline |
    | **Correlation** — relationship between two things | Scatter, Bubble |
    | **Distribution** — how data is spread | Distribution, Violin, Histogram (Stacked Bar) |
    | **Flow / process** — how things move between stages | Sankey, Funnel |
    | **Relationships / dependencies** — what connects to what | Network, Chord Diagram |
    | **Status / health** — where things stand right now | RAG Grid, Gauge, Progress Bars, Circular Bar |
    | **Strategic positioning** — classify into quadrants | Quadrant Chart |
    | **Cumulative change** — what added up or eroded a total | Waterfall |
    | **Intensity across two dimensions** — where are the hotspots | Heatmap / Matrix |
    | **Single KPI headline** — one big number with context | Gauge, Sparkline (inline), Circular Bar |

    Present the recommendation: _"To show [what they described], I'd suggest a **[Chart Type]** — it works well because [reason]. Here's what it looks like…"_ (describe or reference the pattern in `chart-components.html`).

    If they're unsure, offer 2-3 options with a brief explanation of the visual difference.

#### Step B: Determine the Data Source

11. **Where is the data coming from?**

    Classify into one of three source types:

    | Source Type | Description | How to Handle |
    |---|---|---|
    | **Structured file** | CSV, Excel, JSON, database export — real numbers exist in a file | Ask the user to provide or point to the file. Read it, extract relevant columns/rows, and map values to the SVG chart coordinates. Always cite the source on the slide (e.g. "Source: FY24 Asset Register extract"). |
    | **Anecdotal / estimated** | The user knows rough numbers or proportions from experience but has no file | Ask them to provide the values conversationally (e.g. "About 60% roads, 25% bridges, 15% other"). Use their estimates directly. Label the chart appropriately (e.g. "Indicative" or "Estimated based on [context]"). |
    | **Mixed** | Some data is from files, some is estimated or contextual | Handle each data series independently — structured data gets precise values, anecdotal gets estimates. Clearly distinguish sourced vs estimated in footnotes or labels. |

12. **For structured data — ask:**
    - _"Can you share the file, or tell me where it is?"_ (path, URL, or paste)
    - _"Which columns or fields should I use?"_
    - _"Is there a specific time period, filter, or subset?"_
    - _"Should I aggregate or summarise (e.g. sum by category, average by year)?"_

13. **For anecdotal data — ask:**
    - _"What are the categories or labels?"_
    - _"Can you give me rough numbers, percentages, or relative sizes?"_ (e.g. "Roads is about twice as big as bridges")
    - _"Is this based on a specific year, project, or experience?"_ (for the source attribution)
    - If the user can only describe proportions qualitatively (e.g. "most of the budget goes to roads"), suggest approximate splits and confirm: _"Would something like 55% Roads, 25% Bridges, 20% Other feel right?"_

14. **For both — confirm the visual:**
    - _"Here's what I'll put on the chart: [list the labels and values]. Does that look right?"_
    - _"Should I add a source line? Something like 'Source: FY24 Asset Register' or 'Indicative estimates, March 2026'?"_

#### Step C: Map Data to Chart

Once the data and chart type are confirmed:

- **Structured data**: Read the file, extract values, calculate SVG coordinates (pixel positions, arc lengths, path points) proportional to the data range. Ensure axis labels, grid lines, and tooltips reflect actual values.
- **Anecdotal data**: Convert the user's estimates into concrete numbers if they provided percentages/proportions. Map to SVG coordinates the same way. Use softer language in labels where appropriate ("~45%" or "Est. $2.3M").
- **Multiple charts on one slide**: If a slide needs several charts (e.g. a dashboard), confirm layout (side by side, stacked, grid) before building.

#### Chart Source Attribution Rules

Every chart MUST include a source attribution, either:
- **Below the chart**: `<text class="chart-axis-label" x="..." y="[bottom]" text-anchor="start">Source: [attribution]</text>`
- **In a slide footnote**: Small text at the bottom of the slide content area

| Data Source | Attribution Format |
|---|---|
| File / database | "Source: [File name or system], [date/period]" |
| Anecdotal (from user) | "Source: [User's role/name] estimates, [month year]" |
| Anecdotal (general) | "Indicative only — based on operational experience" |
| Published / external | "Source: [Publication/org], [year]" |
| Mixed | Cite each series separately in a footnote |

### Default Narrative Structure (for "Presentation" type)

The default **Presentation** type uses the Situation → Complication → Resolution arc, structured as three acts with a bold close:

| Section | data-section | Act | Purpose | Format | Content Limit |
|---------|-------------|-----|---------|--------|---------------|
| **Title** | `title` | — | Orient the audience, establish credibility | Logo + bold heading + green subtitle + audience line | 8 words on h1. No agenda. |
| **Situation** | `situation` | 1 (Hook) | Earn the next 20 minutes. Open with tension. | Single provocative statement, question, or big stat | One sentence. No name/title/agenda. |
| **Complication** | `complication` | 2 (Meat) | Introduce the tension — the "but" | Question slide or single stat on dark background | One question or one number. Speaker explains. |
| **Evidence** | `evidence` | 2 (Meat) | Prove the complication is real with data | Single chart, single metric, or full bleed image | One chart or one image. Source attribution. |
| **Decisions** | `decisions` | 3 (Payoff) | Deliver the answer — the "therefore" | Split layout or single bold statement | 10 words max. Speaker delivers substance. |
| **Recommendation** | `recommendation` | 3 (Payoff) | What the audience should DO | Three cards (max) or single recommendation | Three items, each 5 words or fewer. |
| **Contributions** | `recommendation` | Close | What we accomplished. Stays visible during Q&A. | Numbered list. Never "Thank You" or "Questions?" | 3 items. Echoes the opening hook. |

**Footer nav labels**: TITLE | SITUATION | COMPLICATION | EVIDENCE | DECISIONS | RECOMMENDATION

**Key structural rule**: slides within the same act share a `data-section` value. Multiple slides can belong to the same section — the footer nav highlights the act, not the individual slide.

Other types have their own section structures — see `references/presentation-types.md` for the full mapping.

---

## File Structure

A SAS presentation consists of:

```
presentation-folder/
├── presentation.html    # Main presentation file
├── styles.css           # Custom theme styles
└── assets/              # Images (PNG, JPG, SVG)
    └── [slide-images]-blue.png / -green.png
```

> **Note:** SAS logos are loaded from the Webflow CDN — no local logo files needed.

## Logo Assets (CDN)

SAS-AM logos are hosted on the Webflow CDN. **No local logo files are required.**

| Mode | URL | Description |
|------|-----|-------------|
| **Light mode** | `https://cdn.prod.website-files.com/653497186047abfdf821b2fc/69a77a2f0e9f223c5f196bd3_sas-logo.jpg` | Full SAS wordmark (dual arrows + "SAS" text, dark navy on white) |
| **Dark mode** | `https://cdn.prod.website-files.com/653497186047abfdf821b2fc/69a777cb2f01269a5c7f073e_sas-logo-lightmode.png` | Green arrow brandmark on transparent background |

### Logo Behaviour

The CSS automatically switches logos based on the current theme:
- **Light mode**: Displays elements with class `logo-light` (full wordmark)
- **Dark mode**: Displays elements with class `logo-dark` (green brandmark)

### Usage in HTML

```html
<img src="https://cdn.prod.website-files.com/653497186047abfdf821b2fc/69a77a2f0e9f223c5f196bd3_sas-logo.jpg" alt="SAS Logo" class="title-logo logo-light">
<img src="https://cdn.prod.website-files.com/653497186047abfdf821b2fc/69a777cb2f01269a5c7f073e_sas-logo-lightmode.png" alt="SAS Logo" class="title-logo logo-dark">
```

No local asset copying needed — logos load directly from CDN.

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
  <link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@300;400;500;600;700&family=Source+Code+Pro:wght@400;600&display=swap" rel="stylesheet">

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

All types inherit this base configuration. The Notes plugin is always included for speaker view (press S to open).

```html
<!-- CDN scripts (before </body>) -->
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js"></script>
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/plugin/notes/notes.js"></script>
```

```javascript
Reveal.initialize({
  plugins: [RevealNotes],
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

Four states: `light` (default), `dark`, `share` (codec friendly mode for Teams / Zoom screen sharing), and `system` (follows OS preference). Storage key: `marcov-presentation-theme`. The theme toggle button cycles light → dark → share → light.

The `data-theme` attribute is applied to `<html>`, `<body>`, and `.reveal-viewport`. All colours use CSS custom properties.

### Sharing over Microsoft Teams or Zoom

Screen sharing over Teams and Zoom compresses the slide stream with 4:2:0 chroma subsampling and adaptive bitrate. The common symptoms are washed out greens, faded text, invisible card borders, banded gradients, and muted greys that disappear against white.

**Before joining a call, switch the deck to share mode.** Either:

- Click the theme toggle until the broadcast icon shows, or
- Open the deck with `?mode=share` appended to the URL (persists via localStorage)

Share mode applies the following codec survival tactics:

- Off white background (`#fafbfc`) instead of pure white — stops saturated colour from bleeding across chroma block boundaries
- Darker, more saturated accent green (`#4F9A1E`) used for fills only, never text
- Card borders thickened from 1px to 2px and darkened from 15 percent alpha to 45 percent
- Shadows doubled in opacity so they survive compression
- Decorative binary rain background hidden (at 3 percent alpha it becomes noise)
- Full bleed gradient overlays replaced with solid scrims (gradients band heavily after quantisation)
- Body font weight bumped from 400 to 500
- Subpixel antialiasing disabled (chroma subsampling destroys it anyway)
- Reveal slide canvas shrunk from 1920 by 1080 to 1440 by 810 so text scales up larger on the receiver's screen

**Additional call settings to check:**

- **Microsoft Teams:** untick *Include computer sound* unless playing video. Do NOT enable *Optimize for video clips* for slide only decks (that profile crushes still frame colour fidelity). Share the browser window, not the full screen, when possible.
- **Zoom:** leave *Optimize for video* OFF unless playing embedded video. Use *Share sound* only if required.
- Share a windowed 1080p browser rather than the full desktop — the encoder does not have to downscale.
- Dark mode alone (without share) is also more codec friendly than pure light mode for slide only content (white text on dark navy survives chroma subsampling better than dark text on white).

### Footer Navigation

- Section map built once on Reveal `ready` event
- Active section highlighted with accent colour
- Click any section to jump to its first slide
- Keyboard accessible: `tabindex="0"`, `role="button"`, Enter/Space activation
- Footer positioned `fixed` outside Reveal container

---

## Slide Types

### 1. Title Slide

Bold heading, green subtitle, audience line. No agenda.

```html
<section id="title" class="title-slide" data-section="title">
  <div class="title-content">
    <img src="https://cdn.prod.website-files.com/653497186047abfdf821b2fc/69a77a2f0e9f223c5f196bd3_sas-logo.jpg" alt="SAS Logo" class="title-logo logo-light">
    <img src="https://cdn.prod.website-files.com/653497186047abfdf821b2fc/69a777cb2f01269a5c7f073e_sas-logo-lightmode.png" alt="SAS Logo" class="title-logo logo-dark">
    <h1>Roster & Payroll Risk</h1>
    <h2>Current State, Exposure & Transition Roadmap</h2>
    <p class="author">Prepared for RS Leadership — GM, Directors & Depot Managers</p>
    <p class="tagline">At SAS-AM we help organisations understand their strengths and weaknesses...</p>
  </div>
  <aside class="notes">
    Do NOT introduce yourself here. Let the title speak. Move to the hook immediately.
    Timing: ~15 seconds on the title before advancing.
  </aside>
</section>
```

**Typography:**
- `<h1>`: 96px, weight 700, text-primary colour, letter-spacing -1px
- `<h2>`: 40px, weight 500, accent colour (SAS Green)
- `.author`: 24px, text-muted colour

---

### 2. Standard Content Slide

Two-column split layout. Content left, visual right. 10 words max on the content side.

```html
<section id="unique-id" data-section="situation">
  <div class="slide-layout with-image">
    <img src="[CDN_LOGO_LIGHT]" alt="SAS Logo" class="slide-logo logo-light">
    <img src="[CDN_LOGO_DARK]" alt="SAS Logo" class="slide-logo logo-dark">
    <div class="slide-header">
      <span class="section-tag">SITUATION</span>
    </div>
    <div class="slide-body split">
      <div class="slide-content">
        <h2 class="slide-title">REFRAMING ASSET DATA</h2>
        <p class="slide-subtitle">Your EAM Is A Filing Cabinet</p>
      </div>
      <div class="slide-image">
        <img src="assets/visual-blue.png" alt="Description" class="logo-light">
        <img src="assets/visual-green.png" alt="Description" class="logo-dark">
      </div>
    </div>
  </div>
  <aside class="notes">
    Transition: "Let me show you what we found..."
    Key stat: [stat to deliver verbally]
    Timing: ~3 minutes
  </aside>
</section>
```

**Typography:**
- `.section-tag`: 14px, weight 600, uppercase, letter-spacing 2px, accent colour
- `.slide-title`: 72px, weight 700, uppercase, letter-spacing -1px
- `.slide-subtitle`: 36px, weight 300, text-secondary colour

---

### 3. Question Slide

Provocative question, centred. The slide teases; the speaker tells. Use for complication slides.

```html
<section id="complication-1" class="slide-question" data-section="complication">
  <div class="question-text">What happens when <em>every sensor reading</em> is a missed opportunity?</div>
  <aside class="notes">
    Transition: "But here is where it breaks down..."
    Pause after showing the question. Let the audience read it. Then answer verbally.
    Timing: ~3 minutes.
  </aside>
</section>
```

**Typography:**
- `.question-text`: 72px, weight 700, text-primary colour
- `em` within question: accent colour (SAS Green), no italic

---

### 4. Full Bleed Image Slide

Single powerful image filling the screen. Optional text overlay at bottom.

```html
<section id="fullbleed-1" class="slide-fullbleed" data-section="evidence">
  <img src="assets/site-visit.jpg" alt="Control room at 2am during the incident">
  <div class="fullbleed-overlay">
    <h2>The Night It Failed</h2>
    <p>Depot 3, February 2024</p>
  </div>
  <aside class="notes">
    Let this image sit for 5 seconds before speaking.
    Tell the story of what happened that night — sensory detail.
    Timing: ~2 minutes.
  </aside>
</section>
```

---

### 5. Breather Slide (Dark Blank)

Pure dark background. All focus returns to the speaker. Use between acts.

```html
<section id="breather-1" class="slide-breather" data-section="evidence">
  <div class="breather-text">So what changed?</div>
  <aside class="notes">
    This is a pause slide. Slow down. Make eye contact.
    Deliver the transition to your resolution verbally.
    Timing: ~30 seconds of silence before moving on.
  </aside>
</section>
```

---

### 6. Stat / Single Number Slide

One bold number with context. Use for impact data points.

```html
<section id="stat-1" class="slide-stat" data-section="evidence">
  <div>
    <div class="stat-number">$4.2M</div>
    <div class="stat-label">Preventable Cost in 2023</div>
  </div>
  <aside class="notes">
    Let the number land. Pause 3 seconds.
    Then explain: "That is what a single undetected fault cost across the fleet last year."
    Timing: ~1 minute.
  </aside>
</section>
```

---

### 7. Contributions Slide (Final)

What you accomplished. Stays visible during Q&A. Never "Thank You" or "Questions?"

```html
<section id="closing" class="slide-contributions" data-section="recommendation">
  <h2>What We Covered</h2>
  <ol class="contributions-list">
    <li>Identified $4.2M in preventable roster exposure</li>
    <li>Mapped three high risk transition points</li>
    <li>Proposed a phased remediation roadmap</li>
  </ol>
  <div class="closing-branding" style="margin-top: auto;">
    <img src="[CDN_LOGO_LIGHT]" alt="SAS Logo" class="closing-logo logo-light">
    <img src="[CDN_LOGO_DARK]" alt="SAS Logo" class="closing-logo logo-dark">
  </div>
  <aside class="notes">
    Close with a salute, not thanks: "And with that, I will conclude."
    This slide stays up during Q&A. The audience will stare at it for 10+ minutes.
    If you lose your place during Q&A, repeat your last point — it acts as a memory jogger.
  </aside>
</section>
```

---

### 8. Standard Content Slide with SVG Diagram

For conceptual diagrams, use inline SVG with CSS variables for theme support.

```html
<section id="concept" data-section="decisions">
  <div class="slide-layout">
    <div class="slide-header">
      <span class="section-tag">DECISIONS</span>
    </div>
    <div class="slide-body split">
      <div class="slide-content">
        <h2 class="slide-title">EDGE FEDERATED ML</h2>
        <p class="slide-subtitle">Intelligence On The Asset</p>
      </div>
      <div class="slide-image">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="600" height="400">
          <rect fill="var(--bg-tertiary)" stroke="var(--card-border)" .../>
          <circle fill="var(--accent)" .../>
          <text fill="var(--text-primary)" font-family="Arial, sans-serif">...</text>
        </svg>
      </div>
    </div>
  </div>
  <aside class="notes">
    Walk through the diagram verbally. Do not turn to look at the screen.
    Timing: ~3 minutes.
  </aside>
</section>
```

---

### 9. Step Animation Slide (Fragment Transitions)

Progressive reveal using Reveal.js fragments.

```html
<section id="process" data-section="decisions">
  <div class="slide-layout">
    <div class="slide-header">
      <span class="section-tag">DECISIONS</span>
    </div>
    <div class="slide-body split">
      <div class="slide-content">
        <h2 class="slide-title">THREE PHASES</h2>
      </div>
      <div class="slide-image diagram-container">
        <div class="federated-diagram step-1 fragment fade-out" data-fragment-index="1">
          <img src="assets/step-1-blue.png" class="logo-light">
          <img src="assets/step-1-green.png" class="logo-dark">
        </div>
        <div class="federated-diagram step-2 fragment fade-in-then-out" data-fragment-index="1">
          <img src="assets/step-2-blue.png" class="logo-light">
          <img src="assets/step-2-green.png" class="logo-dark">
        </div>
        <div class="federated-diagram step-3 fragment fade-in" data-fragment-index="2">
          <img src="assets/step-3-blue.png" class="logo-light">
          <img src="assets/step-3-green.png" class="logo-dark">
        </div>
      </div>
    </div>
  </div>
  <aside class="notes">
    Advance fragments with arrow keys. Each step builds on the last.
    Timing: ~1 minute per step.
  </aside>
</section>
```

---

### 10. Closing/CTA Slide (Alternative to Contributions)

Call to action with QR code. Use when the presentation needs a direct next step rather than a summary.

```html
<section id="closing" data-section="recommendation">
  <div class="slide-layout closing">
    <div class="slide-header">
      <span class="section-tag">RECOMMENDATION</span>
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
        <img src="[CDN_LOGO_LIGHT]" alt="SAS Logo" class="closing-logo logo-light">
        <img src="[CDN_LOGO_DARK]" alt="SAS Logo" class="closing-logo logo-dark">
        <p class="closing-search"><i class="fas fa-search"></i> EDGE AI ASSET MANAGEMENT</p>
      </div>
    </div>
  </div>
  <aside class="notes">
    Close with a salute: "And with that, I will conclude."
    Keep this slide up during Q&A.
  </aside>
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
| Title Slide h1 | 96px | 700 | text-primary | line-height 1.1, letter-spacing -1px |
| Title Slide h2 | 40px | 500 | accent | — |
| Author | 24px | 400 | text-muted | — |
| Section Tag | 14px | 600 | accent | uppercase, letter-spacing 2px |
| Slide Title | 72px | 700 | text-primary | uppercase, letter-spacing -1px |
| Slide Subtitle | 36px | 300 | text-secondary | line-height 1.4 |
| Question Text | 72px | 700 | text-primary | em = accent colour |
| Stat Number | 160px | 700 | accent | line-height 1 |
| Stat Label | 36px | 300 | text-secondary | uppercase, letter-spacing 3px |
| Footer Nav | 13px | 700 | text-secondary | uppercase, letter-spacing 2px |

**Font Families:**
- Source Sans Pro (300, 400, 500, 600, 700 weights) — body text, headings
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
| Question Slide | `.slide-question` | Provocative question, centred. Tease with slide, tell with voice. |
| Full Bleed Image | `.slide-fullbleed` | Single powerful image, edge to edge |
| Breather (Dark Blank) | `.slide-breather` | Pure dark background, focus returns to speaker |
| Stat / Single Number | `.slide-stat` | One bold number with context label |
| Contributions (Final) | `.slide-contributions` + `.contributions-list` | What was accomplished. Stays visible during Q&A. |
| Card | `.card` | Content container with border and shadow |
| Card Grid | `.card-grid` + `.card-grid-2/3/4` | Responsive grid of cards (3 max per slide) |
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

For additional chart types or custom visualisation components, source them via the `21st` CLI tool (see `~/.claude/CLAUDE.md` § UI Component Sourcing). All fetched components must inherit the CSS variable theming system and meet WCAG 2.1 AA accessibility standards before integration.

---

## Workflow

### Step 1: Discovery Interview

Conduct the discovery interview to:
1. **Identify the presentation type** using Phase 1 questions (purpose, audience, slide count, content format)
2. **Confirm the type** with the user
3. **Get the one sentence summary** (Phase 2, question 5) — this is the single most important discovery question
4. **Get the three supporting points** (Phase 2, question 6) — these become the content sections
5. **Get the hook** (Phase 2, question 7) — this becomes the opening slide
6. **Get a sensory moment** (Phase 2, question 8) — this feeds into speaker notes
7. **Get the ask** (Phase 2, question 9) — this becomes the close
8. **Gather remaining details** (delivery context, branding, assets, outline)
9. **Plan data visualisations** using Phase 3 questions — for each data-driven slide, identify chart type, data source (file vs anecdotal), and confirm values before building

### Step 2: Create Presentation Structure

1. Create a new directory for the presentation
2. Copy `base-styles.css` from references as `styles.css`
3. Create `presentation.html` using the scaffold template — adapt the sections and footer nav items to match the selected presentation type
4. Create `assets/` directory for slide images (logos load from CDN automatically)

### Step 3: Build Content Slides

Work through slides incrementally:
1. **Title slide** — bold heading (96px/700), green subtitle, audience line. No agenda.
2. **Hook/Situation slide** — the surprising opening. Question slide, stat slide, or single statement.
3. **Content slides** — one per key point (max 3). Choose slide type per the Slide Selection Guide. Enforce 10 word limit.
4. **Breather slides** — insert dark blank slides between acts for emphasis moments.
5. **Contributions/Close** — echo the opening hook. List what was accomplished.
6. For each slide, write **speaker notes** in `<aside class="notes">`:
   - Transition phrase into this slide
   - One key stat or story beat to deliver verbally
   - Approximate timing
7. Update footer nav items to match the sections
8. Apply any type-specific Reveal.js overrides
9. Include dual-theme images where needed
10. Add charts and data visualisations from `references/chart-components.html` where needed
11. For UI components or chart types not in the reference library, use the `21st` CLI outside Claude Code

### Step 4: Word Count Audit

Before finalising, audit every slide against the 10 word rule:
1. Count visible text elements per slide (headings, subtitles, stat labels, card headings)
2. If any slide exceeds 10 words, move content to speaker notes
3. Check that no bullet point lists exist anywhere in the deck
4. Verify the dead laptop test: could this talk be delivered without the slides?

### Step 5: Review and Refine

1. Test navigation in browser
2. Verify light/dark mode toggle
3. Check all images load correctly
4. Ensure footer navigation tracks correctly
5. Test speaker view (press S) — verify notes display correctly
6. Run the full pre-delivery checklist (see below)

### Step 6: Export (Optional)

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

### The 10 Word Rule

Every slide — including titles, subtitles, questions, and stat labels — must contain **10 words or fewer** of visible text. Speaker notes carry the substance. The slide earns curiosity; your voice delivers the reward.

**Counting words**: count only visible text elements (h1, h2, subtitle, stat label, card headings). Do not count section tags, logos, or speaker notes. Card grids with 3 items: each card heading counts towards the total, so keep each to 2-3 words.

### Headlines (Slide Titles)

- **Format**: ALL CAPS, punchy, memorable
- **Length**: 2-5 words
- **Style**: Action oriented or provocative
- **Examples**:
  - "REFRAMING ASSET DATA"
  - "SILOED FAILURES"
  - "PREDICTABLE RISK"

### Subtitles

- **Format**: Title Case, explanatory
- **Length**: One sentence, **10 words maximum** (combined with headline)
- **Style**: Expands on the headline with a specific insight
- **Examples**:
  - "Your EAM Is A Filing Cabinet"
  - "Every Sensor Reading Is A Missed Opportunity"

### Section Tags

- **Format**: ALL CAPS
- **Default options**: TITLE, SITUATION, COMPLICATION, EVIDENCE, DECISIONS, RECOMMENDATION

### What NOT to Put on a Slide

| Banned | Why | Alternative |
|--------|-----|-------------|
| Bullet point lists | Audience reads instead of listens | Single statement, card grid (3 max), or image |
| Full sentences | Slide becomes a teleprompter | Compress to 3-5 words. Move detail to speaker notes. |
| Your name / title | Weak opening. Forgettable. | Introduce yourself verbally after the hook, if at all. |
| Agenda slides | Kill momentum before you start | Jump straight to the hook. |
| "Thank You" or "Questions?" | Weak close. Implies audience was trapped. | Contributions slide. Salute: "And with that, I will conclude." |
| White blank slides | Look broken | Dark breather slides (`.slide-breather`) |
| Animations without meaning | Subtract attention | Only use fade/dissolve. Fragment reveals for progressive build. |
| Stock images without purpose | Generic and forgettable | Use your own photos (site visits, equipment, real moments). If stock, apply a colour overlay. |

### Slide Selection Guide

When building each slide, choose the type based on what the slide needs to achieve:

| What you need | Slide type | CSS class |
|--------------|------------|-----------|
| Open with tension | Question slide | `.slide-question` |
| Show a single powerful image | Full bleed image | `.slide-fullbleed` |
| Land a shocking number | Stat slide | `.slide-stat` |
| Pause between acts | Breather (dark blank) | `.slide-breather` |
| Explain with a visual | Standard split layout | `.slide-layout .split` |
| Show three recommendations | Card grid | `.card-grid-3` |
| Close the talk | Contributions | `.slide-contributions` |
| Progressive reveal | Fragment transitions | Reveal.js fragments |
| Direct CTA with QR | Closing/CTA | `.slide-layout.closing` |

---

## Responsive Considerations

```css
@media screen and (max-width: 1400px) {
  .slide-title { font-size: 56px; }
  .slide-subtitle { font-size: 28px; }
  .title-slide h1 { font-size: 72px; }
  .title-slide h2 { font-size: 32px; }
  .slide-question .question-text { font-size: 56px; }
  .slide-stat .stat-number { font-size: 120px; }
  .ref-title { font-size: 44px; }
  .ref-subtitle { font-size: 24px; }
  .card-grid-3 { grid-template-columns: repeat(2, 1fr); }
}

@media screen and (max-width: 1000px) {
  .slide-body.split { flex-direction: column; }
  .slide-image { max-height: 300px; }
  .title-slide h1 { font-size: 56px; }
  .slide-question .question-text { font-size: 40px; }
  .slide-stat .stat-number { font-size: 88px; }
  .nav-items { gap: 20px; }
  .nav-item { font-size: 11px; }
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

### Presentation Philosophy
- [ ] Entire talk summarisable in one sentence (one idea)
- [ ] Three key points or fewer
- [ ] Every slide has 10 words or fewer of visible text
- [ ] No bullet point lists anywhere in the deck
- [ ] First 30 seconds do not contain name, title, or agenda
- [ ] Closing slide echoes the opening hook
- [ ] Final slide is Contributions (not "Thank You" or "Questions?")
- [ ] Dead laptop test passes — could deliver this without slides

### Speaker Notes
- [ ] Every slide has `<aside class="notes">` with content
- [ ] Notes contain transition phrase (not a full script)
- [ ] Notes contain one key stat or story beat
- [ ] Notes contain approximate timing
- [ ] RevealNotes plugin loaded and `plugins: [RevealNotes]` in config
- [ ] Speaker view opens correctly (press S)

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

### Data Visualisations
- [ ] Chart type appropriate for the data story (checked against decision tree)
- [ ] Data source identified (structured file, anecdotal, or mixed)
- [ ] Data values confirmed with user before building
- [ ] All charts have `role="img"` and `aria-label`
- [ ] All charts use `.chart-interactive` for hover effects
- [ ] Chart colours use `--chart-1` through `--chart-6` (no hardcoded values)
- [ ] Tooltips present (SVG fallback or JS-enhanced)
- [ ] Source attribution present on every chart
- [ ] Anecdotal data clearly labelled as estimated/indicative
- [ ] Axis labels, legends, and values are accurate and readable

### Content
- [ ] Discovery interview completed (Phases 1, 2, and 3)
- [ ] Presentation type identified and confirmed
- [ ] Section structure follows the type definition
- [ ] Tone matches the type (formal, punchy, narrative, etc.)
- [ ] At least one story with sensory detail
- [ ] Logic and emotion alternate throughout (data → story → data)
- [ ] SAS-AM tagline included on at least one slide
