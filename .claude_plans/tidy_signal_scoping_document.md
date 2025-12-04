# tidy-signal: Comprehensive Research Scoping Document

**Version:** 1.0 | **Date:** December 4, 2025 | **Status:** Research Complete

---

## Executive Summary

**Verdict: HIGHLY VIABLE**

`tidy-signal` fills a clear gap in the Python quantitative finance ecosystem by uniquely combining:
1. **Tidyverse-style API** for signal detection workflows
2. **Native vintage data support** for point-in-time backtesting (prevent lookahead bias)
3. **Convergence dynamics analysis** for optimal entry/exit timing
4. **Seamless py-tidymodels integration** for fundamental model predictions
5. **Statistical rigor** with built-in validation tests
6. **Commodity-specific features** (spreads, seasonality, term structure)

The library provides a unified grammar for testing divergence between forward curve fair values and fundamental model predictions, specifically tracking how divergence moves as contracts approach settlement.

---

## 1. Problem Definition & Conceptual Framework

### 1.1 Core Problem Statement

Commodities traders and quantitative researchers need to:
1. **Detect divergence** between forward curve prices and fundamental model fair values
2. **Track divergence evolution** as contracts approach settlement (the "cohort" concept)
3. **Determine optimal entry/exit timing** based on convergence dynamics
4. **Validate statistical significance** of divergence signals
5. **Avoid lookahead bias** through proper vintage data handling
6. **Maintain audit trails** for regulatory compliance and reproducibility

### 1.2 The Cohort Concept

**Definition:** A "cohort" tracks the same settlement contract through time, observing how divergence between forward price and fundamental value evolves as settlement approaches.

**Key Dimensions:**
```
Time Axes:
├── observation_date: When we observe the data
├── vintage_date: When the data was available (for point-in-time analysis)
├── settlement_date: Contract expiration date
└── days_to_settlement: settlement_date - observation_date

Signal Dimensions:
├── forward_price: Market price from forward curve
├── fundamental_value: Model prediction (from py-parsnip model)
├── divergence: forward_price - fundamental_value
├── divergence_zscore: Standardized divergence
└── convergence_velocity: Rate of change in divergence
```

**Cohort Lifecycle:**
```
Settlement Date: June 2025
Cohort Start: January 2025 (5 months to settlement)

Jan 1:  Days=150, Div=+$4.00, Forward=$22, Fund=$18
Feb 1:  Days=120, Div=+$3.50, Forward=$21, Fund=$17.50
Mar 1:  Days=90,  Div=+$2.80, Forward=$20, Fund=$17.20
Apr 1:  Days=60,  Div=+$1.50, Forward=$19, Fund=$17.50
May 1:  Days=30,  Div=+$0.50, Forward=$18, Fund=$17.50
Jun 1:  Days=0,   Div=$0.00,  Forward=$18, Fund=$18 (convergence)
```

### 1.3 Why Divergence Matters

**Convergence Hypothesis:** Forward prices and fundamental fair values should converge as settlement approaches because:
1. **Arbitrage forces** eliminate mispricing near delivery
2. **Information asymmetry** decreases as uncertainty resolves
3. **Physical delivery** enforces final price alignment

**Trading Opportunity:** If divergence is statistically significant and mean-reverting, we can:
- **Enter** when divergence exceeds threshold (e.g., 2σ)
- **Exit** when divergence normalizes or at profit target
- **Size positions** based on convergence confidence

---

## 2. Multi-Dimensional Data Structure

### 2.1 Four-Dimensional Analysis Framework

```python
# Core data structure using xarray
import xarray as xr

ds = xr.Dataset({
    'forward_price': (['vintage_date', 'observation_date', 'tenor', 'contract'], data),
    'fundamental_value': (['vintage_date', 'observation_date', 'tenor', 'contract'], data),
    'inventory': (['vintage_date', 'observation_date'], data),
    'demand': (['vintage_date', 'observation_date'], data)
})

# Natural slicing operations
ds.sel(vintage_date='2024-01-01', tenor='3M')  # Point-in-time view
ds.sel(contract='CL_Jun25')  # Single contract cohort
```

### 2.2 Dimension Definitions

