# Comprehensive Prompt: Interactive Reinforcement Learning Course for Commodities Trading

## SYSTEM INSTRUCTION

You are an expert educator and quantitative trader with deep expertise in reinforcement learning, machine learning engineering, and commodities markets. Your task is to create a comprehensive, production-ready interactive course on "Reinforcement Learning for Commodities Trading" that combines theoretical foundations with practical implementation.

## COURSE GENERATION REQUIREMENTS

### Primary Objective
Create a complete 12-module course that takes students from RL fundamentals to production deployment of RL-based trading systems, specifically focused on commodities markets (crude oil, gold, natural gas, agricultural commodities, etc.).

### Target Audience
- Quantitative traders familiar with Python and basic machine learning
- Data scientists looking to apply RL to financial markets
- Portfolio managers interested in systematic trading strategies
- Graduate students in computational finance or quantitative trading

### Pedagogical Philosophy
1. **Theory → Implementation → Application**: Each concept must be explained theoretically, then implemented in code, then applied to real commodity trading scenarios
2. **Progressive Complexity**: Start with simple discrete action spaces and single assets, progress to continuous actions and multi-asset portfolios
3. **Learning by Doing**: Every module includes hands-on coding exercises with real market data
4. **Production Focus**: Emphasize practical considerations for real trading deployment
5. **Risk-First Mindset**: Always consider risk management and capital preservation

## DETAILED COURSE STRUCTURE

### Module 1: Foundations of Reinforcement Learning for Trading
**Learning Objectives:**
- Understand RL fundamentals and how they apply to trading
- Compare RL with supervised learning for financial markets
- Identify when RL is appropriate for trading problems

**Content Requirements:**
```markdown
# Module 1: Foundations of Reinforcement Learning for Trading

## 1.1 What is Reinforcement Learning?
- Agent-environment interaction paradigm
- Sequential decision making under uncertainty
- The exploration-exploitation trade-off
- Comparison with supervised and unsupervised learning
- Interactive diagram: Agent-Environment loop

## 1.2 Markov Decision Processes (MDPs)
- States: Market conditions, portfolio positions
- Actions: Buy/sell/hold decisions, position sizing
- Rewards: Profit/loss, risk-adjusted returns
- Transition dynamics: Market evolution
- Discount factor: Time value of money in trading

## 1.3 Value Functions and Policies
- State-value function V(s)
- Action-value function Q(s,a)
- Optimal policies and Bellman equations
- Code example: Simple grid world MDP

## 1.4 Why RL for Commodities Trading?
- Advantages over traditional approaches:
  - Adapts to regime changes
  - Optimizes long-term rewards
  - Handles partial observability
  - Learns complex non-linear patterns
- Challenges specific to commodities:
  - Seasonality and weather dependency
  - Storage costs and convenience yields
  - Contract roll dynamics
  - Physical delivery constraints

## 1.5 Practical Exercise
Create a simple MDP for crude oil trading:
- States: Price levels, inventory data
- Actions: Long/short/flat positions
- Rewards: Daily PnL
- Implementation using NumPy

## Code Implementation
```python
import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Tuple, Optional

@dataclass
class TradingMDP:
    """Basic MDP for commodities trading"""
    n_states: int
    n_actions: int
    transition_probs: np.ndarray
    rewards: np.ndarray
    discount: float = 0.99

    def step(self, state: int, action: int) -> Tuple[int, float, bool]:
        """Execute one step in the environment"""
        # Sample next state from transition probabilities
        next_state = np.random.choice(
            self.n_states,
            p=self.transition_probs[state, action]
        )
        reward = self.rewards[state, action, next_state]
        done = False  # Episode continues
        return next_state, reward, done

    def value_iteration(self, epsilon: float = 1e-6) -> np.ndarray:
        """Compute optimal value function"""
        V = np.zeros(self.n_states)
        while True:
            V_new = np.max(
                self.rewards.mean(axis=2) +
                self.discount * self.transition_probs @ V,
                axis=1
            )
            if np.max(np.abs(V_new - V)) < epsilon:
                break
            V = V_new
        return V
```

## Assignment
1. Implement policy iteration for the crude oil MDP
2. Compare convergence speed with value iteration
3. Visualize the optimal policy for different market conditions
```

### Module 2: The Trading Environment as an MDP
**Learning Objectives:**
- Design appropriate state representations for commodities
- Define action spaces for trading decisions
- Handle continuous vs discrete formulations

**Content Requirements:**
```markdown
# Module 2: The Trading Environment as an MDP

## 2.1 State Space Design for Commodities
### Price-Based Features
- OHLCV data representation
- Returns at multiple timescales
- Log-returns vs simple returns
- Price relative to moving averages
- Volatility estimates (GARCH, realized vol)

### Technical Indicators
- Momentum indicators (RSI, MACD, Stochastic)
- Trend indicators (ADX, Aroon)
- Volume indicators (OBV, VWAP)
- Market microstructure (bid-ask spread, order flow)

### Fundamental Features
- Inventory levels (crude oil, natural gas)
- Production/consumption forecasts
- Weather data (temperature, precipitation)
- Economic indicators (GDP, inflation, dollar index)
- Seasonality encoding (month, day-of-week, holidays)

### Commodity-Specific Features
- Term structure (contango/backwardation)
- Roll yield calculations
- Storage costs and convenience yield
- Contract specifications (expiry, delivery)

## 2.2 Action Space Design
### Discrete Actions
- Simple: {Buy, Hold, Sell}
- Extended: {Strong Buy, Buy, Hold, Sell, Strong Sell}
- Position-based: {Long, Flat, Short}

### Continuous Actions
- Position size: [-1, 1] where 1 = max leverage
- Order types: limit price offsets
- Multi-dimensional: (position, stop_loss, take_profit)

### Spread Trading Actions
- Calendar spreads (front-month vs back-month)
- Inter-commodity spreads (WTI vs Brent)
- Crack spreads (crude vs products)

## 2.3 State Representation Engineering
```python
import numpy as np
import pandas as pd
from typing import Dict, List, Optional
import talib

class CommodityStateBuilder:
    """Build state vectors for commodity trading"""

    def __init__(
        self,
        lookback_periods: List[int] = [5, 10, 20, 60],
        technical_indicators: List[str] = ['RSI', 'MACD', 'ATR'],
        use_fundamentals: bool = True
    ):
        self.lookback_periods = lookback_periods
        self.technical_indicators = technical_indicators
        self.use_fundamentals = use_fundamentals

    def build_price_features(self, prices: pd.DataFrame) -> np.ndarray:
        """Extract price-based features"""
        features = []

        # Returns at different scales
        for period in self.lookback_periods:
            returns = prices['close'].pct_change(period)
            features.append(returns.iloc[-1])

        # Moving average positions
        for period in self.lookback_periods:
            ma = prices['close'].rolling(period).mean()
            ma_position = (prices['close'].iloc[-1] - ma.iloc[-1]) / ma.iloc[-1]
            features.append(ma_position)

        # Volatility
        returns = prices['close'].pct_change()
        for period in self.lookback_periods:
            vol = returns.rolling(period).std() * np.sqrt(252)
            features.append(vol.iloc[-1])

        return np.array(features)

    def build_technical_features(self, prices: pd.DataFrame) -> np.ndarray:
        """Calculate technical indicators"""
        features = []

        if 'RSI' in self.technical_indicators:
            rsi = talib.RSI(prices['close'].values)
            features.append(rsi[-1] / 100.0)  # Normalize to [0,1]

        if 'MACD' in self.technical_indicators:
            macd, signal, hist = talib.MACD(prices['close'].values)
            features.extend([macd[-1], signal[-1], hist[-1]])

        if 'ATR' in self.technical_indicators:
            atr = talib.ATR(
                prices['high'].values,
                prices['low'].values,
                prices['close'].values
            )
            features.append(atr[-1] / prices['close'].iloc[-1])  # Normalize

        return np.array(features)

    def build_fundamental_features(
        self,
        date: pd.Timestamp,
        commodity: str
    ) -> np.ndarray:
        """Extract fundamental features"""
        features = []

        # Seasonality
        features.append(np.sin(2 * np.pi * date.dayofyear / 365))
        features.append(np.cos(2 * np.pi * date.dayofyear / 365))
        features.append(date.weekday() / 6.0)  # Day of week

        # Commodity-specific (would connect to data API in production)
        if commodity == 'crude_oil':
            # Mock inventory data
            inventory_zscore = np.random.randn()  # Replace with real data
            features.append(inventory_zscore)

        elif commodity == 'natural_gas':
            # Mock weather data
            heating_degree_days = np.random.uniform(0, 30)
            features.append(heating_degree_days / 30.0)

        return np.array(features)

    def build_term_structure_features(
        self,
        futures_curve: pd.DataFrame
    ) -> np.ndarray:
        """Extract term structure features"""
        features = []

        # Front-month to second-month spread
        spread_1_2 = (futures_curve.iloc[1] - futures_curve.iloc[0]) / futures_curve.iloc[0]
        features.append(spread_1_2)

        # Roll yield (3-month)
        if len(futures_curve) >= 3:
            roll_yield = (futures_curve.iloc[0] - futures_curve.iloc[2]) / futures_curve.iloc[2]
            features.append(roll_yield)

        # Curve slope
        if len(futures_curve) >= 12:
            slope = np.polyfit(range(12), futures_curve.iloc[:12].values, 1)[0]
            features.append(slope)

        return np.array(features)

    def build_state(
        self,
        prices: pd.DataFrame,
        date: pd.Timestamp,
        commodity: str,
        futures_curve: Optional[pd.DataFrame] = None,
        position: float = 0.0,
        pnl: float = 0.0
    ) -> np.ndarray:
        """Build complete state vector"""
        state_components = []

        # Price features
        state_components.append(self.build_price_features(prices))

        # Technical features
        state_components.append(self.build_technical_features(prices))

        # Fundamental features
        if self.use_fundamentals:
            state_components.append(
                self.build_fundamental_features(date, commodity)
            )

        # Term structure
        if futures_curve is not None:
            state_components.append(
                self.build_term_structure_features(futures_curve)
            )

        # Current position and PnL
        state_components.append(np.array([position, pnl]))

        # Concatenate all features
        state = np.concatenate(state_components)

        # Handle NaN values
        state = np.nan_to_num(state, nan=0.0)

        return state
