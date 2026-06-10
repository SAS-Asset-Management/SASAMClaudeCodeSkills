---
name: sas-am-docs
description: >
  SAS-AM asset-management document hub. Use when the user wants to create any strategic or
  technical asset-management document — a Strategic Asset Management Plan (SAMP), Asset
  Management Plan (AMP / BAMP), Tactical Maintenance Plan (TMP), or Reliability-Centred
  Maintenance (RCM) analysis — or mentions "AM docs", "asset management document suite",
  the ISO 55001 line of sight, or asks which AM document they need. Routes to the right
  sub-skill (sas-samp, sas-amp, sas-tmp, sas-rcm, fmeca) and composes them top-down or
  bottom-up. All four documents are produced over the shared, code-grounded amEngine so the
  numbers are computed from real audit/financial data, not estimated.
version: 1.0.0
---

# SAS-AM Asset Management Document Hub

Unified entry point for SAS-AM's strategic and technical asset-management documents. Choose
a document below, or describe what you need and the hub will route you — then each tier can
**spawn its children** so a whole engagement flows from one intake.

## The ISO 55000 line of sight

```
Organisational Strategic Plan (OSP)            ← client input (not authored here)
        │
        ▼
   SAMP   Strategic Asset Management Plan       → /sas-samp
        │  org objectives → AM objectives; policy, decision criteria, funding strategy
        ▼
   AMP    Asset Management Plan (per class)     → /sas-amp
        │  activities, resources, timescales, lifecycle, renewal, risk, financials
        ▼
   TMP    Tactical Maintenance Plan             → /sas-tmp
        ▲  maintenance tactics / task list per equipment class
        │
   RCM  +  FMECA   failure analysis             → /sas-rcm  ·  /fmeca
           failure modes → tactics that populate the TMP
```

| Command | Document | When |
|---------|----------|------|
| `/sas-samp` | **Strategic Asset Management Plan** | Board/exec level; translates org strategy into AM objectives, policy, risk appetite, funding strategy. Parents the AMP(s). |
| `/sas-amp`  | **Asset Management Plan (AMP/BAMP)** | Per asset class/portfolio; condition, levels of service, demand, lifecycle, renewal, risk, 10-yr financials. |
| `/sas-tmp`  | **Tactical Maintenance Plan** | Per equipment class; maintenance tactics, task list, intervals, contract coverage. Consumes RCM/FMECA. |
| `/sas-rcm`  | **Reliability-Centred Maintenance** | Failure-mode driven maintenance strategy for critical equipment. Feeds the TMP. |
| `/fmeca`    | **FMEA / FMECA** | Failure mode, effects & criticality analysis (IEC 60812 / ISO 14224). Feeds RCM/TMP. |

## Quick start

**What would you like to produce?**

A) A **SAMP** (strategic, board-level) — and optionally spawn the AMPs beneath it
B) An **AMP / BAMP** for an asset class — condition, renewal, risk, financials
C) A **TMP** (maintenance tactics) — typically after an RCM/FMECA
D) An **RCM** analysis for critical equipment
E) **A full engagement** — start at the top (SAMP) and flow down the line of sight
F) Not sure — describe the decision you're trying to support and I'll recommend the tier

Wait for the selection, then invoke the matching sub-skill (`/sas-samp`, `/sas-amp`,
`/sas-tmp`, `/sas-rcm`, `/fmeca`). For **E**, run `/sas-samp` first and accept its offer to
spawn the AMP(s); each AMP then offers TMP/RCM/FMECA for the critical equipment it surfaces.

## How these differ from one-off drafters — the engine

Every document in this suite is produced over the shared **`amEngine`** (the SAS-AM
asset-management engine, generalised from the Kairos/LHG first-pass). The engine:

1. **Ingests** the client's real artefacts (condition workbooks, financials, signed
   maintenance contracts) and **catalogues** them in an artefact register with an
   evidence-gap → RFI loop.
2. **Cleans** them into a canonical dataset with **blocking quality gates** (no silent bad
   data), versioned condition-scale mapping, and a contract-rate cost basis.
3. **Computes** the analytics deterministically — condition profile, criticality, the
   condition × criticality risk plane, renewal demand with Monte-Carlo P10/P50/P90, KPI
   baseline, ISO-55001 maturity, improvement sequencing.
4. **Assembles** a professional, paginated, SAS-branded document (standalone HTML + PDF)
   from section narrative + the computed figures, plus an optional workshop pack.

The **document profile** (SAMP / AMP / TMP / RCM) selects the section set, thresholds and
ISO-clause mapping over that one engine. See `_engine-guide/ENGINE.md` for how a SKILL.md
drives it. Standards references are bundled in `standards-library/`.

## Line-of-sight composition (shared context, no re-interviewing)

Captured context — organisation, sector, asset hierarchy, criticality, condition scale,
policy thresholds — is written **once** to a shared engagement config and reused by every
downstream document. When a tier completes it offers to spawn its children:

- **SAMP done** → "Spawn AMP(s) for the priority asset classes you named?"
- **AMP done** → "Develop TMP / RCM / FMECA for the critical equipment identified?"
- **RCM/FMECA done** → tactics flow into the **TMP**.

Run top-down (SAMP-first) or bottom-up (start at RCM, roll up). Either way the evidence and
numbers are shared and consistent across the document set.

## Owner & governance

Owned by **larsFrederickson** (delivery). Standards-compliance review is performed by
**andreasNygaard** against the bundled `standards-library/` (and, when available, the
enterprise-brain ISO graph — see `_engine-guide/brain-hook.md`). Log every cross-tier
handoff/spawn via `record_handoff` so the radar replay sees the beams.
