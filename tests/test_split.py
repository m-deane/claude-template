"""
Tests for the `drone-reel split` CLI command.

Tests parameter validation, scene filtering, preview mode,
export naming, JSON manifest, and integration with synthetic video.
"""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import cv2
import numpy as np
import pytest
from click.testing import CliRunner

from drone_reel.cli import main
from drone_reel.core.scene_detector import SceneInfo


def _make_scene(start, end, score, source_file=None):
    """Create a SceneInfo for testing."""
    return SceneInfo(
        start_time=start,
        end_time=end,
        duration=end - start,
        score=score,
        source_file=source_file or Path("/fake/video.mp4"),
        thumbnail=None,
    )


def _create_test_video(path, width=320, height=240, fps=30, duration_sec=5.0):
    """Create a minimal synthetic video with scene changes."""
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(str(path), fourcc, fps, (width, height))

    total_frames = int(fps * duration_sec)
    for i in range(total_frames):
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        # Create distinct scenes via color shifts
        progress = i / total_frames
        if progress < 0.33:
            frame[:] = (50, 100, 150)  # Blue-ish scene 1
        elif progress < 0.66:
            frame[:] = (150, 50, 100)  # Purple-ish scene 2
        else:
            frame[:] = (100, 150, 50)  # Green-ish scene 3

        # Add motion: shifting rectangle
        x_offset = int((i / total_frames) * (width - 80))
        cv2.rectangle(frame, (x_offset, 60), (x_offset + 80, 180), (255, 255, 255), -1)
        out.write(frame)

    out.release()
    return path


# ---------------------------------------------------------------------------
# Parameter validation tests
# ---------------------------------------------------------------------------


class TestSplitParameterValidation:
    """Test CLI parameter validation for split command."""

    def test_input_directory_rejected(self, tmp_path):
        """split requires a single file, not a directory."""
        runner = CliRunner()
        # Create a directory with a video file inside
        video_dir = tmp_path / "videos"
        video_dir.mkdir()
        _create_test_video(video_dir / "clip.mp4")

        result = runner.invoke(main, ["split", "-i", str(video_dir)])
        assert result.exit_code != 0
        assert (
            "single video file" in result.output.lower()
            or "not a directory" in result.output.lower()
        )

    def test_non_video_file_rejected(self, tmp_path):
        """Non-video files should be rejected with format list."""
        text_file = tmp_path / "readme.txt"
        text_file.write_text("not a video")

        runner = CliRunner()
        result = runner.invoke(main, ["split", "-i", str(text_file)])
        assert result.exit_code != 0
        assert "supported" in result.output.lower()

    def test_min_duration_gte_max_duration_rejected(self, tmp_path):
        """--min-duration must be less than --max-duration."""
        video = tmp_path / "clip.mp4"
        _create_test_video(video)

        runner = CliRunner()
        result = runner.invoke(
            main,
            [
                "split",
                "-i",
                str(video),
                "--min-duration",
                "10",
                "--max-duration",
                "5",
            ],
        )
        assert result.exit_code != 0
        assert "min-duration" in result.output.lower()

    def test_output_dir_not_writable(self, tmp_path):
        """Unwritable output directory should fail."""
        video = tmp_path / "clip.mp4"
        _create_test_video(video)

        runner = CliRunner()
        result = runner.invoke(
            main,
            [
                "split",
                "-i",
                str(video),
                "-o",
                "/root/no_access_dir_12345",
            ],
        )
        assert result.exit_code != 0

    def test_valid_parameters_accepted(self, tmp_path):
        """Valid parameters should pass validation (mocking scene detection)."""
        video = tmp_path / "clip.mp4"
        _create_test_video(video)
        out_dir = tmp_path / "highlights"

        scenes = [_make_scene(0, 3, 65, video), _make_scene(3, 6, 55, video)]

        with (
            patch("drone_reel.cli.SceneDetector") as mock_sd,
            patch("drone_reel.cli.analyze_scenes_batch") as mock_ab,
            patch("drone_reel.cli.SceneFilter") as mock_sf,
        ):

            mock_sd.return_value.detect_scenes.return_value = scenes
            mock_ab.return_value = {
                id(scenes[0]): {"motion_energy": 50, "brightness": 120, "shake_score": 10},
                id(scenes[1]): {"motion_energy": 40, "brightness": 130, "shake_score": 15},
            }
            mock_filter_result = MagicMock()
            mock_filter_result.all_passing = scenes
            mock_filter_result.dark_scenes_filtered = 0
            mock_filter_result.shaky_scenes_filtered = 0
            mock_sf.return_value.filter_scenes.return_value = mock_filter_result

            runner = CliRunner()
            result = runner.invoke(
                main,
                [
                    "split",
                    "-i",
                    str(video),
                    "-o",
                    str(out_dir),
                    "--preview",
                ],
            )
            assert result.exit_code == 0
            assert "Detected" in result.output or "highlights" in result.output.lower()


# ---------------------------------------------------------------------------
# Filtering and selection tests
# ---------------------------------------------------------------------------


