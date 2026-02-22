# Advanced Transition Effects Research for Drone Video Editing

**Date:** 2026-02-21
**Scope:** Modern transition effects beyond basic crossfades for the drone-reel project
**Stack Context:** Python 3.10+, MoviePy 2.x, OpenCV, NumPy (current `video_processor.py` implementation)

---

## Current Implementation Status

The project already implements these transitions in `video_processor.py`:
- `CUT`, `CROSSFADE`, `FADE_BLACK`, `FADE_WHITE`
- `ZOOM_IN`, `ZOOM_OUT`
- `SLIDE_LEFT`, `SLIDE_RIGHT`
- `WIPE_LEFT`, `WIPE_RIGHT` (defined in enum but not implemented)
- `select_motion_matched_transition()`: motion direction-based automatic selection

---

## Category 1: Motion-Matched Transitions

### 1.1 Whip Pan Match Cut
**Visual:** Camera rapidly pans right at end of clip A; clip B starts with rightward pan already in motion. No blur overlay needed — pure cut with matching motion vectors creates perceptual continuity.

**Implementation approach:** MoviePy frame transform. At cut point, confirm last N frames of clip A have optical flow direction (dx, dy) where |dx| >> |dy|. Then confirm first N frames of clip B have similar flow direction. Apply hard CUT rather than crossfade.

```python
# Detection pseudo-code
flow = cv2.calcOpticalFlowFarneback(prev_gray, curr_gray, None,
    pyr_scale=0.5, levels=3, winsize=15, iterations=3,
    poly_n=5, poly_sigma=1.2, flags=0)
mean_dx = np.mean(flow[..., 0])
mean_dy = np.mean(flow[..., 1])
# Whip pan if |mean_dx| > 8.0 px/frame and |mean_dx| / (|mean_dy| + 1e-5) > 3.0
```

**Motion blur smear overlay (optional enhancement):**
```python
def whip_blur_frame(frame, dx_magnitude, blur_strength=0.6):
    kernel_size = int(min(dx_magnitude * blur_strength, 61))
    if kernel_size % 2 == 0: kernel_size += 1
    return cv2.filter2D(frame, -1,
        np.ones((1, kernel_size)) / kernel_size)  # horizontal only
```

- **Feasibility:** 5/5 — uses existing optical flow already in `scene_analyzer.py`
- **Lines of code:** ~40 lines (detection) + ~20 lines (blur overlay)
- **Best use case:** PAN_LEFT or PAN_RIGHT motion types; consecutive same-direction pans
- **Priority:** MUST-HAVE — already partially implemented via `select_motion_matched_transition()`
- **Enhancement needed:** Add blur smear effect; widen threshold tuning for social media pace

---

### 1.2 Orbital Continuation Cut
**Visual:** Two clips both orbiting same subject clockwise. Cut at matching position angle. Creates illusion of continuous orbit across different altitudes/distances.

**Implementation approach:** Detect ORBIT_CW or ORBIT_CCW motion type in both scenes. Compute rotation angle of optical flow field (circular vs linear). If both clips classify as same orbit direction and flow magnitudes are within 30%, use hard CUT.

**Motion analysis needed:**
```python
# Compute circular flow score using curl of flow field
flow_u = flow[..., 0]  # x-component
flow_v = flow[..., 1]  # y-component
# Numerical curl approximation
curl = np.gradient(flow_v, axis=1) - np.gradient(flow_u, axis=0)
orbit_score = np.mean(np.abs(curl))  # high = rotational motion
```

- **Feasibility:** 4/5 — requires curl computation but no new dependencies
- **Lines of code:** ~60 lines
- **Best use case:** ORBIT_CW / ORBIT_CCW scenes from same subject
- **Priority:** MUST-HAVE for drone content — highly viral technique (TikTok @TheDroneCreative orbit+speedramp)

---

### 1.3 Altitude-Match Zoom Cut
**Visual:** Clip A ascending shot (camera moving upward, ground receding). Clip B descending shot (ground approaching). Cut with zoom scale matched so ground texture scale is continuous.

**Implementation approach:** Estimate scale change between last frame of clip A and first frame of clip B using feature matching. Apply inverse zoom pre-warp to normalize.

```python
# ORB feature matching for scale estimation
orb = cv2.ORB_create(500)
kp1, des1 = orb.detectAndCompute(last_frame_gray, None)
kp2, des2 = orb.detectAndCompute(first_frame_gray, None)
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(des1, des2)
# Estimate homography -> extract scale component
H, _ = cv2.findHomography(pts1, pts2, cv2.RANSAC, 5.0)
scale = np.sqrt(H[0,0]*H[1,1] - H[0,1]*H[1,0])
```

- **Feasibility:** 3/5 — needs feature matching computation at cut points
- **Lines of code:** ~80 lines
- **Best use case:** TILT_UP into TILT_DOWN; FLYOVER transitions
- **Priority:** NICE-TO-HAVE — computationally expensive, use for premium mode only

