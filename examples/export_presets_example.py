"""
Example demonstrating multi-platform export presets.

This script shows how to use the PlatformExporter to:
- List available platforms
- Get platform specifications
- Validate content for platforms
- Export to multiple platforms
- Suggest optimal platforms
"""

from pathlib import Path

from drone_reel.core.export_presets import Platform, PlatformExporter


def list_all_platforms():
    """List all available platform presets with their specifications."""
    print("\n=== Available Platform Presets ===\n")

    exporter = PlatformExporter()

    for platform in exporter.get_all_platforms():
        preset = exporter.get_preset(platform)

        print(f"{preset.name}:")
        print(f"  Aspect Ratio: {exporter.get_aspect_ratio_string(preset.aspect_ratio)}")
        print(f"  Resolution: {preset.resolution[0]}x{preset.resolution[1]}")
        print(f"  FPS: {preset.fps}")
        print(f"  Max Duration: {preset.max_duration}s" if preset.max_duration else "  Max Duration: Unlimited")
        min_opt, max_opt = preset.optimal_duration
        print(f"  Optimal Range: {min_opt}s - {max_opt}s")
        print(f"  Video Bitrate: {preset.video_bitrate}")
        print(f"  Audio Bitrate: {preset.audio_bitrate}")
        print()


def validate_content_for_platforms(duration: float, aspect_ratio: tuple[int, int]):
    """Validate content duration and aspect ratio for different platforms."""
    print(f"\n=== Validating {duration}s video with {aspect_ratio[0]}:{aspect_ratio[1]} aspect ratio ===\n")

    exporter = PlatformExporter()

    platforms_to_check = [
        Platform.INSTAGRAM_REELS,
        Platform.TIKTOK,
        Platform.YOUTUBE_SHORTS,
        Platform.YOUTUBE,
    ]

    for platform in platforms_to_check:
        preset = exporter.get_preset(platform)
        validation = exporter.validate_for_platform(duration, platform)

        print(f"{preset.name}:")

        if not validation["errors"] and not validation["warnings"]:
            print("  ✓ Content meets all requirements")
        else:
            if validation["errors"]:
                for error in validation["errors"]:
                    print(f"  ✗ Error: {error}")

            if validation["warnings"]:
                for warning in validation["warnings"]:
                    print(f"  ⚠ Warning: {warning}")

        print()


def suggest_platforms_for_content(duration: float, aspect_ratio: tuple[int, int]):
    """Get platform suggestions based on content characteristics."""
    print(f"\n=== Platform Suggestions for {duration}s video ({aspect_ratio[0]}:{aspect_ratio[1]}) ===\n")

    exporter = PlatformExporter()
    suggestions = exporter.suggest_platform(duration, aspect_ratio)

    if suggestions:
        print("Recommended platforms (ordered by compatibility):")
        for i, platform in enumerate(suggestions, 1):
            preset = exporter.get_preset(platform)
            print(f"  {i}. {preset.name}")
    else:
        print("No platforms match this content's requirements.")

    print()


def get_export_parameters_example():
    """Show how to get export parameters for a platform."""
    print("\n=== Export Parameters for Instagram Reels ===\n")

    exporter = PlatformExporter()
    preset = exporter.get_preset(Platform.INSTAGRAM_REELS)

    # Get parameters without hardware encoder
    params = exporter.get_export_params(Platform.INSTAGRAM_REELS)

    print("MoviePy write_videofile parameters:")
    for key, value in params.items():
        print(f"  {key}: {value}")

    print("\n--- With Hardware Encoder ---\n")

    # Get parameters with hardware encoder
    params_hw = exporter.get_export_params(
        Platform.INSTAGRAM_REELS,
        hardware_encoder="h264_videotoolbox"
    )

    print("MoviePy write_videofile parameters (hardware):")
    for key, value in params_hw.items():
        print(f"  {key}: {value}")

    print()


def create_custom_preset_example():
    """Demonstrate creating a custom export preset."""
    print("\n=== Creating Custom Preset ===\n")

    exporter = PlatformExporter()

    # Create a custom preset for square 4K videos
    custom = exporter.create_custom_preset(
        name="4K Square",
        aspect_ratio=(1, 1),
        resolution=(3840, 3840),
        fps=60,
        video_bitrate="50M",
        audio_bitrate="320k",
        max_duration=300.0,
        optimal_duration=(30.0, 120.0),
    )

    print(f"Custom Preset: {custom.name}")
    print(f"  Aspect Ratio: {custom.aspect_ratio}")
    print(f"  Resolution: {custom.resolution}")
    print(f"  FPS: {custom.fps}")
    print(f"  Video Bitrate: {custom.video_bitrate}")
    print(f"  Audio Bitrate: {custom.audio_bitrate}")
    print()


def multi_platform_export_simulation():
    """Show how multi-platform export would work (simulation only)."""
    print("\n=== Multi-Platform Export (Simulation) ===\n")

    exporter = PlatformExporter()

    platforms = [
        Platform.INSTAGRAM_REELS,
        Platform.TIKTOK,
        Platform.YOUTUBE_SHORTS,
    ]

    print("Would export to the following platforms:")
    for platform in platforms:
        preset = exporter.get_preset(platform)
        print(f"  - {preset.name} ({preset.resolution[0]}x{preset.resolution[1]})")

    print("\nOutput files would be:")
    output_dir = Path("./exports")
    base_filename = "my_drone_reel"

    for platform in platforms:
        output_path = output_dir / f"{base_filename}_{platform.value}.mp4"
        print(f"  {output_path}")

    print()


def main():
    """Run all examples."""
    print("=" * 60)
    print("Multi-Platform Export Presets Examples")
    print("=" * 60)

    # Example 1: List all platforms
    list_all_platforms()

    # Example 2: Validate a 30-second vertical video
    validate_content_for_platforms(duration=30.0, aspect_ratio=(9, 16))

    # Example 3: Validate a 2-minute horizontal video
    validate_content_for_platforms(duration=120.0, aspect_ratio=(16, 9))

    # Example 4: Get platform suggestions for vertical content
    suggest_platforms_for_content(duration=25.0, aspect_ratio=(9, 16))

    # Example 5: Get platform suggestions for horizontal content
    suggest_platforms_for_content(duration=90.0, aspect_ratio=(16, 9))

    # Example 6: Show export parameters
    get_export_parameters_example()

    # Example 7: Create custom preset
    create_custom_preset_example()

    # Example 8: Multi-platform export simulation
    multi_platform_export_simulation()

    print("=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
