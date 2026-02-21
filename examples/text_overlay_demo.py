"""
Text overlay demonstration for drone-reel.

Shows how to use the text overlay system with various animations,
lower thirds, and beat-synced captions.
"""

from pathlib import Path

from moviepy import VideoFileClip

from drone_reel.core.text_overlay import (
    TextAnimation,
    TextOverlay,
    TextRenderer,
)


def demo_basic_text_overlay(video_path: Path, output_path: Path):
    """Demonstrate basic text overlay with fade animation."""
    print("Demo 1: Basic text overlay with fade in/out...")

    clip = VideoFileClip(str(video_path))
    renderer = TextRenderer()

    overlay = TextOverlay(
        text="Amazing Drone Footage",
        position=(0.5, 0.1),
        font_size=72,
        color=(255, 255, 255),
        shadow=True,
        animation_in=TextAnimation.FADE_IN,
        animation_out=TextAnimation.FADE_OUT,
        animation_duration=0.5,
        start_time=1.0,
        duration=3.0,
    )

    result_clip = renderer.apply_overlay_to_clip(clip, overlay)
    result_clip.write_videofile(
        str(output_path),
        codec="libx264",
        audio_codec="aac",
        logger=None,
    )

    clip.close()
    result_clip.close()
    print(f"Saved to: {output_path}")


def demo_multiple_overlays(video_path: Path, output_path: Path):
    """Demonstrate multiple text overlays with different animations."""
    print("Demo 2: Multiple overlays with different animations...")

    clip = VideoFileClip(str(video_path))
    renderer = TextRenderer()

    overlays = [
        TextOverlay(
            text="POP Animation",
            position=(0.5, 0.2),
            font_size=56,
            animation_in=TextAnimation.POP,
            animation_out=TextAnimation.FADE_OUT,
            start_time=0.5,
            duration=2.0,
        ),
        TextOverlay(
            text="Slide Up Animation",
            position=(0.5, 0.5),
            font_size=56,
            animation_in=TextAnimation.SLIDE_UP,
            animation_out=TextAnimation.SLIDE_DOWN,
            start_time=2.0,
            duration=2.0,
        ),
        TextOverlay(
            text="Typewriter Effect",
            position=(0.5, 0.8),
            font_size=48,
            animation_in=TextAnimation.TYPEWRITER,
            animation_out=TextAnimation.FADE_OUT,
            animation_duration=1.5,
            start_time=4.0,
            duration=3.0,
        ),
    ]

    result_clip = renderer.apply_multiple_overlays(clip, overlays)
    result_clip.write_videofile(
        str(output_path),
        codec="libx264",
        audio_codec="aac",
        logger=None,
    )

    clip.close()
    result_clip.close()
    print(f"Saved to: {output_path}")


def demo_lower_thirds(video_path: Path, output_path: Path):
    """Demonstrate professional lower third overlays."""
    print("Demo 3: Professional lower thirds...")

    clip = VideoFileClip(str(video_path))
    renderer = TextRenderer()

    lower_thirds_modern = renderer.create_lower_third(
        title="Modern Style",
        subtitle="Sleek and professional",
        style="modern",
    )
    for overlay in lower_thirds_modern:
        overlay.start_time = 1.0
        overlay.duration = 3.0

    lower_thirds_bold = renderer.create_lower_third(
        title="Bold Impact",
        subtitle="Eye-catching design",
        style="bold",
    )
    for overlay in lower_thirds_bold:
        overlay.start_time = 5.0
        overlay.duration = 3.0

    lower_thirds_minimal = renderer.create_lower_third(
        title="Minimal Elegance",
        style="minimal",
    )
    for overlay in lower_thirds_minimal:
        overlay.start_time = 9.0
        overlay.duration = 3.0

    all_overlays = lower_thirds_modern + lower_thirds_bold + lower_thirds_minimal
    result_clip = renderer.apply_multiple_overlays(clip, all_overlays)

    result_clip.write_videofile(
        str(output_path),
        codec="libx264",
        audio_codec="aac",
        logger=None,
    )

    clip.close()
    result_clip.close()
    print(f"Saved to: {output_path}")


