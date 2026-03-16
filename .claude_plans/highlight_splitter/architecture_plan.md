# Highlight Splitter Architecture Plan

## Executive Summary

The highlight splitter command is a **simplified, lightweight extraction tool** that identifies and exports visually compelling scenes from a single raw video file. Unlike the full `create` command (which stitches clips into a finished reel), `split` focuses on **detection, filtering, and export only**—no transitions, reframing, color grading, music sync, or sequencing.

### Key Insight
The highlight splitter should be a **new dedicated command**, NOT a refactored extract-clips with flags. While superficially similar, their use cases, UX patterns, and feature roadmaps are distinct.

---

## 1. New Command vs Refactor: Decision

### Recommendation: **New `split` Command**

**Why NOT refactor extract-clips:**
- **Code clarity**: Extract-clips handles 10+ quality/resolution/filtering modes. Splitter is 90% simpler.
- **Backward compatibility**: Extract-clips is a stable public API. Refactoring introduces risk of breaking existing workflows.
- **Feature divergence**: Splitter will gain unique features (preview thumbnails, scene annotation metadata, ML-based highlight ranking) that don't belong in extract-clips.
- **CLI idiom**: `split` is a single-file operation with simple output (numbered clips). Extract-clips is batch processing with tier-based filtering. Different mental models.
- **Maintenance burden**: Adding a `--simple` mode to extract-clips would bloat the function, require double testing, and confuse users about which path to use.

**Trade-off acceptance:**
- ~15-20 lines of duplicated parameter parsing (acceptable vs coupling).
- Two similar functions in cli.py (mitigated by extracting shared logic into `_highlight_splitter_worker()` utility).
- Slight code duplication in scene detection calls (MoviePy frame reads—unavoidable unless we architect for streaming, which adds complexity).

**Analogy**: Git has both `git add` and `git stage`—different commands, same semantics. It's OK.

---

## 2. Code Reuse Map

### What GETS Called

| Component | Function | Usage | Notes |
|-----------|----------|-------|-------|
| **SceneDetector** | `detect_scenes(video_path)` | ✅ Used as-is | Outputs scenes with score, time bounds |
| **analyze_scenes_batch** | `analyze_scenes_batch(scenes, include_sharpness=True)` | ✅ Used as-is | Returns motion_energy, brightness, shake_score, sharpness per scene |
| **SceneFilter** | `SceneFilter.filter_scenes()` | ✅ Used as-is | Tiered filtering (high_subject → high_motion → medium_motion → low_motion) |
| **VideoProcessor** | `write_clip(scene, output_path)` | ✅ Used as-is | Exports individual clip to MP4 (handles codec/bitrate) |
| **Config** | `load_config() + merge_cli_args()` | ✅ Used as-is | User config (~/.config/drone_reel/config.json) |
| **file_utils** | `find_video_files()`, `get_unique_output_path()` | ✅ Used as-is | Path handling, uniqueness guards |

### What DOESN'T Get Called (Pipeline Stages Skipped)

| Component | Why Skipped |
|-----------|------------|
| **BeatSync** | No music input; splitter works with raw footage |
| **SceneSequencer** | No narrative arc; splitter exports clips in chronological order |
| **DiversitySelector** | No content balance needed; all high-scoring scenes are exported |
| **DurationAdjuster** | Clips exported at natural durations; no time budget |
| **Reframer** | Optional later; v1 exports at original aspect ratio |
| **ColorGrader** | Optional later; v1 exports without grading |
| **Stabilizer** | Optional later; v1 skips by default |
| **Speed ramping** | No reel assembly; no musical timing needed |
| **TextOverlay/Captions** | No text—just numbered clips |

---

## 3. Module Structure

### Option A: Thin CLI Function (Recommended)
```
cli.py
├── split() command
│   ├── Validation (input, output, params)
│   ├── Scene detection (SceneDetector)
│   ├── Filtering (SceneFilter)
│   ├── Export loop (VideoProcessor.write_clip)
│   └── Reporting
```

