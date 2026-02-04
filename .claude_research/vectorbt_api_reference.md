# VectorBT Complete API Reference & User Guide

**Research Date:** 2025-12-17
**Library Version:** 0.28.2 (latest stable)
**Python Support:** 3.6 - 3.12

---

## Table of Contents

1. [Installation & Setup](#installation--setup)
2. [Module Inventory](#module-inventory)
3. [Portfolio Class - Complete API](#portfolio-class---complete-api)
4. [Record Classes](#record-classes)
5. [Indicators](#indicators)
6. [Signals](#signals)
7. [Returns & Metrics](#returns--metrics)
8. [Data Management](#data-management)
9. [Core Concepts](#core-concepts)
10. [Common Workflows](#common-workflows)
11. [Performance Tips](#performance-tips)
12. [Limitations & Gotchas](#limitations--gotchas)

---

## Installation & Setup

### Basic Installation
```bash
pip install -U vectorbt
```

### With All Optional Dependencies
```bash
pip install -U "vectorbt[full]"
```

### Without TA-Lib (if C library unavailable)
```bash
pip install -U "vectorbt[full-no-talib]"
```

### Core Dependencies
- **numpy** - Array operations and numerical computing
- **pandas** - Time series and DataFrame handling
- **numba** - JIT compilation for 80-100x performance boost
- **plotly** - Interactive visualizations

### Optional Dependencies
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

**Note:** This guide covers the free version unless otherwise specified.

---

## Module Inventory

### Complete Module Structure

```
vectorbt/
├── base/                  # Foundation layer
│   ├── accessors          # Base accessor functionality
│   ├── array_wrapper      # NumPy ↔ pandas conversion
│   ├── column_grouper     # Column grouping
│   ├── combine_fns        # Array combination functions
│   ├── index_fns          # Index manipulation
│   ├── indexing           # Indexing operations
│   └── reshape_fns        # Broadcasting & reshaping
│
├── data/                  # Data management
│   ├── base               # Base Data class
│   ├── custom             # YFData, BinanceData, etc.
│   └── updater            # Update functionality
│
├── generic/               # Generic time series ops
│   ├── accessors          # GenericAccessor (rolling, groupby, etc.)
│   ├── decorators         # Decorator patterns
│   ├── drawdowns          # Drawdown analysis
│   ├── enums              # Enumerations
│   ├── nb                 # Numba functions
│   ├── plots_builder      # Plot builders
│   ├── plotting           # Plotting functions
│   ├── ranges             # Range records
│   ├── splitters          # Data splitting
│   └── stats_builder      # Stats framework
│
├── indicators/            # Technical indicators
│   ├── basic              # Built-in indicators (MA, RSI, etc.)
│   ├── configs            # Indicator configs
│   ├── factory            # IndicatorFactory
│   └── nb                 # Numba indicator functions
│
├── labels/                # ML label generation
│   ├── enums
│   ├── generators
│   └── nb
│
├── messaging/             # Notifications
│   └── telegram           # Telegram integration
│
├── ohlcv_accessors/       # OHLCV data accessor
│
├── portfolio/             # Core backtesting
│   ├── base               # Portfolio class
│   ├── decorators
│   ├── enums              # DirectionT, SizeTypeT, etc.
│   ├── logs               # Simulation logs
│   ├── nb                 # Numba simulation
│   ├── orders             # Order records
│   └── trades             # Trade records
│
├── records/               # Sparse event data
│   ├── base               # Base record classes
│   ├── col_mapper
│   ├── decorators
│   ├── mapped_array
│   └── nb
│
├── returns/               # Return analysis
│   ├── accessors          # ReturnsAccessor
│   ├── metrics            # Financial metrics
│   ├── nb                 # Numba metrics
│   └── qs_adapter         # QuantStats adapter
│
├── signals/               # Signal generation
│   ├── accessors
│   ├── enums
│   ├── factory
│   ├── generators         # OHLCSTX, RAND, etc.
│   └── nb
│
├── utils/                 # Utilities (20+ submodules)
│   ├── array_, attr_, checks, colors, config
│   ├── datetime_, decorators, docs, enum_
│   ├── figure, image_, mapping, math_
│   ├── module_, params, random_, requests_
│   ├── schedule_, tags
│   └── ... (see detailed list below)
│
├── root_accessors/        # Root pandas accessors
└── _settings/             # Global configuration
```

---

## Portfolio Class - Complete API

**Import:** `from vectorbt.portfolio import Portfolio` or `vbt.Portfolio`

### Simulation Methods

#### 1. `Portfolio.from_signals()`
**Purpose:** Create portfolio from entry/exit signals with automatic signal management

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

---

#### 2. `Portfolio.from_orders()`
**Purpose:** Create portfolio from predefined orders (fastest and most straightforward)

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
# Buy 10 shares every day close is positive
size = np.where(close.pct_change() > 0, 10, 0)

pf = vbt.Portfolio.from_orders(
    close=close,
    size=size,
    price=close,
    fees=0.001,
    freq='D'
)
```

---

#### 3. `Portfolio.from_order_func()`
**Purpose:** Maximum flexibility using custom order generation functions

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
@njit
def order_func_nb(c, *args):
    """
    c: context object with:
        - c.i: current bar index
        - c.col: current column
        - c.cash_now: available cash
        - c.position_now: current position
        - ... (many more context variables)

    Returns: Order namedtuple or NoOrder
    """
    # Your logic here
    return Order(size=10, price=c.close[c.i, c.col], ...)
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
from vectorbt.portfolio.enums import Order

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
```

---

#### 4. `Portfolio.from_holding()`
**Purpose:** Simple buy-and-hold strategy

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

---

### Portfolio Properties

**Core Data:**
```python
pf.cash()           # Cash balance over time
pf.assets()         # Asset holdings over time
pf.value()          # Total portfolio value
pf.returns()        # Period returns
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
```

---

### Portfolio Metrics

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

---

### Portfolio Plotting

```python
pf.plot_value()             # Value curve
pf.plot_returns()           # Return distribution
pf.plot_drawdowns()         # Drawdown periods
pf.plot_underwater()        # Underwater plot
pf.plot_positions()         # Position visualization
pf.plot_trades()            # Trade markers
pf.plot_cash_flow()         # Cash flows
pf.plot_gross_exposure()    # Exposure over time
pf.plot()                   # General plot
```

**Example:**
```python
# Create subplot dashboard
fig = pf.plot()
fig.show()

# Individual plots
pf.plot_value().show()
pf.plot_drawdowns(top_n=5).show()  # Top 5 drawdowns
```

---

### Stats Method

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

---

## Record Classes

### Orders Class

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

---

### Trades Class

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

---

### EntryTrades, ExitTrades, Positions

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

---

### Drawdowns Class

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

**Plotting:**
```python
dd.plot()               # Visualize drawdowns
dd.stats()              # DD statistics
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

---

## Indicators

### Built-in Indicators (30+)

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

### Using Built-in Indicators

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

---

### External Library Integration

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

---

### Custom Indicators

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

---

## Signals

### Signal Generators

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

### Signal Operations

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

---

## Returns & Metrics

### ReturnsAccessor

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

### Return Metrics

```python
# Basic returns
returns.vbt.returns.total_return()          # Cumulative
returns.vbt.returns.annualized_return()     # CAGR
returns.vbt.returns.annual                  # Alias for annualized
returns.vbt.returns.cumulative_returns()    # Growth curve
returns.vbt.returns.daily_returns()         # Daily bucketed
returns.vbt.returns.annual_returns()        # Annual bucketed
```

### Risk Metrics

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

### Risk-Adjusted Metrics

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

### Benchmark Comparison

```python
# Requires benchmark returns
returns.vbt.returns.beta(benchmark_returns)
returns.vbt.returns.alpha(benchmark_returns)
returns.vbt.returns.capture(benchmark_returns)
returns.vbt.returns.up_capture(benchmark_returns)
returns.vbt.returns.down_capture(benchmark_returns)
returns.vbt.returns.tail_ratio()
```

### Rolling Metrics

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

## Data Management

### Data Class

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

### YFData - Yahoo Finance

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

### Other Data Sources

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

---

## Core Concepts

### 1. Vectorized Backtesting

**Traditional Backtesting:**
```python
# Slow - processes bar by bar
for i in range(len(data)):
    if condition[i]:
        execute_trade()
```

**Vectorized Backtesting:**
```python
# Fast - processes entire array at once
entries = (fast_ma > slow_ma) & (fast_ma.shift(1) <= slow_ma.shift(1))
pf = vbt.Portfolio.from_signals(close, entries, exits)
```

**Benefits:**
- Test 1000s of strategies in seconds
- 80-100x faster than pandas
- Test parameter grids efficiently
- Memory efficient with broadcasting

---

### 2. Broadcasting

**Concept:** Automatically expand arrays to compatible shapes

**Example:**
```python
# Single price, multiple windows
close.shape  # (1000,)
windows = [10, 20, 50, 100, 200]

ma = vbt.MA.run(close, window=windows)
ma.ma.shape  # (1000, 5) - broadcasts to 5 columns
```

**Grid Search:**
```python
# Test all combinations
fast_windows = [5, 10, 15, 20]
slow_windows = [50, 100, 150, 200]

for fast_w in fast_windows:
    for slow_w in slow_windows:
        # 4×4 = 16 combinations

# Vectorized equivalent (much faster!)
fast_ma = vbt.MA.run(close, window=fast_windows)
slow_ma = vbt.MA.run(close, window=slow_windows)
# Automatic broadcasting creates 16 combinations
```

---

### 3. Numba Acceleration

**Purpose:** JIT compile Python to machine code

**Usage:**
```python
from numba import njit

@njit
def my_fast_function(arr):
    """Compiled to C speed"""
    result = np.empty_like(arr)
    for i in range(len(arr)):
        result[i] = arr[i] * 2
    return result
```

**Where Used:**
- Portfolio simulation loops
- Indicator calculations
- Rolling/groupby/resample operations
- Custom order functions
- All `nb` modules

**Performance:** Near C speed (80-100x vs pandas)

---

### 4. Two Data Representations

**Matrix Form (Dense):**
- Type: pandas DataFrame / NumPy array
- Use for: Prices, indicators, signals, continuous data
- Example: Close prices over time

**Record Form (Sparse):**
- Type: Structured NumPy array
- Use for: Orders, trades, positions, events
- Example: Trade records with entry/exit
- Classes: Orders, Trades, Positions, Drawdowns, Logs

**Why Both?**
- Matrix: Vectorized operations, easy visualization
- Records: Memory efficient for sparse events, fast queries

---

### 5. ArrayWrapper

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

---

### 6. Configuration System

**Hierarchical settings:**

```python
# Access settings
import vectorbt as vbt

# Global settings
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
# Change default
vbt.settings['portfolio']['init_cash'] = 100000
vbt.settings['portfolio']['fees'] = 0.001
```

---

## Common Workflows

### 1. Basic Backtest

```python
import vectorbt as vbt
import pandas as pd

# 1. Download data
data = vbt.YFData.download('AAPL', start='2020-01-01', end='2023-01-01')
close = data.get('Close')

# 2. Generate signals
fast_ma = vbt.MA.run(close, 10)
slow_ma = vbt.MA.run(close, 50)
entries = fast_ma.ma_crossed_above(slow_ma)
exits = fast_ma.ma_crossed_below(slow_ma)

# 3. Backtest
pf = vbt.Portfolio.from_signals(
    close=close,
    entries=entries,
    exits=exits,
    fees=0.001,
    freq='D'
)

# 4. Analyze
print(pf.stats())
print(f"Total Return: {pf.total_return():.2%}")
print(f"Sharpe Ratio: {pf.sharpe_ratio():.2f}")
print(f"Max Drawdown: {pf.max_drawdown():.2%}")

# 5. Visualize
pf.plot().show()
```

---

### 2. Parameter Optimization

```python
import numpy as np

# Define parameter ranges
fast_windows = np.arange(5, 50, 5)   # [5, 10, 15, ..., 45]
slow_windows = np.arange(50, 200, 10)  # [50, 60, 70, ..., 190]

# Run indicators with all parameters
fast_ma = vbt.MA.run(close, window=fast_windows)
slow_ma = vbt.MA.run(close, window=slow_windows)

# Generate signals (broadcasts to all combinations)
entries = fast_ma.ma_crossed_above(slow_ma)
exits = fast_ma.ma_crossed_below(slow_ma)

# Backtest all combinations
pf = vbt.Portfolio.from_signals(close, entries, exits, fees=0.001, freq='D')

# Find best parameters
sharpe_ratios = pf.sharpe_ratio()
best_combo = sharpe_ratios.idxmax()
best_sharpe = sharpe_ratios.max()

print(f"Best combination: {best_combo}")
print(f"Best Sharpe: {best_sharpe:.2f}")

# Analyze best strategy
pf[best_combo].stats()
pf[best_combo].plot().show()
```

---

### 3. Custom Indicator Creation

```python
from vectorbt import IndicatorFactory

# Define calculation
def rsi_ma_strategy(close, rsi_window, ma_window, rsi_threshold):
    """RSI + MA combined indicator"""
    # Calculate RSI
    rsi = vbt.RSI.run(close, rsi_window).rsi

    # Calculate MA
    ma = vbt.MA.run(close, ma_window).ma

    # Generate signals
    rsi_signal = rsi < rsi_threshold
    ma_signal = close > ma

    # Combined
    combined = rsi_signal & ma_signal

    return combined

# Create indicator factory
RSI_MA = IndicatorFactory(
    class_name='RSI_MA_Strategy',
    short_name='rsi_ma',
    input_names=['close'],
    param_names=['rsi_window', 'ma_window', 'rsi_threshold'],
    output_names=['signal']
).from_apply_func(rsi_ma_strategy)

# Use it
result = RSI_MA.run(
    close,
    rsi_window=[10, 14, 20],
    ma_window=[50, 100, 200],
    rsi_threshold=[25, 30, 35]
)

# Backtest
pf = vbt.Portfolio.from_signals(
    close,
    entries=result.signal,
    exits=~result.signal,
    freq='D'
)

# Optimize
best = pf.sharpe_ratio().idxmax()
print(f"Best params: {best}")
```

---

### 4. Complex Strategy with from_order_func

```python
from numba import njit
from vectorbt.portfolio.enums import Order, NoOrder

# Define strategy logic
@njit
def momentum_strategy_nb(c, rsi, bb_upper, bb_lower):
    """
    Buy on RSI oversold + price at BB lower
    Sell on RSI overbought + price at BB upper
    Position sizing: risk 2% per trade
    """
    current_rsi = rsi[c.i, c.col]
    current_price = c.close[c.i, c.col]
    bb_up = bb_upper[c.i, c.col]
    bb_low = bb_lower[c.i, c.col]

    # Entry: RSI < 30 and price touching lower BB
    if current_rsi < 30 and current_price <= bb_low and c.position_now == 0:
        # Risk 2% of capital
        stop_loss = current_price * 0.98
        risk_per_share = current_price - stop_loss
        position_value = c.cash_now * 0.02 / risk_per_share
        size = position_value / current_price

        return Order(
            size=size,
            price=current_price,
            fees=0.001,
            slippage=0.0001
        )

    # Exit: RSI > 70 or price touching upper BB
    elif (current_rsi > 70 or current_price >= bb_up) and c.position_now > 0:
        return Order(
            size=-c.position_now,
            price=current_price,
            fees=0.001
        )

    return NoOrder

# Prepare indicators
rsi = vbt.RSI.run(close, 14).rsi
bb = vbt.BBANDS.run(close, window=20, alpha=2)

# Run simulation
pf = vbt.Portfolio.from_order_func(
    close=close,
    order_func_nb=momentum_strategy_nb,
    rsi=rsi.values,
    bb_upper=bb.upper.values,
    bb_lower=bb.lower.values,
    freq='D',
    log=True  # Enable logging for debugging
)

# Analyze
print(pf.stats())
pf.trades.stats()
pf.plot().show()
```

---

### 5. Walk-Forward Analysis

```python
# Split data into rolling windows
window_len = 252  # 1 year
train_len = 0.7   # 70% train
val_len = 0.3     # 30% validation

splits = close.vbt.rolling_split(
    window_len=window_len,
    set_lens=(train_len, val_len),
    left_to_right=False
)

results = []

for i, (train, val) in enumerate(splits):
    # Optimize on training data
    fast_windows = np.arange(5, 30, 5)
    slow_windows = np.arange(30, 100, 10)

    train_close = close.iloc[train]
    fast_ma = vbt.MA.run(train_close, window=fast_windows)
    slow_ma = vbt.MA.run(train_close, window=slow_windows)
    entries = fast_ma.ma_crossed_above(slow_ma)
    exits = fast_ma.ma_crossed_below(slow_ma)

    train_pf = vbt.Portfolio.from_signals(
        train_close, entries, exits, freq='D'
    )

    # Find best parameters
    best_params = train_pf.sharpe_ratio().idxmax()

    # Test on validation data
    val_close = close.iloc[val]
    val_fast_ma = vbt.MA.run(val_close, window=best_params[0])
    val_slow_ma = vbt.MA.run(val_close, window=best_params[1])
    val_entries = val_fast_ma.ma_crossed_above(val_slow_ma)
    val_exits = val_fast_ma.ma_crossed_below(val_slow_ma)

    val_pf = vbt.Portfolio.from_signals(
        val_close, val_entries, val_exits, freq='D'
    )

    results.append({
        'window': i,
        'best_params': best_params,
        'train_sharpe': train_pf[best_params].sharpe_ratio(),
        'val_sharpe': val_pf.sharpe_ratio(),
        'degradation': train_pf[best_params].sharpe_ratio() - val_pf.sharpe_ratio()
    })

# Analyze walk-forward results
import pandas as pd
wf_results = pd.DataFrame(results)
print(wf_results)
print(f"\nAvg degradation: {wf_results['degradation'].mean():.2f}")
```

---

### 6. Multi-Asset Portfolio with Rebalancing

```python
# Download multiple assets
symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']
data = vbt.YFData.download(symbols, start='2020-01-01')
close = data.get('Close')

# Define rebalancing strategy
@njit
def equal_weight_rebalance_nb(c, rebal_freq):
    """
    Equal weight portfolio, rebalance every N days
    """
    # Only rebalance on schedule
    if c.i % rebal_freq != 0:
        return NoOrder

    # Target: 25% in each asset (4 assets)
    target_value = c.value_now / c.group_len
    current_value = c.position_now * c.close[c.i, c.col]

    # Calculate required trade
    diff = target_value - current_value
    size = diff / c.close[c.i, c.col]

    return Order(
        size=size,
        price=c.close[c.i, c.col],
        fees=0.001
    )

# Run portfolio simulation
pf = vbt.Portfolio.from_order_func(
    close=close,
    order_func_nb=equal_weight_rebalance_nb,
    rebal_freq=21,  # Rebalance monthly (21 trading days)
    cash_sharing=True,  # Share cash across all assets
    group_by=True,      # Treat as single portfolio
    freq='D'
)

# Analyze portfolio
print(pf.stats())
print("\nPer-asset stats:")
for symbol in symbols:
    print(f"\n{symbol}:")
    print(pf[symbol].stats())

# Plot
pf.plot_value().show()
```

---

## Performance Tips

### Speed Optimization

**1. Use from_orders When Possible**
```python
# Fastest
pf = vbt.Portfolio.from_orders(close, size, ...)

# Slower (more features)
pf = vbt.Portfolio.from_signals(close, entries, exits, ...)

# Slowest but most flexible
pf = vbt.Portfolio.from_order_func(close, order_func_nb, ...)
```

**2. Numba for Custom Logic**
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

**3. Leverage Caching**
```python
# Indicators cache results
ma = vbt.MA.run(close, window=20)  # Computed once
ma.ma  # Cached
ma.ma  # Retrieved from cache
```

**4. Batch Parameters**
```python
# Slow: loop
for window in [10, 20, 30, 40, 50]:
    pf = vbt.Portfolio.from_signals(...)

# Fast: broadcast
pf = vbt.Portfolio.from_signals(..., window=[10, 20, 30, 40, 50])
```

**5. Avoid Excessive Logging**
```python
# Only for debugging
pf = vbt.Portfolio.from_order_func(..., log=True)  # Slow with many bars

# Production
pf = vbt.Portfolio.from_order_func(..., log=False)  # Fast
```

---

### Memory Optimization

**1. Broadcasting is Efficient**
```python
# Doesn't duplicate data - shares references
close.shape  # (1000,)
ma = vbt.MA.run(close, window=[10, 20, 30])  # Doesn't create 3 copies of close
```

**2. Use Records for Sparse Data**
```python
# Memory efficient
orders = pf.orders  # Sparse records

# Memory intensive
orders_df = pf.orders.records_readable  # Full DataFrame
```

**3. Limit Parameter Grids**
```python
# Memory heavy
windows = np.arange(1, 1000, 1)  # 1000 columns

# More reasonable
windows = np.arange(10, 200, 10)  # 19 columns
```

**4. Clear Intermediate Results**
```python
# Large intermediate results
large_ma = vbt.MA.run(close, window=range(1, 1000))
pf = vbt.Portfolio.from_signals(...)

del large_ma  # Free memory
```

---

### Common Bottlenecks

1. **Python loops** → Use vectorization/Numba
2. **Excessive logging** → Disable log unless debugging
3. **Huge parameter grids** → Reduce grid size, use hierarchical search
4. **Plotting 1000s of series** → Sample or aggregate first
5. **Non-Numba custom functions** → Compile with @njit

---

## Limitations & Gotchas

### Known Limitations

1. **No portfolio optimization** (free version) - Available in PRO
2. **Limited short selling controls** - Improved in PRO
3. **No built-in regime detection** - Must implement custom
4. **Plotly no multi-index** - Flatten before plotting
5. **Yahoo Finance quality** - Use for demo only
6. **TA-Lib installation** - Requires C library (complex on Windows)
7. **Maintenance mode** - Free version gets bug fixes only, no new features

---

### Common Pitfalls

**1. Missing Frequency**
```python
# WRONG - no freq
pf = vbt.Portfolio.from_signals(close, entries, exits)
print(pf.sharpe_ratio())  # Wrong annualization!

# RIGHT - set freq
pf = vbt.Portfolio.from_signals(close, entries, exits, freq='D')
```

**2. Active Drawdowns in Metrics**
```python
# WRONG - includes active DD
dd = pf.drawdowns
avg_dd = dd.drawdown.mean()  # Skewed!

# RIGHT - filter recovered only
recovered_dd = dd.recovered
avg_dd = recovered_dd.drawdown.mean()
```

**3. Size Type Confusion**
```python
# Amount = number of shares
pf = vbt.Portfolio.from_orders(close, size=10, size_type='Amount')

# TargetAmount = target number of shares to hold
pf = vbt.Portfolio.from_orders(close, size=10, size_type='TargetAmount')
```

**4. Lookahead Bias**
```python
# WRONG - uses future data
ma = close.rolling(20).mean()
entries = close > ma  # Includes today's close in MA!

# RIGHT - shift MA or use proper calculation
ma = close.rolling(20).mean().shift(1)
entries = close > ma
```

**5. Forgetting Fees**
```python
# Unrealistic
pf = vbt.Portfolio.from_signals(close, entries, exits)

# Realistic
pf = vbt.Portfolio.from_signals(close, entries, exits, fees=0.001, slippage=0.0001)
```

**6. Accumulate Flag**
```python
# from_signals prevents duplicate entries by default
pf = vbt.Portfolio.from_signals(close, entries, exits)  # accumulate=False

# To allow pyramiding
pf = vbt.Portfolio.from_signals(close, entries, exits, accumulate=True)
```

**7. Broadcasting Shape Errors**
```python
# WRONG - incompatible shapes
fast_ma = vbt.MA.run(close, window=[10, 20])  # Shape: (1000, 2)
slow_ma = vbt.MA.run(close, window=[50, 100, 150])  # Shape: (1000, 3)
entries = fast_ma.ma_crossed_above(slow_ma)  # Error! 2 vs 3 columns

# RIGHT - use same parameter counts or single values
fast_ma = vbt.MA.run(close, window=[10, 20])
slow_ma = vbt.MA.run(close, window=[50, 100])
```

---

### Data Quality Warnings

1. **Yahoo Finance:** Unstable, gaps, noise - demo only
2. **Always validate:** Check for NaN, duplicates, gaps
3. **Missing values:** Use `ffill_val_price=True`
4. **Timezone handling:** Stocks (+0500) vs Crypto (UTC)
5. **Survivorship bias:** Historical data may exclude delisted stocks

---

## Resources & Community

### Official Documentation
- **Free version:** https://vectorbt.dev/
- **PRO version:** https://vectorbt.pro/
- **API Reference:** https://vectorbt.dev/api/
- **GitHub:** https://github.com/polakowo/vectorbt

### Community
- **Discussions:** GitHub Discussions
- **Chat:** https://gitter.im/vectorbt/community
- **Issues:** GitHub Issues

### Learning Resources
- Official Jupyter notebooks (examples/ directory)
- Greyhound Analytics tutorials
- AlgoTrading101 guides
- Medium articles
- Stack Overflow

### Statistics
- **Stars:** 6,300+
- **Status:** Mature, stable (maintenance mode)
- **Latest Version:** 0.28.2
- **Last Update:** December 2025

---

## Quick Reference

### Essential Imports
```python
import vectorbt as vbt
import numpy as np
import pandas as pd
from numba import njit
```

### Basic Backtest Template
```python
# Data
data = vbt.YFData.download('SYMBOL', start='YYYY-MM-DD')
close = data.get('Close')

# Signals
entries = ...  # Boolean array
exits = ...    # Boolean array

# Backtest
pf = vbt.Portfolio.from_signals(close, entries, exits, fees=0.001, freq='D')

# Analyze
print(pf.stats())
pf.plot().show()
```

### Parameter Optimization Template
```python
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

### Custom Order Function Template
```python
@njit
def my_order_func_nb(c, *args):
    # Your logic
    if condition:
        return Order(size=..., price=...)
    return NoOrder

pf = vbt.Portfolio.from_order_func(close, order_func_nb=my_order_func_nb, ...)
```

---

**End of VectorBT Complete API Reference**

For the most up-to-date information, always refer to the official documentation at https://vectorbt.dev/
