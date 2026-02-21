# Algorithm Enhancement Plan for Drone-Reel

## Executive Summary

This plan synthesizes findings from viral pattern research, reel version analysis (V1-V5), and source footage evaluation to create a targeted enhancement roadmap. The goal is to improve the overall reel score from **56.75/100 (V5)** to **75+/100** by addressing five critical areas:

1. **Scene Detection** - Add subject detection, hook potential scoring, and motion trajectory analysis
2. **Transition System** - Fix the dark frame bug and implement motion-matched cuts
3. **Speed Ramping** - Implement smooth Bezier curves and auto-detect peak moments
4. **Dynamic Cropping** - Add subject tracking and Ken Burns effects
5. **Pacing Optimization** - Target 2.0-2.5s clips with proper energy arc

---

## Priority Matrix

| Enhancement | Impact Score | Effort | Expected Score Improvement |
|-------------|-------------|--------|---------------------------|
| Fix Dark Frame Bug | CRITICAL | Low | +10 points (transition score) |
| Subject Detection Scoring | High | Medium | +8 points (hook/subject) |
| Hook Potential Algorithm | High | Medium | +12 points (hook score) |
| Speed Ramping Integration | High | Medium | +15 points (speed score) |
| Motion-Matched Cuts | Medium | Medium | +5 points (transition) |
| Ken Burns for Static Shots | Medium | Low | +5 points (pacing) |
| Crossfade Timing | Medium | Low | +3 points (transition) |

---

## 1. Scene Detection Enhancements

### 1.1 Subject Detection Scoring

**Problem**: Current scoring treats all content equally. Whale footage scores similarly to empty ocean.

**Implementation Location**: `src/drone_reel/core/scene_detector.py`

**Algorithm Design**:
```
Subject Detection Weights:
- wildlife_present: 2.0x boost (whales, dolphins, birds)
- human_activity: 1.5x boost (boats, people)
- dynamic_subject: 1.3x boost (moving objects against water)
- texture_only: 0.7x penalty (empty ocean, sky)
```

**New Scoring Weights** (modify `_score_scene` method):
```python
# Current weights:
#   motion_score * 0.30 + composition_score * 0.20 +
#   color_score * 0.20 + sharpness * 0.15 + brightness_score * 0.15

# New weights with subject detection:
#   subject_score * 0.25 + motion_score * 0.25 + composition_score * 0.15 +
#   color_score * 0.15 + sharpness * 0.10 + brightness_score * 0.10
```

### 1.2 Hook Potential Calculation Algorithm

**Algorithm Design**:
```
Hook Potential Score = weighted_sum(
    visual_interest_density * 0.35,    # Subjects per frame area
    motion_intensity * 0.25,           # Optical flow magnitude
    color_vibrancy * 0.20,             # Saturation + contrast
    composition_strength * 0.10,       # Rule of thirds alignment
    uniqueness_factor * 0.10           # Difference from other clips
)
```

**Hook Classification Tiers**:
- MAXIMUM (9-10): Wildlife in frame, dynamic motion, high contrast
- HIGH (7-8): Moving boat, golden hour landscape, dramatic reveal
- MEDIUM (5-6): Static scenic, mountain panorama, ocean with texture
- LOW (3-4): Empty ocean, distant subjects, flat lighting
- POOR (1-2): Overexposed, underexposed, no focal point

### 1.3 Motion Trajectory Analysis

**Enhanced Classification** (extend `classify_camera_motion()`):
```python
MotionType additions:
- WHALE_TRACKING: Following subject in water
- ASCENDING_REVEAL: Upward motion with increasing scene complexity
- DESCENDING_APPROACH: Downward motion toward subject
```

### 1.4 Reveal Moment Detection

**Detection Algorithm**:
1. Measure scene complexity growth over time (edge density increase)
2. Detect subject emergence (blob appearing where none existed)
3. Track horizon reveal (sky-to-land or water-to-subject transition)
4. Score based on complexity_delta / time_delta

---

## 2. Transition System Enhancements

### 2.1 Dark Frame Bug Fix (CRITICAL - P0)

**Problem**: V4 Fixed and V5 have a dark/black frame at ~2.0-2.5 seconds.

**Root Cause Investigation Points**:

1. **video_processor.py line 348-367** - `_concatenate_with_transitions()` method
2. **video_processor.py line 369-386** - `_apply_transition_in()` method

**Recommended Fix**:
```python
def _apply_transition_in(self, clip, transition, duration):
    # Clamp duration to prevent frame dropout
    safe_duration = min(duration, clip.duration * 0.4)
    if safe_duration < 0.1:
        return clip  # Skip transition if clip too short

    return clip.with_effects([vfx.CrossFadeIn(safe_duration)])
```

### 2.2 Motion-Matched Cuts Implementation

**Algorithm**:
```python
def _select_motion_matched_transition(self, clip1_motion, clip2_motion):
    # Direction match: same screen direction = hard cut
    if motion_directions_aligned(clip1_motion, clip2_motion):
        return TransitionType.CUT, 0.0

    # Speed match: similar velocity = quick crossfade
    if motion_speeds_similar(clip1_motion, clip2_motion):
        return TransitionType.CROSSFADE, 0.2

    # Different motion: longer crossfade
    return TransitionType.CROSSFADE, 0.4
```

### 2.3 Crossfade Timing (0.3-0.5s)

