"""
Comprehensive tests for enhanced ColorGrader functionality.

Tests LUT support, tone curves, selective color adjustments,
GPU acceleration, and preview mode.
"""

import tempfile
from pathlib import Path

import cv2
import numpy as np
import pytest

from drone_reel.core.color_grader import (
    ColorAdjustments,
    ColorGrader,
    ColorPreset,
    SelectiveColorAdjustments,
    ToneCurve,
)


@pytest.fixture
def test_frame():
    """Create a test frame with known colors."""
    frame = np.zeros((100, 100, 3), dtype=np.uint8)

    frame[0:25, :] = [255, 0, 0]  # Blue
    frame[25:50, :] = [0, 255, 0]  # Green
    frame[50:75, :] = [0, 0, 255]  # Red
    frame[75:100, :] = [128, 128, 128]  # Gray

    return frame


@pytest.fixture
def gradient_frame():
    """Create a gradient frame for testing tonal adjustments."""
    frame = np.zeros((256, 256, 3), dtype=np.uint8)
    gradient = np.arange(256, dtype=np.uint8)

    for i in range(256):
        frame[i, :] = gradient[i]

    return frame


@pytest.fixture
def sample_lut_file(tmp_path):
    """Create a sample .cube LUT file for testing."""
    lut_path = tmp_path / "test.cube"

    with open(lut_path, 'w') as f:
        f.write("# Test LUT\n")
        f.write("LUT_3D_SIZE 3\n")
        f.write("\n")

        for r in range(3):
            for g in range(3):
                for b in range(3):
                    f.write(f"{r/2.0} {g/2.0} {b/2.0}\n")

    return lut_path


class TestLUTSupport:
    """Test LUT loading and application."""

    def test_load_lut_valid_file(self, sample_lut_file):
        """Test loading a valid .cube LUT file."""
        grader = ColorGrader()
        lut = grader.load_lut(sample_lut_file)

        assert lut is not None
        assert lut.shape == (3, 3, 3, 3)
        assert lut.dtype == np.float32

    def test_load_lut_missing_size(self, tmp_path):
        """Test error handling for LUT without size specification."""
        lut_path = tmp_path / "invalid.cube"
        with open(lut_path, 'w') as f:
            f.write("0.0 0.0 0.0\n")

        grader = ColorGrader()
        with pytest.raises(ValueError, match="does not specify LUT_3D_SIZE"):
            grader.load_lut(lut_path)

    def test_load_lut_wrong_entry_count(self, tmp_path):
        """Test error handling for LUT with incorrect entry count."""
        lut_path = tmp_path / "invalid.cube"
        with open(lut_path, 'w') as f:
            f.write("LUT_3D_SIZE 3\n")
            f.write("0.0 0.0 0.0\n")  # Only 1 entry instead of 27

        grader = ColorGrader()
        with pytest.raises(ValueError, match="Expected 27 LUT entries"):
            grader.load_lut(lut_path)

    def test_apply_lut(self, test_frame, sample_lut_file):
        """Test LUT application to a frame."""
        grader = ColorGrader(lut_path=sample_lut_file)
        result = grader.grade_frame(test_frame)

        assert result.shape == test_frame.shape
        assert result.dtype == np.uint8
        assert not np.array_equal(result, test_frame)

    def test_lut_with_adjustments(self, test_frame, sample_lut_file):
        """Test LUT combined with other adjustments."""
        adjustments = ColorAdjustments(brightness=10, contrast=5)
        grader = ColorGrader(adjustments=adjustments, lut_path=sample_lut_file)

        result = grader.grade_frame(test_frame)

        assert result.shape == test_frame.shape
        assert result.dtype == np.uint8


