# drone-reel Quick Start

## Install

```bash
git clone <repo>
cd drone-reel
pip install -e ".[dev]"
```

---

## The two main commands

| Command | Use case |
|---------|----------|
| `drone-reel create` | Sequence clips from a folder into a single beat-synced reel |
| `drone-reel split` | Split one long video into graded highlight clips |

---

## `drone-reel create`

Turn a folder of clips into a vertical reel.

```bash
drone-reel create -i ./clips/ -o reel.mp4
```

### All parameters

#### Required

| Flag | Description |
|------|-------------|
| `-i / --input PATH` | Input folder or single video file |

#### Output

| Flag | Default | Options | Description |
|------|---------|---------|-------------|
| `-o / --output PATH` | `./output/reel.mp4` | any path | Output file |
| `-d / --duration FLOAT` | `45.0` | 0.5–600 | Target length in seconds |
| `--aspect` | `9:16` | `9:16` `1:1` `4:5` `16:9` | Output aspect ratio |
| `--quality` | `medium` | `low` `medium` `high` `ultra` | Bitrate: 5M / 10M / 15M / 25M |
| `--resolution` | `hd` | `hd` `2k` `4k` | Output resolution: 1080p / 1440p / 2160p |
| `--platform` | — | see below | Platform preset (overrides aspect/resolution) |
| `--clips INT` | auto | 1–∞ | Force a specific clip count |
| `--preview` | off | flag | Show plan without encoding |

Platform options: `instagram_reels` `instagram_feed` `tiktok` `youtube_shorts` `youtube` `youtube_4k` `pinterest` `twitter` `vertical_4k`

#### Audio & beat sync

| Flag | Default | Description |
|------|---------|-------------|
| `-m / --music PATH` | — | Music file for beat-synced cuts |
| `--beat-mode` | `all` | `all` = every beat · `downbeat` = strong beats only |
| `--duck-outro` | off | Fade audio over final 2s |

#### Color grading

| Flag | Default | Description |
|------|---------|-------------|
| `-c / --color PRESET` | `drone_aerial` | Color preset — run `drone-reel presets` for full list |
| `--color-intensity FLOAT` | `1.0` | Scale all preset adjustments 0.0–1.0 |
| `--no-color` | off | Skip color grading entirely |
| `--lut PATH` | — | Apply a `.cube` 3D LUT instead of or on top of a preset |

#### Color science

| Flag | Default | Description |
|------|---------|-------------|
| `--input-colorspace` | `rec709` | `rec709` `dlog` `dlog_m` `slog3` `auto` — converts log footage to Rec.709 |
| `--auto-wb` | off | Gray world auto white balance |
| `--auto-color-match` | off | Histogram-match all clips to the first clip |
| `--denoise FLOAT` | `0.0` | Noise reduction 0.0–1.0 |

#### Visual effects

| Flag | Default | Range | Description |
|------|---------|-------|-------------|
| `--vignette FLOAT` | `0.0` | 0–1 | Sigmoid edge darkening (0.3 subtle · 0.6 cinematic) |
| `--halation FLOAT` | `0.0` | 0–1 | Warm highlight bloom (0.3 subtle · 0.7 cinematic) |
| `--chromatic-aberration FLOAT` | `0.0` | 0–1 | RGB edge fringing |
| `--haze FLOAT` | `0.0` | 0–1 | Atmospheric depth haze |
| `--gnd-sky FLOAT` | `0.0` | 0–1 | Graduated sky darkening |
| `--letterbox` | `off` | `off` `2.35` `1.85` `2.39` | Cinematic black bars |

#### Stabilization

| Flag | Default | Description |
|------|---------|-------------|
| `--stabilize` | off | Adaptive stabilization (auto-detects shaky clips) |
| `--stabilize-all` | off | Force stabilization on every clip |
| `--stable-threshold FLOAT` | `15.0` | Shake score threshold — lower stabilizes more clips |
| `--stab-strength` | `adaptive` | `off` `light` `adaptive` `full` — off skips entirely, light always applies mild correction, full always applies full correction |
| `--smooth-radius INT` | `50` | 5–120 · Optical-flow smoothing window (larger = smoother, slower) |
| `--border-crop FLOAT` | `0.05` | 0.0–0.15 · Border crop fraction after stabilization |
| `--max-corners INT` | `200` | 50–500 · Feature tracking points (more = more accurate, slower) |

