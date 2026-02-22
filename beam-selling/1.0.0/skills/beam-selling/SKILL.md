---
name: beam-selling
description: Guide a sales engagement through the marcov.BEAM evidence-gated sales lifecycle. Use when the user wants to develop, progress, or review a sales opportunity using the BEAM framework (Bayesian Evidence-Advancing Markov). Integrates with b2b-research-agent output to form scope, build engagement strategy, and advance deals stage by stage. Supports saving and resuming progress across sessions.
---

# marcov.BEAM Selling Skill

Guide sales engagements through a structured, evidence-gated lifecycle. This skill implements the **marcov.BEAM** (Bayesian Evidence-Advancing Markov) framework — a 6-stage sales pipeline where advancement requires earning the right through demonstrated evidence at each gate.

## Overview

This skill helps you:

- **beamUP a sales pitch**: Take B2B research and transform it into a structured sales engagement
- **Follow the bouncing ball**: Progress through 6 evidence-gated stages with clear criteria at each gate
- **Save and resume**: Persist engagement state locally so you can clear context and pick up later
- **SPIN-integrated selling**: Apply Situation, Problem, Implication, and Need-payoff questioning at every stage
- **Evidence-gated progression**: No stage-skipping — earn the gate or exit
- **Build proposals**: Generate tailored proposals from diagnostic findings

## BEAM Acronym

| Letter | Meaning | Application |
|--------|---------|-------------|
| **B** | Bayesian | Update your probability of winning as new evidence arrives |
| **E** | Evidence | Every stage advancement requires concrete evidence, not gut feel |
| **A** | Advancing | Forward momentum only when evidence earns it |
| **M** | Markov | Current state determines next actions — history informs but doesn't constrain |

---

## Input

This skill accepts a **company name** or **deal name** as its primary input. It builds on the output from the `b2b-research-agent` skill, but can also start from scratch.

### Invocation Examples

```
/beam-selling Acme Corp
/beam-selling Resume Acme Corp engagement
/beam-selling Advance BHP to Stage 3
/beam-selling Review gate criteria for GeelongPort
/beam-selling Show all active engagements
```

### Integration with b2b-research-agent

If a b2b-research-agent dossier exists for the target company, **automatically ingest it** as the foundation for Stage 1 (Qualify). Look for:

1. A `.beam/` directory in the current working directory
2. Any HTML reports or Markdown dossiers matching the company name in the current directory tree
3. Ask the user to point to the research if not found automatically

---

## The 6-Stage Pipeline

```
[1. Qualify] → [2. Diagnose] → [3. Align] → [4. Propose] → [5. Commit] → [6. Deliver]
```

### Design Principles

1. **No stage-skipping** — earn the gate or exit
2. **The skill is the gatekeeper** — the skill independently assesses evidence quality and refuses to advance until it is satisfied. The user does not self-certify gates.
3. **SPIN intensity peaks in Stages 2–3** — deep diagnostic questioning is where deals are won or lost
4. **"No" is a legitimate outcome** — qualifying out is a success, not a failure
5. **Evidence over opinion** — every advancement decision is backed by documented, verifiable evidence
6. **Earn the right** — progression is earned through demonstrated rigour, not claimed through assertion

---

## Stage Definitions

### Stage 1: Qualify

**Purpose**: Establish whether a conversation is worth having.

**SPIN Focus**: Situation

**Activities**:
- Review b2b-research-agent dossier (if available)
- Confirm the prospect fits the Ideal Customer Profile (ICP)
- Identify the problem domain you can address
- Confirm access to authority or influence
- Assess willingness to have a diagnostic conversation

**Gate Criteria** (all must be met — assessed by the skill, not self-certified):
- [ ] Problem domain identified
- [ ] Access to authority or influence confirmed
- [ ] Prospect willing to have a diagnostic conversation

**Right to Advance**: Prospect has agreed to a discovery conversation.

**Minimum Evidence Bar** (what the skill needs to see before it will accept each gate):

| Gate | The skill will accept this when... | The skill will reject this if... |
|------|-----------------------------------|---------------------------------|
| Problem domain identified | User has articulated a **specific** problem area (not a vague category), explained why their offering addresses it, and provided a plausible ICP fit rationale | User gives a one-line generic statement like "they need digital transformation" with no specifics |
| Access to authority | User can name a **specific person** (name + title/role) who has authority or influence, and explain the relationship or how access was obtained | User says "I'll find someone" or names a role without a person |
| Willing to diagnose | User provides evidence of **explicit agreement** to a discovery conversation — a meeting booked, an email accepting, a verbal yes with date. Not an assumption of willingness | User assumes willingness ("they'll probably agree") or conflates a marketing interaction with a sales conversation |

**Key Questions to Ask the User**:
1. What b2b-research exists for this prospect? (dossier, report, notes)
2. What is your offering for this specific engagement?
3. Has there been any prior contact or engagement?
4. What triggered this opportunity? (event, referral, cold outreach, tender)
5. Who is your initial point of contact?

**Evidence to Document**:
- Source of the opportunity (how did this prospect surface?)
- ICP alignment score (from b2b-research-agent or assessed here)
- Initial contact details and relationship status
- Problem hypothesis (what do you believe their pain is?)

---

### Stage 2: Diagnose

**Purpose**: Uncover whether real pain exists and what's driving it.

**SPIN Focus**: Problem → Implication

**Activities**:
- Conduct discovery conversation(s) using SPIN questioning
- Uncover specific problems the prospect is experiencing
- Quantify the implications of those problems (cost, risk, time, reputation)
- Establish the cost of inaction — what happens if they do nothing?
- Map the organisational impact of the problem