```

## 2.4 Practical Exercise
Build a complete state representation for natural gas trading that includes:
- Weather forecasts
- Storage levels
- Seasonal patterns
- Technical indicators
```

### Module 3: Reward Function Design
**Learning Objectives:**
- Design effective reward functions for trading
- Balance profitability with risk management
- Avoid common reward engineering pitfalls

**Content Requirements:**
```markdown
# Module 3: Reward Function Design for Trading

## 3.1 The Challenge of Reward Design
- Sparse vs dense rewards in trading
- Credit assignment problem
- Reward hacking and unintended behaviors
- Aligning rewards with trading objectives

## 3.2 Basic Reward Functions
```python
import numpy as np
from typing import Optional, Dict
from dataclasses import dataclass

@dataclass
class TradingMetrics:
    """Container for trading performance metrics"""
    returns: np.ndarray
    positions: np.ndarray
    prices: np.ndarray
    transaction_costs: float = 0.001  # 10 bps

    def calculate_pnl(self) -> np.ndarray:
        """Calculate profit and loss"""
        price_changes = np.diff(self.prices)
        trading_pnl = self.positions[:-1] * price_changes

        # Transaction costs
        position_changes = np.diff(self.positions)
        costs = np.abs(position_changes) * self.prices[1:] * self.transaction_costs

        return trading_pnl - costs

class RewardCalculator:
    """Calculate various reward functions for RL trading"""

    @staticmethod
    def simple_pnl_reward(
        current_price: float,
        previous_price: float,
        position: float,
        transaction_cost: float = 0.001
    ) -> float:
        """Simple PnL-based reward"""
        price_change = current_price - previous_price
        pnl = position * price_change

        # Subtract transaction cost if position changed
        if abs(position) > 0:
            pnl -= abs(position) * current_price * transaction_cost

        return pnl

    @staticmethod
    def sharpe_reward(
        returns: np.ndarray,
        risk_free_rate: float = 0.02,
        periods_per_year: int = 252
    ) -> float:
        """Sharpe ratio-based reward"""
        if len(returns) < 2:
            return 0.0

        excess_returns = returns - risk_free_rate / periods_per_year

        if excess_returns.std() == 0:
            return 0.0

        sharpe = np.sqrt(periods_per_year) * excess_returns.mean() / excess_returns.std()
        return sharpe

    @staticmethod
    def sortino_reward(
        returns: np.ndarray,
        target_return: float = 0.0,
        periods_per_year: int = 252
    ) -> float:
        """Sortino ratio-based reward (penalizes downside volatility)"""
        if len(returns) < 2:
            return 0.0

        excess_returns = returns - target_return
        downside_returns = excess_returns[excess_returns < 0]

        if len(downside_returns) == 0:
            return excess_returns.mean() * 100  # No downside risk

        downside_std = np.sqrt(np.mean(downside_returns ** 2))

        if downside_std == 0:
            return 0.0

        sortino = np.sqrt(periods_per_year) * excess_returns.mean() / downside_std
        return sortino

    @staticmethod
    def drawdown_penalized_reward(
        pnl: float,
        current_equity: float,
        peak_equity: float,
        max_drawdown_threshold: float = 0.1,
        penalty_weight: float = 2.0
    ) -> float:
        """PnL with drawdown penalty"""
        drawdown = (peak_equity - current_equity) / peak_equity

        if drawdown > max_drawdown_threshold:
            # Exponential penalty for exceeding threshold
            penalty = penalty_weight * np.exp(drawdown - max_drawdown_threshold) - penalty_weight
            return pnl - penalty

        return pnl

    @staticmethod
    def risk_adjusted_reward(
        pnl: float,
        position_size: float,
        volatility: float,
        max_position: float = 1.0,
        risk_penalty: float = 0.5
    ) -> float:
        """Reward that penalizes excessive risk-taking"""
        # Base reward is PnL
        reward = pnl

        # Penalize large positions in high volatility
        risk_score = abs(position_size) * volatility / max_position
        reward -= risk_penalty * risk_score

        return reward

    @staticmethod
    def multi_objective_reward(
        metrics: Dict[str, float],
        weights: Dict[str, float]
    ) -> float:
        """Combine multiple objectives"""
        reward = 0.0

        for metric, weight in weights.items():
            if metric in metrics:
                reward += weight * metrics[metric]

        return reward

class AdaptiveRewardShaper:
    """Shape rewards to accelerate learning"""

    def __init__(
        self,
        base_reward_fn,
        shaping_gamma: float = 0.99
    ):
        self.base_reward_fn = base_reward_fn
        self.shaping_gamma = shaping_gamma
        self.potential_fn = self._initialize_potential()

    def _initialize_potential(self):
        """Initialize potential function for shaping"""
        def potential(state):
            # Example: Reward being in profitable positions
            position = state[-2]  # Assuming position is second-to-last
            pnl = state[-1]  # Assuming PnL is last

            return 0.1 * pnl + 0.01 * abs(position)

        return potential

    def shaped_reward(
        self,
        state: np.ndarray,
        action: int,
        next_state: np.ndarray,
        base_reward: float
    ) -> float:
        """Apply reward shaping"""
        # Potential-based shaping (guaranteed to preserve optimal policy)
        shaping_reward = (
            self.shaping_gamma * self.potential_fn(next_state) -
            self.potential_fn(state)
        )

        return base_reward + shaping_reward
```

## 3.3 Advanced Reward Engineering
### Hierarchical Rewards
- Long-term strategic rewards
- Short-term tactical rewards
- Risk management rewards

### Curriculum-Based Rewards
- Start with simple profit maximization
- Gradually introduce risk penalties
- Add complexity as agent improves

## 3.4 Common Pitfalls and Solutions
1. **Reward Hacking**: Agent finds loopholes
   - Solution: Comprehensive testing, constraints

2. **Sparse Rewards**: No signal for learning
   - Solution: Reward shaping, intermediate rewards

3. **Conflicting Objectives**: Risk vs return
   - Solution: Multi-objective optimization

4. **Lookahead Bias**: Using future information
   - Solution: Careful environment design

## Practical Exercise
Design and test three different reward functions for crude oil trading:
1. Simple PnL
2. Sharpe ratio
3. Custom multi-objective function
Compare agent behavior and performance.
```

### Module 4: Building Custom Trading Environments
**Learning Objectives:**
- Implement Gymnasium-compatible trading environments
- Handle realistic market dynamics
- Create multi-asset portfolio environments

**Content Requirements:**
```markdown
# Module 4: Building Custom Trading Environments

## 4.1 Gymnasium Interface Basics
```python
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pandas as pd
from typing import Optional, Tuple, Dict, Any
from dataclasses import dataclass
import yfinance as yf

@dataclass
class MarketConfig:
    """Configuration for market environment"""
    symbol: str
    start_date: str
    end_date: str
    initial_balance: float = 10000.0
    max_position: float = 1.0
    transaction_cost: float = 0.001
    slippage_model: str = 'linear'
    leverage: float = 1.0

class CommodityTradingEnv(gym.Env):
    """Custom Gymnasium environment for commodity trading"""

    metadata = {'render.modes': ['human', 'rgb_array']}

    def __init__(
        self,
        config: MarketConfig,
        window_size: int = 20,
        reward_fn: str = 'sharpe'
    ):
        super().__init__()

        self.config = config
        self.window_size = window_size
        self.reward_fn = reward_fn

        # Load market data
        self.data = self._load_data()
        self.n_steps = len(self.data) - window_size

        # Define action space
        # 0: Sell, 1: Hold, 2: Buy
        self.action_space = spaces.Discrete(3)

        # Define observation space
        # Price features + technical indicators + position
        self.observation_space = spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=(window_size * 5 + 10,),  # OHLCV * window + indicators
            dtype=np.float32
        )

        # Trading state
        self.reset()

    def _load_data(self) -> pd.DataFrame:
        """Load and preprocess market data"""
        # In production, this would connect to a data provider
        ticker = yf.Ticker(self.config.symbol)
        data = ticker.history(
            start=self.config.start_date,
            end=self.config.end_date
        )

        # Add technical indicators
        data['returns'] = data['Close'].pct_change()
        data['sma_20'] = data['Close'].rolling(20).mean()
        data['sma_50'] = data['Close'].rolling(50).mean()
        data['rsi'] = self._calculate_rsi(data['Close'])
        data['atr'] = self._calculate_atr(data)

        return data.dropna()

    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate RSI indicator"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def _calculate_atr(self, data: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calculate Average True Range"""
        high_low = data['High'] - data['Low']
        high_close = np.abs(data['High'] - data['Close'].shift())
        low_close = np.abs(data['Low'] - data['Close'].shift())

        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = ranges.max(axis=1)
        atr = true_range.rolling(window=period).mean()

        return atr

    def _get_observation(self) -> np.ndarray:
        """Get current market observation"""
        # Get price window
        window_data = self.data.iloc[self.current_step:self.current_step + self.window_size]

        # Flatten OHLCV data
        prices = window_data[['Open', 'High', 'Low', 'Close', 'Volume']].values.flatten()

        # Normalize prices
        prices = (prices - prices.mean()) / (prices.std() + 1e-8)

        # Get current indicators
        current_data = self.data.iloc[self.current_step + self.window_size - 1]
        indicators = np.array([
            current_data['returns'],
            current_data['rsi'] / 100.0,
            current_data['atr'] / current_data['Close'],
            (current_data['Close'] - current_data['sma_20']) / current_data['sma_20'],
            (current_data['Close'] - current_data['sma_50']) / current_data['sma_50'],
            self.position,
            self.balance / self.config.initial_balance,
            self.total_pnl / self.config.initial_balance,
            self.n_trades / 100.0,
            self.current_step / self.n_steps
        ])

        observation = np.concatenate([prices, indicators]).astype(np.float32)

        return observation

    def _calculate_reward(self) -> float:
        """Calculate step reward"""
        if self.reward_fn == 'pnl':
            return self.step_pnl

        elif self.reward_fn == 'sharpe':
            if len(self.returns_history) < 2:
                return 0.0
            returns = np.array(self.returns_history)
            if returns.std() == 0:
                return 0.0
            sharpe = np.sqrt(252) * returns.mean() / returns.std()
            return sharpe / 100.0  # Scale down

        elif self.reward_fn == 'risk_adjusted':
            # Combine PnL with risk penalty
            risk_penalty = abs(self.position) * self.current_volatility
            return self.step_pnl - 0.5 * risk_penalty

        else:
            raise ValueError(f"Unknown reward function: {self.reward_fn}")

    def step(self, action: int) -> Tuple[np.ndarray, float, bool, bool, Dict]:
        """Execute trading action"""
        # Map action to position change
        action_map = {0: -1, 1: 0, 2: 1}  # Sell, Hold, Buy
        target_position = action_map[action]

        # Get current and next price
        current_price = self.data.iloc[self.current_step + self.window_size]['Close']
        next_price = self.data.iloc[self.current_step + self.window_size + 1]['Close']

        # Calculate position change and transaction cost
        position_change = target_position - self.position
        transaction_cost = abs(position_change) * current_price * self.config.transaction_cost

        # Apply slippage
        if position_change != 0:
            if self.config.slippage_model == 'linear':
                slippage = abs(position_change) * current_price * 0.0005
                transaction_cost += slippage

        # Update position
        self.position = target_position

        # Calculate PnL
        price_change = next_price - current_price
        self.step_pnl = self.position * price_change - transaction_cost
        self.total_pnl += self.step_pnl
        self.balance += self.step_pnl

        # Update metrics
        if position_change != 0:
            self.n_trades += 1

        step_return = self.step_pnl / self.balance
        self.returns_history.append(step_return)

        # Calculate current volatility for risk management
        if len(self.returns_history) >= 20:
            self.current_volatility = np.std(self.returns_history[-20:]) * np.sqrt(252)

        # Update step
        self.current_step += 1

        # Check if episode is done
        done = (
            self.current_step >= self.n_steps - 1 or
            self.balance <= 0.1 * self.config.initial_balance  # 90% loss
        )

        # Get observation and reward
        observation = self._get_observation()
        reward = self._calculate_reward()

        # Additional info
        info = {
            'pnl': self.step_pnl,
            'total_pnl': self.total_pnl,
            'position': self.position,
            'balance': self.balance,
            'n_trades': self.n_trades,
            'current_price': current_price
        }

        return observation, reward, done, False, info

    def reset(
        self,
        seed: Optional[int] = None,
        options: Optional[Dict] = None
    ) -> Tuple[np.ndarray, Dict]:
        """Reset environment to initial state"""
        super().reset(seed=seed)

        # Reset trading state
        self.current_step = 0
        self.position = 0
        self.balance = self.config.initial_balance
        self.total_pnl = 0.0
        self.step_pnl = 0.0
        self.n_trades = 0
        self.returns_history = []
        self.current_volatility = 0.02  # Initial volatility estimate

        # Random start for training variety
        if options and 'start_step' in options:
            self.current_step = options['start_step']
        else:
            max_start = max(0, self.n_steps - 1000)  # Ensure enough steps
            self.current_step = np.random.randint(0, max_start + 1)

        observation = self._get_observation()
        info = {'start_step': self.current_step}

        return observation, info

    def render(self, mode: str = 'human'):
        """Render the environment"""
        if mode == 'human':
            print(f"Step: {self.current_step}, Position: {self.position}, "
                  f"Balance: ${self.balance:.2f}, PnL: ${self.total_pnl:.2f}")

