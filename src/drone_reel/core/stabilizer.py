"""
Video stabilization for drone footage.

Uses OpenCV feature tracking and perspective transforms to reduce
camera shake while preserving intentional camera movements.
"""

import cv2
import numpy as np
from typing import Optional, Callable


def stabilize_clip(
    clip,
    smoothing_radius: int = 30,
    border_crop: float = 0.05,
    progress_callback: Optional[Callable[[float], None]] = None,
):
    """
    Stabilize a MoviePy video clip using feature-based tracking.

    This uses a rolling average of frame transforms to smooth out
    camera shake while preserving intentional camera movements like
    pans and tilts.

    Args:
        clip: MoviePy VideoClip to stabilize
        smoothing_radius: Number of frames to average for smoothing (default 30)
        border_crop: Fraction of frame to crop for stabilization margin (default 5%)
        progress_callback: Optional callback for progress updates (0.0 to 1.0)

    Returns:
        Stabilized MoviePy VideoClip
    """
    # Get clip properties
    fps = clip.fps
    n_frames = int(clip.duration * fps)
    w, h = clip.size

    if n_frames < 3:
        return clip  # Too short to stabilize

    # Phase 1: Analyze motion and build transform trajectory
    transforms = []
    prev_gray = None

    # Feature detection parameters
    feature_params = dict(
        maxCorners=200,
        qualityLevel=0.01,
        minDistance=30,
        blockSize=3
    )

    for i in range(n_frames):
        frame = clip.get_frame(i / fps)
        # Handle both uint8 (0-255) and float (0-1) frame formats
        is_float = frame.dtype in (np.float32, np.float64) and frame.max() <= 1.0
        if is_float:
            frame_uint8 = (frame * 255).astype(np.uint8)
        else:
            frame_uint8 = frame.astype(np.uint8)
        gray = cv2.cvtColor(frame_uint8, cv2.COLOR_RGB2GRAY)

        if prev_gray is not None:
            # Detect features in previous frame
            prev_pts = cv2.goodFeaturesToTrack(prev_gray, **feature_params)

            if prev_pts is not None and len(prev_pts) > 0:
                # Track features to current frame
                curr_pts, status, _ = cv2.calcOpticalFlowPyrLK(
                    prev_gray, gray, prev_pts, None
                )

                # Filter valid points
                valid = status.flatten() == 1
                if np.sum(valid) >= 4:
                    prev_valid = prev_pts[valid]
                    curr_valid = curr_pts[valid]

                    # Estimate affine transform (translation, rotation, scale)
                    transform_matrix, _ = cv2.estimateAffinePartial2D(
                        prev_valid, curr_valid
                    )

                    if transform_matrix is not None:
                        # Extract translation
                        dx = transform_matrix[0, 2]
                        dy = transform_matrix[1, 2]
                        # Extract rotation angle
                        da = np.arctan2(transform_matrix[1, 0], transform_matrix[0, 0])
                        transforms.append([dx, dy, da])
                    else:
                        transforms.append([0, 0, 0])
                else:
                    transforms.append([0, 0, 0])
            else:
                transforms.append([0, 0, 0])

        prev_gray = gray

        if progress_callback:
            progress_callback(0.5 * (i + 1) / n_frames)

    if len(transforms) == 0:
        return clip

    transforms = np.array(transforms)

    # Phase 2: Compute cumulative trajectory and smooth it
    trajectory = np.cumsum(transforms, axis=0)

    # Apply moving average smoothing
    smoothed_trajectory = smooth_trajectory(trajectory, smoothing_radius)

    # Calculate the difference (correction) needed
    difference = smoothed_trajectory - trajectory

    # Pad the difference array to match frame count
    if len(difference) < n_frames - 1:
        pad_size = (n_frames - 1) - len(difference)
        difference = np.vstack([difference, np.zeros((pad_size, 3))])

    # Phase 3: Apply stabilization transforms
    def make_frame(t):
        frame_idx = int(t * fps)
        frame = clip.get_frame(t)

        if frame_idx >= len(difference):
            return frame

        # Get correction for this frame
        dx, dy, da = difference[frame_idx]

        # Build transform matrix
        cos_a = np.cos(da)
        sin_a = np.sin(da)

        # Center of frame
        cx, cy = w / 2, h / 2

        # Affine transform: rotate around center, then translate
        transform_matrix = np.array([
            [cos_a, -sin_a, dx + cx * (1 - cos_a) + cy * sin_a],
            [sin_a, cos_a, dy + cx * (-sin_a) + cy * (1 - cos_a)]
        ], dtype=np.float32)

        # Handle both uint8 (0-255) and float (0-1) frame formats
        is_float = frame.dtype in (np.float32, np.float64) and frame.max() <= 1.0
        if is_float:
            frame_uint8 = (frame * 255).astype(np.uint8)
        else:
            frame_uint8 = frame.astype(np.uint8)

        # Apply transform
        stabilized = cv2.warpAffine(
            frame_uint8, transform_matrix, (w, h),
            borderMode=cv2.BORDER_REPLICATE
        )

        # Crop borders to hide edge artifacts
        crop_x = int(w * border_crop)
        crop_y = int(h * border_crop)

        if crop_x > 0 and crop_y > 0:
            cropped = stabilized[crop_y:-crop_y, crop_x:-crop_x]
            # Resize back to original size
            stabilized = cv2.resize(cropped, (w, h))

        # Return in same format as input
        if is_float:
            return stabilized.astype(np.float32) / 255.0
        else:
            return stabilized

    # Create new clip with stabilized frames
    from moviepy import VideoClip

    stabilized_clip = VideoClip(make_frame, duration=clip.duration)
    stabilized_clip = stabilized_clip.with_fps(fps)

    if clip.audio is not None:
        stabilized_clip = stabilized_clip.with_audio(clip.audio)

    if progress_callback:
        progress_callback(1.0)

    return stabilized_clip


