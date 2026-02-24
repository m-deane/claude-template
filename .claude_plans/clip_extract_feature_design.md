# Feature Design: `extract-clips` Command

## Overview

A new CLI command that automatically detects and extracts the best scenes from raw drone footage as individual .mp4 files. These clips can then be fed into `drone-reel create` for reel assembly, or used standalone.

---

## 1. CLI UX Design

### Command Signature

```
drone-reel extract-clips [OPTIONS]
```

### Options

| Option | Short | Type | Default | Help |
|--------|-------|------|---------|------|
| `--input` | `-i` | `Path(exists=True)` | **required** | Video file or directory of videos to extract clips from |
| `--output-dir` | `-o` | `Path` | `./clips` | Directory for extracted clip files |
| `--count` | `-n` | `IntRange(1, 100)` | `10` | Maximum number of clips to extract |
| `--min-score` | | `FloatRange(0, 100)` | `30.0` | Minimum scene score threshold (0-100) |
| `--min-duration` | | `FloatRange(0.5, 300)` | `2.0` | Minimum clip duration in seconds |
| `--max-duration` | | `FloatRange(1.0, 300)` | `10.0` | Maximum clip duration in seconds |
| `--quality` | `-q` | `Choice[low,medium,high,ultra]` | `high` | Output quality (low=5M, medium=10M, high=15M, ultra=25M) |
| `--resolution` | | `Choice[source,hd,2k,4k]` | `source` | Output resolution (source=keep original) |
| `--sort` | `-s` | `Choice[score,chronological,duration]` | `score` | Output ordering / naming order |
| `--no-filter` | | `is_flag` | `False` | Skip quality filtering (extract all detected scenes) |
| `--enhanced` | | `is_flag` | `False` | Run enhanced analysis (subject detection, hook potential) for better ranking. Slower. |
| `--json` | | `is_flag` | `False` | Write a sidecar .json manifest with scene metadata |
| `--overwrite` | | `is_flag` | `False` | Overwrite existing clips in output directory |

### Design Decisions for Options

**`--input` accepts files OR directories.** Same pattern as `create` command. When a directory is passed, all video files within it are scanned. This supports the common case of extracting from a single long flight recording and the batch case of processing an entire SD card dump.

**`--count` defaults to 10, max 100.** Ten clips is a practical default for a typical 5-10 minute drone flight. Capping at 100 prevents accidental extraction of hundreds of clips from very long videos, which would be slow and likely unwanted.

**`--resolution` defaults to `source` (not `hd`).** Unlike `create` which produces a finished reel at a target resolution, `extract-clips` preserves the original resolution by default. Users extracting clips for later editing want full-quality source material. The `hd`/`2k`/`4k` options are available for when clips need to be pre-scaled (e.g., saving disk space).

**`--sort` controls both naming and output order.** When set to `score` (default), the best clip is `clip_001`. When `chronological`, clips are numbered by their position in the source video. When `duration`, longest clips come first. This determines the natural ordering when these clips are fed into `drone-reel create --input ./clips/`.

**`--enhanced` is opt-in.** The basic `detect_scenes()` + `_score_scene()` pipeline is fast (~50 ms/scene). Enhanced analysis adds subject detection via DFT saliency (~150 ms/scene) and hook potential scoring. The quality improvement is meaningful but the cost is 3x, so it's opt-in.

**`--no-filter` exists for power users.** Sometimes you want every detected scene, even dark or shaky ones. The flag bypasses `SceneFilter` entirely, only respecting `--min-duration` and `--max-duration`.

**`--json` sidecar is opt-in.** Most users just want the clips. Power users who want to inspect scores, motion types, or pipe metadata into `create` can enable it. The sidecar is always written alongside clips (not a separate output path) to keep the directory self-contained.

**`--overwrite` defaults to safe behavior.** Without the flag, existing files are skipped with a warning. This prevents accidental data loss when re-running extraction with different parameters on the same output directory.

**Not exposed: `--scene-threshold`, `--stabilize`, `--reframe`.** These are implementation details better left to `create`. The extraction command's job is to find and cut the best raw scenes, not to process them. Reframing and stabilization belong in the reel assembly step where they're context-dependent (aspect ratio, platform, etc.).

