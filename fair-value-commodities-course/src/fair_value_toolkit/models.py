"""
Fair Value Models for Commodities
=================================

This module provides various fair value model implementations for commodity
price analysis. Each model encodes different economic theories about what
drives commodity prices.

Key Models:
- InventoryFairValueModel: Based on storage theory (Kaldor, Working)
- CostOfCarryModel: Based on storage costs and convenience yield
- SupplyDemandModel: Based on fundamental supply/demand balance
- CostCurveModel: Based on marginal cost of production
- EnsembleFairValueModel: Combines multiple models with weights
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, List, Any, Tuple, Union
import numpy as np
import pandas as pd
from scipy import optimize
from sklearn.linear_model import LinearRegression, Ridge, ElasticNet
from sklearn.preprocessing import StandardScaler
import warnings


@dataclass
class FairValueResult:
    """Container for fair value model output."""
    fair_value: float
    confidence_interval: Tuple[float, float]
    model_name: str
    as_of_date: datetime
    components: Dict[str, float] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def lower_bound(self) -> float:
        return self.confidence_interval[0]

    @property
    def upper_bound(self) -> float:
        return self.confidence_interval[1]

    def to_dict(self) -> Dict[str, Any]:
        return {
            'fair_value': self.fair_value,
            'lower_bound': self.lower_bound,
            'upper_bound': self.upper_bound,
            'model_name': self.model_name,
            'as_of_date': self.as_of_date,
            'components': self.components,
            'metadata': self.metadata,
        }


class FairValueModel(ABC):
    """
    Abstract base class for fair value models.

    All fair value models must implement:
    - fit(): Train the model on historical data
    - predict(): Generate fair value estimates
    - predict_proba(): Generate probabilistic forecasts

    Models maintain temporal discipline by accepting an as_of_date parameter
    that restricts data to what was known at that point in time.
    """

    def __init__(self, name: str = None):
        self.name = name or self.__class__.__name__
        self.is_fitted = False
        self.fit_date: Optional[datetime] = None
        self.feature_names: List[str] = []
        self.target_name: str = ''
        self._model_params: Dict[str, Any] = {}
        self._fit_metadata: Dict[str, Any] = {}

    @abstractmethod
    def fit(self,
            X: pd.DataFrame,
            y: pd.Series,
            as_of_date: Optional[datetime] = None) -> 'FairValueModel':
        """
        Fit the model to training data.

        Parameters
        ----------
        X : pd.DataFrame
            Feature matrix with datetime index
        y : pd.Series
            Target variable (typically price)
        as_of_date : datetime, optional
            Restrict data to what was known as of this date

        Returns
        -------
        self : FairValueModel
            Fitted model instance
        """
        pass

    @abstractmethod
    def predict(self,
                X: pd.DataFrame,
                as_of_date: Optional[datetime] = None) -> pd.Series:
        """
        Generate point estimates of fair value.

        Parameters
        ----------
        X : pd.DataFrame
            Feature matrix for prediction
        as_of_date : datetime, optional
            Point-in-time for data filtering

        Returns
        -------
        pd.Series
            Fair value estimates
        """
        pass

    def predict_proba(self,
                      X: pd.DataFrame,
                      confidence: float = 0.95,
                      as_of_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        Generate probabilistic forecasts with confidence intervals.

        Parameters
        ----------
        X : pd.DataFrame
            Feature matrix for prediction
        confidence : float
            Confidence level (default 0.95)
        as_of_date : datetime, optional
            Point-in-time for data filtering

        Returns
        -------
        pd.DataFrame
            DataFrame with columns: fair_value, lower, upper
        """
        point_estimate = self.predict(X, as_of_date)

        # Default implementation: use residual standard error
        if hasattr(self, '_residual_std') and self._residual_std is not None:
            from scipy import stats
            z = stats.norm.ppf((1 + confidence) / 2)
            margin = z * self._residual_std

            return pd.DataFrame({
                'fair_value': point_estimate,
                'lower': point_estimate - margin,
                'upper': point_estimate + margin,
            }, index=point_estimate.index)
        else:
            return pd.DataFrame({
                'fair_value': point_estimate,
                'lower': np.nan,
                'upper': np.nan,
            }, index=point_estimate.index)

    def evaluate(self,
                 X: pd.DataFrame,
                 y: pd.Series,
                 as_of_date: Optional[datetime] = None) -> Dict[str, float]:
        """
        Evaluate model performance on test data.

        Returns
        -------
        dict
            Performance metrics including MAE, RMSE, R2, directional accuracy
        """
        predictions = self.predict(X, as_of_date)

        # Align indices
        common_idx = predictions.index.intersection(y.index)
        pred = predictions.loc[common_idx]
        actual = y.loc[common_idx]

        # Basic metrics
        residuals = actual - pred
        mae = np.abs(residuals).mean()
        rmse = np.sqrt((residuals ** 2).mean())
        ss_res = (residuals ** 2).sum()
        ss_tot = ((actual - actual.mean()) ** 2).sum()
        r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else np.nan

        # Directional accuracy
        if len(actual) > 1:
            actual_dir = np.sign(actual.diff().dropna())
            pred_dir = np.sign(pred.diff().dropna())
            common_dir_idx = actual_dir.index.intersection(pred_dir.index)
            if len(common_dir_idx) > 0:
                dir_accuracy = (actual_dir.loc[common_dir_idx] == pred_dir.loc[common_dir_idx]).mean()
            else:
                dir_accuracy = np.nan
        else:
            dir_accuracy = np.nan

        # Information coefficient (rank correlation)
        from scipy.stats import spearmanr
        if len(pred) > 2:
            ic, ic_pval = spearmanr(actual, pred)
        else:
            ic, ic_pval = np.nan, np.nan

        return {
            'mae': mae,
            'rmse': rmse,
            'r2': r2,
            'directional_accuracy': dir_accuracy,
            'information_coefficient': ic,
            'ic_pvalue': ic_pval,
            'n_observations': len(pred),
        }

    def get_fair_value_result(self,
                              X: pd.DataFrame,
                              row_idx: int = -1,
                              confidence: float = 0.95,
                              as_of_date: Optional[datetime] = None) -> FairValueResult:
        """
        Get a structured fair value result for a specific observation.
        """
        proba = self.predict_proba(X, confidence, as_of_date)

        row = proba.iloc[row_idx]
        result_date = proba.index[row_idx] if hasattr(proba.index[row_idx], 'strftime') else datetime.now()

        return FairValueResult(
            fair_value=row['fair_value'],
            confidence_interval=(row['lower'], row['upper']),
            model_name=self.name,
            as_of_date=as_of_date or datetime.now(),
            components=self._get_components(X.iloc[[row_idx]]),
            metadata=self._fit_metadata.copy(),
        )

    def _get_components(self, X: pd.DataFrame) -> Dict[str, float]:
        """Override in subclasses to provide fair value decomposition."""
        return {}

    def get_params(self) -> Dict[str, Any]:
        """Get model parameters."""
        return self._model_params.copy()

    def set_params(self, **params) -> 'FairValueModel':
        """Set model parameters."""
        self._model_params.update(params)
        return self