class MultiAssetTradingEnv(gym.Env):
    """Portfolio trading environment for multiple commodities"""

    def __init__(
        self,
        symbols: List[str],
        config: MarketConfig,
        window_size: int = 20,
        correlation_window: int = 60
    ):
        super().__init__()

        self.symbols = symbols
        self.n_assets = len(symbols)
        self.config = config
        self.window_size = window_size
        self.correlation_window = correlation_window

        # Load data for all assets
        self.data = self._load_multi_asset_data()

        # Action space: position for each asset [-1, 0, 1]
        self.action_space = spaces.MultiDiscrete([3] * self.n_assets)

        # Observation space: features for each asset + correlation matrix
        single_asset_features = window_size * 5 + 10
        correlation_features = self.n_assets * (self.n_assets - 1) // 2
        total_features = single_asset_features * self.n_assets + correlation_features

        self.observation_space = spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=(total_features,),
            dtype=np.float32
        )

        self.reset()

    def _load_multi_asset_data(self) -> Dict[str, pd.DataFrame]:
        """Load data for all assets"""
        data = {}
        for symbol in self.symbols:
            ticker = yf.Ticker(symbol)
            df = ticker.history(
                start=self.config.start_date,
                end=self.config.end_date
            )
            df['returns'] = df['Close'].pct_change()
            data[symbol] = df

        # Align indices
        common_index = data[self.symbols[0]].index
        for symbol in self.symbols[1:]:
            common_index = common_index.intersection(data[symbol].index)

        for symbol in self.symbols:
            data[symbol] = data[symbol].loc[common_index]

        return data

    def _calculate_correlation_features(self) -> np.ndarray:
        """Calculate correlation matrix features"""
        returns = pd.DataFrame()

        for symbol in self.symbols:
            window_end = self.current_step + self.window_size
            window_start = max(0, window_end - self.correlation_window)
            returns[symbol] = self.data[symbol].iloc[window_start:window_end]['returns']

        # Get upper triangular correlation matrix
        corr_matrix = returns.corr().values
        upper_tri = corr_matrix[np.triu_indices(self.n_assets, k=1)]

        return upper_tri

    def _get_observation(self) -> np.ndarray:
        """Get portfolio observation"""
        observations = []

        # Get features for each asset
        for symbol in self.symbols:
            asset_data = self.data[symbol].iloc[
                self.current_step:self.current_step + self.window_size
            ]

            # Price features
            prices = asset_data[['Open', 'High', 'Low', 'Close', 'Volume']].values.flatten()
            prices = (prices - prices.mean()) / (prices.std() + 1e-8)

            # Current metrics
            current = asset_data.iloc[-1]
            metrics = np.array([
                current['returns'],
                self.positions[symbol],
                self.asset_pnl[symbol] / self.config.initial_balance
            ])

            observations.extend(prices)
            observations.extend(metrics)

        # Add correlation features
        correlations = self._calculate_correlation_features()
        observations.extend(correlations)

        # Add portfolio-level metrics
        portfolio_metrics = np.array([
            self.total_pnl / self.config.initial_balance,
            self.balance / self.config.initial_balance,
            np.sum(list(self.positions.values())) / self.n_assets,  # Avg position
            self.current_step / len(self.data[self.symbols[0]])
        ])
        observations.extend(portfolio_metrics)

        return np.array(observations, dtype=np.float32)

    # ... Additional methods for portfolio management ...

class SpreadTradingEnv(gym.Env):
    """Environment for spread trading between commodities"""

    def __init__(
        self,
        front_contract: str,
        back_contract: str,
        config: MarketConfig,
        spread_threshold: float = 2.0  # Z-score threshold
    ):
        super().__init__()

        self.front_contract = front_contract
        self.back_contract = back_contract
        self.config = config
        self.spread_threshold = spread_threshold

        # Load data
        self.front_data = self._load_contract_data(front_contract)
        self.back_data = self._load_contract_data(back_contract)
        self._calculate_spread()

        # Action space: Long spread, Flat, Short spread
        self.action_space = spaces.Discrete(3)

        # Observation space
        self.observation_space = spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=(50,),  # Spread features + contract features
            dtype=np.float32
        )

        self.reset()

    def _calculate_spread(self):
        """Calculate spread time series"""
        self.spread = self.front_data['Close'] - self.back_data['Close']
        self.spread_returns = self.spread.pct_change()

        # Calculate rolling statistics
        self.spread_mean = self.spread.rolling(20).mean()
        self.spread_std = self.spread.rolling(20).std()
        self.spread_zscore = (self.spread - self.spread_mean) / self.spread_std

    # ... Additional spread trading methods ...
```

## 4.2 Realistic Market Simulation
- Order book simulation
- Market impact modeling
- Latency and execution delays
- Partial fills and rejections

## 4.3 Environment Testing and Validation
```python
def validate_environment(env_class, config):
    """Test suite for trading environments"""

    env = env_class(config)

    # Test 1: Check spaces
    assert isinstance(env.action_space, spaces.Space)
    assert isinstance(env.observation_space, spaces.Space)

    # Test 2: Reset
    obs, info = env.reset()
    assert obs.shape == env.observation_space.shape

    # Test 3: Step
    for _ in range(10):
        action = env.action_space.sample()
        obs, reward, done, truncated, info = env.step(action)
        assert obs.shape == env.observation_space.shape
        assert isinstance(reward, (float, int))

        if done:
            obs, info = env.reset()

    # Test 4: Determinism
    env1 = env_class(config)
    env2 = env_class(config)

    obs1, _ = env1.reset(seed=42)
    obs2, _ = env2.reset(seed=42)
    np.testing.assert_array_equal(obs1, obs2)

    print("Environment validation passed!")
```

## Practical Exercise
Build a custom environment for WTI-Brent spread trading with:
- Cointegration-based signals
- Dynamic position sizing
- Risk limits
```

### Module 5: Value-Based Methods (Q-Learning, DQN)
**Learning Objectives:**
- Implement Q-learning for discrete trading actions
- Build Deep Q-Networks for complex state spaces
- Apply advanced DQN variants

**Content Requirements:**
```markdown
# Module 5: Value-Based Methods for Trading

## 5.1 Q-Learning Fundamentals
```python
import numpy as np
from collections import defaultdict, deque
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from typing import Tuple, List
import random

class TabularQLearning:
    """Tabular Q-learning for discrete states and actions"""

    def __init__(
        self,
        n_states: int,
        n_actions: int,
        learning_rate: float = 0.1,
        discount: float = 0.99,
        epsilon: float = 0.1
    ):
        self.n_states = n_states
        self.n_actions = n_actions
        self.lr = learning_rate
        self.gamma = discount
        self.epsilon = epsilon

        # Initialize Q-table
        self.q_table = defaultdict(lambda: np.zeros(n_actions))

    def get_action(self, state: int, training: bool = True) -> int:
        """Epsilon-greedy action selection"""
        if training and random.random() < self.epsilon:
            return random.randint(0, self.n_actions - 1)

        return np.argmax(self.q_table[state])

    def update(
        self,
        state: int,
        action: int,
        reward: float,
        next_state: int,
        done: bool
    ):
        """Q-learning update rule"""
        current_q = self.q_table[state][action]

        if done:
            target = reward
        else:
            target = reward + self.gamma * np.max(self.q_table[next_state])

        # TD error
        td_error = target - current_q

        # Update Q-value
        self.q_table[state][action] += self.lr * td_error

        return td_error