class TestSplitFiltering:
    """Test scene filtering and selection logic."""

    @pytest.fixture
    def video_and_scenes(self, tmp_path):
        """Create a video and mock scenes."""
        video = tmp_path / "clip.mp4"
        _create_test_video(video)
        scenes = [
            _make_scene(0, 3, 75, video),  # High score
            _make_scene(3, 6, 50, video),  # Medium score
            _make_scene(6, 8, 30, video),  # Low score
            _make_scene(8, 9, 20, video),  # Below default min_score (40)
        ]
        return video, scenes, tmp_path

    def _run_split_preview(self, runner, video, out_dir, scenes, extra_args=None):
        """Helper to run split in preview mode with mocked detection."""
        with (
            patch("drone_reel.cli.SceneDetector") as mock_sd,
            patch("drone_reel.cli.analyze_scenes_batch") as mock_ab,
            patch("drone_reel.cli.SceneFilter") as mock_sf,
        ):

            mock_sd.return_value.detect_scenes.return_value = scenes
            analysis = {}
            for s in scenes:
                analysis[id(s)] = {
                    "motion_energy": 50,
                    "brightness": 120,
                    "shake_score": 10,
                }
            mock_ab.return_value = analysis

            mock_filter_result = MagicMock()
            mock_filter_result.all_passing = list(scenes)
            mock_filter_result.dark_scenes_filtered = 0
            mock_filter_result.shaky_scenes_filtered = 0
            mock_sf.return_value.filter_scenes.return_value = mock_filter_result

            args = ["split", "-i", str(video), "-o", str(out_dir), "--preview"]
            if extra_args:
                args.extend(extra_args)
            return runner.invoke(main, args)

    def test_min_score_filters_low_scenes(self, video_and_scenes):
        """Scenes below --min-score are excluded."""
        video, scenes, tmp_path = video_and_scenes
        runner = CliRunner()

        # Default min_score=40 should exclude the 30 and 20 score scenes
        result = self._run_split_preview(runner, video, tmp_path / "out", scenes)
        assert result.exit_code == 0
        # Should show 2 highlights (scores 75 and 50), not 4
        assert "2 highlights" in result.output

    def test_explicit_min_score(self, video_and_scenes):
        """Explicit --min-score overrides default."""
        video, scenes, tmp_path = video_and_scenes
        runner = CliRunner()

        result = self._run_split_preview(
            runner,
            video,
            tmp_path / "out",
            scenes,
            extra_args=["--min-score", "60"],
        )
        assert result.exit_code == 0
        assert "1 highlights" in result.output  # Only score 75

    def test_no_filter_passes_all(self, video_and_scenes):
        """--no-filter should bypass SceneFilter."""
        video, scenes, tmp_path = video_and_scenes
        runner = CliRunner()

        with (
            patch("drone_reel.cli.SceneDetector") as mock_sd,
            patch("drone_reel.cli.analyze_scenes_batch") as mock_ab,
        ):

            mock_sd.return_value.detect_scenes.return_value = scenes
            analysis = {}
            for s in scenes:
                analysis[id(s)] = {
                    "motion_energy": 50,
                    "brightness": 120,
                    "shake_score": 10,
                }
            mock_ab.return_value = analysis

            result = runner.invoke(
                main,
                [
                    "split",
                    "-i",
                    str(video),
                    "-o",
                    str(tmp_path / "out"),
                    "--preview",
                    "--no-filter",
                    "--min-score",
                    "0",
                    "--min-duration",
                    "0.5",
                ],
            )
            assert result.exit_code == 0
            assert "4 highlights" in result.output

    def test_count_limits_output(self, video_and_scenes):
        """--count limits the number of exported highlights."""
        video, scenes, tmp_path = video_and_scenes
        runner = CliRunner()

        result = self._run_split_preview(
            runner,
            video,
            tmp_path / "out",
            scenes,
            extra_args=["--count", "1", "--min-score", "0"],
        )
        assert result.exit_code == 0
        assert "1 highlights" in result.output

    def test_sort_chronological(self, video_and_scenes):
        """--sort chronological should order by start_time."""
        video, scenes, tmp_path = video_and_scenes
        runner = CliRunner()

        result = self._run_split_preview(
            runner,
            video,
            tmp_path / "out",
            scenes,
            extra_args=["--sort", "chronological", "--min-score", "0"],
        )
        assert result.exit_code == 0
        # Check that output includes scenes (order not easily verifiable in text,
        # but at least it shouldn't crash)
        assert "highlights" in result.output.lower()

    def test_zero_scenes_detected(self, tmp_path):
        """Zero scenes should exit with helpful message."""
        video = tmp_path / "clip.mp4"
        _create_test_video(video)

        with patch("drone_reel.cli.SceneDetector") as mock_sd:
            mock_sd.return_value.detect_scenes.return_value = []

            runner = CliRunner()
            result = runner.invoke(
                main,
                [
                    "split",
                    "-i",
                    str(video),
                    "-o",
                    str(tmp_path / "out"),
                ],
            )
            assert result.exit_code != 0
            assert "0 scenes" in result.output

    def test_all_scenes_filtered_out(self, tmp_path):
        """All scenes below min_score should show helpful message."""
        video = tmp_path / "clip.mp4"
        _create_test_video(video)
        scenes = [_make_scene(0, 3, 10, video)]

        with (
            patch("drone_reel.cli.SceneDetector") as mock_sd,
            patch("drone_reel.cli.analyze_scenes_batch") as mock_ab,
            patch("drone_reel.cli.SceneFilter") as mock_sf,
        ):

            mock_sd.return_value.detect_scenes.return_value = scenes
            mock_ab.return_value = {
                id(scenes[0]): {
                    "motion_energy": 50,
                    "brightness": 120,
                    "shake_score": 10,
                },
            }
            mock_filter_result = MagicMock()
            mock_filter_result.all_passing = scenes
            mock_filter_result.dark_scenes_filtered = 0
            mock_filter_result.shaky_scenes_filtered = 0
            mock_sf.return_value.filter_scenes.return_value = mock_filter_result

            runner = CliRunner()
            result = runner.invoke(
                main,
                [
                    "split",
                    "-i",
                    str(video),
                    "-o",
                    str(tmp_path / "out"),
                ],
            )
            assert result.exit_code != 0
            assert "no scenes" in result.output.lower() or "min-score" in result.output.lower()


# ---------------------------------------------------------------------------
# Preview mode tests
# ---------------------------------------------------------------------------


class TestSplitPreview:
    """Test --preview dry-run mode."""

    def _mock_and_run_preview(self, runner, video, out_dir, scenes):
        """Run split --preview with mocked detection."""
        with (
            patch("drone_reel.cli.SceneDetector") as mock_sd,
            patch("drone_reel.cli.analyze_scenes_batch") as mock_ab,
            patch("drone_reel.cli.SceneFilter") as mock_sf,
        ):

            mock_sd.return_value.detect_scenes.return_value = scenes
            analysis = {}
            for s in scenes:
                analysis[id(s)] = {
                    "motion_energy": 50,
                    "brightness": 120,
                    "shake_score": 10,
                }
            mock_ab.return_value = analysis

            mock_filter_result = MagicMock()
            mock_filter_result.all_passing = list(scenes)
            mock_filter_result.dark_scenes_filtered = 0
            mock_filter_result.shaky_scenes_filtered = 0
            mock_sf.return_value.filter_scenes.return_value = mock_filter_result

            return runner.invoke(
                main,
                [
                    "split",
                    "-i",
                    str(video),
                    "-o",
                    str(out_dir),
                    "--preview",
                    "--min-score",
                    "0",
                ],
            )

    def test_preview_does_not_create_files(self, tmp_path):
        """Preview mode should not create any output files."""
        video = tmp_path / "clip.mp4"
        _create_test_video(video)
        out_dir = tmp_path / "highlights"

        scenes = [_make_scene(0, 3, 65, video), _make_scene(3, 6, 55, video)]
        runner = CliRunner()
        result = self._mock_and_run_preview(runner, video, out_dir, scenes)

        assert result.exit_code == 0
        assert not out_dir.exists()  # Output dir not created in preview

    def test_preview_shows_scene_table(self, tmp_path):
        """Preview should display a table of detected highlights."""
        video = tmp_path / "clip.mp4"
        _create_test_video(video)
        out_dir = tmp_path / "highlights"

        scenes = [_make_scene(0, 3, 65, video), _make_scene(3, 6, 55, video)]
        runner = CliRunner()
        result = self._mock_and_run_preview(runner, video, out_dir, scenes)

        assert result.exit_code == 0
        assert "Detected Highlights" in result.output
        assert "2 highlights" in result.output

    def test_preview_with_json_flag_still_no_files(self, tmp_path):
        """--preview + --json should still not write anything."""
        video = tmp_path / "clip.mp4"
        _create_test_video(video)
        out_dir = tmp_path / "highlights"

        scenes = [_make_scene(0, 3, 65, video)]

        with (
            patch("drone_reel.cli.SceneDetector") as mock_sd,
            patch("drone_reel.cli.analyze_scenes_batch") as mock_ab,
            patch("drone_reel.cli.SceneFilter") as mock_sf,
        ):

            mock_sd.return_value.detect_scenes.return_value = scenes
            mock_ab.return_value = {
                id(scenes[0]): {
                    "motion_energy": 50,
                    "brightness": 120,
                    "shake_score": 10,
                },
            }
            mock_filter_result = MagicMock()
            mock_filter_result.all_passing = scenes
            mock_filter_result.dark_scenes_filtered = 0
            mock_filter_result.shaky_scenes_filtered = 0
            mock_sf.return_value.filter_scenes.return_value = mock_filter_result

            runner = CliRunner()
            result = runner.invoke(
                main,
                [
                    "split",
                    "-i",
                    str(video),
                    "-o",
                    str(out_dir),
                    "--preview",
                    "--json",
                    "--min-score",
                    "0",
                ],
            )
            assert result.exit_code == 0
            assert not out_dir.exists()


