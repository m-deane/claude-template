---
mode: agent
description: "Orchestrate complex automation workflows with task dependencies, scheduling, and cross-platform execution"
tools: ["read", "edit", "execute"]
---

# Workflow Orchestrator

Orchestrate complex automation workflows: ${input:scope}

## Task

Create and manage complex automation workflows with dependency management, scheduling, and monitoring.

## Workflow Definition Structure

### Basic Workflow Schema
```json
{
  "name": "deployment-workflow",
  "version": "1.0.0",
  "description": "Complete deployment automation with testing and rollback",
  "trigger": {
    "type": "manual|schedule|webhook|file_change",
    "config": {}
  },
  "environment": {},
  "tasks": [
    {
      "id": "task-id",
      "name": "Task Name",
      "type": "shell",
      "command": "npm run validate",
      "timeout": 300,
      "depends_on": [],
      "on_success": [],
      "on_failure": []
    }
  ]
}
```

## Advanced Workflow Features

### Conditional Execution
Execute tasks based on conditions (previous task results, environment variables).

### Parallel Task Execution
Run independent tasks concurrently with configurable wait strategies (all, any, first).

### Loop and Iteration
Deploy to multiple environments or process multiple items with stop-on-failure control.

## Workflow Operations

### Create
- Define workflow schema with tasks, dependencies, and triggers
- Set up environment variables and configuration
- Configure notifications and alerting

### Run
- Validate workflow definition
- Execute tasks respecting dependency graph
- Handle errors with retry and rollback strategies

### Schedule
- Set up cron-based scheduling
- Configure systemd timers for Linux deployments

### Monitor
- Track execution metrics (success rate, duration, throughput)
- Configure alerts for failures, high failure rates, and long durations
- Generate health reports

## CLI Usage

```bash
workflow create --name "deployment" --template "web-app"
workflow run deployment-workflow.json
workflow schedule --cron "0 2 * * *" backup-workflow.json
workflow monitor --live
workflow history --limit 10
workflow validate deployment-workflow.json
```

This workflow orchestrator provides enterprise-grade automation capabilities with dependency management, monitoring, and cross-platform execution support.
