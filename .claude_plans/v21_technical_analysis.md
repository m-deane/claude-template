# V21 Technical Quality Analysis

## Overview

Technical analysis of two 30-second 4K drone reels rendered with different stabilization strategies:
- **Adaptive Stabilization** (`reel_30s_4k_adaptive_stab.mp4`) - stabilizes only shaky clips
- **Full Stabilization** (`reel_30s_4k_full_stab.mp4`) - stabilizes all clips

Analysis performed via ffprobe on 2026-02-20.

---

## 1. Stream & Container Details

| Property | Adaptive Stab | Full Stab |
|---|---|---|
| **Container** | MP4 (isom/iso2/avc1/mp41) | MP4 (isom/iso2/avc1/mp41) |
| **Video Codec** | H.264 (AVC) | H.264 (AVC) |
| **Profile / Level** | High / 5.1 | High / 5.1 |
| **Encoder** | h264_videotoolbox (HW) | h264_videotoolbox (HW) |
| **Resolution** | 2160x3840 (portrait 4K) | 2160x3840 (portrait 4K) |
| **Frame Rate** | 30 fps (constant) | 30 fps (constant) |
| **Pixel Format** | yuv420p | yuv420p |
| **Bit Depth** | 8 bits | 8 bits |
| **Color Space** | Not tagged (BT.601 assumed) | Not tagged (BT.601 assumed) |
| **Scan Type** | Progressive | Progressive |
| **B-Frames** | 0 (none) | 0 (none) |
| **Reference Frames** | 1 | 1 |
| **Duration** | 30.567s | 30.567s |
| **Total Frames** | 917 | 917 |
| **File Size** | 294 MB (307,857,135 bytes) | 294 MB (308,238,382 bytes) |
| **Audio** | **NONE** | **NONE** |

---

## 2. Bitrate Analysis

### Average Bitrate

| Metric | Adaptive Stab | Full Stab |
|---|---|---|
| **Stream bit_rate** | 80,571 kbps (~80.6 Mbps) | 80,671 kbps (~80.7 Mbps) |
| **Container bit_rate** | 80,573 kbps | 80,673 kbps |
| **Calculated avg (frame sizes)** | ~77,583 kbps | ~77,679 kbps |

### Frame Size Statistics

| Metric | Adaptive Stab | Full Stab |
|---|---|---|
| **Avg frame size** | 327.8 KB | 328.3 KB |
| **Max frame size** | 1,118.5 KB (1.09 MB) | 1,014.8 KB (0.99 MB) |
| **Max/Avg ratio** | 3.41x | 3.09x |

### Per-Second Bitrate Distribution

**Adaptive Stabilization:**
- Min: 39,731 kbps (sec 27) | Max: 97,985 kbps (sec 23) | Avg: 77,583 kbps
- Range ratio: 2.47x (max/min)
- Notable spike at seconds 21-25 (92-98 Mbps) - likely high-motion or scene-transition segments
- Drop at second 27 (40 Mbps) - possibly a static or crossfade segment

**Full Stabilization:**
- Min: 26,535 kbps (sec 27) | Max: 99,094 kbps (sec 23) | Avg: 77,679 kbps
- Range ratio: 3.73x (max/min)
- Similar spike pattern at seconds 21-25 (94-99 Mbps)
- Deeper trough at second 27 (27 Mbps) - stabilization may have smoothed motion creating lower-complexity frames

### Bitrate Assessment

Both videos are encoded at approximately **80 Mbps**, which is:
- Extremely high for social media delivery (Instagram caps re-encoding at ~3.5 Mbps for Reels)
- Appropriate as a **master/archive quality** output
- Well above YouTube's recommended 53-68 Mbps for 4K HDR uploads
- Results in ~294 MB for 30 seconds -- too large for most direct upload workflows

---

## 3. Keyframe (GOP) Analysis

| Property | Adaptive Stab | Full Stab |
|---|---|---|
| **Total keyframes** | 76 | 76 |
| **GOP size** | 12 frames (consistent) | 12 frames (consistent) |
| **GOP duration** | 0.4 seconds | 0.4 seconds |
| **Keyframe interval** | Every 12th frame | Every 12th frame |

