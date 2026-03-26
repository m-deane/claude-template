# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

<!-- CUSTOMIZE: Replace with your project name, description, and tech stack -->
**Project Name** - Brief description of what this project does.

**Stack**: [e.g., Python + FastAPI + PostgreSQL, or Next.js + TypeScript, etc.]

## Development Commands

<!-- CUSTOMIZE: Replace with your project's actual commands -->
```bash
# Common commands (adjust for your stack)
# npm run dev / python manage.py runserver / go run .    # Start dev server
# npm run build / python -m build                        # Build
# npm run lint / ruff check . / golangci-lint run        # Lint
# npm run test / pytest / go test ./...                  # Test
```

## Architecture

<!-- CUSTOMIZE: Describe your project's data flow and structure -->
### Key Directories
- `src/` - Source code
- `tests/` - Test files
- `docs/` - Documentation

## Project Conventions

- Planning documents go in `.claude_plans/`
- Tests go in `tests/`
- No mocks/stubs/TODOs - implement complete working code
- Run lint and build commands to verify changes
- See `.claude/rules/` for detailed guidelines by concern
