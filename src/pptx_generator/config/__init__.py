"""Configuration models for PowerPoint presentation generator.

This package contains Pydantic v2 models for managing presentation styling,
layout, and settings.
"""

from .colors import ColorPalette, PALETTES
from .settings import PresentationConfig, SlideConfig
from .typography import FontSpec, Typography, FONT_STACKS

__all__ = [
    "ColorPalette",
    "PALETTES",
    "PresentationConfig",
    "SlideConfig",
    "FontSpec",
    "Typography",
    "FONT_STACKS",
]
