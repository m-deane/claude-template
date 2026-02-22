#!/usr/bin/env python3
"""
Narrative-arc reel: Hook → Build → Climax → Resolution.

Uses hook_tier scoring to place the emotionally strongest clip first,
builds energy through the middle, and closes with a calm resolution.
Ideal for weddings, events, travel films, and documentary-style content.

Usage:
  python narrative_reel.py ./event_clips/ ./music.mp3 ./output/event_reel.mp4
  python narrative_reel.py ./event_clips/ ./music.mp3 ./output/event_reel.mp4 --duration 60
"""

import sys
import argparse
from pathlib import Path

from drone_reel import SceneDetector, VideoProcessor, ColorGrader
from drone_reel.core.beat_sync import BeatSync
from drone_reel.core.video_processor import TransitionType
from drone_reel.core.color_grader import ColorPreset
from drone_reel.utils.file_utils import find_video_files


# Map hook tier names to numeric weights for sorting
HOOK_WEIGHTS = {"MAXIMUM": 5, "HIGH": 4, "MEDIUM": 3, "LOW": 2, "POOR": 1}


def narrative_sort(scenes: list, n: int) -> list:
    """
    Arrange n scenes into a Hook → Build → Climax → Resolution arc.

    Proportions: Hook 10% | Build 30% | Climax 40% | Resolution 20%
    """
    weighted = sorted(
        scenes,
        key=lambda s: (
            HOOK_WEIGHTS.get(getattr(s, "hook_tier", None) and s.hook_tier.name, 1),
            s.score,
        ),
        reverse=True,
    )[:n]

    n_hook       = max(1, round(n * 0.10))
    n_build      = max(1, round(n * 0.30))
    n_climax     = max(1, round(n * 0.40))
    n_resolution = max(1, n - n_hook - n_build - n_climax)

    hook       = weighted[:n_hook]
    build      = sorted(weighted[n_hook: n_hook + n_build],
                        key=lambda s: s.score)                # Ascending energy
    climax     = weighted[n_hook + n_build: n_hook + n_build + n_climax]
    resolution = sorted(
        weighted[n_hook + n_build + n_climax: n_hook + n_build + n_climax + n_resolution],
        key=lambda s: s.score,
    )                                                          # Quiet close

    return hook + build + climax + resolution


def arc_transitions(n: int) -> list[TransitionType]:
    """
    Assign transitions that match the emotional arc:
      - Open with fade
      - Build with crossfades
      - Climax with whip pans
      - Resolve with light leaks and a fade close
    """
    transitions = []
    for i in range(n):
        frac = i / max(n - 1, 1)
        if i == 0:
            transitions.append(TransitionType.FADE_BLACK)     # Soft open
        elif frac < 0.35:
            transitions.append(TransitionType.CROSSFADE)      # Gentle build
        elif frac < 0.75:
            transitions.append(TransitionType.WHIP_PAN)       # Peak energy
        elif i == n - 1:
            transitions.append(TransitionType.FADE_BLACK)     # Soft close
        else:
            transitions.append(TransitionType.LIGHT_LEAK)     # Warm resolution
    return transitions