## 5.2 Deep Q-Networks (DQN)
class DQN(nn.Module):
    """Deep Q-Network for trading"""

    def __init__(
        self,
        input_dim: int,
        hidden_dims: List[int],
        output_dim: int,
        dropout: float = 0.1
    ):
        super(DQN, self).__init__()

        layers = []
        prev_dim = input_dim

        for hidden_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.ReLU(),
                nn.Dropout(dropout),
                nn.BatchNorm1d(hidden_dim)
            ])
            prev_dim = hidden_dim

        layers.append(nn.Linear(prev_dim, output_dim))

        self.network = nn.Sequential(*layers)

        # Initialize weights
        self.apply(self._init_weights)

    def _init_weights(self, module):
        if isinstance(module, nn.Linear):
            nn.init.xavier_uniform_(module.weight)
            nn.init.constant_(module.bias, 0.0)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)

class ReplayBuffer:
    """Experience replay buffer"""

    def __init__(self, capacity: int):
        self.buffer = deque(maxlen=capacity)

    def push(
        self,
        state: np.ndarray,
        action: int,
        reward: float,
        next_state: np.ndarray,
        done: bool
    ):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size: int) -> Tuple:
        batch = random.sample(self.buffer, batch_size)
        state, action, reward, next_state, done = zip(*batch)

        return (
            np.array(state),
            np.array(action),
            np.array(reward),
            np.array(next_state),
            np.array(done)
        )

    def __len__(self):
        return len(self.buffer)

class DQNAgent:
    """DQN agent for commodity trading"""

    def __init__(
        self,
        state_dim: int,
        action_dim: int,
        learning_rate: float = 1e-3,
        discount: float = 0.99,
        epsilon_start: float = 1.0,
        epsilon_end: float = 0.01,
        epsilon_decay: int = 1000,
        tau: float = 0.001,
        batch_size: int = 64,
        buffer_size: int = 10000,
        device: str = 'cuda' if torch.cuda.is_available() else 'cpu'
    ):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.gamma = discount
        self.tau = tau
        self.batch_size = batch_size
        self.device = torch.device(device)

        # Networks
        self.q_network = DQN(
            state_dim,
            [256, 128, 64],
            action_dim
        ).to(self.device)

        self.target_network = DQN(
            state_dim,
            [256, 128, 64],
            action_dim
        ).to(self.device)

        self.target_network.load_state_dict(self.q_network.state_dict())

        # Optimizer
        self.optimizer = optim.Adam(
            self.q_network.parameters(),
            lr=learning_rate
        )

        # Replay buffer
        self.replay_buffer = ReplayBuffer(buffer_size)

        # Epsilon schedule
        self.epsilon = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay = epsilon_decay
        self.steps = 0

    def get_action(self, state: np.ndarray, training: bool = True) -> int:
        """Select action using epsilon-greedy policy"""
        if training and random.random() < self.epsilon:
            return random.randint(0, self.action_dim - 1)

        with torch.no_grad():
            state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
            q_values = self.q_network(state_tensor)
            return q_values.argmax(dim=1).item()

    def update(self):
        """Train the Q-network"""
        if len(self.replay_buffer) < self.batch_size:
            return

        # Sample batch
        states, actions, rewards, next_states, dones = self.replay_buffer.sample(
            self.batch_size
        )

        # Convert to tensors
        states = torch.FloatTensor(states).to(self.device)
        actions = torch.LongTensor(actions).to(self.device)
        rewards = torch.FloatTensor(rewards).to(self.device)
        next_states = torch.FloatTensor(next_states).to(self.device)
        dones = torch.FloatTensor(dones).to(self.device)

        # Current Q values
        current_q_values = self.q_network(states).gather(1, actions.unsqueeze(1))

        # Next Q values from target network
        with torch.no_grad():
            next_q_values = self.target_network(next_states).max(1)[0]
            target_q_values = rewards + (1 - dones) * self.gamma * next_q_values

        # Compute loss
        loss = F.mse_loss(current_q_values.squeeze(), target_q_values)

        # Optimize
        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.q_network.parameters(), 1.0)
        self.optimizer.step()

        # Update target network (soft update)
        for target_param, param in zip(
            self.target_network.parameters(),
            self.q_network.parameters()
        ):
            target_param.data.copy_(
                self.tau * param.data + (1 - self.tau) * target_param.data
            )

        # Update epsilon
        self.epsilon = max(
            self.epsilon_end,
            self.epsilon - (self.epsilon - self.epsilon_end) / self.epsilon_decay
        )

        self.steps += 1

        return loss.item()

## 5.3 Advanced DQN Variants
class DoubleDQN(DQNAgent):
    """Double DQN to reduce overestimation bias"""

    def update(self):
        if len(self.replay_buffer) < self.batch_size:
            return

        states, actions, rewards, next_states, dones = self.replay_buffer.sample(
            self.batch_size
        )

        states = torch.FloatTensor(states).to(self.device)
        actions = torch.LongTensor(actions).to(self.device)
        rewards = torch.FloatTensor(rewards).to(self.device)
        next_states = torch.FloatTensor(next_states).to(self.device)
        dones = torch.FloatTensor(dones).to(self.device)

        current_q_values = self.q_network(states).gather(1, actions.unsqueeze(1))

        # Double DQN: use online network to select actions
        with torch.no_grad():
            next_actions = self.q_network(next_states).argmax(1)
            next_q_values = self.target_network(next_states).gather(
                1, next_actions.unsqueeze(1)
            ).squeeze()
            target_q_values = rewards + (1 - dones) * self.gamma * next_q_values

        loss = F.mse_loss(current_q_values.squeeze(), target_q_values)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # Soft update target network
        for target_param, param in zip(
            self.target_network.parameters(),
            self.q_network.parameters()
        ):
            target_param.data.copy_(
                self.tau * param.data + (1 - self.tau) * target_param.data
            )

        return loss.item()

