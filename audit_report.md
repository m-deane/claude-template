# Repository Audit Report
*Agent 1 — Presentation Creator Template Assessment*
*Date: 2026-03-10*

---

## Section 1: Files to Delete (leftover web app artifacts)

These files and directories are remnants of the Digital Filofax Next.js/Prisma/tRPC web app. They have no bearing on the presentation creator use case and will confuse any new user or agent operating in this repo.

### Directories — delete entirely

| Path | Reason |
|---|---|
| `src/` | Complete Next.js app source tree (app router, components, hooks, lib, server/tRPC routers, types). Zero relevance to presentation creation. |
| `prisma/` | Prisma schema for the personal org app database. No database is needed for presentation generation. |
| `tests/` | Vitest test suite for the web app (e2e pages test, tRPC router tests, import tests). The quality gate referenced in `.claude/CLAUDE.md` ("npm test passes (320 tests)") refers to this test suite. |
| `node_modules/` | Built artifact of the web app's package.json. Should not be committed; not relevant post-cleanup. |
| `.next/` | Next.js build cache. Build artifact, not source. |
| `public/` | Contains a `presentations/` subdirectory (empty except for the directory itself). Appears to be Next.js public assets folder — empty and irrelevant. |
| `.vscode/` | Editor config from the web app project. Not template infrastructure. |

### Root-level screenshot PNG files — delete all

These are UI screenshots of the Digital Filofax app, committed directly to the root. They total several MB and have no presentation-creator relevance.

| File | Reason |
|---|---|
| `contacts.png` | Filofax app screenshot |
| `daily-planner.png` | Filofax app screenshot |
| `dashboard-full.png` | Filofax app screenshot |
| `finance.png` | Filofax app screenshot |
| `goals.png` | Filofax app screenshot |
| `habits.png` | Filofax app screenshot |
| `ideas.png` | Filofax app screenshot |
| `memos.png` | Filofax app screenshot |
| `mobile-daily.png` | Filofax app screenshot |
| `mobile-dashboard.png` | Filofax app screenshot |
| `mobile-tasks.png` | Filofax app screenshot |
| `mobile-test-375.png` | Filofax app screenshot |
| `monthly-planner.png` | Filofax app screenshot |
| `monthly-tasks.png` | Filofax app screenshot |
| `phase2-sidebar-desktop.png` | Filofax app screenshot |
| `quick-capture-dialog.png` | Filofax app screenshot |
| `reflect.png` | Filofax app screenshot |
| `review.png` | Filofax app screenshot |
| `roles.png` | Filofax app screenshot |
| `settings-modules.png` | Filofax app screenshot |
| `settings.png` | Filofax app screenshot |
| `someday.png` | Filofax app screenshot |
| `tasks.png` | Filofax app screenshot |
| `templates.png` | Filofax app screenshot |
| `vision.png` | Filofax app screenshot |
| `weekly-planner.png` | Filofax app screenshot |

### Root-level config files — delete

| File | Reason |
|---|---|
| `eslint.config.mjs` | ESLint config for Next.js/TypeScript web app |
| `next.config.ts` | Next.js configuration |
| `postcss.config.js` | PostCSS/Tailwind config for web app |
| `tailwind.config.ts` | Tailwind CSS config for web app |
| `tsconfig.json` | TypeScript config for the web app |
| `vitest.config.ts` | Vitest test runner config |
| `package.json` | Web app package manifest (Next.js, tRPC, Prisma, Radix UI, etc.). Contains `pptxgenjs` as a dependency, but in the context of a full Next.js app — the template does not need this entire manifest. |
| `package-lock.json` | Lock file for the web app dependencies |
| `TODO.md` | Empty file — leftover placeholder from the web app project |
| `.env.example` | Environment variable template for Next.js/Supabase/NextAuth — not applicable to a presentation generator |

### .claude_plans/ — delete all files (keep directory with .gitkeep)

The `.claude_plans/` directory contains 43 planning documents for the Digital Filofax web app. None are relevant to the presentation creator template. Files include: `ai-suggestions-implementation.md`, `analytics-dashboard-implementation.md`, `bulk-operations-architecture.md`, `filofax-roadmap.md`, `competitive-audit.md`, `obsidian-bidirectional-sync-plan.md`, and 37 others of the same type.

The three files that ARE relevant and should be retained: `presentation-design-spec.md`, `presentation-research.md`, `presentation-scripts.md` — these are the Phase 2 design spec and research artifacts from the gen_ai_fmi presentation build. These should be moved (see Section 2).

### docs/ — evaluate and partially delete

