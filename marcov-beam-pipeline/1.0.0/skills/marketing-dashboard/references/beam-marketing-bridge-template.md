# BEAM Pipeline Marketing Attribution Report

> **Report Date**: {{REPORT_DATE}}
> **Reporting Period**: {{PERIOD_START}} to {{PERIOD_END}}
> **Active BEAM Engagements**: {{TOTAL_ACTIVE_ENGAGEMENTS}}
> **Marketing-Influenced Engagements**: {{MARKETING_INFLUENCED_COUNT}} of {{TOTAL_ACTIVE_ENGAGEMENTS}} ({{MARKETING_INFLUENCED_PERCENTAGE}}%)
> **Attribution Model**: {{ATTRIBUTION_MODEL}}
> **Prepared by**: MBP:marketing-dashboard

---

## 1. Marketing-Influenced Pipeline Summary

An overview of how marketing activity has contributed to the active BEAM sales pipeline during the reporting period.

| Metric | Value |
|--------|-------|
| Total Active Pipeline Value | ${{TOTAL_PIPELINE_VALUE}} |
| Marketing-Influenced Pipeline Value | ${{MARKETING_INFLUENCED_PIPELINE_VALUE}} |
| Marketing-Influenced Pipeline % | {{MARKETING_INFLUENCED_PIPELINE_PERCENTAGE}}% |
| Total Marketing Spend (Period) | ${{TOTAL_MARKETING_SPEND}} |
| Marketing ROI (Pipeline Value / Spend) | {{MARKETING_ROI}}x |
| Number of Deals with Marketing Touchpoints | {{DEALS_WITH_TOUCHPOINTS}} |
| Total Deals in Pipeline | {{TOTAL_DEALS}} |
| Average Marketing Touchpoints per Deal | {{AVG_TOUCHPOINTS_PER_DEAL}} |
| Average Marketing Spend per Influenced Deal | ${{AVG_SPEND_PER_DEAL}} |
| Average Influenced Deal Value | ${{AVG_INFLUENCED_DEAL_VALUE}} |

### Pipeline Value by BEAM Stage

| BEAM Stage | Total Deals | Pipeline Value | Marketing-Influenced Deals | Marketing-Influenced Value | % Marketing-Influenced |
|-----------|-------------|---------------|---------------------------|---------------------------|----------------------|
| Stage 1: Qualify | {{QUALIFY_TOTAL_DEALS}} | ${{QUALIFY_PIPELINE_VALUE}} | {{QUALIFY_INFLUENCED_DEALS}} | ${{QUALIFY_INFLUENCED_VALUE}} | {{QUALIFY_INFLUENCED_PCT}}% |
| Stage 2: Diagnose | {{DIAGNOSE_TOTAL_DEALS}} | ${{DIAGNOSE_PIPELINE_VALUE}} | {{DIAGNOSE_INFLUENCED_DEALS}} | ${{DIAGNOSE_INFLUENCED_VALUE}} | {{DIAGNOSE_INFLUENCED_PCT}}% |
| Stage 3: Align | {{ALIGN_TOTAL_DEALS}} | ${{ALIGN_PIPELINE_VALUE}} | {{ALIGN_INFLUENCED_DEALS}} | ${{ALIGN_INFLUENCED_VALUE}} | {{ALIGN_INFLUENCED_PCT}}% |
| Stage 4: Propose | {{PROPOSE_TOTAL_DEALS}} | ${{PROPOSE_PIPELINE_VALUE}} | {{PROPOSE_INFLUENCED_DEALS}} | ${{PROPOSE_INFLUENCED_VALUE}} | {{PROPOSE_INFLUENCED_PCT}}% |
| Stage 5: Commit | {{COMMIT_TOTAL_DEALS}} | ${{COMMIT_PIPELINE_VALUE}} | {{COMMIT_INFLUENCED_DEALS}} | ${{COMMIT_INFLUENCED_VALUE}} | {{COMMIT_INFLUENCED_PCT}}% |
| Stage 6: Deliver | {{DELIVER_TOTAL_DEALS}} | ${{DELIVER_PIPELINE_VALUE}} | {{DELIVER_INFLUENCED_DEALS}} | ${{DELIVER_INFLUENCED_VALUE}} | {{DELIVER_INFLUENCED_PCT}}% |
| **Total** | **{{TOTAL_DEALS}}** | **${{TOTAL_PIPELINE_VALUE}}** | **{{DEALS_WITH_TOUCHPOINTS}}** | **${{MARKETING_INFLUENCED_PIPELINE_VALUE}}** | **{{MARKETING_INFLUENCED_PIPELINE_PERCENTAGE}}%** |

