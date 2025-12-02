# Prompt: Generate Complete Course on Fair Value Modelling in Commodities Trading

## COURSE GENERATION DIRECTIVE

You are tasked with creating a comprehensive, production-ready course titled **"Fair Value Modelling in Commodities Trading: From Point-in-Time Data to Signal Discovery"**. This is NOT a generic commodities course. It specifically focuses on the intersection of temporal data management, fundamental fair value modeling, and actionable signal generation when model predictions diverge from market prices.

Generate a complete 40-hour course (10 modules, 4 hours each) that teaches practitioners how to build, validate, and trade fair value models while maintaining strict temporal discipline to avoid look-ahead bias and data leakage.

## CORE PRINCIPLES TO EMBED THROUGHOUT

### Principle 1: Temporal Integrity
Every data point, calculation, and model prediction must respect what was actually knowable at that point in time. This means:
- Data has observation dates (when event occurred) AND publication dates (when data became available)
- Features must account for reporting lags (EIA reports Wednesday data on Thursday)
- Backtests must simulate real-time trading constraints
- Model training must never use future information

### Principle 2: Fair Value as Fundamental Equilibrium
Fair value represents where commodity prices "should" trade based on fundamental supply-demand dynamics, NOT technical analysis or momentum. Define fair value through:
- Physical market balance (supply, demand, inventories)
- Cost structures (production costs, storage, transportation)
- Seasonal patterns (harvest cycles, heating/cooling demand)
- Structural relationships (crack spreads, crush margins)

### Principle 3: Signal Discovery Through Divergence
The course focuses on identifying when market prices diverge from fair value, creating trading opportunities:
- Markets can remain irrational longer than models predict
- Divergence magnitude matters less than convergence probability
- Regime changes affect signal reliability
- Position sizing reflects conviction in convergence

### Principle 4: Validation Without Deception
Many backtests show false profits due to data leakage. This course emphasizes:
- Walk-forward validation with proper data vintages
- Out-of-sample testing that simulates real trading
- Attribution of returns to model skill vs. luck
- Detection and elimination of look-ahead bias

## DETAILED MODULE SPECIFICATIONS

### Module 1: Foundations of Commodities Fair Value (4 hours)

**Learning Objectives:**
- Define fair value in physical commodity markets vs. financial assets
- Understand spot-forward relationships and term structure
- Identify when fair value models add value vs. market efficiency

**Content Requirements:**

**1.1 What Makes Commodities Different (45 min)**
- Physical delivery and storage constraints
- Quality specifications and location basis
- Seasonal production/consumption patterns
- Why equities valuation models don't apply
- Case study: Nickel squeeze of 2022 - when physical matters

**1.2 The Cost-of-Carry Framework (60 min)**
```python
# Include working code example:
def cost_of_carry_fair_value(
    spot_price: float,
    storage_cost_per_month: float,
    interest_rate: float,
    months_to_delivery: int,
    convenience_yield: float = 0
) -> float:
    """
    Calculate theoretical forward price using cost-of-carry.

    Fair Value = Spot * exp((r + s - y) * t)
    where:
        r = risk-free rate
        s = storage cost rate
        y = convenience yield
        t = time to maturity
    """
    # Implementation with numerical example using crude oil
```
- Full vs. financing cost of carry
- Convenience yield and its estimation
- When cost-of-carry breaks down

**1.3 Supply-Demand Fundamentals (75 min)**
- Balance sheet construction (production + imports = consumption + exports + Δstocks)
- Elasticity concepts in commodities
- Threshold effects (tank tops, pipeline constraints)
- Data sources: EIA, USDA, IEA, JODI
- Exercise: Build corn balance sheet from WASDE data

**1.4 Market Structure and Fair Value Implications (60 min)**
- Contango vs. backwardation equilibrium
- Term structure as information
- Futures convergence to spot
- Roll yield and its fair value interpretation
- Practical: Calculate implied storage costs from futures curves

**Module Assessment:**
- Quiz: 15 questions on fundamental concepts
- Project: Calculate cost-of-carry fair value for WTI crude given current data

### Module 2: Point-in-Time Data Architecture (4 hours)

**Learning Objectives:**
- Design databases that preserve temporal integrity
- Implement as-of-date queries
- Handle data revisions systematically
- Simulate historical data availability

**Content Requirements:**

