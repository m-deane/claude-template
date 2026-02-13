"""Test suite for presentation presets."""

from __future__ import annotations

import pytest

from pptx_generator.presets.registry import (
    get_preset,
    list_available_presets,
    PRESET_REGISTRY,
)
from pptx_generator.presets.base import BasePreset


class TestPresetRegistry:
    """Test preset registry functionality."""

    def test_preset_registry_initialized(self):
        """Test that the preset registry is initialized on module import."""
        assert len(PRESET_REGISTRY) > 0
        assert "technical" in PRESET_REGISTRY
        assert "executive" in PRESET_REGISTRY

    def test_list_available_presets(self):
        """Test listing all available presets."""
        presets = list_available_presets()
        assert isinstance(presets, list)
        assert len(presets) > 0
        assert all(isinstance(p, str) for p in presets)
        # Check sorted
        assert presets == sorted(presets)

    def test_get_preset_by_name(self):
        """Test retrieving a preset by name."""
        preset = get_preset("technical")
        assert isinstance(preset, BasePreset)
        assert preset.name == "technical"

    def test_get_preset_invalid_name(self):
        """Test that invalid preset names raise ValueError."""
        with pytest.raises(ValueError) as exc_info:
            get_preset("nonexistent_preset")

        assert "Unknown preset" in str(exc_info.value)
        assert "nonexistent_preset" in str(exc_info.value)

    def test_preset_aliases(self):
        """Test that preset aliases work correctly."""
        educational = get_preset("educational")
        explain = get_preset("explain")

        # Should be the same instance
        assert educational is explain

        summary = get_preset("summary")
        summarise = get_preset("summarise")
        assert summary is summarise


class TestDefaultPresets:
    """Test all default preset configurations."""

    @pytest.mark.parametrize("preset_name", [
        "technical",
        "executive",
        "analyst",
        "trader",
        "educational",
        "summary",
    ])
    def test_preset_loads(self, preset_name):
        """Test that each preset loads successfully."""
        preset = get_preset(preset_name)
        assert isinstance(preset, BasePreset)
        assert preset.name == preset_name

    @pytest.mark.parametrize("preset_name", [
        "technical",
        "executive",
        "analyst",
        "trader",
        "educational",
        "summary",
    ])
    def test_preset_has_required_fields(self, preset_name):
        """Test that each preset has required fields."""
        preset = get_preset(preset_name)

        # Verify basic attributes exist
        assert hasattr(preset, "name")
        assert hasattr(preset, "description")
        assert hasattr(preset, "max_bullets_per_slide")
        assert hasattr(preset, "max_words_per_bullet")
        assert hasattr(preset, "words_per_slide_target")

        # Verify values are reasonable
        assert preset.max_bullets_per_slide > 0
        assert preset.max_bullets_per_slide <= 10
        assert preset.max_words_per_bullet > 0
        assert preset.max_words_per_bullet <= 50
        assert preset.words_per_slide_target > 0

    @pytest.mark.parametrize("preset_name", [
        "technical",
        "executive",
        "analyst",
        "trader",
        "educational",
        "summary",
    ])
    def test_preset_has_slide_type_flags(self, preset_name):
        """Test that each preset has slide type configuration flags."""
        preset = get_preset(preset_name)

        assert isinstance(preset.use_title_slide, bool)
        assert isinstance(preset.use_agenda_slide, bool)
        assert isinstance(preset.use_section_dividers, bool)
        assert isinstance(preset.use_chart_slides, bool)
        assert isinstance(preset.use_diagram_slides, bool)
        assert isinstance(preset.use_timeline_slides, bool)
        assert isinstance(preset.use_comparison_slides, bool)
        assert isinstance(preset.use_closing_slide, bool)

    @pytest.mark.parametrize("preset_name", [
        "technical",
        "executive",
        "analyst",
        "trader",
        "educational",
        "summary",
    ])
    def test_preset_has_recommendations(self, preset_name):
        """Test that each preset has theme/palette/font recommendations."""
        preset = get_preset(preset_name)

        assert hasattr(preset, "recommended_theme")
        assert hasattr(preset, "recommended_palette")
        assert hasattr(preset, "recommended_font_stack")

        assert isinstance(preset.recommended_theme, str)
        assert isinstance(preset.recommended_palette, str)
        assert isinstance(preset.recommended_font_stack, str)


