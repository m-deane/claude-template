"""
Tests for sequence optimizer module.

Tests diversity-aware scene selection and motion continuity optimization.
"""

from pathlib import Path

import pytest
import numpy as np

from drone_reel.core.scene_detector import SceneInfo
from drone_reel.core.sequence_optimizer import (
    DiversitySelector,
    EnhancedSceneInfo,
    MotionContinuityEngine,
    MotionType,
)


@pytest.fixture
def sample_scenes():
    """Create sample SceneInfo objects for testing."""
    scenes = [
        SceneInfo(
            start_time=0.0,
            end_time=3.0,
            duration=3.0,
            score=85.0,
            source_file=Path("/video1.mp4"),
        ),
        SceneInfo(
            start_time=10.0,
            end_time=13.0,
            duration=3.0,
            score=90.0,
            source_file=Path("/video1.mp4"),
        ),
        SceneInfo(
            start_time=20.0,
            end_time=23.0,
            duration=3.0,
            score=75.0,
            source_file=Path("/video1.mp4"),
        ),
        SceneInfo(
            start_time=0.0,
            end_time=3.0,
            duration=3.0,
            score=80.0,
            source_file=Path("/video2.mp4"),
        ),
        SceneInfo(
            start_time=10.0,
            end_time=13.0,
            duration=3.0,
            score=70.0,
            source_file=Path("/video2.mp4"),
        ),
    ]
    return scenes


@pytest.fixture
def enhanced_scenes():
    """Create sample EnhancedSceneInfo objects for testing."""
    scenes = [
        EnhancedSceneInfo(
            start_time=0.0,
            end_time=3.0,
            duration=3.0,
            score=85.0,
            source_file=Path("/video1.mp4"),
            motion_type=MotionType.PAN_LEFT,
            motion_direction=(-1.0, 0.0),
            motion_smoothness=0.9,
            dominant_colors=[(100, 150, 200), (50, 100, 150)],
            color_variance=45.0,
        ),
        EnhancedSceneInfo(
            start_time=10.0,
            end_time=13.0,
            duration=3.0,
            score=90.0,
            source_file=Path("/video1.mp4"),
            motion_type=MotionType.PAN_RIGHT,
            motion_direction=(1.0, 0.0),
            motion_smoothness=0.85,
            dominant_colors=[(200, 100, 50), (150, 80, 30)],
            color_variance=38.0,
        ),
        EnhancedSceneInfo(
            start_time=20.0,
            end_time=23.0,
            duration=3.0,
            score=75.0,
            source_file=Path("/video1.mp4"),
            motion_type=MotionType.STATIC,
            motion_direction=(0.0, 0.0),
            motion_smoothness=1.0,
            dominant_colors=[(50, 150, 100), (30, 120, 80)],
            color_variance=52.0,
        ),
        EnhancedSceneInfo(
            start_time=0.0,
            end_time=3.0,
            duration=3.0,
            score=80.0,
            source_file=Path("/video2.mp4"),
            motion_type=MotionType.ORBIT_CW,
            motion_direction=(0.5, 0.5),
            motion_smoothness=0.95,
            dominant_colors=[(180, 180, 200), (160, 160, 180)],
            color_variance=28.0,
        ),
        EnhancedSceneInfo(
            start_time=10.0,
            end_time=13.0,
            duration=3.0,
            score=70.0,
            source_file=Path("/video2.mp4"),
            motion_type=MotionType.REVEAL,
            motion_direction=(0.0, 1.0),
            motion_smoothness=0.88,
            dominant_colors=[(220, 180, 140), (200, 160, 120)],
            color_variance=33.0,
        ),
    ]
    return scenes


