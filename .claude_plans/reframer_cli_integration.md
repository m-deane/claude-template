# Reframer CLI Integration Guide

## New Reframe Modes Available

The enhanced reframer adds three new modes to the existing CLI:

```bash
drone-reel reframe [OPTIONS] INPUT OUTPUT
```

### Available Modes

| Mode | Description | Best For |
|------|-------------|----------|
| `center` | Simple center crop | Static subjects, basic use |
| `smart` | AI saliency with drone optimizations | General drone footage (DEFAULT) |
| `pan` | Smooth left-to-right pan | Landscape reveals, wide scenes |
| `thirds` | Rule of thirds composition | Artistic framing |
| `custom` | Manual focal point | Precise control needed |
| `horizon-lock` | Keep horizon level at upper third | Aerial shots with visible horizon |
| `face` | Track faces (fallback to saliency) | People-focused drone shots |
| `motion` | Track areas of highest motion | Action shots, moving subjects |

## Usage Examples

### Horizon Lock Mode
Perfect for aerial shots with visible horizon:
```bash
drone-reel reframe --mode horizon-lock \
  --output-width 1080 \
  input.mp4 output_vertical.mp4
```

### Face Tracking Mode
Ideal for drone shots with people:
```bash
drone-reel reframe --mode face \
  --output-width 1080 \
  drone_wedding.mp4 wedding_reel.mp4
```

### Motion Tracking Mode
Best for action sequences:
```bash
drone-reel reframe --mode motion \
  --output-width 1080 \
  drone_sports.mp4 sports_reel.mp4
```

### Optimized Smart Mode (Recommended)
Enhanced AI-based tracking with drone optimizations:
```bash
drone-reel reframe --mode smart \
  --output-width 1080 \
  drone_footage.mp4 social_reel.mp4
```

## Advanced Configuration via Code

For fine-tuned control, use the Python API:

### Example 1: Aggressive Sky Masking
```python
from drone_reel.core.reframer import Reframer, ReframeSettings, ReframeMode, AspectRatio

settings = ReframeSettings(
    mode=ReframeMode.SMART,
    target_ratio=AspectRatio.VERTICAL_9_16,
    output_width=1080,

    # Drone-specific optimizations
    sky_mask_enabled=True,
    sky_region_ratio=0.4,  # Mask top 40% (more aggressive)
    horizon_penalty_weight=0.8,  # Heavily penalize tilted horizons

    # Performance
    saliency_cache_frames=15,  # Cache longer for stable aerial shots
    scene_change_threshold=0.25,  # More sensitive scene change detection

    # Composition
    focal_clamp_x=(0.25, 0.75),  # Keep focal point more centered
    focal_clamp_y=(0.3, 0.9),  # Favor lower frame for ground subjects

    # Smoothing
    adaptive_smoothing=True,
    tracking_smoothness=0.25,  # Smoother base tracking
)

reframer = Reframer(settings)
reframer.reframe_video(input_path, output_path)
```

### Example 2: Custom Face Tracking
```python
from pathlib import Path

settings = ReframeSettings(
    mode=ReframeMode.FACE,
    face_cascade_path=Path("/path/to/custom/cascade.xml"),  # Optional
    adaptive_smoothing=True,
    tracking_smoothness=0.35,
)

reframer = Reframer(settings)
reframer.reframe_video(input_path, output_path)
```

### Example 3: High-Performance Motion Tracking
```python
settings = ReframeSettings(
    mode=ReframeMode.MOTION,

    # Tighter focal point constraints
    focal_clamp_x=(0.3, 0.7),
    focal_clamp_y=(0.3, 0.7),

    # Fast adaptive smoothing for action
    adaptive_smoothing=True,
    tracking_smoothness=0.4,  # Higher for less lag
)

reframer = Reframer(settings)
reframer.reframe_video(input_path, output_path)
```

### Example 4: Horizon Lock with Custom Settings
```python
settings = ReframeSettings(
    mode=ReframeMode.HORIZON_LOCK,
    smooth_tracking=True,
    tracking_smoothness=0.2,  # Very smooth horizon stabilization
)

reframer = Reframer(settings)
reframer.reframe_video(input_path, output_path)
```

## Mode Selection Guide

### When to Use Each Mode

**HORIZON_LOCK**
- Aerial landscape shots
- Ocean/water scenes
- Mountain/valley footage
- Any shot where horizon should be visible and level

**FACE**
- Wedding drone shots
- Event coverage with people
- Real estate tours with agents
- Travel vlogs

**MOTION**
- Sports footage (surfing, skiing, biking)
- Vehicle tracking shots
- Wildlife in motion
- Action sequences

**SMART (Enhanced)**
- General-purpose drone footage
- Mixed scenes (people + landscape)
- When you're not sure what content dominates
- Best balance of performance and quality

**CENTER**
- Simple, predictable framing
- Pre-composed shots
- When processing speed is critical

**PAN**
- Establishing shots of landscapes
- Slow reveals
- When you want controlled left-to-right motion

## Performance Considerations

### Computational Cost (Relative)

| Mode | Speed | Quality | CPU Usage |
|------|-------|---------|-----------|
| CENTER | Fastest | Basic | Minimal |
| PAN | Fastest | Basic | Minimal |
| SMART | Medium | Excellent | Moderate |
| THIRDS | Medium | Good | Moderate |
| HORIZON_LOCK | Medium | Good | Moderate |
| FACE | Slower | Excellent | High |
| MOTION | Slowest | Excellent | Very High |

### Optimization Tips

1. **Use saliency caching** (enabled by default)
   - Set `saliency_cache_frames=15-20` for stable drone shots

2. **Adjust scene change threshold**
   - Lower for frequent cuts: `scene_change_threshold=0.2`
   - Higher for stable scenes: `scene_change_threshold=0.4`

