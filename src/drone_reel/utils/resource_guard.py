"""Resource preflight checks for video rendering.

Validates system resources (memory, disk space) before starting
expensive rendering operations to prevent system crashes.
"""

import os
import platform
import shutil
import subprocess
from pathlib import Path
from typing import Optional


def check_available_memory_mb() -> float:
    """Return available physical memory in MB.

    On macOS: parses vm_stat for free + inactive pages.
    On Linux: reads MemAvailable from /proc/meminfo.
    Returns float('inf') if detection fails (fail-open).
    """
    system = platform.system()
    try:
        if system == "Darwin":
            # Get page size
            page_size_result = subprocess.run(
                ["sysctl", "-n", "hw.pagesize"],
                capture_output=True, text=True, timeout=5,
            )
            page_size = int(page_size_result.stdout.strip())

            # Get vm_stat
            result = subprocess.run(
                ["vm_stat"], capture_output=True, text=True, timeout=5,
            )
            free_pages = 0
            for line in result.stdout.splitlines():
                if "Pages free" in line or "Pages inactive" in line:
                    # Parse "Pages free:    12345." format
                    value = line.split(":")[1].strip().rstrip(".")
                    free_pages += int(value)
            return (free_pages * page_size) / (1024 * 1024)

        elif system == "Linux":
            with open("/proc/meminfo") as f:
                for line in f:
                    if line.startswith("MemAvailable:"):
                        return int(line.split()[1]) / 1024  # kB to MB
    except Exception:
        pass
    return float("inf")


def check_disk_space_mb(path: Path) -> float:
    """Return free disk space in MB at the given path.

    Args:
        path: Path to check disk space for (uses its mount point).

    Returns:
        Free space in MB, or float('inf') if detection fails.
    """
    try:
        # Resolve to existing parent if path doesn't exist yet
        check_path = path
        while not check_path.exists() and check_path.parent != check_path:
            check_path = check_path.parent
        usage = shutil.disk_usage(str(check_path))
        return usage.free / (1024 * 1024)
    except Exception:
        return float("inf")


def estimate_render_memory_mb(
    resolution_height: int,
    fps: int = 30,
    clip_count: int = 10,
    stabilize: bool = False,
    avg_clip_duration: float = 3.0,
) -> float:
    """Estimate peak memory usage for a render in MB.

    Args:
        resolution_height: Output height in pixels (e.g., 2160 for 4K).
        fps: Frames per second.
        clip_count: Number of clips in the reel.
        stabilize: Whether stabilization is enabled.
        avg_clip_duration: Average clip duration in seconds.

    Returns:
        Estimated peak memory in MB.
    """
    # Frame size: height * width * 3 channels (assuming 9:16 vertical)
    width = int(resolution_height * 9 / 16)
    frame_bytes = resolution_height * width * 3
    frame_mb = frame_bytes / (1024 * 1024)

    # Base: MoviePy clip references (lazy, but metadata + file handles)
    base_mb = 200  # MoviePy overhead, Python runtime
    clip_refs_mb = clip_count * 20  # ~20 MB per clip reference/metadata

    # Encoding buffer: FFmpeg uses ~2-4 frames for encoding
    encode_buffer_mb = frame_mb * 4

    # Stabilization: analysis holds 2 frames (current + previous gray)
    # plus the transform arrays
    if stabilize:
        stab_mb = frame_mb * 3  # Current frame + gray + transform temps
        # Transform arrays are small: n_frames * 3 * 8 bytes
        stab_mb += (fps * avg_clip_duration * 3 * 8) / (1024 * 1024)
    else:
        stab_mb = 0

    # Color grading: holds 1 frame + conversion temps
    color_grade_mb = frame_mb * 3  # BGR + HSV + LAB temps

    # Reframing: 1 frame + resize buffer
    reframe_mb = frame_mb * 2

    total = base_mb + clip_refs_mb + encode_buffer_mb + stab_mb + color_grade_mb + reframe_mb

    return total


def estimate_output_size_mb(
    duration: float,
    video_bitrate: str = "15M",
) -> float:
    """Estimate output file size in MB.

    Args:
        duration: Video duration in seconds.
        video_bitrate: Video bitrate string (e.g., "15M", "80M").

    Returns:
        Estimated file size in MB.
    """
    # Parse bitrate string
    bitrate_str = video_bitrate.upper().replace("K", "000").replace("M", "000000")
    try:
        bitrate_bps = int(bitrate_str)
    except ValueError:
        bitrate_bps = 15_000_000  # Default 15 Mbps

    # Size = bitrate * duration / 8 (bits to bytes)
    size_bytes = bitrate_bps * duration / 8
    return size_bytes / (1024 * 1024)


def preflight_check(
    output_path: Path,
    resolution_height: int = 1080,
    fps: int = 30,
    clip_count: int = 10,
    stabilize: bool = False,
    video_bitrate: str = "15M",
    duration: float = 15.0,
) -> list[dict]:
    """Run resource preflight checks before rendering.

    Returns a list of issues found. Empty list means all clear.
    Each issue is a dict with 'level' ('warning' or 'error') and 'message'.

    Args:
        output_path: Where the output video will be written.
        resolution_height: Output height in pixels.
        fps: Output frames per second.
        clip_count: Expected number of clips.
        stabilize: Whether stabilization will be used.
        video_bitrate: Video bitrate string.
        duration: Target reel duration in seconds.

    Returns:
        List of dicts with 'level' and 'message' keys.
    """
    issues = []

    # Check available memory
    available_mb = check_available_memory_mb()
    estimated_mb = estimate_render_memory_mb(
        resolution_height=resolution_height,
        fps=fps,
        clip_count=clip_count,
        stabilize=stabilize,
    )

    if available_mb != float("inf"):
        if estimated_mb > available_mb * 0.95:
            issues.append({
                "level": "error",
                "message": (
                    f"Insufficient memory: estimated {estimated_mb:.0f} MB needed, "
                    f"only {available_mb:.0f} MB available. "
                    "Close other applications or reduce resolution/clip count."
                ),
            })
        elif estimated_mb > available_mb * 0.7:
            issues.append({
                "level": "warning",
                "message": (
                    f"Memory may be tight: estimated {estimated_mb:.0f} MB needed, "
                    f"{available_mb:.0f} MB available. "
                    "Consider closing other applications."
                ),
            })

    # Check disk space
    output_size_mb = estimate_output_size_mb(duration, video_bitrate)
    # Need ~2x for temp files during encoding
    required_disk_mb = output_size_mb * 2
    available_disk_mb = check_disk_space_mb(output_path)

    if available_disk_mb != float("inf"):
        if required_disk_mb > available_disk_mb * 0.95:
            issues.append({
                "level": "error",
                "message": (
                    f"Insufficient disk space: estimated {required_disk_mb:.0f} MB needed, "
                    f"only {available_disk_mb:.0f} MB available."
                ),
            })
        elif required_disk_mb > available_disk_mb * 0.5:
            issues.append({
                "level": "warning",
                "message": (
                    f"Disk space may be tight: estimated {required_disk_mb:.0f} MB needed, "
                    f"{available_disk_mb:.0f} MB available."
                ),
            })

    return issues
