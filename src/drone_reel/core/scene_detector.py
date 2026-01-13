"""
Scene detection and highlight extraction for drone footage.

Uses PySceneDetect for scene boundary detection and OpenCV for
visual quality scoring to identify the most compelling moments.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import cv2
import numpy as np
from scenedetect import ContentDetector, SceneManager, open_video


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
    ):
        """
        Initialize the scene detector.

        Args:
            threshold: Sensitivity for scene detection (lower = more scenes)
            min_scene_length: Minimum scene duration in seconds
            max_scene_length: Maximum scene duration in seconds
        """
        self.threshold = threshold
        self.min_scene_length = min_scene_length
        self.max_scene_length = max_scene_length

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

        scene_manager.detect_scenes(video)
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
        - Sharpness (laplacian variance)
        - Color variance (saturation spread)
        - Motion estimation (frame difference)
        - Brightness balance (not too dark/bright)

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
        mid_frame = (start_frame + end_frame) // 2

        sample_frames = [start_frame, mid_frame, end_frame]
        scores = []

        prev_frame = None
        for frame_num in sample_frames:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
            ret, frame = cap.read()
            if not ret:
                continue

            sharpness = self._calculate_sharpness(frame)
            color_score = self._calculate_color_variance(frame)
            brightness_score = self._calculate_brightness_balance(frame)

            motion_score = 0.0
            if prev_frame is not None:
                motion_score = self._calculate_motion(prev_frame, frame)

            frame_score = (
                sharpness * 0.3 + color_score * 0.25 + brightness_score * 0.25 + motion_score * 0.2
            )
            scores.append(frame_score)
            prev_frame = frame

        cap.release()

        return np.mean(scores) if scores else 0.0

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

    def _calculate_motion(self, prev_frame: np.ndarray, curr_frame: np.ndarray) -> float:
        """Estimate motion between frames."""
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(prev_gray, curr_gray)
        motion = np.mean(diff)
        return min(motion / 30.0 * 100, 100.0)

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
