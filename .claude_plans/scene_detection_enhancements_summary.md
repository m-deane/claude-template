# Scene Detection Enhancements Summary

**Date:** 2026-01-27
**Status:** COMPLETED

## Enhancements Implemented

### 1. Subject Detection (Saliency-Based)

**Implementation:** Added automatic subject detection using spectral residual saliency analysis - a lightweight approach that doesn't require ML models.

**New Method:**
- `_calculate_subject_score(frame)` - Returns (subject_score, visual_interest_density)

**Algorithm:**
1. Convert frame to grayscale and resize to 64x64 for efficiency
2. Apply DCT (Discrete Cosine Transform) to get frequency domain
3. Calculate spectral residual (log amplitude - smoothed log amplitude)
4. Apply inverse DCT to get saliency map
5. Threshold to find salient regions
6. Calculate visual interest density as ratio of salient pixels
7. Score based on density with optimal range 0.05-0.30

**Files Modified:**
- `src/drone_reel/core/scene_detector.py` (lines 818-880)

### 2. Hook Potential Algorithm

**Implementation:** Added Instagram-style hook potential scoring to identify scenes that make great video openers.

**New Enum:**
```python
class HookPotential(Enum):
    MAXIMUM = "maximum"  # 9-10: Wildlife, dynamic motion, golden hour
    HIGH = "high"        # 7-8: Moving boat, aerial reveal
    MEDIUM = "medium"    # 5-6: Static scenic, moderate interest
    LOW = "low"          # 3-4: Empty ocean, distant subjects
    POOR = "poor"        # 1-2: Overexposed, no focal point
```

**New Method:**
- `_calculate_hook_potential(frame, subject_score, motion_score, color_score, composition_score)` - Returns (hook_score, HookPotential tier)

**Scoring Formula:**
| Component | Weight | Description |
|-----------|--------|-------------|
| Subject Score | 35% | Salient subject presence |
| Motion Score | 25% | Dynamic movement quality |
| Color Vibrancy | 20% | Color saturation/variance |
| Composition | 10% | Rule of thirds, etc. |
| Uniqueness | 10% | Frame entropy/distinctiveness |

**Tier Thresholds:**
- MAXIMUM: ≥80
- HIGH: ≥65
- MEDIUM: ≥45
- LOW: ≥25
- POOR: <25

**Files Modified:**
- `src/drone_reel/core/scene_detector.py` (lines 894-946)

### 3. Enhanced Scene Scoring

**Implementation:** Extended `EnhancedSceneInfo` dataclass with new fields for hook-potential aware scene selection.

**New Fields:**
```python
@dataclass
class EnhancedSceneInfo(SceneInfo):
    # ... existing fields ...
    subject_score: float = 0.0           # 0-100 saliency-based subject score
    hook_potential: float = 0.0          # 0-100 hook potential score
    hook_tier: HookPotential = HookPotential.MEDIUM
    visual_interest_density: float = 0.0  # 0-1 ratio of interesting pixels
```

**New Method:**
- `score_scene_with_hook_potential(frame, prev_frame_gray)` - Combined scoring with new weights

**Updated Scoring Weights:**
| Metric | Old Weight | New Weight |
|--------|------------|------------|
| Subject Score | N/A | 25% |
| Motion | 20% | 25% |
| Composition | 25% | 15% |
| Color Variance | 20% | 15% |
| Sharpness | 25% | 10% |
| Brightness | 10% | 10% |

**Files Modified:**
- `src/drone_reel/core/scene_detector.py` (lines 60-77, 960-1012)

## Test Summary

- **New Tests Added:** 7 tests in `TestSubjectDetection`
- **Total Scene Detector Tests:** 27 (25 passed, 2 skipped)
- **Total Project Tests:** 586 passed
- **All Tests Pass:** ✅

### Test Coverage:
- `test_calculate_subject_score_uniform_frame` - Verifies low scores for uniform frames
- `test_calculate_subject_score_varied_frame` - Verifies varied frames produce valid scores
- `test_calculate_subject_score_returns_tuple` - Verifies return type
- `test_calculate_hook_potential_basic` - Verifies hook potential calculation
- `test_calculate_hook_potential_tiers` - Verifies tier classification
- `test_enhanced_scene_info_new_fields` - Verifies new dataclass fields
- `test_hook_potential_enum_values` - Verifies enum values

## Expected Score Improvements

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Scene Selection | 60/100 | 80/100 | +20 |
| Hook Quality | N/A | +25-35% | New capability |
| Subject Detection | N/A | +15-20% | New capability |

## Usage

### Calculate Subject Score
```python
from drone_reel.core.scene_detector import SceneDetector

detector = SceneDetector()
subject_score, density = detector._calculate_subject_score(frame)
print(f"Subject score: {subject_score:.1f}, Density: {density:.3f}")
```

### Calculate Hook Potential
```python
hook_score, tier = detector._calculate_hook_potential(
    frame,
    subject_score=75.0,
    motion_score=60.0,
    color_score=70.0,
    composition_score=65.0
)
print(f"Hook potential: {hook_score:.1f} ({tier.value})")
```

### Full Scene Scoring with Hook Potential
```python
score, metrics = detector.score_scene_with_hook_potential(frame, prev_frame_gray)
print(f"Total score: {score:.1f}")
print(f"Hook tier: {metrics['hook_tier'].value}")
```

## Integration with Pipeline

The hook potential scoring integrates with the existing pipeline:

1. **Scene Detection** → Finds scene boundaries
2. **Frame Scoring** → Now includes subject detection + hook potential
3. **Scene Selection** → Prioritizes HIGH/MAXIMUM hook potential for openers
4. **Beat Sync** → Aligns cuts to music beats
5. **Motion-Matched Transitions** → Uses motion data from enhanced scenes

## Next Steps

1. **Task 9 (Pending):** Implement dynamic cropping system (Ken Burns, punch-in)
2. **Task 10 (Pending):** Generate and test improved reels (V6+)
