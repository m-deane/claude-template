"""Core modules for drone reel video processing."""

from drone_reel.core.beat_sync import BeatSync
from drone_reel.core.color_grader import ColorGrader
from drone_reel.core.duration_adjuster import DurationAdjuster, DurationConfig
from drone_reel.core.export_presets import (
    PLATFORM_PRESETS,
    ExportPreset,
    Platform,
    PlatformExporter,
)
from drone_reel.core.narrative import (
    HookGenerator,
    HookPattern,
    NarrativeArc,
    NarrativeSequencer,
)
from drone_reel.core.preview import (
    PreviewGenerator,
    ThumbnailGenerator,
    ThumbnailStyle,
)
from drone_reel.core.reframe_selector import KenBurnsConfig, ReframeSelector
from drone_reel.core.reframer import Reframer
from drone_reel.core.scene_analyzer import (
    analyze_scene_motion,
    analyze_scenes_batch,
    classify_motion_type,
    get_scene_sharpness,
)
from drone_reel.core.scene_detector import (
    EnhancedSceneInfo,
    MotionType,
    SceneDetector,
    SceneInfo,
)
from drone_reel.core.scene_filter import FilterResult, FilterThresholds, SceneFilter
from drone_reel.core.scene_sequencer import SceneSequencer
from drone_reel.core.sequence_optimizer import (
    DiversitySelector,
    MotionContinuityEngine,
)
from drone_reel.core.speed_ramper import SpeedRamper
from drone_reel.core.stabilizer import calculate_shake_score, stabilize_clip
from drone_reel.core.text_overlay import TextOverlay
from drone_reel.core.video_processor import VideoProcessor

__all__ = [
    "SceneDetector",
    "SceneInfo",
    "EnhancedSceneInfo",
    "MotionType",
    "BeatSync",
    "VideoProcessor",
    "Reframer",
    "ColorGrader",
    "stabilize_clip",
    "calculate_shake_score",
    "DiversitySelector",
    "MotionContinuityEngine",
    "analyze_scene_motion",
    "analyze_scenes_batch",
    "get_scene_sharpness",
    "classify_motion_type",
    "SceneFilter",
    "FilterThresholds",
    "FilterResult",
    "SceneSequencer",
    "DurationAdjuster",
    "DurationConfig",
    "ReframeSelector",
    "KenBurnsConfig",
    "SpeedRamper",
    "TextOverlay",
    "Platform",
    "ExportPreset",
    "PlatformExporter",
    "PLATFORM_PRESETS",
    "HookGenerator",
    "HookPattern",
    "NarrativeArc",
    "NarrativeSequencer",
    "ThumbnailGenerator",
    "ThumbnailStyle",
    "PreviewGenerator",
]
