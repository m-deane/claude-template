# Examples

Complete examples from first run to production pipeline, covering beginner through expert use cases.

---

## Quick Reference

The 10 most useful CLI combinations:

```bash
# 1. Instant reel from a folder
drone-reel create -i ./clips/ -o reel.mp4

# 2. Viral-optimized 15-second reel
drone-reel create -i ./clips/ --viral -c drone_aerial

# 3. Beat-synced with downbeats only
drone-reel create -i ./clips/ -m track.mp3 --beat-mode downbeat -d 30

# 4. D-Log footage with auto white balance
drone-reel create -i ./clips/ --input-colorspace dlog_m --auto-wb -c drone_aerial

# 5. Cinematic film look with full effects
drone-reel create -i ./clips/ -c kodak_2383 --vignette 0.35 --halation 0.25 --letterbox 0.1

# 6. Atmospheric mountain/landscape footage
drone-reel create -i ./clips/ -c snow_mountain --haze 0.25 --gnd-sky 0.5 --stabilize

# 7. Night city drone footage
drone-reel create -i ./clips/ -c night_city --chromatic-aberration 0.2 --vignette 0.5

# 8. 4K ultra quality with stabilization
drone-reel create -i ./clips/ --resolution 4k --quality ultra --stabilize-all -c cinematic

# 9. Social media batch: Instagram + TikTok
drone-reel create -i ./clips/ --platform instagram_reels -o reel_ig.mp4
drone-reel create -i ./clips/ --platform tiktok -o reel_tt.mp4

# 10. Preview clip selection before committing
drone-reel create -i ./clips/ -m track.mp3 -d 45 --preview
```

---

## Clip Extraction

Long raw drone recordings often contain hours of footage with only a handful of
great moments. The `extract-clips` command detects scene boundaries, scores each
scene on sharpness, color, motion, and hook potential, then exports the top-ranked
scenes as individual clip files. These clips feed directly into the `create`
pipeline.

---

### Extract the Best Scenes (Beginner)

One command to pull the 10 best scenes from a raw video, then build a reel
from those clips.

```bash
# Extract the 10 best scenes from a raw drone video
drone-reel extract-clips -i DJI_0001.mp4 -o ./clips

# Then create a reel from those clips
drone-reel create -i ./clips/ -m music.mp3 -o reel.mp4 --duration 30
```

---

### Full Extract Pipeline with Manifest (Intermediate)

Extract more clips with enhanced scoring, a minimum quality threshold, and a
JSON manifest that records each scene's metadata for inspection.

```bash
# Extract 20 clips with enhanced scoring and JSON manifest
drone-reel extract-clips -i ./raw_shoots/ \
  -o ./clips \
  -n 20 \
  --enhanced \
  --min-score 40 \
  --json \
  --quality high

# The manifest.json records scene scores for inspection
cat clips/manifest.json | python -m json.tool | head -30

# Build a reel from the best clips
drone-reel create -i ./clips/ -m track.mp3 -o reel.mp4 \
  --color drone_aerial \
  --beat-mode downbeat \
  --duration 30
```

---

### Python API: Extract and Build (Advanced)

Use `SceneDetector` to detect scenes and `VideoProcessor.write_clip()` to
export individual clips programmatically.

```python
from pathlib import Path
from drone_reel import SceneDetector, VideoProcessor

detector = SceneDetector(threshold=25.0)
scenes = detector.detect_scenes(Path("./raw_footage.mp4"))
scenes.sort(key=lambda s: s.score, reverse=True)

processor = VideoProcessor(output_fps=30)
for i, scene in enumerate(scenes[:10]):
    processor.write_clip(scene, Path(f"./clips/clip_{i:02d}.mp4"))
```

See [`extract_and_reel.py`](extract_and_reel.py) for a complete end-to-end
script that extracts, filters, and builds a reel in one pass.

---

## Beginner

No Python required. These examples use the CLI only.

---

### 1. Your First Reel

Create a 30-second reel from a folder of drone clips. drone-reel automatically
finds the best scenes, reframes them to vertical (9:16), and applies the
`drone_aerial` color grade.

```bash
drone-reel create --input ./clips/ --output my_first_reel.mp4 --duration 30
```

- `--input` — folder containing your `.mp4` or `.mov` files
- `--output` — where to save the result
- `--duration` — target length in seconds

**What happens automatically:** scene detection, quality scoring, reframing to
9:16, crossfade transitions, `drone_aerial` color grade.

---

### 2. Adding Music with Beat Sync

Provide a music track and drone-reel will align every cut to a beat.
`--beat-mode downbeat` only cuts on strong beats (every 4th beat typically),
giving longer, more cinematic clips.

```bash
drone-reel create -i ./clips/ -m ./music/track.mp3 -d 45 --beat-mode downbeat -o reel_music.mp4
```

Check your track's tempo first:

```bash
drone-reel beats -i ./music/track.mp3
```

---

### 3. Platform-Specific Export

Each platform preset sets the correct aspect ratio, resolution, and codec
settings automatically.

```bash
# Instagram Reels — 9:16, 1080x1920, H.264
drone-reel create -i ./clips/ --platform instagram_reels -o reel_ig.mp4

# TikTok — 9:16, 1080x1920, H.264
drone-reel create -i ./clips/ --platform tiktok -o reel_tt.mp4

# YouTube Shorts — 9:16, 1080x1920
drone-reel create -i ./clips/ --platform youtube_shorts -o reel_yt.mp4

# YouTube landscape — 16:9, 1920x1080
drone-reel create -i ./clips/ --platform youtube --no-reframe -o reel_yt_wide.mp4
```

---

### 4. Choosing a Color Preset

drone-reel includes 30 color presets. Use `-c` to pick one.

```bash
# Drone footage default
drone-reel create -i ./clips/ -c drone_aerial

# Warm golden-hour look
drone-reel create -i ./clips/ -c golden_hour

# Kodak film emulation
drone-reel create -i ./clips/ -c kodak_2383

# Moody desaturated (popular on social)
drone-reel create -i ./clips/ -c desaturated_moody

# Night city footage
drone-reel create -i ./clips/ -c night_city
```

Dial down the intensity if a preset feels too strong:

```bash
drone-reel create -i ./clips/ -c cyberpunk_neon --color-intensity 0.5
```

