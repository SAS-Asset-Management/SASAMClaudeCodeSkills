# marcov.BEAM Selling Skill

A Claude Code skill for guiding sales engagements through the **marcov.BEAM** (Bayesian Evidence-Advancing Markov) evidence-gated sales lifecycle. Integrates with the b2b-research-agent skill to take prospect research and transform it into structured, stage-gated sales progression.

## Features

- **6-Stage Evidence-Gated Pipeline**: Qualify → Diagnose → Align → Propose → Commit → Deliver
- **SPIN Selling Integration**: Situation, Problem, Implication, and Need-payoff questions woven into every stage
- **b2b-research-agent Integration**: Automatically ingests prospect dossiers as the foundation for qualification
- **Save and Resume**: Persists engagement state to `.beam/` so you can clear context and pick up later
- **Auto-Dump**: Automatically saves learnings and next steps after every interaction
- **Session Logs**: Human-readable Markdown session logs for easy review
- **Win Probability**: Bayesian win probability updated at each stage with evidence-based modifiers
- **Stakeholder Mapping**: Track the buying committee throughout the engagement
- **Proposal Generation**: Structured proposal template built from diagnostic findings
- **Pipeline Dashboard**: Track all active engagements in one view

## Installation

### Option 1: Global Installation (Recommended)

```bash
cp -r beam-selling ~/.claude/skills/
```

### Option 2: Project-Level Installation

```bash
mkdir -p .claude/skills
cp -r beam-selling .claude/skills/
```

## Usage

Start a new engagement:

```
/beam-selling Acme Corp
```

Resume an existing engagement:

```
/beam-selling Resume Acme Corp
```

Review pipeline:

```
/beam-selling Show all active engagements
```

## The BEAM Framework

| Letter | Meaning | Application |
|--------|---------|-------------|
| **B** | Bayesian | Update probability of winning as new evidence arrives |
| **E** | Evidence | Every stage advancement requires concrete evidence |
| **A** | Advancing | Forward momentum only when evidence earns it |
| **M** | Markov | Current state determines next actions |

## The 6 Stages

| Stage | Purpose | SPIN Focus | Right to Advance |
|-------|---------|------------|------------------|
| 1. Qualify | Is a conversation worth having? | Situation | Agreed to discovery conversation |
| 2. Diagnose | Does real pain exist? | Problem → Implication | "This is a problem we need to address" |
| 3. Align | Shared understanding of problem and success? | Implication → Need-payoff | "What would you recommend?" |
| 4. Propose | Tailored recommendation from findings | Need-payoff | Confirmed intent to decide |
| 5. Commit | Secure formal agreement | Validation | Contract signed |
| 6. Deliver | Execute, demonstrate value, earn renewal | Continuous Discovery | New opportunity → Stage 1 |

## Design Principles

1. **No stage-skipping** — earn the gate or exit
2. **Each gate requires mutual agreement** — both seller and buyer confirm
3. **SPIN intensity peaks in Stages 2–3** — deep diagnostic is where deals are won or lost
4. **"No" is a legitimate outcome** — qualifying out is a success

## Local State (`.beam/` Directory)

The skill automatically saves all progress to a hidden `.beam/` directory:

```
.beam/
├── engagements/
│   └── acme-corp.json          # Full engagement state (JSON)
├── sessions/
│   ├── acme-corp-2026-02-22.md # Session log with learnings and next steps
│   └── acme-corp-2026-02-25.md
└── config.json                  # Seller's company info (cached, asked once)
```

After every interaction, the skill dumps:
- Updated engagement state (gates, evidence, probability)
- A session log with learnings, decisions, and next steps
- A resume hint so the user knows how to pick up later

## In-Session Commands

| Command | Action |
|---------|--------|
| `save` | Save current state |
| `status` | Show stage, gates, and win probability |
| `gates` | Show gate criteria for current stage |
| `evidence` | Show evidence for current stage |
| `stakeholders` | Show stakeholder map |
| `advance` | Attempt to advance (triggers gate review) |
| `next` | Suggest what to do next |
| `list` | List all active engagements |
| `export` | Export as Markdown summary |
| `close` | Close engagement (won/lost/disqualified) |

## Files Included

```
beam-selling/
├── 1.0.0/
│   ├── .claude-plugin/
│   │   ├── plugin.json
│   │   └── marketplace.json
│   ├── skills/
│   │   └── beam-selling/
│   │       ├── SKILL.md                               # Main skill instructions
│   │       └── references/
│   │           ├── beam-state-template.json            # Engagement state schema
│   │           ├── stage-gate-checklist.md             # Gate criteria per stage
│   │           ├── spin-question-bank.md               # SPIN questions by stage
│   │           ├── proposal-template.md                # Stage 4 proposal output
│   │           └── engagement-tracker-template.md      # Pipeline dashboard
│   └── README.md
```

## Requirements

- Claude Code CLI
- Web search access (for live research during qualification)
- b2b-research-agent skill (recommended, not required)

## Licence

MIT

## Author

SAS-AM
