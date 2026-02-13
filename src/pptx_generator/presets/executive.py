from __future__ import annotations

from pptx_generator.presets.base import BasePreset


class ExecutivePreset(BasePreset):
    """Executive presentation preset for high-level strategic content.

    Characteristics:
    - Low content density with minimal text
    - Action-oriented titles and concise bullets
    - Focus on key insights and takeaways
    - Number highlights and visual impact over detailed charts
    """

    name: str = "executive"
    description: str = "Executive-level presentations with concise messaging and high visual impact"

    # Content density - minimal text
    max_bullets_per_slide: int = 4
    max_words_per_bullet: int = 12
    words_per_slide_target: int = 50
    min_slides: int = 5
    max_slides: int = 20

    # Slide type preferences
    use_title_slide: bool = True
    use_agenda_slide: bool = True
    use_section_dividers: bool = True
    use_chart_slides: bool = True
    use_diagram_slides: bool = True
    use_timeline_slides: bool = False
    use_comparison_slides: bool = False
    use_quote_slides: bool = True
    use_closing_slide: bool = True

    # Visual preferences - emphasis on infographics
    chart_density: str = "low"
    diagram_style: str = "flow"
    infographic_style: str = "number_highlight"

    # Theme preferences
    recommended_theme: str = "corporate"
    recommended_palette: str = "corporate"
    recommended_font_stack: str = "professional"

    # Content style
    bullet_style: str = "concise"
    title_style: str = "action_oriented"
