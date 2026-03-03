# Project Control Library

A meta-orchestration system that sits in your `~/projects/` directory and manages Claude Code sessions across multiple repositories.

## Prerequisites

- Python 3.9+
- Claude Code CLI installed
- Git

## Quick Start

```bash
# 1. Clone/copy to your projects directory
cp -r project-control-library ~/projects/

# 2. Open a Claude Code session
cd ~/projects/project-control-library
claude

# 3. The SessionStart hook auto-registers your projects
# Or manually run:
python3 scripts/project-scanner.py --register
```

## What's Included

### 5 Skills

| Skill | Purpose |
|-------|---------|
| `give-me-a-prompt` | Generate prompts with success criteria from any project's CLAUDE.md |
| `create-demo-notebooks` | Auto-generate Jupyter notebooks showcasing project features |
| `create-an-agent-team` | Deploy multi-agent teams (Opus planning + Sonnet implementation) |
| `launch` | Start services on unused ports without killing other projects |
| `finalise-session` | End-of-session housekeeping, docs, commits, directory cleanup |

### 8 Batch Commands

| Command | Purpose |
|---------|---------|
| `/batch-commit` | Commit across all managed projects |
| `/batch-update-docs` | Update docs in all managed projects |
| `/batch-init` | Re-initialize projects from template |
| `/batch-review` | Health check across all repos |
| `/batch-production-readiness` | Production readiness assessment |
| `/batch-housekeeping` | Clean all project directories |
| `/batch-update-rules` | Push CLAUDE rules to all projects |
| `/catalog` | View/update skill, command, agent catalog |

### 4 Utility Scripts

```bash
python3 scripts/project-scanner.py          # Discover projects
python3 scripts/port-manager.py --scan      # Check port registry
python3 scripts/token-tracker.py --budget   # Token usage budget
bash scripts/housekeeping.sh ~/projects/X   # Clean a project directory
```

## Model Strategy

| Role | Model |
|------|-------|
| Planning, architecture, reviews | Opus 4.6 |
| Implementation, code generation | Sonnet 4.6 |
| Quick lookups, simple tasks | Haiku 4.5 |

## Configuration

Edit `config.json` to customize:
- `projects_root` — where your projects live (default: `~/projects`)
- `token_budget` — daily token limit and alert threshold
- `housekeeping` — auto-commit, auto-docs, and cleanup settings

See [CLAUDE.md](CLAUDE.md) for full documentation.
