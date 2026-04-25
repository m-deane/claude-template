"""Tests for scene_analyzer module."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from drone_reel.core.scene_analyzer import (
    analyze_scene_motion,
    analyze_scenes_batch,
    classify_motion_type,
    get_scene_sharpness,
)
from drone_reel.core.scene_detector import MotionType, SceneInfo

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_scene(
    source_file: str = "/tmp/test.mp4",
    start_time: float = 0.0,
    end_time: float = 5.0,
    score: float = 50.0,
) -> SceneInfo:
    return SceneInfo(
        start_time=start_time,
        end_time=end_time,
        duration=end_time - start_time,
        score=score,
        source_file=Path(source_file),
    )


def _make_frame(brightness: int = 128) -> np.ndarray:
    """Create a 180x320 BGR frame with uniform brightness."""
    frame = np.full((180, 320, 3), brightness, dtype=np.uint8)
    return frame


def _make_flow(dx: float = 0.0, dy: float = 0.0) -> np.ndarray:
    """Create a 180x320x2 optical flow field with uniform direction."""
    flow = np.zeros((180, 320, 2), dtype=np.float32)
    flow[..., 0] = dx
    flow[..., 1] = dy
    return flow


# ===========================================================================
# classify_motion_type
# ===========================================================================


class TestClassifyMotionType:
    """Tests for classify_motion_type()."""

    # --- STATIC ---

    def test_empty_flow_vectors_returns_static(self):
        motion_type, direction = classify_motion_type([], motion_energy=50.0)
        assert motion_type == MotionType.STATIC
        assert direction == (0.0, 0.0)

    def test_low_motion_energy_returns_static(self):
        vectors = [(1.0, 0.5), (0.8, 0.3)]
        motion_type, direction = classify_motion_type(vectors, motion_energy=5.0)
        assert motion_type == MotionType.STATIC
        assert direction == (0.0, 0.0)

    def test_low_motion_energy_at_threshold_returns_static(self):
        vectors = [(1.0, 0.0)]
        motion_type, _ = classify_motion_type(vectors, motion_energy=9.9)
        assert motion_type == MotionType.STATIC

    def test_low_magnitude_returns_static(self):
        """Vectors that average near zero magnitude -> STATIC even with energy."""
        vectors = [(0.1, 0.1), (-0.1, -0.1), (0.1, -0.1)]
        motion_type, _ = classify_motion_type(vectors, motion_energy=20.0)
        assert motion_type == MotionType.STATIC

    def test_custom_static_threshold(self):
        vectors = [(2.0, 0.0)]
        motion_type, _ = classify_motion_type(vectors, motion_energy=15.0, static_threshold=20.0)
        assert motion_type == MotionType.STATIC

    # --- PAN ---

    def test_pan_right(self):
        vectors = [(5.0, 0.0), (6.0, 0.1), (5.5, -0.1)]
        motion_type, direction = classify_motion_type(vectors, motion_energy=50.0)
        assert motion_type == MotionType.PAN_RIGHT
        assert direction[0] > 0  # positive dx

    def test_pan_left(self):
        vectors = [(-5.0, 0.0), (-6.0, 0.1), (-5.5, -0.1)]
        motion_type, direction = classify_motion_type(vectors, motion_energy=50.0)
        assert motion_type == MotionType.PAN_LEFT
        assert direction[0] < 0  # negative dx

    def test_pan_requires_horizontal_dominance(self):
        """dx must be > 1.5 * dy for PAN classification."""
        vectors = [(3.0, 2.5)] * 3  # ratio < 1.5 -> not a clean pan
        motion_type, _ = classify_motion_type(vectors, motion_energy=50.0)
        assert motion_type != MotionType.PAN_LEFT
        assert motion_type != MotionType.PAN_RIGHT

    # --- TILT ---

    def test_tilt_down(self):
        # Use consistent positive dx to avoid orbit detection triggering
        # from direction reversals in dx crossing zero
        vectors = [(0.2, 5.0), (0.3, 6.0), (0.1, 5.5)]
        motion_type, direction = classify_motion_type(vectors, motion_energy=50.0)
        assert motion_type == MotionType.TILT_DOWN
        assert direction[1] > 0  # positive dy

    def test_tilt_up(self):
        vectors = [(0.2, -5.0), (0.3, -6.0), (0.1, -5.5)]
        motion_type, direction = classify_motion_type(vectors, motion_energy=50.0)
        assert motion_type == MotionType.TILT_UP
        assert direction[1] < 0  # negative dy

    def test_tilt_requires_vertical_dominance(self):
        """dy must be > 1.5 * dx for TILT classification."""
        vectors = [(2.5, 3.0)] * 3  # ratio < 1.5
        motion_type, _ = classify_motion_type(vectors, motion_energy=50.0)
        assert motion_type != MotionType.TILT_UP
        assert motion_type != MotionType.TILT_DOWN

    # --- FPV ---

    def test_fpv_high_energy_inconsistent_flow(self):
        """FPV: low consistency (< 0.15) and high energy (> 40)."""
        # Wildly varying directions -> high std -> low consistency
        vectors = [(10.0, -10.0), (-10.0, 10.0), (10.0, 5.0), (-8.0, -12.0), (9.0, -3.0)]
        motion_type, _ = classify_motion_type(vectors, motion_energy=60.0)
        assert motion_type == MotionType.FPV

    def test_not_fpv_with_low_energy(self):
        """Inconsistent motion but low energy should not be FPV."""
        vectors = [(10.0, -10.0), (-10.0, 10.0), (10.0, 5.0)]
        motion_type, _ = classify_motion_type(vectors, motion_energy=20.0)
        assert motion_type != MotionType.FPV

    # --- ORBIT ---

    def test_orbit_cw(self):
        """Direction reversals with positive avg_dx -> ORBIT_CW."""
        vectors = [(3.0, 0.0), (-2.0, 0.0), (3.0, 0.0), (-2.0, 0.0), (3.0, 0.0)]
        motion_type, _ = classify_motion_type(vectors, motion_energy=30.0)
        assert motion_type == MotionType.ORBIT_CW

    def test_orbit_ccw(self):
        """Direction reversals with negative avg_dx -> ORBIT_CCW."""
        vectors = [(-3.0, 0.0), (2.0, 0.0), (-3.0, 0.0), (2.0, 0.0), (-3.0, 0.0)]
        motion_type, _ = classify_motion_type(vectors, motion_energy=30.0)
        assert motion_type == MotionType.ORBIT_CCW

    # --- REVEAL ---

    def test_reveal(self):
        """Direction reversals with upward avg_dy > 0.5 -> REVEAL."""
        vectors = [(3.0, 2.0), (-2.0, 1.0), (3.0, 2.0), (-2.0, 1.0), (3.0, 2.0)]
        motion_type, _ = classify_motion_type(vectors, motion_energy=30.0)
        assert motion_type == MotionType.REVEAL

    # --- FLYOVER ---

    def test_flyover(self):
        """Combined direction with avg_dy > 0 and energy > 30 -> FLYOVER."""
        # Diagonal motion that doesn't meet the 1.5x ratio for pan or tilt
        vectors = [(2.0, 2.5)] * 3
        motion_type, _ = classify_motion_type(vectors, motion_energy=35.0)
        assert motion_type == MotionType.FLYOVER

    def test_flyover_requires_sufficient_energy(self):
        """FLYOVER needs motion_energy > 30."""
        vectors = [(2.0, 2.5)] * 3
        motion_type, _ = classify_motion_type(vectors, motion_energy=20.0)
        assert motion_type != MotionType.FLYOVER

    # --- APPROACH ---

    def test_approach(self):
        """Combined direction with avg_dy < 0 and energy > 25 -> APPROACH."""
        vectors = [(2.0, -2.5)] * 3
        motion_type, _ = classify_motion_type(vectors, motion_energy=30.0)
        assert motion_type == MotionType.APPROACH

    def test_approach_requires_sufficient_energy(self):
        """APPROACH needs motion_energy > 25."""
        vectors = [(2.0, -2.5)] * 3
        motion_type, _ = classify_motion_type(vectors, motion_energy=15.0)
        assert motion_type != MotionType.APPROACH

    # --- UNKNOWN ---

    def test_unknown_fallthrough(self):
        """Motion that doesn't match any specific pattern -> UNKNOWN."""
        # Diagonal but with low energy (not FLYOVER/APPROACH) and no direction dominance
        vectors = [(2.0, -2.0)] * 3
        # avg_dy < 0 but energy <= 25 -> not APPROACH, not FLYOVER
        motion_type, _ = classify_motion_type(vectors, motion_energy=15.0)
        assert motion_type == MotionType.UNKNOWN

    # --- Direction return value ---

    def test_direction_returns_average_vector(self):
        vectors = [(2.0, 4.0), (6.0, 8.0)]
        _, direction = classify_motion_type(vectors, motion_energy=50.0)
        assert direction[0] == pytest.approx(4.0)
        assert direction[1] == pytest.approx(6.0)

    def test_static_direction_is_zero(self):
        _, direction = classify_motion_type([], motion_energy=0.0)
        assert direction == (0.0, 0.0)

    # --- Edge cases ---

    def test_single_flow_vector(self):
        """Single vector: not enough for orbit detection, should still classify."""
        vectors = [(5.0, 0.0)]
        motion_type, _ = classify_motion_type(vectors, motion_energy=20.0)
        assert motion_type == MotionType.PAN_RIGHT

    def test_two_flow_vectors(self):
        """Two vectors: not enough for orbit detection (< 3), still classifies."""
        vectors = [(5.0, 0.0), (5.0, 0.0)]
        motion_type, _ = classify_motion_type(vectors, motion_energy=20.0)
        assert motion_type == MotionType.PAN_RIGHT

    def test_exactly_at_static_threshold(self):
        """Motion energy exactly at threshold -> NOT static (< is strict)."""
        vectors = [(5.0, 0.0)]
        motion_type, _ = classify_motion_type(vectors, motion_energy=10.0)
        # The condition is `motion_energy < static_threshold`, so exactly at
        # threshold passes through to direction-based classification
        assert motion_type != MotionType.STATIC

    def test_just_above_static_threshold(self):
        """Motion energy just above threshold -> not STATIC."""
        vectors = [(5.0, 0.0)]
        motion_type, _ = classify_motion_type(vectors, motion_energy=10.1)
        assert motion_type != MotionType.STATIC


