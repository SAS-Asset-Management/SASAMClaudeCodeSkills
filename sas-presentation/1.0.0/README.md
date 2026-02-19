# SAS-AM Presentation Skill

A Claude Code skill for creating professional SAS-AM branded Reveal.js presentations with light/dark mode, narrative structure, and professional layouts.

## Features

- **SAS Brand Colours**: SAS Blue (#002244) and SAS Green (#69BE28)
- **Light/Dark Mode Toggle**: Built-in theme switching with localStorage persistence
- **Narrative Structure**: Proven 7-section storytelling arc
- **Professional Typography**: Source Sans Pro font family
- **Static Footer Navigation**: Section progress indicator with theme toggle
- **Dual-Theme Assets**: Support for light/dark image variants
- **Subtle Animations**: Binary background, animated SVG diagrams

## Installation

### Option 1: Global Installation (Recommended)

Copy the skill folder to your Claude Code skills directory:

```bash
cp -r sas-presentation ~/.claude/skills/
```

### Option 2: Project-Level Installation

Copy to your project's `.claude/skills/` directory:

```bash
mkdir -p .claude/skills
cp -r sas-presentation .claude/skills/
```

## Usage

Invoke the skill by asking Claude Code to create a presentation:

```
Create a presentation about [your topic]
```

Or use the skill directly:

```
/sas-presentation Create a presentation about edge computing in asset management
```

## Workflow

1. **Discovery Interview**: Claude will ask questions about your topic, audience, and content
2. **Structure Planning**: Define the narrative arc using the 7-section structure
3. **Content Creation**: Generate slides incrementally
4. **Review & Refine**: Test light/dark mode, navigation, and export

## Narrative Structure

| Section | Purpose |
|---------|---------|
| OPENING | Hook the audience, reframe the problem |
| THE CONTEXT | Establish the current situation |
| THE PROBLEM | Identify specific pain points |
| THE SOLUTION | Present your answer |
| THE IMPLEMENTATION | Show how it works practically |
| THE FUTURE | Vision and possibilities |
| THE CONNECTION | Call to action |

## Files Included

```
sas-presentation/
├── 1.0.0/
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── skills/
│   │   └── sas-presentation/
│   │       ├── SKILL.md                    # Main skill instructions
│   │       └── references/
│   │           ├── base-styles.css         # SAS theme CSS
│   │           └── scaffold-template.html  # HTML template
│   └── README.md
```

## Requirements

- Claude Code CLI
- Modern web browser (for viewing presentations)
- Optional: `decktape` for PDF export

## License

MIT

## Author

SAS-AM
