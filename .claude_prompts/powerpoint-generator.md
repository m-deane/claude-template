# PowerPoint Presentation Generator - Project Prompt & Reference

## Project Overview

**pptx-generator** is a Python-based PowerPoint presentation generator that transforms plain text, Markdown, and JSON input into professionally themed `.pptx` files. It supports audience-specific presets (technical, executive, analyst, trader, educational, summary), visual themes, color palettes, and a full library of slide types including charts, diagrams, timelines, and infographics.

**Technology Stack**: Python 3.10+, python-pptx, Click (CLI)
**Architecture**: Single-package modular architecture under `src/pptx_generator/`

---

## Quick Start

### Installation

```bash
# Create and activate virtual environment
python -m venv pptx-env
source pptx-env/bin/activate  # Linux/macOS
# pptx-env\Scripts\activate   # Windows

# Install in development mode
pip install -e ".[dev]"
```

### First Generation

```bash
# From a Markdown file with the technical preset
pptx-gen generate notes.md -p technical --theme modern -o my_talk.pptx

# From plain text with automatic parsing
pptx-gen generate notes.txt -t "Project Update" -p executive -o update.pptx
```

### Verify Installation

```bash
pptx-gen presets        # List all available presets
pptx-gen preview notes.md  # Preview slide structure without generating
```

---

## Package Structure

```
src/pptx_generator/
├── __init__.py
├── generator.py             # Main orchestrator (PresentationGenerator)
├── cli.py                   # Click-based CLI (pptx-gen)
├── config/                  # Configuration layer
│   ├── palettes.py          # 6 color palettes
│   ├── typography.py        # 4 font stacks
│   └── settings.py          # PresentationConfig dataclass
├── presets/                  # Audience presets
│   ├── technical.py
│   ├── executive.py
│   ├── analyst.py
│   ├── trader.py
│   ├── educational.py       # Also matched by "explain"
│   └── summary.py           # Also matched by "summarise"/"summarize"
├── themes/                  # Visual themes
│   ├── corporate.py
│   ├── modern.py
│   ├── dark.py
│   └── minimal.py
├── slides/                  # 9 slide builders
│   ├── title.py
│   ├── agenda.py
│   ├── section.py
│   ├── content.py
│   ├── comparison.py
│   ├── chart.py
│   ├── timeline.py
│   ├── diagram.py
│   └── closing.py
├── visuals/                 # Visual element renderers
│   ├── charts.py            # bar, line, pie, horizontal_bar
│   ├── diagrams.py          # flow, hierarchy, cycle, process_arrows
│   ├── infographics.py      # stat_cards, progress_bars, kpi_dashboards
│   └── shapes.py            # Reusable shape primitives
└── parsers/                 # Input format parsers
    ├── text_parser.py
    ├── markdown_parser.py
    └── json_parser.py
```

---

## Input Format Reference

### Plain Text (.txt)

The text parser splits input into slides by detecting structural patterns:
- Blank-line-separated paragraphs become individual content slides
- Lines in ALL CAPS or ending with `:` are treated as slide titles
- Bulleted lines (starting with `-`, `*`, or numbered) are grouped under the preceding title
- The first line or paragraph is used as the presentation title slide

```text
Q4 Financial Review

Revenue Performance
- Revenue grew 15% YoY to $4.2M
- Subscription revenue up 22%
- Professional services flat

Cost Structure
- Engineering headcount +3
- Infrastructure costs reduced 8%
- Marketing spend increased for product launch

Next Quarter Outlook
- Target: $4.8M revenue
- Key hire: VP of Sales
- Product launch: March 15
```

### Markdown (.md)

Structured mapping from Markdown elements to slide types:

| Markdown Element | Slide Mapping |
|------------------|---------------|
| `# Heading 1` | Title slide (first H1) or section divider |
| `## Heading 2` | New content slide title |
| `### Heading 3` | Subsection within current slide |
| `- bullet` / `* bullet` | Bullet points on current slide |
| `1. numbered` | Numbered list on current slide |
| Markdown table | Comparison slide (2 columns) or content table |
| `> blockquote` | Callout/highlight box |
| `**bold text**` | Emphasized text styling |
| `---` (horizontal rule) | Section break / new section divider |

