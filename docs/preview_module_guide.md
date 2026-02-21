# Preview Module Developer Guide

## Overview

The `drone_reel.core.preview` module provides professional thumbnail generation and video preview capabilities for the drone-reel video editing pipeline.

## Quick Start

```python
from drone_reel.core import (
    ThumbnailGenerator,
    ThumbnailStyle,
    PreviewGenerator
)
from pathlib import Path

# Initialize generators
thumb_gen = ThumbnailGenerator()
preview_gen = PreviewGenerator(preview_scale=0.25, preview_fps=15)
```

## ThumbnailGenerator

### Class: `ThumbnailGenerator`

Generates high-quality thumbnails from video scenes using advanced visual analysis.

#### Methods

##### `generate(scenes, output_path, style, size, text=None)`

Generate a thumbnail from video scenes.

**Parameters:**
- `scenes` (list[SceneInfo]): Scenes to select from
- `output_path` (Path): Output path for thumbnail image
- `style` (ThumbnailStyle): Thumbnail style (HERO, COMPOSITE, TEXT_OVERLAY)
- `size` (tuple[int, int]): Output size as (width, height)
- `text` (str, optional): Text for TEXT_OVERLAY style

**Returns:** Path to generated thumbnail

**Example:**
```python
thumbnail_path = thumb_gen.generate(
    scenes=detected_scenes,
    output_path=Path("output/thumbnail.jpg"),
    style=ThumbnailStyle.HERO,
    size=(1080, 1920),
)
```

##### `select_best_frame(scene, criteria="composition")`

Select the best single frame from a scene.

**Parameters:**
- `scene` (SceneInfo): Scene to extract from
- `criteria` (str): Selection criteria - "composition", "color", or "sharpness"

**Returns:** Best frame as numpy array (BGR)

**Example:**
```python
best_frame = thumb_gen.select_best_frame(
    scene=scene,
    criteria="composition"
)
```

##### `score_thumbnail_potential(frame)`

Score a frame's suitability as a thumbnail (0-100).

**Scoring Factors:**
- Composition (rule of thirds): 30%
- Color saturation: 25%
- Sharpness: 25%
- Focal point clarity: 20%

**Example:**
```python
score = thumb_gen.score_thumbnail_potential(frame)
print(f"Thumbnail score: {score}/100")
```

##### `create_composite_thumbnail(scenes, grid_size=(2,2), output_size=(1080,1080))`

Create a grid composite of multiple scenes.

**Example:**
```python
composite = thumb_gen.create_composite_thumbnail(
    scenes=scenes[:4],
    grid_size=(2, 2),
    output_size=(1080, 1080)
)
```

##### `add_text_to_thumbnail(image, text, position="bottom", style="bold")`

Add text overlay to an image.

**Parameters:**
- `image` (np.ndarray): Input image (BGR)
- `text` (str): Text to add
- `position` (str): "top", "bottom", or "center"
- `style` (str): "bold", "outlined", or "shadowed"

**Example:**
```python
with_text = thumb_gen.add_text_to_thumbnail(
    image=thumbnail,
    text="Epic Drone Adventure",
    position="bottom",
    style="bold"
)
```

### Enum: `ThumbnailStyle`

Available thumbnail styles:

- `HERO`: Single best frame from all scenes
- `COMPOSITE`: Grid layout of multiple frames
- `TEXT_OVERLAY`: Best frame with text overlay

## PreviewGenerator

### Class: `PreviewGenerator(preview_scale=0.25, preview_fps=15)`

Generate quick preview videos and storyboards for rapid iteration.

**Parameters:**
- `preview_scale` (float): Resolution scale factor (0.0-1.0)
- `preview_fps` (int): Frame rate for preview videos

#### Methods

##### `generate_preview(segments, output_path, include_transitions=True)`

Generate a low-resolution preview video.

**Parameters:**
- `segments` (list[ClipSegment]): Segments to preview
- `output_path` (Path): Output path for preview video
- `include_transitions` (bool): Whether to include transitions

**Example:**
```python
preview_path = preview_gen.generate_preview(
    segments=clip_segments,
    output_path=Path("output/preview.mp4"),
    include_transitions=True
)
```

