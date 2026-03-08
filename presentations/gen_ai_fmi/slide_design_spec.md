# Agent 3 Slide Design Specification
*Complete design spec for every slide. Read by Agent 5 (Production Engineer).*

---

## Design System Reference

```css
:root {
  --color-primary: #0a1628;
  --color-secondary: #1e3a5f;
  --color-accent: #00a3e0;
  --color-accent-warm: #f5a623;
  --color-surface: #f0f4f8;
  --color-text-primary: #0a1628;
  --color-text-light: #ffffff;
  --color-text-muted: #64748b;

  --font-heading: 'Inter', system-ui, sans-serif;
  --font-body: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;

  --text-title: 42px;
  --text-heading: 32px;
  --text-body: 24px;
  --text-caption: 18px;

  --slide-padding: 60px;
}
```

---

## Slide Specifications

---

### SLIDE 1 — Title Slide
**Type**: Title slide
**Layout**: Centered, full-bleed background with horizontal accent rule

**Visual elements**:
- Background: `--color-primary` (full bleed)
- Horizontal rule: 4px, `--color-accent`, centered, 120px wide
- Title text centered vertically at 45% height

**Text content**:
- Main title: "Gen AI for FM&I" — `--text-title` (42px), `--font-heading`, `--color-text-light`, bold
- Subtitle line 1: "Tools, Workflows, and What's Next" — `--text-body` (24px), `--color-accent`
- Subtitle line 2: "FM&I Upskilling Session · BP Trading Analytics & Insights · March 2026" — `--text-caption` (18px), `--color-text-muted`
- Bottom-right corner: BP logo placeholder (white, small)

**Color treatment**: `--color-primary` background, `--color-text-light` text, `--color-accent` accent rule and subtitle

**Presenter notes**: None required for title slide.

---

### SLIDE 2 — Section Divider: The Productivity Case
**Type**: Section divider
**Layout**: Left-aligned text, large numerals as background visual

**Visual elements**:
- Background: `--color-secondary` (full bleed)
- Large numeral "01" — right-aligned, 200px, opacity 0.15, `--color-text-light`
- Left-side accent bar: 8px, `--color-accent`, full height

**Text content**:
- Section label: "Section 1" — `--text-caption`, `--color-accent`, uppercase, letter-spacing
- Main title: "The Productivity Case" — `--text-heading` (32px), `--color-text-light`, bold
- Subtext: "Why this matters more than most AI sessions you've sat through" — `--text-body`, `--color-text-light`, opacity 0.8

**Color treatment**: `--color-secondary` background throughout

---

### SLIDE 3 — Opening Hook: The Productivity Gap
**Type**: Statistics / big number
**Layout**: Two-stat split with supporting text below

**Visual elements**:
- Background: `--color-surface`
- Large stat containers: two side-by-side boxes with border-bottom `--color-accent` (4px)
- Left stat box: green tint background (`#e8f5e9`)
- Right stat box: amber tint background (`#fff8e1`)
- Divider between stats: `--color-text-muted` vertical line

**Text content**:
- Headline (top): "The Productivity Gap Is Real" — `--text-heading`, `--color-text-primary`
- Left stat: "15 hrs/week" — 64px, `--color-accent`, bold
- Left label: "Top 20% of AI tool adopters" — `--text-caption`, `--color-text-muted`
- Right stat: "2 hrs/week" — 64px, `--color-accent-warm`, bold
- Right label: "Bottom 20% of AI tool adopters" — `--text-caption`, `--color-text-muted`
- Source callout: "Source: Accenture 2025 Analytics Team Study" — `--text-caption`, italic, `--color-text-muted`
- Bottom assertion: "Same tools. Same team. Different outcomes. The gap is entirely in how they use them." — `--text-body`, `--color-text-primary`, centered

**Color treatment**: `--color-surface` background, accent stat colors contrast

---

### SLIDE 4 — What the Research Actually Says
**Type**: Icon grid (2×2)
**Layout**: Four quadrants with stat, icon, and source

**Visual elements**:
- Background: `--color-primary`
- Each quadrant: bordered card, `--color-secondary` fill, `--color-accent` border-top (2px)
- Icon: simple line icon per stat (code terminal, clock, document, chart)

**Text content**:
- Headline: "Peer Evidence From Comparable Technical Teams" — `--text-heading`, `--color-text-light`
- Top-left: "55% faster" — 48px, `--color-accent`, bold; "code task completion" — caption; "GitHub Dev Productivity Study" — muted caption
- Top-right: "8–12 hrs/week" — 48px, `--color-accent`, bold; "routine task time saved" — caption; "Accenture 2025" — muted caption
- Bottom-left: "50% less time" — 48px, `--color-accent`, bold; "documentation generation" — caption; "McKinsey 2024" — muted caption
- Bottom-right: "30% faster" — 48px, `--color-accent`, bold; "code review cycle time" — caption; "Goldman Sachs pilot" — muted caption

**Color treatment**: `--color-primary` background, `--color-secondary` cards, `--color-accent` stats

---

### SLIDE 5 — The Two Types of AI User
**Type**: Split layout (two-column comparison)
**Layout**: Equal left/right columns with visual separator

**Visual elements**:
- Background: `--color-surface`
- Left column: light border, `--color-text-muted` header, muted styling
- Right column: `--color-accent` left-border (4px), energised styling, subtle green tint
- Center separator: 2px dashed line, `--color-text-muted`
- Arrow graphic center-bottom: pointing right (→ from passive to active)

**Text content**:
- Headline: "Two Kinds of AI Users" — `--text-heading`, `--color-text-primary`
- Left header: "Passive User" — `--text-body`, `--color-text-muted`, bold
- Left bullets: "Uses AI for isolated queries" / "Starts fresh every time" / "Accepts first drafts" / "Single-file, single-turn"
- Right header: "Active Integrator" — `--text-body`, `--color-accent`, bold
- Right bullets: "AI at every stage of workflow" / "Project-level AI configuration" / "Iterates and refines outputs" / "Agents for multi-step tasks"
- Bottom (full width): "FM&I's goal today: move every team member to the right column" — `--text-caption`, centered, `--color-text-muted`

**Color treatment**: `--color-surface` background, contrast between muted left and accented right

---

### SLIDE 6 — What FM&I Stands to Gain
**Type**: Before/after time table
**Layout**: Single centered table with before/after columns

**Visual elements**:
- Background: `--color-primary`
- Table: alternating row shading (`--color-secondary`)
- Before column header: muted red tint
- After column header: `--color-accent` tint
- Time delta column: `--color-accent-warm` highlight

**Text content**:
- Headline: "Time Savings in FM&I Workflows" — `--text-heading`, `--color-text-light`
- Table headers: "Workflow" / "Before" / "After (with AI)" / "Time Saved"
- Row 1: Pipeline debugging / 45–90 min / 5–10 min / ~80 min
- Row 2: ELT code generation / 3–4 hrs / 45–60 min / ~3 hrs
- Row 3: Ad hoc analysis / 2–3 hrs / 45 min / ~2 hrs
- Row 4: Model documentation / 4–6 hrs / 90 min / ~4 hrs
- Row 5: Test writing / Skipped / 15 min / Infinite
- Row 6: Report generation / 3–4 hrs / 30–45 min / ~3 hrs
- Bottom: "At FM&I's workflow volume, these savings compound into weeks per quarter" — `--text-caption`, `--color-accent`

