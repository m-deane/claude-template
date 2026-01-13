"""Tests for video reframing module."""

import numpy as np
import pytest

from drone_reel.core.reframer import (
    Reframer,
    ReframeSettings,
    AspectRatio,
    ReframeMode,
    create_vertical_reframer,
)


class TestAspectRatio:
    """Tests for AspectRatio enum."""

    def test_vertical_ratio(self):
        """Test vertical 9:16 ratio values."""
        assert AspectRatio.VERTICAL_9_16.value == (9, 16)

    def test_square_ratio(self):
        """Test square 1:1 ratio values."""
        assert AspectRatio.SQUARE_1_1.value == (1, 1)

    def test_landscape_ratio(self):
        """Test landscape 16:9 ratio values."""
        assert AspectRatio.LANDSCAPE_16_9.value == (16, 9)


class TestReframeSettings:
    """Tests for ReframeSettings dataclass."""

    def test_default_settings(self):
        """Test default reframe settings."""
        settings = ReframeSettings()
        assert settings.target_ratio == AspectRatio.VERTICAL_9_16
        assert settings.mode == ReframeMode.SMART
        assert settings.output_width == 1080

    def test_custom_settings(self):
        """Test custom reframe settings."""
        settings = ReframeSettings(
            target_ratio=AspectRatio.SQUARE_1_1,
            mode=ReframeMode.CENTER,
            output_width=720,
        )
        assert settings.target_ratio == AspectRatio.SQUARE_1_1
        assert settings.mode == ReframeMode.CENTER
        assert settings.output_width == 720


class TestReframer:
    """Tests for Reframer class."""

    @pytest.fixture
    def landscape_frame(self):
        """Create a 16:9 landscape test frame."""
        return np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)

    @pytest.fixture
    def vertical_reframer(self):
        """Create a reframer for vertical output."""
        settings = ReframeSettings(
            target_ratio=AspectRatio.VERTICAL_9_16,
            mode=ReframeMode.CENTER,
            output_width=1080,
        )
        return Reframer(settings)

    def test_calculate_output_dimensions_vertical(self):
        """Test output dimensions for vertical aspect ratio."""
        reframer = create_vertical_reframer()
        width, height = reframer.calculate_output_dimensions(1920, 1080)

        assert width == 1080
        assert height == 1920  # 9:16 ratio

    def test_calculate_output_dimensions_square(self):
        """Test output dimensions for square aspect ratio."""
        settings = ReframeSettings(
            target_ratio=AspectRatio.SQUARE_1_1,
            output_width=1080,
        )
        reframer = Reframer(settings)
        width, height = reframer.calculate_output_dimensions(1920, 1080)

        assert width == 1080
        assert height == 1080

    def test_crop_region_center_mode(self, landscape_frame, vertical_reframer):
        """Test center crop calculation."""
        vertical_reframer.settings.mode = ReframeMode.CENTER

        output_w, output_h = vertical_reframer.calculate_output_dimensions(
            landscape_frame.shape[1], landscape_frame.shape[0]
        )

        x, y, crop_w, crop_h = vertical_reframer.calculate_crop_region(
            landscape_frame, output_w, output_h
        )

        # Crop should be centered
        expected_x = (1920 - crop_w) // 2
        expected_y = (1080 - crop_h) // 2

        assert x == expected_x
        assert y == expected_y

    def test_crop_region_bounds(self, landscape_frame, vertical_reframer):
        """Test crop region stays within frame bounds."""
        output_w, output_h = vertical_reframer.calculate_output_dimensions(
            landscape_frame.shape[1], landscape_frame.shape[0]
        )

        x, y, crop_w, crop_h = vertical_reframer.calculate_crop_region(
            landscape_frame, output_w, output_h
        )

        # Verify bounds
        assert x >= 0
        assert y >= 0
        assert x + crop_w <= landscape_frame.shape[1]
        assert y + crop_h <= landscape_frame.shape[0]

    def test_reframe_frame_output_size(self, landscape_frame, vertical_reframer):
        """Test reframed frame has correct output size."""
        result = vertical_reframer.reframe_frame(landscape_frame)

        # Should be vertical 9:16
        output_w, output_h = vertical_reframer.calculate_output_dimensions(
            landscape_frame.shape[1], landscape_frame.shape[0]
        )

        assert result.shape[1] == output_w
        assert result.shape[0] == output_h
        assert result.shape[2] == 3  # BGR channels

    def test_reframe_frame_preserves_dtype(self, landscape_frame, vertical_reframer):
        """Test reframing preserves data type."""
        result = vertical_reframer.reframe_frame(landscape_frame)
        assert result.dtype == landscape_frame.dtype

    def test_pan_mode_progression(self, landscape_frame):
        """Test pan mode changes crop position over frames."""
        settings = ReframeSettings(
            target_ratio=AspectRatio.VERTICAL_9_16,
            mode=ReframeMode.PAN,
            output_width=1080,
        )
        reframer = Reframer(settings)

        output_w, output_h = reframer.calculate_output_dimensions(
            landscape_frame.shape[1], landscape_frame.shape[0]
        )

        # Get crop at start
        x_start, _, _, _ = reframer.calculate_crop_region(
            landscape_frame, output_w, output_h,
            frame_index=0, total_frames=100
        )

        # Get crop at end
        x_end, _, _, _ = reframer.calculate_crop_region(
            landscape_frame, output_w, output_h,
            frame_index=99, total_frames=100
        )

        # Pan should have moved the crop position
        assert x_end > x_start

    def test_reset_tracking(self, vertical_reframer):
        """Test tracking reset clears history."""
        vertical_reframer._tracker_history = [(100, 100), (110, 110)]
        vertical_reframer.reset_tracking()
        assert len(vertical_reframer._tracker_history) == 0


class TestCreateVerticalReframer:
    """Tests for create_vertical_reframer helper function."""

    def test_creates_vertical_reframer(self):
        """Test helper creates properly configured reframer."""
        reframer = create_vertical_reframer()

        assert reframer.settings.target_ratio == AspectRatio.VERTICAL_9_16

    def test_custom_mode(self):
        """Test helper respects custom mode."""
        reframer = create_vertical_reframer(mode=ReframeMode.PAN)
        assert reframer.settings.mode == ReframeMode.PAN

    def test_custom_width(self):
        """Test helper respects custom output width."""
        reframer = create_vertical_reframer(output_width=720)
        assert reframer.settings.output_width == 720
