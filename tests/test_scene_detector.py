"""Tests for scene detection module."""

import numpy as np
import pytest

from drone_reel.core.scene_detector import SceneDetector, SceneInfo


class TestSceneInfo:
    """Tests for SceneInfo dataclass."""

    def test_midpoint_calculation(self):
        """Test midpoint property calculates correctly."""
        scene = SceneInfo(
            start_time=10.0,
            end_time=20.0,
            duration=10.0,
            score=75.0,
            source_file=None,
        )
        assert scene.midpoint == 15.0

    def test_midpoint_short_scene(self):
        """Test midpoint for short scenes."""
        scene = SceneInfo(
            start_time=0.0,
            end_time=2.0,
            duration=2.0,
            score=50.0,
            source_file=None,
        )
        assert scene.midpoint == 1.0


class TestSceneDetector:
    """Tests for SceneDetector class."""

    def test_initialization_defaults(self):
        """Test default initialization values."""
        detector = SceneDetector()
        assert detector.threshold == 27.0
        assert detector.min_scene_length == 1.0
        assert detector.max_scene_length == 10.0

    def test_initialization_custom(self):
        """Test custom initialization values."""
        detector = SceneDetector(
            threshold=30.0,
            min_scene_length=2.0,
            max_scene_length=5.0,
        )
        assert detector.threshold == 30.0
        assert detector.min_scene_length == 2.0
        assert detector.max_scene_length == 5.0

    def test_calculate_sharpness(self):
        """Test sharpness calculation on synthetic image."""
        detector = SceneDetector()

        # Sharp image (high frequency)
        sharp_img = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        sharp_score = detector._calculate_sharpness(sharp_img)
        assert 0 <= sharp_score <= 100

        # Blurry image (uniform)
        blurry_img = np.ones((480, 640, 3), dtype=np.uint8) * 128
        blurry_score = detector._calculate_sharpness(blurry_img)

        # Sharp should score higher than blurry
        assert sharp_score > blurry_score

    def test_calculate_color_variance(self):
        """Test color variance calculation."""
        detector = SceneDetector()

        # Colorful image
        colorful = np.zeros((480, 640, 3), dtype=np.uint8)
        colorful[:, :320, 0] = 255  # Blue half
        colorful[:, 320:, 2] = 255  # Red half
        colorful_score = detector._calculate_color_variance(colorful)

        # Gray image
        gray = np.ones((480, 640, 3), dtype=np.uint8) * 128
        gray_score = detector._calculate_color_variance(gray)

        assert colorful_score > gray_score

    def test_calculate_brightness_balance(self):
        """Test brightness balance calculation."""
        detector = SceneDetector()

        # Well-lit image
        balanced = np.ones((480, 640, 3), dtype=np.uint8) * 127
        balanced_score = detector._calculate_brightness_balance(balanced)

        # Dark image
        dark = np.ones((480, 640, 3), dtype=np.uint8) * 30
        dark_score = detector._calculate_brightness_balance(dark)

        # Overexposed image
        bright = np.ones((480, 640, 3), dtype=np.uint8) * 250
        bright_score = detector._calculate_brightness_balance(bright)

        # Balanced should score highest
        assert balanced_score > dark_score
        assert balanced_score > bright_score

    def test_calculate_motion(self):
        """Test motion calculation between frames."""
        detector = SceneDetector()

        # Two identical frames (no motion)
        frame1 = np.ones((480, 640, 3), dtype=np.uint8) * 128
        frame2 = np.ones((480, 640, 3), dtype=np.uint8) * 128
        no_motion = detector._calculate_motion(frame1, frame2)

        # Two different frames (motion)
        frame3 = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        motion = detector._calculate_motion(frame1, frame3)

        assert motion > no_motion


class TestSceneDetectorIntegration:
    """Integration tests requiring video files."""

    @pytest.mark.skip(reason="Requires actual video files")
    def test_detect_scenes_real_video(self):
        """Test scene detection on real video file."""
        pass

    @pytest.mark.skip(reason="Requires actual video files")
    def test_get_top_scenes(self):
        """Test getting top scenes from multiple videos."""
        pass
