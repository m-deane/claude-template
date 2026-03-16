# Extract-Clips Code Path Analysis

**Date**: 2026-03-03  
**Objective**: Analyze the existing `extract_clips` CLI command to understand architecture, identify unnecessary overhead, memory profile, and scoring mechanisms.

---

## 1. Code Path Trace: CLI Entry → Output

### 1.1 Entry Point: `extract_clips()` Command
**Location**: `src/drone_reel/cli.py:1283-1752`

**CLI Parameters**:
```python
--input/-i          # Video file or directory
--output-dir/-o     # Extraction output directory (default: ./clips)
--count/-n          # Max clips (1-100, default: 10)
--min-score         # Min scene score threshold (0-100, default: 30.0)
--min-duration      # Min clip duration (0.5-300s, default: 2.0s)
--max-duration      # Max clip duration (1.0-300s, default: 10.0s)
--quality/-q        # Output quality (low/medium/high/ultra)
--resolution        # Output resolution (source/hd/2k/4k)
--sort/-s           # Sort order (score/chronological/duration)
--no-filter         # Skip quality filtering
--enhanced          # Run enhanced analysis (subject detection)
--json              # Write manifest.json with metadata
--overwrite         # Overwrite existing files
```

### 1.2 Validation Phase
1. **Parameter validation**: `min_duration < max_duration`
2. **Input path resolution**: File vs. directory → `find_video_files()`
3. **Video format check**: Uses `VIDEO_EXTENSIONS` list
4. **Output directory check**: Ensures writable directory, creates if needed
5. **Quality/resolution presets**: Maps to bitrate strings
6. **Resource preflight check**: `preflight_check()` validates memory + disk before processing

### 1.3 Scene Detection Phase
**Location**: Lines 1428-1444

```python
scene_detector = SceneDetector()
all_scenes = []

for video_path in video_files:
    if enhanced:
        scenes = scene_detector.detect_scenes_enhanced(video_path)
    else:
        scenes = scene_detector.detect_scenes(video_path)
    all_scenes.extend(scenes)
```

**Two paths**:
- **Normal path** (`detect_scenes`):
  - Uses PySceneDetect's ContentDetector with configurable threshold (default 27.0)
  - Returns `SceneInfo` objects with basic: `start_time`, `end_time`, `duration`, `score`, `source_file`
  - Score computed via `_score_scene()` (see Section 5)

- **Enhanced path** (`detect_scenes_enhanced`):
  - Wraps `detect_scenes()` then enriches each scene with:
    - `motion_type`: Classified via optical flow
    - `motion_energy`: Scalar 0-100
    - `motion_direction`: (dx, dy) tuple
    - `motion_smoothness`: Flow consistency
    - `subject_score`: Subject detection 0-100
    - `hook_potential`: Overall hook quality 0-100
    - `hook_tier`: Categorical (MAXIMUM/HIGH/MEDIUM/LOW/POOR)
    - `dominant_colors`, `is_golden_hour`, `depth_score`
  - Returns `EnhancedSceneInfo` (extends `SceneInfo`)

### 1.4 Motion Analysis Phase
**Location**: Lines 1446-1451

```python
analysis = analyze_scenes_batch(all_scenes, include_sharpness=True)
motion_map = {id(s): analysis[id(s)]["motion_energy"] for s in all_scenes}
brightness_map = {id(s): analysis[id(s)]["brightness"] for s in all_scenes}
shake_map = {id(s): analysis[id(s)]["shake_score"] for s in all_scenes}
```

**`analyze_scenes_batch()` function** (parallel or sequential):
- **Parallel**: Uses ThreadPoolExecutor (max_workers = `min(4, cpu_count)`)
- **Per-scene analysis** via `_analyze_single_scene()`:
  - Opens cv2.VideoCapture independently per scene
  - Samples frames at 2/second over the scene duration
  - Computes:
    - `motion_energy`: Optical flow magnitude across sampled frames
    - `brightness`: Mean pixel brightness (0-255)
    - `shake_score`: Frame-to-frame variance in motion (0-100 scale)
    - `motion_type`: via `classify_motion_type()`
    - `motion_direction`: Flow vector avg
    - `sharpness`: Laplacian variance (only if `include_sharpness=True`)
  - Returns dict keyed by `id(scene)`

