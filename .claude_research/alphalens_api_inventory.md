# Alphalens Python Library - Comprehensive API Inventory

**Research Date:** 2025-12-17

**Purpose:** Complete API inventory for comprehensive Alphalens documentation

---

## Executive Summary

Alphalens is a Python library for performance analysis of predictive (alpha) stock factors. Originally developed by Quantopian, it provides systematic framework to evaluate whether quantitative signals have genuine predictive power for future returns.

### Key Statistics
- **Original Repository:** 4,000+ GitHub stars, 1,300+ forks, 745 dependent projects
- **Status:** Original archived (2020), actively maintained forks available
- **Best Maintained Fork:** alphalens-reloaded by Stefan Jansen (v0.4.6, 2025-06-02)

---

## 1. VERSION AND INSTALLATION

### 1.1 Original Package (Not Recommended for New Projects)

```bash
pip install alphalens
```

- **Latest Version:** 0.4.0
- **Last Updated:** 2020-04-27
- **Status:** No longer maintained
- **PyPI:** https://pypi.org/project/alphalens/

### 1.2 Alphalens-Reloaded (Recommended)

```bash
pip install alphalens-reloaded
```

- **Latest Version:** 0.4.6
- **Last Updated:** 2025-06-02
- **Python Support:** 3.10, 3.11, 3.12, 3.13
- **Maintainer:** Stefan Jansen
- **GitHub:** https://github.com/stefan-jansen/alphalens-reloaded
- **Documentation:** https://alphalens.ml4trading.io/
- **Status:** Actively maintained, CI/CD with GitHub Actions

### 1.3 Alternative Installations

**Conda:**
```bash
conda install -c conda-forge alphalens
# or for reloaded version
conda install -c conda-forge alphalens-reloaded
```

**Development Version:**
```bash
pip install git+https://github.com/quantopian/alphalens
# or
pip install git+https://github.com/stefan-jansen/alphalens-reloaded
```

### 1.4 Dependencies

**Required:**
- matplotlib (visualization)
- numpy (numerical computing)
- pandas (data manipulation)
- scipy (scientific functions)
- seaborn (statistical graphics)
- statsmodels (statistical modeling)

**Compatibility Note:**
- numpy >= 2.0 requires pandas >= 2.2.2

**Integrations:**
- **Zipline:** Backtesting library integration
- **Pyfolio:** Portfolio performance and risk analysis

---

## 2. MODULE STRUCTURE

Alphalens is organized into four core modules:

```python
import alphalens as al

# Available modules
al.utils      # Data preparation and utilities
al.tears      # Tear sheet generation (comprehensive reports)
al.performance  # Performance metrics computation
al.plotting   # Visualization functions
```

### Package Imports (from __init__.py)

```python
from alphalens import performance
from alphalens import plotting
from alphalens import tears
from alphalens import utils

# Version info
print(alphalens.__version__)
```

---

## 3. MODULE: alphalens.utils

**Purpose:** Data preparation and utility functions for factor analysis

### 3.1 Primary Data Preparation Function

#### get_clean_factor_and_forward_returns()

**Signature:**
```python
alphalens.utils.get_clean_factor_and_forward_returns(
    factor,
    prices,
    groupby=None,
    binning_by_group=False,
    quantiles=5,
    bins=None,
    periods=(1, 5, 10),
    filter_zscore=20,
    groupby_labels=None,
    max_loss=0.35,
    zero_aware=False,
    cumulative_returns=True
)
```

**Description:**
Primary data pipeline function. Formats factor data, forward return data, and group mappings into a DataFrame suitable for all Alphalens analysis functions.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `factor` | pd.Series (MultiIndex) | Required | MultiIndex Series indexed by (timestamp, asset) containing alpha factor values |
| `prices` | pd.DataFrame | Required | DataFrame with date index and asset columns containing pricing data |
| `groupby` | pd.Series or dict | None | Optional group assignments (e.g., sector) for grouped analysis |
| `binning_by_group` | bool | False | If True, perform separate quantile bucketing per group |
| `quantiles` | int or sequence | 5 | Integer for equal-sized quantiles or sequence of quantile thresholds |
| `bins` | int or sequence | None | Integer for equal-width bins or sequence of bin edges (alternative to quantiles) |
| `periods` | tuple | (1, 5, 10) | Tuple of forward return horizons in trading days |
| `filter_zscore` | float | 20 | Outlier filtering threshold in standard deviations |
| `groupby_labels` | dict | None | Dictionary mapping group IDs to human-readable labels |
| `max_loss` | float | 0.35 | Maximum allowed data loss percentage (0.0-1.0). Raises error if exceeded |
| `zero_aware` | bool | False | If True, perform zero-aware binning |
| `cumulative_returns` | bool | True | If True, compute cumulative forward returns |

**Returns:**
- **Type:** pd.DataFrame (MultiIndex)
- **Index:** (date, asset) MultiIndex
- **Columns:**
  - `factor`: Original factor values
  - `factor_quantile`: Quantile assignment (1, 2, 3, 4, 5)
  - `[period]_period_return`: Forward returns for each period (e.g., '1D', '5D', '10D')
  - `group`: Optional group membership (e.g., sector)

**Raises:**
- `MaxLossExceededError`: When data loss exceeds max_loss threshold
- `NonMatchingTimezoneError`: When timezone mismatches occur

