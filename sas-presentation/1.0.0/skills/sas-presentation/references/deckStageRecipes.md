# deck-stage v2 — engine guide + template catalogue

This is the reference for the **default** SAS-AM presentation engine (v2). It replaces the Reveal.js build for new decks. Reveal.js stays available as a legacy path (see `rendering-modes.md`).

Everything here is standalone: open the HTML in any browser, no build step, no CDN required for the engine (only the Google Fonts link, which you may inline for a fully offline deck).

## What ships with a v2 deck

```
presentation-folder/
├── presentation.html          # your deck (from deckStageScaffold.html)
├── engine/
│   ├── deckStage.js           # the <deck-stage> web component (copy verbatim)
│   ├── deckChrome.css         # theme tokens, entrance animations, chrome
│   ├── deckChrome.js          # theme toggle, count-ups, nav rail, cameo
│   └── serveDeck.py           # local server for live delivery (camera)
└── assets/
    ├── sasLogoPrimary.svg     # navy wordmark (for light slides)
    └── sasLogoReversed.svg    # white/green wordmark (for dark slides)
```

Copy `engine/` and `assets/` from `references/` into the deck folder. For a **single-file offline** deck, inline `deckStage.js` and `deckChrome.js` inside `<script>` tags, inline `deckChrome.css` inside `<style>`, and base64-embed the two SVGs (see `logos.md`).

## The engine in one paragraph

`<deck-stage width="1920" height="1080">` wraps your slides — each slide is a direct-child `<section>` with inline styles. The component renders one slide at a time on a fixed 1920×1080 canvas and scales the whole canvas with `transform: scale()` to fit the viewport, letterboxing on narrow screens (it never reflows slide content). It handles ←/→, PgUp/PgDn, Space, Home/End, number keys, touch tap-to-advance, `R` to reset, a fade-out slide counter overlay, and — via `@media print` — lays every slide out as its own page so Chrome's Print → Save as PDF produces a clean one-page-per-slide export. Author at the fixed size; never add responsive rules that restack slide content.

Set `no-rail` on `<deck-stage>` for delivery — it hides the engine's built-in *authoring thumbnail rail* (an editing aid). Navigation for the audience is the icon rail (below).

## Per-slide attributes

| Attribute | Purpose |
|---|---|
| `data-label` | Slide name — feeds the icon nav rail pill and the engine's slide labels. |
| `data-nav-icon` | Rail glyph key: `home list tag bookmark help target grid bar trend pie split image quote columns route crosshair book flag`. Defaults to `bookmark`. |
| `data-speaker-notes` | Presenter note for this slide. The engine posts `{slideIndexChanged}` to any parent window (speaker-view host) and exposes it on the `slidechange` event. |
| `data-deck-skip` | Omit this slide from navigation and print (kept in source). |

## Entrance animations (deckChrome.css)

Add a class to any element; it animates when its slide becomes active, and is gated on `prefers-reduced-motion`. Stagger with `d1`…`d8`.

`a-up` (rise + fade) · `a-scale` · `a-blur` · `a-fade` · `grow-x` / `grow-y` (bars, transform-origin left/bottom) · `draw` (SVG line draw, set `--len` and `stroke-dasharray` to the path length).

Disable all motion for a deck with `data-motion="off"` on `<html>` or `<body>`.

## Count-up numbers

Wrap a number in `<span data-count="4.2" data-decimals="1" data-prefix="$" data-suffix="M">$4.2M</span>`. It counts up from zero on slide entry (respects reduced-motion / `data-motion="off"`, which show the final value immediately). Keep the element's text content as the final value so it is correct with JS disabled.

## Theme

`data-default-theme="light|dark"` on `<html>` sets the initial theme (default `dark`). The Theme button toggles and persists to `localStorage`. All slide colours use the tokens in `deckChrome.css` (`--bg`, `--ink`, `--ink2/3`, `--green`, `--green-ink`, `--line`, `--rag-r/a/g`, …) so both themes just work. Dual-theme logos: put `class="l-light"` on the navy logo and `class="l-dark"` on the reversed logo; the CSS swaps them.

## Presenter camera cameo (live delivery)

The Camera button opens a draggable, resizable webcam picture-in-picture for presenting over the deck. Controls (hover the cameo): crop shape (circle/rounded/pill/square), mirror, switch camera, zoom, blur, pin controls open, close. Position/size/settings persist to `localStorage`. It never auto-starts (getUserMedia needs a user gesture).

