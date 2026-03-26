---
description: Core workflow guidelines for all development tasks
---

# Workflow Guidelines

## Implementation Standards
- Never use mock data, results, or workarounds
- Generate complete, working code - no stubs, TODOs, or placeholder functions
- Implement tests after every checkpoint and verify all tests pass
- Always run `npm run lint` and `npm run build` to verify changes before completing

## Verification (Anti-Hallucination)
- Verify files exist before importing from them - do not invent import paths
- Verify functions, methods, and properties exist and check their actual signatures before calling them
- Verify package dependencies are installed in package.json before using them
- Verify database models and fields match the schema before writing queries
- Run build/lint after each logical change, not just at the end
- Do not invent CLI flags, configuration options, or API parameters - verify they exist first
- Do not recommend installing new packages without verifying the exact package name exists in the npm registry
- When a library's API has changed across major versions, prefer codebase patterns over training knowledge - the codebase reflects the installed version
- When a library's API is unclear, search the codebase for existing usage before guessing

## Grounding (Stay Anchored to Reality)
- Read the actual source file before modifying or referencing it
- Use existing project patterns as templates - copy and adapt, do not invent new patterns
- When uncertain, search the codebase for existing usage before writing new code
- State assumptions explicitly rather than proceeding silently
- When facing ambiguity, ask for clarification rather than guessing intent
- Before implementing a feature with ambiguous requirements, state your interpretation of the expected behavior in one sentence before writing code

## Scope Control
- Restate the specific task before starting implementation
- Only change what is necessary to fulfill the stated task
- Do not refactor, optimize, or "improve" adjacent code unless asked
- If changes affect shared interfaces, flag the downstream impact first
- Do not add features, abstractions, or configurability beyond what was requested

## File Organization
- Planning documents go in `.claude_plans/`
- Tests go in `tests/`
- Do not leave files in the root directory - sort into appropriate folders
- Prefer editing existing files over creating new ones

## Change Management
- Read and understand existing code before modifying it
- Match the style and patterns of surrounding code
- Make atomic, focused changes - one logical change per unit of work
- Verify changes compile and pass linting before marking complete

## Security
- Never commit secrets, credentials, API keys, or .env files
- Validate at system boundaries; trust internal code and framework guarantees
- Do not add error handling for impossible scenarios
- All tRPC procedures that accept user input must validate with a complete Zod schema - do not use `.passthrough()`

## Code Quality
- Write self-documenting code with clear naming over excessive comments
- Delete dead code completely - no commented-out blocks or unused imports
- Do not add features, refactoring, or improvements beyond what was asked
- Keep functions focused with single responsibility
