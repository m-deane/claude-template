# Behavioral Directives — Project Control Library

## Implementation Philosophy
- This library controls other projects — never modify managed project files without explicit skill invocation
- Use Opus 4.6 for all planning, architecture, and review tasks
- Use Sonnet 4.6 for all implementation and code generation tasks
- Use Haiku 4.5 for quick lookups, status checks, and simple queries
- Direct implementation only — complete, working code on first attempt
- No partial implementations, mocks, stubs, TODOs, or placeholder functions

## Analysis Framework
When encountering requests:
1. **Scope check**: Does this affect one project or many? Use batch commands for multi-project ops
2. **Port safety**: Will this launch anything? Check port registry first, never kill other processes
3. **Token budget**: Is this within budget? Use the cheapest model that can handle the task
4. **Documentation sync**: Will this change implementation? Queue doc updates for finalise-session

## Prohibited Patterns
- Killing processes on ports owned by other projects
- Modifying managed project files outside of skill/command invocation
- Using Opus for simple implementation tasks (use Sonnet)
- Using Sonnet for complex planning tasks (use Opus)
- Leaving orphaned files in any project root directory
- Committing without running the project's own lint/build/test suite
- Launching services on hardcoded ports without checking availability
- Social validation ("Great question!"), hedging language ("might", "could potentially")
- `console.log` or `print()` left in production code

## Post-Task Protocol (MANDATORY)
After every agent team completes work on any project:
1. Run the project's test suite — do not proceed if tests fail
2. Update the project's CLAUDE.md if implementation changed
3. Update the project's documentation
4. Update to-do lists and status tracking
5. Commit changes with descriptive message
6. Report token usage for the completed task

## Quality Gates
- All managed projects pass their own quality checks
- CLAUDE.md files are in sync with implementation
- No orphaned files in project roots
- Plans consolidated with timestamps
- Git working trees clean after session
- Port registry accurate
- Token usage within budget

# currentDate
Today's date is 2026-03-03.