class DuelingDQN(nn.Module):
    """Dueling architecture for value and advantage separation"""

    def __init__(
        self,
        input_dim: int,
        hidden_dims: List[int],
        output_dim: int
    ):
        super(DuelingDQN, self).__init__()

        # Shared layers
        shared_layers = []
        prev_dim = input_dim

        for hidden_dim in hidden_dims[:-1]:
            shared_layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.ReLU()
            ])
            prev_dim = hidden_dim

        self.shared = nn.Sequential(*shared_layers)

        # Value stream
        self.value_stream = nn.Sequential(
            nn.Linear(prev_dim, hidden_dims[-1]),
            nn.ReLU(),
            nn.Linear(hidden_dims[-1], 1)
        )

        # Advantage stream
        self.advantage_stream = nn.Sequential(
            nn.Linear(prev_dim, hidden_dims[-1]),
            nn.ReLU(),
            nn.Linear(hidden_dims[-1], output_dim)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        shared_features = self.shared(x)
        value = self.value_stream(shared_features)
        advantage = self.advantage_stream(shared_features)

        # Combine value and advantage
        q_values = value + advantage - advantage.mean(dim=1, keepdim=True)

        return q_values

## 5.4 Training Loop Example
def train_dqn_trader(
    env,
    agent: DQNAgent,
    n_episodes: int = 1000,
    save_freq: int = 100
):
    """Train DQN agent for commodity trading"""

    episode_rewards = []
    episode_lengths = []
    losses = []

    for episode in range(n_episodes):
        state, _ = env.reset()
        episode_reward = 0
        episode_length = 0

        while True:
            # Select action
            action = agent.get_action(state)

            # Execute action
            next_state, reward, done, truncated, info = env.step(action)

            # Store transition
            agent.replay_buffer.push(state, action, reward, next_state, done)

            # Update agent
            loss = agent.update()
            if loss is not None:
                losses.append(loss)

            episode_reward += reward
            episode_length += 1
            state = next_state

            if done or truncated:
                break

        episode_rewards.append(episode_reward)
        episode_lengths.append(episode_length)

        # Log progress
        if (episode + 1) % 10 == 0:
            avg_reward = np.mean(episode_rewards[-10:])
            avg_length = np.mean(episode_lengths[-10:])
            print(f"Episode {episode + 1}/{n_episodes}, "
                  f"Avg Reward: {avg_reward:.2f}, "
                  f"Avg Length: {avg_length:.1f}, "
                  f"Epsilon: {agent.epsilon:.3f}")

        # Save model
        if (episode + 1) % save_freq == 0:
            torch.save(
                agent.q_network.state_dict(),
                f"dqn_trader_ep{episode + 1}.pth"
            )

    return episode_rewards, losses

## Practical Exercise
Implement and compare:
1. Vanilla DQN
2. Double DQN
3. Dueling DQN
On gold futures trading with different reward functions.
```

### Module 6: Policy Gradient Methods
**Learning Objectives:**
- Understand policy gradient theorem
- Implement REINFORCE and Actor-Critic
- Apply policy gradients to continuous action spaces

**Content Requirements:**
```markdown
# Module 6: Policy Gradient Methods for Trading

## 6.1 Policy Gradient Fundamentals
```python
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.distributions import Categorical, Normal
import numpy as np
from typing import List, Tuple

class PolicyNetwork(nn.Module):
    """Neural network for policy representation"""

    def __init__(
        self,
        input_dim: int,
        hidden_dims: List[int],
        output_dim: int,
        continuous: bool = False
    ):
        super(PolicyNetwork, self).__init__()

        self.continuous = continuous

        layers = []
        prev_dim = input_dim

        for hidden_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.ReLU(),
                nn.LayerNorm(hidden_dim)
            ])
            prev_dim = hidden_dim

        self.shared = nn.Sequential(*layers)

        if continuous:
            # Output mean and std for Gaussian policy
            self.mean_head = nn.Linear(prev_dim, output_dim)
            self.log_std_head = nn.Linear(prev_dim, output_dim)
        else:
            # Output logits for categorical policy
            self.logits_head = nn.Linear(prev_dim, output_dim)

    def forward(self, state: torch.Tensor):
        features = self.shared(state)

        if self.continuous:
            mean = self.mean_head(features)
            log_std = self.log_std_head(features)
            std = torch.exp(torch.clamp(log_std, -20, 2))
            return mean, std
        else:
            logits = self.logits_head(features)
            return F.softmax(logits, dim=-1)

class REINFORCE:
    """REINFORCE algorithm for discrete actions"""

    def __init__(
        self,
        state_dim: int,
        action_dim: int,
        learning_rate: float = 1e-3,
        gamma: float = 0.99
    ):
        self.gamma = gamma

        self.policy = PolicyNetwork(
            state_dim,
            [128, 64],
            action_dim,
            continuous=False
        )

        self.optimizer = optim.Adam(
            self.policy.parameters(),
            lr=learning_rate
        )

        self.saved_log_probs = []
        self.rewards = []

    def select_action(self, state: np.ndarray) -> int:
        """Sample action from policy"""
        state_tensor = torch.FloatTensor(state).unsqueeze(0)
        probs = self.policy(state_tensor)

        dist = Categorical(probs)
        action = dist.sample()

        self.saved_log_probs.append(dist.log_prob(action))

        return action.item()

    def update(self):
        """Update policy using collected trajectory"""
        # Calculate discounted returns
        returns = []
        G = 0

        for reward in reversed(self.rewards):
            G = reward + self.gamma * G
            returns.insert(0, G)

        returns = torch.tensor(returns)

        # Normalize returns for stability
        returns = (returns - returns.mean()) / (returns.std() + 1e-8)

        # Calculate policy gradient
        policy_loss = []
        for log_prob, G in zip(self.saved_log_probs, returns):
            policy_loss.append(-log_prob * G)

        policy_loss = torch.cat(policy_loss).sum()

        # Update policy
        self.optimizer.zero_grad()
        policy_loss.backward()
        torch.nn.utils.clip_grad_norm_(self.policy.parameters(), 1.0)
        self.optimizer.step()

        # Clear episode data
        self.saved_log_probs = []
        self.rewards = []

        return policy_loss.item()

## 6.2 Actor-Critic Methods
class ActorCritic(nn.Module):
    """Combined actor-critic network"""

    def __init__(
        self,
        input_dim: int,
        hidden_dims: List[int],
        action_dim: int
    ):
        super(ActorCritic, self).__init__()

        # Shared layers
        layers = []
        prev_dim = input_dim

        for hidden_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.ReLU(),
                nn.LayerNorm(hidden_dim)
            ])
            prev_dim = hidden_dim

        self.shared = nn.Sequential(*layers)

        # Actor head (policy)
        self.actor = nn.Linear(prev_dim, action_dim)

        # Critic head (value function)
        self.critic = nn.Linear(prev_dim, 1)

    def forward(self, state: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        features = self.shared(state)
        action_probs = F.softmax(self.actor(features), dim=-1)
        state_value = self.critic(features)
        return action_probs, state_value

class A2C:
    """Advantage Actor-Critic for trading"""

    def __init__(
        self,
        state_dim: int,
        action_dim: int,
        learning_rate: float = 1e-3,
        gamma: float = 0.99,
        value_coef: float = 0.5,
        entropy_coef: float = 0.01
    ):
        self.gamma = gamma
        self.value_coef = value_coef
        self.entropy_coef = entropy_coef

        self.ac_network = ActorCritic(
            state_dim,
            [256, 128],
            action_dim
        )

        self.optimizer = optim.Adam(
            self.ac_network.parameters(),
            lr=learning_rate
        )

    def get_action(self, state: np.ndarray) -> Tuple[int, float, float]:
        """Get action, log probability, and value estimate"""
        state_tensor = torch.FloatTensor(state).unsqueeze(0)

        action_probs, value = self.ac_network(state_tensor)
        dist = Categorical(action_probs)

        action = dist.sample()
        log_prob = dist.log_prob(action)
        entropy = dist.entropy()

        return action.item(), log_prob, value.item(), entropy

    def update(
        self,
        states: List[np.ndarray],
        actions: List[int],
        rewards: List[float],
        next_states: List[np.ndarray],
        dones: List[bool],
        log_probs: List[torch.Tensor],
        values: List[float],
        entropies: List[torch.Tensor]
    ):
        """Update actor and critic networks"""
        # Convert to tensors
        states = torch.FloatTensor(states)
        actions = torch.LongTensor(actions)
        rewards = torch.FloatTensor(rewards)
        next_states = torch.FloatTensor(next_states)
        dones = torch.FloatTensor(dones)
        log_probs = torch.cat(log_probs)
        values = torch.FloatTensor(values)
        entropies = torch.cat(entropies)

        # Calculate returns and advantages
        with torch.no_grad():
            _, next_values = self.ac_network(next_states)
            next_values = next_values.squeeze()
            returns = rewards + self.gamma * next_values * (1 - dones)
            advantages = returns - values

            # Normalize advantages
            advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

        # Calculate losses
        policy_loss = -(log_probs * advantages).mean()
        value_loss = F.mse_loss(values, returns)
        entropy_loss = -entropies.mean()

        # Total loss
        total_loss = (
            policy_loss +
            self.value_coef * value_loss +
            self.entropy_coef * entropy_loss
        )

        # Update networks
        self.optimizer.zero_grad()
        total_loss.backward()
        torch.nn.utils.clip_grad_norm_(self.ac_network.parameters(), 0.5)
        self.optimizer.step()

        return {
            'policy_loss': policy_loss.item(),
            'value_loss': value_loss.item(),
            'entropy': -entropy_loss.item(),
            'total_loss': total_loss.item()
        }

## 6.3 Continuous Action Spaces
class ContinuousActorCritic(nn.Module):
    """Actor-Critic for continuous action spaces"""

    def __init__(
        self,
        state_dim: int,
        action_dim: int,
        hidden_dims: List[int] = [256, 128],
        action_bound: float = 1.0
    ):
        super(ContinuousActorCritic, self).__init__()

        self.action_bound = action_bound

        # Build actor network
        actor_layers = []
        prev_dim = state_dim

        for hidden_dim in hidden_dims:
            actor_layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.ReLU()
            ])
            prev_dim = hidden_dim

        self.actor_shared = nn.Sequential(*actor_layers)
        self.actor_mean = nn.Linear(prev_dim, action_dim)
        self.actor_log_std = nn.Linear(prev_dim, action_dim)

        # Build critic network
        critic_layers = []
        prev_dim = state_dim

        for hidden_dim in hidden_dims:
            critic_layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.ReLU()
            ])
            prev_dim = hidden_dim

        self.critic = nn.Sequential(
            *critic_layers,
            nn.Linear(prev_dim, 1)
        )

    def forward(self, state: torch.Tensor):
        # Actor
        actor_features = self.actor_shared(state)
        mean = self.actor_mean(actor_features)
        mean = torch.tanh(mean) * self.action_bound
        log_std = self.actor_log_std(actor_features)
        log_std = torch.clamp(log_std, -20, 2)
        std = torch.exp(log_std)

        # Critic
        value = self.critic(state)

        return mean, std, value

    def get_action(self, state: torch.Tensor):
        mean, std, value = self.forward(state)
        dist = Normal(mean, std)
        action = dist.sample()
        log_prob = dist.log_prob(action).sum(dim=-1)

        return action, log_prob, value

## 6.4 Training Natural Gas Trading Agent
def train_policy_gradient_trader(
    env,
    agent,
    n_episodes: int = 1000,
    max_steps: int = 1000
):
    """Train policy gradient agent for commodity trading"""

    episode_rewards = []

    for episode in range(n_episodes):
        state, _ = env.reset()
        episode_reward = 0

        states = []
        actions = []
        rewards = []
        log_probs = []
        values = []
        entropies = []

        for step in range(max_steps):
            # Get action from policy
            if isinstance(agent, A2C):
                action, log_prob, value, entropy = agent.get_action(state)
                log_probs.append(log_prob)
                values.append(value)
                entropies.append(entropy)
            else:
                action = agent.select_action(state)

            # Execute action
            next_state, reward, done, truncated, info = env.step(action)

            # Store transition
            states.append(state)
            actions.append(action)
            rewards.append(reward)

            episode_reward += reward
            state = next_state

            if done or truncated:
                break

        # Update agent
        if isinstance(agent, A2C):
            # Prepare next states and dones
            next_states = states[1:] + [state]
            dones = [False] * (len(states) - 1) + [done]

            losses = agent.update(
                states, actions, rewards, next_states, dones,
                log_probs, values, entropies
            )
        else:
            agent.rewards = rewards
            loss = agent.update()

        episode_rewards.append(episode_reward)

        # Log progress
        if (episode + 1) % 10 == 0:
            avg_reward = np.mean(episode_rewards[-10:])
            print(f"Episode {episode + 1}/{n_episodes}, "
                  f"Avg Reward: {avg_reward:.3f}")

    return episode_rewards

## Practical Exercise
Implement a continuous action policy gradient agent for natural gas trading with:
- Position sizing as continuous action
- Risk-adjusted reward function
- Comparison with discrete action baseline
```

### Module 7: Advanced Algorithms (PPO, SAC)
**Learning Objectives:**
- Master Proximal Policy Optimization
- Implement Soft Actor-Critic for maximum entropy RL
- Apply advanced algorithms to portfolio management

**Content Requirements:**
```markdown
# Module 7: Advanced RL Algorithms for Trading

## 7.1 Proximal Policy Optimization (PPO)
```python
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.distributions import Categorical, Normal
import numpy as np
from typing import Dict, List, Tuple

class PPOMemory:
    """Memory buffer for PPO"""

    def __init__(self):
        self.states = []
        self.actions = []
        self.rewards = []
        self.log_probs = []
        self.values = []
        self.dones = []
        self.advantages = []
        self.returns = []

    def store(
        self,
        state: np.ndarray,
        action: int,
        reward: float,
        log_prob: torch.Tensor,
        value: torch.Tensor,
        done: bool
    ):
        self.states.append(state)
        self.actions.append(action)
        self.rewards.append(reward)
        self.log_probs.append(log_prob)
        self.values.append(value)
        self.dones.append(done)

    def compute_returns_and_advantages(
        self,
        last_value: torch.Tensor,
        gamma: float = 0.99,
        lam: float = 0.95
    ):
        """Calculate GAE returns and advantages"""
        # Convert to tensors
        rewards = torch.FloatTensor(self.rewards)
        values = torch.cat(self.values)
        dones = torch.FloatTensor(self.dones)

        # Calculate returns and advantages using GAE
        advantages = []
        returns = []
        gae = 0

        # Add last value for calculation
        values = torch.cat([values, last_value])

        for t in reversed(range(len(rewards))):
            if t == len(rewards) - 1:
                next_value = last_value
            else:
                next_value = values[t + 1]

            delta = rewards[t] + gamma * next_value * (1 - dones[t]) - values[t]
            gae = delta + gamma * lam * (1 - dones[t]) * gae

            advantages.insert(0, gae)
            returns.insert(0, gae + values[t])

        self.advantages = torch.FloatTensor(advantages)
        self.returns = torch.FloatTensor(returns)

    def get_batches(self, batch_size: int):
        """Generate random batches for training"""
        n_states = len(self.states)
        batch_start = np.arange(0, n_states, batch_size)
        indices = np.arange(n_states)
        np.random.shuffle(indices)

        batches = [indices[i:i + batch_size] for i in batch_start]

        states = torch.FloatTensor(self.states)
        actions = torch.LongTensor(self.actions)
        log_probs = torch.cat(self.log_probs)

        for batch in batches:
            yield (
                states[batch],
                actions[batch],
                log_probs[batch],
                self.advantages[batch],
                self.returns[batch]
            )

    def clear(self):
        """Clear memory after update"""
        self.states = []
        self.actions = []
        self.rewards = []
        self.log_probs = []
        self.values = []
        self.dones = []
        self.advantages = []
        self.returns = []

class PPONetwork(nn.Module):
    """Neural network for PPO"""

    def __init__(
        self,
        input_dim: int,
        action_dim: int,
        hidden_dims: List[int] = [256, 256],
        activation: str = 'tanh'
    ):
        super(PPONetwork, self).__init__()

        # Select activation function
        if activation == 'relu':
            self.activation = nn.ReLU
        elif activation == 'tanh':
            self.activation = nn.Tanh
        else:
            raise ValueError(f"Unknown activation: {activation}")

        # Build shared layers
        layers = []
        prev_dim = input_dim

        for hidden_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                self.activation(),
                nn.LayerNorm(hidden_dim)
            ])
            prev_dim = hidden_dim

        self.shared = nn.Sequential(*layers)

        # Actor head
        self.actor = nn.Linear(prev_dim, action_dim)

        # Critic head
        self.critic = nn.Linear(prev_dim, 1)

    def forward(self, state: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        features = self.shared(state)

        # Get action probabilities
        action_logits = self.actor(features)
        action_probs = F.softmax(action_logits, dim=-1)

        # Get value estimate
        value = self.critic(features)

        return action_probs, value

class PPOAgent:
    """PPO agent for commodity trading"""

    def __init__(
        self,
        state_dim: int,
        action_dim: int,
        learning_rate: float = 3e-4,
        gamma: float = 0.99,
        lam: float = 0.95,
        epsilon: float = 0.2,
        c1: float = 0.5,  # Value loss coefficient
        c2: float = 0.01,  # Entropy coefficient
        epochs: int = 10,
        batch_size: int = 64,
        device: str = 'cuda' if torch.cuda.is_available() else 'cpu'
    ):
        self.gamma = gamma
        self.lam = lam
        self.epsilon = epsilon
        self.c1 = c1
        self.c2 = c2
        self.epochs = epochs
        self.batch_size = batch_size
        self.device = torch.device(device)

        # Initialize network
        self.network = PPONetwork(
            state_dim,
            action_dim
        ).to(self.device)

        # Initialize optimizer
        self.optimizer = optim.Adam(
            self.network.parameters(),
            lr=learning_rate,
            eps=1e-5
        )

        # Initialize memory
        self.memory = PPOMemory()

    def get_action(
        self,
        state: np.ndarray,
        training: bool = True
    ) -> Tuple[int, torch.Tensor, torch.Tensor]:
        """Select action using current policy"""
        state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)

        with torch.no_grad():
            action_probs, value = self.network(state_tensor)

        if training:
            dist = Categorical(action_probs)
            action = dist.sample()
            log_prob = dist.log_prob(action)
        else:
            action = action_probs.argmax(dim=-1)
            log_prob = torch.log(action_probs.squeeze()[action])

        return action.item(), log_prob, value

    def update(self):
        """Update policy using PPO"""
        # Get last value for GAE calculation
        if len(self.memory.states) == 0:
            return {}

        last_state = torch.FloatTensor(
            self.memory.states[-1]
        ).unsqueeze(0).to(self.device)

        with torch.no_grad():
            _, last_value = self.network(last_state)

        # Compute returns and advantages
        self.memory.compute_returns_and_advantages(
            last_value,
            self.gamma,
            self.lam
        )

        # Training loop
        total_policy_loss = 0
        total_value_loss = 0
        total_entropy = 0
        n_updates = 0

        for epoch in range(self.epochs):
            for states, actions, old_log_probs, advantages, returns in \
                    self.memory.get_batches(self.batch_size):

                states = states.to(self.device)
                actions = actions.to(self.device)
                old_log_probs = old_log_probs.to(self.device)
                advantages = advantages.to(self.device)
                returns = returns.to(self.device)

                # Get current policy predictions
                action_probs, values = self.network(states)
                dist = Categorical(action_probs)

                # Calculate log probabilities
                log_probs = dist.log_prob(actions)

                # Calculate ratio for PPO
                ratio = torch.exp(log_probs - old_log_probs)

                # Calculate surrogate losses
                surr1 = ratio * advantages
                surr2 = torch.clamp(ratio, 1 - self.epsilon, 1 + self.epsilon) * advantages

                # Policy loss (negative because we maximize)
                policy_loss = -torch.min(surr1, surr2).mean()

                # Value loss
                value_loss = F.mse_loss(values.squeeze(), returns)

                # Entropy bonus
                entropy = dist.entropy().mean()

                # Total loss
                loss = policy_loss + self.c1 * value_loss - self.c2 * entropy

                # Update network
                self.optimizer.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.network.parameters(), 0.5)
                self.optimizer.step()

                # Track losses
                total_policy_loss += policy_loss.item()
                total_value_loss += value_loss.item()
                total_entropy += entropy.item()
                n_updates += 1

        # Clear memory after update
        self.memory.clear()

        return {
            'policy_loss': total_policy_loss / n_updates,
            'value_loss': total_value_loss / n_updates,
            'entropy': total_entropy / n_updates
        }