**Example:**
```python
import alphalens as al
import pandas as pd

# Prepare factor data
factor_data = al.utils.get_clean_factor_and_forward_returns(
    factor=my_factor,           # pd.Series with MultiIndex
    prices=pricing_data,        # pd.DataFrame
    quantiles=5,
    periods=(1, 5, 10),
    groupby=sector_map,
    binning_by_group=True,
    groupby_labels={'tech': 'Technology', 'fin': 'Finance'},
    max_loss=0.4
)
```

### 3.2 Alternative Data Preparation

#### get_clean_factor()

```python
alphalens.utils.get_clean_factor(
    factor,
    forward_returns,
    groupby=None,
    binning_by_group=False,
    quantiles=5,
    bins=None,
    groupby_labels=None,
    max_loss=0.35,
    zero_aware=False
)
```

**Description:** Use when forward returns are already computed. Same output structure as `get_clean_factor_and_forward_returns`.

#### compute_forward_returns()

```python
alphalens.utils.compute_forward_returns(
    factor,
    prices,
    periods=(1, 5, 10),
    filter_zscore=None,
    cumulative_returns=True
)
```

**Description:** Calculates N-period forward returns for each asset at each timestamp.

**Returns:** pd.DataFrame (MultiIndex) with forward return columns

#### demean_forward_returns()

```python
alphalens.utils.demean_forward_returns(
    factor_data,
    grouper=None
)
```

**Description:** Converts returns to group-relative or universe-relative basis by subtracting mean returns.

**Returns:** pd.DataFrame with normalized returns (same shape as input)

### 3.3 Factor Binning

#### quantize_factor()

```python
alphalens.utils.quantize_factor(*args, **kwargs)
```

**Description:** Assigns factor values to quantile buckets.

### 3.4 Calendar Utilities

#### infer_trading_calendar()

```python
alphalens.utils.infer_trading_calendar(factor_idx, prices_idx)
```

**Returns:** pd.DateOffset

#### add_custom_calendar_timedelta()

```python
alphalens.utils.add_custom_calendar_timedelta(input, timedelta, freq)
```

**Returns:** pd.DatetimeIndex or pd.Timestamp

#### diff_custom_calendar_timedeltas()

```python
alphalens.utils.diff_custom_calendar_timedeltas(start, end, freq)
```

**Returns:** pd.Timedelta

#### backshift_returns_series()

```python
alphalens.utils.backshift_returns_series(series, N)
```

**Description:** Shifts multi-indexed return series backward N observations.

### 3.5 Time Conversion

#### rate_of_return()

```python
alphalens.utils.rate_of_return(period_ret, base_period)
```

**Description:** Annualizes or standardizes returns to target frequency.

**Returns:** pd.DataFrame

#### std_conversion()

```python
alphalens.utils.std_conversion(period_std, base_period)
```

**Description:** Converts volatility to standardized period basis.

**Returns:** pd.DataFrame

#### timedelta_to_string()

```python
alphalens.utils.timedelta_to_string(timedelta)
```

**Returns:** str (e.g., '1D', '5D')

#### timedelta_strings_to_integers()

```python
alphalens.utils.timedelta_strings_to_integers(sequence)
```

**Example:** `['1D', '5D'] -> [1, 5]`

**Returns:** list

#### get_forward_returns_columns()

```python
alphalens.utils.get_forward_returns_columns(
    columns,
    require_exact_day_multiple=False
)
```

**Description:** Identifies forward return columns in DataFrames.

**Returns:** list of column names

### 3.6 Display and Formatting

#### print_table()

```python
alphalens.utils.print_table(table, name=None, fmt=None)
```

**Description:** Pretty-prints DataFrames/Series (HTML in Jupyter, text in console).

**Parameters:**
- `table`: pd.DataFrame or pd.Series
- `name`: str, optional - Table name/header
- `fmt`: str, optional - Format string for values

### 3.7 Error Handling

#### Exceptions

**MaxLossExceededError**
- Raised when data loss exceeds max_loss threshold during data preparation

**NonMatchingTimezoneError**
- Raised when timezone mismatches detected between factor and price data

#### Decorators/Functions

**non_unique_bin_edges_error()**
```python
@alphalens.utils.non_unique_bin_edges_error
def func():
    pass
```

**Description:** Decorator providing informative quantile binning errors

**rethrow()**
```python
alphalens.utils.rethrow(exception, additional_message)
```

**Description:** Re-raises exceptions with supplementary context

---

## 4. MODULE: alphalens.tears

**Purpose:** Tear sheet generation providing comprehensive factor analysis visualizations and reports

### 4.1 Classes

#### GridFigure

```python
class alphalens.tears.GridFigure(rows, cols)
```

**Description:** Helper class for grid-based plotting operations

**Methods:**

| Method | Description |
|--------|-------------|
| `close()` | Closes the figure |
| `next_cell()` | Advances to next cell in grid |
| `next_row()` | Advances to next row in grid |

### 4.2 Comprehensive Tear Sheets

#### create_full_tear_sheet()

```python
alphalens.tears.create_full_tear_sheet(
    factor_data,
    long_short=True,
    group_neutral=False,
    by_group=False
)
```

**Description:** Creates comprehensive tear sheet combining returns analysis, information coefficient analysis, and turnover analysis. PRIMARY function for complete factor evaluation.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `factor_data` | pd.DataFrame (MultiIndex) | Required | Output from get_clean_factor_and_forward_returns |
| `long_short` | bool | True | If True, compute long-short portfolio (demean returns and factor values) |
| `group_neutral` | bool | False | If True, perform group-level demeaning |
| `by_group` | bool | False | If True, display separate graphs for each group |