##### `generate_storyboard(segments, output_path, frames_per_segment=3, grid_columns=4)`

Generate a storyboard grid image.

**Parameters:**
- `segments` (list[ClipSegment]): Segments to show
- `output_path` (Path): Output path for storyboard image
- `frames_per_segment` (int): Frames to extract per segment
- `grid_columns` (int): Number of columns in grid

**Example:**
```python
storyboard_path = preview_gen.generate_storyboard(
    segments=clip_segments,
    output_path=Path("output/storyboard.jpg"),
    frames_per_segment=3,
    grid_columns=4
)
```

##### `estimate_preview_time(segments)`

Estimate time to generate preview in seconds.

**Example:**
```python
estimated_seconds = preview_gen.estimate_preview_time(segments)
print(f"Preview will take ~{estimated_seconds:.1f} seconds")
```

##### `create_comparison(original, edited, output_path, mode="side_by_side")`

Create before/after comparison video.

**Parameters:**
- `original` (Path): Original video path
- `edited` (Path): Edited video path
- `output_path` (Path): Output comparison video path
- `mode` (str): "side_by_side", "overlay", or "split"

**Example:**
```python
comparison_path = preview_gen.create_comparison(
    original=Path("original.mp4"),
    edited=Path("edited.mp4"),
    output_path=Path("comparison.mp4"),
    mode="side_by_side"
)
```

## Common Workflows

### Workflow 1: Generate Social Media Thumbnail

```python
from drone_reel.core import (
    SceneDetector,
    ThumbnailGenerator,
    ThumbnailStyle
)
from pathlib import Path

# Detect scenes
detector = SceneDetector()
scenes = detector.detect_scenes(Path("drone_footage.mp4"))

# Generate Instagram-style thumbnail
thumb_gen = ThumbnailGenerator()
thumb_gen.generate(
    scenes=scenes,
    output_path=Path("instagram_thumb.jpg"),
    style=ThumbnailStyle.HERO,
    size=(1080, 1920),  # Instagram portrait
)

# Generate YouTube thumbnail with text
thumb_gen.generate(
    scenes=scenes,
    output_path=Path("youtube_thumb.jpg"),
    style=ThumbnailStyle.TEXT_OVERLAY,
    size=(1920, 1080),  # YouTube landscape
    text="EPIC DRONE FOOTAGE"
)
```

### Workflow 2: Quick Preview Before Full Render

```python
from drone_reel.core import (
    VideoProcessor,
    PreviewGenerator
)
from pathlib import Path

# Create clip segments
processor = VideoProcessor()
segments = processor.create_segments_from_scenes(
    scenes=top_scenes,
    clip_durations=[2.0] * len(top_scenes)
)

# Generate quick preview
preview_gen = PreviewGenerator(preview_scale=0.25, preview_fps=15)

# Estimate time
est_time = preview_gen.estimate_preview_time(segments)
print(f"Preview will take ~{est_time:.1f}s")

# Generate preview
preview_path = preview_gen.generate_preview(
    segments=segments,
    output_path=Path("preview.mp4"),
    include_transitions=True
)

# Generate storyboard for review
storyboard_path = preview_gen.generate_storyboard(
    segments=segments,
    output_path=Path("storyboard.jpg"),
    frames_per_segment=3
)

print(f"Preview: {preview_path}")
print(f"Storyboard: {storyboard_path}")
```

### Workflow 3: A/B Testing Thumbnails

```python
from drone_reel.core import ThumbnailGenerator, ThumbnailStyle
from pathlib import Path

thumb_gen = ThumbnailGenerator()
output_dir = Path("thumbnails")
output_dir.mkdir(exist_ok=True)

# Generate multiple variations
styles = [
    (ThumbnailStyle.HERO, "hero.jpg"),
    (ThumbnailStyle.COMPOSITE, "composite.jpg"),
    (ThumbnailStyle.TEXT_OVERLAY, "text.jpg"),
]

for style, filename in styles:
    thumb_gen.generate(
        scenes=scenes,
        output_path=output_dir / filename,
        style=style,
        size=(1080, 1920),
        text="Amazing Footage" if style == ThumbnailStyle.TEXT_OVERLAY else None
    )

# Score individual frames
for i, scene in enumerate(scenes[:5]):
    frame = thumb_gen.select_best_frame(scene)
    score = thumb_gen.score_thumbnail_potential(frame)
    print(f"Scene {i}: Thumbnail score = {score:.1f}/100")
```

