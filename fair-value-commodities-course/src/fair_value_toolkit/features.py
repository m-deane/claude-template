"""
Temporal Feature Engineering
============================

This module provides tools for creating features from time series data
while maintaining strict temporal discipline. The key principle is:
features must only use data available at the time of prediction.

Key Components:
- TemporalFeatureEngineer: Main feature engineering class
- create_lagged_features: Create time-lagged versions of variables
- create_rolling_features: Calculate rolling statistics
- create_seasonal_features: Extract seasonal patterns
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any, Tuple, Union, Callable
import numpy as np
import pandas as pd
from scipy import stats
import warnings


@dataclass
class FeatureMetadata:
    """Metadata about an engineered feature."""
    name: str
    source_column: str
    feature_type: str  # 'lag', 'rolling', 'seasonal', 'interaction', 'custom'
    lookback_periods: int
    creation_date: datetime = field(default_factory=datetime.now)
    description: str = ''
    safe_for_realtime: bool = True

    def __repr__(self) -> str:
        return f"Feature({self.name}, type={self.feature_type}, lookback={self.lookback_periods})"


class TemporalFeatureEngineer:
    """
    Feature engineering with temporal discipline.

    This class ensures that all engineered features:
    1. Only use past data (no look-ahead bias)
    2. Have consistent calculation across train/test
    3. Are documented with their temporal properties

    Parameters
    ----------
    date_column : str
        Name of the date column (if not using index)
    target_column : str
        Name of the target variable (for supervised features)
    fill_method : str
        How to fill missing values ('ffill', 'bfill', 'zero', 'drop')
    """

    def __init__(self,
                 date_column: Optional[str] = None,
                 target_column: Optional[str] = None,
                 fill_method: str = 'ffill'):
        self.date_column = date_column
        self.target_column = target_column
        self.fill_method = fill_method

        self._features: Dict[str, FeatureMetadata] = {}
        self._fitted = False
        self._fit_columns: List[str] = []
        self._rolling_stats: Dict[str, Dict[str, float]] = {}

    def fit(self, X: pd.DataFrame) -> 'TemporalFeatureEngineer':
        """
        Fit the feature engineer on training data.

        Stores statistics needed for normalization and rolling calculations.

        Parameters
        ----------
        X : pd.DataFrame
            Training data

        Returns
        -------
        self
        """
        self._fit_columns = list(X.columns)

        # Store rolling statistics for each numeric column
        for col in X.select_dtypes(include=[np.number]).columns:
            self._rolling_stats[col] = {
                'mean': X[col].mean(),
                'std': X[col].std(),
                'min': X[col].min(),
                'max': X[col].max(),
            }

        self._fitted = True
        return self

    def transform(self,
                  X: pd.DataFrame,
                  as_of_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        Transform data by adding engineered features.

        Parameters
        ----------
        X : pd.DataFrame
            Data to transform
        as_of_date : datetime, optional
            Point-in-time cutoff for calculations

        Returns
        -------
        pd.DataFrame
            Data with engineered features
        """
        result = X.copy()

        # Apply point-in-time filter
        if as_of_date is not None:
            if isinstance(result.index, pd.DatetimeIndex):
                result = result.loc[result.index <= as_of_date]

        # Handle missing values
        if self.fill_method == 'ffill':
            result = result.ffill()
        elif self.fill_method == 'bfill':
            result = result.bfill()
        elif self.fill_method == 'zero':
            result = result.fillna(0)

        return result

    def fit_transform(self,
                      X: pd.DataFrame,
                      as_of_date: Optional[datetime] = None) -> pd.DataFrame:
        """Fit and transform in one step."""
        return self.fit(X).transform(X, as_of_date)

    def add_lags(self,
                 X: pd.DataFrame,
                 columns: List[str],
                 lags: List[int],
                 drop_original: bool = False) -> pd.DataFrame:
        """
        Add lagged features to DataFrame.

        Parameters
        ----------
        X : pd.DataFrame
            Input data
        columns : list
            Columns to create lags for
        lags : list
            Lag periods (positive integers)
        drop_original : bool
            Whether to drop original columns

        Returns
        -------
        pd.DataFrame
            Data with lag features
        """
        result = X.copy()

        for col in columns:
            if col not in X.columns:
                warnings.warn(f"Column {col} not found in data")
                continue

            for lag in lags:
                lag_name = f"{col}_lag{lag}"
                result[lag_name] = X[col].shift(lag)

                # Register feature
                self._features[lag_name] = FeatureMetadata(
                    name=lag_name,
                    source_column=col,
                    feature_type='lag',
                    lookback_periods=lag,
                    description=f"{lag}-period lag of {col}",
                )

        if drop_original:
            result = result.drop(columns=columns)

        return result

    def add_rolling_stats(self,
                          X: pd.DataFrame,
                          columns: List[str],
                          windows: List[int],
                          stats: List[str] = None) -> pd.DataFrame:
        """
        Add rolling statistics features.

        Parameters
        ----------
        X : pd.DataFrame
            Input data
        columns : list
            Columns to calculate rolling stats for
        windows : list
            Window sizes in periods
        stats : list
            Statistics to calculate ('mean', 'std', 'min', 'max', 'sum', 'skew')

        Returns
        -------
        pd.DataFrame
            Data with rolling features
        """
        if stats is None:
            stats = ['mean', 'std']

        result = X.copy()

        for col in columns:
            if col not in X.columns:
                continue

            for window in windows:
                rolling = X[col].rolling(window=window, min_periods=1)

                for stat in stats:
                    feat_name = f"{col}_roll{window}_{stat}"

                    if stat == 'mean':
                        result[feat_name] = rolling.mean()
                    elif stat == 'std':
                        result[feat_name] = rolling.std()
                    elif stat == 'min':
                        result[feat_name] = rolling.min()
                    elif stat == 'max':
                        result[feat_name] = rolling.max()
                    elif stat == 'sum':
                        result[feat_name] = rolling.sum()
                    elif stat == 'skew':
                        result[feat_name] = rolling.skew()

                    self._features[feat_name] = FeatureMetadata(
                        name=feat_name,
                        source_column=col,
                        feature_type='rolling',
                        lookback_periods=window,
                        description=f"{window}-period rolling {stat} of {col}",
                    )

        return result

    def add_returns(self,
                    X: pd.DataFrame,
                    columns: List[str],
                    periods: List[int] = None,
                    log_return: bool = False) -> pd.DataFrame:
        """
        Add return features.

        Parameters
        ----------
        X : pd.DataFrame
            Input data
        columns : list
            Price columns to calculate returns for
        periods : list
            Return periods (default [1, 5, 21])
        log_return : bool
            Use log returns instead of simple returns

        Returns
        -------
        pd.DataFrame
            Data with return features
        """
        if periods is None:
            periods = [1, 5, 21]

        result = X.copy()
        return_type = 'log' if log_return else 'simple'

        for col in columns:
            if col not in X.columns:
                continue

            for period in periods:
                feat_name = f"{col}_return{period}{'_log' if log_return else ''}"

                if log_return:
                    result[feat_name] = np.log(X[col] / X[col].shift(period))
                else:
                    result[feat_name] = X[col].pct_change(periods=period)

                self._features[feat_name] = FeatureMetadata(
                    name=feat_name,
                    source_column=col,
                    feature_type='return',
                    lookback_periods=period,
                    description=f"{period}-period {return_type} return of {col}",
                )

        return result

    def add_volatility(self,
                       X: pd.DataFrame,
                       columns: List[str],
                       windows: List[int] = None,
                       method: str = 'std') -> pd.DataFrame:
        """
        Add volatility features.

        Parameters
        ----------
        X : pd.DataFrame
            Input data
        columns : list
            Price columns to calculate volatility for
        windows : list
            Volatility windows (default [5, 21, 63])
        method : str
            'std' for standard deviation, 'parkinson' for Parkinson estimator

        Returns
        -------
        pd.DataFrame
            Data with volatility features
        """
        if windows is None:
            windows = [5, 21, 63]

        result = X.copy()

        for col in columns:
            if col not in X.columns:
                continue

            # First calculate returns
            returns = X[col].pct_change()

            for window in windows:
                feat_name = f"{col}_vol{window}"

                if method == 'std':
                    result[feat_name] = returns.rolling(window=window, min_periods=1).std() * np.sqrt(252)
                elif method == 'parkinson':
                    # Parkinson estimator requires high/low data
                    warnings.warn("Parkinson estimator requires high/low columns, using std")
                    result[feat_name] = returns.rolling(window=window, min_periods=1).std() * np.sqrt(252)

                self._features[feat_name] = FeatureMetadata(
                    name=feat_name,
                    source_column=col,
                    feature_type='volatility',
                    lookback_periods=window,
                    description=f"{window}-period annualized volatility of {col}",
                )

        return result

    def add_zscore(self,
                   X: pd.DataFrame,
                   columns: List[str],
                   windows: List[int] = None) -> pd.DataFrame:
        """
        Add z-score features (standardized deviation from rolling mean).

        Parameters
        ----------
        X : pd.DataFrame
            Input data
        columns : list
            Columns to calculate z-scores for
        windows : list
            Lookback windows for mean/std (default [21, 63, 252])

        Returns
        -------
        pd.DataFrame
            Data with z-score features
        """
        if windows is None:
            windows = [21, 63, 252]

        result = X.copy()

        for col in columns:
            if col not in X.columns:
                continue

            for window in windows:
                feat_name = f"{col}_zscore{window}"

                rolling_mean = X[col].rolling(window=window, min_periods=1).mean()
                rolling_std = X[col].rolling(window=window, min_periods=1).std()

                result[feat_name] = (X[col] - rolling_mean) / rolling_std
                result[feat_name] = result[feat_name].replace([np.inf, -np.inf], np.nan)

                self._features[feat_name] = FeatureMetadata(
                    name=feat_name,
                    source_column=col,
                    feature_type='zscore',
                    lookback_periods=window,
                    description=f"{window}-period z-score of {col}",
                )

        return result

    def add_seasonal(self,
                     X: pd.DataFrame,
                     include: List[str] = None) -> pd.DataFrame:
        """
        Add seasonal features from datetime index.

        Parameters
        ----------
        X : pd.DataFrame
            Input data with datetime index
        include : list
            Features to include ('month', 'quarter', 'dayofweek', 'weekofyear',
            'dayofyear', 'is_month_end', 'is_quarter_end')

        Returns
        -------
        pd.DataFrame
            Data with seasonal features
        """
        if include is None:
            include = ['month', 'quarter', 'dayofweek']

        result = X.copy()

        # Get datetime index
        if isinstance(result.index, pd.DatetimeIndex):
            dt = result.index
        elif self.date_column and self.date_column in result.columns:
            dt = pd.to_datetime(result[self.date_column])
        else:
            warnings.warn("No datetime index or date column found")
            return result

        for feat in include:
            if feat == 'month':
                result['month'] = dt.month
            elif feat == 'quarter':
                result['quarter'] = dt.quarter
            elif feat == 'dayofweek':
                result['dayofweek'] = dt.dayofweek
            elif feat == 'weekofyear':
                result['weekofyear'] = dt.isocalendar().week.astype(int)
            elif feat == 'dayofyear':
                result['dayofyear'] = dt.dayofyear
            elif feat == 'is_month_end':
                result['is_month_end'] = dt.is_month_end.astype(int)
            elif feat == 'is_quarter_end':
                result['is_quarter_end'] = dt.is_quarter_end.astype(int)

            if feat in result.columns:
                self._features[feat] = FeatureMetadata(
                    name=feat,
                    source_column='date',
                    feature_type='seasonal',
                    lookback_periods=0,
                    description=f"Seasonal feature: {feat}",
                )

        return result

    def add_interactions(self,
                         X: pd.DataFrame,
                         interactions: List[Tuple[str, str]],
                         operation: str = 'multiply') -> pd.DataFrame:
        """
        Add interaction features between columns.

        Parameters
        ----------
        X : pd.DataFrame
            Input data
        interactions : list of tuples
            Pairs of columns to create interactions for
        operation : str
            'multiply', 'add', 'subtract', 'ratio'

        Returns
        -------
        pd.DataFrame
            Data with interaction features
        """
        result = X.copy()

        for col1, col2 in interactions:
            if col1 not in X.columns or col2 not in X.columns:
                continue

            feat_name = f"{col1}_x_{col2}" if operation == 'multiply' else f"{col1}_{operation}_{col2}"

            if operation == 'multiply':
                result[feat_name] = X[col1] * X[col2]
            elif operation == 'add':
                result[feat_name] = X[col1] + X[col2]
            elif operation == 'subtract':
                result[feat_name] = X[col1] - X[col2]
            elif operation == 'ratio':
                result[feat_name] = X[col1] / X[col2].replace(0, np.nan)

            self._features[feat_name] = FeatureMetadata(
                name=feat_name,
                source_column=f"{col1}, {col2}",
                feature_type='interaction',
                lookback_periods=0,
                description=f"Interaction: {col1} {operation} {col2}",
            )

        return result

    def add_relative_strength(self,
                              X: pd.DataFrame,
                              column: str,
                              benchmark_column: str,
                              windows: List[int] = None) -> pd.DataFrame:
        """
        Add relative strength features (column performance vs benchmark).

        Parameters
        ----------
        X : pd.DataFrame
            Input data
        column : str
            Column to calculate relative strength for
        benchmark_column : str
            Benchmark column for comparison
        windows : list
            Windows for relative strength calculation

        Returns
        -------
        pd.DataFrame
            Data with relative strength features
        """
        if windows is None:
            windows = [21, 63]

        result = X.copy()

        if column not in X.columns or benchmark_column not in X.columns:
            return result

        for window in windows:
            feat_name = f"{column}_rs_{benchmark_column}_{window}"

            col_return = X[column].pct_change(periods=window)
            bench_return = X[benchmark_column].pct_change(periods=window)

            result[feat_name] = col_return - bench_return

            self._features[feat_name] = FeatureMetadata(
                name=feat_name,
                source_column=f"{column}, {benchmark_column}",
                feature_type='relative_strength',
                lookback_periods=window,
                description=f"{window}-period relative strength of {column} vs {benchmark_column}",
            )

        return result

    def get_feature_info(self) -> pd.DataFrame:
        """Get information about all registered features."""
        records = [
            {
                'name': f.name,
                'source': f.source_column,
                'type': f.feature_type,
                'lookback': f.lookback_periods,
                'description': f.description,
            }
            for f in self._features.values()
        ]
        return pd.DataFrame(records)

    def get_max_lookback(self) -> int:
        """Get maximum lookback period across all features."""
        if not self._features:
            return 0
        return max(f.lookback_periods for f in self._features.values())


