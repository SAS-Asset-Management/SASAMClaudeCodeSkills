# Slide Recipes — HTML Patterns per Slide Type

Copy ready HTML for each slide type. All patterns are Reveal.js `<section>` based, brand compliant (SAS Blue `#002244`, SAS Green `#69BE28`), flat design (no box shadows), and carry `<aside class="notes">` speaker notes. For the zero dependency single file mode, the same markup goes inside `.deck-stage` with `class="slide"` instead of a bare `<section>` (see `references/rendering-modes.md`).

Quick chooser (also in `SKILL.md` § Slide Selection Guide):

| What you need | Recipe | CSS class |
|--------------|--------|-----------|
| Orient the audience | 1. Title | `.title-slide` |
| Explain with a visual | 2. Standard content | `.slide-layout .split` |
| Open with tension | 3. Question | `.slide-question` |
| One powerful image | 4. Full bleed image | `.slide-fullbleed` |
| Pause between acts | 5. Breather (dark blank) | `.slide-breather` |
| Land a shocking number | 6. Stat / single number | `.slide-stat` |
| Close the talk | 7. Contributions | `.slide-contributions` |
| Explain with a diagram | 8. Content + SVG diagram | `.slide-layout .split` |
| Progressive reveal | 9. Step animation | Reveal fragments |
| Direct CTA with QR | 10. Closing / CTA | `.slide-layout.closing` |

---

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
- `.slide-subtitle`: 36px, weight 600, text-secondary colour (never 300 — see the compression-safe typography rule in `SKILL.md`)

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
