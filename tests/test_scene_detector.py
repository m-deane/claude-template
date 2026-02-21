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

    def test_calculate_motion_optical_flow(self):
        """Test motion calculation using optical flow."""
        detector = SceneDetector()

        # Two identical frames (no motion)
        frame1 = np.ones((480, 640, 3), dtype=np.uint8) * 128
        frame2 = np.ones((480, 640, 3), dtype=np.uint8) * 128
        frame1_gray = np.ones((480, 640), dtype=np.uint8) * 128
        no_motion = detector._calculate_motion_optical_flow(frame1_gray, frame2)

        # Verify score is in valid range and low for no motion
        assert 0 <= no_motion <= 100
        assert no_motion < 50  # Should be low for identical frames

        # Create frame with simulated camera pan (consistent motion)
        frame3 = np.ones((480, 640, 3), dtype=np.uint8) * 128
        # Add some features
        frame3[:, ::20, :] = 200  # Vertical stripes
        # Shift the features to simulate motion
        frame4 = np.ones((480, 640, 3), dtype=np.uint8) * 128
        frame4[:, 10::20, :] = 200  # Shifted stripes
        frame3_gray = frame1_gray  # Use same gray for prev
        motion = detector._calculate_motion_optical_flow(frame3_gray, frame4)

        assert 0 <= motion <= 100

    def test_calculate_composition(self):
        """Test composition scoring."""
        detector = SceneDetector()

        # Test with a simple frame
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 128
        score = detector._calculate_composition(frame)

        assert 0 <= score <= 100

    def test_score_rule_of_thirds(self):
        """Test rule of thirds scoring."""
        detector = SceneDetector()

        # Create edge map with features at rule of thirds lines
        edges = np.zeros((480, 640), dtype=np.uint8)
        # Add vertical line at 1/3
        edges[:, 213] = 255
        # Add horizontal line at 2/3
        edges[320, :] = 255

        score = detector._score_rule_of_thirds(edges, 640, 480)
        assert 0 <= score <= 100

    def test_score_horizon_level(self):
        """Test horizon levelness scoring."""
        detector = SceneDetector()

        # Create edge map with horizontal line
        edges = np.zeros((480, 640), dtype=np.uint8)
        edges[240, :] = 255  # Perfectly horizontal line

        score = detector._score_horizon_level(edges, 640, 480)
        assert 0 <= score <= 100

    def test_score_leading_lines(self):
        """Test leading lines scoring."""
        detector = SceneDetector()

        # Create edge map with diagonal lines
        edges = np.zeros((480, 640), dtype=np.uint8)
        for i in range(480):
            if i < 640:
                edges[i, i] = 255  # Diagonal line

        score = detector._score_leading_lines(edges, 640, 480)
        assert 0 <= score <= 100


class TestSceneDetectorEdgeCases:
    """Tests for edge cases and error handling."""

    @pytest.fixture
    def detector(self):
        """Create a SceneDetector instance."""
        return SceneDetector()

    def test_calculate_sharpness_all_black(self, detector):
        """Test sharpness calculation on all-black frame."""
        black_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        score = detector._calculate_sharpness(black_frame)

        assert score == 0.0  # No variance in all black

    def test_calculate_sharpness_all_white(self, detector):
        """Test sharpness calculation on all-white frame."""
        white_frame = np.ones((480, 640, 3), dtype=np.uint8) * 255
        score = detector._calculate_sharpness(white_frame)

        assert score == 0.0  # No variance in all white

    def test_calculate_color_variance_monochrome(self, detector):
        """Test color variance on monochrome frame."""
        mono_frame = np.ones((480, 640, 3), dtype=np.uint8) * 100
        score = detector._calculate_color_variance(mono_frame)

        assert score < 10  # Very low variance

    def test_calculate_brightness_balance_extremes(self, detector):
        """Test brightness balance at extremes."""
        # All black
        black = np.zeros((480, 640, 3), dtype=np.uint8)
        black_score = detector._calculate_brightness_balance(black)

        # All white
        white = np.ones((480, 640, 3), dtype=np.uint8) * 255
        white_score = detector._calculate_brightness_balance(white)

        # Both should score poorly
        assert black_score < 50
        assert white_score < 50

    def test_motion_optical_flow_small_frame(self, detector):
        """Test optical flow with very small frame."""
        small_gray = np.ones((10, 10), dtype=np.uint8) * 128
        small_frame = np.ones((10, 10, 3), dtype=np.uint8) * 128

        score = detector._calculate_motion_optical_flow(small_gray, small_frame)
        assert 0 <= score <= 100

    def test_composition_edge_detection_failure(self, detector):
        """Test composition handling when edge detection produces no edges."""
        # Uniform frame should produce minimal edges
        uniform = np.ones((480, 640, 3), dtype=np.uint8) * 128
        score = detector._calculate_composition(uniform)

        assert 0 <= score <= 100


