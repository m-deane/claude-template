# V3 Improvements - Final Polish

## Priority Fixes

### 1. Saliency-Aware Cropping (Critical)
The center-crop lost the boat in the hook scene. Need intelligent subject tracking.

```python
# Instead of center crop, use the existing Reframer with saliency
from drone_reel.core.reframer import Reframer

reframer = Reframer()
clip = reframer.reframe(
    clip,
    target_ratio=(9, 16),
    mode='saliency',  # Detect and track subjects
    horizon_lock=True
)
```

### 2. Shorter Transitions
Current 0.5s fade is too long. Reduce to 0.3s.

### 3. Exposure Normalization
Dark clips need brightness boost before color grading.

### 4. Audio Integration
Add royalty-free music with beat sync.

## Remaining Feature Integration

### Text Overlays
```python
from drone_reel.core.text_overlay import TextRenderer, TextOverlay, TextAnimation

renderer = TextRenderer()
overlay = TextOverlay(
    text="Sardinia, Italy 🇮🇹",
    position=(0.5, 0.85),
    font='Montserrat-Bold',
    size=42,
    animation=TextAnimation.SLIDE_UP,
    start_time=1.0,
    duration=3.0
)
```

### Speed Ramping
```python
from drone_reel.core.speed_ramper import SpeedRamper, SpeedRamp

ramper = SpeedRamper()
# Slow-mo on reveal moments
ramp = SpeedRamp(
    start_time=0.5,
    end_time=2.0,
    start_speed=1.0,
    end_speed=0.5,
    easing='ease_in_out'
)
```

## Quality Checklist

- [ ] Full frame utilization (no letterbox)
- [ ] Cinematic color grade
- [ ] Smooth transitions (0.3s fades)
- [ ] Subject-aware cropping
- [ ] Exposure normalized across clips
- [ ] Audio track with beat sync
- [ ] Location text overlay
- [ ] Speed ramps on key moments
- [ ] Hook scene optimized
- [ ] Narrative arc (Hook→Build→Climax→Resolve)

## Final Pipeline

```
Input Videos
    ↓
Scene Detection (enhanced)
    ↓
Diversity Selection
    ↓
Hook Optimization
    ↓
Narrative Sequencing
    ↓
Motion Continuity
    ↓
For each clip:
    → Saliency-aware reframing (9:16)
    → Exposure normalization
    → Color grading
    → Speed ramping
    ↓
Concatenate with 0.3s fades
    ↓
Add music + beat sync
    ↓
Add text overlays
    ↓
Export (Instagram preset)
```
