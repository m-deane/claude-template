# Module 2: Core HMM Algorithms

## Overview

Implement the three fundamental HMM algorithms: Forward-Backward for probability computation, Viterbi for optimal state decoding, and Baum-Welch for parameter estimation.

**Time Estimate:** 10-12 hours

## Learning Objectives

By completing this module, you will:
1. Implement the Forward algorithm from scratch
2. Implement the Backward algorithm and combine with Forward
3. Decode the most likely state sequence with Viterbi
4. Train HMMs using Baum-Welch (EM)
5. Understand log-space computation for numerical stability

## Contents

### Guides
- `01_forward_backward.md` - Computing observation likelihood
- `02_viterbi.md` - Most likely state sequence
- `03_baum_welch.md` - Parameter estimation

### Notebooks
- `01_forward_backward_impl.ipynb` - Forward-Backward from scratch
- `02_viterbi_impl.ipynb` - Viterbi implementation
- `03_em_training.ipynb` - Complete training loop

## Key Algorithms

### Forward Algorithm

**Purpose:** Compute $P(O | \lambda)$ efficiently

**Complexity:** $O(K^2 T)$ vs naive $O(K^T)$

```
α₁(i) = π_i · b_i(o₁)

αₜ₊₁(j) = [Σᵢ αₜ(i) · aᵢⱼ] · bⱼ(oₜ₊₁)

P(O|λ) = Σᵢ αₜ(i)
```

### Backward Algorithm

**Purpose:** Compute $P(o_{t+1},...,o_T | q_t, \lambda)$

```
βₜ(i) = 1  (final time)

βₜ(i) = Σⱼ aᵢⱼ · bⱼ(oₜ₊₁) · βₜ₊₁(j)
```

### Viterbi Algorithm

**Purpose:** Find $\argmax_Q P(Q | O, \lambda)$

```
δ₁(i) = π_i · b_i(o₁)
ψ₁(i) = 0

δₜ(j) = max_i [δₜ₋₁(i) · aᵢⱼ] · bⱼ(oₜ)
ψₜ(j) = argmax_i [δₜ₋₁(i) · aᵢⱼ]

Backtrack from argmax δₜ using ψ
```

### Baum-Welch (EM)

**E-Step:** Compute expected sufficient statistics

$$\gamma_t(i) = P(q_t = s_i | O, \lambda) = \frac{\alpha_t(i)\beta_t(i)}{\sum_j \alpha_t(j)\beta_t(j)}$$

$$\xi_t(i,j) = P(q_t = s_i, q_{t+1} = s_j | O, \lambda)$$

**M-Step:** Update parameters

$$\hat{\pi}_i = \gamma_1(i)$$

$$\hat{a}_{ij} = \frac{\sum_t \xi_t(i,j)}{\sum_t \gamma_t(i)}$$

## Numerical Considerations

### Log-Space Computation

Probabilities underflow quickly:
$$\alpha_{100}(i) \approx 10^{-100}$$

Solution: Work in log-space with log-sum-exp:

$$\log(a + b) = \log a + \log(1 + e^{\log b - \log a})$$

```python
def log_sum_exp(log_a, log_b):
    max_val = max(log_a, log_b)
    return max_val + np.log(np.exp(log_a - max_val) + np.exp(log_b - max_val))
```

## Prerequisites

- Module 0 and 1 completed
- Strong linear algebra fundamentals
- Python proficiency
