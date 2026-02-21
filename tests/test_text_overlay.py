"""
Tests for text overlay system.

Tests all animation types, rendering, auto-placement, templates,
and edge cases.
"""

import tempfile
from pathlib import Path

import cv2
import numpy as np
import pytest
from moviepy import VideoFileClip

from drone_reel.core.text_overlay import (
    TextAnimation,
    TextOverlay,
    TextRenderer,
)


@pytest.fixture
def renderer():
    """Create a TextRenderer instance."""
    return TextRenderer()


@pytest.fixture
def sample_frame():
    """Create a sample video frame (1920x1080, blue background)."""
    frame = np.zeros((1080, 1920, 3), dtype=np.uint8)
    frame[:, :] = (200, 100, 50)
    return frame


@pytest.fixture
def sample_video(tmp_path):
    """Create a sample video clip for testing."""
    video_path = tmp_path / "test_video.mp4"

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(video_path), fourcc, 30, (640, 480))

    for i in range(90):
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        frame[:, :] = (100, 150, 200)
        writer.write(frame)

    writer.release()
    return video_path


class TestTextAnimation:
    """Test TextAnimation enum."""

    def test_animation_values(self):
        """Test all animation types have correct values."""
        assert TextAnimation.NONE.value == "none"
        assert TextAnimation.FADE_IN.value == "fade_in"
        assert TextAnimation.FADE_OUT.value == "fade_out"
        assert TextAnimation.FADE_IN_OUT.value == "fade_in_out"
        assert TextAnimation.POP.value == "pop"
        assert TextAnimation.TYPEWRITER.value == "typewriter"
        assert TextAnimation.SLIDE_UP.value == "slide_up"
        assert TextAnimation.SLIDE_DOWN.value == "slide_down"
        assert TextAnimation.SLIDE_LEFT.value == "slide_left"
        assert TextAnimation.SLIDE_RIGHT.value == "slide_right"

    def test_animation_count(self):
        """Test expected number of animation types."""
        assert len(TextAnimation) == 10


class TestTextOverlay:
    """Test TextOverlay dataclass."""

    def test_default_values(self):
        """Test default overlay values."""
        overlay = TextOverlay(text="Test")
        assert overlay.text == "Test"
        assert overlay.position == (0.5, 0.9)
        assert overlay.font == "Arial-Bold"
        assert overlay.font_size == 48
        assert overlay.color == (255, 255, 255)
        assert overlay.background_color is None
        assert overlay.shadow is True
        assert overlay.shadow_color == (0, 0, 0)
        assert overlay.shadow_offset == (2, 2)
        assert overlay.animation_in == TextAnimation.FADE_IN
        assert overlay.animation_out == TextAnimation.FADE_OUT
        assert overlay.animation_duration == 0.3
        assert overlay.start_time == 0.0
        assert overlay.duration == 3.0
        assert overlay.align == "center"

    def test_custom_values(self):
        """Test custom overlay configuration."""
        overlay = TextOverlay(
            text="Custom",
            position=(0.2, 0.5),
            font_size=64,
            color=(255, 0, 0),
            background_color=(0, 0, 0, 200),
            shadow=False,
            animation_in=TextAnimation.POP,
            animation_out=TextAnimation.SLIDE_LEFT,
            duration=5.0,
            align="left",
        )
        assert overlay.text == "Custom"
        assert overlay.position == (0.2, 0.5)
        assert overlay.font_size == 64
        assert overlay.color == (255, 0, 0)
        assert overlay.background_color == (0, 0, 0, 200)
        assert overlay.shadow is False
        assert overlay.animation_in == TextAnimation.POP
        assert overlay.animation_out == TextAnimation.SLIDE_LEFT
        assert overlay.duration == 5.0
        assert overlay.align == "left"


