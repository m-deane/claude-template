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

### 2.4 xarray Alignment Behavior Specifications

**The `align()` Verb - Complete Specification:**

```python
import xarray as xr
import pandas as pd
from typing import Literal, Optional, Union

def align(
    forward_data: Union[xr.Dataset, 'VintageDataFrame'],
    fundamental_data: Union[pd.DataFrame, xr.DataArray],
    by: str = 'observation_date',
    how: Literal['inner', 'outer', 'left', 'right'] = 'inner',
    vintage_mode: Literal['as_of', 'latest', 'exact'] = 'latest',
    vintage_date: Optional[str] = None,
    tolerance: Optional[str] = None,
    missing_strategy: Literal['ffill', 'bfill', 'interpolate', 'drop'] = 'ffill',
    max_gap: Optional[int] = 5
) -> 'AlignedSignalData':
    """
    Align forward curve data with fundamental model predictions.

    Parameters
    ----------
    forward_data : VintageDataFrame or xr.Dataset
        Forward curve data with dimensions [vintage_date, observation_date, tenor, contract]
    fundamental_data : pd.DataFrame or xr.DataArray
        Fundamental model predictions (output from py-parsnip ModelFit.predict())
    by : str, default 'observation_date'
        Primary alignment key (coordinate name to join on)
    how : {'inner', 'outer', 'left', 'right'}, default 'inner'
        Join type:
        - 'inner': Keep only dates present in both datasets
        - 'outer': Keep all dates from both, fill missing with NaN
        - 'left': Keep all dates from forward_data
        - 'right': Keep all dates from fundamental_data
    vintage_mode : {'as_of', 'latest', 'exact'}, default 'latest'
        How to select vintage:
        - 'as_of': Use data available as of vintage_date (forward-fill)
        - 'latest': Use most recent vintage
        - 'exact': Require exact vintage_date match
    vintage_date : str, optional
        Required if vintage_mode='as_of' or 'exact'. ISO format date string.
    tolerance : str, optional
        Maximum time difference for inexact matching, e.g., '1D' for 1 day.
        If None, requires exact match on `by` coordinate.
    missing_strategy : {'ffill', 'bfill', 'interpolate', 'drop'}, default 'ffill'
        How to handle missing values after alignment:
        - 'ffill': Forward-fill up to max_gap
        - 'bfill': Backward-fill up to max_gap
        - 'interpolate': Linear interpolation
        - 'drop': Remove rows with any NaN
    max_gap : int, optional, default 5
        Maximum number of consecutive missing values to fill.
        If gap > max_gap, values remain NaN.

    Returns
    -------
    AlignedSignalData
        Container with aligned forward and fundamental data,
        plus SignalBlueprint for future alignment operations.

    Raises
    ------
    SignalAlignmentError
        If alignment fails due to incompatible data or no overlapping dates.

    Examples
    --------
    >>> # Basic alignment using latest vintage
    >>> aligned = align(forwards, model.predict(features))

    >>> # Point-in-time alignment for backtesting
    >>> aligned = align(
    ...     forwards,
    ...     fundamentals,
    ...     vintage_mode='as_of',
    ...     vintage_date='2024-01-15',
    ...     how='inner'
    ... )

    >>> # Alignment with tolerance for date mismatches
    >>> aligned = align(
    ...     forwards,
    ...     fundamentals,
    ...     tolerance='1D',  # Allow 1-day mismatch
    ...     missing_strategy='interpolate'
    ... )
    """
    # Implementation details below...
```

**Coordinate Handling Edge Cases:**

| Scenario | Behavior | Configuration |
|----------|----------|---------------|
| **Date not in vintage_coords** | Forward-fill from nearest prior date | `vintage_mode='as_of'` |
| **Date not found (exact mode)** | Raise `SignalAlignmentError` | `vintage_mode='exact'` |
| **No overlapping dates** | Raise `SignalAlignmentError` | Any `how` mode |
| **Different date frequencies** | Resample to coarser frequency | Automatic |
| **NaT (missing timestamps)** | Drop rows with NaT before alignment | Automatic |
| **Duplicate timestamps** | Keep last value (warn) | Automatic |

**Coordinate dtype Handling:**

