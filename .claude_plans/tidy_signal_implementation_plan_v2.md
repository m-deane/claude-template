# tidy-signal: Implementation Plan v2

**Version:** 2.0 | **Date:** December 7, 2025 | **Status:** Implementation Ready

---

## Changes from v1

### Removed (py-tidymodels specific patterns)
| Item | Reason |
|------|--------|
| `py-tidymodels2` virtual environment | tidy-signal is a separate library with its own environment |
| "from py-parsnip ModelSpec" framing | These are general Python patterns, not py-parsnip specific |
| Rigid Three-DataFrame column requirements | Use scoping document's schema instead |
| "Consistent with py-tidymodels" goal | Goal is "integrates with", not "mirrors" |
| ChromaDB integration section | Out of scope for MVP, can be added later |

### Kept (general best practices)
| Practice | Rationale |
|----------|-----------|
| Frozen dataclasses | Standard Python immutability pattern |
| Registry pattern | Standard plugin architecture |
| 90%+ test coverage | Good quality standard |
| Type hints + docstrings | Good Python practice |
| No placeholder implementations | Good development discipline |
| Tests after checkpoints | Good workflow |

### Modified
| Item | v1 | v2 |
|------|----|----|
| Virtual environment | `py-tidymodels2` | `tidy-signal-env` |
| Output schema | Invented rigid columns | Scoping document Section 4.4 |
| SignalBlueprint | Partial definition | Full scoping document Section 4.3 |
| Integration goal | "Mirror py-parsnip" | "Integrate with py-parsnip" |

---

## 1. Source of Truth

**This implementation plan derives entirely from:**
- `.claude_plans/tidy_signal_scoping_document.md` (v1.1)

The scoping document defines all data structures, verbs, output formats, and architecture. This plan operationalizes that specification.

---

## 2. Development Environment

### 2.1 Virtual Environment Setup

```bash
# Create tidy-signal specific environment
python -m venv tidy-signal-env
source tidy-signal-env/bin/activate

# Install core dependencies
pip install pandas numpy scipy xarray statsmodels

# Install development dependencies
pip install pytest pytest-cov black mypy sphinx

# Install in editable mode
pip install -e .
```

### 2.2 Project Structure

```
tidy-signal/                    # Root directory (separate from py-tidymodels)
├── tidy_signal/               # Main package
│   ├── __init__.py
│   ├── exceptions.py
│   ├── core/
│   │   ├── signal_spec.py     # SignalSpec (scoping doc Section 4.1)
│   │   ├── signal_fit.py      # SignalFit (scoping doc Section 4.2)
│   │   ├── signal_blueprint.py # SignalBlueprint (scoping doc Section 4.3)
│   │   ├── registry.py
│   │   └── outputs.py         # Three-DataFrame (scoping doc Section 4.4)
│   ├── data/
│   │   ├── vintage.py         # VintageDataFrame (scoping doc Section 2.3)
│   │   ├── alignment.py       # xarray alignment (scoping doc Section 2.4)
│   │   └── structures.py      # AlignedSignalData
│   ├── verbs/                 # Verb API (scoping doc Section 3)
│   │   ├── align.py
│   │   ├── detect.py
│   │   ├── calibrate.py
│   │   ├── diagnose.py
│   │   ├── converge.py
│   │   ├── time_entry.py
│   │   ├── time_exit.py
│   │   └── backtest.py
│   ├── engines/
│   │   ├── base.py
│   │   ├── ou_process.py      # OU Process (scoping doc Section 5)
│   │   ├── zscore.py
│   │   └── ecm.py
│   ├── statistical/
│   │   ├── cointegration.py   # (scoping doc Section 6.1)
│   │   ├── stationarity.py    # (scoping doc Section 6.4)
│   │   └── ou_fitting.py      # MLE (scoping doc Section 5.2)
│   ├── validation/
│   │   ├── walk_forward.py
│   │   ├── metrics.py
│   │   └── ic_analysis.py
│   └── commodities/
│       ├── spreads.py
│       └── seasonality.py
├── tests/
│   └── test_tidy_signal/
├── examples/
├── docs/
├── setup.py
├── pyproject.toml
└── requirements.txt
```

---

## 3. Coding Standards (General Best Practices)

### 3.1 Frozen Dataclasses for Immutability

Immutable specifications prevent side effects and enable safe reuse:

