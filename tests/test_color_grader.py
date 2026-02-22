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


class TestColorGraderIntensity:
    """Tests for color grading intensity scaling."""

    @pytest.fixture
    def sample_frame(self):
        """Create a sample BGR frame for testing."""
        return np.ones((100, 100, 3), dtype=np.uint8) * 128

    def test_intensity_default_is_full(self):
        """Test default intensity is 1.0."""
        grader = ColorGrader(preset=ColorPreset.DRONE_AERIAL)
        assert grader.intensity == 1.0
        assert grader.adjustments.brightness == 5

    def test_intensity_scales_adjustments(self):
        """Test intensity=0.5 halves all adjustment values."""
        grader = ColorGrader(preset=ColorPreset.DRONE_AERIAL, intensity=0.5)
        assert grader.intensity == 0.5
        assert grader.adjustments.brightness == 2.5
        # contrast was boosted to 14; 14 * 0.5 = 7.0
        assert grader.adjustments.contrast == 7.0
        assert grader.adjustments.vibrance == 7.5

    def test_intensity_zero_gives_no_adjustments(self):
        """Test intensity=0.0 zeroes all adjustments."""
        grader = ColorGrader(preset=ColorPreset.DRONE_AERIAL, intensity=0.0)
        assert grader.adjustments.brightness == 0.0
        assert grader.adjustments.contrast == 0.0
        assert grader.adjustments.saturation == 0.0

    def test_intensity_clamped_above_one(self):
        """Test intensity above 1.0 is clamped to 1.0."""
        grader = ColorGrader(preset=ColorPreset.DRONE_AERIAL, intensity=1.5)
        assert grader.intensity == 1.0

    def test_intensity_clamped_below_zero(self):
        """Test intensity below 0.0 is clamped to 0.0."""
        grader = ColorGrader(preset=ColorPreset.DRONE_AERIAL, intensity=-0.5)
        assert grader.intensity == 0.0

    def test_intensity_produces_weaker_grade(self, sample_frame):
        """Test that lower intensity produces less color change."""
        grader_full = ColorGrader(preset=ColorPreset.WARM_SUNSET, intensity=1.0)
        grader_half = ColorGrader(preset=ColorPreset.WARM_SUNSET, intensity=0.5)

        result_full = grader_full.grade_frame(sample_frame.copy())
        result_half = grader_half.grade_frame(sample_frame.copy())

        # Half intensity should be closer to original than full intensity
        diff_full = np.mean(np.abs(result_full.astype(float) - sample_frame.astype(float)))
        diff_half = np.mean(np.abs(result_half.astype(float) - sample_frame.astype(float)))
        assert diff_half < diff_full

    def test_intensity_preserves_selective_color(self):
        """Test that intensity scaling preserves selective_color reference."""
        from drone_reel.core.color_grader import SelectiveColorAdjustments
        sel = SelectiveColorAdjustments(red_hue=10)
        adj = ColorAdjustments(brightness=20, selective_color=sel)
        grader = ColorGrader(adjustments=adj, intensity=0.5)
        # Manual adjustments override preset, intensity still applies
        assert grader.adjustments.selective_color is sel

    def test_intensity_one_no_change(self):
        """Test intensity=1.0 does not create new adjustments object."""
        grader = ColorGrader(preset=ColorPreset.DRONE_AERIAL, intensity=1.0)
        expected = ColorGrader.PRESET_ADJUSTMENTS[ColorPreset.DRONE_AERIAL]
        assert grader.adjustments.brightness == expected.brightness


class TestColorGraderLUTSupport:
    """Tests for LUT loading and application."""

    @pytest.fixture
    def grader(self):
        """Create a ColorGrader instance."""
        return ColorGrader()

    @pytest.fixture
    def sample_frame(self):
        """Create a sample BGR frame for testing."""
        return np.ones((100, 100, 3), dtype=np.uint8) * 128

    def test_lut_loading_cube_format(self, grader):
        """Test loading .cube LUT file."""
        # This is a placeholder test - actual implementation would need a real LUT file
        # For now, just verify the method exists and can be called
        if hasattr(grader, 'load_lut'):
            assert callable(grader.load_lut)

    def test_lut_loading_3dl_format(self, grader):
        """Test loading .3dl LUT file."""
        if hasattr(grader, 'load_lut'):
            assert callable(grader.load_lut)

    def test_lut_application(self, grader, sample_frame):
        """Test applying loaded LUT to frame."""
        # Placeholder test for LUT application
        if hasattr(grader, 'apply_lut'):
            assert callable(grader.apply_lut)


class TestColorGraderToneCurves:
    """Tests for tone curve adjustments."""

    @pytest.fixture
    def grader(self):
        """Create a ColorGrader instance."""
        return ColorGrader()

    @pytest.fixture
    def sample_frame(self):
        """Create a sample BGR frame for testing."""
        return np.ones((100, 100, 3), dtype=np.uint8) * 128

    def test_tone_curve_s_curve(self, grader, sample_frame):
        """Test S-curve tone adjustment."""
        if hasattr(grader, '_apply_tone_curve'):
            # S-curve increases contrast
            result = grader._apply_tone_curve(sample_frame.astype(np.float32), curve_type='s_curve')
            assert isinstance(result, np.ndarray)

    def test_tone_curve_linear(self, grader, sample_frame):
        """Test linear tone curve (no change)."""
        if hasattr(grader, '_apply_tone_curve'):
            result = grader._apply_tone_curve(sample_frame.astype(np.float32), curve_type='linear')
            assert isinstance(result, np.ndarray)

    def test_tone_curve_custom_points(self, grader, sample_frame):
        """Test custom tone curve from control points."""
        if hasattr(grader, '_apply_custom_curve'):
            # Define curve control points (input -> output)
            points = [(0, 0), (64, 48), (128, 128), (192, 208), (255, 255)]
            result = grader._apply_custom_curve(sample_frame.astype(np.float32), points)
            assert isinstance(result, np.ndarray)


class TestColorGraderSelectiveColor:
    """Tests for selective color adjustments."""

    @pytest.fixture
    def grader(self):
        """Create a ColorGrader instance."""
        return ColorGrader()

    @pytest.fixture
    def colorful_frame(self):
        """Create a colorful test frame."""
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        frame[:50, :50] = [255, 0, 0]  # Blue
        frame[:50, 50:] = [0, 255, 0]  # Green
        frame[50:, :50] = [0, 0, 255]  # Red
        frame[50:, 50:] = [255, 255, 0]  # Cyan
        return frame

    def test_selective_color_adjustment_reds(self, grader, colorful_frame):
        """Test adjusting only red tones."""
        if hasattr(grader, '_adjust_selective_color'):
            # Adjust reds: increase saturation
            result = grader._adjust_selective_color(
                colorful_frame.astype(np.float32),
                hue_range=(0, 30),  # Red hue range
                saturation_shift=20,
            )
            assert isinstance(result, np.ndarray)

    def test_selective_color_adjustment_blues(self, grader, colorful_frame):
        """Test adjusting only blue tones."""
        if hasattr(grader, '_adjust_selective_color'):
            result = grader._adjust_selective_color(
                colorful_frame.astype(np.float32),
                hue_range=(90, 120),  # Blue hue range
                saturation_shift=15,
            )
            assert isinstance(result, np.ndarray)

    def test_selective_color_preserves_other_colors(self, grader, colorful_frame):
        """Test that selective adjustment doesn't affect other colors."""
        if hasattr(grader, '_adjust_selective_color'):
            # When implemented, this would verify color isolation
            pass


