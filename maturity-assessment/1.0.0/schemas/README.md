# Schemas

The three JSON Schemas (draft 2020-12) in this directory are the binding contracts for the suite's configuration and data surfaces. Hooks (`contractValidator.py`) and the engine validate against them; anything that does not conform is rejected before it can corrupt an engagement.

| Schema                   | Validates                                     | Lives at                                  |
| ------------------------ | --------------------------------------------- | ------------------------------------------ |
| `engagementSchema.json`  | `engagement.yaml` — the single per engagement configuration surface: client block, framework selection and weights, brand rules, data sovereignty assertions, deliverable switches | engagement repo root |
| `packSchema.json`        | `pack.yaml` — a framework pack manifest: id, title, semver, maturity scale and level labels, domain and subject taxonomy, calc pack and compliance matrix switches, default aggregation weights | `packs/<id>/pack.yaml` |
| `scoreLedgerSchema.json` | `scoreLedger.json` — the structured score ledger, the single source of truth for scores, evidence records, run history, flags and disputes. Encodes the write discipline: only `engine/aggregate.py` writes `final`, `ci`, `history` and `flag` | engagement repo root |

`engagementExample.yaml` is a complete, fictional worked example (Acme Rail) that satisfies `engagementSchema.json`. Copy it into a new engagement repo as the starting point for `engagement.yaml`.

Note on YAML: all `.yaml` surfaces are parsed by `engine/configLoader.py`, which supports a deliberate subset — two space indentation, nested maps, block lists, inline lists, and scalar strings, numbers, booleans and dates. No anchors, no multiline scalars.