---

## 2. BEAM Engagement Attribution Table

A complete view of each marketing-influenced deal, showing the first-touch channel, total touchpoints, and attributed marketing spend.

| Company | BEAM Stage | Deal Value (AUD) | First Touch Channel | First Touch Date | Total Touchpoints | Marketing Spend Attributed | ROI |
|---------|-----------|-----------------|---------------------|------------------|-------------------|---------------------------|-----|
| {{COMPANY_1}} | {{COMPANY_1_BEAM_STAGE}} | ${{COMPANY_1_DEAL_VALUE}} | {{COMPANY_1_FIRST_TOUCH_CHANNEL}} | {{COMPANY_1_FIRST_TOUCH_DATE}} | {{COMPANY_1_TOTAL_TOUCHPOINTS}} | ${{COMPANY_1_MARKETING_SPEND}} | {{COMPANY_1_ROI}}x |
| {{COMPANY_2}} | {{COMPANY_2_BEAM_STAGE}} | ${{COMPANY_2_DEAL_VALUE}} | {{COMPANY_2_FIRST_TOUCH_CHANNEL}} | {{COMPANY_2_FIRST_TOUCH_DATE}} | {{COMPANY_2_TOTAL_TOUCHPOINTS}} | ${{COMPANY_2_MARKETING_SPEND}} | {{COMPANY_2_ROI}}x |
| {{COMPANY_3}} | {{COMPANY_3_BEAM_STAGE}} | ${{COMPANY_3_DEAL_VALUE}} | {{COMPANY_3_FIRST_TOUCH_CHANNEL}} | {{COMPANY_3_FIRST_TOUCH_DATE}} | {{COMPANY_3_TOTAL_TOUCHPOINTS}} | ${{COMPANY_3_MARKETING_SPEND}} | {{COMPANY_3_ROI}}x |
| {{COMPANY_N}} | {{COMPANY_N_BEAM_STAGE}} | ${{COMPANY_N_DEAL_VALUE}} | {{COMPANY_N_FIRST_TOUCH_CHANNEL}} | {{COMPANY_N_FIRST_TOUCH_DATE}} | {{COMPANY_N_TOTAL_TOUCHPOINTS}} | ${{COMPANY_N_MARKETING_SPEND}} | {{COMPANY_N_ROI}}x |
| **Total** | — | **${{TOTAL_INFLUENCED_DEAL_VALUE}}** | — | — | **{{TOTAL_TOUCHPOINTS}}** | **${{TOTAL_MARKETING_SPEND_ATTRIBUTED}}** | **{{OVERALL_ROI}}x** |

*Repeat rows for each marketing-influenced BEAM engagement. ROI = Deal Value / Marketing Spend Attributed.*

---

## 3. Channel Attribution to Pipeline

How each marketing channel contributed to pipeline creation and progression.

### Channel Contribution Summary

