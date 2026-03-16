# CLI Reference

The `drone-reel` command-line tool provides commands for creating reels and analyzing media files.

> **New user?** See [QUICKSTART.md](QUICKSTART.md) for a single-page reference with all parameters and recipes.

## Global Options

```bash
drone-reel --version  # Show version
drone-reel --help     # Show help
```

Commands: `create` · `split` · `extract-clips` · `analyze` · `beats` · `presets` · `platforms`

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

| Option | Default | Description |
|--------|---------|-------------|
| `--stabilize` | off | Enable stabilization for shaky clips |
| `--stabilize-all` | off | Force stabilization on all clips |
| `--stable-threshold FLOAT` | `15.0` | Shake score threshold for auto-stabilization (0-100) |
| `--stab-strength CHOICE` | `adaptive` | `off` · `light` · `adaptive` · `full` — off skips entirely, light always applies mild correction, adaptive uses threshold logic, full always applies full correction |
| `--smooth-radius INT` | `50` | Optical-flow smoothing window radius (5–120) |
| `--border-crop FLOAT` | `0.05` | Border crop fraction after stabilization (0.0–0.15) |
| `--max-corners INT` | `200` | Feature tracking points for optical flow (50–500) |

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

## split

Detect scenes in a single video and export graded highlight clips.

```bash
drone-reel split [OPTIONS]
```

### Scene Selection Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--input PATH` | `-i` | required | Single video file |
| `--output-dir PATH` | `-o` | `./highlights` | Output folder |
| `--min-score FLOAT` | | `40.0` | Minimum scene quality score (0–100) |
| `--min-duration FLOAT` | | `2.0` | Shortest clip to export in seconds |
| `--max-duration FLOAT` | | `15.0` | Longest clip. Scenes exceeding this are chunked into multiple clips |
| `--count INT` | `-n` | unlimited | Cap total clips exported |
| `--sort CHOICE` | `-s` | `score` | Output order: `score`, `chronological`, `duration` |
| `--no-filter` | | off | Skip quality filtering — export all detected scenes |
| `--scene-threshold FLOAT` | | `27.0` | Detection sensitivity (1–100, lower = more boundaries) |
| `--enhanced` | | off | Enhanced detection with subject tracking. Slower. |
| `--analysis-scale FLOAT` | | `0.5` | Frame downscale factor for analysis (0.1–1.0, lower = faster) |
| `--motion-energy-method CHOICE` | | `mean` | Aggregate per-frame motion scores: `mean` · `median` · `p95` |
| `--prefer-motion-type TEXT` | | `none` | Comma-separated motion types to float to front e.g. `flyover,pan_right` |
| `--preview` | | off | Print scene table without exporting |
| `--json` | | off | Write `manifest.json` with per-clip metadata |
| `--overwrite` | | off | Overwrite existing clips |

### Scene Filtering Options

Fine-tune which scenes pass the quality filter (applied before `--no-filter` override):

| Option | Default | Description |
|--------|---------|-------------|
| `--brightness-range TEXT` | `30-245` | Brightness bounds `MIN-MAX` — scenes outside range filtered |
| `--motion-threshold FLOAT` | — | Minimum motion energy required (0–100) |
| `--shake-tolerance FLOAT` | — | Maximum allowed shake score (0–100) |
| `--subject-confidence FLOAT` | — | Minimum subject detection confidence (0.0–1.0) |

> **Tip for long clips:** Use `--scene-threshold 7–12` when targeting `--min-duration 11+`. The default threshold produces many short scenes; a lower threshold merges them into longer coherent segments.

### Motion Correction Options

| Option | Default | Description |
|--------|---------|-------------|
| `--auto-speed` | off | Auto-correct pan/tilt speed — slows fast pans (0.65–0.80×), speeds up sluggish ones (1.25×), corrects tilts/flyovers/FPV |
| `--stabilize` | off | Adaptive optical-flow stabilization (skips stable clips) |
| `--stabilize-all` | off | Force full stabilization on every clip |

#### Auto-speed tuning (requires `--auto-speed`)

| Option | Default | Description |
|--------|---------|-------------|
| `--speed-correction-profile CHOICE` | `normal` | `aggressive` · `normal` · `smooth` · `cinematic` — preset speed factors |
| `--pan-speed-high FLOAT` | — | Speed factor override for high-energy pans, energy > 70 (0.1–1.5) |
| `--pan-speed-mid FLOAT` | — | Speed factor override for mid-energy pans, energy 55–70 (0.1–1.5) |
| `--tilt-speed FLOAT` | — | Speed factor override for fast tilts (0.1–1.5) |
| `--fpv-speed FLOAT` | — | Speed factor override for FPV shots (0.1–1.5) |
| `--correct-orbit` | off | Apply gentle 0.85× correction to orbit shots |
| `--ease-speed-ramps` | off | Ease in/out of speed corrections (15% ramp-in · 70% constant · 15% ramp-out) |
| `--vertical-drift-damping FLOAT` | `0.0` | Extra slowdown on tilt-down to reduce vertical drift (0.0–1.0) |

Speed profile comparison:

| Profile | PAN high | PAN mid | TILT | FPV | FLYOVER |
|---------|----------|---------|------|-----|---------|
| `aggressive` | 0.55× | 0.70× | 0.60× | 0.65× | 0.60× |
| `normal` | 0.65× | 0.80× | 0.70× | 0.75× | 0.70× |
| `cinematic` | 0.60× | 0.75× | 0.65× | 0.70× | 0.65× |
| `smooth` | 0.75× | 0.85× | 0.80× | 0.80× | 0.80× |

#### Stabilization tuning