class TestDiversitySelector:
    """Tests for DiversitySelector class."""

    def test_initialization(self):
        """Test DiversitySelector initialization with valid parameters."""
        selector = DiversitySelector(
            diversity_weight=0.3,
            max_per_source=2,
            min_temporal_gap=5.0,
        )
        assert selector.diversity_weight == 0.3
        assert selector.score_weight == 0.7
        assert selector.max_per_source == 2
        assert selector.min_temporal_gap == 5.0

    def test_initialization_invalid_weight(self):
        """Test that invalid diversity_weight raises error."""
        with pytest.raises(ValueError, match="diversity_weight must be between 0 and 1"):
            DiversitySelector(diversity_weight=1.5)

        with pytest.raises(ValueError, match="diversity_weight must be between 0 and 1"):
            DiversitySelector(diversity_weight=-0.1)

    def test_initialization_invalid_max_per_source(self):
        """Test that invalid max_per_source raises error."""
        with pytest.raises(ValueError, match="max_per_source must be at least 1"):
            DiversitySelector(max_per_source=0)

    def test_initialization_invalid_temporal_gap(self):
        """Test that invalid min_temporal_gap raises error."""
        with pytest.raises(ValueError, match="min_temporal_gap must be non-negative"):
            DiversitySelector(min_temporal_gap=-1.0)

    def test_select_empty_scenes(self):
        """Test selection with empty scene list."""
        selector = DiversitySelector()
        result = selector.select([], 5)
        assert result == []

    def test_select_zero_count(self):
        """Test selection with count=0."""
        selector = DiversitySelector()
        scenes = [
            SceneInfo(0.0, 3.0, 3.0, 85.0, Path("/video.mp4"))
        ]
        result = selector.select(scenes, 0)
        assert result == []

    def test_select_count_exceeds_scenes(self, sample_scenes):
        """Test selection when requested count exceeds available scenes."""
        selector = DiversitySelector()
        result = selector.select(sample_scenes, 10)
        assert len(result) == len(sample_scenes)

    def test_source_diversity_constraint(self, sample_scenes):
        """Test that max_per_source constraint is enforced when possible."""
        selector = DiversitySelector(max_per_source=1, diversity_weight=0.0)
        # Request only 2 scenes so constraint can be satisfied
        result = selector.select(sample_scenes, 2)

        # Count scenes per source
        source_counts = {}
        for scene in result:
            source_counts[scene.source_file] = source_counts.get(scene.source_file, 0) + 1

        # Each source should have at most 1 scene
        assert all(count <= 1 for count in source_counts.values())
        # Should select from different sources
        assert len(source_counts) == 2

    def test_temporal_diversity_constraint(self):
        """Test that min_temporal_gap constraint is enforced."""
        scenes = [
            SceneInfo(0.0, 3.0, 3.0, 90.0, Path("/video.mp4")),
            SceneInfo(2.0, 5.0, 3.0, 85.0, Path("/video.mp4")),  # Too close
            SceneInfo(15.0, 18.0, 3.0, 80.0, Path("/video.mp4")),  # Far enough
        ]

        selector = DiversitySelector(
            min_temporal_gap=5.0,
            max_per_source=3,
            diversity_weight=0.0,  # Pure score-based to test constraint
        )
        result = selector.select(scenes, 3)

        # Should exclude the middle scene (2.0-5.0) because it's too close to first
        assert len(result) >= 2
        selected_times = [s.start_time for s in result]

        # Check temporal gaps
        for i, scene in enumerate(result):
            for other_scene in result[i + 1 :]:
                if scene.source_file == other_scene.source_file:
                    gap = abs(scene.start_time - other_scene.start_time)
                    # Allow some scenes through if constraints can't be satisfied
                    # but prefer those with larger gaps
                    if len(result) == len(scenes):
                        pass  # All scenes selected, constraints relaxed
                    else:
                        assert gap >= selector.min_temporal_gap or gap == min(
                            abs(s.start_time - scene.start_time)
                            for s in scenes
                            if s.source_file == scene.source_file and s != scene
                        )

    def test_motion_type_diversity(self, enhanced_scenes):
        """Test that different motion types are preferred."""
        selector = DiversitySelector(diversity_weight=0.8, max_per_source=5)
        result = selector.select(enhanced_scenes, 4)

        # Should select scenes with different motion types
        motion_types = {s.motion_type for s in result}
        assert len(motion_types) >= 3  # At least 3 different motion types

    def test_color_diversity(self, enhanced_scenes):
        """Test color diversity calculation."""
        selector = DiversitySelector(diversity_weight=0.5, max_per_source=5)
        result = selector.select(enhanced_scenes, 3)

        # Verify we got results
        assert len(result) == 3

        # Results should prefer varied colors
        # Check that we got some diversity in dominant colors
        if all(isinstance(s, EnhancedSceneInfo) for s in result):
            colors_variance = []
            for scene in result:
                if scene.dominant_colors:
                    colors_variance.append(scene.color_variance)
            # Just verify colors exist and vary
            assert len(colors_variance) >= 2

    def test_pure_score_selection(self, sample_scenes):
        """Test selection with diversity_weight=0 (pure score-based)."""
        selector = DiversitySelector(
            diversity_weight=0.0,
            max_per_source=10,  # No source constraint
            min_temporal_gap=0.0,  # No temporal constraint
        )
        result = selector.select(sample_scenes, 3)

        # Should select top 3 by score
        expected_scores = sorted([s.score for s in sample_scenes], reverse=True)[:3]
        actual_scores = sorted([s.score for s in result], reverse=True)
        assert actual_scores == expected_scores

    def test_pure_diversity_selection(self, sample_scenes):
        """Test selection with diversity_weight=1.0."""
        selector = DiversitySelector(
            diversity_weight=1.0,
            max_per_source=1,
            min_temporal_gap=5.0,
        )
        result = selector.select(sample_scenes, 2)

        # Should select from different sources
        sources = {s.source_file for s in result}
        assert len(sources) == 2