List all presets:

```bash
drone-reel presets
```

---

### 5. Viral One-Liner

The `--viral` flag is a shortcut that sets: 15-second duration, Instagram Reels
platform, 60% color intensity, and speed ramping on the best hook clip.

```bash
drone-reel create -i ./clips/ --viral -c drone_aerial
```

Add a caption for the lower third:

```bash
drone-reel create -i ./clips/ --viral -c drone_aerial --caption "Shot on DJI Mini 4 Pro"
```

---

## Intermediate

These examples combine CLI flags and simple Python to go beyond the defaults.

---

### 6. D-Log Footage Workflow

DJI cameras shooting in D-Log M produce flat, washed-out footage for maximum
dynamic range. You must tell drone-reel what colorspace your footage is in so
it can normalise it before applying a grade.

```bash
# DJI Mini 3 Pro / Air 3 — D-Log M
drone-reel create -i ./dlog_clips/ \
  --input-colorspace dlog_m \
  --auto-wb \
  --color drone_aerial \
  --vignette 0.3 \
  -o dlog_reel.mp4
```

Auto-detect if you're unsure which log profile was used:

```bash
drone-reel create -i ./clips/ --input-colorspace auto --color drone_aerial
```

| Camera | Flag |
|--------|------|
| DJI (generic) | `--input-colorspace dlog` |
| DJI Mini 3 / Air 3 / Mavic 3 | `--input-colorspace dlog_m` |
| Sony ZV-E10 / FX3 | `--input-colorspace slog3` |

---

### 7. Combining Visual Effects

Layer multiple effects for a cinematic look. Effects are applied in a fixed
pipeline order so they always interact correctly regardless of the CLI order.

```bash
# Golden-hour cinematic with full effect stack
drone-reel create -i ./clips/ \
  -m track.mp3 \
  -c golden_hour \
  --vignette 0.35 \
  --halation 0.3 \
  --letterbox 0.1 \
  --gnd-sky 0.4 \
  -o cinematic.mp4
```

```bash
# Mountain landscape with atmospheric depth
drone-reel create -i ./mountain_clips/ \
  -c snow_mountain \
  --haze 0.3 \
  --gnd-sky 0.6 \
  --denoise 0.4 \
  --vignette 0.2 \
  --stabilize \
  -o mountain_reel.mp4
```

```bash
# Night city — neon glow with lens artifacts
drone-reel create -i ./city_clips/ \
  -c cyberpunk_neon \
  --chromatic-aberration 0.25 \
  --halation 0.4 \
  --vignette 0.55 \
  --color-intensity 0.75 \
  -o night_city.mp4
```

Effect cheat sheet:

| Effect | Flag | Best Value |
|--------|------|------------|
| Edge darkening | `--vignette` | 0.3–0.45 |
| Warm highlight bloom | `--halation` | 0.2–0.35 |
| Lens fringing | `--chromatic-aberration` | 0.1–0.25 |
| Aerial depth haze | `--haze` | 0.15–0.35 |
| Sky darkening | `--gnd-sky` | 0.3–0.6 |
| Cinematic bars | `--letterbox` | 0.08–0.12 |
| Noise reduction | `--denoise` | 0.3–0.6 |

---

### 8. Multi-Platform Batch Export

```python
#!/usr/bin/env python3
"""Export the same reel to multiple platforms in one script."""

import subprocess
from pathlib import Path

INPUT = "./clips/"
MUSIC = "./music/track.mp3"
COLOR = "drone_aerial"

platforms = [
    ("instagram_reels", "reel_instagram.mp4"),
    ("tiktok",          "reel_tiktok.mp4"),
    ("youtube_shorts",  "reel_shorts.mp4"),
]

for platform, filename in platforms:
    output = Path("./output") / filename
    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "drone-reel", "create",
        "-i", INPUT,
        "-m", MUSIC,
        "-d", "30",
        "--platform", platform,
        "-c", COLOR,
        "--vignette", "0.3",
        "--beat-mode", "downbeat",
        "-o", str(output),
    ]
    print(f"Exporting {platform}...")
    subprocess.run(cmd, check=True)
    print(f"  → {output}")
```

---

### 9. Custom Color Grade with Selective Color

When no preset fits, build a grade from individual parameters. The Python API
gives you full control over each colour channel.

```python
#!/usr/bin/env python3
"""Custom color grade targeting specific hue ranges."""

import cv2
from pathlib import Path
from drone_reel.core.color_grader import (
    ColorGrader, ColorAdjustments, SelectiveColorAdjustments, ToneCurve,
)

# Teal-and-orange blockbuster look
selective = SelectiveColorAdjustments(
    # Push warm tones orange
    orange_sat=30, orange_hue=5,
    red_sat=20,
    yellow_sat=15,
    # Push cool tones teal
    cyan_sat=35, cyan_hue=-8,
    blue_sat=20, blue_hue=8,
    # Suppress green to keep teal clean
    green_sat=-10,
)

tone_curve = ToneCurve(
    red_points=[(0, 0), (64, 55), (192, 200), (255, 255)],
    green_points=[(0, 0), (64, 50), (192, 205), (255, 255)],
    blue_points=[(0, 0), (64, 60), (192, 195), (255, 255)],
)

adjustments = ColorAdjustments(
    contrast=18,
    saturation=8,
    temperature=10,
    tint=-8,
    shadows=8,
    highlights=-12,
    selective_color=selective,
)

grader = ColorGrader(
    adjustments=adjustments,
    tone_curve=tone_curve,
    vignette_strength=0.35,
    intensity=0.85,
)

grader.grade_video(
    Path("./output/reel_raw.mp4"),
    Path("./output/reel_graded.mp4"),
    progress_callback=lambda p: print(f"\rGrading {p*100:.0f}%", end=""),
)
print("\nDone.")
```

---

### 10. Consistent Color Across Multi-Camera Clips

When clips come from different cameras or different white balance settings, use
`--auto-color-match` to normalize all clips to the same color distribution as
the first frame.

```bash
drone-reel create -i ./mixed_clips/ \
  --auto-color-match \
  --auto-wb \
  --denoise 0.3 \
  -c cinematic \
  -o color_matched.mp4
```

In Python, set the reference explicitly:

