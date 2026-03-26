---
description: Code style and naming conventions
---

# Code Style Standards

<!-- CUSTOMIZE: Adjust naming conventions for your language -->
## Naming Conventions
- Variables/functions: camelCase (JS/TS) or snake_case (Python/Go)
- Types/interfaces/classes: PascalCase
- Constants: SCREAMING_SNAKE_CASE
- Files: kebab-case or snake_case (match your project's existing pattern)

## Import Conventions
- Group imports: external packages, then internal modules, then relative paths
- No unused imports
- Use path aliases if configured in your project

## Error Handling
- Handle loading, error, empty, and success states in UI components
- Provide user-friendly error messages
- Handle null, undefined, and empty inputs explicitly in business logic

## Prohibited Patterns
- Using loosely-typed constructs when proper types exist
- Mock functions or placeholder data structures
- Incomplete error handling or validation
- Debug print/log statements in committed code
