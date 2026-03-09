# Agent vs Skill: What's the difference?

## Agent

An agent is a **sub-agent Claude Code spawns** to handle a specialist task autonomously.
- Has its own tool access, system prompt, and model
- Claude Code decides when to invoke it based on the description
- Can read files, write files, run commands
- Best for: multi-step tasks that need their own context window

## Skill (slash command)

A skill is a **prompt template you invoke with a slash command**.
- You type `/skill-name` in the chat
- Claude expands it into a detailed prompt and executes it
- Best for: repeatable workflows you want consistent behaviour on

## Skill example: /model-doc

Save to `.claude/commands/model-doc.md`:

```markdown
---
Create comprehensive MODEL.md documentation for the specified Dataiku recipe.

## Steps to follow:

1. Read the recipe file specified by the user (or the most recently modified .py file in /recipes/)
2. Extract: (a) all input datasets, (b) all output datasets, (c) all transformation logic, (d) any model parameters or config references
3. Identify the commercial purpose from the recipe name and variable names
4. Generate a MODEL.md with these sections:
   - **Purpose**: what commercial question this model answers
   - **Data inputs**: each dataset, what columns it uses, assumed frequency
   - **Methodology**: the transformation logic in plain English + key equations in LaTeX where relevant
   - **Known limitations**: edge cases, assumptions, sensitivity to input quality
   - **Calibration parameters**: list all parameters read from config (do NOT include their values)
   - **Last updated**: today's date
   - **Next review**: 6 months from today

5. Save the file as MODEL.md in the project root
6. Print a one-line summary of what was documented

## Usage
/model-doc compute_crack_spread.py
/model-doc  (no argument = reads most recently modified recipe)
---
```

## How to create your own skill

1. Create `.claude/commands/your-skill-name.md`
2. Write a detailed prompt describing exactly what Claude should do step by step
3. Invoke it in Claude Code by typing `/your-skill-name`

## Recommended FM&I skills to build

- `/model-doc [recipe]` — generate MODEL.md from recipe code (shown above)
- `/recipe-review [recipe]` — run the pipeline reviewer checklist
- `/desk-brief [request]` — convert a free-text desk request to a structured analytics brief
- `/scenario-check` — verify all recipes in a Dataiku scenario are production-ready
- `/test-recipe [recipe]` — generate pytest test suite for a recipe
