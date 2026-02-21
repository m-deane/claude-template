# V21 Viral Benchmark Review -- Consolidated Enhancement Roadmap

**Date**: 2026-02-20
**Inputs**: Visual Analysis, Viral Research, Technical Quality Analysis, Opus Codebase Review
**Branch**: `claude/ai-video-stitching-research-DGpPg`

---

## Executive Summary

The drone-reel tool produces technically valid H.264 MP4 files with correct aspect ratio, high 4K resolution, and clean stabilization. However, the **output is not competitive for social media virality**. The visual analysis scored both test renders at **5.0/10** overall, with critical failures in opening hook quality (2/10), scene variety (4/10), and pacing/energy (3/10). The technical analysis found the rendered files are **missing audio entirely**, use **excessive bitrate (80 Mbps vs 8-15 Mbps recommended)**, and lack **color space metadata**. The strongest content (mountain dusk panorama, marine life overhead) is buried in the back half of the reel while featureless ocean occupies the first 7 seconds.

The core algorithmic pipeline (SceneDetector, BeatSync, SceneFilter, SceneSequencer, DiversitySelector) is architecturally sound, with most P0/P1 bugs from the codebase review already fixed across Phases 1-7. The remaining gaps are in **how the pipeline assembles and renders clips**, not in the individual module quality.

---

## Critical Fixes (Must-Have for Any Viral Potential)

These issues make the current output non-viable for social media distribution.

### CF-1. Audio Track Missing from Output
- **What**: Rendered videos have zero audio streams. Social platforms deprioritize silent videos; Instagram/TikTok auto-play muted but still expect an audio track. Even when `--music` is provided, the output may lack audio if the music path is not passed through the pipeline correctly when using `return_clip=True` followed by a separate `write_videofile` call.
- **Where**: `src/drone_reel/cli.py` -- the code path around lines 873-951 where `stitch_clips(return_clip=True)` is used for color grading, followed by a manual `write_videofile`. The audio attachment happens inside `stitch_clips` at `video_processor.py:472-478`, but when `return_clip=True` is used, the caller's `write_videofile` call at `cli.py:915-925` must also specify `audio_codec`. Additionally, when no `--music` is provided, there is no silent audio track injected.
- **Impact**: 10/10 -- Without audio, the video will be algorithmically suppressed on every major platform. This is the single most damaging technical deficiency.
- **Complexity**: S -- Two fixes needed: (1) ensure `audio_codec="aac"` is passed in the CLI's manual `write_videofile` call; (2) add a silent audio track when no music is provided (MoviePy can generate silence via `AudioClip`).
- **Rationale**: Technical analysis found "CRITICAL: Both videos have zero audio streams." Viral research confirms all platforms expect audio; Instagram's algorithm specifically weights audio presence.

### CF-2. Opening Hook Uses Worst Content Instead of Best
- **What**: The scene sequencer places low-interest content (featureless ocean surface) at position 0, wasting the critical first 1-3 seconds where 50% of viewers decide to stay or scroll. The strongest content (mountain dusk panorama scored as "STRONGEST FRAME IN THE REEL", marine life overhead scored as "EXCELLENT subject interest") appears at 15s and 22s respectively.
- **Where**: `src/drone_reel/core/scene_sequencer.py` -- `SceneSequencer.sequence()` method. The hook ordering uses `hook_tier` which is now computed from actual scores (Phase 5 fix), but the sequencer may not be enforcing a hard constraint that position 0 MUST be the highest-scoring hook scene. Also check `src/drone_reel/cli.py` for how `SceneSequencer` is invoked.
- **Impact**: 10/10 -- Viral research: "The average viewer decides to swipe within 1-2 seconds. Up to 50% drop off in the first 3 seconds." A boring opener guarantees scroll-past.
- **Complexity**: M -- The SceneSequencer needs to enforce: (a) position 0 must be hook_tier HIGH or MAXIMUM; (b) if no scene qualifies, pick the highest-scoring scene regardless of tier; (c) prefer scenes with dynamic motion (PAN, ORBIT, FLYOVER) over static for opener.
- **Rationale**: Visual analysis: "WEAK OPENER. Open ocean with zero visual interest is a poor hook." Viral research ranks "rapid dive through narrow space" and "fast pull-back reveal" as top hook patterns.