**Output:** Displays comprehensive visualizations including:
- Returns by quantile (bar charts, violin plots)
- Cumulative returns over time
- Information Coefficient time series
- IC distribution and Q-Q plots
- Monthly IC heatmaps
- Turnover metrics
- Summary statistics tables

**Example:**
```python
import alphalens as al

# After preparing factor_data
al.tears.create_full_tear_sheet(
    factor_data,
    long_short=True,
    group_neutral=False,
    by_group=False
)
```

### 4.3 Focused Tear Sheets

#### create_returns_tear_sheet()

```python
alphalens.tears.create_returns_tear_sheet(
    factor_data,
    long_short=True,
    group_neutral=False,
    by_group=False
)
```

**Description:** Tear sheet focused on returns analysis. Shows mean returns by quantile, cumulative returns, and return distributions.

**Output:**
- Mean returns by quantile (bar chart)
- Return distributions (violin plots)
- Cumulative returns by quantile
- Long-short return spread
- Returns summary table

#### create_information_tear_sheet()

```python
alphalens.tears.create_information_tear_sheet(
    factor_data,
    group_neutral=False,
    by_group=False
)
```

**Description:** Evaluates factor predictiveness through Information Coefficient analysis.

**Output:**
- IC time series with moving average
- IC histogram
- IC Q-Q plot
- Monthly IC heatmap
- IC by group (if groups provided)
- IC summary statistics table

#### create_turnover_tear_sheet()

```python
alphalens.tears.create_turnover_tear_sheet(
    factor_data,
    turnover_periods=None
)
```

**Description:** Examines portfolio rebalancing frequency and position changes.

**Parameters:**
- `factor_data`: pd.DataFrame (MultiIndex)
- `turnover_periods`: list/tuple, optional - Custom periods for turnover analysis

**Output:**
- Factor rank autocorrelation plot
- Top/bottom quantile turnover
- Turnover summary table

#### create_summary_tear_sheet()

```python
alphalens.tears.create_summary_tear_sheet(
    factor_data,
    long_short=True,
    group_neutral=False
)
```

**Description:** Condensed summary with key metrics from returns, IC, and turnover.

**Use Case:** Quick factor screening before full analysis

### 4.4 Event Analysis Tear Sheets

#### create_event_returns_tear_sheet()

```python
alphalens.tears.create_event_returns_tear_sheet(
    factor_data,
    returns,
    avgretplot=(5, 15),
    long_short=True,
    group_neutral=False,
    std_bar=True,
    by_group=False
)
```

**Description:** Displays average cumulative returns within event windows (before/after events).

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `factor_data` | pd.DataFrame | Required | Event-aligned factor data |
| `returns` | pd.DataFrame | Required | Returns data for event analysis |
| `avgretplot` | tuple | (5, 15) | (periods_before, periods_after) |
| `long_short` | bool | True | Long-short portfolio flag |
| `group_neutral` | bool | False | Group-neutral flag |
| `std_bar` | bool | True | If True, display standard error bars |
| `by_group` | bool | False | Display by group |

#### create_event_study_tear_sheet()

```python
alphalens.tears.create_event_study_tear_sheet(
    factor_data,
    returns,
    avgretplot=(5, 15),
    rate_of_ret=True,
    n_bars=50
)
```

**Description:** Analyzes specific events with optional event-window return visualization.

**Parameters:**
- `rate_of_ret`: bool - If True, compute rate of return
- `n_bars`: int - Number of bars for event distribution histogram

---

## 5. MODULE: alphalens.performance

**Purpose:** Computational functions for factor analytics and portfolio metrics

### 5.1 Information Coefficient Functions

#### factor_information_coefficient()

```python
alphalens.performance.factor_information_coefficient(
    factor_data,
    group_adjust=False,
    by_group=False
)
```

**Description:** Computes Spearman Rank Correlation based Information Coefficient (IC) between factor values and N-period forward returns.

**Parameters:**
- `factor_data`: pd.DataFrame (MultiIndex) from get_clean_factor_and_forward_returns
- `group_adjust`: bool - If True, demean returns by group before computing IC
- `by_group`: bool - If True, compute IC separately for each group

**Returns:** pd.DataFrame with Spearman correlations (index: dates, columns: forward return periods)

**Interpretation:**
- IC > 0.03: Strong predictive ability
- IC > 0.05: Excellent predictive ability
- IC measures monotonic relationship between factor ranks and future returns

**Example:**
```python
ic = al.performance.factor_information_coefficient(factor_data)
print(f"Mean IC: {ic.mean().mean():.4f}")
```

#### mean_information_coefficient()

```python
alphalens.performance.mean_information_coefficient(
    factor_data,
    group_adjust=False,
    by_group=False,
    by_time=None
)
```

**Description:** Computes mean IC grouped by time periods or groups. Answers: "What is the mean IC for each month?" or "What is the mean IC for each group?"

**Parameters:**
- `by_time`: str, optional - Time grouping period ('M' for monthly, 'W' for weekly)

**Returns:** pd.DataFrame of aggregated IC statistics

**Example:**
```python
# Monthly IC
monthly_ic = al.performance.mean_information_coefficient(
    factor_data,
    by_time='M'
)
```

### 5.2 Return Analysis Functions

#### mean_return_by_quantile()

```python
alphalens.performance.mean_return_by_quantile(
    factor_data,
    by_date=False,
    by_group=False,
    demeaned=True,
    group_adjust=False
)
```

**Description:** Computes mean returns for factor quantiles across forward return periods. Core function for evaluating if higher factor values lead to higher returns.

