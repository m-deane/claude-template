"""
Speed ramping system for variable-speed video effects.

Provides smooth speed transitions using cubic bezier interpolation
for professional-looking time remapping effects.
"""

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np
from moviepy import VideoFileClip

from drone_reel.core.beat_sync import BeatInfo
from drone_reel.core.scene_detector import MotionType, SceneInfo
from drone_reel.core.video_processor import ClipSegment


@dataclass
class SpeedRamp:
    """Definition of a speed ramp effect."""

    start_time: float
    end_time: float
    start_speed: float
    end_speed: float
    easing: str = "linear"

    def __post_init__(self):
        """Validate speed ramp parameters."""
        if self.start_time < 0:
            raise ValueError("start_time must be non-negative")
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be greater than start_time")
        if self.start_speed <= 0:
            raise ValueError("start_speed must be positive")
        if self.end_speed <= 0:
            raise ValueError("end_speed must be positive")
        if self.easing not in {"linear", "ease_in", "ease_out", "ease_in_out"}:
            raise ValueError(
                f"easing must be one of: linear, ease_in, ease_out, ease_in_out (got {self.easing})"
            )

    @property
    def duration(self) -> float:
        """Duration of the ramp in source time."""
        return self.end_time - self.start_time


class SpeedRamper:
    """
    Applies variable speed effects to video clips.

    Supports smooth speed transitions using cubic bezier easing functions
    for professional time remapping effects.
    """

    def __init__(self):
        """Initialize the speed ramper."""
        self._easing_functions: dict[str, Callable[[float], float]] = {
            "linear": self._ease_linear,
            "ease_in": self._ease_in,
            "ease_out": self._ease_out,
            "ease_in_out": self._ease_in_out,
        }

    def _ease_linear(self, t: float) -> float:
        """Linear interpolation (no easing)."""
        return t

    def _ease_in(self, t: float) -> float:
        """Cubic ease-in (slow start)."""
        return t * t * t

    def _ease_out(self, t: float) -> float:
        """Cubic ease-out (slow end)."""
        return 1 - (1 - t) ** 3

    def _ease_in_out(self, t: float) -> float:
        """Cubic ease-in-out (slow start and end)."""
        if t < 0.5:
            return 4 * t * t * t
        else:
            return 1 - (-2 * t + 2) ** 3 / 2

    def _interpolate_speed(self, ramp: SpeedRamp, time: float) -> float:
        """
        Calculate speed multiplier at a given time within a ramp.

        Args:
            ramp: SpeedRamp definition
            time: Time within the clip

        Returns:
            Speed multiplier at that time
        """
        if time < ramp.start_time:
            return ramp.start_speed
        elif time > ramp.end_time:
            return ramp.end_speed

        # Normalize time to 0-1 range within the ramp
        t = (time - ramp.start_time) / ramp.duration

        # Apply easing function
        easing_func = self._easing_functions[ramp.easing]
        eased_t = easing_func(t)

        # Interpolate speed
        speed = ramp.start_speed + (ramp.end_speed - ramp.start_speed) * eased_t
        return speed

    def _create_time_mapping(
        self, clip_duration: float, ramps: list[SpeedRamp]
    ) -> Callable[[float], float]:
        """
        Create a time mapping function for multiple speed ramps.

        Args:
            clip_duration: Total duration of the source clip
            ramps: List of SpeedRamp objects (must be non-overlapping and sorted)

        Returns:
            Function that maps output time to source time
        """
        # Sort ramps by start time
        sorted_ramps = sorted(ramps, key=lambda r: r.start_time)

        # Validate non-overlapping ramps
        for i in range(len(sorted_ramps) - 1):
            if sorted_ramps[i].end_time > sorted_ramps[i + 1].start_time:
                raise ValueError(
                    f"Overlapping ramps detected: ramp ending at {sorted_ramps[i].end_time} "
                    f"overlaps with ramp starting at {sorted_ramps[i + 1].start_time}"
                )

        # Build segments with their speeds
        segments = []
        current_time = 0.0

        for ramp in sorted_ramps:
            # Add constant-speed segment before ramp if needed
            if ramp.start_time > current_time:
                segments.append(
                    {
                        "start": current_time,
                        "end": ramp.start_time,
                        "speed": ramp.start_speed,
                        "type": "constant",
                    }
                )

            # Add the ramp segment
            segments.append(
                {
                    "start": ramp.start_time,
                    "end": ramp.end_time,
                    "speed": None,
                    "type": "ramp",
                    "ramp": ramp,
                }
            )
            current_time = ramp.end_time

        # Add final constant-speed segment if needed
        if current_time < clip_duration:
            final_speed = sorted_ramps[-1].end_speed if sorted_ramps else 1.0
            segments.append(
                {
                    "start": current_time,
                    "end": clip_duration,
                    "speed": final_speed,
                    "type": "constant",
                }
            )

        # Pre-compute cumulative output durations for each segment
        cumulative_output_time = 0.0
        for seg in segments:
            seg["output_start"] = cumulative_output_time

            if seg["type"] == "constant":
                seg_duration = seg["end"] - seg["start"]
                output_duration = seg_duration / seg["speed"]
                seg["output_end"] = cumulative_output_time + output_duration
                cumulative_output_time += output_duration
            else:
                # For ramp segments, numerically integrate to find output duration
                ramp = seg["ramp"]
                dt = 0.01  # Integration step
                output_duration = 0.0
                t = ramp.start_time

                while t < ramp.end_time:
                    speed = self._interpolate_speed(ramp, t)
                    output_duration += dt / speed
                    t += dt

                seg["output_end"] = cumulative_output_time + output_duration
                cumulative_output_time += output_duration

        def time_mapping(output_time: float) -> float:
            """Map output time to source time."""
            # Find which segment we're in
            for seg in segments:
                if seg["output_start"] <= output_time <= seg["output_end"]:
                    if seg["type"] == "constant":
                        # Simple linear mapping for constant speed
                        output_offset = output_time - seg["output_start"]
                        source_offset = output_offset * seg["speed"]
                        return seg["start"] + source_offset
                    else:
                        # Numerical inversion for ramp segments
                        ramp = seg["ramp"]
                        output_offset = output_time - seg["output_start"]

                        # Binary search for source time
                        left, right = ramp.start_time, ramp.end_time
                        tolerance = 0.001

                        while right - left > tolerance:
                            mid = (left + right) / 2

                            # Integrate from ramp start to mid
                            t = ramp.start_time
                            dt = 0.01
                            integrated = 0.0

                            while t < mid:
                                speed = self._interpolate_speed(ramp, t)
                                integrated += dt / speed
                                t += dt

                            if integrated < output_offset:
                                left = mid
                            else:
                                right = mid

                        return (left + right) / 2

            # If beyond all segments, return clip duration
            return clip_duration

        return time_mapping

    def apply_ramp(self, clip: VideoFileClip, ramp: SpeedRamp) -> VideoFileClip:
        """
        Apply a speed ramp to a video clip.

        Args:
            clip: Source VideoFileClip
            ramp: SpeedRamp to apply

        Returns:
            Modified VideoFileClip with speed ramp applied
        """
        time_mapping = self._create_time_mapping(clip.duration, [ramp])

        # Calculate new duration
        new_duration = 0.0
        dt = 0.01
        t = 0.0

        while t < clip.duration:
            if ramp.start_time <= t <= ramp.end_time:
                speed = self._interpolate_speed(ramp, t)
                new_duration += dt / speed
            elif t < ramp.start_time:
                new_duration += dt / ramp.start_speed
            else:
                new_duration += dt / ramp.end_speed
            t += dt

        ramped_clip = clip.time_transform(time_mapping)
        ramped_clip = ramped_clip.with_duration(new_duration)

        return ramped_clip

    def apply_multiple_ramps(self, clip: VideoFileClip, ramps: list[SpeedRamp]) -> VideoFileClip:
        """
        Apply multiple speed ramps to a video clip.

        Args:
            clip: Source VideoFileClip
            ramps: List of SpeedRamp objects (must be non-overlapping)

        Returns:
            Modified VideoFileClip with all speed ramps applied
        """
        if not ramps:
            return clip

        time_mapping = self._create_time_mapping(clip.duration, ramps)

        # Calculate new duration by integrating 1/speed over all segments
        sorted_ramps = sorted(ramps, key=lambda r: r.start_time)
        new_duration = 0.0
        dt = 0.01
        t = 0.0

        while t < clip.duration:
            # Find current speed
            current_speed = 1.0

            for ramp in sorted_ramps:
                if ramp.start_time <= t <= ramp.end_time:
                    current_speed = self._interpolate_speed(ramp, t)
                    break
                elif t < ramp.start_time:
                    current_speed = ramp.start_speed if sorted_ramps[0] == ramp else 1.0
                    break
            else:
                # After all ramps
                if sorted_ramps:
                    current_speed = sorted_ramps[-1].end_speed

            new_duration += dt / current_speed
            t += dt

        ramped_clip = clip.time_transform(time_mapping)
        ramped_clip = ramped_clip.with_duration(new_duration)

        return ramped_clip

    def auto_detect_ramp_points(
        self,
        scene: SceneInfo,
        beat_info: BeatInfo | None = None,
        motion_threshold: float = 0.7,
    ) -> list[SpeedRamp]:
        """
        Automatically detect moments suitable for speed ramping.

        Analyzes:
        - Motion patterns (smooth motion = slow-mo candidate)
        - Beat drops from beat_sync (speed up or slow down on drops)
        - Scene reveals (low to high complexity)

        Args:
            scene: SceneInfo for the scene to analyze
            beat_info: Optional BeatInfo for music synchronization
            motion_threshold: Threshold for detecting smooth motion (0-1)

        Returns:
            List of recommended SpeedRamp objects
        """
        ramps = []

        # Strategy 1: Slow motion for smooth, scenic moments
        # Typically at the beginning or middle of scenes
        if scene.duration >= 3.0 and scene.score > 60:
            # Add a slow-motion ramp at the start
            ramps.append(
                SpeedRamp(
                    start_time=0.0,
                    end_time=min(1.5, scene.duration * 0.3),
                    start_speed=1.0,
                    end_speed=0.5,
                    easing="ease_in",
                )
            )

            # Return to normal speed
            if scene.duration >= 4.0:
                ramps.append(
                    SpeedRamp(
                        start_time=scene.duration * 0.6,
                        end_time=scene.duration * 0.8,
                        start_speed=0.5,
                        end_speed=1.0,
                        easing="ease_out",
                    )
                )

        # Strategy 2: Beat-synchronized speed changes
        if beat_info is not None:
            beat_ramps = self.create_beat_synced_ramps(
                clip_duration=scene.duration,
                beat_times=beat_info.beat_times,
                drop_times=beat_info.downbeat_times,
            )
            # Merge with existing ramps (avoiding overlaps)
            for beat_ramp in beat_ramps:
                # Check for overlaps
                overlaps = any(
                    not (beat_ramp.end_time <= r.start_time or beat_ramp.start_time >= r.end_time)
                    for r in ramps
                )
                if not overlaps:
                    ramps.append(beat_ramp)

        return ramps

    def create_beat_synced_ramps(
        self,
        clip_duration: float,
        beat_times: np.ndarray,
        drop_times: np.ndarray,
    ) -> list[SpeedRamp]:
        """
        Create speed ramps synchronized to music beats and drops.

        Args:
            clip_duration: Duration of the clip
            beat_times: Array of beat times in seconds
            drop_times: Array of beat drop/downbeat times in seconds

        Returns:
            List of SpeedRamp objects synced to music
        """
        ramps = []

        # Filter beat times within clip duration
        valid_drops = drop_times[drop_times < clip_duration]

        # Strategy: Slow down before drops, speed up after
        for drop_time in valid_drops:
            if drop_time < 1.0 or drop_time > clip_duration - 1.0:
                continue  # Skip drops too close to edges

            # Slow down before the drop (build anticipation)
            pre_drop_start = max(0, drop_time - 0.8)
            pre_drop_end = drop_time - 0.1

            if pre_drop_end > pre_drop_start:
                ramps.append(
                    SpeedRamp(
                        start_time=pre_drop_start,
                        end_time=pre_drop_end,
                        start_speed=1.0,
                        end_speed=0.6,
                        easing="ease_in",
                    )
                )

            # Speed up on the drop (impact)
            post_drop_start = drop_time
            post_drop_end = min(clip_duration, drop_time + 0.5)

            if post_drop_end > post_drop_start:
                ramps.append(
                    SpeedRamp(
                        start_time=post_drop_start,
                        end_time=post_drop_end,
                        start_speed=0.6,
                        end_speed=1.2,
                        easing="ease_out",
                    )
                )

                # Return to normal speed
                return_start = post_drop_end
                return_end = min(clip_duration, return_start + 0.4)

                if return_end > return_start:
                    ramps.append(
                        SpeedRamp(
                            start_time=return_start,
                            end_time=return_end,
                            start_speed=1.2,
                            end_speed=1.0,
                            easing="ease_in_out",
                        )
                    )

        return ramps

    def apply_ramp_to_segment(self, segment: ClipSegment, ramp: SpeedRamp) -> ClipSegment:
        """
        Apply speed ramp information to a ClipSegment.

        Note: This doesn't modify the actual video, just stores the ramp
        info for later application during video processing.

        Args:
            segment: ClipSegment to modify
            ramp: SpeedRamp to apply

        Returns:
            Modified ClipSegment with ramp information
        """
        # Store ramp as a custom attribute
        # This would require extending ClipSegment class
        # For now, return the segment as-is
        # In production, you'd extend ClipSegment to store ramps
        return segment

    def calculate_ramped_duration(self, original_duration: float, ramps: list[SpeedRamp]) -> float:
        """
        Calculate the resulting duration after applying speed ramps.

        Args:
            original_duration: Original clip duration
            ramps: List of SpeedRamp objects

        Returns:
            New duration after speed ramping
        """
        if not ramps:
            return original_duration

        sorted_ramps = sorted(ramps, key=lambda r: r.start_time)
        new_duration = 0.0
        dt = 0.01
        t = 0.0

        while t < original_duration:
            current_speed = 1.0

            for ramp in sorted_ramps:
                if ramp.start_time <= t <= ramp.end_time:
                    current_speed = self._interpolate_speed(ramp, t)
                    break
                elif t < ramp.start_time:
                    current_speed = ramp.start_speed if sorted_ramps[0] == ramp else 1.0
                    break
            else:
                if sorted_ramps:
                    current_speed = sorted_ramps[-1].end_speed

            new_duration += dt / current_speed
            t += dt

        return new_duration