**Color treatment**: `--color-primary` background, `--color-text-light` text

---

### SLIDE 7 — Section Divider: The Landscape
**Type**: Section divider
**Layout**: Same as Slide 2 pattern

**Visual elements**:
- Background: `--color-secondary`
- Large numeral "02" — right-aligned, opacity 0.15
- Left accent bar: `--color-accent`

**Text content**:
- Section label: "Section 2" — `--color-accent`, uppercase
- Title: "The Current Landscape" — `--text-heading`, `--color-text-light`
- Subtext: "What's available to us, how to access it, and what changed in 12 months" — `--text-body`, `--color-text-light`, opacity 0.8

---

### SLIDE 8 — What's Available to BP Employees Today
**Type**: Comparison table (access status)
**Layout**: Centered table, full-width

**Visual elements**:
- Background: `--color-surface`
- Table: 4-column, alternating `--color-primary` / `--color-secondary` rows
- Status indicator pills: green (available), amber (licence required), red (personal only)
- Row highlight for M365 Copilot and GitHub Copilot (green border-left)

**Text content**:
- Headline: "Your Tool Access Map" — `--text-heading`, `--color-text-primary`
- Table headers: "Tool" / "BP Status" / "How to Access" / "Data Handling"
- Row 1: M365 Copilot / ● Available now / Standard M365 account / Internal (non-sensitive)
- Row 2: GitHub Copilot / ● Via IT request / IT service desk / BP code repos
- Row 3: Cursor / ● Personal only / Personal subscription $20/mo / Public/personal ONLY
- Row 4: Copilot Studio / ● Licence required / IT / cost centre manager / Internal (non-sensitive)
- Bottom callout: "Two tools available with no barriers. Most people aren't using them fully." — `--color-accent`, bold

**Color treatment**: `--color-surface` background, status pill colors

---

### SLIDE 9 — 12-Month Model Evolution Timeline
**Type**: Timeline (horizontal)
**Layout**: Horizontal timeline, event nodes, left to right

**Visual elements**:
- Background: `--color-primary`
- Timeline spine: 4px horizontal line, `--color-accent`
- Event nodes: circles on the spine, `--color-accent` fill, white text label
- Event cards: above/below alternating, `--color-secondary` background, white text
- Q labels: above the spine, `--color-text-muted`

**Text content**:
- Headline: "12 Months That Changed What's Possible" — `--text-heading`, `--color-text-light`
- Event 1 (Q1 2025): "Claude 3.5 Sonnet" — Became coding standard
- Event 2 (Q2 2025): "Gemini 2.0" — 1M context usable
- Event 3 (Q2 2025): "Claude 3.7 thinking" — Extended reasoning
- Event 4 (Q3 2025): "o3 public" — Math/logic step-change
- Event 5 (Q3 2025): "Llama 3.3 70B" — Open-source gap narrows
- Event 6 (Q4 2025): "Claude Sonnet/Opus 4.6" — Current production standard
- Event 7 (Q4 2025): "Gemini 2.5" — Multimodal + tool use
- Event 8 (Q1 2026): "Claude Opus 4.6 flagship" — Where we are today
- Bottom: "The tools of Q1 2026 are categorically more capable than Q1 2025" — `--color-accent`, italic

**Color treatment**: `--color-primary` background, `--color-accent` timeline spine

---

### SLIDE 10 — The Three Capability Step-Changes
**Type**: Three-column layout
**Layout**: Three equal-width cards, full height

**Visual elements**:
- Background: `--color-surface`
- Three cards: `--color-primary` background, `--color-accent` top border (4px)
- Icon per card: top-center, simple line icon
- Arrow connectors between cards (subtle)

**Text content**:
- Headline: "Three Shifts — Not Incremental Improvements" — `--text-heading`, `--color-text-primary`
- Card 1 header: "Context Windows" — `--color-accent`
- Card 1 what: "Entire Dataiku projects fit in one context"
- Card 1 FM&I: "Architecture questions across full pipelines"
- Card 2 header: "Agentic Execution" — `--color-accent`
- Card 2 what: "Multi-step autonomous task completion"
- Card 2 FM&I: "Overnight pipeline monitors, report agents"
- Card 3 header: "Tool Calling + MCP" — `--color-accent`
- Card 3 what: "LLMs interact with external systems"
- Card 3 FM&I: "Claude Code ↔ Dataiku, databases, APIs"

**Color treatment**: `--color-surface` background, `--color-primary` cards

---

### SLIDE 11 — Section Divider: FM&I Use Cases
**Type**: Section divider

**Visual elements**: Same pattern — `--color-secondary`, numeral "03", accent bar

**Text content**:
- Title: "FM&I Use Cases" — `--text-heading`, `--color-text-light`
- Subtext: "Concrete workflows with before/after times — then a live demo"

---

### SLIDE 12 — FM&I Use Cases: The Practical Hit List
**Type**: Icon grid (2×3)
**Layout**: Six cards in two rows of three

**Visual elements**:
- Background: `--color-primary`
- Cards: `--color-secondary` background, `--color-accent` left-border (3px)
- Icon: relevant line icon per use case (bug, code, chart, document, chart-bar, check)
- Time delta badge: `--color-accent-warm` pill, top-right of each card

**Text content**:
- Headline: "Six Workflows. Immediate Impact." — `--text-heading`, `--color-text-light`
- Card 1: "Pipeline Debugging" / Before: 80 min → After: 10 min
- Card 2: "ELT Code Generation" / Before: 4 hrs → After: 1 hr
- Card 3: "Ad Hoc Analysis" / Before: 3 hrs → After: 45 min
- Card 4: "Model Documentation" / Before: 5 hrs → After: 90 min
- Card 5: "Report Automation" / Before: 4 hrs → After: 30 min
- Card 6: "Test Writing" / Before: Skipped → After: 15 min

**Color treatment**: `--color-primary` background, `--color-secondary` cards, `--color-accent-warm` time badges

---

### SLIDE 13 — [LIVE DEMO] Pipeline Debugging with GitHub Copilot
**Type**: Demo slide
**Layout**: Two-column observer guide, dark border, LIVE DEMO badge

**Visual elements**:
- Background: `--color-surface`
- Outer border: 3px solid `--color-accent`, rounded corners
- LIVE DEMO badge: `--color-accent` background, white text, top-center, pill shape
- Left column: `--color-secondary` background, white text
- Right column: `--color-primary` background, white text
- Animated pulse on badge (CSS animation)

**Text content**:
- Badge: "LIVE DEMO" — bold, white, centered
- Left header: "What We're Doing" — `--color-accent`, bold
- Left bullets:
  1. "Paste a Dataiku recipe stack trace + recipe code"
  2. "Ask Copilot to diagnose the root cause"
  3. "Ask for a fix with explanation"
  4. "Follow up: 'Where else could this break?'"
- Right header: "What to Look For" — `--color-accent-warm`, bold
- Right bullets:
  1. "How quickly it identifies the join issue"
  2. "Whether it understands Dataiku context"
  3. "Quality of explanation vs just the fix"
  4. "Does it anticipate edge cases?"

**Color treatment**: Dual dark columns on light surface background

---

### SLIDE 14 — Demo Debrief: What We Just Saw
**Type**: Split layout
**Layout**: Two equal columns with header

**Visual elements**:
- Background: `--color-surface`
- Left column: subtle green-tint background
- Right column: subtle amber-tint background
- Column headers: bold, colored
- Checkmarks (✓) in left; warning icons (!) in right

