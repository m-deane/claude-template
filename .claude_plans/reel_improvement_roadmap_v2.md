# Instagram Reel Improvement Roadmap v2

## Current State Analysis

After reviewing the generated `instagram_reel.mp4`:

### What's Working
- Hook scene selection (boat with wake = motion + action)
- Scene diversity (ocean, mountains, sunset)
- Correct output format (1080x1920, 30fps)
- Duration within optimal range (22.9s)

### Critical Problems

#### 1. Black Letterbox Bars (40% frame waste)
**Problem**: Source footage is 16:9, output is 9:16, resulting in massive black bars
**Solution**: Use smart reframing with saliency detection

```python
# Current: Simple scale + pad (bad)
scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920

# Needed: Smart crop to subject
reframer.reframe(clip, target_ratio=(9, 16), mode='saliency')
```

#### 2. No Transitions (jarring cuts)
**Problem**: Hard cuts between clips feel amateur
**Solution**: Apply beat-synced transitions

```python
TRANSITIONS_TO_IMPLEMENT = {
    'cross_dissolve': 0.5,      # Smooth blend for calm scenes
    'fade_through_black': 0.3,   # For major scene changes
    'whip_pan': 0.2,             # For high-energy moments
    'zoom_blur': 0.3,            # For reveals
    'match_cut': 0.0,            # For similar motion directions
}
```

#### 3. No Color Grading
**Problem**: Raw footage lacks cinematic look
**Solution**: Apply teal-orange or drone-aerial preset

```python
from drone_reel.core.color_grader import ColorGrader
grader = ColorGrader()
clip = grader.apply_preset(clip, 'teal_orange')  # or 'drone_aerial'
```

#### 4. No Audio
**Problem**: Silent reels get 80% less engagement
**Solution**: Add music with beat detection

```python
from drone_reel.core.beat_sync import BeatSynchronizer
sync = BeatSynchronizer()
beat_info = sync.analyze(music_path)
# Sync cuts to beats
```

#### 5. Speed Ramping Not Applied
**Problem**: Missing cinematic slow-mo moments
**Solution**: Apply auto-detected ramps

```python
from drone_reel.core.speed_ramper import SpeedRamper
ramper = SpeedRamper()
ramps = ramper.auto_detect_ramp_points(scene)
clip = ramper.apply_multiple_ramps(clip, ramps)
```

#### 6. No Text Overlays
**Problem**: Missing location tags, captions
**Solution**: Add animated text

```python
from drone_reel.core.text_overlay import TextRenderer, TextOverlay
renderer = TextRenderer()
overlay = TextOverlay(
    text="Sardinia, Italy",
    position=(0.5, 0.85),
    animation='slide_up',
    duration=3.0
)
```

---

## Implementation Priority

### Phase 1: Critical Visual Fixes (Immediate)

#### 1.1 Smart Vertical Reframing
Replace letterbox with intelligent cropping:

```python
def reframe_for_vertical(clip_path, scene):
    """Reframe 16:9 to 9:16 with saliency detection."""
    from drone_reel.core.reframer import Reframer

    reframer = Reframer()
    clip = VideoFileClip(str(clip_path))

    # Detect points of interest (boats, horizon, landmarks)
    reframed = reframer.reframe(
        clip,
        target_ratio=(9, 16),
        mode='saliency',
        horizon_lock=True,
        smooth_motion=True
    )
    return reframed
```

**Expected Impact**: +50% visual quality, full frame utilization

#### 1.2 Transitions Between Clips
Add smooth transitions:

```python
def add_transitions(clips, beat_times=None):
    """Add transitions between clips, synced to beats if available."""
    from moviepy import concatenate_videoclips, CompositeVideoClip

    final_clips = []
    for i, clip in enumerate(clips):
        final_clips.append(clip)

        if i < len(clips) - 1:
            # Add cross-dissolve transition
            transition_duration = 0.5
            # Overlap clips for smooth transition
            clip.crossfadeout(transition_duration)
            clips[i+1].crossfadein(transition_duration)

    return concatenate_videoclips(final_clips, method='compose')
```

**Expected Impact**: +30% professional feel

### Phase 2: Cinematic Enhancement

#### 2.1 Color Grading Pipeline
```python
def apply_cinematic_grade(clip, preset='teal_orange'):
    """Apply cinematic color grading."""
    from drone_reel.core.color_grader import ColorGrader

    grader = ColorGrader()

    # Apply preset
    graded = grader.apply_preset(clip, preset)

    # Additional adjustments
    graded = grader.adjust_exposure(graded, exposure=0.1)
    graded = grader.adjust_contrast(graded, contrast=1.1)
    graded = grader.adjust_saturation(graded, saturation=1.15)

    return graded
```

#### 2.2 Speed Ramping Integration
```python
def add_speed_ramps(clip, scene_info, beat_info=None):
    """Add cinematic speed ramps."""
    from drone_reel.core.speed_ramper import SpeedRamper

    ramper = SpeedRamper()

    # Auto-detect good moments for slow-mo
    ramps = ramper.auto_detect_ramp_points(scene_info, beat_info)

    if ramps:
        clip = ramper.apply_multiple_ramps(clip, ramps)

    return clip
```

### Phase 3: Audio Integration

