# Visual Enhancements Roadmap - drone-reel CLI

**Synthesized from:** Viral Trends Research, Professional Software Analysis, Color Science Research, Transition Effects Research
**Date:** 2026-02-21

---

## Executive Summary

### Current Tool Capabilities
The drone-reel CLI currently provides: 10 color presets (cinematic, warm_sunset, cool_blue, vintage, high_contrast, muted, vibrant, teal_orange, black_white, drone_aerial), 10 transition types (cut, crossfade, fade_black, fade_white, zoom_in, zoom_out, slide_left, slide_right, wipe_left, wipe_right), 5 reframe modes (center, smart, ken_burns, punch_in, subject_track), adaptive stabilization, speed ramping with auto-detect, text overlays with fade animation, beat-synced editing with downbeat mode, 1D LUT support, shadow lift, selective HSL adjustments, per-channel tone curves, and grain in ColorAdjustments.

### Enhancement Scope
- **Total new enhancements identified:** 62 distinct items across color presets, transitions, visual effects, and pipeline features
- **New color presets:** 16 (5 time-of-day, 6 terrain, 5 cinematic/social)
- **New transitions:** 18 (7 must-have, 8 nice-to-have, 3 experimental)
- **New visual effects/pipeline features:** 18 (post-processing effects, color science, audio)
- **Expected viral readiness improvement:** From ~65% to ~90%+ parity with professional editing tools for automated short-form drone content

---

## Top 10 Highest-Impact Additions

