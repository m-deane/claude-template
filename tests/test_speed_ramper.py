"""
Tests for the speed ramping system.
"""

import numpy as np
import pytest
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

from drone_reel.core.beat_sync import BeatInfo
from drone_reel.core.scene_detector import SceneInfo
from drone_reel.core.speed_ramper import SpeedRamp, SpeedRamper
from drone_reel.core.video_processor import ClipSegment


class TestSpeedRamp:
    """Test SpeedRamp dataclass."""

    def test_valid_ramp_creation(self):
        """Test creating a valid speed ramp."""
        ramp = SpeedRamp(
            start_time=1.0, end_time=3.0, start_speed=1.0, end_speed=0.5, easing="ease_in"
        )
        assert ramp.start_time == 1.0
        assert ramp.end_time == 3.0
        assert ramp.start_speed == 1.0
        assert ramp.end_speed == 0.5
        assert ramp.easing == "ease_in"
        assert ramp.duration == 2.0

    def test_invalid_start_time(self):
        """Test that negative start_time raises ValueError."""
        with pytest.raises(ValueError, match="start_time must be non-negative"):
            SpeedRamp(start_time=-1.0, end_time=3.0, start_speed=1.0, end_speed=0.5)

    def test_invalid_end_time(self):
        """Test that end_time <= start_time raises ValueError."""
        with pytest.raises(ValueError, match="end_time must be greater than start_time"):
            SpeedRamp(start_time=3.0, end_time=3.0, start_speed=1.0, end_speed=0.5)

    def test_invalid_start_speed(self):
        """Test that non-positive start_speed raises ValueError."""
        with pytest.raises(ValueError, match="start_speed must be positive"):
            SpeedRamp(start_time=1.0, end_time=3.0, start_speed=0.0, end_speed=0.5)

    def test_invalid_end_speed(self):
        """Test that non-positive end_speed raises ValueError."""
        with pytest.raises(ValueError, match="end_speed must be positive"):
            SpeedRamp(start_time=1.0, end_time=3.0, start_speed=1.0, end_speed=-0.5)

    def test_invalid_easing(self):
        """Test that invalid easing type raises ValueError."""
        with pytest.raises(ValueError, match="easing must be one of"):
            SpeedRamp(
                start_time=1.0, end_time=3.0, start_speed=1.0, end_speed=0.5, easing="invalid"
            )

    def test_all_easing_types(self):
        """Test all valid easing types."""
        for easing in ["linear", "ease_in", "ease_out", "ease_in_out"]:
            ramp = SpeedRamp(start_time=0, end_time=1, start_speed=1, end_speed=0.5, easing=easing)
            assert ramp.easing == easing


class TestEasingFunctions:
    """Test easing functions."""

    @pytest.fixture
    def ramper(self):
        """Create a SpeedRamper instance."""
        return SpeedRamper()

    def test_ease_linear(self, ramper):
        """Test linear easing."""
        assert ramper._ease_linear(0.0) == 0.0
        assert ramper._ease_linear(0.5) == 0.5
        assert ramper._ease_linear(1.0) == 1.0

    def test_ease_in(self, ramper):
        """Test cubic ease-in."""
        assert ramper._ease_in(0.0) == 0.0
        assert ramper._ease_in(0.5) == 0.125  # 0.5^3
        assert ramper._ease_in(1.0) == 1.0
        # Should start slow
        assert ramper._ease_in(0.2) < 0.2

    def test_ease_out(self, ramper):
        """Test cubic ease-out."""
        assert ramper._ease_out(0.0) == 0.0
        assert ramper._ease_out(1.0) == 1.0
        # Should end slow
        assert ramper._ease_out(0.8) > 0.8

    def test_ease_in_out(self, ramper):
        """Test cubic ease-in-out."""
        assert ramper._ease_in_out(0.0) == 0.0
        assert ramper._ease_in_out(0.5) == 0.5
        assert ramper._ease_in_out(1.0) == 1.0
        # Should start slow and end slow
        assert ramper._ease_in_out(0.2) < 0.2
        assert ramper._ease_in_out(0.8) > 0.8