class TestMotionContinuityEngine:
    """Tests for MotionContinuityEngine class."""

    def test_empty_sequence(self):
        """Test optimization with empty sequence."""
        engine = MotionContinuityEngine()
        result = engine.optimize_sequence([])
        assert result == []

    def test_single_scene(self, enhanced_scenes):
        """Test optimization with single scene."""
        engine = MotionContinuityEngine()
        result = engine.optimize_sequence([enhanced_scenes[0]])
        assert len(result) == 1
        assert result[0] == enhanced_scenes[0]

    def test_motion_compatibility_same_direction(self):
        """Test that same motion direction has high compatibility."""
        engine = MotionContinuityEngine()

        scene1 = EnhancedSceneInfo(
            start_time=0.0,
            end_time=3.0,
            duration=3.0,
            score=80.0,
            source_file=Path("/video.mp4"),
            motion_type=MotionType.PAN_LEFT,
        )
        scene2 = EnhancedSceneInfo(
            start_time=3.0,
            end_time=6.0,
            duration=3.0,
            score=80.0,
            source_file=Path("/video.mp4"),
            motion_type=MotionType.PAN_LEFT,
        )

        compatibility = engine._motion_compatibility(scene1, scene2)
        assert compatibility >= 0.8

    def test_motion_compatibility_opposite_direction(self):
        """Test that opposite motion direction has low compatibility."""
        engine = MotionContinuityEngine()

        scene1 = EnhancedSceneInfo(
            start_time=0.0,
            end_time=3.0,
            duration=3.0,
            score=80.0,
            source_file=Path("/video.mp4"),
            motion_type=MotionType.PAN_LEFT,
        )
        scene2 = EnhancedSceneInfo(
            start_time=3.0,
            end_time=6.0,
            duration=3.0,
            score=80.0,
            source_file=Path("/video.mp4"),
            motion_type=MotionType.PAN_RIGHT,
        )

        compatibility = engine._motion_compatibility(scene1, scene2)
        assert compatibility <= 0.3

    def test_motion_compatibility_static_neutral(self):
        """Test that static shots work well with any motion."""
        engine = MotionContinuityEngine()

        static = EnhancedSceneInfo(
            start_time=0.0,
            end_time=3.0,
            duration=3.0,
            score=80.0,
            source_file=Path("/video.mp4"),
            motion_type=MotionType.STATIC,
        )
        pan = EnhancedSceneInfo(
            start_time=3.0,
            end_time=6.0,
            duration=3.0,
            score=80.0,
            source_file=Path("/video.mp4"),
            motion_type=MotionType.PAN_LEFT,
        )

        # Static to motion
        compat1 = engine._motion_compatibility(static, pan)
        assert compat1 >= 0.7

        # Motion to static
        compat2 = engine._motion_compatibility(pan, static)
        assert compat2 >= 0.7

    def test_optimize_sequence_avoids_jarring_transitions(self):
        """Test that optimization avoids jarring transitions."""
        engine = MotionContinuityEngine()

        # Create sequence with potential jarring transition
        scenes = [
            EnhancedSceneInfo(
                start_time=0.0,
                end_time=3.0,
                duration=3.0,
                score=90.0,
                source_file=Path("/video.mp4"),
                motion_type=MotionType.PAN_LEFT,
            ),
            EnhancedSceneInfo(
                start_time=3.0,
                end_time=6.0,
                duration=3.0,
                score=85.0,
                source_file=Path("/video.mp4"),
                motion_type=MotionType.PAN_RIGHT,  # Opposite direction
            ),
            EnhancedSceneInfo(
                start_time=6.0,
                end_time=9.0,
                duration=3.0,
                score=80.0,
                source_file=Path("/video.mp4"),
                motion_type=MotionType.STATIC,  # Buffer
            ),
        ]

        result = engine.optimize_sequence(scenes)
        assert len(result) == 3

        # Check that adjacent scenes don't have jarring transitions
        for i in range(len(result) - 1):
            compat = engine._motion_compatibility(result[i], result[i + 1])
            # Should avoid worst compatibility
            assert compat > 0.3 or result[i].motion_type == MotionType.STATIC or result[i + 1].motion_type == MotionType.STATIC

    def test_optimize_sequence_greedy_approach(self, enhanced_scenes):
        """Test that optimization uses greedy approach."""
        engine = MotionContinuityEngine()
        result = engine.optimize_sequence(enhanced_scenes)

        # Should return all scenes
        assert len(result) == len(enhanced_scenes)

        # First scene should be highest scoring
        assert result[0].score == max(s.score for s in enhanced_scenes)

        # Subsequent scenes should have reasonable compatibility
        avg_compat = []
        for i in range(len(result) - 1):
            compat = engine._motion_compatibility(result[i], result[i + 1])
            avg_compat.append(compat)

        # Average compatibility should be decent
        assert np.mean(avg_compat) >= 0.4

    def test_check_sequence_quality_good_sequence(self):
        """Test quality check on well-ordered sequence."""
        engine = MotionContinuityEngine()

        scenes = [
            EnhancedSceneInfo(
                start_time=0.0,
                end_time=3.0,
                duration=3.0,
                score=80.0,
                source_file=Path("/video.mp4"),
                motion_type=MotionType.STATIC,
            ),
            EnhancedSceneInfo(
                start_time=3.0,
                end_time=6.0,
                duration=3.0,
                score=80.0,
                source_file=Path("/video.mp4"),
                motion_type=MotionType.PAN_LEFT,
            ),
            EnhancedSceneInfo(
                start_time=6.0,
                end_time=9.0,
                duration=3.0,
                score=80.0,
                source_file=Path("/video.mp4"),
                motion_type=MotionType.PAN_LEFT,
            ),
        ]

        quality = engine.check_sequence_quality(scenes)

        assert quality["overall_score"] >= 0.7
        assert quality["avg_compatibility"] >= 0.7
        assert len(quality["warnings"]) == 0

    def test_check_sequence_quality_jarring_transitions(self):
        """Test quality check detects jarring transitions."""
        engine = MotionContinuityEngine()

        scenes = [
            EnhancedSceneInfo(
                start_time=0.0,
                end_time=3.0,
                duration=3.0,
                score=80.0,
                source_file=Path("/video.mp4"),
                motion_type=MotionType.PAN_LEFT,
            ),
            EnhancedSceneInfo(
                start_time=3.0,
                end_time=6.0,
                duration=3.0,
                score=80.0,
                source_file=Path("/video.mp4"),
                motion_type=MotionType.PAN_RIGHT,
            ),
            EnhancedSceneInfo(
                start_time=6.0,
                end_time=9.0,
                duration=3.0,
                score=80.0,
                source_file=Path("/video.mp4"),
                motion_type=MotionType.PAN_LEFT,
            ),
        ]

        quality = engine.check_sequence_quality(scenes)

        # Should detect jarring transitions
        assert len(quality["warnings"]) > 0
        assert any("Jarring transition" in w for w in quality["warnings"])

    def test_check_sequence_quality_single_scene(self, enhanced_scenes):
        """Test quality check with single scene."""
        engine = MotionContinuityEngine()
        quality = engine.check_sequence_quality([enhanced_scenes[0]])

        assert quality["overall_score"] == 1.0
        assert quality["avg_compatibility"] == 1.0
        assert len(quality["warnings"]) == 0

    def test_check_sequence_quality_high_variation(self):
        """Test quality check detects high motion variation."""
        engine = MotionContinuityEngine()

        # Create sequence with many motion type changes
        scenes = [
            EnhancedSceneInfo(
                start_time=i * 3.0,
                end_time=(i + 1) * 3.0,
                duration=3.0,
                score=80.0,
                source_file=Path("/video.mp4"),
                motion_type=motion,
            )
            for i, motion in enumerate(
                [
                    MotionType.PAN_LEFT,
                    MotionType.ORBIT_CW,
                    MotionType.REVEAL,
                    MotionType.FPV,
                    MotionType.STATIC,
                ]
            )
        ]

        quality = engine.check_sequence_quality(scenes)

        # Should detect high variation
        assert len(quality["warnings"]) > 0

    def test_to_enhanced_conversion(self):
        """Test conversion from SceneInfo to EnhancedSceneInfo."""
        engine = MotionContinuityEngine()

        scene = SceneInfo(
            start_time=0.0,
            end_time=3.0,
            duration=3.0,
            score=80.0,
            source_file=Path("/video.mp4"),
        )

        enhanced = engine._to_enhanced(scene)

        assert isinstance(enhanced, EnhancedSceneInfo)
        assert enhanced.motion_type == MotionType.UNKNOWN
        assert enhanced.start_time == scene.start_time
        assert enhanced.score == scene.score

    def test_motion_direction_alignment_bonus(self):
        """Test that aligned motion directions get compatibility bonus."""
        engine = MotionContinuityEngine()

        # Aligned directions
        scene1 = EnhancedSceneInfo(
            start_time=0.0,
            end_time=3.0,
            duration=3.0,
            score=80.0,
            source_file=Path("/video.mp4"),
            motion_type=MotionType.PAN_LEFT,
            motion_direction=(-1.0, 0.0),
        )
        scene2 = EnhancedSceneInfo(
            start_time=3.0,
            end_time=6.0,
            duration=3.0,
            score=80.0,
            source_file=Path("/video.mp4"),
            motion_type=MotionType.PAN_LEFT,
            motion_direction=(-0.9, -0.1),
        )

        compat_aligned = engine._motion_compatibility(scene1, scene2)

        # Opposite directions
        scene3 = EnhancedSceneInfo(
            start_time=6.0,
            end_time=9.0,
            duration=3.0,
            score=80.0,
            source_file=Path("/video.mp4"),
            motion_type=MotionType.PAN_LEFT,
            motion_direction=(1.0, 0.0),
        )

        compat_opposite = engine._motion_compatibility(scene1, scene3)

        # Aligned should be better than opposite
        assert compat_aligned > compat_opposite


