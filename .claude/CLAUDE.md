# Project Directives

## Workflow Rules

- Never use mock data, results or workarounds
- Implement complete working code - no stubs, TODOs, or placeholder functions
- Implement tests after every checkpoint; verify all tests pass
- Store project plans and progress in `.claude_plans/` directory
- Write all tests to `tests/` folder
- Do not leave files in the root directory - sort into appropriate folder locations
- Run `pytest -x` after significant changes

## Code Style

- Python naming: snake_case (variables/functions), PascalCase (classes), SCREAMING_SNAKE_CASE (constants)
- Line length: 100 (configured in pyproject.toml for black and ruff)
- Linting: `ruff check src/ tests/` and `black --check src/ tests/`

## Implementation Approach

- Direct implementation only - generate complete, working code
- When encountering complex requirements, analyze: technical feasibility, edge cases, performance implications, integration points
- Prefer editing existing files over creating new ones
- When modifying a symbol, ensure backward compatibility or update all references
