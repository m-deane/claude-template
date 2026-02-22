# Python API Reference

drone-reel can be used as a Python library for programmatic video processing.

## Installation

```bash
pip install drone-reel
```

## Quick Start

```python
from pathlib import Path
from drone_reel import SceneDetector, BeatSync, VideoProcessor, ColorGrader, Reframer

# Detect scenes in a video
detector = SceneDetector()
scenes = detector.detect_scenes(Path("footage.mp4"))

# Analyze music beats
beat_sync = BeatSync()
beat_info = beat_sync.analyze(Path("music.mp3"))

# Process and stitch video
processor = VideoProcessor()
segments = processor.create_segments_from_scenes(scenes, durations=[3.0, 4.0, 3.0])
processor.stitch_clips(segments, Path("output.mp4"))
```

---

## Core Classes

### SceneDetector

Detects scenes in video files and scores them for visual interest.

```python
from drone_reel import SceneDetector

detector = SceneDetector(
    threshold=27.0,        # Scene detection sensitivity (lower = more scenes)
    min_scene_length=1.0,  # Minimum scene duration in seconds
    max_scene_length=10.0  # Maximum scene duration in seconds
)
```

#### Methods

**`detect_scenes(video_path: Path) -> list[SceneInfo]`**

Detect all scenes in a video file. If no scene changes are detected, treats the entire video as a single scene.

```python
scenes = detector.detect_scenes(Path("video.mp4"))
for scene in scenes:
    print(f"Scene at {scene.start_time:.1f}s - {scene.end_time:.1f}s (score: {scene.score:.1f})")
```

**`get_top_scenes(video_paths: list[Path], count: int = 10, min_per_video: int = 1) -> list[SceneInfo]`**

Get the top-scoring scenes from multiple videos.

```python
videos = [Path("clip1.mp4"), Path("clip2.mp4"), Path("clip3.mp4")]
best_scenes = detector.get_top_scenes(videos, count=5, min_per_video=1)
```

**`extract_thumbnail(scene: SceneInfo) -> np.ndarray`**

Extract a thumbnail image from the middle of a scene.

#### SceneInfo Data Class

```python
@dataclass
class SceneInfo:
    start_time: float      # Start time in seconds
    end_time: float        # End time in seconds
    duration: float        # Duration in seconds
    score: float           # Visual quality score (0-100)
    source_file: Path      # Source video file
    thumbnail: np.ndarray  # Optional thumbnail image

    @property
    def midpoint(self) -> float:  # Middle timestamp of the scene
```

---

### BeatSync

Analyzes music tracks to extract beat timing for video synchronization.

```python
from drone_reel.core.beat_sync import BeatSync

beat_sync = BeatSync(
    hop_length=512,     # Samples between analysis frames
    min_tempo=60.0,     # Minimum expected BPM
    max_tempo=180.0     # Maximum expected BPM
)
```

#### Methods

**`analyze(audio_path: Path) -> BeatInfo`**

Analyze an audio file to extract beat information.

```python
beat_info = beat_sync.analyze(Path("music.mp3"))
print(f"Tempo: {beat_info.tempo:.1f} BPM")
print(f"Total beats: {beat_info.beat_count}")
```

**`get_cut_points(beat_info, target_duration, min_clip_length=1.5, max_clip_length=4.0, prefer_downbeats=True) -> list[CutPoint]`**

Generate suggested cut points aligned with the music.

```python
cut_points = beat_sync.get_cut_points(
    beat_info,
    target_duration=45.0,
    min_clip_length=2.0,
    max_clip_length=5.0,
    prefer_downbeats=True
)
```

**`calculate_clip_durations(cut_points: list[CutPoint], target_duration: float) -> list[float]`**

Calculate duration for each clip between cut points.

**`get_energy_at_time(beat_info: BeatInfo, time: float) -> float`**

Get the normalized energy level (0-1) at a specific time.

