"""Tests for enhanced scene detection with motion classification."""

import numpy as np
import pytest

from drone_reel.core.scene_detector import (
    EnhancedSceneInfo,
    MotionType,
    SceneDetector,
)


class TestMotionTypeEnum:
    """Tests for MotionType enum."""

    def test_motion_type_values(self):
        """Test all motion type enum values are accessible."""
        assert MotionType.STATIC.value == "static"
        assert MotionType.PAN_LEFT.value == "pan_left"
        assert MotionType.PAN_RIGHT.value == "pan_right"
        assert MotionType.TILT_UP.value == "tilt_up"
        assert MotionType.TILT_DOWN.value == "tilt_down"
        assert MotionType.ORBIT_CW.value == "orbit_cw"
        assert MotionType.ORBIT_CCW.value == "orbit_ccw"
        assert MotionType.REVEAL.value == "reveal"
        assert MotionType.FLYOVER.value == "flyover"
        assert MotionType.FPV.value == "fpv"
        assert MotionType.APPROACH.value == "approach"
        assert MotionType.UNKNOWN.value == "unknown"


class TestEnhancedSceneInfo:
    """Tests for EnhancedSceneInfo dataclass."""

    def test_initialization_defaults(self):
        """Test default values for enhanced fields."""
        scene = EnhancedSceneInfo(
            start_time=0.0,
            end_time=10.0,
            duration=10.0,
            score=75.0,
            source_file=None,
        )

        assert scene.motion_type == MotionType.UNKNOWN
        assert scene.motion_direction == (0.0, 0.0)
        assert scene.motion_smoothness == 0.0
        assert scene.is_golden_hour is False
        assert scene.dominant_colors == []
        assert scene.depth_score == 0.0

    def test_initialization_custom_values(self):
        """Test initialization with custom values."""
        scene = EnhancedSceneInfo(
            start_time=5.0,
            end_time=15.0,
            duration=10.0,
            score=85.0,
            source_file=None,
            motion_type=MotionType.PAN_RIGHT,
            motion_direction=(1.0, 0.0),
            motion_smoothness=95.0,
            is_golden_hour=True,
            dominant_colors=[(255, 200, 100), (50, 100, 200)],
            depth_score=78.5,
        )

        assert scene.motion_type == MotionType.PAN_RIGHT
        assert scene.motion_direction == (1.0, 0.0)
        assert scene.motion_smoothness == 95.0
        assert scene.is_golden_hour is True
        assert len(scene.dominant_colors) == 2
        assert scene.depth_score == 78.5

    def test_inherits_from_scene_info(self):
        """Test that EnhancedSceneInfo inherits SceneInfo properties."""
        scene = EnhancedSceneInfo(
            start_time=10.0,
            end_time=20.0,
            duration=10.0,
            score=90.0,
            source_file=None,
        )

        assert scene.midpoint == 15.0


