"""
Command-line interface for drone-reel.

Usage:
    drone-reel --input ./clips/ --music ./track.mp3 --output reel.mp4
    drone-reel --input ./clips/ --duration 30 --preset cinematic
"""

import os
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.table import Table
from rich.panel import Panel

from drone_reel import __version__
from drone_reel.core.beat_sync import BeatSync
from drone_reel.core.color_grader import ColorGrader, ColorPreset, get_preset_names
from drone_reel.core.duration_adjuster import DurationAdjuster
from drone_reel.core.reframe_selector import ReframeSelector, KenBurnsConfig
from drone_reel.core.scene_analyzer import analyze_scenes_batch
from drone_reel.core.scene_detector import SceneDetector
from drone_reel.core.scene_filter import SceneFilter, FilterThresholds
from drone_reel.core.scene_sequencer import SceneSequencer
from drone_reel.core.sequence_optimizer import DiversitySelector
from drone_reel.core.video_processor import VideoProcessor, TransitionType
from drone_reel.core.export_presets import Platform, PlatformExporter, PLATFORM_PRESETS
from drone_reel.presets.transitions import get_transitions_for_energy
from drone_reel.utils.config import Config, load_config, merge_cli_args
from drone_reel.utils.file_utils import (
    find_video_files,
    format_duration,
    get_unique_output_path,
    ensure_output_dir,
)

console = Console()


@click.group(invoke_without_command=True)
@click.option("--version", "-v", is_flag=True, help="Show version and exit")
@click.pass_context
def main(ctx, version):
    """
    Drone Reel - Create Instagram-style reels from drone footage.

    Automatically stitches video clips with beat-synced transitions,
    color grading, and vertical reframing.
    """
    if version:
        console.print(f"[bold]drone-reel[/bold] version {__version__}")
        return

    if ctx.invoked_subcommand is None:
        console.print(ctx.get_help())


