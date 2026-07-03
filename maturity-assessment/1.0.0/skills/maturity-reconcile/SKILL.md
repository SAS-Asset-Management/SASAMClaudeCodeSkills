---
name: maturity-reconcile
description: Reconcile the say layer (artefact reviews plus ledger evidence) against the do layer (interview notes) into a final per subject finding — the only pathway authorised to produce one. Use when the assessor says "reconcile subject NN", "synthesise the finding", "say versus do for this subject", or "close out this subject". Consumes reviews/, the subject's evidence records in scoreLedger.json, and interviews/NN_<subjectName>_notes.md, and produces findings/runNN/NN_<subjectName>_finding.md with provenance frontmatter and visible epistemics, plus sayScore, doScore, and any dispute records written to scoreLedger.json before the engine reruns. Refuses with "interview pending" when the do input is missing.
version: 1.0.0
---

# Maturity Reconcile Skill

This is the highest judgement step in the engagement and the only pathway authorised to produce a final finding. It answers, for one subject at a time, the engagement's core question: do they actually do what they say? The agent proposes; the assessor rules; unresolved disagreements become open disputes for an auditor call — never silent resolutions.

## Workflow

Execute the phases in order. Do not compress or reorder.

### 1. Bootstrap the engagement context

- Load `engagement.yaml` from the engagement repo root. Stop if absent.
- Resolve the framework pack: engagement `packs/<packId>/` overlay first, then `${CLAUDE_PLUGIN_ROOT}/packs/<packId>/`.
- Read `pack.yaml` for the taxonomy and scale, and the subject's rubric at `rubrics/NN_subjectName.md`. Never assume a subject count.
- Confirm the subject with the assessor before reading anything else.

### 2. Verify both inputs exist — refuse otherwise

- **Say input:** the subject's evidence records in `scoreLedger.json`, the reviews in `reviews/` mapped to this subject, and the rendered narrative in `scoring/` if present.
- **Do input:** the extracted notes at `interviews/NN_<subjectName>_notes.md`.

**If the do input is missing, do not invent — return "interview pending" and stop.** If the say input is missing, stop and route the subject back through maturity-parse and maturity-score. This skill never proceeds on one leg, and the `finding-synthesiser` agent it delegates to enforces the same refusal.

### 3. Read the say position

From the ledger and reviews, state the score the artefacts alone would warrant, with its evidence basis and confidence. Keep the rubric criteria for the levels under consideration visible while reasoning.

### 4. Read the do position

From the interview notes, extract:

- **Confirmations** — where practice reinforces the artefact picture
- **Contradictions** — where practice diverges from the documentation (this almost always lowers the score)
- **New evidence** — practices the artefacts did not capture (can raise or lower)
- **Commitments** — forward actions mentioned in session (the commitment-tracker agent logs these; note them as context, do not duplicate)

State the score the interviews alone would warrant.

### 5. Apply the tie break decision table

The settled table. Apply it exactly — no improvisation:

| Situation | Rule |
| --- | --- |
| Artefacts claim more than interviews evidence | Take the lower |
| Interviews evidence more than artefacts document | Accept, but cap confidence at Medium |
| Say and do agree | High confidence |
| One side missing | Drop confidence a notch |

Documentation is necessary but not sufficient; informal practice does not survive turnover. Settle a final score 0 to 5 and a confidence of exactly Low, Medium, or High. Where the say and do readings cannot be reconciled — or the assessor disagrees with the proposed settlement — record an open dispute rather than forcing a number.

### 6. Write the finding with provenance and epistemics

Determine the current run NN (from the `runs` array in `scoreLedger.json`, or the highest existing `findings/runNN/` directory) and write `findings/runNN/NN_<subjectName>_finding.md` with:

- **Provenance frontmatter:** subject, domain, finalScore, confidence, date, `saySources` (list of reviews and scoring files) and `doSources` (list of interview note files)
- **Visible epistemics:** what the artefacts alone would score, what the interviews alone would score, and why the final differs — the reconciliation is the interesting part and it is written out, not implied
- Strengths cited with evidence references; gaps blocking a higher score, each citing the rubric criterion at the next level it would take to clear
- Recommendations as discrete actions — action verb and object with rationale. No delivery horizons, no dates, no owners: sequencing delivery is the client's call.

Only the `finding-synthesiser` agent (or this skill acting through it) writes to `findings/` — hook enforced.

### 7. Update the ledger and rerun the engine

Write to `scoreLedger.json` per the shared contract: the subject's `sayScore`, `doScore`, and any dispute records shaped `{id, raised (YYYY-MM-DD), description, status: "open", resolution: null}`. Then rerun:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/engine/aggregate.py --repo <engagementRoot> --run-trigger "reconciliation of subject NN"
```

The engine — never this skill — updates `final`, `ci`, `history`, and `flag`.

### 8. Present to the assessor for ruling

Summarise the finding to the assessor: final score, the two line reconciliation, the recommendation count, and any open dispute. **The assessor rules, the agent proposes.** If the assessor overrules, record their ruling as the resolution and update the finding and the dispute record; if the disagreement stands, the dispute stays open for an auditor call. An open dispute holds the report gate closed by design.

## Guardrails

- This skill is the only pathway to a final finding, and only the finding-synthesiser agent writes to `findings/`.
- **Both inputs or refusal.** If the do input is missing, return "interview pending" and stop. Never invent interview evidence. Never proceed on the say leg alone.
- Apply the tie break table exactly: artefacts over claiming take the lower; interview only maturity caps confidence at Medium; agreement earns High; a missing side drops confidence a notch.
- Unresolved disagreements are logged as open disputes for an auditor call — never silently resolved. The assessor rules, the agent proposes.
- Every finding carries provenance frontmatter (saySources, doSources) and visible epistemics — the say alone score, the do alone score, and why the final differs.
- Recommendations carry no delivery horizons, no dates, and no owners. Action and rationale only.
- Write `sayScore`, `doScore`, and disputes to the ledger, then rerun the engine. Never hand compute or hand edit `final`, `ci`, `history`, or `flag`.
- Confidence is exactly Low, Medium, High. Never assume the subject count — enumerate from the pack taxonomy.
- Australian English throughout. No hyphens in prose — em dashes or rephrase. No emojis. DD/MM/YYYY displayed dates, ISO 8601 in the ledger.

## Invocation

Trigger this skill on any of the following:

- "Reconcile subject NN"
- "Synthesise the finding"
- "Say versus do for this subject"
- "Close out this subject"

On trigger, execute the eight phases in order. Do not compress or reorder them.
