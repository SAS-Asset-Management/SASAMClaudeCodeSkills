# SAS-AM Visual Branding

Shared branding specifications used across MBP visual skills (MBP:presentation, MBP:nano-banana, MBP:data-quality, MBP:b2b-research, MBP:content-intel).

## Colours

| Name | Hex | RGB | Usage |
|---|---|---|---|
| SAS Blue (Navy) | `#002244` | 0, 34, 68 | Primary brand colour. Headers, headings, primary buttons, nav backgrounds |
| SAS Green | `#69BE28` | 105, 190, 40 | Accent colour. CTAs, highlights, success states, accent borders |
| Tint Light | `#F2F4F6` | 242, 244, 246 | Page backgrounds, alternating table rows |
| Tint Mid | `#E5E9EC` | 229, 233, 236 | Borders, card outlines |
| Tint Dark | `#D9DEE3` | 217, 222, 227 | Heavier borders, inactive elements |
| Blue Grey | `#5D6C7B` | 93, 108, 123 | Body text secondary, descriptions |
| Mid Grey | `#9B9B9B` | 155, 155, 155 | Labels, metadata, timestamps |
| Text | `#1A2535` | 26, 37, 53 | Primary body text |

## Rating Colours

| Rating | Colour | Hex | Usage |
|---|---|---|---|
| High / Good / Green | Green | `#4A9B1C` | Positive scores, passing metrics |
| Adequate / Amber | Amber | `#F5A623` | Moderate scores, warnings |
| Low / Red | Red | `#E23939` | Poor scores, critical issues |

## Typography

- **Primary font:** DM Sans (Google Fonts)
- **Fallback:** Source Sans Pro, system sans-serif
- **Monospace:** Source Code Pro, monospace
- **Headings:** DM Sans 700 (bold)
- **Body:** DM Sans 400 (regular)
- **Labels/metadata:** DM Sans 600 (semibold), uppercase, letter-spacing 0.06em

## Logo

- **Mark:** White "SAS" text on SAS Green (#69BE28) rounded rectangle
- **Watermark (nano-banana):** Semi-transparent SAS logo, bottom-right corner
  - Light backgrounds: dark watermark
  - Dark backgrounds: light watermark
  - Automatically selected by post-processing script based on background brightness

## Report Layout Patterns

- **Header:** SAS Blue background, white text, green accent border bottom
- **Cards:** White background, 1px tint-mid border, 8px border-radius
- **Tables:** SAS Blue thead, alternating tint-light rows
- **Sidebar:** Fixed left navigation with section jump links
- **Score rings:** SVG circle, stroke colour by rating
- **Light/dark mode:** Toggle with localStorage persistence