```python
# Automatic dtype harmonization
DATETIME_DTYPES = {'datetime64[ns]', 'datetime64[us]', 'datetime64[ms]'}
STRING_DTYPES = {'object', 'str', 'string'}

def harmonize_coordinates(coord1, coord2, coord_name: str):
    """
    Harmonize coordinate dtypes between two datasets.

    Rules:
    1. datetime types: Convert both to datetime64[ns]
    2. string types: Convert both to str
    3. numeric types: Use higher precision
    4. Incompatible: Raise SignalAlignmentError
    """
    dtype1 = str(coord1.dtype)
    dtype2 = str(coord2.dtype)

    if dtype1 in DATETIME_DTYPES or dtype2 in DATETIME_DTYPES:
        # Convert both to datetime64[ns]
        coord1 = pd.to_datetime(coord1).values
        coord2 = pd.to_datetime(coord2).values
    elif dtype1 in STRING_DTYPES or dtype2 in STRING_DTYPES:
        # Convert both to string
        coord1 = coord1.astype(str)
        coord2 = coord2.astype(str)
    elif not np.issubdtype(coord1.dtype, np.number) or not np.issubdtype(coord2.dtype, np.number):
        raise SignalAlignmentError(
            f"Incompatible dtypes for {coord_name}: {dtype1} vs {dtype2}"
        )

    return coord1, coord2
```

**Multi-Index Alignment (vintage_date × observation_date pairs):**

```python
def align_multi_index(forward_ds, fundamental_df, vintage_date):
    """
    Align when fundamental data has different values per vintage.

    This handles the case where fundamental model predictions
    are themselves vintage-dependent (e.g., model retrained weekly).
    """
    # Create multi-index from forward data
    forward_flat = forward_ds.sel(vintage_date=vintage_date, method='ffill')

    # If fundamental_df has vintage column, filter it
    if 'vintage_date' in fundamental_df.columns:
        fundamental_filtered = fundamental_df[
            fundamental_df['vintage_date'] <= vintage_date
        ].sort_values('vintage_date').groupby('observation_date').last()
    else:
        fundamental_filtered = fundamental_df.set_index('observation_date')

    # Align on observation_date
    common_dates = forward_flat.coords['observation_date'].values
    common_dates = np.intersect1d(
        common_dates,
        fundamental_filtered.index.values
    )

    if len(common_dates) == 0:
        raise SignalAlignmentError("No overlapping observation dates")

    return forward_flat.sel(observation_date=common_dates), \
           fundamental_filtered.loc[common_dates]
```

**Ragged-Edge Handling:**

```python
def handle_ragged_edge(
    data: xr.Dataset,
    max_staleness: int = 5,
    warn_stale: bool = True
) -> xr.Dataset:
    """
    Handle ragged-edge data (different publication lags by variable).

    Parameters
    ----------
    data : xr.Dataset
        Dataset potentially with ragged edge (different last valid dates per variable)
    max_staleness : int
        Maximum days a variable can be stale before flagging
    warn_stale : bool
        Whether to emit warning for stale data

    Returns
    -------
    xr.Dataset
        Dataset with staleness flags added
    """
    last_valid = {}
    staleness = {}

    for var in data.data_vars:
        # Find last non-NaN observation per variable
        valid_mask = ~np.isnan(data[var].values)
        if valid_mask.any():
            last_valid_idx = np.where(valid_mask.any(axis=tuple(range(1, valid_mask.ndim))))[0][-1]
            last_valid[var] = data.coords['observation_date'].values[last_valid_idx]

            # Calculate staleness
            current_date = data.coords['observation_date'].values[-1]
            staleness[var] = (pd.Timestamp(current_date) -
                              pd.Timestamp(last_valid[var])).days

    # Add staleness as metadata
    data.attrs['last_valid_dates'] = last_valid
    data.attrs['staleness_days'] = staleness

    # Warn if any variable exceeds max_staleness
    if warn_stale:
        stale_vars = [v for v, s in staleness.items() if s > max_staleness]
        if stale_vars:
            import warnings
            warnings.warn(
                f"Variables exceed {max_staleness}-day staleness: {stale_vars}. "
                f"Staleness: {dict((v, staleness[v]) for v in stale_vars)}"
            )

    return data
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

### 4.3 SignalBlueprint (Alignment Metadata)

```python
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
import pandas as pd

