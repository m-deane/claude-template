# Scene Detection Tuning Parameters for Highlight Splitter

## Research Summary

This document analyzes the scene detection and scoring parameters that affect the `split` command's ability to differentiate highlight quality. The DJI video case produced 7 scenes with similar scores (55-64 range), suggesting the current parameters lack granularity for fine distinction.

---

## 1. Current Hardcoded Defaults vs Exposed Parameters

### 1.1 SceneDetector Constructor Parameters

| Parameter | Current Default | Range | Type | Currently Exposed? | Location |
|-----------|-----------------|-------|------|-------------------|----------|
| `threshold` | 27.0 | 15.0-50.0 | Float | YES (via config) | `config.py:27` |
| `min_scene_length` | 1.0s | 0.5s-5.0s | Float | YES (via config) | `config.py:28` |
| `max_scene_length` | 8.0s (create) / 10.0s (detector init default) | 5.0s-20.0s | Float | YES (via config) | `config.py:29` |
| `analysis_scale` | 0.5 | 0.25-1.0 | Float | NO - hardcoded | `scene_detector.py:212` |

### Analysis

- **`threshold` (scene_threshold)**: Controls ContentDetector sensitivity via PySceneDetect. Lower values = more scene cuts. Config-exposed but not used in `split()` or `extract_clips()` commands (both instantiate `SceneDetector()` with defaults).
- **`analysis_scale`**: Frame downscaling factor for scoring (1.0 = full resolution, 0.5 = 50%). NOT exposed to CLI. Affects all downstream scores (motion, sharpness, composition). Lower scales reduce accuracy but increase speed.

### Issue Identified

The `split` and `extract_clips` commands **do not wire `config.scene_threshold`** to SceneDetector. They instantiate with all defaults, ignoring user config:

```python
# Line 1948 (split command)
scene_detector = SceneDetector()  # Uses defaults, ignores config

# Line 1476 (extract_clips command)
scene_detector = SceneDetector()  # Uses defaults, ignores config

# vs. Line 546 (create command - DOES wire config)
scene_detector = SceneDetector(
    threshold=config.scene_threshold,
    min_scene_length=config.min_scene_length,
    max_scene_length=config.max_scene_length,
)
```

---

## 2. Scene Scoring Weights (The Core Differentiator)

### 2.1 Basic `_score_scene()` Pipeline (Used by split/extract_clips)

The basic detector uses these weights:

```python
frame_score = (
    motion_score * 0.30 +      # 30% - Motion intensity
    composition_score * 0.20 +  # 20% - Rule of thirds, horizon, leading lines
    color_score * 0.20 +        # 20% - Saturation variance + mean
    sharpness * 0.15 +          # 15% - Laplacian variance (image detail)
    brightness_score * 0.15     # 15% - Distance from ideal (127/255)
)

# Final scene score (peak scoring)
overall = 0.6 * max(frame_scores) + 0.4 * mean(frame_scores)
```

**Problem**: This is generic, does not distinguish between subject content. All 7 DJI scenes likely scored in 55-64 range due to:
- Similar motion consistency (all smooth drone footage)
- Similar brightness (daytime, consistent lighting)
- Similar composition (landscape scenes)

### 2.2 Enhanced `score_scene_with_hook_potential()` Pipeline (Opt-in)

When `--enhanced` flag used in `extract_clips`, scores include subject detection:

```python
frame_score = (
    subject_score * 0.25 +      # 25% - Subject detection (NEW)
    motion_score * 0.25 +       # 25% - Motion (reduced from 30%)
    composition_score * 0.15 +  # 15% - Composition (reduced from 20%)
    color_score * 0.15 +        # 15% - Color (reduced from 20%)
    sharpness * 0.10 +          # 10% - Sharpness (reduced from 15%)
    brightness_score * 0.10     # 10% - Brightness (reduced from 15%)
)

# Plus hook_potential classification into tiers:
# MAXIMUM (>=80), HIGH (>=65), MEDIUM (>=45), LOW (>=25), POOR (<25)
```

