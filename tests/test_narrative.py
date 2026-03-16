"""
Tests for narrative arc sequencing and hook generation.
"""

from pathlib import Path

import numpy as np
import pytest

from drone_reel.core.beat_sync import BeatInfo
from drone_reel.core.narrative import (
    HookGenerator,
    HookPattern,
    MotionCharacteristics,
    NarrativeArc,
    NarrativeSequencer,
)
from drone_reel.core.scene_detector import SceneInfo
from drone_reel.core.video_processor import TransitionType


@pytest.fixture
def sample_scenes():
    """Create sample scenes with varying scores."""
    return [
        SceneInfo(
            start_time=0.0,
            end_time=5.0,
            duration=5.0,
            score=95.0,
            source_file=Path("video1.mp4"),
        ),
        SceneInfo(
            start_time=5.0,
            end_time=10.0,
            duration=5.0,
            score=75.0,
            source_file=Path("video1.mp4"),
        ),
        SceneInfo(
            start_time=10.0,
            end_time=15.0,
            duration=5.0,
            score=85.0,
            source_file=Path("video1.mp4"),
        ),
        SceneInfo(
            start_time=15.0,
            end_time=20.0,
            duration=5.0,
            score=60.0,
            source_file=Path("video1.mp4"),
        ),
        SceneInfo(
            start_time=20.0,
            end_time=25.0,
            duration=5.0,
            score=80.0,
            source_file=Path("video1.mp4"),
        ),
        SceneInfo(
            start_time=25.0,
            end_time=30.0,
            duration=5.0,
            score=70.0,
            source_file=Path("video1.mp4"),
        ),
    ]


@pytest.fixture
def minimal_scenes():
    """Create minimal scene set for edge case testing."""
    return [
        SceneInfo(
            start_time=0.0,
            end_time=3.0,
            duration=3.0,
            score=80.0,
            source_file=Path("video1.mp4"),
        ),
        SceneInfo(
            start_time=3.0,
            end_time=6.0,
            duration=3.0,
            score=70.0,
            source_file=Path("video1.mp4"),
        ),
    ]


@pytest.fixture
def sample_beat_info():
    """Create sample beat info for testing."""
    beat_times = np.array([0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0])
    downbeat_times = np.array([0.0, 2.0, 4.0])
    energy_profile = np.array([0.5, 0.6, 0.7, 0.8, 0.9, 0.8, 0.7, 0.6, 0.5])
    phrase_boundaries = np.array([0.0, 2.0, 4.0])
    spectral_profile = np.array([0.4, 0.5, 0.6, 0.7, 0.8, 0.7, 0.6, 0.5, 0.4])
    onset_density = np.array([0.3, 0.4, 0.5, 0.6, 0.7, 0.6, 0.5, 0.4, 0.3])
    harmonic_energy = np.array([0.6, 0.6, 0.6, 0.7, 0.7, 0.6, 0.6, 0.5, 0.5])
    percussive_energy = np.array([0.4, 0.5, 0.6, 0.7, 0.8, 0.7, 0.6, 0.5, 0.4])

    return BeatInfo(
        tempo=120.0,
        beat_times=beat_times,
        downbeat_times=downbeat_times,
        duration=4.5,
        energy_profile=energy_profile,
        time_signature=(4, 4),
        phrase_boundaries=phrase_boundaries,
        tempo_changes=[],
        spectral_profile=spectral_profile,
        onset_density=onset_density,
        harmonic_energy=harmonic_energy,
        percussive_energy=percussive_energy,
    )