### GOP Assessment

- **Consistent GOP**: Both videos have perfectly regular 12-frame GOP intervals with no deviations. This is imposed by the h264_videotoolbox encoder defaults.
- **0.4s keyframe interval** is excellent for seeking and streaming -- well within the 1-2 second recommendation for social platforms.
- **No B-frames**: The encoder produced I/P-only streams. This simplifies seeking but slightly reduces compression efficiency. Adding B-frames could reduce file size by 10-20% at equivalent quality.

---

## 4. Encoding Quality Assessment

### Strengths
1. **H.264 High Profile Level 5.1**: Maximum compatibility codec/profile for 4K content
2. **Hardware encoding (VideoToolbox)**: Fast encode times via Apple Silicon
3. **Constant frame rate (30 fps)**: No dropped or duplicated frames
4. **Progressive scan**: Correct for all modern platforms
5. **yuv420p pixel format**: Universal compatibility

### Issues Identified

| Issue | Severity | Detail |
|---|---|---|
| **No audio track** | CRITICAL | Both videos have zero audio streams. Social platforms expect audio; silent videos get deprioritized by algorithms and auto-play muted. Even ambient audio or a music track is essential. |
| **No color space tags** | MODERATE | Missing color_primaries, transfer_characteristics, and matrix_coefficients metadata. Platforms may interpret colors incorrectly (BT.601 vs BT.709). Should tag as BT.709 for HD/4K content. |
| **Excessive bitrate (80 Mbps)** | MODERATE | 10-20x higher than platform delivery bitrate. Wastes storage/bandwidth. Platforms will re-encode aggressively, potentially introducing double-compression artifacts. A 15-25 Mbps encode for 4K or 8-12 Mbps for 1080p would be optimal. |
| **No B-frames** | LOW | Compression efficiency could be improved 10-20% with 2-3 B-frames. The h264_videotoolbox encoder may not support B-frames; libx264 would. |
| **File size (294 MB / 30s)** | MODERATE | Most platforms have upload limits (Instagram: 650 MB/60s, TikTok: 287 MB for some accounts). At this rate, a 60s video would be ~588 MB, approaching limits. |
| **Resolution (2160x3840)** | LOW | Above most platform native resolution. Instagram/TikTok deliver at 1080x1920 max. The extra resolution provides a quality buffer for re-encoding but doubles encode time and storage. |
| **Bitrate variance (2.5-3.7x)** | LOW | VBR encoding shows noticeable bitrate swings. The second 27 dip to 27-40 Mbps may indicate quality drops in that segment, though at these overall bitrates it is unlikely to be visible. |

---

## 5. Platform Compatibility Matrix

### Recommended Upload Specifications

| Platform | Resolution | FPS | Codec | Bitrate (video) | Audio | Max Size | Max Duration |
|---|---|---|---|---|---|---|---|
| **Instagram Reels** | 1080x1920 | 30 | H.264 | 3,500+ kbps | AAC 128 kbps | 650 MB | 90s |
| **TikTok** | 1080x1920 | 30 | H.264/HEVC | 2,500+ kbps | AAC 128 kbps | 287 MB* | 10 min |
| **YouTube Shorts** | 1080x1920 | 30-60 | H.264 | 8,000+ kbps | AAC 128 kbps | 256 MB** | 60s |
| **YouTube (4K)** | 2160x3840 | 30 | H.264/VP9 | 35,000-68,000 | AAC 384 kbps | 128 GB | 12 hr |

*TikTok limits vary by account/region
**YouTube Shorts: uploaded as regular video, flagged as Short by metadata

### Current Video vs Platform Requirements