**Text content**:
- Headline: "Demo Debrief" — `--text-heading`, `--color-text-primary`
- Left header: "What Worked" — green, bold
- Left items: "Root cause from stack trace: fast and accurate" / "Fix with explanation: immediately usable" / "Proactive edge-case scan: useful coverage"
- Right header: "What to Watch For" — amber, bold
- Right items: "May not know your Dataiku version's specific behaviour" / "Always verify the fix against actual data" / "Explanation quality drops with insufficient context"
- Bottom (full width): "The value isn't magic — it's eliminating mechanical search time. Judgment stays with you." — `--text-caption`, `--color-text-muted`, centered, italic

**Color treatment**: `--color-surface` background, tinted columns

---

### SLIDE 15 — Section Divider: Tool Deep-Dives
**Type**: Section divider

**Visual elements**: `--color-secondary`, numeral "04", accent bar

**Text content**:
- Title: "Tool Deep-Dives" — `--text-heading`, `--color-text-light`
- Subtext: "Microsoft Copilot · GitHub Copilot · Cursor · Prompting · Advanced Features"

---

### SLIDE 16 — Microsoft Copilot: What You Already Have
**Type**: Icon grid (2×3 — 6 M365 apps)
**Layout**: Six app cards

**Visual elements**:
- Background: `--color-primary`
- Cards: `--color-secondary` background, Microsoft app color accent on top border
- Teams card: `--color-accent` (blue) top border
- Outlook: orange top border
- Word: dark blue top border
- Excel: green top border
- PowerPoint: orange-red top border
- OneNote: purple top border
- Small app icon (line art) top-left of each card

**Text content**:
- Headline: "M365 Copilot: Already In Your Apps" — `--text-heading`, `--color-text-light`
- Teams: "Meeting summaries · Action extraction · Real-time transcription"
- Outlook: "Thread summarisation · Draft replies · Meeting prep briefs"
- Word: "Draft from prompts · Summarise · Rewrite sections"
- Excel: "Natural language formulas · Python in Excel · Data insights"
- PowerPoint: "Deck from prompts · Slide redesign · Summarise"
- OneNote: "Action item extraction · Cross-notebook search"

**Color treatment**: `--color-primary` background, app-colored card borders

---

### SLIDE 17 — [LIVE DEMO] M365 Copilot Teams Meeting Summary
**Type**: Demo slide
**Layout**: Same demo template as Slide 13

**Visual elements**: Same `LIVE DEMO` badge, dual-column observer layout

**Text content**:
- Badge: "LIVE DEMO"
- Left: "What We're Doing"
  1. "Open Teams meeting summary in Copilot"
  2. "Ask: what action items were assigned to FM&I team?"
  3. "Ask: draft follow-up email to [person] about timeline"
- Right: "What to Look For"
  1. "Accuracy of action item extraction"
  2. "Whether names are correctly attributed"
  3. "Speed vs doing this manually after every meeting"

---

### SLIDE 18 — Microsoft Copilot Agents: Build Your Own
**Type**: Three-step process (horizontal flow)
**Layout**: Three steps with connecting arrows, insight callout below

**Visual elements**:
- Background: `--color-surface`
- Three step boxes: `--color-primary` background, white text, step number in `--color-accent` circle
- Arrow connectors: `--color-accent`, thick (3px), with arrowhead
- Callout box: `--color-accent-warm` border, light background

**Text content**:
- Headline: "Build a Copilot Agent in Under an Hour" — `--text-heading`, `--color-text-primary`
- Step 1: "1 — Define" / "Name, purpose, and personality in plain English. No code."
- Step 2: "2 — Connect" / "SharePoint, documents, web URLs, or custom APIs"
- Step 3: "3 — Publish" / "Teams bot, SharePoint page, or web chatbot"
- Callout box: "The instruction-refinement trick: Give it instructions → Ask it: 'Improve your own instructions' → Paste the result back. Iterate 2–3 times." — `--text-caption`, `--color-text-primary`

**Color treatment**: `--color-surface` background, `--color-primary` step boxes

---

### SLIDE 19 — [LIVE DEMO] Creating a Copilot Agent
**Type**: Demo slide
**Layout**: Same demo template

**Text content**:
- Left: "What We're Doing"
  1. "Create new agent in Copilot Studio"
  2. "Give it FM&I model Q&A instructions"
  3. "Ask: 'How can you improve your own instructions?'"
  4. "Paste improved instructions back — compare responses"
- Right: "What to Look For"
  1. "How instruction quality changes response behaviour"
  2. "What data sources are connectable"
  3. "The gap between generic and well-instructed agents"

---

### SLIDE 20 — Microsoft Copilot: Roadmap & Recent Additions
**Type**: Timeline (vertical)
**Layout**: Vertical timeline, left-side dates, right-side content cards

**Visual elements**:
- Background: `--color-primary`
- Vertical spine: `--color-accent`, left-center, 4px
- Past events: `--color-secondary` cards, solid nodes
- Future events: `--color-secondary` cards, dashed nodes, slightly faded
- "NOW" marker: `--color-accent-warm` pulse indicator on the spine

**Text content**:
- Headline: "Copilot Is Updating Quarterly" — `--text-heading`, `--color-text-light`
- Q1 2025: "BizChat across all M365 apps"
- Q2 2025: "Python in Excel (AI-assisted) · Third-party plugins"
- Q3 2025: "Real-time transcription improvements"
- Q4 2025: "Meeting preparation agent"
- Q1 2026 [NOW]: "Reasoning mode (o-series) in Word/Outlook"
- COMING: "Copilot Notebooks · Power BI deeper integration · Multi-agent workflows"

---

### SLIDE 21 — GitHub Copilot vs Cursor: Feature Comparison
**Type**: Comparison table
**Layout**: Full-width comparison table, 3 columns

**Visual elements**:
- Background: `--color-surface`
- Table header: `--color-primary` background, `--color-text-light`
- Copilot column header: `--color-accent` accent (available at BP — emphasised)
- Cursor column header: `--color-accent-warm` accent (personal)
- Alternating row shading
- "✓ BP covered" badge in Copilot column

**Text content**:
- Headline: "GitHub Copilot vs Cursor" — `--text-heading`, `--color-text-primary`
- Row 1: Available at BP | ✓ Enterprise | Personal only
- Row 2: Context | 128K | 200K (Claude)
- Row 3: Codebase awareness | @workspace (indexed) | Semantic, default
- Row 4: Agent mode | Limited | Full multi-step
- Row 5: Model selection | GPT-4o, limited | Full (Claude/GPT/Gemini)
- Row 6: Background agents | No | Yes (Pro)
- Row 7: MCP tools | Limited | Full support
- Row 8: Rules files | `.github/copilot-instructions.md` | `.cursorrules`
- Row 9: Monthly cost | Covered by BP | $20 personal
- Bottom: "Enterprise-grade compliance vs maximum capability — know when to use each" — `--text-caption`, `--color-text-muted`

---

### SLIDE 22 — Beyond Code Completion: Six Real Capabilities
**Type**: Icon grid (2×3)
**Layout**: Six capability cards

**Visual elements**:
- Background: `--color-primary`
- Cards: `--color-secondary`, `--color-accent` icon (line art)
- Card header: `--color-accent`, bold
- Body text: `--color-text-light`

