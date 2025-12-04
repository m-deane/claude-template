# Tidy-Signal: Research Summary & Viability Assessment

**Research Date:** December 4, 2025
**Researcher:** Technical Research Agent
**Objective:** Assess viability and prior art for a Python library applying R tidyverse/tidymodels philosophy to signal detection in commodities markets

---

## Executive Summary

**tidy-signal** represents a significant gap in the Python quantitative finance ecosystem. While excellent tools exist for general backtesting (zipline, vectorbt, backtrader) and statistical modeling (statsmodels, arch), no library combines:

1. **Tidyverse-inspired grammar** for signal detection workflows
2. **Native vintage/point-in-time data support** to prevent lookahead bias
3. **Commodity-specific patterns** (seasonality, spreads, term structure)
4. **Standardized outputs** across signal types (broom-style three-DataFrame pattern)
5. **Integrated validation workflows** (walk-forward, IC analysis, structural breaks)

The research identified strong prior art to learn from, clear design patterns to adopt, and a well-defined niche that tidy-signal can fill.

---

## 1. R Tidyverse/Tidymodels Patterns

### 1.1 Grammar of Verbs Philosophy

The tidyverse revolutionized R data science through consistent verb-based APIs:

**Core Principles:**
- **Table-in, table-out consistency** - Every function takes a data frame, returns a data frame
- **Pipe operator (`%>%`)** - Enables left-to-right, top-to-bottom reading: `x %>% f(y)` becomes `f(x, y)`
- **Five core verbs** - `mutate()`, `filter()`, `select()`, `arrange()`, `summarise()`
- **Data masking** - Use variables without `df$` prefix
- **No side effects** - Functional approach, always save results

> "The magic of dplyr is that with just a handful of commands (the verbs of dplyr), you can do nearly anything you'd want to do with your data."

**Implication for tidy-signal:** Adopt verb-based API like `detect_cointegration()`, `filter_signals()`, `mutate_signals()`, `validate_signals()`, `summarize_performance()`

### 1.2 Tidymodels Extension Pattern

**Parsnip (Model Interface):**
- **Specification → Engine → Mode → Fit → Predict** workflow
- Example: `rand_forest(mtry=10) %>% set_engine('ranger') %>% set_mode('regression') %>% fit(data)`
- **Modular design** - parsnip only handles interface, recipes handle preprocessing, workflows bundle them
- **Multiple engines per model type** - sklearn, statsmodels, prophet, etc.

**Recipes (Preprocessing):**
- **step_* functions** build preprocessing pipeline
- Separated from models because different models need different preprocessing
- Example: `recipe(y ~ .) %>% step_normalize(all_predictors()) %>% step_pca()`

**Workflows (Composition):**
- Bundle preprocessing + model + postprocessing
- `workflow() %>% add_recipe() %>% add_model()`

**Broom (Output Standardization):**
- **Three verbs for model outputs:**
  - `tidy()` - per-term statistics (coefficients, p-values)
  - `augment()` - per-observation statistics (predictions, residuals)
  - `glance()` - per-model statistics (R², AIC)
- Always returns tibbles, no rownames, consistent column names
- Supports 100+ model types

**Implication for tidy-signal:** Adopt three-DataFrame output pattern (`signal_outputs`, `signal_parameters`, `signal_metrics`)

### 1.3 Tidyquant Integration Pattern

**Core Functions:**
- `tq_get()` - One-stop shop for financial data in tidy format
- `tq_mutate()` - Add columns with financial function results
- `tq_transmute()` - Return new data frame (for periodicity changes)
- `tq_performance()` - Convert returns to performance metrics
- `tq_portfolio()` - Aggregate asset returns into portfolios

**Philosophy:** "Few core functions with a lot of power" - wrap financial algorithms (quantmod, TTR, PerformanceAnalytics) in tidyverse-compatible interface

**Implication for tidy-signal:** Wrap statistical arbitrage algorithms in tidy interface, distinguish mutate vs transmute where periodicity changes

---

## 2. Python Signal/Trading Libraries - Prior Art Analysis

### 2.1 Zipline (Quantopian) - Pipeline API for Alpha Factors

**Status:** Original archived (2020), active fork: zipline-reloaded
**Stars:** 17,000+

