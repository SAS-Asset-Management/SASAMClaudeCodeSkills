---
name: maturity-validate
description: Deterministic validation of client calculation data against the pack's calculation engines. Use when a calculation CSV lands, or when the assessor says "validate this CSV", "check these calculations", "recompute these scores against the standard", or "run the calc validator". Only active when the resolved pack declares calcPack true. Consumes a client CSV plus the pack's calcPack/ engines and methodIndex.yaml routing, and produces a recomputed comparison, quote ready discrepancy narratives, and Direct tagged evidence records for scoreLedger.json. The model routes; Python computes — no arithmetic by the model, ever.
version: 1.0.0
---

# Maturity Validate Skill

This skill validates client declared calculation outputs against the framework's canonical engines. Its discipline is absolute: the model reads headers and routes; a stdlib Python engine recomputes; discrepancies are surfaced as quote ready narratives with citations. The language model performs no arithmetic at any point.

## Workflow

Execute the phases in order. Do not compress or reorder.

### 1. Bootstrap the engagement context

- Load `engagement.yaml` from the engagement repo root. Stop if absent.
- Resolve the framework pack: engagement `packs/<packId>/` overlay first, then `${CLAUDE_PLUGIN_ROOT}/packs/<packId>/`.
- Read `pack.yaml`. **If `calcPack` is false, stop:** this framework has no arithmetic and this skill does not apply. Tell the assessor and, if a document was being routed here by mistake, send it back to maturity-parse.
- Read the pack's `coverageManifest.yaml` — if the engine an input needs is declared `not-implemented`, stop and tell the assessor the subject must be scored narratively; that gap is a stated caveat, never a silent workaround.

### 2. Route via the method index

Read the CSV headers and any declared class or method columns, then resolve the correct engine through `calcPack/methodIndex.yaml` — the declared subclass to method mapping. **Never try both methods to discover which applies.** If the index does not resolve the input, stop and ask the assessor; guessing a method fabricates a conformance result. Delegate the sniff and dispatch to the `calc-validator` agent where available.

### 3. Read the engine's skill spec

Before running anything, read the resolved engine's `calcPack/<engineName>/SKILL.md` — its inputs, ranges, equations, and citations into the MDR standard (or whichever governing document the pack declares). The spec states what the engine covers and what is out of scope; respect both.

### 4. Compute and validate — in Python

Dispatch to the engine's CLI with its two verbs:

- `compute` — recompute the outputs from the declared inputs
- `validate` — compare the client's declared output columns against the recomputed values and write a discrepancy report, one row per disagreement, with declared versus computed and the canonical reasoning

**The model routes, Python computes.** No mental arithmetic, no spreadsheet style reasoning in prose, no "roughly checks out" calls. If the engine cannot run, the validation did not happen.

### 5. Surface the discrepancies as narrative

Use the engine's report examples style emitter to produce up to a handful of representative discrepancies in quote ready narrative form — each naming the record id, the declared and computed values, the governing equation or table, and the citation into the standard. These narratives are what the maturity report quotes; select the largest deltas first, with diversity of error kind as the tie breaker.

### 6. Feed the ledger

Validation results are primary evidence. For each subject the validation informs, append an evidence record to `scoreLedger.json` per the shared contract, with `tag` set to `Direct`, the rubric level the result supports, the verbatim rubric sentence quoted, and a confidence of exactly Low, Medium, or High. Reference the discrepancy report path as the artefact. Then hand the subject to maturity-score's homogenisation step (`engine/aggregate.py`) rather than aggregating here.

### 7. Record and hand off

Note the validation in `evidence/ARTEFACT_SCHEDULE.md` against the source CSV (received, validated, discrepancy count) and state the handoff explicitly — which subjects gained Direct evidence and where the discrepancy report lives.

## Guardrails

- Only active when the resolved pack declares `calcPack: true`. Otherwise stop.
- **The model routes, Python computes. No arithmetic by the model, ever.** A validation without an engine run is not a validation.
- Route via `calcPack/methodIndex.yaml` — never try both methods to discover which applies, and never guess when the index does not resolve.
- Engines declared `not-implemented` in the coverage manifest are stated caveats: score those subjects narratively, never approximate the missing engine.
- Discrepancies are surfaced through the engine's narrative emitter with citations — never paraphrase a discrepancy from memory of the numbers.
- Validation evidence enters the ledger with `tag` exactly `Direct`; aggregation stays with `engine/aggregate.py`.
- Never modify the client's CSV. The discrepancy report is a separate output.
- Australian English throughout. No hyphens in prose — em dashes or rephrase. No emojis. DD/MM/YYYY displayed dates.
- **Agent fallback.** If a named delegate agent is not an available subagent type in this session, execute its instruction file from the plugin's `agents/` directory inline and record in the output that it ran inline.

## Invocation

Trigger this skill on any of the following:

- "Validate this CSV"
- "Check these calculations"
- "Recompute these scores against the standard"
- "Run the calc validator"

On trigger, execute the seven phases in order. Do not compress or reorder them.