class InventoryFairValueModel(FairValueModel):
    """
    Fair value model based on inventory/storage theory.

    Economic Foundation:
    Storage theory (Kaldor 1939, Working 1949) suggests that commodity prices
    should reflect storage costs minus convenience yield. When inventories are
    low, convenience yield is high (backwardation). When inventories are high,
    storage costs dominate (contango).

    Model Specification:
        Fair Value = alpha + beta_inv * inventory_zscore + beta_trend * trend + ...

    Where:
    - inventory_zscore: Standardized inventory deviation from seasonal norm
    - Coefficients reflect marginal price impact of inventory changes

    Parameters
    ----------
    inventory_column : str
        Name of the inventory feature column
    normalize : bool
        Whether to standardize features (default True)
    include_squared : bool
        Include squared inventory term for non-linearity (default True)
    """

    def __init__(self,
                 inventory_column: str = 'inventory',
                 normalize: bool = True,
                 include_squared: bool = True,
                 regularization: float = 0.0,
                 name: str = None):
        super().__init__(name or 'InventoryFairValue')
        self.inventory_column = inventory_column
        self.normalize = normalize
        self.include_squared = include_squared
        self.regularization = regularization

        self._scaler: Optional[StandardScaler] = None
        self._model: Optional[LinearRegression] = None
        self._residual_std: Optional[float] = None
        self._coefficients: Dict[str, float] = {}

    def fit(self,
            X: pd.DataFrame,
            y: pd.Series,
            as_of_date: Optional[datetime] = None) -> 'InventoryFairValueModel':
        """Fit inventory-based fair value model."""

        # Apply point-in-time filter
        if as_of_date is not None:
            if hasattr(X.index, 'tz'):
                as_of_date = pd.Timestamp(as_of_date).tz_localize(X.index.tz)
            mask = X.index <= as_of_date
            X = X.loc[mask]
            y = y.loc[mask]

        if len(X) == 0:
            raise ValueError("No data available for fitting after as_of_date filter")

        # Prepare features
        X_features = self._prepare_features(X, fit=True)

        # Align target
        common_idx = X_features.index.intersection(y.index)
        X_features = X_features.loc[common_idx]
        y_aligned = y.loc[common_idx]

        # Fit model
        if self.regularization > 0:
            self._model = Ridge(alpha=self.regularization)
        else:
            self._model = LinearRegression()

        self._model.fit(X_features.values, y_aligned.values)

        # Store metadata
        self.feature_names = list(X_features.columns)
        self.target_name = y.name or 'price'
        self._coefficients = dict(zip(self.feature_names, self._model.coef_))
        self._coefficients['intercept'] = self._model.intercept_

        # Calculate residual std for confidence intervals
        predictions = self._model.predict(X_features.values)
        residuals = y_aligned.values - predictions
        self._residual_std = np.std(residuals, ddof=len(self.feature_names) + 1)

        self._fit_metadata = {
            'n_samples': len(y_aligned),
            'fit_date': as_of_date or datetime.now(),
            'r2': self._model.score(X_features.values, y_aligned.values),
            'coefficients': self._coefficients.copy(),
        }

        self.is_fitted = True
        self.fit_date = as_of_date or datetime.now()

        return self

    def predict(self,
                X: pd.DataFrame,
                as_of_date: Optional[datetime] = None) -> pd.Series:
        """Generate fair value predictions."""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")

        X_features = self._prepare_features(X, fit=False)
        predictions = self._model.predict(X_features.values)

        return pd.Series(predictions, index=X_features.index, name='fair_value')

    def _prepare_features(self, X: pd.DataFrame, fit: bool = False) -> pd.DataFrame:
        """Prepare feature matrix with optional normalization."""
        features = X.copy()

        # Add squared inventory term if requested
        if self.include_squared and self.inventory_column in features.columns:
            features[f'{self.inventory_column}_squared'] = features[self.inventory_column] ** 2

        # Drop non-numeric columns
        features = features.select_dtypes(include=[np.number])

        # Handle missing values
        features = features.dropna()

        if fit:
            if self.normalize:
                self._scaler = StandardScaler()
                scaled_values = self._scaler.fit_transform(features.values)
                features = pd.DataFrame(scaled_values, index=features.index, columns=features.columns)
        else:
            if self.normalize and self._scaler is not None:
                # Only scale columns that were in training
                common_cols = [c for c in self.feature_names if c in features.columns]
                if len(common_cols) < len(self.feature_names):
                    missing = set(self.feature_names) - set(common_cols)
                    warnings.warn(f"Missing features in prediction: {missing}")
                    for col in missing:
                        features[col] = 0.0

                features = features[self.feature_names]
                scaled_values = self._scaler.transform(features.values)
                features = pd.DataFrame(scaled_values, index=features.index, columns=features.columns)

        return features

    def _get_components(self, X: pd.DataFrame) -> Dict[str, float]:
        """Get fair value decomposition by component."""
        if not self.is_fitted:
            return {}

        X_features = self._prepare_features(X, fit=False)
        components = {'intercept': self._model.intercept_}

        for i, col in enumerate(self.feature_names):
            components[col] = X_features[col].values[0] * self._model.coef_[i]

        return components