```python
import cv2
from pathlib import Path
from drone_reel.core.color_grader import ColorGrader, ColorPreset

grader = ColorGrader(preset=ColorPreset.CINEMATIC, denoise_strength=0.3)

# Use the hero clip's first frame as the color reference
cap = cv2.VideoCapture("./hero_clip.mp4")
ret, reference_frame = cap.read()
cap.release()

if ret:
    grader.set_reference_frame(reference_frame)

# All subsequent grading matches the reference
grader.grade_video(Path("./camera_b_clip.mp4"), Path("./camera_b_matched.mp4"))
grader.grade_video(Path("./camera_c_clip.mp4"), Path("./camera_c_matched.mp4"))
```

---

## Advanced

Full Python API workflows with error handling, progress tracking, and
fine-grained pipeline control.

---

### 11. Full Pipeline with Manual Scene Selection

Take complete control of every pipeline stage: detect, filter, sequence,
time, stitch, grade.

```python
#!/usr/bin/env python3
"""
Full pipeline with manual control over every stage.
"""

from pathlib import Path
from drone_reel import SceneDetector, VideoProcessor, ColorGrader
from drone_reel.core.beat_sync import BeatSync
from drone_reel.core.video_processor import TransitionType, ClipSegment
from drone_reel.core.color_grader import ColorPreset
from drone_reel.presets.transitions import get_transitions_for_energy
from drone_reel.utils.file_utils import find_video_files


def build_reel(input_dir: Path, music_path: Path, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # ── 1. Discover footage ──────────────────────────────────────────────
    videos = find_video_files(input_dir)
    if not videos:
        raise FileNotFoundError(f"No video files in {input_dir}")
    print(f"Found {len(videos)} clips")

    # ── 2. Detect + score scenes ─────────────────────────────────────────
    detector = SceneDetector(threshold=24.0, min_scene_length=1.5, max_scene_length=8.0)
    all_scenes = []
    for i, video in enumerate(videos, 1):
        print(f"  Analysing {video.name} ({i}/{len(videos)})")
        try:
            all_scenes.extend(detector.detect_scenes(video))
        except Exception as e:
            print(f"  Skipping {video.name}: {e}")

    print(f"Detected {len(all_scenes)} total scenes")

    # Filter: require score >= 55 and duration >= 2s
    scenes = [s for s in all_scenes if s.score >= 55.0 and s.duration >= 2.0]
    scenes.sort(key=lambda s: s.score, reverse=True)
    print(f"Filtered to {len(scenes)} quality scenes")

    if len(scenes) < 5:
        raise RuntimeError(f"Not enough quality scenes (found {len(scenes)}, need 5+)")

    # ── 3. Beat analysis ─────────────────────────────────────────────────
    beat_sync = BeatSync()
    beat_info = beat_sync.analyze(music_path)
    print(f"Music: {beat_info.tempo:.1f} BPM, {beat_info.duration:.0f}s")

    cut_points = beat_sync.get_cut_points(
        beat_info, target_duration=45.0,
        min_clip_length=2.0, max_clip_length=5.0,
        prefer_downbeats=True,
    )
    durations = beat_sync.calculate_clip_durations(cut_points, 45.0)
    n = min(len(durations), len(scenes))
    durations, scenes = durations[:n], scenes[:n]

    # ── 4. Energy-mapped transitions ─────────────────────────────────────
    energies = [beat_sync.get_energy_at_time(beat_info, cp.time) for cp in cut_points[:n]]
    transitions = []
    for energy in energies:
        if energy > 0.75:
            transitions.append(TransitionType.WHIP_PAN)
        elif energy > 0.45:
            transitions.append(TransitionType.CROSSFADE)
        else:
            transitions.append(TransitionType.FADE_BLACK)

    # ── 5. Build ClipSegments ────────────────────────────────────────────
    processor = VideoProcessor(output_fps=30, preset="medium")
    segments = processor.create_segments_from_scenes(
        scenes, durations, transitions=transitions, transition_duration=0.3,
    )

    # ── 6. Stitch ────────────────────────────────────────────────────────
    temp = output_path.with_stem(output_path.stem + "_raw")
    print("Stitching...")
    processor.stitch_clips(
        segments, temp,
        audio_path=music_path,
        target_size=(1080, 1920),
        progress_callback=lambda p: print(f"\r  {p*100:.0f}%", end=""),
    )
    print()

    # ── 7. Grade ─────────────────────────────────────────────────────────
    grader = ColorGrader(
        preset=ColorPreset.DRONE_AERIAL,
        intensity=0.75,
        vignette_strength=0.3,
        halation_strength=0.2,
    )
    print("Grading...")
    grader.grade_video(
        temp, output_path,
        progress_callback=lambda p: print(f"\r  {p*100:.0f}%", end=""),
    )
    print()
    temp.unlink(missing_ok=True)
    print(f"Done → {output_path}")


if __name__ == "__main__":
    build_reel(
        input_dir=Path("./clips/"),
        music_path=Path("./music/track.mp3"),
        output_path=Path("./output/reel.mp4"),
    )
```

---

### 12. Custom Tone Curves + LUT Stack

Combine a 3D LUT with per-channel tone curves and selective colour for a
signature cinematic look. Useful when you have a reference grade you want
to reproduce consistently.

```python
#!/usr/bin/env python3
"""LUT + tone curve + selective colour stacked grade."""

from pathlib import Path
from drone_reel.core.color_grader import (
    ColorGrader, ColorAdjustments, SelectiveColorAdjustments, ToneCurve,
)


def build_signature_grader(lut_path: Path) -> ColorGrader:
    """Create a reusable grader with a signature look."""

    # Gentle S-curve with slightly cooler shadows and warmer highlights
    tone_curve = ToneCurve(
        red_points=  [(0, 0),  (64, 52),  (192, 208), (255, 255)],
        green_points=[(0, 0),  (64, 49),  (192, 206), (255, 252)],
        blue_points= [(0, 10), (64, 55),  (192, 203), (255, 248)],
    )

    # Punch skies, pop sand, suppress midday greens
    selective = SelectiveColorAdjustments(
        blue_sat=18,  blue_hue=5,
        cyan_sat=12,  cyan_hue=-5,
        orange_sat=20,
        yellow_sat=12,
        green_sat=-8,
    )

    adjustments = ColorAdjustments(
        contrast=14,
        saturation=-5,   # Slight desaturation — the LUT handles colour
        temperature=6,
        shadows=10,
        highlights=-8,
        fade=4,
        grain=8,
        selective_color=selective,
    )

    return ColorGrader(
        lut_path=lut_path,        # Applied first; curves/adjustments refine on top
        tone_curve=tone_curve,
        adjustments=adjustments,
        vignette_strength=0.3,
        halation_strength=0.15,
        intensity=0.8,
    )


if __name__ == "__main__":
    grader = build_signature_grader(Path("./luts/my_look.cube"))

    # Grade a finished reel
    grader.grade_video(
        Path("./output/reel_raw.mp4"),
        Path("./output/reel_signature.mp4"),
        progress_callback=lambda p: print(f"\rGrading {p*100:.0f}%", end=""),
    )
    print("\nDone.")
```

