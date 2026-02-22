# Advanced Color Grader Features

Comprehensive guide to the enhanced ColorGrader functionality in drone-reel.

## Table of Contents

1. [Color Science Pipeline](#color-science-pipeline)
2. [D-Log / S-Log3 Normalization](#d-log--s-log3-normalization)
3. [Auto White Balance](#auto-white-balance)
4. [Auto Color Match](#auto-color-match)
5. [Noise Reduction](#noise-reduction)
6. [LUT Support](#lut-support)
7. [Tone Curves](#tone-curves)
8. [Selective Color Adjustments](#selective-color-adjustments)
9. [Improved Shadows/Highlights](#improved-shadowshighlights)
10. [Visual Effects](#visual-effects)
11. [Enhanced Film Grain](#enhanced-film-grain)
12. [GPU Acceleration](#gpu-acceleration)
13. [Preview Mode](#preview-mode)
14. [Complete Workflow Examples](#complete-workflow-examples)

---

## Color Science Pipeline

The ColorGrader processes frames through a carefully ordered pipeline. Understanding this order helps when combining features:

| Phase | Stage | Description |
|-------|-------|-------------|
| -2 | D-Log/S-Log normalization | Convert log-encoded footage to Rec.709 |
| -1 | Auto white balance | Gray world per-channel correction |
| -0.5 | Auto color match | Histogram CDF matching to reference frame |
| -0.25 | Noise reduction | Non-local means spatial denoising |
| 0 | LUT application | 3D LUT color transform |
| 0 | Tone curves | RGB spline curves |
| 0.5 | Shadow lift | LAB-space shadow/highlight recovery |
| 1 | Basic adjustments | Brightness, contrast (BGR) |
| 2 | HSV adjustments | Saturation, vibrance, temperature, tint |
| 3 | LAB adjustments | Shadows, highlights |
| 4 | Selective color | Per-color range hue/sat/lum |
| 4 | Fade | Black level lift |
| 4 | Film grain | Temporal organic noise |
| 5 | Vignette | Radial edge darkening |
| 6 | Halation | Warm highlight bloom |
| 7 | Chromatic aberration | RGB channel offset |
| 8 | Atmospheric haze | Vertical gradient fog |
| 9 | GND sky correction | Graduated neutral density |
| Final | Dithering | Bayer-matrix anti-banding |

Color correction stages (D-Log, AWB, denoise, color match) run before creative grading. Atmospheric effects run after all color work.

---

## D-Log / S-Log3 Normalization

Professional drone cameras (DJI, Sony) shoot in log color spaces for maximum dynamic range. The footage looks flat/washed out and must be normalized before grading.

### Supported Colorspaces

| Colorspace | Camera | Description |
|-----------|--------|-------------|
| `rec709` | Standard | No normalization (default) |
| `dlog` | DJI (generic) | DJI D-Log inverse curve |
| `dlog_m` | DJI Mini/Air/Mavic | DJI D-Log M linearization |
| `slog3` | Sony | Sony S-Log3 inverse curve |
| `auto` | Any | Auto-detect from histogram |

### CLI Usage

```bash
# Specify colorspace directly
drone-reel create -i ./clips/ --input-colorspace dlog_m --color drone_aerial

# Auto-detect log footage
drone-reel create -i ./clips/ --input-colorspace auto --color golden_hour
```

### Python API

```python
from drone_reel.core.color_grader import ColorGrader, ColorPreset

# DJI Mini 3 Pro footage
grader = ColorGrader(
    preset=ColorPreset.DRONE_AERIAL,
    input_colorspace="dlog_m",
)
result = grader.grade_frame(frame)

# Auto-detect
is_log = ColorGrader.detect_log_footage(Path("footage.mp4"))
# Returns "dlog" or "rec709"
```

---

## Auto White Balance

Gray world auto white balance corrects color casts by scaling each channel so its mean matches the overall frame mean.

### CLI Usage

```bash
drone-reel create -i ./clips/ --auto-wb --color drone_aerial
```

### Python API

```python
grader = ColorGrader(
    preset=ColorPreset.DRONE_AERIAL,
    auto_wb=True,
)
```

**Best for:** Mixed lighting conditions, indoor-outdoor transitions, correcting blue/orange casts from incorrect camera WB settings.

---

## Auto Color Match

Normalizes color distribution across clips by matching each frame's per-channel histogram CDF to a reference frame. This ensures consistent color across clips from different cameras or lighting conditions.

### CLI Usage

```bash
drone-reel create -i ./clips/ --auto-color-match --color cinematic
```

### Python API

```python
grader = ColorGrader(preset=ColorPreset.CINEMATIC)

# Set reference from first frame
reference_frame = get_first_frame(video_path)
grader.set_reference_frame(reference_frame)

# All subsequent frames will match reference color distribution
for frame in frames:
    graded = grader.grade_frame(frame)
```

**Best for:** Multi-camera shoots, inconsistent lighting between clips, ensuring uniform look across a reel.

---

## Noise Reduction

Spatial denoising using OpenCV's non-local means algorithm. Reduces sensor noise while preserving edges and detail.

### CLI Usage

```bash
# Subtle denoising
drone-reel create -i ./clips/ --denoise 0.3

# Strong denoising (high-ISO footage)
drone-reel create -i ./clips/ --denoise 0.8
```

### Python API

```python
grader = ColorGrader(
    denoise_strength=0.5,  # 0.0-1.0, maps to h=3-15 internally
)
```

### Strength Guide

| Value | Effect | Use Case |
|-------|--------|----------|
| 0.0-0.2 | Minimal | Clean footage, subtle smoothing |
| 0.2-0.5 | Moderate | Standard drone footage, slight noise |
| 0.5-0.8 | Strong | High-ISO, low-light footage |
| 0.8-1.0 | Heavy | Very noisy footage (detail loss expected) |

---

## LUT Support

Load and apply 3D LUTs (Look-Up Tables) in .cube format for professional color grading.

### Features

- Parses standard .cube LUT files
- Trilinear interpolation for smooth color transitions
- Combines seamlessly with other adjustments
- Supports any LUT size (typically 17x17x17 or 33x33x33)

### CLI Usage

```bash
drone-reel create -i ./clips/ --lut cinematic.cube
drone-reel create -i ./clips/ --lut my_grade.cube --color-intensity 0.5
```

### Python API

```python
from pathlib import Path
from drone_reel.core.color_grader import ColorGrader

# Load and apply a LUT
grader = ColorGrader(lut_path=Path('cinematic.cube'))
result = grader.grade_frame(frame)
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
    adjustments=adjustments,
    vignette_strength=0.3,
)
```

---

## Tone Curves

Create custom tonal mappings using control points with cubic spline interpolation.

### Features

- Per-channel RGB curves
- Cubic spline interpolation for smooth curves
- Control point-based interface

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
    red_points=[(0, 30), (128, 128), (255, 255)],
    green_points=[(0, 30), (128, 128), (255, 255)],
    blue_points=[(0, 30), (128, 128), (255, 255)],
)
```

---

## Selective Color Adjustments

Target specific color ranges (red, orange, yellow, green, cyan, blue, purple, magenta) with independent hue, saturation, and luminance controls.

### Usage

```python
from drone_reel.core.color_grader import (
    ColorAdjustments,
    ColorGrader,
    SelectiveColorAdjustments,
)

selective = SelectiveColorAdjustments(
    blue_sat=20,      # Enhance sky
    cyan_sat=15,      # Boost ocean/water
    green_sat=10,     # Subtle foliage enhancement
    orange_sat=-5,    # Slightly desaturate warm tones
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

---

## Improved Shadows/Highlights

Enhanced shadow and highlight adjustments using LAB color space for superior color preservation.

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

### Best Practices

- **Shadows**: Use positive values (10-50) to lift shadows
- **Highlights**: Use negative values (-10 to -40) to recover highlights
- **Combine with curves**: Use tone curves for overall contrast, shadows/highlights for fine-tuning

---

## Visual Effects

### Vignette

Radial edge darkening that draws the eye toward the center of the frame.

```bash
drone-reel create -i ./clips/ --vignette 0.4
```

```python
grader = ColorGrader(vignette_strength=0.4)  # 0.0-1.0
```

| Value | Effect |
|-------|--------|
| 0.1-0.3 | Subtle, barely noticeable |
| 0.3-0.5 | Standard cinematic vignette |
| 0.5-0.8 | Strong, dramatic darkening |
| 0.8-1.0 | Extreme, artistic effect |

---

### Halation

Warm bloom/glow around bright highlights, emulating the light scatter in analog film.

```bash
drone-reel create -i ./clips/ --halation 0.3
```

```python
grader = ColorGrader(halation_strength=0.3)  # 0.0-1.0
```

**Best for:** Sunset footage, golden hour, warm cinematic looks. Creates a dreamy, filmic glow around bright areas.

---

### Chromatic Aberration

RGB channel offset at frame edges, simulating lens fringing found in vintage or wide-angle lenses.

```bash
drone-reel create -i ./clips/ --chromatic-aberration 0.2
```

```python
grader = ColorGrader(chromatic_aberration_strength=0.2)  # 0.0-1.0
```

**Best for:** Vintage/analog looks, creative projects. Use subtly (0.1-0.3) for realism or stronger for artistic effect.

---

### Atmospheric Haze

Vertical gradient that blends the frame with a pale blue-white tone, strongest at the top. Simulates aerial perspective/atmospheric depth.

```bash
drone-reel create -i ./clips/ --haze 0.3
```

```python
grader = ColorGrader(haze_strength=0.3)  # 0.0-1.0
```

**Best for:** High-altitude footage, mountain vistas, creating depth in flat scenes.

---

### GND Sky Correction

Graduated neutral density filter that darkens the top half of the frame. Simulates a physical GND filter to balance bright skies with darker foreground.

```bash
drone-reel create -i ./clips/ --gnd-sky 0.4
```

```python
grader = ColorGrader(gnd_sky_strength=0.4)  # 0.0-1.0
```

**Best for:** Bright sky/dark ground scenes, landscapes, horizon shots. Darkening factor: `1.0 - strength * 0.6` at the top of frame.

---

### Letterbox

Cinematic letterbox bars (applied in the video processor, not ColorGrader).

```bash
drone-reel create -i ./clips/ --letterbox 0.1  # 10% of frame height per bar
```

**Best for:** Cinematic look on vertical format, dramatic presentation.

---

## Enhanced Film Grain

Professional film grain simulation with temporal coherence, organic structure, and shadow suppression.

### Features

- **Hash-based temporal seed**: Frame-index hash `(frame_index * 2654435761) % 2^31` ensures reproducible but varied grain per frame
- **Organic structure**: GaussianBlur applied to raw noise for film-like clumping
- **Shadow suppression**: Grain is suppressed in dark areas (weighted by `clip(gray / 0.1, 0, 1)`)
- **Midtone weighting**: Stronger in midtones, weaker in highlights (like real film)

### Usage

```python
from drone_reel.core.color_grader import ColorAdjustments, ColorGrader

adjustments = ColorAdjustments(grain=30)  # Range: 0-100
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

---

## GPU Acceleration

Optional GPU acceleration using CUDA for faster processing.

### Usage

```python
from drone_reel.core.color_grader import ColorGrader

grader = ColorGrader(use_gpu=True)

if grader.use_gpu:
    print("Using GPU acceleration")
else:
    print("GPU not available, using CPU")
```

### Requirements

- OpenCV compiled with CUDA support
- NVIDIA GPU with CUDA capability
- Appropriate CUDA drivers installed

---

## Preview Mode

Fast preview rendering at reduced resolution for quick iteration.

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

---

## Complete Workflow Examples

### Example 1: DJI D-Log M Drone Footage

```python
from pathlib import Path
from drone_reel.core.color_grader import ColorGrader, ColorPreset

# D-Log footage with auto white balance, film grain, and vignette
grader = ColorGrader(
    preset=ColorPreset.DRONE_AERIAL,
    input_colorspace="dlog_m",
    auto_wb=True,
    intensity=0.7,
    vignette_strength=0.3,
    halation_strength=0.2,
)

for i, frame in enumerate(video_frames):
    graded = grader.grade_frame(frame, frame_index=i)
```

### Example 2: Consistent Multi-Clip Color

```python
# Match all clips to the first clip's color distribution
grader = ColorGrader(
    preset=ColorPreset.CINEMATIC,
    denoise_strength=0.3,
)

# Set reference from hero clip
reference = get_first_frame(Path("hero_clip.mp4"))
grader.set_reference_frame(reference)

# Grade all clips - they'll match the reference color
for clip_path in clip_paths:
    grader.grade_video(clip_path, output_dir / clip_path.name)
```

### Example 3: Cinematic Kodak Film Look

```python
from drone_reel.core.color_grader import (
    ColorAdjustments, ColorGrader, ColorPreset,
    SelectiveColorAdjustments, ToneCurve,
)

selective = SelectiveColorAdjustments(
    blue_sat=20,
    cyan_sat=15,
    green_sat=10,
    orange_sat=-5,
)

tone_curve = ToneCurve(
    red_points=[(0, 0), (64, 50), (192, 205), (255, 255)],
    green_points=[(0, 0), (64, 48), (192, 207), (255, 255)],
    blue_points=[(0, 0), (64, 45), (192, 210), (255, 250)],
)

adjustments = ColorAdjustments(
    brightness=3,
    contrast=15,
    saturation=-8,
    temperature=5,
    shadows=12,
    highlights=-8,
    fade=5,
    grain=15,
    selective_color=selective,
)

grader = ColorGrader(
    adjustments=adjustments,
    tone_curve=tone_curve,
    vignette_strength=0.35,
    halation_strength=0.25,
    chromatic_aberration_strength=0.1,
)

for i, frame in enumerate(video_frames):
    graded = grader.grade_frame(frame, frame_index=i)
```

### Example 4: Atmospheric Mountain Footage

```python
grader = ColorGrader(
    preset=ColorPreset.SNOW_MOUNTAIN,
    input_colorspace="dlog_m",
    auto_wb=True,
    haze_strength=0.25,
    gnd_sky_strength=0.5,
    vignette_strength=0.2,
    denoise_strength=0.3,
    intensity=0.8,
)
```

### Example 5: Cyberpunk Night City

```python
grader = ColorGrader(
    preset=ColorPreset.CYBERPUNK_NEON,
    chromatic_aberration_strength=0.3,
    halation_strength=0.4,
    vignette_strength=0.5,
    intensity=0.8,
)
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
- `intensity: float` - Scale all adjustments (0.0-1.0, default: 1.0)
- `vignette_strength: float` - Radial edge darkening (0.0-1.0, default: 0.0)
- `halation_strength: float` - Warm highlight bloom (0.0-1.0, default: 0.0)
- `chromatic_aberration_strength: float` - RGB edge fringing (0.0-1.0, default: 0.0)
- `input_colorspace: str` - Input colorspace: `rec709`, `dlog`, `dlog_m`, `slog3` (default: `rec709`)
- `auto_wb: bool` - Enable gray world auto white balance (default: False)
- `denoise_strength: float` - Spatial denoising (0.0-1.0, default: 0.0)
- `haze_strength: float` - Atmospheric haze overlay (0.0-1.0, default: 0.0)
- `gnd_sky_strength: float` - Graduated ND sky darkening (0.0-1.0, default: 0.0)

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

- `frame: np.ndarray` - Input BGR frame
- `frame_index: int` - Optional frame index for temporal effects (grain)
- Returns: `np.ndarray` - Graded BGR frame

#### `ColorGrader.grade_frame_preview(frame, scale=0.25)`
Apply color grading at reduced resolution.

#### `ColorGrader.grade_video(input_path, output_path, progress_callback=None)`
Apply color grading to an entire video file.

#### `ColorGrader.set_reference_frame(frame)`
Set reference frame for auto color matching.

#### `ColorGrader.detect_log_footage(video_path)` *(static)*
Detect if footage is log-encoded. Returns `"dlog"` or `"rec709"`.

#### `ColorGrader.load_lut(lut_path)`
Load a .cube LUT file. Returns 3D LUT array.

#### `ColorGrader.apply_curve(frame)`
Apply tone curve to frame (float32 BGR input).

---

## Performance Tips

1. **Use preview mode** for iterating on settings
2. **Enable GPU** for batch processing if available
3. **Load LUTs once** and reuse the grader instance
4. **Minimize selective color adjustments** for better performance
5. **Reduce grain amount** if processing time is critical
6. **D-Log normalization** adds minimal overhead (single-pass per frame)
7. **Denoise** is the most expensive operation - use only when needed
8. **Auto color match** requires a reference frame set before grading

## Troubleshooting

### LUT Not Loading
- Verify .cube file format is correct
- Check LUT_3D_SIZE is specified
- Ensure correct number of entries (size^3)

### D-Log Footage Still Looks Flat
- Verify `--input-colorspace` matches your camera's log mode
- Use `auto` to let drone-reel detect the colorspace
- Combine with a preset for creative grading after normalization

### Colors Inconsistent Across Clips
- Use `--auto-color-match` to normalize all clips to the first
- Combine with `--auto-wb` for additional correction
- Check that clips were shot in the same colorspace

### GPU Not Working
- Verify OpenCV has CUDA support: `cv2.cuda.getCudaEnabledDeviceCount()`
- Install opencv-contrib-python with CUDA
- Update GPU drivers

---

## Resources

- [.cube LUT Format Specification](https://wwwimages.adobe.com/content/dam/acom/en/products/speedgrade/cc/pdfs/cube-lut-specification-1.0.pdf)
- [Color Grading Theory](https://en.wikipedia.org/wiki/Color_grading)
- [LAB Color Space](https://en.wikipedia.org/wiki/CIELAB_color_space)
- [Film Grain Characteristics](https://en.wikipedia.org/wiki/Film_grain)
- [DJI D-Log Color Science](https://store.dji.com/guides/dji-d-log/)