**Key Innovation - Pipeline API:**
- **Separates alpha factor computation from order execution**
- Factors are transformations that output predictive signals
- Built-in factors: moving averages, Bollinger Bands, momentum
- Optimizes computations over entire backtest period (not event-by-event)

**Architecture:**
- Event-driven system with `initialize()` and `handle_data()` methods
- Context dictionary maintains state
- Point-in-time data handling to prevent lookahead bias
- Integration with Alphalens (factor analysis) and Pyfolio (performance)

**API Style:** Object-oriented with functional elements (Pipeline API)

**Strengths:**
- Modular factor research
- Production-ready event-driven backtesting
- Strong community and documentation

**Limitations:**
- No longer maintained by Quantopian
- Steep learning curve
- Originally equity-focused

**Lessons for tidy-signal:**
- Separate signal computation from execution
- Pipeline optimization for batch computations
- Point-in-time data as first-class concept

### 2.2 VectorBT - Vectorized Backtesting

**Status:** Active (Pro version invite-only)
**Stars:** 4,000+

**Key Innovation - Vectorized Operations:**
- Tests thousands of strategies in seconds via NumPy/Numba
- Represents strategy instances in multi-dimensional arrays
- Boolean arrays for entry/exit signals

**Signal Definition Pattern:**
```python
entries = fast_ma.ma_crossed_above(slow_ma)
exits = fast_ma.ma_crossed_below(slow_ma)
pf = vbt.Portfolio.from_signals(price, entries, exits, init_cash=100)
```

**Architecture:**
- Hybrid functional-OOP design
- Method chaining on indicator objects
- Factory pattern: `Portfolio.from_signals()`, `Portfolio.from_holding()`
- Interactive Plotly dashboards in Jupyter

**API Style:** Fluent interface with method chaining

**Strengths:**
- Extremely fast parameter optimization
- Pattern recognition (Pro: 230M pattern combinations)
- MAE/MFE analysis for exit optimization
- Portfolio optimization and rebalancing

**Limitations:**
- Pro features require paid membership
- Less intuitive for complex state-dependent strategies

**Lessons for tidy-signal:**
- Boolean arrays for signal representation
- Factory pattern for multiple signal generation methods
- Method chaining for fluent API

### 2.3 Backtrader - Object-Oriented Strategy Framework

**Status:** Active since 2015
**Stars:** 13,000+
**Usage:** Banks and trading houses use for prototyping

**Signal Definition Pattern:**
```python
class SmaCross(bt.SignalStrategy):
    def __init__(self):
        sma1 = bt.ind.SMA(period=10)
        sma2 = bt.ind.SMA(period=30)
        crossover = bt.ind.CrossOver(sma1, sma2)
        self.signal_add(bt.SIGNAL_LONG, crossover)
```

**Signal Types:**
- SIGNAL_LONGSHORT, SIGNAL_LONG, SIGNAL_SHORT
- SIGNAL_LONGEXIT, SIGNAL_SHORTEXIT (override exits)

**Architecture:**
- **Cerebro** - controlling brain, handles strategy instantiation and optimization
- **Strategy lifecycle:** `__init__()` → `prenext()` → `next()`
- Methods: `buy()`, `sell()`, `close()`, `cancel()`

**API Style:** Object-oriented with inheritance-based strategies

**Strengths:**
- Very flexible and customizable
- Extensive documentation and community
- Live trading support
- Position sizing and risk management

**Limitations:**
- More verbose than vectorized approaches
- Slower for parameter optimization

**Lessons for tidy-signal:**
- Signal type taxonomy (entry vs exit, long vs short)
- Strategy lifecycle pattern
- Built-in risk management integration

### 2.4 Alphalens - Factor Analysis Framework

**Status:** Archived (Quantopian closure)
**Stars:** 3,000+

**Key Innovation - Tear Sheet Analysis:**

**Workflow:**
```python
factor_data = alphalens.utils.get_clean_factor_and_forward_returns(
    my_factor, pricing, quantiles=5, groupby=ticker_sector
)
alphalens.tears.create_full_tear_sheet(factor_data)
```

**Four Analysis Categories:**
1. **Returns Analysis** - Factor-sorted portfolio performance by quantile
2. **Information Coefficient** - Correlation between factor and forward returns
3. **Turnover Analysis** - Rebalancing frequency and costs
4. **Grouped Analysis** - Performance by sector/category

**Key Metric:** Information Ratio (mean IC / std IC) - benchmark: IR ≥ 0.05

