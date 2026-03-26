# Core Directives

## WORKFLOW - Core Guidelines

- Never use mock data, results, or workarounds
- Generate complete, working code - no stubs, TODOs, or placeholder functions
- Implement tests after every checkpoint and verify all tests pass
- Write all tests to the `tests/` folder
- Only update progress and create planning documents in `.claude_plans/`
- Do not leave files in the root directory - sort into appropriate folders
- Always run `npm run lint` and `npm run build` to verify changes before completing
- Read and understand existing code before modifying it
- Match the style and patterns of surrounding code
- Make atomic, focused changes - one logical change per unit of work
- Never commit secrets, credentials, API keys, or .env files
- Handle all UI states: loading, error, empty, and success
- Validate at system boundaries; trust internal code and framework guarantees
- Prefer editing existing files over creating new ones
- Verify changes compile and pass linting before marking complete
- Write self-documenting code with clear naming over excessive comments
- Delete dead code completely - no commented-out blocks or unused imports

## Analysis Framework

When encountering complex requirements:
1. **Technical feasibility**: Can this be done with the current stack patterns?
2. **Edge cases**: Empty data, invalid inputs, unauthorized access?
3. **Performance**: N+1 queries? Missing includes/relations?
4. **Integration**: Does this affect existing routers or components?

## Prohibited Patterns

### Implementation
- Mock functions or placeholder data structures
- Incomplete error handling or validation
- Queries without user scoping (`userId: ctx.session.user.id`)
- Direct database access outside tRPC routers
- Using `any` type when proper types exist in `src/types/`
- Console.log statements in committed code

### Communication
- Social validation: "You're absolutely right!", "Great question!"
- Hedging language: "might", "could potentially", "perhaps"
- Excessive explanation of obvious concepts

## File Boundaries

**SAFE TO MODIFY**: `src/`, `prisma/schema.prisma`, `tests/`
**NEVER MODIFY**: `node_modules/`, `.git/`, `.next/`, `.env` files

## Pre-Completion Checklist

- `npm run lint` passes
- `npm run build` succeeds
- All tRPC procedures are user-scoped
- No TypeScript errors or console.log statements
- All tests pass
- Changes are atomic and focused