### Workflow 4: Before/After Comparison

```python
from drone_reel.core import PreviewGenerator
from pathlib import Path

preview_gen = PreviewGenerator(preview_scale=0.5, preview_fps=30)

# Create all comparison modes
modes = ["side_by_side", "overlay", "split"]

for mode in modes:
    preview_gen.create_comparison(
        original=Path("original.mp4"),
        edited=Path("edited.mp4"),
        output_path=Path(f"comparison_{mode}.mp4"),
        mode=mode
    )
```

## Performance Tips

1. **Thumbnail Generation:**
   - Use HERO style for fastest generation (single frame)
   - COMPOSITE is slower (multiple frame extractions)
   - Cache thumbnails to avoid regeneration

2. **Preview Generation:**
   - Lower `preview_scale` = faster generation (try 0.25)
   - Lower `preview_fps` = faster generation (try 10-15 FPS)
   - Set `include_transitions=False` for quickest preview

3. **Storyboard Generation:**
   - Reduce `frames_per_segment` for faster generation
   - Larger `grid_columns` = more compact output

## Error Handling

All methods raise informative exceptions:

```python
from drone_reel.core import ThumbnailGenerator
from pathlib import Path

try:
    thumb_gen = ThumbnailGenerator()
    thumb_gen.generate(
        scenes=[],  # Empty list
        output_path=Path("thumb.jpg"),
    )
except ValueError as e:
    print(f"Invalid input: {e}")
except RuntimeError as e:
    print(f"Processing failed: {e}")
```

Common errors:
- `ValueError`: Invalid parameters (empty scenes, invalid scale, etc.)
- `RuntimeError`: Processing failures (video read errors, encoding issues)

## Best Practices

1. **Always validate scenes before generation:**
   ```python
   if not scenes:
       raise ValueError("No scenes available for thumbnail")
   ```

2. **Use context managers when possible:**
   ```python
   # Clips are automatically cleaned up
   preview_gen.generate_preview(segments, output_path)
   ```

3. **Check estimated time for large previews:**
   ```python
   est_time = preview_gen.estimate_preview_time(segments)
   if est_time > 60:
       print("Warning: Preview will take over 1 minute")
   ```

4. **Create output directories proactively:**
   ```python
   output_path.parent.mkdir(parents=True, exist_ok=True)
   ```

## Dependencies

- `opencv-python` (cv2): Video frame extraction and processing
- `numpy`: Array operations
- `Pillow` (PIL): Image manipulation and text rendering
- `moviepy`: Video clip handling and composition

## Module Structure

```
drone_reel.core.preview
├── ThumbnailStyle (Enum)
│   ├── HERO
│   ├── COMPOSITE
│   └── TEXT_OVERLAY
├── ThumbnailGenerator (Class)
│   ├── generate()
│   ├── select_best_frame()
│   ├── score_thumbnail_potential()
│   ├── create_composite_thumbnail()
│   └── add_text_to_thumbnail()
└── PreviewGenerator (Class)
    ├── generate_preview()
    ├── generate_storyboard()
    ├── estimate_preview_time()
    └── create_comparison()
```

## Testing

Run tests:
```bash
# All preview tests
pytest tests/test_preview.py -v

# Specific test class
pytest tests/test_preview.py::TestThumbnailGenerator -v

# With coverage
pytest tests/test_preview.py --cov=src/drone_reel/core/preview
```

## Further Reading

- [MoviePy Documentation](https://zulko.github.io/moviepy/)
- [OpenCV Python Tutorials](https://docs.opencv.org/master/d6/d00/tutorial_py_root.html)
- [Pillow Documentation](https://pillow.readthedocs.io/)