### 1. 3D LUT (.cube) File Loading and Application
- **Description:** Load industry-standard .cube 3D LUT files (33x33x33 or 64x64x64) and apply trilinear interpolation per frame. Current ColorGrader only supports 1D lookup tables. This enables DJI D-Log correction, thousands of free/commercial creative LUTs, and instant professional looks.
- **Reports:** Pro Software (#1), Color Science (LUT equivalents section)
- **Implementation:** New `lut_manager.py` module. Parse .cube header for LUT_3D_SIZE, build 3D array, trilinear interpolation via `colour-science` library or manual implementation. CLI flag: `--lut PATH`.
- **Estimated LOC:** 150
- **Dependencies:** `colour-science` or `pycubelut` (new pip dependency)
- **Priority:** CRITICAL

### 2. Vignette Effect
- **Description:** Radial gradient darkening toward frame edges. Universally used in cinematic content. Draws viewer attention to center subject, adds professional filmic quality.
- **Reports:** Pro Software (#2), Color Science (blue_hour, night_city, dark_moody presets), Viral Trends (LOW engagement but universal base)
- **Implementation:** NumPy distance mask with sigmoid falloff in `ColorGrader`. CLI flag: `--vignette FLOAT` (0.0-1.0). Also auto-applied by certain presets.
- **Estimated LOC:** 40
- **Dependencies:** None (numpy existing)
- **Priority:** CRITICAL

### 3. Whip Pan / Motion Blur Transition
- **Description:** Fast horizontal blur streak used as cut between scenes. The #1 visual signature of modern viral drone reels on TikTok/Instagram.
- **Reports:** Viral Trends (HIGH engagement), Pro Software (#13), Transitions (1.1 + motion blur enhancement)
- **Implementation:** Directional motion blur kernel via `cv2.filter2D` with horizontal/vertical kernel. Detection via existing optical flow. New enum `WHIP_PAN` in TransitionType.
- **Estimated LOC:** 60
- **Dependencies:** None (OpenCV existing)
- **Priority:** CRITICAL

### 4. RGB Channel Split / Glitch Transition
- **Description:** R/G/B channels separate horizontally for 3-5 frames at cut point. Creates "digital glitch" effect extremely common in 2025 social media edits.
- **Reports:** Viral Trends (glitch effect), Pro Software (#3 chromatic aberration), Transitions (4.1 RGB Channel Split)
- **Implementation:** NumPy array slice shifting per channel. Triangle wave intensity curve. New enum `GLITCH_RGB`.
- **Estimated LOC:** 40
- **Dependencies:** None (NumPy existing)
- **Priority:** CRITICAL

### 5. Halation / Bloom Effect
- **Description:** Red-orange glow around bright highlights simulating analog film light reflection. Creates warm, organic, filmic feel. Heavily used in cinematic drone editing 2024-2026.
- **Reports:** Pro Software (#4), Color Science (night_city preset, Kodak 2383 emulation), Viral Trends (film emulation trend)
- **Implementation:** Extract highlights from red channel, Gaussian blur, blend back with strength parameter. Add to `ColorGrader`.
- **Estimated LOC:** 70
- **Dependencies:** None (OpenCV existing)
- **Priority:** HIGH

### 6. D-Log / Log Footage Auto-Normalization
- **Description:** Auto-detect flat log-encoded footage (DJI D-Log M, D-Log) and apply gamma expansion before creative grading. Without this, all presets produce incorrect results on professional DJI footage.
- **Reports:** Pro Software (#10), Color Science (ARRI LogC, RED IPP2 sections)
- **Implementation:** Detection heuristic (low contrast + mid brightness), D-Log M decode curve, CLI flag: `--input-colorspace [rec709|dlog|dlog_m|slog3]`.
- **Estimated LOC:** 150
- **Dependencies:** None (numpy existing)
- **Priority:** HIGH

### 7. Iris Wipe Transition (In/Out)
- **Description:** Clip B reveals from expanding circle centered on frame. Classic cinematic effect with high visual impact. Common in professional drone edits for reveals.
- **Reports:** Transitions (3.1, MUST-HAVE)
- **Implementation:** NumPy circular distance mask with feathered edge, expanding over time. New enums `IRIS_IN`, `IRIS_OUT`.
- **Estimated LOC:** 40
- **Dependencies:** None (NumPy existing)
- **Priority:** HIGH

### 8. Auto Color Match / Scene Consistency
- **Description:** Automatically normalize color across clips from different lighting conditions using histogram matching. Makes multi-clip reels feel like one continuous session.
- **Reports:** Pro Software (#6), Viral Trends (Sam Kolder style consistency)
- **Implementation:** `skimage.exposure.match_histograms` with reference frame selection. Per-clip normalization pass before creative grading. CLI flag: `--auto-color-match`.
- **Estimated LOC:** 120
- **Dependencies:** `scikit-image` (may need pip install)
- **Priority:** HIGH

### 9. Cinematic Letterbox Bars
- **Description:** Add 2.35:1 or 2.39:1 anamorphic black bars to any output format. Major Instagram disruptor in 2025 (5120x1080 trend). Signals "cinematic" quality even on vertical format.
- **Reports:** Viral Trends (HIGH engagement, Instagram trend), Pro Software (#17)
- **Implementation:** MoviePy CompositeVideoClip with black bar clips on top/bottom. CLI flag: `--letterbox [2.35|1.85|2.39]`.
- **Estimated LOC:** 60
- **Dependencies:** None (MoviePy existing)
- **Priority:** HIGH

### 10. Light Leak / Gradient Transition
- **Description:** Colored gradient (amber/orange or cyan) sweeps diagonally across frame during transition, simulating film light leak. Procedurally generated.
- **Reports:** Pro Software (#16), Transitions (5.2 Light Leak Gradient, MUST-HAVE), Viral Trends (light leaks LOW engagement but cinematic base)
- **Implementation:** Gaussian sweep with configurable color. New enum `LIGHT_LEAK`. Fully procedural, no asset files.
- **Estimated LOC:** 35
- **Dependencies:** None (NumPy existing)
- **Priority:** HIGH

---

## Quick Wins (< 50 LOC each)

| # | Name | Description | Implementation | LOC | Priority |
|---|------|-------------|---------------|-----|----------|
| 1 | Vignette Effect | Radial gradient edge darkening | NumPy distance mask in ColorGrader, `--vignette FLOAT` | 40 | CRITICAL |
| 2 | RGB Glitch Transition | Channel split at cut points | NumPy slice shifting, new `GLITCH_RGB` enum | 40 | CRITICAL |
| 3 | Iris Wipe In/Out | Circle reveal/close transition | NumPy circular mask, new `IRIS_IN`/`IRIS_OUT` enums | 40 | HIGH |
| 4 | Light Leak Transition | Diagonal warm gradient sweep | Procedural Gaussian sweep, new `LIGHT_LEAK` enum | 35 | HIGH |
| 5 | Whiteout Flash (Enhanced) | Non-linear flash with fast rise/slow fall | Exponential curve extending FADE_WHITE, `FLASH_WHITE` enum | 25 | HIGH |
| 6 | Diamond Wipe | Diamond-shaped reveal from center | L1 distance mask (shares iris infrastructure) | 25 | LOW |
| 7 | Diagonal Wipe | Diagonal line sweep reveal | Projected coordinate mask with feathering | 30 | LOW |
| 8 | Scan Line Flash | CRT-style sweep at cut point | Horizontal band overlay with sine fade | 25 | LOW |
| 9 | Whoosh Cut (Speed Ramp Transition) | Speed ramp up at exit, ramp down at entry | Ramp config factory using existing SpeedRamper | 15 | MEDIUM |
| 10 | Slow-Mo Peak Freeze | Hold best frame at 0.1x for 0.3s | SpeedRamper configuration for MAXIMUM hook clips | 10 | MEDIUM |
| 11 | Anamorphic Streak Flash | Horizontal cyan-blue lens flare streak | Gaussian vertical/horizontal profiles, additive blend | 35 | LOW |
| 12 | Split Screen Reveal | Top/bottom halves slide apart | NumPy row slicing with offset | 35 | LOW |

---

## Medium Features (50-200 LOC)

| # | Name | Description | Implementation | LOC | Priority |
|---|------|-------------|---------------|-----|----------|
| 1 | Whip Pan Transition | Directional motion blur streak between clips | cv2.filter2D horizontal kernel + flow detection, `WHIP_PAN` enum | 60 | CRITICAL |
| 2 | Halation / Bloom | Red-orange glow around highlights | Gaussian blur on highlight mask, blend back in ColorGrader | 70 | HIGH |
| 3 | Letterbox Bars | Cinematic 2.35:1 black bars | CompositeVideoClip in VideoProcessor, `--letterbox` CLI | 60 | HIGH |
| 4 | Chromatic Aberration Effect | RGB channel lateral offset toward edges | cv2.warpAffine per-channel with radial variant, `--chromatic-aberration` | 80 | HIGH |
| 5 | Audio Ducking (Outro Fade) | Smooth music fade-out in final 2-3 seconds | MoviePy audio volume transform, `--duck-outro` CLI | 80 | HIGH |
| 6 | Film Grain (Upgraded) | Temporal per-frame grain with luminance weighting | RNG per frame_index, Gaussian blur for grain size, midtone bell curve | 80 | HIGH |
| 7 | Orbital Continuation Cut | Matching orbit cuts using flow curl detection | Curl computation on optical flow field | 60 | MEDIUM |
| 8 | Parallax Slide | Differential speed slide (depth illusion) | Dual get_frame with speed ratio, `PARALLAX_LEFT`/`PARALLAX_RIGHT` | 60 | MEDIUM |
| 9 | Atmospheric Haze / Depth Fog | Gradient haze from horizon for aerial depth | Gradient mask blended with haze color in ColorGrader | 90 | MEDIUM |
| 10 | Noise Reduction | Spatial denoising for low-light footage | cv2.bilateralFilter or fastNlMeansDenoisingColored, `--denoise` | 80 | MEDIUM |
| 11 | Auto White Balance | Gray world channel normalization | Per-channel mean scaling, `--auto-wb` CLI | 80 | MEDIUM |
| 12 | GND Sky Correction Filter | Graduated exposure darkening for sky | Linear gradient mask with exposure factor, `--gnd-sky` | 70 | MEDIUM |
| 13 | Lens Distortion Correction | Barrel/fisheye removal for DJI/FPV cameras | cv2.initUndistortRectifyMap with camera profiles, `--lens-model` | 100 | MEDIUM |
| 14 | Audio Section Detection | Classify intro/build/drop/outro for energy matching | librosa spectral flux + RMS energy sections in BeatSync | 100 | MEDIUM |
| 15 | Cloud/Fog Pass Transition | Procedural fog obscures then reveals new clip | Multi-freq sinusoid fog generation, `FOG_PASS` enum | 55 | LOW |
| 16 | FPV Vortex Zoom | Radial zoom blur tunnel effect | Iterative cv2.resize + center crop averaging, `VORTEX_ZOOM` | 55 | LOW |
| 17 | Motion Blur Frame Blending | Simulate 180-degree shutter via frame averaging | Weighted frame buffer in VideoProcessor, `--motion-blur` | 100 | LOW |
| 18 | Lens Flare (Procedural) | Anamorphic streak + bokeh from sun position | Procedural generation with screen blend, `--lens-flare` | 150 | LOW |

---

## Major Features (200+ LOC)

| # | Name | Description | Implementation | LOC | Dependencies | Priority |
|---|------|-------------|---------------|-----|-------------|----------|
| 1 | 3D LUT (.cube) Loading | Load/apply industry-standard .cube 3D LUTs | New `lut_manager.py`: parse .cube, trilinear interp, `--lut PATH` | 150-200 | `colour-science` or `pycubelut` | CRITICAL |
| 2 | D-Log Auto-Normalization | Detect + decode DJI D-Log M/D-Log footage | New `colorspace.py`: detection heuristic + decode curves, `--input-colorspace` | 150-200 | None | HIGH |
| 3 | Auto Color Match | Histogram-based cross-clip color normalization | Reference frame selection + per-clip match pass, `--auto-color-match` | 120-150 | `scikit-image` | HIGH |
| 4 | Sky Masking + Selective Grade | Auto-detect sky region, grade sky/ground independently | HSV threshold + morphological cleanup + dual grade pass | 130-150 | None (OpenCV) | MEDIUM |
| 5 | Transition Base Class Refactor | Modular transition pattern for extensibility | TransitionEffect base class, per-transition subclasses | 200+ | None | MEDIUM |
| 6 | 16 New Color Presets | Time-of-day + terrain + cinematic + social presets | ColorAdjustments configs with HSV/LAB params per preset | 300+ | None | HIGH |
| 7 | Telemetry HUD Overlay | Extract DJI GPS/speed/altitude from SRT tracks | ffprobe SRT parsing + HUD positioning via TextOverlay, `--telemetry-hud` | 200 | ffprobe (system) | LOW |
| 8 | Hyperlapse Zoom-Through | Combined speed ramp + zoom for flyover transitions | SpeedRamper exit ramp + zoom tail, `HYPERLAPSE_ZOOM` enum | 30 (transition) + 200 (auto-detect) | SpeedRamper (existing) | HIGH |

---

## New Color Presets

### Time-of-Day Presets

| Preset Name | Description | Key Adjustments | Reports |
|-------------|-------------|-----------------|---------|
| `golden_hour` | Warm amber-orange with cool shadow undertones | Temp +300K, highlights -50, vibrance +30, orange/yellow sat boost, LAB warm highlights | Color Science (1.1), Viral Trends |
| `blue_hour` | Deep indigo-blue ethereal atmosphere | Temp -400K, blue sat +30, LAB b -10 global, deep blue shadows, vignette 40% | Color Science (1.2) |
| `harsh_midday` | Dynamic range recovery for overhead sun | Highlights -90, shadows +70, vibrance +50, blue sat +30, green sat -15 | Color Science (1.3) |
| `overcast` | Soft diffused documentary feel | Temp -75K, contrast +8, clarity +25, sat -8, vibrance +10, green sat +10 | Color Science (1.4) |
| `night_city` | Deep blacks with warm artificial light pools | Exposure -0.7, contrast +40, orange sat +30, blue sat +25, vignette 50%, halation | Color Science (1.5) |

### Terrain-Aware Presets

| Preset Name | Description | Key Adjustments | Reports |
|-------------|-------------|-----------------|---------|
| `ocean_coastal` | Teal water + warm sand separation | Cyan hue -5 toward blue, cyan sat +20, orange/yellow sat +25, dehaze +20 | Color Science (2.1) |
| `forest_jungle` | Anti-neon green with canopy shadow lift | Green hue -5 toward cyan, green sat -12, shadows +40, clarity +25, LAB a +3 | Color Science (2.2) |
| `urban_city` | High-contrast architecture with neon control | Contrast +30, clarity +20, cool blue shadows, orange/red sat +20, vignette 25% | Color Science (2.3), Viral Trends |
| `desert_arid` | Warm earth tones without over-saturation | Orange sat -12, highlights -60, blue sat +20, temp +200K, dehaze +20 | Color Science (2.4) |
| `snow_mountain` | Blue cast correction with sky depth | WB +75K, highlights -70, blue sat -25, cyan sat -15, vibrance +20 | Color Science (2.5) |
| `autumn_foliage` | Rich reds/oranges without garish tones | Orange sat +30 hue -5, red sat +20, green sat -20, temp +150K, sky blue +20 | Color Science (2.6) |

### Cinematic Film Emulation Presets

| Preset Name | Description | Key Adjustments | Reports |
|-------------|-------------|-----------------|---------|
| `kodak_2383` | Warm 90s cinema: deep blacks, gentle highlight rolloff | S-curve with toe lift + shoulder compress, LAB b +6 warm, green hue +5 toward yellow | Color Science (3.1) |
| `fujifilm_3513` | Cool-neutral with teal shadows, magenta midtones | LAB shadow b -4 (teal), midtone a +3 (magenta), cool highlights | Color Science (3.4) |
| `technicolor_2strip` | Vintage 1920s: cyan-green + red-orange only | Blue channel suppressed 70%, red +20%, green +10%, LAB b +10 warm | Color Science (3.5) |

### Social Media Trend Presets

| Preset Name | Description | Key Adjustments | Reports |
|-------------|-------------|-----------------|---------|
| `desaturated_moody` | Crushed blacks with selective blue/cyan retention | Global sat -35, blue/cyan preserved, blacks -50, contrast +35, vignette 50% | Color Science (4.2), Viral Trends (moody dark) |
| `warm_pastel` | Soft faded film wash: lifted blacks, low contrast | Blacks +40 (matte), contrast -25, sat -20, temp +150K, tint +5 pink | Color Science (4.3) |
| `cyberpunk_neon` | Near-black with electric neon pops (cyan/magenta/orange) | Exposure -1.0, blacks -70, cyan sat +50, magenta sat +40, vignette 60% | Color Science (4.4), Viral Trends (FPV urban) |
| `hyper_natural` | Documentary authenticity: faithful color, minimal manipulation | WB matched, exposure +0.1, contrast +7, sat +3, vibrance +8, no split toning | Color Science (4.5) |
| `film_emulation` | Faded blacks, warm color cast, halation glow, green shadows | Blacks +20, warm cast +8 LAB b, halation on highlights, shadow green tint | Viral Trends (vintage/analog trend) |

---

## New Transitions

| # | Transition Name | Enum Value | Description | Feasibility | LOC | Best Motion Type Match | Priority |
|---|----------------|------------|-------------|-------------|-----|----------------------|----------|
| 1 | Whip Pan | `WHIP_PAN` | Directional motion blur streak | 5/5 | 60 | PAN_LEFT, PAN_RIGHT | CRITICAL |
| 2 | RGB Glitch Cut | `GLITCH_RGB` | RGB channel split for 3-5 frames | 5/5 | 40 | FPV, any high-energy | CRITICAL |
| 3 | Iris Wipe In | `IRIS_IN` | Circle expanding to reveal new clip | 5/5 | 40 | REVEAL, MAXIMUM hook | HIGH |
| 4 | Iris Wipe Out | `IRIS_OUT` | Circle closing on current clip | 5/5 | (shared) | Any exit to black | HIGH |
| 5 | Light Leak | `LIGHT_LEAK` | Diagonal amber/cyan gradient sweep | 5/5 | 35 | TILT_UP, golden hour | HIGH |
| 6 | Whiteout Flash | `FLASH_WHITE` | Non-linear overexposure burst | 5/5 | 25 | REVEAL into bright sky | HIGH |
| 7 | Hyperlapse Zoom | `HYPERLAPSE_ZOOM` | Speed ramp + zoom fly-through | 4/5 | 30 | FLYOVER, APPROACH | HIGH |
| 8 | Orbital Continuation | Enhanced `CUT` | Orbit-matched hard cut via curl | 4/5 | 60 | ORBIT_CW, ORBIT_CCW | MEDIUM |
| 9 | Whoosh Cut | Enhanced `CUT` + SpeedRamper | Speed ramp exit/entry at cut | 5/5 | 15 | Beat drops, direction changes | MEDIUM |
| 10 | Parallax Slide L/R | `PARALLAX_LEFT`/`RIGHT` | Depth illusion via differential speed | 4/5 | 60 | PAN exits, landscape | MEDIUM |
| 11 | Diagonal Wipe | `WIPE_DIAGONAL` | 45-degree line sweep | 5/5 | 30 | Scene direction changes | LOW |
| 12 | Diamond Wipe | `WIPE_DIAMOND` | L1 distance expanding diamond | 5/5 | 25 | High-energy beats | LOW |
| 13 | Split Reveal | `SPLIT_REVEAL` | Top/bottom halves slide apart | 5/5 | 35 | TILT transitions | LOW |
| 14 | Anamorphic Streak | `STREAK_FLASH` | Horizontal cyan-blue flare streak | 5/5 | 35 | FLYOVER exits, sun shots | LOW |
| 15 | Scan Line Flash | `SCANLINE_FLASH` | CRT horizontal sweep | 5/5 | 25 | STATIC to high-motion | LOW |
| 16 | Cloud/Fog Pass | `FOG_PASS` | Procedural fog obscure/reveal | 4/5 | 55 | Altitude changes, mountain | LOW |
| 17 | FPV Vortex Zoom | `VORTEX_ZOOM` | Radial zoom blur tunnel | 4/5 | 55 | FPV, APPROACH | LOW |
| 18 | Pixel Sort | `PIXEL_SORT` | Glitch art pixel sorting | 3/5 | 80 | Experimental/artistic | EXPERIMENTAL |

---

## Implementation Phases

### Phase 1: Quick Wins + Top 3 Must-Haves (1-2 days)

**Goal:** Largest viral readiness jump with minimal code. ~400 LOC total.

| Order | Item | Type | LOC | Why First |
|-------|------|------|-----|-----------|
| 1 | Vignette effect | Visual effect | 40 | Universal cinematic base; auto-included in multiple presets |
| 2 | Whip Pan transition | Transition | 60 | #1 viral drone transition per all reports |
| 3 | RGB Glitch Cut transition | Transition | 40 | #1 social media cut style; trivial to implement |
| 4 | Iris Wipe In/Out transitions | Transition | 40 | High visual impact, classic cinematic reveal |
| 5 | Whiteout Flash transition | Transition | 25 | Extends existing FADE_WHITE with non-linear curve |
| 6 | Light Leak transition | Transition | 35 | Procedural, no assets, high cinematic value |
| 7 | Letterbox bars | Video effect | 60 | Major Instagram 2025 trend; simple CompositeVideoClip |
| 8 | Audio ducking (outro fade) | Audio | 80 | Every viral reel needs smooth audio ending |
| 9 | Whoosh Cut (speed ramp transition) | Transition | 15 | Uses existing SpeedRamper; just config |

**Phase 1 Deliverables:**
- 6 new transition types in TransitionType enum
- `--vignette`, `--letterbox`, `--duck-outro` CLI flags
- Updated `select_motion_matched_transition()` for new types
- Tests for all new transitions and effects

### Phase 2: Medium Features + Color Presets (3-5 days)

**Goal:** Professional color science and remaining high-priority features. ~1200 LOC total.

| Order | Item | Type | LOC | Why Phase 2 |
|-------|------|------|-----|-------------|
| 1 | 3D LUT (.cube) loading | Color | 150-200 | Unlocks thousands of professional LUTs |
| 2 | D-Log auto-normalization | Color | 150-200 | Required for professional DJI footage |
| 3 | 16 new color presets | Color | 300+ | Time-of-day, terrain, cinematic, social presets |
| 4 | Halation / bloom effect | Visual | 70 | Cinematic film look; auto-included in presets |
| 5 | Film grain upgrade | Visual | 80 | Temporal + luminance-weighted; fixes existing grain |
| 6 | Chromatic aberration effect | Visual | 80 | FPV aesthetic; creative stylization |
| 7 | Auto color match | Color | 120 | Cross-clip consistency |
| 8 | Hyperlapse zoom transition | Transition | 30 | Viral drone-specific technique |

**Phase 2 Deliverables:**
- New `lut_manager.py` and `colorspace.py` modules
- 16 new preset entries in ColorGrader
- `--lut`, `--input-colorspace`, `--chromatic-aberration`, `--halation`, `--auto-color-match` CLI flags
- `HYPERLAPSE_ZOOM` transition
- New dependency: `colour-science` (or `pycubelut`)
- Tests for all new presets and features

### Phase 3: Major Features + Experimental (1-2 weeks)

**Goal:** Advanced features, polish, and experimental capabilities. ~1500 LOC total.

| Order | Item | Type | LOC | Why Phase 3 |
|-------|------|------|-----|-------------|
| 1 | Auto white balance | Color | 80 | Per-clip WB normalization |
| 2 | Noise reduction | Visual | 80 | Low-light footage quality |
| 3 | Lens distortion correction | Visual | 100 | FPV/wide-angle correction |
| 4 | Sky masking + selective grade | Color | 130 | Professional sky/ground independent grading |
| 5 | Atmospheric haze | Visual | 90 | Aerial depth enhancement |
| 6 | GND sky correction filter | Visual | 70 | Exposure balance for bright skies |
| 7 | Audio section detection | Audio | 100 | Energy-matched clip sequencing |
| 8 | Transition base class refactor | Architecture | 200+ | Modular transitions for extensibility |
| 9 | Remaining transitions | Transitions | 300+ | Parallax, diagonal, diamond, fog, vortex, etc. |
| 10 | Motion blur frame blending | Visual | 100 | 180-degree shutter simulation |
| 11 | Lens flare (procedural) | Visual | 150 | Procedural sun flare |
| 12 | Telemetry HUD overlay | Feature | 200 | GPS/speed/altitude DJI overlay |

**Phase 3 Deliverables:**
- `--auto-wb`, `--denoise`, `--lens-model`, `--gnd-sky`, `--motion-blur` CLI flags
- Sky masking integration in ColorGrader
- Audio section classification in BeatSync
- TransitionEffect base class with modular pattern
- 8+ additional transition types
- Telemetry extraction and HUD (experimental)
- Potential new dependency: `scikit-image` (for histogram matching)

---

## Dependency Summary

| Dependency | Status | Features Requiring It | Phase |
|-----------|--------|----------------------|-------|
| numpy | Existing | Vignette, transitions, grain, haze, GND, AWB | All |
| OpenCV | Existing | Whip pan, halation, CA, denoise, sky mask, distortion | All |
| MoviePy | Existing | Letterbox, audio duck, all transitions | All |
| librosa | Existing | Audio section detection | 3 |
| SpeedRamper | Existing | Whoosh cut, hyperlapse zoom, slow-mo freeze | 1-2 |
| `colour-science` OR `pycubelut` | **New** | 3D LUT loading | 2 |
| `scikit-image` | **New (optional)** | Auto color match (histogram matching) | 2-3 |
| ffprobe | **System** | Telemetry HUD overlay | 3 |

---

## Risk Assessment

- **Highest risk:** 3D LUT loading performance -- trilinear interpolation per-pixel per-frame could be slow. Mitigation: pre-compute interpolation table, apply as vectorized NumPy operation.
- **Medium risk:** D-Log decode curves are approximate without official DJI SDK. Mitigation: provide manual `--input-colorspace` override; test against known D-Log footage.
- **Low risk:** New transitions may conflict with existing `select_motion_matched_transition()`. Mitigation: extend selection logic incrementally; default to proven transitions.
- **Performance note:** All per-frame effects (vignette, halation, CA, grain) add processing time. Consider lazy evaluation and `--fast` mode that skips non-essential effects.