_SPEED_CORRECTION_PROFILES: dict[str, dict[str, float]] = {
    "normal": {
        "pan_high": 0.65,
        "pan_mid": 0.80,
        "tilt_high": 0.70,
        "fpv": 0.75,
        "flyover": 0.70,
    },
    "aggressive": {
        "pan_high": 0.55,
        "pan_mid": 0.70,
        "tilt_high": 0.60,
        "fpv": 0.65,
        "flyover": 0.60,
    },
    "smooth": {
        "pan_high": 0.75,
        "pan_mid": 0.85,
        "tilt_high": 0.80,
        "fpv": 0.80,
        "flyover": 0.80,
    },
    "cinematic": {
        "pan_high": 0.60,
        "pan_mid": 0.75,
        "tilt_high": 0.65,
        "fpv": 0.70,
        "flyover": 0.65,
    },
}


def detect_gimbal_bounces(
    motion_data: list[dict],
    magnitude_threshold: float = 2.0,
    bounce_duration: float = 0.4,
) -> list[float]:
    """
    Detect sudden motion-reversal events in per-frame motion data.

    A bounce is defined as a sign flip in dx or dy accompanied by a combined
    magnitude exceeding ``magnitude_threshold``.

    Args:
        motion_data: List of per-frame dicts with keys "t" (timestamp), "dx", "dy".
        magnitude_threshold: Minimum combined |dx|+|dy| to count as a bounce.
        bounce_duration: Duration window (seconds) centred on each bounce event
            that will receive a speed ramp.  Not used in detection itself.

    Returns:
        List of timestamps (float seconds) at the centre of each bounce event.
    """
    bounces: list[float] = []
    if len(motion_data) < 2:
        return bounces

    prev = motion_data[0]
    for curr in motion_data[1:]:
        dx_flip = (prev["dx"] * curr["dx"] < 0) and (
            abs(curr["dx"]) + abs(prev["dx"]) >= magnitude_threshold
        )
        dy_flip = (prev["dy"] * curr["dy"] < 0) and (
            abs(curr["dy"]) + abs(prev["dy"]) >= magnitude_threshold
        )
        if dx_flip or dy_flip:
            bounces.append(float(curr["t"]))
        prev = curr

    return bounces


