---
name: maturity-score
description: Tag and score reviewed artefacts against the pack rubrics — the four step algorithm of Tag, Score, Homogenise, Flag. Use when the assessor says "score this artefact", "tag artefacts against the subjects", "run the scoring", "score subject NN", or "rebuild the scorecard". Consumes recorded reviews from reviews/, the pack's rubrics and evidenceTypes.yaml, and produces evidence records appended to scoreLedger.json, an engine computed final score per subject, and a rendered narrative at scoring/NN_<subjectName>_scoring.md. The model never does the aggregation arithmetic — engine/aggregate.py does.
version: 1.0.0
---

# Maturity Score Skill

This skill converts recorded artefact reviews into auditable subject scores. The algorithm has four steps — Tag, Score, Homogenise, Flag — and a hard division of labour: the model tags and scores individual evidence records with verbatim rubric citations; a deterministic engine does every piece of aggregation arithmetic. Nothing downstream recomputes scores from prose.

## Workflow

Execute the phases in order. Do not compress or reorder.

### 1. Bootstrap the engagement context

- Load `engagement.yaml` from the engagement repo root. Stop if absent.
- Resolve the framework pack: engagement `packs/<packId>/` overlay first, then `${CLAUDE_PLUGIN_ROOT}/packs/<packId>/`.
- Read `pack.yaml` for the taxonomy, the scale (levels and labels), and `defaultWeights`. Never assume a subject count or a domain count — enumerate from the taxonomy.
- Read the pack's `evidenceTypes.yaml` and, for each subject in play, the rubric at `rubrics/NN_subjectName.md`.

### 2. Confirm the precondition

**Every artefact being scored must have a recorded review at `reviews/NN_<artefactName>_review.md`, produced through the maturity-parse skill with the assessor discussion on record.** If the assessor asks to score an artefact that has no review, stop and invoke maturity-parse first. Scoring without a recorded parse and discussion is forbidden and hook enforced.

### 3. Tag

For each artefact and subject pair, match the review content against the subject's entry in `evidenceTypes.yaml` and assign exactly one of:

- **None** — no evidence for this subject. A first class, cheap output: record it and move on.
- **Indirect** — the artefact references or implies evidence.
- **Direct** — the artefact is primary evidence for this subject.

Tagging is a cheap pre filter that shrinks the subject by artefact matrix to only the cells worth scoring. Output the tag matrix for the assessor to see.

### 4. Score

For each pair tagged Indirect or Direct:

1. Read the subject rubric and identify the level the evidence supports.
2. **Bracket before settling.** Explicitly test the level above and the level below: state why the evidence does not clear the level above, and why it exceeds the level below. This defeats anchoring on the first plausible level. Record the bracketing rationale.
3. Assign a rubric level 0 to 5 and an orthogonal confidence of exactly Low, Medium, or High.
4. **Always quote the matched rubric sentence verbatim** from the pack rubric file — never paraphrase it — and cite the evidence passage from the review.
5. Append the result to `scoreLedger.json` as an evidence record under the subject, per the shared contract shape:

```json
{ "artefact": "reviews/04_iamPolicy_review.md", "tag": "Direct",
  "rubricLevel": 3, "rubricQuote": "<verbatim rubric sentence>",
  "confidence": "Medium" }
```

Scoring techniques that are instructions, not suggestions:

- **Cluster scoring.** A set of near identical artefacts carrying a uniform signal is scored once as a cluster, with divergences called out narratively — not as parallel independent runs.
- **Anti flattery guardrail.** Low scores are expected and acceptable — this is a roadworthiness check, not a blame exercise. Neither the model nor a reviewer drifts toward flattering scores; the narrative focus is the improvement roadmap.
- **Self disclosure escalation.** A client documented admission of a gap is stronger, higher confidence evidence than an assessor's inference. Weight it accordingly in the confidence label.

### 5. Homogenise — run the engine

Aggregation is never done by the model. Run:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/engine/aggregate.py --repo <engagementRoot> [--run-trigger "text"]
```

The engine — and only the engine — weights the evidence records (Direct over Indirect, High over Low, per the pack or engagement weights), computes one final score per subject with a 95 percent confidence interval, applies the fixed rounding rule (`from-0.7`), computes the run over run delta with direction and driver, and writes `final`, `ci`, `history`, and `flag` into `scoreLedger.json`. **The model NEVER does the aggregation arithmetic.** If a final score looks wrong, fix the evidence records and rerun the engine — never hand edit a final.

### 6. Flag — read back the outliers

Read the ledger the engine just wrote. Subjects flagged `lowOutlier` (final score below 2) or `highOutlier` (final score above 4) are narrative hotspots: surface them to the assessor and mark them for the report narrative and for interview targeting. Subjects with thin evidence (few records, Low confidence) are flagged for interview follow up.

### 7. Render the scoring narrative

Only AFTER the engine has run, render `scoring/NN_<subjectName>_scoring.md` for each scored subject. The narrative presents the numbers from the ledger — final score, confidence, confidence interval, evidence list — together with the bracketing rationale ("why not the level above, why not the level below") as prose. The narrative is a rendered projection of the ledger; it is never the calculation surface, and no number appears in it that is not in the ledger.

## Guardrails

- Never score without a prior recorded parse and discussion (maturity-parse). Hook enforced.
- Tags are exactly None, Indirect, Direct. Confidence is exactly Low, Medium, High. No synonyms, no half grades.
- Always quote the matched rubric sentence verbatim when assigning a score — paraphrase breaks auditability.
- Bracket every score: test the level above and the level below explicitly before settling.
- **The model never does aggregation arithmetic.** Only `engine/aggregate.py` writes `final`, `ci`, `history`, and `flag`. Skills append evidence records only.
- Never hand edit a final score in the ledger. Fix the evidence, rerun the engine.
- The scoring narrative is rendered after the engine runs and contains no figure that is not in the ledger.
- Low scores are expected and acceptable — a roadworthiness check, not a blame exercise. Do not flatter.
- A client self disclosed gap outranks an inferred one in evidentiary strength.
- First pass artefact scores are indicative — the final finding waits for interview evidence and the maturity-reconcile skill.
- Never assume the subject count — enumerate from the pack taxonomy.
- Australian English throughout. No hyphens in prose — em dashes or rephrase. No emojis. DD/MM/YYYY displayed dates.

## Invocation

Trigger this skill on any of the following:

- "Score this artefact"
- "Tag artefacts against the subjects"
- "Run the scoring"
- "Score subject NN"
- "Rebuild the scorecard"

On trigger, execute the seven phases in order. Do not compress or reorder them.
