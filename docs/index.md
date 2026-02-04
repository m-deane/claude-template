# Drone Reel Documentation

**drone-reel** is an AI-powered CLI tool that creates Instagram-style vertical reels from drone footage.

## Features

- **Automatic scene detection** with visual quality scoring
- **Beat-synchronized editing** that aligns cuts with music
- **Smart reframing** from landscape to vertical format
- **Color grading presets** optimized for aerial footage
- **Smooth transitions** including crossfade, fade, and zoom effects
- **Video stabilization** with adaptive shake detection and correction

## Quick Start

### Installation

```bash
pip install -e ".[dev]"
```

### Create Your First Reel

```bash
# Basic usage - stitch clips from a folder
drone-reel create --input ./drone_clips/ --output my_reel.mp4

# With music and beat sync
drone-reel create --input ./clips/ --music ./track.mp3 --duration 60

# Full options
drone-reel create \
  --input ./clips/ \
  --music ./music.mp3 \
  --output ./output/reel.mp4 \
  --duration 45 \
  --color cinematic \
  --aspect 9:16 \
  --reframe smart

# With video stabilization (adaptive - skips stable clips)
drone-reel create --input ./clips/ --output reel.mp4 --stabilize

# Force full stabilization on all clips
drone-reel create --input ./clips/ --output reel.mp4 --stabilize-all

# Adjust shake detection threshold (lower = more clips get stabilized)
drone-reel create --input ./clips/ --output reel.mp4 --stabilize --stable-threshold 10
```

## Documentation

- [CLI Reference](cli-reference.md) - All commands and options
- [Python API Reference](api-reference.md) - Using drone-reel as a library
- [Color Presets](presets/color-presets.md) - Available color grades
- [Transitions](presets/transitions.md) - Transition types and effects
- [Examples](examples/README.md) - Code examples and workflows

## Requirements

- Python 3.10+
- FFmpeg (for video encoding)
- Dependencies: MoviePy, OpenCV, librosa, PySceneDetect, Click, Rich
