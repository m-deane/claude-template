#!/usr/bin/env python3
"""
Complete vertical reel factory.

Every pipeline stage is explicit and configurable:
  D-Log detect → Scene detect → Beat sync → Diversity select
  → Stitch → Grade (BT.709) → Verify

Usage:
  python reel_factory.py ./clips/ ./music.mp3 ./output/reel.mp4
  python reel_factory.py ./clips/ ./music.mp3 ./output/reel.mp4 --duration 45
"""

import argparse
import gc
from pathlib import Path

from drone_reel import SceneDetector, VideoProcessor
from drone_reel.core.beat_sync import BeatSync
from drone_reel.core.color_grader import ColorGrader, ColorPreset
from drone_reel.core.video_processor import TransitionType
from drone_reel.utils.file_utils import find_video_files


def run(
    input_dir: Path,
    music_path: Path,
    output_path: Path,
    target_duration: float = 30.0,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # ── Stage 1: Discover footage + detect log profile ───────────────────
    videos = find_video_files(input_dir)
    if not videos:
        raise FileNotFoundError(f"No video files in {input_dir}")

    sample_colorspace = ColorGrader.detect_log_footage(videos[0])
    print(f"[1/7] {len(videos)} clips found  |  colorspace: {sample_colorspace}")

    # ── Stage 2: Scene detection + scoring ───────────────────────────────
    print("[2/7] Detecting scenes...")
    detector = SceneDetector(threshold=25.0, min_scene_length=1.5, max_scene_length=8.0)
    all_scenes = []
    for v in videos:
        try:
            scenes = detector.detect_scenes(v)
            all_scenes.extend(scenes)
        except Exception as e:
            print(f"      Skipping {v.name}: {e}")

    # Diversity selection: prefer scenes from different source files
    seen: set[str] = set()
    diverse: list = []
    for scene in sorted(all_scenes, key=lambda s: s.score, reverse=True):
        fname = scene.source_file.name
        if fname not in seen or len(diverse) < 4:
            diverse.append(scene)
            seen.add(fname)

    print(f"      {len(all_scenes)} scenes detected → {len(diverse)} diverse candidates")
    gc.collect()

    # ── Stage 3: Beat analysis ───────────────────────────────────────────
    print("[3/7] Analysing music...")
    beat_sync = BeatSync()
    beat_info = beat_sync.analyze(music_path)
    print(f"      {beat_info.tempo:.1f} BPM  |  {beat_info.beat_count} beats")

    cut_points = beat_sync.get_cut_points(
        beat_info,
        target_duration=target_duration,
        min_clip_length=1.5,
        max_clip_length=5.0,
        prefer_downbeats=True,
    )
    durations = beat_sync.calculate_clip_durations(cut_points, target_duration)
    print(f"      {len(cut_points)} cuts  |  {sum(durations):.1f}s total")

    # ── Stage 4: Clip selection ──────────────────────────────────────────
    n = min(len(durations), len(diverse))
    scenes = diverse[:n]
    durations = durations[:n]
    print(f"[4/7] Selected {n} clips")

    # Energy-mapped transitions
    transitions = []
    for i, cp in enumerate(cut_points[:n]):
        energy = beat_sync.get_energy_at_time(beat_info, cp.time)
        if i == n - 1:
            transitions.append(TransitionType.FADE_BLACK)
        elif energy > 0.70:
            transitions.append(TransitionType.WHIP_PAN)
        elif energy > 0.40:
            transitions.append(TransitionType.CROSSFADE)
        else:
            transitions.append(TransitionType.PARALLAX_LEFT)

    # ── Stage 5: Stitch ──────────────────────────────────────────────────
    print("[5/7] Stitching...")
    processor = VideoProcessor(output_fps=30, preset="medium")
    segments = processor.create_segments_from_scenes(
        scenes, durations, transitions=transitions, transition_duration=0.3,
    )
    raw = output_path.with_stem(output_path.stem + "_raw")
    processor.stitch_clips(
        segments, raw,
        audio_path=music_path,
        target_size=(1080, 1920),
        progress_callback=lambda p: print(f"\r      {p*100:.0f}%", end=""),
    )
    print()
    gc.collect()

    # ── Stage 6: Grade ───────────────────────────────────────────────────
    print("[6/7] Colour grading...")
    is_log = sample_colorspace != "rec709"
    grader = ColorGrader(
        preset=ColorPreset.DRONE_AERIAL,
        input_colorspace=sample_colorspace,
        auto_wb=is_log,           # Only correct WB when log footage detected
        denoise_strength=0.25 if is_log else 0.0,
        intensity=0.70,
        vignette_strength=0.32,
        halation_strength=0.20,
        gnd_sky_strength=0.30,
    )
    grader.grade_video(
        raw, output_path,
        progress_callback=lambda p: print(f"\r      {p*100:.0f}%", end=""),
    )
    print()
    raw.unlink(missing_ok=True)
    gc.collect()

    # ── Stage 7: Verify output ───────────────────────────────────────────
    if output_path.exists() and output_path.stat().st_size > 100_000:
        size_mb = output_path.stat().st_size / 1_048_576
        print(f"[7/7] Done → {output_path}  ({size_mb:.1f} MB)")
    else:
        raise RuntimeError(f"Output file is missing or too small: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Vertical reel factory")
    parser.add_argument("clips_dir", type=Path, help="Directory of source clips")
    parser.add_argument("music",     type=Path, help="Music file (.mp3, .wav)")
    parser.add_argument("output",    type=Path, help="Output .mp4 path")
    parser.add_argument("--duration", type=float, default=30.0, help="Target duration (s)")
    args = parser.parse_args()

    run(args.clips_dir, args.music, args.output, args.duration)


if __name__ == "__main__":
    main()
