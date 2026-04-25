"""
Tests for multi-platform export presets.
"""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from moviepy import VideoFileClip

from drone_reel.core.export_presets import (
    PLATFORM_PRESETS,
    ExportPreset,
    Platform,
    PlatformExporter,
)


@pytest.fixture
def exporter():
    """Create PlatformExporter instance."""
    return PlatformExporter()


@pytest.fixture
def mock_video_clip():
    """Create a mock video clip."""
    clip = MagicMock(spec=VideoFileClip)
    clip.duration = 30.0
    clip.fps = 30
    clip.w = 1920
    clip.h = 1080
    clip.size = (1920, 1080)

    resized_clip = MagicMock(spec=VideoFileClip)
    resized_clip.duration = 30.0

    def mock_write_videofile(path, **kwargs):
        Path(path).touch()

    resized_clip.write_videofile = mock_write_videofile
    clip.resized.return_value = resized_clip

    return clip


class TestPlatformEnum:
    """Test Platform enum."""

    def test_all_platforms_defined(self):
        """All expected platforms should be defined."""
        expected = {
            "instagram_reels",
            "instagram_feed",
            "tiktok",
            "youtube_shorts",
            "youtube",
            "youtube_4k",
            "pinterest",
            "twitter",
            "vertical_4k",
            "custom",
        }
        actual = {p.value for p in Platform}
        assert actual == expected

    def test_platform_values_are_strings(self):
        """Platform values should be lowercase strings."""
        for platform in Platform:
            assert isinstance(platform.value, str)
            assert platform.value.islower()


class TestExportPreset:
    """Test ExportPreset dataclass."""

    def test_preset_creation(self):
        """Should create preset with all required fields."""
        preset = ExportPreset(
            name="Test Preset",
            platform=Platform.INSTAGRAM_REELS,
            aspect_ratio=(9, 16),
            resolution=(1080, 1920),
            fps=30,
            codec="h264",
            audio_codec="aac",
            video_bitrate="8M",
            audio_bitrate="128k",
            max_duration=90.0,
            optimal_duration=(15.0, 30.0),
        )

        assert preset.name == "Test Preset"
        assert preset.platform == Platform.INSTAGRAM_REELS
        assert preset.aspect_ratio == (9, 16)
        assert preset.resolution == (1080, 1920)
        assert preset.fps == 30
        assert preset.codec == "h264"
        assert preset.audio_codec == "aac"
        assert preset.video_bitrate == "8M"
        assert preset.audio_bitrate == "128k"
        assert preset.max_duration == 90.0
        assert preset.optimal_duration == (15.0, 30.0)
        assert preset.pixel_format == "yuv420p"
        assert preset.preset == "medium"