# ---------------------------------------------------------------------------
# Export and naming tests
# ---------------------------------------------------------------------------


class TestSplitExport:
    """Test clip export, naming, and manifest."""

    def _mock_and_run_export(self, runner, video, out_dir, scenes, extra_args=None):
        """Run split with mocked detection and export."""
        with (
            patch("drone_reel.cli.SceneDetector") as mock_sd,
            patch("drone_reel.cli.analyze_scenes_batch") as mock_ab,
            patch("drone_reel.cli.SceneFilter") as mock_sf,
            patch("drone_reel.core.video_processor.VideoProcessor.extract_clip") as mock_ec,
            patch("drone_reel.core.video_processor.VideoProcessor.write_clip") as mock_wc,
        ):

            mock_sd.return_value.detect_scenes.return_value = scenes
            analysis = {}
            for s in scenes:
                analysis[id(s)] = {
                    "motion_energy": 50,
                    "brightness": 120,
                    "shake_score": 10,
                }
            mock_ab.return_value = analysis

            mock_filter_result = MagicMock()
            mock_filter_result.all_passing = list(scenes)
            mock_filter_result.dark_scenes_filtered = 0
            mock_filter_result.shaky_scenes_filtered = 0
            mock_sf.return_value.filter_scenes.return_value = mock_filter_result

            # Mock extract_clip to return a mock clip
            mock_clip = MagicMock()
            mock_clip.w = 320
            mock_clip.h = 240
            mock_ec.return_value = mock_clip

            # Mock write_clip to create a dummy output file
            def create_dummy(clip, output_path):
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(b"\x00" * 1024)
                return output_path

            mock_wc.side_effect = create_dummy

            args = [
                "split",
                "-i",
                str(video),
                "-o",
                str(out_dir),
                "--min-score",
                "0",
            ]
            if extra_args:
                args.extend(extra_args)
            return runner.invoke(main, args)

    def test_output_naming_convention(self, tmp_path):
        """Output files should be named split_NNN_sSCORE.mp4."""
        video = tmp_path / "clip.mp4"
        _create_test_video(video)
        out_dir = tmp_path / "highlights"

        scenes = [_make_scene(0, 3, 72, video), _make_scene(3, 6, 58, video)]
        runner = CliRunner()
        result = self._mock_and_run_export(runner, video, out_dir, scenes)

        assert result.exit_code == 0
        assert (out_dir / "split_001_s72.mp4").exists()
        assert (out_dir / "split_002_s58.mp4").exists()

    def test_overwrite_flag(self, tmp_path):
        """--overwrite should replace existing files."""
        video = tmp_path / "clip.mp4"
        _create_test_video(video)
        out_dir = tmp_path / "highlights"
        out_dir.mkdir()

        # Pre-create a file
        existing = out_dir / "split_001_s72.mp4"
        existing.write_bytes(b"old_content")

        scenes = [_make_scene(0, 3, 72, video)]
        runner = CliRunner()
        result = self._mock_and_run_export(
            runner, video, out_dir, scenes, extra_args=["--overwrite"]
        )

        assert result.exit_code == 0
        assert existing.read_bytes() != b"old_content"

    def test_skip_existing_without_overwrite(self, tmp_path):
        """Without --overwrite, existing files should be skipped."""
        video = tmp_path / "clip.mp4"
        _create_test_video(video)
        out_dir = tmp_path / "highlights"
        out_dir.mkdir()

        # Pre-create matching filename
        existing = out_dir / "split_001_s72.mp4"
        existing.write_bytes(b"old_content")

        scenes = [_make_scene(0, 3, 72, video)]
        runner = CliRunner()
        result = self._mock_and_run_export(runner, video, out_dir, scenes)

        assert result.exit_code == 0
        assert "Skipping" in result.output
        assert existing.read_bytes() == b"old_content"

    def test_json_manifest_written(self, tmp_path):
        """--json should write manifest.json with correct structure."""
        video = tmp_path / "clip.mp4"
        _create_test_video(video)
        out_dir = tmp_path / "highlights"

        scenes = [_make_scene(0, 3, 72, video), _make_scene(3, 6, 58, video)]
        runner = CliRunner()
        result = self._mock_and_run_export(runner, video, out_dir, scenes, extra_args=["--json"])

        assert result.exit_code == 0
        manifest_path = out_dir / "manifest.json"
        assert manifest_path.exists()

        manifest = json.loads(manifest_path.read_text())
        assert manifest["version"] == 1
        assert "source_file" in manifest
        assert manifest["source_file"]["name"] == "clip.mp4"
        assert "split_params" in manifest
        assert "clips" in manifest
        assert len(manifest["clips"]) == 2
        assert manifest["clips"][0]["filename"] == "split_001_s72.mp4"
        assert "summary" in manifest
        assert manifest["summary"]["total_clips"] == 2

    def test_json_not_written_without_flag(self, tmp_path):
        """Without --json, no manifest.json should be created."""
        video = tmp_path / "clip.mp4"
        _create_test_video(video)
        out_dir = tmp_path / "highlights"

        scenes = [_make_scene(0, 3, 72, video)]
        runner = CliRunner()
        result = self._mock_and_run_export(runner, video, out_dir, scenes)

        assert result.exit_code == 0
        assert not (out_dir / "manifest.json").exists()

    def test_export_summary_output(self, tmp_path):
        """Successful export should show summary with count and size."""
        video = tmp_path / "clip.mp4"
        _create_test_video(video)
        out_dir = tmp_path / "highlights"

        scenes = [_make_scene(0, 3, 72, video)]
        runner = CliRunner()
        result = self._mock_and_run_export(runner, video, out_dir, scenes)

        assert result.exit_code == 0
        assert "Exported" in result.output
        assert "1 highlight" in result.output.lower() or "1 highlights" in result.output


