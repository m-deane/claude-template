# tidy-signal: Minimum Viable Product (MVP) Specification

**Based on Research Findings - December 4, 2025**

---

## 1. MVP Scope Definition

### Core Philosophy
Bring R tidyverse/tidymodels "grammar of verbs" to commodities signal detection with:
- Consistent verb-based API
- Fluent method chaining
- Standardized three-DataFrame outputs
- Native vintage data support
- Comprehensive validation by default

### Target Users
1. **Quantitative researchers** - Testing statistical arbitrage strategies
2. **Commodity traders** - Developing signal-based trading systems
3. **Data scientists** - Analyzing time series with lookahead bias prevention

### MVP Feature Set
Focus on **statistical arbitrage for commodity spreads** as the killer use case:
- Cointegration testing
- Ornstein-Uhlenbeck process fitting
- Signal generation with optimal thresholds
- Walk-forward validation
- Standardized performance reporting

---

## 2. Architecture Design

### 2.1 Core Components

```
tidy_signal/
├── core/
│   ├── signal_spec.py          # SignalSpec frozen dataclass
│   ├── signal_fit.py           # SignalFit results container
│   ├── registry.py             # Engine registry pattern
│   └── outputs.py              # Three-DataFrame output standardization
├── data/
│   ├── vintage.py              # Vintage data handling
│   ├── structures.py           # xarray integration utilities
│   └── tidy.py                 # Tidy data conversion utilities
├── signals/
│   ├── mean_reversion.py       # Mean reversion signal specs
│   ├── cointegration.py        # Cointegration detection
│   └── ou_process.py           # Ornstein-Uhlenbeck modeling
├── engines/
│   ├── base.py                 # SignalEngine ABC
│   ├── statsmodels_engine.py  # Statsmodels implementations
│   └── sklearn_engine.py       # Scikit-learn implementations
├── validation/
│   ├── walk_forward.py         # Walk-forward analysis
│   ├── ic_analysis.py          # Information Coefficient
│   └── structural_breaks.py    # Regime change detection
├── commodities/
│   ├── spreads.py              # Calendar, crack, crush spreads
│   └── seasonality.py          # Seasonal decomposition
└── workflows/
    └── composition.py          # Multi-signal workflows
```

### 2.2 Data Structures

#### SignalSpec (Frozen Dataclass)
```python
from dataclasses import dataclass, field
from typing import Dict, Optional

@dataclass(frozen=True)
class SignalSpec:
    """Immutable signal specification following parsnip pattern"""
    signal_type: str              # 'mean_reversion', 'trend_following', etc.
    engine: str                   # 'statsmodels', 'sklearn', 'custom'
    mode: str                     # 'long_short', 'long_only', 'short_only'
    args: Dict = field(default_factory=dict)  # Hyperparameters
    metadata: Dict = field(default_factory=dict)  # Creation info

    def set_args(self, **kwargs):
        """Return new spec with updated args"""
        new_args = {**self.args, **kwargs}
        return dataclasses.replace(self, args=new_args)

    def set_mode(self, mode: str):
        """Return new spec with updated mode"""
        return dataclasses.replace(self, mode=mode)
```

#### SignalFit (Result Container)
```python
@dataclass
class SignalFit:
    """Container for fitted signal results"""
    spec: SignalSpec
    fit_data: Dict              # Engine-specific fitted parameters
    outputs_df: pd.DataFrame    # Per-observation results
    parameters_df: pd.DataFrame # Per-parameter statistics
    metrics_df: pd.DataFrame    # Per-signal summary metrics
    metadata: Dict              # Fit timestamp, data shape, etc.

    def predict(self, new_data, **kwargs):
        """Generate signals on new data"""
        engine = get_engine(self.spec.signal_type, self.spec.engine)
        return engine.predict(self, new_data, **kwargs)

    def validate(self, test_data, method='walk_forward', **kwargs):
        """Validate signal on test data"""
        from tidy_signal.validation import validate_signal
        return validate_signal(self, test_data, method=method, **kwargs)

    def tear_sheet(self, output_type='full'):
        """Generate comprehensive analysis tear sheet"""
        from tidy_signal.visualization import create_tear_sheet
        return create_tear_sheet(self, output_type=output_type)
```