| Dimension | Description | Purpose |
|-----------|-------------|---------|
| `vintage_date` | When data was published/available | Prevent lookahead bias |
| `observation_date` | When event occurred | Time series ordering |
| `tenor` | Time to settlement (1M, 3M, 6M, etc.) | Forward curve position |
| `contract` | Specific contract identifier | Cohort tracking |

### 2.3 Vintage Data Handling

**The Ragged-Edge Problem:**
- Different data sources have different publication lags
- Model inputs may be revised after initial release
- Must use only data available at decision time

**Solution:** `VintageDataFrame` wrapper for xarray
```python
class VintageDataFrame:
    """Multi-dimensional data structure with vintage support"""

    def as_of(self, vintage_date):
        """Filter to data available as of vintage_date"""
        return self.ds.sel(vintage_date=vintage_date, method='ffill')

    def latest(self):
        """Get most recent vintage"""
        return self.ds.isel(vintage_date=-1)

    def to_cohort(self, settlement_date):
        """Extract single cohort tracking through time"""
        return self.ds.sel(contract=settlement_date)
```

---

## 3. Verb Grammar Design

### 3.1 Core Verb Categories

**Data Preparation:**
| Verb | Purpose | Example |
|------|---------|---------|
| `align()` | Match vintages and tenors across data sources | `align(forwards, fundamentals, by='observation_date')` |
| `slice()` | Extract specific vintage/tenor combinations | `slice(vintage='2024-01-01', tenor='3M')` |

**Signal Construction:**
| Verb | Purpose | Example |
|------|---------|---------|
| `detect()` | Compute divergence between forward and fundamental | `detect(signal_type='divergence', standardize=True)` |
| `decompose()` | Break spread into trend, seasonal, residual | `decompose(method='stl', period=52)` |

**Calibration:**
| Verb | Purpose | Example |
|------|---------|---------|
| `calibrate()` | Fit convergence model (OU, ECM, threshold) | `calibrate(model='ou_process')` |
| `diagnose()` | Run statistical validity tests | `diagnose(tests=['stationarity', 'cointegration'])` |

**Evaluation:**
| Verb | Purpose | Example |
|------|---------|---------|
| `evaluate()` | Score signal strength and confidence | `evaluate(metrics=['ic', 'hit_rate'])` |
| `converge()` | Analyze convergence dynamics | `converge(analysis=['half_life', 'velocity'])` |

**Trading Rules:**
| Verb | Purpose | Example |
|------|---------|---------|
| `time_entry()` | Determine optimal entry timing | `time_entry(threshold=2.0, min_tenor=60)` |
| `time_exit()` | Determine optimal exit timing | `time_exit(take_profit=0.85, stop_loss=1.8)` |
| `backtest()` | Historical performance evaluation | `backtest(transaction_costs=0.002)` |

**Monitoring:**
| Verb | Purpose | Example |
|------|---------|---------|
| `monitor()` | Track relationship stability | `monitor(window=252, alert_threshold=2.5)` |
| `compare()` | Compare signals across models/tenors | `compare(by=['model', 'tenor'])` |
| `trace()` | Generate full audit trail | `trace(include=['inputs', 'decisions', 'outputs'])` |

### 3.2 Fluent Interface Pattern

```python
# Complete workflow with method chaining
signal = (align(forwards, model.predict(data))
          .detect(signal_type='divergence', standardize=True)
          .calibrate(convergence_model='ou_process')
          .diagnose(tests=['stationarity', 'cointegration'])
          .converge(analysis_type=['half_life', 'optimal_window'])
          .time_entry(entry_threshold=2.0, min_tenor=60)
          .time_exit(take_profit=0.85, stop_loss=1.8)
          .backtest(transaction_costs=0.002))

# Extract standardized outputs
outputs, coefficients, stats = signal.extract_outputs()
```

---

## 4. Core Data Structures

### 4.1 SignalSpec (Immutable Specification)

```python
from dataclasses import dataclass, field
from typing import Dict, Any, Optional

@dataclass(frozen=True)
class SignalSpec:
    """Immutable signal specification following parsnip pattern"""
    signal_type: str                    # "divergence", "ratio", "spread"
    forward_source: Dict[str, Any]      # Forward curve data config
    fundamental_model: 'ModelFit'       # From py-parsnip
    alignment_rules: Dict[str, Any]     # Vintage/tenor alignment
    convergence_model: str = "ou_process"
    standardize: bool = True
    args: Dict[str, Any] = field(default_factory=dict)

    def set_args(self, **kwargs) -> 'SignalSpec':
        """Return new spec with updated args (immutable)"""
        new_args = {**self.args, **kwargs}
        return dataclasses.replace(self, args=new_args)
```

