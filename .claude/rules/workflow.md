---
description: Core workflow guidelines for all development tasks
---

# Workflow Guidelines

## Implementation Standards
- Never use mock data, results, or workarounds
- Generate complete, working code - no stubs, TODOs, or placeholder functions
- Implement tests after every checkpoint and verify all tests pass
- Always run `npm run lint` and `npm run build` to verify changes before completing

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

## Code Quality
- Write self-documenting code with clear naming over excessive comments
- Delete dead code completely - no commented-out blocks or unused imports
- Do not add features, refactoring, or improvements beyond what was asked
- Keep functions focused with single responsibility
