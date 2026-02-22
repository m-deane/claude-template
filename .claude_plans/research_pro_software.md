# Professional Drone Editing Software Feature Analysis
## Missing Features for drone-reel CLI Tool

**Research Date**: 2026-02-21
**Researcher**: Technical Research Agent
**Task**: Identify automatable drone/aerial features from DaVinci Resolve, CapCut, Adobe Premiere, Final Cut Pro, LumaFusion that are NOT in drone-reel

---

## Existing Features (Already Implemented - DO NOT RE-IMPLEMENT)

- Color presets: cinematic, warm_sunset, cool_blue, vintage, high_contrast, muted, vibrant, teal_orange, black_white, drone_aerial
- Transitions: cut, crossfade, fade_black, zoom_in
- Reframe modes: center, smart, ken_burns, punch_in, subject_track
- Adaptive/full stabilization (feature-based optical flow)
- Speed ramping with auto-detect (SpeedRamper module)
- Text overlays with fade animation (TextOverlay module)
- Beat-synced editing (BeatSync module with downbeat detection)
- BT.709 color space
- Shadow lift / fade (black lift in ColorAdjustments)
- SelectiveColorAdjustments (HSL per color range)
- ToneCurve per channel (R/G/B)
- LUT support (1D LUT via lookup table in ColorGrader)
- Grain parameter in ColorAdjustments
- Sharpness scoring and scene filtering
- Scene diversity selection

---

## TOP 20 MISSING FEATURES - Ranked by Viral Readiness Impact

---

### #1 - 3D LUT (.cube) File Loading and Application
**Source Tool**: DaVinci Resolve, Adobe Premiere Pro
**Priority**: MUST-HAVE

**Description**:
Load industry-standard .cube LUT files (33x33x33 or 64x64x64 3D color lookup tables) and apply them to video frames. The current `ColorGrader` only supports 1D lookup tables mapped per-channel, not true 3D LUTs that remap all three channels jointly. Cinematic drone LUT packs (DJI D-Log to Rec.709, Mavic drone presets, "Orange and Teal" LUTs) are the single most impactful visual upgrade for professional aerial footage.

**How it applies to drone footage**:
DJI cameras record in D-Log M (flat profile) for maximum dynamic range. Professional colorists apply camera-specific D-Log-to-Rec.709 LUTs as first step, then creative LUTs for the final look. Without 3D LUT support, flat D-Log footage cannot be properly graded.

**Implementation**:
```python
# Using pycubelut or pylut library
import numpy as np

def load_cube_lut(path: str) -> np.ndarray:
    """Load .cube file, return (size, size, size, 3) array."""
    # Parse header for LUT_3D_SIZE
    # Build trilinear interpolation lookup
    pass

def apply_3d_lut(frame: np.ndarray, lut: np.ndarray) -> np.ndarray:
    """Apply 3D LUT via trilinear interpolation per frame."""
    # Normalize 0-1, interpolate in LUT cube, return uint8
    pass
```
Or use `colour-science` library: `colour.LUT3D` with `colour.apply_lut_3d()`.

**Complexity**: ~150 LOC (parsing + trilinear interpolation + integration into ColorGrader)
**Dependencies**: `colour-science` or `pycubelut` (both available via pip)

---

### #2 - Vignette Effect (Graduated Lens Darkening)
**Source Tool**: DaVinci Resolve, Adobe Premiere Pro, Final Cut Pro, LumaFusion
**Priority**: MUST-HAVE

**Description**:
Apply a radial gradient darkening toward frame edges. This is one of the most universally used cinematic effects - it draws viewer attention to the center subject and adds a professional, filmic look. DaVinci Resolve has a dedicated Vignette node; Premiere Pro has it in Lumetri Color.

**How it applies to drone footage**:
Aerial footage often has bright horizons and expansive skies that compete with the primary subject. A vignette grounds the composition and focuses the eye.

**Implementation**:
```python
def apply_vignette(frame: np.ndarray, strength: float = 0.5,
                   radius: float = 0.75, softness: float = 0.5) -> np.ndarray:
    """Apply radial vignette using numpy distance mask."""
    h, w = frame.shape[:2]
    cx, cy = w / 2, h / 2
    Y, X = np.ogrid[:h, :w]
    dist = np.sqrt(((X - cx) / cx) ** 2 + ((Y - cy) / cy) ** 2)
    # Sigmoid falloff for soft edges
    mask = 1 - np.clip((dist - radius) / softness, 0, 1) * strength
    return (frame * mask[..., np.newaxis]).astype(np.uint8)
```

**Complexity**: ~60 LOC (numpy only, no new dependencies, add to `ColorGrader`)
**Dependencies**: numpy (already installed)

---

### #3 - Chromatic Aberration (Fringing) Effect
**Source Tool**: Adobe Premiere Pro, DaVinci Resolve, CapCut
**Priority**: MUST-HAVE

