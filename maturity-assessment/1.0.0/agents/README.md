# Maturity Assessment — Agent Suite

Fourteen generic subagents that wrap the maturity assessment workflow into discrete, parallelisable steps. Every agent begins by loading `engagement.yaml` at the engagement repo root and resolving the framework pack (engagement `packs/<packId>/` overlay first, then `${CLAUDE_PLUGIN_ROOT}/packs/<packId>/`) — no subject names, domain names, or client facts are hardcoded anywhere in this directory.

This index is generated from the directory listing, so it can never drift from what ships. **Count: fourteen agents.**

## Agent index

| Agent | Model tier | When to invoke |
| --- | --- | --- |
| `artefact-triage` | sonnet | A new client artefact lands in `evidence/` — parse, file the review, map to subjects. Never scores |
| `rubric-tagger` | sonnet | A review is filed and a subject is ready to codify — drafts 0 to 5 scores, appends ledger evidence and sayScore |
| `calc-validator` | sonnet | A client calculation CSV needs validation against the pack's calc engines |
| `interview-prep` | sonnet | An interview is being scheduled for a subject — drafts the question pack from the gap typology |
| `transcript-extractor` | sonnet | An interview transcript is filed — converts it to subject tagged notes with strengthening and gapping markers |
| `finding-synthesiser` | opus | Both say and do inputs exist for a subject — the only agent that writes `findings/` |
| `section-writer` | sonnet | One report section needs drafting per the pack reportSpec — fan out in parallel |
| `report-qa` | haiku | The draft report is assembled — detection only punch list, pattern plus semantic checks |
| `citation` | haiku | A claim needs traceability to the governing standard — clause, page, verbatim proof |
| `commitment-tracker` | haiku | Interview notes or a review mention a forward action — logs it to the commitments table |
| `email-finder` | haiku | A finding needs context from correspondence rather than formal artefacts |
| `requirement-extractor` | sonnet | Compliance matrix Phase 1 — catalogue requirements from the chunked standard |
| `conformance-assessor` | sonnet | Compliance matrix Phase 2 — assign conformance and severity per requirement |
| `matrix-compiler` | haiku | Compliance matrix Phase 3 — reconcile, aggregate, and roll up |

Model tiering is a default; an engagement may override per agent.

## Workflow choreography

```
Artefact track
  intake (skill)
      └── artefact-triage ────────▶ reviews/NN_<artefactName>_review.md
              └── rubric-tagger ──▶ scoring/NN_<subjectName>_scoring.md
                                    + evidence records and sayScore in scoreLedger.json
                      └── engine/aggregate.py ▶ scoreLedger.json (final, ci, history, flag)

Interview track
  interview ──▶ transcript-extractor ──▶ interviews/NN_<subjectName>_notes.md
            └── commitment-tracker  ──▶ tracking/commitments.md
                    └── finding-synthesiser (say + do required)
                            ──▶ findings/runNN/NN_<subjectName>_finding.md
                            ──▶ sayScore, doScore, disputes in scoreLedger.json
                                    └── engine/aggregate.py ▶ ledger updated

Report track
  report gate (deliverable/reportGate.py open)
      └── section-writer × N (parallel) ──▶ deliverable/draft/<sectionId>.md
              └── report-qa (punch list) ──▶ assessor dispositions
                      └── deliverable pipeline ──▶ dashboard.html, summary.html, summary.pdf

Cross cutting (any time)
  calc-validator ──▶ discrepancy summary + two narrative examples
  citation ──▶ formatted standard reference with proving quote
  email-finder ──▶ correspondence quotes with sender role and date
  requirement-extractor ─▶ conformance-assessor ─▶ matrix-compiler (compliance/ track)
```

The consultant sits at three judgement points: confirming triage mappings, ruling on say versus do disputes, and dispositioning the QA punch list. Everything else is dispatched and computed.

## Parallelisation

Independent work runs in parallel: several `artefact-triage` calls over a batch of new artefacts, `rubric-tagger` per subject, `section-writer` per section, `requirement-extractor` per standard slice. Sequential dependencies are enforced by the hooks (a score needs its review; a finding needs both inputs).

## Hard rules (enforced across all agents)

- **artefact-triage never scores.** Mapping only — the scoring gate hook backs this structurally.
- **Only finding-synthesiser writes `findings/`**, and it refuses when the say or the do input is missing. The findingAuthorGate hook backs this.
- **Ledger write discipline.** Agents append evidence records, sayScore, doScore, and disputes only. `final`, `ci`, `history`, and `flag` are written by `engine/aggregate.py` alone. Nothing recomputes scores from prose.
- **Fixed enums, character for character.** Evidence tags None / Indirect / Direct; confidence Low / Medium / High; conformance Complete / Partial / Not at all / TBC / Out of scope; severity Critical / High / Medium / Low / n/a; gap typology procedural / evidence / contradiction / recency / coverage.
- **No delivery horizons, no owners** in recommendations. Sequencing is the client's call.
- **Roles, never personal names**, in every extracted quote, attendee list, and commitment row.
- **Sovereignty.** Raw evidence and interview material never leave the engagement repo — the sovereignty gate hook blocks it at push time.
- **Australian English throughout. No hyphens in prose** — em dashes or rephrase. No emojis.
