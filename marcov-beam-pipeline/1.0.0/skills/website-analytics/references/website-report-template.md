# Website Analytics Report

**Website**: {{WEBSITE_URL}}
**GA4 Property**: {{GA4_PROPERTY_ID}}
**Period**: {{PERIOD_START}} to {{PERIOD_END}}
**Data Source**: {{DATA_SOURCE}}
**Generated**: {{GENERATED_DATE}}

---

## Executive Summary

{{EXECUTIVE_SUMMARY}}

### Key Metrics at a Glance

| Metric | This Period | Previous Period | Change |
|---|---|---|---|
| Sessions | {{SESSIONS}} | {{PREV_SESSIONS}} | {{SESSIONS_CHANGE}} |
| Users | {{USERS}} | {{PREV_USERS}} | {{USERS_CHANGE}} |
| New users | {{NEW_USERS}} | {{PREV_NEW_USERS}} | {{NEW_USERS_CHANGE}} |
| Engagement rate | {{ENGAGEMENT_RATE}} | {{PREV_ENGAGEMENT_RATE}} | {{ENGAGEMENT_RATE_CHANGE}} |
| Conversions | {{CONVERSIONS}} | {{PREV_CONVERSIONS}} | {{CONVERSIONS_CHANGE}} |
| Conversion rate | {{CONVERSION_RATE}} | {{PREV_CONVERSION_RATE}} | {{CONVERSION_RATE_CHANGE}} |
| Top channel (by conversions) | {{TOP_CHANNEL}} | — | — |
| Top converting page | {{TOP_CONVERTING_PAGE}} | — | — |

### Traffic Health Indicator

{{TRAFFIC_HEALTH_SUMMARY}}

- **Overall trend**: {{TREND_DIRECTION}} (growing / stable / declining)
- **New vs returning split**: {{NEW_PCT}}% new / {{RETURNING_PCT}}% returning
- **Device split**: {{DESKTOP_PCT}}% desktop / {{MOBILE_PCT}}% mobile / {{TABLET_PCT}}% tablet

---

## 1. Traffic Source Breakdown

### By Channel Group

| Channel | Sessions | % of Total | Users | Engagement Rate | Conversions | Conv. Rate | vs Prev. Period |
|---|---|---|---|---|---|---|---|
| Organic Search | {{ORG_SEARCH_SESSIONS}} | {{ORG_SEARCH_PCT}} | {{ORG_SEARCH_USERS}} | {{ORG_SEARCH_ENG}} | {{ORG_SEARCH_CONV}} | {{ORG_SEARCH_CR}} | {{ORG_SEARCH_CHANGE}} |
| Paid Search | {{PAID_SEARCH_SESSIONS}} | {{PAID_SEARCH_PCT}} | {{PAID_SEARCH_USERS}} | {{PAID_SEARCH_ENG}} | {{PAID_SEARCH_CONV}} | {{PAID_SEARCH_CR}} | {{PAID_SEARCH_CHANGE}} |
| Paid Social | {{PAID_SOCIAL_SESSIONS}} | {{PAID_SOCIAL_PCT}} | {{PAID_SOCIAL_USERS}} | {{PAID_SOCIAL_ENG}} | {{PAID_SOCIAL_CONV}} | {{PAID_SOCIAL_CR}} | {{PAID_SOCIAL_CHANGE}} |
| Organic Social | {{ORG_SOCIAL_SESSIONS}} | {{ORG_SOCIAL_PCT}} | {{ORG_SOCIAL_USERS}} | {{ORG_SOCIAL_ENG}} | {{ORG_SOCIAL_CONV}} | {{ORG_SOCIAL_CR}} | {{ORG_SOCIAL_CHANGE}} |
| Direct | {{DIRECT_SESSIONS}} | {{DIRECT_PCT}} | {{DIRECT_USERS}} | {{DIRECT_ENG}} | {{DIRECT_CONV}} | {{DIRECT_CR}} | {{DIRECT_CHANGE}} |
| Referral | {{REFERRAL_SESSIONS}} | {{REFERRAL_PCT}} | {{REFERRAL_USERS}} | {{REFERRAL_ENG}} | {{REFERRAL_CONV}} | {{REFERRAL_CR}} | {{REFERRAL_CHANGE}} |
| Email | {{EMAIL_SESSIONS}} | {{EMAIL_PCT}} | {{EMAIL_USERS}} | {{EMAIL_ENG}} | {{EMAIL_CONV}} | {{EMAIL_CR}} | {{EMAIL_CHANGE}} |
| Display | {{DISPLAY_SESSIONS}} | {{DISPLAY_PCT}} | {{DISPLAY_USERS}} | {{DISPLAY_ENG}} | {{DISPLAY_CONV}} | {{DISPLAY_CR}} | {{DISPLAY_CHANGE}} |
| **Total** | **{{TOTAL_SESSIONS}}** | **100%** | **{{TOTAL_USERS}}** | **{{TOTAL_ENG}}** | **{{TOTAL_CONV}}** | **{{TOTAL_CR}}** | **{{TOTAL_CHANGE}}** |

