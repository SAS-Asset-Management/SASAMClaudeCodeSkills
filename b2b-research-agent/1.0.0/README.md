# B2B Research Agent Skill

A Claude Code skill for researching and identifying business-to-business engagement opportunities with structured prospect intelligence, decision-maker mapping, and personalised outreach strategies.

## Features

- **Prospect Research**: Deep-dive into target companies — financials, tech stack, org structure, recent news
- **Industry Scanning**: Identify companies matching your ideal customer profile (ICP)
- **Decision-Maker Mapping**: Find and profile key stakeholders and buying-committee members
- **Engagement Trigger Detection**: Surface pain points, initiatives, and events that signal buying intent
- **Outreach Strategy**: Generate personalised talking points, email templates, and call scripts
- **Competitive Intelligence**: Understand what solutions prospects use and where gaps exist
- **Pipeline Building**: Produce structured prospect lists ranked by fit and timing

## Installation

### Option 1: Global Installation (Recommended)

Copy the skill folder to your Claude Code skills directory:

```bash
cp -r b2b-research-agent ~/.claude/skills/
```

### Option 2: Project-Level Installation

Copy to your project's `.claude/skills/` directory:

```bash
mkdir -p .claude/skills
cp -r b2b-research-agent .claude/skills/
```

## Usage

Invoke the skill by asking Claude Code to research prospects:

```
Research potential clients in the mining industry for our asset management platform
```

Or use the skill directly:

```
/b2b-research-agent Find engagement opportunities in Australian utilities for edge AI solutions
```

## Workflow

1. **Discovery Interview**: Claude asks about your business, target market, ICP, and engagement goals
2. **Research Planning**: Define scope, scoring rubric, and primary sources
3. **Prospect Identification**: Web research to build and filter a candidate list
4. **Deep-Dive Intelligence**: Compile dossiers with company snapshots, decision-makers, and buying signals
5. **Strategy Development**: Score, rank, and develop personalised engagement plans
6. **Delivery**: Produce the final report in the requested format

## Output Formats

| Format | Use Case |
|--------|----------|
| **HTML Report** (Default) | Branded, interactive web report with light/dark mode, sidebar nav, score badges, and outreach timeline |
| **Executive Summary** | Quick-read key findings with icons — opportunity, timing, positioning, decision-makers, value alignment |
| **Prospect Dossier** | Deep research on a single target company |
| **Prospect Pipeline** | Batch research across multiple companies with priority ranking |
| **Outreach Templates** | Personalised email sequences, LinkedIn notes, and call scripts |
| **Event Brief** | Pre-conference engagement planning with target attendees |

## Scoring System

Prospects are scored on two axes:

- **Fit Score (1–5)**: How well the company matches your ICP
- **Timing Score (1–5)**: How strong the buying signals are right now

Combined into a priority matrix: **HIGH** / **MEDIUM** / **LOW** / **Monitor**

## Files Included

```
b2b-research-agent/
├── 1.0.0/
│   ├── .claude-plugin/
│   │   ├── plugin.json
│   │   └── marketplace.json
│   ├── skills/
│   │   └── b2b-research-agent/
│   │       ├── SKILL.md                              # Main skill instructions
│   │       └── references/
│   │           ├── report-template.html               # HTML report scaffold
│   │           ├── report-styles.css                  # Report theme CSS
│   │           ├── prospect-dossier-template.md       # Single-company dossier
│   │           ├── pipeline-template.md               # Multi-company pipeline
│   │           ├── outreach-templates.md              # Email & call scripts
│   │           └── event-brief-template.md            # Conference prep brief
│   └── README.md
```

## Requirements

- Claude Code CLI
- Web search access (for live prospect research)
- Modern web browser (for viewing HTML reports)

## Licence

MIT

## Author

SAS-AM