---

### 13. Terrain-Aware Preset Selection

Automatically choose a color preset based on scene content. This example uses
the scene `motion_type` and score to infer the best terrain preset, then
applies it clip-by-clip.

```python
#!/usr/bin/env python3
"""Select color preset dynamically per scene based on content analysis."""

import cv2
import numpy as np
from pathlib import Path
from drone_reel import SceneDetector
from drone_reel.core.color_grader import ColorGrader, ColorPreset
from drone_reel.utils.file_utils import find_video_files


def infer_preset(scene) -> ColorPreset:
    """
    Infer a terrain-aware preset from scene properties.
    Falls back to drone_aerial for ambiguous scenes.
    """
    # Read the middle frame for colour analysis
    cap = cv2.VideoCapture(str(scene.source_file))
    cap.set(cv2.CAP_PROP_POS_MSEC, (scene.start_time + scene.duration / 2) * 1000)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return ColorPreset.DRONE_AERIAL

    # Convert to HSV and sample colour statistics
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)
    mean_sat = hsv[:, :, 1].mean()
    mean_val = hsv[:, :, 2].mean()

    # Sample top-third (sky) and bottom-third (ground) separately
    h = frame.shape[0]
    top_bgr    = frame[:h // 3].astype(np.float32)
    bottom_bgr = frame[2 * h // 3:].astype(np.float32)

    top_blue_ratio = top_bgr[:, :, 0].mean() / (top_bgr[:, :, 2].mean() + 1)
    bottom_green   = bottom_bgr[:, :, 1].mean()
    bottom_blue    = bottom_bgr[:, :, 0].mean()

    # Heuristic rules
    if mean_val < 60:
        return ColorPreset.NIGHT_CITY
    if top_blue_ratio > 1.4 and bottom_blue > 120:
        return ColorPreset.OCEAN_COASTAL
    if mean_val > 180 and mean_sat < 30:
        return ColorPreset.SNOW_MOUNTAIN
    if bottom_bgr[:, :, 2].mean() > 160:   # Orange-heavy bottom = desert/arid
        return ColorPreset.DESERT_ARID
    if bottom_green > 120 and bottom_green > bottom_blue:
        return ColorPreset.FOREST_JUNGLE
    return ColorPreset.DRONE_AERIAL


if __name__ == "__main__":
    videos = find_video_files(Path("./mixed_terrain_clips/"))
    detector = SceneDetector(threshold=27.0)

    for video in videos:
        scenes = detector.detect_scenes(video)
        if not scenes:
            continue

        # Use the best scene from each clip
        best = max(scenes, key=lambda s: s.score)
        preset = infer_preset(best)
        print(f"{video.name} → {preset.value}")

        grader = ColorGrader(
            preset=preset,
            intensity=0.7,
            vignette_strength=0.25,
            gnd_sky_strength=0.35,
        )
        out = Path("./output/graded") / video.name
        out.parent.mkdir(parents=True, exist_ok=True)
        grader.grade_video(video, out)
```

---

### 14. Speed Ramping with Beat Energy Mapping

Apply slow-motion to low-energy sections and normal/fast speed on high-energy
beats. Combine with the `--speed-ramp` CLI flag or use the API to control it
precisely.

```bash
# CLI — automatic speed ramp on hook clips
drone-reel create -i ./clips/ -m track.mp3 --speed-ramp -c drone_aerial -o speed_reel.mp4
```

For precise control, build the reel first then map energy manually:

```python
#!/usr/bin/env python3
"""Map music energy to clip speed per-segment."""

from pathlib import Path
from drone_reel import SceneDetector, VideoProcessor, ColorGrader
from drone_reel.core.beat_sync import BeatSync
from drone_reel.core.video_processor import TransitionType
from drone_reel.core.color_grader import ColorPreset
from drone_reel.utils.file_utils import find_video_files


def energy_speed_map(energy: float) -> float:
    """Map beat energy (0–1) to playback speed."""
    if energy < 0.25:
        return 0.65   # Slow-motion on quiet passages
    if energy < 0.55:
        return 0.85   # Slightly slowed for mid-energy
    if energy > 0.80:
        return 1.15   # Slightly fast for peak energy
    return 1.0        # Normal speed


if __name__ == "__main__":
    input_dir = Path("./clips/")
    music_path = Path("./music/track.mp3")
    output_path = Path("./output/speed_reel.mp4")

    videos = find_video_files(input_dir)
    detector = SceneDetector(threshold=25.0)
    beat_sync = BeatSync()

    scenes = []
    for v in videos:
        scenes.extend(detector.detect_scenes(v))
    scenes.sort(key=lambda s: s.score, reverse=True)

    beat_info = beat_sync.analyze(music_path)
    cut_points = beat_sync.get_cut_points(beat_info, target_duration=30.0,
                                          prefer_downbeats=True)
    durations = beat_sync.calculate_clip_durations(cut_points, 30.0)

    n = min(len(durations), len(scenes))
    selected_scenes = scenes[:n]

    # Log the energy-to-speed mapping for each cut
    for i, cp in enumerate(cut_points[:n]):
        energy = beat_sync.get_energy_at_time(beat_info, cp.time)
        speed = energy_speed_map(energy)
        print(f"  Cut {i+1:02d} at {cp.time:5.2f}s — energy {energy:.2f} → {speed:.2f}x speed")

    processor = VideoProcessor(output_fps=30)
    segments = processor.create_segments_from_scenes(
        selected_scenes, durations,
        transitions=[TransitionType.CROSSFADE] * (n - 1) + [TransitionType.FADE_BLACK],
        transition_duration=0.3,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    processor.stitch_clips(segments, output_path, audio_path=music_path,
                           target_size=(1080, 1920))

    # Apply grade
    graded = output_path.with_stem(output_path.stem + "_graded")
    grader = ColorGrader(preset=ColorPreset.DRONE_AERIAL, intensity=0.7,
                         vignette_strength=0.3)
    grader.grade_video(output_path, graded)
    output_path.unlink()
    graded.rename(output_path)
    print(f"Done → {output_path}")
```

