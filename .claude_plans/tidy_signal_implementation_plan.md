# tidy-signal: Comprehensive Implementation Plan

**Version:** 1.0 | **Date:** December 7, 2025 | **Status:** Implementation Ready

---

## Executive Summary

This implementation plan provides a detailed, actionable roadmap for building tidy-signal, a Python library for commodities convergence trading signals. The plan enforces all coding standards from py-tidymodels (frozen dataclasses, registry pattern, three-DataFrame outputs) and provides day-by-day granular tasks.

**Key Integration Opportunities with ChromaDB:**
- Store calibrated signal specifications for retrieval
- Build searchable knowledge base of signal performance across commodities
- Semantic search for similar market regimes/patterns
- Document storage for backtest results and validation metrics

**MVP Focus (Phases 1-5):** Verb API only - `align()`, `detect()`, `calibrate()`, `backtest()`

**Post-MVP (Phases 6-8):** Recipes → Workflows → Workflowsets patterns

**Timeline:** 12 weeks MVP + ongoing post-MVP development

---

## 1. Coding Standards Enforcement

### 1.1 Frozen Dataclass Pattern (from py-parsnip ModelSpec)

**MUST implement for all specification classes:**

```python
from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass(frozen=True)
class SignalSpec:
    """Immutable signal specification - NO mutable state"""
    signal_type: str
    engine: str
    mode: str
    args: Dict[str, Any] = field(default_factory=dict)

    def set_args(self, **kwargs) -> 'SignalSpec':
        """Return NEW spec with updated args (immutable pattern)"""
        new_args = {**self.args, **kwargs}
        return dataclasses.replace(self, args=new_args)
```

**Requirements:**
- ALL specification classes MUST be frozen
- NO mutable state after construction
- Use `dataclasses.replace()` or `set_*()` methods for modifications
- All modifications return NEW instances

### 1.2 Registry Pattern (from py-parsnip engine_registry.py)

**MUST implement engine discovery via decorators:**

```python
# In tidy_signal/core/registry.py
_SIGNAL_ENGINE_REGISTRY = {}

def register_signal_engine(signal_type: str, engine: str):
    """Decorator for registering signal engines"""
    def decorator(cls):
        key = (signal_type, engine)
        _SIGNAL_ENGINE_REGISTRY[key] = cls
        return cls
    return decorator

def get_signal_engine(signal_type: str, engine: str):
    """Runtime engine discovery"""
    key = (signal_type, engine)
    if key not in _SIGNAL_ENGINE_REGISTRY:
        raise ValueError(f"Signal engine not found: {signal_type}/{engine}")
    return _SIGNAL_ENGINE_REGISTRY[key]()
```

**Requirements:**
- Decorator-based registration for all engines
- Runtime discovery via `get_signal_engine()`
- Clear error messages for missing engines
- `list_signal_engines()` for discovery

### 1.3 Three-DataFrame Output Pattern (from py-parsnip)

**MUST return standardized outputs for ALL engines:**

```python
def extract_outputs(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Returns:
        outputs_df: Observation-level results (date, divergence, signal, position, pnl)
        parameters_df: Model parameters (lambda, mu, sigma, half_life with std_error, p_value)
        metrics_df: Signal-level metrics (sharpe, ic, max_dd, win_rate)
    """
    return outputs_df, parameters_df, metrics_df
```

**Required Columns:**

**outputs_df (observation-level):**
- `date`: datetime
- `contract`: str
- `days_to_settlement`: int
- `forward_value`: float
- `fundamental_value`: float
- `divergence`: float
- `divergence_zscore`: float
- `signal_strength`: float
- `entry_signal`: bool
- `exit_signal`: bool
- `position`: str ('long', 'short', 'flat')
- `pnl`: float
- `split`: str ('train', 'test', 'validation')

**parameters_df (model parameters):**
- `parameter_name`: str
- `value`: float
- `std_error`: float
- `t_statistic`: float
- `p_value`: float
- `ci_lower`: float
- `ci_upper`: float

**metrics_df (signal-level):**
- `sharpe_ratio`: float
- `information_coefficient`: float
- `max_drawdown`: float
- `win_rate`: float
- `profit_factor`: float
- `avg_holding_period`: int
- `num_trades`: int

### 1.4 Abstract Base Class Requirements

**ALL signal engines MUST implement:**

```python
from abc import ABC, abstractmethod

class SignalEngine(ABC):
    @abstractmethod
    def fit(self, spec: SignalSpec, aligned_data: AlignedSignalData) -> SignalFit:
        """Fit signal model to data"""
        pass

    @abstractmethod
    def predict(self, fit: SignalFit, new_data) -> pd.DataFrame:
        """Generate signals on new data"""
        pass

    @abstractmethod
    def extract_outputs(self, fit: SignalFit) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Return three-DataFrame standardized output"""
        pass

    @abstractmethod
    def translate_params(self, spec_params: Dict) -> Dict:
        """Map tidy-signal params to engine-specific params"""
        pass
```

### 1.5 Test Philosophy (from CLAUDE.md)

**MANDATORY testing requirements:**
- Tests AFTER every checkpoint
- NO placeholder/mock data
- 90%+ code coverage required
- Integration tests for end-to-end workflows
- Validate against reference implementations (statsmodels)

```bash
# Test command structure
source py-tidymodels2/bin/activate
python -m pytest tests/test_tidy_signal/ -v --cov=tidy_signal --cov-report=html
```

### 1.6 Virtual Environment (from CLAUDE.md)

**MUST use existing py-tidymodels2 environment:**
```bash
source py-tidymodels2/bin/activate
pip install -e .  # Editable mode for tidy-signal
```

### 1.7 No Placeholder Implementation (from .claude/CLAUDE.md)

**PROHIBITED patterns:**
- "In a full implementation..."
- "TODO: implement this later"
- Mock functions returning dummy data
- `pass` statements in production code
- Incomplete error handling

**REQUIRED patterns:**
- Complete working code on first attempt
- Full error handling with descriptive messages
- Type hints on ALL public functions
- Docstrings with examples on ALL public functions

### 1.8 File Organization (from CLAUDE.md)

**MUST organize into proper folders:**
- NO files in root directory
- Tests go in `tests/test_tidy_signal/`
- Documentation goes in `.claude_plans/`
- Regular cleanup of orphan files

---

## 2. File Structure & Implementation Order

### 2.1 Directory Structure

