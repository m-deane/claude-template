---
name: create-demo-notebooks
description: Generate Python Jupyter demo notebooks that showcase project features, APIs, data flows, and integration points. Auto-discovers capabilities from CLAUDE.md and source code.
---

# Create Demo Notebooks — Project Feature Showcase Generator

## Overview

Automatically generate Python Jupyter notebooks that demonstrate a project's features, APIs, data flows, and integration points. Notebooks are created with working code examples, markdown documentation, and clear explanations suitable for stakeholders, new developers, or demo purposes.

---

# Process

## Phase 1: Project Discovery

### 1.1 Read Project Context

Load and analyze the target project's documentation:

```bash
# Read project CLAUDE.md for overview
cat ~/projects/{target}/CLAUDE.md

# Read API routes/routers for available endpoints
find ~/projects/{target}/src -name "*.ts" -path "*/routers/*" | head -30

# Read types and schemas
cat ~/projects/{target}/src/types/index.ts 2>/dev/null | head -200
```

### 1.2 Identify Demonstrable Features

From the CLAUDE.md and source code, catalog:
- **API endpoints/procedures** — what data operations are available
- **Data models** — what entities exist and their relationships
- **Key workflows** — multi-step operations (create → update → query)
- **Integration points** — external APIs, databases, auth flows
- **Utility functions** — reusable logic worth demonstrating

### 1.3 Plan Notebook Structure

Create a notebook plan:

```markdown
## Notebook Plan
1. `01-project-overview.ipynb` — Architecture, stack, and key concepts
2. `02-data-models.ipynb` — Schema exploration and relationships
3. `03-core-api-demo.ipynb` — CRUD operations on primary entities
4. `04-advanced-workflows.ipynb` — Multi-step operations and integrations
5. `05-analytics-and-reporting.ipynb` — Data analysis and visualization
```

---

## Phase 2: Notebook Generation

### 2.1 Standard Notebook Structure

Every notebook follows this template:

```python
# Cell 1: Title and Description (Markdown)
"""
# {Feature Name} — Demo Notebook
**Project**: {Project Name}
**Date**: {Current Date}
**Purpose**: {What this notebook demonstrates}

## Prerequisites
- {Required setup, API keys, database access}
"""

# Cell 2: Setup and Configuration (Code)
import requests
import json
import os
from datetime import datetime

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:3000")
API_URL = f"{BASE_URL}/api/trpc"

# Helper function for tRPC calls
def trpc_query(procedure: str, input_data: dict = None):
    """Execute a tRPC query."""
    url = f"{API_URL}/{procedure}"
    params = {"input": json.dumps(input_data)} if input_data else {}
    response = requests.get(url, params=params)
    return response.json()

def trpc_mutation(procedure: str, input_data: dict):
    """Execute a tRPC mutation."""
    url = f"{API_URL}/{procedure}"
    response = requests.post(url, json=input_data)
    return response.json()

# Cell 3+: Feature demonstrations with markdown explanations
```

### 2.2 Content Guidelines

Each demonstration cell must include:
- **Markdown explanation** before the code cell explaining what's being demonstrated and why
- **Working code** that can be executed against the running project
- **Output interpretation** — comments explaining what the output means
- **Error handling** — graceful handling of common failures
- **Variations** — show different parameter combinations

### 2.3 Visualization Cells

Where appropriate, add visualization:

```python
import matplotlib.pyplot as plt
import pandas as pd

# Convert API response to DataFrame for analysis
df = pd.DataFrame(data)

# Visualization with clear labels
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_title("Task Distribution by Category")
ax.set_xlabel("Category")
ax.set_ylabel("Count")
df.groupby("category")["id"].count().plot(kind="bar", ax=ax)
plt.tight_layout()
plt.show()
```

---

## Phase 3: Output and Organization

### 3.1 File Placement

```
{target_project}/
└── notebooks/
    ├── README.md                          # Index of all notebooks
    ├── requirements.txt                   # Python dependencies
    ├── 01-project-overview.ipynb
    ├── 02-data-models.ipynb
    ├── 03-core-api-demo.ipynb
    ├── 04-advanced-workflows.ipynb
    └── 05-analytics-and-reporting.ipynb
```

### 3.2 Requirements File

```
jupyter>=1.0
requests>=2.31
pandas>=2.0
matplotlib>=3.7
python-dotenv>=1.0
tabulate>=0.9
```

### 3.3 README Index

Generate a README.md that lists all notebooks with:
- Notebook name and description
- Prerequisites for running
- Expected runtime
- Key features demonstrated

### 3.4 Quality Checks

Before delivering:
- [ ] All code cells have markdown explanation cells preceding them
- [ ] No hardcoded credentials or secrets
- [ ] API URLs use environment variables
- [ ] Error handling present for network calls
- [ ] Notebooks can run independently (no cross-notebook dependencies)
- [ ] Requirements.txt includes all dependencies
- [ ] README index is complete and accurate
