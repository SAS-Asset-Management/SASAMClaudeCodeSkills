---
name: maturity-parse
description: Structured artefact review workflow — the "what they say they do" pipeline. Use when the assessor says "parse this document", "walk me through this artefact", "review this doc with me", or "prep this for scoring". Consumes an artefact already registered by maturity-intake plus the engagement's generated standard chunks, and produces a recorded review at reviews/NN_<artefactName>_review.md containing a delta table cited to clause and chunk, the assessor discussion, and the agreed interpretation. Scoring never happens without this review on record.
version: 1.0.0
---

# Maturity Parse Skill

This skill governs how artefacts are reviewed before any maturity scoring occurs. It enforces a strict order — parse, compare, open, present, discuss, record, then hand off — so that scoring is never applied to an artefact the assessor has not personally engaged with. The standard the client is held to is the MDR standard (or whichever governing document the resolved pack declares), consumed only through the engagement's generated chunk files, never from memory and never as the whole document.

## Workflow

Execute the seven phases in order, after the bootstrap. Do not compress or reorder.

### 0. Bootstrap the engagement context

- Load `engagement.yaml` from the engagement repo root. Stop if it is absent.
- Resolve the framework pack: the engagement's `packs/<packId>/` overlay first, then `${CLAUDE_PLUGIN_ROOT}/packs/<packId>/`.
- Read `pack.yaml` for the taxonomy and scale. Never assume a subject count or a domain count.
- Confirm the standard chunks exist at the engagement's `packs/<packId>/standard/` with an `INDEX.md`. **If the chunks are missing, stop and instruct the assessor to generate them with `python3 engine/chunker.py --pdf <path> --manifest <manifest.yaml> --out <dir>` from the licensed document — never proceed from memory of the standard.**

### 1. Parse

Read the document. Produce a structured briefing containing:

- Title (exact), author or issuing function, issue date and current revision
- Stated scope and purpose
- Key sections (headings, tables, appendices)
- Explicit claims made by the document
- Visible assumptions (what the document takes for granted)
- Artefact type (procedure, plan, register, report, specification, presentation, data extract)
- Candidate subjects from the pack taxonomy the artefact might inform

Apply the adaptive fidelity rules:

- **Documents over about 50 pages** get sectioned briefings rather than one global summary, discussed section by section.
- **Recurring record types** (the fifth near identical inspection report) get a light triage template: metadata, what changed against the prior instance, anything anomalous.
- **CSVs and calculation datasets** are not read here — route them to the maturity-validate skill and record the routing in the review.

### 2. Compare against the standard chunks

Work out which sections of the standard are relevant and load **only those**.

1. Read the standard `INDEX.md` for the topic to chunk routing.
2. Select the chunk files matching the artefact's topics. When the artefact contains records conditioned on a specific class or category the standard treats separately, load the matching chunk for **every** class present before making any conformance call — a generic clause frequently has class specific overrides.
3. Read the selected chunks and extract what the standard actually requires (data, methodology, frequency, quality, scope) with the specific clause or table being compared against.
4. Produce the **delta table** — the atomic evidentiary unit of the engagement. One row per requirement:

| Requirement | Artefact Position | Alignment | Notes |
| --- | --- | --- | --- |

Alignment takes exactly one of: Meets, Partial, Gap, Exceeds, Not applicable. Every row cites the specific clause and the specific chunk file it was compared against. See references/deltaTable.md for row construction detail and worked examples.

**Never compare against the standard from memory — always load the relevant chunks and cite them.** Never load the full governing document. If a needed section is not chunked, stop and tell the assessor — do not guess at requirements.

### 3. Open

Present the file to the assessor so they can see what the skill is describing. State the absolute path and offer to open it with the platform's opener. Do not assume an operating system — ask, or use the command the assessor prefers. Always quote the path.

### 4. Present

Give the assessor:

- Key takeaways (three to five bullets)
- **The delta table** from Phase 2, with the chunk file and clause cited per row — the delta is the spine, everything else orbits it
- Possible subject relevance (which taxonomy subjects this artefact might evidence and at what indicative level)
- Anything surprising (inconsistencies, scope shifts, unexpected authorship, missing sections)
- Red flags (undeclared assumptions, missing document control, gaps between claim and evidence)

Keep it tight. The goal is to orient the assessor, not to pre empt their judgement.

### 5. Discuss

Ask the assessor probing questions **one at a time** — multiple choice where possible, wait for each answer. Probing lines:

- Does the document actually demonstrate what it claims?
- Is this the current revision, or superseded?
- Does the assessor's tacit knowledge of the client confirm or contradict the reading?
- Which subjects does the assessor think this evidences, and at what indicative level?
- On each delta row — does the assessor agree with the Meets, Partial, Gap call, or read it differently?
- Are there client constraints or history that explain an apparent Gap?

**The auditor's read always wins.** Capture their interpretation, added context, and every point of disagreement with the skill's reading.

### 6. Record

Write the review to:

```
reviews/NN_<artefactName>_review.md
```

using the review number already allocated by maturity-intake (never allocate a fresh one here). The file must contain: document metadata; the briefing; the standard chunks consulted (listed by file); the delta table with the assessor agreed alignment calls; assessor commentary; any disagreements with the assessor's view recorded as the resolution; and the final agreed interpretation — which subjects it evidences and at what indicative level.

### 7. Hand off

Only after the discussion is recorded, hand off to the maturity-score skill for tagging and scoring. Make it explicit:

> Handing off to maturity-score for tagging against subjects 03, 07, and 12. Review file reviews/07_assetDataStandard_review.md.

## Guardrails

- Never score or codify an artefact without a recorded parse and discussion. Scoring without a recorded parse is forbidden and hook enforced.
- **Never compare against the standard from memory — always load the relevant chunk files and cite them.**
- **Never load the full governing document.** Load only the chunks selected via the standard `INDEX.md`. If a needed section is not chunked, stop and tell the assessor.
- **If the standard chunks are missing entirely, stop and instruct the assessor to run engine/chunker.py — never proceed from memory of the standard.**
- Match the strength of the conformance call to the strength of the citation. A hard Gap call needs a specific clause; where the specific chunk has not been loaded, record a potential gap pending verification instead.
- Alignment values are exactly Meets, Partial, Gap, Exceeds, Not applicable — no synonyms.
- One question at a time in the discussion phase.
- If the assessor disagrees with the skill's reading, the assessor's interpretation wins. Record the disagreement rather than suppressing it.
- Never invent artefact names or facts. Only reference documents that exist under `evidence/`.
- Documents over about 50 pages get sectioned briefings; CSVs route to maturity-validate.
- Australian English throughout. No hyphens in prose — em dashes or rephrase. No emojis. camelCase file names. DD/MM/YYYY displayed dates.

## Invocation

Trigger this skill on any of the following:

- "Parse this document"
- "Walk me through this artefact"
- "Review this doc with me"
- "Prep this for scoring"

On trigger, execute the seven phases in order. Do not compress or reorder them.