def demo_beat_synced_captions(video_path: Path, output_path: Path):
    """Demonstrate beat-synced captions."""
    print("Demo 4: Beat-synced captions...")

    clip = VideoFileClip(str(video_path))
    renderer = TextRenderer()

    captions = [
        "Epic Aerial View",
        "Stunning Landscape",
        "Cinematic Perfection",
        "Professional Quality",
    ]

    beat_times = [0.5, 2.0, 3.5, 5.0]

    overlays = renderer.create_beat_synced_captions(
        captions=captions,
        beat_times=beat_times,
        duration_per_caption=1.5,
    )

    result_clip = renderer.apply_multiple_overlays(clip, overlays)
    result_clip.write_videofile(
        str(output_path),
        codec="libx264",
        audio_codec="aac",
        logger=None,
    )

    clip.close()
    result_clip.close()
    print(f"Saved to: {output_path}")


def demo_auto_placement(video_path: Path, output_path: Path):
    """Demonstrate automatic text placement."""
    print("Demo 5: Auto placement in different zones...")

    clip = VideoFileClip(str(video_path))
    renderer = TextRenderer()

    sample_frame = clip.get_frame(0)

    overlays = []

    for i, zone in enumerate(["top", "bottom", "center", "lower_third"]):
        position = renderer.auto_place_text(sample_frame, f"{zone.title()} Zone", zone)

        overlay = TextOverlay(
            text=f"{zone.title()} Zone",
            position=position,
            font_size=48,
            animation_in=TextAnimation.FADE_IN,
            animation_out=TextAnimation.FADE_OUT,
            start_time=i * 2.0,
            duration=2.0,
        )
        overlays.append(overlay)

    result_clip = renderer.apply_multiple_overlays(clip, overlays)
    result_clip.write_videofile(
        str(output_path),
        codec="libx264",
        audio_codec="aac",
        logger=None,
    )

    clip.close()
    result_clip.close()
    print(f"Saved to: {output_path}")


def demo_custom_styles(video_path: Path, output_path: Path):
    """Demonstrate custom text styles and backgrounds."""
    print("Demo 6: Custom styles with backgrounds...")

    clip = VideoFileClip(str(video_path))
    renderer = TextRenderer()

    overlays = [
        TextOverlay(
            text="Black Background",
            position=(0.5, 0.2),
            font_size=56,
            color=(255, 255, 255),
            background_color=(0, 0, 0, 200),
            shadow=False,
            animation_in=TextAnimation.SLIDE_LEFT,
            start_time=0.5,
            duration=2.5,
        ),
        TextOverlay(
            text="Blue Background",
            position=(0.5, 0.4),
            font_size=56,
            color=(255, 255, 255),
            background_color=(0, 100, 200, 180),
            shadow=True,
            animation_in=TextAnimation.SLIDE_RIGHT,
            start_time=2.5,
            duration=2.5,
        ),
        TextOverlay(
            text="Gold Text",
            position=(0.5, 0.6),
            font_size=64,
            color=(255, 215, 0),
            background_color=None,
            shadow=True,
            shadow_offset=(4, 4),
            animation_in=TextAnimation.POP,
            start_time=4.5,
            duration=2.5,
        ),
    ]

    result_clip = renderer.apply_multiple_overlays(clip, overlays)
    result_clip.write_videofile(
        str(output_path),
        codec="libx264",
        audio_codec="aac",
        logger=None,
    )

    clip.close()
    result_clip.close()
    print(f"Saved to: {output_path}")


def main():
    """Run all text overlay demonstrations."""
    video_path = Path("input_video.mp4")

    if not video_path.exists():
        print(f"Error: Please provide a video file at {video_path}")
        print("You can use any drone footage video for testing.")
        return

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    demos = [
        (demo_basic_text_overlay, "01_basic_overlay.mp4"),
        (demo_multiple_overlays, "02_multiple_overlays.mp4"),
        (demo_lower_thirds, "03_lower_thirds.mp4"),
        (demo_beat_synced_captions, "04_beat_synced.mp4"),
        (demo_auto_placement, "05_auto_placement.mp4"),
        (demo_custom_styles, "06_custom_styles.mp4"),
    ]

    print("=" * 60)
    print("Text Overlay System Demonstration")
    print("=" * 60)
    print()

    for demo_func, output_name in demos:
        output_path = output_dir / output_name
        try:
            demo_func(video_path, output_path)
            print()
        except Exception as e:
            print(f"Error in {demo_func.__name__}: {e}")
            print()

    print("=" * 60)
    print("All demonstrations complete!")
    print(f"Output files saved to: {output_dir.absolute()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