**API Style:** Functional with utility functions

**Strengths:**
- Comprehensive factor validation
- Quantile-based analysis
- Sector decomposition
- Tear sheet standardization

**Lessons for tidy-signal:**
- Information Coefficient as key validation metric
- Quantile-based signal strength analysis
- Turnover analysis for transaction cost estimation

### 2.5 Pyfolio - Portfolio Performance Analysis

**Status:** Archived, fork: pyfolio-reloaded
**Stars:** 5,500+

**Core Function:**
```python
pf.create_full_tear_sheet(portfolio_returns, benchmark_rets=benchmark_rets)
```

**Tear Sheet Components:**
- Performance statistics table (annual return, Sharpe, beta)
- Cumulative returns plot
- Rolling metrics (beta, Sharpe)
- Drawdown analysis (top 5 worst periods)
- Return distributions and quantiles

**API Style:** Functional with plotting utilities

**Lessons for tidy-signal:**
- Tear sheet pattern for comprehensive reporting
- Rolling metrics for time-varying analysis
- Benchmark comparison as default

### 2.6 Empyrical - Risk Metrics Library

**Status:** Active fork: empyrical-reloaded
**Stars:** 1,200+

**Key Metrics:**
- Sharpe ratio: `sharpe_ratio(returns, risk_free=0, period='daily')`
- Max drawdown, Calmar ratio, Sortino ratio
- Alpha, beta, tail ratio
- Rolling variants: `roll_sharpe_ratio()`

**API Style:** Pure functional - stateless calculations

**Usage:** Backend for pyfolio and zipline metrics

**Lessons for tidy-signal:**
- Separate metrics calculation from analysis
- Support both point-in-time and rolling metrics
- Handle different periodicities (daily, weekly, monthly)

---

## 3. Statistical Arbitrage & Convergence Trading

### 3.1 Pairs Trading Framework

**Core Concepts:**
- **Mean reversion** - Prices revert to long-term equilibrium
- **Cointegration** - Long-run stationary relationship between non-stationary series
- **Spread modeling** - Price difference exhibits mean-reverting behavior

**Process:**
1. Select pairs via cointegration testing
2. Model spread as mean-reverting process
3. Generate entry/exit signals based on spread deviations
4. Manage positions and risk

### 3.2 Cointegration Testing

**Engle-Granger Method:**
- Two-step: (1) OLS regression, (2) ADF test on residuals
- `statsmodels.tsa.stattools.coint()`
- **Limitation:** Sensitive to which asset is dependent, error accumulates between steps

**Johansen Test:**
- Simultaneous estimation and testing
- `statsmodels.tsa.vector_ar.vecm.coint_johansen()`
- **Advantages:**
  - Finds hedge ratio and tests cointegration simultaneously
  - Handles multiple assets (not just pairs)
  - Seeks most stationary linear combination
- **Interpretation:** Compare `trace_stat` and `max_eig_stat` against critical values

**Best Practice:** Use both methods for robustness

### 3.3 Ornstein-Uhlenbeck Process for Spread Modeling

**Model:** dXt = θ(μ - Xt)dt + σdWt
- θ = mean reversion speed
- μ = long-term mean
- σ = volatility

**Two-Step Process:**
1. Fit OU process, find optimal asset ratio via max log-likelihood
2. Solve optimal stopping problem for entry/exit thresholds

**Performance Example:** 16.38% annual return, Sharpe Ratio 1.34 (Brazilian stocks - Caldeira & Moura)

**Python Implementation:** MLE via Kalman filtering (statsmodels)

### 3.4 Convergence Trading in Commodities

**Calendar Spreads:**
- Buy near-month, sell far-month futures (or vice versa)
- Profit from changes in term structure relationship
- Lower margin requirements (75% credit typical)

**Commodity Product Spreads:**
- **Crack spread** - Crude oil vs refined products (gasoline, heating oil)
  - 3-2-1 crack: 3 barrels crude → 2 barrels gas + 1 barrel distillate
- **Crush spread** - Soybeans vs soy meal + soy oil

**Important Caveat:**
> "Commodities are typically trending markets, not mean-reverting - trend following works better"

However, statistical arbitrage on spreads (not outright positions) can work due to arbitrage relationships

**Risks:**
- Convergence may not happen or take too long
- Margin calls if prices diverge first
- Negative skew - consistent small profits, occasional large losses

