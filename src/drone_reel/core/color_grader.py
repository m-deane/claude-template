"""
Color grading presets and adjustments for video.

Provides cinematic color grading presets optimized for drone footage
including warm tones, cool grades, vintage looks, and more.
Supports LUTs, tone curves, selective color adjustments, and GPU acceleration.
"""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Callable, Optional

import cv2
import numpy as np
from moviepy import VideoFileClip
from scipy.interpolate import CubicSpline


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
class SelectiveColorAdjustments:
    """Adjustments for specific color ranges."""

    red_hue: float = 0.0  # -180 to 180
    red_sat: float = 0.0  # -100 to 100
    red_lum: float = 0.0  # -100 to 100

    orange_hue: float = 0.0
    orange_sat: float = 0.0
    orange_lum: float = 0.0

    yellow_hue: float = 0.0
    yellow_sat: float = 0.0
    yellow_lum: float = 0.0

    green_hue: float = 0.0
    green_sat: float = 0.0
    green_lum: float = 0.0

    cyan_hue: float = 0.0
    cyan_sat: float = 0.0
    cyan_lum: float = 0.0

    blue_hue: float = 0.0
    blue_sat: float = 0.0
    blue_lum: float = 0.0

    purple_hue: float = 0.0
    purple_sat: float = 0.0
    purple_lum: float = 0.0

    magenta_hue: float = 0.0
    magenta_sat: float = 0.0
    magenta_lum: float = 0.0


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
    selective_color: Optional[SelectiveColorAdjustments] = None


@dataclass
class ToneCurve:
    """Tone curve defined by control points."""

    red_points: list[tuple[float, float]] = field(default_factory=lambda: [(0, 0), (255, 255)])
    green_points: list[tuple[float, float]] = field(default_factory=lambda: [(0, 0), (255, 255)])
    blue_points: list[tuple[float, float]] = field(default_factory=lambda: [(0, 0), (255, 255)])