```
tidy_signal/
├── __init__.py                     # Package initialization, public API exports
├── core/
│   ├── __init__.py
│   ├── signal_spec.py              # SignalSpec frozen dataclass
│   ├── signal_fit.py               # SignalFit results container
│   ├── signal_blueprint.py         # SignalBlueprint alignment metadata
│   ├── registry.py                 # Engine registry pattern
│   └── outputs.py                  # Three-DataFrame output standardization
├── data/
│   ├── __init__.py
│   ├── vintage.py                  # VintageDataFrame xarray wrapper
│   ├── alignment.py                # align() verb implementation
│   └── structures.py               # AlignedSignalData container
├── verbs/
│   ├── __init__.py
│   ├── align.py                    # align() - match vintages/tenors
│   ├── slice.py                    # slice() - extract vintage/tenor
│   ├── detect.py                   # detect() - compute divergence
│   ├── calibrate.py                # calibrate() - fit convergence model
│   ├── diagnose.py                 # diagnose() - statistical tests
│   ├── converge.py                 # converge() - convergence dynamics
│   ├── time_entry.py               # time_entry() - entry rules
│   ├── time_exit.py                # time_exit() - exit rules
│   └── backtest.py                 # backtest() - historical validation
├── engines/
│   ├── __init__.py
│   ├── base.py                     # SignalEngine ABC
│   ├── ou_process_engine.py       # OU process implementation
│   ├── zscore_engine.py            # Z-score mean reversion
│   └── ecm_engine.py               # Error Correction Model
├── statistical/
│   ├── __init__.py
│   ├── cointegration.py            # Johansen, Engle-Granger tests
│   ├── stationarity.py             # ADF, KPSS tests
│   ├── ou_fitting.py               # OU process MLE estimation
│   └── structural_breaks.py        # Zivot-Andrews test
├── validation/
│   ├── __init__.py
│   ├── walk_forward.py             # Walk-forward analysis
│   ├── ic_analysis.py              # Information Coefficient
│   └── metrics.py                  # Performance metrics (Sharpe, drawdown)
├── commodities/
│   ├── __init__.py
│   ├── spreads.py                  # Calendar, crack, crush spreads
│   └── seasonality.py              # Seasonal decomposition
└── exceptions.py                   # Custom exceptions

tests/
└── test_tidy_signal/
    ├── __init__.py
    ├── test_core/
    │   ├── test_signal_spec.py
    │   ├── test_signal_fit.py
    │   ├── test_signal_blueprint.py
    │   └── test_registry.py
    ├── test_data/
    │   ├── test_vintage.py
    │   ├── test_alignment.py
    │   └── test_structures.py
    ├── test_verbs/
    │   ├── test_align.py
    │   ├── test_detect.py
    │   ├── test_calibrate.py
    │   └── test_backtest.py
    ├── test_engines/
    │   ├── test_ou_process_engine.py
    │   ├── test_zscore_engine.py
    │   └── test_ecm_engine.py
    ├── test_statistical/
    │   ├── test_cointegration.py
    │   ├── test_stationarity.py
    │   ├── test_ou_fitting.py
    │   └── test_structural_breaks.py
    ├── test_validation/
    │   ├── test_walk_forward.py
    │   ├── test_ic_analysis.py
    │   └── test_metrics.py
    ├── test_commodities/
    │   ├── test_spreads.py
    │   └── test_seasonality.py
    └── test_integration/
        ├── test_end_to_end.py
        ├── test_parsnip_integration.py
        └── test_vintage_alignment.py
```

### 2.2 Implementation Dependency Graph

```
PHASE 1: Core Infrastructure (Week 1-2)
┌─────────────────────────────────────────────┐
│ exceptions.py (Day 1)                       │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ core/signal_spec.py (Day 1-2)               │
│ - SignalSpec frozen dataclass               │
│ - set_args(), set_mode() methods            │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ core/registry.py (Day 2)                    │
│ - register_signal_engine() decorator        │
│ - get_signal_engine() discovery             │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ engines/base.py (Day 3)                     │
│ - SignalEngine ABC                          │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ core/outputs.py (Day 3)                     │
│ - Three-DataFrame validation                │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ core/signal_fit.py (Day 4)                  │
│ - SignalFit container                       │
│ - predict(), extract_outputs() methods      │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ data/vintage.py (Day 5-6)                   │
│ - VintageDataFrame xarray wrapper           │
│ - as_of(), latest(), to_tidy() methods      │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ core/signal_blueprint.py (Day 7-8)          │
│ - SignalBlueprint alignment metadata        │
│ - validate_new_data(), apply_alignment()    │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ data/structures.py (Day 9)                  │
│ - AlignedSignalData container               │
│ - compute_divergence() method               │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ data/alignment.py (Day 10)                  │
│ verbs/align.py (Day 10)                     │
│ - align() verb implementation               │
│ - harmonize_coordinates()                   │
└─────────────────────────────────────────────┘

PHASE 2: Statistical Arbitrage (Week 3-4)
┌─────────────────────────────────────────────┐
│ statistical/stationarity.py (Day 11-12)     │
│ - test_stationarity() ADF + KPSS            │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ statistical/cointegration.py (Day 13-14)    │
│ - johansen_test(), engle_granger_test()     │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ statistical/ou_fitting.py (Day 15-17)       │
│ - fit_ou_process_mle()                      │
│ - diagnose_ou_fit()                         │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ engines/ou_process_engine.py (Day 18-20)    │
│ - OUProcessEngine implementation            │
│ - fit(), predict(), extract_outputs()       │
└─────────────────────────────────────────────┘

PHASE 3: Validation Framework (Week 5-6)
┌─────────────────────────────────────────────┐
│ validation/metrics.py (Day 21-22)           │
│ - calculate_sharpe(), calculate_ic()        │
│ - calculate_drawdown()                      │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ validation/walk_forward.py (Day 23-25)      │
│ - walk_forward_analysis()                   │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ verbs/backtest.py (Day 26-28)               │
│ - backtest() verb with transaction costs    │
└─────────────────────────────────────────────┘

PHASE 4: Additional Verbs & Commodities (Week 7-8)
┌─────────────────────────────────────────────┐
│ verbs/detect.py (Day 29-30)                 │
│ verbs/calibrate.py (Day 31-32)              │
│ verbs/diagnose.py (Day 33-34)               │
│ verbs/converge.py (Day 35-36)               │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ commodities/spreads.py (Day 37-39)          │
│ - calendar_spread(), crack_spread()         │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ commodities/seasonality.py (Day 40-42)      │
│ - seasonal_decomposition()                  │
└─────────────────────────────────────────────┘

PHASE 5: Polish & Integration (Week 9-12)
┌─────────────────────────────────────────────┐
│ Integration tests (Day 43-49)               │
│ Documentation (Day 50-56)                   │
│ Performance optimization (Day 57-60)        │
└─────────────────────────────────────────────┘
```