3. **Disable sky masking for non-aerial shots**
   - Set `sky_mask_enabled=False` for ground-level footage

4. **Use CENTER mode for previews**
   - Fast processing for rough cuts
   - Switch to SMART/FACE/MOTION for final export

## Integration with Other Drone-Reel Features

### Combined with Color Grading
```python
from drone_reel.core.reframer import create_vertical_reframer, ReframeMode
from drone_reel.core.color_grader import ColorGrader, PRESETS

# Create reframer
reframer = create_vertical_reframer(mode=ReframeMode.SMART)

# Reframe first
reframed_path = reframer.reframe_video(input_path, temp_path)

# Then color grade
grader = ColorGrader(PRESETS['vibrant'])
grader.grade_video(reframed_path, output_path)
```

### Combined with Scene Detection
```python
from drone_reel.core.scene_detector import SceneDetector
from drone_reel.core.reframer import Reframer, ReframeSettings, ReframeMode

# Detect scenes
detector = SceneDetector()
scenes = detector.detect_scenes(input_path)

# Reframe each scene separately
settings = ReframeSettings(mode=ReframeMode.SMART)
reframer = Reframer(settings)

for i, (start, end) in enumerate(scenes):
    # Extract scene
    scene_clip = video.subclipped(start, end)

    # Reset tracking for each scene
    reframer.reset_tracking()

    # Reframe
    scene_output = f"scene_{i:03d}_reframed.mp4"
    reframer.reframe_video(scene_clip, scene_output)
```

## Troubleshooting

### Face Detection Not Working
```bash
# Install opencv-contrib-python if missing
pip install opencv-contrib-python
```

### Horizon Detection Unreliable
- Try adjusting scene to have clearer horizon
- Use SMART mode instead with `horizon_penalty_weight=0.0`
- Ensure horizon is visible in middle 60% of frame

### Motion Tracking Jittery
- Increase `tracking_smoothness` to 0.5-0.7
- Enable `adaptive_smoothing=True`
- Reduce camera shake in original footage

### Slow Performance
- Increase `saliency_cache_frames` to 20-30
- Lower `output_width` to 720 for faster processing
- Use CENTER or PAN mode for previews
- Process in chunks with scene detection

## API Reference Quick Guide

### ReframeSettings Parameters

```python
# Target aspect ratio
target_ratio: AspectRatio = VERTICAL_9_16  # or SQUARE_1_1, LANDSCAPE_16_9, etc.

# Reframing mode
mode: ReframeMode = SMART  # center, smart, pan, thirds, custom, horizon_lock, face, motion

# Output dimensions
output_width: int = 1080  # Height calculated from aspect ratio

# Focal point control
focal_clamp_x: tuple[float, float] = (0.2, 0.8)  # X bounds (0-1)
focal_clamp_y: tuple[float, float] = (0.2, 0.8)  # Y bounds (0-1)

# Tracking behavior
smooth_tracking: bool = True
tracking_smoothness: float = 0.3  # 0=instant, 1=frozen
adaptive_smoothing: bool = True  # Auto-adjust based on velocity

# Drone-specific optimizations
sky_mask_enabled: bool = True
sky_region_ratio: float = 0.35  # Top portion to mask (0-1)
horizon_penalty_weight: float = 0.5  # 0=no penalty, 1=max penalty

# Performance tuning
saliency_cache_frames: int = 10  # Frames between recompute
scene_change_threshold: float = 0.3  # 0=always change, 1=never change

# Face detection (FACE mode only)
face_cascade_path: Optional[str] = None  # Auto-detect if None
```

### Reframer Methods

```python
# Calculate output dimensions
width, height = reframer.calculate_output_dimensions(input_w, input_h)

# Process entire video
output_path = reframer.reframe_video(
    input_path,
    output_path,
    progress_callback=lambda p: print(f"{p*100:.1f}%")
)

# Process single frame
reframed_frame = reframer.reframe_frame(
    frame,
    frame_index=0,
    total_frames=100
)

# Reset tracking state
reframer.reset_tracking()
```

## Real-World Example Workflows

### Workflow 1: Instagram Reel from Drone Footage
```bash
# 1. Reframe to vertical
drone-reel reframe --mode smart input_drone.mp4 vertical.mp4

# 2. Add music sync (if using beat-sync feature)
drone-reel sync vertical.mp4 music.mp3 final_reel.mp4

# 3. Color grade
drone-reel grade --preset vibrant final_reel.mp4 instagram_reel.mp4
```

### Workflow 2: Multiple Clip Compilation
```python
from pathlib import Path
from drone_reel.core.reframer import Reframer, ReframeSettings, ReframeMode

clips = list(Path("drone_clips/").glob("*.mp4"))
settings = ReframeSettings(mode=ReframeMode.SMART)
reframer = Reframer(settings)

for clip_path in clips:
    output_path = Path("reframed") / f"{clip_path.stem}_vertical.mp4"
    reframer.reset_tracking()  # Reset between clips
    reframer.reframe_video(clip_path, output_path)
```

### Workflow 3: Adaptive Mode Selection
```python
from drone_reel.core.reframer import Reframer, ReframeSettings, ReframeMode

def select_mode(clip_metadata):
    """Select best mode based on metadata."""
    if clip_metadata.get('has_people'):
        return ReframeMode.FACE
    elif clip_metadata.get('has_horizon'):
        return ReframeMode.HORIZON_LOCK
    elif clip_metadata.get('is_action'):
        return ReframeMode.MOTION
    else:
        return ReframeMode.SMART

# Process with adaptive mode
mode = select_mode(metadata)
settings = ReframeSettings(mode=mode)
reframer = Reframer(settings)
reframer.reframe_video(input_path, output_path)
```
