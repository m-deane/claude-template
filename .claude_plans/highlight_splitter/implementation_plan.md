# Highlight Splitter Implementation Plan

## Overview
Build a lightweight `drone-reel split` command to detect and export high-quality scenes from a single video file. **No code to write yet**—this is the step-by-step blueprint for Phase 2 after architecture approval.

---

## Step 1: Add CLI Command Skeleton

**File**: `src/drone_reel/cli.py`

**Location**: After `extract_clips()` function (around line 1750), add new command:

```python
@main.command(name="split")
@click.option("--input", "-i", ..., required=True, help="Input video file")
@click.option("--output", "-o", ..., default="./highlights", help="Output directory")
@click.option("--min-score", ..., default=60.0, help="Min quality threshold")
@click.option("--min-duration", ..., default=1.5, help="Min clip duration (s)")
@click.option("--max-duration", ..., default=10.0, help="Max clip duration (s)")
@click.option("--quality", ..., default="high", help="Export bitrate")
def split(input_path, output_dir, min_score, min_duration, max_duration, quality):
    """Split a video into highlight clips."""
    # Placeholder body
    pass
```

**Estimated LOC**: 30 (decorators + signature)

**Test checkpoint**: CLI definition loads without errors.
```bash
drone-reel split --help
```

---

## Step 2: Implement Parameter Validation

**File**: `src/drone_reel/cli.py` (inside `split()` function)

**Tasks**:
1. Check `input_path` is a file (not directory).
2. Check `input_path` is a supported video format.
3. Validate `min_duration < max_duration`.
4. Create/verify output directory is writable.
5. Validate `min_score` in range [0, 100].
6. Parse quality preset (low/medium/high/ultra) → bitrate tuple.

**Reuse**: Copy pattern from extract-clips (lines 1390-1440):
```python
# Check input is a file
if not input_path.is_file():
    ...
    raise SystemExit(1)

# Check is video file
from drone_reel.utils.file_utils import is_video_file
if not is_video_file(input_path):
    ...

# Check output dir writable
output_dir = Path(output_dir)
if not output_dir.exists():
    output_dir.mkdir(parents=True, exist_ok=True)
...

# Parse quality
quality_presets = {"low": ("5M", "128k"), ...}
video_bitrate, audio_bitrate = quality_presets[quality]
```

**Estimated LOC**: 40

**Test checkpoint**: Run pytest on new validation tests.
```bash
pytest tests/test_split.py::TestSplitValidation -v
```

---

## Step 3: Scene Detection Loop

**File**: `src/drone_reel/cli.py` (inside `split()` function)

**Tasks**:
1. Instantiate `SceneDetector(threshold=27.0, min_scene_length=1.0)`.
2. Call `detector.detect_scenes(input_path)`.
3. Handle exceptions (corrupted video, unsupported codec).
4. Print scene count to console.

**Code pattern**:
```python
from drone_reel.core.scene_detector import SceneDetector

scene_detector = SceneDetector()
try:
    all_scenes = scene_detector.detect_scenes(input_path)
except Exception as e:
    console.print(f"[red]Error:[/red] Scene detection failed: {e}")
    raise SystemExit(1)

if not all_scenes:
    console.print("[yellow]No scenes detected[/yellow]")
    raise SystemExit(1)

console.print(f"  Detected {len(all_scenes)} scenes")
```

**Estimated LOC**: 20

**Test checkpoint**: Mock SceneDetector; verify exception handling.
```bash
pytest tests/test_split.py::TestSplitDetection -v
```

---

## Step 4: Scene Analysis & Filtering

**File**: `src/drone_reel/cli.py` (inside `split()` function)

**Tasks**:
1. Call `analyze_scenes_batch(all_scenes, include_sharpness=True)`.
2. Extract motion_energy, brightness, shake_score into maps.
3. Instantiate `SceneFilter(FilterThresholds(...))`.
4. Call `filter.filter_scenes()` to get FilterResult.
5. Apply `min_score` threshold to candidates.
6. Report filtering stats (dark filtered, shaky filtered, low score).