---

## Category 2: Speed-Ramped Transitions

### 2.1 Whoosh Cut (Speed Ramp + Hard Cut)
**Visual:** Last 0.5s of clip A ramps from 1.0x to 2.5x (fast exit). Cut. First 0.5s of clip B ramps from 2.5x back to 1.0x (slow settle). Creates kinetic "whoosh" energy at beat drops.

**Timing curve (cubic ease-in/ease-out):**
```python
def cubic_ease_in(t):
    """t in [0,1] -> speed multiplier for ramp-up"""
    return 1.0 + (2.5 - 1.0) * (t ** 3)  # 1.0x -> 2.5x

def cubic_ease_out(t):
    """t in [0,1] -> speed multiplier for ramp-down"""
    return 2.5 - (2.5 - 1.0) * (t ** 3)  # 2.5x -> 1.0x
```

**Integration with existing SpeedRamper:**
The project already has `SpeedRamper` in `speed_ramper.py`. This transition is a pre-built ramp pattern that applies ramp points at clip boundaries. Call `SpeedRamper.apply_multiple_ramps()` with exit ramp on clip A tail and entry ramp on clip B head.

- **Feasibility:** 5/5 — `SpeedRamper` already implemented
- **Lines of code:** ~15 lines (ramp config factory function)
- **Best use case:** Beat drops in music; PAN_RIGHT to PAN_LEFT direction changes; FPV scenes
- **Priority:** MUST-HAVE — already wired via `--speed-ramp` flag; needs cut-point variant

---

### 2.2 Slow-Mo Peak Freeze
**Visual:** Action peak (e.g., drone at maximum altitude) held at 0.1x speed for 0.3s, then resumes. Used as emphasis rather than transition, but creates rhythmic editing feel between clips.

**Timing curve:**
```
1.0x ----\
          \  0.1x (hold 0.3s)
           \_______________/----1.0x
```

- **Feasibility:** 5/5 — SpeedRamper supports this
- **Lines of code:** ~10 lines
- **Best use case:** MAXIMUM hook_tier clips; REVEAL motion type scenes
- **Priority:** NICE-TO-HAVE

---

## Category 3: Geometric Transitions

### 3.1 Iris / Circle Wipe (In and Out)
**Visual:** Clip B reveals from expanding circle centered on frame. Classic cinematic effect; "iris out" closes to black from clip A.

**Implementation approach:** NumPy boolean mask expanding over time.
```python
def iris_wipe_frame(frame_a, frame_b, t, duration, w, h):
    """t=0 shows frame_a; t=duration shows frame_b"""
    cx, cy = w // 2, h // 2
    max_radius = np.sqrt(cx**2 + cy**2) * 1.05  # cover corners
    progress = t / duration  # 0 -> 1
    radius = int(max_radius * progress)

    # Create circular mask
    Y, X = np.ogrid[:h, :w]
    dist = np.sqrt((X - cx)**2 + (Y - cy)**2)
    mask = (dist <= radius).astype(np.float32)

    # Feather edge (4px softness)
    mask = np.clip((radius - dist + 4) / 8.0, 0, 1)

    mask_3d = mask[:, :, np.newaxis]
    return (frame_b * mask_3d + frame_a * (1 - mask_3d)).astype(np.uint8)
```

**MoviePy integration:**
```python
def _transition_iris_in(self, clip1, clip2, duration):
    w, h = clip1.w, clip1.h
    composite_duration = duration

    def make_frame(t):
        fa = clip1.get_frame(clip1.duration - duration + t)
        fb = clip2.get_frame(t)
        return iris_wipe_frame(fa, fb, t, duration, w, h)

    from moviepy import VideoClip
    transition_clip = VideoClip(make_frame, duration=composite_duration)
    return concatenate_videoclips([
        clip1.subclipped(0, clip1.duration - duration),
        transition_clip,
        clip2.subclipped(duration)
    ])
```

- **Feasibility:** 5/5 — pure NumPy, no new dependencies
- **Lines of code:** ~40 lines (iris_in + iris_out)
- **Best use case:** REVEAL motion type entering; MAXIMUM hook_tier openers
- **Priority:** MUST-HAVE — high visual impact, commonly used in cinematic drone edits

---

### 3.2 Diagonal Wipe
**Visual:** Clip B reveals from a diagonal line sweeping across the frame (45° or 135° angle).

**Implementation approach:**
```python
def diagonal_wipe_frame(frame_a, frame_b, t, duration, w, h, angle_deg=45):
    progress = t / duration  # 0 -> 1
    # Distance threshold along diagonal axis
    angle_rad = np.radians(angle_deg)
    nx, ny = np.cos(angle_rad), np.sin(angle_rad)  # Normal to wipe direction

    Y, X = np.mgrid[:h, :w]
    # Project pixel coords onto wipe axis
    proj = X * nx + Y * ny
    max_proj = w * nx + h * ny
    threshold = progress * max_proj

    # Feathered mask
    mask = np.clip((threshold - proj + 8) / 16.0, 0, 1).astype(np.float32)
    mask_3d = mask[:, :, np.newaxis]
    return (frame_b * mask_3d + frame_a * (1 - mask_3d)).astype(np.uint8)
```