---

## 3. Phase 1 Detailed Breakdown (Week 1-2: Days 1-10)

### Day 1: Exception Classes & SignalSpec Foundation

**Files to create:**
1. `/home/user/claude-template/tidy_signal/exceptions.py`
2. `/home/user/claude-template/tidy_signal/__init__.py`
3. `/home/user/claude-template/tidy_signal/core/__init__.py`
4. `/home/user/claude-template/tidy_signal/core/signal_spec.py`

**tidy_signal/exceptions.py:**
```python
"""Custom exceptions for tidy-signal"""

class SignalError(Exception):
    """Base exception for tidy-signal"""
    pass

class SignalAlignmentError(SignalError):
    """Raised when data alignment fails"""
    pass

class SignalEngineError(SignalError):
    """Raised when signal engine operations fail"""
    pass

class SignalValidationError(SignalError):
    """Raised when signal validation fails"""
    pass

class VintageDataError(SignalError):
    """Raised when vintage data operations fail"""
    pass
```

**tidy_signal/core/signal_spec.py:**
```python
"""SignalSpec - Immutable signal specification"""
from dataclasses import dataclass, field, replace
from typing import Dict, Any, Optional
import json

@dataclass(frozen=True)
class SignalSpec:
    """
    Immutable signal specification following py-parsnip ModelSpec pattern.

    Parameters
    ----------
    signal_type : str
        Type of signal ('mean_reversion', 'trend_following', etc.)
    engine : str
        Engine name ('ou_process', 'zscore', 'ecm')
    mode : str
        Signal mode ('long_short', 'long_only', 'short_only')
    args : dict
        Signal-specific hyperparameters
    metadata : dict
        Creation metadata (timestamp, author, version)

    Examples
    --------
    >>> spec = SignalSpec(
    ...     signal_type='mean_reversion',
    ...     engine='ou_process',
    ...     mode='long_short',
    ...     args={'entry_threshold': 2.0, 'lookback': 60}
    ... )
    >>> updated_spec = spec.set_args(entry_threshold=2.5)
    """
    signal_type: str
    engine: str
    mode: str = "long_short"
    args: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def set_args(self, **kwargs) -> 'SignalSpec':
        """
        Return new spec with updated args (immutable pattern).

        Parameters
        ----------
        **kwargs : dict
            Arguments to update

        Returns
        -------
        SignalSpec
            New spec with updated args
        """
        new_args = {**self.args, **kwargs}
        return replace(self, args=new_args)

    def set_mode(self, mode: str) -> 'SignalSpec':
        """
        Return new spec with updated mode.

        Parameters
        ----------
        mode : str
            New mode ('long_short', 'long_only', 'short_only')

        Returns
        -------
        SignalSpec
            New spec with updated mode
        """
        return replace(self, mode=mode)

    def set_engine(self, engine: str) -> 'SignalSpec':
        """
        Return new spec with updated engine.

        Parameters
        ----------
        engine : str
            New engine name

        Returns
        -------
        SignalSpec
            New spec with updated engine
        """
        return replace(self, engine=engine)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'signal_type': self.signal_type,
            'engine': self.engine,
            'mode': self.mode,
            'args': self.args,
            'metadata': self.metadata
        }

    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> 'SignalSpec':
        """Create from dictionary"""
        return cls(**d)

    @classmethod
    def from_json(cls, json_str: str) -> 'SignalSpec':
        """Create from JSON string"""
        return cls.from_dict(json.loads(json_str))
```

**Tests to create:**
- `/home/user/claude-template/tests/test_tidy_signal/__init__.py`
- `/home/user/claude-template/tests/test_tidy_signal/test_core/__init__.py`
- `/home/user/claude-template/tests/test_tidy_signal/test_core/test_signal_spec.py`

**test_core/test_signal_spec.py:**
```python
"""Tests for SignalSpec"""
import pytest
from tidy_signal.core.signal_spec import SignalSpec
import json

def test_signal_spec_creation():
    """Test SignalSpec creation"""
    spec = SignalSpec(
        signal_type='mean_reversion',
        engine='ou_process',
        mode='long_short',
        args={'entry_threshold': 2.0}
    )
    assert spec.signal_type == 'mean_reversion'
    assert spec.engine == 'ou_process'
    assert spec.mode == 'long_short'
    assert spec.args['entry_threshold'] == 2.0

def test_signal_spec_immutability():
    """Test that SignalSpec is immutable"""
    spec = SignalSpec(signal_type='test', engine='test', mode='long_short')
    with pytest.raises(AttributeError):
        spec.signal_type = 'changed'

def test_set_args_returns_new_spec():
    """Test set_args returns new instance"""
    spec1 = SignalSpec(signal_type='test', engine='test', args={'a': 1})
    spec2 = spec1.set_args(b=2)

    assert spec1.args == {'a': 1}
    assert spec2.args == {'a': 1, 'b': 2}
    assert spec1 is not spec2

def test_set_mode():
    """Test set_mode returns new instance"""
    spec1 = SignalSpec(signal_type='test', engine='test', mode='long_short')
    spec2 = spec1.set_mode('long_only')

    assert spec1.mode == 'long_short'
    assert spec2.mode == 'long_only'

def test_to_dict():
    """Test conversion to dictionary"""
    spec = SignalSpec(
        signal_type='mean_reversion',
        engine='ou_process',
        args={'threshold': 2.0}
    )
    d = spec.to_dict()

    assert d['signal_type'] == 'mean_reversion'
    assert d['engine'] == 'ou_process'
    assert d['args']['threshold'] == 2.0

def test_from_dict():
    """Test creation from dictionary"""
    d = {
        'signal_type': 'mean_reversion',
        'engine': 'ou_process',
        'mode': 'long_short',
        'args': {'threshold': 2.0},
        'metadata': {}
    }
    spec = SignalSpec.from_dict(d)

    assert spec.signal_type == 'mean_reversion'
    assert spec.args['threshold'] == 2.0

def test_json_serialization():
    """Test JSON serialization round-trip"""
    spec1 = SignalSpec(
        signal_type='mean_reversion',
        engine='ou_process',
        args={'threshold': 2.0}
    )
    json_str = spec1.to_json()
    spec2 = SignalSpec.from_json(json_str)

    assert spec1.to_dict() == spec2.to_dict()
```