**Description**:
Simulate or correct lens chromatic aberration - the slight lateral offset of color channels (red/green/blue) toward frame edges. Used creatively as a cinematic stylization in viral drone videos: adds texture and energy to transitions and action sequences. Also used as "glitch" effect for modern edits.

**How it applies to drone footage**:
FPV and wide-angle drone lenses naturally exhibit chromatic aberration. Intentional artistic CA adds a stylized "action cam" or lo-fi cinematic look highly popular in TikTok/Instagram drone reels.

**Implementation**:
```python
def apply_chromatic_aberration(frame: np.ndarray,
                                strength: float = 3.0) -> np.ndarray:
    """Shift R and B channels outward from center."""
    h, w = frame.shape[:2]
    b, g, r = cv2.split(frame)
    # Compute pixel shift map relative to center
    M_r = np.float32([[1, 0, strength], [0, 1, 0]])   # shift R right
    M_b = np.float32([[1, 0, -strength], [0, 1, 0]])   # shift B left
    r_shifted = cv2.warpAffine(r, M_r, (w, h))
    b_shifted = cv2.warpAffine(b, M_b, (w, h))
    return cv2.merge([b_shifted, g, r_shifted])
```

**Complexity**: ~80 LOC (OpenCV warpAffine per channel, radial variant adds ~30 LOC)
**Dependencies**: OpenCV (already installed)

---

### #4 - Halation / Bloom Effect (Highlight Bleed)
**Source Tool**: DaVinci Resolve (Film Look Creator), FilmConvert, Dehancer
**Priority**: MUST-HAVE

**Description**:
Halation is the red-orange glow/halo that appears around bright highlights on analog film, caused by light reflecting off the film base. Bloom is the softer version where bright areas "bleed" luminance into surrounding pixels. Both are heavily used in cinematic drone editing to create a warm, organic, filmic feel.

**How it applies to drone footage**:
Drone footage in golden hour or looking into the sun creates natural bright spots. Halation makes these look cinematic rather than digital/clinical. Extremely popular in 2024-2026 viral drone aesthetics.

**Implementation**:
```python
def apply_halation(frame: np.ndarray, strength: float = 0.3,
                   radius: int = 21) -> np.ndarray:
    """Apply halation: blur red channel highlights and blend back."""
    b, g, r = cv2.split(frame.astype(np.float32))
    # Extract highlights from red channel
    highlights = np.clip(r - 200, 0, None)
    # Gaussian blur the highlights
    blurred = cv2.GaussianBlur(highlights, (radius | 1, radius | 1), 0)
    r_halo = np.clip(r + blurred * strength, 0, 255)
    return cv2.merge([b, g, r_halo]).astype(np.uint8)
```

**Complexity**: ~70 LOC (OpenCV Gaussian blur on highlight mask)
**Dependencies**: OpenCV (already installed)

---

### #5 - Lens Distortion Correction / Fisheye Removal
**Source Tool**: Adobe Premiere Pro, DaVinci Resolve, GoPro Player
**Priority**: MUST-HAVE

**Description**:
Wide-angle drone lenses (DJI Mini/Air/Mavic series) and especially FPV cameras introduce barrel distortion (fisheye). Premiere Pro includes lens correction profiles for DJI cameras. Automatable correction using OpenCV undistortion or lensfunpy lens database.

**How it applies to drone footage**:
FPV footage without correction looks amateur/raw. Even standard DJI footage benefits from slight distortion correction for cinematic rectilinear projection. Critical for real estate and professional content.

**Implementation**:
```python
# Using OpenCV camera calibration parameters
def correct_lens_distortion(frame: np.ndarray,
                             k1: float = -0.3, k2: float = 0.1) -> np.ndarray:
    """Correct barrel/pincushion distortion using radial coefficients."""
    h, w = frame.shape[:2]
    cam_matrix = np.array([[w, 0, w/2], [0, w, h/2], [0, 0, 1]], dtype=np.float64)
    dist_coeffs = np.array([k1, k2, 0, 0, 0])
    map1, map2 = cv2.initUndistortRectifyMap(cam_matrix, dist_coeffs,
                                              None, cam_matrix, (w, h), cv2.CV_32FC1)
    return cv2.remap(frame, map1, map2, cv2.INTER_LINEAR)
```

**Complexity**: ~100 LOC (calibration profiles for DJI Mavic/Mini/Air cameras, CLI `--lens-model` flag)
**Dependencies**: OpenCV (already installed); optional `lensfunpy` for accurate profiles

---

### #6 - Auto Color Match / Scene Color Consistency
**Source Tool**: Adobe Premiere Pro (Auto Color Match), DaVinci Resolve (Color Warper)
**Priority**: MUST-HAVE

**Description**:
Automatically normalize color across clips from different lighting conditions (golden hour vs. midday vs. shade). Premiere Pro uses histogram/shadow-midtone-highlight matching. In a multi-clip reel from one shoot, clips can have wildly different exposures. Auto-matching creates visual coherence.

