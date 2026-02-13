from __future__ import annotations

from pydantic import BaseModel, Field


class BasePreset(BaseModel):
    """Presentation preset defining content structure and visual approach."""

    name: str
    description: str

    # Content density
    max_bullets_per_slide: int = 6
    max_words_per_bullet: int = 20
    words_per_slide_target: int = 80
    min_slides: int = 5
    max_slides: int = 30

    # Slide type weights (higher = more likely to be used)
    use_title_slide: bool = True
    use_agenda_slide: bool = True
    use_section_dividers: bool = True
    use_chart_slides: bool = True
    use_diagram_slides: bool = True
    use_timeline_slides: bool = False
    use_comparison_slides: bool = False
    use_quote_slides: bool = False
    use_closing_slide: bool = True

    # Visual element preferences
    chart_density: str = "medium"  # "low", "medium", "high"
    diagram_style: str = "flow"  # "flow", "hierarchy", "cycle", "matrix"
    infographic_style: str = "icon_stat"  # "icon_stat", "progress_bar", "number_highlight"

    # Recommended theme and palette
    recommended_theme: str = "corporate"
    recommended_palette: str = "corporate"
    recommended_font_stack: str = "professional"

    # Content transformation rules
    bullet_style: str = "concise"  # "concise", "detailed", "data_driven"
    title_style: str = "descriptive"  # "descriptive", "action_oriented", "question_based"

    def get_slide_sequence(self, section_count: int) -> list[str]:
        """Generate recommended slide type sequence based on section count.
        Returns list of slide type names."""
        sequence = []

        if self.use_title_slide:
            sequence.append("title")

        if self.use_agenda_slide and section_count > 3:
            sequence.append("agenda")

        for i in range(section_count):
            if self.use_section_dividers and i > 0:
                sequence.append("section_divider")

            sequence.append("content")

            # Intersperse visual slides based on preferences
            if self.use_chart_slides and i % 3 == 1:
                sequence.append("chart")

            if self.use_diagram_slides and i % 4 == 2:
                sequence.append("diagram")

            if self.use_timeline_slides and i % 5 == 3:
                sequence.append("timeline")

            if self.use_comparison_slides and i % 4 == 0 and i > 0:
                sequence.append("comparison")

        if self.use_closing_slide:
            sequence.append("closing")

        return sequence