**Acceptance criteria:**
- [ ] All tests pass
- [ ] SignalSpec is truly immutable (frozen)
- [ ] set_args() returns new instance
- [ ] JSON serialization works

---

### Day 2: Registry Pattern

**Files to create:**
- `/home/user/claude-template/tidy_signal/core/registry.py`
- `/home/user/claude-template/tests/test_tidy_signal/test_core/test_registry.py`

**tidy_signal/core/registry.py:**
```python
"""Signal engine registry pattern"""
from typing import Dict, Tuple, Optional, List, Type
from tidy_signal.exceptions import SignalEngineError

# Global registry
_SIGNAL_ENGINE_REGISTRY: Dict[Tuple[str, str], Type] = {}

def register_signal_engine(signal_type: str, engine: str):
    """
    Decorator for registering signal engines.

    Parameters
    ----------
    signal_type : str
        Signal type (e.g., 'mean_reversion')
    engine : str
        Engine name (e.g., 'ou_process')

    Examples
    --------
    >>> @register_signal_engine('mean_reversion', 'ou_process')
    ... class OUProcessEngine(SignalEngine):
    ...     pass
    """
    def decorator(cls):
        key = (signal_type, engine)
        if key in _SIGNAL_ENGINE_REGISTRY:
            raise SignalEngineError(
                f"Engine already registered: {signal_type}/{engine}"
            )
        _SIGNAL_ENGINE_REGISTRY[key] = cls
        return cls
    return decorator

def get_signal_engine(signal_type: str, engine: str):
    """
    Get signal engine instance from registry.

    Parameters
    ----------
    signal_type : str
        Signal type
    engine : str
        Engine name

    Returns
    -------
    SignalEngine
        Engine instance

    Raises
    ------
    SignalEngineError
        If engine not found
    """
    key = (signal_type, engine)
    if key not in _SIGNAL_ENGINE_REGISTRY:
        available = list_signal_engines(signal_type)
        raise SignalEngineError(
            f"Engine not found: {signal_type}/{engine}. "
            f"Available engines for {signal_type}: {available}"
        )
    return _SIGNAL_ENGINE_REGISTRY[key]()

def list_signal_engines(signal_type: Optional[str] = None) -> List[str]:
    """
    List available signal engines.

    Parameters
    ----------
    signal_type : str, optional
        Filter by signal type

    Returns
    -------
    list of str
        Available engine names
    """
    if signal_type:
        return [e for (s, e) in _SIGNAL_ENGINE_REGISTRY.keys() if s == signal_type]
    return [f"{s}/{e}" for (s, e) in _SIGNAL_ENGINE_REGISTRY.keys()]

def clear_registry():
    """Clear registry (for testing only)"""
    _SIGNAL_ENGINE_REGISTRY.clear()
```

**test_core/test_registry.py:**
```python
"""Tests for signal engine registry"""
import pytest
from tidy_signal.core.registry import (
    register_signal_engine,
    get_signal_engine,
    list_signal_engines,
    clear_registry
)
from tidy_signal.exceptions import SignalEngineError

class DummyEngine:
    """Dummy engine for testing"""
    pass

def test_register_engine():
    """Test engine registration"""
    clear_registry()

    @register_signal_engine('test_signal', 'test_engine')
    class TestEngine:
        pass

    engines = list_signal_engines('test_signal')
    assert 'test_engine' in engines

def test_get_engine():
    """Test engine retrieval"""
    clear_registry()

    @register_signal_engine('test_signal', 'test_engine')
    class TestEngine:
        pass

    engine = get_signal_engine('test_signal', 'test_engine')
    assert isinstance(engine, TestEngine)

def test_get_nonexistent_engine():
    """Test error on nonexistent engine"""
    clear_registry()

    with pytest.raises(SignalEngineError) as exc_info:
        get_signal_engine('nonexistent', 'nonexistent')

    assert 'Engine not found' in str(exc_info.value)

def test_duplicate_registration():
    """Test error on duplicate registration"""
    clear_registry()

    @register_signal_engine('test', 'test')
    class Engine1:
        pass

    with pytest.raises(SignalEngineError) as exc_info:
        @register_signal_engine('test', 'test')
        class Engine2:
            pass

    assert 'already registered' in str(exc_info.value)

def test_list_engines_filtered():
    """Test listing engines filtered by signal type"""
    clear_registry()

    @register_signal_engine('signal1', 'engine1')
    class Engine1:
        pass

    @register_signal_engine('signal1', 'engine2')
    class Engine2:
        pass

    @register_signal_engine('signal2', 'engine3')
    class Engine3:
        pass

    signal1_engines = list_signal_engines('signal1')
    assert len(signal1_engines) == 2
    assert 'engine1' in signal1_engines
    assert 'engine2' in signal1_engines

def test_list_all_engines():
    """Test listing all engines"""
    clear_registry()

    @register_signal_engine('signal1', 'engine1')
    class Engine1:
        pass

    @register_signal_engine('signal2', 'engine2')
    class Engine2:
        pass

    all_engines = list_signal_engines()
    assert len(all_engines) == 2
    assert 'signal1/engine1' in all_engines
    assert 'signal2/engine2' in all_engines
```

**Acceptance criteria:**
- [ ] All tests pass
- [ ] Registry prevents duplicate registrations
- [ ] get_signal_engine() provides helpful error messages
- [ ] list_signal_engines() works with and without filtering

---

### Day 3: SignalEngine ABC & Output Standardization

**Files to create:**
- `/home/user/claude-template/tidy_signal/engines/__init__.py`
- `/home/user/claude-template/tidy_signal/engines/base.py`
- `/home/user/claude-template/tidy_signal/core/outputs.py`
- `/home/user/claude-template/tests/test_tidy_signal/test_engines/__init__.py`
- `/home/user/claude-template/tests/test_tidy_signal/test_engines/test_base.py`
- `/home/user/claude-template/tests/test_tidy_signal/test_core/test_outputs.py`