```markdown
# Q4 Financial Review
## Presented by Finance Team

## Revenue Performance
- Revenue grew 15% YoY to **$4.2M**
- Subscription revenue up 22%
- Professional services flat

## Cost Comparison

| Category | Q3 | Q4 |
|----------|----|----|
| Engineering | $1.2M | $1.4M |
| Infrastructure | $800K | $736K |
| Marketing | $400K | $520K |

---

## Next Quarter Outlook
- Target: $4.8M revenue
- Key hire: VP of Sales
- Product launch: March 15

> Key risk: Supply chain delays may impact hardware product timeline
```

### JSON (.json)

Full structured control over every slide. Each slide object requires a `type` field and type-specific properties.

**Complete JSON Schema:**

```json
{
  "title": "Presentation Title",
  "subtitle": "Optional subtitle",
  "author": "Author Name",
  "slides": [
    {
      "type": "content",
      "title": "Slide Title",
      "bullets": ["Point 1", "Point 2", "Point 3"]
    },
    {
      "type": "chart",
      "title": "Revenue by Quarter",
      "chart_data": {
        "labels": ["Q1", "Q2", "Q3", "Q4"],
        "values": [100, 150, 130, 200],
        "chart_type": "bar"
      }
    },
    {
      "type": "comparison",
      "title": "Before vs After",
      "left_title": "Before",
      "left_bullets": ["Manual process", "3-day turnaround", "High error rate"],
      "right_title": "After",
      "right_bullets": ["Automated pipeline", "2-hour turnaround", "99.5% accuracy"]
    },
    {
      "type": "timeline",
      "title": "Project Roadmap",
      "events": [
        {"label": "Q1 2026", "description": "Foundation & core API"},
        {"label": "Q2 2026", "description": "Beta launch"},
        {"label": "Q3 2026", "description": "GA release"},
        {"label": "Q4 2026", "description": "Enterprise features"}
      ]
    },
    {
      "type": "diagram",
      "title": "Data Pipeline",
      "nodes": ["Ingest", "Validate", "Transform", "Load", "Monitor"],
      "diagram_type": "flow"
    },
    {
      "type": "section",
      "title": "Appendix"
    },
    {
      "type": "closing",
      "title": "Thank You",
      "contact": "team@company.com"
    }
  ]
}
```

**Slide Type Reference:**

| Type | Required Fields | Optional Fields |
|------|----------------|-----------------|
| `title` | `title` | `subtitle`, `author`, `date` |
| `agenda` | `title`, `items` | |
| `section` | `title` | `subtitle` |
| `content` | `title`, `bullets` | `notes` |
| `comparison` | `title`, `left_title`, `left_bullets`, `right_title`, `right_bullets` | |
| `chart` | `title`, `chart_data` | `notes` |
| `timeline` | `title`, `events` | |
| `diagram` | `title`, `nodes`, `diagram_type` | `connections` |
| `closing` | `title` | `contact`, `subtitle` |

**chart_data sub-fields:**

| Field | Type | Description |
|-------|------|-------------|
| `labels` | `list[str]` | Category labels for x-axis |
| `values` | `list[float]` or `list[list[float]]` | Single series or multi-series data |
| `chart_type` | `str` | One of: `bar`, `line`, `pie`, `horizontal_bar` |
| `series_names` | `list[str]` | Names for multi-series charts (optional) |

---

## Preset Reference

### technical

**Target audience**: Engineers, developers, technical staff
**Bullet density**: High -- up to 8 bullets per slide with detailed explanations
**Visual emphasis**: Charts and diagrams (flow diagrams, architecture diagrams, process arrows)
**Default theme**: modern
**Default palette**: tech
**Behavior**: Preserves technical detail. Does not simplify jargon. Includes code-style formatting where appropriate. Prefers diagrams over bullet summaries when structure is detected.

### executive

**Target audience**: C-suite, VPs, board members, management
**Bullet density**: Low -- maximum 4 bullets per slide, concise phrasing
**Visual emphasis**: Infographics, KPI dashboards, stat cards, key metric callouts
**Default theme**: corporate
**Default palette**: corporate (or finance)
**Behavior**: Aggressive simplification. Strips technical detail. Leads with outcomes and metrics. Promotes key numbers to visual callouts. Adds agenda and closing slides automatically.

### analyst

**Target audience**: Research analysts, data scientists, quantitative roles
**Bullet density**: High -- data-driven with supporting evidence
**Visual emphasis**: Charts (all types), comparison slides, timeline slides
**Default theme**: minimal
**Default palette**: finance
**Behavior**: Preserves data granularity. Generates chart slides from detected numeric patterns. Creates comparison slides from tabular data. Includes source attribution where detected.