#### VintageDataFrame (xarray wrapper)
```python
class VintageDataFrame:
    """Multi-dimensional data structure with vintage support"""

    def __init__(self, xr_dataset):
        self.ds = xr_dataset

    def as_of(self, vintage_date):
        """Filter to data available as of vintage_date"""
        return self.ds.sel(vintage_date=vintage_date, method='ffill')

    def latest(self):
        """Get most recent vintage"""
        return self.ds.isel(vintage_date=-1)

    def to_tidy(self):
        """Convert to long-format pandas DataFrame"""
        return self.ds.to_dataframe().reset_index()

    @classmethod
    def from_tidy(cls, df, dims=['vintage_date', 'date', 'tenor', 'contract']):
        """Create from long-format DataFrame"""
        ds = df.set_index(dims).to_xarray()
        return cls(ds)
```

### 2.3 Registry Pattern

```python
# In tidy_signal/core/registry.py

_SIGNAL_REGISTRY = {}

def register_engine(signal_type: str, engine: str):
    """Decorator for registering signal engines"""
    def decorator(cls):
        _SIGNAL_REGISTRY[(signal_type, engine)] = cls
        return cls
    return decorator

def get_engine(signal_type: str, engine: str):
    """Get engine instance from registry"""
    key = (signal_type, engine)
    if key not in _SIGNAL_REGISTRY:
        raise ValueError(f"Engine not found: {signal_type}/{engine}")
    return _SIGNAL_REGISTRY[key]()

def list_engines(signal_type: Optional[str] = None):
    """List available engines"""
    if signal_type:
        return [e for (s, e) in _SIGNAL_REGISTRY if s == signal_type]
    return list(_SIGNAL_REGISTRY.keys())
```

---

## 3. MVP User Workflows

### 3.1 Basic Pairs Trading Workflow

```python
import tidy_signal as ts
import pandas as pd

# Load data
prices = pd.read_csv('commodity_prices.csv', parse_dates=['date'])

# Step 1: Detect cointegrated pairs
pairs = ts.detect_cointegration(
    prices,
    contracts=['CL_M1', 'CL_M2', 'CL_M3'],
    method='johansen',
    threshold=0.05
)

# Step 2: Fit Ornstein-Uhlenbeck process to spread
signal_spec = ts.mean_reversion_signal(
    engine='ou_process',
    lookback=60,
    entry_threshold=2.0,
    exit_threshold=0.5
)

fit = signal_spec.fit(
    prices,
    pair=pairs.best_pair,
    formula='CL_M1 ~ CL_M2'
)

# Step 3: Generate signals
signals = fit.predict(prices)

# Step 4: Validate with walk-forward
validation = fit.validate(
    prices,
    method='walk_forward',
    train_window=252,
    test_window=63
)

# Step 5: View results
print(validation.metrics_df)
validation.tear_sheet()
```

### 3.2 Fluent Interface Workflow

```python
# Same workflow with method chaining
results = (prices
    .pipe(ts.detect_cointegration,
          contracts=['CL_M1', 'CL_M2', 'CL_M3'],
          method='johansen')
    .pipe(lambda df: ts.mean_reversion_signal(engine='ou_process')
          .fit(df, pair=df.best_pair, formula='CL_M1 ~ CL_M2'))
    .validate(method='walk_forward', train_window=252)
)

results.tear_sheet()
```

### 3.3 Calendar Spread Workflow

```python
# Load forward curve data
curves = ts.VintageDataFrame.from_tidy(
    pd.read_csv('forward_curves.csv'),
    dims=['vintage_date', 'date', 'tenor', 'contract']
)

# Calculate calendar spreads
spreads = ts.calculate_spreads(
    curves.as_of('2024-01-01'),
    spread_type='calendar',
    front='M1',
    back='M3'
)

# Detect anomalies
signal_spec = ts.mean_reversion_signal(
    engine='zscore',
    window=20,
    entry_threshold=2.0
)

fit = signal_spec.fit(spreads)
signals = fit.predict(spreads)

# Validate
validation = fit.validate(spreads, method='walk_forward')
validation.tear_sheet()
```

