# Cross-Library Integration Guide

This guide demonstrates how to combine Alphalens, Pyfolio, VectorBT, and OpenBB for complete quantitative research workflows.

---

## Integration Patterns

### Pattern 1: Factor Research Pipeline
```
OpenBB (data) → Alphalens (factor analysis) → Pyfolio (risk analysis)
```

### Pattern 2: Strategy Development
```
OpenBB (data) → VectorBT (backtesting) → Pyfolio (risk reporting)
```

### Pattern 3: Complete Research Pipeline
```
OpenBB (data acquisition)
    ↓
Alphalens (alpha research)
    ↓
VectorBT (strategy backtesting)
    ↓
Pyfolio (comprehensive risk reporting)
```

---

## Integration 1: Factor Research Pipeline

### Complete Example

```python
"""
Complete Factor Research Pipeline
OpenBB → Alphalens → Pyfolio

Goal: Research a momentum factor, evaluate it, and analyze the portfolio
"""

# ============================================================
# STEP 1: DATA ACQUISITION (OpenBB)
# ============================================================

from openbb import obb
import pandas as pd
import numpy as np

# Define universe
symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA',
           'JPM', 'BAC', 'GS', 'XOM', 'CVX', 'JNJ', 'PFE', 'UNH']

# Fetch historical prices
print("Fetching price data...")
prices_dict = {}
for symbol in symbols:
    try:
        data = obb.equity.price.historical(
            symbol,
            start_date='2020-01-01',
            end_date='2023-12-31',
            provider='yfinance'
        )
        prices_dict[symbol] = data.to_dataframe()['close']
    except Exception as e:
        print(f"  Error fetching {symbol}: {e}")

# Combine into DataFrame
prices = pd.DataFrame(prices_dict)
prices.index = pd.to_datetime(prices.index)
print(f"Price data shape: {prices.shape}")

# Fetch sector information
sectors = {}
for symbol in symbols:
    try:
        profile = obb.equity.profile(symbol, provider='yfinance')
        profile_data = profile.to_dict()
        if profile_data:
            sectors[symbol] = profile_data[0].get('sector', 'Unknown')
    except:
        sectors[symbol] = 'Unknown'

sector_map = pd.Series(sectors)
print(f"Sectors: {sector_map.value_counts().to_dict()}")

# ============================================================
# STEP 2: FACTOR CONSTRUCTION & ANALYSIS (Alphalens)
# ============================================================

import alphalens as al

# Create momentum factor (60-day returns)
print("\nConstructing momentum factor...")
momentum = prices.pct_change(60)

# Convert to MultiIndex Series (required by Alphalens)
factor = momentum.stack()
factor.index.names = ['date', 'asset']
factor = factor.dropna()
factor.name = 'momentum_60d'

print(f"Factor observations: {len(factor)}")

# Prepare data for Alphalens
factor_data = al.utils.get_clean_factor_and_forward_returns(
    factor=factor,
    prices=prices,
    groupby=sector_map,
    quantiles=5,
    periods=(1, 5, 21),  # 1-day, 1-week, 1-month
    max_loss=0.35
)

print(f"Factor data shape: {factor_data.shape}")

# Quick screening
print("\n=== FACTOR SUMMARY ===")
al.tears.create_summary_tear_sheet(factor_data)

# Get IC metrics
ic = al.performance.factor_information_coefficient(factor_data)
mean_ic = ic.mean()
ic_std = ic.std()
ir = mean_ic / ic_std

print("\n=== IC METRICS ===")
for period in mean_ic.index:
    print(f"{period}:")
    print(f"  Mean IC: {mean_ic[period]:.4f}")
    print(f"  IC Std: {ic_std[period]:.4f}")
    print(f"  IR: {ir[period]:.4f}")
    print(f"  Viable: {abs(mean_ic[period]) > 0.02 and abs(ir[period]) > 0.3}")

# Full analysis (if promising)
if (abs(mean_ic) > 0.02).any():
    print("\n=== FULL TEAR SHEET ===")
    al.tears.create_full_tear_sheet(
        factor_data,
        long_short=True,
        group_neutral=True,
        by_group=False
    )

# ============================================================
# STEP 3: PORTFOLIO ANALYSIS (Pyfolio)
# ============================================================

import pyfolio as pf

# Create Pyfolio inputs from Alphalens
print("\n=== PORTFOLIO ANALYSIS ===")
returns, positions, benchmark = al.performance.create_pyfolio_input(
    factor_data,
    period='5D',  # 5-day holding period
    long_short=True,
    capital=1000000  # $1M capital
)

print(f"Returns shape: {returns.shape}")
print(f"Positions shape: {positions.shape}")

# Performance metrics
print("\n=== PERFORMANCE METRICS ===")
stats = pf.timeseries.perf_stats(returns, benchmark)
print(stats)

# Full tear sheet
pf.create_full_tear_sheet(
    returns,
    positions=positions,
    benchmark_rets=benchmark,
    live_start_date=returns.index[-63]  # Last quarter OOS
)
```