class CostOfCarryModel(FairValueModel):
    """
    Fair value model based on cost-of-carry theory.

    Economic Foundation:
    The cost-of-carry model states that futures/forward prices should equal
    spot prices plus carrying costs minus convenience yield:

        F(T) = S * exp((r + c - y) * T)

    Where:
    - F(T): Futures price at time T
    - S: Spot price
    - r: Risk-free rate
    - c: Storage cost rate
    - y: Convenience yield

    For spot price fair value, we invert this relationship using the
    futures term structure to infer convenience yield.

    Parameters
    ----------
    rate_column : str
        Name of the interest rate column
    storage_cost : float
        Annual storage cost rate (default 0.02 = 2%)
    """

    def __init__(self,
                 rate_column: str = 'interest_rate',
                 storage_cost: float = 0.02,
                 name: str = None):
        super().__init__(name or 'CostOfCarry')
        self.rate_column = rate_column
        self.storage_cost = storage_cost

        self._convenience_yield_model: Optional[LinearRegression] = None
        self._residual_std: Optional[float] = None

    def fit(self,
            X: pd.DataFrame,
            y: pd.Series,
            as_of_date: Optional[datetime] = None) -> 'CostOfCarryModel':
        """
        Fit the cost-of-carry model.

        Estimates the relationship between observable factors and
        convenience yield.
        """
        # Apply point-in-time filter
        if as_of_date is not None:
            mask = X.index <= as_of_date
            X = X.loc[mask]
            y = y.loc[mask]

        # We model the spread between actual price and carry-implied price
        # This spread reflects convenience yield
        if self.rate_column not in X.columns:
            raise ValueError(f"Rate column '{self.rate_column}' not found in data")

        # Prepare features for convenience yield model
        features = X.select_dtypes(include=[np.number]).dropna()
        common_idx = features.index.intersection(y.index)
        features = features.loc[common_idx]
        y_aligned = y.loc[common_idx]

        self.feature_names = list(features.columns)
        self.target_name = y.name or 'price'

        # Fit simple regression for now
        self._convenience_yield_model = LinearRegression()
        self._convenience_yield_model.fit(features.values, y_aligned.values)

        # Calculate residual std
        predictions = self._convenience_yield_model.predict(features.values)
        residuals = y_aligned.values - predictions
        self._residual_std = np.std(residuals)

        self._fit_metadata = {
            'n_samples': len(y_aligned),
            'fit_date': as_of_date or datetime.now(),
            'r2': self._convenience_yield_model.score(features.values, y_aligned.values),
            'storage_cost': self.storage_cost,
        }

        self.is_fitted = True
        self.fit_date = as_of_date or datetime.now()

        return self

    def predict(self,
                X: pd.DataFrame,
                as_of_date: Optional[datetime] = None) -> pd.Series:
        """Generate fair value predictions."""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")

        features = X.select_dtypes(include=[np.number]).dropna()
        features = features[self.feature_names]

        predictions = self._convenience_yield_model.predict(features.values)

        return pd.Series(predictions, index=features.index, name='fair_value')


