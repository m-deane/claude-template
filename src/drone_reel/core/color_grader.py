"""
Color grading presets and adjustments for video.

Provides cinematic color grading presets optimized for drone footage
including warm tones, cool grades, vintage looks, and more.
"""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Callable, Optional

import cv2
import numpy as np
from moviepy.editor import VideoFileClip


class ColorPreset(Enum):
    """Available color grading presets."""

    NONE = "none"
    CINEMATIC = "cinematic"
    WARM_SUNSET = "warm_sunset"
    COOL_BLUE = "cool_blue"
    VINTAGE = "vintage"
    HIGH_CONTRAST = "high_contrast"
    MUTED = "muted"
    VIBRANT = "vibrant"
    TEAL_ORANGE = "teal_orange"
    BLACK_WHITE = "black_white"
    DRONE_AERIAL = "drone_aerial"


@dataclass
class ColorAdjustments:
    """Manual color adjustment parameters."""

    brightness: float = 0.0  # -100 to 100
    contrast: float = 0.0  # -100 to 100
    saturation: float = 0.0  # -100 to 100
    temperature: float = 0.0  # -100 (cool) to 100 (warm)
    tint: float = 0.0  # -100 (green) to 100 (magenta)
    shadows: float = 0.0  # -100 to 100
    highlights: float = 0.0  # -100 to 100
    vibrance: float = 0.0  # -100 to 100
    fade: float = 0.0  # 0 to 100 (lifts blacks)
    grain: float = 0.0  # 0 to 100