---

## 4. Vintage Data & Point-in-Time Analysis

### 4.1 ALFRED Database (Federal Reserve)

**Description:** ArchivaL Federal Reserve Economic Data - vintage versions of economic data

**Purpose:**
- Retrieve data as it was available on specific historical dates
- Reproduce past research with data available at the time
- Build accurate forecasting models avoiding lookahead bias
- Analyze policy decisions with contemporaneous data

**Bitemporal Modeling:** Two timelines
- **Observation date** - When event occurred
- **Revision date** - When data was published/revised

**Python Access:** `fredapi` package supports FRED and ALFRED

**Database Size:** 815,000+ data series

### 4.2 The Ragged-Edge Problem

**Definition:** Different publication lags create incomplete recent data (unbalanced dataset)

**Example:**
- Stock prices: current through today
- GDP: current through last quarter
- Employment: current through last month

**Importance:** "Appropriately dealing with jagged edge is key for nowcasting"

### 4.3 Real-Time vs Revised Data

**Challenge:**
- First release is timely but noisy estimate
- Gets revised as more information becomes available
- Final data is object of interest, preliminary data is noisy indicator

**Modeling Approaches:**
- **State-space models** handle publication lags and revisions
- Including simple revision model improves imputation accuracy
- **MIDAS (Mixed-frequency data sampling)** handles unbalanced datasets
- **Factor MIDAS** - Nowcast low-frequency (GDP) using high-frequency indicators with ragged edge

### 4.4 Lookahead Bias Prevention

**Definition:** Using information not available at signal execution time

**Detection Signals:**
- Too-good-to-be-true equity curves (smooth straight line)
- Surprisingly high performance metrics
- No train/test split or walk-forward validation

**Prevention Techniques:**

1. **Signal shifting:**
```python
df['Position'] = df['Buy'].shift(1).fillna(False).astype(int)
```

2. **Event-driven backtesting** - Prevents indexing mistakes with queues and messages

3. **Point-in-time databases** - Track all historical revisions

4. **Train/test splits** - Temporal separation

5. **Walk-forward analysis** - Rolling optimization and validation

---

## 5. Multi-Dimensional Time Series

### 5.1 xarray Library

**Description:** N-dimensional labeled arrays for Python, inspired by pandas

**Key Advantages Over Pandas:**
- Dimensions can have names ('time', 'latitude', 'longitude')
- Operations work regardless of dimension order: `x - x.mean(dim='time')`
- No need to reshape arrays for arithmetic
- Better for ndim > 2 (panel data, climate/weather data)

**Data Structures:**
- **DataArray** - Single multi-dimensional array with labeled dimensions
- **Dataset** - Dict-like container of aligned DataArrays (multi-dimensional DataFrame)

**Time Series Features:**
- `resample()` for temporal upsampling/downsampling
- `groupby()` for split-apply-combine on any dimension
- Integration with pandas for time indexing

**Use Cases:** Geoscience, physics, machine learning, finance (multi-dimensional data)

**Example for Commodities:**
```python
# Dimensions: vintage_date × observation_date × tenor × contract
ds = xr.Dataset({
    'price': (['vintage', 'date', 'tenor', 'contract'], price_array)
})
# Natural slicing:
ds.sel(vintage='2024-01-01', tenor='3M')
```

### 5.2 Term Structure Modeling

**Academic Models:**
- **Gibson & Schwartz (1990)** - Two-factor model
- **Schwartz (1997)** - Three-factor model
- **Schwartz & Smith (2000)** - Short-term (OU) + long-term (Brownian) factors
- **Cortazar & Naranjo (2006)** - N-factor framework

**Seasonality Decomposition:**
f(t) = s(t) + ε(t) where:
- s(t) = seasonal component
- ε(t) = smooth deviation from seasonality

**Estimation:** Kalman filtering for MLE of unobserved factors

**Python Tools:**
- QuantLib-Python - Term structure classes
- statsmodels - State space models for Kalman filtering

**R Package:** NFCP - N-factor commodity pricing models

---

## 6. Statistical Methods Inventory (Ranked)

### Rank 1: Cointegration Testing (Critical)
**Methods:** Johansen & Engle-Granger
**Purpose:** Identify pairs with long-term stationary relationships
**Python:** `statsmodels.tsa.stattools.coint()`, `statsmodels.tsa.vector_ar.vecm.coint_johansen()`
**Use Case:** Pairs selection for statistical arbitrage

