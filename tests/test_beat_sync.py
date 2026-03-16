"""Comprehensive tests for beat synchronization module."""

from pathlib import Path
from unittest.mock import patch

import numpy as np
import pytest

from drone_reel.core.beat_sync import (
    BeatInfo,
    BeatSync,
    CutPoint,
)


class TestBeatInfo:
    """Tests for BeatInfo dataclass."""

    @pytest.fixture
    def sample_beat_info(self):
        """Create sample beat info."""
        return BeatInfo(
            tempo=120.0,
            beat_times=np.array([0.5, 1.0, 1.5, 2.0, 2.5, 3.0]),
            downbeat_times=np.array([0.5, 1.5, 2.5]),
            duration=10.0,
            energy_profile=np.linspace(0.3, 0.8, 100),
            time_signature=(4, 4),
            phrase_boundaries=np.array([0.0, 4.0, 8.0]),
            tempo_changes=[],
            spectral_profile=np.ones(100) * 0.5,
            onset_density=np.ones(100) * 0.5,
            harmonic_energy=np.ones(100) * 0.5,
            percussive_energy=np.ones(100) * 0.5,
        )

    def test_beat_interval_calculation(self, sample_beat_info):
        """Test beat interval property calculates correctly."""
        # 120 BPM = 0.5 seconds per beat
        assert sample_beat_info.beat_interval == 0.5

    def test_beat_interval_different_tempo(self):
        """Test beat interval with different tempo."""
        beat_info = BeatInfo(
            tempo=90.0,
            beat_times=np.array([]),
            downbeat_times=np.array([]),
            duration=10.0,
            energy_profile=np.array([]),
            time_signature=(4, 4),
            phrase_boundaries=np.array([]),
            tempo_changes=[],
            spectral_profile=np.array([]),
            onset_density=np.array([]),
            harmonic_energy=np.array([]),
            percussive_energy=np.array([]),
        )
        # 90 BPM = 0.667 seconds per beat
        assert abs(beat_info.beat_interval - 0.6667) < 0.001

    def test_beat_count(self, sample_beat_info):
        """Test beat count property."""
        assert sample_beat_info.beat_count == 6

    def test_beat_count_empty(self):
        """Test beat count with no beats."""
        beat_info = BeatInfo(
            tempo=120.0,
            beat_times=np.array([]),
            downbeat_times=np.array([]),
            duration=10.0,
            energy_profile=np.array([]),
            time_signature=(4, 4),
            phrase_boundaries=np.array([]),
            tempo_changes=[],
            spectral_profile=np.array([]),
            onset_density=np.array([]),
            harmonic_energy=np.array([]),
            percussive_energy=np.array([]),
        )
        assert beat_info.beat_count == 0


class TestCutPoint:
    """Tests for CutPoint dataclass."""

    def test_cutpoint_creation(self):
        """Test CutPoint initialization."""
        cut = CutPoint(time=2.5, strength=0.9, is_downbeat=True, beat_index=5)

        assert cut.time == 2.5
        assert cut.strength == 0.9
        assert cut.is_downbeat is True
        assert cut.beat_index == 5

    def test_cutpoint_defaults(self):
        """Test CutPoint with default values."""
        cut = CutPoint(time=1.0, strength=0.7, is_downbeat=False, beat_index=2)

        assert cut.time == 1.0
        assert cut.strength == 0.7
        assert cut.is_downbeat is False


class TestBeatSync:
    """Tests for BeatSync class."""

    def test_initialization_defaults(self):
        """Test default initialization values."""
        sync = BeatSync()

        assert sync.hop_length == 512
        assert sync.min_tempo == 60.0
        assert sync.max_tempo == 180.0

    def test_initialization_custom(self):
        """Test custom initialization values."""
        sync = BeatSync(hop_length=1024, min_tempo=80.0, max_tempo=160.0)

        assert sync.hop_length == 1024
        assert sync.min_tempo == 80.0
        assert sync.max_tempo == 160.0


