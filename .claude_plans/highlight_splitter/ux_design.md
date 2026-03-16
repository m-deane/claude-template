# UX Design: `drone-reel split` Command

**Date**: 2026-03-03  
**Status**: Complete Research  
**Purpose**: Design CLI UX for new `split` command that extracts individual highlight clips from a single drone video, with scoring and ranking, but NO reel creation, color grading, or reframing.

---

## Executive Summary

The `split` command is a **lightweight, focused tool** for drone pilots to:
1. Process a single long video file
2. Auto-detect and score scenes
3. Export top-scoring clips as individual files
4. Quickly review which moments were "the best"

It is **NOT** a replacement for `extract-clips`. Instead, it sits between `analyze` (which only reports) and `extract-clips` (which is feature-rich). `split` is optimized for **speed** and **simplicity** with sensible defaults.

---

## 1. Minimal Command

The simplest case should be a one-liner for a pilot who just landed and wants to see their best shots:

```bash
drone-reel split -i DJI_20241029.mp4
```

This should:
- Detect all scenes in the video
- Score them using standard motion/brightness/sharpness heuristics
- Export clips scoring **≥50** (default `--min-score`)
- Write to `./highlights/` directory (not `./clips/` to distinguish from extract-clips)
- Use source resolution and bitrate (minimal re-encoding)
- Show a summary table with scene info and export status

**Default output locations**:
```
./highlights/
  ├── split_001_s92.mp4     # 1st clip: score 92
  ├── split_002_s88.mp4     # 2nd clip: score 88
  ├── split_003_s76.mp4     # 3rd clip: score 76
  └── manifest.json         # [Optional, only with --json]
```

---

## 2. Essential Parameters (Proposed Option Set)

| Option | Short | Type | Default | Description | Rationale |
|--------|-------|------|---------|-------------|-----------|
| `--input` | `-i` | PATH | required | Video file to split | Required; CLI convention matches create/extract-clips |
| `--output-dir` | `-o` | PATH | `./highlights` | Export directory | Convention: diff from extract-clips (./clips) to indicate purpose |
| `--min-score` | | FLOAT | 50 | Minimum quality threshold (0-100) | Sensible middle ground; filters out weak scenes; customizable for fast/thorough |
| `--count` | `-n` | INT | unlimited | Max clips to export | Optional cap; defaults to "all ≥ min-score" for flexibility |
| `--min-duration` | | FLOAT | 2.0 | Skip very short scenes (seconds) | Prevents <1s flickers from being exported |
| `--max-duration` | | FLOAT | 15.0 | Cap clip length (seconds) | Prevents single long scenes from being over-represented |
| `--sort` | `-s` | CHOICE | score | Output order: `score` \| `chronological` | score=best first (default); chronological=timeline order |
| `--preview` | | FLAG | off | Dry-run: list scenes, write nothing | UX gold: safe way to tune thresholds |
| `--json` | | FLAG | off | Write manifest.json with metadata | Useful for batch workflows or re-querying without re-detect |

### Parameters NOT Included (Why Excluded)

| Feature | Exclusion Rationale |
|---------|---------------------|
| `--quality` (low/medium/high/ultra) | **split is for review, not delivery**. Source bitrate is fine; no encoding overhead needed. |
| `--resolution` (hd/2k/4k) | Same reasoning. Pilot wants source quality for assessment. Editing comes later. |
| `--enhanced` (hook potential scoring) | Out of scope. split uses fast scene detection only; extract-clips is the advanced tool. |
| `--no-filter` | Confusing UX. split is built around filtering (min-score). Extract-clips offers this for power users. |
| `--overwrite` | split creates dir if missing; skips existing files. Safer default. |
| `--scene-threshold` | Hidden param; uses detector defaults. Expert users go to extract-clips. |

### Additional Parameters to Consider

**NOT included (scope creep)**:
- `--stabilize` — split is preview mode; stabilization is reel-creation concern
- `--caption` / `--color` — same; these are post-split editing decisions
- `--music` / `--beat-mode` — reel-creation feature; not needed here
- `--platform` — meaningless for individual clips
- Reframing options (`--reframe`, `--ken-burns`) — split exports in source aspect ratio

---

## 3. What to EXCLUDE (vs extract-clips)

Detailed justification for each:

### `--quality` (low/medium/high/ultra)
- **extract-clips use case**: Exporting delivery-ready clips for editing suite or archives
- **split use case**: Quick review on set to decide "do we re-shoot this angle?"
- **Decision**: Source bitrate (minimal re-encoding) is fast and honest
- **Impact**: Saves 40-60% encode time vs high-quality export

