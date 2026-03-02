---
name: sas-presentation
description: Create polished SAS-AM branded Reveal.js presentations. Use when the user asks to create slides, a presentation, a deck, or a slideshow. Implements SAS brand guidelines with light/dark mode, narrative structure, and professional layouts. Generates standalone HTML + CSS with no build step required.
---

# SAS-AM Presentation Skill

Create professional HTML presentations using Reveal.js with SAS-AM brand guidelines. The output is a standalone HTML file that can be opened directly in any browser, shared via USB, or hosted on any static file server.

## Overview

This skill creates presentations following the SAS-AM communication style, which features:

- **SAS Brand Colours**: SAS Blue (#002244) and SAS Green (#69BE28)
- **Light/Dark Mode Toggle**: Built-in theme switching with localStorage persistence
- **Narrative Structure**: A proven 7-section storytelling arc
- **Professional Typography**: Source Sans Pro font family
- **Static Footer Navigation**: Section progress indicator with theme toggle
- **Dual-Theme Assets**: Support for light/dark image variants
- **Subtle Animations**: Binary background, animated SVG diagrams

## Discovery Process (CRITICAL)

**Before creating any presentation, you MUST conduct a discovery interview to understand:**

### Questions to Ask

1. **Topic & Purpose**
   - What is the presentation about?
   - What is the key message you want the audience to remember?
   - Is there a specific call-to-action?

2. **Audience**
   - Who is the audience? (executives, technical team, clients, conference)
   - What do they already know about this topic?
   - What concerns or objections might they have?

3. **Context**
   - Where will this be presented? (conference, boardroom, webinar, USB for sharing)
   - How much time do you have? (affects number of slides)
   - Will you be presenting live or is it for self-navigation?

4. **Branding**
   - Should we use SAS-AM branding (default) or a client's brand?
   - If client branding, what are their brand colours?

5. **Visual Assets**
   - Do you have specific images, diagrams, or visualisations to include?
   - Should I create conceptual SVG diagrams?
   - Do you need a QR code for the closing slide?

6. **Content Outline**
   - Do you have existing content, bullet points, or a rough outline?
   - What are the key sections or topics to cover?

### Suggested Narrative Structure

Guide users toward this proven 7-section structure (adjustable based on content):

| Section | Purpose | Example |
|---------|---------|---------|
| **OPENING** | Hook the audience, reframe the problem | "Your Million-Dollar EAM System Might Just Be A Very Expensive Filing Cabinet" |
| **THE CONTEXT** | Establish the current situation | "Siloed failures - one truck breaks down but the fleet learns nothing" |
| **THE PROBLEM** | Identify specific pain points | "Cloud analytics can't make split-second decisions" |
| **THE SOLUTION** | Present your answer | "Edge Federated Machine Learning" |
| **THE IMPLEMENTATION** | Show how it works practically | "Start small. One asset class. One location." |
| **THE FUTURE** | Vision and possibilities | "Maintenance schedules that write themselves" |
| **THE CONNECTION** | Call to action | "Ready to make your assets intelligent?" |

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

### HTML Document Structure

```html
<!DOCTYPE html>
<html lang="en-AU" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Presentation Title | SAS-AM</title>

  <!-- Reveal.js -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css">

  <!-- Font Awesome for icons -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@300;400;600;700&display=swap" rel="stylesheet">

  <!-- Custom Styles -->
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <div class="presentation-wrapper">
    <!-- Subtle binary background -->
    <div class="binary-background" id="binaryBg"></div>

    <!-- Reveal.js container -->
    <div class="reveal">
      <div class="slides">
        <!-- Slides go here -->
      </div>
    </div>

    <!-- Static footer (outside reveal.js) -->
    <footer class="static-footer">
      <div class="footer-content">
        <div class="nav-items">
          <span class="nav-item" data-section="opening">OPENING</span>
          <span class="nav-item" data-section="context">THE CONTEXT</span>
          <!-- ... more sections ... -->
        </div>
        <div class="footer-controls">
          <button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle light/dark mode">
            <i class="fas fa-sun light-icon"></i>
            <i class="fas fa-moon dark-icon"></i>
          </button>
        </div>
      </div>
    </footer>
  </div>

  <!-- Reveal.js -->
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js"></script>

  <!-- Theme & Navigation Scripts -->
  <script>
    // Theme management
    const STORAGE_KEY = 'sas-presentation-theme';

    function getSystemTheme() {
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }

    function setTheme(theme) {
      const resolved = theme === 'system' ? getSystemTheme() : theme;
      document.documentElement.setAttribute('data-theme', resolved);
      document.body.setAttribute('data-theme', resolved);
      const viewport = document.querySelector('.reveal-viewport');
      if (viewport) viewport.setAttribute('data-theme', resolved);
      localStorage.setItem(STORAGE_KEY, theme);
    }

    function toggleTheme() {
      const current = document.documentElement.getAttribute('data-theme') || 'light';
      setTheme(current === 'light' ? 'dark' : 'light');
    }

    // Initialize theme
    setTheme(localStorage.getItem(STORAGE_KEY) || 'light');

    // Reveal.js initialization
    Reveal.initialize({
      hash: true,
      slideNumber: 'c/t',
      showSlideNumber: 'speaker',
      transition: 'slide',
      transitionSpeed: 'default',
      backgroundTransition: 'fade',
      center: false,
      width: 1920,
      height: 1080,
      margin: 0,
      minScale: 0.2,
      maxScale: 2.0,
    });

    // Update footer navigation
    function updateNavigation() {
      const currentSlide = Reveal.getCurrentSlide();
      const currentSection = currentSlide?.getAttribute('data-section');
      document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.toggle('active', item.getAttribute('data-section') === currentSection);
      });
    }
    Reveal.on('slidechanged', updateNavigation);
    updateNavigation();

    // Binary background animation
    (function() {
      const container = document.getElementById('binaryBg');
      for (let i = 0; i < 50; i++) {
        const column = document.createElement('div');
        column.className = 'binary-column';
        let str = '';
        for (let j = 0; j < 150; j++) {
          str += Math.random() > 0.5 ? '1' : '0';
          if (j < 149) str += '<br>';
        }
        column.innerHTML = str;
        column.style.left = (i * 2) + '%';
        const duration = 45 + Math.random() * 30;
        column.style.animationDuration = duration + 's';
        column.style.animationDelay = (Math.random() * -duration) + 's';
        container.appendChild(column);
      }
    })();
  </script>
</body>
</html>
```

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

**Font Family:** Source Sans Pro (300, 400, 600, 700 weights)

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

## Workflow

### Step 1: Discovery Interview

Conduct the discovery interview to understand:
- Topic, audience, context
- Key message and call-to-action
- Content outline
- Visual requirements

### Step 2: Create Presentation Structure

1. Create a new directory for the presentation
2. Copy `base-styles.css` from references as `styles.css`
3. Create `presentation.html` with the scaffold
4. Create `assets/` directory

### Step 3: Build Content Slides

Work through slides incrementally:
1. Create title slide
2. Build out each section following the narrative arc
3. Add section-appropriate `data-section` attributes
4. Include dual-theme images where needed

### Step 4: Review and Refine

1. Test navigation in browser
2. Verify light/dark mode toggle
3. Check all images load correctly
4. Ensure footer navigation tracks correctly

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
}

@media screen and (max-width: 1000px) {
  .slide-body.split { flex-direction: column; }
  .slide-image { max-height: 300px; }
  .nav-items { gap: 15px; }
  .nav-item { font-size: 10px; }
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

## Accessibility

- **Language**: `lang="en-AU"` on `<html>`
- **Alt text**: All images must have descriptive alt text
- **ARIA labels**: Theme toggle and interactive elements
- **Reduced motion**: Respect `prefers-reduced-motion`

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Dependencies (CDN)

All loaded from CDN - no npm install required:

- **Reveal.js 5.1.0**: Presentation framework
- **Font Awesome 6.5.1**: Icons
- **Google Fonts**: Source Sans Pro

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

## Checklist

Before delivering a presentation, verify:

- [ ] Discovery interview completed
- [ ] Narrative structure follows 7-section arc
- [ ] All slides have unique IDs
- [ ] All slides have `data-section` attributes
- [ ] Light/dark mode toggle works
- [ ] All images have alt text
- [ ] Footer navigation updates correctly
- [ ] PDF export works (if required)
- [ ] Australian English spelling used
