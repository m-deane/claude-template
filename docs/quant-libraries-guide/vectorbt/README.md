# VectorBT User Reference Guide

**Version:** 0.28.2 (latest stable)
**Python Support:** 3.6 - 3.12
**License:** Apache 2.0 + Commons Clause
**Documentation Date:** 2025-12-17

---

## Table of Contents

1. [Overview & Installation](#1-overview--installation)
2. [Complete API Reference](#2-complete-api-reference)
3. [Plotting Functions with Interpretation](#3-plotting-functions-with-interpretation)
4. [Use Cases by Skill Level](#4-use-cases-by-skill-level)
5. [Core Concepts](#5-core-concepts)
6. [Performance Optimization](#6-performance-optimization)
7. [Best Practices & Common Pitfalls](#7-best-practices--common-pitfalls)
8. [Resources](#8-resources)

---

## 1. Overview & Installation

### What is VectorBT?

VectorBT is a high-performance backtesting library for Python that leverages vectorization and Numba JIT compilation to achieve 80-100x speedups over traditional pandas-based approaches. It enables rapid testing of thousands of strategy variations through broadcasting and parallel parameter optimization.

**Key Features:**
- Vectorized backtesting (process entire arrays at once)
- Numba JIT compilation for C-level performance
- Broadcasting across 50+ parameters
- Built-in technical indicators (30+)
- Portfolio simulation with realistic constraints
- Comprehensive performance metrics
- Interactive Plotly visualizations
- Record-based sparse data structures

### Installation

**Basic Installation:**
```bash
pip install -U vectorbt
```

**With All Optional Dependencies:**
```bash
pip install -U "vectorbt[full]"
```

**Without TA-Lib (if C library unavailable):**
```bash
pip install -U "vectorbt[full-no-talib]"
```

**Core Dependencies:**
- **numpy** - Array operations and numerical computing
- **pandas** - Time series and DataFrame handling
- **numba** - JIT compilation for 80-100x performance boost
- **plotly** - Interactive visualizations

**Optional Dependencies:**
- **TA-Lib** - Technical analysis (requires C library)
- **pandas-ta** - Alternative TA library (pure Python)
- **ta** - Another TA library
- **yfinance** - Yahoo Finance data
- **ccxt** - Cryptocurrency exchange integration
- **alpaca-trade-api** - Alpaca broker

### VectorBT vs VectorBT PRO

| Feature | Free (vectorbt) | PRO (vectorbtpro) |
|---------|----------------|-------------------|
| Status | Maintenance mode | Active development |
| Price | Free (Apache 2.0 + Commons Clause) | Paid subscription |
| Indicators | ~30 built-in | 500+ |
| Portfolio Optimization | No | Yes |
| Parallelization | No | Yes |
| Limit Orders | No | Yes |
| Pattern Recognition | No | Yes |
| Access | Public GitHub | Private repository |
| Support | Community | Priority support |

**Note:** This guide covers the free version unless otherwise specified.

---

## 2. Complete API Reference

### 2.1 Portfolio Class

**Import:** `from vectorbt.portfolio import Portfolio` or `vbt.Portfolio`

The Portfolio class is the core of VectorBT's backtesting functionality. It provides four methods for creating portfolio simulations, each with different trade-offs between simplicity and flexibility.

#### 2.1.1 Portfolio.from_signals()

Create portfolio from entry/exit signals with automatic signal management.

**Full Signature:**
```python
Portfolio.from_signals(
    # Core inputs
    close,                      # Asset prices (required)
    entries=None,               # Long entry signals (bool array)
    exits=None,                 # Long exit signals (bool array)
    short_entries=None,         # Short entry signals
    short_exits=None,           # Short exit signals

    # Signal customization
    signal_func_nb=nb.no_signal_func_nb,  # Custom Numba signal function
    signal_args=(),             # Args for signal function

    # Order sizing
    size=None,                  # Order size (default: np.inf)
    size_type=None,             # Amount, Value, Percent, TargetAmount, etc.

    # Execution prices
    price=None,                 # Execution price (default: close)

    # Costs
    fees=None,                  # Transaction fees (broadcastable)
    fixed_fees=None,            # Fixed fees per order
    slippage=None,              # Slippage percentage

    # Order constraints
    min_size=None,              # Minimum order size
    max_size=None,              # Maximum order size
    size_granularity=None,      # Size rounding
    reject_prob=None,           # Rejection probability
    lock_cash=None,             # Lock cash for orders
    allow_partial=None,         # Allow partial fills
    raise_reject=None,          # Raise on rejection

    # Logging
    log=None,                   # Enable detailed logs

    # Signal behavior
    accumulate=None,            # Allow position stacking
    upon_long_conflict=None,    # Handle long conflicts
    upon_short_conflict=None,   # Handle short conflicts
    upon_dir_conflict=None,     # Handle direction conflicts
    upon_opposite_entry=None,   # Handle opposite entries
    direction=None,             # Long, Short, All

    # Valuation
    val_price=None,             # Valuation price

    # Stop orders (OHLC data for stops)
    open=None,                  # Open prices
    high=None,                  # High prices
    low=None,                   # Low prices
    sl_stop=None,               # Stop loss level
    sl_trail=None,              # Trailing stop flag
    tp_stop=None,               # Take profit level
    stop_entry_price=None,      # Entry stop price
    stop_exit_price=None,       # Exit stop price
    upon_stop_exit=None,        # Stop exit action
    upon_stop_update=None,      # Stop update action
    adjust_sl_func_nb=nb.no_adjust_sl_func_nb,  # SL adjustment
    adjust_sl_args=(),
    adjust_tp_func_nb=nb.no_adjust_tp_func_nb,  # TP adjustment
    adjust_tp_args=(),
    use_stops=None,             # Enable stops

    # Capital management
    init_cash=None,             # Starting cash (numeric/'auto'/'autoalign')
    cash_sharing=None,          # Share cash in groups

    # Execution control
    call_seq=None,              # Custom call sequence
    ffill_val_price=None,       # Forward-fill prices (default: True)
    update_value=None,          # Update value each bar
    max_orders=None,            # Max orders to allocate
    max_logs=None,              # Max log entries
    seed=None,                  # Random seed

    # Grouping
    group_by=None,              # Column grouping

    # Advanced
    broadcast_named_args=None,
    broadcast_kwargs=None,
    template_mapping=None,
    wrapper_kwargs=None,

    # Metadata
    freq=None,                  # Time frequency ('D', 'H', etc.)
    attach_call_seq=None,
    **kwargs
)
```

**Key Features:**
- Prevents duplicate entries by default (set `accumulate=True` to allow)
- Built-in stop-loss and take-profit
- Automatic conflict resolution
- Broadcasting across 50+ parameters
- Integrates with indicators seamlessly

**Example:**
```python
import vectorbt as vbt

# Download data
data = vbt.YFData.download('AAPL', start='2020-01-01')
close = data.get('Close')

# Generate signals
fast_ma = vbt.MA.run(close, 10)
slow_ma = vbt.MA.run(close, 50)
entries = fast_ma.ma_crossed_above(slow_ma)
exits = fast_ma.ma_crossed_below(slow_ma)

# Backtest
pf = vbt.Portfolio.from_signals(
    close=close,
    entries=entries,
    exits=exits,
    fees=0.001,          # 0.1% fees
    sl_stop=0.02,        # 2% stop loss
    freq='D'             # Daily data
)

# Analyze
print(pf.stats())
pf.plot().show()
```

#### 2.1.2 Portfolio.from_orders()

Create portfolio from predefined orders (fastest and most straightforward).

**Full Signature:**
```python
Portfolio.from_orders(
    close,                      # Asset prices (required)
    size=None,                  # Order sizes (broadcastable)
    size_type=None,             # Amount, Value, Percent, etc.
    direction=None,             # Long, Short, All
    price=None,                 # Execution prices
    fees=None,                  # Transaction fees
    fixed_fees=None,
    slippage=None,
    min_size=None,
    max_size=None,
    size_granularity=None,
    reject_prob=None,
    lock_cash=None,
    allow_partial=None,
    raise_reject=None,
    log=None,
    val_price=None,
    init_cash=None,
    cash_sharing=None,
    call_seq=None,
    ffill_val_price=None,
    update_value=None,
    max_orders=None,
    max_logs=None,
    seed=None,
    group_by=None,
    broadcast_kwargs=None,
    wrapper_kwargs=None,
    freq=None,
    attach_call_seq=None,
    **kwargs
)
```

**When to Use:**
- You have explicit order sizes/directions
- Maximum performance needed
- Simple strategy logic
- No complex dependencies

**Example:**
```python
import numpy as np

# Buy 10 shares every day close is positive
size = np.where(close.pct_change() > 0, 10, 0)

pf = vbt.Portfolio.from_orders(
    close=close,
    size=size,
    price=close,
    fees=0.001,
    freq='D'
)

print(f"Total Return: {pf.total_return():.2%}")
```

#### 2.1.3 Portfolio.from_order_func()

Maximum flexibility using custom order generation functions.

**Key Parameters:**
```python
Portfolio.from_order_func(
    close,
    order_func_nb,              # Numba function (required)
    flexible=False,             # Multiple orders per bar?
    pre_sim_func_nb=None,       # Pre-simulation setup
    pre_segment_func_nb=None,   # Pre-segment callback
    post_segment_func_nb=None,  # Post-segment callback
    # ... (similar to from_orders)
)
```

**Order Function Signature:**
```python
from numba import njit
from vectorbt.portfolio.enums import Order, NoOrder

@njit
def order_func_nb(c, *args):
    """
    c: context object with:
        - c.i: current bar index
        - c.col: current column
        - c.cash_now: available cash
        - c.position_now: current position
        - c.value_now: portfolio value
        - c.close: price array
        - ... (many more context variables)

    Returns: Order namedtuple or NoOrder
    """
    # Your logic here
    return Order(size=10, price=c.close[c.i, c.col])
```

**When to Use:**
- Complex strategy logic
- Dependencies between orders
- Custom money management
- Multiple orders per bar (flexible=True)
- Advanced portfolio rebalancing

**Example:**
```python
from numba import njit
from vectorbt.portfolio.enums import Order, NoOrder

@njit
def rsi_order_func_nb(c, rsi, threshold_low, threshold_high):
    """Buy on oversold, sell on overbought"""
    current_rsi = rsi[c.i, c.col]

    if current_rsi < threshold_low and c.position_now == 0:
        # Buy with all cash
        size = c.cash_now / c.close[c.i, c.col]
        return Order(size=size, price=c.close[c.i, c.col])

    elif current_rsi > threshold_high and c.position_now > 0:
        # Sell entire position
        return Order(size=-c.position_now, price=c.close[c.i, c.col])

    return NoOrder

# Run simulation
rsi = vbt.RSI.run(close, 14).rsi
pf = vbt.Portfolio.from_order_func(
    close=close,
    order_func_nb=rsi_order_func_nb,
    rsi=rsi.values,
    threshold_low=30,
    threshold_high=70,
    freq='D'
)

print(pf.stats())
```

#### 2.1.4 Portfolio.from_holding()

Simple buy-and-hold strategy.

```python
Portfolio.from_holding(
    close,
    bm_close=None,              # Benchmark for comparison
    init_cash=None,
    freq=None,
    **kwargs
)
```

**Example:**
```python
# Buy and hold with benchmark
spy = vbt.YFData.download('SPY', start='2020-01-01').get('Close')
aapl = vbt.YFData.download('AAPL', start='2020-01-01').get('Close')

pf = vbt.Portfolio.from_holding(
    close=aapl,
    bm_close=spy,    # Compare against S&P 500
    freq='D'
)

pf.plot_returns(benchmark_returns=pf.benchmark_returns).show()
```

### 2.2 Portfolio Properties

**Core Data:**
```python
pf.cash()           # Cash balance over time (DataFrame)
pf.assets()         # Asset holdings over time (DataFrame)
pf.value()          # Total portfolio value (Series)
pf.returns()        # Period returns (Series)
```

**Records:**
```python
pf.orders           # Orders instance
pf.trades           # Trades instance
pf.entry_trades     # EntryTrades instance
pf.exit_trades      # ExitTrades instance
pf.positions        # Positions instance
pf.drawdowns        # Drawdowns instance
pf.logs             # Logs (if log=True)
```

**Metadata:**
```python
pf.close            # Close prices used
pf.init_cash        # Initial capital
pf.cash_sharing     # Cash sharing enabled?
pf.wrapper          # ArrayWrapper instance
```

### 2.3 Portfolio Metrics

**Return Metrics:**
```python
pf.total_return()           # Cumulative return
pf.annualized_return()      # CAGR
pf.cumulative_returns()     # Growth curve
pf.daily_returns()          # Daily bucketed
pf.annual_returns()         # Annual bucketed
```

**Risk Metrics:**
```python
pf.annualized_volatility()  # Std dev (annualized)
pf.downside_risk()          # Downside volatility
pf.max_drawdown()           # Maximum DD
pf.drawdown()               # DD series
pf.value_at_risk()          # VaR
pf.cond_value_at_risk()     # CVaR
```

**Risk-Adjusted:**
```python
pf.sharpe_ratio()           # Sharpe ratio
pf.sortino_ratio()          # Sortino ratio
pf.calmar_ratio()           # Calmar ratio
pf.omega_ratio()            # Omega ratio
pf.information_ratio()      # Information ratio
pf.deflated_sharpe_ratio()  # Haircut Sharpe
pf.common_sense_ratio()     # Common Sense Ratio
```

**Benchmark Comparison:**
```python
pf.beta()                   # Beta vs benchmark
pf.alpha()                  # Alpha vs benchmark
pf.capture()                # Capture ratio
pf.up_capture()             # Upside capture
pf.down_capture()           # Downside capture
pf.tail_ratio()             # Tail ratio
```

**Trade Analysis:**
```python
pf.final_value()            # Ending value
pf.total_profit()           # Total P&L
pf.win_rate()               # Win percentage
pf.profit_factor()          # Profit factor
pf.expectancy()             # Expected value
pf.sqn()                    # System Quality Number
```

### 2.4 Portfolio Stats Method

**Comprehensive Analysis:**
```python
pf.stats(
    column=None,        # Select column/group
    metrics=None,       # List of metrics (default: all)
    agg_func=None,      # Aggregation function
    group_by=None,      # Override grouping
    settings=None,      # Custom settings
    tags=None          # Filter by tags ('returns', 'trades', etc.)
)
```

**Example:**
```python
# All stats
print(pf.stats())

# Only return metrics
print(pf.stats(tags='returns'))

# Specific metrics
print(pf.stats(metrics=['sharpe_ratio', 'max_drawdown', 'win_rate']))

# For specific column
print(pf['AAPL'].stats())
```

### 2.5 Record Classes

#### 2.5.1 Orders Class

**Access:** `portfolio.orders`

**Fields:**
```python
orders.id           # Order identifier
orders.col          # Column index
orders.idx          # Timestamp index
orders.size         # Order size (signed)
orders.price        # Execution price
orders.fees         # Transaction fees
orders.side         # 0=Buy, 1=Sell
```

**Filtering:**
```python
orders.buy          # Buy orders only
orders.sell         # Sell orders only
```

**Methods:**
```python
orders.stats()              # Summary statistics
orders.plot()               # Visualize orders
orders.records_readable     # Convert to DataFrame
```

**Example:**
```python
# Analyze orders
print(pf.orders.stats())

# Get all buy orders
buy_orders = pf.orders.buy
print(f"Total buys: {len(buy_orders)}")

# Plot orders on price chart
pf.orders.plot().show()
```

#### 2.5.2 Trades Class

**Access:** `portfolio.trades`

**Fields:**
```python
trades.entry_idx        # Entry timestamp
trades.entry_price      # Entry price
trades.entry_fees       # Entry fees
trades.exit_idx         # Exit timestamp
trades.exit_price       # Exit price
trades.exit_fees        # Exit fees
trades.size             # Position size
trades.pnl              # Profit/loss
trades.returns          # Return %
trades.direction        # 0=Long, 1=Short
trades.parent_id        # Parent position ID
```

**Classification:**
```python
trades.long             # Long trades
trades.short            # Short trades
trades.winning          # Profitable trades
trades.losing           # Losing trades
trades.winning_streak   # Win streaks
trades.losing_streak    # Loss streaks
```

**Metrics:**
```python
trades.win_rate()           # Win percentage
trades.profit_factor()      # Profit factor
trades.expectancy()         # Expected value
trades.sqn()                # SQN
```

**Plotting:**
```python
trades.plot()               # Trade visualization
trades.plot_pnl()           # P&L chart
trades.plots()              # Multiple subplots
```

**Example:**
```python
# Analyze trades
print(pf.trades.stats())

# Get winning trades
winners = pf.trades.winning
print(f"Winners: {len(winners)} ({pf.trades.win_rate():.1%})")

# Analyze by direction
print(f"Long win rate: {pf.trades.long.win_rate():.1%}")
print(f"Short win rate: {pf.trades.short.win_rate():.1%}")

# Plot trades
pf.trades.plot().show()
```

#### 2.5.3 EntryTrades, ExitTrades, Positions

**Three Trade Types:**
```python
pf.entry_trades     # Individual entry orders → trades
pf.exit_trades      # Individual exit orders → trades
pf.positions        # Aggregated entry/exit sequences
```

**Switching Between Types:**
```python
# Change trade type
pf_positions = pf.replace(trades_type='Positions')
pf_entries = pf.replace(trades_type='EntryTrades')

# Include open trades
pf.trades.replace(incl_open=True)
```

**Use Cases:**
- **EntryTrades:** Analyze entry timing and prices
- **ExitTrades:** Analyze exit timing and prices
- **Positions:** Full lifecycle analysis (default)

#### 2.5.4 Drawdowns Class

**Access:** `portfolio.drawdowns` or `vbt.Drawdowns.from_ts(series)`

**Fields:**
```python
dd.peak_idx             # Peak index
dd.peak_val             # Peak value
dd.valley_idx           # Valley index
dd.valley_val           # Valley value
dd.end_idx              # Recovery end index
dd.end_val              # End value
dd.status               # 0=Active, 1=Recovered
dd.decline_duration     # Peak → valley time
dd.recovery_duration    # Valley → recovery time
```

**Filtering:**
```python
dd.active               # Currently recovering
dd.recovered            # Fully recovered
```

**Metrics:**
```python
dd.max_drawdown()               # MDD
dd.avg_drawdown()               # Average DD
dd.active_drawdown()            # Current DD
dd.active_duration()            # Current DD duration
dd.max_recovery_return()        # Best recovery
dd.avg_recovery_return()        # Avg recovery
```

**Important:** Drawdowns include BOTH active and recovered. Filter as needed!

**Example:**
```python
# Get drawdowns
dd = pf.drawdowns

# Maximum drawdown
print(f"MDD: {dd.max_drawdown():.2%}")

# Current drawdown
if len(dd.active) > 0:
    print(f"Active DD: {dd.active_drawdown():.2%}")
    print(f"Duration: {dd.active_duration()} days")

# Analyze recovered drawdowns only
recovered = dd.recovered
print(f"Avg recovery time: {recovered.recovery_duration.mean()}")

# Plot top 5 drawdowns
dd.plot(top_n=5).show()
```

### 2.6 Indicators

#### 2.6.1 Built-in Indicators (30+)

**Import:** `import vectorbt as vbt`

**Available Indicators:**
```python
vbt.MA              # Moving Average
vbt.MACD            # MACD
vbt.RSI             # RSI
vbt.BBANDS          # Bollinger Bands
vbt.ATR             # Average True Range
vbt.STOCH           # Stochastic
vbt.OBV             # On-Balance Volume
vbt.MSTD            # Moving Std Dev

# Stop-based generators
vbt.OHLCSTX         # OHLC stops
vbt.OHLCSTCX        # Chained OHLC stops
vbt.STX             # Generic stops
vbt.STCX            # Chained stops

# Random/probability generators
vbt.RAND, vbt.RANDX, vbt.RANDNX
vbt.RPROB, vbt.RPROBX, vbt.RPROBCX, vbt.RPROBNX

# Others
vbt.FMAX, vbt.FMIN, vbt.FMEAN, vbt.FSTD
vbt.BOLB, vbt.FIXLB, vbt.LEXLB, vbt.MEANLB, vbt.TRENDLB
```

#### 2.6.2 Using Built-in Indicators

**Basic Usage:**
```python
# Single parameter
ma = vbt.MA.run(close, window=20)
ma.ma  # Access output

# Multiple parameters (broadcasting)
ma = vbt.MA.run(close, window=[10, 20, 50, 100, 200])
ma.ma  # DataFrame with 5 columns

# Parameter combinations
ma_fast = vbt.MA.run(close, window=[10, 20])
ma_slow = vbt.MA.run(close, window=[50, 100])
# Creates 2×2=4 combinations
```

**Signal Generation:**
```python
# Crossovers
fast_ma = vbt.MA.run(close, 10)
slow_ma = vbt.MA.run(close, 50)

entries = fast_ma.ma_crossed_above(slow_ma)
exits = fast_ma.ma_crossed_below(slow_ma)

# Comparisons
rsi = vbt.RSI.run(close, 14)
entries = rsi.rsi_below(30)     # Oversold
exits = rsi.rsi_above(70)       # Overbought

# Logical combinations
entries = rsi.rsi_below(30) & macd.macd_above(macd.signal)
```

**Common Methods on Indicators:**
```python
ind.run(*inputs, **params)      # Run indicator
ind.run_combs(*inputs, **params) # Parameter combinations
ind.plot()                      # Visualize
ind.*_above(threshold)          # Above comparison
ind.*_below(threshold)          # Below comparison
ind.*_crossed_above(other)      # Crossover up
ind.*_crossed_below(other)      # Crossover down
ind.*_equal(value)              # Equality
ind.*_and(other)                # Logical AND
ind.*_or(other)                 # Logical OR
ind.*_xor(other)                # Logical XOR
```

#### 2.6.3 External Library Integration

**TA-Lib:**
```python
# Create indicator from TA-Lib
SMA = vbt.IndicatorFactory.from_talib('SMA')
sma = SMA.run(close, timeperiod=[10, 20, 30])

# Or shortcut
sma = vbt.talib('SMA').run(close, timeperiod=[10, 20, 30])
```

**pandas-ta:**
```python
# From pandas-ta
sma = vbt.pandas_ta('SMA').run(close, [10, 20, 30])
```

**ta library:**
```python
# From ta
sma_ind = vbt.ta('SMAIndicator')
sma = sma_ind.run(close, window=[10, 20, 30])
```

**Advantages of vectorbt wrappers:**
- Broadcasting support
- Works with DataFrames
- Handles missing values
- Resampling support
- Integration with Portfolio

#### 2.6.4 Custom Indicators

**IndicatorFactory - Create Your Own:**

```python
from vectorbt import IndicatorFactory

# Define calculation function
def my_indicator(close, window, multiplier):
    """Custom indicator logic"""
    ma = close.rolling(window).mean()
    upper = ma * multiplier
    return upper

# Create indicator class
MyInd = IndicatorFactory(
    class_name='MyIndicator',
    short_name='my_ind',
    input_names=['close'],
    param_names=['window', 'multiplier'],
    output_names=['upper']
).from_apply_func(my_indicator)

# Use it
result = MyInd.run(close, window=[10, 20], multiplier=[1.1, 1.2])
# Creates 2×2=4 parameter combinations

# Generate signals
entries = result.upper_crossed_above(close)
```

**Numba-Optimized Custom Indicator:**

```python
from numba import njit
import numpy as np

@njit
def my_nb_func(close, window):
    """Numba-compiled for speed"""
    out = np.empty_like(close)
    for i in range(len(close)):
        if i < window:
            out[i] = np.nan
        else:
            out[i] = np.mean(close[i-window:i])
    return out

MyFastInd = IndicatorFactory(
    class_name='MyFastIndicator',
    input_names=['close'],
    param_names=['window'],
    output_names=['value']
).from_apply_func(my_nb_func)
```

**Factory Parameters:**
```python
IndicatorFactory(
    class_name='IndicatorName',     # Class name
    short_name='ind',               # Short identifier
    input_names=['close', 'volume'], # Input parameters
    param_names=['window', 'threshold'], # Tunable parameters
    output_names=['signal', 'value'],    # Outputs
    takes_1d=False                  # Process column-by-column?
)
```

### 2.7 Signals Module

#### 2.7.1 Signal Generators

**OHLC-based Stop Signals:**

```python
# OHLCSTX - Stop loss/take profit exits
exits, stop_price, stop_type = vbt.OHLCSTX.run(
    entries=entries,
    open=open_prices,
    high=high_prices,
    low=low_prices,
    close=close_prices,
    sl_stop=0.02,       # 2% stop loss
    sl_trail=True,      # Trailing stop
    tp_stop=0.05        # 5% take profit
)

# OHLCSTCX - Chained (generates new entries too)
new_entries, exits = vbt.OHLCSTCX.run(
    entries=initial_entries,
    # ... same params
)
```

**Generic Stop Signals:**

```python
# STX - Stop based on any time series
exits = vbt.STX.run(
    entries=entries,
    ts=close,
    stop_list=[0.98, 0.95],  # 2% and 5% stops
    trailing_list=[True, False]
)
```

**Random Signals (for testing):**

```python
# RAND - Random entries
entries = vbt.RAND.run(close.shape, n_list=[10, 20])

# RANDX - Random entry/exit pairs
entries, exits = vbt.RANDX.run(close.shape, n_list=[10, 20])
```

**Probability-based:**

```python
# RPROB - Probability-based entries
entries = vbt.RPROB.run(close.shape, prob_list=[0.1, 0.2])

# RPROBX - Entry/exit with probabilities
entries, exits = vbt.RPROBX.run(
    close.shape,
    prob_list=[0.1, 0.2]
)

# RPROBNX - Independent entry/exit probabilities
entries, exits = vbt.RPROBNX.run(
    close.shape,
    entry_prob_list=[0.1],
    exit_prob_list=[0.3]
)
```

#### 2.7.2 Signal Operations

**Logical Combinations:**
```python
# AND
combined = signal1.vbt.signals.AND(signal2)

# OR
combined = signal1.vbt.signals.OR(signal2)

# XOR
combined = signal1.vbt.signals.XOR(signal2)

# Using operators
combined = signal1 & signal2  # AND
combined = signal1 | signal2  # OR
```

### 2.8 Data Module

#### 2.8.1 Data Class

**Base class for data storage and management:**

```python
from vectorbt.data import Data

# Override download method
class MyData(Data):
    @classmethod
    def download_symbol(cls, symbol, **kwargs):
        # Your download logic
        return dataframe

# Align data
Data.align_columns(data_dict, missing='raise')
Data.align_index(data_dict, missing='nan')
```

#### 2.8.2 YFData - Yahoo Finance

**Download Data:**

```python
import vectorbt as vbt

# Single symbol
data = vbt.YFData.download('AAPL', start='2020-01-01', end='2023-01-01')

# Multiple symbols
data = vbt.YFData.download(
    ['AAPL', 'GOOGL', 'MSFT'],
    start='2020-01-01 UTC',
    end='2023-01-01 UTC'
)

# Cryptocurrency
crypto_data = vbt.YFData.download(
    ['BTC-USD', 'ETH-USD'],
    start='2020-01-01 UTC',
    end='2023-01-01 UTC'
)
```

**Access Data:**

```python
# Get specific columns
close = data.get('Close')
volume = data.get('Volume')
ohlcv = data.get()  # All data

# Update data
data.update()
```

**Important Notes:**
- Yahoo data may have gaps and noise
- Only for demonstration - not production
- Stocks: +0500 timezone
- Crypto: UTC timezone

#### 2.8.3 Other Data Sources

```python
# Binance
from vectorbt.data.custom import BinanceData
binance_data = BinanceData.download(['BTCUSDT', 'ETHUSDT'], ...)

# CCXT (multiple exchanges)
from vectorbt.data.custom import CCXTData
ccxt_data = CCXTData.download(['BTC/USD', 'ETH/USD'], exchange='binance', ...)

# Alpaca
from vectorbt.data.custom import AlpacaData
alpaca_data = AlpacaData.download(['AAPL', 'GOOGL'], ...)

# Synthetic data
from vectorbt.data.custom import SyntheticData
synthetic = SyntheticData.download(['random_walk'], ...)
```

### 2.9 Returns Accessor

#### 2.9.1 ReturnsAccessor

**Access:** `series.vbt.returns` or `df.vbt.returns`

**Converting Price to Returns:**
```python
# Method 1: pandas
returns = close.pct_change()

# Method 2: vectorbt
returns = close.vbt.to_returns()

# Method 3: from_value
returns_accessor = pd.Series.vbt.returns.from_value(close, freq='D')
```

#### 2.9.2 Return Metrics

```python
# Basic returns
returns.vbt.returns.total_return()          # Cumulative
returns.vbt.returns.annualized_return()     # CAGR
returns.vbt.returns.annual                  # Alias for annualized
returns.vbt.returns.cumulative_returns()    # Growth curve
returns.vbt.returns.daily_returns()         # Daily bucketed
returns.vbt.returns.annual_returns()        # Annual bucketed
```

#### 2.9.3 Risk Metrics

```python
# Volatility
returns.vbt.returns.annualized_volatility(
    levy_alpha=2.0,     # Levy exponent
    ddof=1              # Degrees of freedom
)
returns.vbt.returns.downside_risk()         # Downside vol

# Drawdown
returns.vbt.returns.max_drawdown()          # MDD
returns.vbt.returns.drawdown()              # DD series

# VaR/CVaR
returns.vbt.returns.value_at_risk()         # VaR
returns.vbt.returns.cond_value_at_risk()    # CVaR
```

#### 2.9.4 Risk-Adjusted Metrics

```python
# Sharpe family
returns.vbt.returns.sharpe_ratio()
returns.vbt.returns.deflated_sharpe_ratio()
returns.vbt.returns.sortino_ratio()

# Other ratios
returns.vbt.returns.calmar_ratio()
returns.vbt.returns.omega_ratio()
returns.vbt.returns.information_ratio()
returns.vbt.returns.common_sense_ratio()
```

#### 2.9.5 Benchmark Comparison

```python
# Requires benchmark returns
returns.vbt.returns.beta(benchmark_returns)
returns.vbt.returns.alpha(benchmark_returns)
returns.vbt.returns.capture(benchmark_returns)
returns.vbt.returns.up_capture(benchmark_returns)
returns.vbt.returns.down_capture(benchmark_returns)
returns.vbt.returns.tail_ratio()
```

#### 2.9.6 Rolling Metrics

**Numba-compiled rolling versions available:**
```python
from vectorbt.returns import nb

# Rolling Sharpe
rolling_sharpe = nb.rolling_sharpe_ratio_nb(returns, window=252)

# Rolling Sortino
rolling_sortino = nb.rolling_sortino_ratio_nb(returns, window=252)

# And more...
nb.rolling_downside_risk_nb()
nb.rolling_information_ratio_nb()
nb.rolling_down_capture_nb()
```

---

## 3. Plotting Functions with Interpretation

### 3.1 Portfolio Plots

#### 3.1.1 Portfolio Value Plot

```python
pf.plot_value()
```

**What it shows:**
- Portfolio value over time
- Starting value (typically 10,000)
- Ending value
- Growth trajectory

**How to interpret:**
- **Upward trend:** Profitable strategy
- **Flat/downward:** Losing strategy
- **Smoothness:** Lower volatility
- **Steep sections:** High volatility periods

**Example:**
```python
fig = pf.plot_value()
fig.update_layout(title='Portfolio Value Over Time')
fig.show()
```

#### 3.1.2 Portfolio Returns Distribution

```python
pf.plot_returns()
```

**What it shows:**
- Histogram of returns
- Distribution shape
- Return frequency

**How to interpret:**
- **Center:** Average return
- **Width:** Volatility
- **Tails:** Extreme events
- **Skew:** Asymmetric returns
- **Fat tails:** Black swan risk

#### 3.1.3 Drawdown Plot

```python
pf.plot_drawdowns(top_n=5)
```

**What it shows:**
- Top N largest drawdowns
- Duration of each drawdown
- Recovery periods
- Active drawdowns

**How to interpret:**
- **Depth:** Maximum loss from peak
- **Duration:** Recovery time
- **Frequency:** How often they occur
- **Active (red):** Still in drawdown
- **Recovered (green):** Full recovery

**Example:**
```python
fig = pf.plot_drawdowns(top_n=10)
fig.update_layout(title='Top 10 Drawdown Periods')
fig.show()
```

#### 3.1.4 Underwater Plot

```python
pf.plot_underwater()
```

**What it shows:**
- Continuous drawdown curve
- Percentage below previous peak
- Recovery patterns

**How to interpret:**
- **At 0%:** New all-time high
- **Below 0%:** In drawdown
- **Deep valleys:** Major losses
- **Quick recovery:** Resilient strategy
- **Prolonged valleys:** Extended drawdowns

#### 3.1.5 Complete Dashboard

```python
pf.plot()
```

**What it shows:**
- Comprehensive multi-panel dashboard
- Value, orders, returns, drawdowns
- All-in-one visualization

**Example:**
```python
fig = pf.plot()
fig.update_layout(height=1000)
fig.show()
```

### 3.2 Trade Plots

#### 3.2.1 Trade Markers

```python
pf.trades.plot()
```

**What it shows:**
- Entry points (green triangles)
- Exit points (red triangles)
- Price during trades
- Trade overlay on price chart

**How to interpret:**
- **Entry quality:** Buying dips vs peaks
- **Exit quality:** Selling peaks vs dips
- **Timing:** Entry/exit synchronization
- **Density:** Trade frequency

#### 3.2.2 Trade P&L

```python
pf.trades.plot_pnl()
```

**What it shows:**
- Profit/loss per trade
- Win/loss distribution
- Trade sequence

**How to interpret:**
- **Above zero:** Winning trades
- **Below zero:** Losing trades
- **Consistency:** Win/loss pattern
- **Outliers:** Exceptional trades

**Example:**
```python
fig = pf.trades.plot_pnl()
fig.update_layout(title='Per-Trade Profit/Loss')
fig.show()
```

### 3.3 Indicator Plots

```python
# Moving Average
ma = vbt.MA.run(close, 20)
ma.plot()

# RSI
rsi = vbt.RSI.run(close, 14)
rsi.plot()

# Bollinger Bands
bb = vbt.BBANDS.run(close, window=20)
bb.plot()
```

**What they show:**
- Indicator values over time
- Overlay on price (MA, BB)
- Separate panel (RSI, MACD)

**How to interpret:**
- **MA:** Trend direction
- **RSI:** Overbought/oversold
- **BB:** Volatility and extremes
- **MACD:** Momentum shifts

---

## 4. Use Cases by Skill Level

### 4.1 BEGINNER: Simple MA Crossover Strategy

**Goal:** Learn basic signal generation and backtesting

```python
import vectorbt as vbt
import pandas as pd

# Step 1: Download data
data = vbt.YFData.download('AAPL', start='2020-01-01', end='2023-01-01')
close = data.get('Close')

# Step 2: Calculate indicators
fast_ma = vbt.MA.run(close, window=10)
slow_ma = vbt.MA.run(close, window=50)

# Step 3: Generate signals
entries = fast_ma.ma_crossed_above(slow_ma)
exits = fast_ma.ma_crossed_below(slow_ma)

# Step 4: Backtest
pf = vbt.Portfolio.from_signals(
    close=close,
    entries=entries,
    exits=exits,
    fees=0.001,      # 0.1% commission
    freq='D'         # Daily frequency
)

# Step 5: Analyze results
print("=" * 50)
print("STRATEGY PERFORMANCE")
print("=" * 50)
print(f"Total Return: {pf.total_return():.2%}")
print(f"Sharpe Ratio: {pf.sharpe_ratio():.2f}")
print(f"Max Drawdown: {pf.max_drawdown():.2%}")
print(f"Win Rate: {pf.trades.win_rate():.2%}")
print(f"Total Trades: {pf.trades.count()}")

# Step 6: Visualize
fig = pf.plot()
fig.show()

# Compare to buy-and-hold
bh = vbt.Portfolio.from_holding(close, freq='D')
print(f"\nBuy & Hold Return: {bh.total_return():.2%}")
print(f"Strategy Outperformance: {pf.total_return() - bh.total_return():.2%}")
```

**Key Learnings:**
- Data download and preparation
- Indicator calculation
- Signal generation
- Portfolio creation
- Performance analysis
- Visualization

### 4.2 INTERMEDIATE: Parameter Optimization with Grid Search

**Goal:** Find optimal strategy parameters

```python
import vectorbt as vbt
import numpy as np
import pandas as pd

# Download data
data = vbt.YFData.download('AAPL', start='2020-01-01', end='2023-01-01')
close = data.get('Close')

# Define parameter ranges
fast_windows = np.arange(5, 50, 5)      # [5, 10, 15, ..., 45]
slow_windows = np.arange(50, 200, 10)   # [50, 60, 70, ..., 190]

print(f"Testing {len(fast_windows)} × {len(slow_windows)} = {len(fast_windows) * len(slow_windows)} combinations")

# Calculate indicators (broadcasting creates all combinations)
fast_ma = vbt.MA.run(close, window=fast_windows)
slow_ma = vbt.MA.run(close, window=slow_windows)

# Generate signals for all combinations
entries = fast_ma.ma_crossed_above(slow_ma)
exits = fast_ma.ma_crossed_below(slow_ma)

# Backtest all combinations at once
pf = vbt.Portfolio.from_signals(
    close=close,
    entries=entries,
    exits=exits,
    fees=0.001,
    freq='D'
)

# Analyze results across all combinations
sharpe_ratios = pf.sharpe_ratio()
total_returns = pf.total_return()
max_drawdowns = pf.max_drawdown()
win_rates = pf.trades.win_rate()

# Find best parameters by different metrics
best_sharpe = sharpe_ratios.idxmax()
best_return = total_returns.idxmax()
best_dd = max_drawdowns.idxmin()  # Minimum drawdown

print("\n" + "=" * 60)
print("OPTIMIZATION RESULTS")
print("=" * 60)
print(f"\nBest Sharpe Ratio: {sharpe_ratios.max():.2f}")
print(f"  Parameters: Fast={best_sharpe[0]}, Slow={best_sharpe[1]}")

print(f"\nBest Total Return: {total_returns.max():.2%}")
print(f"  Parameters: Fast={best_return[0]}, Slow={best_return[1]}")

print(f"\nLowest Drawdown: {max_drawdowns.min():.2%}")
print(f"  Parameters: Fast={best_dd[0]}, Slow={best_dd[1]}")

# Analyze best Sharpe strategy in detail
best_pf = pf[best_sharpe]
print("\n" + "=" * 60)
print("BEST SHARPE STRATEGY DETAILS")
print("=" * 60)
print(best_pf.stats())

# Visualize best strategy
fig = best_pf.plot()
fig.update_layout(title=f'Best Strategy: Fast={best_sharpe[0]}, Slow={best_sharpe[1]}')
fig.show()

# Create heatmap of results
import plotly.graph_objects as go

# Reshape results for heatmap
sharpe_matrix = sharpe_ratios.unstack()

fig = go.Figure(data=go.Heatmap(
    z=sharpe_matrix.values,
    x=sharpe_matrix.columns,
    y=sharpe_matrix.index,
    colorscale='RdYlGn',
    colorbar=dict(title='Sharpe Ratio')
))

fig.update_layout(
    title='Sharpe Ratio Heatmap',
    xaxis_title='Slow MA Window',
    yaxis_title='Fast MA Window',
    height=600
)
fig.show()
```

**Key Learnings:**
- Parameter grid creation
- Broadcasting for optimization
- Multi-dimensional analysis
- Heatmap visualization
- Metric comparison
- Overfitting awareness

### 4.3 ADVANCED: Custom Order Function with Position Sizing

**Goal:** Implement sophisticated risk management

```python
import vectorbt as vbt
import numpy as np
from numba import njit
from vectorbt.portfolio.enums import Order, NoOrder

# Download data
data = vbt.YFData.download('AAPL', start='2020-01-01', end='2023-01-01')
close = data.get('Close')

# Calculate indicators
rsi = vbt.RSI.run(close, 14).rsi
bb = vbt.BBANDS.run(close, window=20, alpha=2)
atr = vbt.ATR.run(data.get('High'), data.get('Low'), close, 14).atr

# Custom order function with ATR-based position sizing
@njit
def atr_position_sizing_nb(c, rsi, bb_upper, bb_lower, atr, risk_pct=0.02):
    """
    Advanced strategy:
    - Entry: RSI < 30 AND price touches lower BB
    - Exit: RSI > 70 OR price touches upper BB
    - Position sizing: Risk 2% per trade based on ATR stop
    - Stop loss: 2 × ATR
    """
    current_rsi = rsi[c.i, c.col]
    current_price = c.close[c.i, c.col]
    bb_up = bb_upper[c.i, c.col]
    bb_low = bb_lower[c.i, c.col]
    current_atr = atr[c.i, c.col]

    # Entry conditions
    entry_signal = current_rsi < 30 and current_price <= bb_low
    exit_signal = current_rsi > 70 or current_price >= bb_up

    # Not in position - check entry
    if c.position_now == 0:
        if entry_signal and not np.isnan(current_atr):
            # Calculate position size based on ATR
            # Risk = 2% of portfolio
            # Stop distance = 2 × ATR
            stop_distance = 2 * current_atr
            risk_amount = c.value_now * risk_pct
            position_size = risk_amount / stop_distance

            # Don't use more than 95% of available cash
            max_shares = (c.cash_now * 0.95) / current_price
            position_size = min(position_size, max_shares)

            if position_size > 0:
                return Order(
                    size=position_size,
                    price=current_price,
                    fees=0.001,
                    slippage=0.0005
                )

    # In position - check exit
    elif c.position_now > 0:
        if exit_signal:
            return Order(
                size=-c.position_now,
                price=current_price,
                fees=0.001,
                slippage=0.0005
            )

    return NoOrder

# Run backtest
pf = vbt.Portfolio.from_order_func(
    close=close,
    order_func_nb=atr_position_sizing_nb,
    rsi=rsi.values,
    bb_upper=bb.upper.values,
    bb_lower=bb.lower.values,
    atr=atr.values,
    risk_pct=0.02,
    freq='D'
)

# Detailed analysis
print("=" * 60)
print("ADVANCED STRATEGY PERFORMANCE")
print("=" * 60)
print(pf.stats())

print("\n" + "=" * 60)
print("TRADE ANALYSIS")
print("=" * 60)
print(pf.trades.stats())

# Risk analysis
print("\n" + "=" * 60)
print("RISK METRICS")
print("=" * 60)
print(f"Sharpe Ratio: {pf.sharpe_ratio():.2f}")
print(f"Sortino Ratio: {pf.sortino_ratio():.2f}")
print(f"Calmar Ratio: {pf.calmar_ratio():.2f}")
print(f"Max Drawdown: {pf.max_drawdown():.2%}")
print(f"Volatility: {pf.annualized_volatility():.2%}")

# Trade statistics
print("\n" + "=" * 60)
print("TRADE STATISTICS")
print("=" * 60)
print(f"Total Trades: {pf.trades.count()}")
print(f"Win Rate: {pf.trades.win_rate():.2%}")
print(f"Profit Factor: {pf.trades.profit_factor():.2f}")
print(f"Expectancy: ${pf.trades.expectancy():.2f}")

# Compare to buy-and-hold
bh = vbt.Portfolio.from_holding(close, freq='D')
print("\n" + "=" * 60)
print("COMPARISON TO BUY & HOLD")
print("=" * 60)
print(f"Strategy Return: {pf.total_return():.2%}")
print(f"B&H Return: {bh.total_return():.2%}")
print(f"Outperformance: {pf.total_return() - bh.total_return():.2%}")

# Visualize
pf.plot().show()
pf.trades.plot().show()
```

**Key Learnings:**
- Custom order functions
- ATR-based position sizing
- Risk management (2% rule)
- Multi-indicator strategies
- Advanced performance analysis
- Risk-adjusted metrics

### 4.4 EXPERT: Walk-Forward Analysis with Multi-Asset Portfolio

**Goal:** Robust strategy validation with out-of-sample testing

```python
import vectorbt as vbt
import numpy as np
import pandas as pd
from numba import njit
from vectorbt.portfolio.enums import Order, NoOrder

# Download multi-asset data
symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']
data = vbt.YFData.download(symbols, start='2018-01-01', end='2023-01-01')
close = data.get('Close')

print(f"Data shape: {close.shape}")
print(f"Symbols: {symbols}")

# Walk-forward parameters
window_len = 252 * 2  # 2-year windows
train_ratio = 0.7      # 70% train, 30% validation

# Split data into rolling windows
splits = close.vbt.rolling_split(
    window_len=window_len,
    set_lens=(train_ratio, 1 - train_ratio),
    left_to_right=False
)

print(f"\nNumber of walk-forward windows: {len(splits)}")

# Store results
wf_results = []

# Walk-forward loop
for window_idx, (train_indices, val_indices) in enumerate(splits):
    print(f"\n{'='*60}")
    print(f"Window {window_idx + 1}/{len(splits)}")
    print(f"{'='*60}")

    # Get train/validation data
    train_close = close.iloc[train_indices]
    val_close = close.iloc[val_indices]

    print(f"Train: {train_close.index[0]} to {train_close.index[-1]}")
    print(f"Val: {val_close.index[0]} to {val_close.index[-1]}")

    # Optimize on training data
    fast_windows = np.arange(10, 30, 5)
    slow_windows = np.arange(50, 100, 10)

    # Calculate indicators for training
    train_fast_ma = vbt.MA.run(train_close, window=fast_windows)
    train_slow_ma = vbt.MA.run(train_close, window=slow_windows)
    train_entries = train_fast_ma.ma_crossed_above(train_slow_ma)
    train_exits = train_fast_ma.ma_crossed_below(train_slow_ma)

    # Backtest all parameter combinations on training data
    train_pf = vbt.Portfolio.from_signals(
        close=train_close,
        entries=train_entries,
        exits=train_exits,
        fees=0.001,
        cash_sharing=True,  # Share cash across symbols
        group_by=True,      # Treat as single portfolio
        freq='D'
    )

    # Find best parameters (by Sharpe ratio)
    train_sharpe = train_pf.sharpe_ratio()
    best_params = train_sharpe.idxmax()

    print(f"\nBest params: Fast={best_params[0]}, Slow={best_params[1]}")
    print(f"Train Sharpe: {train_sharpe.max():.2f}")

    # Test on validation data with best parameters
    val_fast_ma = vbt.MA.run(val_close, window=best_params[0])
    val_slow_ma = vbt.MA.run(val_close, window=best_params[1])
    val_entries = val_fast_ma.ma_crossed_above(val_slow_ma)
    val_exits = val_fast_ma.ma_crossed_below(val_slow_ma)

    val_pf = vbt.Portfolio.from_signals(
        close=val_close,
        entries=val_entries,
        exits=val_exits,
        fees=0.001,
        cash_sharing=True,
        group_by=True,
        freq='D'
    )

    # Calculate metrics
    val_sharpe = val_pf.sharpe_ratio()
    val_return = val_pf.total_return()
    val_dd = val_pf.max_drawdown()

    print(f"Val Sharpe: {val_sharpe:.2f}")
    print(f"Val Return: {val_return:.2%}")
    print(f"Val Max DD: {val_dd:.2%}")

    # Store results
    wf_results.append({
        'window': window_idx + 1,
        'train_start': train_close.index[0],
        'train_end': train_close.index[-1],
        'val_start': val_close.index[0],
        'val_end': val_close.index[-1],
        'best_fast': best_params[0],
        'best_slow': best_params[1],
        'train_sharpe': train_sharpe.max(),
        'val_sharpe': val_sharpe,
        'val_return': val_return,
        'val_max_dd': val_dd,
        'degradation': train_sharpe.max() - val_sharpe
    })

# Analyze walk-forward results
wf_df = pd.DataFrame(wf_results)

print("\n" + "=" * 60)
print("WALK-FORWARD ANALYSIS SUMMARY")
print("=" * 60)
print(wf_df.to_string())

print("\n" + "=" * 60)
print("AGGREGATE STATISTICS")
print("=" * 60)
print(f"Average train Sharpe: {wf_df['train_sharpe'].mean():.2f}")
print(f"Average val Sharpe: {wf_df['val_sharpe'].mean():.2f}")
print(f"Average degradation: {wf_df['degradation'].mean():.2f}")
print(f"Median degradation: {wf_df['degradation'].median():.2f}")
print(f"Std of degradation: {wf_df['degradation'].std():.2f}")

print(f"\nAverage val return: {wf_df['val_return'].mean():.2%}")
print(f"Average val max DD: {wf_df['val_max_dd'].mean():.2%}")

print(f"\nPositive val Sharpe windows: {(wf_df['val_sharpe'] > 0).sum()}/{len(wf_df)}")
print(f"Positive val return windows: {(wf_df['val_return'] > 0).sum()}/{len(wf_df)}")

# Visualize degradation
import plotly.graph_objects as go

fig = go.Figure()

fig.add_trace(go.Bar(
    x=wf_df['window'],
    y=wf_df['train_sharpe'],
    name='Train Sharpe',
    marker_color='lightblue'
))

fig.add_trace(go.Bar(
    x=wf_df['window'],
    y=wf_df['val_sharpe'],
    name='Validation Sharpe',
    marker_color='coral'
))

fig.update_layout(
    title='Walk-Forward Analysis: Train vs Validation Sharpe Ratio',
    xaxis_title='Window',
    yaxis_title='Sharpe Ratio',
    barmode='group',
    height=500
)

fig.show()

# Visualize degradation over time
fig2 = go.Figure()

fig2.add_trace(go.Scatter(
    x=wf_df['window'],
    y=wf_df['degradation'],
    mode='lines+markers',
    name='Sharpe Degradation',
    line=dict(color='red', width=2)
))

fig2.add_hline(y=0, line_dash="dash", line_color="gray")
fig2.add_hline(y=wf_df['degradation'].mean(), line_dash="dot", line_color="blue",
               annotation_text=f"Mean: {wf_df['degradation'].mean():.2f}")

fig2.update_layout(
    title='Walk-Forward Analysis: Sharpe Ratio Degradation',
    xaxis_title='Window',
    yaxis_title='Degradation (Train - Val)',
    height=400
)

fig2.show()
```

**Key Learnings:**
- Walk-forward analysis methodology
- Out-of-sample validation
- Multi-asset portfolio management
- Cash sharing across assets
- Strategy degradation analysis
- Robust parameter selection
- Overfitting detection

**Interpretation:**
- **Low degradation:** Robust strategy
- **High degradation:** Overfitting
- **Consistent positive validation:** Good generalization
- **Negative validation:** Poor strategy

---

## 5. Core Concepts

### 5.1 Vectorized vs Traditional Backtesting

**Traditional Backtesting (Event-Driven):**
```python
# Slow - processes bar by bar
for i in range(len(data)):
    if condition[i]:
        execute_trade()
    update_portfolio()
```

**Vectorized Backtesting:**
```python
# Fast - processes entire array at once
entries = (fast_ma > slow_ma) & (fast_ma.shift(1) <= slow_ma.shift(1))
pf = vbt.Portfolio.from_signals(close, entries, exits)
```

**Performance Comparison:**

| Dataset Size | Traditional | VectorBT | Speedup |
|--------------|-------------|----------|---------|
| 1,000 bars   | 2.5s        | 0.03s    | 83x     |
| 10,000 bars  | 25s         | 0.15s    | 167x    |
| 100,000 bars | 250s        | 1.2s     | 208x    |

**Benefits:**
- Test 1000s of strategies in seconds
- 80-100x faster than pandas
- Test parameter grids efficiently
- Memory efficient with broadcasting

### 5.2 Broadcasting Mechanics

**Concept:** Automatically expand arrays to compatible shapes

**Example 1: Single Price, Multiple Windows**
```python
close.shape  # (1000,)
windows = [10, 20, 50, 100, 200]

ma = vbt.MA.run(close, window=windows)
ma.ma.shape  # (1000, 5) - broadcasts to 5 columns
```

**Example 2: Grid Search**
```python
# Test all combinations
fast_windows = [5, 10, 15, 20]
slow_windows = [50, 100, 150, 200]

# Traditional approach: nested loops (16 iterations)
for fast_w in fast_windows:
    for slow_w in slow_windows:
        # 4×4 = 16 combinations

# Vectorized approach: single operation
fast_ma = vbt.MA.run(close, window=fast_windows)
slow_ma = vbt.MA.run(close, window=slow_windows)
# Automatic broadcasting creates 16 combinations
```

**Broadcasting Rules:**
- Single value broadcasts to any shape
- Arrays must have compatible dimensions
- VectorBT handles multi-dimensional broadcasting
- Efficient memory usage (no duplication)

### 5.3 Numba Acceleration

**Purpose:** JIT compile Python to machine code

**Usage:**
```python
from numba import njit
import numpy as np

@njit
def my_fast_function(arr):
    """Compiled to C speed"""
    result = np.empty_like(arr)
    for i in range(len(arr)):
        result[i] = arr[i] * 2
    return result
```

**Where Used in VectorBT:**
- Portfolio simulation loops
- Indicator calculations
- Rolling/groupby/resample operations
- Custom order functions
- All `nb` modules

**Performance:** Near C speed (80-100x vs pandas)

**Important Notes:**
- First call is slow (compilation)
- Subsequent calls are fast (cached)
- Supports NumPy but limited Python features
- No pandas operations inside @njit

### 5.4 Two Data Representations

#### Matrix Form (Dense)
- **Type:** pandas DataFrame / NumPy array
- **Use for:** Prices, indicators, signals, continuous data
- **Example:** Close prices over time

```python
close.shape  # (1000, 4) - 1000 bars, 4 symbols
# Every cell has a value (dense)
```

#### Record Form (Sparse)
- **Type:** Structured NumPy array
- **Use for:** Orders, trades, positions, events
- **Example:** Trade records with entry/exit
- **Classes:** Orders, Trades, Positions, Drawdowns, Logs

```python
pf.trades.records  # Structured array
# Only trade events stored (sparse)
```

**Why Both?**
- **Matrix:** Vectorized operations, easy visualization
- **Records:** Memory efficient for sparse events, fast queries

**Conversion:**
```python
# Records to DataFrame
trades_df = pf.trades.records_readable

# DataFrame to array
arr = df.values
```

### 5.5 ArrayWrapper

**Bridge between NumPy and pandas:**

```
pandas → NumPy → Compute → ArrayWrapper → pandas
```

**Workflow:**
1. Extract NumPy array from pandas
2. Perform fast NumPy/Numba operations
3. ArrayWrapper restores index/columns/freq
4. Return pandas object

**Benefits:**
- Speed of NumPy
- Convenience of pandas
- Preserves metadata
- Automatic alignment

**Example:**
```python
# Input: pandas DataFrame
close  # DatetimeIndex, symbol columns

# VectorBT extracts array
arr = close.values

# Numba computation
result_arr = fast_computation(arr)

# ArrayWrapper restores pandas
result_df = wrapper.wrap(result_arr)
# Same index/columns as input
```

### 5.6 Configuration System

**Hierarchical settings:**

```python
import vectorbt as vbt

# Access settings
vbt.settings

# Portfolio settings
vbt.settings['portfolio']

# Specific setting
vbt.settings['portfolio']['init_cash']
```

**None = Pull from Settings:**
```python
# These are equivalent
pf = vbt.Portfolio.from_signals(close, entries, exits, init_cash=10000)
pf = vbt.Portfolio.from_signals(close, entries, exits)  # Uses default from settings
```

**Modify Settings:**
```python
# Change defaults
vbt.settings['portfolio']['init_cash'] = 100000
vbt.settings['portfolio']['fees'] = 0.001
```

### 5.7 Call Sequence

**Controls order execution when cash is shared:**

```python
pf = vbt.Portfolio.from_signals(
    close,
    entries,
    exits,
    cash_sharing=True,
    call_seq='auto'  # or 'default', 'reversed', custom array
)
```

**Options:**
- **'default':** Process columns left to right
- **'reversed':** Process columns right to left
- **'auto':** Optimize based on signals
- **Custom array:** Specify exact order

**Why it matters:**
- With shared cash, order affects execution
- First assets get priority
- Can bias results
- Use 'auto' for fairness

---

## 6. Performance Optimization

### 6.1 Speed Optimization

#### 6.1.1 Choose the Right Method

```python
# Fastest
pf = vbt.Portfolio.from_orders(close, size, ...)

# Slower (more features)
pf = vbt.Portfolio.from_signals(close, entries, exits, ...)

# Slowest but most flexible
pf = vbt.Portfolio.from_order_func(close, order_func_nb, ...)
```

**Rule:** Use the simplest method that meets your needs.

#### 6.1.2 Use Numba for Custom Logic

```python
# Slow
def my_func(arr):
    return [x * 2 for x in arr]

# Fast
@njit
def my_func_nb(arr):
    result = np.empty_like(arr)
    for i in range(len(arr)):
        result[i] = arr[i] * 2
    return result
```

**Speedup:** 50-100x for loops

#### 6.1.3 Leverage Caching

```python
# Indicators cache results
ma = vbt.MA.run(close, window=20)  # Computed once
ma.ma  # Cached
ma.ma  # Retrieved from cache (instant)
```

**Tip:** Reuse indicator objects

#### 6.1.4 Batch Parameters

```python
# Slow: loop
for window in [10, 20, 30, 40, 50]:
    pf = vbt.Portfolio.from_signals(...)

# Fast: broadcast
pf = vbt.Portfolio.from_signals(..., window=[10, 20, 30, 40, 50])
```

**Speedup:** 10-50x depending on parameters

#### 6.1.5 Avoid Excessive Logging

```python
# Only for debugging
pf = vbt.Portfolio.from_order_func(..., log=True)  # Slow with many bars

# Production
pf = vbt.Portfolio.from_order_func(..., log=False)  # Fast
```

### 6.2 Memory Optimization

#### 6.2.1 Broadcasting is Efficient

```python
# Doesn't duplicate data - shares references
close.shape  # (1000,)
ma = vbt.MA.run(close, window=[10, 20, 30])  # Doesn't create 3 copies of close
```

#### 6.2.2 Use Records for Sparse Data

```python
# Memory efficient
orders = pf.orders  # Sparse records

# Memory intensive
orders_df = pf.orders.records_readable  # Full DataFrame
```

**Tip:** Only convert to DataFrame when needed

#### 6.2.3 Limit Parameter Grids

```python
# Memory heavy
windows = np.arange(1, 1000, 1)  # 1000 columns

# More reasonable
windows = np.arange(10, 200, 10)  # 19 columns
```

**Rule:** Start small, expand if needed

#### 6.2.4 Clear Intermediate Results

```python
# Large intermediate results
large_ma = vbt.MA.run(close, window=range(1, 1000))
pf = vbt.Portfolio.from_signals(...)

del large_ma  # Free memory
```

### 6.3 Common Bottlenecks

1. **Python loops** → Use vectorization/Numba
2. **Excessive logging** → Disable log unless debugging
3. **Huge parameter grids** → Reduce grid size, use hierarchical search
4. **Plotting 1000s of series** → Sample or aggregate first
5. **Non-Numba custom functions** → Compile with @njit
6. **Unnecessary conversions** → Keep data in efficient format
7. **Repeated calculations** → Cache and reuse

### 6.4 Performance Profiling

```python
import time

# Time your code
start = time.time()
pf = vbt.Portfolio.from_signals(...)
end = time.time()
print(f"Backtest took {end - start:.2f} seconds")

# Profile specific sections
with vbt.timeit("Indicator calculation"):
    ma = vbt.MA.run(close, window=[10, 20, 30])

with vbt.timeit("Backtesting"):
    pf = vbt.Portfolio.from_signals(...)
```

---

## 7. Best Practices & Common Pitfalls

### 7.1 Best Practices

#### 7.1.1 Always Set Frequency

```python
# GOOD
pf = vbt.Portfolio.from_signals(close, entries, exits, freq='D')

# BAD
pf = vbt.Portfolio.from_signals(close, entries, exits)
# Metrics will use wrong annualization!
```

**Why:** Frequency affects annualized metrics (Sharpe, returns, volatility)

#### 7.1.2 Include Realistic Costs

```python
# GOOD
pf = vbt.Portfolio.from_signals(
    close, entries, exits,
    fees=0.001,      # 0.1% commission
    slippage=0.0005  # 0.05% slippage
)

# BAD
pf = vbt.Portfolio.from_signals(close, entries, exits)
# Unrealistic results
```

**Typical costs:**
- **Stocks:** 0.1% - 0.5% fees
- **Crypto:** 0.1% - 0.3% fees
- **Slippage:** 0.01% - 0.1%

#### 7.1.3 Validate Data Quality

```python
# Check for issues
print(f"Missing values: {close.isna().sum()}")
print(f"Duplicates: {close.index.duplicated().sum()}")
print(f"Date range: {close.index[0]} to {close.index[-1]}")

# Handle missing values
close = close.fillna(method='ffill')  # Forward fill
# or
pf = vbt.Portfolio.from_signals(..., ffill_val_price=True)
```

#### 7.1.4 Use Walk-Forward Analysis

```python
# Don't just optimize on full dataset
# Use walk-forward or cross-validation

splits = close.vbt.rolling_split(window_len=252, set_lens=(0.7, 0.3))
for train, val in splits:
    # Optimize on train
    # Validate on val
```

**Why:** Prevents overfitting

#### 7.1.5 Compare to Benchmark

```python
# Always compare to buy-and-hold
bh = vbt.Portfolio.from_holding(close, freq='D')
print(f"Strategy: {pf.total_return():.2%}")
print(f"Buy & Hold: {bh.total_return():.2%}")
```

### 7.2 Common Pitfalls

#### 7.2.1 Missing Frequency

```python
# WRONG
pf = vbt.Portfolio.from_signals(close, entries, exits)
print(pf.sharpe_ratio())  # Wrong annualization!

# RIGHT
pf = vbt.Portfolio.from_signals(close, entries, exits, freq='D')
print(pf.sharpe_ratio())  # Correct annualization
```

#### 7.2.2 Active Drawdowns in Metrics

```python
# WRONG - includes active DD
dd = pf.drawdowns
avg_dd = dd.drawdown.mean()  # Skewed by active DD!

# RIGHT - filter recovered only
recovered_dd = dd.recovered
avg_dd = recovered_dd.drawdown.mean()
```

#### 7.2.3 Size Type Confusion

```python
# Amount = number of shares
pf = vbt.Portfolio.from_orders(close, size=10, size_type='Amount')
# Buys 10 shares

# TargetAmount = target number of shares to hold
pf = vbt.Portfolio.from_orders(close, size=10, size_type='TargetAmount')
# Adjusts position to 10 shares
```

**Size Types:**
- **Amount:** Fixed number of shares
- **Value:** Fixed dollar amount
- **Percent:** Percentage of portfolio
- **TargetAmount:** Target position size
- **TargetValue:** Target position value
- **TargetPercent:** Target allocation

#### 7.2.4 Lookahead Bias

```python
# WRONG - uses future data
ma = close.rolling(20).mean()
entries = close > ma  # Includes today's close in MA!

# RIGHT - shift MA or use proper calculation
ma = close.rolling(20).mean().shift(1)
entries = close > ma
```

**Critical:** Ensure signals don't use future data

#### 7.2.5 Forgetting Fees

```python
# Unrealistic
pf = vbt.Portfolio.from_signals(close, entries, exits)

# Realistic
pf = vbt.Portfolio.from_signals(
    close, entries, exits,
    fees=0.001,
    slippage=0.0001
)
```

**Impact:** Fees can turn profitable strategy into losing one

#### 7.2.6 Accumulate Flag

```python
# from_signals prevents duplicate entries by default
pf = vbt.Portfolio.from_signals(close, entries, exits)  # accumulate=False

# To allow pyramiding
pf = vbt.Portfolio.from_signals(close, entries, exits, accumulate=True)
```

#### 7.2.7 Broadcasting Shape Errors

```python
# WRONG - incompatible shapes
fast_ma = vbt.MA.run(close, window=[10, 20])  # Shape: (1000, 2)
slow_ma = vbt.MA.run(close, window=[50, 100, 150])  # Shape: (1000, 3)
entries = fast_ma.ma_crossed_above(slow_ma)  # Error! 2 vs 3 columns

# RIGHT - use same parameter counts or single values
fast_ma = vbt.MA.run(close, window=[10, 20])
slow_ma = vbt.MA.run(close, window=[50, 100])
# Now: 2×2=4 combinations
```

#### 7.2.8 Data Quality Issues

**Yahoo Finance Warnings:**
1. **Unstable:** Data can change or disappear
2. **Gaps:** Missing trading days
3. **Noise:** Incorrect prices
4. **Demo only:** Not for production

**Best practice:**
```python
# Use professional data providers for production
# - Alpaca, Interactive Brokers, Polygon.io, etc.
```

#### 7.2.9 Overfitting

**Signs of overfitting:**
- Too many parameters
- Excessive optimization
- Perfect training results
- Poor validation results
- High train/val degradation

**Solutions:**
- Simpler strategies
- Walk-forward analysis
- Out-of-sample testing
- Regularization (limit parameters)

#### 7.2.10 Not Testing Edge Cases

```python
# Test your strategy on:
# - Bull markets
# - Bear markets
# - Sideways markets
# - High volatility
# - Low volatility
# - Different symbols
# - Different time periods
```

### 7.3 Debugging Tips

#### 7.3.1 Enable Logging

```python
pf = vbt.Portfolio.from_order_func(
    close,
    order_func_nb=my_func,
    log=True  # Enable detailed logs
)

# Inspect logs
print(pf.logs.records_readable)
```

#### 7.3.2 Check Intermediate Results

```python
# Verify signals
print(f"Entries: {entries.sum().sum()}")
print(f"Exits: {exits.sum().sum()}")

# Verify indicators
print(f"MA range: {ma.ma.min():.2f} - {ma.ma.max():.2f}")

# Check for NaN
print(f"NaN in close: {close.isna().sum()}")
```

#### 7.3.3 Start Simple

```python
# Start with simplest method
pf = vbt.Portfolio.from_holding(close)

# Add complexity incrementally
pf = vbt.Portfolio.from_orders(close, size)
pf = vbt.Portfolio.from_signals(close, entries, exits)
pf = vbt.Portfolio.from_order_func(close, order_func_nb)
```

#### 7.3.4 Visualize Everything

```python
# Plot price and indicators
close.vbt.plot().show()
ma.plot().show()

# Plot signals
entries.vbt.signals.plot_as_entries(close).show()

# Plot portfolio
pf.plot().show()
```

---

## 8. Resources

### 8.1 Official Documentation

- **Free version:** https://vectorbt.dev/
- **PRO version:** https://vectorbt.pro/
- **API Reference:** https://vectorbt.dev/api/
- **GitHub:** https://github.com/polakowo/vectorbt

### 8.2 Community

- **Discussions:** GitHub Discussions
- **Chat:** https://gitter.im/vectorbt/community
- **Issues:** GitHub Issues
- **Stack Overflow:** Tag: vectorbt

### 8.3 Learning Resources

- Official Jupyter notebooks (examples/ directory in repo)
- Greyhound Analytics tutorials
- AlgoTrading101 guides
- Medium articles
- YouTube tutorials

### 8.4 Quick Reference Templates

#### Basic Backtest Template

```python
import vectorbt as vbt

# 1. Data
data = vbt.YFData.download('SYMBOL', start='YYYY-MM-DD')
close = data.get('Close')

# 2. Signals
entries = ...  # Boolean array
exits = ...    # Boolean array

# 3. Backtest
pf = vbt.Portfolio.from_signals(close, entries, exits, fees=0.001, freq='D')

# 4. Analyze
print(pf.stats())
pf.plot().show()
```

#### Parameter Optimization Template

```python
import numpy as np

# Parameters
param_range = np.arange(start, stop, step)

# Run with broadcasting
indicator = vbt.INDICATOR.run(close, param=param_range)

# Backtest all
pf = vbt.Portfolio.from_signals(close, entries, exits, freq='D')

# Find best
best = pf.sharpe_ratio().idxmax()
print(f"Best: {best}")
```

#### Custom Order Function Template

```python
from numba import njit
from vectorbt.portfolio.enums import Order, NoOrder

@njit
def my_order_func_nb(c, *args):
    # Your logic
    if condition:
        return Order(size=..., price=...)
    return NoOrder

pf = vbt.Portfolio.from_order_func(close, order_func_nb=my_order_func_nb, ...)
```

### 8.5 Library Statistics

- **GitHub Stars:** 6,300+
- **Status:** Mature, stable (maintenance mode for free version)
- **Latest Version:** 0.28.2
- **Python Versions:** 3.6 - 3.12
- **License:** Apache 2.0 + Commons Clause
- **First Release:** 2020
- **Last Update:** December 2025

---

## Appendix: Complete Function Reference

### Portfolio Creation Methods

| Method | Use Case | Complexity | Performance |
|--------|----------|------------|-------------|
| `from_signals()` | Signal-based strategies | Low | Fast |
| `from_orders()` | Predefined orders | Low | Fastest |
| `from_order_func()` | Custom logic | High | Medium |
| `from_holding()` | Buy and hold | Low | Fastest |

### Key Performance Metrics

| Metric | Method | Description |
|--------|--------|-------------|
| Total Return | `total_return()` | Cumulative return |
| CAGR | `annualized_return()` | Annualized return |
| Sharpe Ratio | `sharpe_ratio()` | Risk-adjusted return |
| Sortino Ratio | `sortino_ratio()` | Downside risk-adjusted |
| Max Drawdown | `max_drawdown()` | Maximum peak-to-trough |
| Win Rate | `win_rate()` | Percentage winning trades |
| Profit Factor | `profit_factor()` | Gross profit / gross loss |

### Essential Imports

```python
import vectorbt as vbt
import numpy as np
import pandas as pd
from numba import njit
from vectorbt.portfolio.enums import Order, NoOrder
```

---

**End of VectorBT User Reference Guide**

For the most up-to-date information, always refer to the official documentation at https://vectorbt.dev/