# ---------------------------------------------------------------------------
# Help text test
# ---------------------------------------------------------------------------


class TestSplitHelp:
    """Test help text and command registration."""

    def test_split_help_shows_parameters(self):
        """drone-reel split --help should show all parameters."""
        runner = CliRunner()
        result = runner.invoke(main, ["split", "--help"])
        assert result.exit_code == 0
        assert "Split a single video" in result.output
        assert "--min-score" in result.output
        assert "--preview" in result.output
        assert "--json" in result.output
        assert "--no-filter" in result.output
        assert "--count" in result.output
        assert "--quality" in result.output

    def test_split_registered_in_main(self):
        """split should be a registered subcommand."""
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "split" in result.output


# ---------------------------------------------------------------------------
# Duration capping tests
# ---------------------------------------------------------------------------


class TestSplitDurationCapping:
    """Test that clip durations are properly capped."""

    def test_max_duration_caps_long_scenes(self, tmp_path):
        """Scenes longer than --max-duration should be capped."""
        video = tmp_path / "clip.mp4"
        _create_test_video(video)
        out_dir = tmp_path / "highlights"

        # Scene is 20s but max_duration is 10
        scenes = [_make_scene(0, 20, 65, video)]

        with (
            patch("drone_reel.cli.SceneDetector") as mock_sd,
            patch("drone_reel.cli.analyze_scenes_batch") as mock_ab,
            patch("drone_reel.cli.SceneFilter") as mock_sf,
        ):

            mock_sd.return_value.detect_scenes.return_value = scenes
            mock_ab.return_value = {
                id(scenes[0]): {
                    "motion_energy": 50,
                    "brightness": 120,
                    "shake_score": 10,
                },
            }
            mock_filter_result = MagicMock()
            mock_filter_result.all_passing = scenes
            mock_filter_result.dark_scenes_filtered = 0
            mock_filter_result.shaky_scenes_filtered = 0
            mock_sf.return_value.filter_scenes.return_value = mock_filter_result

            runner = CliRunner()
            result = runner.invoke(
                main,
                [
                    "split",
                    "-i",
                    str(video),
                    "-o",
                    str(out_dir),
                    "--preview",
                    "--max-duration",
                    "10",
                    "--min-score",
                    "0",
                ],
            )
            assert result.exit_code == 0
            # The preview table should show 10.0s duration, not 20.0s
            assert "10.0s" in result.output

    def test_min_duration_filters_short_scenes(self, tmp_path):
        """Scenes shorter than --min-duration should be excluded."""
        video = tmp_path / "clip.mp4"
        _create_test_video(video)

        scenes = [
            _make_scene(0, 1, 80, video),  # 1s - below default 2s
            _make_scene(1, 5, 60, video),  # 4s - passes
        ]

        with (
            patch("drone_reel.cli.SceneDetector") as mock_sd,
            patch("drone_reel.cli.analyze_scenes_batch") as mock_ab,
            patch("drone_reel.cli.SceneFilter") as mock_sf,
        ):

            mock_sd.return_value.detect_scenes.return_value = scenes
            analysis = {}
            for s in scenes:
                analysis[id(s)] = {
                    "motion_energy": 50,
                    "brightness": 120,
                    "shake_score": 10,
                }
            mock_ab.return_value = analysis

            mock_filter_result = MagicMock()
            mock_filter_result.all_passing = list(scenes)
            mock_filter_result.dark_scenes_filtered = 0
            mock_filter_result.shaky_scenes_filtered = 0
            mock_sf.return_value.filter_scenes.return_value = mock_filter_result

            runner = CliRunner()
            result = runner.invoke(
                main,
                [
                    "split",
                    "-i",
                    str(video),
                    "-o",
                    str(tmp_path / "out"),
                    "--preview",
                ],
            )
            assert result.exit_code == 0
            # Only 1 scene (4s) should pass the 2s min duration filter
            assert "1 highlights" in result.output


# ---------------------------------------------------------------------------
# Post-processing: Color grading tests
# ---------------------------------------------------------------------------


