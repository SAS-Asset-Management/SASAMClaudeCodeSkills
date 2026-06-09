---
name: nano-banana-2
description: Generate SAS-AM brand-consistent image prompts and images using Google's Nano Banana 2 model. Use when the user wants to create an image prompt or image for a LinkedIn post, blog article, Webflow page, or slide topic, or asks for SAS-AM visuals, social or blog or presentation imagery, AI-generated images, graphics, or artwork from a piece of written content. Acts as a router — selects one of four modes (Editorial Diagram, Technical Line, Data as Hero, Architectural) based on the subject of the input and assembles a finished prompt using the SAS-AM brand frame (deep navy #002244 base, single lime-green #69BE28 accent).
---

# Nano Banana 2 Image Generation Skill

Generate SAS-AM brand-consistent image prompts (and the images themselves) using Google's Nano Banana 2 model. The skill separates a FIXED brand frame from VARIABLE per-image content so every visual is on-brand by construction.

## Overview

This skill integrates with Google's Gemini API to generate images using the Nano Banana 2 model (`gemini-3.1-flash-image-preview`), optimised for speed and high-volume use. The primary path is the **SAS-AM Brand Prompt Architect (Router)** described in the next section — given a piece of written content (LinkedIn post, blog article, slide topic), the router selects one of four modes and assembles a single natural-language prompt ready to paste into Nano Banana 2.

**Key Capabilities:**
- Brand-consistent prompt assembly from written content (post, article, slide topic)
- Four mode templates selected automatically from the subject:
  - Mode 1 — Editorial Diagram (`modes/mode-1-editorial-diagram.md`)
  - Mode 2 — Technical Line (`modes/mode-2-technical-line.md`)
  - Mode 3 — Data as Hero (`modes/mode-3-data-as-hero.md`)
  - Mode 4 — Architectural (`modes/mode-4-architectural.md`)
- Text-to-image generation via the Gemini API
- Web search grounding for real-world accuracy (optional, for non-brand work)
- Configurable aspect ratios (16:9, 1:1, 4:5)
- Integration with other SAS-AM skills (presentations, social media, research)

**Use Cases:**
- Hero images for blog articles published via webflow-content-creator
- Feed and carousel imagery for linkedin-post-generator
- Slide visuals for sas-presentation
- Industry and market infographics for b2b-research-agent
- Proposal visuals for beam-selling

---

## SAS-AM Brand Prompt Architect (Router)

When the input is a piece of written content (LinkedIn post, blog article, Webflow page, slide topic, or any SAS-AM communication), the skill **must** assemble one finished image prompt using the brand frame below and one of four mode sub-files in `modes/`. This is the default path for any SAS-AM imagery request.

### Context

Nano Banana 2 responds to natural-language descriptive prompts, **not** comma-stacked keyword lists. It takes the aspect ratio as plain English inside the prompt body (no CLI flags). Negative instructions land best as a prose sentence, not a bullet list. **Subjects are always stylised, simplified real objects, never pure abstraction.**

Images are consumed across LinkedIn (1:1 feed, 4:5 carousel), Webflow articles (16:9 hero), and presentations (16:9 slide). Aspect ratio is a variable slot. **No text, words, or letters appear in the image** — overlay text is added later in the design layer.

### The FIXED brand frame (verbatim — inserted into every mode at `[FIXED BRAND FRAME]`)

