# v4 Build Summary

## Use Case Review Scores (Agent 1)

| Goal | Score | Key Finding |
|------|-------|-------------|
| Goal 1: Upskill | 7/10 | Tool map, access paths, and compliance rules are clear and actionable. Prompting technique present but thin on worked examples. Dataiku IDE integration not explicitly explained. |
| Goal 2: Inspire | 6/10 | Three genuine wow moments (Slide 19 Cursor demo, Slide 33 Claude Code audit, Slide 2 15-hrs stat). Demo slides mostly effective but big numbers not visually dominant enough. Meeting summary demo too generic. |
| Goal 3: Warn About Pace | 4/10 | Most significant weakness. Statement slides (44–46) have the right instincts but are abstract. No dedicated acceleration slide. No cost-of-not-engaging slide. Capability timeline framed as informational not alarming. |

## Enhancements Applied

### P0 — Must Fix (3 applied)

| # | Enhancement | Target | Description |
|---|-------------|--------|-------------|
| 1 | The Acceleration Curve | New Slide 4 (s1_s3_v4) | New slide with 4 before/after capability jumps + 4 forward predictions for 12 months. Core "the gradient is steepening" message. |
| 2 | The Cost of Not Engaging | New Slide 5 (s1_s3_v4) | New slide with "6 months" big number, quantified output velocity gap, and FM&I-specific framing of adoption lag consequences. |
| 3 | Capability Timeline Reframing | Slide 9 v4 (was Slide 7) | Title changed to "Five capability jumps — not equal-sized steps", framing text added, all milestone descriptions rewritten to communicate acceleration not just change, bottom bar rewritten as challenge not summary. |

### P1 — Should Fix (5 applied)

| # | Enhancement | Target | Description |
|---|-------------|--------|-------------|
| 4 | Cursor Demo Visual Priority | Slide 21 v4 (was Slide 19) | "12 min" enlarged to 48pt (from 36pt), "2–3 days" added as 22pt red secondary stat with "That is not a typo." note. Big number now visual centrepiece. |
| 5 | Copilot Demo FM&I Prompt | Slide 15 v4 (was Slide 13) | Prompt replaced with FM&I-specific language: crack spread ELT pipeline, model calibration decisions, VaR scenario parameters. Output steps use real FM&I domain terms. |
| 6 | Stat Cascade Right Card | Slide 3 v4 | "3×" secondary big number (36pt, C.orange) added to right card above the explanatory text. Source line added. Body text tightened. |
| 7 | Statement Slides Proof Points | Slides 46–48 v4 (was 44–46) | All three statement slides updated with specific quantified evidence: 15hrs/2hrs gap, Goldman Sachs 30% code review reduction, 85–95% AI accuracy (5–15% error rate), "hired right now" framing. |
| 8 | Title Slide Urgency Line | Slide 1 v4 | Added urgency sub-line in C.orange italic: "In 12 months, the analysts using these tools daily will be 40–80 hours ahead of those who aren't. This session is about making sure that isn't you." |

## New Slides Added

- **Slide 4** (s1_s3_v4): "The capability is accelerating — this is not a steady improvement curve" — 4 before/after rows + forward predictions panel
- **Slide 5** (s1_s3_v4): "What does it look like if we don't engage — the honest answer" — big number panel (6 months) + FM&I consequence statement

## Slide Count

| Version | Slides |
|---------|--------|
| v3 | 47 |
| v4 | 49 (+2 new slides) |

## File Size

`gen_ai_fmi_presentation_v4.pptx` — **938 KB**

## Files Produced

```
presentations/gen_ai_fmi/
├── use_case_review.md          — Agent 1 review with scores and priorities
├── v4_enhancements.md          — Agent 2 exact content for all enhancements
├── slides_s1_s3_v4.cjs         — Sections 1–3 (17 slides, 2 new, 5 modified)
├── slides_s4_s6_v4.cjs         — Sections 4–6 (unchanged structure, 1 panel modified)
├── slides_s7_s10_v4.cjs        — Sections 7–10 (unchanged structure, 3 body texts modified)
├── generate_pptx_v4.cjs        — Generator script
├── gen_ai_fmi_presentation_v4.pptx  — 938 KB, 49 slides
└── v4_summary.md               — This file
```
