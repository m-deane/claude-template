---
allowed-tools: Bash, Read, Glob, Grep
argument-hint: [--all | project-name]
description: Production readiness review for all managed projects
---

# Batch Production Readiness Review

Run production readiness checks: $ARGUMENTS

## Process

1. **For each managed project, check**:

### Security
- [ ] No secrets in code (scan for API keys, passwords, tokens)
- [ ] No `.env` files committed to git
- [ ] Dependencies have no critical vulnerabilities (`npm audit`)
- [ ] Authentication properly enforced on all routes
- [ ] Input validation on all user-facing endpoints (Zod .max() bounds)
- [ ] No SQL injection risks (parameterized queries / Prisma)
- [ ] CORS configured correctly
- [ ] Rate limiting in place

### Reliability
- [ ] All tests passing
- [ ] Error handling covers edge cases (TRPCError, not raw throw)
- [ ] No console.log/print statements in production code
- [ ] Database migrations are reversible
- [ ] Graceful shutdown handling

### Performance
- [ ] No N+1 query patterns (proper Prisma includes)
- [ ] Pagination on list endpoints
- [ ] Database indexes on frequently queried fields
- [ ] Static assets optimized (images, bundles)
- [ ] Build output size reasonable

### Operations
- [ ] README has deployment instructions
- [ ] Environment variables documented (.env.example)
- [ ] Health check endpoint exists
- [ ] Logging structured and meaningful
- [ ] Monitoring/alerting configured

2. **Generate readiness scorecard**: Pass/fail per category with remediation steps
