# Google Ads Performance Report

**Account:** {{ACCOUNT_NAME}}
**Period:** {{START_DATE}} to {{END_DATE}}
**Prepared:** {{REPORT_DATE}}
**Analyst:** Claude (MBP:google-ads)
**Data Source:** {{DATA_SOURCE — MCP (live) or CSV export}}

---

## Executive Summary

### Headline Metrics

| Metric | This Period | Previous Period | Change | Trend |
|---|---|---|---|---|
| Total Spend | {{SPEND}} | {{PREV_SPEND}} | {{CHANGE_%}} | {{TREND_ARROW}} |
| Impressions | {{IMPRESSIONS}} | {{PREV_IMPRESSIONS}} | {{CHANGE_%}} | {{TREND_ARROW}} |
| Clicks | {{CLICKS}} | {{PREV_CLICKS}} | {{CHANGE_%}} | {{TREND_ARROW}} |
| CTR | {{CTR}} | {{PREV_CTR}} | {{CHANGE_PP}} | {{TREND_ARROW}} |
| Conversions | {{CONVERSIONS}} | {{PREV_CONVERSIONS}} | {{CHANGE_%}} | {{TREND_ARROW}} |
| Cost per Conversion | {{CPA}} | {{PREV_CPA}} | {{CHANGE_%}} | {{TREND_ARROW}} |
| Conversion Value | {{CONV_VALUE}} | {{PREV_CONV_VALUE}} | {{CHANGE_%}} | {{TREND_ARROW}} |
| ROAS | {{ROAS}} | {{PREV_ROAS}} | {{CHANGE}} | {{TREND_ARROW}} |

### Key Findings

1. {{KEY_FINDING_1}}
2. {{KEY_FINDING_2}}
3. {{KEY_FINDING_3}}

### Overall Assessment

{{OVERALL_ASSESSMENT — 2-3 sentence summary of account health, direction, and primary opportunity or concern.}}

---

## Campaign Performance

### Active Campaigns

| Campaign | Type | Spend | Impressions | Clicks | CTR | CPC | Conversions | Conv. Rate | CPA | Conv. Value | ROAS |
|---|---|---|---|---|---|---|---|---|---|---|---|
| {{CAMPAIGN_1}} | {{TYPE}} | {{SPEND}} | {{IMP}} | {{CLICKS}} | {{CTR}} | {{CPC}} | {{CONV}} | {{CR}} | {{CPA}} | {{CV}} | {{ROAS}} |
| {{CAMPAIGN_2}} | {{TYPE}} | {{SPEND}} | {{IMP}} | {{CLICKS}} | {{CTR}} | {{CPC}} | {{CONV}} | {{CR}} | {{CPA}} | {{CV}} | {{ROAS}} |
| {{...}} | | | | | | | | | | | |
| **Total** | | **{{TOTAL_SPEND}}** | **{{TOTAL_IMP}}** | **{{TOTAL_CLICKS}}** | **{{AVG_CTR}}** | **{{AVG_CPC}}** | **{{TOTAL_CONV}}** | **{{AVG_CR}}** | **{{AVG_CPA}}** | **{{TOTAL_CV}}** | **{{OVERALL_ROAS}}** |

### Budget Pacing

| Campaign | Daily Budget | Avg Daily Spend | Pacing % | Status |
|---|---|---|---|---|
| {{CAMPAIGN}} | {{BUDGET}} | {{AVG_DAILY}} | {{PACING_%}} | {{STATUS — On Track / Underspending / Budget Limited}} |

---

## Top and Bottom Performers

### Top 5 Campaigns by ROAS

| Rank | Campaign | ROAS | Spend | Conversions | CPA |
|---|---|---|---|---|---|
| 1 | {{CAMPAIGN}} | {{ROAS}} | {{SPEND}} | {{CONV}} | {{CPA}} |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

### Bottom 5 Campaigns by ROAS

| Rank | Campaign | ROAS | Spend | Conversions | CPA |
|---|---|---|---|---|---|
| 1 | {{CAMPAIGN}} | {{ROAS}} | {{SPEND}} | {{CONV}} | {{CPA}} |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

### Top 10 Keywords by Conversions