| File | Keep/Delete | Reason |
|---|---|---|
| `docs/API-REFERENCE.md` | Delete | API reference for the Filofax web app (tRPC router API documentation) |
| `docs/RECOMMENDATION.md` | Delete | Technology stack recommendations for the web app |
| `docs/personal-organization-app-platform-research.json` | Delete | Market research for the personal org app, not presentations |
| `docs/presentation-design-research.md` | Move to `examples/research/` | Relevant presentation design research — keep but relocate |

### .claude_research/ — partially delete

| File | Keep/Delete | Reason |
|---|---|---|
| `.claude_research/RECOMMENDATION.md` | Delete | Tech stack recommendation for the web app |
| `.claude_research/personal-organization-app-platform-research.json` | Delete | Personal org app market research |
| `.claude_research/presentation-design-research.md` | Keep | Relevant background research on presentation design |

### Other root-level files — delete or evaluate

| File | Action | Reason |
|---|---|---|
| `README.md` | Rewrite (see Section 3) | Current README describes the Digital Filofax app |
| `gen_ai_presentation_plan.md` | Move to `presentations/gen_ai_fmi/` | Planning doc for the FMI presentation, out of place at root |
| `GenAI_FMI_Presentation.pdf` | Move to `presentations/gen_ai_fmi/` | PDF export of the example presentation, misplaced at root |

---

## Section 2: Files to Move (wrong location)

| Source | Destination | Reason |
|---|---|---|
| `/gen_ai_presentation_plan.md` (root) | `presentations/gen_ai_fmi/gen_ai_presentation_plan.md` | Planning doc for the FMI deck; belongs with its presentation |
| `/GenAI_FMI_Presentation.pdf` (root) | `presentations/gen_ai_fmi/gen_ai_fmi_presentation.pdf` | PDF export of the FMI deck; belongs with the source files |
| `.claude_plans/presentation-design-spec.md` | `presentations/gen_ai_fmi/` or `review/` | Agent 2 output from the FMI build; should be co-located with the presentation or with review artifacts |
| `.claude_plans/presentation-research.md` | `presentations/gen_ai_fmi/` | Agent 1 research output from the FMI build |
| `.claude_plans/presentation-scripts.md` | `presentations/gen_ai_fmi/` | Agent 3 script output from the FMI build |
| `docs/presentation-design-research.md` | `examples/research/` or `.claude_research/` | Relevant reference material; the `docs/` directory is being deleted |

---

## Section 3: Files to Update (gap description + priority)

### P0: `.claude/CLAUDE.md` — Completely wrong content
**Priority**: P0 — This file is read by Claude Code on every session. Its current content actively misleads any agent working in this repo.

**What's wrong**: The entire file is web-app behavioral directives for a tRPC/Prisma/Next.js application:
- "Use tRPC + React Query for all server state management"
- "All tRPC errors use `TRPCError` from `@trpc/server`"
- Prohibited patterns: "Queries without user scoping (`userId: ctx.session.user.id`)"
- Quality gates: "`npm run lint` passes with 0 errors", "`npm run build` succeeds (38/38 pages)", "`npm test` passes (320 tests)`"
- Analysis framework: "Can this be done with existing tRPC/Prisma/Next.js patterns?"

None of these are applicable to a presentation creator template. An agent reading this file would be confused about the project's nature, might try to scope database queries, and would invoke non-existent test commands.

**What's needed**: Replace the entire file with presentation-creator-specific directives:
- Philosophy: "Generate complete, working presentation files on first attempt"
- pptxgenjs technical rules (the critical ones listed in Section 5)
- Output quality gates (from `review/final_verdict.md`)
- Prohibited patterns relevant to presentation generation (no `#` hex prefix in pptxgenjs, no `shadow`, no `bullet: true`, no reused option objects)
- File placement rules (which outputs go where)

---

### P0: `CLAUDE.md` (root) — Missing pptxgenjs technical rules
**Priority**: P0 — The root CLAUDE.md accurately describes the presentation creator system but omits all technical rules for the most critical and failure-prone output format (PPTX via pptxgenjs).

**What's wrong**: The file documents the 4-agent pipeline, evaluation scores, and workflow rules, but contains no mention of:
- `.cjs` file extension requirement for pptxgenjs scripts
- No `#` prefix on hex color strings (pptxgenjs uses bare hex: `"1B2A4A"` not `"#1B2A4A"`)
- `pres.ShapeType.rect` (not string `"rect"`)
- `pres.layout = "LAYOUT_16x9"` (not `"LAYOUT_WIDE"`)
- Modular section architecture for large decks (separate `slides_s1_s3.cjs`, `slides_s4_s6.cjs` files)
- The `require()` / `module.exports` CommonJS pattern required (not ESM `import`)

