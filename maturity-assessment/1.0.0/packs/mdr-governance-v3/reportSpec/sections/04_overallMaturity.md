# Section 4 — Overall Maturity Result

## Purpose

Present the maturity position at three resolutions — whole of framework, per
domain, per subject — and let the plots carry the signal. This is the
centrepiece section: the plots alone must convey the correct understanding.

## Length budget

Three to four pages. Prose is sparse and sits around the plots.

## Required elements

1. **Headline number.** Mean of `subjects.<subjectId>.final.score` across the
   taxonomy, one decimal, with scale label, plus the confidence profile (count
   of Low, Medium, High from `final.confidence`). Flag draft status if the
   report gate is closed.
2. **Distribution commentary.** One paragraph on the shape of the score
   distribution, drawing the eye to the interesting part of the
   subjectConfidence plot.
3. **Domain level result.** A five row table: domain name, mean subject score
   (one decimal), best subject, worst subject, confidence profile, one sentence
   narrative. All values computed from `scoreLedger.json`.
4. **Say versus do reading.** One paragraph on whether maturity is pulled down
   more by documentation gaps or practice gaps, anchored to the two or three
   subjects with the largest `sayScore` to `doScore` variance.
5. **Narrative hotspots.** Subjects flagged `lowOutlier` (below 2) and
   `highOutlier` (above 4) by the engine: name each, give the score, quote the
   applicable rubric sentence, link to Section 5. If there are no high
   outliers, state that plainly.
6. **Run movement.** Where more than one aggregation run exists, one paragraph
   on movement between runs, grounded in the `history` entries and shown by the
   runTrend plot.
7. **Peer position.** Only when a benchmark input is present: one paragraph on
   cohort position per the peerPercentile plot. When absent, omit entirely —
   never fabricate a cohort.

## Forbidden

- No per subject detail beyond name, score, and one rubric sentence.
- No finding narrative and no interview quotes — those live in Section 5.

## Plots — this section carries the visual spine

| Plot | Placement | Notes |
| --- | --- | --- |
| domainRadar | Under the headline number | Full size; highlight the weakest domain vertex |
| subjectConfidence | Under the domain table | Score per subject with confidence encoding; caption mandatory |
| runTrend | Alongside the run movement paragraph | Only when two or more runs exist |
| peerPercentile | Alongside the peer paragraph | Only when benchmark data is present; omitted, never faked |

Catalogue ids only. Every numeric annotation binds to `scoreLedger.json`.
