---
allowed-tools: Bash, Read, Write, Edit, Glob
argument-hint: [--all | project-name] [--template claude-template]
description: Re-initialize projects from latest base template
---

# Batch Init

Re-initialize projects from latest template: $ARGUMENTS

## Process

1. **Read base template**: Load claude-template's `.claude/` directory structure
2. **For each target project**:
   a. Compare existing `.claude/agents/`, `.claude/commands/`, `.claude/skills/` with template
   b. Identify new or updated files in template
   c. Copy new agents/commands/skills that don't exist in target
   d. Report updated files (don't overwrite project-specific customizations)
   e. Update `.claude/CLAUDE.md` behavioral directives if template has changes
3. **Report**: What was added/updated per project, what was skipped (project customizations preserved)

## Safety
- Never overwrite project-specific CLAUDE.md (root) — only .claude/CLAUDE.md directives
- Never overwrite project-specific skill customizations
- Always preserve project's own agents/commands that aren't in the template
- Report differences rather than auto-merging conflicting files
