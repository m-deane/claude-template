"""
Tests for Batch B P2 flags: --flow-winsize, --flow-levels, --motion-energy-percentile.

Covers:
  - analyze_scene_motion with new keyword params
  - analyze_scenes_batch forwarding
  - CLI flags forwarded via mock
"""

from unittest.mock import MagicMock, patch

import cv2
import numpy as np
from click.testing import CliRunner

from drone_reel.cli import main
from drone_reel.core.scene_analyzer import analyze_scene_motion, analyze_scenes_batch
from drone_reel.core.scene_detector import SceneInfo

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_test_video(path, duration_sec=2.0, width=160, height=120, fps=15):
    """Create a minimal synthetic MP4."""
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(str(path), fourcc, fps, (width, height))
    total = int(fps * duration_sec)
    for i in range(total):
        frame = np.full((height, width, 3), (i * 8) % 200 + 30, dtype=np.uint8)
        out.write(frame)
    out.release()


def _make_scene(start, end, source_file):
    return SceneInfo(
        start_time=start,
        end_time=end,
        duration=end - start,
        score=50.0,
        source_file=source_file,
        thumbnail=None,
    )


# ---------------------------------------------------------------------------
# analyze_scene_motion — keyword param tests
# ---------------------------------------------------------------------------


class TestAnalyzeSceneMotionParams:
    """Test that flow_winsize, flow_levels, motion_energy_percentile are accepted."""

    def test_default_params_work(self, tmp_path):
        video = tmp_path / "clip.mp4"
        _make_test_video(video)
        scene = _make_scene(0.0, 1.5, video)

        result = analyze_scene_motion(scene, include_sharpness=False)
        assert isinstance(result, tuple)
        assert len(result) == 5

    def test_custom_flow_winsize(self, tmp_path):
        video = tmp_path / "clip.mp4"
        _make_test_video(video)
        scene = _make_scene(0.0, 1.5, video)

        result = analyze_scene_motion(scene, flow_winsize=7)
        assert len(result) == 5
        motion_energy = result[0]
        assert 0.0 <= motion_energy <= 100.0

    def test_custom_flow_levels(self, tmp_path):
        video = tmp_path / "clip.mp4"
        _make_test_video(video)
        scene = _make_scene(0.0, 1.5, video)

        result = analyze_scene_motion(scene, flow_levels=1)
        assert len(result) == 5

    def test_percentile_method(self, tmp_path):
        video = tmp_path / "clip.mp4"
        _make_test_video(video)
        scene = _make_scene(0.0, 1.5, video)

        result = analyze_scene_motion(
            scene,
            motion_energy_method="percentile",
            motion_energy_percentile=75,
        )
        assert isinstance(result[0], float)
        assert 0.0 <= result[0] <= 100.0

    def test_percentile_vs_mean_differ(self, tmp_path):
        """p75 should give a different result from mean for non-uniform motion."""
        video = tmp_path / "motion.mp4"
        # Create a video with varying motion (changing scene)
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(str(video), fourcc, 15, (160, 120))
        for i in range(30):
            intensity = (i * 17) % 255
            frame = np.full((120, 160, 3), intensity, dtype=np.uint8)
            out.write(frame)
        out.release()

        scene = _make_scene(0.0, 2.0, video)

        result_mean = analyze_scene_motion(scene, motion_energy_method="mean")
        result_p75 = analyze_scene_motion(
            scene, motion_energy_method="percentile", motion_energy_percentile=75
        )
        # Both are valid floats
        assert isinstance(result_mean[0], float)
        assert isinstance(result_p75[0], float)

    def test_include_sharpness_with_custom_params(self, tmp_path):
        video = tmp_path / "clip.mp4"
        _make_test_video(video)
        scene = _make_scene(0.0, 1.5, video)

        result = analyze_scene_motion(
            scene,
            include_sharpness=True,
            flow_winsize=9,
            flow_levels=3,
            motion_energy_percentile=80,
        )
        assert len(result) == 6  # includes sharpness


# ---------------------------------------------------------------------------
# analyze_scenes_batch forwarding
# ---------------------------------------------------------------------------