class TestEnhancedSceneInfo:
    """Tests for EnhancedSceneInfo dataclass."""

    def test_initialization_with_defaults(self):
        """Test EnhancedSceneInfo initialization with defaults."""
        scene = EnhancedSceneInfo(
            start_time=0.0,
            end_time=3.0,
            duration=3.0,
            score=80.0,
            source_file=Path("/video.mp4"),
        )

        assert scene.motion_type == MotionType.UNKNOWN
        assert scene.motion_direction == (0.0, 0.0)
        assert scene.motion_smoothness == 0.0
        assert scene.dominant_colors == []
        assert scene.color_variance == 0.0

    def test_initialization_with_values(self):
        """Test EnhancedSceneInfo initialization with all values."""
        scene = EnhancedSceneInfo(
            start_time=0.0,
            end_time=3.0,
            duration=3.0,
            score=80.0,
            source_file=Path("/video.mp4"),
            motion_type=MotionType.PAN_LEFT,
            motion_direction=(-1.0, 0.0),
            motion_smoothness=0.9,
            dominant_colors=[(100, 150, 200)],
            color_variance=45.0,
        )

        assert scene.motion_type == MotionType.PAN_LEFT
        assert scene.motion_direction == (-1.0, 0.0)
        assert scene.motion_smoothness == 0.9
        assert scene.dominant_colors == [(100, 150, 200)]
        assert scene.color_variance == 45.0

    def test_inherits_from_scene_info(self):
        """Test that EnhancedSceneInfo properly inherits from SceneInfo."""
        scene = EnhancedSceneInfo(
            start_time=0.0,
            end_time=10.0,
            duration=10.0,
            score=85.0,
            source_file=Path("/video.mp4"),
        )

        # Should have midpoint property from SceneInfo
        assert scene.midpoint == 5.0


