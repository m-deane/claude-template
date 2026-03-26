# Core Directives

## WORKFLOW - Core Guidelines

### Implementation Standards
- Never use mock data, results, or workarounds
- Generate complete, working code - no stubs, TODOs, or placeholder functions
- Implement tests after every checkpoint and verify all tests pass
- Write all tests to the `tests/` folder
- Only update progress and create planning documents in `.claude_plans/`
- Do not leave files in the root directory - sort into appropriate folders
- Always run lint and build commands to verify changes before completing

### Verification (Anti-Hallucination)
- Verify files exist before importing from them - do not invent import paths
- Verify functions, methods, and properties exist and check their actual signatures before calling them
- Verify package dependencies are installed before using them in code
- Verify database models and fields match the schema before writing queries
- When referencing code, cite actual file paths - do not reference files you have not read
- Run build/lint after each logical change, not just at the end
- If a library's API is unclear, search the codebase for existing usage patterns before guessing
- Do not invent CLI flags, configuration options, or API parameters - verify they exist first
- Do not recommend installing new packages without verifying the exact package name exists in the registry
- When a library's API has changed across major versions, prefer codebase patterns over training knowledge - the codebase reflects the installed version

### Grounding (Stay Anchored to Reality)
- Read the actual source file before modifying or referencing it - never assume file contents
- Use existing project patterns as templates - copy and adapt working code, do not invent new patterns
- When uncertain about an API or method, search the codebase for existing usage before writing new code
- State assumptions explicitly rather than proceeding silently on uncertain ground
- When facing ambiguity in requirements, ask for clarification rather than guessing intent
- Before implementing a feature with ambiguous requirements, state your interpretation of the expected behavior in one sentence before writing code
- Reference concrete code (file paths, function names) rather than abstract descriptions

### Scope Control
- Restate the specific task before starting implementation to confirm understanding
- Only change what is necessary to fulfill the stated task
- Do not refactor, optimize, or "improve" adjacent code unless asked
- If the task requires changes to shared interfaces, flag the downstream impact before proceeding
- Do not add features, abstractions, or configurability beyond what was requested

### Change Management
- Read and understand existing code before modifying it
- Match the style and patterns of surrounding code
- Make atomic, focused changes - one logical change per unit of work
- Prefer editing existing files over creating new ones
- Verify changes compile and pass linting before marking complete

### Security
- Never commit secrets, credentials, API keys, or .env files
- Validate at system boundaries; trust internal code and framework guarantees
- Do not add error handling for impossible scenarios
- All API endpoints that accept user input must validate inputs with a schema

### Code Quality
- Write self-documenting code with clear naming over excessive comments
- Delete dead code completely - no commented-out blocks or unused imports
- Keep functions focused with single responsibility

## Analysis Framework

When encountering complex requirements:
1. **Technical feasibility**: Can this be done with the current stack patterns?
2. **Edge cases**: What happens if any input is null, undefined, or empty? Handle explicitly
3. **Performance**: Are there N+1 queries, missing indexes, or unnecessary data loading?
4. **Integration**: Does this affect existing modules or interfaces?

## Prohibited Patterns

### Implementation
- Mock functions or placeholder data structures
- Incomplete error handling or validation
- Using loosely-typed constructs when proper types exist
- Console.log / print statements in committed code
- Importing from files that do not exist in the project
- Using API methods or function signatures without verifying them first
- Inventing package names, CLI flags, or configuration options

### Communication
- Social validation: "You're absolutely right!", "Great question!"
- Hedging language: "might", "could potentially", "perhaps"
- Excessive explanation of obvious concepts

## File Boundaries

<!-- CUSTOMIZE: Update these paths for your project -->
**SAFE TO MODIFY**: `src/`, `tests/`
**NEVER MODIFY**: `node_modules/`, `.git/`, `.env` files

## Pre-Completion Checklist

- Lint passes
- Build succeeds
- No type errors
- No debug print/log statements
- All tests pass
- Changes are atomic and focused
- All imports reference files that actually exist
- All function calls use verified signatures