**2.1 The Look-Ahead Bias Problem (45 min)**
- Common ways models accidentally cheat
- GDP revisions example - preliminary vs. final
- Agricultural data: planting intentions vs. actual
- Case study: Fund that failed due to look-ahead bias

**2.2 Data Vintage Concepts (60 min)**
```python
# Core data structure for point-in-time data
@dataclass
class PointInTimeRecord:
    """
    Fundamental unit of temporal data storage.
    """
    series_id: str              # e.g., "EIA.CRUDE.STOCKS"
    observation_date: datetime  # Date data refers to
    publication_date: datetime  # When data was released
    as_of_date: datetime       # When we knew this value
    value: float               # The actual data point
    revision: int              # 0=first release, 1=first revision
    is_final: bool            # Is this the final value?

    def was_known_on(self, query_date: datetime) -> bool:
        """Check if this data was available on query_date."""
        return self.publication_date <= query_date
```

**2.3 Building Point-in-Time Database (75 min)**
- Schema design for temporal data
- Efficient storage strategies (bitemporal tables)
- Query patterns for as-of-date retrieval
- Hands-on: Implement SQLite point-in-time database
```sql
-- Example schema
CREATE TABLE commodity_data (
    series_id TEXT,
    observation_date DATE,
    publication_date DATE,
    value REAL,
    revision INTEGER,
    PRIMARY KEY (series_id, observation_date, publication_date)
);

-- As-of query pattern
SELECT * FROM commodity_data
WHERE series_id = 'EIA_CRUDE_STOCKS'
  AND observation_date <= '2024-01-15'
  AND publication_date <= '2024-01-16'  -- as-of date
  AND (series_id, observation_date, publication_date) IN (
    SELECT series_id, observation_date, MAX(publication_date)
    FROM commodity_data
    WHERE publication_date <= '2024-01-16'
    GROUP BY series_id, observation_date
  );
```

**2.4 Data Collection with Temporal Awareness (60 min)**
- API patterns that preserve publication dates
- Web scraping with timestamp capture
- Handling embargo periods
- Building data pipelines that maintain vintage
- Exercise: Scrape EIA weekly petroleum report with proper timestamps

**Module Assessment:**
- Lab: Build point-in-time database for natural gas storage
- Quiz: Identify look-ahead bias in provided code samples

### Module 3: Exploratory Data Analysis with Temporal Discipline (4 hours)

**Learning Objectives:**
- Perform EDA that respects data availability
- Visualize revision patterns and their impact
- Identify stable vs. unstable relationships over time

**Content Requirements:**

**3.1 Vintage-Aware Summary Statistics (60 min)**
```python
def temporal_eda(data: PointInTimeDataFrame, as_of_date: datetime):
    """
    Generate summary statistics as they would have appeared
    on a specific date in history.
    """
    # Filter to data known on as_of_date
    known_data = data.as_of(as_of_date)

    # Calculate statistics
    stats = {
        'mean': known_data.mean(),
        'std': known_data.std(),
        'skew': known_data.skew(),
        # Include revision statistics
        'mean_revision': data.revision_magnitude().mean(),
        'revision_bias': data.revision_direction().mean()
    }
    return stats
```
- Rolling statistics with proper alignment
- Detecting structural breaks in real-time
- Correlation evolution over data vintages

**3.2 Visualizing Data Revisions (75 min)**
- Revision waterfall charts
- Vintage spider plots
- Real-time vs. final data comparison
- Case study: USDA crop estimate revisions impact on trading
- Practical: Build revision analysis dashboard

**3.3 Feature Stability Analysis (60 min)**
- Testing if relationships hold across vintages
- Correlation decay with data age
- Which features survive revision cycles?
- Implementation: Feature importance stability metrics

**3.4 Seasonality Detection with Point-in-Time Data (45 min)**
- X-13ARIMA-SEATS with vintage data
- Rolling seasonal patterns
- Distinguishing true seasonality from data artifacts
- Exercise: Detect natural gas seasonality using only historical data

**Module Assessment:**
- Project: Complete EDA report on crude oil data with vintage analysis
- Identify three revision patterns that could affect trading

### Module 4: Fundamental Data Sources and Processing (4 hours)

**Learning Objectives:**
- Master key commodity data sources and their quirks
- Implement proper timestamp tracking
- Handle missing data and outliers temporally
- Build reliable data pipelines