**How it applies to drone footage**:
Drone shoots often span multiple time periods or lighting conditions. Auto color matching makes a reel feel like it was shot in one continuous session rather than pieced together.

**Implementation**:
```python
# Using color-matcher library or scikit-image histogram matching
from skimage.exposure import match_histograms

def auto_color_match(source_frame: np.ndarray,
                     reference_frame: np.ndarray) -> np.ndarray:
    """Match source color distribution to reference frame."""
    return match_histograms(source_frame, reference_frame, channel_axis=-1)

def normalize_clip_colors(clips: list, reference_clip_idx: int = 0):
    """Apply color matching from reference to all other clips."""
    pass
```

**Complexity**: ~120 LOC (reference frame selection, per-clip normalization pass, integration into pipeline)
**Dependencies**: `scikit-image` (already in scipy ecosystem, likely installed)

---

### #7 - Audio Ducking (Dynamic Music Volume Reduction)
**Source Tool**: DaVinci Resolve (Fairlight), Adobe Premiere Pro, CapCut, Filmora
**Priority**: MUST-HAVE

**Description**:
Automatically lower music volume at the end of the reel or at specific moments (e.g., before a title card, during a slow-mo sequence). DaVinci Resolve Fairlight has auto-ducking via sidechain compression. For reels, this typically means a smooth fade-out in the final 2-3 seconds.

**How it applies to drone footage**:
Viral drone reels typically have music fade out at the end rather than hard-cutting. Auto ducking also smooths the music when transitioning between scenes with different energy levels.

**Implementation**:
```python
# In BeatSync or VideoProcessor module
def apply_audio_duck(audio_clip, duck_start: float, duck_duration: float = 2.0,
                     target_db: float = -20.0):
    """Exponential volume fadeout for end-of-reel ducking."""
    # Use moviepy audio manipulation
    # audio_clip.with_volume_scaled(lambda t: ...)
    pass

def auto_duck_outro(reel_clip, duck_seconds: float = 2.5):
    """Apply automatic volume duck in final N seconds of reel."""
    pass
```

**Complexity**: ~80 LOC (MoviePy audio transform, BeatSync integration, `--duck-outro` CLI flag)
**Dependencies**: MoviePy (already installed)

---

### #8 - Film Grain (Cinematic Noise Overlay)
**Source Tool**: DaVinci Resolve (Film Look Creator), FilmConvert, CapCut
**Priority**: MUST-HAVE

**Description**:
The existing `ColorAdjustments.grain` parameter applies grain but its implementation needs verification. A proper film grain implementation uses temporally varying Gaussian noise with size-scaled particles (not per-pixel random noise) and luminance-weighted application (more grain in midtones/shadows, less in highlights).

**How it applies to drone footage**:
Digital drone footage can look overly clean/sterile. Film grain adds organic texture and warmth. Highly used in cinematic aerial reels. DaVinci Resolve's Film Look Creator has 5 grain types.

**Implementation**:
```python
def apply_film_grain(frame: np.ndarray, strength: float = 0.3,
                     grain_size: int = 2, frame_index: int = 0) -> np.ndarray:
    """Apply temporally varying film grain."""
    rng = np.random.default_rng(frame_index)  # different grain per frame
    noise = rng.normal(0, strength * 50, frame.shape[:2]).astype(np.float32)
    if grain_size > 1:
        noise = cv2.GaussianBlur(noise, (grain_size*2+1, grain_size*2+1), grain_size)
    # Luminance-weighted: apply more grain to midtones
    lum = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    weight = 4 * lum * (1 - lum)  # bell curve peaking at midtones
    result = frame.astype(np.float32) + noise[..., np.newaxis] * weight[..., np.newaxis]
    return np.clip(result, 0, 255).astype(np.uint8)
```

**Complexity**: ~80 LOC (upgrade existing grain parameter, temporal variation, frame_index threading)
**Dependencies**: numpy + OpenCV (already installed)

---

### #9 - Atmospheric Haze / Depth Fog Effect
**Source Tool**: DaVinci Resolve, Adobe After Effects, Corel AfterShot Pro
**Priority**: NICE-TO-HAVE

**Description**:
Add depth-based atmospheric haze to aerial footage. In real aerial photography, distant objects appear hazier due to atmospheric scattering. Simulating this enhances perceived depth and cinematic quality. Uses depth estimation or simple distance-from-horizon blur/exposure lifting.

**How it applies to drone footage**:
Aerial footage with mountains, cityscapes, or coastlines benefits enormously from atmospheric haze. Creates sense of scale and distance. Common in cinematic landscape drone work.