**Gate Criteria** (all must be met — assessed by the skill, not self-certified):
- [ ] Specific problems articulated by the prospect (not assumed by you)
- [ ] Implications quantified (in dollars, time, risk, or other metrics)
- [ ] Cost of inaction acknowledged by the prospect

**Right to Advance**: The prospect says "This is a problem we need to address."

**Minimum Evidence Bar** (what the skill needs to see before it will accept each gate):

| Gate | The skill will accept this when... | The skill will reject this if... |
|------|-----------------------------------|---------------------------------|
| Problems articulated | User provides **at least 2 distinct problems** stated by the prospect, ideally with direct quotes or close paraphrases. The problems must be specific and operational, not generic buzzwords | User lists problems they *assume* the prospect has, or provides only one vague issue |
| Implications quantified | User provides **at least one concrete metric** — a dollar figure, time cost, risk exposure percentage, headcount impact, or similar. The metric must be tied to a specific problem, not a general industry stat | User says "it's costing them a lot" or only provides qualitative impact without numbers |
| Cost of inaction acknowledged | User provides evidence the **prospect themselves** acknowledged what happens if they do nothing — a quote, a described reaction, or an email excerpt. This cannot be the seller's assertion about the prospect's situation | User says "they know it's a problem" without evidence of the prospect actually saying so |

**SPIN Questions to Prepare**:

*Problem Questions* (uncover difficulties):
- "What challenges are you facing with [area]?"
- "How satisfied are you with your current approach to [area]?"
- "What happens when [current process] fails?"
- "Where do you see the biggest gaps in [area]?"

*Implication Questions* (develop the severity):
- "What impact does that have on [downstream process]?"
- "How does that affect your ability to [strategic goal]?"
- "What does that cost you annually — in direct costs and lost opportunity?"
- "If this continues for another 12 months, what's the likely outcome?"
- "How does this compare to what your board/leadership expects?"

**Evidence to Document**:
- Specific problems stated by the prospect (direct quotes preferred)
- Quantified implications (dollar values, time delays, risk exposure)
- Stakeholders affected and how
- Prospect's own words acknowledging the cost of inaction

---

### Stage 3: Align

**Purpose**: Confirm shared understanding of the problem and what success looks like.

**SPIN Focus**: Implication → Need-payoff

**Activities**:
- Validate the problem definition with the prospect — do they agree on the diagnosis?
- Define success criteria together — what does "fixed" look like?
- Map the stakeholder landscape — who else needs to agree?
- Understand the decision-making process — who, when, how
- Transition from problems to solutions in the prospect's mind

**Gate Criteria** (all must be met — assessed by the skill, not self-certified):
- [ ] Problem definition agreed by both parties
- [ ] Success criteria defined and measurable
- [ ] Stakeholder landscape mapped (economic buyer, technical evaluator, champion, gatekeeper)
- [ ] Decision-making process understood (timeline, approvals, procurement)

**Right to Advance**: The prospect asks "What would you recommend?"

**Minimum Evidence Bar** (what the skill needs to see before it will accept each gate):

| Gate | The skill will accept this when... | The skill will reject this if... |
|------|-----------------------------------|---------------------------------|
| Problem definition agreed | User provides a **written problem statement** that the prospect has seen and confirmed — shared in a meeting, sent via email, or documented in meeting notes. Both parties must have explicitly agreed, not just the seller | User wrote a problem statement but hasn't confirmed the prospect agrees with it |
| Success criteria defined | User provides **at least 2 measurable success criteria** with specific targets (numbers, dates, percentages). "Improve efficiency" is not measurable; "Reduce unplanned downtime from 40% to <10% within 6 months" is | User lists vague outcomes ("better performance", "happier team") without measurable targets |
| Stakeholder landscape mapped | User has identified **at least 3 stakeholders by name** with their buying role (economic buyer, technical evaluator, champion, or gatekeeper) and current attitude (supporter/neutral/sceptic/blocker) | User names only one contact or lists roles without names or attitudes |
| Decision process understood | User can describe the **specific steps** to get to a decision — who approves, what the timeline is, whether procurement is involved, and what the budget situation looks like. Must include at least a target decision date | User says "they'll decide soon" or can only describe the process in vague terms |

**SPIN Questions to Prepare**:

*Implication Questions* (reinforce urgency):
- "You mentioned [problem] — how is that affecting [broader goal]?"
- "If we could eliminate [problem], what would that free up for your team?"

*Need-payoff Questions* (let them sell themselves):
- "How would it help if you could [desired outcome]?"
- "What would it mean for your team if [problem] were resolved?"
- "If you had [capability], how would that change your approach to [area]?"
- "What value would you place on being able to [outcome]?"

**Evidence to Document**:
- Agreed problem statement (signed off by prospect)
- Success criteria with measurable targets
- Stakeholder map with buying roles identified
- Decision process timeline and milestones
- Budget indicators or investment appetite

---

### Stage 4: Propose

**Purpose**: Present a tailored recommendation built from diagnostic findings.

**SPIN Focus**: Need-payoff

**Activities**:
- Build a proposal that directly addresses the diagnosed problems
- Link every recommendation to evidence gathered in Stages 2–3
- Present commercial terms clearly
- Confirm the decision process and timeline
- Address anticipated objections proactively

**Gate Criteria** (all must be met — assessed by the skill, not self-certified):
- [ ] Proposal addresses all stated needs (no scope creep, no gaps)
- [ ] Commercial terms clear and understood
- [ ] Decision process and timeline confirmed
- [ ] Key objections addressed

**Right to Advance**: Prospect confirms intent to decide (not necessarily "yes" — but committed to making a decision).

**Minimum Evidence Bar** (what the skill needs to see before it will accept each gate):