class TestToneCurves:
    """Test tone curve functionality."""

    def test_default_tone_curve(self, test_frame):
        """Test that default tone curve is approximately identity.

        Note: Small variations (+/- 3 pixel values) are expected due to
        anti-banding dithering applied during color grading.
        """
        tone_curve = ToneCurve()
        grader = ColorGrader(tone_curve=tone_curve)

        result = grader.grade_frame(test_frame)

        # Allow tolerance of 3 for anti-banding dithering
        assert np.allclose(result, test_frame, atol=3)

    def test_linear_tone_curve(self, gradient_frame):
        """Test linear tone curve with different slope.

        Note: Small variations (+/- 3 pixel values) are expected due to
        anti-banding dithering applied during color grading.
        """
        tone_curve = ToneCurve(
            red_points=[(0, 0), (255, 200)],
            green_points=[(0, 0), (255, 200)],
            blue_points=[(0, 0), (255, 200)],
        )
        grader = ColorGrader(tone_curve=tone_curve)

        result = grader.grade_frame(gradient_frame)

        assert result.shape == gradient_frame.shape
        # Allow tolerance of 3 for anti-banding dithering
        assert result.max() <= 203

    def test_s_curve_tone_curve(self, gradient_frame):
        """Test S-curve for contrast enhancement."""
        tone_curve = ToneCurve(
            red_points=[(0, 0), (64, 32), (192, 223), (255, 255)],
            green_points=[(0, 0), (64, 32), (192, 223), (255, 255)],
            blue_points=[(0, 0), (64, 32), (192, 223), (255, 255)],
        )
        grader = ColorGrader(tone_curve=tone_curve)

        result = grader.grade_frame(gradient_frame)

        assert result.shape == gradient_frame.shape
        assert result.dtype == np.uint8

    def test_per_channel_curves(self, test_frame):
        """Test different curves for each channel."""
        tone_curve = ToneCurve(
            red_points=[(0, 0), (255, 255)],
            green_points=[(0, 0), (255, 200)],
            blue_points=[(0, 0), (255, 150)],
        )
        grader = ColorGrader(tone_curve=tone_curve)

        result = grader.grade_frame(test_frame)

        assert result.shape == test_frame.shape
        assert not np.array_equal(result, test_frame)

    def test_apply_curve_directly(self, gradient_frame):
        """Test apply_curve method directly."""
        tone_curve = ToneCurve(
            red_points=[(0, 50), (255, 205)],
            green_points=[(0, 50), (255, 205)],
            blue_points=[(0, 50), (255, 205)],
        )
        grader = ColorGrader(tone_curve=tone_curve)

        result = grader.apply_curve(gradient_frame.astype(np.float32))

        assert result.shape == gradient_frame.shape
        assert result.min() >= 50
        assert result.max() <= 205


class TestSelectiveColor:
    """Test selective color adjustments."""

    def test_selective_color_red_adjustment(self, test_frame):
        """Test adjusting only red colors."""
        selective = SelectiveColorAdjustments(red_sat=50)
        adjustments = ColorAdjustments(selective_color=selective)
        grader = ColorGrader(adjustments=adjustments)

        result = grader.grade_frame(test_frame)

        assert result.shape == test_frame.shape
        assert result.dtype == np.uint8

    def test_selective_color_blue_adjustment(self, test_frame):
        """Test adjusting only blue colors."""
        selective = SelectiveColorAdjustments(blue_hue=10, blue_sat=20)
        adjustments = ColorAdjustments(selective_color=selective)
        grader = ColorGrader(adjustments=adjustments)

        result = grader.grade_frame(test_frame)

        assert result.shape == test_frame.shape

    def test_selective_color_luminance(self, test_frame):
        """Test selective luminance adjustment."""
        selective = SelectiveColorAdjustments(green_lum=30)
        adjustments = ColorAdjustments(selective_color=selective)
        grader = ColorGrader(adjustments=adjustments)

        result = grader.grade_frame(test_frame)

        assert result.shape == test_frame.shape

    def test_selective_color_multiple_ranges(self, test_frame):
        """Test adjusting multiple color ranges."""
        selective = SelectiveColorAdjustments(
            red_sat=20,
            blue_sat=-10,
            green_hue=5,
        )
        adjustments = ColorAdjustments(selective_color=selective)
        grader = ColorGrader(adjustments=adjustments)

        result = grader.grade_frame(test_frame)

        assert result.shape == test_frame.shape

    def test_selective_color_all_ranges(self, test_frame):
        """Test adjustments across all color ranges."""
        selective = SelectiveColorAdjustments(
            red_sat=10,
            orange_sat=10,
            yellow_sat=10,
            green_sat=10,
            cyan_sat=10,
            blue_sat=10,
            purple_sat=10,
            magenta_sat=10,
        )
        adjustments = ColorAdjustments(selective_color=selective)
        grader = ColorGrader(adjustments=adjustments)

        result = grader.grade_frame(test_frame)

        assert result.shape == test_frame.shape


class TestShadowsHighlights:
    """Test improved shadows/highlights with LAB color space."""

    def test_shadows_adjustment_lab(self, gradient_frame):
        """Test shadows adjustment using LAB color space."""
        adjustments = ColorAdjustments(shadows=50)
        grader = ColorGrader(adjustments=adjustments)

        result = grader.grade_frame(gradient_frame)

        assert result.shape == gradient_frame.shape
        assert result[0:50].mean() > gradient_frame[0:50].mean()

    def test_highlights_adjustment_lab(self, gradient_frame):
        """Test highlights adjustment using LAB color space."""
        adjustments = ColorAdjustments(highlights=-30)
        grader = ColorGrader(adjustments=adjustments)

        result = grader.grade_frame(gradient_frame)

        assert result.shape == gradient_frame.shape
        assert result[200:256].mean() < gradient_frame[200:256].mean()

    def test_shadows_preserve_color(self, test_frame):
        """Test that shadows adjustment preserves color better."""
        adjustments = ColorAdjustments(shadows=40)
        grader = ColorGrader(adjustments=adjustments)

        result = grader.grade_frame(test_frame)

        assert result.shape == test_frame.shape
        assert result.dtype == np.uint8


