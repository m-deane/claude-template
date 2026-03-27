# Review: Cursor Template Parity with Claude Template

You are auditing a project template that provides AI-assisted development configurations for multiple tools. The `.claude/` configuration is the **master reference**. The `.cursor/` and `.cursorrules` configuration must achieve **functional parity** - delivering the same rules, constraints, and behaviors through Cursor's native configuration system.

## Success Criteria

Every rule, constraint, and guideline present in the Claude configuration MUST have an equivalent in the Cursor configuration. "Equivalent" means: if an LLM follows the Claude rules, it would produce identical code to an LLM following the Cursor rules, given the same task.

## Instructions

### Step 1: Inventory the Claude Master Configuration

Read every file in the Claude configuration and extract a flat list of every distinct rule/instruction:

**Files to read:**
- `CLAUDE.md` (root)
- `.claude/CLAUDE.md`
- `.claude/rules/workflow.md`
- `.claude/rules/code-style.md`
- `.claude/rules/testing.md`
- `.claude/rules/api-conventions.md`

For each rule, record:
- The exact rule text
- Which file it lives in
- Whether it is generic (applies always) or path-scoped (applies to specific files)

### Step 2: Inventory the Cursor Configuration

Read every file in the Cursor configuration:

**Files to read:**
- `.cursorrules`
- `.cursor/rules/api-conventions.mdc`
- `.cursor/rules/ui-components.mdc`
- `.cursor/rules/testing.mdc`

For each rule, record:
- The exact rule text
- Which file it lives in
- Whether it has a glob scope (from frontmatter)

### Step 3: Map Rules 1:1

Create a comparison table:

| # | Rule (from Claude master) | Claude File | Cursor File | Status |
|---|---|---|---|---|
| 1 | "Verify files exist before importing..." | .claude/CLAUDE.md | .cursorrules | MATCH / MISSING / DIFFERS |
| 2 | ... | ... | ... | ... |

**Status definitions:**
- **MATCH** - Rule exists in Cursor config with equivalent wording and scope
- **MISSING** - Rule exists in Claude config but has no equivalent in Cursor config
- **DIFFERS** - Rule exists in both but wording differs enough to potentially cause different LLM behavior
- **EXTRA** - Rule exists in Cursor config but not in Claude config (flag for review)

### Step 4: Check Structural Parity

Verify the Cursor configuration mirrors the Claude structure using Cursor's native mechanisms:

| Claude Feature | Cursor Equivalent | Status |
|---|---|---|
| `CLAUDE.md` (root project context) | `.cursorrules` (root project rules) | |
| `.claude/CLAUDE.md` (core directives) | Content merged into `.cursorrules` | |
| `.claude/rules/workflow.md` (always loaded) | Content in `.cursorrules` (always loaded) | |
| `.claude/rules/code-style.md` (always loaded) | Content in `.cursorrules` (always loaded) | |
| `.claude/rules/testing.md` (path-scoped to tests/) | `.cursor/rules/testing.mdc` (glob-scoped) | |
| `.claude/rules/api-conventions.md` (path-scoped to server/) | `.cursor/rules/api-conventions.mdc` (glob-scoped) | |
| `.claude/settings.json` (allow/deny permissions) | No Cursor equivalent (note as limitation) | |

**Key structural difference:** Claude loads `CLAUDE.md` + `.claude/CLAUDE.md` + all unconditional `rules/*.md` into every session. Cursor loads `.cursorrules` into every session. Therefore: all "always-loaded" Claude rules MUST be present in `.cursorrules`.

### Step 5: Check for Stale/Project-Specific Content

Flag any content in the Cursor files that:
- References a specific project (app names, specific frameworks like "tRPC", "Prisma", "NextAuth", "shadcn", "Supabase")
- Contains placeholder text that was not properly genericized (look for `<!-- CUSTOMIZE -->` markers that should be present but aren't, or project-specific examples that should have been replaced)
- Contains TODO items or incomplete sections
- Duplicates content from `.cursorrules` in `.cursor/rules/*.mdc` files unnecessarily

### Step 6: Verify Cursor-Specific Formatting

Check that Cursor files use the correct format:
- `.cursorrules` is a plain text/markdown file at the project root
- `.cursor/rules/*.mdc` files use proper MDC frontmatter:
  ```
  ---
  description: [when this rule applies]
  globs: ["pattern1", "pattern2"]
  ---
  ```
- Glob patterns in `.cursor/rules/` files are valid and match the equivalent `paths:` in `.claude/rules/`
- Rules without a glob scope in `.cursor/rules/` should have `alwaysApply: true` or be moved into `.cursorrules`

## Output Format

### Parity Report

A table listing every rule with its status (MATCH / MISSING / DIFFERS / EXTRA).

### Issues Found

For each MISSING or DIFFERS rule:
- The exact rule text from the Claude master
- Where it should be added in the Cursor config
- The exact text to add (adapted for Cursor's format if needed)

### Stale Content

List any project-specific references or placeholder issues found.

### Fixed Files

Output the complete corrected contents of every Cursor file that needs changes:
1. `.cursorrules` - complete file
2. `.cursor/rules/api-conventions.mdc` - complete file
3. `.cursor/rules/ui-components.mdc` - complete file
4. `.cursor/rules/testing.mdc` - complete file
5. Any new `.cursor/rules/*.mdc` files needed

For each file, wrap in a code block with the file path as header.

### Limitations

Note any Claude features that have no Cursor equivalent (e.g., settings.json permissions, agents, commands, skills) so the user understands what cannot be ported.