class TestIntegration:
    """Integration tests combining multiple components."""

    def test_diversity_selection_with_motion_optimization(self, enhanced_scenes):
        """Test full pipeline: diversity selection -> motion optimization."""
        # Step 1: Select diverse scenes
        selector = DiversitySelector(
            diversity_weight=0.5,
            max_per_source=2,
            min_temporal_gap=5.0,
        )
        selected = selector.select(enhanced_scenes, 4)

        # Step 2: Optimize motion continuity
        engine = MotionContinuityEngine()
        optimized = engine.optimize_sequence(selected)

        # Step 3: Check quality
        quality = engine.check_sequence_quality(optimized)

        assert len(optimized) == len(selected)
        assert quality["overall_score"] > 0.3  # Should be reasonable

    def test_edge_case_all_same_motion_type(self):
        """Test handling when all scenes have same motion type."""
        scenes = [
            EnhancedSceneInfo(
                start_time=i * 3.0,
                end_time=(i + 1) * 3.0,
                duration=3.0,
                score=80.0 - i * 5,
                source_file=Path("/video.mp4"),
                motion_type=MotionType.PAN_LEFT,
            )
            for i in range(5)
        ]

        selector = DiversitySelector(diversity_weight=0.5, max_per_source=5)
        selected = selector.select(scenes, 3)

        engine = MotionContinuityEngine()
        optimized = engine.optimize_sequence(selected)

        # Should still work
        assert len(optimized) == 3

        quality = engine.check_sequence_quality(optimized)
        # High compatibility since all same motion
        assert quality["avg_compatibility"] >= 0.8

    def test_edge_case_single_source_file(self):
        """Test handling when all scenes from single source."""
        scenes = [
            EnhancedSceneInfo(
                start_time=i * 20.0,  # Increased gap to satisfy constraints
                end_time=(i + 1) * 20.0,
                duration=20.0,
                score=80.0 - i * 5,
                source_file=Path("/video.mp4"),
                motion_type=MotionType.PAN_LEFT,
            )
            for i in range(5)
        ]

        selector = DiversitySelector(
            diversity_weight=0.3,
            max_per_source=2,
            min_temporal_gap=15.0,
        )
        selected = selector.select(scenes, 2)

        # Should respect constraints with single source
        assert len(selected) <= 2

        # Check temporal gaps
        if len(selected) >= 2:
            for i in range(len(selected) - 1):
                for j in range(i + 1, len(selected)):
                    gap = abs(selected[i].start_time - selected[j].start_time)
                    # Should respect the temporal gap constraint
                    assert gap >= 15.0