@main.command()
@click.option(
    "--input", "-i",
    "input_path",
    type=click.Path(exists=True, path_type=Path),
    required=True,
    help="Input directory with video files or single video file",
)
@click.option(
    "--music", "-m",
    "music_path",
    type=click.Path(exists=True, path_type=Path),
    help="Music track for beat synchronization",
)
@click.option(
    "--output", "-o",
    "output_path",
    type=click.Path(path_type=Path),
    default="./output/reel.mp4",
    help="Output video file path",
)
@click.option(
    "--duration", "-d",
    type=click.FloatRange(0.5, 600),
    default=45.0,
    help="Target duration in seconds (0.5-600, default: 45)",
)
@click.option(
    "--color", "-c",
    type=click.Choice(get_preset_names()),
    default="drone_aerial",
    help="Color grading preset",
)
@click.option(
    "--reframe",
    type=click.Choice(["smart", "center", "pan", "thirds"]),
    default="smart",
    help="Reframing mode for vertical conversion",
)
@click.option(
    "--aspect",
    type=click.Choice(["9:16", "1:1", "4:5", "16:9"]),
    default="9:16",
    help="Output aspect ratio",
)
@click.option(
    "--platform",
    type=click.Choice([p.value for p in Platform if p != Platform.CUSTOM]),
    default=None,
    help="Export preset for specific platform (overrides aspect/resolution)",
)
@click.option(
    "--transition",
    type=click.Choice(["cut", "crossfade", "fade_black", "zoom_in"]),
    default="crossfade",
    help="Default transition type",
)
@click.option(
    "--clips",
    type=int,
    default=None,
    help="Number of clips to include (auto if not specified)",
)
@click.option(
    "--no-reframe",
    is_flag=True,
    help="Skip reframing (keep original aspect ratio)",
)
@click.option(
    "--no-color",
    is_flag=True,
    help="Skip color grading",
)
@click.option(
    "--color-intensity",
    "color_intensity",
    type=click.FloatRange(0.0, 1.0),
    default=1.0,
    help="Color grading intensity (0.0-1.0, default: 1.0). Viral reels work best at 0.4-0.7.",
)
@click.option(
    "--preview",
    is_flag=True,
    help="Preview mode - show plan without processing",
)
@click.option(
    "--quality",
    type=click.Choice(["low", "medium", "high", "ultra"]),
    default="high",
    help="Output video quality (low=5M, medium=10M, high=15M, ultra=25M bitrate)",
)
@click.option(
    "--resolution",
    type=click.Choice(["hd", "2k", "4k"]),
    default="hd",
    help="Output resolution (hd=1080p, 2k=1440p, 4k=2160p)",
)
@click.option(
    "--stabilize",
    is_flag=True,
    help="Apply adaptive video stabilization (skips stable clips)",
)
@click.option(
    "--stabilize-all",
    "stabilize_all",
    is_flag=True,
    help="Apply full stabilization to ALL clips (ignores shake scores)",
)
@click.option(
    "--stable-threshold",
    "stable_threshold",
    type=click.FloatRange(0, 100),
    default=15.0,
    help="Shake score threshold (0-100, default: 15). Lower = more clips get stabilized.",
)
@click.option(
    "--speed-ramp",
    "speed_ramp",
    is_flag=True,
    help="Enable variable speed effects (slow-mo at scenic moments, speed-up at transitions)",
)
@click.option(
    "--caption",
    type=str,
    default=None,
    help="Text caption overlay (displayed as lower-third for first 3 seconds)",
)
@click.option(
    "--beat-mode",
    "beat_mode",
    type=click.Choice(["all", "downbeat"]),
    default="all",
    help="Beat sync mode: 'all' cuts on every beat, 'downbeat' cuts only on downbeats (less frenetic)",
)
@click.option(
    "--viral",
    is_flag=True,
    help="Viral optimization preset: 15s duration, 60%% color intensity, speed ramping, Instagram Reels",
)
@click.option(
    "--ken-burns",
    "ken_burns_style",
    type=click.Choice(["off", "conservative", "moderate", "cinematic"]),
    default="off",
    help="Ken Burns effect style for panoramic shots (off=CENTER crop, conservative=subtle, moderate=medium, cinematic=full effect)",
)
@click.option(
    "--kb-zoom-end",
    "kb_zoom_end",
    type=click.FloatRange(1.0, 2.0),
    default=None,
    help="Ken Burns end zoom factor (1.0-2.0, where 1.1=10%% zoom). Overrides --ken-burns preset.",
)
@click.option(
    "--kb-pan-x",
    "kb_pan_x",
    type=click.FloatRange(0.0, 0.3),
    default=None,
    help="Ken Burns horizontal pan (0.0-0.3, where 0.1=10%% of width). Overrides --ken-burns preset.",
)
@click.option(
    "--kb-pan-y",
    "kb_pan_y",
    type=click.FloatRange(0.0, 0.2),
    default=None,
    help="Ken Burns vertical pan (0.0-0.2, where 0.05=5%% of height). Overrides --ken-burns preset.",
)
def create(
    input_path: Path,
    music_path: Optional[Path],
    output_path: Path,
    duration: float,
    color: str,
    reframe: str,
    aspect: str,
    platform: Optional[str],
    transition: str,
    clips: Optional[int],
    no_reframe: bool,
    no_color: bool,
    color_intensity: float,
    preview: bool,
    quality: str,
    resolution: str,
    stabilize: bool,
    stabilize_all: bool,
    stable_threshold: float,
    speed_ramp: bool,
    caption: Optional[str],
    beat_mode: str,
    viral: bool,
    ken_burns_style: str,
    kb_zoom_end: Optional[float],
    kb_pan_x: Optional[float],
    kb_pan_y: Optional[float],
):
    """Create a reel from drone footage."""
    # Validate conflicting options
    if no_reframe and reframe != "smart":
        console.print("[red]Error:[/red] Cannot use --reframe with --no-reframe")
        raise SystemExit(1)

    # --stabilize-all implies --stabilize
    if stabilize_all:
        stabilize = True

    # --viral preset applies optimized defaults
    if viral:
        # Use Click's get_parameter_source to detect user-explicit values
        ctx = click.get_current_context()
        if ctx.get_parameter_source("duration") != click.core.ParameterSource.COMMANDLINE:
            duration = 15.0
        if ctx.get_parameter_source("platform") != click.core.ParameterSource.COMMANDLINE:
            platform = "instagram_reels"
        if ctx.get_parameter_source("color_intensity") != click.core.ParameterSource.COMMANDLINE:
            color_intensity = 0.6
        speed_ramp = True
        viral_parts = []
        viral_parts.append(f"{duration:.0f}s duration")
        viral_parts.append(f"{int(color_intensity * 100)}% color intensity")
        viral_parts.append("speed ramping")
        if platform:
            viral_parts.append(platform.replace("_", " "))
        console.print(f"[cyan]Viral mode:[/cyan] {', '.join(viral_parts)}")

    # Ken Burns preset definitions
    KB_PRESETS = {
        "off": None,  # Use CENTER mode instead
        "conservative": {"zoom_end": 1.03, "pan_x": 0.02, "pan_y": 0.01},
        "moderate": {"zoom_end": 1.05, "pan_x": 0.05, "pan_y": 0.02},
        "cinematic": {"zoom_end": 1.10, "pan_x": 0.10, "pan_y": 0.05},
    }

    # Resolve Ken Burns settings (CLI overrides take precedence over presets)
    kb_settings = None
    if ken_burns_style != "off":
        kb_settings = KB_PRESETS[ken_burns_style].copy()
        # Apply individual CLI overrides
        if kb_zoom_end is not None:
            kb_settings["zoom_end"] = kb_zoom_end
        if kb_pan_x is not None:
            kb_settings["pan_x"] = kb_pan_x
        if kb_pan_y is not None:
            kb_settings["pan_y"] = kb_pan_y
    elif kb_zoom_end is not None or kb_pan_x is not None or kb_pan_y is not None:
        # Individual params specified without preset - use conservative as base
        kb_settings = KB_PRESETS["conservative"].copy()
        if kb_zoom_end is not None:
            kb_settings["zoom_end"] = kb_zoom_end
        if kb_pan_x is not None:
            kb_settings["pan_x"] = kb_pan_x
        if kb_pan_y is not None:
            kb_settings["pan_y"] = kb_pan_y

    config = load_config()

    exporter = None
    preset = None

    if platform:
        exporter = PlatformExporter()
        try:
            platform_enum = Platform(platform)
            preset = exporter.get_preset(platform_enum)

            validation = exporter.validate_for_platform(duration, platform_enum)
            if validation["errors"]:
                console.print(f"[red]Platform validation errors:[/red]")
                for error in validation["errors"]:
                    console.print(f"  - {error}")
                raise SystemExit(1)

            if validation["warnings"]:
                console.print(f"[yellow]Platform warnings:[/yellow]")
                for warning in validation["warnings"]:
                    console.print(f"  - {warning}")
                console.print()

            platform_aspect = f"{preset.aspect_ratio[0]}:{preset.aspect_ratio[1]}"
            if aspect != "9:16" and aspect != platform_aspect:
                console.print(
                    f"[yellow]Note:[/yellow] --platform {platform} overrides "
                    f"--aspect {aspect} with {platform_aspect}"
                )
            aspect = platform_aspect
        except ValueError as e:
            console.print(f"[red]Error:[/red] {e}")
            raise SystemExit(1)

    config = merge_cli_args(
        config,
        output_duration=duration,
        color_preset=color,
        reframe_mode=reframe,
        aspect_ratio=aspect,
        transition_type=transition,
    )

    # Quality presets (video bitrate, audio bitrate)
    quality_presets = {
        "low": ("5M", "128k"),
        "medium": ("10M", "192k"),
        "high": ("15M", "192k"),
        "ultra": ("25M", "320k"),
    }
    video_bitrate, audio_bitrate = quality_presets.get(quality, ("15M", "192k"))

    # Resolution presets (width in pixels)
    resolution_presets = {
        "hd": 1080,   # 1080x1920 vertical, 1920x1080 landscape
        "2k": 1440,   # 1440x2560 vertical, 2560x1440 landscape
        "4k": 2160,   # 2160x3840 vertical, 3840x2160 landscape
    }
    output_width = resolution_presets.get(resolution, 1080)
    config.output_width = output_width

    # Scale bitrate for higher resolutions (4K needs ~4x bitrate of 1080p)
    if resolution == "4k":
        bitrate_multipliers = {"low": "15M", "medium": "25M", "high": "40M", "ultra": "80M"}
        video_bitrate = bitrate_multipliers.get(quality, "40M")
    elif resolution == "2k":
        bitrate_multipliers = {"low": "8M", "medium": "15M", "high": "25M", "ultra": "45M"}
        video_bitrate = bitrate_multipliers.get(quality, "25M")

    platform_info = f" for {preset.name}" if preset else ""
    resolution_label = {"hd": "1080p", "2k": "1440p", "4k": "2160p"}.get(resolution, "1080p")
    quality_info = f" ({resolution_label} {quality}, {video_bitrate} bitrate)"
    console.print(Panel.fit(
        "[bold blue]Drone Reel Creator[/bold blue]\n"
        f"Creating {duration}s reel{platform_info} with {color} color grade{quality_info}",
        border_style="blue",
    ))

    # Find video files
    if input_path.is_file():
        video_files = [input_path]
    else:
        video_files = find_video_files(input_path)

    if not video_files:
        from drone_reel.utils.file_utils import VIDEO_EXTENSIONS
        formats = ", ".join(sorted(VIDEO_EXTENSIONS))
        console.print(f"[red]Error:[/red] No video files found in input path")
        console.print(f"[dim]Supported formats: {formats}[/dim]")
        raise SystemExit(1)

    console.print(f"\n[green]Found {len(video_files)} video file(s)[/green]")

    # Verify output path is writable before expensive processing
    output_dir = output_path.parent
    if not output_dir.exists():
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            console.print(f"[red]Error:[/red] Cannot create output directory: {e}")
            raise SystemExit(1)
    elif not os.access(output_dir, os.W_OK):
        console.print(f"[red]Error:[/red] Output directory is not writable: {output_dir}")
        raise SystemExit(1)

    # Resource preflight check
    from drone_reel.utils.resource_guard import preflight_check
    preflight_results = preflight_check(
        output_path=output_path,
        resolution_height=output_width,  # output_width is the larger dimension (height in vertical)
        fps=config.output_fps,
        clip_count=max(1, int(duration / 2.5)),  # Conservative estimate
        stabilize=stabilize,
        video_bitrate=video_bitrate,
        duration=duration,
    )
    for result in preflight_results:
        if result["level"] == "error":
            console.print(f"[red]Error:[/red] {result['message']}")
        else:
            console.print(f"[yellow]Warning:[/yellow] {result['message']}")
    if any(r["level"] == "error" for r in preflight_results):
        raise SystemExit(1)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:

        # Step 1: Analyze scenes (fast detection, motion energy calculated later)
        task = progress.add_task("[cyan]Analyzing scenes...", total=len(video_files))

        scene_detector = SceneDetector(
            threshold=config.scene_threshold,
            min_scene_length=config.min_scene_length,
            max_scene_length=config.max_scene_length,
        )

        all_scenes = []
        for video_file in video_files:
            try:
                scenes = scene_detector.detect_scenes(video_file)
                all_scenes.extend(scenes)
            except Exception as e:
                console.print(f"[yellow]Warning:[/yellow] Skipping {video_file.name}: {e}")
            progress.advance(task)

        if not all_scenes:
            console.print("[red]Error:[/red] No valid scenes detected from any video file")
            console.print("[dim]Tip: Check that video files are not corrupted and are at least 1 second long.[/dim]")
            raise SystemExit(1)

        console.print(f"[green]Detected {len(all_scenes)} scenes[/green]")

        # Step 2: Analyze music (if provided)
        beat_info = None
        cut_points = None
        clip_durations = None

        if music_path:
            progress.add_task("[cyan]Analyzing music...", total=None)

            beat_sync = BeatSync()
            beat_info = beat_sync.analyze(music_path)

            console.print(f"[green]Detected tempo: {beat_info.tempo:.1f} BPM[/green]")

            cut_points = beat_sync.get_cut_points(
                beat_info,
                target_duration=duration,
                min_clip_length=config.min_clip_length,
                max_clip_length=config.max_clip_length,
                prefer_downbeats=config.prefer_downbeats,
                downbeat_only=(beat_mode == "downbeat"),
            )

            clip_durations = beat_sync.calculate_clip_durations(cut_points, duration)
        else:
            # Generate evenly spaced cuts without music (will be refined by adaptive durations later)
            num_clips = clips or max(1, int(duration / 3))
            clip_durations = [duration / num_clips] * num_clips

        # Step 3: Select best scenes with diversity optimization and motion filtering
        num_clips_needed = len(clip_durations)

        # Dynamic max_per_source based on duration - longer reels need more clips per source
        # Short reels (≤15s): 3 clips/source, Medium (≤30s): 4, Long (≤60s): 5, Very long: 6
        if duration <= 15:
            max_clips_per_source = 3
        elif duration <= 30:
            max_clips_per_source = 4
        elif duration <= 60:
            max_clips_per_source = 5
        else:
            max_clips_per_source = 6

        # Use DiversitySelector for better scene variety
        diversity_selector = DiversitySelector(
            diversity_weight=0.3,  # 30% diversity, 70% quality score
            max_per_source=max_clips_per_source,
            min_temporal_gap=4.0,  # Reduced from 5.0 to allow more clips from same source
        )

        # Get initial candidate scenes - more than needed so we can filter
        all_detected_scenes = all_scenes
        candidate_count = min(len(all_detected_scenes), num_clips_needed * 3)  # 3x candidates

        # Sort by score and get top candidates
        sorted_candidates = sorted(all_detected_scenes, key=lambda s: s.score, reverse=True)[:candidate_count]

        from drone_reel.core.scene_detector import EnhancedSceneInfo, MotionType

        # Analyze motion energy, brightness, shake, motion type, and sharpness in single pass
        progress.add_task("[cyan]Analyzing motion energy...", total=len(sorted_candidates))

        analysis_results = analyze_scenes_batch(sorted_candidates, include_sharpness=True)

        scene_motion_map = {sid: r["motion_energy"] for sid, r in analysis_results.items()}
        scene_brightness_map = {sid: r["brightness"] for sid, r in analysis_results.items()}
        scene_shake_map = {sid: r["shake_score"] for sid, r in analysis_results.items()}

        # Update EnhancedSceneInfo with computed motion types (fixes P0 issue #3)
        for scene in sorted_candidates:
            r = analysis_results.get(id(scene))
            if r and isinstance(scene, EnhancedSceneInfo):
                scene.motion_type = r["motion_type"]
                scene.motion_direction = r["motion_direction"]
                scene.motion_energy = r["motion_energy"]

        # Filter scenes using SceneFilter
        scene_filter = SceneFilter()
        filter_result = scene_filter.filter_scenes(
            sorted_candidates, scene_motion_map, scene_brightness_map, scene_shake_map,
        )

        # Report subject scenes found
        if filter_result.high_subject_scenes:
            console.print(f"[cyan]Subject detection:[/cyan] {len(filter_result.high_subject_scenes)} scenes with interesting subjects preserved")

        # Get prioritized scenes, adding low-motion if needed
        prioritized_scenes = filter_result.with_low_motion_if_needed(num_clips_needed)

        if len(filter_result.prioritized) >= num_clips_needed:
            filter_msg = (
                f"[green]Motion filtering:[/green] {len(filter_result.high_motion_scenes)} high, "
                f"{len(filter_result.medium_motion_scenes)} medium, "
                f"{len(filter_result.low_motion_scenes)} filtered out"
            )
            if filter_result.dark_scenes_filtered > 0:
                filter_msg += f", [yellow]{filter_result.dark_scenes_filtered} dark/bright[/yellow]"
            if filter_result.shaky_scenes_filtered > 0:
                filter_msg += f", [red]{filter_result.shaky_scenes_filtered} shaky[/red]"
            console.print(filter_msg)
        elif filter_result.low_motion_scenes:
            console.print(f"[yellow]Warning:[/yellow] Including {len(filter_result.low_motion_scenes)} low-motion scenes to meet clip count")

        # Use diversity-aware selection on prioritized scenes, enforcing minimum scene count
        selected_scenes = diversity_selector.select_with_minimum(
            prioritized_scenes, count=num_clips_needed, target_duration=duration
        )

        # Progressive filter relaxation: if too few scenes, relax filters and retry
        if len(selected_scenes) == 0 and len(sorted_candidates) > 0:
            console.print("[yellow]Warning:[/yellow] All scenes filtered out. Relaxing filters...")
            selected_scenes = diversity_selector.select_with_minimum(
                sorted_candidates, count=num_clips_needed, target_duration=duration
            )
            if selected_scenes:
                console.print(f"[green]Recovered {len(selected_scenes)} scenes after relaxing filters[/green]")

        if not selected_scenes:
            console.print("[red]Error:[/red] No usable scenes found in video files")
            console.print("[dim]Tip: Videos must be at least 1 second long.[/dim]")
            console.print("[dim]Tip: Try using --clips to specify number of clips[/dim]")
            raise SystemExit(1)

        if len(selected_scenes) < num_clips_needed:
            console.print(
                f"[yellow]Warning:[/yellow] Only {len(selected_scenes)} scenes available, "
                f"requested {num_clips_needed}"
            )
            # Scale up clip durations to fill target duration with fewer clips
            original_total = sum(clip_durations)
            clip_durations = clip_durations[:len(selected_scenes)]
            current_total = sum(clip_durations)
            if current_total > 0 and original_total > current_total:
                scale_factor = min(original_total / current_total, 2.5)  # Allow up to 2.5x to avoid short reels
                clip_durations = [d * scale_factor for d in clip_durations]
                achieved = sum(clip_durations)
                shortfall = (1 - achieved / duration) * 100
                msg = f"[cyan]Duration scaling:[/cyan] Extended clips by {scale_factor:.1f}x"
                if shortfall > 10:
                    msg += f" [yellow](still {shortfall:.0f}% short of {duration:.0f}s target)[/yellow]"
                console.print(msg)

        # Reorder scenes for optimal pacing using SceneSequencer
        sequencer = SceneSequencer()
        selected_scenes = sequencer.sequence(selected_scenes, motion_map=scene_motion_map)

        # Use sharpness already computed in the batch analysis pass (no extra file I/O)
        scene_sharpness_map = {
            id(scene): analysis_results.get(id(scene), {}).get("sharpness", 0.0)
            for scene in selected_scenes
        }

        # Adjust clip durations using DurationAdjuster
        duration_adjuster = DurationAdjuster()

        # Use adaptive durations when scenes have hook_tier information (EnhancedSceneInfo)
        if all(isinstance(s, EnhancedSceneInfo) for s in selected_scenes):
            clip_durations = duration_adjuster.compute_adaptive_durations(
                selected_scenes, target_duration=duration
            )
            auto_scale = None
        else:
            clip_durations, auto_scale = duration_adjuster.adjust_durations(
                selected_scenes, clip_durations, scene_sharpness_map, duration,
            )

        actual_duration = sum(clip_durations)
        if auto_scale:
            console.print(f"[cyan]Duration adjustment:[/cyan] Scaled clips by {auto_scale:.2f}x → {actual_duration:.0f}s")

        # Preview mode - show plan and exit
        if preview:
            _show_preview(selected_scenes, clip_durations, config, beat_info)
            return

        # Step 4: Generate transitions
        # Map CLI transition choice to TransitionType
        import random
        transition_map = {
            "cut": TransitionType.CUT,
            "crossfade": TransitionType.CROSSFADE,
            "fade_black": TransitionType.FADE_BLACK,
            "zoom_in": TransitionType.ZOOM_IN,
        }
        user_transition = transition_map.get(transition, TransitionType.CROSSFADE)

        if beat_info and cut_points:
            energy_levels = [
                beat_sync.get_energy_at_time(beat_info, cp.time)
                for cp in cut_points[:-1]
            ]
            avg_energy = sum(energy_levels) / len(energy_levels) if energy_levels else 0.5
            transitions = get_transitions_for_energy(
                avg_energy,
                len(selected_scenes),
                style="cinematic",  # Use cinematic style for drone footage
            )
            # Override with user's choice if they explicitly set --transition to something other than default
            if transition != "crossfade":
                transitions = [user_transition] * len(selected_scenes)
        else:
            if transition != "crossfade":
                # User explicitly chose a transition type - use it consistently
                transitions = [user_transition] * len(selected_scenes)
            else:
                # Generate varied dynamic transitions without music
                transitions = []
                for i in range(len(selected_scenes)):
                    if i == 0:
                        transitions.append(TransitionType.FADE_BLACK)  # Start with fade in
                    elif i == len(selected_scenes) - 1:
                        transitions.append(TransitionType.FADE_BLACK)  # End with fade out
                    else:
                        transitions.append(random.choice([
                            TransitionType.CROSSFADE,
                            TransitionType.CROSSFADE,
                            TransitionType.ZOOM_IN,
                            TransitionType.ZOOM_OUT,
                        ]))

        # Step 5: Create clip segments with motion-matched transitions
        processor_kwargs = {
            "output_fps": config.output_fps,
            "threads": config.threads,
            "preset": config.preset,
            "video_bitrate": video_bitrate,
            "audio_bitrate": audio_bitrate,
            "stabilize": stabilize,
        }

        if stabilize:
            if stabilize_all:
                console.print("[cyan]Stabilization:[/cyan] Full mode - stabilizing ALL clips")
            else:
                console.print(f"[cyan]Stabilization:[/cyan] Adaptive mode (stable threshold: {stable_threshold:.0f})")

        # Display Ken Burns settings
        if kb_settings:
            kb_info = f"zoom={kb_settings['zoom_end']:.2f}x, pan=({kb_settings['pan_x']:.2f}, {kb_settings['pan_y']:.2f})"
            console.print(f"[cyan]Ken Burns:[/cyan] {ken_burns_style} ({kb_info})")
        else:
            console.print("[cyan]Ken Burns:[/cyan] off (using CENTER mode for panoramas)")

        if preset:
            processor_kwargs["output_fps"] = preset.fps
            processor_kwargs["output_audio_codec"] = preset.audio_codec
            # Use platform-specific bitrate if specified
            processor_kwargs["video_bitrate"] = preset.video_bitrate
            processor_kwargs["audio_bitrate"] = preset.audio_bitrate

        video_processor = VideoProcessor(**processor_kwargs)

        # Use motion-matched transitions for smoother, more professional cuts
        segments = video_processor.create_motion_matched_segments(
            selected_scenes,
            clip_durations,
            config.transition_duration,
        )

        # Step 6: Determine output dimensions and create per-clip reframers
        output_w, output_h = config.get_output_dimensions()

        # Create intelligent per-clip reframers based on scene content
        clip_reframers = []
        clip_reframe_modes = []
        if not no_reframe:
            kb_cfg = None
            if kb_settings:
                kb_cfg = KenBurnsConfig(
                    zoom_end=kb_settings["zoom_end"],
                    pan_x=kb_settings["pan_x"],
                    pan_y=kb_settings["pan_y"],
                )
            reframe_selector = ReframeSelector(
                output_width=output_w,
                kb_config=kb_cfg,
            )
            clip_reframers, clip_reframe_modes = reframe_selector.select_reframers(
                selected_scenes, clip_durations,
            )

        # Step 7: Stitch video
        task = progress.add_task("[cyan]Stitching video...", total=100)

        def update_progress(p):
            progress.update(task, completed=int(p * 100))

        ensure_output_dir(output_path)
        output_path = get_unique_output_path(output_path)

        # Extract shake scores for selected scenes (for adaptive stabilization)
        selected_shake_scores = [
            scene_shake_map.get(id(scene), 50.0) for scene in selected_scenes
        ]

        # OPTION A FIX: Force FULL stabilization for non-CENTER reframe modes
        # Reframing with KEN_BURNS or SMART can introduce micro-jitter even on stable footage
        # Boost shake scores for ALL these clips to ensure FULL stabilization is applied
        REFRAME_JITTER_BOOST = 35.0  # Boost score to ensure FULL stabilization (>= 30)
        reframe_boosted_clips = 0
        if stabilize and clip_reframe_modes and not stabilize_all:
            for i, mode in enumerate(clip_reframe_modes):
                if i < len(selected_shake_scores) and mode in ("SMART", "KEN_BURNS"):
                    original_score = selected_shake_scores[i]
                    if original_score < REFRAME_JITTER_BOOST:
                        # Boost ALL Ken Burns/SMART clips to FULL stabilization
                        selected_shake_scores[i] = REFRAME_JITTER_BOOST
                        reframe_boosted_clips += 1

        # Display shake scores when stabilization is enabled (Feature C)
        if stabilize:
            console.print("\n[bold]Clip Shake Analysis:[/bold]")
            clips_to_stabilize = 0
            clips_to_skip = 0
            for i, (scene, shake_score) in enumerate(zip(selected_scenes, selected_shake_scores), 1):
                source_name = scene.source_file.name[:25]
                # Check if this clip was boosted due to reframe mode
                reframe_mode = clip_reframe_modes[i-1] if clip_reframe_modes and i-1 < len(clip_reframe_modes) else "CENTER"
                original_score = scene_shake_map.get(id(scene), 50.0)
                was_boosted = (reframe_mode in ("SMART", "KEN_BURNS") and
                              original_score < stable_threshold and
                              shake_score >= REFRAME_JITTER_BOOST)

                if stabilize_all:
                    status = "[yellow]FULL[/yellow]"
                    clips_to_stabilize += 1
                elif shake_score < stable_threshold:
                    status = "[green]SKIP[/green]"
                    clips_to_skip += 1
                elif shake_score < 30:
                    status = "[cyan]LIGHT[/cyan]"
                    clips_to_stabilize += 1
                else:
                    status = "[yellow]FULL[/yellow]"
                    if was_boosted:
                        status += f" [dim](+{reframe_mode})[/dim]"
                    clips_to_stabilize += 1
                console.print(f"  {i:2d}. {source_name:<25} shake: {shake_score:5.1f} → {status}")

            if stabilize_all:
                console.print(f"\n[cyan]Summary:[/cyan] Stabilizing all {len(selected_scenes)} clips (--stabilize-all)")
            else:
                summary = f"[cyan]Summary:[/cyan] {clips_to_stabilize} to stabilize, {clips_to_skip} stable (threshold: {stable_threshold:.0f})"
                if reframe_boosted_clips > 0:
                    summary += f" [dim]({reframe_boosted_clips} boosted for reframe jitter)[/dim]"
                console.print(summary)
            console.print()

        # Handle --stabilize-all: force full stabilization on all clips
        if stabilize_all:
            selected_shake_scores = [100.0] * len(selected_scenes)  # Force full stabilization

        # Pass stable_threshold to video processor via shake_scores adjustment
        # The stabilizer uses shake_score to decide: <15 skip, 15-30 light, >30 full
        # If user sets different threshold, we adjust scores accordingly
        if stabilize and not stabilize_all and stable_threshold != 15.0:
            # Remap scores so clips below stable_threshold appear as "stable" to stabilizer
            # stabilizer skips if shake_score < 15, so we scale scores:
            # - Clips with original score < stable_threshold → score < 15 (skip)
            # - Clips with original score >= stable_threshold → keep proportional
            adjusted_shake_scores = []
            for score in selected_shake_scores:
                if score < stable_threshold:
                    # Map to below 15 (stabilizer's skip threshold)
                    adjusted_shake_scores.append(score * (14.9 / stable_threshold) if stable_threshold > 0 else 0)
                else:
                    # Keep original score
                    adjusted_shake_scores.append(score)
            selected_shake_scores = adjusted_shake_scores

        # Step 7b: Generate speed ramps if enabled
        clip_speed_ramps = None
        if speed_ramp:
            from drone_reel.core.speed_ramper import SpeedRamper
            speed_ramper = SpeedRamper()
            clip_speed_ramps = []
            ramped_count = 0
            for scene in selected_scenes:
                ramps = speed_ramper.auto_detect_ramp_points(
                    scene, beat_info=beat_info
                )
                clip_speed_ramps.append(ramps)
                if ramps:
                    ramped_count += 1
            # Hook enhancement: add slow-mo opener to first clip for dramatic hook
            if clip_speed_ramps and selected_scenes:
                from drone_reel.core.speed_ramper import SpeedRamp
                first_scene = selected_scenes[0]
                opener_duration = min(1.0, first_scene.duration * 0.3)
                if opener_duration > 0.2:
                    opener_ramp = SpeedRamp(
                        start_time=0.0,
                        end_time=opener_duration,
                        start_speed=0.7,
                        end_speed=1.0,
                        easing="ease_out",
                    )
                    # Prepend to first clip's ramps (avoid overlap with auto-detected)
                    existing = clip_speed_ramps[0]
                    if not existing or existing[0].start_time >= opener_duration:
                        clip_speed_ramps[0] = [opener_ramp] + existing
                        if not existing:
                            ramped_count += 1
            console.print(f"[cyan]Speed ramping:[/cyan] {ramped_count} of {len(selected_scenes)} clips ramped")

        # Determine if post-processing is needed (caption, color grading, or silent audio injection)
        # Also force return_clip path when no music so we can inject a silent audio stream
        # (platforms require an audio track for compatibility)
        needs_post_processing = caption or (not no_color and color != "none") or not music_path

        if needs_post_processing:
            # Single-pipeline mode: get clip object, apply transforms, write once
            final_clip = video_processor.stitch_clips(
                segments,
                output_path,
                audio_path=music_path,
                target_size=None,  # Let reframers handle sizing
                progress_callback=update_progress,
                reframers=clip_reframers if clip_reframers else None,
                shake_scores=selected_shake_scores if stabilize else None,
                speed_ramps=clip_speed_ramps,
                return_clip=True,
            )

            try:
                # CF-1: Inject near-silent stereo audio when no music provided for platform compatibility
                # The make_frame must handle vectorized t (numpy array of time points).
                # Uses inaudible low-amplitude signal so AAC doesn't optimize to zero length.
                if not music_path:
                    import numpy as np
                    from moviepy.audio.AudioClip import AudioClip

                    def _silent_frame(t):
                        if isinstance(t, np.ndarray):
                            return np.full((len(t), 2), 1e-6)
                        return np.array([1e-6, 1e-6])

                    silent = AudioClip(
                        _silent_frame,
                        duration=final_clip.duration,
                        fps=44100,
                    )
                    final_clip = final_clip.with_audio(silent)

                # Apply text caption overlay as in-memory transform
                if caption:
                    from drone_reel.core.text_overlay import TextOverlay as TextOverlayConfig, TextRenderer, TextAnimation
                    console.print(f"[cyan]Caption:[/cyan] \"{caption}\"")

                    renderer = TextRenderer()
                    overlay_config = TextOverlayConfig(
                        text=caption,
                        position=(0.5, 0.88),
                        font_size=42,
                        duration=3.0,
                        animation_in=TextAnimation.FADE_IN,
                        animation_out=TextAnimation.FADE_OUT,
                    )
                    final_clip = renderer.apply_overlay_to_clip(final_clip, overlay_config)

                # Apply color grading as in-memory transform
                if not no_color and color != "none":
                    import cv2
                    console.print(f"[cyan]Color grade:[/cyan] {color} @ {color_intensity:.0%} intensity")
                    color_grader = ColorGrader(preset=ColorPreset(color), intensity=color_intensity)

                    def grade_transform(get_frame, t):
                        frame = get_frame(t)
                        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                        graded_bgr = color_grader.grade_frame(frame_bgr)
                        return cv2.cvtColor(graded_bgr, cv2.COLOR_BGR2RGB)

                    final_clip = final_clip.transform(grade_transform)

                # Write once to disk with identical encoding params to video_processor path
                output_path.parent.mkdir(parents=True, exist_ok=True)

                # Build ffmpeg_params matching video_processor.py: BT.709 + faststart + VBV caps
                manual_ffmpeg_params = [
                    "-pix_fmt", "yuv420p",
                    "-colorspace", "bt709",
                    "-color_primaries", "bt709",
                    "-color_trc", "bt709",
                    "-movflags", "+faststart",
                ]
                _bitrate_for_caps = video_bitrate or video_processor.video_bitrate
                if _bitrate_for_caps:
                    _numeric_str = _bitrate_for_caps.rstrip("MmKk")
                    try:
                        _numeric_val = float(_numeric_str)
                        _unit = _bitrate_for_caps[len(_numeric_str):].upper()
                        manual_ffmpeg_params += [
                            "-maxrate", f"{_numeric_val * 1.5:.0f}{_unit}",
                            "-bufsize", f"{_numeric_val * 2:.0f}{_unit}",
                        ]
                    except (ValueError, IndexError):
                        pass

                final_clip.write_videofile(
                    str(output_path),
                    fps=video_processor.output_fps,
                    codec=video_processor.output_codec,
                    audio_codec="aac",
                    preset=video_processor.preset,
                    threads=video_processor.threads,
                    bitrate=video_bitrate or video_processor.video_bitrate,
                    audio_bitrate=audio_bitrate or video_processor.audio_bitrate,
                    ffmpeg_params=manual_ffmpeg_params,
                    logger=None,
                )
            finally:
                # Clean up all clip resources
                if hasattr(final_clip, '_stitch_source_clips'):
                    for clip in final_clip._stitch_source_clips:
                        try:
                            if hasattr(clip, '_source_clip_ref') and clip._source_clip_ref:
                                clip._source_clip_ref.close()
                            clip.close()
                        except Exception:
                            pass
                if hasattr(final_clip, '_stitch_audio') and final_clip._stitch_audio:
                    try:
                        final_clip._stitch_audio.close()
                    except Exception:
                        pass
                try:
                    final_clip.close()
                except Exception:
                    pass
        else:
            # No post-processing: write directly to disk (original path)
            video_processor.stitch_clips(
                segments,
                output_path,
                audio_path=music_path,
                target_size=None,  # Let reframers handle sizing
                progress_callback=update_progress,
                reframers=clip_reframers if clip_reframers else None,
                shake_scores=selected_shake_scores if stabilize else None,
                speed_ramps=clip_speed_ramps,
            )

    # Done!
    duration_info = format_duration(actual_duration)
    if actual_duration < duration * 0.95:  # More than 5% shorter than requested
        duration_info += f" [dim](requested {format_duration(duration)})[/dim]"

    # Get actual output dimensions
    if no_reframe:
        from moviepy import VideoFileClip
        with VideoFileClip(str(output_path)) as final_clip:
            output_w, output_h = final_clip.w, final_clip.h

    success_message = f"[bold green]Reel created successfully![/bold green]\n\n"
    success_message += f"Output: [cyan]{output_path}[/cyan]\n"
    success_message += f"Duration: {duration_info}\n"
    success_message += f"Resolution: {output_w}x{output_h}\n"
    success_message += f"Clips: {len(selected_scenes)}"

    if preset:
        success_message += f"\nPlatform: {preset.name}"
        if exporter:
            validation = exporter.validate_for_platform(actual_duration, platform_enum)
            if not validation["errors"] and not validation["warnings"]:
                success_message += " [green]✓[/green]"

    console.print(Panel.fit(success_message, border_style="green"))


