"""
Scene analysis for motion energy, brightness, shake detection, and sharpness.

Extracts per-scene visual metrics used for filtering and duration adjustment.
"""

import os
from concurrent.futures import ThreadPoolExecutor

import cv2
import numpy as np

from drone_reel.core.scene_detector import MotionType, SceneInfo


def classify_motion_type(
    flow_vectors: list[tuple[float, float]],
    motion_energy: float,
    static_threshold: float = 10.0,
) -> tuple[MotionType, tuple[float, float]]:
    """
    Classify camera motion from optical flow vectors.

    Analyzes the dominant direction of motion across sampled frame pairs
    to determine the camera movement type.

    Args:
        flow_vectors: List of (mean_dx, mean_dy) flow vectors per frame pair
        motion_energy: Overall motion energy score (0-100)
        static_threshold: Motion energy below this is classified as STATIC

    Returns:
        Tuple of (MotionType, average_direction)
    """
    if not flow_vectors or motion_energy < static_threshold:
        return MotionType.STATIC, (0.0, 0.0)

    avg_dx = float(np.mean([v[0] for v in flow_vectors]))
    avg_dy = float(np.mean([v[1] for v in flow_vectors]))

    # Check flow consistency - high variance means chaotic/FPV motion
    dx_std = float(np.std([v[0] for v in flow_vectors]))
    dy_std = float(np.std([v[1] for v in flow_vectors]))
    consistency = 1.0 / (1.0 + dx_std + dy_std)

    magnitude = np.sqrt(avg_dx**2 + avg_dy**2)

    if magnitude < 0.5:
        return MotionType.STATIC, (avg_dx, avg_dy)

    # Very inconsistent motion = FPV or chaotic
    if consistency < 0.15 and motion_energy > 40:
        return MotionType.FPV, (avg_dx, avg_dy)

    # Check for rotational motion (orbit) by analyzing flow field variance
    # Orbits have consistent magnitude but varying direction across the frame
    dx_values = [v[0] for v in flow_vectors]
    if len(dx_values) >= 3:
        direction_changes = sum(
            1 for i in range(1, len(dx_values)) if (dx_values[i] > 0) != (dx_values[i - 1] > 0)
        )
        if direction_changes >= len(dx_values) * 0.4:
            # Frequent direction reversals suggest orbit or reveal
            if avg_dy > 0.5:
                return MotionType.REVEAL, (avg_dx, avg_dy)
            elif avg_dx > 0:
                return MotionType.ORBIT_CW, (avg_dx, avg_dy)
            else:
                return MotionType.ORBIT_CCW, (avg_dx, avg_dy)

    # Classify by dominant direction
    # Horizontal dominance
    if abs(avg_dx) > abs(avg_dy) * 1.5:
        if avg_dx > 0:
            return MotionType.PAN_RIGHT, (avg_dx, avg_dy)
        else:
            return MotionType.PAN_LEFT, (avg_dx, avg_dy)

    # Vertical dominance
    if abs(avg_dy) > abs(avg_dx) * 1.5:
        if avg_dy > 0:
            return MotionType.TILT_DOWN, (avg_dx, avg_dy)
        else:
            return MotionType.TILT_UP, (avg_dx, avg_dy)

    # Combined forward + downward = flyover
    if avg_dy > 0 and motion_energy > 30:
        return MotionType.FLYOVER, (avg_dx, avg_dy)

    # Forward motion with upward tilt = approach
    if avg_dy < 0 and motion_energy > 25:
        return MotionType.APPROACH, (avg_dx, avg_dy)

    return MotionType.UNKNOWN, (avg_dx, avg_dy)


