from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import click

from pptx_generator.config.settings import PresentationConfig
from pptx_generator.generator import PresentationGenerator


@click.group()
@click.version_option(version="0.1.0")
def main() -> None:
    """PPTX Generator - Professional PowerPoint presentation generator.

    Generate polished presentations from text, markdown, or JSON input
    with configurable themes, presets, and visual elements.
    """
    pass


@main.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('-o', '--output', default='output/presentation.pptx', help='Output file path')
@click.option('-t', '--title', default='', help='Presentation title')
@click.option('-s', '--subtitle', default='', help='Presentation subtitle')
@click.option('-a', '--author', default='', help='Author name')
@click.option('-p', '--preset', default='executive',
              type=click.Choice(['technical', 'executive', 'analyst', 'trader',
                                 'educational', 'explain', 'summary', 'summarise']),
              help='Audience preset')
@click.option('--theme', default='corporate',
              type=click.Choice(['corporate', 'modern', 'dark', 'minimal']),
              help='Visual theme')
@click.option('--palette', default='corporate',
              type=click.Choice(['corporate', 'modern', 'dark', 'minimal', 'finance', 'tech']),
              help='Color palette')
@click.option('--fonts', default='professional',
              type=click.Choice(['professional', 'modern', 'classic', 'technical']),
              help='Font stack')
