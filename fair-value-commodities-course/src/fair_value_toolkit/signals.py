"""
Signal Generation Framework
===========================

This module converts fair value model outputs into trading signals.
The key insight is that fair value alone is not a trading signal -
we need to consider:

1. Magnitude of mispricing (fair value vs market price)
2. Confidence in the fair value estimate
3. Time dynamics (mean reversion speed)
4. Risk constraints (position limits, correlation with portfolio)

Key Components:
- FairValueSignal: Container for signal information
- SignalGenerator: Convert fair value to trading signals
- PositionSizer: Determine position sizes based on signals
- RiskManager: Apply risk constraints to positions
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, List, Any, Tuple
import numpy as np
import pandas as pd
from scipy import stats
import warnings


@dataclass
class FairValueSignal:
    """
    Container for a fair value trading signal.

    Attributes
    ----------
    date : datetime
        Signal generation date
    commodity : str
        Commodity identifier
    fair_value : float
        Model-estimated fair value
    market_price : float
        Current market price
    mispricing : float
        Fair value minus market price
    mispricing_zscore : float
        Standardized mispricing (in standard deviations)
    signal_direction : int
        1 (long), -1 (short), or 0 (neutral)
    signal_strength : float
        Signal strength from 0 to 1
    confidence : float
        Model confidence (0 to 1)
    half_life : float
        Expected half-life of mean reversion (in days)
    metadata : dict
        Additional signal information
    """
    date: datetime
    commodity: str
    fair_value: float
    market_price: float
    mispricing: float
    mispricing_zscore: float
    signal_direction: int
    signal_strength: float
    confidence: float = 1.0
    half_life: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def percentage_mispricing(self) -> float:
        """Mispricing as percentage of market price."""
        if self.market_price != 0:
            return self.mispricing / self.market_price * 100
        return np.nan

    def to_dict(self) -> Dict[str, Any]:
        return {
            'date': self.date,
            'commodity': self.commodity,
            'fair_value': self.fair_value,
            'market_price': self.market_price,
            'mispricing': self.mispricing,
            'mispricing_zscore': self.mispricing_zscore,
            'mispricing_pct': self.percentage_mispricing,
            'signal_direction': self.signal_direction,
            'signal_strength': self.signal_strength,
            'confidence': self.confidence,
            'half_life': self.half_life,
            **self.metadata,
        }


class SignalGenerator:
    """
    Generate trading signals from fair value model outputs.

    The signal generation process:
    1. Calculate mispricing = fair_value - market_price
    2. Normalize by historical volatility → z-score
    3. Apply entry/exit thresholds
    4. Incorporate model confidence
    5. Apply signal decay

    Parameters
    ----------
    entry_threshold : float
        Z-score threshold for signal generation (default 1.5)
    exit_threshold : float
        Z-score threshold for position exit (default 0.5)
    lookback_window : int
        Window for calculating historical mispricing statistics
    confidence_weight : bool
        Weight signal by model confidence
    decay_halflife : int
        Signal decay half-life in periods (None = no decay)
    max_signal : float
        Maximum signal strength (default 1.0)
    """

    def __init__(self,
                 entry_threshold: float = 1.5,
                 exit_threshold: float = 0.5,
                 lookback_window: int = 252,
                 confidence_weight: bool = True,
                 decay_halflife: Optional[int] = None,
                 max_signal: float = 1.0):
        self.entry_threshold = entry_threshold
        self.exit_threshold = exit_threshold
        self.lookback_window = lookback_window
        self.confidence_weight = confidence_weight
        self.decay_halflife = decay_halflife
        self.max_signal = max_signal

        self._mispricing_history: Optional[pd.Series] = None
        self._signal_history: List[FairValueSignal] = []

    def generate(self,
                 fair_values: pd.DataFrame,
                 market_prices: pd.Series,
                 commodity: str = 'commodity') -> pd.DataFrame:
        """
        Generate signals for a time series of fair values.

        Parameters
        ----------
        fair_values : pd.DataFrame
            DataFrame with 'fair_value' column and optionally 'lower', 'upper'
            for confidence intervals
        market_prices : pd.Series
            Market prices aligned with fair_values index
        commodity : str
            Commodity identifier

        Returns
        -------
        pd.DataFrame
            DataFrame with signal columns
        """
        # Align indices
        common_idx = fair_values.index.intersection(market_prices.index)
        fv = fair_values.loc[common_idx]
        mp = market_prices.loc[common_idx]

        # Calculate mispricing
        mispricing = fv['fair_value'] - mp

        # Calculate rolling statistics for z-score
        mispricing_mean = mispricing.rolling(window=self.lookback_window, min_periods=20).mean()
        mispricing_std = mispricing.rolling(window=self.lookback_window, min_periods=20).std()

        # Z-score
        zscore = (mispricing - mispricing_mean) / mispricing_std
        zscore = zscore.replace([np.inf, -np.inf], np.nan)

        # Generate raw signal
        signal_direction = np.where(zscore > self.entry_threshold, 1,
                                   np.where(zscore < -self.entry_threshold, -1, 0))

        # Signal strength (scaled by z-score magnitude)
        signal_strength = np.clip(np.abs(zscore) / self.entry_threshold * 0.5, 0, self.max_signal)

        # Incorporate model confidence if available
        if 'lower' in fv.columns and 'upper' in fv.columns:
            confidence_interval = fv['upper'] - fv['lower']
            relative_ci = confidence_interval / mp
            confidence = 1 / (1 + relative_ci)  # Higher CI = lower confidence
            if self.confidence_weight:
                signal_strength = signal_strength * confidence.values
        else:
            confidence = pd.Series(1.0, index=common_idx)

        # Apply signal decay
        if self.decay_halflife is not None:
            decay = np.exp(-np.log(2) / self.decay_halflife * np.arange(len(signal_strength)))
            # This is simplified - full implementation would track signal age

        # Build output DataFrame
        result = pd.DataFrame({
            'fair_value': fv['fair_value'],
            'market_price': mp,
            'mispricing': mispricing,
            'mispricing_zscore': zscore,
            'signal_direction': signal_direction,
            'signal_strength': signal_strength,
            'confidence': confidence,
            'commodity': commodity,
        }, index=common_idx)

        # Store history
        self._mispricing_history = mispricing

        return result

    def generate_single(self,
                        fair_value: float,
                        confidence_interval: Tuple[float, float],
                        market_price: float,
                        date: datetime,
                        commodity: str) -> FairValueSignal:
        """
        Generate a single signal from fair value output.

        Parameters
        ----------
        fair_value : float
            Point estimate of fair value
        confidence_interval : tuple
            (lower, upper) bounds
        market_price : float
            Current market price
        date : datetime
            Signal date
        commodity : str
            Commodity identifier

        Returns
        -------
        FairValueSignal
            Signal object
        """
        mispricing = fair_value - market_price

        # Use historical mispricing for z-score
        if self._mispricing_history is not None and len(self._mispricing_history) > 20:
            hist_mean = self._mispricing_history.mean()
            hist_std = self._mispricing_history.std()
            zscore = (mispricing - hist_mean) / hist_std if hist_std > 0 else 0
        else:
            # Use confidence interval as proxy for std
            ci_width = confidence_interval[1] - confidence_interval[0]
            zscore = mispricing / (ci_width / 4) if ci_width > 0 else 0

        # Signal direction
        if zscore > self.entry_threshold:
            direction = 1  # Long (undervalued)
        elif zscore < -self.entry_threshold:
            direction = -1  # Short (overvalued)
        else:
            direction = 0  # Neutral

        # Signal strength
        strength = min(abs(zscore) / self.entry_threshold * 0.5, self.max_signal)

        # Confidence from CI width
        relative_ci = (confidence_interval[1] - confidence_interval[0]) / market_price
        confidence = 1 / (1 + relative_ci)

        return FairValueSignal(
            date=date,
            commodity=commodity,
            fair_value=fair_value,
            market_price=market_price,
            mispricing=mispricing,
            mispricing_zscore=zscore,
            signal_direction=direction,
            signal_strength=strength,
            confidence=confidence,
        )

    def estimate_half_life(self, mispricing: pd.Series) -> float:
        """
        Estimate mean reversion half-life from mispricing series.

        Uses OLS regression of price changes on price levels:
            Δm_t = β * m_{t-1} + ε_t

        Half-life = -ln(2) / ln(1 + β)

        Parameters
        ----------
        mispricing : pd.Series
            Mispricing time series

        Returns
        -------
        float
            Estimated half-life in periods
        """
        if len(mispricing) < 30:
            return np.nan

        # Remove NaN
        m = mispricing.dropna()

        # Regression
        delta_m = m.diff().dropna()
        lagged_m = m.shift(1).dropna()

        # Align
        common_idx = delta_m.index.intersection(lagged_m.index)
        y = delta_m.loc[common_idx].values
        X = lagged_m.loc[common_idx].values.reshape(-1, 1)

        from sklearn.linear_model import LinearRegression
        model = LinearRegression()
        model.fit(X, y)

        beta = model.coef_[0]

        if beta >= 0:
            return np.inf  # No mean reversion

        half_life = -np.log(2) / np.log(1 + beta)
        return max(half_life, 0)


class PositionSizer:
    """
    Determine position sizes based on trading signals.

    Implements several position sizing methods:
    - Equal weight: All signals get same position size
    - Signal-proportional: Size proportional to signal strength
    - Kelly criterion: Optimal sizing based on expected return/risk
    - Risk parity: Size inversely proportional to volatility

    Parameters
    ----------
    method : str
        Position sizing method ('equal', 'signal', 'kelly', 'risk_parity')
    max_position : float
        Maximum position size as fraction of portfolio (default 0.1)
    kelly_fraction : float
        Fraction of Kelly criterion to use (default 0.25)
    target_volatility : float
        Target portfolio volatility for risk parity (default 0.15)
    """

    def __init__(self,
                 method: str = 'signal',
                 max_position: float = 0.1,
                 kelly_fraction: float = 0.25,
                 target_volatility: float = 0.15):
        self.method = method
        self.max_position = max_position
        self.kelly_fraction = kelly_fraction
        self.target_volatility = target_volatility

        valid_methods = ['equal', 'signal', 'kelly', 'risk_parity']
        if method not in valid_methods:
            raise ValueError(f"method must be one of {valid_methods}")

    def size(self,
             signals: pd.DataFrame,
             volatility: Optional[pd.Series] = None,
             expected_return: Optional[pd.Series] = None) -> pd.Series:
        """
        Calculate position sizes for a series of signals.

        Parameters
        ----------
        signals : pd.DataFrame
            Output from SignalGenerator.generate()
        volatility : pd.Series, optional
            Historical volatility (required for kelly, risk_parity)
        expected_return : pd.Series, optional
            Expected return (required for kelly)

        Returns
        -------
        pd.Series
            Position sizes (positive = long, negative = short)
        """
        direction = signals['signal_direction'].values
        strength = signals['signal_strength'].values

        if self.method == 'equal':
            # Equal weight for all signals
            base_size = np.ones(len(signals)) * self.max_position

        elif self.method == 'signal':
            # Proportional to signal strength
            base_size = strength * self.max_position

        elif self.method == 'kelly':
            # Kelly criterion
            if expected_return is None or volatility is None:
                warnings.warn("Kelly requires expected_return and volatility, using signal method")
                base_size = strength * self.max_position
            else:
                # Kelly: f* = μ / σ²
                exp_ret = expected_return.reindex(signals.index).fillna(0)
                vol = volatility.reindex(signals.index).fillna(1)

                kelly_size = exp_ret / (vol ** 2)
                kelly_size = kelly_size * self.kelly_fraction
                base_size = np.clip(np.abs(kelly_size), 0, self.max_position)

        elif self.method == 'risk_parity':
            # Inverse volatility weighting
            if volatility is None:
                warnings.warn("risk_parity requires volatility, using signal method")
                base_size = strength * self.max_position
            else:
                vol = volatility.reindex(signals.index).fillna(1)
                # Size inversely proportional to volatility
                inv_vol = 1 / vol
                # Scale to target volatility
                base_size = (self.target_volatility / vol) * strength
                base_size = np.clip(base_size, 0, self.max_position)

        # Apply direction
        position_size = base_size * direction

        return pd.Series(position_size, index=signals.index, name='position_size')

    def kelly_optimal(self,
                      win_rate: float,
                      avg_win: float,
                      avg_loss: float) -> float:
        """
        Calculate Kelly optimal fraction.

        Kelly formula: f* = (p * b - q) / b

        Where:
        - p = win rate
        - q = 1 - p
        - b = avg_win / avg_loss

        Parameters
        ----------
        win_rate : float
            Probability of winning (0 to 1)
        avg_win : float
            Average winning return
        avg_loss : float
            Average losing return (positive number)

        Returns
        -------
        float
            Optimal fraction to bet
        """
        p = win_rate
        q = 1 - p
        b = avg_win / avg_loss if avg_loss > 0 else np.inf

        kelly = (p * b - q) / b

        # Apply fraction and max position
        position = min(kelly * self.kelly_fraction, self.max_position)
        return max(position, 0)


class RiskManager:
    """
    Apply risk constraints to position sizes.

    Risk constraints include:
    - Position limits (per asset and total)
    - Correlation constraints (max correlation between positions)
    - Drawdown controls (reduce size after losses)
    - Volatility targeting (scale positions to target vol)

    Parameters
    ----------
    max_position_single : float
        Max position in single commodity (default 0.1)
    max_position_total : float
        Max total gross position (default 1.0)
    max_correlation : float
        Max average correlation between positions (default 0.7)
    drawdown_threshold : float
        Drawdown level to start reducing positions (default 0.1)
    """

    def __init__(self,
                 max_position_single: float = 0.1,
                 max_position_total: float = 1.0,
                 max_correlation: float = 0.7,
                 drawdown_threshold: float = 0.1):
        self.max_position_single = max_position_single
        self.max_position_total = max_position_total
        self.max_correlation = max_correlation
        self.drawdown_threshold = drawdown_threshold

        self._equity_curve: Optional[pd.Series] = None

    def apply_constraints(self,
                          positions: pd.DataFrame,
                          correlation_matrix: Optional[pd.DataFrame] = None,
                          current_drawdown: float = 0.0) -> pd.DataFrame:
        """
        Apply risk constraints to position matrix.

        Parameters
        ----------
        positions : pd.DataFrame
            Position sizes by commodity (columns) and date (rows)
        correlation_matrix : pd.DataFrame, optional
            Correlation matrix between commodities
        current_drawdown : float
            Current drawdown from peak (0 to 1)

        Returns
        -------
        pd.DataFrame
            Constrained position sizes
        """
        constrained = positions.copy()

        # Apply single position limit
        constrained = constrained.clip(-self.max_position_single, self.max_position_single)

        # Apply total position limit
        gross_exposure = constrained.abs().sum(axis=1)
        scale_factor = np.minimum(1, self.max_position_total / gross_exposure)
        scale_factor = scale_factor.replace([np.inf, np.nan], 1.0)
        constrained = constrained.multiply(scale_factor, axis=0)

        # Apply drawdown reduction
        if current_drawdown > self.drawdown_threshold:
            # Linear reduction: at 2x threshold, positions are halved
            dd_scale = 1 - (current_drawdown - self.drawdown_threshold) / self.drawdown_threshold
            dd_scale = np.clip(dd_scale, 0.25, 1.0)  # Never reduce below 25%
            constrained = constrained * dd_scale

        # Apply correlation constraint (simplified)
        if correlation_matrix is not None and len(constrained.columns) > 1:
            # If average pairwise correlation is too high, reduce concentrated positions
            avg_corr = correlation_matrix.values[np.triu_indices_from(correlation_matrix.values, k=1)].mean()
            if avg_corr > self.max_correlation:
                # Scale by 1 / sqrt(avg_corr) to reduce correlation impact
                corr_scale = self.max_correlation / avg_corr
                constrained = constrained * np.sqrt(corr_scale)

        return constrained

    def calculate_var(self,
                      positions: pd.Series,
                      returns: pd.DataFrame,
                      confidence: float = 0.95,
                      method: str = 'historical') -> float:
        """
        Calculate Value at Risk for current positions.

        Parameters
        ----------
        positions : pd.Series
            Current positions by commodity
        returns : pd.DataFrame
            Historical returns by commodity
        confidence : float
            Confidence level (default 0.95)
        method : str
            'historical' or 'parametric'

        Returns
        -------
        float
            VaR as positive number (potential loss)
        """
        # Align positions with returns
        common_cols = positions.index.intersection(returns.columns)
        pos = positions.loc[common_cols]
        ret = returns[common_cols]

        # Portfolio returns
        portfolio_returns = (ret * pos).sum(axis=1)

        if method == 'historical':
            var = -np.percentile(portfolio_returns, (1 - confidence) * 100)
        else:
            # Parametric (assuming normal)
            mu = portfolio_returns.mean()
            sigma = portfolio_returns.std()
            var = -(mu + stats.norm.ppf(1 - confidence) * sigma)

        return var

    def calculate_cvar(self,
                       positions: pd.Series,
                       returns: pd.DataFrame,
                       confidence: float = 0.95) -> float:
        """
        Calculate Conditional Value at Risk (Expected Shortfall).

        Parameters
        ----------
        positions : pd.Series
            Current positions by commodity
        returns : pd.DataFrame
            Historical returns by commodity
        confidence : float
            Confidence level (default 0.95)

        Returns
        -------
        float
            CVaR as positive number (expected loss beyond VaR)
        """
        common_cols = positions.index.intersection(returns.columns)
        pos = positions.loc[common_cols]
        ret = returns[common_cols]

        portfolio_returns = (ret * pos).sum(axis=1)

        var_threshold = np.percentile(portfolio_returns, (1 - confidence) * 100)
        tail_returns = portfolio_returns[portfolio_returns <= var_threshold]

        return -tail_returns.mean() if len(tail_returns) > 0 else np.nan

    def calculate_drawdown(self, equity_curve: pd.Series) -> pd.Series:
        """
        Calculate drawdown series from equity curve.

        Parameters
        ----------
        equity_curve : pd.Series
            Portfolio equity over time

        Returns
        -------
        pd.Series
            Drawdown as fraction of peak (0 to 1)
        """
        self._equity_curve = equity_curve

        rolling_max = equity_curve.expanding().max()
        drawdown = (rolling_max - equity_curve) / rolling_max

        return drawdown

    def get_max_drawdown(self, equity_curve: pd.Series = None) -> float:
        """Get maximum drawdown."""
        if equity_curve is None:
            equity_curve = self._equity_curve

        if equity_curve is None:
            return np.nan

        drawdown = self.calculate_drawdown(equity_curve)
        return drawdown.max()


def generate_signal_report(signals: pd.DataFrame,
                          positions: pd.Series = None,
                          returns: pd.Series = None) -> Dict[str, Any]:
    """
    Generate a summary report for trading signals.

    Parameters
    ----------
    signals : pd.DataFrame
        Output from SignalGenerator.generate()
    positions : pd.Series, optional
        Position sizes
    returns : pd.Series, optional
        Realized returns from signals

    Returns
    -------
    dict
        Summary statistics
    """
    report = {
        'total_signals': len(signals),
        'long_signals': (signals['signal_direction'] == 1).sum(),
        'short_signals': (signals['signal_direction'] == -1).sum(),
        'neutral_periods': (signals['signal_direction'] == 0).sum(),
        'avg_signal_strength': signals['signal_strength'].mean(),
        'avg_confidence': signals['confidence'].mean(),
        'avg_mispricing_pct': (signals['mispricing'] / signals['market_price'] * 100).mean(),
    }

    if positions is not None:
        report['avg_position'] = positions.abs().mean()
        report['max_position'] = positions.abs().max()
        report['turnover'] = positions.diff().abs().mean()

    if returns is not None:
        report['total_return'] = (1 + returns).prod() - 1
        report['avg_return'] = returns.mean()
        report['sharpe'] = returns.mean() / returns.std() * np.sqrt(252) if returns.std() > 0 else np.nan
        report['win_rate'] = (returns > 0).mean()

    return report