class TestPlatformPresets:
    """Test PLATFORM_PRESETS dictionary."""

    def test_instagram_reels_preset(self):
        """Instagram Reels should have correct specifications."""
        preset = PLATFORM_PRESETS[Platform.INSTAGRAM_REELS]
        assert preset.name == "Instagram Reels"
        assert preset.aspect_ratio == (9, 16)
        assert preset.resolution == (1080, 1920)
        assert preset.fps == 30
        assert preset.max_duration == 90.0
        assert preset.optimal_duration == (15.0, 30.0)

    def test_instagram_feed_preset(self):
        """Instagram Feed should have correct specifications."""
        preset = PLATFORM_PRESETS[Platform.INSTAGRAM_FEED]
        assert preset.name == "Instagram Feed"
        assert preset.aspect_ratio == (4, 5)
        assert preset.resolution == (1080, 1350)
        assert preset.max_duration == 60.0

    def test_tiktok_preset(self):
        """TikTok should have correct specifications."""
        preset = PLATFORM_PRESETS[Platform.TIKTOK]
        assert preset.name == "TikTok"
        assert preset.aspect_ratio == (9, 16)
        assert preset.resolution == (1080, 1920)
        assert preset.max_duration == 180.0
        assert preset.optimal_duration == (15.0, 60.0)

    def test_youtube_shorts_preset(self):
        """YouTube Shorts should have correct specifications."""
        preset = PLATFORM_PRESETS[Platform.YOUTUBE_SHORTS]
        assert preset.name == "YouTube Shorts"
        assert preset.aspect_ratio == (9, 16)
        assert preset.resolution == (1080, 1920)
        assert preset.max_duration == 60.0

    def test_youtube_preset(self):
        """YouTube should have correct specifications."""
        preset = PLATFORM_PRESETS[Platform.YOUTUBE]
        assert preset.name == "YouTube"
        assert preset.aspect_ratio == (16, 9)
        assert preset.resolution == (1920, 1080)
        assert preset.max_duration is None

    def test_pinterest_preset(self):
        """Pinterest should have correct specifications."""
        preset = PLATFORM_PRESETS[Platform.PINTEREST]
        assert preset.name == "Pinterest"
        assert preset.aspect_ratio == (2, 3)
        assert preset.resolution == (1000, 1500)

    def test_twitter_preset(self):
        """Twitter should have correct specifications."""
        preset = PLATFORM_PRESETS[Platform.TWITTER]
        assert preset.name == "Twitter"
        assert preset.aspect_ratio == (16, 9)
        assert preset.resolution == (1280, 720)
        assert preset.max_duration == 140.0

    def test_all_presets_have_required_fields(self):
        """All presets should have valid required fields."""
        for platform, preset in PLATFORM_PRESETS.items():
            assert isinstance(preset.name, str)
            assert preset.platform == platform
            assert len(preset.aspect_ratio) == 2
            assert len(preset.resolution) == 2
            assert preset.fps > 0
            assert isinstance(preset.codec, str)
            assert isinstance(preset.audio_codec, str)
            assert isinstance(preset.video_bitrate, str)
            assert isinstance(preset.audio_bitrate, str)
            assert len(preset.optimal_duration) == 2

    def test_all_presets_have_valid_codecs(self):
        """All presets should use valid codecs."""
        for preset in PLATFORM_PRESETS.values():
            assert preset.codec in ["h264", "h265", "libx264", "libx265"]
            assert preset.audio_codec in ["aac", "mp3"]


class TestPlatformExporterGetPreset:
    """Test PlatformExporter.get_preset method."""

    def test_get_existing_preset(self, exporter):
        """Should retrieve preset for valid platform."""
        preset = exporter.get_preset(Platform.INSTAGRAM_REELS)
        assert preset.platform == Platform.INSTAGRAM_REELS
        assert preset.name == "Instagram Reels"

    def test_get_all_presets(self, exporter):
        """Should retrieve all platform presets."""
        for platform in Platform:
            if platform == Platform.CUSTOM:
                continue
            preset = exporter.get_preset(platform)
            assert preset.platform == platform


class TestPlatformExporterValidation:
    """Test PlatformExporter.validate_for_platform method."""

    def test_validation_within_optimal_range(self, exporter):
        """Should pass validation for duration within optimal range."""
        result = exporter.validate_for_platform(20.0, Platform.INSTAGRAM_REELS)
        assert len(result["errors"]) == 0
        assert len(result["warnings"]) == 0

    def test_validation_below_optimal_range(self, exporter):
        """Should warn for duration below optimal range."""
        result = exporter.validate_for_platform(5.0, Platform.INSTAGRAM_REELS)
        assert len(result["errors"]) == 0
        assert len(result["warnings"]) == 1
        assert "shorter than optimal" in result["warnings"][0]

    def test_validation_above_optimal_range(self, exporter):
        """Should warn for duration above optimal range."""
        result = exporter.validate_for_platform(60.0, Platform.INSTAGRAM_REELS)
        assert len(result["errors"]) == 0
        assert len(result["warnings"]) == 1
        assert "exceeds optimal" in result["warnings"][0]

    def test_validation_exceeds_max_duration(self, exporter):
        """Should error for duration exceeding maximum."""
        result = exporter.validate_for_platform(100.0, Platform.INSTAGRAM_REELS)
        assert len(result["errors"]) == 1
        assert "exceeds maximum" in result["errors"][0]

    def test_validation_no_max_duration(self, exporter):
        """Should not error for platform with no max duration."""
        result = exporter.validate_for_platform(1000.0, Platform.YOUTUBE)
        assert len(result["errors"]) == 0

    def test_validation_at_max_duration(self, exporter):
        """Should pass validation at exact max duration."""
        result = exporter.validate_for_platform(90.0, Platform.INSTAGRAM_REELS)
        assert len(result["errors"]) == 0

    def test_validation_just_above_max(self, exporter):
        """Should fail validation just above max duration."""
        result = exporter.validate_for_platform(90.1, Platform.INSTAGRAM_REELS)
        assert len(result["errors"]) == 1