### `--resolution` (source/hd/2k/4k)
- **extract-clips**: "I want to downscale to 1080p to save disk"
- **split**: "I want to see it as shot"
- **Decision**: Always source resolution for accurate assessment
- **Impact**: Prevents "oops, I downscaled away the issue" surprise

### `--enhanced` (hook potential scoring)
- **extract-clips**: Subject detection, color variance, motion analysis for sophisticated ranking
- **split**: Fast basic scoring (motion energy, brightness, sharpness)
- **Decision**: split is the quick tool; enhanced analysis goes to extract-clips
- **Impact**: split completes 3-5× faster; good for field use

### `--no-filter` (extract all scenes)
- **extract-clips use case**: "I want every detected scene, even junk"
- **split use case**: Built on the premise of **filtering**
- **Decision**: Remove parameter; `--min-score 0` achieves "extract all" if needed
- **Impact**: Simpler UX; clearer intent

### `--overwrite` (overwrite existing clips)
- **extract-clips**: Power-user tool for batch re-processing
- **split**: Assumes directory is clean or newly created
- **Decision**: Auto-create if missing; skip existing (safer default)
- **Impact**: Can't accidentally trash a day's work with one flag typo

---

## 4. Preview Mode UX

`--preview` is the **killer feature** for field testing. It shows you what WOULD be exported without writing files.

### Command
```bash
drone-reel split -i DJI_20241029.mp4 --min-score 45 --preview
```

### Output Format

A Rich table showing:

```
                       PREVIEW: Would extract 8 clips @ score ≥45
┏━━━━━┳━━━━━━━━┳━━━━━━━━┳──────────┳━━━━━━━┳──────────┳───────────┳────────────┓
┃ # ┃ Start  ┃ End    ┃ Duration ┃ Score ┃ Motion   ┃ Hook     ┃ Filename   ┃
┡━━━━━╇━━━━━━━━╇━━━━━━━━╇──────────╇━━━━━━━╇──────────╇───────────╇────────────┛
│ 1 │ 0:12   │ 0:19   │ 7.2s     │ 92    │ ORBIT_CW │ HIGH     │ split_001… │
│ 2 │ 1:34   │ 1:41   │ 7.1s     │ 88    │ FLYOVER  │ HIGH     │ split_002… │
│ 3 │ 3:02   │ 3:08   │ 6.1s     │ 76    │ PAN_RIGHT│ MEDIUM   │ split_003… │
│ 4 │ 4:45   │ 4:51   │ 6.3s     │ 71    │ STATIC   │ MEDIUM   │ split_004… │
│ 5 │ 6:23   │ 6:29   │ 5.8s     │ 68    │ TILT_UP  │ MEDIUM   │ split_005… │
│ 6 │ 7:51   │ 7:59   │ 8.0s     │ 64    │ REVEAL   │ MEDIUM   │ split_006… │
│ 7 │ 9:12   │ 9:18   │ 6.2s     │ 56    │ PAN_LEFT │ LOW      │ split_007… │
│ 8 │ 11:04  │ 11:10  │ 6.1s     │ 52    │ FPV      │ LOW      │ split_008… │
└───┴────────┴────────┴──────────┴───────┴──────────┴──────────┴────────────┘

Scenes below --min-score (3 filtered out):
  • 2:15 - 2:21 (6.2s, score 42)    [Below threshold]
  • 5:33 - 5:38 (4.8s, score 38)    [Below threshold]
  • 8:47 - 8:53 (5.1s, score 29)    [Below threshold]

Ready to export? Remove --preview and run:
  drone-reel split -i DJI_20241029.mp4 --min-score 45
```

**Columns**:
- `#` — Export sequence number (1-N)
- `Start` / `End` — Timestamps in video
- `Duration` — Clip length (sec)
- `Score` — Quality score (0-100)
- `Motion` — Detected motion type (STATIC, PAN_LEFT, ORBIT_CW, FLYOVER, etc.)
- `Hook` — Hook potential tier (MAXIMUM, HIGH, MEDIUM, LOW, POOR) *optional, only with enhanced*
- `Filename` — What it will be named (split_001_s92.mp4, etc.)

**Below-threshold summary**: Show a few examples of scenes that were filtered out so user can tune `--min-score` if needed.

---

## 5. Output Naming Convention

Two candidates; **Option A recommended**:

### Option A: `split_NNN_sSCORE.mp4` ✓ RECOMMENDED
Example: `split_001_s92.mp4`, `split_002_s88.mp4`

