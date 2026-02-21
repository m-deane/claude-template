# Narrative Module - Quick Reference

## Overview

The narrative module provides hook generation and narrative arc sequencing for creating viral drone reels optimized for social media engagement.

## Quick Start

```python
from drone_reel.core import (
    HookGenerator,
    HookPattern,
    NarrativeSequencer,
    NarrativeArc,
)

# Generate hook
generator = HookGenerator()
hook_segments = generator.create_hook_sequence(
    scenes,
    HookPattern.DRAMATIC_REVEAL,
    hook_duration=3.0
)

# Sequence scenes
sequencer = NarrativeSequencer(arc_type=NarrativeArc.CLASSIC)
sequenced = sequencer.sequence(scenes, target_duration=30.0)
```

## Hook Patterns

| Pattern | Description | Segments | Best For |
|---------|-------------|----------|----------|
| `DRAMATIC_REVEAL` | Single high-impact scene with fade-in | 1 | Showcasing best moment |
| `QUICK_CUT_MONTAGE` | 3-4 rapid cuts for instant energy | 3-4 | Action/variety content |
| `SPEED_RAMP_INTRO` | High-motion scene with dynamic feel | 1 | Movement-heavy footage |
| `TEXT_REVEAL` | Extended fade for text overlay | 1 | Branded/captioned videos |

## Narrative Arcs

| Arc | Pattern | Energy Curve | Best For |
|-----|---------|--------------|----------|
| `CLASSIC` | Hook → Build → Climax → Resolve | Peak-Rising-Peak-Falling | General content, proven engagement |
| `BUILDING` | Continuous increase | Low → High | Building anticipation, reveals |
| `BOOKEND` | Strong open/close | Peak-Medium-Peak | Memorable start/end |
| `MONTAGE` | Rapid variety | Alternating high/medium | Diverse content showcase |
| `CINEMATIC` | Slow atmospheric | Low-Rising-Low | Artistic, mood pieces |

## API Reference

### HookGenerator

**Initialization**:
```python
generator = HookGenerator(
    motion_weight=0.4,        # Weight for motion in scoring
    composition_weight=0.3    # Weight for composition
)
```

**Methods**:

```python
# Select best hook scene
hook_scene = generator.select_hook_scene(
    scenes: list[SceneInfo],
    prefer_motion_types: list[str] = ["reveal", "orbit", "flyover"]
) -> SceneInfo

# Create hook sequence
segments = generator.create_hook_sequence(
    scenes: list[SceneInfo],
    pattern: HookPattern,
    hook_duration: float = 3.0
) -> list[ClipSegment]

# Score hook potential
score = generator.score_hook_potential(
    scene: SceneInfo
) -> float  # 0-100
```

### NarrativeSequencer

**Initialization**:
```python
sequencer = NarrativeSequencer(
    arc_type: NarrativeArc = NarrativeArc.CLASSIC
)
```

**Methods**:

```python
# Sequence scenes
sequenced = sequencer.sequence(
    scenes: list[SceneInfo],
    target_duration: float = 30.0,
    hook_duration: float = 3.0,
    beat_info: Optional[BeatInfo] = None  # For music-aware sequencing
) -> list[SceneInfo]

# Calculate energy curve
energy_curve = sequencer.calculate_energy_curve(
    scenes: list[SceneInfo]
) -> list[float]  # 0-1 values
```

## Common Workflows

### 1. Basic Hook + Sequence

```python
# Create hook
generator = HookGenerator()
hook_segments = generator.create_hook_sequence(
    scenes, HookPattern.DRAMATIC_REVEAL, 3.0
)

# Sequence remaining scenes
hook_scene = hook_segments[0].scene
remaining = [s for s in scenes if s != hook_scene]
sequencer = NarrativeSequencer(NarrativeArc.CLASSIC)
sequenced = sequencer.sequence(remaining, 27.0)

# Combine: hook + sequenced scenes
final = [hook_scene] + sequenced
```

### 2. Music-Aware Sequencing

```python
from drone_reel.core import BeatSync

# Analyze music
beat_sync = BeatSync()
beat_info = beat_sync.analyze(Path("soundtrack.mp3"))

# Sequence with beat awareness
sequencer = NarrativeSequencer(NarrativeArc.CLASSIC)
sequenced = sequencer.sequence(
    scenes,
    target_duration=30.0,
    beat_info=beat_info
)
```