| Gate | The skill will accept this when... | The skill will reject this if... |
|------|-----------------------------------|---------------------------------|
| Proposal addresses needs | The skill cross-references the proposal content against every problem and success criterion documented in Stages 2–3. **Every diagnosed problem** must have a corresponding recommendation. The skill will flag gaps | Proposal was sent but the skill cannot verify it maps back to documented problems (user must provide the proposal content or summary) |
| Commercial terms clear | User has documented **specific pricing** (dollar amount or rate), **scope boundaries** (what's in, what's out), and **timeline** (start date, duration, milestones). The prospect must have received these terms | User says "we discussed pricing" without providing the actual figures |
| Decision process confirmed | User provides an **updated and specific** decision timeline — who decides, by when, what steps remain. This must reflect the current state, not what was discussed in Stage 3 | Timeline is recycled from Stage 3 without confirmation it still holds, or user says "they're thinking about it" |
| Objections addressed | User has documented **at least the top objections** raised by the prospect (or explicitly confirmed none were raised) and described how each was handled. The skill will assess whether the responses are substantive | User says "no objections" without evidence of having actually asked, or lists objections without responses |

**Proposal Structure** (use the proposal-template.md reference):
1. Executive Summary — the problem, the cost of inaction, the recommended path
2. Diagnostic Findings — evidence from Stages 2–3
3. Recommended Solution — what you propose and why
4. Success Metrics — tied to the agreed success criteria from Stage 3
5. Investment — pricing, terms, timeline
6. Next Steps — what happens if they say yes

**Evidence to Document**:
- Proposal delivered (date, to whom)
- Prospect feedback on the proposal
- Objections raised and responses given
- Decision timeline confirmed
- Competitors or alternatives being considered

---

### Stage 5: Commit

**Purpose**: Secure formal agreement and transition to delivery.

**SPIN Focus**: Validation

**Activities**:
- Navigate final objections and negotiate terms
- Secure formal commitment (verbal or written)
- Agree on commercial terms (contract, SOW, PO)
- Initiate delivery handover — introduce delivery team
- Set expectations for the engagement

**Gate Criteria** (all must be met — assessed by the skill, not self-certified):
- [ ] Commitment received (verbal agreement or letter of intent)
- [ ] Commercial terms accepted (pricing, scope, timeline)
- [ ] Delivery handover initiated (introduction to delivery team)

**Right to Advance**: Contract signed.

**Minimum Evidence Bar** (what the skill needs to see before it will accept each gate):

| Gate | The skill will accept this when... | The skill will reject this if... |
|------|-----------------------------------|---------------------------------|
| Commitment received | User provides a **specific commitment artefact** — a signed LOI, a verbal "yes" with the name/date/context of who said it, an email confirmation, or a PO number. Must include who committed and when | User says "they're going ahead" without identifying who confirmed and how |
| Commercial terms accepted | User provides the **final agreed terms** — price, scope, timeline, payment terms. These must be the accepted terms, not the proposed terms. Any negotiated changes from the proposal must be documented | User recycles the proposal terms without confirming the prospect formally accepted them |
| Delivery handover initiated | User confirms the **delivery team has been introduced** to the prospect — names who was introduced, when, and the prospect's response. The delivery team must know the engagement context | User says "we'll introduce the team soon" — the introduction must have happened, not be planned |

**Evidence to Document**:
- Signed agreement or PO number
- Final commercial terms
- Delivery team introduced
- Kick-off date confirmed
- Success criteria reconfirmed for delivery

---

### Stage 6: Deliver & Renew

**Purpose**: Execute, demonstrate value, and earn the right to the next engagement.

**SPIN Focus**: Continuous Discovery

**Activities**:
- Deliver on commitments — meet or exceed the agreed success criteria
- Maintain the relationship — regular check-ins, progress updates
- Surface new needs — use ongoing SPIN discovery during delivery
- Document outcomes and build case studies
- Identify expansion or renewal opportunities

**Gate Criteria** (ongoing — assessed by the skill, not self-certified):
- [ ] Outcomes delivered against success criteria
- [ ] Relationship health maintained (regular contact, satisfaction checks)
- [ ] Future needs surfaced through continuous discovery
- [ ] Case study or reference potential identified

**Right to Advance**: New opportunity surfaces → cycle back to Stage 1.

**Minimum Evidence Bar** (what the skill needs to see before it will accept each gate):

| Gate | The skill will accept this when... | The skill will reject this if... |
|------|-----------------------------------|---------------------------------|
| Outcomes delivered | User maps **actual results** against the measurable success criteria defined in Stage 3 — with specific numbers, dates, or metrics showing targets were met or exceeded | User says "they're happy" without demonstrating outcomes against the agreed criteria |
| Relationship maintained | User provides evidence of **regular contact** — meeting dates, check-in summaries, satisfaction indicators. Must show a pattern, not a single data point | User last spoke to the prospect months ago or has no documented check-ins |
| Future needs surfaced | User has identified **at least one specific new need or opportunity** through ongoing SPIN discovery, with enough detail to evaluate whether it warrants a new Stage 1 qualification | User says "there might be more work" without a specific need articulated |
| Case study potential | User has evidence the prospect is **open to being a reference** or has agreed to participate in a case study — or has explicitly documented why not. Must be based on a conversation, not an assumption | User assumes the prospect will be a reference without having asked |

**Evidence to Document**:
- Outcomes delivered vs. success criteria
- Client satisfaction indicators
- New opportunities identified
- Lessons learned
- Reference or case study material

---

## Saving and Resuming Progress

Sales engagements take weeks or months. This skill persists state locally so you can clear context and resume later.

### State File Location

All engagement state is saved to a `.beam/` hidden directory in the current working directory:

