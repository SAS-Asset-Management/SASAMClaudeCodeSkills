# The Delta Table — Row Construction

The delta table is the atomic evidentiary unit of the engagement. Every downstream score, finding, and conformance call traces back to delta rows, so each row must be independently verifiable by a reviewer who was not in the room.

## Columns

| Column | Rule |
| --- | --- |
| Requirement | What the standard requires, paraphrased tightly (about 200 characters), never a long verbatim republication of the standard. |
| Artefact Position | What the artefact says or does about that requirement, with a page or section reference into the artefact. |
| Alignment | Exactly one of: Meets, Partial, Gap, Exceeds, Not applicable. |
| Notes | The citation — chunk file plus clause — and any nuance (class specific override, pending verification, corroborating artefact). |

## Alignment semantics

- **Meets** — the artefact demonstrably satisfies the requirement as written.
- **Partial** — the requirement is addressed but with a material shortfall named in Notes.
- **Gap** — the requirement is not addressed, or is contradicted. A Gap call requires a specific clause citation and, where the standard has class specific overrides, the matching class chunk loaded.
- **Exceeds** — the artefact goes beyond the requirement in a way worth recording.
- **Not applicable** — the requirement does not bind this artefact or this client scope; justify the exemption in Notes.

## Worked example (fictional, Acme Rail)

| Requirement | Artefact Position | Alignment | Notes |
| --- | --- | --- | --- |
| Condition data submitted in the controlled schema each period | Data supply plan section 4 commits to the schema but names no validation step | Partial | standard/012_chunk.md clause 5.2 — validation gap named |
| Assessor competency records retained | Not addressed anywhere in the plan | Gap | standard/019_chunk.md clause 6.4 — no competency register referenced |

## Citation discipline

Every row's Notes cite one chunk file from the engagement's generated `packs/<packId>/standard/` directory plus a clause. A row that cannot cite a chunk is not a delta row — it is an impression, and impressions do not enter the review.