**No new module file needed.** The command is straightforward enough to stay in cli.py (estimated 120 lines).

**Pros:**
- No additional imports or cross-file dependencies.
- Easy to find, modify, test.
- Follows existing `extract-clips` pattern.

**Cons:**
- cli.py grows by ~120 lines (acceptable; it's already 1.8K lines).

### Option B: Dedicated HighlightSplitter Class
```
core/highlight_splitter.py
├── class HighlightSplitter
│   ├── __init__(scene_threshold, filter_thresholds, quality)
│   ├── split(video_path, output_dir, clip_naming)  # -> list[Path]
│   └── _export_metadata(scenes, output_json)      # Optional
```

**Pros:**
- Reusable for batch operations (`split_batch()`).
- Testable without CLI.
- Extensible for ML ranking, scene annotation.

**Cons:**
- Premature abstraction if we're only building a CLI command.
- Adds an import; marginal benefit.

**Decision: Skip for v1.** Go with Option A. If batch splitting or ML ranking arrives in Phase 2, refactor to HighlightSplitter class.

---

## 4. Implementation Size Estimate

### Breakdown by Component

| Component | File | Est. LOC | Notes |
|-----------|------|---------|-------|
| CLI command definition | cli.py | 120 | Decorators, validation, reporting |
| Worker/utility logic | cli.py | 40 | Scene detection loop, export loop |
| Unit tests | tests/test_split.py | 180 | Parameter validation, filtering, edge cases |
| Integration test | tests/test_split.py | 80 | Mock video, end-to-end flow |
| **TOTAL** | | **420** | |

### Files Changed
- **src/drone_reel/cli.py** — Add ~160 lines for new command (split + helper)
- **tests/test_split.py** — Create new, ~260 lines
- **src/drone_reel/__init__.py** — No change (split is CLI-only, not a reusable module)

---

## 5. Performance for 1 GB 4K

### Time Breakdown (Estimated, Sequential)

| Stage | Time | Notes |
|-------|------|-------|
| Scene detection (PySceneDetect) | ~2-3 min | ContentDetector, 50 frames/s, analyze_scale=0.5 |
| Scene analysis (motion/brightness/shake) | ~1.5 min | analyze_scenes_batch w/ 4 workers, optical flow |
| Filtering (CPU-bound) | <1 sec | Threshold logic only |
| Exporting (N clips × codec) | ~8-15 min | Bottleneck: FFmpeg encode (depends on scene count & clip durations) |
| **Total wall time** | **~12-20 min** | Dominated by export |

### Parallelization Opportunities

✅ **Already parallelizable:**
- `analyze_scenes_batch()` uses ThreadPoolExecutor with 4 workers (already implemented).
- Scene detection (PySceneDetect) is inherently single-threaded per file, but OK for single-input use case.

❓ **Export parallelization:**
- Multiple VideoProcessor.write_clip() calls could run in parallel via ThreadPoolExecutor.
- Trade-off: 2-3 parallel encodes at 30 FPS 4K = ~4 GB memory + 2-3× FFmpeg process overhead.
- **Decision for v1**: Sequential export. v2 can add `--parallel N` flag if needed.

**Predicted v1 output:** 1 GB 4K video → 15-20 scenes → 8-12 min for scene detection/analysis, 10-15 min for export = **25-35 min total**.

---

## 6. Test Strategy

### Unit Tests (in `test_split.py`)

**Parameter Validation:**
- `--min-score` > 100 → error
- `--min-duration` > `--max-duration` → error
- Invalid input path → error
- Output dir not writable → error
- No video files found → error

**Filtering Logic:**
- Scene with motion_energy < threshold filtered out
- Scene with brightness < 30 or > 245 filtered out
- Scene with shake_score > 40 filtered out
- Low-motion scenes included if count threshold not met (progressive relaxation)

**Naming & Export:**
- Output clips named `clip_001.mp4`, `clip_002.mp4`, etc.
- Unique naming when files already exist (append counter)
- JSON metadata (if enabled) contains scene data

### Integration Tests

**Mock Video Approach:**
- Create synthetic 5-second CV2 VideoWriter clip (frames with motion patterns).
- Pass through SceneDetector, analyze, filter, export.
- Assert: 1-3 scenes detected, clips written to disk, file sizes > 0.

**Test Case:**
```python
def test_split_integration_with_synthetic_video():
    # Create temp 5s video (100 frames, 1280x720)
    # Add 2 scene cuts + motion
    # Run split command
    # Assert: 2 clips exported, metadata correct
```

### Coverage Target
- Aim for **80%+ coverage** on new `split` code (currently project threshold is 70%).
- Focus on: parameter validation, filtering tiers, export loop.
- Mock VideoProcessor.write_clip() to avoid actual encoding in tests.

---

## 7. Justification: Separate Command

### Key Question: Does extract-clips already do this well enough?

**Short answer: No.**

**Detailed analysis:**

**extract-clips current purpose:**
- Batch process multiple video files.
- Apply quality/resolution/bitrate tiers for different use cases.
- Output clips with extensive filtering/scoring metadata.
- Focus: "Extract N best scenes across a shoot library."

**split desired purpose:**
- Single video file input only.
- Simple, fast scene detection.
- Export all high-quality scenes without tuning.
- Focus: "Quick highlight pass on a single long drone recording."

**Specific UX differences:**

| Aspect | extract-clips | split |
|--------|---------------|-------|
| **Input** | Directory or multiple files | Single video file |
| **Output count** | Exact (top N) | Determined by quality threshold |
| **Filtering** | Sophisticated (8 tiers) | Simple (good/bad) |
| **Params** | 13 options (quality, resolution, sort, etc.) | 5 options (threshold, min-duration, output-dir, etc.) |
| **Use case** | "I shot 2 GB of material across 10 clips; give me top 20 scenes" | "I have 1 raw 30 min file; split into chapters" |
| **Advanced users** | Video editors wanting fine control | Content creators wanting quick preview |

**Why UX improves with a separate command:**
1. **Discoverability**: New users run `drone-reel split --help` and immediately understand it extracts highlights.
2. **Simplicity**: No confusing `--quality` option for a tool focused on detection, not encoding variants.
3. **Defaults**: `--min-score 60` is a sensible default for "good-looking" clips. Extract-clips defaults to top-N, not quality-based.
4. **Future features**: Splitter gains thumbnails (`--preview`), scene merging (`--merge-proximity 5s`), ML ranking (`--ml-rank`) without bloating extract-clips.

**Precedent:**
- FFmpeg: `ffprobe` is separate from `ffmpeg` (analysis vs transformation).
- ImageMagick: `identify` is separate from `convert` (inspection vs processing).
- Git: `git log` is simpler/faster than `git show` (read-only vs full object).

---

## 8. Feature Roadmap (Post-MVP)

**Phase 2 (after MVP):**
- `--preview` flag: Generate JPEG thumbnails for each clip.
- `--merge-proximity 5s`: Merge scenes closer than N seconds (chapter grouping).
- `--json-metadata` flag: Export scene data (times, scores, motion types) as JSON.

**Phase 3 (exploratory):**
- ML-based highlight ranking (beyond motion/brightness).
- Audio peak detection (sync with music even in raw file).
- Transition recommendation (suggest best transition between consecutive scenes).

---

## Summary

- **Use separate `split` command** for clarity, maintainability, and future extensibility.
- **No new module file** in v1; everything lives in cli.py (~160 new lines).
- **Reuse SceneDetector, analyze_scenes_batch, SceneFilter, VideoProcessor** as-is.
- **Skip** sequencer, diversity selector, reframing, color grading, audio sync.
- **Performance**: 25-35 min for 1 GB 4K (dominated by FFmpeg encode, not analysis).
- **Tests**: 30+ unit tests + integration test; target 80%+ coverage.
- **Justification**: Different use case, simpler UX, extensible architecture.

