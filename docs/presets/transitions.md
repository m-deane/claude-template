# Transitions Reference

drone-reel supports 23 transition effects between clips, from classic cuts and fades to cinematic parallax and vortex effects.

## Available Transitions

### Basic Transitions

#### cut
Hard cut with no effect. Instant switch between clips.

**Best for:** Fast-paced edits, action footage, high-energy music

---

#### crossfade
Smooth dissolve where one clip fades out while the next fades in. The clips overlap during the transition.

**Best for:** Most general purpose editing, smooth flowing content

---

#### fade_black
Fade out to black, then fade in from black. Creates a clear separation between clips.

**Best for:** Scene changes, chapter breaks, dramatic moments

---

#### fade_white
Fade out to white, then fade in from white. Creates a bright, ethereal transition.

**Best for:** Dream sequences, flashbacks, uplifting moments

---

### Zoom Transitions

#### zoom_in
Zoom into the outgoing clip before cutting to the next.

**Best for:** Drawing attention, creating energy, beat drops

---

#### zoom_out
Zoom out from the incoming clip after cutting.

**Best for:** Revealing shots, calming transitions

---

### Slide & Wipe Transitions

#### slide_left / slide_right
Slide transition where one clip moves off-screen while the next slides in.

**Best for:** Modern content, social media style

---

#### wipe_left / wipe_right
Wipe transition where a line moves across revealing the next clip.

**Best for:** Energetic content, retro style

---

#### wipe_diagonal
A 45-degree diagonal wipe with feathered edge that sweeps from corner to corner.

**Best for:** Dynamic sequences, different-motion scene pairs

---

#### wipe_diamond
Diamond-shaped reveal from center outward using L1 distance masking with soft edge.

**Best for:** Orbit shots, circular camera movements

---

### Cinematic Transitions

#### whip_pan
Fast horizontal blur simulating a camera whip pan between scenes.

**Best for:** Energetic drone movements, panning shots, action sequences

---

#### iris_in / iris_out
Circular iris that closes in on the outgoing clip or opens to reveal the incoming clip.

**Best for:** Dramatic reveals, focus transitions, retro cinematic style

---

#### flash_white
Brief bright flash between clips simulating a camera flash or light burst.

**Best for:** High-energy moments, beat drops, dramatic impact

---

#### light_leak
Warm orange/golden light leak overlay that transitions between clips with a filmic glow.

**Best for:** Golden hour footage, warm/nostalgic content, dreamy transitions

---

#### hyperlapse_zoom
Rapid zoom with motion blur simulating a hyperlapse speed change between clips.

**Best for:** Hyperlapse footage, FPV drone content, speed transitions

---

### Depth & Motion Transitions

#### parallax_left / parallax_right
Differential-speed slide: the top half shifts at 15% while the bottom shifts at 35%, creating a parallax depth illusion.

**Best for:** Slow panning shots, landscape reveals, travel content

---

#### fog_pass
Multi-frequency sinusoidal fog pattern that rolls across the frame, obscuring and then revealing the next clip.

**Best for:** Tilt-down shots, moody sequences, nature footage

---

#### vortex_zoom
Radial zoom blur with iterative averaging that spirals outward, creating a vortex effect between clips.

**Best for:** Fast FPV drone footage, high-energy sequences, action content

---

### Stylistic Transitions

#### glitch_rgb
Digital glitch effect with RGB channel splitting and scan line artifacts.

**Best for:** Urban/cyberpunk content, electronic music, creative projects

---

## Usage

### CLI

```bash
# Set default transition for all cuts
drone-reel create -i ./clips/ --transition crossfade
drone-reel create -i ./clips/ --transition fog_pass
drone-reel create -i ./clips/ --transition vortex_zoom
```

### Python API

```python
from drone_reel import VideoProcessor
from drone_reel.core.video_processor import TransitionType

processor = VideoProcessor()

# Manually specify transitions for each cut
transitions = [
    TransitionType.CROSSFADE,
    TransitionType.PARALLAX_LEFT,
    TransitionType.WIPE_DIAMOND,
    TransitionType.FOG_PASS,
    TransitionType.VORTEX_ZOOM,
]

segments = processor.create_segments_from_scenes(
    scenes,
    durations,
    transitions=transitions,
    transition_duration=0.3  # Duration of each transition in seconds
)
```

---

## Motion-Matched Transitions

drone-reel automatically selects transitions based on scene motion type when `--transition` is not specified:

| Motion Type | Transition | Reason |
|-------------|-----------|--------|
| PAN_LEFT | SLIDE_LEFT | Matches directional movement |
| PAN_RIGHT | SLIDE_RIGHT | Matches directional movement |
| PAN (slow) | PARALLAX_LEFT/RIGHT | Depth parallax enhances slow pans |
| TILT_UP | ZOOM_OUT | Upward reveal matches zoom |
| TILT_DOWN | FOG_PASS | Fog obscures downward tilt |
| ORBIT | WIPE_DIAMOND | Diamond shape complements circular motion |
| FPV (fast) | VORTEX_ZOOM | Radial blur matches FPV speed |
| FLYOVER | HYPERLAPSE_ZOOM | Speed zoom matches forward movement |
| REVEAL | IRIS_IN | Iris reveals match dramatic reveals |
| Different high-motion | WIPE_DIAGONAL | Diagonal wipe bridges contrasting motions |
| STATIC | CROSSFADE | Smooth dissolve for still shots |

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
| Low (0.0-0.3) | Crossfade, fade_black, parallax |
| Medium (0.3-0.7) | Crossfade, fade_black, zoom_out, wipe_diagonal |
| High (0.7-1.0) | Cut, zoom_in, vortex_zoom, whip_pan, flash_white |

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