| Keyword | Campaign | Match Type | Conversions | CPA | QS | Spend |
|---|---|---|---|---|---|---|
| {{KEYWORD}} | {{CAMPAIGN}} | {{MATCH}} | {{CONV}} | {{CPA}} | {{QS}} | {{SPEND}} |

### Bottom 10 Keywords by Efficiency (High Spend, Low/No Conversions)

| Keyword | Campaign | Match Type | Spend | Clicks | Conversions | QS |
|---|---|---|---|---|---|---|
| {{KEYWORD}} | {{CAMPAIGN}} | {{MATCH}} | {{SPEND}} | {{CLICKS}} | {{CONV}} | {{QS}} |

---

## Wasted Spend Analysis

### Summary

| Category | Spend | % of Total | Count |
|---|---|---|---|
| Keywords with zero conversions (30+ days) | {{AMOUNT}} | {{PCT}} | {{COUNT}} keywords |
| Low Quality Score keywords (QS 1-3) | {{AMOUNT}} | {{PCT}} | {{COUNT}} keywords |
| Irrelevant search terms | {{AMOUNT}} | {{PCT}} | {{COUNT}} terms |
| High CPA keywords (> 3x target) | {{AMOUNT}} | {{PCT}} | {{COUNT}} keywords |
| **Total Estimated Wasted Spend** | **{{TOTAL}}** | **{{PCT}}** | |

### Recommended Negative Keywords

Based on search term analysis, the following negative keywords are recommended:

| Negative Keyword | Match Type | Reason | Spend Saved (Est.) |
|---|---|---|---|
| {{TERM}} | {{MATCH}} | {{REASON}} | {{SAVINGS}} |

### Zero-Conversion Keywords (Top by Spend)

| Keyword | Campaign | Ad Group | Spend | Clicks | QS | Recommendation |
|---|---|---|---|---|---|---|
| {{KEYWORD}} | {{CAMPAIGN}} | {{AD_GROUP}} | {{SPEND}} | {{CLICKS}} | {{QS}} | {{ACTION — Pause / Adjust match type / Improve landing page}} |

---

## Keyword Insights

### Quality Score Distribution

| Quality Score | Keyword Count | % of Keywords | Avg CPC | Avg Position |
|---|---|---|---|---|
| 9-10 | {{COUNT}} | {{PCT}} | {{CPC}} | {{POS}} |
| 7-8 | {{COUNT}} | {{PCT}} | {{CPC}} | {{POS}} |
| 5-6 | {{COUNT}} | {{PCT}} | {{CPC}} | {{POS}} |
| 3-4 | {{COUNT}} | {{PCT}} | {{CPC}} | {{POS}} |
| 1-2 | {{COUNT}} | {{PCT}} | {{CPC}} | {{POS}} |

### Quality Score Component Breakdown (Keywords with QS < 5)

| Keyword | QS | Expected CTR | Ad Relevance | Landing Page Exp. | Suggested Action |
|---|---|---|---|---|---|
| {{KEYWORD}} | {{QS}} | {{RATING}} | {{RATING}} | {{RATING}} | {{ACTION}} |

### Match Type Analysis

| Match Type | Keywords | Spend | Conversions | CPA | Search Term Relevance |
|---|---|---|---|---|---|
| Exact | {{COUNT}} | {{SPEND}} | {{CONV}} | {{CPA}} | {{HIGH/MEDIUM/LOW}} |
| Phrase | {{COUNT}} | {{SPEND}} | {{CONV}} | {{CPA}} | {{HIGH/MEDIUM/LOW}} |
| Broad | {{COUNT}} | {{SPEND}} | {{CONV}} | {{CPA}} | {{HIGH/MEDIUM/LOW}} |

### New Keyword Opportunities

High-performing search terms not yet added as keywords:

| Search Term | Impressions | Clicks | Conversions | CPA | Recommended Match Type |
|---|---|---|---|---|---|
| {{TERM}} | {{IMP}} | {{CLICKS}} | {{CONV}} | {{CPA}} | {{MATCH}} |

---

## Impression Share Analysis

### Campaign-Level Impression Share

| Campaign | Search IS | Lost IS (Budget) | Lost IS (Rank) | Exact Match IS |
|---|---|---|---|---|
| {{CAMPAIGN}} | {{IS_%}} | {{LOST_BUDGET_%}} | {{LOST_RANK_%}} | {{EXACT_IS_%}} |

