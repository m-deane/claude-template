# Pyfolio Python Library - Comprehensive API Inventory

**Research Date:** 2025-12-17
**Status:** Complete comprehensive analysis of pyfolio and pyfolio-reloaded

---

## Executive Summary

**Pyfolio** is a Python library for performance and risk analysis of financial portfolios, originally developed by Quantopian Inc. The library generates comprehensive "tear sheets" - multi-panel visualizations combining plots and statistics for portfolio analysis.

### Current Status

- **Original pyfolio**: Version 0.9.2 (April 2019) - ARCHIVED/UNMAINTAINED
- **pyfolio-reloaded**: Version 0.9.9 (June 2025) - ACTIVELY MAINTAINED ✓

**Recommendation:** Use **pyfolio-reloaded** for all new projects (Python 3.9-3.13 support)

---

## Installation

### Recommended (pyfolio-reloaded)
```bash
pip install pyfolio-reloaded
# or
conda install -c ml4t pyfolio-reloaded
```

### Original (not recommended)
```bash
pip install pyfolio  # Only for legacy projects
```

---

## Module Structure

### Core Modules (8 primary modules)

1. **pyfolio.tears** - Tear sheet generation (comprehensive reports)
2. **pyfolio.timeseries** - Performance metrics and time series analysis
3. **pyfolio.plotting** - Visualization functions
4. **pyfolio.perf_attrib** - Performance attribution analysis
5. **pyfolio.utils** - Utility and helper functions
6. **pyfolio.pos** - Position tracking and analysis
7. **pyfolio.txn** - Transaction handling
8. **pyfolio.round_trips** - Round-trip trade analysis
9. **pyfolio.capacity** - Capacity and liquidity analysis
10. **pyfolio.interesting_periods** - Historical market event data

---

## Key Tear Sheet Functions

### 1. create_full_tear_sheet()
**Priority: CRITICAL** - Main entry point for comprehensive analysis

```python
pyfolio.create_full_tear_sheet(
    returns,                    # pd.Series - Daily returns (required)
    positions=None,             # pd.DataFrame - Daily position values
    transactions=None,          # pd.DataFrame - Trade data
    market_data=None,           # pd.DataFrame - OHLCV data
    benchmark_rets=None,        # pd.Series - Benchmark returns
    slippage=None,              # int/float - Slippage in bps
    live_start_date=None,       # date - Out-of-sample period start
    sector_mappings=None,       # dict/Series - Symbol to sector
    round_trips=False,          # bool - Include round trip analysis
    estimate_intraday='infer',  # str/bool - Detect intraday strategies
    hide_positions=False,       # bool - Hide position details
    cone_std=(1.0, 1.5, 2.0),  # tuple - Cone standard deviations
    bootstrap=False,            # bool - Bootstrap analysis
    turnover_denom='AGB',       # str - 'AGB' or 'portfolio_value'
    factor_returns=None,        # pd.DataFrame - Factor returns
    factor_loadings=None,       # pd.DataFrame - Factor loadings
    pos_in_dollars=True,        # bool - Positions in $ vs shares
    return_fig=False            # bool - Return figure object
)
```

**Generates:**
- Returns analysis (cumulative, rolling, distributions)
- Risk metrics (volatility, drawdowns, Sharpe ratio)
- Position analysis (holdings, leverage, exposures)
- Transaction analysis (turnover, volume)
- Optional: Round trips, factor attribution, Bayesian analysis

---

### 2. create_returns_tear_sheet()
**Priority: HIGH** - Focus on return metrics

```python
pyfolio.create_returns_tear_sheet(
    returns,
    positions=None,
    transactions=None,
    live_start_date=None,
    cone_std=(1.0, 1.5, 2.0),
    benchmark_rets=None,
    bootstrap=False,
    turnover_denom='AGB',
    header_rows=None,
    return_fig=False
)
```

**Generates:**
- Cumulative returns plot
- Rolling metrics (Sharpe, beta, volatility)
- Drawdown analysis
- Monthly/annual return breakdowns
- Return distributions

---

### 3. create_position_tear_sheet()
**Priority: HIGH** - Portfolio holdings analysis

```python
pyfolio.create_position_tear_sheet(
    returns,
    positions,
    show_and_plot_top_pos=2,
    hide_positions=False,
    sector_mappings=None,
    transactions=None,
    estimate_intraday='infer',
    return_fig=False
)
```

