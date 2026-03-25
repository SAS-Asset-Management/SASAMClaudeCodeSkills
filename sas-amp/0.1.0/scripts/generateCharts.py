#!/usr/bin/env python3
"""
Generate SAS-AM branded charts for Asset Management Plan documents.

Usage:
    python3 generateCharts.py \
        --data-file ./sas-amp-working/data/cleaned/assets.csv \
        --output-dir ./sas-amp-working/data/charts/ \
        --chart-type all|age-profile|condition|renewal|funding-gap|value-trajectory|expenditure|criticality
"""

import argparse
import json
import os
import sys

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker
    import numpy as np
except ImportError:
    print("ERROR: matplotlib/numpy not installed. Run: pip3 install matplotlib numpy")
    sys.exit(1)

try:
    import pandas as pd
except ImportError:
    print("ERROR: pandas not installed. Run: pip3 install pandas")
    sys.exit(1)

# SAS-AM Brand
BRAND = {
    'sas_blue': '#002244',
    'sas_green': '#69BE28',
    'palette': ['#69BE28', '#002244', '#3B82F6', '#F59E0B', '#EF4444', '#8B5CF6'],
    'rag_green': '#69BE28',
    'rag_amber': '#F59E0B',
    'rag_red': '#EF4444',
    'background': '#ffffff',
    'text': '#002244',
    'grid': '#ededed',
    'font': 'sans-serif',
}

DPI = 200
FIG_SIZE = (10, 6)


def apply_style(fig, ax):
    """Apply SAS-AM branding to a matplotlib figure."""
    ax.set_facecolor(BRAND['background'])
    fig.set_facecolor(BRAND['background'])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(BRAND['grid'])
    ax.spines['bottom'].set_color(BRAND['grid'])
    ax.tick_params(colors=BRAND['text'], labelsize=9)
    ax.yaxis.grid(True, color=BRAND['grid'], linewidth=0.5, alpha=0.7)
    ax.set_axisbelow(True)
    ax.title.set_color(BRAND['text'])
    ax.xaxis.label.set_color(BRAND['text'])
    ax.yaxis.label.set_color(BRAND['text'])
    return fig, ax


def format_currency(x, pos):
    """Format axis values as currency ($M)."""
    if x >= 1_000_000:
        return f'${x / 1_000_000:.1f}M'
    elif x >= 1_000:
        return f'${x / 1_000:.0f}K'
    return f'${x:.0f}'


