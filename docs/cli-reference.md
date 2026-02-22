# CLI Reference

The `drone-reel` command-line tool provides commands for creating reels and analyzing media files.

## Global Options

```bash
drone-reel --version  # Show version
drone-reel --help     # Show help
```

---

## create

Create a reel from drone footage.

```bash
drone-reel create [OPTIONS]
```

### Required Options

| Option | Short | Description |
|--------|-------|-------------|
| `--input PATH` | `-i` | Input directory with video files or single video file |

### Output Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--output PATH` | `-o` | `./output/reel.mp4` | Output video file path |
| `--duration FLOAT` | `-d` | `45.0` | Target duration in seconds |
| `--aspect CHOICE` | | `9:16` | Output aspect ratio: `9:16`, `1:1`, `4:5`, `16:9` |
| `--resolution CHOICE` | | `1080p` | Output resolution: `720p`, `1080p`, `1440p`, `4k` |
| `--quality CHOICE` | | `medium` | Encoding quality: `draft`, `medium`, `high`, `ultra` |
| `--platform CHOICE` | | | Platform preset: `instagram_reels`, `tiktok`, `youtube_shorts`, `youtube` |

### Audio Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--music PATH` | `-m` | | Music track for beat synchronization |
| `--beat-mode CHOICE` | | `all` | Beat sync mode: `all` (every beat), `downbeat` (strong beats only) |
| `--duck-outro FLOAT` | | `0.0` | Fade music volume at end (seconds, 0 = off) |

### Color Grading Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--color PRESET` | `-c` | `drone_aerial` | Color grading preset (see [Color Presets](presets/color-presets.md)) |
| `--color-intensity FLOAT` | | `1.0` | Scale color adjustments (0.0-1.0) |
| `--lut PATH` | | | Path to .cube LUT file for custom color grading |

### Visual Effects Options

| Option | Default | Description |
|--------|---------|-------------|
| `--vignette FLOAT` | `0.0` | Edge darkening strength (0.0-1.0) |
| `--halation FLOAT` | `0.0` | Warm highlight bloom strength (0.0-1.0) |
| `--chromatic-aberration FLOAT` | `0.0` | RGB edge fringing strength (0.0-1.0) |
| `--haze FLOAT` | `0.0` | Atmospheric haze overlay (0.0-1.0) |
| `--gnd-sky FLOAT` | `0.0` | Graduated ND sky darkening (0.0-1.0) |
| `--letterbox FLOAT` | `0.0` | Cinematic letterbox bars (0.0-1.0, fraction of frame height) |

### Color Science Options

| Option | Default | Description |
|--------|---------|-------------|
| `--input-colorspace CHOICE` | `rec709` | Input footage colorspace: `rec709`, `dlog`, `dlog_m`, `slog3`, `auto` |
| `--auto-wb` | off | Enable gray world auto white balance |
| `--auto-color-match` | off | Normalize clip colors to first clip's histogram |
| `--denoise FLOAT` | `0.0` | Spatial noise reduction strength (0.0-1.0) |

### Transition Options

| Option | Default | Description |
|--------|---------|-------------|
| `--transition TYPE` | `crossfade` | Default transition type (see [Transitions](presets/transitions.md)) |

Available types: `cut`, `crossfade`, `fade_black`, `fade_white`, `zoom_in`, `zoom_out`, `slide_left`, `slide_right`, `wipe_left`, `wipe_right`, `whip_pan`, `glitch_rgb`, `iris_in`, `iris_out`, `flash_white`, `light_leak`, `hyperlapse_zoom`, `parallax_left`, `parallax_right`, `wipe_diagonal`, `wipe_diamond`, `fog_pass`, `vortex_zoom`

### Reframing Options

| Option | Default | Description |
|--------|---------|-------------|
| `--reframe MODE` | `smart` | Reframing mode: `smart`, `center`, `pan`, `thirds` |
| `--clips INT` | auto | Number of clips to include (auto-calculated if not specified) |

### Stabilization Options

| Option | Description |
|--------|-------------|
| `--stabilize` | Enable stabilization for shaky clips |
| `--stabilize-all` | Force stabilization on all clips |
| `--stable-threshold FLOAT` | Shake score threshold for auto-stabilization (0-100) |

### Speed & Text Options

| Option | Description |
|--------|-------------|
| `--speed-ramp` | Enable automatic speed ramping (slow-mo on hooks) |
| `--caption TEXT` | Add animated lower-third text overlay |

### Preset Options

| Option | Description |
|--------|-------------|
| `--viral` | Viral preset: 15s, Instagram Reels, 60% color, speed ramp |

### Skip Options

