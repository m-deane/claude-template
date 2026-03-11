---
applyTo: "presentations/**"
description: "Presentation pipeline rules — 4-agent workflow and quality standards"
---

# Presentation Pipeline

## The 4-Agent Pipeline

| Agent | Role | Output |
|---|---|---|
| Agent 1: Research & Content Strategist | SCR narrative arc, Minto Pyramid, audience analysis | Content outline |
| Agent 2: Slide Architect & Designer | 18 slide types, design system, CSS tokens | Slide design spec |
| Agent 3: Script Writer | Speaker notes, 130 wpm timing, transitions | Complete script |
| Agent 4: Production Engineer | reveal.js HTML, PDF instructions, pptxgenjs PPTX | Final deliverables |

### Agent 1: Research & Content Strategist

- Build the narrative arc using the SCR (Situation, Complication, Resolution) framework
- Apply the Minto Pyramid principle for logical argument structure
- Perform audience analysis to tailor content depth and terminology
- Output: structured content outline with key assertions per slide

### Agent 2: Slide Architect & Designer

- Select from 18 available slide types for visual variety
- Apply the design system (color constants, typography, layout grid)
- Define CSS tokens and visual hierarchy for each slide
- Output: complete slide design specification

### Agent 3: Script Writer

- Write full speaker notes in complete sentences (not bullet points)
- Target 130 words per minute pacing
- Include transition cues between slides
- Verify total timing matches the target duration (+/-15%)
- Output: complete speaker script

### Agent 4: Production Engineer

- Generate self-contained reveal.js HTML with CDN links
- Generate pptxgenjs `.cjs` script for PowerPoint output
- Provide PDF generation instructions (print-to-PDF via Chrome)
- Output: final deliverable files

## Invocation Format

```yaml
topic: "Why Teams Should Adopt AI Coding Assistants"
audience: "Engineering leadership (CTOs, VPs of Engineering)"
purpose: "Get buy-in to roll out AI coding tools company-wide"
duration: "10 minutes"
tone: "Professional but direct"
output_formats: ["html", "pptx"]
brand_colors: ["#0f172a", "#3b82f6", "#f8fafc"]
```

## Content Standards

- Max 40 words visible on any slide body
- One key assertion per slide — not a list of facts
- Narrative arc must be traceable: hook → 3 MECE pillars → specific CTA
- Speaker notes: 130 words per minute model — verify timing before finalizing
- Demo slides: the big number (time saved, ROI, improvement) must be the visual centerpiece

## Evaluation Pass Thresholds

- Slide count within +/-2 of duration target (1 slide per 1.5-2 min)
- 100% of slides have speaker notes in `<aside class="notes">` tags
- 0 slides with >50 words of visible body text
- HTML opens in Chrome without console errors; `S` key opens speaker notes
- Narrative arc traceable: hook → 3 MECE pillars → specific CTA
- Timing estimate within +/-15% of target (measured at 130 words/minute)

## Quality Gates

- pptxgenjs script runs: `node generate_pptx.cjs` exits 0
- HTML opens in Chrome without console errors
- Slide count within +/-2 of duration target (8 slides per 10 min)
- 100% of slides have speaker notes
- Narrative arc reviewable in slide titles alone
- No stub slides (title only, empty body)
- No "See speaker notes for full content" as slide body text