**Generates:**
- Top positions table and plot
- Long/short exposure
- Gross leverage
- Position concentration
- Holdings count over time
- Sector allocations (if mappings provided)

---

### 4. create_txn_tear_sheet()
**Priority: MEDIUM** - Transaction analysis

```python
pyfolio.create_txn_tear_sheet(
    returns,
    positions,
    transactions,
    turnover_denom='AGB',
    unadjusted_returns=None,
    estimate_intraday='infer',
    return_fig=False
)
```

**Generates:**
- Turnover time series
- Daily volume analysis
- Transaction time distribution
- Slippage sensitivity

---

### 5. create_round_trip_tear_sheet()
**Priority: MEDIUM** - Trade cycle analysis

```python
pyfolio.create_round_trip_tear_sheet(
    returns,
    positions,
    transactions,
    sector_mappings=None,
    estimate_intraday='infer',
    return_fig=False
)
```

**Round Trip Definition:** Complete trade from opening position to returning to zero shares

**Generates:**
- Round trip statistics (PnL, duration, returns)
- Trade lifetime plots
- Probability of profit distribution
- Win rate analysis
- Long vs short performance

---

### 6. create_capacity_tear_sheet()
**Priority: MEDIUM** - Liquidity and scalability

```python
pyfolio.create_capacity_tear_sheet(
    returns,
    positions,
    transactions,
    market_data,                      # Required!
    liquidation_daily_vol_limit=0.2,
    trade_daily_vol_limit=0.05,
    last_n_days=126,
    days_to_liquidate_limit=1,
    estimate_intraday='infer',
    return_fig=False
)
```

**Generates:**
- Capacity sweep (Sharpe vs capital size)
- Days to liquidate analysis
- Low liquidity transactions
- Market impact estimates

---

### 7. create_perf_attrib_tear_sheet()
**Priority: MEDIUM** - Factor attribution

```python
pyfolio.create_perf_attrib_tear_sheet(
    returns,
    positions,
    factor_returns,      # Required!
    factor_loadings,     # Required!
    transactions=None,
    pos_in_dollars=True,
    factor_partitions={},
    return_fig=False
)
```

**Generates:**
- Common returns (factor-explained)
- Specific returns (alpha)
- Factor contribution plots
- Risk exposure time series
- Attribution statistics

---

### 8. create_simple_tear_sheet()
**Priority: MEDIUM** - Quick overview

```python
pyfolio.create_simple_tear_sheet(
    returns,
    positions=None,
    transactions=None,
    benchmark_rets=None,
    slippage=None,
    estimate_intraday='infer',
    live_start_date=None,
    turnover_denom='AGB',
    header_rows=None
)
```

Simplified version for quick analysis without extensive data requirements.

---

### 9. create_bayesian_tear_sheet()
**Priority: LOW** - Uncertainty quantification

```python
pyfolio.create_bayesian_tear_sheet(
    returns,
    live_start_date=None,
    samples=2000,
    ...
)
```

**Requirements:** PyMC3, Theano
**Note:** Computationally intensive (MCMC sampling)

**Generates:**
- Bayesian cone (probabilistic forecast)
- Parameter posteriors (distributions, not point estimates)
- In-sample vs out-of-sample comparison with uncertainty

---

## Critical Timeseries Functions

### Performance Metrics

#### annual_return(returns, period='daily')
Calculates CAGR (Compound Annual Growth Rate)

#### annual_volatility(returns, period='daily')
Calculates annualized volatility (standard deviation)

#### sharpe_ratio(returns, risk_free=0, period='daily')
Risk-adjusted return metric
- **Interpretation:** >1 is good, >2 is very good

#### sortino_ratio(returns, required_return=0, period='daily')
Return-to-downside-risk ratio (only penalizes downside volatility)

#### calmar_ratio(returns, period='daily')
Annual return / Maximum drawdown

#### omega_ratio(returns, annual_return_threshhold=0.0)
Probability-weighted gains / losses ratio

---

### Risk Metrics

#### max_drawdown(returns)
Maximum peak-to-trough decline

#### get_top_drawdowns(returns, top=10)
Returns list of worst drawdown events

#### gen_drawdown_table(returns, top=10)
DataFrame with drawdown details (peak, valley, recovery dates)

#### downside_risk(returns, required_return=0, period='daily')
Downside deviation below target

#### tail_ratio(returns)
Right tail (95%) / left tail (5%) ratio

