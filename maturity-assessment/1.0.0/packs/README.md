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

## Library roadmap

`mdr-governance-v3` is the first pack, extracted and generalised from the
proven MDR governance engagement methodology. Further packs are authored per
this template: `iso-55001-am` (asset management system maturity),
`cyber-governance` (cyber maturity), and `data-governance` (data management
maturity). Authoring a pack is skilled work done once per framework: codify the
taxonomy, write citable sentence rubrics, list evidence types, write the
question bank, port any calculation engines, and declare coverage.
