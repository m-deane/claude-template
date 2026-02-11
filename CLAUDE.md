# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Claude Code project template** - a reusable starting point for new projects optimized for Claude Code workflows. It includes pre-configured slash commands, specialized agents, workflow templates, and directory structure conventions.

## Repository Structure

```
.claude/                    # Claude Code configuration (core of this template)
├── CLAUDE.md               # Core behavioral directives
├── TEMPLATE_GUIDE.md       # Customization instructions
├── example_prompt.md       # Project requirements template
├── settings.json           # Hooks configuration (post-edit, pre-commit)
├── agents/                 # 16 specialized agents
├── commands/               # 17 slash commands
├── scripts/                # Utility scripts
└── skills/                 # Skills (webapp-testing, mcp-builder, custom-skill-example)

.claude_plans/              # Project planning documents
.claude_prompts/            # Workflow prompt templates
.claude_research/           # Research document storage
src/                        # Source code placeholder
tests/                      # Test files placeholder
```

## Key Slash Commands

| Command | Purpose |
|---------|---------|
| `/ultra-think [problem]` | Deep multi-dimensional analysis |
| `/code-review [file]` | Comprehensive code review |
| `/generate-tests [component]` | Generate test suite |
| `/security-scan [scope]` | Security audit |
| `/explain-code [file]` | Detailed code explanation |
| `/create-pr [branch]` | Auto-generate PR description |
| `/dependency-update` | Check/update dependencies |
| `/architecture-review` | Review architecture patterns |
| `/create-architecture-documentation` | Generate architecture docs |
| `/parallel-agents [features]` | Self-healing parallel agent implementation with build gates |
| `/test-driven-fix [bug]` | Test-driven bug fix with codebase-wide sibling scanning |
| `/autonomous-review [scope]` | Full autonomous review pipeline with parallel audit and fixes |

## Key Agents

| Agent | Use For |
|-------|---------|
| `python-pro` | Python best practices, optimization |
| `typescript-pro` | TypeScript type system, strict mode |
| `sql-expert` | Schema design, query optimization |
| `ml-engineer` | ML pipelines, MLOps |
| `test-engineer` | Test strategy, coverage |
| `code-reviewer` | Code quality, security |
| `debugger` | Error investigation |

## Template Customization Workflow

When using this template for a new project:

1. Clone/copy this repository
2. Edit root `CLAUDE.md` - replace `<!-- CUSTOMIZE -->` sections with project specifics
3. Copy `.claude/example_prompt.md` to `.claude_prompts/` and customize
4. Delete `.claude/TEMPLATE_GUIDE.md` after setup
5. Update `.gitignore` for your language/framework

## Core Directives (from .claude/CLAUDE.md)

The template enforces these behavioral patterns:

- **No partial implementations** - Complete working code, no mocks/stubs/TODOs
- **Direct implementation** - Skip hedging language and excessive explanation
- **File organization** - Use `.claude_plans/` for planning, `tests/` for tests
- **Testing discipline** - Run tests after each checkpoint
- **Build verification** - Always run build/compile after multi-file edits before declaring done
- **Codebase-wide fixes** - Grep for sibling patterns when fixing bugs, fix all instances
- **No over-delivery** - Stay focused on what was asked, no unsolicited extras
- **Large file guard** - Check for >50MB files before pushing to GitHub
- **Verify before done** - Run reproduction steps to confirm fixes, not just code inspection

## Hooks (from .claude/settings.json)

The template includes pre-configured hooks:

- **Post-Edit Build Check** - Runs build verification after every Edit/Write operation (customize command for your stack)
- **Pre-Commit Large File Guard** - Scans for files >50MB before committing to prevent failed GitHub pushes

See `.claude/TEMPLATE_GUIDE.md` for customization examples per language/framework.

## Adding New Commands

Create a markdown file in `.claude/commands/` with frontmatter:

```yaml
---
description: Brief description
argument-hint: [arg] | --flag
allowed-tools: Read, Write, Edit, Bash
---
```

## Adding New Agents

Create a markdown file in `.claude/agents/` with frontmatter:

```yaml
---
name: agent-name
description: When to use this agent
tools: Read, Write, Edit, Bash
model: sonnet
---
```