### Rank 2: Stationarity Testing (Critical)
**Methods:** ADF, KPSS
**Purpose:** Test if spread/series is mean-reverting vs trending
**Python:** `statsmodels.tsa.stattools.adfuller()`, `statsmodels.tsa.stattools.kpss()`
**Best Practice:** Use both tests together (opposite null hypotheses)
**Interpretation:**
- ADF rejects null → stationary
- KPSS fails to reject null → stationary
- Both agree → robust conclusion

### Rank 3: Walk-Forward Analysis (Critical)
**Purpose:** Out-of-sample validation with rolling optimization
**Process:**
1. Optimize on in-sample window
2. Test on following out-of-sample period
3. Roll window forward
4. Aggregate results

**Benefit:** Reduces overfitting, tests adaptability to changing markets
**Gold Standard:** Robert Pardo (1992) - "Design, Testing and Optimization of Trading Systems"

### Rank 4: Structural Break Detection (High)
**Methods:** Zivot-Andrews, Chow test
**Purpose:** Detect regime changes that invalidate historical relationships
**Python:** `statsmodels.tsa.stattools.zivot_andrews()`
**Use Case:** Identify when cointegration relationship breaks down

### Rank 5: Ornstein-Uhlenbeck Parameter Estimation (High)
**Purpose:** Estimate mean reversion speed, equilibrium level, volatility
**Estimation:** Maximum Likelihood Estimation via Kalman filtering
**Parameters:**
- θ (theta) - mean reversion speed
- μ (mu) - long-term mean
- σ (sigma) - volatility
**Use Case:** Determine optimal entry/exit thresholds

### Rank 6: Information Coefficient Analysis (High)
**Purpose:** Measure correlation between signal and forward returns
**Metric:** Information Ratio (mean IC / std IC)
**Benchmark:** IR ≥ 0.05 is considered good
**Python:** alphalens library
**Use Case:** Factor validation and ranking

### Rank 7: Volatility Modeling - GARCH (Medium)
**Purpose:** Model time-varying volatility for risk management
**Models:** GARCH, EGARCH, GJR-GARCH
**Python:** `arch` library
**Use Case:** Position sizing, risk-adjusted entry/exit

### Rank 8: Half-Life Estimation (Medium)
**Purpose:** Measure how quickly spread reverts to mean
**Calculation:** half_life = -log(2) / log(AR(1) coefficient)
**Use Case:** Set holding period expectations

### Rank 9: Kalman Filtering (Medium)
**Purpose:** Estimate unobserved factors and time-varying parameters
**Python:** `statsmodels.tsa.statespace`
**Use Case:** Term structure modeling, adaptive hedge ratios

### Rank 10: Seasonality Decomposition (Medium)
**Purpose:** Separate seasonal patterns from trend and residual
**Python:** `statsmodels.tsa.seasonal.seasonal_decompose()`
**Use Case:** Agricultural and energy commodity modeling
**Importance:** High for commodities with harvest cycles or seasonal demand

---

## 7. Data Structure Recommendations

### 7.1 Multi-Dimensional Structure (xarray)

**Problem:** Handle data with vintage_date × observation_date × tenor × contracts

**Recommended Structure:** `xarray.Dataset` with named dimensions

**Example Dimensions:**
```python
ds = xr.Dataset({
    'price': (['vintage_date', 'observation_date', 'tenor', 'contract'], data),
    'volume': (['vintage_date', 'observation_date', 'tenor', 'contract'], data)
})
```

**Advantages:**
- Natural representation of multi-dimensional data
- Operations work regardless of dimension order
- Easy slicing: `ds.sel(vintage_date='2024-01-01', tenor='3M')`
- Alignment happens automatically
- Integrates with pandas for I/O

### 7.2 Tidy Format for Signals

**Structure:** Long format following Hadley Wickham's tidy data principles

```
| date       | contract | signal_name    | signal_value | confidence | metadata |
|------------|----------|----------------|--------------|------------|----------|
| 2024-01-01 | CL_M1    | mean_reversion | 1.0          | 0.85       | {...}    |
| 2024-01-01 | CL_M2    | mean_reversion | 0.5          | 0.60       | {...}    |
```