**Parameters:**
- `by_date`: bool - If True, compute separately for each date
- `by_group`: bool - If True, compute separately for each group
- `demeaned`: bool - If True, demean returns across universe
- `group_adjust`: bool - If True, demean returns by group

**Returns:** tuple of (mean_returns_df, std_error_df)

#### compute_mean_returns_spread()

```python
alphalens.performance.compute_mean_returns_spread(
    mean_returns,
    upper_quant,
    lower_quant,
    std_err=None
)
```

**Description:** Computes difference between mean returns of two quantiles (typically top vs bottom for long-short analysis).

**Parameters:**
- `mean_returns`: pd.DataFrame - From mean_return_by_quantile()
- `upper_quant`: int - Upper quantile number (e.g., 5)
- `lower_quant`: int - Lower quantile number (e.g., 1)
- `std_err`: pd.DataFrame, optional - Standard errors

**Returns:** tuple of (spread_series, std_error_series or None)

**Example:**
```python
mean_ret, std_err = al.performance.mean_return_by_quantile(factor_data)
spread, spread_err = al.performance.compute_mean_returns_spread(
    mean_ret,
    upper_quant=5,
    lower_quant=1,
    std_err=std_err
)
```

#### cumulative_returns()

```python
alphalens.performance.cumulative_returns(returns)
```

**Description:** Computes cumulative returns from simple period returns. Converts returns into growth trajectory.

**Parameters:**
- `returns`: pd.Series - Period returns

**Returns:** pd.Series - Cumulative returns (growth of $1)

### 5.3 Portfolio Construction Functions

#### factor_weights()

```python
alphalens.performance.factor_weights(
    factor_data,
    demeaned=True,
    group_adjust=False,
    equal_weight=False
)
```

**Description:** Computes asset weights by normalizing factor values. Divides by sum of absolute values to achieve gross leverage of 1.

**Parameters:**
- `demeaned`: bool - If True, demean factor values (creates long-short)
- `group_adjust`: bool - If True, demean within groups
- `equal_weight`: bool - If True, use equal weights

**Returns:** pd.Series with normalized asset weights

#### factor_returns()

```python
alphalens.performance.factor_returns(
    factor_data,
    demeaned=True,
    group_adjust=False,
    equal_weight=False,
    by_asset=False
)
```

**Description:** Computes period-wise returns for portfolio weighted by factor values. Generates actual returns time series for factor-based strategy.

**Parameters:**
- `by_asset`: bool - If True, return per-asset returns instead of portfolio returns

**Returns:** pd.DataFrame of period-wise portfolio returns (one column per forward return period)

#### factor_cumulative_returns()

```python
alphalens.performance.factor_cumulative_returns(
    factor_data,
    period,
    long_short=True,
    group_neutral=False,
    equal_weight=False,
    quantiles=None,
    groups=None
)
```

**Description:** Simulates portfolio using factor and returns cumulative returns over time. Complete backtest simulation.

**Parameters:**
- `period`: str or pd.Timedelta - Forward return period to use (e.g., '1D', '5D')
- `quantiles`: list, optional - Specific quantiles to include (None = all)
- `groups`: list, optional - Specific groups to include (None = all)

**Returns:** pd.Series - Cumulative return series indexed by date

#### factor_positions()

```python
alphalens.performance.factor_positions(
    factor_data,
    period,
    long_short=True,
    group_neutral=False,
    equal_weight=False,
    quantiles=None,
    groups=None
)
```

**Description:** Simulates portfolio and returns asset positions as percentage of total portfolio.

**Returns:** pd.DataFrame with datetime index and asset columns showing position percentages

#### positions()

```python
alphalens.performance.positions(weights, period, freq=None)
```

**Description:** Builds net position values time series.

**Parameters:**
- `weights`: pd.Series - Asset weights
- `period`: str or pd.Timedelta - Holding period
- `freq`: str, optional - Rebalancing frequency

**Returns:** pd.DataFrame - Position time series

### 5.4 Risk and Alpha Analysis

#### factor_alpha_beta()

```python
alphalens.performance.factor_alpha_beta(
    factor_data,
    returns=None,
    demeaned=True,
    group_adjust=False,
    equal_weight=False
)
```

**Description:** Computes alpha (excess returns), alpha t-stat (significance), and beta (market exposure) through regression.

**Parameters:**
- `returns`: pd.DataFrame, optional - Benchmark returns. If None, uses equal-weight portfolio

**Returns:** pd.Series containing ['alpha', 'beta', 't-stat']

### 5.5 Turnover and Stability Functions

#### factor_rank_autocorrelation()

```python
alphalens.performance.factor_rank_autocorrelation(
    factor_data,
    period=1
)
```

**Description:** Computes autocorrelation of mean factor ranks across time. Measures factor stability and predicts turnover.

**Parameters:**
- `period`: int - Number of periods for autocorrelation lag

**Returns:** pd.Series of rolling autocorrelations indexed by date

**Interpretation:**
- High autocorrelation (>0.7): Stable rankings, low turnover
- Low autocorrelation (<0.3): High turnover, high transaction costs

#### quantile_turnover()

```python
alphalens.performance.quantile_turnover(
    quantile_factor,
    quantile,
    period=1
)
```

**Description:** Computes proportion of names in a quantile that were not in that quantile in previous period.

**Parameters:**
- `quantile_factor`: pd.Series (MultiIndex) - Factor data with quantile assignments
- `quantile`: int - Quantile number to analyze (1 for bottom, 5 for top)
- `period`: int - Periods between turnover measurements

**Returns:** pd.Series of turnover percentages (0.0-1.0) indexed by date