### CF-3. Single Clip Runs 7+ Seconds (23% of Reel)
- **What**: The ocean surface clip occupies approximately 0-7 seconds, which is 23% of the entire 30-second reel on a single low-interest subject. Viral drone reels use 1-3 second clips with 8-12 distinct scenes in 30 seconds.
- **Where**: `src/drone_reel/core/duration_adjuster.py` -- `DurationAdjuster` class manages clip durations. The `DurationConfig.max_clip_duration` may not be enforced strictly enough. Also `src/drone_reel/cli.py` where clips are generated from scenes -- the max clip duration setting needs to account for scene interest level (low-interest scenes should be shorter).
- **Impact**: 9/10 -- Visual analysis: "5 seconds of nearly identical ocean surface is far too long." Viral research: "TikTok: Faster cuts, ~1-3 seconds per clip."
- **Complexity**: M -- Implement interest-adaptive clip duration: high-hook scenes can run 3-4s, medium scenes 2-3s, low scenes 1.5-2s max. Requires changes to DurationAdjuster to accept hook_tier per scene and vary max duration accordingly.
- **Rationale**: 3 distinct scenes in 30 seconds vs the 8-12 recommended means the DiversitySelector and DurationAdjuster are both allowing too-long, too-few clips.

### CF-4. Excessive Bitrate and File Size
- **What**: Output is encoded at ~80 Mbps (294 MB for 30s). Instagram re-encodes at ~3.5 Mbps, TikTok at similar. The 80 Mbps encode wastes storage, bandwidth, and encode time. At this rate, a 60s video (~588 MB) would exceed TikTok's 287 MB upload limit.
- **Where**: `src/drone_reel/core/video_processor.py` -- `VideoProcessor.__init__` defaults `video_bitrate` to `"15M"`, which is reasonable. But when the CLI uses `return_clip=True` and calls `write_videofile` directly at `cli.py:915-925`, it passes `bitrate=video_bitrate` which may use the h264_videotoolbox encoder that ignores bitrate constraints. The `_detect_best_encoder()` method selects VideoToolbox on macOS, which has limited rate control.
- **Impact**: 8/10 -- Technical analysis: "10-20x higher than platform delivery bitrate. Wastes storage/bandwidth. Platforms will re-encode aggressively, potentially introducing double-compression artifacts."
- **Complexity**: M -- (1) Add `-maxrate` and `-bufsize` FFmpeg params alongside `-b:v` to enforce bitrate ceiling; (2) Add `--export` flag that applies platform-specific encoding from `export_presets.py` (already implemented but not wired to CLI rendering); (3) Consider falling back to `libx264` when rate control is critical.
- **Rationale**: The export_presets module already defines correct bitrates per platform (Instagram: 8M, TikTok: 10M, YouTube Shorts: 12M) but they are not applied during the actual encode step.

---

## Quick Wins (High Impact, Small/Medium Effort)

### QW-1. Add Color Space Metadata Tags
- **What**: Output videos lack `color_primaries`, `transfer_characteristics`, and `matrix_coefficients` metadata. Platforms may interpret colors as BT.601 (SD) instead of BT.709 (HD/4K), causing subtle color shifts.
- **Where**: `src/drone_reel/core/video_processor.py` -- `stitch_clips()` method at line 477 where `ffmpeg_params` is set. Add `["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]` to the existing `["-pix_fmt", "yuv420p"]`. Same for `cli.py:924` where the fallback `write_videofile` call happens.
- **Impact**: 7/10 -- Ensures consistent color rendering across devices and platforms.
- **Complexity**: S -- Adding 6 strings to two `ffmpeg_params` lists.
- **Rationale**: Technical analysis: "Missing color_primaries, transfer_characteristics, and matrix_coefficients metadata."