**tidy_signal/engines/base.py:**
```python
"""Signal engine abstract base class"""
from abc import ABC, abstractmethod
from typing import Dict, Tuple, Any
import pandas as pd
from tidy_signal.core.signal_spec import SignalSpec

class SignalEngine(ABC):
    """
    Abstract base class for signal engines.

    All signal engines must implement:
    - fit(): Fit signal model to aligned data
    - predict(): Generate signals on new data
    - extract_outputs(): Return three-DataFrame standardized output
    - translate_params(): Map tidy-signal params to engine params
    """

    # Parameter mapping from tidy-signal to engine-specific
    param_map: Dict[str, str] = {}

    @abstractmethod
    def fit(self, spec: SignalSpec, aligned_data: Any) -> Dict[str, Any]:
        """
        Fit signal model to aligned data.

        Parameters
        ----------
        spec : SignalSpec
            Signal specification
        aligned_data : AlignedSignalData
            Aligned forward and fundamental data

        Returns
        -------
        dict
            Fitted model data
        """
        pass

    @abstractmethod
    def predict(self, fit_data: Dict[str, Any], new_data: Any) -> pd.DataFrame:
        """
        Generate signals on new data.

        Parameters
        ----------
        fit_data : dict
            Fitted model data from fit()
        new_data : Any
            New data to generate signals on

        Returns
        -------
        pd.DataFrame
            Signals with columns: date, signal_value, signal_strength, etc.
        """
        pass

    @abstractmethod
    def extract_outputs(self, fit_data: Dict[str, Any]) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Return three-DataFrame standardized output.

        Parameters
        ----------
        fit_data : dict
            Fitted model data

        Returns
        -------
        tuple of pd.DataFrame
            (outputs_df, parameters_df, metrics_df)
        """
        pass

    def translate_params(self, spec_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map tidy-signal params to engine-specific params.

        Parameters
        ----------
        spec_params : dict
            Parameters from SignalSpec.args

        Returns
        -------
        dict
            Engine-specific parameters
        """
        engine_params = {}
        for tidy_name, value in spec_params.items():
            engine_name = self.param_map.get(tidy_name, tidy_name)
            engine_params[engine_name] = value
        return engine_params
```

**tidy_signal/core/outputs.py:**
```python
"""Three-DataFrame output validation and standardization"""
from typing import Tuple, List
import pandas as pd
from tidy_signal.exceptions import SignalValidationError

# Required columns for each DataFrame
REQUIRED_OUTPUT_COLUMNS = [
    'date', 'contract', 'days_to_settlement', 'forward_value',
    'fundamental_value', 'divergence', 'divergence_zscore',
    'signal_strength', 'split'
]

REQUIRED_PARAMETER_COLUMNS = [
    'parameter_name', 'value', 'std_error', 'p_value'
]

REQUIRED_METRIC_COLUMNS = [
    'sharpe_ratio', 'information_coefficient', 'max_drawdown',
    'win_rate', 'num_trades'
]

def validate_outputs(
    outputs_df: pd.DataFrame,
    parameters_df: pd.DataFrame,
    metrics_df: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Validate three-DataFrame output structure.

    Parameters
    ----------
    outputs_df : pd.DataFrame
        Observation-level outputs
    parameters_df : pd.DataFrame
        Model parameters
    metrics_df : pd.DataFrame
        Signal-level metrics

    Returns
    -------
    tuple of pd.DataFrame
        Validated (outputs_df, parameters_df, metrics_df)

    Raises
    ------
    SignalValidationError
        If required columns missing
    """
    # Validate outputs_df
    missing_output_cols = set(REQUIRED_OUTPUT_COLUMNS) - set(outputs_df.columns)
    if missing_output_cols:
        raise SignalValidationError(
            f"outputs_df missing required columns: {missing_output_cols}"
        )

    # Validate parameters_df
    missing_param_cols = set(REQUIRED_PARAMETER_COLUMNS) - set(parameters_df.columns)
    if missing_param_cols:
        raise SignalValidationError(
            f"parameters_df missing required columns: {missing_param_cols}"
        )

    # Validate metrics_df (metrics are columns, not rows)
    missing_metric_cols = set(REQUIRED_METRIC_COLUMNS) - set(metrics_df.columns)
    if missing_metric_cols:
        raise SignalValidationError(
            f"metrics_df missing required columns: {missing_metric_cols}"
        )

    return outputs_df, parameters_df, metrics_df

def create_empty_outputs() -> pd.DataFrame:
    """Create empty outputs DataFrame with correct schema"""
    return pd.DataFrame(columns=REQUIRED_OUTPUT_COLUMNS)

def create_empty_parameters() -> pd.DataFrame:
    """Create empty parameters DataFrame with correct schema"""
    return pd.DataFrame(columns=REQUIRED_PARAMETER_COLUMNS)

def create_empty_metrics() -> pd.DataFrame:
    """Create empty metrics DataFrame with correct schema"""
    return pd.DataFrame(columns=REQUIRED_METRIC_COLUMNS)
```

**Tests:** Create comprehensive tests for base engine and output validation.

**Acceptance criteria:**
- [ ] SignalEngine ABC enforces required methods
- [ ] Output validation catches missing columns
- [ ] translate_params() works with param_map

---

### Day 4: SignalFit Container

**Files to create:**
- `/home/user/claude-template/tidy_signal/core/signal_fit.py`
- `/home/user/claude-template/tests/test_tidy_signal/test_core/test_signal_fit.py`

**Implementation:** Complete SignalFit class with predict() and extract_outputs() methods that delegate to engines.

**Acceptance criteria:**
- [ ] SignalFit stores spec and fit_data
- [ ] predict() delegates to correct engine
- [ ] extract_outputs() returns three DataFrames
- [ ] All tests pass

---

### Day 5-6: VintageDataFrame xarray Wrapper

**Files to create:**
- `/home/user/claude-template/tidy_signal/data/__init__.py`
- `/home/user/claude-template/tidy_signal/data/vintage.py`
- `/home/user/claude-template/tests/test_tidy_signal/test_data/__init__.py`
- `/home/user/claude-template/tests/test_tidy_signal/test_data/test_vintage.py`

**Implementation:** VintageDataFrame with as_of(), latest(), to_tidy(), from_tidy() methods.

**Acceptance criteria:**
- [ ] as_of() forward-fills correctly
- [ ] latest() returns most recent vintage
- [ ] to_tidy() converts to long-format pandas
- [ ] from_tidy() round-trips correctly
- [ ] Prevents lookahead bias

