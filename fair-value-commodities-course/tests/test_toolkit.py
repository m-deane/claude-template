"""
Tests for the Fair Value Toolkit
================================

Run with: pytest tests/test_toolkit.py -v
"""

import pytest
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestPointInTime:
    """Tests for point-in-time data infrastructure."""

    def test_point_in_time_record_creation(self):
        """Test PointInTimeRecord dataclass."""
        from fair_value_toolkit.point_in_time import PointInTimeRecord

        record = PointInTimeRecord(
            series_id='crude_oil',
            observation_date=datetime(2023, 1, 1),
            publication_date=datetime(2023, 1, 5),
            value=75.0,
            revision=0,
            is_final=False,
        )

        assert record.series_id == 'crude_oil'
        assert record.value == 75.0
        assert record.publication_lag_days == 4

    def test_point_in_time_dataframe_as_of(self):
        """Test PointInTimeDataFrame as_of query."""
        from fair_value_toolkit.point_in_time import PointInTimeDataFrame

        # Create sample data
        dates = pd.date_range('2023-01-01', periods=10, freq='D')
        data = pd.DataFrame({
            'price': np.random.randn(10) + 100,
        }, index=dates)

        pit_df = PointInTimeDataFrame(data, observation_dates=dates)

        # Query as of a specific date
        result = pit_df.as_of(datetime(2023, 1, 5))

        assert len(result) <= 5  # Should only have data up to Jan 5

    def test_point_in_time_dataframe_without_leakage(self):
        """Ensure no future data leaks."""
        from fair_value_toolkit.point_in_time import PointInTimeDataFrame

        dates = pd.date_range('2023-01-01', periods=30, freq='D')
        data = pd.DataFrame({
            'price': range(30),  # Sequential values 0-29
        }, index=dates)

        pit_df = PointInTimeDataFrame(data, observation_dates=dates)

        # Query as of Jan 15
        result = pit_df.as_of(datetime(2023, 1, 15))

        # Maximum value should be 14 (day 15, 0-indexed)
        assert result['price'].max() <= 14


class TestFairValueModels:
    """Tests for fair value model classes."""

    @pytest.fixture
    def sample_data(self):
        """Create sample commodity data."""
        np.random.seed(42)
        n = 500

        dates = pd.bdate_range('2020-01-01', periods=n)
        inventory = 100 + np.cumsum(np.random.randn(n) * 2)
        price = 50 - 0.3 * (inventory - 100) + np.random.randn(n) * 5

        data = pd.DataFrame({
            'inventory': inventory,
            'interest_rate': 2 + np.random.randn(n) * 0.5,
        }, index=dates)

        return data, pd.Series(price, index=dates, name='price')

    def test_inventory_model_fit_predict(self, sample_data):
        """Test InventoryFairValueModel fit and predict."""
        from fair_value_toolkit.models import InventoryFairValueModel

        X, y = sample_data

        model = InventoryFairValueModel(inventory_column='inventory')
        model.fit(X, y)

        assert model.is_fitted
        assert 'inventory' in model.feature_names or 'inventory_squared' in model.feature_names

        predictions = model.predict(X)
        assert len(predictions) == len(X)

    def test_inventory_model_evaluation(self, sample_data):
        """Test model evaluation metrics."""
        from fair_value_toolkit.models import InventoryFairValueModel

        X, y = sample_data

        model = InventoryFairValueModel()
        model.fit(X, y)

        metrics = model.evaluate(X, y)

        assert 'mae' in metrics
        assert 'rmse' in metrics
        assert 'r2' in metrics
        assert metrics['r2'] > 0  # Should explain some variance

    def test_cost_of_carry_model(self, sample_data):
        """Test CostOfCarryModel."""
        from fair_value_toolkit.models import CostOfCarryModel

        X, y = sample_data

        model = CostOfCarryModel(rate_column='interest_rate')
        model.fit(X, y)

        assert model.is_fitted
        predictions = model.predict(X)
        assert len(predictions) == len(X)

    def test_supply_demand_model(self, sample_data):
        """Test SupplyDemandModel."""
        from fair_value_toolkit.models import SupplyDemandModel

        X, y = sample_data

        model = SupplyDemandModel(supply_columns=['inventory'])
        model.fit(X, y)

        assert model.is_fitted

    def test_ensemble_model(self, sample_data):
        """Test EnsembleFairValueModel."""
        from fair_value_toolkit.models import (
            InventoryFairValueModel,
            CostOfCarryModel,
            EnsembleFairValueModel,
        )

        X, y = sample_data

        model1 = InventoryFairValueModel()
        model2 = CostOfCarryModel(rate_column='interest_rate')

        ensemble = EnsembleFairValueModel([model1, model2], optimize_weights=True)
        ensemble.fit(X, y)

        assert ensemble.is_fitted
        assert ensemble._optimized_weights is not None
        assert abs(sum(ensemble._optimized_weights) - 1.0) < 0.01

    def test_as_of_date_filtering(self, sample_data):
        """Test that as_of_date properly filters data."""
        from fair_value_toolkit.models import InventoryFairValueModel

        X, y = sample_data

        cutoff = X.index[250]  # Middle of data

        model = InventoryFairValueModel()
        model.fit(X, y, as_of_date=cutoff)

        # Model should only use data up to cutoff
        assert model._fit_metadata['fit_date'] == cutoff