The invocation example in the root CLAUDE.md shows `brand_colors: ["#0f172a", "#3b82f6", "#f8fafc"]` with `#` prefix — which is correct for HTML/CSS but would be wrong if an agent naively copies this to a pptxgenjs script.

**What's needed**: Add a "pptxgenjs Technical Rules" section with all seven critical rules (see Section 5 for full list).

---

### P1: `.claude_prompts/presentation-creator-prompt.md` — Agent 4 PPTX spec is a skeleton
**Priority**: P1

**What's wrong**: The Agent 4 PPTX section (lines 246–267) provides:
- A JSON fragment showing a single slide's hypothetical structure (not actual pptxgenjs API syntax)
- The JSON example uses `#`-prefixed hex colors (`"#1a1a2e"`, `"#ffffff"`) — this is WRONG for pptxgenjs. Colors must be bare hex strings
- No `.cjs` extension requirement mentioned
- No `pres.ShapeType.rect` usage
- No `pres.layout = "LAYOUT_16x9"` specification
- No modular architecture guidance for multi-section decks
- No `require("pptxgenjs")` / `module.exports` pattern
- No prohibition on `shadow`, `bullet: true`, or reused option objects

The section says "generate a complete Node.js script using PptxGenJS" but gives no working example of the actual API. An agent following this spec would produce scripts with ESM syntax (`import`) that fail with "require is not defined" errors, or scripts with `#`-prefixed colors that break silently.

**What's needed**: Replace the PPTX skeleton with a working reference implementation showing the correct pptxgenjs patterns, plus an explicit list of prohibited API usages.

---

### P1: `README.md` — Describes wrong project
**Priority**: P1

**What's wrong**: The README describes the Digital Filofax personal organization app. It is entirely incorrect for a presentation creator template.

**What's needed**: A new README that describes the presentation creator system: what it produces, how to invoke it, the 4-agent pipeline, and how to get started (copy the invocation example, paste into Claude Code).

---

### P1: `.claude/agents/` — No presentation-specific agents
**Priority**: P1 — See Section 4 for full detail.

**What's wrong**: The agents directory contains generic development agents: `code-reviewer`, `debugger`, `typescript-pro`, `test-engineer`, `ml-engineer`, `sql-expert`, `python-pro`, `ui-ux-designer`, `prompt-engineer`, `docusaurus-expert`, `command-expert`, `context-manager`, `error-detective`, `task-decomposition-expert`, `technical-researcher`, `unused-code-cleaner`. All are useful for software development projects but none are specialized for presentation generation workflows.

**What's needed**: At minimum, a `pptxgenjs-engineer.md` agent (pptxgenjs API expert, knows all anti-patterns) and a `revealjs-engineer.md` agent (HTML/CSS presentation specialist, knows the reveal.js v5 plugin architecture). See Section 4.

---

### P2: `.claude/TEMPLATE_GUIDE.md` — Partially stale
**Priority**: P2

**What's partially wrong**: The TEMPLATE_GUIDE.md is a generic "how to use this Claude Code template" document. Most of it is useful and language-agnostic. However:
- The "Available Agents" table lists web-app-focused agents and will become stale once agent files are updated
- The slash commands listed include `generate-tests`, `architecture-review`, `generate-api-documentation` — all web-app oriented
- There is no mention of how to invoke the presentation creator prompt

**What's needed**: Update the agents table and add a "Creating Your First Presentation" quick-start section pointing to the invocation example in `presentation-creator-prompt.md`.

---

### P2: `.claude_prompts/examples-library-prompt.md` — Verify relevance
**Priority**: P2

This file exists in `.claude_prompts/` alongside the presentation creator prompt. Based on filename, it may be a prompt for building the examples library. Its content should be reviewed to confirm whether it's still relevant or is a web-app artifact.

---

## Section 4: Files to Create (missing from working template)

### 1. `.claude/agents/pptxgenjs-engineer.md` — CRITICAL MISSING AGENT
**Priority**: P0

The primary output format requested most often (PPTX) has no specialist agent. When Agent 4 (Production Engineer) generates a pptxgenjs script, it should delegate to a pptxgenjs expert agent to enforce the API rules. Without this agent, every PPTX generation run risks hitting the known failure modes.