**`suggest_transition_intensity(beat_info: BeatInfo, cut_point: CutPoint) -> str`**

Returns `'hard'`, `'medium'`, or `'soft'` based on beat strength and energy.

#### BeatInfo Data Class

```python
@dataclass
class BeatInfo:
    tempo: float                  # Detected tempo in BPM
    beat_times: np.ndarray        # Array of beat timestamps
    downbeat_times: np.ndarray    # Array of strong beat timestamps
    duration: float               # Track duration in seconds
    energy_profile: np.ndarray    # Normalized energy over time

    @property
    def beat_interval(self) -> float:  # Seconds between beats

    @property
    def beat_count(self) -> int:       # Total number of beats
```

#### CutPoint Data Class

```python
@dataclass
class CutPoint:
    time: float        # Suggested cut time in seconds
    strength: float    # Cut strength (0-1)
    is_downbeat: bool  # Whether this is on a strong beat
    beat_index: int    # Index in beat_times array
```

---

### VideoProcessor

Processes and stitches video clips with transitions.

```python
from drone_reel import VideoProcessor
from drone_reel.core.video_processor import TransitionType

processor = VideoProcessor(
    output_fps=30,
    output_codec="libx264",
    output_audio_codec="aac",
    preset="medium",    # FFmpeg preset: ultrafast, fast, medium, slow, veryslow
    threads=4
)
```

#### Methods

**`stitch_clips(segments, output_path, audio_path=None, target_size=None, progress_callback=None) -> Path`**

Stitch multiple clip segments into a single video.

```python
output = processor.stitch_clips(
    segments,
    Path("output.mp4"),
    audio_path=Path("music.mp3"),
    target_size=(1080, 1920),  # (width, height)
    progress_callback=lambda p: print(f"{p*100:.0f}%")
)
```

**`create_segments_from_scenes(scenes, clip_durations, transitions=None, transition_duration=0.3) -> list[ClipSegment]`**

Create ClipSegments from scenes with specified durations.

```python
segments = processor.create_segments_from_scenes(
    scenes[:5],
    clip_durations=[3.0, 4.0, 3.5, 4.0, 3.0],
    transitions=[TransitionType.CROSSFADE] * 4 + [TransitionType.FADE_BLACK],
    transition_duration=0.3
)
```

**`extract_clip(segment: ClipSegment, target_size=None) -> VideoFileClip`**

Extract a single clip segment from its source video.

**`get_video_info(video_path: Path) -> dict`**

Get information about a video file (duration, fps, size).

#### TransitionType Enum

```python
class TransitionType(Enum):
    # Basic
    CUT = "cut"
    CROSSFADE = "crossfade"
    FADE_BLACK = "fade_black"
    FADE_WHITE = "fade_white"
    # Zoom
    ZOOM_IN = "zoom_in"
    ZOOM_OUT = "zoom_out"
    # Slide & Wipe
    SLIDE_LEFT = "slide_left"
    SLIDE_RIGHT = "slide_right"
    WIPE_LEFT = "wipe_left"
    WIPE_RIGHT = "wipe_right"
    WIPE_DIAGONAL = "wipe_diagonal"
    WIPE_DIAMOND = "wipe_diamond"
    # Cinematic
    WHIP_PAN = "whip_pan"
    GLITCH_RGB = "glitch_rgb"
    IRIS_IN = "iris_in"
    IRIS_OUT = "iris_out"
    FLASH_WHITE = "flash_white"
    LIGHT_LEAK = "light_leak"
    HYPERLAPSE_ZOOM = "hyperlapse_zoom"
    # Depth & Motion
    PARALLAX_LEFT = "parallax_left"
    PARALLAX_RIGHT = "parallax_right"
    FOG_PASS = "fog_pass"
    VORTEX_ZOOM = "vortex_zoom"
```

#### ClipSegment Data Class