class TestGrainImprovement:
    """Test improved grain implementation."""

    def test_grain_temporal_coherence(self, test_frame):
        """Test that grain changes between frames."""
        adjustments = ColorAdjustments(grain=50)
        grader = ColorGrader(adjustments=adjustments)

        result1 = grader.grade_frame(test_frame, frame_index=0)
        result2 = grader.grade_frame(test_frame, frame_index=1)

        assert not np.array_equal(result1, result2)

    def test_grain_same_seed_same_result(self, test_frame):
        """Test that same frame index produces same grain."""
        adjustments = ColorAdjustments(grain=50)
        grader1 = ColorGrader(adjustments=adjustments)
        grader2 = ColorGrader(adjustments=adjustments)

        result1 = grader1.grade_frame(test_frame, frame_index=42)
        result2 = grader2.grade_frame(test_frame, frame_index=42)

        np.testing.assert_array_equal(result1, result2)

    def test_grain_film_like_characteristics(self, gradient_frame):
        """Test that grain is stronger in midtones."""
        adjustments = ColorAdjustments(grain=80)
        grader = ColorGrader(adjustments=adjustments)

        original = gradient_frame.copy()
        result = grader.grade_frame(gradient_frame, frame_index=0)

        difference = np.abs(result.astype(np.float32) - original.astype(np.float32))
        midtone_diff = difference[100:156].mean()
        shadow_diff = difference[0:50].mean()
        highlight_diff = difference[200:256].mean()

        assert midtone_diff > shadow_diff
        assert midtone_diff > highlight_diff


class TestGPUAcceleration:
    """Test GPU acceleration functionality."""

    def test_check_gpu_available(self):
        """Test GPU availability check."""
        grader = ColorGrader()
        result = grader._check_gpu_available()

        assert isinstance(result, bool)

    def test_gpu_initialization_when_unavailable(self):
        """Test that GPU initialization fails gracefully."""
        grader = ColorGrader(use_gpu=True)

        assert isinstance(grader.use_gpu, bool)

    def test_gpu_fallback_to_cpu(self, test_frame):
        """Test that GPU falls back to CPU when operations fail."""
        grader = ColorGrader(use_gpu=True)

        result = grader.grade_frame(test_frame)

        assert result.shape == test_frame.shape
        assert result.dtype == np.uint8

    def test_gpu_basic_adjustments(self, test_frame):
        """Test basic adjustments with GPU enabled."""
        adjustments = ColorAdjustments(brightness=10, contrast=5)
        grader = ColorGrader(adjustments=adjustments, use_gpu=True)

        result = grader.grade_frame(test_frame)

        assert result.shape == test_frame.shape

    def test_gpu_vs_cpu_consistency(self, test_frame):
        """Test that GPU and CPU produce similar results."""
        adjustments = ColorAdjustments(brightness=10, contrast=5)

        grader_cpu = ColorGrader(adjustments=adjustments, use_gpu=False)
        grader_gpu = ColorGrader(adjustments=adjustments, use_gpu=True)

        result_cpu = grader_cpu.grade_frame(test_frame)
        result_gpu = grader_gpu.grade_frame(test_frame)

        np.testing.assert_allclose(result_cpu, result_gpu, rtol=0.1, atol=5)


class TestPreviewMode:
    """Test preview mode functionality."""

    def test_grade_frame_preview_default_scale(self, test_frame):
        """Test preview at default 25% scale."""
        grader = ColorGrader()
        result = grader.grade_frame_preview(test_frame)

        expected_h, expected_w = 25, 25
        assert result.shape == (expected_h, expected_w, 3)

    def test_grade_frame_preview_custom_scale(self, test_frame):
        """Test preview at custom scale."""
        grader = ColorGrader()
        result = grader.grade_frame_preview(test_frame, scale=0.5)

        expected_h, expected_w = 50, 50
        assert result.shape == (expected_h, expected_w, 3)

    def test_preview_applies_adjustments(self, test_frame):
        """Test that preview applies color adjustments."""
        adjustments = ColorAdjustments(brightness=50)
        grader = ColorGrader(adjustments=adjustments)

        result = grader.grade_frame_preview(test_frame)

        assert result.mean() > test_frame.mean()

    def test_preview_much_faster(self, gradient_frame):
        """Test that preview is significantly smaller."""
        grader = ColorGrader()

        full_result = grader.grade_frame(gradient_frame)
        preview_result = grader.grade_frame_preview(gradient_frame)

        full_pixels = full_result.shape[0] * full_result.shape[1]
        preview_pixels = preview_result.shape[0] * preview_result.shape[1]

        assert preview_pixels < full_pixels * 0.1