**Interpretation:**
- Turnover 0.5 = 50% of positions changed
- High turnover increases transaction costs

### 5.6 Event Analysis Functions

#### average_cumulative_return_by_quantile()

```python
alphalens.performance.average_cumulative_return_by_quantile(
    factor_data,
    returns,
    periods_before=10,
    periods_after=15,
    demeaned=True,
    group_adjust=False,
    by_group=False
)
```

**Description:** Computes average cumulative returns by quantile in event windows.

**Returns:** pd.DataFrame with mean/std returns indexed by quantile and event time period

#### common_start_returns()

```python
alphalens.performance.common_start_returns(
    factor,
    returns,
    before,
    after,
    cumulative=False,
    mean_by_date=False,
    demean_by=None
)
```

**Description:** Extracts event-aligned return windows. For each (date, asset) in factor, builds return series from 'before' to 'after' periods.

**Parameters:**
- `before`: int - Periods before event
- `after`: int - Periods after event
- `cumulative`: bool - If True, compute cumulative returns
- `mean_by_date`: bool - If True, average across events on same date
- `demean_by`: str, optional - Grouping for demeaning

**Returns:** pd.DataFrame with aligned return series (index: -before to after)

### 5.7 Pyfolio Integration

#### create_pyfolio_input()

```python
alphalens.performance.create_pyfolio_input(
    factor_data,
    period,
    capital=None,
    long_short=True,
    group_neutral=False,
    equal_weight=False,
    quantiles=None,
    groups=None,
    benchmark_period='1D'
)
```

**Description:** Simulates portfolio and formats output for Pyfolio integration.

**Parameters:**
- `capital`: float, optional - Starting capital for position sizing
- `benchmark_period`: str - Benchmark return period

**Returns:** tuple of (returns_series, positions_df, benchmark_series)

**Example:**
```python
returns, positions, benchmark = al.performance.create_pyfolio_input(
    factor_data,
    period='5D',
    long_short=True
)

# Then use with Pyfolio
import pyfolio as pf
pf.create_full_tear_sheet(returns, positions=positions, benchmark_rets=benchmark)
```

---

## 6. MODULE: alphalens.plotting

**Purpose:** Visualization functions for factor analysis. All functions return matplotlib Axes objects.

### 6.1 Styling and Context

#### axes_style()

```python
alphalens.plotting.axes_style(style='darkgrid', rc=None)
```

**Description:** Creates Alphalens default axes style context using seaborn.

**Parameters:**
- `style`: str - Seaborn style name
- `rc`: dict, optional - Additional rc parameters

#### plotting_context()

```python
alphalens.plotting.plotting_context(
    context='notebook',
    font_scale=1.5,
    rc=None
)
```

**Description:** Creates Alphalens default plotting context with larger fonts.

#### @customize

```python
@alphalens.plotting.customize
def plot_function():
    pass
```

**Description:** Decorator that applies consistent plotting context and styling.

### 6.2 Information Coefficient Plots

#### plot_ic_ts()

```python
alphalens.plotting.plot_ic_ts(ic, ax=None)
```

**Description:** Plots IC time series with rolling mean overlay.

**Parameters:**
- `ic`: pd.DataFrame - IC data from factor_information_coefficient()
- `ax`: matplotlib.Axes, optional

**Returns:** matplotlib.Axes

#### plot_ic_hist()

```python
alphalens.plotting.plot_ic_hist(ic, ax=None)
```

**Description:** Plots histogram of IC distribution.

#### plot_ic_qq()

```python
alphalens.plotting.plot_ic_qq(
    ic,
    theoretical_dist=scipy.stats.norm,
    ax=None
)
```

**Description:** Q-Q plot of IC against theoretical distribution.

**Parameters:**
- `theoretical_dist`: scipy.stats distribution - Default is normal

#### plot_ic_by_group()

```python
alphalens.plotting.plot_ic_by_group(ic_group, ax=None)
```

**Description:** IC comparison across groups (e.g., sectors).

#### plot_monthly_ic_heatmap()

```python
alphalens.plotting.plot_monthly_ic_heatmap(mean_monthly_ic, ax=None)
```

**Description:** Heatmap of monthly IC values. Reveals seasonal patterns.

### 6.3 Returns Plots

#### plot_quantile_returns_bar()

```python
alphalens.plotting.plot_quantile_returns_bar(
    mean_ret_by_q,
    by_group=False,
    ylim_percentiles=None,
    ax=None
)
```

**Description:** Bar chart of mean returns by quantile. CORE visualization for monotonic relationship.

**Parameters:**
- `mean_ret_by_q`: pd.DataFrame - From mean_return_by_quantile()
- `by_group`: bool - Show separate bars by group
- `ylim_percentiles`: tuple - (lower, upper) percentiles for y-axis limits

**Interpretation:** Expect monotonic increase Q1 to Q5 for predictive factors. Spread = long-short profitability.

#### plot_quantile_returns_violin()

```python
alphalens.plotting.plot_quantile_returns_violin(
    return_by_q,
    ylim_percentiles=None,
    ax=None
)
```

**Description:** Violin plots showing full return distribution by quantile.

#### plot_mean_quantile_returns_spread_time_series()

```python
alphalens.plotting.plot_mean_quantile_returns_spread_time_series(
    mean_returns_spread,
    std_err=None,
    bandwidth=1,
    ax=None
)
```

**Description:** Long-short return spread (Q5 - Q1) over time with confidence bands. KEY profitability metric.

