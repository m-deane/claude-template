---
mode: agent
description: "Check and update project dependencies with security and compatibility analysis"
tools: ["read", "edit", "execute"]
---

# Dependency Update

Manage project dependencies: ${input:scope}

## Task

Analyze and optionally update project dependencies.

### 1. Dependency Analysis

**Detect Package Manager:**
- `package.json` -> npm/yarn/pnpm
- `requirements.txt` / `pyproject.toml` -> pip/poetry
- `Cargo.toml` -> cargo
- `go.mod` -> go modules
- `Gemfile` -> bundler

**Check Current Versions** using the appropriate outdated command for the detected package manager.

### 2. Categorize Updates

Group dependencies by update type:

| Category | Risk Level | Action |
|----------|------------|--------|
| **Patch** (1.0.0 -> 1.0.1) | Low | Usually safe to update |
| **Minor** (1.0.0 -> 1.1.0) | Medium | Review changelog |
| **Major** (1.0.0 -> 2.0.0) | High | Breaking changes likely |
| **Security** | Critical | Update immediately |

### 3. Security Vulnerabilities

Check for known vulnerabilities using audit tools (npm audit, pip-audit, govulncheck, cargo audit).

### 4. Compatibility Check

Before updating, verify:
- [ ] Peer dependency compatibility
- [ ] Node/Python/Go version requirements
- [ ] Breaking change impact
- [ ] Deprecated API usage

### 5. Update Report

Generate a dependency update report with summary, security updates, major updates, minor updates, patch updates, and recommendations.

### 6. Perform Updates

Apply updates based on the requested scope (patches only, all updates, security-only).

### 7. Post-Update Verification

After updating:
- Run tests
- Check for runtime issues
- Verify build succeeds
- Commit updated lock files

## Safety Guidelines

1. **Always run tests** after updating
2. **Update incrementally** for large projects
3. **Read changelogs** for major updates
4. **Keep lock files** in version control
5. **Don't update** right before releases