```
.beam/
├── engagements/
│   ├── acme-corp.json              # One file per engagement
│   ├── acme-corp-kanban.html       # Auto-generated kanban dashboard (open in browser)
│   ├── bhp-mining.json
│   ├── bhp-mining-kanban.html
│   ├── geelong-port.json
│   └── geelong-port-kanban.html
├── sessions/
│   ├── acme-corp-2026-02-22.md     # Session log per interaction
│   └── acme-corp-2026-02-25.md
└── config.json                      # User's company info (cached)
```

### Auto-Dump Behaviour (CRITICAL)

**At the end of EVERY interaction — no exceptions — automatically dump the following to `.beam/`:**

1. **Update the engagement JSON** (`.beam/engagements/<company>.json`) with:
   - All new evidence collected
   - Gate criteria status changes
   - Stakeholder updates
   - Win probability recalculation
   - Updated `activity_log` with timestamped entry for this session
   - Updated `kanban` object with any new, changed, or completed cards

2. **Regenerate the kanban dashboard** (`.beam/engagements/<company>-kanban.html`):
   - Read the `references/kanban-board.html` template
   - Inject the full engagement JSON as a `BEAM_DATA` JavaScript variable into the HTML
   - Write the self-contained HTML file to `.beam/engagements/<company>-kanban.html`
   - This file can be opened directly in a browser — it contains all data inline
   - **This regeneration happens EVERY session end, not just when the user asks for it**

3. **Write a session log** (`.beam/sessions/<company>-<date>.md`) containing:

```markdown
# Session Log — [Company Name] — [Date]

## What We Covered
- [Summary of what was discussed/worked on this session]

## Key Learnings
- [Learning 1 — what was discovered or confirmed]
- [Learning 2]
- [Learning 3]

## Evidence Collected
- [Evidence item with source and date]

## Gate Progress
- Stage [N]: [Gate criterion] — [MET/UNMET] — [evidence summary]

## Decisions Made
- [Decision 1]
- [Decision 2]

## Next Steps (Pick Up Here)
1. [Specific action — what to do first in the next session]
2. [Second priority action]
3. [Third priority action]

## Open Questions
- [Question that needs answering before progressing]

## Current State
- Stage: [N] — [Name]
- Win Probability: [X%]
- Gates Met: [X/Y]
- Days in Stage: [N]
```

4. **Print a resume hint** to the user:

```
--- Session saved to .beam/ ---
Kanban board updated: .beam/engagements/<company>-kanban.html
To resume next time, run: /beam-selling [Company Name]
```

**This auto-dump happens regardless of whether the user asks to save.** It is the skill's responsibility to ensure no work is lost between sessions.

### Save Behaviour

**Automatically save state** after every meaningful interaction:
- When gate criteria are checked or updated
- When evidence is documented
- When stage transitions occur
- When the user explicitly asks to save
- **At the end of every conversation turn where work was done**

**To save manually**: The user says "save" or "save progress" at any time.

### State File Structure

Each engagement is saved as a JSON file (see `references/beam-state-template.json`). The state includes:

- **Metadata**: Company name, deal name, created/updated dates, current stage
- **User context**: The seller's company, offering, and value proposition
- **Stage progress**: For each stage — status, gate criteria checklist, evidence collected, SPIN notes, key dates
- **Stakeholder map**: Buying committee members and their roles
- **Win probability**: Bayesian estimate updated at each stage
- **Activity log**: Timestamped history of all key actions and decisions
- **Kanban board**: Cards for each stage tracking activities, evidence, blockers, and questions
- **Session logs**: Separate Markdown files per session for easy human reading

### Resume Behaviour

When the user invokes the skill:

1. **Check for existing state**: Look in `.beam/engagements/` for a matching file
2. **If found**: Load the engagement JSON AND the most recent session log from `.beam/sessions/`
3. **Display the resume summary** (see format below)
4. **Read the "Next Steps" from the last session log** — these are the first things to work on
5. **Ask the user for updates** (CRITICAL — see below)
6. **If not found**: Start a new engagement from Stage 1
7. **If multiple found**: List all active engagements and ask which to resume

### Resume Check-In (CRITICAL)

**After displaying the resume summary, you MUST ask the user for updates before proceeding.** Sales engagements happen in the real world between sessions — meetings occur, emails are exchanged, decisions are made. The skill needs to capture what happened offline.

Ask the following:

```
--- Since Last Session ([Date]) ---

Before we continue, let me check in on what's happened since we last worked on this:

1. Have you had any meetings or calls with [Company] since [last session date]?
   - If yes: Who did you meet? What was discussed? Any key takeaways?

2. Have any of the next steps from last session been completed?
   [List the next steps from the last session]

3. Has anything changed?
   - New contacts or stakeholders?
   - Timeline shifts?
   - Budget changes?
   - Competitor activity?
   - Internal changes at the prospect?

4. Any new evidence or insights to capture?
   - Quotes from the prospect
   - Documents shared (proposals, RFPs, specs)
   - Decisions made

Take your time — the more I know, the better I can help you advance this deal.
```

**After the user responds**, update the engagement state with any new information before continuing with the planned work. This ensures the `.beam/` state file always reflects reality, not just what happened in Claude sessions.

### Resume Summary Format

When resuming, display this summary:

```
=== marcov.BEAM — Resuming Engagement ===

Company:        [Name]
Deal:           [Deal name]
Current Stage:  [Stage number and name]
Win Probability: [X%]
Last Session:   [Date — N days ago]
Days in Stage:  [N days]
Days Active:    [N days total]

--- Stage Progress ---
[1] Qualify    ████████████ COMPLETE
[2] Diagnose   ████████░░░░ IN PROGRESS (2/3 gates met)
[3] Align      ░░░░░░░░░░░░ NOT STARTED
[4] Propose    ░░░░░░░░░░░░ NOT STARTED
[5] Commit     ░░░░░░░░░░░░ NOT STARTED
[6] Deliver    ░░░░░░░░░░░░ NOT STARTED

--- Outstanding Gates (Stage 2: Diagnose) ---
[x] Specific problems articulated
[x] Implications quantified
[ ] Cost of inaction acknowledged

--- Last Session Learnings ---
- [Key learning from previous session]
- [Key learning from previous session]

--- Next Steps (from last session) ---
1. [Action item carried forward]
2. [Suggested next action based on current stage]

--- Open Questions ---
- [Unresolved question from last session]

--- Since Last Session Check-In ---
[Asks the user about updates — see Resume Check-In above]
```

