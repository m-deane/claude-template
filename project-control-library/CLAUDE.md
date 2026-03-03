# CLAUDE.md — Project Control Library

## Problem Statement

Managing multiple software projects with Claude Code sessions requires constant manual context-switching, repetitive housekeeping, inconsistent documentation practices, and fragmented workflow orchestration. Developers waste significant time on:

- **Prompt engineering per session** — crafting effective prompts from scratch for each task
- **Cross-project coordination** — no unified view of what's happening across repositories
- **Documentation drift** — CLAUDE.md files, plans, and docs fall out of sync with actual implementation
- **Session cleanup** — uncommitted work, stale branches, orphaned files accumulate
- **Service management** — port conflicts, killed processes, and manual startup/teardown
- **No reusable patterns** — solving the same orchestration problems differently each time

This library solves all of the above by providing a meta-control layer that sits in your `~/projects/` directory with read/write access to all child repositories, offering skills, agents, and batch operations to orchestrate Claude Code sessions across your entire portfolio.

## Commercial Use Case

A solo developer or small team managing 5-20 active repositories needs a single control plane to:
1. Generate well-structured prompts with success criteria tied to each project's CLAUDE.md
2. Spin up agent teams (Opus for planning, Sonnet for implementation) with proper delegation
3. Launch services on safe ports without killing other projects' processes
4. Maintain documentation, commit hygiene, and project status across all repos
5. Run batch operations (commit all, update all docs, review all projects)
6. Track token usage and optimize agent team efficiency

## Architecture

```
~/projects/
├── project-control-library/          # THIS LIBRARY (the control plane)
│   ├── CLAUDE.md                     # This file
│   ├── .claude/
│   │   ├── CLAUDE.md                 # Behavioral directives
│   │   ├── skills/                   # 5 core skills (see below)
│   │   ├── commands/                 # Slash commands for batch ops
│   │   ├── agents/                   # Specialized control agents
│   │   └── hooks/                    # Session lifecycle hooks
│   ├── .claude_plans/
│   │   └── control-library-plan.md   # Implementation plan
│   ├── scripts/                      # Python/bash utility scripts
│   │   ├── port-manager.py           # Safe port allocation
│   │   ├── project-scanner.py        # Discover and index all repos
│   │   ├── token-tracker.py          # Token usage monitoring
│   │   └── housekeeping.sh           # Directory cleanup automation
│   ├── templates/                    # Base templates (from claude-template)
│   │   └── claude-template/          # Symlink or copy of base template
│   ├── catalog/                      # Registry of all skills, hooks, plugins
│   │   ├── skills.json               # Skill catalog with metadata
│   │   ├── hooks.json                # Hook catalog
│   │   ├── agents.json               # Agent catalog
│   │   └── plugins.json              # Plugin catalog
│   ├── status/                       # Per-project status tracking
│   │   └── {project-name}.status.md  # Auto-generated status files
│   └── config.json                   # Global configuration
├── claude-template/                  # Base template repo
├── project-a/                        # Managed project
├── project-b/                        # Managed project
└── ...
```

## Model Strategy

| Role | Model | Rationale |
|------|-------|-----------|
| Planning, architecture, reviews | Opus 4.6 (`claude-opus-4-6`) | Deep reasoning for complex decisions |
| Implementation, code generation | Sonnet 4.6 (`claude-sonnet-4-6`) | Fast, cost-effective code output |
| Quick lookups, simple tasks | Haiku 4.5 (`claude-haiku-4-5-20251001`) | Minimal token cost |

## Core Skills (5)

### 1. `give-me-a-prompt`
Generate a well-structured prompt with success criteria linked to the target project's CLAUDE.md.
- Reads target project's CLAUDE.md to understand context
- Produces a prompt with: problem statement, success criteria, constraints, expected output
- Supports manual review notes injection
- Diagnoses the problem, identifies solutions, plans implementation

### 2. `create-demo-notebooks`
Generate Python demo notebooks showcasing project features.
- Creates Jupyter notebooks with working examples
- Covers key APIs, data flows, and integration points
- Includes markdown documentation cells with explanations
- Auto-discovers project capabilities from CLAUDE.md and router/API definitions

