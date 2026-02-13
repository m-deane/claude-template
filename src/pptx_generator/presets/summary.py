from __future__ import annotations

from pptx_generator.presets.base import BasePreset


class SummaryPreset(BasePreset):
    """Summary presentation preset for condensed overviews.

    Characteristics:
    - Highly condensed with minimal slides
    - Low chart density, focus on key points
    - No section dividers or agenda (keep it short)
    - Action-oriented titles and concise bullets
    - Minimal visual complexity
    """

    name: str = "summary"
    description: str = "Condensed summary presentations with key points and minimal visual complexity"

    # Content density - condensed
    max_bullets_per_slide: int = 5
    max_words_per_bullet: int = 15
    words_per_slide_target: int = 60
    min_slides: int = 3
    max_slides: int = 12

    # Slide type preferences - minimal structure
    use_title_slide: bool = True
    use_agenda_slide: bool = False
    use_section_dividers: bool = False
    use_chart_slides: bool = True
    use_diagram_slides: bool = False
    use_timeline_slides: bool = False
    use_comparison_slides: bool = False
    use_quote_slides: bool = False
    use_closing_slide: bool = True

    # Visual preferences - minimal
    chart_density: str = "low"
    diagram_style: str = "flow"
    infographic_style: str = "number_highlight"

    # Theme preferences
    recommended_theme: str = "minimal"
    recommended_palette: str = "minimal"
    recommended_font_stack: str = "professional"

    # Content style
    bullet_style: str = "concise"
    title_style: str = "action_oriented"
