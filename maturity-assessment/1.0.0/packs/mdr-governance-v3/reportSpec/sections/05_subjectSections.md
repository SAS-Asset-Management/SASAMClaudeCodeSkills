# Section 5 — Subject Sections

## Purpose

One brief section per subject in the pack taxonomy. These sections are the
evidentiary depth of the report. Each is self contained — a reader landing on
any subject can read it without the others.

## Length budget

Half a page to one page per subject. Prose is dense; cite specifically; do not
pad.

## Ordering

Follow the taxonomy order in `pack.yaml`, grouped by domain. Each domain opens
with a single paragraph header describing the domain purpose and its overall
position. No new plots at the domain level — Section 4 carries that signal.

## Per subject template

1. **Heading.** `### N.M Subject NN — Subject Name`, numbered per domain.
2. **Score line.** `**Score: X / 5 ({scale label})** · Confidence: {level}` —
   both values read from `subjects.<subjectId>.final` in `scoreLedger.json`,
   with the confidence interval stated where it is wider than one point.
3. **Definition recap.** One sentence from the pack rubric Definition, cited
   verbatim where practical.
4. **Evidence summary.** Two to four bullets naming the artefact reviews and
   interview notes that contributed, each citing its engagement file path as
   recorded in the ledger `evidence` entries.
5. **Rubric level cited.** Direct quote of the rubric sentence at the assigned
   level from the pack rubric. If the weighted mean sits between levels, quote
   the level below and the level above and explain which elements of each
   applied.
6. **Say versus do reading.** One short paragraph on the documented position,
   the observed practice, and the variance, grounded in `sayScore` and
   `doScore`. If the do layer is pending, state that and mark the score draft.
7. **Open findings.** Any findings and open disputes affecting the subject,
   with status and scoring impact, in bullets.
8. **Recommendation.** One sentence, action oriented, with a suggested owner
   function. No delivery horizon, date, or timeframe.

## Forbidden

- No numbers that do not trace to `scoreLedger.json`.
- No paraphrased rubric citations — quote the sentence.
- No individually attributed frontline quotes — cohort attribution only.

## Plots

None per subject. The closed catalogue carries subject level signal in the
Section 4 subjectConfidence plot; do not author per subject micro plots.
