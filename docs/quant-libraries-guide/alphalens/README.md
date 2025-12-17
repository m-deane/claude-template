# Alphalens - Comprehensive User Reference Guide

**Version:** alphalens-reloaded 0.4.6
**Status:** Actively Maintained
**Purpose:** Factor Analysis and Performance Attribution

---

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Complete API Reference](#complete-api-reference)
5. [Plotting Functions with Interpretation](#plotting-functions-with-interpretation)
6. [Use Cases by Skill Level](#use-cases-by-skill-level)
7. [Core Concepts](#core-concepts)
8. [Best Practices & Common Pitfalls](#best-practices--common-pitfalls)

---

## Overview

Alphalens is a Python library for performance analysis of predictive (alpha) stock factors. It evaluates whether quantitative signals have genuine predictive power for future returns.

**Key Capabilities:**
- Evaluate factor predictiveness via Information Coefficient (IC)
- Analyze returns by factor quantile
- Assess turnover and transaction cost implications
- Generate comprehensive "tear sheets" for factor evaluation
- Integrate with Pyfolio for portfolio analysis

---

## Installation

### Recommended: alphalens-reloaded

```bash
pip install alphalens-reloaded
```

- **Latest Version:** 0.4.6 (June 2025)
- **Python Support:** 3.10, 3.11, 3.12, 3.13
- **Maintainer:** Stefan Jansen (ml4trading)

### Alternative: Conda

```bash
conda install -c conda-forge alphalens-reloaded
```

### Dependencies

- matplotlib, numpy, pandas, scipy, seaborn, statsmodels

---

## Quick Start

```python
import alphalens as al
import pandas as pd
import numpy as np

# 1. Prepare your factor data (MultiIndex: date, asset)
# factor = pd.Series with MultiIndex (date, asset)

# 2. Prepare pricing data
# prices = pd.DataFrame with date index and asset columns

# 3. Format data for analysis
factor_data = al.utils.get_clean_factor_and_forward_returns(
    factor=factor,
    prices=prices,
    quantiles=5,
    periods=(1, 5, 10)
)

# 4. Generate tear sheet
al.tears.create_full_tear_sheet(factor_data)
```

---

## Complete API Reference

### Module: alphalens.utils

#### get_clean_factor_and_forward_returns()

**The primary data pipeline function.**

```python
al.utils.get_clean_factor_and_forward_returns(
    factor,                    # pd.Series (MultiIndex: date, asset) - Required
    prices,                    # pd.DataFrame (date index, asset columns) - Required
    groupby=None,              # pd.Series or dict - Sector/group mapping
    binning_by_group=False,    # bool - Separate quantiles per group
    quantiles=5,               # int or sequence - Number of quantile buckets
    bins=None,                 # int or sequence - Equal-width bins (alt to quantiles)
    periods=(1, 5, 10),        # tuple - Forward return horizons in trading days
    filter_zscore=20,          # float - Outlier threshold in std devs
    groupby_labels=None,       # dict - Human-readable group labels
    max_loss=0.35,             # float - Max allowed data loss (0.0-1.0)
    zero_aware=False,          # bool - Zero-aware binning
    cumulative_returns=True    # bool - Compute cumulative returns
)
```

**Returns:** pd.DataFrame (MultiIndex) with columns:
- `factor`: Original factor values
- `factor_quantile`: Quantile assignment (1, 2, ..., 5)
- `1D`, `5D`, `10D`: Forward returns for each period
- `group`: Group membership (if groupby provided)

**Raises:**
- `MaxLossExceededError`: When data loss exceeds max_loss
- `NonMatchingTimezoneError`: When timezone mismatches occur

**Example:**
```python
factor_data = al.utils.get_clean_factor_and_forward_returns(
    factor=momentum_factor,
    prices=stock_prices,
    quantiles=5,
    periods=(1, 5, 21),
    groupby=sector_map,
    binning_by_group=True,
    max_loss=0.4
)
```

#### compute_forward_returns()

```python
al.utils.compute_forward_returns(
    factor,                    # pd.Series (MultiIndex) - Factor data
    prices,                    # pd.DataFrame - Price data
    periods=(1, 5, 10),        # tuple - Forward return horizons
    filter_zscore=None,        # float - Outlier filter
    cumulative_returns=True    # bool - Cumulative or period returns
)
```

**Returns:** pd.DataFrame (MultiIndex) with forward return columns

#### demean_forward_returns()

```python
al.utils.demean_forward_returns(
    factor_data,               # pd.DataFrame - From get_clean_factor_and_forward_returns
    grouper=None               # str - Column name for group demeaning
)
```

**Returns:** pd.DataFrame with demeaned returns

---

### Module: alphalens.tears

#### create_full_tear_sheet()

**Comprehensive factor analysis - the main function.**

```python
al.tears.create_full_tear_sheet(
    factor_data,               # pd.DataFrame - From get_clean_factor_and_forward_returns
    long_short=True,           # bool - Compute long-short portfolio
    group_neutral=False,       # bool - Group-level demeaning
    by_group=False             # bool - Display by group
)
```

**Displays:**
- Returns analysis (quantile returns, cumulative performance)
- IC analysis (time series, distribution, heatmaps)
- Turnover analysis (autocorrelation, quantile turnover)
- Summary statistics tables

#### create_returns_tear_sheet()

```python
al.tears.create_returns_tear_sheet(
    factor_data,
    long_short=True,
    group_neutral=False,
    by_group=False
)
```

**Displays:** Mean returns by quantile, return distributions, cumulative returns

#### create_information_tear_sheet()

```python
al.tears.create_information_tear_sheet(
    factor_data,
    group_neutral=False,
    by_group=False
)
```

**Displays:** IC time series, IC histogram, IC Q-Q plot, monthly IC heatmap

#### create_turnover_tear_sheet()

```python
al.tears.create_turnover_tear_sheet(
    factor_data,
    turnover_periods=None      # list - Custom periods for analysis
)
```

**Displays:** Factor rank autocorrelation, top/bottom quantile turnover

#### create_summary_tear_sheet()

```python
al.tears.create_summary_tear_sheet(
    factor_data,
    long_short=True,
    group_neutral=False
)
```

**Use Case:** Quick factor screening before full analysis

#### create_event_returns_tear_sheet()

```python
al.tears.create_event_returns_tear_sheet(
    factor_data,
    returns,                   # pd.DataFrame - Returns for event analysis
    avgretplot=(5, 15),        # tuple - (periods_before, periods_after)
    long_short=True,
    group_neutral=False,
    std_bar=True,              # bool - Show standard error bars
    by_group=False
)
```

---

### Module: alphalens.performance

#### factor_information_coefficient()

```python
al.performance.factor_information_coefficient(
    factor_data,               # pd.DataFrame - From get_clean_factor_and_forward_returns
    group_adjust=False,        # bool - Demean by group before IC
    by_group=False             # bool - Compute IC per group
)
```

**Returns:** pd.DataFrame with Spearman correlations (IC)

**Interpretation:**
- IC > 0.03: Strong predictive ability
- IC > 0.05: Excellent predictive ability
- Information Ratio (IR) = mean(IC) / std(IC): > 0.5 is good, > 1.0 excellent

#### mean_information_coefficient()

```python
al.performance.mean_information_coefficient(
    factor_data,
    group_adjust=False,
    by_group=False,
    by_time=None               # str - 'M' for monthly, 'W' for weekly
)
```

**Returns:** pd.DataFrame of aggregated IC statistics

#### mean_return_by_quantile()

```python
al.performance.mean_return_by_quantile(
    factor_data,
    by_date=False,             # bool - Per-date returns
    by_group=False,            # bool - Per-group returns
    demeaned=True,             # bool - Demean universe
    group_adjust=False         # bool - Demean by group
)
```

**Returns:** tuple of (mean_returns_df, std_error_df)

#### compute_mean_returns_spread()

```python
al.performance.compute_mean_returns_spread(
    mean_returns,              # pd.DataFrame - From mean_return_by_quantile
    upper_quant,               # int - Upper quantile (e.g., 5)
    lower_quant,               # int - Lower quantile (e.g., 1)
    std_err=None               # pd.DataFrame - Standard errors
)
```

**Returns:** tuple of (spread_series, std_error_series)

#### factor_returns()

```python
al.performance.factor_returns(
    factor_data,
    demeaned=True,
    group_adjust=False,
    equal_weight=False,
    by_asset=False             # bool - Per-asset returns
)
```

**Returns:** pd.DataFrame of period-wise portfolio returns

#### factor_alpha_beta()

```python
al.performance.factor_alpha_beta(
    factor_data,
    returns=None,              # pd.DataFrame - Benchmark returns
    demeaned=True,
    group_adjust=False,
    equal_weight=False
)
```

**Returns:** pd.Series with ['alpha', 'beta', 't-stat']

#### quantile_turnover()

```python
al.performance.quantile_turnover(
    quantile_factor,           # pd.Series - Factor with quantile assignments
    quantile,                  # int - Quantile to analyze
    period=1                   # int - Period lag
)
```

**Returns:** pd.Series of turnover percentages (0.0-1.0)

#### factor_rank_autocorrelation()

```python
al.performance.factor_rank_autocorrelation(
    factor_data,
    period=1                   # int - Autocorrelation lag
)
```

**Returns:** pd.Series of rolling autocorrelations

#### create_pyfolio_input()

```python
al.performance.create_pyfolio_input(
    factor_data,
    period,                    # str - Forward return period ('1D', '5D')
    capital=None,              # float - Starting capital
    long_short=True,
    group_neutral=False,
    equal_weight=False,
    quantiles=None,            # list - Specific quantiles
    groups=None,               # list - Specific groups
    benchmark_period='1D'
)
```

**Returns:** tuple of (returns_series, positions_df, benchmark_series)

---

### Module: alphalens.plotting

#### plot_ic_ts()

```python
al.plotting.plot_ic_ts(ic, ax=None)
```

**Displays:** IC time series with 1-month rolling mean

#### plot_ic_hist()

```python
al.plotting.plot_ic_hist(ic, ax=None)
```

**Displays:** Histogram of IC distribution

#### plot_ic_qq()

```python
al.plotting.plot_ic_qq(
    ic,
    theoretical_dist=scipy.stats.norm,
    ax=None
)
```

**Displays:** Q-Q plot of IC against theoretical distribution

#### plot_monthly_ic_heatmap()

```python
al.plotting.plot_monthly_ic_heatmap(mean_monthly_ic, ax=None)
```

**Displays:** Heatmap of monthly IC values

#### plot_quantile_returns_bar()

```python
al.plotting.plot_quantile_returns_bar(
    mean_ret_by_q,
    by_group=False,
    ylim_percentiles=None,
    ax=None
)
```

**Displays:** Bar chart of mean returns by quantile - CORE visualization

#### plot_quantile_returns_violin()

```python
al.plotting.plot_quantile_returns_violin(
    return_by_q,
    ylim_percentiles=None,
    ax=None
)
```

**Displays:** Violin plots of return distributions by quantile

#### plot_cumulative_returns()

```python
al.plotting.plot_cumulative_returns(
    factor_returns,
    period,                    # str - Period to plot
    freq=None,
    title=None,
    ax=None
)
```

**Displays:** Cumulative returns of factor-based strategy

#### plot_cumulative_returns_by_quantile()

```python
al.plotting.plot_cumulative_returns_by_quantile(
    quantile_returns,
    period,
    freq=None,
    ax=None
)
```

**Displays:** Cumulative returns separately per quantile

#### plot_mean_quantile_returns_spread_time_series()

```python
al.plotting.plot_mean_quantile_returns_spread_time_series(
    mean_returns_spread,
    std_err=None,
    bandwidth=1,
    ax=None
)
```

**Displays:** Long-short return spread (Q5 - Q1) over time

#### plot_factor_rank_auto_correlation()

```python
al.plotting.plot_factor_rank_auto_correlation(
    factor_autocorrelation,
    period=1,
    ax=None
)
```

**Displays:** Factor rank autocorrelation over time

#### plot_top_bottom_quantile_turnover()

```python
al.plotting.plot_top_bottom_quantile_turnover(
    quantile_turnover,
    period=1,
    ax=None
)
```

**Displays:** Turnover for top and bottom quantiles

#### Summary Tables

```python
al.plotting.plot_information_table(ic_data)
al.plotting.plot_returns_table(alpha_beta, mean_ret_quantile, mean_ret_spread_quantile)
al.plotting.plot_quantile_statistics_table(factor_data)
al.plotting.plot_turnover_table(autocorrelation_data, quantile_turnover)
```

---

## Plotting Functions with Interpretation

### plot_quantile_returns_bar() - CRITICAL

**What it shows:** Bar chart of mean forward returns for each factor quantile.

**How to interpret:**
- **Monotonic pattern (Q1 < Q2 < Q3 < Q4 < Q5):** Strong predictive factor
- **Inverted pattern:** Factor predicts negative returns (good for shorting)
- **Flat pattern:** No predictive power

**Good signs:**
- Clear monotonic increase from Q1 to Q5
- Large spread between Q1 and Q5 (profitable long-short)
- Consistent across different time periods

**Red flags:**
- Non-monotonic (e.g., Q3 highest)
- Tiny spread (< 0.1% daily)
- High error bars overlapping

**Example interpretation:**
```
Q1: -0.05%  Q2: -0.02%  Q3: 0.01%  Q4: 0.03%  Q5: 0.06%
→ Good monotonic relationship
→ Spread = 0.11% daily ≈ 28% annualized
→ Factor is predictive
```

### plot_ic_ts() - CRITICAL

**What it shows:** Information Coefficient over time with rolling average.

**How to interpret:**
- **Consistent positive IC:** Reliable factor
- **Volatile IC:** Regime-dependent factor
- **Declining IC:** Factor decay (alpha erosion)

**Good signs:**
- Mean IC > 0.03 (visible in rolling average)
- Low volatility around mean
- No prolonged negative periods

**Red flags:**
- Mean IC near zero
- Extended negative IC periods
- High volatility (unreliable signal)

### plot_monthly_ic_heatmap()

**What it shows:** Calendar heatmap of average IC by month/year.

**How to interpret:**
- **Uniform colors:** Stable factor across time
- **Seasonal patterns:** Time-dependent factor
- **Recent deterioration:** Factor may be crowded

**Good signs:**
- Mostly green/positive across all periods
- No obvious seasonal bias
- Recent months similar to historical

**Red flags:**
- Specific months consistently red
- Recent years worse than historical
- Strong seasonal patterns (may not persist)

### plot_top_bottom_quantile_turnover()

**What it shows:** Percentage of positions that change each period in top/bottom quantiles.

**How to interpret:**
- **High turnover (> 50%):** High transaction costs
- **Low turnover (< 20%):** Stable signals, lower costs
- **Asymmetric turnover:** Different behavior in longs vs shorts

**Good signs:**
- Turnover < 30% for daily rebalancing
- Symmetric top/bottom turnover
- Stable over time

**Red flags:**
- Turnover > 50% (costs may exceed alpha)
- Spiky turnover (unstable signal)
- Increasing trend (factor becoming noisier)

---

## Use Cases by Skill Level

### BEGINNER: Simple Momentum Factor Analysis

```python
"""
Beginner Example: 20-day momentum factor evaluation
Goal: Determine if past 20-day returns predict future returns
"""
import alphalens as al
import pandas as pd
import numpy as np

# Step 1: Generate sample data
np.random.seed(42)
dates = pd.date_range('2020-01-01', periods=500, freq='D')
assets = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'META']

# Create price data
prices = pd.DataFrame(
    index=dates,
    columns=assets,
    data=100 * np.cumprod(1 + np.random.randn(500, 5) * 0.02, axis=0)
)

# Step 2: Create momentum factor (20-day return)
# Factor must be MultiIndex Series (date, asset)
momentum = prices.pct_change(20)  # 20-day momentum
factor = momentum.stack()
factor.index.names = ['date', 'asset']
factor = factor.dropna()

print(f"Factor shape: {factor.shape}")
print(f"Factor sample:\n{factor.head(10)}")

# Step 3: Prepare data for Alphalens
factor_data = al.utils.get_clean_factor_and_forward_returns(
    factor=factor,
    prices=prices,
    quantiles=5,           # Divide into 5 groups
    periods=(1, 5, 10),    # 1-day, 5-day, 10-day forward returns
    max_loss=0.5           # Allow up to 50% data loss
)

print(f"\nFactor data shape: {factor_data.shape}")
print(f"Columns: {factor_data.columns.tolist()}")

# Step 4: Quick summary analysis
al.tears.create_summary_tear_sheet(factor_data)

# Step 5: Full analysis (if promising)
al.tears.create_full_tear_sheet(factor_data, long_short=True)

# Step 6: Extract key metrics programmatically
ic = al.performance.factor_information_coefficient(factor_data)
mean_ic = ic.mean()
print(f"\nMean IC by period:\n{mean_ic}")
print(f"IC > 0.03 threshold: {(mean_ic.abs() > 0.03).any()}")
```

### INTERMEDIATE: Sector-Neutral Factor with Multiple Periods

```python
"""
Intermediate Example: Value factor with sector neutralization
Goal: Evaluate factor while removing sector effects
"""
import alphalens as al
import pandas as pd
import numpy as np

# Setup data (assume prices DataFrame exists)
# ...

# Create sector mapping
sector_map = pd.Series({
    'AAPL': 'Tech', 'GOOGL': 'Tech', 'MSFT': 'Tech',
    'JPM': 'Finance', 'BAC': 'Finance', 'GS': 'Finance',
    'XOM': 'Energy', 'CVX': 'Energy',
    'JNJ': 'Healthcare', 'PFE': 'Healthcare'
})

# Create value factor (e.g., earnings yield - simulated)
np.random.seed(42)
value_factor = pd.DataFrame(
    index=prices.index,
    columns=prices.columns,
    data=np.random.randn(len(prices), len(prices.columns)) * 0.1
).stack()
value_factor.index.names = ['date', 'asset']

# Prepare with sector grouping
factor_data = al.utils.get_clean_factor_and_forward_returns(
    factor=value_factor,
    prices=prices,
    groupby=sector_map,        # Add sector information
    binning_by_group=True,     # Rank within sectors
    quantiles=5,
    periods=(1, 5, 21, 63),    # Daily, weekly, monthly, quarterly
    max_loss=0.35
)

# Sector-neutral analysis
al.tears.create_full_tear_sheet(
    factor_data,
    long_short=True,
    group_neutral=True,        # Remove sector exposure
    by_group=True              # Show per-sector breakdown
)

# Compare sector performance
ic_by_sector = al.performance.mean_information_coefficient(
    factor_data, by_group=True
)
print("IC by Sector:")
print(ic_by_sector)

# Identify best/worst sectors for this factor
mean_ic_by_sector = ic_by_sector.mean(axis=1)
print(f"\nBest sector: {mean_ic_by_sector.idxmax()}")
print(f"Worst sector: {mean_ic_by_sector.idxmin()}")
```

### ADVANCED: Multi-Factor with Pyfolio Integration

```python
"""
Advanced Example: Combined momentum + value factor with full risk analysis
Goal: Create and evaluate combined factor, then analyze with Pyfolio
"""
import alphalens as al
import pyfolio as pf
import pandas as pd
import numpy as np

# Assume we have momentum_factor and value_factor

# Step 1: Combine factors (z-score normalization + equal weight)
def zscore(x):
    return (x - x.mean()) / x.std()

# Normalize each factor cross-sectionally
momentum_z = momentum_factor.groupby(level='date').apply(zscore)
value_z = value_factor.groupby(level='date').apply(zscore)

# Combined factor (equal weight)
combined_factor = 0.5 * momentum_z + 0.5 * value_z
combined_factor = combined_factor.dropna()

# Step 2: Alphalens analysis
factor_data = al.utils.get_clean_factor_and_forward_returns(
    factor=combined_factor,
    prices=prices,
    groupby=sector_map,
    quantiles=5,
    periods=(1, 5, 21)
)

# Check if factor is worth pursuing
ic = al.performance.factor_information_coefficient(factor_data)
mean_ic = ic.mean()
ic_std = ic.std()
ir = mean_ic / ic_std  # Information Ratio

print("Combined Factor Analysis:")
print(f"Mean IC: {mean_ic.to_dict()}")
print(f"IR: {ir.to_dict()}")
print(f"Viable: {(ir > 0.5).any()}")

# Step 3: Generate Pyfolio inputs
if (ir > 0.5).any():
    returns, positions, benchmark = al.performance.create_pyfolio_input(
        factor_data,
        period='5D',           # 5-day holding period
        long_short=True,
        capital=1000000        # $1M capital
    )

    # Step 4: Pyfolio risk analysis
    pf.create_full_tear_sheet(
        returns,
        positions=positions,
        benchmark_rets=benchmark,
        live_start_date=returns.index[-63]  # Last quarter OOS
    )
```

### EXPERT: Custom Factor Pipeline with Statistical Validation

```python
"""
Expert Example: Production-grade factor research pipeline
Goal: Rigorous statistical validation with multiple testing correction
"""
import alphalens as al
import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests

class FactorResearchPipeline:
    """Production factor research with statistical rigor."""

    def __init__(self, prices, sectors=None, min_ic=0.02, min_ir=0.3):
        self.prices = prices
        self.sectors = sectors
        self.min_ic = min_ic
        self.min_ir = min_ir
        self.results = {}

    def evaluate_factor(self, factor, name, periods=(1, 5, 21)):
        """Evaluate single factor with full statistics."""
        try:
            factor_data = al.utils.get_clean_factor_and_forward_returns(
                factor=factor,
                prices=self.prices,
                groupby=self.sectors,
                quantiles=5,
                periods=periods,
                max_loss=0.35
            )
        except Exception as e:
            return {'name': name, 'status': 'failed', 'error': str(e)}

        # IC analysis
        ic = al.performance.factor_information_coefficient(factor_data)
        mean_ic = ic.mean()
        ic_std = ic.std()
        ir = mean_ic / ic_std
        ic_tstat = mean_ic / (ic_std / np.sqrt(len(ic)))
        ic_pvalue = 2 * (1 - stats.t.cdf(abs(ic_tstat), df=len(ic)-1))

        # Quantile returns
        mean_ret, std_err = al.performance.mean_return_by_quantile(factor_data)
        spread = mean_ret.loc[5] - mean_ret.loc[1]

        # Turnover
        autocorr = al.performance.factor_rank_autocorrelation(factor_data)
        turnover_q1 = al.performance.quantile_turnover(
            factor_data['factor_quantile'], 1
        ).mean()
        turnover_q5 = al.performance.quantile_turnover(
            factor_data['factor_quantile'], 5
        ).mean()

        result = {
            'name': name,
            'status': 'evaluated',
            'mean_ic': mean_ic.to_dict(),
            'ir': ir.to_dict(),
            'ic_tstat': ic_tstat.to_dict(),
            'ic_pvalue': ic_pvalue.to_dict(),
            'spread': spread.to_dict(),
            'mean_autocorr': autocorr.mean(),
            'turnover_q1': turnover_q1,
            'turnover_q5': turnover_q5,
            'factor_data': factor_data
        }

        self.results[name] = result
        return result

    def evaluate_multiple(self, factors_dict):
        """Evaluate multiple factors with multiple testing correction."""
        for name, factor in factors_dict.items():
            self.evaluate_factor(factor, name)

        # Collect p-values for multiple testing correction
        pvalues = []
        factor_names = []
        period_names = []

        for name, result in self.results.items():
            if result['status'] == 'evaluated':
                for period, pval in result['ic_pvalue'].items():
                    pvalues.append(pval)
                    factor_names.append(name)
                    period_names.append(period)

        if pvalues:
            # Benjamini-Hochberg correction
            rejected, adjusted_pvals, _, _ = multipletests(
                pvalues, method='fdr_bh', alpha=0.05
            )

            # Update results with adjusted p-values
            idx = 0
            for name, result in self.results.items():
                if result['status'] == 'evaluated':
                    result['adjusted_pvalue'] = {}
                    result['significant'] = {}
                    for period in result['ic_pvalue'].keys():
                        result['adjusted_pvalue'][period] = adjusted_pvals[idx]
                        result['significant'][period] = rejected[idx]
                        idx += 1

        return self.get_summary()

    def get_summary(self):
        """Return summary of all evaluated factors."""
        summary = []
        for name, result in self.results.items():
            if result['status'] == 'evaluated':
                for period in result['mean_ic'].keys():
                    summary.append({
                        'factor': name,
                        'period': period,
                        'mean_ic': result['mean_ic'][period],
                        'ir': result['ir'][period],
                        'ic_pvalue': result['ic_pvalue'][period],
                        'adj_pvalue': result.get('adjusted_pvalue', {}).get(period),
                        'significant': result.get('significant', {}).get(period),
                        'spread': result['spread'][period],
                        'turnover': (result['turnover_q1'] + result['turnover_q5'])/2
                    })
        return pd.DataFrame(summary)

    def get_viable_factors(self):
        """Return factors passing all criteria."""
        summary = self.get_summary()
        viable = summary[
            (summary['mean_ic'].abs() >= self.min_ic) &
            (summary['ir'].abs() >= self.min_ir) &
            (summary['significant'] == True) &
            (summary['turnover'] < 0.5)
        ]
        return viable

# Usage
pipeline = FactorResearchPipeline(prices, sectors, min_ic=0.02, min_ir=0.3)

# Define factors to test
factors = {
    'momentum_20d': momentum_factor_20d,
    'momentum_60d': momentum_factor_60d,
    'value': value_factor,
    'quality': quality_factor,
    'volatility': volatility_factor
}

# Evaluate all with multiple testing correction
summary = pipeline.evaluate_multiple(factors)
print("\nFactor Evaluation Summary:")
print(summary.to_string())

# Get viable factors
viable = pipeline.get_viable_factors()
print(f"\nViable factors: {viable['factor'].unique().tolist()}")
```

---

## Core Concepts

### Information Coefficient (IC)

**Definition:** Spearman rank correlation between factor values and subsequent forward returns.

**Formula:** `IC = spearman_correlation(factor_ranks, forward_return_ranks)`

**Range:** -1 to +1

**Benchmarks:**
| IC Value | Interpretation |
|----------|----------------|
| > 0.05 | Excellent |
| 0.03 - 0.05 | Strong |
| 0.02 - 0.03 | Moderate |
| < 0.02 | Weak |

**Information Ratio (IR):**
- Formula: `IR = mean(IC) / std(IC)`
- Interpretation: Sharpe ratio for IC
- Good: > 0.5
- Excellent: > 1.0

### Quantile Returns

**Definition:** Mean forward returns for assets in each factor quintile.

**Key Metrics:**
- **Monotonicity:** Q5 > Q4 > Q3 > Q2 > Q1 (ideal)
- **Spread:** Q5 - Q1 (long-short profitability)
- **Significance:** Error bars should not overlap

**Demeaning Modes:**
- **None:** Raw returns
- **Long-Short (demeaned=True):** Universe-demeaned
- **Group-Neutral:** Group-demeaned

### Turnover

**Definition:** Rate of position changes due to factor reranking.

**Metrics:**
- **Quantile Turnover:** % of positions changed per period
- **Factor Rank Autocorrelation:** Stability of rankings

**Interpretation:**
| Turnover | Cost Implication |
|----------|------------------|
| < 0.2 | Low costs |
| 0.2 - 0.5 | Moderate costs |
| > 0.5 | High costs (may erode alpha) |

**Relationship:** High autocorrelation → Low turnover → Lower costs

---

## Best Practices & Common Pitfalls

### Best Practices

1. **Always run `get_clean_factor_and_forward_returns` first** to validate data
2. **Use `create_summary_tear_sheet` for quick screening** before full analysis
3. **Compare multiple holding periods** to find optimal frequency
4. **Set appropriate `max_loss`** (0.35 default, lower for critical data)
5. **Use `group_neutral=True`** to isolate alpha from sector bets
6. **Check turnover** before declaring profitability
7. **Validate IC consistency over time** (not just average)
8. **Use alphalens-reloaded** instead of original alphalens

### Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Ignoring turnover | Always check transaction cost implications |
| Insufficient price history | Need prices extending past last factor date |
| Timezone mismatches | Ensure consistent timezones |
| Too many quantiles with small universe | Use quantiles=3 for < 50 assets |
| Mistaking high IC for profitability | Check return magnitudes and costs |
| Overfitting to specific period | Test across different time windows |
| Not accounting for survivorship bias | Use point-in-time data |
| Factor crowding | Monitor IC decay over time |

### Diagnostic Checklist

- [ ] IC > 0.03 (or < -0.03 for short factors)
- [ ] IR > 0.5
- [ ] Monotonic quantile returns
- [ ] Turnover < 0.5 for daily rebalancing
- [ ] Stable IC across time periods
- [ ] Works across multiple sectors
- [ ] Spread exceeds estimated transaction costs

---

## Resources

- **Documentation:** https://alphalens.ml4trading.io/
- **GitHub (reloaded):** https://github.com/stefan-jansen/alphalens-reloaded
- **Original Quantopian:** https://github.com/quantopian/alphalens