| Requirement | Adaptive Stab | Full Stab | Status |
|---|---|---|---|
| **Codec (H.264)** | H.264 High | H.264 High | PASS |
| **Container (MP4)** | MP4 | MP4 | PASS |
| **Frame Rate (30fps)** | 30 fps | 30 fps | PASS |
| **Pixel Format (yuv420p)** | yuv420p | yuv420p | PASS |
| **Progressive Scan** | Yes | Yes | PASS |
| **Portrait Aspect (9:16)** | 2160:3840 = 9:16 | 2160:3840 = 9:16 | PASS |
| **Audio Present** | NO | NO | **FAIL** |
| **Resolution <= 1080x1920** | 2160x3840 | 2160x3840 | WARN (oversized) |
| **Bitrate reasonable** | 80 Mbps | 80 Mbps | WARN (excessive) |
| **File size < 287 MB (TikTok)** | 294 MB | 294 MB | **FAIL** |
| **Color space tagged** | No | No | WARN |

---

## 6. Adaptive vs Full Stabilization Comparison

Both videos are technically near-identical in encoding parameters. Key differences:

| Metric | Adaptive | Full | Winner |
|---|---|---|---|
| **File size** | 307,857,135 B | 308,238,382 B | Adaptive (381 KB smaller) |
| **Avg bitrate** | 80,571 kbps | 80,671 kbps | Adaptive (marginally) |
| **Max frame size** | 1,118.5 KB | 1,014.8 KB | Full (lower spikes) |
| **Bitrate variance** | 2.47x | 3.73x | Adaptive (more consistent) |
| **Min bitrate** | 39,731 kbps | 26,535 kbps | Adaptive (higher floor) |

**Interpretation**: Full stabilization creates slightly smoother motion data, reducing peak frame complexity but also creating deeper troughs in low-motion segments. Adaptive stabilization preserves original motion where stable, resulting in more consistent bitrate distribution. The differences are minimal at these bitrates.

---

## 7. Recommendations for Production Pipeline

### Critical (Must Fix)
1. **Add audio track**: Wire BeatSync audio output to final render. Even a silent AAC track is better than no audio stream.
2. **Reduce output bitrate**: Target 15-20 Mbps for 4K master, or render at 1080x1920 with 8-12 Mbps for direct social upload.

### High Priority
3. **Add color space metadata**: Tag output as BT.709 (or BT.2020 for HDR). Add `-colorspace bt709 -color_primaries bt709 -color_trc bt709` to FFmpeg flags.
4. **Add export presets**: Create platform-specific encoding profiles:
   - `--export instagram`: 1080x1920, H.264, 8 Mbps, AAC audio
   - `--export youtube`: 2160x3840, H.264, 40 Mbps, AAC audio
   - `--export master`: Current quality for archival

### Medium Priority
5. **Enable B-frames**: Switch to libx264 for final encode (slower but better compression). Use `-bf 3` for ~15% bitrate savings.
6. **Add 2-pass encoding**: VBR 2-pass would smooth bitrate distribution and improve quality consistency.
7. **Add faststart flag**: Ensure `-movflags +faststart` for progressive download/streaming compatibility (may already be set).

### Low Priority
8. **Consider HEVC output**: For YouTube and TikTok, HEVC provides 30-50% better compression at equivalent quality. Not universally supported yet.
9. **Frame rate option**: Add 24fps option for cinematic look, 60fps for action/FPV footage.
10. **Render time optimization**: At 80 Mbps the encoder is working unnecessarily hard. Reducing to 15-20 Mbps would also speed up encoding significantly.

---

## 8. Summary

Both videos are technically well-formed H.264 MP4 files with correct aspect ratio, frame rate, and codec compatibility. The primary issues are:

1. **Missing audio** -- the single most impactful deficiency for social media viability
2. **Excessive bitrate/file size** -- 80 Mbps / 294 MB for a 30s clip is 10x more than needed
3. **Missing color space metadata** -- may cause subtle color shifts on different devices

The encoding pipeline uses Apple VideoToolbox hardware acceleration, which explains the lack of B-frames and high bitrate (VideoToolbox has limited rate control compared to libx264). The keyframe interval is good. The videos are functionally identical from an encoding perspective -- the stabilization mode choice should be driven by visual quality, not technical parameters.