### Interpretation

**Budget-Constrained Campaigns** (Lost IS Budget > 10%):

{{List campaigns that are losing significant impression share due to budget limitations. For each, note the estimated additional impressions and conversions available if budget were increased.}}

**Rank-Constrained Campaigns** (Lost IS Rank > 20%):

{{List campaigns losing impression share due to ad rank. For each, diagnose whether the issue is bid-related (low bids) or quality-related (low Quality Score, poor ad relevance, poor landing page experience).}}

### Device Performance

| Device | Impressions | Clicks | CTR | Conversions | Conv. Rate | CPA | Share of Spend |
|---|---|---|---|---|---|---|---|
| Desktop | {{IMP}} | {{CLICKS}} | {{CTR}} | {{CONV}} | {{CR}} | {{CPA}} | {{PCT}} |
| Mobile | {{IMP}} | {{CLICKS}} | {{CTR}} | {{CONV}} | {{CR}} | {{CPA}} | {{PCT}} |
| Tablet | {{IMP}} | {{CLICKS}} | {{CTR}} | {{CONV}} | {{CR}} | {{CPA}} | {{PCT}} |

### Geographic Performance (Top 10 Locations)

| Location | Impressions | Clicks | Conversions | CPA | ROAS | Spend |
|---|---|---|---|---|---|---|
| {{LOCATION}} | {{IMP}} | {{CLICKS}} | {{CONV}} | {{CPA}} | {{ROAS}} | {{SPEND}} |

---

## Recommendations

### Critical Priority

> These issues require immediate attention and are likely costing significant budget or missing substantial opportunities.

**{{REC_NUMBER}}. {{RECOMMENDATION_TITLE}}**

- **Finding:** {{What the data shows}}
- **Impact:** {{Quantified business impact — e.g., estimated savings, additional conversions}}
- **Action:** {{Specific steps to implement}}
- **Priority:** Critical

---

### High Priority

> These changes will meaningfully improve performance and should be implemented within the next 1-2 weeks.

**{{REC_NUMBER}}. {{RECOMMENDATION_TITLE}}**

- **Finding:** {{What the data shows}}
- **Impact:** {{Quantified business impact}}
- **Action:** {{Specific steps to implement}}
- **Priority:** High

---

### Medium Priority

> These optimisations will incrementally improve performance and should be addressed within the next month.

**{{REC_NUMBER}}. {{RECOMMENDATION_TITLE}}**

- **Finding:** {{What the data shows}}
- **Impact:** {{Quantified business impact}}
- **Action:** {{Specific steps to implement}}
- **Priority:** Medium

---

### Low Priority

> These are minor improvements or longer-term strategic considerations.

**{{REC_NUMBER}}. {{RECOMMENDATION_TITLE}}**

- **Finding:** {{What the data shows}}
- **Impact:** {{Estimated impact}}
- **Action:** {{Specific steps to implement}}
- **Priority:** Low

---

## Recommendation Summary

| # | Recommendation | Category | Priority | Est. Impact |
|---|---|---|---|---|
| 1 | {{TITLE}} | {{Budget / Keywords / Ad Copy / Bid Strategy}} | {{PRIORITY}} | {{IMPACT}} |
| 2 | {{TITLE}} | {{CATEGORY}} | {{PRIORITY}} | {{IMPACT}} |
| 3 | {{TITLE}} | {{CATEGORY}} | {{PRIORITY}} | {{IMPACT}} |

---

## Next Review

| Item | Detail |
|---|---|
| **Next Review Date** | {{DATE — typically 2-4 weeks from report date}} |
| **Key Metrics to Monitor** | {{List 3-5 metrics to watch before next review}} |
| **Actions to Complete Before Review** | {{List the critical and high priority recommendations}} |
| **Expected Outcomes** | {{What improvement is expected if recommendations are implemented}} |

---

*Report generated by MBP:google-ads on {{REPORT_DATE}}. Data sourced from {{DATA_SOURCE}}. All monetary values in {{CURRENCY}}. Attribution model: {{ATTRIBUTION_MODEL}}.*