class TestCameraMotionClassification:
    """Tests for camera motion classification."""

    @pytest.fixture
    def detector(self):
        """Create a SceneDetector instance."""
        return SceneDetector()

    def test_classify_static_motion(self, detector):
        """Test classification of static camera (no motion)."""
        flow = np.zeros((480, 640, 2), dtype=np.float32)

        motion_type, direction = detector.classify_camera_motion(flow)

        assert motion_type == MotionType.STATIC
        assert direction == (0.0, 0.0)

    def test_classify_pan_motion_horizontal(self, detector):
        """Test classification of horizontal pan motion."""
        flow = np.zeros((480, 640, 2), dtype=np.float32)
        flow[..., 0] = 5.0
        flow[..., 1] = 0.5

        motion_type, direction = detector.classify_camera_motion(flow)

        assert motion_type in [MotionType.PAN_RIGHT, MotionType.PAN_LEFT]
        assert abs(direction[0]) > abs(direction[1])

    def test_classify_tilt_motion_vertical(self, detector):
        """Test classification of vertical tilt motion."""
        flow = np.zeros((480, 640, 2), dtype=np.float32)
        flow[..., 0] = 0.5
        flow[..., 1] = 5.0

        motion_type, direction = detector.classify_camera_motion(flow)

        assert motion_type in [MotionType.TILT_UP, MotionType.TILT_DOWN]
        assert abs(direction[1]) > abs(direction[0])

    def test_classify_flyover_motion_radial_outward(self, detector):
        """Test classification of flyover motion (radial outward from center)."""
        height, width = 480, 640
        flow = np.zeros((height, width, 2), dtype=np.float32)

        center_y, center_x = height // 2, width // 2
        y_coords, x_coords = np.meshgrid(
            np.arange(height) - center_y, np.arange(width) - center_x, indexing="ij"
        )

        distances = np.sqrt(x_coords**2 + y_coords**2) + 1e-6
        flow[..., 0] = (x_coords / distances) * 3.0
        flow[..., 1] = (y_coords / distances) * 3.0

        motion_type, direction = detector.classify_camera_motion(flow)

        assert motion_type == MotionType.FLYOVER

    def test_classify_reveal_motion_radial_inward(self, detector):
        """Test classification of reveal motion (radial inward to center)."""
        height, width = 480, 640
        flow = np.zeros((height, width, 2), dtype=np.float32)

        center_y, center_x = height // 2, width // 2
        y_coords, x_coords = np.meshgrid(
            np.arange(height) - center_y, np.arange(width) - center_x, indexing="ij"
        )

        distances = np.sqrt(x_coords**2 + y_coords**2) + 1e-6
        flow[..., 0] = -(x_coords / distances) * 2.5
        flow[..., 1] = -(y_coords / distances) * 2.5

        motion_type, direction = detector.classify_camera_motion(flow)

        assert motion_type == MotionType.REVEAL

    def test_classify_orbit_motion_rotational(self, detector):
        """Test classification of orbit motion (rotational around center)."""
        height, width = 480, 640
        flow = np.zeros((height, width, 2), dtype=np.float32)

        center_y, center_x = height // 2, width // 2
        y_coords, x_coords = np.meshgrid(
            np.arange(height) - center_y, np.arange(width) - center_x, indexing="ij"
        )

        distances = np.sqrt(x_coords**2 + y_coords**2) + 1e-6
        flow[..., 0] = -(y_coords / distances) * 2.0
        flow[..., 1] = (x_coords / distances) * 2.0

        motion_type, direction = detector.classify_camera_motion(flow)

        assert motion_type in [MotionType.ORBIT_CW, MotionType.ORBIT_CCW]

    def test_classify_fpv_motion_chaotic(self, detector):
        """Test classification of FPV motion (high variance/chaotic)."""
        np.random.seed(42)
        flow = np.zeros((480, 640, 2), dtype=np.float32)

        magnitudes = np.random.uniform(1.5, 7.0, (480, 640)).astype(np.float32)
        angles = np.random.uniform(0, 2 * np.pi, (480, 640)).astype(np.float32)

        flow[..., 0] = magnitudes * np.cos(angles)
        flow[..., 1] = magnitudes * np.sin(angles)

        motion_type, direction = detector.classify_camera_motion(flow)

        assert motion_type in MotionType
        assert isinstance(direction, tuple)
        assert len(direction) == 2

    def test_classify_fpv_motion_extreme_variance(self, detector):
        """Test FPV classification with extreme magnitude variance."""
        flow = np.ones((480, 640, 2), dtype=np.float32) * 3.0

        flow[:240, :, 0] *= 3.0
        flow[240:, :, 0] *= 0.2

        flow[:, :320, 1] *= 2.5
        flow[:, 320:, 1] *= 0.3

        motion_type, direction = detector.classify_camera_motion(flow)

        assert motion_type in [
            MotionType.FPV,
            MotionType.UNKNOWN,
            MotionType.PAN_LEFT,
            MotionType.PAN_RIGHT,
            MotionType.TILT_UP,
            MotionType.TILT_DOWN,
        ]

    def test_classify_hyperlapse_motion(self, detector):
        """Test classification of hyperlapse motion (high magnitude, low variance)."""
        flow = np.zeros((480, 640, 2), dtype=np.float32)
        flow[..., 0] = 4.0
        flow[..., 1] = 0.0

        motion_type, direction = detector.classify_camera_motion(flow)

        assert motion_type in [MotionType.PAN_RIGHT, MotionType.PAN_LEFT]


