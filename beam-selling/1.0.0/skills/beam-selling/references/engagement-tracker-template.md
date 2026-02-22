# marcov.BEAM — Engagement Tracker

## Active Pipeline Dashboard

*Last updated: {{DATE}}*

### Pipeline Summary

| # | Company | Deal Name | Stage | Win % | Days in Stage | Next Action | Due |
|---|---------|-----------|-------|-------|---------------|-------------|-----|
| 1 | {{COMPANY_1}} | {{DEAL_1}} | {{STAGE_1}} | {{WIN_1}}% | {{DAYS_1}} | {{ACTION_1}} | {{DUE_1}} |
| 2 | {{COMPANY_2}} | {{DEAL_2}} | {{STAGE_2}} | {{WIN_2}}% | {{DAYS_2}} | {{ACTION_2}} | {{DUE_2}} |
| 3 | {{COMPANY_3}} | {{DEAL_3}} | {{STAGE_3}} | {{WIN_3}}% | {{DAYS_3}} | {{ACTION_3}} | {{DUE_3}} |

### Pipeline by Stage

```
Stage 1 — Qualify:     {{COUNT_1}} deals  |  {{VALUE_1}} weighted value
Stage 2 — Diagnose:    {{COUNT_2}} deals  |  {{VALUE_2}} weighted value
Stage 3 — Align:       {{COUNT_3}} deals  |  {{VALUE_3}} weighted value
Stage 4 — Propose:     {{COUNT_4}} deals  |  {{VALUE_4}} weighted value
Stage 5 — Commit:      {{COUNT_5}} deals  |  {{VALUE_5}} weighted value
Stage 6 — Deliver:     {{COUNT_6}} deals  |  {{VALUE_6}} weighted value
──────────────────────────────────────────────────────────────
Total:                 {{COUNT_TOTAL}} deals  |  {{VALUE_TOTAL}} weighted value
```

---

## Engagement Detail — {{COMPANY_NAME}}

### Overview

| Field | Detail |
|-------|--------|
| **Company** | {{COMPANY_NAME}} |
| **Deal Name** | {{DEAL_NAME}} |
| **Current Stage** | {{CURRENT_STAGE}} |
| **Win Probability** | {{WIN_PROBABILITY}}% |
| **Engagement Started** | {{START_DATE}} |
| **Days Active** | {{DAYS_ACTIVE}} |
| **Days in Current Stage** | {{DAYS_IN_STAGE}} |
| **Estimated Deal Value** | {{DEAL_VALUE}} |
| **Weighted Value** | {{WEIGHTED_VALUE}} |
| **Source** | {{OPPORTUNITY_SOURCE}} |

### Stage Progress

```
[1] Qualify    {{STAGE_1_BAR}}  {{STAGE_1_STATUS}}
[2] Diagnose   {{STAGE_2_BAR}}  {{STAGE_2_STATUS}}
[3] Align      {{STAGE_3_BAR}}  {{STAGE_3_STATUS}}
[4] Propose    {{STAGE_4_BAR}}  {{STAGE_4_STATUS}}
[5] Commit     {{STAGE_5_BAR}}  {{STAGE_5_STATUS}}
[6] Deliver    {{STAGE_6_BAR}}  {{STAGE_6_STATUS}}
```

### Gate Status — {{CURRENT_STAGE_NAME}}

| # | Gate Criterion | Status | Evidence Summary |
|---|---------------|--------|-----------------|
| 1 | {{GATE_1}} | {{MET/UNMET}} | {{EVIDENCE_1}} |
| 2 | {{GATE_2}} | {{MET/UNMET}} | {{EVIDENCE_2}} |
| 3 | {{GATE_3}} | {{MET/UNMET}} | {{EVIDENCE_3}} |

### Stakeholder Map

| Name | Title | Buying Role | Attitude | Last Contact |
|------|-------|-------------|----------|-------------|
| {{NAME_1}} | {{TITLE_1}} | {{ROLE_1}} | {{ATTITUDE_1}} | {{DATE_1}} |
| {{NAME_2}} | {{TITLE_2}} | {{ROLE_2}} | {{ATTITUDE_2}} | {{DATE_2}} |
| {{NAME_3}} | {{TITLE_3}} | {{ROLE_3}} | {{ATTITUDE_3}} | {{DATE_3}} |

### Win Probability Breakdown

| Factor | Base/Modifier | Reasoning |
|--------|--------------|-----------|
| **Base rate (Stage {{N}})** | {{BASE}}% | {{REASONING}} |
| {{MODIFIER_1}} | {{MODIFIER_VALUE_1}} | {{REASONING_1}} |
| {{MODIFIER_2}} | {{MODIFIER_VALUE_2}} | {{REASONING_2}} |
| {{MODIFIER_3}} | {{MODIFIER_VALUE_3}} | {{REASONING_3}} |
| **Adjusted probability** | **{{FINAL}}%** | |

### Activity Log (Recent)

| Date | Activity | Stage | Notes |
|------|----------|-------|-------|
| {{DATE_1}} | {{ACTIVITY_1}} | {{STAGE_1}} | {{NOTES_1}} |
| {{DATE_2}} | {{ACTIVITY_2}} | {{STAGE_2}} | {{NOTES_2}} |
| {{DATE_3}} | {{ACTIVITY_3}} | {{STAGE_3}} | {{NOTES_3}} |
| {{DATE_4}} | {{ACTIVITY_4}} | {{STAGE_4}} | {{NOTES_4}} |
| {{DATE_5}} | {{ACTIVITY_5}} | {{STAGE_5}} | {{NOTES_5}} |

### Next Steps

| # | Action | Owner | Due Date | Priority |
|---|--------|-------|----------|----------|
| 1 | {{ACTION_1}} | {{OWNER_1}} | {{DUE_1}} | {{PRIORITY_1}} |
| 2 | {{ACTION_2}} | {{OWNER_2}} | {{DUE_2}} | {{PRIORITY_2}} |
| 3 | {{ACTION_3}} | {{OWNER_3}} | {{DUE_3}} | {{PRIORITY_3}} |

---

## Closed Engagements

| Company | Deal Name | Outcome | Stage Reached | Close Date | Reason |
|---------|-----------|---------|---------------|------------|--------|
| {{COMPANY}} | {{DEAL}} | {{WON/LOST/DISQUALIFIED/STALLED}} | {{STAGE}} | {{DATE}} | {{REASON}} |

---

## Pipeline Health Metrics

| Metric | Value | Benchmark |
|--------|-------|-----------|
| **Average days to close (won)** | {{AVG_DAYS_WON}} | {{BENCHMARK}} |
| **Average days per stage** | {{AVG_DAYS_STAGE}} | {{BENCHMARK}} |
| **Stage 1 → 2 conversion** | {{CONV_1_2}}% | {{BENCHMARK}} |
| **Stage 2 → 3 conversion** | {{CONV_2_3}}% | {{BENCHMARK}} |
| **Stage 3 → 4 conversion** | {{CONV_3_4}}% | {{BENCHMARK}} |
| **Stage 4 → 5 conversion** | {{CONV_4_5}}% | {{BENCHMARK}} |
| **Stage 5 → 6 conversion** | {{CONV_5_6}}% | {{BENCHMARK}} |
| **Overall win rate** | {{WIN_RATE}}% | {{BENCHMARK}} |
| **Deals stalled > 30 days** | {{STALLED_COUNT}} | 0 |

---

*Tracker generated: {{DATE}}*
*Framework: marcov.BEAM v1.0.0*