#### 3.1 Music + Beat Sync
```python
def add_music_and_sync(video_path, music_path, output_path):
    """Add music and sync cuts to beats."""
    from drone_reel.core.beat_sync import BeatSynchronizer

    sync = BeatSynchronizer()
    beat_info = sync.analyze(music_path)

    # Get optimal cut points
    cut_points = sync.get_cut_points(
        beat_info,
        video_duration=video.duration,
        cuts_per_bar=1
    )

    # Mix audio
    video = VideoFileClip(str(video_path))
    audio = AudioFileClip(str(music_path))

    # Fade in/out
    audio = audio.audio_fadein(0.5).audio_fadeout(1.0)

    # Set audio
    final = video.set_audio(audio.subclip(0, video.duration))

    return final
```

### Phase 4: Text & Branding

#### 4.1 Location Overlays
```python
def add_location_text(clip, location="Sardinia, Italy"):
    """Add animated location text."""
    from drone_reel.core.text_overlay import TextRenderer, TextOverlay

    renderer = TextRenderer()

    overlay = TextOverlay(
        text=location,
        position=(0.5, 0.85),  # Lower third
        font='Montserrat-Bold',
        size=48,
        color='#FFFFFF',
        shadow=True,
        animation='slide_up',
        start_time=1.0,
        duration=3.0
    )

    return renderer.render(clip, overlay)
```

#### 4.2 Call-to-Action
```python
def add_cta(clip, text="Follow for more"):
    """Add end-screen CTA."""
    overlay = TextOverlay(
        text=text,
        position=(0.5, 0.5),
        animation='pop',
        start_time=clip.duration - 3.0,
        duration=2.5
    )
    return renderer.render(clip, overlay)
```

---

## Enhanced Reel Creation Pipeline

```python
def create_instagram_reel_v2(
    video_dir: Path,
    music_path: Optional[Path] = None,
    output_path: Path = Path('output/instagram_reel_v2.mp4'),
    location_text: Optional[str] = None,
):
    """
    Create Instagram-worthy reel with all enhancements.

    Pipeline:
    1. Scene detection with enhanced metadata
    2. Diversity-aware selection
    3. Hook optimization
    4. Narrative sequencing
    5. Smart vertical reframing (no letterbox)
    6. Color grading
    7. Speed ramping
    8. Transitions
    9. Music + beat sync
    10. Text overlays
    11. Export with platform preset
    """

    # 1. Detect scenes
    detector = SceneDetector()
    scenes = []
    for video in find_video_files(video_dir):
        scenes.extend(detector.detect_scenes_enhanced(video))

    # 2. Diversity selection
    selector = DiversitySelector()
    selected = selector.select(scenes, count=8)

    # 3. Hook optimization
    hook_gen = HookGenerator()
    best_hook = hook_gen.select_hook_scene(selected)

    # 4. Narrative sequencing
    sequencer = NarrativeSequencer()
    sequenced = [best_hook] + sequencer.sequence(
        [s for s in selected if s != best_hook],
        target_duration=27.0
    )

    # 5. Motion continuity
    engine = MotionContinuityEngine()
    optimized = engine.optimize_sequence(sequenced)

    # 6-10. Process each clip
    processed_clips = []
    reframer = Reframer()
    grader = ColorGrader()
    ramper = SpeedRamper()

    for scene in optimized:
        clip = VideoFileClip(str(scene.source_file))
        clip = clip.subclip(scene.start_time, scene.end_time)

        # Smart reframe (no letterbox)
        clip = reframer.reframe(clip, (9, 16), mode='saliency')

        # Color grade
        clip = grader.apply_preset(clip, 'teal_orange')

        # Speed ramp
        ramps = ramper.auto_detect_ramp_points(scene)
        if ramps:
            clip = ramper.apply_multiple_ramps(clip, ramps)

        processed_clips.append(clip)

    # 11. Concatenate with transitions
    final = concatenate_with_transitions(processed_clips)

    # 12. Add music if provided
    if music_path:
        final = add_music_and_sync(final, music_path)

    # 13. Add text overlays
    if location_text:
        final = add_location_text(final, location_text)

    # 14. Export
    exporter = PlatformExporter()
    params = exporter.get_export_params(Platform.INSTAGRAM_REELS)
    final.write_videofile(str(output_path), **params)

    return output_path
```

---

## Quick Wins (Implement Now)

### 1. Fix Letterboxing with Center Crop
```bash
# FFmpeg center crop instead of letterbox
-vf "scale=-1:1920,crop=1080:1920"
```

### 2. Add Cross-Dissolve Transitions
```bash
# FFmpeg xfade filter between clips
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "xfade=transition=fade:duration=0.5:offset=4.5"
```

### 3. Apply LUT Color Grade
```bash
# FFmpeg LUT application
-vf "lut3d=cinematic.cube"
```

---

## Success Metrics

| Metric | Current | Target | Method |
|--------|---------|--------|--------|
| Frame utilization | 60% | 100% | Smart reframing |
| Transition quality | None | Smooth | Cross-dissolves |
| Color grade | Raw | Cinematic | Teal-orange preset |
| Audio | None | Beat-synced | Music integration |
| Text overlays | None | Location + CTA | Text system |
| Speed variation | None | Dynamic | Auto-ramps |

---

## Next Steps

1. **Immediate**: Implement center-crop reframing to eliminate letterbox
2. **Short-term**: Add transition system between clips
3. **Medium-term**: Integrate color grading into pipeline
4. **Long-term**: Full music + beat sync integration

The goal is to transform from "technically correct" to "Instagram viral-worthy".