**Advantages:**
- Follows tidy data principles (each variable is a column, each observation is a row)
- Easy to filter, group, and aggregate
- Natural for time series operations
- Integrates well with plotting libraries

### 7.3 Signal Specification Pattern (Frozen Dataclass)

**Recommendation:** Immutable frozen dataclass similar to parsnip ModelSpec

```python
@dataclass(frozen=True)
class SignalSpec:
    signal_type: str  # 'mean_reversion', 'trend_following', etc.
    engine: str       # 'statsmodels', 'sklearn', 'custom'
    mode: str         # 'long_short', 'long_only', 'short_only'
    args: dict        # Hyperparameters
    metadata: dict    # Creation date, version, etc.
```

**Benefits:**
- **Immutable** - prevents side effects when reusing specs
- **Serializable** - can save/load configurations (reproducible research)
- **Type-safe** - frozen dataclasses are hashable (can use as dict keys)
- **Replace() method** - create modified copies without mutation

### 7.4 Output Standardization (Three-DataFrame Pattern)

**Inspired by broom package:**

**1. signal_outputs (Per-Observation Results):**
```
| date       | contract | signal_value | confidence | position | entry_price | exit_price | pnl   |
|------------|----------|--------------|------------|----------|-------------|------------|-------|
```

**2. signal_parameters (Per-Parameter Statistics):**
```
| parameter_name | value | std_error | confidence_interval_lower | confidence_interval_upper |
|----------------|-------|-----------|---------------------------|---------------------------|
```

**3. signal_metrics (Per-Signal Summary):**
```
| sharpe_ratio | information_ratio | max_drawdown | win_rate | profit_factor | turnover |
|--------------|-------------------|--------------|----------|---------------|----------|
```

---

## 8. API Pattern Recommendations

### 8.1 Fluent Interface Design (Method Chaining)

**Rationale:** Method chaining improves readability and reduces intermediate variables

**Pattern:** Return self (or new instance) from methods to enable chaining

**Example:**
```python
signal = (SignalSpec()
    .set_type('mean_reversion')
    .set_engine('statsmodels')
    .set_lookback(20)
    .set_threshold(2.0))
```

**Considerations:**
- Use copy-on-write pattern for immutability (like pandas)
- Don't make chains too long (readability suffers)
- Consider both mutable (return self) and immutable (return copy) variants

### 8.2 Tidyverse-Inspired Verbs

**Data Manipulation:**
- `detect_cointegration()` - Test pairs for cointegration
- `filter_signals()` - Select signals by criteria
- `mutate_signals()` - Add derived signal columns
- `summarize_performance()` - Aggregate to performance metrics
- `group_by_contract()` - Apply operations per contract

**Signal Operations:**
- `specify_signal()` - Create signal specification
- `fit_signal()` - Fit signal to historical data
- `validate_signal()` - Out-of-sample validation
- `deploy_signal()` - Generate live signals

**Workflow Composition:**
- `add_preprocessing()` - Add data preprocessing step
- `add_signal()` - Add signal specification
- `add_validation()` - Add validation method
- `add_execution()` - Add execution logic

### 8.3 Registry Pattern for Extensibility

**Pattern:** Decorator-based registration like parsnip engines

**Example:**
```python
@register_signal('mean_reversion', 'ou_process')
class OUSignalEngine(SignalEngine):
    def fit(self, data, spec):
        # Fit Ornstein-Uhlenbeck process
        pass

    def predict(self, data, fit):
        # Generate signals
        pass
```

**Benefits:**
- Runtime discovery of available signals: `get_available_signals()`
- Easy to add custom implementations
- Clean separation of interface and implementation
- Plugin architecture for third-party extensions

**Implementation:**
```python
_SIGNAL_REGISTRY = {}

def register_signal(signal_type, engine):
    def decorator(cls):
        _SIGNAL_REGISTRY[(signal_type, engine)] = cls
        return cls
    return decorator

def get_signal(signal_type, engine):
    return _SIGNAL_REGISTRY[(signal_type, engine)]()
```

### 8.4 Dual-Path Architecture

**Rationale:** Some signals need raw data access for complex temporal patterns

**Pattern:** Standard path vs Raw path (like py-parsnip)

**Standard Path:**
```python
preprocess(data) → fit(preprocessed_data) → predict(new_data)
```

**Raw Path:**
```python
fit_raw(raw_data) → predict_raw(raw_new_data)
```