**Code pattern**:
```python
from drone_reel.core.scene_analyzer import analyze_scenes_batch
from drone_reel.core.scene_filter import SceneFilter, FilterThresholds

analysis = analyze_scenes_batch(all_scenes, include_sharpness=True)

motion_map = {id(s): analysis[id(s)]["motion_energy"] for s in all_scenes}
brightness_map = {id(s): analysis[id(s)]["brightness"] for s in all_scenes}
shake_map = {id(s): analysis[id(s)]["shake_score"] for s in all_scenes}

sf = SceneFilter()
filter_result = sf.filter_scenes(all_scenes, motion_map, brightness_map, shake_map)

# Apply min_score threshold to prioritized list
candidates = [s for s in filter_result.prioritized if s.score >= min_score]

# Report
console.print(f"  After filtering: {len(candidates)} candidates")
```

**Estimated LOC**: 35

**Test checkpoint**: Mock analysis results; verify filtering logic.
```bash
pytest tests/test_split.py::TestSplitFiltering -v
```

---

## Step 5: Duration Filtering & Sorting

**File**: `src/drone_reel/cli.py` (inside `split()` function)

**Tasks**:
1. Filter candidates by duration: `min_duration <= scene.duration <= max_duration`.
2. Sort by `scene.score` descending (best first).
3. Report final clip count.

**Code pattern**:
```python
candidates = [
    s for s in candidates
    if min_duration <= s.duration <= max_duration
]

candidates = sorted(candidates, key=lambda s: s.score, reverse=True)
console.print(f"  Final selection: {len(candidates)} clips")
```

**Estimated LOC**: 10

**Test checkpoint**: Test boundary conditions (min_duration edge cases).
```bash
pytest tests/test_split.py::TestSplitDuration -v
```

---

## Step 6: Output Path Naming & Uniqueness

**File**: `src/drone_reel/cli.py` (inside `split()` function, pre-export loop)

**Tasks**:
1. Build list of output paths: `clip_001.mp4`, `clip_002.mp4`, etc.
2. Check for file existence; warn if overwriting (unless `--overwrite` flag).
3. Use `get_unique_output_path()` if needed.

**Code pattern**:
```python
output_clips = []
for i, scene in enumerate(candidates, 1):
    clip_path = output_dir / f"clip_{i:03d}.mp4"
    if clip_path.exists():
        console.print(f"  [yellow]Warning:[/yellow] {clip_path.name} exists; will overwrite")
    output_clips.append(clip_path)
```

**Estimated LOC**: 15

**Test checkpoint**: Test clip naming and uniqueness logic.
```bash
pytest tests/test_split.py::TestSplitNaming -v
```

---

## Step 7: Export Loop

**File**: `src/drone_reel/cli.py` (inside `split()` function)

**Tasks**:
1. Create VideoProcessor with bitrate/codec settings.
2. Loop through `candidates` and `output_clips` in parallel.
3. Call `processor.write_clip(scene, output_path, video_bitrate, audio_bitrate)`.
4. Handle per-clip exceptions (skip corrupted clips, warn).
5. Track progress with Rich progress bar.

**Code pattern**:
```python
from drone_reel.core.video_processor import VideoProcessor
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

processor = VideoProcessor(
    output_fps=30,
    video_bitrate=video_bitrate,
    audio_bitrate=audio_bitrate,
    preset="medium"
)

with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TimeElapsedColumn(),
    console=console,
) as progress:
    task = progress.add_task("Exporting clips...", total=len(candidates))
    
    successful = 0
    for scene, output_path in zip(candidates, output_clips):
        try:
            processor.write_clip(scene, output_path)
            successful += 1
        except Exception as e:
            console.print(f"  [yellow]Warning:[/yellow] Skipped {output_path.name}: {e}")
        progress.advance(task)

console.print(f"  Exported {successful}/{len(candidates)} clips")
```

**Estimated LOC**: 35

**Test checkpoint**: Mock VideoProcessor; verify loop logic.
```bash
pytest tests/test_split.py::TestSplitExport -v
```

---

## Step 8: Reporting & Final Summary

**File**: `src/drone_reel/cli.py` (inside `split()` function, final)

**Tasks**:
1. Print summary table (input file, duration, scenes detected, filtered, exported).
2. List output clips with times and scores.
3. Print disk space used.
4. Print time elapsed.

**Code pattern**:
```python
import os

total_size = sum(c.stat().st_size for c in output_clips if c.exists())
size_mb = total_size / (1024 * 1024)

console.print(Panel.fit(
    f"[bold green]✓ Complete[/bold green]\n"
    f"Exported {successful} clips\n"
    f"Total size: {size_mb:.1f} MB\n"
    f"Location: {output_dir}",
    border_style="green"
))
```

**Estimated LOC**: 20