def chart_age_profile(df, output_dir):
    """Generate asset age profile histogram."""
    if 'install_date' not in df.columns and 'age_years' not in df.columns:
        print("SKIP: age-profile — no install_date or age_years column")
        return

    if 'age_years' not in df.columns:
        df['install_date'] = pd.to_datetime(df['install_date'], errors='coerce')
        df['age_years'] = (pd.Timestamp.now() - df['install_date']).dt.days / 365.25

    ages = df['age_years'].dropna()
    if ages.empty:
        return

    fig, ax = plt.subplots(figsize=FIG_SIZE)
    apply_style(fig, ax)

    max_age = min(int(ages.max()) + 5, 100)
    bins = range(0, max_age + 5, 5)
    ax.hist(ages, bins=bins, color=BRAND['sas_blue'], edgecolor='white', linewidth=0.5, alpha=0.9)

    if 'useful_life_years' in df.columns:
        avg_life = df['useful_life_years'].dropna().mean()
        ax.axvline(x=avg_life, color=BRAND['sas_green'], linestyle='--', linewidth=2,
                    label=f'Avg useful life ({avg_life:.0f} yrs)')
        ax.legend(loc='upper right', frameon=False)

    ax.set_xlabel('Asset Age (years)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Number of Assets', fontsize=11, fontweight='bold')
    ax.set_title('Asset Age Profile', fontsize=14, fontweight='bold', pad=15)

    plt.tight_layout()
    path = os.path.join(output_dir, 'age-profile.png')
    fig.savefig(path, dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print(f"Generated: {path}")


def chart_condition_distribution(df, output_dir):
    """Generate condition distribution bar chart."""
    col = None
    for candidate in ['condition_score', 'condition', 'condition_grade', 'cond_score']:
        if candidate in df.columns:
            col = candidate
            break

    if col is None:
        print("SKIP: condition-distribution — no condition column found")
        return

    conditions = df[col].dropna()
    counts = conditions.value_counts().sort_index()

    fig, ax = plt.subplots(figsize=FIG_SIZE)
    apply_style(fig, ax)

    grade_colours = {1: '#69BE28', 2: '#A3D977', 3: '#F59E0B', 4: '#EF8C44', 5: '#EF4444'}
    colours = [grade_colours.get(int(g), BRAND['sas_blue']) for g in counts.index]

    bars = ax.barh(counts.index.astype(str), counts.values, color=colours, edgecolor='white', height=0.6)

    for bar, val in zip(bars, counts.values):
        ax.text(bar.get_width() + max(counts.values) * 0.02, bar.get_y() + bar.get_height() / 2,
                f'{val}', ha='left', va='center', fontsize=10, color=BRAND['text'])

    grade_labels = {1: 'Very Good', 2: 'Good', 3: 'Fair', 4: 'Poor', 5: 'Very Poor'}
    ax.set_yticklabels([f'{g} — {grade_labels.get(int(g), "")}' for g in counts.index])

    ax.set_xlabel('Number of Assets', fontsize=11, fontweight='bold')
    ax.set_title('Asset Condition Distribution', fontsize=14, fontweight='bold', pad=15)
    ax.invert_yaxis()

    plt.tight_layout()
    path = os.path.join(output_dir, 'condition-distribution.png')
    fig.savefig(path, dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print(f"Generated: {path}")


def chart_renewal_forecast(df, output_dir, planning_horizon=10, discount_rate=0.04):
    """Generate renewal forecast bar chart."""
    if 'remaining_life_years' not in df.columns or 'replacement_value' not in df.columns:
        print("SKIP: renewal-forecast — need remaining_life_years and replacement_value columns")
        return

    forecast = {yr: 0 for yr in range(1, planning_horizon + 1)}
    for _, row in df.iterrows():
        remaining = row.get('remaining_life_years', None)
        value = row.get('replacement_value', 0)
        if pd.isna(remaining) or pd.isna(value):
            continue
        if remaining <= 0:
            forecast[1] += value
        elif remaining <= planning_horizon:
            year = max(1, int(round(remaining)))
            forecast[year] += value

    years = list(range(1, planning_horizon + 1))
    values = [forecast[y] for y in years]

    fig, ax = plt.subplots(figsize=FIG_SIZE)
    apply_style(fig, ax)

    ax.bar(years, values, color=BRAND['sas_blue'], edgecolor='white', width=0.7)

    avg = sum(values) / len(values)
    ax.axhline(y=avg, color=BRAND['sas_green'], linestyle='--', linewidth=2,
               label=f'Average (${avg:,.0f}/yr)')
    ax.legend(loc='upper right', frameon=False)

    ax.set_xlabel('Year', fontsize=11, fontweight='bold')
    ax.set_ylabel('Renewal Expenditure ($)', fontsize=11, fontweight='bold')
    ax.set_title('10-Year Renewal Forecast', fontsize=14, fontweight='bold', pad=15)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_currency))
    ax.set_xticks(years)

    plt.tight_layout()
    path = os.path.join(output_dir, 'renewal-forecast.png')
    fig.savefig(path, dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print(f"Generated: {path}")


def chart_expenditure_breakdown(df, output_dir):
    """Generate expenditure breakdown pie chart."""
    # Try to find expenditure columns
    exp_cols = {}
    for col in df.columns:
        lower = col.lower()
        if 'operat' in lower:
            exp_cols['Operations'] = col
        elif 'maint' in lower:
            exp_cols['Maintenance'] = col
        elif 'renew' in lower or 'replac' in lower:
            exp_cols['Renewal'] = col
        elif 'upgrad' in lower or 'capital' in lower or 'capex' in lower:
            exp_cols['Upgrade/New'] = col

    if not exp_cols:
        print("SKIP: expenditure-breakdown — no expenditure columns found")
        return

    totals = {name: df[col].sum() for name, col in exp_cols.items() if df[col].dtype in ['float64', 'int64']}

    if not totals:
        return

    fig, ax = plt.subplots(figsize=(8, 8))
    fig.set_facecolor(BRAND['background'])

    colours = BRAND['palette'][:len(totals)]
    wedges, texts, autotexts = ax.pie(
        totals.values(), labels=totals.keys(), autopct='%1.1f%%',
        colors=colours, startangle=90, textprops={'fontsize': 11, 'color': BRAND['text']},
        pctdistance=0.75, wedgeprops={'edgecolor': 'white', 'linewidth': 2}
    )
    for autotext in autotexts:
        autotext.set_fontweight('bold')

    ax.set_title('Expenditure Breakdown', fontsize=14, fontweight='bold',
                 color=BRAND['text'], pad=20)

    plt.tight_layout()
    path = os.path.join(output_dir, 'expenditure-breakdown.png')
    fig.savefig(path, dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print(f"Generated: {path}")


def chart_value_trajectory(df, output_dir, planning_horizon=10):
    """Generate asset value trajectory chart."""
    if 'replacement_value' not in df.columns or 'useful_life_years' not in df.columns:
        print("SKIP: value-trajectory — need replacement_value and useful_life_years columns")
        return

    total_rv = df['replacement_value'].sum()
    if 'depreciated_value' in df.columns:
        current_wdv = df['depreciated_value'].sum()
    elif 'age_years' in df.columns:
        df['_wdv'] = df.apply(
            lambda r: max(0, r['replacement_value'] * (1 - min(r['age_years'] / max(r['useful_life_years'], 1), 1)))
            if pd.notna(r['age_years']) and pd.notna(r['useful_life_years']) else r['replacement_value'],
            axis=1
        )
        current_wdv = df['_wdv'].sum()
    else:
        print("SKIP: value-trajectory — insufficient data for depreciation calculation")
        return

    avg_life = df['useful_life_years'].mean()
    annual_dep = total_rv / avg_life if avg_life > 0 else 0

    years = list(range(0, planning_horizon + 1))
    rv_line = [total_rv] * len(years)
    wdv_line = [max(0, current_wdv - annual_dep * y) for y in years]

    fig, ax = plt.subplots(figsize=FIG_SIZE)
    apply_style(fig, ax)

    ax.plot(years, rv_line, color=BRAND['sas_blue'], linewidth=2.5, label='Replacement Value')
    ax.plot(years, wdv_line, color=BRAND['sas_green'], linewidth=2.5, linestyle='--', label='Written Down Value')
    ax.fill_between(years, wdv_line, alpha=0.1, color=BRAND['sas_green'])

    ax.set_xlabel('Year', fontsize=11, fontweight='bold')
    ax.set_ylabel('Value ($)', fontsize=11, fontweight='bold')
    ax.set_title('Asset Value Trajectory', fontsize=14, fontweight='bold', pad=15)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_currency))
    ax.legend(loc='upper right', frameon=False)

    plt.tight_layout()
    path = os.path.join(output_dir, 'value-trajectory.png')
    fig.savefig(path, dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print(f"Generated: {path}")


def chart_funding_gap(df, output_dir, planning_horizon=10):
    """Generate funding gap analysis chart."""
    # Requires pre-calculated funding data — typically passed as separate columns
    required_col = next((c for c in df.columns if 'required' in c.lower() or 'need' in c.lower()), None)
    available_col = next((c for c in df.columns if 'available' in c.lower() or 'budget' in c.lower() or 'funded' in c.lower()), None)

    if not required_col or not available_col:
        print("SKIP: funding-gap — need 'required' and 'available/budget' columns")
        return

    years = list(range(1, min(len(df), planning_horizon) + 1))
    required = df[required_col].values[:len(years)]
    available = df[available_col].values[:len(years)]
    gap = required - available

    fig, ax = plt.subplots(figsize=FIG_SIZE)
    apply_style(fig, ax)

    colours = [BRAND['rag_red'] if g > 0 else BRAND['rag_green'] for g in gap]
    ax.bar(years, gap, color=colours, edgecolor='white', width=0.7, alpha=0.8)

    cumulative = np.cumsum(gap)
    ax.plot(years, cumulative, color=BRAND['sas_blue'], linewidth=2.5, marker='o',
            markersize=5, label='Cumulative Gap')

    ax.axhline(y=0, color=BRAND['text'], linewidth=0.8, alpha=0.5)
    ax.legend(loc='upper left', frameon=False)

    ax.set_xlabel('Year', fontsize=11, fontweight='bold')
    ax.set_ylabel('Funding Gap ($)', fontsize=11, fontweight='bold')
    ax.set_title('Funding Gap Analysis', fontsize=14, fontweight='bold', pad=15)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_currency))
    ax.set_xticks(years)

    plt.tight_layout()
    path = os.path.join(output_dir, 'funding-gap.png')
    fig.savefig(path, dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print(f"Generated: {path}")


def chart_criticality_matrix(df, output_dir):
    """Generate criticality/risk matrix heatmap."""
    likelihood_col = next((c for c in df.columns if 'likelihood' in c.lower() or 'probability' in c.lower()), None)
    consequence_col = next((c for c in df.columns if 'consequence' in c.lower() or 'impact' in c.lower()), None)

    if not likelihood_col or not consequence_col:
        # Try to use a single criticality score as a distribution
        crit_col = next((c for c in ['criticality_score', 'criticality', 'risk_score'] if c in df.columns), None)
        if not crit_col:
            print("SKIP: criticality — need likelihood+consequence or criticality_score columns")
            return

        # Show criticality distribution as a simple bar chart
        counts = df[crit_col].dropna().value_counts().sort_index()
        fig, ax = plt.subplots(figsize=FIG_SIZE)
        apply_style(fig, ax)

        colours = [BRAND['rag_green'], '#A3D977', BRAND['rag_amber'], '#EF8C44', BRAND['rag_red']]
        bar_colours = colours[:len(counts)]
        ax.bar(counts.index.astype(str), counts.values, color=bar_colours, edgecolor='white', width=0.6)

        ax.set_xlabel('Criticality Score', fontsize=11, fontweight='bold')
        ax.set_ylabel('Number of Assets', fontsize=11, fontweight='bold')
        ax.set_title('Asset Criticality Distribution', fontsize=14, fontweight='bold', pad=15)

        plt.tight_layout()
        path = os.path.join(output_dir, 'criticality-distribution.png')
        fig.savefig(path, dpi=DPI, bbox_inches='tight')
        plt.close(fig)
        print(f"Generated: {path}")
        return

    # Build 5x5 risk matrix
    matrix = np.zeros((5, 5))
    for _, row in df.iterrows():
        l = int(row[likelihood_col]) if pd.notna(row[likelihood_col]) else 0
        c = int(row[consequence_col]) if pd.notna(row[consequence_col]) else 0
        if 1 <= l <= 5 and 1 <= c <= 5:
            matrix[c - 1][l - 1] += 1

    fig, ax = plt.subplots(figsize=(8, 7))
    fig.set_facecolor(BRAND['background'])

    from matplotlib.colors import LinearSegmentedColormap
    colours_map = ['#69BE28', '#A3D977', '#F59E0B', '#EF8C44', '#EF4444']
    cmap = LinearSegmentedColormap.from_list('risk', colours_map, N=256)

    im = ax.imshow(matrix, cmap=cmap, aspect='auto', origin='lower')

    for i in range(5):
        for j in range(5):
            val = int(matrix[i][j])
            if val > 0:
                ax.text(j, i, str(val), ha='center', va='center',
                        fontsize=14, fontweight='bold', color='white')

    ax.set_xticks(range(5))
    ax.set_yticks(range(5))
    ax.set_xticklabels(['1\nRare', '2\nUnlikely', '3\nPossible', '4\nLikely', '5\nAlmost\nCertain'],
                        fontsize=9, color=BRAND['text'])
    ax.set_yticklabels(['1\nInsignificant', '2\nMinor', '3\nModerate', '4\nMajor', '5\nCatastrophic'],
                        fontsize=9, color=BRAND['text'])

    ax.set_xlabel('Likelihood', fontsize=11, fontweight='bold', color=BRAND['text'])
    ax.set_ylabel('Consequence', fontsize=11, fontweight='bold', color=BRAND['text'])
    ax.set_title('Asset Criticality Matrix', fontsize=14, fontweight='bold',
                 color=BRAND['text'], pad=15)

    plt.colorbar(im, ax=ax, label='Asset Count', shrink=0.8)

    plt.tight_layout()
    path = os.path.join(output_dir, 'criticality-matrix.png')
    fig.savefig(path, dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print(f"Generated: {path}")


def generate_d3_specs(df, output_dir, planning_horizon=10):
    """Generate D3.js chart specifications as JSON for HTML presentation."""
    d3_dir = os.path.join(output_dir, 'd3')
    os.makedirs(d3_dir, exist_ok=True)

    # Age profile spec
    if 'age_years' in df.columns:
        ages = df['age_years'].dropna()
        hist, bin_edges = np.histogram(ages, bins=range(0, int(ages.max()) + 10, 5))
        spec = {
            'chart_type': 'histogram',
            'title': 'Asset Age Profile',
            'x_axis': {'label': 'Age (years)', 'bins': [int(b) for b in bin_edges]},
            'y_axis': {'label': 'Count'},
            'values': [int(v) for v in hist],
            'colour': BRAND['sas_blue']
        }
        with open(os.path.join(d3_dir, 'age-profile.json'), 'w') as f:
            json.dump(spec, f, indent=2)
        print(f"Generated D3 spec: {d3_dir}/age-profile.json")

    # Condition distribution spec
    cond_col = next((c for c in ['condition_score', 'condition', 'condition_grade'] if c in df.columns), None)
    if cond_col:
        counts = df[cond_col].dropna().value_counts().sort_index()
        spec = {
            'chart_type': 'horizontal_bar',
            'title': 'Asset Condition Distribution',
            'categories': [str(c) for c in counts.index],
            'values': [int(v) for v in counts.values],
            'colours': ['#69BE28', '#A3D977', '#F59E0B', '#EF8C44', '#EF4444'][:len(counts)]
        }
        with open(os.path.join(d3_dir, 'condition-distribution.json'), 'w') as f:
            json.dump(spec, f, indent=2)
        print(f"Generated D3 spec: {d3_dir}/condition-distribution.json")


def main():
    parser = argparse.ArgumentParser(description='Generate SAS-AM branded AMP charts')
    parser.add_argument('--data-file', required=True, help='Path to cleaned CSV data file')
    parser.add_argument('--output-dir', required=True, help='Directory to save chart images')
    parser.add_argument('--chart-type', default='all',
                        choices=['all', 'age-profile', 'condition', 'renewal', 'funding-gap',
                                 'value-trajectory', 'expenditure', 'criticality'],
                        help='Which chart(s) to generate')
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    # Load data
    print(f"Loading data from: {args.data_file}")
    if args.data_file.endswith('.xlsx') or args.data_file.endswith('.xls'):
        df = pd.read_excel(args.data_file)
    else:
        df = pd.read_csv(args.data_file)

    print(f"Loaded {len(df)} rows, {len(df.columns)} columns")
    print(f"Columns: {list(df.columns)}")

    chart_funcs = {
        'age-profile': chart_age_profile,
        'condition': chart_condition_distribution,
        'renewal': chart_renewal_forecast,
        'expenditure': chart_expenditure_breakdown,
        'value-trajectory': chart_value_trajectory,
        'funding-gap': chart_funding_gap,
        'criticality': chart_criticality_matrix,
    }

    if args.chart_type == 'all':
        for name, func in chart_funcs.items():
            try:
                func(df, args.output_dir)
            except Exception as e:
                print(f"ERROR generating {name}: {e}")

        try:
            generate_d3_specs(df, args.output_dir)
        except Exception as e:
            print(f"ERROR generating D3 specs: {e}")
    else:
        func = chart_funcs.get(args.chart_type)
        if func:
            func(df, args.output_dir)
        else:
            print(f"Chart type '{args.chart_type}' not yet implemented")


if __name__ == '__main__':
    main()
