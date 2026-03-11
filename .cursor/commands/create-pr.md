# Create Pull Request

Create a pull request with auto-generated description from commits and changes.

## Current State

Review the current state before creating the PR:
- Identify the current branch
- Determine the base branch (typically main or master)
- Review unpushed commits
- Review changed files compared to base branch

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

Example: `feat(auth): add OAuth2 login with Google`

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

### Test Instructions
[How to test these changes]

## Screenshots (if applicable)
[Add screenshots for UI changes]

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings introduced
- [ ] Tests pass locally

## Related Issues
Closes #[issue-number]
```

### 4. Pre-PR Checks

Before creating the PR, verify:
- Ensure the branch is up to date with the base branch
- Run tests to confirm they pass
- Check for lint issues
- Push all changes to the remote

### 5. Create the PR

Use the GitHub CLI (`gh pr create`) with the generated title and body. Support options for:
- Draft PRs
- Specific reviewers
- Labels

### 6. Post-Creation

After PR is created:
- Add appropriate labels
- Request reviewers
- Link related issues
- Add to project board (if applicable)

## Output

Return:
- PR URL
- PR number
- Summary of what was included

Refer to @project-instructions for project-specific conventions.
