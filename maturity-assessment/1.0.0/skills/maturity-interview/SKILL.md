---
name: maturity-interview
description: Design and run the stakeholder interview programme — the "what they actually do" pipeline. Use when the assessor says "develop the interview programme", "plan the interviews", "design the fieldwork", "what should I ask this cohort", or "prep this session". Consumes the pack's questionBank (core.md plus cohorts/), the current evidence gaps from reviews/ and scoreLedger.json, and the engagement's interviewCeiling, and produces a tiered roster with budget arithmetic, artefact anchored question packs, a timeboxed session script, and transcripts in interviews/ processed into interviews/NN_<subjectName>_notes.md by the transcript-extractor agent before any reconciliation.
version: 1.0.0
---

# Maturity Interview Skill

This skill produces interview programmes that generate maturity scoring evidence, not general commentary. The sole investigative purpose of a session is to test the gap between what the organisation says it does (its artefacts) and what it actually does (lived practice). Every question traces to a maturity subject and a named artefact — if it cannot, it does not belong in the programme.

## Workflow

Execute the phases in order. Do not compress or reorder.

### 1. Bootstrap the engagement context

- Load `engagement.yaml` from the engagement repo root. Stop if absent. Note `engagement.interviewCeiling` — the hard budget for one on one sessions.
- Resolve the framework pack: engagement `packs/<packId>/` overlay first, then `${CLAUDE_PLUGIN_ROOT}/packs/<packId>/`.
- Read `pack.yaml` for the taxonomy — never assume a subject count or a domain count.
- Read the pack's `questionBank/core.md` (the fixed cross session question set) and the cohort probe files under `questionBank/cohorts/`.

### 2. Classify the evidence gaps

Before drafting a single question, classify what the current artefact derived picture is missing, subject by subject, using the fixed gap typology — exactly these five types:

- **procedural** — the documented process exists but its lived execution is unverified
- **evidence** — a claim has no artefact behind it, or the artefact was requested and never arrived
- **contradiction** — two sources disagree and only a practitioner can arbitrate
- **recency** — the evidence exists but may be superseded or stale
- **coverage** — whole subjects or organisational areas the artefacts simply do not reach

Read `scoreLedger.json` for thin subjects (few evidence records, Low confidence, `lowOutlier` flags) — these drive the targeting. Delegate gap classification and question drafting to the `interview-prep` agent where available.

### 3. Build the tiered roster within the ceiling

Budget is always the constraint. Build the roster in three tiers and show the arithmetic:

- **Tier 1 — core (must do).** Roles that directly author, approve, or execute the assessed process: sponsor, accountable executive, process owner, and a representative frontline voice per stream.
- **Tier 2 — targeted (complete the picture).** Hands on analytical and operational roles that corroborate or contradict Tier 1 claims.
- **Tier 3 — reserve (activate on demand).** Names held back, activated only when Tier 1 and 2 sessions reveal specific signal gaps.

Tier 1 plus Tier 2 must not exceed `engagement.interviewCeiling`. **State the budget arithmetic explicitly** — sessions available, sessions allocated per tier, and a one line justification for every inclusion and every exclusion. The assessor may disagree; the programme must make the choice defensible either way. See references/rosterDesign.md for the tiering heuristics and the session timebox template.

### 4. Map artefact touchpoints per interviewee

Non negotiable. For every Tier 1 and Tier 2 interviewee, build an artefact touchpoint table: which artefacts they authored, approved, work from, or are accountable for; why each matters in that session; and a pre written say versus do probe anchored to that artefact. Where maturity-parse has produced a review, reference the review file so the interviewer can pre read it. Walk the full `evidence/` inventory when building the tables — never rely on memory of earlier reviews.

**No probe without a named document.**

### 5. Assemble the question packs

Every session opens with the fixed core set from `questionBank/core.md`, asked identically in every session for cross session comparability. Then add cohort probes drawn from the matching `questionBank/cohorts/<archetype>.md`, tailored to the interviewee's touchpoints and the classified gaps.

Every drafted question must be:

- **Specific** — names an artefact, a system, or a record ("Walk me through the last entry in…")
- **Open** — asks for behaviour, not a yes or no ("…how does that actually happen?")
- **Traceable** — maps to at least one maturity subject AND a named artefact
- and carries a **pre registered listen for** — the scoring cue the interviewer is listening for, written down before the session so hindsight cannot reshape it.

### 6. Script and schedule the sessions

Timebox every session and write the script: framing (a governance review, not an audit; cohort level attribution for frontline voices; observer role declared; consent to capture), role walk through, artefact anchored probes, evidence and examples ("give me an asset ID, a date, a record we can trace"), pain points, and a close that confirms follow up evidence requests. Propose a complete schedule (day, time, mode) the client coordinator can action as one committed proposal. Record the capture tool from `data.captureTool` in `engagement.yaml`.

### 7. Capture and extract

Raw transcripts land in `interviews/`. After each session, the `transcript-extractor` agent processes the transcript into `interviews/NN_<subjectName>_notes.md` — subject tagged quotes, each marked as strengthening or gapping the current score, with timestamp and speaker. **Reconciliation never consumes a raw transcript** — the maturity-reconcile skill reads only the extracted notes. Follow up artefact requests raised in session go back through maturity-intake.

## Guardrails

- Every probe maps to at least one maturity subject AND a named artefact. No probe without a named document.
- Tier 1 plus Tier 2 never exceeds `engagement.interviewCeiling`. The budget arithmetic is written into the programme, with every inclusion and exclusion justified.
- Gap typology values are exactly procedural, evidence, contradiction, recency, coverage.
- Questions are Specific, Open, and Traceable, each with a pre registered listen for cue.
- The core question set comes from the pack's `questionBank/core.md` and is asked in every session — comparability depends on it. Do not swell the core set; role tailoring lives in the cohort probes.
- Raw transcripts are processed by the transcript-extractor agent into subject notes before any reconciliation. Never feed a raw transcript to maturity-reconcile.
- Frontline voices are attributed at cohort level, never individually. State this at the top of every frontline session.
- Say versus do is the core question — everything else is colour.
- Never assume the subject count — enumerate from the pack taxonomy.
- Australian English throughout. No hyphens in prose — em dashes or rephrase. No emojis. DD/MM/YYYY displayed dates.

## Invocation

Trigger this skill on any of the following:

- "Develop the interview programme"
- "Plan the interviews"
- "Design the fieldwork"
- "What should I ask this cohort"
- "Prep this session"

On trigger, execute the seven phases in order. Do not compress or reorder them.