```python
from dataclasses import dataclass, field, replace
from typing import Dict, Any

@dataclass(frozen=True)
class SignalSpec:
    """Immutable signal specification"""
    signal_type: str
    engine: str
    mode: str = "long_short"
    args: Dict[str, Any] = field(default_factory=dict)

    def set_args(self, **kwargs) -> 'SignalSpec':
        """Return NEW spec with updated args"""
        return replace(self, args={**self.args, **kwargs})
```

### 3.2 Registry Pattern for Extensibility

Decorator-based engine discovery:

```python
_ENGINE_REGISTRY = {}

def register_engine(signal_type: str, engine_name: str):
    def decorator(cls):
        _ENGINE_REGISTRY[(signal_type, engine_name)] = cls
        return cls
    return decorator

def get_engine(signal_type: str, engine_name: str):
    key = (signal_type, engine_name)
    if key not in _ENGINE_REGISTRY:
        raise SignalEngineError(f"Engine not found: {signal_type}/{engine_name}")
    return _ENGINE_REGISTRY[key]()
```

### 3.3 Testing Standards

- Tests after every checkpoint
- 90%+ code coverage
- No mock data - use synthetic data with known properties
- Integration tests for py-parsnip compatibility

```bash
# Run tests
source tidy-signal-env/bin/activate
python -m pytest tests/ -v --cov=tidy_signal --cov-report=html
```

### 3.4 Code Quality

- Type hints on all public functions
- Docstrings with examples on all public functions
- No placeholder implementations (`pass`, `TODO`, etc.)

---

## 4. Data Structures (from Scoping Document)

### 4.1 SignalSpec (Scoping Doc Section 4.1)

```python
@dataclass(frozen=True)
class SignalSpec:
    """Immutable signal specification"""
    signal_type: str                    # "divergence", "ratio", "spread"
    forward_source: Dict[str, Any]      # Forward curve data config
    fundamental_model: Any              # py-parsnip ModelFit (optional)
    alignment_rules: Dict[str, Any]     # Vintage/tenor alignment
    convergence_model: str = "ou_process"
    standardize: bool = True
    args: Dict[str, Any] = field(default_factory=dict)
```

### 4.2 SignalFit (Scoping Doc Section 4.2)

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
```

### 4.3 SignalBlueprint (Scoping Doc Section 4.3)

```python
@dataclass
class SignalBlueprint:
    """Alignment metadata for consistent transformations"""
    # Core alignment rules
    forward_columns: List[str]
    fundamental_columns: List[str]
    alignment_key: str                      # 'observation_date'
    vintage_handling: str                   # 'as_of', 'latest', 'exact'

    # Coordinate specifications
    vintage_coords: Optional[pd.DatetimeIndex] = None
    observation_coords: Optional[pd.DatetimeIndex] = None
    tenor_coords: Optional[List[str]] = None
    contract_coords: Optional[List[str]] = None

    # Data type enforcement
    column_dtypes: Dict[str, str] = field(default_factory=dict)

    # Alignment behavior
    missing_data_strategy: str = 'ffill'
    max_staleness_days: int = 5
    coordinate_tolerance: Optional[str] = None

    # Calibration metadata
    calibration_vintage: Optional[str] = None
    calibration_date_range: Optional[tuple] = None
    standardization_params: Dict[str, float] = field(default_factory=dict)

    def validate_new_data(self, new_data) -> bool:
        """Validate new data conforms to blueprint"""
        ...

    def apply_alignment(self, forward_data, fundamental_data) -> 'AlignedSignalData':
        """Apply blueprint rules (forge equivalent)"""
        ...
