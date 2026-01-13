"""
Beat detection and music synchronization for video editing.

Uses librosa for audio analysis to detect beats, tempo, and musical
structure for synchronizing video cuts with music.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import librosa
import numpy as np


@dataclass
class BeatInfo:
    """Information about detected beats and tempo."""

    tempo: float
    beat_times: np.ndarray
    downbeat_times: np.ndarray
    duration: float
    energy_profile: np.ndarray

    @property
    def beat_interval(self) -> float:
        """Average interval between beats in seconds."""
        return 60.0 / self.tempo

    @property
    def beat_count(self) -> int:
        """Total number of beats detected."""
        return len(self.beat_times)


@dataclass
class CutPoint:
    """A suggested cut point for video editing."""

    time: float
    strength: float  # 0-1, how strong this cut point is
    is_downbeat: bool
    beat_index: int


class BeatSync:
    """
    Analyzes music tracks to extract beat timing for video synchronization.

    Provides beat times, tempo, and suggested cut points that align
    with the musical structure.
    """

    def __init__(
        self,
        hop_length: int = 512,
        min_tempo: float = 60.0,
        max_tempo: float = 180.0,
    ):
        """
        Initialize the beat synchronizer.

        Args:
            hop_length: Number of samples between analysis frames
            min_tempo: Minimum expected tempo (BPM)
            max_tempo: Maximum expected tempo (BPM)
        """
        self.hop_length = hop_length
        self.min_tempo = min_tempo
        self.max_tempo = max_tempo

    def analyze(self, audio_path: Path) -> BeatInfo:
        """
        Analyze an audio file to extract beat information.

        Args:
            audio_path: Path to the audio file (mp3, wav, etc.)

        Returns:
            BeatInfo with tempo, beat times, and energy profile
        """
        y, sr = librosa.load(str(audio_path), sr=None)
        duration = librosa.get_duration(y=y, sr=sr)

        tempo, beat_frames = librosa.beat.beat_track(
            y=y,
            sr=sr,
            hop_length=self.hop_length,
            start_bpm=120.0,
            tightness=100,
        )

        if isinstance(tempo, np.ndarray):
            tempo = float(tempo[0])

        beat_times = librosa.frames_to_time(beat_frames, sr=sr, hop_length=self.hop_length)

        downbeat_times = self._detect_downbeats(y, sr, beat_times)

        energy_profile = self._compute_energy_profile(y, sr)

        return BeatInfo(
            tempo=tempo,
            beat_times=beat_times,
            downbeat_times=downbeat_times,
            duration=duration,
            energy_profile=energy_profile,
        )

    def _detect_downbeats(
        self, y: np.ndarray, sr: int, beat_times: np.ndarray
    ) -> np.ndarray:
        """
        Detect downbeats (first beat of each measure).

        Uses onset strength to identify stronger beats that likely
        correspond to measure boundaries.
        """
        onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=self.hop_length)

        beat_frames = librosa.time_to_frames(beat_times, sr=sr, hop_length=self.hop_length)
        beat_strengths = []

        for frame in beat_frames:
            if frame < len(onset_env):
                beat_strengths.append(onset_env[frame])
            else:
                beat_strengths.append(0.0)

        beat_strengths = np.array(beat_strengths)

        if len(beat_strengths) == 0:
            return np.array([])

        threshold = np.percentile(beat_strengths, 75)
        downbeat_mask = beat_strengths >= threshold

        downbeat_indices = np.where(downbeat_mask)[0]
        if len(downbeat_indices) > 0:
            downbeat_times = beat_times[downbeat_indices]
        else:
            downbeat_times = beat_times[::4] if len(beat_times) >= 4 else beat_times

        return downbeat_times

    def _compute_energy_profile(self, y: np.ndarray, sr: int) -> np.ndarray:
        """Compute the energy profile over time."""
        rms = librosa.feature.rms(y=y, hop_length=self.hop_length)[0]
        rms_normalized = (rms - rms.min()) / (rms.max() - rms.min() + 1e-6)
        return rms_normalized

    def get_cut_points(
        self,
        beat_info: BeatInfo,
        target_duration: float,
        min_clip_length: float = 1.5,
        max_clip_length: float = 4.0,
        prefer_downbeats: bool = True,
    ) -> list[CutPoint]:
        """
        Generate suggested cut points for video editing.

        Args:
            beat_info: BeatInfo from analyze()
            target_duration: Target video duration in seconds
            min_clip_length: Minimum time between cuts
            max_clip_length: Maximum time between cuts
            prefer_downbeats: Weight downbeats more heavily

        Returns:
            List of CutPoint objects with suggested edit times
        """
        cut_points = []
        current_time = 0.0
        beat_idx = 0

        cut_points.append(
            CutPoint(time=0.0, strength=1.0, is_downbeat=True, beat_index=0)
        )

        while current_time < min(target_duration, beat_info.duration):
            candidates = []

            for i, beat_time in enumerate(beat_info.beat_times):
                if beat_time <= current_time + min_clip_length:
                    continue
                if beat_time > current_time + max_clip_length:
                    break

                is_downbeat = beat_time in beat_info.downbeat_times
                strength = 0.7
                if is_downbeat and prefer_downbeats:
                    strength = 1.0

                energy_idx = int(
                    beat_time / beat_info.duration * len(beat_info.energy_profile)
                )
                if energy_idx < len(beat_info.energy_profile):
                    energy = beat_info.energy_profile[energy_idx]
                    strength *= 0.7 + 0.3 * energy

                candidates.append(
                    CutPoint(
                        time=beat_time,
                        strength=strength,
                        is_downbeat=is_downbeat,
                        beat_index=i,
                    )
                )

            if not candidates:
                next_time = current_time + max_clip_length
                if next_time < target_duration:
                    candidates.append(
                        CutPoint(
                            time=next_time,
                            strength=0.5,
                            is_downbeat=False,
                            beat_index=beat_idx,
                        )
                    )
                else:
                    break

            best_cut = max(candidates, key=lambda c: c.strength)
            cut_points.append(best_cut)
            current_time = best_cut.time
            beat_idx = best_cut.beat_index

        return cut_points

    def calculate_clip_durations(
        self,
        cut_points: list[CutPoint],
        target_duration: float,
    ) -> list[float]:
        """
        Calculate the duration for each clip between cut points.

        Args:
            cut_points: List of CutPoint objects
            target_duration: Target total duration

        Returns:
            List of clip durations in seconds
        """
        durations = []

        for i in range(len(cut_points) - 1):
            duration = cut_points[i + 1].time - cut_points[i].time
            durations.append(duration)

        if cut_points:
            final_duration = target_duration - cut_points[-1].time
            if final_duration > 0.5:
                durations.append(final_duration)

        return durations

    def get_energy_at_time(self, beat_info: BeatInfo, time: float) -> float:
        """Get the normalized energy level at a specific time."""
        if beat_info.duration == 0:
            return 0.5

        idx = int(time / beat_info.duration * len(beat_info.energy_profile))
        idx = max(0, min(idx, len(beat_info.energy_profile) - 1))
        return float(beat_info.energy_profile[idx])

    def suggest_transition_intensity(
        self, beat_info: BeatInfo, cut_point: CutPoint
    ) -> str:
        """
        Suggest transition intensity based on beat strength and energy.

        Returns:
            'hard' for strong beats, 'medium' for regular beats, 'soft' for weak points
        """
        energy = self.get_energy_at_time(beat_info, cut_point.time)

        if cut_point.is_downbeat and energy > 0.7:
            return "hard"
        elif cut_point.strength > 0.8 or energy > 0.6:
            return "medium"
        else:
            return "soft"
