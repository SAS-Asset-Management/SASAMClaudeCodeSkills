# maturity-assessment

An internal SAS Asset Management delivery accelerator for evidence based maturity assessments. It generalises a proven method — evidence intake, parse, score, interview, reconcile, validate, compliance matrix, report — across any assessment framework via framework packs and a per engagement `engagement.yaml`. The consultant drives Claude Code conversationally; the plugin supplies the skills, agents, hooks, scoring engine, and deliverable pipeline.

## Three Tier Architecture

```
+----------------------------------------------------------------+
|  TIER 1 - maturity-assessment plugin  (versioned, shared)      |
|  in SASAMClaudeCodeSkills, marketplace synced                  |
|                                                                |
|   skills/        the eight method skills                       |
|   agents/        fourteen specialist subagents                 |
|   hooks/         config driven gates and guardrails            |
|   engine/        score ledger, aggregation, CI, orchestration  |
|   deliverable/   dashboard builder, PDF renderer               |
|   packs/         the framework pack library                    |
+-------------------------------+--------------------------------+
                                | reads config, loads a pack
                                v
+----------------------------------------------------------------+
|  TIER 2 - framework pack  (data, one per assessment type)      |
|  rubrics . evidence types . question bank . optional calc      |
|  pack . report spec . coverage manifest                        |
+-------------------------------+--------------------------------+
                                | named in engagement.yaml
                                v
+----------------------------------------------------------------+
|  TIER 3 - engagement repo  (per client job, on SAS AM disk)    |
|  engagement.yaml . evidence/ . reviews/ . scoreLedger.json .   |
|  interviews/ . findings/ . deliverable/                        |
|  (the ONLY place client evidence ever lives)                   |
+----------------------------------------------------------------+
```

## Quick Start

1. **Create the engagement repo** on SAS AM controlled disk with this exact layout:

   ```
   engagement.yaml           configuration (see step 2)
   evidence/                 raw client artefacts
     ARTEFACT_SCHEDULE.md    requested versus received, with provenance
   reviews/                  NN_<artefactName>_review.md
   scoreLedger.json          the structured source of truth
   scoring/                  NN_<subjectName>_scoring.md (rendered narrative)
   interviews/               raw transcripts plus NN_<subjectName>_notes.md
   findings/                 run01/, run02/, ... each holding NN_<subjectName>_finding.md
   compliance/               optional matrix track (requirements.csv, conformance.csv, matrix.csv, auditorRulings.md)
   deliverable/              outputs (dashboard.html, summary.html, summary.pdf)
   tracking/                 PLAN.md, KANBAN.md
   .claude/                  thin, local overrides only
   ```

2. **Write `engagement.yaml`** from the worked example at `schemas/engagementExample.yaml`, validated by `schemas/engagementSchema.json`. Pin `engagement.pluginVersion` to the installed plugin version at init.

3. **Generate the standard chunks locally.** Framework packs never ship the chunked standard. From the licensed document, run:

   ```
   python3 engine/chunker.py --pdf <standard.pdf> --manifest <manifest.yaml> --out packs/<packId>/standard/
   ```

   inside the engagement repo. The engagement's local `packs/<packId>/` overlay is resolved before the plugin's copy, so the generated chunks are found first.

4. **Run the method through the eight skills**, in order as the engagement progresses: `/maturity-intake`, `/maturity-parse`, `/maturity-score`, `/maturity-interview`, `/maturity-reconcile`, `/maturity-validate` (when calculation evidence exists), `/maturity-compliance-matrix` (when the pack enables it), `/maturity-report`.

## Component Inventory

### Skills