class ColorGrader:
    """
    Applies color grading to video frames and clips.

    Supports preset grades optimized for drone footage as well as
    custom manual adjustments.
    """

    PRESET_ADJUSTMENTS: dict[ColorPreset, ColorAdjustments] = {
        ColorPreset.NONE: ColorAdjustments(),
        ColorPreset.CINEMATIC: ColorAdjustments(
            contrast=15,
            saturation=-10,
            temperature=5,
            shadows=-10,
            highlights=-5,
            fade=5,
        ),
        ColorPreset.WARM_SUNSET: ColorAdjustments(
            brightness=5,
            contrast=10,
            saturation=15,
            temperature=30,
            tint=5,
            vibrance=20,
        ),
        ColorPreset.COOL_BLUE: ColorAdjustments(
            contrast=10,
            saturation=5,
            temperature=-25,
            shadows=5,
            highlights=-10,
        ),
        ColorPreset.VINTAGE: ColorAdjustments(
            contrast=-5,
            saturation=-20,
            temperature=10,
            fade=20,
            grain=15,
        ),
        ColorPreset.HIGH_CONTRAST: ColorAdjustments(
            contrast=35,
            saturation=10,
            shadows=-15,
            highlights=10,
        ),
        ColorPreset.MUTED: ColorAdjustments(
            contrast=-10,
            saturation=-30,
            fade=15,
        ),
        ColorPreset.VIBRANT: ColorAdjustments(
            contrast=15,
            saturation=30,
            vibrance=25,
            highlights=-5,
        ),
        ColorPreset.TEAL_ORANGE: ColorAdjustments(
            contrast=10,
            saturation=5,
            temperature=15,
            tint=-10,
        ),
        ColorPreset.BLACK_WHITE: ColorAdjustments(
            saturation=-100,
            contrast=20,
        ),
        ColorPreset.DRONE_AERIAL: ColorAdjustments(
            brightness=5,
            contrast=12,
            saturation=8,
            temperature=8,
            vibrance=15,
            shadows=10,
            highlights=-8,
        ),
    }

    def __init__(
        self,
        preset: ColorPreset = ColorPreset.NONE,
        adjustments: Optional[ColorAdjustments] = None,
    ):
        """
        Initialize the color grader.

        Args:
            preset: Color preset to use
            adjustments: Optional manual adjustments (overrides preset)
        """
        self.preset = preset
        if adjustments:
            self.adjustments = adjustments
        else:
            self.adjustments = self.PRESET_ADJUSTMENTS.get(preset, ColorAdjustments())

    def grade_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Apply color grading to a single frame.

        Args:
            frame: Input frame as BGR numpy array

        Returns:
            Color graded frame
        """
        result = frame.astype(np.float32)

        if self.adjustments.brightness != 0:
            result = self._adjust_brightness(result, self.adjustments.brightness)

        if self.adjustments.contrast != 0:
            result = self._adjust_contrast(result, self.adjustments.contrast)

        if self.adjustments.temperature != 0:
            result = self._adjust_temperature(result, self.adjustments.temperature)

        if self.adjustments.tint != 0:
            result = self._adjust_tint(result, self.adjustments.tint)

        if self.adjustments.saturation != 0:
            result = self._adjust_saturation(result, self.adjustments.saturation)

        if self.adjustments.vibrance != 0:
            result = self._adjust_vibrance(result, self.adjustments.vibrance)

        if self.adjustments.shadows != 0:
            result = self._adjust_shadows(result, self.adjustments.shadows)

        if self.adjustments.highlights != 0:
            result = self._adjust_highlights(result, self.adjustments.highlights)

        if self.adjustments.fade > 0:
            result = self._apply_fade(result, self.adjustments.fade)

        if self.adjustments.grain > 0:
            result = self._apply_grain(result, self.adjustments.grain)

        if self.preset == ColorPreset.TEAL_ORANGE:
            result = self._apply_teal_orange_grade(result)

        result = np.clip(result, 0, 255).astype(np.uint8)

        return result

    def _adjust_brightness(self, frame: np.ndarray, amount: float) -> np.ndarray:
        """Adjust frame brightness."""
        adjustment = amount * 2.55
        return frame + adjustment

    def _adjust_contrast(self, frame: np.ndarray, amount: float) -> np.ndarray:
        """Adjust frame contrast."""
        factor = (100 + amount) / 100
        return (frame - 128) * factor + 128

    def _adjust_saturation(self, frame: np.ndarray, amount: float) -> np.ndarray:
        """Adjust color saturation."""
        hsv = cv2.cvtColor(frame.astype(np.uint8), cv2.COLOR_BGR2HSV).astype(np.float32)
        factor = 1 + amount / 100
        hsv[:, :, 1] = hsv[:, :, 1] * factor
        hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
        return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)

    def _adjust_vibrance(self, frame: np.ndarray, amount: float) -> np.ndarray:
        """
        Adjust vibrance (saturation that protects skin tones).

        Increases saturation more on less-saturated pixels.
        """
        hsv = cv2.cvtColor(frame.astype(np.uint8), cv2.COLOR_BGR2HSV).astype(np.float32)
        saturation = hsv[:, :, 1]

        mask = 1 - (saturation / 255)
        adjustment = mask * (amount / 100) * 50

        hsv[:, :, 1] = np.clip(saturation + adjustment, 0, 255)
        return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)

    def _adjust_temperature(self, frame: np.ndarray, amount: float) -> np.ndarray:
        """Adjust color temperature (warm/cool)."""
        adjustment = amount / 100 * 30
        frame[:, :, 0] = frame[:, :, 0] - adjustment  # Blue
        frame[:, :, 2] = frame[:, :, 2] + adjustment  # Red
        return frame

    def _adjust_tint(self, frame: np.ndarray, amount: float) -> np.ndarray:
        """Adjust tint (green/magenta)."""
        adjustment = amount / 100 * 20
        frame[:, :, 1] = frame[:, :, 1] - adjustment  # Green
        return frame

    def _adjust_shadows(self, frame: np.ndarray, amount: float) -> np.ndarray:
        """Adjust shadow levels."""
        hsv = cv2.cvtColor(frame.astype(np.uint8), cv2.COLOR_BGR2HSV).astype(np.float32)
        v = hsv[:, :, 2]

        shadow_mask = 1 - (v / 255)
        shadow_mask = shadow_mask**2

        adjustment = shadow_mask * (amount / 100) * 50
        hsv[:, :, 2] = np.clip(v + adjustment, 0, 255)

        return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)

    def _adjust_highlights(self, frame: np.ndarray, amount: float) -> np.ndarray:
        """Adjust highlight levels."""
        hsv = cv2.cvtColor(frame.astype(np.uint8), cv2.COLOR_BGR2HSV).astype(np.float32)
        v = hsv[:, :, 2]

        highlight_mask = v / 255
        highlight_mask = highlight_mask**2

        adjustment = highlight_mask * (amount / 100) * 50
        hsv[:, :, 2] = np.clip(v + adjustment, 0, 255)

        return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)

    def _apply_fade(self, frame: np.ndarray, amount: float) -> np.ndarray:
        """Apply fade effect (lift blacks)."""
        lift = amount / 100 * 30
        return frame + lift * (1 - frame / 255)

    def _apply_grain(self, frame: np.ndarray, amount: float) -> np.ndarray:
        """Apply film grain effect."""
        noise = np.random.normal(0, amount / 100 * 25, frame.shape)
        return frame + noise

    def _apply_teal_orange_grade(self, frame: np.ndarray) -> np.ndarray:
        """Apply teal and orange color grade popular in cinema."""
        hsv = cv2.cvtColor(frame.astype(np.uint8), cv2.COLOR_BGR2HSV).astype(np.float32)

        hue = hsv[:, :, 0]

        orange_mask = ((hue >= 0) & (hue <= 30)) | ((hue >= 150) & (hue <= 180))
        teal_mask = (hue >= 75) & (hue <= 105)

        hsv[:, :, 1][orange_mask] = np.clip(hsv[:, :, 1][orange_mask] * 1.2, 0, 255)
        hsv[:, :, 1][teal_mask] = np.clip(hsv[:, :, 1][teal_mask] * 1.15, 0, 255)

        mid_tones = ~orange_mask & ~teal_mask
        hsv[:, :, 0][mid_tones] = np.where(
            hsv[:, :, 0][mid_tones] < 90, 15, 90  # Push towards orange or teal
        )

        return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)

    def grade_video(
        self,
        input_path: Path,
        output_path: Path,
        progress_callback: Optional[Callable[[float], None]] = None,
    ) -> Path:
        """
        Apply color grading to an entire video file.

        Args:
            input_path: Path to input video
            output_path: Path for output video
            progress_callback: Optional callback for progress updates

        Returns:
            Path to the graded video
        """
        clip = VideoFileClip(str(input_path))

        total_frames = int(clip.duration * clip.fps)
        frame_count = [0]

        def grade_frame_func(get_frame, t):
            frame = get_frame(t)
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            graded_bgr = self.grade_frame(frame_bgr)
            graded_rgb = cv2.cvtColor(graded_bgr, cv2.COLOR_BGR2RGB)

            frame_count[0] += 1
            if progress_callback and frame_count[0] % 30 == 0:
                progress_callback(frame_count[0] / total_frames)

            return graded_rgb

        graded_clip = clip.fl(grade_frame_func)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        graded_clip.write_videofile(
            str(output_path),
            codec="libx264",
            audio_codec="aac",
            logger=None,
        )

        clip.close()
        graded_clip.close()

        if progress_callback:
            progress_callback(1.0)

        return output_path


def get_preset_names() -> list[str]:
    """Get list of available preset names."""
    return [preset.value for preset in ColorPreset]


def create_grader_from_preset(preset_name: str) -> ColorGrader:
    """
    Create a ColorGrader from a preset name string.

    Args:
        preset_name: Name of the preset (e.g., 'cinematic', 'warm_sunset')

    Returns:
        Configured ColorGrader instance
    """
    try:
        preset = ColorPreset(preset_name.lower())
    except ValueError:
        preset = ColorPreset.NONE

    return ColorGrader(preset=preset)