### 4.2 SignalFit (Calibrated Relationship)

```python
@dataclass
class SignalFit:
    """Container for fitted signal results"""
    spec: SignalSpec
    calibration_data: Dict[str, Any]
    convergence_params: Dict[str, float]  # half_life, lambda, mu, sigma
    entry_rules: Dict[str, Any]
    exit_rules: Dict[str, Any]
    blueprint: 'SignalBlueprint'
    evaluation_data: Optional[Dict[str, Any]] = None

    def predict(self, new_data, **kwargs):
        """Generate signals on new data"""
        engine = get_engine(self.spec.signal_type, self.spec.convergence_model)
        return engine.predict(self, new_data, **kwargs)

    def extract_outputs(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Return three-DataFrame standardized output"""
        return self.outputs_df, self.parameters_df, self.metrics_df
```

### 4.3 Three-DataFrame Output Pattern

**1. Outputs DataFrame (Observation-Level):**
| Column | Type | Description |
|--------|------|-------------|
| `date` | datetime | Observation date |
| `contract` | str | Contract identifier |
| `days_to_settlement` | int | Days until settlement |
| `forward_value` | float | Forward curve price |
| `fundamental_value` | float | Model prediction |
| `divergence` | float | forward - fundamental |
| `divergence_zscore` | float | Standardized divergence |
| `signal_strength` | float | Normalized strength (-1 to 1) |
| `entry_signal` | bool | Entry triggered |
| `exit_signal` | bool | Exit triggered |
| `convergence_velocity` | float | Rate of divergence change |
| `confidence` | float | Signal confidence (0 to 1) |
| `p_value` | float | Statistical significance |
| `split` | str | 'train', 'test', 'validation' |

**2. Coefficients DataFrame (Relationship Parameters):**
| Column | Type | Description |
|--------|------|-------------|
| `parameter_name` | str | Parameter identifier |
| `value` | float | Estimated value |
| `std_error` | float | Standard error |
| `t_statistic` | float | t-statistic |
| `p_value` | float | Significance level |
| `ci_lower` | float | Lower confidence interval |
| `ci_upper` | float | Upper confidence interval |

**Key Parameters:**
- `mean_reversion_speed` (λ): From OU process
- `long_run_mean` (μ): Equilibrium divergence level
- `volatility` (σ): Divergence volatility
- `half_life`: Days for 50% divergence decay
- `hedge_ratio`: Optimal hedge ratio
- Feature importances (if ML model used)

**3. Stats DataFrame (Signal-Level Metrics):**
| Metric | Description |
|--------|-------------|
| `hit_rate` | Percentage of winning signals |
| `sharpe_ratio` | Risk-adjusted return |
| `information_coefficient` | Correlation with forward returns |
| `max_drawdown` | Maximum peak-to-trough decline |
| `profit_factor` | Gross profit / gross loss |
| `avg_holding_period` | Average days in position |
| `turnover` | Portfolio turnover rate |
| `num_signals` | Total signals generated |

---

## 5. Convergence Analysis Framework

### 5.1 Ornstein-Uhlenbeck Process

**Model:** dD = -λ(D - μ)dt + σdW

Where:
- D = divergence (forward - fundamental)
- λ = mean reversion speed
- μ = long-run mean (equilibrium divergence)
- σ = volatility
- dW = Wiener process (random noise)

**Key Metrics:**
- **Half-life:** t₁/₂ = ln(2) / λ (days for 50% decay)
- **Expected convergence:** E[D_t] = μ + (D_0 - μ)e^(-λt)
- **Variance:** Var[D_t] = (σ²/2λ)(1 - e^(-2λt))

### 5.2 Entry/Exit Optimization