**Content Requirements:**

**4.1 Energy Data Sources (60 min)**
- EIA weekly petroleum status report
  - Release schedule: Wed 10:30am ET for week ending Friday
  - Key series: crude stocks, refinery runs, product supplied
  - Revision patterns and adjustments
- Natural gas storage report
  - Thursday 10:30am ET release
  - Regional breakdown importance
- IEA Oil Market Report timing
```python
class EIADataCollector:
    """
    Collect EIA data with proper publication timestamps.
    """
    def fetch_weekly_petroleum(self, as_of_date: datetime):
        # API call with proper date handling
        # Map report date to observation period
        # Store with publication timestamp
        pass
```

**4.2 Agricultural Data Sources (75 min)**
- USDA WASDE report
  - Monthly release around 10th at noon ET
  - Lock-up procedures and embargo
  - Preliminary vs. final estimates
- Crop Progress and Condition
  - Weekly during growing season
  - State-level data aggregation
- CFTC Commitments of Traders
  - Friday 3:30pm ET for Tuesday positions
  - Managed money positioning as sentiment
- Implementation: WASDE data parser with revision tracking

**4.3 Metals and Industrial Data (60 min)**
- LME warehouse stocks (daily 9am London)
- Chinese industrial data (NBS release calendar)
- Ship tracking and trade flows (real-time with lag)
- Mining company production reports
- Exercise: Build copper supply tracker with proper timestamps

**4.4 Alternative Data Integration (45 min)**
- Satellite data for crop monitoring (2-week processing lag)
- Weather data and forecasts (continuous updates)
- Vessel tracking for oil flows
- Google trends as demand proxy
- Key principle: Alternative data also has observation vs. availability lag

**Module Assessment:**
- Build unified data collector for one commodity
- Document all temporal lags and revision patterns

### Module 5: Fair Value Model Construction (4 hours)

**Learning Objectives:**
- Build multiple types of fair value models
- Understand strengths/weaknesses of each approach
- Implement models with point-in-time discipline
- Calibrate models for different time horizons

**Content Requirements:**

**5.1 Inventory-Based Models (75 min)**
```python
class InventoryFairValueModel:
    """
    Fair value based on stocks-to-use ratio or days of supply.
    """
    def __init__(self, commodity: str, model_type: str = 'power_law'):
        self.commodity = commodity
        self.model_type = model_type

    def fit(self, data: PointInTimeDataFrame, as_of_date: datetime):
        """
        Calibrate model using only data known on as_of_date.

        Power law form: Price = a * (Stocks/Use)^b
        Logistic form: Price = L / (1 + exp(-k*(x-x0)))
        """
        historical = data.as_of(as_of_date)

        if self.model_type == 'power_law':
            # Fit: log(price) = log(a) + b*log(stocks_to_use)
            pass
        elif self.model_type == 'logistic':
            # Fit S-curve for extreme inventory scenarios
            pass

    def predict_fair_value(self, current_stocks: float,
                          current_use_rate: float) -> float:
        """Generate fair value estimate."""
        pass
```
- Case study: Crude oil stocks vs. WTI price
- Handling tank tops and operational minimums
- Regional vs. global inventory models

**5.2 Supply-Demand Balance Models (60 min)**
- Balance sheet projection
- Price elasticity estimation
- Shock scenario modeling
- Example: Global wheat balance and price discovery
- Implementation: Multi-region S&D optimizer

**5.3 Cost Curve Models (75 min)**
- Marginal cost of production
- Breakeven analysis by producer
- Mine/field production economics
- Transport and logistics costs
- Practical: Build aluminum cost curve from smelter data
```python
def marginal_cost_fair_value(
    cost_curve: pd.DataFrame,  # Producer costs sorted ascending
    total_demand: float
) -> float:
    """
    Find marginal producer that sets price.
    """
    cumulative_supply = cost_curve['capacity'].cumsum()
    marginal_producer_idx = (cumulative_supply >= total_demand).idxmax()
    marginal_cost = cost_curve.loc[marginal_producer_idx, 'total_cost']

    # Add normal profit margin
    fair_value = marginal_cost * (1 + NORMAL_PROFIT_MARGIN)
    return fair_value
```