#### value_at_risk(returns, period=None, sigma=2.0)
Expected loss at confidence level

---

### Benchmark Comparison

#### alpha(returns, factor_returns)
Annualized excess return beyond beta prediction

#### beta(returns, factor_returns)
Sensitivity to benchmark movements

#### alpha_beta(returns, factor_returns)
Returns both alpha and beta simultaneously

#### rolling_beta(returns, factor_returns, rolling_window=126)
Time-varying market sensitivity (default: 6 months)

---

### Statistics & Analysis

#### perf_stats(returns, factor_returns=None, positions=None, transactions=None, turnover_denom='AGB')
**Priority: CRITICAL** - Returns comprehensive performance metrics as pd.Series

Includes: Annual return, volatility, Sharpe, Sortino, Calmar, max drawdown, alpha, beta, and more

#### cum_returns(returns, starting_value=0)
Cumulative returns from simple returns

#### aggregate_returns(returns, convert_to)
Resamples to 'weekly', 'monthly', or 'yearly'

#### gross_lev(positions)
Daily gross leverage (long + short exposure / NAV)

---

### Rolling Metrics

#### rolling_sharpe(returns, rolling_sharpe_window)
Rolling Sharpe ratio

#### rolling_volatility(returns, rolling_vol_window)
Rolling volatility

#### rolling_regression(returns, factor_returns, rolling_window=126, nan_threshold=0.1)
Rolling multivariate regression coefficients

---

### Simulation & Forecasting

#### simulate_paths(is_returns, num_days, starting_value=1, num_samples=1000, random_seed=None)
Generates alternative outcome paths via bootstrapped resampling

#### forecast_cone_bootstrap(is_returns, num_days, cone_std=(1.0, 1.5, 2.0), ...)
Non-parametric probability cone bounds

---

## Key Plotting Functions

### Returns Visualization

- **plot_returns()** - Cumulative returns (green=backtest, red=live)
- **plot_rolling_returns()** - Rolling returns with optional cone overlay
- **plot_annual_returns()** - Bar chart of yearly returns
- **plot_monthly_returns_heatmap()** - Calendar heatmap
- **plot_return_quantiles()** - Box plots of return distributions

### Risk Visualization

- **plot_drawdown_periods()** - Cumulative returns with highlighted drawdowns
- **plot_drawdown_underwater()** - Rolling drawdown depth over time
- **plot_rolling_sharpe()** - Rolling Sharpe ratio
- **plot_rolling_beta()** - Rolling 6-month and 12-month beta
- **plot_rolling_volatility()** - Rolling volatility

### Position Visualization

- **plot_holdings()** - Count of active positions over time
- **plot_long_short_holdings()** - Stacked long/short position count
- **plot_gross_leverage()** - Gross leverage time series
- **plot_exposures()** - Pie chart of long/short exposure
- **plot_sector_allocations()** - Sector exposure time series

### Transaction Visualization

- **plot_turnover()** - Turnover percentage over time
- **plot_daily_volume()** - Daily trading volume
- **plot_daily_turnover_hist()** - Turnover rate histogram
- **plot_txn_time_hist()** - Transaction execution time distribution

### Round Trip Visualization

- **plot_round_trip_lifetimes()** - Trade timespans and directions
- **plot_prob_profit_trade()** - Probability distribution of profitable trades

### Display Functions

- **show_perf_stats()** - Pretty-print performance metrics table
- **show_worst_drawdown_periods()** - Print drawdown details
- **show_and_plot_top_positions()** - Print/plot top holdings

---

## Position Module Functions

#### get_percent_alloc(values)
Computes portfolio allocations as proportions

#### get_top_long_short_abs(positions, top=10)
Returns top long, short, and absolute positions

#### get_max_median_position_concentration(positions)
Max and median position concentrations

#### extract_pos(positions, cash)
Transforms backtest position data to daily net values

#### get_sector_exposures(positions, symbol_sector_map)
Aggregates position exposures by sector

#### get_long_short_pos(positions)
Calculates long and short allocations

---

## Transaction Module Functions

#### get_turnover(positions, transactions, denominator='AGB')
Calculates portfolio turnover
- **'AGB'** - Actual Gross Book (sum of absolute position values)
- **'portfolio_value'** - Net portfolio value

#### get_txn_vol(transactions)
Extracts daily transaction volume and share counts

#### adjust_returns_for_slippage(returns, positions, transactions, slippage_bps)
Applies slippage penalties to returns

