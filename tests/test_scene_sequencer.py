"""Tests for scene_sequencer module."""

from pathlib import Path

import pytest

from drone_reel.core.scene_detector import (
    EnhancedSceneInfo,
    HookPotential,
    MotionType,
    SceneInfo,
)
from drone_reel.core.scene_sequencer import (
    _DYNAMIC_MOTION_TYPES,
    SceneSequencer,
    _composition_sort_key,
    _distribute_arc,
    _hook_sort_key,
    get_hook_priority,
    get_opening_score,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _scene(start: float = 0, end: float = 3, score: float = 80) -> SceneInfo:
    """Create a plain SceneInfo for testing."""
    return SceneInfo(
        start_time=start,
        end_time=end,
        duration=end - start,
        score=score,
        source_file=Path("clip.mp4"),
    )


def _enhanced(
    start: float = 0,
    end: float = 3,
    score: float = 80,
    hook_tier: HookPotential = HookPotential.MEDIUM,
    hook_potential: float = 50.0,
    motion_type: MotionType = MotionType.PAN_LEFT,
    subject_score: float = 0.5,
    source_file: str = "a.mp4",
) -> EnhancedSceneInfo:
    """Create an EnhancedSceneInfo for testing."""
    return EnhancedSceneInfo(
        start_time=start,
        end_time=end,
        duration=end - start,
        score=score,
        source_file=Path(source_file),
        hook_tier=hook_tier,
        hook_potential=hook_potential,
        motion_type=motion_type,
        subject_score=subject_score,
    )


# ===========================================================================
# get_opening_score tests
# ===========================================================================


class TestGetOpeningScore:
    """Tests for the get_opening_score function."""

    def test_plain_scene_info_returns_zero(self):
        scene = _scene()
        assert get_opening_score(scene) == 0.0

    def test_plain_scene_info_with_motion_map_returns_zero(self):
        scene = _scene()
        motion_map = {id(scene): 75.0}
        assert get_opening_score(scene, motion_map) == 0.0

    # -- Hook tier scoring --

    def test_maximum_tier_scores_50(self):
        scene = _enhanced(hook_tier=HookPotential.MAXIMUM, subject_score=0.0)
        assert get_opening_score(scene) == 50.0

    def test_high_tier_scores_40(self):
        scene = _enhanced(hook_tier=HookPotential.HIGH, subject_score=0.0)
        assert get_opening_score(scene) == 40.0

    def test_medium_tier_scores_25(self):
        scene = _enhanced(hook_tier=HookPotential.MEDIUM, subject_score=0.0)
        assert get_opening_score(scene) == 25.0

    def test_low_tier_scores_10(self):
        scene = _enhanced(hook_tier=HookPotential.LOW, subject_score=0.0)
        assert get_opening_score(scene) == 10.0

    def test_poor_tier_scores_0(self):
        scene = _enhanced(hook_tier=HookPotential.POOR, subject_score=0.0)
        assert get_opening_score(scene) == 0.0

    # -- Motion map contribution --

    def test_motion_map_adds_motion_points(self):
        scene = _enhanced(
            hook_tier=HookPotential.POOR,
            subject_score=0.0,
        )
        motion_map = {id(scene): 100.0}
        # 0 (tier) + 100*0.3 (motion) + 0 (subject) = 30
        assert get_opening_score(scene, motion_map) == 30.0

    def test_motion_map_capped_at_100(self):
        scene = _enhanced(
            hook_tier=HookPotential.POOR,
            subject_score=0.0,
        )
        motion_map = {id(scene): 200.0}
        # min(200, 100) * 0.3 = 30
        assert get_opening_score(scene, motion_map) == 30.0

    def test_no_motion_map_zero_motion_contribution(self):
        scene = _enhanced(
            hook_tier=HookPotential.POOR,
            subject_score=0.0,
        )
        assert get_opening_score(scene) == 0.0

    def test_motion_map_missing_scene_id(self):
        scene = _enhanced(
            hook_tier=HookPotential.POOR,
            subject_score=0.0,
        )
        motion_map = {999999: 80.0}
        assert get_opening_score(scene, motion_map) == 0.0

    def test_empty_motion_map_treated_as_falsy(self):
        scene = _enhanced(
            hook_tier=HookPotential.POOR,
            subject_score=0.0,
        )
        # Empty dict is falsy, so the `if motion_map:` branch is skipped
        assert get_opening_score(scene, {}) == 0.0

    # -- Subject score contribution --

    def test_subject_score_contribution(self):
        scene = _enhanced(
            hook_tier=HookPotential.POOR,
            subject_score=1.0,
        )
        # 0 + 0 + 1.0*20 = 20
        assert get_opening_score(scene) == 20.0

    def test_subject_score_half(self):
        scene = _enhanced(
            hook_tier=HookPotential.POOR,
            subject_score=0.5,
        )
        assert get_opening_score(scene) == 10.0

    def test_subject_score_zero(self):
        scene = _enhanced(
            hook_tier=HookPotential.POOR,
            subject_score=0.0,
        )
        assert get_opening_score(scene) == 0.0

    # -- Combined scoring --

    def test_combined_all_components(self):
        scene = _enhanced(
            hook_tier=HookPotential.HIGH,
            subject_score=0.5,
        )
        motion_map = {id(scene): 50.0}
        # 40 (HIGH) + 50*0.3 (motion) + 0.5*20 (subject) = 40 + 15 + 10 = 65
        assert get_opening_score(scene, motion_map) == 65.0

    def test_maximum_possible_score(self):
        scene = _enhanced(
            hook_tier=HookPotential.MAXIMUM,
            subject_score=1.0,
        )
        motion_map = {id(scene): 100.0}
        # 50 + 30 + 20 = 100
        assert get_opening_score(scene, motion_map) == 100.0


# ===========================================================================
# get_hook_priority tests
# ===========================================================================


class TestGetHookPriority:
    """Tests for the get_hook_priority function."""

    def test_plain_scene_info_returns_default(self):
        scene = _scene()
        assert get_hook_priority(scene) == (2, 0)

    def test_maximum_tier_priority(self):
        scene = _enhanced(hook_tier=HookPotential.MAXIMUM, hook_potential=90.0)
        assert get_hook_priority(scene) == (0, -90.0)

    def test_high_tier_priority(self):
        scene = _enhanced(hook_tier=HookPotential.HIGH, hook_potential=80.0)
        assert get_hook_priority(scene) == (1, -80.0)

    def test_medium_tier_priority(self):
        scene = _enhanced(hook_tier=HookPotential.MEDIUM, hook_potential=50.0)
        assert get_hook_priority(scene) == (2, -50.0)

    def test_low_tier_priority(self):
        scene = _enhanced(hook_tier=HookPotential.LOW, hook_potential=30.0)
        assert get_hook_priority(scene) == (3, -30.0)

    def test_poor_tier_priority(self):
        scene = _enhanced(hook_tier=HookPotential.POOR, hook_potential=10.0)
        assert get_hook_priority(scene) == (4, -10.0)

    def test_negative_hook_potential_for_sorting(self):
        """Negating hook_potential ensures higher potential sorts first within same tier."""
        s1 = _enhanced(hook_tier=HookPotential.HIGH, hook_potential=90.0)
        s2 = _enhanced(hook_tier=HookPotential.HIGH, hook_potential=60.0)
        assert get_hook_priority(s1) < get_hook_priority(s2)

    def test_tier_takes_precedence_over_potential(self):
        """A higher tier (lower number) beats higher potential in a lower tier."""
        high_tier = _enhanced(hook_tier=HookPotential.HIGH, hook_potential=10.0)
        low_tier = _enhanced(hook_tier=HookPotential.LOW, hook_potential=99.0)
        assert get_hook_priority(high_tier) < get_hook_priority(low_tier)


# ===========================================================================
# SceneSequencer.sequence tests
# ===========================================================================


class TestSceneSequencerSequence:
    """Tests for SceneSequencer.sequence()."""

    def setup_method(self):
        self.sequencer = SceneSequencer()

    def test_empty_list_returns_empty(self):
        assert self.sequencer.sequence([]) == []

    def test_single_scene_returns_as_is(self):
        scene = _enhanced()
        result = self.sequencer.sequence([scene])
        assert result == [scene]

    def test_single_plain_scene_returns_as_is(self):
        scene = _scene()
        result = self.sequencer.sequence([scene])
        assert result == [scene]

    def test_best_opener_is_first(self):
        poor = _enhanced(
            hook_tier=HookPotential.POOR,
            subject_score=0.0,
            start=0,
            end=3,
        )
        best = _enhanced(
            hook_tier=HookPotential.MAXIMUM,
            subject_score=1.0,
            start=3,
            end=6,
        )
        medium = _enhanced(
            hook_tier=HookPotential.MEDIUM,
            subject_score=0.0,
            start=6,
            end=9,
        )
        result = self.sequencer.sequence([poor, best, medium])
        assert result[0] is best

    def test_opener_uses_motion_map(self):
        s1 = _enhanced(
            hook_tier=HookPotential.POOR,
            subject_score=0.0,
            start=0,
            end=3,
        )
        s2 = _enhanced(
            hook_tier=HookPotential.POOR,
            subject_score=0.0,
            start=3,
            end=6,
        )
        # s1 has high motion, s2 has none
        motion_map = {id(s1): 100.0, id(s2): 0.0}
        result = self.sequencer.sequence([s2, s1], motion_map)
        assert result[0] is s1

    def test_remaining_sorted_by_hook_priority(self):
        """After the opener, remaining scenes should be sorted by hook priority."""
        opener = _enhanced(
            hook_tier=HookPotential.MAXIMUM,
            hook_potential=99.0,
            subject_score=1.0,
            motion_type=MotionType.REVEAL,
            start=0,
            end=3,
        )
        low = _enhanced(
            hook_tier=HookPotential.LOW,
            hook_potential=20.0,
            motion_type=MotionType.STATIC,
            start=3,
            end=6,
        )
        high = _enhanced(
            hook_tier=HookPotential.HIGH,
            hook_potential=80.0,
            motion_type=MotionType.PAN_RIGHT,
            start=6,
            end=9,
        )
        # All different motion types so motion variety won't reorder them
        result = self.sequencer.sequence([low, opener, high])
        assert result[0] is opener
        assert result[1] is high
        assert result[2] is low

    def test_preserves_all_scenes(self):
        scenes = [
            _enhanced(start=i * 3, end=(i + 1) * 3, hook_tier=tier)
            for i, tier in enumerate(
                [HookPotential.LOW, HookPotential.HIGH, HookPotential.MEDIUM]
            )
        ]
        result = self.sequencer.sequence(scenes)
        assert len(result) == 3
        assert set(id(s) for s in result) == set(id(s) for s in scenes)

    def test_two_scenes_no_motion_variety_applied(self):
        """With exactly 2 scenes, motion variety is not applied (len > 2 check)."""
        s1 = _enhanced(
            hook_tier=HookPotential.POOR,
            motion_type=MotionType.PAN_LEFT,
            start=0,
            end=3,
        )
        s2 = _enhanced(
            hook_tier=HookPotential.MAXIMUM,
            subject_score=1.0,
            motion_type=MotionType.PAN_LEFT,
            start=3,
            end=6,
        )
        result = self.sequencer.sequence([s1, s2])
        assert result[0] is s2  # best opener
        assert result[1] is s1

    def test_plain_scene_infos_sequenced(self):
        """Plain SceneInfo objects all score 0 for opening; order is deterministic."""
        s1 = _scene(start=0, end=3)
        s2 = _scene(start=3, end=6)
        s3 = _scene(start=6, end=9)
        result = self.sequencer.sequence([s1, s2, s3])
        assert len(result) == 3

    def test_mixed_plain_and_enhanced(self):
        """Enhanced scenes should be preferred as openers over plain SceneInfo."""
        plain = _scene(start=0, end=3)
        enhanced = _enhanced(
            hook_tier=HookPotential.HIGH,
            subject_score=0.5,
            start=3,
            end=6,
        )
        plain2 = _scene(start=6, end=9)
        result = self.sequencer.sequence([plain, enhanced, plain2])
        assert result[0] is enhanced


# ===========================================================================
# SceneSequencer._apply_motion_variety tests
# ===========================================================================


class TestApplyMotionVariety:
    """Tests for SceneSequencer._apply_motion_variety()."""

    def setup_method(self):
        self.sequencer = SceneSequencer()

    def test_first_scene_stays_fixed(self):
        opener = _enhanced(
            hook_tier=HookPotential.MAXIMUM,
            motion_type=MotionType.PAN_LEFT,
            start=0,
            end=3,
        )
        s2 = _enhanced(
            hook_tier=HookPotential.HIGH,
            motion_type=MotionType.PAN_RIGHT,
            start=3,
            end=6,
        )
        s3 = _enhanced(
            hook_tier=HookPotential.MEDIUM,
            motion_type=MotionType.FLYOVER,
            start=6,
            end=9,
        )
        result = self.sequencer._apply_motion_variety([opener, s2, s3])
        assert result[0] is opener

    def test_avoids_consecutive_same_motion(self):
        """Scenes with the same motion type should not be adjacent when alternatives exist."""
        s_pan_a = _enhanced(
            hook_tier=HookPotential.HIGH,
            hook_potential=90.0,
            motion_type=MotionType.PAN_LEFT,
            start=0,
            end=3,
        )
        s_pan_b = _enhanced(
            hook_tier=HookPotential.HIGH,
            hook_potential=85.0,
            motion_type=MotionType.PAN_LEFT,
            start=3,
            end=6,
        )
        s_fly = _enhanced(
            hook_tier=HookPotential.MEDIUM,
            hook_potential=50.0,
            motion_type=MotionType.FLYOVER,
            start=6,
            end=9,
        )
        result = self.sequencer._apply_motion_variety([s_pan_a, s_pan_b, s_fly])
        # After s_pan_a, should pick s_fly (different motion) before s_pan_b
        assert result[0] is s_pan_a
        assert result[1] is s_fly
        assert result[2] is s_pan_b

    def test_fallback_when_all_same_motion(self):
        """When all remaining scenes have the same motion, pick best by hook priority."""
        s1 = _enhanced(
            hook_tier=HookPotential.HIGH,
            hook_potential=90.0,
            motion_type=MotionType.PAN_LEFT,
            start=0,
            end=3,
        )
        s2 = _enhanced(
            hook_tier=HookPotential.MEDIUM,
            hook_potential=50.0,
            motion_type=MotionType.PAN_LEFT,
            start=3,
            end=6,
        )
        s3 = _enhanced(
            hook_tier=HookPotential.LOW,
            hook_potential=20.0,
            motion_type=MotionType.PAN_LEFT,
            start=6,
            end=9,
        )
        result = self.sequencer._apply_motion_variety([s1, s2, s3])
        assert result[0] is s1
        # Fallback: best by hook priority
        assert result[1] is s2
        assert result[2] is s3

    def test_motion_variety_with_three_different_motions(self):
        s_pan = _enhanced(
            hook_tier=HookPotential.HIGH,
            hook_potential=80.0,
            motion_type=MotionType.PAN_LEFT,
            start=0,
            end=3,
        )
        s_orbit = _enhanced(
            hook_tier=HookPotential.HIGH,
            hook_potential=80.0,
            motion_type=MotionType.ORBIT_CW,
            start=3,
            end=6,
        )
        s_fly = _enhanced(
            hook_tier=HookPotential.HIGH,
            hook_potential=80.0,
            motion_type=MotionType.FLYOVER,
            start=6,
            end=9,
        )
        result = self.sequencer._apply_motion_variety([s_pan, s_orbit, s_fly])
        # No consecutive same-motion clips
        for i in range(len(result) - 1):
            assert result[i].motion_type != result[i + 1].motion_type

    def test_plain_scene_defaults_to_static_motion(self):
        """Plain SceneInfo should be treated as STATIC motion type."""
        enhanced_static = _enhanced(
            hook_tier=HookPotential.HIGH,
            hook_potential=90.0,
            motion_type=MotionType.STATIC,
            start=0,
            end=3,
        )
        plain = _scene(start=3, end=6)
        enhanced_pan = _enhanced(
            hook_tier=HookPotential.LOW,
            hook_potential=10.0,
            motion_type=MotionType.PAN_LEFT,
            start=6,
            end=9,
        )
        result = self.sequencer._apply_motion_variety(
            [enhanced_static, plain, enhanced_pan]
        )
        # enhanced_static is STATIC, plain defaults to STATIC -> same motion
        # So motion variety should prefer enhanced_pan after enhanced_static
        assert result[0] is enhanced_static
        assert result[1] is enhanced_pan
        assert result[2] is plain

    def test_preserves_all_scenes_count(self):
        scenes = [
            _enhanced(
                start=i * 3,
                end=(i + 1) * 3,
                motion_type=motion,
                hook_tier=HookPotential.MEDIUM,
                hook_potential=50.0,
            )
            for i, motion in enumerate(
                [MotionType.PAN_LEFT, MotionType.ORBIT_CW, MotionType.FLYOVER,
                 MotionType.TILT_UP, MotionType.REVEAL]
            )
        ]
        result = self.sequencer._apply_motion_variety(scenes)
        assert len(result) == 5
        assert set(id(s) for s in result) == set(id(s) for s in scenes)


# ===========================================================================
# SceneSequencer._get_motion_type tests
# ===========================================================================


class TestGetMotionType:
    """Tests for SceneSequencer._get_motion_type()."""

    def test_enhanced_scene_returns_motion_type(self):
        scene = _enhanced(motion_type=MotionType.FPV)
        assert SceneSequencer._get_motion_type(scene) == MotionType.FPV

    def test_plain_scene_returns_static(self):
        scene = _scene()
        assert SceneSequencer._get_motion_type(scene) == MotionType.STATIC

    @pytest.mark.parametrize(
        "motion",
        [
            MotionType.STATIC,
            MotionType.PAN_LEFT,
            MotionType.PAN_RIGHT,
            MotionType.TILT_UP,
            MotionType.TILT_DOWN,
            MotionType.ORBIT_CW,
            MotionType.ORBIT_CCW,
            MotionType.REVEAL,
            MotionType.FLYOVER,
            MotionType.FPV,
            MotionType.APPROACH,
            MotionType.UNKNOWN,
        ],
    )
    def test_all_motion_types_returned_correctly(self, motion):
        scene = _enhanced(motion_type=motion)
        assert SceneSequencer._get_motion_type(scene) == motion


# ===========================================================================
# Integration / edge-case tests
# ===========================================================================


class TestSceneSequencerEdgeCases:
    """Edge case and integration tests for SceneSequencer."""

    def setup_method(self):
        self.sequencer = SceneSequencer()

    def test_duplicate_opening_scores_deterministic(self):
        """When multiple scenes tie for best opener, max() picks one deterministically."""
        scenes = [
            _enhanced(
                hook_tier=HookPotential.MEDIUM,
                subject_score=0.0,
                start=i * 3,
                end=(i + 1) * 3,
                motion_type=MotionType.PAN_LEFT,
            )
            for i in range(4)
        ]
        result = self.sequencer.sequence(scenes)
        assert len(result) == 4

    def test_large_scene_list(self):
        """Sequencing a large list completes and preserves all scenes."""
        motions = list(MotionType)
        scenes = [
            _enhanced(
                start=i * 3,
                end=(i + 1) * 3,
                hook_tier=HookPotential.MEDIUM,
                hook_potential=float(i),
                motion_type=motions[i % len(motions)],
                subject_score=0.1 * (i % 10),
            )
            for i in range(50)
        ]
        result = self.sequencer.sequence(scenes)
        assert len(result) == 50
        assert set(id(s) for s in result) == set(id(s) for s in scenes)

    def test_sequence_returns_new_list(self):
        """Sequence should return a new list, not mutate the original."""
        scenes = [
            _enhanced(start=0, end=3, motion_type=MotionType.PAN_LEFT),
            _enhanced(start=3, end=6, motion_type=MotionType.PAN_RIGHT),
            _enhanced(start=6, end=9, motion_type=MotionType.FLYOVER),
        ]
        original_order = list(scenes)
        result = self.sequencer.sequence(scenes)
        # Original list unchanged
        assert scenes == original_order
        # Result is a different list object
        assert result is not scenes

    def test_all_poor_scenes_still_sequences(self):
        """Even if all scenes are POOR tier, sequencing produces a valid result."""
        scenes = [
            _enhanced(
                hook_tier=HookPotential.POOR,
                hook_potential=0.0,
                subject_score=0.0,
                start=i * 3,
                end=(i + 1) * 3,
                motion_type=MotionType.STATIC,
            )
            for i in range(5)
        ]
        result = self.sequencer.sequence(scenes)
        assert len(result) == 5

    def test_motion_variety_alternates_two_types(self):
        """With two alternating motion types, no consecutive duplicates."""
        scenes = []
        for i in range(6):
            motion = MotionType.PAN_LEFT if i % 2 == 0 else MotionType.ORBIT_CW
            scenes.append(
                _enhanced(
                    start=i * 3,
                    end=(i + 1) * 3,
                    hook_tier=HookPotential.MEDIUM,
                    hook_potential=50.0 - i,
                    motion_type=motion,
                    subject_score=0.0,
                )
            )
        result = self.sequencer.sequence(scenes)
        for i in range(len(result) - 1):
            if isinstance(result[i], EnhancedSceneInfo) and isinstance(
                result[i + 1], EnhancedSceneInfo
            ):
                assert result[i].motion_type != result[i + 1].motion_type


# ===========================================================================
# CF-2: Hook enforcement tests
# ===========================================================================


class TestHookSortKey:
    """Tests for the _hook_sort_key helper (CF-2)."""

    def test_maximum_tier_ranks_first(self):
        maximum = _enhanced(hook_tier=HookPotential.MAXIMUM, score=50.0)
        high = _enhanced(hook_tier=HookPotential.HIGH, score=90.0)
        assert _hook_sort_key(maximum) < _hook_sort_key(high)

    def test_dynamic_motion_preferred_within_same_tier(self):
        flyover = _enhanced(
            hook_tier=HookPotential.HIGH, motion_type=MotionType.FLYOVER, score=70.0
        )
        static = _enhanced(
            hook_tier=HookPotential.HIGH, motion_type=MotionType.STATIC, score=70.0
        )
        assert _hook_sort_key(flyover) < _hook_sort_key(static)

    def test_orbit_preferred_over_pan_within_same_tier(self):
        orbit = _enhanced(
            hook_tier=HookPotential.HIGH, motion_type=MotionType.ORBIT_CW, score=70.0
        )
        pan = _enhanced(
            hook_tier=HookPotential.HIGH, motion_type=MotionType.PAN_LEFT, score=70.0
        )
        assert _hook_sort_key(orbit) < _hook_sort_key(pan)

    def test_higher_score_wins_when_tier_and_motion_tied(self):
        hi_score = _enhanced(
            hook_tier=HookPotential.HIGH, motion_type=MotionType.FLYOVER, score=90.0
        )
        lo_score = _enhanced(
            hook_tier=HookPotential.HIGH, motion_type=MotionType.FLYOVER, score=50.0
        )
        assert _hook_sort_key(hi_score) < _hook_sort_key(lo_score)

    def test_plain_scene_info_gets_medium_tier_rank(self):
        plain = _scene(score=99.0)
        # Plain scenes get MEDIUM tier rank (2) and rank after all dynamic motion
        tier_rank, motion_rank, neg_score = _hook_sort_key(plain)
        assert tier_rank == 2
        assert motion_rank == len(_DYNAMIC_MOTION_TYPES)

    def test_tilt_motion_treated_as_non_dynamic(self):
        tilt = _enhanced(
            hook_tier=HookPotential.MAXIMUM, motion_type=MotionType.TILT_UP, score=80.0
        )
        flyover = _enhanced(
            hook_tier=HookPotential.MAXIMUM, motion_type=MotionType.FLYOVER, score=80.0
        )
        # Same tier, flyover is dynamic -> lower motion_rank -> better key
        assert _hook_sort_key(flyover) < _hook_sort_key(tilt)


class TestCF2HookEnforcement:
    """Integration tests verifying CF-2: position 0 is best hook scene."""

    def setup_method(self):
        self.sequencer = SceneSequencer()

    def test_maximum_tier_always_first(self):
        poor = _enhanced(hook_tier=HookPotential.POOR, score=99.0, start=0, end=3)
        maximum = _enhanced(
            hook_tier=HookPotential.MAXIMUM,
            motion_type=MotionType.FLYOVER,
            score=50.0,
            start=3,
            end=6,
        )
        medium = _enhanced(hook_tier=HookPotential.MEDIUM, score=80.0, start=6, end=9)
        result = self.sequencer.sequence([poor, maximum, medium])
        assert result[0] is maximum

    def test_dynamic_motion_beats_static_within_same_tier(self):
        static_hook = _enhanced(
            hook_tier=HookPotential.HIGH,
            motion_type=MotionType.STATIC,
            score=90.0,
            start=0,
            end=3,
        )
        flyover_hook = _enhanced(
            hook_tier=HookPotential.HIGH,
            motion_type=MotionType.FLYOVER,
            score=70.0,
            start=3,
            end=6,
        )
        other = _enhanced(hook_tier=HookPotential.LOW, score=40.0, start=6, end=9)
        result = self.sequencer.sequence([static_hook, flyover_hook, other])
        assert result[0] is flyover_hook

    def test_higher_score_wins_with_same_tier_and_motion(self):
        lo = _enhanced(
            hook_tier=HookPotential.MAXIMUM,
            motion_type=MotionType.ORBIT_CW,
            score=60.0,
            start=0,
            end=3,
        )
        hi = _enhanced(
            hook_tier=HookPotential.MAXIMUM,
            motion_type=MotionType.ORBIT_CW,
            score=90.0,
            start=3,
            end=6,
        )
        other = _enhanced(hook_tier=HookPotential.MEDIUM, score=50.0, start=6, end=9)
        result = self.sequencer.sequence([lo, hi, other])
        assert result[0] is hi

    def test_reveal_motion_preferred_over_pan_same_tier(self):
        pan = _enhanced(
            hook_tier=HookPotential.MAXIMUM,
            motion_type=MotionType.PAN_LEFT,
            score=80.0,
            start=0,
            end=3,
        )
        reveal = _enhanced(
            hook_tier=HookPotential.MAXIMUM,
            motion_type=MotionType.REVEAL,
            score=80.0,
            start=3,
            end=6,
        )
        other = _enhanced(hook_tier=HookPotential.LOW, score=30.0, start=6, end=9)
        result = self.sequencer.sequence([pan, reveal, other])
        assert result[0] is reveal

    def test_hook_enforcement_with_all_poor_scenes(self):
        """Even with all POOR scenes, sequencing returns all scenes."""
        scenes = [
            _enhanced(
                hook_tier=HookPotential.POOR,
                motion_type=MotionType.STATIC,
                score=float(i * 10),
                start=i * 3,
                end=(i + 1) * 3,
            )
            for i in range(4)
        ]
        result = self.sequencer.sequence(scenes)
        assert len(result) == 4

    def test_single_scene_returned_as_is(self):
        scene = _enhanced(hook_tier=HookPotential.POOR)
        result = self.sequencer.sequence([scene])
        assert result == [scene]

    def test_two_scenes_best_hook_is_first(self):
        low = _enhanced(hook_tier=HookPotential.LOW, score=60.0, start=0, end=3)
        high = _enhanced(
            hook_tier=HookPotential.HIGH, motion_type=MotionType.FLYOVER,
            score=70.0, start=3, end=6,
        )
        result = self.sequencer.sequence([low, high])
        assert result[0] is high


# ===========================================================================
# QW-4: Narrative energy arc tests
# ===========================================================================


class TestDistributeArc:
    """Unit tests for the _distribute_arc helper (QW-4)."""

    def _make_scenes(self, n: int) -> list[EnhancedSceneInfo]:
        """Create n scenes with varying tiers, motions, and scores."""
        tiers = list(HookPotential)
        motions = [
            MotionType.FLYOVER, MotionType.PAN_LEFT, MotionType.STATIC,
            MotionType.ORBIT_CW, MotionType.TILT_UP,
        ]
        return [
            _enhanced(
                hook_tier=tiers[i % len(tiers)],
                motion_type=motions[i % len(motions)],
                score=float((i + 1) * 10 % 100 + 5),
                start=i * 3,
                end=(i + 1) * 3,
            )
            for i in range(n)
        ]

    def test_preserves_all_scenes(self):
        scenes = self._make_scenes(8)
        result = _distribute_arc(scenes)
        assert len(result) == len(scenes)
        assert set(id(s) for s in result) == set(id(s) for s in scenes)

    def test_opener_stays_at_position_0(self):
        scenes = self._make_scenes(6)
        result = _distribute_arc(scenes)
        assert result[0] is scenes[0]

    def test_short_list_returns_unchanged(self):
        for n in (1, 2, 3):
            scenes = self._make_scenes(n)
            result = _distribute_arc(scenes)
            assert result == scenes

    def test_resolution_clip_is_last(self):
        """The best composition scene should appear at the end."""
        # Create a scene with a very high depth_score to be the closer.
        closer = EnhancedSceneInfo(
            start_time=30,
            end_time=33,
            duration=3,
            score=80.0,
            source_file=Path("a.mp4"),
            hook_tier=HookPotential.LOW,
            motion_type=MotionType.STATIC,
            depth_score=1.0,  # max composition -> should be closer
        )
        opener = _enhanced(hook_tier=HookPotential.MAXIMUM, motion_type=MotionType.FLYOVER, start=0, end=3)
        others = self._make_scenes(6)
        all_scenes = [opener] + others + [closer]
        result = _distribute_arc(all_scenes)
        assert result[-1] is closer

    def test_climax_section_has_highest_scoring_scenes(self):
        """Climax section clips should have higher scores than build clips."""
        # 8 scenes: opener at [0], high-score climax candidates in the middle.
        opener = _enhanced(
            hook_tier=HookPotential.MAXIMUM,
            motion_type=MotionType.FLYOVER,
            score=90.0,
            start=0,
            end=3,
        )
        high_energy = [
            _enhanced(
                hook_tier=HookPotential.HIGH,
                motion_type=MotionType.ORBIT_CW,
                score=float(80 + i),
                start=(i + 1) * 3,
                end=(i + 2) * 3,
            )
            for i in range(3)
        ]
        low_energy = [
            _enhanced(
                hook_tier=HookPotential.LOW,
                motion_type=MotionType.STATIC,
                score=float(20 + i),
                start=(i + 4) * 3,
                end=(i + 5) * 3,
            )
            for i in range(3)
        ]
        closer = EnhancedSceneInfo(
            start_time=21,
            end_time=24,
            duration=3,
            score=50.0,
            source_file=Path("a.mp4"),
            hook_tier=HookPotential.POOR,
            motion_type=MotionType.STATIC,
            depth_score=0.9,
        )
        all_scenes = [opener] + high_energy + low_energy + [closer]
        result = _distribute_arc(all_scenes)

        n = len(result)
        climax_start = round(n * 0.50)
        climax_end = round(n * 0.85)
        build_end = round(n * 0.50)

        climax_clips = result[climax_start:climax_end]
        build_clips = result[1:build_end]  # skip opener

        if climax_clips and build_clips:
            avg_climax = sum(s.score for s in climax_clips) / len(climax_clips)
            avg_build = sum(s.score for s in build_clips) / len(build_clips)
            assert avg_climax >= avg_build, (
                f"Climax avg score {avg_climax:.1f} should be >= build avg {avg_build:.1f}"
            )


class TestQW4NarrativeArc:
    """Integration tests for QW-4 narrative arc in SceneSequencer.sequence()."""

    def setup_method(self):
        self.sequencer = SceneSequencer()

    def test_all_scenes_preserved(self):
        scenes = [
            _enhanced(
                hook_tier=HookPotential.MEDIUM,
                motion_type=MotionType.PAN_LEFT,
                score=float(50 + i * 5),
                start=i * 3,
                end=(i + 1) * 3,
            )
            for i in range(10)
        ]
        result = self.sequencer.sequence(scenes)
        assert len(result) == 10
        assert set(id(s) for s in result) == set(id(s) for s in scenes)

    def test_opener_is_always_position_0(self):
        scenes = [
            _enhanced(
                hook_tier=HookPotential.HIGH if i == 2 else HookPotential.LOW,
                motion_type=MotionType.FLYOVER if i == 2 else MotionType.STATIC,
                score=float(50 + i),
                start=i * 3,
                end=(i + 1) * 3,
            )
            for i in range(8)
        ]
        result = self.sequencer.sequence(scenes)
        assert result[0] is scenes[2]

    def test_large_arc_no_consecutive_same_motion(self):
        """After arc + motion variety, no two consecutive clips share the same motion."""
        motions = [
            MotionType.PAN_LEFT, MotionType.ORBIT_CW, MotionType.FLYOVER,
            MotionType.TILT_UP, MotionType.REVEAL, MotionType.PAN_RIGHT,
        ]
        scenes = [
            _enhanced(
                hook_tier=HookPotential.MEDIUM,
                motion_type=motions[i % len(motions)],
                score=float(50 + i),
                start=i * 3,
                end=(i + 1) * 3,
            )
            for i in range(12)
        ]
        result = self.sequencer.sequence(scenes)
        for i in range(len(result) - 1):
            s_a, s_b = result[i], result[i + 1]
            if isinstance(s_a, EnhancedSceneInfo) and isinstance(s_b, EnhancedSceneInfo):
                assert s_a.motion_type != s_b.motion_type, (
                    f"Consecutive same motion {s_a.motion_type} at positions {i}, {i+1}"
                )

    def test_minimum_scenes_for_arc(self):
        """Arc is only applied when len > 3; smaller lists pass through."""
        for n in (1, 2, 3):
            scenes = [
                _enhanced(score=float(i * 10), start=i * 3, end=(i + 1) * 3)
                for i in range(n)
            ]
            result = self.sequencer.sequence(scenes)
            assert len(result) == n

    def test_arc_with_mixed_plain_and_enhanced(self):
        """Mixed scene types: enhanced scenes take priority for hook, arc applied."""
        plain_scenes = [_scene(start=i * 3, end=(i + 1) * 3) for i in range(4)]
        enhanced_hook = _enhanced(
            hook_tier=HookPotential.MAXIMUM,
            motion_type=MotionType.FLYOVER,
            score=90.0,
            start=12,
            end=15,
        )
        all_scenes = plain_scenes + [enhanced_hook]
        result = self.sequencer.sequence(all_scenes)
        assert result[0] is enhanced_hook
        assert len(result) == 5

    def test_composition_sort_key_for_plain_scene(self):
        """Plain SceneInfo uses raw score as composition key."""
        plain = _scene(score=75.0)
        assert _composition_sort_key(plain) == 75.0

    def test_composition_sort_key_calm_motion_bonus(self):
        """Static/tilt scenes get a bonus for resolution slot."""
        calm = _enhanced(motion_type=MotionType.STATIC, score=50.0)
        dynamic = _enhanced(motion_type=MotionType.FLYOVER, score=50.0)
        assert _composition_sort_key(calm) > _composition_sort_key(dynamic)