### 3.4 Multi-Signal Workflow

```python
# Combine multiple signals
workflow = (ts.SignalWorkflow()
    .add_signal(
        ts.mean_reversion_signal(engine='ou_process'),
        weight=0.5
    )
    .add_signal(
        ts.momentum_signal(engine='macd'),
        weight=0.3
    )
    .add_signal(
        ts.seasonality_signal(engine='fourier'),
        weight=0.2
    )
    .fit(train_data)
)

signals = workflow.predict(test_data)
validation = workflow.validate(test_data, method='walk_forward')
validation.tear_sheet()
```

---

## 4. Core API Reference

### 4.1 Signal Specification

```python
# Mean Reversion Signals
ts.mean_reversion_signal(
    engine='ou_process',      # 'ou_process', 'zscore', 'bollinger'
    lookback=60,
    entry_threshold=2.0,
    exit_threshold=0.5,
    mode='long_short'
)

# Trend Following Signals
ts.trend_following_signal(
    engine='macd',            # 'macd', 'moving_average', 'donchian'
    fast_period=12,
    slow_period=26,
    mode='long_only'
)

# Seasonality Signals
ts.seasonality_signal(
    engine='fourier',         # 'fourier', 'seasonal_decompose'
    periods=[12, 52],
    harmonics=3
)
```

### 4.2 Cointegration Detection

```python
ts.detect_cointegration(
    data,
    contracts=['CL_M1', 'CL_M2', 'CL_M3'],
    method='johansen',        # 'johansen', 'engle_granger'
    threshold=0.05,
    max_pairs=10,
    return_type='best'        # 'best', 'all', 'top_n'
)

# Returns:
# CointegrationResult with attributes:
#   .pairs: DataFrame of cointegrated pairs
#   .statistics: Test statistics
#   .best_pair: Top cointegrated pair
#   .hedge_ratios: Optimal weights
```

### 4.3 Validation Methods

```python
fit.validate(
    test_data,
    method='walk_forward',    # 'walk_forward', 'expanding', 'rolling'
    train_window=252,         # Training period
    test_window=63,           # Testing period
    step=21,                  # Step size for rolling
    metrics=['sharpe', 'ic', 'max_dd']
)

# Returns:
# ValidationResult with attributes:
#   .metrics_df: Per-window performance metrics
#   .signals_df: Generated signals with performance
#   .summary: Aggregated statistics
#   .tear_sheet(): Visualization method
```

### 4.4 Spread Calculations

```python
ts.calculate_spreads(
    data,
    spread_type='calendar',   # 'calendar', 'crack', 'crush', 'custom'
    front='M1',
    back='M3',
    weights=None              # For custom spreads
)

# Crack spread (3-2-1)
ts.calculate_crack_spread(
    crude_oil,
    gasoline,
    heating_oil,
    ratio='3-2-1'             # 3 barrels crude → 2 gas + 1 heating
)

# Crush spread
ts.calculate_crush_spread(
    soybeans,
    soy_meal,
    soy_oil
)
```

---

## 5. Output Standardization (Three-DataFrame Pattern)

### 5.1 Outputs DataFrame (Per-Observation)

```python
fit.outputs_df
```

| Column | Type | Description |
|--------|------|-------------|
| date | datetime | Observation date |
| contract | str | Contract identifier |
| signal_value | float | Raw signal value |
| signal_strength | float | Normalized signal strength (-1 to 1) |
| confidence | float | Signal confidence (0 to 1) |
| position | str | 'long', 'short', 'flat' |
| entry_price | float | Entry price (if position opened) |
| exit_price | float | Exit price (if position closed) |
| pnl | float | Realized P&L |
| split | str | 'train', 'test', 'validation' |

### 5.2 Parameters DataFrame (Per-Parameter)

```python
fit.parameters_df
```

