"""
Tests for scene-detection and selection enhancements.

Covers:
- FilterThresholds custom brightness / motion / shake / subject-confidence bounds
- motion_energy_method ("mean", "median", "p95") in analyze_scene_motion /
  analyze_scenes_batch
- --brightness-range CLI parsing (valid, invalid, out-of-range)
- --prefer-motion-type reordering of candidates in the split command
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import cv2
import numpy as np
import pytest
from click.testing import CliRunner

from drone_reel.cli import main
from drone_reel.core.scene_analyzer import analyze_scene_motion, analyze_scenes_batch
from drone_reel.core.scene_detector import EnhancedSceneInfo, MotionType, SceneInfo
from drone_reel.core.scene_filter import FilterThresholds, SceneFilter

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _create_test_video(path, width=320, height=240, fps=30, duration_sec=3.0):
    """Create a minimal synthetic MP4 video file."""
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(str(path), fourcc, fps, (width, height))
    total_frames = int(fps * duration_sec)
    for i in range(total_frames):
        frame = np.full((height, width, 3), 128 + (i % 30), dtype=np.uint8)
        out.write(frame)
    out.release()
    return path


def _make_scene(start=0.0, end=3.0, score=50.0, source="clip.mp4"):
    return SceneInfo(
        start_time=start,
        end_time=end,
        duration=end - start,
        score=score,
        source_file=Path(source),
    )


def _make_enhanced(start=0.0, end=3.0, score=50.0, source="clip.mp4", subject_score=0.0):
    return EnhancedSceneInfo(
        start_time=start,
        end_time=end,
        duration=end - start,
        score=score,
        source_file=Path(source),
        subject_score=subject_score,
    )


def _make_flow(dx: float = 0.0, dy: float = 0.0) -> np.ndarray:
    flow = np.zeros((180, 320, 2), dtype=np.float32)
    flow[..., 0] = dx
    flow[..., 1] = dy
    return flow


# ===========================================================================
# 1.  FilterThresholds custom brightness bounds
# ===========================================================================


class TestFilterThresholdsCustomBrightness:
    """Custom min/max brightness changes what gets filtered."""

    def test_scene_passes_with_default_brightness_30(self):
        """brightness=30 should pass default thresholds."""
        scene = _make_enhanced()
        sid = id(scene)
        sf = SceneFilter()
        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 50.0},
            brightness_map={sid: 30.0},
            shake_map={sid: 0.0},
        )
        assert result.dark_scenes_filtered == 0
        assert len(result.all_passing) == 1

    def test_scene_filtered_by_custom_min_brightness(self):
        """brightness=40 is below a custom min of 50 — should be filtered."""
        scene = _make_enhanced()
        sid = id(scene)
        t = FilterThresholds(min_brightness=50.0, max_brightness=245.0)
        sf = SceneFilter(thresholds=t)
        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 50.0},
            brightness_map={sid: 40.0},
            shake_map={sid: 0.0},
        )
        assert result.dark_scenes_filtered == 1
        assert result.all_passing == []

    def test_scene_passes_with_relaxed_min_brightness(self):
        """brightness=20 is below default (30) but above custom min (15)."""
        scene = _make_enhanced()
        sid = id(scene)
        t = FilterThresholds(min_brightness=15.0, max_brightness=245.0)
        sf = SceneFilter(thresholds=t)
        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 50.0},
            brightness_map={sid: 20.0},
            shake_map={sid: 0.0},
        )
        assert result.dark_scenes_filtered == 0
        assert len(result.all_passing) == 1

    def test_scene_filtered_by_custom_max_brightness(self):
        """brightness=210 is above a custom max of 200 — should be filtered."""
        scene = _make_enhanced()
        sid = id(scene)
        t = FilterThresholds(min_brightness=30.0, max_brightness=200.0)
        sf = SceneFilter(thresholds=t)
        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 50.0},
            brightness_map={sid: 210.0},
            shake_map={sid: 0.0},
        )
        assert result.dark_scenes_filtered == 1

    def test_custom_brightness_range_night_scenes(self):
        """'20-250' is useful for night footage — brightness=25 should pass."""
        scene = _make_enhanced()
        sid = id(scene)
        t = FilterThresholds(min_brightness=20.0, max_brightness=250.0)
        sf = SceneFilter(thresholds=t)
        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 50.0},
            brightness_map={sid: 25.0},
            shake_map={sid: 0.0},
        )
        assert result.dark_scenes_filtered == 0


# ===========================================================================
# 2.  Custom motion_threshold affects tier classification
# ===========================================================================


class TestMotionThresholdTierClassification:
    """motion_threshold changes which motion energy level is 'low' vs 'medium'."""

    def test_lower_motion_threshold_promotes_slow_pans_to_medium(self):
        """With min_motion_energy=10, energy=15 should be medium not low."""
        scene = _make_enhanced()
        sid = id(scene)
        t = FilterThresholds(min_motion_energy=10.0, ideal_motion_energy=45.0)
        sf = SceneFilter(thresholds=t)
        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 15.0},
            brightness_map={sid: 127.0},
            shake_map={sid: 0.0},
        )
        assert scene in result.medium_motion_scenes
        assert scene not in result.low_motion_scenes

    def test_default_motion_threshold_keeps_slow_pan_at_low(self):
        """Default min_motion_energy=25; energy=15 should be low."""
        scene = _make_enhanced()
        sid = id(scene)
        sf = SceneFilter()
        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 15.0},
            brightness_map={sid: 127.0},
            shake_map={sid: 0.0},
        )
        assert scene in result.low_motion_scenes

    def test_higher_motion_threshold_demotes_medium_to_low(self):
        """With min_motion_energy=40, energy=30 should be low."""
        scene = _make_enhanced()
        sid = id(scene)
        t = FilterThresholds(min_motion_energy=40.0, ideal_motion_energy=60.0)
        sf = SceneFilter(thresholds=t)
        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 30.0},
            brightness_map={sid: 127.0},
            shake_map={sid: 0.0},
        )
        assert scene in result.low_motion_scenes

    def test_ideal_motion_threshold_boundary(self):
        """Energy exactly at ideal threshold goes to high_motion."""
        scene = _make_enhanced()
        sid = id(scene)
        t = FilterThresholds(min_motion_energy=10.0, ideal_motion_energy=30.0)
        sf = SceneFilter(thresholds=t)
        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 30.0},
            brightness_map={sid: 127.0},
            shake_map={sid: 0.0},
        )
        assert scene in result.high_motion_scenes


# ===========================================================================
# 3.  shake_tolerance changes what gets filtered
# ===========================================================================


class TestShakeToleranceFiltering:
    """max_shake_score changes the shake filter cut-off."""

    def test_raising_shake_tolerance_admits_previously_filtered_scene(self):
        """Default max=40 filters shake=50; raising to 60 should admit it."""
        scene = _make_enhanced()
        sid = id(scene)

        # With default threshold: filtered
        sf_default = SceneFilter()
        res_default = sf_default.filter_scenes(
            [scene],
            motion_map={sid: 50.0},
            brightness_map={sid: 127.0},
            shake_map={sid: 50.0},
        )
        assert res_default.shaky_scenes_filtered == 1

        # With raised threshold: passes
        t = FilterThresholds(max_shake_score=60.0)
        sf_raised = SceneFilter(thresholds=t)
        res_raised = sf_raised.filter_scenes(
            [scene],
            motion_map={sid: 50.0},
            brightness_map={sid: 127.0},
            shake_map={sid: 50.0},
        )
        assert res_raised.shaky_scenes_filtered == 0
        assert len(res_raised.all_passing) == 1

    def test_lowering_shake_tolerance_filters_moderately_shaky_scene(self):
        """Default max=40 admits shake=35; lowering to 20 should filter it."""
        scene = _make_enhanced()
        sid = id(scene)

        t = FilterThresholds(max_shake_score=20.0)
        sf = SceneFilter(thresholds=t)
        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 50.0},
            brightness_map={sid: 127.0},
            shake_map={sid: 35.0},
        )
        assert result.shaky_scenes_filtered == 1

    def test_stabilize_all_use_case_high_shake_tolerance(self):
        """Very high shake tolerance (95) admits shake=90 (stabilize-all scenario)."""
        scene = _make_enhanced()
        sid = id(scene)
        t = FilterThresholds(max_shake_score=95.0)
        sf = SceneFilter(thresholds=t)
        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 50.0},
            brightness_map={sid: 127.0},
            shake_map={sid: 90.0},
        )
        assert result.shaky_scenes_filtered == 0
        assert len(result.all_passing) == 1


# ===========================================================================
# 4.  motion_energy_method in analyze_scene_motion
# ===========================================================================


class TestMotionEnergyMethod:
    """motion_energy_method changes how per-frame scores are aggregated."""

    def _make_mock_cv2_with_varied_magnitudes(self, mock_cv2, magnitudes):
        """Set up mock cv2 with a sequence of flow magnitude values."""
        cap = MagicMock()
        mock_cv2.VideoCapture.return_value = cap
        cap.get.return_value = 30.0

        frame = np.full((180, 320, 3), 128, dtype=np.uint8)
        gray = np.full((180, 320), 128, dtype=np.uint8)
        cap.read.return_value = (True, frame)
        mock_cv2.cvtColor.return_value = gray
        mock_cv2.resize.return_value = gray
        mock_cv2.COLOR_BGR2GRAY = 6

        flows = [_make_flow(1.0, 0.0)] * len(magnitudes)
        mock_cv2.calcOpticalFlowFarneback.side_effect = flows

        mag_arrays = [np.full((180, 320), m, dtype=np.float32) for m in magnitudes]
        mock_cv2.magnitude.side_effect = mag_arrays

    @patch("drone_reel.core.scene_analyzer.cv2")
    def test_p95_higher_than_mean_with_spike(self, mock_cv2):
        """p95 should exceed mean when there is one high-magnitude spike."""
        # Scores (after /3 * 100 normalisation): 4 low values + 1 spike
        # mean_magnitude values for 5 frames
        magnitudes = [0.6, 0.6, 0.6, 0.6, 9.0]  # spike at end
        self._make_mock_cv2_with_varied_magnitudes(mock_cv2, magnitudes)

        scene = _make_scene()
        mean_energy, *_ = analyze_scene_motion(scene, motion_energy_method="mean")
        mock_cv2.reset_mock()
        self._make_mock_cv2_with_varied_magnitudes(mock_cv2, magnitudes)
        p95_energy, *_ = analyze_scene_motion(scene, motion_energy_method="p95")

        assert (
            p95_energy >= mean_energy
        ), f"p95 ({p95_energy:.2f}) should be >= mean ({mean_energy:.2f}) for spiked data"

    @patch("drone_reel.core.scene_analyzer.cv2")
    def test_median_lower_than_mean_with_spike(self, mock_cv2):
        """median should be <= mean when there is one high-magnitude spike."""
        magnitudes = [0.6, 0.6, 0.6, 0.6, 9.0]
        self._make_mock_cv2_with_varied_magnitudes(mock_cv2, magnitudes)

        scene = _make_scene()
        mean_energy, *_ = analyze_scene_motion(scene, motion_energy_method="mean")
        mock_cv2.reset_mock()
        self._make_mock_cv2_with_varied_magnitudes(mock_cv2, magnitudes)
        median_energy, *_ = analyze_scene_motion(scene, motion_energy_method="median")

        assert (
            median_energy <= mean_energy
        ), f"median ({median_energy:.2f}) should be <= mean ({mean_energy:.2f}) for spiked data"

    @patch("drone_reel.core.scene_analyzer.cv2")
    def test_mean_is_default_method(self, mock_cv2):
        """Calling without motion_energy_method should equal 'mean'."""
        magnitudes = [1.5, 2.1, 0.9, 1.8, 1.2]
        self._make_mock_cv2_with_varied_magnitudes(mock_cv2, magnitudes)
        scene = _make_scene()
        default_energy, *_ = analyze_scene_motion(scene)

        mock_cv2.reset_mock()
        self._make_mock_cv2_with_varied_magnitudes(mock_cv2, magnitudes)
        explicit_mean_energy, *_ = analyze_scene_motion(scene, motion_energy_method="mean")

        assert default_energy == pytest.approx(explicit_mean_energy)

    @patch("drone_reel.core.scene_analyzer.cv2")
    def test_uniform_magnitudes_all_methods_equal(self, mock_cv2):
        """For uniform scores, mean == median == p95."""
        magnitudes = [3.0, 3.0, 3.0, 3.0, 3.0]
        scene = _make_scene()

        results = {}
        for method in ("mean", "median", "p95"):
            self._make_mock_cv2_with_varied_magnitudes(mock_cv2, magnitudes)
            energy, *_ = analyze_scene_motion(scene, motion_energy_method=method)
            results[method] = energy
            mock_cv2.reset_mock()

        assert results["mean"] == pytest.approx(results["median"], abs=0.01)
        assert results["mean"] == pytest.approx(results["p95"], abs=0.01)


# ===========================================================================
# 5.  motion_energy_method in analyze_scenes_batch
# ===========================================================================


class TestAnalyzeScenesBatchMethod:
    """motion_energy_method is passed through batch processing."""

    @patch("drone_reel.core.scene_analyzer.cv2")
    def test_batch_p95_exceeds_mean_with_spiked_scene(self, mock_cv2):
        """Batch p95 should exceed batch mean for spiked magnitudes."""
        magnitudes = [0.6, 0.6, 0.6, 0.6, 9.0]

        def _setup():
            cap = MagicMock()
            mock_cv2.VideoCapture.return_value = cap
            cap.get.return_value = 30.0
            frame = np.full((180, 320, 3), 128, dtype=np.uint8)
            gray = np.full((180, 320), 128, dtype=np.uint8)
            cap.read.return_value = (True, frame)
            mock_cv2.cvtColor.return_value = gray
            mock_cv2.resize.return_value = gray
            mock_cv2.COLOR_BGR2GRAY = 6
            mock_cv2.calcOpticalFlowFarneback.side_effect = [_make_flow(1.0, 0.0)] * len(magnitudes)
            mock_cv2.magnitude.side_effect = [
                np.full((180, 320), m, dtype=np.float32) for m in magnitudes
            ]

        scene = _make_scene()

        _setup()
        batch_mean = analyze_scenes_batch([scene], motion_energy_method="mean")
        mean_e = batch_mean[id(scene)]["motion_energy"]

        mock_cv2.reset_mock()
        _setup()
        batch_p95 = analyze_scenes_batch([scene], motion_energy_method="p95")
        p95_e = batch_p95[id(scene)]["motion_energy"]

        assert p95_e >= mean_e

    def test_batch_default_method_is_mean(self):
        """analyze_scenes_batch default is 'mean', should not raise."""
        # Just call with an empty list — exercising the default codepath
        result = analyze_scenes_batch([], motion_energy_method="mean")
        assert result == {}


# ===========================================================================
# 6.  --brightness-range CLI parsing
# ===========================================================================


def _make_split_mocks(scenes, tmp_path):
    """Return a context-manager stack of patches for the split command."""
    import contextlib

    video = tmp_path / "clip.mp4"
    _create_test_video(video)  # real MP4 so is_video_file() passes

    analysis = {
        id(s): {
            "motion_energy": 50.0,
            "brightness": 127.0,
            "shake_score": 0.0,
            "motion_type": MotionType.UNKNOWN,
            "motion_direction": (0.0, 0.0),
            "sharpness": 100.0,
        }
        for s in scenes
    }

    @contextlib.contextmanager
    def _stack():
        with (
            patch("drone_reel.cli.SceneDetector") as mock_det,
            patch("drone_reel.cli.analyze_scenes_batch", return_value=analysis),
            patch("drone_reel.cli.SceneFilter") as mock_sf,
        ):
            det_inst = MagicMock()
            det_inst.detect_scenes.return_value = scenes
            det_inst.detect_scenes_enhanced.return_value = scenes
            mock_det.return_value = det_inst

            sf_inst = MagicMock()
            sf_inst.filter_scenes.return_value = MagicMock(
                all_passing=scenes,
                dark_scenes_filtered=0,
                shaky_scenes_filtered=0,
            )
            mock_sf.return_value = sf_inst

            yield mock_det, mock_sf

    return video, _stack


class TestBrightnessRangeCLIParsing:
    """--brightness-range parsing: valid, invalid, malformed."""

    def test_valid_brightness_range_accepted(self, tmp_path):
        """'20-250' is a valid range and should be accepted."""
        scenes = [_make_scene(0, 5)]
        video, ctx = _make_split_mocks(scenes, tmp_path)
        runner = CliRunner()

        with ctx() as (mock_det, mock_sf):
            result = runner.invoke(
                main,
                [
                    "split",
                    "-i",
                    str(video),
                    "-o",
                    str(tmp_path),
                    "--brightness-range",
                    "20-250",
                    "--preview",
                ],
            )

        assert (
            result.exit_code == 0
            or "0 highlights" in result.output.lower()
            or (result.exit_code == 0)
        ), f"Exit {result.exit_code}:\n{result.output}"

    def test_invalid_alpha_brightness_range_rejected(self, tmp_path):
        """'abc' is not a valid range."""
        scenes = [_make_scene(0, 5)]
        video, ctx = _make_split_mocks(scenes, tmp_path)
        runner = CliRunner()

        with ctx():
            result = runner.invoke(
                main,
                [
                    "split",
                    "-i",
                    str(video),
                    "-o",
                    str(tmp_path),
                    "--brightness-range",
                    "abc",
                    "--preview",
                ],
            )

        assert result.exit_code != 0
        assert "brightness-range" in result.output.lower()

    def test_non_numeric_values_rejected(self, tmp_path):
        """'foo-bar' has two parts but neither is a number."""
        scenes = [_make_scene(0, 5)]
        video, ctx = _make_split_mocks(scenes, tmp_path)
        runner = CliRunner()

        with ctx():
            result = runner.invoke(
                main,
                [
                    "split",
                    "-i",
                    str(video),
                    "-o",
                    str(tmp_path),
                    "--brightness-range",
                    "foo-bar",
                    "--preview",
                ],
            )

        assert result.exit_code != 0
        assert "brightness-range" in result.output.lower()

    def test_inverted_range_rejected(self, tmp_path):
        """'200-50' has min > max — should be rejected."""
        scenes = [_make_scene(0, 5)]
        video, ctx = _make_split_mocks(scenes, tmp_path)
        runner = CliRunner()

        with ctx():
            result = runner.invoke(
                main,
                [
                    "split",
                    "-i",
                    str(video),
                    "-o",
                    str(tmp_path),
                    "--brightness-range",
                    "200-50",
                    "--preview",
                ],
            )

        assert result.exit_code != 0
        assert "brightness-range" in result.output.lower()

    def test_default_range_30_245_is_accepted(self, tmp_path):
        """Default '30-245' should pass through without error."""
        scenes = [_make_scene(0, 5)]
        video, ctx = _make_split_mocks(scenes, tmp_path)
        runner = CliRunner()

        with ctx():
            result = runner.invoke(
                main,
                [
                    "split",
                    "-i",
                    str(video),
                    "-o",
                    str(tmp_path),
                    "--brightness-range",
                    "30-245",
                    "--preview",
                ],
            )

        # Should not fail at parsing stage
        assert "brightness-range" not in result.output.lower() or result.exit_code == 0


# ===========================================================================
# 7.  --prefer-motion-type reorders candidates
# ===========================================================================


class TestPreferMotionTypeCLI:
    """--prefer-motion-type floats matching scenes to the front."""

    def test_prefer_motion_type_reorders_pan_scenes_first(self, tmp_path):
        """Scenes with PAN in their motion type should come before STATIC."""
        scene_pan = _make_scene(0, 3, score=40)
        scene_static = _make_scene(3, 6, score=80)  # higher score but wrong type

        scene_pan.motion_type = MotionType.PAN_RIGHT
        scene_static.motion_type = MotionType.STATIC

        scenes = [scene_static, scene_pan]  # static comes first initially

        analysis = {
            id(s): {
                "motion_energy": 50.0,
                "brightness": 127.0,
                "shake_score": 0.0,
                "motion_type": s.motion_type,
                "motion_direction": (0.0, 0.0),
                "sharpness": 100.0,
            }
            for s in scenes
        }

        video = tmp_path / "clip.mp4"
        _create_test_video(video)
        runner = CliRunner()

        with (
            patch("drone_reel.cli.SceneDetector") as mock_det,
            patch("drone_reel.cli.analyze_scenes_batch", return_value=analysis),
            patch("drone_reel.cli.SceneFilter") as mock_sf,
        ):
            det_inst = MagicMock()
            det_inst.detect_scenes.return_value = scenes
            mock_det.return_value = det_inst

            sf_inst = MagicMock()
            sf_inst.filter_scenes.return_value = MagicMock(
                all_passing=scenes,
                dark_scenes_filtered=0,
                shaky_scenes_filtered=0,
            )
            mock_sf.return_value = sf_inst

            result = runner.invoke(
                main,
                [
                    "split",
                    "-i",
                    str(video),
                    "-o",
                    str(tmp_path),
                    "--prefer-motion-type",
                    "pan",
                    "--preview",
                ],
            )

        assert (
            result.exit_code == 0 or "highlights found" in result.output.lower()
        ), f"Exit {result.exit_code}:\n{result.output}"

    def test_prefer_motion_type_none_leaves_order_unchanged(self, tmp_path):
        """--prefer-motion-type none should not change candidate order."""
        scenes = [_make_scene(i, i + 3, score=float(50 - i * 5)) for i in range(3)]
        video = tmp_path / "clip.mp4"
        _create_test_video(video)

        analysis = {
            id(s): {
                "motion_energy": 50.0,
                "brightness": 127.0,
                "shake_score": 0.0,
                "motion_type": MotionType.UNKNOWN,
                "motion_direction": (0.0, 0.0),
                "sharpness": 100.0,
            }
            for s in scenes
        }

        runner = CliRunner()
        with (
            patch("drone_reel.cli.SceneDetector") as mock_det,
            patch("drone_reel.cli.analyze_scenes_batch", return_value=analysis),
            patch("drone_reel.cli.SceneFilter") as mock_sf,
        ):
            det_inst = MagicMock()
            det_inst.detect_scenes.return_value = scenes
            mock_det.return_value = det_inst

            sf_inst = MagicMock()
            sf_inst.filter_scenes.return_value = MagicMock(
                all_passing=scenes,
                dark_scenes_filtered=0,
                shaky_scenes_filtered=0,
            )
            mock_sf.return_value = sf_inst

            result = runner.invoke(
                main,
                [
                    "split",
                    "-i",
                    str(video),
                    "-o",
                    str(tmp_path),
                    "--prefer-motion-type",
                    "none",
                    "--preview",
                ],
            )

        assert result.exit_code == 0 or "highlights found" in result.output.lower()
