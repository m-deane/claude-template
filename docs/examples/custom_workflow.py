#!/usr/bin/env python3
"""
Custom workflow example.

Demonstrates full control over the reel creation process including:
- Custom scene selection criteria
- Manual transition assignment
- Custom color grading
- Reframing with specific settings
"""

from pathlib import Path

from drone_reel import SceneDetector, VideoProcessor, ColorGrader, Reframer
from drone_reel.core.beat_sync import BeatSync
from drone_reel.core.video_processor import TransitionType, ClipSegment
from drone_reel.core.color_grader import ColorPreset, ColorAdjustments
from drone_reel.core.reframer import ReframeSettings, AspectRatio, ReframeMode
from drone_reel.utils.file_utils import find_video_files


def custom_scene_filter(scenes, min_score: float = 60.0):
    """Filter scenes by minimum quality score."""
    return [s for s in scenes if s.score >= min_score]


def create_custom_reel(
    input_dir: Path,
    output_path: Path,
    music_path: Path | None = None,
) -> Path:
    """
    Create a reel with full custom control.

    Args:
        input_dir: Directory containing video files
        output_path: Output video file path
        music_path: Optional music file

    Returns:
        Path to the created reel
    """
    video_files = find_video_files(input_dir)
    print(f"Found {len(video_files)} video files")

    # Step 1: Custom scene detection with stricter settings
    detector = SceneDetector(
        threshold=22.0,  # More sensitive = more scenes detected
        min_scene_length=2.0,  # Longer minimum scenes
        max_scene_length=6.0,  # Shorter maximum
    )

    all_scenes = []
    for video in video_files:
        scenes = detector.detect_scenes(video)
        all_scenes.extend(scenes)

    print(f"Detected {len(all_scenes)} total scenes")

    # Step 2: Custom filtering - only high-quality scenes
    quality_scenes = custom_scene_filter(all_scenes, min_score=60.0)
    quality_scenes.sort(key=lambda s: s.score, reverse=True)
    print(f"Filtered to {len(quality_scenes)} high-quality scenes")

    # Step 3: Beat analysis (if music provided)
    if music_path:
        beat_sync = BeatSync()
        beat_info = beat_sync.analyze(music_path)
        print(f"Music tempo: {beat_info.tempo:.1f} BPM")

        cut_points = beat_sync.get_cut_points(
            beat_info,
            target_duration=45.0,
            min_clip_length=2.0,
            max_clip_length=5.0,
            prefer_downbeats=True,
        )
        durations = beat_sync.calculate_clip_durations(cut_points, 45.0)
    else:
        # Fixed durations without music
        durations = [3.0, 4.0, 3.5, 4.0, 3.0, 4.5, 3.0, 4.0, 3.5, 3.5]

    # Step 4: Select scenes to match durations
    selected_scenes = quality_scenes[: len(durations)]

    # Step 5: Create segments with custom transitions
    # Manually assign transitions based on position
    transitions = []
    for i in range(len(selected_scenes)):
        if i == 0:
            transitions.append(TransitionType.FADE_BLACK)  # Start with fade in
        elif i == len(selected_scenes) - 1:
            transitions.append(TransitionType.FADE_BLACK)  # End with fade out
        elif i % 3 == 0:
            transitions.append(TransitionType.ZOOM_IN)  # Every 3rd clip: zoom
        else:
            transitions.append(TransitionType.CROSSFADE)  # Default: crossfade

    # Build ClipSegments manually for full control
    segments = []
    for i, (scene, duration) in enumerate(zip(selected_scenes, durations)):
        # Center the clip within the scene
        center_offset = max(0, (scene.duration - duration) / 2)

        segment = ClipSegment(
            scene=scene,
            start_offset=center_offset,
            duration=duration,
            transition_in=transitions[i - 1] if i > 0 else TransitionType.FADE_BLACK,
            transition_out=transitions[i],
            transition_duration=0.4,  # Slightly longer transitions
        )
        segments.append(segment)

    print(f"Created {len(segments)} clip segments")

    # Step 6: Stitch video
    processor = VideoProcessor(
        output_fps=30,
        preset="slow",  # Higher quality encoding
        threads=8,
    )

    temp_stitched = output_path.with_stem(output_path.stem + "_stitched")
    processor.stitch_clips(
        segments,
        temp_stitched,
        audio_path=music_path,
        target_size=(1080, 1920),
        progress_callback=lambda p: print(f"Stitching: {p * 100:.0f}%"),
    )

    # Step 7: Custom color grading
    custom_grade = ColorAdjustments(
        brightness=3,
        contrast=18,
        saturation=12,
        temperature=12,  # Slightly warm
        vibrance=20,
        shadows=8,
        highlights=-10,
        fade=3,  # Subtle lifted blacks
    )

    grader = ColorGrader(adjustments=custom_grade)
    temp_graded = output_path.with_stem(output_path.stem + "_graded")
    grader.grade_video(
        temp_stitched,
        temp_graded,
        progress_callback=lambda p: print(f"Grading: {p * 100:.0f}%"),
    )

    # Step 8: Final output (already reframed during stitching)
    temp_graded.rename(output_path)

    # Cleanup
    temp_stitched.unlink(missing_ok=True)

    print(f"Custom reel created: {output_path}")
    return output_path


def reframe_existing_video(input_path: Path, output_path: Path) -> Path:
    """
    Reframe an existing video to vertical format.

    Demonstrates standalone reframing functionality.
    """
    # Smart reframing with custom settings
    settings = ReframeSettings(
        target_ratio=AspectRatio.VERTICAL_9_16,
        mode=ReframeMode.SMART,  # Saliency-based tracking
        output_width=1080,
        smooth_tracking=True,
        tracking_smoothness=0.25,  # Very smooth tracking
    )

    reframer = Reframer(settings)
    reframer.reframe_video(
        input_path,
        output_path,
        progress_callback=lambda p: print(f"Reframing: {p * 100:.0f}%"),
    )

    print(f"Reframed video: {output_path}")
    return output_path


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python custom_workflow.py <input_directory> [music_file] [output_path]")
        print("       python custom_workflow.py --reframe <video_file> [output_path]")
        sys.exit(1)

    if sys.argv[1] == "--reframe":
        input_path = Path(sys.argv[2])
        output_path = Path(sys.argv[3]) if len(sys.argv) > 3 else input_path.with_stem(
            input_path.stem + "_vertical"
        )
        reframe_existing_video(input_path, output_path)
    else:
        input_dir = Path(sys.argv[1])
        music_path = Path(sys.argv[2]) if len(sys.argv) > 2 and not sys.argv[2].endswith(".mp4") else None
        output_path = Path(sys.argv[-1]) if sys.argv[-1].endswith(".mp4") else Path("./output/custom_reel.mp4")
        create_custom_reel(input_dir, output_path, music_path)