### QW-2. Boost Color Grade Intensity for Social Media
- **What**: Color grading is too subtle for social media. The sunset sky (15s) needs more saturated pinks/purples; ocean blues could be deeper. Social media videos compete against heavily-graded content in feeds.
- **Where**: `src/drone_reel/core/color_grader.py` -- All preset adjustment values. The `--color-intensity` flag (Phase 7) controls a 0.0-1.0 scale factor. The default or viral preset should use 0.6-0.7 intensity, not lower. Also consider adding a shadow-lift operation in `ColorGrader.grade_frame_cpu()` for scenes with high dynamic range.
- **Impact**: 7/10 -- Visual analysis: "Color grading is too subtle for social media. The sunset sky at 15s should have more saturated pinks/purples."
- **Complexity**: S -- Adjust default `--color-intensity` to 0.6 when a platform is selected, and add a shadow-lift step (~10-15 units) in the LAB processing path for frames with mean luminance below 80.
- **Rationale**: Viral research: "Instagram/TikTok: Slightly more saturated than cinema (screen brightness, thumb-stopping color)." Visual analysis scored color at 5/10.

### QW-3. Increase Minimum Scene Count for Diversity
- **What**: Only 3 distinct scenes in 30 seconds is monotonous. The DiversitySelector should enforce a minimum scene count based on duration (e.g., min 6 scenes for 30s, min 10 for 60s).
- **Where**: `src/drone_reel/core/sequence_optimizer.py` -- `DiversitySelector` class. Add a minimum scene count parameter that scales with target duration. Also `src/drone_reel/core/duration_adjuster.py` -- `DurationConfig` should set lower max_clip_duration to force more clips.
- **Impact**: 8/10 -- Visual analysis: "3 distinct scenes in 30s is insufficient. Viral drone reels typically show 8-12 distinct locations/angles in 30 seconds."
- **Complexity**: M -- Need to adjust clip count targets and max_clip_duration calculations. For a 30s reel: target 8-10 clips at 2.5-3.5s each. For 15s: target 5-7 clips at 2-2.5s each.
- **Rationale**: Viral research: "TikTok: Faster cuts, ~1-3 seconds per clip, high energy throughout."

### QW-4. Implement Narrative Energy Arc
- **What**: The reel has an inverted energy curve -- starts slow and builds to best content. Viral reels follow a Hook -> Build -> Climax -> Resolution arc. The SceneSequencer needs to enforce this structure.
- **Where**: `src/drone_reel/core/scene_sequencer.py` -- `SceneSequencer.sequence()` method. Implement 4-section structure: Hook (0-15%: highest-energy scene), Build (15-50%: rising energy with beat-matched cuts), Climax (50-85%: fastest cuts, most dramatic content), Resolution (85-100%: wide/epic closing shot).
- **Impact**: 8/10 -- Visual analysis: "The reel has an inverted energy curve. A viral reel should open strong, maintain energy, and close with a memorable moment."
- **Complexity**: M -- The NarrativeSequencer module (`src/drone_reel/core/narrative.py`) already has arc patterns defined but is not integrated into the main pipeline. Wire it into SceneSequencer or replace the sequencing logic.
- **Rationale**: Viral research: "Hook section (0-5s): 1-2 cuts. Build section (5-15s): Cuts every 1.5-3s. Climax/Drop (15-25s): Fastest cuts. Resolution (25-30s): Slower cuts, land on wide/epic shot."

### QW-5. Wire Export Presets to Encoding Pipeline
- **What**: The `export_presets.py` module defines correct platform-specific encoding settings (resolution, bitrate, codec) but they are only partially applied. When a `--platform` is set, the output should automatically use the platform's encoding preset for the final render.
- **Where**: `src/drone_reel/cli.py` -- around lines 700-710 where `processor_kwargs` is built, the platform preset's `video_bitrate` is applied. But the resolution, codec, and additional FFmpeg params from the preset are not applied to the final encode. `src/drone_reel/core/video_processor.py` -- `stitch_clips()` and the manual `write_videofile` fallback need to receive and apply the full preset.
- **Impact**: 7/10 -- Ensures correct output specs per platform without manual bitrate/resolution flags.
- **Complexity**: M -- Thread the full ExportPreset object through to the encoding step. Apply `resolution` for output scaling, `video_bitrate` and `audio_bitrate` for rate control, and add platform-specific FFmpeg params (e.g., `-maxrate`, `-bufsize`).
- **Rationale**: Technical analysis: "A 15-25 Mbps encode for 4K or 8-12 Mbps for 1080p would be optimal." The presets already define this but aren't fully applied.

