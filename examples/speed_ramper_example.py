"""
Example usage of the SpeedRamper system for drone video effects.

This demonstrates various speed ramping techniques including:
- Basic slow motion
- Beat-synchronized speed changes
- Auto-detected ramp points
- Multiple sequential ramps
"""

from pathlib import Path
import numpy as np

from drone_reel.core.speed_ramper import SpeedRamp, SpeedRamper
from drone_reel.core.scene_detector import SceneDetector, SceneInfo
from drone_reel.core.beat_sync import BeatSync
from moviepy import VideoFileClip


def example_1_basic_slow_motion():
    """Apply simple slow motion effect to a clip."""
    print("Example 1: Basic Slow Motion")
    print("-" * 50)

    ramper = SpeedRamper()

    # Create a slow-motion ramp from 2s to 4s
    ramp = SpeedRamp(
        start_time=2.0,
        end_time=4.0,
        start_speed=1.0,
        end_speed=0.5,  # 50% speed = 2x slower
        easing="ease_in_out",
    )

    print(f"Ramp: {ramp.start_time}s to {ramp.end_time}s")
    print(f"Speed: {ramp.start_speed}x -> {ramp.end_speed}x")
    print(f"Easing: {ramp.easing}")

    # Calculate how this affects duration
    original_duration = 10.0
    new_duration = ramper.calculate_ramped_duration(original_duration, [ramp])
    print(f"\nOriginal duration: {original_duration}s")
    print(f"New duration: {new_duration:.2f}s")
    print(f"Difference: +{new_duration - original_duration:.2f}s")

    # Apply to a real clip (commented out - requires actual video file)
    # clip = VideoFileClip("drone_footage.mp4")
    # ramped_clip = ramper.apply_ramp(clip, ramp)
    # ramped_clip.write_videofile("output_slow_motion.mp4")


def example_2_speed_up_effect():
    """Create a time-lapse style speed-up effect."""
    print("\n\nExample 2: Speed-Up Effect")
    print("-" * 50)

    ramper = SpeedRamper()

    # Speed up from 1x to 3x over 5 seconds
    ramp = SpeedRamp(
        start_time=0.0,
        end_time=5.0,
        start_speed=1.0,
        end_speed=3.0,  # 3x faster
        easing="ease_in",
    )

    original_duration = 10.0
    new_duration = ramper.calculate_ramped_duration(original_duration, [ramp])

    print(f"Speed-up from {ramp.start_speed}x to {ramp.end_speed}x")
    print(f"Original duration: {original_duration}s")
    print(f"New duration: {new_duration:.2f}s")
    print(f"Time saved: {original_duration - new_duration:.2f}s")


def example_3_multiple_ramps():
    """Apply multiple speed ramps in sequence."""
    print("\n\nExample 3: Multiple Sequential Ramps")
    print("-" * 50)

    ramper = SpeedRamper()

    # Create a sequence of ramps
    ramps = [
        # Start with slow motion
        SpeedRamp(
            start_time=1.0,
            end_time=3.0,
            start_speed=1.0,
            end_speed=0.5,
            easing="ease_in",
        ),
        # Return to normal
        SpeedRamp(
            start_time=3.0,
            end_time=4.0,
            start_speed=0.5,
            end_speed=1.0,
            easing="ease_out",
        ),
        # Speed up for action
        SpeedRamp(
            start_time=6.0,
            end_time=8.0,
            start_speed=1.0,
            end_speed=2.0,
            easing="ease_in_out",
        ),
    ]

    original_duration = 10.0
    new_duration = ramper.calculate_ramped_duration(original_duration, ramps)

    print(f"Applied {len(ramps)} speed ramps:")
    for i, ramp in enumerate(ramps, 1):
        print(
            f"  {i}. {ramp.start_time}s-{ramp.end_time}s: "
            f"{ramp.start_speed}x → {ramp.end_speed}x ({ramp.easing})"
        )

    print(f"\nOriginal duration: {original_duration}s")
    print(f"New duration: {new_duration:.2f}s")

    # Apply to clip (commented out)
    # clip = VideoFileClip("drone_footage.mp4")
    # ramped_clip = ramper.apply_multiple_ramps(clip, ramps)
    # ramped_clip.write_videofile("output_multiple_ramps.mp4")


