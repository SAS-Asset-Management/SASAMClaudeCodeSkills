# Data Analysis Patterns for AMP Development

Reference guide for data analysis, lifecycle costing, and chart generation methodologies used in Asset Management Plans.

## Data Cleaning and Normalisation

### Common Data Issues

| Issue | Detection | Treatment |
|-------|-----------|-----------|
| Missing values | Count nulls per column | Impute (median for numeric, mode for categorical) or flag as unknown |
| Inconsistent naming | Value frequency analysis | Create lookup table; map to standard categories |
| Duplicate records | Group by asset ID; count | Keep most recent record; flag duplicates |
| Mixed units | Inspect numeric ranges | Normalise to standard units (e.g., km, $AUD, years) |
| Date format inconsistency | Parse with multiple formats | Standardise to YYYY-MM-DD |
| Outliers | Z-score or IQR method | Investigate; correct if error, retain if genuine |

### Standard Column Mappings

Normalise common column names to these standards:

```
asset_id, asset_name, asset_class, asset_subclass,
install_date, useful_life_years, remaining_life_years,
condition_score, condition_date, condition_method,
replacement_value, depreciated_value,
criticality_score, criticality_category,
location, latitude, longitude,
maintenance_annual_cost, last_maintenance_date
```

## Asset Profiling

### Age Distribution Analysis

```python
# Calculate asset ages
df['age_years'] = (pd.Timestamp.now() - pd.to_datetime(df['install_date'])).dt.days / 365.25
df['life_consumed_pct'] = (df['age_years'] / df['useful_life_years'] * 100).clip(0, 200)

# Age profile summary
age_stats = df.groupby('asset_class').agg(
    count=('asset_id', 'count'),
    avg_age=('age_years', 'mean'),
    max_age=('age_years', 'max'),
    avg_life_consumed=('life_consumed_pct', 'mean'),
    past_useful_life=('life_consumed_pct', lambda x: (x > 100).sum())
).round(1)
```

### Condition Distribution

