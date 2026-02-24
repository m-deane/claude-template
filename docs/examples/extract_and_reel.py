#!/usr/bin/env python3
"""
Extract top clips from raw footage, then optionally build a reel.

Stage 1: Detect scenes in the source video(s)
Stage 2: Analyze, filter, and rank scenes by quality
Stage 3: Extract top N clips to disk with a JSON manifest
Stage 4: Beat-sync music (only if --music provided)
Stage 5: Stitch + colour grade a reel (only if --music provided)

Usage:
  # Extract 10 best clips only
  python extract_and_reel.py ./raw_flight.mp4 ./output/

  # Extract 8 clips and build a 30s reel with music
  python extract_and_reel.py ./raw_flight.mp4 ./output/ --music track.mp3 --count 8

  # Extract from a directory of clips
  python extract_and_reel.py ./footage/ ./output/ --music track.mp3 --duration 45
"""

import argparse
import gc
import json
from pathlib import Path

from drone_reel import SceneDetector, VideoProcessor
from drone_reel.core.beat_sync import BeatSync
from drone_reel.core.color_grader import ColorGrader, ColorPreset
from drone_reel.core.scene_analyzer import analyze_scenes_batch
from drone_reel.core.scene_filter import SceneFilter
from drone_reel.core.video_processor import ClipSegment, TransitionType
from drone_reel.utils.file_utils import find_video_files


def run(
    input_path: Path,
    output_dir: Path,
    music_path: Path | None,
    reel_output: Path,
    count: int,
    duration: float,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    clips_dir = output_dir / "clips"
    clips_dir.mkdir(exist_ok=True)

    # ── Stage 1: Detect scenes ─────────────────────────────────────────
    if input_path.is_file():
        videos = [input_path]
    else:
        videos = find_video_files(input_path)
    if not videos:
        raise FileNotFoundError(f"No video files found at {input_path}")

    print(f"[1/5] {len(videos)} source file(s) found")
    detector = SceneDetector(threshold=25.0, min_scene_length=1.5, max_scene_length=8.0)
    all_scenes = []
    for v in videos:
        try:
            all_scenes.extend(detector.detect_scenes(v))
        except Exception as e:
            print(f"      Skipping {v.name}: {e}")
    print(f"      {len(all_scenes)} scenes detected")

    # ── Stage 2: Filter + rank ─────────────────────────────────────────
    print("[2/5] Analysing and filtering...")
    analysis = analyze_scenes_batch(all_scenes, include_sharpness=True)

    motion_map = {sid: r["motion_energy"] for sid, r in analysis.items()}
    brightness_map = {sid: r["brightness"] for sid, r in analysis.items()}
    shake_map = {sid: r["shake_score"] for sid, r in analysis.items()}

    scene_filter = SceneFilter()
    result = scene_filter.filter_scenes(all_scenes, motion_map, brightness_map, shake_map)
    ranked = result.with_low_motion_if_needed(count)
    ranked.sort(key=lambda s: s.score, reverse=True)
    top = ranked[:count]
    print(f"      {len(result.all_passing)} passed filter → top {len(top)} selected")
    gc.collect()

    # ── Stage 3: Extract clips + manifest ──────────────────────────────
    print(f"[3/5] Extracting {len(top)} clips...")
    processor = VideoProcessor(output_fps=30, preset="medium")
    manifest = []
    for i, scene in enumerate(top):
        clip_path = clips_dir / f"clip_{i:03d}.mp4"
        segment = ClipSegment(scene=scene)
        clip = processor.extract_clip(segment)
        try:
            processor.write_clip(clip, clip_path)
        finally:
            clip.close()

        manifest.append({
            "index": i,
            "file": clip_path.name,
            "source": str(scene.source_file),
            "start": round(scene.start_time, 2),
            "end": round(scene.end_time, 2),
            "duration": round(scene.duration, 2),
            "score": round(scene.score, 2),
        })
        print(f"      {clip_path.name}  ({scene.duration:.1f}s, score {scene.score:.0f})")

    manifest_path = clips_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(f"      Manifest written to {manifest_path}")
    gc.collect()

    if not music_path:
        print("[4/5] No music provided — skipping reel creation")
        print(f"[5/5] Done. {len(top)} clips in {clips_dir}")
        return

    # ── Stage 4: Beat sync ─────────────────────────────────────────────
    print("[4/5] Analysing music...")
    beat_sync = BeatSync()
    beat_info = beat_sync.analyze(music_path)
    cut_points = beat_sync.get_cut_points(
        beat_info,
        target_duration=duration,
        min_clip_length=1.5,
        max_clip_length=5.0,
        prefer_downbeats=True,
    )
    clip_durations = beat_sync.calculate_clip_durations(cut_points, duration)
    print(f"      {beat_info.tempo:.1f} BPM  |  {len(cut_points)} cuts")

    # ── Stage 5: Stitch + grade ────────────────────────────────────────
    print("[5/5] Stitching reel...")
    n = min(len(clip_durations), len(top))
    scenes = top[:n]
    clip_durations = clip_durations[:n]

    transitions = [TransitionType.CROSSFADE] * (n - 1) + [TransitionType.FADE_BLACK]
    segments = processor.create_segments_from_scenes(
        scenes, clip_durations, transitions=transitions, transition_duration=0.3,
    )

    reel_output.parent.mkdir(parents=True, exist_ok=True)
    raw_path = reel_output.with_stem(reel_output.stem + "_raw")
    processor.stitch_clips(
        segments, raw_path,
        audio_path=music_path,
        target_size=(1080, 1920),
    )
    gc.collect()

    grader = ColorGrader(
        preset=ColorPreset.DRONE_AERIAL,
        intensity=0.65,
        vignette_strength=0.30,
    )
    grader.grade_video(raw_path, reel_output)
    raw_path.unlink(missing_ok=True)

    size_mb = reel_output.stat().st_size / 1_048_576
    print(f"      Reel saved to {reel_output}  ({size_mb:.1f} MB)")


def main():
    parser = argparse.ArgumentParser(
        description="Extract top clips from raw footage and optionally build a reel",
    )
    parser.add_argument("input", type=Path, help="Source video file or directory")
    parser.add_argument("output_dir", type=Path, help="Output directory for extracted clips")
    parser.add_argument("--music", type=Path, default=None, help="Music file for reel creation")
    parser.add_argument(
        "--reel-output", type=Path, default=None,
        help="Reel output path (default: <output_dir>/reel.mp4)",
    )
    parser.add_argument("--count", type=int, default=10, help="Number of clips to extract")
    parser.add_argument("--duration", type=float, default=30.0, help="Target reel duration (s)")
    args = parser.parse_args()

    reel_output = args.reel_output or args.output_dir / "reel.mp4"
    run(args.input, args.output_dir, args.music, reel_output, args.count, args.duration)


if __name__ == "__main__":
    main()
