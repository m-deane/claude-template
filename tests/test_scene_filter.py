"""Tests for scene_filter module."""

from pathlib import Path

from drone_reel.core.scene_detector import EnhancedSceneInfo, MotionType, SceneInfo
from drone_reel.core.scene_filter import FilterResult, FilterThresholds, SceneFilter

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_scene(start=0.0, end=2.0, score=50.0, source="clip.mp4"):
    """Create a basic SceneInfo for testing."""
    return SceneInfo(
        start_time=start,
        end_time=end,
        duration=end - start,
        score=score,
        source_file=Path(source),
    )


def _make_enhanced(
    start=0.0,
    end=2.0,
    score=50.0,
    source="clip.mp4",
    subject_score=0.0,
    motion_type=MotionType.UNKNOWN,
):
    """Create an EnhancedSceneInfo for testing."""
    return EnhancedSceneInfo(
        start_time=start,
        end_time=end,
        duration=end - start,
        score=score,
        source_file=Path(source),
        subject_score=subject_score,
        motion_type=motion_type,
    )


# ===========================================================================
# FilterThresholds
# ===========================================================================

class TestFilterThresholds:
    """Tests for FilterThresholds default values."""

    def test_default_min_motion_energy(self):
        t = FilterThresholds()
        assert t.min_motion_energy == 25.0

    def test_default_ideal_motion_energy(self):
        t = FilterThresholds()
        assert t.ideal_motion_energy == 45.0

    def test_default_min_brightness(self):
        t = FilterThresholds()
        assert t.min_brightness == 30.0

    def test_default_max_brightness(self):
        t = FilterThresholds()
        assert t.max_brightness == 245.0

    def test_default_max_shake_score(self):
        t = FilterThresholds()
        assert t.max_shake_score == 40.0

    def test_default_subject_score_threshold(self):
        t = FilterThresholds()
        assert t.subject_score_threshold == 0.6

    def test_custom_thresholds(self):
        t = FilterThresholds(
            min_motion_energy=10.0,
            ideal_motion_energy=30.0,
            min_brightness=50.0,
            max_brightness=200.0,
            max_shake_score=20.0,
            subject_score_threshold=0.8,
        )
        assert t.min_motion_energy == 10.0
        assert t.ideal_motion_energy == 30.0
        assert t.min_brightness == 50.0
        assert t.max_brightness == 200.0
        assert t.max_shake_score == 20.0
        assert t.subject_score_threshold == 0.8


# ===========================================================================
# FilterResult
# ===========================================================================