### trader

**Target audience**: Traders, portfolio managers, market participants
**Bullet density**: Medium -- concise, action-oriented
**Visual emphasis**: Charts (line, bar), timeline slides, trend indicators
**Default theme**: dark
**Default palette**: finance
**Behavior**: Speed-oriented layout. High contrast for readability. Numeric data promoted to chart slides. Timeline events shown chronologically. Minimal decorative elements.

### educational (alias: explain)

**Target audience**: Students, learners, onboarding audiences
**Bullet density**: Medium -- step-by-step progressive disclosure
**Visual emphasis**: Flow diagrams, progress bars, cycle diagrams, process arrows
**Default theme**: modern
**Default palette**: (default)
**Behavior**: Breaks complex topics into sequential steps. Uses numbered progression. Adds section dividers between major topics. Prefers diagrams that show process and relationships.

### summary (alias: summarise, summarize)

**Target audience**: Quick overview consumers, stakeholders wanting highlights
**Bullet density**: Low -- condensed key points only
**Visual emphasis**: Minimal -- clean text-focused slides
**Default theme**: minimal
**Default palette**: (default)
**Behavior**: Aggressive condensation. Merges related points. Removes supporting detail, keeps conclusions. Targets fewest slides possible. No diagram or chart generation unless data is explicitly structured.

---

## Theme Reference

| Theme | Background | Text | Accent | Use Case |
|-------|-----------|------|--------|----------|
| `corporate` | White/light gray | Dark gray/black | Navy, dark blue | Formal business, board presentations |
| `modern` | White | Dark charcoal | Bright accent colors | Tech companies, product updates |
| `dark` | Dark gray/black | White/light gray | High-contrast accents | Trading floors, low-light, high-impact |
| `minimal` | White | Black | Single subtle accent | Research, academic, data-heavy |

## Palette Reference

Six color palettes are available. Each defines primary, secondary, accent, background, and text colors.

| Palette | Primary | Style | Best Paired With |
|---------|---------|-------|-----------------|
| `corporate` | Navy blue | Conservative, professional | corporate theme, executive preset |
| `tech` | Electric blue | Modern, high-energy | modern theme, technical preset |
| `finance` | Deep green | Data-focused, trustworthy | minimal/dark theme, analyst/trader preset |
| `creative` | Purple/magenta | Bold, expressive | modern theme |
| `earth` | Warm brown/olive | Natural, grounded | minimal theme |
| `mono` | Grayscale | Neutral, universal | minimal theme, summary preset |

## Typography Stacks

| Stack | Heading Font | Body Font | Use Case |
|-------|-------------|-----------|----------|
| `classic` | Georgia / serif | Times-style body | Formal, traditional |
| `modern` | Calibri / sans-serif | Segoe UI / Helvetica | General business |
| `technical` | Consolas / monospace headings | Calibri body | Technical, engineering |
| `clean` | Arial / Helvetica | Arial body | Minimal, universal |

---

## CLI Command Reference

### `pptx-gen generate`

Generate a presentation from an input file.

```bash
pptx-gen generate <INPUT_FILE> [OPTIONS]
```

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--preset` | `-p` | Audience preset name | `technical` |
| `--theme` | | Visual theme | Preset default |
| `--palette` | | Color palette | Preset default |
| `--title` | `-t` | Override presentation title | Parsed from input |
| `--subtitle` | | Override subtitle | None |
| `--author` | `-a` | Author name | None |
| `--font-stack` | | Typography stack | `modern` |
| `--output` | `-o` | Output file path | `output/presentation.pptx` |

**Examples:**

```bash
# Markdown input, technical audience, modern theme
pptx-gen generate research.md -p technical --theme modern --palette tech -o talk.pptx

# Plain text input, executive summary
pptx-gen generate notes.txt -t "Q4 Report" -p executive --palette finance

# JSON input, dark theme for trading desk
pptx-gen generate slides.json -p trader --theme dark -o market_update.pptx

# Educational step-by-step
pptx-gen generate tutorial.md -p educational --theme modern -o lesson.pptx

