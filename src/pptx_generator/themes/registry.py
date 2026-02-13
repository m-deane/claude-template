"""Theme registry for managing available themes."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pptx_generator.themes.corporate import CorporateTheme
from pptx_generator.themes.dark import DarkTheme
from pptx_generator.themes.minimal import MinimalTheme
from pptx_generator.themes.modern import ModernTheme

if TYPE_CHECKING:
    from pptx_generator.themes.base import BaseTheme


THEME_REGISTRY: dict[str, type[BaseTheme]] = {
    "corporate": CorporateTheme,
    "modern": ModernTheme,
    "dark": DarkTheme,
    "minimal": MinimalTheme,
}


def get_theme(name: str) -> BaseTheme:
    """Get a theme instance by name.

    Args:
        name: Theme name (e.g., "corporate", "modern", "dark", "minimal")

    Returns:
        Instantiated theme object

    Raises:
        ValueError: If theme name is not found in registry
    """
    name_lower = name.lower()

    if name_lower not in THEME_REGISTRY:
        available = ", ".join(sorted(THEME_REGISTRY.keys()))
        raise ValueError(
            f"Theme '{name}' not found. Available themes: {available}"
        )

    theme_class = THEME_REGISTRY[name_lower]
    return theme_class()


def list_available_themes() -> list[str]:
    """Get list of all available theme names.

    Returns:
        Sorted list of theme names
    """
    return sorted(THEME_REGISTRY.keys())


def register_theme(name: str, theme_class: type[BaseTheme]) -> None:
    """Register a custom theme.

    Args:
        name: Theme name (will be converted to lowercase)
        theme_class: Theme class (must inherit from BaseTheme)

    Raises:
        ValueError: If theme_class is not a subclass of BaseTheme
    """
    from pptx_generator.themes.base import BaseTheme

    if not issubclass(theme_class, BaseTheme):
        raise ValueError(
            f"Theme class must inherit from BaseTheme, got {theme_class.__name__}"
        )

    THEME_REGISTRY[name.lower()] = theme_class