```python
def optimize_entry_exit(divergence_series, half_life, volatility):
    """
    Optimize entry/exit thresholds based on OU dynamics.

    Entry: When |divergence| > entry_threshold * std
    Exit: When |divergence| < exit_threshold * std OR time decay
    """
    # Optimal entry: Balance signal strength vs false positive rate
    # Literature suggests 1.5-2.5σ for mean reversion strategies
    entry_threshold = 2.0  # Standard deviations

    # Exit conditions:
    # 1. Take profit at X% convergence toward equilibrium
    take_profit_pct = 0.85  # 85% convergence

    # 2. Stop loss at Y× divergence expansion
    stop_loss_multiplier = 1.8  # 80% expansion from entry

    # 3. Time decay exit after N× half-life
    max_holding_halflifes = 3.0  # Exit after 3 half-lives if no convergence

    return EntryExitRules(
        entry_threshold=entry_threshold,
        take_profit=take_profit_pct,
        stop_loss=stop_loss_multiplier,
        time_decay=max_holding_halflifes * half_life
    )
```

### 5.3 Optimal Entry Window Analysis

```python
def analyze_optimal_window(cohort_data, tenor_buckets):
    """
    Analyze optimal entry window by days-to-settlement.

    Returns Sharpe ratio by tenor bucket to identify
    when divergence signals are most profitable.
    """
    results = []
    for tenor in tenor_buckets:
        subset = cohort_data[cohort_data['days_to_settlement'].between(*tenor)]
        sharpe = calculate_sharpe(subset['signal_returns'])
        results.append({
            'tenor_min': tenor[0],
            'tenor_max': tenor[1],
            'sharpe_ratio': sharpe,
            'hit_rate': calculate_hit_rate(subset),
            'avg_divergence': subset['divergence'].mean()
        })
    return pd.DataFrame(results)
```

---

## 6. Statistical Methods (Ranked by Priority)

### 6.1 Critical Methods

| Rank | Method | Purpose | Python Implementation |
|------|--------|---------|----------------------|
| 1 | **Cointegration (Johansen)** | Pairs selection, hedge ratios | `statsmodels.tsa.vector_ar.vecm.coint_johansen()` |
| 2 | **Cointegration (Engle-Granger)** | Two-step pairs testing | `statsmodels.tsa.stattools.coint()` |
| 3 | **Stationarity (ADF + KPSS)** | Mean reversion validation | `statsmodels.tsa.stattools.adfuller()`, `kpss()` |
| 4 | **Walk-Forward Analysis** | Out-of-sample validation | Custom implementation |

### 6.2 High Priority Methods

| Rank | Method | Purpose | Python Implementation |
|------|--------|---------|----------------------|
| 5 | **Structural Breaks (Zivot-Andrews)** | Regime changes | `statsmodels.tsa.stattools.zivot_andrews()` |
| 6 | **OU Parameter Estimation** | Half-life, entry/exit | MLE via Kalman filtering |
| 7 | **Information Coefficient** | Factor validation | alphalens / custom |
| 8 | **Half-Life Estimation** | Holding period | AR(1) coefficient analysis |

### 6.3 Medium Priority Methods

| Rank | Method | Purpose | Python Implementation |
|------|--------|---------|----------------------|
| 9 | **GARCH Volatility** | Risk management | `arch` library |
| 10 | **Kalman Filtering** | State estimation | `statsmodels.tsa.statespace` |
| 11 | **Seasonality Decomposition** | Commodity cycles | `statsmodels.tsa.seasonal` |

### 6.4 Stationarity Testing Protocol

```python
def test_stationarity(series, significance=0.05):
    """
    Combined ADF + KPSS testing for robust stationarity assessment.

    ADF null: Series has unit root (non-stationary)
    KPSS null: Series is stationary

    Best practice: Use both tests with opposite null hypotheses.
    """
    adf_result = adfuller(series)
    kpss_result = kpss(series)

    adf_stationary = adf_result[1] < significance
    kpss_stationary = kpss_result[1] > significance

    if adf_stationary and kpss_stationary:
        return 'stationary', 'high_confidence'
    elif not adf_stationary and not kpss_stationary:
        return 'non_stationary', 'high_confidence'
    else:
        return 'inconclusive', 'low_confidence'
```

---

## 7. EDA Workflow Design

### 7.1 Signal Discovery Phase

```python
# Step 1: Align data sources
aligned = (align(forward_curves, fundamental_model.predict(features))
           .slice(vintage='latest'))

# Step 2: Calculate divergence
divergence = (aligned
              .detect(signal_type='divergence')
              .decompose(method='stl'))

# Step 3: Test statistical properties
diagnostics = (divergence
               .diagnose(tests=['stationarity', 'cointegration', 'structural_breaks']))

# Step 4: Visualize cohort patterns
divergence.plot_cohort_evolution(by='settlement_date')
divergence.plot_divergence_distribution(by='days_to_settlement')
```

