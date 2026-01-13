"""
Drone Reel - AI-powered CLI tool to create Instagram-style reels from drone footage.

This package provides automated video stitching with:
- Scene detection and highlight extraction
- Beat-synchronized editing
- Smooth transitions
- Auto-reframe to vertical format
- Color grading presets
"""

__version__ = "1.0.0"
__author__ = "Drone Reel CLI"

from drone_reel.core.scene_detector import SceneDetector
from drone_reel.core.beat_sync import BeatSync
from drone_reel.core.video_processor import VideoProcessor
from drone_reel.core.reframer import Reframer
from drone_reel.core.color_grader import ColorGrader

__all__ = [
    "SceneDetector",
    "BeatSync",
    "VideoProcessor",
    "Reframer",
    "ColorGrader",
]