**Implementation**:
```python
def apply_atmospheric_haze(frame: np.ndarray, horizon_y: float = 0.4,
                            haze_strength: float = 0.2) -> np.ndarray:
    """Apply gradient haze from horizon upward (sky region)."""
    h, w = frame.shape[:2]
    horizon_px = int(horizon_y * h)
    # Gradient mask: full haze at top, zero at horizon
    gradient = np.linspace(haze_strength, 0, horizon_px)
    mask = np.zeros(h)
    mask[:horizon_px] = gradient[::-1]
    haze_color = np.array([220, 220, 200], dtype=np.float32)  # light blue-white
    result = frame.astype(np.float32)
    for c in range(3):
        result[:, :, c] += (haze_color[c] - result[:, :, c]) * mask[:, np.newaxis]
    return np.clip(result, 0, 255).astype(np.uint8)
```

**Complexity**: ~90 LOC (gradient mask, optional sky segmentation via cv2 threshold)
**Dependencies**: numpy + OpenCV (already installed)

---

### #10 - Log Footage Detection & Auto Normalization (D-Log/D-Log M to Rec.709)
**Source Tool**: DaVinci Resolve (Color Managed Workflow), Adobe Premiere Pro
**Priority**: MUST-HAVE

**Description**:
DJI drones shooting in D-Log M (Mavic 3) or D-Log produce flat, desaturated footage for maximum dynamic range. Current drone-reel applies presets directly to whatever input color space is given. Add auto-detection of log footage (low contrast, low saturation) and automatic gamma expansion before grading.

**How it applies to drone footage**:
This is the most critical missing feature for professional DJI drone users. Without D-Log normalization, all color presets will produce incorrect/flat results on log footage. DaVinci Resolve's color managed workflow handles this automatically.

**Implementation**:
```python
def detect_log_footage(frame: np.ndarray) -> bool:
    """Detect if frame appears to be log-encoded (low contrast, reduced saturation)."""
    # Log footage: low contrast ratio, mean brightness 80-160, low saturation
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    contrast = gray.std()
    return contrast < 40 and 80 < gray.mean() < 160

def apply_dlog_to_rec709(frame: np.ndarray, log_type: str = "dlog_m") -> np.ndarray:
    """Apply D-Log M to Rec.709 gamma transform."""
    # D-Log M curve: Y = c * log10(b * X + 1) + offset (reverse for decode)
    f32 = frame.astype(np.float32) / 255.0
    # DJI D-Log M decode parameters
    if log_type == "dlog_m":
        decoded = np.where(f32 >= 0.14,
                           np.power(10, (f32 - 0.584) / 0.36) / 4.6,
                           (f32 - 0.0208) / 3.5)
    return np.clip(decoded * 255, 0, 255).astype(np.uint8)
```

**Complexity**: ~150 LOC (detection heuristic, D-Log/D-Log M/S-Log decode curves, CLI `--input-colorspace` flag)
**Dependencies**: numpy (already installed)

---

### #11 - Temporal Dithering / Motion Blur Frame Blending
**Source Tool**: DaVinci Resolve, Adobe Premiere Pro
**Priority**: NICE-TO-HAVE

**Description**:
Add artificial motion blur to drone footage by blending consecutive frames. Drone cameras often use very fast shutter speeds (1/2000s+) resulting in stroboscopic, choppy motion. Blending 2-4 adjacent frames simulates a more natural 180-degree shutter look.

**How it applies to drone footage**:
High-shutter drone footage looks harsh and jittery in slow playback. Frame blending creates the cinematic "motion blur" look associated with Hollywood productions. Adobe Premiere Pro's "Frame Blending" mode does this automatically.

**Implementation**:
```python
def apply_motion_blur_blend(frames: list[np.ndarray],
                             blend_frames: int = 3) -> np.ndarray:
    """Blend consecutive frames to simulate motion blur."""
    weights = np.exp(-np.arange(blend_frames) * 1.5)
    weights = weights / weights.sum()
    result = np.zeros_like(frames[0], dtype=np.float32)
    for i, w in enumerate(weights):
        if i < len(frames):
            result += frames[i].astype(np.float32) * w
    return result.astype(np.uint8)
```

**Complexity**: ~100 LOC (frame buffer management in VideoProcessor, `--motion-blur` CLI flag)
**Dependencies**: numpy (already installed)

---

### #12 - Auto Sky Masking & Sky-Selective Color Grading
**Source Tool**: DaVinci Resolve (Magic Mask), Adobe Premiere Pro (Mask with Tracking)
**Priority**: NICE-TO-HAVE

**Description**:
Automatically detect sky region in aerial footage using color/brightness thresholding or simple segmentation, then apply different color grades to sky vs. ground independently. DaVinci Resolve's Magic Mask uses AI for this; a simpler threshold approach works well for drone footage.

**How it applies to drone footage**:
Aerial footage typically has sky in upper portion of frame. Selective sky enhancement (boosting blue saturation, adding haze) while separately enhancing foreground (boosting greens/earthy tones) is a hallmark of professional drone color work.