| Channel | Deals Influenced | Pipeline Value (AUD) | % of Pipeline | Avg Touchpoints to Deal | Channel Spend | Pipeline ROI |
|---------|-----------------|---------------------|---------------|-------------------------|---------------|-------------|
| Google Ads | {{GOOGLE_DEALS_INFLUENCED}} | ${{GOOGLE_PIPELINE_VALUE}} | {{GOOGLE_PIPELINE_PCT}}% | {{GOOGLE_AVG_TOUCHPOINTS}} | ${{GOOGLE_CHANNEL_SPEND}} | {{GOOGLE_PIPELINE_ROI}}x |
| LinkedIn Ads | {{LINKEDIN_DEALS_INFLUENCED}} | ${{LINKEDIN_PIPELINE_VALUE}} | {{LINKEDIN_PIPELINE_PCT}}% | {{LINKEDIN_AVG_TOUCHPOINTS}} | ${{LINKEDIN_CHANNEL_SPEND}} | {{LINKEDIN_PIPELINE_ROI}}x |
| Organic Search | {{ORGANIC_DEALS_INFLUENCED}} | ${{ORGANIC_PIPELINE_VALUE}} | {{ORGANIC_PIPELINE_PCT}}% | {{ORGANIC_AVG_TOUCHPOINTS}} | — | — |
| Content | {{CONTENT_DEALS_INFLUENCED}} | ${{CONTENT_PIPELINE_VALUE}} | {{CONTENT_PIPELINE_PCT}}% | {{CONTENT_AVG_TOUCHPOINTS}} | ${{CONTENT_CHANNEL_SPEND}} | {{CONTENT_PIPELINE_ROI}}x |
| Email | {{EMAIL_DEALS_INFLUENCED}} | ${{EMAIL_PIPELINE_VALUE}} | {{EMAIL_PIPELINE_PCT}}% | {{EMAIL_AVG_TOUCHPOINTS}} | ${{EMAIL_CHANNEL_SPEND}} | {{EMAIL_PIPELINE_ROI}}x |
| Referral | {{REFERRAL_DEALS_INFLUENCED}} | ${{REFERRAL_PIPELINE_VALUE}} | {{REFERRAL_PIPELINE_PCT}}% | {{REFERRAL_AVG_TOUCHPOINTS}} | — | — |
| **Total** | **{{TOTAL_DEALS_INFLUENCED}}** | **${{TOTAL_PIPELINE_VALUE_INFLUENCED}}** | **100%** | **{{OVERALL_AVG_TOUCHPOINTS}}** | **${{TOTAL_CHANNEL_SPEND}}** | **{{OVERALL_PIPELINE_ROI}}x** |

### Channel Role Analysis

| Channel | First-Touch Deals | First-Touch Pipeline Value | Assist Deals | Assist Pipeline Value |
|---------|-------------------|---------------------------|-------------|----------------------|
| Google Ads | {{GOOGLE_FT_DEALS}} | ${{GOOGLE_FT_VALUE}} | {{GOOGLE_ASSIST_DEALS}} | ${{GOOGLE_ASSIST_VALUE}} |
| LinkedIn Ads | {{LINKEDIN_FT_DEALS}} | ${{LINKEDIN_FT_VALUE}} | {{LINKEDIN_ASSIST_DEALS}} | ${{LINKEDIN_ASSIST_VALUE}} |
| Organic Search | {{ORGANIC_FT_DEALS}} | ${{ORGANIC_FT_VALUE}} | {{ORGANIC_ASSIST_DEALS}} | ${{ORGANIC_ASSIST_VALUE}} |
| Content | {{CONTENT_FT_DEALS}} | ${{CONTENT_FT_VALUE}} | {{CONTENT_ASSIST_DEALS}} | ${{CONTENT_ASSIST_VALUE}} |
| Email | {{EMAIL_FT_DEALS}} | ${{EMAIL_FT_VALUE}} | {{EMAIL_ASSIST_DEALS}} | ${{EMAIL_ASSIST_VALUE}} |
| Referral | {{REFERRAL_FT_DEALS}} | ${{REFERRAL_FT_VALUE}} | {{REFERRAL_ASSIST_DEALS}} | ${{REFERRAL_ASSIST_VALUE}} |

---

## 4. Marketing Touchpoint Timeline

A chronological record of all marketing interactions for each active BEAM engagement. This timeline maps the prospect's marketing journey from first touch through to the current BEAM stage.

### {{DEAL_1_COMPANY}} — {{DEAL_1_BEAM_STAGE}}

**Deal Value**: ${{DEAL_1_DEAL_VALUE}}
**Engagement Owner**: {{DEAL_1_OWNER}}
**Days in Pipeline**: {{DEAL_1_DAYS_IN_PIPELINE}}
**Total Marketing Touchpoints**: {{DEAL_1_TOTAL_TOUCHPOINTS}}