> Visual style: clean, sophisticated, intentional — the look of a high-end consultancy report or quality editorial publication. Flat with crisp clean edges; no outer glow, no halo, no soft luminous bloom, no glassy or frosted texture, no glossy 3D render. Subtle, restrained, confident.
>
> Colour: a deep navy blue (hex #002244) dominates as background and base. A bright lime-green (hex #69BE28) appears ONLY as a precise, deliberate accent — on a single highlighted element, a callout, or a key line. It must never appear as a glow, haze, gradient field, starburst or background light. Support these with cool greys and a soft off-white. Use no other colours.
>
> Lighting: soft, even, calm and assured.
>
> Do not include any text, words, letters, numbers, logos, people or faces. Avoid clutter, neon, rainbow palettes, lens flares, and a generic stock-image look.

### Mode-selection logic

Pick exactly one mode for each prompt.

| If the input is… | Use |
|---|---|
| Explaining a concept, process, or relationship (most posts) | **Mode 1 — Editorial Diagram** — `modes/mode-1-editorial-diagram.md` |
| Engineering teardown, failure analysis, asset structure, Maximo data structure, FMECA, reliability hierarchies | **Mode 2 — Technical Line** — `modes/mode-2-technical-line.md` |
| About numbers or an analytical result (maturity assessments, Weibull, fleet simulation, analytics findings) | **Mode 3 — Data as Hero** — `modes/mode-3-data-as-hero.md` |
| Sector positioning, infrastructure, "who we serve" — mood and gravitas over explanation | **Mode 4 — Architectural** — `modes/mode-4-architectural.md` |

If the choice is genuinely ambiguous between two modes, **state the call you made and the reason**. Do not silently default.

### Required behaviour

1. Take the written content as input — post draft, article, Webflow page copy, or slide topic.
2. Infer the mode from the subject. If ambiguous, declare the call and the reason.
3. Load the matching mode sub-file from `modes/`.
4. Derive the slot values for that mode (subject, core idea, composition directive, chart type, etc — slot set depends on the mode).
5. Accept an aspect ratio. Default to `a wide 16:9 landscape composition` if none is given. Also support `a square 1:1 composition` and `a tall 4:5 portrait composition`. Phrase the aspect in plain English inside the prompt body.
6. Choose a sensible open-space region for the text overlay — typically opposite the focal point.
7. Assemble the final prompt by inserting the brand frame verbatim into the mode template at `[FIXED BRAND FRAME]`, filling all bracketed slots.
8. Output **one finished prompt**, ready to paste into Nano Banana 2 or to use as the `PROMPT` value for the API call documented later in this file.

### Aspect-ratio reference

- `a wide 16:9 landscape composition` — default; blog hero, slide visual, LinkedIn article header
- `a square 1:1 composition` — LinkedIn feed post, profile image
- `a tall 4:5 portrait composition` — LinkedIn carousel slides, mobile-first

### When NOT to use the router

Skip the router only when the user explicitly asks for:
- A photorealistic scene (industrial photograph, portrait, on-site asset)
- Non-SAS-AM creative work
- A pure illustration in a non-SAS visual style

In those cases, follow the **Hyper-Realistic Photography Style** notes in `references/prompt-guide.md`.

---

## ⚠️ MANDATORY: Post-Processing Required

**Every generated image MUST be post-processed before delivery.**

After saving the raw PNG, ALWAYS run:
```bash
node ~/.claude/SASAMClaudeCodeSkills/nano-banana-2/1.1.0/scripts/post-process.js <input.png> <output_final.jpg>
```

This adds the SAS logo watermark and optimises the image. **The `_final.jpg` file is what you deliver to the user, NOT the raw PNG.**

DO NOT:
- Add "watermark" or "SAS logo" to the generation prompt
- Deliver the raw PNG without post-processing
- Skip this step for any reason

---

## Commands

| Command | Action |
|---------|--------|
| `setup` | Run first-time API key configuration |
| `status` | Show current configuration and statistics |
| `generate [prompt]` | Generate an image from text prompt |
| `history` | Show recent generation history |
| `[prompt]` | Shorthand for generate (most common usage) |

## Invocation Examples

```
/nano-banana-2 setup                                    # First-time configuration
/nano-banana-2 status                                   # Show config and stats
/nano-banana-2 "A futuristic city skyline at sunset"   # Generate image
/nano-banana-2 "Professional infographic about AI trends" --aspect 16:9 --size 2K
/nano-banana-2 history                                  # Recent generations
```

---

## Discovery Process

### Check Configuration State

Before generating any image, check if `~/.claude/skills/nano-banana-2/config.json` exists.

**If config exists:**
1. Load configuration from `~/.claude/skills/nano-banana-2/config.json`
2. Validate API key is set
3. Proceed with generation using saved preferences

**If config does NOT exist:**
1. Run first-time setup interview
2. Guide through API key configuration
3. Set default preferences
4. Create config file
5. Then proceed with generation

### First-Time Setup Questions

When no configuration exists, ask:

1. **API Key**
   - Do you have a Google AI Studio API key?
   - If yes: Ask for the key
   - If no: Guide to https://aistudio.google.com/apikey
   - Validate key with a test API call before saving

2. **Default Aspect Ratio**
   - What's your typical use case?
   - Options: 16:9 (presentations/videos), 1:1 (social media), 4:5 (portrait/mobile)

3. **Web Search Grounding**
   - Enable web search grounding by default? (Recommended: Yes)
   - This helps generate more accurate, contextually-aware images

4. **Output Directory**
   - Use default `./generated-images/` or specify custom location?

### Setup Guide for API Key

If the user doesn't have an API key, provide these instructions:

```
To get your Google AI Studio API key:

1. Go to https://aistudio.google.com/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key (starts with "AIza...")
5. Paste it here when prompted

Note: The API key will be stored globally in ~/.claude/skills/nano-banana-2/config.json
This location is outside your project directory, so credentials are protected.
```

---

## Configuration State

Store configuration in `~/.claude/skills/nano-banana-2/config.json`:

```json
{
  "schema_version": "1.0.0",
  "created_at": "2026-02-27T10:30:00Z",
  "updated_at": "2026-02-27T10:30:00Z",
  "api_key": "AIza...",
  "verified_at": "2026-02-27T10:30:00Z",
  "preferences": {
    "default_aspect_ratio": "16:9",
    "default_image_size": "2K",
    "web_search_enabled": true,
    "output_directory": "./generated-images"
  },
  "statistics": {
    "total_generated": 0,
    "last_generated_at": null
  }
}
```

See `references/config-template.json` for the full schema.

**Security:**
- Config is stored in `~/.claude/skills/nano-banana-2/` (outside project directory)
- No `.gitignore` changes needed - credentials are not in the repo
- When displaying status, mask the API key: `AIza...xyz`

---

## Generating Images

### API Call Structure

Use the Bash tool to call the Gemini API via curl:

```bash
API_KEY="{{API_KEY}}"
PROMPT="{{USER_PROMPT}}"
ASPECT_RATIO="{{ASPECT_RATIO}}"  # e.g., "16:9"
IMAGE_SIZE="{{IMAGE_SIZE}}"      # e.g., "2K"

curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent" \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: ${API_KEY}" \
  -d '{
    "contents": [{"parts": [{"text": "'"${PROMPT}"'"}]}],
    "generationConfig": {
      "responseModalities": ["IMAGE"],
      "imageConfig": {
        "aspectRatio": "'"${ASPECT_RATIO}"'",
        "imageSize": "'"${IMAGE_SIZE}"'"
      }
    },
    "tools": [{"googleSearch": {}}]
  }'
```

### Response Handling

The API returns JSON with base64-encoded image data:

```json
{
  "candidates": [{
    "content": {
      "parts": [{
        "inlineData": {
          "mimeType": "image/png",
          "data": "iVBORw0KGgo..."
        }
      }]
    }
  }]
}
```

**Processing Steps:**
1. Parse JSON response
2. Extract base64 data from `candidates[0].content.parts[0].inlineData.data`
3. Decode base64 to binary
4. Save as PNG file with timestamp and prompt summary
5. Create metadata JSON file alongside image

### Extracting and Saving Image

```bash
# Parse response and save image
RESPONSE=$(curl ... )  # API call from above

# Extract base64 data (using jq)
IMAGE_DATA=$(echo "$RESPONSE" | jq -r '.candidates[0].content.parts[0].inlineData.data')

# Generate filename with timestamp and prompt summary
TIMESTAMP=$(date +%Y-%m-%d_%H%M%S)
PROMPT_SLUG=$(echo "$PROMPT" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | cut -c1-40)
FILENAME="${TIMESTAMP}_${PROMPT_SLUG}"

# Create output directory if needed
mkdir -p ./generated-images

# Save raw image
echo "$IMAGE_DATA" | base64 -d > "./generated-images/${FILENAME}.png"

# MANDATORY: Run post-processing to add watermark
node ~/.claude/SASAMClaudeCodeSkills/nano-banana-2/1.1.0/scripts/post-process.js "./generated-images/${FILENAME}.png" "./generated-images/${FILENAME}_final.jpg"

# Save metadata (reference the final watermarked file)
cat > "./generated-images/${FILENAME}.json" << EOF
{
  "prompt": "${PROMPT}",
  "aspect_ratio": "${ASPECT_RATIO}",
  "image_size": "${IMAGE_SIZE}",
  "web_search_enabled": true,
  "generated_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "raw_file": "./generated-images/${FILENAME}.png",
  "final_file": "./generated-images/${FILENAME}_final.jpg"
}
EOF
```

**IMPORTANT:** The `_final.jpg` file is the deliverable. Always provide this file path to the user, not the raw PNG.

---

## Web Search Grounding

Web search grounding enhances image generation by allowing the model to reference real-world information.

**How It Works:**
- When enabled, the model can search the web for context about the prompt
- Results in more accurate depictions of real entities, current events, and factual details
- Particularly useful for generating images of real products, places, or people

**When to Use:**
- Generating images of real-world subjects (cities, landmarks, products)
- Creating infographics with factual content
- Producing visuals that reference current trends or events

**When to Disable:**
- Pure creative/fictional imagery
- Abstract art
- When you want the model to rely solely on its training data

**Disabling for a Single Request:**

If the user specifies `--no-search` or asks for purely creative imagery, modify the API call to omit the tools parameter:

```bash
# Without web search grounding
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent" \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: ${API_KEY}" \
  -d '{
    "contents": [{"parts": [{"text": "'"${PROMPT}"'"}]}],
    "generationConfig": {
      "responseModalities": ["IMAGE"],
      "imageConfig": {
        "aspectRatio": "'"${ASPECT_RATIO}"'",
        "imageSize": "'"${IMAGE_SIZE}"'"
      }
    }
  }'
```

---

## Parameter Reference

### Aspect Ratios

| Ratio | Best For |
|-------|----------|
| `1:1` | Social media posts, profile images, thumbnails |
| `16:9` | Presentations, video thumbnails, desktop wallpapers |
| `9:16` | Mobile wallpapers, stories, vertical video |
| `4:5` | Portrait images, Instagram posts |
| `4:3` | Traditional photo format |
| `3:4` | Portrait traditional format |

### Image Sizes

| Size | Dimensions (approx) | Best For |
|------|---------------------|----------|
| `512px` | 512x512 (or aspect equivalent) | Quick previews, thumbnails |
| `1K` | ~1024px | Web use, presentations |
| `2K` | ~2048px | High-quality prints, detailed work (default) |
| `4K` | ~4096px | Large prints, maximum detail |

---

## Output Management

### File Naming Convention

```
./generated-images/
├── 2026-02-27_143022_futuristic-city-skyline-at-sunset.png
├── 2026-02-27_143022_futuristic-city-skyline-at-sunset.json
├── 2026-02-27_145530_professional-infographic-about-ai-t.png
├── 2026-02-27_145530_professional-infographic-about-ai-t.json
└── ...
```

### Metadata File Structure

Each generated image has an accompanying `.json` file:

```json
{
  "prompt": "A futuristic city skyline at sunset",
  "aspect_ratio": "16:9",
  "image_size": "2K",
  "web_search_enabled": true,
  "generated_at": "2026-02-27T14:30:22Z",
  "file_path": "./generated-images/2026-02-27_143022_futuristic-city-skyline-at-sunset.png",
  "model": "gemini-3.1-flash-image-preview"
}
```

### After Generation

**CRITICAL: Always run post-processing after saving the raw PNG.**

1. **Run post-processing script** (REQUIRED):
   ```bash
   node ~/.claude/SASAMClaudeCodeSkills/nano-banana-2/1.1.0/scripts/post-process.js <input.png> <output.jpg>
   ```
2. Report success with the final watermarked file path
3. Update statistics in config file
4. Offer next steps (regenerate, adjust parameters, use in another skill)

---

## Post-Processing

**All generated images MUST be post-processed** to add the SAS watermark and optimise for web use.

### Post-Processing Script

Run this after every image generation:

```bash
node ~/.claude/SASAMClaudeCodeSkills/nano-banana-2/1.1.0/scripts/post-process.js ./generated-images/IMAGE.png ./generated-images/IMAGE_final.jpg
```

The script automatically:
- Resizes to 1000px (maintaining aspect ratio)
- Analyzes corner brightness to select appropriate watermark
- Adds SAS logo watermark (bottom-right)
- Compresses to JPG with MozJPEG (quality 85)
- Outputs file under 200KB

### Target Specifications

| Property | Target |
|----------|--------|
| Dimensions | 1000x1000 pixels (or aspect-equivalent) |
| File Size | Under 200KB |
| Format | JPG (MozJPEG optimised) |
| Watermark | SAS logo, bottom-right corner |

### Watermark Selection

The post-processing script automatically selects the appropriate watermark:
- **Dark backgrounds** (brightness < 128): Light SAS logo
- **Light backgrounds** (brightness >= 128): Dark SAS logo

Assets located at:
```
~/.claude/SASAMClaudeCodeSkills/nano-banana-2/1.1.0/skills/nano-banana-2/assets/
├── sas-logo-dark.png   # For light backgrounds
└── sas-logo-light.png  # For dark backgrounds
```

---

## Integration with Other Skills

This skill can be called from other SAS-AM skills to generate visual content.

### Integration Pattern

When another skill needs an image:

```
--- Generating Visual ---

[Skill Name] is generating an image using Nano Banana 2...

Prompt: [derived prompt]
Aspect Ratio: [contextually appropriate ratio]
```

### Skill-Specific Integrations

| Source Skill | Trigger Context | Suggested Parameters |
|--------------|-----------------|---------------------|
| sas-presentation | "Generate visual for slide about [topic]" | 16:9, 2K |
| linkedin-post-generator | "Create image for LinkedIn post" | 1:1 or 4:5, 2K |
| b2b-research-agent | "Generate infographic for [company/market]" | 16:9 or 1:1, 2K |
| beam-selling | "Create visual for proposal section" | 16:9, 2K |

### Cross-Skill Example

When sas-presentation needs a visual:

1. sas-presentation identifies need for visual asset
2. Check if nano-banana-2 is configured
3. Generate appropriate prompt based on slide content
4. Call nano-banana-2 with 16:9 aspect ratio
5. Save image to presentation assets directory
6. Reference in slide HTML

---

## Error Handling

### API Key Not Configured

```
No API key configured

Run `/nano-banana-2 setup` to configure your Google AI Studio API key.

To get an API key:
1. Go to https://aistudio.google.com/apikey
2. Sign in with your Google account
3. Create and copy your API key
```

### Invalid API Key

```
API key validation failed

Error: Invalid API key or key has been revoked

To fix:
1. Verify your key at https://aistudio.google.com/apikey
2. Run `/nano-banana-2 setup` to enter a new key
```

### Quota Exceeded

```
API quota exceeded

Your Google AI Studio quota has been reached.

Options:
- Wait for quota reset (typically daily)
- Upgrade your Google AI Studio plan
- Check quota usage at https://aistudio.google.com

Current statistics:
- Images generated today: [N]
- Last generation: [timestamp]
```

### Content Policy Violation

```
Content policy restriction

The requested image could not be generated due to content policy.

Suggestions:
- Rephrase the prompt to be less specific about restricted content
- Remove references to real people, trademarks, or sensitive topics
- Focus on abstract or general descriptions

Original prompt: [prompt]
```

### Network Error

```
Network error

Unable to reach the Google API endpoint.

Troubleshooting:
- Check your internet connection
- Verify firewall/proxy settings allow access to googleapis.com
- Try again in a few moments

If the issue persists, check Google Cloud status: https://status.cloud.google.com
```

### Malformed Response

```
Unexpected API response

The API returned an unexpected response format.

This may indicate:
- A temporary API issue
- An API version change

Action: Retry the request. If the issue persists, report it.

Response received: [truncated response]
```

---

## Status Command Output

When the user runs `/nano-banana-2 status`:

```
Nano Banana 2 Configuration
===========================

API Key: AIza...xyz (verified 2026-02-27)

Preferences:
  Aspect Ratio: 16:9
  Image Size: 2K
  Web Search: Enabled
  Output Dir: ./generated-images

Statistics:
  Total Generated: 42
  Last Generated: 2026-02-27 14:30:22

Recent Generations:
  1. futuristic-city-skyline-at-sunset.png (16:9, 2K)
  2. professional-infographic-about-ai-t.png (16:9, 2K)
  3. abstract-data-visualisation.png (1:1, 2K)
```

---

## Pre-Delivery Checklist

Before completing a generation request, verify:

- [ ] Configuration loaded from `~/.claude/skills/nano-banana-2/config.json`
- [ ] API key is valid and not expired
- [ ] Prompt is not empty
- [ ] Output directory exists or was created
- [ ] Image was successfully saved
- [ ] Metadata JSON was created alongside image
- [ ] Statistics updated in config

After generation:

- [ ] Report file path to user
- [ ] Display generation parameters used
- [ ] Offer to open image or generate variations
- [ ] Update `last_generated_at` timestamp

---

## Content Guidelines

**For SAS-AM imagery, use the [SAS-AM Brand Prompt Architect](#sas-am-brand-prompt-architect-primary-mode) section above.** The tips below apply only when the user has explicitly asked for non-brand or photographic work.

**Prompt Engineering Tips:**
- Be specific and descriptive
- Include style keywords (photorealistic, digital art, watercolour, minimalist)
- Specify lighting, mood, and composition
- Reference time of day, weather, or environment
- For infographics, describe the data story and visual style

### Hyper-Realistic Prompt Enhancement (Opt-In Only)

**Not the default for SAS-AM content.** Use this enhancement only when the user explicitly asks for a photorealistic image or supplies a `--photoreal` flag. For SAS-AM brand imagery, route through the SAS-AM Brand Prompt Architect instead.

For maximum photorealism on opt-in requests, enhance user prompts with these modifiers:

**Core Hyper-Realistic Keywords:**
- `hyperrealistic photograph`
- `photorealistic, 8K resolution`
- `professional DSLR photography, Canon EOS R5`
- `RAW photo style`
- `shallow depth of field`
- `cinematic lighting`

**Prompt Enhancement Pattern:**

When the user provides a prompt, prepend hyper-realistic modifiers:

```
User prompt: "Industrial factory with machinery failure"

Enhanced prompt: "Hyperrealistic photograph of an industrial factory
with machinery failure, photorealistic, 8K resolution, professional
DSLR photography Canon EOS R5, dramatic cinematic lighting, RAW photo
style, shallow depth of field"
```

**When NOT to Enhance:**
- User explicitly requests illustration, cartoon, or artistic style
- Abstract or conceptual imagery
- Infographics and data visualisations
- User includes `--no-enhance` flag

**Examples of Effective Prompts:**

```
"A photorealistic sunset over Sydney Harbour Bridge, warm golden light,
dramatic clouds, professional photography style"

"Minimalist infographic showing AI adoption trends, clean lines,
SAS-AM brand colours (blue and green accents), modern corporate style"

"Abstract data visualisation representing network connections,
glowing nodes, dark background, futuristic technology aesthetic"
```

**SAS-AM Brand Integration:**
- For SAS-AM content, use the [SAS-AM Brand Prompt Architect](#sas-am-brand-prompt-architect-primary-mode) — it enforces the brand colour system and visual style by construction.
- Brand colours: SAS Blue `#002244` (dominant); SAS Green `#69BE28` (single sparing accent); cool greys and soft off-white as supports.
- Visual style: minimalist geometric abstraction, generous negative space, no people, no text in image.

---

## Reference Files

- `references/config-template.json` - Configuration schema
- `references/api-examples.md` - Sample API calls and responses
- `references/prompt-guide.md` - Prompt engineering best practices