class TestHookGenerator:
    """Test hook generation functionality."""

    def test_initialization(self):
        """Test hook generator initialization."""
        generator = HookGenerator()
        assert generator.motion_weight == 0.4
        assert generator.composition_weight == 0.3

        generator = HookGenerator(motion_weight=0.5, composition_weight=0.4)
        assert generator.motion_weight == 0.5
        assert generator.composition_weight == 0.4

    def test_select_hook_scene_basic(self, sample_scenes):
        """Test basic hook scene selection."""
        generator = HookGenerator()
        hook_scene = generator.select_hook_scene(sample_scenes)

        assert hook_scene is not None
        assert hook_scene in sample_scenes
        assert hook_scene.score >= 75.0

    def test_select_hook_scene_no_scenes(self):
        """Test hook selection with no scenes."""
        generator = HookGenerator()

        with pytest.raises(ValueError, match="No scenes provided"):
            generator.select_hook_scene([])

    def test_select_hook_scene_motion_preference(self, sample_scenes):
        """Test hook selection respects motion preferences."""
        generator = HookGenerator()
        hook_scene = generator.select_hook_scene(
            sample_scenes, prefer_motion_types=["reveal", "orbit"]
        )

        assert hook_scene is not None
        motion_chars = generator._analyze_motion_characteristics(hook_scene)
        assert motion_chars.motion_type in [
            "reveal",
            "orbit",
            "flyover",
            "pan",
            "static",
        ]

    def test_score_hook_potential(self, sample_scenes):
        """Test hook potential scoring."""
        generator = HookGenerator()

        for scene in sample_scenes:
            score = generator.score_hook_potential(scene)
            assert 0 <= score <= 100

        high_score_scene = sample_scenes[0]
        low_score_scene = sample_scenes[3]

        high_hook_score = generator.score_hook_potential(high_score_scene)
        low_hook_score = generator.score_hook_potential(low_score_scene)

        assert high_hook_score > low_hook_score

    def test_analyze_motion_characteristics(self, sample_scenes):
        """Test motion characteristics analysis."""
        generator = HookGenerator()

        high_score_scene = sample_scenes[0]
        motion_chars = generator._analyze_motion_characteristics(high_score_scene)

        assert isinstance(motion_chars, MotionCharacteristics)
        assert motion_chars.motion_type in [
            "reveal",
            "orbit",
            "flyover",
            "pan",
            "tilt",
            "static",
        ]
        assert 0 <= motion_chars.motion_intensity <= 1
        assert 0 <= motion_chars.complexity_score <= 1
        assert isinstance(motion_chars.is_golden_hour, bool)
        assert isinstance(motion_chars.has_dramatic_subject, bool)

    def test_create_dramatic_reveal(self, sample_scenes):
        """Test dramatic reveal hook pattern."""
        generator = HookGenerator()
        segments = generator.create_hook_sequence(
            sample_scenes, HookPattern.DRAMATIC_REVEAL, hook_duration=3.0
        )

        assert len(segments) == 1
        assert segments[0].duration == 3.0
        assert segments[0].transition_in == TransitionType.FADE_BLACK
        assert segments[0].transition_out == TransitionType.CUT

    def test_create_quick_cut_montage(self, sample_scenes):
        """Test quick cut montage hook pattern."""
        generator = HookGenerator()
        segments = generator.create_hook_sequence(
            sample_scenes, HookPattern.QUICK_CUT_MONTAGE, hook_duration=3.0
        )

        assert 3 <= len(segments) <= 4
        total_duration = sum(seg.duration for seg in segments)
        assert abs(total_duration - 3.0) < 0.1

        assert segments[0].transition_in == TransitionType.FADE_BLACK
        for seg in segments[1:]:
            assert seg.transition_in == TransitionType.CUT

    def test_create_quick_cut_montage_insufficient_scenes(self, minimal_scenes):
        """Test quick cut montage with insufficient scenes."""
        generator = HookGenerator()

        with pytest.raises(ValueError, match="at least 3 scenes"):
            generator.create_hook_sequence(
                minimal_scenes, HookPattern.QUICK_CUT_MONTAGE, hook_duration=3.0
            )

    def test_create_speed_ramp_intro(self, sample_scenes):
        """Test speed ramp intro hook pattern."""
        generator = HookGenerator()
        segments = generator.create_hook_sequence(
            sample_scenes, HookPattern.SPEED_RAMP_INTRO, hook_duration=3.0
        )

        assert len(segments) == 1
        assert segments[0].duration == 3.0
        assert segments[0].transition_in == TransitionType.FADE_BLACK

    def test_create_text_reveal(self, sample_scenes):
        """Test text reveal hook pattern."""
        generator = HookGenerator()
        segments = generator.create_hook_sequence(
            sample_scenes, HookPattern.TEXT_REVEAL, hook_duration=3.0
        )

        assert len(segments) == 1
        assert segments[0].duration == 3.0
        assert segments[0].transition_in == TransitionType.FADE_BLACK
        assert segments[0].transition_duration == 0.6

    def test_all_hook_patterns(self, sample_scenes):
        """Test all hook patterns produce valid output."""
        generator = HookGenerator()

        for pattern in HookPattern:
            try:
                segments = generator.create_hook_sequence(sample_scenes, pattern, 3.0)
                assert len(segments) > 0
                assert all(seg.duration > 0 for seg in segments)
            except ValueError as e:
                pytest.fail(f"Pattern {pattern} failed: {e}")

    def test_detect_golden_hour(self, sample_scenes):
        """Test golden hour detection."""
        generator = HookGenerator()

        high_score = sample_scenes[0]
        low_score = sample_scenes[3]

        assert generator._detect_golden_hour(high_score) is True
        assert generator._detect_golden_hour(low_score) is False

    def test_calculate_visual_variety(self, sample_scenes):
        """Test visual variety calculation."""
        generator = HookGenerator()

        for scene in sample_scenes:
            variety = generator._calculate_visual_variety(scene)
            assert 0 <= variety <= 1