- **Feasibility:** 5/5 — pure NumPy
- **Lines of code:** ~30 lines
- **Best use case:** Scene direction changes; PAN transitions
- **Priority:** NICE-TO-HAVE

---

### 3.3 Diamond Wipe
**Visual:** Clip B reveals from expanding diamond (rotated square) from screen center.

**Implementation approach:** Same as iris but using L1 (Manhattan) distance instead of L2:
```python
dist_l1 = np.abs(X - cx) + np.abs(Y - cy)  # Diamond shape
```

- **Feasibility:** 5/5 — pure NumPy
- **Lines of code:** ~25 lines (shares iris infrastructure)
- **Best use case:** High-energy music beats; abstract/geometric drone footage
- **Priority:** NICE-TO-HAVE

---

### 3.4 Parallax Slide (Differential Speed Slide)
**Visual:** Two clips slide horizontally but at different speeds, creating depth illusion. Clip A (background layer) moves at 0.5x rate; clip B (foreground layer) moves at 1.0x rate.

**Implementation approach:**
```python
def _transition_parallax_slide(self, clip1, clip2, duration, direction='left'):
    w, h = clip1.w, clip1.h
    bg_speed = 0.5  # Background moves slower
    fg_speed = 1.0  # Foreground moves at normal rate

    def make_frame(t):
        progress = t / duration

        # Background: clip1 slides out slowly
        bg_offset = int(w * progress * bg_speed)
        fb = clip1.get_frame(clip1.duration - duration + t)
        # Crop/position background
        bg_x = min(bg_offset, w - 1)

        # Foreground: clip2 slides in at full speed
        fg_offset = int(w * (1 - progress) * fg_speed)
        ff = clip2.get_frame(t)

        # Composite: paste ff onto fb offset
        result = np.zeros_like(fb)
        if direction == 'left':
            # bg slides left, fg comes from right
            if bg_x < w:
                result[:, :w - bg_x] = fb[:, bg_x:]
            fg_start = w - fg_offset if fg_offset <= w else 0
            paste_w = min(fg_offset, w)
            result[:, fg_start:fg_start + paste_w] = ff[:, :paste_w]
        return result.astype(np.uint8)

    from moviepy import VideoClip
    trans = VideoClip(make_frame, duration=duration)
    return concatenate_videoclips([
        clip1.subclipped(0, clip1.duration - duration),
        trans,
        clip2.subclipped(duration)
    ])
```

- **Feasibility:** 4/5 — requires careful boundary handling; pure NumPy
- **Lines of code:** ~60 lines
- **Best use case:** PAN_LEFT exit into PAN_RIGHT entry; landscape reveals
- **Priority:** NICE-TO-HAVE — adds cinematic depth, common in travel content

---

### 3.5 Split Screen Reveal
**Visual:** Frame splits horizontally (top half slides up, bottom half slides down) to reveal clip B beneath.

**Implementation approach:**
```python
def split_reveal_frame(frame_a, frame_b, t, duration, w, h):
    progress = t / duration
    offset = int(h // 2 * progress)

    result = frame_b.copy()
    # Top half of frame_a slides upward
    top_src_end = h // 2
    top_dst_end = max(0, h // 2 - offset)
    if top_dst_end > 0:
        result[:top_dst_end] = frame_a[offset:offset + top_dst_end]
    # Bottom half slides downward
    bot_src_start = h // 2
    bot_dst_start = min(h, h // 2 + offset)
    if bot_dst_start < h:
        copy_rows = h - bot_dst_start
        result[bot_dst_start:] = frame_a[bot_src_start:bot_src_start + copy_rows]
    return result.astype(np.uint8)
```

- **Feasibility:** 5/5 — pure NumPy
- **Lines of code:** ~35 lines
- **Best use case:** TILT transitions; altitude changes; before/after comparisons
- **Priority:** NICE-TO-HAVE

---

## Category 4: Glitch / Digital Effects

### 4.1 RGB Channel Split (Chromatic Aberration Transition)
**Visual:** At cut point, R/G/B channels separate horizontally for 3-5 frames, then snap back to normal. Creates jarring "digital glitch" feel popular in social media edits.