### 7.2 Calibration Phase

```python
# Step 5: Fit convergence model
calibrated = (divergence
              .calibrate(model='ou_process')
              .converge(analysis=['half_life', 'optimal_window']))

# Step 6: Optimize entry/exit
rules = (calibrated
         .time_entry(threshold=2.0, min_tenor=60)
         .time_exit(take_profit=0.85, stop_loss=1.8))

# Step 7: Generate signals
signals = rules.generate_signals()
```

### 7.3 Validation Phase

```python
# Step 8: Walk-forward backtest
backtest_results = (signals
                    .backtest(
                        method='walk_forward',
                        train_window=252,
                        test_window=63,
                        transaction_costs=0.002
                    ))

# Step 9: Extract results
outputs, coefficients, stats = backtest_results.extract_outputs()

# Step 10: Generate tear sheet
backtest_results.tear_sheet(output='html')
```

---

## 8. Red Flags Checklist

### 8.1 Data Quality Red Flags

| Red Flag | Detection Method | Mitigation |
|----------|------------------|------------|
| Lookahead bias | Check vintage dates vs signal dates | Use `as_of()` consistently |
| Survivorship bias | Check for missing contracts | Include delisted/expired |
| Data gaps | Check observation continuity | Interpolate or flag |
| Stale prices | Check last update timestamps | Exclude stale data |
| Publication lag | Compare vintage vs observation | Model publication delays |

### 8.2 Statistical Red Flags

| Red Flag | Detection Method | Mitigation |
|----------|------------------|------------|
| Non-stationarity | ADF + KPSS tests | Difference or use ECM |
| Structural breaks | Zivot-Andrews test | Regime-aware models |
| Spurious regression | Cointegration tests | Verify true relationship |
| Overfitting | Walk-forward OOS | Cross-validation |
| Parameter instability | Rolling estimation | Adaptive parameters |

### 8.3 Strategy Red Flags

| Red Flag | Detection Method | Mitigation |
|----------|------------------|------------|
| Too-good equity curve | Suspiciously high Sharpe | Verify no leakage |
| Excessive turnover | Trade frequency analysis | Widen thresholds |
| Concentration risk | Position analysis | Diversify signals |
| Capacity constraints | Volume analysis | Size appropriately |
| Regime dependence | Subsample analysis | Regime indicators |

---

## 9. Prior Art Analysis

### 9.1 Python Libraries Comparison

| Library | Key Innovation | Lesson for tidy-signal |
|---------|----------------|------------------------|
| **Zipline** (17k+ stars) | Pipeline API separates factors from execution | Modular signal architecture |
| **VectorBT** (4k+ stars) | Vectorized operations (thousands/second) | Boolean signal arrays + fluent API |
| **Backtrader** (13k+ stars) | Comprehensive signal taxonomy | Entry/exit signal types |
| **Alphalens** (3k+ stars) | Information Coefficient analysis | IC as validation metric |
| **Pyfolio** (5.5k+ stars) | Performance tear sheets | Three-DataFrame output |
| **Empyrical** (1.2k+ stars) | Pure functional metrics | Separate calculation from analysis |

### 9.2 Gap Analysis - What tidy-signal Uniquely Provides

| Gap | Current State | tidy-signal Solution |
|-----|---------------|---------------------|
| No unified signal grammar | Fragmented tools | Tidyverse verb API |
| Fragmented stat arb tools | Multiple libraries | Integrated coint → OU → signals |
| No vintage data support | Manual handling | First-class `vintage_date` dimension |
| Limited multi-dim support | pandas only | xarray integration |
| Inconsistent outputs | Ad hoc formats | Three-DataFrame broom pattern |
| Commodity features underserved | Generic tools | Built-in spreads, seasonality |
| Manual validation | Ad hoc testing | Built-in walk-forward, IC |
| No config management | Script-based | Frozen dataclass specs |

---

## 10. py-tidymodels Integration

### 10.1 Architecture Alignment