# Quick summary, minimal styling
pptx-gen generate brief.txt -p summary -o highlights.pptx
```

### `pptx-gen presets`

List all available presets with their descriptions.

```bash
pptx-gen presets
```

### `pptx-gen describe`

Show detailed configuration for a specific preset.

```bash
pptx-gen describe -p executive
```

### `pptx-gen preview`

Parse input and display the slide structure without generating a file. Useful for verifying how input will be interpreted.

```bash
pptx-gen preview research.md
```

Output shows slide count, types, and titles:

```
Slide 1: [title] "Q4 Financial Review"
Slide 2: [content] "Revenue Performance" (4 bullets)
Slide 3: [comparison] "Cost Comparison" (3 vs 3)
Slide 4: [section] "Outlook"
Slide 5: [content] "Next Quarter Outlook" (3 bullets)
Slide 6: [closing] "Thank You"
```

---

## Python API Reference

### PresentationConfig

Dataclass holding all generation settings.

```python
from pptx_generator import PresentationConfig

config = PresentationConfig(
    title="My Presentation",          # Required: presentation title
    subtitle="A deep dive",           # Optional: subtitle on title slide
    author="Author Name",             # Optional: author attribution
    preset_name="technical",          # Preset: technical|executive|analyst|trader|educational|summary
    theme_name="modern",              # Theme: corporate|modern|dark|minimal
    palette_name="tech",              # Palette: corporate|tech|finance|creative|earth|mono
    font_stack_name="modern",         # Font stack: classic|modern|technical|clean
)
```

### PresentationGenerator

Main orchestrator class. Accepts a `PresentationConfig` and provides four generation methods.

```python
from pptx_generator import PresentationGenerator, PresentationConfig

config = PresentationConfig(title="Demo", preset_name="executive")
gen = PresentationGenerator(config)
```

#### generate_from_file(input_path, output_path)

Auto-detects format from file extension (`.txt`, `.md`, `.json`) and generates.

```python
gen.generate_from_file("input/notes.md", "output/presentation.pptx")
```

#### generate_from_text(text, output_path)

Parses raw plain text content.

```python
raw = """
Project Status Update

Completed Items
- Database migration finished
- API v2 deployed to staging
- Load testing passed at 10K RPS

Blockers
- Auth service dependency not ready
- Design review pending for dashboard
"""
gen.generate_from_text(raw, "output/update.pptx")
```

#### generate_from_markdown(markdown_str, output_path)

Parses a Markdown string.

```python
md = """# Sprint Review
## Velocity
- Completed 34 story points
- Sprint goal: 30 points (exceeded)

## Demo Highlights
- New search feature with fuzzy matching
- Dashboard redesign live in staging

---

## Retrospective
- **Keep**: Daily standups working well
- **Improve**: PR review turnaround time
"""
gen.generate_from_markdown(md, "output/sprint_review.pptx")
```

#### generate_from_json(data, output_path)

Accepts a Python dict matching the JSON input schema.

```python
data = {
    "title": "Pipeline Architecture",
    "slides": [
        {
            "type": "diagram",
            "title": "Data Flow",
            "nodes": ["Source", "Ingest", "Transform", "Warehouse", "Dashboard"],
            "diagram_type": "flow"
        },
        {
            "type": "chart",
            "title": "Processing Latency",
            "chart_data": {
                "labels": ["Jan", "Feb", "Mar", "Apr"],
                "values": [120, 95, 80, 65],
                "chart_type": "line"
            }
        }
    ]
}
gen.generate_from_json(data, "output/architecture.pptx")
```

---

## Example Workflows

### 1. Convert Research Notes to Executive Presentation

You have detailed research notes and need a concise executive summary.

```bash
# Preview what the parser will produce
pptx-gen preview research_notes.md

# Generate with executive preset (auto-condenses, adds KPI callouts)
pptx-gen generate research_notes.md \
  -p executive \
  --theme corporate \
  --palette corporate \
  -t "Market Analysis - Q4 2026" \
  -a "Research Team" \
  -o output/exec_summary.pptx
```

### 2. Technical Architecture Review Deck

```bash
# JSON input gives full control over diagram and chart slides
pptx-gen generate architecture.json \
  -p technical \
  --theme modern \
  --palette tech \
  --font-stack technical \
  -o output/arch_review.pptx
```

### 3. Quick Team Update from Meeting Notes

```bash
# Plain text input, summary preset for minimal slides
pptx-gen generate meeting_notes.txt \
  -p summary \
  -t "Team Sync - Feb 13" \
  -o output/team_sync.pptx