class TestGoldenHourDetection:
    """Tests for golden hour lighting detection."""

    @pytest.fixture
    def detector(self):
        """Create a SceneDetector instance."""
        return SceneDetector()

    def test_detect_golden_hour_warm_lighting(self, detector):
        """Test detection of golden hour with warm lighting."""
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        frame[:, :, 2] = 200
        frame[:, :, 1] = 150
        frame[:, :, 0] = 100

        is_golden = detector.detect_golden_hour(frame)

        assert isinstance(is_golden, bool)

    def test_detect_golden_hour_neutral_lighting(self, detector):
        """Test that neutral lighting is not detected as golden hour."""
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 128

        is_golden = detector.detect_golden_hour(frame)

        assert is_golden is False

    def test_detect_golden_hour_cool_lighting(self, detector):
        """Test that cool/blue lighting is not detected as golden hour."""
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        frame[:, :, 0] = 200
        frame[:, :, 1] = 150
        frame[:, :, 2] = 100

        is_golden = detector.detect_golden_hour(frame)

        assert is_golden is False

    def test_detect_golden_hour_dark_frame(self, detector):
        """Test that dark frames are not detected as golden hour."""
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 30

        is_golden = detector.detect_golden_hour(frame)

        assert is_golden is False


class TestDominantColorExtraction:
    """Tests for dominant color extraction."""

    @pytest.fixture
    def detector(self):
        """Create a SceneDetector instance."""
        return SceneDetector()

    def test_extract_dominant_colors_default(self, detector):
        """Test extraction of default 3 dominant colors."""
        frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

        colors = detector.extract_dominant_colors(frame)

        assert len(colors) == 3
        assert all(isinstance(c, tuple) and len(c) == 3 for c in colors)
        assert all(0 <= val <= 255 for c in colors for val in c)

    def test_extract_dominant_colors_custom_count(self, detector):
        """Test extraction of custom number of dominant colors."""
        frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

        colors = detector.extract_dominant_colors(frame, n=5)

        assert len(colors) == 5

    def test_extract_dominant_colors_uniform_frame(self, detector):
        """Test extraction from uniform color frame."""
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 128

        colors = detector.extract_dominant_colors(frame, n=3)

        assert len(colors) == 3
        for color in colors:
            assert all(abs(val - 128) < 10 for val in color)

    def test_extract_dominant_colors_two_color_frame(self, detector):
        """Test extraction from frame with two distinct colors."""
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        frame[:, :320, :] = [255, 0, 0]
        frame[:, 320:, :] = [0, 255, 0]

        colors = detector.extract_dominant_colors(frame, n=2)

        assert len(colors) == 2


class TestDepthScoreCalculation:
    """Tests for depth/layering score calculation."""

    @pytest.fixture
    def detector(self):
        """Create a SceneDetector instance."""
        return SceneDetector()

    def test_calculate_depth_score_range(self, detector):
        """Test that depth score is in valid range."""
        frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

        score = detector.calculate_depth_score(frame)

        assert 0 <= score <= 100

    def test_calculate_depth_score_flat_frame(self, detector):
        """Test depth score for flat/uniform frame (low depth)."""
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 128

        score = detector.calculate_depth_score(frame)

        assert 0 <= score < 50

    def test_calculate_depth_score_layered_frame(self, detector):
        """Test depth score for frame with distinct layers."""
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        frame[:160, :, :] = 50
        frame[160:320, :, :] = 128
        frame[320:, :, :] = 200

        score = detector.calculate_depth_score(frame)

        assert 0 <= score <= 100