**5.4 Machine Learning Fair Value Models (60 min)**
- Feature engineering for ML models
- Random forests with temporal cross-validation
- Neural networks for non-linear relationships
- Ensemble methods combining multiple approaches
- Critical: Avoiding data leakage in ML pipelines
```python
class TemporalMLPipeline(sklearn.pipeline.Pipeline):
    """
    Scikit-learn pipeline that respects temporal constraints.
    """
    def fit(self, X, y, as_of_dates):
        # Custom fit that ensures point-in-time discipline
        pass
```

**Module Assessment:**
- Build complete fair value model for natural gas
- Compare three different modeling approaches
- Backtest with proper temporal validation

### Module 6: Feature Engineering with Temporal Constraints (4 hours)

**Learning Objectives:**
- Create features that could actually be calculated in real-time
- Handle publication lags in feature construction
- Build cross-sectional features properly
- Maintain feature stability over time

**Content Requirements:**

**6.1 Temporal Feature Engineering Patterns (60 min)**
```python
class TemporalFeatureEngineer:
    """
    Feature engineering that respects data availability.
    """
    def create_lagged_features(self,
                              data: PointInTimeDataFrame,
                              feature_col: str,
                              lags: List[int],
                              as_of_date: datetime):
        """
        Create lagged features using only past data.
        Account for publication delay.
        """
        features = {}
        for lag in lags:
            # Get value from lag periods ago
            # BUT ensure it was published by as_of_date
            observation_date = as_of_date - timedelta(days=lag)
            value = data.get_value_as_of(
                observation_date=observation_date,
                as_of_date=as_of_date,
                column=feature_col
            )
            features[f'{feature_col}_lag_{lag}'] = value
        return features

    def create_rolling_features(self, window: int, min_periods: int):
        """Rolling statistics with proper data alignment."""
        pass

    def create_seasonal_features(self, method: str = 'x13'):
        """Seasonal adjustment using only historical data."""
        pass
```

**6.2 Cross-Sectional Features (75 min)**
- Spread features (calendar, quality, location)
- Relative value across commodity complex
- Cross-commodity ratios (gold/silver, corn/wheat)
- Term structure features
- Implementation: Build corn-soy spread features with proper timing

**6.3 Regime and Structural Features (60 min)**
- Detecting regime changes in real-time
- Markov regime switching features
- Structural break indicators
- Volatility regime features
- Case study: Identifying energy crisis regimes

**6.4 Feature Selection with Temporal Stability (45 min)**
- Feature importance over time
- Stability metrics for feature selection
- Handling feature drift
- Recursive feature elimination with time series
- Exercise: Select stable features for copper model

**Module Assessment:**
- Engineer 20+ features for crude oil with proper timestamps
- Test feature stability across different time periods
- Document data requirements and lags

### Module 7: Model Validation and Backtesting (4 hours)

**Learning Objectives:**
- Implement walk-forward validation correctly
- Detect and eliminate data leakage
- Measure model decay and retraining needs
- Build confidence intervals for predictions

**Content Requirements:**

**7.1 Walk-Forward Validation Framework (75 min)**
```python
class WalkForwardValidator:
    """
    Time series validation with point-in-time data.
    """
    def __init__(self,
                 train_window: int = 252,  # days
                 test_window: int = 21,
                 retrain_frequency: int = 21,
                 gap: int = 1):  # gap between train and test
        self.train_window = train_window
        self.test_window = test_window
        self.retrain_frequency = retrain_frequency
        self.gap = gap

    def generate_splits(self, data: PointInTimeDataFrame):
        """
        Generate train/test splits respecting time.
        """
        splits = []
        for test_start in self.test_dates:
            train_end = test_start - timedelta(days=self.gap)
            train_start = train_end - timedelta(days=self.train_window)
            test_end = test_start + timedelta(days=self.test_window)

            # Get data AS IT WAS KNOWN at train_end
            train_data = data.as_of(train_end).loc[train_start:train_end]

            # Test data uses real-time updates
            test_data = data.loc[test_start:test_end]

            splits.append((train_data, test_data))
        return splits

    def backtest(self, model, data):
        """Run complete walk-forward backtest."""
        results = []
        for train, test in self.generate_splits(data):
            model.fit(train)
            predictions = model.predict(test)
            metrics = self.calculate_metrics(test['y'], predictions)
            results.append(metrics)
        return pd.DataFrame(results)
```