class ColorGrader:
    """
    Applies color grading to video frames and clips.

    Supports preset grades optimized for drone footage as well as
    custom manual adjustments, LUTs, tone curves, and GPU acceleration.
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
        lut_path: Optional[Path] = None,
        tone_curve: Optional[ToneCurve] = None,
        use_gpu: bool = False,
    ):
        """
        Initialize the color grader.

        Args:
            preset: Color preset to use
            adjustments: Optional manual adjustments (overrides preset)
            lut_path: Optional path to .cube LUT file
            tone_curve: Optional tone curve for RGB channels
            use_gpu: Enable GPU acceleration if available
        """
        self.preset = preset
        if adjustments:
            self.adjustments = adjustments
        else:
            self.adjustments = self.PRESET_ADJUSTMENTS.get(preset, ColorAdjustments())

        self.lut: Optional[np.ndarray] = None
        if lut_path:
            self.lut = self.load_lut(lut_path)

        self.tone_curve = tone_curve
        self._tone_curve_luts: Optional[tuple[np.ndarray, np.ndarray, np.ndarray]] = None
        if tone_curve:
            self._tone_curve_luts = self._build_tone_curve_luts(tone_curve)

        self.use_gpu = use_gpu and self._check_gpu_available()
        self._frame_index = 0

    def _check_gpu_available(self) -> bool:
        """Check if CUDA GPU is available."""
        try:
            return cv2.cuda.getCudaEnabledDeviceCount() > 0
        except (AttributeError, cv2.error):
            return False

    def load_lut(self, lut_path: Path) -> np.ndarray:
        """
        Load a 3D LUT from a .cube file.

        Args:
            lut_path: Path to .cube LUT file

        Returns:
            3D LUT as numpy array with shape (size, size, size, 3)
        """
        with open(lut_path, 'r') as f:
            lines = f.readlines()

        lut_size = None
        lut_data = []

        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            if line.startswith('LUT_3D_SIZE'):
                lut_size = int(line.split()[1])
                continue

            if line.startswith('TITLE') or line.startswith('DOMAIN_'):
                continue

            parts = line.split()
            if len(parts) == 3:
                try:
                    r, g, b = map(float, parts)
                    lut_data.append([r, g, b])
                except ValueError:
                    continue

        if not lut_size:
            raise ValueError("LUT file does not specify LUT_3D_SIZE")

        if len(lut_data) != lut_size ** 3:
            raise ValueError(f"Expected {lut_size ** 3} LUT entries, got {len(lut_data)}")

        lut = np.array(lut_data, dtype=np.float32)
        lut = lut.reshape((lut_size, lut_size, lut_size, 3))

        return lut

    def _apply_lut(self, frame: np.ndarray, lut: np.ndarray) -> np.ndarray:
        """
        Apply 3D LUT using trilinear interpolation.

        Args:
            frame: Input frame (BGR, float32, 0-255)
            lut: 3D LUT array

        Returns:
            Frame with LUT applied
        """
        lut_size = lut.shape[0]
        scale = (lut_size - 1) / 255.0

        b, g, r = frame[:, :, 0], frame[:, :, 1], frame[:, :, 2]

        b_scaled = np.clip(b * scale, 0, lut_size - 1.001)
        g_scaled = np.clip(g * scale, 0, lut_size - 1.001)
        r_scaled = np.clip(r * scale, 0, lut_size - 1.001)

        b0, g0, r0 = b_scaled.astype(np.int32), g_scaled.astype(np.int32), r_scaled.astype(np.int32)
        b1, g1, r1 = np.minimum(b0 + 1, lut_size - 1), np.minimum(g0 + 1, lut_size - 1), np.minimum(r0 + 1, lut_size - 1)

        b_frac = b_scaled - b0
        g_frac = g_scaled - g0
        r_frac = r_scaled - r0

        c000 = lut[r0, g0, b0]
        c001 = lut[r0, g0, b1]
        c010 = lut[r0, g1, b0]
        c011 = lut[r0, g1, b1]
        c100 = lut[r1, g0, b0]
        c101 = lut[r1, g0, b1]
        c110 = lut[r1, g1, b0]
        c111 = lut[r1, g1, b1]

        c00 = c000 * (1 - b_frac[:, :, np.newaxis]) + c001 * b_frac[:, :, np.newaxis]
        c01 = c010 * (1 - b_frac[:, :, np.newaxis]) + c011 * b_frac[:, :, np.newaxis]
        c10 = c100 * (1 - b_frac[:, :, np.newaxis]) + c101 * b_frac[:, :, np.newaxis]
        c11 = c110 * (1 - b_frac[:, :, np.newaxis]) + c111 * b_frac[:, :, np.newaxis]

        c0 = c00 * (1 - g_frac[:, :, np.newaxis]) + c01 * g_frac[:, :, np.newaxis]
        c1 = c10 * (1 - g_frac[:, :, np.newaxis]) + c11 * g_frac[:, :, np.newaxis]

        result = c0 * (1 - r_frac[:, :, np.newaxis]) + c1 * r_frac[:, :, np.newaxis]

        return result * 255.0

    def _build_tone_curve_luts(self, tone_curve: ToneCurve) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Build lookup tables from tone curve control points.

        Args:
            tone_curve: Tone curve with control points

        Returns:
            Tuple of (red_lut, green_lut, blue_lut) each as 256-element arrays
        """
        def build_channel_lut(points: list[tuple[float, float]]) -> np.ndarray:
            points = sorted(points, key=lambda p: p[0])
            x_vals = np.array([p[0] for p in points])
            y_vals = np.array([p[1] for p in points])

            if len(points) < 2:
                return np.arange(256, dtype=np.float32)

            if len(points) == 2:
                interp_func = lambda x: np.interp(x, x_vals, y_vals)
            else:
                spline = CubicSpline(x_vals, y_vals, bc_type='clamped')
                interp_func = spline

            x_full = np.arange(256, dtype=np.float32)
            y_full = interp_func(x_full)
            return np.clip(y_full, 0, 255).astype(np.float32)

        red_lut = build_channel_lut(tone_curve.red_points)
        green_lut = build_channel_lut(tone_curve.green_points)
        blue_lut = build_channel_lut(tone_curve.blue_points)

        return red_lut, green_lut, blue_lut

    def apply_curve(self, frame: np.ndarray) -> np.ndarray:
        """
        Apply tone curve to frame.

        Args:
            frame: Input frame (BGR, float32, 0-255)

        Returns:
            Frame with curve applied
        """
        if not self._tone_curve_luts:
            return frame

        red_lut, green_lut, blue_lut = self._tone_curve_luts

        result = frame.copy()
        result[:, :, 0] = blue_lut[np.clip(frame[:, :, 0].astype(np.int32), 0, 255)]
        result[:, :, 1] = green_lut[np.clip(frame[:, :, 1].astype(np.int32), 0, 255)]
        result[:, :, 2] = red_lut[np.clip(frame[:, :, 2].astype(np.int32), 0, 255)]

        return result

    def _apply_selective_color(self, frame: np.ndarray, selective: SelectiveColorAdjustments) -> np.ndarray:
        """
        Apply selective color adjustments to specific hue ranges.

        Args:
            frame: Input frame (BGR, float32, 0-255)
            selective: Selective color adjustments

        Returns:
            Frame with selective color applied
        """
        hsv = cv2.cvtColor(frame.astype(np.uint8), cv2.COLOR_BGR2HSV).astype(np.float32)
        lab = cv2.cvtColor(frame.astype(np.uint8), cv2.COLOR_BGR2LAB).astype(np.float32)

        hue = hsv[:, :, 0]
        sat = hsv[:, :, 1]
        lum = lab[:, :, 0]

        color_ranges = {
            'red': (0, 15, 345, 360, selective.red_hue, selective.red_sat, selective.red_lum),
            'orange': (16, 45, None, None, selective.orange_hue, selective.orange_sat, selective.orange_lum),
            'yellow': (46, 75, None, None, selective.yellow_hue, selective.yellow_sat, selective.yellow_lum),
            'green': (76, 165, None, None, selective.green_hue, selective.green_sat, selective.green_lum),
            'cyan': (166, 195, None, None, selective.cyan_hue, selective.cyan_sat, selective.cyan_lum),
            'blue': (196, 255, None, None, selective.blue_hue, selective.blue_sat, selective.blue_lum),
            'purple': (256, 285, None, None, selective.purple_hue, selective.purple_sat, selective.purple_lum),
            'magenta': (286, 344, None, None, selective.magenta_hue, selective.magenta_sat, selective.magenta_lum),
        }

        for color_name, params in color_ranges.items():
            start1, end1, start2, end2, hue_adj, sat_adj, lum_adj = params

            if start2 is not None:
                mask = ((hue >= start1) & (hue <= end1)) | ((hue >= start2) & (hue <= end2))
            else:
                mask = (hue >= start1) & (hue <= end1)

            if hue_adj != 0:
                hsv[:, :, 0][mask] = np.clip(hue[mask] + hue_adj / 2, 0, 360)

            if sat_adj != 0:
                sat_factor = 1 + sat_adj / 100
                hsv[:, :, 1][mask] = np.clip(sat[mask] * sat_factor, 0, 255)

            if lum_adj != 0:
                lum_adjustment = lum_adj * 2.55
                lab[:, :, 0][mask] = np.clip(lum[mask] + lum_adjustment, 0, 255)

        result_from_hsv = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)
        result_from_lab = cv2.cvtColor(lab.astype(np.uint8), cv2.COLOR_LAB2BGR).astype(np.float32)

        result = cv2.addWeighted(result_from_hsv, 0.7, result_from_lab, 0.3, 0)

        return result

    def grade_frame(self, frame: np.ndarray, frame_index: Optional[int] = None) -> np.ndarray:
        """
        Apply color grading to a single frame.

        Args:
            frame: Input frame as BGR numpy array
            frame_index: Optional frame index for temporal consistency

        Returns:
            Color graded frame
        """
        if frame_index is not None:
            self._frame_index = frame_index

        if self.use_gpu:
            return self._grade_frame_gpu(frame)
        else:
            return self._grade_frame_cpu(frame)

    def _grade_frame_cpu(self, frame: np.ndarray) -> np.ndarray:
        """CPU implementation of frame grading."""
        result = frame.astype(np.float32)

        if self.lut is not None:
            result = self._apply_lut(result, self.lut)

        if self._tone_curve_luts is not None:
            result = self.apply_curve(result)

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

        if self.adjustments.selective_color is not None:
            result = self._apply_selective_color(result, self.adjustments.selective_color)

        if self.adjustments.grain > 0:
            result = self._apply_grain(result, self.adjustments.grain)

        if self.preset == ColorPreset.TEAL_ORANGE:
            result = self._apply_teal_orange_grade(result)

        result = np.clip(result, 0, 255).astype(np.uint8)
        self._frame_index += 1

        return result

    def _grade_frame_gpu(self, frame: np.ndarray) -> np.ndarray:
        """
        GPU-accelerated implementation of frame grading.

        Falls back to CPU for operations not supported on GPU.
        """
        try:
            gpu_frame = cv2.cuda_GpuMat()
            gpu_frame.upload(frame)

            if self.adjustments.brightness != 0:
                adjustment = self.adjustments.brightness * 2.55
                gpu_frame = cv2.cuda.add(gpu_frame, (adjustment, adjustment, adjustment, 0))

            if self.adjustments.contrast != 0:
                factor = (100 + self.adjustments.contrast) / 100
                gpu_frame = cv2.cuda.subtract(gpu_frame, (128, 128, 128, 0))
                gpu_frame = cv2.cuda.multiply(gpu_frame, (factor, factor, factor, 1))
                gpu_frame = cv2.cuda.add(gpu_frame, (128, 128, 128, 0))

            result = gpu_frame.download()

            if self.lut is not None:
                result = self._apply_lut(result.astype(np.float32), self.lut)

            if self._tone_curve_luts is not None:
                result = self.apply_curve(result.astype(np.float32))

            if self.adjustments.temperature != 0:
                result = self._adjust_temperature(result.astype(np.float32), self.adjustments.temperature)

            if self.adjustments.tint != 0:
                result = self._adjust_tint(result.astype(np.float32), self.adjustments.tint)

            if self.adjustments.saturation != 0:
                result = self._adjust_saturation(result.astype(np.float32), self.adjustments.saturation)

            if self.adjustments.vibrance != 0:
                result = self._adjust_vibrance(result.astype(np.float32), self.adjustments.vibrance)

            if self.adjustments.shadows != 0:
                result = self._adjust_shadows(result.astype(np.float32), self.adjustments.shadows)

            if self.adjustments.highlights != 0:
                result = self._adjust_highlights(result.astype(np.float32), self.adjustments.highlights)

            if self.adjustments.fade > 0:
                result = self._apply_fade(result.astype(np.float32), self.adjustments.fade)

            if self.adjustments.selective_color is not None:
                result = self._apply_selective_color(result.astype(np.float32), self.adjustments.selective_color)

            if self.adjustments.grain > 0:
                result = self._apply_grain(result.astype(np.float32), self.adjustments.grain)

            if self.preset == ColorPreset.TEAL_ORANGE:
                result = self._apply_teal_orange_grade(result.astype(np.float32))

            result = np.clip(result, 0, 255).astype(np.uint8)
            self._frame_index += 1

            return result

        except (cv2.error, AttributeError):
            return self._grade_frame_cpu(frame)

    def grade_frame_preview(self, frame: np.ndarray, scale: float = 0.25) -> np.ndarray:
        """
        Apply color grading at reduced resolution for fast preview.

        Args:
            frame: Input frame as BGR numpy array
            scale: Scale factor for preview (default 0.25 = 25% size)

        Returns:
            Color graded preview frame at reduced resolution
        """
        h, w = frame.shape[:2]
        preview_h, preview_w = int(h * scale), int(w * scale)

        small_frame = cv2.resize(frame, (preview_w, preview_h), interpolation=cv2.INTER_LINEAR)

        graded_small = self.grade_frame(small_frame)

        return graded_small

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
        """
        Adjust shadow levels using LAB color space for better color preservation.
        """
        lab = cv2.cvtColor(frame.astype(np.uint8), cv2.COLOR_BGR2LAB).astype(np.float32)
        l_channel = lab[:, :, 0]

        shadow_mask = 1 - (l_channel / 255)
        shadow_mask = shadow_mask ** 2

        adjustment = shadow_mask * (amount / 100) * 50
        lab[:, :, 0] = np.clip(l_channel + adjustment, 0, 255)

        return cv2.cvtColor(lab.astype(np.uint8), cv2.COLOR_LAB2BGR).astype(np.float32)

    def _adjust_highlights(self, frame: np.ndarray, amount: float) -> np.ndarray:
        """
        Adjust highlight levels using LAB color space for better color preservation.
        """
        lab = cv2.cvtColor(frame.astype(np.uint8), cv2.COLOR_BGR2LAB).astype(np.float32)
        l_channel = lab[:, :, 0]

        highlight_mask = l_channel / 255
        highlight_mask = highlight_mask ** 2

        adjustment = highlight_mask * (amount / 100) * 50
        lab[:, :, 0] = np.clip(l_channel + adjustment, 0, 255)

        return cv2.cvtColor(lab.astype(np.uint8), cv2.COLOR_LAB2BGR).astype(np.float32)

    def _apply_fade(self, frame: np.ndarray, amount: float) -> np.ndarray:
        """Apply fade effect (lift blacks)."""
        lift = amount / 100 * 30
        return frame + lift * (1 - frame / 255)

    def _apply_grain(self, frame: np.ndarray, amount: float) -> np.ndarray:
        """
        Apply film grain effect with temporal coherence and film-like characteristics.
        """
        np.random.seed(self._frame_index % 100000)

        h, w = frame.shape[:2]
        grain_h, grain_w = h // 2, w // 2

        noise = np.random.normal(0, amount / 100 * 25, (grain_h, grain_w))

        noise_upscaled = cv2.resize(noise, (w, h), interpolation=cv2.INTER_LINEAR)

        lab = cv2.cvtColor(frame.astype(np.uint8), cv2.COLOR_BGR2LAB).astype(np.float32)
        luminance = lab[:, :, 0] / 255.0

        midtone_mask = 1 - np.abs(luminance - 0.5) * 2
        midtone_mask = midtone_mask ** 0.5

        weighted_noise = noise_upscaled * midtone_mask

        result = frame.copy()
        result[:, :, 0] += weighted_noise
        result[:, :, 1] += weighted_noise
        result[:, :, 2] += weighted_noise

        return result

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
        video_bitrate: str = "15M",
        audio_bitrate: str = "192k",
    ) -> Path:
        """
        Apply color grading to an entire video file.

        Args:
            input_path: Path to input video
            output_path: Path for output video
            progress_callback: Optional callback for progress updates
            video_bitrate: Video bitrate (e.g., "8M", "15M", "25M")
            audio_bitrate: Audio bitrate (e.g., "128k", "192k")

        Returns:
            Path to the graded video
        """
        clip = VideoFileClip(str(input_path))

        total_frames = int(clip.duration * clip.fps)
        frame_count = [0]

        def grade_frame_func(get_frame, t):
            frame = get_frame(t)
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            graded_bgr = self.grade_frame(frame_bgr, frame_index=frame_count[0])
            graded_rgb = cv2.cvtColor(graded_bgr, cv2.COLOR_BGR2RGB)

            frame_count[0] += 1
            if progress_callback and frame_count[0] % 30 == 0:
                progress_callback(frame_count[0] / total_frames)

            return graded_rgb

        graded_clip = clip.transform(grade_frame_func)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        graded_clip.write_videofile(
            str(output_path),
            codec="libx264",
            audio_codec="aac",
            bitrate=video_bitrate,
            audio_bitrate=audio_bitrate,
            ffmpeg_params=["-pix_fmt", "yuv420p"],
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
