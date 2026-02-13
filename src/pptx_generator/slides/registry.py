from __future__ import annotations
from pptx_generator.slides.base import BaseSlideBuilder

SLIDE_BUILDERS: dict[str, BaseSlideBuilder] = {}


def _register_defaults():
    """Register all default slide builders."""
    from .title import TitleSlideBuilder
    from .agenda import AgendaSlideBuilder
    from .section import SectionDividerBuilder
    from .content import ContentSlideBuilder
    from .comparison import ComparisonSlideBuilder
    from .chart_slide import ChartSlideBuilder
    from .timeline import TimelineSlideBuilder
    from .diagram import DiagramSlideBuilder
    from .closing import ClosingSlideBuilder

    for builder_cls in [
        TitleSlideBuilder,
        AgendaSlideBuilder,
        SectionDividerBuilder,
        ContentSlideBuilder,
        ComparisonSlideBuilder,
        ChartSlideBuilder,
        TimelineSlideBuilder,
        DiagramSlideBuilder,
        ClosingSlideBuilder
    ]:
        builder = builder_cls()
        SLIDE_BUILDERS[builder.slide_type] = builder


_register_defaults()
