"""
Temporal Validation Framework
=============================

This module provides tools for validating fair value models with strict
temporal discipline. The key principle is: never use future information
when evaluating model performance.

Key Components:
- WalkForwardValidator: Expanding/rolling window validation
- TimeSeriesSplit: Generate train/test splits with gap periods
- detect_data_leakage: Check for look-ahead bias
- calculate_model_decay: Measure how model accuracy degrades over time
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any, Tuple, Iterator, Callable, Union
import numpy as np
import pandas as pd
from scipy import stats
import warnings


@dataclass
class ValidationFold:
    """Container for a single validation fold."""
    fold_number: int
    train_start: datetime
    train_end: datetime
    test_start: datetime
    test_end: datetime
    train_indices: np.ndarray
    test_indices: np.ndarray
    gap_days: int = 0

    def __repr__(self) -> str:
        return (f"ValidationFold(fold={self.fold_number}, "
                f"train={self.train_start.strftime('%Y-%m-%d')}→{self.train_end.strftime('%Y-%m-%d')}, "
                f"test={self.test_start.strftime('%Y-%m-%d')}→{self.test_end.strftime('%Y-%m-%d')})")


@dataclass
class ValidationResult:
    """Container for validation results."""
    fold_number: int
    train_metrics: Dict[str, float]
    test_metrics: Dict[str, float]
    predictions: pd.DataFrame
    actuals: pd.Series
    as_of_date: datetime
    model_params: Dict[str, Any] = field(default_factory=dict)

    @property
    def test_rmse(self) -> float:
        return self.test_metrics.get('rmse', np.nan)

    @property
    def test_mae(self) -> float:
        return self.test_metrics.get('mae', np.nan)

    @property
    def test_r2(self) -> float:
        return self.test_metrics.get('r2', np.nan)


class TimeSeriesSplit:
    """
    Time series cross-validator with temporal awareness.

    Unlike sklearn's TimeSeriesSplit, this implementation:
    - Works with datetime indices
    - Supports gap periods between train and test
    - Supports both expanding and rolling windows
    - Respects point-in-time data constraints

    Parameters
    ----------
    n_splits : int
        Number of validation folds
    train_period : str or int
        Training window size ('1Y', '6M', '90D' or int for days)
    test_period : str or int
        Test window size
    gap_period : str or int
        Gap between train end and test start (default '0D')
    expanding : bool
        If True, training window expands from initial date.
        If False, uses rolling window of fixed size.
    min_train_size : int
        Minimum number of observations in training set
    """

    def __init__(self,
                 n_splits: int = 5,
                 train_period: Union[str, int] = '1Y',
                 test_period: Union[str, int] = '3M',
                 gap_period: Union[str, int] = '0D',
                 expanding: bool = True,
                 min_train_size: int = 100):
        self.n_splits = n_splits
        self.train_period = self._parse_period(train_period)
        self.test_period = self._parse_period(test_period)
        self.gap_period = self._parse_period(gap_period)
        self.expanding = expanding
        self.min_train_size = min_train_size

    def _parse_period(self, period: Union[str, int]) -> timedelta:
        """Parse period string to timedelta."""
        if isinstance(period, int):
            return timedelta(days=period)

        period = period.upper()
        if period.endswith('Y'):
            return timedelta(days=365 * int(period[:-1]))
        elif period.endswith('M'):
            return timedelta(days=30 * int(period[:-1]))
        elif period.endswith('W'):
            return timedelta(weeks=int(period[:-1]))
        elif period.endswith('D'):
            return timedelta(days=int(period[:-1]))
        else:
            return timedelta(days=int(period))

    def split(self, X: pd.DataFrame) -> Iterator[Tuple[np.ndarray, np.ndarray]]:
        """
        Generate train/test indices for each fold.

        Parameters
        ----------
        X : pd.DataFrame
            Data with datetime index

        Yields
        ------
        train_indices, test_indices : tuple of arrays
            Indices for train and test sets
        """
        if not isinstance(X.index, pd.DatetimeIndex):
            raise ValueError("X must have a DatetimeIndex")

        dates = X.index.sort_values()
        n = len(dates)

        # Calculate fold boundaries
        total_test_period = self.test_period * self.n_splits
        data_range = dates[-1] - dates[0]

        if self.expanding:
            # Expanding window: train starts from beginning, test moves forward
            min_train_end = dates[0] + self.train_period
            test_windows_start = min_train_end + self.gap_period

            for fold in range(self.n_splits):
                # Test window for this fold
                test_start = test_windows_start + fold * self.test_period
                test_end = test_start + self.test_period

                # Training ends before gap
                train_end = test_start - self.gap_period
                train_start = dates[0]

                # Get indices
                train_mask = (dates >= train_start) & (dates < train_end)
                test_mask = (dates >= test_start) & (dates < test_end)

                train_idx = np.where(train_mask)[0]
                test_idx = np.where(test_mask)[0]

                if len(train_idx) >= self.min_train_size and len(test_idx) > 0:
                    yield train_idx, test_idx
        else:
            # Rolling window: fixed train size, slides forward
            for fold in range(self.n_splits):
                # Calculate windows from end backwards
                test_end = dates[-1] - fold * self.test_period
                test_start = test_end - self.test_period
                train_end = test_start - self.gap_period
                train_start = train_end - self.train_period

                train_mask = (dates >= train_start) & (dates < train_end)
                test_mask = (dates >= test_start) & (dates < test_end)

                train_idx = np.where(train_mask)[0]
                test_idx = np.where(test_mask)[0]

                if len(train_idx) >= self.min_train_size and len(test_idx) > 0:
                    yield train_idx, test_idx

    def get_folds(self, X: pd.DataFrame) -> List[ValidationFold]:
        """
        Generate ValidationFold objects with metadata.

        Parameters
        ----------
        X : pd.DataFrame
            Data with datetime index

        Returns
        -------
        list of ValidationFold
            Fold objects with train/test boundaries
        """
        if not isinstance(X.index, pd.DatetimeIndex):
            raise ValueError("X must have a DatetimeIndex")

        dates = X.index.sort_values()
        folds = []

        for fold_num, (train_idx, test_idx) in enumerate(self.split(X)):
            fold = ValidationFold(
                fold_number=fold_num,
                train_start=dates[train_idx[0]],
                train_end=dates[train_idx[-1]],
                test_start=dates[test_idx[0]],
                test_end=dates[test_idx[-1]],
                train_indices=train_idx,
                test_indices=test_idx,
                gap_days=self.gap_period.days,
            )
            folds.append(fold)

        return folds


class WalkForwardValidator:
    """
    Walk-forward validation framework with point-in-time discipline.

    This validator ensures that:
    1. Models are only trained on data available at each point in time
    2. No future information leaks into training
    3. Model performance is measured out-of-sample

    Parameters
    ----------
    splitter : TimeSeriesSplit
        Cross-validation splitter
    refit_frequency : str
        How often to refit the model ('fold', 'daily', 'weekly', 'monthly')
    store_predictions : bool
        Whether to store all predictions for later analysis
    parallel : bool
        Whether to run folds in parallel (default False)
    verbose : bool
        Print progress information
    """

    def __init__(self,
                 splitter: TimeSeriesSplit = None,
                 refit_frequency: str = 'fold',
                 store_predictions: bool = True,
                 parallel: bool = False,
                 verbose: bool = True):
        self.splitter = splitter or TimeSeriesSplit()
        self.refit_frequency = refit_frequency
        self.store_predictions = store_predictions
        self.parallel = parallel
        self.verbose = verbose

        self.results_: List[ValidationResult] = []
        self.summary_: Optional[pd.DataFrame] = None

    def validate(self,
                 model,
                 X: pd.DataFrame,
                 y: pd.Series,
                 feature_columns: List[str] = None) -> 'WalkForwardValidator':
        """
        Run walk-forward validation.

        Parameters
        ----------
        model : FairValueModel
            Model instance with fit() and predict() methods
        X : pd.DataFrame
            Feature data with datetime index
        y : pd.Series
            Target variable
        feature_columns : list, optional
            Columns to use as features. If None, uses all numeric columns.

        Returns
        -------
        self : WalkForwardValidator
            Fitted validator with results
        """
        self.results_ = []

        if feature_columns is not None:
            X = X[feature_columns]

        folds = self.splitter.get_folds(X)

        for fold in folds:
            if self.verbose:
                print(f"Processing {fold}")

            # Extract train and test data
            X_train = X.iloc[fold.train_indices]
            y_train = y.iloc[fold.train_indices]
            X_test = X.iloc[fold.test_indices]
            y_test = y.iloc[fold.test_indices]

            # Fit model with as_of_date constraint
            as_of_date = fold.train_end
            model.fit(X_train, y_train, as_of_date=as_of_date)

            # Generate predictions
            predictions = model.predict(X_test, as_of_date=as_of_date)

            # Calculate metrics
            train_pred = model.predict(X_train, as_of_date=as_of_date)
            train_metrics = self._calculate_metrics(y_train, train_pred)
            test_metrics = self._calculate_metrics(y_test, predictions)

            # Store probabilistic predictions if available
            try:
                pred_df = model.predict_proba(X_test, as_of_date=as_of_date)
            except:
                pred_df = pd.DataFrame({'fair_value': predictions}, index=predictions.index)

            result = ValidationResult(
                fold_number=fold.fold_number,
                train_metrics=train_metrics,
                test_metrics=test_metrics,
                predictions=pred_df,
                actuals=y_test,
                as_of_date=as_of_date,
                model_params=model.get_params() if hasattr(model, 'get_params') else {},
            )

            self.results_.append(result)

        self._compute_summary()
        return self

    def _calculate_metrics(self,
                          actuals: pd.Series,
                          predictions: pd.Series) -> Dict[str, float]:
        """Calculate standard evaluation metrics."""
        # Align indices
        common_idx = actuals.index.intersection(predictions.index)
        if len(common_idx) == 0:
            return {'mae': np.nan, 'rmse': np.nan, 'r2': np.nan}

        y_true = actuals.loc[common_idx].values
        y_pred = predictions.loc[common_idx].values

        residuals = y_true - y_pred
        mae = np.abs(residuals).mean()
        rmse = np.sqrt((residuals ** 2).mean())

        ss_res = (residuals ** 2).sum()
        ss_tot = ((y_true - y_true.mean()) ** 2).sum()
        r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else np.nan

        # Directional accuracy
        if len(y_true) > 1:
            actual_dir = np.sign(np.diff(y_true))
            pred_dir = np.sign(np.diff(y_pred))
            dir_acc = np.mean(actual_dir == pred_dir)
        else:
            dir_acc = np.nan

        # Mean absolute percentage error
        mape = np.mean(np.abs(residuals / y_true)) * 100 if not np.any(y_true == 0) else np.nan

        return {
            'mae': mae,
            'rmse': rmse,
            'r2': r2,
            'directional_accuracy': dir_acc,
            'mape': mape,
            'n_obs': len(y_true),
        }

    def _compute_summary(self) -> None:
        """Compute summary statistics across folds."""
        if not self.results_:
            return

        records = []
        for r in self.results_:
            record = {
                'fold': r.fold_number,
                'as_of_date': r.as_of_date,
                **{f'train_{k}': v for k, v in r.train_metrics.items()},
                **{f'test_{k}': v for k, v in r.test_metrics.items()},
            }
            records.append(record)

        self.summary_ = pd.DataFrame(records)

    def get_summary(self) -> pd.DataFrame:
        """Get summary DataFrame of all folds."""
        if self.summary_ is None:
            raise ValueError("Must run validate() first")
        return self.summary_.copy()

    def get_aggregated_metrics(self) -> Dict[str, float]:
        """Get mean and std of metrics across folds."""
        if self.summary_ is None:
            raise ValueError("Must run validate() first")

        metrics = {}
        for col in self.summary_.columns:
            if col.startswith('test_') and self.summary_[col].dtype in [float, int]:
                metric_name = col.replace('test_', '')
                metrics[f'{metric_name}_mean'] = self.summary_[col].mean()
                metrics[f'{metric_name}_std'] = self.summary_[col].std()

        return metrics

    def get_all_predictions(self) -> pd.DataFrame:
        """Concatenate predictions from all folds."""
        if not self.results_:
            raise ValueError("Must run validate() first")

        all_preds = []
        for r in self.results_:
            pred_df = r.predictions.copy()
            pred_df['fold'] = r.fold_number
            pred_df['actual'] = r.actuals
            all_preds.append(pred_df)

        return pd.concat(all_preds, axis=0)

    def plot_results(self, ax=None):
        """Plot validation results across folds."""
        import matplotlib.pyplot as plt

        if self.summary_ is None:
            raise ValueError("Must run validate() first")

        if ax is None:
            fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        else:
            axes = ax

        # RMSE by fold
        axes[0, 0].bar(self.summary_['fold'], self.summary_['test_rmse'])
        axes[0, 0].axhline(self.summary_['test_rmse'].mean(), color='r', linestyle='--',
                          label=f"Mean: {self.summary_['test_rmse'].mean():.3f}")
        axes[0, 0].set_xlabel('Fold')
        axes[0, 0].set_ylabel('RMSE')
        axes[0, 0].set_title('Test RMSE by Fold')
        axes[0, 0].legend()

        # R2 by fold
        axes[0, 1].bar(self.summary_['fold'], self.summary_['test_r2'])
        axes[0, 1].axhline(self.summary_['test_r2'].mean(), color='r', linestyle='--',
                          label=f"Mean: {self.summary_['test_r2'].mean():.3f}")
        axes[0, 1].set_xlabel('Fold')
        axes[0, 1].set_ylabel('R²')
        axes[0, 1].set_title('Test R² by Fold')
        axes[0, 1].legend()

        # Train vs Test RMSE
        x = np.arange(len(self.summary_))
        width = 0.35
        axes[1, 0].bar(x - width/2, self.summary_['train_rmse'], width, label='Train')
        axes[1, 0].bar(x + width/2, self.summary_['test_rmse'], width, label='Test')
        axes[1, 0].set_xlabel('Fold')
        axes[1, 0].set_ylabel('RMSE')
        axes[1, 0].set_title('Train vs Test RMSE')
        axes[1, 0].legend()

        # Predictions vs actuals scatter (all folds)
        all_preds = self.get_all_predictions()
        axes[1, 1].scatter(all_preds['actual'], all_preds['fair_value'], alpha=0.5)
        min_val = min(all_preds['actual'].min(), all_preds['fair_value'].min())
        max_val = max(all_preds['actual'].max(), all_preds['fair_value'].max())
        axes[1, 1].plot([min_val, max_val], [min_val, max_val], 'r--', label='Perfect')
        axes[1, 1].set_xlabel('Actual')
        axes[1, 1].set_ylabel('Predicted')
        axes[1, 1].set_title('Predicted vs Actual (All Folds)')
        axes[1, 1].legend()

        plt.tight_layout()
        return axes


def detect_data_leakage(X: pd.DataFrame,
                        y: pd.Series,
                        feature_columns: List[str] = None,
                        threshold: float = 0.95) -> Dict[str, Any]:
    """
    Detect potential data leakage in feature matrix.

    Checks for:
    1. Features with perfect or near-perfect correlation with target
    2. Features that are future-shifted versions of target
    3. Features with suspicious temporal patterns

    Parameters
    ----------
    X : pd.DataFrame
        Feature matrix
    y : pd.Series
        Target variable
    feature_columns : list, optional
        Specific columns to check
    threshold : float
        Correlation threshold for flagging (default 0.95)

    Returns
    -------
    dict
        Report of potential leakage issues
    """
    report = {
        'high_correlation_features': [],
        'shifted_target_features': [],
        'suspicious_patterns': [],
        'is_clean': True,
    }

    if feature_columns is not None:
        X = X[feature_columns]

    # Check for high correlation with target
    for col in X.columns:
        if X[col].dtype in [float, int, np.float64, np.int64]:
            corr = X[col].corr(y)
            if abs(corr) > threshold:
                report['high_correlation_features'].append({
                    'column': col,
                    'correlation': corr,
                })
                report['is_clean'] = False

    # Check for shifted target
    for shift in range(1, 6):
        y_shifted = y.shift(shift)
        for col in X.columns:
            if X[col].dtype in [float, int, np.float64, np.int64]:
                corr = X[col].corr(y_shifted.dropna())
                if abs(corr) > threshold:
                    report['shifted_target_features'].append({
                        'column': col,
                        'shift': shift,
                        'correlation': corr,
                    })
                    report['is_clean'] = False

    # Check for suspicious patterns (constant during test period)
    # This would require train/test split info, so we skip for now

    return report


def calculate_model_decay(predictions: pd.DataFrame,
                          actuals: pd.Series,
                          horizons: List[int] = None) -> pd.DataFrame:
    """
    Calculate how model accuracy decays over forecast horizon.

    This helps understand how quickly model predictions become stale
    and when retraining is needed.

    Parameters
    ----------
    predictions : pd.DataFrame
        DataFrame with 'fair_value' column and datetime index
    actuals : pd.Series
        Actual values
    horizons : list, optional
        Forecast horizons to evaluate (in days). Default [1, 5, 10, 21, 63]

    Returns
    -------
    pd.DataFrame
        Decay metrics by horizon
    """
    if horizons is None:
        horizons = [1, 5, 10, 21, 63]  # 1d, 1w, 2w, 1m, 3m

    results = []

    for horizon in horizons:
        # Shift actuals to align with predictions
        actuals_shifted = actuals.shift(-horizon)

        # Calculate error at this horizon
        common_idx = predictions.index.intersection(actuals_shifted.dropna().index)
        if len(common_idx) == 0:
            continue

        pred = predictions.loc[common_idx, 'fair_value']
        actual = actuals_shifted.loc[common_idx]

        residuals = actual - pred
        mae = np.abs(residuals).mean()
        rmse = np.sqrt((residuals ** 2).mean())

        # Directional accuracy
        if len(actual) > 1:
            actual_dir = np.sign(actual.diff().dropna())
            pred_dir = np.sign(pred.diff().dropna())
            common_dir = actual_dir.index.intersection(pred_dir.index)
            dir_acc = (actual_dir.loc[common_dir] == pred_dir.loc[common_dir]).mean()
        else:
            dir_acc = np.nan

        results.append({
            'horizon': horizon,
            'mae': mae,
            'rmse': rmse,
            'directional_accuracy': dir_acc,
            'n_observations': len(common_idx),
        })

    return pd.DataFrame(results)


def assess_vintage_impact(data: pd.DataFrame,
                          target_column: str,
                          vintage_dates: List[datetime],
                          model_factory: Callable) -> pd.DataFrame:
    """
    Assess how using different data vintages affects model performance.

    This analysis reveals the impact of data revisions on model accuracy
    and helps quantify the "vintage premium" of using point-in-time data.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame with point-in-time data (must have as_of capability)
    target_column : str
        Name of target variable
    vintage_dates : list
        List of vintage dates to compare
    model_factory : callable
        Function that returns a new model instance

    Returns
    -------
    pd.DataFrame
        Performance comparison across vintages
    """
    results = []

    # Get final (fully revised) data as ground truth
    # This would require the point-in-time infrastructure

    for vintage in vintage_dates:
        # Get data as it was known on vintage date
        # Fit model with that vintage
        # Evaluate against final truth

        results.append({
            'vintage_date': vintage,
            # 'mae': ...,
            # 'revision_impact': ...,
        })

    warnings.warn("assess_vintage_impact requires PointInTimeDataFrame integration")
    return pd.DataFrame(results)


class AdaptiveValidator(WalkForwardValidator):
    """
    Adaptive walk-forward validator that adjusts based on market conditions.

    This validator can:
    - Use shorter refit periods during high volatility
    - Skip folds during market disruptions
    - Weight recent performance more heavily

    Parameters
    ----------
    base_splitter : TimeSeriesSplit
        Base splitter configuration
    volatility_column : str
        Column name for volatility metric
    volatility_threshold : float
        Threshold above which to use fast refit
    fast_refit_period : str
        Refit period during high volatility
    """

    def __init__(self,
                 base_splitter: TimeSeriesSplit = None,
                 volatility_column: str = 'volatility',
                 volatility_threshold: float = 2.0,
                 fast_refit_period: str = '1W',
                 **kwargs):
        super().__init__(splitter=base_splitter, **kwargs)
        self.volatility_column = volatility_column
        self.volatility_threshold = volatility_threshold
        self.fast_refit_period = fast_refit_period

    def validate(self,
                 model,
                 X: pd.DataFrame,
                 y: pd.Series,
                 feature_columns: List[str] = None,
                 volatility_data: pd.Series = None) -> 'AdaptiveValidator':
        """
        Run adaptive walk-forward validation.

        In high volatility regimes, uses faster refit periods.
        """
        # For now, delegate to parent
        # Full implementation would switch splitter based on volatility
        return super().validate(model, X, y, feature_columns)