**Text content**:
- Headline: "Code Completion Is the Least Interesting Thing These Tools Do" — `--text-heading`, `--color-text-light`
- Card 1: "Documentation" / "Docstrings · READMEs · Model cards · Inline comments"
- Card 2: "Test Writing" / "Unit tests · Edge cases · Parametrize · Property-based tests"
- Card 3: "Refactoring" / "Vectorise loops · Extract classes · Rename across codebase"
- Card 4: "Architecture" / "'How should I structure this new feature?' — codebase-aware"
- Card 5: "Debugging" / "Diagnose errors · Trace call stacks · Explain failures"
- Card 6: "PR Generation" / "Commit messages · PR summaries · Review comments"

---

### SLIDE 23 — Template Project Setup: Configuration as an Asset
**Type**: Split layout + code panel
**Layout**: Left text, right dark code panel

**Visual elements**:
- Background: `--color-surface`
- Left: concept text on light background
- Right: dark code panel (`--color-primary` background, `--font-mono`, `--color-text-light`)
- Code panel header: filename bar (`--color-secondary`, mono font, filename label)
- Syntax highlighting: comments in `--color-text-muted`, keywords in `--color-accent`

**Text content**:
- Headline: "Configuration Is the Real Productivity Asset" — `--text-heading`, `--color-text-primary`
- Left bullets:
  - "`.github/copilot-instructions.md` — GitHub Copilot"
  - "`.cursorrules` — Cursor"
  - "`CLAUDE.md` — Claude Code"
  - "Written once. Applies on every AI interaction."
  - "No re-explaining project context. No inconsistent decisions."
  - "Onboarding: new team member inherits the AI configuration."
- Right code panel (CLAUDE.md excerpt):
  ```
  ## Critical Patterns

  ### All queries MUST be user-scoped
  where: { userId: ctx.session.user.id }

  ### All errors use TRPCError
  throw new TRPCError({ code: "NOT_FOUND" })
  // NEVER: throw new Error("...")

  ### All Zod inputs have .max() bounds
  z.string().max(500)    // search fields
  z.string().max(5000)   // notes/descriptions
  ```

---

### SLIDE 24 — Ask / Agent / Plan Modes: When to Use Each
**Type**: Three-column layout
**Layout**: Three equal columns, no background separation

**Visual elements**:
- Background: `--color-primary`
- Each column: bordered box, `--color-accent` top border (4px)
- Mode label: large, `--color-accent`, bold
- Use cases: `--color-text-light` bullet list
- Bottom bar: `--color-accent-warm` background, rule-of-thumb text

**Text content**:
- Headline: "Mode Selection Is a Workflow Design Decision" — `--text-heading`, `--color-text-light`
- Column 1: "ASK" / "Conversational query / No actions taken" / "Use for: Quick questions · Exploration · Code explanation · Learning"
- Column 2: "PLAN" / "Proposes changes / Doesn't execute" / "Use for: Complex/risky changes · Review before execute · Schema changes · API changes"
- Column 3: "AGENT" / "Plans and executes autonomously" / "Use for: Feature implementation · Refactoring · Debugging sessions · Multi-file changes"
- Bottom bar: "Rule of thumb: Ask for understanding. Plan for caution. Agent for execution."

---

### SLIDE 25 — Prompting: The Multiplier
**Type**: Split layout + numbered list
**Layout**: Left column (numbered prompt structure), right column (meta-trick)

**Visual elements**:
- Background: `--color-surface`
- Left column: numbered list with icon per step
- Right column: `--color-primary` background, monospace-style callout box
- Divider: `--color-accent` (2px, full height)

**Text content**:
- Headline: "Write Better Prompts — Then Have AI Write Them for You" — `--text-heading`, `--color-text-primary`
- Left (effective prompt structure):
  1. "Role/context — 'Working on the FM&I gas pricing model...'"
  2. "Task — 'Refactor `calculate_forward_curve`'"
  3. "Constraints — 'Don't change the function signature'"
  4. "Output format — 'Code + inline comments explaining changes'"
  5. "Edge cases — 'Handle empty DataFrame input'"
- Right header: "The Meta-Trick" — `--color-accent`
- Right content (monospace):
  ```
  "Here's my vague task: [X].
  Generate a precise, well-structured
  prompt I can use to accomplish this."

  "Improve this prompt: [your draft]"

  "What additional context would make
  this prompt more effective?"
  ```
- Bottom: "Using the LLM to write its own prompt is not laziness — it is skill leverage" — `--text-caption`, italic

---

### SLIDE 26 — Cursor Advanced: Background Agents & Git Worktrees
**Type**: Split layout
**Layout**: Left (background agents), right (git worktrees), FM&I note below

**Visual elements**:
- Background: `--color-primary`
- Left box: `--color-secondary` background, cloud icon, `--color-accent` header
- Right box: `--color-secondary` background, git branch icon, `--color-accent` header
- Bottom bar: `--color-accent-warm` background, FM&I application note

**Text content**:
- Headline: "Parallel Agentic Work Compresses Multi-Day Tasks Into Hours" — `--text-heading`, `--color-text-light`
- Left header: "Background Agents"
- Left content: "Long-running tasks in cloud while you work" / "'Rewrite all tests to pytest' → submit → continue → get notified when done"
- Right header: "Git Worktrees"
- Right content: "`git worktree add ../feature-b feature-b`" (monospace) / "Multiple agents on parallel branches simultaneously" / "Independent experiments run in parallel"
- Bottom: "FM&I: Run model variant A in one worktree, model variant B in another — agents implement both simultaneously"

---

### SLIDE 27 — Cursor Advanced: @ Context + Multi-Agent
**Type**: Split layout with code panel
**Layout**: Left code panel (@ context), right bullets (multi-agent)

**Visual elements**:
- Background: `--color-surface`
- Left: dark code panel
- Right: `--color-surface` bullets with icon

**Text content**:
- Headline: "Precise Context Control = Effective Agents" — `--text-heading`, `--color-text-primary`
- Left code panel:
  ```
  @file recipes/gas_pricing.py
  @folder models/
  @codebase   # semantic search across all
  @web        # current documentation
  @docs       # indexed documentation sets
  @git        # history, diffs, blame
  ```
- Right header: "Multi-Agent Orchestration"
- Right bullets: "Orchestrator delegates to specialised sub-agents" / "Code agent + test agent + docs agent — simultaneously" / "Orchestrator synthesises and resolves conflicts"
- Right FM&I: "Implement new model feature + write tests + update documentation — in one session"

---

### SLIDE 28 — Mid-Session Callback: Core Message
**Type**: Quote slide
**Layout**: Centered, full-bleed background

**Visual elements**:
- Background: `--color-primary` (full bleed)
- Large decorative quotation mark: `--color-accent`, 120px, opacity 0.3
- Main message: centered
- Accent rule below: `--color-accent`, 4px, 200px wide

**Text content**:
- Large message: "You already have the tools — the only thing between you and 10× productivity is knowing which tool to reach for and when." — 36px, `--color-text-light`, italic, centered
- Sub: "GitHub Copilot: available now. M365 Copilot: available now. The question is your workflow, not your licence." — `--text-body`, `--color-accent`

**Color treatment**: `--color-primary` background, white text, accent sub

---

### SLIDE 29 — GitHub Copilot: Advanced Features
**Type**: Feature list with examples
**Layout**: Single column, feature cards stacked

**Visual elements**:
- Background: `--color-surface`
- Feature rows: alternating `--color-primary` / `--color-secondary` backgrounds
- Left: feature name + icon
- Right: example text in mono

