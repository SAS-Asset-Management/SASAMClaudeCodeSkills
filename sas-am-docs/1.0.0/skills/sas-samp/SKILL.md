---
name: sas-samp
description: >
  Create or review a Strategic Asset Management Plan (SAMP) — the ISO 55001 document that
  translates organisational objectives into asset-management objectives and sets policy,
  decision criteria, risk appetite and funding strategy. Use when the user asks for a SAMP,
  a strategic asset management plan, an AM policy/objectives document, the "line of sight"
  from corporate strategy to asset plans, a capital-prioritisation or funding strategy, or
  the strategic parent above an AMP. Produced over amEngine (numbers computed from data).
version: 1.0.0
---

# Strategic Asset Management Plan (SAMP)

The SAMP is the **strategic parent** of the asset-management document family. It sits
between the Organisational Strategic Plan (OSP) and the Asset Management Plan(s) (AMPs), and
makes the "line of sight" explicit: organisational objectives → asset-management objectives
→ the approach for developing AMPs. ISO 55000 clause 3.3.2.

Run the engine as described in `_engine-guide/ENGINE.md`. The SAMP is mostly **strategic
narrative + roll-ups** of engine outputs (lightest new analytics of the suite); the heavy
lifting is org-strategy translation, risk appetite, and funding strategy.

## Parents / children (line of sight)

- **Parent:** Organisational Strategic Plan (client input — not authored here).
- **Children:** the **AMP(s)** (`/sas-amp`). On completion, offer to spawn an AMP for each
  priority asset class the SAMP names, reusing the shared engagement config.

## Section structure

1. **Organisational context & strategic objectives** — the OSP objectives this SAMP serves;
   stakeholders; the line of sight diagram.
2. **Asset management policy** — the organisation's commitments and principles (ISO 55001 §5.2).
3. **Asset management objectives** — org objectives translated into measurable AM objectives
   (§6.2.1), with the traceability matrix OSP → AM objective → AMP.
4. **Decision-making criteria** — how capital and renewal decisions are made: risk-based and
   criticality-weighted capital prioritisation model; whole-life-cost basis.
5. **Risk appetite & management framework** — risk appetite statement by consequence type
   (safety, compliance, service, financial); link to the AMP risk registers (§6.1).
6. **Levels of service strategy** — the board-set service strategy that the AMPs operationalise
   (high-level, not the data-derived LoS measures — those live in the AMP).
7. **Funding & financial strategy** — long-term financial plan (LTFP) linkage; funding
   sources; asset sustainability ratio target; the strategic 20-year renewal outlook
   (engine renewal roll-up).
8. **The AM system & SAMP→AMP framework** — scope of the AM system; how AMPs are developed,
   structured and reviewed under this SAMP.
9. **Governance, roles & capability** — accountabilities (RACI); ISO 55001 maturity baseline
   (engine maturity module) and the capability uplift the SAMP commits to.
10. **Performance & review** — strategic KPIs; the SAMP review cycle and triggers.

## Engine reuse vs new

| Engine output (reused) | SAMP use |
|---|---|
| Portfolio age profile, renewal wave (20-yr roll-up) | §7 strategic financial outlook |
| Risk register (portfolio-level) | §5 risk appetite calibration |
| ISO 55001 maturity baseline | §9 capability & improvement |
| KPI baseline | §3 / §10 objectives & performance |

**New for SAMP (not in the AMP):** LTFP / funding-adequacy framework, risk-appetite
statement, OSP→AM-objective translation, board-level LoS strategy. These are interview- and
strategy-led, not data-derived — gather them from the executive, don't infer from the audit.

## Standards alignment

ISO 55000 (§3.3.2 SAMP definition, line of sight), ISO 55001 §4 (context), §5 (leadership,
policy), §6.2.1 (objectives & planning), §9 (performance evaluation), §10 (improvement);
GFMAM Landscape; IAM subject groups. Clause map: `standards-library/iso55001-clause-map.md`.

## Interview & output

Follow the gap-driven interview in the engine guide: analyse provided materials first, then
ask only about gaps (one question at a time, multiple choice where possible). Strategic
inputs to gather: OSP objectives, growth strategy, risk appetite, LTFP/funding envelope,
governance. Output a branded, paginated **standalone HTML + PDF** via `amEngine.render`, and
optionally a board/executive workshop pack. Andreas Nygaard runs the ISO-clause critique
gate before client exposure.
