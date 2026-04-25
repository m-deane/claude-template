"""Tests for utility modules."""

from pathlib import Path

from drone_reel.utils.config import (
    Config,
    load_config,
    merge_cli_args,
    save_config,
)
from drone_reel.utils.file_utils import (
    find_audio_files,
    find_video_files,
    format_duration,
    format_file_size,
    get_unique_output_path,
    is_audio_file,
    is_video_file,
)


class TestConfig:
    """Tests for Config class."""

    def test_default_values(self):
        """Test default configuration values."""
        config = Config()
        assert config.output_duration == 45.0
        assert config.output_fps == 30
        assert config.aspect_ratio == "9:16"
        assert config.color_preset == "drone_aerial"

    def test_get_output_dimensions(self):
        """Test output dimension calculation."""
        config = Config(output_width=1080, aspect_ratio="9:16")
        width, height = config.get_output_dimensions()

        assert width == 1080
        assert height == 1920

    def test_get_output_dimensions_square(self):
        """Test output dimensions for square ratio."""
        config = Config(output_width=1080, aspect_ratio="1:1")
        width, height = config.get_output_dimensions()

        assert width == 1080
        assert height == 1080


class TestConfigPersistence:
    """Tests for config save/load functionality."""

    def test_save_and_load_config(self, tmp_path):
        """Test saving and loading config."""
        config = Config(
            output_duration=60.0,
            color_preset="cinematic",
        )

        config_path = tmp_path / "config.json"
        save_config(config, config_path)

        loaded = load_config(config_path)

        assert loaded.output_duration == 60.0
        assert loaded.color_preset == "cinematic"

    def test_load_nonexistent_returns_default(self, tmp_path):
        """Test loading nonexistent config returns defaults."""
        config_path = tmp_path / "nonexistent.json"
        loaded = load_config(config_path)

        default = Config()
        assert loaded.output_duration == default.output_duration

    def test_merge_cli_args(self):
        """Test merging CLI args into config."""
        config = Config(output_duration=45.0, color_preset="none")

        merged = merge_cli_args(
            config,
            output_duration=30.0,
            color_preset="cinematic",
        )

        assert merged.output_duration == 30.0
        assert merged.color_preset == "cinematic"

    def test_merge_cli_args_none_ignored(self):
        """Test that None CLI args don't override config."""
        config = Config(output_duration=45.0)

        merged = merge_cli_args(
            config,
            output_duration=None,
        )

        assert merged.output_duration == 45.0


class TestFileUtils:
    """Tests for file utility functions."""

    def test_is_video_file_true(self):
        """Test video file detection."""
        assert is_video_file(Path("video.mp4"))
        assert is_video_file(Path("video.mov"))
        assert is_video_file(Path("video.MOV"))
        assert is_video_file(Path("video.avi"))

    def test_is_video_file_false(self):
        """Test non-video file rejection."""
        assert not is_video_file(Path("audio.mp3"))
        assert not is_video_file(Path("image.jpg"))
        assert not is_video_file(Path("document.pdf"))

    def test_is_audio_file_true(self):
        """Test audio file detection."""
        assert is_audio_file(Path("audio.mp3"))
        assert is_audio_file(Path("audio.wav"))
        assert is_audio_file(Path("audio.WAV"))
        assert is_audio_file(Path("audio.m4a"))

    def test_is_audio_file_false(self):
        """Test non-audio file rejection."""
        assert not is_audio_file(Path("video.mp4"))
        assert not is_audio_file(Path("image.jpg"))

    def test_find_video_files(self, tmp_path):
        """Test finding video files in directory."""
        # Create test files
        (tmp_path / "video1.mp4").touch()
        (tmp_path / "video2.mov").touch()
        (tmp_path / "audio.mp3").touch()
        (tmp_path / "document.txt").touch()

        videos = find_video_files(tmp_path)

        assert len(videos) == 2
        assert all(is_video_file(v) for v in videos)

    def test_find_video_files_recursive(self, tmp_path):
        """Test recursive video file finding."""
        subdir = tmp_path / "subdir"
        subdir.mkdir()

        (tmp_path / "video1.mp4").touch()
        (subdir / "video2.mp4").touch()

        # Non-recursive
        videos = find_video_files(tmp_path, recursive=False)
        assert len(videos) == 1

        # Recursive
        videos = find_video_files(tmp_path, recursive=True)
        assert len(videos) == 2

    def test_find_audio_files(self, tmp_path):
        """Test finding audio files in directory."""
        (tmp_path / "audio1.mp3").touch()
        (tmp_path / "audio2.wav").touch()
        (tmp_path / "video.mp4").touch()

        audio = find_audio_files(tmp_path)

        assert len(audio) == 2
        assert all(is_audio_file(a) for a in audio)

    def test_find_files_empty_directory(self, tmp_path):
        """Test finding files in empty directory."""
        videos = find_video_files(tmp_path)
        assert len(videos) == 0

    def test_find_files_nonexistent_directory(self):
        """Test finding files in nonexistent directory."""
        videos = find_video_files(Path("/nonexistent/path"))
        assert len(videos) == 0


class TestFormatting:
    """Tests for formatting functions."""

    def test_format_duration_seconds(self):
        """Test duration formatting for seconds."""
        assert format_duration(30) == "00:30"
        assert format_duration(59) == "00:59"

    def test_format_duration_minutes(self):
        """Test duration formatting for minutes."""
        assert format_duration(60) == "01:00"
        assert format_duration(90) == "01:30"
        assert format_duration(125) == "02:05"

    def test_format_duration_hours(self):
        """Test duration formatting for hours."""
        assert format_duration(3600) == "01:00:00"
        assert format_duration(3661) == "01:01:01"

    def test_format_file_size_bytes(self):
        """Test file size formatting for bytes."""
        assert "B" in format_file_size(500)

    def test_format_file_size_kilobytes(self):
        """Test file size formatting for kilobytes."""
        assert "KB" in format_file_size(1024 * 5)

    def test_format_file_size_megabytes(self):
        """Test file size formatting for megabytes."""
        assert "MB" in format_file_size(1024 * 1024 * 50)

    def test_format_file_size_gigabytes(self):
        """Test file size formatting for gigabytes."""
        assert "GB" in format_file_size(1024 * 1024 * 1024 * 2)


class TestUniqueOutputPath:
    """Tests for unique output path generation."""

    def test_unique_path_no_conflict(self, tmp_path):
        """Test path returned as-is when no conflict."""
        path = tmp_path / "output.mp4"
        result = get_unique_output_path(path)
        assert result == path

    def test_unique_path_with_conflict(self, tmp_path):
        """Test numbered path when conflict exists."""
        path = tmp_path / "output.mp4"
        path.touch()

        result = get_unique_output_path(path)

        assert result != path
        assert "output_1" in result.name

    def test_unique_path_multiple_conflicts(self, tmp_path):
        """Test incrementing number with multiple conflicts."""
        (tmp_path / "output.mp4").touch()
        (tmp_path / "output_1.mp4").touch()
        (tmp_path / "output_2.mp4").touch()

        result = get_unique_output_path(tmp_path / "output.mp4")

        assert "output_3" in result.name