@main.command()
@click.option(
    "--input", "-i",
    "input_path",
    type=click.Path(exists=True, path_type=Path),
    required=True,
    help="Video file to analyze",
)
def analyze(input_path: Path):
    """Analyze a video file and show scene information."""
    console.print(f"\n[bold]Analyzing:[/bold] {input_path.name}\n")

    scene_detector = SceneDetector()
    scenes = scene_detector.detect_scenes(input_path)

    table = Table(title="Detected Scenes")
    table.add_column("Scene", style="cyan")
    table.add_column("Start", style="green")
    table.add_column("End", style="green")
    table.add_column("Duration", style="yellow")
    table.add_column("Score", style="magenta")

    for i, scene in enumerate(scenes, 1):
        table.add_row(
            str(i),
            format_duration(scene.start_time),
            format_duration(scene.end_time),
            f"{scene.duration:.1f}s",
            f"{scene.score:.1f}",
        )

    console.print(table)
    console.print(f"\n[bold]Total scenes:[/bold] {len(scenes)}")


@main.command()
@click.option(
    "--input", "-i",
    "input_path",
    type=click.Path(exists=True, path_type=Path),
    required=True,
    help="Audio file to analyze",
)
def beats(input_path: Path):
    """Analyze a music track and show beat information."""
    console.print(f"\n[bold]Analyzing:[/bold] {input_path.name}\n")

    beat_sync = BeatSync()
    beat_info = beat_sync.analyze(input_path)

    console.print(f"[bold]Tempo:[/bold] {beat_info.tempo:.1f} BPM")
    console.print(f"[bold]Duration:[/bold] {format_duration(beat_info.duration)}")
    console.print(f"[bold]Total beats:[/bold] {beat_info.beat_count}")
    console.print(f"[bold]Downbeats:[/bold] {len(beat_info.downbeat_times)}")
    console.print(f"[bold]Beat interval:[/bold] {beat_info.beat_interval:.3f}s")

    # Show first 10 beats
    console.print("\n[bold]First 10 beat times:[/bold]")
    for i, beat_time in enumerate(beat_info.beat_times[:10], 1):
        is_downbeat = beat_time in beat_info.downbeat_times
        marker = " [bold magenta]*[/bold magenta]" if is_downbeat else ""
        console.print(f"  {i}. {format_duration(beat_time)}{marker}")