```python
@dataclass
class ClipSegment:
    scene: SceneInfo
    start_offset: float = 0.0           # Offset from scene start
    duration: Optional[float] = None     # Clip duration (None = full scene)
    transition_in: TransitionType = TransitionType.CUT
    transition_out: TransitionType = TransitionType.CUT
    transition_duration: float = 0.3

    @property
    def effective_start(self) -> float:    # Actual start time in source

    @property
    def effective_duration(self) -> float: # Actual duration to use
```

---

### ColorGrader

Applies color grading, visual effects, and color science corrections to video frames and clips.

```python
from drone_reel import ColorGrader
from drone_reel.core.color_grader import ColorPreset, ColorAdjustments

# Using a preset
grader = ColorGrader(preset=ColorPreset.CINEMATIC)

# Using custom adjustments
grader = ColorGrader(adjustments=ColorAdjustments(
    brightness=10,
    contrast=15,
    saturation=-5,
    temperature=20
))

# Full-featured setup
grader = ColorGrader(
    preset=ColorPreset.KODAK_2383,
    intensity=0.7,
    vignette_strength=0.4,
    halation_strength=0.3,
    chromatic_aberration_strength=0.2,
    input_colorspace="dlog_m",
    auto_wb=True,
    denoise_strength=0.3,
    haze_strength=0.15,
    gnd_sky_strength=0.4,
)
```

#### Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `preset` | `ColorPreset` | `NONE` | Color grading preset |
| `adjustments` | `ColorAdjustments` | `None` | Manual color adjustments (overrides preset) |
| `lut_path` | `Path` | `None` | Path to .cube LUT file |
| `tone_curve` | `ToneCurve` | `None` | Tone curve RGB adjustments |
| `use_gpu` | `bool` | `False` | Enable GPU acceleration |
| `intensity` | `float` | `1.0` | Scale all color adjustments (0.0-1.0) |
| `vignette_strength` | `float` | `0.0` | Radial edge darkening (0.0-1.0) |
| `halation_strength` | `float` | `0.0` | Warm highlight bloom (0.0-1.0) |
| `chromatic_aberration_strength` | `float` | `0.0` | RGB edge fringing (0.0-1.0) |
| `input_colorspace` | `str` | `"rec709"` | Input colorspace: `rec709`, `dlog`, `dlog_m`, `slog3` |
| `auto_wb` | `bool` | `False` | Gray world auto white balance |
| `denoise_strength` | `float` | `0.0` | Spatial denoising (0.0-1.0) |
| `haze_strength` | `float` | `0.0` | Atmospheric haze overlay (0.0-1.0) |
| `gnd_sky_strength` | `float` | `0.0` | Graduated ND sky darkening (0.0-1.0) |

#### Methods

**`grade_frame(frame: np.ndarray, frame_index: int = None) -> np.ndarray`**

Apply color grading to a single frame (BGR numpy array).

```python
import cv2
frame = cv2.imread("frame.jpg")
graded = grader.grade_frame(frame, frame_index=0)
cv2.imwrite("graded.jpg", graded)
```

**`grade_video(input_path: Path, output_path: Path, progress_callback=None) -> Path`**

Apply color grading to an entire video file.

```python
grader.grade_video(
    Path("input.mp4"),
    Path("graded.mp4"),
    progress_callback=lambda p: print(f"{p*100:.0f}%")
)
```

**`grade_frame_preview(frame: np.ndarray, scale: float = 0.25) -> np.ndarray`**

Apply color grading at reduced resolution for fast iteration.

**`set_reference_frame(frame: np.ndarray)`**

Set a reference frame for auto color matching. Call before grading clips that should match this reference.

**`detect_log_footage(video_path: Path) -> str`** *(static)*

Detect if footage is log-encoded by analyzing frame histogram. Returns `"dlog"` or `"rec709"`.

#### ColorPreset Enum

