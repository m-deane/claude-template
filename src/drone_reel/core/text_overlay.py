"""
Text overlay system for drone reels.

Provides animated text overlays with various animation types, auto-placement,
and professional templates like lower thirds and beat-synced captions.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional

import cv2
import numpy as np
from moviepy import CompositeVideoClip, VideoFileClip
from PIL import Image, ImageDraw, ImageFont


class TextAnimation(Enum):
    """Available text animation types."""

    NONE = "none"
    FADE_IN = "fade_in"
    FADE_OUT = "fade_out"
    FADE_IN_OUT = "fade_in_out"
    POP = "pop"  # Scale up quickly then settle
    TYPEWRITER = "typewriter"  # Character by character
    SLIDE_UP = "slide_up"
    SLIDE_DOWN = "slide_down"
    SLIDE_LEFT = "slide_left"
    SLIDE_RIGHT = "slide_right"


@dataclass
class TextOverlay:
    """Configuration for text overlay on video."""

    text: str
    position: tuple[float, float] = (0.5, 0.9)  # Normalized (0-1), center-bottom default
    font: str = "Arial-Bold"
    font_size: int = 48
    color: tuple[int, int, int] = (255, 255, 255)
    background_color: Optional[tuple[int, int, int, int]] = None  # RGBA
    shadow: bool = True
    shadow_color: tuple[int, int, int] = (0, 0, 0)
    shadow_offset: tuple[int, int] = (2, 2)
    animation_in: TextAnimation = TextAnimation.FADE_IN
    animation_out: TextAnimation = TextAnimation.FADE_OUT
    animation_duration: float = 0.3
    start_time: float = 0.0
    duration: float = 3.0
    align: str = "center"  # "left", "center", "right"


class TextRenderer:
    """
    Renders animated text overlays on video clips.

    Supports multiple animation types, auto-placement to avoid busy areas,
    and professional templates for lower thirds and beat-synced captions.
    """

    SAFE_ZONES = {
        "top": {"y_range": (0.05, 0.20), "x_range": (0.05, 0.95)},
        "bottom": {"y_range": (0.80, 0.95), "x_range": (0.05, 0.95)},
        "center": {"y_range": (0.40, 0.60), "x_range": (0.10, 0.90)},
        "lower_third": {"y_range": (0.75, 0.90), "x_range": (0.05, 0.70)},
    }

    def __init__(self):
        """Initialize the text renderer."""
        self._font_cache: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}

    def _get_font(self, font_name: str, font_size: int) -> ImageFont.FreeTypeFont:
        """
        Get or load a font with caching.

        Args:
            font_name: Font name or path
            font_size: Font size in points

        Returns:
            PIL ImageFont object
        """
        cache_key = (font_name, font_size)
        if cache_key not in self._font_cache:
            try:
                font = ImageFont.truetype(font_name, font_size)
            except (OSError, IOError):
                font_candidates = [
                    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                    "arial.ttf",
                    "DejaVuSans-Bold.ttf",
                ]
                font = None
                for candidate in font_candidates:
                    try:
                        font = ImageFont.truetype(candidate, font_size)
                        break
                    except (OSError, IOError):
                        continue
                if font is None:
                    font = ImageFont.load_default()
            self._font_cache[cache_key] = font
        return self._font_cache[cache_key]

    def _ease_out_cubic(self, t: float) -> float:
        """
        Cubic ease-out function.

        Args:
            t: Progress from 0 to 1

        Returns:
            Eased value from 0 to 1
        """
        return 1 - pow(1 - t, 3)

    def _ease_in_out_cubic(self, t: float) -> float:
        """
        Cubic ease-in-out function.

        Args:
            t: Progress from 0 to 1

        Returns:
            Eased value from 0 to 1
        """
        if t < 0.5:
            return 4 * t * t * t
        return 1 - pow(-2 * t + 2, 3) / 2

    def _calculate_animation_progress(
        self, overlay: TextOverlay, current_time: float
    ) -> tuple[float, float]:
        """
        Calculate animation progress for in and out animations.

        Args:
            overlay: TextOverlay configuration
            current_time: Current time in the clip

        Returns:
            Tuple of (in_progress, out_progress) from 0 to 1
        """
        relative_time = current_time - overlay.start_time
        in_progress = 0.0
        out_progress = 0.0

        if overlay.animation_in != TextAnimation.NONE:
            in_progress = min(1.0, relative_time / overlay.animation_duration)

        if overlay.animation_out != TextAnimation.NONE:
            time_to_end = overlay.duration - relative_time
            out_progress = min(1.0, time_to_end / overlay.animation_duration)

        return in_progress, out_progress

    def _apply_fade_animation(
        self, image: Image.Image, progress: float, fade_in: bool = True
    ) -> Image.Image:
        """
        Apply fade animation to image.

        Args:
            image: PIL Image to fade
            progress: Animation progress 0-1
            fade_in: True for fade in, False for fade out

        Returns:
            Faded PIL Image
        """
        if fade_in:
            opacity = progress
        else:
            opacity = progress

        if opacity < 1.0:
            alpha = image.split()[3] if image.mode == "RGBA" else None
            if alpha:
                alpha = alpha.point(lambda p: int(p * opacity))
                image.putalpha(alpha)
        return image

    def _apply_pop_animation(self, scale: float, progress: float) -> float:
        """
        Calculate scale for pop animation.

        Args:
            scale: Current scale
            progress: Animation progress 0-1

        Returns:
            New scale value
        """
        if progress < 1.0:
            eased = self._ease_out_cubic(progress)
            scale = 1.0 + (1.0 - eased) * 0.2
        return scale

    def _apply_slide_animation(
        self,
        position: tuple[int, int],
        frame_size: tuple[int, int],
        text_size: tuple[int, int],
        progress: float,
        direction: str,
    ) -> tuple[int, int]:
        """
        Calculate position for slide animation.

        Args:
            position: Current position (x, y)
            frame_size: Frame dimensions (width, height)
            text_size: Text dimensions (width, height)
            progress: Animation progress 0-1
            direction: Slide direction (up, down, left, right)

        Returns:
            New position (x, y)
        """
        eased = self._ease_in_out_cubic(progress)
        x, y = position

        if direction == "up":
            offset = int((1.0 - eased) * (frame_size[1] + text_size[1]))
            y += offset
        elif direction == "down":
            offset = int((1.0 - eased) * (frame_size[1] + text_size[1]))
            y -= offset
        elif direction == "left":
            offset = int((1.0 - eased) * (frame_size[0] + text_size[0]))
            x += offset
        elif direction == "right":
            offset = int((1.0 - eased) * (frame_size[0] + text_size[0]))
            x -= offset

        return (x, y)

    def render_text_frame(
        self, frame: np.ndarray, overlay: TextOverlay, progress: float
    ) -> np.ndarray:
        """
        Render text onto a single frame with animation state.

        Args:
            frame: NumPy array of the frame (H, W, 3)
            overlay: TextOverlay configuration
            progress: Overall progress through overlay duration (0-1)

        Returns:
            Frame with text rendered
        """
        frame_h, frame_w = frame.shape[:2]
        current_time = overlay.start_time + (progress * overlay.duration)

        in_progress, out_progress = self._calculate_animation_progress(overlay, current_time)

        font = self._get_font(overlay.font, overlay.font_size)

        dummy_img = Image.new("RGBA", (1, 1))
        dummy_draw = ImageDraw.Draw(dummy_img)
        bbox = dummy_draw.textbbox((0, 0), overlay.text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        padding = 20
        img_w = text_w + padding * 2
        img_h = text_h + padding * 2
        text_img = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_img)

        if overlay.background_color:
            bg_bbox = [5, 5, img_w - 5, img_h - 5]
            draw.rectangle(bg_bbox, fill=overlay.background_color)

        text_pos = (padding, padding)

        if overlay.shadow:
            shadow_pos = (
                text_pos[0] + overlay.shadow_offset[0],
                text_pos[1] + overlay.shadow_offset[1],
            )
            shadow_color = overlay.shadow_color + (200,)
            draw.text(shadow_pos, overlay.text, font=font, fill=shadow_color)

        text_color = overlay.color + (255,)
        draw.text(text_pos, overlay.text, font=font, fill=text_color)

        scale = 1.0
        if overlay.animation_in == TextAnimation.POP and in_progress < 1.0:
            scale = self._apply_pop_animation(scale, in_progress)
        elif overlay.animation_out == TextAnimation.POP and out_progress < 1.0:
            scale = self._apply_pop_animation(scale, 1.0 - out_progress)

        if scale != 1.0:
            new_size = (int(img_w * scale), int(img_h * scale))
            text_img = text_img.resize(new_size, Image.LANCZOS)
            img_w, img_h = new_size

        if overlay.animation_in == TextAnimation.FADE_IN and in_progress < 1.0:
            text_img = self._apply_fade_animation(text_img, in_progress, fade_in=True)
        elif overlay.animation_out == TextAnimation.FADE_OUT and out_progress < 1.0:
            text_img = self._apply_fade_animation(text_img, out_progress, fade_in=False)
        elif (
            overlay.animation_in == TextAnimation.FADE_IN_OUT
            or overlay.animation_out == TextAnimation.FADE_IN_OUT
        ):
            if in_progress < 1.0:
                text_img = self._apply_fade_animation(text_img, in_progress, fade_in=True)
            elif out_progress < 1.0:
                text_img = self._apply_fade_animation(text_img, out_progress, fade_in=False)

        pos_x = int(overlay.position[0] * frame_w - img_w / 2)
        pos_y = int(overlay.position[1] * frame_h - img_h / 2)

        if overlay.align == "left":
            pos_x = int(overlay.position[0] * frame_w)
        elif overlay.align == "right":
            pos_x = int(overlay.position[0] * frame_w - img_w)

        slide_animations = {
            TextAnimation.SLIDE_UP: "up",
            TextAnimation.SLIDE_DOWN: "down",
            TextAnimation.SLIDE_LEFT: "left",
            TextAnimation.SLIDE_RIGHT: "right",
        }

        if overlay.animation_in in slide_animations and in_progress < 1.0:
            pos_x, pos_y = self._apply_slide_animation(
                (pos_x, pos_y),
                (frame_w, frame_h),
                (img_w, img_h),
                in_progress,
                slide_animations[overlay.animation_in],
            )
        elif overlay.animation_out in slide_animations and out_progress < 1.0:
            pos_x, pos_y = self._apply_slide_animation(
                (pos_x, pos_y),
                (frame_w, frame_h),
                (img_w, img_h),
                out_progress,
                slide_animations[overlay.animation_out],
            )

        if overlay.animation_in == TextAnimation.TYPEWRITER and in_progress < 1.0:
            visible_chars = max(1, int(len(overlay.text) * in_progress))
            visible_text = overlay.text[:visible_chars]

            text_img = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
            draw = ImageDraw.Draw(text_img)

            if overlay.background_color:
                bg_bbox = [5, 5, img_w - 5, img_h - 5]
                draw.rectangle(bg_bbox, fill=overlay.background_color)

            if overlay.shadow:
                shadow_pos = (
                    text_pos[0] + overlay.shadow_offset[0],
                    text_pos[1] + overlay.shadow_offset[1],
                )
                shadow_color = overlay.shadow_color + (200,)
                draw.text(shadow_pos, visible_text, font=font, fill=shadow_color)

            text_color = overlay.color + (255,)
            draw.text(text_pos, visible_text, font=font, fill=text_color)

        pos_x = max(0, min(pos_x, frame_w - img_w))
        pos_y = max(0, min(pos_y, frame_h - img_h))

        frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        frame_pil.paste(text_img, (pos_x, pos_y), text_img)
        frame = cv2.cvtColor(np.array(frame_pil), cv2.COLOR_RGB2BGR)

        return frame

    def apply_overlay_to_clip(
        self, clip: VideoFileClip, overlay: TextOverlay
    ) -> VideoFileClip:
        """
        Apply animated text overlay to video clip.

        Args:
            clip: MoviePy VideoFileClip
            overlay: TextOverlay configuration

        Returns:
            VideoFileClip with text overlay applied
        """

        def make_frame(get_frame, t):
            frame = get_frame(t)
            if overlay.start_time <= t <= overlay.start_time + overlay.duration:
                progress = (t - overlay.start_time) / overlay.duration
                frame = self.render_text_frame(frame, overlay, progress)
            return frame

        return clip.transform(make_frame)

    def apply_multiple_overlays(
        self, clip: VideoFileClip, overlays: list[TextOverlay]
    ) -> VideoFileClip:
        """
        Apply multiple text overlays to clip.

        Args:
            clip: MoviePy VideoFileClip
            overlays: List of TextOverlay configurations

        Returns:
            VideoFileClip with all overlays applied
        """

        def make_frame(get_frame, t):
            frame = get_frame(t)
            for overlay in overlays:
                if overlay.start_time <= t <= overlay.start_time + overlay.duration:
                    progress = (t - overlay.start_time) / overlay.duration
                    frame = self.render_text_frame(frame, overlay, progress)
            return frame

        return clip.transform(make_frame)

    def auto_place_text(
        self, frame: np.ndarray, text: str, preferred_zone: str = "bottom"
    ) -> tuple[float, float]:
        """
        Find optimal text placement avoiding busy areas.

        Args:
            frame: NumPy array of the frame
            text: Text to place
            preferred_zone: Preferred zone name from SAFE_ZONES

        Returns:
            Tuple of normalized position (x, y) in range 0-1
        """
        if preferred_zone not in self.SAFE_ZONES:
            preferred_zone = "bottom"

        zone = self.SAFE_ZONES[preferred_zone]
        frame_h, frame_w = frame.shape[:2]

        y_start = int(zone["y_range"][0] * frame_h)
        y_end = int(zone["y_range"][1] * frame_h)
        x_start = int(zone["x_range"][0] * frame_w)
        x_end = int(zone["x_range"][1] * frame_w)

        region = frame[y_start:y_end, x_start:x_end]

        gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)

        block_h = (y_end - y_start) // 3
        block_w = (x_end - x_start) // 3

        min_variance = float("inf")
        best_block = (1, 1)

        for i in range(3):
            for j in range(3):
                block_y_start = i * block_h
                block_y_end = min((i + 1) * block_h, gray.shape[0])
                block_x_start = j * block_w
                block_x_end = min((j + 1) * block_w, gray.shape[1])

                block = gray[block_y_start:block_y_end, block_x_start:block_x_end]
                variance = np.var(block)

                if variance < min_variance:
                    min_variance = variance
                    best_block = (i, j)

        block_center_y = y_start + (best_block[0] + 0.5) * block_h
        block_center_x = x_start + (best_block[1] + 0.5) * block_w

        norm_x = block_center_x / frame_w
        norm_y = block_center_y / frame_h

        return (norm_x, norm_y)

    def create_lower_third(
        self,
        title: str,
        subtitle: Optional[str] = None,
        style: str = "modern",
    ) -> list[TextOverlay]:
        """
        Create professional lower third text overlays.

        Args:
            title: Main title text
            subtitle: Optional subtitle text
            style: Style preset ("modern", "minimal", "bold")

        Returns:
            List of TextOverlay configurations for lower third
        """
        overlays = []

        if style == "modern":
            title_overlay = TextOverlay(
                text=title,
                position=(0.1, 0.85),
                font="Arial-Bold",
                font_size=56,
                color=(255, 255, 255),
                background_color=(0, 0, 0, 180),
                shadow=True,
                shadow_offset=(3, 3),
                animation_in=TextAnimation.SLIDE_LEFT,
                animation_out=TextAnimation.SLIDE_LEFT,
                animation_duration=0.4,
                align="left",
            )
            overlays.append(title_overlay)

            if subtitle:
                subtitle_overlay = TextOverlay(
                    text=subtitle,
                    position=(0.1, 0.92),
                    font="Arial-Bold",
                    font_size=36,
                    color=(200, 200, 200),
                    background_color=(0, 0, 0, 120),
                    shadow=True,
                    shadow_offset=(2, 2),
                    animation_in=TextAnimation.SLIDE_LEFT,
                    animation_out=TextAnimation.SLIDE_LEFT,
                    animation_duration=0.4,
                    start_time=0.1,
                    align="left",
                )
                overlays.append(subtitle_overlay)

        elif style == "minimal":
            title_overlay = TextOverlay(
                text=title,
                position=(0.5, 0.88),
                font="Arial-Bold",
                font_size=48,
                color=(255, 255, 255),
                background_color=None,
                shadow=True,
                shadow_offset=(2, 2),
                animation_in=TextAnimation.FADE_IN,
                animation_out=TextAnimation.FADE_OUT,
                animation_duration=0.5,
                align="center",
            )
            overlays.append(title_overlay)

            if subtitle:
                subtitle_overlay = TextOverlay(
                    text=subtitle,
                    position=(0.5, 0.94),
                    font="Arial-Bold",
                    font_size=32,
                    color=(220, 220, 220),
                    background_color=None,
                    shadow=True,
                    shadow_offset=(1, 1),
                    animation_in=TextAnimation.FADE_IN,
                    animation_out=TextAnimation.FADE_OUT,
                    animation_duration=0.5,
                    start_time=0.15,
                    align="center",
                )
                overlays.append(subtitle_overlay)

        elif style == "bold":
            title_overlay = TextOverlay(
                text=title,
                position=(0.5, 0.85),
                font="Arial-Bold",
                font_size=72,
                color=(255, 215, 0),
                background_color=(0, 0, 0, 200),
                shadow=True,
                shadow_offset=(4, 4),
                shadow_color=(0, 0, 0),
                animation_in=TextAnimation.POP,
                animation_out=TextAnimation.FADE_OUT,
                animation_duration=0.5,
                align="center",
            )
            overlays.append(title_overlay)

            if subtitle:
                subtitle_overlay = TextOverlay(
                    text=subtitle,
                    position=(0.5, 0.93),
                    font="Arial-Bold",
                    font_size=42,
                    color=(255, 255, 255),
                    background_color=(50, 50, 50, 180),
                    shadow=True,
                    shadow_offset=(2, 2),
                    animation_in=TextAnimation.FADE_IN,
                    animation_out=TextAnimation.FADE_OUT,
                    animation_duration=0.4,
                    start_time=0.2,
                    align="center",
                )
                overlays.append(subtitle_overlay)

        else:
            title_overlay = TextOverlay(text=title)
            overlays.append(title_overlay)
            if subtitle:
                subtitle_overlay = TextOverlay(text=subtitle, position=(0.5, 0.95))
                overlays.append(subtitle_overlay)

        return overlays

    def create_beat_synced_captions(
        self,
        captions: list[str],
        beat_times: list[float],
        duration_per_caption: float = 2.0,
    ) -> list[TextOverlay]:
        """
        Create captions that appear on beat.

        Args:
            captions: List of caption texts
            beat_times: List of beat timestamps
            duration_per_caption: How long each caption stays visible

        Returns:
            List of TextOverlay configurations synced to beats
        """
        overlays = []

        num_overlays = min(len(captions), len(beat_times))

        for i in range(num_overlays):
            animation_types = [
                TextAnimation.POP,
                TextAnimation.FADE_IN,
                TextAnimation.SLIDE_UP,
            ]
            animation = animation_types[i % len(animation_types)]

            overlay = TextOverlay(
                text=captions[i],
                position=(0.5, 0.85),
                font="Arial-Bold",
                font_size=56,
                color=(255, 255, 255),
                background_color=(0, 0, 0, 160),
                shadow=True,
                shadow_offset=(3, 3),
                animation_in=animation,
                animation_out=TextAnimation.FADE_OUT,
                animation_duration=0.3,
                start_time=beat_times[i],
                duration=duration_per_caption,
                align="center",
            )
            overlays.append(overlay)

        return overlays