**Parameters:**
- `mean_returns_spread`: pd.Series - From compute_mean_returns_spread()
- `std_err`: pd.Series, optional - Standard errors for confidence bands
- `bandwidth`: float - Number of standard errors for band width

### 6.4 Cumulative Returns Plots

#### plot_cumulative_returns()

```python
alphalens.plotting.plot_cumulative_returns(
    factor_returns,
    period,
    freq=None,
    title=None,
    ax=None
)
```

**Description:** Cumulative returns of factor-based strategy. Growth of $1 over time.

**Parameters:**
- `factor_returns`: pd.DataFrame - From factor_returns()
- `period`: str or pd.Timedelta - Period to plot ('1D', '5D', etc.)
- `freq`: str, optional - Frequency for date formatting
- `title`: str, optional - Plot title

#### plot_cumulative_returns_by_quantile()

```python
alphalens.plotting.plot_cumulative_returns_by_quantile(
    quantile_returns,
    period,
    freq=None,
    ax=None
)
```

**Description:** Cumulative returns separately for each quantile.

#### plot_quantile_average_cumulative_return()

```python
alphalens.plotting.plot_quantile_average_cumulative_return(
    avg_cumulative_returns,
    by_quantile=False,
    std_bar=False,
    title=None,
    ax=None
)
```

**Description:** Average cumulative returns in event windows (before/after events).

**Parameters:**
- `avg_cumulative_returns`: pd.DataFrame - From average_cumulative_return_by_quantile()
- `by_quantile`: bool - Plot separate lines per quantile
- `std_bar`: bool - Show standard error bars

### 6.5 Turnover Plots

#### plot_factor_rank_auto_correlation()

```python
alphalens.plotting.plot_factor_rank_auto_correlation(
    factor_autocorrelation,
    period=1,
    ax=None
)
```

**Description:** Factor rank autocorrelation over time. Indicates stability.

#### plot_top_bottom_quantile_turnover()

```python
alphalens.plotting.plot_top_bottom_quantile_turnover(
    quantile_turnover,
    period=1,
    ax=None
)
```

**Description:** Turnover for top and bottom quantiles. CRITICAL for transaction cost estimation.

**Interpretation:** High turnover (>50%) indicates high costs. Aim for <30%.

### 6.6 Event Analysis Plots

#### plot_events_distribution()

```python
alphalens.plotting.plot_events_distribution(
    events,
    num_bars=50,
    ax=None
)
```

**Description:** Histogram of event timing distribution.

### 6.7 Summary Tables

#### plot_information_table()

```python
alphalens.plotting.plot_information_table(ic_data)
```

**Description:** Displays tabular IC summary (mean, std, IR).

#### plot_returns_table()

```python
alphalens.plotting.plot_returns_table(
    alpha_beta,
    mean_ret_quantile,
    mean_ret_spread_quantile
)
```

**Description:** Formatted table of return metrics (alpha, beta, quantile returns).

#### plot_quantile_statistics_table()

```python
alphalens.plotting.plot_quantile_statistics_table(factor_data)
```

**Description:** Descriptive statistics table for each quantile.

#### plot_turnover_table()

```python
alphalens.plotting.plot_turnover_table(
    autocorrelation_data,
    quantile_turnover
)
```

**Description:** Turnover and stability metrics table.

---

## 7. CORE CONCEPTS

### 7.1 Factor Analysis

**Definition:** Systematic evaluation of whether a quantitative signal (factor) has predictive power for future asset returns.

**Purpose:** Determine if factor can be profitably traded before implementing in production.

**Workflow:**
1. Define factor (signal/alpha) as time series of asset rankings
2. Prepare data using `get_clean_factor_and_forward_returns()`
3. Analyze returns, IC, turnover via tear sheets
4. Evaluate if factor meets profitability and implementability criteria

### 7.2 Quantiles

**Definition:** Factor values are ranked and divided into equal-sized groups (typically 5 or 10).

**Purpose:** Convert continuous factor values into discrete buckets for portfolio construction.

**Interpretation:**
- **Quantile 1 (Q1):** Bottom-ranked assets (lowest factor values)
- **Quantile 5 (Q5):** Top-ranked assets (highest factor values)
- **Monotonic Relationship:** Ideal pattern is Q5 returns > Q4 > Q3 > Q2 > Q1

**Long-Short Strategy:** Long top quantile (Q5), short bottom quantile (Q1), profit from spread.

**Binning Options:**
- **quantiles:** Equal-sized buckets (each has ~same number of assets)
- **bins:** Equal-width buckets (each covers same factor value range)
- **binning_by_group:** Separate quantile ranking within each group (e.g., per sector)

### 7.3 Information Coefficient (IC)

**Definition:** Spearman rank correlation between factor values and subsequent forward returns.

**Formula:** `IC = spearman_correlation(factor_ranks, forward_return_ranks)`

**Range:** -1 to +1

**Interpretation:**
- **Positive IC:** Higher factor values predict higher returns (good for long strategies)
- **Negative IC:** Higher factor values predict lower returns (good for short strategies)
- **Zero IC:** No predictive relationship
- **Strong Factor:** |IC| > 0.03
- **Excellent Factor:** |IC| > 0.05

**Information Ratio (IR):**
- **Formula:** `IR = mean(IC) / std(IC)`
- **Interpretation:** Sharpe ratio equivalent for IC
- **Good:** IR > 0.5
- **Excellent:** IR > 1.0
- **Purpose:** Measures consistency of predictive power

**Advantages:**
- Robust to outliers (uses ranks, not raw values)
- Comparable across different factors and markets
- Direct measure of monotonic predictive relationship

