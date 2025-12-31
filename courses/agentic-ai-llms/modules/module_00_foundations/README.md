# Module 0: Foundations

## Overview

This module ensures you have the technical foundations to build agent systems: understanding transformer architectures, setting up LLM APIs, and mastering basic prompt engineering.

**Time Estimate:** 4-6 hours

## Learning Objectives

By completing this module, you will:
1. Understand transformer architecture at a practical level
2. Set up and test multiple LLM provider APIs
3. Write effective basic prompts
4. Understand token economics and context windows

## Contents

### Guides
- `01_transformer_architecture.md` - How LLMs work under the hood
- `02_llm_providers.md` - Comparing Claude, GPT-4, and open-source
- `03_prompt_basics.md` - Foundation prompting techniques

### Notebooks
- `01_api_setup.ipynb` - Configure and test LLM APIs
- `02_token_exploration.ipynb` - Understanding tokenization and costs
- `03_basic_prompting.ipynb` - Prompt engineering exercises

## Key Concepts

### The Transformer Stack
```
Input Text → Tokenization → Embeddings → Attention Layers → Output Logits → Tokens → Text
```

### Context Window Comparison
| Model | Context Window | Cost (input/1M tokens) |
|-------|----------------|------------------------|
| Claude 3.5 Sonnet | 200K | $3.00 |
| GPT-4 Turbo | 128K | $10.00 |
| Llama 3 70B | 8K | Self-hosted |

### Token Economics
- Average English word ≈ 1.3 tokens
- Code is more token-dense than prose
- Context window = input + output tokens

## Prerequisites

- Python 3.10+
- Basic understanding of neural networks
- API key from at least one provider