The agent should encode:
- `.cjs` extension requirement (ESM/CommonJS conflict: `package.json` sets `"type": "module"`, so pptxgenjs scripts MUST use `.cjs` extension or explicit CommonJS syntax)
- Bare hex color strings (no `#` prefix — pptxgenjs parses colors as hex strings, `#` causes silent failure)
- No `shadow` property on shapes (crashes pptxgenjs silently)
- No `bullet: true` on text options (deprecated and unreliable in v4)
- No reused option objects across multiple `addText`/`addShape` calls (pptxgenjs mutates options internally, causing style bleed between elements)
- `pres.ShapeType.rect` (enum reference, not string `"rect"`)
- `pres.layout = "LAYOUT_16x9"` (not `"LAYOUT_WIDE"` which is an older alias that may not be supported)
- Modular architecture: for decks with more than ~15 slides, split into section modules (`slides_s1_s3.cjs`, `slides_s4_s6.cjs`) that export builder functions, combined by a thin orchestrator script
- Color constants object pattern: define all colors as a `const C = { navy: "1B2A4A", ... }` object at the top of the orchestrator and pass it to section modules — never hardcode color strings inline

### 2. `.claude/agents/revealjs-engineer.md` — HIGH PRIORITY MISSING AGENT
**Priority**: P1

An HTML presentation specialist agent that knows:
- reveal.js v5 CDN paths and config keys
- Mandatory plugin loading: `RevealNotes` for speaker notes (the P0 bug in the current prompt)
- `<aside class="notes">` placement and syntax
- `?print-pdf` PDF mode requirements
- CSS custom property scoping for reveal.js slides (`:root` vs `.reveal` vs `.slides`)
- Fragment animation patterns
- Cross-browser rendering quirks for presentation-specific CSS (Flexbox in slide context, `vh`/`vw` units)

### 3. A minimal `package.json` for pptxgenjs scripts — MISSING INFRASTRUCTURE
**Priority**: P0

A new user who clones this template has no way to run pptxgenjs scripts. The existing `package.json` is the full web app manifest. A standalone `package.json` scoped to pptxgenjs generation is needed — either:
- A root-level `package.json` containing only `{ "dependencies": { "pptxgenjs": "^4.0.1" } }` and no `"type": "module"` (so `.cjs` files work via `require()`), OR
- A `presentations/package.json` template that new presentations can copy

The current `package.json` has `"type": "module"` which means any `.js` file will be treated as ESM and `require()` will fail — this is why the working example uses `.cjs` extensions throughout. New users will not understand this constraint without documentation.

### 4. `presentations/TEMPLATE/` — Starter presentation scaffold
**Priority**: P1

A new user has no starting point for their first presentation. The `presentations/gen_ai_fmi/` directory is a useful example but it is a completed, polished project with 40+ files. A stripped-down template showing:
- `generate_pptx.cjs` — minimal working orchestrator
- `slides_section1.cjs` — one-slide section module example
- `presentation.html` — minimal reveal.js skeleton with correct plugin loading
- `content_outline.md` — blank template with the SCR arc structure pre-filled

### 5. Root-level `QUICK_START.md` (or equivalent section in README)
**Priority**: P1

A new user's first question is "how do I make a presentation right now?" The answer is not obvious:
1. Copy the invocation YAML from `presentation-creator-prompt.md`
2. Paste it with the full prompt into a Claude Code session
3. Wait for the 4-agent pipeline to run
4. Take the output `.cjs` files and run `node generate_pptx.cjs`

This flow is not documented anywhere in the current repo. The `TEMPLATE_GUIDE.md` explains how to customize the template but not how to actually use the presentation creator.

### 6. `.claude/agents/content-strategist.md` — Optional but useful
**Priority**: P2

A specialized content strategy agent that knows the Minto Pyramid Principle, SCR arc, MECE testing, and audience profiling. Could be invoked independently when a user wants help structuring content before running the full 4-agent pipeline.

---

## Section 5: pptxgenjs Rule Gaps in presentation-creator-prompt.md

The following table audits Agent 4's PPTX section against the rules demonstrated by the working reference implementation (`presentations/gen_ai_fmi/generate_pptx_v5.cjs` and its section modules).

