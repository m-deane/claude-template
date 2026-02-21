# drone-reel

AI-powered CLI tool to create Instagram-style vertical reels from drone footage.

## Features

- **Automatic scene detection** with quality scoring (sharpness, color, motion, hook potential)
- **Beat-synced editing** with librosa-powered music analysis
- **Intelligent reframing** from landscape to vertical (9:16, 1:1, 4:5)
- **Video stabilization** with adaptive shake detection
- **Color grading** with 11 presets including drone-optimized aerial grade
- **Speed ramping** with slow-motion at scenic moments
- **Text overlays** with animated lower thirds
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

# 4K with full stabilization
drone-reel create --input ./clips/ --resolution 4k --quality ultra --stabilize-all
```

## Documentation

- [CLI Reference](cli-reference.md) - All commands and options
- [Python API Reference](api-reference.md) - Using drone-reel as a library
- [Generated API Docs](api/index.md) - Auto-generated from docstrings
- [Color Presets](presets/color-presets.md) - Available color grades
- [Transitions](presets/transitions.md) - Transition types and effects
- [Examples](examples/README.md) - Code examples and workflows

## Requirements

- Python 3.10+
- FFmpeg (for video encoding)
- Dependencies: MoviePy, OpenCV, librosa, PySceneDetect, Click, Rich
