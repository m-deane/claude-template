"""Configuration management for drone reel processing."""

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Optional

from drone_reel.core.color_grader import ColorPreset
from drone_reel.core.reframer import AspectRatio, ReframeMode
from drone_reel.core.video_processor import TransitionType


@dataclass
class Config:
    """Configuration for drone reel generation."""

    # Output settings
    output_duration: float = 45.0
    output_fps: int = 30
    output_width: int = 1080
    aspect_ratio: str = "9:16"

    # Scene detection
    scene_threshold: float = 27.0
    min_scene_length: float = 1.0
    max_scene_length: float = 8.0
    min_clip_length: float = 1.5
    max_clip_length: float = 4.0

    # Reframing
    reframe_mode: str = "smart"

    # Color grading
    color_preset: str = "drone_aerial"

    # Transitions
    transition_type: str = "crossfade"
    transition_duration: float = 0.3

    # Beat sync
    prefer_downbeats: bool = True

    # Processing
    threads: int = 4
    preset: str = "medium"  # FFmpeg encoding preset

    # Paths (optional defaults)
    default_output_dir: str = "./output"

    def get_aspect_ratio(self) -> AspectRatio:
        """Get AspectRatio enum from string."""
        ratio_map = {
            "9:16": AspectRatio.VERTICAL_9_16,
            "1:1": AspectRatio.SQUARE_1_1,
            "16:9": AspectRatio.LANDSCAPE_16_9,
            "4:5": AspectRatio.PORTRAIT_4_5,
        }
        return ratio_map.get(self.aspect_ratio, AspectRatio.VERTICAL_9_16)

    def get_reframe_mode(self) -> ReframeMode:
        """Get ReframeMode enum from string."""
        try:
            return ReframeMode(self.reframe_mode.lower())
        except ValueError:
            return ReframeMode.SMART

    def get_color_preset(self) -> ColorPreset:
        """Get ColorPreset enum from string."""
        try:
            return ColorPreset(self.color_preset.lower())
        except ValueError:
            return ColorPreset.DRONE_AERIAL

    def get_transition_type(self) -> TransitionType:
        """Get TransitionType enum from string."""
        try:
            return TransitionType(self.transition_type.lower())
        except ValueError:
            return TransitionType.CROSSFADE

    def get_output_dimensions(self) -> tuple[int, int]:
        """Calculate output dimensions from aspect ratio."""
        ratio = self.get_aspect_ratio().value
        width = self.output_width
        height = int(width * ratio[1] / ratio[0])
        return width, height


def get_config_path() -> Path:
    """Get the default configuration file path."""
    config_dir = Path.home() / ".config" / "drone_reel"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "config.json"


def load_config(config_path: Optional[Path] = None) -> Config:
    """
    Load configuration from file.

    Args:
        config_path: Path to config file (uses default if None)

    Returns:
        Config object with loaded or default values
    """
    if config_path is None:
        config_path = get_config_path()

    if not config_path.exists():
        return Config()

    try:
        with open(config_path) as f:
            data = json.load(f)
        return Config(**data)
    except (json.JSONDecodeError, TypeError):
        return Config()


def save_config(config: Config, config_path: Optional[Path] = None) -> Path:
    """
    Save configuration to file.

    Args:
        config: Config object to save
        config_path: Path to save to (uses default if None)

    Returns:
        Path where config was saved
    """
    if config_path is None:
        config_path = get_config_path()

    config_path.parent.mkdir(parents=True, exist_ok=True)

    with open(config_path, "w") as f:
        json.dump(asdict(config), f, indent=2)

    return config_path


def merge_cli_args(config: Config, **cli_args: Any) -> Config:
    """
    Merge CLI arguments into config, CLI args take precedence.

    Args:
        config: Base config object
        **cli_args: CLI arguments to merge

    Returns:
        New Config with merged values
    """
    config_dict = asdict(config)

    for key, value in cli_args.items():
        if value is not None and key in config_dict:
            config_dict[key] = value

    return Config(**config_dict)