def auto_pan_speed_ramp(
    scene: SceneInfo,
    clip_duration: float,
    motion_energy: float | None = None,
    motion_type: MotionType | None = None,
    *,
    speed_correction_profile: str = "normal",
    pan_speed_high: float | None = None,
    pan_speed_mid: float | None = None,
    tilt_speed: float | None = None,
    fpv_speed: float | None = None,
    correct_orbit: bool = False,
    ease_speed_ramps: bool = False,
    vertical_drift_damping: float = 0.0,
    gimbal_bounce_recovery: bool = False,
    motion_data: list[dict] | None = None,
) -> list[SpeedRamp]:
    """
    Design a full-clip constant-speed ramp to correct panning speed issues.

    Slows down uncomfortably fast pans/tilts/FPV moves and gently speeds up
    sluggish pans so every clip plays at a cinematically comfortable pace.
    Returns a single full-clip SpeedRamp (or 3 segments when ease_speed_ramps=True),
    or an empty list when no adjustment is needed.

    Speed correction matrix (using "normal" profile defaults):
        PAN_LEFT / PAN_RIGHT:
            energy > 70  →  0.65× (too fast — strong slow-down)
            55 < energy ≤ 70  →  0.80× (fast — light slow-down)
            5 < energy < 20  →  1.25× (sluggish — gentle speed-up)
            otherwise  →  no change
        TILT_UP / TILT_DOWN:
            energy > 65  →  0.70×
        FLYOVER:
            energy > 70  →  0.70×
        APPROACH:
            energy > 70  →  0.70×
        FPV:
            energy > 50  →  0.75×
        ORBIT_CW / ORBIT_CCW:
            correct_orbit=True  →  0.85×
        STATIC, REVEAL, UNKNOWN  →  no change

    Args:
        scene: Scene whose motion_type / score may inform the decision.
        clip_duration: Duration of the clip in seconds.
        motion_energy: Optical-flow energy (0–100).  When None, falls back to
            ``scene.score`` as a rough proxy (not ideal, but safe).
        motion_type: Detected camera motion type.  When None the function
            inspects ``scene`` for a ``motion_type`` attribute; if still
            unavailable it returns an empty list.
        speed_correction_profile: Preset profile ("normal", "aggressive", "smooth",
            "cinematic") that sets all speed thresholds at once.
        pan_speed_high: Override speed factor for PAN with energy >70 (beats profile).
        pan_speed_mid: Override speed factor for PAN with energy 55-70 (beats profile).
        tilt_speed: Override speed factor for TILT with energy >65 (beats profile).
        fpv_speed: Override speed factor for FPV with energy >50 (beats profile).
        correct_orbit: When True, apply 0.85× correction to ORBIT motion types.
        ease_speed_ramps: When True, split the correction into 3 segments with a gentle
            linear ease in (first 15%) and ease out (final 15%) around the constant
            middle (70%), rather than a single hard constant-speed ramp.
        vertical_drift_damping: For TILT_DOWN clips, apply an additional proportional
            speed reduction on top of tilt correction (0.0–1.0 scale).
            new_speed = tilt_speed × (1 - vertical_drift_damping × 0.15).
        gimbal_bounce_recovery: When True, inject 0.95× speed ramps (0.4s) centred
            on detected motion-reversal events.  Requires ``motion_data`` to be provided.
            New ramps do not overlap existing ones — conflicts prefer existing ramps.
        motion_data: Optional list of per-frame dicts {"t": float, "dx": float, "dy": float}
            used for gimbal bounce detection when ``gimbal_bounce_recovery=True``.

    Returns:
        List with one or three SpeedRamp segments, or [] when no adjustment needed.
    """
    if clip_duration < 1.0:
        return []

    # Resolve motion_type: parameter → scene attribute → give up
    if motion_type is None:
        motion_type = getattr(scene, "motion_type", None)
    if motion_type is None:
        return []

    # Resolve motion_energy: parameter → scene attribute → scene.score proxy
    if motion_energy is None:
        motion_energy = getattr(scene, "motion_energy", None)
    if motion_energy is None:
        motion_energy = scene.score  # rough proxy

    # Resolve profile thresholds
    if speed_correction_profile not in _SPEED_CORRECTION_PROFILES:
        raise ValueError(
            f"speed_correction_profile must be one of "
            f"{list(_SPEED_CORRECTION_PROFILES.keys())}, got {speed_correction_profile!r}"
        )
    profile = _SPEED_CORRECTION_PROFILES[speed_correction_profile]

    # Merge individual overrides on top of profile
    effective_pan_high = pan_speed_high if pan_speed_high is not None else profile["pan_high"]
    effective_pan_mid = pan_speed_mid if pan_speed_mid is not None else profile["pan_mid"]
    effective_tilt = tilt_speed if tilt_speed is not None else profile["tilt_high"]
    effective_fpv = fpv_speed if fpv_speed is not None else profile["fpv"]
    effective_flyover = profile["flyover"]

    # Determine speed multiplier based on motion type + energy
    speed: float | None = None

    if motion_type in (MotionType.PAN_LEFT, MotionType.PAN_RIGHT):
        if motion_energy > 70:
            speed = effective_pan_high
        elif motion_energy > 55:
            speed = effective_pan_mid
        elif 5 < motion_energy < 20:
            speed = 1.25
    elif motion_type in (MotionType.TILT_UP, MotionType.TILT_DOWN):
        if motion_energy > 65:
            speed = effective_tilt
            if motion_type is MotionType.TILT_DOWN and vertical_drift_damping > 0.0:
                speed = speed * (1.0 - vertical_drift_damping * 0.15)
    elif motion_type is MotionType.FLYOVER:
        if motion_energy > 70:
            speed = effective_flyover
    elif motion_type is MotionType.APPROACH:
        if motion_energy > 70:
            speed = effective_flyover
    elif motion_type is MotionType.FPV:
        if motion_energy > 50:
            speed = effective_fpv
    elif motion_type in (MotionType.ORBIT_CW, MotionType.ORBIT_CCW):
        if correct_orbit:
            speed = 0.85
    # STATIC, REVEAL, UNKNOWN → no adjustment

    if speed is None:
        # No motion-based ramp, but may still inject bounce ramps below.
        base_ramps: list[SpeedRamp] = []
    elif not ease_speed_ramps:
        base_ramps = [
            SpeedRamp(
                start_time=0.0,
                end_time=clip_duration,
                start_speed=speed,
                end_speed=speed,
                easing="ease_in_out",
            )
        ]
    else:
        # ease_speed_ramps=True: split into 3 segments
        # First 15%: linear ramp 1.0 → target
        # Middle 70%: constant at target
        # Final 15%: linear ramp target → 1.0
        # For very short clips, ensure each segment has a minimum valid duration.
        ease_fraction = 0.15
        ease_in_end = max(clip_duration * ease_fraction, 0.01)
        main_end = max(clip_duration * (1.0 - ease_fraction), ease_in_end + 0.01)
        # Clamp to clip bounds
        ease_in_end = min(ease_in_end, clip_duration - 0.02)
        main_end = min(main_end, clip_duration - 0.01)

        base_ramps = [
            # Ease-in: ramp from 1.0 to target speed
            SpeedRamp(
                start_time=0.0,
                end_time=ease_in_end,
                start_speed=1.0,
                end_speed=speed,
                easing="linear",
            ),
            # Middle: constant at target speed
            SpeedRamp(
                start_time=ease_in_end,
                end_time=main_end,
                start_speed=speed,
                end_speed=speed,
                easing="linear",
            ),
            # Ease-out: ramp from target speed to 1.0
            SpeedRamp(
                start_time=main_end,
                end_time=clip_duration,
                start_speed=speed,
                end_speed=1.0,
                easing="linear",
            ),
        ]

    # Inject gimbal bounce recovery ramps (no overlap with existing ramps)
    if gimbal_bounce_recovery and motion_data:
        bounce_half = 0.2  # half of 0.4s bounce window
        bounce_speed = 0.95
        bounce_timestamps = detect_gimbal_bounces(motion_data)

        for ts in bounce_timestamps:
            b_start = max(0.0, ts - bounce_half)
            b_end = min(clip_duration, ts + bounce_half)
            if b_end - b_start < 0.05:
                continue  # too small to be useful

            # Check for overlap with existing ramps — skip if conflict
            overlap = any(not (b_end <= r.start_time or b_start >= r.end_time) for r in base_ramps)
            if overlap:
                continue

            base_ramps.append(
                SpeedRamp(
                    start_time=b_start,
                    end_time=b_end,
                    start_speed=bounce_speed,
                    end_speed=bounce_speed,
                    easing="ease_in_out",
                )
            )

    if not base_ramps:
        return []

    # Sort by start_time for deterministic ordering
    base_ramps.sort(key=lambda r: r.start_time)
    return base_ramps