# ===========================================================================
# analyze_scene_motion
# ===========================================================================


class TestAnalyzeSceneMotion:
    """Tests for analyze_scene_motion()."""

    def _setup_mock_cap(self, mock_video_cap, fps=30.0, frames=None):
        """Set up a mock VideoCapture with given frames."""
        cap_instance = MagicMock()
        mock_video_cap.return_value = cap_instance
        cap_instance.get.return_value = fps

        if frames is None:
            frames = [_make_frame(128)] * 6

        read_returns = [(True, f) for f in frames]
        cap_instance.read.side_effect = read_returns
        return cap_instance

    @patch("drone_reel.core.scene_analyzer.cv2")
    def test_returns_five_tuple(self, mock_cv2):
        """Should return (motion_energy, brightness, shake_score, motion_type, direction)."""
        cap = MagicMock()
        mock_cv2.VideoCapture.return_value = cap
        cap.get.return_value = 30.0

        frame = _make_frame(128)
        gray = np.full((180, 320), 128, dtype=np.uint8)
        flow = _make_flow(0.0, 0.0)

        cap.read.return_value = (True, frame)
        mock_cv2.cvtColor.return_value = gray
        mock_cv2.resize.return_value = gray
        mock_cv2.calcOpticalFlowFarneback.return_value = flow
        mock_cv2.magnitude.return_value = np.zeros((180, 320), dtype=np.float32)
        mock_cv2.COLOR_BGR2GRAY = 6

        scene = _make_scene()
        result = analyze_scene_motion(scene)

        assert len(result) == 5
        motion_energy, brightness, shake_score, motion_type, direction = result
        assert isinstance(motion_energy, float)
        assert isinstance(brightness, float)
        assert isinstance(shake_score, float)
        assert isinstance(motion_type, MotionType)
        assert isinstance(direction, tuple)
        assert len(direction) == 2

    @patch("drone_reel.core.scene_analyzer.cv2")
    def test_brightness_from_frames(self, mock_cv2):
        """Brightness should reflect the mean gray pixel value."""
        cap = MagicMock()
        mock_cv2.VideoCapture.return_value = cap
        cap.get.return_value = 30.0

        bright_frame = _make_frame(200)
        gray_bright = np.full((180, 320), 200, dtype=np.uint8)
        flow = _make_flow(0.0, 0.0)

        cap.read.return_value = (True, bright_frame)
        mock_cv2.cvtColor.return_value = gray_bright
        mock_cv2.resize.return_value = gray_bright
        mock_cv2.calcOpticalFlowFarneback.return_value = flow
        mock_cv2.magnitude.return_value = np.zeros((180, 320), dtype=np.float32)
        mock_cv2.COLOR_BGR2GRAY = 6

        scene = _make_scene()
        _, brightness, _, _, _ = analyze_scene_motion(scene)

        assert brightness == pytest.approx(200.0, abs=1.0)

    @patch("drone_reel.core.scene_analyzer.cv2")
    def test_motion_energy_from_optical_flow(self, mock_cv2):
        """Non-zero flow magnitude should produce non-zero motion energy."""
        cap = MagicMock()
        mock_cv2.VideoCapture.return_value = cap
        cap.get.return_value = 30.0

        frame = _make_frame(128)
        gray = np.full((180, 320), 128, dtype=np.uint8)
        flow = _make_flow(3.0, 0.0)

        cap.read.return_value = (True, frame)
        mock_cv2.cvtColor.return_value = gray
        mock_cv2.resize.return_value = gray
        mock_cv2.calcOpticalFlowFarneback.return_value = flow

        magnitude = np.full((180, 320), 3.0, dtype=np.float32)
        mock_cv2.magnitude.return_value = magnitude
        mock_cv2.COLOR_BGR2GRAY = 6

        scene = _make_scene()
        motion_energy, _, _, _, _ = analyze_scene_motion(scene)

        assert motion_energy > 0.0

    @patch("drone_reel.core.scene_analyzer.cv2")
    def test_shake_score_from_flow_variance(self, mock_cv2):
        """Erratic flow changes produce higher shake scores."""
        cap = MagicMock()
        mock_cv2.VideoCapture.return_value = cap
        cap.get.return_value = 30.0

        frame = _make_frame(128)
        gray = np.full((180, 320), 128, dtype=np.uint8)

        # Alternate flow directions to simulate shake
        flow_right = _make_flow(5.0, 0.0)
        flow_left = _make_flow(-5.0, 0.0)

        cap.read.return_value = (True, frame)
        mock_cv2.cvtColor.return_value = gray
        mock_cv2.resize.return_value = gray
        # Alternate flow directions across frame pairs
        mock_cv2.calcOpticalFlowFarneback.side_effect = [
            flow_right,
            flow_left,
            flow_right,
            flow_left,
            flow_right,
        ]

        mag_vals = [
            np.full((180, 320), 5.0, dtype=np.float32),
            np.full((180, 320), 5.0, dtype=np.float32),
            np.full((180, 320), 5.0, dtype=np.float32),
            np.full((180, 320), 5.0, dtype=np.float32),
            np.full((180, 320), 5.0, dtype=np.float32),
        ]
        mock_cv2.magnitude.side_effect = mag_vals
        mock_cv2.COLOR_BGR2GRAY = 6

        scene = _make_scene()
        _, _, shake_score, _, _ = analyze_scene_motion(scene)

        # Alternating directions should produce some shake score
        assert shake_score > 0.0

    @patch("drone_reel.core.scene_analyzer.cv2")
    def test_exception_returns_defaults(self, mock_cv2):
        """Any exception during analysis should return safe defaults."""
        mock_cv2.VideoCapture.side_effect = RuntimeError("file not found")

        scene = _make_scene()
        result = analyze_scene_motion(scene)

        assert result == (0.0, 127.0, 0.0, MotionType.UNKNOWN, (0.0, 0.0))

    @patch("drone_reel.core.scene_analyzer.cv2")
    def test_no_readable_frames_returns_defaults(self, mock_cv2):
        """If cap.read() always fails, return defaults for energy/brightness."""
        cap = MagicMock()
        mock_cv2.VideoCapture.return_value = cap
        cap.get.return_value = 30.0
        cap.read.return_value = (False, None)

        scene = _make_scene()
        motion_energy, brightness, shake_score, motion_type, direction = analyze_scene_motion(scene)

        assert motion_energy == 0.0
        assert brightness == 127.0  # default when no brightness_values
        assert shake_score == 0.0
        assert motion_type == MotionType.STATIC

    @patch("drone_reel.core.scene_analyzer.cv2")
    def test_releases_capture(self, mock_cv2):
        """VideoCapture should be released after analysis."""
        cap = MagicMock()
        mock_cv2.VideoCapture.return_value = cap
        cap.get.return_value = 30.0
        cap.read.return_value = (True, _make_frame())

        gray = np.full((180, 320), 128, dtype=np.uint8)
        mock_cv2.cvtColor.return_value = gray
        mock_cv2.resize.return_value = gray
        mock_cv2.calcOpticalFlowFarneback.return_value = _make_flow()
        mock_cv2.magnitude.return_value = np.zeros((180, 320), dtype=np.float32)
        mock_cv2.COLOR_BGR2GRAY = 6

        scene = _make_scene()
        analyze_scene_motion(scene)

        cap.release.assert_called_once()

    @patch("drone_reel.core.scene_analyzer.cv2")
    def test_fps_fallback_to_30(self, mock_cv2):
        """If cap.get(FPS) returns 0, should fall back to 30."""
        cap = MagicMock()
        mock_cv2.VideoCapture.return_value = cap
        cap.get.return_value = 0  # falsy -> should use 30
        cap.read.return_value = (True, _make_frame())

        gray = np.full((180, 320), 128, dtype=np.uint8)
        mock_cv2.cvtColor.return_value = gray
        mock_cv2.resize.return_value = gray
        mock_cv2.calcOpticalFlowFarneback.return_value = _make_flow()
        mock_cv2.magnitude.return_value = np.zeros((180, 320), dtype=np.float32)
        mock_cv2.COLOR_BGR2GRAY = 6

        scene = _make_scene(start_time=0.0, end_time=2.0)
        result = analyze_scene_motion(scene)

        # Should not crash; should compute sample frames using fps=30
        assert len(result) == 5

    @patch("drone_reel.core.scene_analyzer.cv2")
    def test_motion_type_propagated_from_classify(self, mock_cv2):
        """Motion type returned should be determined by classify_motion_type."""
        cap = MagicMock()
        mock_cv2.VideoCapture.return_value = cap
        cap.get.return_value = 30.0

        frame = _make_frame(128)
        gray = np.full((180, 320), 128, dtype=np.uint8)
        # Consistent rightward flow -> PAN_RIGHT
        flow = _make_flow(5.0, 0.0)

        cap.read.return_value = (True, frame)
        mock_cv2.cvtColor.return_value = gray
        mock_cv2.resize.return_value = gray
        mock_cv2.calcOpticalFlowFarneback.return_value = flow
        mock_cv2.magnitude.return_value = np.full((180, 320), 5.0, dtype=np.float32)
        mock_cv2.COLOR_BGR2GRAY = 6

        scene = _make_scene()
        _, _, _, motion_type, direction = analyze_scene_motion(scene)

        assert motion_type == MotionType.PAN_RIGHT
        assert direction[0] > 0

    @patch("drone_reel.core.scene_analyzer.cv2")
    def test_short_scene_single_frame(self, mock_cv2):
        """A very short scene (start_frame == end_frame) should not crash."""
        cap = MagicMock()
        mock_cv2.VideoCapture.return_value = cap
        cap.get.return_value = 30.0
        cap.read.return_value = (True, _make_frame())

        gray = np.full((180, 320), 128, dtype=np.uint8)
        mock_cv2.cvtColor.return_value = gray
        mock_cv2.resize.return_value = gray
        mock_cv2.COLOR_BGR2GRAY = 6

        scene = _make_scene(start_time=0.0, end_time=0.03)  # ~1 frame
        result = analyze_scene_motion(scene)

        assert len(result) == 5

    @patch("drone_reel.core.scene_analyzer.cv2")
    def test_motion_energy_capped_at_100(self, mock_cv2):
        """Motion energy should be clamped to 100 max."""
        cap = MagicMock()
        mock_cv2.VideoCapture.return_value = cap
        cap.get.return_value = 30.0

        frame = _make_frame(128)
        gray = np.full((180, 320), 128, dtype=np.uint8)
        flow = _make_flow(50.0, 50.0)

        cap.read.return_value = (True, frame)
        mock_cv2.cvtColor.return_value = gray
        mock_cv2.resize.return_value = gray
        mock_cv2.calcOpticalFlowFarneback.return_value = flow
        # Very high magnitude -> energy should clamp at 100
        mock_cv2.magnitude.return_value = np.full((180, 320), 100.0, dtype=np.float32)
        mock_cv2.COLOR_BGR2GRAY = 6

        scene = _make_scene()
        motion_energy, _, _, _, _ = analyze_scene_motion(scene)

        assert motion_energy <= 100.0

    @patch("drone_reel.core.scene_analyzer.cv2")
    def test_shake_score_capped_at_100(self, mock_cv2):
        """Shake score should be clamped to 100 max."""
        cap = MagicMock()
        mock_cv2.VideoCapture.return_value = cap
        cap.get.return_value = 30.0

        frame = _make_frame(128)
        gray = np.full((180, 320), 128, dtype=np.uint8)
        flow = _make_flow(0.0, 0.0)

        cap.read.return_value = (True, frame)
        mock_cv2.cvtColor.return_value = gray
        mock_cv2.resize.return_value = gray
        mock_cv2.calcOpticalFlowFarneback.return_value = flow
        # Very high std magnitude to push shake score high
        mag = np.random.uniform(0, 200, (180, 320)).astype(np.float32)
        mock_cv2.magnitude.return_value = mag
        mock_cv2.COLOR_BGR2GRAY = 6

        scene = _make_scene()
        _, _, shake_score, _, _ = analyze_scene_motion(scene)

        assert shake_score <= 100.0


