"""Test suite for presentation configuration models."""

from __future__ import annotations

import pytest
from pydantic import ValidationError
from pptx.dml.color import RGBColor

from src.pptx_generator.config import (
    ColorPalette,
    FontSpec,
    FONT_STACKS,
    PALETTES,
    PresentationConfig,
    SlideConfig,
    Typography,
)


class TestColorPalette:
    """Test ColorPalette model and color utilities."""

    def test_color_palette_creation(self):
        """Test creating a ColorPalette from dict."""
        palette = ColorPalette(**PALETTES['corporate'])
        assert palette.primary == "#1E3A5F"
        assert palette.background == "#FFFFFF"
        assert palette.text_dark == "#1A1A1A"

    def test_all_palettes_load(self):
        """Test that all predefined palettes load successfully."""
        for name, colors in PALETTES.items():
            palette = ColorPalette(**colors)
            assert palette.primary
            assert palette.secondary
            assert palette.accent
            assert len(colors) == 12

    def test_to_rgb_conversion(self):
        """Test hex to RGBColor conversion."""
        palette = ColorPalette(**PALETTES['corporate'])

        # Test with hash prefix
        rgb = palette.to_rgb('#1E3A5F')
        assert isinstance(rgb, RGBColor)

        # Test without hash prefix
        rgb2 = palette.to_rgb('1E3A5F')
        assert isinstance(rgb2, RGBColor)

        # Test white
        rgb_white = palette.to_rgb('#FFFFFF')
        assert isinstance(rgb_white, RGBColor)

        # Test black
        rgb_black = palette.to_rgb('#000000')
        assert isinstance(rgb_black, RGBColor)

    def test_get_color_map(self):
        """Test getting all colors as RGBColor objects."""
        palette = ColorPalette(**PALETTES['modern'])
        color_map = palette.get_color_map()

        assert len(color_map) == 12
        assert all(isinstance(v, RGBColor) for v in color_map.values())
        assert 'primary' in color_map
        assert 'secondary' in color_map
        assert 'accent' in color_map


class TestFontSpec:
    """Test FontSpec model."""

    def test_font_spec_creation(self):
        """Test creating a FontSpec."""
        font = FontSpec(family='Arial', size_pt=16, bold=True, italic=False)
        assert font.family == 'Arial'
        assert font.size_pt == 16
        assert font.bold is True
        assert font.italic is False
        assert font.color_hex is None

    def test_font_spec_with_color(self):
        """Test FontSpec with color override."""
        font = FontSpec(
            family='Calibri',
            size_pt=24,
            bold=True,
            color_hex='#FF0000'
        )
        assert font.color_hex == '#FF0000'

    def test_font_spec_validation(self):
        """Test FontSpec validation for invalid sizes."""
        with pytest.raises(ValidationError):
            FontSpec(family='Arial', size_pt=0)

        with pytest.raises(ValidationError):
            FontSpec(family='Arial', size_pt=-10)


class TestTypography:
    """Test Typography model."""

    def test_typography_creation(self):
        """Test creating Typography from font stack."""
        typo = Typography(**{
            k: FontSpec(**v)
            for k, v in FONT_STACKS['professional'].items()
        })

        assert typo.title.size_pt == 36
        assert typo.subtitle.size_pt == 24
        assert typo.heading.size_pt == 28
        assert typo.subheading.size_pt == 20
        assert typo.body.size_pt == 16
        assert typo.caption.size_pt == 12
        assert typo.footnote.size_pt == 10

    def test_all_font_stacks_load(self):
        """Test that all predefined font stacks load successfully."""
        for name, specs in FONT_STACKS.items():
            typo = Typography(**{k: FontSpec(**v) for k, v in specs.items()})
            assert typo.title
            assert typo.subtitle
            assert typo.heading
            assert typo.subheading
            assert typo.body
            assert typo.caption
            assert typo.footnote

    def test_font_stack_hierarchy(self):
        """Test that font sizes follow hierarchical order."""
        for name, specs in FONT_STACKS.items():
            typo = Typography(**{k: FontSpec(**v) for k, v in specs.items()})

            # Title should be largest
            assert typo.title.size_pt >= typo.subtitle.size_pt
            assert typo.title.size_pt >= typo.heading.size_pt

            # Heading hierarchy
            assert typo.heading.size_pt >= typo.subheading.size_pt
            assert typo.subheading.size_pt >= typo.body.size_pt

            # Body should be larger than caption/footnote
            assert typo.body.size_pt >= typo.caption.size_pt
            assert typo.caption.size_pt >= typo.footnote.size_pt


class TestSlideConfig:
    """Test SlideConfig model."""

    def test_default_slide_config(self):
        """Test default widescreen 16:9 dimensions."""
        config = SlideConfig()
        assert config.width_inches == 13.333
        assert config.height_inches == 7.5
        assert config.margin_inches == 0.6
        assert config.content_area_ratio == 0.85

    def test_custom_slide_config(self):
        """Test custom slide dimensions."""
        config = SlideConfig(
            width_inches=10.0,
            height_inches=7.5,
            margin_inches=0.5,
            content_area_ratio=0.9
        )
        assert config.width_inches == 10.0
        assert config.height_inches == 7.5
        assert config.margin_inches == 0.5
        assert config.content_area_ratio == 0.9

    def test_slide_config_validation(self):
        """Test SlideConfig validation rules."""
        # Width must be positive
        with pytest.raises(ValidationError):
            SlideConfig(width_inches=0)

        # Height must be positive
        with pytest.raises(ValidationError):
            SlideConfig(height_inches=-1)

        # Margin cannot be negative
        with pytest.raises(ValidationError):
            SlideConfig(margin_inches=-0.5)

        # Content area ratio must be 0-1
        with pytest.raises(ValidationError):
            SlideConfig(content_area_ratio=1.5)


