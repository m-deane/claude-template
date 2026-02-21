"""
Reframe mode selection for drone video reels.

Selects the appropriate reframe mode (CENTER, SMART, KEN_BURNS) for each
clip based on scene characteristics like motion type and subject score.
"""

from dataclasses import dataclass
from typing import Optional

from drone_reel.core.reframer import Reframer, ReframeSettings, AspectRatio, ReframeMode
from drone_reel.core.scene_detector import (
    EnhancedSceneInfo,
    MotionType,
    SceneInfo,
)


@dataclass
class KenBurnsConfig:
    """Ken Burns effect configuration."""

    zoom_end: float = 1.05
    pan_x: float = 0.05
    pan_y: float = 0.02


class ReframeSelector:
    """
    Select the appropriate reframe mode for each clip.

    Decision logic:
    1. High subject score with no camera movement -> SMART (gentle tracking)
    2. Camera already moving -> CENTER (stable crop)
    3. Landscape panorama with Ken Burns enabled -> KEN_BURNS
    4. Default -> CENTER
    """

    MOVING_MOTION_TYPES = (
        MotionType.PAN_LEFT, MotionType.PAN_RIGHT,
        MotionType.TILT_UP, MotionType.TILT_DOWN,
        MotionType.ORBIT_CW, MotionType.ORBIT_CCW,
        MotionType.FLYOVER, MotionType.REVEAL, MotionType.FPV,
    )

    def __init__(
        self,
        output_width: int = 1080,
        kb_config: Optional[KenBurnsConfig] = None,
        subject_threshold: float = 40.0,
    ):
        """
        Initialize reframe selector.

        Args:
            output_width: Target output width in pixels
            kb_config: Ken Burns configuration, or None to disable
            subject_threshold: Subject score threshold for SMART mode
        """
        self.output_width = output_width
        self.kb_config = kb_config
        self.subject_threshold = subject_threshold

    def select_reframers(
        self,
        scenes: list[SceneInfo],
        clip_durations: list[float],
    ) -> tuple[list[Reframer], list[str]]:
        """
        Select reframe mode and create Reframer instances for each clip.

        Args:
            scenes: Selected scenes
            clip_durations: Duration for each clip

        Returns:
            Tuple of (reframers, mode_names) where mode_names is list of
            "SMART", "CENTER", or "KEN_BURNS" strings
        """
        reframers = []
        mode_names = []

        for i, scene in enumerate(scenes):
            clip_duration = clip_durations[i] if i < len(clip_durations) else 3.0
            settings, mode_name = self._select_for_scene(scene, clip_duration)
            reframers.append(Reframer(settings))
            mode_names.append(mode_name)

        return reframers, mode_names

    def _select_for_scene(
        self,
        scene: SceneInfo,
        clip_duration: float,
    ) -> tuple[ReframeSettings, str]:
        """
        Select reframe settings for a single scene.

        Args:
            scene: Scene to create reframer for
            clip_duration: Duration of the clip

        Returns:
            Tuple of (ReframeSettings, mode_name)
        """
        motion_type = MotionType.STATIC
        subject_score = 0.0

        if isinstance(scene, EnhancedSceneInfo):
            motion_type = scene.motion_type
            subject_score = scene.subject_score

        has_active_subject = subject_score >= self.subject_threshold
        camera_moving = motion_type in self.MOVING_MOTION_TYPES
        duration_scale = min(clip_duration / 3.0, 1.5)

        if has_active_subject and not camera_moving:
            return self._smart_settings(duration_scale), "SMART"
        elif camera_moving:
            return self._center_settings(), "CENTER"
        elif self.kb_config:
            return self._ken_burns_settings(), "KEN_BURNS"
        else:
            return self._center_settings(), "CENTER"

    def _smart_settings(self, duration_scale: float) -> ReframeSettings:
        """Create SMART reframe settings for subject tracking."""
        smoothness = 0.003 * duration_scale
        return ReframeSettings(
            target_ratio=AspectRatio.VERTICAL_9_16,
            mode=ReframeMode.SMART,
            output_width=self.output_width,
            tracking_smoothness=smoothness,
            saliency_cache_frames=240,
            smooth_tracking=True,
            adaptive_smoothing=False,
            focal_clamp_x=(0.4, 0.6),
            focal_clamp_y=(0.4, 0.6),
        )

    def _center_settings(self) -> ReframeSettings:
        """Create CENTER reframe settings."""
        return ReframeSettings(
            target_ratio=AspectRatio.VERTICAL_9_16,
            mode=ReframeMode.CENTER,
            output_width=self.output_width,
        )

    def _ken_burns_settings(self) -> ReframeSettings:
        """Create KEN_BURNS reframe settings."""
        kb = self.kb_config
        return ReframeSettings(
            target_ratio=AspectRatio.VERTICAL_9_16,
            mode=ReframeMode.KEN_BURNS,
            output_width=self.output_width,
            ken_burns_zoom_start=1.0,
            ken_burns_zoom_end=kb.zoom_end,
            ken_burns_pan_direction=(kb.pan_x, kb.pan_y),
            ken_burns_ease_curve="ease_in_out",
        )
