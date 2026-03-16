# drone-reel CLI Parameter Demo Guide

Each video was created from the same 9 pre-extracted source clips (Snowdonia/Wales, Germia Pool/Kosovo, Summit Camp/Greenland) to isolate the effect of each parameter. All are 1080×1920 vertical reels suitable for Instagram/TikTok.

## Demo Videos

| Filename | Key flags | Size | What it demonstrates |
|----------|-----------|------|----------------------|
| `demo_baseline.mp4` | *(none)* | 24 MB | Default output — no colour grade, no effects. Baseline for comparison. |
| `demo_drone_aerial.mp4` | `--color drone_aerial --color-intensity 0.6` | 24 MB | Drone-optimised colour: boosted contrast (14), saturation (10), cooler tone. Most popular preset for aerial footage. |
| `demo_golden_hour.mp4` | `--color golden_hour --color-intensity 0.7` | 19 MB | Warm amber tones, lifted shadows, high contrast — mimics late-afternoon sunlight. |
| `demo_film_emulation.mp4` | `--color film_emulation --color-intensity 0.5` | 19 MB | Cinematic film look: slight desaturation, warm highlights, lifted blacks. |
| `demo_vignette.mp4` | `--vignette 0.6 --color drone_aerial` | 19 MB | Sigmoid-falloff dark border draws focus to the centre of frame. |
| `demo_letterbox.mp4` | `--letterbox 2.35 --color drone_aerial` | 13 MB | Black bars create a 2.35:1 cinematic aspect ratio within the vertical frame. |
| `demo_stabilized.mp4` | `--stabilize-all --color drone_aerial` | 19 MB | Optical-flow stabilization applied to every clip — smooths camera shake. |
| `demo_viral.mp4` | `--viral --color drone_aerial` | 20 MB | Viral preset: auto 15s, Instagram Reels platform, 60% colour, speed ramp enabled. |
| `demo_long_30s.mp4` | `--duration 30 --color drone_aerial` | 30 MB | 30-second reel using 10 clips instead of 5 — shows duration scaling. |
| `demo_caption.mp4` | `--caption "Drone Footage Demo" --color drone_aerial` | 19 MB | Lower-third text overlay with fade-in/out animation. |

## Quick Reference

| Parameter | Description | Example |
|-----------|-------------|---------|
| `--color` / `-c` | Apply a colour preset (11+ presets available — run `drone-reel presets`) | `--color drone_aerial` |
| `--color-intensity` | Scale preset strength 0.0–1.0 (0 = off, 1 = full) | `--color-intensity 0.6` |
| `--vignette` | Add dark border falloff 0.0–1.0 | `--vignette 0.5` |
| `--letterbox` | Cinematic black bars at aspect ratio `2.35`, `1.85`, or `2.39` | `--letterbox 2.35` |
| `--stabilize-all` | Force optical-flow stabilization on every clip (default: auto-detect) | `--stabilize-all` |
| `--viral` | One-flag shortcut: 15s duration, Instagram Reels, 60% colour, speed ramp | `--viral` |
| `--duration` | Target reel length in seconds | `--duration 30` |
| `--caption` | Lower-third text overlay with fade animation | `--caption "My Reel"` |
| `--beat-mode` | `downbeat` (major beats only) or `all` (every beat) | `--beat-mode downbeat` |
| `--halation` | Soft highlight bloom 0.0–1.0 | `--halation 0.3` |
| `--chromatic-aberration` | RGB channel fringe 0.0–1.0 | `--chromatic-aberration 0.2` |
| `--lut` | Apply a `.cube` 3D LUT file | `--lut /path/to/look.cube` |

## Recommended Starting Points

- **Instagram/TikTok quick reel**: `--viral --color drone_aerial`
- **Cinematic aerial**: `--color drone_aerial --color-intensity 0.7 --vignette 0.4 --letterbox 2.35`
- **Golden sunset**: `--color golden_hour --color-intensity 0.8 --vignette 0.3`
- **Stabilized handheld**: `--stabilize-all --color film_emulation --color-intensity 0.5`

