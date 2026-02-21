# BeatSync Quick Reference Card

## Quick Start

```python
from drone_reel.core.beat_sync import BeatSync
from pathlib import Path

# Initialize
beat_sync = BeatSync()

# Analyze
beat_info = beat_sync.analyze(Path("music.mp3"))

# Get optimal cut points
cut_points = beat_sync.get_cut_points(
    beat_info,
    target_duration=30.0,
    min_clip_length=2.0,
    max_clip_length=4.0,
)

# Use transition recommendations
for cp in cut_points:
    rec = cp.transition_rec
    print(f"{rec.transition_type}: {rec.intensity:.2f}")
```

---

## BeatInfo Fields

| Field | Type | Description |
|-------|------|-------------|
| `tempo` | float | BPM |
| `beat_times` | ndarray | All beat times (seconds) |
| `downbeat_times` | ndarray | Downbeat times (first beat of measure) |
| `duration` | float | Track duration (seconds) |
| `energy_profile` | ndarray | RMS energy over time (0-1) |
| `time_signature` | tuple | (beats_per_measure, note_value) |
| `phrase_boundaries` | ndarray | Musical section boundaries |
| `tempo_changes` | list | [(time, new_tempo), ...] |
| `spectral_profile` | ndarray | Brightness over time (0-1) |
| `onset_density` | ndarray | Rhythmic activity (0-1) |
| `harmonic_energy` | ndarray | Melodic component (0-1) |
| `percussive_energy` | ndarray | Rhythmic component (0-1) |

---

## CutPoint Fields

| Field | Type | Description |
|-------|------|-------------|
| `time` | float | Cut time (seconds) |
| `strength` | float | Cut quality (0-1) |
| `is_downbeat` | bool | On downbeat? |
| `beat_index` | int | Beat number |
| `is_phrase_boundary` | bool | At section boundary? |
| `transition_rec` | TransitionRecommendation | Transition details |

---

## TransitionRecommendation Fields

| Field | Type | Values | Description |
|-------|------|--------|-------------|
| `intensity` | float | 0-1 | Continuous intensity |
| `transition_type` | str | cut, fade, crossfade, impact | Recommended type |
| `duration` | float | 0.0-0.5 | Transition duration (seconds) |
| `energy_gradient` | str | rising, falling, stable | Energy direction |

---

## Common Patterns

### Check if downbeat is also phrase boundary

```python
for cp in cut_points:
    if cp.is_downbeat and cp.is_phrase_boundary:
        print(f"Perfect cut point at {cp.time:.2f}s")
```

### Filter high-quality cuts

```python
strong_cuts = [cp for cp in cut_points if cp.strength > 0.8]
```

### Get transition details

```python
for cp in cut_points:
    rec = cp.transition_rec
    print(f"{cp.time:.2f}s: {rec.transition_type} "
          f"({rec.intensity:.2f}) - {rec.energy_gradient}")
```

### Find tempo changes

```python
if beat_info.tempo_changes:
    for time, new_tempo in beat_info.tempo_changes:
        print(f"Tempo changes to {new_tempo:.1f} BPM at {time:.2f}s")
```

### Get energy at specific time

```python
energy = beat_sync.get_energy_at_time(beat_info, 15.5)
print(f"Energy at 15.5s: {energy:.2f}")
```

---

## Initialization Options

```python
BeatSync(
    hop_length=512,     # Frames between analysis (default: 512)
    min_tempo=60.0,     # Minimum BPM (default: 60)
    max_tempo=180.0,    # Maximum BPM (default: 180)
)
```

**Trade-offs:**
- Lower `hop_length` = more accurate, slower
- Higher `hop_length` = faster, less accurate
- Recommended: 512 for most music, 1024 for speed

---

## Transition Type Thresholds

| Type | Intensity | Conditions |
|------|-----------|------------|
| `impact` | > 0.75 | High percussion (> 0.7) |
| `cut` | > 0.6 | High energy |
| `crossfade` | > 0.3 | Medium energy |
| `fade` | ≤ 0.3 | Low energy |

---

## Performance Tips

### Fast analysis (trade accuracy for speed)

```python
beat_sync = BeatSync(hop_length=1024)  # 2x faster
```

### Prefer specific cut types

```python
# Prefer phrase boundaries over downbeats
phrase_cuts = [cp for cp in cut_points if cp.is_phrase_boundary]

# Only use high-energy cuts
energetic_cuts = [
    cp for cp in cut_points
    if cp.transition_rec.intensity > 0.7
]
```

### Calculate optimal clip count

```python
target_duration = 30.0
avg_clip_length = 3.0  # seconds
optimal_clips = int(target_duration / avg_clip_length)
```

