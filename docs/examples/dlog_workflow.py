#!/usr/bin/env python3
"""
D-Log M normalisation workflow.

For DJI cameras (Mini 3 Pro, Air 3, Mavic 3) shooting in D-Log M.
Normalises the flat log footage to Rec.709 before applying a grade.

Usage:
  python dlog_workflow.py ./dlog_clips/ ./music.mp3 ./output/reel.mp4
"""

import sys
from pathlib import Path

from drone_reel import SceneDetector, VideoProcessor, ColorGrader
from drone_reel.core.beat_sync import BeatSync
from drone_reel.core.video_processor import TransitionType
from drone_reel.core.color_grader import ColorGrader, ColorPreset
from drone_reel.utils.file_utils import find_video_files


def create_dlog_reel(
    input_dir: Path,
    music_path: Path,
    output_path: Path,
    target_duration: float = 30.0,
    input_colorspace: str = "dlog_m",
) -> None:
    """
    Create a reel from D-Log (or other log) drone footage.

    Args:
        input_dir: Directory containing log-encoded video files.
        music_path: Path to the music file.
        output_path: Destination for the finished reel.
        target_duration: Target reel length in seconds.
        input_colorspace: Log profile: 'dlog', 'dlog_m', 'slog3', or 'auto'.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # ── 1. Auto-detect log profile if requested ──────────────────────────
    videos = find_video_files(input_dir)
    if not videos:
        raise FileNotFoundError(f"No video files found in {input_dir}")

    if input_colorspace == "auto":
        detected = ColorGrader.detect_log_footage(videos[0])
        print(f"Auto-detected colorspace: {detected}")
        input_colorspace = detected

    print(f"Input colorspace: {input_colorspace}")
    print(f"Found {len(videos)} clips")

    # ── 2. Scene detection ───────────────────────────────────────────────
    print("Detecting scenes...")
    detector = SceneDetector(threshold=25.0, min_scene_length=2.0, max_scene_length=8.0)
    all_scenes = []
    for video in videos:
        try:
            scenes = detector.detect_scenes(video)
            all_scenes.extend(scenes)
            print(f"  {video.name}: {len(scenes)} scenes")
        except Exception as e:
            print(f"  Skipping {video.name}: {e}")

    if not all_scenes:
        raise RuntimeError("No scenes detected. Check that your video files are readable.")

    # Sort by quality score, best first
    all_scenes.sort(key=lambda s: s.score, reverse=True)
    print(f"Total scenes: {len(all_scenes)}, best score: {all_scenes[0].score:.1f}")

    # ── 3. Beat sync ─────────────────────────────────────────────────────
    print("Analysing music...")
    beat_sync = BeatSync()
    beat_info = beat_sync.analyze(music_path)
    print(f"  Tempo: {beat_info.tempo:.1f} BPM, {beat_info.beat_count} beats")

    cut_points = beat_sync.get_cut_points(
        beat_info,
        target_duration=target_duration,
        min_clip_length=2.0,
        max_clip_length=5.0,
        prefer_downbeats=True,
    )
    durations = beat_sync.calculate_clip_durations(cut_points, target_duration)

    n = min(len(durations), len(all_scenes))
    scenes = all_scenes[:n]
    durations = durations[:n]
    print(f"  Using {n} clips over {sum(durations):.1f}s")

    # ── 4. Stitch ────────────────────────────────────────────────────────
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

    # ── 5. Grade with D-Log normalisation ────────────────────────────────
    print(f"Grading (normalising {input_colorspace} → Rec.709)...")
    grader = ColorGrader(
        preset=ColorPreset.DRONE_AERIAL,
        # Core colour science
        input_colorspace=input_colorspace,  # Inverse log curve applied first
        auto_wb=True,                        # Gray-world white balance correction
        denoise_strength=0.3,                # Light denoising common on log footage
        # Creative
        intensity=0.70,
        vignette_strength=0.30,
        halation_strength=0.20,
        gnd_sky_strength=0.35,
    )

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
        print("Usage: python dlog_workflow.py <clips_dir> <music.mp3> <output.mp4> [colorspace]")
        print("       colorspace: dlog | dlog_m | slog3 | auto  (default: dlog_m)")
        sys.exit(1)

    colorspace = sys.argv[4] if len(sys.argv) > 4 else "dlog_m"
    create_dlog_reel(
        input_dir=Path(sys.argv[1]),
        music_path=Path(sys.argv[2]),
        output_path=Path(sys.argv[3]),
        input_colorspace=colorspace,
    )