**7.2 Data Leakage Detection (60 min)**
- Common leakage patterns in commodities
- Statistical tests for leakage
- Information coefficient analysis
- Permutation importance for leakage detection
- Case study: Fund that discovered leakage after going live

**7.3 Model Stability and Decay Analysis (75 min)**
- Measuring prediction accuracy over time
- Model half-life estimation
- When to retrain vs. recalibrate
- Parameter stability tracking
- Implementation: Model monitoring dashboard

**7.4 Confidence Intervals and Uncertainty (60 min)**
- Bootstrapping prediction intervals
- Conformal prediction for time series
- Uncertainty from data revisions
- Ensemble-based uncertainty estimates
- Exercise: Build prediction intervals for nat gas model

**Module Assessment:**
- Implement complete backtesting harness
- Run backtest on your fair value model
- Identify any data leakage issues
- Calculate model decay metrics

### Module 8: Signal Discovery and Trading Logic (4 hours)

**Learning Objectives:**
- Convert fair value estimates to trading signals
- Size positions based on conviction
- Implement entry/exit logic
- Handle transaction costs and market impact

**Content Requirements:**

**8.1 From Fair Value to Trading Signal (75 min)**
```python
class FairValueSignalGenerator:
    """
    Convert fair value model to actionable signals.
    """
    def __init__(self,
                 z_score_entry: float = 2.0,
                 z_score_exit: float = 0.5,
                 lookback_window: int = 60,
                 min_holding_period: int = 5):
        self.z_score_entry = z_score_entry
        self.z_score_exit = z_score_exit
        self.lookback_window = lookback_window
        self.min_holding_period = min_holding_period

    def calculate_signal(self,
                        market_price: float,
                        fair_value: float,
                        historical_divergence: pd.Series) -> dict:
        """
        Generate trading signal from price-value divergence.
        """
        # Calculate current divergence
        divergence = (market_price - fair_value) / fair_value

        # Normalize using historical distribution
        mean_div = historical_divergence.rolling(self.lookback_window).mean()
        std_div = historical_divergence.rolling(self.lookback_window).std()
        z_score = (divergence - mean_div.iloc[-1]) / std_div.iloc[-1]

        # Generate signal
        signal = {
            'divergence': divergence,
            'z_score': z_score,
            'signal': self._determine_position(z_score),
            'confidence': self._calculate_confidence(z_score),
            'expected_convergence_days': self._estimate_convergence_time()
        }
        return signal
```

**8.2 Position Sizing and Risk Management (60 min)**
- Kelly criterion for commodities
- Volatility-based position sizing
- Correlation-adjusted portfolio weights
- Stop-loss vs. time-based exits
- Implementation: Multi-commodity portfolio optimizer

**8.3 Market Regime Considerations (75 min)**
- When fundamentals don't matter (crisis periods)
- Momentum vs. mean reversion regimes
- Volatility regime adjustments
- Liquidity-aware position sizing
- Case study: 2008 commodity super-cycle signal failure

**8.4 Transaction Costs and Implementation (60 min)**
- Futures roll costs
- Bid-ask spreads by commodity
- Market impact modeling
- Optimal execution strategies
- Exercise: Calculate net returns after costs

**Module Assessment:**
- Build complete signal generation system
- Backtest with realistic transaction costs
- Compare multiple position sizing methods
- Document risk management rules

### Module 9: Production Systems and Real-Time Trading (4 hours)

**Learning Objectives:**
- Design production-ready fair value systems
- Handle real-time data feeds
- Implement model monitoring and alerting
- Build execution infrastructure

**Content Requirements:**

**9.1 System Architecture for Fair Value Trading (60 min)**
```python
class ProductionFairValueSystem:
    """
    Production architecture for fair value trading.
    """
    def __init__(self):
        self.data_collector = RealTimeDataCollector()
        self.point_in_time_db = PointInTimeDatabase()
        self.model_registry = ModelRegistry()
        self.signal_generator = SignalGenerator()
        self.risk_manager = RiskManager()
        self.executor = OrderExecutor()

    def run_trading_loop(self):
        """Main trading loop."""
        while market_is_open():
            # Collect latest data
            new_data = self.data_collector.fetch_latest()

            # Store with proper timestamps
            self.point_in_time_db.insert(new_data)

            # Update models if needed
            if self.should_update_models():
                self.retrain_models()

            # Generate signals
            signals = self.generate_all_signals()

            # Risk checks
            approved_signals = self.risk_manager.approve(signals)

            # Execute trades
            self.executor.execute(approved_signals)

            # Log and monitor
            self.log_activity()

            time.sleep(self.loop_interval)
```

