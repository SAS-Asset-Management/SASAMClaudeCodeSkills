# Tender Assessment Skill

Automated Victorian government tender discovery, alignment scoring, and pursuit package generation.

## What It Does

1. **Scrapes** open tenders from tenders.vic.gov.au
2. **Scores** each tender against marcov's capabilities using a weighted matrix
3. **Shortlists** opportunities with ≥80% alignment
4. **Generates** full pursuit packages for qualified opportunities

## Usage

```bash
# In Claude Code CLI
/tender-assessment
```

### Common Workflows

- **"Run tender assessment"** - Full scan of all open tenders
- **"Check for new tenders"** - Last 24 hours only
- **"Generate pursuit package for RFT-12345"** - Single tender deep dive

## Outputs

### Shortlist Report
- Summary dashboard with counts
- Categorised tenders (pursue/review/decline)
- Quick assessments and recommendations
- Deadline warnings

### Pursuit Package (per shortlisted tender)
- Go/No-Go recommendation with rationale
- Competitive positioning and win themes
- Draft response outline
- Team requirements
- Risk matrix
- Pricing considerations

## Scoring Matrix

| Dimension | Weight | Top Score |
|-----------|--------|-----------|
| Domain Fit | 30 pts | Core service match |
| Industry Match | 25 pts | Rail/transport |
| Service Type | 20 pts | Advisory work |
| Strategic Value | 15 pts | Tier 1 client |
| Competitive Position | 10 pts | Known relationship |

**Pass threshold**: ≥80 points

## Requirements

- Python 3.x
- `pip install requests beautifulsoup4 lxml`
- `vic_tenders_scraper.py` accessible

## Files

```
tender-assessment/
└── 1.0.0/
    ├── .claude-plugin/plugin.json
    ├── skills/tender-assessment/
    │   ├── SKILL.md
    │   └── references/
    │       ├── company-profile.md
    │       ├── scoring-matrix.md
    │       ├── pursuit-package-template.md
    │       └── shortlist-report-template.md
    ├── vic_tenders_scraper.py
    └── README.md
```

## Customisation

- Edit `company-profile.md` to adjust capabilities and constraints
- Edit `scoring-matrix.md` to change scoring weights
- Modify scraper keywords in `vic_tenders_scraper.py`

## License

MIT