**Dynamic Duration**:
```python
def _calculate_transition_duration(self, beat_info, cut_time):
    is_downbeat = np.any(np.abs(beat_info.downbeat_times - cut_time) < 0.1)

    if is_downbeat:
        return 0.2  # Quick cut on strong beat
    else:
        return 0.4  # Smoother transition on weak beat
```

### 2.4 Whip Pan Transitions

**Implementation**:
```python
def _transition_whip_pan(self, clip1, clip2, duration=0.2):
    """
    Create whip pan transition with motion blur simulation.

    Technique:
    1. Speed up last 5 frames of clip1
    2. Add horizontal motion blur
    3. Speed up first 5 frames of clip2
    4. Blend at peak blur point
    """
```

---

## 3. Speed Ramping Implementation

### 3.1 Smooth Bezier Curves (10-20 frames)

**Integration Points**:
1. CLI: Add `--speed-ramp` flag (auto, subtle, dramatic, none)
2. Pipeline: Apply after clip extraction, before stitching

**Curve Enhancement**:
```python
def _ease_in_out(self, t, steepness=3.0):
    """
    Configurable cubic ease-in-out.
    steepness: 2.0 = gentle, 3.0 = standard, 4.0 = aggressive
    """
```

### 3.2 Auto-Detect Peak Moments for Slow-Mo (50%)

**Detection Algorithm**:
- Calculate motion magnitude per frame
- Find peaks above 75th percentile
- Apply 50% slow-mo at peaks

### 3.3 Ramp Patterns

```python
RAMP_PATTERNS = {
    "punch": [...],           # Quick slow-mo hit
    "dramatic_reveal": [...], # Slow build to reveal
    "energy_burst": [...],    # Quick speed cycle
}
```

---

## 4. Dynamic Cropping Enhancements

### 4.1 Subject Tracking Across Frames

**Implementation**:
```python
# Initialize CSRT tracker on detected subjects
self._object_tracker = cv2.TrackerCSRT_create()

# Track frame-to-frame for smooth following
success, bbox = self._object_tracker.update(frame)
```

### 4.2 Ken Burns Effect for Static Shots

**Add new ReframeMode**:
```python
class ReframeMode(Enum):
    KEN_BURNS = "ken_burns"  # Slow zoom + pan

# Parameters
ken_burns_zoom_factor: float = 1.1  # 10% zoom over clip
ken_burns_pan_direction: tuple = (0.1, 0.05)  # X, Y per second
```

### 4.3 Punch-In for Emphasis

**Beat-synced implementation**:
```python
if is_beat_at_time(beat_info, current_time):
    punch_progress = get_punch_curve(time_since_beat)
    frame = reframer.apply_punch_in(frame, focal_point, 0.05, punch_progress)
```

### 4.4 Composition-Aware Auto-Framing

**Weight saliency toward rule-of-thirds positions**

---

## 5. Pacing Optimization

### 5.1 Target 2.0-2.5s Clip Duration

**New defaults**:
```python
min_clip_length: float = 1.5
max_clip_length: float = 3.0
target_clip_length: float = 2.25  # Sweet spot
```

### 5.2 Energy Arc: High -> Medium -> High -> Peak

**Structure**:
```
- Position 0 (0-10%): HIGHEST hook potential
- Positions 1-40%: Build - increasing energy
- Position 40-70%: Climax - peak energy
- Position 70-90%: Second climax
- Position 90-100%: Resolve - strong closer
```

### 5.3 Cut Alignment with Beat Markers

**Target: 90%+ alignment**
```python
def calculate_beat_alignment_score(self, cut_times, beat_times, tolerance=0.1):
    aligned_count = sum(1 for cut in cut_times
                       if np.any(np.abs(beat_times - cut) < tolerance))
    return aligned_count / len(cut_times)
```

---

## Implementation Sequence

### Phase 1: Critical Bug Fix (Week 1)
1. Dark Frame Bug Investigation & Fix
2. Test V6 Generation

### Phase 2: Hook Optimization (Week 2)
1. Subject Detection Scoring
2. Hook Potential Algorithm
3. Test with Whale Footage (verify 0356 @ 5:00-7:00 selected as opener)

### Phase 3: Speed Ramping Integration (Week 3)
1. CLI Integration
2. Auto-Detection Enhancement
3. Curve Refinement

### Phase 4: Transition Enhancements (Week 4)
1. Motion-Matched Cuts
2. Crossfade Timing
3. Whip Pan Transitions

### Phase 5: Dynamic Cropping (Week 5)
1. Subject Tracking
2. Ken Burns Effect
3. Punch-In Integration

### Phase 6: Pacing Optimization (Week 6)
1. Duration Targeting
2. Energy Arc Sequencing
3. Beat Alignment Enforcement

---

## Expected Score Improvements

| Category | V5 Score | Target Score | Improvement |
|----------|----------|--------------|-------------|
| Hook Effectiveness | 65 | 85 | +20 |
| Transition Quality | 45 | 75 | +30 |
| Pacing Quality | 55 | 75 | +20 |
| Subject Visibility | 70 | 80 | +10 |
| Speed Usage | 35 | 70 | +35 |
| **Overall** | **56.75** | **77** | **+20.25** |

---

## Critical Files for Implementation

| File | Enhancement Target |
|------|-------------------|
| `scene_detector.py` | Subject detection, hook potential, motion trajectory |
| `video_processor.py` | Dark frame fix, motion-matched cuts, transitions |
| `speed_ramper.py` | Bezier curves, peak moment detection |
| `reframer.py` | Subject tracking, Ken Burns, punch-in |
| `cli.py` | CLI flags, energy arc sequencing |
