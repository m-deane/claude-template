# Text Overlay Quick Reference

## Quick Start

```python
from moviepy import VideoFileClip
from drone_reel.core.text_overlay import TextAnimation, TextOverlay, TextRenderer

# Initialize renderer
renderer = TextRenderer()

# Load video
clip = VideoFileClip("video.mp4")

# Create basic overlay
overlay = TextOverlay(
    text="Your Text Here",
    start_time=1.0,
    duration=3.0,
)

# Apply and save
result = renderer.apply_overlay_to_clip(clip, overlay)
result.write_videofile("output.mp4")
```

## Animation Types

| Animation | Description | Best For |
|-----------|-------------|----------|
| `NONE` | No animation | Static text |
| `FADE_IN` | Fade from transparent | Subtle entrance |
| `FADE_OUT` | Fade to transparent | Subtle exit |
| `FADE_IN_OUT` | Fade in then out | Full lifecycle |
| `POP` | Scale up then settle | Attention-grabbing |
| `TYPEWRITER` | Character by character | Storytelling |
| `SLIDE_UP` | Slide from bottom | News/captions |
| `SLIDE_DOWN` | Slide from top | Announcements |
| `SLIDE_LEFT` | Slide from right | Lower thirds |
| `SLIDE_RIGHT` | Slide from left | Credits |

## Common Patterns

### 1. Title Card
```python
overlay = TextOverlay(
    text="EPIC DRONE FOOTAGE",
    position=(0.5, 0.5),
    font_size=96,
    color=(255, 255, 255),
    animation_in=TextAnimation.POP,
    animation_out=TextAnimation.FADE_OUT,
    animation_duration=0.5,
    start_time=0.0,
    duration=3.0,
)
```

### 2. Lower Third (Modern)
```python
overlays = renderer.create_lower_third(
    title="Location Name",
    subtitle="City, Country",
    style="modern",
)
for overlay in overlays:
    overlay.start_time = 2.0
    overlay.duration = 4.0
```

### 3. Beat-Synced Captions
```python
captions = ["Word 1", "Word 2", "Word 3"]
beat_times = [0.5, 1.5, 2.5]
overlays = renderer.create_beat_synced_captions(captions, beat_times)
result = renderer.apply_multiple_overlays(clip, overlays)
```

### 4. Auto-Placed Text
```python
frame = clip.get_frame(0)
position = renderer.auto_place_text(frame, "Auto Text", "bottom")
overlay = TextOverlay(text="Auto Text", position=position)
```

### 5. Multiple Overlays
```python
overlays = [
    TextOverlay(text="First", start_time=0, duration=2),
    TextOverlay(text="Second", start_time=1.5, duration=2),
    TextOverlay(text="Third", start_time=3, duration=2),
]
result = renderer.apply_multiple_overlays(clip, overlays)
```

## Styling Options

### Font Configuration
```python
overlay = TextOverlay(
    text="Custom Font",
    font="Arial-Bold",  # or path to .ttf file
    font_size=64,
)
```

### Colors
```python
overlay = TextOverlay(
    text="Colored Text",
    color=(255, 215, 0),  # Gold RGB
    background_color=(0, 0, 0, 180),  # Black RGBA (semi-transparent)
)
```

### Shadow Effects
```python
overlay = TextOverlay(
    text="Shadowed Text",
    shadow=True,
    shadow_color=(0, 0, 0),
    shadow_offset=(4, 4),  # pixels
)
```

### Alignment
```python
# Left-aligned at 10% from left edge
overlay = TextOverlay(
    text="Left",
    position=(0.1, 0.5),
    align="left",
)

# Center-aligned
overlay = TextOverlay(
    text="Center",
    position=(0.5, 0.5),
    align="center",
)

# Right-aligned at 90% from left edge
overlay = TextOverlay(
    text="Right",
    position=(0.9, 0.5),
    align="right",
)
```

## Safe Zones

Predefined areas for optimal text placement:

| Zone | Y Range | X Range | Use Case |
|------|---------|---------|----------|
| `top` | 0.05-0.20 | 0.05-0.95 | Titles |
| `bottom` | 0.80-0.95 | 0.05-0.95 | Subtitles/captions |
| `center` | 0.40-0.60 | 0.10-0.90 | Main content |
| `lower_third` | 0.75-0.90 | 0.05-0.70 | Name/location |

## Lower Third Styles

### Modern
- Dark backgrounds with transparency
- Slide-left animation
- Left-aligned text
- Professional appearance

```python
overlays = renderer.create_lower_third(
    title="John Doe",
    subtitle="Professional Pilot",
    style="modern",
)
```

### Minimal
- No background
- Fade animations
- Center-aligned
- Clean and elegant

```python
overlays = renderer.create_lower_third(
    title="Beautiful Location",
    style="minimal",
)
```

### Bold
- High contrast backgrounds
- Gold/yellow title color
- Pop animations
- Maximum impact