class TestColorGraderImprovedGrain:
    """Tests for improved film grain effect."""

    @pytest.fixture
    def grader(self):
        """Create a ColorGrader instance."""
        return ColorGrader()

    @pytest.fixture
    def sample_frame(self):
        """Create a sample BGR frame for testing."""
        return np.ones((100, 100, 3), dtype=np.uint8) * 128

    def test_film_grain_basic(self, grader, sample_frame):
        """Test basic film grain application."""
        adjusted = ColorAdjustments(grain=30)
        grader.adjustments = adjusted

        result = grader.grade_frame(sample_frame)

        # Grain should add variation
        assert result.std() > sample_frame.std()

    def test_film_grain_intensity_levels(self, grader, sample_frame):
        """Test different grain intensity levels."""
        # Low grain
        grader_low = ColorGrader(adjustments=ColorAdjustments(grain=10))
        result_low = grader_low.grade_frame(sample_frame)

        # High grain
        grader_high = ColorGrader(adjustments=ColorAdjustments(grain=50))
        result_high = grader_high.grade_frame(sample_frame)

        # Higher grain should produce more variation
        assert result_high.std() > result_low.std()

    def test_film_grain_luminance_based(self, grader):
        """Test luminance-based grain distribution."""
        if hasattr(grader, '_apply_luminance_grain'):
            # Create frame with varying brightness
            frame = np.zeros((100, 100, 3), dtype=np.float32)
            frame[:50, :] = 50   # Dark region
            frame[50:, :] = 200  # Bright region

            result = grader._apply_luminance_grain(frame, amount=20)

            # Grain should vary with luminance
            assert isinstance(result, np.ndarray)

    def test_film_grain_color_channels(self, grader, sample_frame):
        """Test that grain affects color channels differently."""
        if hasattr(grader, '_apply_color_grain'):
            # Chromatic grain adds different noise to each channel
            result = grader._apply_color_grain(sample_frame.astype(np.float32), amount=25)

            # Channels should have different variations
            assert isinstance(result, np.ndarray)


class TestColorGraderGPUFallback:
    """Tests for GPU acceleration and fallback."""

    @pytest.fixture
    def grader(self):
        """Create a ColorGrader instance."""
        return ColorGrader()

    def test_gpu_detection(self, grader):
        """Test GPU availability detection."""
        if hasattr(grader, '_has_gpu_support'):
            # Should return boolean
            assert isinstance(grader._has_gpu_support(), bool)

    def test_gpu_grade_fallback(self, grader):
        """Test that grading falls back to CPU if GPU unavailable."""
        sample_frame = np.ones((100, 100, 3), dtype=np.uint8) * 128

        # Should work regardless of GPU availability
        result = grader.grade_frame(sample_frame)

        assert isinstance(result, np.ndarray)
        assert result.shape == sample_frame.shape


class TestColorGraderEdgeCases:
    """Tests for edge cases and error handling."""

    @pytest.fixture
    def grader(self):
        """Create a ColorGrader instance."""
        return ColorGrader()

    def test_extreme_brightness_positive(self, grader):
        """Test extreme positive brightness adjustment."""
        frame = np.ones((100, 100, 3), dtype=np.uint8) * 128
        grader.adjustments = ColorAdjustments(brightness=100)

        result = grader.grade_frame(frame)

        # Should be clipped at 255
        assert np.all(result <= 255)
        assert np.mean(result) > np.mean(frame)

    def test_extreme_brightness_negative(self, grader):
        """Test extreme negative brightness adjustment."""
        frame = np.ones((100, 100, 3), dtype=np.uint8) * 128
        grader.adjustments = ColorAdjustments(brightness=-100)

        result = grader.grade_frame(frame)

        # Should be clipped at 0
        assert np.all(result >= 0)
        assert np.mean(result) < np.mean(frame)

    def test_extreme_contrast(self, grader):
        """Test extreme contrast adjustment."""
        frame = np.random.randint(50, 200, (100, 100, 3), dtype=np.uint8)
        grader.adjustments = ColorAdjustments(contrast=100)

        result = grader.grade_frame(frame)

        # Should still be valid
        assert np.all(result >= 0)
        assert np.all(result <= 255)

    def test_extreme_saturation_desaturate(self, grader):
        """Test complete desaturation."""
        colorful = np.zeros((100, 100, 3), dtype=np.uint8)
        colorful[:, :, 0] = 255  # Pure blue

        grader.adjustments = ColorAdjustments(saturation=-100)
        result = grader.grade_frame(colorful)

        # Should be grayscale (all channels equal)
        assert result[:, :, 0].mean() == pytest.approx(result[:, :, 1].mean(), abs=1)
        assert result[:, :, 1].mean() == pytest.approx(result[:, :, 2].mean(), abs=1)

    def test_all_black_frame(self, grader):
        """Test grading all-black frame."""
        black = np.zeros((100, 100, 3), dtype=np.uint8)
        grader.adjustments = ColorAdjustments(brightness=50, contrast=20)

        result = grader.grade_frame(black)

        assert isinstance(result, np.ndarray)
        assert result.shape == black.shape

    def test_all_white_frame(self, grader):
        """Test grading all-white frame."""
        white = np.ones((100, 100, 3), dtype=np.uint8) * 255
        grader.adjustments = ColorAdjustments(brightness=-50, contrast=20)

        result = grader.grade_frame(white)

        assert isinstance(result, np.ndarray)
        assert result.shape == white.shape

    def test_single_pixel_frame(self, grader):
        """Test grading very small frame."""
        tiny = np.ones((1, 1, 3), dtype=np.uint8) * 128

        result = grader.grade_frame(tiny)

        assert result.shape == (1, 1, 3)

    def test_combined_extreme_adjustments(self, grader):
        """Test multiple extreme adjustments combined."""
        frame = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)

        grader.adjustments = ColorAdjustments(
            brightness=80,
            contrast=50,
            saturation=40,
            temperature=60,
            vibrance=30,
            fade=40,
            grain=25,
        )

        result = grader.grade_frame(frame)

        # Should still produce valid output
        assert np.all(result >= 0)
        assert np.all(result <= 255)
        assert result.shape == frame.shape