**Use Cases:**
- **Standard:** Linear signals with simple feature engineering
- **Raw:** ARIMA with datetime handling, OU process fitting with vintage data

**Implementation:** Check `hasattr(engine, 'fit_raw')` to determine path

---

## 9. Gap Analysis - What tidy-signal Provides

### 9.1 What Already Exists

- General backtesting frameworks (zipline, backtrader, vectorbt)
- Statistical testing libraries (statsmodels, arch)
- Performance metrics (empyrical, pyfolio)
- Factor analysis (alphalens)
- Financial data wrappers (tidyquant in R)

### 9.2 Unique Value of tidy-signal

| Gap | tidy-signal Solution | Benefit |
|-----|---------------------|---------|
| No unified grammar for signal detection | Tidyverse-inspired verb API: `detect_*`, `validate_*`, `evaluate_*` | Consistent, composable interface across signal types |
| Fragmented tools for statistical arbitrage | Integrated cointegration → OU fitting → optimal stopping workflow | End-to-end pairs trading pipeline in one package |
| No native support for vintage/point-in-time data | First-class support for `vintage_date` dimension | Proper handling of data revisions, avoid lookahead bias |
| Limited multi-dimensional time series support | xarray integration for tenor × vintage × time | Natural representation of forward curves and term structures |
| No standardized signal output format | Three-DataFrame pattern (outputs, parameters, metrics) like broom | Consistent interface for downstream analysis and comparison |
| Commodities-specific patterns underserved | Built-in support for seasonality, calendar spreads, crack spreads | Domain-specific features for commodity traders |
| Signal validation often manual | Built-in walk-forward analysis, IC analysis, structural break detection | Rigorous validation workflow baked into package |
| Configuration management for signal specs | Immutable frozen dataclass specs with serialization | Reproducible research, version control for strategies |

### 9.3 Unique Value Proposition

> "Bringing the tidyverse philosophy to commodities signal detection with modern Python tooling, native vintage data support, and comprehensive validation workflows"

---

## 10. Implementation Recommendations

### Scenario 1: Pairs Trading on Commodity Spreads

**Recommended Solution:** Integrated cointegration → OU process → signal generation

```python
signals = (data
    .detect_cointegration(method='johansen', threshold=0.05)
    .fit_ou_process()
    .generate_signals(entry_threshold=2.0, exit_threshold=0.5))
```

**Rationale:** Integrated workflow from pair selection through signal generation, leverages OU process optimal stopping theory

### Scenario 2: Term Structure Arbitrage on Forward Curves

**Recommended Solution:** xarray-based term structure modeling with calendar spread detection

```python
spreads = (curves
    .calculate_spreads(type='calendar', front='M1', back='M3')
    .detect_anomalies(method='zscore', window=20)
    .validate_signals(method='walk_forward'))
```

**Rationale:** Multi-dimensional data structure naturally handles tenor × time, built-in spread calculations

### Scenario 3: Nowcasting with Ragged-Edge Data

**Recommended Solution:** MIDAS regression with vintage data support

```python
forecast = (data
    .filter_vintage(as_of='2024-01-01')
    .fit_midas(low_freq='monthly', high_freq='daily')
    .predict(horizon='1M'))
```

**Rationale:** Handles mixed frequency and publication lags, vintage dimension prevents lookahead bias

### Scenario 4: Trend Following on Commodity Momentum

**Recommended Solution:** Vectorized signal generation with fast backtesting

```python
signals = (prices
    .calculate_indicator('moving_average', [10, 20, 50])
    .generate_crossover_signals()
    .backtest(commission=0.001)
    .evaluate_performance())
```

**Rationale:** Fast parameter optimization, natural for simple trend rules

### Scenario 5: Multi-Factor Signal Combination

**Recommended Solution:** Workflow composition with add_signal() pattern

```python
workflow = (SignalWorkflow()
    .add_signal(mean_reversion_signal, weight=0.4)
    .add_signal(momentum_signal, weight=0.3)
    .add_signal(seasonality_signal, weight=0.3)
    .add_execution_rules()
    .fit(train_data)
    .validate(test_data))
```

**Rationale:** Modular signal definitions, easy to weight and combine

---

## 11. Community Insights

### Popular Solutions
- Vectorized backtesting (vectorbt) for speed
- Event-driven backtesting (zipline, backtrader) for realism
- Cointegration testing for pairs selection
- Walk-forward analysis for validation
- Jupyter notebooks for research workflow

