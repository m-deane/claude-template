"""
Video reframing for social media aspect ratios.

Handles automatic reframing from landscape drone footage to vertical
9:16 format for Instagram Reels, TikTok, and YouTube Shorts.
"""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Callable, Optional

import cv2
import numpy as np
from moviepy import VideoFileClip


class AspectRatio(Enum):
    """Common social media aspect ratios."""

    VERTICAL_9_16 = (9, 16)  # Instagram Reels, TikTok, Shorts
    SQUARE_1_1 = (1, 1)  # Instagram Feed
    LANDSCAPE_16_9 = (16, 9)  # YouTube, standard HD
    PORTRAIT_4_5 = (4, 5)  # Instagram Portrait
    CINEMATIC_21_9 = (21, 9)  # Ultra-wide cinematic


class ReframeMode(Enum):
    """Reframing strategies."""

    CENTER = "center"  # Center crop
    SMART = "smart"  # AI-based subject tracking
    PAN = "pan"  # Slow pan across the frame
    THIRDS = "thirds"  # Follow rule of thirds
    CUSTOM = "custom"  # Custom focal point


@dataclass
class ReframeSettings:
    """Settings for video reframing."""

    target_ratio: AspectRatio = AspectRatio.VERTICAL_9_16
    mode: ReframeMode = ReframeMode.SMART
    output_width: int = 1080
    pan_speed: float = 0.1  # For PAN mode, pixels per frame
    focal_point: tuple[float, float] = (0.5, 0.5)  # For CUSTOM mode (0-1 normalized)
    smooth_tracking: bool = True
    tracking_smoothness: float = 0.3  # Lower = smoother, more lag