class TestBeatSyncAnalyze:
    """Tests for audio analysis functionality."""

    @pytest.fixture
    def beat_sync(self):
        """Create a BeatSync instance."""
        return BeatSync()

    def create_test_audio(self, duration=5.0, sr=22050, tempo=120.0):
        """
        Create synthetic audio with clear beats.

        Args:
            duration: Audio duration in seconds
            sr: Sample rate
            tempo: BPM for beat generation

        Returns:
            Tuple of (audio_array, sample_rate)
        """
        # Generate time array
        t = np.linspace(0, duration, int(sr * duration))

        # Create sine wave base
        frequency = 440.0  # A4
        audio = np.sin(2 * np.pi * frequency * t)

        # Add beats at tempo intervals
        beat_interval = 60.0 / tempo
        for beat_time in np.arange(0, duration, beat_interval):
            beat_idx = int(beat_time * sr)
            if beat_idx < len(audio):
                # Add percussion-like click
                click_duration = int(0.05 * sr)
                click = np.exp(-np.arange(click_duration) / (sr * 0.01))
                audio[beat_idx : beat_idx + click_duration] += click * 0.5

        # Normalize
        audio = audio / np.max(np.abs(audio))

        return audio.astype(np.float32), sr

    @patch("librosa.load")
    @patch("librosa.beat.beat_track")
    @patch("librosa.get_duration")
    @patch("librosa.frames_to_time")
    def test_analyze_basic(
        self,
        mock_frames_to_time,
        mock_get_duration,
        mock_beat_track,
        mock_load,
        beat_sync,
    ):
        """Test basic audio analysis."""
        # Setup mocks
        mock_audio = np.random.randn(22050 * 5)
        mock_load.return_value = (mock_audio, 22050)
        mock_get_duration.return_value = 5.0
        mock_beat_track.return_value = (120.0, np.array([10, 20, 30, 40]))
        mock_frames_to_time.return_value = np.array([0.5, 1.0, 1.5, 2.0])

        result = beat_sync.analyze(Path("/tmp/test.mp3"))

        assert isinstance(result, BeatInfo)
        assert result.tempo == 120.0
        assert len(result.beat_times) == 4
        assert result.duration == 5.0

    @patch("librosa.load")
    @patch("librosa.beat.beat_track")
    @patch("librosa.get_duration")
    @patch("librosa.frames_to_time")
    @patch("librosa.effects.hpss")
    @patch("librosa.feature.rms")
    @patch("librosa.feature.spectral_centroid")
    @patch("librosa.onset.onset_detect")
    def test_analyze_with_downbeats(
        self,
        mock_onset_detect,
        mock_spectral,
        mock_rms,
        mock_hpss,
        mock_frames_to_time,
        mock_get_duration,
        mock_beat_track,
        mock_load,
        beat_sync,
    ):
        """Test analysis detects downbeats."""
        # Setup mocks
        mock_audio = np.random.randn(22050 * 5)
        mock_load.return_value = (mock_audio, 22050)
        mock_get_duration.return_value = 5.0
        mock_beat_track.return_value = (120.0, np.array([10, 20, 30, 40]))
        mock_frames_to_time.return_value = np.array([0.5, 1.0, 1.5, 2.0])
        mock_hpss.return_value = (mock_audio * 0.5, mock_audio * 0.5)
        mock_rms.return_value = np.array([np.linspace(0.3, 0.8, 100)])
        mock_spectral.return_value = np.array([np.linspace(0.4, 0.7, 100)])
        mock_onset_detect.return_value = np.array([10, 30, 50, 70])

        result = beat_sync.analyze(Path("/tmp/test.mp3"))

        assert len(result.downbeat_times) > 0
        assert len(result.energy_profile) > 0
        assert result.time_signature[0] >= 2
        assert len(result.phrase_boundaries) >= 0
        assert len(result.spectral_profile) > 0
        assert len(result.onset_density) > 0

    @patch("librosa.load")
    @patch("librosa.beat.beat_track")
    @patch("librosa.get_duration")
    @patch("librosa.frames_to_time")
    def test_analyze_tempo_as_array(
        self,
        mock_frames_to_time,
        mock_get_duration,
        mock_beat_track,
        mock_load,
        beat_sync,
    ):
        """Test analysis handles tempo returned as array."""
        mock_audio = np.random.randn(22050 * 5)
        mock_load.return_value = (mock_audio, 22050)
        mock_get_duration.return_value = 5.0
        # Return tempo as array
        mock_beat_track.return_value = (np.array([128.5]), np.array([10, 20, 30]))
        mock_frames_to_time.return_value = np.array([0.5, 1.0, 1.5])

        result = beat_sync.analyze(Path("/tmp/test.mp3"))

        # Should convert array to float
        assert isinstance(result.tempo, float)
        assert result.tempo == 128.5