| # | Date | Channel | Type | Campaign / Detail |
|---|------|---------|------|-------------------|
| 1 | {{DEAL_1_TP1_DATE}} | {{DEAL_1_TP1_CHANNEL}} | {{DEAL_1_TP1_TYPE}} | {{DEAL_1_TP1_CAMPAIGN}} |
| 2 | {{DEAL_1_TP2_DATE}} | {{DEAL_1_TP2_CHANNEL}} | {{DEAL_1_TP2_TYPE}} | {{DEAL_1_TP2_CAMPAIGN}} |
| 3 | {{DEAL_1_TP3_DATE}} | {{DEAL_1_TP3_CHANNEL}} | {{DEAL_1_TP3_TYPE}} | {{DEAL_1_TP3_CAMPAIGN}} |
| — | {{DEAL_1_BEAM_START_DATE}} | — | **BEAM Engagement Started** | Stage 1: Qualify |
| 4 | {{DEAL_1_TP4_DATE}} | {{DEAL_1_TP4_CHANNEL}} | {{DEAL_1_TP4_TYPE}} | {{DEAL_1_TP4_CAMPAIGN}} |
| 5 | {{DEAL_1_TP5_DATE}} | {{DEAL_1_TP5_CHANNEL}} | {{DEAL_1_TP5_TYPE}} | {{DEAL_1_TP5_CAMPAIGN}} |

**Touchpoint Types**: ad click, website visit, content download, email open, social engagement

**Attribution Summary**:
- First touch: {{DEAL_1_FIRST_TOUCH_CHANNEL}} — {{DEAL_1_FIRST_TOUCH_CAMPAIGN}} on {{DEAL_1_FIRST_TOUCH_DATE}}
- Last touch before engagement: {{DEAL_1_LAST_PRE_TOUCH_CHANNEL}} — {{DEAL_1_LAST_PRE_TOUCH_CAMPAIGN}} on {{DEAL_1_LAST_PRE_TOUCH_DATE}}
- Pre-engagement touchpoints: {{DEAL_1_PRE_TOUCHPOINTS}}
- During-engagement touchpoints: {{DEAL_1_DURING_TOUCHPOINTS}}
- Marketing spend attributed: ${{DEAL_1_SPEND_ATTRIBUTED}}

---

### {{DEAL_2_COMPANY}} — {{DEAL_2_BEAM_STAGE}}

**Deal Value**: ${{DEAL_2_DEAL_VALUE}}
**Engagement Owner**: {{DEAL_2_OWNER}}
**Days in Pipeline**: {{DEAL_2_DAYS_IN_PIPELINE}}
**Total Marketing Touchpoints**: {{DEAL_2_TOTAL_TOUCHPOINTS}}

| # | Date | Channel | Type | Campaign / Detail |
|---|------|---------|------|-------------------|
| 1 | {{DEAL_2_TP1_DATE}} | {{DEAL_2_TP1_CHANNEL}} | {{DEAL_2_TP1_TYPE}} | {{DEAL_2_TP1_CAMPAIGN}} |
| 2 | {{DEAL_2_TP2_DATE}} | {{DEAL_2_TP2_CHANNEL}} | {{DEAL_2_TP2_TYPE}} | {{DEAL_2_TP2_CAMPAIGN}} |
| — | {{DEAL_2_BEAM_START_DATE}} | — | **BEAM Engagement Started** | Stage 1: Qualify |
| 3 | {{DEAL_2_TP3_DATE}} | {{DEAL_2_TP3_CHANNEL}} | {{DEAL_2_TP3_TYPE}} | {{DEAL_2_TP3_CAMPAIGN}} |

**Attribution Summary**:
- First touch: {{DEAL_2_FIRST_TOUCH_CHANNEL}} — {{DEAL_2_FIRST_TOUCH_CAMPAIGN}} on {{DEAL_2_FIRST_TOUCH_DATE}}
- Last touch before engagement: {{DEAL_2_LAST_PRE_TOUCH_CHANNEL}} — {{DEAL_2_LAST_PRE_TOUCH_CAMPAIGN}} on {{DEAL_2_LAST_PRE_TOUCH_DATE}}
- Pre-engagement touchpoints: {{DEAL_2_PRE_TOUCHPOINTS}}
- During-engagement touchpoints: {{DEAL_2_DURING_TOUCHPOINTS}}
- Marketing spend attributed: ${{DEAL_2_SPEND_ATTRIBUTED}}

---

*Repeat the Marketing Touchpoint Timeline section for each marketing-influenced BEAM engagement.*

---

## 5. First-Touch vs Last-Touch Analysis

Understanding which channels introduce prospects to the pipeline versus which channels support deal progression. This reveals whether a channel's primary role is awareness (generating new pipeline) or conversion (advancing existing deals).

### First-Touch Attribution (Channels That Introduce Deals)

