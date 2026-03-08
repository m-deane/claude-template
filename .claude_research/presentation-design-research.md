# Presentation Design Research

## Research Summary

This document captures the research foundations behind the Presentation Creator Agent Team prompt.

---

## 1. What Makes a Great Presentation

### Expert Frameworks

**Nancy Duarte (Resonate, Slide:ology)**:
- Presentations should follow a **story arc** — alternating between "what is" and "what could be" to create tension and resolution
- The audience is the hero, not the presenter. The presenter is the mentor
- The "Big Idea" should be expressible in one complete sentence
- Every element in a presentation should support the Big Idea

**Garr Reynolds (Presentation Zen)**:
- **Restraint** in design — remove everything that isn't essential
- **Simplicity** is not dumbing down; it's intelligent clarity
- Use high-quality, full-bleed images that evoke emotion
- Embrace empty space — it creates focus
- Tell stories; humans are wired for narrative

**Edward Tufte (The Visual Display of Quantitative Information)**:
- **Data-ink ratio**: Maximize the share of ink used to present data, minimize non-data ink
- **Chartjunk**: Remove unnecessary grid lines, 3D effects, decorative elements
- **Small multiples**: Show patterns through repetition of simple charts
- **Lie factor**: Ensure visual representation accurately reflects the data
- Strongly opposed to bullet points and PowerPoint's default templates

**Assertion-Evidence Model (Michael Alley, Penn State)**:
- Replace topic-phrase headlines with **full-sentence assertions**
- Body of slide is **visual evidence** (not text bullets) that supports the assertion
- Research shows 20% better retention vs. traditional topic-bullet slides
- Example: Instead of "Q3 Revenue" → "Q3 revenue grew 34%, driven by enterprise expansion"

### Key Principles Synthesized

1. **One message per slide** — if you can't state the slide's point in one sentence, it's too complex
2. **Signal-to-noise ratio** — every pixel must earn its place
3. **Story structure** — beginning (status quo), middle (tension/insight), end (resolution/CTA)
4. **Picture superiority effect** — images remembered 6x better than text after 3 days (Paivio, 1986)
5. **Cognitive load theory** (Sweller) — working memory handles 4±1 chunks; don't exceed this per slide
6. **Dual coding** — combine verbal and visual channels for maximum retention

---

## 2. Effective Slide Design

### Typography Best Practices

- **Sans-serif for presentations**: Screen readability favors Inter, Helvetica Neue, Poppins, Montserrat
- **Minimum sizes**: 44pt titles, 28pt body, 18pt absolute minimum for any text
- **Maximum 2 typefaces**: One heading, one body. Differentiate through weight/size
- **Line spacing**: 1.4-1.6x for readability at distance
- **Contrast**: WCAG AA minimum (4.5:1 ratio for normal text, 3:1 for large text)

### Color Theory

- **60-30-10 rule**: 60% dominant neutral, 30% secondary, 10% accent
- **Limit palette to 3-5 colors** maximum
- **Colorblind safety**: 8% of males have color vision deficiency — never rely on color alone to convey meaning
- **Dark backgrounds**: Use sparingly for emphasis (section dividers, quotes). Harder to read extended text

### Layout

- **16:9 widescreen** is the modern standard (not 4:3)
- **Grid-based layout**: Consistent margins, aligned elements
- **Rule of thirds**: Place key elements at grid intersections
- **Whitespace**: Professional decks use 40-60% whitespace. Novice decks use < 20%
- **Z-pattern / F-pattern**: Eye tracking shows readers scan top-left to bottom-right

### Data Visualization on Slides

- **One chart per slide** — never stack multiple charts
- **Annotate the insight** directly on the chart with a callout
- **Chart selection**: Bar (comparison), Line (trend), Pie (proportion, max 3-4 segments), Scatter (correlation)
- **Remove clutter**: No 3D, no unnecessary gridlines, no legend if labels can go directly on data
- **Highlight the story**: Gray out non-essential data, color the key series

### Accessibility

- **WCAG AA compliance**: 4.5:1 contrast for text, 3:1 for large text and graphics
- **Alt text**: For any shared digital versions
- **Font size minimums**: 18pt for any text
- **Color independence**: Use shape, pattern, or label in addition to color
- **Readable fonts**: Avoid thin weights, decorative faces

---

## 3. Presentation Scripting

### Narrative Frameworks

**Situation → Complication → Resolution** (Minto Pyramid):
- Situation: "Here's what's happening" (context the audience agrees with)
- Complication: "Here's the problem/opportunity" (creates tension)
- Resolution: "Here's what we should do" (your recommendation)

**Hero's Journey** (Nancy Duarte):
- Ordinary world → Call to adventure → Challenge → Transformation → Return with elixir

**Problem → Agitate → Solve** (Direct/Sales):
- State the problem, amplify the pain, present your solution

### Script Writing Rules

- **Write for the ear, not the eye**: Short sentences. Conversational. Use contractions
- **Never read the slide**: The script adds context, stories, and nuance
- **One idea per paragraph**: Mirror the one-idea-per-slide rule
- **Pacing**: ~150 words per minute for natural speaking. 2 minutes per content slide
- **Transitions**: Every slide needs a bridge sentence to the next ("So that brings us to...")
- **Pauses**: Mark strategic pauses after key statements for emphasis
- **Rule of Three**: Lists of three are memorable and rhythmic ("faster, cheaper, better")
- **Concrete over abstract**: "Revenue grew $4M" not "Revenue grew significantly"

