# Fair Value Modelling for Commodities Trading

A comprehensive, interactive course on building and validating fair value models for commodity markets, with special emphasis on temporal data discipline and signal discovery.

## Course Overview

This course teaches you how to build robust fair value models for commodities while avoiding common pitfalls like look-ahead bias and data leakage. Each module combines economic theory, practical implementation, and real-world trading applications.

**Duration**: ~35 hours of content
**Prerequisites**: Python (intermediate), pandas, basic statistics, linear regression
**Technical Stack**: pandas, scikit-learn, SQLite, matplotlib, plotly

## Key Learning Themes

### 1. Point-in-Time Data Discipline
- Understanding observation date vs publication date vs revision date
- Building infrastructure for as-of queries
- Avoiding look-ahead bias in backtests

### 2. Fair Value Model Theory
- Inventory-based models (storage theory)
- Cost-of-carry models (futures pricing)
- Supply-demand balance models
- Cost curve models (marginal producer)

### 3. Signal Discovery
- Identifying when fair value diverges from market price
- Distinguishing model error from true mispricing
- Combining fundamental signals with market signals

## Quick Start

```bash
# Create and activate virtual environment
python -m venv fair-value-env
source fair-value-env/bin/activate  # Linux/Mac
# fair-value-env\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Launch Jupyter
jupyter notebook

# Start with Module 1
# notebooks/01_foundations/notebook.ipynb
```

## Course Structure

### Module 1: Foundations of Commodities Fair Value
- What is "fair value" in commodity markets?
- Economic foundations: storage theory, convenience yield
- Why fair value models matter for trading
- Introduction to the course toolkit

### Module 2: Point-in-Time Data Architecture
- The data leakage problem in finance
- Observation date vs publication date vs as-of date
- Building a point-in-time data infrastructure
- SQLite-based temporal queries

### Module 3: Exploratory Data Analysis with Temporal Discipline
- EDA that respects time boundaries
- Vintage comparison: how data revisions affect analysis
- Detecting structural breaks and regime changes
- Visualizing data quality over time

### Module 4: Commodity Data Sources and Quality
- Free vs premium data sources
- API integration: Yahoo Finance, FRED, EIA
- Data quality assessment framework
- Handling missing data and outliers temporally

### Module 5: Fair Value Model Fundamentals
- Inventory-based models (Kaldor, Working)
- Cost-of-carry models for futures
- Supply-demand balance models
- Combining multiple approaches

### Module 6: Feature Engineering for Commodities
- Temporal feature engineering principles
- Lagged features and rolling statistics
- Seasonal adjustments
- Interaction features and relative strength

### Module 7: Model Validation with Walk-Forward Testing
- Why cross-validation fails for time series
- Walk-forward validation framework
- Expanding vs rolling windows
- Gap periods and embargo rules

### Module 8: Signal Discovery and Alpha Generation
- From fair value to trading signal
- Z-score normalization and signal strength
- Mean reversion half-life estimation
- Combining model signals with market signals

### Module 9: Production Systems and Monitoring
- Deploying fair value models in production
- Model decay and retraining schedules
- Performance monitoring dashboards
- Handling model degradation

### Module 10: Advanced Topics
- Hierarchical models for commodity complexes
- Bayesian model averaging for uncertainty
- Machine learning augmentation
- Regime-switching models

### Capstone Project
Build a complete fair value forecasting and signal generation system for a commodity portfolio, including:
- Point-in-time data infrastructure
- Multiple fair value models
- Walk-forward backtesting
- Signal generation and risk analysis

## Directory Structure