**Test checkpoint**: Integration test (end-to-end with mock video).
```bash
pytest tests/test_split.py::TestSplitIntegration -v
```

---

## Step 9: Unit Tests

**File**: `tests/test_split.py` (create new)

**Test Classes & Coverage**:

### TestSplitValidation (30 tests)
- Input path doesn't exist → error
- Input path is directory (not file) → error
- Input file not a video → error
- min_duration >= max_duration → error
- min_score > 100 → error
- min_score < 0 → error
- Output dir not writable → error
- Output dir doesn't exist → creates it

### TestSplitDetection (15 tests)
- Mock SceneDetector returns N scenes
- Exception in detector → caught, error printed
- 0 scenes detected → exit with warning
- Scene times computed correctly
- Scene scores assigned

### TestSplitFiltering (20 tests)
- Scene below motion_energy threshold filtered
- Scene too bright filtered
- Scene too dark filtered
- Scene too shaky filtered
- Low-motion scenes included when count low (progressive relaxation)
- Prioritization: high_subject > high_motion > medium_motion

### TestSplitDuration (15 tests)
- Scene duration < min_duration filtered
- Scene duration > max_duration filtered
- Scene duration = min_duration included
- Scene duration = max_duration included

### TestSplitNaming (10 tests)
- Output clips named clip_001.mp4, clip_002.mp4, etc.
- Overwrite warning when file exists
- Unique naming appends counter

### TestSplitExport (10 tests)
- VideoProcessor.write_clip called for each scene
- Exception in export catches and logs warning
- Skip corrupted clip, continue
- Progress bar updated

**Estimated test LOC**: 260

**Test execution**:
```bash
pytest tests/test_split.py -v
pytest tests/test_split.py --cov=src/drone_reel/cli -v  # Check coverage
```

---

## Step 10: Integration Test

**File**: `tests/test_split.py` (append to existing file)

**Test Class**: TestSplitIntegration

**Approach**:
1. Create synthetic video (CV2 VideoWriter, 5s, 1280x720, 30 FPS).
2. Add motion to 2-3 frames (create distinct "scenes").
3. Mock SceneDetector to return 2-3 scenes.
4. Mock VideoProcessor.write_clip to write dummy MP4.
5. Run `split` command with --input temp_video.mp4 --output temp_output/.
6. Assert: 2 clips written to disk with correct names.
7. Assert: output_dir exists with clip_001.mp4, clip_002.mp4.
8. Assert: clips have non-zero file sizes.

**Code skeleton**:
```python
def test_split_integration_end_to_end():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        
        # Create synthetic video
        synthetic_video = _make_synthetic_video(tmpdir / "raw.mp4")
        
        # Run split command
        runner = CliRunner()
        result = runner.invoke(main, [
            "split",
            "-i", str(synthetic_video),
            "-o", str(tmpdir / "output"),
            "--min-score", "50",
        ])
        
        # Assert success
        assert result.exit_code == 0
        
        # Assert clips exported
        clips = sorted((tmpdir / "output").glob("clip_*.mp4"))
        assert len(clips) >= 2
        assert all(c.stat().st_size > 0 for c in clips)
```

**Estimated LOC**: 80

---

## Step 11: CLI Integration & Documentation

**File**: `src/drone_reel/cli.py` (update main docstring, if needed)

**Tasks**:
1. Add `split` to command list in `main()` docstring.
2. Update CLAUDE.md build commands section with example:
   ```bash
   drone-reel split --input raw_footage.mp4 --output ./highlights/
   ```
3. Verify no import errors.

**Estimated LOC**: 10 (documentation)

**Test checkpoint**:
```bash
drone-reel --help  # Shows split command
drone-reel split --help  # Full help text
```

---

## Step 12: Coverage Check & Cleanup

**File**: `tests/test_split.py` + CI

**Tasks**:
1. Run full test suite: `pytest tests/test_split.py -v --cov=src/drone_reel/cli`.
2. Achieve **≥80% coverage** on new split code.
3. Fix any uncovered branches (mock edge cases).
4. Run linting: `ruff check src/drone_reel/cli.py` + `black --check src/drone_reel/cli.py`.
5. Run full pytest suite to ensure no regressions: `pytest -x`.

**Expected output**:
```
tests/test_split.py::TestSplitValidation::... PASSED
tests/test_split.py::TestSplitDetection::... PASSED
...
======================== 130 passed in 12s =========================
coverage: 80%+ on cli.py::split
```