class TestPlatformExporterExportParams:
    """Test PlatformExporter.get_export_params method."""

    def test_export_params_default_codec(self, exporter):
        """Should return export params with default codec."""
        params = exporter.get_export_params(Platform.INSTAGRAM_REELS)

        assert params["fps"] == 30
        assert params["codec"] == "h264"
        assert params["audio_codec"] == "aac"
        assert params["preset"] == "medium"
        assert params["bitrate"] == "8M"
        assert params["audio_bitrate"] == "128k"
        assert "ffmpeg_params" in params
        assert "-pix_fmt" in params["ffmpeg_params"]

    def test_export_params_hardware_encoder(self, exporter):
        """Should use hardware encoder when specified."""
        params = exporter.get_export_params(
            Platform.INSTAGRAM_REELS, hardware_encoder="h264_videotoolbox"
        )

        assert params["codec"] == "h264_videotoolbox"

    def test_export_params_all_platforms(self, exporter):
        """Should return valid params for all platforms."""
        for platform in Platform:
            if platform == Platform.CUSTOM:
                continue

            params = exporter.get_export_params(platform)

            assert "fps" in params
            assert "codec" in params
            assert "audio_codec" in params
            assert "preset" in params
            assert "bitrate" in params
            assert "audio_bitrate" in params


class TestPlatformExporterSuggestions:
    """Test PlatformExporter.suggest_platform method."""

    def test_suggest_perfect_match(self, exporter):
        """Should suggest platform with perfect aspect ratio and duration match."""
        suggestions = exporter.suggest_platform(20.0, (9, 16))

        assert Platform.INSTAGRAM_REELS in suggestions
        assert Platform.TIKTOK in suggestions
        assert len(suggestions) > 0

    def test_suggest_aspect_ratio_mismatch(self, exporter):
        """Should suggest horizontal platforms for horizontal content."""
        suggestions = exporter.suggest_platform(20.0, (16, 9))

        horizontal_platforms = {Platform.YOUTUBE, Platform.TWITTER}

        matching_count = sum(1 for p in suggestions if p in horizontal_platforms)
        assert matching_count > 0

    def test_suggest_duration_too_long(self, exporter):
        """Should exclude platforms with exceeded max duration."""
        suggestions = exporter.suggest_platform(200.0, (9, 16))

        assert Platform.INSTAGRAM_REELS not in suggestions
        assert Platform.YOUTUBE_SHORTS not in suggestions

    def test_suggest_horizontal_content(self, exporter):
        """Should suggest horizontal platforms for 16:9 content."""
        suggestions = exporter.suggest_platform(120.0, (16, 9))

        assert Platform.YOUTUBE in suggestions
        assert Platform.TWITTER in suggestions

    def test_suggest_square_content(self, exporter):
        """Should handle content with no matching aspect ratio."""
        suggestions = exporter.suggest_platform(30.0, (1, 1))

        assert len(suggestions) >= 0


