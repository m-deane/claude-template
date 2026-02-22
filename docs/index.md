# drone-reel

AI-powered CLI tool to create Instagram-style vertical reels from drone footage.

## Features

- **Automatic scene detection** with quality scoring (sharpness, color, motion, hook potential)
- **Beat-synced editing** with librosa-powered music analysis
- **Intelligent reframing** from landscape to vertical (9:16, 1:1, 4:5)
- **Video stabilization** with adaptive shake detection
- **Color grading** with 30 presets including drone-optimized, film emulation, and terrain-aware grades
- **Visual effects** - vignette, halation/bloom, chromatic aberration, atmospheric haze, letterbox
- **Color science** - D-Log/S-Log3 normalization, auto white balance, auto color match, noise reduction
- **23 transition types** including parallax, diamond wipe, fog pass, vortex zoom
- **Speed ramping** with slow-motion at scenic moments
- **Text overlays** with animated lower thirds
- **Audio ducking** with automatic intro/outro volume fades
- **Platform export presets** for Instagram, TikTok, YouTube Shorts

## Quick Start

```bash
pip install -e ".[dev]"

# Basic reel from a clips folder
drone-reel create --input ./clips/ --output reel.mp4 --duration 30

# Viral preset (15s, Instagram Reels, speed ramp, 60% color)
drone-reel create --input ./clips/ --viral -c drone_aerial

# With music and beat sync
drone-reel create --input ./clips/ -m track.mp3 --beat-mode downbeat

# 4K with full stabilization and film look
drone-reel create --input ./clips/ --resolution 4k --quality ultra --stabilize-all --color kodak_2383

# D-Log footage with auto white balance and aerial haze
drone-reel create --input ./clips/ --input-colorspace dlog_m --auto-wb --haze 0.3 --color drone_aerial
```

## Documentation

- [CLI Reference](cli-reference.md) - All commands and options
- [Python API Reference](api-reference.md) - Using drone-reel as a library
- [Color Presets](presets/color-presets.md) - 30 available color grades
- [Transitions](presets/transitions.md) - 23 transition types and effects
- [Advanced Color Grader](color_grader_advanced_features.md) - LUTs, tone curves, selective color, visual effects
- [Examples](examples/README.md) - Code examples and workflows

## Requirements

- Python 3.10+
- FFmpeg (for video encoding)
- Dependencies: MoviePy, OpenCV, librosa, PySceneDetect, Click, Rich