| Rule | Present in prompt? | Evidence |
|---|---|---|
| Use `.cjs` extension (not `.js`) to avoid ESM conflict | **ABSENT** | The prompt says "generate a complete Node.js script" with no file extension guidance. The working example uses `.cjs` throughout. |
| No `#` prefix on hex color strings | **ABSENT — ACTIVELY WRONG** | The prompt's PptxGenJS example (line 254–257) uses `"#1a1a2e"`, `"#ffffff"`, `"#cccccc"` — all wrong for pptxgenjs. The working example uses bare hex: `"1B2A4A"`, `"FFFFFF"`. |
| No `shadow` property on shapes | **ABSENT** | Not mentioned. The working example contains zero `shadow` properties, consistent with this being a known crash-causing field. |
| No `bullet: true` on text options | **ABSENT** | Not mentioned anywhere in the prompt. |
| No reused option objects across multiple addText/addShape calls | **ABSENT** | Not mentioned. The working example creates fresh inline objects per call. |
| `pres.ShapeType.rect` (not string `"rect"`) | **ABSENT** | The prompt makes no reference to `ShapeType` enum. The working example uses `pres.ShapeType.rect` exclusively. |
| `pres.layout = "LAYOUT_16x9"` (not `"LAYOUT_WIDE"`) | **ABSENT** | The prompt does not specify the layout constant. The working example sets `pres.layout = "LAYOUT_16x9"`. |
| Modular section architecture for large decks | **ABSENT** | The prompt says "generate a complete Node.js script" implying a monolithic file. The working example splits into 3 section modules (slides_s1_s3.cjs, slides_s4_s6.cjs, slides_s7_s10.cjs) plus an orchestrator. Large monolithic pptxgenjs scripts become unwieldy and hit context window limits. |
| Color constants object pattern (`const C = { ... }`) | **ABSENT** | The prompt shows no color management pattern. The working example defines all colors as a `const C` object at the orchestrator level and passes it to section modules — prevents hardcoding and enables global palette changes. |
| CommonJS require/module.exports pattern | **ABSENT** | The prompt provides no `require("pptxgenjs")` example. The working example uses `const PptxGenJS = require("pptxgenjs")` and section files use `module.exports = function buildSectionN(pres, C, h) {...}`. |

**Summary**: 0 of 10 pptxgenjs-specific technical rules are documented in the Agent 4 PPTX section. The existing code example in the prompt actively demonstrates the most common error (hex colors with `#` prefix). This section requires a complete rewrite.

---

## Section 6: Summary Score

**Overall readiness score: 3 / 10**

### Justification

**What works (raising the score from 1)**:
- The primary artifact — `presentation-creator-prompt.md` — is substantively strong for HTML output. The content strategy, design system, and script guidance are well-grounded and produce genuinely good results. The 18 slide type template library in `examples/templates/` is comprehensive and well-built. The `review/` evaluation suite provides an honest, detailed baseline. The working example in `presentations/gen_ai_fmi/` demonstrates a successful end-to-end PPTX generation run, establishing that the approach is sound.

**Why the score is low**:

1. **The two behavioral directive files mislead every agent that operates in this repo.** `.claude/CLAUDE.md` directs agents to use tRPC, Prisma, scope database queries with `userId`, and pass tests that don't exist. A new agent session in this repo would begin with fundamentally wrong assumptions about the project's nature.

2. **The most critical output format (PPTX) is completely unguided.** The Agent 4 PPTX section contains a working example that actively demonstrates the wrong syntax (hex colors with `#` prefix). The 10 pptxgenjs rules that prevent script failures are not documented anywhere in the prompt. A naive execution will produce broken scripts.

3. **No specialist agents exist for the core workflows.** The 16 agents in `.claude/agents/` are for web app development. There is no `pptxgenjs-engineer.md` agent, no `revealjs-engineer.md` agent. The most technically demanding parts of the pipeline (PPTX generation, reveal.js HTML production) have no expert agent to catch errors.

4. **The repo is structurally cluttered.** The root directory contains 26 PNG screenshots, a full Next.js application in `src/`, a Prisma schema, a web app test suite, and 43 planning documents for an unrelated project. A new user cloning this repo would need to understand that almost everything visible is irrelevant noise before they can find the actual template infrastructure.

5. **No runnable starting point for new users.** There is no minimal `package.json` for pptxgenjs, no presentation scaffold, and no documented path from "clone the repo" to "run my first presentation." The gap between the template's intent and its setup is bridged only by studying the complex `gen_ai_fmi` example.

**What would lift this to 8/10**:
- Replace `.claude/CLAUDE.md` entirely with presentation-creator directives (P0)
- Add pptxgenjs technical rules to the root `CLAUDE.md` and `presentation-creator-prompt.md` (P0)
- Create `pptxgenjs-engineer.md` agent (P0)
- Delete all web app artifacts (P0 cleanup)
- Create a minimal `package.json` and presentation scaffold (P1)
- Create `revealjs-engineer.md` agent (P1)
- Rewrite the `README.md` (P1)