### By Source / Medium (Top 15)

| Source / Medium | Sessions | Engagement Rate | Conversions | Conv. Rate |
|---|---|---|---|---|
| {{SOURCE_MEDIUM_1}} | {{SM1_SESSIONS}} | {{SM1_ENG}} | {{SM1_CONV}} | {{SM1_CR}} |
| {{SOURCE_MEDIUM_2}} | {{SM2_SESSIONS}} | {{SM2_ENG}} | {{SM2_CONV}} | {{SM2_CR}} |
| ... | ... | ... | ... | ... |

### Attribution Integrity Check

| Check | Status | Notes |
|---|---|---|
| Google Ads auto-tagging active | {{GADS_AUTOTAGGING}} | {{GADS_AUTOTAGGING_NOTES}} |
| LinkedIn Ads UTM-tagged | {{LI_UTM_STATUS}} | {{LI_UTM_NOTES}} |
| Direct traffic proportion | {{DIRECT_PROPORTION}} | {{DIRECT_NOTES}} |
| UTM consistency (per taxonomy) | {{UTM_CONSISTENCY}} | {{UTM_NOTES}} |

---

## 2. Content Performance

### Top Pages by Sessions

| Page | Sessions | Avg. Engagement Time | Engagement Rate | Conversions | Conv. Rate |
|---|---|---|---|---|---|
| {{PAGE_1}} | {{P1_SESSIONS}} | {{P1_ENG_TIME}} | {{P1_ENG_RATE}} | {{P1_CONV}} | {{P1_CR}} |
| {{PAGE_2}} | {{P2_SESSIONS}} | {{P2_ENG_TIME}} | {{P2_ENG_RATE}} | {{P2_CONV}} | {{P2_CR}} |
| {{PAGE_3}} | {{P3_SESSIONS}} | {{P3_ENG_TIME}} | {{P3_ENG_RATE}} | {{P3_CONV}} | {{P3_CR}} |
| ... | ... | ... | ... | ... | ... |

### Content by Section

| Section | Sessions | % of Total | Engagement Rate | Conversions | Conv. Rate |
|---|---|---|---|---|---|
| Homepage | {{HOME_SESSIONS}} | {{HOME_PCT}} | {{HOME_ENG}} | {{HOME_CONV}} | {{HOME_CR}} |
| Service pages | {{SVC_SESSIONS}} | {{SVC_PCT}} | {{SVC_ENG}} | {{SVC_CONV}} | {{SVC_CR}} |
| Blog / Insights | {{BLOG_SESSIONS}} | {{BLOG_PCT}} | {{BLOG_ENG}} | {{BLOG_CONV}} | {{BLOG_CR}} |
| Resources / Downloads | {{RES_SESSIONS}} | {{RES_PCT}} | {{RES_ENG}} | {{RES_CONV}} | {{RES_CR}} |
| Contact / Conversion pages | {{CONTACT_SESSIONS}} | {{CONTACT_PCT}} | {{CONTACT_ENG}} | {{CONTACT_CONV}} | {{CONTACT_CR}} |
| Other | {{OTHER_SESSIONS}} | {{OTHER_PCT}} | {{OTHER_ENG}} | {{OTHER_CONV}} | {{OTHER_CR}} |

