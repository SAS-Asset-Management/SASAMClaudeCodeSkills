---
name: sas-rcm
description: >
  Develop or review a Reliability-Centred Maintenance (RCM) analysis — a failure-mode-driven
  maintenance strategy for critical equipment, following the SAE JA1011/JA1012 RCM process.
  Use when the user asks for RCM, reliability-centred maintenance, an RCM analysis/decision
  worksheet, maintenance-task selection from failure modes, on-condition / scheduled-restoration
  / failure-finding task logic, or wants to turn an FMECA into a maintenance strategy. Feeds
  the Tactical Maintenance Plan (TMP). Leans on the fmeca skill for the failure analysis.
version: 1.0.0
---

# Reliability-Centred Maintenance (RCM)

RCM determines **what must be done to ensure an asset continues to do what its users require
in its present operating context** (SAE JA1011). It is the rigorous, failure-mode-driven
method that produces the maintenance tactics the **TMP** packages and schedules.

This skill reuses the **`fmeca`** skill for the failure analysis (functions → functional
failures → failure modes → effects → criticality) and the **amEngine** criticality/risk
engine to select and rank the systems worth analysing. See `_engine-guide/ENGINE.md`.

## Parents / children (line of sight)

- **Parent:** the **AMP** (`/sas-amp`) — its risk plane and criticality ranking select the
  critical systems for RCM.
- **Sibling input:** **`/fmeca`** — supplies the failure modes & effects (IEC 60812 / ISO 14224).
- **Child:** the **TMP** (`/sas-tmp`) — RCM-selected tasks package into the maintenance plan.

## The SAE JA1011 seven questions (analysis structure)

1. **Functions & performance standards** — what the asset does, to what standard, in its
   operating context.
2. **Functional failures** — the ways it can fail to deliver each function.
3. **Failure modes** — what causes each functional failure (from the FMECA).
4. **Failure effects** — what happens when each failure mode occurs (local / system / end).
5. **Failure consequences** — classify each: **hidden**, **safety/environmental**,
   **operational**, **non-operational**. This drives task worth.
6. **Proactive tasks & intervals** — apply the RCM decision logic:
   on-condition (predictive) → scheduled restoration → scheduled discard, by technical and
   worth feasibility.
7. **Default actions** where no proactive task is effective: **failure-finding** (hidden
   functions), **redesign** (safety/environmental with no effective task), or **run-to-fail**
   (economic, for non-safety consequences).

## Outputs

- **RCM decision worksheet** (per system): function → functional failure → failure mode →
  effect → consequence category → selected task / interval / responsibility.
- **Criticality-ranked system selection** (engine risk plane + criticality) — which systems
  to analyse first.
- **Task list handoff to the TMP** — the proactive tasks, intervals and default actions,
  ready for packaging and scheduling.
- Branded, paginated **standalone HTML + PDF** via `amEngine.render`.

## Standards alignment

SAE JA1011 (RCM process criteria), SAE JA1012 (RCM guide), IEC 60812 (FMEA/FMECA), ISO 14224
(reliability data & taxonomy), ISO 55001 §8 (operational planning & control). Clause map:
`standards-library/reliability-standards-map.md`.

## Workflow

1. **Select systems** — use the AMP's criticality ranking / risk plane (engine) to pick the
   critical systems (hidden-function and safety-consequence systems first).
2. **Run / import the FMECA** — invoke `/fmeca` (author or parse existing) for each system.
3. **Classify consequences & select tasks** — apply the JA1011 decision logic per failure
   mode; record on the decision worksheet.
4. **Package to TMP** — hand the selected tasks/intervals to `/sas-tmp`.
5. **Critique gate** — Andreas Nygaard checks JA1011/ISO 14224 alignment.
