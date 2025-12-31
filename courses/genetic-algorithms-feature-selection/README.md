# Genetic Algorithms for Feature Selection in Time Series Forecasting

## Course Overview

Apply evolutionary optimization to identify optimal feature subsets for time series prediction. Learn to design fitness functions, implement selection/crossover/mutation operators, and avoid overfitting when features are many and observations are few.

**Level:** Advanced
**Prerequisites:** ML fundamentals, time series basics, Python
**Duration:** 6 modules (8-10 weeks)
**Effort:** 8-10 hours per week

## Why Genetic Algorithms for Feature Selection?

Time series forecasting faces the curse of dimensionality:
- Many candidate features (lags, indicators, external variables)
- Limited training samples
- High risk of overfitting
- Exhaustive search is computationally infeasible

GAs provide:
- **Efficient Search**: Explore large feature spaces
- **Flexibility**: Custom fitness functions for any model
- **Robustness**: Population-based approach avoids local optima
- **Interpretability**: Final feature sets are explicit

## Learning Outcomes

By completing this course, you will:

1. **Understand** GA fundamentals and operators
2. **Design** fitness functions for time series prediction
3. **Implement** GAs with proper validation strategies
4. **Avoid** overfitting through nested cross-validation
5. **Apply** GAs to real forecasting problems
6. **Compare** GA results with other selection methods

## Course Structure

| Module | Topic | Key Skills |
|--------|-------|------------|
| 0 | Foundations | Optimization, search spaces |
| 1 | GA Fundamentals | Encoding, selection, crossover, mutation |
| 2 | Fitness Design | Validation strategies, objectives |
| 3 | Time Series Considerations | Walk-forward, stationarity |
| 4 | Implementation | DEAP, custom operators |
| 5 | Advanced Topics | Multi-objective, hybrid methods |

## Mathematical Foundation

### The Feature Selection Problem

Given:
- Feature set $F = \{f_1, f_2, ..., f_n\}$
- Target variable $y_t$
- Forecasting model $M$

Find: Subset $S \subseteq F$ that minimizes forecasting error

$$S^* = \argmin_{S \subseteq F} \text{CV\_Error}(M, S)$$

### Chromosome Representation

Binary encoding: Each bit represents feature inclusion

```
Chromosome: [1, 0, 1, 1, 0, 1, 0, 0, 1, 1]
                    ↓
Features:   [lag1, lag2, lag3, sma20, sma50, rsi, macd, ...]
                    ↓
Selected:   [lag1, lag3, sma20, rsi, ...]
```

### GA Operators

**Selection** (Tournament, Roulette):
$$P(\text{select}_i) \propto \text{fitness}_i$$

**Crossover** (Single-point, Uniform):
```
Parent 1: [1,0,1,1|0,1,0]
Parent 2: [0,1,0,1|1,0,1]
            ↓
Child:    [1,0,1,1|1,0,1]
```

**Mutation** (Bit-flip):
$$P(\text{flip bit}_i) = p_m \approx 0.01$$

## Key Concepts

### Fitness Function Design

```python
def fitness_function(chromosome, X, y):
    """Evaluate feature subset for forecasting."""
    selected_features = X[:, chromosome == 1]

    # Walk-forward cross-validation
    scores = walk_forward_cv(model, selected_features, y)

    # Combine accuracy and parsimony
    accuracy = -np.mean(scores)  # Negative MSE
    complexity = sum(chromosome) / len(chromosome)

    return accuracy - lambda_penalty * complexity
```

### Avoiding Overfitting

1. **Walk-Forward Validation**: Time-respecting splits
2. **Nested CV**: Outer loop for assessment, inner for selection
3. **Parsimony Pressure**: Penalize large feature sets
4. **Ensemble Validation**: Multiple forecast horizons

## Technology Stack

**Python Libraries:**
- `DEAP` - Distributed Evolutionary Algorithms
- `scikit-learn` - ML models
- `pandas`, `numpy` - Data handling
- `statsmodels` - Time series models

```bash
pip install deap scikit-learn pandas numpy statsmodels
```

## Sample Problems

1. **Stock Price Forecasting**: Select from 100+ technical indicators
2. **Energy Demand**: Weather, calendar, economic features
3. **Commodity Prices**: Fundamentals, positioning, macro variables
4. **Volatility Prediction**: Realized measures, regime indicators

---

*"Genetic algorithms don't find the global optimum—they find good solutions fast. In feature selection, 'good enough' often outperforms overfitted 'optimal'."*
