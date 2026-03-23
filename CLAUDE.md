# CLAUDE.md — Presentation Creator Template

## Project Purpose

A Claude Code template for creating professional presentations from a brief.
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
  CLAUDE.md                        # Behavioral directives
  settings.json                    # Permission allow/deny rules
  rules/                           # Modular, path-scoped instruction files
  agents/                          # Specialized sub-agent definitions
  commands/                        # Slash command definitions
  skills/                          # MCP skill definitions

.claude_plans/                     # Planning and research documents
.claude_research/                  # Background research
review/                            # Evaluation outputs (use case analysis, audit, test HTML files, verdict)
examples/                          # Slide template library, showcases, CSS patterns, design system reference
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
- Full technical rules in `.claude/rules/pptxgenjs-rules.md` and `.claude/rules/revealjs-rules.md`

## Workflow Rules

- Plans → `.claude_plans/`
- Research → `.claude_research/`
- Evaluations → `review/`
- Prompts → `.claude_prompts/`
- Generated presentations → `presentations/<topic>/`
- New presentation scripts: always `.cjs` extension