---

## Workflow: "Follow the Bouncing Ball"

This is the core interactive workflow. The skill guides the user through each stage sequentially, never skipping ahead.

### Step 1: Initialise

1. Check `.beam/engagements/` for existing state
2. If resuming: load state, display summary, ask where to pick up
3. If new: ask the user for the target company name
4. Check for b2b-research-agent output (HTML report or Markdown dossier)
5. If found: ingest the research as the Stage 1 foundation
6. If not found: offer to run b2b-research-agent first, or proceed with manual input

### Step 2: Gather Seller Context (First Time Only)

If `.beam/config.json` doesn't exist, ask:

1. **Your Company**: Name, what you do (elevator pitch)
2. **Your Offering**: Product or service for this engagement
3. **Your Value Proposition**: Why should prospects choose you?
4. **Your Contact Details**: Name, title, email, phone (for outreach templates)

Save to `.beam/config.json` so this is only asked once.

### Step 3: Work the Current Stage

For each stage, the skill:

1. **Presents the stage overview** — purpose, SPIN focus, gate criteria, and the Minimum Evidence Bar for each gate
2. **Guides the user through activities** — asks SPIN questions, prompts for evidence, challenges vague or unsupported claims
3. **Assesses gate criteria in real-time** — as evidence is provided, the skill runs the three quality tests (Specificity, Source, Recency) and gives immediate feedback on whether a gate criterion would currently pass
4. **Documents evidence** — captures what was learned, with dates, and links evidence to the specific gate criterion it supports
5. **Updates win probability** — Bayesian estimate based on evidence strength (not just gate completion)
6. **Creates kanban cards** — adds activity cards for research, meetings, evidence, stakeholders, blockers, and questions as they arise

### Step 4: Gate Review (Skill-Assessed)

Before advancing to the next stage, the **skill independently assesses** whether the evidence meets the bar. The user does not self-certify.

1. **Display all gate criteria** with their status (met/unmet)
2. **For each gate criterion**, the skill:
   a. Reviews ALL evidence documented for that criterion
   b. Checks against the **Minimum Evidence Bar** defined in the stage definition
   c. Assigns a verdict: **PASS**, **INSUFFICIENT**, or **MISSING**
   d. Provides a brief rationale for the verdict
3. **Display the Gate Assessment** (see format below)
4. **If ALL gates PASS**: the skill advances to the next stage and updates state
5. **If any gate is INSUFFICIENT**: the skill explains exactly what's weak, asks targeted follow-up questions to fill the gaps, and **refuses to advance** until the evidence improves
6. **If any gate is MISSING**: the skill identifies the gap and suggests specific actions to close it
7. **If the deal is dead**: mark as "Closed — Lost" or "Closed — Disqualified" with reasons

**The skill will challenge the user.** If the user says "just advance me" or "I know it's fine", the skill responds:

```
I can't advance this engagement without sufficient evidence — that's the BEAM commitment.
Here's specifically what I need to see before I can pass this gate:

[specific gap description]

This isn't bureaucracy — it's protecting you from advancing a deal that isn't ready.
Let's work on closing these gaps. What can you tell me about [specific question]?
```

**Gate Assessment Display Format**:

```
=== Gate Review — Stage [N]: [Name] ===

  [PASS]         Problem domain identified
                 ✓ Identified: [specific problem domain]
                 ✓ ICP fit rationale provided
                 ✓ Offering-to-problem link clear

  [INSUFFICIENT] Access to authority
                 ✗ Named contact: Jane Smith (CTO) — BUT
                 ✗ No evidence of actual access or relationship
                 → What is your relationship with Jane? Have you spoken directly?

  [MISSING]      Willing to have diagnostic conversation
                 ✗ No evidence provided
                 → Has the prospect agreed to a discovery call? When? How?

--- Verdict: BLOCKED — 1/3 gates passed ---

I need more information on 2 gates before I can advance this engagement.
Let's start with the most critical gap: [specific question]
```

### Step 5: Stage Transition

When advancing:

1. Update the engagement state file
2. Recalculate win probability
3. Present the next stage overview
4. Generate preparation materials (SPIN questions, templates, checklists)

### Step 6: Output Generation

At key milestones, generate deliverables:

| Stage | Deliverable |
|-------|-------------|
| After Stage 1 | Qualification summary and discovery call agenda |
| After Stage 2 | Diagnostic findings report |
| After Stage 3 | Alignment memo (shared problem definition and success criteria) |
| After Stage 4 | Formal proposal (from proposal-template.md) |
| After Stage 5 | Engagement kickoff brief |
| After Stage 6 | Outcomes report and case study draft |

---

## Win Probability (Bayesian Estimate)

Update the win probability at each stage transition. This is a rough Bayesian prior, not a precise calculation.

### Base Rates

| Stage | Base Win Probability | Reasoning |
|-------|---------------------|-----------|
| Stage 1: Qualify | 10% | Most qualified leads don't convert |
| Stage 2: Diagnose | 25% | Real pain confirmed increases odds |
| Stage 3: Align | 45% | Shared understanding is a strong signal |
| Stage 4: Propose | 60% | Proposal requested = serious interest |
| Stage 5: Commit | 80% | Intent to decide = high confidence |
| Stage 6: Deliver | 95% | Contract signed, execution underway |

