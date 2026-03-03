---
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
argument-hint: [--all | project-name]
description: Update documentation across all managed projects
---

# Batch Update Docs

Update documentation across managed projects: $ARGUMENTS

## Process

1. **Discover projects**: Read `config.json` for managed project list
2. **For each project**:
   a. Read CLAUDE.md to understand project structure
   b. Check if implementation has drifted from documentation
   c. Update metric counts (pages, routers, tests, models)
   d. Update architecture section if new directories/patterns exist
   e. Update README.md if features have changed
   f. Update STATUS.md with current completion state
3. **Report**: Summary of what was updated in each project