### 1.5 Filtering Phase
**Location**: Lines 1453-1465

**Option A: `--no-filter`**
```python
if no_filter:
    candidates = list(all_scenes)
    scenes_filtered = 0
    dark_filtered = 0
    shaky_filtered = 0
```
Bypasses all filtering, passes all scenes.

**Option B: Normal filtering**
```python
sf = SceneFilter()
result = sf.filter_scenes(all_scenes, motion_map, brightness_map, shake_map)
candidates = result.all_passing
```

**SceneFilter logic**:
- Filters by brightness: `min_brightness` (30) ≤ brightness ≤ `max_brightness` (245)
- Filters by shake: `shake_score > max_shake_score` (40) → rejected
- Tiers remaining scenes:
  - **high_subject**: Has `subject_score >= 0.6`
  - **high_motion**: No subject, but `motion_energy >= 45.0`
  - **medium_motion**: No subject, `motion_energy >= 25.0`
  - **low_motion**: No subject, `motion_energy < 25.0`
- Returns `FilterResult` with all tiers accessible via:
  - `.all_passing`: Concatenates high_subject + high_motion + medium_motion + low_motion
  - `.prioritized`: Omits low_motion

### 1.6 Score & Duration Thresholding
**Location**: Lines 1467-1470

```python
candidates = [s for s in candidates if s.score >= min_score]
candidates = [s for s in candidates if s.duration >= min_duration]
```

Applies CLI-specified `--min-score` (default 30) and `--min-duration` (default 2.0s) filters.

### 1.7 Sorting & Selection
**Location**: Lines 1487-1495

```python
if sort == "score":
    candidates.sort(key=lambda s: s.score, reverse=True)
elif sort == "chronological":
    candidates.sort(key=lambda s: (str(s.source_file), s.start_time))
elif sort == "duration":
    candidates.sort(key=lambda s: s.duration, reverse=True)

selected = candidates[:count]  # Limit to --count (default 10)
```

### 1.8 Clip Extraction & Write Phase
**Location**: Lines 1499-1680

```python
processor = VideoProcessor(
    output_fps=30,
    video_bitrate=video_bitrate,
    audio_bitrate=audio_bitrate,
)

for i, scene in enumerate(selected):
    segment = ClipSegment(scene=scene, start_offset=0.0, duration=clip_duration)
    clip = processor.extract_clip(segment)
    
    if resolution != "source":
        # Resize to target height (hd/2k/4k)
        clip = clip.resized((target_width, target_height))
    
    processor.write_clip(clip, output_file)
```

**`VideoProcessor.extract_clip()` flow**:
1. Opens `VideoFileClip(segment.scene.source_file)`
2. Subclips to `[segment.effective_start, segment.effective_end)`
3. Optional resize via `.resized()` (if resolution != "source")
4. Stores reference in `clip._source_clip_ref` to keep source open
5. Returns subclip

**`VideoProcessor.write_clip()` flow**:
1. Calls `clip.write_videofile()` with:
   - `fps=30`
   - `codec="libx264"` (H.264)
   - `audio_codec="aac"`
   - **FFmpeg params** (BT.709 + faststart + VBV):
     ```
     -pix_fmt yuv420p
     -colorspace bt709
     -color_primaries bt709
     -color_trc bt709
     -movflags +faststart
     -maxrate (1.5x video_bitrate)
     -bufsize (2x video_bitrate)
     ```

### 1.9 Manifest & Summary
**Location**: Lines 1682-1729

- Collects metadata per clip: filename, source, times, duration, score, motion_type, hook_tier, golden_hour flag
- Writes optional `manifest.json` with:
  - `version`, `source_files`, `extraction_params`, `clips[]`, `summary`
  - Summary includes: total_clips, total_duration, total_size_mb, avg_score, scenes_detected, scenes_filtered

---

