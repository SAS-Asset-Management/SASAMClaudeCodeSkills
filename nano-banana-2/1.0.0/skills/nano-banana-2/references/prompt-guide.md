# Nano Banana 2 Prompt Engineering Guide

Best practices for crafting effective image generation prompts.

## Core Principles

### 1. Be Specific and Descriptive

**Weak:** "A city"
**Strong:** "A futuristic city skyline at sunset with flying vehicles, neon lights reflecting on glass towers, cyberpunk aesthetic"

### 2. Include Style Keywords

Specify the visual style you want:

- **Photographic:** photorealistic, professional photography, DSLR quality, 35mm film
- **Digital Art:** digital illustration, concept art, 3D render, CGI
- **Traditional Art:** oil painting, watercolour, pencil sketch, charcoal drawing
- **Design:** minimalist, flat design, vector art, infographic style
- **Aesthetic:** modern, vintage, retro, futuristic, corporate, playful

### 3. Describe Composition

- **Framing:** close-up, wide shot, aerial view, eye-level, bird's eye
- **Layout:** centred, rule of thirds, symmetrical, dynamic diagonal
- **Focus:** shallow depth of field, everything in focus, bokeh background

### 4. Specify Lighting and Mood

- **Lighting:** golden hour, dramatic shadows, soft diffused light, backlit, studio lighting
- **Mood:** serene, energetic, mysterious, professional, warm, cool

---

## Prompt Structure

Follow this template for consistent results:

```
[Subject] + [Style] + [Composition] + [Lighting/Mood] + [Additional Details]
```

**Example:**
```
A professional businesswoman in a modern office (subject),
photorealistic corporate photography style (style),
medium shot with shallow depth of field (composition),
natural window lighting creating soft shadows (lighting),
wearing navy suit, confident expression, glass walls in background (details)
```

---

## Use Case Templates

### Presentation Visuals (16:9)

```
Professional [topic] infographic, clean minimalist design,
corporate colour palette with blue and green accents,
modern data visualisation style, white background,
suitable for business presentation
```

### Social Media Graphics (1:1 or 4:5)

```
Eye-catching [topic] social media graphic,
bold typography space, vibrant colours,
professional but approachable style,
optimised for LinkedIn/Instagram
```

### Conceptual Illustrations

```
Abstract representation of [concept],
modern digital art style, flowing shapes,
gradient colours transitioning from [colour1] to [colour2],
clean composition with negative space
```

### Industry/Market Visuals

```
[Industry] sector visualisation,
professional photorealistic style,
showing [key element] in modern context,
corporate appropriate, high production value
```

---

## SAS-AM Brand Integration

When generating images for SAS-AM content:

### Brand Colours
- **SAS Blue:** #002244 (primary)
- **SAS Green:** #69BE28 (accent)
- **Neutrals:** White, light grey backgrounds

### Brand Voice Keywords
- Professional
- Innovative
- Trustworthy
- Clear
- Forward-thinking

### Example Brand-Aligned Prompts

```
Modern asset management concept visualisation,
clean professional design with navy blue (#002244) accents,
subtle green (#69BE28) highlights,
corporate photography style,
suitable for institutional investor audience
```

```
Technology in finance infographic,
minimalist design with SAS-AM brand colours,
data visualisation elements,
professional corporate aesthetic,
white background with blue and green accents
```

---

## Aspect Ratio Recommendations

| Use Case | Ratio | Prompt Considerations |
|----------|-------|----------------------|
| Presentations | 16:9 | Horizontal composition, leave space for text overlays |
| LinkedIn posts | 1:1 | Centred subject, bold visually impactful |
| LinkedIn articles | 16:9 | Wide establishing shots, professional scenes |
| Mobile stories | 9:16 | Vertical composition, action in centre |
| Profile images | 1:1 | Head-and-shoulders, clean background |
| Print materials | 4:3 | Traditional photo composition |

---

## Common Mistakes to Avoid

### 1. Vague Descriptions
- **Bad:** "An office"
- **Good:** "A modern open-plan tech office with standing desks, natural light from floor-to-ceiling windows, plants, and collaborative spaces"

### 2. Conflicting Styles
- **Bad:** "Photorealistic cartoon of..."
- **Good:** Pick one style and commit to it

### 3. Overloading Details
- **Bad:** "A cat sitting on a chair in a room with a window and curtains and a lamp and a table and books and a plant and a rug..."
- **Good:** "A tabby cat sitting in a cosy reading nook, warm afternoon light from a nearby window, bokeh background"

### 4. Ignoring Composition
- **Bad:** "Mountains"
- **Good:** "Dramatic mountain range shot from valley perspective, leading lines from foreground rocks, misty atmosphere"

### 5. Missing Context
- **Bad:** "A graph"
- **Good:** "Clean data visualisation bar chart showing growth trend, modern infographic style, blue gradient bars on white background"

---

## Web Search Grounding Tips

When web search grounding is enabled, the model can reference real-world information:

### Good Use Cases for Web Search

- Real landmarks and locations: "Sydney Opera House at golden hour"
- Current product designs: "Latest smartphone design, realistic render"
- Industry-specific contexts: "Modern data centre interior"
- Factual representations: "Accurate human heart anatomical illustration"

### When to Disable Web Search

- Pure fantasy/fiction: "Dragon flying over medieval castle"
- Abstract concepts: "Visualisation of emotions"
- Stylised art: "Impressionist painting of flowers"
- Original creations: "Unique alien creature design"

---

## Quality Modifiers

Add these keywords to enhance output quality:

### Resolution & Detail
- "highly detailed"
- "intricate"
- "sharp focus"
- "8K resolution"
- "ultra HD"

### Professional Quality
- "professional photography"
- "studio quality"
- "commercial grade"
- "publication ready"
- "award-winning"

### Lighting Quality
- "professional lighting"
- "cinematic lighting"
- "dramatic shadows"
- "soft box lighting"
- "rim lighting"

---

## Iterating on Results

If the first generation isn't quite right:

1. **Add specificity** to the area that needs improvement
2. **Remove conflicting descriptors** that might confuse the model
3. **Try different style keywords** to shift the aesthetic
4. **Adjust aspect ratio** if composition feels cramped or empty
5. **Increase resolution** (2K to 4K) for more detail

### Example Iteration

**V1:** "A modern office"
→ Result: Generic, uninspiring

**V2:** "A modern tech startup office with exposed brick, standing desks, natural light"
→ Result: Better, but too busy

**V3:** "A clean modern tech startup office, minimalist design, warm natural light from large windows, focus on one standing desk area, professional photography"
→ Result: Exactly what was needed

---

## Quick Reference Cheatsheet

| Element | Options |
|---------|---------|
| Style | photorealistic, digital art, illustration, minimalist, corporate |
| Lighting | golden hour, soft, dramatic, studio, natural |
| Mood | professional, energetic, serene, bold, sophisticated |
| Quality | detailed, sharp, high resolution, commercial grade |
| Composition | centred, rule of thirds, wide shot, close-up |