---

## Round Trips Module Functions

#### extract_round_trips(transactions, portfolio_value=None)
**Priority: CRITICAL** - Groups transactions into complete trade cycles

Returns DataFrame with columns:
- PnL, returns, duration
- Symbol, open/close dates
- Long/short direction

#### gen_round_trip_stats(round_trips)
Generates comprehensive round trip statistics

#### add_closing_transactions(positions, transactions)
Appends transactions to close all open positions

---

## Performance Attribution Functions

#### perf_attrib(returns, positions, factor_returns, factor_loadings, transactions=None, pos_in_dollars=True)
Attributes returns to risk factors

**Returns:** (perf_attrib_data, risk_exposures)
- Common returns (factor-explained)
- Specific returns (alpha)

#### compute_exposures(positions, factor_loadings, stack_positions=True, pos_in_dollars=True)
Calculates daily risk factor exposures

#### create_perf_attrib_stats(perf_attrib, risk_exposures)
Computes annualized multifactor alpha and Sharpe

---

## Capacity Analysis Functions

#### days_to_liquidate_positions(positions, market_data, max_bar_consumption=0.2, capital_base=1e6, mean_volume_window=5)
Estimates liquidation timeline for positions

#### get_max_days_to_liquidate_by_ticker(...)
Worst-case liquidation duration per ticker

#### get_low_liquidity_transactions(transactions, market_data, last_n_days=None)
Identifies transactions consuming high proportion of volume

#### apply_slippage_penalty(returns, txn_daily, simulate_starting_capital, backtest_starting_capital, impact=0.1)
Applies quadratic volumeshare slippage model

---

## Utility Functions

#### extract_rets_pos_txn_from_zipline(backtest)
**Priority: CRITICAL** - Extracts data from Zipline backtest

**Returns:** (returns, positions, transactions)

#### check_intraday(estimate, returns, positions, transactions)
Detects and processes intraday strategies

#### clip_returns_to_benchmark(rets, benchmark_rets)
Aligns return dates with benchmark

#### print_table(table, name=None, float_format=None, formatters=None, header_rows=None)
Pretty-prints pandas objects (HTML in Jupyter)

---

## Data Structures

### Returns
```python
# pd.Series with DatetimeIndex
returns = pd.Series(
    [0.01, -0.005, 0.02, ...],
    index=pd.DatetimeIndex(['2020-01-02', '2020-01-03', ...])
)
```
**Note:** Simple returns, not log returns!

### Positions
```python
# pd.DataFrame with symbols as columns
positions = pd.DataFrame({
    'AAPL': [10000, 10500, ...],
    'GOOG': [5000, 4800, ...],
    'cash': [1000, 1200, ...]
}, index=pd.DatetimeIndex([...]))
```

### Transactions
```python
# pd.DataFrame with required columns
transactions = pd.DataFrame({
    'symbol': ['AAPL', 'GOOG', ...],
    'amount': [100, -50, ...],      # Positive=buy, Negative=sell
    'price': [150.25, 2800.50, ...],
    'commission': [1.0, 1.0, ...]   # Optional
}, index=pd.DatetimeIndex([...]))
```

### Factor Returns
```python
# pd.DataFrame with factors as columns
factor_returns = pd.DataFrame({
    'Momentum': [0.01, 0.02, ...],
    'Value': [-0.005, 0.01, ...],
    'Size': [0.003, -0.002, ...]
}, index=pd.DatetimeIndex([...]))
```

### Factor Loadings
```python
# pd.DataFrame with symbols as index, factors as columns
factor_loadings = pd.DataFrame({
    'Momentum': [0.8, -0.3, ...],
    'Value': [1.2, 0.5, ...],
    'Size': [-0.2, 0.9, ...]
}, index=['AAPL', 'GOOG', ...])
```

---

## Core Concepts

### Tear Sheets
Comprehensive visual reports combining multiple plots and statistics. Types:
- **Full** - Complete analysis
- **Returns** - Return metrics focus
- **Position** - Holdings analysis
- **Transaction** - Trading costs
- **Round Trip** - Trade cycles
- **Capacity** - Liquidity constraints
- **Performance Attribution** - Factor decomposition
- **Bayesian** - Uncertainty quantification

### Risk-Adjusted Metrics

