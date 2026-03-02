# MBP State Conventions

All MBP skills that persist state use the conventions documented here.

## Directory Structure

```
{working-directory}/
├── .beam/                               # Sales pipeline state (MBP:beam-selling)
│   ├── config.json                      # Seller context (company info, cached once)
│   ├── engagements/
│   │   ├── {company}.json               # Engagement state (JSON)
│   │   ├── {company}-kanban.html        # Interactive dashboard (HTML)
│   │   └── {company}-timeline.md        # Narrative timeline (Markdown)
│   └── sessions/
│       └── {company}-{date}.md          # Session logs (append-only)
│
├── .marketing/                          # Marketing analytics state
│   ├── config.json                      # Budget targets, CPA goals, review cadence
│   ├── google-ads/
│   │   ├── latest.json                  # Most recent normalised metrics
│   │   └── history/
│   │       └── {YYYY-MM-DD}.json        # Historical snapshots
│   ├── linkedin-ads/
│   │   ├── latest.json
│   │   └── history/
│   │       └── {YYYY-MM-DD}.json
│   ├── website/
│   │   ├── latest.json
│   │   └── history/
│   │       └── {YYYY-MM-DD}.json
│   ├── seo/
│   │   ├── latest.json
│   │   └── history/
│   │       └── {YYYY-MM-DD}.json
│   └── content-intel/
│       ├── latest.json                  # Most recent topic scores
│       └── history/
│           └── {YYYY-MM-DD}.json
│
├── .notifications/
│   └── config.json                      # Teams webhook URL, alert thresholds
│
└── generated-images/                    # MBP:nano-banana output
    ├── {timestamp}_{slug}.png           # Raw generation
    ├── {timestamp}_{slug}_final.jpg     # Post-processed (DELIVERABLE)
    └── {timestamp}_{slug}.json          # Generation metadata
```

## Schema References

- **Engagement state:** See `skills/beam-selling/references/beam-state-template.json`
- **Normalised metrics:** See `shared/normalised-metrics-schema.json`
- **Marketing config:** See below

## Marketing Config Schema

`.marketing/config.json`:
```json
{
  "total_monthly_budget": 5500,
  "currency": "AUD",
  "budget_split": {
    "google-ads": 3000,
    "linkedin-ads": 2000,
    "content-seo": 500
  },
  "targets": {
    "max_cpa": 150,
    "min_roas": 3.0,
    "monthly_lead_target": 30
  },
  "review_cadence": "fortnightly",
  "beam_integration": true,
  "push_notifications": {
    "enabled": false,
    "teams_webhook": null,
    "alert_thresholds": {
      "cpa_increase_pct": 25,
      "conversion_drop_pct": 30,
      "budget_pacing_threshold": 0.9
    }
  }
}
```

## Cross-Skill State Access

| Skill | Reads | Writes |
|---|---|---|
| MBP:beam-selling | `.beam/engagements/`, b2b-research dossiers | `.beam/engagements/`, `.beam/sessions/` |
| MBP:b2b-research | — | Dossier HTML/MD in working dir, `.beam/` on ingest |
| MBP:google-ads | `.marketing/config.json` | `.marketing/google-ads/latest.json` |
| MBP:linkedin-ads | `.marketing/config.json` | `.marketing/linkedin-ads/latest.json` |
| MBP:website-analytics | `.marketing/config.json` | `.marketing/website/latest.json` |
| MBP:seo | — | `.marketing/seo/latest.json` |
| MBP:content-intel | — | `.marketing/content-intel/latest.json` |
| MBP:marketing-dashboard | `.marketing/*/latest.json`, `.beam/engagements/` | `.beam/engagements/*.json` (marketing_attribution) |
| MBP:notifications | `.notifications/config.json` | `.notifications/config.json` (statistics) |
| MBP:nano-banana | `~/.claude/skills/nano-banana/config.json` | `generated-images/` |

## Rules

1. **All state is local** — no cloud sync, user owns all data
2. **Never overwrite session logs** — append only
3. **Regenerate dashboards** — kanban HTML is regenerated from JSON at every session end
4. **History is immutable** — `.marketing/*/history/` files are never modified after creation
5. **latest.json is always current** — overwritten each time the platform skill runs
