# tidy-signal Feasibility Study

## Executive Summary

**Verdict: HIGHLY VIABLE**

`tidy-signal` fills a clear gap by uniquely combining tidyverse design patterns, native vintage data support, commodity-specific features, and rigorous validation workflows for testing divergence between forward curves and fundamental model predictions.

---

## Research Findings

### 1. Prior Art Analysis

| Library | Key Innovation | Lesson for tidy-signal |
|---------|----------------|------------------------|
| **Zipline** (17k+ stars) | Pipeline API separates factors from execution | Modular signal architecture |
| **VectorBT** (4k+ stars) | Vectorized operations (thousands of strategies/second) | Boolean signal arrays + fluent API |
| **Backtrader** (13k+ stars) | Comprehensive signal taxonomy | Entry/exit signal types |
| **Alphalens** (3k+ stars) | Information Coefficient analysis | IC as validation metric |
| **Pyfolio** (5.5k+ stars) | Performance tear sheets | Three-DataFrame output |
| **Empyrical** (1.2k+ stars) | Pure functional metrics | Separate calculation from analysis |

### 2. Gap Analysis - What tidy-signal Uniquely Provides

1. **No unified grammar for signals** → Tidyverse verb API
2. **Fragmented stat arb tools** → Integrated cointegration → OU → signals pipeline
3. **No vintage data support** → First-class `vintage_date` dimension (prevent lookahead bias)
4. **Limited multi-dim support** → xarray integration for tenor × vintage × time
5. **Inconsistent outputs** → Three-DataFrame broom pattern
6. **Commodity features underserved** → Built-in spreads, seasonality, term structure
7. **Manual validation** → Built-in walk-forward, IC, structural breaks
8. **No config management** → Frozen dataclass specs with serialization

### 3. Statistical Methods (Ranked by Priority)

| Rank | Method | Priority | Use Case |
|------|--------|----------|----------|
| 1 | Cointegration (Johansen & Engle-Granger) | **Critical** | Pairs selection |
| 2 | Stationarity (ADF + KPSS) | **Critical** | Mean reversion validation |
| 3 | Walk-Forward Analysis | **Critical** | Out-of-sample validation |
| 4 | Structural Break Detection (Zivot-Andrews) | **High** | Regime changes |
| 5 | OU Parameter Estimation | **High** | Optimal entry/exit thresholds |

---

## Proposed Verb Grammar

### Data Preparation
- `align()` - Match vintages and tenors across data sources
- `slice()` - Extract specific vintage/tenor combinations

### Signal Construction
- `detect()` - Compute divergence between forward and fundamental
- `decompose()` - Break spread into trend, seasonal, residual

### Calibration
- `calibrate()` - Fit convergence model (OU process, ECM, threshold)
- `diagnose()` - Run statistical validity tests

### Evaluation
- `evaluate()` - Score signal strength and confidence
- `converge()` - Analyze convergence dynamics (half-life, velocity)

### Trading Rules
- `time_entry()` - Determine optimal entry timing
- `time_exit()` - Determine optimal exit timing
- `backtest()` - Historical performance evaluation

### Monitoring
- `monitor()` - Track relationship stability over time
- `compare()` - Compare signals across models/tenors
- `trace()` - Generate full audit trail

---

## Core Data Structures

### SignalSpec (Immutable Specification)
```python
@dataclass(frozen=True)
class SignalSpec:
    signal_type: str  # "divergence", "ratio", "spread"
    forward_source: Dict[str, Any]
    fundamental_model: ModelFit  # From py-parsnip
    alignment_rules: Dict[str, Any]
    convergence_model: str = "ou_process"
    standardize: bool = True
    args: Dict[str, Any] = None
```

### SignalFit (Calibrated Relationship)
```python
@dataclass(frozen=True)
class SignalFit:
    spec: SignalSpec
    calibration_data: Dict[str, Any]
    convergence_params: Dict[str, float]  # half_life, lambda, mu, sigma
    entry_rules: Dict[str, Any]
    exit_rules: Dict[str, Any]
    blueprint: SignalBlueprint
    evaluation_data: Dict[str, Any] = None
```

### Three-DataFrame Output Pattern

**outputs** (observation-level):
- divergence, forward_value, fundamental_value
- signal_strength, entry_signal, exit_signal
- convergence_velocity, confidence, p_value

**coefficients** (relationship parameters):
- mean_reversion_speed (λ), long_run_mean (μ), volatility (σ)
- half_life, feature importances, hedge ratios