def smooth_trajectory(trajectory: np.ndarray, radius: int) -> np.ndarray:
    """
    Apply moving average smoothing to trajectory.

    Args:
        trajectory: Array of shape (N, 3) with [dx, dy, da] per frame
        radius: Smoothing window radius

    Returns:
        Smoothed trajectory of same shape
    """
    smoothed = np.copy(trajectory)

    for i in range(len(trajectory)):
        start = max(0, i - radius)
        end = min(len(trajectory), i + radius + 1)
        smoothed[i] = np.mean(trajectory[start:end], axis=0)

    return smoothed


def calculate_shake_score(clip, sample_frames: int = 10) -> float:
    """
    Calculate a shake score for a video clip.

    Args:
        clip: MoviePy VideoClip
        sample_frames: Number of frames to sample

    Returns:
        Shake score from 0 (stable) to 100 (very shaky)
    """
    fps = clip.fps
    duration = clip.duration

    if duration < 0.5:
        return 0.0

    # Sample frames evenly
    times = np.linspace(0, duration - 0.1, sample_frames)

    flow_variances = []
    prev_gray = None
    prev_mean_flow = None

    for t in times:
        frame = clip.get_frame(t)
        frame_uint8 = (frame * 255).astype(np.uint8)
        gray = cv2.cvtColor(frame_uint8, cv2.COLOR_RGB2GRAY)
        gray = cv2.resize(gray, (320, 180))

        if prev_gray is not None:
            flow = cv2.calcOpticalFlowFarneback(
                prev_gray, gray, None,
                pyr_scale=0.5, levels=2, winsize=15,
                iterations=2, poly_n=5, poly_sigma=1.1, flags=0
            )

            magnitude = cv2.magnitude(flow[..., 0], flow[..., 1])
            flow_std = float(np.std(magnitude))
            mean_flow = (float(np.mean(flow[..., 0])), float(np.mean(flow[..., 1])))

            if prev_mean_flow is not None:
                direction_change = np.sqrt(
                    (mean_flow[0] - prev_mean_flow[0])**2 +
                    (mean_flow[1] - prev_mean_flow[1])**2
                )
                flow_variances.append(flow_std + direction_change * 2)

            prev_mean_flow = mean_flow

        prev_gray = gray

    if not flow_variances:
        return 0.0

    raw_shake = float(np.mean(flow_variances))
    return min(raw_shake * 5.0, 100.0)