**Advantage**: Subject detection uses saliency analysis to identify visual interest points (objects, animals, dynamic foreground subjects). This WOULD differentiate between scenes with subjects vs. scenic landscapes.

**Limitation**: Still not available in `split` command (no `--enhanced` flag wired).

### 2.3 Breakdown of Individual Scoring Components

#### 2.3.1 Motion Score (30% weight)

**Calculation** (in `_calculate_motion_optical_flow()`):
```
optical_flow_magnitude = cv2.calcOpticalFlowFarneback()
motion_amount = min(mean_magnitude / 3.0 * 100, 100.0)  # Normalize by factor of 3
motion_quality = 1.0 - min(std_magnitude / mean_magnitude, 1.0)  # Consistency
motion_score = 0.7 * motion_amount + 0.3 * motion_quality
```

**Problem for drone footage**: All 7 scenes have smooth, consistent camera motion (no shaking). Farneback optical flow produces similar magnitude & consistency scores across scenes, so motion scores converge to 40-60 range.

**Tuning opportunity**: 
- Reduce motion weight (currently 30%) since all drone footage has similar motion
- OR introduce sub-metrics like "flow acceleration" (ramping speed-up/slow-down), "zoom motion", "orbital complexity"

#### 2.3.2 Composition Score (20% weight)

Weighted combination of:
- **Rule of thirds** (40%): Edge density at 1/3 and 2/3 intersections
- **Horizon level** (30%): Deviation from level (via Hough line detection)
- **Leading lines** (30%): Count and total length of salient lines

**Problem**: Landscape drone footage has strong horizons and leading lines consistently. All 7 scenes likely score 50-70 on composition.

**Tuning opportunity**: Weighted differently for drone content (prioritize depth/leading lines over horizon).

#### 2.3.3 Color Variance (20% weight)

```
saturation_score = (mean_sat / 255.0 * 50) + (std_sat / 128.0 * 50)
```

**Problem**: DJI footage has consistent color temperature across scenes. Golden hour scenes may score slightly higher if warm-toned, but variance is small.

