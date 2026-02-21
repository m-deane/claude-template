# Color Presets Reference

drone-reel includes 11 color grading presets optimized for different footage types and styles.

## Available Presets

### none
No color grading applied. Use when you want to preserve the original footage colors.

### cinematic
Film-like aesthetic with lifted blacks and slightly reduced saturation. Creates a professional, moody look.

| Parameter | Value |
|-----------|-------|
| Contrast | +15 |
| Saturation | -10 |
| Temperature | +5 |
| Shadows | -10 |
| Highlights | -5 |
| Fade | +5 |

**Best for:** Dramatic aerial shots, urban landscapes, storytelling

---

### warm_sunset
Warm golden tones that enhance sunrise/sunset footage. Adds vibrance and a golden glow.

| Parameter | Value |
|-----------|-------|
| Brightness | +5 |
| Contrast | +10 |
| Saturation | +15 |
| Temperature | +30 |
| Tint | +5 |
| Vibrance | +20 |

**Best for:** Golden hour footage, beach scenes, desert landscapes

---

### cool_blue
Cool blue tones that work well with ocean, sky, and winter footage.

| Parameter | Value |
|-----------|-------|
| Contrast | +10 |
| Saturation | +5 |
| Temperature | -25 |
| Shadows | +5 |
| Highlights | -10 |

**Best for:** Ocean footage, snow scenes, early morning/twilight shots

---

### vintage
Faded retro look with film grain. Creates a nostalgic, analog film aesthetic.

| Parameter | Value |
|-----------|-------|
| Contrast | -5 |
| Saturation | -20 |
| Temperature | +10 |
| Fade | +20 |
| Grain | +15 |

**Best for:** Historical locations, artistic projects, music videos

---

### high_contrast
Punchy, dramatic look with strong blacks and whites.

| Parameter | Value |
|-----------|-------|
| Contrast | +35 |
| Saturation | +10 |
| Shadows | -15 |
| Highlights | +10 |

**Best for:** Dramatic landscapes, action footage, sports content

---

### muted
Desaturated, understated look popular in contemporary content.

| Parameter | Value |
|-----------|-------|
| Contrast | -10 |
| Saturation | -30 |
| Fade | +15 |

**Best for:** Lifestyle content, fashion, minimalist aesthetics

---

### vibrant
Enhanced colors and saturation for eye-catching footage.

| Parameter | Value |
|-----------|-------|
| Contrast | +15 |
| Saturation | +30 |
| Vibrance | +25 |
| Highlights | -5 |

**Best for:** Tropical locations, colorful landscapes, nature footage

---

### teal_orange
Popular Hollywood color grade that pushes shadows to teal and skin tones to orange.

| Parameter | Value |
|-----------|-------|
| Contrast | +10 |
| Saturation | +5 |
| Temperature | +15 |
| Tint | -10 |

**Best for:** Cinematic content, urban scenes, any footage with people

---

### black_white
Classic black and white with enhanced contrast.

| Parameter | Value |
|-----------|-------|
| Saturation | -100 |
| Contrast | +20 |

**Best for:** Documentary style, artistic projects, classic aesthetics

---

### drone_aerial
**Default preset.** Optimized specifically for aerial drone footage. Balances colors for typical sky/ground compositions and enhances the natural beauty of landscapes.

| Parameter | Value |
|-----------|-------|
| Brightness | +5 |
| Contrast | +12 |
| Saturation | +8 |
| Temperature | +8 |
| Vibrance | +15 |
| Shadows | +10 |
| Highlights | -8 |

**Best for:** General drone footage, landscapes, travel content

---

## Usage

### CLI

```bash
drone-reel create -i ./clips/ --color cinematic
drone-reel create -i ./clips/ --color warm_sunset
drone-reel create -i ./clips/ --no-color  # Skip grading
```

### Python API

```python
from drone_reel import ColorGrader
from drone_reel.core.color_grader import ColorPreset

# Using a preset
grader = ColorGrader(preset=ColorPreset.CINEMATIC)
grader.grade_video(input_path, output_path)

# List all presets
from drone_reel.core.color_grader import get_preset_names
print(get_preset_names())
```

---

## Custom Adjustments

You can create custom color grades by specifying individual parameters:

```python
from drone_reel import ColorGrader
from drone_reel.core.color_grader import ColorAdjustments

custom = ColorAdjustments(
    brightness=0.0,     # -100 to 100
    contrast=20.0,      # -100 to 100
    saturation=10.0,    # -100 to 100
    temperature=-10.0,  # -100 (cool) to 100 (warm)
    tint=0.0,           # -100 (green) to 100 (magenta)
    shadows=5.0,        # -100 to 100
    highlights=-5.0,    # -100 to 100
    vibrance=15.0,      # -100 to 100
    fade=0.0,           # 0 to 100 (lifts blacks)
    grain=0.0           # 0 to 100
)

grader = ColorGrader(adjustments=custom)
```

### Parameter Descriptions

| Parameter | Range | Effect |
|-----------|-------|--------|
| **brightness** | -100 to 100 | Overall image brightness |
| **contrast** | -100 to 100 | Difference between darks and lights |
| **saturation** | -100 to 100 | Color intensity (-100 = grayscale) |
| **temperature** | -100 to 100 | Color temperature (negative = cool/blue, positive = warm/orange) |
| **tint** | -100 to 100 | Green/magenta shift (negative = green, positive = magenta) |
| **shadows** | -100 to 100 | Brightness of dark areas |
| **highlights** | -100 to 100 | Brightness of light areas |
| **vibrance** | -100 to 100 | Saturation that protects already-saturated colors |
| **fade** | 0 to 100 | Lifts black levels for a faded/matte look |
| **grain** | 0 to 100 | Adds film grain noise |
