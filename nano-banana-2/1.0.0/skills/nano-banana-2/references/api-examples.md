# Nano Banana 2 API Examples

Reference examples for the Gemini Image Generation API.

## Basic Text-to-Image

```bash
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent" \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: YOUR_API_KEY" \
  -d '{
    "contents": [{"parts": [{"text": "A serene mountain landscape at sunrise"}]}],
    "generationConfig": {
      "responseModalities": ["IMAGE"],
      "imageConfig": {
        "aspectRatio": "16:9",
        "imageSize": "2K"
      }
    }
  }'
```

## With Web Search Grounding (Recommended)

```bash
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent" \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: YOUR_API_KEY" \
  -d '{
    "contents": [{"parts": [{"text": "Sydney Opera House at golden hour"}]}],
    "generationConfig": {
      "responseModalities": ["IMAGE"],
      "imageConfig": {
        "aspectRatio": "16:9",
        "imageSize": "2K"
      }
    },
    "tools": [{"googleSearch": {}}]
  }'
```

## Square Format (Social Media)

```bash
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent" \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: YOUR_API_KEY" \
  -d '{
    "contents": [{"parts": [{"text": "Modern minimalist logo concept for fintech"}]}],
    "generationConfig": {
      "responseModalities": ["IMAGE"],
      "imageConfig": {
        "aspectRatio": "1:1",
        "imageSize": "2K"
      }
    },
    "tools": [{"googleSearch": {}}]
  }'
```

## Portrait Format (Mobile/Stories)

```bash
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent" \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: YOUR_API_KEY" \
  -d '{
    "contents": [{"parts": [{"text": "Professional business person in modern office"}]}],
    "generationConfig": {
      "responseModalities": ["IMAGE"],
      "imageConfig": {
        "aspectRatio": "9:16",
        "imageSize": "2K"
      }
    },
    "tools": [{"googleSearch": {}}]
  }'
```

## High Resolution (4K)

```bash
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent" \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: YOUR_API_KEY" \
  -d '{
    "contents": [{"parts": [{"text": "Detailed architectural rendering of modern skyscraper"}]}],
    "generationConfig": {
      "responseModalities": ["IMAGE"],
      "imageConfig": {
        "aspectRatio": "16:9",
        "imageSize": "4K"
      }
    },
    "tools": [{"googleSearch": {}}]
  }'
```

## Quick Preview (512px)

```bash
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent" \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: YOUR_API_KEY" \
  -d '{
    "contents": [{"parts": [{"text": "Simple icon representing data analytics"}]}],
    "generationConfig": {
      "responseModalities": ["IMAGE"],
      "imageConfig": {
        "aspectRatio": "1:1",
        "imageSize": "512px"
      }
    }
  }'
```

---

## Successful Response Format

```json
{
  "candidates": [
    {
      "content": {
        "parts": [
          {
            "inlineData": {
              "mimeType": "image/png",
              "data": "iVBORw0KGgoAAAANSUhEUgAA... (base64 encoded image data)"
            }
          }
        ],
        "role": "model"
      },
      "finishReason": "STOP",
      "avgLogprobs": -0.123
    }
  ],
  "usageMetadata": {
    "promptTokenCount": 10,
    "candidatesTokenCount": 256,
    "totalTokenCount": 266
  }
}
```

---

## Error Response Examples

### Invalid API Key

```json
{
  "error": {
    "code": 401,
    "message": "API key not valid. Please pass a valid API key.",
    "status": "UNAUTHENTICATED"
  }
}
```

### Quota Exceeded

```json
{
  "error": {
    "code": 429,
    "message": "Resource has been exhausted (e.g. check quota).",
    "status": "RESOURCE_EXHAUSTED"
  }
}
```

### Content Policy Violation

```json
{
  "candidates": [
    {
      "finishReason": "SAFETY",
      "safetyRatings": [
        {
          "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
          "probability": "HIGH"
        }
      ]
    }
  ]
}
```

### Invalid Parameter

```json
{
  "error": {
    "code": 400,
    "message": "Invalid value for imageConfig.aspectRatio",
    "status": "INVALID_ARGUMENT"
  }
}
```

---

## Shell Script for Extraction

Extract and save image from API response:

```bash
#!/bin/bash
# Usage: ./extract_image.sh response.json output.png

RESPONSE_FILE="$1"
OUTPUT_FILE="$2"

# Extract base64 data using jq
IMAGE_DATA=$(jq -r '.candidates[0].content.parts[0].inlineData.data' "$RESPONSE_FILE")

if [ "$IMAGE_DATA" != "null" ] && [ -n "$IMAGE_DATA" ]; then
    echo "$IMAGE_DATA" | base64 -d > "$OUTPUT_FILE"
    echo "Image saved to $OUTPUT_FILE"
else
    echo "Error: Could not extract image data from response"
    exit 1
fi
```

---

## Alternative Models

Other available Nano Banana models:

| Model | ID | Optimised For |
|-------|-----|---------------|
| Nano Banana 2 | `gemini-3.1-flash-image-preview` | Speed, high-volume |
| Nano Banana Pro | `gemini-3-pro-image-preview` | Professional assets |
| Nano Banana | `gemini-2.5-flash-image` | Efficiency |

To switch models, replace the model ID in the endpoint URL.
