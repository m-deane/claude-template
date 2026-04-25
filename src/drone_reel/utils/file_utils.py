"""File handling utilities for drone reel processing."""

import tempfile
from pathlib import Path

VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v", ".wmv", ".flv"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac", ".wma"}


def find_video_files(directory: Path, recursive: bool = False) -> list[Path]:
    """
    Find all video files in a directory.

    Args:
        directory: Directory to search
        recursive: Whether to search subdirectories

    Returns:
        List of paths to video files, sorted by name
    """
    if not directory.exists():
        return []

    if recursive:
        pattern = "**/*"
    else:
        pattern = "*"

    video_files = []
    for path in directory.glob(pattern):
        if path.is_file() and path.suffix.lower() in VIDEO_EXTENSIONS:
            video_files.append(path)

    return sorted(video_files)


def find_audio_files(directory: Path, recursive: bool = False) -> list[Path]:
    """
    Find all audio files in a directory.

    Args:
        directory: Directory to search
        recursive: Whether to search subdirectories

    Returns:
        List of paths to audio files, sorted by name
    """
    if not directory.exists():
        return []

    if recursive:
        pattern = "**/*"
    else:
        pattern = "*"

    audio_files = []
    for path in directory.glob(pattern):
        if path.is_file() and path.suffix.lower() in AUDIO_EXTENSIONS:
            audio_files.append(path)

    return sorted(audio_files)


def ensure_output_dir(output_path: Path) -> Path:
    """
    Ensure the output directory exists.

    Args:
        output_path: Path to output file or directory

    Returns:
        Path to the output directory
    """
    if output_path.suffix:
        output_dir = output_path.parent
    else:
        output_dir = output_path

    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def get_temp_path(suffix: str = ".mp4") -> Path:
    """
    Get a temporary file path.

    Args:
        suffix: File extension for the temp file

    Returns:
        Path to a temporary file
    """
    temp_dir = Path(tempfile.gettempdir()) / "drone_reel"
    temp_dir.mkdir(parents=True, exist_ok=True)

    temp_file = tempfile.NamedTemporaryFile(
        suffix=suffix, dir=temp_dir, delete=False
    )
    temp_file.close()

    return Path(temp_file.name)


def is_video_file(path: Path) -> bool:
    """Check if a path is a video file."""
    return path.suffix.lower() in VIDEO_EXTENSIONS


def is_audio_file(path: Path) -> bool:
    """Check if a path is an audio file."""
    return path.suffix.lower() in AUDIO_EXTENSIONS


def get_unique_output_path(base_path: Path) -> Path:
    """
    Get a unique output path by adding a number suffix if needed.

    Args:
        base_path: Desired output path

    Returns:
        Unique path that doesn't exist
    """
    if not base_path.exists():
        return base_path

    stem = base_path.stem
    suffix = base_path.suffix
    parent = base_path.parent

    counter = 1
    while True:
        new_path = parent / f"{stem}_{counter}{suffix}"
        if not new_path.exists():
            return new_path
        counter += 1


def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to MM:SS or HH:MM:SS.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted duration string
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def format_file_size(bytes_size: int) -> str:
    """
    Format file size in bytes to human readable format.

    Args:
        bytes_size: Size in bytes

    Returns:
        Formatted size string (e.g., "1.5 GB")
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_size < 1024:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.1f} PB"