@dataclass
class SignalBlueprint:
    """
    Stores alignment metadata ensuring consistent transformations
    between calibration and prediction phases.

    Extends py-hardhat Blueprint pattern for multi-dimensional signal data.
    """
    # Core alignment rules
    forward_columns: List[str]              # Columns from forward curve data
    fundamental_columns: List[str]          # Columns from fundamental model output
    alignment_key: str                      # Primary join key ('observation_date')
    vintage_handling: str                   # 'as_of', 'latest', 'exact'

    # Coordinate specifications
    vintage_coords: Optional[pd.DatetimeIndex] = None   # Valid vintage dates
    observation_coords: Optional[pd.DatetimeIndex] = None  # Valid observation dates
    tenor_coords: Optional[List[str]] = None            # Valid tenors ['1M', '3M', '6M']
    contract_coords: Optional[List[str]] = None         # Valid contract identifiers

    # Data type enforcement
    column_dtypes: Dict[str, str] = field(default_factory=dict)  # {'price': 'float64'}

    # Alignment behavior
    missing_data_strategy: str = 'ffill'    # 'ffill', 'bfill', 'interpolate', 'drop'
    max_staleness_days: int = 5             # Maximum days to forward-fill
    coordinate_tolerance: Optional[str] = None  # e.g., '1D' for 1-day tolerance

    # Calibration metadata (filled during calibrate())
    calibration_vintage: Optional[str] = None
    calibration_date_range: Optional[tuple] = None
    standardization_params: Dict[str, float] = field(default_factory=dict)  # mean, std

    def validate_new_data(self, new_data) -> bool:
        """
        Validate new data conforms to blueprint specifications.

        Returns True if valid, raises SignalAlignmentError if not.
        """
        # Check required columns exist
        required = set(self.forward_columns + self.fundamental_columns)
        actual = set(new_data.columns) if hasattr(new_data, 'columns') else set(new_data.data_vars)

        missing = required - actual
        if missing:
            raise SignalAlignmentError(f"Missing columns: {missing}")

        # Check dtype compatibility
        for col, expected_dtype in self.column_dtypes.items():
            if col in new_data:
                actual_dtype = str(new_data[col].dtype)
                if not self._dtypes_compatible(actual_dtype, expected_dtype):
                    raise SignalAlignmentError(
                        f"Column {col}: expected {expected_dtype}, got {actual_dtype}"
                    )

        # Check coordinate coverage
        if self.contract_coords:
            new_contracts = set(new_data.coords.get('contract', []))
            unknown = new_contracts - set(self.contract_coords)
            if unknown:
                raise SignalAlignmentError(f"Unknown contracts: {unknown}")

        return True

    def apply_alignment(self, forward_data, fundamental_data) -> 'AlignedSignalData':
        """
        Apply blueprint rules to align forward and fundamental data.

        This is the 'forge' equivalent for signal data.
        """
        # Apply vintage selection
        if self.vintage_handling == 'as_of':
            forward_aligned = forward_data.sel(
                vintage_date=self.calibration_vintage,
                method='ffill'
            )
        elif self.vintage_handling == 'latest':
            forward_aligned = forward_data.isel(vintage_date=-1)
        else:  # 'exact'
            forward_aligned = forward_data.sel(vintage_date=self.calibration_vintage)

        # Align on observation_date
        aligned = xr.align(
            forward_aligned,
            fundamental_data,
            join='inner',
            exclude=['vintage_date']
        )

        # Apply missing data strategy
        if self.missing_data_strategy == 'ffill':
            aligned = [ds.ffill(dim='observation_date', limit=self.max_staleness_days)
                       for ds in aligned]

        return AlignedSignalData(
            forward=aligned[0],
            fundamental=aligned[1],
            blueprint=self
        )

    def _dtypes_compatible(self, actual: str, expected: str) -> bool:
        """Check if dtypes are compatible (e.g., float32 compatible with float64)"""
        float_types = {'float16', 'float32', 'float64', 'float'}
        int_types = {'int8', 'int16', 'int32', 'int64', 'int'}

        if actual in float_types and expected in float_types:
            return True
        if actual in int_types and expected in int_types:
            return True
        return actual == expected


class SignalAlignmentError(Exception):
    """Raised when data alignment fails validation."""
    pass


@dataclass
class AlignedSignalData:
    """Container for aligned forward and fundamental data."""
    forward: xr.DataArray
    fundamental: xr.DataArray
    blueprint: SignalBlueprint

    def compute_divergence(self, standardize: bool = True) -> xr.DataArray:
        """Compute divergence between forward and fundamental."""
        divergence = self.forward - self.fundamental

        if standardize and self.blueprint.standardization_params:
            mean = self.blueprint.standardization_params.get('mean', 0)
            std = self.blueprint.standardization_params.get('std', 1)
            divergence = (divergence - mean) / std

        return divergence