**Implementation approach:** Pure NumPy array manipulation.
```python
def rgb_split_frame(frame, shift_px, direction='horizontal'):
    """
    Args:
        frame: HxWx3 uint8 array
        shift_px: Pixel offset amount (0 = no effect, 8 = strong)
        direction: 'horizontal' or 'vertical'
    """
    result = frame.copy()
    if direction == 'horizontal':
        # Red channel shifts right
        result[:, shift_px:, 0] = frame[:, :-shift_px, 0]
        # Blue channel shifts left
        result[:, :-shift_px, 2] = frame[:, shift_px:, 2]
        # Green stays centered
    else:
        result[shift_px:, :, 0] = frame[:-shift_px, :, 0]
        result[:-shift_px, :, 2] = frame[shift_px:, :, 2]
    return result

def _transition_glitch_cut(self, clip1, clip2, duration=0.15):
    """3-frame RGB split glitch at cut point."""
    fps = clip1.fps or 30
    glitch_frames = max(3, int(duration * fps))
    w, h = clip1.w, clip1.h

    def make_glitch(t):
        # Map t to [0,1] triangle wave for glitch pulse
        progress = t / duration
        shift = int(12 * (1 - abs(2 * progress - 1)))  # 0 -> 12 -> 0

        # Blend from clip1 to clip2 during glitch
        if progress < 0.5:
            frame = clip1.get_frame(clip1.duration - duration + t)
        else:
            frame = clip2.get_frame(t - duration / 2)

        return rgb_split_frame(frame, max(0, shift))

    from moviepy import VideoClip
    glitch_clip = VideoClip(make_glitch, duration=duration)
    return concatenate_videoclips([
        clip1.subclipped(0, clip1.duration - duration / 2),
        glitch_clip,
        clip2.subclipped(duration / 2)
    ])
```

- **Feasibility:** 5/5 — pure NumPy, trivial implementation
- **Lines of code:** ~40 lines
- **Best use case:** Beat drops; FPV footage; high-energy scene changes
- **Priority:** MUST-HAVE for viral style — extremely common in 2025 social media edits

---

### 4.2 Scan Line Flash
**Visual:** Horizontal white/black scan lines sweep across frame during cut, lasting 3-6 frames. Mimics CRT or digital artifact.

**Implementation approach:**
```python
def scanline_flash_frame(frame, t, duration, line_width=3, color=(255, 255, 255)):
    result = frame.copy().astype(np.float32)
    h, w = frame.shape[:2]
    progress = t / duration  # 0->1

    # Sweep position
    sweep_y = int(h * progress)
    y_start = max(0, sweep_y - line_width)
    y_end = min(h, sweep_y + line_width)

    intensity = np.sin(np.pi * progress)  # Fade in/out
    result[y_start:y_end] = (
        result[y_start:y_end] * (1 - intensity) +
        np.array(color, dtype=np.float32) * intensity
    )
    return np.clip(result, 0, 255).astype(np.uint8)
```

- **Feasibility:** 5/5 — pure NumPy
- **Lines of code:** ~25 lines
- **Best use case:** STATIC to high-motion scene changes; sci-fi/tech aesthetic
- **Priority:** NICE-TO-HAVE — niche aesthetic

---

### 4.3 Pixel Sort Transition
**Visual:** At transition, pixels sort themselves by brightness into columns/rows, then re-sort into new frame. Glitch art aesthetic.

**Implementation approach:** Apply pixel sorting to transition blend. Sort columns of frame by luminance during 0.1-0.2s window.
```python
def pixel_sort_frame(frame, sort_strength=1.0):
    """Sort pixels within each column by brightness (partial sort for subtlety)."""
    result = frame.copy()
    h, w = frame.shape[:2]
    luminance = 0.299 * frame[:,:,0] + 0.587 * frame[:,:,1] + 0.114 * frame[:,:,2]
    sort_threshold = 128  # Only sort pixels above threshold

    for x in range(0, w, 2):  # Skip columns for performance
        col_lum = luminance[:, x]
        mask = col_lum > sort_threshold
        if np.sum(mask) > 2:
            sorted_indices = np.argsort(col_lum[mask])
            result[mask, x] = frame[mask, x][sorted_indices]

    return result
```

**Performance note:** Per-column iteration in Python is slow. For production use, vectorize with `np.argsort` on full array or apply only to a small horizontal band at the cut point.

- **Feasibility:** 3/5 — pure NumPy but slow without vectorization; needs optimization
- **Lines of code:** ~50 lines (naive) / ~80 lines (vectorized)
- **Best use case:** Experimental/artistic content; glitch aesthetic
- **Priority:** EXPERIMENTAL — high visual impact but computationally expensive

---

### 4.4 Datamosh Simulation
**Visual:** Simulates video codec artifact — blocks of pixels from clip A remain as ghost overlay for 5-10 frames into clip B. True datamoshing requires FFmpeg bitstream manipulation, but visual simulation is achievable.

