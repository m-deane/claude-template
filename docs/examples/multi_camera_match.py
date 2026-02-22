#!/usr/bin/env python3
"""
Multi-camera colour matching workflow.

When clips come from different cameras, different white balance settings,
or different lighting conditions, this script normalises all clips to match
a single reference clip using per-channel histogram CDF matching.

Usage:
  python multi_camera_match.py ./mixed_clips/ ./music.mp3 ./output/reel.mp4
  python multi_camera_match.py ./mixed_clips/ ./music.mp3 ./output/reel.mp4 ./reference.mp4
"""

import sys
import cv2
from pathlib import Path

from drone_reel import SceneDetector, VideoProcessor, ColorGrader
from drone_reel.core.beat_sync import BeatSync
from drone_reel.core.video_processor import TransitionType
from drone_reel.core.color_grader import ColorGrader, ColorPreset
from drone_reel.utils.file_utils import find_video_files


def read_first_frame(video_path: Path):
    """Return the first readable frame from a video, or None."""
    cap = cv2.VideoCapture(str(video_path))
    ret, frame = cap.read()
    cap.release()
    return frame if ret else None


def create_matched_reel(
    input_dir: Path,
    music_path: Path,
    output_path: Path,
    reference_path: Path | None = None,
    target_duration: float = 30.0,
) -> None:
    """
    Create a reel with consistent colour across all source clips.

    Args:
        input_dir: Directory containing clips from multiple cameras.
        music_path: Path to music file.
        output_path: Destination for the finished reel.
        reference_path: Optional video to use as colour reference.
                        If None, the highest-scoring clip is used.
        target_duration: Target reel length in seconds.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # ── 1. Find clips ────────────────────────────────────────────────────
    videos = find_video_files(input_dir)
    if not videos:
        raise FileNotFoundError(f"No video files in {input_dir}")
    print(f"Found {len(videos)} clips")

    # ── 2. Scene detection ───────────────────────────────────────────────
    print("Detecting scenes...")
    detector = SceneDetector(threshold=26.0, min_scene_length=1.5, max_scene_length=8.0)
    all_scenes = []
    for v in videos:
        try:
            all_scenes.extend(detector.detect_scenes(v))
        except Exception as e:
            print(f"  Skipping {v.name}: {e}")

    all_scenes.sort(key=lambda s: s.score, reverse=True)
    print(f"Detected {len(all_scenes)} scenes")

    # ── 3. Beat sync ─────────────────────────────────────────────────────
    beat_sync = BeatSync()
    beat_info = beat_sync.analyze(music_path)
    print(f"Music: {beat_info.tempo:.1f} BPM")

    cut_points = beat_sync.get_cut_points(
        beat_info,
        target_duration=target_duration,
        min_clip_length=2.0,
        max_clip_length=5.0,
        prefer_downbeats=True,
    )
    durations = beat_sync.calculate_clip_durations(cut_points, target_duration)
    n = min(len(durations), len(all_scenes))
    scenes, durations = all_scenes[:n], durations[:n]

    # ── 4. Determine colour reference frame ──────────────────────────────
    if reference_path is not None:
        print(f"Using reference: {reference_path.name}")
        reference_frame = read_first_frame(reference_path)
        if reference_frame is None:
            raise RuntimeError(f"Could not read reference video: {reference_path}")
    else:
        # Use the first frame of the highest-scoring scene as reference
        best_scene = scenes[0]
        reference_frame = read_first_frame(best_scene.source_file)
        if reference_frame is not None:
            print(f"Auto reference: {best_scene.source_file.name} (score={best_scene.score:.0f})")
        else:
            reference_frame = None
            print("Warning: could not read reference frame; skipping colour match")

    # ── 5. Stitch ────────────────────────────────────────────────────────
    transitions = [TransitionType.CROSSFADE] * (n - 1) + [TransitionType.FADE_BLACK]
    processor = VideoProcessor(output_fps=30, preset="medium")
    segments = processor.create_segments_from_scenes(
        scenes, durations, transitions=transitions, transition_duration=0.3,
    )

    raw = output_path.with_stem(output_path.stem + "_raw")
    print("Stitching...")
    processor.stitch_clips(
        segments, raw,
        audio_path=music_path,
        target_size=(1080, 1920),
        progress_callback=lambda p: print(f"\r  {p*100:.0f}%", end=""),
    )
    print()

    # ── 6. Colour-matched grade ───────────────────────────────────────────
    print("Grading with colour match...")
    grader = ColorGrader(
        preset=ColorPreset.CINEMATIC,
        auto_wb=True,
        denoise_strength=0.25,
        intensity=0.70,
        vignette_strength=0.30,
    )

    if reference_frame is not None:
        grader.set_reference_frame(reference_frame)
        print("  Colour matching enabled")

    grader.grade_video(
        raw, output_path,
        progress_callback=lambda p: print(f"\r  {p*100:.0f}%", end=""),
    )
    print()
    raw.unlink(missing_ok=True)

    size_mb = output_path.stat().st_size / 1_048_576
    print(f"Done → {output_path}  ({size_mb:.1f} MB)")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python multi_camera_match.py <clips_dir> <music.mp3> <output.mp4> [reference.mp4]")
        sys.exit(1)

    ref = Path(sys.argv[4]) if len(sys.argv) > 4 else None
    create_matched_reel(
        input_dir=Path(sys.argv[1]),
        music_path=Path(sys.argv[2]),
        output_path=Path(sys.argv[3]),
        reference_path=ref,
    )