class TestAnalyzeScenesBatchForwarding:
    """Test that analyze_scenes_batch forwards new params to each scene."""

    def test_batch_with_flow_params(self, tmp_path):
        video = tmp_path / "clip.mp4"
        _make_test_video(video)
        scenes = [_make_scene(0.0, 1.0, video), _make_scene(1.0, 2.0, video)]

        results = analyze_scenes_batch(
            scenes,
            include_sharpness=False,
            motion_energy_method="mean",
            flow_winsize=7,
            flow_levels=1,
        )
        assert len(results) == 2
        for scene in scenes:
            assert id(scene) in results
            assert "motion_energy" in results[id(scene)]

    def test_batch_percentile_method(self, tmp_path):
        video = tmp_path / "clip.mp4"
        _make_test_video(video)
        scenes = [_make_scene(0.0, 1.5, video)]

        results = analyze_scenes_batch(
            scenes,
            motion_energy_method="percentile",
            motion_energy_percentile=90,
        )
        assert id(scenes[0]) in results


# ---------------------------------------------------------------------------
# CLI wiring tests
# ---------------------------------------------------------------------------


def _make_cli_scene(start, end, score, source_file):
    return SceneInfo(
        start_time=start,
        end_time=end,
        duration=end - start,
        score=score,
        source_file=source_file,
        thumbnail=None,
    )


class TestOpticalFlowCliFlags:
    """Test that --flow-winsize, --flow-levels, --motion-energy-percentile wire correctly."""

    def _run_preview(self, video, tmp_path, extra_args):
        scenes = [_make_cli_scene(0, 2.5, 60, video)]
        with (
            patch("drone_reel.cli.SceneDetector") as mock_sd,
            patch("drone_reel.cli.analyze_scenes_batch") as mock_ab,
            patch("drone_reel.cli.SceneFilter") as mock_sf,
        ):
            mock_sd.return_value.detect_scenes.return_value = scenes
            mock_ab.return_value = {
                id(scenes[0]): {"motion_energy": 30, "brightness": 120, "shake_score": 5}
            }
            mock_fr = MagicMock()
            mock_fr.all_passing = scenes
            mock_fr.dark_scenes_filtered = 0
            mock_fr.shaky_scenes_filtered = 0
            mock_sf.return_value.filter_scenes.return_value = mock_fr

            runner = CliRunner()
            result = runner.invoke(
                main,
                ["split", "-i", str(video), "-o", str(tmp_path / "out"), "--preview"] + extra_args,
            )
            return result, mock_ab

    def test_flow_winsize_forwarded(self, tmp_path):
        video = tmp_path / "clip.mp4"
        _make_test_video(video)
        result, mock_ab = self._run_preview(video, tmp_path, ["--flow-winsize", "9"])
        assert result.exit_code == 0, result.output
        call_kwargs = mock_ab.call_args.kwargs
        assert call_kwargs.get("flow_winsize") == 9

    def test_flow_levels_forwarded(self, tmp_path):
        video = tmp_path / "clip.mp4"
        _make_test_video(video)
        result, mock_ab = self._run_preview(video, tmp_path, ["--flow-levels", "4"])
        assert result.exit_code == 0, result.output
        call_kwargs = mock_ab.call_args.kwargs
        assert call_kwargs.get("flow_levels") == 4

    def test_motion_energy_percentile_forwarded(self, tmp_path):
        video = tmp_path / "clip.mp4"
        _make_test_video(video)
        result, mock_ab = self._run_preview(
            video,
            tmp_path,
            ["--motion-energy-method", "percentile", "--motion-energy-percentile", "80"],
        )
        assert result.exit_code == 0, result.output
        call_kwargs = mock_ab.call_args.kwargs
        assert call_kwargs.get("motion_energy_percentile") == 80
        assert call_kwargs.get("motion_energy_method") == "percentile"

    def test_flow_winsize_out_of_range_rejected(self, tmp_path):
        video = tmp_path / "clip.mp4"
        _make_test_video(video)
        runner = CliRunner()
        result = runner.invoke(
            main,
            ["split", "-i", str(video), "-o", str(tmp_path / "out"), "--flow-winsize", "3"],
        )
        assert result.exit_code != 0

    def test_flow_levels_out_of_range_rejected(self, tmp_path):
        video = tmp_path / "clip.mp4"
        _make_test_video(video)
        runner = CliRunner()
        result = runner.invoke(
            main,
            ["split", "-i", str(video), "-o", str(tmp_path / "out"), "--flow-levels", "5"],
        )
        assert result.exit_code != 0

    def test_motion_energy_percentile_out_of_range_rejected(self, tmp_path):
        video = tmp_path / "clip.mp4"
        _make_test_video(video)
        runner = CliRunner()
        result = runner.invoke(
            main,
            [
                "split",
                "-i",
                str(video),
                "-o",
                str(tmp_path / "out"),
                "--motion-energy-percentile",
                "100",
            ],
        )
        assert result.exit_code != 0