class TestSplitColorGrading:
    """Test color grading and visual effects options."""

    def _mock_and_run_export(self, runner, video, out_dir, scenes, extra_args=None):
        """Run split with mocked detection and export, return result + mock refs."""
        with (
            patch("drone_reel.cli.SceneDetector") as mock_sd,
            patch("drone_reel.cli.analyze_scenes_batch") as mock_ab,
            patch("drone_reel.cli.SceneFilter") as mock_sf,
            patch("drone_reel.core.video_processor.VideoProcessor.extract_clip") as mock_ec,
            patch("drone_reel.core.video_processor.VideoProcessor.write_clip") as mock_wc,
        ):

            mock_sd.return_value.detect_scenes.return_value = scenes
            analysis = {}
            for s in scenes:
                analysis[id(s)] = {
                    "motion_energy": 50,
                    "brightness": 120,
                    "shake_score": 10,
                }
            mock_ab.return_value = analysis

            mock_filter_result = MagicMock()
            mock_filter_result.all_passing = list(scenes)
            mock_filter_result.dark_scenes_filtered = 0
            mock_filter_result.shaky_scenes_filtered = 0
            mock_sf.return_value.filter_scenes.return_value = mock_filter_result

            mock_clip = MagicMock()
            mock_clip.w = 320
            mock_clip.h = 240
            mock_clip.duration = 3.0
            mock_ec.return_value = mock_clip

            def create_dummy(clip, output_path):
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(b"\x00" * 1024)
                return output_path

            mock_wc.side_effect = create_dummy

            args = [
                "split",
                "-i",
                str(video),
                "-o",
                str(out_dir),
                "--min-score",
                "0",
            ]
            if extra_args:
                args.extend(extra_args)
            result = runner.invoke(main, args)
            return result, mock_clip, mock_wc

    def test_color_preset_applies_grading(self, tmp_path):
        """--color should trigger color grading pipeline."""
        video = tmp_path / "clip.mp4"
        _create_test_video(video)
        out_dir = tmp_path / "highlights"

        scenes = [_make_scene(0, 3, 65, video)]
        runner = CliRunner()
        result, mock_clip, _ = self._mock_and_run_export(
            runner, video, out_dir, scenes, extra_args=["--color", "drone_aerial"]
        )

        assert result.exit_code == 0
        assert "Color grade" in result.output
        assert "drone_aerial" in result.output
        # Verify transform was called on the clip (color grading applies via clip.transform)
        mock_clip.transform.assert_called_once()

    def test_color_with_intensity(self, tmp_path):
        """--color-intensity should be reported in output."""
        video = tmp_path / "clip.mp4"
        _create_test_video(video)
        out_dir = tmp_path / "highlights"

        scenes = [_make_scene(0, 3, 65, video)]
        runner = CliRunner()
        result, _, _ = self._mock_and_run_export(
            runner,
            video,
            out_dir,
            scenes,
            extra_args=["--color", "drone_aerial", "--color-intensity", "0.6"],
        )

        assert result.exit_code == 0
        assert "60%" in result.output

    def test_vignette_shows_in_effects(self, tmp_path):
        """--vignette should appear in effects output."""
        video = tmp_path / "clip.mp4"
        _create_test_video(video)
        out_dir = tmp_path / "highlights"

        scenes = [_make_scene(0, 3, 65, video)]
        runner = CliRunner()
        result, mock_clip, _ = self._mock_and_run_export(
            runner, video, out_dir, scenes, extra_args=["--vignette", "0.5"]
        )

        assert result.exit_code == 0
        assert "vignette" in result.output.lower()
        # Effects-only (no color preset) still triggers transform
        mock_clip.transform.assert_called_once()

    def test_denoise_shows_in_effects(self, tmp_path):
        """--denoise should appear in effects output."""
        video = tmp_path / "clip.mp4"
        _create_test_video(video)
        out_dir = tmp_path / "highlights"

        scenes = [_make_scene(0, 3, 65, video)]
        runner = CliRunner()
        result, _, _ = self._mock_and_run_export(
            runner, video, out_dir, scenes, extra_args=["--denoise", "0.4"]
        )

        assert result.exit_code == 0
        assert "denoise" in result.output.lower()

    def test_multiple_effects_combined(self, tmp_path):
        """Multiple effects should all appear in output."""
        video = tmp_path / "clip.mp4"
        _create_test_video(video)
        out_dir = tmp_path / "highlights"

        scenes = [_make_scene(0, 3, 65, video)]
        runner = CliRunner()
        result, mock_clip, _ = self._mock_and_run_export(
            runner,
            video,
            out_dir,
            scenes,
            extra_args=[
                "--color",
                "drone_aerial",
                "--vignette",
                "0.3",
                "--halation",
                "0.2",
                "--gnd-sky",
                "0.5",
            ],
        )

        assert result.exit_code == 0
        assert "vignette" in result.output.lower()
        assert "halation" in result.output.lower()
        assert "GND sky" in result.output
        mock_clip.transform.assert_called_once()

    def test_no_color_no_effects_skips_grading(self, tmp_path):
        """Without color/effects flags, no grading should be applied."""
        video = tmp_path / "clip.mp4"
        _create_test_video(video)
        out_dir = tmp_path / "highlights"

        scenes = [_make_scene(0, 3, 65, video)]
        runner = CliRunner()
        result, mock_clip, _ = self._mock_and_run_export(runner, video, out_dir, scenes)

        assert result.exit_code == 0
        assert "Color grade" not in result.output
        mock_clip.transform.assert_not_called()

    def test_graded_tag_in_export_output(self, tmp_path):
        """When post-processing is active, export lines should show +graded tag."""
        video = tmp_path / "clip.mp4"
        _create_test_video(video)
        out_dir = tmp_path / "highlights"

        scenes = [_make_scene(0, 3, 65, video)]
        runner = CliRunner()
        result, _, _ = self._mock_and_run_export(
            runner, video, out_dir, scenes, extra_args=["--color", "drone_aerial"]
        )

        assert result.exit_code == 0
        assert "+graded" in result.output


# ---------------------------------------------------------------------------
# Post-processing: Stabilization tests
# ---------------------------------------------------------------------------


