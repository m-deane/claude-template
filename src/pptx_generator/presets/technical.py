from __future__ import annotations

from pptx_generator.presets.base import BasePreset


class TechnicalPreset(BasePreset):
    """Technical presentation preset for detailed, data-heavy content.

    Characteristics:
    - High detail density with more bullets and words
    - Heavy emphasis on charts, diagrams, and comparisons
    - Hierarchical diagram style for system architectures
    - Detailed bullet style for comprehensive explanations
    """

    name: str = "technical"
    description: str = "Detailed technical presentations with charts, diagrams, and comprehensive explanations"

    # Content density - more detailed
    max_bullets_per_slide: int = 8
    max_words_per_bullet: int = 25
    words_per_slide_target: int = 120
    min_slides: int = 8
    max_slides: int = 40

    # Slide type preferences
    use_title_slide: bool = True
    use_agenda_slide: bool = True
    use_section_dividers: bool = True
    use_chart_slides: bool = True
    use_diagram_slides: bool = True
    use_timeline_slides: bool = True
    use_comparison_slides: bool = True
    use_quote_slides: bool = False
    use_closing_slide: bool = True

    # Visual preferences
    chart_density: str = "high"
    diagram_style: str = "hierarchy"
    infographic_style: str = "icon_stat"

    # Theme preferences
    recommended_theme: str = "modern"
    recommended_palette: str = "tech"
    recommended_font_stack: str = "technical"

    # Content style
    bullet_style: str = "detailed"
    title_style: str = "descriptive"
