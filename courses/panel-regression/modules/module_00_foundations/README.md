# Module 0: Foundations

## Overview

Establish the mathematical and computational foundations for panel data analysis. Review OLS, understand matrix notation, and set up your computing environment.

**Time Estimate:** 4-6 hours

## Learning Objectives

By completing this module, you will:
1. Review OLS estimation in matrix form
2. Understand the assumptions underlying regression
3. Set up Python/R environments for panel analysis
4. Recognize panel data structures in practice

## Contents

### Guides
- `01_ols_review.md` - OLS in matrix form
- `02_data_structures.md` - Panel data organization
- `03_environment_setup.md` - Python and R setup

### Notebooks
- `01_ols_fundamentals.ipynb` - Matrix algebra for regression
- `02_data_preparation.ipynb` - Preparing panel datasets

## Key Concepts

### Matrix Form of OLS

$$\hat{\beta} = (X'X)^{-1}X'y$$

### Gauss-Markov Assumptions

1. **Linearity**: $y = X\beta + \epsilon$
2. **Exogeneity**: $E[\epsilon|X] = 0$
3. **No multicollinearity**: $rank(X) = k$
4. **Homoskedasticity**: $Var(\epsilon|X) = \sigma^2 I$
5. **No autocorrelation**: $E[\epsilon_i \epsilon_j] = 0$ for $i \neq j$

### Panel Data Structure

| Entity (i) | Time (t) | X₁ | X₂ | Y |
|------------|----------|----|----|---|
| 1 | 1 | ... | ... | ... |
| 1 | 2 | ... | ... | ... |
| 2 | 1 | ... | ... | ... |
| 2 | 2 | ... | ... | ... |

## Prerequisites

- Linear algebra basics
- Probability and statistics
- Python or R programming
