"""Tests for duration_adjuster module."""

from pathlib import Path

import pytest

from drone_reel.core.duration_adjuster import DurationAdjuster, DurationConfig
from drone_reel.core.scene_detector import (
    EnhancedSceneInfo,
    HookPotential,
    MotionType,
    SceneInfo,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _scene(start=0.0, end=5.0, score=80.0):
    """Create a basic SceneInfo."""
    return SceneInfo(
        start_time=start,
        end_time=end,
        duration=end - start,
        score=score,
        source_file=Path("clip.mp4"),
    )


def _enhanced_scene(
    start=0.0,
    end=5.0,
    score=80.0,
    motion_type=MotionType.STATIC,
    hook_tier=HookPotential.MEDIUM,
    subject_score=0.0,
):
    """Create an EnhancedSceneInfo."""
    return EnhancedSceneInfo(
        start_time=start,
        end_time=end,
        duration=end - start,
        score=score,
        source_file=Path("clip.mp4"),
        motion_type=motion_type,
        hook_tier=hook_tier,
        subject_score=subject_score,
    )


def _no_autoscale_config():
    """DurationConfig with auto-scaling disabled for isolated unit tests."""
    return DurationConfig(auto_scale_shortfall=0.0)


# ===========================================================================
# DurationConfig tests
# ===========================================================================


class TestDurationConfig:
    """Tests for DurationConfig dataclass."""

    def test_defaults(self):
        cfg = DurationConfig()
        assert cfg.min_clip_duration == 2.0
        assert cfg.sharp_threshold == 100.0
        assert cfg.soft_threshold == 30.0
        assert cfg.auto_scale_shortfall == 0.85
        assert cfg.auto_scale_max == 1.5

    def test_max_clip_duration_short_reel(self):
        cfg = DurationConfig()
        assert cfg.max_clip_duration(10) == 4.0
        assert cfg.max_clip_duration(15) == 4.0

    def test_max_clip_duration_medium_reel(self):
        cfg = DurationConfig()
        assert cfg.max_clip_duration(20) == 5.0
        assert cfg.max_clip_duration(30) == 5.0

    def test_max_clip_duration_long_reel(self):
        cfg = DurationConfig()
        assert cfg.max_clip_duration(31) == 6.0
        assert cfg.max_clip_duration(60) == 6.0
        assert cfg.max_clip_duration(120) == 6.0

    def test_custom_values(self):
        cfg = DurationConfig(min_clip_duration=1.5, sharp_threshold=120.0)
        assert cfg.min_clip_duration == 1.5
        assert cfg.sharp_threshold == 120.0


# ===========================================================================
# DurationAdjuster tests
# ===========================================================================


class TestDurationAdjusterSharpness:
    """Tests for sharpness-based duration adjustment."""

    def test_very_blurry_gets_min_duration(self):
        """Scenes with sharpness < soft_threshold get minimum clip duration."""
        adjuster = DurationAdjuster(config=_no_autoscale_config())
        scene = _scene()
        scenes = [scene]
        durations = [4.0]
        sharpness_map = {id(scene): 20.0}  # Below soft_threshold of 30

        result, scale = adjuster.adjust_durations(scenes, durations, sharpness_map, 30.0)

        assert result[0] == 2.0  # min_clip_duration
        assert scale is None

    def test_sharp_scene_keeps_original(self):
        """Scenes with sharpness >= sharp_threshold keep original duration."""
        adjuster = DurationAdjuster(config=_no_autoscale_config())
        scene = _scene()
        scenes = [scene]
        durations = [4.0]
        sharpness_map = {id(scene): 150.0}  # Above sharp_threshold of 100

        result, scale = adjuster.adjust_durations(scenes, durations, sharpness_map, 30.0)

        assert result[0] == 4.0

    def test_soft_scene_scaled_proportionally(self):
        """Scenes between soft and sharp thresholds get proportional scaling."""
        adjuster = DurationAdjuster(config=_no_autoscale_config())
        scene = _scene()
        scenes = [scene]
        base_dur = 4.0
        durations = [base_dur]
        sharpness = 65.0  # Midpoint between 30 and 100
        sharpness_map = {id(scene): sharpness}

        result, scale = adjuster.adjust_durations(scenes, durations, sharpness_map, 30.0)

        # Expected: min + (base - min) * (65 - 30) / (100 - 30)
        expected_scale = (sharpness - 30.0) / (100.0 - 30.0)
        expected = 2.0 + (base_dur - 2.0) * expected_scale
        assert result[0] == pytest.approx(expected, abs=0.01)

    def test_missing_sharpness_defaults_to_100(self):
        """Missing sharpness value defaults to 100 (sharp_threshold), keeping duration."""
        adjuster = DurationAdjuster(config=_no_autoscale_config())
        scene = _scene()
        scenes = [scene]
        durations = [4.0]
        sharpness_map = {}  # No entry for this scene

        result, _ = adjuster.adjust_durations(scenes, durations, sharpness_map, 30.0)

        # Default 100.0 == sharp_threshold, so no scaling
        assert result[0] == 4.0

    def test_exactly_at_soft_threshold(self):
        """Sharpness exactly at soft_threshold gets min scaling."""
        adjuster = DurationAdjuster(config=_no_autoscale_config())
        scene = _scene()
        scenes = [scene]
        durations = [4.0]
        sharpness_map = {id(scene): 30.0}  # Exactly at soft_threshold

        result, _ = adjuster.adjust_durations(scenes, durations, sharpness_map, 30.0)

        # scale = (30 - 30) / (100 - 30) = 0, so adjusted = 2.0 + 0 = 2.0
        assert result[0] == 2.0

    def test_exactly_at_sharp_threshold(self):
        """Sharpness exactly at sharp_threshold keeps full duration."""
        adjuster = DurationAdjuster(config=_no_autoscale_config())
        scene = _scene()
        scenes = [scene]
        durations = [4.0]
        sharpness_map = {id(scene): 100.0}  # Exactly at sharp_threshold

        result, _ = adjuster.adjust_durations(scenes, durations, sharpness_map, 30.0)

        # scale = (100 - 30) / (100 - 30) = 1.0, so adjusted = 2.0 + 2.0*1.0 = 4.0
        assert result[0] == 4.0


class TestDurationAdjusterHookTier:
    """Tests for hook tier based duration adjustment."""

    def test_maximum_hook_gets_minimum_showcase(self):
        """MAXIMUM hook tier with decent sharpness gets at least 3.0s."""
        adjuster = DurationAdjuster(config=_no_autoscale_config())
        scene = _enhanced_scene(
            hook_tier=HookPotential.MAXIMUM,
            motion_type=MotionType.PAN_LEFT,  # Non-static to isolate hook logic
        )
        scenes = [scene]
        durations = [2.5]
        sharpness_map = {id(scene): 100.0}  # Sharp enough

        result, _ = adjuster.adjust_durations(scenes, durations, sharpness_map, 30.0)

        assert result[0] >= 3.0

    def test_high_hook_gets_minimum_showcase(self):
        """HIGH hook tier with decent sharpness gets at least 3.0s."""
        adjuster = DurationAdjuster(config=_no_autoscale_config())
        scene = _enhanced_scene(
            hook_tier=HookPotential.HIGH,
            motion_type=MotionType.PAN_LEFT,  # Non-static to isolate hook logic
        )
        scenes = [scene]
        durations = [2.5]
        sharpness_map = {id(scene): 100.0}

        result, _ = adjuster.adjust_durations(scenes, durations, sharpness_map, 30.0)

        assert result[0] >= 3.0

    def test_high_hook_blurry_no_showcase_boost(self):
        """HIGH hook tier with low sharpness does NOT get showcase boost."""
        adjuster = DurationAdjuster(config=_no_autoscale_config())
        scene = _enhanced_scene(
            hook_tier=HookPotential.HIGH,
            motion_type=MotionType.PAN_LEFT,
        )
        scenes = [scene]
        durations = [2.5]
        sharpness_map = {id(scene): 20.0}  # Below soft_threshold

        result, _ = adjuster.adjust_durations(scenes, durations, sharpness_map, 30.0)

        # Should get min_clip_duration instead of showcase boost
        assert result[0] == 2.0

    def test_low_hook_capped_short_reel(self):
        """LOW hook tier capped at 2.0 for short reels (<=15s)."""
        adjuster = DurationAdjuster(config=_no_autoscale_config())
        scene = _enhanced_scene(
            hook_tier=HookPotential.LOW,
            motion_type=MotionType.PAN_LEFT,  # Non-static to isolate hook logic
        )
        scenes = [scene]
        durations = [4.0]
        sharpness_map = {id(scene): 150.0}

        result, _ = adjuster.adjust_durations(scenes, durations, sharpness_map, 15.0)

        assert result[0] == 2.0

    def test_low_hook_capped_long_reel(self):
        """LOW hook tier capped at 3.0 for longer reels (>15s)."""
        adjuster = DurationAdjuster(config=_no_autoscale_config())
        scene = _enhanced_scene(
            hook_tier=HookPotential.LOW,
            motion_type=MotionType.PAN_LEFT,  # Non-static to isolate hook logic
        )
        scenes = [scene]
        durations = [4.0]
        sharpness_map = {id(scene): 150.0}

        result, _ = adjuster.adjust_durations(scenes, durations, sharpness_map, 30.0)

        assert result[0] == 3.0

    def test_poor_hook_capped_short_reel(self):
        """POOR hook tier capped at 2.0 for short reels (<=15s)."""
        adjuster = DurationAdjuster(config=_no_autoscale_config())
        scene = _enhanced_scene(
            hook_tier=HookPotential.POOR,
            motion_type=MotionType.PAN_LEFT,  # Non-static to isolate hook logic
        )
        scenes = [scene]
        durations = [4.0]
        sharpness_map = {id(scene): 150.0}

        result, _ = adjuster.adjust_durations(scenes, durations, sharpness_map, 15.0)

        assert result[0] == 2.0

    def test_poor_hook_capped_long_reel(self):
        """POOR hook tier capped at 3.0 for longer reels (>15s)."""
        adjuster = DurationAdjuster(config=_no_autoscale_config())
        scene = _enhanced_scene(
            hook_tier=HookPotential.POOR,
            motion_type=MotionType.PAN_LEFT,  # Non-static to isolate hook logic
        )
        scenes = [scene]
        durations = [4.0]
        sharpness_map = {id(scene): 150.0}

        result, _ = adjuster.adjust_durations(scenes, durations, sharpness_map, 30.0)

        assert result[0] == 3.0

    def test_medium_hook_no_special_treatment(self):
        """MEDIUM hook tier gets no special cap or boost."""
        adjuster = DurationAdjuster(config=_no_autoscale_config())
        scene = _enhanced_scene(
            hook_tier=HookPotential.MEDIUM,
            motion_type=MotionType.PAN_LEFT,
        )
        scenes = [scene]
        durations = [4.0]
        sharpness_map = {id(scene): 150.0}

        result, _ = adjuster.adjust_durations(scenes, durations, sharpness_map, 30.0)

        # No cap, no boost, sharp -> keeps original
        assert result[0] == 4.0


class TestDurationAdjusterMotionType:
    """Tests for motion-type based capping."""

    def test_static_capped_short_reel(self):
        """STATIC motion type capped at 2.5 for short reels (<=15s)."""
        adjuster = DurationAdjuster(config=_no_autoscale_config())
        scene = _enhanced_scene(motion_type=MotionType.STATIC)
        scenes = [scene]
        durations = [4.0]
        sharpness_map = {id(scene): 150.0}

        result, _ = adjuster.adjust_durations(scenes, durations, sharpness_map, 15.0)

        assert result[0] == 2.5

    def test_static_capped_long_reel(self):
        """STATIC motion type capped at 3.5 for longer reels (>15s)."""
        adjuster = DurationAdjuster(config=_no_autoscale_config())
        scene = _enhanced_scene(motion_type=MotionType.STATIC)
        scenes = [scene]
        durations = [4.0]
        sharpness_map = {id(scene): 150.0}

        result, _ = adjuster.adjust_durations(scenes, durations, sharpness_map, 30.0)

        assert result[0] == 3.5

    def test_non_static_not_capped(self):
        """Non-STATIC motion types are not subject to static cap."""
        adjuster = DurationAdjuster(config=_no_autoscale_config())
        scene = _enhanced_scene(motion_type=MotionType.PAN_LEFT)
        scenes = [scene]
        durations = [4.0]
        sharpness_map = {id(scene): 150.0}

        result, _ = adjuster.adjust_durations(scenes, durations, sharpness_map, 30.0)

        assert result[0] == 4.0

    def test_static_and_low_hook_both_apply(self):
        """Both static cap and low hook cap apply; most restrictive wins."""
        adjuster = DurationAdjuster(config=_no_autoscale_config())
        scene = _enhanced_scene(
            motion_type=MotionType.STATIC,
            hook_tier=HookPotential.LOW,
        )
        scenes = [scene]
        durations = [4.0]
        sharpness_map = {id(scene): 150.0}

        result, _ = adjuster.adjust_durations(scenes, durations, sharpness_map, 15.0)

        # LOW cap = 2.0, STATIC cap = 2.5 => min is 2.0, but STATIC applied second
        # LOW cap makes it 2.0, STATIC cap min(2.0, 2.5) = 2.0
        assert result[0] == 2.0

    def test_unknown_motion_not_capped(self):
        """UNKNOWN motion type is not subject to static cap."""
        adjuster = DurationAdjuster(config=_no_autoscale_config())
        scene = _enhanced_scene(motion_type=MotionType.UNKNOWN)
        scenes = [scene]
        durations = [4.0]
        sharpness_map = {id(scene): 150.0}

        result, _ = adjuster.adjust_durations(scenes, durations, sharpness_map, 30.0)

        assert result[0] == 4.0


class TestDurationAdjusterAutoScale:
    """Tests for auto-scaling when total is below target."""

    def test_no_scale_when_close_to_target(self):
        """No auto-scale when total is >= 85% of target."""
        adjuster = DurationAdjuster()
        scenes = [_scene() for _ in range(5)]
        durations = [3.5] * 5  # Total = 17.5
        sharpness_map = {id(s): 150.0 for s in scenes}

        result, scale = adjuster.adjust_durations(scenes, durations, sharpness_map, 20.0)

        # 17.5 / 20 = 0.875 >= 0.85, so no scale
        assert scale is None

    def test_scale_when_significantly_short(self):
        """Auto-scale applied when total < 85% of target."""
        adjuster = DurationAdjuster()
        scenes = [_scene() for _ in range(3)]
        durations = [2.0] * 3  # Total = 6.0
        sharpness_map = {id(s): 150.0 for s in scenes}
        target = 30.0

        result, scale = adjuster.adjust_durations(scenes, durations, sharpness_map, target)

        # 6.0 / 30 = 0.2 < 0.85, so scale = min(30/6, 1.5) = 1.5
        assert scale is not None
        assert scale == pytest.approx(1.5, abs=0.01)

    def test_scale_capped_at_max(self):
        """Auto-scale capped at auto_scale_max (1.5)."""
        adjuster = DurationAdjuster()
        scenes = [_scene()]
        durations = [2.0]  # Total = 2.0
        sharpness_map = {id(scenes[0]): 150.0}
        target = 30.0

        _, scale = adjuster.adjust_durations(scenes, durations, sharpness_map, target)

        # 30 / 2 = 15, capped to 1.5
        assert scale == pytest.approx(1.5, abs=0.01)

    def test_scaled_durations_capped_at_max_clip(self):
        """Scaled durations are capped at max_clip_duration."""
        adjuster = DurationAdjuster()
        scenes = [_scene() for _ in range(2)]
        durations = [4.0, 4.0]  # Total = 8.0
        sharpness_map = {id(s): 150.0 for s in scenes}
        target = 30.0  # max_clip_duration = 5.0

        result, scale = adjuster.adjust_durations(scenes, durations, sharpness_map, target)

        assert scale is not None
        for d in result:
            assert d <= 5.0  # max_clip_duration for target 30

    def test_returns_none_scale_when_adequate(self):
        """Returns (durations, None) when no auto-scale needed."""
        adjuster = DurationAdjuster()
        scenes = [_scene() for _ in range(10)]
        durations = [3.0] * 10  # Total = 30.0
        sharpness_map = {id(s): 150.0 for s in scenes}

        result, scale = adjuster.adjust_durations(scenes, durations, sharpness_map, 30.0)

        assert scale is None
        assert len(result) == 10

    def test_moderate_scale_factor(self):
        """Auto-scale with moderate factor (not capped)."""
        adjuster = DurationAdjuster()
        scenes = [_scene() for _ in range(5)]
        durations = [3.0] * 5  # Total = 15.0
        sharpness_map = {id(s): 150.0 for s in scenes}
        target = 20.0  # 15/20 = 0.75 < 0.85

        result, scale = adjuster.adjust_durations(scenes, durations, sharpness_map, target)

        assert scale is not None
        assert scale == pytest.approx(20.0 / 15.0, abs=0.01)


class TestDurationAdjusterGlobalLimits:
    """Tests for global minimum and maximum enforcement."""

    def test_never_below_min_clip_duration(self):
        """No duration should ever go below min_clip_duration."""
        adjuster = DurationAdjuster(config=_no_autoscale_config())
        scene = _enhanced_scene(hook_tier=HookPotential.POOR)
        scenes = [scene]
        durations = [1.0]  # Below min
        sharpness_map = {id(scene): 10.0}  # Very blurry

        result, _ = adjuster.adjust_durations(scenes, durations, sharpness_map, 30.0)

        assert result[0] >= 2.0

    def test_never_above_max_clip_duration(self):
        """No duration should exceed max_clip_duration for the target."""
        adjuster = DurationAdjuster(config=_no_autoscale_config())
        scene = _enhanced_scene(hook_tier=HookPotential.MAXIMUM)
        scenes = [scene]
        durations = [10.0]  # Very long
        sharpness_map = {id(scene): 200.0}  # Very sharp

        result, _ = adjuster.adjust_durations(scenes, durations, sharpness_map, 15.0)

        assert result[0] <= 4.0  # max_clip_duration for <=15

    def test_basic_scene_info_skips_hook_and_motion(self):
        """Basic SceneInfo (non-enhanced) skips hook/motion adjustments."""
        adjuster = DurationAdjuster(config=_no_autoscale_config())
        scene = _scene()  # Not EnhancedSceneInfo
        scenes = [scene]
        durations = [4.0]
        sharpness_map = {id(scene): 150.0}

        result, _ = adjuster.adjust_durations(scenes, durations, sharpness_map, 30.0)

        # Should keep original since sharp enough and no enhanced adjustments
        assert result[0] == 4.0

    def test_max_clip_for_short_reel(self):
        """Max clip for target <= 15s is 4.0."""
        adjuster = DurationAdjuster(config=_no_autoscale_config())
        scene = _scene()
        scenes = [scene]
        durations = [5.0]
        sharpness_map = {id(scene): 150.0}

        result, _ = adjuster.adjust_durations(scenes, durations, sharpness_map, 10.0)

        assert result[0] == 4.0

    def test_max_clip_for_long_reel(self):
        """Max clip for target > 30s is 6.0."""
        adjuster = DurationAdjuster(config=_no_autoscale_config())
        scene = _scene()
        scenes = [scene]
        durations = [8.0]
        sharpness_map = {id(scene): 150.0}

        result, _ = adjuster.adjust_durations(scenes, durations, sharpness_map, 60.0)

        assert result[0] == 6.0


class TestDurationAdjusterMultipleScenes:
    """Tests with multiple scenes."""

    def test_multiple_scenes_independent_adjustment(self):
        """Each scene is adjusted independently."""
        adjuster = DurationAdjuster(config=_no_autoscale_config())
        s1 = _enhanced_scene(
            hook_tier=HookPotential.HIGH,
            motion_type=MotionType.PAN_LEFT,
        )
        s2 = _enhanced_scene(
            hook_tier=HookPotential.POOR,
            motion_type=MotionType.PAN_LEFT,
        )
        scenes = [s1, s2]
        durations = [3.0, 3.0]
        sharpness_map = {id(s1): 150.0, id(s2): 150.0}

        result, _ = adjuster.adjust_durations(scenes, durations, sharpness_map, 30.0)

        assert result[0] >= 3.0  # HIGH hook showcase
        assert result[1] <= 3.0  # POOR hook capped

    def test_result_length_matches_input(self):
        """Output list has same length as input."""
        adjuster = DurationAdjuster(config=_no_autoscale_config())
        scenes = [_scene() for _ in range(7)]
        durations = [3.0] * 7
        sharpness_map = {id(s): 100.0 for s in scenes}

        result, _ = adjuster.adjust_durations(scenes, durations, sharpness_map, 30.0)

        assert len(result) == 7

    def test_mixed_sharpness_and_hooks(self):
        """Multiple scenes with varying sharpness and hooks are all adjusted."""
        adjuster = DurationAdjuster(config=_no_autoscale_config())
        s1 = _enhanced_scene(hook_tier=HookPotential.MAXIMUM, motion_type=MotionType.PAN_LEFT)
        s2 = _enhanced_scene(hook_tier=HookPotential.POOR, motion_type=MotionType.STATIC)
        s3 = _scene()
        scenes = [s1, s2, s3]
        durations = [4.0, 4.0, 4.0]
        sharpness_map = {
            id(s1): 150.0,  # Sharp, MAXIMUM hook -> showcase boost
            id(s2): 150.0,  # Sharp, POOR hook + STATIC -> capped
            id(s3): 20.0,   # Blurry -> min_clip_duration
        }

        result, _ = adjuster.adjust_durations(scenes, durations, sharpness_map, 30.0)

        assert result[0] >= 3.0   # MAXIMUM showcase
        assert result[1] <= 3.5   # STATIC cap (3.5 for >15s)
        assert result[2] == 2.0   # Blurry -> min


# ===========================================================================
# scale_for_fewer_scenes tests
# ===========================================================================


class TestScaleForFewerScenes:
    """Tests for scale_for_fewer_scenes method."""

    def test_scales_up_correctly(self):
        """Scales durations up when fewer scenes available."""
        adjuster = DurationAdjuster()
        clip_durations = [2.0, 3.0]  # Total = 5.0
        original_total = 10.0

        scaled, factor = adjuster.scale_for_fewer_scenes(clip_durations, original_total)

        assert factor == pytest.approx(2.0, abs=0.01)
        assert scaled[0] == pytest.approx(4.0, abs=0.01)
        assert scaled[1] == pytest.approx(6.0, abs=0.01)

    def test_respects_max_scale(self):
        """Scale factor is capped at max_scale."""
        adjuster = DurationAdjuster()
        clip_durations = [1.0]  # Total = 1.0
        original_total = 30.0

        scaled, factor = adjuster.scale_for_fewer_scenes(clip_durations, original_total, max_scale=2.5)

        assert factor == pytest.approx(2.5, abs=0.01)
        assert scaled[0] == pytest.approx(2.5, abs=0.01)

    def test_no_scale_when_already_sufficient(self):
        """No scaling when current total >= original total."""
        adjuster = DurationAdjuster()
        clip_durations = [5.0, 5.0]  # Total = 10.0
        original_total = 8.0

        scaled, factor = adjuster.scale_for_fewer_scenes(clip_durations, original_total)

        assert factor == 1.0
        assert scaled == clip_durations

    def test_no_scale_when_equal(self):
        """No scaling when current total equals original total."""
        adjuster = DurationAdjuster()
        clip_durations = [3.0, 3.0]  # Total = 6.0

        scaled, factor = adjuster.scale_for_fewer_scenes(clip_durations, 6.0)

        assert factor == 1.0

    def test_zero_total_returns_unchanged(self):
        """Zero total durations returns unchanged list."""
        adjuster = DurationAdjuster()
        clip_durations = [0.0, 0.0]

        scaled, factor = adjuster.scale_for_fewer_scenes(clip_durations, 10.0)

        assert factor == 1.0
        assert scaled == [0.0, 0.0]

    def test_empty_list(self):
        """Empty list returns empty list with factor 1.0."""
        adjuster = DurationAdjuster()

        scaled, factor = adjuster.scale_for_fewer_scenes([], 10.0)

        assert factor == 1.0
        assert scaled == []

    def test_custom_max_scale(self):
        """Custom max_scale is honored."""
        adjuster = DurationAdjuster()
        clip_durations = [2.0]
        original_total = 100.0

        _, factor = adjuster.scale_for_fewer_scenes(clip_durations, original_total, max_scale=1.5)

        assert factor == pytest.approx(1.5, abs=0.01)

    def test_preserves_relative_proportions(self):
        """Scaled durations preserve relative proportions."""
        adjuster = DurationAdjuster()
        clip_durations = [2.0, 4.0]  # 1:2 ratio
        original_total = 12.0

        scaled, factor = adjuster.scale_for_fewer_scenes(clip_durations, original_total)

        assert factor == pytest.approx(2.0, abs=0.01)
        # Ratio should still be 1:2
        assert scaled[1] / scaled[0] == pytest.approx(2.0, abs=0.01)


# ===========================================================================
# DurationAdjuster initialization
# ===========================================================================


class TestDurationAdjusterInit:
    """Tests for DurationAdjuster initialization."""

    def test_default_config(self):
        adjuster = DurationAdjuster()
        assert adjuster.config.min_clip_duration == 2.0

    def test_custom_config(self):
        cfg = DurationConfig(min_clip_duration=1.0, auto_scale_max=2.0)
        adjuster = DurationAdjuster(config=cfg)
        assert adjuster.config.min_clip_duration == 1.0
        assert adjuster.config.auto_scale_max == 2.0

    def test_none_config_uses_defaults(self):
        adjuster = DurationAdjuster(config=None)
        assert adjuster.config.min_clip_duration == 2.0
        assert adjuster.config.sharp_threshold == 100.0


# ===========================================================================
# compute_adaptive_durations tests
# ===========================================================================


def _enhanced(hook_tier: HookPotential) -> EnhancedSceneInfo:
    """Create an EnhancedSceneInfo with the given hook_tier."""
    return EnhancedSceneInfo(
        start_time=0.0,
        end_time=5.0,
        duration=5.0,
        score=70.0,
        source_file=Path("clip.mp4"),
        hook_tier=hook_tier,
    )


class TestComputeAdaptiveDurations:
    """Tests for DurationAdjuster.compute_adaptive_durations()."""

    def test_empty_scenes_returns_empty(self):
        adjuster = DurationAdjuster()
        result = adjuster.compute_adaptive_durations([], 30.0)
        assert result == []

    def test_output_length_matches_input(self):
        adjuster = DurationAdjuster()
        scenes = [_enhanced(HookPotential.HIGH) for _ in range(5)]
        result = adjuster.compute_adaptive_durations(scenes, 30.0)
        assert len(result) == 5

    def test_no_duration_below_minimum(self):
        """Every clip must be at least 1.5 seconds."""
        adjuster = DurationAdjuster()
        scenes = [_enhanced(HookPotential.POOR) for _ in range(25)]
        result = adjuster.compute_adaptive_durations(scenes, 30.0)
        assert all(d >= 1.5 for d in result), f"Some clips below 1.5s: {result}"

    def test_maximum_hook_gets_longer_than_poor(self):
        """MAXIMUM hook scenes should receive more time than POOR hook scenes."""
        adjuster = DurationAdjuster()
        scenes_max = [_enhanced(HookPotential.MAXIMUM) for _ in range(5)]
        scenes_poor = [_enhanced(HookPotential.POOR) for _ in range(5)]
        dur_max = adjuster.compute_adaptive_durations(scenes_max, 30.0)
        dur_poor = adjuster.compute_adaptive_durations(scenes_poor, 30.0)
        assert sum(dur_max) >= sum(dur_poor)

    def test_sum_approximates_target_mixed(self):
        """Total duration should be close to target for a mixed set."""
        adjuster = DurationAdjuster()
        scenes = [
            _enhanced(HookPotential.MAXIMUM),
            _enhanced(HookPotential.HIGH),
            _enhanced(HookPotential.MEDIUM),
            _enhanced(HookPotential.LOW),
            _enhanced(HookPotential.POOR),
        ]
        target = 15.0
        result = adjuster.compute_adaptive_durations(scenes, target)
        total = sum(result)
        # Allow tolerance of ±10% or minimum clip enforcement drift
        assert abs(total - target) / target < 0.15, f"Total {total:.2f} far from {target}"

    def test_sum_approximates_target_uniform(self):
        """Uniform tier: total should closely match target."""
        adjuster = DurationAdjuster()
        scenes = [_enhanced(HookPotential.MEDIUM) for _ in range(8)]
        target = 30.0
        result = adjuster.compute_adaptive_durations(scenes, target)
        total = sum(result)
        assert abs(total - target) / target < 0.15, f"Total {total:.2f} far from {target}"

    def test_high_tier_clips_longer_than_low_in_mixed_set(self):
        """In a mixed set, HIGH tier clips should be longer than LOW tier clips."""
        adjuster = DurationAdjuster()
        s_high = _enhanced(HookPotential.HIGH)
        s_low = _enhanced(HookPotential.LOW)
        result = adjuster.compute_adaptive_durations([s_high, s_low], 30.0)
        assert result[0] >= result[1], f"HIGH ({result[0]:.2f}) should >= LOW ({result[1]:.2f})"

    def test_30s_reel_target_clip_count(self):
        """For a 30s target, 8-10 clips at 1.5-4s each should be achievable."""
        adjuster = DurationAdjuster()
        # 9 scenes of mixed quality
        scenes = [
            _enhanced(HookPotential.MAXIMUM),
            _enhanced(HookPotential.HIGH),
            _enhanced(HookPotential.HIGH),
            _enhanced(HookPotential.MEDIUM),
            _enhanced(HookPotential.MEDIUM),
            _enhanced(HookPotential.MEDIUM),
            _enhanced(HookPotential.LOW),
            _enhanced(HookPotential.LOW),
            _enhanced(HookPotential.POOR),
        ]
        result = adjuster.compute_adaptive_durations(scenes, 30.0)
        assert len(result) == 9
        for d in result:
            assert 1.5 <= d <= 4.5, f"Clip duration {d:.2f} out of expected range"
