from __future__ import annotations

from pptx_generator.presets.base import BasePreset
from pptx_generator.presets.technical import TechnicalPreset
from pptx_generator.presets.executive import ExecutivePreset
from pptx_generator.presets.analyst import AnalystPreset
from pptx_generator.presets.trader import TraderPreset
from pptx_generator.presets.educational import EducationalPreset
from pptx_generator.presets.summary import SummaryPreset


PRESET_REGISTRY: dict[str, BasePreset] = {}


def _register_defaults() -> None:
    """Register all default presets in the registry."""
    # Instantiate each preset
    technical = TechnicalPreset()
    executive = ExecutivePreset()
    analyst = AnalystPreset()
    trader = TraderPreset()
    educational = EducationalPreset()
    summary = SummaryPreset()

    # Register with primary names
    PRESET_REGISTRY["technical"] = technical
    PRESET_REGISTRY["executive"] = executive
    PRESET_REGISTRY["analyst"] = analyst
    PRESET_REGISTRY["trader"] = trader
    PRESET_REGISTRY["educational"] = educational
    PRESET_REGISTRY["summary"] = summary

    # Register aliases
    PRESET_REGISTRY["explain"] = educational  # Alias for educational
    PRESET_REGISTRY["summarise"] = summary  # British spelling alias


def get_preset(name: str) -> BasePreset:
    """Retrieve a preset by name.

    Args:
        name: The preset name or alias

    Returns:
        BasePreset instance

    Raises:
        ValueError: If preset name is not recognized
    """
    if name not in PRESET_REGISTRY:
        available = ", ".join(sorted(PRESET_REGISTRY.keys()))
        raise ValueError(f"Unknown preset '{name}'. Available: {available}")
    return PRESET_REGISTRY[name]


def list_available_presets() -> list[str]:
    """List all available preset names (including aliases).

    Returns:
        Sorted list of preset names
    """
    return sorted(PRESET_REGISTRY.keys())


# Initialize registry on module import
_register_defaults()