### QW-6. Add faststart Flag for Streaming Compatibility
- **What**: MP4 files should have the moov atom at the beginning for progressive download/streaming. Without `-movflags +faststart`, platforms must download the entire file before playback begins.
- **Where**: `src/drone_reel/core/video_processor.py` -- `stitch_clips()` at the `ffmpeg_params` list (line 477). Add `"-movflags", "+faststart"`. Same for `cli.py:924`.
- **Impact**: 7/10 -- Streaming compatibility and faster preview on upload.
- **Complexity**: S -- Two additional strings in FFmpeg params.
- **Rationale**: Technical analysis recommendation: "Ensure `-movflags +faststart` for progressive download/streaming compatibility."

---

## Major Upgrades (High Impact, Larger Effort)

### MU-1. Interest-Adaptive Clip Duration System
- **What**: Replace the current uniform max_clip_duration with a system that varies clip length based on scene interest, hook_tier, and position in the reel. High-interest scenes get 3-4s; low-interest scenes get 1.5-2s; hook position gets 2-3s max (fast, punchy opener). The total clip count should target 8-12 for a 30s reel.
- **Where**: `src/drone_reel/core/duration_adjuster.py` -- `DurationAdjuster` class needs a new method that accepts per-scene hook_tier and computes adaptive durations. `src/drone_reel/core/scene_sequencer.py` -- duration assignments should be coordinated with sequence position (opener shorter, climax fastest, resolution can be longer).
- **Impact**: 9/10 -- This single change would address the 3-scenes-in-30s problem, the 7s-ocean-clip problem, and the flat pacing problem simultaneously.
- **Complexity**: L -- Requires coordinating DurationAdjuster, SceneSequencer, and DiversitySelector to work together on a unified clip plan.
- **Rationale**: Visual analysis showed 3 clips averaging 10s each. Viral benchmark shows 8-12 clips at 1-3s each.

### MU-2. Speed Ramp Integration with Beat Drop Detection
- **What**: Detect beat drops in the audio and insert speed ramps (1.5x acceleration into drop, 0.3-0.5x slow-mo on drop) at those points. The `--speed-ramp` flag (Phase 7) enables basic speed ramping, but it needs beat-drop-aware placement.
- **Where**: `src/drone_reel/core/beat_sync.py` -- Add `detect_beat_drops()` method that identifies energy spikes in the audio. `src/drone_reel/core/speed_ramper.py` -- Already has `auto_detect_ramp_points()` but needs a mode that takes beat drop timestamps as input. `src/drone_reel/cli.py` -- Wire drop-detection into the speed ramp pipeline.
- **Impact**: 8/10 -- Viral research: "Speed ramping is one of the TOP trending effects for drone content in 2025."
- **Complexity**: L -- Beat drop detection requires librosa onset strength analysis; speed ramp placement must coordinate with clip boundaries and transitions.
- **Rationale**: Viral research: "Standard pattern: Normal speed -> rapid acceleration -> slow-motion peak -> resume normal." This is the #1 trending drone editing effect.

### MU-3. Smart Transition Selection Based on Scene Content
- **What**: Replace random/energy-based transition selection with content-aware transitions. Match-cut detection (same sky color between clips -> seamless sky match), motion-direction-matched cuts (pan right -> slide right transition), orbit continuity cuts (same subject, different angle).
- **Where**: `src/drone_reel/core/video_processor.py` -- `select_motion_matched_transition()` already exists but is basic. Enhance it with sky-color matching (compare top-third average color between adjacent clips), motion direction continuity, and scene type awareness. `src/drone_reel/core/sequence_optimizer.py` -- `MotionContinuityEngine` is exported but never used; wire it in.
- **Impact**: 7/10 -- Viral research: "Speed ramp + zoom" and "seamless sky match" are top trending transitions. Generic crossfades are declining.
- **Complexity**: L -- Requires frame analysis at clip boundaries, color histogram comparison, and motion vector extraction for adjacent clips.
- **Rationale**: Visual analysis: "Scene changes appear to use hard cuts. For a drone reel, smooth crossfades or zoom transitions between drastically different scenes would feel more polished." Transitions scored 4/10.

