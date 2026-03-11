# Security Scan

Perform a comprehensive security audit on the specified scope, dependencies, code, secrets, or the full project.

## Current State

Before starting, review the project to understand:
- The repository root and project type
- Available package files (package.json, requirements.txt, etc.)
- Current git status

## Task

Conduct a thorough security scan based on the specified scope:

### 1. Dependency Vulnerability Scan

Check for known vulnerabilities in dependencies:

**Python:**
```bash
pip-audit 2>/dev/null || safety check 2>/dev/null || echo "Install: pip install pip-audit"
```

**Node.js:**
```bash
npm audit 2>/dev/null || echo "Run: npm audit"
```

**Go:**
```bash
govulncheck ./... 2>/dev/null || echo "Install: go install golang.org/x/vuln/cmd/govulncheck@latest"
```

### 2. Secret Detection

Scan for hardcoded secrets, API keys, and credentials:

- Look for patterns: API keys, tokens, passwords, private keys
- Check common files: `.env`, config files, test fixtures
- Scan git history for accidentally committed secrets
- Check for AWS keys, GitHub tokens, database credentials

**Patterns to search:**
- `password\s*=`
- `api[_-]?key\s*=`
- `secret\s*=`
- `token\s*=`
- `private[_-]?key`
- `-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----`
- `AKIA[0-9A-Z]{16}` (AWS Access Key)
- `ghp_[a-zA-Z0-9]{36}` (GitHub Personal Token)

### 3. Code Security Analysis

Review code for common vulnerabilities:

**Injection Vulnerabilities:**
- SQL injection (raw queries, string concatenation)
- Command injection (shell=True, os.system, exec)
- XSS (unescaped user input in HTML)
- Path traversal (unsanitized file paths)

**Authentication & Authorization:**
- Hardcoded credentials
- Weak password policies
- Missing authentication checks
- Insecure session management

**Data Exposure:**
- Sensitive data in logs
- Verbose error messages
- Missing encryption for sensitive data
- Insecure data transmission

**Configuration Issues:**
- Debug mode in production
- CORS misconfiguration
- Missing security headers
- Insecure default settings

### 4. OWASP Top 10 Checklist

- [ ] A01: Broken Access Control
- [ ] A02: Cryptographic Failures
- [ ] A03: Injection
- [ ] A04: Insecure Design
- [ ] A05: Security Misconfiguration
- [ ] A06: Vulnerable Components
- [ ] A07: Authentication Failures
- [ ] A08: Software and Data Integrity Failures
- [ ] A09: Security Logging Failures
- [ ] A10: Server-Side Request Forgery

### 5. Report Generation

Generate a security report with:

```markdown
# Security Scan Report

## Summary
- Total Issues Found: X
- Critical: X
- High: X
- Medium: X
- Low: X

## Dependency Vulnerabilities
| Package | Version | Vulnerability | Severity | Fix Version |
|---------|---------|---------------|----------|-------------|

## Secrets Detected
| File | Line | Type | Status |
|------|------|------|--------|

## Code Vulnerabilities
| File | Line | Issue | Severity | Recommendation |
|------|------|-------|----------|----------------|

## Recommendations
1. [Priority action items]
2. [Security improvements]
3. [Best practices to adopt]
```

## Scope Options

- **dependencies** - Only scan dependencies for vulnerabilities
- **code** - Only scan code for security issues
- **secrets** - Only scan for hardcoded secrets
- **full** - Complete security audit (default)
- A specific path - Scan specific directory or file

## Tools Used

The scan will attempt to use available security tools:
- **Python**: pip-audit, safety, bandit
- **Node.js**: npm audit, snyk
- **Go**: govulncheck, gosec
- **General**: gitleaks, trufflehog, semgrep

Refer to @project-instructions for project-specific security requirements.