| Option | Description |
|--------|-------------|
| `--no-reframe` | Skip reframing (keep original aspect ratio) |
| `--no-color` | Skip color grading |
| `--preview` | Preview mode - show plan without processing |

### Examples

```bash
# Basic reel from folder of clips
drone-reel create -i ./clips/ -o reel.mp4

# 60-second reel with music and cinematic color grade
drone-reel create -i ./clips/ -m ./track.mp3 -d 60 --color cinematic

# D-Log footage with auto white balance and film look
drone-reel create -i ./clips/ --input-colorspace dlog_m --auto-wb --color kodak_2383

# Cinematic with vignette, halation, and letterbox
drone-reel create -i ./clips/ --color cinematic --vignette 0.4 --halation 0.3 --letterbox 0.1

# 4K with stabilization and atmospheric effects
drone-reel create -i ./clips/ --resolution 4k --quality ultra --stabilize-all --haze 0.2 --gnd-sky 0.4

# Consistent color across clips with denoising
drone-reel create -i ./clips/ --auto-color-match --denoise 0.5

# Square format for Instagram feed
drone-reel create -i ./clips/ --aspect 1:1 --reframe center

# Preview what clips will be selected
drone-reel create -i ./clips/ -d 30 --preview

# Keep original landscape format with color grading only
drone-reel create -i ./clips/ --no-reframe --color warm_sunset

# Custom LUT with chromatic aberration
drone-reel create -i ./clips/ --lut my_grade.cube --chromatic-aberration 0.3
```

---

## analyze

Analyze a video file and display detected scenes.

```bash
drone-reel analyze --input VIDEO_FILE
```

### Options

| Option | Short | Description |
|--------|-------|-------------|
| `--input PATH` | `-i` | Video file to analyze (required) |

### Output

Displays a table showing:
- Scene number
- Start/end timestamps
- Duration
- Visual quality score (0-100)

### Example

```bash
drone-reel analyze -i ./raw_footage.mp4
```

Output:
```
                    Detected Scenes
┏━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━┳━━━━━━━┓
┃ Scene ┃ Start  ┃ End    ┃ Duration ┃ Score ┃
┡━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━╇━━━━━━━┩
│ 1     │ 0:00   │ 0:04   │ 4.2s     │ 78.3  │
│ 2     │ 0:04   │ 0:09   │ 5.1s     │ 82.1  │
│ 3     │ 0:09   │ 0:15   │ 6.0s     │ 65.4  │
└───────┴────────┴────────┴──────────┴───────┘
```

---

## beats

Analyze a music track and display beat information.

```bash
drone-reel beats --input AUDIO_FILE
```

### Options

| Option | Short | Description |
|--------|-------|-------------|
| `--input PATH` | `-i` | Audio file to analyze (required) |

### Output

Displays:
- Detected tempo (BPM)
- Track duration
- Total beat count
- Number of downbeats (strong beats)
- Beat interval (seconds between beats)
- First 10 beat timestamps (* marks downbeats)

### Example

```bash
drone-reel beats -i ./music.mp3
```

Output:
```
Tempo: 128.0 BPM
Duration: 3:24
Total beats: 432
Downbeats: 108
Beat interval: 0.469s

First 10 beat times:
  1. 0:00 *
  2. 0:00
  3. 0:01
  4. 0:01 *
  ...
```

---

## presets

List available color grading presets.

```bash
drone-reel presets
```

### Output

Displays a table of all 30 available color presets with descriptions.

---

## platforms

List available platform export presets.

```bash
drone-reel platforms
```

---

## Configuration

User configuration is stored at `~/.config/drone_reel/config.json`. CLI arguments override config file values.

### Default Configuration

```json
{
  "output_duration": 45.0,
  "output_fps": 30,
  "output_width": 1080,
  "aspect_ratio": "9:16",
  "scene_threshold": 27.0,
  "min_scene_length": 1.0,
  "max_scene_length": 8.0,
  "min_clip_length": 1.5,
  "max_clip_length": 4.0,
  "reframe_mode": "smart",
  "color_preset": "drone_aerial",
  "transition_type": "crossfade",
  "transition_duration": 0.3,
  "prefer_downbeats": true,
  "threads": 4,
  "preset": "medium"
}
```

### Key Parameters

| Parameter | Description |
|-----------|-------------|
| `scene_threshold` | Sensitivity for scene detection (lower = more cuts) |
| `min_scene_length` / `max_scene_length` | Scene duration bounds (seconds) |
| `min_clip_length` / `max_clip_length` | Clip duration bounds for beat sync |
| `prefer_downbeats` | Prioritize strong beats for cut points |
| `preset` | FFmpeg encoding preset (ultrafast to veryslow) |