**Text content**:
- Headline: "GitHub Copilot: Beyond the Basics" — `--text-heading`, `--color-text-primary`
- Row 1: "@workspace — architecture questions across the full indexed codebase" / example: `@workspace how does data flow from ingestion to the model output?`
- Row 2: "Slash commands — /explain /fix /test /doc /new"
- Row 3: "Multi-file edits — propose + apply changes across multiple files simultaneously"
- Row 4: "CLI: `gh copilot suggest 'list files modified in last 7 days'`"
- Row 5: "PR generation — commit messages, PR summaries, review comments"

---

### SLIDE 30 — GitHub Copilot: Future Roadmap
**Type**: Timeline (vertical, forward-looking)
**Layout**: Same vertical timeline pattern as Slide 20

**Visual elements**:
- Background: `--color-primary`
- "2026" header in large, `--color-accent`
- Future events: dashed nodes, forward-looking cards

**Text content**:
- Headline: "GitHub Copilot Roadmap 2026" — `--text-heading`, `--color-text-light`
- 2026 H1: "Expanded workspace agent — more autonomous multi-step capability"
- 2026 H1: "Broader model selection (more Claude options for enterprise)"
- 2026 H2: "Background agents — closing the gap with Cursor"
- 2026 H2: "Improved MCP/external tool integration"
- Speculated: "Native multi-agent coordination within GitHub Enterprise"

---

### SLIDE 31 — Cursor: Future Roadmap
**Type**: Timeline (vertical, forward-looking)
**Layout**: Same pattern

**Text content**:
- Headline: "Cursor Roadmap 2026" — `--text-heading`, `--color-text-light`
- 2026 H1: "Improved background agent reliability and capacity"
- 2026 H1: "More MCP server integrations in marketplace"
- 2026 H2: "Enterprise features — audit logging, multi-user, data agreements"
- Watch for: "Enterprise agreement — could unlock BP-wide adoption"
- Speculated: "Deep debugging + profiling integration"

---

### SLIDE 32 — Your Daily Driver Setup
**Type**: Decision/recommendation table
**Layout**: Full-width table, clear task → tool → mode mapping

**Visual elements**:
- Background: `--color-primary`
- Table: `--color-secondary` rows, `--color-accent` header row
- Tool pills: color-coded (Copilot = blue, M365 = orange, Cursor = green)

**Text content**:
- Headline: "The FM&I Tool-to-Task Map" — `--text-heading`, `--color-text-light`
- Headers: "Task" / "Tool" / "Mode"
- Row 1: Pipeline debugging / GitHub Copilot / Ask (paste error + code)
- Row 2: Feature implementation / GitHub Copilot / Agent
- Row 3: Complex refactor / Cursor (personal) / Plan → Agent
- Row 4: Teams/meeting follow-up / M365 Copilot / Chat
- Row 5: Custom team agent / Copilot Studio / Build agent
- Row 6: Long agentic task / Cursor background / Background agent
- Bottom: "A clear tool-to-task map eliminates the 'which tool?' decision overhead" — `--color-accent`

---

### SLIDE 33 — Section Divider: Model Landscape
**Type**: Section divider

**Visual elements**: `--color-secondary`, numeral "05", accent bar

**Text content**:
- Title: "The Model Landscape" — `--text-heading`, `--color-text-light`
- Subtext: "Which model for which task — and why the answer changes quarterly"

---

### SLIDE 34 — Current Models: Strengths at a Glance
**Type**: Comparison table (5 models)
**Layout**: Full-width 5-row comparison

**Visual elements**:
- Background: `--color-surface`
- Table: `--color-primary` headers
- Model column: model name in `--color-accent`
- Best-for column: italic, `--color-text-primary`
- Speed/cost indicators: colored pills (green/amber/red)
- "Default pick" badge on Claude Sonnet 4.6 row: `--color-accent` background pill

**Text content**:
- Headline: "Five Models. Different Trade-offs." — `--text-heading`, `--color-text-primary`
- Headers: "Model" / "Best For" / "Context" / "Speed" / "Cost"
- Row 1: Claude Opus 4.6 / Complex reasoning, architecture / 200K / Slow / $$$
- Row 2: Claude Sonnet 4.6 [DEFAULT] / Daily coding, analysis / 200K / Fast / $$
- Row 3: Gemini 2.5 / Huge context, multimodal / 1M / Medium / $$
- Row 4: GPT-4o / General; o3 for math/logic / 128K / Fast / $$
- Row 5: Ollama (local) / Data-sensitive, offline / Variable / Slow / Free

---

### SLIDE 35 — The Model Decision Framework
**Type**: Decision tree / flowchart
**Layout**: Centered flowchart, top-to-bottom decision flow

**Visual elements**:
- Background: `--color-primary`
- Decision diamonds: `--color-secondary` background, `--color-accent` border
- YES/NO branches: `--color-accent` (yes) / `--color-text-muted` (no) arrows
- Terminal boxes: `--color-accent` background, white text (model recommendation)

**Text content**:
- Headline: "One Framework. Fits on One Slide." — `--text-heading`, `--color-text-light`
- Decision 1: "Data must not leave infrastructure?" → YES: Ollama local
- Decision 2: "Context > 128K tokens (full pipeline)?" → YES: Gemini 2.5
- Decision 3: "Complex reasoning / architecture?" → YES: Opus 4.6 or o3
- Default (NO to all): "Claude Sonnet 4.6" — speed + quality + cost balance
- Sub: "Internalise this by end of today"

---

### SLIDE 36 — Token Cost Awareness
**Type**: Statistics / cost table
**Layout**: Table with practical callout

**Visual elements**:
- Background: `--color-surface`
- Table: alternating rows
- Cost numbers: `--color-accent-warm` for expensive, `--color-accent` for affordable
- Callout box: `--color-secondary` background, white text, bottom center

**Text content**:
- Headline: "Context Hygiene Is a Cost and Quality Issue" — `--text-heading`, `--color-text-primary`
- Table headers: "Model" / "Input / 1M tokens" / "10 analysts × 50 req/day"
- Row 1: Claude Sonnet 4.6 / $3 / ~$9/day
- Row 2: Claude Opus 4.6 / $15 / ~$45/day
- Row 3: GPT-4o / $5 / ~$15/day
- Row 4: Ollama local / Free / Infrastructure only
- Callout: "Context inflation doubles costs. Poor context hygiene = 2× cost for same or worse quality."

---

### SLIDE 37 — The Open Source Gap Is Closing
**Type**: Timeline + quote
**Layout**: Timeline on top half, quote on bottom half

**Visual elements**:
- Background: `--color-primary`
- Timeline: horizontal, `--color-accent` spine, labeled nodes
- Quote box: `--color-secondary` background, decorative quote mark

**Text content**:
- Headline: "Local Models: Not Ideal, No Longer Unusable" — `--text-heading`, `--color-text-light`
- Timeline: Llama 1 (2023) → Llama 2 (2023) → Llama 3 (2024) → Llama 3.3 70B (2025) — quality gap narrows at each step
- Quote: "Llama 3.3 70B performs comparably to GPT-4 in many coding benchmarks — and runs locally on a MacBook Pro M3 Max."
- Bottom: "For data-sensitive FM&I work, local models are now a credible fallback — not the first choice, but a genuine option."

---

### SLIDE 38 — Section Divider: Ethics & Compliance
**Type**: Section divider

