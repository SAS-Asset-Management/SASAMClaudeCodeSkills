# Framework packs

A framework pack is an entire assessment framework expressed as data. The
plugin is framework blind — the skills, agents, hooks, engine, and deliverable
pipeline know nothing about any particular standard. A pack makes the plugin an
MDR governance review, a cyber review, or an ISO 55001 review.

## Anatomy

Every pack follows the same fixed layout:

```
packs/<packId>/
  pack.yaml                 manifest: identity, scale, taxonomy, thresholds, capability flags
  rubrics/
    NN_subjectName.md       one file per subject, one citable sentence per level
  standard/
    INDEX.md                topic to chunk router (generated, not shipped for licensed standards)
    NNN_chunk.md            the governing document, chunked (generated locally)
  evidenceTypes.yaml        per subject list of artefact types that count as Direct evidence
  questionBank/
    core.md                 fixed cross session question set
    cohorts/<archetype>.md  role archetype specific probes
  calcPack/                 OPTIONAL — only when the framework has arithmetic
    <engineName>/SKILL.md
    <engineName>/calculate.py
    <engineName>/tests/
    methodIndex.yaml        declared shape to method routing (no try both)
  reportSpec/
    sections/NN_sectionName.md
    qaRules.yaml            banned phrasings, citation format, prose and plot rules
  coverageManifest.yaml     what the pack covers and, explicitly, what it does not
```

## Authoring rules

- **One citable sentence per maturity level.** Every level cell in a rubric is
  a single sentence the scorer can quote verbatim. No paragraphs, no bullets
  inside a level. This is what keeps scores auditable across runs.
- **Coverage is declared, never silent.** Anything the pack does not cover — a
  deferred calc engine, an unchunked standard, a partial question bank — is a
  `knownGaps` entry in `coverageManifest.yaml`, surfaced at engagement start.
- **No client content ever enters a pack.** Rubric text, scoring method, tie
  break tables, and equations are SAS methodology and ship. Client names,
  interviewee names, client document titles, client data values, and auditor
  ruling contents from any engagement do not. Fictional examples use
  Acme Rail (engagement code ACME-CYBER-2026) only.
- **Licensed standards are not redistributed.** Packs built on a licensed
  governing document ship a `standard/README.md` stub; chunks are generated
  locally per engagement with `engine/chunker.py` into the engagement repo's
  local pack overlay.
- **Stay inside the YAML subset.** Two space indentation, block and inline
  lists, scalars only — no anchors, no multiline scalars — so the engine's
  `configLoader.py` can parse every shipped file.

## Writing rubric level sentences

Level sentences are matched against every kind of evidence the engagement
produces, not only documents. Two rules keep them serviceable in the field:

- **Write for practice evidence as well as document evidence.** Interview
  quotes and observed behaviour must be able to match a level sentence, so
  phrase levels around what the organisation does ("defect scores are
  reviewed at a set cadence"), not only around what its documents contain
  ("a procedure document defines the review cadence"). A sentence that can
  only ever be satisfied by a document silently caps the do layer.
- **Substance over sentence.** Real evidence will sometimes sit between two
  level sentences or match a level's intent in different words. The scorer
  scores the substance, cites the nearest rubric sentence verbatim, and
  records the mismatch as an epistemic note on the evidence record — this is
  blessed practice, mirrored in the maturity-score skill's guardrails, not a
  rubric failure. If the same mismatch recurs across engagements, reword the
  level sentence in the next pack version.

## Library roadmap

`mdr-governance-v3` is the first pack, extracted and generalised from the
proven MDR governance engagement methodology. Further packs are authored per
this template: `iso-55001-am` (asset management system maturity),
`cyber-governance` (cyber maturity), and `data-governance` (data management
maturity). Authoring a pack is skilled work done once per framework: codify the
taxonomy, write citable sentence rubrics, list evidence types, write the
question bank, port any calculation engines, and declare coverage.
