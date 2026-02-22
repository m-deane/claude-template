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
    # Time-of-day presets
    GOLDEN_HOUR = "golden_hour"
    BLUE_HOUR = "blue_hour"
    HARSH_MIDDAY = "harsh_midday"
    OVERCAST = "overcast"
    NIGHT_CITY = "night_city"
    # Terrain-aware presets
    OCEAN_COASTAL = "ocean_coastal"
    FOREST_JUNGLE = "forest_jungle"
    URBAN_CITY = "urban_city"
    DESERT_ARID = "desert_arid"
    SNOW_MOUNTAIN = "snow_mountain"
    AUTUMN_FOLIAGE = "autumn_foliage"
    # Cinematic film emulation
    KODAK_2383 = "kodak_2383"
    FUJIFILM_3513 = "fujifilm_3513"
    TECHNICOLOR_2STRIP = "technicolor_2strip"
    # Social media trend presets
    DESATURATED_MOODY = "desaturated_moody"
    WARM_PASTEL = "warm_pastel"
    CYBERPUNK_NEON = "cyberpunk_neon"
    HYPER_NATURAL = "hyper_natural"
    FILM_EMULATION = "film_emulation"


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
            contrast=14,
            saturation=10,
            temperature=8,
            vibrance=15,
            shadows=10,
            highlights=-8,
        ),
        # --- Time-of-day presets ---
        ColorPreset.GOLDEN_HOUR: ColorAdjustments(
            temperature=30,
            highlights=-50,
            vibrance=30,
            saturation=8,
            contrast=8,
            selective_color=SelectiveColorAdjustments(
                orange_sat=25, yellow_sat=20,
            ),
        ),
        ColorPreset.BLUE_HOUR: ColorAdjustments(
            temperature=-40,
            saturation=10,
            contrast=12,
            shadows=-15,
            highlights=-20,
            selective_color=SelectiveColorAdjustments(
                blue_sat=30, cyan_sat=15,
            ),
        ),
        ColorPreset.HARSH_MIDDAY: ColorAdjustments(
            highlights=-90,
            shadows=70,
            vibrance=50,
            contrast=5,
            selective_color=SelectiveColorAdjustments(
                blue_sat=30, green_sat=-15,
            ),
        ),
        ColorPreset.OVERCAST: ColorAdjustments(
            temperature=-8,
            contrast=8,
            saturation=-8,
            vibrance=10,
            selective_color=SelectiveColorAdjustments(
                green_sat=10,
            ),
        ),
        ColorPreset.NIGHT_CITY: ColorAdjustments(
            brightness=-7,
            contrast=40,
            saturation=5,
            selective_color=SelectiveColorAdjustments(
                orange_sat=30, blue_sat=25,
            ),
        ),
        # --- Terrain-aware presets ---
        ColorPreset.OCEAN_COASTAL: ColorAdjustments(
            contrast=10,
            vibrance=15,
            selective_color=SelectiveColorAdjustments(
                cyan_hue=-5, cyan_sat=20,
                orange_sat=25, yellow_sat=25,
            ),
        ),
        ColorPreset.FOREST_JUNGLE: ColorAdjustments(
            shadows=40,
            contrast=8,
            selective_color=SelectiveColorAdjustments(
                green_hue=-5, green_sat=-12,
            ),
        ),
        ColorPreset.URBAN_CITY: ColorAdjustments(
            contrast=30,
            temperature=-5,
            shadows=-10,
            selective_color=SelectiveColorAdjustments(
                orange_sat=20, red_sat=15,
            ),
        ),
        ColorPreset.DESERT_ARID: ColorAdjustments(
            temperature=20,
            highlights=-60,
            selective_color=SelectiveColorAdjustments(
                orange_sat=-12, blue_sat=20,
            ),
        ),
        ColorPreset.SNOW_MOUNTAIN: ColorAdjustments(
            temperature=8,
            highlights=-70,
            vibrance=20,
            selective_color=SelectiveColorAdjustments(
                blue_sat=-25, cyan_sat=-15,
            ),
        ),
        ColorPreset.AUTUMN_FOLIAGE: ColorAdjustments(
            temperature=15,
            vibrance=10,
            selective_color=SelectiveColorAdjustments(
                orange_sat=30, orange_hue=-5,
                red_sat=20, green_sat=-20,
                blue_sat=20,
            ),
        ),
        # --- Cinematic film emulation ---
        ColorPreset.KODAK_2383: ColorAdjustments(
            contrast=12,
            temperature=8,
            shadows=-8,
            highlights=-15,
            fade=8,
        ),
        ColorPreset.FUJIFILM_3513: ColorAdjustments(
            contrast=10,
            temperature=-10,
            tint=5,
            shadows=-5,
            highlights=-10,
        ),
        ColorPreset.TECHNICOLOR_2STRIP: ColorAdjustments(
            contrast=15,
            temperature=15,
            saturation=-15,
            selective_color=SelectiveColorAdjustments(
                red_sat=20, orange_sat=15,
                blue_sat=-30,
            ),
        ),
        # --- Social media trend presets ---
        ColorPreset.DESATURATED_MOODY: ColorAdjustments(
            saturation=-35,
            contrast=35,
            shadows=-20,
            selective_color=SelectiveColorAdjustments(
                blue_sat=15, cyan_sat=10,
            ),
        ),
        ColorPreset.WARM_PASTEL: ColorAdjustments(
            contrast=-25,
            saturation=-20,
            temperature=15,
            tint=5,
            fade=40,
        ),
        ColorPreset.CYBERPUNK_NEON: ColorAdjustments(
            brightness=-10,
            contrast=30,
            shadows=-25,
            selective_color=SelectiveColorAdjustments(
                cyan_sat=50, magenta_sat=40, orange_sat=25,
            ),
        ),
        ColorPreset.HYPER_NATURAL: ColorAdjustments(
            brightness=1,
            contrast=7,
            saturation=3,
            vibrance=8,
        ),
        ColorPreset.FILM_EMULATION: ColorAdjustments(
            contrast=5,
            temperature=8,
            fade=20,
            grain=10,
            shadows=5,
        ),
    }

    def __init__(
        self,
        preset: ColorPreset = ColorPreset.NONE,
        adjustments: Optional[ColorAdjustments] = None,
        lut_path: Optional[Path] = None,
        tone_curve: Optional[ToneCurve] = None,
        use_gpu: bool = False,
        intensity: float = 1.0,
        vignette_strength: float = 0.0,
        halation_strength: float = 0.0,
        chromatic_aberration_strength: float = 0.0,
        input_colorspace: str = "rec709",
        auto_wb: bool = False,
        denoise_strength: float = 0.0,
        haze_strength: float = 0.0,
        gnd_sky_strength: float = 0.0,
    ):
        """
        Initialize the color grader.

        Args:
            preset: Color preset to use
            adjustments: Optional manual adjustments (overrides preset)
            lut_path: Optional path to .cube LUT file
            tone_curve: Optional tone curve for RGB channels
            use_gpu: Enable GPU acceleration if available
            intensity: Scale factor for color adjustments (0.0-1.0, default 1.0)
            vignette_strength: Radial edge darkening (0.0-1.0, default 0.0 = off)
            halation_strength: Warm bloom around highlights (0.0-1.0, default 0.0 = off)
            chromatic_aberration_strength: RGB edge fringing (0.0-1.0, default 0.0 = off)
            input_colorspace: Input footage colorspace (rec709, dlog, dlog_m, slog3)
            auto_wb: Enable gray world auto white balance
            denoise_strength: Spatial denoising strength (0.0-1.0, default 0.0 = off)
            haze_strength: Atmospheric haze overlay (0.0-1.0, default 0.0 = off)
            gnd_sky_strength: Graduated ND sky darkening (0.0-1.0, default 0.0 = off)
        """
        self.preset = preset
        self.intensity = max(0.0, min(1.0, intensity))
        if adjustments:
            self.adjustments = adjustments
        else:
            self.adjustments = self.PRESET_ADJUSTMENTS.get(preset, ColorAdjustments())

        if self.intensity != 1.0:
            self.adjustments = ColorAdjustments(
                brightness=self.adjustments.brightness * self.intensity,
                contrast=self.adjustments.contrast * self.intensity,
                saturation=self.adjustments.saturation * self.intensity,
                temperature=self.adjustments.temperature * self.intensity,
                tint=self.adjustments.tint * self.intensity,
                shadows=self.adjustments.shadows * self.intensity,
                highlights=self.adjustments.highlights * self.intensity,
                vibrance=self.adjustments.vibrance * self.intensity,
                fade=self.adjustments.fade * self.intensity,
                grain=self.adjustments.grain * self.intensity,
                selective_color=self.adjustments.selective_color,
            )

        self.lut: Optional[np.ndarray] = None
        if lut_path:
            self.lut = self.load_lut(lut_path)

        self.tone_curve = tone_curve
        self._tone_curve_luts: Optional[tuple[np.ndarray, np.ndarray, np.ndarray]] = None
        if tone_curve:
            self._tone_curve_luts = self._build_tone_curve_luts(tone_curve)

        self.use_gpu = use_gpu and self._check_gpu_available()
        self._frame_index = 0
        self.vignette_strength = max(0.0, min(1.0, vignette_strength))
        self._vignette_mask_cache: Optional[tuple[int, int, np.ndarray]] = None
        self.halation_strength = max(0.0, min(1.0, halation_strength))
        self.chromatic_aberration_strength = max(0.0, min(1.0, chromatic_aberration_strength))
        self.input_colorspace = input_colorspace.lower()
        self.auto_wb = auto_wb
        self.denoise_strength = max(0.0, min(1.0, denoise_strength))
        self.haze_strength = max(0.0, min(1.0, haze_strength))
        self.gnd_sky_strength = max(0.0, min(1.0, gnd_sky_strength))
        self._dlog_normalized = False
        self._reference_histogram: Optional[list] = None

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

        # Clamp input to valid range before scaling
        frame_clamped = np.clip(frame, 0, 255)
        b, g, r = frame_clamped[:, :, 0], frame_clamped[:, :, 1], frame_clamped[:, :, 2]

        b_scaled = np.clip(b * scale, 0, lut_size - 1 - 1e-6)
        g_scaled = np.clip(g * scale, 0, lut_size - 1 - 1e-6)
        r_scaled = np.clip(r * scale, 0, lut_size - 1 - 1e-6)

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

        return np.clip(result * 255.0, 0, 255)

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

        # OpenCV uint8 HSV: hue is 0-180 (not 0-360), saturation 0-255
        color_ranges = {
            'red': (0, 8, 173, 180, selective.red_hue, selective.red_sat, selective.red_lum),
            'orange': (9, 23, None, None, selective.orange_hue, selective.orange_sat, selective.orange_lum),
            'yellow': (24, 38, None, None, selective.yellow_hue, selective.yellow_sat, selective.yellow_lum),
            'green': (39, 83, None, None, selective.green_hue, selective.green_sat, selective.green_lum),
            'cyan': (84, 98, None, None, selective.cyan_hue, selective.cyan_sat, selective.cyan_lum),
            'blue': (99, 128, None, None, selective.blue_hue, selective.blue_sat, selective.blue_lum),
            'purple': (129, 143, None, None, selective.purple_hue, selective.purple_sat, selective.purple_lum),
            'magenta': (144, 172, None, None, selective.magenta_hue, selective.magenta_sat, selective.magenta_lum),
        }

        for color_name, params in color_ranges.items():
            start1, end1, start2, end2, hue_adj, sat_adj, lum_adj = params

            if start2 is not None:
                mask = ((hue >= start1) & (hue <= end1)) | ((hue >= start2) & (hue <= end2))
            else:
                mask = (hue >= start1) & (hue <= end1)

            if hue_adj != 0:
                # hue_adj is -180..180 degrees, /2 converts to 0-180 HSV scale
                hsv[:, :, 0][mask] = np.clip(hue[mask] + hue_adj / 2, 0, 180)

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
        """CPU implementation of frame grading.

        Batches color space conversions to avoid redundant BGR->HSV->BGR and
        BGR->LAB->BGR round-trips. Saturation + vibrance + teal_orange share
        a single HSV pass; shadows + highlights share a single LAB pass.
        """
        result = frame.astype(np.float32)
        applied_adjustments = False

        # Phase -2: D-Log / S-Log normalization (must happen before all grading)
        if self.input_colorspace != "rec709":
            result = self._normalize_dlog(result)
            applied_adjustments = True

        # Phase -1: Auto white balance (before creative grading)
        if self.auto_wb:
            result = self._apply_auto_wb(result)
            applied_adjustments = True

        # Phase -0.5: Auto color match (histogram matching to reference)
        if self._reference_histogram is not None:
            result = self._apply_auto_color_match(result)
            applied_adjustments = True

        # Phase -0.25: Noise reduction (before grading to avoid amplifying noise)
        if self.denoise_strength > 0:
            result = self._apply_denoise(result, self.denoise_strength)
            applied_adjustments = True

        # Phase 0: LUT and tone curves (direct pixel mapping)
        if self.lut is not None:
            result = self._apply_lut(result, self.lut)
            applied_adjustments = True

        if self._tone_curve_luts is not None:
            result = self.apply_curve(result)
            applied_adjustments = True

        # Phase 0.5: Automatic shadow lift (LAB space, before preset adjustments).
        # Only active when a non-NONE preset is in use and intensity is non-zero,
        # so the NONE/identity path is unaffected.
        if self.intensity > 0 and self.preset != ColorPreset.NONE:
            result_norm = result / 255.0
            lab_tmp = cv2.cvtColor(result_norm.astype(np.float32), cv2.COLOR_BGR2LAB)
            lab_tmp = self._auto_shadow_lift(lab_tmp)
            result = np.clip(
                cv2.cvtColor(lab_tmp, cv2.COLOR_LAB2BGR) * 255.0, 0, 255
            )
            applied_adjustments = True

        # Phase 1: Direct BGR operations (no color space conversion needed)
        if self.adjustments.brightness != 0:
            result = self._adjust_brightness(result, self.adjustments.brightness)
            applied_adjustments = True

        if self.adjustments.contrast != 0:
            result = self._adjust_contrast(result, self.adjustments.contrast)
            applied_adjustments = True

        if self.adjustments.temperature != 0:
            result = self._adjust_temperature(result, self.adjustments.temperature)
            applied_adjustments = True

        if self.adjustments.tint != 0:
            result = self._adjust_tint(result, self.adjustments.tint)
            applied_adjustments = True

        # Phase 2: Batched HSV operations (single BGR->HSV->BGR round-trip)
        needs_hsv = (
            self.adjustments.saturation != 0
            or self.adjustments.vibrance != 0
            or self.preset == ColorPreset.TEAL_ORANGE
        )
        if needs_hsv:
            result = self._apply_hsv_batch(result)
            applied_adjustments = True

        # Phase 3: Batched LAB operations (single BGR->LAB->BGR round-trip)
        needs_lab = (
            self.adjustments.shadows != 0
            or self.adjustments.highlights != 0
        )
        if needs_lab:
            result = self._apply_lab_batch(result)
            applied_adjustments = True

        # Phase 4: Remaining operations
        if self.adjustments.fade > 0:
            result = self._apply_fade(result, self.adjustments.fade)
            applied_adjustments = True

        if self.adjustments.selective_color is not None:
            result = self._apply_selective_color(result, self.adjustments.selective_color)
            applied_adjustments = True

        if self.adjustments.grain > 0:
            result = self._apply_grain(result, self.adjustments.grain)
            applied_adjustments = True

        # Phase 5: Vignette (radial edge darkening)
        if self.vignette_strength > 0:
            result = self._apply_vignette(result, self.vignette_strength)
            applied_adjustments = True

        # Phase 6: Halation / bloom (warm glow around highlights)
        if self.halation_strength > 0:
            result = self._apply_halation(result, self.halation_strength)
            applied_adjustments = True

        # Phase 7: Chromatic aberration (RGB edge fringing)
        if self.chromatic_aberration_strength > 0:
            result = self._apply_chromatic_aberration(result, self.chromatic_aberration_strength)
            applied_adjustments = True

        # Phase 8: Atmospheric haze (aerial depth effect)
        if self.haze_strength > 0:
            result = self._apply_haze(result, self.haze_strength)
            applied_adjustments = True

        # Phase 9: GND sky correction (graduated exposure darkening)
        if self.gnd_sky_strength > 0:
            result = self._apply_gnd_sky(result, self.gnd_sky_strength)
            applied_adjustments = True

        # Apply subtle dithering to mask banding in gradients (only if adjustments were made)
        if applied_adjustments:
            result = self._apply_dither(result)

        result = np.clip(result, 0, 255).astype(np.uint8)
        self._frame_index += 1

        return result

    def _apply_hsv_batch(self, frame: np.ndarray) -> np.ndarray:
        """Apply saturation, vibrance, and teal_orange in a single HSV pass.

        Replaces individual _adjust_saturation + _adjust_vibrance +
        _apply_teal_orange_grade calls that each did their own BGR->HSV->BGR
        conversion.
        """
        frame_normalized = frame / 255.0
        hsv = cv2.cvtColor(frame_normalized.astype(np.float32), cv2.COLOR_BGR2HSV)

        if self.adjustments.saturation != 0:
            factor = 1 + self.adjustments.saturation / 100
            hsv[:, :, 1] = np.clip(hsv[:, :, 1] * factor, 0, 1)

        if self.adjustments.vibrance != 0:
            saturation = hsv[:, :, 1]
            mask = 1 - saturation
            adjustment = mask * (self.adjustments.vibrance / 100) * 0.5
            hsv[:, :, 1] = np.clip(saturation + adjustment, 0, 1)

        if self.preset == ColorPreset.TEAL_ORANGE:
            hue = hsv[:, :, 0]
            orange_mask = ((hue >= 0) & (hue <= 60)) | ((hue >= 300) & (hue <= 360))
            teal_mask = (hue >= 150) & (hue <= 210)
            hsv[:, :, 1][orange_mask] = np.clip(hsv[:, :, 1][orange_mask] * 1.2, 0, 1)
            hsv[:, :, 1][teal_mask] = np.clip(hsv[:, :, 1][teal_mask] * 1.15, 0, 1)
            mid_tones = ~orange_mask & ~teal_mask
            hsv[:, :, 0][mid_tones] = np.where(
                hsv[:, :, 0][mid_tones] < 180, 30, 180
            )

        result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return result * 255.0

    def _auto_shadow_lift(self, frame_lab: np.ndarray) -> np.ndarray:
        """Lift underexposed shadows in float32 LAB space (L channel 0-100).

        Analyzes mean luminance of the frame. If the frame has underexposed
        regions (mean L < 80), pixels in the bottom 30% of the luminance
        range (L < 30) are brightened by up to 15 units using a smooth curve
        that tapers off towards midtones, leaving highlights untouched.

        Args:
            frame_lab: Float32 LAB frame with L channel in 0-100 range.

        Returns:
            LAB frame with shadow pixels lifted; original array modified in place.
        """
        l_channel = frame_lab[:, :, 0]
        mean_l = float(l_channel.mean())

        if mean_l >= 80.0:
            # Frame is well-exposed; no adjustment needed.
            return frame_lab

        # Shadow threshold: bottom 30% of the 0-100 L range = pixels with L < 30.
        shadow_threshold = 30.0
        lift_amount = 15.0

        shadow_pixels = l_channel < shadow_threshold

        # Smooth weight: 1.0 at L=0, tapering to 0.0 at L=shadow_threshold.
        # Using a quadratic curve so the lift is gentle near the threshold.
        weight = ((shadow_threshold - l_channel) / shadow_threshold) ** 2
        weight = np.where(shadow_pixels, weight, 0.0)

        l_channel_lifted = np.clip(l_channel + weight * lift_amount, 0.0, 100.0)
        frame_lab[:, :, 0] = l_channel_lifted

        return frame_lab

    def _apply_lab_batch(self, frame: np.ndarray) -> np.ndarray:
        """Apply shadows and highlights in a single LAB pass.

        Replaces individual _adjust_shadows + _adjust_highlights calls that
        each did their own BGR->LAB->BGR conversion.
        """
        frame_normalized = frame / 255.0
        lab = cv2.cvtColor(frame_normalized.astype(np.float32), cv2.COLOR_BGR2LAB)
        l_channel = lab[:, :, 0]

        if self.adjustments.shadows != 0:
            shadow_mask = 1 - (l_channel / 100)
            shadow_mask = shadow_mask ** 2
            shadow_adj = shadow_mask * (self.adjustments.shadows / 100) * 25
            l_channel = np.clip(l_channel + shadow_adj, 0, 100)

        if self.adjustments.highlights != 0:
            highlight_mask = l_channel / 100
            highlight_mask = highlight_mask ** 2
            highlight_adj = highlight_mask * (self.adjustments.highlights / 100) * 25
            l_channel = np.clip(l_channel + highlight_adj, 0, 100)

        lab[:, :, 0] = l_channel
        result = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        return np.clip(result * 255.0, 0, 255)

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
        """Adjust color saturation using high-precision float32 conversion."""
        # Convert to 0-1 range for float32 HSV conversion (avoids uint8 banding)
        frame_normalized = frame / 255.0
        hsv = cv2.cvtColor(frame_normalized.astype(np.float32), cv2.COLOR_BGR2HSV)
        # In float32 HSV: H is 0-360, S is 0-1, V is 0-1
        factor = 1 + amount / 100
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * factor, 0, 1)
        result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return result * 255.0

    def _adjust_vibrance(self, frame: np.ndarray, amount: float) -> np.ndarray:
        """
        Adjust vibrance (saturation that protects skin tones).

        Increases saturation more on less-saturated pixels.
        Uses high-precision float32 conversion to avoid banding.
        """
        # Convert to 0-1 range for float32 HSV conversion
        frame_normalized = frame / 255.0
        hsv = cv2.cvtColor(frame_normalized.astype(np.float32), cv2.COLOR_BGR2HSV)
        # In float32 HSV: S is 0-1
        saturation = hsv[:, :, 1]

        # Mask based on current saturation (less saturated pixels get more boost)
        mask = 1 - saturation
        adjustment = mask * (amount / 100) * 0.5  # Scaled for 0-1 range

        hsv[:, :, 1] = np.clip(saturation + adjustment, 0, 1)
        result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return result * 255.0

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
        Uses high-precision float32 conversion to avoid banding.
        """
        # Convert to 0-1 range for float32 LAB conversion
        frame_normalized = frame / 255.0
        lab = cv2.cvtColor(frame_normalized.astype(np.float32), cv2.COLOR_BGR2LAB)
        # In float32 LAB: L is 0-100, a/b are roughly -127 to 127
        l_channel = lab[:, :, 0]

        # Shadow mask targets darker areas (low L values)
        shadow_mask = 1 - (l_channel / 100)
        shadow_mask = shadow_mask ** 2

        # Adjustment scaled for 0-100 L range
        adjustment = shadow_mask * (amount / 100) * 25
        lab[:, :, 0] = np.clip(l_channel + adjustment, 0, 100)

        result = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        return np.clip(result * 255.0, 0, 255)

    def _adjust_highlights(self, frame: np.ndarray, amount: float) -> np.ndarray:
        """
        Adjust highlight levels using LAB color space for better color preservation.
        Uses high-precision float32 conversion to avoid banding.
        """
        # Convert to 0-1 range for float32 LAB conversion
        frame_normalized = frame / 255.0
        lab = cv2.cvtColor(frame_normalized.astype(np.float32), cv2.COLOR_BGR2LAB)
        # In float32 LAB: L is 0-100
        l_channel = lab[:, :, 0]

        # Highlight mask targets brighter areas (high L values)
        highlight_mask = l_channel / 100
        highlight_mask = highlight_mask ** 2

        # Adjustment scaled for 0-100 L range
        adjustment = highlight_mask * (amount / 100) * 25
        lab[:, :, 0] = np.clip(l_channel + adjustment, 0, 100)

        result = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        return np.clip(result * 255.0, 0, 255)

    def _apply_fade(self, frame: np.ndarray, amount: float) -> np.ndarray:
        """Apply fade effect (lift blacks)."""
        lift = amount / 100 * 30
        return frame + lift * (1 - frame / 255)

    def _apply_grain(self, frame: np.ndarray, amount: float) -> np.ndarray:
        """
        Apply film grain with temporal variation, luminance weighting, and configurable size.

        Generates per-frame unique noise weighted by a midtone bell curve (grain is most
        visible in midtones, less in shadows/highlights). Grain is slightly blurred to
        simulate photochemical grain structure rather than digital pixel noise.
        """
        # Use frame_index XOR with spatial hash for unique-per-frame grain
        seed = (self._frame_index * 2654435761) % (2**31)
        rng = np.random.RandomState(seed)

        h, w = frame.shape[:2]
        # Generate grain at half res then upscale for organic feel
        grain_h, grain_w = max(h // 2, 1), max(w // 2, 1)

        # Gaussian noise scaled by amount
        noise = rng.normal(0, amount / 100 * 25, (grain_h, grain_w)).astype(np.float32)

        # Slight blur for photochemical grain structure (not pixel-sharp)
        ksize = 3 if amount < 50 else 5
        noise = cv2.GaussianBlur(noise, (ksize, ksize), 0)

        noise_upscaled = cv2.resize(noise, (w, h), interpolation=cv2.INTER_LINEAR)

        # Luminance-weighted: bell curve peaking at midtones
        gray = np.mean(frame, axis=2) / 255.0
        midtone_mask = 1.0 - np.abs(gray - 0.5) * 2.0
        midtone_mask = np.power(midtone_mask, 0.5)

        # Also suppress grain in very dark regions (< 10%) to preserve clean blacks
        shadow_suppression = np.clip(gray / 0.1, 0, 1)
        weighted_noise = noise_upscaled * midtone_mask * shadow_suppression

        result = frame.copy()
        result[:, :, 0] += weighted_noise
        result[:, :, 1] += weighted_noise
        result[:, :, 2] += weighted_noise

        return result

    def _apply_dither(self, frame: np.ndarray, strength: float = 1.5) -> np.ndarray:
        """
        Apply subtle ordered dithering to mask color banding in gradients.

        Uses Bayer-matrix ordered dithering which is spatially deterministic
        (same pixel always gets same dither value) and won't cause temporal
        flickering between frames.

        Args:
            frame: Input frame (float32, 0-255)
            strength: Dithering strength (default 1.5, clamped to 0-10)

        Returns:
            Frame with dithering applied
        """
        strength = max(0.0, min(strength, 10.0))
        if strength == 0.0:
            return frame

        h, w = frame.shape[:2]

        # 4x4 Bayer matrix for ordered dithering (normalized to -0.5 to 0.5)
        bayer_4x4 = np.array([
            [ 0,  8,  2, 10],
            [12,  4, 14,  6],
            [ 3, 11,  1,  9],
            [15,  7, 13,  5]
        ], dtype=np.float32) / 16.0 - 0.5

        # Tile the Bayer matrix to cover the frame
        tiles_y = (h + 3) // 4
        tiles_x = (w + 3) // 4
        dither_pattern = np.tile(bayer_4x4, (tiles_y, tiles_x))[:h, :w]

        # Scale by strength
        dither_pattern = dither_pattern * strength * 2

        # Apply dither to all channels
        result = frame.copy()
        for c in range(3):
            result[:, :, c] = result[:, :, c] + dither_pattern

        return result

    def _apply_vignette(self, frame: np.ndarray, strength: float) -> np.ndarray:
        """
        Apply radial vignette (edge darkening) effect.

        Uses a precomputed distance mask with sigmoid falloff for cinematic
        edge darkening. The mask is cached per resolution to avoid recomputation.

        Args:
            frame: Input frame (float32, 0-255)
            strength: Vignette intensity (0.0-1.0)

        Returns:
            Frame with vignette applied
        """
        if strength <= 0.0:
            return frame

        h, w = frame.shape[:2]

        # Cache the mask per resolution to avoid recomputing every frame
        if self._vignette_mask_cache is None or self._vignette_mask_cache[:2] != (h, w):
            cy, cx = h / 2.0, w / 2.0
            y_coords = np.arange(h, dtype=np.float32).reshape(-1, 1) - cy
            x_coords = np.arange(w, dtype=np.float32).reshape(1, -1) - cx
            # Normalize to elliptical distance (accounts for non-square frames)
            dist = np.sqrt((x_coords / cx) ** 2 + (y_coords / cy) ** 2)
            # Sigmoid falloff: 1.0 at center, 0 at edges
            # Steepness controls the transition width
            mask = 1.0 / (1.0 + np.exp(6.0 * (dist - 0.8)))
            self._vignette_mask_cache = (h, w, mask)

        mask = self._vignette_mask_cache[2]
        # Blend: darken = frame * (1 - strength * (1 - mask))
        vignette_factor = 1.0 - strength * (1.0 - mask)
        vignette_factor_3d = vignette_factor[:, :, np.newaxis]

        return frame * vignette_factor_3d

    def _apply_halation(self, frame: np.ndarray, strength: float) -> np.ndarray:
        """
        Apply halation/bloom effect: red-orange glow around bright highlights.

        Simulates analog film light reflection where bright areas bleed warm color
        into surrounding regions. Creates an organic, cinematic feel.

        Args:
            frame: Input frame (float32, 0-255)
            strength: Halation intensity (0.0-1.0)

        Returns:
            Frame with halation applied
        """
        if strength <= 0.0:
            return frame

        # Extract luminance to find highlights
        gray = 0.299 * frame[:, :, 2] + 0.587 * frame[:, :, 1] + 0.114 * frame[:, :, 0]  # BGR
        # Threshold: only bright areas (top 15% of range)
        threshold = 200.0
        highlight_mask = np.clip((gray - threshold) / (255.0 - threshold), 0, 1)

        if highlight_mask.max() < 0.01:
            return frame  # No highlights to bloom

        # Create warm halation color layer (red-orange: BGR 40, 100, 255)
        halation_r = highlight_mask * 255.0
        halation_g = highlight_mask * 100.0
        halation_b = highlight_mask * 40.0
        halation_layer = np.stack([halation_b, halation_g, halation_r], axis=-1).astype(np.float32)

        # Gaussian blur for bloom spread
        kernel_size = max(15, int(frame.shape[0] * 0.04)) | 1  # ~4% of height, odd
        halation_layer = cv2.GaussianBlur(halation_layer, (kernel_size, kernel_size), 0)

        # Screen blend: result = 1 - (1 - base) * (1 - layer)
        base_norm = frame / 255.0
        layer_norm = halation_layer / 255.0 * strength
        blended = 1.0 - (1.0 - base_norm) * (1.0 - layer_norm)

        return blended * 255.0

    def _apply_chromatic_aberration(self, frame: np.ndarray, strength: float) -> np.ndarray:
        """
        Apply chromatic aberration: RGB channel lateral offset toward frame edges.

        Simulates lens fringing where red and blue channels shift outward from center,
        creating a subtle color separation most visible at frame edges.

        Args:
            frame: Input frame (float32, 0-255)
            strength: CA intensity (0.0-1.0)

        Returns:
            Frame with chromatic aberration applied
        """
        if strength <= 0.0:
            return frame

        h, w = frame.shape[:2]
        # Scale factor: max pixel shift at edges (1-4 pixels depending on strength)
        max_shift = strength * 4.0

        # Red channel shifts outward (scale up slightly from center)
        # Blue channel shifts inward (scale down slightly from center)
        cy, cx = h / 2.0, w / 2.0

        # Build affine matrices for slight scale transforms
        # Red: scale up by factor, Blue: scale down by factor
        scale_r = 1.0 + max_shift / max(cx, cy)
        scale_b = 1.0 - max_shift / max(cx, cy)

        M_r = cv2.getRotationMatrix2D((cx, cy), 0, scale_r)
        M_b = cv2.getRotationMatrix2D((cx, cy), 0, scale_b)

        frame_u8 = np.clip(frame, 0, 255).astype(np.uint8)

        # Apply per-channel warp
        b_ch = cv2.warpAffine(frame_u8[:, :, 0], M_b, (w, h), borderMode=cv2.BORDER_REFLECT)
        g_ch = frame_u8[:, :, 1]  # Green stays centered
        r_ch = cv2.warpAffine(frame_u8[:, :, 2], M_r, (w, h), borderMode=cv2.BORDER_REFLECT)

        return np.stack([b_ch, g_ch, r_ch], axis=-1).astype(np.float32)

    def _normalize_dlog(self, frame: np.ndarray) -> np.ndarray:
        """
        Normalize D-Log / D-Log M / S-Log3 footage to Rec.709 gamma.

        Applies the inverse log curve to expand the compressed dynamic range
        before creative grading. Without this, presets produce incorrect results
        on professional DJI/Sony log-encoded footage.

        Args:
            frame: Input frame (float32, 0-255)

        Returns:
            Linearized and re-gamma'd frame in Rec.709 space
        """
        normalized = frame / 255.0

        if self.input_colorspace in ("dlog", "dlog_m"):
            # DJI D-Log M linearization curve (approximate)
            # D-Log M: maps 0-1 log to linear via power + offset
            linear = np.where(
                normalized <= 0.14,
                (normalized - 0.0929) / 6.025,
                np.power(10.0, (normalized - 0.584) / 0.342) / 106.3,
            )
            linear = np.clip(linear, 0, 1)
        elif self.input_colorspace == "slog3":
            # Sony S-Log3 linearization
            linear = np.where(
                normalized >= 171.2102946929 / 1023.0,
                np.power(10.0, (normalized * 1023.0 - 420.0) / 261.5) * (0.18 + 0.01) - 0.01,
                (normalized * 1023.0 - 95.0) * 0.01125000 / (171.2102946929 - 95.0),
            )
            linear = np.clip(linear, 0, 1)
        else:
            return frame

        # Apply Rec.709 gamma (approximate sRGB)
        rec709 = np.where(
            linear < 0.018,
            linear * 4.5,
            1.099 * np.power(linear, 0.45) - 0.099,
        )
        return np.clip(rec709 * 255.0, 0, 255).astype(np.float32)

    @staticmethod
    def detect_log_footage(frame: np.ndarray) -> str:
        """
        Heuristic detection of log-encoded footage.

        Log footage has characteristically low contrast and mid-range brightness
        due to dynamic range compression. Returns detected colorspace string.

        Args:
            frame: Sample frame (uint8 BGR)

        Returns:
            'dlog' if log footage detected, 'rec709' otherwise
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype(np.float32)
        mean_val = np.mean(gray)
        std_val = np.std(gray)
        min_val = np.percentile(gray, 2)
        max_val = np.percentile(gray, 98)
        dynamic_range = max_val - min_val

        # Log footage: compressed DR (low contrast), mid-range mean, low std
        if dynamic_range < 120 and 60 < mean_val < 180 and std_val < 40:
            return "dlog"
        return "rec709"

    def _apply_auto_wb(self, frame: np.ndarray) -> np.ndarray:
        """
        Gray world auto white balance.

        Scales each channel so the mean of each channel matches the overall mean,
        correcting color casts from mixed lighting or incorrect WB settings.

        Args:
            frame: Input frame (float32, 0-255)

        Returns:
            White-balanced frame
        """
        mean_b = np.mean(frame[:, :, 0])
        mean_g = np.mean(frame[:, :, 1])
        mean_r = np.mean(frame[:, :, 2])
        overall_mean = (mean_b + mean_g + mean_r) / 3.0

        if mean_b > 0:
            frame[:, :, 0] *= overall_mean / mean_b
        if mean_g > 0:
            frame[:, :, 1] *= overall_mean / mean_g
        if mean_r > 0:
            frame[:, :, 2] *= overall_mean / mean_r

        return np.clip(frame, 0, 255)

    def _apply_denoise(self, frame: np.ndarray, strength: float) -> np.ndarray:
        """
        Spatial denoising using OpenCV's fast non-local means.

        Reduces noise in low-light footage while preserving edges.
        Strength maps to filter strength parameter (h).

        Args:
            frame: Input frame (float32, 0-255)
            strength: Denoise intensity (0.0-1.0)

        Returns:
            Denoised frame
        """
        if strength <= 0.0:
            return frame

        # Map 0-1 strength to h parameter (3-15 typical range)
        h = 3.0 + strength * 12.0
        frame_u8 = np.clip(frame, 0, 255).astype(np.uint8)
        denoised = cv2.fastNlMeansDenoisingColored(
            frame_u8, None, h, h, 7, 21
        )
        return denoised.astype(np.float32)

    def _apply_haze(self, frame: np.ndarray, strength: float) -> np.ndarray:
        """
        Apply atmospheric haze / depth fog effect.

        Creates a vertical gradient that simulates aerial perspective,
        adding haze that increases toward the top of the frame (horizon).

        Args:
            frame: Input frame (float32, 0-255)
            strength: Haze intensity (0.0-1.0)

        Returns:
            Frame with atmospheric haze
        """
        if strength <= 0.0:
            return frame

        h, w = frame.shape[:2]
        # Vertical gradient: strongest at top (y=0), fading to zero at bottom
        gradient = np.linspace(strength, 0, h, dtype=np.float32)
        gradient = gradient.reshape(h, 1, 1)

        # Haze color: pale blue-white (BGR)
        haze_color = np.array([235, 225, 215], dtype=np.float32)

        # Blend: result = frame * (1 - gradient) + haze_color * gradient
        result = frame * (1 - gradient) + haze_color * gradient
        return np.clip(result, 0, 255)

    def _apply_gnd_sky(self, frame: np.ndarray, strength: float) -> np.ndarray:
        """
        Graduated neutral density sky correction.

        Darkens the upper portion of the frame to balance exposure between
        bright sky and darker ground, mimicking a physical GND filter.

        Args:
            frame: Input frame (float32, 0-255)
            strength: Darkening intensity (0.0-1.0)

        Returns:
            Frame with graduated sky darkening
        """
        if strength <= 0.0:
            return frame

        h, w = frame.shape[:2]
        # Gradient: darkest at top, reaching 1.0 (no effect) at middle of frame
        midpoint = h // 2
        top_gradient = np.linspace(1.0 - strength * 0.6, 1.0, midpoint, dtype=np.float32)
        bottom_ones = np.ones(h - midpoint, dtype=np.float32)
        gradient = np.concatenate([top_gradient, bottom_ones])
        gradient = gradient.reshape(h, 1, 1)

        return np.clip(frame * gradient, 0, 255)

    def _apply_auto_color_match(self, frame: np.ndarray) -> np.ndarray:
        """
        Match frame histogram to reference frame for cross-clip consistency.

        Uses cumulative histogram matching per channel to normalize color
        across clips from different lighting conditions.

        Args:
            frame: Input frame (float32, 0-255)

        Returns:
            Color-matched frame
        """
        if self._reference_histogram is None:
            return frame

        frame_u8 = np.clip(frame, 0, 255).astype(np.uint8)
        result = np.zeros_like(frame_u8)

        for ch in range(3):
            # Build CDF for source
            src_hist, _ = np.histogram(frame_u8[:, :, ch].ravel(), 256, [0, 256])
            src_cdf = src_hist.cumsum()
            src_cdf_norm = src_cdf / src_cdf[-1] if src_cdf[-1] > 0 else src_cdf

            ref_cdf = self._reference_histogram[ch]

            # Build mapping: for each source level, find closest reference level
            mapping = np.zeros(256, dtype=np.uint8)
            for s in range(256):
                idx = np.argmin(np.abs(ref_cdf - src_cdf_norm[s]))
                mapping[s] = idx

            result[:, :, ch] = mapping[frame_u8[:, :, ch]]

        return result.astype(np.float32)

    def set_reference_frame(self, frame: np.ndarray):
        """
        Set the reference frame for auto color matching.

        Computes and stores the CDF histogram per channel from the reference frame.

        Args:
            frame: Reference frame (uint8 BGR)
        """
        self._reference_histogram = []
        for ch in range(3):
            hist, _ = np.histogram(frame[:, :, ch].ravel(), 256, [0, 256])
            cdf = hist.cumsum()
            cdf_norm = cdf / cdf[-1] if cdf[-1] > 0 else cdf
            self._reference_histogram.append(cdf_norm)

    def _apply_teal_orange_grade(self, frame: np.ndarray) -> np.ndarray:
        """Apply teal and orange color grade popular in cinema.
        Uses high-precision float32 conversion to avoid banding.
        """
        # Convert to 0-1 range for float32 HSV conversion
        frame_normalized = frame / 255.0
        hsv = cv2.cvtColor(frame_normalized.astype(np.float32), cv2.COLOR_BGR2HSV)
        # In float32 HSV: H is 0-360, S is 0-1, V is 0-1

        hue = hsv[:, :, 0]

        # Adjust hue ranges for 0-360 scale
        orange_mask = ((hue >= 0) & (hue <= 60)) | ((hue >= 300) & (hue <= 360))
        teal_mask = (hue >= 150) & (hue <= 210)

        hsv[:, :, 1][orange_mask] = np.clip(hsv[:, :, 1][orange_mask] * 1.2, 0, 1)
        hsv[:, :, 1][teal_mask] = np.clip(hsv[:, :, 1][teal_mask] * 1.15, 0, 1)

        mid_tones = ~orange_mask & ~teal_mask
        hsv[:, :, 0][mid_tones] = np.where(
            hsv[:, :, 0][mid_tones] < 180, 30, 180  # Push towards orange or teal (scaled for 0-360)
        )

        result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return result * 255.0

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