**Implementation approach (simulation):**
```python
def datamosh_blend_frame(frame_a, frame_b, t, duration, block_size=16):
    """
    Block-based ghost overlay: tiles from frame_a persist into frame_b.
    NOT true datamoshing (no codec manipulation) but visually similar.
    """
    h, w = frame_b.shape[:2]
    decay = 1.0 - (t / duration)  # Fade from 1.0 to 0.0
    result = frame_b.copy().astype(np.float32)

    # Random block selection (seed from frame hash for consistency)
    rng = np.random.RandomState(42)
    for y in range(0, h, block_size):
        for x in range(0, w, block_size):
            if rng.random() < 0.3 * decay:  # 30% of blocks persist
                y2 = min(y + block_size, h)
                x2 = min(x + block_size, w)
                result[y:y2, x:x2] = frame_a[y:y2, x:x2].astype(np.float32)

    return result.astype(np.uint8)
```

**True datamosh** requires removing I-frames via FFmpeg bitstream access — requires `ffmpeg-python` and raw H.264 manipulation. Not recommended for production pipeline due to quality unpredictability.

- **Feasibility:** 4/5 (simulation) / 1/5 (true datamosh)
- **Lines of code:** ~40 lines (simulation)
- **Best use case:** Artistic/experimental segments; music video style
- **Priority:** EXPERIMENTAL

---

## Category 5: Light-Based Transitions

### 5.1 Whiteout Flash
**Visual:** Frame rapidly brightens to pure white over 2-4 frames, then new clip fades in from white. Simulates overexposure burst.

**Implementation approach:** Already partially implemented as `FADE_WHITE`. Enhanced version adds non-linear curve:
```python
def whiteout_flash_frame(frame, t, peak_time, duration, w, h):
    """Non-linear flash: fast rise to white, slow fall back."""
    if t <= peak_time:
        # Fast rise: exponential
        intensity = (t / peak_time) ** 0.4  # Concave up = fast rise
    else:
        # Slow fall: linear
        intensity = 1.0 - (t - peak_time) / (duration - peak_time)

    white = np.ones_like(frame, dtype=np.float32) * 255
    result = frame.astype(np.float32) * (1 - intensity) + white * intensity
    return np.clip(result, 0, 255).astype(np.uint8)
```

- **Feasibility:** 5/5 — pure NumPy; extends existing FADE_WHITE
- **Lines of code:** ~25 lines
- **Best use case:** Golden hour to direct sun; REVEAL scenes entering bright sky
- **Priority:** MUST-HAVE — highly effective for drone golden hour footage

---

### 5.2 Light Leak Gradient
**Visual:** Colored gradient (amber/orange or cyan) sweeps diagonally across frame during transition, simulating film light leak effect.

**Procedural generation approach:**
```python
def light_leak_overlay(h, w, t, duration,
                        color=(255, 200, 120),  # Amber
                        direction='diagonal'):
    """Generate a light leak gradient mask (no asset files needed)."""
    intensity = np.sin(np.pi * t / duration)  # Bell curve fade in/out

    Y, X = np.mgrid[:h, :w]
    # Diagonal gradient along 45 degrees
    grad_raw = (X + Y).astype(np.float32)
    # Normalize and shift sweep position
    sweep_center = (w + h) * (t / duration)
    spread = (w + h) * 0.3
    gaussian = np.exp(-((grad_raw - sweep_center) ** 2) / (2 * spread ** 2))

    leak = (gaussian * intensity * 0.6)[:, :, np.newaxis]  # 60% max opacity
    leak_color = np.array(color, dtype=np.float32)
    return leak * leak_color  # HxWx3 float additive layer

def apply_light_leak(frame, leak_layer):
    result = frame.astype(np.float32) + leak_layer
    return np.clip(result, 0, 255).astype(np.uint8)
```

- **Feasibility:** 5/5 — procedurally generated, no asset files required
- **Lines of code:** ~35 lines
- **Best use case:** Golden hour footage; TILT_UP sky reveals; warm cinematic presets
- **Priority:** MUST-HAVE for cinematic drone style

---

### 5.3 Anamorphic Streak Flash
**Visual:** Horizontal blue/cyan streak (lens flare simulation) passes across frame at cut point. Mimics anamorphic lens artifact. Typically 2-4 frames.

**Procedural generation approach:**
```python
def anamorphic_streak_frame(frame, t, duration,
                              streak_y=None,
                              color=(180, 220, 255),  # Cyan-blue
                              width_px=8):
    """Horizontal anamorphic streak overlay."""
    h, w = frame.shape[:2]
    if streak_y is None:
        streak_y = h // 2  # Default to center

    intensity = np.sin(np.pi * t / duration)  # Bell fade

    # Gaussian vertical falloff from streak center
    Y = np.arange(h)
    vertical_profile = np.exp(-((Y - streak_y) ** 2) / (2 * width_px ** 2))
    # Horizontal gradient: brighter at center
    X = np.arange(w)
    horiz_profile = np.exp(-((X - w // 2) ** 2) / (2 * (w * 0.4) ** 2))

    mask = np.outer(vertical_profile, horiz_profile) * intensity * 1.5
    mask = np.clip(mask, 0, 1)[:, :, np.newaxis]

    streak_color = np.array(color, dtype=np.float32)
    overlay = mask * streak_color
    result = frame.astype(np.float32) + overlay
    return np.clip(result, 0, 255).astype(np.uint8)
```