class TestSpeedInterpolation:
    """Test speed interpolation within ramps."""

    @pytest.fixture
    def ramper(self):
        """Create a SpeedRamper instance."""
        return SpeedRamper()

    def test_interpolate_before_ramp(self, ramper):
        """Test interpolation before ramp starts."""
        ramp = SpeedRamp(start_time=2.0, end_time=4.0, start_speed=1.0, end_speed=0.5)
        assert ramper._interpolate_speed(ramp, 1.0) == 1.0

    def test_interpolate_after_ramp(self, ramper):
        """Test interpolation after ramp ends."""
        ramp = SpeedRamp(start_time=2.0, end_time=4.0, start_speed=1.0, end_speed=0.5)
        assert ramper._interpolate_speed(ramp, 5.0) == 0.5

    def test_interpolate_at_ramp_start(self, ramper):
        """Test interpolation at ramp start."""
        ramp = SpeedRamp(start_time=2.0, end_time=4.0, start_speed=1.0, end_speed=0.5)
        assert ramper._interpolate_speed(ramp, 2.0) == 1.0

    def test_interpolate_at_ramp_end(self, ramper):
        """Test interpolation at ramp end."""
        ramp = SpeedRamp(start_time=2.0, end_time=4.0, start_speed=1.0, end_speed=0.5)
        assert ramper._interpolate_speed(ramp, 4.0) == 0.5

    def test_interpolate_linear_midpoint(self, ramper):
        """Test linear interpolation at midpoint."""
        ramp = SpeedRamp(
            start_time=2.0, end_time=4.0, start_speed=1.0, end_speed=0.5, easing="linear"
        )
        assert ramper._interpolate_speed(ramp, 3.0) == 0.75

    def test_interpolate_ease_in(self, ramper):
        """Test ease-in interpolation."""
        ramp = SpeedRamp(
            start_time=0.0, end_time=2.0, start_speed=1.0, end_speed=0.5, easing="ease_in"
        )
        speed_at_quarter = ramper._interpolate_speed(ramp, 0.5)
        # With cubic ease-in, progress should be slower at start
        # t=0.25 -> eased=0.25^3=0.015625 -> speed ≈ 0.992
        assert 0.98 < speed_at_quarter < 1.0


class TestApplyRamp:
    """Test applying speed ramps to clips."""

    @pytest.fixture
    def ramper(self):
        """Create a SpeedRamper instance."""
        return SpeedRamper()

    @pytest.fixture
    def mock_clip(self):
        """Create a mock VideoFileClip."""
        clip = Mock()
        clip.duration = 10.0
        clip.time_transform = Mock(return_value=clip)
        clip.with_duration = Mock(return_value=clip)
        return clip

    def test_apply_single_ramp(self, ramper, mock_clip):
        """Test applying a single speed ramp."""
        ramp = SpeedRamp(start_time=2.0, end_time=4.0, start_speed=1.0, end_speed=0.5)
        result = ramper.apply_ramp(mock_clip, ramp)

        # Verify time_transform was called
        mock_clip.time_transform.assert_called_once()
        # Verify with_duration was called
        mock_clip.with_duration.assert_called_once()
        assert result is not None

    def test_apply_ramp_duration_calculation(self, ramper, mock_clip):
        """Test that duration is calculated correctly."""
        # Ramp from speed 1.0 to 0.5 over 2 seconds
        ramp = SpeedRamp(start_time=2.0, end_time=4.0, start_speed=1.0, end_speed=0.5)
        ramper.apply_ramp(mock_clip, ramp)

        # Check that with_duration was called with a value > original duration
        call_args = mock_clip.with_duration.call_args[0]
        assert len(call_args) > 0
        # Slowing down should increase duration
        assert call_args[0] > 10.0

    def test_apply_multiple_ramps(self, ramper, mock_clip):
        """Test applying multiple non-overlapping ramps."""
        ramps = [
            SpeedRamp(start_time=1.0, end_time=2.0, start_speed=1.0, end_speed=0.5),
            SpeedRamp(start_time=5.0, end_time=6.0, start_speed=1.0, end_speed=2.0),
        ]
        result = ramper.apply_multiple_ramps(mock_clip, ramps)

        mock_clip.time_transform.assert_called_once()
        mock_clip.with_duration.assert_called_once()
        assert result is not None

    def test_apply_multiple_ramps_empty_list(self, ramper, mock_clip):
        """Test applying empty ramps list returns original clip."""
        result = ramper.apply_multiple_ramps(mock_clip, [])
        assert result == mock_clip

    def test_overlapping_ramps_raises_error(self, ramper, mock_clip):
        """Test that overlapping ramps raise ValueError."""
        ramps = [
            SpeedRamp(start_time=1.0, end_time=3.0, start_speed=1.0, end_speed=0.5),
            SpeedRamp(start_time=2.5, end_time=4.0, start_speed=1.0, end_speed=2.0),
        ]
        with pytest.raises(ValueError, match="Overlapping ramps detected"):
            ramper.apply_multiple_ramps(mock_clip, ramps)


