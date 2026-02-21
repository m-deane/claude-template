"""
Beat detection and music synchronization for video editing.

Uses librosa for audio analysis to detect beats, tempo, and musical
structure for synchronizing video cuts with music.
"""

import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import librosa
import numpy as np
from scipy import signal


@dataclass
class TransitionRecommendation:
    """Recommendation for video transition at a cut point."""

    intensity: float  # 0-1, continuous intensity level
    transition_type: str  # 'cut', 'fade', 'crossfade', 'impact'
    duration: float  # Recommended transition duration in seconds
    energy_gradient: str  # 'rising', 'falling', 'stable'


@dataclass
class BeatInfo:
    """Information about detected beats and tempo."""

    tempo: float
    beat_times: np.ndarray
    downbeat_times: np.ndarray
    duration: float
    energy_profile: np.ndarray
    time_signature: tuple[int, int]  # (beats_per_measure, note_value)
    phrase_boundaries: np.ndarray  # Musical phrase/section boundaries
    tempo_changes: list[tuple[float, float]]  # (time, new_tempo) pairs
    spectral_profile: np.ndarray  # Spectral centroid over time
    onset_density: np.ndarray  # Onset event density
    harmonic_energy: np.ndarray  # Harmonic component energy
    percussive_energy: np.ndarray  # Percussive component energy

    @property
    def beat_interval(self) -> float:
        """Average interval between beats in seconds."""
        if self.tempo <= 0:
            return 0.5  # Fallback: 120 BPM equivalent
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
    is_phrase_boundary: bool = False
    transition_rec: Optional[TransitionRecommendation] = None


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

        # Detect tempo and beats
        tempo, beat_frames = librosa.beat.beat_track(
            y=y,
            sr=sr,
            hop_length=self.hop_length,
            start_bpm=120.0,
            tightness=100,
        )

        if isinstance(tempo, np.ndarray):
            tempo = float(tempo[0])

        # Guard against zero/negative tempo from librosa
        if tempo <= 0:
            tempo = 120.0

        beat_times = librosa.frames_to_time(beat_frames, sr=sr, hop_length=self.hop_length)

        # Detect time signature
        time_signature = self._estimate_time_signature(y, sr, beat_times)

        # Detect tempo changes
        tempo_changes = self._detect_tempo_changes(y, sr)

        # Separate harmonic and percussive components
        y_harmonic, y_percussive = librosa.effects.hpss(y)

        # Detect downbeats with enhanced multi-feature analysis
        downbeat_times = self._detect_downbeats(
            y, y_harmonic, y_percussive, sr, beat_times, time_signature
        )

        # Detect phrase boundaries
        phrase_boundaries = self._detect_phrase_boundaries(y, sr)

        # Compute enhanced energy profile
        energy_profile = self._compute_energy_profile(y, sr)

        # Compute spectral profile
        spectral_profile = self._compute_spectral_profile(y, sr)

        # Compute onset density
        onset_density = self._compute_onset_density(y, sr)

        # Compute harmonic and percussive energy
        harmonic_energy = self._compute_energy_profile(y_harmonic, sr)
        percussive_energy = self._compute_energy_profile(y_percussive, sr)

        return BeatInfo(
            tempo=tempo,
            beat_times=beat_times,
            downbeat_times=downbeat_times,
            duration=duration,
            energy_profile=energy_profile,
            time_signature=time_signature,
            phrase_boundaries=phrase_boundaries,
            tempo_changes=tempo_changes,
            spectral_profile=spectral_profile,
            onset_density=onset_density,
            harmonic_energy=harmonic_energy,
            percussive_energy=percussive_energy,
        )

    def _estimate_time_signature(
        self, y: np.ndarray, sr: int, beat_times: np.ndarray
    ) -> tuple[int, int]:
        """
        Estimate time signature using autocorrelation of beat strengths.

        Returns:
            (beats_per_measure, note_value) e.g., (4, 4) for 4/4 time
        """
        if len(beat_times) < 8:
            return (4, 4)  # Default to 4/4

        onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=self.hop_length)
        beat_frames = librosa.time_to_frames(beat_times, sr=sr, hop_length=self.hop_length)

        beat_strengths = []
        for frame in beat_frames:
            if frame < len(onset_env):
                beat_strengths.append(onset_env[frame])
            else:
                beat_strengths.append(0.0)

        beat_strengths = np.array(beat_strengths)

        # Try common time signatures
        max_beats_per_measure = min(8, len(beat_strengths) // 2)
        best_score = -1
        best_signature = (4, 4)

        for beats_per_measure in range(2, max_beats_per_measure + 1):
            # Calculate autocorrelation at this lag
            if len(beat_strengths) < beats_per_measure * 2:
                continue

            score = 0
            count = 0
            for i in range(0, len(beat_strengths) - beats_per_measure, beats_per_measure):
                score += beat_strengths[i]
                count += 1

            avg_score = score / count if count > 0 else 0

            if avg_score > best_score:
                best_score = avg_score
                best_signature = (beats_per_measure, 4)

        return best_signature

    def _detect_tempo_changes(
        self, y: np.ndarray, sr: int, window_size: float = 8.0
    ) -> list[tuple[float, float]]:
        """
        Detect significant tempo changes using windowed tempo estimation.

        Args:
            y: Audio time series
            sr: Sample rate
            window_size: Window size in seconds for tempo estimation

        Returns:
            List of (time, new_tempo) tuples
        """
        duration = librosa.get_duration(y=y, sr=sr)
        window_samples = int(window_size * sr)
        hop_samples = window_samples // 2

        tempo_changes = []
        prev_tempo = None

        for start_sample in range(0, len(y) - window_samples, hop_samples):
            window = y[start_sample : start_sample + window_samples]
            tempo, _ = librosa.beat.beat_track(
                y=window, sr=sr, hop_length=self.hop_length
            )

            if isinstance(tempo, np.ndarray):
                tempo = float(tempo[0])

            if prev_tempo is not None and abs(tempo - prev_tempo) > 10:
                time = start_sample / sr
                tempo_changes.append((time, tempo))

            prev_tempo = tempo

        return tempo_changes

    def _detect_downbeats(
        self,
        y: np.ndarray,
        y_harmonic: np.ndarray,
        y_percussive: np.ndarray,
        sr: int,
        beat_times: np.ndarray,
        time_signature: tuple[int, int],
    ) -> np.ndarray:
        """
        Detect downbeats using multi-feature analysis.

        Combines onset strength, low-frequency flux, and percussive onsets
        with adaptive thresholding.
        """
        if len(beat_times) == 0:
            return np.array([])

        # Feature 1: Standard onset strength
        onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=self.hop_length)

        # Feature 2: Low-frequency flux (bass emphasis)
        S = librosa.feature.melspectrogram(
            y=y, sr=sr, hop_length=self.hop_length, n_mels=128
        )
        S_db = librosa.power_to_db(S, ref=np.max)
        # Focus on low frequencies (first 20% of mel bands)
        low_freq_flux = np.sum(np.abs(np.diff(S_db[:25, :], axis=1)), axis=0)
        low_freq_flux = np.concatenate([[0], low_freq_flux])  # Pad to match length

        # Feature 3: Percussive onset strength
        percussive_onset = librosa.onset.onset_strength(
            y=y_percussive, sr=sr, hop_length=self.hop_length
        )

        # Align all features to same length
        min_len = min(len(onset_env), len(low_freq_flux), len(percussive_onset))
        onset_env = onset_env[:min_len]
        low_freq_flux = low_freq_flux[:min_len]
        percussive_onset = percussive_onset[:min_len]

        # Normalize each feature
        onset_env = (onset_env - onset_env.min()) / (onset_env.max() - onset_env.min() + 1e-6)
        low_freq_flux = (low_freq_flux - low_freq_flux.min()) / (
            low_freq_flux.max() - low_freq_flux.min() + 1e-6
        )
        percussive_onset = (percussive_onset - percussive_onset.min()) / (
            percussive_onset.max() - percussive_onset.min() + 1e-6
        )

        # Combine features with weights
        combined_strength = (
            0.4 * onset_env + 0.3 * low_freq_flux + 0.3 * percussive_onset
        )

        # Get beat frames and extract strengths
        beat_frames = librosa.time_to_frames(beat_times, sr=sr, hop_length=self.hop_length)
        beat_strengths = []

        for frame in beat_frames:
            if frame < len(combined_strength):
                beat_strengths.append(combined_strength[frame])
            else:
                beat_strengths.append(0.0)

        beat_strengths = np.array(beat_strengths)

        if len(beat_strengths) == 0:
            return np.array([])

        # Adaptive thresholding: use local maxima approach
        beats_per_measure = time_signature[0]
        downbeat_indices = []

        # First, identify local maxima within measure-sized windows
        for i in range(0, len(beat_strengths), beats_per_measure):
            window_end = min(i + beats_per_measure, len(beat_strengths))
            window = beat_strengths[i:window_end]

            if len(window) > 0:
                local_max_idx = i + np.argmax(window)
                downbeat_indices.append(local_max_idx)

        # Refine using adaptive threshold
        if len(downbeat_indices) > 0:
            downbeat_strengths = beat_strengths[downbeat_indices]
            # Use median + 0.5 * std as threshold
            threshold = np.median(downbeat_strengths) + 0.5 * np.std(downbeat_strengths)
            downbeat_indices = [
                idx
                for idx in downbeat_indices
                if beat_strengths[idx] >= threshold
            ]

        if len(downbeat_indices) > 0:
            downbeat_times = beat_times[downbeat_indices]
        else:
            # Fallback to regular spacing
            downbeat_times = beat_times[::beats_per_measure] if len(beat_times) >= beats_per_measure else beat_times

        return downbeat_times

    def _detect_phrase_boundaries(self, y: np.ndarray, sr: int) -> np.ndarray:
        """
        Detect musical phrase boundaries using spectral clustering.

        Returns:
            Array of times (in seconds) where phrase boundaries occur
        """
        # Compute chroma features for harmonic analysis
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=self.hop_length)

        # Use spectral clustering to find segment boundaries
        # Using recurrence matrix approach
        R = librosa.segment.recurrence_matrix(
            chroma, mode='affinity', metric='cosine', width=9
        )

        # Apply lag matrix for sequence information
        R_lag = librosa.segment.recurrence_to_lag(R, pad=False)

        # Detect boundaries using novelty curve
        novelty = np.sum(np.abs(np.diff(R_lag, axis=1)), axis=0)
        novelty = np.concatenate([[0], novelty])

        # Find peaks in novelty curve
        peaks, _ = signal.find_peaks(
            novelty,
            height=np.percentile(novelty, 75),
            distance=int(4 * sr / self.hop_length),  # Min 4 seconds between boundaries
        )

        # Convert frames to times
        boundary_times = librosa.frames_to_time(peaks, sr=sr, hop_length=self.hop_length)

        return boundary_times

    def _compute_energy_profile(self, y: np.ndarray, sr: int) -> np.ndarray:
        """
        Compute enhanced energy profile with adaptive normalization.

        Uses RMS energy with local percentile-based normalization.
        """
        rms = librosa.feature.rms(y=y, hop_length=self.hop_length)[0]

        # Apply adaptive normalization using local percentiles
        window_size = int(4 * sr / self.hop_length)  # 4-second window
        rms_normalized = np.zeros_like(rms)

        for i in range(len(rms)):
            start = max(0, i - window_size // 2)
            end = min(len(rms), i + window_size // 2)
            window = rms[start:end]

            if len(window) > 0:
                p10 = np.percentile(window, 10)
                p90 = np.percentile(window, 90)
                rms_normalized[i] = (rms[i] - p10) / (p90 - p10 + 1e-6)

        # Clip to [0, 1] range
        rms_normalized = np.clip(rms_normalized, 0, 1)

        return rms_normalized

    def _compute_spectral_profile(self, y: np.ndarray, sr: int) -> np.ndarray:
        """Compute spectral centroid profile (brightness over time)."""
        spectral_centroids = librosa.feature.spectral_centroid(
            y=y, sr=sr, hop_length=self.hop_length
        )[0]

        # Normalize to 0-1
        sc_normalized = (spectral_centroids - spectral_centroids.min()) / (
            spectral_centroids.max() - spectral_centroids.min() + 1e-6
        )

        return sc_normalized

    def _compute_onset_density(self, y: np.ndarray, sr: int) -> np.ndarray:
        """
        Compute onset event density over time.

        Returns:
            Array of onset density values (events per second) over time
        """
        onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=self.hop_length)
        onset_frames = librosa.onset.onset_detect(
            onset_envelope=onset_env, sr=sr, hop_length=self.hop_length
        )

        # Compute density in sliding windows
        window_size = int(2 * sr / self.hop_length)  # 2-second window
        density = np.zeros(len(onset_env))

        for i in range(len(onset_env)):
            start = max(0, i - window_size // 2)
            end = min(len(onset_env), i + window_size // 2)

            # Count onsets in window
            onsets_in_window = np.sum((onset_frames >= start) & (onset_frames < end))
            density[i] = onsets_in_window / (window_size * self.hop_length / sr)

        # Normalize
        density_normalized = (density - density.min()) / (density.max() - density.min() + 1e-6)

        return density_normalized

    def _score_cut_point(
        self,
        beat_time: float,
        beat_index: int,
        beat_info: BeatInfo,
        is_downbeat: bool,
        prefer_downbeats: bool,
    ) -> float:
        """
        Compute comprehensive score for a potential cut point.

        Considers: downbeat status, phrase boundaries, energy, spectral features,
        onset density, and harmonic/percussive balance.
        """
        score = 0.5  # Base score

        # Downbeat bonus
        if is_downbeat and prefer_downbeats:
            score += 0.3

        # Phrase boundary bonus (strong preference)
        is_phrase_boundary = np.any(np.abs(beat_info.phrase_boundaries - beat_time) < 0.1)
        if is_phrase_boundary:
            score += 0.4

        # Energy contribution
        energy_idx = int(beat_time / beat_info.duration * len(beat_info.energy_profile))
        energy_idx = max(0, min(energy_idx, len(beat_info.energy_profile) - 1))
        energy = beat_info.energy_profile[energy_idx]
        score += 0.15 * energy

        # Spectral profile contribution (prefer brighter moments)
        spectral_idx = int(beat_time / beat_info.duration * len(beat_info.spectral_profile))
        spectral_idx = max(0, min(spectral_idx, len(beat_info.spectral_profile) - 1))
        spectral = beat_info.spectral_profile[spectral_idx]
        score += 0.1 * spectral

        # Onset density contribution
        onset_idx = int(beat_time / beat_info.duration * len(beat_info.onset_density))
        onset_idx = max(0, min(onset_idx, len(beat_info.onset_density) - 1))
        onset_d = beat_info.onset_density[onset_idx]
        score += 0.1 * onset_d

        # Percussive vs harmonic balance (prefer percussive hits)
        perc_idx = int(beat_time / beat_info.duration * len(beat_info.percussive_energy))
        perc_idx = max(0, min(perc_idx, len(beat_info.percussive_energy) - 1))
        perc_energy = beat_info.percussive_energy[perc_idx]
        score += 0.15 * perc_energy

        return min(score, 1.0)

    def get_cut_points(
        self,
        beat_info: BeatInfo,
        target_duration: float,
        min_clip_length: float = 1.5,
        max_clip_length: float = 4.0,
        prefer_downbeats: bool = True,
        downbeat_only: bool = False,
    ) -> list[CutPoint]:
        """
        Generate suggested cut points using dynamic programming for global optimization.

        Args:
            beat_info: BeatInfo from analyze()
            target_duration: Target video duration in seconds
            min_clip_length: Minimum time between cuts
            max_clip_length: Maximum time between cuts
            prefer_downbeats: Weight downbeats more heavily
            downbeat_only: Only use downbeats as candidates (less frenetic, better for drone)

        Returns:
            List of CutPoint objects with suggested edit times
        """
        # Build list of all potential cut points with scores
        max_duration = min(target_duration, beat_info.duration)
        candidates = []

        # Always include time 0
        candidates.append(
            {
                "time": 0.0,
                "index": -1,
                "score": 1.0,
                "is_downbeat": True,
                "is_phrase_boundary": True,
            }
        )

        # Add all beat times as candidates
        for i, beat_time in enumerate(beat_info.beat_times):
            if beat_time > max_duration:
                break

            is_downbeat = np.any(np.abs(beat_info.downbeat_times - beat_time) < 0.05)
            is_phrase_boundary = np.any(
                np.abs(beat_info.phrase_boundaries - beat_time) < 0.1
            )

            # In downbeat-only mode, skip non-downbeat candidates
            if downbeat_only and not is_downbeat:
                continue

            score = self._score_cut_point(
                beat_time, i, beat_info, is_downbeat, prefer_downbeats
            )

            candidates.append(
                {
                    "time": beat_time,
                    "index": i,
                    "score": score,
                    "is_downbeat": is_downbeat,
                    "is_phrase_boundary": is_phrase_boundary,
                }
            )

        # Fallback: if no beats detected, generate uniform cut points
        if len(candidates) <= 1:
            warnings.warn(
                "No beats detected in audio. Using uniform cut points as fallback.",
                stacklevel=2,
            )
            avg_clip = (min_clip_length + max_clip_length) / 2
            num_cuts = max(1, int(max_duration / avg_clip))
            interval = max_duration / num_cuts
            cut_points = []
            for i in range(num_cuts):
                t = i * interval
                cut_points.append(
                    CutPoint(
                        time=t,
                        strength=0.5,
                        is_downbeat=False,
                        beat_index=i,
                        is_phrase_boundary=False,
                        transition_rec=TransitionRecommendation(
                            intensity=0.5,
                            transition_type="crossfade",
                            duration=0.3,
                            energy_gradient="stable",
                        ),
                    )
                )
            return cut_points

        # Dynamic programming to find optimal sequence
        n = len(candidates)
        dp = [{"score": -float("inf"), "prev": -1} for _ in range(n)]
        dp[0] = {"score": 0.0, "prev": -1}

        for i in range(1, n):
            current_time = candidates[i]["time"]

            for j in range(i):
                prev_time = candidates[j]["time"]
                clip_duration = current_time - prev_time

                # Check if this transition is valid
                if clip_duration < min_clip_length:
                    continue
                if clip_duration > max_clip_length:
                    # No point checking earlier candidates
                    break

                # Score includes previous path score + current candidate score
                # Add bonus for good clip duration (prefer closer to middle of range)
                duration_score = 1.0 - abs(
                    clip_duration - (min_clip_length + max_clip_length) / 2
                ) / (max_clip_length - min_clip_length)

                transition_score = (
                    dp[j]["score"]
                    + candidates[i]["score"]
                    + 0.1 * duration_score
                )

                if transition_score > dp[i]["score"]:
                    dp[i]["score"] = transition_score
                    dp[i]["prev"] = j

        # Find best endpoint
        best_endpoint = -1
        best_score = -float("inf")

        for i in range(n):
            if (
                candidates[i]["time"] >= target_duration - max_clip_length
                and dp[i]["score"] > best_score
            ):
                best_score = dp[i]["score"]
                best_endpoint = i

        if best_endpoint == -1:
            # Fallback: use last valid candidate
            best_endpoint = n - 1

        # Backtrack to build cut point list
        cut_indices = []
        current = best_endpoint

        while current != -1:
            cut_indices.append(current)
            current = dp[current]["prev"]

        cut_indices.reverse()

        # Build CutPoint objects with transition recommendations
        cut_points = []
        for idx in cut_indices:
            cand = candidates[idx]
            transition_rec = self._compute_transition_recommendation(beat_info, cand["time"])

            cut_point = CutPoint(
                time=cand["time"],
                strength=cand["score"],
                is_downbeat=cand["is_downbeat"],
                beat_index=max(0, cand["index"]),
                is_phrase_boundary=cand["is_phrase_boundary"],
                transition_rec=transition_rec,
            )
            cut_points.append(cut_point)

        return cut_points

    def _compute_transition_recommendation(
        self, beat_info: BeatInfo, time: float
    ) -> TransitionRecommendation:
        """
        Compute detailed transition recommendation for a cut point.

        Args:
            beat_info: Beat information
            time: Time of the cut point

        Returns:
            TransitionRecommendation with intensity, type, duration, and gradient
        """
        # Get energy at cut point and surrounding context
        idx = int(time / beat_info.duration * len(beat_info.energy_profile))
        idx = max(0, min(idx, len(beat_info.energy_profile) - 1))

        energy = beat_info.energy_profile[idx]

        # Calculate energy gradient
        window = 10  # frames
        start_idx = max(0, idx - window)
        end_idx = min(len(beat_info.energy_profile), idx + window)

        if start_idx < end_idx:
            pre_energy = np.mean(beat_info.energy_profile[start_idx:idx]) if idx > start_idx else energy
            post_energy = np.mean(beat_info.energy_profile[idx:end_idx]) if end_idx > idx else energy

            gradient = post_energy - pre_energy

            if gradient > 0.1:
                energy_gradient = "rising"
            elif gradient < -0.1:
                energy_gradient = "falling"
            else:
                energy_gradient = "stable"
        else:
            energy_gradient = "stable"
            gradient = 0.0

        # Get percussive energy
        perc_idx = int(time / beat_info.duration * len(beat_info.percussive_energy))
        perc_idx = max(0, min(perc_idx, len(beat_info.percussive_energy) - 1))
        perc_energy = beat_info.percussive_energy[perc_idx]

        # Get onset density
        onset_idx = int(time / beat_info.duration * len(beat_info.onset_density))
        onset_idx = max(0, min(onset_idx, len(beat_info.onset_density) - 1))
        onset_d = beat_info.onset_density[onset_idx]

        # Compute continuous intensity (0-1)
        intensity = 0.4 * energy + 0.3 * perc_energy + 0.2 * onset_d + 0.1 * abs(gradient)
        intensity = min(1.0, intensity)

        # Determine transition type
        if intensity > 0.75 and perc_energy > 0.7:
            transition_type = "impact"  # Hard cut with impact effect
            duration = 0.1
        elif intensity > 0.6:
            transition_type = "cut"  # Direct cut
            duration = 0.0
        elif intensity > 0.3:
            transition_type = "crossfade"  # Smooth crossfade
            duration = 0.3
        else:
            transition_type = "fade"  # Gentle fade
            duration = 0.5

        return TransitionRecommendation(
            intensity=intensity,
            transition_type=transition_type,
            duration=duration,
            energy_gradient=energy_gradient,
        )

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

        Maintained for backward compatibility. Use cut_point.transition_rec for
        more detailed recommendations.

        Returns:
            'hard' for strong beats, 'medium' for regular beats, 'soft' for weak points
        """
        # Use the new transition recommendation if available
        if cut_point.transition_rec is not None:
            intensity = cut_point.transition_rec.intensity
            if intensity > 0.7:
                return "hard"
            elif intensity > 0.4:
                return "medium"
            else:
                return "soft"

        # Fallback to original implementation
        energy = self.get_energy_at_time(beat_info, cut_point.time)

        if cut_point.is_downbeat and energy > 0.7:
            return "hard"
        elif cut_point.strength > 0.8 or energy > 0.6:
            return "medium"
        else:
            return "soft"
