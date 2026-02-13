"""Tests for pptx_generator.utils.units module."""

from __future__ import annotations

import pytest

from src.pptx_generator.utils import units


class TestInches:
    """Test inches() conversion function."""

    def test_inches_basic(self) -> None:
        """Test basic inch to EMU conversion."""
        assert units.inches(1.0) == 914400
        assert units.inches(2.0) == 1828800

    def test_inches_fractional(self) -> None:
        """Test fractional inch values."""
        assert units.inches(0.5) == 457200
        assert units.inches(1.5) == 1371600
        assert units.inches(2.25) == 2057400  # 2.25 * 914400 = 2057400

    def test_inches_zero(self) -> None:
        """Test zero inches."""
        assert units.inches(0) == 0

    def test_inches_returns_int(self) -> None:
        """Test that result is integer."""
        result = units.inches(1.5)
        assert isinstance(result, int)


class TestPt:
    """Test pt() conversion function."""

    def test_pt_basic(self) -> None:
        """Test basic point to EMU conversion."""
        assert units.pt(12) == 152400
        assert units.pt(24) == 304800

    def test_pt_fractional(self) -> None:
        """Test fractional point values."""
        assert units.pt(10.5) == 133350
        assert units.pt(18.5) == 234950

    def test_pt_zero(self) -> None:
        """Test zero points."""
        assert units.pt(0) == 0

    def test_pt_returns_int(self) -> None:
        """Test that result is integer."""
        result = units.pt(12.7)
        assert isinstance(result, int)


class TestCm:
    """Test cm() conversion function."""

    def test_cm_basic(self) -> None:
        """Test basic cm to EMU conversion."""
        assert units.cm(1.0) == 360000
        assert units.cm(5.0) == 1800000

    def test_cm_fractional(self) -> None:
        """Test fractional cm values."""
        assert units.cm(2.5) == 900000
        assert units.cm(7.5) == 2700000

    def test_cm_zero(self) -> None:
        """Test zero centimeters."""
        assert units.cm(0) == 0

    def test_cm_returns_int(self) -> None:
        """Test that result is integer."""
        result = units.cm(3.7)
        assert isinstance(result, int)


class TestPctOfWidth:
    """Test pct_of_width() conversion function."""

    def test_pct_of_width_default_slide(self) -> None:
        """Test percentage with default slide width."""
        # 50% of 13.333 inches = 6.6665 inches = 6095847 EMU (integer truncation)
        result = units.pct_of_width(50)
        assert result == 6095847

        # 100% should equal full width
        result = units.pct_of_width(100)
        assert result == units.inches(13.333)

    def test_pct_of_width_custom_slide(self) -> None:
        """Test percentage with custom slide width."""
        # 25% of 10 inches = 2.5 inches = 2286000 EMU
        result = units.pct_of_width(25, slide_width_inches=10)
        assert result == 2286000

        # 50% of 8 inches = 4 inches
        result = units.pct_of_width(50, slide_width_inches=8)
        assert result == units.inches(4)

    def test_pct_of_width_zero(self) -> None:
        """Test zero percentage."""
        assert units.pct_of_width(0) == 0

    def test_pct_of_width_invalid_percentage(self) -> None:
        """Test invalid percentage values."""
        with pytest.raises(ValueError, match="Percentage must be between 0 and 100"):
            units.pct_of_width(-1)

        with pytest.raises(ValueError, match="Percentage must be between 0 and 100"):
            units.pct_of_width(101)

    def test_pct_of_width_invalid_slide_width(self) -> None:
        """Test invalid slide width values."""
        with pytest.raises(ValueError, match="Slide width must be positive"):
            units.pct_of_width(50, slide_width_inches=0)

        with pytest.raises(ValueError, match="Slide width must be positive"):
            units.pct_of_width(50, slide_width_inches=-5)

    def test_pct_of_width_returns_int(self) -> None:
        """Test that result is integer."""
        result = units.pct_of_width(33.33)
        assert isinstance(result, int)


class TestPctOfHeight:
    """Test pct_of_height() conversion function."""

    def test_pct_of_height_default_slide(self) -> None:
        """Test percentage with default slide height."""
        # 50% of 7.5 inches = 3.75 inches = 3429000 EMU
        result = units.pct_of_height(50)
        assert result == 3429000

        # 100% should equal full height
        result = units.pct_of_height(100)
        assert result == units.inches(7.5)

    def test_pct_of_height_custom_slide(self) -> None:
        """Test percentage with custom slide height."""
        # 75% of 10 inches = 7.5 inches = 6858000 EMU
        result = units.pct_of_height(75, slide_height_inches=10)
        assert result == 6858000

        # 25% of 8 inches = 2 inches
        result = units.pct_of_height(25, slide_height_inches=8)
        assert result == units.inches(2)

    def test_pct_of_height_zero(self) -> None:
        """Test zero percentage."""
        assert units.pct_of_height(0) == 0

    def test_pct_of_height_invalid_percentage(self) -> None:
        """Test invalid percentage values."""
        with pytest.raises(ValueError, match="Percentage must be between 0 and 100"):
            units.pct_of_height(-1)

        with pytest.raises(ValueError, match="Percentage must be between 0 and 100"):
            units.pct_of_height(150)

    def test_pct_of_height_invalid_slide_height(self) -> None:
        """Test invalid slide height values."""
        with pytest.raises(ValueError, match="Slide height must be positive"):
            units.pct_of_height(50, slide_height_inches=0)

        with pytest.raises(ValueError, match="Slide height must be positive"):
            units.pct_of_height(50, slide_height_inches=-3)

    def test_pct_of_height_returns_int(self) -> None:
        """Test that result is integer."""
        result = units.pct_of_height(66.67)
        assert isinstance(result, int)


class TestReExports:
    """Test that python-pptx utilities are properly re-exported."""

    def test_inches_available(self) -> None:
        """Test Inches is available."""
        assert hasattr(units, "Inches")
        assert callable(units.Inches)

    def test_pt_available(self) -> None:
        """Test Pt is available."""
        assert hasattr(units, "Pt")
        assert callable(units.Pt)

    def test_emu_available(self) -> None:
        """Test Emu is available."""
        assert hasattr(units, "Emu")
        assert callable(units.Emu)


class TestConstants:
    """Test module constants."""

    def test_emu_constants(self) -> None:
        """Test EMU conversion constants are correct."""
        assert units.EMU_PER_INCH == 914400
        assert units.EMU_PER_POINT == 12700
        assert units.EMU_PER_CM == 360000

    def test_slide_dimension_constants(self) -> None:
        """Test default slide dimension constants."""
        assert units.DEFAULT_SLIDE_WIDTH_INCHES == 13.333
        assert units.DEFAULT_SLIDE_HEIGHT_INCHES == 7.5