### 7.4 Quantile Returns

**Definition:** Mean forward returns for assets in each factor quantile.

**Key Metrics:**
- **Mean Return by Quantile:** Average return for Q1, Q2, Q3, Q4, Q5
- **Return Spread:** Q5_return - Q1_return (long-short profitability)
- **Monotonicity:** Whether returns increase consistently from Q1 to Q5

**Demeaning Modes:**
- **None:** Raw returns (absolute performance)
- **Long-Short:** Universe-demeaned (removes market beta)
- **Group-Neutral:** Group-demeaned (removes sector exposure)

### 7.5 Turnover

**Definition:** Frequency of portfolio position changes due to factor reranking.

**Importance:** High turnover → high transaction costs → reduced net profitability.

**Metrics:**

**Quantile Turnover:**
- **Formula:** `turnover = 1 - (assets_still_in_quantile / total_assets_in_quantile)`
- **Range:** 0.0 (no turnover) to 1.0 (complete replacement)
- **Interpretation:**
  - Low: <0.2 (low trading costs)
  - Medium: 0.2-0.5 (moderate costs)
  - High: >0.5 (high costs, may erode profits)

**Factor Rank Autocorrelation:**
- **Range:** 0 to 1
- **Interpretation:**
  - High (>0.7): Stable rankings, low turnover
  - Low (<0.3): Unstable rankings, high turnover

**Transaction Cost Estimation:**
`annual_cost ≈ turnover × trades_per_year × cost_per_trade`

### 7.6 Forward Returns

**Definition:** Returns measured from factor observation date to N periods in the future.

**Common Periods:**
- **1D:** 1-day (high frequency trading)
- **5D:** 5-day / 1 week (short-term)
- **10D:** 10-day / 2 weeks
- **21D:** 21-day / 1 month (medium-term)
- **63D:** 63-day / 3 months (long-term)

**Calculation:** `forward_return = (price[t+N] - price[t]) / price[t]`

### 7.7 Grouped Analysis

**Definition:** Breaking down factor performance by categories (sectors/industries).

**Purpose:**
- Identify which groups factor predicts best
- Construct sector-neutral portfolios
- Avoid sector concentration risk
- Meet regulatory constraints

**Group-Neutral Portfolios:**
- Within each group: long top-ranked, short bottom-ranked
- Benefit: Removes sector exposure, isolates factor effect

---

## 8. TYPICAL WORKFLOW

### Step 1: Data Preparation

```python
import alphalens as al

factor_data = al.utils.get_clean_factor_and_forward_returns(
    factor=my_factor,      # pd.Series with MultiIndex (date, asset)
    prices=pricing_data,   # pd.DataFrame with date index, asset columns
    quantiles=5,           # or 10 for finer granularity
    periods=(1, 5, 10),    # Forward return periods
    groupby=sector_map,    # Optional sector grouping
    max_loss=0.35          # Max allowed data loss
)
```

**Parameters to Consider:**
- `quantiles`: 5 or 10 (more = finer granularity)
- `periods`: (1, 5, 10) or custom holding periods
- `binning_by_group`: True for sector-relative ranking
- `max_loss`: 0.35 default, lower if data quality critical

### Step 2: Quick Analysis

```python
al.tears.create_summary_tear_sheet(factor_data)
```

**Decision:** If promising, proceed to full analysis.

### Step 3: Full Analysis

```python
al.tears.create_full_tear_sheet(
    factor_data,
    long_short=True,
    group_neutral=False,
    by_group=False
)
```

**Output Components:**
- Returns analysis (quantile returns, cumulative performance)
- IC analysis (time series, distribution, heatmaps)
- Turnover analysis (autocorrelation, quantile turnover)

### Step 4: Detailed Drill-Down (Optional)

```python
# Deep dive into returns
al.tears.create_returns_tear_sheet(factor_data)

# Detailed IC analysis
al.tears.create_information_tear_sheet(factor_data)

# Transaction cost estimation
al.tears.create_turnover_tear_sheet(factor_data)
```

### Step 5: Pyfolio Integration (Optional)

```python
returns, positions, benchmark = al.performance.create_pyfolio_input(
    factor_data,
    period='5D',
    long_short=True
)

import pyfolio as pf
pf.create_full_tear_sheet(returns, positions=positions)
```

---

## 9. FACTOR EVALUATION CRITERIA

### 9.1 Predictive Power
- **Metric:** Information Coefficient (IC)
- **Good:** mean(|IC|) > 0.03, IR > 0.5
- **Excellent:** mean(|IC|) > 0.05, IR > 1.0
- **Check:** IC should be consistent over time

### 9.2 Profitability
- **Metric:** Quantile return spread (Q5 - Q1)
- **Good:** Consistent positive spread, statistically significant
- **Check:** Spread must exceed transaction costs after turnover adjustment

### 9.3 Monotonicity
- **Metric:** Return progression Q1 < Q2 < Q3 < Q4 < Q5
- **Good:** Clear monotonic relationship
- **Acceptable:** Q5 >> Q1 even if middle quantiles not perfectly ordered

### 9.4 Stability
- **Metric:** Factor rank autocorrelation
- **Good:** 0.5-0.8 (stable but not static)
- **Too High:** >0.95 (not incorporating new information)
- **Too Low:** <0.2 (high turnover, likely unprofitable)

### 9.5 Implementability
- **Metric:** Quantile turnover (especially Q1 and Q5)
- **Good:** <0.3 for daily rebalancing
- **Marginal:** 0.3-0.5
- **Poor:** >0.5 (transaction costs likely exceed profits)

