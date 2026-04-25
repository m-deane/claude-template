# drone-reel

AI-powered CLI tool to create Instagram-style vertical reels from drone footage.

## Features

- **Automatic scene detection** with quality scoring (sharpness, color, motion, hook potential) — tunable weights and tier thresholds
- **Beat-synced editing** with librosa-powered music analysis
- **Intelligent reframing** from landscape to vertical (9:16, 1:1, 4:5)
- **Video stabilization** with adaptive shake detection
- **Auto pan/speed correction** — slows fast pans, speeds up sluggish movement, gimbal-bounce recovery, roll-drift correction
- **Color grading** with 30 presets including drone-optimized, film emulation, and terrain-aware grades
- **Visual effects** — vignette, halation/bloom, chromatic aberration, atmospheric haze, letterbox
- **Color science** — D-Log/S-Log3 normalization, auto white balance, auto color match, noise reduction
- **23 transition types** including parallax, diamond wipe, fog pass, vortex zoom
- **Speed ramping** with slow-motion at scenic moments
- **Text overlays** with animated lower thirds
- **Highlight extraction** — split one long video into graded, motion-corrected clips
- **Platform export presets** for Instagram, TikTok, YouTube Shorts

## Quick Start

```bash
pip install -e ".[dev]"

# Basic reel from a clips folder
drone-reel create -i ./clips/ -o reel.mp4 -d 30

# Viral preset (15s, Instagram Reels, speed ramp, 60% color)
drone-reel create -i ./clips/ --viral -c drone_aerial

# Beat-synced with cinematic look
drone-reel create -i ./clips/ -m track.mp3 --beat-mode downbeat \
  --color drone_aerial --color-intensity 0.7 --vignette 0.4 --letterbox 2.35

# Split a single video into 5–15s graded highlights
drone-reel split -i footage.mp4 -o ./highlights \
  --min-duration 5 --max-duration 15 --no-filter \
  --color drone_aerial --auto-speed --letterbox 2.35 --json

# Extract best clips, then build a reel
drone-reel extract-clips -i raw_footage.mp4 -o ./clips -n 15
drone-reel create -i ./clips/ -m music.mp3 -o reel.mp4
```

## Documentation

- **[Quick Start Reference](QUICKSTART.md)** — All parameters, defaults, and recipes on one page
- [CLI Reference](cli-reference.md) — Full command documentation
- [Python API Reference](api-reference.md) — Using drone-reel as a library
- [Color Presets](presets/color-presets.md) — 30 available color grades
- [Transitions](presets/transitions.md) — 23 transition types and effects
- [Advanced Color Grader](color_grader_advanced_features.md) — LUTs, tone curves, selective color, visual effects
- [Examples](examples/README.md) — Code examples and workflows

## Requirements

- Python 3.10+
- FFmpeg (for video encoding)
- Dependencies: MoviePy, OpenCV, librosa, PySceneDetect, Click, Rich
