"""Shared data models for presentation parsers.

This module defines the standardized internal representation used by all
parsers to represent presentation content before conversion to PowerPoint.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class SlideContent(BaseModel):
    """Content for a single slide.

    Supports multiple slide types with specialized content fields:
    - title: Title slide with subtitle
    - agenda: Agenda/overview slide
    - section_divider: Section separator
    - content: Standard content slide with bullets
    - comparison: Two-column comparison
    - chart: Data visualization
    - timeline: Sequential events
    - diagram: Flow or process diagram
    - closing: Final slide with contact info
    """

    slide_type: str = "content"
    title: str = ""
    subtitle: str = ""
    bullets: list[str] = Field(default_factory=list)

    # For comparison slides (two-column layout)
    left_title: str = ""
    left_bullets: list[str] = Field(default_factory=list)
    right_title: str = ""
    right_bullets: list[str] = Field(default_factory=list)

    # For chart slides
    chart_data: dict | None = None

    # For timeline slides
    events: list[dict] = Field(default_factory=list)

    # For diagram slides
    nodes: list[str] = Field(default_factory=list)
    diagram_type: str = "flow"

    # For closing slides
    contact: str = ""
    message: str = ""

    # Metadata
    section_number: int | None = None
    notes: str = ""


class ParsedPresentation(BaseModel):
    """Complete parsed presentation content.

    This is the unified output format from all parsers, containing all
    slides and metadata needed to generate a PowerPoint file.
    """

    title: str = "Untitled Presentation"
    subtitle: str = ""
    author: str = ""
    date: str = ""
    sections: list[SlideContent] = Field(default_factory=list)
    raw_text: str = ""
    metadata: dict = Field(default_factory=dict)