### Blog / Insight Content Performance (Top 10)

| Post | Published | Sessions | Engagement Rate | Conversions | Content Pillar |
|---|---|---|---|---|---|
| {{BLOG_1_TITLE}} | {{BLOG_1_DATE}} | {{BLOG_1_SESSIONS}} | {{BLOG_1_ENG}} | {{BLOG_1_CONV}} | {{BLOG_1_PILLAR}} |
| {{BLOG_2_TITLE}} | {{BLOG_2_DATE}} | {{BLOG_2_SESSIONS}} | {{BLOG_2_ENG}} | {{BLOG_2_CONV}} | {{BLOG_2_PILLAR}} |
| ... | ... | ... | ... | ... | ... |

### Content Pillar Performance

| Pillar | Pages | Total Sessions | Avg. Engagement Rate | Total Conversions | Avg. Conv. Rate |
|---|---|---|---|---|---|
| {{PILLAR_1}} | {{P1_PAGES}} | {{P1_SESSIONS}} | {{P1_ENG}} | {{P1_CONV}} | {{P1_CR}} |
| {{PILLAR_2}} | {{P2_PAGES}} | {{P2_SESSIONS}} | {{P2_ENG}} | {{P2_CONV}} | {{P2_CR}} |
| ... | ... | ... | ... | ... | ... |

### Content That Converts vs Content That Only Drives Traffic

**High conversion pages (traffic + conversions):**
{{HIGH_CONVERSION_PAGES}}

**High traffic, low conversion pages (awareness only):**
{{HIGH_TRAFFIC_LOW_CONVERSION_PAGES}}

**Assessment:** {{CONTENT_CONVERSION_ASSESSMENT}}

---

## 3. Conversion Funnel

### Funnel Overview

```
Sessions: {{SESSIONS}}
    │
    ▼ ({{ENGAGE_DROP_PCT}}% drop-off)
Engaged Sessions: {{ENGAGED_SESSIONS}} ({{ENGAGEMENT_RATE}})
    │
    ▼ ({{CONVERT_DROP_PCT}}% drop-off)
Conversions: {{CONVERSIONS}} ({{CONVERSION_RATE}} of all sessions)
```

### Conversion Rate by Source

| Source | Sessions | Engaged Sessions | Eng. Rate | Conversions | Conv. Rate | vs Site Avg |
|---|---|---|---|---|---|---|
| {{SOURCE_1}} | {{S1_SESSIONS}} | {{S1_ENGAGED}} | {{S1_ENG_RATE}} | {{S1_CONV}} | {{S1_CR}} | {{S1_VS_AVG}} |
| {{SOURCE_2}} | {{S2_SESSIONS}} | {{S2_ENGAGED}} | {{S2_ENG_RATE}} | {{S2_CONV}} | {{S2_CR}} | {{S2_VS_AVG}} |
| ... | ... | ... | ... | ... | ... | ... |

### Landing Page Conversion Performance

| Landing Page | Sessions | Conversions | Conv. Rate | Primary Source |
|---|---|---|---|---|
| {{LP_1}} | {{LP1_SESSIONS}} | {{LP1_CONV}} | {{LP1_CR}} | {{LP1_SOURCE}} |
| {{LP_2}} | {{LP2_SESSIONS}} | {{LP2_CONV}} | {{LP2_CR}} | {{LP2_SOURCE}} |
| ... | ... | ... | ... | ... |

### Conversion by Type

