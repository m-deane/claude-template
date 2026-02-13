"""Visual themes for presentations."""

from __future__ import annotations

from pptx_generator.themes.base import BaseTheme
from pptx_generator.themes.corporate import CorporateTheme
from pptx_generator.themes.dark import DarkTheme
from pptx_generator.themes.minimal import MinimalTheme
from pptx_generator.themes.modern import ModernTheme
from pptx_generator.themes.registry import (
    THEME_REGISTRY,
    get_theme,
    list_available_themes,
    register_theme,
)

__all__ = [
    "BaseTheme",
    "CorporateTheme",
    "DarkTheme",
    "MinimalTheme",
    "ModernTheme",
    "THEME_REGISTRY",
    "get_theme",
    "list_available_themes",
    "register_theme",
]