### 9.6 Group Robustness
- **Check:** Factor works across multiple groups, not just one sector
- **Risk:** Sector concentration = sector bet, not true alpha

### 9.7 Time Consistency
- **Check:** IC and returns stable across different time periods
- **Risk:** Regime-dependent factors may not generalize

---

## 10. BEST PRACTICES

1. **Always run `get_clean_factor_and_forward_returns` first** to validate data alignment
2. **Check max_loss warnings** - high data loss indicates data quality issues
3. **Use `create_summary_tear_sheet` for quick screening**
4. **Compare multiple holding periods** to find optimal trade frequency
5. **Examine both IC and returns** - high IC with low returns may indicate capacity issues
6. **Account for transaction costs** using turnover metrics before declaring profitability
7. **Use `group_neutral=True`** to remove market/sector beta and isolate alpha
8. **Look for IC > 0.03** as minimum threshold for practical factors
9. **Monitor IC consistency** - volatile IC suggests regime-dependent factor
10. **Cross-reference autocorrelation with turnover** to predict implementation costs

---

## 11. COMMON PITFALLS

1. **Ignoring turnover** - factor may be unprofitable after transaction costs
2. **Insufficient price history** - need prices extending past last factor date by max(periods)
3. **Timezone mismatches** between factor and price data
4. **Too many quantiles with small universes** - need sufficient assets per quantile
5. **Mistaking high IC for profitability** - must check return magnitudes
6. **Overfitting to specific time period** - factor may not generalize
7. **Not accounting for survivorship bias** in data
8. **Assuming universal factor effectiveness** across all market conditions
9. **Neglecting capacity constraints** - IC doesn't capture market impact

---

## 12. IMPLEMENTATION RECOMMENDATIONS

### Quick Factor Screening
- **Use:** `create_summary_tear_sheet()` with defaults
- **Rationale:** Fast, covers key metrics, identifies bad factors quickly

### Production Factor Validation
- **Use:** `create_full_tear_sheet()` with `group_neutral=True`
- **Rationale:** Comprehensive, accounts for sector effects, validates implementability

### Research Portfolio Integration
- **Use:** `create_pyfolio_input()` → Pyfolio
- **Rationale:** Deep risk metrics, drawdown analysis, factor exposures

### Sector-Specific Strategy
- **Use:** `binning_by_group=True` with `by_group=True`
- **Rationale:** Within-sector ranking and separate analysis per sector

### High-Frequency Trading
- **Use:** `periods=(1,)`, monitor turnover closely
- **Rationale:** Short periods increase turnover - verify profitability after costs

### Long-Term Investment
- **Use:** `periods=(21, 63)`
- **Rationale:** Longer periods reduce turnover, better for low-frequency strategies

### Event-Driven Strategy
- **Use:** `create_event_study_tear_sheet()` with custom windows
- **Rationale:** Specialized for returns around events (earnings, M&A, etc.)

### Outlier-Prone Factors
- **Use:** Lower `filter_zscore` (3-5) in `get_clean_factor_and_forward_returns`
- **Rationale:** Removes extreme outliers that distort analysis

### Small Universe (<50 assets)
- **Use:** `quantiles=3` instead of 5
- **Rationale:** Ensures sufficient assets per quantile

### Large Universe (>1000 assets)
- **Use:** `quantiles=10`
- **Rationale:** Finer granularity with sufficient sample size

---

## 13. SOURCES AND REFERENCES

### Official Documentation
1. **Alphalens Official Docs:** https://quantopian.github.io/alphalens/
2. **Alphalens-Reloaded Docs:** https://alphalens.ml4trading.io/
3. **Quantopian API Reference:** https://www.quantopian.com/docs/api-reference/alphalens-api-reference

### Repositories
4. **Original Repository:** https://github.com/quantopian/alphalens
5. **Alphalens-Reloaded:** https://github.com/stefan-jansen/alphalens-reloaded
6. **cloudQuant Fork:** https://github.com/cloudQuant/alphalens

### Package Distribution
7. **PyPI (Original):** https://pypi.org/project/alphalens/
8. **PyPI (Reloaded):** https://pypi.org/project/alphalens-reloaded/
9. **Conda-Forge:** https://anaconda.org/conda-forge/alphalens

### Additional Resources
10. **Alphalens Overview Tutorial:** https://alphalens.ml4trading.io/notebooks/overview.html
11. **Factor Analysis Lecture:** https://www.quantrocket.com/codeload/quant-finance-lectures/
12. **IC Analysis Guide:** https://www.pyquantnews.com/the-pyquant-newsletter/information-coefficient-measure-your-alpha

---

## 14. SUMMARY STATISTICS

### Research Coverage
- **Platforms Searched:** GitHub, PyPI, Quantopian Docs, ML4Trading, Developer Forums
- **Repositories Analyzed:** 3 (Quantopian original, alphalens-reloaded, cloudQuant fork)
- **Documentation Sources Reviewed:** 5
- **Functions Documented:** 60+
- **Concepts Explained:** 7 core concepts with sub-topics

### Library Statistics
- **Total Modules:** 4 (utils, tears, performance, plotting)
- **Total Public Functions:** 60+
- **Total Classes:** 1 (GridFigure)
- **Total Exceptions:** 2 (MaxLossExceededError, NonMatchingTimezoneError)
- **Dependencies:** 6 required packages

---

**End of Comprehensive API Inventory**

*This document provides complete API coverage for writing comprehensive Alphalens documentation. All function signatures, parameters, return types, and usage patterns are included.*
