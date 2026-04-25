"""Tests for the extract-clips CLI command."""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from drone_reel.cli import main
from drone_reel.core.scene_detector import EnhancedSceneInfo, HookPotential, MotionType, SceneInfo


def _make_scene(
    start=0.0, end=5.0, score=70.0, source_file=None, enhanced=False
):
    """Helper to create a SceneInfo or EnhancedSceneInfo for tests."""
    if source_file is None:
        source_file = Path("/tmp/test_video.mp4")

    if enhanced:
        return EnhancedSceneInfo(
            start_time=start,
            end_time=end,
            duration=end - start,
            score=score,
            source_file=source_file,
            motion_energy=50.0,
            motion_type=MotionType.PAN_RIGHT,
            motion_direction=(0.5, 0.0),
            motion_smoothness=80.0,
            color_variance=60.0,
            hook_potential=score,
            hook_tier=HookPotential.HIGH if score >= 65 else HookPotential.MEDIUM,
            subject_score=45.0,
            is_golden_hour=False,
            dominant_colors=[(100, 150, 200)],
            visual_interest_density=0.5,
            depth_score=60.0,
        )
    else:
        return SceneInfo(
            start_time=start,
            end_time=end,
            duration=end - start,
            score=score,
            source_file=source_file,
        )


def _make_analysis_result(scenes):
    """Helper to build analysis results dict keyed by id(scene)."""
    result = {}
    for s in scenes:
        result[id(s)] = {
            "motion_energy": getattr(s, "motion_energy", 50.0),
            "brightness": 127.0,
            "shake_score": 10.0,
            "motion_type": getattr(s, "motion_type", MotionType.STATIC),
            "motion_direction": getattr(s, "motion_direction", (0.0, 0.0)),
            "sharpness": 50.0,
        }
    return result


