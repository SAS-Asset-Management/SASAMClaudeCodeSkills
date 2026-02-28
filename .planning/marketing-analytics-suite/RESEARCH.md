# Marketing Analytics Suite — API & Ecosystem Research

**Research Date:** 2026-02-28
**Purpose:** Inform the design of a Claude Code skill suite that joins marketing, ads, and website data across Google Ads, LinkedIn Campaign Manager, and Google Analytics 4 (GA4).

---

## 1. Google Ads API

### Overview
- **Current version:** v19 (latest stable, Jan 2026)
- **Protocol:** gRPC + REST (REST is secondary)
- **Query language:** GAQL (Google Ads Query Language) — SQL-like syntax for querying campaign data
- **Base URL:** `googleads.googleapis.com`

### Authentication
- **OAuth 2.0** — standard Google auth flow (consent screen → authorisation code → access/refresh tokens)
- **Developer token** — required for all API calls, obtained through Google Ads Manager account
- **Client ID + Client Secret** — from Google Cloud Console
- **Login Customer ID** — required when accessing accounts via a manager hierarchy
- **Refresh token** — long-lived, used to mint new access tokens

### Key Resources & GAQL Examples
| Resource | Description | Example GAQL |
|---|---|---|
| `campaign` | Campaign-level data | `SELECT campaign.name, metrics.impressions, metrics.clicks, metrics.cost_micros FROM campaign WHERE segments.date DURING LAST_30_DAYS` |
| `ad_group` | Ad group within campaigns | `SELECT ad_group.name, metrics.conversions FROM ad_group WHERE campaign.id = 123` |
| `ad_group_ad` | Individual ads | `SELECT ad_group_ad.ad.responsive_search_ad.headlines FROM ad_group_ad` |
| `keyword_view` | Search keyword performance | `SELECT segments.keyword.info.text, metrics.impressions FROM keyword_view` |
| `customer` | Account-level summary | `SELECT customer.descriptive_name, metrics.cost_micros FROM customer` |
| `search_term_view` | Actual search terms | `SELECT search_term_view.search_term, metrics.clicks FROM search_term_view` |
| `campaign_budget` | Budget data | `SELECT campaign_budget.amount_micros FROM campaign_budget` |
| `conversion_action` | Conversion tracking | `SELECT conversion_action.name, metrics.conversions FROM conversion_action` |
| `landing_page_view` | Landing page performance | `SELECT landing_page_view.unexpanded_final_url, metrics.clicks FROM landing_page_view` |

### Key Metrics Available
| Metric | Field | Notes |
|---|---|---|
| Impressions | `metrics.impressions` | Times ad was shown |
| Clicks | `metrics.clicks` | Total clicks |
| Cost | `metrics.cost_micros` | Cost in micros (divide by 1,000,000 for AUD) |
| Conversions | `metrics.conversions` | Completed conversion actions |
| Conversion value | `metrics.conversions_value` | Monetary value of conversions |
| CTR | `metrics.ctr` | Click-through rate |
| CPC | `metrics.average_cpc` | Average cost per click (micros) |
| ROAS | `metrics.conversions_value / metrics.cost_micros` | Calculated — return on ad spend |
| Quality Score | `ad_group_criterion.quality_info.quality_score` | 1-10 keyword quality |
| Impression Share | `metrics.search_impression_share` | % of available impressions captured |
| Search Lost IS (Budget) | `metrics.search_budget_lost_impression_share` | % lost due to budget |
| Search Lost IS (Rank) | `metrics.search_rank_lost_impression_share` | % lost due to ad rank |

### Segmentation
GAQL supports `segments.*` for breaking down metrics:
- `segments.date` — daily breakdown
- `segments.device` — desktop/mobile/tablet
- `segments.ad_network_type` — search/display/YouTube
- `segments.conversion_action` — by conversion type
- `segments.geo_target_city` / `segments.geo_target_region` — geographic

### Rate Limits & Quotas
| Access Level | Daily Operations | Mutate Operations |
|---|---|---|
| Basic | 15,000/day | 10,000/day |
| Standard | Unlimited | Unlimited |
- Standard access requires application (usage history, compliance review)
- Page size max: 10,000 rows per request
- Requests can be paginated via `page_token`