def build_narrative_reel(
    input_dir: Path,
    music_path: Path,
    output_path: Path,
    target_duration: float = 60.0,
) -> None:
    """
    Build a narrative-arc reel.

    Args:
        input_dir: Directory containing source clips.
        music_path: Music file for beat synchronisation.
        output_path: Destination for finished reel.
        target_duration: Target length in seconds (60s recommended for events).
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # ── 1. Scene detection ───────────────────────────────────────────────
    videos = find_video_files(input_dir)
    if not videos:
        raise FileNotFoundError(f"No video files in {input_dir}")

    print(f"Found {len(videos)} clips")
    detector = SceneDetector(threshold=25.0, min_scene_length=2.0, max_scene_length=8.0)
    all_scenes = []
    for v in videos:
        try:
            all_scenes.extend(detector.detect_scenes(v))
        except Exception as e:
            print(f"  Skipping {v.name}: {e}")

    # Apply quality threshold — narrative arcs need decent raw material
    quality = [s for s in all_scenes if s.score >= 45.0]
    if len(quality) < 5:
        print(f"Warning: only {len(quality)} quality scenes (score ≥ 45), "
              "lowering threshold to 30")
        quality = [s for s in all_scenes if s.score >= 30.0]

    print(f"Detected {len(all_scenes)} scenes, {len(quality)} meet quality threshold")

    # ── 2. Beat sync ─────────────────────────────────────────────────────
    beat_sync = BeatSync()
    beat_info = beat_sync.analyze(music_path)
    print(f"Music: {beat_info.tempo:.1f} BPM, {beat_info.duration:.0f}s")

    cut_points = beat_sync.get_cut_points(
        beat_info,
        target_duration=target_duration,
        min_clip_length=2.5,
        max_clip_length=6.0,
        prefer_downbeats=True,
    )
    durations = beat_sync.calculate_clip_durations(cut_points, target_duration)

    n = min(len(durations), len(quality))
    durations = durations[:n]

    # ── 3. Narrative ordering ────────────────────────────────────────────
    arc = narrative_sort(quality, n)

    print(f"\nNarrative arc ({n} clips):")
    section_labels = (
        ["HOOK"]
        + ["BUILD"] * max(1, round(n * 0.30))
        + ["CLIMAX"] * max(1, round(n * 0.40))
        + ["RESOLUTION"] * max(1, n - 1 - round(n * 0.30) - round(n * 0.40))
    )
    for i, (scene, label) in enumerate(zip(arc, section_labels)):
        tier = getattr(scene, "hook_tier", None)
        tier_name = tier.name if tier else "N/A"
        print(f"  {i+1:02d}. [{label:<10}] {scene.source_file.name:30s} "
              f"score={scene.score:.0f}  tier={tier_name}")

    # ── 4. Stitch ────────────────────────────────────────────────────────
    transitions = arc_transitions(n)
    processor = VideoProcessor(output_fps=30, preset="medium")
    segments = processor.create_segments_from_scenes(
        arc, durations,
        transitions=transitions,
        transition_duration=0.4,   # Slightly longer for emotional pacing
    )

    raw = output_path.with_stem(output_path.stem + "_raw")
    print("\nStitching...")
    processor.stitch_clips(
        segments, raw,
        audio_path=music_path,
        target_size=(1080, 1920),
        progress_callback=lambda p: print(f"\r  {p*100:.0f}%", end=""),
    )
    print()

    # ── 5. Grade — warm, film-like ───────────────────────────────────────
    print("Grading...")
    grader = ColorGrader(
        preset=ColorPreset.FILM_EMULATION,
        intensity=0.65,
        vignette_strength=0.35,
        halation_strength=0.30,     # Warm glow around highlights
        chromatic_aberration_strength=0.08,  # Very subtle lens character
    )
    grader.grade_video(
        raw, output_path,
        progress_callback=lambda p: print(f"\r  {p*100:.0f}%", end=""),
    )
    print()
    raw.unlink(missing_ok=True)

    size_mb = output_path.stat().st_size / 1_048_576
    print(f"Done → {output_path}  ({size_mb:.1f} MB)")


def main():
    parser = argparse.ArgumentParser(
        description="Narrative-arc reel: Hook → Build → Climax → Resolution"
    )
    parser.add_argument("clips_dir", type=Path, help="Directory of source clips")
    parser.add_argument("music",     type=Path, help="Music file (.mp3, .wav)")
    parser.add_argument("output",    type=Path, help="Output .mp4 path")
    parser.add_argument("--duration", type=float, default=60.0,
                        help="Target reel duration in seconds (default: 60)")
    args = parser.parse_args()

    build_narrative_reel(args.clips_dir, args.music, args.output, args.duration)


if __name__ == "__main__":
    main()
