from __future__ import annotations
from pptx.slide import Slide
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN

from pptx_generator.config.colors import ColorPalette
from pptx_generator.config.typography import Typography
from pptx_generator.themes.base import BaseTheme
from pptx_generator.slides.base import BaseSlideBuilder


class ContentSlideBuilder(BaseSlideBuilder):
    """Builder for content slides with bullet points."""

    @property
    def slide_type(self) -> str:
        return "content"

    def _build_content(self, slide: Slide, theme: BaseTheme, palette: ColorPalette,
                       typography: Typography, **kwargs) -> None:
        """Build content slide with title and bullets."""
        title = kwargs.get('title', 'Content')
        bullets = kwargs.get('bullets', [])
        subtitle = kwargs.get('subtitle', '')

        # Title at top
        self._add_text_box(
            slide,
            left=Inches(0.5),
            top=Inches(0.5),
            width=Inches(12.333),
            height=Inches(0.7),
            text=title,
            font_spec=typography.heading,
            alignment=PP_ALIGN.LEFT
        )

        # Accent underline
        line = slide.shapes.add_shape(
            1,  # Line
            Inches(0.5),
            Inches(1.3),
            Inches(2.5),
            Inches(0)
        )
        line.line.color.rgb = palette.to_rgb(palette.accent)
        line.line.width = Pt(3)

        content_top = Inches(1.6)

        # Optional subtitle
        if subtitle:
            self._add_text_box(
                slide,
                left=Inches(0.5),
                top=content_top,
                width=Inches(12.333),
                height=Inches(0.5),
                text=subtitle,
                font_spec=typography.subheading,
                color_hex=palette.text_light,
                alignment=PP_ALIGN.LEFT
            )
            content_top = Inches(2.2)

        # Bullet points
        if bullets:
            self._add_bullet_list(
                slide,
                left=Inches(0.8),
                top=content_top,
                width=Inches(11.5),
                height=Inches(5.3 - content_top.inches),
                bullets=bullets,
                font_spec=typography.body,
                bullet_color_hex=palette.accent
            )