class TestAutoDetectRampPoints:
    """Test automatic detection of ramp points."""

    @pytest.fixture
    def ramper(self):
        """Create a SpeedRamper instance."""
        return SpeedRamper()

    @pytest.fixture
    def scene(self):
        """Create a test SceneInfo."""
        return SceneInfo(
            start_time=0.0,
            end_time=5.0,
            duration=5.0,
            score=75.0,
            source_file=Path("/test/video.mp4"),
        )

    @pytest.fixture
    def beat_info(self):
        """Create a test BeatInfo."""
        return BeatInfo(
            tempo=120.0,
            beat_times=np.array([0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]),
            downbeat_times=np.array([0.5, 2.5, 4.5]),
            duration=5.0,
            energy_profile=np.linspace(0.3, 0.8, 100),
            time_signature=(4, 4),
            phrase_boundaries=np.array([0.0, 2.5]),
            tempo_changes=[],
            spectral_profile=np.linspace(0.4, 0.7, 100),
            onset_density=np.linspace(0.2, 0.6, 100),
            harmonic_energy=np.linspace(0.3, 0.7, 100),
            percussive_energy=np.linspace(0.4, 0.8, 100),
        )

    def test_auto_detect_without_beats(self, ramper, scene):
        """Test auto-detection without beat info."""
        ramps = ramper.auto_detect_ramp_points(scene)
        assert isinstance(ramps, list)
        assert len(ramps) > 0
        # Should detect slow-motion opportunities
        assert all(isinstance(r, SpeedRamp) for r in ramps)

    def test_auto_detect_with_beats(self, ramper, scene, beat_info):
        """Test auto-detection with beat info."""
        ramps = ramper.auto_detect_ramp_points(scene, beat_info=beat_info)
        assert isinstance(ramps, list)
        assert len(ramps) > 0

    def test_auto_detect_short_scene(self, ramper):
        """Test auto-detection with short scene."""
        short_scene = SceneInfo(
            start_time=0.0,
            end_time=1.5,
            duration=1.5,
            score=75.0,
            source_file=Path("/test/video.mp4"),
        )
        ramps = ramper.auto_detect_ramp_points(short_scene)
        # Short scenes may have fewer or no ramps
        assert isinstance(ramps, list)

    def test_auto_detect_low_score_scene(self, ramper):
        """Test auto-detection with low score scene."""
        low_score_scene = SceneInfo(
            start_time=0.0,
            end_time=5.0,
            duration=5.0,
            score=40.0,
            source_file=Path("/test/video.mp4"),
        )
        ramps = ramper.auto_detect_ramp_points(low_score_scene)
        # Low score scenes may have fewer ramps
        assert isinstance(ramps, list)