### Example Invocations

**Basic: Extract top 10 clips from a single video**
```bash
drone-reel extract-clips -i flight_001.mp4
# Creates ./clips/clip_001_s85.mp4 through clip_010_s42.mp4
```

**Specify output directory and count**
```bash
drone-reel extract-clips -i flight_001.mp4 -o ./best_clips -n 5
```

**Extract from an entire directory of videos**
```bash
drone-reel extract-clips -i ./raw_footage/ -o ./selected -n 20 --quality ultra
```

**Enhanced analysis for best possible ranking**
```bash
drone-reel extract-clips -i flight_001.mp4 --enhanced --json
# Creates clips + clips/manifest.json with hook_potential, subject_score, etc.
```

**Extract all scenes (no quality filtering)**
```bash
drone-reel extract-clips -i flight_001.mp4 --no-filter --sort chronological
```

**Pipe into reel creation**
```bash
drone-reel extract-clips -i raw_flight.mp4 -o ./clips -n 15
drone-reel create -i ./clips -m track.mp3 --viral
```

**Strict quality threshold with duration constraints**
```bash
drone-reel extract-clips -i flight.mp4 --min-score 60 --min-duration 3 --max-duration 8
```

### Console Output

**Normal run:**
```
Extracting clips from: flight_001.mp4

  Detecting scenes...  ━━━━━━━━━━━━━━━━  00:03
  Detected 47 scenes (12.4s avg)

  Filtering & ranking... done
  Passed filter: 31 scenes (16 filtered: 9 too dark, 4 too shaky, 3 too short)

  Extracting clips...   ━━━━━━━━━━━━━━━━  00:12
   1/10  clip_001_s85.mp4   00:42-00:47  5.2s  score: 85
   2/10  clip_002_s78.mp4   01:15-01:19  4.1s  score: 78
   3/10  clip_003_s74.mp4   03:02-03:08  6.0s  score: 74
   ...
  10/10  clip_010_s42.mp4   08:11-08:14  2.8s  score: 42

  Extracted 10 clips to ./clips/ (total: 43.2s, 127 MB)
```

**With `--json`:**
```
  ...
  Extracted 10 clips to ./clips/ (total: 43.2s, 127 MB)
  Manifest written to ./clips/manifest.json
```

**Edge case - all filtered:**
```
  Detected 12 scenes

  Filtering & ranking... done
  Passed filter: 0 scenes (12 filtered: 8 too dark, 4 too short)

  Warning: No scenes passed quality filters.
  Tip: Try --no-filter to extract all scenes, or lower --min-score (currently 30.0)
```

**Edge case - file not readable:**
```
  Error: Cannot read video file: flight_001.mp4
  The file may be corrupted or in an unsupported format.
  Supported formats: .mp4, .mov, .avi, .mkv, .webm, .m4v, .wmv, .flv
```

**Edge case - output directory not writable:**
```
  Error: Output directory is not writable: /readonly/path
```

---

## 2. Python API Design

### New Method: `VideoProcessor.write_clip()`

```python
def write_clip(
    self,
    clip: VideoFileClip,
    output_path: Path,
) -> Path:
    """
    Write a single clip to disk with configured encoding parameters.

    Uses the same BT.709 color space, faststart, and VBV bitrate enforcement
    as the main stitch_clips pipeline.

    Args:
        clip: MoviePy VideoFileClip to write (from extract_clip()).
        output_path: Destination .mp4 file path. Parent directories
            are created automatically.

    Returns:
        The output_path after successful write.

    Raises:
        RuntimeError: If encoding fails.
    """
```

**Implementation notes:**
- Reuses the same FFmpeg params block from `stitch_clips()` (lines 483-516): BT.709 color space, yuv420p, faststart, VBV caps.
- Does NOT take a `progress_callback` — individual clips are short enough that per-clip progress is unnecessary. The CLI progress bar tracks clip-level progress (1/10, 2/10, etc.).
- Does NOT handle clip cleanup — the caller (`extract-clips` command) manages the extract/write/close lifecycle.
- Location: Insert after `extract_clip()` (line 259) and before `stitch_clips()` (line 280) in `video_processor.py`.

