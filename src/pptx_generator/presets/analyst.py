from __future__ import annotations

from pptx_generator.presets.base import BasePreset


class AnalystPreset(BasePreset):
    """Analyst presentation preset for data-driven insights.

    Characteristics:
    - Data-heavy content with emphasis on metrics and trends
    - High chart density with timelines and comparisons
    - Matrix diagrams for multi-dimensional analysis
    - Data-driven bullet style with supporting evidence
    """

    name: str = "analyst"
    description: str = "Data-driven analyst presentations with charts, metrics, and comparative analysis"

    # Content density - balanced but data-focused
    max_bullets_per_slide: int = 6
    max_words_per_bullet: int = 18
    words_per_slide_target: int = 100
    min_slides: int = 6
    max_slides: int = 35

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

    # Visual preferences - data visualization focus
    chart_density: str = "high"
    diagram_style: str = "matrix"
    infographic_style: str = "icon_stat"

    # Theme preferences
    recommended_theme: str = "minimal"
    recommended_palette: str = "finance"
    recommended_font_stack: str = "professional"

    # Content style
    bullet_style: str = "data_driven"
    title_style: str = "descriptive"