class TestFilterResult:
    """Tests for FilterResult properties and methods."""

    def _make_result(self, high_subject=None, high_motion=None, medium_motion=None, low_motion=None):
        return FilterResult(
            high_subject_scenes=high_subject or [],
            high_motion_scenes=high_motion or [],
            medium_motion_scenes=medium_motion or [],
            low_motion_scenes=low_motion or [],
            dark_scenes_filtered=0,
            shaky_scenes_filtered=0,
        )

    def test_prioritized_returns_high_subject_high_motion_medium_motion(self):
        s1 = _make_scene(0, 1)
        s2 = _make_scene(1, 2)
        s3 = _make_scene(2, 3)
        s4 = _make_scene(3, 4)

        result = self._make_result(
            high_subject=[s1],
            high_motion=[s2],
            medium_motion=[s3],
            low_motion=[s4],
        )

        assert result.prioritized == [s1, s2, s3]
        assert s4 not in result.prioritized

    def test_prioritized_order_is_high_subject_first(self):
        s1 = _make_scene(0, 1)
        s2 = _make_scene(1, 2)
        s3 = _make_scene(2, 3)

        result = self._make_result(
            high_subject=[s1],
            high_motion=[s2],
            medium_motion=[s3],
        )

        assert result.prioritized[0] is s1
        assert result.prioritized[1] is s2
        assert result.prioritized[2] is s3

    def test_prioritized_empty_when_all_tiers_empty(self):
        result = self._make_result()
        assert result.prioritized == []

    def test_all_passing_includes_low_motion(self):
        s1 = _make_scene(0, 1)
        s2 = _make_scene(1, 2)

        result = self._make_result(
            high_motion=[s1],
            low_motion=[s2],
        )

        assert s1 in result.all_passing
        assert s2 in result.all_passing

    def test_all_passing_equals_prioritized_plus_low_motion(self):
        s1 = _make_scene(0, 1)
        s2 = _make_scene(1, 2)
        s3 = _make_scene(2, 3)
        s4 = _make_scene(3, 4)

        result = self._make_result(
            high_subject=[s1],
            high_motion=[s2],
            medium_motion=[s3],
            low_motion=[s4],
        )

        assert result.all_passing == result.prioritized + [s4]

    def test_all_passing_empty_when_all_empty(self):
        result = self._make_result()
        assert result.all_passing == []

    def test_with_low_motion_if_needed_returns_prioritized_when_enough(self):
        s1 = _make_scene(0, 1)
        s2 = _make_scene(1, 2)
        s3 = _make_scene(2, 3)

        result = self._make_result(
            high_subject=[s1],
            high_motion=[s2],
            low_motion=[s3],
        )

        # min_count=2, prioritized has 2, so low_motion not needed
        scenes = result.with_low_motion_if_needed(min_count=2)
        assert len(scenes) == 2
        assert s3 not in scenes

    def test_with_low_motion_if_needed_adds_low_when_short(self):
        s1 = _make_scene(0, 1)
        s2 = _make_scene(1, 2)

        result = self._make_result(
            high_motion=[s1],
            low_motion=[s2],
        )

        # min_count=3, prioritized has 1, so low_motion added
        scenes = result.with_low_motion_if_needed(min_count=3)
        assert s1 in scenes
        assert s2 in scenes

    def test_with_low_motion_if_needed_exact_boundary(self):
        """When prioritized count == min_count, low_motion is NOT added."""
        s1 = _make_scene(0, 1)
        s2 = _make_scene(1, 2)

        result = self._make_result(
            high_motion=[s1],
            low_motion=[s2],
        )

        scenes = result.with_low_motion_if_needed(min_count=1)
        assert len(scenes) == 1
        assert s2 not in scenes

    def test_with_low_motion_if_needed_zero_min_count(self):
        s1 = _make_scene(0, 1)
        result = self._make_result(low_motion=[s1])

        scenes = result.with_low_motion_if_needed(min_count=0)
        assert scenes == []

    def test_with_low_motion_if_needed_empty_result(self):
        result = self._make_result()
        scenes = result.with_low_motion_if_needed(min_count=5)
        assert scenes == []


# ===========================================================================
# SceneFilter
# ===========================================================================