### MU-4. Shadow Recovery / Dynamic Range Correction
- **What**: Automatically lift shadows in scenes with high dynamic range (bright sky, dark foreground). The mountain shots at 15-20s had underexposed foreground vegetation against a properly-exposed sunset sky.
- **Where**: `src/drone_reel/core/color_grader.py` -- Add a `_auto_dynamic_range()` method that analyzes the luminance histogram and applies selective shadow lifting when the bottom 30% of the histogram is underrepresented. Apply before color grading presets.
- **Impact**: 7/10 -- Prevents content from looking dark/amateur on bright phone screens.
- **Complexity**: L -- Requires per-frame luminance histogram analysis and adaptive shadow curve application without clipping highlights. Must avoid flattening intentionally moody scenes.
- **Rationale**: Visual analysis: "Foreground vegetation is noticeably dark/underexposed. The color grader should lift shadows in scenes with this kind of dynamic range challenge." Viral research: "Dark/underexposed clips will be filtered out by algorithm (perceived low quality)."

### MU-5. Platform-Specific Rendering Pipeline
- **What**: When `--platform` is set, automatically configure the entire pipeline: resolution, bitrate, codec, duration targets, clip pacing, color intensity, and encoding flags. Currently `--platform` only sets aspect ratio and partially applies bitrate.
- **Where**: `src/drone_reel/cli.py` -- After platform selection, thread the full `ExportPreset` through every pipeline stage. `src/drone_reel/core/export_presets.py` -- Add `pacing_profile` (cuts_per_30s, max_clip_duration) and `color_intensity` to `ExportPreset`. `src/drone_reel/core/video_processor.py` -- Accept full preset for encoding.
- **Impact**: 8/10 -- One-flag-optimal output instead of requiring users to set 5+ flags manually.
- **Complexity**: L -- Touches every stage of the pipeline; requires careful coordination.
- **Rationale**: Viral research shows different optimal specs per platform (TikTok: 15-25s, fast cuts; Instagram: 60-90s, mixed pacing; YouTube Shorts: 30-60s). Each platform needs its own pacing and encoding profile.

---

## Nice-to-Have (Lower Priority)

### NH-1. Enable B-Frames for Better Compression
- **What**: Current h264_videotoolbox encoder produces I/P-only streams. Adding B-frames would reduce file size by 10-20% at equivalent quality.
- **Where**: `src/drone_reel/core/video_processor.py` -- `_detect_best_encoder()` and `stitch_clips()`. Add option to fall back to `libx264` with `-bf 3` when file size matters more than encode speed.
- **Impact**: 5/10 -- Primarily a storage/upload optimization.
- **Complexity**: S -- Add FFmpeg param `-bf 3` when using libx264.
- **Rationale**: Technical analysis: "Adding B-frames could reduce file size by 10-20% at equivalent quality."

### NH-2. 60fps Option for Action/FPV Content
- **What**: Add `--fps 60` option for smoother motion perception on action-heavy drone footage. Currently fixed at 30fps.
- **Where**: `src/drone_reel/core/video_processor.py` -- `__init__` parameter. `src/drone_reel/cli.py` -- Add `--fps` CLI option.
- **Impact**: 5/10 -- YouTube Shorts research notes "60fps adds perceived quality for drone footage."
- **Complexity**: S -- Parameter threading only.
- **Rationale**: Technical analysis and viral research both mention 60fps as a quality signal for action content.

