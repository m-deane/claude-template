# Project Instructions

## Project Purpose

A template for creating professional presentations from a brief.
Primary outputs: speaker transcript, reveal.js HTML/PDF, Microsoft PowerPoint (pptxgenjs).
Primary artifact: `.claude_prompts/presentation-creator-prompt.md` — a 4-agent pipeline.

## Repository Structure

```
.claude_prompts/
  presentation-creator-prompt.md  # Main 4-agent presentation system (PRIMARY ARTIFACT)
  claude.md                        # Standard implementation workflow
  iterative-testing-prompt.md      # Iterative browser-based testing workflow
  personal-org-app-prompt.md       # Personal org app build prompt

.claude/
  CLAUDE.md                        # Behavioral directives (Claude Code)
  settings.json                    # Permission allow/deny rules (Claude Code)
  rules/                           # Modular, path-scoped instruction files (Claude Code)
  agents/                          # Specialized sub-agent definitions (Claude Code)
  commands/                        # Slash command definitions (Claude Code)
  skills/                          # MCP skill definitions (Claude Code)

.cursor/
  rules/                           # Cursor rules (.mdc files with frontmatter)
  commands/                        # Cursor slash commands

.github/
  copilot-instructions.md          # GitHub Copilot global instructions (this file)
  agents/                          # Copilot Chat agents (.agent.md)
  instructions/                    # Path-scoped instructions (.instructions.md)
  prompts/                         # Reusable prompt files (.prompt.md)

.claude_plans/                     # Planning and research documents
.claude_research/                  # Background research
review/                            # Evaluation outputs
examples/                          # Slide template library, CSS patterns, design system reference
docs/                              # API reference
presentations/<topic>/             # Generated presentations (one directory per presentation)
```

## The 4-Agent Pipeline

| Agent | Role | Output |
|---|---|---|
| Agent 1: Research & Content Strategist | SCR narrative arc, Minto Pyramid, audience analysis | Content outline |
| Agent 2: Slide Architect & Designer | 18 slide types, design system, CSS tokens | Slide design spec |
| Agent 3: Script Writer | Speaker notes, 130 wpm timing, transitions | Complete script |
| Agent 4: Production Engineer | reveal.js HTML, PDF instructions, pptxgenjs PPTX | Final deliverables |

## Invocation

```yaml
topic: "Why Teams Should Adopt AI Coding Assistants"
audience: "Engineering leadership (CTOs, VPs of Engineering)"
purpose: "Get buy-in to roll out AI coding tools company-wide"
duration: "10 minutes"
tone: "Professional but direct"
output_formats: ["html", "pptx"]
brand_colors: ["#0f172a", "#3b82f6", "#f8fafc"]
```

## Key Technical Gotchas

- pptxgenjs scripts must use `.cjs` extension (repo has `"type":"module"`)
- pptxgenjs hex colors: no `#` prefix — `"2563EB"` not `"#2563EB"`
- Reveal.js: self-contained HTML with CDN links only, no local dependencies
- Full pptxgenjs rules in `.github/instructions/pptxgenjs.instructions.md`
- Full reveal.js rules in `.github/instructions/revealjs.instructions.md`

## Behavioral Directives

### Production Rules

- Direct production output only — complete, working deliverables on first attempt
- No stub slides — never produce a slide with only a title and empty body
- Never write "See speaker notes for full content" as slide body text
- Every slide must have speaker notes (full sentences, not bullet points)
- Every pptxgenjs script must run without errors on first attempt

### Quality Gates

- pptxgenjs script runs: `node generate_pptx.cjs` exits 0
- HTML opens in Chrome without console errors; `S` key opens speaker notes
- Slide count within +/-2 of duration target (8 slides per 10 min)
- 100% of slides have speaker notes
- Narrative arc reviewable in slide titles alone

### Prohibited Patterns

- Social validation ("Great question!"), hedging language ("might", "could potentially")
- See `.github/instructions/pptxgenjs.instructions.md` for full technical prohibitions
- See `.github/instructions/presentation.instructions.md` for content standards

## Workflow Rules

- Plans go in `.claude_plans/`
- Research goes in `.claude_research/`
- Evaluations go in `review/`
- Prompts go in `.claude_prompts/`
- Generated presentations go in `presentations/<topic>/`
- New presentation scripts: always use `.cjs` extension