class SupplyDemandModel(FairValueModel):
    """
    Fair value model based on supply-demand balance.

    Economic Foundation:
    Prices clear markets where supply equals demand. By modeling supply
    and demand curves as functions of price and fundamental factors,
    we can solve for the equilibrium price (fair value).

    Model Specification:
        Supply: Q_s = alpha_s + beta_s * P + gamma_s * Z_s
        Demand: Q_d = alpha_d + beta_d * P + gamma_d * Z_d
        Equilibrium: Q_s = Q_d

    Where:
    - Z_s: Supply shifters (production, imports, etc.)
    - Z_d: Demand shifters (consumption, exports, etc.)

    Parameters
    ----------
    supply_columns : list
        Column names for supply factors
    demand_columns : list
        Column names for demand factors
    """

    def __init__(self,
                 supply_columns: List[str] = None,
                 demand_columns: List[str] = None,
                 name: str = None):
        super().__init__(name or 'SupplyDemand')
        self.supply_columns = supply_columns or []
        self.demand_columns = demand_columns or []

        self._model: Optional[LinearRegression] = None
        self._residual_std: Optional[float] = None

    def fit(self,
            X: pd.DataFrame,
            y: pd.Series,
            as_of_date: Optional[datetime] = None) -> 'SupplyDemandModel':
        """Fit supply-demand balance model."""

        if as_of_date is not None:
            mask = X.index <= as_of_date
            X = X.loc[mask]
            y = y.loc[mask]

        # Create balance features
        features = pd.DataFrame(index=X.index)

        # Supply factors (higher supply = lower price, so we negate)
        for col in self.supply_columns:
            if col in X.columns:
                features[f'supply_{col}'] = -X[col]

        # Demand factors (higher demand = higher price)
        for col in self.demand_columns:
            if col in X.columns:
                features[f'demand_{col}'] = X[col]

        # If no specific columns, use all numeric columns
        if len(features.columns) == 0:
            features = X.select_dtypes(include=[np.number])

        features = features.dropna()
        common_idx = features.index.intersection(y.index)
        features = features.loc[common_idx]
        y_aligned = y.loc[common_idx]

        self.feature_names = list(features.columns)
        self.target_name = y.name or 'price'

        self._model = LinearRegression()
        self._model.fit(features.values, y_aligned.values)

        predictions = self._model.predict(features.values)
        residuals = y_aligned.values - predictions
        self._residual_std = np.std(residuals)

        self._fit_metadata = {
            'n_samples': len(y_aligned),
            'fit_date': as_of_date or datetime.now(),
            'r2': self._model.score(features.values, y_aligned.values),
        }

        self.is_fitted = True
        self.fit_date = as_of_date or datetime.now()

        return self

    def predict(self,
                X: pd.DataFrame,
                as_of_date: Optional[datetime] = None) -> pd.Series:
        """Generate fair value predictions."""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")

        # Create balance features using same logic as fit
        features = pd.DataFrame(index=X.index)

        for col in self.supply_columns:
            if col in X.columns:
                features[f'supply_{col}'] = -X[col]

        for col in self.demand_columns:
            if col in X.columns:
                features[f'demand_{col}'] = X[col]

        if len(features.columns) == 0:
            features = X.select_dtypes(include=[np.number])

        features = features.dropna()
        features = features.reindex(columns=self.feature_names, fill_value=0)

        predictions = self._model.predict(features.values)

        return pd.Series(predictions, index=features.index, name='fair_value')


