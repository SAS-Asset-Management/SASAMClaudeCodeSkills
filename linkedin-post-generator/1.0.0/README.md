# SAS-AM LinkedIn Post Generator

A Claude Code skill for generating LinkedIn posts in the SAS-AM brand voice. Supports two core post types: **pillar promotion** (driving traffic to website articles) and **quick insight** (standalone thought leadership).

## Features

- **Brand Voice Enforcement**: Upbeat, clear, tech-forward, conversational — never corporate
- **Two Post Types**: Pillar promotion posts and quick insight posts
- **Hook Craft**: Generates multiple opening line options to earn the "see more" click
- **Australian English**: Enforces Australian spelling and conventions throughout
- **Quality Checklist**: Automated review against brand guidelines before delivery
- **No Emojis, No Hashtags**: Clean, professional posts that let the writing speak
- **Carousel Support**: Generate slide-by-slide text for carousel/infographic posts

## Installation

### Option 1: Global Installation (Recommended)

```bash
cp -r linkedin-post-generator ~/.claude/skills/
```

### Option 2: Project-Level Installation

```bash
mkdir -p .claude/skills
cp -r linkedin-post-generator .claude/skills/
```

## Usage

Generate a pillar promotion post:

```
/linkedin-post-generator Promote this article about AI readiness for asset managers
```

Generate a quick insight post:

```
/linkedin-post-generator Quick insight on why most risk registers are useless
```

Generate carousel text:

```
/linkedin-post-generator Carousel: 5 signs your data isn't AI-ready
```

Get alternative hooks:

```
/linkedin-post-generator hooks
```

Adjust tone:

```
/linkedin-post-generator spicier
/linkedin-post-generator softer
```

## Post Types

| Type | Purpose | Length | When to Use |
|------|---------|--------|-------------|
| **Pillar Promotion** | Drive traffic to a website article | 150-300 words | When you have a full article to promote |
| **Quick Insight** | Standalone thought leadership | 150-400 words | Tips, contrarian takes, myth-busting, lists |
| **Carousel Text** | High engagement, shareability | Max 30 words/slide | Visual content with one idea per slide |

## In-Session Commands

| Command | Action |
|---------|--------|
| `draft` | Generate a new post from the current brief |
| `hooks` | Generate 3-5 alternative hook options |
| `shorter` | Rewrite in fewer words |
| `longer` | Expand with more detail |
| `spicier` | Make more provocative or opinionated |
| `softer` | Tone down — less confrontational |
| `carousel` | Convert topic into carousel slide text |
| `variations` | Generate 2-3 different angles on the same topic |
| `checklist` | Run the quality checklist against the current draft |

## Files Included

```
linkedin-post-generator/
├── 1.0.0/
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── skills/
│   │   └── linkedin-post-generator/
│   │       ├── SKILL.md                            # Main skill instructions
│   │       └── references/
│   │           ├── pillar-post-template.md          # Pillar promotion post template
│   │           └── insight-post-template.md         # Quick insight post template
│   └── README.md
```

## Requirements

- Claude Code CLI

## Licence

MIT

## Author

SAS-AM