## 7.2 Soft Actor-Critic (SAC)
class SACGaussianActor(nn.Module):
    """Gaussian policy for continuous actions"""

    def __init__(
        self,
        state_dim: int,
        action_dim: int,
        hidden_dims: List[int] = [256, 256],
        action_bound: float = 1.0,
        log_std_min: float = -20,
        log_std_max: float = 2
    ):
        super(SACGaussianActor, self).__init__()

        self.action_bound = action_bound
        self.log_std_min = log_std_min
        self.log_std_max = log_std_max

        layers = []
        prev_dim = state_dim

        for hidden_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.ReLU(),
                nn.LayerNorm(hidden_dim)
            ])
            prev_dim = hidden_dim

        self.shared = nn.Sequential(*layers)
        self.mean_head = nn.Linear(prev_dim, action_dim)
        self.log_std_head = nn.Linear(prev_dim, action_dim)

    def forward(self, state: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        features = self.shared(state)
        mean = self.mean_head(features)
        log_std = self.log_std_head(features)
        log_std = torch.clamp(log_std, self.log_std_min, self.log_std_max)

        return mean, log_std

    def sample(
        self,
        state: torch.Tensor,
        deterministic: bool = False
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """Sample action from policy"""
        mean, log_std = self.forward(state)
        std = torch.exp(log_std)

        if deterministic:
            action = torch.tanh(mean) * self.action_bound
            log_prob = None
        else:
            dist = Normal(mean, std)
            z = dist.rsample()  # Reparameterization trick
            action = torch.tanh(z) * self.action_bound

            # Calculate log probability with correction for tanh
            log_prob = dist.log_prob(z)
            log_prob -= torch.log(
                self.action_bound * (1 - action.pow(2)) + 1e-6
            )
            log_prob = log_prob.sum(dim=-1, keepdim=True)

        return action, log_prob

class SACCritic(nn.Module):
    """Twin Q-networks for SAC"""

    def __init__(
        self,
        state_dim: int,
        action_dim: int,
        hidden_dims: List[int] = [256, 256]
    ):
        super(SACCritic, self).__init__()

        # Q1 network
        q1_layers = []
        prev_dim = state_dim + action_dim

        for hidden_dim in hidden_dims:
            q1_layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.ReLU()
            ])
            prev_dim = hidden_dim

        q1_layers.append(nn.Linear(prev_dim, 1))
        self.q1 = nn.Sequential(*q1_layers)

        # Q2 network
        q2_layers = []
        prev_dim = state_dim + action_dim

        for hidden_dim in hidden_dims:
            q2_layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.ReLU()
            ])
            prev_dim = hidden_dim

        q2_layers.append(nn.Linear(prev_dim, 1))
        self.q2 = nn.Sequential(*q2_layers)

    def forward(
        self,
        state: torch.Tensor,
        action: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        state_action = torch.cat([state, action], dim=-1)
        q1_value = self.q1(state_action)
        q2_value = self.q2(state_action)

        return q1_value, q2_value

class SACAgent:
    """Soft Actor-Critic for continuous control in trading"""

    def __init__(
        self,
        state_dim: int,
        action_dim: int,
        action_bound: float = 1.0,
        learning_rate: float = 3e-4,
        gamma: float = 0.99,
        tau: float = 0.005,
        alpha: float = 0.2,
        automatic_entropy_tuning: bool = True,
        device: str = 'cuda' if torch.cuda.is_available() else 'cpu'
    ):
        self.gamma = gamma
        self.tau = tau
        self.alpha = alpha
        self.automatic_entropy_tuning = automatic_entropy_tuning
        self.device = torch.device(device)

        # Initialize actor
        self.actor = SACGaussianActor(
            state_dim,
            action_dim,
            action_bound=action_bound
        ).to(self.device)

        # Initialize critics
        self.critic = SACCritic(
            state_dim,
            action_dim
        ).to(self.device)

        self.critic_target = SACCritic(
            state_dim,
            action_dim
        ).to(self.device)

        # Copy critic parameters to target
        self.critic_target.load_state_dict(self.critic.state_dict())

        # Initialize optimizers
        self.actor_optimizer = optim.Adam(
            self.actor.parameters(),
            lr=learning_rate
        )

        self.critic_optimizer = optim.Adam(
            self.critic.parameters(),
            lr=learning_rate
        )

        # Automatic entropy tuning
        if automatic_entropy_tuning:
            self.target_entropy = -action_dim
            self.log_alpha = torch.zeros(1, requires_grad=True, device=self.device)
            self.alpha_optimizer = optim.Adam([self.log_alpha], lr=learning_rate)

    def get_action(
        self,
        state: np.ndarray,
        deterministic: bool = False
    ) -> np.ndarray:
        """Get action from actor"""
        state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)

        with torch.no_grad():
            action, _ = self.actor.sample(state_tensor, deterministic)

        return action.cpu().numpy().squeeze()

    def update(
        self,
        replay_buffer,
        batch_size: int = 256
    ) -> Dict[str, float]:
        """Update SAC networks"""
        # Sample batch from replay buffer
        states, actions, rewards, next_states, dones = replay_buffer.sample(batch_size)

        states = torch.FloatTensor(states).to(self.device)
        actions = torch.FloatTensor(actions).to(self.device)
        rewards = torch.FloatTensor(rewards).unsqueeze(-1).to(self.device)
        next_states = torch.FloatTensor(next_states).to(self.device)
        dones = torch.FloatTensor(dones).unsqueeze(-1).to(self.device)

        # Update critics
        with torch.no_grad():
            next_actions, next_log_probs = self.actor.sample(next_states)
            next_q1, next_q2 = self.critic_target(next_states, next_actions)
            next_q = torch.min(next_q1, next_q2) - self.alpha * next_log_probs
            target_q = rewards + (1 - dones) * self.gamma * next_q

        q1, q2 = self.critic(states, actions)

        critic_loss = F.mse_loss(q1, target_q) + F.mse_loss(q2, target_q)

        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        self.critic_optimizer.step()

        # Update actor
        new_actions, log_probs = self.actor.sample(states)
        q1_new, q2_new = self.critic(states, new_actions)
        q_new = torch.min(q1_new, q2_new)

        actor_loss = (self.alpha * log_probs - q_new).mean()

        self.actor_optimizer.zero_grad()
        actor_loss.backward()
        self.actor_optimizer.step()

        # Update temperature
        if self.automatic_entropy_tuning:
            alpha_loss = -(
                self.log_alpha * (log_probs + self.target_entropy).detach()
            ).mean()

            self.alpha_optimizer.zero_grad()
            alpha_loss.backward()
            self.alpha_optimizer.step()

            self.alpha = self.log_alpha.exp()

        # Soft update target networks
        for param, target_param in zip(
            self.critic.parameters(),
            self.critic_target.parameters()
        ):
            target_param.data.copy_(
                self.tau * param.data + (1 - self.tau) * target_param.data
            )

        return {
            'critic_loss': critic_loss.item(),
            'actor_loss': actor_loss.item(),
            'alpha': self.alpha.item() if isinstance(self.alpha, torch.Tensor) else self.alpha
        }