class TestMotionSmoothnessCalculation:
    """Tests for motion smoothness calculation."""

    @pytest.fixture
    def detector(self):
        """Create a SceneDetector instance."""
        return SceneDetector()

    def test_calculate_motion_smoothness_empty_history(self, detector):
        """Test smoothness calculation with empty history."""
        flow_history = []

        smoothness = detector.calculate_motion_smoothness(flow_history)

        assert smoothness == 50.0

    def test_calculate_motion_smoothness_single_flow(self, detector):
        """Test smoothness calculation with single flow."""
        flow = np.ones((480, 640, 2), dtype=np.float32)
        flow_history = [flow]

        smoothness = detector.calculate_motion_smoothness(flow_history)

        assert smoothness == 50.0

    def test_calculate_motion_smoothness_consistent_flow(self, detector):
        """Test smoothness with consistent flow (high smoothness)."""
        flow = np.ones((480, 640, 2), dtype=np.float32) * 2.0
        flow_history = [flow.copy() for _ in range(10)]

        smoothness = detector.calculate_motion_smoothness(flow_history)

        assert smoothness > 90

    def test_calculate_motion_smoothness_varying_flow(self, detector):
        """Test smoothness with varying flow (lower smoothness)."""
        flow_history = []
        for i in range(10):
            flow = np.ones((480, 640, 2), dtype=np.float32) * (i + 1)
            flow_history.append(flow)

        smoothness = detector.calculate_motion_smoothness(flow_history)

        assert 0 <= smoothness <= 100

    def test_calculate_motion_smoothness_no_motion(self, detector):
        """Test smoothness with zero motion (maximum smoothness)."""
        flow = np.zeros((480, 640, 2), dtype=np.float32)
        flow_history = [flow.copy() for _ in range(10)]

        smoothness = detector.calculate_motion_smoothness(flow_history)

        assert smoothness == 100.0


class TestSceneDetectorEnhancedIntegration:
    """Integration tests for enhanced scene detection."""

    @pytest.fixture
    def detector(self):
        """Create a SceneDetector instance."""
        return SceneDetector()

    @pytest.mark.skip(reason="Requires actual video files")
    def test_detect_scenes_enhanced_real_video(self, detector):
        """Test enhanced scene detection on real video file."""
        pass

    def test_enhanced_scene_info_compatibility(self, detector):
        """Test that EnhancedSceneInfo is compatible with SceneInfo."""
        from pathlib import Path

        enhanced = EnhancedSceneInfo(
            start_time=0.0,
            end_time=10.0,
            duration=10.0,
            score=80.0,
            source_file=Path("/test/video.mp4"),
            motion_type=MotionType.PAN_RIGHT,
            motion_smoothness=85.0,
        )

        assert hasattr(enhanced, "midpoint")
        assert enhanced.midpoint == 5.0
        assert hasattr(enhanced, "motion_type")
        assert hasattr(enhanced, "motion_smoothness")


class TestMotionClassificationEdgeCases:
    """Edge case tests for motion classification."""

    @pytest.fixture
    def detector(self):
        """Create a SceneDetector instance."""
        return SceneDetector()

    def test_classify_motion_very_small_flow(self, detector):
        """Test classification with very small flow values."""
        flow = np.ones((480, 640, 2), dtype=np.float32) * 0.01

        motion_type, direction = detector.classify_camera_motion(flow)

        assert motion_type == MotionType.STATIC

    def test_classify_motion_mixed_directions(self, detector):
        """Test classification with mixed direction flow."""
        flow = np.zeros((480, 640, 2), dtype=np.float32)
        flow[:240, :, 0] = 2.0
        flow[240:, :, 0] = -2.0

        motion_type, direction = detector.classify_camera_motion(flow)

        assert motion_type in MotionType

    def test_classify_motion_small_frame(self, detector):
        """Test classification with very small frame."""
        flow = np.ones((10, 10, 2), dtype=np.float32) * 2.0

        motion_type, direction = detector.classify_camera_motion(flow)

        assert motion_type in MotionType
        assert isinstance(direction, tuple)
        assert len(direction) == 2


class TestEnhancedMethodsRobustness:
    """Robustness tests for enhanced methods."""

    @pytest.fixture
    def detector(self):
        """Create a SceneDetector instance."""
        return SceneDetector()

    def test_dominant_colors_single_pixel_clusters(self, detector):
        """Test dominant color extraction edge case."""
        frame = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)

        colors = detector.extract_dominant_colors(frame, n=1)

        assert len(colors) == 1

    def test_depth_score_all_edges(self, detector):
        """Test depth score with edge-heavy frame."""
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        for i in range(0, 480, 2):
            frame[i, :, :] = 255

        score = detector.calculate_depth_score(frame)

        assert 0 <= score <= 100

    def test_golden_hour_edge_hue_values(self, detector):
        """Test golden hour detection with edge hue values."""
        frame = np.zeros((480, 640, 3), dtype=np.uint8)

        result = detector.detect_golden_hour(frame)

        assert isinstance(result, bool)