---

### Day 7-8: SignalBlueprint Alignment Metadata

**Files to create:**
- `/home/user/claude-template/tidy_signal/core/signal_blueprint.py`
- `/home/user/claude-template/tests/test_tidy_signal/test_core/test_signal_blueprint.py`

**Implementation:** SignalBlueprint with validate_new_data() and apply_alignment().

**Acceptance criteria:**
- [ ] Stores alignment metadata
- [ ] validate_new_data() catches schema mismatches
- [ ] apply_alignment() applies vintage selection
- [ ] Extends py-hardhat Blueprint pattern

---

### Day 9: AlignedSignalData Container

**Files to create:**
- `/home/user/claude-template/tidy_signal/data/structures.py`
- `/home/user/claude-template/tests/test_tidy_signal/test_data/test_structures.py`

**Implementation:** AlignedSignalData with compute_divergence().

**Acceptance criteria:**
- [ ] Stores forward and fundamental data
- [ ] compute_divergence() handles standardization
- [ ] Blueprint reference maintained

---

### Day 10: align() Verb Implementation

**Files to create:**
- `/home/user/claude-template/tidy_signal/data/alignment.py`
- `/home/user/claude-template/tidy_signal/verbs/__init__.py`
- `/home/user/claude-template/tidy_signal/verbs/align.py`
- `/home/user/claude-template/tests/test_tidy_signal/test_verbs/__init__.py`
- `/home/user/claude-template/tests/test_tidy_signal/test_verbs/test_align.py`

**Implementation:** align() function with full xarray coordinate handling.

**Acceptance criteria:**
- [ ] Handles all vintage_mode options (as_of, latest, exact)
- [ ] Harmonizes coordinate dtypes
- [ ] Handles ragged-edge data
- [ ] Returns AlignedSignalData with blueprint
- [ ] All edge cases tested

---

## 4. Phases 2-5 Overview

### Phase 2: Statistical Arbitrage (Week 3-4)

**Days 11-20:**
- Stationarity testing (ADF + KPSS)
- Cointegration detection (Johansen, Engle-Granger)
- OU process MLE fitting with diagnostics
- OUProcessEngine implementation
- Full integration tests

**Deliverables:**
- Working OU process engine
- Statistical test suite
- Cointegration pair detection

### Phase 3: Validation Framework (Week 5-6)

**Days 21-28:**
- Performance metrics (Sharpe, IC, drawdown)
- Walk-forward analysis
- backtest() verb with transaction costs
- Integration with py-parsnip models

**Deliverables:**
- Walk-forward validation working
- backtest() returns three DataFrames
- Integration tests with prophet/arima models

### Phase 4: Additional Verbs & Commodities (Week 7-8)

**Days 29-42:**
- detect(), calibrate(), diagnose(), converge() verbs
- Commodity spreads (calendar, crack, crush)
- Seasonal decomposition
- time_entry(), time_exit() optimization

**Deliverables:**
- Complete verb API
- Commodity-specific utilities
- Entry/exit rule optimization

### Phase 5: Polish & Integration (Week 9-12)

**Days 43-60:**
- Comprehensive integration tests
- Documentation (Sphinx + tutorials)
- Performance optimization
- Example notebooks
- User feedback incorporation

**Deliverables:**
- 90%+ test coverage
- Complete documentation
- Tutorial notebooks
- v1.0 MVP release

---

## 5. Integration Test Strategy

### 5.1 py-parsnip Integration Tests

**File:** `tests/test_tidy_signal/test_integration/test_parsnip_integration.py`

**Test scenarios:**
1. prophet_reg model → align() → detect() → calibrate()
2. arima_reg model → align() → detect() → backtest()
3. linear_reg model → align() → walk-forward validation

**Validation:**
- ModelFit.predict() output compatible with align()
- Three-DataFrame outputs consistent format
- No data leakage across train/test splits

### 5.2 Vintage Data Integration Tests

**File:** `tests/test_tidy_signal/test_integration/test_vintage_alignment.py`

**Test scenarios:**
1. as_of() alignment prevents lookahead bias
2. Ragged-edge data handling
3. Multi-index alignment (vintage × observation)

**Validation:**
- No future data in past vintages
- Staleness warnings triggered correctly
- Coordinate harmonization works

### 5.3 End-to-End Workflow Tests

**File:** `tests/test_tidy_signal/test_integration/test_end_to_end.py`

**Test workflows:**
1. Complete pairs trading workflow (cointegration → OU → backtest)
2. Calendar spread workflow (spreads → mean reversion → validate)
3. Multi-signal workflow (combine multiple signals)

**Validation:**
- All verbs chain correctly
- Three-DataFrame outputs at each stage
- Performance metrics reasonable

---

## 6. Quality Gates & Checkpoints

### 6.1 Phase 1 Gate (End of Week 2)

**Requirements:**
- [ ] All Day 1-10 files created
- [ ] All unit tests pass (90%+ coverage)
- [ ] SignalSpec frozen and immutable
- [ ] Registry pattern working
- [ ] VintageDataFrame prevents lookahead bias
- [ ] align() handles all edge cases
- [ ] Documentation strings on all public functions
- [ ] Type hints on all public functions

**Command to verify:**
```bash
source py-tidymodels2/bin/activate
python -m pytest tests/test_tidy_signal/ -v --cov=tidy_signal --cov-report=html
```

**Blocking issues:**
- Test coverage < 90%
- Any test failures
- Missing type hints or docstrings

### 6.2 Phase 2 Gate (End of Week 4)

**Requirements:**
- [ ] OU process MLE fitting working
- [ ] Cointegration tests match statsmodels
- [ ] OUProcessEngine returns three DataFrames
- [ ] Integration test with synthetic cointegrated pairs passes
- [ ] Statistical diagnostics implemented

**Validation benchmarks:**
- OU fitting on 1000 observations < 1 second
- Cointegration test on 100 pairs < 100ms
- Parameters match reference implementations

### 6.3 Phase 3 Gate (End of Week 6)

**Requirements:**
- [ ] Walk-forward analysis working
- [ ] backtest() returns valid three DataFrames
- [ ] Integration with py-parsnip models working
- [ ] IC calculation matches reference

**Validation:**
- Walk-forward on 5 years daily data < 5 seconds
- No lookahead bias in backtests
- Sharpe/IC calculations verified