### Python Client Library
- **Package:** `google-ads` (PyPI)
- **Install:** `pip install google-ads`
- **Config:** `google-ads.yaml` file with developer_token, client_id, client_secret, refresh_token, login_customer_id
- **Usage pattern:**
```python
from google.ads.googleads.client import GoogleAdsClient

client = GoogleAdsClient.load_from_storage("google-ads.yaml")
ga_service = client.get_service("GoogleAdsService")
query = "SELECT campaign.name, metrics.impressions FROM campaign"
response = ga_service.search(customer_id="1234567890", query=query)
for row in response:
    print(row.campaign.name, row.metrics.impressions)
```

### Existing MCP Servers
| Server | Repo | Notes |
|---|---|---|
| **cohnen/mcp-google-ads** | github.com/cohnen/mcp-google-ads | Python, read-only, GAQL queries |
| **gomarble-ai/google-ads-mcp-server** | github.com/gomarble-ai/google-ads-mcp-server | Full campaign management |
| **TrueClicks/google-ads-mcp-js** | github.com/TrueClicks/google-ads-mcp-js | JavaScript/TypeScript |
| **amekala/ads-mcp** | github.com/amekala/ads-mcp | Multi-platform (Google + Meta + LinkedIn + TikTok) |
| **Flyweel** | flyweel.co | Free Google + Meta MCP, recommended for 2026 |

### Google Ads → GA4 Linking
- Google Ads accounts can be linked to GA4 properties
- Enables seeing GA4 conversion data in Google Ads and vice versa
- Auto-tagging (`gclid`) tracks ad clicks through to website conversions
- Shared audiences between platforms
- Cross-platform attribution via Google's data-driven attribution model

---

## 2. LinkedIn Campaign Manager API (Marketing API)

### Overview
- **Current version:** Marketing 2026-02 (versioned API)
- **Protocol:** REST (Rest.li protocol)
- **Base URL:** `https://api.linkedin.com/rest/`
- **Documentation:** learn.microsoft.com/en-us/linkedin/marketing/

### Authentication
- **OAuth 2.0** — authorisation code flow (3-legged)
- **Scope required:** `rw_ads` (read-write advertising)
- **Access token** — short-lived, obtained via OAuth flow
- **Refresh token** — for token renewal
- **Ad Account ID** — 9-digit ID from Campaign Manager, must be registered in Developer Portal

### Access Tiers
| Tier | Permissions | Limits |
|---|---|---|
| Development | GET unlimited, POST for 5 accounts | Testing and development |
| Standard | Full CRUD, unlimited accounts | Production use |
| Marketing Developer Platform Partner | Broadest access, higher rate limits | Formal partnership agreement |

### Key Resources & Endpoints
| Resource | Endpoint | Methods |
|---|---|---|
| Ad Accounts | `/adAccounts/{id}` | GET, POST, PATCH |
| Campaigns | `/adAccounts/{id}/adCampaigns` | GET, POST, PATCH |
| Campaign Groups | `/adAccounts/{id}/adCampaignGroups` | GET, POST, PATCH |
| Creatives | `/adAccounts/{id}/creatives` | GET, POST, PATCH |
| Audiences | `/adAccounts/{id}/audienceGroups` | GET, POST |
| Analytics | `/adAccounts/{id}/adAnalytics` | GET |

### Analytics & Reporting
**Endpoints:**
- **Analytics Finder:** Single pivot (group by one dimension)
- **Statistics Finder:** Up to three pivots
- **Endpoint:** `/adAccounts/{id}/adAnalytics`

**Available Metrics:**
| Metric | Description | Notes |
|---|---|---|
| Impressions | Times ads shown | Exact count |
| Clicks | Total ad clicks | Includes social clicks |
| Engagement Rate | % who interacted | Calculated |
| Conversions | Completed actions | Requires conversion tracking |
| Reach | Approximate campaign reach | Privacy-protected estimate |
| Spend | Total ad expenditure | In account currency |
| Cost per Click | Average CPC | Calculated |
| Cost per Impression | CPM | Calculated |
| Social Actions | Likes, comments, shares | LinkedIn-specific |

**Demographic Breakdowns:**
- Job title, job function, seniority
- Company name, company size, industry
- Geographic location
- All demographic metrics are approximate (privacy protection)

### Conversion Tracking

**Insight Tag (Client-Side):**
- JavaScript pixel placed on website
- Tracks: page visits, button clicks, form submissions
- Enables retargeting audiences
- Provides demographic insights about website visitors
- Cookie-dependent (impacted by Safari/Firefox cookie blocking, Chrome phase-out)

