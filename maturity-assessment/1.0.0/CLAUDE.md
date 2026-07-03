# maturity-assessment Plugin

## Always Known Facts

- **What this is:** an internal SAS Asset Management delivery accelerator that runs an evidence based maturity assessment method (intake, parse, score, interview, reconcile, validate, compliance matrix, report) against any assessment framework.
- **Three tier architecture:**
  - **Tier 1 — the plugin** (this directory, versioned in the marketplace): holds the method — skills, agents, hooks, the scoring engine, and the deliverable pipeline. Framework independent.
  - **Tier 2 — the framework pack** (`packs/<packId>/`): holds one assessment framework as data — rubrics, evidence types, question bank, optional calc pack, report spec, coverage manifest. Named by `framework.pack` in the engagement config.
  - **Tier 3 — the engagement repo** (per client job, on SAS AM controlled disk): holds `engagement.yaml`, evidence, reviews, `scoreLedger.json`, interviews, findings, and the deliverable. **The engagement repo is the ONLY place client evidence ever lives.** The plugin and the packs never contain client material.
- **Data terms:** all Claude API reasoning runs under zero data retention and no training terms, asserted as `data.api: zdr-no-training` in `engagement.yaml`. Evidence never leaves the engagement repo (`data.sovereignty: local-only`).
- **Source of truth:** `scoreLedger.json` at the engagement root. Every score, confidence, CI, flag, and dispute lives there; markdown narrative, dashboard, and PDF all render from it.

---

## Progressive Disclosure — Skill Triggers

Before acting on any task that matches the table below, read the referenced skill file. Do not attempt the work from memory of this file alone.

| If the task involves…                                                          | Read this file                                    |
| ------------------------------------------------------------------------------ | ------------------------------------------------- |
| Receiving an inbound artefact from the client (any format) — register it first | `skills/maturity-intake/SKILL.md`                 |
| Parsing a registered artefact into a review with a delta table                 | `skills/maturity-parse/SKILL.md`                  |
| Scoring or tagging reviewed evidence against the pack rubrics                  | `skills/maturity-score/SKILL.md`                  |
| Preparing an interview roster or question pack for a subject                   | `skills/maturity-interview/SKILL.md`              |
| Reconciling "what they say" against "what they do" into a finding              | `skills/maturity-reconcile/SKILL.md`              |
| Validating a client calculation CSV against a pack calc engine                 | `skills/maturity-validate/SKILL.md`               |
| Working shall style requirements: extraction, conformance, matrix compilation  | `skills/maturity-compliance-matrix/SKILL.md`      |
| Any deliverable work — dashboard, summary, PDF, benchmark                      | `skills/maturity-report/SKILL.md`                 |

**Mandatory sequence on any inbound artefact:** `maturity-intake` (register, allocate the review number) then `maturity-parse` (record the parse and discussion) before any scoring. Scoring without a recorded parse and review is forbidden and blocked by hook.

---

## Agent Delegation — Triggers

When a task matches a trigger below, delegate via the `Task` tool with `subagent_type` rather than doing the work in context.

| Trigger                                                       | Delegate to             | Model tier |
| ------------------------------------------------------------- | ----------------------- | ---------- |
| New artefact lands in `evidence/`                             | `artefact-triage`       | sonnet     |
| Review filed; subject ready to score against the rubric       | `rubric-tagger`         | sonnet     |
| Client calculation CSV needs engine validation                | `calc-validator`        | sonnet     |
| Interview being prepared for a subject                        | `interview-prep`        | sonnet     |
| Raw transcript needs conversion to subject tagged notes       | `transcript-extractor`  | sonnet     |
| Say and do inputs both ready for a subject                    | `finding-synthesiser`   | opus       |
| One specific report section needs drafting                    | `section-writer`        | sonnet     |
| Draft deliverable ready for pre send review                   | `report-qa`             | haiku      |
| A claim needs standard traceability to a chunk and clause     | `citation`              | haiku      |
| Transcript or artefact mentions a forward action              | `commitment-tracker`    | haiku      |
| Finding needs context from correspondence                     | `email-finder`          | haiku      |
| Compliance matrix phase 1 — extract requirements              | `requirement-extractor` | sonnet     |
| Compliance matrix phase 2 — assess conformance                | `conformance-assessor`  | sonnet     |
| Compliance matrix phase 3 — compile the matrix                | `matrix-compiler`       | haiku      |

For independent work, run agents in parallel (for example, several `section-writer` calls at once).

---

## Hard Rules

1. **Never score without a recorded parse and review.** Every score traces to a review file in `reviews/`.
2. **Only `finding-synthesiser` writes to `findings/`**, and it refuses when either the say or the do input is missing.
3. **Intake agents never score.** `artefact-triage` registers, parses, and maps to subjects — nothing more.
4. **The engine computes all maths, never the model.** Only `engine/aggregate.py` writes `final`, `ci`, `history`, and `flag` in the ledger. Skills and agents append evidence records, `sayScore`, `doScore`, and disputes. Nothing downstream recomputes scores from prose.
5. **JS rendered plots only, from the closed catalogue** (`deliverable/plotCatalogue.md`): domainRadar, subjectConfidence, runTrend, peerPercentile. No other plots, no static images, no CDN at runtime.
6. **The auditor's read always wins.** Disputed scores carry a dispute record; the human ruling is final.
7. **Low scores are expected and acceptable.** The method reports what the evidence supports; it never inflates.
8. **Every citation resolves to a chunk file and clause** in the engagement's generated `standard/` directory, rendered per `brand.citationFormat`.
9. **Australian English, no hyphens in prose, no emojis** in every generated artefact. Hyphens are permitted only in identifiers where the convention requires them.

---

## Engagement Bootstrap

When a session starts inside an engagement repo (detected by the presence of `engagement.yaml` at the repo root):

1. **Read `engagement.yaml`** via the engine loader (`engine/configLoader.py` — `loadEngagement(repoRoot)`). It supplies the client block, framework selection, brand rules, data terms, and deliverable switches. The full contract is in `schemas/engagementSchema.json`.
2. **Resolve the pack** with `resolvePack(repoRoot, pluginRoot)`: the engagement's local `packs/<packId>/` overlay is checked FIRST, then the plugin's `packs/<packId>/`. Generated standard chunks always live in the engagement at `packs/<packId>/standard/` — the plugin never ships chunked standards.
3. **Honour the pinned version.** `engagement.pluginVersion` is written at init and pins the plugin version for the life of the engagement. Do not silently run a newer plugin against a pinned engagement; the consultant upgrades deliberately.
4. If `engagement.yaml` is absent, the session is not an engagement — hooks exit silently and no engagement behaviour applies.