class TestBeatSyncedRamps:
    """Test beat-synchronized ramp creation."""

    @pytest.fixture
    def ramper(self):
        """Create a SpeedRamper instance."""
        return SpeedRamper()

    def test_create_beat_synced_ramps_basic(self, ramper):
        """Test basic beat-synced ramp creation."""
        clip_duration = 10.0
        beat_times = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0])
        drop_times = np.array([2.0, 6.0])

        ramps = ramper.create_beat_synced_ramps(clip_duration, beat_times, drop_times)

        assert isinstance(ramps, list)
        assert len(ramps) > 0
        # Should create ramps around drops
        assert all(isinstance(r, SpeedRamp) for r in ramps)

    def test_create_beat_synced_ramps_edge_drops(self, ramper):
        """Test that drops near clip edges are handled properly."""
        clip_duration = 5.0
        beat_times = np.array([0.5, 1.5, 2.5, 3.5, 4.5])
        drop_times = np.array([0.5, 4.5])  # Near start and end

        ramps = ramper.create_beat_synced_ramps(clip_duration, beat_times, drop_times)

        # Drops too close to edges should be skipped
        for ramp in ramps:
            assert 0 <= ramp.start_time < ramp.end_time <= clip_duration

    def test_create_beat_synced_ramps_no_drops(self, ramper):
        """Test with no drop times."""
        clip_duration = 5.0
        beat_times = np.array([1.0, 2.0, 3.0, 4.0])
        drop_times = np.array([])

        ramps = ramper.create_beat_synced_ramps(clip_duration, beat_times, drop_times)

        assert isinstance(ramps, list)
        assert len(ramps) == 0

    def test_create_beat_synced_ramps_speed_patterns(self, ramper):
        """Test that ramps follow correct speed patterns around drops."""
        clip_duration = 10.0
        beat_times = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        drop_times = np.array([3.0])

        ramps = ramper.create_beat_synced_ramps(clip_duration, beat_times, drop_times)

        # Should have ramps that slow down before and speed up after
        pre_drop_ramps = [r for r in ramps if r.end_time <= 3.0]
        post_drop_ramps = [r for r in ramps if r.start_time >= 3.0]

        # At least one pre-drop ramp should slow down
        assert any(r.end_speed < r.start_speed for r in pre_drop_ramps)


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    @pytest.fixture
    def ramper(self):
        """Create a SpeedRamper instance."""
        return SpeedRamper()

    def test_ramp_at_clip_start(self, ramper):
        """Test ramp starting at t=0."""
        ramp = SpeedRamp(start_time=0.0, end_time=2.0, start_speed=1.0, end_speed=0.5)
        assert ramp.start_time == 0.0
        assert ramper._interpolate_speed(ramp, 0.0) == 1.0

    def test_ramp_at_clip_end(self, ramper):
        """Test ramp ending at clip duration."""
        ramp = SpeedRamp(start_time=8.0, end_time=10.0, start_speed=1.0, end_speed=0.5)
        assert ramp.end_time == 10.0
        assert ramper._interpolate_speed(ramp, 10.0) == 0.5

    def test_very_short_ramp(self, ramper):
        """Test very short ramp duration."""
        ramp = SpeedRamp(start_time=5.0, end_time=5.1, start_speed=1.0, end_speed=0.5)
        assert abs(ramp.duration - 0.1) < 1e-9

    def test_extreme_speed_change(self, ramper):
        """Test extreme speed changes."""
        ramp = SpeedRamp(start_time=1.0, end_time=2.0, start_speed=0.1, end_speed=5.0)
        mid_speed = ramper._interpolate_speed(ramp, 1.5)
        assert 0.1 < mid_speed < 5.0

    def test_calculate_ramped_duration_no_ramps(self, ramper):
        """Test duration calculation with no ramps."""
        duration = ramper.calculate_ramped_duration(10.0, [])
        assert duration == 10.0

    def test_calculate_ramped_duration_slowdown(self, ramper):
        """Test that slowing down increases duration."""
        ramps = [SpeedRamp(start_time=2.0, end_time=4.0, start_speed=1.0, end_speed=0.5)]
        duration = ramper.calculate_ramped_duration(10.0, ramps)
        # Slowing down should increase duration
        assert duration > 10.0

    def test_calculate_ramped_duration_speedup(self, ramper):
        """Test that speeding up decreases duration."""
        ramps = [SpeedRamp(start_time=2.0, end_time=4.0, start_speed=1.0, end_speed=2.0)]
        duration = ramper.calculate_ramped_duration(10.0, ramps)
        # Speeding up should decrease duration
        assert duration < 10.0

    def test_multiple_ramps_non_overlapping(self, ramper):
        """Test multiple non-overlapping ramps in sequence."""
        ramps = [
            SpeedRamp(start_time=1.0, end_time=2.0, start_speed=1.0, end_speed=0.5),
            SpeedRamp(start_time=3.0, end_time=4.0, start_speed=1.0, end_speed=0.5),
            SpeedRamp(start_time=6.0, end_time=7.0, start_speed=1.0, end_speed=2.0),
        ]
        duration = ramper.calculate_ramped_duration(10.0, ramps)
        assert duration > 0