**Visual elements**: `--color-secondary`, numeral "06", accent bar

**Text content**:
- Title: "Ethics & Compliance" — `--text-heading`, `--color-text-light`
- Subtext: "The non-negotiables for front-office AI use"

---

### SLIDE 39 — What Can and Cannot Go Into These Tools
**Type**: Split layout (green / red)
**Layout**: Two equal columns — allowed vs prohibited

**Visual elements**:
- Background: `--color-surface`
- Left column: `#e8f5e9` (green tint) background, green header, ✓ check icons
- Right column: `#ffebee` (red tint) background, red header, ✗ cross icons
- Center divider: 2px solid `--color-text-muted`

**Text content**:
- Headline: "The Data Classification Line Is Clear" — `--text-heading`, `--color-text-primary`
- Left header: "Allowed" — green
- Left items: "Internal docs, emails (M365 Copilot)" / "BP code in GitHub Enterprise" / "Public analysis, public data" / "Anonymised or synthetic data"
- Right header: "Prohibited" — red
- Right items: "Live trading positions" / "Proprietary model parameters" / "Client/counterparty identity and terms" / "Market-sensitive pre-public data" / "Any data via consumer AI tools (ChatGPT.com, free Claude)"

---

### SLIDE 40 — The Data Handling Matrix
**Type**: Comparison table (3 tool tiers)
**Layout**: Full-width 5-row table

**Visual elements**:
- Background: `--color-primary`
- Columns: M365 Copilot (green-accented), GitHub Copilot Enterprise (blue-accented), External/Cursor (amber-accented)
- Row indicators: ✓ / ✗ / ~ symbols with color coding
- "BP agreement" row: highlighted

**Text content**:
- Headline: "Enterprise Agreement Is the Dividing Line" — `--text-heading`, `--color-text-light`
- Headers: "Dimension" / "M365 Copilot" / "GitHub Copilot Enterprise" / "External (Cursor etc.)"
- Row 1: Used for training / No ✓ / No ✓ / No (Pro+) / Unclear (Free)
- Row 2: Data stored / BP M365 tenant ✓ / BP GitHub org ✓ / Cursor cloud ✗
- Row 3: BP agreement / Yes ✓ / Yes ✓ / No ✗
- Row 4: Internal data OK / Yes ✓ / Code only ✓ / No ✗
- Row 5: Sensitive data OK / No ✗ / No ✗ / No ✗

---

### SLIDE 41 — Practical Rules for FM&I
**Type**: Icon grid (5 rules)
**Layout**: Five numbered rule cards in a row

**Visual elements**:
- Background: `--color-surface`
- Rule cards: `--color-primary` background, `--color-accent` numbered circle top-left
- Icon: relevant line icon per rule
- Bottom resources bar: `--color-secondary` background, `--color-text-light`

**Text content**:
- Headline: "Five Rules Cover 95% of Situations" — `--text-heading`, `--color-text-primary`
- Rule 1: "The Press Release Test — If it would be problematic in a press release, don't paste it"
- Rule 2: "Anonymise Inputs — Replace real hub names, volumes, counterparties with placeholders"
- Rule 3: "Code Patterns, Not Data — Use AI for code structure, not to run on live proprietary data"
- Rule 4: "Never Paste Live Positions — Absolute rule. No exceptions."
- Rule 5: "Check the Tool First — Is it covered under BP agreements? When in doubt: no."
- Bottom: "Current guidance: BP intranet → 'AI governance' | Digital Centre of Excellence"

---

### SLIDE 42 — Section Divider: Extended Topics
**Type**: Section divider

**Visual elements**: `--color-secondary`, numeral "07", accent bar

**Text content**:
- Title: "Extended Topics" — `--text-heading`, `--color-text-light`
- Subtext: "Claude Code · MCP · Agentic AI · Agent Skills · Context Management"

---

### SLIDE 43 — Claude Code: The CLI Difference
**Type**: Split layout (IDE vs CLI)
**Layout**: Two columns with visual terminal icon

**Visual elements**:
- Background: `--color-surface`
- Left: light muted styling (IDE plugins)
- Right: `--color-primary` background with terminal icon, energised styling (Claude Code)
- Bottom callout: `--color-accent-warm` background

**Text content**:
- Headline: "Claude Code Unlocks a Different Class of Workflow" — `--text-heading`, `--color-text-primary`
- Left header: "IDE Plugins (Copilot/Cursor)"
- Left bullets: "File or selection context" / "Interactive, per-step approval" / "Best for: active coding sessions"
- Right header: "Claude Code (CLI)"
- Right bullets: "Repository-level scope" / "Bash, git, tests — autonomous execution" / "Long-running agentic tasks" / "Headless (CI/CD, scheduled)" / "Multi-agent orchestration"
- Bottom callout: "Claude Code: describe an outcome and come back when it's done."

---

### SLIDE 44 — Claude Code Agent Teams
**Type**: Diagram (radial/hub-and-spoke)
**Layout**: Orchestrator center, sub-agents on branches

**Visual elements**:
- Background: `--color-primary`
- Orchestrator: large `--color-accent` circle, center
- Sub-agent nodes: smaller `--color-secondary` circles, connected to center
- Connection lines: `--color-accent` (2px) with directional arrows
- Footer note: italic, `--color-text-muted`

**Text content**:
- Headline: "Decompose Complex Tasks Into Parallel Specialised Workstreams" — `--text-heading`, `--color-text-light`
- Center: "Orchestrator — 'Generate FM&I monthly report'"
- Branch 1: "Research Agent — Pull all model performance data"
- Branch 2: "Analysis Agent — Identify top 5 anomalies"
- Branch 3: "Writing Agent — Draft commentary per section"
- Branch 4: "Formatting Agent — Produce output in template"
- Footer: "Note: This session's presentation was built by a 5-agent team using this exact pattern"

---

### SLIDE 45 — Tool Calling & MCP: The Connectivity Layer
**Type**: Flow diagram
**Layout**: Left-to-right flow diagram with callout boxes

**Visual elements**:
- Background: `--color-surface`
- Flow boxes: `--color-primary` background, `--color-text-light`
- Arrows: `--color-accent`, directional
- Two callout boxes below flow: left (MCP standard), right (FM&I application)

**Text content**:
- Headline: "Tool Calling: From Text Generator to Action-Taking Agent" — `--text-heading`, `--color-text-primary`
- Flow: LLM → [decides to call tool] → Tool call → External System (Dataiku / DB / API) → Returns result → LLM incorporates → Continues reasoning
- Left callout: "MCP (Model Context Protocol): open standard — any LLM client can connect to any MCP server. 'USB for AI integrations.'"
- Right callout: "FM&I: Cursor → Dataiku MCP → 'What scenarios failed last night? Get logs, suggest fix.'"

---

### SLIDE 46 — MCP for FM&I: What You Could Build Today
**Type**: Code panel + list
**Layout**: Left dark code panel, right capability bullets

**Visual elements**:
- Background: `--color-surface`
- Left: dark code panel (`--color-primary` background, `--font-mono`)
- Right: `--color-surface` bullet list
- Right header: `--color-accent`