class TestTextRenderer:
    """Test TextRenderer class."""

    def test_initialization(self):
        """Test renderer initialization."""
        renderer = TextRenderer()
        assert renderer._font_cache == {}
        assert len(renderer.SAFE_ZONES) == 4
        assert "top" in renderer.SAFE_ZONES
        assert "bottom" in renderer.SAFE_ZONES
        assert "center" in renderer.SAFE_ZONES
        assert "lower_third" in renderer.SAFE_ZONES

    def test_safe_zones(self):
        """Test safe zone definitions."""
        zones = TextRenderer.SAFE_ZONES
        assert zones["top"]["y_range"] == (0.05, 0.20)
        assert zones["bottom"]["y_range"] == (0.80, 0.95)
        assert zones["center"]["y_range"] == (0.40, 0.60)
        assert zones["lower_third"]["y_range"] == (0.75, 0.90)

    def test_get_font_caching(self, renderer):
        """Test font caching mechanism."""
        font1 = renderer._get_font("Arial-Bold", 48)
        font2 = renderer._get_font("Arial-Bold", 48)
        assert font1 is font2
        assert ("Arial-Bold", 48) in renderer._font_cache

    def test_get_font_different_sizes(self, renderer):
        """Test different font sizes are cached separately."""
        font1 = renderer._get_font("Arial-Bold", 48)
        font2 = renderer._get_font("Arial-Bold", 64)
        assert font1 is not font2
        assert len(renderer._font_cache) == 2

    def test_ease_out_cubic(self, renderer):
        """Test cubic ease-out function."""
        assert renderer._ease_out_cubic(0.0) == 0.0
        assert renderer._ease_out_cubic(1.0) == 1.0
        mid = renderer._ease_out_cubic(0.5)
        assert 0.0 < mid < 1.0
        assert mid > 0.5

    def test_ease_in_out_cubic(self, renderer):
        """Test cubic ease-in-out function."""
        assert renderer._ease_in_out_cubic(0.0) == 0.0
        assert renderer._ease_in_out_cubic(1.0) == 1.0
        mid = renderer._ease_in_out_cubic(0.5)
        assert 0.0 < mid < 1.0

    def test_calculate_animation_progress(self, renderer):
        """Test animation progress calculation."""
        overlay = TextOverlay(
            text="Test",
            animation_duration=0.5,
            start_time=1.0,
            duration=3.0,
        )

        in_prog, out_prog = renderer._calculate_animation_progress(overlay, 1.0)
        assert in_prog == 0.0
        assert out_prog == 1.0

        in_prog, out_prog = renderer._calculate_animation_progress(overlay, 1.25)
        assert in_prog == 0.5
        assert out_prog == 1.0

        in_prog, out_prog = renderer._calculate_animation_progress(overlay, 3.5)
        assert in_prog == 1.0
        assert out_prog == 1.0

    def test_render_text_frame_basic(self, renderer, sample_frame):
        """Test basic text rendering on frame."""
        overlay = TextOverlay(
            text="Test Text",
            animation_in=TextAnimation.NONE,
            animation_out=TextAnimation.NONE,
        )
        result = renderer.render_text_frame(sample_frame, overlay, 0.5)
        assert result.shape == sample_frame.shape
        assert not np.array_equal(result, sample_frame)

    def test_render_text_frame_with_shadow(self, renderer, sample_frame):
        """Test text rendering with shadow."""
        overlay = TextOverlay(
            text="Shadow Text",
            shadow=True,
            shadow_offset=(5, 5),
            animation_in=TextAnimation.NONE,
            animation_out=TextAnimation.NONE,
        )
        result = renderer.render_text_frame(sample_frame, overlay, 0.5)
        assert result.shape == sample_frame.shape

    def test_render_text_frame_with_background(self, renderer, sample_frame):
        """Test text rendering with background."""
        overlay = TextOverlay(
            text="Background Text",
            background_color=(0, 0, 0, 180),
            animation_in=TextAnimation.NONE,
            animation_out=TextAnimation.NONE,
        )
        result = renderer.render_text_frame(sample_frame, overlay, 0.5)
        assert result.shape == sample_frame.shape

    def test_render_text_frame_fade_in(self, renderer, sample_frame):
        """Test fade in animation."""
        overlay = TextOverlay(
            text="Fade In",
            animation_in=TextAnimation.FADE_IN,
            animation_out=TextAnimation.NONE,
            animation_duration=0.5,
        )

        result_start = renderer.render_text_frame(sample_frame.copy(), overlay, 0.0)
        result_mid = renderer.render_text_frame(sample_frame.copy(), overlay, 0.5)
        result_end = renderer.render_text_frame(sample_frame.copy(), overlay, 1.0)

        assert result_start.shape == sample_frame.shape
        assert result_mid.shape == sample_frame.shape
        assert result_end.shape == sample_frame.shape

    def test_render_text_frame_fade_out(self, renderer, sample_frame):
        """Test fade out animation."""
        overlay = TextOverlay(
            text="Fade Out",
            animation_in=TextAnimation.NONE,
            animation_out=TextAnimation.FADE_OUT,
            animation_duration=0.5,
            duration=2.0,
        )
        result = renderer.render_text_frame(sample_frame, overlay, 0.9)
        assert result.shape == sample_frame.shape

    def test_render_text_frame_pop(self, renderer, sample_frame):
        """Test pop animation."""
        overlay = TextOverlay(
            text="Pop",
            animation_in=TextAnimation.POP,
            animation_out=TextAnimation.NONE,
        )
        result = renderer.render_text_frame(sample_frame, overlay, 0.2)
        assert result.shape == sample_frame.shape

    def test_render_text_frame_typewriter(self, renderer, sample_frame):
        """Test typewriter animation."""
        overlay = TextOverlay(
            text="Typewriter Text",
            animation_in=TextAnimation.TYPEWRITER,
            animation_out=TextAnimation.NONE,
            animation_duration=1.0,
        )

        result_start = renderer.render_text_frame(sample_frame.copy(), overlay, 0.0)
        result_mid = renderer.render_text_frame(sample_frame.copy(), overlay, 0.5)
        result_end = renderer.render_text_frame(sample_frame.copy(), overlay, 1.0)

        assert result_start.shape == sample_frame.shape
        assert result_mid.shape == sample_frame.shape
        assert result_end.shape == sample_frame.shape

    def test_render_text_frame_slide_up(self, renderer, sample_frame):
        """Test slide up animation."""
        overlay = TextOverlay(
            text="Slide Up",
            animation_in=TextAnimation.SLIDE_UP,
            animation_out=TextAnimation.NONE,
        )
        result = renderer.render_text_frame(sample_frame, overlay, 0.5)
        assert result.shape == sample_frame.shape

    def test_render_text_frame_slide_down(self, renderer, sample_frame):
        """Test slide down animation."""
        overlay = TextOverlay(
            text="Slide Down",
            animation_in=TextAnimation.SLIDE_DOWN,
            animation_out=TextAnimation.NONE,
        )
        result = renderer.render_text_frame(sample_frame, overlay, 0.5)
        assert result.shape == sample_frame.shape

    def test_render_text_frame_slide_left(self, renderer, sample_frame):
        """Test slide left animation."""
        overlay = TextOverlay(
            text="Slide Left",
            animation_in=TextAnimation.SLIDE_LEFT,
            animation_out=TextAnimation.NONE,
        )
        result = renderer.render_text_frame(sample_frame, overlay, 0.5)
        assert result.shape == sample_frame.shape

    def test_render_text_frame_slide_right(self, renderer, sample_frame):
        """Test slide right animation."""
        overlay = TextOverlay(
            text="Slide Right",
            animation_in=TextAnimation.SLIDE_RIGHT,
            animation_out=TextAnimation.NONE,
        )
        result = renderer.render_text_frame(sample_frame, overlay, 0.5)
        assert result.shape == sample_frame.shape

    def test_render_text_frame_alignment_left(self, renderer, sample_frame):
        """Test left text alignment."""
        overlay = TextOverlay(
            text="Left Aligned",
            align="left",
            position=(0.1, 0.5),
            animation_in=TextAnimation.NONE,
            animation_out=TextAnimation.NONE,
        )
        result = renderer.render_text_frame(sample_frame, overlay, 0.5)
        assert result.shape == sample_frame.shape

    def test_render_text_frame_alignment_right(self, renderer, sample_frame):
        """Test right text alignment."""
        overlay = TextOverlay(
            text="Right Aligned",
            align="right",
            position=(0.9, 0.5),
            animation_in=TextAnimation.NONE,
            animation_out=TextAnimation.NONE,
        )
        result = renderer.render_text_frame(sample_frame, overlay, 0.5)
        assert result.shape == sample_frame.shape

    def test_render_text_frame_alignment_center(self, renderer, sample_frame):
        """Test center text alignment."""
        overlay = TextOverlay(
            text="Center Aligned",
            align="center",
            animation_in=TextAnimation.NONE,
            animation_out=TextAnimation.NONE,
        )
        result = renderer.render_text_frame(sample_frame, overlay, 0.5)
        assert result.shape == sample_frame.shape

    def test_apply_overlay_to_clip(self, renderer, sample_video):
        """Test applying overlay to video clip."""
        clip = VideoFileClip(str(sample_video))
        overlay = TextOverlay(
            text="Test Overlay",
            start_time=0.5,
            duration=1.0,
        )

        try:
            result_clip = renderer.apply_overlay_to_clip(clip, overlay)
            assert result_clip.duration == clip.duration
            assert result_clip.fps == clip.fps
            assert tuple(result_clip.size) == tuple(clip.size)

            frame_at_0 = result_clip.get_frame(0.0)
            frame_at_1 = result_clip.get_frame(1.0)
            assert frame_at_0.shape == (480, 640, 3)
            assert frame_at_1.shape == (480, 640, 3)
        finally:
            clip.close()
            if "result_clip" in locals():
                result_clip.close()

    def test_apply_multiple_overlays(self, renderer, sample_video):
        """Test applying multiple overlays to clip."""
        clip = VideoFileClip(str(sample_video))

        overlays = [
            TextOverlay(
                text="First",
                start_time=0.0,
                duration=1.0,
                position=(0.5, 0.3),
            ),
            TextOverlay(
                text="Second",
                start_time=0.5,
                duration=1.5,
                position=(0.5, 0.7),
            ),
        ]

        try:
            result_clip = renderer.apply_multiple_overlays(clip, overlays)
            assert result_clip.duration == clip.duration

            frame = result_clip.get_frame(0.75)
            assert frame.shape == (480, 640, 3)
        finally:
            clip.close()
            if "result_clip" in locals():
                result_clip.close()

    def test_auto_place_text_bottom(self, renderer, sample_frame):
        """Test auto-placement in bottom zone."""
        pos = renderer.auto_place_text(sample_frame, "Test Text", "bottom")
        assert isinstance(pos, tuple)
        assert len(pos) == 2
        assert 0.0 <= pos[0] <= 1.0
        assert 0.0 <= pos[1] <= 1.0
        assert 0.80 <= pos[1] <= 0.95

    def test_auto_place_text_top(self, renderer, sample_frame):
        """Test auto-placement in top zone."""
        pos = renderer.auto_place_text(sample_frame, "Test Text", "top")
        assert isinstance(pos, tuple)
        assert 0.05 <= pos[1] <= 0.20

    def test_auto_place_text_center(self, renderer, sample_frame):
        """Test auto-placement in center zone."""
        pos = renderer.auto_place_text(sample_frame, "Test Text", "center")
        assert isinstance(pos, tuple)
        assert 0.40 <= pos[1] <= 0.60

    def test_auto_place_text_invalid_zone(self, renderer, sample_frame):
        """Test auto-placement with invalid zone defaults to bottom."""
        pos = renderer.auto_place_text(sample_frame, "Test Text", "invalid_zone")
        assert isinstance(pos, tuple)
        assert 0.80 <= pos[1] <= 0.95

    def test_create_lower_third_modern(self, renderer):
        """Test modern lower third creation."""
        overlays = renderer.create_lower_third("Main Title", "Subtitle", "modern")
        assert len(overlays) == 2
        assert overlays[0].text == "Main Title"
        assert overlays[1].text == "Subtitle"
        assert overlays[0].animation_in == TextAnimation.SLIDE_LEFT
        assert overlays[0].background_color is not None
        assert overlays[0].align == "left"

    def test_create_lower_third_minimal(self, renderer):
        """Test minimal lower third creation."""
        overlays = renderer.create_lower_third("Title Only", None, "minimal")
        assert len(overlays) == 1
        assert overlays[0].text == "Title Only"
        assert overlays[0].animation_in == TextAnimation.FADE_IN
        assert overlays[0].background_color is None
        assert overlays[0].align == "center"

    def test_create_lower_third_bold(self, renderer):
        """Test bold lower third creation."""
        overlays = renderer.create_lower_third("Bold Title", "Bold Sub", "bold")
        assert len(overlays) == 2
        assert overlays[0].font_size == 72
        assert overlays[0].color == (255, 215, 0)
        assert overlays[0].animation_in == TextAnimation.POP

    def test_create_lower_third_unknown_style(self, renderer):
        """Test lower third with unknown style."""
        overlays = renderer.create_lower_third("Title", "Sub", "unknown")
        assert len(overlays) == 2
        assert overlays[0].text == "Title"
        assert overlays[1].text == "Sub"

    def test_create_lower_third_no_subtitle(self, renderer):
        """Test lower third without subtitle."""
        overlays = renderer.create_lower_third("Only Title", style="modern")
        assert len(overlays) == 1
        assert overlays[0].text == "Only Title"

    def test_create_beat_synced_captions(self, renderer):
        """Test beat-synced caption creation."""
        captions = ["First", "Second", "Third"]
        beat_times = [0.5, 1.5, 2.5]
        overlays = renderer.create_beat_synced_captions(captions, beat_times)

        assert len(overlays) == 3
        assert overlays[0].text == "First"
        assert overlays[0].start_time == 0.5
        assert overlays[1].text == "Second"
        assert overlays[1].start_time == 1.5
        assert overlays[2].text == "Third"
        assert overlays[2].start_time == 2.5

        assert overlays[0].animation_in == TextAnimation.POP
        assert overlays[1].animation_in == TextAnimation.FADE_IN
        assert overlays[2].animation_in == TextAnimation.SLIDE_UP

    def test_create_beat_synced_captions_mismatched_lengths(self, renderer):
        """Test beat-synced captions with different lengths."""
        captions = ["First", "Second", "Third", "Fourth", "Fifth"]
        beat_times = [0.5, 1.5, 2.5]
        overlays = renderer.create_beat_synced_captions(captions, beat_times)

        assert len(overlays) == 3

        captions_short = ["First", "Second"]
        beat_times_long = [0.5, 1.5, 2.5, 3.5]
        overlays = renderer.create_beat_synced_captions(captions_short, beat_times_long)

        assert len(overlays) == 2

    def test_create_beat_synced_captions_custom_duration(self, renderer):
        """Test beat-synced captions with custom duration."""
        captions = ["Test"]
        beat_times = [1.0]
        duration = 5.0
        overlays = renderer.create_beat_synced_captions(
            captions, beat_times, duration_per_caption=duration
        )

        assert len(overlays) == 1
        assert overlays[0].duration == duration


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_text(self, renderer, sample_frame):
        """Test rendering empty text."""
        overlay = TextOverlay(
            text="",
            animation_in=TextAnimation.NONE,
            animation_out=TextAnimation.NONE,
        )
        result = renderer.render_text_frame(sample_frame, overlay, 0.5)
        assert result.shape == sample_frame.shape

    def test_very_long_text(self, renderer, sample_frame):
        """Test rendering very long text."""
        overlay = TextOverlay(
            text="This is a very long text that should still render properly",
            animation_in=TextAnimation.NONE,
            animation_out=TextAnimation.NONE,
        )
        result = renderer.render_text_frame(sample_frame, overlay, 0.5)
        assert result.shape == sample_frame.shape

    def test_special_characters(self, renderer, sample_frame):
        """Test rendering special characters."""
        overlay = TextOverlay(
            text="Special: !@#$%^&*()",
            animation_in=TextAnimation.NONE,
            animation_out=TextAnimation.NONE,
        )
        result = renderer.render_text_frame(sample_frame, overlay, 0.5)
        assert result.shape == sample_frame.shape

    def test_unicode_text(self, renderer, sample_frame):
        """Test rendering unicode text."""
        overlay = TextOverlay(
            text="Unicode: \u2665 \u2600 \u2601",
            animation_in=TextAnimation.NONE,
            animation_out=TextAnimation.NONE,
        )
        result = renderer.render_text_frame(sample_frame, overlay, 0.5)
        assert result.shape == sample_frame.shape

    def test_multiline_text(self, renderer, sample_frame):
        """Test rendering multiline text."""
        overlay = TextOverlay(
            text="Line 1\nLine 2\nLine 3",
            animation_in=TextAnimation.NONE,
            animation_out=TextAnimation.NONE,
        )
        result = renderer.render_text_frame(sample_frame, overlay, 0.5)
        assert result.shape == sample_frame.shape

    def test_extreme_font_sizes(self, renderer, sample_frame):
        """Test very small and large font sizes."""
        small_overlay = TextOverlay(
            text="Small",
            font_size=8,
            animation_in=TextAnimation.NONE,
            animation_out=TextAnimation.NONE,
        )
        result_small = renderer.render_text_frame(sample_frame.copy(), small_overlay, 0.5)
        assert result_small.shape == sample_frame.shape

        large_overlay = TextOverlay(
            text="Large",
            font_size=200,
            animation_in=TextAnimation.NONE,
            animation_out=TextAnimation.NONE,
        )
        result_large = renderer.render_text_frame(sample_frame.copy(), large_overlay, 0.5)
        assert result_large.shape == sample_frame.shape

    def test_edge_positions(self, renderer, sample_frame):
        """Test text at frame edges."""
        positions = [(0.0, 0.0), (1.0, 1.0), (0.0, 1.0), (1.0, 0.0)]
        for pos in positions:
            overlay = TextOverlay(
                text="Edge",
                position=pos,
                animation_in=TextAnimation.NONE,
                animation_out=TextAnimation.NONE,
            )
            result = renderer.render_text_frame(sample_frame.copy(), overlay, 0.5)
            assert result.shape == sample_frame.shape

    def test_zero_duration_overlay(self, renderer):
        """Test overlay with zero duration."""
        overlay = TextOverlay(text="Zero Duration", duration=0.0)
        assert overlay.duration == 0.0

    def test_negative_progress(self, renderer, sample_frame):
        """Test rendering with negative progress."""
        overlay = TextOverlay(text="Test")
        result = renderer.render_text_frame(sample_frame, overlay, -0.5)
        assert result.shape == sample_frame.shape

    def test_progress_greater_than_one(self, renderer, sample_frame):
        """Test rendering with progress > 1."""
        overlay = TextOverlay(text="Test")
        result = renderer.render_text_frame(sample_frame, overlay, 1.5)
        assert result.shape == sample_frame.shape

    def test_small_frame(self, renderer):
        """Test rendering on very small frame."""
        small_frame = np.zeros((100, 100, 3), dtype=np.uint8)
        overlay = TextOverlay(
            text="Small",
            animation_in=TextAnimation.NONE,
            animation_out=TextAnimation.NONE,
        )
        result = renderer.render_text_frame(small_frame, overlay, 0.5)
        assert result.shape == small_frame.shape

    def test_large_shadow_offset(self, renderer, sample_frame):
        """Test very large shadow offset."""
        overlay = TextOverlay(
            text="Shadow",
            shadow=True,
            shadow_offset=(50, 50),
            animation_in=TextAnimation.NONE,
            animation_out=TextAnimation.NONE,
        )
        result = renderer.render_text_frame(sample_frame, overlay, 0.5)
        assert result.shape == sample_frame.shape