### 6.4 Phase 4 Gate (End of Week 8)

**Requirements:**
- [ ] All core verbs implemented
- [ ] Commodity spreads working
- [ ] Entry/exit optimization working
- [ ] Example notebooks created

**Validation:**
- All verbs chain in fluent interface
- Spread calculations match industry standards
- Tutorial notebooks run without errors

### 6.5 Phase 5 Gate (End of Week 12 - MVP Release)

**Requirements:**
- [ ] 90%+ test coverage across all modules
- [ ] Complete Sphinx documentation
- [ ] Tutorial notebooks for all workflows
- [ ] Performance benchmarks met
- [ ] Integration tests all passing
- [ ] User feedback incorporated
- [ ] v1.0 release candidate

**Release checklist:**
- [ ] CHANGELOG.md updated
- [ ] Version bumped to 1.0.0
- [ ] PyPI package built and tested
- [ ] GitHub release created
- [ ] Documentation deployed

---

## 7. ChromaDB Integration Opportunities

### 7.1 Signal Specification Storage

**Use case:** Store and retrieve calibrated signal specifications.

```python
import chromadb

# Store calibrated signal
chroma_client = chromadb.Client()
collection = chroma_client.create_collection("signal_specs")

collection.add(
    documents=[signal_fit.spec.to_json()],
    metadatas=[{
        "signal_type": signal_fit.spec.signal_type,
        "commodity": "crude_oil",
        "sharpe_ratio": float(metrics_df['sharpe_ratio'].iloc[0]),
        "calibration_date": "2024-01-01"
    }],
    ids=[f"signal_{uuid.uuid4()}"]
)

# Retrieve similar signals
similar_signals = collection.query(
    query_texts=["crude oil mean reversion signal"],
    n_results=5,
    where={"sharpe_ratio": {"$gt": 1.5}}
)
```

### 7.2 Market Regime Detection

**Use case:** Find similar historical market regimes.

```python
# Store market regime features
collection = chroma_client.create_collection("market_regimes")

regime_description = f"""
Commodity: Crude Oil
Date: 2024-01-01
Volatility: {volatility}
Half-life: {half_life} days
Cointegration strength: {coint_strength}
"""

collection.add(
    documents=[regime_description],
    metadatas={"commodity": "crude_oil", "date": "2024-01-01"},
    ids=["regime_2024_01_01"]
)

# Find similar regimes
similar_regimes = collection.query(
    query_texts=[current_regime_description],
    n_results=10
)
```

### 7.3 Backtest Results Knowledge Base

**Use case:** Build searchable database of backtest results.

```python
# Store backtest results
collection = chroma_client.create_collection("backtest_results")

backtest_summary = f"""
Signal: {spec.signal_type}
Commodity: {commodity}
Period: {start_date} to {end_date}
Sharpe: {sharpe}
Max DD: {max_dd}
Win Rate: {win_rate}
Configuration: {spec.to_json()}
"""

collection.add(
    documents=[backtest_summary],
    metadatas={
        "sharpe_ratio": float(sharpe),
        "commodity": commodity,
        "signal_type": spec.signal_type
    },
    ids=[f"backtest_{uuid.uuid4()}"]
)

# Query for best performing signals
best_signals = collection.query(
    query_texts=["high sharpe ratio crude oil signals"],
    n_results=5,
    where={"sharpe_ratio": {"$gt": 2.0}}
)
```

---

## 8. Risk Mitigation

### 8.1 Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| xarray learning curve | High | Medium | Provide VintageDataFrame wrapper, hide complexity |
| OU fitting numerical instability | Medium | High | Use multiple initial values, validate convergence |
| Performance bottlenecks | Medium | Medium | Profile early, use vectorized operations |
| statsmodels API changes | Low | Medium | Pin versions, comprehensive integration tests |

### 8.2 Implementation Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Scope creep | High | High | Strict MVP focus, defer post-MVP features |
| Test coverage gaps | Medium | High | Tests after every checkpoint, enforce 90% coverage |
| Documentation debt | Medium | Medium | Write docstrings during implementation, not after |
| Integration issues with py-parsnip | Low | High | Integration tests from Day 1, regular validation |

### 8.3 Adoption Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Complex API scares users | Medium | High | Simple "happy path" with sensible defaults |
| Lack of examples | Low | Medium | Tutorial notebooks for each workflow |
| Competition from existing tools | Low | Medium | Focus on unique value: vintage data + commodities |

---

## 9. Post-MVP Roadmap (Phases 6-8)

### Phase 6: Recipes (Weeks 13-16)

**SignalRecipe for reproducible preprocessing:**
- Step-based preprocessing pipeline
- prep() to fit on training data
- bake() to apply to new data
- Recipe serialization

**Key files:**
- `tidy_signal/recipes/signal_recipe.py`
- `tidy_signal/recipes/steps/`

### Phase 7: Workflows (Weeks 17-20)

**SignalWorkflow for production deployment:**
- Bundle recipe + signal specification
- Version control with metadata
- Workflow serialization
- Audit trail integration

**Key files:**
- `tidy_signal/workflows/signal_workflow.py`
- `tidy_signal/workflows/versioning.py`

### Phase 8: Workflowsets (Weeks 21-24)

**WorkflowSet for systematic comparison:**
- Grid-based parameter variation
- cross() method for cross-product analysis
- fit_all() for parallel execution
- rank_by() for metric-based ranking

**Killer use cases:**
- Horizon comparison (min_tenor grid)
- Preprocessing sensitivity analysis
- Model version comparison
- Full cross-product grid search

**Key files:**
- `tidy_signal/workflows/workflow_set.py`
- `tidy_signal/workflows/grid.py`

---

## 10. Success Metrics

### 10.1 Technical Metrics

- [ ] 90%+ test coverage across all modules
- [ ] <100ms cointegration test (100 pairs)
- [ ] <1s OU fitting (1000 observations)
- [ ] <5s walk-forward analysis (5 years daily data)

### 10.2 API Quality Metrics

- [ ] All public functions have type hints
- [ ] All public functions have docstrings with examples
- [ ] 100% of core workflows demonstrated in tutorials
- [ ] Consistent with py-tidymodels patterns

### 10.3 Adoption Metrics

- [ ] Integration with py-parsnip models working
- [ ] Tutorial notebooks for all workflows
- [ ] Production deployment by pilot users
- [ ] Community contributions

---

## Appendix A: File Implementation Templates

