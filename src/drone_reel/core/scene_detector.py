"""
Scene detection and highlight extraction for drone footage.

Uses PySceneDetect for scene boundary detection and OpenCV for
visual quality scoring to identify the most compelling moments.
"""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional

import cv2
import numpy as np
from scenedetect import ContentDetector, SceneManager, open_video


class MotionType(Enum):
    """Camera motion classification."""

    STATIC = "static"
    PAN_LEFT = "pan_left"
    PAN_RIGHT = "pan_right"
    TILT_UP = "tilt_up"
    TILT_DOWN = "tilt_down"
    ORBIT_CW = "orbit_cw"
    ORBIT_CCW = "orbit_ccw"
    REVEAL = "reveal"
    FLYOVER = "flyover"
    FPV = "fpv"
    APPROACH = "approach"
    UNKNOWN = "unknown"


@dataclass
class SceneInfo:
    """Information about a detected scene."""

    start_time: float
    end_time: float
    duration: float
    score: float
    source_file: Path
    thumbnail: Optional[np.ndarray] = None

    @property
    def midpoint(self) -> float:
        """Get the midpoint time of the scene."""
        return self.start_time + (self.duration / 2)


class HookPotential(Enum):
    """Hook potential classification tiers."""

    MAXIMUM = "maximum"  # 9-10: Wildlife, dynamic motion, high contrast
    HIGH = "high"  # 7-8: Moving boat, golden hour, dramatic reveal
    MEDIUM = "medium"  # 5-6: Static scenic, mountain panorama, ocean texture
    LOW = "low"  # 3-4: Empty ocean, distant subjects, flat lighting
    POOR = "poor"  # 1-2: Overexposed, underexposed, no focal point


@dataclass
class EnhancedSceneInfo(SceneInfo):
    """Extended scene metadata with motion and visual attributes."""

    motion_type: MotionType = MotionType.UNKNOWN
    motion_direction: tuple[float, float] = (0.0, 0.0)
    motion_smoothness: float = 0.0
    motion_energy: float = 0.0  # Motion intensity score (0-100), used for filtering
    dominant_colors: list[tuple[int, int, int]] = field(default_factory=list)
    color_variance: float = 0.0
    is_golden_hour: bool = False
    depth_score: float = 0.0
    # New fields for hook potential
    subject_score: float = 0.0  # Subject detection score (0-100)
    hook_potential: float = 0.0  # Overall hook potential (0-100)
    hook_tier: HookPotential = HookPotential.MEDIUM
    visual_interest_density: float = 0.0  # Subjects per frame area