---

## Timeline & Dependencies

### Dependency Graph
```
Step 1 (CLI skeleton)
  ↓
Step 2 (Validation) ← Can start tests
  ↓
Step 3 (Detection) ← Depends on Step 2 validation
  ↓
Step 4 (Filtering) ← Depends on Step 3 detection
  ↓
Step 5 (Duration filtering) ← Depends on Step 4
  ↓
Step 6 (Naming) ← Depends on Step 5
  ↓
Step 7 (Export) ← Depends on Step 6
  ↓
Step 8 (Reporting) ← Depends on Step 7
  ↓
Step 9 (Unit tests) ← Can run in parallel once each step completes
  ↓
Step 10 (Integration test)
  ↓
Step 11 (CLI docs)
  ↓
Step 12 (Coverage check)
```

### Sequential Phases
- **Phase A** (Steps 1-8): Implementation, ~3-4 hours (dev + manual testing).
- **Phase B** (Steps 9-10): Testing, ~2-3 hours (unit + integration).
- **Phase C** (Steps 11-12): Polish + cleanup, ~1 hour.

**Total estimate: 6-8 hours** (includes debugging, code review, rework).

---

## What to Test at Each Checkpoint

| Step | Test | Command | Pass Criteria |
|------|------|---------|---------------|
| 1 | CLI loads | `drone-reel split --help` | Help text appears |
| 2 | Validation | `pytest tests/test_split.py::TestSplitValidation -v` | All 30 tests pass |
| 3 | Detection | `pytest tests/test_split.py::TestSplitDetection -v` | All 15 tests pass |
| 4 | Filtering | `pytest tests/test_split.py::TestSplitFiltering -v` | All 20 tests pass |
| 5 | Duration | `pytest tests/test_split.py::TestSplitDuration -v` | All 15 tests pass |
| 6 | Naming | `pytest tests/test_split.py::TestSplitNaming -v` | All 10 tests pass |
| 7 | Export | `pytest tests/test_split.py::TestSplitExport -v` | All 10 tests pass |
| 8 | Reporting | Manual run with test video | Output text correct |
| 9 | Unit coverage | `pytest tests/test_split.py --cov=src/drone_reel/cli -v` | ≥80% coverage |
| 10 | Integration | `pytest tests/test_split.py::TestSplitIntegration -v` | End-to-end works |
| 11 | Docs | `drone-reel split --help` | Help updated |
| 12 | Regression | `pytest -x` | All 1100+ tests still pass |

---

## Estimated LOC Summary

| Component | LOC | Notes |
|-----------|-----|-------|
| CLI command (Steps 1-8) | 185 | Decorators (30) + validation (40) + detection (20) + filtering (35) + duration (10) + naming (15) + export (35) + reporting (20) |
| Unit tests (Step 9) | 260 | 90 test functions across 6 classes |
| Integration test (Step 10) | 80 | 1 end-to-end test + helper |
| Documentation (Step 11) | 10 | Docstrings, CLAUDE.md update |
| **Total** | **535** | |

**Files changed:**
- `src/drone_reel/cli.py` — +185 lines (add split command after extract_clips)
- `tests/test_split.py` — +340 lines (create new file)
- `CLAUDE.md` — +5 lines (update build commands section)

---

## Success Criteria

✅ Command loads and responds to `--help`.
✅ All parameter validation tests pass (min_duration < max_duration, etc.).
✅ Scene detection integrates with existing SceneDetector.
✅ Filtering applies thresholds correctly.
✅ Clips exported with correct naming (clip_001.mp4, etc.).
✅ Export loop handles per-clip exceptions gracefully.
✅ Progress bar shows during export.
✅ Final report displays summary (clips exported, total size, location).
✅ ≥80% coverage on `split()` code.
✅ Integration test passes (end-to-end with synthetic video).
✅ All 1100+ existing tests still pass (no regressions).
✅ Linting passes (ruff, black).
✅ Help text is clear and discoverable.

---

## Post-MVP Roadmap

**Phase 2 features (not in this plan):**
- `--preview` flag: Generate JPG thumbnails for each clip.
- `--merge-proximity 5s`: Merge scenes closer than N seconds.
- `--json-metadata`: Export scene metadata as JSON.

**Phase 3 features (exploratory):**
- ML-based ranking (supplement motion/brightness scores with learned importance).
- Audio peak sync (detect audio peaks in raw file for music-less ranking).

