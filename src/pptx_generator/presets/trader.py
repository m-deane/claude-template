from __future__ import annotations

from pptx_generator.presets.base import BasePreset


class TraderPreset(BasePreset):
    """Trader presentation preset for market-focused content.

    Characteristics:
    - Fast-paced, action-oriented content
    - High chart density for market data and trends
    - Timeline emphasis for temporal analysis
    - Minimal section dividers for quick flow
    - Dark theme for trading floor aesthetics
    """

    name: str = "trader"
    description: str = "Market-focused presentations with high chart density and action-oriented insights"

    # Content density - concise and focused
    max_bullets_per_slide: int = 5
    max_words_per_bullet: int = 15
    words_per_slide_target: int = 70
    min_slides: int = 5
    max_slides: int = 25

    # Slide type preferences - fast-paced flow
    use_title_slide: bool = True
    use_agenda_slide: bool = False
    use_section_dividers: bool = False
    use_chart_slides: bool = True
    use_diagram_slides: bool = True
    use_timeline_slides: bool = True
    use_comparison_slides: bool = True
    use_quote_slides: bool = False
    use_closing_slide: bool = True

    # Visual preferences - chart heavy
    chart_density: str = "high"
    diagram_style: str = "flow"
    infographic_style: str = "number_highlight"

    # Theme preferences - dark trading theme
    recommended_theme: str = "dark"
    recommended_palette: str = "finance"
    recommended_font_stack: str = "professional"

    # Content style
    bullet_style: str = "concise"
    title_style: str = "action_oriented"
