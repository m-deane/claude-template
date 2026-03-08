# CLAUDE.md

This file provides guidance to Claude Code when working in this repository.

## Project Overview

**Presentation Creator** — A Claude Code template and multi-agent prompt system that produces professional presentations (HTML/reveal.js, PDF, PPTX) from a topic + parameters input.

**What this repo is**: A reusable Claude Code project template, pre-configured with agents, slash commands, skills, and workflow prompts. The primary deliverable is the Presentation Creator agent team prompt.

## Repository Structure

```
.claude_prompts/
  presentation-creator-prompt.md  # Main 4-agent presentation system (PRIMARY ARTIFACT)
  claude.md                        # Standard implementation workflow
  iterative-testing-prompt.md      # Iterative browser-based testing workflow
  personal-org-app-prompt.md       # Personal org app build prompt

.claude/
  CLAUDE.md                        # Behavioral directives
  TEMPLATE_GUIDE.md                # How to use this template for new projects
  agents/                          # Specialized sub-agent definitions
  commands/                        # Slash command definitions
  skills/                          # MCP skill definitions
  example_prompt.md                # Prompt template starting point

.claude_plans/                     # Planning and research documents
.claude_research/                  # Background research
review/                            # Evaluation outputs (use case analysis, audit, test HTML files, verdict)
docs/                              # API reference
```

## Presentation Creator System

The core system is `.claude_prompts/presentation-creator-prompt.md` — a 4-agent pipeline:

| Agent | Role | Output |
|---|---|---|
| Agent 1: Research & Content Strategist | SCR narrative arc, Minto Pyramid, audience analysis | Content outline |
| Agent 2: Slide Architect & Designer | 12 slide type templates, design system, CSS tokens | Slide design spec |
| Agent 3: Script Writer | Speaker notes, timing (130 wpm model), transitions | Complete script |
| Agent 4: Production Engineer | reveal.js HTML, PDF instructions, PPTX spec | Final deliverables |

**Invocation example**:
```yaml
topic: "Why Teams Should Adopt AI Coding Assistants"
audience: "Engineering leadership (CTOs, VPs of Engineering)"
purpose: "Get buy-in to roll out AI coding tools company-wide"
duration: "10 minutes"
tone: "Professional but direct"
output_formats: ["html"]
brand_colors: ["#0f172a", "#3b82f6", "#f8fafc"]
```

## Evaluation Results

The system has been formally evaluated. Key findings in `review/`:

- **Fulfillment score**: 74/100 (estimated 88–92/100 post-fixes)
- `review/use_case_analysis.md` — 5 canonical use cases + success criteria
- `review/implementation_audit.md` — 10-dimension scored audit
- `review/test_output_1.html` / `test_output_2.html` — Live generated presentations
- `review/test_results.md` — Scored test results
- `review/final_verdict.md` — Full verdict, improvement backlog, success criteria baseline

**Production-quality pass thresholds** (from `review/final_verdict.md`):
- Slide count within ±2 of duration target
- 100% of slides have speaker notes
- 0 slides with >50 words of body text
- HTML opens without errors in Chrome, `S` key opens speaker notes
- Narrative arc traceable: hook → 3 MECE pillars → specific CTA
- Timing estimate accurate within ±15% (measured at 130 words/minute)

## Workflow Rules

- Planning documents go in `.claude_plans/`
- Research documents go in `.claude_research/`
- Evaluation outputs go in `review/`
- New prompt variants go in `.claude_prompts/`
- No TODOs or placeholder implementations in prompt files