Standard 1-5 condition scale (adapt to organisation's scale):

| Grade | Description | Intervention |
|-------|------------|--------------|
| 1 | Very Good — New or near-new | Routine maintenance only |
| 2 | Good — Minor deterioration | Planned maintenance |
| 3 | Fair — Moderate deterioration | Increased maintenance; plan renewal |
| 4 | Poor — Significant deterioration | Renewal required within 1-3 years |
| 5 | Very Poor — Failed or near-failure | Immediate renewal/replacement |

### Criticality Assessment

If no criticality data exists, derive from:
- **Consequence of failure** (safety, service, financial, environmental, reputation)
- **Likelihood of failure** (condition, age vs useful life, maintenance history)
- **Criticality score** = Consequence x Likelihood (risk-based approach)

## Financial Analysis

### Net Present Value (NPV)

```python
def npv(cashflows, discount_rate=0.04):
    """Calculate NPV of a series of annual cashflows."""
    return sum(cf / (1 + discount_rate) ** year
               for year, cf in enumerate(cashflows))

def present_value(future_value, years, discount_rate=0.04):
    """Calculate present value of a single future amount."""
    return future_value / (1 + discount_rate) ** years
```

### Straight-Line Depreciation

```python
def annual_depreciation(replacement_value, useful_life, residual_value=0):
    """Calculate annual straight-line depreciation."""
    return (replacement_value - residual_value) / useful_life

def written_down_value(replacement_value, age, useful_life, residual_value=0):
    """Calculate current written-down value."""
    consumed = min(age / useful_life, 1.0)
    return replacement_value - (replacement_value - residual_value) * consumed
```

### Renewal Forecasting

Age-based renewal forecast (simple approach):

```python
def renewal_forecast(df, planning_horizon=10, discount_rate=0.04):
    """Generate year-by-year renewal forecast based on remaining life."""
    forecast = {year: 0 for year in range(1, planning_horizon + 1)}

    for _, asset in df.iterrows():
        remaining = asset['remaining_life_years']
        if remaining <= 0:
            # Already past useful life — renew in year 1
            forecast[1] += asset['replacement_value']
        elif remaining <= planning_horizon:
            year = max(1, int(round(remaining)))
            forecast[year] += asset['replacement_value']

    # Calculate NPV
    cashflows = [forecast.get(y, 0) for y in range(1, planning_horizon + 1)]
    total_npv = npv(cashflows, discount_rate)

    return forecast, total_npv
```

### Funding Gap Analysis

```python
def funding_gap(required_expenditure, available_funding):
    """Calculate annual and cumulative funding gap."""
    gap = {}
    cumulative = 0
    for year in required_expenditure:
        annual_gap = required_expenditure[year] - available_funding.get(year, 0)
        cumulative += annual_gap
        gap[year] = {
            'required': required_expenditure[year],
            'available': available_funding.get(year, 0),
            'annual_gap': annual_gap,
            'cumulative_gap': cumulative,
            'sustainability_ratio': available_funding.get(year, 0) / max(required_expenditure[year], 1) * 100
        }
    return gap
```

### Default Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Discount rate | 4.0% | Real discount rate (nominal minus inflation) |
| Inflation rate | 2.5% | CPI-based |
| Planning horizon | 10 years | Standard for AMPs |
| Residual value | $0 | Conservative assumption |
| Condition trigger for renewal | Grade 4 | Most organisations |

## Chart Specifications

### Standard Charts for AMP

All charts follow SAS-AM branding:

```python
import matplotlib.pyplot as plt
import matplotlib

BRAND = {
    'sas_blue': '#002244',
    'sas_green': '#69BE28',
    'palette': ['#69BE28', '#002244', '#3B82F6', '#F59E0B', '#EF4444', '#8B5CF6'],
    'background': '#ffffff',
    'text': '#002244',
    'grid': '#ededed',
    'font': 'sans-serif'  # Falls back gracefully; Source Sans Pro if installed
}

def apply_sas_style(fig, ax):
    """Apply SAS-AM branding to matplotlib figure."""
    ax.set_facecolor(BRAND['background'])
    fig.set_facecolor(BRAND['background'])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(BRAND['grid'])
    ax.spines['bottom'].set_color(BRAND['grid'])
    ax.tick_params(colors=BRAND['text'], labelsize=10)
    ax.yaxis.grid(True, color=BRAND['grid'], linewidth=0.5)
    ax.set_axisbelow(True)
    for text in [ax.title, ax.xaxis.label, ax.yaxis.label]:
        text.set_color(BRAND['text'])
    return fig, ax
```

### Chart 1: Renewal Forecast vs Available Funding

- Type: Stacked bar (renewal by class) + line overlay (available funding)
- X-axis: Year (1-10)
- Y-axis: $ (millions)
- Colours: Chart palette for asset classes; SAS Green dashed line for funding
- File: `charts/renewal-vs-funding.png`

### Chart 2: Asset Condition Distribution

- Type: Horizontal bar chart
- X-axis: Count or percentage of assets
- Y-axis: Condition grade (1-5)
- Colours: Green-to-red gradient (1=green, 5=red)
- File: `charts/condition-distribution.png`

### Chart 3: Asset Age Profile

- Type: Histogram
- X-axis: Age (years), binned in 5-year intervals
- Y-axis: Count or replacement value
- Colour: SAS Blue bars
- Overlay: Vertical line at average useful life
- File: `charts/age-profile.png`

### Chart 4: Expenditure Breakdown

- Type: Pie chart or treemap
- Segments: Operations, Maintenance, Renewal, Upgrade, Disposal
- Colours: Chart palette
- File: `charts/expenditure-breakdown.png`

### Chart 5: Asset Value Trajectory

- Type: Dual line chart
- Lines: Replacement value (solid), written-down value (dashed)
- X-axis: Year (0-10)
- Y-axis: $ (millions)
- Colours: SAS Blue (replacement), SAS Green (WDV)
- File: `charts/value-trajectory.png`

### Chart 6: Funding Gap Analysis

- Type: Bar chart with cumulative line
- Bars: Annual gap (positive = surplus, negative = deficit)
- Line: Cumulative gap
- Colours: SAS Green (surplus), Red (deficit)
- File: `charts/funding-gap.png`

### Chart 7: Criticality Distribution

- Type: Heatmap or matrix
- X-axis: Likelihood (1-5)
- Y-axis: Consequence (1-5)
- Colour: Green-yellow-red heat scale
- Cell values: Count of assets
- File: `charts/criticality-matrix.png`

## D3.js Chart Specifications

For the HTML presentation, generate D3.js specifications as JSON files:

```json
{
  "chart_type": "stacked_bar_with_line",
  "title": "10-Year Renewal Forecast vs Available Funding",
  "x_axis": {"label": "Year", "values": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]},
  "y_axis": {"label": "Expenditure ($M)", "format": ",.1f"},
  "series": [
    {"name": "Roads", "values": [...], "type": "bar", "colour": "#69BE28"},
    {"name": "Buildings", "values": [...], "type": "bar", "colour": "#002244"},
    {"name": "Available Funding", "values": [...], "type": "line", "colour": "#EF4444", "dash": "5,5"}
  ]
}
```

Save D3 specs to `sas-amp-working/data/charts/d3/` for HTML presentation embedding.

## Data Quality Assessment Framework

Rate each dimension:

| Dimension | High | Medium | Low |
|-----------|------|--------|-----|
| Completeness | >90% fields populated | 70-90% | <70% |
| Accuracy | Verified/audited data | Self-reported, reasonable | Estimated or unknown origin |
| Timeliness | <2 years old | 2-5 years old | >5 years old |
| Consistency | Uniform naming/units | Minor inconsistencies | Major inconsistencies |
| Granularity | Individual asset level | Asset class level | Portfolio level only |

Overall confidence = lowest dimension rating (conservative approach).