class TestNarrativeSequencer:
    """Test narrative sequencing functionality."""

    def test_initialization(self):
        """Test narrative sequencer initialization."""
        sequencer = NarrativeSequencer()
        assert sequencer.arc_type == NarrativeArc.CLASSIC

        sequencer = NarrativeSequencer(arc_type=NarrativeArc.BUILDING)
        assert sequencer.arc_type == NarrativeArc.BUILDING

    def test_sequence_classic_arc(self, sample_scenes):
        """Test classic narrative arc sequencing."""
        sequencer = NarrativeSequencer(arc_type=NarrativeArc.CLASSIC)
        sequenced = sequencer.sequence(sample_scenes, target_duration=30.0)

        assert len(sequenced) > 0
        assert len(sequenced) <= len(sample_scenes)
        assert all(scene in sample_scenes for scene in sequenced)

        assert sequenced[0].score >= 75.0

    def test_sequence_building_arc(self, sample_scenes):
        """Test building narrative arc."""
        sequencer = NarrativeSequencer(arc_type=NarrativeArc.BUILDING)
        sequenced = sequencer.sequence(sample_scenes, target_duration=30.0)

        assert len(sequenced) > 0
        energy_curve = sequencer.calculate_energy_curve(sequenced)
        assert energy_curve[0] < energy_curve[-1]

    def test_sequence_bookend_arc(self, sample_scenes):
        """Test bookend narrative arc."""
        sequencer = NarrativeSequencer(arc_type=NarrativeArc.BOOKEND)
        sequenced = sequencer.sequence(sample_scenes, target_duration=30.0)

        assert len(sequenced) > 0

        energy_curve = sequencer.calculate_energy_curve(sequenced)
        assert energy_curve[0] > 0.7
        assert energy_curve[-1] > 0.7

    def test_sequence_montage_arc(self, sample_scenes):
        """Test montage narrative arc."""
        sequencer = NarrativeSequencer(arc_type=NarrativeArc.MONTAGE)
        sequenced = sequencer.sequence(sample_scenes, target_duration=30.0)

        assert len(sequenced) > 0

    def test_sequence_cinematic_arc(self, sample_scenes):
        """Test cinematic narrative arc."""
        sequencer = NarrativeSequencer(arc_type=NarrativeArc.CINEMATIC)
        sequenced = sequencer.sequence(sample_scenes, target_duration=30.0)

        assert len(sequenced) > 0

    def test_sequence_all_arc_types(self, sample_scenes):
        """Test all narrative arc types produce valid output."""
        for arc_type in NarrativeArc:
            sequencer = NarrativeSequencer(arc_type=arc_type)
            sequenced = sequencer.sequence(sample_scenes, target_duration=30.0)

            assert len(sequenced) > 0
            assert all(scene in sample_scenes for scene in sequenced)

    def test_sequence_no_scenes(self):
        """Test sequencing with no scenes."""
        sequencer = NarrativeSequencer()

        with pytest.raises(ValueError, match="No scenes provided"):
            sequencer.sequence([], target_duration=30.0)

    def test_sequence_minimal_scenes(self, minimal_scenes):
        """Test sequencing with minimal scenes."""
        sequencer = NarrativeSequencer()
        sequenced = sequencer.sequence(minimal_scenes, target_duration=10.0)

        assert len(sequenced) == len(minimal_scenes)

    def test_sequence_with_beat_info(self, sample_scenes, sample_beat_info):
        """Test sequencing with beat information."""
        sequencer = NarrativeSequencer()
        sequenced = sequencer.sequence(
            sample_scenes, target_duration=30.0, beat_info=sample_beat_info
        )

        assert len(sequenced) > 0
        assert all(scene in sample_scenes for scene in sequenced)

    def test_calculate_energy_curve(self, sample_scenes):
        """Test energy curve calculation."""
        sequencer = NarrativeSequencer(arc_type=NarrativeArc.CLASSIC)
        sequenced = sequencer.sequence(sample_scenes, target_duration=30.0)

        energy_curve = sequencer.calculate_energy_curve(sequenced)

        assert len(energy_curve) == len(sequenced)
        assert all(0 <= energy <= 1 for energy in energy_curve)

    def test_calculate_energy_curve_all_arcs(self, sample_scenes):
        """Test energy curve for all arc types."""
        for arc_type in NarrativeArc:
            sequencer = NarrativeSequencer(arc_type=arc_type)
            sequenced = sequencer.sequence(sample_scenes, target_duration=30.0)
            energy_curve = sequencer.calculate_energy_curve(sequenced)

            assert len(energy_curve) == len(sequenced)
            assert all(0 <= e <= 1 for e in energy_curve)

    def test_get_arc_template_classic(self):
        """Test classic arc template."""
        sequencer = NarrativeSequencer()
        template = sequencer._get_arc_template(NarrativeArc.CLASSIC, 30.0)

        assert len(template) == 4
        assert template[0] == (0.0, 0.1, "peak")
        assert template[1] == (0.1, 0.4, "rising")
        assert template[2] == (0.4, 0.8, "peak")
        assert template[3] == (0.8, 1.0, "falling")

    def test_get_arc_template_building(self):
        """Test building arc template."""
        sequencer = NarrativeSequencer()
        template = sequencer._get_arc_template(NarrativeArc.BUILDING, 30.0)

        assert len(template) == 4
        energy_levels = [t[2] for t in template]
        assert "peak" in energy_levels

    def test_get_arc_template_bookend(self):
        """Test bookend arc template."""
        sequencer = NarrativeSequencer()
        template = sequencer._get_arc_template(NarrativeArc.BOOKEND, 30.0)

        assert len(template) == 5
        assert template[0][2] == "peak"
        assert template[-1][2] == "peak"

    def test_get_arc_template_montage(self):
        """Test montage arc template."""
        sequencer = NarrativeSequencer()
        template = sequencer._get_arc_template(NarrativeArc.MONTAGE, 30.0)

        assert len(template) == 5

    def test_get_arc_template_cinematic(self):
        """Test cinematic arc template."""
        sequencer = NarrativeSequencer()
        template = sequencer._get_arc_template(NarrativeArc.CINEMATIC, 30.0)

        assert len(template) == 4
        assert template[0][2] == "low"
        assert template[-1][2] == "low"

    def test_select_scene_for_section(self, sample_scenes):
        """Test scene selection for section."""
        sequencer = NarrativeSequencer()

        peak_scene = sequencer._select_scene_for_section(
            sample_scenes, "peak", 5.0, None, 0.0
        )
        assert peak_scene.score >= 75.0

        low_scene = sequencer._select_scene_for_section(
            sample_scenes, "low", 5.0, None, 0.0
        )
        assert low_scene is not None

    def test_select_scene_for_section_with_beats(
        self, sample_scenes, sample_beat_info
    ):
        """Test scene selection with beat info."""
        sequencer = NarrativeSequencer()

        scene = sequencer._select_scene_for_section(
            sample_scenes, "peak", 5.0, sample_beat_info, 0.0
        )
        assert scene is not None

    def test_get_energy_at_position_classic(self):
        """Test energy calculation for classic arc."""
        sequencer = NarrativeSequencer(arc_type=NarrativeArc.CLASSIC)

        hook_energy = sequencer._get_energy_at_position(0.05, NarrativeArc.CLASSIC)
        assert hook_energy > 0.7

        climax_energy = sequencer._get_energy_at_position(0.6, NarrativeArc.CLASSIC)
        assert climax_energy > 0.7

        resolve_energy = sequencer._get_energy_at_position(0.9, NarrativeArc.CLASSIC)
        assert resolve_energy < climax_energy

    def test_get_energy_at_position_building(self):
        """Test energy calculation for building arc."""
        sequencer = NarrativeSequencer(arc_type=NarrativeArc.BUILDING)

        start_energy = sequencer._get_energy_at_position(0.1, NarrativeArc.BUILDING)
        end_energy = sequencer._get_energy_at_position(0.9, NarrativeArc.BUILDING)

        assert end_energy > start_energy

    def test_get_energy_at_position_all_arcs(self):
        """Test energy calculation for all arc types."""
        for arc_type in NarrativeArc:
            sequencer = NarrativeSequencer(arc_type=arc_type)

            for position in [0.0, 0.25, 0.5, 0.75, 1.0]:
                energy = sequencer._get_energy_at_position(position, arc_type)
                assert 0 <= energy <= 1

    def test_get_beat_energy_at_time(self, sample_beat_info):
        """Test beat energy retrieval."""
        sequencer = NarrativeSequencer()

        energy_start = sequencer._get_beat_energy_at_time(sample_beat_info, 0.0)
        assert 0 <= energy_start <= 1

        energy_mid = sequencer._get_beat_energy_at_time(sample_beat_info, 2.0)
        assert 0 <= energy_mid <= 1

        energy_end = sequencer._get_beat_energy_at_time(sample_beat_info, 4.0)
        assert 0 <= energy_end <= 1

    def test_get_beat_energy_edge_cases(self, sample_beat_info):
        """Test beat energy edge cases."""
        sequencer = NarrativeSequencer()

        energy = sequencer._get_beat_energy_at_time(sample_beat_info, -1.0)
        assert energy == 0.5

        energy = sequencer._get_beat_energy_at_time(sample_beat_info, 100.0)
        assert 0 <= energy <= 1


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_hook_pattern_creation(self):
        """Test hook pattern creation with empty scenes."""
        generator = HookGenerator()

        with pytest.raises(ValueError):
            generator.create_hook_sequence([], HookPattern.DRAMATIC_REVEAL, 3.0)

    def test_very_short_duration(self, sample_scenes):
        """Test sequencing with very short duration."""
        sequencer = NarrativeSequencer()
        sequenced = sequencer.sequence(sample_scenes, target_duration=5.0)

        assert len(sequenced) > 0

    def test_very_long_duration(self, sample_scenes):
        """Test sequencing with very long duration."""
        sequencer = NarrativeSequencer()
        sequenced = sequencer.sequence(sample_scenes, target_duration=120.0)

        assert len(sequenced) > 0

    def test_single_scene(self):
        """Test with single scene."""
        single_scene = [
            SceneInfo(
                start_time=0.0,
                end_time=10.0,
                duration=10.0,
                score=80.0,
                source_file=Path("video.mp4"),
            )
        ]

        generator = HookGenerator()
        hook = generator.select_hook_scene(single_scene)
        assert hook == single_scene[0]

        sequencer = NarrativeSequencer()
        sequenced = sequencer.sequence(single_scene, target_duration=30.0)
        assert len(sequenced) == 1

    def test_all_low_score_scenes(self):
        """Test with all low-scoring scenes."""
        low_scenes = [
            SceneInfo(
                start_time=float(i),
                end_time=float(i + 3),
                duration=3.0,
                score=20.0,
                source_file=Path("video.mp4"),
            )
            for i in range(5)
        ]

        generator = HookGenerator()
        hook = generator.select_hook_scene(low_scenes)
        assert hook in low_scenes

        sequencer = NarrativeSequencer()
        sequenced = sequencer.sequence(low_scenes, target_duration=15.0)
        assert len(sequenced) > 0

    def test_all_high_score_scenes(self):
        """Test with all high-scoring scenes."""
        high_scenes = [
            SceneInfo(
                start_time=float(i),
                end_time=float(i + 3),
                duration=3.0,
                score=95.0,
                source_file=Path("video.mp4"),
            )
            for i in range(5)
        ]

        generator = HookGenerator()
        hook = generator.select_hook_scene(high_scenes)
        assert hook in high_scenes

        sequencer = NarrativeSequencer()
        sequenced = sequencer.sequence(high_scenes, target_duration=15.0)
        assert len(sequenced) > 0