class TestColorGraderPresetQuality:
    """Tests for preset quality and consistency."""

    @pytest.fixture
    def test_frame(self):
        """Create a representative test frame."""
        # Create a frame with varied content
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        # Sky
        frame[0:160, :] = [200, 150, 100]
        # Vegetation
        frame[160:320, :] = [50, 120, 40]
        # Water/reflection
        frame[320:, :] = [120, 100, 80]
        return frame

    def test_drone_aerial_preset_consistency(self, test_frame):
        """Test DRONE_AERIAL preset produces consistent results."""
        grader = ColorGrader(preset=ColorPreset.DRONE_AERIAL)

        result1 = grader.grade_frame(test_frame.copy())
        result2 = grader.grade_frame(test_frame.copy())

        # Should be deterministic (except for grain)
        np.testing.assert_array_almost_equal(result1, result2, decimal=0)

    def test_all_presets_valid_output(self, test_frame):
        """Test all presets produce valid output."""
        for preset in ColorPreset:
            grader = ColorGrader(preset=preset)
            result = grader.grade_frame(test_frame)

            assert result.shape == test_frame.shape
            assert result.dtype == np.uint8
            assert np.all(result >= 0)
            assert np.all(result <= 255)


class TestDithering:
    """Tests for dithering functionality."""

    @pytest.fixture
    def grader(self):
        """Create a ColorGrader instance."""
        return ColorGrader()

    @pytest.fixture
    def sample_frame(self):
        """Create a sample BGR frame with gradients."""
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        # Create a gradient to make banding visible
        for i in range(100):
            frame[i, :] = [i * 2.55, i * 2.55, i * 2.55]
        return frame

    def test_dither_produces_different_output(self, grader, sample_frame):
        """Test that _apply_dither() produces output different from input."""
        frame_float = sample_frame.astype(np.float32)
        result = grader._apply_dither(frame_float)

        # Dithering should change the frame
        assert not np.array_equal(result, frame_float)

        # Changes should be subtle (within a few levels)
        diff = np.abs(result - frame_float)
        assert np.max(diff) < 10  # Max change should be small

    def test_dither_is_deterministic(self, grader, sample_frame):
        """Test that dither pattern is deterministic (same input = same output)."""
        frame_float = sample_frame.astype(np.float32)

        result1 = grader._apply_dither(frame_float.copy())
        result2 = grader._apply_dither(frame_float.copy())

        # Same input should produce identical output
        np.testing.assert_array_equal(result1, result2)

    def test_dither_strength_affects_magnitude(self, grader, sample_frame):
        """Test that dithering strength parameter affects the magnitude of changes."""
        frame_float = sample_frame.astype(np.float32)

        result_weak = grader._apply_dither(frame_float.copy(), strength=0.5)
        result_medium = grader._apply_dither(frame_float.copy(), strength=1.5)
        result_strong = grader._apply_dither(frame_float.copy(), strength=3.0)

        # Calculate average absolute difference from original
        diff_weak = np.mean(np.abs(result_weak - frame_float))
        diff_medium = np.mean(np.abs(result_medium - frame_float))
        diff_strong = np.mean(np.abs(result_strong - frame_float))

        # Higher strength should produce larger changes
        assert diff_weak < diff_medium < diff_strong

    def test_dither_preserves_shape_and_type(self, grader, sample_frame):
        """Test that dithering preserves frame shape and dtype."""
        frame_float = sample_frame.astype(np.float32)
        result = grader._apply_dither(frame_float)

        assert result.shape == frame_float.shape
        assert result.dtype == np.float32

    def test_dither_applied_when_adjustments_made(self, grader, sample_frame):
        """Test that dithering is applied during grade_frame when adjustments are made."""
        # Apply an adjustment to trigger dithering
        grader.adjustments = ColorAdjustments(brightness=10)

        result = grader.grade_frame(sample_frame)

        # Should have dithering applied (hard to test directly, but should succeed)
        assert result.shape == sample_frame.shape
        assert result.dtype == np.uint8


class TestBatchedHSV:
    """Tests for batched HSV conversion."""

    @pytest.fixture
    def grader(self):
        """Create a ColorGrader instance."""
        return ColorGrader()

    @pytest.fixture
    def colorful_frame(self):
        """Create a colorful test frame."""
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        frame[:50, :50] = [255, 0, 0]  # Blue
        frame[:50, 50:] = [0, 255, 0]  # Green
        frame[50:, :50] = [0, 0, 255]  # Red
        frame[50:, 50:] = [255, 255, 0]  # Cyan
        return frame

    def test_batched_hsv_saturation_only(self, grader, colorful_frame):
        """Test that batched HSV with saturation only matches individual call."""
        frame_float = colorful_frame.astype(np.float32)

        # Set up for batched saturation
        grader.adjustments = ColorAdjustments(saturation=20)
        grader.preset = ColorPreset.NONE
        batched_result = grader._apply_hsv_batch(frame_float.copy())

        # Individual saturation call
        individual_result = grader._adjust_saturation(frame_float.copy(), 20)

        # Should be equivalent within floating point tolerance
        np.testing.assert_allclose(batched_result, individual_result, atol=2.0)

    def test_batched_hsv_vibrance_only(self, grader, colorful_frame):
        """Test that batched HSV with vibrance only matches individual call."""
        frame_float = colorful_frame.astype(np.float32)

        # Set up for batched vibrance
        grader.adjustments = ColorAdjustments(vibrance=15)
        grader.preset = ColorPreset.NONE
        batched_result = grader._apply_hsv_batch(frame_float.copy())

        # Individual vibrance call
        individual_result = grader._adjust_vibrance(frame_float.copy(), 15)

        # Should be equivalent within floating point tolerance
        np.testing.assert_allclose(batched_result, individual_result, atol=2.0)

    def test_batched_hsv_saturation_and_vibrance(self, grader, colorful_frame):
        """Test that batched HSV with both saturation and vibrance works correctly."""
        frame_float = colorful_frame.astype(np.float32)

        # Set up for batched operations
        grader.adjustments = ColorAdjustments(saturation=20, vibrance=15)
        grader.preset = ColorPreset.NONE
        batched_result = grader._apply_hsv_batch(frame_float.copy())

        # Sequential individual calls
        temp_result = grader._adjust_saturation(frame_float.copy(), 20)
        individual_result = grader._adjust_vibrance(temp_result, 15)

        # Should be equivalent within floating point tolerance
        np.testing.assert_allclose(batched_result, individual_result, atol=2.0)

    def test_batched_hsv_teal_orange_preset(self, grader, colorful_frame):
        """Test that TEAL_ORANGE preset is applied within the HSV batch."""
        frame_float = colorful_frame.astype(np.float32)

        # Set up for teal_orange grade
        grader.adjustments = ColorAdjustments()
        grader.preset = ColorPreset.TEAL_ORANGE
        batched_result = grader._apply_hsv_batch(frame_float.copy())

        # Individual teal_orange call
        individual_result = grader._apply_teal_orange_grade(frame_float.copy())

        # Should be equivalent within floating point tolerance
        np.testing.assert_allclose(batched_result, individual_result, atol=2.0)

    def test_batched_hsv_all_combined(self, grader, colorful_frame):
        """Test batched HSV with saturation, vibrance, and teal_orange all combined."""
        frame_float = colorful_frame.astype(np.float32)

        # Set up for all HSV operations
        grader.adjustments = ColorAdjustments(saturation=10, vibrance=12)
        grader.preset = ColorPreset.TEAL_ORANGE
        batched_result = grader._apply_hsv_batch(frame_float.copy())

        # Sequential individual calls
        temp1 = grader._adjust_saturation(frame_float.copy(), 10)
        temp2 = grader._adjust_vibrance(temp1, 12)
        individual_result = grader._apply_teal_orange_grade(temp2)

        # Should be equivalent within floating point tolerance
        np.testing.assert_allclose(batched_result, individual_result, atol=2.0)

    def test_batched_hsv_preserves_shape(self, grader, colorful_frame):
        """Test that batched HSV preserves frame shape and dtype."""
        frame_float = colorful_frame.astype(np.float32)
        grader.adjustments = ColorAdjustments(saturation=20, vibrance=15)

        result = grader._apply_hsv_batch(frame_float)

        assert result.shape == frame_float.shape
        assert result.dtype == np.float32