def example_4_beat_synchronized():
    """Create ramps synchronized to music beats."""
    print("\n\nExample 4: Beat-Synchronized Ramps")
    print("-" * 50)

    ramper = SpeedRamper()

    # Simulate beat detection results
    beat_times = np.array([0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0])
    drop_times = np.array([2.0, 4.5])  # Beat drops/downbeats

    # Create beat-synced ramps
    ramps = ramper.create_beat_synced_ramps(
        clip_duration=10.0, beat_times=beat_times, drop_times=drop_times
    )

    print(f"Detected {len(beat_times)} beats")
    print(f"Detected {len(drop_times)} drops")
    print(f"Created {len(ramps)} beat-synced ramps:")

    for i, ramp in enumerate(ramps, 1):
        print(
            f"  {i}. {ramp.start_time:.2f}s-{ramp.end_time:.2f}s: "
            f"{ramp.start_speed}x → {ramp.end_speed}x"
        )

    # These ramps will:
    # - Slow down before each drop (build anticipation)
    # - Speed up on the drop (impact effect)
    # - Return to normal speed after

    # Apply to clip with music (commented out)
    # clip = VideoFileClip("drone_footage.mp4")
    # ramped_clip = ramper.apply_multiple_ramps(clip, ramps)
    # ramped_clip.write_videofile("output_beat_synced.mp4")


def example_5_auto_detection():
    """Auto-detect ramp opportunities from scene analysis."""
    print("\n\nExample 5: Auto-Detection")
    print("-" * 50)

    ramper = SpeedRamper()

    # Simulate a high-quality scenic moment
    scene = SceneInfo(
        start_time=0.0,
        end_time=8.0,
        duration=8.0,
        score=85.0,  # High score = good candidate for effects
        source_file=Path("drone_footage.mp4"),
    )

    # Auto-detect ramp opportunities
    ramps = ramper.auto_detect_ramp_points(scene)

    print(f"Scene duration: {scene.duration}s")
    print(f"Scene quality score: {scene.score}/100")
    print(f"Auto-detected {len(ramps)} ramp opportunities:")

    for i, ramp in enumerate(ramps, 1):
        effect = "slow-mo" if ramp.end_speed < ramp.start_speed else "speed-up"
        print(
            f"  {i}. {ramp.start_time:.2f}s-{ramp.end_time:.2f}s: "
            f"{effect} ({ramp.start_speed}x → {ramp.end_speed}x)"
        )

    # The auto-detection analyzes:
    # - Scene quality score
    # - Scene duration
    # - Optimal moments for slow motion
    # - Natural flow of the footage


def example_6_easing_comparison():
    """Compare different easing functions."""
    print("\n\nExample 6: Easing Function Comparison")
    print("-" * 50)

    ramper = SpeedRamper()

    # Create same ramp with different easing
    base_config = {
        "start_time": 2.0,
        "end_time": 4.0,
        "start_speed": 1.0,
        "end_speed": 0.5,
    }

    easing_types = ["linear", "ease_in", "ease_out", "ease_in_out"]

    print("Speed at 25%, 50%, 75% through ramp:\n")

    for easing in easing_types:
        ramp = SpeedRamp(**base_config, easing=easing)

        # Sample speeds at different points
        times = [2.5, 3.0, 3.5]  # 25%, 50%, 75% through the ramp
        speeds = [ramper._interpolate_speed(ramp, t) for t in times]

        print(f"{easing:15s} | ", end="")
        print(" | ".join(f"{s:.3f}x" for s in speeds))

    print("\nInterpretation:")
    print("  linear:       Constant rate of change")
    print("  ease_in:      Slow start, accelerates")
    print("  ease_out:     Fast start, decelerates")
    print("  ease_in_out:  Slow start and end, faster middle")


def example_7_full_workflow():
    """Complete workflow with scene detection and beat sync."""
    print("\n\nExample 7: Full Production Workflow")
    print("-" * 50)

    # This would be a complete workflow in production
    print("Production workflow steps:")
    print("1. Detect scenes in drone footage")
    print("2. Analyze music track for beats")
    print("3. Auto-detect ramp opportunities")
    print("4. Apply ramps with beat synchronization")
    print("5. Export final video")

    print("\nCode structure:")
    print(
        """
    # Detect scenes
    detector = SceneDetector()
    scenes = detector.detect_scenes(Path("drone_footage.mp4"))

    # Analyze music
    beat_sync = BeatSync()
    beat_info = beat_sync.analyze(Path("music.mp3"))

    # Auto-detect ramps with beat sync
    ramper = SpeedRamper()
    ramps = ramper.auto_detect_ramp_points(
        scene=scenes[0],
        beat_info=beat_info
    )

    # Apply ramps
    clip = VideoFileClip(str(scenes[0].source_file))
    ramped_clip = ramper.apply_multiple_ramps(clip, ramps)

    # Export
    ramped_clip.write_videofile("final_output.mp4")
    """
    )


if __name__ == "__main__":
    print("=" * 50)
    print("Speed Ramper Examples")
    print("=" * 50)

    example_1_basic_slow_motion()
    example_2_speed_up_effect()
    example_3_multiple_ramps()
    example_4_beat_synchronized()
    example_5_auto_detection()
    example_6_easing_comparison()
    example_7_full_workflow()

    print("\n" + "=" * 50)
    print("Examples complete!")
    print("=" * 50)