**Conversions API — CAPI (Server-Side):**
- Server-to-server integration, cookieless
- Tracks online and offline conversions (phone calls, in-person meetings, CRM events)
- Attribution windows: up to 365 days for leads/purchases, 90 days for others
- Can run alongside Insight Tag — LinkedIn auto-deduplicates
- Processing: up to 24 hours to appear in Campaign Manager

### Python Client Library
- **Package:** `linkedin-api-python-client` (PyPI)
- **Official:** Yes, maintained by LinkedIn
- **Status:** Available but may still be maturing
- **Alternative:** Direct REST calls with `requests` library

### Existing MCP Servers
| Server | Repo | Focus |
|---|---|---|
| **CData LinkedIn Ads MCP** | github.com/CDataSoftware/linkedin-ads-mcp-server-by-cdata | Read-only, JDBC-backed |
| **Radiate B2B LinkedIn Ads** | github.com/radiateb2b/mcp-linkedin-ads | Performance analysis, benchmarks |
| **danielpopamd/linkedin-ads-mcp** | mcpservers.org | Campaign optimisation |
| **Zapier LinkedIn Ads MCP** | zapier.com/mcp/linkedin-ads | No-code, 8000+ integrations |
| **amekala/ads-mcp** | github.com/amekala/ads-mcp | Multi-platform (includes LinkedIn) |

### Rate Limits
- **Not publicly documented** — endpoint-specific
- Developers check limits via Developer Portal → Analytics tab
- 429 response = rate limit exceeded
- Email alert at 75% of quota
- Higher limits available through Marketing Developer Platform Partner tier

---

## 3. Google Analytics 4 (GA4) Data API

### Overview
- **Current version:** GA4 Data API v1 (stable)
- **Protocol:** REST + gRPC
- **Base URL:** `analyticsdata.googleapis.com`
- **Purpose:** Extract website/app analytics data programmatically

### Authentication
- **OAuth 2.0** or **Service Account** (for server-to-server)
- **Property ID** — GA4 property identifier (numeric)
- **Scopes:** `analytics.readonly` for read access

### Key Dimensions & Metrics
**Dimensions:**
- `date`, `dateHour`, `dateHourMinute`
- `sessionSource`, `sessionMedium`, `sessionCampaignName` — traffic source attribution
- `pagePath`, `pageTitle`, `landingPage`
- `city`, `country`, `region`
- `deviceCategory` — desktop/mobile/tablet
- `firstUserSource`, `firstUserMedium` — acquisition source
- `sessionGoogleAdsAdGroupName`, `sessionGoogleAdsQuery` — Google Ads dimensions

**Metrics:**
- `sessions`, `totalUsers`, `newUsers`
- `screenPageViews`, `engagedSessions`, `engagementRate`
- `bounceRate`, `averageSessionDuration`
- `conversions`, `eventCount`
- `ecommercePurchases`, `purchaseRevenue`
- `advertiserAdCost`, `advertiserAdClicks` — imported Google Ads data

### GA4 → Google Ads Integration
- Linked GA4 properties share conversion data with Google Ads
- GA4 audiences can be exported to Google Ads for remarketing
- Google Ads cost data can be imported into GA4 reports
- Auto-tagging via `gclid` parameter enables cross-platform attribution

### GA4 → LinkedIn Attribution
- UTM parameters: `utm_source=linkedin&utm_medium=paid_social&utm_campaign={campaign_name}`
- LinkedIn click tracking passes UTM params to landing page
- GA4 captures these as session source/medium/campaign dimensions
- Manual matching required (no native GA4-LinkedIn integration like GA4-Google Ads)

### Python Client Library
- **Package:** `google-analytics-data` (PyPI)
- **Usage:**
```python
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Dimension, Metric

client = BetaAnalyticsDataClient()
request = RunReportRequest(
    property=f"properties/{PROPERTY_ID}",
    dimensions=[Dimension(name="sessionSource"), Dimension(name="sessionMedium")],
    metrics=[Metric(name="sessions"), Metric(name="conversions")],
    date_ranges=[DateRange(start_date="30daysAgo", end_date="today")],
)
response = client.run_report(request)
```