class SceneDetector:
    """
    Detects scenes in video files and scores them for visual interest.

    Uses content-based scene detection combined with visual quality metrics
    to identify the most compelling moments in drone footage.
    """

    def __init__(
        self,
        threshold: float = 27.0,
        min_scene_length: float = 1.0,
        max_scene_length: float = 10.0,
        analysis_scale: float = 0.5,
        frame_skip: int = 0,
    ):
        """
        Initialize the scene detector.

        Args:
            threshold: Sensitivity for scene detection (lower = more scenes)
            min_scene_length: Minimum scene duration in seconds
            max_scene_length: Maximum scene duration in seconds
            analysis_scale: Scale factor for frame analysis (0.25-1.0, lower=faster)
            frame_skip: Frames to skip during detection (0=process all, 1=every 2nd, 3=every 4th).
                Use 1 for 60fps footage, 3 for 120fps. Reduces accuracy slightly.
        """
        self.threshold = threshold
        self.min_scene_length = min_scene_length
        self.max_scene_length = max_scene_length
        self.analysis_scale = max(0.25, min(1.0, analysis_scale))
        self.frame_skip = max(0, int(frame_skip))

    def detect_scenes(self, video_path: Path) -> list[SceneInfo]:
        """
        Detect all scenes in a video file.

        If no scene changes are detected, treats the entire video as a single scene.

        Args:
            video_path: Path to the video file

        Returns:
            List of SceneInfo objects for each detected scene
        """
        video = open_video(str(video_path))
        scene_manager = SceneManager()
        scene_manager.add_detector(ContentDetector(threshold=self.threshold))

        scene_manager.detect_scenes(video, frame_skip=self.frame_skip)
        scene_list = scene_manager.get_scene_list()

        scenes = []
        for start, end in scene_list:
            start_time = start.get_seconds()
            end_time = end.get_seconds()
            duration = end_time - start_time

            if duration < self.min_scene_length:
                continue

            if duration > self.max_scene_length:
                sub_scenes = self._split_long_scene(
                    video_path, start_time, end_time, self.max_scene_length
                )
                scenes.extend(sub_scenes)
            else:
                score = self._score_scene(video_path, start_time, end_time)
                scenes.append(
                    SceneInfo(
                        start_time=start_time,
                        end_time=end_time,
                        duration=duration,
                        score=score,
                        source_file=video_path,
                    )
                )

        # If no scenes detected, treat entire video as one scene
        if not scenes:
            video_duration = self._get_video_duration(video_path)
            if video_duration >= self.min_scene_length:
                # Split into segments if video is longer than max_scene_length
                if video_duration > self.max_scene_length:
                    scenes = self._split_long_scene(
                        video_path, 0, video_duration, self.max_scene_length
                    )
                else:
                    score = self._score_scene(video_path, 0, video_duration)
                    scenes.append(
                        SceneInfo(
                            start_time=0,
                            end_time=video_duration,
                            duration=video_duration,
                            score=score,
                            source_file=video_path,
                        )
                    )

        return scenes

    def _get_video_duration(self, video_path: Path) -> float:
        """Get the duration of a video file in seconds."""
        cap = cv2.VideoCapture(str(video_path))
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        cap.release()
        if fps > 0:
            return frame_count / fps
        return 0.0

    def _split_long_scene(
        self, video_path: Path, start: float, end: float, max_length: float
    ) -> list[SceneInfo]:
        """Split a long scene into smaller segments."""
        scenes = []
        current_start = start

        while current_start < end:
            current_end = min(current_start + max_length, end)
            duration = current_end - current_start

            if duration >= self.min_scene_length:
                score = self._score_scene(video_path, current_start, current_end)
                scenes.append(
                    SceneInfo(
                        start_time=current_start,
                        end_time=current_end,
                        duration=duration,
                        score=score,
                        source_file=video_path,
                    )
                )

            current_start = current_end

        return scenes

    def _score_scene(self, video_path: Path, start: float, end: float) -> float:
        """
        Score a scene based on visual quality metrics.

        Scoring factors:
        - Motion (30%): Camera movement and dynamic content via optical flow
        - Composition (20%): Rule of thirds, horizon level, leading lines
        - Color variance (20%): Saturation spread
        - Sharpness (15%): Laplacian variance
        - Brightness balance (15%): Not too dark/bright

        Args:
            video_path: Path to video file
            start: Start time in seconds
            end: End time in seconds

        Returns:
            Score from 0-100, higher is better
        """
        cap = cv2.VideoCapture(str(video_path))
        fps = cap.get(cv2.CAP_PROP_FPS)

        start_frame = int(start * fps)
        end_frame = int(end * fps)
        duration_frames = end_frame - start_frame

        # Adaptive sampling: 2 samples per second, minimum 10 frames
        samples_per_second = 2
        target_samples = max(10, int((end - start) * samples_per_second))
        sample_interval = max(1, duration_frames // target_samples)

        sample_frames = list(range(start_frame, end_frame, sample_interval))
        if not sample_frames or sample_frames[-1] != end_frame - 1:
            sample_frames.append(end_frame - 1)

        scores = []
        prev_frame = None
        prev_gray = None

        for frame_num in sample_frames:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
            ret, frame = cap.read()
            if not ret:
                continue

            sharpness = self._calculate_sharpness(frame)
            color_score = self._calculate_color_variance(frame)
            brightness_score = self._calculate_brightness_balance(frame)
            composition_score = self._calculate_composition(frame)

            # Initialize motion score properly for first frame
            motion_score = 50.0  # Neutral score for first frame
            if prev_frame is not None and prev_gray is not None:
                motion_score = self._calculate_motion_optical_flow(prev_gray, frame)

            frame_score = (
                motion_score * 0.30
                + composition_score * 0.20
                + color_score * 0.20
                + sharpness * 0.15
                + brightness_score * 0.15
            )
            scores.append(frame_score)

            prev_frame = frame.copy()
            prev_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cap.release()

        if not scores:
            return 0.0

        # Use weighted combination of max and mean (peak scoring)
        max_score = np.max(scores)
        mean_score = np.mean(scores)
        return 0.6 * max_score + 0.4 * mean_score

    def _calculate_sharpness(self, frame: np.ndarray) -> float:
        """Calculate sharpness using Laplacian variance."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        variance = laplacian.var()
        return min(variance / 500.0 * 100, 100.0)

    def _calculate_color_variance(self, frame: np.ndarray) -> float:
        """Calculate color richness using saturation variance."""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        saturation = hsv[:, :, 1]
        mean_sat = np.mean(saturation)
        std_sat = np.std(saturation)
        score = (mean_sat / 255.0 * 50) + (std_sat / 128.0 * 50)
        return min(score, 100.0)

    def _calculate_brightness_balance(self, frame: np.ndarray) -> float:
        """Score brightness - penalize too dark or too bright."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mean_brightness = np.mean(gray)
        ideal_brightness = 127
        deviation = abs(mean_brightness - ideal_brightness) / ideal_brightness
        return max(0, 100 - deviation * 100)

    def _calculate_motion_optical_flow(
        self, prev_gray: np.ndarray, curr_frame: np.ndarray
    ) -> float:
        """
        Estimate motion using optical flow analysis.

        Uses Farneback optical flow to detect camera movement and distinguish
        between different types of motion (pan, tilt, zoom).

        Args:
            prev_gray: Previous frame in grayscale
            curr_frame: Current frame in BGR

        Returns:
            Motion score from 0-100
        """
        curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)

        # Calculate dense optical flow
        flow = cv2.calcOpticalFlowFarneback(
            prev_gray,
            curr_gray,
            None,
            pyr_scale=0.5,
            levels=3,
            winsize=15,
            iterations=3,
            poly_n=5,
            poly_sigma=1.2,
            flags=0,
        )

        # Calculate flow magnitude and angle
        magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])

        # Calculate motion metrics
        mean_magnitude = np.mean(magnitude)
        max_magnitude = np.percentile(magnitude, 95)  # 95th percentile
        std_magnitude = np.std(magnitude)

        # Motion consistency (more consistent = better camera movement)
        consistency = 1.0 - min(std_magnitude / (mean_magnitude + 1e-6), 1.0)

        # Combine metrics
        motion_amount = min(mean_magnitude / 3.0 * 100, 100.0)
        motion_quality = consistency * 100

        # Weighted combination: prefer smooth, consistent motion
        motion_score = 0.7 * motion_amount + 0.3 * motion_quality

        return min(motion_score, 100.0)

    def _calculate_composition(self, frame: np.ndarray) -> float:
        """
        Analyze composition quality of a frame.

        Checks:
        - Rule of thirds: Key points near intersection lines
        - Horizon levelness: Using Hough line detection
        - Leading lines: Presence of strong directional elements

        Args:
            frame: Input frame in BGR

        Returns:
            Composition score from 0-100
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        height, width = gray.shape

        # Edge detection for feature analysis
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)

        # 1. Rule of thirds score
        thirds_score = self._score_rule_of_thirds(edges, width, height)

        # 2. Horizon levelness score
        horizon_score = self._score_horizon_level(edges, width, height)

        # 3. Leading lines score
        lines_score = self._score_leading_lines(edges, width, height)

        # Combine scores
        composition_score = thirds_score * 0.4 + horizon_score * 0.3 + lines_score * 0.3

        return min(composition_score, 100.0)

    def _score_rule_of_thirds(self, edges: np.ndarray, width: int, height: int) -> float:
        """
        Score frame based on rule of thirds.

        Checks if key points/edges align with rule of thirds intersections.
        """
        # Define rule of thirds lines
        h_third = height // 3
        w_third = width // 3

        # Create bands around rule of thirds lines (10% tolerance)
        tolerance = int(min(width, height) * 0.05)

        # Vertical bands at 1/3 and 2/3
        v_band1 = edges[:, max(0, w_third - tolerance) : min(width, w_third + tolerance)]
        v_band2 = edges[:, max(0, 2 * w_third - tolerance) : min(width, 2 * w_third + tolerance)]

        # Horizontal bands at 1/3 and 2/3
        h_band1 = edges[max(0, h_third - tolerance) : min(height, h_third + tolerance), :]
        h_band2 = edges[max(0, 2 * h_third - tolerance) : min(height, 2 * h_third + tolerance), :]

        # Calculate edge density in bands
        v_density = (np.sum(v_band1) + np.sum(v_band2)) / (v_band1.size + v_band2.size + 1e-6)
        h_density = (np.sum(h_band1) + np.sum(h_band2)) / (h_band1.size + h_band2.size + 1e-6)

        # Normalize to 0-100
        v_score = min(v_density / 255.0 * 100 * 50, 100.0)
        h_score = min(h_density / 255.0 * 100 * 50, 100.0)

        return (v_score + h_score) / 2

    def _score_horizon_level(self, edges: np.ndarray, width: int, height: int) -> float:
        """
        Score horizon levelness using Hough line detection.

        Detects strong horizontal lines and checks their angle deviation.
        """
        # Detect lines using Hough transform
        lines = cv2.HoughLinesP(
            edges, rho=1, theta=np.pi / 180, threshold=50, minLineLength=width // 4, maxLineGap=10
        )

        if lines is None:
            return 50.0  # Neutral score if no lines detected

        # Find horizontal lines (angle close to 0 or 180 degrees)
        horizontal_angles = []

        for line in lines:
            x1, y1, x2, y2 = line[0]
            # Skip vertical lines
            if abs(x2 - x1) < 1:
                continue

            # Calculate angle
            angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))

            # Normalize to 0-180
            angle = abs(angle)
            if angle > 90:
                angle = 180 - angle

            # Check if nearly horizontal (within 30 degrees)
            if angle < 30:
                horizontal_angles.append(angle)

        if not horizontal_angles:
            return 50.0  # Neutral score

        # Score based on deviation from perfectly level
        mean_angle = np.mean(horizontal_angles)
        deviation = abs(mean_angle) / 30.0  # Normalize to 0-1

        # Lower deviation = higher score
        score = (1.0 - deviation) * 100

        return max(0.0, min(score, 100.0))

    def _score_leading_lines(self, edges: np.ndarray, width: int, height: int) -> float:
        """
        Score presence of leading lines.

        Detects strong directional lines that guide the viewer's eye.
        """
        # Detect lines using Hough transform
        lines = cv2.HoughLinesP(
            edges, rho=1, theta=np.pi / 180, threshold=50, minLineLength=width // 5, maxLineGap=20
        )

        if lines is None:
            return 30.0  # Low base score if no lines

        # Count and measure line strength
        line_count = len(lines)
        total_length = 0

        for line in lines:
            x1, y1, x2, y2 = line[0]
            length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            total_length += length

        # Normalize scores
        count_score = min(line_count / 20.0 * 100, 100.0)
        length_score = min(total_length / (width * height * 0.5) * 100, 100.0)

        # Combine metrics
        score = count_score * 0.4 + length_score * 0.6

        return min(score, 100.0)

    def _calculate_subject_score(self, frame: np.ndarray) -> tuple[float, float]:
        """
        Calculate subject detection score using saliency and contrast analysis.

        This method detects visually interesting subjects (objects, wildlife, boats)
        without requiring ML models by analyzing:
        - Saliency/contrast regions that stand out from background
        - Edge density in distinct areas
        - Color distinctiveness from average

        Args:
            frame: Input frame in BGR

        Returns:
            Tuple of (subject_score 0-100, visual_interest_density 0-1)
        """
        height, width = frame.shape[:2]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 1. Compute saliency using spectral residual approach
        # (simplified version without opencv_contrib dependency)
        dft = cv2.dft(np.float32(gray), flags=cv2.DFT_COMPLEX_OUTPUT)
        magnitude = cv2.magnitude(dft[:, :, 0], dft[:, :, 1])
        log_magnitude = np.log(magnitude + 1)

        # Smooth and find residual (salient regions)
        smooth_mag = cv2.blur(log_magnitude, (3, 3))
        residual = log_magnitude - smooth_mag

        # Reconstruct
        exp_residual = np.exp(residual)
        dft_modified = dft.copy()
        eps = 1e-10
        dft_modified[:, :, 0] = dft_modified[:, :, 0] * (exp_residual / (magnitude + eps))
        dft_modified[:, :, 1] = dft_modified[:, :, 1] * (exp_residual / (magnitude + eps))

        idft = cv2.idft(dft_modified)
        saliency_map = cv2.magnitude(idft[:, :, 0], idft[:, :, 1])

        # Normalize saliency
        saliency_map = cv2.normalize(saliency_map, None, 0, 255, cv2.NORM_MINMAX)
        saliency_map = cv2.GaussianBlur(saliency_map.astype(np.uint8), (9, 9), 0)

        # 2. Find salient regions (potential subjects)
        _, thresh = cv2.threshold(saliency_map, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Find contours of salient regions
        contours, _ = cv2.findContours(thresh.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            return 30.0, 0.0  # No distinct subjects, low base score

        # 3. Analyze subject characteristics
        total_area = height * width
        subject_area = 0
        significant_subjects = 0

        for contour in contours:
            area = cv2.contourArea(contour)
            # Subject is significant if between 0.5% and 50% of frame
            if 0.005 * total_area < area < 0.5 * total_area:
                significant_subjects += 1
                subject_area += area

        # Calculate metrics
        visual_interest_density = min(subject_area / total_area, 1.0)
        subject_count_score = min(significant_subjects * 20, 100)  # Up to 5 subjects for full score

        # 4. Measure contrast distinctiveness
        mean_val = np.mean(gray)
        salient_mask = thresh > 127
        if np.any(salient_mask):
            subject_mean = np.mean(gray[salient_mask])
            contrast_ratio = abs(subject_mean - mean_val) / max(mean_val, 1)
            contrast_score = min(contrast_ratio * 100, 100)
        else:
            contrast_score = 30.0

        # Combine scores
        subject_score = (
            visual_interest_density * 100 * 0.35  # Subject area presence
            + subject_count_score * 0.35  # Number of subjects
            + contrast_score * 0.30  # Subject contrast
        )

        return min(subject_score, 100.0), visual_interest_density

    def _calculate_hook_potential(
        self,
        frame: np.ndarray,
        subject_score: float,
        motion_score: float,
        color_score: float,
        composition_score: float,
    ) -> tuple[float, HookPotential]:
        """
        Calculate hook potential score for a frame/scene.

        Hook potential determines how engaging the content is for the first
        3 seconds of a reel. Higher hook potential = better opener.

        Hook Potential Formula:
            visual_interest_density * 0.35 +
            motion_intensity * 0.25 +
            color_vibrancy * 0.20 +
            composition_strength * 0.10 +
            uniqueness_factor * 0.10

        Args:
            frame: Input frame in BGR
            subject_score: Subject detection score (0-100)
            motion_score: Motion intensity score (0-100)
            color_score: Color vibrancy score (0-100)
            composition_score: Composition quality score (0-100)

        Returns:
            Tuple of (hook_potential 0-100, HookPotential tier)
        """
        # Calculate color vibrancy (enhanced saturation analysis)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        saturation = hsv[:, :, 1]
        brightness = hsv[:, :, 2]

        sat_mean = np.mean(saturation)
        sat_std = np.std(saturation)
        bright_contrast = np.std(brightness)

        color_vibrancy = min(
            (sat_mean / 255 * 50) + (sat_std / 50 * 25) + (bright_contrast / 50 * 25), 100
        )

        # Uniqueness factor - measure of how different this frame is
        # (approximated by histogram entropy)
        hist = cv2.calcHist([frame], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        hist = hist.flatten()
        hist = hist / hist.sum()
        hist = hist[hist > 0]
        entropy = -np.sum(hist * np.log2(hist))
        uniqueness_score = min(entropy / 6 * 100, 100)  # Normalize (max entropy ~6 for 8x8x8)

        # Calculate hook potential
        hook_potential = (
            subject_score * 0.35
            + motion_score * 0.25
            + color_vibrancy * 0.20
            + composition_score * 0.10
            + uniqueness_score * 0.10
        )

        # Classify into tiers
        if hook_potential >= 80:
            tier = HookPotential.MAXIMUM
        elif hook_potential >= 65:
            tier = HookPotential.HIGH
        elif hook_potential >= 45:
            tier = HookPotential.MEDIUM
        elif hook_potential >= 25:
            tier = HookPotential.LOW
        else:
            tier = HookPotential.POOR

        return min(hook_potential, 100.0), tier

    def score_scene_with_hook_potential(
        self, video_path: Path, start: float, end: float
    ) -> tuple[float, float, float, HookPotential]:
        """
        Score a scene with enhanced hook potential analysis.

        Returns overall score plus subject score, hook potential, and tier.

        Args:
            video_path: Path to video file
            start: Start time in seconds
            end: End time in seconds

        Returns:
            Tuple of (overall_score, subject_score, hook_potential, hook_tier)
        """
        cap = cv2.VideoCapture(str(video_path))
        fps = cap.get(cv2.CAP_PROP_FPS)

        start_frame = int(start * fps)
        end_frame = int(end * fps)
        duration_frames = end_frame - start_frame

        # Sample frames
        samples_per_second = 2
        target_samples = max(10, int((end - start) * samples_per_second))
        sample_interval = max(1, duration_frames // target_samples)
        sample_frames = list(range(start_frame, end_frame, sample_interval))

        scores = []
        subject_scores = []
        hook_potentials = []
        prev_gray = None

        for frame_num in sample_frames:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
            ret, frame = cap.read()
            if not ret:
                continue

            # Downscale for analysis (scoring is scale-invariant)
            if self.analysis_scale < 1.0:
                analysis_frame = cv2.resize(
                    frame, (0, 0),
                    fx=self.analysis_scale, fy=self.analysis_scale,
                    interpolation=cv2.INTER_AREA,
                )
            else:
                analysis_frame = frame

            # Calculate all metrics
            sharpness = self._calculate_sharpness(analysis_frame)
            color_score = self._calculate_color_variance(analysis_frame)
            brightness_score = self._calculate_brightness_balance(analysis_frame)
            composition_score = self._calculate_composition(analysis_frame)
            subject_score, visual_density = self._calculate_subject_score(analysis_frame)

            motion_score = 50.0
            if prev_gray is not None:
                motion_score = self._calculate_motion_optical_flow(prev_gray, analysis_frame)

            hook_score, _ = self._calculate_hook_potential(
                frame, subject_score, motion_score, color_score, composition_score
            )

            # New scoring weights with subject detection (25%)
            frame_score = (
                subject_score * 0.25
                + motion_score * 0.25
                + composition_score * 0.15
                + color_score * 0.15
                + sharpness * 0.10
                + brightness_score * 0.10
            )

            scores.append(frame_score)
            subject_scores.append(subject_score)
            hook_potentials.append(hook_score)

            prev_gray = cv2.cvtColor(analysis_frame, cv2.COLOR_BGR2GRAY)

        cap.release()

        if not scores:
            return 0.0, 0.0, 0.0, HookPotential.POOR

        # Aggregate scores
        overall_score = 0.6 * np.max(scores) + 0.4 * np.mean(scores)
        avg_subject = np.mean(subject_scores)
        avg_hook = np.mean(hook_potentials)

        # Determine tier from average hook potential
        if avg_hook >= 80:
            tier = HookPotential.MAXIMUM
        elif avg_hook >= 65:
            tier = HookPotential.HIGH
        elif avg_hook >= 45:
            tier = HookPotential.MEDIUM
        elif avg_hook >= 25:
            tier = HookPotential.LOW
        else:
            tier = HookPotential.POOR

        return overall_score, avg_subject, avg_hook, tier

    def get_top_scenes(
        self, video_paths: list[Path], count: int = 10, min_per_video: int = 1
    ) -> list[SceneInfo]:
        """
        Get the top-scoring scenes from multiple videos.

        Args:
            video_paths: List of video file paths
            count: Total number of scenes to return
            min_per_video: Minimum scenes to include from each video

        Returns:
            List of top-scoring SceneInfo objects
        """
        all_scenes: list[SceneInfo] = []

        for video_path in video_paths:
            scenes = self.detect_scenes(video_path)
            if scenes:
                scenes.sort(key=lambda s: s.score, reverse=True)
                top_from_video = scenes[: max(min_per_video, count // len(video_paths))]
                all_scenes.extend(top_from_video)

        all_scenes.sort(key=lambda s: s.score, reverse=True)
        return all_scenes[:count]

    def extract_thumbnail(self, scene: SceneInfo) -> np.ndarray:
        """Extract a thumbnail from the middle of a scene."""
        cap = cv2.VideoCapture(str(scene.source_file))
        fps = cap.get(cv2.CAP_PROP_FPS)
        mid_frame = int(scene.midpoint * fps)

        cap.set(cv2.CAP_PROP_POS_FRAMES, mid_frame)
        ret, frame = cap.read()
        cap.release()

        if ret:
            scene.thumbnail = frame
            return frame
        return np.zeros((480, 640, 3), dtype=np.uint8)

    def classify_camera_motion(self, flow: np.ndarray) -> tuple[MotionType, tuple[float, float]]:
        """
        Classify camera motion type from optical flow.

        Args:
            flow: Optical flow array from cv2.calcOpticalFlowFarneback

        Returns:
            Tuple of (MotionType, direction_vector)
        """
        magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])

        mean_magnitude = np.mean(magnitude)
        std_magnitude = np.std(magnitude)

        if mean_magnitude < 0.5:
            return MotionType.STATIC, (0.0, 0.0)

        height, width = flow.shape[:2]
        center_y, center_x = height // 2, width // 2

        flow_x = flow[..., 0]
        flow_y = flow[..., 1]

        mean_flow_x = np.mean(flow_x)
        mean_flow_y = np.mean(flow_y)

        direction_x = mean_flow_x / (mean_magnitude + 1e-6)
        direction_y = mean_flow_y / (mean_magnitude + 1e-6)

        horizontal_dominance = abs(mean_flow_x) / (abs(mean_flow_y) + abs(mean_flow_x) + 1e-6)
        vertical_dominance = abs(mean_flow_y) / (abs(mean_flow_y) + abs(mean_flow_x) + 1e-6)

        y_coords, x_coords = np.meshgrid(
            np.arange(height) - center_y, np.arange(width) - center_x, indexing="ij"
        )
        radial_vectors_x = x_coords / (np.sqrt(x_coords**2 + y_coords**2) + 1e-6)
        radial_vectors_y = y_coords / (np.sqrt(x_coords**2 + y_coords**2) + 1e-6)

        radial_dot = np.mean(flow_x * radial_vectors_x + flow_y * radial_vectors_y)

        tangent_vectors_x = -radial_vectors_y
        tangent_vectors_y = radial_vectors_x
        tangent_dot = np.mean(flow_x * tangent_vectors_x + flow_y * tangent_vectors_y)

        flow_variance = std_magnitude / (mean_magnitude + 1e-6)

        if flow_variance > 1.2 and mean_magnitude > 1.0:
            return MotionType.FPV, (direction_x, direction_y)

        if abs(tangent_dot) > abs(radial_dot) * 1.5 and abs(tangent_dot) > 1.0:
            if tangent_dot > 0:
                return MotionType.ORBIT_CW, (direction_x, direction_y)
            else:
                return MotionType.ORBIT_CCW, (direction_x, direction_y)

        if radial_dot > 2.0:
            return MotionType.FLYOVER, (direction_x, direction_y)
        elif radial_dot < -1.5:
            return MotionType.REVEAL, (direction_x, direction_y)

        if horizontal_dominance > 0.7:
            if mean_flow_x > 0:
                return MotionType.PAN_RIGHT, (direction_x, direction_y)
            else:
                return MotionType.PAN_LEFT, (direction_x, direction_y)
        elif vertical_dominance > 0.7:
            if mean_flow_y > 0:
                return MotionType.TILT_DOWN, (direction_x, direction_y)
            else:
                return MotionType.TILT_UP, (direction_x, direction_y)

        return MotionType.UNKNOWN, (direction_x, direction_y)

    def detect_golden_hour(self, frame: np.ndarray) -> bool:
        """
        Detect golden hour lighting conditions.

        Checks for warm tones, soft contrast, and characteristic color distribution.

        Args:
            frame: Input frame in BGR

        Returns:
            True if golden hour conditions detected
        """
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hue = hsv[:, :, 0]
        saturation = hsv[:, :, 1]
        value = hsv[:, :, 2]

        warm_hue_mask = ((hue >= 0) & (hue <= 30)) | ((hue >= 160) & (hue <= 180))
        warm_pixels = np.sum(warm_hue_mask)
        total_pixels = hue.size
        warm_ratio = warm_pixels / total_pixels

        mean_saturation = np.mean(saturation[warm_hue_mask]) if warm_pixels > 0 else 0
        mean_value = np.mean(value)

        bgr_mean = np.mean(frame, axis=(0, 1))
        b, g, r = bgr_mean
        rg_ratio = r / (g + 1e-6)
        rb_ratio = r / (b + 1e-6)

        is_golden = (
            warm_ratio > 0.3
            and mean_saturation > 80
            and 100 < mean_value < 220
            and rg_ratio > 1.1
            and rb_ratio > 1.2
        )

        return bool(is_golden)

    def extract_dominant_colors(
        self, frame: np.ndarray, n: int = 3
    ) -> list[tuple[int, int, int]]:
        """
        Extract dominant colors using k-means clustering.

        Args:
            frame: Input frame in BGR
            n: Number of dominant colors to extract

        Returns:
            List of (B, G, R) tuples representing dominant colors
        """
        resized = cv2.resize(frame, (150, 150))
        pixels = resized.reshape(-1, 3).astype(np.float32)

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
        _, labels, centers = cv2.kmeans(
            pixels, n, None, criteria, 10, cv2.KMEANS_PP_CENTERS
        )

        centers = centers.astype(int)
        colors = [tuple(map(int, center)) for center in centers]

        return colors

    def calculate_depth_score(self, frame: np.ndarray) -> float:
        """
        Calculate depth/layering score based on edge distribution.

        Analyzes foreground/mid-ground/background separation.

        Args:
            frame: Input frame in BGR

        Returns:
            Depth score from 0-100
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        height, width = gray.shape

        edges = cv2.Canny(gray, 50, 150)

        top_third = edges[: height // 3, :]
        mid_third = edges[height // 3 : 2 * height // 3, :]
        bottom_third = edges[2 * height // 3 :, :]

        top_density = np.sum(top_third) / top_third.size
        mid_density = np.sum(mid_third) / mid_third.size
        bottom_density = np.sum(bottom_third) / bottom_third.size

        layer_variance = np.var([top_density, mid_density, bottom_density])

        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        focus_map = cv2.Laplacian(blurred, cv2.CV_64F)
        focus_variance = np.var(focus_map)

        depth_score = min((layer_variance * 1000 + focus_variance / 100) / 2, 100.0)

        return depth_score

    def calculate_motion_smoothness(self, flow_history: list[np.ndarray]) -> float:
        """
        Calculate motion smoothness from flow history.

        Args:
            flow_history: List of optical flow arrays over time

        Returns:
            Smoothness score from 0-100, higher is smoother
        """
        if len(flow_history) < 2:
            return 50.0

        magnitudes = []
        for flow in flow_history:
            magnitude, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
            magnitudes.append(np.mean(magnitude))

        magnitude_array = np.array(magnitudes)
        mean_magnitude = np.mean(magnitude_array)

        if mean_magnitude < 1e-6:
            return 100.0

        variance = np.var(magnitude_array)
        coefficient_of_variation = np.sqrt(variance) / (mean_magnitude + 1e-6)

        smoothness = max(0, 100 - coefficient_of_variation * 50)

        return min(smoothness, 100.0)

    def detect_scenes_enhanced(self, video_path: Path) -> list[EnhancedSceneInfo]:
        """
        Detect scenes with enhanced motion and visual analysis.

        Args:
            video_path: Path to the video file

        Returns:
            List of EnhancedSceneInfo objects
        """
        base_scenes = self.detect_scenes(video_path)

        enhanced_scenes = []

        for scene in base_scenes:
            cap = cv2.VideoCapture(str(video_path))
            fps = cap.get(cv2.CAP_PROP_FPS)

            start_frame = int(scene.start_time * fps)
            end_frame = int(scene.end_time * fps)

            sample_interval = max(1, (end_frame - start_frame) // 20)
            sample_frames = list(range(start_frame, end_frame, sample_interval))

            if not sample_frames or sample_frames[-1] != end_frame - 1:
                sample_frames.append(end_frame - 1)

            flow_history = []
            prev_gray = None
            motion_types = []
            motion_directions = []
            motion_energies = []  # Track motion energy per frame
            is_golden_samples = []
            depth_samples = []
            hook_potentials = []
            subject_scores = []

            mid_frame_idx = len(sample_frames) // 2
            dominant_colors = []

            for idx, frame_num in enumerate(sample_frames):
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
                ret, frame = cap.read()
                if not ret:
                    continue

                # Downscale for analysis (scoring is scale-invariant)
                if self.analysis_scale < 1.0:
                    analysis_frame = cv2.resize(
                        frame, (0, 0),
                        fx=self.analysis_scale, fy=self.analysis_scale,
                        interpolation=cv2.INTER_AREA,
                    )
                else:
                    analysis_frame = frame

                curr_gray = cv2.cvtColor(analysis_frame, cv2.COLOR_BGR2GRAY)

                if idx == mid_frame_idx:
                    dominant_colors = self.extract_dominant_colors(analysis_frame)

                is_golden_samples.append(self.detect_golden_hour(analysis_frame))
                depth_samples.append(self.calculate_depth_score(analysis_frame))

                # Compute hook potential metrics at sampled frames
                subj_score, _ = self._calculate_subject_score(analysis_frame)
                color_var = self._calculate_color_variance(analysis_frame)
                comp_score = self._calculate_composition(analysis_frame)
                subject_scores.append(subj_score)

                if prev_gray is not None:
                    flow = cv2.calcOpticalFlowFarneback(
                        prev_gray,
                        curr_gray,
                        None,
                        pyr_scale=0.5,
                        levels=3,
                        winsize=15,
                        iterations=3,
                        poly_n=5,
                        poly_sigma=1.2,
                        flags=0,
                    )
                    flow_history.append(flow)

                    motion_type, direction = self.classify_camera_motion(flow)
                    motion_types.append(motion_type)
                    motion_directions.append(direction)

                    # Calculate motion energy from optical flow
                    motion_score = self._calculate_motion_optical_flow(prev_gray, analysis_frame)
                    motion_energies.append(motion_score)

                    # Compute hook potential using available metrics
                    hook_score, _ = self._calculate_hook_potential(
                        analysis_frame, subj_score, motion_score, color_var, comp_score
                    )
                    hook_potentials.append(hook_score)

                prev_gray = curr_gray

            cap.release()

            if motion_types:
                motion_counts = {}
                for mt in motion_types:
                    motion_counts[mt] = motion_counts.get(mt, 0) + 1
                dominant_motion = max(motion_counts, key=motion_counts.get)
            else:
                dominant_motion = MotionType.STATIC

            if motion_directions:
                avg_direction = (
                    np.mean([d[0] for d in motion_directions]),
                    np.mean([d[1] for d in motion_directions]),
                )
            else:
                avg_direction = (0.0, 0.0)

            smoothness = self.calculate_motion_smoothness(flow_history)

            is_golden = sum(is_golden_samples) / len(is_golden_samples) > 0.5 if is_golden_samples else False

            depth_score = np.mean(depth_samples) if depth_samples else 0.0

            # Calculate average motion energy (0-100 scale)
            avg_motion_energy = np.mean(motion_energies) if motion_energies else 0.0

            # Calculate hook potential and tier from sampled data
            avg_hook = float(np.mean(hook_potentials)) if hook_potentials else 0.0
            avg_subject = float(np.mean(subject_scores)) if subject_scores else 0.0
            if avg_hook >= 80:
                hook_tier = HookPotential.MAXIMUM
            elif avg_hook >= 65:
                hook_tier = HookPotential.HIGH
            elif avg_hook >= 45:
                hook_tier = HookPotential.MEDIUM
            elif avg_hook >= 25:
                hook_tier = HookPotential.LOW
            else:
                hook_tier = HookPotential.POOR

            enhanced_scene = EnhancedSceneInfo(
                start_time=scene.start_time,
                end_time=scene.end_time,
                duration=scene.duration,
                score=scene.score,
                source_file=scene.source_file,
                thumbnail=scene.thumbnail,
                motion_type=dominant_motion,
                motion_direction=avg_direction,
                motion_smoothness=smoothness,
                motion_energy=avg_motion_energy,
                is_golden_hour=is_golden,
                dominant_colors=dominant_colors,
                depth_score=depth_score,
                subject_score=avg_subject,
                hook_potential=avg_hook,
                hook_tier=hook_tier,
            )

            enhanced_scenes.append(enhanced_scene)

        return enhanced_scenes