| Conversion Event | Count | % of Total | Primary Source |
|---|---|---|---|
| {{EVENT_1}} | {{E1_COUNT}} | {{E1_PCT}} | {{E1_SOURCE}} |
| {{EVENT_2}} | {{E2_COUNT}} | {{E2_PCT}} | {{E2_SOURCE}} |
| ... | ... | ... | ... |

### Multi-Touch Attribution (if available)

**Average conversion path length**: {{AVG_PATH_LENGTH}} touchpoints
**Average time to conversion**: {{AVG_TIME_TO_CONV}} days

| Channel Role | First Touch | Assisted | Last Touch |
|---|---|---|---|
| Organic Search | {{ORG_FT}} | {{ORG_ASSIST}} | {{ORG_LT}} |
| Paid Search | {{PAID_FT}} | {{PAID_ASSIST}} | {{PAID_LT}} |
| Paid Social | {{SOCIAL_FT}} | {{SOCIAL_ASSIST}} | {{SOCIAL_LT}} |
| Direct | {{DIR_FT}} | {{DIR_ASSIST}} | {{DIR_LT}} |
| Email | {{EMAIL_FT}} | {{EMAIL_ASSIST}} | {{EMAIL_LT}} |
| Referral | {{REF_FT}} | {{REF_ASSIST}} | {{REF_LT}} |

{{MULTI_TOUCH_COMMENTARY}}

---

## 4. Channel Attribution

### Cross-Channel Performance Summary

This section connects website analytics to upstream ad platform data for true attribution.

| Channel | Ad Platform Clicks | GA4 Sessions | Discrepancy | GA4 Conversions | Cost (from platform) | True CPA |
|---|---|---|---|---|---|---|
| Google Ads | {{GADS_CLICKS}} | {{GADS_GA4_SESSIONS}} | {{GADS_DISCREPANCY}} | {{GADS_GA4_CONV}} | {{GADS_SPEND}} | {{GADS_TRUE_CPA}} |
| LinkedIn Ads | {{LI_CLICKS}} | {{LI_GA4_SESSIONS}} | {{LI_DISCREPANCY}} | {{LI_GA4_CONV}} | {{LI_SPEND}} | {{LI_TRUE_CPA}} |

**Notes:**
- GA4 sessions may differ from ad platform clicks due to: page load failures, consent banner blocking, redirect losses, and bot filtering
- A discrepancy of <15% between platform clicks and GA4 sessions is normal
- Discrepancy >25% warrants investigation into tracking integrity

### Attribution Model Context

**GA4 attribution model**: {{ATTRIBUTION_MODEL}}
**Impact**: {{ATTRIBUTION_MODEL_IMPACT}}

---

## 5. User Behaviour

### New vs Returning Users

| Metric | New Users | Returning Users | Delta |
|---|---|---|---|
| Sessions | {{NEW_SESSIONS}} | {{RETURNING_SESSIONS}} | {{NR_DELTA_SESSIONS}} |
| Engagement rate | {{NEW_ENG_RATE}} | {{RETURNING_ENG_RATE}} | {{NR_DELTA_ENG}} |
| Pages per session | {{NEW_PPS}} | {{RETURNING_PPS}} | {{NR_DELTA_PPS}} |
| Avg. engagement time | {{NEW_ENG_TIME}} | {{RETURNING_ENG_TIME}} | {{NR_DELTA_TIME}} |
| Conversion rate | {{NEW_CR}} | {{RETURNING_CR}} | {{NR_DELTA_CR}} |

### Device Breakdown

| Device | Sessions | Engagement Rate | Conv. Rate | Notes |
|---|---|---|---|---|
| Desktop | {{DESKTOP_SESSIONS}} | {{DESKTOP_ENG}} | {{DESKTOP_CR}} | {{DESKTOP_NOTES}} |
| Mobile | {{MOBILE_SESSIONS}} | {{MOBILE_ENG}} | {{MOBILE_CR}} | {{MOBILE_NOTES}} |
| Tablet | {{TABLET_SESSIONS}} | {{TABLET_ENG}} | {{TABLET_CR}} | {{TABLET_NOTES}} |

