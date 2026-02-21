"""
Example usage of the narrative arc sequencer and hook generator.

Demonstrates how to create engaging video openings and sequence scenes
according to narrative patterns optimized for social media.
"""

from pathlib import Path
from drone_reel.core import (
    HookGenerator,
    HookPattern,
    NarrativeArc,
    NarrativeSequencer,
    SceneDetector,
    BeatSync,
)
from drone_reel.core.scene_detector import SceneInfo


def example_hook_generation():
    """Demonstrate hook pattern generation."""
    print("=== Hook Generation Example ===\n")

    sample_scenes = [
        SceneInfo(
            start_time=0.0,
            end_time=5.0,
            duration=5.0,
            score=95.0,  # High-quality reveal shot
            source_file=Path("drone_footage_1.mp4"),
        ),
        SceneInfo(
            start_time=5.0,
            end_time=10.0,
            duration=5.0,
            score=75.0,  # Good orbit shot
            source_file=Path("drone_footage_1.mp4"),
        ),
        SceneInfo(
            start_time=10.0,
            end_time=15.0,
            duration=5.0,
            score=85.0,  # Excellent flyover
            source_file=Path("drone_footage_1.mp4"),
        ),
    ]

    generator = HookGenerator()

    print("1. Selecting best hook scene...")
    hook_scene = generator.select_hook_scene(
        sample_scenes, prefer_motion_types=["reveal", "orbit"]
    )
    hook_score = generator.score_hook_potential(hook_scene)
    print(f"   Selected scene with score: {hook_score:.1f}")
    print(f"   Duration: {hook_scene.duration}s\n")

    print("2. Creating hook patterns:")
    for pattern in HookPattern:
        if pattern == HookPattern.QUICK_CUT_MONTAGE and len(sample_scenes) < 3:
            continue

        print(f"\n   {pattern.value}:")
        try:
            segments = generator.create_hook_sequence(
                sample_scenes, pattern, hook_duration=3.0
            )
            print(f"     - Segments: {len(segments)}")
            total_duration = sum(seg.duration for seg in segments)
            print(f"     - Total duration: {total_duration:.1f}s")
            print(f"     - First transition: {segments[0].transition_in.value}")
        except ValueError as e:
            print(f"     - Skipped: {e}")


def example_narrative_sequencing():
    """Demonstrate narrative arc sequencing."""
    print("\n\n=== Narrative Sequencing Example ===\n")

    sample_scenes = [
        SceneInfo(i, i + 5, 5.0, 70 + i * 3, Path("video.mp4")) for i in range(0, 30, 5)
    ]

    print("Available narrative arcs:")
    for arc in NarrativeArc:
        print(f"  - {arc.value}")

    print("\n1. Classic arc (Hook → Build → Climax → Resolve):")
    sequencer = NarrativeSequencer(arc_type=NarrativeArc.CLASSIC)
    sequenced = sequencer.sequence(sample_scenes, target_duration=30.0)

    print(f"   Sequenced {len(sequenced)} scenes")

    energy_curve = sequencer.calculate_energy_curve(sequenced)
    print("\n   Energy progression:")
    for i, (scene, energy) in enumerate(zip(sequenced, energy_curve)):
        position_pct = i / max(len(sequenced) - 1, 1) * 100
        print(f"     {position_pct:5.1f}%: Energy={energy:.2f}, Score={scene.score:.1f}")

    print("\n2. Building arc (Continuous energy increase):")
    sequencer = NarrativeSequencer(arc_type=NarrativeArc.BUILDING)
    sequenced = sequencer.sequence(sample_scenes, target_duration=30.0)
    energy_curve = sequencer.calculate_energy_curve(sequenced)

    print(f"   Start energy: {energy_curve[0]:.2f}")
    print(f"   End energy: {energy_curve[-1]:.2f}")
    print(f"   Energy increase: {energy_curve[-1] - energy_curve[0]:.2f}")

    print("\n3. Bookend arc (Strong open/close):")
    sequencer = NarrativeSequencer(arc_type=NarrativeArc.BOOKEND)
    sequenced = sequencer.sequence(sample_scenes, target_duration=30.0)
    energy_curve = sequencer.calculate_energy_curve(sequenced)

    print(f"   Opening energy: {energy_curve[0]:.2f}")
    print(f"   Middle energy: {energy_curve[len(energy_curve)//2]:.2f}")
    print(f"   Closing energy: {energy_curve[-1]:.2f}")


def example_complete_workflow():
    """Demonstrate complete hook + narrative workflow."""
    print("\n\n=== Complete Workflow Example ===\n")

    sample_scenes = [
        SceneInfo(i, i + 4, 4.0, 60 + i * 2, Path("footage.mp4")) for i in range(0, 40, 4)
    ]

    print("1. Generate hook sequence (3s)...")
    generator = HookGenerator()
    hook_segments = generator.create_hook_sequence(
        sample_scenes, HookPattern.DRAMATIC_REVEAL, hook_duration=3.0
    )
    hook_scene = hook_segments[0].scene
    print(f"   Hook scene score: {hook_scene.score:.1f}")

    print("\n2. Remove hook scene from available scenes...")
    remaining_scenes = [s for s in sample_scenes if s != hook_scene]
    print(f"   Remaining scenes: {len(remaining_scenes)}")

    print("\n3. Sequence remaining scenes (27s)...")
    sequencer = NarrativeSequencer(arc_type=NarrativeArc.CLASSIC)
    sequenced = sequencer.sequence(remaining_scenes, target_duration=27.0)

    print(f"   Sequenced {len(sequenced)} scenes")

    print("\n4. Calculate final energy curve...")
    energy_curve = sequencer.calculate_energy_curve(sequenced)

    print(f"   Peak energy: {max(energy_curve):.2f}")
    print(f"   Average energy: {sum(energy_curve)/len(energy_curve):.2f}")

    print("\n✓ Complete 30s video structured for maximum engagement!")


def example_beat_sync_integration():
    """Demonstrate integration with beat sync for music-aware sequencing."""
    print("\n\n=== Beat Sync Integration Example ===\n")

    print("Note: This example shows the API structure.")
    print("For actual use, you would:")
    print("  1. Analyze audio track with BeatSync")
    print("  2. Pass BeatInfo to NarrativeSequencer")
    print("  3. Get energy-aware scene sequencing\n")

    print("Example code:")
    print("""
    # Analyze music
    beat_sync = BeatSync()
    beat_info = beat_sync.analyze(Path("soundtrack.mp3"))

    # Create scenes
    detector = SceneDetector()
    scenes = detector.detect_scenes(Path("footage.mp4"))

    # Sequence with beat awareness
    sequencer = NarrativeSequencer(arc_type=NarrativeArc.CLASSIC)
    sequenced = sequencer.sequence(
        scenes,
        target_duration=30.0,
        beat_info=beat_info  # Enables music-aware sequencing
    )

    # Scenes will align with musical energy and structure
    """)


if __name__ == "__main__":
    example_hook_generation()
    example_narrative_sequencing()
    example_complete_workflow()
    example_beat_sync_integration()

    print("\n" + "=" * 60)
    print("Narrative module ready for viral drone reel creation!")
    print("=" * 60)