```python
overlays = renderer.create_lower_third(
    title="EPIC MOMENT",
    subtitle="Once in a lifetime",
    style="bold",
)
```

## Position Coordinate System

Positions use normalized coordinates (0.0 to 1.0):

```
(0.0, 0.0) = Top-left corner
(0.5, 0.5) = Center
(1.0, 1.0) = Bottom-right corner

Position = (x_normalized, y_normalized)
```

### Common Positions
```python
TOP_LEFT = (0.1, 0.1)
TOP_CENTER = (0.5, 0.1)
TOP_RIGHT = (0.9, 0.1)
CENTER = (0.5, 0.5)
BOTTOM_LEFT = (0.1, 0.9)
BOTTOM_CENTER = (0.5, 0.9)
BOTTOM_RIGHT = (0.9, 0.9)
```

## Timing

### Start Time and Duration
```python
overlay = TextOverlay(
    text="Timed Text",
    start_time=2.5,  # Appears at 2.5 seconds
    duration=3.0,    # Visible for 3 seconds (ends at 5.5s)
)
```

### Animation Duration
```python
overlay = TextOverlay(
    text="Quick Animation",
    animation_in=TextAnimation.FADE_IN,
    animation_out=TextAnimation.FADE_OUT,
    animation_duration=0.2,  # Fast fade
)
```

## Performance Tips

1. **Font Caching:** Fonts are automatically cached; reuse font names when possible
2. **Multiple Overlays:** Use `apply_multiple_overlays()` for better performance
3. **Frame Analysis:** Auto-placement analyzes one frame; use sparingly
4. **Animation Duration:** Shorter durations (0.2-0.4s) feel snappier

## Troubleshooting

### Text Not Appearing
- Check `start_time` and `duration` relative to clip length
- Verify `position` is within 0.0-1.0 range
- Ensure text color contrasts with background

### Font Issues
```python
# Fallback to system fonts
overlay = TextOverlay(
    text="Safe Font",
    font="Arial-Bold",  # Cross-platform
)
```

### Text Cut Off
```python
# Use safe zones
position = renderer.auto_place_text(frame, text, "bottom")
```

### Performance Issues
```python
# Cache renderer instance
renderer = TextRenderer()  # Create once

# Reuse for multiple operations
result1 = renderer.apply_overlay_to_clip(clip1, overlay1)
result2 = renderer.apply_overlay_to_clip(clip2, overlay2)
```

## Examples

### Complete Workflow
```python
from pathlib import Path
from moviepy import VideoFileClip
from drone_reel.core.text_overlay import (
    TextAnimation,
    TextOverlay,
    TextRenderer,
)

def add_text_to_video(video_path: Path, output_path: Path):
    """Add animated text overlay to video."""
    # Initialize
    renderer = TextRenderer()
    clip = VideoFileClip(str(video_path))

    # Create overlays
    title = TextOverlay(
        text="Amazing Drone Shots",
        position=(0.5, 0.1),
        font_size=72,
        animation_in=TextAnimation.POP,
        start_time=0.5,
        duration=3.0,
    )

    lower_thirds = renderer.create_lower_third(
        title="Iceland",
        subtitle="Land of Fire and Ice",
        style="modern",
    )
    for overlay in lower_thirds:
        overlay.start_time = 4.0
        overlay.duration = 4.0

    # Apply all overlays
    all_overlays = [title] + lower_thirds
    result = renderer.apply_multiple_overlays(clip, all_overlays)

    # Save
    result.write_videofile(
        str(output_path),
        codec="libx264",
        audio_codec="aac",
    )

    # Cleanup
    clip.close()
    result.close()

# Usage
add_text_to_video(Path("input.mp4"), Path("output.mp4"))
```

## API Reference Summary

### TextAnimation (Enum)
- 10 animation types for text entrance/exit

### TextOverlay (Dataclass)
- Complete text configuration
- Position, styling, timing, animation

### TextRenderer (Class)

**Methods:**
- `render_text_frame(frame, overlay, progress)` - Render to single frame
- `apply_overlay_to_clip(clip, overlay)` - Apply to video
- `apply_multiple_overlays(clip, overlays)` - Apply multiple
- `auto_place_text(frame, text, zone)` - Smart placement
- `create_lower_third(title, subtitle, style)` - Template
- `create_beat_synced_captions(captions, beats, duration)` - Sync to music

**Properties:**
- `SAFE_ZONES` - Predefined safe areas

## See Also

- Full documentation: `/Users/matthewdeane/Documents/Data Science/python/_projects/_p-ai-drone-video/src/drone_reel/core/text_overlay.py`
- Examples: `/Users/matthewdeane/Documents/Data Science/python/_projects/_p-ai-drone-video/examples/text_overlay_demo.py`
- Tests: `/Users/matthewdeane/Documents/Data Science/python/_projects/_p-ai-drone-video/tests/test_text_overlay.py`
