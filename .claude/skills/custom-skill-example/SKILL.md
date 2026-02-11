# Custom Skill Template

This is an example skill demonstrating how to create reusable, domain-specific workflows as Claude Code skills. Replace this with your own skill logic.

## What Are Skills?

Skills are reusable prompts stored as markdown files, triggered by a `/command`. They encode domain knowledge, preferences, and multi-step workflows so you don't have to repeat yourself across sessions.

## When to Create a Skill

Create a skill when you have:
- A workflow you repeat across multiple sessions (e.g., meal planning, app launch, data pipeline)
- Domain-specific preferences that should be consistent (e.g., dietary requirements, coding standards)
- Multi-step processes that benefit from a fixed sequence (e.g., deploy, review, generate)

## Skill Structure

```
.claude/skills/
└── your-skill-name/
    ├── SKILL.md          # Main skill definition (this file)
    ├── reference/        # Optional: reference docs, examples
    └── scripts/          # Optional: helper scripts
```

## Example: Meal Plan Skill

Below is an example of a domain-specific skill for meal planning. Replace this with your own workflow.

### Workflow Steps

1. Read recipes from the recipe database or source
2. Filter for high-protein options (>30g per serving)
3. Prioritize preferred proteins (customize per user)
4. Generate a 7-day plan with no recipe repeats
5. Output cooking instructions and consolidated shopping list
6. Ask user for swap requests before finalizing

### Customization Points

Replace these with your domain-specific parameters:
- **Data source**: Where to read input data from
- **Filter criteria**: What constraints to apply
- **Output format**: How to present results
- **User interaction**: When to pause for user input

## Example: App Launch Skill

Another common pattern — encoding a project startup sequence:

### Workflow Steps

1. Check all dependencies are installed
2. Start backend services (database, cache, API server)
3. Start frontend development server
4. Open browser to the correct URL
5. Run a quick smoke test to verify everything is up
6. Report status of all services

## Creating Your Own Skill

1. Create a new directory under `.claude/skills/`
2. Add a `SKILL.md` with your workflow steps
3. Optionally add `reference/` docs and `scripts/` helpers
4. Invoke with `/your-skill-name`

### Tips

- Keep skills focused on one workflow — don't combine unrelated tasks
- Include explicit decision points where the user should confirm before proceeding
- Reference specific file paths and commands rather than generic instructions
- Include error handling steps (what to do if a step fails)