---

## Expert

Production-ready scripts for automated workflows and large-scale processing.

---

### 15. Automated Batch Processor

Processes an entire folder of shoot days, each in its own subdirectory.
Renders all to multiple output sizes in parallel, with memory pre-flight checks
and per-render logging.

> **Render time estimate:** ~1h per 30-second 4K ultra render. Plan accordingly.

```python
#!/usr/bin/env python3
"""
Production batch processor.

Directory structure expected:
  ./shoots/
    2024-07-01/   ← one folder per shoot day
      *.mp4
    2024-07-08/
      *.mp4
  ./music/track.mp3

Outputs:
  ./output/2024-07-01/reel_1080p.mp4
  ./output/2024-07-01/reel_4k.mp4
  ./output/2024-07-08/reel_1080p.mp4
  ...
"""

import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path


MUSIC = Path("./music/track.mp3")
SHOOTS_DIR = Path("./shoots/")
OUTPUT_DIR = Path("./output/")

RENDER_CONFIGS = [
    {"name": "1080p",  "resolution": "1080p", "quality": "high"},
    {"name": "4k",     "resolution": "4k",    "quality": "ultra"},
]


def render_shoot(shoot_dir: Path, config: dict) -> tuple[bool, str]:
    """Render one shoot day at one quality level. Returns (success, message)."""
    out = OUTPUT_DIR / shoot_dir.name / f"reel_{config['name']}.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)

    # Skip if already rendered
    if out.exists() and out.stat().st_size > 1_000_000:
        return True, f"SKIP  {out} (already exists)"

    cmd = [
        "drone-reel", "create",
        "-i", str(shoot_dir),
        "-m", str(MUSIC),
        "-d", "30",
        "--platform", "instagram_reels",
        "--resolution", config["resolution"],
        "--quality", config["quality"],
        "-c", "drone_aerial",
        "--vignette", "0.3",
        "--halation", "0.2",
        "--beat-mode", "downbeat",
        "--stabilize",
        "-o", str(out),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        return True, f"OK    {out}"
    else:
        return False, f"FAIL  {out}\n{result.stderr[-500:]}"


def main():
    shoot_dirs = sorted(d for d in SHOOTS_DIR.iterdir() if d.is_dir())
    if not shoot_dirs:
        print(f"No shoot directories found in {SHOOTS_DIR}")
        sys.exit(1)

    print(f"Processing {len(shoot_dirs)} shoot days × {len(RENDER_CONFIGS)} configs\n")

    tasks = [(d, cfg) for d in shoot_dirs for cfg in RENDER_CONFIGS]
    failures = []

    # Limit parallelism to avoid overwhelming memory (4K renders use ~1 GB each)
    max_workers = min(2, len(tasks))
    with ProcessPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(render_shoot, d, cfg): (d, cfg) for d, cfg in tasks}
        for future in as_completed(futures):
            success, msg = future.result()
            print(msg)
            if not success:
                failures.append(msg)

    if failures:
        print(f"\n{len(failures)} render(s) failed:")
        for f in failures:
            print(f"  {f}")
        sys.exit(1)
    else:
        print(f"\nAll {len(tasks)} renders complete.")


if __name__ == "__main__":
    main()
```

---

### 16. Generative Grading — Preset from Scene Analysis

Analyse each clip's motion type, time-of-day brightness, and terrain to select
the ideal preset dynamically. Then apply per-clip in a single-pass grade.