class TestSubjectDetection:
    """Tests for subject detection and hook potential."""

    @pytest.fixture
    def detector(self):
        """Create a scene detector instance."""
        return SceneDetector()

    def test_calculate_subject_score_uniform_frame(self, detector):
        """Test subject detection on uniform frame (no subjects)."""
        uniform = np.ones((480, 640, 3), dtype=np.uint8) * 128
        score, density = detector._calculate_subject_score(uniform)

        assert 0 <= score <= 100
        assert 0 <= density <= 1.0
        # Uniform frame should have low subject score
        assert score < 50

    def test_calculate_subject_score_varied_frame(self, detector):
        """Test subject detection on varied frame (realistic content)."""
        # Create a frame with varied content (simulating real scene)
        frame = np.random.randint(50, 200, (480, 640, 3), dtype=np.uint8)
        # Add some distinct bright regions
        frame[100:200, 100:200] = 250
        frame[300:400, 400:500] = 20

        score, density = detector._calculate_subject_score(frame)

        assert 0 <= score <= 100
        assert 0 <= density <= 1.0
        # Varied frame should produce a valid score
        assert score >= 0

    def test_calculate_subject_score_returns_tuple(self, detector):
        """Test that subject score returns proper tuple."""
        frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        result = detector._calculate_subject_score(frame)

        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], (int, float))
        assert isinstance(result[1], (int, float))

    def test_calculate_hook_potential_basic(self, detector):
        """Test hook potential calculation returns valid values."""
        from drone_reel.core.scene_detector import HookPotential

        frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

        hook_score, tier = detector._calculate_hook_potential(
            frame,
            subject_score=50.0,
            motion_score=50.0,
            color_score=50.0,
            composition_score=50.0,
        )

        assert 0 <= hook_score <= 100
        assert isinstance(tier, HookPotential)

    def test_calculate_hook_potential_tiers(self, detector):
        """Test hook potential tier classification."""
        from drone_reel.core.scene_detector import HookPotential

        # Create varied frame with high entropy (uniqueness)
        frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

        # High input scores should contribute to higher tier
        high_score, high_tier = detector._calculate_hook_potential(
            frame, subject_score=90, motion_score=90, color_score=90, composition_score=90
        )
        # Score should be relatively high
        assert high_score > 50

        # Low scores should yield lower tier
        low_score, low_tier = detector._calculate_hook_potential(
            frame, subject_score=10, motion_score=10, color_score=10, composition_score=10
        )
        # Low inputs should yield lower score
        assert low_score < high_score

    def test_enhanced_scene_info_new_fields(self):
        """Test that EnhancedSceneInfo has hook potential fields."""
        from pathlib import Path
        from drone_reel.core.scene_detector import EnhancedSceneInfo, HookPotential, MotionType

        scene = EnhancedSceneInfo(
            start_time=0.0,
            end_time=5.0,
            duration=5.0,
            score=80.0,
            source_file=Path("/tmp/test.mp4"),
            motion_type=MotionType.PAN_RIGHT,
            motion_direction=(1.0, 0.0),
            subject_score=75.0,
            hook_potential=70.0,
            hook_tier=HookPotential.HIGH,
            visual_interest_density=0.15,
        )

        assert scene.subject_score == 75.0
        assert scene.hook_potential == 70.0
        assert scene.hook_tier == HookPotential.HIGH
        assert scene.visual_interest_density == 0.15

    def test_hook_potential_enum_values(self):
        """Test HookPotential enum has expected values."""
        from drone_reel.core.scene_detector import HookPotential

        assert HookPotential.MAXIMUM.value == "maximum"
        assert HookPotential.HIGH.value == "high"
        assert HookPotential.MEDIUM.value == "medium"
        assert HookPotential.LOW.value == "low"
        assert HookPotential.POOR.value == "poor"


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
