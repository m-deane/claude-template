"""
Sequence optimization for drone video reels.

Provides diversity-aware scene selection and motion continuity optimization
to create smooth, engaging video sequences.
"""

from collections import defaultdict
from pathlib import Path

import numpy as np

from drone_reel.core.scene_detector import EnhancedSceneInfo, MotionType, SceneInfo


class DiversitySelector:
    """
    Select scenes balancing quality scores with content diversity.

    Prevents repetitive reels by ensuring variety in:
    - Motion types (different camera movements)
    - Source files (clips from different videos)
    - Temporal spacing (avoid adjacent clips from same source)
    - Color palettes (visual variety)
    """

    def __init__(
        self,
        diversity_weight: float = 0.3,
        max_per_source: int = 2,
        min_temporal_gap: float = 5.0,
    ):
        """
        Initialize diversity selector.

        Args:
            diversity_weight: Weight for diversity vs. score (0-1)
            max_per_source: Maximum clips allowed from same source file
            min_temporal_gap: Minimum seconds between clips from same source
        """
        if not 0 <= diversity_weight <= 1:
            raise ValueError("diversity_weight must be between 0 and 1")
        if max_per_source < 1:
            raise ValueError("max_per_source must be at least 1")
        if min_temporal_gap < 0:
            raise ValueError("min_temporal_gap must be non-negative")

        self.diversity_weight = diversity_weight
        self.score_weight = 1.0 - diversity_weight
        self.max_per_source = max_per_source
        self.min_temporal_gap = min_temporal_gap

    @staticmethod
    def min_scenes_for_duration(target_duration: float) -> int:
        """
        Return the minimum recommended scene count for a target reel duration.

        Args:
            target_duration: Desired reel length in seconds.

        Returns:
            Minimum number of scenes (5, 8, 12, or 15).
        """
        if target_duration <= 15:
            return 5
        elif target_duration <= 30:
            return 8
        elif target_duration <= 60:
            return 12
        return 15

    def select(
        self, scenes: list[SceneInfo], count: int
    ) -> list[SceneInfo]:
        """
        Select scenes balancing score with diversity.

        Args:
            scenes: Candidate scenes to select from
            count: Number of scenes to select

        Returns:
            List of selected scenes in score-diversity order
        """
        if not scenes:
            return []

        if count <= 0:
            return []

        if count >= len(scenes):
            return list(scenes)

        selected: list[SceneInfo] = []
        source_counts: dict[Path, int] = defaultdict(int)
        source_times: dict[Path, list[float]] = defaultdict(list)

        # Sort by score initially
        candidates = sorted(scenes, key=lambda s: s.score, reverse=True)

        # Track used motion types for EnhancedSceneInfo
        used_motion_types: set[MotionType] = set()

        for candidate in candidates:
            if len(selected) >= count:
                break

            # Check source diversity constraint
            if source_counts[candidate.source_file] >= self.max_per_source:
                continue

            # Check temporal diversity constraint
            if self.min_temporal_gap > 0:
                too_close = False
                for prev_time in source_times[candidate.source_file]:
                    if abs(candidate.start_time - prev_time) < self.min_temporal_gap:
                        too_close = True
                        break
                if too_close:
                    continue

            # Calculate combined score
            diversity_score = self._calculate_diversity_score(candidate, selected, used_motion_types)
            combined_score = (
                self.score_weight * candidate.score
                + self.diversity_weight * diversity_score
            )

            # Add to selected
            selected.append(candidate)
            source_counts[candidate.source_file] += 1
            source_times[candidate.source_file].append(candidate.start_time)

            # Track motion type if enhanced
            if isinstance(candidate, EnhancedSceneInfo):
                used_motion_types.add(candidate.motion_type)

        # If we didn't get enough scenes due to constraints, relax and add more
        if len(selected) < count:
            remaining = [s for s in candidates if s not in selected]
            selected.extend(remaining[: count - len(selected)])

        return selected

    def select_with_minimum(
        self,
        scenes: list[SceneInfo],
        count: int,
        target_duration: float,
    ) -> list[SceneInfo]:
        """
        Select scenes with a minimum count enforced by target duration.

        If diversity/quality constraints yield fewer scenes than the minimum,
        this method progressively relaxes the max_per_source limit (down to 1)
        and then ignores all constraints to reach the minimum count.

        Args:
            scenes: Candidate scenes.
            count: Desired number of scenes (upper bound).
            target_duration: Used to derive the minimum scene count.

        Returns:
            Selected scenes list of length between min_scenes and count.
        """
        min_count = self.min_scenes_for_duration(target_duration)
        effective_count = max(count, min_count)

        selected = self.select(scenes, effective_count)
        if len(selected) >= min_count:
            return selected

        # Progressively relax max_per_source to meet min_count
        for relaxed_limit in range(self.max_per_source + 1, len(scenes) + 1):
            relaxed = DiversitySelector(
                diversity_weight=self.diversity_weight,
                max_per_source=relaxed_limit,
                min_temporal_gap=self.min_temporal_gap,
            )
            selected = relaxed.select(scenes, effective_count)
            if len(selected) >= min_count:
                return selected

        # Last resort: return everything available up to effective_count
        if len(selected) < min_count:
            existing_ids = {id(s) for s in selected}
            extras = [s for s in scenes if id(s) not in existing_ids]
            selected = selected + extras[: min_count - len(selected)]

        return selected

    def _calculate_diversity_score(
        self,
        candidate: SceneInfo,
        selected: list[SceneInfo],
        used_motion_types: set[MotionType],
    ) -> float:
        """
        Calculate how different a candidate is from selected scenes.

        Args:
            candidate: Scene to evaluate
            selected: Already selected scenes
            used_motion_types: Motion types already used

        Returns:
            Diversity score from 0-100, higher is more diverse
        """
        if not selected:
            return 100.0

        scores: list[float] = []

        # Motion type diversity (for EnhancedSceneInfo)
        if isinstance(candidate, EnhancedSceneInfo):
            if candidate.motion_type not in used_motion_types:
                scores.append(100.0)
            else:
                # Penalize but not completely
                scores.append(30.0)

        # Source file diversity
        source_files = {s.source_file for s in selected}
        if candidate.source_file not in source_files:
            scores.append(100.0)
        else:
            # Penalize based on how many times we've used this source
            count = sum(1 for s in selected if s.source_file == candidate.source_file)
            scores.append(max(0, 100 - count * 50))

        # Temporal diversity - prefer scenes from different parts of source videos
        temporal_score = 100.0
        for scene in selected:
            if scene.source_file == candidate.source_file:
                time_diff = abs(candidate.start_time - scene.start_time)
                if time_diff < self.min_temporal_gap:
                    temporal_score = min(temporal_score, time_diff / self.min_temporal_gap * 100)
        scores.append(temporal_score)

        # Color diversity (for EnhancedSceneInfo)
        if isinstance(candidate, EnhancedSceneInfo) and candidate.dominant_colors:
            color_diversity = self._calculate_color_diversity(candidate, selected)
            scores.append(color_diversity)

        return np.mean(scores) if scores else 50.0

    def _calculate_color_diversity(
        self, candidate: EnhancedSceneInfo, selected: list[SceneInfo]
    ) -> float:
        """
        Calculate color palette diversity.

        Args:
            candidate: Scene with color information
            selected: Already selected scenes

        Returns:
            Color diversity score 0-100
        """
        if not candidate.dominant_colors:
            return 50.0

        # Get dominant colors from selected EnhancedSceneInfo scenes
        selected_colors: list[tuple[int, int, int]] = []
        for scene in selected:
            if isinstance(scene, EnhancedSceneInfo) and scene.dominant_colors:
                selected_colors.extend(scene.dominant_colors)

        if not selected_colors:
            return 100.0

        # Calculate minimum color distance
        min_distance = float("inf")
        for cand_color in candidate.dominant_colors:
            for sel_color in selected_colors:
                distance = self._color_distance(cand_color, sel_color)
                min_distance = min(min_distance, distance)

        # Normalize distance to 0-100 (max distance in RGB is ~441)
        return min(min_distance / 441.0 * 100, 100.0)

    @staticmethod
    def _color_distance(color1: tuple[int, int, int], color2: tuple[int, int, int]) -> float:
        """Calculate Euclidean distance between two RGB colors."""
        return np.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2)))