**9.2 Real-Time Data Management (75 min)**
- WebSocket feeds for futures prices
- API polling for fundamental data
- Data quality checks and validation
- Handling missing or delayed data
- Implementation: Build real-time EIA data monitor

**9.3 Model Monitoring and Drift Detection (60 min)**
- Real-time performance tracking
- Prediction error monitoring
- Feature drift detection
- A/B testing framework for models
- Alert system for anomalies
- Dashboard implementation with Grafana

**9.4 Execution and Order Management (45 min)**
- FIX protocol basics
- Order types for commodities
- Smart order routing
- Position reconciliation
- Exercise: Build paper trading system

**Module Assessment:**
- Design complete system architecture
- Implement monitoring dashboard
- Build alert system for model issues
- Create execution simulator

### Module 10: Advanced Topics and Case Studies (4 hours)

**Learning Objectives:**
- Apply course concepts to complex scenarios
- Understand frontier techniques
- Learn from historical successes and failures
- Build complete trading strategies

**Content Requirements:**

**10.1 Ensemble Methods for Fair Value (60 min)**
```python
class FairValueEnsemble:
    """
    Combine multiple fair value models.
    """
    def __init__(self, models: List[FairValueModel]):
        self.models = models
        self.weights = None

    def fit_weights(self, data: PointInTimeDataFrame, method: str = 'inverse_variance'):
        """
        Learn optimal model weights.
        """
        if method == 'inverse_variance':
            # Weight by inverse of prediction variance
            variances = [model.prediction_variance(data) for model in self.models]
            self.weights = 1 / np.array(variances)
            self.weights /= self.weights.sum()
        elif method == 'stacking':
            # Use meta-learner to combine
            pass

    def predict(self, data):
        """Weighted ensemble prediction."""
        predictions = [m.predict(data) for m in self.models]
        return np.average(predictions, weights=self.weights)
```

**10.2 Multi-Commodity Portfolio Construction (75 min)**
- Correlation-aware portfolio optimization
- Cross-commodity hedging
- Sector rotation strategies
- Dynamic commodity allocation
- Case study: Building diversified commodity portfolio

**10.3 Alternative Data Integration (60 min)**
- Satellite imagery for crop yields
- Ship tracking for oil flows
- Weather derivatives and trading
- Social media sentiment
- Implementation: Integrate satellite data for corn model

**10.4 Historical Case Studies (45 min)**
- Amaranth Advisors: Natural gas calendar spread disaster
- 2014 oil crash: When fair value models failed
- Cocoa squeeze 2010: Physical vs. financial
- Lessons learned and risk management implications

**Final Capstone Project:**
Build complete fair value trading system for one commodity including:
- Point-in-time data infrastructure
- Fair value model with proper validation
- Signal generation and backtesting
- Risk management framework
- Production system design

## PEDAGOGICAL SPECIFICATIONS

### For Each Module Include:

1. **Conceptual Introduction (15 min)**
   - Why this topic matters for fair value trading
   - Common misconceptions to address
   - Real-world motivation

2. **Mathematical Foundations (where applicable)**
   - Formal definitions with notation
   - Derivations of key formulas
   - Intuitive explanations alongside math

3. **Implementation Deep Dive**
   - Complete, working Python code
   - No pseudo-code or stubs - full implementations
   - Extensive code comments explaining logic
   - Edge case handling

4. **Common Pitfalls Section**
   - Specific mistakes practitioners make
   - How to detect these errors
   - Corrective actions

5. **Hands-On Exercises**
   - 3-4 exercises per module
   - Progressive difficulty
   - Solutions with explanations

6. **Real Data Applications**
   - Use actual commodity data (can simulate if needed)
   - Show real dates, real revision patterns
   - Include data sourcing instructions

7. **Knowledge Check Quiz**
   - 10-15 questions per module
   - Mix of conceptual and practical
   - Include code debugging questions

8. **Further Reading**
   - Academic papers (2-3 per module)
   - Industry reports
   - Documentation links

