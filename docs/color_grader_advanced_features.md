# Advanced Color Grader Features

Comprehensive guide to the enhanced ColorGrader functionality in drone-reel.

## Table of Contents

1. [LUT Support](#lut-support)
2. [Tone Curves](#tone-curves)
3. [Selective Color Adjustments](#selective-color-adjustments)
4. [Improved Shadows/Highlights](#improved-shadowshighlights)
5. [Enhanced Film Grain](#enhanced-film-grain)
6. [GPU Acceleration](#gpu-acceleration)
7. [Preview Mode](#preview-mode)
8. [Complete Workflow Examples](#complete-workflow-examples)

---

## LUT Support

Load and apply 3D LUTs (Look-Up Tables) in .cube format for professional color grading.

### Features

- Parses standard .cube LUT files
- Trilinear interpolation for smooth color transitions
- Combines seamlessly with other adjustments
- Supports any LUT size (typically 17x17x17 or 33x33x33)

### Usage

```python
from pathlib import Path
from drone_reel.core.color_grader import ColorGrader

# Load and apply a LUT
grader = ColorGrader(lut_path=Path('cinematic.cube'))
result = grader.grade_frame(frame)
```

### Creating a LUT File

```python
# Example .cube file format
# cinematic.cube
LUT_3D_SIZE 17

# RGB values (0.0 to 1.0)
0.0 0.0 0.0
0.1 0.05 0.03
...
```

### Combining LUT with Adjustments

```python
from drone_reel.core.color_grader import ColorAdjustments

adjustments = ColorAdjustments(
    brightness=5,
    contrast=10,
)

grader = ColorGrader(
    lut_path=Path('my_lut.cube'),
    adjustments=adjustments
)
```

---

## Tone Curves

Create custom tonal mappings using control points with cubic spline interpolation.

### Features

- Per-channel RGB curves
- Cubic spline interpolation for smooth curves
- Control point-based interface
- Excellent for contrast and color grading

### Basic Usage

```python
from drone_reel.core.color_grader import ColorGrader, ToneCurve

# Create an S-curve for contrast
tone_curve = ToneCurve(
    red_points=[(0, 0), (64, 45), (192, 210), (255, 255)],
    green_points=[(0, 0), (64, 45), (192, 210), (255, 255)],
    blue_points=[(0, 0), (64, 45), (192, 210), (255, 255)],
)

grader = ColorGrader(tone_curve=tone_curve)
result = grader.grade_frame(frame)
```

### Common Curve Patterns

#### S-Curve (Enhanced Contrast)
```python
ToneCurve(
    red_points=[(0, 0), (64, 45), (192, 210), (255, 255)],
    green_points=[(0, 0), (64, 45), (192, 210), (255, 255)],
    blue_points=[(0, 0), (64, 45), (192, 210), (255, 255)],
)
```

#### Warm Look
```python
ToneCurve(
    red_points=[(0, 0), (128, 140), (255, 255)],    # Boost reds
    green_points=[(0, 0), (128, 128), (255, 245)],  # Slight green
    blue_points=[(0, 0), (128, 115), (255, 230)],   # Reduce blues
)
```

#### Fade (Lifted Blacks)
```python
ToneCurve(
    red_points=[(0, 30), (128, 128), (255, 255)],   # Lift shadows
    green_points=[(0, 30), (128, 128), (255, 255)],
    blue_points=[(0, 30), (128, 128), (255, 255)],
)
```

### Per-Channel Color Grading

```python
# Create different curves for each channel
tone_curve = ToneCurve(
    red_points=[(0, 0), (128, 145), (255, 255)],   # More red in midtones
    green_points=[(0, 0), (128, 125), (255, 250)], # Less green overall
    blue_points=[(0, 0), (128, 110), (255, 235)],  # Significantly less blue
)

grader = ColorGrader(tone_curve=tone_curve)
```

---

## Selective Color Adjustments

Target specific color ranges (red, orange, yellow, green, cyan, blue, purple, magenta) with independent hue, saturation, and luminance controls.

### Features

- 8 color ranges: red, orange, yellow, green, cyan, blue, purple, magenta
- Independent hue, saturation, and luminance adjustments per range
- Uses HSV and LAB color spaces for accurate targeting
- Minimal impact on adjacent colors

### Usage

```python
from drone_reel.core.color_grader import (
    ColorAdjustments,
    ColorGrader,
    SelectiveColorAdjustments,
)

# Create selective adjustments
selective = SelectiveColorAdjustments(
    # Boost skin tones (orange)
    orange_sat=25,
    orange_lum=5,

    # Enhance skies (blue/cyan)
    blue_sat=15,
    cyan_sat=10,

    # Enrich foliage (green)
    green_sat=20,
    green_hue=-5,  # Shift towards cyan for natural look
)

adjustments = ColorAdjustments(selective_color=selective)
grader = ColorGrader(adjustments=adjustments)

result = grader.grade_frame(frame)
```

### Color Ranges

| Color Range | Hue Range (degrees) | Typical Use Cases |
|-------------|---------------------|-------------------|
| Red | 0-15, 345-360 | Fire, red clothing, stop signs |
| Orange | 16-45 | Skin tones, sunset, warm tones |
| Yellow | 46-75 | Sun, yellow flowers, golden hour |
| Green | 76-165 | Foliage, grass, nature |
| Cyan | 166-195 | Ocean, cyan skies, cool tones |
| Blue | 196-255 | Sky, water, blue objects |
| Purple | 256-285 | Purple flowers, twilight |
| Magenta | 286-344 | Magenta tones, creative looks |

### Common Adjustments

#### Enhance Skin Tones
```python
SelectiveColorAdjustments(
    orange_sat=20,  # More vibrant
    orange_lum=5,   # Slightly brighter
)
```

#### Teal and Orange Look
```python
SelectiveColorAdjustments(
    orange_sat=30,
    orange_hue=5,
    cyan_sat=25,
    blue_hue=10,
)
```

#### Natural Foliage Enhancement
```python
SelectiveColorAdjustments(
    green_sat=25,
    green_hue=-8,      # Shift towards cyan
    yellow_sat=15,     # Enhance yellow-green
    yellow_hue=5,
)
```

---

## Improved Shadows/Highlights

Enhanced shadow and highlight adjustments using LAB color space for superior color preservation.

### Why LAB Color Space?

- Separates luminance (L) from color (A, B)
- Better preserves color when adjusting tones
- Reduces color shifts in shadows and highlights
- More natural-looking results

### Usage

```python
from drone_reel.core.color_grader import ColorAdjustments, ColorGrader

adjustments = ColorAdjustments(
    shadows=40,      # Lift shadows (range: -100 to 100)
    highlights=-30,  # Recover highlights (range: -100 to 100)
)

grader = ColorGrader(adjustments=adjustments)
result = grader.grade_frame(frame)
```

### Comparison: HSV vs LAB

```python
# Old implementation (HSV - removed)
# - Used V channel (value)
# - Color shifts when adjusting tones
# - Less control over color preservation

# New implementation (LAB)
# - Uses L channel (lightness)
# - Preserves color information
# - Professional-grade results
```

### Best Practices

- **Shadows**: Use positive values (10-50) to lift shadows
- **Highlights**: Use negative values (-10 to -40) to recover highlights
- **Combine with curves**: Use tone curves for overall contrast, shadows/highlights for fine-tuning
- **Don't overdo it**: Excessive adjustments can look unnatural

---

## Enhanced Film Grain

Professional film grain simulation with temporal coherence and film-like characteristics.

### Features

- **Temporal coherence**: Grain pattern changes between frames naturally
- **Lower resolution generation**: Generates noise at half resolution, upscales for authentic film look
- **Luminance-weighted**: Stronger in midtones, weaker in shadows/highlights (like real film)
- **Seeded randomness**: Same frame index produces same grain for consistency

### Usage

```python
from drone_reel.core.color_grader import ColorAdjustments, ColorGrader

adjustments = ColorAdjustments(
    grain=30,  # Range: 0-100
)

grader = ColorGrader(adjustments=adjustments)

# Process multiple frames with temporal coherence
for i, frame in enumerate(video_frames):
    result = grader.grade_frame(frame, frame_index=i)
```

### Grain Intensity Guide

| Value | Effect | Use Case |
|-------|--------|----------|
| 0-15 | Subtle | Minimal vintage feel |
| 15-30 | Light | Modern film look |
| 30-50 | Medium | Classic film aesthetic |
| 50-70 | Heavy | Strong vintage/retro |
| 70-100 | Extreme | Artistic/experimental |

### Technical Details

```python
# Grain implementation highlights:
# 1. Seed based on frame index for temporal coherence
np.random.seed(frame_index % 100000)

# 2. Generate at lower resolution
grain_h, grain_w = h // 2, w // 2
noise = np.random.normal(0, amount / 100 * 25, (grain_h, grain_w))

# 3. Upscale for film-like characteristics
noise_upscaled = cv2.resize(noise, (w, h), interpolation=cv2.INTER_LINEAR)

# 4. Weight by luminance (stronger in midtones)
midtone_mask = 1 - np.abs(luminance - 0.5) * 2
weighted_noise = noise_upscaled * midtone_mask
```

---

## GPU Acceleration

Optional GPU acceleration using CUDA for faster processing.

### Features

- Automatic GPU detection
- Graceful fallback to CPU
- Accelerated operations: brightness, contrast, basic transformations
- Complex operations (LUTs, curves) run on CPU even in GPU mode

### Usage

```python
from drone_reel.core.color_grader import ColorGrader

# Enable GPU if available
grader = ColorGrader(use_gpu=True)

# Check if GPU is being used
if grader.use_gpu:
    print("Using GPU acceleration")
else:
    print("GPU not available, using CPU")
```

### GPU vs CPU Performance

| Operation | GPU Speedup | Notes |
|-----------|-------------|-------|
| Brightness/Contrast | 2-5x | Simple arithmetic operations |
| Saturation/Color | Minimal | Requires color space conversions |
| LUT Application | No speedup | Complex indexing operations |
| Tone Curves | No speedup | Lookup table operations |

### Requirements

- OpenCV compiled with CUDA support
- NVIDIA GPU with CUDA capability
- Appropriate CUDA drivers installed

### When to Use GPU

- **Yes**: Processing large batches of high-resolution videos
- **Yes**: Real-time video processing
- **No**: Single frame processing
- **No**: When GPU isn't available (automatic fallback)

---

## Preview Mode

Fast preview rendering at reduced resolution for quick iteration.

### Features

- Configurable scale factor (default 25%)
- Applies all color grading operations
- Significantly faster than full resolution
- Perfect for tweaking settings

### Usage

```python
from drone_reel.core.color_grader import ColorGrader

grader = ColorGrader(adjustments=adjustments)

# Quick preview at 25% resolution
preview = grader.grade_frame_preview(frame, scale=0.25)

# Larger preview at 50% resolution
preview = grader.grade_frame_preview(frame, scale=0.5)

# Apply full resolution when satisfied
final = grader.grade_frame(frame)
```

### Typical Workflow

```python
# 1. Create your color grade
adjustments = ColorAdjustments(...)
tone_curve = ToneCurve(...)
grader = ColorGrader(adjustments=adjustments, tone_curve=tone_curve)

# 2. Iterate quickly with previews
for adjustment_value in range(0, 50, 5):
    adjustments.contrast = adjustment_value
    preview = grader.grade_frame_preview(test_frame, scale=0.25)
    # Display or save preview for review

# 3. Apply final grade at full resolution
for frame in video_frames:
    result = grader.grade_frame(frame)
```

### Performance Comparison

| Resolution | Scale | Processing Time | Speedup |
|------------|-------|-----------------|---------|
| 3840x2160 (4K) | 1.0 | 100 ms | 1x |
| 1920x1080 (1080p) | 0.5 | 25 ms | 4x |
| 960x540 | 0.25 | 6 ms | 16x |
| 480x270 | 0.125 | 1.5 ms | 64x |

---

## Complete Workflow Examples

### Example 1: Cinematic Drone Footage

```python
from pathlib import Path
from drone_reel.core.color_grader import (
    ColorAdjustments,
    ColorGrader,
    SelectiveColorAdjustments,
    ToneCurve,
)

# 1. Define selective color adjustments
selective = SelectiveColorAdjustments(
    blue_sat=20,      # Enhance sky
    cyan_sat=15,      # Boost ocean/water
    green_sat=10,     # Subtle foliage enhancement
    orange_sat=-5,    # Slightly desaturate warm tones
)

# 2. Create S-curve for contrast
tone_curve = ToneCurve(
    red_points=[(0, 0), (64, 50), (192, 205), (255, 255)],
    green_points=[(0, 0), (64, 48), (192, 207), (255, 255)],
    blue_points=[(0, 0), (64, 45), (192, 210), (255, 250)],
)

# 3. Define overall adjustments
adjustments = ColorAdjustments(
    brightness=3,
    contrast=15,
    saturation=-8,     # Slight desaturation for cinematic look
    temperature=5,     # Warm tone
    shadows=12,        # Lift shadows
    highlights=-8,     # Recover highlights
    fade=5,            # Subtle fade effect
    grain=15,          # Light film grain
    selective_color=selective,
)

# 4. Create grader with optional LUT
grader = ColorGrader(
    adjustments=adjustments,
    tone_curve=tone_curve,
    lut_path=Path('cinematic.cube'),  # Optional
    use_gpu=True,
)

# 5. Process video
for i, frame in enumerate(video_frames):
    graded_frame = grader.grade_frame(frame, frame_index=i)
```

### Example 2: Vintage Film Look

```python
# Vintage warm film aesthetic
selective = SelectiveColorAdjustments(
    red_hue=5,
    red_sat=15,
    yellow_sat=20,
    blue_sat=-30,    # Heavily desaturate blues
)

tone_curve = ToneCurve(
    # Lifted blacks, rolled highlights
    red_points=[(0, 25), (128, 135), (255, 240)],
    green_points=[(0, 20), (128, 130), (255, 235)],
    blue_points=[(0, 15), (128, 120), (255, 225)],
)

adjustments = ColorAdjustments(
    contrast=-10,      # Reduce contrast
    saturation=-25,    # Heavy desaturation
    temperature=20,    # Strong warm tone
    fade=25,           # Strong fade
    grain=40,          # Heavy grain
    selective_color=selective,
)

grader = ColorGrader(
    adjustments=adjustments,
    tone_curve=tone_curve,
)
```

### Example 3: Teal and Orange Blockbuster

```python
# Popular Hollywood color grade
selective = SelectiveColorAdjustments(
    orange_sat=35,
    orange_hue=5,
    red_sat=25,
    yellow_sat=20,
    cyan_sat=30,
    cyan_hue=-5,
    blue_sat=20,
    blue_hue=10,
)

tone_curve = ToneCurve(
    red_points=[(0, 0), (64, 55), (192, 200), (255, 255)],
    green_points=[(0, 0), (64, 50), (192, 205), (255, 255)],
    blue_points=[(0, 0), (64, 60), (192, 195), (255, 255)],
)

adjustments = ColorAdjustments(
    contrast=18,
    saturation=10,
    temperature=10,
    tint=-8,           # Slight green shift
    shadows=8,
    highlights=-12,
    selective_color=selective,
)

grader = ColorGrader(
    adjustments=adjustments,
    tone_curve=tone_curve,
)
```

### Example 4: Natural Documentary Style

```python
# Clean, natural look with subtle enhancements
selective = SelectiveColorAdjustments(
    green_sat=15,
    green_hue=-5,
    blue_sat=10,
    orange_sat=5,     # Subtle skin tone enhancement
)

tone_curve = ToneCurve(
    # Gentle S-curve
    red_points=[(0, 0), (64, 60), (192, 200), (255, 255)],
    green_points=[(0, 0), (64, 60), (192, 200), (255, 255)],
    blue_points=[(0, 0), (64, 60), (192, 200), (255, 255)],
)

adjustments = ColorAdjustments(
    brightness=2,
    contrast=8,
    saturation=5,
    shadows=10,
    highlights=-5,
    selective_color=selective,
)

grader = ColorGrader(
    adjustments=adjustments,
    tone_curve=tone_curve,
)
```

### Example 5: High-Performance Batch Processing

```python
import cv2
from pathlib import Path

# Setup for fast batch processing
grader = ColorGrader(
    preset=ColorPreset.DRONE_AERIAL,
    use_gpu=True,
)

input_dir = Path('input_videos')
output_dir = Path('output_videos')

for video_path in input_dir.glob('*.mp4'):
    print(f"Processing {video_path.name}")

    # Use preview to verify settings
    cap = cv2.VideoCapture(str(video_path))
    ret, first_frame = cap.read()
    cap.release()

    preview = grader.grade_frame_preview(first_frame, scale=0.25)
    cv2.imwrite(f'preview_{video_path.stem}.jpg', preview)

    # Process full video
    output_path = output_dir / f'graded_{video_path.name}'
    grader.grade_video(video_path, output_path)
```

---

## API Reference

### Classes

#### `ColorGrader`
Main color grading class with all features.

**Constructor Parameters:**
- `preset: ColorPreset` - Preset color grade (default: NONE)
- `adjustments: ColorAdjustments` - Manual adjustments
- `lut_path: Path` - Path to .cube LUT file
- `tone_curve: ToneCurve` - Tone curve adjustments
- `use_gpu: bool` - Enable GPU acceleration (default: False)

#### `ColorAdjustments`
Color adjustment parameters dataclass.

**Fields:**
- `brightness: float` (-100 to 100)
- `contrast: float` (-100 to 100)
- `saturation: float` (-100 to 100)
- `temperature: float` (-100 to 100)
- `tint: float` (-100 to 100)
- `shadows: float` (-100 to 100)
- `highlights: float` (-100 to 100)
- `vibrance: float` (-100 to 100)
- `fade: float` (0 to 100)
- `grain: float` (0 to 100)
- `selective_color: SelectiveColorAdjustments`

#### `SelectiveColorAdjustments`
Per-color adjustments dataclass.

**Fields (8 color ranges):**
- `{color}_hue: float` (-180 to 180)
- `{color}_sat: float` (-100 to 100)
- `{color}_lum: float` (-100 to 100)

Colors: red, orange, yellow, green, cyan, blue, purple, magenta

#### `ToneCurve`
Tone curve definition dataclass.

**Fields:**
- `red_points: list[tuple[float, float]]` - Red channel control points
- `green_points: list[tuple[float, float]]` - Green channel control points
- `blue_points: list[tuple[float, float]]` - Blue channel control points

### Methods

#### `ColorGrader.grade_frame(frame, frame_index=None)`
Apply color grading to a single frame.

**Parameters:**
- `frame: np.ndarray` - Input BGR frame
- `frame_index: int` - Optional frame index for temporal effects

**Returns:** `np.ndarray` - Graded BGR frame

#### `ColorGrader.grade_frame_preview(frame, scale=0.25)`
Apply color grading at reduced resolution.

**Parameters:**
- `frame: np.ndarray` - Input BGR frame
- `scale: float` - Scale factor (default: 0.25)

**Returns:** `np.ndarray` - Graded BGR frame at reduced resolution

#### `ColorGrader.load_lut(lut_path)`
Load a .cube LUT file.

**Parameters:**
- `lut_path: Path` - Path to .cube file

**Returns:** `np.ndarray` - 3D LUT array

#### `ColorGrader.apply_curve(frame)`
Apply tone curve to frame.

**Parameters:**
- `frame: np.ndarray` - Input BGR frame (float32)

**Returns:** `np.ndarray` - Frame with curve applied

---

## Performance Tips

1. **Use preview mode** for iterating on settings
2. **Enable GPU** for batch processing if available
3. **Load LUTs once** and reuse the grader instance
4. **Minimize selective color adjustments** for better performance
5. **Reduce grain amount** if processing time is critical
6. **Process in batches** when handling multiple videos

## Troubleshooting

### LUT Not Loading
- Verify .cube file format is correct
- Check LUT_3D_SIZE is specified
- Ensure correct number of entries (size^3)

### GPU Not Working
- Verify OpenCV has CUDA support: `cv2.cuda.getCudaEnabledDeviceCount()`
- Install opencv-contrib-python with CUDA
- Update GPU drivers

### Colors Look Wrong
- Check color space (should be BGR for OpenCV)
- Verify adjustment ranges (-100 to 100, etc.)
- Review selective color hue ranges

### Performance Issues
- Use preview mode for iteration
- Reduce frame resolution
- Disable grain for faster processing
- Use simpler tone curves (fewer control points)

---

## Resources

- [.cube LUT Format Specification](https://wwwimages.adobe.com/content/dam/acom/en/products/speedgrade/cc/pdfs/cube-lut-specification-1.0.pdf)
- [Color Grading Theory](https://en.wikipedia.org/wiki/Color_grading)
- [LAB Color Space](https://en.wikipedia.org/wiki/CIELAB_color_space)
- [Film Grain Characteristics](https://en.wikipedia.org/wiki/Film_grain)

---

## Credits

Enhanced ColorGrader implementation by the drone-reel team.
Built with OpenCV, NumPy, and SciPy.
