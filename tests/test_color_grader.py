"""Tests for color grading module."""

import numpy as np
import pytest

from drone_reel.core.color_grader import (
    ColorGrader,
    ColorPreset,
    ColorAdjustments,
    get_preset_names,
    create_grader_from_preset,
)


class TestColorAdjustments:
    """Tests for ColorAdjustments dataclass."""

    def test_default_values(self):
        """Test default adjustment values are neutral."""
        adj = ColorAdjustments()
        assert adj.brightness == 0.0
        assert adj.contrast == 0.0
        assert adj.saturation == 0.0
        assert adj.temperature == 0.0

    def test_custom_values(self):
        """Test custom adjustment values."""
        adj = ColorAdjustments(
            brightness=10,
            contrast=20,
            saturation=-10,
        )
        assert adj.brightness == 10
        assert adj.contrast == 20
        assert adj.saturation == -10


class TestColorGrader:
    """Tests for ColorGrader class."""

    @pytest.fixture
    def sample_frame(self):
        """Create a sample BGR frame for testing."""
        return np.ones((100, 100, 3), dtype=np.uint8) * 128

    @pytest.fixture
    def colorful_frame(self):
        """Create a colorful test frame."""
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        frame[:50, :50] = [255, 0, 0]  # Blue
        frame[:50, 50:] = [0, 255, 0]  # Green
        frame[50:, :50] = [0, 0, 255]  # Red
        frame[50:, 50:] = [255, 255, 0]  # Cyan
        return frame

    def test_grade_frame_no_adjustment(self, sample_frame):
        """Test grading with no adjustments returns similar frame."""
        grader = ColorGrader(preset=ColorPreset.NONE)
        result = grader.grade_frame(sample_frame)

        assert result.shape == sample_frame.shape
        assert result.dtype == np.uint8
        # Should be nearly identical
        np.testing.assert_array_almost_equal(result, sample_frame, decimal=0)

    def test_brightness_increase(self, sample_frame):
        """Test brightness increase makes frame brighter."""
        grader = ColorGrader(
            adjustments=ColorAdjustments(brightness=50)
        )
        result = grader.grade_frame(sample_frame)

        assert np.mean(result) > np.mean(sample_frame)

    def test_brightness_decrease(self, sample_frame):
        """Test brightness decrease makes frame darker."""
        grader = ColorGrader(
            adjustments=ColorAdjustments(brightness=-50)
        )
        result = grader.grade_frame(sample_frame)

        assert np.mean(result) < np.mean(sample_frame)

    def test_contrast_increase(self, sample_frame):
        """Test contrast increase affects dynamic range."""
        grader = ColorGrader(
            adjustments=ColorAdjustments(contrast=50)
        )
        result = grader.grade_frame(sample_frame)

        # Higher contrast should push values away from middle
        assert result.shape == sample_frame.shape

    def test_saturation_decrease(self, colorful_frame):
        """Test saturation decrease moves toward grayscale."""
        grader = ColorGrader(
            adjustments=ColorAdjustments(saturation=-50)
        )
        result = grader.grade_frame(colorful_frame)

        # Check that color channels are more similar
        assert result.shape == colorful_frame.shape

    def test_temperature_warm(self, sample_frame):
        """Test warm temperature increases red, decreases blue."""
        grader = ColorGrader(
            adjustments=ColorAdjustments(temperature=50)
        )
        result = grader.grade_frame(sample_frame)

        # Red channel should increase, blue should decrease
        assert np.mean(result[:, :, 2]) > np.mean(sample_frame[:, :, 2])  # Red
        assert np.mean(result[:, :, 0]) < np.mean(sample_frame[:, :, 0])  # Blue

    def test_temperature_cool(self, sample_frame):
        """Test cool temperature decreases red, increases blue."""
        grader = ColorGrader(
            adjustments=ColorAdjustments(temperature=-50)
        )
        result = grader.grade_frame(sample_frame)

        # Blue channel should increase, red should decrease
        assert np.mean(result[:, :, 0]) > np.mean(sample_frame[:, :, 0])  # Blue
        assert np.mean(result[:, :, 2]) < np.mean(sample_frame[:, :, 2])  # Red

    def test_all_presets_produce_valid_output(self, sample_frame):
        """Test all presets produce valid output frames."""
        for preset in ColorPreset:
            grader = ColorGrader(preset=preset)
            result = grader.grade_frame(sample_frame)

            assert result.shape == sample_frame.shape
            assert result.dtype == np.uint8
            assert np.all(result >= 0)
            assert np.all(result <= 255)

    def test_output_clipping(self):
        """Test that output is properly clipped to valid range."""
        # Create frame that would overflow with high brightness
        bright_frame = np.ones((100, 100, 3), dtype=np.uint8) * 250
        grader = ColorGrader(
            adjustments=ColorAdjustments(brightness=50)
        )
        result = grader.grade_frame(bright_frame)

        assert np.all(result <= 255)

        # Create frame that would underflow with low brightness
        dark_frame = np.ones((100, 100, 3), dtype=np.uint8) * 10
        grader = ColorGrader(
            adjustments=ColorAdjustments(brightness=-50)
        )
        result = grader.grade_frame(dark_frame)

        assert np.all(result >= 0)


class TestPresetHelpers:
    """Tests for preset helper functions."""

    def test_get_preset_names(self):
        """Test get_preset_names returns all presets."""
        names = get_preset_names()

        assert "none" in names
        assert "cinematic" in names
        assert "drone_aerial" in names
        assert len(names) == len(ColorPreset)

    def test_create_grader_from_valid_preset(self):
        """Test creating grader from valid preset name."""
        grader = create_grader_from_preset("cinematic")
        assert grader.preset == ColorPreset.CINEMATIC

    def test_create_grader_from_invalid_preset(self):
        """Test creating grader from invalid preset defaults to NONE."""
        grader = create_grader_from_preset("nonexistent")
        assert grader.preset == ColorPreset.NONE

    def test_create_grader_case_insensitive(self):
        """Test preset names are case insensitive."""
        grader1 = create_grader_from_preset("CINEMATIC")
        grader2 = create_grader_from_preset("Cinematic")
        grader3 = create_grader_from_preset("cinematic")

        assert grader1.preset == grader2.preset == grader3.preset
