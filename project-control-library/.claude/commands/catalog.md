---
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
argument-hint: [view | update | export] [--type skills|hooks|agents|plugins]
description: View and manage the catalog of all skills, hooks, plugins, and agents across projects
---

# Catalog Manager

Manage the catalog of skills, hooks, plugins, and agents: $ARGUMENTS

## Process

### View Mode (`catalog view`)

Scan all managed projects and display:

```markdown
## Skills Catalog
| Skill | Project | Description | Status |
|-------|---------|-------------|--------|
| give-me-a-prompt | control-library | Generate prompts with success criteria | active |
| mcp-builder | claude-template | Build MCP servers | active |
| webapp-testing | claude-template | Playwright automation | active |

## Commands Catalog
| Command | Project | Description |
|---------|---------|-------------|
| /ultra-think | claude-template | Deep multi-dimensional analysis |
| /batch-commit | control-library | Cross-project commits |

## Agents Catalog
| Agent | Project | Model | Purpose |
|-------|---------|-------|---------|
| code-reviewer | claude-template | sonnet | Code quality review |
| typescript-pro | claude-template | sonnet | TypeScript expertise |

## Hooks Catalog
| Hook | Project | Trigger | Action |
|------|---------|---------|--------|
| (discovered hooks listed here) |
```

### Update Mode (`catalog update`)

Re-scan all projects and rebuild catalog files:

```bash
# Scan for skills
find ~/projects/*/.claude/skills/*/SKILL.md

# Scan for commands
find ~/projects/*/.claude/commands/*.md

# Scan for agents
find ~/projects/*/.claude/agents/*.md

# Scan for hooks
find ~/projects/*/.claude/hooks/ -type f
find ~/projects/*/.claude/settings.json -exec grep -l "hooks" {} \;
```

Write results to `catalog/skills.json`, `catalog/agents.json`, etc.

### Export Mode (`catalog export`)

Generate a single markdown document listing everything:
- All skills with descriptions and phases
- All commands with argument hints
- All agents with model assignments
- All hooks with trigger conditions
- Cross-references showing which projects use which items