### Timing Guidelines

| Duration | Content Slides | Opening | Core | Closing |
|----------|---------------|---------|------|---------|
| 5 min    | 5-7           | 30s     | 3.5min | 1min |
| 10 min   | 8-12          | 1min    | 7min | 2min   |
| 20 min   | 15-20         | 2min    | 15min | 3min  |
| 45 min   | 30-50         | 3min    | 35min | 7min  |

---

## 4. Technical Approaches

### HTML Slide Frameworks

**reveal.js** (Best overall):
- Most mature and widely used (40k+ GitHub stars)
- Rich feature set: speaker notes, PDF export, fragments, code highlighting
- Fully customizable with CSS
- Self-contained single-file output possible
- Keyboard navigation, touch support, overview mode
- Plugin ecosystem (math, charts, search)

**Slidev** (Best for developers):
- Markdown-based, Vue-powered
- Built-in code highlighting and live coding
- Recording and drawing capabilities
- Requires Node.js build step — not self-contained

**Marp** (Best for simplicity):
- Markdown to slides converter
- Very simple syntax
- Limited design customization
- Good for quick internal presentations

**impress.js** (Best for wow factor):
- Prezi-like 3D transformations
- Complex to author
- Can be disorienting if overused

**Recommendation**: reveal.js for maximum flexibility and professional output with zero server requirements.

### PDF Generation

1. **reveal.js print-pdf**: Built-in — append `?print-pdf` to URL, Ctrl+P, save as PDF. Reliable, zero dependencies
2. **Puppeteer/Playwright**: Automate headless Chrome to generate PDF from HTML. Highest quality, programmatic
3. **wkhtmltopdf**: Command-line HTML to PDF. Fast but less accurate CSS rendering than headless Chrome
4. **Recommendation**: reveal.js native print-pdf for manual workflow; Puppeteer for automated pipelines

### PowerPoint Generation

**PptxGenJS** (JavaScript — Best for web/Node.js):
- Pure JavaScript, works in browser and Node
- Rich API: shapes, charts, images, tables, speaker notes
- Active maintenance, good documentation
- Can generate .pptx files directly in the browser

**python-pptx** (Python — Best for data-heavy decks):
- Mature Python library
- Excellent for programmatic chart generation
- Template-based slide creation
- Strong community

**officegen** (Node.js):
- Generates PPTX, DOCX, XLSX
- Less actively maintained than PptxGenJS
- Simpler API but fewer features

**Recommendation**: PptxGenJS for JavaScript/web environments; python-pptx for Python/data science workflows.

### Format Comparison

| Format | Sharing | Editing | Offline | Quality | Interactivity |
|--------|---------|---------|---------|---------|---------------|
| HTML   | Web link, email | Source code | Yes (single file) | Highest (CSS control) | Full (animations, links, embeds) |
| PDF    | Universal | None (read-only) | Yes | High | None |
| PPTX   | Email, cloud | Full (PowerPoint/Slides) | Yes | Medium (limited CSS) | Basic (PowerPoint animations) |

---

## 5. Best-in-Class Slide Templates

### McKinsey-Style (Strategic/Executive)

- Clean, structured, data-heavy
- Heavy use of structured frameworks (2x2 matrices, waterfall charts, stacked bars)
- Assertion-evidence titles (full-sentence headlines that state the conclusion)
- Sources cited on every data slide
- Action-oriented language ("Invest in X to capture $YM opportunity")
- Limited use of imagery — data-first approach
- Precise, minimal color palette (navy + one accent)

### Apple Keynote-Style (Product/Launch)

- Extreme simplicity: one word or image per slide
- Full-bleed product photography on solid backgrounds
- Very large, bold typography (often just a number or short phrase)
- Cinematic transitions between major sections
- Dark backgrounds (emphasizes product on screen)
- Build drama through pacing: slow reveal, then big moment
- Minimal text — the speaker does the talking

### TED Talk-Style (Thought Leadership)

- Highly visual: full-bleed images, minimal text
- Personal stories illustrated with photographs
- Data shown simply (one number, one chart)
- Emotional arc: surprise → curiosity → empathy → call to action
- Slides support the speaker, never compete with them
- Often 60+ slides for 18 minutes (fast-paced visual storytelling)

### Common Layout Patterns Across All Styles

1. **Title Slide**: Minimal, bold, sets the tone
2. **Agenda/Overview**: 3-4 items max (often skipped in favor of narrative flow)
3. **Section Divider**: Clear visual break, resets audience attention
4. **Split Content**: 50/50 text and image — most versatile layout
5. **Data Slide**: One chart with annotated insight
6. **Quote Slide**: Large quote, minimal design
7. **Comparison**: Two-column parallel structure
8. **Big Number**: Statistical shock value
9. **Process/Timeline**: 3-6 step visual flow
10. **Summary/Recap**: Key takeaways (max 3 points)
11. **CTA/Closing**: What to do next — specific and actionable
12. **Appendix**: Backup data (numbered for easy reference in Q&A)
