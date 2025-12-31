# Panel Regression Models with Fixed and Random Effects

## Course Overview

Master econometric techniques for analyzing panel (longitudinal) data—observations of multiple entities over time. Learn to choose between fixed and random effects, handle common estimation challenges, and apply these methods to real-world time series and cross-sectional data.

**Level:** Advanced
**Prerequisites:** Linear regression, basic econometrics, Python/R proficiency
**Duration:** 6 modules (8-10 weeks)
**Effort:** 8-10 hours per week

## Why Panel Regression?

Cross-sectional data captures variation across entities. Time series captures variation over time. Panel data captures both—enabling you to:

- **Control for unobserved heterogeneity** across entities
- **Model dynamic relationships** while accounting for individual differences
- **Improve efficiency** with more observations and variation
- **Address endogeneity** through within-entity variation

## Learning Outcomes

By completing this course, you will:

1. **Understand** when and why to use panel data methods
2. **Distinguish** between fixed effects, random effects, and pooled OLS
3. **Apply** the Hausman test and other diagnostic tools
4. **Handle** practical challenges: clustering, serial correlation, heteroskedasticity
5. **Implement** panel models in Python (statsmodels, linearmodels) and R
6. **Interpret** results correctly for policy and business applications

## Course Structure

| Module | Topic | Key Skills |
|--------|-------|------------|
| 0 | Foundations | Data structures, OLS review, matrix notation |
| 1 | Panel Data Structure | Long vs wide format, balanced vs unbalanced panels |
| 2 | Fixed Effects Models | Within transformation, entity dummies, time FE |
| 3 | Random Effects Models | GLS estimation, when to use random effects |
| 4 | Model Selection | Hausman test, specification tests, diagnostics |
| 5 | Advanced Topics | Dynamic panels, clustered errors, GMM |

## Mathematical Foundation

### The Basic Panel Model

$$y_{it} = \alpha + X_{it}\beta + u_{it}$$

Where:
- $y_{it}$: Outcome for entity $i$ at time $t$
- $X_{it}$: Vector of covariates
- $u_{it} = \mu_i + \epsilon_{it}$: Composite error (entity effect + idiosyncratic)

### Fixed Effects Model

$$y_{it} = \alpha_i + X_{it}\beta + \epsilon_{it}$$

Each entity has its own intercept $\alpha_i$, capturing time-invariant unobserved characteristics.

### Random Effects Model

$$y_{it} = \alpha + X_{it}\beta + \mu_i + \epsilon_{it}$$

Entity effects $\mu_i$ are treated as random draws from a distribution, uncorrelated with $X_{it}$.

## Technology Stack

**Python:**
- `linearmodels` - Panel data econometrics
- `statsmodels` - Statistical modeling
- `pandas` - Data manipulation
- `numpy` - Numerical computing

**R:**
- `plm` - Panel linear models
- `lmtest` - Diagnostic tests
- `sandwich` - Robust standard errors

## Setup

```bash
# Python environment
pip install linearmodels statsmodels pandas numpy matplotlib seaborn

# R packages
install.packages(c("plm", "lmtest", "sandwich", "stargazer"))
```

## Datasets Used

- **Grunfeld Investment Data**: Classic panel of 10 firms over 20 years
- **Crime Dataset**: State-level panel for policy analysis
- **Penn World Tables**: Cross-country economic data
- **Custom Commodity Data**: Commodity fundamentals panel

---

*"Panel data allows you to control for what you cannot observe—the hidden factors that drive differences across entities."*