**Secure-context requirement (important).** `getUserMedia` only works in a secure context:

- **Chrome** treats `http://localhost` as secure — plain HTTP is fine.
- **Safari** (and camera on any non-localhost host) treats `http://localhost` as **insecure** — it needs **https://**.

The cameo detects this: if the context is insecure or the camera API is missing, it shows a diagnostic in the cameo frame (the protocol/host and "serve over https / use Chrome") instead of failing silently, and it maps permission/hardware errors to plain messages (denied, no camera, in use, blocked).

**To present with the camera:**

```bash
cd presentation-folder
python3 engine/serveDeck.py            # Chrome: open http://localhost:8137
# For Safari, serve HTTPS with an mkcert cert (one-time CA install):
brew install mkcert && mkcert -install # asks for the Mac password, once
mkcert localhost 127.0.0.1             # writes localhost+1.pem in this folder
python3 engine/serveDeck.py --https    # open https://localhost:8444
```

Safari gotcha: if you opened the http page before `mkcert -install`, Safari cached the cert as untrusted — fully quit and reopen Safari, and don't use a Private window. Opening the deck as a bare `file://` also fails the secure-context test for the camera; serve it.

## Icon navigation rail

`<nav data-nav-rail>` in the body renders a right-edge dot per slide, built automatically from each slide's `data-label` (pill text) and `data-nav-icon` (glyph). Current slide is green, passed slides dimmed green, upcoming faint. Click a dot to jump. Hidden in print. For wide edge-to-edge content, keep a ~172px right gutter so blocks don't slide under the rail.

## The 22 templates (deckStageTemplates.html)

Copy any `<section>` out of `deckStageTemplates.html` and drop it into your deck, then replace the copy/data. Grouped by narrative act.

| # | Template | `data-nav-icon` | Use for |
|---|---|---|---|
| 1 | Title | `home` | Orient. Logo, kicker, one-idea headline, subtitle. No agenda. |
| 2 | Contents | `list` | Optional menu of sections. Skip for short speaker-led decks. |
| 3 | Price anchor | `tag` | **Cognitive frame.** Name the biggest honest number (cost of inaction) before the ask, so the ask is judged against it. Use defensible anchors only. |
| 4 | Section divider | `bookmark` | Act break. Giant number + section name. |
| 5 | Question | `help` | Open with tension. One provocative question, centred. Tease with slide, tell with voice. |
| 6 | Hero stat | `target` | One shocking number (count-up) + context line. |
| 7 | KPI wall | `grid` | Three signals max, each with a sparkline. |
| 8 | Horizontal bar | `bar` | Ranking. Bars grow left-to-right. Name only the top one aloud. |
| 9 | Trend area | `trend` | Slope over time. Line draws on entry. |
| 10 | Donut | `pie` | Composition, three slices max. |
| 11 | Stacked bar | `bar` | Composition over time. Columns grow from baseline. |
| 12 | Split + flow | `split` | Statement left, sense→model→act flow right. |
| 13 | Full-bleed image | `image` | One photo edge-to-edge, bottom scrim overlay. Swap the placeholder for a real site photo. |
| 14 | Quote | `quote` | Testimonial in the speaker's voice, attribution on screen. |
| 15 | Before / after | `columns` | Nancy Duarte what-is vs what-could-be. Right panel is the payoff. |
| 16 | RAG grid | `grid` | Status by domain. Speak only to the reds. |
| 17 | Waterfall | `bar` | Bridge a total: green adds, red subtracts, navy endpoints. |
| 18 | Roadmap | `route` | Phased plan, current phase green. Speak to sequence, not dates. |
| 19 | Quadrant | `crosshair` | 2×2 positioning. Point to the top-right cluster. |
| 20 | Article reference | `book` | One real `/resources` article: hero image + UTM QR. Generate the QR locally (see `resources-showcase.md`), never a remote QR service. |
| 21 | Resources | `book` | Up to two `/resources` pages as hero + QR cards. No text-list variant. |
| 22 | Close / contributions | `flag` | What we accomplished. Numbered, echoes the opening. Never "Thank You" / "Questions?". Stays up during Q&A. |

The full-bleed (13), article (20) and resources (21) templates carry visible placeholders — replace them with a real photo, a real article hero, and locally-generated QR codes before delivery. All other data (bars, donut arcs, sparklines, waterfall heights, quadrant dot positions) is inline in the section — edit the numbers and the geometry together, or ask the build to recompute the SVG coordinates from your real values.