### 3. Custom Arc Selection

```python
# Choose arc based on content type
if content_type == "action":
    arc = NarrativeArc.MONTAGE
elif content_type == "cinematic":
    arc = NarrativeArc.CINEMATIC
else:
    arc = NarrativeArc.CLASSIC

sequencer = NarrativeSequencer(arc_type=arc)
sequenced = sequencer.sequence(scenes, 30.0)
```

### 4. Energy Analysis

```python
# Analyze energy progression
sequencer = NarrativeSequencer(NarrativeArc.CLASSIC)
sequenced = sequencer.sequence(scenes, 30.0)
energy = sequencer.calculate_energy_curve(sequenced)

# Check energy characteristics
peak_energy = max(energy)
avg_energy = sum(energy) / len(energy)
energy_variance = np.std(energy)

print(f"Peak: {peak_energy:.2f}")
print(f"Average: {avg_energy:.2f}")
print(f"Variance: {energy_variance:.2f}")
```

## Motion Types Detected

- `reveal`: High-impact dramatic reveals (score > 80)
- `orbit`: Circular camera movement (score 60-80)
- `flyover`: Forward motion flyovers (score 40-60)
- `pan`: Horizontal pans (score 20-40)
- `tilt`: Vertical tilts (inferred from motion)
- `static`: Minimal movement (score < 20)

## Scoring Factors

### Hook Potential Score (0-100)

| Factor | Weight | Description |
|--------|--------|-------------|
| Base scene score | Base | Scene quality from detector |
| Motion intensity | 20% × weight | Amount of camera movement |
| Visual complexity | 15% × weight | Composition complexity |
| Visual variety | 10% | Scene duration factor |
| Motion type | +20% | Bonus for preferred motion |
| Golden hour | +15% | High-quality lighting bonus |
| Dramatic subject | +10% | High motion intensity bonus |

### Energy Matching

Scenes matched to arc sections based on:
- Energy level match: 50%
- Duration match: 30%
- Beat energy match (if available): 20%

## Best Practices

1. **Hook Selection**: Use scenes with score > 75 for hooks
2. **Arc Choice**: Start with CLASSIC for general content
3. **Duration**: Target 3s hook + 27s body for 30s videos
4. **Beat Sync**: Always use when music is available
5. **Energy Variance**: Aim for 0.15-0.25 std dev for engagement

## Error Handling

Common errors and solutions:

```python
# ValueError: No scenes provided
# → Ensure scenes list is not empty

# ValueError: Need at least 3 scenes for quick cut montage
# → Use DRAMATIC_REVEAL pattern instead, or add more scenes

# Empty sequence result
# → Check that scenes meet minimum duration requirements
```

## Performance Tips

- Hook generation: ~10ms for 10 scenes
- Sequencing: ~50ms for 20 scenes
- Pre-filter scenes by score before sequencing for faster processing
- Cache energy curves for repeated analysis

## Integration Examples

### With Video Processor

```python
from drone_reel.core import VideoProcessor

# Create segments from sequenced scenes
processor = VideoProcessor()
clip_durations = [3.0] * len(sequenced)
segments = processor.create_segments_from_scenes(
    sequenced,
    clip_durations,
    transitions=[TransitionType.CROSSFADE] * (len(sequenced) - 1)
)

# Stitch
processor.stitch_clips(segments, output_path, audio_path)
```

### With Scene Detector

```python
from drone_reel.core import SceneDetector

# Detect and sequence
detector = SceneDetector()
scenes = detector.detect_scenes(video_path)

# Select high-quality scenes only
quality_scenes = [s for s in scenes if s.score > 60]

# Sequence for viral reel
sequencer = NarrativeSequencer(NarrativeArc.CLASSIC)
sequenced = sequencer.sequence(quality_scenes, 30.0)
```

## Testing

Run tests with:
```bash
pytest tests/test_narrative.py -v
```

47 tests cover:
- All hook patterns
- All narrative arcs
- Beat sync integration
- Edge cases (empty, single scene, etc.)
- Complete workflows

Coverage: 95%