### Existing MCP Servers for GA4
| Server | Notes |
|---|---|
| **adsquared/ga4-mcp-server** | GA4 data access via MCP |
| **Various community servers** | Listed on Awesome MCP Servers |

---

## 4. Cross-Channel Integration Patterns

### The Attribution Challenge
Each platform claims credit for conversions differently:
- **Google Ads:** Data-driven attribution (ML model), or rules-based (last click, first click, linear, time decay, position-based)
- **LinkedIn Ads:** Last-touch attribution within configurable click/view windows (30-day click, 7-day view default)
- **GA4:** Data-driven attribution as default, last-click available

This means the **same conversion will be counted differently** across platforms. A user might:
1. See a LinkedIn ad → click → visit website (LinkedIn claims credit)
2. Later Google the company → click search ad → convert (Google Ads also claims credit)
3. GA4 attributes to the Google Ads click (last touch) or splits credit (data-driven)

### Cross-Channel Metrics Framework
To join data meaningfully, normalise on common metrics:

| Metric | Google Ads Field | LinkedIn Ads Field | GA4 Field | Normalised Name |
|---|---|---|---|---|
| Ad Spend | `metrics.cost_micros / 1e6` | Spend (account currency) | `advertiserAdCost` | `spend` |
| Impressions | `metrics.impressions` | Impressions | N/A (ads only) | `impressions` |
| Clicks | `metrics.clicks` | Clicks | `advertiserAdClicks` | `clicks` |
| CTR | `metrics.ctr` | Clicks / Impressions | Calculated | `ctr` |
| CPC | `metrics.average_cpc / 1e6` | Spend / Clicks | Calculated | `cpc` |
| Conversions | `metrics.conversions` | Conversions | `conversions` | `conversions` |
| Conv. Rate | Conversions / Clicks | Conversions / Clicks | Conversions / Sessions | `conversion_rate` |
| Cost per Conv. | Cost / Conversions | Spend / Conversions | Calculated | `cost_per_conversion` |
| ROAS | Conv. Value / Cost | Conv. Value / Spend | Revenue / Ad Cost | `roas` |

### Data Joining Approaches

**1. Date-Based Join (Simplest)**
- Export daily metrics from each platform
- Join on date for side-by-side comparison
- Limitation: No user-level attribution, just aggregate comparison

**2. UTM-Based Join (Medium)**
- Enforce consistent UTM taxonomy across platforms
- Use GA4 as the common ground (all paid traffic lands on website with UTMs)
- Join GA4 sessions to platform spend data via campaign name matching
- Better attribution but relies on UTM discipline

**3. Warehouse Join (Most Complete)**
- Export all platform data to BigQuery / data warehouse
- Build unified fact tables with common dimensions
- Apply custom attribution models
- Most complex but most accurate

### UTM Taxonomy for SAS-AM

Recommended UTM convention:
```
utm_source:   google | linkedin
utm_medium:   cpc | paid_social | display
utm_campaign: {campaign-name-slug}
utm_content:  {ad-group-or-creative-id}
utm_term:     {keyword} (Google only)
```

### Funnel Framework
| Stage | Metric Focus | Google Ads | LinkedIn Ads | GA4 |
|---|---|---|---|---|
| **Awareness** | Reach, Impressions | Impression share, Display reach | Reach, Impressions, Social actions | New users, Page views |
| **Consideration** | Engagement, Clicks | CTR, Quality Score, CPC | Engagement rate, Social clicks, CTR | Engaged sessions, Engagement rate, Pages/session |
| **Conversion** | Leads, Sales | Conversions, Conv. value, ROAS | Conversions, Lead gen forms | Conversions, Revenue, Goal completions |
| **Retention** | Repeat, LTV | Customer match audiences | Retargeting audiences | Returning users, Cohort retention |

---

## 5. Integration with Existing SAS-AM Skills

### linkedin-post-generator ↔ Marketing Analytics
- **Organic vs Paid comparison:** Compare LinkedIn post performance (organic reach, engagement) with paid campaign metrics
- **Content-informed targeting:** Use top-performing organic topics to inform paid campaign messaging
- **Promotion ROI:** Track which pillar posts driven by paid promotion generate the most website traffic and conversions

### b2b-research-agent ↔ Marketing Analytics
- **Account-based marketing:** Correlate B2B prospect research with LinkedIn ad targeting (company targeting, job title targeting)
- **Research-to-campaign:** Use dossier intelligence to craft targeted ad copy and landing pages
- **Pipeline attribution:** Map which marketing campaigns generated the leads now in the B2B research pipeline