class TestExtractClipsValidation:
    """Tests for parameter validation in extract-clips command."""

    def test_min_duration_gte_max_duration_fails(self):
        """Test error when --min-duration >= --max-duration."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            Path("video.mp4").touch()
            result = runner.invoke(
                main,
                ["extract-clips", "-i", "video.mp4",
                 "--min-duration", "10", "--max-duration", "5"],
            )
            assert result.exit_code != 0
            assert "must be less than" in result.output

    def test_min_duration_equal_max_duration_fails(self):
        """Test error when --min-duration == --max-duration."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            Path("video.mp4").touch()
            result = runner.invoke(
                main,
                ["extract-clips", "-i", "video.mp4",
                 "--min-duration", "5", "--max-duration", "5"],
            )
            assert result.exit_code != 0
            assert "must be less than" in result.output

    def test_nonexistent_input_fails(self):
        """Test error when input path doesn't exist."""
        runner = CliRunner()
        result = runner.invoke(
            main,
            ["extract-clips", "-i", "/nonexistent/path.mp4"],
        )
        assert result.exit_code != 0

    def test_unsupported_file_extension_fails(self):
        """Test error when input file has unsupported extension."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            Path("video.txt").touch()
            result = runner.invoke(
                main,
                ["extract-clips", "-i", "video.txt"],
            )
            assert result.exit_code != 0
            assert "Not a supported video file" in result.output


class TestExtractClipsSceneDetection:
    """Tests for scene detection flow in extract-clips."""

    @patch("drone_reel.cli.analyze_scenes_batch")
    @patch("drone_reel.cli.SceneDetector")
    @patch("drone_reel.utils.resource_guard.check_available_memory_mb",
           return_value=float("inf"))
    @patch("drone_reel.utils.resource_guard.check_disk_space_mb",
           return_value=float("inf"))
    def test_zero_scenes_detected(
        self, mock_disk, mock_mem, mock_detector_cls, mock_analyze
    ):
        """Test handling when zero scenes are detected."""
        mock_detector = MagicMock()
        mock_detector.detect_scenes.return_value = []
        mock_detector_cls.return_value = mock_detector

        runner = CliRunner()
        with runner.isolated_filesystem():
            Path("video.mp4").touch()
            result = runner.invoke(main, ["extract-clips", "-i", "video.mp4"])

        assert result.exit_code != 0
        assert "0 scenes" in result.output

    @patch("drone_reel.cli.analyze_scenes_batch")
    @patch("drone_reel.cli.SceneDetector")
    @patch("drone_reel.utils.resource_guard.check_available_memory_mb",
           return_value=float("inf"))
    @patch("drone_reel.utils.resource_guard.check_disk_space_mb",
           return_value=float("inf"))
    def test_all_scenes_filtered_out(
        self, mock_disk, mock_mem, mock_detector_cls, mock_analyze
    ):
        """Test handling when all scenes are filtered out by min-score."""
        scenes = [_make_scene(score=20.0)]
        mock_detector = MagicMock()
        mock_detector.detect_scenes.return_value = scenes
        mock_detector_cls.return_value = mock_detector
        mock_analyze.return_value = _make_analysis_result(scenes)

        runner = CliRunner()
        with runner.isolated_filesystem():
            Path("video.mp4").touch()
            result = runner.invoke(
                main,
                ["extract-clips", "-i", "video.mp4", "--min-score", "90"],
            )

        assert result.exit_code != 0
        assert "No scenes passed" in result.output

    @patch("drone_reel.cli.analyze_scenes_batch")
    @patch("drone_reel.cli.SceneDetector")
    @patch("drone_reel.utils.resource_guard.check_available_memory_mb",
           return_value=float("inf"))
    @patch("drone_reel.utils.resource_guard.check_disk_space_mb",
           return_value=float("inf"))
    def test_corrupted_video_skipped_in_directory(
        self, mock_disk, mock_mem, mock_detector_cls, mock_analyze
    ):
        """Test that corrupted videos in a directory are skipped with warning."""
        mock_detector = MagicMock()

        def detect_side_effect(path):
            if "bad" in str(path):
                raise Exception("Corrupted file")
            return [_make_scene(source_file=path)]

        mock_detector.detect_scenes.side_effect = detect_side_effect
        mock_detector_cls.return_value = mock_detector

        runner = CliRunner()
        with runner.isolated_filesystem():
            Path("good.mp4").touch()
            Path("bad.mp4").touch()
            # Need to patch find_video_files to return these
            with patch("drone_reel.cli.find_video_files") as mock_find:
                mock_find.return_value = [Path("good.mp4"), Path("bad.mp4")]
                good_scenes = [_make_scene(source_file=Path("good.mp4"))]
                mock_analyze.return_value = _make_analysis_result(good_scenes)

                # Also need to patch VideoProcessor to avoid real encoding
                with patch("drone_reel.cli.VideoProcessor") as mock_vp_cls:
                    mock_processor = MagicMock()
                    mock_clip = MagicMock()
                    mock_clip.w = 1920
                    mock_clip.h = 1080
                    mock_clip.duration = 5.0
                    mock_processor.extract_clip.return_value = mock_clip
                    mock_processor.write_clip.return_value = Path(
                        "clips/clip_001_s70.mp4"
                    )
                    mock_vp_cls.return_value = mock_processor

                    # write_clip needs to create the file for stat()
                    def write_side_effect(clip, path):
                        path.parent.mkdir(parents=True, exist_ok=True)
                        path.write_bytes(b"\x00" * 1000)
                        return path

                    mock_processor.write_clip.side_effect = write_side_effect

                    result = runner.invoke(
                        main,
                        ["extract-clips", "-i", ".", "-o", "clips"],
                    )

        assert "Skipping" in result.output or "Warning" in result.output


class TestExtractClipsOutput:
    """Tests for clip output behavior."""

    @patch("drone_reel.cli.analyze_scenes_batch")
    @patch("drone_reel.cli.SceneDetector")
    @patch("drone_reel.cli.VideoProcessor")
    @patch("drone_reel.utils.resource_guard.check_available_memory_mb",
           return_value=float("inf"))
    @patch("drone_reel.utils.resource_guard.check_disk_space_mb",
           return_value=float("inf"))
    def test_clips_named_with_score(
        self, mock_disk, mock_mem, mock_vp_cls, mock_detector_cls, mock_analyze
    ):
        """Test that output files are named clip_NNN_sSCORE.mp4."""
        scenes = [
            _make_scene(start=0, end=5, score=85.0),
            _make_scene(start=10, end=15, score=72.0),
        ]
        mock_detector = MagicMock()
        mock_detector.detect_scenes.return_value = scenes
        mock_detector_cls.return_value = mock_detector
        mock_analyze.return_value = _make_analysis_result(scenes)

        mock_processor = MagicMock()
        mock_clip = MagicMock()
        mock_clip.w = 1920
        mock_clip.h = 1080
        mock_clip.duration = 5.0
        mock_processor.extract_clip.return_value = mock_clip

        # Make write_clip create the file so stat() works
        def write_side_effect(clip, path):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"\x00" * 1000)
            return path

        mock_processor.write_clip.side_effect = write_side_effect
        mock_vp_cls.return_value = mock_processor

        runner = CliRunner()
        with runner.isolated_filesystem():
            Path("video.mp4").touch()
            result = runner.invoke(
                main,
                ["extract-clips", "-i", "video.mp4", "-o", "out", "-n", "2"],
            )

        # Check that write_clip was called with correctly named paths
        calls = mock_processor.write_clip.call_args_list
        assert len(calls) == 2
        assert "clip_001_s85" in str(calls[0])
        assert "clip_002_s72" in str(calls[1])

    @patch("drone_reel.cli.analyze_scenes_batch")
    @patch("drone_reel.cli.SceneDetector")
    @patch("drone_reel.cli.VideoProcessor")
    @patch("drone_reel.utils.resource_guard.check_available_memory_mb",
           return_value=float("inf"))
    @patch("drone_reel.utils.resource_guard.check_disk_space_mb",
           return_value=float("inf"))
    def test_count_limits_output(
        self, mock_disk, mock_mem, mock_vp_cls, mock_detector_cls, mock_analyze
    ):
        """Test that --count limits the number of extracted clips."""
        scenes = [
            _make_scene(start=i * 5, end=(i + 1) * 5, score=90 - i * 5)
            for i in range(10)
        ]
        mock_detector = MagicMock()
        mock_detector.detect_scenes.return_value = scenes
        mock_detector_cls.return_value = mock_detector
        mock_analyze.return_value = _make_analysis_result(scenes)

        mock_processor = MagicMock()
        mock_clip = MagicMock()
        mock_clip.w = 1920
        mock_clip.h = 1080
        mock_clip.duration = 5.0
        mock_processor.extract_clip.return_value = mock_clip

        def write_side_effect(clip, path):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"\x00" * 1000)
            return path

        mock_processor.write_clip.side_effect = write_side_effect
        mock_vp_cls.return_value = mock_processor

        runner = CliRunner()
        with runner.isolated_filesystem():
            Path("video.mp4").touch()
            result = runner.invoke(
                main,
                ["extract-clips", "-i", "video.mp4", "-n", "3"],
            )

        assert mock_processor.write_clip.call_count == 3

    @patch("drone_reel.cli.analyze_scenes_batch")
    @patch("drone_reel.cli.SceneDetector")
    @patch("drone_reel.cli.VideoProcessor")
    @patch("drone_reel.utils.resource_guard.check_available_memory_mb",
           return_value=float("inf"))
    @patch("drone_reel.utils.resource_guard.check_disk_space_mb",
           return_value=float("inf"))
    def test_existing_files_skipped_without_overwrite(
        self, mock_disk, mock_mem, mock_vp_cls, mock_detector_cls, mock_analyze
    ):
        """Test that existing clips are skipped without --overwrite."""
        scenes = [_make_scene(score=80.0)]
        mock_detector = MagicMock()
        mock_detector.detect_scenes.return_value = scenes
        mock_detector_cls.return_value = mock_detector
        mock_analyze.return_value = _make_analysis_result(scenes)

        mock_processor = MagicMock()
        mock_vp_cls.return_value = mock_processor

        runner = CliRunner()
        with runner.isolated_filesystem():
            Path("video.mp4").touch()
            out_dir = Path("clips")
            out_dir.mkdir()
            (out_dir / "clip_001_s80.mp4").write_bytes(b"\x00" * 100)

            result = runner.invoke(
                main,
                ["extract-clips", "-i", "video.mp4", "-o", "clips", "-n", "1"],
            )

        assert "Skipping" in result.output
        mock_processor.extract_clip.assert_not_called()

    @patch("drone_reel.cli.analyze_scenes_batch")
    @patch("drone_reel.cli.SceneDetector")
    @patch("drone_reel.cli.VideoProcessor")
    @patch("drone_reel.utils.resource_guard.check_available_memory_mb",
           return_value=float("inf"))
    @patch("drone_reel.utils.resource_guard.check_disk_space_mb",
           return_value=float("inf"))
    def test_overwrite_replaces_existing(
        self, mock_disk, mock_mem, mock_vp_cls, mock_detector_cls, mock_analyze
    ):
        """Test that --overwrite replaces existing clips."""
        scenes = [_make_scene(score=80.0)]
        mock_detector = MagicMock()
        mock_detector.detect_scenes.return_value = scenes
        mock_detector_cls.return_value = mock_detector
        mock_analyze.return_value = _make_analysis_result(scenes)

        mock_processor = MagicMock()
        mock_clip = MagicMock()
        mock_clip.w = 1920
        mock_clip.h = 1080
        mock_clip.duration = 5.0
        mock_processor.extract_clip.return_value = mock_clip

        def write_side_effect(clip, path):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"\x00" * 2000)
            return path

        mock_processor.write_clip.side_effect = write_side_effect
        mock_vp_cls.return_value = mock_processor

        runner = CliRunner()
        with runner.isolated_filesystem():
            Path("video.mp4").touch()
            out_dir = Path("clips")
            out_dir.mkdir()
            (out_dir / "clip_001_s80.mp4").write_bytes(b"\x00" * 100)

            result = runner.invoke(
                main,
                ["extract-clips", "-i", "video.mp4", "-o", "clips",
                 "-n", "1", "--overwrite"],
            )

        mock_processor.extract_clip.assert_called_once()


class TestExtractClipsSorting:
    """Tests for clip sorting behavior."""

    @patch("drone_reel.cli.analyze_scenes_batch")
    @patch("drone_reel.cli.SceneDetector")
    @patch("drone_reel.cli.VideoProcessor")
    @patch("drone_reel.utils.resource_guard.check_available_memory_mb",
           return_value=float("inf"))
    @patch("drone_reel.utils.resource_guard.check_disk_space_mb",
           return_value=float("inf"))
    def test_sort_by_score_default(
        self, mock_disk, mock_mem, mock_vp_cls, mock_detector_cls, mock_analyze
    ):
        """Test that clips are sorted by score by default (best first)."""
        scenes = [
            _make_scene(start=0, end=5, score=60.0),
            _make_scene(start=10, end=15, score=90.0),
            _make_scene(start=20, end=25, score=75.0),
        ]
        mock_detector = MagicMock()
        mock_detector.detect_scenes.return_value = scenes
        mock_detector_cls.return_value = mock_detector
        mock_analyze.return_value = _make_analysis_result(scenes)

        mock_processor = MagicMock()
        mock_clip = MagicMock()
        mock_clip.w = 1920
        mock_clip.h = 1080
        mock_clip.duration = 5.0
        mock_processor.extract_clip.return_value = mock_clip

        def write_side_effect(clip, path):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"\x00" * 1000)
            return path

        mock_processor.write_clip.side_effect = write_side_effect
        mock_vp_cls.return_value = mock_processor

        runner = CliRunner()
        with runner.isolated_filesystem():
            Path("video.mp4").touch()
            result = runner.invoke(
                main,
                ["extract-clips", "-i", "video.mp4", "-n", "3"],
            )

        calls = mock_processor.write_clip.call_args_list
        filenames = [str(c[0][1]) for c in calls]
        # Best score (90) should be clip_001
        assert "clip_001_s90" in filenames[0]
        assert "clip_002_s75" in filenames[1]
        assert "clip_003_s60" in filenames[2]


class TestExtractClipsJsonManifest:
    """Tests for JSON manifest output."""

    @patch("drone_reel.cli.analyze_scenes_batch")
    @patch("drone_reel.cli.SceneDetector")
    @patch("drone_reel.cli.VideoProcessor")
    @patch("drone_reel.utils.resource_guard.check_available_memory_mb",
           return_value=float("inf"))
    @patch("drone_reel.utils.resource_guard.check_disk_space_mb",
           return_value=float("inf"))
    def test_json_manifest_written(
        self, mock_disk, mock_mem, mock_vp_cls, mock_detector_cls, mock_analyze
    ):
        """Test that --json writes a manifest.json file."""
        scenes = [_make_scene(score=80.0)]
        mock_detector = MagicMock()
        mock_detector.detect_scenes.return_value = scenes
        mock_detector_cls.return_value = mock_detector
        mock_analyze.return_value = _make_analysis_result(scenes)

        mock_processor = MagicMock()
        mock_clip = MagicMock()
        mock_clip.w = 1920
        mock_clip.h = 1080
        mock_clip.duration = 5.0
        mock_processor.extract_clip.return_value = mock_clip

        def write_side_effect(clip, path):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"\x00" * 1000)
            return path

        mock_processor.write_clip.side_effect = write_side_effect
        mock_vp_cls.return_value = mock_processor

        runner = CliRunner()
        with runner.isolated_filesystem():
            Path("video.mp4").touch()
            result = runner.invoke(
                main,
                ["extract-clips", "-i", "video.mp4", "-o", "clips",
                 "--json", "-n", "1"],
            )

            manifest_path = Path("clips") / "manifest.json"
            assert manifest_path.exists()

            with open(manifest_path) as f:
                manifest = json.load(f)

            assert manifest["version"] == 1
            assert len(manifest["clips"]) == 1
            assert manifest["clips"][0]["score"] == 80.0
            assert manifest["summary"]["total_clips"] == 1

    @patch("drone_reel.cli.analyze_scenes_batch")
    @patch("drone_reel.cli.SceneDetector")
    @patch("drone_reel.cli.VideoProcessor")
    @patch("drone_reel.utils.resource_guard.check_available_memory_mb",
           return_value=float("inf"))
    @patch("drone_reel.utils.resource_guard.check_disk_space_mb",
           return_value=float("inf"))
    def test_no_json_by_default(
        self, mock_disk, mock_mem, mock_vp_cls, mock_detector_cls, mock_analyze
    ):
        """Test that manifest.json is NOT written without --json flag."""
        scenes = [_make_scene(score=80.0)]
        mock_detector = MagicMock()
        mock_detector.detect_scenes.return_value = scenes
        mock_detector_cls.return_value = mock_detector
        mock_analyze.return_value = _make_analysis_result(scenes)

        mock_processor = MagicMock()
        mock_clip = MagicMock()
        mock_clip.w = 1920
        mock_clip.h = 1080
        mock_clip.duration = 5.0
        mock_processor.extract_clip.return_value = mock_clip

        def write_side_effect(clip, path):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"\x00" * 1000)
            return path

        mock_processor.write_clip.side_effect = write_side_effect
        mock_vp_cls.return_value = mock_processor

        runner = CliRunner()
        with runner.isolated_filesystem():
            Path("video.mp4").touch()
            result = runner.invoke(
                main,
                ["extract-clips", "-i", "video.mp4", "-o", "clips", "-n", "1"],
            )

            manifest_path = Path("clips") / "manifest.json"
            assert not manifest_path.exists()


class TestExtractClipsNoFilter:
    """Tests for --no-filter behavior."""

    @patch("drone_reel.cli.analyze_scenes_batch")
    @patch("drone_reel.cli.SceneDetector")
    @patch("drone_reel.cli.VideoProcessor")
    @patch("drone_reel.utils.resource_guard.check_available_memory_mb",
           return_value=float("inf"))
    @patch("drone_reel.utils.resource_guard.check_disk_space_mb",
           return_value=float("inf"))
    def test_no_filter_includes_all_scenes(
        self, mock_disk, mock_mem, mock_vp_cls, mock_detector_cls, mock_analyze
    ):
        """Test that --no-filter bypasses quality filtering."""
        # Include a scene with low motion that would normally be filtered
        scenes = [
            _make_scene(start=0, end=5, score=80.0),
            _make_scene(start=10, end=15, score=50.0),
        ]
        mock_detector = MagicMock()
        mock_detector.detect_scenes.return_value = scenes
        mock_detector_cls.return_value = mock_detector

        # Give second scene very low motion (would be filtered)
        analysis = _make_analysis_result(scenes)
        analysis[id(scenes[1])]["motion_energy"] = 5.0  # Below min threshold
        mock_analyze.return_value = analysis

        mock_processor = MagicMock()
        mock_clip = MagicMock()
        mock_clip.w = 1920
        mock_clip.h = 1080
        mock_clip.duration = 5.0
        mock_processor.extract_clip.return_value = mock_clip

        def write_side_effect(clip, path):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"\x00" * 1000)
            return path

        mock_processor.write_clip.side_effect = write_side_effect
        mock_vp_cls.return_value = mock_processor

        runner = CliRunner()
        with runner.isolated_filesystem():
            Path("video.mp4").touch()
            result = runner.invoke(
                main,
                ["extract-clips", "-i", "video.mp4", "--no-filter", "-n", "10"],
            )

        # Both scenes should be extracted (low motion scene not filtered)
        assert mock_processor.write_clip.call_count == 2


class TestExtractClipsErrorHandling:
    """Tests for error handling during extraction."""

    @patch("drone_reel.cli.analyze_scenes_batch")
    @patch("drone_reel.cli.SceneDetector")
    @patch("drone_reel.cli.VideoProcessor")
    @patch("drone_reel.utils.resource_guard.check_available_memory_mb",
           return_value=float("inf"))
    @patch("drone_reel.utils.resource_guard.check_disk_space_mb",
           return_value=float("inf"))
    def test_failed_clip_continues_extraction(
        self, mock_disk, mock_mem, mock_vp_cls, mock_detector_cls, mock_analyze
    ):
        """Test that a failed clip extraction doesn't stop the batch."""
        scenes = [
            _make_scene(start=0, end=5, score=90.0),
            _make_scene(start=10, end=15, score=80.0),
        ]
        mock_detector = MagicMock()
        mock_detector.detect_scenes.return_value = scenes
        mock_detector_cls.return_value = mock_detector
        mock_analyze.return_value = _make_analysis_result(scenes)

        mock_processor = MagicMock()
        call_count = [0]

        def extract_side_effect(segment):
            call_count[0] += 1
            if call_count[0] == 1:
                raise Exception("Extraction failed")
            mock_clip = MagicMock()
            mock_clip.w = 1920
            mock_clip.h = 1080
            mock_clip.duration = 5.0
            return mock_clip

        mock_processor.extract_clip.side_effect = extract_side_effect

        def write_side_effect(clip, path):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"\x00" * 1000)
            return path

        mock_processor.write_clip.side_effect = write_side_effect
        mock_vp_cls.return_value = mock_processor

        runner = CliRunner()
        with runner.isolated_filesystem():
            Path("video.mp4").touch()
            result = runner.invoke(
                main,
                ["extract-clips", "-i", "video.mp4", "-n", "2"],
            )

        assert "Failed" in result.output
        # Second clip should still be extracted
        assert mock_processor.write_clip.call_count == 1

    @patch("drone_reel.utils.resource_guard.check_available_memory_mb",
           return_value=100.0)
    @patch("drone_reel.utils.resource_guard.check_disk_space_mb",
           return_value=10.0)
    def test_resource_preflight_blocks_on_error(self, mock_disk, mock_mem):
        """Test that resource preflight errors stop extraction."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            Path("video.mp4").touch()
            result = runner.invoke(
                main,
                ["extract-clips", "-i", "video.mp4",
                 "--quality", "ultra", "-n", "50"],
            )

        # Should fail due to insufficient resources
        assert result.exit_code != 0