```

**SignalBlueprint Purpose:**
- Stores alignment metadata from calibration phase
- Ensures consistent transformations when predicting on new data
- Validates new data conforms to expected schema
- Extends py-hardhat `Blueprint` pattern for multi-dimensional xarray data

### 4.4 Three-DataFrame Output Pattern

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

### 5.2 OU Process MLE Implementation Guide

**Method 1: Exact Discrete MLE (Recommended)**

The continuous OU process discretizes to an AR(1) process:
```
D_t = a + b * D_{t-1} + ε_t,  where ε_t ~ N(0, σ_ε²)
```

Parameter mapping:
- `b = exp(-λ * Δt)` where Δt is observation interval (typically 1 day)
- `a = μ * (1 - b)`
- `σ_ε² = (σ² / 2λ) * (1 - exp(-2λΔt))`

```python
import numpy as np
from scipy import optimize
from scipy import stats

def fit_ou_process_mle(divergence_series: np.ndarray, dt: float = 1.0) -> dict:
    """
    Fit Ornstein-Uhlenbeck process via Maximum Likelihood Estimation.

    Parameters
    ----------
    divergence_series : np.ndarray
        Time series of divergence values (forward - fundamental)
    dt : float
        Time step between observations (default=1.0 for daily data)

    Returns
    -------
    dict with keys:
        lambda_: Mean reversion speed
        mu: Long-run mean
        sigma: Volatility
        half_life: Days for 50% decay
        std_errors: Dict of parameter standard errors
        log_likelihood: Maximized log-likelihood
        aic: Akaike Information Criterion
        bic: Bayesian Information Criterion
    """
    D = divergence_series
    n = len(D)

    # Remove NaN values
    D = D[~np.isnan(D)]
    n = len(D)

    if n < 10:
        raise ValueError("Need at least 10 observations to fit OU process")

    # Prepare lagged values
    D_prev = D[:-1]  # D_{t-1}
    D_curr = D[1:]   # D_t

    def neg_log_likelihood(params):
        """Negative log-likelihood for OU process."""
        lambda_, mu, sigma = params

        # Ensure positive parameters
        if lambda_ <= 0 or sigma <= 0:
            return np.inf

        # AR(1) parameters from OU parameters
        b = np.exp(-lambda_ * dt)
        a = mu * (1 - b)
        sigma_eps_sq = (sigma**2 / (2 * lambda_)) * (1 - np.exp(-2 * lambda_ * dt))

        if sigma_eps_sq <= 0:
            return np.inf

        # Predicted values and residuals
        D_pred = a + b * D_prev
        residuals = D_curr - D_pred

        # Log-likelihood (Gaussian)
        n_obs = len(residuals)
        log_lik = -0.5 * n_obs * np.log(2 * np.pi * sigma_eps_sq)
        log_lik -= 0.5 * np.sum(residuals**2) / sigma_eps_sq

        return -log_lik  # Negative for minimization

    # Initial parameter estimates via OLS
    X = np.column_stack([np.ones(len(D_prev)), D_prev])
    y = D_curr
    beta_ols = np.linalg.lstsq(X, y, rcond=None)[0]
    a_init, b_init = beta_ols

    # Convert OLS to OU initial guesses
    if 0 < b_init < 1:
        lambda_init = -np.log(b_init) / dt
        mu_init = a_init / (1 - b_init)
    else:
        lambda_init = 0.1
        mu_init = np.mean(D)

    residuals_init = y - X @ beta_ols
    sigma_init = np.std(residuals_init) * np.sqrt(2 * lambda_init)

    # Bounds: lambda > 0, sigma > 0, mu unbounded
    bounds = [(1e-6, 10), (None, None), (1e-6, None)]
    initial_params = [lambda_init, mu_init, sigma_init]

    # Optimize
    result = optimize.minimize(
        neg_log_likelihood,
        initial_params,
        method='L-BFGS-B',
        bounds=bounds,
        options={'maxiter': 1000}
    )

    lambda_opt, mu_opt, sigma_opt = result.x
    log_lik = -result.fun

    # Calculate half-life
    half_life = np.log(2) / lambda_opt

    # Standard errors via Hessian inverse
    try:
        hessian = _numerical_hessian(neg_log_likelihood, result.x)
        cov_matrix = np.linalg.inv(hessian)
        std_errors = {
            'lambda': np.sqrt(cov_matrix[0, 0]),
            'mu': np.sqrt(cov_matrix[1, 1]),
            'sigma': np.sqrt(cov_matrix[2, 2])
        }
    except:
        std_errors = {'lambda': np.nan, 'mu': np.nan, 'sigma': np.nan}

    # Information criteria
    k = 3  # Number of parameters
    aic = 2 * k - 2 * log_lik
    bic = k * np.log(n) - 2 * log_lik

    return {
        'lambda_': lambda_opt,
        'mu': mu_opt,
        'sigma': sigma_opt,
        'half_life': half_life,
        'std_errors': std_errors,
        'log_likelihood': log_lik,
        'aic': aic,
        'bic': bic,
        'converged': result.success,
        'n_observations': n
    }


