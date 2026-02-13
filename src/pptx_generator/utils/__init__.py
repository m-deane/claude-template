"""Utility modules for PowerPoint presentation generation.

This package provides helper functions for unit conversion and text processing
when working with python-pptx.
"""

from __future__ import annotations

from .text import (
    clean_text,
    estimate_slide_count,
    extract_title,
    split_into_bullets,
    split_into_sections,
    truncate,
)
from .units import Emu, Inches, Pt, cm, inches, pct_of_height, pct_of_width, pt

__all__ = [
    # Text utilities
    "split_into_bullets",
    "truncate",
    "extract_title",
    "estimate_slide_count",
    "clean_text",
    "split_into_sections",
    # Unit utilities
    "inches",
    "pt",
    "cm",
    "pct_of_width",
    "pct_of_height",
    "Inches",
    "Pt",
    "Emu",
]