### No New Public Functions Needed in Other Modules

The extraction pipeline uses only existing public APIs:

| Step | Module | Method |
|------|--------|--------|
| Scene detection | `SceneDetector` | `detect_scenes(video_path)` |
| Enhanced analysis (optional) | `SceneDetector` | `detect_scenes_enhanced(video_path)` |
| Motion/brightness/shake analysis | `scene_analyzer` | `analyze_scenes_batch(scenes)` |
| Quality filtering | `SceneFilter` | `filter_scenes(scenes, motion, brightness, shake)` |
| Clip extraction | `VideoProcessor` | `extract_clip(segment)` |
| Clip writing | `VideoProcessor` | `write_clip(clip, path)` **[NEW]** |
| Resource check | `resource_guard` | `preflight_check(...)` |
| Video info | `VideoProcessor` | `get_video_info(video_path)` |

### Batch Extraction Pattern

The CLI command orchestrates extraction as a sequential loop with proper resource cleanup:

```python
processor = VideoProcessor(
    output_fps=fps,
    video_bitrate=video_bitrate,
    audio_bitrate=audio_bitrate,
)

for i, scene in enumerate(selected_scenes):
    segment = ClipSegment(
        scene=scene,
        start_offset=0.0,
        duration=min(scene.duration, max_duration),
    )
    clip = processor.extract_clip(segment)
    try:
        output_file = output_dir / filename
        processor.write_clip(clip, output_file)
    finally:
        if hasattr(clip, '_source_clip_ref') and clip._source_clip_ref:
            clip._source_clip_ref.close()
        clip.close()
    gc.collect()  # Free numpy arrays between clips
```

Key points:
- Sequential extraction (not parallel) to minimize peak memory on large files.
- Each clip is closed immediately after writing — never hold multiple open clips.
- `gc.collect()` between clips releases any lingering numpy frame buffers.
- `_source_clip_ref.close()` releases the underlying VideoFileClip file handle.

---

## 3. Output File Naming Convention

### Filename Format

```
clip_{NNN}_s{SCORE}.mp4
```

- `NNN`: 3-digit zero-padded index (001-100), ordered by `--sort` mode
- `SCORE`: Integer scene score (0-100), for quick visual scanning in file browsers

**Examples:**
```
clip_001_s85.mp4
clip_002_s78.mp4
clip_003_s74.mp4
...
clip_010_s42.mp4
```

**Why this format:**
- **Index comes first** — files sort naturally in OS file browsers and `ls`
- **Score in filename** — visible without opening metadata; helps manual curation
- **No timestamps in filename** — they're long and hard to read; available in the JSON manifest
- **No duration in filename** — hard to parse at a glance; available in manifest
- **3-digit padding** — supports up to 999 clips without breaking sort order

### JSON Manifest (opt-in via `--json`)

File: `{output_dir}/manifest.json`

```json
{
  "version": 1,
  "source_files": [
    {
      "path": "/absolute/path/to/flight_001.mp4",
      "duration": 623.4,
      "resolution": [3840, 2160],
      "fps": 30
    }
  ],
  "extraction_params": {
    "count": 10,
    "min_score": 30.0,
    "min_duration": 2.0,
    "max_duration": 10.0,
    "quality": "high",
    "resolution": "source",
    "sort": "score",
    "enhanced": false,
    "filtered": true
  },
  "clips": [
    {
      "filename": "clip_001_s85.mp4",
      "source_file": "flight_001.mp4",
      "start_time": 42.3,
      "end_time": 47.5,
      "duration": 5.2,
      "score": 85.1,
      "motion_energy": 62.4,
      "motion_type": "ORBIT_CW",
      "hook_tier": "MAXIMUM",
      "is_golden_hour": false
    }
  ],
  "summary": {
    "total_clips": 10,
    "total_duration": 43.2,
    "total_size_mb": 127.3,
    "avg_score": 65.4,
    "scenes_detected": 47,
    "scenes_filtered": 16
  }
}
```

**Why a manifest:**
- Enables pipeline automation: a script can read `manifest.json` to decide which clips to include in a reel
- Preserves scene metadata that would be lost once clips are individual files
- Future: `drone-reel create` could accept `--manifest manifest.json` to use pre-computed scores/ordering