| Column | Type | Description |
|--------|------|-------------|
| parameter_name | str | Parameter identifier |
| value | float | Estimated value |
| std_error | float | Standard error (if available) |
| t_statistic | float | t-statistic (if available) |
| p_value | float | p-value (if available) |
| ci_lower | float | Lower confidence interval |
| ci_upper | float | Upper confidence interval |

**Example for OU Process:**
- theta (mean reversion speed)
- mu (long-term mean)
- sigma (volatility)
- half_life (derived)

### 5.3 Metrics DataFrame (Per-Signal Summary)

```python
fit.metrics_df
```

| Metric | Description |
|--------|-------------|
| sharpe_ratio | Risk-adjusted return |
| information_ratio | IC mean / IC std |
| max_drawdown | Maximum peak-to-trough decline |
| calmar_ratio | Annual return / max drawdown |
| win_rate | Percentage of winning trades |
| profit_factor | Gross profit / gross loss |
| avg_trade_pnl | Average P&L per trade |
| turnover | Portfolio turnover rate |
| avg_holding_period | Average position duration |
| num_trades | Total number of trades |

---

## 6. Implementation Priorities

### Phase 1: Core Infrastructure (Week 1-2)

**Week 1:**
- [x] Set up package structure
- [ ] Implement SignalSpec frozen dataclass
- [ ] Implement SignalFit result container
- [ ] Create registry pattern
- [ ] Standardize three-DataFrame outputs

**Week 2:**
- [ ] VintageDataFrame wrapper for xarray
- [ ] Tidy data conversion utilities
- [ ] Basic SignalEngine ABC
- [ ] Unit tests for core components

### Phase 2: Statistical Arbitrage (Week 3-4)

**Week 3:**
- [ ] Cointegration detection (Johansen)
- [ ] Cointegration detection (Engle-Granger)
- [ ] Pairs selection utilities
- [ ] Tests for cointegration

**Week 4:**
- [ ] OU process parameter estimation
- [ ] OU process signal generation
- [ ] Optimal threshold calculation
- [ ] Tests for OU process

### Phase 3: Validation Framework (Week 5-6)

**Week 5:**
- [ ] Walk-forward analysis implementation
- [ ] Information Coefficient calculation
- [ ] Performance metrics (Sharpe, IC, drawdown)
- [ ] Tests for validation

**Week 6:**
- [ ] Structural break detection (Zivot-Andrews)
- [ ] Lookahead bias testing utilities
- [ ] Validation tear sheets
- [ ] Integration tests

### Phase 4: Commodities Features (Week 7-8)

**Week 7:**
- [ ] Calendar spread calculations
- [ ] Crack spread calculations
- [ ] Crush spread calculations
- [ ] Tests for spreads

**Week 8:**
- [ ] Seasonality modeling (Fourier)
- [ ] Seasonal decomposition
- [ ] Term structure utilities
- [ ] Documentation and examples

---

## 7. Testing Strategy

### 7.1 Unit Tests
- Test each component in isolation
- Mock external dependencies (statsmodels, sklearn)
- Cover edge cases (missing data, single observations, etc.)
- Target: 90%+ code coverage

### 7.2 Integration Tests
- Test end-to-end workflows
- Use synthetic data with known properties
- Verify outputs match expected statistical properties
- Test against reference implementations (statsmodels)

### 7.3 Benchmark Tests
- Compare cointegration tests vs statsmodels
- Compare OU fitting vs known analytical solutions
- Performance benchmarks (speed, memory)
- Reproduce results from academic papers

### 7.4 Example Data
- Synthetic cointegrated pairs (known properties)
- Historical commodity data (oil, gold, corn)
- Forward curve data with term structure
- Data with known lookahead bias (for testing)

---

## 8. Documentation Plan

### 8.1 API Documentation (Sphinx)
- Auto-generated from docstrings
- Type hints throughout
- Usage examples in docstrings
- Cross-references between components

### 8.2 Tutorial Notebooks
1. **Getting Started** - Basic signal workflow
2. **Pairs Trading** - Cointegration → OU → signals
3. **Calendar Spreads** - Forward curve analysis
4. **Validation** - Walk-forward and IC analysis
5. **Multi-Signal Workflows** - Combining signals