@click.option('--no-slide-numbers', is_flag=True, help='Disable slide numbers')
@click.option('--no-agenda', is_flag=True, help='Disable agenda slide')
@click.option('--no-section-dividers', is_flag=True, help='Disable section dividers')
def generate(
    input_file: str,
    output: str,
    title: str,
    subtitle: str,
    author: str,
    preset: str,
    theme: str,
    palette: str,
    fonts: str,
    no_slide_numbers: bool,
    no_agenda: bool,
    no_section_dividers: bool,
) -> None:
    """Generate a presentation from INPUT_FILE.

    Supports .txt, .md, .markdown, and .json input files.
    Auto-detects format from file extension.

    Examples:

      pptx-gen generate notes.md -p technical --theme modern

      pptx-gen generate research.txt -t "Q4 Report" -p analyst --palette finance

      pptx-gen generate slides.json -o report.pptx --theme dark
    """
    try:
        input_path = Path(input_file)

        # Validate input file
        if not input_path.exists():
            click.echo(click.style(f"Error: Input file '{input_file}' not found.", fg='red'), err=True)
            sys.exit(1)

        # Detect file type
        suffix = input_path.suffix.lower()
        supported_formats = {'.txt', '.md', '.markdown', '.json'}

        if suffix not in supported_formats:
            click.echo(
                click.style(
                    f"Error: Unsupported file format '{suffix}'. "
                    f"Supported formats: {', '.join(supported_formats)}",
                    fg='red'
                ),
                err=True
            )
            sys.exit(1)

        # Build configuration
        config = PresentationConfig(
            title=title or input_path.stem.replace('_', ' ').replace('-', ' ').title(),
            subtitle=subtitle,
            author=author,
            palette_name=palette,
            font_stack_name=fonts,
            theme_name=theme,
            preset_name=preset,
            include_slide_numbers=not no_slide_numbers,
            include_agenda=not no_agenda,
            include_section_dividers=not no_section_dividers,
        )

        # Display configuration
        click.echo(click.style("\nGenerating presentation...", fg='cyan', bold=True))
        click.echo(f"  Input:  {input_path}")
        click.echo(f"  Output: {output}")
        click.echo(f"  Title:  {config.title}")
        if config.subtitle:
            click.echo(f"  Subtitle: {config.subtitle}")
        if config.author:
            click.echo(f"  Author: {config.author}")
        click.echo(f"  Preset: {preset}")
        click.echo(f"  Theme:  {theme}")
        click.echo(f"  Palette: {palette}")
        click.echo(f"  Fonts:  {fonts}")
        click.echo()

        # Create generator
        generator = PresentationGenerator(config=config)

        # Generate presentation
        with click.progressbar(
            length=100,
            label=click.style('Processing', fg='green'),
            show_percent=True,
            show_pos=False
        ) as bar:
            bar.update(20)
            output_path = generator.generate_from_file(str(input_path), output)
            bar.update(80)

        # Success message
        click.echo()
        click.echo(click.style("✓ Presentation generated successfully!", fg='green', bold=True))
        click.echo(f"  Output: {output_path}")
        click.echo()

    except FileNotFoundError as e:
        click.echo(click.style(f"Error: File not found - {e}", fg='red'), err=True)
        sys.exit(1)
    except ValueError as e:
        click.echo(click.style(f"Error: Invalid configuration - {e}", fg='red'), err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(click.style(f"Error: {e}", fg='red'), err=True)
        sys.exit(1)


@main.command()
@click.option('-p', '--preset', default='executive',
              type=click.Choice(['technical', 'executive', 'analyst', 'trader',
                                 'educational', 'explain', 'summary', 'summarise']),
              help='Preset to describe')
def describe(preset: str) -> None:
    """Show details about a preset configuration.

    Displays the content density, visual preferences, and recommended
    theme settings for a specific preset.
    """
    from pptx_generator.config.presets import preset_registry

    # Normalize preset name (summary/summarise both map to summary)
    normalized_preset = 'summary' if preset == 'summarise' else preset

    preset_config = preset_registry.get(normalized_preset)

    if not preset_config:
        click.echo(click.style(f"Error: Preset '{preset}' not found.", fg='red'), err=True)
        sys.exit(1)

    click.echo()
    click.echo(click.style(f"Preset: {preset.upper()}", fg='cyan', bold=True))
    click.echo(click.style("=" * 60, fg='cyan'))
    click.echo()

    # Description
    descriptions = {
        'technical': 'Detailed technical documentation with code examples and diagrams',
        'executive': 'High-level strategic overview with key insights and recommendations',
        'analyst': 'Data-driven analysis with charts, metrics, and detailed findings',
        'trader': 'Market analysis with real-time data, trends, and trading signals',
        'educational': 'Learning-focused content with clear explanations and examples',
        'explain': 'Deep-dive explanations with step-by-step breakdowns',
        'summary': 'Concise overview hitting only the key points',
    }

    click.echo(click.style("Description:", fg='yellow'))
    click.echo(f"  {descriptions.get(normalized_preset, 'Custom preset configuration')}")
    click.echo()

    # Content settings
    click.echo(click.style("Content Settings:", fg='yellow'))
    click.echo(f"  Max bullets per slide:  {preset_config.max_bullets_per_slide}")
    click.echo(f"  Max words per bullet:   {preset_config.max_words_per_bullet}")
    click.echo(f"  Include agenda:         {preset_config.include_agenda}")
    click.echo(f"  Include section dividers: {preset_config.include_section_dividers}")
    click.echo(f"  Include slide numbers:  {preset_config.include_slide_numbers}")
    click.echo()

    # Visual settings
    click.echo(click.style("Visual Settings:", fg='yellow'))
    click.echo(f"  Theme:   {preset_config.theme_name}")
    click.echo(f"  Palette: {preset_config.palette_name}")
    click.echo(f"  Fonts:   {preset_config.font_stack_name}")
    click.echo()

    # Slide configuration details
    if hasattr(preset_config, 'slide_config'):
        slide_cfg = preset_config.slide_config
        click.echo(click.style("Slide Configuration:", fg='yellow'))
        click.echo(f"  Title font size:    {slide_cfg.title_font_size}pt")
        click.echo(f"  Body font size:     {slide_cfg.body_font_size}pt")
        click.echo(f"  Margins:            {slide_cfg.margin_left:.2f}\" (L/R), "
                   f"{slide_cfg.margin_top:.2f}\" (T/B)")
        click.echo()

    # Recommended use cases
    click.echo(click.style("Recommended For:", fg='yellow'))
    use_cases = {
        'technical': [
            'Technical documentation',
            'Architecture presentations',
            'Developer training',
            'Code reviews',
        ],
        'executive': [
            'Board presentations',
            'Strategic planning',
            'Quarterly business reviews',
            'Investor pitches',
        ],
        'analyst': [
            'Data analysis reports',
            'Research findings',
            'Performance reviews',
            'Market research',
        ],
        'trader': [
            'Trading strategies',
            'Market analysis',
            'Portfolio reviews',
            'Risk assessments',
        ],
        'educational': [
            'Training materials',
            'Course content',
            'Workshops',
            'Tutorials',
        ],
        'explain': [
            'Concept explanations',
            'Process documentation',
            'How-to guides',
            'Knowledge transfer',
        ],
        'summary': [
            'Executive summaries',
            'Quick overviews',
            'Meeting recaps',
            'Brief updates',
        ],
    }

    for use_case in use_cases.get(normalized_preset, []):
        click.echo(f"  • {use_case}")
    click.echo()


@main.command()
def presets() -> None:
    """List all available presets with descriptions."""
    from pptx_generator.config.presets import preset_registry

    click.echo()
    click.echo(click.style("Available Presets", fg='cyan', bold=True))
    click.echo(click.style("=" * 60, fg='cyan'))
    click.echo()

    preset_descriptions = {
        'technical': 'Detailed technical documentation with code and diagrams',
        'executive': 'High-level strategic overview for leadership',
        'analyst': 'Data-driven analysis with charts and metrics',
        'trader': 'Market analysis with real-time data and trends',
        'educational': 'Learning-focused content with clear explanations',
        'explain': 'Deep-dive explanations with step-by-step breakdowns',
        'summary': 'Concise overview hitting only key points',
    }

    for preset_name in sorted(preset_registry.keys()):
        description = preset_descriptions.get(preset_name, 'Custom preset')
        click.echo(click.style(f"{preset_name:15}", fg='yellow', bold=True) + f" {description}")

    click.echo()
    click.echo(click.style("Aliases:", fg='cyan'))
    click.echo(f"  {'summarise':15} → summary")
    click.echo()
    click.echo("Use 'pptx-gen describe --preset <name>' for detailed information.")
    click.echo()


@main.command()
def themes() -> None:
    """List all available themes."""
    from pptx_generator.config.themes import theme_registry

    click.echo()
    click.echo(click.style("Available Themes", fg='cyan', bold=True))
    click.echo(click.style("=" * 60, fg='cyan'))
    click.echo()

    theme_descriptions = {
        'corporate': 'Professional corporate style with clean lines',
        'modern': 'Contemporary design with bold elements',
        'dark': 'Dark background with high contrast',
        'minimal': 'Minimalist design with maximum whitespace',
    }

    for theme_name in sorted(theme_registry.keys()):
        theme_config = theme_registry[theme_name]
        description = theme_descriptions.get(theme_name, 'Custom theme')

        click.echo(click.style(f"{theme_name:15}", fg='yellow', bold=True) + f" {description}")

        # Show some key characteristics
        if hasattr(theme_config, 'slide_config'):
            click.echo(f"  {'':15} Title: {theme_config.slide_config.title_font_size}pt, "
                      f"Body: {theme_config.slide_config.body_font_size}pt")

    click.echo()
    click.echo(click.style("Available Palettes:", fg='cyan'))
    palettes = ['corporate', 'modern', 'dark', 'minimal', 'finance', 'tech']
    for palette in palettes:
        click.echo(f"  • {palette}")

    click.echo()
    click.echo(click.style("Available Font Stacks:", fg='cyan'))
    fonts = ['professional', 'modern', 'classic', 'technical']
    for font in fonts:
        click.echo(f"  • {font}")

    click.echo()


@main.command()
@click.argument('input_file', type=click.Path(exists=True), required=False)
@click.option('--text', '-t', default=None, help='Direct text input')
@click.option('-p', '--preset', default='executive',
              type=click.Choice(['technical', 'executive', 'analyst', 'trader',
                                 'educational', 'explain', 'summary', 'summarise']),
              help='Preset for parsing')
def preview(input_file: str | None, text: str | None, preset: str) -> None:
    """Preview how input will be parsed into slides (dry run).

    Shows the planned slide structure without generating the PPTX file.

    Examples:

      pptx-gen preview notes.md

      pptx-gen preview --text "Key Points:\\n- Point 1\\n- Point 2"
    """
    if not input_file and not text:
        click.echo(click.style("Error: Provide either INPUT_FILE or --text option.", fg='red'), err=True)
        sys.exit(1)

    if input_file and text:
        click.echo(click.style("Error: Provide either INPUT_FILE or --text, not both.", fg='red'), err=True)
        sys.exit(1)

    try:
        # Read input content
        if input_file:
            input_path = Path(input_file)
            if not input_path.exists():
                click.echo(click.style(f"Error: File '{input_file}' not found.", fg='red'), err=True)
                sys.exit(1)

            content = input_path.read_text(encoding='utf-8')
            source = str(input_path)
        else:
            content = text or ""
            source = "direct text input"

        # Parse content into slide structure
        from pptx_generator.parser import ContentParser
        from pptx_generator.config.presets import preset_registry

        normalized_preset = 'summary' if preset == 'summarise' else preset
        preset_config = preset_registry.get(normalized_preset, preset_registry['executive'])

        parser = ContentParser(preset_config)
        slides = parser.parse(content)

        # Display preview
        click.echo()
        click.echo(click.style("Slide Preview", fg='cyan', bold=True))
        click.echo(click.style("=" * 60, fg='cyan'))
        click.echo(f"Source: {source}")
        click.echo(f"Preset: {preset}")
        click.echo(f"Total slides: {len(slides)}")
        click.echo()

        for idx, slide in enumerate(slides, 1):
            slide_type = slide.get('type', 'content')
            title = slide.get('title', 'Untitled')

            # Color code by slide type
            if slide_type == 'title':
                type_color = 'magenta'
                type_label = 'TITLE'
            elif slide_type == 'section':
                type_color = 'blue'
                type_label = 'SECTION'
            elif slide_type == 'agenda':
                type_color = 'cyan'
                type_label = 'AGENDA'
            else:
                type_color = 'green'
                type_label = 'CONTENT'

            click.echo(click.style(f"Slide {idx}: ", fg='yellow', bold=True) +
                      click.style(f"[{type_label}] ", fg=type_color) +
                      click.style(title, bold=True))

            # Show content preview
            if 'content' in slide and slide['content']:
                content_items = slide['content']
                if isinstance(content_items, list):
                    for item in content_items[:3]:  # Show first 3 items
                        item_text = str(item)[:70]  # Truncate long items
                        if len(str(item)) > 70:
                            item_text += "..."
                        click.echo(f"    • {item_text}")

                    if len(content_items) > 3:
                        click.echo(f"    ... and {len(content_items) - 3} more items")
                else:
                    content_preview = str(content_items)[:100]
                    if len(str(content_items)) > 100:
                        content_preview += "..."
                    click.echo(f"    {content_preview}")

            click.echo()

        click.echo(click.style("Preview complete. ", fg='green') +
                  "Use 'generate' command to create the actual presentation.")
        click.echo()

    except Exception as e:
        click.echo(click.style(f"Error: {e}", fg='red'), err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