| Channel | Deals Originated | Pipeline Value Originated | % of Originated Pipeline | Avg Deal Value |
|---------|-----------------|--------------------------|--------------------------|----------------|
| Google Ads | {{GOOGLE_FT_ORIGINATED}} | ${{GOOGLE_FT_ORIGINATED_VALUE}} | {{GOOGLE_FT_ORIGINATED_PCT}}% | ${{GOOGLE_FT_AVG_DEAL}} |
| LinkedIn Ads | {{LINKEDIN_FT_ORIGINATED}} | ${{LINKEDIN_FT_ORIGINATED_VALUE}} | {{LINKEDIN_FT_ORIGINATED_PCT}}% | ${{LINKEDIN_FT_AVG_DEAL}} |
| Organic Search | {{ORGANIC_FT_ORIGINATED}} | ${{ORGANIC_FT_ORIGINATED_VALUE}} | {{ORGANIC_FT_ORIGINATED_PCT}}% | ${{ORGANIC_FT_AVG_DEAL}} |
| Content | {{CONTENT_FT_ORIGINATED}} | ${{CONTENT_FT_ORIGINATED_VALUE}} | {{CONTENT_FT_ORIGINATED_PCT}}% | ${{CONTENT_FT_AVG_DEAL}} |
| Referral | {{REFERRAL_FT_ORIGINATED}} | ${{REFERRAL_FT_ORIGINATED_VALUE}} | {{REFERRAL_FT_ORIGINATED_PCT}}% | ${{REFERRAL_FT_AVG_DEAL}} |
| Email | {{EMAIL_FT_ORIGINATED}} | ${{EMAIL_FT_ORIGINATED_VALUE}} | {{EMAIL_FT_ORIGINATED_PCT}}% | ${{EMAIL_FT_AVG_DEAL}} |
| **Total** | **{{TOTAL_FT_ORIGINATED}}** | **${{TOTAL_FT_ORIGINATED_VALUE}}** | **100%** | **${{TOTAL_FT_AVG_DEAL}}** |

### Last-Touch Attribution (Channels That Advance Deals)

*The last marketing touchpoint before the most recent BEAM stage progression.*

| Channel | Deals Advanced | Pipeline Value Advanced | % of Advanced Pipeline | Avg Deal Value |
|---------|---------------|------------------------|------------------------|----------------|
| Google Ads | {{GOOGLE_LT_ADVANCED}} | ${{GOOGLE_LT_ADVANCED_VALUE}} | {{GOOGLE_LT_ADVANCED_PCT}}% | ${{GOOGLE_LT_AVG_DEAL}} |
| LinkedIn Ads | {{LINKEDIN_LT_ADVANCED}} | ${{LINKEDIN_LT_ADVANCED_VALUE}} | {{LINKEDIN_LT_ADVANCED_PCT}}% | ${{LINKEDIN_LT_AVG_DEAL}} |
| Organic Search | {{ORGANIC_LT_ADVANCED}} | ${{ORGANIC_LT_ADVANCED_VALUE}} | {{ORGANIC_LT_ADVANCED_PCT}}% | ${{ORGANIC_LT_AVG_DEAL}} |
| Content | {{CONTENT_LT_ADVANCED}} | ${{CONTENT_LT_ADVANCED_VALUE}} | {{CONTENT_LT_ADVANCED_PCT}}% | ${{CONTENT_LT_AVG_DEAL}} |
| Email | {{EMAIL_LT_ADVANCED}} | ${{EMAIL_LT_ADVANCED_VALUE}} | {{EMAIL_LT_ADVANCED_PCT}}% | ${{EMAIL_LT_AVG_DEAL}} |
| **Total** | **{{TOTAL_LT_ADVANCED}}** | **${{TOTAL_LT_ADVANCED_VALUE}}** | **100%** | **${{TOTAL_LT_AVG_DEAL}}** |

### Channel Role Summary

