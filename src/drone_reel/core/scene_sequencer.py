"""
Scene sequencing for drone video reels.

Handles hook-based opening clip selection, hook-priority ordering,
narrative energy arc distribution, and motion variety sequencing to
create engaging reel pacing.
"""

from drone_reel.core.scene_detector import (
    EnhancedSceneInfo,
    HookPotential,
    MotionType,
    SceneInfo,
)

# Motion types that are considered "dynamic" for hook selection.
# Ordered from most preferred to least preferred.
_DYNAMIC_MOTION_TYPES: tuple[MotionType, ...] = (
    MotionType.FLYOVER,
    MotionType.ORBIT_CW,
    MotionType.ORBIT_CCW,
    MotionType.REVEAL,
    MotionType.PAN_LEFT,
    MotionType.PAN_RIGHT,
    MotionType.APPROACH,
    MotionType.FPV,
)

# Tier ordering for hook enforcement (lower = better).
_TIER_RANK: dict[HookPotential, int] = {
    HookPotential.MAXIMUM: 0,
    HookPotential.HIGH: 1,
    HookPotential.MEDIUM: 2,
    HookPotential.LOW: 3,
    HookPotential.POOR: 4,
}

# Sections for the narrative energy arc expressed as (start_pct, end_pct).
# Hook: first 15%, Build: 15-50%, Climax: 50-85%, Resolution: last 15%.
_ARC_SECTIONS = (
    (0.0, 0.15),   # Hook
    (0.15, 0.50),  # Build
    (0.50, 0.85),  # Climax
    (0.85, 1.0),   # Resolution
)


def get_opening_score(
    scene: SceneInfo,
    motion_map: dict[int, float] | None = None,
) -> float:
    """
    Score a scene for opening clip selection (higher = better opener).

    Combines hook potential, motion energy, and subject interest.

    Args:
        scene: Scene to score
        motion_map: Optional map of id(scene) -> motion_energy

    Returns:
        Opening score (0-100)
    """
    score = 0.0

    if isinstance(scene, EnhancedSceneInfo):
        # Hook tier contribution (0-50 points)
        tier_scores = {
            HookPotential.MAXIMUM: 50,
            HookPotential.HIGH: 40,
            HookPotential.MEDIUM: 25,
            HookPotential.LOW: 10,
            HookPotential.POOR: 0,
        }
        score += tier_scores.get(scene.hook_tier, 25)

        # Motion energy contribution (0-30 points)
        motion = 0.0
        if motion_map:
            motion = motion_map.get(id(scene), 0.0)
        score += min(motion, 100) * 0.3

        # Subject score contribution (0-20 points)
        subject = getattr(scene, 'subject_score', 0.0)
        score += subject * 20

    return score


def get_hook_priority(scene: SceneInfo) -> tuple[int, float]:
    """
    Get hook priority for ordering subsequent clips (lower tuple = higher priority).

    Args:
        scene: Scene to evaluate

    Returns:
        Tuple of (tier_priority, -hook_potential) for sorting
    """
    if isinstance(scene, EnhancedSceneInfo):
        tier_priority = {
            HookPotential.MAXIMUM: 0,
            HookPotential.HIGH: 1,
            HookPotential.MEDIUM: 2,
            HookPotential.LOW: 3,
            HookPotential.POOR: 4,
        }
        return (tier_priority.get(scene.hook_tier, 2), -scene.hook_potential)
    return (2, 0)