## 7.3 Multi-Commodity Portfolio Management
def train_portfolio_manager(
    env,
    agent,
    n_episodes: int = 1000,
    replay_start: int = 1000
):
    """Train agent for multi-asset portfolio management"""

    replay_buffer = ReplayBuffer(capacity=100000)
    episode_rewards = []

    # Initial data collection
    print("Collecting initial experience...")
    state, _ = env.reset()

    for step in range(replay_start):
        action = env.action_space.sample()  # Random action
        next_state, reward, done, truncated, _ = env.step(action)
        replay_buffer.push(state, action, reward, next_state, done)
        state = next_state if not done else env.reset()[0]

    print("Starting training...")

    for episode in range(n_episodes):
        state, _ = env.reset()
        episode_reward = 0
        losses = []

        while True:
            # Get action from agent
            if isinstance(agent, SACAgent):
                action = agent.get_action(state, deterministic=False)
            elif isinstance(agent, PPOAgent):
                action, log_prob, value = agent.get_action(state)
                agent.memory.store(state, action, 0, log_prob, value, False)

            # Execute action
            next_state, reward, done, truncated, info = env.step(action)

            # Store transition
            if isinstance(agent, SACAgent):
                replay_buffer.push(state, action, reward, next_state, done)

                # Update SAC
                if len(replay_buffer) >= 256:
                    loss = agent.update(replay_buffer, batch_size=256)
                    losses.append(loss)
            elif isinstance(agent, PPOAgent):
                agent.memory.rewards[-1] = reward
                agent.memory.dones[-1] = done

            episode_reward += reward
            state = next_state

            if done or truncated:
                break

        # Update PPO at episode end
        if isinstance(agent, PPOAgent):
            loss = agent.update()
            if loss:
                losses.append(loss)

        episode_rewards.append(episode_reward)

        # Log progress
        if (episode + 1) % 10 == 0:
            avg_reward = np.mean(episode_rewards[-10:])
            print(f"Episode {episode + 1}/{n_episodes}, "
                  f"Avg Reward: {avg_reward:.3f}")

            if losses:
                avg_losses = {}
                for key in losses[0].keys():
                    avg_losses[key] = np.mean([l[key] for l in losses])
                print(f"Losses: {avg_losses}")

    return episode_rewards

## Practical Exercise
Implement and compare PPO and SAC on a multi-commodity portfolio:
- Crude oil, natural gas, gold
- Continuous position sizing
- Risk constraints
- Performance analysis
```

### Module 8: Handling Market Complexity
**Learning Objectives:**
- Address non-stationarity in markets
- Implement transfer learning across commodities
- Apply attention mechanisms to RL

**Content Requirements:**
```markdown
# Module 8: Handling Market Complexity

## 8.1 Non-Stationarity and Regime Detection
```python
import numpy as np
import pandas as pd
from sklearn.mixture import GaussianMixture
from typing import List, Dict, Optional
import torch
import torch.nn as nn

class MarketRegimeDetector:
    """Detect market regimes for adaptive RL"""

    def __init__(
        self,
        n_regimes: int = 3,
        features: List[str] = ['returns', 'volatility', 'volume']
    ):
        self.n_regimes = n_regimes
        self.features = features
        self.gmm = GaussianMixture(n_components=n_regimes, covariance_type='full')
        self.regime_stats = {}

    def fit(self, market_data: pd.DataFrame):
        """Fit regime model to historical data"""
        # Extract features
        feature_data = []

        if 'returns' in self.features:
            returns = market_data['close'].pct_change()
            feature_data.append(returns)

        if 'volatility' in self.features:
            vol = returns.rolling(20).std() * np.sqrt(252)
            feature_data.append(vol)

        if 'volume' in self.features:
            volume_ma = market_data['volume'].rolling(20).mean()
            feature_data.append(volume_ma)

        # Combine features
        X = pd.concat(feature_data, axis=1).dropna()

        # Fit GMM
        self.gmm.fit(X)

        # Calculate regime statistics
        regimes = self.gmm.predict(X)

        for i in range(self.n_regimes):
            regime_mask = regimes == i
            self.regime_stats[i] = {
                'mean_return': returns[regime_mask].mean(),
                'volatility': returns[regime_mask].std(),
                'frequency': regime_mask.sum() / len(regimes)
            }

    def predict_regime(self, current_features: np.ndarray) -> int:
        """Predict current market regime"""
        return self.gmm.predict(current_features.reshape(1, -1))[0]

    def get_regime_probabilities(self, current_features: np.ndarray) -> np.ndarray:
        """Get probability distribution over regimes"""
        return self.gmm.predict_proba(current_features.reshape(1, -1))[0]

class AdaptiveRLAgent:
    """RL agent that adapts to market regimes"""

    def __init__(
        self,
        base_agent,
        regime_detector: MarketRegimeDetector,
        n_regimes: int = 3
    ):
        self.regime_detector = regime_detector
        self.n_regimes = n_regimes

        # Create separate agents for each regime
        self.agents = {
            i: base_agent.__class__(**base_agent.__dict__)
            for i in range(n_regimes)
        }

        self.current_regime = 0
        self.regime_history = []

    def get_action(
        self,
        state: np.ndarray,
        market_features: np.ndarray
    ) -> int:
        """Get action based on current regime"""
        # Detect regime
        regime = self.regime_detector.predict_regime(market_features)

        if regime != self.current_regime:
            print(f"Regime switch: {self.current_regime} -> {regime}")
            self.current_regime = regime

        self.regime_history.append(regime)

        # Get action from regime-specific agent
        return self.agents[regime].get_action(state)

    def update(self, *args, **kwargs):
        """Update current regime's agent"""
        return self.agents[self.current_regime].update(*args, **kwargs)

## 8.2 Transfer Learning Across Commodities
class TransferLearningAgent:
    """Transfer knowledge across different commodities"""

    def __init__(
        self,
        source_model_path: str,
        target_state_dim: int,
        target_action_dim: int,
        freeze_layers: int = 2
    ):
        # Load pre-trained model
        self.base_model = torch.load(source_model_path)

        # Freeze early layers
        for i, (name, param) in enumerate(self.base_model.named_parameters()):
            if i < freeze_layers:
                param.requires_grad = False

        # Add commodity-specific heads
        self.commodity_heads = nn.ModuleDict()

    def add_commodity_head(self, commodity: str, output_dim: int):
        """Add new head for specific commodity"""
        # Get feature dimension from base model
        feature_dim = self.base_model.shared[-2].out_features

        # Create commodity-specific head
        head = nn.Sequential(
            nn.Linear(feature_dim, 128),
            nn.ReLU(),
            nn.Linear(128, output_dim)
        )

        self.commodity_heads[commodity] = head

    def forward(self, state: torch.Tensor, commodity: str):
        """Forward pass with commodity-specific head"""
        # Get shared features
        features = self.base_model.shared(state)

        # Use commodity-specific head
        if commodity in self.commodity_heads:
            output = self.commodity_heads[commodity](features)
        else:
            raise ValueError(f"No head for commodity: {commodity}")

        return output

def meta_learning_update(
    agent,
    tasks: List[Dict],
    inner_lr: float = 0.01,
    outer_lr: float = 0.001,
    inner_steps: int = 5
):
    """MAML-style meta-learning for commodity trading"""

    meta_optimizer = torch.optim.Adam(agent.parameters(), lr=outer_lr)

    for epoch in range(100):
        meta_loss = 0

        for task in tasks:
            # Clone agent for inner loop
            task_agent = copy.deepcopy(agent)
            task_optimizer = torch.optim.SGD(
                task_agent.parameters(),
                lr=inner_lr
            )

            # Inner loop: adapt to specific commodity
            for _ in range(inner_steps):
                states, actions, rewards = task['data']

                # Calculate task-specific loss
                predictions = task_agent(states)
                loss = compute_loss(predictions, actions, rewards)

                # Inner update
                task_optimizer.zero_grad()
                loss.backward()
                task_optimizer.step()

            # Evaluate on test data
            test_states, test_actions, test_rewards = task['test_data']
            test_predictions = task_agent(test_states)
            test_loss = compute_loss(test_predictions, test_actions, test_rewards)

            meta_loss += test_loss

        # Outer update
        meta_optimizer.zero_grad()
        meta_loss.backward()
        meta_optimizer.step()

        print(f"Meta-learning epoch {epoch}: Loss = {meta_loss.item()}")

## 8.3 Hierarchical RL for Multi-Timeframe Trading
class HierarchicalTradingAgent:
    """Hierarchical RL for strategic and tactical decisions"""

    def __init__(
        self,
        state_dim: int,
        strategic_action_dim: int,
        tactical_action_dim: int
    ):
        # High-level controller (strategic)
        self.high_level = PPOAgent(
            state_dim,
            strategic_action_dim,
            learning_rate=1e-4
        )

        # Low-level controllers (tactical)
        self.low_level_agents = {}
        for i in range(strategic_action_dim):
            self.low_level_agents[i] = PPOAgent(
                state_dim,
                tactical_action_dim,
                learning_rate=3e-4
            )

        self.current_strategy = None
        self.strategy_steps = 0
        self.max_strategy_steps = 20

    def get_action(self, state: np.ndarray) -> int:
        """Get hierarchical action"""
        # Check if need new strategy
        if self.strategy_steps >= self.max_strategy_steps or \
           self.current_strategy is None:

            # Get new strategy from high-level controller
            self.current_strategy = self.high_level.get_action(state)[0]
            self.strategy_steps = 0
            print(f"New strategy selected: {self.current_strategy}")

        # Get tactical action from low-level controller
        tactical_action = self.low_level_agents[
            self.current_strategy
        ].get_action(state)[0]

        self.strategy_steps += 1

        return tactical_action

## 8.4 Attention Mechanisms in RL
class AttentionRLNetwork(nn.Module):
    """RL network with attention mechanism"""

    def __init__(
        self,
        state_dim: int,
        action_dim: int,
        n_heads: int = 4,
        embed_dim: int = 128
    ):
        super(AttentionRLNetwork, self).__init__()

        # Embedding layer
        self.embedding = nn.Linear(state_dim, embed_dim)

        # Multi-head attention
        self.attention = nn.MultiheadAttention(
            embed_dim,
            n_heads,
            batch_first=True
        )

        # Feed-forward network
        self.ffn = nn.Sequential(
            nn.Linear(embed_dim, 256),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(256, 128),
            nn.ReLU()
        )

        # Output heads
        self.actor = nn.Linear(128, action_dim)
        self.critic = nn.Linear(128, 1)

    def forward(
        self,
        state: torch.Tensor,
        return_attention: bool = False
    ):
        # Embed state
        x = self.embedding(state)

        # Reshape for attention (batch, seq_len, embed_dim)
        if len(x.shape) == 2:
            x = x.unsqueeze(1)

        # Apply attention
        attn_out, attn_weights = self.attention(x, x, x)

        # Feed-forward
        features = self.ffn(attn_out.squeeze(1))

        # Get outputs
        action_logits = self.actor(features)
        value = self.critic(features)

        if return_attention:
            return action_logits, value, attn_weights

        return action_logits, value

## Practical Exercise
Build an adaptive RL system that:
1. Detects market regimes
2. Switches between regime-specific agents
3. Uses attention to focus on relevant features
4. Transfers knowledge between similar commodities
```