#### Motion & speed

| Flag | Default | Description |
|------|---------|-------------|
| `--speed-ramp` | off | Slow-mo on hook moments, speed-up at transitions |
| `--reframe` | `smart` | `smart` `center` `pan` `thirds` — how to crop to target aspect |
| `--no-reframe` | off | Keep source aspect ratio |
| `--ken-burns` | `off` | `off` `conservative` `moderate` `cinematic` — animated zoom/pan on stills |
| `--kb-zoom-end FLOAT` | — | Ken Burns end zoom factor 1.0–2.0 |
| `--kb-pan-x FLOAT` | — | Ken Burns horizontal pan 0.0–0.3 |
| `--kb-pan-y FLOAT` | — | Ken Burns vertical pan 0.0–0.2 |

#### Transitions

| Flag | Default | Description |
|------|---------|-------------|
| `--transition TYPE` | `crossfade` | Default cut transition type |

Available transitions: `cut` `crossfade` `fade_black` `zoom_in` `whip_pan` `glitch_rgb` `iris_in` `iris_out` `flash_white` `light_leak` `hyperlapse_zoom` `parallax_left` `parallax_right` `wipe_diagonal` `wipe_diamond` `fog_pass` `vortex_zoom`

#### Text

| Flag | Default | Description |
|------|---------|-------------|
| `--caption TEXT` | — | Lower-third text overlay with 3s fade animation |

#### Presets

| Flag | Description |
|------|-------------|
| `--viral` | One-flag shortcut: 15s · Instagram Reels · 60% color · speed ramp |

---

### `create` example recipes

```bash
# Minimal: clips → reel
drone-reel create -i ./clips/ -o reel.mp4

# Instagram Reels with viral preset
drone-reel create -i ./clips/ --viral

# Beat-synced 30s reel with cinematic look
drone-reel create -i ./clips/ -m track.mp3 -d 30 \
  --color drone_aerial --color-intensity 0.7 \
  --vignette 0.4 --letterbox 2.35

# DJI D-Log footage
drone-reel create -i ./clips/ --input-colorspace dlog \
  --auto-wb --color film_emulation --color-intensity 0.6

# TikTok with golden hour grade and stabilization
drone-reel create -i ./clips/ --platform tiktok -d 15 \
  --color golden_hour --color-intensity 0.8 --stabilize-all

# Dry run — see which clips will be selected
drone-reel create -i ./clips/ -d 30 --preview
```

---

## `drone-reel split`

Detect scenes in one video file and export graded highlights.

```bash
drone-reel split -i video.mp4 -o ./highlights/
```

### All parameters

#### Required

| Flag | Description |
|------|-------------|
| `-i / --input PATH` | Single video file |

#### Output

| Flag | Default | Options | Description |
|------|---------|---------|-------------|
| `-o / --output-dir PATH` | `./highlights` | any path | Output folder |
| `-q / --quality` | `high` | `low` `medium` `high` `ultra` | Bitrate: 5M / 10M / 15M / 25M |
| `--resolution` | `source` | `source` `hd` `2k` `4k` | Output resolution |
| `--json` | off | flag | Write `manifest.json` with per-clip metadata |
| `--overwrite` | off | flag | Replace existing clips |
| `--preview` | off | flag | Print scene table, no export |

#### Scene selection

| Flag | Default | Range | Description |
|------|---------|-------|-------------|
| `--min-score FLOAT` | `40.0` | 0–100 | Minimum scene quality score |
| `--min-duration FLOAT` | `2.0` | 0.5–300 | Shortest clip to export (seconds) |
| `--max-duration FLOAT` | `15.0` | 1.0–300 | Longest clip — scenes longer than this are chunked into multiple clips |
| `-n / --count INT` | unlimited | 1–100 | Cap total clips exported |
| `-s / --sort` | `score` | `score` `chronological` `duration` | Output ordering |
| `--no-filter` | off | flag | Skip quality filtering — export all detected scenes |
| `--scene-threshold FLOAT` | `27.0` | 1–100 | Detection sensitivity (lower = more scene boundaries) |
| `--enhanced` | off | flag | Enhanced detection with subject tracking (slower) |
| `--analysis-scale FLOAT` | `0.5` | 0.1–1.0 | Frame downscale factor for analysis (lower = faster) |
| `--motion-energy-method` | `mean` | `mean` `median` `p95` | How to aggregate per-frame motion scores |
| `--prefer-motion-type TEXT` | `none` | | Comma-separated motion types to float to front e.g. `flyover,pan_right` |