def _hook_sort_key(scene: SceneInfo) -> tuple[int, int, float]:
    """
    Sort key for strict hook-tier enforcement at position 0.

    Priority: (tier_rank ASC, dynamic_motion_rank ASC, -score ASC).
    Lower tuple = better candidate for the opening hook slot.

    Args:
        scene: Scene to evaluate.

    Returns:
        Three-element tuple suitable for use with min().
    """
    if not isinstance(scene, EnhancedSceneInfo):
        return (_TIER_RANK[HookPotential.MEDIUM], len(_DYNAMIC_MOTION_TYPES), 0.0)

    tier_rank = _TIER_RANK.get(scene.hook_tier, 2)

    motion_type = scene.motion_type
    if motion_type in _DYNAMIC_MOTION_TYPES:
        motion_rank = _DYNAMIC_MOTION_TYPES.index(motion_type)
    else:
        # Static/Tilt/Unknown are deprioritised: rank after all dynamic types.
        motion_rank = len(_DYNAMIC_MOTION_TYPES)

    return (tier_rank, motion_rank, -scene.score)


def _composition_sort_key(scene: SceneInfo) -> float:
    """
    Score a scene's suitability as a resolution/closer shot.

    Favours high composition scores and calmer motion types.

    Args:
        scene: Scene to evaluate.

    Returns:
        Float where higher = better resolution candidate.
    """
    if not isinstance(scene, EnhancedSceneInfo):
        return scene.score

    calm_motions = {
        MotionType.STATIC,
        MotionType.TILT_UP,
        MotionType.TILT_DOWN,
        MotionType.PAN_LEFT,
        MotionType.PAN_RIGHT,
    }
    motion_bonus = 10.0 if scene.motion_type in calm_motions else 0.0

    # Use depth_score as a proxy for cinematic composition quality.
    composition = getattr(scene, 'depth_score', 0.0) * 20.0
    color_var = getattr(scene, 'color_variance', 0.0) * 0.1

    return scene.score + composition + color_var + motion_bonus


def _distribute_arc(scenes: list[SceneInfo]) -> list[SceneInfo]:
    """
    Distribute scenes into the 4-section narrative energy arc.

    Sections (by clip index, not time):
      - Hook        (first ~15%): already assigned – passed in as scenes[0]
      - Build       (15-50%):     moderate energy, rising hook tiers
      - Climax      (50-85%):     highest energy, fastest motion
      - Resolution  (last ~15%):  wide/epic closer, high composition

    The function expects *all* scenes including the opener at index 0.
    It returns a reordered list preserving all scenes.

    Args:
        scenes: All scenes, with the chosen opener at index 0.

    Returns:
        Reordered scene list following the arc.
    """
    n = len(scenes)
    if n <= 3:
        return list(scenes)

    opener = scenes[0]
    remaining = list(scenes[1:])

    # Determine section sizes from clip counts.
    n_remaining = len(remaining)

    def _section_size(start_pct: float, end_pct: float) -> int:
        return max(0, round(n * end_pct) - round(n * start_pct))

    # Hook section is already filled by opener (1 clip).
    n_build = _section_size(0.15, 0.50)
    n_climax = _section_size(0.50, 0.85)
    n_resolve = _section_size(0.85, 1.0)

    # Adjust so totals add up to n_remaining.
    total = n_build + n_climax + n_resolve
    if total < n_remaining:
        n_climax += n_remaining - total
    elif total > n_remaining:
        # Trim from climax first, then build.
        excess = total - n_remaining
        trim_climax = min(excess, n_climax)
        n_climax -= trim_climax
        excess -= trim_climax
        n_build -= min(excess, n_build)

    # Select the best resolution clip first (calm + wide composition).
    remaining_sorted_resolution = sorted(
        remaining, key=_composition_sort_key, reverse=True
    )
    resolve_clips: list[SceneInfo] = []
    if n_resolve > 0 and remaining_sorted_resolution:
        resolve_clips.append(remaining_sorted_resolution[0])
        remaining = [s for s in remaining if s is not resolve_clips[0]]
        n_resolve -= 1

    # Fill remaining resolution slots (if n_resolve > 1) with next best composition.
    if n_resolve > 0:
        for candidate in remaining_sorted_resolution[1:]:
            if candidate in remaining:
                resolve_clips.append(candidate)
                remaining.remove(candidate)
                n_resolve -= 1
                if n_resolve == 0:
                    break

    # Sort remaining by hook priority for climax vs build assignment.
    # Higher hook tier + dynamic motion → climax; moderate → build.
    remaining_by_hook = sorted(remaining, key=_hook_sort_key)

    climax_clips = remaining_by_hook[:n_climax]
    build_clips = remaining_by_hook[n_climax:n_climax + n_build]

    # Sort climax by energy descending (most dramatic first in that section).
    climax_clips = sorted(climax_clips, key=lambda s: s.score, reverse=True)
    # Sort build with gradually rising energy.
    build_clips = sorted(build_clips, key=lambda s: s.score)

    return [opener] + build_clips + climax_clips + resolve_clips