# ===========================================================================
# get_scene_sharpness
# ===========================================================================


class TestGetSceneSharpness:
    """Tests for get_scene_sharpness()."""

    @patch("drone_reel.core.scene_analyzer.cv2")
    def test_returns_laplacian_variance(self, mock_cv2):
        """Should return the variance of the Laplacian of the midpoint frame."""
        cap = MagicMock()
        mock_cv2.VideoCapture.return_value = cap
        cap.get.return_value = 30.0
        cap.read.return_value = (True, _make_frame())

        gray = np.full((180, 320), 128, dtype=np.uint8)
        mock_cv2.cvtColor.return_value = gray
        mock_cv2.COLOR_BGR2GRAY = 6
        mock_cv2.CV_64F = 6

        # Create a laplacian with known variance
        laplacian = np.array([0.0, 10.0, -10.0, 5.0, -5.0])
        mock_cv2.Laplacian.return_value = laplacian

        scene = _make_scene()
        sharpness = get_scene_sharpness(scene)

        expected_variance = float(laplacian.var())
        assert sharpness == pytest.approx(expected_variance)

    @patch("drone_reel.core.scene_analyzer.cv2")
    def test_returns_zero_on_read_failure(self, mock_cv2):
        """Should return 0.0 if frame cannot be read."""
        cap = MagicMock()
        mock_cv2.VideoCapture.return_value = cap
        cap.get.return_value = 30.0
        cap.read.return_value = (False, None)

        scene = _make_scene()
        sharpness = get_scene_sharpness(scene)

        assert sharpness == 0.0

    @patch("drone_reel.core.scene_analyzer.cv2")
    def test_returns_zero_on_exception(self, mock_cv2):
        """Should return 0.0 if any exception is raised."""
        mock_cv2.VideoCapture.side_effect = RuntimeError("corrupted file")

        scene = _make_scene()
        sharpness = get_scene_sharpness(scene)

        assert sharpness == 0.0

    @patch("drone_reel.core.scene_analyzer.cv2")
    def test_returns_zero_on_none_frame(self, mock_cv2):
        """Should return 0.0 if frame is None despite ret=True."""
        cap = MagicMock()
        mock_cv2.VideoCapture.return_value = cap
        cap.get.return_value = 30.0
        cap.read.return_value = (True, None)

        scene = _make_scene()
        sharpness = get_scene_sharpness(scene)

        assert sharpness == 0.0

    @patch("drone_reel.core.scene_analyzer.cv2")
    def test_releases_capture(self, mock_cv2):
        """VideoCapture should always be released."""
        cap = MagicMock()
        mock_cv2.VideoCapture.return_value = cap
        cap.get.return_value = 30.0
        cap.read.return_value = (True, _make_frame())

        gray = np.full((180, 320), 128, dtype=np.uint8)
        mock_cv2.cvtColor.return_value = gray
        mock_cv2.Laplacian.return_value = np.zeros((180, 320), dtype=np.float64)
        mock_cv2.COLOR_BGR2GRAY = 6
        mock_cv2.CV_64F = 6

        scene = _make_scene()
        get_scene_sharpness(scene)

        cap.release.assert_called_once()

    @patch("drone_reel.core.scene_analyzer.cv2")
    def test_uses_midpoint_frame(self, mock_cv2):
        """Should seek to the midpoint frame of the scene."""
        cap = MagicMock()
        mock_cv2.VideoCapture.return_value = cap
        cap.get.return_value = 30.0
        cap.read.return_value = (True, _make_frame())

        gray = np.full((180, 320), 128, dtype=np.uint8)
        mock_cv2.cvtColor.return_value = gray
        mock_cv2.Laplacian.return_value = np.zeros((180, 320), dtype=np.float64)
        mock_cv2.COLOR_BGR2GRAY = 6
        mock_cv2.CV_64F = 6

        scene = _make_scene(start_time=2.0, end_time=6.0)
        # midpoint = 2.0 + (4.0 / 2) = 4.0
        # mid_frame = int(4.0 * 30) = 120
        get_scene_sharpness(scene)

        cap.set.assert_called_once_with(mock_cv2.CAP_PROP_POS_FRAMES, 120)

    @patch("drone_reel.core.scene_analyzer.cv2")
    def test_fps_fallback_to_30(self, mock_cv2):
        """If FPS is 0, should fall back to 30."""
        cap = MagicMock()
        mock_cv2.VideoCapture.return_value = cap
        cap.get.return_value = 0  # falsy
        cap.read.return_value = (True, _make_frame())

        gray = np.full((180, 320), 128, dtype=np.uint8)
        mock_cv2.cvtColor.return_value = gray
        mock_cv2.Laplacian.return_value = np.zeros((180, 320), dtype=np.float64)
        mock_cv2.COLOR_BGR2GRAY = 6
        mock_cv2.CV_64F = 6

        scene = _make_scene(start_time=0.0, end_time=4.0)
        # midpoint = 2.0, with fps=30 -> frame 60
        get_scene_sharpness(scene)

        cap.set.assert_called_once_with(mock_cv2.CAP_PROP_POS_FRAMES, 60)

    @patch("drone_reel.core.scene_analyzer.cv2")
    def test_high_sharpness_value(self, mock_cv2):
        """Sharp frames should produce high variance values."""
        cap = MagicMock()
        mock_cv2.VideoCapture.return_value = cap
        cap.get.return_value = 30.0
        cap.read.return_value = (True, _make_frame())

        gray = np.full((180, 320), 128, dtype=np.uint8)
        mock_cv2.cvtColor.return_value = gray
        mock_cv2.COLOR_BGR2GRAY = 6
        mock_cv2.CV_64F = 6

        # High-variance Laplacian -> sharp
        rng = np.random.RandomState(42)
        laplacian = rng.randn(180, 320) * 50.0
        mock_cv2.Laplacian.return_value = laplacian

        scene = _make_scene()
        sharpness = get_scene_sharpness(scene)

        assert sharpness > 100.0  # high variance from edges

    @patch("drone_reel.core.scene_analyzer.cv2")
    def test_blurry_frame_low_sharpness(self, mock_cv2):
        """Uniform frames should produce near-zero sharpness."""
        cap = MagicMock()
        mock_cv2.VideoCapture.return_value = cap
        cap.get.return_value = 30.0
        cap.read.return_value = (True, _make_frame())

        gray = np.full((180, 320), 128, dtype=np.uint8)
        mock_cv2.cvtColor.return_value = gray
        mock_cv2.COLOR_BGR2GRAY = 6
        mock_cv2.CV_64F = 6

        # Uniform Laplacian -> blurry
        laplacian = np.zeros((180, 320), dtype=np.float64)
        mock_cv2.Laplacian.return_value = laplacian

        scene = _make_scene()
        sharpness = get_scene_sharpness(scene)

        assert sharpness == pytest.approx(0.0)


