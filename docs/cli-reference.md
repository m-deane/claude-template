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

### Audio Options

| Option | Short | Description |
|--------|-------|-------------|
| `--music PATH` | `-m` | Music track for beat synchronization |

### Visual Options

| Option | Default | Description |
|--------|---------|-------------|
| `--color PRESET` | `drone_aerial` | Color grading preset (see [Color Presets](presets/color-presets.md)) |
| `--reframe MODE` | `smart` | Reframing mode: `smart`, `center`, `pan`, `thirds` |
| `--transition TYPE` | `crossfade` | Default transition: `cut`, `crossfade`, `fade_black`, `zoom_in` |
| `--clips INT` | auto | Number of clips to include (auto-calculated if not specified) |

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

# Square format for Instagram feed
drone-reel create -i ./clips/ --aspect 1:1 --reframe center

# Preview what clips will be selected
drone-reel create -i ./clips/ -d 30 --preview

# Keep original landscape format with color grading only
drone-reel create -i ./clips/ --no-reframe --color warm_sunset
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

Displays a table of all available color presets with descriptions.

```
          Available Color Presets
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Preset         ┃ Description                         ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ none           │ No color grading                    │
│ cinematic      │ Film-like with lifted blacks        │
│ warm_sunset    │ Warm golden tones                   │
│ cool_blue      │ Cool blue tones                     │
│ drone_aerial   │ Optimized for aerial drone footage  │
│ ...            │ ...                                 │
└────────────────┴─────────────────────────────────────┘
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