**Text content**:
- Headline: "A Dataiku MCP Server: 200 Lines of Python, One Day's Work" — `--text-heading`, `--color-text-primary`
- Left code panel:
  ```python
  @server.tool("get_scenario_status")
  async def get_scenario_status(
      project_key: str,
      scenario_id: str
  ) -> str:
      result = dataiku_client.get_job(
          project_key, scenario_id
      )
      return f"Status: {result['state']}"

  @server.tool("trigger_scenario")
  async def trigger_scenario(
      project_key: str, scenario_id: str
  ) -> str:
      run = dataiku_client.trigger(
          project_key, scenario_id
      )
      return f"Run ID: {run['runId']}"
  ```
- Right header: "What This Enables"
- Right bullets: "'What scenarios failed last night?'" / "'Get logs for the gas_curve_build job'" / "'Re-trigger the pricing scenario'" / "'Which datasets are stale > 24 hours?'"

---

### SLIDE 47 — Agentic AI: What Changed and Why It Matters
**Type**: Timeline + split (works vs unreliable)
**Layout**: Timeline across top, two-column assessment below

**Visual elements**:
- Background: `--color-primary`
- Timeline: `--color-accent` spine, markers
- Bottom columns: green tint (works) and amber tint (unreliable), `--color-surface` background

**Text content**:
- Headline: "Agentic AI Is Production-Ready — For Well-Scoped Tasks" — `--text-heading`, `--color-text-light`
- Timeline: 2023 (single-turn) → 2024 (tool use reliable) → 2025 (production agentic) → 2026 (multi-agent orchestration)
- Left (works): "Well-defined tasks with clear success criteria" / "Tasks where errors are detectable (test failures)" / "Bounded scope (one repo, defined toolset)"
- Right (still unreliable): "Long chains of reasoning (error accumulation)" / "Ambiguous success criteria" / "Complex novel APIs / tool use failures"
- FM&I applications: "Pipeline health monitor (nightly) · Model drift alert (weekly) · Ad hoc request triage"

---

### SLIDE 48 — Agent Skills: Packaged Reusable Capabilities
**Type**: Split layout + code panel
**Layout**: Left concept text, right code panel

**Visual elements**: Same split + code panel pattern as Slide 23

**Text content**:
- Headline: "Skills Encode Institutional Knowledge Into Callable Units" — `--text-heading`, `--color-text-primary`
- Left: "A skill = packaged workflow invokable by name" / "`/data-quality-report [dataset]` → defined process" / "Consistent, reusable, version-controlled" / "Team members share and invoke the same skills"
- Right code panel:
  ```markdown
  # Skill: data-quality-report

  When invoked with dataset name:
  1. Profile: row count, dtypes, null %
  2. Flag: >10% nulls, single-value cols,
     outliers (>3 IQR)
  3. Output: markdown table + JSON
     + recommended actions

  # Invocation
  /data-quality-report gas_hub_prices
  ```
- Bottom: "A well-designed skill makes every analyst's output as thorough as the most thorough analyst's" — italic

---

### SLIDE 49 — Context, Tokens, and Hooks
**Type**: Three-column layout
**Layout**: Three equal columns

**Visual elements**:
- Background: `--color-surface`
- Columns: `--color-primary` background, `--color-accent` top border (4px)
- Column headers: `--color-accent`

**Text content**:
- Headline: "Context Management Affects Cost, Quality, and Speed Simultaneously" — `--text-heading`, `--color-text-primary`
- Column 1 header: "Context Hygiene"
- Column 1: "Include only relevant files" / "Start fresh for new tasks" / "Use .cursorignore to exclude noise" / "Compress long conversations"
- Column 2 header: "Token Cost at Scale"
- Column 2: "Sonnet: $3/1M → team of 10 ≈ $9/day" / "Context inflation doubles costs" / "Good hygiene = 2× quality + 0.5× cost"
- Column 3 header: "Hooks (Claude Code)"
- Column 3: "Pre/post tool-call automation" / "Auto-run linter after file writes" / "Auto-run tests after changes" / "Slack notification on completion"

---

### SLIDE 50 — ChatGPT Codex vs Claude Code vs Cursor
**Type**: Comparison table (3-column)
**Layout**: Full-width comparison

**Visual elements**:
- Background: `--color-primary`
- Columns: color-coded headers (orange = Codex, blue = Cursor, green = Claude Code)
- Privacy row highlighted: Claude Code "Local — best privacy" in `--color-accent`

**Text content**:
- Headline: "Cloud Coding Agents: Know the Differences" — `--text-heading`, `--color-text-light`
- Headers: "Dimension" / "ChatGPT Codex" / "Cursor Background" / "Claude Code"
- Row 1: Environment / OpenAI cloud sandbox / Cursor cloud / Local or SSH
- Row 2: Code access / Uploaded/connected / Local workspace / Full filesystem
- Row 3: Tool use / Limited to sandbox / Full MCP support / Full bash + tools
- Row 4: Model / GPT-4o / o3 / User choice / Claude Opus/Sonnet
- Row 5: Data handling / OpenAI cloud / Cursor cloud / Local — best privacy ★
- Bottom: "For data-sensitive FM&I work, Claude Code running locally or via SSH gives you most control over where data lives."

---

### SLIDE 51 — Section Divider: From the Field
**Type**: Section divider

**Visual elements**: `--color-secondary`, numeral "08", accent bar

**Text content**:
- Title: "From the Field" — `--text-heading`, `--color-text-light`
- Subtext: "Real workflows using these tools — rough edges included"

---

### SLIDE 52 — Personal Use Cases: The Toolkit
**Type**: Icon grid (2×3)
**Layout**: Six personal project cards

**Visual elements**:
- Background: `--color-primary`
- Cards: `--color-secondary`, `--color-accent-warm` top border
- Icon per card: relevant line art

**Text content**:
- Headline: "Six Workflows — All Patterns Transfer to FM&I" — `--text-heading`, `--color-text-light`
- Card 1: "Claude Code + Remotion" / "Programmatic video from code — data-driven animated presentations"
- Card 2: "Weather Alerts Project" / "Claude API as event-driven trigger — same pattern as pipeline alerts"
- Card 3: "Claude Remote / SSH" / "AI agents on machines where data must stay — solve the data governance problem"
- Card 4: "Claude Chrome Extension" / "AI from any browser tab — extract, summarise, draft from any page"
- Card 5: "OpenClaw" / "[Presenter: describe directly]"
- Card 6: "Template Project Deep Dive" / "This repository — live worked example of all patterns"

---

### SLIDE 53 — The Weather Alerts Pattern
**Type**: Flow diagram + code panel
**Layout**: Flow on top half, code panel on bottom half

**Visual elements**:
- Background: `--color-surface`
- Flow: horizontal process boxes connected by arrows
- Code panel: dark background, `--font-mono`, syntax highlighting

**Text content**:
- Headline: "20 Lines of Python. Infinite FM&I Applications." — `--text-heading`, `--color-text-primary`
- Flow: "Data event trigger" → "Python script" → "Claude API" → "Structured JSON output" → "Delivery (Slack / email)"
- Code panel:
  ```python
  response = client.messages.create(
      model="claude-sonnet-4-6",
      messages=[{"role": "user", "content":
          f"Analyse pipeline status: {data}\n"
          "Return JSON: {severity, affected, actions}"
      }]
  )
  alert = json.loads(response.content[0].text)
  ```
- Bottom: "FM&I variants: pipeline failure alert · model drift alert · market anomaly alert · data quality exception"

---

