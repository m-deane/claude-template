# ColorGrader Quick Reference

Quick reference guide for common ColorGrader operations.

## Installation

```bash
pip install scipy  # Required for tone curves
```

## Basic Usage

```python
from drone_reel.core.color_grader import ColorGrader, ColorPreset

# Use a preset
grader = ColorGrader(preset=ColorPreset.CINEMATIC)
result = grader.grade_frame(frame)
```

## Feature Quick Reference

### 1. LUT Support

```python
from pathlib import Path

grader = ColorGrader(lut_path=Path('my_lut.cube'))
```

### 2. Tone Curves

```python
from drone_reel.core.color_grader import ToneCurve

# S-curve for contrast
curve = ToneCurve(
    red_points=[(0, 0), (64, 45), (192, 210), (255, 255)],
    green_points=[(0, 0), (64, 45), (192, 210), (255, 255)],
    blue_points=[(0, 0), (64, 45), (192, 210), (255, 255)],
)
grader = ColorGrader(tone_curve=curve)
```

### 3. Selective Color

```python
from drone_reel.core.color_grader import (
    ColorAdjustments,
    SelectiveColorAdjustments,
)

selective = SelectiveColorAdjustments(
    red_sat=30,      # Boost red saturation
    blue_hue=10,     # Shift blue hue
    green_lum=15,    # Brighten greens
)

adjustments = ColorAdjustments(selective_color=selective)
grader = ColorGrader(adjustments=adjustments)
```

### 4. Shadows/Highlights (LAB)

```python
adjustments = ColorAdjustments(
    shadows=40,      # Lift shadows
    highlights=-30,  # Recover highlights
)
grader = ColorGrader(adjustments=adjustments)
```

### 5. Film Grain

```python
adjustments = ColorAdjustments(grain=30)
grader = ColorGrader(adjustments=adjustments)

# Process with temporal coherence
for i, frame in enumerate(frames):
    result = grader.grade_frame(frame, frame_index=i)
```

### 6. GPU Acceleration

```python
grader = ColorGrader(use_gpu=True)

if grader.use_gpu:
    print("GPU enabled")
else:
    print("Using CPU")
```

### 7. Preview Mode

```python
# Fast preview at 25% size
preview = grader.grade_frame_preview(frame, scale=0.25)

# Full resolution when ready
final = grader.grade_frame(frame)
```

## Common Recipes

### Cinematic Look

```python
selective = SelectiveColorAdjustments(
    blue_sat=20,
    orange_sat=-5,
)

curve = ToneCurve(
    red_points=[(0, 0), (64, 50), (192, 205), (255, 255)],
    green_points=[(0, 0), (64, 48), (192, 207), (255, 255)],
    blue_points=[(0, 0), (64, 45), (192, 210), (255, 250)],
)

adjustments = ColorAdjustments(
    contrast=15,
    saturation=-8,
    shadows=12,
    highlights=-8,
    grain=15,
    selective_color=selective,
)

grader = ColorGrader(adjustments=adjustments, tone_curve=curve)
```

### Vintage Film

```python
selective = SelectiveColorAdjustments(
    yellow_sat=20,
    blue_sat=-30,
)

curve = ToneCurve(
    red_points=[(0, 25), (128, 135), (255, 240)],
    green_points=[(0, 20), (128, 130), (255, 235)],
    blue_points=[(0, 15), (128, 120), (255, 225)],
)

adjustments = ColorAdjustments(
    contrast=-10,
    saturation=-25,
    temperature=20,
    fade=25,
    grain=40,
    selective_color=selective,
)

grader = ColorGrader(adjustments=adjustments, tone_curve=curve)
```

### Teal & Orange

```python
selective = SelectiveColorAdjustments(
    orange_sat=35,
    orange_hue=5,
    cyan_sat=30,
    blue_sat=20,
    blue_hue=10,
)

adjustments = ColorAdjustments(
    contrast=18,
    saturation=10,
    temperature=10,
    tint=-8,
    selective_color=selective,
)

grader = ColorGrader(adjustments=adjustments)
```

### Natural Enhancement

```python
selective = SelectiveColorAdjustments(
    green_sat=15,
    green_hue=-5,
    blue_sat=10,
)

adjustments = ColorAdjustments(
    contrast=8,
    saturation=5,
    shadows=10,
    highlights=-5,
    selective_color=selective,
)

grader = ColorGrader(adjustments=adjustments)
```

## Parameter Ranges

| Parameter | Range | Unit | Description |
|-----------|-------|------|-------------|
| brightness | -100 to 100 | % | Lighter/darker |
| contrast | -100 to 100 | % | Flatter/punchier |
| saturation | -100 to 100 | % | Desaturate/saturate |
| temperature | -100 to 100 | % | Cool/warm |
| tint | -100 to 100 | % | Green/magenta |
| shadows | -100 to 100 | % | Darken/lift |
| highlights | -100 to 100 | % | Lift/recover |
| vibrance | -100 to 100 | % | Subtle saturation |
| fade | 0 to 100 | % | Black lift amount |
| grain | 0 to 100 | % | Film grain intensity |

## Selective Color Ranges

| Color | Hue Range (HSV) | Typical Content |
|-------|-----------------|-----------------|
| red | 0-15°, 345-360° | Fire, red objects |
| orange | 16-45° | Skin tones, sunset |
| yellow | 46-75° | Sun, golden hour |
| green | 76-165° | Foliage, grass |
| cyan | 166-195° | Ocean, cyan sky |
| blue | 196-255° | Sky, water |
| purple | 256-285° | Purple flowers |
| magenta | 286-344° | Magenta tones |