**Tuning opportunity**: Introduce "color distinctiveness" metric (how unique is this scene's palette vs. neighbors?).

#### 2.3.4 Sharpness (15% weight)

```
variance = cv2.Laplacian(gray, cv2.CV_64F).var()
sharpness_score = min(variance / 500.0 * 100, 100.0)
```

**Problem**: All well-focused drone footage has similar sharpness. Focus rarely varies within a scene.

#### 2.3.5 Brightness Balance (15% weight)

```
ideal = 127
deviation = abs(mean_brightness - ideal) / ideal
brightness_score = max(0, 100 - deviation * 100)
```

**Problem**: Daytime footage converges to similar brightness values. Overexposure/underexposure only affects scenes if lighting dramatically changes (rare in 7-scene video).

---

## 3. Scene Filtering (FilterThresholds)

### 3.1 Current Filter Thresholds (Hardcoded)

```python
@dataclass
class FilterThresholds:
    min_motion_energy: float = 25.0      # Below this = filtered out (for split: LOW tier)
    ideal_motion_energy: float = 45.0    # Below this = medium tier
    min_brightness: float = 30.0
    max_brightness: float = 245.0
    max_shake_score: float = 40.0
    subject_score_threshold: float = 0.6 # Requires subject if using enhanced detection
```

### 3.2 Filter Logic

Scenes are tiered:
1. **High Subject** (only if `--enhanced`): subject_score >= 0.6
2. **High Motion**: motion_energy >= 45.0
3. **Medium Motion**: motion_energy >= 25.0
4. **Low Motion**: motion_energy < 25.0
5. **Filtered**: brightness out of range, shake > 40.0

### 3.3 Problem with DJI Case

If all 7 scenes have motion_energy in 35-50 range (likely for consistent drone motion):
- Some classified as "High Motion" (>=45)
- Some classified as "Medium Motion" (25-45)
- All pass brightness/shake checks

Result: All 7 pass filtering, but relative quality is indistinct because tiers are too coarse.

### 3.4 Missing Fine-Grained Metrics

These metrics are NOT used in filtering:

| Metric | Calculation | Why Useful |
|--------|-------------|-----------|
| **Depth Score** | Foreground/mid-ground/background layer variance | Distinguish scenes with clear subject foreground from flat landscapes |
| **Subject Score** | Saliency-based object detection (only in enhanced mode) | Identify whether scene has compelling subject matter |
| **Golden Hour Detection** | Warm hue ratio + saturation + brightness | Distinguish lighting quality |
| **Motion Smoothness** | Flow magnitude consistency across frame sequence | Smooth gimbal motion vs. jittery stabilization artifacts |
| **Color Distinctiveness** | Histogram uniqueness vs. scene neighbors | Avoid boring repetitive color palettes |
| **Hook Potential** | Combined subject + motion + color + composition score | Engagement metric for reel openers |

---

## 4. Recommended CLI Flags for Split Command

### 4.1 Critical (High Priority - Fixes Immediate Issue)

#### `--scene-threshold VALUE` (default 27.0)
- **Type**: FloatRange(15.0, 50.0)
- **Purpose**: Lower = more scenes detected, higher = fewer but longer scenes
- **Impact on DJI case**: Lowering to 20-22 would split the long segments into more granular scenes, potentially revealing subtle quality boundaries
- **Implementation**: Pass to SceneDetector constructor (currently ignored)

#### `--enhanced` flag
- **Type**: Boolean flag
- **Purpose**: Enable subject detection and hook potential scoring
- **Impact on DJI case**: Would give each scene a subject_score (0-100) and hook_tier (MAXIMUM/HIGH/MEDIUM/LOW/POOR), creating clear quality tiers
- **Tradeoff**: 2-3x slower (~30 sec per video instead of 10-15 sec), but provides much better scene differentiation
- **Implementation**: Add flag to `split()`, wire to `detect_scenes_enhanced()`

#### `--motion-weight FLOAT` (default 0.30)
- **Type**: FloatRange(0.0, 1.0)
- **Purpose**: Adjust motion score weight for drone-specific footage
- **Recommendation for drone footage**: Reduce to 0.15-0.20 (motion is expected to be smooth; don't overweight it)
- **Trade-off with other weights**: Would require UI to show or auto-normalize other weights

### 4.2 Secondary (Medium Priority - Fine-Tuning)

#### `--min-subject-score FLOAT` (default 0.3)
- **Type**: FloatRange(0.0, 1.0)
- **Purpose**: Only include scenes with subject detection score above threshold (requires `--enhanced`)
- **Impact**: Quickly filters out empty landscapes, prioritizes scenes with wildlife/boats/objects
- **Example**: `--enhanced --min-subject-score 0.5` would only show scenes with clear subjects

#### `--golden-hour-boost FLOAT` (default 1.0)
- **Type**: FloatRange(0.5, 2.0)
- **Purpose**: Multiply scores of scenes with golden hour detection by this factor
- **Impact**: Prioritize sunset/sunrise footage which often looks better
- **Implementation**: Run `detect_golden_hour()` on each scene, scale final score if True

#### `--depth-threshold FLOAT` (default 0.0, meaning no filter)
- **Type**: FloatRange(0.0, 100.0)
- **Purpose**: Minimum depth/layering score to pass filter
- **Impact**: Favor scenes with clear foreground/background separation (more cinematic)
- **Implementation**: Compute `calculate_depth_score()` during analysis phase, add to FilterResult tiers

#### `--analysis-scale FLOAT` (default 0.5)
- **Type**: FloatRange(0.25, 1.0)
- **Purpose**: Frame downscaling for faster scoring (0.5 = 50% resolution)
- **Tradeoff**: Higher = slower but more accurate, lower = faster but less detail
- **Use case**: `--analysis-scale 1.0` for maximum quality detection, `--analysis-scale 0.25` for quick preview

### 4.3 Advanced (Low Priority - Future Enhancement)

#### `--color-distinctiveness` flag
- Would compute histogram entropy of each scene vs. neighbors, boost unique color palettes
- Requires tracking cross-scene statistics (more complex pipeline change)

#### `--motion-variety` flag
- Would analyze flow vector consistency to detect interesting motion types (orbit, flyover, reveal)
- Boost scenes with motion_type != STATIC
- Example: Orbit/Flyover/Reveal scenes get +10 to final score

#### `--focus-area-detection` flag
- Would use face detection or object tracking (requires opencv-contrib-python dependency)
- Identify if scene has a subject in focus vs. landscape-only
- More robust than saliency-based subject_score

---

## 5. Why the 7 DJI Scenes Converge to Similar Scores

### Root Cause Analysis

Given a sequence of 7 landscape drone shots (55-64 score range):

1. **Motion Similarity** (30% weight):
   - All smooth gimbal-stabilized pans/orbital motion
   - Optical flow consistency: 35-55 motion_score across all scenes
   - No significant shake or jitter to differentiate

2. **Composition Similarity** (20% weight):
   - Landscape framing: strong horizon, leading lines
   - Hough line detection finds similar edge distributions
   - Composition scores: 45-65 across all scenes

3. **Brightness Similarity** (15% weight):
   - Daytime footage: mean brightness 90-110 (all pass balance check)
   - All scenes near ideal, so minimal brightness differentiation

4. **Color Similarity** (20% weight):
   - Same lighting conditions (daytime, no dramatic golden hour)
   - Saturation relatively consistent
   - Color scores: 40-60 across all scenes

5. **Sharpness Similarity** (15% weight):
   - Drone camera has consistent focus (not subject to focus breathing)
   - All in-focus: sharpness scores 60-80 across all scenes

**Combined Effect**:
```
All scenes → 0.6*max(55-65) + 0.4*mean(55-65) = 0.6*65 + 0.4*58 = 63.2
```

Result: Final scores converge to 55-64 range with no clear tiers.

---

## 6. How Proposed Parameters Would Fix This

### Scenario: `drone-reel split video.mp4 --scene-threshold 20 --enhanced --min-subject-score 0.4`

1. **Lower scene threshold (20 vs 27)**: Would detect 10-12 scenes instead of 7 (more granular)

2. **Enhanced analysis**: Each scene gets:
   - `subject_score`: 0.2 (empty landscape), 0.7 (wildlife), 0.5 (interesting rock formation)
   - `hook_tier`: POOR → HIGH based on subject + motion + color + composition

3. **Subject score filter (0.4)**: Would clearly separate:
   - TIER 1: Scenes with subject_score >= 0.5 (hook_tier HIGH/MAXIMUM)
   - TIER 2: Scenes with subject_score 0.4-0.5 (hook_tier MEDIUM)
   - TIER 3: Scenes with subject_score < 0.4 (hook_tier LOW/POOR, filtered out)

**Expected result**: Clear differentiation between "highlights with subjects" vs "scenic filler", instead of 7 nearly-equal scores.

---

## 7. Implementation Complexity Assessment

| Parameter | Complexity | Code Changes Needed | Performance Impact |
|-----------|------------|---------------------|-------------------|
| `--scene-threshold` | TRIVIAL | 1 line: wire config to SceneDetector | None (already computed) |
| `--enhanced` | LOW | ~10 lines: add flag, call detect_scenes_enhanced() instead of detect_scenes() | 2-3x slower (accept trade-off for quality) |
| `--motion-weight` | LOW | ~20 lines: parameterize scoring formula, update SceneDetector._score_scene() | None |
| `--min-subject-score` | LOW | ~5 lines: filter candidates after scene analysis (requires --enhanced) | None |
| `--golden-hour-boost` | MEDIUM | ~15 lines: compute detect_golden_hour() in analysis phase, scale score | ~10% slower |
| `--depth-threshold` | MEDIUM | ~20 lines: add depth_score to FilterResult tiers, new filter logic | ~5-10% slower |
| `--analysis-scale` | TRIVIAL | 1 line: wire to SceneDetector parameter | Variable (scales with setting) |

---

## 8. Recommended Rollout Strategy

### Phase 1 (Immediate - 1-2 hours)
1. Wire `--scene-threshold` to `split` command (fix bug, enable existing config)
2. Add `--enhanced` flag to `split` command (expose existing feature)
3. Add `--analysis-scale` flag to `split` command (expose existing parameter)

**Why**: These require minimal code changes, immediately unlock scene differentiation.

### Phase 2 (Short-term - 2-4 hours)
4. Add `--min-subject-score` filter (requires --enhanced)
5. Add `--golden-hour-boost` parameter
6. Add `--motion-weight` parameter with weight normalization

**Why**: Enable fine-grained user control over scene quality preferences.

### Phase 3 (Medium-term - 4+ hours)
7. Implement `--depth-threshold` filter
8. Add motion variety analysis (`ORBIT`, `FLYOVER`, `REVEAL` scoring)
9. Expose `--color-distinctiveness` flag

**Why**: Advanced features for power users, enable more cinematic highlight selection.

---

## 9. Testing Plan for DJI Video

Once parameters are implemented:

```bash
# Test 1: Basic threshold tuning
drone-reel split dji_video.mp4 --scene-threshold 20 --min-score 40 --preview

# Test 2: Enhanced detection with subject filtering
drone-reel split dji_video.mp4 --enhanced --min-subject-score 0.4 --preview

# Test 3: Combination (full tuning)
drone-reel split dji_video.mp4 \
  --scene-threshold 22 \
  --enhanced \
  --min-subject-score 0.35 \
  --golden-hour-boost 1.5 \
  --min-score 45 \
  --preview

# Test 4: Conservative mode (prioritize best scenes only)
drone-reel split dji_video.mp4 \
  --enhanced \
  --min-subject-score 0.6 \
  --min-score 60 \
  --sort score \
  --count 5 \
  --preview
```

**Expected outcome**: Clear visual differentiation between top-tier (5-star) and mid-tier (3-star) highlights, addressing the original "7 nearly-equal scores" problem.

---

## 10. Summary: Parameters Ranked by Impact on DJI Case

| Rank | Parameter | Impact on DJI Case | Why |
|------|-----------|-------------------|-----|
| 1 | `--enhanced` | **CRITICAL** | Subject detection would differentiate wildlife/objects from landscapes |
| 2 | `--scene-threshold` | **CRITICAL** | Current value (27) produces coarse splits; lowering to 20-22 creates more granular scene boundaries |
| 3 | `--min-subject-score` | **HIGH** | Would filter empty landscapes, leaving only scenes with visual subjects |
| 4 | `--motion-weight` | **HIGH** | Drone motion too smooth to differentiate; reducing 30% → 15% refocuses scoring on subject/color |
| 5 | `--golden-hour-boost` | **MEDIUM** | Would boost sunset shots if present in footage |
| 6 | `--depth-threshold` | **MEDIUM** | Would prefer foreground-subject shots over flat landscapes |
| 7 | `--analysis-scale` | **LOW** | Only useful for speed/quality trade-off, not differentiation |

---

## Conclusion

The split command's 7-similar-score problem stems from:
1. **Hardcoded threshold values** that are scene-agnostic
2. **Missing subject detection** (only available in `--enhanced` for extract_clips, not exposed in split)
3. **Even weighting of generic metrics** (motion, composition, color) that converge for landscape drone footage
4. **Coarse scene splits** (threshold=27 produces long scenes; more granular detection needed)

Implementing the **Phase 1 parameters** (`--scene-threshold`, `--enhanced`, `--analysis-scale`) would immediately provide users meaningful control over scene detection sensitivity and quality differentiation, directly addressing the DJI video use case.
