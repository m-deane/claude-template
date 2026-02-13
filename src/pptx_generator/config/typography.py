from __future__ import annotations

from typing import Dict

from pydantic import BaseModel, Field


class FontSpec(BaseModel):
    """Font specification for text elements.

    Defines the complete styling for a text element including family,
    size, weight, and color.
    """

    family: str = Field(..., description="Font family name")
    size_pt: int = Field(..., description="Font size in points", gt=0)
    bold: bool = Field(default=False, description="Bold weight")
    italic: bool = Field(default=False, description="Italic style")
    color_hex: str | None = Field(
        default=None,
        description="Optional color override as hex string"
    )


class Typography(BaseModel):
    """Complete typography system for presentations.

    Defines font specifications for all text hierarchy levels.
    """

    title: FontSpec = Field(..., description="Main slide title")
    subtitle: FontSpec = Field(..., description="Slide subtitle")
    heading: FontSpec = Field(..., description="Section heading (H1)")
    subheading: FontSpec = Field(..., description="Subsection heading (H2)")
    body: FontSpec = Field(..., description="Body text / paragraphs")
    caption: FontSpec = Field(..., description="Captions and labels")
    footnote: FontSpec = Field(..., description="Footnotes and references")


FONT_STACKS: Dict[str, Dict[str, Dict]] = {
    "professional": {
        "title": {
            "family": "Calibri",
            "size_pt": 36,
            "bold": True,
            "italic": False,
            "color_hex": None,
        },
        "subtitle": {
            "family": "Calibri",
            "size_pt": 24,
            "bold": False,
            "italic": False,
            "color_hex": None,
        },
        "heading": {
            "family": "Calibri",
            "size_pt": 28,
            "bold": True,
            "italic": False,
            "color_hex": None,
        },
        "subheading": {
            "family": "Calibri",
            "size_pt": 20,
            "bold": True,
            "italic": False,
            "color_hex": None,
        },
        "body": {
            "family": "Calibri",
            "size_pt": 16,
            "bold": False,
            "italic": False,
            "color_hex": None,
        },
        "caption": {
            "family": "Calibri",
            "size_pt": 12,
            "bold": False,
            "italic": True,
            "color_hex": None,
        },
        "footnote": {
            "family": "Calibri",
            "size_pt": 10,
            "bold": False,
            "italic": False,
            "color_hex": None,
        },
    },
    "modern": {
        "title": {
            "family": "Segoe UI",
            "size_pt": 36,
            "bold": True,
            "italic": False,
            "color_hex": None,
        },
        "subtitle": {
            "family": "Segoe UI",
            "size_pt": 24,
            "bold": False,
            "italic": False,
            "color_hex": None,
        },
        "heading": {
            "family": "Segoe UI",
            "size_pt": 28,
            "bold": True,
            "italic": False,
            "color_hex": None,
        },
        "subheading": {
            "family": "Segoe UI Semibold",
            "size_pt": 20,
            "bold": False,
            "italic": False,
            "color_hex": None,
        },
        "body": {
            "family": "Segoe UI",
            "size_pt": 16,
            "bold": False,
            "italic": False,
            "color_hex": None,
        },
        "caption": {
            "family": "Segoe UI",
            "size_pt": 12,
            "bold": False,
            "italic": True,
            "color_hex": None,
        },
        "footnote": {
            "family": "Segoe UI",
            "size_pt": 10,
            "bold": False,
            "italic": False,
            "color_hex": None,
        },
    },
    "classic": {
        "title": {
            "family": "Georgia",
            "size_pt": 36,
            "bold": True,
            "italic": False,
            "color_hex": None,
        },
        "subtitle": {
            "family": "Georgia",
            "size_pt": 24,
            "bold": False,
            "italic": True,
            "color_hex": None,
        },
        "heading": {
            "family": "Georgia",
            "size_pt": 28,
            "bold": True,
            "italic": False,
            "color_hex": None,
        },
        "subheading": {
            "family": "Georgia",
            "size_pt": 20,
            "bold": True,
            "italic": False,
            "color_hex": None,
        },
        "body": {
            "family": "Times New Roman",
            "size_pt": 16,
            "bold": False,
            "italic": False,
            "color_hex": None,
        },
        "caption": {
            "family": "Times New Roman",
            "size_pt": 12,
            "bold": False,
            "italic": True,
            "color_hex": None,
        },
        "footnote": {
            "family": "Times New Roman",
            "size_pt": 10,
            "bold": False,
            "italic": False,
            "color_hex": None,
        },
    },
    "technical": {
        "title": {
            "family": "Consolas",
            "size_pt": 36,
            "bold": True,
            "italic": False,
            "color_hex": None,
        },
        "subtitle": {
            "family": "Consolas",
            "size_pt": 24,
            "bold": False,
            "italic": False,
            "color_hex": None,
        },
        "heading": {
            "family": "Consolas",
            "size_pt": 28,
            "bold": True,
            "italic": False,
            "color_hex": None,
        },
        "subheading": {
            "family": "Consolas",
            "size_pt": 20,
            "bold": True,
            "italic": False,
            "color_hex": None,
        },
        "body": {
            "family": "Calibri",
            "size_pt": 16,
            "bold": False,
            "italic": False,
            "color_hex": None,
        },
        "caption": {
            "family": "Courier New",
            "size_pt": 12,
            "bold": False,
            "italic": False,
            "color_hex": None,
        },
        "footnote": {
            "family": "Calibri",
            "size_pt": 10,
            "bold": False,
            "italic": False,
            "color_hex": None,
        },
    },
}