---

## Integration 2: Backtesting with Risk Analytics

### Complete Example

```python
"""
Strategy Backtesting Pipeline
OpenBB → VectorBT → Pyfolio

Goal: Develop MA crossover strategy, backtest, analyze risk
"""

# ============================================================
# STEP 1: DATA ACQUISITION (OpenBB)
# ============================================================

from openbb import obb
import pandas as pd
import numpy as np

# Fetch data
print("Fetching data...")
data = obb.equity.price.historical(
    symbol='SPY',
    start_date='2018-01-01',
    end_date='2023-12-31',
    provider='yfinance'
)

df = data.to_dataframe()
close = df['close']
print(f"Data shape: {close.shape}")

# ============================================================
# STEP 2: STRATEGY BACKTESTING (VectorBT)
# ============================================================

import vectorbt as vbt

# Define strategy parameters
fast_windows = [10, 20, 30]
slow_windows = [50, 100, 150]

# Generate signals
print("\nRunning backtests...")
fast_ma = vbt.MA.run(close, window=fast_windows)
slow_ma = vbt.MA.run(close, window=slow_windows)

entries = fast_ma.ma_crossed_above(slow_ma)
exits = fast_ma.ma_crossed_below(slow_ma)

# Run portfolio simulation
pf_vbt = vbt.Portfolio.from_signals(
    close=close,
    entries=entries,
    exits=exits,
    fees=0.001,
    freq='D'
)

# Find best parameters
sharpe_ratios = pf_vbt.sharpe_ratio()
print(f"\nSharpe Ratios:\n{sharpe_ratios}")

best_params = sharpe_ratios.idxmax()
print(f"\nBest Parameters: {best_params}")
print(f"Best Sharpe: {sharpe_ratios.max():.2f}")

# Get best portfolio
best_pf = pf_vbt[best_params]

# VectorBT stats
print("\n=== VECTORBT STATS ===")
print(best_pf.stats())

# ============================================================
# STEP 3: RISK ANALYSIS (Pyfolio)
# ============================================================

import pyfolio as pf

# Extract returns and positions from VectorBT
vbt_returns = best_pf.returns()

# Convert to Pyfolio format
returns = vbt_returns.copy()
returns.name = 'strategy'

# Get positions from VectorBT
# VectorBT stores positions as asset values
vbt_positions = pd.DataFrame({
    'SPY': best_pf.assets(),
    'cash': best_pf.cash()
})

# Get benchmark (buy-and-hold)
benchmark = close.pct_change().dropna()
benchmark = benchmark.loc[returns.index]

print("\n=== PYFOLIO ANALYSIS ===")

# Calculate key metrics
print("Key Metrics:")
print(f"  Annual Return: {pf.timeseries.annual_return(returns):.2%}")
print(f"  Annual Vol: {pf.timeseries.annual_volatility(returns):.2%}")
print(f"  Sharpe Ratio: {pf.timeseries.sharpe_ratio(returns):.2f}")
print(f"  Max Drawdown: {pf.timeseries.max_drawdown(returns):.2%}")

# Compare to benchmark
alpha, beta = pf.timeseries.alpha_beta(returns, benchmark)
print(f"  Alpha: {alpha:.2%}")
print(f"  Beta: {beta:.2f}")

# Create tear sheet
pf.create_returns_tear_sheet(
    returns,
    benchmark_rets=benchmark,
    live_start_date=returns.index[-252]  # Last year OOS
)

# ============================================================
# STEP 4: COMBINED REPORT
# ============================================================

print("\n" + "=" * 60)
print("COMBINED STRATEGY REPORT")
print("=" * 60)

print(f"\nStrategy: MA Crossover ({best_params[0]}/{best_params[1]})")
print(f"Period: {returns.index[0].date()} to {returns.index[-1].date()}")

print("\n--- VectorBT Metrics ---")
print(f"Total Return: {best_pf.total_return():.2%}")
print(f"Win Rate: {best_pf.trades.win_rate():.1%}")
print(f"Profit Factor: {best_pf.trades.profit_factor():.2f}")
print(f"Total Trades: {len(best_pf.trades.records)}")

print("\n--- Pyfolio Metrics ---")
print(f"Sharpe Ratio: {pf.timeseries.sharpe_ratio(returns):.2f}")
print(f"Sortino Ratio: {pf.timeseries.sortino_ratio(returns):.2f}")
print(f"Calmar Ratio: {pf.timeseries.calmar_ratio(returns):.2f}")
print(f"Tail Ratio: {pf.timeseries.tail_ratio(returns):.2f}")
```

