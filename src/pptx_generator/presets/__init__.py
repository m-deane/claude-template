"""Audience-specific presentation presets."""

from pptx_generator.presets.base import BasePreset
from pptx_generator.presets.registry import PRESET_REGISTRY, get_preset

__all__ = ["BasePreset", "PRESET_REGISTRY", "get_preset"]
