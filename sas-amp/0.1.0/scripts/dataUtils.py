#!/usr/bin/env python3
"""
Data utilities for Asset Management Plan development.

Provides functions for data cleaning, LCC calculations, NPV analysis,
renewal forecasting, and condition-based modelling.

Usage:
    python3 dataUtils.py clean --input data.csv --output cleaned.csv
    python3 dataUtils.py profile --input cleaned.csv
    python3 dataUtils.py lcc --input cleaned.csv --discount-rate 0.04 --horizon 10
    python3 dataUtils.py quality --input data.csv
"""

import argparse
import json
import os
import sys

try:
    import pandas as pd
    import numpy as np
except ImportError:
    print("ERROR: pandas/numpy not installed. Run: pip3 install pandas numpy")
    sys.exit(1)


# --- Data Cleaning ---

def clean_data(df, verbose=True):
    """Clean and normalise an asset dataset."""
    report = {
        'original_rows': len(df),
        'original_cols': len(df.columns),
        'actions': []
    }

    # Standardise column names
    col_mapping = {}
    for col in df.columns:
        lower = col.lower().strip().replace(' ', '_').replace('-', '_')
        # Common mappings
        mappings = {
            'asset_id': ['assetid', 'asset_no', 'asset_number', 'id', 'asset_code'],
            'asset_name': ['assetname', 'name', 'description', 'asset_description'],
            'asset_class': ['assetclass', 'class', 'category', 'asset_category', 'asset_type'],
            'asset_subclass': ['assetsubclass', 'subclass', 'sub_class', 'sub_category'],
            'install_date': ['installdate', 'installation_date', 'date_installed', 'constructed',
                             'construction_date', 'commission_date', 'commissioned'],
            'useful_life_years': ['usefullife', 'useful_life', 'expected_life', 'design_life',
                                  'economic_life', 'total_useful_life'],
            'remaining_life_years': ['remaininglife', 'remaining_life', 'remaining_useful_life',
                                     'years_remaining'],
            'condition_score': ['condition', 'condition_grade', 'condition_rating',
                                'cond_score', 'cond_grade', 'overall_condition'],
            'replacement_value': ['replacementvalue', 'replacement_cost', 'current_replacement_cost',
                                  'crc', 'gross_replacement_cost', 'grc'],
            'depreciated_value': ['depreciatedvalue', 'written_down_value', 'wdv',
                                  'fair_value', 'net_book_value', 'nbv'],
            'criticality_score': ['criticality', 'risk_score', 'criticality_rating'],
            'maintenance_annual_cost': ['maintenance_cost', 'annual_maintenance',
                                        'opex', 'annual_opex'],
            'location': ['loc', 'site', 'facility', 'area'],
        }

        matched = False
        for standard_name, aliases in mappings.items():
            if lower == standard_name or lower in aliases:
                col_mapping[col] = standard_name
                matched = True
                break
        if not matched:
            col_mapping[col] = lower

    df = df.rename(columns=col_mapping)
    if col_mapping:
        report['actions'].append(f"Renamed {sum(1 for k, v in col_mapping.items() if k != v)} columns")

    # Remove duplicate rows
    before = len(df)
    df = df.drop_duplicates()
    removed = before - len(df)
    if removed:
        report['actions'].append(f"Removed {removed} duplicate rows")

    # Parse dates
    if 'install_date' in df.columns:
        df['install_date'] = pd.to_datetime(df['install_date'], errors='coerce', dayfirst=True)
        report['actions'].append("Parsed install_date to datetime")

    # Calculate age if not present
    if 'install_date' in df.columns and 'age_years' not in df.columns:
        df['age_years'] = (pd.Timestamp.now() - df['install_date']).dt.days / 365.25
        df['age_years'] = df['age_years'].round(1)
        report['actions'].append("Calculated age_years from install_date")

    # Calculate remaining life if not present
    if 'age_years' in df.columns and 'useful_life_years' in df.columns and 'remaining_life_years' not in df.columns:
        df['remaining_life_years'] = (df['useful_life_years'] - df['age_years']).round(1)
        report['actions'].append("Calculated remaining_life_years")

    # Ensure numeric columns are numeric
    numeric_cols = ['useful_life_years', 'remaining_life_years', 'condition_score',
                    'replacement_value', 'depreciated_value', 'criticality_score',
                    'maintenance_annual_cost', 'age_years']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    report['final_rows'] = len(df)
    report['final_cols'] = len(df.columns)

    if verbose:
        print("=== Data Cleaning Report ===")
        print(f"Rows: {report['original_rows']} -> {report['final_rows']}")
        print(f"Columns: {report['original_cols']} -> {report['final_cols']}")
        for action in report['actions']:
            print(f"  - {action}")

    return df, report


