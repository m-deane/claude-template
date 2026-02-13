from __future__ import annotations
from pptx.slide import Slide
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN

from pptx_generator.config.colors import ColorPalette
from pptx_generator.config.typography import Typography
from pptx_generator.themes.base import BaseTheme
from pptx_generator.slides.base import BaseSlideBuilder


class SectionDividerBuilder(BaseSlideBuilder):
    """Builder for section divider slides."""

    @property
    def slide_type(self) -> str:
        return "section"

    def _build_content(self, slide: Slide, theme: BaseTheme, palette: ColorPalette,
                       typography: Typography, **kwargs) -> None:
        """Build section divider content."""
        title = kwargs.get('title', 'Section Title')
        section_number = kwargs.get('section_number', None)

        # Add decorative element
        theme.add_decorative_element(slide, palette, element_type="corner")

        # Large section number if provided (background element)
        if section_number is not None:
            number_text = str(section_number)
            # Create large semi-transparent number
            from pptx_generator.config.typography import FontSpec
            number_font = FontSpec(
                family=typography.title.family,
                size_pt=180,
                bold=True,
                italic=False,
                color_hex=palette.accent
            )
            num_box = self._add_text_box(
                slide,
                left=Inches(8),
                top=Inches(1.5),
                width=Inches(4),
                height=Inches(3),
                text=number_text,
                font_spec=number_font,
                alignment=PP_ALIGN.CENTER
            )
            # Set transparency on the number
            num_box.fill.solid()
            num_box.fill.fore_color.rgb = palette.to_rgb(palette.accent)
            num_box.fill.transparency = 0.85

        # Large centered section title
        self._add_text_box(
            slide,
            left=Inches(1),
            top=Inches(2.5),
            width=Inches(11.333),
            height=Inches(2),
            text=title,
            font_spec=typography.title,
            alignment=PP_ALIGN.CENTER
        )

        # Accent bar at bottom
        bar = slide.shapes.add_shape(
            1,  # Line
            Inches(3),
            Inches(6.5),
            Inches(7.333),
            Inches(0)
        )
        bar.line.color.rgb = palette.to_rgb(palette.accent)
        bar.line.width = Pt(4)