class TestBeatSyncDownbeats:
    """Tests for downbeat detection."""

    @pytest.fixture
    def beat_sync(self):
        """Create a BeatSync instance."""
        return BeatSync()

    @patch("librosa.onset.onset_strength")
    @patch("librosa.feature.melspectrogram")
    @patch("librosa.power_to_db")
    def test_detect_downbeats_basic(
        self, mock_power_to_db, mock_mel, mock_onset_strength, beat_sync
    ):
        """Test basic downbeat detection."""
        mock_audio = np.random.randn(22050 * 5)
        y_harmonic = mock_audio * 0.5
        y_percussive = mock_audio * 0.5
        sr = 22050
        beat_times = np.array([0.5, 1.0, 1.5, 2.0, 2.5])
        time_signature = (4, 4)

        # Simulate varying onset strengths
        mock_onset_strength.return_value = np.linspace(0.3, 1.0, 100)
        mock_mel.return_value = np.ones((128, 100))
        mock_power_to_db.return_value = np.ones((128, 100))

        result = beat_sync._detect_downbeats(
            mock_audio, y_harmonic, y_percussive, sr, beat_times, time_signature
        )

        assert isinstance(result, np.ndarray)
        assert len(result) > 0

    def test_detect_downbeats_empty(self, beat_sync):
        """Test downbeat detection with no beats."""
        mock_audio = np.random.randn(22050 * 5)
        y_harmonic = mock_audio * 0.5
        y_percussive = mock_audio * 0.5
        sr = 22050
        beat_times = np.array([])
        time_signature = (4, 4)

        result = beat_sync._detect_downbeats(
            mock_audio, y_harmonic, y_percussive, sr, beat_times, time_signature
        )

        assert len(result) == 0


class TestBeatSyncCutPoints:
    """Tests for cut point generation."""

    @pytest.fixture
    def beat_sync(self):
        """Create a BeatSync instance."""
        return BeatSync()

    @pytest.fixture
    def sample_beat_info(self):
        """Create sample beat info."""
        return BeatInfo(
            tempo=120.0,
            beat_times=np.array([0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]),
            downbeat_times=np.array([0.5, 1.5, 2.5, 3.5]),
            duration=10.0,
            energy_profile=np.linspace(0.3, 0.9, 100),
            time_signature=(4, 4),
            phrase_boundaries=np.array([0.0, 4.0, 8.0]),
            tempo_changes=[],
            spectral_profile=np.ones(100) * 0.5,
            onset_density=np.ones(100) * 0.5,
            harmonic_energy=np.ones(100) * 0.5,
            percussive_energy=np.ones(100) * 0.5,
        )

    def test_get_cut_points_basic(self, beat_sync, sample_beat_info):
        """Test basic cut point generation."""
        cut_points = beat_sync.get_cut_points(
            sample_beat_info, target_duration=5.0, min_clip_length=1.0, max_clip_length=3.0
        )

        assert len(cut_points) > 0
        # First cut should be at time 0
        assert cut_points[0].time == 0.0
        assert cut_points[0].strength == 1.0

    def test_get_cut_points_respects_min_length(self, beat_sync, sample_beat_info):
        """Test cut points respect minimum clip length."""
        cut_points = beat_sync.get_cut_points(
            sample_beat_info, target_duration=10.0, min_clip_length=2.0, max_clip_length=4.0
        )

        # Check all cuts are at least min_clip_length apart
        for i in range(len(cut_points) - 1):
            gap = cut_points[i + 1].time - cut_points[i].time
            assert gap >= 2.0

    def test_get_cut_points_respects_max_length(self, beat_sync, sample_beat_info):
        """Test cut points respect maximum clip length."""
        cut_points = beat_sync.get_cut_points(
            sample_beat_info, target_duration=10.0, min_clip_length=1.0, max_clip_length=2.5
        )

        # Check no cuts are more than max_clip_length apart
        for i in range(len(cut_points) - 1):
            gap = cut_points[i + 1].time - cut_points[i].time
            assert gap <= 2.5 + 0.1  # Small tolerance

    def test_get_cut_points_prefer_downbeats(self, beat_sync, sample_beat_info):
        """Test cut points prefer downbeats when enabled."""
        cut_points = beat_sync.get_cut_points(
            sample_beat_info,
            target_duration=5.0,
            min_clip_length=1.0,
            max_clip_length=3.0,
            prefer_downbeats=True,
        )

        # Check that downbeat cuts have higher strength
        downbeat_cuts = [cp for cp in cut_points if cp.is_downbeat]
        regular_cuts = [cp for cp in cut_points if not cp.is_downbeat]

        if downbeat_cuts and regular_cuts:
            avg_downbeat_strength = sum(cp.strength for cp in downbeat_cuts) / len(
                downbeat_cuts
            )
            avg_regular_strength = sum(cp.strength for cp in regular_cuts) / len(
                regular_cuts
            )
            assert avg_downbeat_strength >= avg_regular_strength

    def test_get_cut_points_no_downbeat_preference(self, beat_sync, sample_beat_info):
        """Test cut points without downbeat preference."""
        cut_points = beat_sync.get_cut_points(
            sample_beat_info,
            target_duration=5.0,
            min_clip_length=1.0,
            max_clip_length=3.0,
            prefer_downbeats=False,
        )

        assert len(cut_points) > 0

    def test_get_cut_points_short_target_duration(self, beat_sync, sample_beat_info):
        """Test cut points with very short target duration."""
        cut_points = beat_sync.get_cut_points(
            sample_beat_info, target_duration=2.0, min_clip_length=0.5, max_clip_length=1.5
        )

        # Should only get cuts within target duration
        assert all(cp.time <= 2.0 for cp in cut_points)