> **Tip:** For clips ≥ 11s use `--scene-threshold 7–12` to merge micro-cuts into longer coherent scenes. At the default of 27 most footage produces very short scenes.

#### Scene filtering

Fine-tune which scenes pass the quality filter:

| Flag | Default | Range | Description |
|------|---------|-------|-------------|
| `--brightness-range TEXT` | `30-245` | | Allowed brightness bounds `MIN-MAX` — scenes outside range are filtered |
| `--motion-threshold FLOAT` | — | 0–100 | Minimum motion energy required |
| `--shake-tolerance FLOAT` | — | 0–100 | Maximum allowed shake score |
| `--subject-confidence FLOAT` | — | 0.0–1.0 | Minimum subject detection confidence |

#### Motion correction

| Flag | Default | Description |
|------|---------|-------------|
| `--auto-speed` | off | Auto-correct pan/tilt speed — slows fast pans (0.65–0.80×), speeds up sluggish ones (1.25×), corrects fast tilts/flyovers/FPV |
| `--stabilize` | off | Adaptive shake stabilization (skips stable clips) |
| `--stabilize-all` | off | Force optical-flow stabilization on every clip |

Auto-speed correction table (`normal` profile):

| Motion type | Energy | Speed factor |
|-------------|--------|-------------|
| PAN_LEFT / PAN_RIGHT | > 70 | **0.65×** slow down |
| PAN_LEFT / PAN_RIGHT | 55–70 | **0.80×** slow down |
| PAN_LEFT / PAN_RIGHT | 5–20 | **1.25×** speed up |
| TILT_UP / TILT_DOWN | > 65 | **0.70×** slow down |
| FLYOVER / APPROACH | > 70 | **0.70×** slow down |
| FPV | > 50 | **0.75×** slow down |
| STATIC / ORBIT / REVEAL | any | no change |

Auto-speed tuning (`--auto-speed` must be set):

| Flag | Default | Description |
|------|---------|-------------|
| `--speed-correction-profile` | `normal` | `aggressive` `normal` `smooth` `cinematic` — preset speed factors for all motion types |
| `--pan-speed-high FLOAT` | — | 0.1–1.5 · Override profile speed for high-energy pans (energy > 70) |
| `--pan-speed-mid FLOAT` | — | 0.1–1.5 · Override profile speed for mid-energy pans (energy 55–70) |
| `--tilt-speed FLOAT` | — | 0.1–1.5 · Override profile speed for fast tilts |
| `--fpv-speed FLOAT` | — | 0.1–1.5 · Override profile speed for FPV shots |
| `--correct-orbit` | off | flag · Apply gentle 0.85× correction to orbit shots |
| `--ease-speed-ramps` | off | flag · Ease in/out of speed corrections (15% ramp-in · 70% constant · 15% ramp-out) |
| `--vertical-drift-damping FLOAT` | `0.0` | 0.0–1.0 · Extra slowdown on tilt-down clips to reduce vertical drift |

Speed profile comparison:

| Profile | PAN high | PAN mid | TILT | FPV | FLYOVER |
|---------|----------|---------|------|-----|---------|
| `aggressive` | 0.55× | 0.70× | 0.60× | 0.65× | 0.60× |
| `normal` | 0.65× | 0.80× | 0.70× | 0.75× | 0.70× |
| `cinematic` | 0.60× | 0.75× | 0.65× | 0.70× | 0.65× |
| `smooth` | 0.75× | 0.85× | 0.80× | 0.80× | 0.80× |

Stabilization tuning:

| Flag | Default | Description |
|------|---------|-------------|
| `--stab-strength` | `adaptive` | `off` `light` `adaptive` `full` — off skips entirely, light always applies mild correction, full always applies full correction |
| `--smooth-radius INT` | `50` | 5–120 · Optical-flow smoothing window |
| `--border-crop FLOAT` | `0.05` | 0.0–0.15 · Border crop fraction after stabilization |
| `--max-corners INT` | `200` | 50–500 · Feature tracking points |

#### Color grading (same as `create`)

