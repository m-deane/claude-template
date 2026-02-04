# Python Quantitative Finance Libraries - Comprehensive User Reference Guide

**Version:** 1.0.0
**Last Updated:** December 2025
**Authors:** Claude Code AI Assistant

---

## Overview

This comprehensive user reference guide covers four essential Python libraries for quantitative finance:

| Library | Purpose | Status |
|---------|---------|--------|
| [Alphalens](./alphalens/README.md) | Factor analysis and performance attribution | alphalens-reloaded v0.4.6 |
| [Pyfolio](./pyfolio/README.md) | Portfolio performance and risk analytics | pyfolio-reloaded v0.9.9 |
| [VectorBT](./vectorbt/README.md) | Vectorized backtesting framework | v0.28.2 |
| [OpenBB](./openbb/README.md) | Financial data platform | v4.5.0 |

---

## Quick Start Installation

```bash
# Install all libraries (recommended versions)
pip install alphalens-reloaded pyfolio-reloaded vectorbt "openbb[all]"

# Or install individually
pip install alphalens-reloaded    # Factor analysis
pip install pyfolio-reloaded      # Portfolio analytics
pip install vectorbt              # Backtesting
pip install openbb                # Financial data
```

---

## Guide Structure

### Per-Library Documentation

Each library section includes:

1. **Overview & Installation** - Purpose, installation, dependencies
2. **Complete API Reference** - Every class, function, and argument documented
3. **Plotting Functions** - With visual interpretation guides
4. **Use Cases by Skill Level**:
   - Beginner (step-by-step with extensive comments)
   - Intermediate (multiple parameters, error handling)
   - Advanced (production patterns, testing strategies)
   - Expert (institutional-grade implementations)
5. **Best Practices & Common Pitfalls**

### Integration Guides

- [Full Factor Research Pipeline](./integration/factor-research-pipeline.md) - OpenBB → Alphalens → Pyfolio
- [Backtesting with Risk Analytics](./integration/backtesting-risk-analytics.md) - VectorBT → Pyfolio
- [Research to Production Workflow](./integration/research-to-production.md) - All four libraries

### Appendices

- [Complete Parameter Reference Tables](./appendices/parameter-reference.md)
- [Return Type Reference](./appendices/return-types.md)
- [Exception Reference](./appendices/exceptions.md)
- [Performance Benchmarks](./appendices/benchmarks.md)
- [Glossary of Terms](./appendices/glossary.md)

---

## Library Comparison Matrix

| Feature | Alphalens | Pyfolio | VectorBT | OpenBB |
|---------|-----------|---------|----------|--------|
| **Primary Use** | Factor evaluation | Risk analysis | Backtesting | Data acquisition |
| **Input Data** | Factor + prices | Returns + positions | Price data | Ticker symbols |
| **Key Output** | IC, quantile returns | Tear sheets | Portfolio metrics | DataFrames |
| **Visualization** | matplotlib | matplotlib | plotly | plotly/matplotlib |
| **Performance** | Medium | Medium | Very High (Numba) | Depends on provider |
| **Learning Curve** | Medium | Low | High | Low |

---

## Recommended Workflows

### Workflow 1: Factor Research
```
OpenBB (data) → Alphalens (factor analysis) → Pyfolio (portfolio analysis)
```

### Workflow 2: Strategy Development
```
OpenBB (data) → VectorBT (backtest) → Pyfolio (risk analysis)
```

### Workflow 3: Complete Research Pipeline
```
OpenBB (data acquisition)
    ↓
Alphalens (alpha research)
    ↓
VectorBT (strategy backtesting)
    ↓
Pyfolio (comprehensive risk reporting)
```

---

## Sample Data Setup

All examples in this guide use sample data that can be generated with:

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Generate sample price data
def generate_sample_prices(symbols=['AAPL', 'GOOGL', 'MSFT'],
                           start='2020-01-01', periods=756):
    """Generate realistic-looking stock price data for examples."""
    dates = pd.date_range(start=start, periods=periods, freq='D')
    prices = pd.DataFrame(index=dates)

    np.random.seed(42)
    for symbol in symbols:
        # Start price between 100 and 500
        start_price = np.random.uniform(100, 500)
        # Daily returns with drift
        returns = np.random.normal(0.0005, 0.02, periods)
        prices[symbol] = start_price * np.cumprod(1 + returns)

    return prices

# Generate sample factor data
def generate_sample_factor(prices, name='momentum'):
    """Generate a sample factor based on price momentum."""
    # 20-day momentum factor
    factor = prices.pct_change(20).stack()
    factor.index.names = ['date', 'asset']
    factor.name = name
    return factor

# Generate sample returns
def generate_sample_returns(prices, symbol='AAPL'):
    """Generate daily returns series."""
    return prices[symbol].pct_change().dropna()

# Usage
prices = generate_sample_prices()
factor = generate_sample_factor(prices)
returns = generate_sample_returns(prices)
```

---

## Prerequisites

### Python Version
- **Minimum:** Python 3.9
- **Recommended:** Python 3.10 - 3.12

### Core Dependencies
All libraries require:
- numpy >= 1.20
- pandas >= 1.3
- matplotlib >= 3.4

### Optional Dependencies
- **numba** - Required for VectorBT performance
- **plotly** - Required for VectorBT/OpenBB interactive charts
- **scipy** - Required for statistical analysis
- **seaborn** - Required for Alphalens/Pyfolio styling

---

## Document Conventions

### Code Examples

All code examples follow these conventions:

```python
# Imports at the top
import alphalens as al
import pyfolio as pf
import vectorbt as vbt
from openbb import obb

# Comments explain the "why", not the "what"
# BAD: # Calculate mean
# GOOD: # Aggregate IC across time periods for stability assessment

# All examples are copy-paste runnable
# All examples include expected output descriptions
```

### Function Signatures

```python
function_name(
    param1,                    # Required parameter (type) - Description
    param2=default,            # Optional parameter (type) - Description
                               #   Default: value
                               #   Valid: list of valid values
)
# Returns: type - Description
# Raises: ExceptionType - When raised
```

### Interpretation Guides

For plotting functions:
- **What to look for:** Key patterns and indicators
- **Good signs:** Indicators of quality/success
- **Red flags:** Warning indicators
- **Common misinterpretations:** Frequent mistakes

---

## Version Compatibility

| Library | Tested Version | Python | Notes |
|---------|---------------|--------|-------|
| alphalens-reloaded | 0.4.6 | 3.10-3.13 | Use instead of original alphalens |
| pyfolio-reloaded | 0.9.9 | 3.9-3.13 | Use instead of original pyfolio |
| vectorbt | 0.28.2 | 3.6-3.12 | Free version in maintenance mode |
| openbb | 4.5.0 | 3.10-3.13 | Python 3.9 deprecated |

---

## Contributing

Found an error or want to contribute improvements? This guide is maintained as part of the claude-template project.

---

## License

This documentation is provided under the MIT License. The underlying libraries have their own licenses:
- Alphalens: Apache 2.0
- Pyfolio: Apache 2.0
- VectorBT: Apache 2.0 + Commons Clause
- OpenBB: AGPLv3
