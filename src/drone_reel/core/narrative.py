"""
Hook generation and narrative arc sequencing for viral drone reels.

Creates engaging opening sequences and arranges scenes according to
narrative patterns optimized for social media engagement.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional

import numpy as np

from drone_reel.core.beat_sync import BeatInfo
from drone_reel.core.scene_detector import SceneInfo
from drone_reel.core.video_processor import ClipSegment, TransitionType


class NarrativeArc(Enum):
    """Available narrative arc patterns."""

    CLASSIC = "classic"  # Hook → Build → Climax → Resolve
    BUILDING = "building"  # Energy increases throughout
    BOOKEND = "bookend"  # Strong open/close, varied middle
    MONTAGE = "montage"  # Rapid-fire variety
    CINEMATIC = "cinematic"  # Slow, atmospheric


class HookPattern(Enum):
    """Hook pattern types for video openings."""

    DRAMATIC_REVEAL = "dramatic_reveal"  # Low to high complexity
    QUICK_CUT_MONTAGE = "quick_cut_montage"  # 3-4 rapid cuts
    SPEED_RAMP_INTRO = "speed_ramp_intro"  # Fast to slow
    TEXT_REVEAL = "text_reveal"  # Text + dramatic reveal


@dataclass
class MotionCharacteristics:
    """Motion analysis results for a scene."""

    motion_type: str  # 'reveal', 'orbit', 'flyover', 'static', 'pan', 'tilt'
    motion_intensity: float  # 0-1
    complexity_score: float  # 0-1
    is_golden_hour: bool
    has_dramatic_subject: bool


class HookGenerator:
    """
    Generates engaging hook sequences for video openings.

    Analyzes scenes to identify and create compelling opening sequences
    that maximize viewer retention in the first 3 seconds.
    """

    def __init__(self, motion_weight: float = 0.4, composition_weight: float = 0.3):
        """
        Initialize hook generator.

        Args:
            motion_weight: Weight for motion in hook scoring
            composition_weight: Weight for composition in hook scoring
        """
        self.motion_weight = motion_weight
        self.composition_weight = composition_weight

    def select_hook_scene(
        self,
        scenes: list[SceneInfo],
        prefer_motion_types: list[str] = None,
    ) -> SceneInfo:
        """
        Select most hook-worthy scene for opening.

        Prioritizes reveals, maximum motion, unique angles, and golden hour lighting.

        Args:
            scenes: Available scenes to choose from
            prefer_motion_types: Preferred motion types (default: reveal, orbit, flyover)

        Returns:
            Best scene for hook

        Raises:
            ValueError: If no scenes provided
        """
        if not scenes:
            raise ValueError("No scenes provided for hook selection")

        if prefer_motion_types is None:
            prefer_motion_types = ["reveal", "orbit", "flyover"]

        hook_scores = []
        for scene in scenes:
            motion_chars = self._analyze_motion_characteristics(scene)
            score = self.score_hook_potential(scene)

            motion_type_bonus = 0.2 if motion_chars.motion_type in prefer_motion_types else 0.0
            golden_hour_bonus = 0.15 if motion_chars.is_golden_hour else 0.0
            dramatic_bonus = 0.1 if motion_chars.has_dramatic_subject else 0.0

            total_score = score + motion_type_bonus + golden_hour_bonus + dramatic_bonus
            hook_scores.append((total_score, scene))

        hook_scores.sort(key=lambda x: x[0], reverse=True)
        return hook_scores[0][1]

    def create_hook_sequence(
        self,
        scenes: list[SceneInfo],
        pattern: HookPattern,
        hook_duration: float = 3.0,
    ) -> list[ClipSegment]:
        """
        Create optimized hook sequence based on pattern.

        Args:
            scenes: Available scenes for hook
            pattern: Hook pattern to use
            hook_duration: Total duration for hook in seconds

        Returns:
            List of ClipSegments for hook sequence

        Raises:
            ValueError: If insufficient scenes for pattern
        """
        if pattern == HookPattern.DRAMATIC_REVEAL:
            return self._create_dramatic_reveal(scenes, hook_duration)
        elif pattern == HookPattern.QUICK_CUT_MONTAGE:
            return self._create_quick_cut_montage(scenes, hook_duration)
        elif pattern == HookPattern.SPEED_RAMP_INTRO:
            return self._create_speed_ramp_intro(scenes, hook_duration)
        elif pattern == HookPattern.TEXT_REVEAL:
            return self._create_text_reveal(scenes, hook_duration)
        else:
            raise ValueError(f"Unknown hook pattern: {pattern}")

    def score_hook_potential(self, scene: SceneInfo) -> float:
        """
        Score a scene's potential as a hook (0-100).

        Combines motion intensity, visual complexity, and composition quality.

        Args:
            scene: Scene to score

        Returns:
            Score from 0-100
        """
        motion_chars = self._analyze_motion_characteristics(scene)

        base_score = scene.score

        motion_bonus = motion_chars.motion_intensity * 20 * self.motion_weight
        complexity_bonus = motion_chars.complexity_score * 15 * self.composition_weight

        visual_variety_bonus = self._calculate_visual_variety(scene) * 10

        total_score = base_score + motion_bonus + complexity_bonus + visual_variety_bonus

        return min(total_score, 100.0)

    def _analyze_motion_characteristics(self, scene: SceneInfo) -> MotionCharacteristics:
        """
        Analyze motion characteristics of a scene.

        Uses scene scoring components to infer motion type and intensity.

        Args:
            scene: Scene to analyze

        Returns:
            MotionCharacteristics dataclass
        """
        motion_intensity = min(scene.score / 100.0, 1.0)

        if motion_intensity > 0.8:
            motion_type = "reveal"
            complexity_score = 0.9
        elif motion_intensity > 0.6:
            motion_type = "orbit"
            complexity_score = 0.7
        elif motion_intensity > 0.4:
            motion_type = "flyover"
            complexity_score = 0.6
        elif motion_intensity > 0.2:
            motion_type = "pan"
            complexity_score = 0.4
        else:
            motion_type = "static"
            complexity_score = 0.3

        is_golden_hour = self._detect_golden_hour(scene)
        has_dramatic_subject = motion_intensity > 0.65

        return MotionCharacteristics(
            motion_type=motion_type,
            motion_intensity=motion_intensity,
            complexity_score=complexity_score,
            is_golden_hour=is_golden_hour,
            has_dramatic_subject=has_dramatic_subject,
        )

    def _detect_golden_hour(self, scene: SceneInfo) -> bool:
        """
        Detect if scene was shot during golden hour.

        Uses heuristics based on scene score and duration.

        Args:
            scene: Scene to check

        Returns:
            True if likely golden hour
        """
        return scene.score > 75.0

    def _calculate_visual_variety(self, scene: SceneInfo) -> float:
        """
        Calculate visual variety score for a scene.

        Args:
            scene: Scene to analyze

        Returns:
            Variety score 0-1
        """
        variety = min(scene.duration / 5.0, 1.0)
        return variety * 0.8 + 0.2

    def _create_dramatic_reveal(
        self, scenes: list[SceneInfo], duration: float
    ) -> list[ClipSegment]:
        """Create dramatic reveal hook pattern."""
        if not scenes:
            raise ValueError("Need at least 1 scene for dramatic reveal")

        best_scene = self.select_hook_scene(scenes, ["reveal", "orbit"])

        segment = ClipSegment(
            scene=best_scene,
            start_offset=0.0,
            duration=duration,
            transition_in=TransitionType.FADE_BLACK,
            transition_out=TransitionType.CUT,
            transition_duration=0.5,
        )

        return [segment]

    def _create_quick_cut_montage(
        self, scenes: list[SceneInfo], duration: float
    ) -> list[ClipSegment]:
        """Create quick cut montage hook pattern."""
        if len(scenes) < 3:
            raise ValueError("Need at least 3 scenes for quick cut montage")

        top_scenes = sorted(scenes, key=lambda s: self.score_hook_potential(s), reverse=True)[
            :4
        ]

        clip_duration = duration / len(top_scenes)
        segments = []

        for i, scene in enumerate(top_scenes):
            transition_in = TransitionType.CUT if i > 0 else TransitionType.FADE_BLACK
            segment = ClipSegment(
                scene=scene,
                start_offset=0.0,
                duration=clip_duration,
                transition_in=transition_in,
                transition_out=TransitionType.CUT,
                transition_duration=0.15,
            )
            segments.append(segment)

        return segments

    def _create_speed_ramp_intro(
        self, scenes: list[SceneInfo], duration: float
    ) -> list[ClipSegment]:
        """Create speed ramp intro hook pattern."""
        if not scenes:
            raise ValueError("Need at least 1 scene for speed ramp intro")

        high_motion_scenes = [
            s for s in scenes if self._analyze_motion_characteristics(s).motion_intensity > 0.5
        ]

        if not high_motion_scenes:
            high_motion_scenes = scenes

        best_scene = max(high_motion_scenes, key=lambda s: self.score_hook_potential(s))

        segment = ClipSegment(
            scene=best_scene,
            start_offset=0.0,
            duration=duration,
            transition_in=TransitionType.FADE_BLACK,
            transition_out=TransitionType.CUT,
            transition_duration=0.3,
        )

        return [segment]

    def _create_text_reveal(
        self, scenes: list[SceneInfo], duration: float
    ) -> list[ClipSegment]:
        """Create text reveal hook pattern."""
        if not scenes:
            raise ValueError("Need at least 1 scene for text reveal")

        best_scene = self.select_hook_scene(scenes)

        segment = ClipSegment(
            scene=best_scene,
            start_offset=0.0,
            duration=duration,
            transition_in=TransitionType.FADE_BLACK,
            transition_out=TransitionType.CUT,
            transition_duration=0.6,
        )

        return [segment]


class NarrativeSequencer:
    """
    Sequences scenes into narrative arcs optimized for engagement.

    Arranges scenes according to energy curves and narrative patterns
    to maintain viewer interest throughout the video.
    """

    def __init__(self, arc_type: NarrativeArc = NarrativeArc.CLASSIC):
        """
        Initialize narrative sequencer.

        Args:
            arc_type: Narrative arc pattern to use
        """
        self.arc_type = arc_type

    def sequence(
        self,
        scenes: list[SceneInfo],
        target_duration: float = 30.0,
        hook_duration: float = 3.0,
        beat_info: Optional[BeatInfo] = None,
    ) -> list[SceneInfo]:
        """
        Arrange scenes into narrative arc.

        Classic arc (30s):
        - 0-3s: HOOK - Most dramatic moment
        - 3-12s: BUILD - Establishing shots, increasing energy
        - 12-24s: CLIMAX - Best scenes, peak energy
        - 24-30s: RESOLVE - Calm ending

        Args:
            scenes: Scenes to arrange
            target_duration: Target video duration
            hook_duration: Duration for hook section
            beat_info: Optional beat information for energy-aware sequencing

        Returns:
            Sequenced list of scenes

        Raises:
            ValueError: If insufficient scenes
        """
        if not scenes:
            raise ValueError("No scenes provided for sequencing")

        if len(scenes) < 3:
            return sorted(scenes, key=lambda s: s.score, reverse=True)

        arc_template = self._get_arc_template(self.arc_type, target_duration)

        sequenced = []
        available_scenes = scenes.copy()

        for start_pct, end_pct, energy_level in arc_template:
            section_start = start_pct * target_duration
            section_end = end_pct * target_duration
            section_duration = section_end - section_start

            if not available_scenes:
                break

            best_scene = self._select_scene_for_section(
                available_scenes, energy_level, section_duration, beat_info, section_start
            )

            sequenced.append(best_scene)
            available_scenes.remove(best_scene)

        return sequenced

    def calculate_energy_curve(self, scenes: list[SceneInfo]) -> list[float]:
        """
        Calculate energy score for each scene position.

        Args:
            scenes: Sequenced scenes

        Returns:
            List of energy scores (0-1) for each scene
        """
        energy_scores = []

        for i, scene in enumerate(scenes):
            position_pct = i / max(len(scenes) - 1, 1)

            arc_energy = self._get_energy_at_position(position_pct, self.arc_type)

            scene_energy = min(scene.score / 100.0, 1.0)

            combined_energy = 0.6 * arc_energy + 0.4 * scene_energy

            energy_scores.append(combined_energy)

        return energy_scores

    def _get_arc_template(
        self, arc_type: NarrativeArc, duration: float
    ) -> list[tuple[float, float, str]]:
        """
        Get (start_pct, end_pct, energy_level) template for arc.

        Args:
            arc_type: Type of narrative arc
            duration: Total duration

        Returns:
            List of tuples defining arc sections
        """
        if arc_type == NarrativeArc.CLASSIC:
            return [
                (0.0, 0.1, "peak"),  # Hook: 0-10%
                (0.1, 0.4, "rising"),  # Build: 10-40%
                (0.4, 0.8, "peak"),  # Climax: 40-80%
                (0.8, 1.0, "falling"),  # Resolve: 80-100%
            ]
        elif arc_type == NarrativeArc.BUILDING:
            return [
                (0.0, 0.15, "medium"),  # 0-15%
                (0.15, 0.4, "rising"),  # 15-40%
                (0.4, 0.7, "high"),  # 40-70%
                (0.7, 1.0, "peak"),  # 70-100%
            ]
        elif arc_type == NarrativeArc.BOOKEND:
            return [
                (0.0, 0.15, "peak"),  # Strong open: 0-15%
                (0.15, 0.4, "medium"),  # 15-40%
                (0.4, 0.7, "rising"),  # 40-70%
                (0.7, 0.85, "medium"),  # 70-85%
                (0.85, 1.0, "peak"),  # Strong close: 85-100%
            ]
        elif arc_type == NarrativeArc.MONTAGE:
            return [
                (0.0, 0.2, "high"),  # 0-20%
                (0.2, 0.4, "medium"),  # 20-40%
                (0.4, 0.6, "high"),  # 40-60%
                (0.6, 0.8, "medium"),  # 60-80%
                (0.8, 1.0, "high"),  # 80-100%
            ]
        elif arc_type == NarrativeArc.CINEMATIC:
            return [
                (0.0, 0.3, "low"),  # Slow build: 0-30%
                (0.3, 0.5, "medium"),  # 30-50%
                (0.5, 0.75, "rising"),  # 50-75%
                (0.75, 1.0, "low"),  # Atmospheric end: 75-100%
            ]
        else:
            return [(0.0, 1.0, "medium")]

    def _select_scene_for_section(
        self,
        available_scenes: list[SceneInfo],
        energy_level: str,
        section_duration: float,
        beat_info: Optional[BeatInfo],
        section_start: float,
    ) -> SceneInfo:
        """
        Select best scene for a narrative section.

        Args:
            available_scenes: Scenes to choose from
            energy_level: Required energy level (peak, high, rising, medium, falling, low)
            section_duration: Duration of section
            beat_info: Optional beat information
            section_start: Start time of section

        Returns:
            Best matching scene
        """
        energy_map = {
            "peak": (0.8, 1.0),
            "high": (0.7, 0.9),
            "rising": (0.5, 0.8),
            "medium": (0.4, 0.7),
            "falling": (0.3, 0.6),
            "low": (0.0, 0.5),
        }

        target_min, target_max = energy_map.get(energy_level, (0.4, 0.7))

        best_scene = None
        best_score = -1

        for scene in available_scenes:
            scene_energy = min(scene.score / 100.0, 1.0)

            energy_match = 1.0 - abs(scene_energy - (target_min + target_max) / 2)

            duration_match = 1.0 - abs(scene.duration - section_duration) / section_duration

            beat_match = 1.0
            if beat_info is not None:
                beat_energy = self._get_beat_energy_at_time(beat_info, section_start)
                beat_match = 1.0 - abs(scene_energy - beat_energy)

            total_score = 0.5 * energy_match + 0.3 * duration_match + 0.2 * beat_match

            if total_score > best_score:
                best_score = total_score
                best_scene = scene

        return best_scene if best_scene else available_scenes[0]

    def _get_energy_at_position(self, position_pct: float, arc_type: NarrativeArc) -> float:
        """
        Get energy level at position in arc.

        Args:
            position_pct: Position in arc (0-1)
            arc_type: Narrative arc type

        Returns:
            Energy level 0-1
        """
        if arc_type == NarrativeArc.CLASSIC:
            if position_pct < 0.1:
                return 0.9  # Hook
            elif position_pct < 0.4:
                return 0.3 + (position_pct - 0.1) / 0.3 * 0.4  # Rising
            elif position_pct < 0.8:
                return 0.85  # Peak climax
            else:
                return 0.85 - (position_pct - 0.8) / 0.2 * 0.45  # Falling

        elif arc_type == NarrativeArc.BUILDING:
            return min(0.4 + position_pct * 0.6, 1.0)

        elif arc_type == NarrativeArc.BOOKEND:
            if position_pct < 0.15:
                return 0.9
            elif position_pct < 0.85:
                return 0.5
            else:
                return 0.9

        elif arc_type == NarrativeArc.MONTAGE:
            return 0.6 + 0.3 * np.sin(position_pct * np.pi * 4)

        elif arc_type == NarrativeArc.CINEMATIC:
            if position_pct < 0.5:
                return 0.3 + position_pct * 0.4
            else:
                return 0.7 - (position_pct - 0.5) * 0.4

        return 0.5

    def _get_beat_energy_at_time(self, beat_info: BeatInfo, time: float) -> float:
        """
        Get beat energy at specific time.

        Args:
            beat_info: Beat information
            time: Time in seconds

        Returns:
            Energy level 0-1
        """
        if beat_info.duration == 0:
            return 0.5

        idx = int(time / beat_info.duration * len(beat_info.energy_profile))
        idx = max(0, min(idx, len(beat_info.energy_profile) - 1))
        return float(beat_info.energy_profile[idx])