class SceneSequencer:
    """
    Sequence scenes for optimal reel pacing.

    Applies CF-2 hook enforcement (strict tier + dynamic motion + score
    ordering for position 0) and QW-4 narrative energy arc (Hook → Build
    → Climax → Resolution) before applying motion variety.
    """

    def sequence(
        self,
        scenes: list[SceneInfo],
        motion_map: dict[int, float] | None = None,
    ) -> list[SceneInfo]:
        """
        Reorder scenes for optimal reel pacing.

        1. Select best opener (CF-2): highest hook_tier, then dynamic motion
           type preference, then highest scene score.
        2. Distribute remaining scenes into narrative energy arc (QW-4):
           Hook → Build → Climax → Resolution.
        3. Apply motion variety within each section to avoid consecutive
           same-motion clips, keeping the opener fixed at position 0.

        Args:
            scenes: Selected scenes to reorder.
            motion_map: Optional map of id(scene) -> motion_energy.
                        When provided, augments opening score for scenes
                        that lack hook metadata.

        Returns:
            Reordered scene list.
        """
        if len(scenes) <= 1:
            return list(scenes)

        # --- CF-2: Select best opening hook ---
        # Primary key: hook_sort_key (tier > dynamic motion > score).
        # Secondary key (for plain SceneInfo with equal tier): opening score
        # from motion_map.
        best_opener = min(scenes, key=_hook_sort_key)

        # If multiple scenes share the same hook_sort_key (e.g. all plain
        # SceneInfo), fall back to opening score (which uses motion_map).
        best_opener_key = _hook_sort_key(best_opener)
        tied = [s for s in scenes if _hook_sort_key(s) == best_opener_key]
        if len(tied) > 1:
            best_opener = max(tied, key=lambda s: get_opening_score(s, motion_map))

        other_scenes = [s for s in scenes if s is not best_opener]

        # --- QW-4: Narrative arc distribution ---
        arc_ordered = _distribute_arc([best_opener] + other_scenes)

        # --- Motion variety: avoid consecutive same-motion type ---
        if len(arc_ordered) > 2:
            arc_ordered = self._apply_motion_variety(arc_ordered)

        return arc_ordered

    def _apply_motion_variety(
        self, scenes: list[SceneInfo]
    ) -> list[SceneInfo]:
        """
        Reorder scenes (keeping first fixed) to maximise motion variety.

        Avoids consecutive clips with the same motion type by preferring
        scenes with different motion from the previous clip.

        Args:
            scenes: Scenes with first scene (opener) fixed.

        Returns:
            Reordered scenes.
        """
        reordered = [scenes[0]]
        remaining = list(scenes[1:])

        while remaining:
            last_motion = self._get_motion_type(reordered[-1])
            # Find scenes with different motion type
            different_motion = [
                s for s in remaining
                if self._get_motion_type(s) != last_motion
            ]

            if different_motion:
                next_scene = min(different_motion, key=get_hook_priority)
            else:
                next_scene = min(remaining, key=get_hook_priority)

            reordered.append(next_scene)
            remaining.remove(next_scene)

        return reordered

    @staticmethod
    def _get_motion_type(scene: SceneInfo) -> MotionType:
        """Get motion type from a scene, defaulting to STATIC for non-enhanced."""
        if isinstance(scene, EnhancedSceneInfo):
            return scene.motion_type
        return MotionType.STATIC