```

### 4.4 Three-DataFrame Output (Scoping Doc Section 4.4)

**Outputs DataFrame (observation-level):**

| Column | Type | Description |
|--------|------|-------------|
| `date` | datetime | Observation date |
| `contract` | str | Contract identifier |
| `days_to_settlement` | int | Days until settlement |
| `forward_value` | float | Forward curve price |
| `fundamental_value` | float | Model prediction |
| `divergence` | float | forward - fundamental |
| `divergence_zscore` | float | Standardized divergence |
| `signal_strength` | float | Normalized (-1 to 1) |
| `entry_signal` | bool | Entry triggered |
| `exit_signal` | bool | Exit triggered |
| `convergence_velocity` | float | Rate of change |
| `confidence` | float | 0 to 1 |
| `p_value` | float | Statistical significance |
| `split` | str | 'train', 'test', 'validation' |

**Coefficients DataFrame (relationship parameters):**

| Column | Type | Description |
|--------|------|-------------|
| `parameter_name` | str | Parameter identifier |
| `value` | float | Estimated value |
| `std_error` | float | Standard error |
| `t_statistic` | float | t-statistic |
| `p_value` | float | Significance level |
| `ci_lower` | float | Lower CI |
| `ci_upper` | float | Upper CI |

**Key parameters:** `mean_reversion_speed` (λ), `long_run_mean` (μ), `volatility` (σ), `half_life`, `hedge_ratio`

**Stats DataFrame (signal-level metrics):**

| Metric | Description |
|--------|-------------|
| `hit_rate` | % winning signals |
| `sharpe_ratio` | Risk-adjusted return |
| `information_coefficient` | Correlation with forward returns |
| `max_drawdown` | Maximum peak-to-trough |
| `profit_factor` | Gross profit / gross loss |
| `avg_holding_period` | Average days in position |
| `turnover` | Portfolio turnover rate |
| `num_signals` | Total signals generated |

---

## 5. Phase 1: Core Infrastructure (Weeks 1-2)

### Day 1: Exceptions and SignalSpec

**Files:**
- `tidy_signal/exceptions.py`
- `tidy_signal/core/signal_spec.py`
- `tests/test_tidy_signal/test_core/test_signal_spec.py`

**exceptions.py:**
```python
class SignalError(Exception):
    """Base exception for tidy-signal"""
    pass

class SignalAlignmentError(SignalError):
    """Data alignment failed"""
    pass

class SignalEngineError(SignalError):
    """Engine operation failed"""
    pass

class SignalValidationError(SignalError):
    """Validation failed"""
    pass

class VintageDataError(SignalError):
    """Vintage data operation failed"""
    pass
```

**Acceptance criteria:**
- [ ] SignalSpec is frozen (immutable)
- [ ] set_args() returns new instance
- [ ] JSON serialization works
- [ ] All tests pass

### Day 2: Registry Pattern

**Files:**
- `tidy_signal/core/registry.py`
- `tests/test_tidy_signal/test_core/test_registry.py`

**Acceptance criteria:**
- [ ] Decorator registration works
- [ ] Duplicate registration raises error
- [ ] get_engine() provides helpful error messages
- [ ] list_engines() works with/without filtering

### Day 3: SignalEngine ABC and Outputs

**Files:**
- `tidy_signal/engines/base.py`
- `tidy_signal/core/outputs.py`
- `tests/test_tidy_signal/test_engines/test_base.py`
- `tests/test_tidy_signal/test_core/test_outputs.py`

**Acceptance criteria:**
- [ ] SignalEngine ABC enforces fit/predict/extract_outputs
- [ ] Output validation uses scoping document schema
- [ ] translate_params() works

### Day 4: SignalFit Container

**Files:**
- `tidy_signal/core/signal_fit.py`
- `tests/test_tidy_signal/test_core/test_signal_fit.py`

**Acceptance criteria:**
- [ ] Stores spec, calibration_data, convergence_params
- [ ] predict() delegates to engine
- [ ] extract_outputs() returns three DataFrames

### Days 5-6: VintageDataFrame

**Files:**
- `tidy_signal/data/vintage.py`
- `tests/test_tidy_signal/test_data/test_vintage.py`

**Implementation per scoping doc Section 2.3:**
```python
class VintageDataFrame:
    """Multi-dimensional data with vintage support"""

    def __init__(self, xr_dataset):
        self.ds = xr_dataset

    def as_of(self, vintage_date):
        """Data available as of vintage_date (forward-fill)"""
        return self.ds.sel(vintage_date=vintage_date, method='ffill')

    def latest(self):
        """Most recent vintage"""
        return self.ds.isel(vintage_date=-1)

    def to_cohort(self, settlement_date):
        """Extract single cohort"""
        return self.ds.sel(contract=settlement_date)
```

**Acceptance criteria:**
- [ ] as_of() forward-fills correctly
- [ ] latest() returns most recent
- [ ] Prevents lookahead bias
- [ ] to_tidy()/from_tidy() round-trip

### Days 7-8: SignalBlueprint

**Files:**
- `tidy_signal/core/signal_blueprint.py`
- `tests/test_tidy_signal/test_core/test_signal_blueprint.py`

**Implementation per scoping doc Section 4.3 (full class above)**

**Acceptance criteria:**
- [ ] validate_new_data() catches schema mismatches
- [ ] apply_alignment() applies vintage selection
- [ ] Stores all calibration metadata

### Day 9: AlignedSignalData

**Files:**
- `tidy_signal/data/structures.py`
- `tests/test_tidy_signal/test_data/test_structures.py`

```python
@dataclass
class AlignedSignalData:
    """Container for aligned forward and fundamental data"""
    forward: xr.DataArray
    fundamental: xr.DataArray
    blueprint: SignalBlueprint

    def compute_divergence(self, standardize: bool = True) -> xr.DataArray:
        """Compute divergence between forward and fundamental"""
        divergence = self.forward - self.fundamental
        if standardize and self.blueprint.standardization_params:
            mean = self.blueprint.standardization_params.get('mean', 0)
            std = self.blueprint.standardization_params.get('std', 1)
            divergence = (divergence - mean) / std
        return divergence