### Modifiers

Adjust the base rate up or down based on evidence:

| Signal | Modifier |
|--------|----------|
| Champion identified and active | +10% |
| Economic buyer engaged directly | +10% |
| Competitor incumbent with long contract | -15% |
| Budget confirmed and allocated | +15% |
| Multiple stakeholders aligned | +10% |
| No clear decision timeline | -10% |
| Prospect initiated contact (inbound) | +10% |
| Procurement process required | -5% |
| Strong prior relationship | +10% |
| Political or organisational change underway | -10% |

---

## SPIN Selling Integration

SPIN (Situation, Problem, Implication, Need-payoff) is woven into every stage.

### SPIN by Stage

| Stage | Primary SPIN | Secondary SPIN | Intensity |
|-------|-------------|---------------|-----------|
| 1. Qualify | Situation | — | Low |
| 2. Diagnose | Problem | Implication | **High** |
| 3. Align | Implication | Need-payoff | **High** |
| 4. Propose | Need-payoff | — | Medium |
| 5. Commit | Validation | — | Low |
| 6. Deliver | Continuous Discovery | All types | Medium |

### SPIN Question Reference

See `references/spin-question-bank.md` for a comprehensive bank of SPIN questions organised by stage and topic area.

---

## Gate Enforcement Protocol

The skill is the gatekeeper. It does not rely on the user to self-certify readiness. Instead, it independently evaluates the quality, specificity, and completeness of the evidence before allowing progression.

### Core Philosophy: Earn the Right

Every stage transition in BEAM must be **earned, not claimed**. The user earns the right to advance by demonstrating — through evidence documented in the engagement — that they have done the work required at that stage. The skill's job is to:

1. **Hold the line** — refuse to advance when evidence is thin, vague, or missing
2. **Challenge constructively** — explain exactly what's weak and why it matters
3. **Guide the fix** — ask targeted questions that help the user close the gap
4. **Celebrate the pass** — when evidence is solid, acknowledge the work and advance with confidence

### Evidence Quality Assessment

When the user requests advancement (via `advance` command or reaching the end of a stage), the skill evaluates each gate criterion using three tests:

**Test 1: Specificity** — Is the evidence specific or generic?
- PASS: Names, dates, numbers, direct quotes, concrete details
- FAIL: Vague statements, assumptions, generalisations, industry truisms

**Test 2: Source** — Does the evidence come from the right place?
- PASS: Evidence from the prospect (their words, their data, their agreement)
- FAIL: Evidence that is only the seller's interpretation or assumption about the prospect

**Test 3: Recency & Relevance** — Is the evidence current and connected?
- PASS: Evidence is from a recent interaction and directly supports the gate criterion
- FAIL: Evidence is stale, recycled from a different context, or only tangentially related

Each gate criterion must pass **all three tests** to be marked as met.

### Skill Assessment Behaviour

The skill behaves differently depending on the evidence quality:

**Strong Evidence (all tests pass)**:
```
✓ PASS — [Gate criterion]
  Evidence: [Summary of what was provided]
  Assessed: Specific, prospect-sourced, current
```
The skill marks the gate as met and moves on.

**Partial Evidence (1-2 tests fail)**:
```
⚠ INSUFFICIENT — [Gate criterion]
  Evidence provided: [What was given]
  Gap: [Which test(s) failed and why]
  → [Specific question to close the gap]
```
The skill does NOT mark the gate as met. It asks a targeted follow-up question to help the user strengthen the evidence. The user must provide better evidence before the skill will re-assess.

**No Evidence**:
```
✗ MISSING — [Gate criterion]
  No evidence documented for this criterion.
  → [Suggested action to obtain the evidence]
```
The skill flags the gap and suggests what the user needs to do (in the real world, not in the tool) to get the evidence.

### Handling Pushback

Users may push back when the skill blocks advancement. The skill handles this firmly but constructively:

**"Just advance me, I know it's ready"**
→ "I understand you feel confident, but BEAM's value is in the discipline. Specifically, I need [X] before I can pass [gate]. Can you help me with that?"

**"This is just a formality"**
→ "If the evidence exists, it should be quick to document. What I'm missing is [specific gap]. Can you fill that in?"

**"I don't have that level of detail"**
→ "That's actually an important signal — if we don't have [specific evidence], the deal might not be as far along as we think. Let's talk about how to get it."

**"The prospect told me verbally"**
→ "Great — I'll take verbal evidence. Who said it, when, and what were the exact words (or close to)? I just need it documented so we can build on it."

**"Override this"**
→ "There is no override. That's the BEAM commitment — evidence earns advancement. But I can help you close this gap quickly. Here's what I suggest: [specific action]"

The skill **never** allows a gate to be bypassed, overridden, or marked as met without evidence that passes all three quality tests. This is non-negotiable.

### Gate Assessment Verdicts

After assessing all gate criteria for a stage, the skill issues one of three verdicts:

| Verdict | Condition | Action |
|---------|-----------|--------|
| **ADVANCE** | All gates PASS | Proceed to next stage, update state, celebrate |
| **BLOCKED** | 1+ gates INSUFFICIENT or MISSING | Refuse to advance, present gaps, guide the user to close them |
| **EXIT** | Evidence suggests the deal is not viable | Recommend qualifying out — closing as lost or disqualified is a legitimate and respected outcome |

### Evidence Strength and Win Probability

The quality of evidence at each gate directly influences the win probability modifier:

| Evidence Quality | Win Probability Effect |
|-----------------|----------------------|
| All gates passed with strong evidence (quotes, metrics, dates) | Base rate + all applicable positive modifiers |
| Gates passed but evidence is at minimum bar | Base rate only — no positive modifiers applied |
| Gates have lingering weaknesses (passed but barely) | Base rate − 5% per weak gate |

