"""
Video reframing for social media aspect ratios.

Handles automatic reframing from landscape drone footage to vertical
9:16 format for Instagram Reels, TikTok, and YouTube Shorts.
"""

from dataclasses import dataclass, field
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
    SMART = "smart"  # AI-based subject tracking with drone optimizations
    PAN = "pan"  # Slow pan across the frame
    THIRDS = "thirds"  # Follow rule of thirds
    CUSTOM = "custom"  # Custom focal point
    HORIZON_LOCK = "horizon_lock"  # Lock horizon level at upper third
    FACE = "face"  # Track faces with fallback to saliency
    MOTION = "motion"  # Track motion-based focal point
    KEN_BURNS = "ken_burns"  # Slow zoom + pan for cinematic effect
    PUNCH_IN = "punch_in"  # Beat-synced zoom emphasis
    SUBJECT_TRACK = "subject_track"  # CSRT tracker-based subject following


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
    focal_clamp_x: tuple[float, float] = (0.2, 0.8)  # X-axis focal point bounds
    focal_clamp_y: tuple[float, float] = (0.2, 0.8)  # Y-axis focal point bounds
    adaptive_smoothing: bool = True  # Adjust smoothness based on velocity
    sky_mask_enabled: bool = True  # Mask sky in saliency detection
    sky_region_ratio: float = 0.35  # Portion of frame considered sky (upper)
    saliency_cache_frames: int = 10  # Recompute saliency every N frames
    scene_change_threshold: float = 0.3  # Histogram diff threshold for scene change
    horizon_penalty_weight: float = 0.5  # Penalty for tilted horizons in SMART mode
    face_cascade_path: Optional[str] = None  # Path to face cascade XML (optional)

    # Ken Burns effect settings
    ken_burns_zoom_start: float = 1.0  # Start zoom factor (1.0 = no zoom)
    ken_burns_zoom_end: float = 1.1  # End zoom factor (1.1 = 10% zoom in)
    ken_burns_pan_direction: tuple[float, float] = (0.1, 0.05)  # X, Y pan per clip
    ken_burns_ease_curve: str = "ease_in_out"  # easing: linear, ease_in, ease_out, ease_in_out

    # Punch-in zoom settings
    punch_in_zoom_factor: float = 1.15  # Maximum zoom on punch (1.15 = 15% zoom)
    punch_in_duration: float = 0.3  # Duration of punch effect in seconds
    punch_in_ease_in: float = 0.1  # Time to reach max zoom
    punch_in_ease_out: float = 0.2  # Time to return to normal

    # Subject tracking settings
    subject_tracker_type: str = "CSRT"  # Tracker type: CSRT, KCF, MOSSE
    subject_init_mode: str = "saliency"  # Initialization: saliency, center, manual
    subject_redetect_interval: int = 30  # Frames between re-detection
    subject_lost_fallback: str = "saliency"  # Fallback when tracker loses subject


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

        # Caching for performance
        self._saliency_cache: Optional[np.ndarray] = None
        self._saliency_cache_index: int = -1
        self._prev_histogram: Optional[np.ndarray] = None

        # Face detection
        self._face_cascade: Optional[cv2.CascadeClassifier] = None
        if self.settings.mode == ReframeMode.FACE:
            cascade_path = self.settings.face_cascade_path
            if cascade_path is None:
                # Try default OpenCV cascade
                cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            self._face_cascade = cv2.CascadeClassifier(cascade_path)
            if self._face_cascade.empty():
                raise ValueError(f"Failed to load face cascade from {cascade_path}")

        # Optical flow for motion tracking
        self._prev_gray: Optional[np.ndarray] = None

        # Adaptive smoothing
        self._focal_velocity_history: list[float] = []

        # Subject tracking (CSRT/KCF/MOSSE)
        self._subject_tracker: Optional[cv2.Tracker] = None
        self._subject_bbox: Optional[tuple[int, int, int, int]] = None
        self._subject_tracking_initialized: bool = False
        self._frames_since_redetect: int = 0

        # Punch-in state
        self._punch_in_active: bool = False
        self._punch_in_start_frame: int = 0
        self._beat_times: list[float] = []  # Set externally for beat-synced effects

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

        # Clamp crop dimensions to frame bounds (handles unusual aspect ratios)
        crop_w = min(crop_w, w)
        crop_h = min(crop_h, h)

        if self.settings.mode == ReframeMode.CENTER:
            x = (w - crop_w) // 2
            y = (h - crop_h) // 2

        elif self.settings.mode == ReframeMode.SMART:
            focal_x, focal_y = self._detect_focal_point(frame, frame_index)
            x = int(focal_x * w - crop_w / 2)
            y = int(focal_y * h - crop_h / 2)

            smoothness = self._calculate_adaptive_smoothness(x, y)

            if self.settings.smooth_tracking and self._tracker_history:
                prev_x, prev_y = self._tracker_history[-1]
                x = int(prev_x + (x - prev_x) * smoothness)
                y = int(prev_y + (y - prev_y) * smoothness)

            self._tracker_history.append((x, y))
            if len(self._tracker_history) > 30:
                self._tracker_history.pop(0)

        elif self.settings.mode == ReframeMode.HORIZON_LOCK:
            horizon_y = self._detect_horizon_line(frame)
            focal_x = 0.5  # Center horizontally

            if horizon_y is not None:
                # Position horizon at upper third
                target_horizon_y = crop_h / 3
                y = max(0, min(int(horizon_y - target_horizon_y), h - crop_h))
            else:
                # Fallback to upper third positioning
                y = int(h * 0.2)

            x = int(focal_x * (w - crop_w))

            if self.settings.smooth_tracking and self._tracker_history:
                prev_x, prev_y = self._tracker_history[-1]
                smoothness = self.settings.tracking_smoothness
                x = int(prev_x + (x - prev_x) * smoothness)
                y = int(prev_y + (y - prev_y) * smoothness)

            self._tracker_history.append((x, y))
            if len(self._tracker_history) > 30:
                self._tracker_history.pop(0)

        elif self.settings.mode == ReframeMode.FACE:
            faces = self._detect_faces(frame)
            if faces:
                focal_x, focal_y = self._calculate_face_center_of_mass(faces, w, h)
            else:
                # Fallback to saliency detection
                focal_x, focal_y = self._detect_focal_point(frame, frame_index)

            x = int(focal_x * w - crop_w / 2)
            y = int(focal_y * h - crop_h / 2)

            smoothness = self._calculate_adaptive_smoothness(x, y)

            if self.settings.smooth_tracking and self._tracker_history:
                prev_x, prev_y = self._tracker_history[-1]
                x = int(prev_x + (x - prev_x) * smoothness)
                y = int(prev_y + (y - prev_y) * smoothness)

            self._tracker_history.append((x, y))
            if len(self._tracker_history) > 30:
                self._tracker_history.pop(0)

        elif self.settings.mode == ReframeMode.MOTION:
            focal_x, focal_y = self._detect_motion_focal_point(frame)
            x = int(focal_x * w - crop_w / 2)
            y = int(focal_y * h - crop_h / 2)

            smoothness = self._calculate_adaptive_smoothness(x, y)

            if self.settings.smooth_tracking and self._tracker_history:
                prev_x, prev_y = self._tracker_history[-1]
                x = int(prev_x + (x - prev_x) * smoothness)
                y = int(prev_y + (y - prev_y) * smoothness)

            self._tracker_history.append((x, y))
            if len(self._tracker_history) > 30:
                self._tracker_history.pop(0)

        elif self.settings.mode == ReframeMode.PAN:
            progress = frame_index / max(total_frames - 1, 1)
            max_x = w - crop_w
            x = int(progress * max_x)
            y = (h - crop_h) // 2

        elif self.settings.mode == ReframeMode.THIRDS:
            focal_x, focal_y = self._detect_focal_point(frame, frame_index)
            third_x = round(focal_x * 2) / 2
            third_y = round(focal_y * 2) / 2
            x = int(third_x * (w - crop_w))
            y = int(third_y * (h - crop_h))

        elif self.settings.mode == ReframeMode.CUSTOM:
            focal_x, focal_y = self.settings.focal_point
            x = int(focal_x * (w - crop_w))
            y = int(focal_y * (h - crop_h))

        elif self.settings.mode == ReframeMode.KEN_BURNS:
            x, y, crop_w, crop_h = self._calculate_ken_burns_crop(
                frame, w, h, crop_w, crop_h, frame_index, total_frames
            )

        elif self.settings.mode == ReframeMode.PUNCH_IN:
            x, y, crop_w, crop_h = self._calculate_punch_in_crop(
                frame, w, h, crop_w, crop_h, frame_index, total_frames
            )

        elif self.settings.mode == ReframeMode.SUBJECT_TRACK:
            x, y, crop_w, crop_h = self._calculate_subject_tracking_crop(
                frame, w, h, crop_w, crop_h, frame_index
            )

        else:
            x = (w - crop_w) // 2
            y = (h - crop_h) // 2

        x = max(0, min(x, w - crop_w))
        y = max(0, min(y, h - crop_h))

        return x, y, crop_w, crop_h

    def _detect_focal_point(self, frame: np.ndarray, frame_index: int = 0) -> tuple[float, float]:
        """
        Detect the focal point of interest in a frame.

        Uses drone-optimized saliency detection with sky masking,
        rule of thirds weighting, and caching for performance.

        Args:
            frame: Input frame
            frame_index: Current frame index for caching

        Returns:
            Tuple of (x, y) normalized coordinates (0-1)
        """
        # Check if we can use cached saliency
        use_cache = (
            self._saliency_cache is not None
            and frame_index - self._saliency_cache_index < self.settings.saliency_cache_frames
            and not self._is_scene_change(frame)
        )

        if use_cache:
            saliency_map = self._saliency_cache
        else:
            if self._saliency is None:
                try:
                    self._saliency = cv2.saliency.StaticSaliencySpectralResidual_create()
                except AttributeError:
                    # opencv-contrib-python not installed, use fallback
                    return 0.5, 0.5

            small_frame = cv2.resize(frame, (320, 180))

            success, saliency_map = self._saliency.computeSaliency(small_frame)

            if not success:
                return 0.5, 0.5

            saliency_map = (saliency_map * 255).astype(np.uint8)

            # Apply drone-specific optimizations
            if self.settings.sky_mask_enabled:
                saliency_map = self._apply_sky_mask(saliency_map)

            # Apply rule of thirds weighting
            saliency_map = self._apply_rule_of_thirds_weighting(saliency_map)

            # Apply horizon tilt penalty
            if self.settings.horizon_penalty_weight > 0:
                saliency_map = self._apply_horizon_penalty(frame, saliency_map)

            # Cache the result
            self._saliency_cache = saliency_map
            self._saliency_cache_index = frame_index

        blurred = cv2.GaussianBlur(saliency_map, (21, 21), 0)
        _, max_val, _, max_loc = cv2.minMaxLoc(blurred)

        focal_x = max_loc[0] / 320
        focal_y = max_loc[1] / 180

        # Apply configurable clamping
        clamp_min_x, clamp_max_x = self.settings.focal_clamp_x
        clamp_min_y, clamp_max_y = self.settings.focal_clamp_y

        focal_x = clamp_min_x + focal_x * (clamp_max_x - clamp_min_x)
        focal_y = clamp_min_y + focal_y * (clamp_max_y - clamp_min_y)

        return focal_x, focal_y

    def _is_scene_change(self, frame: np.ndarray) -> bool:
        """
        Detect scene changes using histogram comparison.

        Args:
            frame: Current frame

        Returns:
            True if scene change detected
        """
        if self._prev_histogram is None:
            self._prev_histogram = self._compute_histogram(frame)
            return True

        current_hist = self._compute_histogram(frame)
        correlation = cv2.compareHist(
            self._prev_histogram, current_hist, cv2.HISTCMP_CORREL
        )

        # Correlation close to 1 means similar, close to -1 or 0 means different
        is_change = correlation < (1.0 - self.settings.scene_change_threshold)

        self._prev_histogram = current_hist
        return is_change

    def _compute_histogram(self, frame: np.ndarray) -> np.ndarray:
        """
        Compute color histogram for scene change detection.

        Args:
            frame: Input frame

        Returns:
            Normalized histogram
        """
        small_frame = cv2.resize(frame, (160, 90))
        hsv = cv2.cvtColor(small_frame, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([hsv], [0, 1], None, [50, 60], [0, 180, 0, 256])
        cv2.normalize(hist, hist)
        return hist

    def _apply_sky_mask(self, saliency_map: np.ndarray) -> np.ndarray:
        """
        Reduce saliency in sky region (typically upper portion).

        Args:
            saliency_map: Input saliency map

        Returns:
            Masked saliency map
        """
        h, w = saliency_map.shape[:2]
        sky_height = int(h * self.settings.sky_region_ratio)

        # Create gradient mask (smooth transition instead of hard cutoff)
        mask = np.ones_like(saliency_map, dtype=np.float32)
        for i in range(sky_height):
            # Gradient from 0.2 at top to 1.0 at sky boundary
            mask[i, :] = 0.2 + (0.8 * i / sky_height)

        return (saliency_map.astype(np.float32) * mask).astype(np.uint8)

    def _apply_rule_of_thirds_weighting(self, saliency_map: np.ndarray) -> np.ndarray:
        """
        Weight saliency map to favor rule of thirds composition.

        Args:
            saliency_map: Input saliency map

        Returns:
            Weighted saliency map
        """
        h, w = saliency_map.shape[:2]

        # Create 2D Gaussian centered at lower third
        y_weight = np.zeros(h, dtype=np.float32)
        lower_third_y = int(h * 0.66)

        for i in range(h):
            # Gaussian centered at lower third, sigma = h/3
            distance = (i - lower_third_y) ** 2
            y_weight[i] = np.exp(-distance / (2 * (h / 3) ** 2))

        # Normalize to range [0.7, 1.3] to boost lower third
        y_weight = 0.7 + 0.6 * (y_weight / y_weight.max())

        # Apply weighting
        weight_map = np.tile(y_weight[:, np.newaxis], (1, w))
        return (saliency_map.astype(np.float32) * weight_map).astype(np.uint8)

    def _apply_horizon_penalty(
        self, frame: np.ndarray, saliency_map: np.ndarray
    ) -> np.ndarray:
        """
        Penalize saliency based on horizon tilt.

        Args:
            frame: Original frame
            saliency_map: Input saliency map

        Returns:
            Penalized saliency map
        """
        horizon_angle = self._detect_horizon_angle(frame)

        if horizon_angle is not None and abs(horizon_angle) > 2.0:
            # Apply penalty proportional to tilt
            penalty = 1.0 - min(abs(horizon_angle) / 45.0, 0.5) * self.settings.horizon_penalty_weight
            return (saliency_map.astype(np.float32) * penalty).astype(np.uint8)

        return saliency_map

    def _detect_horizon_line(self, frame: np.ndarray) -> Optional[float]:
        """
        Detect the horizon line Y-coordinate using Hough line detection.

        Args:
            frame: Input frame

        Returns:
            Y-coordinate of horizon line, or None if not detected
        """
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Focus on horizontal edges in middle region
        h, w = gray.shape
        roi = gray[int(h * 0.2):int(h * 0.8), :]

        # Edge detection
        edges = cv2.Canny(roi, 50, 150, apertureSize=3)

        # Hough line detection
        lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=int(w * 0.3))

        if lines is None:
            return None

        # Find most horizontal line (closest to 0 or 180 degrees)
        horizontal_lines = []
        for line in lines:
            rho, theta = line[0]
            # Check if line is close to horizontal (within 15 degrees)
            if abs(theta) < np.pi / 12 or abs(theta - np.pi) < np.pi / 12:
                # Convert to y-coordinate
                y = rho / np.sin(theta) if np.sin(theta) != 0 else None
                if y is not None:
                    # Adjust for ROI offset
                    y += int(h * 0.2)
                    horizontal_lines.append(y)

        if horizontal_lines:
            # Return median horizontal line
            return float(np.median(horizontal_lines))

        return None

    def _detect_horizon_angle(self, frame: np.ndarray) -> Optional[float]:
        """
        Detect the tilt angle of the horizon line.

        Args:
            frame: Input frame

        Returns:
            Angle in degrees (0 = level), or None if not detected
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape
        roi = gray[int(h * 0.2):int(h * 0.8), :]

        edges = cv2.Canny(roi, 50, 150, apertureSize=3)
        lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=int(w * 0.3))

        if lines is None:
            return None

        angles = []
        for line in lines:
            rho, theta = line[0]
            # Convert to degrees from horizontal
            angle = (theta * 180 / np.pi) - 90
            if abs(angle) < 15:  # Only consider near-horizontal lines
                angles.append(angle)

        if angles:
            return float(np.median(angles))

        return None

    def _detect_faces(self, frame: np.ndarray) -> list[tuple[int, int, int, int]]:
        """
        Detect faces in the frame using Haar cascade.

        Args:
            frame: Input frame

        Returns:
            List of (x, y, w, h) rectangles for detected faces
        """
        if self._face_cascade is None:
            return []

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces at multiple scales
        faces = self._face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        return [(int(x), int(y), int(w), int(h)) for x, y, w, h in faces]

    def _calculate_face_center_of_mass(
        self, faces: list[tuple[int, int, int, int]], frame_w: int, frame_h: int
    ) -> tuple[float, float]:
        """
        Calculate the center of mass of detected faces.

        Weights larger faces more heavily.

        Args:
            faces: List of (x, y, w, h) face rectangles
            frame_w: Frame width
            frame_h: Frame height

        Returns:
            Tuple of (x, y) normalized coordinates (0-1)
        """
        if not faces:
            return 0.5, 0.5

        total_area = 0.0
        weighted_x = 0.0
        weighted_y = 0.0

        for x, y, w, h in faces:
            area = w * h
            center_x = x + w / 2
            center_y = y + h / 2

            weighted_x += center_x * area
            weighted_y += center_y * area
            total_area += area

        if total_area == 0:
            return 0.5, 0.5

        focal_x = weighted_x / total_area / frame_w
        focal_y = weighted_y / total_area / frame_h

        # Clamp to valid range
        focal_x = max(0.0, min(1.0, focal_x))
        focal_y = max(0.0, min(1.0, focal_y))

        return focal_x, focal_y

    def _detect_motion_focal_point(self, frame: np.ndarray) -> tuple[float, float]:
        """
        Detect focal point based on motion using optical flow.

        Tracks the region with highest motion magnitude.

        Args:
            frame: Input frame

        Returns:
            Tuple of (x, y) normalized coordinates (0-1)
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if self._prev_gray is None:
            self._prev_gray = gray
            return 0.5, 0.5

        # Calculate dense optical flow
        flow = cv2.calcOpticalFlowFarneback(
            self._prev_gray,
            gray,
            None,
            pyr_scale=0.5,
            levels=3,
            winsize=15,
            iterations=3,
            poly_n=5,
            poly_sigma=1.2,
            flags=0
        )

        # Calculate motion magnitude
        magnitude, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])

        # Downsample for performance
        small_magnitude = cv2.resize(magnitude, (320, 180))

        # Find region with highest motion
        blurred = cv2.GaussianBlur(small_magnitude, (21, 21), 0)
        _, max_val, _, max_loc = cv2.minMaxLoc(blurred)

        focal_x = max_loc[0] / 320
        focal_y = max_loc[1] / 180

        # Apply configurable clamping
        clamp_min_x, clamp_max_x = self.settings.focal_clamp_x
        clamp_min_y, clamp_max_y = self.settings.focal_clamp_y

        focal_x = clamp_min_x + focal_x * (clamp_max_x - clamp_min_x)
        focal_y = clamp_min_y + focal_y * (clamp_max_y - clamp_min_y)

        # Update previous frame
        self._prev_gray = gray

        return focal_x, focal_y

    def _calculate_adaptive_smoothness(self, x: int, y: int) -> float:
        """
        Calculate adaptive smoothness based on focal point velocity.

        Faster motion gets higher smoothness factor (less lag).

        Args:
            x: Current focal point X
            y: Current focal point Y

        Returns:
            Smoothness factor (0-1)
        """
        if not self.settings.adaptive_smoothing or not self._tracker_history:
            return self.settings.tracking_smoothness

        prev_x, prev_y = self._tracker_history[-1]

        # Calculate velocity magnitude
        velocity = np.sqrt((x - prev_x) ** 2 + (y - prev_y) ** 2)

        # Store velocity history
        self._focal_velocity_history.append(velocity)
        if len(self._focal_velocity_history) > 10:
            self._focal_velocity_history.pop(0)

        # Calculate average velocity
        avg_velocity = np.mean(self._focal_velocity_history)

        # Map velocity to smoothness
        # Low velocity (< 5 px): use base smoothness
        # High velocity (> 50 px): increase smoothness up to 0.7
        base_smoothness = self.settings.tracking_smoothness

        if avg_velocity < 5:
            return base_smoothness
        elif avg_velocity > 50:
            return min(0.7, base_smoothness * 2.0)
        else:
            # Linear interpolation
            velocity_factor = (avg_velocity - 5) / 45  # 0 to 1
            return base_smoothness + velocity_factor * (0.7 - base_smoothness)

    def _ease_function(self, t: float, curve: str = "ease_in_out") -> float:
        """
        Apply easing function to a normalized time value.

        Args:
            t: Normalized time (0.0 to 1.0)
            curve: Easing type (linear, ease_in, ease_out, ease_in_out)

        Returns:
            Eased value (0.0 to 1.0)
        """
        t = max(0.0, min(1.0, t))

        if curve == "linear":
            return t
        elif curve == "ease_in":
            return t * t
        elif curve == "ease_out":
            return 1 - (1 - t) * (1 - t)
        elif curve == "ease_in_out":
            if t < 0.5:
                return 2 * t * t
            else:
                return 1 - (-2 * t + 2) ** 2 / 2
        else:
            return t

    def _calculate_ken_burns_crop(
        self,
        frame: np.ndarray,
        w: int,
        h: int,
        base_crop_w: int,
        base_crop_h: int,
        frame_index: int,
        total_frames: int,
    ) -> tuple[int, int, int, int]:
        """
        Calculate Ken Burns effect crop with animated zoom and pan.

        The Ken Burns effect slowly zooms in/out while panning across the frame,
        creating a cinematic feel for static shots.

        Args:
            frame: Input frame
            w: Frame width
            h: Frame height
            base_crop_w: Base crop width for target aspect
            base_crop_h: Base crop height for target aspect
            frame_index: Current frame index
            total_frames: Total frames in clip

        Returns:
            Tuple of (x, y, crop_w, crop_h)
        """
        # Calculate progress through the clip
        progress = frame_index / max(total_frames - 1, 1)

        # Apply easing
        eased_progress = self._ease_function(
            progress, self.settings.ken_burns_ease_curve
        )

        # Calculate current zoom factor (interpolate between start and end)
        zoom_start = self.settings.ken_burns_zoom_start
        zoom_end = self.settings.ken_burns_zoom_end
        current_zoom = zoom_start + (zoom_end - zoom_start) * eased_progress

        # Apply zoom to crop dimensions (larger zoom = smaller crop area)
        # Clamp zoom to prevent micro-crops (minimum 25% of base dimensions)
        effective_zoom = min(current_zoom, 4.0)
        crop_w = max(int(base_crop_w / effective_zoom), base_crop_w // 4)
        crop_h = max(int(base_crop_h / effective_zoom), base_crop_h // 4)

        # Ensure crop doesn't exceed frame bounds
        crop_w = min(crop_w, w)
        crop_h = min(crop_h, h)

        # Calculate pan offset based on progress
        pan_x, pan_y = self.settings.ken_burns_pan_direction

        # Start position: center or detect focal point
        if not self._tracker_history:
            focal_x, focal_y = self._detect_focal_point(frame, frame_index)
            self._tracker_history.append((focal_x, focal_y))
        else:
            focal_x, focal_y = self._tracker_history[0]

        # Apply pan over time
        current_focal_x = focal_x + pan_x * eased_progress
        current_focal_y = focal_y + pan_y * eased_progress

        # Clamp focal point to valid range
        current_focal_x = max(0.1, min(0.9, current_focal_x))
        current_focal_y = max(0.1, min(0.9, current_focal_y))

        # Calculate crop position centered on focal point
        x = int(current_focal_x * w - crop_w / 2)
        y = int(current_focal_y * h - crop_h / 2)

        # Clamp to frame bounds
        x = max(0, min(x, w - crop_w))
        y = max(0, min(y, h - crop_h))

        return x, y, crop_w, crop_h

    def _calculate_punch_in_crop(
        self,
        frame: np.ndarray,
        w: int,
        h: int,
        base_crop_w: int,
        base_crop_h: int,
        frame_index: int,
        total_frames: int,
    ) -> tuple[int, int, int, int]:
        """
        Calculate punch-in zoom effect for beat-synced emphasis.

        Creates a quick zoom effect that can be triggered by beat times.

        Args:
            frame: Input frame
            w: Frame width
            h: Frame height
            base_crop_w: Base crop width
            base_crop_h: Base crop height
            frame_index: Current frame index
            total_frames: Total frames in clip

        Returns:
            Tuple of (x, y, crop_w, crop_h)
        """
        # Default: no punch effect active
        zoom_factor = 1.0

        # Check if we should activate a punch-in
        if self._beat_times:
            fps = 30  # Assume 30fps, could be passed as parameter
            current_time = frame_index / fps

            for beat_time in self._beat_times:
                time_since_beat = current_time - beat_time

                # Check if we're within the punch-in window
                if 0 <= time_since_beat < self.settings.punch_in_duration:
                    punch_progress = time_since_beat / self.settings.punch_in_duration

                    # Two-phase: quick ease-in, slower ease-out
                    ease_in_portion = self.settings.punch_in_ease_in / self.settings.punch_in_duration
                    ease_out_portion = self.settings.punch_in_ease_out / self.settings.punch_in_duration

                    if punch_progress < ease_in_portion:
                        # Ease in to max zoom
                        t = punch_progress / ease_in_portion
                        zoom_factor = 1.0 + (self.settings.punch_in_zoom_factor - 1.0) * self._ease_function(t, "ease_out")
                    else:
                        # Ease out back to normal
                        t = (punch_progress - ease_in_portion) / (1.0 - ease_in_portion)
                        zoom_factor = self.settings.punch_in_zoom_factor - (self.settings.punch_in_zoom_factor - 1.0) * self._ease_function(t, "ease_in")

                    break  # Only process first matching beat

        # Apply zoom factor to crop (larger zoom = smaller crop)
        crop_w = int(base_crop_w / zoom_factor)
        crop_h = int(base_crop_h / zoom_factor)

        # Ensure crop doesn't exceed frame bounds
        crop_w = min(crop_w, w)
        crop_h = min(crop_h, h)

        # Detect focal point for centering the punch
        focal_x, focal_y = self._detect_focal_point(frame, frame_index)

        # Apply smooth tracking
        smoothness = self._calculate_adaptive_smoothness(
            int(focal_x * w), int(focal_y * h)
        )
        if self.settings.smooth_tracking and self._tracker_history:
            prev_x, prev_y = self._tracker_history[-1]
            focal_x = prev_x + (focal_x - prev_x) * smoothness
            focal_y = prev_y + (focal_y - prev_y) * smoothness

        self._tracker_history.append((focal_x, focal_y))
        if len(self._tracker_history) > 30:
            self._tracker_history.pop(0)

        # Calculate crop position
        x = int(focal_x * w - crop_w / 2)
        y = int(focal_y * h - crop_h / 2)

        # Clamp to frame bounds
        x = max(0, min(x, w - crop_w))
        y = max(0, min(y, h - crop_h))

        return x, y, crop_w, crop_h

    def _initialize_subject_tracker(self, frame: np.ndarray) -> bool:
        """
        Initialize the subject tracker on first frame.

        Uses saliency detection to find initial bounding box.

        Args:
            frame: First frame to initialize tracking

        Returns:
            True if initialization successful
        """
        h, w = frame.shape[:2]

        # Get initial bounding box based on init mode
        if self.settings.subject_init_mode == "saliency":
            focal_x, focal_y = self._detect_focal_point(frame, 0)

            # Create bounding box around focal point
            bbox_w = int(w * 0.2)  # 20% of frame width
            bbox_h = int(h * 0.2)  # 20% of frame height

            bbox_x = int(focal_x * w - bbox_w / 2)
            bbox_y = int(focal_y * h - bbox_h / 2)

            # Clamp to frame bounds
            bbox_x = max(0, min(bbox_x, w - bbox_w))
            bbox_y = max(0, min(bbox_y, h - bbox_h))

            self._subject_bbox = (bbox_x, bbox_y, bbox_w, bbox_h)

        elif self.settings.subject_init_mode == "center":
            bbox_w = int(w * 0.2)
            bbox_h = int(h * 0.2)
            bbox_x = (w - bbox_w) // 2
            bbox_y = (h - bbox_h) // 2
            self._subject_bbox = (bbox_x, bbox_y, bbox_w, bbox_h)

        else:  # manual - use focal_point setting
            focal_x, focal_y = self.settings.focal_point
            bbox_w = int(w * 0.2)
            bbox_h = int(h * 0.2)
            bbox_x = int(focal_x * w - bbox_w / 2)
            bbox_y = int(focal_y * h - bbox_h / 2)
            self._subject_bbox = (bbox_x, bbox_y, bbox_w, bbox_h)

        # Create tracker based on type
        tracker_type = self.settings.subject_tracker_type.upper()
        if tracker_type == "CSRT":
            self._subject_tracker = cv2.TrackerCSRT_create()
        elif tracker_type == "KCF":
            self._subject_tracker = cv2.TrackerKCF_create()
        elif tracker_type == "MOSSE":
            self._subject_tracker = cv2.legacy.TrackerMOSSE_create()
        else:
            # Default to CSRT
            self._subject_tracker = cv2.TrackerCSRT_create()

        # Initialize tracker with bounding box
        try:
            success = self._subject_tracker.init(frame, self._subject_bbox)
            self._subject_tracking_initialized = success
            return success
        except Exception:
            self._subject_tracking_initialized = False
            return False

    def _calculate_subject_tracking_crop(
        self,
        frame: np.ndarray,
        w: int,
        h: int,
        crop_w: int,
        crop_h: int,
        frame_index: int,
    ) -> tuple[int, int, int, int]:
        """
        Calculate crop region using CSRT subject tracking.

        Tracks a subject across frames using OpenCV's tracking API.

        Args:
            frame: Input frame
            w: Frame width
            h: Frame height
            crop_w: Crop width
            crop_h: Crop height
            frame_index: Current frame index

        Returns:
            Tuple of (x, y, crop_w, crop_h)
        """
        # Initialize tracker on first frame
        if not self._subject_tracking_initialized:
            if not self._initialize_subject_tracker(frame):
                # Fallback to center crop
                return (w - crop_w) // 2, (h - crop_h) // 2, crop_w, crop_h

        # Update tracker
        success = False
        if self._subject_tracker is not None:
            try:
                success, bbox = self._subject_tracker.update(frame)
                if success:
                    self._subject_bbox = tuple(int(v) for v in bbox)
            except Exception:
                success = False

        # Check if we need to re-detect
        self._frames_since_redetect += 1
        if not success or self._frames_since_redetect >= self.settings.subject_redetect_interval:
            # Re-initialize tracker
            self._subject_tracking_initialized = False
            self._frames_since_redetect = 0

            if self.settings.subject_lost_fallback == "saliency":
                if self._initialize_subject_tracker(frame):
                    success = True

        # Calculate focal point from bounding box or fallback
        if success and self._subject_bbox:
            bbox_x, bbox_y, bbox_w, bbox_h = self._subject_bbox
            focal_x = (bbox_x + bbox_w / 2) / w
            focal_y = (bbox_y + bbox_h / 2) / h
        else:
            # Fallback to saliency
            focal_x, focal_y = self._detect_focal_point(frame, frame_index)

        # Apply smooth tracking
        smoothness = self._calculate_adaptive_smoothness(
            int(focal_x * w), int(focal_y * h)
        )
        if self.settings.smooth_tracking and self._tracker_history:
            prev_x, prev_y = self._tracker_history[-1]
            focal_x = prev_x + (focal_x - prev_x) * smoothness
            focal_y = prev_y + (focal_y - prev_y) * smoothness

        self._tracker_history.append((focal_x, focal_y))
        if len(self._tracker_history) > 30:
            self._tracker_history.pop(0)

        # Calculate crop position
        x = int(focal_x * w - crop_w / 2)
        y = int(focal_y * h - crop_h / 2)

        # Clamp to frame bounds
        x = max(0, min(x, w - crop_w))
        y = max(0, min(y, h - crop_h))

        return x, y, crop_w, crop_h

    def set_beat_times(self, beat_times: list[float]) -> None:
        """
        Set beat times for punch-in effect synchronization.

        Args:
            beat_times: List of beat times in seconds
        """
        self._beat_times = sorted(beat_times)

    def apply_ken_burns_to_static_clip(
        self,
        frame: np.ndarray,
        zoom_start: float = 1.0,
        zoom_end: float = 1.1,
        pan_x: float = 0.1,
        pan_y: float = 0.05,
    ) -> dict:
        """
        Get Ken Burns parameters for a clip without changing settings.

        Useful for applying Ken Burns to specific clips while keeping
        default settings unchanged.

        Args:
            frame: Sample frame to analyze
            zoom_start: Starting zoom factor
            zoom_end: Ending zoom factor
            pan_x: X pan direction per clip
            pan_y: Y pan direction per clip

        Returns:
            Dict with focal_point, zoom_range, and pan_direction
        """
        focal_x, focal_y = self._detect_focal_point(frame, 0)

        return {
            "focal_point": (focal_x, focal_y),
            "zoom_start": zoom_start,
            "zoom_end": zoom_end,
            "pan_direction": (pan_x, pan_y),
        }

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
        self._saliency_cache = None
        self._saliency_cache_index = -1
        self._prev_histogram = None
        self._prev_gray = None
        self._focal_velocity_history = []
        # Reset subject tracking
        self._subject_tracker = None
        self._subject_bbox = None
        self._subject_tracking_initialized = False
        self._frames_since_redetect = 0
        # Reset punch-in state
        self._punch_in_active = False
        self._punch_in_start_frame = 0


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