| Metric | Formula | Good Value |
|--------|---------|------------|
| Sharpe Ratio | (Return - RiskFree) / Volatility | >1 good, >2 very good |
| Sortino Ratio | (Return - Target) / Downside Risk | Higher better |
| Calmar Ratio | Annual Return / Max Drawdown | Higher better |
| Omega Ratio | Prob-weighted gains / losses | >1 good |

### Turnover Denominators

- **AGB (Actual Gross Book)** - Sum of absolute position values (long + short)
- **Portfolio Value** - Net portfolio value

AGB is typically higher and more conservative.

### Round Trips

**Definition:** Complete trade cycle from opening position to returning to zero shares

**Example:**
1. Day 1: Buy 100 shares @ $50
2. Day 5: Buy 50 more @ $52
3. Day 10: Sell 150 shares @ $55
→ One round trip: PnL = $650, Duration = 9 days, Return = 8.8%

---

## Typical Workflows

### 1. Basic Analysis from Zipline
```python
import pyfolio as pf

# Run Zipline backtest
backtest = run_algorithm(...)

# Extract data
returns, positions, transactions = pf.utils.extract_rets_pos_txn_from_zipline(backtest)

# Generate full analysis
pf.create_full_tear_sheet(returns, positions, transactions)
```

### 2. Returns-Only Analysis
```python
import pyfolio as pf

# Get returns and benchmark
returns = get_strategy_returns()
benchmark = pf.utils.get_symbol_rets('SPY')

# Quick analysis
pf.create_simple_tear_sheet(returns, benchmark_rets=benchmark)

# Or more detailed
pf.create_returns_tear_sheet(returns, benchmark_rets=benchmark)
```

### 3. Custom Metric Calculation
```python
import pyfolio as pf

returns = get_returns()

# Calculate individual metrics
sharpe = pf.timeseries.sharpe_ratio(returns)
max_dd = pf.timeseries.max_drawdown(returns)
annual_ret = pf.timeseries.annual_return(returns)
annual_vol = pf.timeseries.annual_volatility(returns)

# Get comprehensive stats
stats = pf.timeseries.perf_stats(returns)
print(stats)
```

### 4. Factor Attribution Analysis
```python
import pyfolio as pf

# Prepare data
returns = get_returns()
positions = get_positions()
factor_returns = get_factor_returns()  # From research platform
factor_loadings = get_factor_loadings()

# Generate attribution analysis
pf.create_perf_attrib_tear_sheet(
    returns, positions, factor_returns, factor_loadings
)
```

### 5. Round Trip Analysis
```python
import pyfolio as pf

returns, positions, transactions = get_backtest_data()

# Generate round trip tear sheet
pf.create_round_trip_tear_sheet(returns, positions, transactions)

# Or extract round trips for custom analysis
round_trips = pf.round_trips.extract_round_trips(
    transactions,
    portfolio_value=positions.sum(axis='columns')
)

# Generate statistics
stats = pf.round_trips.gen_round_trip_stats(round_trips)
```

---

## Best Practices

### Data Preparation
1. Ensure returns are **simple returns**, not log returns
2. Use consistent timezone (UTC recommended)
3. Remove NaN/inf values from returns
4. Verify transactions have required columns
5. Include 'cash' column in positions DataFrame

### Analysis
1. **Always** specify `live_start_date` to separate in-sample from out-of-sample
2. Include benchmark for proper context
3. Use `sector_mappings` for better position analysis
4. Run round trip analysis to understand trade efficiency
5. Check capacity constraints for real-world applicability

### Performance
1. Start with `create_simple_tear_sheet()` for quick overview
2. Use `return_fig=True` to save figures instead of displaying
3. Bootstrap analysis is slow - use sparingly
4. Bayesian analysis requires PyMC3 and is computationally intensive

### Interpretation
1. Look at **risk-adjusted metrics** (Sharpe, Sortino), not just returns
2. Examine drawdown characteristics - recovery time matters
3. Check rolling metrics for stability over time
4. Compare in-sample vs out-of-sample performance
5. Verify results aren't driven by few large positions
6. Consider capacity constraints for live trading
7. Use interesting periods to test in various market conditions

---

## Common Pitfalls

| Issue | Solution |
|-------|----------|
| Using log returns | Convert: `simple_returns = np.exp(log_returns) - 1` |
| Missing cash column | Add cash column to positions DataFrame |
| Timezone mismatches | Convert to UTC: `df.index = df.index.tz_localize('UTC')` |
| Overfitting to in-sample | Always use `live_start_date` parameter |
| Ignoring transaction costs | Include commissions, use slippage parameter |
| Not checking capacity | Run capacity tear sheet for tradeable scale |
| Wrong benchmark | Use appropriate benchmark for strategy type |