### Controversial Topics
- **Vectorized vs event-driven backtesting** - Speed vs realism trade-offs
- **Mean reversion in commodities** - Conventional wisdom says no, but pairs trading on spreads can work
- **Optimal lookback windows** - Vary by market regime, no universal answer
- **Out-of-sample weight** - How much to trust vs in-sample performance
- **Classification vs regression** - For signal generation approaches

### Expert Opinions

> "Separate alpha factor computation from order execution" - Quantopian (Pipeline API design)

> "Walk-forward analysis is the gold standard for validation" - Robert Pardo (1992)

> "Tidy datasets are all alike, but every messy dataset is messy in its own way" - Hadley Wickham

> "Commodities are trending markets, use momentum not mean reversion" - Common wisdom
> BUT: Statistical arbitrage on spreads (not outright) can work due to arbitrage relationships

> "Use both ADF and KPSS tests together for robust stationarity assessment" - Best practice from econometrics community

---

## 12. Key Literature References

### Foundational Papers
- Wickham, H. (2014). "Tidy Data." *Journal of Statistical Software*, 59(10).
- Schwartz, E. S., & Smith, J. E. (2000). "Short-term variations and long-term dynamics in commodity prices." *Management Science*.
- Engle, R. F., & Granger, C. W. J. (1987). "Co-integration and error correction." *Econometrica*.
- Pardo, R. (1992). "Design, Testing and Optimization of Trading Systems."

### R Packages & Documentation
- dplyr: https://dplyr.tidyverse.org/
- tidymodels: https://www.tidymodels.org/
- broom: https://broom.tidymodels.org/
- tidyquant: https://business-science.github.io/tidyquant/

### Python Libraries
- zipline: https://github.com/quantopian/zipline
- vectorbt: https://github.com/polakowo/vectorbt
- alphalens: https://github.com/quantopian/alphalens
- statsmodels: https://www.statsmodels.org/
- arch: https://arch.readthedocs.io/
- xarray: https://xarray.pydata.org/

### Books & Practitioner Resources
- Jansen, S. "Machine Learning for Trading." https://www.ml4trading.io/
- Hilpisch, Y. "Python for Finance: Analyze Big Financial Data."
- Chan, E. "Quantitative Trading" and "Algorithmic Trading."
- Lopez de Prado, M. "Advances in Financial Machine Learning."

### Academic Papers on Methodology
- Bańbura, M., et al. "Nowcasting." ECB Working Paper.
- Various. "Factor MIDAS for Nowcasting with Ragged-Edge Data." *Oxford Bulletin*.
- Various. "Pairs trading with fractional Ornstein–Uhlenbeck spread model." *Applied Economics*.

### Data & Methodology Resources
- ALFRED Database: https://alfred.stlouisfed.org/
- Hudson & Thames Research: https://hudsonthames.org/
- QuantConnect Documentation

---

## 13. Conclusion & Next Steps

### Viability Assessment: STRONG

tidy-signal fills a clear gap in the Python ecosystem by combining:
1. Tidyverse design philosophy
2. Commodity-specific domain knowledge
3. Native vintage data support
4. Comprehensive validation workflows

### Recommended Development Priorities

**Phase 1: Core Infrastructure**
1. Data structures (xarray integration, vintage data handling)
2. Signal specification pattern (frozen dataclass)
3. Registry pattern for extensibility
4. Three-DataFrame output standardization

**Phase 2: Statistical Arbitrage Module**
1. Cointegration testing (Johansen & Engle-Granger)
2. Ornstein-Uhlenbeck process fitting
3. Optimal stopping for entry/exit
4. Pairs selection utilities

**Phase 3: Validation Framework**
1. Walk-forward analysis
2. Information Coefficient analysis
3. Structural break detection
4. Lookahead bias testing

**Phase 4: Commodities-Specific Features**
1. Calendar spread utilities
2. Crack/crush spread calculations
3. Seasonality modeling
4. Term structure analysis

**Phase 5: Workflow Composition**
1. Multi-signal combination
2. Pipeline optimization
3. Production deployment tools

### Success Metrics
- Adoption by quant researchers
- Contributions from community
- Benchmark comparisons vs existing tools
- Real-world strategy performance

---

**End of Research Summary**