class TestSceneFilter:
    """Tests for SceneFilter.filter_scenes()."""

    def test_default_thresholds_used_when_none_provided(self):
        sf = SceneFilter()
        assert sf.thresholds.min_motion_energy == 25.0
        assert sf.thresholds.ideal_motion_energy == 45.0

    def test_custom_thresholds_used(self):
        t = FilterThresholds(min_motion_energy=10.0)
        sf = SceneFilter(thresholds=t)
        assert sf.thresholds.min_motion_energy == 10.0

    def test_empty_input_returns_empty_result(self):
        sf = SceneFilter()
        result = sf.filter_scenes([], {}, {}, {})

        assert result.high_subject_scenes == []
        assert result.high_motion_scenes == []
        assert result.medium_motion_scenes == []
        assert result.low_motion_scenes == []
        assert result.dark_scenes_filtered == 0
        assert result.shaky_scenes_filtered == 0

    # -----------------------------------------------------------------------
    # Brightness filtering
    # -----------------------------------------------------------------------

    def test_dark_scene_filtered(self):
        scene = _make_scene()
        sid = id(scene)
        sf = SceneFilter()

        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 50.0},
            brightness_map={sid: 20.0},  # < 30
            shake_map={sid: 10.0},
        )

        assert result.dark_scenes_filtered == 1
        assert result.all_passing == []

    def test_brightness_at_lower_boundary_excluded(self):
        """brightness == 29.9 is below min_brightness=30 -> filtered."""
        scene = _make_scene()
        sid = id(scene)
        sf = SceneFilter()

        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 50.0},
            brightness_map={sid: 29.9},
            shake_map={sid: 0.0},
        )

        assert result.dark_scenes_filtered == 1

    def test_brightness_at_exact_lower_boundary_passes(self):
        """brightness == 30 is not < 30 -> passes."""
        scene = _make_enhanced(subject_score=0.0)
        sid = id(scene)
        sf = SceneFilter()

        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 50.0},
            brightness_map={sid: 30.0},
            shake_map={sid: 0.0},
        )

        assert result.dark_scenes_filtered == 0
        assert len(result.all_passing) == 1

    def test_overexposed_scene_filtered(self):
        scene = _make_scene()
        sid = id(scene)
        sf = SceneFilter()

        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 50.0},
            brightness_map={sid: 250.0},  # > 245
            shake_map={sid: 10.0},
        )

        assert result.dark_scenes_filtered == 1
        assert result.all_passing == []

    def test_brightness_at_upper_boundary_excluded(self):
        """brightness == 245.1 is above max_brightness=245 -> filtered."""
        scene = _make_scene()
        sid = id(scene)
        sf = SceneFilter()

        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 50.0},
            brightness_map={sid: 245.1},
            shake_map={sid: 0.0},
        )

        assert result.dark_scenes_filtered == 1

    def test_brightness_at_exact_upper_boundary_passes(self):
        """brightness == 245 is not > 245 -> passes."""
        scene = _make_enhanced(subject_score=0.0)
        sid = id(scene)
        sf = SceneFilter()

        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 50.0},
            brightness_map={sid: 245.0},
            shake_map={sid: 0.0},
        )

        assert result.dark_scenes_filtered == 0
        assert len(result.all_passing) == 1

    # -----------------------------------------------------------------------
    # Shake filtering
    # -----------------------------------------------------------------------

    def test_shaky_scene_filtered(self):
        scene = _make_scene()
        sid = id(scene)
        sf = SceneFilter()

        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 50.0},
            brightness_map={sid: 127.0},
            shake_map={sid: 50.0},  # > 40
        )

        assert result.shaky_scenes_filtered == 1
        assert result.all_passing == []

    def test_shake_at_exact_boundary_passes(self):
        """shake_score == 40 is not > 40 -> passes."""
        scene = _make_enhanced(subject_score=0.0)
        sid = id(scene)
        sf = SceneFilter()

        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 50.0},
            brightness_map={sid: 127.0},
            shake_map={sid: 40.0},
        )

        assert result.shaky_scenes_filtered == 0
        assert len(result.all_passing) == 1

    def test_shake_just_above_boundary_filtered(self):
        """shake_score == 40.1 is > 40 -> filtered."""
        scene = _make_scene()
        sid = id(scene)
        sf = SceneFilter()

        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 50.0},
            brightness_map={sid: 127.0},
            shake_map={sid: 40.1},
        )

        assert result.shaky_scenes_filtered == 1

    # -----------------------------------------------------------------------
    # Brightness filtering happens before shake filtering
    # -----------------------------------------------------------------------

    def test_dark_and_shaky_counted_as_dark(self):
        """Dark scenes are filtered first; shaky count should not increment."""
        scene = _make_scene()
        sid = id(scene)
        sf = SceneFilter()

        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 50.0},
            brightness_map={sid: 10.0},  # dark
            shake_map={sid: 90.0},  # also shaky
        )

        assert result.dark_scenes_filtered == 1
        assert result.shaky_scenes_filtered == 0

    # -----------------------------------------------------------------------
    # Subject score tiering
    # -----------------------------------------------------------------------

    def test_high_subject_score_goes_to_high_subject(self):
        scene = _make_enhanced(subject_score=0.7)
        sid = id(scene)
        sf = SceneFilter()

        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 80.0},  # also high motion
            brightness_map={sid: 127.0},
            shake_map={sid: 0.0},
        )

        assert scene in result.high_subject_scenes
        assert scene not in result.high_motion_scenes

    def test_subject_score_at_threshold_goes_to_high_subject(self):
        """subject_score == 0.6 is >= 0.6 -> high_subject."""
        scene = _make_enhanced(subject_score=0.6)
        sid = id(scene)
        sf = SceneFilter()

        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 80.0},
            brightness_map={sid: 127.0},
            shake_map={sid: 0.0},
        )

        assert scene in result.high_subject_scenes

    def test_subject_score_below_threshold_not_high_subject(self):
        """subject_score == 0.59 is < 0.6 -> NOT high_subject."""
        scene = _make_enhanced(subject_score=0.59)
        sid = id(scene)
        sf = SceneFilter()

        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 80.0},
            brightness_map={sid: 127.0},
            shake_map={sid: 0.0},
        )

        assert scene not in result.high_subject_scenes
        assert scene in result.high_motion_scenes

    # -----------------------------------------------------------------------
    # Motion tiering (when subject_score < threshold)
    # -----------------------------------------------------------------------

    def test_high_motion_scene_classified_correctly(self):
        """motion >= 45 -> high_motion."""
        scene = _make_enhanced(subject_score=0.0)
        sid = id(scene)
        sf = SceneFilter()

        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 60.0},
            brightness_map={sid: 127.0},
            shake_map={sid: 0.0},
        )

        assert scene in result.high_motion_scenes

    def test_motion_at_ideal_threshold_goes_to_high(self):
        """motion == 45 is >= 45 -> high_motion."""
        scene = _make_enhanced(subject_score=0.0)
        sid = id(scene)
        sf = SceneFilter()

        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 45.0},
            brightness_map={sid: 127.0},
            shake_map={sid: 0.0},
        )

        assert scene in result.high_motion_scenes

    def test_medium_motion_scene_classified_correctly(self):
        """25 <= motion < 45 -> medium_motion."""
        scene = _make_enhanced(subject_score=0.0)
        sid = id(scene)
        sf = SceneFilter()

        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 35.0},
            brightness_map={sid: 127.0},
            shake_map={sid: 0.0},
        )

        assert scene in result.medium_motion_scenes

    def test_motion_at_min_threshold_goes_to_medium(self):
        """motion == 25 is >= 25 -> medium_motion."""
        scene = _make_enhanced(subject_score=0.0)
        sid = id(scene)
        sf = SceneFilter()

        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 25.0},
            brightness_map={sid: 127.0},
            shake_map={sid: 0.0},
        )

        assert scene in result.medium_motion_scenes

    def test_low_motion_scene_classified_correctly(self):
        """motion < 25 -> low_motion."""
        scene = _make_enhanced(subject_score=0.0)
        sid = id(scene)
        sf = SceneFilter()

        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 10.0},
            brightness_map={sid: 127.0},
            shake_map={sid: 0.0},
        )

        assert scene in result.low_motion_scenes

    def test_motion_just_below_min_threshold_goes_to_low(self):
        """motion == 24.9 is < 25 -> low_motion."""
        scene = _make_enhanced(subject_score=0.0)
        sid = id(scene)
        sf = SceneFilter()

        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 24.9},
            brightness_map={sid: 127.0},
            shake_map={sid: 0.0},
        )

        assert scene in result.low_motion_scenes

    def test_zero_motion_goes_to_low(self):
        scene = _make_enhanced(subject_score=0.0)
        sid = id(scene)
        sf = SceneFilter()

        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 0.0},
            brightness_map={sid: 127.0},
            shake_map={sid: 0.0},
        )

        assert scene in result.low_motion_scenes

    # -----------------------------------------------------------------------
    # Default map values when scene ID not in maps
    # -----------------------------------------------------------------------

    def test_missing_motion_defaults_to_zero(self):
        """Scene not in motion_map gets motion=0.0 -> low_motion."""
        scene = _make_enhanced(subject_score=0.0)
        sid = id(scene)
        sf = SceneFilter()

        result = sf.filter_scenes(
            [scene],
            motion_map={},  # scene not present
            brightness_map={sid: 127.0},
            shake_map={sid: 0.0},
        )

        assert scene in result.low_motion_scenes

    def test_missing_brightness_defaults_to_127(self):
        """Scene not in brightness_map gets brightness=127.0 -> passes."""
        scene = _make_enhanced(subject_score=0.0)
        sid = id(scene)
        sf = SceneFilter()

        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 50.0},
            brightness_map={},  # defaults to 127.0
            shake_map={sid: 0.0},
        )

        assert result.dark_scenes_filtered == 0
        assert len(result.all_passing) == 1

    def test_missing_shake_defaults_to_zero(self):
        """Scene not in shake_map gets shake_score=0.0 -> passes."""
        scene = _make_enhanced(subject_score=0.0)
        sid = id(scene)
        sf = SceneFilter()

        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 50.0},
            brightness_map={sid: 127.0},
            shake_map={},  # defaults to 0.0
        )

        assert result.shaky_scenes_filtered == 0
        assert len(result.all_passing) == 1

    # -----------------------------------------------------------------------
    # SceneInfo (no subject_score attribute) handling
    # -----------------------------------------------------------------------

    def test_basic_scene_info_no_subject_score_attribute(self):
        """SceneInfo has no subject_score -> treated as 0.0 -> not high_subject."""
        scene = _make_scene()
        sid = id(scene)
        sf = SceneFilter()

        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 80.0},
            brightness_map={sid: 127.0},
            shake_map={sid: 0.0},
        )

        assert scene not in result.high_subject_scenes
        assert scene in result.high_motion_scenes

    # -----------------------------------------------------------------------
    # Multiple scenes
    # -----------------------------------------------------------------------

    def test_multiple_scenes_distributed_across_tiers(self):
        s_subject = _make_enhanced(start=0, end=1, subject_score=0.9)
        s_high = _make_enhanced(start=1, end=2, subject_score=0.0)
        s_med = _make_enhanced(start=2, end=3, subject_score=0.0)
        s_low = _make_enhanced(start=3, end=4, subject_score=0.0)
        s_dark = _make_enhanced(start=4, end=5, subject_score=0.0)
        s_shaky = _make_enhanced(start=5, end=6, subject_score=0.0)

        scenes = [s_subject, s_high, s_med, s_low, s_dark, s_shaky]

        motion_map = {
            id(s_subject): 50.0,
            id(s_high): 60.0,
            id(s_med): 30.0,
            id(s_low): 10.0,
            id(s_dark): 50.0,
            id(s_shaky): 50.0,
        }
        brightness_map = {
            id(s_subject): 127.0,
            id(s_high): 127.0,
            id(s_med): 127.0,
            id(s_low): 127.0,
            id(s_dark): 15.0,  # too dark
            id(s_shaky): 127.0,
        }
        shake_map = {
            id(s_subject): 5.0,
            id(s_high): 5.0,
            id(s_med): 5.0,
            id(s_low): 5.0,
            id(s_dark): 5.0,
            id(s_shaky): 60.0,  # too shaky
        }

        sf = SceneFilter()
        result = sf.filter_scenes(scenes, motion_map, brightness_map, shake_map)

        assert s_subject in result.high_subject_scenes
        assert s_high in result.high_motion_scenes
        assert s_med in result.medium_motion_scenes
        assert s_low in result.low_motion_scenes
        assert result.dark_scenes_filtered == 1
        assert result.shaky_scenes_filtered == 1

    def test_all_scenes_filtered_out(self):
        """When every scene fails brightness or shake, result is empty."""
        s1 = _make_scene(0, 1)
        s2 = _make_scene(1, 2)

        sf = SceneFilter()
        result = sf.filter_scenes(
            [s1, s2],
            motion_map={id(s1): 50.0, id(s2): 50.0},
            brightness_map={id(s1): 10.0, id(s2): 250.0},
            shake_map={id(s1): 0.0, id(s2): 0.0},
        )

        assert result.all_passing == []
        assert result.dark_scenes_filtered == 2

    def test_multiple_dark_scenes_counted(self):
        s1 = _make_scene(0, 1)
        s2 = _make_scene(1, 2)
        s3 = _make_scene(2, 3)

        sf = SceneFilter()
        result = sf.filter_scenes(
            [s1, s2, s3],
            motion_map={id(s1): 50.0, id(s2): 50.0, id(s3): 50.0},
            brightness_map={id(s1): 5.0, id(s2): 10.0, id(s3): 127.0},
            shake_map={id(s1): 0.0, id(s2): 0.0, id(s3): 0.0},
        )

        assert result.dark_scenes_filtered == 2

    def test_multiple_shaky_scenes_counted(self):
        s1 = _make_scene(0, 1)
        s2 = _make_scene(1, 2)
        s3 = _make_scene(2, 3)

        sf = SceneFilter()
        result = sf.filter_scenes(
            [s1, s2, s3],
            motion_map={id(s1): 50.0, id(s2): 50.0, id(s3): 50.0},
            brightness_map={id(s1): 127.0, id(s2): 127.0, id(s3): 127.0},
            shake_map={id(s1): 50.0, id(s2): 60.0, id(s3): 0.0},
        )

        assert result.shaky_scenes_filtered == 2

    # -----------------------------------------------------------------------
    # Custom thresholds
    # -----------------------------------------------------------------------

    def test_custom_brightness_thresholds(self):
        """Using custom min/max brightness changes what gets filtered."""
        scene = _make_enhanced(subject_score=0.0)
        sid = id(scene)

        # With custom thresholds, brightness=40 is below min_brightness=50
        t = FilterThresholds(min_brightness=50.0, max_brightness=200.0)
        sf = SceneFilter(thresholds=t)

        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 50.0},
            brightness_map={sid: 40.0},
            shake_map={sid: 0.0},
        )

        assert result.dark_scenes_filtered == 1

    def test_custom_shake_threshold(self):
        """Using custom max_shake_score changes what gets filtered."""
        scene = _make_enhanced(subject_score=0.0)
        sid = id(scene)

        # With max_shake_score=20, shake_score=25 is filtered
        t = FilterThresholds(max_shake_score=20.0)
        sf = SceneFilter(thresholds=t)

        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 50.0},
            brightness_map={sid: 127.0},
            shake_map={sid: 25.0},
        )

        assert result.shaky_scenes_filtered == 1

    def test_custom_motion_thresholds(self):
        """Custom min/ideal motion thresholds change tier classification."""
        scene = _make_enhanced(subject_score=0.0)
        sid = id(scene)

        # With min_motion=10, ideal_motion=30:
        # motion=25 is >= ideal(30)? No. >= min(10)? Yes -> medium
        t = FilterThresholds(min_motion_energy=10.0, ideal_motion_energy=30.0)
        sf = SceneFilter(thresholds=t)

        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 25.0},
            brightness_map={sid: 127.0},
            shake_map={sid: 0.0},
        )

        assert scene in result.medium_motion_scenes

        # motion=35 is >= ideal(30)? Yes -> high_motion
        scene2 = _make_enhanced(start=1, end=2, subject_score=0.0)
        result2 = sf.filter_scenes(
            [scene2],
            motion_map={id(scene2): 35.0},
            brightness_map={id(scene2): 127.0},
            shake_map={id(scene2): 0.0},
        )

        assert scene2 in result2.high_motion_scenes

    def test_custom_subject_score_threshold(self):
        """Custom subject_score_threshold changes high_subject classification."""
        scene = _make_enhanced(subject_score=0.7)
        sid = id(scene)

        # With threshold=0.8, subject_score=0.7 is NOT high_subject
        t = FilterThresholds(subject_score_threshold=0.8)
        sf = SceneFilter(thresholds=t)

        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 50.0},
            brightness_map={sid: 127.0},
            shake_map={sid: 0.0},
        )

        assert scene not in result.high_subject_scenes
        assert scene in result.high_motion_scenes

    # -----------------------------------------------------------------------
    # Integration: FilterResult from filter_scenes
    # -----------------------------------------------------------------------

    def test_filter_result_prioritized_integration(self):
        """Verify prioritized property works with actual filter output."""
        s1 = _make_enhanced(start=0, end=1, subject_score=0.8)
        s2 = _make_enhanced(start=1, end=2, subject_score=0.0)
        s3 = _make_enhanced(start=2, end=3, subject_score=0.0)
        s4 = _make_enhanced(start=3, end=4, subject_score=0.0)

        sf = SceneFilter()
        result = sf.filter_scenes(
            [s1, s2, s3, s4],
            motion_map={id(s1): 50.0, id(s2): 60.0, id(s3): 30.0, id(s4): 5.0},
            brightness_map={id(s1): 127.0, id(s2): 127.0, id(s3): 127.0, id(s4): 127.0},
            shake_map={id(s1): 0.0, id(s2): 0.0, id(s3): 0.0, id(s4): 0.0},
        )

        prioritized = result.prioritized
        assert s1 in prioritized  # high_subject
        assert s2 in prioritized  # high_motion
        assert s3 in prioritized  # medium_motion
        assert s4 not in prioritized  # low_motion
        assert len(prioritized) == 3

    def test_filter_result_with_low_motion_if_needed_integration(self):
        """Verify with_low_motion_if_needed works with actual filter output."""
        s1 = _make_enhanced(start=0, end=1, subject_score=0.0)
        s2 = _make_enhanced(start=1, end=2, subject_score=0.0)

        sf = SceneFilter()
        result = sf.filter_scenes(
            [s1, s2],
            motion_map={id(s1): 50.0, id(s2): 5.0},
            brightness_map={id(s1): 127.0, id(s2): 127.0},
            shake_map={id(s1): 0.0, id(s2): 0.0},
        )

        # prioritized has 1 (s1 in high_motion), min_count=2 triggers adding low
        scenes = result.with_low_motion_if_needed(min_count=2)
        assert s1 in scenes
        assert s2 in scenes

    # -----------------------------------------------------------------------
    # Edge cases
    # -----------------------------------------------------------------------

    def test_subject_score_takes_priority_over_motion(self):
        """A scene with high subject AND high motion goes to high_subject only."""
        scene = _make_enhanced(subject_score=0.9)
        sid = id(scene)
        sf = SceneFilter()

        result = sf.filter_scenes(
            [scene],
            motion_map={sid: 99.0},
            brightness_map={sid: 127.0},
            shake_map={sid: 0.0},
        )

        assert scene in result.high_subject_scenes
        assert scene not in result.high_motion_scenes
        assert scene not in result.medium_motion_scenes
        assert scene not in result.low_motion_scenes

    def test_scene_appears_in_exactly_one_tier(self):
        """Each scene should appear in only one tier list."""
        scenes = [
            _make_enhanced(start=i, end=i + 1, subject_score=0.0)
            for i in range(10)
        ]

        sf = SceneFilter()
        motion_map = {id(s): float(i * 10) for i, s in enumerate(scenes)}
        brightness_map = {id(s): 127.0 for s in scenes}
        shake_map = {id(s): 0.0 for s in scenes}

        result = sf.filter_scenes(scenes, motion_map, brightness_map, shake_map)

        all_tiered = (
            result.high_subject_scenes
            + result.high_motion_scenes
            + result.medium_motion_scenes
            + result.low_motion_scenes
        )

        # Each passing scene appears exactly once
        assert len(all_tiered) == len(set(id(s) for s in all_tiered))

    def test_scene_count_conservation(self):
        """Total scenes = tiered + dark_filtered + shaky_filtered."""
        s1 = _make_enhanced(start=0, end=1, subject_score=0.0)
        s2 = _make_enhanced(start=1, end=2, subject_score=0.0)
        s3 = _make_enhanced(start=2, end=3, subject_score=0.0)
        s4 = _make_enhanced(start=3, end=4, subject_score=0.0)

        sf = SceneFilter()
        scenes = [s1, s2, s3, s4]
        result = sf.filter_scenes(
            scenes,
            motion_map={id(s1): 50.0, id(s2): 30.0, id(s3): 10.0, id(s4): 50.0},
            brightness_map={id(s1): 127.0, id(s2): 127.0, id(s3): 127.0, id(s4): 5.0},
            shake_map={id(s1): 0.0, id(s2): 0.0, id(s3): 50.0, id(s4): 0.0},
        )

        total_tiered = len(result.all_passing)
        total_filtered = result.dark_scenes_filtered + result.shaky_scenes_filtered

        assert total_tiered + total_filtered == len(scenes)
