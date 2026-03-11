---
mode: agent
description: "Create a pull request with auto-generated description from commits and changes"
tools: ["read", "execute", "search"]
---

# Create Pull Request

Create a pull request: ${input:target}

## Task

Create a well-documented pull request following best practices.

### 1. Gather Information

**Commits Analysis:**
- List all commits in this branch vs base
- Identify the type of changes (feature, fix, refactor, docs, etc.)
- Extract key changes from commit messages

**Code Changes:**
- Summarize files changed
- Identify breaking changes
- Note any migration requirements

### 2. Generate PR Title

Format: `<type>(<scope>): <description>`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting, no code change
- `refactor`: Code restructuring
- `perf`: Performance improvement
- `test`: Adding tests
- `chore`: Maintenance

### 3. Generate PR Description

```markdown
## Summary
[2-3 sentences describing what this PR does and why]

## Changes
- [Change 1]
- [Change 2]
- [Change 3]

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Documentation update
- [ ] Refactoring (no functional changes)

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings introduced
- [ ] Tests pass locally
```

### 4. Pre-PR Checks

Before creating the PR, verify:
- Branch is up to date with base
- Tests pass
- Lint checks pass
- Changes are pushed

### 5. Create the PR

Use `gh pr create` with the generated title and body.

### 6. Post-Creation

After PR is created:
- Add appropriate labels
- Request reviewers
- Link related issues

## Output

Return:
- PR URL
- PR number
- Summary of what was included