| Flag | Default | Description |
|------|---------|-------------|
| `-c / --color PRESET` | `none` | Color preset |
| `--color-intensity FLOAT` | `1.0` | Scale preset strength 0.0–1.0 |
| `--input-colorspace` | `rec709` | `rec709` `dlog` `dlog_m` `slog3` `auto` |
| `--auto-wb` | off | Auto white balance |
| `--denoise FLOAT` | `0.0` | Noise reduction 0.0–1.0 |
| `--lut PATH` | — | `.cube` LUT file |

#### Visual effects (same as `create`)

| Flag | Default | Range | Description |
|------|---------|-------|-------------|
| `--vignette FLOAT` | `0.0` | 0–1 | Edge darkening |
| `--halation FLOAT` | `0.0` | 0–1 | Highlight bloom |
| `--chromatic-aberration FLOAT` | `0.0` | 0–1 | RGB fringing |
| `--haze FLOAT` | `0.0` | 0–1 | Atmospheric haze |
| `--gnd-sky FLOAT` | `0.0` | 0–1 | Sky darkening |
| `--letterbox` | `off` | `off` `2.35` `1.85` `2.39` | Cinematic bars |

---

### `split` example recipes

```bash
# Preview scenes before committing to export
drone-reel split -i clip.mp4 -o ./out --preview

# Best 5–15s highlights with cinematic grade
drone-reel split -i clip.mp4 -o ./out \
  --min-duration 5 --max-duration 15 \
  --min-score 0 --no-filter \
  --color drone_aerial --color-intensity 0.65 \
  --vignette 0.3 --letterbox 2.35 \
  --auto-speed --quality high --json

# Long highlights 11–17s (chunked from long scenes)
drone-reel split -i clip.mp4 -o ./out \
  --min-duration 11 --max-duration 17 \
  --min-score 0 --no-filter \
  --scene-threshold 7 \
  --color drone_aerial --color-intensity 0.65 \
  --vignette 0.3 --auto-speed --letterbox 2.35 \
  --quality high --json

# DJI 4K HEVC — create 720p proxy first
ffmpeg -i DJI_SOURCE.MP4 -vf scale=1280:720 -r 30 \
  -c:v libx264 -preset ultrafast -crf 26 -an proxy.mp4

drone-reel split -i proxy.mp4 -o ./out \
  --min-duration 5 --max-duration 15 \
  --input-colorspace dlog \
  --color drone_aerial --auto-speed --letterbox 2.35 --json
```

Output files: `split_NNN_sSCORE.mp4` — e.g. `split_001_s72.mp4` = clip #1, score 72.

---

## Utility commands

```bash
drone-reel analyze -i video.mp4     # Scene table: start/end/duration/score
drone-reel beats -i track.mp3       # BPM, downbeats, beat timestamps
drone-reel presets                  # All 30 color presets
drone-reel platforms                # Platform export specs
```

---

## Color presets

Run `drone-reel presets` for the full list. Key ones:

| Preset | Character |
|--------|-----------|
| `drone_aerial` | Boosted contrast + saturation, cool tone — default for aerials |
| `golden_hour` | Warm amber, lifted shadows, high contrast |
| `film_emulation` | Slight desaturation, warm highlights, lifted blacks |
| `blue_hour` | Cool blue/purple, lifted shadows |
| `kodak_2383` | Warm film print with lifted blacks |
| `fujifilm_3513` | Cool neutral film with pastel tone |
| `cyberpunk_neon` | High saturation, teal/magenta push |
| `hyper_natural` | High-saturation natural colours |
| `desaturated_moody` | Muted, desaturated, moody |
| `snow_mountain` | Cold whites, high clarity |

---

## Performance notes

**4K HEVC footage** (DJI, GoPro) is slow to process because OpenCV random-seeks in H.265 require full GOP re-decode. Always create a 720p H.264 proxy first:

```bash
ffmpeg -i source.MP4 -vf scale=1280:720 -r 30 \
  -c:v libx264 -preset ultrafast -crf 26 -an proxy.mp4
```

**Stabilizer** adds ~30–60s per clip depending on resolution. Use `--stabilize` (adaptive) rather than `--stabilize-all` if only some clips are shaky. Use `--stab-strength light` for a faster, gentler pass.

**Auto-speed** (`--auto-speed`) runs optical-flow analysis per clip to measure motion energy, then applies constant-speed time-transform. Adds a few seconds per clip. Use `--ease-speed-ramps` for smoother transitions in/out of corrections.

---

## Verification (after any change)

```bash
ruff check src/ tests/ && black --check src/ tests/ && pytest -x
```
