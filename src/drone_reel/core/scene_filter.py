"""
Scene filtering for drone video reels.

Filters scenes based on motion energy, brightness, and shake score thresholds.
Supports progressive threshold relaxation when all scenes are filtered out.
"""

from dataclasses import dataclass


@dataclass
class FilterThresholds:
    """Configurable thresholds for scene filtering."""

    min_motion_energy: float = 25.0
    ideal_motion_energy: float = 45.0
    min_brightness: float = 30.0
    max_brightness: float = 245.0
    max_shake_score: float = 40.0
    subject_score_threshold: float = 0.6


@dataclass
class FilterResult:
    """Result of scene filtering with tier breakdown."""

    high_subject_scenes: list
    high_motion_scenes: list
    medium_motion_scenes: list
    low_motion_scenes: list
    dark_scenes_filtered: int
    shaky_scenes_filtered: int

    @property
    def prioritized(self) -> list:
        """Get prioritized scene list (high-subject > high-motion > medium-motion)."""
        return self.high_subject_scenes + self.high_motion_scenes + self.medium_motion_scenes

    @property
    def all_passing(self) -> list:
        """Get all scenes that passed filtering, including low-motion."""
        return self.prioritized + self.low_motion_scenes

    def with_low_motion_if_needed(self, min_count: int) -> list:
        """Get prioritized scenes, adding low-motion if needed to meet count."""
        result = self.prioritized
        if len(result) < min_count:
            result = result + self.low_motion_scenes
        return result


class SceneFilter:
    """
    Filter scenes based on motion energy, brightness, and shake score.

    Separates scenes into quality tiers and supports progressive
    filter relaxation when too few scenes pass.
    """

    def __init__(self, thresholds: FilterThresholds | None = None):
        """
        Initialize scene filter.

        Args:
            thresholds: Filtering thresholds. Uses defaults if None.
        """
        self.thresholds = thresholds or FilterThresholds()

    def filter_scenes(
        self,
        scenes: list,
        motion_map: dict[int, float],
        brightness_map: dict[int, float],
        shake_map: dict[int, float],
    ) -> FilterResult:
        """
        Filter and tier scenes based on motion, brightness, and shake.

        Args:
            scenes: Candidate scenes to filter
            motion_map: Map of id(scene) -> motion_energy (0-100)
            brightness_map: Map of id(scene) -> mean_brightness (0-255)
            shake_map: Map of id(scene) -> shake_score (0-100)

        Returns:
            FilterResult with tiered scene lists and filter statistics
        """
        t = self.thresholds

        high_motion = []
        medium_motion = []
        low_motion = []
        high_subject = []
        dark_filtered = 0
        shaky_filtered = 0

        for scene in scenes:
            motion_energy = motion_map.get(id(scene), 0.0)
            brightness = brightness_map.get(id(scene), 127.0)
            shake_score = shake_map.get(id(scene), 0.0)

            # Filter dark/bright scenes
            if brightness < t.min_brightness or brightness > t.max_brightness:
                dark_filtered += 1
                continue

            # Filter shaky clips
            if shake_score > t.max_shake_score:
                shaky_filtered += 1
                continue

            # Check for high subject score
            subject_score = getattr(scene, 'subject_score', 0.0) if hasattr(scene, 'subject_score') else 0.0
            has_subject = subject_score >= t.subject_score_threshold

            if has_subject:
                high_subject.append(scene)
            elif motion_energy >= t.ideal_motion_energy:
                high_motion.append(scene)
            elif motion_energy >= t.min_motion_energy:
                medium_motion.append(scene)
            else:
                low_motion.append(scene)

        return FilterResult(
            high_subject_scenes=high_subject,
            high_motion_scenes=high_motion,
            medium_motion_scenes=medium_motion,
            low_motion_scenes=low_motion,
            dark_scenes_filtered=dark_filtered,
            shaky_scenes_filtered=shaky_filtered,
        )