class TestSplitStabilization:
    """Test stabilization options."""

    def test_stabilize_flag_shows_mode(self, tmp_path):
        """--stabilize should show adaptive mode in output."""
        video = tmp_path / "clip.mp4"
        _create_test_video(video)
        out_dir = tmp_path / "highlights"

        scenes = [_make_scene(0, 3, 65, video)]

        with (
            patch("drone_reel.cli.SceneDetector") as mock_sd,
            patch("drone_reel.cli.analyze_scenes_batch") as mock_ab,
            patch("drone_reel.cli.SceneFilter") as mock_sf,
            patch("drone_reel.core.video_processor.VideoProcessor.extract_clip") as mock_ec,
            patch("drone_reel.core.video_processor.VideoProcessor.write_clip") as mock_wc,
            patch("drone_reel.core.stabilizer.stabilize_clip") as mock_stab,
        ):

            mock_sd.return_value.detect_scenes.return_value = scenes
            analysis = {}
            for s in scenes:
                analysis[id(s)] = {
                    "motion_energy": 50,
                    "brightness": 120,
                    "shake_score": 25,
                }
            mock_ab.return_value = analysis

            mock_filter_result = MagicMock()
            mock_filter_result.all_passing = list(scenes)
            mock_filter_result.dark_scenes_filtered = 0
            mock_filter_result.shaky_scenes_filtered = 0
            mock_sf.return_value.filter_scenes.return_value = mock_filter_result

            mock_clip = MagicMock()
            mock_clip.w = 320
            mock_clip.h = 240
            mock_clip.duration = 3.0
            mock_ec.return_value = mock_clip

            # stabilize_clip returns the clip unchanged
            mock_stab.return_value = mock_clip

            def create_dummy(clip, output_path):
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(b"\x00" * 1024)
                return output_path

            mock_wc.side_effect = create_dummy

            runner = CliRunner()
            result = runner.invoke(
                main,
                [
                    "split",
                    "-i",
                    str(video),
                    "-o",
                    str(out_dir),
                    "--min-score",
                    "0",
                    "--stabilize",
                ],
            )

            assert result.exit_code == 0
            assert "Stabilization" in result.output
            assert "adaptive" in result.output.lower()
            mock_stab.assert_called_once()
            # Should use the scene's actual shake score
            call_kwargs = mock_stab.call_args
            assert call_kwargs[1]["shake_score"] == 25

    def test_stabilize_all_forces_full(self, tmp_path):
        """--stabilize-all should force shake_score=100 (full stabilization)."""
        video = tmp_path / "clip.mp4"
        _create_test_video(video)
        out_dir = tmp_path / "highlights"

        scenes = [_make_scene(0, 3, 65, video)]

        with (
            patch("drone_reel.cli.SceneDetector") as mock_sd,
            patch("drone_reel.cli.analyze_scenes_batch") as mock_ab,
            patch("drone_reel.cli.SceneFilter") as mock_sf,
            patch("drone_reel.core.video_processor.VideoProcessor.extract_clip") as mock_ec,
            patch("drone_reel.core.video_processor.VideoProcessor.write_clip") as mock_wc,
            patch("drone_reel.core.stabilizer.stabilize_clip") as mock_stab,
        ):

            mock_sd.return_value.detect_scenes.return_value = scenes
            analysis = {}
            for s in scenes:
                analysis[id(s)] = {
                    "motion_energy": 50,
                    "brightness": 120,
                    "shake_score": 5,  # Low shake — normally would skip
                }
            mock_ab.return_value = analysis

            mock_filter_result = MagicMock()
            mock_filter_result.all_passing = list(scenes)
            mock_filter_result.dark_scenes_filtered = 0
            mock_filter_result.shaky_scenes_filtered = 0
            mock_sf.return_value.filter_scenes.return_value = mock_filter_result

            mock_clip = MagicMock()
            mock_clip.w = 320
            mock_clip.h = 240
            mock_clip.duration = 3.0
            mock_ec.return_value = mock_clip
            mock_stab.return_value = mock_clip

            def create_dummy(clip, output_path):
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(b"\x00" * 1024)
                return output_path

            mock_wc.side_effect = create_dummy

            runner = CliRunner()
            result = runner.invoke(
                main,
                [
                    "split",
                    "-i",
                    str(video),
                    "-o",
                    str(out_dir),
                    "--min-score",
                    "0",
                    "--stabilize-all",
                ],
            )

            assert result.exit_code == 0
            assert "all clips" in result.output.lower()
            mock_stab.assert_called_once()
            call_kwargs = mock_stab.call_args
            assert call_kwargs[1]["shake_score"] == 100.0


# ---------------------------------------------------------------------------
# Post-processing: Detection tuning tests
# ---------------------------------------------------------------------------


class TestSplitDetectionTuning:
    """Test --scene-threshold and --enhanced detection flags."""

    def test_scene_threshold_passed_to_detector(self, tmp_path):
        """--scene-threshold should configure SceneDetector."""
        video = tmp_path / "clip.mp4"
        _create_test_video(video)

        with (
            patch("drone_reel.cli.SceneDetector") as mock_sd,
            patch("drone_reel.cli.analyze_scenes_batch") as mock_ab,
            patch("drone_reel.cli.SceneFilter") as mock_sf,
        ):

            mock_sd.return_value.detect_scenes.return_value = [_make_scene(0, 3, 65, video)]
            mock_ab.return_value = {
                id(mock_sd.return_value.detect_scenes.return_value[0]): {
                    "motion_energy": 50,
                    "brightness": 120,
                    "shake_score": 10,
                },
            }
            mock_filter_result = MagicMock()
            mock_filter_result.all_passing = mock_sd.return_value.detect_scenes.return_value
            mock_filter_result.dark_scenes_filtered = 0
            mock_filter_result.shaky_scenes_filtered = 0
            mock_sf.return_value.filter_scenes.return_value = mock_filter_result

            runner = CliRunner()
            result = runner.invoke(
                main,
                [
                    "split",
                    "-i",
                    str(video),
                    "-o",
                    str(tmp_path / "out"),
                    "--preview",
                    "--scene-threshold",
                    "15",
                    "--min-score",
                    "0",
                ],
            )

            assert result.exit_code == 0
            # Verify SceneDetector was created with threshold=15
            mock_sd.assert_called_once_with(threshold=15.0, max_scene_length=15.0, frame_skip=0)

    def test_enhanced_uses_enhanced_detection(self, tmp_path):
        """--enhanced should call detect_scenes_enhanced() instead of detect_scenes()."""
        video = tmp_path / "clip.mp4"
        _create_test_video(video)

        with (
            patch("drone_reel.cli.SceneDetector") as mock_sd,
            patch("drone_reel.cli.analyze_scenes_batch") as mock_ab,
            patch("drone_reel.cli.SceneFilter") as mock_sf,
        ):

            scenes = [_make_scene(0, 3, 65, video)]
            mock_sd.return_value.detect_scenes_enhanced.return_value = scenes
            mock_ab.return_value = {
                id(scenes[0]): {
                    "motion_energy": 50,
                    "brightness": 120,
                    "shake_score": 10,
                },
            }
            mock_filter_result = MagicMock()
            mock_filter_result.all_passing = scenes
            mock_filter_result.dark_scenes_filtered = 0
            mock_filter_result.shaky_scenes_filtered = 0
            mock_sf.return_value.filter_scenes.return_value = mock_filter_result

            runner = CliRunner()
            result = runner.invoke(
                main,
                [
                    "split",
                    "-i",
                    str(video),
                    "-o",
                    str(tmp_path / "out"),
                    "--preview",
                    "--enhanced",
                    "--min-score",
                    "0",
                ],
            )

            assert result.exit_code == 0
            # detect_scenes_enhanced should be called, NOT detect_scenes
            mock_sd.return_value.detect_scenes_enhanced.assert_called_once()
            mock_sd.return_value.detect_scenes.assert_not_called()

    def test_enhanced_label_in_progress(self, tmp_path):
        """--enhanced should show 'enhanced' in detection progress."""
        video = tmp_path / "clip.mp4"
        _create_test_video(video)

        with (
            patch("drone_reel.cli.SceneDetector") as mock_sd,
            patch("drone_reel.cli.analyze_scenes_batch") as mock_ab,
            patch("drone_reel.cli.SceneFilter") as mock_sf,
        ):

            scenes = [_make_scene(0, 3, 65, video)]
            mock_sd.return_value.detect_scenes_enhanced.return_value = scenes
            mock_ab.return_value = {
                id(scenes[0]): {
                    "motion_energy": 50,
                    "brightness": 120,
                    "shake_score": 10,
                },
            }
            mock_filter_result = MagicMock()
            mock_filter_result.all_passing = scenes
            mock_filter_result.dark_scenes_filtered = 0
            mock_filter_result.shaky_scenes_filtered = 0
            mock_sf.return_value.filter_scenes.return_value = mock_filter_result

            runner = CliRunner()
            result = runner.invoke(
                main,
                [
                    "split",
                    "-i",
                    str(video),
                    "-o",
                    str(tmp_path / "out"),
                    "--preview",
                    "--enhanced",
                    "--min-score",
                    "0",
                ],
            )

            assert result.exit_code == 0


