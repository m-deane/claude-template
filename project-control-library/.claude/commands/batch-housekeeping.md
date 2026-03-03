---
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
argument-hint: [--all | project-name]
description: Run full housekeeping across all managed projects
---

# Batch Housekeeping

Run housekeeping across all projects: $ARGUMENTS

## Process

For each managed project, execute the full housekeeping sequence:

1. **Consolidate plans**: Merge `.claude_plans/*.md` into `UNIFIED_PLAN.md`
   - Mark items as IMPLEMENTED / IN PROGRESS / PLANNED
   - Sync with CLAUDE.md claims

2. **Update CLAUDE.md metrics**: Recount pages, routers, models, tests
   - Verify scale numbers match actual file counts

3. **Clean root directory**: Relocate misplaced files
   - Move stray `.md` files to `docs/`
   - Move scripts to `scripts/`
   - Move notebooks to `notebooks/`
   - Delete `.tmp`, `.bak`, `.log` files older than 7 days

4. **Generate/update STATUS.md**: Completed and incomplete items

5. **Update and launch docs**: Ensure docs reflect current state

6. **Git status check**: Report uncommitted changes (don't auto-commit in batch mode)

7. **Report per project**: What was cleaned, moved, updated
