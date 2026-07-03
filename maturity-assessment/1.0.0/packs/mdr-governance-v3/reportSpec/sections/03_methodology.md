# Section 3 — Methodology

## Purpose

Explain how the maturity scores were derived. This section is the bulwark
against the "how did you get that number" challenge: every workflow component
named, every source referenced, every decision rule articulated.

## Length budget

Two to three pages, 1,000 to 1,400 words.

## Required elements

1. **Framework summary.** The pack taxonomy — domains and subjects from
   `pack.yaml` — scored on the pack scale, with the full rubrics reproduced in
   the appendix.
2. **Scale definition.** The scale ladder with all level labels, and a
   statement that each subject rubric specialises the generic ladder with one
   citable sentence per level.
3. **Say versus do methodology.** The dual track evidence design: the say layer
   (artefacts parsed into reviews, deltas captured against the chunked MDR
   standard) and the do layer (interviews with artefact anchored probes), with
   variance between the two treated as the maturity signal.
4. **Scoring workflow.** Tag (None, Indirect, Direct per `evidenceTypes.yaml`),
   score with a quoted rubric sentence and a confidence label, aggregate
   deterministically in the engine (Direct outweighs Indirect, High outweighs
   Low, stated confidence interval, from-0.7 rounding), and flag outliers below
   2 and above 4. State plainly that aggregation is computed by the engine over
   `scoreLedger.json`, not by narrative judgement.
5. **Confidence model.** What High, Medium, and Low mean for the reader's
   interpretation.
6. **Deterministic validation.** Where calculation engines were used, name the
   engines from the pack calcPack, the equations they encode, and the
   discrepancy counts they produced.
7. **Artefact and interview register summaries.** Counts and coverage, with
   links to the appendices.
8. **Limitations.** State them honestly: confidence bounds, interview sampling
   limits, the version of the MDR standard used as the comparison anchor, and
   cohort level attribution constraints.

## Forbidden

- No actual scores — they live in Sections 4 and 5.
- No finding content — this section describes how findings were produced.
- No editorialising — describe the process, do not defend it.

## Plots

None from the closed catalogue apply. This section is text and tables; the
framework taxonomy may be shown as a plain table drawn from `pack.yaml`.