class TestValidation:
    """Tests for walk-forward validation."""

    @pytest.fixture
    def sample_data(self):
        """Create sample data for validation tests."""
        np.random.seed(42)
        n = 1000

        dates = pd.bdate_range('2018-01-01', periods=n)
        X = pd.DataFrame({
            'feature1': np.random.randn(n),
            'feature2': np.random.randn(n),
        }, index=dates)
        y = pd.Series(np.random.randn(n), index=dates, name='target')

        return X, y

    def test_time_series_split_basic(self, sample_data):
        """Test TimeSeriesSplit generates valid folds."""
        from fair_value_toolkit.validation import TimeSeriesSplit

        X, y = sample_data

        splitter = TimeSeriesSplit(
            n_splits=5,
            train_period='1Y',
            test_period='3M',
            gap_period='5D',
        )

        folds = list(splitter.split(X))

        assert len(folds) > 0

        # Check no overlap between train and test
        for train_idx, test_idx in folds:
            assert max(train_idx) < min(test_idx), "Train must come before test"

    def test_time_series_split_gap(self, sample_data):
        """Test that gap period is enforced."""
        from fair_value_toolkit.validation import TimeSeriesSplit

        X, y = sample_data

        splitter = TimeSeriesSplit(
            n_splits=3,
            train_period='6M',
            test_period='1M',
            gap_period='10D',
        )

        folds = splitter.get_folds(X)

        for fold in folds:
            # Gap between train end and test start
            gap = (fold.test_start - fold.train_end).days
            assert gap >= 10, f"Gap should be at least 10 days, got {gap}"

    def test_walk_forward_validator(self, sample_data):
        """Test WalkForwardValidator integration."""
        from fair_value_toolkit.validation import WalkForwardValidator, TimeSeriesSplit
        from fair_value_toolkit.models import InventoryFairValueModel

        X, y = sample_data

        # Use simple features
        X_simple = X.copy()
        X_simple.columns = ['inventory', 'rate']

        splitter = TimeSeriesSplit(n_splits=3, train_period='6M', test_period='2M')
        validator = WalkForwardValidator(splitter=splitter, verbose=False)

        model = InventoryFairValueModel(inventory_column='inventory')
        validator.validate(model, X_simple, y)

        assert len(validator.results_) > 0
        assert validator.summary_ is not None

    def test_data_leakage_detection(self):
        """Test data leakage detection."""
        from fair_value_toolkit.validation import detect_data_leakage

        n = 100
        y = pd.Series(np.random.randn(n))

        # Create a feature with perfect correlation (leakage)
        X = pd.DataFrame({
            'legit_feature': np.random.randn(n),
            'leaking_feature': y + np.random.randn(n) * 0.01,  # Almost perfect
        })

        report = detect_data_leakage(X, y, threshold=0.95)

        assert not report['is_clean'], "Should detect the leaking feature"
        assert len(report['high_correlation_features']) > 0