**Implementation**:
```python
def create_sky_mask(frame: np.ndarray) -> np.ndarray:
    """Create binary mask for sky region using HSV thresholding."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Sky: high brightness, blue-ish hue, low saturation for overcast
    sky_mask = cv2.inRange(hsv, (90, 20, 150), (140, 255, 255))
    # Morphological cleanup
    sky_mask = cv2.morphologyEx(sky_mask, cv2.MORPH_CLOSE,
                                 np.ones((15, 15), np.uint8))
    return sky_mask

def apply_sky_grade(frame: np.ndarray, sky_boost_saturation: float = 1.2):
    """Apply selective enhancement to sky region only."""
    pass
```

**Complexity**: ~130 LOC (sky detection, morphological cleanup, blended apply)
**Dependencies**: OpenCV (already installed)

---

### #13 - Transition Pack: Whip Pan, Spin, Warp Zoom
**Source Tool**: CapCut, Adobe Premiere Pro (Film Impact), LumaFusion
**Priority**: MUST-HAVE

**Description**:
Additional transition types beyond the current cut/crossfade/fade_black/zoom_in set. Whip pan (horizontal blur streak), spin (rotational blur), and warp zoom (radial zoom blur) are the most popular drone video transitions in viral content. These define the "TikTok/Instagram Reels" aesthetic.

**How it applies to drone footage**:
Whip pan transitions are natural for drone content that involves panning moves. Warp zoom transitions emphasize the speed and movement of flyover shots. These transitions are the #1 visual signature of modern viral drone reels.

**Implementation**:
```python
def whip_pan_transition(clip_a, clip_b, duration: float = 0.2,
                         direction: str = "left") -> VideoClip:
    """Motion blur streak transition between clips."""
    # Apply directional motion blur kernel to transition frames
    # cv2.filter2D with horizontal/vertical kernel
    pass

def spin_transition(clip_a, clip_b, duration: float = 0.3) -> VideoClip:
    """Rotational blur transition."""
    # cv2.warpAffine with rotation + radial blur
    pass

def warp_zoom_transition(clip_a, clip_b, duration: float = 0.25) -> VideoClip:
    """Radial zoom blur transition."""
    # cv2.remap with radial displacement map
    pass
```

**Complexity**: ~200 LOC (3 new transition types in video_processor.py + TransitionType enum)
**Dependencies**: OpenCV + numpy (already installed)

---

### #14 - Automatic Audio Beat Classification (Energy/Section Detection)
**Source Tool**: DaVinci Resolve, Premiere Pro, CapCut Smart Cut
**Priority**: NICE-TO-HAVE

**Description**:
Beyond simple beat detection, classify audio sections as intro/build/drop/outro and match clip energy to audio energy. CapCut's AI auto-edit uses energy sections. The current BeatSync does beat+downbeat detection but lacks section-level audio analysis.

**How it applies to drone footage**:
Match calm/static drone shots to intro/outro sections, and dynamic/fast shots to the build/drop sections. Creates a professional editorial rhythm that feels intentional rather than random.

**Implementation**:
```python
# Extend BeatSync with librosa section analysis
import librosa

def detect_audio_sections(audio_path: str) -> list[dict]:
    """Detect intro/build/drop/outro sections using spectral flux."""
    y, sr = librosa.load(audio_path)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    # RMS energy in segments
    # Classify sections by energy percentile
    pass
```

**Complexity**: ~100 LOC (extend BeatSync, add `energy_sections` output, use in SceneSequencer)
**Dependencies**: librosa (already installed)

---

### #15 - Graduated Neutral Density (GND) Sky Correction Filter
**Source Tool**: DaVinci Resolve, Lightroom, Final Cut Pro
**Priority**: NICE-TO-HAVE

**Description**:
A graduated filter that darkens the top of the frame (sky) while leaving the bottom (ground) unaffected. Simulates a physical GND filter used in landscape photography. Essential for exposure-balancing aerial footage with bright skies.

**How it applies to drone footage**:
Drone cameras often have exposure mismatches between sky (overexposed) and ground (underexposed). A GND correction filter compensates without masking artifacts.

**Implementation**:
```python
def apply_gnd_filter(frame: np.ndarray, sky_fraction: float = 0.4,
                     exposure_stops: float = -1.5) -> np.ndarray:
    """Apply graduated ND filter to sky region."""
    h, w = frame.shape[:2]
    sky_h = int(sky_fraction * h)
    factor = 2 ** exposure_stops  # -1.5 stops = 0.354x
    gradient = np.linspace(factor, 1.0, sky_h)
    gradient = np.concatenate([gradient, np.ones(h - sky_h)])
    result = frame.astype(np.float32) * gradient[:, np.newaxis, np.newaxis]
    return np.clip(result, 0, 255).astype(np.uint8)
```

**Complexity**: ~70 LOC (gradient mask, exposure factor, CLI `--gnd-sky` parameter)
**Dependencies**: numpy (already installed)

---

### #16 - Lens Flare / Light Leak Overlay
**Source Tool**: Adobe Premiere, CapCut, Final Cut Pro plugins
**Priority**: NICE-TO-HAVE