class TestIntegration:
    """Integration tests with real-world scenarios."""

    @pytest.fixture
    def ramper(self):
        """Create a SpeedRamper instance."""
        return SpeedRamper()

    def test_full_workflow_without_beats(self, ramper):
        """Test complete workflow without beat synchronization."""
        scene = SceneInfo(
            start_time=0.0,
            end_time=10.0,
            duration=10.0,
            score=80.0,
            source_file=Path("/test/video.mp4"),
        )

        # Auto-detect ramps
        ramps = ramper.auto_detect_ramp_points(scene)
        assert len(ramps) > 0

        # Calculate new duration
        new_duration = ramper.calculate_ramped_duration(scene.duration, ramps)
        assert new_duration > 0

    def test_full_workflow_with_beats(self, ramper):
        """Test complete workflow with beat synchronization."""
        scene = SceneInfo(
            start_time=0.0,
            end_time=10.0,
            duration=10.0,
            score=80.0,
            source_file=Path("/test/video.mp4"),
        )

        beat_info = BeatInfo(
            tempo=120.0,
            beat_times=np.array([0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]),
            downbeat_times=np.array([0.5, 2.5, 4.5]),
            duration=10.0,
            energy_profile=np.linspace(0.3, 0.8, 200),
            time_signature=(4, 4),
            phrase_boundaries=np.array([0.0, 2.5, 5.0]),
            tempo_changes=[],
            spectral_profile=np.linspace(0.4, 0.7, 200),
            onset_density=np.linspace(0.2, 0.6, 200),
            harmonic_energy=np.linspace(0.3, 0.7, 200),
            percussive_energy=np.linspace(0.4, 0.8, 200),
        )

        # Auto-detect ramps with beats
        ramps = ramper.auto_detect_ramp_points(scene, beat_info=beat_info)
        assert len(ramps) > 0

        # Calculate new duration
        new_duration = ramper.calculate_ramped_duration(scene.duration, ramps)
        assert new_duration > 0

    def test_easing_continuity(self, ramper):
        """Test that easing functions are continuous."""
        ramp = SpeedRamp(
            start_time=0.0, end_time=2.0, start_speed=1.0, end_speed=0.5, easing="ease_in_out"
        )

        # Sample speeds at many points
        times = np.linspace(0, 2, 100)
        speeds = [ramper._interpolate_speed(ramp, t) for t in times]

        # Check continuity (no large jumps)
        for i in range(len(speeds) - 1):
            diff = abs(speeds[i + 1] - speeds[i])
            assert diff < 0.1  # No large discontinuities

    def test_ramp_ordering(self, ramper):
        """Test that ramps are properly sorted and handled."""
        # Create ramps in random order
        ramps = [
            SpeedRamp(start_time=5.0, end_time=6.0, start_speed=1.0, end_speed=0.5),
            SpeedRamp(start_time=1.0, end_time=2.0, start_speed=1.0, end_speed=2.0),
            SpeedRamp(start_time=3.0, end_time=4.0, start_speed=1.0, end_speed=0.8),
        ]

        # Should handle unsorted ramps
        duration = ramper.calculate_ramped_duration(10.0, ramps)
        assert duration > 0
