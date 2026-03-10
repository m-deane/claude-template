# Behavioural Directives

## Presentation Production Rules

- Direct production output only — complete, working deliverables on first attempt
- No stub slides — never produce a slide with only a title and empty body
- Never write "See speaker notes for full content" as slide body text
- Every slide must have speaker notes (full sentences, not bullet points)
- Every pptxgenjs script must run without errors on first attempt

## Content Standards

- Max 40 words visible on any slide body
- One key assertion per slide — not a list of facts
- Narrative arc must be traceable: hook → 3 MECE pillars → specific CTA
- Speaker notes: 130 words per minute model — verify timing before finalising
- Demo slides: the big number (time saved, ROI, improvement) must be the visual centrepiece, not a supporting element

## pptxgenjs Technical Rules

Reference: see root `CLAUDE.md` for the complete list.

Quick reference — check before writing any code:

- `.cjs` extension ✓
- No `#` on hex colors ✓
- No `shadow` ✓
- No `bullet: true` ✓
- Fresh option objects per call ✓
- `pres.ShapeType.rect` ✓
- `LAYOUT_16x9` ✓

## Quality Gates

Before delivering any output:

- pptxgenjs script runs: `node generate_pptx.cjs` exits 0
- HTML opens in Chrome without console errors; `S` key opens speaker notes
- Slide count within ±2 of duration target (8 slides per 10 min)
- 100% of slides have speaker notes
- Narrative arc reviewable in slide titles alone

## Prohibited Patterns

- `console.log` left in production scripts
- Slides with >50 words of body text
- Grids with more than 4 cards
- Cards with fewer than 30 words of body content
- `bullet: true` in any pptxgenjs call
- `shadow` in any pptxgenjs call
- `#` prefix on any hex color value
- Reused option objects across `addShape`/`addText` calls
- Social validation ("Great question!"), hedging language ("might", "could potentially")