This means the skill doesn't just check a box — it distinguishes between "technically passed" and "strongly passed", and the win probability reflects that distinction.

### Continuous Gate Monitoring

Gates are not just assessed at the `advance` command. The skill also:

1. **Monitors during the session** — if new evidence strengthens or weakens a gate, update the assessment in real-time
2. **Flags regression** — if new information contradicts previously documented evidence (e.g., a stakeholder leaves the organisation), the skill can **re-open a gate** that was previously met
3. **Cross-references across stages** — if Stage 3 evidence contradicts Stage 2 evidence, the skill flags the inconsistency

---

## Stakeholder Mapping

Track the buying committee throughout the engagement:

| Role | Description | Typical Titles |
|------|-------------|---------------|
| **Economic Buyer** | Controls the budget; makes the final financial decision | CEO, CFO, VP, GM |
| **Technical Evaluator** | Assesses solution fit and technical feasibility | CTO, Head of IT, Engineering Director |
| **Champion / Sponsor** | Internally advocates for your solution; feels the pain most | Director, Senior Manager, Program Lead |
| **Gatekeeper** | Controls access to decision-makers and process | EA, Procurement Manager, PMO |
| **End User** | Will use the solution day-to-day; influences adoption | Team leads, operators, analysts |

For each stakeholder, track:
- Name, title, and contact details
- Their role in the buying committee
- Their attitude (Supporter / Neutral / Sceptic / Blocker)
- What they care about most (priorities, KPIs, fears)
- Engagement history (meetings, emails, calls)

---

## Engagement Timeline

Because engagements run over weeks or months with many sessions in between, the skill maintains a comprehensive timeline in the engagement state file.

### Timeline Data Captured

Every session and every significant event is timestamped and logged:

- **Engagement start date**: When the opportunity was first created
- **Target close date**: When you aim to close (set during qualification, updated as needed)
- **Stage transitions**: Date of every stage change, with days spent in each stage
- **Key dates**: First contact, discovery call, diagnostic complete, alignment, proposal, contract, delivery start
- **Milestones**: Custom milestones added during the engagement (e.g., "Met CFO", "Presented to board")
- **Session history**: Every session date with a summary of what was covered

### Timeline Display

When the user asks for `status` or `timeline`, display:

```
=== marcov.BEAM — Engagement Timeline ===

Company:          [Name]
Engagement Start: [Date]
Target Close:     [Date]
Days Active:      [N days]
Deal Value:       [Value]

--- Timeline ---
[Date]  Stage 1 — Qualify
        ├── [Date] Created engagement from b2b-research dossier
        ├── [Date] Session: Confirmed ICP alignment, identified problem domain
        ├── [Date] Discovery call scheduled with [Name]
        └── [Date] GATE PASSED — Agreed to diagnostic conversation

[Date]  Stage 2 — Diagnose (current — [N days])
        ├── [Date] Session: Ran SPIN discovery, uncovered 3 problems
        ├── [Date] Session: Quantified implications — $X annual impact
        └── [Date] Session: [Most recent activity]

--- Upcoming ---
[ ] Cost of inaction acknowledged (Stage 2 gate)
[ ] Problem definition agreed (Stage 3 gate)
[ ] Target close: [Date]
```

### Overview Timeline File

In addition to the JSON state, the skill maintains a human-readable timeline file at `.beam/sessions/<company>-timeline.md`:

```markdown
# [Company Name] — Engagement Timeline

## Overview
| Field | Detail |
|-------|--------|
| **Started** | [Date] |
| **Current Stage** | [Stage N — Name] |
| **Days Active** | [N] |
| **Win Probability** | [X%] |
| **Target Close** | [Date] |
| **Deal Value** | [Value] |

## Stage History

### Stage 1: Qualify ([Start Date] → [End Date] — [N days])
- [Date]: [What happened]
- [Date]: [What happened]
- **Gate passed**: [Date] — [Evidence summary]

### Stage 2: Diagnose ([Start Date] → present — [N days])
- [Date]: [What happened]
- [Date]: [What happened]

## Key Milestones
| Date | Milestone | Notes |
|------|-----------|-------|
| [Date] | [Milestone] | [Notes] |

## Session Log
| # | Date | Stage | Summary | Next Steps |
|---|------|-------|---------|------------|
| 1 | [Date] | Qualify | [Summary] | [Next steps] |
| 2 | [Date] | Qualify | [Summary] | [Next steps] |
| 3 | [Date] | Diagnose | [Summary] | [Next steps] |
```

This timeline file is updated at the end of every session alongside the JSON state and individual session logs. It serves as the "master narrative" of the engagement.

---

## Commands

The skill responds to these commands within a session:

| Command | Action |
|---------|--------|
| `save` | Save current engagement state to `.beam/` |
| `status` | Display current stage, gate progress, and win probability |
| `board` | Regenerate and open the kanban dashboard (`.beam/engagements/<company>-kanban.html`) |
| `timeline` | Show the full engagement timeline with dates and milestones |
| `gates` | Show gate criteria for the current stage |
| `evidence` | Show all evidence collected for the current stage |
| `stakeholders` | Show the stakeholder map |
| `history` | Show the activity log |
| `probability` | Show and recalculate win probability |
| `next` | Suggest what to do next based on current state |
| `advance` | Attempt to advance to the next stage (triggers gate review) |
| `back` | Review a previous stage (does not reverse progress) |
| `close` | Close the engagement (won, lost, or disqualified) |
| `list` | List all active engagements in `.beam/` |
| `export` | Export engagement as Markdown summary |

---

## Content Writing Guidelines

### Tone
- **Consultative and strategic** — you are a trusted advisor, not a pushy salesperson
- **Evidence-based** — cite specific findings, quotes, and data points
- **Action-oriented** — every output should lead to a clear next step
- **Honest** — if the deal is weak, say so; qualifying out is a good outcome