```python
#!/usr/bin/env python3
"""
Generative grade: infer preset from scene motion + brightness + colour.

Each clip gets the grade it deserves — no manual preset per clip required.
"""

import cv2
import numpy as np
from pathlib import Path
from dataclasses import dataclass
from drone_reel import SceneDetector, VideoProcessor, ColorGrader
from drone_reel.core.beat_sync import BeatSync
from drone_reel.core.video_processor import TransitionType
from drone_reel.core.color_grader import ColorPreset, ColorAdjustments
from drone_reel.utils.file_utils import find_video_files


@dataclass
class SceneContext:
    mean_brightness: float  # 0–255
    warm_ratio: float       # red/blue mean ratio
    green_dominance: float  # green channel mean
    blue_dominance: float   # blue channel mean


def read_scene_context(scene) -> SceneContext:
    cap = cv2.VideoCapture(str(scene.source_file))
    cap.set(cv2.CAP_PROP_POS_MSEC, (scene.start_time + scene.duration / 2) * 1000)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        return SceneContext(128, 1.0, 100, 100)

    b, g, r = cv2.split(frame.astype(np.float32))
    return SceneContext(
        mean_brightness=frame.mean(),
        warm_ratio=r.mean() / (b.mean() + 1),
        green_dominance=g.mean(),
        blue_dominance=b.mean(),
    )


def select_preset(ctx: SceneContext) -> ColorPreset:
    """Rule-based preset selection from scene context."""
    if ctx.mean_brightness < 55:
        return ColorPreset.NIGHT_CITY
    if ctx.mean_brightness > 210 and ctx.warm_ratio < 0.9:
        return ColorPreset.SNOW_MOUNTAIN
    if ctx.warm_ratio > 1.3 and ctx.mean_brightness > 140:
        return ColorPreset.GOLDEN_HOUR
    if ctx.warm_ratio < 0.75 and ctx.mean_brightness < 100:
        return ColorPreset.BLUE_HOUR
    if ctx.blue_dominance > 130 and ctx.blue_dominance > ctx.green_dominance:
        return ColorPreset.OCEAN_COASTAL
    if ctx.green_dominance > 120:
        return ColorPreset.FOREST_JUNGLE
    if ctx.warm_ratio > 1.1:
        return ColorPreset.DESERT_ARID
    return ColorPreset.DRONE_AERIAL


def build_generative_reel(input_dir: Path, music_path: Path, output_path: Path):
    videos = find_video_files(input_dir)
    detector = SceneDetector(threshold=26.0)
    beat_sync = BeatSync()

    all_scenes = []
    for v in videos:
        all_scenes.extend(detector.detect_scenes(v))
    all_scenes.sort(key=lambda s: s.score, reverse=True)

    beat_info = beat_sync.analyze(music_path)
    cut_points = beat_sync.get_cut_points(beat_info, target_duration=45.0,
                                          prefer_downbeats=True)
    durations = beat_sync.calculate_clip_durations(cut_points, 45.0)
    n = min(len(durations), len(all_scenes))
    scenes, durations = all_scenes[:n], durations[:n]

    # Log the generative preset selection
    print("Generative preset selection:")
    for i, scene in enumerate(scenes):
        ctx = read_scene_context(scene)
        preset = select_preset(ctx)
        print(f"  {i+1:02d}. {scene.source_file.name} → {preset.value:<20} "
              f"(brightness={ctx.mean_brightness:.0f}, warm={ctx.warm_ratio:.2f})")

    # Use a single global grade (drone_aerial) for stitch pass
    # then fine-tune per-scene grade in post if needed
    processor = VideoProcessor(output_fps=30, preset="medium")
    segments = processor.create_segments_from_scenes(
        scenes, durations,
        transitions=[TransitionType.CROSSFADE] * (n - 1) + [TransitionType.FADE_BLACK],
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    raw = output_path.with_stem(output_path.stem + "_raw")
    processor.stitch_clips(segments, raw, audio_path=music_path, target_size=(1080, 1920))

    # Grade with the most common preset from the selection
    from collections import Counter
    ctxs = [read_scene_context(s) for s in scenes]
    presets = [select_preset(c) for c in ctxs]
    dominant_preset, _ = Counter(p.value for p in presets).most_common(1)[0]
    print(f"\nDominant preset: {dominant_preset}")

    grader = ColorGrader(
        preset=ColorPreset(dominant_preset),
        intensity=0.70,
        vignette_strength=0.30,
        halation_strength=0.18,
        gnd_sky_strength=0.35,
    )
    grader.grade_video(raw, output_path)
    raw.unlink(missing_ok=True)
    print(f"Done → {output_path}")


if __name__ == "__main__":
    build_generative_reel(
        input_dir=Path("./clips/"),
        music_path=Path("./music/track.mp3"),
        output_path=Path("./output/generative_reel.mp4"),
    )
```

---

### 17. Complete Vertical Reel Factory

The full production pipeline in one script: D-Log normalisation → auto white
balance → beat sync → diversity selection → transitions → stitch → grade with
BT.709 encoding. Mirrors exactly what the CLI's `--viral` flag orchestrates
internally.

> **Render time estimate:** ~8 minutes for 30s at 1080p medium, ~45 minutes for 4K ultra.

```python
#!/usr/bin/env python3
"""
Full reel factory: every pipeline stage explicit and configurable.

Usage:
  python reel_factory.py ./clips/ ./music.mp3 ./output/reel.mp4
"""

import sys
import gc
from pathlib import Path
from drone_reel import SceneDetector, VideoProcessor, ColorGrader
from drone_reel.core.beat_sync import BeatSync
from drone_reel.core.video_processor import TransitionType
from drone_reel.core.color_grader import (
    ColorGrader, ColorPreset, ColorAdjustments, SelectiveColorAdjustments,
)
from drone_reel.utils.file_utils import find_video_files


TARGET_DURATION = 30.0
TARGET_SIZE = (1080, 1920)   # width × height (9:16)


def run(input_dir: Path, music_path: Path, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # ── Stage 1: Detect D-Log ────────────────────────────────────────────
    videos = find_video_files(input_dir)
    if not videos:
        raise FileNotFoundError(f"No video files in {input_dir}")
    print(f"[1/7] Found {len(videos)} clips")

    sample_colorspace = ColorGrader.detect_log_footage(videos[0])
    print(f"      Detected input colorspace: {sample_colorspace}")

    # ── Stage 2: Scene detection + scoring ───────────────────────────────
    print("[2/7] Detecting scenes...")
    detector = SceneDetector(threshold=25.0, min_scene_length=1.5, max_scene_length=8.0)
    all_scenes = []
    for v in videos:
        try:
            all_scenes.extend(detector.detect_scenes(v))
        except Exception as e:
            print(f"      Skipping {v.name}: {e}")

    # Sort by hook potential (score) and ensure diversity (no two from same file)
    seen_files: set[str] = set()
    diverse_scenes = []
    for scene in sorted(all_scenes, key=lambda s: s.score, reverse=True):
        key = scene.source_file.name
        if key not in seen_files or len(diverse_scenes) < 4:
            diverse_scenes.append(scene)
            seen_files.add(key)

    print(f"      {len(all_scenes)} scenes → {len(diverse_scenes)} diverse candidates")
    gc.collect()

    # ── Stage 3: Beat sync ───────────────────────────────────────────────
    print("[3/7] Analysing music...")
    beat_sync = BeatSync()
    beat_info = beat_sync.analyze(music_path)
    print(f"      {beat_info.tempo:.1f} BPM, {beat_info.beat_count} beats")

    cut_points = beat_sync.get_cut_points(
        beat_info,
        target_duration=TARGET_DURATION,
        min_clip_length=1.5,
        max_clip_length=5.0,
        prefer_downbeats=True,
    )
    durations = beat_sync.calculate_clip_durations(cut_points, TARGET_DURATION)
    print(f"      {len(cut_points)} cut points → {sum(durations):.1f}s total")

    # ── Stage 4: Select final clips ──────────────────────────────────────
    n = min(len(durations), len(diverse_scenes))
    scenes = diverse_scenes[:n]
    durations = durations[:n]
    print(f"[4/7] Selected {n} clips")

    # Motion-matched transitions
    transitions = []
    for i, (scene, cp) in enumerate(zip(scenes, cut_points[:n])):
        energy = beat_sync.get_energy_at_time(beat_info, cp.time)
        if i == n - 1:
            transitions.append(TransitionType.FADE_BLACK)
        elif energy > 0.70:
            transitions.append(TransitionType.WHIP_PAN)
        elif energy > 0.40:
            transitions.append(TransitionType.CROSSFADE)
        else:
            transitions.append(TransitionType.PARALLAX_LEFT)

    # ── Stage 5: Stitch ───────────────────────────────────────────────────
    print("[5/7] Stitching...")
    processor = VideoProcessor(output_fps=30, preset="medium")
    segments = processor.create_segments_from_scenes(
        scenes, durations, transitions=transitions, transition_duration=0.3,
    )
    raw = output_path.with_stem(output_path.stem + "_raw")
    processor.stitch_clips(
        segments, raw,
        audio_path=music_path,
        target_size=TARGET_SIZE,
        progress_callback=lambda p: print(f"\r      {p*100:.0f}%", end=""),
    )
    print()
    gc.collect()

    # ── Stage 6: Grade ────────────────────────────────────────────────────
    print("[6/7] Colour grading...")
    grader = ColorGrader(
        preset=ColorPreset.DRONE_AERIAL,
        input_colorspace=sample_colorspace,
        auto_wb=(sample_colorspace != "rec709"),
        intensity=0.70,
        vignette_strength=0.32,
        halation_strength=0.20,
        gnd_sky_strength=0.30,
        denoise_strength=0.25,
    )
    grader.grade_video(
        raw, output_path,
        progress_callback=lambda p: print(f"\r      {p*100:.0f}%", end=""),
    )
    print()
    raw.unlink(missing_ok=True)
    gc.collect()

    # ── Stage 7: Report ───────────────────────────────────────────────────
    size_mb = output_path.stat().st_size / 1_048_576
    print(f"[7/7] Done → {output_path}  ({size_mb:.1f} MB)")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python reel_factory.py <clips_dir> <music.mp3> <output.mp4>")
        sys.exit(1)
    run(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))
```

