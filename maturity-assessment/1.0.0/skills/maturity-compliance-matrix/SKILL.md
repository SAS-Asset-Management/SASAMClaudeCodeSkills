---
name: maturity-compliance-matrix
description: Build the requirement by requirement compliance matrix for frameworks with a shall style standard. Use when the assessor says "build the compliance matrix", "extract the requirements", "assess conformance", or "compile the matrix". Only active when the resolved pack declares complianceMatrix true. Consumes the engagement's generated standard chunks and the full evidence base (reviews, ledger, findings, interview notes), and produces compliance/requirements.csv, compliance/conformance.csv, and compliance/matrix.csv plus the subject to requirement rollup, governed by the binding auditor ruling file compliance/auditorRulings.md.
version: 1.0.0
---

# Maturity Compliance Matrix Skill

For frameworks codifiable against a shall style standard, this skill builds the heavier parallel track: one row per requirement, each with a conformance rating and a defensible justification, compiled into a master matrix and a subject level rollup. The rollup is the bridge between the requirement level evidence base and the subject level scorecard.

## Workflow

Execute the phases in order. Do not compress or reorder.

### 1. Bootstrap the engagement context

- Load `engagement.yaml` from the engagement repo root. Stop if absent.
- Resolve the framework pack: engagement `packs/<packId>/` overlay first, then `${CLAUDE_PLUGIN_ROOT}/packs/<packId>/`.
- Read `pack.yaml`. **If `complianceMatrix` is false, stop:** this framework carries no shall style corpus and the track does not apply.
- Confirm the standard chunks exist at the engagement's `packs/<packId>/standard/`. If missing, stop and instruct the assessor to run `engine/chunker.py` — the matrix is built from chunks, never from memory of the standard.
- Read the taxonomy — never assume a subject count.

### 2. Phase 1 — extract the requirements

Delegate slices of the standard chunks to the `requirement-extractor` agent. For every "shall", "must", "mandatory", "required", or equivalent binding statement, extract one requirement row with:

- `req_id` in the scheme `REQ-<sectionId>-<ordinal>` (for example `REQ-04.7-01`)
- The section reference, a tight paraphrase of the requirement (never a long verbatim republication of a licensed standard), its scope of application, and the taxonomy subjects it informs
- A short verbatim anchor phrase for reproducibility

Write the rows to `compliance/requirements.csv`. Record the total row count — Phase 3 reconciles against it.

### 3. Phase 2 — assess conformance per requirement

Delegate requirement subsets to the `conformance-assessor` agent. For each requirement, search the whole evidence base — `reviews/`, `scoreLedger.json` evidence records, `findings/`, `interviews/` notes — and assign a conformance rating of exactly one of:

| Rating | Meaning |
| --- | --- |
| Complete | Conformance evidenced; no material gap |
| Partial | Testable and partially met; the specific gap named in the justification |
| Not at all | No evidence of conformance, or direct evidence of non conformance |
| TBC | Not yet testable — state what would close it |
| Out of scope | Does not bind this client's scope; justify the exemption |

Do not confuse Partial with TBC: Partial means testable and partly met; TBC means it cannot yet be tested. Where the rating is Partial, Not at all, or TBC, assign a severity of exactly one of Critical, High, Medium, Low; where Complete or Out of scope, severity is n/a. Every rating carries a one to three sentence justification citing specific evidence with file references. Write to `compliance/conformance.csv`, one assessed row per Phase 1 row.

### 4. Apply the binding auditor rulings

Read `compliance/auditorRulings.md` before compiling anything. **Auditor rulings are binding and override inflated conformance reads** — where a ruling caps a subject's rollup, apply the cap regardless of what the assessed rows would otherwise aggregate to, and record the cap's application visibly in the rollup. Per stream or per area lifts may be recorded as observations, but the capped homogenised rating never lifts above the ruling.

### 5. Phase 3 — compile the master matrix and the subject rollup

Delegate compilation to the `matrix-compiler` agent. It:

1. Aggregates the assessments into `compliance/matrix.csv` — the master matrix
2. Computes the summary statistics: total requirements, conformance distribution, per section conformance percentages, severity distribution across the non Complete rows, and the top Critical and High non conformances by subject impact
3. Builds the **subject to requirement rollup** — for every taxonomy subject, the count of requirements informing it, the conformance and severity distributions across those requirements, and the representative non conformances. This rollup is the single most important Phase 3 output: it is the bridge between the requirement level evidence and the subject level scorecard, and the report's per subject narrative draws from it directly.

### 6. Reconcile the row counts

Phase 3 totals must reconcile against the Phase 1 and Phase 2 sums — every extracted requirement is assessed exactly once and appears in the matrix exactly once. Run:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/engine/orchestrate.py --repo <root> check
```

which verifies the reconciliation and exits nonzero on failure. A failed check blocks the matrix from feeding the report — fix the missing or duplicated rows and rerun.

## Guardrails

- Only active when the resolved pack declares `complianceMatrix: true`. Otherwise stop.
- Conformance values are exactly Complete, Partial, Not at all, TBC, Out of scope. Severity values are exactly Critical, High, Medium, Low, n/a. No synonyms, no half grades.
- **Never rate a requirement without specific cited evidence.** TBC is the correct answer when the evidence base does not yet support a call.
- **Auditor rulings are binding.** `compliance/auditorRulings.md` overrides any inflated conformance read; capped rollups stay capped, with the cap visible.
- Requirement ids follow `REQ-<sectionId>-<ordinal>` exactly.
- Paraphrase requirements; quote only short anchor phrases. The standard is licensed — refer to it, do not republish it.
- Phase 3 row counts must reconcile against Phase 1 and Phase 2 sums, verified by `engine/orchestrate.py check`.
- Build from the generated standard chunks, never from memory of the standard.
- Never assume the subject count — enumerate from the pack taxonomy.
- Australian English throughout. No hyphens in prose — em dashes or rephrase. No emojis. DD/MM/YYYY displayed dates.
- **Agent fallback.** If a named delegate agent is not an available subagent type in this session, execute its instruction file from the plugin's `agents/` directory inline and record in the output that it ran inline.

## Invocation

Trigger this skill on any of the following:

- "Build the compliance matrix"
- "Extract the requirements"
- "Assess conformance"
- "Compile the matrix"

On trigger, execute the six phases in order. Do not compress or reorder them.