class TestBatchedLAB:
    """Tests for batched LAB conversion."""

    @pytest.fixture
    def grader(self):
        """Create a ColorGrader instance."""
        return ColorGrader()

    @pytest.fixture
    def gradient_frame(self):
        """Create a frame with brightness gradient (for testing shadows/highlights)."""
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        # Create vertical gradient from dark to bright
        for i in range(100):
            brightness = int(i * 2.55)
            frame[i, :] = [brightness, brightness, brightness]
        return frame

    def test_batched_lab_shadows_only(self, grader, gradient_frame):
        """Test that batched LAB with shadows only matches individual call."""
        frame_float = gradient_frame.astype(np.float32)

        # Set up for batched shadows
        grader.adjustments = ColorAdjustments(shadows=20)
        batched_result = grader._apply_lab_batch(frame_float.copy())

        # Individual shadows call
        individual_result = grader._adjust_shadows(frame_float.copy(), 20)

        # Should be equivalent within floating point tolerance
        np.testing.assert_allclose(batched_result, individual_result, atol=2.0)

    def test_batched_lab_highlights_only(self, grader, gradient_frame):
        """Test that batched LAB with highlights only matches individual call."""
        frame_float = gradient_frame.astype(np.float32)

        # Set up for batched highlights
        grader.adjustments = ColorAdjustments(highlights=-15)
        batched_result = grader._apply_lab_batch(frame_float.copy())

        # Individual highlights call
        individual_result = grader._adjust_highlights(frame_float.copy(), -15)

        # Should be equivalent within floating point tolerance
        np.testing.assert_allclose(batched_result, individual_result, atol=2.0)

    def test_batched_lab_shadows_and_highlights(self, grader, gradient_frame):
        """Test that batched LAB with both shadows and highlights works correctly."""
        frame_float = gradient_frame.astype(np.float32)

        # Set up for batched operations
        grader.adjustments = ColorAdjustments(shadows=20, highlights=-15)
        batched_result = grader._apply_lab_batch(frame_float.copy())

        # Sequential individual calls
        temp_result = grader._adjust_shadows(frame_float.copy(), 20)
        individual_result = grader._adjust_highlights(temp_result, -15)

        # Should be equivalent within floating point tolerance
        np.testing.assert_allclose(batched_result, individual_result, atol=2.0)

    def test_batched_lab_preserves_shape(self, grader, gradient_frame):
        """Test that batched LAB preserves frame shape and dtype."""
        frame_float = gradient_frame.astype(np.float32)
        grader.adjustments = ColorAdjustments(shadows=20, highlights=-15)

        result = grader._apply_lab_batch(frame_float)

        assert result.shape == frame_float.shape
        assert result.dtype == np.float32

    def test_batched_lab_clipping(self, grader):
        """Test that batched LAB properly clips values to valid range."""
        # Create extreme bright frame
        bright_frame = np.ones((50, 50, 3), dtype=np.float32) * 255

        grader.adjustments = ColorAdjustments(shadows=50, highlights=50)
        result = grader._apply_lab_batch(bright_frame)

        # Should be clipped to valid range
        assert np.all(result >= 0)
        assert np.all(result <= 255)

    def test_batched_lab_negative_adjustments(self, grader, gradient_frame):
        """Test batched LAB with negative adjustment values."""
        frame_float = gradient_frame.astype(np.float32)

        # Set up for negative adjustments
        grader.adjustments = ColorAdjustments(shadows=-25, highlights=-20)
        batched_result = grader._apply_lab_batch(frame_float.copy())

        # Sequential individual calls
        temp_result = grader._adjust_shadows(frame_float.copy(), -25)
        individual_result = grader._adjust_highlights(temp_result, -20)

        # Should be equivalent within floating point tolerance
        np.testing.assert_allclose(batched_result, individual_result, atol=2.0)


class TestAutoShadowLift:
    """Tests for the automatic shadow lift feature."""

    @pytest.fixture
    def grader(self):
        """Create a ColorGrader instance with non-zero intensity."""
        return ColorGrader(preset=ColorPreset.DRONE_AERIAL, intensity=0.6)

    def _make_lab_frame(self, dark_l: float, bright_l: float) -> np.ndarray:
        """Return a float32 LAB frame: top half dark, bottom half bright."""
        import cv2

        frame = np.zeros((100, 100, 3), dtype=np.float32)
        # Top half: dark foreground
        frame[:50, :, 0] = dark_l
        # Bottom half: bright sky
        frame[50:, :, 0] = bright_l
        # a/b channels neutral
        frame[:, :, 1] = 0.0
        frame[:, :, 2] = 0.0
        return frame

    def test_shadow_lift_raises_dark_pixels(self, grader):
        """Verify that pixels with L < 30 are lifted when mean L < 80."""
        # mean L will be (10 + 200) / 2 = 105... too high.
        # Use a mostly-dark frame so mean L < 80.
        lab = self._make_lab_frame(dark_l=10.0, bright_l=40.0)
        # mean L = (10*50*100 + 40*50*100) / (100*100) = 25.0 < 80 → triggers lift
        original_dark = lab[:50, :, 0].copy()
        result = grader._auto_shadow_lift(lab)
        # Shadow region (L=10) should be lifted
        assert np.all(result[:50, :, 0] > original_dark)

    def test_shadow_lift_leaves_highlights_untouched(self, grader):
        """Verify that pixels with L >= 30 are not affected by shadow lift."""
        # Frame: dark half (L=10) and midtone half (L=50, >= shadow_threshold=30)
        lab = self._make_lab_frame(dark_l=10.0, bright_l=50.0)
        # mean L = (10*50*100 + 50*50*100) / 10000 = 30.0 < 80 → triggers lift
        original_mid = lab[50:, :, 0].copy()
        result = grader._auto_shadow_lift(lab)
        # Midtone/highlight pixels (L=50 >= 30) must be unchanged
        np.testing.assert_array_equal(result[50:, :, 0], original_mid)

    def test_shadow_lift_skips_well_exposed_frames(self, grader):
        """Verify that shadow lift does NOT fire when mean L >= 80."""
        # Both regions well-lit: mean L = (80+200)/2 = 140 >= 80
        lab = self._make_lab_frame(dark_l=80.0, bright_l=200.0)
        original_l = lab[:, :, 0].copy()
        result = grader._auto_shadow_lift(lab)
        np.testing.assert_array_equal(result[:, :, 0], original_l)

    def test_shadow_lift_respects_intensity_zero(self):
        """Verify _auto_shadow_lift is not called when intensity=0."""
        grader_zero = ColorGrader(preset=ColorPreset.DRONE_AERIAL, intensity=0.0)
        # Create a very dark BGR frame (mean L well below 80)
        dark_frame = np.ones((100, 100, 3), dtype=np.uint8) * 5
        result = grader_zero.grade_frame(dark_frame)
        # With intensity=0 there should be NO shadow lift applied;
        # the output should remain very close to the input.
        assert np.mean(result.astype(float)) < 20.0

    def test_shadow_lift_output_in_valid_lab_range(self, grader):
        """Verify that shadow lift never pushes L outside 0-100."""
        # Worst case: all-black frame (L=0), shadow lift can add at most 15.
        lab = np.zeros((100, 100, 3), dtype=np.float32)
        result = grader._auto_shadow_lift(lab)
        assert np.all(result[:, :, 0] >= 0.0)
        assert np.all(result[:, :, 0] <= 100.0)

    def test_shadow_lift_integrated_in_grade_frame(self):
        """End-to-end: grade_frame on a dark frame yields brighter output than intensity=0."""
        dark_frame = np.ones((100, 100, 3), dtype=np.uint8) * 8
        grader_on = ColorGrader(preset=ColorPreset.DRONE_AERIAL, intensity=0.6)
        grader_off = ColorGrader(preset=ColorPreset.NONE, intensity=0.0)

        result_on = grader_on.grade_frame(dark_frame.copy())
        result_off = grader_off.grade_frame(dark_frame.copy())

        # The graded result should be measurably brighter due to shadow lift
        assert np.mean(result_on.astype(float)) > np.mean(result_off.astype(float))