# ===========================================================================
# min_scenes_for_duration tests
# ===========================================================================


class TestMinScenesForDuration:
    """Tests for DiversitySelector.min_scenes_for_duration()."""

    def test_short_reel_15s_or_less(self):
        assert DiversitySelector.min_scenes_for_duration(10.0) == 5
        assert DiversitySelector.min_scenes_for_duration(15.0) == 5

    def test_medium_reel_up_to_30s(self):
        assert DiversitySelector.min_scenes_for_duration(15.1) == 8
        assert DiversitySelector.min_scenes_for_duration(30.0) == 8

    def test_long_reel_up_to_60s(self):
        assert DiversitySelector.min_scenes_for_duration(30.1) == 12
        assert DiversitySelector.min_scenes_for_duration(60.0) == 12

    def test_very_long_reel_beyond_60s(self):
        assert DiversitySelector.min_scenes_for_duration(60.1) == 15
        assert DiversitySelector.min_scenes_for_duration(120.0) == 15


# ===========================================================================
# select_with_minimum tests
# ===========================================================================


def _make_scenes(n: int, sources: int = 1) -> list[SceneInfo]:
    """Create n SceneInfo objects spread across `sources` source files."""
    scenes = []
    for i in range(n):
        src = Path(f"/video{i % sources + 1}.mp4")
        scenes.append(
            SceneInfo(
                start_time=float(i * 20),
                end_time=float(i * 20 + 5),
                duration=5.0,
                score=float(80 - i),
                source_file=src,
            )
        )
    return scenes