| Channel | Primary Role | First-Touch % | Last-Touch % | Insight |
|---------|-------------|---------------|-------------|---------|
| Google Ads | {{GOOGLE_ROLE}} | {{GOOGLE_FT_PCT}}% | {{GOOGLE_LT_PCT}}% | {{GOOGLE_ROLE_INSIGHT}} |
| LinkedIn Ads | {{LINKEDIN_ROLE}} | {{LINKEDIN_FT_PCT}}% | {{LINKEDIN_LT_PCT}}% | {{LINKEDIN_ROLE_INSIGHT}} |
| Organic Search | {{ORGANIC_ROLE}} | {{ORGANIC_FT_PCT}}% | {{ORGANIC_LT_PCT}}% | {{ORGANIC_ROLE_INSIGHT}} |
| Content | {{CONTENT_ROLE}} | {{CONTENT_FT_PCT}}% | {{CONTENT_LT_PCT}}% | {{CONTENT_ROLE_INSIGHT}} |
| Email | {{EMAIL_ROLE}} | {{EMAIL_FT_PCT}}% | {{EMAIL_LT_PCT}}% | {{EMAIL_ROLE_INSIGHT}} |

**Key Insight**: {{FIRST_VS_LAST_TOUCH_KEY_INSIGHT}}

---

## 6. Unattributed Opportunities

BEAM engagements where no marketing touchpoints have been identified. These deals entered the pipeline through channels not captured by digital marketing attribution.

### Unattributed BEAM Engagements

| Company | BEAM Stage | Deal Value (AUD) | Likely Source | Notes |
|---------|-----------|-----------------|--------------|-------|
| {{UNATTR_COMPANY_1}} | {{UNATTR_1_BEAM_STAGE}} | ${{UNATTR_1_DEAL_VALUE}} | {{UNATTR_1_SOURCE}} | {{UNATTR_1_NOTES}} |
| {{UNATTR_COMPANY_2}} | {{UNATTR_2_BEAM_STAGE}} | ${{UNATTR_2_DEAL_VALUE}} | {{UNATTR_2_SOURCE}} | {{UNATTR_2_NOTES}} |
| {{UNATTR_COMPANY_3}} | {{UNATTR_3_BEAM_STAGE}} | ${{UNATTR_3_DEAL_VALUE}} | {{UNATTR_3_SOURCE}} | {{UNATTR_3_NOTES}} |
| **Total** | — | **${{TOTAL_UNATTRIBUTED_VALUE}}** | — | — |

**Unattributed pipeline value**: ${{TOTAL_UNATTRIBUTED_VALUE}} ({{UNATTRIBUTED_PIPELINE_PCT}}% of total pipeline)

### Possible Explanations for No Attribution

- **Personal networks and referrals**: Engagement originated through a relationship not tracked by marketing systems
- **Direct outreach**: Sales-initiated contact via phone, email, or in-person meeting with no prior marketing interaction
- **Industry events and conferences**: First contact occurred at an event where digital tracking was not in place
- **Privacy and tracking limitations**: Prospect used ad blockers, cookie consent denial, or other privacy tools that prevented touchpoint capture
- **Tracking window**: Marketing touchpoints may have occurred outside the attribution lookback window ({{ATTRIBUTION_LOOKBACK_WINDOW}})
- **Offline channels**: Word-of-mouth, partner referrals, or media coverage not captured digitally

### Closing the Attribution Gap

| Gap | Recommended Action | Expected Improvement |
|-----|--------------------|----------------------|
| Event leads not tracked | {{GAP_ACTION_EVENTS}} | {{GAP_IMPROVEMENT_EVENTS}} |
| Referral sources unrecorded | {{GAP_ACTION_REFERRALS}} | {{GAP_IMPROVEMENT_REFERRALS}} |
| Offline interactions missing | {{GAP_ACTION_OFFLINE}} | {{GAP_IMPROVEMENT_OFFLINE}} |
| Privacy-related data loss | {{GAP_ACTION_PRIVACY}} | {{GAP_IMPROVEMENT_PRIVACY}} |

---

## 7. Recommendations

### Scale Channels Driving Pipeline

1. **{{SCALE_RECOMMENDATION_1_TITLE}}**
   - Current performance: {{SCALE_REC_1_CURRENT}}
   - Action: {{SCALE_REC_1_ACTION}}
   - Expected impact: {{SCALE_REC_1_IMPACT}}
   - Priority: {{SCALE_REC_1_PRIORITY}}

2. **{{SCALE_RECOMMENDATION_2_TITLE}}**
   - Current performance: {{SCALE_REC_2_CURRENT}}
   - Action: {{SCALE_REC_2_ACTION}}
   - Expected impact: {{SCALE_REC_2_IMPACT}}
   - Priority: {{SCALE_REC_2_PRIORITY}}

### Fix Attribution Gaps