class TestPlatformExporterMultiExport:
    """Test PlatformExporter.create_multi_platform_export method."""

    def test_multi_export_single_platform(self, exporter, mock_video_clip):
        """Should export to single platform."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)

            results = exporter.create_multi_platform_export(
                mock_video_clip,
                output_dir,
                [Platform.INSTAGRAM_REELS],
            )

            assert Platform.INSTAGRAM_REELS in results
            assert results[Platform.INSTAGRAM_REELS].exists()

    def test_multi_export_multiple_platforms(self, exporter, mock_video_clip):
        """Should export to multiple platforms."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)

            platforms = [Platform.INSTAGRAM_REELS, Platform.TIKTOK]

            results = exporter.create_multi_platform_export(
                mock_video_clip, output_dir, platforms
            )

            assert len(results) == 2
            assert Platform.INSTAGRAM_REELS in results
            assert Platform.TIKTOK in results

    def test_multi_export_creates_output_dir(self, exporter, mock_video_clip):
        """Should create output directory if it doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "exports" / "social"

            assert not output_dir.exists()

            exporter.create_multi_platform_export(
                mock_video_clip,
                output_dir,
                [Platform.INSTAGRAM_REELS],
            )

            assert output_dir.exists()

    def test_multi_export_custom_filename(self, exporter, mock_video_clip):
        """Should use custom base filename."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)

            results = exporter.create_multi_platform_export(
                mock_video_clip,
                output_dir,
                [Platform.INSTAGRAM_REELS],
                base_filename="my_video",
            )

            output_path = results[Platform.INSTAGRAM_REELS]
            assert "my_video" in output_path.name

    def test_multi_export_validation_failure(self, exporter, mock_video_clip):
        """Should raise error if validation fails."""
        mock_video_clip.duration = 200.0

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)

            with pytest.raises(ValueError, match="Validation failed"):
                exporter.create_multi_platform_export(
                    mock_video_clip,
                    output_dir,
                    [Platform.INSTAGRAM_REELS],
                )

    def test_multi_export_calls_resize(self, exporter, mock_video_clip):
        """Should resize clip to platform resolution."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)

            exporter.create_multi_platform_export(
                mock_video_clip,
                output_dir,
                [Platform.INSTAGRAM_REELS],
            )

            mock_video_clip.resized.assert_called_with((1080, 1920))


class TestPlatformExporterUtilities:
    """Test PlatformExporter utility methods."""

    def test_get_aspect_ratio_string(self, exporter):
        """Should convert aspect ratio tuple to string."""
        assert exporter.get_aspect_ratio_string((16, 9)) == "16:9"
        assert exporter.get_aspect_ratio_string((9, 16)) == "9:16"
        assert exporter.get_aspect_ratio_string((4, 5)) == "4:5"
        assert exporter.get_aspect_ratio_string((1920, 1080)) == "16:9"
        assert exporter.get_aspect_ratio_string((1080, 1920)) == "9:16"

    def test_get_platforms_by_aspect_ratio(self, exporter):
        """Should find platforms matching aspect ratio."""
        vertical = exporter.get_platforms_by_aspect_ratio((9, 16))
        assert Platform.INSTAGRAM_REELS in vertical
        assert Platform.TIKTOK in vertical
        assert Platform.YOUTUBE_SHORTS in vertical

        horizontal = exporter.get_platforms_by_aspect_ratio((16, 9))
        assert Platform.YOUTUBE in horizontal
        assert Platform.TWITTER in horizontal

    def test_get_all_platforms(self, exporter):
        """Should return all available platforms."""
        platforms = exporter.get_all_platforms()
        assert len(platforms) > 0
        assert Platform.INSTAGRAM_REELS in platforms
        assert Platform.YOUTUBE in platforms

    def test_create_custom_preset(self, exporter):
        """Should create custom preset with specified parameters."""
        preset = exporter.create_custom_preset(
            name="My Custom Preset",
            aspect_ratio=(1, 1),
            resolution=(1000, 1000),
            fps=60,
            video_bitrate="20M",
        )

        assert preset.name == "My Custom Preset"
        assert preset.platform == Platform.CUSTOM
        assert preset.aspect_ratio == (1, 1)
        assert preset.resolution == (1000, 1000)
        assert preset.fps == 60
        assert preset.video_bitrate == "20M"

    def test_create_custom_preset_defaults(self, exporter):
        """Should use defaults for unspecified parameters."""
        preset = exporter.create_custom_preset(
            name="Simple Custom",
            aspect_ratio=(1, 1),
            resolution=(1000, 1000),
        )

        assert preset.fps == 30
        assert preset.codec == "h264"
        assert preset.audio_codec == "aac"


class TestAspectRatioHandling:
    """Test aspect ratio handling across presets."""

    def test_vertical_platforms(self):
        """Vertical platforms should have 9:16 aspect ratio."""
        vertical = [
            Platform.INSTAGRAM_REELS,
            Platform.TIKTOK,
            Platform.YOUTUBE_SHORTS,
        ]

        for platform in vertical:
            preset = PLATFORM_PRESETS[platform]
            assert preset.aspect_ratio == (9, 16)

    def test_horizontal_platforms(self):
        """Horizontal platforms should have 16:9 aspect ratio."""
        horizontal = [Platform.YOUTUBE, Platform.TWITTER]

        for platform in horizontal:
            preset = PLATFORM_PRESETS[platform]
            assert preset.aspect_ratio == (16, 9)

    def test_portrait_platforms(self):
        """Portrait platforms should have tall aspect ratios."""
        portrait = [Platform.INSTAGRAM_FEED, Platform.PINTEREST]

        for platform in portrait:
            preset = PLATFORM_PRESETS[platform]
            w, h = preset.aspect_ratio
            assert h > w


class TestDurationHandling:
    """Test duration limits and optimal ranges."""

    def test_short_form_platforms_have_limits(self):
        """Short-form platforms should have max duration limits."""
        short_form = [
            Platform.INSTAGRAM_REELS,
            Platform.INSTAGRAM_FEED,
            Platform.TIKTOK,
            Platform.YOUTUBE_SHORTS,
        ]

        for platform in short_form:
            preset = PLATFORM_PRESETS[platform]
            assert preset.max_duration is not None
            assert preset.max_duration <= 180.0

    def test_long_form_platforms_unlimited(self):
        """Long-form platforms should have no max duration."""
        preset = PLATFORM_PRESETS[Platform.YOUTUBE]
        assert preset.max_duration is None

    def test_optimal_ranges_valid(self):
        """All optimal ranges should be valid."""
        for preset in PLATFORM_PRESETS.values():
            min_opt, max_opt = preset.optimal_duration
            assert min_opt > 0
            assert max_opt > min_opt
            if preset.max_duration is not None:
                assert max_opt <= preset.max_duration


class TestBitrateHandling:
    """Test bitrate configurations."""

    def test_video_bitrates_are_valid(self):
        """Video bitrates should be valid strings."""
        for preset in PLATFORM_PRESETS.values():
            assert preset.video_bitrate.endswith(("M", "K", "k"))
            bitrate_value = int(preset.video_bitrate[:-1])
            assert bitrate_value > 0

    def test_audio_bitrates_are_valid(self):
        """Audio bitrates should be valid strings."""
        for preset in PLATFORM_PRESETS.values():
            assert preset.audio_bitrate.endswith(("k", "K"))
            bitrate_value = int(preset.audio_bitrate[:-1])
            assert bitrate_value > 0

    def test_higher_quality_platforms_higher_bitrate(self):
        """YouTube should have higher bitrate than Instagram."""
        youtube_bitrate = int(PLATFORM_PRESETS[Platform.YOUTUBE].video_bitrate[:-1])
        instagram_bitrate = int(
            PLATFORM_PRESETS[Platform.INSTAGRAM_REELS].video_bitrate[:-1]
        )

        assert youtube_bitrate > instagram_bitrate