def create_lagged_features(data: pd.DataFrame,
                           columns: List[str],
                           lags: List[int]) -> pd.DataFrame:
    """
    Convenience function to create lagged features.

    Parameters
    ----------
    data : pd.DataFrame
        Input data
    columns : list
        Columns to lag
    lags : list
        Lag periods

    Returns
    -------
    pd.DataFrame
        Data with lag features
    """
    engineer = TemporalFeatureEngineer()
    return engineer.add_lags(data, columns, lags)


def create_rolling_features(data: pd.DataFrame,
                            columns: List[str],
                            windows: List[int],
                            stats: List[str] = None) -> pd.DataFrame:
    """
    Convenience function to create rolling statistical features.

    Parameters
    ----------
    data : pd.DataFrame
        Input data
    columns : list
        Columns to calculate rolling stats for
    windows : list
        Window sizes
    stats : list
        Statistics to calculate

    Returns
    -------
    pd.DataFrame
        Data with rolling features
    """
    engineer = TemporalFeatureEngineer()
    return engineer.add_rolling_stats(data, columns, windows, stats)


def create_seasonal_features(data: pd.DataFrame,
                              include: List[str] = None) -> pd.DataFrame:
    """
    Convenience function to create seasonal features.

    Parameters
    ----------
    data : pd.DataFrame
        Input data with datetime index
    include : list
        Seasonal features to include

    Returns
    -------
    pd.DataFrame
        Data with seasonal features
    """
    engineer = TemporalFeatureEngineer()
    return engineer.add_seasonal(data, include)