1. **{{ATTRIBUTION_FIX_1_TITLE}}**
   - Current gap: {{ATTR_FIX_1_GAP}}
   - Action: {{ATTR_FIX_1_ACTION}}
   - Expected impact: {{ATTR_FIX_1_IMPACT}}
   - Priority: {{ATTR_FIX_1_PRIORITY}}

2. **{{ATTRIBUTION_FIX_2_TITLE}}**
   - Current gap: {{ATTR_FIX_2_GAP}}
   - Action: {{ATTR_FIX_2_ACTION}}
   - Expected impact: {{ATTR_FIX_2_IMPACT}}
   - Priority: {{ATTR_FIX_2_PRIORITY}}

### Content That Correlates with Deal Progression

| Content / Campaign | BEAM Stage Correlation | Deals Influenced | Engagement Type | Recommendation |
|--------------------|-----------------------|-----------------|-----------------|----------------|
| {{CONTENT_1_NAME}} | {{CONTENT_1_STAGE}} | {{CONTENT_1_DEALS}} | {{CONTENT_1_TYPE}} | {{CONTENT_1_REC}} |
| {{CONTENT_2_NAME}} | {{CONTENT_2_STAGE}} | {{CONTENT_2_DEALS}} | {{CONTENT_2_TYPE}} | {{CONTENT_2_REC}} |
| {{CONTENT_3_NAME}} | {{CONTENT_3_STAGE}} | {{CONTENT_3_DEALS}} | {{CONTENT_3_TYPE}} | {{CONTENT_3_REC}} |

### Content Gaps Supporting Active Engagements

*Content or campaigns that could support active BEAM engagements but do not yet exist.*

| BEAM Engagement | Needed Content / Campaign | Channel | Priority | Rationale |
|----------------|--------------------------|---------|----------|-----------|
| {{CONTENT_GAP_1_ENGAGEMENT}} | {{CONTENT_GAP_1_DESCRIPTION}} | {{CONTENT_GAP_1_CHANNEL}} | {{CONTENT_GAP_1_PRIORITY}} | {{CONTENT_GAP_1_RATIONALE}} |
| {{CONTENT_GAP_2_ENGAGEMENT}} | {{CONTENT_GAP_2_DESCRIPTION}} | {{CONTENT_GAP_2_CHANNEL}} | {{CONTENT_GAP_2_PRIORITY}} | {{CONTENT_GAP_2_RATIONALE}} |

### Prioritised Next Steps

| Priority | Action | Owner | Timeline | Expected Impact |
|----------|--------|-------|----------|-----------------|
| 1 | {{ACTION_1}} | {{ACTION_1_OWNER}} | {{ACTION_1_TIMELINE}} | {{ACTION_1_IMPACT}} |
| 2 | {{ACTION_2}} | {{ACTION_2_OWNER}} | {{ACTION_2_TIMELINE}} | {{ACTION_2_IMPACT}} |
| 3 | {{ACTION_3}} | {{ACTION_3_OWNER}} | {{ACTION_3_TIMELINE}} | {{ACTION_3_IMPACT}} |
| 4 | {{ACTION_4}} | {{ACTION_4_OWNER}} | {{ACTION_4_TIMELINE}} | {{ACTION_4_IMPACT}} |
| 5 | Schedule next BEAM-Marketing alignment review | {{REVIEW_OWNER}} | {{REVIEW_DATE}} | Maintain marketing-sales alignment |

---

## 8. Methodology Notes

### Attribution Model

**Model used**: {{ATTRIBUTION_MODEL}}

| Model | Description | When to Use |
|-------|-------------|-------------|
| **Linear** | Marketing spend distributed equally across all touchpoints | Default model — suitable when all touchpoints are considered equally influential |
| **First-touch** | 100% of credit assigned to the first marketing interaction | Use when measuring which channels generate new pipeline |
| **Last-touch** | 100% of credit assigned to the last marketing interaction before BEAM engagement | Use when measuring which channels directly drive deal creation |
| **Time-decay** | More credit assigned to touchpoints closer to the BEAM engagement start | Use when recency of interaction is considered more influential |

**Model applied in this report**: {{ATTRIBUTION_MODEL_DETAIL}}

### Data Sources