# --- Asset Profiling ---

def profile_assets(df):
    """Generate an asset portfolio profile summary."""
    profile = {'total_assets': len(df)}

    # Value summary
    if 'replacement_value' in df.columns:
        rv = df['replacement_value'].dropna()
        profile['total_replacement_value'] = float(rv.sum())
        profile['avg_replacement_value'] = float(rv.mean())

    if 'depreciated_value' in df.columns:
        wdv = df['depreciated_value'].dropna()
        profile['total_depreciated_value'] = float(wdv.sum())
        if 'replacement_value' in df.columns:
            profile['consumption_ratio'] = round(
                (1 - wdv.sum() / max(df['replacement_value'].sum(), 1)) * 100, 1
            )

    # Age summary
    if 'age_years' in df.columns:
        ages = df['age_years'].dropna()
        profile['avg_age'] = round(float(ages.mean()), 1)
        profile['max_age'] = round(float(ages.max()), 1)
        profile['median_age'] = round(float(ages.median()), 1)

    if 'remaining_life_years' in df.columns:
        rl = df['remaining_life_years'].dropna()
        profile['avg_remaining_life'] = round(float(rl.mean()), 1)
        profile['assets_past_useful_life'] = int((rl <= 0).sum())
        profile['pct_past_useful_life'] = round((rl <= 0).sum() / max(len(rl), 1) * 100, 1)

    # Condition summary
    cond_col = next((c for c in ['condition_score', 'condition', 'condition_grade'] if c in df.columns), None)
    if cond_col:
        cond = df[cond_col].dropna()
        profile['condition_distribution'] = {str(k): int(v) for k, v in cond.value_counts().sort_index().items()}
        profile['avg_condition'] = round(float(cond.mean()), 1)

    # Class breakdown
    class_col = next((c for c in ['asset_class', 'asset_type', 'category'] if c in df.columns), None)
    if class_col:
        class_summary = df.groupby(class_col).agg(
            count=('asset_class' if 'asset_class' in df.columns else class_col, 'count'),
            **({'total_rv': ('replacement_value', 'sum')} if 'replacement_value' in df.columns else {}),
            **({'avg_age': ('age_years', 'mean')} if 'age_years' in df.columns else {}),
        ).round(1)
        profile['class_breakdown'] = class_summary.to_dict('index')

    return profile


# --- Financial Analysis ---

def npv(cashflows, discount_rate=0.04):
    """Calculate Net Present Value of annual cashflows."""
    return sum(cf / (1 + discount_rate) ** year for year, cf in enumerate(cashflows))


def present_value(future_value, years, discount_rate=0.04):
    """Calculate present value of a single future amount."""
    return future_value / (1 + discount_rate) ** years


def annual_depreciation(replacement_value, useful_life, residual_value=0):
    """Calculate annual straight-line depreciation."""
    if useful_life <= 0:
        return 0
    return (replacement_value - residual_value) / useful_life


def renewal_forecast(df, planning_horizon=10, discount_rate=0.04):
    """Generate year-by-year renewal forecast based on remaining life."""
    forecast = {yr: 0.0 for yr in range(1, planning_horizon + 1)}
    backlog = 0.0

    for _, row in df.iterrows():
        remaining = row.get('remaining_life_years', None)
        value = row.get('replacement_value', 0)

        if pd.isna(remaining) or pd.isna(value):
            continue

        if remaining <= 0:
            backlog += value
            forecast[1] += value
        elif remaining <= planning_horizon:
            year = max(1, int(round(remaining)))
            if year <= planning_horizon:
                forecast[year] += value

    cashflows = [forecast.get(y, 0) for y in range(1, planning_horizon + 1)]
    total_npv = npv(cashflows, discount_rate)
    total_nominal = sum(cashflows)
    annual_avg = total_nominal / planning_horizon

    return {
        'forecast': forecast,
        'total_nominal': total_nominal,
        'total_npv': total_npv,
        'annual_average': annual_avg,
        'backlog': backlog,
        'discount_rate': discount_rate,
        'planning_horizon': planning_horizon,
    }


def funding_gap_analysis(required, available):
    """Calculate annual and cumulative funding gap.

    Args:
        required: dict of {year: amount} for required expenditure
        available: dict of {year: amount} for available funding
    """
    results = {}
    cumulative = 0

    for year in sorted(required.keys()):
        req = required[year]
        avail = available.get(year, 0)
        gap = req - avail
        cumulative += gap

        results[year] = {
            'required': req,
            'available': avail,
            'annual_gap': gap,
            'cumulative_gap': cumulative,
            'sustainability_ratio': round(avail / max(req, 1) * 100, 1),
        }

    return results