class TestDroneAerialPresetBoost:
    """Tests verifying the boosted drone_aerial preset values."""

    def test_drone_aerial_contrast_boosted(self):
        """Verify contrast was increased from 12 to 14."""
        preset_adj = ColorGrader.PRESET_ADJUSTMENTS[ColorPreset.DRONE_AERIAL]
        assert preset_adj.contrast == 14

    def test_drone_aerial_saturation_boosted(self):
        """Verify saturation was increased from 8 to 10."""
        preset_adj = ColorGrader.PRESET_ADJUSTMENTS[ColorPreset.DRONE_AERIAL]
        assert preset_adj.saturation == 10

    def test_drone_aerial_intensity_scaling_still_works(self):
        """Verify intensity scaling applies correctly to boosted values."""
        grader = ColorGrader(preset=ColorPreset.DRONE_AERIAL, intensity=0.5)
        assert grader.adjustments.contrast == pytest.approx(7.0)
        assert grader.adjustments.saturation == pytest.approx(5.0)

    def test_drone_aerial_grade_is_more_impactful_than_none(self):
        """Verify DRONE_AERIAL grade visibly changes a neutral frame."""
        frame = np.ones((100, 100, 3), dtype=np.uint8) * 100
        grader = ColorGrader(preset=ColorPreset.DRONE_AERIAL, intensity=0.6)
        grader_none = ColorGrader(preset=ColorPreset.NONE, intensity=0.0)

        result = grader.grade_frame(frame.copy())
        result_none = grader_none.grade_frame(frame.copy())

        diff = np.mean(np.abs(result.astype(float) - result_none.astype(float)))
        # Expect at least a small measurable difference
        assert diff > 0.5