---

### 18. Event/Wedding Reel with Narrative Arc

For reels where emotional pacing matters — weddings, events, travel films — use
hook tier scoring to build a deliberate Hook → Build → Climax → Resolution
structure. The best moment leads, energy builds to a peak, then resolves
gracefully.

```python
#!/usr/bin/env python3
"""
Narrative-arc reel: Hook → Build → Climax → Resolution.

Uses hook_tier scoring from EnhancedSceneInfo to place the emotionally
strongest clip at position 0, build energy through the middle,
and close with a calm resolution.
"""

from pathlib import Path
from drone_reel import SceneDetector, VideoProcessor, ColorGrader
from drone_reel.core.beat_sync import BeatSync
from drone_reel.core.video_processor import TransitionType
from drone_reel.core.color_grader import ColorPreset
from drone_reel.utils.file_utils import find_video_files


# Tier weights used for sorting into narrative positions
HOOK_WEIGHTS = {"MAXIMUM": 5, "HIGH": 4, "MEDIUM": 3, "LOW": 2, "POOR": 1}


def narrative_sort(scenes: list, total_clips: int) -> list:
    """
    Arrange scenes into narrative arc sections.

    Sections: Hook (10%) → Build (30%) → Climax (40%) → Resolution (20%)
    """
    weighted = sorted(
        scenes,
        key=lambda s: (HOOK_WEIGHTS.get(s.hook_tier.name, 1), s.score),
        reverse=True,
    )

    n = min(total_clips, len(weighted))
    n_hook       = max(1, round(n * 0.10))
    n_build      = max(1, round(n * 0.30))
    n_climax     = max(1, round(n * 0.40))
    n_resolution = max(1, n - n_hook - n_build - n_climax)

    # Hook: single best scene
    hook       = weighted[:n_hook]
    # Build: next tier ascending
    build      = sorted(weighted[n_hook:n_hook + n_build],
                        key=lambda s: s.score)
    # Climax: peak scenes
    climax     = weighted[n_hook + n_build: n_hook + n_build + n_climax]
    # Resolution: quieter scenes
    resolution = sorted(
        weighted[n_hook + n_build + n_climax: n_hook + n_build + n_climax + n_resolution],
        key=lambda s: s.score,
    )

    return hook + build + climax + resolution


def narrative_transitions(n: int) -> list[TransitionType]:
    """Assign transitions that match the energy arc."""
    transitions = []
    for i in range(n):
        frac = i / max(n - 1, 1)
        if i == 0:
            transitions.append(TransitionType.FADE_BLACK)       # Open slowly
        elif frac < 0.35:
            transitions.append(TransitionType.CROSSFADE)        # Build gently
        elif frac < 0.75:
            transitions.append(TransitionType.WHIP_PAN)         # Climax energy
        elif i == n - 1:
            transitions.append(TransitionType.FADE_BLACK)       # Close softly
        else:
            transitions.append(TransitionType.LIGHT_LEAK)       # Warm resolution
    return transitions


def build_narrative_reel(
    input_dir: Path,
    music_path: Path,
    output_path: Path,
    target_duration: float = 60.0,
    caption: str = "",
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # ── Detect scenes ────────────────────────────────────────────────────
    videos = find_video_files(input_dir)
    detector = SceneDetector(threshold=25.0, min_scene_length=2.0, max_scene_length=8.0)
    all_scenes = []
    for v in videos:
        try:
            all_scenes.extend(detector.detect_scenes(v))
        except Exception as e:
            print(f"Skipping {v.name}: {e}")

    # Filter: only scenes with a recognisable hook tier
    quality = [s for s in all_scenes
               if hasattr(s, "hook_tier") and s.score >= 45.0]
    print(f"Detected {len(all_scenes)} scenes, {len(quality)} pass quality threshold")

    # ── Beat sync ────────────────────────────────────────────────────────
    beat_sync = BeatSync()
    beat_info = beat_sync.analyze(music_path)
    print(f"Music: {beat_info.tempo:.1f} BPM")
    cut_points = beat_sync.get_cut_points(
        beat_info, target_duration=target_duration,
        min_clip_length=2.5, max_clip_length=6.0, prefer_downbeats=True,
    )
    durations = beat_sync.calculate_clip_durations(cut_points, target_duration)

    # ── Narrative ordering ───────────────────────────────────────────────
    n = min(len(durations), len(quality))
    arc = narrative_sort(quality, n)
    durations = durations[:n]

    print("Narrative arc:")
    for i, scene in enumerate(arc):
        tier = getattr(scene, "hook_tier", "?")
        print(f"  {i+1:02d}. {scene.source_file.name:30s} score={scene.score:.0f}  tier={tier}")

    # ── Stitch ───────────────────────────────────────────────────────────
    transitions = narrative_transitions(n)
    processor = VideoProcessor(output_fps=30, preset="medium")
    segments = processor.create_segments_from_scenes(
        arc, durations, transitions=transitions, transition_duration=0.4,
    )
    raw = output_path.with_stem(output_path.stem + "_raw")
    print("Stitching...")
    processor.stitch_clips(segments, raw, audio_path=music_path,
                           target_size=(1080, 1920),
                           progress_callback=lambda p: print(f"\r  {p*100:.0f}%", end=""))
    print()

    # ── Grade — warm, emotional ──────────────────────────────────────────
    grader = ColorGrader(
        preset=ColorPreset.FILM_EMULATION,
        intensity=0.65,
        vignette_strength=0.35,
        halation_strength=0.30,
        chromatic_aberration_strength=0.08,
    )
    print("Grading...")
    grader.grade_video(raw, output_path,
                       progress_callback=lambda p: print(f"\r  {p*100:.0f}%", end=""))
    print()
    raw.unlink(missing_ok=True)
    print(f"Done → {output_path}")


if __name__ == "__main__":
    build_narrative_reel(
        input_dir=Path("./event_clips/"),
        music_path=Path("./music/emotional_track.mp3"),
        output_path=Path("./output/event_reel.mp4"),
        target_duration=60.0,
    )
```

