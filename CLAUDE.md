# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**drone-reel** is a Python CLI tool that creates Instagram-style vertical reels from drone footage — beat-synced transitions, color grading, intelligent reframing, shake stabilization.

**Stack** — Core: Python 3.10+, MoviePy 2.x, OpenCV, librosa, PySceneDetect | CLI/UX: Click, Rich | Dev: pytest, ruff, black

## Commands

```bash
pip install -e ".[dev]"                                        # install

drone-reel create --input ./clips/ --output reel.mp4 --duration 30
drone-reel create --input ./clips/ --viral -c drone_aerial     # viral preset
drone-reel split -i video.mp4 -o ./out/ --preview               # dry-run: show scenes
drone-reel split -i video.mp4 -o ./out/ --min-duration 5 --max-duration 15 \
  --color drone_aerial --color-intensity 0.65 --vignette 0.3 \
  --auto-speed --letterbox 2.35 --json                           # full post-processing
drone-reel split -i video.mp4 -o ./out/ --min-duration 11 --no-filter --auto-speed
drone-reel analyze --input video.mp4
drone-reel presets && drone-reel platforms

pytest -x                          # stop on first failure
pytest tests/test_scene_detector.py
pytest -k "test_sharpness"
ruff check src/ tests/
black --check src/ tests/
```

## Verification (run in this order after any change)

```bash
ruff check src/ tests/ && black --check src/ tests/ && pytest -x
```

All three must pass. Coverage threshold is 70% (enforced by pytest config).

## Architecture

Pipeline orchestrated by `cli.py` → `create` command:

`SceneDetector` → `SceneFilter` → `SceneSequencer` → `DiversitySelector` → `DurationAdjuster` → `BeatSync` → `VideoProcessor` → `Stabilizer` → `Reframer` → `ColorGrader`

The `split` command runs `SceneDetector` → `SceneFilter` → per-clip post-processing (stabilize → color grade → letterbox) → `VideoProcessor.write_clip()`.

When caption/grading/silent audio is needed, `stitch_clips(return_clip=True)` returns an in-memory clip; all transforms apply before a single `write_videofile()` call (BT.709 + faststart + VBV).

Key files: `src/drone_reel/cli.py` (orchestration), `src/drone_reel/core/` (all pipeline modules), `src/drone_reel/utils/` (config, file utils, resource guard).

## MoviePy 2.x — Don't / Do

**Don't** use 1.x method names — they silently fail or error:
```python
# Wrong (1.x)              # Right (2.x)
clip.subclip(s, e)         clip.subclipped(s, e)
clip.resize(size)          clip.resized(size)
clip.fadein(d)             clip.with_effects([vfx.FadeIn(d)])
clip.set_audio(a)          clip.with_audio(a)
```

**Don't** call `.close()` on a `CompositeVideoClip` in a `finally` block when `return_clip=True` — it sets `self.bg = None` (MoviePy 2.1.2 line 192) and breaks subsequent `get_frame()` calls. In `return_clip` mode, skip all cleanup in the finally block.

**Don't** use `lambda t: [0, 0]` for silent audio — MoviePy passes numpy arrays to `make_frame`, producing only ~3 samples per clip. Check `isinstance(t, np.ndarray)` and return `(N, 2)` for arrays or `(2,)` for scalars. Use amplitude `1e-6` not `0` (AAC encodes pure silence to ~0 duration).

## Encoding Standards

All outputs: `-colorspace bt709 -color_primaries bt709 -color_trc bt709`, `-movflags +faststart`, `-maxrate` (1.5× target) + `-bufsize` (2× target), `audio_codec="aac"`, `yuv420p`.

## `split` Post-Processing Pipeline

Per-clip pipeline (in order): stabilize → `auto_pan_speed_ramp()` → color grade → letterbox

**`auto_pan_speed_ramp()`** (`speed_ramper.py`): full-clip constant-speed correction based on `MotionType` + optical-flow energy:
- PAN >70 energy → 0.65×, PAN 55–70 → 0.80×, PAN 5–20 (sluggish) → 1.25×
- TILT >65 → 0.70×, FLYOVER/APPROACH >70 → 0.70×, FPV >50 → 0.75×
- STATIC/ORBIT/REVEAL/UNKNOWN → no change

**4K HEVC footage**: `SceneDetector.frame_skip` auto-set to 1 for >35fps sources. For DJI 4K 60fps, create a 720p proxy first:
```bash
ffmpeg -i source.MP4 -vf scale=1280:720 -r 30 -c:v libx264 -preset ultrafast -crf 26 -an proxy.mp4
```
Then run `split` on the proxy (~11 min vs 40+ min on raw 4K HEVC).

## Performance

- Stabilizer streams frames on demand — no frame cache (removed to prevent 30 GB+ at 4K)
- FFmpeg threads: `min(cpu_count - 1, cpu_count // 2)`
- `resource_guard.py` checks RAM/disk before rendering (fail-open)
- `gc.collect()` between pipeline stages

## Workflow

- Plans and progress in `.claude_plans/`, tests in `tests/`
- `max_scene_length` on `SceneDetector` must match `--max-duration` on `split` — both default to 10s; the CLI passes `max_duration` through to the detector