class CostCurveModel(FairValueModel):
    """
    Fair value model based on marginal cost of production.

    Economic Foundation:
    In competitive commodity markets, price tends toward the marginal
    cost of production. The cost curve ranks producers by cost, and
    the clearing price is set by the marginal producer.

    This model estimates fair value as a function of:
    - Input costs (energy, labor, materials)
    - Exchange rates (for internationally traded commodities)
    - Production technology proxies

    Parameters
    ----------
    cost_columns : list
        Column names for production cost factors
    elasticity_prior : float
        Prior belief about demand elasticity (default 0.5)
    """

    def __init__(self,
                 cost_columns: List[str] = None,
                 elasticity_prior: float = 0.5,
                 name: str = None):
        super().__init__(name or 'CostCurve')
        self.cost_columns = cost_columns or []
        self.elasticity_prior = elasticity_prior

        self._model: Optional[LinearRegression] = None
        self._residual_std: Optional[float] = None

    def fit(self,
            X: pd.DataFrame,
            y: pd.Series,
            as_of_date: Optional[datetime] = None) -> 'CostCurveModel':
        """Fit cost curve model."""

        if as_of_date is not None:
            mask = X.index <= as_of_date
            X = X.loc[mask]
            y = y.loc[mask]

        # Select cost-related features
        if self.cost_columns:
            features = X[self.cost_columns].dropna()
        else:
            features = X.select_dtypes(include=[np.number]).dropna()

        common_idx = features.index.intersection(y.index)
        features = features.loc[common_idx]
        y_aligned = y.loc[common_idx]

        self.feature_names = list(features.columns)
        self.target_name = y.name or 'price'

        # Use ElasticNet to allow some regularization
        self._model = ElasticNet(alpha=0.1, l1_ratio=0.5)
        self._model.fit(features.values, y_aligned.values)

        predictions = self._model.predict(features.values)
        residuals = y_aligned.values - predictions
        self._residual_std = np.std(residuals)

        self._fit_metadata = {
            'n_samples': len(y_aligned),
            'fit_date': as_of_date or datetime.now(),
            'r2': self._model.score(features.values, y_aligned.values),
        }

        self.is_fitted = True
        self.fit_date = as_of_date or datetime.now()

        return self

    def predict(self,
                X: pd.DataFrame,
                as_of_date: Optional[datetime] = None) -> pd.Series:
        """Generate fair value predictions."""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")

        if self.cost_columns:
            features = X[self.cost_columns].dropna()
        else:
            features = X.select_dtypes(include=[np.number]).dropna()

        features = features.reindex(columns=self.feature_names, fill_value=0)
        predictions = self._model.predict(features.values)

        return pd.Series(predictions, index=features.index, name='fair_value')