---

## 4. Integration Points

### Pipeline Flow

```
Input video(s)
    |
    v
[1] SceneDetector.detect_scenes()          # Find scene boundaries
    |                                       # ~50-150 MB memory, streams frames
    v
[2] SceneDetector.detect_scenes_enhanced()  # Optional: if --enhanced flag
    |                                       # Adds subject_score, hook_potential
    v
[3] analyze_scenes_batch(scenes)            # Motion energy, brightness, shake
    |                                       # ThreadPoolExecutor, ~4 workers
    v
[4] SceneFilter.filter_scenes()             # Remove dark/shaky/static scenes
    |                                       # Unless --no-filter
    v
[5] Sort + limit to --count                 # By score (default), chronological, or duration
    |
    v
[6] Duration enforcement                    # Clamp to --min-duration / --max-duration
    |
    v
[7] VideoProcessor.extract_clip()           # Lazy MoviePy subclip, ~50 MB each
    |
    v
[8] VideoProcessor.write_clip()  [NEW]      # Encode to .mp4, BT.709, faststart
    |
    v
[9] Close clip + gc.collect()               # Release file handles + numpy buffers
    |
    v
[repeat 7-9 for each clip]
```

### Exact Functions Called (in order)

```python
# Step 0: Preflight
from drone_reel.utils.resource_guard import preflight_check
issues = preflight_check(output_path, resolution_height, clip_count=count, ...)

# Step 1: Scene detection
from drone_reel.core.scene_detector import SceneDetector
detector = SceneDetector(threshold=27.0)  # Use config default
scenes = detector.detect_scenes(video_path)        # Basic detection
# OR if --enhanced:
scenes = detector.detect_scenes_enhanced(video_path)

# Step 2: Motion analysis (for filtering)
from drone_reel.core.scene_analyzer import analyze_scenes_batch
analysis = analyze_scenes_batch(scenes, include_sharpness=True)

# Step 3: Build filter maps
motion_map = {id(s): analysis[id(s)]["motion_energy"] for s in scenes}
brightness_map = {id(s): analysis[id(s)]["brightness"] for s in scenes}
shake_map = {id(s): analysis[id(s)]["shake_score"] for s in scenes}

# Step 4: Filter (unless --no-filter)
from drone_reel.core.scene_filter import SceneFilter
sf = SceneFilter()
result = sf.filter_scenes(scenes, motion_map, brightness_map, shake_map)
candidates = result.prioritized  # Tiered: high_subject > high_motion > medium_motion

# Step 5: Sort and limit
if sort == "score":
    candidates.sort(key=lambda s: s.score, reverse=True)
elif sort == "chronological":
    candidates.sort(key=lambda s: (str(s.source_file), s.start_time))
elif sort == "duration":
    candidates.sort(key=lambda s: s.duration, reverse=True)
selected = candidates[:count]

# Step 6: Duration enforcement
selected = [s for s in selected if s.duration >= min_duration]
# max_duration applied via ClipSegment.duration during extraction

# Step 7-9: Extract and write
from drone_reel.core.video_processor import VideoProcessor, ClipSegment
processor = VideoProcessor(video_bitrate=video_bitrate, ...)
for i, scene in enumerate(selected):
    segment = ClipSegment(scene=scene, duration=min(scene.duration, max_duration))
    clip = processor.extract_clip(segment)
    try:
        processor.write_clip(clip, output_dir / f"clip_{i+1:03d}_s{int(scene.score)}.mp4")
    finally:
        # cleanup (see section 2)
```

### Thresholds: Exposed vs Hardcoded

| Parameter | Exposed? | Value | Rationale |
|-----------|----------|-------|-----------|
| Scene detection threshold | Hardcoded (27.0) | Config default | Changing this requires understanding PySceneDetect internals; wrong values produce bad results |
| Min motion energy | Hardcoded (25.0) | FilterThresholds default | Filter internals; `--no-filter` bypasses entirely |
| Min brightness | Hardcoded (30.0) | FilterThresholds default | Same rationale |
| Max shake score | Hardcoded (40.0) | FilterThresholds default | Same rationale |
| Min scene score | **Exposed** (`--min-score`) | 30.0 | Users have intuitive control: "only scenes rated 60+" |
| Min/max clip duration | **Exposed** | 2.0s / 10.0s | Directly affects output clip lengths |
| Output quality/bitrate | **Exposed** (`--quality`) | high | Same presets as `create` command |
| Clip count | **Exposed** (`--count`) | 10 | Primary user control |

