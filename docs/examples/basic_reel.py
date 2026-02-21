#!/usr/bin/env python3
"""
Basic reel creation example.

Creates a simple reel from a folder of video clips without music.
Uses automatic scene detection and selection.
"""

from pathlib import Path

from drone_reel import SceneDetector, VideoProcessor, ColorGrader
from drone_reel.core.video_processor import TransitionType
from drone_reel.core.color_grader import ColorPreset
from drone_reel.utils.file_utils import find_video_files


def create_basic_reel(
    input_dir: Path,
    output_path: Path,
    target_duration: float = 30.0,
    num_clips: int = 10,
) -> Path:
    """
    Create a basic reel from video clips.

    Args:
        input_dir: Directory containing video files
        output_path: Output video file path
        target_duration: Target duration in seconds
        num_clips: Number of clips to include

    Returns:
        Path to the created reel
    """
    # Find all video files
    video_files = find_video_files(input_dir)
    if not video_files:
        raise ValueError(f"No video files found in {input_dir}")

    print(f"Found {len(video_files)} video files")

    # Detect and score scenes
    detector = SceneDetector(
        threshold=27.0,
        min_scene_length=1.0,
        max_scene_length=8.0,
    )

    print("Analyzing scenes...")
    best_scenes = detector.get_top_scenes(video_files, count=num_clips)
    print(f"Selected {len(best_scenes)} best scenes")

    # Calculate clip durations (evenly distributed)
    clip_duration = target_duration / len(best_scenes)
    durations = [clip_duration] * len(best_scenes)

    # Create transitions (crossfade between clips, fade out at end)
    transitions = [TransitionType.CROSSFADE] * (len(best_scenes) - 1)
    transitions.append(TransitionType.FADE_BLACK)

    # Create segments
    processor = VideoProcessor(output_fps=30)
    segments = processor.create_segments_from_scenes(
        best_scenes,
        durations,
        transitions=transitions,
        transition_duration=0.3,
    )

    # Stitch clips together
    print("Stitching video...")
    temp_path = output_path.with_stem(output_path.stem + "_temp")
    processor.stitch_clips(
        segments,
        temp_path,
        target_size=(1080, 1920),  # 9:16 vertical
        progress_callback=lambda p: print(f"Progress: {p * 100:.0f}%"),
    )

    # Apply color grading
    print("Applying color grade...")
    grader = ColorGrader(preset=ColorPreset.DRONE_AERIAL)
    grader.grade_video(temp_path, output_path)

    # Clean up temp file
    temp_path.unlink()

    print(f"Reel created: {output_path}")
    return output_path


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python basic_reel.py <input_directory> [output_path]")
        sys.exit(1)

    input_dir = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("./output/reel.mp4")

    create_basic_reel(input_dir, output_path)
