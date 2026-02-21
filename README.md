# Claude Code Skills

A collection of custom Claude Code skills for professional workflows.

## Available Skills

### sas-presentation

Create polished SAS-AM branded Reveal.js presentations with:

- **Light/Dark Mode**: Built-in theme switching with localStorage persistence
- **Narrative Structure**: Proven 7-section storytelling arc (Opening → Context → Problem → Solution → Implementation → Future → Connection)
- **SAS Brand Guidelines**: SAS Blue (#002244) and SAS Green (#69BE28)
- **Professional Typography**: Source Sans Pro font family
- **Static Footer Navigation**: Section progress indicator
- **Dual-Theme Assets**: Support for light/dark image variants
- **Animations**: Binary background, animated SVG diagrams

### data-quality-analysis

Analyse raw data quality using the ABS Data Quality Framework (Catalogue No. 1520.0):

- **Seven Dimensions**: Institutional environment, relevance, timeliness, accuracy, coherence, interpretability, accessibility
- **Data Profiling**: Schema inspection, descriptive statistics, missing data analysis, outlier detection, duplicate detection
- **Evidence-Based Ratings**: HIGH / ADEQUATE / LOW / UNABLE TO ASSESS for each dimension
- **Structured Report**: Markdown report with executive summary, dimension assessments, and prioritised recommendations
- **Framework Reference**: Based on ABS 1520.0 (May 2009), derived from Statistics Canada QAF and European Statistics Code of Practice

## Installation

### Global Installation (Recommended)

Copy skills to your Claude Code skills directory:

```bash
cp -r sas-presentation ~/.claude/skills/
```

### Project-Level Installation

Copy to your project's `.claude/skills/` directory:

```bash
mkdir -p .claude/skills
cp -r sas-presentation .claude/skills/
```

## Usage

Invoke a skill by asking Claude Code to perform the relevant task:

```
Create a presentation about [your topic]
```

Or reference the skill directly:

```
/sas-presentation Create a presentation about edge computing in asset management
```

## Skill Structure

Each skill follows the Claude Code skill format:

```
skill-name/
├── 1.0.0/
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── skills/
│   │   └── skill-name/
│   │       ├── SKILL.md          # Main skill instructions
│   │       └── references/       # Supporting files
│   └── README.md
```

## Contributing

To add a new skill:

1. Create a folder with your skill name
2. Follow the skill structure above
3. Include a comprehensive SKILL.md with instructions
4. Submit a pull request

## Licence

MIT

## Author

SAS-AM
