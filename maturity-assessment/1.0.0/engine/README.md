# Engine

The deterministic core of the maturity assessment plugin. The engine owns ALL arithmetic in the suite: the model routes, Python computes. Skills and agents never do score maths in prose; hooks and the deliverable builder consume the engine's public API by loading `configLoader.py` via `importlib.util.spec_from_file_location`. Everything here is Python standard library only; pytest is a dev only dependency.

## What lives here

| File | Role |
| --- | --- |
| `configLoader.py` | Minimal YAML subset loader. Public API: `loadYaml(path)`, `loadEngagement(repoRoot)`, `resolvePack(repoRoot, pluginRoot)` (local overlay `packs/<id>/` in the engagement wins over the plugin's). |
| `aggregate.py` | Aggregation and confidence engine. The only writer of `final`, `ci`, `history`, `flag`, and `runs` in `scoreLedger.json`. |
| `orchestrate.py` | Fan out orchestration with resume semantics plus the reconciliation gate. Never invokes agents itself. |
| `chunker.py` | Generalised standard chunker. Each engagement generates its local standard chunks with it; chunks are never shipped in a pack. Requires the `pdftotext` binary from poppler. |
| `tests/` | Adversarial pytest suite with a wholly fictional Acme Rail golden fixture. |

## CLIs

```bash
# Recompute finals, confidence intervals, flags, history, and the runs list
python3 engine/aggregate.py --repo /path/to/engagement --run-trigger "interview evidence landed"

# Status table, resume plan (JSON), or the reconciliation gate (exit 1 on failure)
python3 engine/orchestrate.py --repo /path/to/engagement status
python3 engine/orchestrate.py --repo /path/to/engagement plan
python3 engine/orchestrate.py --repo /path/to/engagement check

# Chunk the licensed standard into the engagement's local pack overlay
python3 engine/chunker.py --pdf standard.pdf --manifest chunkManifest.yaml --out packs/<packId>/standard
```

## Write discipline

The score ledger has exactly two writers and they never overlap:

* **Engine (`aggregate.py`) owns:** `final` (score, confidence, ci), `history`, `flag`, and the top level `runs` list.
* **Skills and agents own:** `evidence` records, `sayScore`, `doScore`, and `disputes`.

The engine never deletes or rewrites the agent owned fields, and nothing downstream ever recomputes scores from prose.

## The maths, fixed

Per subject weighted mean over evidence records where weight = tagWeight x confWeight. tagWeight: Direct = `directOverIndirect`, Indirect = 1.0, tag None is excluded entirely. confWeight: High = `highOverLow`, Medium = 1.0, Low = 1 / `highOverLow`. Weights come from `framework.aggregationWeights` in `engagement.yaml`, falling back to the pack's `defaultWeights`. The 95 percent confidence interval is mean plus or minus 1.96 x weighted standard error, clamped to [0, 5]; a single evidence record gives `ci = [mean, mean]`. Final confidence is the weighted mean of evidence confidence (Low 0, Medium 1, High 2): at least 1.5 is High, at least 0.5 is Medium, otherwise Low.

**Rounding rule `from-0.7`:** final score = floor(mean) unless the fractional part is STRICTLY GREATER than 0.7, in which case ceil. So a mean of **1.70 rounds to 1** and a mean of **1.71 rounds to 2**. The fractional part is rounded to nine decimal places before the comparison so binary float representation cannot flip the boundary. Subjects with a final below 2 are flagged `lowOutlier`; above 4, `highOutlier`.

## Determinism guarantee

Given identical inputs, `aggregate.py` rewrites `scoreLedger.json` byte for byte identically: fixed key order per the ledger contract, subject keys sorted, two space indent, trailing newline, and no timestamps beyond the run date. A rerun that changes nothing appends no history and no runs entry. The golden fixture test asserts this byte for byte.

## Running the tests

```bash
cd maturity-assessment/1.0.0
python3 -m pytest engine/tests -q
```

Tests load every module under test by file path (importlib), matching the plugin wide pytest configuration (`--import-mode=importlib`). The chunker's full CLI test skips cleanly when `pdftotext` is not installed (`brew install poppler` on macOS, `apt install poppler-utils` on Debian and Ubuntu).