### 3. `create-an-agent-team`
Design and deploy multi-agent teams with Opus planning and Sonnet implementation.
- Plan phase: Opus 4.6 architects the approach, defines agent roles
- Review phase: Opus 4.6 validates the plan against success criteria
- Implement phase: Sonnet 4.6 agents execute in parallel where possible
- Reports token usage per agent and total team cost

### 4. `launch`
Start backend and frontend services on unused ports without disrupting other projects.
- Scans for occupied ports before allocation
- Never kills processes from other projects on pre-existing ports
- Supports launching: dev servers, doc sites, dashboards, artifacts
- Maintains a port registry in `config.json`
- Provides a status dashboard of all running services

### 5. `finalise-session`
End-of-session housekeeping, documentation, and commit automation.
- Updates CLAUDE.md with session changes
- Updates documentation and plans
- Commits to git with descriptive messages
- Sorts project folders and directories
- Consolidates .claude_plans/ into unified plan
- Generates/updates project status file
- Cleans root directory (moves misplaced files to correct folders)

## Slash Commands

| Command | Purpose |
|---------|---------|
| `/batch-commit` | Commit across all managed projects |
| `/batch-update-docs` | Update docs in all managed projects |
| `/batch-init` | Re-initialize all projects from latest template |
| `/batch-review` | Run project review across all repos |
| `/batch-production-readiness` | Production readiness check for all projects |
| `/batch-housekeeping` | Run housekeeping across all projects |
| `/batch-update-rules` | Push updated CLAUDE rules to all projects |
| `/catalog` | View/update catalog of skills, hooks, plugins, agents |

## Control Agent Responsibilities

The control agent (this library's primary agent) manages:

1. **Agent team orchestration** — spawn, monitor, and collect results from agent teams
2. **Token usage optimization** — track and report token spend per project/session
3. **Status tracking** — maintain to-do lists and completion status per project
4. **Cross-project coordination** — prevent conflicts, share learnings
5. **Post-task automation** — after every agent team finishes: update docs, run tests, update to-do lists, commit to GitHub

## Housekeeping Rules

After every agent team completes work on any project:

1. **Consolidate plans** — merge all `.claude_plans/*.md` into one unified plan showing what was implemented and when, synced with CLAUDE.md
2. **Update and launch docs** — ensure documentation reflects current state
3. **Tidy root directory** — no orphaned files in project root; move files to correct folders
4. **Generate status file** — `STATUS.md` in project root with completed/incomplete items
5. **Clean directory structure** — enforce consistent folder organization

## Template Updates

When updating templates across projects:
- Launch services, docs, dashboards, websites, and artifacts on **unused ports only**
- Scan existing port allocations before starting anything
- Register new services in the central port registry
- Provide a single command to see all running services across all projects

## Configuration

```json
{
  "projects_root": "~/projects",
  "managed_projects": [],
  "port_registry": {},
  "token_budget": {
    "daily_limit": 1000000,
    "alert_threshold": 0.8
  },
  "models": {
    "planning": "claude-opus-4-6",
    "implementation": "claude-sonnet-4-6",
    "quick": "claude-haiku-4-5-20251001"
  },
  "housekeeping": {
    "auto_commit": true,
    "auto_docs": true,
    "auto_consolidate_plans": true,
    "clean_root_directory": true
  }
}
```

## Commands

```bash
# Discover and register all projects in ~/projects
python scripts/project-scanner.py

# Check port availability
python scripts/port-manager.py --check 3000-4000

# Track token usage for current session
python scripts/token-tracker.py --session

# Run full housekeeping on a project
bash scripts/housekeeping.sh ~/projects/my-project

# Generate project status report
python scripts/project-scanner.py --status
```

## Quality Gates

- All managed projects must pass their own lint/build/test suites
- CLAUDE.md must be in sync with actual implementation
- No orphaned files in project root directories
- All plans consolidated and timestamped
- Git working tree clean after finalise-session
- Port registry accurate (no stale entries)
- Token usage within budget

## Troubleshooting

- **Port conflict**: Run `python scripts/port-manager.py --scan` to find available ports
- **Stale status**: Run `/batch-housekeeping` to refresh all project statuses
- **Template drift**: Run `/batch-update-rules` to push latest CLAUDE rules everywhere
- **Token overspend**: Check `python scripts/token-tracker.py --report` for per-project breakdown
