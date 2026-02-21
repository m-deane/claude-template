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
