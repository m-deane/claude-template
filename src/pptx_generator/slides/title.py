from __future__ import annotations
from pptx.slide import Slide
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN

from pptx_generator.config.colors import ColorPalette
from pptx_generator.config.typography import Typography
from pptx_generator.themes.base import BaseTheme
from pptx_generator.slides.base import BaseSlideBuilder


class TitleSlideBuilder(BaseSlideBuilder):
    """Builder for title/cover slides."""

    @property
    def slide_type(self) -> str:
        return "title"

    def _build_content(self, slide: Slide, theme: BaseTheme, palette: ColorPalette,
                       typography: Typography, **kwargs) -> None:
        """Build title slide content."""
        title = kwargs.get('title', 'Presentation Title')
        subtitle = kwargs.get('subtitle', '')
        author = kwargs.get('author', '')
        date = kwargs.get('date', '')

        # Add accent bar on left
        theme.add_accent_bar(slide, palette, position="left")

        # Main title - large and centered in upper portion
        self._add_text_box(
            slide,
            left=Inches(1.5),
            top=Inches(2),
            width=Inches(10),
            height=Inches(1.5),
            text=title,
            font_spec=typography.title,
            alignment=PP_ALIGN.CENTER
        )

        # Subtitle - lighter color
        if subtitle:
            self._add_text_box(
                slide,
                left=Inches(1.5),
                top=Inches(3.7),
                width=Inches(10),
                height=Inches(0.8),
                text=subtitle,
                font_spec=typography.subtitle,
                color_hex=palette.text_light,
                alignment=PP_ALIGN.CENTER
            )

        # Thin accent line separator
        if author or date:
            line = slide.shapes.add_shape(
                1,  # Line shape
                Inches(4),
                Inches(5.5),
                Inches(5.333),
                Inches(0)
            )
            line.line.color.rgb = palette.to_rgb(palette.accent)
            line.line.width = Pt(2)

        # Author and date
        bottom_top = Inches(5.8)
        if author:
            self._add_text_box(
                slide,
                left=Inches(2),
                top=bottom_top,
                width=Inches(9.333),
                height=Inches(0.5),
                text=author,
                font_spec=typography.body,
                color_hex=palette.text_light,
                alignment=PP_ALIGN.CENTER
            )

        if date:
            self._add_text_box(
                slide,
                left=Inches(2),
                top=bottom_top + Inches(0.5),
                width=Inches(9.333),
                height=Inches(0.4),
                text=date,
                font_spec=typography.caption,
                color_hex=palette.text_light,
                alignment=PP_ALIGN.CENTER
            )