| Option | Default | Description |
|--------|---------|-------------|
| `--stable-threshold FLOAT` | `15.0` | Shake score threshold for adaptive stabilization (0–100) |
| `--stab-strength CHOICE` | `adaptive` | `off` · `light` · `adaptive` · `full` |
| `--smooth-radius INT` | `50` | Optical-flow smoothing window radius (5–120) |
| `--border-crop FLOAT` | `0.05` | Border crop fraction after stabilization (0.0–0.15) |
| `--max-corners INT` | `200` | Feature tracking points (50–500) |

### Post-Processing Options

All color/effects flags from `create` are available:

| Option | Default | Description |
|--------|---------|-------------|
| `--color PRESET` | `none` | Color grading preset |
| `--color-intensity FLOAT` | `1.0` | Scale preset strength 0.0–1.0 |
| `--input-colorspace CHOICE` | `rec709` | `rec709`, `dlog`, `dlog_m`, `slog3`, `auto` |
| `--auto-wb` | off | Gray world auto white balance |
| `--denoise FLOAT` | `0.0` | Noise reduction 0.0–1.0 |
| `--lut PATH` | — | `.cube` 3D LUT file |
| `--vignette FLOAT` | `0.0` | Edge darkening 0.0–1.0 |
| `--halation FLOAT` | `0.0` | Highlight bloom 0.0–1.0 |
| `--chromatic-aberration FLOAT` | `0.0` | RGB fringing 0.0–1.0 |
| `--haze FLOAT` | `0.0` | Atmospheric haze 0.0–1.0 |
| `--gnd-sky FLOAT` | `0.0` | Sky darkening 0.0–1.0 |
| `--letterbox CHOICE` | `off` | `off`, `2.35`, `1.85`, `2.39` |
| `--quality CHOICE` | `high` | `low`, `medium`, `high`, `ultra` |
| `--resolution CHOICE` | `source` | `source`, `hd`, `2k`, `4k` |

### Output Naming

`split_NNN_sSCORE.mp4` — e.g. `split_001_s72.mp4` = clip #1, scene score 72.

### Examples

```bash
# Preview scenes before exporting
drone-reel split -i clip.mp4 -o ./out --preview

# Best 5–15s highlights with cinematic grade
drone-reel split -i clip.mp4 -o ./out \
  --min-duration 5 --max-duration 15 --min-score 0 --no-filter \
  --color drone_aerial --color-intensity 0.65 --vignette 0.3 \
  --auto-speed --letterbox 2.35 --quality high --json

# Long highlights 11–17s chunked from long scenes
drone-reel split -i clip.mp4 -o ./out \
  --min-duration 11 --max-duration 17 --min-score 0 --no-filter \
  --scene-threshold 7 \
  --color drone_aerial --color-intensity 0.65 --vignette 0.3 \
  --auto-speed --letterbox 2.35 --quality high --json

# DJI 4K HEVC — proxy required for practical runtimes
ffmpeg -i DJI_SOURCE.MP4 -vf scale=1280:720 -r 30 -c:v libx264 -preset ultrafast -crf 26 -an proxy.mp4
drone-reel split -i proxy.mp4 -o ./out \
  --min-duration 5 --max-duration 15 \
  --input-colorspace dlog --color drone_aerial --auto-speed --letterbox 2.35 --json
```

---

## extract-clips

Extract top-scoring scenes from a video file as individual clips.

```bash
drone-reel extract-clips [OPTIONS]
```

### Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--input PATH` | `-i` | path | required | Video file or directory of videos to extract clips from |
| `--output-dir PATH` | `-o` | path | `./clips` | Directory for extracted clip files |
| `--count INT` | `-n` | int (1-100) | `10` | Maximum number of clips to extract |
| `--min-score FLOAT` | | float (0-100) | `30.0` | Minimum scene score threshold |
| `--min-duration FLOAT` | | float (0.5-300) | `2.0` | Minimum clip duration in seconds |
| `--max-duration FLOAT` | | float (1.0-300) | `10.0` | Maximum clip duration in seconds |
| `--quality CHOICE` | `-q` | choice | `high` | Output quality: `low` (5M), `medium` (10M), `high` (15M), `ultra` (25M) bitrate |
| `--resolution CHOICE` | | choice | `source` | Output resolution: `source`, `hd` (1080p), `2k` (1440p), `4k` (2160p) |
| `--sort CHOICE` | `-s` | choice | `score` | Output order: `score` (best first), `chronological`, `duration` (longest first) |
| `--no-filter` | | flag | off | Skip quality filtering -- extract all detected scenes |
| `--enhanced` | | flag | off | Run enhanced analysis (subject detection, hook potential) for better ranking. Slower. |
| `--json` | | flag | off | Write a sidecar `manifest.json` with scene metadata and extraction params |
| `--overwrite` | | flag | off | Overwrite existing clips in output directory |

### Output Format

Extracted clips are named with a zero-padded index and the scene score: `clip_NNN_sSCORE.mp4` (e.g. `clip_001_s85.mp4`). When `--sort score` (the default), clips are numbered in descending score order so `clip_001` is always the highest-scoring scene.

### Examples

```bash
# Basic: extract top 10 clips from a single file
drone-reel extract-clips -i drone_footage.mp4 -o ./clips

# Extract 20 clips, enhanced scoring, with JSON manifest
drone-reel extract-clips -i footage.mp4 -o ./clips -n 20 --enhanced --json

# Extract from a whole directory, keep original resolution
drone-reel extract-clips -i ./raw_shoots/ -o ./clips -n 30 --resolution source

# Extract then create a reel from the clips
drone-reel extract-clips -i footage.mp4 -o ./clips -n 15 --json
drone-reel create -i ./clips/ -m music.mp3 -o reel.mp4 --duration 30
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