@main.command()
def presets():
    """List available color grading presets."""
    console.print("\n[bold]Available Color Presets:[/bold]\n")

    table = Table()
    table.add_column("Preset", style="cyan")
    table.add_column("Description", style="white")

    descriptions = {
        "none": "No color grading",
        "cinematic": "Film-like with lifted blacks and reduced saturation",
        "warm_sunset": "Warm golden tones, great for sunset footage",
        "cool_blue": "Cool blue tones, good for ocean/sky footage",
        "vintage": "Faded retro look with grain",
        "high_contrast": "Punchy contrast for dramatic footage",
        "muted": "Desaturated, understated look",
        "vibrant": "Enhanced colors and saturation",
        "teal_orange": "Popular cinematic color grade",
        "black_white": "Classic black and white",
        "drone_aerial": "Optimized for aerial drone footage",
    }

    for preset in get_preset_names():
        table.add_row(preset, descriptions.get(preset, ""))

    console.print(table)


@main.command()
def platforms():
    """List available export platforms and their specifications."""
    console.print("\n[bold]Available Export Platforms:[/bold]\n")

    exporter = PlatformExporter()

    table = Table(title="Platform Export Presets")
    table.add_column("Platform", style="cyan")
    table.add_column("Aspect Ratio", style="green")
    table.add_column("Resolution", style="yellow")
    table.add_column("Max Duration", style="magenta")
    table.add_column("Optimal Range", style="blue")

    for platform in exporter.get_all_platforms():
        preset = exporter.get_preset(platform)

        aspect_str = exporter.get_aspect_ratio_string(preset.aspect_ratio)
        resolution_str = f"{preset.resolution[0]}x{preset.resolution[1]}"

        max_dur_str = f"{preset.max_duration:.0f}s" if preset.max_duration else "Unlimited"

        min_opt, max_opt = preset.optimal_duration
        optimal_str = f"{min_opt:.0f}s - {max_opt:.0f}s"

        table.add_row(
            preset.name,
            aspect_str,
            resolution_str,
            max_dur_str,
            optimal_str,
        )

    console.print(table)

    console.print("\n[dim]Use --platform flag with 'create' command to export for specific platform[/dim]")
    console.print("[dim]Example: drone-reel create --input ./clips --platform instagram_reels[/dim]")


def _show_preview(scenes, durations, config, beat_info):
    """Show preview of the planned reel."""
    console.print("\n[bold]Preview Mode - Planned Reel:[/bold]\n")

    table = Table(title="Clip Selection")
    table.add_column("#", style="cyan")
    table.add_column("Source", style="white")
    table.add_column("Start", style="green")
    table.add_column("Duration", style="yellow")
    table.add_column("Score", style="magenta")

    total_duration = 0
    for i, (scene, dur) in enumerate(zip(scenes, durations), 1):
        table.add_row(
            str(i),
            scene.source_file.name[:30],
            format_duration(scene.start_time),
            f"{dur:.1f}s",
            f"{scene.score:.1f}",
        )
        total_duration += dur

    console.print(table)

    console.print(f"\n[bold]Total clips:[/bold] {len(scenes)}")
    console.print(f"[bold]Total duration:[/bold] {format_duration(total_duration)}")
    console.print(f"[bold]Color preset:[/bold] {config.color_preset}")
    console.print(f"[bold]Aspect ratio:[/bold] {config.aspect_ratio}")

    if beat_info:
        console.print(f"[bold]Music tempo:[/bold] {beat_info.tempo:.1f} BPM")


if __name__ == "__main__":
    main()