class TestPresentationConfig:
    """Test PresentationConfig model."""

    def test_minimal_presentation_config(self):
        """Test creating config with only required fields."""
        config = PresentationConfig(title='My Presentation')
        assert config.title == 'My Presentation'
        assert config.subtitle == ''
        assert config.author == ''
        assert config.date == ''
        assert config.palette_name == 'corporate'
        assert config.font_stack_name == 'professional'

    def test_full_presentation_config(self):
        """Test creating config with all fields."""
        config = PresentationConfig(
            title='Q4 Results',
            subtitle='Financial Overview',
            author='Jane Doe',
            date='2026-02-12',
            palette_name='finance',
            font_stack_name='modern',
            theme_name='financial',
            preset_name='executive',
            max_bullets_per_slide=5,
            max_words_per_bullet=15,
            include_slide_numbers=False,
            include_agenda=False,
            include_section_dividers=False
        )

        assert config.title == 'Q4 Results'
        assert config.subtitle == 'Financial Overview'
        assert config.author == 'Jane Doe'
        assert config.date == '2026-02-12'
        assert config.palette_name == 'finance'
        assert config.font_stack_name == 'modern'
        assert config.max_bullets_per_slide == 5
        assert config.max_words_per_bullet == 15
        assert config.include_slide_numbers is False

    def test_palette_name_validation(self):
        """Test that invalid palette names are rejected."""
        with pytest.raises(ValidationError) as exc_info:
            PresentationConfig(
                title='Test',
                palette_name='nonexistent'
            )

        assert 'palette_name' in str(exc_info.value)
        assert 'nonexistent' in str(exc_info.value)

    def test_font_stack_name_validation(self):
        """Test that invalid font stack names are rejected."""
        with pytest.raises(ValidationError) as exc_info:
            PresentationConfig(
                title='Test',
                font_stack_name='invalid_stack'
            )

        assert 'font_stack_name' in str(exc_info.value)
        assert 'invalid_stack' in str(exc_info.value)

    def test_valid_palette_and_font_combinations(self):
        """Test all valid palette and font stack combinations."""
        for palette_name in PALETTES.keys():
            for font_stack_name in FONT_STACKS.keys():
                config = PresentationConfig(
                    title='Test',
                    palette_name=palette_name,
                    font_stack_name=font_stack_name
                )
                assert config.palette_name == palette_name
                assert config.font_stack_name == font_stack_name

    def test_content_limits_validation(self):
        """Test validation of content limit fields."""
        # max_bullets_per_slide must be positive
        with pytest.raises(ValidationError):
            PresentationConfig(title='Test', max_bullets_per_slide=0)

        # max_bullets_per_slide must be <= 10
        with pytest.raises(ValidationError):
            PresentationConfig(title='Test', max_bullets_per_slide=15)

        # max_words_per_bullet must be positive
        with pytest.raises(ValidationError):
            PresentationConfig(title='Test', max_words_per_bullet=0)

        # max_words_per_bullet must be <= 50
        with pytest.raises(ValidationError):
            PresentationConfig(title='Test', max_words_per_bullet=100)


class TestIntegration:
    """Integration tests for combined config usage."""

    def test_complete_presentation_setup(self):
        """Test setting up a complete presentation configuration."""
        # Create presentation config
        config = PresentationConfig(
            title='Strategic Vision 2026',
            subtitle='Company Roadmap',
            author='Leadership Team',
            palette_name='modern',
            font_stack_name='professional'
        )

        # Load color palette
        palette = ColorPalette(**PALETTES[config.palette_name])
        color_map = palette.get_color_map()

        # Load typography
        typo = Typography(**{
            k: FontSpec(**v)
            for k, v in FONT_STACKS[config.font_stack_name].items()
        })

        # Verify complete setup
        assert config.title
        assert palette.primary
        assert typo.title.size_pt > typo.body.size_pt
        assert len(color_map) == 12
        assert isinstance(color_map['primary'], RGBColor)

    def test_all_theme_combinations(self):
        """Test that all palette/font combinations work together."""
        for palette_name in PALETTES.keys():
            for font_stack_name in FONT_STACKS.keys():
                config = PresentationConfig(
                    title=f'Test: {palette_name} + {font_stack_name}',
                    palette_name=palette_name,
                    font_stack_name=font_stack_name
                )

                palette = ColorPalette(**PALETTES[config.palette_name])
                typo = Typography(**{
                    k: FontSpec(**v)
                    for k, v in FONT_STACKS[config.font_stack_name].items()
                })

                # Verify both loaded successfully
                assert palette.primary
                assert typo.title.family
