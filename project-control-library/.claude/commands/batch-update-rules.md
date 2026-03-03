---
allowed-tools: Bash, Read, Write, Edit, Glob
argument-hint: [--all | project-name] [--dry-run]
description: Push updated core CLAUDE rules to all managed projects
---

# Batch Update Rules

Push core CLAUDE rules to all projects: $ARGUMENTS

## Process

1. **Read source rules**: Load `project-control-library/templates/claude-template/.claude/CLAUDE.md`
2. **For each managed project**:
   a. Read current `.claude/CLAUDE.md`
   b. Compare with source template
   c. Identify sections that differ
   d. Update behavioral directives (Implementation Philosophy, Prohibited Patterns, Quality Gates)
   e. Preserve project-specific additions (custom patterns, project-specific constraints)
   f. Report what changed

## Merge Strategy
- **Always update**: Prohibited Patterns, Quality Gates sections
- **Merge (additive)**: Analysis Framework — add new items, keep project-specific ones
- **Never overwrite**: currentDate, project-specific configuration
- **Report conflicts**: Where project customizations conflict with new rules

## Dry Run Mode
When `--dry-run` is specified:
- Show what would change in each project
- Don't write any files
- Report conflicts and merge decisions