class MotionContinuityEngine:
    """
    Optimize scene sequences for smooth motion flow.

    Reorders scenes to avoid jarring motion transitions and create
    a professional viewing experience.
    """

    # Compatibility matrix: (from_motion, to_motion) -> score 0-1
    COMPATIBILITY = {
        # Same motion direction = smooth
        (MotionType.PAN_LEFT, MotionType.PAN_LEFT): 0.9,
        (MotionType.PAN_RIGHT, MotionType.PAN_RIGHT): 0.9,
        (MotionType.TILT_UP, MotionType.TILT_UP): 0.9,
        (MotionType.TILT_DOWN, MotionType.TILT_DOWN): 0.9,
        (MotionType.ORBIT_CW, MotionType.ORBIT_CW): 0.9,
        (MotionType.ORBIT_CCW, MotionType.ORBIT_CCW): 0.9,
        # Opposite directions = jarring
        (MotionType.PAN_LEFT, MotionType.PAN_RIGHT): 0.2,
        (MotionType.PAN_RIGHT, MotionType.PAN_LEFT): 0.2,
        (MotionType.TILT_UP, MotionType.TILT_DOWN): 0.3,
        (MotionType.TILT_DOWN, MotionType.TILT_UP): 0.3,
        (MotionType.ORBIT_CW, MotionType.ORBIT_CCW): 0.3,
        (MotionType.ORBIT_CCW, MotionType.ORBIT_CW): 0.3,
        # Static is neutral - works after anything
        (MotionType.STATIC, MotionType.PAN_LEFT): 0.8,
        (MotionType.STATIC, MotionType.PAN_RIGHT): 0.8,
        (MotionType.STATIC, MotionType.TILT_UP): 0.8,
        (MotionType.STATIC, MotionType.TILT_DOWN): 0.8,
        (MotionType.STATIC, MotionType.ORBIT_CW): 0.8,
        (MotionType.STATIC, MotionType.ORBIT_CCW): 0.8,
        (MotionType.STATIC, MotionType.REVEAL): 0.8,
        (MotionType.STATIC, MotionType.FLYOVER): 0.8,
        (MotionType.STATIC, MotionType.STATIC): 0.7,
        # Any motion to static works well
        (MotionType.PAN_LEFT, MotionType.STATIC): 0.8,
        (MotionType.PAN_RIGHT, MotionType.STATIC): 0.8,
        (MotionType.TILT_UP, MotionType.STATIC): 0.8,
        (MotionType.TILT_DOWN, MotionType.STATIC): 0.8,
        (MotionType.ORBIT_CW, MotionType.STATIC): 0.8,
        (MotionType.ORBIT_CCW, MotionType.STATIC): 0.8,
        (MotionType.REVEAL, MotionType.STATIC): 0.7,
        (MotionType.FLYOVER, MotionType.STATIC): 0.7,
        # Reveals work well at sequence start
        (MotionType.REVEAL, MotionType.PAN_LEFT): 0.7,
        (MotionType.REVEAL, MotionType.PAN_RIGHT): 0.7,
        (MotionType.REVEAL, MotionType.ORBIT_CW): 0.7,
        (MotionType.REVEAL, MotionType.ORBIT_CCW): 0.7,
        (MotionType.REVEAL, MotionType.FLYOVER): 0.6,
        # Flyovers work well after reveals
        (MotionType.REVEAL, MotionType.FLYOVER): 0.8,
        (MotionType.FLYOVER, MotionType.FLYOVER): 0.7,
        (MotionType.FLYOVER, MotionType.REVEAL): 0.5,
        # FPV is chaotic - works better isolated or after static
        (MotionType.STATIC, MotionType.FPV): 0.7,
        (MotionType.FPV, MotionType.STATIC): 0.8,
        (MotionType.FPV, MotionType.FPV): 0.6,
        (MotionType.FPV, MotionType.PAN_LEFT): 0.4,
        (MotionType.FPV, MotionType.PAN_RIGHT): 0.4,
        # Approach sequences
        (MotionType.APPROACH, MotionType.REVEAL): 0.8,
        (MotionType.APPROACH, MotionType.STATIC): 0.7,
        (MotionType.REVEAL, MotionType.APPROACH): 0.5,
        # Unknown - neutral compatibility
        (MotionType.UNKNOWN, MotionType.UNKNOWN): 0.5,
    }

    # Default compatibility for unlisted pairs
    DEFAULT_COMPATIBILITY = 0.5

    def optimize_sequence(
        self, scenes: list[EnhancedSceneInfo]
    ) -> list[EnhancedSceneInfo]:
        """
        Reorder scenes for smooth motion flow using greedy optimization.

        Uses a greedy approach that builds the sequence by always selecting
        the most compatible next scene.

        Args:
            scenes: Scenes to reorder

        Returns:
            Reordered scenes with optimized motion flow
        """
        if len(scenes) <= 1:
            return list(scenes)

        # Convert to EnhancedSceneInfo if needed
        enhanced_scenes = [
            s if isinstance(s, EnhancedSceneInfo) else self._to_enhanced(s)
            for s in scenes
        ]

        # Start with the best scene
        remaining = list(enhanced_scenes)
        current = max(remaining, key=lambda s: s.score)
        remaining.remove(current)
        optimized = [current]

        # Greedy selection - pick most compatible next scene
        while remaining:
            current = optimized[-1]
            best_next = max(
                remaining,
                key=lambda s: self._motion_compatibility(current, s),
            )
            optimized.append(best_next)
            remaining.remove(best_next)

        return optimized

    def _to_enhanced(self, scene: SceneInfo) -> EnhancedSceneInfo:
        """Convert SceneInfo to EnhancedSceneInfo with unknown motion."""
        return EnhancedSceneInfo(
            start_time=scene.start_time,
            end_time=scene.end_time,
            duration=scene.duration,
            score=scene.score,
            source_file=scene.source_file,
            thumbnail=scene.thumbnail,
            motion_type=MotionType.UNKNOWN,
        )

    def _motion_compatibility(
        self, scene1: EnhancedSceneInfo, scene2: EnhancedSceneInfo
    ) -> float:
        """
        Calculate how well scene2 follows scene1.

        Args:
            scene1: Current scene
            scene2: Candidate next scene

        Returns:
            Compatibility score 0-1, higher is better
        """
        motion_key = (scene1.motion_type, scene2.motion_type)

        # Check exact match
        if motion_key in self.COMPATIBILITY:
            base_score = self.COMPATIBILITY[motion_key]
        else:
            # Check if either is STATIC (use static rules)
            if scene1.motion_type == MotionType.STATIC:
                static_key = (MotionType.STATIC, scene2.motion_type)
                base_score = self.COMPATIBILITY.get(static_key, self.DEFAULT_COMPATIBILITY)
            elif scene2.motion_type == MotionType.STATIC:
                static_key = (scene1.motion_type, MotionType.STATIC)
                base_score = self.COMPATIBILITY.get(static_key, self.DEFAULT_COMPATIBILITY)
            else:
                base_score = self.DEFAULT_COMPATIBILITY

        # Boost score if motion directions align
        if scene1.motion_direction != (0.0, 0.0) and scene2.motion_direction != (0.0, 0.0):
            # Calculate angle between motion vectors
            dot_product = (
                scene1.motion_direction[0] * scene2.motion_direction[0]
                + scene1.motion_direction[1] * scene2.motion_direction[1]
            )
            mag1 = np.sqrt(scene1.motion_direction[0] ** 2 + scene1.motion_direction[1] ** 2)
            mag2 = np.sqrt(scene2.motion_direction[0] ** 2 + scene2.motion_direction[1] ** 2)

            if mag1 > 0 and mag2 > 0:
                cos_angle = dot_product / (mag1 * mag2)
                # Aligned directions boost score, opposite directions reduce
                direction_bonus = (cos_angle + 1) / 2 * 0.1  # 0 to 0.1 bonus
                base_score = min(1.0, base_score + direction_bonus)

        return base_score

    def check_sequence_quality(
        self, scenes: list[EnhancedSceneInfo]
    ) -> dict:
        """
        Analyze sequence for motion issues and return warnings.

        Args:
            scenes: Sequence to analyze

        Returns:
            Dictionary with quality metrics and warnings
        """
        if len(scenes) <= 1:
            return {
                "overall_score": 1.0,
                "avg_compatibility": 1.0,
                "warnings": [],
                "suggestions": [],
            }

        compatibilities: list[float] = []
        warnings: list[str] = []
        suggestions: list[str] = []

        for i in range(len(scenes) - 1):
            compat = self._motion_compatibility(scenes[i], scenes[i + 1])
            compatibilities.append(compat)

            # Flag problematic transitions
            if compat < 0.3:
                warnings.append(
                    f"Jarring transition at position {i}-{i+1}: "
                    f"{scenes[i].motion_type.value} -> {scenes[i+1].motion_type.value} "
                    f"(score: {compat:.2f})"
                )

            # Suggest improvements
            if compat < 0.5:
                suggestions.append(
                    f"Consider adding static shot between positions {i} and {i+1}"
                )

        avg_compatibility = np.mean(compatibilities) if compatibilities else 1.0
        overall_score = avg_compatibility

        # Penalty for too many motion type changes
        motion_changes = sum(
            1
            for i in range(len(scenes) - 1)
            if scenes[i].motion_type != scenes[i + 1].motion_type
        )
        change_ratio = motion_changes / max(len(scenes) - 1, 1)
        if change_ratio > 0.8:
            warnings.append(
                f"High motion variation: {change_ratio:.1%} of transitions change motion type"
            )
            overall_score *= 0.9

        # Check for repeated jarring patterns
        jarring_count = sum(1 for c in compatibilities if c < 0.3)
        if jarring_count > len(compatibilities) * 0.3:
            warnings.append(
                f"Too many jarring transitions: {jarring_count}/{len(compatibilities)}"
            )
            suggestions.append("Consider reordering scenes with optimize_sequence()")

        return {
            "overall_score": overall_score,
            "avg_compatibility": avg_compatibility,
            "warnings": warnings,
            "suggestions": suggestions,
            "transition_scores": compatibilities,
        }