```
py-tidymodels Ecosystem
├── py-hardhat (Blueprint/Mold/Forge)     ← SignalBlueprint extends
├── py-parsnip (ModelSpec/ModelFit)       ← fundamental_model source
│   ├── prophet_reg()
│   ├── arima_reg()
│   └── linear_reg()
├── py-workflows (Composition)            ← SignalWorkflow pattern
└── tidy-signal (NEW)
    ├── SignalSpec (extends ModelSpec pattern)
    ├── SignalFit (extends ModelFit pattern)
    └── Three-DataFrame outputs (consistent)
```

### 10.2 Integration Points

**py-parsnip → tidy-signal:**
```python
# Fundamental model from py-parsnip
from py_parsnip import prophet_reg

model = prophet_reg().fit(data, formula="price ~ inventory + demand + date")

# Use model predictions in tidy-signal
signal = (align(forwards, model.predict(features))
          .detect(signal_type='divergence'))
```

**Shared Patterns:**
1. **Frozen dataclass specs** - Immutable, serializable
2. **Registry pattern** - Engine discovery via decorators
3. **Three-DataFrame outputs** - outputs, coefficients, stats
4. **Dual-path architecture** - Standard vs raw data handling
5. **Method chaining** - Fluent interface

### 10.3 Data Structure Mapping

| py-tidymodels | tidy-signal Equivalent |
|---------------|------------------------|
| `Blueprint` | `SignalBlueprint` |
| `ModelSpec` | `SignalSpec` |
| `ModelFit` | `SignalFit` |
| `mold()` | `align()` |
| `forge()` | `apply_alignment()` |
| `extract_outputs()` | `extract_outputs()` |

---

## 11. Worked Example: Gas Oil Crack Spread

### 11.1 Problem Setup

**Scenario:**
- **Asset:** Gas Oil Crack Spread (Gas Oil - Brent Crude)
- **Forward:** $18/bbl for 3-month contract
- **Fundamental Model:** Prophet regression on inventory + demand
- **Fundamental Prediction:** $22/bbl
- **Divergence:** $4/bbl (Forward below Fundamental)
- **Days to Settlement:** 90

### 11.2 Implementation

```python
import tidy_signal as ts
from py_parsnip import prophet_reg

# Load data
forwards = ts.VintageDataFrame.from_csv('crack_spread_forwards.csv')
fundamentals = pd.read_csv('crack_spread_fundamentals.csv')

# Train fundamental model
model = (prophet_reg()
         .set_args(seasonality_mode='multiplicative')
         .fit(fundamentals, formula="spread ~ inventory + demand + date"))

# Create signal workflow
signal = (ts.align(forwards.latest(), model.predict(fundamentals))
          .detect(signal_type='divergence', standardize=True)
          .calibrate(convergence_model='ou_process')
          .diagnose(tests=['stationarity', 'cointegration'])
          .converge(analysis_type=['half_life', 'optimal_window'])
          .time_entry(entry_threshold=2.0, min_tenor=60)
          .time_exit(take_profit=0.85, stop_loss=1.8)
          .backtest(transaction_costs=0.002))

# Extract results
outputs, coefficients, stats = signal.extract_outputs()

# View key metrics
print(f"Half-life: {coefficients.loc['half_life', 'value']:.1f} days")
print(f"Sharpe Ratio: {stats.loc['sharpe_ratio', 'value']:.2f}")
print(f"Hit Rate: {stats.loc['hit_rate', 'value']:.1%}")
print(f"Max Drawdown: {stats.loc['max_drawdown', 'value']:.1%}")
```

### 11.3 Expected Results

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Half-life | ~22 days | Divergence decays 50% in 22 days |
| Sharpe Ratio | ~1.85 | Strong risk-adjusted returns |
| Hit Rate | ~68% | 68% of signals profitable |
| Max Drawdown | ~8.7% | Maximum peak-to-trough loss |
| Avg Holding | ~18 days | Average position duration |
| Profit Factor | ~2.1 | Gross profit 2.1× gross loss |

### 11.4 Cohort Analysis Output

