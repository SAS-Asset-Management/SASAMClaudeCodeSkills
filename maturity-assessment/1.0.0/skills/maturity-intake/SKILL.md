---
name: maturity-intake
description: Evidence intake and hygiene for a maturity assessment engagement. Use when a new client artefact lands, when the assessor says "log this artefact", "we received a new document", "intake this file", "check the artefact schedule", or "is this a duplicate". Consumes inbound artefacts placed in evidence/ and produces an updated evidence/ARTEFACT_SCHEDULE.md row, a content hash record, a subject relevance mapping drawn from the pack's evidenceTypes.yaml, and an allocated review number ready for the maturity-parse skill. This skill never scores.
version: 1.0.0
---

# Maturity Intake Skill

This skill governs how every artefact received from the client enters the engagement. It runs the hygiene battery (hash dedupe, revision diffing, collision free numbering), records provenance, and maps the artefact to the subjects it may inform. Intake is deliberately separated from judgement: this skill registers and routes evidence, it never tags and never scores.

## Workflow

Execute the phases in order. Do not compress or reorder.

### 1. Bootstrap the engagement context

- Load `engagement.yaml` from the engagement repo root. If it does not exist, stop — this skill only runs inside an engagement repo.
- Resolve the framework pack named in `framework.pack`: look for a local overlay at the engagement's `packs/<packId>/` first, then fall back to `${CLAUDE_PLUGIN_ROOT}/packs/<packId>/`.
- Read the resolved pack's `pack.yaml` for the taxonomy (domains and subjects) and the scale. Never assume a subject count or a domain count — always enumerate from the taxonomy.
- Read the pack's `evidenceTypes.yaml` — the per subject list of evidence types that count.

### 2. Register the artefact in the schedule

Maintain `evidence/ARTEFACT_SCHEDULE.md` as the single register of requested versus received artefacts. For the inbound artefact, record:

- Artefact title (exact) and the path where it now sits under `evidence/`
- Provenance: who sent it, when (DD/MM/YYYY), and via which channel (email, portal, handover)
- Whether it answers an outstanding request row (mark that row received) or arrives unsolicited (add a new row)
- Status, current revision, and the content hash column (filled in the next phase)

If the schedule does not yet exist, create it with columns: Requested, Received, Artefact, Revision, Provenance, Hash, Review, Status, Notes.

### 3. Run the hygiene battery

Three mechanical checks, every inbound artefact, no exceptions.

1. **Content hash dedupe.** Compute the hash with `shasum -a 256 <path>` and compare it against the recorded Hash column across the whole schedule. An exact match means a duplicate: flag it to the assessor, note the duplication in the schedule, and do not allocate a review number. A duplicate never consumes a review.
2. **Revision diffing.** If the artefact is a new version of one already received (same title, new revision), diff it against the prior version and summarise what changed. The existing review at `reviews/NN_<artefactName>_review.md` is UPDATED with a revision note — it is never restarted from cold, and the artefact keeps its existing review number.
3. **Collision free review numbering.** For a genuinely new artefact, allocate the next review number centrally: list `reviews/`, find the highest existing `NN_` prefix, and allocate NN plus one, zero padded to two digits. This skill is the only allocator — no other skill or agent invents review numbers.

### 4. Map the artefact to subjects

Using the pack's `evidenceTypes.yaml`, walk every subject in the taxonomy and classify the artefact's relevance as one of: informs, partially informs, not relevant. Delegate the mapping to the `artefact-triage` agent where available; the assessor confirms the mapping before it lands in the schedule. Record the mapping in the schedule Notes so downstream skills know which subjects to expect evidence for.

This mapping is a routing signal only. It is not an evidence tag and it is not a score — the tag enums (None, Indirect, Direct) belong to the maturity-score skill.

### 5. Call intake severity where warranted

Where intake itself surfaces a finding worth recording (a requested artefact confirmed as not existing, missing document control, a superseded revision supplied as current), classify it using the pack's severity rubric with the values Critical, High, and Medium, and record it in the schedule Notes with the severity stated. Consistent severity language across dozens of reviews is the point — never invent synonym grades.

### 6. Hand off

Announce the handoff explicitly: the artefact is registered, hashed, numbered, and mapped, and is ready for the maturity-parse skill. For example:

> Artefact registered as review 07. Handing off to maturity-parse for the structured review at reviews/07_assetDataStandard_review.md.

If the artefact is a calculation CSV, route it to maturity-validate instead of maturity-parse and say so in the handoff.

## Guardrails

- **Intake never scores.** Tagging (None, Indirect, Direct) and scoring belong to the maturity-score skill; this skill produces only the relevance mapping (informs, partially informs, not relevant).
- Never allocate a review number without first running the hash dedupe. A duplicate never consumes a review.
- A new revision of an existing artefact updates the existing review — never restart the review and never allocate a second number.
- Review numbers are allocated centrally from the highest existing `reviews/NN_` prefix. Never guess or reuse a number.
- Never invent artefact names or provenance. Only register documents that physically exist under `evidence/`.
- Never assume the subject count — enumerate subjects from the resolved pack's taxonomy every time.
- Severity calls use exactly Critical, High, Medium — no synonyms, no half grades.
- Australian English throughout. No hyphens in prose — use em dashes or rephrase. No emojis. DD/MM/YYYY for displayed dates.

## Invocation

Trigger this skill on any of the following:

- "Log this artefact"
- "We received a new document"
- "Intake this file"
- "Check the artefact schedule"
- "Is this a duplicate"

On trigger, execute the six phases in order. Do not compress or reorder them.