def analyze_scene_motion(
    scene: SceneInfo,
    include_sharpness: bool = False,
    motion_energy_method: str = "mean",
    *,
    flow_winsize: int = 15,
    flow_levels: int = 2,
    motion_energy_percentile: int = 50,
) -> (
    tuple[float, float, float, MotionType, tuple[float, float]]
    | tuple[float, float, float, MotionType, tuple[float, float], float]
):
    """
    Analyze motion energy, brightness, shake score, and motion type for a scene.

    Uses optical flow to measure motion characteristics. Shake detection uses
    flow variance - shaky footage has erratic, inconsistent motion vectors while
    smooth footage (even fast pans) has consistent flow patterns.

    When include_sharpness=True, also computes sharpness at the midpoint frame
    in the same video capture pass, avoiding a separate file open.

    Args:
        scene: Scene to analyze
        include_sharpness: If True, also compute and return sharpness
        motion_energy_method: How to aggregate per-frame motion scores.
            "mean" (default): np.mean — standard average energy.
            "median": np.median — robust to outlier frames.
            "p95": np.percentile(scores, 95) — catches peak motion in mixed clips.
            "percentile": np.percentile(scores, motion_energy_percentile).
        flow_winsize: Window size for Farneback optical flow (5-31, default 15).
        flow_levels: Pyramid levels for Farneback optical flow (1-4, default 2).
        motion_energy_percentile: Percentile to use when motion_energy_method="percentile"
            (50-99, default 50).

    Returns:
        If include_sharpness=False:
            Tuple of (motion_energy: 0-100, mean_brightness: 0-255,
                      shake_score: 0-100, motion_type, motion_direction)
        If include_sharpness=True:
            Tuple of (motion_energy, mean_brightness, shake_score,
                      motion_type, motion_direction, sharpness)
    """
    try:
        cap = cv2.VideoCapture(str(scene.source_file))
        fps = cap.get(cv2.CAP_PROP_FPS) or 30

        start_frame = int(scene.start_time * fps)
        end_frame = int(scene.end_time * fps)
        mid_frame = int(scene.midpoint * fps)

        # Sample 5 frame pairs evenly across scene
        sample_interval = max(1, (end_frame - start_frame) // 6)
        sample_frames = list(range(start_frame, end_frame, sample_interval))[:6]

        # Ensure midpoint frame is in the sample list for sharpness calculation
        if include_sharpness and mid_frame not in sample_frames:
            sample_frames.append(mid_frame)
            sample_frames.sort()

        motion_scores = []
        brightness_values = []
        flow_variances = []
        flow_vectors = []
        prev_gray = None
        prev_mean_flow = None
        sharpness = 0.0

        for frame_num in sample_frames:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
            ret, frame = cap.read()
            if not ret:
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_small = cv2.resize(gray, (320, 180))

            brightness_values.append(float(np.mean(gray)))

            # Compute sharpness at midpoint frame (reuse the already-read frame)
            if include_sharpness and frame_num == mid_frame:
                laplacian = cv2.Laplacian(gray, cv2.CV_64F)
                sharpness = float(laplacian.var())

            if prev_gray is not None:
                flow = cv2.calcOpticalFlowFarneback(
                    prev_gray,
                    gray_small,
                    None,
                    pyr_scale=0.5,
                    levels=flow_levels,
                    winsize=flow_winsize,
                    iterations=2,
                    poly_n=5,
                    poly_sigma=1.1,
                    flags=0,
                )
                magnitude = cv2.magnitude(flow[..., 0], flow[..., 1])
                motion_score = min(float(magnitude.mean()) / 3.0 * 100, 100.0)
                motion_scores.append(motion_score)

                # Track mean flow direction for motion classification
                mean_dx = float(np.mean(flow[..., 0]))
                mean_dy = float(np.mean(flow[..., 1]))
                flow_vectors.append((mean_dx, mean_dy))

                # Shake detection: measure flow variance and direction consistency
                flow_std = float(np.std(magnitude))
                mean_flow = (mean_dx, mean_dy)

                if prev_mean_flow is not None:
                    direction_change = np.sqrt(
                        (mean_flow[0] - prev_mean_flow[0]) ** 2
                        + (mean_flow[1] - prev_mean_flow[1]) ** 2
                    )
                    flow_variances.append(flow_std + direction_change * 2)

                prev_mean_flow = mean_flow

            prev_gray = gray_small

        cap.release()

        if motion_scores:
            if motion_energy_method == "median":
                motion_energy = float(np.median(motion_scores))
            elif motion_energy_method == "p95":
                motion_energy = float(np.percentile(motion_scores, 95))
            elif motion_energy_method == "percentile":
                motion_energy = float(np.percentile(motion_scores, motion_energy_percentile))
            else:  # "mean" (default)
                motion_energy = float(np.mean(motion_scores))
        else:
            motion_energy = 0.0
        mean_brightness = float(np.mean(brightness_values)) if brightness_values else 127.0

        # Calculate shake score (0-100)
        raw_shake = float(np.mean(flow_variances)) if flow_variances else 0.0
        shake_score = min(raw_shake * 5.0, 100.0)

        # Classify motion type from flow vectors
        motion_type, motion_direction = classify_motion_type(flow_vectors, motion_energy)

        if include_sharpness:
            return (
                motion_energy,
                mean_brightness,
                shake_score,
                motion_type,
                motion_direction,
                sharpness,
            )
        return (motion_energy, mean_brightness, shake_score, motion_type, motion_direction)
    except Exception:
        if include_sharpness:
            return (0.0, 127.0, 0.0, MotionType.UNKNOWN, (0.0, 0.0), 0.0)
        return (0.0, 127.0, 0.0, MotionType.UNKNOWN, (0.0, 0.0))


def get_scene_sharpness(scene: SceneInfo) -> float:
    """
    Calculate sharpness of scene midpoint frame using Laplacian variance.

    Args:
        scene: Scene to analyze

    Returns:
        Sharpness value (higher = sharper). Typical range 0-1000+.
    """
    try:
        cap = cv2.VideoCapture(str(scene.source_file))
        fps = cap.get(cv2.CAP_PROP_FPS) or 30
        mid_frame = int(scene.midpoint * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, mid_frame)
        ret, frame = cap.read()
        cap.release()
        if ret and frame is not None:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            return float(laplacian.var())
    except Exception:
        pass
    return 0.0


def _analyze_single_scene(
    scene: SceneInfo,
    include_sharpness: bool,
    motion_energy_method: str = "mean",
    *,
    flow_winsize: int = 15,
    flow_levels: int = 2,
    motion_energy_percentile: int = 50,
) -> tuple[int, dict]:
    """Analyze a single scene and return (id, result_dict). Used by batch processing."""
    scene_id = id(scene)
    result = analyze_scene_motion(
        scene,
        include_sharpness=include_sharpness,
        motion_energy_method=motion_energy_method,
        flow_winsize=flow_winsize,
        flow_levels=flow_levels,
        motion_energy_percentile=motion_energy_percentile,
    )
    if include_sharpness:
        motion_energy, brightness, shake_score, motion_type, motion_direction, sharpness = result
        return scene_id, {
            "motion_energy": motion_energy,
            "brightness": brightness,
            "shake_score": shake_score,
            "motion_type": motion_type,
            "motion_direction": motion_direction,
            "sharpness": sharpness,
        }
    else:
        motion_energy, brightness, shake_score, motion_type, motion_direction = result
        return scene_id, {
            "motion_energy": motion_energy,
            "brightness": brightness,
            "shake_score": shake_score,
            "motion_type": motion_type,
            "motion_direction": motion_direction,
        }


def analyze_scenes_batch(
    scenes: list[SceneInfo],
    include_sharpness: bool = False,
    max_workers: int | None = None,
    motion_energy_method: str = "mean",
    *,
    flow_winsize: int = 15,
    flow_levels: int = 2,
    motion_energy_percentile: int = 50,
) -> dict[int, dict]:
    """
    Analyze a batch of scenes in parallel using ThreadPoolExecutor.

    Each scene opens its own cv2.VideoCapture independently, so they can
    safely run concurrently. When include_sharpness=True, also computes
    sharpness in the same pass, avoiding a separate file open per scene.

    Args:
        scenes: List of scenes to analyze
        include_sharpness: If True, include sharpness in results
        max_workers: Max threads (default: min(4, cpu_count))
        motion_energy_method: How to aggregate per-frame motion scores.
            "mean" (default): np.mean — standard average energy.
            "median": np.median — robust to outlier frames.
            "p95": np.percentile(scores, 95) — catches peak motion in mixed clips.
            "percentile": np.percentile(scores, motion_energy_percentile).
        flow_winsize: Window size for Farneback optical flow (5-31, default 15).
        flow_levels: Pyramid levels for Farneback optical flow (1-4, default 2).
        motion_energy_percentile: Percentile to use when motion_energy_method="percentile"
            (50-99, default 50).

    Returns:
        Dictionary keyed by id(scene) with analysis results:
        {id(scene): {"motion_energy": float, "brightness": float,
                      "shake_score": float, "motion_type": MotionType,
                      "motion_direction": (float, float),
                      "sharpness": float (only if include_sharpness=True)}}
    """
    if not scenes:
        return {}

    if max_workers is None:
        max_workers = min(4, os.cpu_count() or 1)

    # For small batches or single scene, skip thread overhead
    if len(scenes) <= 1 or max_workers <= 1:
        results = {}
        for scene in scenes:
            scene_id, result_dict = _analyze_single_scene(
                scene,
                include_sharpness,
                motion_energy_method,
                flow_winsize=flow_winsize,
                flow_levels=flow_levels,
                motion_energy_percentile=motion_energy_percentile,
            )
            results[scene_id] = result_dict
        return results

    results = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(
                _analyze_single_scene,
                scene,
                include_sharpness,
                motion_energy_method,
                flow_winsize=flow_winsize,
                flow_levels=flow_levels,
                motion_energy_percentile=motion_energy_percentile,
            ): scene
            for scene in scenes
        }
        for future in futures:
            scene_id, result_dict = future.result()
            results[scene_id] = result_dict

    return results