```
fair-value-commodities-course/
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── src/
│   └── fair_value_toolkit/       # Course library
│       ├── __init__.py
│       ├── point_in_time.py      # Temporal data infrastructure
│       ├── models.py             # Fair value model classes
│       ├── validation.py         # Walk-forward validation
│       ├── signals.py            # Signal generation
│       └── features.py           # Feature engineering
├── data/
│   ├── sample_data/              # Sample datasets
│   └── data_fetchers/            # Data download utilities
├── notebooks/
│   ├── 01_foundations/
│   │   ├── notebook.ipynb
│   │   └── exercises.ipynb
│   ├── 02_point_in_time/
│   ├── 03_temporal_eda/
│   ├── 04_data_sources/
│   ├── 05_fair_value_models/
│   ├── 06_feature_engineering/
│   ├── 07_walk_forward_validation/
│   ├── 08_signal_discovery/
│   ├── 09_production_systems/
│   └── 10_advanced_topics/
├── exercises/                    # Practice problems
├── solutions/                    # Exercise solutions
├── projects/
│   └── capstone_project.ipynb
└── tests/
    └── test_toolkit.py
```

## Core Concepts

### Point-in-Time Data

The most important concept in this course is **point-in-time data discipline**. Most financial data gets revised after initial publication:

- Economic indicators (GDP, employment) are revised multiple times
- Inventory reports may be corrected
- Corporate actions affect historical prices

A proper backtesting framework must use data **as it was known at the time**, not the final revised values.

```python
from fair_value_toolkit import PointInTimeDataFrame

# Query data as it was known on a specific date
data_vintage = pit_data.as_of('2023-01-15')
```

### Fair Value Models

We implement several classes of fair value models:

1. **Inventory-based**: Price = f(inventory deviation from norm)
2. **Cost-of-carry**: Spot = Forward / exp(r + c - y)
3. **Supply-demand**: Price clears where supply = demand
4. **Cost curve**: Price = marginal cost of production

### Signal Generation

Fair value alone isn't a signal. We convert fair value to signals via:

```python
from fair_value_toolkit import SignalGenerator

# Calculate mispricing z-score
signal_gen = SignalGenerator(entry_threshold=1.5, exit_threshold=0.5)
signals = signal_gen.generate(fair_values, market_prices)
```

## Key Learning Outcomes

By completing this course, you will be able to:

1. **Build point-in-time data infrastructure** for proper backtesting
2. **Implement fair value models** based on economic theory
3. **Validate models** using walk-forward testing
4. **Generate trading signals** from fair value estimates
5. **Detect and avoid** data leakage and look-ahead bias
6. **Monitor model performance** in production

## Prerequisites

### Required Knowledge
- Python programming (intermediate)
- pandas for data manipulation
- Basic probability and statistics
- Linear regression concepts

### Recommended Background
- Time series analysis basics
- Some exposure to commodities/finance
- SQL basics (for point-in-time queries)

## Installation

### Full Installation

```bash
pip install -r requirements.txt
```

### Minimal Installation

```bash
# Core (all modules)
pip install numpy pandas matplotlib scipy scikit-learn

# Database (Module 2+)
pip install sqlalchemy

# Data fetching
pip install yfinance pandas-datareader

# Interactive visualizations
pip install plotly ipywidgets
```

## Data Sources

The course uses real and synthetic commodity data:

- **Yahoo Finance**: Futures prices (free, via yfinance)
- **FRED**: Economic indicators and inventories (free API)
- **Synthetic data**: Realistic simulations for testing

Available commodities include:
- Energy: Crude Oil (WTI, Brent), Natural Gas, Gasoline
- Metals: Gold, Silver, Copper, Platinum
- Agriculture: Corn, Wheat, Soybeans, Coffee, Sugar

## Contributing

Contributions welcome! Areas of interest:
- Additional fair value model types
- More commodity examples
- Improved visualizations
- Bug fixes

## License

Educational use. See LICENSE file.

## Acknowledgments

This course draws on:
- Academic literature on commodity pricing (Kaldor, Working, Brennan)
- Quantitative finance best practices
- Real-world trading system design

---

**Remember: Fair value models don't predict prices—they help you understand when prices have deviated from fundamentals. The alpha comes from knowing when those deviations will correct.**