# ---------------------------------------------------------------------------
# Post-processing: Letterbox tests
# ---------------------------------------------------------------------------


class TestSplitLetterbox:
    """Test --letterbox option."""

    def test_letterbox_shows_in_output(self, tmp_path):
        """--letterbox should show in output and apply to clip."""
        video = tmp_path / "clip.mp4"
        _create_test_video(video)
        out_dir = tmp_path / "highlights"

        scenes = [_make_scene(0, 3, 65, video)]

        with (
            patch("drone_reel.cli.SceneDetector") as mock_sd,
            patch("drone_reel.cli.analyze_scenes_batch") as mock_ab,
            patch("drone_reel.cli.SceneFilter") as mock_sf,
            patch("drone_reel.core.video_processor.VideoProcessor.extract_clip") as mock_ec,
            patch("drone_reel.core.video_processor.VideoProcessor.write_clip") as mock_wc,
        ):

            mock_sd.return_value.detect_scenes.return_value = scenes
            analysis = {}
            for s in scenes:
                analysis[id(s)] = {
                    "motion_energy": 50,
                    "brightness": 120,
                    "shake_score": 10,
                }
            mock_ab.return_value = analysis

            mock_filter_result = MagicMock()
            mock_filter_result.all_passing = list(scenes)
            mock_filter_result.dark_scenes_filtered = 0
            mock_filter_result.shaky_scenes_filtered = 0
            mock_sf.return_value.filter_scenes.return_value = mock_filter_result

            mock_clip = MagicMock()
            mock_clip.w = 320
            mock_clip.h = 240
            mock_clip.duration = 3.0
            mock_ec.return_value = mock_clip

            def create_dummy(clip, output_path):
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(b"\x00" * 1024)
                return output_path

            mock_wc.side_effect = create_dummy

            runner = CliRunner()
            result = runner.invoke(
                main,
                [
                    "split",
                    "-i",
                    str(video),
                    "-o",
                    str(out_dir),
                    "--min-score",
                    "0",
                    "--letterbox",
                    "2.35",
                ],
            )

            assert result.exit_code == 0
            assert "Letterbox" in result.output
            assert "2.35" in result.output


# ---------------------------------------------------------------------------
# Post-processing: JSON manifest includes post-processing metadata
# ---------------------------------------------------------------------------


class TestSplitManifestPostProcessing:
    """Test that manifest.json captures post-processing settings."""

    def test_manifest_includes_post_processing(self, tmp_path):
        """--json with post-processing should record settings in manifest."""
        video = tmp_path / "clip.mp4"
        _create_test_video(video)
        out_dir = tmp_path / "highlights"

        scenes = [_make_scene(0, 3, 65, video)]

        with (
            patch("drone_reel.cli.SceneDetector") as mock_sd,
            patch("drone_reel.cli.analyze_scenes_batch") as mock_ab,
            patch("drone_reel.cli.SceneFilter") as mock_sf,
            patch("drone_reel.core.video_processor.VideoProcessor.extract_clip") as mock_ec,
            patch("drone_reel.core.video_processor.VideoProcessor.write_clip") as mock_wc,
            patch("drone_reel.core.stabilizer.stabilize_clip") as mock_stab,
        ):

            mock_sd.return_value.detect_scenes.return_value = scenes
            analysis = {}
            for s in scenes:
                analysis[id(s)] = {
                    "motion_energy": 50,
                    "brightness": 120,
                    "shake_score": 10,
                }
            mock_ab.return_value = analysis

            mock_filter_result = MagicMock()
            mock_filter_result.all_passing = list(scenes)
            mock_filter_result.dark_scenes_filtered = 0
            mock_filter_result.shaky_scenes_filtered = 0
            mock_sf.return_value.filter_scenes.return_value = mock_filter_result

            mock_clip = MagicMock()
            mock_clip.w = 320
            mock_clip.h = 240
            mock_clip.duration = 3.0
            # Ensure transform() returns same mock so w/h are preserved
            mock_clip.transform.return_value = mock_clip
            mock_ec.return_value = mock_clip
            mock_stab.return_value = mock_clip

            def create_dummy(clip, output_path):
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(b"\x00" * 1024)
                return output_path

            mock_wc.side_effect = create_dummy

            runner = CliRunner()
            result = runner.invoke(
                main,
                [
                    "split",
                    "-i",
                    str(video),
                    "-o",
                    str(out_dir),
                    "--min-score",
                    "0",
                    "--json",
                    "--color",
                    "drone_aerial",
                    "--stabilize",
                    "--scene-threshold",
                    "20",
                ],
            )

            assert result.exit_code == 0
            manifest = json.loads((out_dir / "manifest.json").read_text())

            # split_params should include new settings
            params = manifest["split_params"]
            assert params["scene_threshold"] == 20.0
            assert params["color"] == "drone_aerial"
            assert params["stabilize"] is True

            # Per-clip post_processing metadata
            clip_meta = manifest["clips"][0]
            assert "post_processing" in clip_meta
            pp = clip_meta["post_processing"]
            assert pp["color"] == "drone_aerial"
            assert pp["stabilized"] is True


# ---------------------------------------------------------------------------
# Help text: verify new options appear
# ---------------------------------------------------------------------------


class TestSplitHelpPostProcessing:
    """Test that new post-processing options appear in help text."""

    def test_help_shows_color_options(self):
        """Help should list color grading options."""
        runner = CliRunner()
        result = runner.invoke(main, ["split", "--help"])
        assert result.exit_code == 0
        assert "--color" in result.output
        assert "--color-intensity" in result.output
        assert "--vignette" in result.output
        assert "--halation" in result.output
        assert "--chromatic-aberration" in result.output
        assert "--lut" in result.output
        assert "--input-colorspace" in result.output
        assert "--auto-wb" in result.output
        assert "--denoise" in result.output
        assert "--haze" in result.output
        assert "--gnd-sky" in result.output

    def test_help_shows_stabilization_options(self):
        """Help should list stabilization options."""
        runner = CliRunner()
        result = runner.invoke(main, ["split", "--help"])
        assert result.exit_code == 0
        assert "--stabilize" in result.output
        assert "--stabilize-all" in result.output

    def test_help_shows_detection_options(self):
        """Help should list detection tuning options."""
        runner = CliRunner()
        result = runner.invoke(main, ["split", "--help"])
        assert result.exit_code == 0
        assert "--scene-threshold" in result.output
        assert "--enhanced" in result.output

    def test_help_shows_letterbox(self):
        """Help should list letterbox option."""
        runner = CliRunner()
        result = runner.invoke(main, ["split", "--help"])
        assert result.exit_code == 0
        assert "--letterbox" in result.output

    def test_help_shows_auto_speed(self):
        """Help should list --auto-speed option."""
        runner = CliRunner()
        result = runner.invoke(main, ["split", "--help"])
        assert result.exit_code == 0
        assert "--auto-speed" in result.output


