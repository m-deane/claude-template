# Transitions Reference

drone-reel supports various transition effects between clips.

## Available Transitions

### cut
Hard cut with no effect. Instant switch between clips.

**Best for:** Fast-paced edits, action footage, high-energy music

---

### crossfade
Smooth dissolve where one clip fades out while the next fades in. The clips overlap during the transition.

**Best for:** Most general purpose editing, smooth flowing content

---

### fade_black
Fade out to black, then fade in from black. Creates a clear separation between clips.

**Best for:** Scene changes, chapter breaks, dramatic moments

---

### fade_white
Fade out to white, then fade in from white. Creates a bright, ethereal transition.

**Best for:** Dream sequences, flashbacks, uplifting moments

---

### zoom_in
Zoom into the outgoing clip before cutting to the next.

**Best for:** Drawing attention, creating energy, beat drops

---

### zoom_out
Zoom out from the incoming clip after cutting.

**Best for:** Revealing shots, calming transitions

---

### slide_left / slide_right
Slide transition where one clip moves off-screen while the next slides in.

**Best for:** Modern content, social media style

---

### wipe_left / wipe_right
Wipe transition where a line moves across revealing the next clip.

**Best for:** Energetic content, retro style

---

## Usage

### CLI

```bash
# Set default transition for all cuts
drone-reel create -i ./clips/ --transition crossfade
drone-reel create -i ./clips/ --transition fade_black
drone-reel create -i ./clips/ --transition cut
```

### Python API

```python
from drone_reel import VideoProcessor
from drone_reel.core.video_processor import TransitionType

processor = VideoProcessor()

# Manually specify transitions for each cut
transitions = [
    TransitionType.CROSSFADE,
    TransitionType.CROSSFADE,
    TransitionType.ZOOM_IN,
    TransitionType.FADE_BLACK
]

segments = processor.create_segments_from_scenes(
    scenes,
    durations,
    transitions=transitions,
    transition_duration=0.3  # Duration of each transition in seconds
)
```

---

## Energy-Based Transitions

drone-reel can automatically select transitions based on music energy:

```python
from drone_reel.presets.transitions import get_transitions_for_energy

# Get transitions for high-energy section
transitions = get_transitions_for_energy(
    energy_level=0.8,    # 0.0 to 1.0
    count=10,            # Number of transitions needed
    style="dynamic"      # Style: "dynamic", "smooth", or "punchy"
)
```

### Styles

| Style | Description | Transitions Used |
|-------|-------------|------------------|
| **dynamic** | Mix of transitions based on energy | All types |
| **smooth** | Gentle, flowing transitions | Crossfade, fade_black |
| **punchy** | Quick, energetic transitions | Cut, zoom_in, zoom_out |

### Energy Mapping

| Energy Level | Typical Transitions |
|--------------|---------------------|
| Low (0.0-0.3) | Crossfade, fade_black |
| Medium (0.3-0.7) | Crossfade, fade_black, zoom_out |
| High (0.7-1.0) | Cut, zoom_in, zoom_out |

---

## Transition Duration

The default transition duration is **0.3 seconds**. You can adjust this in the configuration or via API:

```python
# In configuration (~/.config/drone_reel/config.json)
{
    "transition_duration": 0.5
}

# Via API
segments = processor.create_segments_from_scenes(
    scenes,
    durations,
    transition_duration=0.5  # 500ms transitions
)
```

### Recommendations

| Tempo | Transition Duration |
|-------|---------------------|
| Slow (<80 BPM) | 0.5 - 1.0 seconds |
| Medium (80-120 BPM) | 0.3 - 0.5 seconds |
| Fast (>120 BPM) | 0.1 - 0.3 seconds |

---

## Beat-Synced Transitions

When music is provided, drone-reel automatically aligns transitions with beats:

```python
from drone_reel.core.beat_sync import BeatSync

beat_sync = BeatSync()
beat_info = beat_sync.analyze(Path("music.mp3"))

# Get cut points aligned with beats
cut_points = beat_sync.get_cut_points(
    beat_info,
    target_duration=45.0,
    prefer_downbeats=True  # Prioritize strong beats for cuts
)

# Suggest transition intensity based on beat strength
for cp in cut_points:
    intensity = beat_sync.suggest_transition_intensity(beat_info, cp)
    print(f"Cut at {cp.time:.2f}s - {intensity} transition")
    # Returns: "hard", "medium", or "soft"
```
