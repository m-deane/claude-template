"""Tests for resource preflight guard module."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from drone_reel.utils.resource_guard import (
    check_available_memory_mb,
    check_disk_space_mb,
    estimate_render_memory_mb,
    estimate_output_size_mb,
    preflight_check,
)


class TestCheckAvailableMemory:
    """Tests for check_available_memory_mb."""

    def test_returns_positive_float(self):
        """Available memory should be positive on any system."""
        result = check_available_memory_mb()
        assert isinstance(result, float)
        assert result > 0

    def test_returns_inf_on_failure(self):
        """Should return inf when detection fails."""
        with patch("subprocess.run", side_effect=Exception("fail")):
            with patch("platform.system", return_value="Darwin"):
                result = check_available_memory_mb()
                assert result == float("inf")

    def test_handles_unknown_platform(self):
        """Should return inf on unknown platform."""
        with patch("platform.system", return_value="UnknownOS"):
            result = check_available_memory_mb()
            assert result == float("inf")


class TestCheckDiskSpace:
    """Tests for check_disk_space_mb."""

    def test_returns_positive_float(self, tmp_path):
        """Disk space should be positive for existing paths."""
        result = check_disk_space_mb(tmp_path)
        assert isinstance(result, float)
        assert result > 0

    def test_handles_nonexistent_path(self, tmp_path):
        """Should resolve to parent for non-existent paths."""
        nonexistent = tmp_path / "does" / "not" / "exist.mp4"
        result = check_disk_space_mb(nonexistent)
        assert isinstance(result, float)
        assert result > 0

    def test_returns_inf_on_failure(self):
        """Should return inf when detection fails."""
        with patch("shutil.disk_usage", side_effect=Exception("fail")):
            result = check_disk_space_mb(Path("/nonexistent"))
            assert result == float("inf")


class TestEstimateRenderMemory:
    """Tests for estimate_render_memory_mb."""

    def test_4k_higher_than_1080p(self):
        """4K rendering should require more memory than 1080p."""
        mem_1080 = estimate_render_memory_mb(resolution_height=1080)
        mem_4k = estimate_render_memory_mb(resolution_height=2160)
        assert mem_4k > mem_1080

    def test_stabilization_increases_memory(self):
        """Stabilization should increase memory estimate."""
        mem_no_stab = estimate_render_memory_mb(resolution_height=1080, stabilize=False)
        mem_stab = estimate_render_memory_mb(resolution_height=1080, stabilize=True)
        assert mem_stab > mem_no_stab

    def test_more_clips_increases_memory(self):
        """More clips should increase memory estimate."""
        mem_5 = estimate_render_memory_mb(resolution_height=1080, clip_count=5)
        mem_20 = estimate_render_memory_mb(resolution_height=1080, clip_count=20)
        assert mem_20 > mem_5

    def test_returns_positive_float(self):
        """Should always return a positive value."""
        result = estimate_render_memory_mb(resolution_height=720)
        assert result > 0


class TestEstimateOutputSize:
    """Tests for estimate_output_size_mb."""

    def test_higher_bitrate_larger_file(self):
        """Higher bitrate should produce larger estimated file size."""
        size_15m = estimate_output_size_mb(30.0, "15M")
        size_80m = estimate_output_size_mb(30.0, "80M")
        assert size_80m > size_15m

    def test_longer_duration_larger_file(self):
        """Longer duration should produce larger estimated file size."""
        size_15s = estimate_output_size_mb(15.0, "15M")
        size_60s = estimate_output_size_mb(60.0, "15M")
        assert size_60s > size_15s

    def test_returns_positive(self):
        """Should return positive value."""
        result = estimate_output_size_mb(10.0, "15M")
        assert result > 0


class TestPreflightCheck:
    """Tests for preflight_check."""

    def test_returns_empty_when_resources_sufficient(self, tmp_path):
        """Should return empty list when all resources are sufficient."""
        output = tmp_path / "test.mp4"
        with patch("drone_reel.utils.resource_guard.check_available_memory_mb", return_value=16000.0):
            with patch("drone_reel.utils.resource_guard.check_disk_space_mb", return_value=50000.0):
                result = preflight_check(
                    output_path=output,
                    resolution_height=1080,
                    clip_count=5,
                    video_bitrate="15M",
                    duration=15.0,
                )
                assert result == []

    def test_returns_error_on_low_memory(self, tmp_path):
        """Should return error when memory is insufficient."""
        output = tmp_path / "test.mp4"
        with patch("drone_reel.utils.resource_guard.check_available_memory_mb", return_value=100.0):
            with patch("drone_reel.utils.resource_guard.check_disk_space_mb", return_value=50000.0):
                result = preflight_check(
                    output_path=output,
                    resolution_height=2160,
                    clip_count=10,
                    stabilize=True,
                    video_bitrate="80M",
                    duration=30.0,
                )
                errors = [r for r in result if r["level"] == "error"]
                assert len(errors) > 0
                assert "memory" in errors[0]["message"].lower()

    def test_returns_error_on_low_disk(self, tmp_path):
        """Should return error when disk space is insufficient."""
        output = tmp_path / "test.mp4"
        with patch("drone_reel.utils.resource_guard.check_available_memory_mb", return_value=16000.0):
            with patch("drone_reel.utils.resource_guard.check_disk_space_mb", return_value=10.0):
                result = preflight_check(
                    output_path=output,
                    resolution_height=2160,
                    clip_count=10,
                    video_bitrate="80M",
                    duration=30.0,
                )
                errors = [r for r in result if r["level"] == "error"]
                assert len(errors) > 0
                assert "disk" in errors[0]["message"].lower()

    def test_returns_warning_on_tight_memory(self, tmp_path):
        """Should return warning when memory is tight but sufficient."""
        output = tmp_path / "test.mp4"
        # Set available memory slightly above the estimated need (between 70-95% threshold)
        estimated = estimate_render_memory_mb(resolution_height=1080, clip_count=5)
        available = estimated / 0.8  # At 80% = between 70% and 95% thresholds
        with patch("drone_reel.utils.resource_guard.check_available_memory_mb", return_value=available):
            with patch("drone_reel.utils.resource_guard.check_disk_space_mb", return_value=50000.0):
                result = preflight_check(
                    output_path=output,
                    resolution_height=1080,
                    clip_count=5,
                    video_bitrate="15M",
                    duration=15.0,
                )
                warnings = [r for r in result if r["level"] == "warning"]
                assert len(warnings) > 0

    def test_handles_inf_memory_gracefully(self, tmp_path):
        """Should not produce issues when memory detection returns inf."""
        output = tmp_path / "test.mp4"
        with patch("drone_reel.utils.resource_guard.check_available_memory_mb", return_value=float("inf")):
            with patch("drone_reel.utils.resource_guard.check_disk_space_mb", return_value=float("inf")):
                result = preflight_check(
                    output_path=output,
                    resolution_height=2160,
                    clip_count=15,
                    stabilize=True,
                    video_bitrate="80M",
                    duration=60.0,
                )
                assert result == []