```
Settlement: Jun-2025, Entry: Mar-2025 (90 days to settlement)

Date        Days  Forward  Fundamental  Divergence  Z-Score  Signal
2025-03-01   90    $18.00      $22.00       -$4.00    -2.3   ENTRY
2025-03-15   75    $18.50      $21.80       -$3.30    -1.9   HOLD
2025-04-01   60    $19.20      $21.50       -$2.30    -1.3   HOLD
2025-04-15   45    $19.80      $21.00       -$1.20    -0.7   HOLD
2025-05-01   30    $20.50      $20.80       -$0.30    -0.2   EXIT (TP)
2025-05-15   15    $20.80      $20.90       -$0.10    -0.1   FLAT
2025-06-01    0    $21.00      $21.00        $0.00     0.0   CONVERGED

Result: +$3.70/bbl profit (92.5% of initial divergence captured)
```

---

## 12. Implementation Roadmap

### Phase 1: Core Infrastructure (Weeks 1-2)
- [ ] SignalSpec, SignalFit, SignalBlueprint dataclasses
- [ ] VintageDataFrame xarray wrapper
- [ ] Registry pattern for signal engines
- [ ] `align()`, `slice()`, `detect()` verbs
- [ ] Unit tests for core components

### Phase 2: Statistical Arbitrage (Weeks 3-4)
- [ ] `calibrate()` with OU process, ECM
- [ ] `diagnose()` with stationarity, cointegration tests
- [ ] `converge()` with half-life, velocity analysis
- [ ] Cointegration detection (Johansen, Engle-Granger)
- [ ] Integration tests for calibration pipeline

### Phase 3: Validation Framework (Weeks 5-6)
- [ ] `evaluate()` with IC, Sharpe, hit rate
- [ ] `backtest()` with transaction costs
- [ ] `time_entry()`, `time_exit()` optimization
- [ ] Walk-forward analysis implementation
- [ ] Structural break detection

### Phase 4: Commodities Features (Weeks 7-8)
- [ ] Spread types (calendar, crack, crush)
- [ ] Seasonality handling (Fourier, STL)
- [ ] `monitor()`, `compare()`, `trace()` verbs
- [ ] Documentation and examples
- [ ] Tutorial notebooks

---

## 13. Dependencies

```
# Core
pandas>=2.0.0
numpy>=1.24.0
scipy>=1.10.0
xarray>=2023.0.0

# Statistical
statsmodels>=0.14.0
arch>=5.3.0

# ML (optional)
scikit-learn>=1.3.0
shap>=0.42.0

# py-tidymodels ecosystem
py-hardhat>=0.1.0
py-parsnip>=0.1.0
```

---

## 14. Key Literature References

### Academic Papers
- Wickham, H. (2014). "Tidy Data." *Journal of Statistical Software*
- Schwartz & Smith (2000). "Commodity price dynamics." *Management Science*
- Pardo, R. (1992). "Design, Testing and Optimization of Trading Systems"
- Engle & Granger (1987). "Co-integration and error correction." *Econometrica*

### Resources
- ALFRED Database (Federal Reserve vintage data methodology)
- Hudson & Thames (optimal stopping research)
- ML4Trading by Stefan Jansen
- alphalens documentation (Quantopian)

---

## 15. Success Metrics

### Technical Metrics
- [ ] 90%+ test coverage
- [ ] <100ms for cointegration test (100 pairs)
- [ ] <1s for OU fitting on 1000 observations
- [ ] <5s for walk-forward analysis (5 years daily data)

### API Quality Metrics
- [ ] All public functions have type hints
- [ ] All public functions have docstrings with examples
- [ ] 100% of core workflows demonstrated in tutorials
- [ ] Consistent with py-tidymodels patterns

### Adoption Metrics
- [ ] Integration with py-parsnip models
- [ ] Tutorial notebooks for common use cases
- [ ] Production deployment by pilot users

---

## Conclusion

`tidy-signal` addresses a clear gap in the Python ecosystem for commodities convergence trading. By combining:

1. **Tidyverse design philosophy** for readable, composable workflows
2. **Native vintage data handling** to prevent lookahead bias
3. **Convergence dynamics analysis** for optimal entry/exit timing
4. **Seamless py-tidymodels integration** for fundamental models
5. **Statistical rigor** with built-in validation tests
6. **Commodity-specific features** for real-world trading

The library provides unique value for quantitative researchers and commodity traders seeking to systematically exploit divergence between forward curves and fundamental fair values.

---

**Document Version:** 1.0
**Last Updated:** December 4, 2025
**Status:** Research Complete, Ready for Implementation
