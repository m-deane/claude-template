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