class TestIntegration:
    """Integration tests for hook generator and sequencer."""

    def test_hook_then_sequence(self, sample_scenes):
        """Test creating hook then sequencing remaining scenes."""
        generator = HookGenerator()
        hook_segments = generator.create_hook_sequence(
            sample_scenes, HookPattern.DRAMATIC_REVEAL, hook_duration=3.0
        )

        assert len(hook_segments) == 1
        hook_scene = hook_segments[0].scene

        remaining_scenes = [s for s in sample_scenes if s != hook_scene]
        sequencer = NarrativeSequencer(arc_type=NarrativeArc.CLASSIC)
        sequenced = sequencer.sequence(remaining_scenes, target_duration=27.0)

        assert len(sequenced) > 0
        assert hook_scene not in sequenced

    def test_hook_with_beat_sync(self, sample_scenes, sample_beat_info):
        """Test hook generation with beat sync integration."""
        generator = HookGenerator()
        hook_segments = generator.create_hook_sequence(
            sample_scenes, HookPattern.QUICK_CUT_MONTAGE, hook_duration=3.0
        )

        assert len(hook_segments) >= 3

        sequencer = NarrativeSequencer()
        sequenced = sequencer.sequence(
            sample_scenes, target_duration=30.0, beat_info=sample_beat_info
        )

        assert len(sequenced) > 0

    def test_complete_workflow(self, sample_scenes, sample_beat_info):
        """Test complete narrative workflow."""
        generator = HookGenerator()
        hook = generator.select_hook_scene(sample_scenes)

        assert hook is not None

        hook_segments = generator.create_hook_sequence(
            sample_scenes, HookPattern.DRAMATIC_REVEAL, hook_duration=3.0
        )

        assert len(hook_segments) == 1

        sequencer = NarrativeSequencer(arc_type=NarrativeArc.CLASSIC)
        sequenced = sequencer.sequence(
            sample_scenes, target_duration=30.0, hook_duration=3.0, beat_info=sample_beat_info
        )

        assert len(sequenced) > 0

        energy_curve = sequencer.calculate_energy_curve(sequenced)
        assert len(energy_curve) == len(sequenced)
        assert all(0 <= e <= 1 for e in energy_curve)

        hook_potential = generator.score_hook_potential(hook)
        assert 0 <= hook_potential <= 100
