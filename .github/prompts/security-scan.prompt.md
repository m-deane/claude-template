---
mode: agent
description: "Run security audit on codebase for vulnerabilities and best practices"
tools: ["read", "execute", "search"]
---

# Security Scan

Perform comprehensive security audit: ${input:scope}

## Task

Conduct a thorough security scan based on the specified scope:

### 1. Dependency Vulnerability Scan

Check for known vulnerabilities in dependencies using the appropriate package manager audit tools (npm audit, pip-audit, govulncheck, cargo audit, etc.).

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

Generate a security report with summary, dependency vulnerabilities, secrets detected, code vulnerabilities, and prioritized recommendations.

## Scope Options

- `--dependencies` - Only scan dependencies for vulnerabilities
- `--code` - Only scan code for security issues
- `--secrets` - Only scan for hardcoded secrets
- `--full` - Complete security audit (default)
- `[path]` - Scan specific directory or file