class TestIntegration:
    """Integration tests combining multiple features."""

    def test_lut_with_tone_curve(self, test_frame, sample_lut_file):
        """Test LUT combined with tone curve."""
        tone_curve = ToneCurve(
            red_points=[(0, 0), (255, 240)],
            green_points=[(0, 0), (255, 240)],
            blue_points=[(0, 0), (255, 240)],
        )
        grader = ColorGrader(lut_path=sample_lut_file, tone_curve=tone_curve)

        result = grader.grade_frame(test_frame)

        assert result.shape == test_frame.shape

    def test_all_adjustments_combined(self, test_frame):
        """Test all adjustment types combined."""
        selective = SelectiveColorAdjustments(red_sat=10, blue_sat=-5)
        adjustments = ColorAdjustments(
            brightness=5,
            contrast=10,
            saturation=5,
            temperature=5,
            shadows=10,
            highlights=-5,
            grain=15,
            selective_color=selective,
        )
        tone_curve = ToneCurve(
            red_points=[(0, 0), (128, 140), (255, 255)],
            green_points=[(0, 0), (128, 140), (255, 255)],
            blue_points=[(0, 0), (128, 140), (255, 255)],
        )
        grader = ColorGrader(adjustments=adjustments, tone_curve=tone_curve)

        result = grader.grade_frame(test_frame, frame_index=0)

        assert result.shape == test_frame.shape
        assert result.dtype == np.uint8

    def test_preset_with_lut(self, test_frame, sample_lut_file):
        """Test preset combined with LUT."""
        grader = ColorGrader(
            preset=ColorPreset.CINEMATIC,
            lut_path=sample_lut_file
        )

        result = grader.grade_frame(test_frame)

        assert result.shape == test_frame.shape

    def test_gpu_with_all_features(self, test_frame, sample_lut_file):
        """Test GPU mode with all features."""
        selective = SelectiveColorAdjustments(green_sat=15)
        adjustments = ColorAdjustments(
            brightness=10,
            saturation=5,
            grain=10,
            selective_color=selective,
        )
        tone_curve = ToneCurve(
            red_points=[(0, 0), (255, 255)],
            green_points=[(0, 0), (255, 240)],
            blue_points=[(0, 0), (255, 220)],
        )
        grader = ColorGrader(
            adjustments=adjustments,
            lut_path=sample_lut_file,
            tone_curve=tone_curve,
            use_gpu=True,
        )

        result = grader.grade_frame(test_frame, frame_index=0)

        assert result.shape == test_frame.shape
        assert result.dtype == np.uint8


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_frame(self):
        """Test grading an empty frame."""
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        grader = ColorGrader()

        result = grader.grade_frame(frame)

        assert result.shape == frame.shape

    def test_white_frame(self):
        """Test grading a white frame."""
        frame = np.full((100, 100, 3), 255, dtype=np.uint8)
        grader = ColorGrader()

        result = grader.grade_frame(frame)

        assert result.shape == frame.shape

    def test_single_pixel_frame(self):
        """Test grading a single pixel frame."""
        frame = np.array([[[128, 128, 128]]], dtype=np.uint8)
        grader = ColorGrader()

        result = grader.grade_frame(frame)

        assert result.shape == frame.shape

    def test_extreme_brightness(self, test_frame):
        """Test extreme brightness values."""
        adjustments = ColorAdjustments(brightness=100)
        grader = ColorGrader(adjustments=adjustments)

        result = grader.grade_frame(test_frame)

        assert result.shape == test_frame.shape
        assert result.max() == 255

    def test_extreme_contrast(self, test_frame):
        """Test extreme contrast values."""
        adjustments = ColorAdjustments(contrast=100)
        grader = ColorGrader(adjustments=adjustments)

        result = grader.grade_frame(test_frame)

        assert result.shape == test_frame.shape

    def test_large_frame(self):
        """Test grading a large frame."""
        frame = np.random.randint(0, 255, (2160, 3840, 3), dtype=np.uint8)
        grader = ColorGrader()

        result = grader.grade_frame(frame)

        assert result.shape == frame.shape

    def test_frame_index_overflow(self, test_frame):
        """Test handling of large frame indices."""
        adjustments = ColorAdjustments(grain=30)
        grader = ColorGrader(adjustments=adjustments)

        result = grader.grade_frame(test_frame, frame_index=200000)

        assert result.shape == test_frame.shape


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
