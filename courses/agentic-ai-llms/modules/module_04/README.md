# Module 4: Planning & Reasoning

## Overview

Move beyond reactive question-answering to proactive goal achievement. This module covers agent reasoning patterns—ReAct, goal decomposition, self-reflection—that enable complex multi-step task completion.

**Time Estimate:** 8-10 hours

## Learning Objectives

By completing this module, you will:
1. Implement the ReAct (Reasoning + Acting) pattern
2. Build agents that decompose goals into subtasks
3. Add self-reflection and error correction
4. Design planning strategies for complex tasks

## Contents

### Guides
- `01_react_pattern.md` - Reasoning and Acting in loops
- `02_goal_decomposition.md` - Breaking complex tasks into steps
- `03_self_reflection.md` - Critique and correction

### Notebooks
- `01_react_agents.ipynb` - Building ReAct agents from scratch
- `02_planning_agents.ipynb` - Goal-oriented planning
- `03_reflection_agents.ipynb` - Agents that learn from mistakes

## Key Concepts

### ReAct Loop

```
User Goal → Thought → Action → Observation → Thought → ... → Final Answer
```

Example:
```
Goal: "Find the capital of the country that won the 2022 FIFA World Cup"

Thought: I need to find who won the 2022 World Cup first.
Action: search("2022 FIFA World Cup winner")
Observation: Argentina won the 2022 FIFA World Cup.

Thought: Now I need to find the capital of Argentina.
Action: search("capital of Argentina")
Observation: Buenos Aires is the capital of Argentina.

Thought: I have the answer.
Final Answer: Buenos Aires
```

### Planning Approaches

| Approach | Description | Use Case |
|----------|-------------|----------|
| ReAct | Interleaved thinking and action | General problem solving |
| Plan-and-Execute | Create full plan first | Structured tasks |
| Hierarchical | Nested sub-plans | Complex projects |
| Adaptive | Replan based on observations | Dynamic environments |

### Self-Reflection

```
Execute Plan → Evaluate Outcome → Identify Issues → Revise Approach → Retry
```

## Prerequisites

- Module 0-3 completed
- Understanding of tool calling
- Basic agent loop implementation