class TestPresetSlideSequence:
    """Test preset slide sequence generation."""

    def test_technical_preset_slide_sequence(self):
        """Test technical preset generates appropriate slide sequence."""
        preset = get_preset("technical")
        sequence = preset.get_slide_sequence(section_count=5)

        assert isinstance(sequence, list)
        assert len(sequence) > 0

        # Technical preset should start with title
        if preset.use_title_slide:
            assert sequence[0] == "title"

    def test_executive_preset_slide_sequence(self):
        """Test executive preset generates appropriate slide sequence."""
        preset = get_preset("executive")
        sequence = preset.get_slide_sequence(section_count=4)

        assert isinstance(sequence, list)
        assert len(sequence) > 0

        # Should include closing if enabled
        if preset.use_closing_slide:
            assert sequence[-1] == "closing"

    def test_slide_sequence_with_zero_sections(self):
        """Test slide sequence generation with zero sections."""
        preset = get_preset("technical")
        sequence = preset.get_slide_sequence(section_count=0)

        # Should still have title and/or closing if enabled
        assert isinstance(sequence, list)

    def test_slide_sequence_with_one_section(self):
        """Test slide sequence generation with single section."""
        preset = get_preset("technical")
        sequence = preset.get_slide_sequence(section_count=1)

        assert isinstance(sequence, list)
        assert len(sequence) >= 1

    def test_slide_sequence_with_many_sections(self):
        """Test slide sequence generation with many sections."""
        preset = get_preset("technical")
        sequence = preset.get_slide_sequence(section_count=10)

        assert isinstance(sequence, list)
        assert len(sequence) >= 10

        # Should contain content slides
        assert "content" in sequence

    def test_slide_sequence_contains_valid_types(self):
        """Test that slide sequences only contain valid slide types."""
        valid_types = [
            "title", "agenda", "section_divider", "section", "content",
            "comparison", "chart", "timeline", "diagram", "closing"
        ]

        preset = get_preset("technical")
        sequence = preset.get_slide_sequence(section_count=5)

        for slide_type in sequence:
            assert slide_type in valid_types, f"Invalid slide type: {slide_type}"

    def test_agenda_slide_only_with_enough_sections(self):
        """Test that agenda slide is only added with sufficient sections."""
        preset = get_preset("technical")

        # Few sections - no agenda
        sequence_small = preset.get_slide_sequence(section_count=2)
        if preset.use_agenda_slide:
            assert "agenda" not in sequence_small

        # Many sections - should have agenda
        sequence_large = preset.get_slide_sequence(section_count=5)
        if preset.use_agenda_slide:
            assert "agenda" in sequence_large


class TestPresetContentDensity:
    """Test preset content density configurations."""

    def test_executive_preset_low_density(self):
        """Test executive preset has low content density."""
        preset = get_preset("executive")

        # Executive presentations typically have fewer bullets
        assert preset.max_bullets_per_slide <= 6

    def test_technical_preset_higher_density(self):
        """Test technical preset allows higher content density."""
        preset = get_preset("technical")

        # Technical presentations may have more detail
        assert preset.max_bullets_per_slide >= 4

    def test_summary_preset_concise(self):
        """Test summary preset is concise."""
        preset = get_preset("summary")

        # Summary should be brief
        assert preset.max_bullets_per_slide <= 8
        assert preset.words_per_slide_target <= 150


class TestPresetStyles:
    """Test preset style configurations."""

    def test_presets_have_valid_chart_density(self):
        """Test that all presets have valid chart density values."""
        valid_densities = ["low", "medium", "high"]

        for preset_name in ["technical", "executive", "analyst", "trader", "educational", "summary"]:
            preset = get_preset(preset_name)
            assert preset.chart_density in valid_densities

    def test_presets_have_valid_diagram_style(self):
        """Test that all presets have valid diagram styles."""
        valid_styles = ["flow", "hierarchy", "cycle", "matrix"]

        for preset_name in ["technical", "executive", "analyst", "trader", "educational", "summary"]:
            preset = get_preset(preset_name)
            assert preset.diagram_style in valid_styles

    def test_presets_have_valid_bullet_style(self):
        """Test that all presets have valid bullet styles."""
        valid_styles = ["concise", "detailed", "data_driven"]

        for preset_name in ["technical", "executive", "analyst", "trader", "educational", "summary"]:
            preset = get_preset(preset_name)
            assert preset.bullet_style in valid_styles

    def test_presets_have_valid_title_style(self):
        """Test that all presets have valid title styles."""
        valid_styles = ["descriptive", "action_oriented", "question_based"]

        for preset_name in ["technical", "executive", "analyst", "trader", "educational", "summary"]:
            preset = get_preset(preset_name)
            assert preset.title_style in valid_styles


class TestPresetSlideRanges:
    """Test preset slide range constraints."""

    def test_presets_have_reasonable_slide_ranges(self):
        """Test that all presets have reasonable min/max slides."""
        for preset_name in ["technical", "executive", "analyst", "trader", "educational", "summary"]:
            preset = get_preset(preset_name)

            assert preset.min_slides > 0
            assert preset.max_slides > preset.min_slides
            assert preset.max_slides <= 100  # Reasonable upper bound