```

### 4. Trading Desk Market Brief

```python
from pptx_generator import PresentationGenerator, PresentationConfig

config = PresentationConfig(
    title="Morning Market Brief",
    subtitle="Feb 13, 2026",
    preset_name="trader",
    theme_name="dark",
    palette_name="finance",
)
gen = PresentationGenerator(config)

data = {
    "title": "Morning Market Brief",
    "slides": [
        {
            "type": "chart",
            "title": "S&P 500 - 5 Day",
            "chart_data": {
                "labels": ["Mon", "Tue", "Wed", "Thu", "Fri"],
                "values": [5890, 5920, 5905, 5945, 5960],
                "chart_type": "line"
            }
        },
        {
            "type": "content",
            "title": "Key Levels",
            "bullets": [
                "Resistance: 5,980 (prior high)",
                "Support: 5,850 (20-day MA)",
                "Volume: Above average on up days"
            ]
        },
        {
            "type": "timeline",
            "title": "Catalysts This Week",
            "events": [
                {"label": "Tue", "description": "CPI release 8:30 ET"},
                {"label": "Wed", "description": "FOMC minutes"},
                {"label": "Fri", "description": "Opex"}
            ]
        }
    ]
}
gen.generate_from_json(data, "output/morning_brief.pptx")
```

### 5. Educational Onboarding Deck from Documentation

```bash
# Markdown docs converted to step-by-step educational deck
pptx-gen generate onboarding_guide.md \
  -p educational \
  --theme modern \
  -t "New Engineer Onboarding" \
  -o output/onboarding.pptx
```

### 6. Analyst Deep-Dive with Comparisons and Charts

```bash
pptx-gen generate analysis.md \
  -p analyst \
  --theme minimal \
  --palette finance \
  --font-stack clean \
  -o output/deep_dive.pptx
```

### 7. Batch Generation (Scripted)

```python
import os
from pptx_generator import PresentationGenerator, PresentationConfig

input_dir = "reports/"
output_dir = "output/decks/"
os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_dir):
    if filename.endswith(".md"):
        name = filename.replace(".md", "")
        config = PresentationConfig(
            title=name.replace("_", " ").title(),
            preset_name="executive",
            theme_name="corporate",
            palette_name="corporate",
        )
        gen = PresentationGenerator(config)
        gen.generate_from_file(
            os.path.join(input_dir, filename),
            os.path.join(output_dir, f"{name}.pptx"),
        )
        print(f"Generated: {name}.pptx")
```

---

## Customization Guide

### Adding a New Preset

1. Create `src/pptx_generator/presets/your_preset.py`:

```python
from pptx_generator.presets.base import PresetBase

class YourPreset(PresetBase):
    name = "your_preset"
    description = "Description of the target audience"

    # Slide behavior
    max_bullets_per_slide = 6
    bullet_style = "concise"          # "concise" | "detailed" | "telegraphic"
    auto_section_dividers = True
    auto_agenda = True
    auto_closing = True

    # Visual preferences
    default_theme = "modern"
    default_palette = "tech"
    preferred_visuals = ["charts", "diagrams"]  # What to auto-generate

    # Content transformation
    simplify_jargon = False
    promote_metrics = True            # Pull numbers into visual callouts
    merge_short_slides = False        # Combine slides with < 2 bullets
```

2. Register in `src/pptx_generator/presets/__init__.py`:

```python
from .your_preset import YourPreset
# Add to PRESETS dict
```

### Adding a New Theme

1. Create `src/pptx_generator/themes/your_theme.py`:

```python
from pptx_generator.themes.base import ThemeBase
from pptx.util import Pt, Emu
from pptx.dml.color import RGBColor

class YourTheme(ThemeBase):
    name = "your_theme"

    # Slide master settings
    background_color = RGBColor(0xFF, 0xFF, 0xFF)
    title_color = RGBColor(0x1A, 0x1A, 0x2E)
    body_color = RGBColor(0x33, 0x33, 0x33)
    accent_color = RGBColor(0x00, 0x7B, 0xFF)

    # Typography
    title_font_size = Pt(32)
    body_font_size = Pt(16)
    bullet_font_size = Pt(14)

    # Layout
    margin_left = Emu(914400)         # 1 inch
    margin_top = Emu(1371600)         # 1.5 inches
    content_width = Emu(7315200)      # 8 inches