- **Feasibility:** 5/5 — fully procedural; no asset files needed
- **Lines of code:** ~35 lines
- **Best use case:** High-altitude sun transitions; FLYOVER exits; cinematic preset mode
- **Priority:** NICE-TO-HAVE — strong cinematic look but niche

---

## Category 6: Drone-Specific Transitions

### 6.1 Hyperlapse Zoom-Through
**Visual:** End of clip A accelerates dramatically (2x → 8x speed) as if flying forward into subject; clip B starts at normal speed from a closer perspective. Creates virtual zoom-through.

**Implementation approach:** Combine SpeedRamper (already implemented) with ZOOM_IN on tail.
```python
def hyperlapse_zoom_through(clip_a, clip_b, duration=0.8):
    """
    Apply progressive speed ramp + zoom to simulate hyperlapse zoom-through.
    Requires existing SpeedRamper.apply_multiple_ramps().
    """
    from drone_reel.core.speed_ramper import SpeedRamper, SpeedRamp
    ramper = SpeedRamper()

    # Ramp clip_a tail: 1.0x -> 3.0x over last `duration` seconds
    ramp_start = max(0, clip_a.duration - duration)
    exit_ramp = [SpeedRamp(
        start_time=ramp_start,
        end_time=clip_a.duration,
        start_speed=1.0,
        end_speed=3.0,
        easing='ease_in'
    )]
    clip_a_ramped = ramper.apply_multiple_ramps(clip_a, exit_ramp)

    # Apply zoom to ramped clip tail
    clip_a_zoomed = _zoom_transition(clip_a_ramped, duration * 0.5,
                                      zoom_in=True, is_start=False)

    # Ramp clip_b head: 3.0x -> 1.0x for smooth settle
    entry_ramp = [SpeedRamp(
        start_time=0,
        end_time=min(duration, clip_b.duration),
        start_speed=3.0,
        end_speed=1.0,
        easing='ease_out'
    )]
    clip_b_ramped = ramper.apply_multiple_ramps(clip_b, entry_ramp)

    return concatenate_videoclips([clip_a_zoomed, clip_b_ramped])
```

- **Feasibility:** 4/5 — uses SpeedRamper (already implemented); needs SpeedRamp dataclass inspection
- **Lines of code:** ~30 lines
- **Best use case:** FLYOVER to APPROACH transitions; cinematic establishing shots
- **Priority:** MUST-HAVE — viral drone technique per TikTok @TheDroneCreative analysis

---

### 6.2 Cloud/Fog Pass-Through
**Visual:** Simulate drone passing through clouds. Frame progressively fills with white/gray fog texture (generated or sampled), then clears to reveal clip B. Duration: 0.3-0.8s.

**Procedural fog generation approach:**
```python
def perlin_fog_frame(h, w, t, duration, opacity=0.85):
    """
    Generate procedural fog using multi-scale noise.
    Approximates Perlin noise using summed sinusoids (no additional libs).
    """
    intensity = np.sin(np.pi * t / duration)  # Peak at midpoint

    # Multi-frequency noise approximation
    Y, X = np.mgrid[:h, :w] / np.array([h, w], dtype=np.float32)

    # Layer 1: large waves
    noise = np.sin(X * 8 + 0.3) * np.cos(Y * 6 + 0.7) * 0.4
    # Layer 2: medium detail
    noise += np.sin(X * 20 + 1.1) * np.cos(Y * 15 + 2.3) * 0.3
    # Layer 3: fine detail
    noise += np.sin(X * 50 + 0.8) * np.cos(Y * 45 + 1.9) * 0.2
    # Normalize to [0, 1]
    noise = (noise - noise.min()) / (noise.max() - noise.min() + 1e-9)

    fog_alpha = noise * intensity * opacity
    return fog_alpha[:, :, np.newaxis]  # HxW1

def _transition_fog_pass(self, clip1, clip2, duration=0.6):
    w, h = clip1.w, clip1.h
    fog_color = np.array([245, 248, 250], dtype=np.float32)  # Cloud white

    def make_frame(t):
        progress = t / duration
        if progress < 0.5:
            base = clip1.get_frame(clip1.duration - duration + t)
        else:
            base = clip2.get_frame(t - duration / 2)

        fog_alpha = perlin_fog_frame(h, w, t, duration)
        result = base.astype(np.float32) * (1 - fog_alpha) + fog_color * fog_alpha
        return np.clip(result, 0, 255).astype(np.uint8)

    from moviepy import VideoClip
    trans = VideoClip(make_frame, duration=duration)
    return concatenate_videoclips([
        clip1.subclipped(0, clip1.duration - duration / 2),
        trans,
        clip2.subclipped(duration / 2)
    ])
```

**Note:** True Perlin noise requires the `noise` package. The sinusoidal approximation above requires no new dependencies.