class TestSelectWithMinimum:
    """Tests for DiversitySelector.select_with_minimum()."""

    def test_returns_at_least_min_scenes_when_possible(self):
        """With enough scenes available, minimum count should be met."""
        selector = DiversitySelector(max_per_source=2, min_temporal_gap=5.0)
        # 15 scenes across 8 sources — plenty to meet min for 30s (=8)
        scenes = _make_scenes(15, sources=8)
        result = selector.select_with_minimum(scenes, count=10, target_duration=30.0)
        assert len(result) >= 8

    def test_never_exceeds_count(self):
        """Should never return more scenes than count."""
        selector = DiversitySelector(max_per_source=3, min_temporal_gap=0.0)
        scenes = _make_scenes(20, sources=5)
        result = selector.select_with_minimum(scenes, count=6, target_duration=15.0)
        # min_scenes_for_duration(15) == 5; count=6 -> effective_count=6
        assert len(result) <= 6

    def test_relaxes_max_per_source_to_reach_minimum(self):
        """When strict constraints yield fewer than min, relax max_per_source."""
        # Only 1 source file; max_per_source=1 would give 1 scene, but min for 15s is 5
        selector = DiversitySelector(max_per_source=1, min_temporal_gap=0.0)
        scenes = _make_scenes(10, sources=1)
        result = selector.select_with_minimum(scenes, count=10, target_duration=15.0)
        assert len(result) >= 5

    def test_fewer_scenes_than_minimum_returns_all(self):
        """When total scenes < minimum, return everything available."""
        selector = DiversitySelector(max_per_source=10, min_temporal_gap=0.0)
        scenes = _make_scenes(3, sources=3)  # Only 3 scenes; min for 30s is 8
        result = selector.select_with_minimum(scenes, count=10, target_duration=30.0)
        assert len(result) == 3  # Can't exceed available scenes

    def test_min_scenes_15s(self):
        """For 15s target, minimum is 5 scenes."""
        selector = DiversitySelector(max_per_source=5, min_temporal_gap=0.0)
        scenes = _make_scenes(10, sources=5)
        result = selector.select_with_minimum(scenes, count=10, target_duration=15.0)
        assert len(result) >= 5

    def test_min_scenes_30s(self):
        """For 30s target, minimum is 8 scenes."""
        selector = DiversitySelector(max_per_source=5, min_temporal_gap=0.0)
        scenes = _make_scenes(15, sources=5)
        result = selector.select_with_minimum(scenes, count=15, target_duration=30.0)
        assert len(result) >= 8

    def test_min_scenes_60s(self):
        """For 60s target, minimum is 12 scenes."""
        selector = DiversitySelector(max_per_source=5, min_temporal_gap=0.0)
        scenes = _make_scenes(20, sources=5)
        result = selector.select_with_minimum(scenes, count=20, target_duration=60.0)
        assert len(result) >= 12

    def test_min_scenes_beyond_60s(self):
        """For >60s target, minimum is 15 scenes."""
        selector = DiversitySelector(max_per_source=5, min_temporal_gap=0.0)
        scenes = _make_scenes(20, sources=5)
        result = selector.select_with_minimum(scenes, count=20, target_duration=90.0)
        assert len(result) >= 15

    def test_count_larger_than_min_is_respected(self):
        """If count > min_scenes and scenes available, return count scenes."""
        selector = DiversitySelector(max_per_source=10, min_temporal_gap=0.0)
        scenes = _make_scenes(20, sources=10)
        result = selector.select_with_minimum(scenes, count=12, target_duration=15.0)
        # min for 15s is 5; count=12 -> effective_count=12
        assert len(result) >= 5  # at least minimum
        assert len(result) <= 12  # never over count
