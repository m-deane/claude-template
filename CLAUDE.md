# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**drone-reel** is a Python CLI tool that creates Instagram-style vertical reels from drone footage. It automatically stitches video clips with beat-synced transitions, color grading, intelligent reframing, and shake detection/stabilization.

**Technology Stack**: Python 3.10+, MoviePy 2.x, OpenCV, librosa, PySceneDetect, Click, Rich

## Build & Development Commands

```bash
# Install in development mode
pip install -e ".[dev]"

# Run the CLI
drone-reel create --input ./clips/ --output reel.mp4 --duration 30
drone-reel create --input ./clips/ --viral -c drone_aerial    # Quick viral preset
drone-reel create --input ./clips/ -m track.mp3 --beat-mode downbeat
drone-reel analyze --input video.mp4
drone-reel presets
drone-reel platforms

# Tests (coverage configured in pyproject.toml, threshold: 70%)
pytest                                # All 1033+ tests with coverage
pytest tests/test_scene_detector.py   # Single test file
pytest -k "test_sharpness"            # Run specific test by name
pytest -x                             # Stop on first failure

# Linting
ruff check src/ tests/
black --check src/ tests/
```

## Architecture

### Processing Pipeline

The `create` command in `cli.py` orchestrates this pipeline:

1. **SceneDetector** (`scene_detector.py`) - Detects scene boundaries via PySceneDetect ContentDetector. Scores each scene on sharpness, color variance, brightness, motion. Outputs `EnhancedSceneInfo` with `motion_type`, `hook_tier`, `subject_score`.

2. **SceneFilter** (`scene_filter.py`) - Filters scenes by motion energy, brightness, shake score with progressive relaxation fallback if too few pass.

3. **SceneSequencer** (`scene_sequencer.py`) - Hook-based reordering: best scene at position 0, narrative arc distribution (Hook/Build/Climax/Resolution).

4. **DiversitySelector** (`sequence_optimizer.py`) - Balances quality (70%) with content diversity (30%). Enforces minimum scene counts per duration. `select_with_minimum()` applies progressive relaxation.

5. **DurationAdjuster** (`duration_adjuster.py`) - Interest-adaptive clip durations based on hook tier. Auto-scales up to 2.5x if short of target.

6. **BeatSync** (`beat_sync.py`) - Extracts tempo/beats/downbeats via librosa. Generates cut points aligned with musical structure. Falls back to uniform cuts when no beats detected.

7. **VideoProcessor** (`video_processor.py`) - Central orchestrator: extracts clips, applies transitions, stabilization, speed ramping, stitches via `concatenate_videoclips`. Has `return_clip=True` mode for in-memory post-processing chain.

8. **Stabilizer** (`stabilizer.py`) - Feature-based optical flow stabilization. Adaptive (skip stable clips) or full mode.

9. **Reframer** (`reframer.py`) - Landscape-to-vertical conversion. Modes: CENTER, SMART, KEN_BURNS, PUNCH_IN, SUBJECT_TRACK.

10. **ColorGrader** (`color_grader.py`) - Float32 color space with Bayer-matrix dithering. Auto shadow lift in LAB space. 11 presets including `drone_aerial`.

### Post-Processing Pipeline (in `cli.py`)

When caption, color grading, or silent audio is needed, `stitch_clips(return_clip=True)` returns an in-memory clip. Then applied sequentially:
1. Silent audio injection (when no music)
2. Caption overlay via `TextRenderer`
3. Color grading via `grade_transform()`
4. Single `write_videofile()` call with BT.709 + faststart + VBV params

### Key Data Structures

- **EnhancedSceneInfo**: Scene with start/end times, score, motion_type, hook_potential, hook_tier, subject_score
- **MotionType**: STATIC, PAN_LEFT/RIGHT, TILT_UP/DOWN, ORBIT_CW/CCW, FLYOVER, REVEAL, FPV
- **HookPotential**: MAXIMUM (>=80), HIGH (>=65), MEDIUM (>=45), LOW (>=25), POOR (<25)
- **ClipSegment**: Video segment with scene reference, duration, transition settings
- **TransitionType**: CUT, CROSSFADE, FADE_BLACK, FADE_WHITE, ZOOM_IN/OUT, SLIDE_LEFT/RIGHT

## Critical MoviePy 2.x Patterns

This project uses MoviePy 2.x which has breaking changes from 1.x:

```python
# Correct 2.x imports
from moviepy import VideoFileClip, concatenate_videoclips, vfx, afx, CompositeVideoClip

# Method changes (NOT the 1.x names)
clip.subclipped(start, end)           # Not subclip()
clip.resized(target_size)             # Not resize()
clip.with_effects([vfx.FadeIn(d)])    # Not fadein()
clip.with_audio(audio)                # Not set_audio()
clip.with_start(t)                    # Not set_start()
clip.with_duration(d)                 # Not set_duration()
clip.with_position(pos)               # Not set_position()
clip.transform(func)                  # (get_frame, t) -> frame
```

### MoviePy Gotchas (hard-won lessons)

1. **CompositeVideoClip.close() sets self.bg = None** (MoviePy 2.1.2 line 192). Any `finally` block that closes a CompositeVideoClip will break subsequent `get_frame()` calls. When using `return_clip=True`, the finally block must NOT close the returned clip.

2. **AudioClip make_frame must handle vectorized t**. MoviePy passes numpy arrays of time points, not just scalars. A naive `lambda t: [0, 0]` only produces ~3 samples for a 3-second clip. Must check `isinstance(t, np.ndarray)` and return `(N, 2)` for arrays, `(2,)` for scalars.

3. **AAC encodes pure silence to ~0 duration**. Use amplitude `1e-6` (inaudible) instead of `0` for silent audio tracks.

## Encoding Standards

All output files use these FFmpeg parameters for platform compatibility:
- BT.709 color space: `-colorspace bt709 -color_primaries bt709 -color_trc bt709`
- Streaming optimized: `-movflags +faststart`
- Bitrate controlled: `-maxrate` (1.5x target) + `-bufsize` (2x target) VBV caps
- Audio: `audio_codec="aac"`, silent stereo track injected when no music provided
- Pixel format: `yuv420p`

## Configuration

User config at `~/.config/drone_reel/config.json`. CLI arguments override config values. Key defaults:
- `scene_threshold`: 27.0 (lower = more scene cuts)
- `min_clip_length` / `max_clip_length`: 2.0-4.0s
- `transition_duration`: 0.3s
- `output_fps`: 30

## Memory & Performance Considerations

- Stabilizer does NOT cache frames (was removed to prevent 30 GB+ memory at 4K)
- FFmpeg threads capped at `min(cpu_count - 1, cpu_count // 2)` to allow parallel renders
- Resource preflight guard (`utils/resource_guard.py`) checks RAM/disk before rendering
- `gc.collect()` called between pipeline stages to free numpy arrays
- 4K ultra renders: ~1 GB peak memory per render, ~1h for 30s

## Workflow Guidelines

- Store project plans and progress in `.claude_plans/` directory
- Write all tests to `tests/` folder
- Always run tests after significant changes: `pytest -x`
- Never use mock data or workarounds - implement complete working code
- No partial implementations, stubs, TODOs, or placeholder functions
