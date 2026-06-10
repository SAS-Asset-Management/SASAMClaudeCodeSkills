# amEngine — how a SKILL.md drives the asset-management engine

All documents in this suite are produced over **`amEngine`** (package `sas-am-engine`,
repo `/home/cortext4/repos/sas-am-engine`; `pip install -e` it, or run modules with the
repo on `PYTHONPATH`). The engine is **code-grounded**: numbers are computed from the
client's real data, never estimated. A SKILL.md orchestrates the engine; it does not
re-implement analytics in prose.

## The five stages

```
1. INTAKE      amEngine.intake   artefact register (13-col, T1/T2/T3) + metadata scan
                                 + evidence-gap report → priority-tiered RFI
2. CLEAN       amEngine.clean    raw workbook → canonical cleanedAssets (blocking quality
               amEngine.io       gates) + condition-scale mapping + contract-rate parser
3. ANALYTICS   amEngine.analytics  condition profile · criticality · risk plane ·
                                   renewal sim (Monte-Carlo P10/P50/P90) · KPI · maturity
4. ASSEMBLE    amEngine.render   section narrative (md) + computed figures → branded,
                                 paginated standalone HTML
5. RENDER      render/renderPdf.js  HTML → A4 paginated PDF (Chrome print engine)
```

## Per-engagement config (the ~20% that is client-specific)

```
config/<engagement>/
  schema.yml            source→canonical column map, coercion, keep-order, base year,
                        sheet roles, required fields  (swap to drive a different audit tool)
  condition_scales.yml  source scale (e.g. 1-10) → narrative band (e.g. 1-5) → G/F/P/VP
  document.yml          DOCUMENT PROFILE: cover meta + section order + figure placements
```

The **document profile** (`document.yml`) is what makes a SAMP differ from an AMP/TMP/RCM:
it selects the section set, the figures, and the cover/standard. The engine and config/lhg
are the worked reference (the Lutheran Homes Group BAMP).

## Workflow a SKILL.md follows

1. **Intake & gap analysis** — accept whatever the client provides; catalogue it
   (`amEngine.intake.artefact_register`); run the evidence-gap report; surface the RFI.
2. **Interview only the gaps** — one question at a time, multiple-choice where possible
   (mirror sas-amp's interview methodology). Write answers into the engagement config.
3. **Run the pipeline** —
   ```bash
   python -m amEngine.orchestrate --workbook <wb.xlsm> --config config/<eng> --outputDir out/cleaned --clean
   python -m amEngine.render.assemble_amp --document config/<eng>/document.yml \
          --config config/<eng> --cleaned out/cleaned/cleanedAssets.csv \
          --sections-dir <narrative-dir> --out out/<eng>/DOC.html
   node amEngine/render/renderPdf.js out/<eng>/DOC.html out/<eng>/DOC.pdf "Footer"
   ```
4. **Write the narrative** around the computed figures (the engine supplies the numbers;
   you supply the sector-authentic prose). Per-section review by the context reviewer.
5. **Critique gate** — andreasNygaard checks ISO-clause alignment against
   `standards-library/` before any client exposure.
6. **Deliver** — standalone HTML + paginated PDF; optionally a workshop pack.

## Determinism notes

- `baseYear` in `schema.yml` pins the renewal window (null → current year). Pin an integer
  for fully reproducible re-derivation.
- The renewal Monte-Carlo is seeded (`MC_SEED`), so P10/P50/P90 reproduce exactly.
- Quality gates are **blocking**: bad data exits non-zero with the offending check named —
  fix at source, never suppress.

## Fidelity proof

`config/lhg` re-derives the LHG first-pass cleaned dataset **byte-identically** (26,534
assets; CPI AUD 58,802,075; criticality uplift AUD 109,114,731; 10-yr window 17,782) — see
`scripts/validate_foundation.py`. The generalisation is lossless.