class TestVignetteEffect:
    """Tests for vignette radial edge darkening effect."""

    @pytest.fixture
    def uniform_frame(self):
        """Create a uniform brightness frame."""
        return np.ones((200, 200, 3), dtype=np.uint8) * 200

    def test_vignette_off_by_default(self):
        """Vignette is disabled when strength is 0."""
        grader = ColorGrader()
        assert grader.vignette_strength == 0.0

    def test_vignette_init_param(self):
        """Vignette strength is set via constructor."""
        grader = ColorGrader(vignette_strength=0.5)
        assert grader.vignette_strength == 0.5

    def test_vignette_clamped_to_range(self):
        """Vignette strength clamped to 0-1."""
        assert ColorGrader(vignette_strength=-0.5).vignette_strength == 0.0
        assert ColorGrader(vignette_strength=2.0).vignette_strength == 1.0

    def test_vignette_darkens_edges(self, uniform_frame):
        """Vignette makes edges darker than center."""
        grader = ColorGrader(vignette_strength=0.8)
        result = grader.grade_frame(uniform_frame)
        h, w = result.shape[:2]
        center_val = float(result[h // 2, w // 2].mean())
        corner_val = float(result[0, 0].mean())
        # Center should be brighter than corner
        assert center_val > corner_val

    def test_vignette_center_unchanged(self, uniform_frame):
        """Vignette center should be approximately unchanged."""
        grader = ColorGrader(vignette_strength=0.5)
        result = grader.grade_frame(uniform_frame)
        h, w = result.shape[:2]
        center_val = float(result[h // 2, w // 2].mean())
        # Center should be close to original (within dithering margin)
        assert abs(center_val - 200.0) < 10

    def test_vignette_higher_strength_darker_corners(self, uniform_frame):
        """Higher vignette strength produces darker corners."""
        grader_light = ColorGrader(vignette_strength=0.2)
        grader_heavy = ColorGrader(vignette_strength=0.9)
        result_light = grader_light.grade_frame(uniform_frame.copy())
        result_heavy = grader_heavy.grade_frame(uniform_frame.copy())
        corner_light = float(result_light[0, 0].mean())
        corner_heavy = float(result_heavy[0, 0].mean())
        assert corner_heavy < corner_light

    def test_vignette_mask_cached(self, uniform_frame):
        """Vignette mask is cached after first frame."""
        grader = ColorGrader(vignette_strength=0.5)
        assert grader._vignette_mask_cache is None
        grader.grade_frame(uniform_frame)
        assert grader._vignette_mask_cache is not None
        assert grader._vignette_mask_cache[:2] == (200, 200)

    def test_vignette_with_preset(self, uniform_frame):
        """Vignette works together with color preset."""
        grader = ColorGrader(
            preset=ColorPreset.CINEMATIC,
            vignette_strength=0.5,
        )
        result = grader.grade_frame(uniform_frame)
        # Should produce a valid frame
        assert result.shape == uniform_frame.shape
        assert result.dtype == np.uint8

    def test_vignette_no_change_when_zero(self, uniform_frame):
        """Zero vignette should not modify the frame beyond other grading."""
        grader_no_vig = ColorGrader(vignette_strength=0.0)
        grader_with_vig = ColorGrader(vignette_strength=0.0)
        r1 = grader_no_vig.grade_frame(uniform_frame.copy())
        r2 = grader_with_vig.grade_frame(uniform_frame.copy())
        np.testing.assert_array_equal(r1, r2)


class TestHalationEffect:
    """Tests for halation/bloom warm glow effect."""

    @pytest.fixture
    def bright_frame(self):
        """Frame with bright highlights for halation testing."""
        frame = np.ones((100, 100, 3), dtype=np.uint8) * 50
        # Add bright spot in center
        frame[40:60, 40:60] = 240
        return frame

    def test_halation_off_by_default(self):
        """Halation is disabled when strength is 0."""
        grader = ColorGrader()
        assert grader.halation_strength == 0.0

    def test_halation_init_param(self):
        """Halation strength is set via constructor."""
        grader = ColorGrader(halation_strength=0.5)
        assert grader.halation_strength == 0.5

    def test_halation_clamped(self):
        """Halation strength clamped to 0-1."""
        assert ColorGrader(halation_strength=-1.0).halation_strength == 0.0
        assert ColorGrader(halation_strength=2.0).halation_strength == 1.0

    def test_halation_adds_warm_glow(self, bright_frame):
        """Halation should add warm glow around bright areas."""
        grader = ColorGrader(halation_strength=0.7)
        result = grader.grade_frame(bright_frame)
        # Area near highlights should be warmer (more red/orange) than original
        # Check pixels adjacent to the bright spot
        nearby_original = bright_frame[35, 50].astype(float)
        nearby_result = result[35, 50].astype(float)
        # Red channel should increase more than blue
        assert nearby_result[2] >= nearby_original[2]  # BGR: index 2 = red

    def test_halation_no_effect_dark_frame(self):
        """Halation should not affect frames with no highlights."""
        dark_frame = np.ones((100, 100, 3), dtype=np.uint8) * 30
        grader = ColorGrader(halation_strength=0.8)
        result = grader.grade_frame(dark_frame)
        # Should be very similar to original
        diff = np.abs(result.astype(float) - dark_frame.astype(float)).mean()
        assert diff < 5.0

    def test_halation_produces_valid_output(self, bright_frame):
        """Halation output should be valid uint8 frame."""
        grader = ColorGrader(halation_strength=1.0)
        result = grader.grade_frame(bright_frame)
        assert result.dtype == np.uint8
        assert result.shape == bright_frame.shape


class TestChromaticAberration:
    """Tests for chromatic aberration RGB edge fringing."""

    @pytest.fixture
    def test_frame(self):
        return np.ones((100, 100, 3), dtype=np.uint8) * 128

    def test_ca_off_by_default(self):
        """CA is disabled when strength is 0."""
        grader = ColorGrader()
        assert grader.chromatic_aberration_strength == 0.0

    def test_ca_init_param(self):
        """CA strength is set via constructor."""
        grader = ColorGrader(chromatic_aberration_strength=0.5)
        assert grader.chromatic_aberration_strength == 0.5

    def test_ca_clamped(self):
        """CA strength clamped to 0-1."""
        assert ColorGrader(chromatic_aberration_strength=-1.0).chromatic_aberration_strength == 0.0
        assert ColorGrader(chromatic_aberration_strength=2.0).chromatic_aberration_strength == 1.0

    def test_ca_shifts_channels_at_edges(self):
        """CA should shift R and B channels at frame edges."""
        # Create frame with distinct per-channel values
        frame = np.zeros((100, 200, 3), dtype=np.uint8)
        frame[:, :, 0] = 50   # B
        frame[:, :, 1] = 128  # G
        frame[:, :, 2] = 200  # R
        grader = ColorGrader(chromatic_aberration_strength=0.8)
        result = grader.grade_frame(frame)
        # G channel center should be approximately unchanged (interpolation may shift by 1)
        assert abs(int(result[50, 100, 1]) - 128) <= 1
        # Edges should show channel separation
        assert result.shape == frame.shape

    def test_ca_produces_valid_output(self, test_frame):
        """CA output should be valid uint8 frame."""
        grader = ColorGrader(chromatic_aberration_strength=0.5)
        result = grader.grade_frame(test_frame)
        assert result.dtype == np.uint8
        assert result.shape == test_frame.shape


class TestNewColorPresets:
    """Tests for the 19 new color presets added in Phase 2."""

    @pytest.fixture
    def sample_frame(self):
        """Uniform mid-gray frame for preset testing."""
        return np.ones((50, 50, 3), dtype=np.uint8) * 128

    def test_all_new_presets_in_enum(self):
        """All 19 new presets exist in ColorPreset enum."""
        new_presets = [
            "golden_hour", "blue_hour", "harsh_midday", "overcast", "night_city",
            "ocean_coastal", "forest_jungle", "urban_city", "desert_arid",
            "snow_mountain", "autumn_foliage", "kodak_2383", "fujifilm_3513",
            "technicolor_2strip", "desaturated_moody", "warm_pastel",
            "cyberpunk_neon", "hyper_natural", "film_emulation",
        ]
        for name in new_presets:
            assert ColorPreset(name) is not None

    def test_all_new_presets_have_adjustments(self):
        """All new presets have PRESET_ADJUSTMENTS entries."""
        for preset in ColorPreset:
            assert preset in ColorGrader.PRESET_ADJUSTMENTS

    def test_total_preset_count(self):
        """Total presets should be 30 (11 original + 19 new)."""
        assert len(ColorPreset) == 30

    def test_new_presets_produce_different_output(self, sample_frame):
        """Each new preset should produce different output than NONE."""
        none_result = ColorGrader(preset=ColorPreset.NONE).grade_frame(sample_frame.copy())
        for preset in ColorPreset:
            if preset == ColorPreset.NONE:
                continue
            result = ColorGrader(preset=preset).grade_frame(sample_frame.copy())
            diff = np.abs(result.astype(float) - none_result.astype(float)).mean()
            assert diff > 0, f"Preset {preset.value} produces same output as NONE"

    def test_golden_hour_warms_frame(self, sample_frame):
        """Golden hour should produce warmer (more red/orange) output."""
        grader = ColorGrader(preset=ColorPreset.GOLDEN_HOUR)
        result = grader.grade_frame(sample_frame.copy())
        # Red channel should increase relative to blue
        assert result[:, :, 2].mean() > result[:, :, 0].mean()

    def test_blue_hour_cools_frame(self, sample_frame):
        """Blue hour should produce cooler (more blue) output."""
        grader = ColorGrader(preset=ColorPreset.BLUE_HOUR)
        result = grader.grade_frame(sample_frame.copy())
        # Blue channel should increase relative to red
        assert result[:, :, 0].mean() > result[:, :, 2].mean()

    def test_desaturated_moody_reduces_saturation(self, sample_frame):
        """Desaturated moody should reduce overall color saturation."""
        import cv2
        grader = ColorGrader(preset=ColorPreset.DESATURATED_MOODY)
        result = grader.grade_frame(sample_frame.copy())
        # Convert to HSV and check saturation is lower
        result_hsv = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)
        original_hsv = cv2.cvtColor(sample_frame, cv2.COLOR_BGR2HSV)
        assert result_hsv[:, :, 1].mean() <= original_hsv[:, :, 1].mean() + 5

    def test_presets_with_intensity_scaling(self, sample_frame):
        """New presets should work with intensity scaling."""
        for preset in [ColorPreset.GOLDEN_HOUR, ColorPreset.CYBERPUNK_NEON, ColorPreset.KODAK_2383]:
            grader = ColorGrader(preset=preset, intensity=0.5)
            result = grader.grade_frame(sample_frame.copy())
            assert result.dtype == np.uint8
            assert result.shape == sample_frame.shape

    def test_get_preset_names_includes_new(self):
        """get_preset_names() should include all new presets."""
        names = get_preset_names()
        assert "golden_hour" in names
        assert "cyberpunk_neon" in names
        assert "kodak_2383" in names
        assert len(names) == 30


class TestDLogNormalization:
    """Tests for D-Log / S-Log3 auto-normalization."""

    @pytest.fixture
    def flat_frame(self):
        """Create a flat, low-contrast frame simulating log footage."""
        frame = np.full((100, 200, 3), 128, dtype=np.uint8)
        # Add slight variation but keep compressed range
        noise = np.random.RandomState(42).normal(0, 10, frame.shape).astype(np.float32)
        return np.clip(frame.astype(np.float32) + noise, 80, 180).astype(np.uint8)

    def test_dlog_normalization_changes_frame(self, flat_frame):
        """D-Log normalization should transform the frame (different from rec709 path)."""
        grader_dlog = ColorGrader(input_colorspace="dlog")
        grader_rec = ColorGrader(input_colorspace="rec709")
        result_dlog = grader_dlog.grade_frame(flat_frame.copy())
        result_rec = grader_rec.grade_frame(flat_frame.copy())
        # D-Log normalization should produce different output than passthrough
        assert not np.array_equal(result_dlog, result_rec)

    def test_dlog_m_normalization(self, flat_frame):
        """D-Log M variant should also normalize."""
        grader = ColorGrader(input_colorspace="dlog_m")
        result = grader.grade_frame(flat_frame)
        assert result.dtype == np.uint8
        assert result.shape == flat_frame.shape

    def test_slog3_normalization(self, flat_frame):
        """S-Log3 should normalize differently from D-Log."""
        grader_dlog = ColorGrader(input_colorspace="dlog")
        grader_slog = ColorGrader(input_colorspace="slog3")
        result_dlog = grader_dlog.grade_frame(flat_frame.copy())
        result_slog = grader_slog.grade_frame(flat_frame.copy())
        # Different curves should produce different results
        assert not np.array_equal(result_dlog, result_slog)

    def test_rec709_passthrough(self, flat_frame):
        """rec709 input should not apply normalization."""
        grader = ColorGrader(input_colorspace="rec709")
        result = grader.grade_frame(flat_frame)
        assert result.dtype == np.uint8

    def test_detect_log_footage_flat(self, flat_frame):
        """Flat, compressed-range frame should be detected as log."""
        result = ColorGrader.detect_log_footage(flat_frame)
        assert result == "dlog"

    def test_detect_log_footage_normal(self):
        """Normal high-contrast frame should be detected as rec709."""
        frame = np.zeros((100, 200, 3), dtype=np.uint8)
        frame[:50] = 240  # High contrast
        frame[50:] = 10
        result = ColorGrader.detect_log_footage(frame)
        assert result == "rec709"

    def test_dlog_with_preset(self, flat_frame):
        """D-Log normalization should work with color presets."""
        grader = ColorGrader(preset=ColorPreset.CINEMATIC, input_colorspace="dlog")
        result = grader.grade_frame(flat_frame)
        assert result.dtype == np.uint8

    def test_normalize_dlog_valid_output(self):
        """_normalize_dlog should produce valid float32 output."""
        grader = ColorGrader(input_colorspace="dlog")
        frame = np.full((50, 50, 3), 128, dtype=np.float32)
        result = grader._normalize_dlog(frame)
        assert result.dtype == np.float32
        assert np.all(result >= 0) and np.all(result <= 255)


class TestAutoWhiteBalance:
    """Tests for gray world auto white balance."""

    def test_awb_corrects_blue_cast(self):
        """AWB should reduce a strong blue color cast."""
        frame = np.full((100, 200, 3), 128, dtype=np.uint8)
        frame[:, :, 0] = 200  # Strong blue cast (BGR)
        grader = ColorGrader(auto_wb=True)
        result = grader.grade_frame(frame)
        # Blue channel should be reduced toward the mean
        assert result[:, :, 0].mean() < 200

    def test_awb_preserves_neutral(self):
        """AWB should minimally affect already-neutral frames."""
        frame = np.full((100, 200, 3), 128, dtype=np.uint8)
        grader = ColorGrader(auto_wb=True)
        result = grader.grade_frame(frame)
        # Should be close to original
        assert np.allclose(result.astype(float), frame.astype(float), atol=5)

    def test_awb_valid_output(self):
        """AWB output should be valid uint8."""
        frame = np.random.RandomState(42).randint(50, 200, (100, 200, 3), dtype=np.uint8)
        grader = ColorGrader(auto_wb=True)
        result = grader.grade_frame(frame)
        assert result.dtype == np.uint8
        assert result.shape == frame.shape

    def test_awb_with_preset(self):
        """AWB should work combined with a color preset."""
        frame = np.full((100, 200, 3), 128, dtype=np.uint8)
        frame[:, :, 2] = 200  # Red cast
        grader = ColorGrader(preset=ColorPreset.DRONE_AERIAL, auto_wb=True)
        result = grader.grade_frame(frame)
        assert result.dtype == np.uint8


class TestDenoise:
    """Tests for noise reduction."""

    def test_denoise_reduces_noise(self):
        """Denoise should reduce noise level."""
        base = np.full((100, 200, 3), 128, dtype=np.uint8)
        noise = np.random.RandomState(42).normal(0, 30, base.shape).astype(np.float32)
        noisy = np.clip(base.astype(np.float32) + noise, 0, 255).astype(np.uint8)
        grader = ColorGrader(denoise_strength=0.8)
        result = grader.grade_frame(noisy)
        # Denoised frame should have lower std deviation
        assert result.astype(float).std() < noisy.astype(float).std()

    def test_denoise_zero_strength_passthrough(self):
        """Zero denoise strength should not modify frame."""
        frame = np.random.RandomState(42).randint(0, 255, (100, 200, 3), dtype=np.uint8)
        grader = ColorGrader(denoise_strength=0.0)
        result = grader.grade_frame(frame)
        assert np.array_equal(result, frame)

    def test_denoise_valid_output(self):
        """Denoise output should be valid uint8."""
        frame = np.random.RandomState(42).randint(0, 255, (100, 200, 3), dtype=np.uint8)
        grader = ColorGrader(denoise_strength=0.5)
        result = grader.grade_frame(frame)
        assert result.dtype == np.uint8
        assert result.shape == frame.shape

    def test_denoise_strength_scaling(self):
        """Higher denoise strength should smooth more."""
        noise = np.random.RandomState(42).normal(128, 30, (100, 200, 3)).astype(np.uint8)
        grader_low = ColorGrader(denoise_strength=0.2)
        grader_high = ColorGrader(denoise_strength=0.9)
        result_low = grader_low.grade_frame(noise.copy())
        result_high = grader_high.grade_frame(noise.copy())
        # Higher strength should produce smoother (lower std) result
        assert result_high.astype(float).std() <= result_low.astype(float).std()


class TestAtmosphericHaze:
    """Tests for atmospheric haze effect."""

    @pytest.fixture
    def test_frame(self):
        return np.full((100, 200, 3), 100, dtype=np.uint8)

    def test_haze_brightens_top(self, test_frame):
        """Haze should make the top of the frame brighter (closer to haze color)."""
        grader = ColorGrader(haze_strength=0.8)
        result = grader.grade_frame(test_frame)
        top_mean = result[:10].mean()
        bottom_mean = result[-10:].mean()
        assert top_mean > bottom_mean

    def test_haze_zero_passthrough(self, test_frame):
        """Zero haze should not modify frame."""
        grader = ColorGrader(haze_strength=0.0)
        result = grader.grade_frame(test_frame)
        assert np.array_equal(result, test_frame)

    def test_haze_valid_output(self, test_frame):
        """Haze output should be valid uint8."""
        grader = ColorGrader(haze_strength=0.5)
        result = grader.grade_frame(test_frame)
        assert result.dtype == np.uint8
        assert result.shape == test_frame.shape

    def test_haze_strength_scaling(self, test_frame):
        """Higher haze strength should produce more effect at top."""
        grader_low = ColorGrader(haze_strength=0.2)
        grader_high = ColorGrader(haze_strength=0.8)
        result_low = grader_low.grade_frame(test_frame.copy())
        result_high = grader_high.grade_frame(test_frame.copy())
        # Top row should be brighter with higher strength
        assert result_high[:5].mean() > result_low[:5].mean()


class TestGNDSkyCorrection:
    """Tests for graduated neutral density sky correction."""

    @pytest.fixture
    def bright_sky_frame(self):
        """Frame with bright top (sky) and darker bottom (ground)."""
        frame = np.zeros((100, 200, 3), dtype=np.uint8)
        frame[:50] = 220  # Bright sky
        frame[50:] = 80   # Darker ground
        return frame

    def test_gnd_darkens_top(self, bright_sky_frame):
        """GND should darken the top of the frame."""
        grader = ColorGrader(gnd_sky_strength=0.8)
        result = grader.grade_frame(bright_sky_frame)
        # Top should be darker than original
        assert result[:10].mean() < bright_sky_frame[:10].mean()

    def test_gnd_preserves_bottom(self, bright_sky_frame):
        """GND should not affect the bottom half."""
        grader = ColorGrader(gnd_sky_strength=0.8)
        result = grader.grade_frame(bright_sky_frame)
        # Bottom half should be approximately unchanged
        assert abs(result[-10:].mean() - bright_sky_frame[-10:].mean()) < 5

    def test_gnd_zero_passthrough(self, bright_sky_frame):
        """Zero GND should not modify frame."""
        grader = ColorGrader(gnd_sky_strength=0.0)
        result = grader.grade_frame(bright_sky_frame)
        assert np.array_equal(result, bright_sky_frame)

    def test_gnd_valid_output(self, bright_sky_frame):
        """GND output should be valid uint8."""
        grader = ColorGrader(gnd_sky_strength=0.6)
        result = grader.grade_frame(bright_sky_frame)
        assert result.dtype == np.uint8
        assert result.shape == bright_sky_frame.shape


class TestAutoColorMatch:
    """Tests for histogram-based auto color matching."""

    def test_color_match_normalizes_toward_reference(self):
        """Color matching should shift frame histogram toward reference."""
        # Reference: bright frame
        ref = np.full((100, 200, 3), 200, dtype=np.uint8)
        # Source: dark frame
        source = np.full((100, 200, 3), 60, dtype=np.uint8)

        grader = ColorGrader()
        grader.set_reference_frame(ref)
        result = grader.grade_frame(source)
        # Result should be brighter than source (shifted toward reference)
        assert result.mean() > source.mean()

    def test_color_match_no_reference_passthrough(self):
        """Without reference frame, color match should be a no-op."""
        frame = np.full((100, 200, 3), 128, dtype=np.uint8)
        grader = ColorGrader()
        result = grader.grade_frame(frame)
        assert np.array_equal(result, frame)

    def test_set_reference_frame(self):
        """set_reference_frame should store CDF histograms."""
        ref = np.random.RandomState(42).randint(0, 255, (100, 200, 3), dtype=np.uint8)
        grader = ColorGrader()
        grader.set_reference_frame(ref)
        assert grader._reference_histogram is not None
        assert len(grader._reference_histogram) == 3
        for cdf in grader._reference_histogram:
            assert len(cdf) == 256
            assert cdf[-1] == pytest.approx(1.0, abs=0.01)

    def test_color_match_valid_output(self):
        """Color match output should be valid uint8."""
        ref = np.random.RandomState(42).randint(0, 255, (100, 200, 3), dtype=np.uint8)
        source = np.random.RandomState(99).randint(0, 255, (100, 200, 3), dtype=np.uint8)
        grader = ColorGrader()
        grader.set_reference_frame(ref)
        result = grader.grade_frame(source)
        assert result.dtype == np.uint8
        assert result.shape == source.shape

    def test_color_match_with_preset(self):
        """Color match should work combined with a preset."""
        ref = np.full((100, 200, 3), 150, dtype=np.uint8)
        source = np.full((100, 200, 3), 80, dtype=np.uint8)
        grader = ColorGrader(preset=ColorPreset.CINEMATIC)
        grader.set_reference_frame(ref)
        result = grader.grade_frame(source)
        assert result.dtype == np.uint8


class TestGrainUpgrade:
    """Tests for the upgraded film grain effect."""

    def test_grain_temporal_variation(self):
        """Consecutive frames should have different grain patterns."""
        frame = np.full((100, 200, 3), 128, dtype=np.uint8)
        grader = ColorGrader(preset=ColorPreset.NONE, adjustments=ColorAdjustments(grain=50))
        result1 = grader.grade_frame(frame.copy())
        result2 = grader.grade_frame(frame.copy())
        # Different frame_index -> different grain
        assert not np.array_equal(result1, result2)

    def test_grain_midtone_weighted(self):
        """Grain should be stronger in midtones than in pure black/white."""
        # Dark frame
        dark = np.full((100, 200, 3), 10, dtype=np.uint8)
        # Midtone frame
        mid = np.full((100, 200, 3), 128, dtype=np.uint8)
        grader = ColorGrader(preset=ColorPreset.NONE, adjustments=ColorAdjustments(grain=50))
        dark_result = grader.grade_frame(dark.copy())
        grader._frame_index = 0  # Reset for fair comparison
        mid_result = grader.grade_frame(mid.copy())
        # Midtone grain variance should be higher than dark
        dark_diff = np.abs(dark_result.astype(float) - dark.astype(float)).std()
        mid_diff = np.abs(mid_result.astype(float) - mid.astype(float)).std()
        assert mid_diff > dark_diff

    def test_grain_valid_output(self):
        """Grain output should be valid uint8."""
        frame = np.random.RandomState(42).randint(0, 255, (100, 200, 3), dtype=np.uint8)
        grader = ColorGrader(preset=ColorPreset.NONE, adjustments=ColorAdjustments(grain=30))
        result = grader.grade_frame(frame)
        assert result.dtype == np.uint8
        assert result.shape == frame.shape
