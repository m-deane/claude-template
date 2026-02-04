# Pyfolio - Comprehensive User Reference Guide

**Version:** pyfolio-reloaded 0.9.9
**Status:** Actively Maintained
**Purpose:** Portfolio Performance and Risk Analytics

---

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Complete API Reference](#complete-api-reference)
5. [Plotting Functions with Interpretation](#plotting-functions-with-interpretation)
6. [Use Cases by Skill Level](#use-cases-by-skill-level)
7. [Data Structure Requirements](#data-structure-requirements)
8. [Best Practices & Common Pitfalls](#best-practices--common-pitfalls)

---

## Overview

Pyfolio is a Python library for performance and risk analysis of financial portfolios. It generates comprehensive "tear sheets" combining plots and statistics for portfolio evaluation.

**Key Capabilities:**
- Performance metrics (Sharpe, Sortino, Calmar, etc.)
- Drawdown analysis
- Position and transaction analysis
- Round-trip trade analysis
- Factor attribution
- Bayesian analysis (optional)

---

## Installation

### Recommended: pyfolio-reloaded

```bash
pip install pyfolio-reloaded
```

- **Latest Version:** 0.9.9 (June 2025)
- **Python Support:** 3.9 - 3.13
- **Maintainer:** Stefan Jansen (ml4trading)

### Alternative: Conda

```bash
conda install -c ml4t pyfolio-reloaded
```

### Dependencies

- numpy, pandas, matplotlib, seaborn, scipy, scikit-learn, empyrical

### Optional (for Bayesian analysis)

```bash
pip install pymc3 theano
```

---

## Quick Start

```python
import pyfolio as pf
import pandas as pd

# Minimal: Just returns
returns = pd.Series([0.01, -0.02, 0.015, ...], index=pd.DatetimeIndex([...]))
pf.create_simple_tear_sheet(returns)

# With benchmark
benchmark = pd.Series([0.005, -0.01, 0.01, ...], index=pd.DatetimeIndex([...]))
pf.create_returns_tear_sheet(returns, benchmark_rets=benchmark)

# Full analysis (with positions and transactions)
pf.create_full_tear_sheet(
    returns,
    positions=positions_df,
    transactions=transactions_df,
    benchmark_rets=benchmark
)
```

---

## Complete API Reference

### Module: pyfolio.tears

#### create_full_tear_sheet()

**The comprehensive analysis function.**

```python
pf.create_full_tear_sheet(
    returns,                    # pd.Series - Daily returns (Required)
    positions=None,             # pd.DataFrame - Position values
    transactions=None,          # pd.DataFrame - Trade data
    market_data=None,           # pd.DataFrame - OHLCV for capacity
    benchmark_rets=None,        # pd.Series - Benchmark returns
    slippage=None,              # float - Slippage in basis points
    live_start_date=None,       # date - Out-of-sample start (CRITICAL)
    sector_mappings=None,       # dict - Symbol to sector
    round_trips=False,          # bool - Include round trip analysis
    estimate_intraday='infer',  # str/bool - Detect intraday
    hide_positions=False,       # bool - Hide position details
    cone_std=(1.0, 1.5, 2.0),   # tuple - Forecast cone std devs
    bootstrap=False,            # bool - Bootstrap analysis
    turnover_denom='AGB',       # str - 'AGB' or 'portfolio_value'
    factor_returns=None,        # pd.DataFrame - For attribution
    factor_loadings=None,       # pd.DataFrame - For attribution
    pos_in_dollars=True,        # bool - Positions in $ vs shares
    return_fig=False            # bool - Return figure object
)
```

**Generates:**
- Cumulative returns plot
- Rolling metrics (Sharpe, beta, volatility)
- Drawdown analysis
- Monthly/annual returns breakdown
- Position analysis (if provided)
- Transaction analysis (if provided)

#### create_returns_tear_sheet()

```python
pf.create_returns_tear_sheet(
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

**Focuses on:** Returns analysis, drawdowns, rolling metrics

#### create_position_tear_sheet()

```python
pf.create_position_tear_sheet(
    returns,
    positions,                  # Required for this tear sheet
    show_and_plot_top_pos=2,    # int - Number of top positions
    hide_positions=False,
    sector_mappings=None,
    transactions=None,
    estimate_intraday='infer',
    return_fig=False
)
```

**Generates:**
- Top positions over time
- Long/short exposure
- Gross leverage
- Holdings count
- Sector allocations (if mappings provided)

#### create_txn_tear_sheet()

```python
pf.create_txn_tear_sheet(
    returns,
    positions,
    transactions,               # Required
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

#### create_round_trip_tear_sheet()

```python
pf.create_round_trip_tear_sheet(
    returns,
    positions,
    transactions,               # Required
    sector_mappings=None,
    estimate_intraday='infer',
    return_fig=False
)
```

**Generates:**
- Round trip statistics (PnL, duration, returns)
- Trade lifetime plots
- Probability of profit distribution
- Win rate analysis

#### create_simple_tear_sheet()

```python
pf.create_simple_tear_sheet(
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

**Use Case:** Quick overview without extensive data requirements

#### create_bayesian_tear_sheet()

```python
pf.create_bayesian_tear_sheet(
    returns,
    live_start_date=None,
    samples=2000,
    return_fig=False
)
```

**Requirements:** PyMC3, Theano
**Generates:** Bayesian cone, parameter posteriors

#### create_perf_attrib_tear_sheet()

```python
pf.create_perf_attrib_tear_sheet(
    returns,
    positions,
    factor_returns,             # pd.DataFrame - Required
    factor_loadings,            # pd.DataFrame - Required
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

#### create_capacity_tear_sheet()

```python
pf.create_capacity_tear_sheet(
    returns,
    positions,
    transactions,
    market_data,                # pd.DataFrame - Required (OHLCV)
    liquidation_daily_vol_limit=0.2,
    trade_daily_vol_limit=0.05,
    last_n_days=126,
    days_to_liquidate_limit=1,
    estimate_intraday='infer',
    return_fig=False
)
```

**Generates:**
- Capacity sweep (Sharpe vs capital)
- Days to liquidate
- Market impact estimates

---

### Module: pyfolio.timeseries

#### Performance Metrics

```python
# Annual return (CAGR)
pf.timeseries.annual_return(returns, period='daily')
# Returns: float

# Annual volatility
pf.timeseries.annual_volatility(returns, period='daily', alpha=2.0)
# Returns: float

# Sharpe ratio
pf.timeseries.sharpe_ratio(returns, risk_free=0, period='daily')
# Returns: float
# Interpretation: >1 good, >2 very good, >3 excellent

# Sortino ratio
pf.timeseries.sortino_ratio(returns, required_return=0, period='daily')
# Returns: float

# Calmar ratio
pf.timeseries.calmar_ratio(returns, period='daily')
# Returns: float (annual_return / max_drawdown)

# Omega ratio
pf.timeseries.omega_ratio(returns, annual_return_threshold=0.0)
# Returns: float
```

#### Risk Metrics

```python
# Maximum drawdown
pf.timeseries.max_drawdown(returns)
# Returns: float (negative value, e.g., -0.25 for 25% DD)

# Drawdown table
pf.timeseries.gen_drawdown_table(returns, top=10)
# Returns: pd.DataFrame with peak, valley, recovery dates

# Top drawdowns
pf.timeseries.get_top_drawdowns(returns, top=10)
# Returns: list of drawdown info

# Downside risk
pf.timeseries.downside_risk(returns, required_return=0, period='daily')
# Returns: float

# Tail ratio
pf.timeseries.tail_ratio(returns)
# Returns: float (right_tail_95 / abs(left_tail_5))

# Value at Risk
pf.timeseries.value_at_risk(returns, period=None, sigma=2.0)
# Returns: float
```

#### Benchmark Comparison

```python
# Alpha
pf.timeseries.alpha(returns, factor_returns)
# Returns: float (annualized excess return)

# Beta
pf.timeseries.beta(returns, factor_returns)
# Returns: float (sensitivity to benchmark)

# Alpha and Beta together
pf.timeseries.alpha_beta(returns, factor_returns)
# Returns: tuple(float, float)

# Rolling beta
pf.timeseries.rolling_beta(returns, factor_returns, rolling_window=126)
# Returns: pd.Series
```

#### Comprehensive Stats

```python
pf.timeseries.perf_stats(
    returns,
    factor_returns=None,
    positions=None,
    transactions=None,
    turnover_denom='AGB'
)
# Returns: pd.Series with all metrics
```

**Includes:** Annual return, cumulative returns, annual volatility, Sharpe, Calmar, stability, max drawdown, omega, sortino, skew, kurtosis, tail ratio, daily VaR, alpha, beta

#### Cumulative Returns

```python
# Cumulative returns from simple returns
pf.timeseries.cum_returns(returns, starting_value=0)
# Returns: pd.Series

# Final cumulative return
pf.timeseries.cum_returns_final(returns, starting_value=0)
# Returns: float

# Aggregate to different frequency
pf.timeseries.aggregate_returns(returns, convert_to='monthly')
# convert_to: 'weekly', 'monthly', 'yearly'
# Returns: pd.Series
```

#### Rolling Metrics

```python
# Rolling Sharpe
pf.timeseries.rolling_sharpe(returns, rolling_sharpe_window)
# Returns: pd.Series

# Rolling volatility
pf.timeseries.rolling_volatility(returns, rolling_vol_window)
# Returns: pd.Series

# Rolling beta
pf.timeseries.rolling_beta(returns, factor_returns, rolling_window=126)
# Returns: pd.Series
```

---

### Module: pyfolio.plotting

#### Returns Plots

```python
# Cumulative returns
pf.plotting.plot_returns(returns, live_start_date=None, ax=None)

# Rolling returns with cone
pf.plotting.plot_rolling_returns(
    returns,
    factor_returns=None,
    live_start_date=None,
    cone_std=(1.0, 1.5, 2.0),
    ax=None
)

# Annual returns bar chart
pf.plotting.plot_annual_returns(returns, ax=None)

# Monthly returns heatmap
pf.plotting.plot_monthly_returns_heatmap(returns, ax=None)

# Return quantiles
pf.plotting.plot_return_quantiles(returns, live_start_date=None, ax=None)

# Monthly returns distribution
pf.plotting.plot_monthly_returns_dist(returns, ax=None)
```

#### Risk Plots

```python
# Drawdown periods (cumulative returns with highlights)
pf.plotting.plot_drawdown_periods(returns, top=10, ax=None)

# Underwater plot (rolling drawdown depth)
pf.plotting.plot_drawdown_underwater(returns, ax=None)

# Rolling Sharpe
pf.plotting.plot_rolling_sharpe(returns, rolling_window=126, ax=None)

# Rolling beta
pf.plotting.plot_rolling_beta(returns, factor_returns, ax=None)

# Rolling volatility
pf.plotting.plot_rolling_volatility(returns, rolling_vol_window=126, ax=None)
```

#### Position Plots

```python
# Holdings count over time
pf.plotting.plot_holdings(returns, positions, ax=None)

# Long/short holdings
pf.plotting.plot_long_short_holdings(returns, positions, ax=None)

# Gross leverage
pf.plotting.plot_gross_leverage(returns, positions, ax=None)

# Exposures pie chart
pf.plotting.plot_exposures(returns, positions, ax=None)

# Sector allocations
pf.plotting.plot_sector_allocations(returns, positions, ax=None)
```

#### Transaction Plots

```python
# Turnover over time
pf.plotting.plot_turnover(returns, positions, transactions, ax=None)

# Daily volume
pf.plotting.plot_daily_volume(returns, transactions, ax=None)

# Turnover histogram
pf.plotting.plot_daily_turnover_hist(returns, transactions, ax=None)
```

#### Round Trip Plots

```python
# Trade lifetimes
pf.plotting.plot_round_trip_lifetimes(round_trips, ax=None)

# Probability of profit
pf.plotting.plot_prob_profit_trade(round_trips, ax=None)
```

---

### Module: pyfolio.round_trips

```python
# Extract round trips from transactions
pf.round_trips.extract_round_trips(
    transactions,
    portfolio_value=None
)
# Returns: pd.DataFrame with columns:
# - pnl, returns, duration, symbol, direction, etc.

# Generate round trip statistics
pf.round_trips.gen_round_trip_stats(round_trips)
# Returns: pd.Series

# Add closing transactions to close all positions
pf.round_trips.add_closing_transactions(positions, transactions)
# Returns: pd.DataFrame
```

---

### Module: pyfolio.pos

```python
# Get percent allocations
pf.pos.get_percent_alloc(values)
# Returns: pd.DataFrame

# Get top long, short, and absolute positions
pf.pos.get_top_long_short_abs(positions, top=10)
# Returns: dict

# Max and median position concentration
pf.pos.get_max_median_position_concentration(positions)
# Returns: tuple(float, float)

# Sector exposures
pf.pos.get_sector_exposures(positions, symbol_sector_map)
# Returns: pd.DataFrame

# Long/short positions
pf.pos.get_long_short_pos(positions)
# Returns: tuple(pd.DataFrame, pd.DataFrame)
```

---

### Module: pyfolio.txn

```python
# Calculate turnover
pf.txn.get_turnover(positions, transactions, denominator='AGB')
# denominator: 'AGB' (Actual Gross Book) or 'portfolio_value'
# Returns: pd.Series

# Transaction volume
pf.txn.get_txn_vol(transactions)
# Returns: pd.DataFrame

# Adjust returns for slippage
pf.txn.adjust_returns_for_slippage(returns, positions, transactions, slippage_bps)
# Returns: pd.Series
```

---

### Module: pyfolio.utils

```python
# Extract from Zipline backtest
pf.utils.extract_rets_pos_txn_from_zipline(backtest)
# Returns: tuple(returns, positions, transactions)

# Check for intraday strategy
pf.utils.check_intraday(estimate, returns, positions, transactions)
# Returns: dict

# Clip returns to benchmark dates
pf.utils.clip_returns_to_benchmark(rets, benchmark_rets)
# Returns: pd.Series

# Print formatted table
pf.utils.print_table(table, name=None, float_format=None)
```

---

## Plotting Functions with Interpretation

### plot_rolling_returns() - CRITICAL

**What it shows:** Cumulative returns over time with optional probability cone.

**How to interpret:**
- **Steady upward slope:** Consistent positive returns
- **Sharp drops:** Drawdown periods
- **Cone divergence:** In-sample (green) vs out-of-sample (red)

**Good signs:**
- Strategy line above benchmark
- Returns within cone bounds
- Consistent out-of-sample vs in-sample

**Red flags:**
- Sharp divergence at live_start_date
- Returns outside 2-std cone
- Choppy, sideways performance

### plot_drawdown_underwater() - CRITICAL

**What it shows:** Rolling drawdown depth from peak values.

**How to interpret:**
- **Shallow, brief dips:** Good risk management
- **Deep, prolonged dips:** Extended losing periods
- **Recovery speed:** How fast strategy rebounds

**Good signs:**
- Max drawdown < 20%
- Quick recoveries (< 3 months)
- Decreasing drawdown depth over time

**Red flags:**
- Max drawdown > 30%
- Multi-year recovery periods
- Increasing drawdown severity

### plot_monthly_returns_heatmap()

**What it shows:** Calendar heatmap of monthly returns.

**How to interpret:**
- **Green cells:** Positive months
- **Red cells:** Negative months
- **Patterns:** Seasonal or regime effects

**Good signs:**
- More green than red
- No extended red streaks
- Consistent performance across years

**Red flags:**
- Specific months consistently red
- Entire years negative
- Recent deterioration

### plot_rolling_sharpe()

**What it shows:** Rolling Sharpe ratio over time (typically 6-month window).

**How to interpret:**
- **Above 1.0 line:** Good risk-adjusted returns
- **Volatile:** Inconsistent performance
- **Declining trend:** Strategy decay

**Good signs:**
- Consistently above 1.0
- Low volatility around mean
- Stable over time

**Red flags:**
- Frequently below 0
- Declining trend
- High volatility

---

## Use Cases by Skill Level

### BEGINNER: Basic Returns Analysis

```python
"""
Beginner Example: Analyze strategy returns vs benchmark
Goal: Understand basic performance metrics
"""
import pyfolio as pf
import pandas as pd
import numpy as np

# Step 1: Create sample returns
np.random.seed(42)
dates = pd.date_range('2020-01-01', periods=756, freq='D')

# Strategy returns (slightly positive drift)
strategy_returns = pd.Series(
    np.random.normal(0.0005, 0.015, len(dates)),
    index=dates,
    name='strategy'
)

# Benchmark returns (SPY-like)
benchmark_returns = pd.Series(
    np.random.normal(0.0003, 0.012, len(dates)),
    index=dates,
    name='benchmark'
)

# Step 2: Quick metrics
print("=== Key Metrics ===")
print(f"Annual Return: {pf.timeseries.annual_return(strategy_returns):.2%}")
print(f"Annual Vol: {pf.timeseries.annual_volatility(strategy_returns):.2%}")
print(f"Sharpe Ratio: {pf.timeseries.sharpe_ratio(strategy_returns):.2f}")
print(f"Max Drawdown: {pf.timeseries.max_drawdown(strategy_returns):.2%}")

# Step 3: Compare to benchmark
alpha, beta = pf.timeseries.alpha_beta(strategy_returns, benchmark_returns)
print(f"\nAlpha: {alpha:.2%}")
print(f"Beta: {beta:.2f}")

# Step 4: Simple tear sheet
pf.create_simple_tear_sheet(
    strategy_returns,
    benchmark_rets=benchmark_returns
)

# Step 5: More detailed returns analysis
pf.create_returns_tear_sheet(
    strategy_returns,
    benchmark_rets=benchmark_returns,
    live_start_date='2022-01-01'  # Last year as out-of-sample
)
```

### INTERMEDIATE: Full Analysis with Positions

```python
"""
Intermediate Example: Complete tear sheet with positions and transactions
Goal: Analyze portfolio holdings and trading behavior
"""
import pyfolio as pf
import pandas as pd
import numpy as np

# Create sample data
np.random.seed(42)
dates = pd.date_range('2020-01-01', periods=500, freq='D')

# Returns
returns = pd.Series(
    np.random.normal(0.0005, 0.015, len(dates)),
    index=dates
)

# Positions (daily position values in dollars)
positions = pd.DataFrame(
    index=dates,
    data={
        'AAPL': np.random.uniform(5000, 15000, len(dates)),
        'GOOGL': np.random.uniform(3000, 10000, len(dates)),
        'MSFT': np.random.uniform(4000, 12000, len(dates)),
        'cash': np.random.uniform(1000, 5000, len(dates))  # REQUIRED!
    }
)

# Transactions
n_trades = 200
trade_dates = np.random.choice(dates, n_trades)
transactions = pd.DataFrame({
    'symbol': np.random.choice(['AAPL', 'GOOGL', 'MSFT'], n_trades),
    'amount': np.random.randint(-100, 100, n_trades),  # + buy, - sell
    'price': np.random.uniform(100, 500, n_trades),
    'commission': np.ones(n_trades)
}, index=trade_dates).sort_index()

# Sector mappings
sector_map = {
    'AAPL': 'Technology',
    'GOOGL': 'Technology',
    'MSFT': 'Technology'
}

# Benchmark
benchmark = pd.Series(
    np.random.normal(0.0003, 0.012, len(dates)),
    index=dates
)

# Full tear sheet
pf.create_full_tear_sheet(
    returns,
    positions=positions,
    transactions=transactions,
    benchmark_rets=benchmark,
    sector_mappings=sector_map,
    live_start_date='2021-06-01',
    round_trips=True  # Include round trip analysis
)

# Individual focused analyses
print("\n=== Transaction Analysis ===")
pf.create_txn_tear_sheet(returns, positions, transactions)

print("\n=== Position Analysis ===")
pf.create_position_tear_sheet(
    returns, positions,
    sector_mappings=sector_map
)
```

### ADVANCED: Round Trip Analysis with Factor Attribution

```python
"""
Advanced Example: Trade efficiency and factor attribution
Goal: Understand trade quality and return sources
"""
import pyfolio as pf
import pandas as pd
import numpy as np

# Assume returns, positions, transactions exist from previous example

# Round Trip Analysis
print("=== Round Trip Analysis ===")

# Extract round trips
round_trips = pf.round_trips.extract_round_trips(
    transactions,
    portfolio_value=positions.sum(axis=1)
)

# Round trip statistics
rt_stats = pf.round_trips.gen_round_trip_stats(round_trips)
print("\nRound Trip Statistics:")
print(rt_stats)

# Key metrics
print(f"\nWin Rate: {(round_trips['pnl'] > 0).mean():.1%}")
print(f"Avg Winner: ${round_trips[round_trips['pnl'] > 0]['pnl'].mean():,.2f}")
print(f"Avg Loser: ${round_trips[round_trips['pnl'] < 0]['pnl'].mean():,.2f}")
print(f"Profit Factor: {round_trips[round_trips['pnl'] > 0]['pnl'].sum() / abs(round_trips[round_trips['pnl'] < 0]['pnl'].sum()):.2f}")

# Factor Attribution (if factor data available)
# Define factor returns (e.g., Fama-French)
factor_returns = pd.DataFrame({
    'Market': np.random.normal(0.0003, 0.01, len(dates)),
    'Size': np.random.normal(0.0001, 0.005, len(dates)),
    'Value': np.random.normal(0.0001, 0.005, len(dates)),
    'Momentum': np.random.normal(0.0002, 0.006, len(dates))
}, index=dates)

# Factor loadings (exposure of each stock to each factor)
factor_loadings = pd.DataFrame({
    'Market': [1.2, 1.1, 0.9],
    'Size': [-0.3, -0.5, -0.4],
    'Value': [0.2, -0.1, 0.3],
    'Momentum': [0.4, 0.6, 0.2]
}, index=['AAPL', 'GOOGL', 'MSFT'])

# Performance attribution
pf.create_perf_attrib_tear_sheet(
    returns,
    positions,
    factor_returns,
    factor_loadings
)
```

### EXPERT: Custom Risk Report with Statistical Testing

```python
"""
Expert Example: Production-grade risk monitoring
Goal: Statistically rigorous performance evaluation
"""
import pyfolio as pf
import pandas as pd
import numpy as np
from scipy import stats

class RiskReport:
    """Production risk reporting with statistical validation."""

    def __init__(self, returns, benchmark=None, positions=None,
                 transactions=None, live_start_date=None):
        self.returns = returns
        self.benchmark = benchmark
        self.positions = positions
        self.transactions = transactions
        self.live_start_date = live_start_date

        # Split in-sample and out-of-sample
        if live_start_date:
            self.is_returns = returns[:live_start_date]
            self.oos_returns = returns[live_start_date:]
        else:
            self.is_returns = returns
            self.oos_returns = None

    def calculate_all_metrics(self):
        """Calculate comprehensive metrics."""
        metrics = {}

        # Basic metrics
        metrics['annual_return'] = pf.timeseries.annual_return(self.returns)
        metrics['annual_vol'] = pf.timeseries.annual_volatility(self.returns)
        metrics['sharpe'] = pf.timeseries.sharpe_ratio(self.returns)
        metrics['sortino'] = pf.timeseries.sortino_ratio(self.returns)
        metrics['calmar'] = pf.timeseries.calmar_ratio(self.returns)
        metrics['max_dd'] = pf.timeseries.max_drawdown(self.returns)

        # Benchmark comparison
        if self.benchmark is not None:
            alpha, beta = pf.timeseries.alpha_beta(self.returns, self.benchmark)
            metrics['alpha'] = alpha
            metrics['beta'] = beta

        # Tail risk
        metrics['var_95'] = np.percentile(self.returns, 5)
        metrics['cvar_95'] = self.returns[self.returns <= metrics['var_95']].mean()
        metrics['tail_ratio'] = pf.timeseries.tail_ratio(self.returns)

        return pd.Series(metrics)

    def test_sharpe_significance(self, null_sharpe=0):
        """Test if Sharpe ratio is statistically significant."""
        n = len(self.returns)
        sharpe = pf.timeseries.sharpe_ratio(self.returns)

        # Standard error of Sharpe (Lo 2002)
        skew = stats.skew(self.returns)
        kurt = stats.kurtosis(self.returns)
        se_sharpe = np.sqrt((1 + 0.5*sharpe**2 - skew*sharpe + (kurt-3)/4*sharpe**2) / n)

        # T-statistic
        t_stat = (sharpe - null_sharpe) / se_sharpe
        p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df=n-1))

        return {
            'sharpe': sharpe,
            't_stat': t_stat,
            'p_value': p_value,
            'significant_5pct': p_value < 0.05,
            'significant_1pct': p_value < 0.01
        }

    def compare_is_oos(self):
        """Compare in-sample vs out-of-sample performance."""
        if self.oos_returns is None:
            return None

        is_metrics = {
            'sharpe': pf.timeseries.sharpe_ratio(self.is_returns),
            'annual_return': pf.timeseries.annual_return(self.is_returns),
            'max_dd': pf.timeseries.max_drawdown(self.is_returns)
        }

        oos_metrics = {
            'sharpe': pf.timeseries.sharpe_ratio(self.oos_returns),
            'annual_return': pf.timeseries.annual_return(self.oos_returns),
            'max_dd': pf.timeseries.max_drawdown(self.oos_returns)
        }

        # Degradation
        degradation = {
            'sharpe_deg': is_metrics['sharpe'] - oos_metrics['sharpe'],
            'return_deg': is_metrics['annual_return'] - oos_metrics['annual_return'],
            'dd_deg': abs(oos_metrics['max_dd']) - abs(is_metrics['max_dd'])
        }

        return {
            'in_sample': is_metrics,
            'out_of_sample': oos_metrics,
            'degradation': degradation
        }

    def run_bootstrap_analysis(self, n_samples=1000):
        """Bootstrap confidence intervals for key metrics."""
        n = len(self.returns)
        boot_sharpes = []
        boot_returns = []

        for _ in range(n_samples):
            # Resample with replacement
            sample = self.returns.sample(n=n, replace=True)
            boot_sharpes.append(pf.timeseries.sharpe_ratio(sample))
            boot_returns.append(pf.timeseries.annual_return(sample))

        return {
            'sharpe_ci_95': (np.percentile(boot_sharpes, 2.5),
                           np.percentile(boot_sharpes, 97.5)),
            'return_ci_95': (np.percentile(boot_returns, 2.5),
                            np.percentile(boot_returns, 97.5))
        }

    def generate_report(self):
        """Generate comprehensive risk report."""
        print("=" * 60)
        print("COMPREHENSIVE RISK REPORT")
        print("=" * 60)

        # Basic metrics
        print("\n1. PERFORMANCE METRICS")
        print("-" * 40)
        metrics = self.calculate_all_metrics()
        for name, value in metrics.items():
            print(f"  {name}: {value:.4f}")

        # Statistical significance
        print("\n2. STATISTICAL SIGNIFICANCE")
        print("-" * 40)
        sig_test = self.test_sharpe_significance()
        print(f"  Sharpe Ratio: {sig_test['sharpe']:.3f}")
        print(f"  T-statistic: {sig_test['t_stat']:.3f}")
        print(f"  P-value: {sig_test['p_value']:.4f}")
        print(f"  Significant at 5%: {sig_test['significant_5pct']}")

        # In-sample vs out-of-sample
        if self.live_start_date:
            print("\n3. IN-SAMPLE VS OUT-OF-SAMPLE")
            print("-" * 40)
            comparison = self.compare_is_oos()
            print(f"  In-sample Sharpe: {comparison['in_sample']['sharpe']:.3f}")
            print(f"  Out-of-sample Sharpe: {comparison['out_of_sample']['sharpe']:.3f}")
            print(f"  Sharpe Degradation: {comparison['degradation']['sharpe_deg']:.3f}")

        # Bootstrap CIs
        print("\n4. BOOTSTRAP CONFIDENCE INTERVALS (95%)")
        print("-" * 40)
        boot = self.run_bootstrap_analysis()
        print(f"  Sharpe CI: [{boot['sharpe_ci_95'][0]:.3f}, {boot['sharpe_ci_95'][1]:.3f}]")
        print(f"  Return CI: [{boot['return_ci_95'][0]:.2%}, {boot['return_ci_95'][1]:.2%}]")

        print("\n" + "=" * 60)

# Usage
report = RiskReport(
    returns=returns,
    benchmark=benchmark,
    positions=positions,
    transactions=transactions,
    live_start_date='2022-01-01'
)

report.generate_report()
```

---

## Data Structure Requirements

### Returns (Required)

```python
# pd.Series with DatetimeIndex
# Values: Daily simple returns (NOT log returns)
returns = pd.Series(
    [0.01, -0.005, 0.02, 0.003, -0.01],
    index=pd.DatetimeIndex([
        '2023-01-02', '2023-01-03', '2023-01-04',
        '2023-01-05', '2023-01-06'
    ])
)

# CRITICAL: Must be simple returns
# If you have log returns, convert:
simple_returns = np.exp(log_returns) - 1
```

### Positions (Optional but Recommended)

```python
# pd.DataFrame with:
# - DatetimeIndex
# - Columns: Asset symbols
# - Values: Dollar position values
# - MUST include 'cash' column

positions = pd.DataFrame({
    'AAPL': [10000, 10500, 10200, 10800, 10600],
    'GOOGL': [8000, 7800, 8200, 8100, 8400],
    'cash': [2000, 1700, 1600, 1100, 1000]  # Required!
}, index=pd.DatetimeIndex([
    '2023-01-02', '2023-01-03', '2023-01-04',
    '2023-01-05', '2023-01-06'
]))
```

### Transactions (Optional)

```python
# pd.DataFrame with:
# - DatetimeIndex (trade execution times)
# Required columns:
# - symbol: Ticker symbol
# - amount: Shares traded (positive=buy, negative=sell)
# - price: Execution price
# Optional columns:
# - commission: Transaction cost

transactions = pd.DataFrame({
    'symbol': ['AAPL', 'GOOGL', 'AAPL'],
    'amount': [100, -50, -25],  # Buy 100, sell 50, sell 25
    'price': [150.25, 2800.50, 152.00],
    'commission': [1.0, 1.0, 1.0]
}, index=pd.DatetimeIndex([
    '2023-01-02 10:30:00',
    '2023-01-03 14:15:00',
    '2023-01-05 09:45:00'
]))
```

### Factor Returns (For Attribution)

```python
# pd.DataFrame with:
# - DatetimeIndex matching returns
# - Columns: Factor names
# - Values: Daily factor returns

factor_returns = pd.DataFrame({
    'Market': [0.005, -0.003, 0.008, 0.002, -0.004],
    'Size': [0.001, 0.002, -0.001, 0.001, 0.000],
    'Value': [-0.002, 0.001, 0.003, -0.001, 0.002],
    'Momentum': [0.003, -0.002, 0.001, 0.004, -0.003]
}, index=returns.index)
```

### Factor Loadings (For Attribution)

```python
# pd.DataFrame with:
# - Index: Asset symbols
# - Columns: Factor names (must match factor_returns)
# - Values: Factor exposures (betas)

factor_loadings = pd.DataFrame({
    'Market': [1.2, 0.9, 1.1],
    'Size': [-0.3, 0.2, -0.1],
    'Value': [0.5, -0.2, 0.3],
    'Momentum': [0.2, 0.4, 0.1]
}, index=['AAPL', 'GOOGL', 'MSFT'])
```

---

## Best Practices & Common Pitfalls

### Best Practices

1. **Always specify `live_start_date`** to separate in-sample from out-of-sample
2. **Include benchmark** for proper context
3. **Use pyfolio-reloaded** instead of original pyfolio
4. **Include 'cash' column** in positions DataFrame
5. **Check round trips** for trade efficiency
6. **Run capacity analysis** before live trading
7. **Verify returns are simple returns** (not log returns)

### Common Pitfalls

| Issue | Symptom | Solution |
|-------|---------|----------|
| Using log returns | Metrics are wrong | Convert: `simple = np.exp(log) - 1` |
| Missing cash column | Position analysis fails | Add 'cash' column to positions |
| Timezone mismatches | Data alignment errors | Convert all to UTC |
| Overfitting | OOS performance collapse | Use `live_start_date` |
| Ignoring transaction costs | Unrealistic returns | Include commissions, use slippage |
| Wrong benchmark | Misleading alpha/beta | Use appropriate benchmark |
| Survivorship bias | Inflated backtest | Use point-in-time data |

### Interpretation Guidelines

| Metric | Poor | Acceptable | Good | Excellent |
|--------|------|------------|------|-----------|
| Sharpe Ratio | < 0.5 | 0.5-1.0 | 1.0-2.0 | > 2.0 |
| Max Drawdown | > 30% | 20-30% | 10-20% | < 10% |
| Win Rate | < 40% | 40-50% | 50-60% | > 60% |
| Profit Factor | < 1.0 | 1.0-1.5 | 1.5-2.0 | > 2.0 |
| Calmar Ratio | < 0.5 | 0.5-1.0 | 1.0-2.0 | > 2.0 |

---

## Resources

- **Documentation:** https://pyfolio.ml4trading.io/
- **GitHub (reloaded):** https://github.com/stefan-jansen/pyfolio-reloaded
- **Original Quantopian:** https://github.com/quantopian/pyfolio
- **empyrical (underlying metrics):** https://github.com/quantopian/empyrical