## TECHNICAL SPECIFICATIONS

### Code Standards:
- Python 3.9+ with type hints
- Follow PEP 8 style guide
- Comprehensive docstrings
- Unit tests for critical functions
- Error handling and logging

### Required Libraries:
```python
# Core
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sqlite3

# Modeling
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from scipy import optimize

# Visualization
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

# Time Series
from statsmodels.tsa.seasonal import seasonal_decompose
from arch import arch_model

# Custom utilities (to be developed in course)
from fair_value_toolkit import (
    PointInTimeDataFrame,
    FairValueModel,
    WalkForwardValidator,
    SignalGenerator
)
```

### Data Requirements:
- Provide sample datasets for each module
- Include data dictionary and schema
- Document update frequencies and lags
- Provide scripts to fetch/simulate data

### Assessment Criteria:
Each module should result in students being able to:
- Implement concepts in production code
- Identify and fix temporal data issues
- Build and validate fair value models
- Generate and evaluate trading signals
- Explain choices and trade-offs

## OUTPUT DELIVERABLES

Generate complete course materials including:

1. **Student Guide** (per module):
   - Learning objectives
   - Conceptual content (3000-4000 words)
   - Mathematical formulations
   - 10+ code examples (complete, runnable)
   - 3-4 hands-on exercises
   - Quiz questions with answers
   - Capstone project component

2. **Instructor Materials**:
   - Teaching notes
   - Common student questions
   - Debugging guides
   - Solution keys with explanations
   - Discussion prompts

3. **Code Repository Structure**:
```
fair-value-course/
├── requirements.txt
├── setup.py
├── data/
│   ├── sample_data/
│   └── data_fetchers/
├── src/
│   ├── fair_value_toolkit/
│   │   ├── __init__.py
│   │   ├── point_in_time.py
│   │   ├── models.py
│   │   ├── validation.py
│   │   └── signals.py
│   └── utils/
├── notebooks/
│   ├── module_01_foundations.ipynb
│   ├── module_02_temporal_data.ipynb
│   └── ...
├── tests/
│   ├── test_point_in_time.py
│   └── test_models.py
├── exercises/
│   └── module_XX_exercises.py
└── solutions/
    └── module_XX_solutions.py
```

4. **Assessment Materials**:
   - Pre-course assessment
   - Module quizzes (auto-gradeable)
   - Practical exercises with test suites
   - Final capstone project rubric
   - Competency certification criteria

## QUALITY REQUIREMENTS

The generated course must:

1. **Be Immediately Actionable**
   - Students can implement ideas same day
   - Code runs without modification
   - Clear path from learning to application

2. **Maintain Temporal Discipline Throughout**
   - Every example respects point-in-time constraints
   - No accidental look-ahead bias in any code
   - Revision handling in all data examples

3. **Focus on Signal Discovery**
   - Not just forecasting prices
   - Finding divergences that can be traded
   - Understanding when signals work/fail

4. **Include Realistic Complexity**
   - Address messy real-world data issues
   - Handle missing data, outliers, revisions
   - Show actual trading considerations

5. **Build Progressively**
   - Each module builds on previous
   - Concepts reinforce throughout
   - Final project uses all skills

## DIFFERENTIATION CHECKLIST

Ensure the course clearly differs from generic commodities courses by:

☐ Every data example shows observation vs. publication dates
☐ All backtests use walk-forward validation with proper data vintages
☐ Fair value is derived from fundamentals, not technical analysis
☐ Focus on divergence signals, not price prediction
☐ Include data revision analysis in every module
☐ Show actual trading implementation, not just models
☐ Address regime changes and model failure modes
☐ Include production system considerations
☐ Demonstrate P&L attribution to model alpha
☐ Validate everything without look-ahead bias

## EXECUTION INSTRUCTIONS

Generate this course as if you are creating materials for a major financial institution's trading desk training program. Assume students are:
- Quantitatively capable (can code Python)
- New to commodities trading
- Will be trading real money after course completion
- Need to avoid costly mistakes from data issues

Make it practical, rigorous, and immediately useful. Include enough detail that someone could build a production trading system from these materials.

Begin with Module 1 and continue through all 10 modules, maintaining consistent quality and depth throughout. Each module should genuinely require 4 hours to complete properly.