### beam-selling ↔ Marketing Analytics
- **Marketing-influenced pipeline:** Which BEAM Stage 1 prospects were first touched by marketing campaigns?
- **Campaign ROI by deal stage:** Attribute marketing spend to deals at each BEAM stage
- **Content recommendations:** Based on deal stage, recommend which marketing content (ads, posts) to share with prospects

### push-notifications ↔ Marketing Analytics
- **Budget alerts:** Notify when daily/weekly spend exceeds thresholds
- **Performance anomalies:** Alert on sudden drops in CTR, conversion rate, or ROAS
- **Campaign milestones:** Notify when campaigns hit impression/click/conversion targets
- **Scheduled digests:** Morning performance summary via Teams webhook

---

## 6. MCP Server Ecosystem Assessment

### Recommended MCP Stack for SAS-AM

**Google Ads:**
- **Primary:** `cohnen/mcp-google-ads` — Python, well-maintained, read-only (safe for analytics)
- **Alternative:** `gomarble-ai/google-ads-mcp-server` — if write access needed for campaign management
- **Setup:** OAuth credentials + developer token, configured in Claude Code MCP settings

**LinkedIn Ads:**
- **Primary:** `CData/linkedin-ads-mcp-server-by-cdata` — read-only, JDBC-backed, mature
- **Alternative:** `radiateb2b/mcp-linkedin-ads` — includes benchmarking and optimisation
- **Setup:** LinkedIn OAuth app + `rw_ads` scope, ad account ID

**GA4 / Website Analytics:**
- **Primary:** Community GA4 MCP servers (less mature than ads MCPs)
- **Alternative:** Direct GA4 Data API via Python scripts (more reliable)
- **Setup:** Google Cloud service account or OAuth, GA4 property ID

**Multi-Platform (If simplicity preferred):**
- **Primary:** `amekala/ads-mcp` — single MCP covering Google, Meta, LinkedIn, TikTok
- **Trade-off:** Less depth per platform, but simpler setup

### MCP Configuration Example
```json
{
  "mcpServers": {
    "google-ads": {
      "command": "uvx",
      "args": ["mcp-google-ads"],
      "env": {
        "GOOGLE_ADS_DEVELOPER_TOKEN": "...",
        "GOOGLE_ADS_CLIENT_ID": "...",
        "GOOGLE_ADS_CLIENT_SECRET": "...",
        "GOOGLE_ADS_REFRESH_TOKEN": "...",
        "GOOGLE_ADS_LOGIN_CUSTOMER_ID": "..."
      }
    },
    "linkedin-ads": {
      "command": "node",
      "args": ["path/to/linkedin-ads-mcp/index.js"],
      "env": {
        "LINKEDIN_ACCESS_TOKEN": "...",
        "LINKEDIN_AD_ACCOUNT_ID": "..."
      }
    }
  }
}
```

---

## 7. Key Considerations for Skill Design

### Data Privacy & Security
- Google Ads and LinkedIn Ads data may contain business-sensitive campaign strategies, budgets, and audience targeting
- All data processing should remain local (consistent with SAS-AM's local-first approach)
- OAuth tokens should never be stored in skill files or committed to git
- MCP server configuration handles credential management separately

### Metric Normalisation
- Google Ads reports costs in **micros** (multiply by 1e-6 for currency)
- LinkedIn Ads reports costs in **account currency** (direct values)
- GA4 reports costs only when imported from linked Google Ads accounts
- All skills should normalise to AUD with consistent decimal formatting

### Attribution Caveats
- Cross-platform attribution is inherently imperfect
- Each platform over-counts conversions (they all claim credit)
- The skill should clearly communicate attribution methodology and limitations
- Recommend using GA4 as the "source of truth" for website conversions, with platform-reported conversions as directional guidance

### B2B Context
- SAS-AM is B2B (asset management professionals)
- Typical conversion cycles are long (weeks to months)
- LinkedIn is often the primary paid channel for B2B (professional targeting)
- Google Ads serves search intent (people actively looking for solutions)
- Website analytics tracks the consideration/research phase
- The skill should account for longer attribution windows and multi-touch journeys

---

*Research compiled: 2026-02-28*
