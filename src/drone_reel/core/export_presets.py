"""
Multi-platform export presets for social media platforms.

Provides export configurations optimized for Instagram, TikTok, YouTube,
and other social media platforms with proper aspect ratios, codecs, and bitrates.
"""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional

from moviepy import VideoFileClip


class Platform(Enum):
    """Supported social media platforms."""

    INSTAGRAM_REELS = "instagram_reels"
    INSTAGRAM_FEED = "instagram_feed"
    TIKTOK = "tiktok"
    YOUTUBE_SHORTS = "youtube_shorts"
    YOUTUBE = "youtube"
    YOUTUBE_4K = "youtube_4k"
    PINTEREST = "pinterest"
    TWITTER = "twitter"
    VERTICAL_4K = "vertical_4k"
    CUSTOM = "custom"


@dataclass
class ExportPreset:
    """Export configuration for a specific platform."""

    name: str
    platform: Platform
    aspect_ratio: tuple[int, int]  # (width, height) ratio
    resolution: tuple[int, int]  # (width, height) pixels
    fps: int
    codec: str
    audio_codec: str
    video_bitrate: str
    audio_bitrate: str
    max_duration: Optional[float]  # seconds, None for unlimited
    optimal_duration: tuple[float, float]  # (min, max) optimal range
    pixel_format: str = "yuv420p"
    preset: str = "medium"  # ffmpeg preset


PLATFORM_PRESETS = {
    Platform.INSTAGRAM_REELS: ExportPreset(
        name="Instagram Reels",
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
    ),
    Platform.INSTAGRAM_FEED: ExportPreset(
        name="Instagram Feed",
        platform=Platform.INSTAGRAM_FEED,
        aspect_ratio=(4, 5),
        resolution=(1080, 1350),
        fps=30,
        codec="h264",
        audio_codec="aac",
        video_bitrate="8M",
        audio_bitrate="128k",
        max_duration=60.0,
        optimal_duration=(15.0, 30.0),
    ),
    Platform.TIKTOK: ExportPreset(
        name="TikTok",
        platform=Platform.TIKTOK,
        aspect_ratio=(9, 16),
        resolution=(1080, 1920),
        fps=30,
        codec="h264",
        audio_codec="aac",
        video_bitrate="10M",
        audio_bitrate="192k",
        max_duration=180.0,
        optimal_duration=(15.0, 60.0),
    ),
    Platform.YOUTUBE_SHORTS: ExportPreset(
        name="YouTube Shorts",
        platform=Platform.YOUTUBE_SHORTS,
        aspect_ratio=(9, 16),
        resolution=(1080, 1920),
        fps=30,
        codec="h264",
        audio_codec="aac",
        video_bitrate="12M",
        audio_bitrate="192k",
        max_duration=60.0,
        optimal_duration=(15.0, 60.0),
    ),
    Platform.YOUTUBE: ExportPreset(
        name="YouTube",
        platform=Platform.YOUTUBE,
        aspect_ratio=(16, 9),
        resolution=(1920, 1080),
        fps=30,
        codec="h264",
        audio_codec="aac",
        video_bitrate="15M",
        audio_bitrate="192k",
        max_duration=None,
        optimal_duration=(60.0, 600.0),
    ),
    Platform.PINTEREST: ExportPreset(
        name="Pinterest",
        platform=Platform.PINTEREST,
        aspect_ratio=(2, 3),
        resolution=(1000, 1500),
        fps=30,
        codec="h264",
        audio_codec="aac",
        video_bitrate="8M",
        audio_bitrate="128k",
        max_duration=None,
        optimal_duration=(6.0, 15.0),
    ),
    Platform.TWITTER: ExportPreset(
        name="Twitter",
        platform=Platform.TWITTER,
        aspect_ratio=(16, 9),
        resolution=(1280, 720),
        fps=30,
        codec="h264",
        audio_codec="aac",
        video_bitrate="10M",
        audio_bitrate="128k",
        max_duration=140.0,
        optimal_duration=(10.0, 45.0),
    ),
    Platform.YOUTUBE_4K: ExportPreset(
        name="YouTube 4K",
        platform=Platform.YOUTUBE_4K,
        aspect_ratio=(16, 9),
        resolution=(3840, 2160),
        fps=30,
        codec="h264",
        audio_codec="aac",
        video_bitrate="45M",
        audio_bitrate="320k",
        max_duration=None,
        optimal_duration=(60.0, 600.0),
    ),
    Platform.VERTICAL_4K: ExportPreset(
        name="Vertical 4K",
        platform=Platform.VERTICAL_4K,
        aspect_ratio=(9, 16),
        resolution=(2160, 3840),
        fps=30,
        codec="h264",
        audio_codec="aac",
        video_bitrate="45M",
        audio_bitrate="320k",
        max_duration=None,
        optimal_duration=(15.0, 60.0),
    ),
}


