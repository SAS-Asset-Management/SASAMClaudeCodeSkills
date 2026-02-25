#!/usr/bin/env python3
"""
assess_tenders.py
-----------------
Comprehensive tender assessment with full JSON output.

Usage:
    python assess_tenders.py                          # All open tenders
    python assess_tenders.py --opened-today           # Today's new tenders only
    python assess_tenders.py --output assessment.json # Save to file
    python assess_tenders.py --pretty                 # Pretty-print output

Output:
    Comprehensive JSON with raw data, scoring, analysis, and statistics.
"""

import json
import re
import argparse
import logging
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path

# Import scraper functions
from vic_tenders_scraper import (
    scrape_all_tenders,
    filter_by_keywords,
    MARCOV_KEYWORDS,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

# ── Scoring Configuration ─────────────────────────────────────────────────────

SCORING_VERSION = "2.0.0"

# Auto-decline patterns (always reject regardless of other factors)
AUTO_DECLINE_TITLE = [
    # Construction/capital
    'construction', 'upgrade', 'renewal', 'rehabilitation', 'installation',
    'refurbishment', 'fit out', 'fit-out', 'pipeline', 'pavement', 'road',
    'lighting', 'path', 'dam', 'underpass', 'signal', 'building',

    # Procurement/supply
    'procurement', 'supply', 'delivery', 'purchasing', 'vehicle', 'equipment',
    'locomotive', 'meter', 'switchboard', 'camera', 'gate', 'poles',
    'furniture', 'hardware',

    # Operational services
    'plumbing', 'cleaning', 'waste', 'desludge', 'tree', 'interpreter',
    'catering', 'security guard', 'landscaping', 'printing',
    'maintenance service', 'services panel', 'services register',

    # Clinical/healthcare
    'clinical', 'medical', 'health service', 'nursing', 'pathology',

    # OHS/Environmental
    'hazardous material', 'asbestos', 'contamination', 'remediation',

    # Property
    'leasing', 'real estate', 'property management',
]

AUTO_DECLINE_ISSUER = [
    'holmesglen', 'chisholm', 'tafe', 'university', 'institute',
    'hospital', 'health',
]

# High-value terms indicating genuine fit
HIGH_VALUE_TERMS = [
    'asset management', 'asset strategy', 'asset plan', 'asset performance',
    'asset lifecycle', 'asset data',
    'reliability', 'rcm', 'fmea', 'root cause', 'failure mode',
    'maintenance strategy', 'maintenance optimisation', 'maintenance optimization',
    'predictive maintenance', 'condition monitoring', 'condition assessment',
    'criticality analysis',
    'iso 55001', 'gfmam', 'maturity assessment',
    'predictive model', 'predictive analytics', 'data analytics',
    'lifecycle model', 'lifecycle modelling',
    'fleet management', 'rolling stock',
    'cmms implementation', 'eam implementation', 'maximo',
]

# Tier 1 clients
TIER1_CLIENTS = ['metro trains', 'melbourne water', 'yarra valley water', 'v/line']
TIER2_CLIENTS = ['yarra trams', 'barwon water', 'ausnet', 'gippsland water']


# ── Scoring Functions ─────────────────────────────────────────────────────────

def score_tender(tender: dict) -> dict:
    """
    Score a tender against the alignment matrix.
    Returns full scoring breakdown with rationale.
    """
    title = tender.get('title', '').lower()
    issuer = tender.get('issuer', '').lower()
    tender_type = tender.get('tender_type', '').lower()

    result = {
        'total_score': 0,
        'threshold_met': False,
        'decision': 'DECLINE',
        'dimensions': {},
        'auto_decline_reason': None,
    }

    # Check auto-decline patterns first
    for term in AUTO_DECLINE_TITLE:
        if term in title:
            result['decision'] = 'AUTO-DECLINE'
            result['auto_decline_reason'] = f"Title contains '{term}'"
            return result

    for term in AUTO_DECLINE_ISSUER:
        if term in issuer:
            result['decision'] = 'AUTO-DECLINE'
            result['auto_decline_reason'] = f"Issuer matches '{term}'"
            return result

    # Check RFI without advisory scope
    if 'request for information' in tender_type:
        advisory_terms = ['strategy', 'advisory', 'consulting', 'asset management']
        if not any(term in title for term in advisory_terms):
            result['decision'] = 'AUTO-DECLINE'
            result['auto_decline_reason'] = "RFI without clear advisory scope"
            return result

    # Domain Fit (30 points max)
    domain_score = 0
    domain_rationale = "No domain match identified"

    for term in HIGH_VALUE_TERMS:
        if term in title:
            domain_score = 30
            domain_rationale = f"High fit: '{term}' in title"
            break

    if domain_score == 0:
        medium_terms = ['advisory', 'consulting', 'strategy', 'review', 'assessment']
        for term in medium_terms:
            if term in title:
                domain_score = 20
                domain_rationale = f"Medium fit: '{term}' in title"
                break

    result['dimensions']['domain_fit'] = {
        'score': domain_score,
        'max': 30,
        'rationale': domain_rationale,
    }

    # Industry Match (25 points max)
    industry_score = 0
    industry_rationale = "Industry not matched to target sectors"

    if any(x in issuer for x in ['metro trains', 'v/line', 'yarra tram', 'rail']):
        industry_score = 25
        industry_rationale = "Rail/transport sector - primary target"
    elif any(x in issuer for x in ['water', 'catchment']):
        industry_score = 22
        industry_rationale = "Water sector - growth target"
    elif 'transport' in issuer:
        industry_score = 20
        industry_rationale = "Transport sector - core sector"
    elif 'energy' in issuer:
        industry_score = 18
        industry_rationale = "Energy sector - strong fit"
    elif any(x in issuer for x in ['mining', 'resources']):
        industry_score = 15
        industry_rationale = "Mining/resources sector"

    result['dimensions']['industry_match'] = {
        'score': industry_score,
        'max': 25,
        'rationale': industry_rationale,
    }

    # Service Type (20 points max)
    service_score = 0
    service_rationale = "Service type unclear or not advisory"

    if any(x in title for x in ['advisory', 'advisor', 'consulting', 'strategy']):
        service_score = 20
        service_rationale = "Advisory/strategy work"
    elif any(x in title for x in ['assessment', 'analysis', 'study', 'diagnostic', 'audit', 'review']):
        service_score = 18
        service_rationale = "Technical analysis/assessment"
    elif any(x in title for x in ['modelling', 'model', 'analytics']):
        service_score = 18
        service_rationale = "Modelling/analytics work"
    elif any(x in title for x in ['support', 'training', 'implementation']):
        service_score = 12
        service_rationale = "Implementation support"

    result['dimensions']['service_type'] = {
        'score': service_score,
        'max': 20,
        'rationale': service_rationale,
    }

    # Strategic Value (15 points max)
    strategic_score = 0
    strategic_rationale = "Limited strategic value"

    if any(x in issuer for x in TIER1_CLIENTS):
        strategic_score = 15
        strategic_rationale = "Tier 1 client - high reference value"
    elif any(x in issuer for x in TIER2_CLIENTS):
        strategic_score = 12
        strategic_rationale = "Tier 2 client - good reference value"
    elif 'water' in issuer:
        strategic_score = 10
        strategic_rationale = "Water sector - strategic growth area"
    elif 'transport' in issuer or 'department of transport' in issuer:
        strategic_score = 10
        strategic_rationale = "Transport sector - core relationship"
    else:
        strategic_score = 4
        strategic_rationale = "Limited strategic alignment"

    result['dimensions']['strategic_value'] = {
        'score': strategic_score,
        'max': 15,
        'rationale': strategic_rationale,
    }

    # Competitive Position (10 points max)
    competitive_score = 6
    competitive_rationale = "Open competition - no known advantage"

    if 'request for information' in tender_type:
        competitive_score = 8
        competitive_rationale = "RFI - early stage, lower barriers"
    elif 'expression of interest' in tender_type:
        competitive_score = 7
        competitive_rationale = "EOI - moderate competition expected"

    result['dimensions']['competitive_position'] = {
        'score': competitive_score,
        'max': 10,
        'rationale': competitive_rationale,
    }

    # Calculate total
    result['total_score'] = sum(d['score'] for d in result['dimensions'].values())
    result['threshold_met'] = result['total_score'] >= 80

    if result['total_score'] >= 80:
        result['decision'] = 'SHORTLIST'
    elif result['total_score'] >= 60:
        result['decision'] = 'REVIEW'
    else:
        result['decision'] = 'DECLINE'

    return result


def analyze_tender(tender: dict, scoring: dict) -> dict:
    """
    Generate synthesized analysis for a tender.
    """
    analysis = {
        'fit_summary': '',
        'key_strengths': [],
        'key_risks': [],
        'recommended_action': '',
        'days_until_closing': None,
        'urgency': 'LOW',
    }

    # Calculate days until closing
    closing_str = tender.get('date_closing', '')
    try:
        # Parse format like "Wed, 11 March 2026 2:00 pm"
        closing = datetime.strptime(closing_str, "%a, %d %B %Y %I:%M %p")
        days = (closing - datetime.now()).days
        analysis['days_until_closing'] = days

        if days <= 3:
            analysis['urgency'] = 'CRITICAL'
        elif days <= 7:
            analysis['urgency'] = 'HIGH'
        elif days <= 14:
            analysis['urgency'] = 'MEDIUM'
        else:
            analysis['urgency'] = 'LOW'
    except ValueError:
        pass

    # Build fit summary
    decision = scoring.get('decision', 'DECLINE')
    score = scoring.get('total_score', 0)

    if decision == 'SHORTLIST':
        analysis['fit_summary'] = f"Strong alignment ({score}/100) with marcov's core capabilities"
        analysis['recommended_action'] = "Pursue - download documents and prepare response"
    elif decision == 'REVIEW':
        analysis['fit_summary'] = f"Moderate alignment ({score}/100) - warrants manual review"
        analysis['recommended_action'] = "Review tender documents to confirm fit"
    elif decision == 'AUTO-DECLINE':
        analysis['fit_summary'] = f"Auto-declined: {scoring.get('auto_decline_reason', 'Outside scope')}"
        analysis['recommended_action'] = "No action required"
    else:
        analysis['fit_summary'] = f"Low alignment ({score}/100) - does not meet threshold"
        analysis['recommended_action'] = "No action required"

    # Extract strengths from high-scoring dimensions
    dimensions = scoring.get('dimensions', {})
    for dim_name, dim_data in dimensions.items():
        if dim_data.get('score', 0) >= dim_data.get('max', 100) * 0.8:
            analysis['key_strengths'].append(dim_data.get('rationale', dim_name))

    # Identify risks
    if analysis['days_until_closing'] and analysis['days_until_closing'] < 14:
        analysis['key_risks'].append(f"Short timeline - {analysis['days_until_closing']} days to closing")

    for dim_name, dim_data in dimensions.items():
        if dim_data.get('score', 0) <= dim_data.get('max', 100) * 0.3:
            if dim_name == 'competitive_position':
                analysis['key_risks'].append("Competitive position unclear")

    return analysis


def generate_shortlist_details(tender: dict, scoring: dict) -> dict:
    """
    Generate extended details for shortlisted tenders.
    """
    title = tender.get('title', '').lower()
    issuer = tender.get('issuer', '').lower()

    details = {
        'tender_id': tender.get('id', ''),
        'pursuit_recommendation': {
            'decision': 'PURSUE',
            'win_probability': 'MEDIUM',
            'estimated_effort_hours': 20,
            'strategic_importance': 'MEDIUM',
        },
        'competitive_positioning': {
            'differentiators': [],
            'win_themes': [],
            'likely_competitors': [],
        },
        'next_steps': [],
    }

    # Determine strategic importance
    if any(x in issuer for x in TIER1_CLIENTS):
        details['pursuit_recommendation']['strategic_importance'] = 'HIGH'

    # Set differentiators based on domain
    if 'asset management' in title or 'iso 55001' in title:
        details['competitive_positioning']['differentiators'] = [
            "Deep ISO 55001 and GFMAM expertise",
            "Practitioner-led consulting approach",
            "Proven track record in Victorian public sector",
        ]
        details['competitive_positioning']['win_themes'] = [
            "Standards-based, best practice approach",
            "Practical implementation focus",
        ]
    elif 'reliability' in title or 'rcm' in title or 'maintenance' in title:
        details['competitive_positioning']['differentiators'] = [
            "Reliability engineering specialists",
            "RCM and FMEA expertise",
            "Data-driven maintenance optimisation",
        ]
        details['competitive_positioning']['win_themes'] = [
            "Evidence-based maintenance strategy",
            "Measurable reliability improvements",
        ]
    elif 'analytics' in title or 'predictive' in title or 'data' in title:
        details['competitive_positioning']['differentiators'] = [
            "Advanced analytics and ML capability",
            "Edge/sovereign AI deployment (AMiPU)",
            "Asset data quality expertise",
        ]
        details['competitive_positioning']['win_themes'] = [
            "Actionable insights from asset data",
            "Secure, on-premise analytics options",
        ]

    # Next steps
    details['next_steps'] = [
        f"Download tender documents from {tender.get('url', '')}",
        "Review full scope and mandatory requirements",
        "Confirm team availability for response period",
        "Prepare clarification questions if needed",
    ]

    return details


def calculate_statistics(tenders: list, assessments: list) -> dict:
    """
    Calculate aggregate statistics across all assessed tenders.
    """
    stats = {
        'by_issuer': defaultdict(int),
        'by_tender_type': defaultdict(int),
        'by_decision': {
            'SHORTLIST': 0,
            'REVIEW': 0,
            'DECLINE': 0,
            'AUTO-DECLINE': 0,
        },
        'auto_decline_reasons': defaultdict(int),
        'average_score': 0,
        'score_distribution': {
            '0-19': 0,
            '20-39': 0,
            '40-59': 0,
            '60-79': 0,
            '80-100': 0,
        },
    }

    scores = []

    for tender, assessment in zip(tenders, assessments):
        # By issuer
        issuer = tender.get('issuer', 'Unknown')
        stats['by_issuer'][issuer] += 1

        # By tender type
        tender_type = tender.get('tender_type', 'Unknown')
        stats['by_tender_type'][tender_type] += 1

        # By decision
        decision = assessment['scoring'].get('decision', 'DECLINE')
        stats['by_decision'][decision] += 1

        # Auto-decline reasons
        if decision == 'AUTO-DECLINE':
            reason = assessment['scoring'].get('auto_decline_reason', 'Unknown')
            # Extract the pattern from the reason
            if "'" in reason:
                pattern = reason.split("'")[1]
                stats['auto_decline_reasons'][pattern] += 1

        # Scores (only for non-auto-declined)
        if decision != 'AUTO-DECLINE':
            score = assessment['scoring'].get('total_score', 0)
            scores.append(score)

            if score < 20:
                stats['score_distribution']['0-19'] += 1
            elif score < 40:
                stats['score_distribution']['20-39'] += 1
            elif score < 60:
                stats['score_distribution']['40-59'] += 1
            elif score < 80:
                stats['score_distribution']['60-79'] += 1
            else:
                stats['score_distribution']['80-100'] += 1

    # Average score
    if scores:
        stats['average_score'] = round(sum(scores) / len(scores), 1)

    # Convert defaultdicts to regular dicts
    stats['by_issuer'] = dict(stats['by_issuer'])
    stats['by_tender_type'] = dict(stats['by_tender_type'])
    stats['auto_decline_reasons'] = dict(stats['auto_decline_reasons'])

    return stats


# ── Main Assessment Function ──────────────────────────────────────────────────

def run_assessment(
    opened_today: bool = False,
    date_from: str = None,
    date_to: str = None,
    use_keywords: bool = True,
) -> dict:
    """
    Run full tender assessment and return comprehensive JSON output.
    """
    log.info("Starting tender assessment...")

    # Determine date filtering
    if opened_today:
        today = datetime.now().strftime("%d/%m/%Y")
        date_from = today
        date_to = today

    # Scrape tenders
    log.info("Scraping tenders...")
    tenders = scrape_all_tenders(delay=1.0, date_from=date_from, date_to=date_to)
    total_scraped = len(tenders)
    log.info(f"Scraped {total_scraped} tenders")

    # Apply keyword filter
    if use_keywords:
        tenders = filter_by_keywords(tenders, MARCOV_KEYWORDS)
        log.info(f"After keyword filter: {len(tenders)} tenders")

    # Assess each tender
    log.info("Scoring tenders...")
    assessments = []
    shortlist_details = []

    for tender in tenders:
        # Score
        scoring = score_tender(tender)

        # Analyze
        analysis = analyze_tender(tender, scoring)

        assessment = {
            'raw': tender,
            'scoring': scoring,
            'analysis': analysis,
        }
        assessments.append(assessment)

        # Generate extended details for shortlisted
        if scoring['decision'] == 'SHORTLIST':
            details = generate_shortlist_details(tender, scoring)
            shortlist_details.append(details)

    # Calculate statistics
    stats = calculate_statistics(tenders, assessments)

    # Build summary
    summary = {
        'total_scraped': total_scraped,
        'total_after_keyword_filter': len(tenders),
        'shortlisted': stats['by_decision']['SHORTLIST'],
        'flagged_for_review': stats['by_decision']['REVIEW'],
        'auto_declined': stats['by_decision']['AUTO-DECLINE'],
        'recommendation': '',
    }

    if summary['shortlisted'] > 0:
        summary['recommendation'] = f"ACTION REQUIRED: {summary['shortlisted']} tender(s) shortlisted for pursuit"
    elif summary['flagged_for_review'] > 0:
        summary['recommendation'] = f"REVIEW: {summary['flagged_for_review']} tender(s) flagged for manual review"
    else:
        summary['recommendation'] = "No action required - no aligned opportunities found"

    # Build output
    output = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'source': 'tenders.vic.gov.au',
            'date_range': {
                'from': date_from,
                'to': date_to,
            },
            'filters_applied': {
                'keywords': MARCOV_KEYWORDS if use_keywords else [],
                'opened_today': opened_today,
                'tender_state': 'OPEN',
            },
            'scoring_version': SCORING_VERSION,
        },
        'summary': summary,
        'tenders': assessments,
        'shortlist_details': shortlist_details,
        'statistics': stats,
    }

    log.info(f"Assessment complete. Shortlisted: {summary['shortlisted']}, Review: {summary['flagged_for_review']}")

    return output


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Comprehensive tender assessment with JSON output"
    )
    parser.add_argument("--output", "-o", help="Write JSON output to file")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    parser.add_argument("--opened-today", action="store_true", help="Only today's tenders")
    parser.add_argument("--opened-from", metavar="DD/MM/YYYY", help="Opening date from")
    parser.add_argument("--opened-to", metavar="DD/MM/YYYY", help="Opening date to")
    parser.add_argument("--no-keywords", action="store_true", help="Skip keyword filtering")

    args = parser.parse_args()

    # Run assessment
    result = run_assessment(
        opened_today=args.opened_today,
        date_from=args.opened_from,
        date_to=args.opened_to,
        use_keywords=not args.no_keywords,
    )

    # Output
    indent = 2 if args.pretty else None
    output_json = json.dumps(result, indent=indent, ensure_ascii=False, default=str)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output_json)
        log.info(f"Output written to {args.output}")
    else:
        print(output_json)

    return 0


if __name__ == "__main__":
    exit(main())
