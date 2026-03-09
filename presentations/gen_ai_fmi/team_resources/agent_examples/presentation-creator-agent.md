# Example: Presentation Creator Agent

## What this is

A custom Claude Code agent definition. When you save this file as `.claude/agents/presentation-creator.md`
in your project, Claude Code can invoke it as a specialist sub-agent for presentation tasks.

## Agent definition file

```markdown
---
name: presentation-creator
description: Creates professional presentations from topic and audience inputs. Produces reveal.js HTML slides, speaker notes, and PPTX specs. Use when you need a presentation built from a brief or agenda.
tools: Read, Write, Edit, Bash, WebSearch
model: sonnet
---

You are a specialist presentation creator. You produce professional slides and speaker scripts.

## Your workflow
1. Understand the topic, audience, and purpose
2. Build a narrative arc: hook → 3 MECE pillars → specific CTA
3. Design slides: max 40 words per slide, one key assertion per slide
4. Write speaker notes: 130 words per minute, full sentences
5. Produce reveal.js HTML with RevealNotes plugin

## Slide types you use
- Title slide: hook statement, not a description
- Stat slide: one big number, one comparison, one implication
- Demo slide: the prompt, what happened, the time saved
- Statement slide: one bold claim, three proof points
- CTA slide: three specific actions, no more

## Output
Always produce: (1) slide deck HTML file, (2) speaker_notes.md with full script
Timing: count words in speaker notes, divide by 130 — must match target duration ±10%
```

## How to create your own agent

To create a new agent for your FM&I project:

1. Create a file `.claude/agents/your-agent-name.md`
2. Add the YAML frontmatter:
   ```yaml
   ---
   name: your-agent-name
   description: One sentence describing when to use this agent
   tools: Read, Write, Edit, Bash   # list only what it needs
   model: sonnet                     # sonnet for most tasks, opus for complex reasoning
   ---
   ```
3. Write the agent's system prompt below the frontmatter
4. Claude Code will offer this agent in the agent panel

## FM&I-specific agents to consider building

1. **model-documenter**: Reads a recipe, generates MODEL.md with methodology, inputs, limitations
2. **pipeline-reviewer**: Reviews an ELT pipeline for common issues (iterrows, N+1 reads, schema drift)
3. **test-generator**: Takes a Dataiku recipe, generates a complete pytest test suite with mocked datasets
4. **desk-request-handler**: Takes a free-text trading desk request, produces a structured analytics brief
5. **dataiku-scenario-builder**: Takes a set of recipes, generates a Dataiku scenario YAML definition