def _numerical_hessian(func, x, eps=1e-5):
    """Compute numerical Hessian matrix."""
    n = len(x)
    hessian = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            x_pp = x.copy()
            x_pm = x.copy()
            x_mp = x.copy()
            x_mm = x.copy()

            x_pp[i] += eps
            x_pp[j] += eps
            x_pm[i] += eps
            x_pm[j] -= eps
            x_mp[i] -= eps
            x_mp[j] += eps
            x_mm[i] -= eps
            x_mm[j] -= eps

            hessian[i, j] = (func(x_pp) - func(x_pm) - func(x_mp) + func(x_mm)) / (4 * eps**2)

    return hessian
```

**Method 2: Kalman Filter State-Space (Alternative)**

For more complex scenarios (e.g., missing data, time-varying parameters):

```python
from statsmodels.tsa.statespace.mlemodel import MLEModel

class OUProcess(MLEModel):
    """
    State-space representation of Ornstein-Uhlenbeck process.

    State equation: D_t = μ + e^(-λΔt)(D_{t-1} - μ) + ε_t
    """
    def __init__(self, endog, dt=1.0):
        super().__init__(endog, k_states=1)
        self.dt = dt
        self['design'] = np.array([[1.0]])
        self['selection'] = np.array([[1.0]])

    @property
    def param_names(self):
        return ['lambda', 'mu', 'sigma']

    @property
    def start_params(self):
        return np.array([0.1, np.mean(self.endog), np.std(self.endog)])

    def transform_params(self, unconstrained):
        """Ensure positive lambda and sigma."""
        return np.array([
            np.exp(unconstrained[0]),   # lambda > 0
            unconstrained[1],            # mu unbounded
            np.exp(unconstrained[2])    # sigma > 0
        ])

    def untransform_params(self, constrained):
        return np.array([
            np.log(constrained[0]),
            constrained[1],
            np.log(constrained[2])
        ])

    def update(self, params, **kwargs):
        lambda_, mu, sigma = params

        # State transition
        phi = np.exp(-lambda_ * self.dt)
        self['transition', 0, 0] = phi

        # State intercept (μ * (1 - φ))
        self['state_intercept', 0, 0] = mu * (1 - phi)

        # State covariance
        state_var = (sigma**2 / (2 * lambda_)) * (1 - np.exp(-2 * lambda_ * self.dt))
        self['state_cov', 0, 0] = state_var


# Usage:
# model = OUProcess(divergence_series)
# results = model.fit()
# lambda_, mu, sigma = results.params
```

**Diagnostic Checks for OU Fit:**

```python
def diagnose_ou_fit(divergence_series: np.ndarray, ou_params: dict) -> dict:
    """
    Diagnostic checks for OU process fit quality.

    Returns dict of diagnostic results.
    """
    lambda_ = ou_params['lambda_']
    mu = ou_params['mu']
    sigma = ou_params['sigma']

    # 1. Compute residuals
    D = divergence_series
    D_prev = D[:-1]
    D_curr = D[1:]
    b = np.exp(-lambda_)
    a = mu * (1 - b)
    predicted = a + b * D_prev
    residuals = D_curr - predicted

    # 2. Normality test (Jarque-Bera)
    jb_stat, jb_pvalue = stats.jarque_bera(residuals)

    # 3. Autocorrelation test (Ljung-Box)
    from statsmodels.stats.diagnostic import acorr_ljungbox
    lb_result = acorr_ljungbox(residuals, lags=[10], return_df=True)
    lb_pvalue = lb_result['lb_pvalue'].values[0]

    # 4. Half-life reasonableness
    half_life = np.log(2) / lambda_
    half_life_reasonable = 1 < half_life < 252  # Between 1 day and 1 year

    # 5. Mean reversion strength
    mean_reversion_strong = lambda_ > 0.01  # Decays meaningfully

    return {
        'residuals_normal': jb_pvalue > 0.05,
        'jb_pvalue': jb_pvalue,
        'residuals_uncorrelated': lb_pvalue > 0.05,
        'lb_pvalue': lb_pvalue,
        'half_life_reasonable': half_life_reasonable,
        'half_life_days': half_life,
        'mean_reversion_strong': mean_reversion_strong,
        'residual_std': np.std(residuals),
        'r_squared': 1 - np.var(residuals) / np.var(D_curr)
    }
```

### 5.3 Entry/Exit Optimization

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