def create_commodity_features(data: pd.DataFrame,
                              price_column: str,
                              inventory_column: Optional[str] = None,
                              production_column: Optional[str] = None,
                              consumption_column: Optional[str] = None) -> pd.DataFrame:
    """
    Create a standard set of features for commodity analysis.

    Parameters
    ----------
    data : pd.DataFrame
        Input data with datetime index
    price_column : str
        Name of price column
    inventory_column : str, optional
        Name of inventory column
    production_column : str, optional
        Name of production column
    consumption_column : str, optional
        Name of consumption column

    Returns
    -------
    pd.DataFrame
        Data with commodity features
    """
    engineer = TemporalFeatureEngineer()
    result = data.copy()

    # Price-based features
    result = engineer.add_returns(result, [price_column], [1, 5, 21, 63])
    result = engineer.add_volatility(result, [price_column], [5, 21, 63])
    result = engineer.add_zscore(result, [price_column], [21, 63, 252])
    result = engineer.add_rolling_stats(result, [price_column], [5, 21], ['mean', 'std', 'min', 'max'])

    # Inventory features
    if inventory_column and inventory_column in data.columns:
        result = engineer.add_lags(result, [inventory_column], [1, 5, 10])
        result = engineer.add_rolling_stats(result, [inventory_column], [4, 12], ['mean', 'std'])
        result = engineer.add_zscore(result, [inventory_column], [12, 52])

        # Inventory change
        result[f'{inventory_column}_change'] = data[inventory_column].diff()
        result[f'{inventory_column}_change_pct'] = data[inventory_column].pct_change()

    # Supply-demand balance
    if production_column and consumption_column:
        if production_column in data.columns and consumption_column in data.columns:
            result['supply_demand_balance'] = data[production_column] - data[consumption_column]
            result = engineer.add_rolling_stats(result, ['supply_demand_balance'], [4, 12], ['mean', 'sum'])

    # Seasonal features
    result = engineer.add_seasonal(result, ['month', 'quarter'])

    return result