# --- Data Quality Assessment ---

def assess_data_quality(df):
    """Assess data quality across key dimensions."""
    quality = {}

    # Completeness
    completeness = {}
    for col in df.columns:
        non_null = df[col].notna().sum()
        completeness[col] = round(non_null / max(len(df), 1) * 100, 1)
    avg_completeness = sum(completeness.values()) / max(len(completeness), 1)

    quality['completeness'] = {
        'by_column': completeness,
        'average': round(avg_completeness, 1),
        'rating': 'High' if avg_completeness > 90 else 'Medium' if avg_completeness > 70 else 'Low',
    }

    # Timeliness
    if 'condition_date' in df.columns:
        dates = pd.to_datetime(df['condition_date'], errors='coerce').dropna()
        if not dates.empty:
            avg_age_days = (pd.Timestamp.now() - dates).dt.days.mean()
            avg_age_years = avg_age_days / 365.25
            quality['timeliness'] = {
                'avg_data_age_years': round(avg_age_years, 1),
                'rating': 'High' if avg_age_years < 2 else 'Medium' if avg_age_years < 5 else 'Low',
            }

    # Consistency
    issues = []
    for col in df.select_dtypes(include=['object']).columns:
        unique = df[col].nunique()
        if unique > 0.5 * len(df) and unique > 20:
            issues.append(f"{col}: high cardinality ({unique} unique values)")

    quality['consistency'] = {
        'issues': issues,
        'rating': 'High' if len(issues) == 0 else 'Medium' if len(issues) < 3 else 'Low',
    }

    # Overall
    ratings = [v.get('rating', 'Medium') for v in quality.values() if isinstance(v, dict)]
    if 'Low' in ratings:
        quality['overall'] = 'Low'
    elif 'Medium' in ratings:
        quality['overall'] = 'Medium'
    else:
        quality['overall'] = 'High'

    return quality


# --- CLI ---

def main():
    parser = argparse.ArgumentParser(description='AMP Data Utilities')
    subparsers = parser.add_subparsers(dest='command')

    # Clean command
    clean_parser = subparsers.add_parser('clean', help='Clean and normalise data')
    clean_parser.add_argument('--input', required=True, help='Input CSV/Excel file')
    clean_parser.add_argument('--output', required=True, help='Output cleaned CSV file')

    # Profile command
    profile_parser = subparsers.add_parser('profile', help='Generate asset profile')
    profile_parser.add_argument('--input', required=True, help='Input CSV file')
    profile_parser.add_argument('--output', default=None, help='Output JSON file (optional)')

    # LCC command
    lcc_parser = subparsers.add_parser('lcc', help='Lifecycle cost analysis')
    lcc_parser.add_argument('--input', required=True, help='Input CSV file')
    lcc_parser.add_argument('--discount-rate', type=float, default=0.04, help='Discount rate (default: 0.04)')
    lcc_parser.add_argument('--horizon', type=int, default=10, help='Planning horizon in years (default: 10)')
    lcc_parser.add_argument('--output', default=None, help='Output JSON file (optional)')

    # Quality command
    quality_parser = subparsers.add_parser('quality', help='Assess data quality')
    quality_parser.add_argument('--input', required=True, help='Input CSV/Excel file')
    quality_parser.add_argument('--output', default=None, help='Output JSON file (optional)')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Load data
    input_file = args.input
    if input_file.endswith('.xlsx') or input_file.endswith('.xls'):
        df = pd.read_excel(input_file)
    else:
        df = pd.read_csv(input_file)
    print(f"Loaded: {len(df)} rows from {input_file}")

    if args.command == 'clean':
        cleaned_df, report = clean_data(df)
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        cleaned_df.to_csv(args.output, index=False)
        print(f"Saved cleaned data: {args.output}")

    elif args.command == 'profile':
        cleaned_df, _ = clean_data(df, verbose=False)
        profile = profile_assets(cleaned_df)
        output = json.dumps(profile, indent=2, default=str)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"Saved profile: {args.output}")
        else:
            print(output)

    elif args.command == 'lcc':
        cleaned_df, _ = clean_data(df, verbose=False)
        result = renewal_forecast(cleaned_df, args.horizon, args.discount_rate)
        output = json.dumps(result, indent=2, default=str)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"Saved LCC analysis: {args.output}")
        else:
            print(output)

    elif args.command == 'quality':
        assessment = assess_data_quality(df)
        output = json.dumps(assessment, indent=2, default=str)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"Saved quality assessment: {args.output}")
        else:
            print(output)


if __name__ == '__main__':
    main()
