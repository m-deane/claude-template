from __future__ import annotations

from pptx_generator.presets.base import BasePreset


class EducationalPreset(BasePreset):
    """Educational presentation preset for teaching and explanation.

    Characteristics:
    - Teaching-oriented with question-based titles
    - Flow diagrams and comparisons for concept illustration
    - Progress bar infographics for learning journeys
    - Detailed explanations with balanced density
    - More slides to break down complex concepts
    """

    name: str = "educational"
    description: str = "Educational presentations with clear explanations, diagrams, and progressive concept building"

    # Content density - balanced for learning
    max_bullets_per_slide: int = 5
    max_words_per_bullet: int = 20
    words_per_slide_target: int = 90
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

    # Visual preferences - diagram focused for learning
    chart_density: str = "medium"
    diagram_style: str = "flow"
    infographic_style: str = "progress_bar"

    # Theme preferences
    recommended_theme: str = "modern"
    recommended_palette: str = "modern"
    recommended_font_stack: str = "professional"

    # Content style
    bullet_style: str = "detailed"
    title_style: str = "question_based"