---

## Scoring Weights

Cut point scoring breakdown:

```python
base_score = 0.5
+ 0.3 if is_downbeat
+ 0.4 if is_phrase_boundary
+ 0.15 * energy
+ 0.1 * spectral
+ 0.1 * onset_density
+ 0.15 * percussive_energy
= final_score (capped at 1.0)
```

---

## Intensity Calculation

```python
intensity = (
    0.4 * rms_energy +
    0.3 * percussive_energy +
    0.2 * onset_density +
    0.1 * abs(energy_gradient)
)
```

---

## Error Handling

```python
from pathlib import Path

audio_path = Path("music.mp3")

# Check file exists
if not audio_path.exists():
    raise FileNotFoundError(f"Audio file not found: {audio_path}")

# Analyze
try:
    beat_info = beat_sync.analyze(audio_path)
except Exception as e:
    print(f"Analysis failed: {e}")

# Check for beats
if len(beat_info.beat_times) == 0:
    print("Warning: No beats detected!")
```

---

## Debugging

### Print analysis summary

```python
print(f"Tempo: {beat_info.tempo:.1f} BPM")
print(f"Duration: {beat_info.duration:.2f}s")
print(f"Beats: {beat_info.beat_count}")
print(f"Downbeats: {len(beat_info.downbeat_times)}")
print(f"Time sig: {beat_info.time_signature}")
print(f"Phrases: {len(beat_info.phrase_boundaries)}")
```

### Visualize cut points

```python
for i, cp in enumerate(cut_points):
    marker = "🎵" if cp.is_downbeat else "  "
    phrase = "📍" if cp.is_phrase_boundary else "  "
    print(f"{i+1:2d}. {cp.time:6.2f}s {marker}{phrase} "
          f"[{cp.strength:.2f}] {cp.transition_rec.transition_type}")
```

---

## Backward Compatibility

### Old API (still works)

```python
# Old discrete intensity
intensity = beat_sync.suggest_transition_intensity(beat_info, cut_point)
# Returns: "hard", "medium", or "soft"
```

### New API (recommended)

```python
# New continuous intensity
rec = cut_point.transition_rec
intensity = rec.intensity  # 0-1 float
trans_type = rec.transition_type  # Specific type
```

---

## Common Use Cases

### Generate video reel cuts

```python
cut_points = beat_sync.get_cut_points(
    beat_info,
    target_duration=30.0,
    min_clip_length=2.0,
    max_clip_length=4.0,
    prefer_downbeats=True,
)

durations = beat_sync.calculate_clip_durations(cut_points, 30.0)

for i, (cp, duration) in enumerate(zip(cut_points[:-1], durations)):
    print(f"Clip {i+1}: {cp.time:.2f}s - {cp.time + duration:.2f}s")
```

### Sync to chorus/verse boundaries

```python
# Get cuts only at phrase boundaries
phrase_cuts = [
    cp for cp in cut_points
    if cp.is_phrase_boundary
]

# Use these for major transitions
for cp in phrase_cuts:
    print(f"Section change at {cp.time:.2f}s")
```

### Match cut intensity to music energy

```python
for cp in cut_points:
    energy = beat_sync.get_energy_at_time(beat_info, cp.time)
    rec = cp.transition_rec

    if rec.energy_gradient == "rising" and energy > 0.7:
        print(f"Building energy at {cp.time:.2f}s - use impact cut")
    elif rec.energy_gradient == "falling":
        print(f"Energy dropping at {cp.time:.2f}s - use fade")
```

---

## Demo Script

Run the comprehensive demo:

```bash
python examples/beat_sync_demo.py path/to/music.mp3
```

Shows:
- Complete analysis breakdown
- Optimal cut points with DP
- Transition recommendations
- Phrase boundaries
- Energy profiles
- Old vs new comparison

---

## Testing

```bash
# Run beat_sync tests
pytest tests/test_beat_sync.py -v

# With coverage
pytest tests/test_beat_sync.py --cov=src/drone_reel/core/beat_sync

# Specific test
pytest tests/test_beat_sync.py::TestBeatSyncCutPoints -v
```

---

## Dependencies

Required:
- `librosa` - audio analysis
- `numpy` - numerical operations
- `scipy.signal` - peak detection

Optional:
- `rich` - demo script output (not required for core functionality)

---

## Further Reading

- **Full Documentation:** `/docs/BEAT_SYNC_UPGRADE.md`
- **Implementation:** `/src/drone_reel/core/beat_sync.py`
- **Tests:** `/tests/test_beat_sync.py`
- **Demo:** `/examples/beat_sync_demo.py`