```

### Day 10: align() Verb

**Files:**
- `tidy_signal/verbs/align.py`
- `tidy_signal/data/alignment.py`
- `tests/test_tidy_signal/test_verbs/test_align.py`

**Implementation per scoping doc Section 2.4:**
```python
def align(
    forward_data: Union[xr.Dataset, VintageDataFrame],
    fundamental_data: Union[pd.DataFrame, xr.DataArray],
    by: str = 'observation_date',
    how: Literal['inner', 'outer', 'left', 'right'] = 'inner',
    vintage_mode: Literal['as_of', 'latest', 'exact'] = 'latest',
    vintage_date: Optional[str] = None,
    tolerance: Optional[str] = None,
    missing_strategy: Literal['ffill', 'bfill', 'interpolate', 'drop'] = 'ffill',
    max_gap: Optional[int] = 5
) -> AlignedSignalData:
    ...
```

**Acceptance criteria:**
- [ ] All vintage_mode options work
- [ ] Coordinate dtype harmonization
- [ ] Ragged-edge handling
- [ ] Returns AlignedSignalData with blueprint

---

## 6. Phase 2: Statistical Arbitrage (Weeks 3-4)

### Days 11-12: Stationarity Testing

**Files:**
- `tidy_signal/statistical/stationarity.py`
- `tests/test_tidy_signal/test_statistical/test_stationarity.py`

**Implementation per scoping doc Section 6.4:**
```python
def test_stationarity(series, significance=0.05):
    """Combined ADF + KPSS testing"""
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

### Days 13-14: Cointegration Detection

**Files:**
- `tidy_signal/statistical/cointegration.py`
- `tests/test_tidy_signal/test_statistical/test_cointegration.py`

**Per scoping doc Section 6.1:**
- Johansen test via `statsmodels.tsa.vector_ar.vecm.coint_johansen()`
- Engle-Granger via `statsmodels.tsa.stattools.coint()`

### Days 15-17: OU Process MLE Fitting

**Files:**
- `tidy_signal/statistical/ou_fitting.py`
- `tests/test_tidy_signal/test_statistical/test_ou_fitting.py`

**Implementation per scoping doc Section 5.2:**
```python
def fit_ou_process_mle(divergence_series: np.ndarray, dt: float = 1.0) -> dict:
    """
    Fit OU process via Maximum Likelihood Estimation.

    Returns:
        lambda_: Mean reversion speed
        mu: Long-run mean
        sigma: Volatility
        half_life: ln(2) / lambda_
        std_errors: Parameter standard errors
        log_likelihood, aic, bic
    """
    # Exact discrete MLE implementation from scoping doc
    ...
```

### Days 18-20: OUProcessEngine

**Files:**
- `tidy_signal/engines/ou_process.py`
- `tests/test_tidy_signal/test_engines/test_ou_process.py`

```python
@register_engine('mean_reversion', 'ou_process')
class OUProcessEngine(SignalEngine):
    param_map = {
        'entry_threshold': 'entry_zscore',
        'exit_threshold': 'exit_zscore',
    }

    def fit(self, spec, aligned_data):
        ...

    def predict(self, fit_data, new_data):
        ...

    def extract_outputs(self, fit_data):
        # Returns three DataFrames per scoping doc Section 4.4
        ...
```

---

## 7. Phase 3: Validation Framework (Weeks 5-6)

### Days 21-22: Performance Metrics

**Files:**
- `tidy_signal/validation/metrics.py`

Implement: `sharpe_ratio`, `information_coefficient`, `max_drawdown`, `hit_rate`, `profit_factor`

### Days 23-25: Walk-Forward Analysis

**Files:**
- `tidy_signal/validation/walk_forward.py`

### Days 26-28: backtest() Verb

**Files:**
- `tidy_signal/verbs/backtest.py`

---

## 8. Phase 4: Commodities & Additional Verbs (Weeks 7-8)

### Days 29-36: Remaining Verbs

- `detect()` - compute divergence
- `calibrate()` - fit convergence model
- `diagnose()` - statistical tests
- `converge()` - convergence dynamics
- `time_entry()`, `time_exit()` - entry/exit optimization