# ===========================================================================
# analyze_scenes_batch
# ===========================================================================


class TestAnalyzeScenesBatch:
    """Tests for analyze_scenes_batch()."""

    @patch("drone_reel.core.scene_analyzer.analyze_scene_motion")
    def test_empty_list_returns_empty_dict(self, mock_analyze):
        result = analyze_scenes_batch([])
        assert result == {}
        mock_analyze.assert_not_called()

    @patch("drone_reel.core.scene_analyzer.analyze_scene_motion")
    def test_single_scene(self, mock_analyze):
        mock_analyze.return_value = (50.0, 128.0, 10.0, MotionType.PAN_RIGHT, (3.0, 0.0))

        scene = _make_scene()
        result = analyze_scenes_batch([scene])

        assert id(scene) in result
        assert result[id(scene)]["motion_energy"] == 50.0
        assert result[id(scene)]["brightness"] == 128.0
        assert result[id(scene)]["shake_score"] == 10.0
        assert result[id(scene)]["motion_type"] == MotionType.PAN_RIGHT
        assert result[id(scene)]["motion_direction"] == (3.0, 0.0)

    @patch("drone_reel.core.scene_analyzer.analyze_scene_motion")
    def test_multiple_scenes(self, mock_analyze):
        # Use a fixed return value (not side_effect) to avoid thread-order dependence.
        mock_analyze.return_value = (50.0, 127.0, 10.0, MotionType.PAN_RIGHT, (2.0, 0.0))

        scenes = [_make_scene(f"/tmp/vid{i}.mp4") for i in range(3)]
        result = analyze_scenes_batch(scenes)

        assert len(result) == 3
        for scene in scenes:
            assert id(scene) in result
            assert result[id(scene)]["motion_type"] == MotionType.PAN_RIGHT
            assert result[id(scene)]["motion_energy"] == 50.0

    @patch("drone_reel.core.scene_analyzer.analyze_scene_motion")
    def test_calls_analyze_for_each_scene(self, mock_analyze):
        mock_analyze.return_value = (0.0, 127.0, 0.0, MotionType.UNKNOWN, (0.0, 0.0))

        scenes = [_make_scene() for _ in range(5)]
        analyze_scenes_batch(scenes)

        assert mock_analyze.call_count == 5

    @patch("drone_reel.core.scene_analyzer.analyze_scene_motion")
    def test_result_keys_are_scene_ids(self, mock_analyze):
        """Keys should be id(scene), distinct per scene object."""
        mock_analyze.return_value = (0.0, 127.0, 0.0, MotionType.UNKNOWN, (0.0, 0.0))

        scene_a = _make_scene()
        scene_b = _make_scene()
        result = analyze_scenes_batch([scene_a, scene_b])

        assert id(scene_a) in result
        assert id(scene_b) in result
        assert id(scene_a) != id(scene_b)

    @patch("drone_reel.core.scene_analyzer.analyze_scene_motion")
    def test_result_dict_keys(self, mock_analyze):
        """Each result entry should contain all expected keys."""
        mock_analyze.return_value = (42.0, 180.0, 15.0, MotionType.TILT_UP, (0.0, -3.0))

        scene = _make_scene()
        result = analyze_scenes_batch([scene])
        entry = result[id(scene)]

        expected_keys = {
            "motion_energy",
            "brightness",
            "shake_score",
            "motion_type",
            "motion_direction",
        }
        assert set(entry.keys()) == expected_keys