```python
class ColorPreset(Enum):
    # Classic
    NONE = "none"
    CINEMATIC = "cinematic"
    WARM_SUNSET = "warm_sunset"
    COOL_BLUE = "cool_blue"
    VINTAGE = "vintage"
    HIGH_CONTRAST = "high_contrast"
    MUTED = "muted"
    VIBRANT = "vibrant"
    TEAL_ORANGE = "teal_orange"
    BLACK_WHITE = "black_white"
    DRONE_AERIAL = "drone_aerial"
    # Time-of-day
    GOLDEN_HOUR = "golden_hour"
    BLUE_HOUR = "blue_hour"
    HARSH_MIDDAY = "harsh_midday"
    OVERCAST = "overcast"
    NIGHT_CITY = "night_city"
    # Terrain-aware
    OCEAN_COASTAL = "ocean_coastal"
    FOREST_JUNGLE = "forest_jungle"
    URBAN_CITY = "urban_city"
    DESERT_ARID = "desert_arid"
    SNOW_MOUNTAIN = "snow_mountain"
    AUTUMN_FOLIAGE = "autumn_foliage"
    # Cinematic film emulation
    KODAK_2383 = "kodak_2383"
    FUJIFILM_3513 = "fujifilm_3513"
    TECHNICOLOR_2STRIP = "technicolor_2strip"
    # Social media trends
    DESATURATED_MOODY = "desaturated_moody"
    WARM_PASTEL = "warm_pastel"
    CYBERPUNK_NEON = "cyberpunk_neon"
    HYPER_NATURAL = "hyper_natural"
    FILM_EMULATION = "film_emulation"
```

#### ColorAdjustments Data Class

```python
@dataclass
class ColorAdjustments:
    brightness: float = 0.0    # -100 to 100
    contrast: float = 0.0      # -100 to 100
    saturation: float = 0.0    # -100 to 100
    temperature: float = 0.0   # -100 (cool) to 100 (warm)
    tint: float = 0.0          # -100 (green) to 100 (magenta)
    shadows: float = 0.0       # -100 to 100
    highlights: float = 0.0    # -100 to 100
    vibrance: float = 0.0      # -100 to 100
    fade: float = 0.0          # 0 to 100 (lifts blacks)
    grain: float = 0.0         # 0 to 100
    selective_color: SelectiveColorAdjustments  # Per-color adjustments
```

---

### Reframer

Reframes video content for different aspect ratios.

```python
from drone_reel import Reframer
from drone_reel.core.reframer import ReframeSettings, AspectRatio, ReframeMode

reframer = Reframer(settings=ReframeSettings(
    target_ratio=AspectRatio.VERTICAL_9_16,
    mode=ReframeMode.SMART,
    output_width=1080
))
```

#### Methods

**`reframe_video(input_path: Path, output_path: Path, progress_callback=None) -> Path`**

Reframe an entire video file.

```python
reframer.reframe_video(
    Path("landscape.mp4"),
    Path("vertical.mp4"),
    progress_callback=lambda p: print(f"{p*100:.0f}%")
)
```

**`reframe_frame(frame: np.ndarray, frame_index=0, total_frames=1) -> np.ndarray`**

Reframe a single frame.

**`calculate_output_dimensions(input_width, input_height) -> tuple[int, int]`**

Calculate output dimensions for the target aspect ratio.

**`calculate_crop_region(frame, output_width, output_height, frame_index=0, total_frames=1) -> tuple[int, int, int, int]`**

Calculate the crop region (x, y, width, height) for a frame.

**`reset_tracking()`**

Reset tracking history (call before processing a new video in SMART mode).

#### AspectRatio Enum

```python
class AspectRatio(Enum):
    VERTICAL_9_16 = (9, 16)   # Instagram Reels, TikTok, Shorts
    SQUARE_1_1 = (1, 1)       # Instagram Feed
    LANDSCAPE_16_9 = (16, 9)  # YouTube, standard HD
    PORTRAIT_4_5 = (4, 5)     # Instagram Portrait
    CINEMATIC_21_9 = (21, 9)  # Ultra-wide cinematic
```