### Days 37-42: Commodity Features

- Calendar spreads
- Crack spreads
- Crush spreads
- Seasonal decomposition

---

## 9. Phase 5: Integration & Polish (Weeks 9-12)

### py-parsnip Integration

**Goal:** tidy-signal **integrates with** py-parsnip (not mirrors it)

```python
# Integration point: ModelFit.predict() output → align()
from py_parsnip import prophet_reg

model = prophet_reg().fit(data, formula="price ~ inventory + demand + date")
predictions = model.predict(features)  # Returns DataFrame

# tidy-signal accepts this DataFrame
signal = (align(forwards, predictions)  # predictions is pd.DataFrame
          .detect(signal_type='divergence')
          .calibrate(model='ou_process')
          .backtest())
```

**Integration tests verify:**
- [ ] ModelFit.predict() output compatible with align()
- [ ] Different model types work (prophet, arima, linear)
- [ ] No data leakage across splits

---

## 10. Quality Gates

### Phase 1 Gate (End Week 2)

- [ ] All core dataclasses implemented
- [ ] VintageDataFrame prevents lookahead bias
- [ ] align() handles all edge cases
- [ ] 90%+ test coverage for Phase 1 code
- [ ] Type hints and docstrings complete

### Phase 2 Gate (End Week 4)

- [ ] OU fitting matches reference implementations
- [ ] Cointegration tests match statsmodels
- [ ] OUProcessEngine returns valid three DataFrames
- [ ] Performance: OU fitting < 1s for 1000 obs

### Phase 3 Gate (End Week 6)

- [ ] Walk-forward analysis working
- [ ] backtest() returns valid outputs
- [ ] No lookahead bias in backtests
- [ ] Performance: walk-forward < 5s for 5 years daily

### Phase 4 Gate (End Week 8)

- [ ] All verbs chain in fluent interface
- [ ] Commodity spreads working
- [ ] Tutorial notebooks run without errors

### Phase 5 Gate (End Week 12 - MVP Release)

- [ ] 90%+ test coverage overall
- [ ] py-parsnip integration tests pass
- [ ] Documentation complete
- [ ] v1.0 release ready

---

## 11. Test Strategy

### Unit Tests

Each module has comprehensive tests:
- `test_core/` - SignalSpec, SignalFit, SignalBlueprint, registry
- `test_data/` - VintageDataFrame, alignment, structures
- `test_verbs/` - Each verb
- `test_engines/` - Each engine
- `test_statistical/` - Cointegration, stationarity, OU fitting
- `test_validation/` - Metrics, walk-forward

### Integration Tests

```python
# tests/test_tidy_signal/test_integration/test_parsnip_integration.py

def test_prophet_model_integration():
    """Test py-parsnip prophet model → tidy-signal workflow"""
    from py_parsnip import prophet_reg

    # Train fundamental model
    model = prophet_reg().fit(train_data, formula="price ~ date")
    predictions = model.predict(features)

    # Use in tidy-signal
    signal = (align(forwards, predictions)
              .detect(signal_type='divergence')
              .calibrate(model='ou_process'))

    outputs, coefficients, stats = signal.extract_outputs()

    # Validate output schema
    assert 'divergence' in outputs.columns
    assert 'half_life' in coefficients['parameter_name'].values
    assert 'sharpe_ratio' in stats.columns
```

### Synthetic Test Data

Create synthetic data with known properties:
- Cointegrated pairs with known hedge ratio
- OU process with known parameters (λ, μ, σ)
- Data with intentional lookahead bias (to verify detection)

---

## 12. Post-MVP Roadmap (Phases 6-8)

### Phase 6: Recipes

SignalRecipe for reproducible preprocessing (scoping doc Section 16.5)

### Phase 7: Workflows

SignalWorkflow for production versioning (scoping doc Section 16.6)

### Phase 8: Workflowsets

WorkflowSet for systematic comparison (scoping doc Section 16.3-16.4)

---

## 13. Risk Mitigation

| Risk | Mitigation |
|------|------------|
| xarray complexity | VintageDataFrame wrapper hides complexity |
| OU fitting instability | Multiple initial values, convergence checks |
| py-parsnip API changes | Integration tests, pin versions |
| Scope creep | Strict MVP focus per scoping doc |

---

**Document Status:** Implementation Ready
**Source of Truth:** `.claude_plans/tidy_signal_scoping_document.md` (v1.1)
**Next Action:** Set up tidy-signal-env, begin Day 1 implementation
