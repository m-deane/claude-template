"""Unit conversion utilities for python-pptx EMU calculations.

This module provides helper functions for converting common units (inches, points,
centimeters, percentages) to EMU (English Metric Units) used by python-pptx.

EMU conversion factors:
- 1 inch = 914400 EMU
- 1 point = 12700 EMU
- 1 cm = 360000 EMU
"""

from __future__ import annotations

from pptx.util import Emu, Inches, Pt

# Re-export python-pptx utilities for convenience
__all__ = ["inches", "pt", "cm", "pct_of_width", "pct_of_height", "Inches", "Pt", "Emu"]

# EMU conversion constants
EMU_PER_INCH = 914400
EMU_PER_POINT = 12700
EMU_PER_CM = 360000

# Default PowerPoint slide dimensions (standard 16:9 widescreen)
DEFAULT_SLIDE_WIDTH_INCHES = 13.333
DEFAULT_SLIDE_HEIGHT_INCHES = 7.5


def inches(val: float) -> int:
    """Convert inches to EMU (English Metric Units).

    Args:
        val: Value in inches

    Returns:
        Equivalent value in EMU (914400 EMU per inch)

    Examples:
        >>> inches(1.0)
        914400
        >>> inches(2.5)
        2286000
    """
    return int(val * EMU_PER_INCH)


def pt(val: float) -> int:
    """Convert points to EMU (English Metric Units).

    Args:
        val: Value in points

    Returns:
        Equivalent value in EMU (12700 EMU per point)

    Examples:
        >>> pt(12)
        152400
        >>> pt(18.5)
        234950
    """
    return int(val * EMU_PER_POINT)


def cm(val: float) -> int:
    """Convert centimeters to EMU (English Metric Units).

    Args:
        val: Value in centimeters

    Returns:
        Equivalent value in EMU (360000 EMU per cm)

    Examples:
        >>> cm(1.0)
        360000
        >>> cm(5.5)
        1980000
    """
    return int(val * EMU_PER_CM)


def pct_of_width(pct: float, slide_width_inches: float = DEFAULT_SLIDE_WIDTH_INCHES) -> int:
    """Convert percentage of slide width to EMU.

    Useful for positioning elements as a percentage of total slide width.

    Args:
        pct: Percentage value (0-100)
        slide_width_inches: Width of slide in inches (default: 13.333 for 16:9)

    Returns:
        Equivalent value in EMU

    Examples:
        >>> pct_of_width(50)  # 50% of default slide width
        6095964
        >>> pct_of_width(25, slide_width_inches=10)  # 25% of 10 inch width
        2286000
    """
    if not 0 <= pct <= 100:
        raise ValueError(f"Percentage must be between 0 and 100, got {pct}")
    if slide_width_inches <= 0:
        raise ValueError(f"Slide width must be positive, got {slide_width_inches}")

    return int((pct / 100.0) * slide_width_inches * EMU_PER_INCH)


def pct_of_height(pct: float, slide_height_inches: float = DEFAULT_SLIDE_HEIGHT_INCHES) -> int:
    """Convert percentage of slide height to EMU.

    Useful for positioning elements as a percentage of total slide height.

    Args:
        pct: Percentage value (0-100)
        slide_height_inches: Height of slide in inches (default: 7.5 for 16:9)

    Returns:
        Equivalent value in EMU

    Examples:
        >>> pct_of_height(50)  # 50% of default slide height
        3429000
        >>> pct_of_height(75, slide_height_inches=10)  # 75% of 10 inch height
        6858000
    """
    if not 0 <= pct <= 100:
        raise ValueError(f"Percentage must be between 0 and 100, got {pct}")
    if slide_height_inches <= 0:
        raise ValueError(f"Slide height must be positive, got {slide_height_inches}")

    return int((pct / 100.0) * slide_height_inches * EMU_PER_INCH)