## 2. Unnecessary Overhead: What extract-clips Does That "Split into Highlights" Doesn't Need

### 2.1 Heavy Processing Overhead

| Component | What | Why For extract-clips | Why NOT Needed For split |
|-----------|------|----------------------|--------------------------|
| **SceneDetector._score_scene()** | Weighted 5-factor scoring (motion 30%, composition 20%, color 20%, sharpness 15%, brightness 15%) | Precise ranking for top-N selection | Just detecting boundaries; coarse tier is enough |
| **Optical Flow Computation** | Farneback optical flow per frame pair during scoring | Hook detection, subject tracking | Not needed; just frame boundaries |
| **Subject Detection** (`_calculate_subject_score()`) | Edge detection + correlation for face/subject blobs | Enhanced ranking for hook potential | Not needed for simple split |
| **Composition Scoring** (Rule of thirds, horizon, leading lines) | Evaluates frame geometry quality | Ranking high-quality scenes | Not needed; accept all valid boundaries |
| **Color Variance & Analysis** | HSV histograms, dominant color extraction | Visual interest ranking | Not needed; just structural detection |
| **Brightness/Darkness Filtering** | Filters scenes outside 30-245 brightness range | Avoid dark/blown-out clips | Not needed for split (user can clip dark footage if they want) |
| **Shake Detection** | Frame-to-frame motion variance scoring | Penalizes shaky/unstable footage | Not needed for split |
| **Motion Energy Filtering** | Tiers scenes by motion activity (ideal 45+, min 25) | Prefers dynamic content | Not needed for split (user accepts what's there) |
| **Enhanced Analysis Mode** | Re-analyzes scenes with golden hour, depth score, hook tier | Premium ranking when user requests `--enhanced` | Not needed |

### 2.2 I/O Overhead

| Component | Cost | Why For extract-clips | Why NOT Needed |
|-----------|------|----------------------|-----------------|
| **Multiple cv2.VideoCapture opens** | ~0.1-0.5s per open | `_score_scene()` opens file for each scene; `analyze_scenes_batch()` opens again per scene | Could open once, seek within |
| **Frame sampling during scoring** | ~10-20 sampled frames per scene @ 2/sec | Precise metric computation | One sample per scene (start frame) would suffice |
| **Manifest JSON write** | ~10-50ms | Optional via `--json` flag | Not relevant for split |

### 2.3 CLI Feature Overhead

| Feature | Impact | For extract-clips | For split |
|---------|--------|-------------------|-----------|
| **Quality/resolution presets** | Bitrate mapping table | Yes (output encoding) | Yes (same output encoding) |
| **Sort modes** (score/chrono/duration) | Sorting logic | Yes (ranking for top-N) | No (output in scene order) |
| **Resource preflight checks** | Memory/disk validation | Yes (expensive render) | Yes (same) |

### 2.4 Summary: Overhead Breakdown

**For a typical 60-second 4K video with ~10 detected scenes:**
- `_score_scene()` per scene: ~0.5s (10 frames × optical flow + composition)
- `analyze_scenes_batch()` per scene: ~0.3s (frame sampling, shake, motion type)
- **Total overhead per scene**: ~0.8s
- **Total for 10 scenes**: ~8 seconds of pure analysis overhead

**For "split into highlights" needs:**
- Scene boundary detection (PySceneDetect): ~1-2 seconds (unavoidable)
- One-pass frame analysis (brightness, motion tier): ~0.5s total
- **Total expected**: ~2 seconds (vs. 10 for extract-clips)

---

## 3. Memory Profile for 1 GB 4K File

### 3.1 SceneDetector Phase (Streaming)

**`detect_scenes()` memory**:
- PySceneDetect ContentDetector: Streams frames via cv2.VideoCapture
- **Peak per frame**: ~50 MB (4K frame @ 3 channels)
- **Holds**: 1 frame in memory at a time during ContentDetector analysis
- **Total SceneDetector peak**: ~100-150 MB (frame + detector state)

**`_score_scene()` during scoring**:
- Opens cv2.VideoCapture: ~10 MB (file handles)
- Samples ~10-20 frames per 5-10s scene
- Keeps 2 frames in memory: current + previous (grayscale)
- **Per-scene peak**: ~100-150 MB (2 color frames + gray conversions)
- **File size**: 1 GB input, ~10 scenes → per-scene: ~100 MB
- Closes file after scoring

**Total SceneDetector phase peak**: ~150-200 MB (one scene being scored at a time)

### 3.2 Motion Analysis Phase (Parallel ThreadPoolExecutor)

**`analyze_scenes_batch()` with `max_workers=min(4, cpu_count)`**:
- If `cpu_count >= 4`: Up to 4 scenes analyzed concurrently
- Each thread independently opens cv2.VideoCapture
- Per-thread memory: ~100-150 MB (same as _score_scene)
- **Peak with 4 workers**: 4 × 150 MB = **~600 MB**

**Breakdown per worker**:
- cv2.VideoCapture: 10 MB
- Frame buffers (2 frames): 100 MB
- Optical flow matrices (Farneback): 10-20 MB
- numpy arrays for motion stats: 5 MB
- **Per-worker total**: ~125-145 MB

### 3.3 MoviePy VideoFileClip (Lazy Decode)

**`VideoFileClip()` itself**:
- **Does NOT pre-load frames** to memory
- Only reads codec metadata + opens FFmpeg pipe
- **Memory footprint**: ~5-10 MB per clip reference (metadata, file handle)

**`extract_clip()` + `.resized()`**:
- `subclipped()`: Does not materialize frames; creates view
- `.resized()`: Still lazy; creates filter graph
- **Still no frame materialization until write_videofile**

### 3.4 Encoding Phase (write_videofile)

**`VideoProcessor.write_clip()` behavior**:
- FFmpeg subprocess is launched with pipe I/O
- MoviePy fetches frames on-demand via `get_frame(t)`
- **Encoding buffer**: ~2-4 frames buffered in FFmpeg
- **Peak during encode**: ~200-300 MB (codec buffers + frame pipeline)

**Single sequential write** (extract-clips uses loop):
- Processes one clip at a time
- Closes previous clip before opening next
- **Peak**: ~300 MB per clip write
- **No accumulation**: Old clips garbage-collected between iterations

### 3.5 Full Pipeline Peak Memory Estimate

| Phase | Peak Memory | Notes |
|-------|------------|-------|
| Scene detection (PySceneDetect) | 100-150 MB | Streaming, 1 frame at a time |
| Scoring (_score_scene) | 100-150 MB | One scene at a time |
| Batch analysis (4 workers) | 600 MB | 4 concurrent scene analyses |
| Clip extraction (MoviePy) | 50 MB | Lazy, no frame materialization |
| Encoding write_clip | 200-300 MB | FFmpeg encoding pipeline |
| **Total worst-case** | **~900 MB** | All phases sequential |

**Actual typical run**:
- Scene detection: 150 MB
- Batch analysis peaks at 600 MB (4 workers)
- Then sequential writes: 300 MB each (garbage collected between)
- **Typical peak**: ~600 MB during parallel analysis phase

### 3.6 Why No Stabilizer Frame Cache

**Historical context**: Early versions cached all frames for stabilizer
- 4K @ 30fps × 30s = 900 frames × 50 MB = **45 GB**
- Phase 8 removed caching; now streams on-demand: **~150 MB peak per clip**

---

## 4. Flag Behavior

### 4.1 `--no-filter` Flag

**What it does** (line 1456):
```python
if no_filter:
    candidates = list(all_scenes)
    scenes_filtered = 0
    dark_filtered = 0
    shaky_filtered = 0
else:
    sf = SceneFilter()
    result = sf.filter_scenes(all_scenes, motion_map, brightness_map, shake_map)
    candidates = result.all_passing
```

**Effect**:
- **Skips** `SceneFilter.filter_scenes()` entirely
- **Includes** all detected scenes, regardless of:
  - Brightness (no 30-245 range check)
  - Shake score (no stability check)
  - Motion energy (no tier filtering)
- Still applies `--min-score` and `--min-duration` thresholds
- **Use case**: User wants to override filters because they disagree with quality judgment

**Overhead saved**: ~0.1s (filter check logic), not significant

### 4.2 `--enhanced` Flag

**What it does** (lines 1437-1441):
```python
if enhanced:
    scenes = scene_detector.detect_scenes_enhanced(video_path)
else:
    scenes = scene_detector.detect_scenes(video_path)
```

**`detect_scenes_enhanced()` additions**:
- Re-analyzes each scene after boundary detection
- Computes per-scene:
  - `motion_type`: Farneback optical flow classification
  - `subject_score`: Face/blob detection (0-100)
  - `hook_potential`: Composite (subject + motion + color + composition)
  - `hook_tier`: AUTO-ASSIGNED from hook_potential:
    - `>= 80` → MAXIMUM
    - `>= 65` → HIGH
    - `>= 45` → MEDIUM
    - `>= 25` → LOW
    - `< 25` → POOR
  - `motion_energy`, `motion_smoothness`, `dominant_colors`, `depth_score`, `is_golden_hour`

**Overhead**: ~1-2s per scene (adds Farneback + subject detection)
- For 10 scenes: ~10-20s additional

**Use case**: Better ranking for highlight selection; user wants AI-powered quality judgment

**Returned object**: `EnhancedSceneInfo` (not `SceneInfo`)

### 4.3 `--json` Flag

**What it does** (line 1724):
```python
if write_json and manifest_clips:
    manifest = {...}
    manifest_path = output_dir / "manifest.json"
    with open(manifest_path, "w") as f:
        json_module.dump(manifest, f, indent=2)
```

**Output**: `manifest.json` with:
- Source files list
- Extraction parameters used
- Per-clip metadata: filename, times, duration, score, motion_type, hook_tier, golden_hour
- Summary: total clips, duration, size, avg score, scenes detected/filtered

**Overhead**: ~10-50ms (JSON serialization)

**Use case**: Downstream processing (NLE import, filtering, automation)

---

## 5. Scoring Formula: The Exact Mechanics

### 5.1 Basic Scoring (`_score_scene()` - Used for extract-clips without --enhanced)

**Called during**: `detect_scenes()` for each detected scene

**Inputs**:
- `video_path`, `start` (seconds), `end` (seconds)

**Sampling strategy**:
- Samples 2 frames per second, minimum 10 frames
- Duration: 5s video → 10 sampled frames at even intervals

**Per-frame metrics computed**:

| Metric | Function | Scale | Definition |
|--------|----------|-------|-----------|
| **Sharpness** | `_calculate_sharpness()` | 0-100 | Laplacian variance (edge content) |
| **Color Variance** | `_calculate_color_variance()` | 0-100 | HSV histogram spread; saturation richness |
| **Brightness Balance** | `_calculate_brightness_balance()` | 0-100 | Penalizes too dark (<50) or too bright (>200); peaks at 100-180 range |
| **Composition Score** | `_calculate_composition()` | 0-100 | Combination of: rule of thirds, horizon level, leading lines |
| **Motion Score** | `_calculate_motion_optical_flow()` | 0-100 | Farneback optical flow magnitude; first frame = neutral 50 |

**Weighting**:
```python
frame_score = (
    motion_score * 0.30              # 30% - Camera movement intensity
    + composition_score * 0.20       # 20% - Framing quality
    + color_score * 0.20             # 20% - Color richness
    + sharpness * 0.15               # 15% - Focus clarity
    + brightness_score * 0.15        # 15% - Exposure balance
)
```

**Aggregation**:
```python
overall_score = 0.6 * max(frame_scores) + 0.4 * mean(frame_scores)
```

**Interpretation**:
- Favors **peaks** (60% weight on max) over average
- Rewards scenes with at least one "standout" moment
- Lower bound: 0.0 (all frames terrible)
- Upper bound: 100.0 (all frames perfect)
- Typical range: 20-80

### 5.2 Enhanced Scoring (`detect_scenes_enhanced()` with --enhanced)

**Called when**: User specifies `--enhanced` flag

**Additional per-frame metrics**:

| Metric | Function | Scale | Definition |
|--------|----------|-------|-----------|
| **Subject Score** | `_calculate_subject_score()` | 0-100 | Blob/face detection via edge detection; higher = clear subject |
| **Hook Potential** | `_calculate_hook_potential()` | 0-100 | Composite scoring: `subject*0.4 + motion*0.3 + color*0.15 + composition*0.15` |
| **Visual Density** | Part of subject score | 0-100 | Concentration of detected edges/objects |
| **Motion Energy** | Derived from optical flow | 0-100 | Magnitude of motion vectors (same as motion_score) |
| **Motion Smoothness** | `calculate_motion_smoothness()` | 0-1 | Consistency of flow across frames (variance-based) |
| **Depth Score** | `calculate_depth_score()` | 0-100 | Edge abundance as proxy for layering |
| **Golden Hour** | `detect_golden_hour()` | Bool | Warm color tones; HSV H in 10-40° range |
| **Dominant Colors** | `extract_dominant_colors()` | List[RGB] | K-means clustering on image (k=3-5) |

**New weighting** (used in `score_scene_with_hook_potential()`):
```python
frame_score = (
    subject_score * 0.25             # 25% - Subject clarity (UP from 0%)
    + motion_score * 0.25            # 25% - Camera movement (DOWN from 30%)
    + composition_score * 0.15       # 15% - Framing (same)
    + color_score * 0.15             # 15% - Color (same)
    + sharpness * 0.10               # 10% - Focus (DOWN from 15%)
    + brightness_score * 0.10        # 10% - Exposure (DOWN from 15%)
)
```

**Aggregation** (same as basic):
```python
overall_score = 0.6 * max(frame_scores) + 0.4 * mean(frame_scores)
```

**Hook Tier Assignment** (from `hook_potential` average):
```python
if avg_hook >= 80: tier = HookPotential.MAXIMUM
elif avg_hook >= 65: tier = HookPotential.HIGH
elif avg_hook >= 45: tier = HookPotential.MEDIUM
elif avg_hook >= 25: tier = HookPotential.LOW
else: tier = HookPotential.POOR
```

### 5.3 Scene Information Data Structures

**`SceneInfo` (basic)**:
```python
@dataclass
class SceneInfo:
    start_time: float              # Seconds
    end_time: float                # Seconds
    duration: float                # = end - start
    score: float                   # 0-100, from _score_scene()
    source_file: Path              # Video file path
    thumbnail: Optional[np.ndarray] # Optional frame capture
```

**`EnhancedSceneInfo` (extended, inherits SceneInfo)**:
```python
@dataclass
class EnhancedSceneInfo(SceneInfo):
    motion_type: MotionType         # UNKNOWN, STATIC, PAN_LEFT/RIGHT, TILT_UP/DOWN, etc.
    motion_direction: tuple[float, float]  # (avg_dx, avg_dy) from optical flow
    motion_smoothness: float        # 0-1, consistency of motion
    motion_energy: float            # 0-100, intensity of movement
    dominant_colors: list[tuple[int,int,int]]  # RGB tuples
    color_variance: float           # 0-100, spread in color distribution
    is_golden_hour: bool            # Warm-tone detection
    depth_score: float              # 0-100, edge abundance (layering)
    subject_score: float            # 0-100, blob/face clarity
    hook_potential: float           # 0-100, composite hook quality
    hook_tier: HookPotential        # MAXIMUM/HIGH/MEDIUM/LOW/POOR
    visual_interest_density: float  # 0-100, concentration of interest points
```

### 5.4 Key Insight: What Makes a Good Highlight?

**For drone footage specifically:**
1. **Motion (25-30%)**: Drones shine when moving; static = boring
   - Optical flow magnitude rewards smooth pans, orbits, reveal shots
2. **Subject Clarity (25%)**: Clear subject beats abstract scenery
   - Blob/edge detection identifies landscapes, buildings, people
3. **Composition (15%)**: Rule of thirds, horizon level, leading lines
   - Prevents compositions that feel "off" or unbalanced
4. **Color (15%)**: Saturation and warmth add visual interest
   - Golden hour scenes score higher; overexposed/desaturated lower
5. **Sharpness (10%)**: Focus clarity; soft = less engaging
   - Laplacian variance penalizes blur
6. **Brightness (10%)**: Exposure balance; avoid too dark/bright
   - Range 30-245 preferred; peaks around 100-180

### 5.5 Filtering Thresholds (After Scoring)

**SceneFilter tier cutoffs**:
```python
@dataclass
class FilterThresholds:
    min_motion_energy: float = 25.0         # Below this = low_motion tier
    ideal_motion_energy: float = 45.0       # At/above this = high_motion tier
    min_brightness: float = 30.0            # Below = filtered out
    max_brightness: float = 245.0           # Above = filtered out
    max_shake_score: float = 40.0           # Above = filtered out (unstable)
    subject_score_threshold: float = 0.6    # Score/100; above = high_subject tier
```

**Filtering decision tree**:
```
for each scene:
    if brightness < 30 or brightness > 245:
        → FILTERED (too dark or blown out)
    elif shake_score > 40:
        → FILTERED (too shaky/unstable)
    elif subject_score >= 60:
        → high_subject tier (prefers this)
    elif motion_energy >= 45:
        → high_motion tier
    elif motion_energy >= 25:
        → medium_motion tier
    else:
        → low_motion tier

return FilterResult:
    .prioritized = high_subject + high_motion + medium_motion
    .all_passing = prioritized + low_motion
```

**Practical effect**:
- Drone footage with **clear subjects + good motion + proper exposure** scores highest
- Scoring is **relative**; scene ranking depends on other scenes in the video
- Filtering is **pass/fail thresholds**; scenes below min_brightness are rejected outright

---

## 6. MotionType Classification (`classify_motion_type()`)

**Input**: Optical flow vectors `[(dx, dy), ...]` + motion_energy

**Output**: `(MotionType, (avg_dx, avg_dy))`

**Classification logic**:

| Condition | Result | Notes |
|-----------|--------|-------|
| `motion_energy < 10` | `STATIC` | Almost no movement |
| `magnitude < 0.5` | `STATIC` | Flow too small |
| `consistency < 0.15` & `motion_energy > 40` | `FPV` | Chaotic, high-energy → First-person |
| Frequent direction reversals | `ORBIT_CW/CCW` or `REVEAL` | Rotational motion pattern |
| `\|avg_dx\| > \|avg_dy\| * 1.5` | `PAN_LEFT/RIGHT` | Horizontal dominance |
| `\|avg_dy\| > \|avg_dx\| * 1.5` & `avg_dy > 0` | `TILT_DOWN` | Downward dominance |
| `\|avg_dy\| > \|avg_dx\| * 1.5` & `avg_dy < 0` | `TILT_UP` | Upward dominance |
| `avg_dy > 0` & `motion_energy > 30` | `FLYOVER` | Forward + downward |
| `avg_dy < 0` & `motion_energy > 25` | `APPROACH` | Forward + upward |
| Default | `UNKNOWN` | Balanced/mixed motion |

---

## 7. Analysis Phase Data Flow Diagram

```
Input Video (1 GB, 4K)
    ↓
[Scene Detection via PySceneDetect]
    ├─ Streams frames via cv2.VideoCapture
    ├─ ContentDetector finds boundaries
    ├─ Returns: list[SceneInfo] with times
    └─ Memory: ~150 MB (streaming)

    ↓
[Score each scene via _score_scene()]
    ├─ Opens cv2.VideoCapture per scene
    ├─ Samples 2 fps (10-20 frames per scene)
    ├─ Computes: sharpness, color, brightness, composition, motion
    ├─ Aggregates: 60% max + 40% mean
    ├─ Closes file
    └─ Memory: ~150 MB peak per scene

    ↓
[Batch Motion Analysis (Parallel)]
    ├─ ThreadPoolExecutor with 4 workers
    ├─ Each worker: _analyze_single_scene()
    ├─ Computes: motion_energy, brightness, shake_score, motion_type
    ├─ Max 4 concurrent: 4 × 150 MB = 600 MB peak
    └─ Returns: dict[id(scene)] → {motion_energy, brightness, shake_score, ...}

    ├─ [IF enhanced=True]
    │   └─ Re-analyze with subject_score, hook_potential, hook_tier
    │       └─ Additional cost: Farneback + blob detection
    │
    ↓
[Filter via SceneFilter]
    ├─ Input: all_scenes, motion_map, brightness_map, shake_map
    ├─ Apply thresholds: brightness, shake, motion_energy
    ├─ Tier into: high_subject, high_motion, medium_motion, low_motion
    └─ Output: FilterResult with all_passing list

    ↓
[Apply Min-Score & Min-Duration]
    ├─ Candidates = [s for s in candidates if s.score >= min_score]
    ├─ Candidates = [s for s in candidates if s.duration >= min_duration]
    └─ Count: typically 30-50% pass

    ↓
[Sort & Select]
    ├─ Sort by: score (desc) or chronological or duration (desc)
    └─ Select top N (--count, default 10)

    ↓
[Extract & Encode per Clip]
    ├─ For each selected scene:
    │   ├─ VideoProcessor.extract_clip(segment)
    │   ├─ Lazy VideoFileClip + subclip
    │   ├─ Optional resize
    │   ├─ VideoProcessor.write_clip() → ffmpeg encode
    │   └─ Memory: 200-300 MB peak per write
    │
    ↓
[Write Manifest.json (optional)]
    └─ JSON output with scene metadata
```

---

## 8. Summary: What's Essential vs. Overhead

### Essential for extract-clips:
1. ✓ Scene boundary detection (PySceneDetect) → unavoidable
2. ✓ Basic scoring (to rank top-N) → required
3. ✓ Filtering (brightness, shake) → optional but recommended
4. ✓ Encoding (write_clip) → obviously required

### Optional/Nice-to-have:
- ✓ Enhanced analysis (subject detection, hook tier) → user controls via `--enhanced`
- ✓ Motion type classification → only used in enhanced mode
- ✓ Manifest JSON → user controls via `--json`

### NOT needed for "split into highlights" (pure scene splitting):
- ✗ Detailed scoring (motion 30%, composition 20%, color 20%, ...) → just need coarse tiers
- ✗ Subject detection → not needed for structural splitting
- ✗ Shake filtering → accept all scenes, let user decide
- ✗ Motion energy filtering → accept all scenes
- ✗ Composition scoring → not needed
- ✗ Optional manifest output → split just outputs files

### Memory bottlenecks:
1. **Parallel motion analysis**: 4 workers × 150 MB = 600 MB peak (unavoidable if parallel)
2. **Sequential encoding**: 300 MB per clip (manageable, garbage collected between)

### Speed bottlenecks:
1. **Scene scoring** (`_score_scene`): ~0.5s per scene (optical flow + composition)
2. **Batch analysis**: ~0.3s per scene (motion classification)
3. **Encoding**: Varies by resolution/bitrate, typically 2-5s per 10s clip

---

## 9. Conclusion for Highlight Splitter Design

**Key insights for a lightweight "split" command**:

1. **Reuse boundary detection** from SceneDetector, but skip `_score_scene()`
2. **Lightweight motion analysis**: One-pass frame analysis (brightness, motion_energy tier only)
3. **No subject detection**: Not needed for structural splitting
4. **No filtering by motion**: Accept all detected scenes; user decides if they want filtering
5. **Streaming I/O**: Open video once per file, seek within for clip extraction
6. **Sequential encoding**: Process one clip at a time to cap memory at ~300 MB
7. **Output manifest**: Optional; similar format to extract-clips for consistency

**Estimated overhead vs. extract-clips**:
- **extract-clips**: 10-20 seconds for typical 60s video + 10 scenes
- **split command**: 2-5 seconds (scene detection only, no scoring)
- **Memory**: extract-clips peaks at 600 MB (parallel analysis), split can stay < 200 MB (sequential)