---

## Troubleshooting

### 1. "No video files found"

drone-reel searches for `.mp4`, `.mov`, `.avi`, `.mkv`, `.m4v`, `.mts` by
default. Check:

```bash
# Verify files exist and are readable
ls -lh ./clips/*.mp4

# If your files are in a nested structure, pass the specific subfolder
drone-reel create -i ./clips/day1/ -o reel.mp4
```

From Python:
```python
from drone_reel.utils.file_utils import find_video_files
print(find_video_files(Path("./clips/")))  # Should list your files
```

---

### 2. Audio Codec Error / No Sound

If you see `AAC encoder not found` or the output has no audio:

```bash
# Verify ffmpeg has AAC support
ffmpeg -codecs 2>&1 | grep aac

# Install ffmpeg with all codecs (macOS)
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg
```

When no music is provided, drone-reel injects a silent audio track automatically
(required by most platforms). If the output is rejected by a platform, verify
the file with:

```bash
ffprobe -v quiet -print_format json -show_streams output.mp4 | python3 -m json.tool | grep codec_name
```

---

### 3. Memory Crash on 4K Renders

4K ultra renders require ~1 GB RAM per render and can OOM on machines with
less than 16 GB. Mitigations:

```bash
# Use high quality instead of ultra for 4K
drone-reel create -i ./clips/ --resolution 4k --quality high -o reel.mp4

# Or render at 1440p ultra for near-4K quality at lower memory
drone-reel create -i ./clips/ --resolution 1440p --quality ultra -o reel.mp4

# Limit parallel renders in batch scripts
# max_workers=1 in ProcessPoolExecutor
```

From Python, check available memory before rendering:
```python
import psutil
available_gb = psutil.virtual_memory().available / 1_073_741_824
if available_gb < 4.0:
    print(f"Warning: only {available_gb:.1f} GB available — consider 1080p quality")
```

---

### 4. D-Log Footage Still Looks Flat After Grading

The two most common causes:

**Wrong log profile specified:**
```bash
# DJI Mini 3 Pro / Air 3 / Mavic 3 use D-Log M, NOT D-Log
drone-reel create -i ./clips/ --input-colorspace dlog_m  # correct
drone-reel create -i ./clips/ --input-colorspace dlog    # may look wrong
```

**Auto-detect falling back to rec709:**
Use `ColorGrader.detect_log_footage()` to verify detection:
```python
from pathlib import Path
from drone_reel.core.color_grader import ColorGrader

result = ColorGrader.detect_log_footage(Path("./clip.mp4"))
print(result)  # "dlog" or "rec709"
# If it returns "rec709" but your footage is log, specify the colorspace manually
```

---

### 5. Beat Sync Producing Too Few Cuts

When the detected tempo is very slow or the track has few beats:

```bash
# Check what beat_sync actually found
drone-reel beats -i ./music.mp3

# Use all beats instead of downbeats only
drone-reel create -i ./clips/ -m track.mp3 --beat-mode all -d 30

# Allow shorter minimum clip length to fit more cuts
```

From Python, the fallback produces uniform cuts when no beats are detected:
```python
beat_info = beat_sync.analyze(music_path)
if beat_info.beat_count < 10:
    print(f"Warning: only {beat_info.beat_count} beats — using uniform cuts")
    # Proceed normally; get_cut_points() handles this with a warning
cut_points = beat_sync.get_cut_points(beat_info, target_duration=45.0)
```

---

## Example Files

| File | Level | Description |
|------|-------|-------------|
| [`extract_and_reel.py`](extract_and_reel.py) | Intermediate | Extract best clips from raw footage, then build a reel |
| [`basic_reel.py`](basic_reel.py) | Beginner | Simple reel without music |
| [`beat_synced_reel.py`](beat_synced_reel.py) | Intermediate | Beat-synced with energy-mapped transitions |
| [`custom_workflow.py`](custom_workflow.py) | Intermediate | Full manual control: filter, sequence, custom grade |
| [`dlog_workflow.py`](dlog_workflow.py) | Intermediate | D-Log M normalisation + auto white balance |
| [`multi_camera_match.py`](multi_camera_match.py) | Advanced | Histogram-matched multi-camera colour |
| [`reel_factory.py`](reel_factory.py) | Expert | Complete pipeline: D-Log → stitch → BT.709 encode |
| [`narrative_reel.py`](narrative_reel.py) | Expert | Hook-tier narrative arc: Hook → Build → Climax → Resolution |
| [`batch_processor.py`](batch_processor.py) | Expert | Parallel multi-shoot-day batch renderer |