---

## Dependencies

### Core Requirements
- ipython >= 3.2.3
- matplotlib >= 1.4.0
- numpy >= 1.11.1
- pandas >= 0.18.1
- pytz >= 2014.10
- scipy >= 0.14.0
- scikit-learn >= 0.16.1
- seaborn >= 0.7.1
- empyrical >= 0.5.0

### Optional
- **PyMC3** and **Theano** - For Bayesian analysis
- **Zipline** - For backtesting integration

---

## Integration Notes

### Zipline Integration
```python
# Primary workflow
backtest = run_algorithm(...)
returns, positions, transactions = pf.utils.extract_rets_pos_txn_from_zipline(backtest)
pf.create_full_tear_sheet(returns, positions, transactions)
```

### Custom Backtesting Frameworks
```python
# Create required data structures
returns = pd.Series([...], index=pd.DatetimeIndex([...]))
positions = pd.DataFrame({...})  # Optional
transactions = pd.DataFrame({...})  # Optional

# Pass to tear sheet function
pf.create_full_tear_sheet(returns, positions, transactions)
```

### Jupyter Notebooks
Pyfolio works best in Jupyter notebooks:
- HTML tables for better formatting
- Inline plots
- Interactive exploration

---

## Alternatives

- **empyrical** - Dependency providing underlying metrics (can use standalone)
- **QuantStats** - Similar portfolio analytics with HTML reports
- **bt** - Alternative backtesting framework
- **Backtrader** - Complete platform with PyFolio analyzer integration

---

## Version Migration: pyfolio → pyfolio-reloaded

### Key Differences
1. **Python Support:** 3.9-3.13 (vs 2.7, 3.4-3.5)
2. **Pandas Compatibility:** Works with Pandas 1.0+ (original has issues)
3. **Active Maintenance:** Regular updates and bug fixes
4. **Modern Packaging:** Uses `src/` layout, pre-commit hooks

### Migration
Most code should work without changes:
```python
# Before
import pyfolio as pf

# After (same import, different package)
pip install pyfolio-reloaded
import pyfolio as pf
```

---

## Research Sources

1. [Quantopian/pyfolio GitHub Repository](https://github.com/quantopian/pyfolio)
2. [Stefan Jansen/pyfolio-reloaded GitHub Repository](https://github.com/stefan-jansen/pyfolio-reloaded)
3. [pyfolio API Reference - ml4trading.io](https://pyfolio.ml4trading.io/api-reference.html)
4. [pyfolio on PyPI](https://pypi.org/project/pyfolio/)
5. [pyfolio-reloaded on PyPI](https://pypi.org/project/pyfolio-reloaded/)
6. [Round Trip Analysis Documentation](https://quantopian.github.io/pyfolio/notebooks/round_trip_tear_sheet_example/)
7. [Bayesian Analysis Documentation](https://quantopian.github.io/pyfolio/notebooks/bayesian/)

---

## Quick Reference Card

### Most Important Functions

```python
# Comprehensive analysis
pf.create_full_tear_sheet(returns, positions, transactions,
                          benchmark_rets=spy, live_start_date='2020-01-01')

# Key metrics
sharpe = pf.timeseries.sharpe_ratio(returns)
max_dd = pf.timeseries.max_drawdown(returns)
stats = pf.timeseries.perf_stats(returns, benchmark_rets)

# Round trips
round_trips = pf.round_trips.extract_round_trips(transactions)
pf.create_round_trip_tear_sheet(returns, positions, transactions)

# Zipline integration
returns, positions, transactions = pf.utils.extract_rets_pos_txn_from_zipline(backtest)
```

### Key Parameters

- **returns** - pd.Series of daily simple returns (required)
- **positions** - pd.DataFrame of position values (optional but recommended)
- **transactions** - pd.DataFrame with symbol, amount, price (optional)
- **benchmark_rets** - pd.Series of benchmark returns (recommended)
- **live_start_date** - Separates in-sample from out-of-sample (critical!)
- **turnover_denom** - 'AGB' or 'portfolio_value'
- **return_fig** - True to get figure object instead of display

---

**End of API Inventory**
For detailed JSON version, see: `pyfolio_comprehensive_api_inventory.json`
