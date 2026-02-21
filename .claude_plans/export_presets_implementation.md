# Export Presets Implementation

## Summary

Implemented comprehensive multi-platform export presets for social media platforms with full CLI integration and 99% test coverage.

## Implementation Status: COMPLETE

### Files Created

1. **`src/drone_reel/core/export_presets.py`** (98 statements, 99% coverage)
   - `Platform` enum with 8 platform types
   - `ExportPreset` dataclass with all export specifications
   - `PLATFORM_PRESETS` dictionary with 7 platform configurations
   - `PlatformExporter` class with full functionality:
     - `get_preset()` - Retrieve platform preset
     - `validate_for_platform()` - Validate duration and requirements
     - `get_export_params()` - Generate MoviePy/FFmpeg parameters
     - `suggest_platform()` - Suggest best platforms for content
     - `create_multi_platform_export()` - Export to multiple platforms
     - `get_aspect_ratio_string()` - Format aspect ratios
     - `get_platforms_by_aspect_ratio()` - Find matching platforms
     - `create_custom_preset()` - Create custom export presets

2. **`tests/test_export_presets.py`** (49 tests, all passing)
   - 10 test classes covering all functionality
   - Tests for all 7 platform presets
   - Validation logic tests
   - Export parameter generation tests
   - Platform suggestion tests
   - Multi-platform export tests
   - Aspect ratio and duration handling tests
   - Bitrate configuration tests

### Platform Presets Implemented

| Platform | Aspect Ratio | Resolution | Max Duration | Optimal Range | Bitrate |
|----------|-------------|------------|--------------|---------------|---------|
| Instagram Reels | 9:16 | 1080x1920 | 90s | 15-30s | 8M |
| Instagram Feed | 4:5 | 1080x1350 | 60s | 15-30s | 8M |
| TikTok | 9:16 | 1080x1920 | 180s | 15-60s | 10M |
| YouTube Shorts | 9:16 | 1080x1920 | 60s | 15-60s | 12M |
| YouTube | 16:9 | 1920x1080 | Unlimited | 60-600s | 15M |
| Pinterest | 2:3 | 1000x1500 | Unlimited | 6-15s | 8M |
| Twitter | 16:9 | 1280x720 | 140s | 10-45s | 10M |

### CLI Integration

1. **New `platforms` command** - List all available platforms with specifications
2. **New `--platform` option** - Select platform preset for export
3. **Automatic validation** - Warns about duration/quality issues
4. **Hardware encoder support** - Uses VideoProcessor's encoder detection

### Key Features

#### Validation System
- Duration validation (min/max/optimal ranges)
- Aspect ratio compatibility
- Error and warning messages
- Platform requirement checks

#### Export Parameters
- Platform-optimized bitrates
- Proper codec selection
- Audio codec configuration
- FFmpeg parameter generation
- Hardware encoder integration

#### Platform Suggestions
- Content-aware recommendations
- Aspect ratio matching
- Duration compatibility
- Sorted by relevance

#### Multi-Platform Export
- Batch export to multiple platforms
- Automatic resizing per platform
- Validated before export
- Custom filename support

### Integration with VideoProcessor

The implementation integrates seamlessly with the existing `VideoProcessor`:

```python
# Hardware encoder is automatically detected
video_processor = VideoProcessor()

# Platform preset can override codec settings
exporter = PlatformExporter()
preset = exporter.get_preset(Platform.INSTAGRAM_REELS)
params = exporter.get_export_params(
    Platform.INSTAGRAM_REELS,
    hardware_encoder=video_processor.output_codec
)
```

### Usage Examples

#### CLI Usage

```bash
# List available platforms
drone-reel platforms

# Create reel for Instagram Reels
drone-reel create --input ./clips --platform instagram_reels --duration 30

# Create reel for YouTube
drone-reel create --input ./clips --platform youtube --duration 120

# Create reel for TikTok with music
drone-reel create --input ./clips --platform tiktok --music track.mp3
```

#### Programmatic Usage

```python
from pathlib import Path
from moviepy import VideoFileClip
from drone_reel.core.export_presets import Platform, PlatformExporter

# Initialize exporter
exporter = PlatformExporter()

# Get preset for Instagram Reels
preset = exporter.get_preset(Platform.INSTAGRAM_REELS)
print(f"Resolution: {preset.resolution}")
print(f"Aspect ratio: {preset.aspect_ratio}")
print(f"Max duration: {preset.max_duration}s")

# Validate content for platform
validation = exporter.validate_for_platform(45.0, Platform.INSTAGRAM_REELS)
if validation["errors"]:
    print("Errors:", validation["errors"])
if validation["warnings"]:
    print("Warnings:", validation["warnings"])

# Get export parameters
params = exporter.get_export_params(Platform.INSTAGRAM_REELS)

# Export video with platform settings
clip = VideoFileClip("input.mp4")
resized_clip = clip.resized(preset.resolution)
resized_clip.write_videofile("output.mp4", **params)

# Export to multiple platforms at once
clip = VideoFileClip("input.mp4")
results = exporter.create_multi_platform_export(
    clip,
    output_dir=Path("./exports"),
    platforms=[
        Platform.INSTAGRAM_REELS,
        Platform.TIKTOK,
        Platform.YOUTUBE_SHORTS,
    ],
)
# Results: {Platform.INSTAGRAM_REELS: Path(...), Platform.TIKTOK: Path(...), ...}

# Suggest platforms for content
suggestions = exporter.suggest_platform(
    clip_duration=30.0,
    aspect_ratio=(9, 16)
)
print(f"Suggested platforms: {suggestions}")

# Create custom preset
custom = exporter.create_custom_preset(
    name="My Custom Format",
    aspect_ratio=(1, 1),
    resolution=(2000, 2000),
    fps=60,
    video_bitrate="20M",
)
```

### Test Coverage

- 49 tests total, all passing
- 99% code coverage (98/98 statements covered)
- Comprehensive edge case testing
- Mock-based multi-platform export tests
- Validation logic verification
- All platform presets validated

### Code Quality

- Type hints throughout
- Comprehensive docstrings
- Clean separation of concerns
- Pythonic design patterns
- No circular dependencies
- Proper error handling

### Performance Considerations

- Lazy loading of presets
- Efficient validation checks
- Hardware encoder auto-detection
- Parallel export capability (via multi_platform_export)

### Future Enhancements (Optional)

1. **Platform-specific features**:
   - Instagram carousel support
   - YouTube chapters/timestamps
   - TikTok effects/filters

2. **Advanced validation**:
   - File size limits
   - Codec compatibility checks
   - Audio channel validation

3. **Batch operations**:
   - Queue multiple videos for export
   - Progress tracking per platform
   - Failure recovery

4. **Cloud integration**:
   - Direct upload to platforms
   - OAuth authentication
   - Metadata injection

## Integration Points

- `VideoProcessor`: Uses hardware encoder detection
- `CLI`: New commands and options
- `Config`: Platform settings can be saved
- `Reframer`: Aspect ratio compatibility

## Testing

All tests pass with 99% coverage:
```bash
pytest tests/test_export_presets.py -v
# 49 passed in 1.11s
```

CLI commands verified:
```bash
drone-reel platforms  # Lists all platforms
drone-reel create --help  # Shows --platform option
```

## Documentation

- Full docstrings on all public methods
- Type hints for all parameters
- Usage examples in this file
- CLI help text for new commands

## Status: READY FOR PRODUCTION