### Module 9: Training Best Practices
### Module 10: Evaluation and Backtesting
### Module 11: Risk Management Integration
### Module 12: Production Deployment

**Note:** Due to space constraints, I'm providing the complete structure for Modules 1-8. The remaining modules (9-12) would follow the same detailed pattern with full code implementations and practical exercises.

## ADDITIONAL SPECIFICATIONS

### Repository Structure
```
rl-commodities-course/
├── modules/
│   ├── 01_foundations/
│   │   ├── README.md
│   │   ├── notebooks/
│   │   │   ├── 01_intro_to_rl.ipynb
│   │   │   ├── 02_mdp_basics.ipynb
│   │   │   └── 03_commodities_mdp.ipynb
│   │   ├── exercises/
│   │   └── solutions/
│   ├── 02_environment_design/
│   │   ├── README.md
│   │   ├── notebooks/
│   │   ├── exercises/
│   │   └── solutions/
│   └── ... (all 12 modules)
├── rl_trading_toolkit/
│   ├── __init__.py
│   ├── environments/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── single_asset.py
│   │   ├── multi_asset.py
│   │   └── spread_trading.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── dqn.py
│   │   ├── ppo.py
│   │   ├── sac.py
│   │   └── hierarchical.py
│   ├── rewards/
│   │   ├── __init__.py
│   │   ├── basic.py
│   │   ├── risk_adjusted.py
│   │   └── multi_objective.py
│   ├── features/
│   │   ├── __init__.py
│   │   ├── technical.py
│   │   ├── fundamental.py
│   │   └── normalization.py
│   ├── evaluation/
│   │   ├── __init__.py
│   │   ├── backtest.py
│   │   ├── metrics.py
│   │   └── visualization.py
│   └── utils/
│       ├── __init__.py
│       ├── data.py
│       ├── config.py
│       └── logging.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── README.md
├── configs/
│   ├── dqn_config.yaml
│   ├── ppo_config.yaml
│   └── sac_config.yaml
├── tests/
│   ├── test_environments.py
│   ├── test_agents.py
│   └── test_rewards.py
├── requirements.txt
├── setup.py
└── README.md
```

### Data Requirements
Each module should use real commodity data:
- **Crude Oil**: WTI and Brent futures
- **Natural Gas**: Henry Hub futures
- **Precious Metals**: Gold, Silver futures
- **Agriculture**: Corn, Wheat, Soybeans futures

Data sources:
- yfinance for daily data
- Interactive Brokers API for intraday
- Quandl for fundamental data

### Assessment Components
Each module includes:
1. **Pre-assessment**: Test existing knowledge
2. **Hands-on Labs**: Guided implementation exercises
3. **Challenges**: Open-ended problems
4. **Quizzes**: Multiple choice conceptual questions
5. **Projects**: Module-specific mini-projects

### Interactive Elements
1. **Visualizations**:
   - Agent behavior animations
   - Performance dashboards
   - Market regime visualizations
   - Attention heatmaps

2. **Experiments**:
   - Hyperparameter tuning interfaces
   - A/B testing frameworks
   - Ablation study tools

3. **Debugging Tools**:
   - Step-through environment execution
   - Policy visualization
   - Reward decomposition

### Production Considerations
1. **Scalability**: Multi-processing for parallel training
2. **Monitoring**: MLflow integration for experiment tracking
3. **Deployment**: Docker containers for model serving
4. **Testing**: Comprehensive unit and integration tests
5. **Documentation**: API documentation with Sphinx

### Common Pitfalls to Address
1. **Lookahead Bias**: Strict temporal data handling
2. **Overfitting**: Proper validation procedures
3. **Non-stationarity**: Adaptive learning rates
4. **Transaction Costs**: Realistic cost models
5. **Risk Management**: Position limits and stops

### Advanced Topics for Bonus Content
1. **Inverse RL**: Learning reward functions from expert traders
2. **Multi-Agent RL**: Modeling market interactions
3. **Options Trading**: Extending to derivatives
4. **Explainable RL**: Interpreting agent decisions
5. **Federated Learning**: Privacy-preserving collaborative training

### Course Delivery Format
1. **Self-paced online**: Jupyter notebooks with embedded explanations
2. **Video tutorials**: Screen recordings of implementations
3. **Live coding sessions**: Instructor-led development
4. **Office hours**: Q&A sessions for difficult concepts
5. **Peer review**: Students review each other's implementations

### Grading Rubric
- **Coding Exercises**: 40%
  - Correctness: 20%
  - Code quality: 10%
  - Documentation: 10%
- **Projects**: 30%
  - Innovation: 10%
  - Performance: 10%
  - Presentation: 10%
- **Quizzes**: 20%
- **Participation**: 10%

### Prerequisites Check
Students should complete a prerequisites notebook that tests:
1. Python proficiency (classes, decorators, async)
2. NumPy/Pandas operations
3. Basic ML concepts (overfitting, cross-validation)
4. Financial markets knowledge (futures, spreads)
5. Probability and statistics

### Certification Criteria
To receive certification, students must:
1. Complete all 12 modules
2. Score ≥80% on assessments
3. Successfully deploy a trading agent
4. Pass final capstone project review
5. Demonstrate risk management understanding

## IMPLEMENTATION NOTES

### Performance Benchmarks
All implementations should achieve:
- DQN convergence within 500 episodes
- PPO stable training with monotonic improvement
- SAC sample efficiency ≥ 100 reward/episode within 1000 episodes
- Backtesting speed ≥ 10,000 steps/second
- Memory usage ≤ 4GB for standard training

### Code Quality Standards
- Type hints for all functions
- Docstrings with examples
- Unit test coverage ≥ 80%
- Pylint score ≥ 8.0
- Black formatting
- Maximum cyclomatic complexity: 10

### Version Requirements
```
python>=3.8
gymnasium>=0.29.0
stable-baselines3>=2.0.0
torch>=2.0.0
pandas>=1.5.0
numpy>=1.23.0
scipy>=1.9.0
matplotlib>=3.6.0
plotly>=5.0.0
yfinance>=0.2.0
ta-lib>=0.4.0
scikit-learn>=1.2.0
tqdm>=4.65.0
pyyaml>=6.0
tensorboard>=2.10.0
mlflow>=2.0.0
pytest>=7.0.0
black>=22.0.0
pylint>=2.15.0
```

This comprehensive prompt provides detailed specifications for generating a complete, production-ready Reinforcement Learning course for commodities trading, with extensive code examples, practical exercises, and professional development practices.