- **Feasibility:** 4/5 — procedural (no assets), but visual realism is limited without Perlin noise
- **Lines of code:** ~55 lines
- **Best use case:** Altitude changes; mountain/coastal footage; TILT_UP into sky
- **Priority:** NICE-TO-HAVE — visually distinctive but context-specific

---

### 6.3 FPV Tunnel Zoom (Vortex)
**Visual:** Clip exit creates radial zoom blur (tunnel effect) as if flying at high speed into a vortex. Clip B enters from same effect reversing.

**Implementation approach:** Radial blur using polar coordinate transform.
```python
def radial_zoom_blur_frame(frame, intensity=0.3, steps=8):
    """
    Create radial zoom blur by averaging scaled versions of frame.
    intensity: 0 = no blur, 1 = heavy blur (use 0.1-0.4)
    """
    h, w = frame.shape[:2]
    result = frame.astype(np.float32)

    for i in range(1, steps + 1):
        scale = 1.0 + intensity * (i / steps)
        new_w, new_h = int(w * scale), int(h * scale)
        scaled = cv2.resize(frame, (new_w, new_h))
        # Crop to original size from center
        y_off = (new_h - h) // 2
        x_off = (new_w - w) // 2
        cropped = scaled[y_off:y_off + h, x_off:x_off + w]
        result = result * (1 - 1/steps) + cropped.astype(np.float32) * (1/steps)

    return result.astype(np.uint8)
```

- **Feasibility:** 4/5 — uses cv2.resize (already imported); iterative scaling loop
- **Lines of code:** ~35 lines
- **Best use case:** FPV motion type clips; APPROACH scenes; high-speed drone shots
- **Priority:** NICE-TO-HAVE

---

## Implementation Priority Summary

### MUST-HAVE (High ROI, Low Effort)

| Transition | New Enum Value | Est. LOC | Dependencies |
|---|---|---|---|
| Whiteout Flash (enhanced) | `FLASH_WHITE` | 25 | None (extends FADE_WHITE) |
| RGB Channel Split Glitch | `GLITCH_RGB` | 40 | None (NumPy) |
| Iris Wipe In/Out | `IRIS_IN`, `IRIS_OUT` | 40 | None (NumPy) |
| Light Leak Gradient | `LIGHT_LEAK` | 35 | None (NumPy) |
| Hyperlapse Zoom-Through | `HYPERLAPSE_ZOOM` | 30 | SpeedRamper (existing) |
| Whip Pan Motion Blur | Enhancement to `CUT` | 40 | None (cv2 existing) |
| Orbital Continuation | Enhancement to `CUT` | 60 | None (cv2 existing) |

### NICE-TO-HAVE (Medium ROI, Medium Effort)

| Transition | New Enum Value | Est. LOC | Dependencies |
|---|---|---|---|
| Diagonal Wipe | `WIPE_DIAGONAL` | 30 | None (NumPy) |
| Diamond Wipe | `WIPE_DIAMOND` | 25 | None (NumPy) |
| Parallax Slide | `PARALLAX_LEFT`, `PARALLAX_RIGHT` | 60 | None (NumPy) |
| Split Screen Reveal | `SPLIT_REVEAL` | 35 | None (NumPy) |
| Anamorphic Streak | `STREAK_FLASH` | 35 | None (NumPy) |
| Scan Line Flash | `SCANLINE_FLASH` | 25 | None (NumPy) |
| Cloud/Fog Pass | `FOG_PASS` | 55 | Optional: `noise` pkg |
| FPV Vortex Zoom | `VORTEX_ZOOM` | 35 | cv2 (existing) |
| Slow-Mo Peak Freeze | Enhancement to SpeedRamper | 10 | SpeedRamper (existing) |
| Altitude Match Cut | Enhancement to `CUT` | 80 | cv2 ORB (existing) |

### EXPERIMENTAL (Low ROI, High Effort or Niche)

| Transition | Est. LOC | Notes |
|---|---|---|
| Pixel Sort | 50-80 | Slow without CUDA; Python loop bottleneck |
| Datamosh Simulation | 40 | Block-based sim OK; true datamosh needs FFmpeg bitstream |
| Diamond/Iris variants | 25 each | Low priority vs IRIS_IN |

---

## Architecture Recommendations

### 1. Transition Base Class Pattern
Currently transitions are private methods on `VideoProcessor`. For the new set, consider a modular approach:

```python
# video_processor.py additions
class TransitionEffect:
    """Base for compositing transitions (as opposed to clip-level effects)."""
    def apply(self, clip1, clip2, duration) -> VideoFileClip:
        raise NotImplementedError

class IrisWipeTransition(TransitionEffect):
    def __init__(self, feather=4):
        self.feather = feather
    def apply(self, clip1, clip2, duration):
        ...
```

This makes transitions independently testable and extendable without growing `VideoProcessor` further.