---

## Integration 3: Complete Research Pipeline

### Production-Grade Example

```python
"""
Complete Research-to-Production Pipeline
All Four Libraries Combined

Goal: Full quantitative research workflow
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ============================================================
# CONFIGURATION
# ============================================================

CONFIG = {
    'universe': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA',
                 'JPM', 'BAC', 'V', 'MA', 'XOM', 'CVX', 'JNJ', 'UNH'],
    'start_date': '2019-01-01',
    'end_date': '2023-12-31',
    'factor_periods': (1, 5, 21),
    'holding_period': '5D',
    'capital': 1000000,
    'fees': 0.001,
    'oos_months': 12
}

# ============================================================
# PHASE 1: DATA ACQUISITION (OpenBB)
# ============================================================

from openbb import obb

class DataAcquisition:
    """Handle all data fetching via OpenBB."""

    def __init__(self, config):
        self.config = config
        self.prices = None
        self.sectors = None
        self.fundamentals = {}

    def fetch_prices(self):
        """Fetch historical prices for universe."""
        print("Phase 1: Fetching price data...")
        prices_dict = {}

        for symbol in self.config['universe']:
            try:
                data = obb.equity.price.historical(
                    symbol,
                    start_date=self.config['start_date'],
                    end_date=self.config['end_date'],
                    provider='yfinance'
                )
                prices_dict[symbol] = data.to_dataframe()['close']
            except Exception as e:
                print(f"  Warning: {symbol} - {e}")

        self.prices = pd.DataFrame(prices_dict)
        self.prices.index = pd.to_datetime(self.prices.index)
        print(f"  Fetched {len(self.prices.columns)} symbols, {len(self.prices)} days")
        return self.prices

    def fetch_sectors(self):
        """Fetch sector mappings."""
        print("Fetching sector data...")
        sectors = {}

        for symbol in self.config['universe']:
            try:
                profile = obb.equity.profile(symbol, provider='yfinance')
                data = profile.to_dict()
                if data:
                    sectors[symbol] = data[0].get('sector', 'Unknown')
            except:
                sectors[symbol] = 'Unknown'

        self.sectors = pd.Series(sectors)
        print(f"  Sectors: {self.sectors.value_counts().to_dict()}")
        return self.sectors

    def fetch_fundamentals(self):
        """Fetch fundamental data for factor construction."""
        print("Fetching fundamentals...")

        for symbol in self.config['universe']:
            try:
                metrics = obb.equity.fundamental.metrics(symbol, provider='fmp')
                self.fundamentals[symbol] = metrics.to_dict()[0] if metrics.to_dict() else {}
            except:
                self.fundamentals[symbol] = {}

        print(f"  Fetched fundamentals for {len(self.fundamentals)} symbols")
        return self.fundamentals

# ============================================================
# PHASE 2: FACTOR ANALYSIS (Alphalens)
# ============================================================

import alphalens as al

class FactorResearch:
    """Factor research using Alphalens."""

    def __init__(self, prices, sectors, config):
        self.prices = prices
        self.sectors = sectors
        self.config = config
        self.factors = {}
        self.results = {}

    def create_momentum_factor(self, lookback=60):
        """Create momentum factor."""
        momentum = self.prices.pct_change(lookback)
        factor = momentum.stack()
        factor.index.names = ['date', 'asset']
        factor = factor.dropna()
        factor.name = f'momentum_{lookback}d'
        self.factors[f'momentum_{lookback}d'] = factor
        return factor

    def create_mean_reversion_factor(self, lookback=20):
        """Create mean reversion factor (negative momentum)."""
        returns = self.prices.pct_change(lookback)
        factor = -returns  # Negative = mean reversion
        factor = factor.stack()
        factor.index.names = ['date', 'asset']
        factor = factor.dropna()
        factor.name = f'mean_reversion_{lookback}d'
        self.factors[f'mean_reversion_{lookback}d'] = factor
        return factor

    def evaluate_factor(self, factor_name):
        """Evaluate factor using Alphalens."""
        factor = self.factors[factor_name]

        factor_data = al.utils.get_clean_factor_and_forward_returns(
            factor=factor,
            prices=self.prices,
            groupby=self.sectors,
            quantiles=5,
            periods=self.config['factor_periods'],
            max_loss=0.35
        )

        # Calculate metrics
        ic = al.performance.factor_information_coefficient(factor_data)
        mean_ic = ic.mean()
        ir = mean_ic / ic.std()

        mean_ret, _ = al.performance.mean_return_by_quantile(factor_data)
        spread = mean_ret.loc[5] - mean_ret.loc[1]

        self.results[factor_name] = {
            'factor_data': factor_data,
            'mean_ic': mean_ic.to_dict(),
            'ir': ir.to_dict(),
            'spread': spread.to_dict(),
            'viable': (abs(mean_ic) > 0.02).any() and (abs(ir) > 0.3).any()
        }

        return self.results[factor_name]

    def get_best_factor(self):
        """Return the best performing factor."""
        best = None
        best_ir = 0

        for name, result in self.results.items():
            if result['viable']:
                max_ir = max(abs(v) for v in result['ir'].values())
                if max_ir > best_ir:
                    best_ir = max_ir
                    best = name

        return best, self.results.get(best)

# ============================================================
# PHASE 3: STRATEGY BACKTESTING (VectorBT)
# ============================================================

import vectorbt as vbt

class StrategyBacktest:
    """Strategy backtesting using VectorBT."""

    def __init__(self, prices, config):
        self.prices = prices
        self.config = config
        self.portfolios = {}

    def backtest_factor_strategy(self, factor_data, name):
        """Backtest factor-based strategy."""
        # Get quantile assignments
        quantiles = factor_data['factor_quantile'].unstack()

        # Entry: When stock enters top quantile
        entries = quantiles == 5

        # Exit: When stock leaves top quantile
        exits = quantiles != 5

        # Align with prices
        common_idx = self.prices.index.intersection(entries.index)
        common_cols = self.prices.columns.intersection(entries.columns)

        aligned_entries = entries.loc[common_idx, common_cols]
        aligned_exits = exits.loc[common_idx, common_cols]
        aligned_prices = self.prices.loc[common_idx, common_cols]

        # Run backtest
        pf = vbt.Portfolio.from_signals(
            close=aligned_prices,
            entries=aligned_entries,
            exits=aligned_exits,
            fees=self.config['fees'],
            freq='D',
            cash_sharing=True,
            group_by=True
        )

        self.portfolios[name] = pf
        return pf

    def get_portfolio_metrics(self, name):
        """Get comprehensive metrics for portfolio."""
        pf = self.portfolios[name]

        return {
            'total_return': pf.total_return(),
            'sharpe_ratio': pf.sharpe_ratio(),
            'sortino_ratio': pf.sortino_ratio(),
            'max_drawdown': pf.max_drawdown(),
            'win_rate': pf.trades.win_rate() if len(pf.trades.records) > 0 else 0,
            'profit_factor': pf.trades.profit_factor() if len(pf.trades.records) > 0 else 0,
            'total_trades': len(pf.trades.records)
        }

# ============================================================
# PHASE 4: RISK ANALYSIS (Pyfolio)
# ============================================================

import pyfolio as pf

class RiskAnalysis:
    """Risk analysis using Pyfolio."""

    def __init__(self, config):
        self.config = config

    def analyze_portfolio(self, vbt_portfolio, benchmark_prices):
        """Comprehensive risk analysis."""
        # Extract returns
        returns = vbt_portfolio.returns()

        # Calculate benchmark returns
        benchmark = benchmark_prices.pct_change().dropna()
        benchmark = benchmark.loc[returns.index]

        # Performance stats
        stats = pf.timeseries.perf_stats(returns, benchmark)

        # Drawdown analysis
        dd_table = pf.timeseries.gen_drawdown_table(returns)

        # Statistical tests
        sharpe = pf.timeseries.sharpe_ratio(returns)
        n = len(returns)
        se_sharpe = np.sqrt((1 + 0.5*sharpe**2) / n)
        t_stat = sharpe / se_sharpe

        return {
            'stats': stats,
            'drawdowns': dd_table,
            'sharpe_t_stat': t_stat,
            'sharpe_significant': abs(t_stat) > 1.96
        }

# ============================================================
# MAIN PIPELINE
# ============================================================

def run_complete_pipeline():
    """Execute complete research pipeline."""
    print("=" * 70)
    print("COMPLETE QUANTITATIVE RESEARCH PIPELINE")
    print("=" * 70)

    # Phase 1: Data Acquisition
    data_mgr = DataAcquisition(CONFIG)
    prices = data_mgr.fetch_prices()
    sectors = data_mgr.fetch_sectors()

    # Phase 2: Factor Research
    print("\nPhase 2: Factor Analysis...")
    factor_research = FactorResearch(prices, sectors, CONFIG)

    # Create and evaluate factors
    factor_research.create_momentum_factor(60)
    factor_research.create_momentum_factor(20)
    factor_research.create_mean_reversion_factor(5)

    for factor_name in factor_research.factors:
        print(f"\n  Evaluating {factor_name}...")
        result = factor_research.evaluate_factor(factor_name)
        print(f"    Mean IC: {result['mean_ic']}")
        print(f"    IR: {result['ir']}")
        print(f"    Viable: {result['viable']}")

    best_factor, best_result = factor_research.get_best_factor()
    print(f"\n  Best Factor: {best_factor}")

    if not best_factor:
        print("  No viable factors found. Exiting.")
        return

    # Phase 3: Backtesting
    print("\nPhase 3: Strategy Backtesting...")
    backtester = StrategyBacktest(prices, CONFIG)
    pf_vbt = backtester.backtest_factor_strategy(
        best_result['factor_data'],
        best_factor
    )

    metrics = backtester.get_portfolio_metrics(best_factor)
    print(f"  Total Return: {metrics['total_return']:.2%}")
    print(f"  Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
    print(f"  Max Drawdown: {metrics['max_drawdown']:.2%}")

    # Phase 4: Risk Analysis
    print("\nPhase 4: Risk Analysis...")

    # Get SPY as benchmark
    spy_data = obb.equity.price.historical(
        'SPY',
        start_date=CONFIG['start_date'],
        end_date=CONFIG['end_date'],
        provider='yfinance'
    )
    benchmark_prices = spy_data.to_dataframe()['close']

    risk_analyzer = RiskAnalysis(CONFIG)
    risk_results = risk_analyzer.analyze_portfolio(pf_vbt, benchmark_prices)

    print("\n  Performance Stats:")
    print(risk_results['stats'])
    print(f"\n  Sharpe T-Stat: {risk_results['sharpe_t_stat']:.2f}")
    print(f"  Statistically Significant: {risk_results['sharpe_significant']}")

    # Final Report
    print("\n" + "=" * 70)
    print("FINAL REPORT")
    print("=" * 70)
    print(f"Strategy: {best_factor}")
    print(f"Universe: {len(CONFIG['universe'])} stocks")
    print(f"Period: {CONFIG['start_date']} to {CONFIG['end_date']}")
    print(f"\nKey Metrics:")
    print(f"  Factor IC: {max(best_result['mean_ic'].values()):.4f}")
    print(f"  Factor IR: {max(best_result['ir'].values()):.4f}")
    print(f"  Strategy Sharpe: {metrics['sharpe_ratio']:.2f}")
    print(f"  Total Return: {metrics['total_return']:.2%}")
    print(f"  Max Drawdown: {metrics['max_drawdown']:.2%}")
    print(f"  Win Rate: {metrics['win_rate']:.1%}")

    recommendation = "VIABLE" if (
        metrics['sharpe_ratio'] > 1.0 and
        metrics['max_drawdown'] > -0.25 and
        risk_results['sharpe_significant']
    ) else "NEEDS IMPROVEMENT"

    print(f"\nRecommendation: {recommendation}")

    return {
        'factor': best_factor,
        'factor_results': best_result,
        'portfolio_metrics': metrics,
        'risk_results': risk_results
    }

# Run pipeline
if __name__ == "__main__":
    results = run_complete_pipeline()
```

---

## Data Flow Diagrams

### Factor Research Pipeline

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   OpenBB    │     │  Alphalens  │     │   Pyfolio   │
│             │     │             │     │             │
│ - Prices    │────>│ - Factor    │────>│ - Returns   │
│ - Sectors   │     │   Analysis  │     │   Analysis  │
│ - Fundmntls │     │ - IC/IR     │     │ - Risk      │
│             │     │ - Quantiles │     │   Metrics   │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Strategy Development Pipeline

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   OpenBB    │     │  VectorBT   │     │   Pyfolio   │
│             │     │             │     │             │
│ - OHLCV     │────>│ - Signals   │────>│ - Tear      │
│ - Benchmark │     │ - Portfolio │     │   Sheets    │
│             │     │ - Trades    │     │ - Risk      │
│             │     │ - Metrics   │     │   Report    │
└─────────────┘     └─────────────┘     └─────────────┘
```

---

## Best Practices for Integration

1. **Use consistent date ranges** across all libraries
2. **Align indices** when passing data between libraries
3. **Handle missing data** before integration
4. **Use same frequency** (daily, weekly) throughout
5. **Document data transformations** at each step
6. **Validate outputs** at each pipeline stage
