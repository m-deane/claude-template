from __future__ import annotations
from pptx.slide import Slide
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN

from pptx_generator.config.colors import ColorPalette
from pptx_generator.config.typography import Typography
from pptx_generator.themes.base import BaseTheme
from pptx_generator.slides.base import BaseSlideBuilder


class ClosingSlideBuilder(BaseSlideBuilder):
    """Builder for closing/thank you slides."""

    @property
    def slide_type(self) -> str:
        return "closing"

    def _build_content(self, slide: Slide, theme: BaseTheme, palette: ColorPalette,
                       typography: Typography, **kwargs) -> None:
        """Build closing slide content."""
        title = kwargs.get('title', 'Thank You')
        message = kwargs.get('message', '')
        contact = kwargs.get('contact', '')

        # Add decorative element
        theme.add_decorative_element(slide, palette, element_type="corner")

        # Large centered title
        self._add_text_box(
            slide,
            left=Inches(1),
            top=Inches(2.5),
            width=Inches(11.333),
            height=Inches(1.5),
            text=title,
            font_spec=typography.title,
            alignment=PP_ALIGN.CENTER
        )

        # Optional message
        if message:
            self._add_text_box(
                slide,
                left=Inches(2),
                top=Inches(4.2),
                width=Inches(9.333),
                height=Inches(1),
                text=message,
                font_spec=typography.subtitle,
                color_hex=palette.text_light,
                alignment=PP_ALIGN.CENTER
            )

        # Optional contact info
        if contact:
            # Thin accent line above contact
            line = slide.shapes.add_shape(
                1,  # Line
                Inches(4),
                Inches(6),
                Inches(5.333),
                Inches(0)
            )
            line.line.color.rgb = palette.to_rgb(palette.accent)
            line.line.width = Pt(2)

            self._add_text_box(
                slide,
                left=Inches(2),
                top=Inches(6.3),
                width=Inches(9.333),
                height=Inches(0.6),
                text=contact,
                font_spec=typography.body,
                color_hex=palette.text_light,
                alignment=PP_ALIGN.CENTER
            )