### 2. Motion-Matched Auto-Selection Extension
Extend `select_motion_matched_transition()` with new cases:

```python
# New cases to add to existing method
if scene1.motion_type == MotionType.FPV:
    return TransitionType.GLITCH_RGB, 0.15  # Glitch cut for FPV
if scene1.motion_type in (MotionType.TILT_UP,) and scene2.hook_tier == HookPotential.MAXIMUM:
    return TransitionType.IRIS_IN, 0.4  # Dramatic reveal
if scene1.is_golden_hour or scene2.is_golden_hour:
    return TransitionType.LIGHT_LEAK, 0.5  # Cinematic light
if scene1.motion_type == MotionType.FLYOVER:
    return TransitionType.HYPERLAPSE_ZOOM, 0.6
```

### 3. New TransitionType Enum Values to Add
```python
class TransitionType(Enum):
    # Existing
    CUT = "cut"
    CROSSFADE = "crossfade"
    FADE_BLACK = "fade_black"
    FADE_WHITE = "fade_white"
    ZOOM_IN = "zoom_in"
    ZOOM_OUT = "zoom_out"
    SLIDE_LEFT = "slide_left"
    SLIDE_RIGHT = "slide_right"
    WIPE_LEFT = "wipe_left"       # existing but unimplemented
    WIPE_RIGHT = "wipe_right"     # existing but unimplemented

    # New Must-Have
    FLASH_WHITE = "flash_white"      # Enhanced non-linear whiteout
    GLITCH_RGB = "glitch_rgb"        # RGB channel split
    IRIS_IN = "iris_in"              # Circle reveal
    IRIS_OUT = "iris_out"            # Circle close
    LIGHT_LEAK = "light_leak"        # Diagonal color gradient
    HYPERLAPSE_ZOOM = "hyperlapse_zoom"  # Speed+zoom through

    # New Nice-To-Have
    WIPE_DIAGONAL = "wipe_diagonal"
    WIPE_DIAMOND = "wipe_diamond"
    PARALLAX_LEFT = "parallax_left"
    PARALLAX_RIGHT = "parallax_right"
    SPLIT_REVEAL = "split_reveal"
    STREAK_FLASH = "streak_flash"
    FOG_PASS = "fog_pass"
    VORTEX_ZOOM = "vortex_zoom"
```

---

## Performance Considerations

| Transition | Per-Frame Cost | Notes |
|---|---|---|
| RGB Glitch | Very low | 3 NumPy slice ops, <1ms/frame |
| Iris Wipe | Low | Distance array + blend, ~2ms/frame |
| Light Leak | Low | Gaussian + additive, ~2ms/frame |
| Whiteout Flash | Very low | Scalar multiply, <1ms/frame |
| Parallax Slide | Medium | Two get_frame() calls per frame, ~5ms |
| Fog Pass | Medium | Multi-freq sinusoid, ~8ms/frame at 1080p |
| Pixel Sort | High | Column iteration in Python, ~100ms/frame |
| Vortex Zoom | Medium | 8 cv2.resize calls, ~15ms/frame |
| Datamosh Sim | Medium | Block iteration, ~20ms/frame |

All transitions operate on MoviePy's per-frame lambda model. Frame costs apply to the transition segment only (typically 0.2-0.8s = 6-24 frames at 30fps).

---

## References

- [OpenCV Optical Flow Tutorial](https://docs.opencv.org/3.4/d4/dee/tutorial_optical_flow.html)
- [Python Glitch Art & Image Processing](https://chezsoi.org/lucas/blog/glitch-art-and-image-processing-with-python.html)
- [RGB Channel Shifting Technique](http://datamoshing.com/2016/06/29/how-to-glitch-images-using-rgb-channel-shifting/)
- [satyarth/pixelsort — Python Pixel Sorting](https://github.com/satyarth/pixelsort)
- [tiberiuiancu/datamoshing — Python Datamoshing](https://github.com/tiberiuiancu/datamoshing)
- [torrober/vhs.py — VHS Effect Emulator](https://github.com/torrober/vhs.py)
- [MoviePy Transitions Discussion](https://github.com/Zulko/moviepy/discussions/2119)
- [Drone Orbit + Speed Ramp Technique (TikTok)](https://www.tiktok.com/@thedronecreative/video/7380822378483338528)
- [Top 5 Video Transitions for Reels/TikTok 2025](https://aaapresets.com/en-de/blogs/video-editing-tips/top-5-video-transitions-to-boost-engagement-in-reels-and-tiktoks-in-2025)
- [Speed Ramping with Bezier Curves — Adobe Guide](https://www.adobe.com/creativecloud/video/hub/guides/premiere-pro-speed-ramp.html)
- [Parallax Image (depth map layers)](https://github.com/strikeraryu/Parallax_Image)
- [Anamorphic Streak — Lindsey Optics](https://www.lindseyoptics.com/blog/what-is-a-streak-filter-how-to-get-anamorphic-lens-flare/)