class TestCalculateClipDurations:
    """Tests for clip duration calculation."""

    @pytest.fixture
    def beat_sync(self):
        """Create a BeatSync instance."""
        return BeatSync()

    def test_calculate_clip_durations_basic(self, beat_sync):
        """Test basic clip duration calculation."""
        cut_points = [
            CutPoint(time=0.0, strength=1.0, is_downbeat=True, beat_index=0),
            CutPoint(time=2.0, strength=0.8, is_downbeat=False, beat_index=4),
            CutPoint(time=4.5, strength=0.9, is_downbeat=True, beat_index=9),
        ]

        durations = beat_sync.calculate_clip_durations(cut_points, target_duration=10.0)

        # Should have 2 durations between cuts, plus final segment
        assert len(durations) == 3
        assert durations[0] == 2.0  # 2.0 - 0.0
        assert durations[1] == 2.5  # 4.5 - 2.0
        assert durations[2] == 5.5  # 10.0 - 4.5

    def test_calculate_clip_durations_single_cut(self, beat_sync):
        """Test calculation with single cut point."""
        cut_points = [
            CutPoint(time=0.0, strength=1.0, is_downbeat=True, beat_index=0),
        ]

        durations = beat_sync.calculate_clip_durations(cut_points, target_duration=5.0)

        assert len(durations) == 1
        assert durations[0] == 5.0

    def test_calculate_clip_durations_no_final_segment(self, beat_sync):
        """Test calculation when final segment is too short."""
        cut_points = [
            CutPoint(time=0.0, strength=1.0, is_downbeat=True, beat_index=0),
            CutPoint(time=2.0, strength=0.8, is_downbeat=False, beat_index=4),
            CutPoint(time=4.8, strength=0.9, is_downbeat=True, beat_index=9),
        ]

        durations = beat_sync.calculate_clip_durations(cut_points, target_duration=5.0)

        # Final segment (5.0 - 4.8 = 0.2) is too short (< 0.5)
        assert len(durations) == 2


