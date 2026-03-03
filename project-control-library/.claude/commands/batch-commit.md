---
allowed-tools: Bash, Read, Glob, Grep
argument-hint: [--all | project-name] [--message "commit message"]
description: Commit changes across all managed projects or a specific project
---

# Batch Commit

Commit changes across managed projects: $ARGUMENTS

## Process

1. **Discover projects**: Read `config.json` for managed project list, or scan `~/projects/*/`
2. **For each project with uncommitted changes**:
   a. Run the project's lint command (skip commit if lint fails)
   b. Run the project's test command (skip commit if tests fail)
   c. Stage all changes: `git add -A`
   d. Commit with descriptive message or provided `--message`
   e. Report commit hash and summary
3. **Report**: Show which projects were committed, skipped (no changes), or failed (lint/test)

## Safety
- Never force-push
- Never commit .env files or secrets
- Skip projects with failing tests (report them instead)
- Use project-specific commit conventions if defined in CLAUDE.md