class EnsembleFairValueModel(FairValueModel):
    """
    Ensemble model that combines multiple fair value models.

    This model aggregates predictions from multiple base models using
    either fixed weights or dynamically optimized weights based on
    recent performance.

    Parameters
    ----------
    models : list
        List of FairValueModel instances
    weights : list, optional
        Fixed weights for each model. If None, uses equal weights or
        optimizes based on historical performance.
    optimize_weights : bool
        Whether to optimize weights during fit (default True)
    lookback_period : int
        Number of periods to use for weight optimization (default 252)
    """

    def __init__(self,
                 models: List[FairValueModel],
                 weights: List[float] = None,
                 optimize_weights: bool = True,
                 lookback_period: int = 252,
                 name: str = None):
        super().__init__(name or 'EnsembleFairValue')
        self.models = models
        self.weights = weights
        self.optimize_weights = optimize_weights
        self.lookback_period = lookback_period

        if weights is not None and len(weights) != len(models):
            raise ValueError("Number of weights must match number of models")

        self._optimized_weights: Optional[np.ndarray] = None
        self._residual_std: Optional[float] = None

    def fit(self,
            X: pd.DataFrame,
            y: pd.Series,
            as_of_date: Optional[datetime] = None) -> 'EnsembleFairValueModel':
        """Fit all base models and optionally optimize weights."""

        # Fit each base model
        for model in self.models:
            model.fit(X, y, as_of_date)

        # Get predictions from each model
        predictions = []
        for model in self.models:
            try:
                pred = model.predict(X, as_of_date)
                predictions.append(pred)
            except Exception as e:
                warnings.warn(f"Model {model.name} prediction failed: {e}")
                predictions.append(pd.Series(np.nan, index=X.index))

        # Align predictions
        pred_df = pd.DataFrame({f'model_{i}': p for i, p in enumerate(predictions)})
        pred_df = pred_df.dropna()
        common_idx = pred_df.index.intersection(y.index)
        pred_df = pred_df.loc[common_idx]
        y_aligned = y.loc[common_idx]

        if self.optimize_weights:
            # Optimize weights to minimize squared error
            def objective(w):
                w = w / w.sum()  # Normalize
                ensemble_pred = (pred_df.values * w).sum(axis=1)
                return np.mean((y_aligned.values - ensemble_pred) ** 2)

            # Initial guess: equal weights
            w0 = np.ones(len(self.models)) / len(self.models)

            # Bounds: weights between 0 and 1
            bounds = [(0, 1) for _ in self.models]

            result = optimize.minimize(objective, w0, bounds=bounds, method='SLSQP')
            self._optimized_weights = result.x / result.x.sum()
        else:
            if self.weights is not None:
                self._optimized_weights = np.array(self.weights)
            else:
                self._optimized_weights = np.ones(len(self.models)) / len(self.models)

        # Calculate ensemble residual std
        ensemble_pred = (pred_df.values * self._optimized_weights).sum(axis=1)
        residuals = y_aligned.values - ensemble_pred
        self._residual_std = np.std(residuals)

        self._fit_metadata = {
            'n_samples': len(y_aligned),
            'fit_date': as_of_date or datetime.now(),
            'weights': dict(zip([m.name for m in self.models], self._optimized_weights)),
            'base_model_r2': {m.name: m._fit_metadata.get('r2', np.nan) for m in self.models},
        }

        self.is_fitted = True
        self.fit_date = as_of_date or datetime.now()

        return self

    def predict(self,
                X: pd.DataFrame,
                as_of_date: Optional[datetime] = None) -> pd.Series:
        """Generate weighted ensemble predictions."""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")

        predictions = []
        for model in self.models:
            try:
                pred = model.predict(X, as_of_date)
                predictions.append(pred)
            except Exception:
                predictions.append(pd.Series(np.nan, index=X.index))

        pred_df = pd.DataFrame({f'model_{i}': p for i, p in enumerate(predictions)})

        # Weighted average
        ensemble_pred = (pred_df.values * self._optimized_weights).sum(axis=1)

        return pd.Series(ensemble_pred, index=pred_df.index, name='fair_value')

    def get_model_contributions(self, X: pd.DataFrame) -> pd.DataFrame:
        """Get the contribution of each base model to the ensemble."""
        predictions = {}
        for i, model in enumerate(self.models):
            try:
                pred = model.predict(X)
                predictions[model.name] = pred * self._optimized_weights[i]
            except Exception:
                predictions[model.name] = np.nan

        return pd.DataFrame(predictions)