Each color has three adjustments:
- `{color}_hue`: -180 to 180 (shift hue)
- `{color}_sat`: -100 to 100 (adjust saturation)
- `{color}_lum`: -100 to 100 (adjust luminance)

## Performance Guidelines

| Operation | Speed | Use Case |
|-----------|-------|----------|
| Preview (0.25x) | 16x faster | Quick iteration |
| Preview (0.5x) | 4x faster | Detailed preview |
| CPU | Baseline | Standard processing |
| GPU | 2-5x faster | Batch processing |

## Tone Curve Control Points

Control points are `(input, output)` tuples where:
- Input: 0-255 (pixel value in)
- Output: 0-255 (pixel value out)

### Common Curves

**Identity (no change)**
```python
[(0, 0), (255, 255)]
```

**S-curve (contrast)**
```python
[(0, 0), (64, 45), (192, 210), (255, 255)]
```

**Lifted blacks**
```python
[(0, 30), (255, 255)]
```

**Rolled highlights**
```python
[(0, 0), (255, 230)]
```

**Inverted**
```python
[(0, 255), (255, 0)]
```

## Color Space Notes

| Operation | Color Space | Why |
|-----------|-------------|-----|
| Brightness | RGB | Direct pixel values |
| Contrast | RGB | Around midpoint |
| Saturation | HSV | Saturation channel |
| Temperature | RGB | Red/blue channels |
| Tint | RGB | Green channel |
| Shadows/Highlights | LAB | Preserves color |
| Selective color | HSV+LAB | Hue targeting + luminance |

## Troubleshooting

### Q: Colors look wrong after grading
**A:** Check that your frame is in BGR format (OpenCV default)

### Q: LUT won't load
**A:** Verify .cube format, ensure `LUT_3D_SIZE` is specified

### Q: GPU isn't being used
**A:** Check `cv2.cuda.getCudaEnabledDeviceCount() > 0`

### Q: Processing is slow
**A:** Use preview mode for iteration, full resolution for final render

### Q: Grain looks the same on every frame
**A:** Pass `frame_index` parameter to `grade_frame()`

### Q: Selective color not working
**A:** Convert to BGR color space first, verify hue ranges

## API Summary

```python
# Constructor
ColorGrader(
    preset=ColorPreset.NONE,
    adjustments=None,
    lut_path=None,
    tone_curve=None,
    use_gpu=False,
)

# Main methods
grader.grade_frame(frame, frame_index=None) -> np.ndarray
grader.grade_frame_preview(frame, scale=0.25) -> np.ndarray
grader.grade_video(input_path, output_path, progress_callback=None) -> Path

# LUT methods
grader.load_lut(lut_path) -> np.ndarray
grader.apply_curve(frame) -> np.ndarray

# GPU check
grader._check_gpu_available() -> bool
```

## Available Presets

- `NONE` - No adjustments
- `CINEMATIC` - Film-like grade
- `WARM_SUNSET` - Warm golden tones
- `COOL_BLUE` - Cool blue tones
- `VINTAGE` - Faded retro look
- `HIGH_CONTRAST` - Punchy contrast
- `MUTED` - Desaturated subtle
- `VIBRANT` - Saturated vibrant
- `TEAL_ORANGE` - Popular blockbuster
- `BLACK_WHITE` - B&W conversion
- `DRONE_AERIAL` - Optimized for drone

## Example Workflows

### Quick Preset Application
```python
grader = ColorGrader(preset=ColorPreset.CINEMATIC)
result = grader.grade_frame(frame)
```

### Iterative Development
```python
# 1. Create grader
grader = ColorGrader(adjustments=adjustments)

# 2. Preview quickly
preview = grader.grade_frame_preview(test_frame, scale=0.25)

# 3. Adjust settings, preview again
adjustments.contrast = 20
preview = grader.grade_frame_preview(test_frame, scale=0.25)

# 4. Process full video
for i, frame in enumerate(video):
    result = grader.grade_frame(frame, frame_index=i)
```

### Batch Processing with LUT
```python
grader = ColorGrader(
    lut_path=Path('cinematic.cube'),
    use_gpu=True
)

for video_path in video_files:
    grader.grade_video(video_path, output_path)
```

### Complete Custom Grade
```python
selective = SelectiveColorAdjustments(
    orange_sat=25,
    blue_sat=15,
)

curve = ToneCurve(
    red_points=[(0, 0), (64, 50), (192, 205), (255, 255)],
    green_points=[(0, 0), (64, 48), (192, 207), (255, 255)],
    blue_points=[(0, 0), (64, 45), (192, 210), (255, 250)],
)

adjustments = ColorAdjustments(
    brightness=3,
    contrast=15,
    saturation=-5,
    shadows=15,
    highlights=-10,
    grain=20,
    selective_color=selective,
)

grader = ColorGrader(
    adjustments=adjustments,
    lut_path=Path('base_look.cube'),
    tone_curve=curve,
    use_gpu=True,
)

# Preview
preview = grader.grade_frame_preview(frame, scale=0.25)

# Process
result = grader.grade_frame(frame, frame_index=0)
```

---

For complete documentation, see [color_grader_advanced_features.md](color_grader_advanced_features.md)