### Top Exit Pages

| Page | Exit Count | Exit Rate | Concern Level |
|---|---|---|---|
| {{EXIT_1}} | {{EXIT_1_COUNT}} | {{EXIT_1_RATE}} | {{EXIT_1_CONCERN}} |
| {{EXIT_2}} | {{EXIT_2_COUNT}} | {{EXIT_2_RATE}} | {{EXIT_2_CONCERN}} |
| {{EXIT_3}} | {{EXIT_3_COUNT}} | {{EXIT_3_RATE}} | {{EXIT_3_CONCERN}} |
| ... | ... | ... | ... |

**Exit page notes**: Exit from confirmation/thank-you pages is expected. Exit from service pages or mid-funnel content is a concern worth investigating.

---

## 6. Recommendations

### SEO Opportunities

| Priority | Recommendation | Expected Impact | Effort |
|---|---|---|---|
| {{SEO_1_PRIORITY}} | {{SEO_1_REC}} | {{SEO_1_IMPACT}} | {{SEO_1_EFFORT}} |
| {{SEO_2_PRIORITY}} | {{SEO_2_REC}} | {{SEO_2_IMPACT}} | {{SEO_2_EFFORT}} |
| ... | ... | ... | ... |

### Conversion Rate Optimisation

| Priority | Recommendation | Expected Impact | Effort |
|---|---|---|---|
| {{CRO_1_PRIORITY}} | {{CRO_1_REC}} | {{CRO_1_IMPACT}} | {{CRO_1_EFFORT}} |
| {{CRO_2_PRIORITY}} | {{CRO_2_REC}} | {{CRO_2_IMPACT}} | {{CRO_2_EFFORT}} |
| ... | ... | ... | ... |

### Content Strategy

| Priority | Recommendation | Expected Impact | Effort |
|---|---|---|---|
| {{CONTENT_1_PRIORITY}} | {{CONTENT_1_REC}} | {{CONTENT_1_IMPACT}} | {{CONTENT_1_EFFORT}} |
| {{CONTENT_2_PRIORITY}} | {{CONTENT_2_REC}} | {{CONTENT_2_IMPACT}} | {{CONTENT_2_EFFORT}} |
| ... | ... | ... | ... |

### Channel Optimisation

| Priority | Recommendation | Expected Impact | Effort |
|---|---|---|---|
| {{CHANNEL_1_PRIORITY}} | {{CHANNEL_1_REC}} | {{CHANNEL_1_IMPACT}} | {{CHANNEL_1_EFFORT}} |
| {{CHANNEL_2_PRIORITY}} | {{CHANNEL_2_REC}} | {{CHANNEL_2_IMPACT}} | {{CHANNEL_2_EFFORT}} |
| ... | ... | ... | ... |

### Tracking Improvements

| Priority | Issue | Recommendation | Impact if Unresolved |
|---|---|---|---|
| {{TRACK_1_PRIORITY}} | {{TRACK_1_ISSUE}} | {{TRACK_1_REC}} | {{TRACK_1_IMPACT}} |
| {{TRACK_2_PRIORITY}} | {{TRACK_2_ISSUE}} | {{TRACK_2_REC}} | {{TRACK_2_IMPACT}} |
| ... | ... | ... | ... |

---

## Data Notes & Limitations

- **Data source**: {{DATA_SOURCE_DETAIL}}
- **Sampling**: {{SAMPLING_NOTES}}
- **Consent impact**: {{CONSENT_NOTES}}
- **Thresholding**: {{THRESHOLDING_NOTES}}
- **Attribution model**: {{ATTRIBUTION_MODEL_NOTES}}
- **Known gaps**: {{KNOWN_GAPS}}

---

*Report generated by MBP:website-analytics. Metrics normalised to `.marketing/website/latest.json` for MBP:marketing-dashboard integration.*
