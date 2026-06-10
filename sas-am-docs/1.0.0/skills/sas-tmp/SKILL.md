---
name: sas-tmp
description: >
  Create or review a Tactical Maintenance Plan (TMP) — the document that turns maintenance
  tactics into an actionable, scheduled task list for an equipment class. Use when the user
  asks for a TMP, a tactical/maintenance plan, a maintenance task schedule, PM intervals,
  maintenance tactics by criticality, contract/service coverage for maintenance, or wants to
  operationalise an RCM/FMECA into a work programme. Consumes RCM + FMECA output. Produced
  over amEngine (contract-rate cost basis, criticality, service coverage computed from data).
version: 1.0.0
---

# Tactical Maintenance Plan (TMP)

The TMP is the **tactical child** of the AMP: it converts maintenance tactics into an
actionable, scheduled, costed task list per equipment class. It consumes the failure-mode
analysis from **RCM/FMECA** and the contract/criticality data from the **amEngine**.

Run the engine per `_engine-guide/ENGINE.md`. The TMP draws heavily on the engine's
**contract-rate parser** (real maintenance cost basis from signed agreements), the
**criticality** model, and **service-coverage** analysis.

## Parents / children (line of sight)

- **Parent:** the **AMP** (`/sas-amp`) — asset class, criticality, condition.
- **Inputs:** **`/sas-rcm`** and **`/fmeca`** — the failure-mode-derived tasks and intervals.
- **Output:** the work programme that a CMMS executes.

## Section structure

1. **Scope & equipment register** — the equipment class in scope, criticality-ranked (engine).
2. **Maintenance objectives & LoS linkage** — the service levels the maintenance sustains
   (from the AMP / SAMP).
3. **Maintenance tactics by criticality tier** — the strategy mix per tier:
   run-to-fail / preventive (time-based) / predictive (condition-based) / failure-finding —
   sourced from RCM consequence classification.
4. **Task list & intervals** — the consolidated PM task list with intervals, derived from
   RCM/FMECA; statutory/compliance tasks called out (ESM/ESP, AS 1851, AS 3666).
5. **Resourcing, contracts & service coverage** — contract matrix and service-coverage gaps
   (engine); in-house vs contracted; the cost basis from the contract-rate parser.
6. **Spares, logistics & shutdowns** — critical spares, lead times, shutdown/scheduled-outage
   windows.
7. **Work management & CMMS** — how tasks are raised, planned, executed, closed; the data
   model the CMMS needs.
8. **Performance & review** — KPIs (planned vs reactive ratio, completion rate, backlog),
   review cycle, and the trigger to re-run RCM.

## Engine reuse

| Engine output | TMP use |
|---|---|
| Contract-rate parser (`rateLines.csv`) | §5 cost basis; contract harmonisation |
| Criticality model | §1 ranking; §3 tactic selection |
| Service-coverage analysis | §5 coverage gaps by site/trade |
| Condition profile | §3 condition-based task triggers |

## Standards alignment

ISO 55001 §8 (operational planning & control), ISO 14224 (maintenance data & taxonomy),
SAE JA1012 (task types), AS 1851 / AS 3666 / ESM-ESP (statutory maintenance). Clause map:
`standards-library/reliability-standards-map.md`.

## Workflow

1. **Scope** — pick the equipment class and pull its criticality/condition/contracts (engine).
2. **Pull tactics** — import RCM/FMECA selected tasks (`/sas-rcm`, `/fmeca`).
3. **Build the task list** — consolidate by tactic and interval; add statutory tasks.
4. **Cost & resource** — apply the contract-rate basis; identify coverage gaps.
5. **Render** — branded, paginated standalone HTML + PDF via `amEngine.render`.
6. **Critique gate** — Andreas Nygaard checks ISO 14224 / statutory alignment.