```

2. Register in `src/pptx_generator/themes/__init__.py`.

### Adding a New Color Palette

Edit `src/pptx_generator/config/palettes.py`:

```python
PALETTES = {
    # ... existing palettes ...
    "your_palette": {
        "primary": "#1A1A2E",
        "secondary": "#16213E",
        "accent": "#0F3460",
        "highlight": "#E94560",
        "background": "#FFFFFF",
        "text": "#1A1A2E",
        "text_light": "#666666",
        "chart_colors": ["#0F3460", "#E94560", "#16213E", "#533483", "#2B9348"],
    },
}
```

### Adding a New Slide Builder

1. Create `src/pptx_generator/slides/your_slide.py`:

```python
from pptx_generator.slides.base import SlideBuilderBase

class YourSlideBuilder(SlideBuilderBase):
    slide_type = "your_type"

    def build(self, slide_data, theme, palette):
        """
        Args:
            slide_data: dict with slide-specific fields
            theme: ThemeBase instance
            palette: dict of color values
        Returns:
            pptx slide object
        """
        slide = self.presentation.slides.add_slide(self.layout)
        # Build slide content using slide_data
        return slide
```

2. Register in `src/pptx_generator/slides/__init__.py`.
3. Add the new type to the JSON schema and parser handling.

### Adding a New Chart Type

Edit `src/pptx_generator/visuals/charts.py` and add a rendering function following the existing pattern (bar, line, pie, horizontal_bar). Each chart function receives `chart_data`, `theme`, and `palette` arguments and returns positioned chart elements.

### Adding a New Font Stack

Edit `src/pptx_generator/config/typography.py`:

```python
FONT_STACKS = {
    # ... existing stacks ...
    "your_stack": {
        "heading": "Your Heading Font",
        "body": "Your Body Font",
        "mono": "Your Mono Font",
        "fallback": "Arial",
    },
}
```

---

## Testing

```bash
# Run full test suite
pytest tests/ -v

# Run specific test modules
pytest tests/test_parsers.py -v
pytest tests/test_presets.py -v
pytest tests/test_slides.py -v
pytest tests/test_generator.py -v

# Run with coverage
pytest tests/ --cov=src/pptx_generator --cov-report=term-missing
```

### Test file organization

```
tests/
├── test_parsers.py          # Input parsing: text, markdown, JSON
├── test_presets.py           # Preset configuration validation
├── test_themes.py            # Theme application
├── test_slides.py            # Individual slide builder output
├── test_visuals.py           # Chart, diagram, infographic rendering
├── test_generator.py         # End-to-end generation
├── test_cli.py               # CLI argument parsing and execution
└── fixtures/                 # Sample input files for testing
    ├── sample.txt
    ├── sample.md
    └── sample.json
```

---

## Common Tasks Reference

| Task | Command / Code |
|------|---------------|
| List presets | `pptx-gen presets` |
| Preview slide structure | `pptx-gen preview input.md` |
| Describe a preset | `pptx-gen describe -p executive` |
| Generate from Markdown | `pptx-gen generate input.md -p technical -o out.pptx` |
| Generate from JSON | `pptx-gen generate input.json -p analyst -o out.pptx` |
| Override title | `pptx-gen generate input.md -t "Custom Title" -o out.pptx` |
| Use dark theme | `pptx-gen generate input.md --theme dark -o out.pptx` |
| Change palette | `pptx-gen generate input.md --palette finance -o out.pptx` |
| Change fonts | `pptx-gen generate input.md --font-stack technical -o out.pptx` |
| Python API basic | `PresentationGenerator(config).generate_from_file(in, out)` |

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| "Unknown preset" error | Preset name misspelled | Run `pptx-gen presets` to see valid names |
| Empty slides generated | Parser did not detect structure | Use `pptx-gen preview` to check parsing; switch to JSON for full control |
| Charts not rendering | `chart_data` missing required fields | Verify `labels`, `values`, and `chart_type` are all present |
| Font not applied | Font not installed on system | python-pptx embeds font names but not font files; ensure the font is installed where the .pptx will be opened |
| Comparison slide shows as content | Markdown table not detected | Ensure table uses standard pipe syntax with header separator row |
| Too many slides | Preset bullet density is high | Switch to `summary` or `executive` preset to condense |
| Too few slides | Preset merging content aggressively | Switch to `technical` or `analyst` preset to preserve detail |