| Skill                        | Purpose                                                            |
| ---------------------------- | ------------------------------------------------------------------ |
| `maturity-intake`            | Register an inbound artefact, allocate its review number, track the artefact schedule |
| `maturity-parse`             | Parse a registered artefact into a review with a delta table       |
| `maturity-score`             | Tag and score reviewed evidence against the pack rubrics into the ledger |
| `maturity-interview`         | Build the interview roster and question packs from evidence gaps   |
| `maturity-reconcile`         | Reconcile say versus do into findings                              |
| `maturity-validate`          | Route client calculation CSVs to the pack's calc engines           |
| `maturity-compliance-matrix` | Three phase requirements matrix (extract, assess, compile)         |
| `maturity-report`            | Render the dashboard, summary, and PDF from the score ledger       |

### Agents

| Agent                   | Model tier | Role                                                        |
| ----------------------- | ---------- | ----------------------------------------------------------- |
| `artefact-triage`       | sonnet     | Parse an inbound artefact, file a review, map to subjects — never scores |
| `rubric-tagger`         | sonnet     | Draft 0 to 5 scores against the rubric with cited evidence  |
| `calc-validator`        | sonnet     | Route a calculation CSV to the right engine, confirm arithmetic |
| `interview-prep`        | sonnet     | Draft a question pack targeting evidence gaps               |
| `transcript-extractor`  | sonnet     | Transcript to subject tagged notes with strength and gap markers |
| `finding-synthesiser`   | opus       | The only agent that writes findings; requires both say and do inputs |
| `section-writer`        | sonnet     | Draft one report section from its spec                      |
| `report-qa`             | haiku      | Detection only punch list on the draft deliverable          |
| `citation`              | haiku      | Resolve a claim to a standard chunk and clause              |
| `commitment-tracker`    | haiku      | Log forward commitments into the ledger                     |
| `email-finder`          | haiku      | Locate correspondence behind a finding                      |
| `requirement-extractor` | sonnet     | Compliance matrix phase 1                                   |
| `conformance-assessor`  | sonnet     | Compliance matrix phase 2                                   |
| `matrix-compiler`       | haiku      | Compliance matrix phase 3                                   |

### Hooks

All hook scripts live at `hooks/scripts/` and are referenced from `hooks/hooks.json`. Every script exits silently when the session is not inside an engagement repo.

| Hook                   | Guards                                                              |
| ---------------------- | ------------------------------------------------------------------- |
| `scoringGate.py`       | Blocks scoring writes without a recorded parse and review           |
| `sovereigntyGate.py`   | Blocks evidence paths from leaving the engagement repo              |
| `findingAuthorGate.py` | Only `finding-synthesiser` may write to `findings/`                 |
| `proseRules.py`        | Australian English, banned phrasings, prose hygiene                 |
| `plotBlocker.py`       | Denies plots outside the closed catalogue                           |
| `coverageWarner.py`    | Warns when the pack's coverage manifest declares known gaps         |
| `sessionPrimer.py`     | Primes an engagement session with status from the ledger            |
| `contractValidator.py` | Validates `engagement.yaml`, pack, and ledger against the schemas   |

## Versioning and Pinning

- The engagement pins the plugin version at init in `engagement.pluginVersion` and runs against it for the life of the engagement unless the consultant deliberately upgrades.
- Framework packs version independently of the plugin — a rubric correction does not force a plugin bump.
- The version appears in exactly three places that must match: this directory name, `.claude-plugin/plugin.json`, and the marketplace registry entry.

## Data Sovereignty

1. **The engagement repo is the only place client evidence lives.** It sits on SAS AM controlled disk. The plugin and the pack library never contain client evidence.
2. **Client evidence is never committed to any shared or cloud store.** The engagement repo's gitignore and the `sovereigntyGate` hook block `evidence/`, `interviews/`, and raw artefact paths from reaching a remote. Only derived, non sensitive outputs may be shared, and only deliberately.
3. **The Claude API operates under zero data retention and no training terms**, asserted as `data.api: zdr-no-training` in `engagement.yaml`. Reasoning happens transiently; nothing is persisted or trained on.
4. **No local model build.** Cloud reasoning under ZDR is the accepted operating mode; an on premise inference mode is out of scope for v1.

---

**SAS Asset Management**
We provide advanced analytics, expert asset management services and maturity assessments to help asset owners realise their value.
