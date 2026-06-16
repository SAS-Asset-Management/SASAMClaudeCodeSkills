# Example templates

Three **100% synthetic, SASdocX-branded** Office templates - one per format - that
showcase what the skills extract and respect. They contain **no proprietary or customer
content**: each is generated from scratch by the reproducible builder beside it, so the
binaries committed here are safe by construction.

| Template | Built by | What it stresses |
|---|---|---|
| [`templates/sasdocx_template.docx`](templates/sasdocx_template.docx) | [`builders/build_sasdocx_docx.py`](builders/build_sasdocx_docx.py) | multi-slot cover with executive scorecard, three indexes (TOC + table + figure), real `numbering.xml` (2-level bullets + numbered list), custom **SASdocX Table**, **SASdocX Callout** and **SASdocX Quote** styles, `SEQ` captions, a header logo, two sections (portrait + a populated landscape appendix carrying a wide rollout-matrix table and a second figure), a risk/readiness matrix, a footnote |
| [`templates/sasdocx_template.pptx`](templates/sasdocx_template.pptx) | [`builders/build_sasdocx_pptx.py`](builders/build_sasdocx_pptx.py) | eleven-slide deck with multi-placeholder cover, the deck's real masters & layouts, injected PowerPoint sections, agenda, KPI dashboard, two native chart families, two native tables including a risk heatmap, picture slide, process diagram approximation, demo slide |
| [`templates/sasdocx_template.xlsx`](templates/sasdocx_template.xlsx) | [`builders/build_sasdocx_xlsx.py`](builders/build_sasdocx_xlsx.py) | seven-sheet workbook with cover scorecard, named regions, cross-sheet formulas, number formats, named cell styles, two native tables, dashboard sheet, scenario sheet with data validation + comment, conditional formatting/data bars, frozen panes, three native charts |

Brand palette (cohesive with the project hero): SASdocX navy `#16213F`, blue `#2B7CD3`,
amber `#E0742B`, on light `#EAF1FF` / band `#DCE7FF`.

Each template ships realistic, internally-consistent **synthetic** sample content and visible
brand polish - a coloured cover band, a generated text-only SASdocX wordmark logo, and
brand-coloured native charts - so the rendered file already reads as a finished
on-brand document. The body is
demo content a generation run clears and replaces; the cover, indexes and named slots are the
reusable surface the skills extract.

## Try them

```bash
# Extract a Brand Profile from a template, then generate an on-brand document of the SAME format
python scripts/sasdockit/cli.py extract  --name demo --template examples/templates/sasdocx_template.docx --scope project
python scripts/sasdockit/cli.py verify   --name demo --scope auto --qa auto
python scripts/sasdockit/cli.py generate --name demo --input your_content.json --output out.docx --scope auto --qa auto
```

(Use the matching `.pptx` / `.xlsx` template to drive `saspptx` / `sasxlsx`. Each
skill stays in its own lane - a Word template makes Word documents, never a deck or a sheet.)

## Regenerate

```bash
python examples/builders/build_sasdocx_docx.py
python examples/builders/build_sasdocx_pptx.py
python examples/builders/build_sasdocx_xlsx.py
```

The builders are deterministic: all timestamps are pinned, so rebuilding yields
byte-identical templates and the regenerate step leaves a clean git tree. They are adapted from
the synthetic complex fixtures under `tests/fixtures/builders/`, re-themed with the
SASdocX brand.