**stats** (signal-level metrics):
- hit_rate, sharpe_ratio, information_coefficient
- max_drawdown, profit_factor, avg_holding_period

---

## Convergence Analysis Framework

### Core Metrics
- **Half-life**: Days for divergence to decay by 50%
- **Mean reversion speed (λ)**: From OU process dD = -λ(D - μ)dt + σdW
- **Long-run mean (μ)**: Equilibrium divergence level
- **Convergence velocity**: Current dD/dt

### Entry/Exit Optimization
- Optimal entry window based on historical Sharpe by tenor
- Take-profit at X% convergence
- Stop-loss at Y× divergence expansion
- Time decay exit after N× half-life

---

## py-tidymodels Integration

### py-parsnip (Model Interface)
- `SignalSpec.fundamental_model` accepts any `ModelFit`
- Supports prophet_reg, arima_reg, linear_reg, rand_forest
- Uses `extract_outputs()` three-DataFrame pattern

### py-hardhat (Preprocessing)
- Can leverage `Blueprint` for feature engineering
- `SignalBlueprint` extends for vintage/tenor alignment

### py-rsample (Future)
- Time series CV for signal calibration
- `rolling_origin()` for walk-forward validation

### py-workflows (Future)
- Compose: align → detect → calibrate → converge → time_entry → backtest

---

## Example Use Case: Gas Oil Crack Spread

**Scenario**:
- Forward: $18/bbl (3-month)
- Fundamental (Prophet): $22/bbl
- Divergence: $4/bbl
- Time to settlement: 90 days

**Workflow**:
```python
# Train fundamental model
model = prophet_reg().fit(data, formula="price ~ inventory + demand + date")

# Create signal
signal = (align(forwards, model.predict(data))
          .detect(signal_type="divergence", standardize=True)
          .calibrate(convergence_model="ou_process")
          .diagnose(tests=["stationarity", "cointegration"])
          .converge(analysis_type=["half_life", "optimal_window"])
          .time_entry(entry_threshold=2.0, min_tenor=60)
          .time_exit(take_profit=0.85, stop_loss=1.8)
          .backtest(transaction_costs=0.002))

# Extract results
outputs, coefficients, stats = signal.extract_outputs()
```

**Expected Results**:
- Half-life: ~22 days
- Sharpe ratio: ~1.85
- Hit rate: ~68%
- Max drawdown: ~8.7%

---

## Implementation Roadmap

### Phase 1: Core Infrastructure (Weeks 1-2)
- SignalSpec, SignalFit, SignalBlueprint dataclasses
- align(), slice(), detect() verbs
- AlignedSignalData multi-dimensional structure

### Phase 2: Statistical Arbitrage (Weeks 3-4)
- calibrate() with OU process, ECM
- diagnose() with stationarity, cointegration tests
- converge() with half-life, velocity analysis

### Phase 3: Validation Framework (Weeks 5-6)
- evaluate() with IC, Sharpe, hit rate
- backtest() with transaction costs
- time_entry(), time_exit() optimization

### Phase 4: Commodities Features (Weeks 7-8)
- Spread types (calendar, crack, crush)
- Seasonality handling
- monitor(), compare(), trace() verbs
- Documentation and examples

---

## Dependencies

```
pandas>=2.0.0
numpy>=1.24.0
scipy>=1.10.0
statsmodels>=0.14.0
scikit-learn>=1.3.0
xarray>=2023.0.0  # Multi-dimensional data
shap>=0.42.0      # Feature importance
arch>=5.3.0       # Phillips-Perron test

# py-tidymodels ecosystem
py-hardhat>=0.1.0
py-parsnip>=0.1.0
```

---

## Key Literature References

**Academic**:
- Wickham, H. (2014). "Tidy Data." Journal of Statistical Software
- Schwartz & Smith (2000). "Commodity price dynamics." Management Science
- Pardo, R. (1992). "Design, Testing and Optimization of Trading Systems"

**Resources**:
- ALFRED Database (Federal Reserve vintage data methodology)
- Hudson & Thames (optimal stopping research)
- ML4Trading by Stefan Jansen

---

## Conclusion

`tidy-signal` is highly viable and addresses a clear gap in the Python ecosystem for:

1. **Tidyverse-style API** for signal detection
2. **Vintage-aware data handling** for point-in-time backtesting
3. **Convergence dynamics analysis** for optimal entry/exit timing
4. **Seamless py-tidymodels integration** for fundamental models
5. **Statistical rigor** with built-in validation tests

The library would provide a unique value proposition by combining the elegance of tidymodels with the specific requirements of commodities convergence trading.