### Australian English
- Use Australian spelling throughout (organisation, behaviour, colour, prioritise, analyse)

### Formatting
- Use progress bars and status indicators for visual clarity
- Use tables for structured data (gate criteria, stakeholder maps, evidence logs)
- Use direct quotes from prospects where available
- Include dates on all evidence and activities

---

## Kanban Board

The skill maintains an interactive kanban dashboard that visualises activities and progress across all 6 BEAM stages. The board is regenerated as a self-contained HTML file at the end of **every session**.

### How It Works

1. **During the session**: As activities happen (research, meetings, evidence captured, stakeholders identified, blockers raised, questions opened), the skill adds **cards** to the `kanban` property in the engagement JSON
2. **At session end**: The auto-dump reads `references/kanban-board.html`, injects the engagement JSON as `BEAM_DATA`, and writes a standalone HTML file to `.beam/engagements/<company>-kanban.html`
3. **To view**: Open the HTML file in any browser — no server needed, all data is inline

### Kanban Generation Procedure

When generating the kanban HTML (at session end or on `board` command):

```
1. Read the engagement JSON from .beam/engagements/<company>.json
2. Read the template from references/kanban-board.html
3. Insert a <script> tag before the closing </body>:
   <script>const BEAM_DATA = { ...engagement JSON... };</script>
4. Write the combined file to .beam/engagements/<company>-kanban.html
5. Report the file path to the user
```

### Card Types

Cards represent different activities within each stage column:

| Icon | Type | Use When |
|------|------|----------|
| `[R]` Research | Desk research, web search, dossier review |
| `[M]` Meeting | Call, meeting, or conversation with prospect |
| `[E]` Evidence | Evidence captured or documented (quotes, metrics, agreements) |
| `[D]` Document | Deliverable produced (proposal, memo, agenda, report) |
| `[S]` Stakeholder | New stakeholder identified or engaged |
| `[!]` Blocker | Something preventing progress |
| `[?]` Question | Open question needing an answer |

### Card Statuses

| Status | Meaning |
|--------|---------|
| `todo` | Not yet started — planned activity |
| `doing` | In progress — currently being worked on |
| `done` | Completed — activity finished |
| `blocked` | Waiting on external input or action |

### When to Create Cards

Add kanban cards automatically when these events occur during a session:

- **Stage entered** → Add cards for the key activities in that stage (as `todo`)
- **Research performed** → Add an `[R]` card summarising what was found
- **Meeting/call discussed** → Add an `[M]` card with attendees and outcomes
- **Evidence captured** → Add an `[E]` card linking to the gate criterion it supports
- **Stakeholder identified** → Add an `[S]` card with name, role, and attitude
- **Blocker discovered** → Add a `[!]` card describing what's stuck and why
- **Question raised** → Add a `[?]` card with the open question
- **Document produced** → Add a `[D]` card with the document type and path
- **Activity completed** → Update existing card status to `done` with completion date
- **Gate criterion met** → Update the relevant `[E]` card and set its `gate_ref`

### Card JSON Schema

Each card in the `kanban` state follows this structure:

```json
{
  "id": "2-003",
  "type": "evidence",
  "icon": "E",
  "title": "Quantified $2.1M annual impact",
  "status": "done",
  "created_at": "2026-02-15",
  "completed_at": "2026-02-15",
  "due_date": null,
  "owner": "seller",
  "notes": "CTO confirmed reactive maintenance costs $2.1M/year in unplanned downtime",
  "evidence_ref": "implications_quantified",
  "gate_ref": "implications_quantified"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Stage number prefix + sequential number (e.g., `1-001`, `2-003`) |
| `type` | enum | `research`, `meeting`, `evidence`, `document`, `stakeholder`, `blocker`, `question` |
| `icon` | string | Display icon: `R`, `M`, `E`, `D`, `S`, `!`, `?` |
| `title` | string | Short card title (max 40 chars) |
| `status` | enum | `todo`, `doing`, `done`, `blocked` |
| `created_at` | date | When the card was created |
| `completed_at` | date | When completed (null if not done) |
| `due_date` | date | Optional due date for `todo` items |
| `owner` | string | Who owns this: `seller`, `prospect`, or a person's name |
| `notes` | string | Detailed notes, context, or findings |
| `evidence_ref` | string | Links to an evidence item in the stage's evidence array |
| `gate_ref` | string | Which gate criterion this card supports (if any) |

### Board Features

The generated HTML kanban board includes:

- **6 columns** — one per BEAM stage, colour-coded
- **Stage status badges** — Complete / Active / Pending
- **Gate progress bars** — visual fill showing gates met vs total
- **Gate criteria checklists** — individual criteria with met/unmet indicators
- **Activity cards** — typed, colour-coded cards with status, date, owner, and gate links
- **Card detail modal** — click any card to see full notes, evidence, and metadata
- **Add card** — interactive form to add new cards (for visual tracking between sessions)
- **Header metrics** — win probability, current stage, days active, deal value
- **Light/dark theme** — toggle with button, persists to localStorage
- **SPIN focus labels** — each column shows the primary SPIN questioning focus for that stage
- **Print-friendly** — use browser print for a clean snapshot of the board

---

## Checklist

Before saving or advancing, verify:

- [ ] Current stage activities completed
- [ ] All gate criteria assessed (met or explicitly unmet)
- [ ] Evidence documented with dates and sources
- [ ] Stakeholder map updated
- [ ] Win probability recalculated
- [ ] Kanban cards added/updated for activities this session
- [ ] Next steps identified
- [ ] State file saved to `.beam/engagements/`
- [ ] Kanban dashboard regenerated to `.beam/engagements/<company>-kanban.html`
- [ ] Activity log updated
