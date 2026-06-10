# Reliability standards map — RCM, TMP, FMECA

Standards governing the maintenance-tactics tier (below the AMP).

## RCM — SAE JA1011 / JA1012

**SAE JA1011** sets the criteria a process must satisfy to be called RCM — the **seven
questions** answered in order:
1. Functions & performance standards (operating context).
2. Functional failures.
3. Failure modes (causes).
4. Failure effects.
5. Failure consequences — **hidden / safety / environmental / operational / non-operational**.
6. Proactive tasks & intervals — **on-condition** (predictive), **scheduled restoration**,
   **scheduled discard** — selected by technical feasibility and worth.
7. Default actions — **failure-finding** (hidden functions), **redesign** (safety/env with no
   effective task), **run-to-fail** (economic, non-safety).

**SAE JA1012** is the guide to the standard (definitions, decision logic, task selection).

## FMEA / FMECA — IEC 60812, ISO 14224, SAE J1739, MIL-STD-1629A

- **IEC 60812** — FMEA/FMECA procedure; criticality analysis; RPN.
- **ISO 14224** — reliability & maintenance data collection and exchange; the **equipment
  taxonomy** (used to structure the equipment register and failure data). MTBF/MTTR.
- **SAE J1739** (design/process FMEA) and **MIL-STD-1629A** (criticality number) — alternate
  column sets. See the `fmeca` skill for the worked taxonomies and scoring scales.

## TMP — task types & statutory maintenance

- **ISO 55001 §8** — operational planning & control (the maintenance programme).
- **ISO 14224** — maintenance task taxonomy and data model (feeds the CMMS).
- **Statutory / compliance maintenance** (sector-specific):
  - **AS 1851** — routine service of fire protection systems.
  - **AS 3666** — air-handling & water systems (Legionella control).
  - **Essential Safety Measures (VIC)** / **Essential Safety Provisions (SA)** — annual
    building safety certification; AS/NZS 3760 (electrical test & tag), AS 1428 (access).

## Consequence → task logic (RCM decision summary)

| Consequence | First choice | If no effective proactive task |
|---|---|---|
| Hidden | failure-finding task | redesign |
| Safety / environmental | on-condition / restoration / discard | **redesign (mandatory)** |
| Operational | proactive if worth it economically | run-to-fail (accept) |
| Non-operational | proactive if worth it economically | run-to-fail (accept) |
