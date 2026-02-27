# Nano Banana 2 Image Generation

Generate images using Google's Nano Banana 2 model (`gemini-3.1-flash-image-preview`) with web search grounding for real-world context.

## Features

- **Text-to-image generation** from natural language prompts
- **Web search grounding** for accurate, contextually-aware images
- **Configurable output** - aspect ratios (1:1, 16:9, 4:5, etc.) and sizes (512px to 4K)
- **Post-processing** - automatic resize to 1000px and compress under 200KB
- **Integration** with other SAS-AM skills (presentations, social media, research)

## Quick Start

```bash
# First-time setup
/nano-banana-2 setup

# Generate an image
/nano-banana-2 "A futuristic city skyline at sunset"

# With custom parameters
/nano-banana-2 "Professional infographic about AI trends" --aspect 16:9 --size 2K
```

## Requirements

- Google AI Studio API key (get one at https://aistudio.google.com/apikey)
- Optional: ImageMagick for CLI-based post-processing

## Configuration

Configuration is stored in `.nano-banana/config.json`:

```json
{
  "api_key": "AIza...",
  "preferences": {
    "default_aspect_ratio": "16:9",
    "default_image_size": "2K",
    "web_search_enabled": true,
    "post_processing": {
      "target_width": 1000,
      "max_file_size_kb": 200
    }
  }
}
```

## Output

Generated images are saved to `./generated-images/` with metadata:

```
./generated-images/
├── 2026-02-27_143022_futuristic-city-skyline.png
├── 2026-02-27_143022_futuristic-city-skyline.json
└── ...
```

## Integration

Works with other SAS-AM skills:

| Skill | Use Case |
|-------|----------|
| sas-presentation | Generate slide visuals |
| linkedin-post-generator | Create social media graphics |
| b2b-research-agent | Generate industry infographics |
| beam-selling | Create proposal visuals |

## Post-Processing

Images are optimised for web use:
- Resized to 1000px width (maintaining aspect ratio)
- Compressed to under 200KB
- Use Squoosh.app or ImageMagick for compression

## Security

- API key stored locally in `.nano-banana/config.json`
- Add `.nano-banana/` to `.gitignore` to protect credentials