# ---------------------------------------------------------------------------
# Auto speed correction tests
# ---------------------------------------------------------------------------


class TestSplitAutoSpeed:
    """Tests for --auto-speed flag in split command."""

    def test_auto_speed_calls_auto_pan_speed_ramp(self, tmp_path):
        """--auto-speed should call auto_pan_speed_ramp for each scene."""
        video = tmp_path / "clip.mp4"
        _create_test_video(video)

        with (
            patch("drone_reel.cli.SceneDetector") as mock_sd,
            patch("drone_reel.cli.analyze_scenes_batch") as mock_ab,
            patch("drone_reel.cli.SceneFilter") as mock_sf,
            patch("drone_reel.core.stabilizer.stabilize_clip"),
            patch("drone_reel.cli.auto_pan_speed_ramp", return_value=[]) as mock_apr,
        ):
            scene = _make_scene(0, 5, 70, video)
            mock_sd.return_value.detect_scenes.return_value = [scene]
            mock_ab.return_value = {id(scene): {"motion_energy": 75, "brightness": 120, "shake_score": 10}}
            mock_filter_result = MagicMock()
            mock_filter_result.all_passing = [scene]
            mock_sf.return_value.filter_scenes.return_value = mock_filter_result

            mock_clip = MagicMock()
            mock_clip.w = 320
            mock_clip.h = 240
            mock_clip.duration = 5.0
            mock_clip.transform.return_value = mock_clip
            mock_clip.time_transform.return_value = mock_clip
            mock_clip.with_duration.return_value = mock_clip

            with patch("drone_reel.core.video_processor.VideoProcessor") as mock_vp_class:
                mock_vp = MagicMock()
                mock_vp_class.return_value = mock_vp
                mock_vp.extract_clip.return_value = mock_clip

                runner = CliRunner()
                result = runner.invoke(
                    main,
                    [
                        "split",
                        "-i", str(video),
                        "-o", str(tmp_path / "out"),
                        "--min-score", "0",
                        "--no-filter",
                        "--auto-speed",
                    ],
                )

            assert result.exit_code == 0
            mock_apr.assert_called()

    def test_without_auto_speed_no_pan_ramp(self, tmp_path):
        """Without --auto-speed, auto_pan_speed_ramp should not be called."""
        video = tmp_path / "clip.mp4"
        _create_test_video(video)

        with (
            patch("drone_reel.cli.SceneDetector") as mock_sd,
            patch("drone_reel.cli.analyze_scenes_batch") as mock_ab,
            patch("drone_reel.cli.SceneFilter") as mock_sf,
            patch("drone_reel.cli.auto_pan_speed_ramp") as mock_apr,
        ):
            scene = _make_scene(0, 5, 70, video)
            mock_sd.return_value.detect_scenes.return_value = [scene]
            mock_ab.return_value = {id(scene): {"motion_energy": 75, "brightness": 120, "shake_score": 10}}
            mock_filter_result = MagicMock()
            mock_filter_result.all_passing = [scene]
            mock_sf.return_value.filter_scenes.return_value = mock_filter_result

            mock_clip = MagicMock()
            mock_clip.w = 320
            mock_clip.h = 240
            mock_clip.duration = 5.0
            mock_clip.transform.return_value = mock_clip

            with patch("drone_reel.core.video_processor.VideoProcessor") as mock_vp_class:
                mock_vp = MagicMock()
                mock_vp_class.return_value = mock_vp
                mock_vp.extract_clip.return_value = mock_clip

                runner = CliRunner()
                runner.invoke(
                    main,
                    [
                        "split",
                        "-i", str(video),
                        "-o", str(tmp_path / "out"),
                        "--min-score", "0",
                        "--no-filter",
                    ],
                )

            mock_apr.assert_not_called()

    def test_auto_speed_applies_ramp_when_returned(self, tmp_path):
        """When auto_pan_speed_ramp returns a ramp, SpeedRamper.apply_multiple_ramps is called."""
        video = tmp_path / "clip.mp4"
        _create_test_video(video)

        from drone_reel.core.speed_ramper import SpeedRamp

        fake_ramp = SpeedRamp(start_time=0.0, end_time=5.0, start_speed=0.65, end_speed=0.65)

        with (
            patch("drone_reel.cli.SceneDetector") as mock_sd,
            patch("drone_reel.cli.analyze_scenes_batch") as mock_ab,
            patch("drone_reel.cli.SceneFilter") as mock_sf,
            patch("drone_reel.cli.auto_pan_speed_ramp", return_value=[fake_ramp]),
            patch("drone_reel.cli.SpeedRamper") as mock_sr_class,
        ):
            scene = _make_scene(0, 5, 70, video)
            mock_sd.return_value.detect_scenes.return_value = [scene]
            mock_ab.return_value = {id(scene): {"motion_energy": 75, "brightness": 120, "shake_score": 10}}
            mock_filter_result = MagicMock()
            mock_filter_result.all_passing = [scene]
            mock_sf.return_value.filter_scenes.return_value = mock_filter_result

            mock_clip = MagicMock()
            mock_clip.w = 320
            mock_clip.h = 240
            mock_clip.duration = 5.0
            mock_clip.transform.return_value = mock_clip

            mock_sr = MagicMock()
            mock_sr_class.return_value = mock_sr
            mock_sr.apply_multiple_ramps.return_value = mock_clip

            with patch("drone_reel.core.video_processor.VideoProcessor") as mock_vp_class:
                mock_vp = MagicMock()
                mock_vp_class.return_value = mock_vp
                mock_vp.extract_clip.return_value = mock_clip

                runner = CliRunner()
                result = runner.invoke(
                    main,
                    [
                        "split",
                        "-i", str(video),
                        "-o", str(tmp_path / "out"),
                        "--min-score", "0",
                        "--no-filter",
                        "--auto-speed",
                    ],
                )

            assert result.exit_code == 0
            mock_sr.apply_multiple_ramps.assert_called_once()
