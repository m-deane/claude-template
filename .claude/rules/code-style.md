---
description: Code style and naming conventions
---

# Code Style Standards

## TypeScript Conventions
- Variables/functions: camelCase
- Types/interfaces/classes: PascalCase
- Constants: SCREAMING_SNAKE_CASE
- Files: kebab-case.ts or camelCase.ts

## Import Conventions
- Use `@/` path alias for imports from `src/`
- Group imports: external packages, then internal modules, then relative paths
- No unused imports

## Error Handling
- Handle loading, error, empty, and success states in UI components
- Use proper error boundaries for React components
- Provide user-friendly error messages

## Prohibited Patterns
- Using `any` type when proper types exist
- Mock functions or placeholder data structures
- Incomplete error handling or validation
- Console.log statements in committed code