class PlatformExporter:
    """
    Handles platform-specific video exports.

    Manages export presets, validation, and multi-platform export operations
    for various social media platforms.
    """

    def __init__(self):
        """Initialize the platform exporter."""
        self.presets = PLATFORM_PRESETS

    def get_preset(self, platform: Platform) -> ExportPreset:
        """
        Get export preset for a platform.

        Args:
            platform: Target platform

        Returns:
            ExportPreset for the platform

        Raises:
            ValueError: If platform preset not found
        """
        if platform not in self.presets:
            raise ValueError(
                f"No preset found for platform: {platform}. "
                f"Available platforms: {list(self.presets.keys())}"
            )
        return self.presets[platform]

    def validate_for_platform(
        self, clip_duration: float, platform: Platform
    ) -> dict[str, list[str]]:
        """
        Validate clip meets platform requirements.

        Args:
            clip_duration: Duration of the clip in seconds
            platform: Target platform

        Returns:
            Dictionary with 'errors' and 'warnings' lists
        """
        preset = self.get_preset(platform)
        result = {"errors": [], "warnings": []}

        if preset.max_duration is not None and clip_duration > preset.max_duration:
            result["errors"].append(
                f"Duration {clip_duration:.1f}s exceeds maximum {preset.max_duration:.1f}s "
                f"for {preset.name}"
            )

        min_optimal, max_optimal = preset.optimal_duration
        if clip_duration < min_optimal:
            result["warnings"].append(
                f"Duration {clip_duration:.1f}s is shorter than optimal range "
                f"{min_optimal:.1f}s-{max_optimal:.1f}s for {preset.name}"
            )
        elif clip_duration > max_optimal:
            result["warnings"].append(
                f"Duration {clip_duration:.1f}s exceeds optimal range "
                f"{min_optimal:.1f}s-{max_optimal:.1f}s for {preset.name}"
            )

        return result

    def get_export_params(
        self, platform: Platform, hardware_encoder: Optional[str] = None
    ) -> dict:
        """
        Get MoviePy/FFmpeg export parameters for platform.

        Args:
            platform: Target platform
            hardware_encoder: Optional hardware encoder (e.g., 'h264_videotoolbox')

        Returns:
            Dictionary of export parameters for MoviePy's write_videofile
        """
        preset = self.get_preset(platform)

        codec = hardware_encoder if hardware_encoder else preset.codec

        params = {
            "fps": preset.fps,
            "codec": codec,
            "audio_codec": preset.audio_codec,
            "preset": preset.preset,
            "bitrate": preset.video_bitrate,
            "audio_bitrate": preset.audio_bitrate,
            "ffmpeg_params": ["-pix_fmt", preset.pixel_format],
        }

        return params

    def suggest_platform(
        self, clip_duration: float, aspect_ratio: tuple[int, int]
    ) -> list[Platform]:
        """
        Suggest best platforms for given content.

        Args:
            clip_duration: Duration of the clip in seconds
            aspect_ratio: (width, height) aspect ratio

        Returns:
            List of suggested platforms, ordered by compatibility
        """
        suggestions = []

        for platform, preset in self.presets.items():
            validation = self.validate_for_platform(clip_duration, platform)

            if validation["errors"]:
                continue

            aspect_match = aspect_ratio == preset.aspect_ratio

            min_optimal, max_optimal = preset.optimal_duration
            duration_optimal = min_optimal <= clip_duration <= max_optimal

            if aspect_match and duration_optimal:
                suggestions.insert(0, platform)
            elif aspect_match or duration_optimal:
                suggestions.append(platform)

        return suggestions

    def create_multi_platform_export(
        self,
        clip: VideoFileClip,
        output_dir: Path,
        platforms: list[Platform],
        hardware_encoder: Optional[str] = None,
        base_filename: str = "export",
    ) -> dict[Platform, Path]:
        """
        Export to multiple platforms at once.

        Args:
            clip: VideoFileClip to export
            output_dir: Directory for output files
            platforms: List of platforms to export to
            hardware_encoder: Optional hardware encoder to use
            base_filename: Base name for output files

        Returns:
            Dictionary mapping Platform to output Path

        Raises:
            ValueError: If validation fails for any platform
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        results = {}

        for platform in platforms:
            preset = self.get_preset(platform)

            validation = self.validate_for_platform(clip.duration, platform)
            if validation["errors"]:
                raise ValueError(
                    f"Validation failed for {preset.name}: {validation['errors']}"
                )

            output_path = output_dir / f"{base_filename}_{platform.value}.mp4"

            resized_clip = clip.resized(preset.resolution)

            export_params = self.get_export_params(platform, hardware_encoder)

            try:
                resized_clip.write_videofile(
                    str(output_path),
                    **export_params,
                    logger=None,
                )
                results[platform] = output_path
            finally:
                resized_clip.close()

        return results

    def get_aspect_ratio_string(self, aspect_ratio: tuple[int, int]) -> str:
        """
        Convert aspect ratio tuple to string.

        Args:
            aspect_ratio: (width, height) tuple

        Returns:
            Formatted aspect ratio string (e.g., "16:9")
        """
        from math import gcd

        w, h = aspect_ratio
        divisor = gcd(w, h)
        return f"{w // divisor}:{h // divisor}"

    def get_platforms_by_aspect_ratio(
        self, aspect_ratio: tuple[int, int]
    ) -> list[Platform]:
        """
        Get all platforms matching a specific aspect ratio.

        Args:
            aspect_ratio: (width, height) aspect ratio

        Returns:
            List of platforms with matching aspect ratio
        """
        matching = []
        for platform, preset in self.presets.items():
            if preset.aspect_ratio == aspect_ratio:
                matching.append(platform)
        return matching

    def get_all_platforms(self) -> list[Platform]:
        """
        Get list of all available platforms.

        Returns:
            List of all Platform enum values with presets
        """
        return list(self.presets.keys())

    def create_custom_preset(
        self,
        name: str,
        aspect_ratio: tuple[int, int],
        resolution: tuple[int, int],
        fps: int = 30,
        codec: str = "h264",
        audio_codec: str = "aac",
        video_bitrate: str = "10M",
        audio_bitrate: str = "128k",
        max_duration: Optional[float] = None,
        optimal_duration: tuple[float, float] = (15.0, 60.0),
    ) -> ExportPreset:
        """
        Create a custom export preset.

        Args:
            name: Preset name
            aspect_ratio: (width, height) ratio
            resolution: (width, height) in pixels
            fps: Frame rate
            codec: Video codec
            audio_codec: Audio codec
            video_bitrate: Video bitrate string
            audio_bitrate: Audio bitrate string
            max_duration: Maximum duration in seconds (None for unlimited)
            optimal_duration: (min, max) optimal duration range

        Returns:
            Custom ExportPreset
        """
        return ExportPreset(
            name=name,
            platform=Platform.CUSTOM,
            aspect_ratio=aspect_ratio,
            resolution=resolution,
            fps=fps,
            codec=codec,
            audio_codec=audio_codec,
            video_bitrate=video_bitrate,
            audio_bitrate=audio_bitrate,
            max_duration=max_duration,
            optimal_duration=optimal_duration,
        )