class TestEnergyAnalysis:
    """Tests for energy profile analysis."""

    @pytest.fixture
    def beat_sync(self):
        """Create a BeatSync instance."""
        return BeatSync()

    @patch("librosa.feature.rms")
    def test_compute_energy_profile(self, mock_rms, beat_sync):
        """Test energy profile computation."""
        mock_audio = np.random.randn(22050 * 5)
        sr = 22050

        # Simulate RMS values
        mock_rms.return_value = np.array([np.linspace(0.1, 0.9, 100)])

        result = beat_sync._compute_energy_profile(mock_audio, sr)

        assert isinstance(result, np.ndarray)
        assert len(result) == 100
        # Should be normalized to 0-1 range
        assert result.min() >= 0.0
        assert result.max() <= 1.0

    def test_get_energy_at_time_basic(self, beat_sync):
        """Test getting energy at specific time."""
        beat_info = BeatInfo(
            tempo=120.0,
            beat_times=np.array([]),
            downbeat_times=np.array([]),
            duration=10.0,
            energy_profile=np.linspace(0.0, 1.0, 100),
            time_signature=(4, 4),
            phrase_boundaries=np.array([]),
            tempo_changes=[],
            spectral_profile=np.ones(100) * 0.5,
            onset_density=np.ones(100) * 0.5,
            harmonic_energy=np.ones(100) * 0.5,
            percussive_energy=np.ones(100) * 0.5,
        )

        # At time 5.0 (midpoint), energy should be around 0.5
        energy = beat_sync.get_energy_at_time(beat_info, 5.0)
        assert 0.4 < energy < 0.6

    def test_get_energy_at_time_start(self, beat_sync):
        """Test getting energy at start."""
        beat_info = BeatInfo(
            tempo=120.0,
            beat_times=np.array([]),
            downbeat_times=np.array([]),
            duration=10.0,
            energy_profile=np.linspace(0.0, 1.0, 100),
            time_signature=(4, 4),
            phrase_boundaries=np.array([]),
            tempo_changes=[],
            spectral_profile=np.ones(100) * 0.5,
            onset_density=np.ones(100) * 0.5,
            harmonic_energy=np.ones(100) * 0.5,
            percussive_energy=np.ones(100) * 0.5,
        )

        energy = beat_sync.get_energy_at_time(beat_info, 0.0)
        assert energy < 0.1

    def test_get_energy_at_time_end(self, beat_sync):
        """Test getting energy at end."""
        beat_info = BeatInfo(
            tempo=120.0,
            beat_times=np.array([]),
            downbeat_times=np.array([]),
            duration=10.0,
            energy_profile=np.linspace(0.0, 1.0, 100),
            time_signature=(4, 4),
            phrase_boundaries=np.array([]),
            tempo_changes=[],
            spectral_profile=np.ones(100) * 0.5,
            onset_density=np.ones(100) * 0.5,
            harmonic_energy=np.ones(100) * 0.5,
            percussive_energy=np.ones(100) * 0.5,
        )

        energy = beat_sync.get_energy_at_time(beat_info, 10.0)
        assert energy > 0.9

    def test_get_energy_zero_duration(self, beat_sync):
        """Test energy with zero duration audio."""
        beat_info = BeatInfo(
            tempo=120.0,
            beat_times=np.array([]),
            downbeat_times=np.array([]),
            duration=0.0,
            energy_profile=np.array([]),
            time_signature=(4, 4),
            phrase_boundaries=np.array([]),
            tempo_changes=[],
            spectral_profile=np.array([]),
            onset_density=np.array([]),
            harmonic_energy=np.array([]),
            percussive_energy=np.array([]),
        )

        energy = beat_sync.get_energy_at_time(beat_info, 0.0)
        assert energy == 0.5  # Default value