class TestSignals:
    """Tests for signal generation."""

    @pytest.fixture
    def sample_signals_data(self):
        """Create sample fair value and market price data."""
        np.random.seed(42)
        n = 500

        dates = pd.bdate_range('2020-01-01', periods=n)
        market_price = pd.Series(100 + np.cumsum(np.random.randn(n) * 0.5), index=dates)

        # Fair value = market + noise
        fair_value = market_price + np.random.randn(n) * 2

        fv_df = pd.DataFrame({'fair_value': fair_value}, index=dates)

        return fv_df, market_price

    def test_signal_generator_basic(self, sample_signals_data):
        """Test basic signal generation."""
        from fair_value_toolkit.signals import SignalGenerator

        fv_df, market_price = sample_signals_data

        gen = SignalGenerator(entry_threshold=1.5, exit_threshold=0.5)
        signals = gen.generate(fv_df, market_price)

        assert 'mispricing' in signals.columns
        assert 'mispricing_zscore' in signals.columns
        assert 'signal_direction' in signals.columns
        assert 'signal_strength' in signals.columns

        # Signal direction should be -1, 0, or 1
        assert set(signals['signal_direction'].dropna().unique()).issubset({-1, 0, 1})

    def test_position_sizer(self, sample_signals_data):
        """Test position sizing methods."""
        from fair_value_toolkit.signals import SignalGenerator, PositionSizer

        fv_df, market_price = sample_signals_data

        gen = SignalGenerator()
        signals = gen.generate(fv_df, market_price)

        # Test different sizing methods
        for method in ['equal', 'signal']:
            sizer = PositionSizer(method=method, max_position=0.1)
            positions = sizer.size(signals)

            assert abs(positions).max() <= 0.1, f"Max position exceeded for {method}"

    def test_risk_manager(self, sample_signals_data):
        """Test risk management constraints."""
        from fair_value_toolkit.signals import RiskManager

        rm = RiskManager(
            max_position_single=0.1,
            max_position_total=0.5,
        )

        # Create sample positions
        positions = pd.DataFrame({
            'commodity1': [0.15, 0.2, 0.1],
            'commodity2': [-0.2, 0.3, 0.0],
            'commodity3': [0.1, -0.1, 0.05],
        })

        constrained = rm.apply_constraints(positions)

        # Check single position limit
        assert constrained.abs().max().max() <= 0.1

        # Check total position limit
        assert constrained.abs().sum(axis=1).max() <= 0.5


class TestFeatures:
    """Tests for feature engineering."""

    @pytest.fixture
    def sample_feature_data(self):
        """Create sample data for feature engineering."""
        np.random.seed(42)
        n = 500

        dates = pd.bdate_range('2020-01-01', periods=n)
        data = pd.DataFrame({
            'price': 100 + np.cumsum(np.random.randn(n) * 0.5),
            'inventory': 50 + np.cumsum(np.random.randn(n) * 0.2),
            'production': np.abs(10 + np.random.randn(n)),
            'consumption': np.abs(10 + np.random.randn(n)),
        }, index=dates)

        return data

    def test_temporal_feature_engineer(self, sample_feature_data):
        """Test TemporalFeatureEngineer class."""
        from fair_value_toolkit.features import TemporalFeatureEngineer

        engineer = TemporalFeatureEngineer()
        data = sample_feature_data

        result = engineer.add_lags(data, ['price'], [1, 5, 21])

        assert 'price_lag1' in result.columns
        assert 'price_lag5' in result.columns
        assert 'price_lag21' in result.columns

    def test_rolling_features(self, sample_feature_data):
        """Test rolling feature creation."""
        from fair_value_toolkit.features import TemporalFeatureEngineer

        engineer = TemporalFeatureEngineer()
        data = sample_feature_data

        result = engineer.add_rolling_stats(
            data, ['price'], [5, 21], stats=['mean', 'std']
        )

        assert 'price_roll5_mean' in result.columns
        assert 'price_roll21_std' in result.columns

    def test_returns_features(self, sample_feature_data):
        """Test return calculation."""
        from fair_value_toolkit.features import TemporalFeatureEngineer

        engineer = TemporalFeatureEngineer()
        data = sample_feature_data

        result = engineer.add_returns(data, ['price'], [1, 5])

        assert 'price_return1' in result.columns
        assert 'price_return5' in result.columns

    def test_seasonal_features(self, sample_feature_data):
        """Test seasonal feature extraction."""
        from fair_value_toolkit.features import TemporalFeatureEngineer

        engineer = TemporalFeatureEngineer()
        data = sample_feature_data

        result = engineer.add_seasonal(data, include=['month', 'quarter', 'dayofweek'])

        assert 'month' in result.columns
        assert 'quarter' in result.columns
        assert 'dayofweek' in result.columns

        # Check value ranges
        assert result['month'].min() >= 1
        assert result['month'].max() <= 12
        assert result['quarter'].min() >= 1
        assert result['quarter'].max() <= 4

    def test_create_commodity_features(self, sample_feature_data):
        """Test convenience function for commodity features."""
        from fair_value_toolkit.features import create_commodity_features

        data = sample_feature_data

        result = create_commodity_features(
            data,
            price_column='price',
            inventory_column='inventory',
            production_column='production',
            consumption_column='consumption',
        )

        # Should have many new features
        assert len(result.columns) > len(data.columns) + 10


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