**Description**:
Apply cinematic lens flare or light leak overlays sourced from numpy-generated patterns or pre-rendered PNG assets. Lens flares add warmth and realism to drone shots looking toward sun. Light leaks (randomized warm bokeh on frame edges) are extremely popular in vintage/cinematic drone aesthetics.

**How it applies to drone footage**:
Drone footage into the sun naturally creates lens flares, but they are inconsistent. Programmatic lens flares can be added to shots where the sun direction is detected. Light leaks can be used as transition decorations.

**Implementation**:
```python
def generate_lens_flare(frame: np.ndarray, sun_x: float = 0.5,
                         sun_y: float = 0.2, strength: float = 0.4) -> np.ndarray:
    """Generate and composite a procedural lens flare."""
    h, w = frame.shape[:2]
    # Generate bright anamorphic streak from sun position
    # Add secondary circular bokeh elements along line from sun through center
    # Blend with screen blend mode
    pass

def apply_light_leak(frame: np.ndarray, leak_type: str = "warm_edge",
                      strength: float = 0.3) -> np.ndarray:
    """Apply pre-generated warm light leak overlay."""
    # Generate radial gradient from corner with warm orange/red tones
    pass
```

**Complexity**: ~150 LOC (procedural flare generation or alpha-blended overlay assets)
**Dependencies**: numpy (already installed)

---

### #17 - Aspect Ratio Padding / Safe Zone Letterboxing
**Source Tool**: DaVinci Resolve, Premiere Pro, Final Cut Pro
**Priority**: NICE-TO-HAVE

**Description**:
Add cinematic letterboxing (2.35:1 or 2.39:1 anamorphic black bars) to any output format. Many viral drone videos use widescreen letterboxing even on vertical/square crops to signal "cinematic" quality. Also includes platform-specific safe zone compliance checking.

**How it applies to drone footage**:
Landscape drone footage cropped to vertical with letterboxing maintains the widescreen cinematic feel while being vertical-format compatible.

**Implementation**:
```python
def apply_letterbox(clip, aspect_ratio: float = 2.35) -> VideoClip:
    """Add black bars for widescreen letterbox look."""
    # Calculate bar height, composite black bars on top/bottom
    # Use MoviePy CompositeVideoClip
    pass
```

**Complexity**: ~60 LOC (MoviePy CompositeVideoClip with black bar clips, `--letterbox` CLI flag)
**Dependencies**: MoviePy (already installed)

---

### #18 - Noise Reduction (Temporal / Spatial Denoising)
**Source Tool**: DaVinci Resolve (Motion Estimation Noise Reduction), Adobe Premiere
**Priority**: NICE-TO-HAVE

**Description**:
Reduce luminance and chroma noise from high-ISO or low-light drone footage using OpenCV bilateral filter or Non-Local Means denoising. DaVinci Resolve's temporal noise reducer is considered industry-leading; a simpler spatial approach is feasible in Python.

**How it applies to drone footage**:
Sunset/golden hour drone footage often has noticeable noise due to challenging auto-exposure conditions. Noise reduction before color grading dramatically improves final output quality.

**Implementation**:
```python
def apply_noise_reduction(frame: np.ndarray, strength: float = 0.5,
                           mode: str = "bilateral") -> np.ndarray:
    """Apply spatial noise reduction."""
    if mode == "bilateral":
        # Bilateral filter: edge-preserving smoothing
        d = int(5 + strength * 10)
        sigma = strength * 75
        return cv2.bilateralFilter(frame, d, sigma, sigma)
    elif mode == "nlm":
        # Non-local means (slower, better quality)
        h = strength * 10
        return cv2.fastNlMeansDenoisingColored(frame, None, h, h, 7, 21)
```

**Complexity**: ~80 LOC (mode selection, strength scaling, `--denoise` CLI flag)
**Dependencies**: OpenCV (already installed)

---

### #19 - Auto White Balance Correction
**Source Tool**: DaVinci Resolve (Auto Balance), CapCut AI Color, Adobe Premiere (Lumetri Auto)
**Priority**: NICE-TO-HAVE

**Description**:
Automatically neutralize color cast by detecting gray/neutral regions or using gray world assumption. Drone cameras auto-white-balance continuously, causing flickering between clips. Consistent WB correction across all clips improves reel cohesion.

**How it applies to drone footage**:
Each drone clip may have been captured with different auto-WB settings. Normalizing white balance across all clips before applying creative color presets ensures consistency.

**Implementation**:
```python
def auto_white_balance(frame: np.ndarray, method: str = "gray_world") -> np.ndarray:
    """Apply automatic white balance correction."""
    if method == "gray_world":
        # Scale each channel so its mean equals overall mean
        mean_b, mean_g, mean_r = [frame[:,:,i].mean() for i in range(3)]
        overall_mean = (mean_b + mean_g + mean_r) / 3
        scale = [overall_mean / m if m > 0 else 1.0
                 for m in [mean_b, mean_g, mean_r]]
        result = frame.astype(np.float32)
        for i, s in enumerate(scale):
            result[:,:,i] *= s
        return np.clip(result, 0, 255).astype(np.uint8)
```

