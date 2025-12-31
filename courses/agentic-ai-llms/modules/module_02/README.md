# Module 2: Tool Use & Function Calling

## Overview

Transform LLMs from text generators into actors. Tool use allows agents to interact with external systems—search the web, query databases, execute code, and manipulate files. This module covers tool design, error handling, and security.

**Time Estimate:** 8-10 hours

## Learning Objectives

By completing this module, you will:
1. Design clear, effective tool schemas
2. Implement robust tool execution with error handling
3. Build agents that chain multiple tool calls
4. Apply security best practices for tool execution

## Contents

### Guides
- `01_tool_fundamentals.md` - How LLM tool calling works
- `02_tool_design.md` - Principles for effective tool schemas
- `03_error_handling.md` - Graceful failure and recovery

### Notebooks
- `01_basic_tools.ipynb` - Implementing your first tools
- `02_multi_tool_agents.ipynb` - Agents that use multiple tools
- `03_tool_security.ipynb` - Security patterns and sandboxing

## Key Concepts

### Tool Calling Flow

```
User Query → LLM Decides Tool Needed → Tool Call Generated
                                            ↓
                              Your Code Executes Tool
                                            ↓
                              Result Returned to LLM
                                            ↓
                              LLM Generates Response
```

### Tool Definition Components

| Component | Purpose | Example |
|-----------|---------|---------|
| Name | Identifies the tool | `search_web` |
| Description | When to use it | "Search the web for current information" |
| Parameters | What inputs it needs | `{"query": "string", "limit": "integer"}` |
| Required | Which params are mandatory | `["query"]` |

### Tool Design Principles

1. **Single Responsibility**: One tool, one purpose
2. **Clear Naming**: Verbs that describe the action
3. **Helpful Descriptions**: When AND when not to use
4. **Safe Defaults**: Sensible parameter defaults
5. **Bounded Output**: Limit response sizes

## Prerequisites

- Module 0 and 1 completed
- Python environment with Anthropic SDK
- Basic understanding of JSON Schema
