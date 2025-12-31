# Module 1: LLM Fundamentals for Agents

## Overview

Master the prompting techniques that make agents reliable and effective. From system prompts to chain-of-thought reasoning, these fundamentals underpin every agent system.

**Time Estimate:** 6-8 hours

## Learning Objectives

By completing this module, you will:
1. Design effective system prompts for agent personas
2. Implement chain-of-thought and structured reasoning
3. Use few-shot examples to guide agent behavior
4. Optimize prompts for cost and latency

## Contents

### Guides
- `01_system_prompts.md` - Designing agent personas and instructions
- `02_chain_of_thought.md` - Reasoning patterns for complex tasks
- `03_few_shot_learning.md` - Teaching by example

### Notebooks
- `01_system_prompt_design.ipynb` - Building and testing system prompts
- `02_reasoning_patterns.ipynb` - CoT, ToT, and structured reasoning
- `03_prompt_optimization.ipynb` - Reducing tokens while maintaining quality

## Key Concepts

### The Prompt Hierarchy

```
System Prompt (persistent context)
    ↓
Few-Shot Examples (optional demonstrations)
    ↓
User Message (current request)
    ↓
Assistant Response (model output)
```

### System Prompt Components

1. **Identity:** Who is the agent?
2. **Capabilities:** What can it do?
3. **Constraints:** What should it avoid?
4. **Format:** How should it respond?
5. **Tools:** What tools are available?

### Chain-of-Thought Variants

| Pattern | Use Case |
|---------|----------|
| Zero-shot CoT | "Let's think step by step" |
| Few-shot CoT | Examples with reasoning traces |
| Self-consistency | Multiple reasoning paths, vote on answer |
| Tree-of-Thought | Explore branching possibilities |

## Prerequisites

- Module 0 completed
- API access configured
