#!/usr/bin/env python3
"""
Beat-synchronized reel creation example.

Creates a reel with cuts synchronized to music beats.
Uses librosa for beat detection and aligns video cuts with downbeats.
"""

from pathlib import Path

from drone_reel import SceneDetector, VideoProcessor, ColorGrader
from drone_reel.core.beat_sync import BeatSync
from drone_reel.core.video_processor import TransitionType
from drone_reel.core.color_grader import ColorPreset
from drone_reel.presets.transitions import get_transitions_for_energy
from drone_reel.utils.file_utils import find_video_files


def create_beat_synced_reel(
    input_dir: Path,
    music_path: Path,
    output_path: Path,
    target_duration: float = 45.0,
) -> Path:
    """
    Create a beat-synchronized reel from video clips.

    Args:
        input_dir: Directory containing video files
        music_path: Path to music file
        output_path: Output video file path
        target_duration: Target duration in seconds

    Returns:
        Path to the created reel
    """
    # Find all video files
    video_files = find_video_files(input_dir)
    if not video_files:
        raise ValueError(f"No video files found in {input_dir}")

    print(f"Found {len(video_files)} video files")

    # Analyze music
    print("Analyzing music...")
    beat_sync = BeatSync()
    beat_info = beat_sync.analyze(music_path)
    print(f"Detected tempo: {beat_info.tempo:.1f} BPM")
    print(f"Duration: {beat_info.duration:.1f}s")

    # Get cut points aligned with beats
    cut_points = beat_sync.get_cut_points(
        beat_info,
        target_duration=target_duration,
        min_clip_length=1.5,
        max_clip_length=4.0,
        prefer_downbeats=True,
    )
    print(f"Generated {len(cut_points)} cut points")

    # Calculate clip durations from cut points
    durations = beat_sync.calculate_clip_durations(cut_points, target_duration)
    num_clips = len(durations)

    # Detect and score scenes
    print("Analyzing scenes...")
    detector = SceneDetector(threshold=25.0)
    best_scenes = detector.get_top_scenes(video_files, count=num_clips)

    # Match scenes to durations (trim if needed)
    if len(best_scenes) < num_clips:
        print(f"Warning: Only {len(best_scenes)} scenes available, need {num_clips}")
        durations = durations[: len(best_scenes)]

    # Generate transitions based on music energy
    avg_energy = sum(
        beat_sync.get_energy_at_time(beat_info, cp.time) for cp in cut_points[:-1]
    ) / max(len(cut_points) - 1, 1)
    print(f"Average energy: {avg_energy:.2f}")

    transitions = get_transitions_for_energy(
        energy_level=avg_energy,
        count=len(durations),
        style="dynamic",
    )

    # Create segments
    processor = VideoProcessor(output_fps=30)
    segments = processor.create_segments_from_scenes(
        best_scenes[: len(durations)],
        durations,
        transitions=transitions,
        transition_duration=0.3,
    )

    # Stitch clips with music
    print("Stitching video...")
    temp_path = output_path.with_stem(output_path.stem + "_temp")
    processor.stitch_clips(
        segments,
        temp_path,
        audio_path=music_path,
        target_size=(1080, 1920),
        progress_callback=lambda p: print(f"Progress: {p * 100:.0f}%"),
    )

    # Apply color grading
    print("Applying color grade...")
    grader = ColorGrader(preset=ColorPreset.DRONE_AERIAL)
    grader.grade_video(temp_path, output_path)

    # Clean up
    temp_path.unlink()

    print(f"Beat-synced reel created: {output_path}")
    return output_path


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python beat_synced_reel.py <input_directory> <music_file> [output_path]")
        sys.exit(1)

    input_dir = Path(sys.argv[1])
    music_path = Path(sys.argv[2])
    output_path = Path(sys.argv[3]) if len(sys.argv) > 3 else Path("./output/reel.mp4")

    create_beat_synced_reel(input_dir, music_path, output_path)