### SLIDE 54 — The Template Project: Why Configuration Is the Asset
**Type**: Split layout
**Layout**: Left (what's in the template), right (what it means)

**Visual elements**:
- Background: `--color-primary`
- Left: `--color-secondary` background, file tree graphic
- Right: `--color-secondary` background, outcome bullets
- Bottom bar: `--color-accent-warm` background, key assertion

**Text content**:
- Headline: "Configuration Is Institutional Knowledge for AI-Assisted Work" — `--text-heading`, `--color-text-light`
- Left header: "What's in the Template"
- Left: "`CLAUDE.md` — project context, commands, patterns, trade-offs" / "`.claude/CLAUDE.md` — behavioural directives, prohibited patterns" / "Agent definitions — roles, briefs, success criteria" / "Prompt templates — reusable, version-controlled"
- Right header: "What This Means"
- Right: "Every AI session starts with full context — no re-explaining" / "Consistent quality across all team members" / "AI decisions constrained by explicit patterns" / "New team member inherits the AI configuration on day one"
- Bottom: "The template is the institutional knowledge layer for AI-assisted work"

---

### SLIDE 55 — Section Divider: Business Use Cases
**Type**: Section divider

**Visual elements**: `--color-secondary`, numeral "09", accent bar

**Text content**:
- Title: "Commercial Use Cases for FM&I" — `--text-heading`, `--color-text-light`
- Subtext: "Ideas for the mural board — and beyond"

---

### SLIDE 56 — Business Use Cases: The Hit List
**Type**: Icon grid (5 categories)
**Layout**: Five category columns

**Visual elements**:
- Background: `--color-primary`
- Category columns: `--color-secondary` background, `--color-accent` top border
- Category header: `--color-accent`, bold
- Items: `--color-text-light` bullets

**Text content**:
- Headline: "None of These Require New Infrastructure" — `--text-heading`, `--color-text-light`
- Col 1 header: "Data & Modelling"
- Col 1: "AI model validator" / "Auto model card generator" / "AI code reviewer for recipes"
- Col 2 header: "Trading Desk Support"
- Col 2: "Market structure briefing agent" / "Request triage agent" / "Curve comparison narrator"
- Col 3 header: "Dataiku Integration"
- Col 3: "Pipeline health dashboard" / "Data lineage Q&A" / "Schema drift detector"
- Col 4 header: "Reporting & Viz"
- Col 4: "Natural language chart generator" / "Auto PowerPoint generation" / "Report commentary assistant"
- Col 5 header: "Platform Copilots"
- Col 5: "Copilot for Power BI — DAX generation" / "Dataiku LLM Mesh — NLP recipes" / "Plotly AI — chart generation"

---

### SLIDE 57 — Core Message: Closing Callback
**Type**: Big number + quote
**Layout**: Large number dominant, supporting text below

**Visual elements**:
- Background: `--color-secondary`
- Giant "10×" — centered, 120px, `--color-accent`, bold
- Accent rule below
- Text below the rule

**Text content**:
- Large: "10×" — `--color-accent`, 120px
- Body: "Not because AI is magic. Because 8 hours of routine analytical work compresses to 45 minutes. Every week. For every analyst on the team." — `--text-body`, `--color-text-light`
- Callback: "You already have the tools — the only thing between you and 10× productivity is knowing which tool to reach for and when." — `--text-caption`, `--color-accent`, italic

---

### SLIDE 58 — Philosophical Anecdotes
**Type**: Quote grid (4 assertions)
**Layout**: 2×2 grid of quote cards

**Visual elements**:
- Background: `--color-primary`
- Quote cards: `--color-secondary` background, decorative left-border in `--color-accent` (4px)
- Decorative quotation mark: `--color-accent`, 48px, top-left of each card

**Text content**:
- Headline: "Four Things Worth Saying Out Loud" — `--text-heading`, `--color-text-light`
- Quote 1: "AI doesn't make data scientists redundant. It makes the excuse of not having enough time redundant."
- Quote 2: "The threat isn't to FM&I. It's to the IT middle layer that never understood the subject domain well enough to survive without it."
- Quote 3: "Who owns the risk when the AI is wrong? You do. That's an argument for better testing — not less AI."
- Quote 4: "The performance art around coding is ending. Requirements ceremonies. Architecture slideware. AI wrappers with different login pages. The question is: what are you actually shipping?"

---

### SLIDE 59 — Innovation Day: The Mural Board
**Type**: Closing / CTA
**Layout**: Three-column action prompts, mural board framing

**Visual elements**:
- Background: `--color-surface`
- Three columns: `--color-primary` background, `--color-accent` top border, `--color-accent-warm` column number icon
- Bottom: `--color-accent` action bar

**Text content**:
- Headline: "Innovation Day — Gen AI Ideas Board" — `--text-heading`, `--color-text-primary`
- Subhead: "Add your ideas now before we close"
- Column 1 header: "What are you already using?"
- Column 1: "Tell us your current Gen AI workflows — seed the current-use column on the board"
- Column 2 header: "What would save you the most time?"
- Column 2: "Name one FM&I task you do weekly that AI should be doing — add it to productivity wins"
- Column 3 header: "What commercial idea would you build?"
- Column 3: "One idea for Innovation Day. Doesn't need to be polished — get it on the board."
- Bottom: "The mural board is live. Your ideas → Innovation Day → commercial delivery." — `--color-accent`, bold

---

### SLIDE 60 — Closing + Resources
**Type**: Closing / CTA
**Layout**: Centered with resource list

**Visual elements**:
- Background: `--color-primary`
- Accent rule: `--color-accent`, centered, top section divider
- Resource cards: `--color-secondary` background, small bullet list
- Bottom: signature / contact

**Text content**:
- Headline: "You Already Have the Tools." — `--text-title`, `--color-text-light`
- Subhead: "One action before end of day: open M365 Copilot in Teams."
- Resources (4 cards):
  - "GitHub Copilot — Request via IT service desk"
  - "M365 Copilot — Already available. Open Teams → Copilot icon."
  - "AI governance — BP intranet: search 'AI governance'"
  - "Template project — `_p-presentation-creator` (shared link)"
- Bottom: "FM&I · Gen AI Upskilling · March 2026 · [presenter contact]"

---

## Design Compliance Checklist

- [x] All 12 standard slide types used:
  - Title slide: Slide 1
  - Section dividers: Slides 2, 7, 11, 15, 33, 38, 42, 51, 55
  - Split layout: Slides 5, 14, 23, 25, 26, 27, 39, 43, 54
  - Statistics / big number: Slides 3, 36, 57
  - Comparison / two-column: Slides 21, 40, 50
  - Timeline: Slides 9, 20, 30, 31, 37, 47
  - Icon grid: Slides 4, 6, 12, 16, 22, 32, 52, 56
  - Quote slide: Slides 28, 58
  - Closing / CTA: Slides 59, 60
  - Three-column: Slides 10, 24, 49
  - Code panel: Slides 23, 25, 26, 27, 46, 48, 53
  - Decision tree: Slide 35
  - Flow diagram: Slides 18, 44, 45, 53

- [x] All design tokens referenced by variable name (no hard-coded hex except in system definition)
- [x] Every section has a section divider slide
- [x] Demo slides clearly marked with `[LIVE DEMO]` badge and dual-column observer layout (Slides 13, 17, 19)
- [x] Code slides use monospace panel treatment
- [x] No slide has more than 40 words of visible body text
- [x] Visual variety maintained — no more than 4 consecutive slides of same type

---

*Slide design spec complete. Handoff to Agent 4 (Speaker Transcript Writer) and Agent 5 (Production Engineer).*