### NH-3. 2-Pass VBR Encoding
- **What**: Switch from single-pass to 2-pass VBR encoding for more consistent quality across the reel.
- **Where**: `src/drone_reel/core/video_processor.py` -- `stitch_clips()`. Requires running FFmpeg twice with `-pass 1` and `-pass 2`.
- **Impact**: 4/10 -- Quality improvement is marginal at reasonable bitrates; doubles encode time.
- **Complexity**: M -- MoviePy's `write_videofile` doesn't natively support 2-pass. Would need custom FFmpeg invocation.
- **Rationale**: Technical analysis: "VBR 2-pass would smooth bitrate distribution and improve quality consistency."

### NH-4. HEVC/H.265 Output Option
- **What**: Add HEVC encoding option for 30-50% better compression at equivalent quality. Supported on TikTok and YouTube.
- **Where**: `src/drone_reel/core/video_processor.py` -- `_detect_best_encoder()` and codec selection. `src/drone_reel/cli.py` -- Add `--codec hevc` option.
- **Impact**: 4/10 -- Better compression but not universally supported; H.264 remains safest default.
- **Complexity**: S -- Encoder detection already exists; add HEVC variant.
- **Rationale**: Technical analysis: "HEVC provides 30-50% better compression at equivalent quality."

### NH-5. Ambient Sound Design Layer
- **What**: Mix subtle environmental audio (wind, waves) below the music track for added production value.
- **Where**: New functionality in `src/drone_reel/core/beat_sync.py` or a new `audio_designer.py` module. Extract ambient audio from source drone clips, reduce volume to -20dB, mix under music.
- **Impact**: 5/10 -- Adds polish but not a virality driver.
- **Complexity**: L -- Audio extraction, noise profiling, volume balancing, mixing.
- **Rationale**: Viral research: "Sound design investment (not just music, but environmental audio layers)" is a rising trend.

### NH-6. Smart Reframe Subject Tracking for Mountain Peaks
- **What**: The 9:16 reframe appears to use center-crop. For compositions with an off-center focal point (mountain peak at rule-of-thirds), SMART reframing should track the focal point.
- **Where**: `src/drone_reel/core/reframer.py` -- SMART mode saliency detection. `src/drone_reel/core/reframe_selector.py` -- Improve per-clip mode selection to detect off-center compositions.
- **Impact**: 6/10 -- Better framing on specific shots, not universal.
- **Complexity**: M -- Saliency detection already exists in SMART mode; may need tuning for landscape focal points vs human subjects.
- **Rationale**: Visual analysis: "The mountain peak at 15-20s would benefit from SMART reframing that tracks the peak as the focal point rather than dead-center."

### NH-7. Closing Shot Optimization
- **What**: Ensure the last clip is a memorable, wide/epic shot. Currently no special handling for the final position.
- **Where**: `src/drone_reel/core/scene_sequencer.py` -- Add closing shot constraint in `sequence()` method. Prefer wide landscape/reveal shots for the final position.
- **Impact**: 6/10 -- A strong closer encourages rewatches and shares.
- **Complexity**: S -- Add a constraint that the last position prefers scenes with high composition scores and wide framing.
- **Rationale**: Viral research: "Resolution (25-30s): Slower cuts, 2-4s each, land on wide/epic shot."

---

## Scoring Summary

### Methodology
Scores are weighted across 10 categories from the visual analysis framework, calibrated against viral research benchmarks.

| Category | Weight | Current Score | After Critical Fixes | After Quick Wins | After Major Upgrades |
|----------|--------|--------------|---------------------|-----------------|---------------------|
| Opening Hook | 15% | 2/10 | 7/10 | 8/10 | 9/10 |
| Scene Variety | 12% | 4/10 | 4/10 | 7/10 | 9/10 |
| Pacing/Energy | 12% | 3/10 | 4/10 | 7/10 | 9/10 |
| Composition Quality | 10% | 6/10 | 6/10 | 6/10 | 7/10 |
| Color Grading | 10% | 5/10 | 5/10 | 7/10 | 8/10 |
| Exposure/DR | 8% | 5/10 | 5/10 | 6/10 | 8/10 |
| Sharpness/Detail | 5% | 8/10 | 8/10 | 8/10 | 8/10 |
| Stabilization | 5% | 8/10 | 8/10 | 8/10 | 8/10 |
| Transitions | 8% | 4/10 | 4/10 | 5/10 | 8/10 |
| Audio/Platform Fit | 10% | 1/10 | 7/10 | 8/10 | 9/10 |
| Subject Interest | 5% | 5/10 | 6/10 | 7/10 | 7/10 |

