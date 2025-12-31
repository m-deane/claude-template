# Module 2: Fixed Effects Models

## Overview

Fixed effects models control for unobserved, time-invariant characteristics of each entity. This is the workhorse of panel econometrics, essential for causal inference when entities differ in unmeasured ways.

**Time Estimate:** 8-10 hours

## Learning Objectives

By completing this module, you will:
1. Understand the fixed effects estimator and its assumptions
2. Implement FE using within-transformation and dummy variables
3. Apply entity fixed effects and time fixed effects
4. Interpret FE coefficients correctly
5. Recognize when FE is appropriate

## Contents

### Guides
- `01_fixed_effects_intuition.md` - Why and when to use FE
- `02_within_transformation.md` - The mathematical derivation
- `03_twoway_fixed_effects.md` - Entity and time fixed effects

### Notebooks
- `01_fe_implementation.ipynb` - FE in Python and R
- `02_fe_diagnostics.ipynb` - Testing FE assumptions
- `03_twfe_practice.ipynb` - Two-way fixed effects examples

## Key Concepts

### The Fixed Effects Model

$$y_{it} = \alpha_i + X_{it}\beta + \epsilon_{it}$$

- $\alpha_i$: Entity-specific intercept (fixed effect)
- Captures all time-invariant differences between entities
- Allows correlation between $\alpha_i$ and $X_{it}$

### The Within Transformation

Transform data to remove entity effects:

$$\tilde{y}_{it} = y_{it} - \bar{y}_i$$
$$\tilde{X}_{it} = X_{it} - \bar{X}_i$$

Then estimate: $\tilde{y}_{it} = \tilde{X}_{it}\beta + \tilde{\epsilon}_{it}$

### Key Properties

| Property | Description |
|----------|-------------|
| Eliminates $\alpha_i$ | By demeaning, entity effects cancel |
| Time-invariant X | Variables constant within entity are eliminated |
| Degrees of freedom | Loses $n-1$ DF for entity dummies |
| Consistency | Consistent even if $Cov(\alpha_i, X_{it}) \neq 0$ |

### Two-Way Fixed Effects

$$y_{it} = \alpha_i + \lambda_t + X_{it}\beta + \epsilon_{it}$$

Controls for both entity-specific and time-specific unobservables.

## Prerequisites

- Module 0 and 1 completed
- Understanding of OLS assumptions
