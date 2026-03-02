# SAS-AM UTM Taxonomy

Standard UTM parameter conventions used across all MBP marketing skills. Consistent UTMs are critical for cross-channel attribution in MBP:marketing-dashboard.

## Parameter Conventions

| Parameter | Format | Example Values |
|---|---|---|
| `utm_source` | Platform name (lowercase) | `google`, `linkedin`, `newsletter`, `event`, `partner`, `reddit` |
| `utm_medium` | Channel type (lowercase) | `cpc`, `paid_social`, `organic_social`, `email`, `referral`, `display` |
| `utm_campaign` | `{platform}-{objective}-{audience}-{YYYYMM}` | `linkedin-leadgen-utilities-202603`, `google-brand-assetmgmt-202603` |
| `utm_content` | Creative or ad group identifier | `iso55001-awareness-v2`, `cmms-data-quality-carousel` |
| `utm_term` | Keyword (Google Ads only) | `asset+management+consultant`, `iso+55001+assessment` |

## Source Values

| Source | When to Use |
|---|---|
| `google` | Google Ads (search, display, YouTube) |
| `linkedin` | LinkedIn Ads (sponsored content, message ads, lead gen forms) |
| `newsletter` | SAS-AM email newsletters |
| `event` | Webinar, conference, or event promotions |
| `partner` | Co-marketing or referral partner links |
| `reddit` | Reddit community engagement (organic posts, not ads) |
| `direct` | Reserved — not set manually (GA4 assigns automatically) |

## Medium Values

| Medium | When to Use |
|---|---|
| `cpc` | Paid search (Google Ads search campaigns) |
| `paid_social` | Paid social (LinkedIn Ads, any paid social platform) |
| `organic_social` | Organic social posts (LinkedIn organic, Reddit) |
| `email` | Email campaigns and newsletters |
| `referral` | Inbound links from external websites |
| `display` | Display advertising (Google Display Network) |
| `video` | YouTube or video ad campaigns |

## Campaign Naming Convention

Format: `{platform}-{objective}-{audience}-{YYYYMM}`

**Objective values:** `brand`, `leadgen`, `traffic`, `retarget`, `content`
**Audience values:** `utilities`, `mining`, `transport`, `government`, `all`, `retarget`

Examples:
- `linkedin-leadgen-utilities-202603`
- `google-brand-assetmgmt-202603`
- `linkedin-content-mining-202604`
- `google-retarget-websitevisitors-202603`

## Enforcement

- All MBP marketing skills (MBP:google-ads, MBP:linkedin-ads, MBP:website-analytics) should validate UTM consistency
- MBP:marketing-dashboard uses UTM parameters as the primary join key for cross-channel attribution
- MBP:content-intel should recommend UTMs when suggesting content distribution