---

## `drone-reel split` — Single-File Highlight Extractor

Splits one video into scored highlight clips. Simpler than `create` — no sequencing, beat-sync, or reframing. Run `--preview` first to inspect detected scenes before committing to the encode.

### Key Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--min-duration` | 2.0s | Shortest clip to export |
| `--max-duration` | 15.0s | Longest clip; set to 300 for no cap |
| `--min-score` | 40.0 | Scene quality threshold (0 = export all) |
| `--no-filter` | off | Skip quality filtering entirely |
| `--scene-threshold` | 27.0 | Detection sensitivity — lower = more cuts |
| `--sort` | `score` | Order: `score`, `chronological`, `duration` |
| `--count` / `-n` | unlimited | Max clips to export |
| `--auto-speed` | off | Auto-correct pan/tilt speed: slows fast pans (0.65–0.80×), speeds up sluggish ones (1.25×) |
| `--enhanced` | off | Enhanced detection with subject tracking (slower) |
| `--preview` | off | Dry-run: print scene table without encoding |
| `--json` | off | Write `manifest.json` with per-clip metadata |

All `create` visual flags work here too: `--color`, `--color-intensity`, `--vignette`, `--halation`, `--chromatic-aberration`, `--lut`, `--input-colorspace`, `--auto-wb`, `--denoise`, `--haze`, `--gnd-sky`, `--stabilize`, `--stabilize-all`, `--letterbox`.

### Example Runs

```bash
# Preview — no encoding, just prints the scene table
drone-reel split -i clip.mp4 -o ./out --preview --scene-threshold 5 --no-filter --min-score 0

# Best 5–15s highlights with cinematic grading
drone-reel split -i clip.mp4 -o ./out \
  --min-duration 5 --max-duration 15 --min-score 0 --no-filter \
  --color drone_aerial --color-intensity 0.65 --vignette 0.3 \
  --auto-speed --letterbox 2.35 --quality high --json

# Long highlights (11s+, no upper limit)
# Use --scene-threshold 7-12 to merge micro-cuts into longer coherent scenes
drone-reel split -i clip.mp4 -o ./out \
  --min-duration 11 --max-duration 300 --min-score 0 --no-filter \
  --scene-threshold 7 \
  --color drone_aerial --color-intensity 0.65 --vignette 0.3 \
  --auto-speed --letterbox 2.35 --quality high --json

# DJI D-Log 4K: create 720p proxy first for practical runtimes
ffmpeg -i DJI_SOURCE.MP4 -vf scale=1280:720 -r 30 -c:v libx264 -preset ultrafast -crf 26 -an proxy.mp4
drone-reel split -i proxy.mp4 -o ./out \
  --min-duration 5 --max-duration 15 --input-colorspace dlog \
  --color drone_aerial --auto-speed --letterbox 2.35 --json
```

### `--auto-speed` Pan Speed Correction

| Motion | Energy | Speed | Effect |
|--------|--------|-------|--------|
| PAN_LEFT / PAN_RIGHT | > 70 | **0.65×** | Uncomfortably fast → cinematic |
| PAN_LEFT / PAN_RIGHT | 55–70 | **0.80×** | Fast → smooth |
| PAN_LEFT / PAN_RIGHT | 5–20 | **1.25×** | Sluggish → engaging |
| TILT_UP / TILT_DOWN | > 65 | **0.70×** | Fast tilt → graceful |
| FLYOVER / APPROACH | > 70 | **0.70×** | Blurry speed → controlled |
| FPV | > 50 | **0.75×** | Intense FPV → watchable |
| STATIC / ORBIT / REVEAL | any | — | No change |

### Output Naming

`split_NNN_sSCORE.mp4` — e.g. `split_001_s70.mp4` = clip #1, scene score 70.