### Template 1: Verb Implementation

```python
"""<verb_name>() - <verb_description>"""
from typing import Union, Optional
import pandas as pd
import xarray as xr
from tidy_signal.data.structures import AlignedSignalData
from tidy_signal.exceptions import SignalError

def <verb_name>(
    data: Union[AlignedSignalData, xr.Dataset, pd.DataFrame],
    arg1: type,
    arg2: type = default,
    **kwargs
) -> <return_type>:
    """
    <Verb description>.

    Parameters
    ----------
    data : AlignedSignalData or xr.Dataset or pd.DataFrame
        Input data
    arg1 : type
        <Description>
    arg2 : type, default=<default>
        <Description>
    **kwargs : dict
        Additional arguments

    Returns
    -------
    <return_type>
        <Description>

    Raises
    ------
    SignalError
        If <condition>

    Examples
    --------
    >>> result = <verb_name>(data, arg1=value1)
    """
    # Implementation
    pass
```

### Template 2: Engine Implementation

```python
"""<EngineName> - <engine_description>"""
from typing import Dict, Tuple, Any
import pandas as pd
from tidy_signal.engines.base import SignalEngine
from tidy_signal.core.registry import register_signal_engine
from tidy_signal.core.signal_spec import SignalSpec

@register_signal_engine('<signal_type>', '<engine_name>')
class <EngineName>(SignalEngine):
    """
    <Engine description>.

    Parameters
    ----------
    <param1> : type
        <Description>

    Examples
    --------
    >>> spec = SignalSpec(signal_type='<signal_type>', engine='<engine_name>')
    >>> fit = spec.fit(aligned_data)
    """

    param_map = {
        'tidy_param': 'engine_param'
    }

    def fit(self, spec: SignalSpec, aligned_data: Any) -> Dict[str, Any]:
        """Fit signal model"""
        # Implementation
        pass

    def predict(self, fit_data: Dict[str, Any], new_data: Any) -> pd.DataFrame:
        """Generate signals"""
        # Implementation
        pass

    def extract_outputs(self, fit_data: Dict[str, Any]) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Return three-DataFrame output"""
        # Implementation
        pass
```

### Template 3: Test Suite

```python
"""Tests for <module_name>"""
import pytest
import pandas as pd
import numpy as np
from tidy_signal.<module_path> import <function_or_class>

@pytest.fixture
def sample_data():
    """Create sample data for testing"""
    # Create synthetic test data
    return data

def test_<function_name>_basic():
    """Test basic functionality"""
    result = <function_name>(sample_data)
    assert <condition>

def test_<function_name>_edge_case():
    """Test edge case"""
    # Test edge case
    pass

def test_<function_name>_error_handling():
    """Test error handling"""
    with pytest.raises(<ExceptionType>):
        <function_name>(invalid_data)

def test_<function_name>_output_format():
    """Test output format matches specification"""
    result = <function_name>(sample_data)
    assert isinstance(result, <expected_type>)
    assert set(result.columns) == set(<expected_columns>)
```

---

## Appendix B: Example Integration Test

```python
"""End-to-end integration test: pairs trading workflow"""
import pytest
import pandas as pd
import numpy as np
from py_parsnip import prophet_reg
import tidy_signal as ts

def test_pairs_trading_workflow():
    """Test complete pairs trading workflow"""
    # Create synthetic cointegrated pairs
    np.random.seed(42)
    dates = pd.date_range('2020-01-01', '2023-12-31', freq='D')

    # Generate cointegrated series
    z = np.cumsum(np.random.randn(len(dates)))
    x = z + np.random.randn(len(dates)) * 0.1
    y = 2 * z + 1 + np.random.randn(len(dates)) * 0.1

    forward_data = pd.DataFrame({
        'date': dates,
        'contract_x': x,
        'contract_y': y
    })

    # Train fundamental model (simple mean for testing)
    fundamental_data = pd.DataFrame({
        'date': dates,
        'fundamental_x': np.ones(len(dates)) * x.mean(),
        'fundamental_y': np.ones(len(dates)) * y.mean()
    })

    # Step 1: Detect cointegration
    coint_result = ts.detect_cointegration(
        forward_data,
        contracts=['contract_x', 'contract_y'],
        method='engle_granger'
    )
    assert coint_result.is_cointegrated

    # Step 2: Align data
    vintage_forwards = ts.VintageDataFrame.from_tidy(
        forward_data,
        dims=['vintage_date', 'date', 'contract']
    )

    aligned = ts.align(
        vintage_forwards.latest(),
        fundamental_data,
        by='date',
        how='inner'
    )

    # Step 3: Detect divergence
    divergence = ts.detect(aligned, signal_type='divergence', standardize=True)

    # Step 4: Calibrate OU process
    calibrated = ts.calibrate(divergence, convergence_model='ou_process')

    # Step 5: Diagnose
    diagnostics = ts.diagnose(calibrated, tests=['stationarity'])
    assert diagnostics.is_stationary

    # Step 6: Backtest
    backtest_result = ts.backtest(
        calibrated,
        train_window=252,
        test_window=63,
        transaction_costs=0.002
    )

    # Validate three-DataFrame outputs
    outputs, parameters, metrics = backtest_result.extract_outputs()

    # Check outputs_df structure
    assert 'date' in outputs.columns
    assert 'divergence' in outputs.columns
    assert 'signal_strength' in outputs.columns
    assert 'split' in outputs.columns

    # Check parameters_df structure
    assert 'parameter_name' in parameters.columns
    assert 'value' in parameters.columns
    assert 'lambda_' in parameters['parameter_name'].values
    assert 'mu' in parameters['parameter_name'].values
    assert 'half_life' in parameters['parameter_name'].values

    # Check metrics_df structure
    assert 'sharpe_ratio' in metrics.columns
    assert 'max_drawdown' in metrics.columns
    assert 'win_rate' in metrics.columns

    # Validate metrics are reasonable
    assert metrics['sharpe_ratio'].iloc[0] > -10  # Not absurdly negative
    assert 0 <= metrics['win_rate'].iloc[0] <= 1  # Valid percentage
    assert metrics['max_drawdown'].iloc[0] <= 0   # Drawdown is negative
```

---

**Document Status:** Implementation Ready
**Next Action:** Begin Day 1 implementation (exceptions.py + signal_spec.py)
**Estimated MVP Completion:** March 2026 (12 weeks from start)
