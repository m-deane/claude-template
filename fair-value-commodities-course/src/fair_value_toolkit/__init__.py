"""
Fair Value Toolkit
==================

A comprehensive library for building and validating fair value models
in commodities trading with strict temporal discipline.

Key Components:
- PointInTimeData: Temporal data management with vintage tracking
- FairValueModel: Base class for fair value models
- WalkForwardValidator: Backtesting with proper data vintages
- SignalGenerator: Convert fair value to trading signals

Example:
    >>> from fair_value_toolkit import PointInTimeDataFrame, FairValueModel
    >>> from fair_value_toolkit import WalkForwardValidator, SignalGenerator
    >>>
    >>> # Load data with proper timestamps
    >>> data = PointInTimeDataFrame.from_csv('crude_oil_data.csv')
    >>>
    >>> # Build fair value model
    >>> model = InventoryFairValueModel()
    >>> model.fit(data, as_of_date='2023-01-01')
    >>>
    >>> # Generate signals
    >>> signals = SignalGenerator(model).generate(data)
"""

from .point_in_time import (
    PointInTimeRecord,
    PointInTimeDataFrame,
    PointInTimeDatabase,
)

from .models import (
    FairValueModel,
    InventoryFairValueModel,
    CostOfCarryModel,
    SupplyDemandModel,
    CostCurveModel,
    EnsembleFairValueModel,
)

from .validation import (
    WalkForwardValidator,
    TimeSeriesSplit,
    detect_data_leakage,
    calculate_model_decay,
)

from .signals import (
    SignalGenerator,
    FairValueSignal,
    PositionSizer,
    RiskManager,
)

from .features import (
    TemporalFeatureEngineer,
    create_lagged_features,
    create_rolling_features,
    create_seasonal_features,
)

__version__ = '1.0.0'

__all__ = [
    # Point-in-time data
    'PointInTimeRecord',
    'PointInTimeDataFrame',
    'PointInTimeDatabase',
    # Models
    'FairValueModel',
    'InventoryFairValueModel',
    'CostOfCarryModel',
    'SupplyDemandModel',
    'CostCurveModel',
    'EnsembleFairValueModel',
    # Validation
    'WalkForwardValidator',
    'TimeSeriesSplit',
    'detect_data_leakage',
    'calculate_model_decay',
    # Signals
    'SignalGenerator',
    'FairValueSignal',
    'PositionSizer',
    'RiskManager',
    # Features
    'TemporalFeatureEngineer',
    'create_lagged_features',
    'create_rolling_features',
    'create_seasonal_features',
]