### 8.3 Conceptual Guides
- **Tidy Data Principles** - Why long format?
- **Vintage Data** - Preventing lookahead bias
- **Statistical Arbitrage Theory** - OU process, cointegration
- **Validation Best Practices** - Walk-forward, IC

### 8.4 Reference Papers
- Maintain bibliography of key papers
- Provide implementation notes
- Document any deviations from literature

---

## 9. Success Metrics

### Technical Metrics
- [ ] 90%+ test coverage
- [ ] <100ms for cointegration test (100 pairs)
- [ ] <1s for OU fitting on 1000 observations
- [ ] <5s for walk-forward analysis (5 years daily data)

### API Quality Metrics
- [ ] All public functions have type hints
- [ ] All public functions have docstrings with examples
- [ ] 100% of core workflows demonstrated in tutorials
- [ ] Zero breaking changes after 1.0 release

### Adoption Metrics
- [ ] 100+ GitHub stars in first 3 months
- [ ] 10+ community contributions
- [ ] 5+ blog posts/tutorials from community
- [ ] Used in production by 3+ organizations

---

## 10. Risk Mitigation

### Technical Risks

| Risk | Mitigation |
|------|------------|
| Performance bottlenecks | Profile early, use Numba/Cython where needed |
| xarray learning curve | Provide high-level wrappers, hide complexity |
| Statsmodels API changes | Pin versions, integration tests alert to breaks |
| Memory issues with large datasets | Support chunked/lazy evaluation via xarray |

### Adoption Risks

| Risk | Mitigation |
|------|------------|
| Complex API scares users | Provide simple "happy path" with sensible defaults |
| Documentation gaps | Write tutorials first, then API |
| Lack of examples | Reproduce 5+ papers as worked examples |
| Competition from existing tools | Focus on unique value: vintage data + commodities |

### Maintenance Risks

| Risk | Mitigation |
|------|------------|
| Lone maintainer burnout | Build contributor community early |
| Dependency hell | Minimize dependencies, pin versions carefully |
| Breaking changes in dependencies | Comprehensive integration tests |
| Feature creep | Maintain strict MVP scope, defer Phase 5 features |

---

## 11. Post-MVP Roadmap

### Phase 5: Workflow Composition (Future)
- Multi-signal combination strategies
- Pipeline optimization
- Production deployment tools
- Real-time signal generation

### Phase 6: Machine Learning Integration (Future)
- Scikit-learn pipeline integration
- Feature engineering for ML signals
- Neural network signal engines
- AutoML for signal optimization

### Phase 7: Visualization & Dashboards (Future)
- Interactive Plotly dashboards
- Real-time signal monitoring
- Performance attribution analysis
- Risk dashboard

---

## 12. Getting Started Checklist

### Environment Setup
- [ ] Create virtual environment: `python -m venv venv`
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Install dev dependencies: `pip install -r requirements-dev.txt`
- [ ] Install pre-commit hooks: `pre-commit install`

### Development Workflow
- [ ] Create feature branch: `git checkout -b feature/signal-spec`
- [ ] Write failing test first (TDD)
- [ ] Implement feature
- [ ] Run tests: `pytest tests/`
- [ ] Check coverage: `pytest --cov=tidy_signal`
- [ ] Format code: `black tidy_signal/`
- [ ] Type check: `mypy tidy_signal/`
- [ ] Commit and push

### Key Dependencies (requirements.txt)
```
# Core
pandas>=2.0.0
numpy>=1.24.0
xarray>=2023.1.0

# Statistical
statsmodels>=0.14.0
scipy>=1.10.0

# Optional ML
scikit-learn>=1.3.0  # For sklearn engines

# Visualization
matplotlib>=3.7.0
plotly>=5.14.0

# Development
pytest>=7.3.0
pytest-cov>=4.1.0
black>=23.3.0
mypy>=1.3.0
sphinx>=6.2.0
```

---

**End of MVP Specification**

This specification provides a concrete, actionable plan to build tidy-signal based on the comprehensive research findings. The focus is on delivering immediate value (statistical arbitrage for commodities) while establishing architectural patterns that support future expansion.