**Complexity**: ~80 LOC (gray world + retinex methods, per-clip normalization, `--auto-wb` CLI flag)
**Dependencies**: numpy + OpenCV (already installed)

---

### #20 - Export Telemetry Data Sidecar (GPS/Speed/Altitude Metadata)
**Source Tool**: Telemetry Overlay, DJI Telemetry Overlay, Adobe After Effects
**Priority**: EXPERIMENTAL

**Description**:
Extract and export GPS/speed/altitude metadata from DJI video files alongside the output reel. The extracted data could be used to display speed/altitude overlays (heads-up display style) on the reel. DJI video files embed telemetry in subtitle track (SRT) format.

**How it applies to drone footage**:
Speed, altitude, and GPS path overlays are popular on YouTube/Patreon drone content. Data-overlay videos get higher engagement from aviation/tech audiences.

**Implementation**:
```python
import subprocess

def extract_dji_telemetry(video_path: str) -> dict:
    """Extract SRT telemetry from DJI video using ffprobe."""
    result = subprocess.run([
        'ffprobe', '-v', 'quiet', '-print_format', 'json',
        '-show_streams', video_path
    ], capture_output=True, text=True)
    # Parse subtitle stream for GPS data
    pass

def overlay_telemetry_hud(clip, telemetry: dict,
                            elements: list = ["speed", "altitude"]):
    """Overlay HUD elements using TextOverlay module."""
    pass
```

**Complexity**: ~200 LOC (ffprobe SRT parsing, HUD positioning, `--telemetry-hud` CLI flag)
**Dependencies**: ffprobe (system dependency), existing TextOverlay module

---

## Summary Table

| Rank | Feature | Source Tool | Priority | Complexity (LOC) | Dependencies |
|------|---------|-------------|----------|------------------|--------------|
| 1 | 3D LUT (.cube) Loading | DaVinci Resolve, Premiere | MUST-HAVE | ~150 | colour-science or pycubelut |
| 2 | Vignette Effect | All Major Tools | MUST-HAVE | ~60 | numpy (existing) |
| 3 | Chromatic Aberration | Premiere, Resolve, CapCut | MUST-HAVE | ~80 | OpenCV (existing) |
| 4 | Halation / Bloom | DaVinci Resolve, FilmConvert | MUST-HAVE | ~70 | OpenCV (existing) |
| 5 | Lens Distortion Correction | Premiere, Resolve | MUST-HAVE | ~100 | OpenCV (existing) |
| 6 | Auto Color Match / Scene Consistency | Premiere, Resolve | MUST-HAVE | ~120 | scikit-image |
| 7 | Audio Ducking | Resolve, Premiere, CapCut | MUST-HAVE | ~80 | MoviePy (existing) |
| 8 | Film Grain (Upgraded) | Resolve, FilmConvert | MUST-HAVE | ~80 | numpy+OpenCV (existing) |
| 9 | Atmospheric Haze / Depth Fog | Resolve, After Effects | NICE-TO-HAVE | ~90 | numpy+OpenCV (existing) |
| 10 | D-Log Auto Normalization | DaVinci Resolve, Premiere | MUST-HAVE | ~150 | numpy (existing) |
| 11 | Motion Blur Frame Blending | Premiere, Resolve | NICE-TO-HAVE | ~100 | numpy (existing) |
| 12 | Sky Masking & Selective Grade | Resolve Magic Mask | NICE-TO-HAVE | ~130 | OpenCV (existing) |
| 13 | Whip Pan / Spin / Warp Zoom Transitions | CapCut, Premiere, LumaFusion | MUST-HAVE | ~200 | OpenCV (existing) |
| 14 | Audio Section Detection | CapCut Smart Cut | NICE-TO-HAVE | ~100 | librosa (existing) |
| 15 | GND Sky Correction Filter | Resolve, Lightroom, FCP | NICE-TO-HAVE | ~70 | numpy (existing) |
| 16 | Lens Flare / Light Leak | Premiere, CapCut, FCP | NICE-TO-HAVE | ~150 | numpy (existing) |
| 17 | Letterbox / Safe Zone | Resolve, Premiere, FCP | NICE-TO-HAVE | ~60 | MoviePy (existing) |
| 18 | Noise Reduction | Resolve, Premiere | NICE-TO-HAVE | ~80 | OpenCV (existing) |
| 19 | Auto White Balance | Resolve, CapCut, Premiere | NICE-TO-HAVE | ~80 | numpy+OpenCV (existing) |
| 20 | Telemetry HUD Overlay | Telemetry Overlay, DJI tools | EXPERIMENTAL | ~200 | ffprobe |

---

## Implementation Sequence Recommendation