### Overall Viral Readiness Scores

| Stage | Score | Rating |
|-------|-------|--------|
| **Current** | **38/100** | Not viable for social media |
| **After Critical Fixes (CF-1 through CF-4)** | **55/100** | Functional but below average |
| **After Quick Wins (QW-1 through QW-6)** | **70/100** | Competitive for casual posting |
| **After Major Upgrades (MU-1 through MU-5)** | **84/100** | Strong viral potential with good source footage |

### Implementation Priority Order

**Immediate (Day 1-2):**
1. CF-1: Fix missing audio (S) -- Highest impact per effort
2. QW-1: Add color space metadata (S) -- Trivial fix
3. QW-6: Add faststart flag (S) -- Trivial fix
4. CF-4: Fix excessive bitrate / wire export presets (M)

**Week 1:**
5. CF-2: Fix opening hook selection (M)
6. CF-3: Enforce max clip duration per interest level (M)
7. QW-2: Boost color grade intensity (S)
8. QW-3: Increase minimum scene count (M)

**Week 2:**
9. QW-4: Implement narrative energy arc (M)
10. QW-5: Wire full export presets to encoding (M)
11. MU-1: Interest-adaptive clip duration system (L)

**Week 3-4:**
12. MU-2: Speed ramp + beat drop integration (L)
13. MU-3: Smart transition selection (L)
14. MU-4: Shadow recovery / dynamic range (L)
15. MU-5: Platform-specific rendering pipeline (L)

---

## Key Files Reference

| File | Primary Role | Enhancement Touches |
|------|-------------|-------------------|
| `src/drone_reel/cli.py` | CLI orchestration, manual write_videofile | CF-1, CF-4, QW-1, QW-5, QW-6 |
| `src/drone_reel/core/video_processor.py` | Clip extraction, encoding, transitions | CF-1, CF-4, QW-1, QW-5, QW-6, MU-3, NH-1 |
| `src/drone_reel/core/scene_sequencer.py` | Hook ordering, sequence structure | CF-2, QW-4, MU-1, NH-7 |
| `src/drone_reel/core/duration_adjuster.py` | Clip duration management | CF-3, QW-3, MU-1 |
| `src/drone_reel/core/color_grader.py` | Color grading pipeline | QW-2, MU-4 |
| `src/drone_reel/core/sequence_optimizer.py` | Diversity selection, motion continuity | QW-3, MU-3 |
| `src/drone_reel/core/export_presets.py` | Platform encoding settings | CF-4, QW-5, MU-5 |
| `src/drone_reel/core/beat_sync.py` | Audio analysis, beat detection | MU-2 |
| `src/drone_reel/core/speed_ramper.py` | Variable speed effects | MU-2 |
| `src/drone_reel/core/reframer.py` | Landscape-to-portrait conversion | NH-6 |
| `src/drone_reel/core/narrative.py` | Narrative arc patterns (unused) | QW-4 |

---

## Appendix: What's Already Working Well

These aspects are at or near viral-quality levels and should not be regressed:

- **4K resolution with clean detail** (8/10 sharpness)
- **Adaptive stabilization** (8/10, correct decision to make this default)
- **H.264 High Profile** (universal platform compatibility)
- **Constant 30fps** (no dropped frames, correct for social)
- **9:16 portrait aspect** (correct for all short-form platforms)
- **Scene detection pipeline** (reliably identifies boundaries)
- **Hook potential scoring** (data-driven after Phase 5 fix)
- **Beat sync engine** (solid tempo detection, downbeat mode)
- **Progressive filter relaxation** (Phase 1 fix prevents empty scene lists)
- **Test suite** (951 tests, 76% coverage provides safety net)