### Resource Guard Integration

Preflight check runs before any scene detection begins:

```python
issues = preflight_check(
    output_path=output_dir / "clip_001.mp4",
    resolution_height=resolution_height,  # source video height or target
    fps=30,
    clip_count=count,
    stabilize=False,  # extract-clips never stabilizes
    video_bitrate=video_bitrate,
    duration=count * 5.0,  # Conservative: avg 5s per clip
)
```

The resource guard estimates:
- **Memory**: ~200 MB base + 20 MB/clip reference + frame buffers. For 10 clips from 4K: ~500 MB.
- **Disk**: `count * avg_duration * bitrate / 8 * 2` (2x for temp files). For 10 clips at 15 Mbps: ~200 MB.

---

## 5. Edge Cases

### Source video doesn't exist / unreadable

```python
if not input_path.exists():
    # Click handles this via Path(exists=True) — never reaches command body
    pass

# For corrupted files, catch during scene detection:
try:
    scenes = detector.detect_scenes(video_path)
except Exception as e:
    console.print(f"[red]Error:[/red] Cannot read video file: {video_path.name}")
    console.print(f"[dim]The file may be corrupted or in an unsupported format.[/dim]")
    console.print(f"[dim]Supported formats: {', '.join(sorted(VIDEO_EXTENSIONS))}[/dim]")
    raise SystemExit(1)
```

When processing a directory with multiple files, corrupted files are skipped with a warning (matching `create` behavior at cli.py:557).

### All scenes filtered out

Two-tier messaging:

```python
if not candidates:
    console.print(
        f"\n[yellow]Warning:[/yellow] No scenes passed quality filters."
    )
    console.print(
        f"[dim]Tip: Try --no-filter to extract all scenes, "
        f"or lower --min-score (currently {min_score})[/dim]"
    )
    raise SystemExit(1)
```

If `--min-score` is very high (e.g., 90) and no scenes qualify, the message suggests lowering it.

### Output directory already has clips

**Default (no `--overwrite`):** Skip existing files with a per-file warning.

```python
if output_file.exists() and not overwrite:
    console.print(f"  [yellow]Skipping[/yellow] {output_file.name} (already exists)")
    skipped += 1
    continue
```

At the end, if all clips were skipped:
```
  All 10 clips already exist in ./clips/
  Use --overwrite to replace existing files.
```

**With `--overwrite`:** Files are silently replaced.

### Single very long video (1+ hour)

Scene detection streams via FFmpeg and handles any length. The concern is the number of detected scenes (could be hundreds).

Mitigations:
- `analyze_scenes_batch` uses ThreadPoolExecutor with max 4 workers — bounded memory.
- Filtering removes low-quality scenes before extraction.
- `--count` caps the extraction count (default 10).
- Sequential clip extraction with per-clip cleanup keeps memory flat.

For a 1-hour video at 30fps:
- Scene detection: ~200-400 MB, ~30-60 seconds
- Motion analysis of top 30 candidates: ~5 seconds
- 10 clip extractions: ~2 minutes total

### Already-short clips (< min_duration detected scenes)

Scenes shorter than `--min-duration` (default 2.0s) are excluded after filtering:

```python
selected = [s for s in candidates if s.duration >= min_duration]
```

If this removes all candidates, the error message mentions the duration constraint:
```
  Warning: No scenes met the minimum duration of 2.0s.
  Tip: Try --min-duration 1.0 to include shorter scenes.
```

### min_duration > max_duration

Validated immediately:
```python
if min_duration >= max_duration:
    console.print(
        f"[red]Error:[/red] --min-duration ({min_duration}s) must be less than "
        f"--max-duration ({max_duration}s)"
    )
    raise SystemExit(1)
```

### Zero scenes detected

