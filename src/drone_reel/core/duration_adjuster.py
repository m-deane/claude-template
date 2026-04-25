"""
Duration adjustment for drone video reels.

Adjusts clip durations based on sharpness, hook tier, motion type,
and target duration constraints.
"""

from dataclasses import dataclass

from drone_reel.core.scene_detector import (
    EnhancedSceneInfo,
    HookPotential,
    MotionType,
    SceneInfo,
)


@dataclass
class DurationConfig:
    """Configuration for duration adjustment."""

    min_clip_duration: float = 2.0
    sharp_threshold: float = 100.0
    soft_threshold: float = 30.0
    auto_scale_shortfall: float = 0.85  # Scale up if below this fraction of target
    auto_scale_max: float = 1.5  # Maximum auto-scale factor

    def max_clip_duration(self, target_duration: float) -> float:
        """Get max clip duration based on target reel length."""
        if target_duration <= 15:
            return 4.0
        elif target_duration <= 30:
            return 5.0
        return 6.0


class DurationAdjuster:
    """
    Adjust clip durations based on scene quality and target duration.

    Applies sharpness-based scaling, hook-tier adjustments, static scene caps,
    and auto-scaling to meet the target reel duration.
    """

    def __init__(self, config: DurationConfig | None = None):
        """
        Initialize duration adjuster.

        Args:
            config: Duration configuration. Uses defaults if None.
        """
        self.config = config or DurationConfig()

    def adjust_durations(
        self,
        scenes: list[SceneInfo],
        clip_durations: list[float],
        sharpness_map: dict[int, float],
        target_duration: float,
    ) -> tuple[list[float], float | None]:
        """
        Adjust clip durations based on scene quality.

        Args:
            scenes: Selected scenes
            clip_durations: Initial clip durations
            sharpness_map: Map of id(scene) -> sharpness value
            target_duration: Target reel duration in seconds

        Returns:
            Tuple of (adjusted_durations, scale_factor_applied_or_None)
        """
        c = self.config
        max_dur = c.max_clip_duration(target_duration)

        adjusted = []
        for scene, dur in zip(scenes, clip_durations):
            adjusted_dur = self._adjust_single(
                scene, dur, sharpness_map.get(id(scene), 100.0),
                target_duration, max_dur,
            )
            adjusted.append(adjusted_dur)

        # Auto-scale if significantly short of target
        actual = sum(adjusted)
        scale_factor = None
        if actual < target_duration * c.auto_scale_shortfall:
            scale_factor = min(target_duration / actual, c.auto_scale_max)
            adjusted = [min(d * scale_factor, max_dur) for d in adjusted]

        return adjusted, scale_factor

    def _adjust_single(
        self,
        scene: SceneInfo,
        base_duration: float,
        sharpness: float,
        target_duration: float,
        max_clip_duration: float,
    ) -> float:
        """
        Adjust a single clip's duration based on its characteristics.

        Args:
            scene: The scene
            base_duration: Initial duration
            sharpness: Scene sharpness value
            target_duration: Target reel duration
            max_clip_duration: Maximum allowed clip duration

        Returns:
            Adjusted duration
        """
        c = self.config
        adjusted = base_duration

        # Sharpness-based scaling
        if sharpness < c.soft_threshold:
            adjusted = c.min_clip_duration
        elif sharpness < c.sharp_threshold:
            scale = (sharpness - c.soft_threshold) / (c.sharp_threshold - c.soft_threshold)
            adjusted = c.min_clip_duration + (base_duration - c.min_clip_duration) * scale

        if isinstance(scene, EnhancedSceneInfo):
            # MAXIMUM/HIGH hook tier: ensure minimum showcase time
            if (scene.hook_tier in (HookPotential.MAXIMUM, HookPotential.HIGH)
                    and sharpness >= c.soft_threshold):
                adjusted = max(adjusted, 3.0)

            # LOW/POOR hook tier: cap duration for tight pacing
            elif scene.hook_tier in (HookPotential.LOW, HookPotential.POOR):
                max_weak = 2.0 if target_duration <= 15 else 3.0
                adjusted = min(adjusted, max_weak)

            # Static scenes: cap to avoid boring segments
            if scene.motion_type == MotionType.STATIC:
                max_static = 2.5 if target_duration <= 15 else 3.5
                adjusted = min(adjusted, max_static)

        # Enforce global limits
        adjusted = max(c.min_clip_duration, min(max_clip_duration, adjusted))

        return adjusted

    def compute_adaptive_durations(
        self,
        scenes: list[EnhancedSceneInfo],
        target_duration: float,
    ) -> list[float]:
        """
        Compute per-scene durations based on hook_tier, scaled to hit target_duration.

        Each scene receives a max duration based on its hook tier:
          - MAXIMUM/HIGH: 3.0-4.0s
          - MEDIUM:       2.0-3.0s
          - LOW:          1.5-2.5s
          - POOR:         1.5-2.0s

        Durations are then proportionally scaled so their sum approaches
        target_duration while respecting a minimum of 1.5s per clip.

        Args:
            scenes: Scenes with hook_tier attributes.
            target_duration: Desired total reel length in seconds.

        Returns:
            List of per-scene durations (same order as scenes).
        """
        MIN_CLIP = 1.5

        # Tier -> (min_dur, max_dur)
        _TIER_RANGES: dict[HookPotential, tuple[float, float]] = {
            HookPotential.MAXIMUM: (3.0, 4.0),
            HookPotential.HIGH:    (3.0, 4.0),
            HookPotential.MEDIUM:  (2.0, 3.0),
            HookPotential.LOW:     (1.5, 2.5),
            HookPotential.POOR:    (1.5, 2.0),
        }

        if not scenes:
            return []

        # Start each clip at its tier max
        raw: list[float] = []
        for scene in scenes:
            _, max_d = _TIER_RANGES.get(scene.hook_tier, (2.0, 3.0))
            raw.append(max_d)

        raw_total = sum(raw)
        if raw_total <= 0:
            return [MIN_CLIP] * len(scenes)

        # Scale proportionally to hit target_duration
        scale = target_duration / raw_total
        durations = [max(MIN_CLIP, d * scale) for d in raw]

        # Re-check total after MIN_CLIP clamping; if still off, apply a second pass
        clamped_total = sum(durations)
        if clamped_total > 0 and abs(clamped_total - target_duration) > 0.1:
            adjust = target_duration / clamped_total
            durations = [max(MIN_CLIP, d * adjust) for d in durations]

        return durations

    def scale_for_fewer_scenes(
        self,
        clip_durations: list[float],
        original_total: float,
        max_scale: float = 2.5,
    ) -> tuple[list[float], float]:
        """
        Scale up clip durations when fewer scenes are available than needed.

        Args:
            clip_durations: Current clip durations
            original_total: Original target total duration
            max_scale: Maximum scale factor

        Returns:
            Tuple of (scaled_durations, scale_factor)
        """
        current_total = sum(clip_durations)
        if current_total <= 0 or original_total <= current_total:
            return clip_durations, 1.0

        scale_factor = min(original_total / current_total, max_scale)
        scaled = [d * scale_factor for d in clip_durations]
        return scaled, scale_factor