| Source | System | Data Available | Coverage | Notes |
|--------|--------|---------------|----------|-------|
| Google Ads | {{GOOGLE_DATA_SYSTEM}} | {{GOOGLE_DATA_AVAILABLE}} | {{GOOGLE_DATA_COVERAGE}} | {{GOOGLE_DATA_NOTES}} |
| LinkedIn Ads | {{LINKEDIN_DATA_SYSTEM}} | {{LINKEDIN_DATA_AVAILABLE}} | {{LINKEDIN_DATA_COVERAGE}} | {{LINKEDIN_DATA_NOTES}} |
| Website Analytics | {{WEB_DATA_SYSTEM}} | {{WEB_DATA_AVAILABLE}} | {{WEB_DATA_COVERAGE}} | {{WEB_DATA_NOTES}} |
| BEAM Engagements | {{BEAM_DATA_SYSTEM}} | {{BEAM_DATA_AVAILABLE}} | {{BEAM_DATA_COVERAGE}} | {{BEAM_DATA_NOTES}} |
| CRM | {{CRM_DATA_SYSTEM}} | {{CRM_DATA_AVAILABLE}} | {{CRM_DATA_COVERAGE}} | {{CRM_DATA_NOTES}} |

### Limitations and Assumptions

- **Attribution lookback window**: {{ATTRIBUTION_LOOKBACK_WINDOW}} — touchpoints outside this window are not included
- **Offline interactions**: Phone calls, in-person meetings, and event attendance are not captured unless manually recorded in the CRM
- **Cross-device tracking**: Users interacting across multiple devices may not be unified, potentially under-counting touchpoints
- **Privacy controls**: Ad blockers, cookie consent denial, and browser privacy features reduce trackable interactions by an estimated {{PRIVACY_DATA_LOSS_ESTIMATE}}%
- **Platform discrepancies**: Google Ads and LinkedIn Ads use different conversion attribution windows and methodologies; GA4 is used as the reconciliation source
- **Currency**: All values are in AUD. Where source data was in another currency, the period average exchange rate of {{EXCHANGE_RATE}} was applied
- **BEAM stage definitions**: Stages follow SAS-AM's standard BEAM framework — Qualify, Diagnose, Align, Propose, Commit, Deliver
- **Deal values**: Deal values are taken from BEAM engagement records at the time of report generation and may change as engagements progress

### Data Written to BEAM Engagements

The following `marketing_attribution` objects were written to `.beam/engagements/` files:

| File | Company | Touchpoints Added | First Touch | Last Updated |
|------|---------|-------------------|-------------|-------------|
| {{FILE_1_NAME}} | {{FILE_1_COMPANY}} | {{FILE_1_TOUCHPOINTS}} | {{FILE_1_FIRST_TOUCH}} — {{FILE_1_FIRST_TOUCH_DATE}} | {{FILE_1_LAST_UPDATED}} |
| {{FILE_2_NAME}} | {{FILE_2_COMPANY}} | {{FILE_2_TOUCHPOINTS}} | {{FILE_2_FIRST_TOUCH}} — {{FILE_2_FIRST_TOUCH_DATE}} | {{FILE_2_LAST_UPDATED}} |

#### Schema Reference

Each `marketing_attribution` object follows this schema:

```json
{
  "marketing_attribution": {
    "first_touch_channel": "{{SCHEMA_FIRST_TOUCH_CHANNEL}}",
    "first_touch_date": "{{SCHEMA_FIRST_TOUCH_DATE}}",
    "first_touch_campaign": "{{SCHEMA_FIRST_TOUCH_CAMPAIGN}}",
    "touchpoints": [
      {
        "date": "{{SCHEMA_TP_DATE}}",
        "channel": "{{SCHEMA_TP_CHANNEL}}",
        "type": "ad_click | website_visit | content_download | email_open | social_engagement",
        "campaign": "{{SCHEMA_TP_CAMPAIGN}}",
        "detail": "{{SCHEMA_TP_DETAIL}}"
      }
    ],
    "total_marketing_spend_attributed": {{SCHEMA_SPEND}},
    "attribution_model": "{{SCHEMA_ATTRIBUTION_MODEL}}",
    "last_updated": "{{SCHEMA_LAST_UPDATED}}"
  }
}
```

---

*This report was generated by MBP:marketing-dashboard. Attribution uses a {{ATTRIBUTION_MODEL}} model applied to available digital touchpoint data. Offline touchpoints (phone calls, in-person meetings, events) are not captured unless manually recorded. All currency values are in AUD.*
