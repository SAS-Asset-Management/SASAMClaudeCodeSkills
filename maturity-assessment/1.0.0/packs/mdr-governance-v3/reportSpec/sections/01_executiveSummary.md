# Section 1 — Executive Summary

## Purpose

Communicate the overall maturity position, the handful of narrative threads
that shape it, and the recommended next actions in a form the client executive
sponsor and the receiving authority's reviewer can both read in under four
minutes.

## Length budget

One page, single column, 600 to 800 words. No section breaks. One plot maximum.

## Required elements

1. **One sentence overall position.** Lead with the mean of the final subject
   scores, rounded to one decimal, with the scale label. Every number binds to
   `scoreLedger.json` — the mean is computed over `subjects.<subjectId>.final.score`
   across the pack taxonomy; never synthesise it in prose.
2. **The three biggest strengths.** The top three subjects by
   `final.score` where `final.confidence` is Medium or High. Do not pad with
   Low confidence strengths.
3. **The three biggest risks.** The three lowest scoring subjects, or the
   subjects with the most material open disputes (`disputes` with status open).
   Name each and state the consequence under the governing obligation if left
   unaddressed.
4. **Say versus do headline finding.** One sentence stating whether documented
   intent is tighter than observed practice or looser, and where the variance
   is most pronounced, grounded in `sayScore` versus `doScore` deltas.
5. **Open findings roll up.** Count of open, partial, and resolved findings in
   one sentence, linked to the appendix register.
6. **Recommended next actions.** Three to five bullets. Each names the subject
   or subjects it addresses and a responsible client function. Do not attach
   delivery horizons — the delivery programme is the client's to build; the
   report identifies what to do and who owns it, not when.
7. **Draft badging.** If the report gate is closed, the DRAFT badge is stamped
   automatically; additionally state the draft status plainly in the final
   paragraph.

## Forbidden

- No raw tables; the executive summary is prose.
- No technical MDR vocabulary without a plain language equivalent in the same
  sentence.
- No single subject narrative beyond one sentence — detail lives in Section 5.
- No recommendation that is not already supported by a subject section.

## Plots

| Plot | Placement | Notes |
| --- | --- | --- |
| domainRadar | Top right, small | Reused from Section 4 at reduced size; caption mandatory |

Catalogue ids only. Do not author bespoke plots for this section.