**Phase A (Highest viral impact, all using existing dependencies):**
1. Vignette (#2) - 60 LOC, numpy only
2. Halation/Bloom (#4) - 70 LOC, OpenCV
3. Chromatic Aberration (#3) - 80 LOC, OpenCV
4. Audio Ducking (#7) - 80 LOC, MoviePy
5. Whip Pan/Spin transitions (#13) - 200 LOC, OpenCV

**Phase B (Requires minor new dependency, high professional quality):**
6. 3D LUT loading (#1) - 150 LOC, colour-science
7. D-Log Normalization (#10) - 150 LOC, numpy
8. Auto Color Match (#6) - 120 LOC, scikit-image
9. Film Grain upgrade (#8) - 80 LOC

**Phase C (Advanced/selective features):**
10. Lens Distortion Correction (#5)
11. Sky Masking (#12)
12. Atmospheric Haze (#9)
13. GND Filter (#15)

---

## Key Architectural Notes

### Adding to ColorGrader
Features #2 (vignette), #3 (CA), #4 (halation), #8 (grain upgrade), #9 (haze), #12 (sky masking), #15 (GND), #18 (denoise), #19 (AWB) all belong as methods on `ColorGrader` class or as new `ColorEffect` enum entries in `/Users/matthewdeane/Documents/Data Science/python/_projects/_p-ai-drone-video/src/drone_reel/core/color_grader.py`.

### Adding to VideoProcessor
Features #7 (audio duck), #11 (motion blur), #13 (transitions), #17 (letterbox) belong in `/Users/matthewdeane/Documents/Data Science/python/_projects/_p-ai-drone-video/src/drone_reel/core/video_processor.py` and/or the TransitionType enum.

### New Module Candidates
- Feature #1 (3D LUT) → new `lut_manager.py` module
- Feature #10 (D-Log) → new `colorspace.py` module
- Feature #20 (Telemetry) → new `telemetry.py` module

### CLI Integration
All MUST-HAVE features should get corresponding `--flag` arguments in `cli.py`. Suggested flags:
- `--vignette FLOAT` (0.0-1.0 strength)
- `--halation FLOAT` (0.0-1.0 strength)
- `--chromatic-aberration FLOAT` (0.0-1.0 or pixel offset)
- `--duck-outro` (bool flag)
- `--lut PATH` (.cube file path)
- `--input-colorspace [rec709|dlog|dlog_m|slog3]`
- `--auto-wb` (bool flag)
- `--denoise` (bool flag)
- `--lens-model [mavic3|mini4|air3|fpv]`

---

## Sources Consulted

1. [Oscar Liang - Color Grade FPV Drone Videos in DaVinci Resolve](https://oscarliang.com/color-grade-fpv-videos/)
2. [DaVinci Resolve 20 New Features Guide](https://documents.blackmagicdesign.com/SupportNotes/DaVinci_Resolve_20_New_Features_Guide.pdf)
3. [Adobe Premiere Pro - Automatically Match Color](https://helpx.adobe.com/premiere-pro/how-to/automatically-match-color.html)
4. [lensfunpy - Lens Distortion Correction Python](https://pypi.org/project/lensfunpy/)
5. [pycubelut - Apply Adobe Cube LUTs](https://pypi.org/project/pycubelut/)
6. [pylut - Create and Modify 3D LUTs in Python](https://github.com/gregcotten/pylut)
7. [colour-science LUT3D](https://colour.readthedocs.io/en/develop/generated/colour.LUT3D.html)
8. [Final Cut Pro Smart Conform](https://support.apple.com/guide/final-cut-pro/adjust-framing-with-smart-conform-ver26664d93f/mac)
9. [Filmgrainer - Realistic Film Grain](https://github.com/larspontoppidan/filmgrainer)
10. [Dehancer Halation Simulation](https://blog.dehancer.com/articles/halation/)
11. [OpenCV Motion Blur](https://www.geeksforgeeks.org/python/opencv-motion-blur-in-python/)
12. [Telemetry Overlay DJI GPS](https://goprotelemetryextractor.com/tools-for-dji)
13. [CapCut Drone Video AI Features](https://www.capcut.com/explore/drone-video-edit)
14. [scikit-image histogram matching](https://pyimagesearch.com/2021/02/08/histogram-matching-with-opencv-scikit-image-and-python/)
15. [DJI D-Log M Color Grading in Resolve](https://filmmakingelements.com/color-grade-dji-d-log-in-davinci-resolve/)
16. [color-matcher Python library](https://github.com/hahnec/color-matcher)
17. [autoducking Python library](https://github.com/atulpatildbz/autoducking)
18. [LumaFusion drone editing features](https://www.premiumbeat.com/blog/tips-for-using-lumafusion/)
19. [Final Cut Pro AI Reframing 2025](https://www.bascombproductions.com/blog/2025/6/8/how-to-auto-crop-a-clip-in-final-cut-pro-for-ipad-ai-reframing-made-easy)
20. [Warp Stabilizer FPV Footage Premiere](https://oscarliang.com/warp-stabilizer-lens-distortion-removal-fpv-footage/)