#### ReframeMode Enum

```python
class ReframeMode(Enum):
    CENTER = "center"   # Center crop
    SMART = "smart"     # Saliency-based subject tracking
    PAN = "pan"         # Slow pan across the frame
    THIRDS = "thirds"   # Follow rule of thirds
    CUSTOM = "custom"   # Custom focal point
```

#### ReframeSettings Data Class

```python
@dataclass
class ReframeSettings:
    target_ratio: AspectRatio = AspectRatio.VERTICAL_9_16
    mode: ReframeMode = ReframeMode.SMART
    output_width: int = 1080
    pan_speed: float = 0.1              # For PAN mode
    focal_point: tuple[float, float] = (0.5, 0.5)  # For CUSTOM mode (0-1)
    smooth_tracking: bool = True
    tracking_smoothness: float = 0.3    # Lower = smoother
```

---

## Utility Functions

### File Utilities

```python
from drone_reel.utils.file_utils import (
    find_video_files,
    find_audio_files,
    ensure_output_dir,
    get_unique_output_path,
    format_duration,
    format_file_size
)

# Find all videos in a directory
videos = find_video_files(Path("./clips"), recursive=True)

# Format duration for display
print(format_duration(125.5))  # "2:05"

# Get unique filename if collision
output = get_unique_output_path(Path("reel.mp4"))  # Returns "reel_1.mp4" if exists
```

### Configuration

```python
from drone_reel.utils.config import Config, load_config, save_config, merge_cli_args

# Load user configuration
config = load_config()

# Merge with CLI arguments
config = merge_cli_args(config, output_duration=60, color_preset="cinematic")

# Save configuration
save_config(config)
```

### Transition Presets

```python
from drone_reel.presets.transitions import (
    get_transitions_for_energy,
    get_random_transitions,
    get_transition_duration
)

# Get transitions based on music energy level
transitions = get_transitions_for_energy(
    energy_level=0.8,  # 0-1
    count=10,
    style="dynamic"    # or "smooth", "punchy"
)
```

---

## Complete Example

```python
from pathlib import Path
from drone_reel import SceneDetector, BeatSync, VideoProcessor, ColorGrader
from drone_reel.core.video_processor import TransitionType
from drone_reel.core.color_grader import ColorPreset
from drone_reel.utils.file_utils import find_video_files

# 1. Find source videos
video_files = find_video_files(Path("./drone_clips"))

# 2. Detect and score scenes
detector = SceneDetector(threshold=25.0)
best_scenes = detector.get_top_scenes(video_files, count=10)

# 3. Analyze music
beat_sync = BeatSync()
beat_info = beat_sync.analyze(Path("./music.mp3"))
cut_points = beat_sync.get_cut_points(beat_info, target_duration=45.0)
durations = beat_sync.calculate_clip_durations(cut_points, 45.0)

# 4. Create segments with transitions
processor = VideoProcessor(output_fps=30)
segments = processor.create_segments_from_scenes(
    best_scenes[:len(durations)],
    durations,
    transitions=[TransitionType.CROSSFADE] * (len(durations) - 1) + [TransitionType.FADE_BLACK]
)

# 5. Stitch video
temp_output = Path("./output/temp.mp4")
processor.stitch_clips(
    segments,
    temp_output,
    audio_path=Path("./music.mp3"),
    target_size=(1080, 1920)  # 9:16 vertical
)

# 6. Apply color grading with visual effects
grader = ColorGrader(
    preset=ColorPreset.DRONE_AERIAL,
    intensity=0.7,
    vignette_strength=0.3,
    halation_strength=0.2,
    input_colorspace="dlog_m",
    auto_wb=True,
)
final_output = Path("./output/final_reel.mp4")
grader.grade_video(temp_output, final_output)

print(f"Reel created: {final_output}")
```