Can happen with uniform footage (no scene transitions):
```
  Detected 0 scenes from flight_001.mp4
  Tip: The video may have no distinct scene changes. Try a lower scene threshold
  or use a video editing tool to manually mark segments.
```

### Disk full during extraction

MoviePy's `write_videofile` raises an exception on write failure. Caught per-clip:

```python
try:
    processor.write_clip(clip, output_file)
except Exception as e:
    console.print(f"  [red]Failed[/red] {output_file.name}: {e}")
    failed += 1
    # Continue with remaining clips — partial extraction is better than none
```

At the end:
```
  Extracted 7 of 10 clips (3 failed). Check disk space.
```

### Multiple input files with overlapping filenames

When `--input` is a directory with multiple video files, clips from different sources get globally numbered:

```
clip_001_s85.mp4   (from flight_001.mp4)
clip_002_s78.mp4   (from flight_002.mp4)
clip_003_s74.mp4   (from flight_001.mp4)
```

The manifest.json includes `source_file` for each clip so provenance is always traceable.

---

## 6. Design Decisions Summary

### Why expose `--count` rather than extract everything

Users typically want "give me the best N clips." Extracting all scenes from a 30-minute video could produce 50+ clips, most of which are mediocre. Defaulting to 10 gives a curated set. `--no-filter --count 100` is available for exhaustive extraction.

### Why `--resolution` defaults to `source` (not `hd`)

Extract-clips serves as a curation step, not a finishing step. Downscaling during extraction permanently loses resolution. Users can always downscale later in `create`, but they can't upscale. Preserving source quality is the safe default for an extraction tool.

### Why no `--reframe` or `--stabilize`

Reframing requires knowing the target aspect ratio and platform, which are `create`-time decisions. Stabilization is computationally expensive and changes the visual character of the clip. Both belong in the reel assembly pipeline where the full context is available.

If a user wants stabilized clips, they should extract first, then process:
```bash
drone-reel extract-clips -i flight.mp4 -o ./clips
drone-reel create -i ./clips --stabilize --output reel.mp4
```

### Why support multiple input files in one command

The common workflow is: mount SD card, extract best clips from all flights. Requiring per-file extraction would be tedious. The `create` command already supports directory input; `extract-clips` should match that pattern.

### Why sequential (not parallel) clip writing

Parallel writing would open multiple VideoFileClip handles to the same source file, each spawning an FFmpeg subprocess. For a 3 GB source:
- Sequential: 1 FFmpeg process, ~200 MB peak, predictable I/O
- 4x parallel: 4 FFmpeg processes, ~800 MB peak, disk thrash on spinning drives

Sequential extraction is simpler, more memory-predictable, and only marginally slower because the bottleneck is I/O (disk read of source + disk write of output), not CPU.

### Why `--sort score` is the default

When clips are later fed into `drone-reel create --input ./clips/`, they're re-analyzed and re-scored. But for standalone use (browsing in Finder, sharing individual clips), having the best clip as `clip_001` is the most useful default.

### Tradeoffs in default values

| Default | Value | Conservative? | Rationale |
|---------|-------|---------------|-----------|
| `--count` | 10 | Moderate | Enough for a 30s reel; not so many that extraction is slow |
| `--min-score` | 30.0 | Liberal | Keeps the "pretty good" clips; users can raise to 60+ for strict curation |
| `--min-duration` | 2.0s | Moderate | Matches `create` command's `min_clip_length` default |
| `--max-duration` | 10.0s | Liberal | Allows longer establishing shots; `create` will trim to fit |
| `--quality` | high (15M) | Good default | Matches `create` default; 4K users should bump to ultra |
| `--resolution` | source | Conservative | Preserves quality; disk is cheap |

---

## 7. Files to Modify

| File | Change | Lines (est.) |
|------|--------|--------------|
| `src/drone_reel/core/video_processor.py` | Add `write_clip()` method | ~35 |
| `src/drone_reel/cli.py` | Add `extract_clips()` command | ~180 |
| `tests/test_video_processor.py` | Add `write_clip()` unit tests | ~40 |
| `tests/test_extract_clips.py` | New file: CLI integration tests | ~200 |
| `docs/cli-reference.md` | Document new command | ~30 |