class Reframer:
    """
    Reframes video content for different aspect ratios.

    Supports multiple strategies including center crop, smart tracking,
    panning, and rule-of-thirds based framing.
    """

    def __init__(self, settings: Optional[ReframeSettings] = None):
        """
        Initialize the reframer.

        Args:
            settings: ReframeSettings for reframing behavior
        """
        self.settings = settings or ReframeSettings()
        self._saliency = None
        self._tracker_history: list[tuple[float, float]] = []

    def calculate_output_dimensions(
        self, input_width: int, input_height: int
    ) -> tuple[int, int]:
        """
        Calculate output dimensions maintaining target aspect ratio.

        Args:
            input_width: Source video width
            input_height: Source video height

        Returns:
            Tuple of (output_width, output_height)
        """
        target_w, target_h = self.settings.target_ratio.value
        target_aspect = target_w / target_h

        output_width = self.settings.output_width
        output_height = int(output_width / target_aspect)

        return output_width, output_height

    def calculate_crop_region(
        self,
        frame: np.ndarray,
        output_width: int,
        output_height: int,
        frame_index: int = 0,
        total_frames: int = 1,
    ) -> tuple[int, int, int, int]:
        """
        Calculate the crop region for a frame.

        Args:
            frame: Input frame as numpy array
            output_width: Target output width
            output_height: Target output height
            frame_index: Current frame index (for PAN mode)
            total_frames: Total frames (for PAN mode)

        Returns:
            Tuple of (x, y, width, height) for crop region
        """
        h, w = frame.shape[:2]

        input_aspect = w / h
        output_aspect = output_width / output_height

        if input_aspect > output_aspect:
            crop_h = h
            crop_w = int(h * output_aspect)
        else:
            crop_w = w
            crop_h = int(w / output_aspect)

        if self.settings.mode == ReframeMode.CENTER:
            x = (w - crop_w) // 2
            y = (h - crop_h) // 2

        elif self.settings.mode == ReframeMode.SMART:
            focal_x, focal_y = self._detect_focal_point(frame)
            x = int(focal_x * w - crop_w / 2)
            y = int(focal_y * h - crop_h / 2)

            if self.settings.smooth_tracking and self._tracker_history:
                prev_x, prev_y = self._tracker_history[-1]
                smooth = self.settings.tracking_smoothness
                x = int(prev_x + (x - prev_x) * smooth)
                y = int(prev_y + (y - prev_y) * smooth)

            self._tracker_history.append((x, y))
            if len(self._tracker_history) > 30:
                self._tracker_history.pop(0)

        elif self.settings.mode == ReframeMode.PAN:
            progress = frame_index / max(total_frames - 1, 1)
            max_x = w - crop_w
            x = int(progress * max_x)
            y = (h - crop_h) // 2

        elif self.settings.mode == ReframeMode.THIRDS:
            focal_x, focal_y = self._detect_focal_point(frame)
            third_x = round(focal_x * 2) / 2
            third_y = round(focal_y * 2) / 2
            x = int(third_x * (w - crop_w))
            y = int(third_y * (h - crop_h))

        elif self.settings.mode == ReframeMode.CUSTOM:
            focal_x, focal_y = self.settings.focal_point
            x = int(focal_x * (w - crop_w))
            y = int(focal_y * (h - crop_h))

        else:
            x = (w - crop_w) // 2
            y = (h - crop_h) // 2

        x = max(0, min(x, w - crop_w))
        y = max(0, min(y, h - crop_h))

        return x, y, crop_w, crop_h

    def _detect_focal_point(self, frame: np.ndarray) -> tuple[float, float]:
        """
        Detect the focal point of interest in a frame.

        Uses saliency detection to find the most visually interesting
        region of the frame.

        Args:
            frame: Input frame

        Returns:
            Tuple of (x, y) normalized coordinates (0-1)
        """
        if self._saliency is None:
            self._saliency = cv2.saliency.StaticSaliencySpectralResidual_create()

        small_frame = cv2.resize(frame, (320, 180))

        success, saliency_map = self._saliency.computeSaliency(small_frame)

        if not success:
            return 0.5, 0.5

        saliency_map = (saliency_map * 255).astype(np.uint8)

        blurred = cv2.GaussianBlur(saliency_map, (21, 21), 0)
        _, max_val, _, max_loc = cv2.minMaxLoc(blurred)

        focal_x = max_loc[0] / 320
        focal_y = max_loc[1] / 180

        focal_x = 0.3 + focal_x * 0.4
        focal_y = 0.3 + focal_y * 0.4

        return focal_x, focal_y

    def reframe_video(
        self,
        input_path: Path,
        output_path: Path,
        progress_callback: Optional[Callable[[float], None]] = None,
    ) -> Path:
        """
        Reframe an entire video file.

        Args:
            input_path: Path to input video
            output_path: Path for output video
            progress_callback: Optional callback for progress updates

        Returns:
            Path to the reframed video
        """
        self._tracker_history = []

        clip = VideoFileClip(str(input_path))

        output_w, output_h = self.calculate_output_dimensions(clip.w, clip.h)

        total_frames = int(clip.duration * clip.fps)
        frame_count = [0]

        def reframe_frame(get_frame, t):
            frame = get_frame(t)

            x, y, crop_w, crop_h = self.calculate_crop_region(
                frame, output_w, output_h, frame_count[0], total_frames
            )

            cropped = frame[y : y + crop_h, x : x + crop_w]

            resized = cv2.resize(cropped, (output_w, output_h))

            frame_count[0] += 1

            if progress_callback and frame_count[0] % 30 == 0:
                progress_callback(frame_count[0] / total_frames)

            return resized

        reframed_clip = clip.transform(reframe_frame)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        reframed_clip.write_videofile(
            str(output_path),
            codec="libx264",
            audio_codec="aac",
            logger=None,
        )

        clip.close()
        reframed_clip.close()

        if progress_callback:
            progress_callback(1.0)

        return output_path

    def reframe_frame(
        self,
        frame: np.ndarray,
        frame_index: int = 0,
        total_frames: int = 1,
    ) -> np.ndarray:
        """
        Reframe a single frame.

        Args:
            frame: Input frame as numpy array
            frame_index: Current frame index
            total_frames: Total number of frames

        Returns:
            Reframed frame
        """
        h, w = frame.shape[:2]
        output_w, output_h = self.calculate_output_dimensions(w, h)

        x, y, crop_w, crop_h = self.calculate_crop_region(
            frame, output_w, output_h, frame_index, total_frames
        )

        cropped = frame[y : y + crop_h, x : x + crop_w]
        resized = cv2.resize(cropped, (output_w, output_h))

        return resized

    def reset_tracking(self):
        """Reset the tracking history for a new video."""
        self._tracker_history = []


def create_vertical_reframer(
    mode: ReframeMode = ReframeMode.SMART,
    output_width: int = 1080,
) -> Reframer:
    """
    Create a reframer configured for vertical 9:16 output.

    Args:
        mode: Reframing strategy to use
        output_width: Output video width (height calculated automatically)

    Returns:
        Configured Reframer instance
    """
    settings = ReframeSettings(
        target_ratio=AspectRatio.VERTICAL_9_16,
        mode=mode,
        output_width=output_width,
    )
    return Reframer(settings)