class TestTransitionIntensity:
    """Tests for transition intensity suggestions."""

    @pytest.fixture
    def beat_sync(self):
        """Create a BeatSync instance."""
        return BeatSync()

    @pytest.fixture
    def sample_beat_info(self):
        """Create sample beat info."""
        return BeatInfo(
            tempo=120.0,
            beat_times=np.array([]),
            downbeat_times=np.array([]),
            duration=10.0,
            energy_profile=np.linspace(0.3, 0.9, 100),
            time_signature=(4, 4),
            phrase_boundaries=np.array([]),
            tempo_changes=[],
            spectral_profile=np.ones(100) * 0.5,
            onset_density=np.ones(100) * 0.5,
            harmonic_energy=np.ones(100) * 0.5,
            percussive_energy=np.ones(100) * 0.5,
        )

    def test_suggest_transition_hard(self, beat_sync, sample_beat_info):
        """Test hard transition suggestion."""
        cut_point = CutPoint(time=9.0, strength=0.9, is_downbeat=True, beat_index=18)

        intensity = beat_sync.suggest_transition_intensity(sample_beat_info, cut_point)

        # High energy + downbeat = hard transition
        assert intensity == "hard"

    def test_suggest_transition_medium(self, beat_sync, sample_beat_info):
        """Test medium transition suggestion."""
        cut_point = CutPoint(time=6.0, strength=0.85, is_downbeat=False, beat_index=12)

        intensity = beat_sync.suggest_transition_intensity(sample_beat_info, cut_point)

        # High strength = medium transition
        assert intensity == "medium"

    def test_suggest_transition_soft(self, beat_sync, sample_beat_info):
        """Test soft transition suggestion."""
        cut_point = CutPoint(time=2.0, strength=0.6, is_downbeat=False, beat_index=4)

        intensity = beat_sync.suggest_transition_intensity(sample_beat_info, cut_point)

        # Low energy + low strength = soft transition
        assert intensity == "soft"


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    @pytest.fixture
    def beat_sync(self):
        """Create a BeatSync instance."""
        return BeatSync()

    @patch("librosa.load")
    @patch("librosa.beat.beat_track")
    @patch("librosa.get_duration")
    @patch("librosa.frames_to_time")
    def test_very_short_audio(
        self,
        mock_frames_to_time,
        mock_get_duration,
        mock_beat_track,
        mock_load,
        beat_sync,
    ):
        """Test analysis with very short audio."""
        # 0.5 second audio
        mock_audio = np.random.randn(22050 // 2)
        mock_load.return_value = (mock_audio, 22050)
        mock_get_duration.return_value = 0.5
        mock_beat_track.return_value = (120.0, np.array([]))
        mock_frames_to_time.return_value = np.array([])

        result = beat_sync.analyze(Path("/tmp/short.mp3"))

        assert result.duration == 0.5
        assert len(result.beat_times) == 0

    def test_no_beats_detected(self, beat_sync):
        """Test handling when no beats are detected."""
        beat_info = BeatInfo(
            tempo=120.0,
            beat_times=np.array([]),
            downbeat_times=np.array([]),
            duration=10.0,
            energy_profile=np.linspace(0.3, 0.8, 100),
            time_signature=(4, 4),
            phrase_boundaries=np.array([]),
            tempo_changes=[],
            spectral_profile=np.ones(100) * 0.5,
            onset_density=np.ones(100) * 0.5,
            harmonic_energy=np.ones(100) * 0.5,
            percussive_energy=np.ones(100) * 0.5,
        )

        cut_points = beat_sync.get_cut_points(
            beat_info, target_duration=5.0, min_clip_length=1.0, max_clip_length=3.0
        )

        # Should still return at least the initial cut point
        assert len(cut_points) >= 1
        assert cut_points[0].time == 0.0

    def test_downbeat_only_mode(self, beat_sync):
        """Test downbeat_only mode filters non-downbeat candidates."""
        beat_times = np.array([0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0])
        downbeat_times = np.array([1.0, 3.0])  # Only beats at 1.0 and 3.0 are downbeats

        beat_info = BeatInfo(
            tempo=120.0,
            beat_times=beat_times,
            downbeat_times=downbeat_times,
            duration=5.0,
            energy_profile=np.linspace(0.3, 0.8, 100),
            time_signature=(4, 4),
            phrase_boundaries=np.array([]),
            tempo_changes=[],
            spectral_profile=np.ones(100) * 0.5,
            onset_density=np.ones(100) * 0.5,
            harmonic_energy=np.ones(100) * 0.5,
            percussive_energy=np.ones(100) * 0.5,
        )

        # Without downbeat_only, should have more cut points
        all_cuts = beat_sync.get_cut_points(
            beat_info, target_duration=5.0, min_clip_length=0.3, max_clip_length=3.0,
            downbeat_only=False,
        )

        # With downbeat_only, should have fewer cut points
        downbeat_cuts = beat_sync.get_cut_points(
            beat_info, target_duration=5.0, min_clip_length=0.3, max_clip_length=3.0,
            downbeat_only=True,
        )

        assert len(downbeat_cuts) <= len(all_cuts)
        # All downbeat_only cut points should be at downbeat times (or time 0)
        for cp in downbeat_cuts:
            assert cp.time == 0.0 or cp.is_downbeat