**Pros**:
- Compact, scannable (sequence + quality at a glance)
- Pilot sees `_s92` = "this was excellent" immediately
- Sortable alphabetically = best-first order (when `--sort score`)
- Easy batch rename/move based on quality thresholds

**Cons**:
- Loses source filename context (which input file did this come from?)
- `NNN` zero-padding implies fixed count; if user then exports only top 5, there's a gap

### Option B: `DJI_20241029_highlight_001.mp4`
Example: `DJI_20241029_highlight_001.mp4`, `DJI_20241029_highlight_002.mp4`

**Pros**:
- Preserves source filename for batch operations
- Clear intent (drone footage → highlights)
- Familiar pattern (drone pilots know DJI's naming)

**Cons**:
- Verbose (48 chars vs 20 chars)
- Doesn't show quality score at a glance
- Harder to script ("give me all s≥80" filtering)

### **Recommendation**: **Option A** with Manifest
Use `split_NNN_sSCORE.mp4` + optional `manifest.json`:

```json
{
  "command": "drone-reel split",
  "source_file": "DJI_20241029.mp4",
  "export_time": "2026-03-03T14:32:00Z",
  "params": {
    "min_score": 50,
    "min_duration": 2.0,
    "max_duration": 15.0
  },
  "clips": [
    {
      "filename": "split_001_s92.mp4",
      "index": 1,
      "score": 92,
      "start_time": 12.3,
      "end_time": 19.5,
      "duration": 7.2,
      "motion_type": "ORBIT_CW"
    },
    ...
  ]
}
```

This gives pilots:
- **Fast visual assessment** (score in filename)
- **Batch scripting** (manifest enables "select all score ≥80")
- **Audit trail** (when, what params, what filtered)

---

## 6. Batch Support (Directory Input)

**Should `--input` accept a directory?** 

**Recommended: YES, but with scope limit**

### Design:

```bash
# Single file (common case)
drone-reel split -i DJI_20241029.mp4

# Batch mode: process all video files in directory
drone-reel split -i ./raw_footage/
```

### Batch Output Organization:

```
./highlights/
  ├── DJI_20241029/
  │   ├── split_001_s92.mp4
  │   ├── split_002_s88.mp4
  │   └── manifest.json
  ├── DJI_20241030/
  │   ├── split_001_s85.mp4
  │   └── manifest.json
  └── batch_summary.json
```

**Rationale**:
- **Pilot workflow**: "I have 3 days of footage, give me all highlights"
- **Safety**: Subdirectories prevent filename collisions (two videos both have a "best moment")
- **Cleanup**: Easy to see "which days produced good footage"

**Batch Summary** (`batch_summary.json`):
```json
{
  "batch_mode": true,
  "source_directory": "./raw_footage",
  "total_files": 3,
  "summary": [
    {"file": "DJI_20241029.mp4", "clips_exported": 8, "avg_score": 72},
    {"file": "DJI_20241030.mp4", "clips_exported": 5, "avg_score": 68},
    {"file": "DJI_20241031.mp4", "clips_exported": 12, "avg_score": 76}
  ]
}
```

### Implementation Notes:
- Process files **sequentially** (not parallel) to avoid resource contention
- Graceful skip on corrupt files (already supported in extract-clips)
- Show progress bar per file

---

## 7. UX Comparison Table

| Aspect | `split` | `extract-clips` | `create` |
|--------|---------|-----------------|---------|
| **Purpose** | Quick field review | Curated clip export | Reel creation |
| **Input** | Single file or dir | Single file or dir | Multiple files/dir |
| **Processing** | Fast scene detection | Optional enhanced analysis | Full pipeline (beat sync, diversity, reframing) |
| **Output** | Individual .mp4 clips | Individual .mp4 clips | Single .mp4 reel |
| **Color grading** | ✗ Source only | ✗ Source only | ✓ Full presets |
| **Reframing** | ✗ Source aspect | ✗ Source aspect | ✓ Vertical reframe |
| **Transitions** | N/A | N/A | ✓ Beat-sync'd |
| **Music sync** | ✗ | ✗ | ✓ |
| **Encoding options** | Minimal (source bitrate) | Full (quality/resolution) | Full (quality/resolution) |
| **Typical use case** | Pilot reviews footage at site | Editor selects best moments for reel | Marketing team creates Instagram content |
| **Typical user** | Drone operator | Editor/DP | Content creator |
| **Speed (30min video)** | ~2-4 min | ~5-10 min (enhanced: 15-20) | ~10-30 min |
| **CLI complexity** | 4-5 main options | 8-10 main options | 20+ options |

---

## 8. Command Examples & Workflows

### Example 1: Basic Split (One-Liner)
```bash
$ drone-reel split -i DJI_20241029.mp4
[Detects, exports 6 clips scoring ≥50, shows summary]
Output: ./highlights/split_00{1-6}_s{92,88,76,71,68,64}.mp4
```

### Example 2: Tune with Preview
```bash
# Too many weak clips? Try preview with higher threshold
$ drone-reel split -i DJI_20241029.mp4 --min-score 70 --preview
[Shows 3 clips would be exported at score ≥70]

# Satisfied? Remove --preview
$ drone-reel split -i DJI_20241029.mp4 --min-score 70
```

### Example 3: Chronological Order (For Timeline Review)
```bash
$ drone-reel split -i DJI_20241029.mp4 --sort chronological
Output: ./highlights/split_001_s92.mp4 (appears at 0:12 in source)
        ./highlights/split_002_s88.mp4 (appears at 1:34 in source)
        ... in timeline order, not by score
```

### Example 4: Strict Duration Constraints
```bash
# "I only want clips between 4-8 seconds for my Instagram story"
$ drone-reel split -i DJI_20241029.mp4 --min-duration 4.0 --max-duration 8.0
```

### Example 5: Batch Process Multiple Days
```bash
$ drone-reel split -i ./raw_footage_dir/
./highlights/
  ├── DJI_20241029/split_001_s92.mp4, ...
  ├── DJI_20241030/split_001_s85.mp4, ...
  └── batch_summary.json
```

### Example 6: Capture for Editing Pipeline
```bash
# Export with manifest for downstream tools
$ drone-reel split -i footage.mp4 --json
./highlights/
  ├── split_001_s92.mp4
  ├── ... (5 more)
  └── manifest.json   # [Can be parsed by editor software]
```

### Example 7: Export Everything Above Minimum Duration
```bash
# No quality filter; just "extract scenes ≥2s"
$ drone-reel split -i DJI.mp4 --min-score 0 --min-duration 2.0
```

### Example 8: High-Score Only (Editorial Review)
```bash
# Only the absolute best moments
$ drone-reel split -i DJI.mp4 --min-score 75 --count 5
[Shows top 5 scoring ≥75; useful for storyboards]
```

---

## 9. Help Text & Error Messages

### Help Output
```bash
$ drone-reel split --help

Usage: drone-reel split [OPTIONS]

  Extract individual highlight clips from a drone video.

  Detects scenes, scores them by visual quality (motion, brightness,
  sharpness), and exports the best ones as individual .mp4 files.

  Ideal for quick on-site review before packing up equipment.

Options:
  -i, --input PATH              Video file or directory to split [required]
  -o, --output-dir PATH         Directory for clips [default: ./highlights]
  --min-score FLOAT             Minimum quality threshold 0-100
                                [default: 50]
  -n, --count INT               Max clips to export (1-100); unlimited if
                                not set [default: all ≥min-score]
  --min-duration FLOAT          Skip clips shorter than N seconds
                                [default: 2.0]
  --max-duration FLOAT          Cap clip length at N seconds
                                [default: 15.0]
  -s, --sort [score|chronological]
                                Sort output by: score (best first) or
                                chronological (timeline order)
                                [default: score]
  --preview                     Dry-run: show clips without exporting
  --json                        Write manifest.json with metadata
  --help                        Show this message and exit.

EXAMPLES:
  # Basic: export all clips scoring ≥50
  drone-reel split -i footage.mp4

  # Preview before exporting with higher threshold
  drone-reel split -i footage.mp4 --min-score 70 --preview

  # Batch process multiple files
  drone-reel split -i ./raw_footage/

  # Export top 5 for quick storyboard review
  drone-reel split -i footage.mp4 --min-score 75 --count 5
```

### Error Messages

```bash
# Missing required input
$ drone-reel split
[red]Error:[/red] --input is required. Specify a video file or directory.

# Invalid threshold
$ drone-reel split -i file.mp4 --min-score 150
[red]Error:[/red] --min-score must be 0-100 (got 150)

# min ≥ max
$ drone-reel split -i file.mp4 --min-duration 10 --max-duration 5
[red]Error:[/red] --min-duration (10s) must be ≤ --max-duration (5s)

# No valid scenes
$ drone-reel split -i file.mp4
[red]Error:[/red] No scenes detected. File may be corrupted or too short.
Tip: Run 'drone-reel analyze -i file.mp4' to diagnose.

# Directory not writable
$ drone-reel split -i file.mp4 -o /readonly/
[red]Error:[/red] Output directory not writable: /readonly/
```

---

## 10. Success Output Example

```bash
$ drone-reel split -i DJI_20241029.mp4 --min-score 50

[Progress bar: Detecting scenes... ████████████████ 100%]

Successfully extracted 8 highlights!

Output directory: ./highlights/

Clips by score:
  1. split_001_s92.mp4  (0:12 - 0:19, 7.2s)  [ORBIT_CW]
  2. split_002_s88.mp4  (1:34 - 1:41, 7.1s)  [FLYOVER]
  3. split_003_s76.mp4  (3:02 - 3:08, 6.1s)  [PAN_RIGHT]
  4. split_004_s71.mp4  (4:45 - 4:51, 6.3s)  [STATIC]
  5. split_005_s68.mp4  (6:23 - 6:29, 5.8s)  [TILT_UP]
  6. split_006_s64.mp4  (7:51 - 7:59, 8.0s)  [REVEAL]
  7. split_007_s56.mp4  (9:12 - 9:18, 6.2s)  [PAN_LEFT]
  8. split_008_s52.mp4  (11:04 - 11:10, 6.1s) [FPV]

Next steps:
  • Review clips in ./highlights/
  • Use --preview to tune --min-score threshold
  • Export to reel with: drone-reel create -i ./highlights/ -o reel.mp4

Execution time: 3m 42s
```

---

## 11. Implementation Considerations

### Parameter Validation (Click decorators)
```python
@click.option(
    "--input", "-i",
    type=click.Path(exists=True, path_type=Path),
    required=True,
    help="Video file or directory"
)
@click.option(
    "--output-dir", "-o",
    type=click.Path(path_type=Path),
    default="./highlights",
    help="Export directory [default: ./highlights]"
)
@click.option(
    "--min-score",
    type=click.FloatRange(0, 100),
    default=50,
    help="Minimum quality threshold 0-100"
)
@click.option(
    "--count", "-n",
    type=click.IntRange(1, 500),  # Set high; check count ≤ detected scenes
    default=None,
    help="Max clips to export (omit for unlimited)"
)
@click.option(
    "--min-duration",
    type=click.FloatRange(0.5, 300),
    default=2.0,
    help="Skip clips shorter than N seconds"
)
@click.option(
    "--max-duration",
    type=click.FloatRange(1.0, 300),
    default=15.0,
    help="Cap clip length at N seconds"
)
@click.option(
    "--sort", "-s",
    type=click.Choice(["score", "chronological"]),
    default="score",
    help="Output order"
)
@click.option(
    "--preview",
    is_flag=True,
    default=False,
    help="Dry-run: show clips without exporting"
)
@click.option(
    "--json",
    is_flag=True,
    default=False,
    help="Write manifest.json"
)
```

### Code Reuse
- **Scene detection**: Reuse `SceneDetector.detect_scenes()` (already in pipeline)
- **VideoProcessor**: Reuse extraction logic from `extract_clips` command
- **Rich tables**: Use existing `Table` + `Panel` patterns
- **File utils**: Reuse `find_video_files()`, `format_duration()`

### Key Differences from extract-clips
- No `--quality`, `--resolution` options
- No `--enhanced` (always fast detection)
- No `--no-filter` (filtering is the core feature)
- No `--overwrite` (safe defaults: create dir, skip existing)
- Default output dir: `./highlights` not `./clips`
- Default `--min-score`: 50 not 30

---

## 12. Testing Strategy (Brief)

**Split-specific tests**:
1. Basic single-file split
2. Batch directory processing (multiple files)
3. Preview mode (no files written)
4. Preview + execute (files match preview)
5. Threshold filtering (verify correct scenes selected)
6. Duration constraints (min/max)
7. Sort modes (score vs chronological)
8. Manifest JSON structure
9. Error cases (no video found, unwritable dir, etc.)

**Reuse from extract-clips**:
- Scene detection (already well-tested)
- Bitrate/format encoding (minimal changes)
- File naming logic (split_NNN_sSCORE pattern)

---

## Summary: Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Output dir**: `./highlights/` not `./clips/` | Signals purpose (review) vs extract-clips (curation) |
| **Naming**: `split_NNN_sSCORE.mp4` | Compact, scannable, batch-scriptable |
| **Default min-score**: 50 | Sweet spot: filters trash, keeps good moments |
| **No --quality param** | split is preview; source bitrate is fine and fast |
| **--preview flag** | Killer feature for field tuning without re-processing |
| **Batch + subdirs** | Real pilot workflow (multi-day shoots) |
| **Manifest.json optional** | Good for pipelines; not required for casual use |
| **No --enhanced** | split is the "fast tool"; extract-clips is the "precise tool" |

---

**End of UX Design Document**
