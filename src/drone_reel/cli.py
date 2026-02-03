"""
Command-line interface for drone-reel.

Usage:
    drone-reel --input ./clips/ --music ./track.mp3 --output reel.mp4
    drone-reel --input ./clips/ --duration 30 --preset cinematic
"""

from pathlib import Path
from typing import Optional

import click
import numpy as np
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.table import Table
from rich.panel import Panel

from drone_reel import __version__
from drone_reel.core.beat_sync import BeatSync
from drone_reel.core.color_grader import ColorGrader, ColorPreset, get_preset_names
from drone_reel.core.reframer import Reframer, ReframeSettings, AspectRatio, ReframeMode
from drone_reel.core.scene_detector import SceneDetector
from drone_reel.core.sequence_optimizer import DiversitySelector
from drone_reel.core.speed_ramper import SpeedRamper, SpeedRamp
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
    type=float,
    default=45.0,
    help="Target duration in seconds (default: 45)",
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
    preview: bool,
    quality: str,
    resolution: str,
):
    """Create a reel from drone footage."""
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

            aspect = f"{preset.aspect_ratio[0]}:{preset.aspect_ratio[1]}"
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
        console.print("[red]Error:[/red] No video files found in input path")
        raise SystemExit(1)

    console.print(f"\n[green]Found {len(video_files)} video file(s)[/green]")

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
            # Use fast detection first
            scenes = scene_detector.detect_scenes(video_file)
            all_scenes.extend(scenes)
            progress.advance(task)

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
            )

            clip_durations = beat_sync.calculate_clip_durations(cut_points, duration)
        else:
            # Generate evenly spaced cuts without music
            num_clips = clips or max(1, int(duration / 3))
            clip_durations = [duration / num_clips] * num_clips

        # Step 3: Select best scenes with diversity optimization and motion filtering
        num_clips_needed = len(clip_durations)

        # Use DiversitySelector for better scene variety
        diversity_selector = DiversitySelector(
            diversity_weight=0.3,  # 30% diversity, 70% quality score
            max_per_source=3,      # Max 3 clips from same video
            min_temporal_gap=5.0,  # Min 5 seconds between clips from same source
        )

        # Get initial candidate scenes - more than needed so we can filter
        all_detected_scenes = all_scenes
        candidate_count = min(len(all_detected_scenes), num_clips_needed * 3)  # 3x candidates

        # Sort by score and get top candidates
        sorted_candidates = sorted(all_detected_scenes, key=lambda s: s.score, reverse=True)[:candidate_count]

        # Calculate motion energy only for top candidates (efficient approach)
        # Motion energy is computed via optical flow which is expensive
        import cv2
        from drone_reel.core.scene_detector import EnhancedSceneInfo, MotionType

        def calculate_scene_motion_energy(scene) -> float:
            """Calculate motion energy for a scene using optical flow (sampled)."""
            try:
                cap = cv2.VideoCapture(str(scene.source_file))
                fps = cap.get(cv2.CAP_PROP_FPS) or 30

                start_frame = int(scene.start_time * fps)
                end_frame = int(scene.end_time * fps)

                # Sample 5 frame pairs evenly across scene
                sample_interval = max(1, (end_frame - start_frame) // 6)
                sample_frames = list(range(start_frame, end_frame, sample_interval))[:6]

                motion_scores = []
                prev_gray = None

                for frame_num in sample_frames:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
                    ret, frame = cap.read()
                    if not ret:
                        continue

                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    # Resize for faster processing
                    gray = cv2.resize(gray, (320, 180))

                    if prev_gray is not None:
                        flow = cv2.calcOpticalFlowFarneback(
                            prev_gray, gray, None,
                            pyr_scale=0.5, levels=2, winsize=15,
                            iterations=2, poly_n=5, poly_sigma=1.1, flags=0
                        )
                        magnitude = cv2.magnitude(flow[..., 0], flow[..., 1])
                        motion_score = min(float(magnitude.mean()) / 3.0 * 100, 100.0)
                        motion_scores.append(motion_score)

                    prev_gray = gray

                cap.release()
                return float(np.mean(motion_scores)) if motion_scores else 0.0
            except Exception:
                return 0.0

        # Calculate motion energy for candidates
        progress.add_task("[cyan]Analyzing motion energy...", total=len(sorted_candidates))

        scene_motion_map = {}
        for scene in sorted_candidates:
            motion_energy = calculate_scene_motion_energy(scene)
            scene_motion_map[id(scene)] = motion_energy

        # Motion energy filtering thresholds
        MIN_MOTION_ENERGY = 25.0   # 25/100 - minimum acceptable motion
        IDEAL_MOTION_ENERGY = 45.0 # 45/100 - good motion level

        # Separate scenes into motion tiers, but preserve high-subject scenes
        high_motion_scenes = []
        medium_motion_scenes = []
        low_motion_scenes = []
        high_subject_scenes = []  # Scenes with interesting subjects (boats, people, etc.)

        SUBJECT_SCORE_THRESHOLD = 0.6  # Scenes with subjects above this are preserved

        for scene in sorted_candidates:
            motion_energy = scene_motion_map.get(id(scene), 0.0)

            # Check for high subject score (Fix #3: Include subject shots)
            subject_score = getattr(scene, 'subject_score', 0.0) if hasattr(scene, 'subject_score') else 0.0
            has_subject = subject_score >= SUBJECT_SCORE_THRESHOLD

            if has_subject:
                # High-subject scenes are always included regardless of motion
                high_subject_scenes.append(scene)
            elif motion_energy >= IDEAL_MOTION_ENERGY:
                high_motion_scenes.append(scene)
            elif motion_energy >= MIN_MOTION_ENERGY:
                medium_motion_scenes.append(scene)
            else:
                low_motion_scenes.append(scene)

        # Report subject scenes found
        if high_subject_scenes:
            console.print(f"[cyan]Subject detection:[/cyan] {len(high_subject_scenes)} scenes with interesting subjects preserved")

        # Prefer: high-subject, then high-motion, then medium-motion
        prioritized_scenes = high_subject_scenes + high_motion_scenes + medium_motion_scenes

        # If we don't have enough scenes, add low motion
        if len(prioritized_scenes) < num_clips_needed:
            prioritized_scenes.extend(low_motion_scenes)
            if low_motion_scenes:
                console.print(f"[yellow]Warning:[/yellow] Including {len(low_motion_scenes)} low-motion scenes to meet clip count")
        else:
            console.print(f"[green]Motion filtering:[/green] {len(high_motion_scenes)} high, {len(medium_motion_scenes)} medium, {len(low_motion_scenes)} filtered out")

        # Use diversity-aware selection on prioritized scenes
        selected_scenes = diversity_selector.select(prioritized_scenes, count=num_clips_needed)

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
            clip_durations = clip_durations[:len(selected_scenes)]

        # Reorder scenes: put highest hook_potential + motion clips first for strong opening
        # Fix #2: Start with most dynamic/interesting shot
        from drone_reel.core.scene_detector import EnhancedSceneInfo, HookPotential

        def get_opening_score(scene):
            """
            Score for opening clip selection (higher = better for opening).
            Combines hook potential, motion energy, and subject interest.
            """
            score = 0.0

            if isinstance(scene, EnhancedSceneInfo):
                # Hook tier contribution (0-50 points)
                tier_scores = {
                    HookPotential.MAXIMUM: 50,
                    HookPotential.HIGH: 40,
                    HookPotential.MEDIUM: 25,
                    HookPotential.LOW: 10,
                    HookPotential.POOR: 0,
                }
                score += tier_scores.get(scene.hook_tier, 25)

                # Motion energy contribution (0-30 points)
                motion = scene_motion_map.get(id(scene), 0.0)
                score += min(motion, 100) * 0.3  # Cap at 30 points

                # Subject score contribution (0-20 points)
                subject = getattr(scene, 'subject_score', 0.0)
                score += subject * 20

            return score

        def get_hook_priority(scene):
            """Get hook priority for subsequent clips (lower = first)."""
            if isinstance(scene, EnhancedSceneInfo):
                tier_priority = {
                    HookPotential.MAXIMUM: 0,
                    HookPotential.HIGH: 1,
                    HookPotential.MEDIUM: 2,
                    HookPotential.LOW: 3,
                    HookPotential.POOR: 4,
                }
                return (tier_priority.get(scene.hook_tier, 2), -scene.hook_potential)
            return (2, 0)  # Default to MEDIUM priority

        # Select BEST opening clip based on combined score (hook + motion + subject)
        best_opener = max(selected_scenes, key=get_opening_score)
        other_scenes = [s for s in selected_scenes if s is not best_opener]

        # Sort remaining by hook potential
        other_scenes = sorted(other_scenes, key=get_hook_priority)

        # Rebuild list with best opener first
        selected_scenes = [best_opener] + other_scenes

        # Motion variety sequencing: avoid consecutive clips with same motion type
        # Keep first scene (best hook) fixed, then reorder rest to maximize variety
        from drone_reel.core.scene_detector import MotionType

        def get_motion_type(scene):
            if isinstance(scene, EnhancedSceneInfo):
                return scene.motion_type
            return MotionType.STATIC

        if len(selected_scenes) > 2:
            # Keep first scene (best hook), reorder rest for motion variety
            reordered = [selected_scenes[0]]
            remaining = selected_scenes[1:]

            while remaining:
                last_motion = get_motion_type(reordered[-1])
                # Find a scene with different motion type
                different_motion = [s for s in remaining if get_motion_type(s) != last_motion]

                if different_motion:
                    # Pick the one with best hook potential
                    next_scene = min(different_motion, key=get_hook_priority)
                else:
                    # All have same motion - just pick best remaining
                    next_scene = min(remaining, key=get_hook_priority)

                reordered.append(next_scene)
                remaining.remove(next_scene)

            selected_scenes = reordered

        # Filter out blurry scenes using sharpness threshold
        import cv2

        def get_scene_sharpness(scene) -> float:
            """Calculate sharpness of scene midpoint frame using Laplacian variance."""
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

        # Calculate sharpness for all scenes and store for duration adjustment
        scene_sharpness_map = {id(scene): get_scene_sharpness(scene) for scene in selected_scenes}

        # Adjust clip durations based on scene characteristics AND sharpness
        # Enforce global duration limits: min 1.5s, max 4.0s
        # Blurry clips get shorter durations, sharp clips get longer
        SHARP_THRESHOLD = 100  # Above this = sharp (full duration)
        SOFT_THRESHOLD = 30    # Below this = very blurry (minimum duration)

        adjusted_durations = []
        for i, (scene, dur) in enumerate(zip(selected_scenes, clip_durations)):
            adjusted_dur = dur
            sharpness = scene_sharpness_map.get(id(scene), 100)

            # Sharpness-based duration scaling
            if sharpness < SOFT_THRESHOLD:
                # Very blurry - use minimum duration
                adjusted_dur = 2.0
            elif sharpness < SHARP_THRESHOLD:
                # Soft but acceptable - reduce duration proportionally
                # Scale from 2.0s (at 30 sharpness) to full dur (at 100 sharpness)
                scale = (sharpness - SOFT_THRESHOLD) / (SHARP_THRESHOLD - SOFT_THRESHOLD)
                adjusted_dur = 2.0 + (dur - 2.0) * scale

            if isinstance(scene, EnhancedSceneInfo):
                # MAXIMUM/HIGH hook tier scenes with good sharpness: ensure minimum showcase time
                if scene.hook_tier in (HookPotential.MAXIMUM, HookPotential.HIGH) and sharpness >= SOFT_THRESHOLD:
                    adjusted_dur = max(adjusted_dur, 3.0)  # At least 3 seconds for best shots

                # LOW/POOR hook tier: cap duration to keep pacing tight
                elif scene.hook_tier in (HookPotential.LOW, HookPotential.POOR):
                    adjusted_dur = min(adjusted_dur, 2.0)  # Max 2 seconds for weak shots

                # Static scenes: cap duration to avoid boring segments
                if scene.motion_type == MotionType.STATIC:
                    adjusted_dur = min(adjusted_dur, 2.5)  # Static shots max 2.5s

            # Enforce global duration limits
            adjusted_dur = max(2.0, min(4.0, adjusted_dur))  # Min 2.0s, max 4.0s

            adjusted_durations.append(adjusted_dur)

        clip_durations = adjusted_durations

        # Calculate actual duration
        actual_duration = sum(clip_durations)

        # Preview mode - show plan and exit
        if preview:
            _show_preview(selected_scenes, clip_durations, config, beat_info)
            return

        # Step 4: Generate dynamic transitions
        import random
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
        else:
            # Generate varied dynamic transitions even without music
            dynamic_transitions = [
                TransitionType.CROSSFADE,
                TransitionType.ZOOM_IN,
                TransitionType.ZOOM_OUT,
                TransitionType.FADE_BLACK,
            ]
            transitions = []
            for i in range(len(selected_scenes)):
                # Alternate between transition types for variety
                if i == 0:
                    transitions.append(TransitionType.FADE_BLACK)  # Start with fade in
                elif i == len(selected_scenes) - 1:
                    transitions.append(TransitionType.FADE_BLACK)  # End with fade out
                else:
                    # Mix of crossfades and zooms
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
        }

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
        if not no_reframe:
            from drone_reel.core.scene_detector import MotionType, EnhancedSceneInfo
            import random

            for i, scene in enumerate(selected_scenes):
                # Get scene characteristics
                motion_type = MotionType.STATIC
                subject_score = 0.0

                if isinstance(scene, EnhancedSceneInfo):
                    motion_type = scene.motion_type
                    subject_score = scene.subject_score

                # Decision logic:
                # 1. High subject score (>= 40) with movement -> gentle subject tracking
                # 2. Landscape/panorama (low subject score) -> stable center or subtle Ken Burns
                # 3. Camera already moving -> stable center crop

                has_active_subject = subject_score >= 40
                camera_moving = motion_type in (
                    MotionType.PAN_LEFT, MotionType.PAN_RIGHT,
                    MotionType.TILT_UP, MotionType.TILT_DOWN,
                    MotionType.ORBIT_CW, MotionType.ORBIT_CCW,
                    MotionType.FLYOVER, MotionType.REVEAL, MotionType.FPV
                )

                # Get clip duration to scale movement speed
                clip_duration = clip_durations[i] if i < len(clip_durations) else 3.0

                # Scale factor: longer clips can have more movement
                # Base is 3 seconds, so a 2-sec clip gets 0.67x, a 4-sec clip gets 1.33x
                duration_scale = min(clip_duration / 3.0, 1.5)  # Cap at 1.5x

                if has_active_subject and not camera_moving:
                    # Scene has subjects - ultra-smooth, barely perceptible tracking
                    # Scale smoothness inversely with duration (shorter = smoother)
                    smoothness = 0.003 * duration_scale  # Even slower base

                    settings = ReframeSettings(
                        target_ratio=AspectRatio.VERTICAL_9_16,
                        mode=ReframeMode.SMART,
                        output_width=output_w,
                        tracking_smoothness=smoothness,  # Ultra-slow, scales with duration
                        saliency_cache_frames=240,  # Update very rarely (every 8 sec at 30fps)
                        smooth_tracking=True,
                        adaptive_smoothing=False,
                        focal_clamp_x=(0.4, 0.6),  # Very tight bounds - barely moves from center
                        focal_clamp_y=(0.4, 0.6),  # Minimal vertical movement
                    )
                elif camera_moving:
                    # Camera already moving - stable center crop, no additional movement
                    settings = ReframeSettings(
                        target_ratio=AspectRatio.VERTICAL_9_16,
                        mode=ReframeMode.CENTER,
                        output_width=output_w,
                    )
                else:
                    # Landscape panorama - very subtle Ken Burns scaled by duration
                    # Shorter clips get less pan to avoid looking rushed
                    base_pan = 0.008 * duration_scale  # Reduced base pan
                    pan_x = random.uniform(-base_pan, base_pan)
                    pan_y = random.uniform(-base_pan * 0.5, base_pan * 0.5)

                    settings = ReframeSettings(
                        target_ratio=AspectRatio.VERTICAL_9_16,
                        mode=ReframeMode.KEN_BURNS,
                        output_width=output_w,
                        ken_burns_zoom_start=1.0,
                        ken_burns_zoom_end=1.01,  # Even more minimal zoom (1%)
                        ken_burns_pan_direction=(pan_x, pan_y),
                        ken_burns_ease_curve="ease_in_out",
                    )

                clip_reframers.append(Reframer(settings))

        # Step 7: Stitch video
        task = progress.add_task("[cyan]Stitching video...", total=100)

        def update_progress(p):
            progress.update(task, completed=int(p * 100))

        ensure_output_dir(output_path)
        output_path = get_unique_output_path(output_path)

        video_processor.stitch_clips(
            segments,
            output_path,
            audio_path=music_path,
            target_size=None,  # Let reframers handle sizing
            progress_callback=update_progress,
            reframers=clip_reframers if clip_reframers else None,
        )

        # Step 8: Apply color grading (if enabled)
        if not no_color and color != "none":
            task = progress.add_task("[cyan]Applying color grade...", total=100)

            color_grader = ColorGrader(preset=ColorPreset(color))

            graded_path = output_path.with_stem(output_path.stem + "_graded")

            def update_color_progress(p):
                progress.update(task, completed=int(p * 100))

            color_grader.grade_video(
                output_path,
                graded_path,
                progress_callback=update_color_progress,
                video_bitrate=video_bitrate,
                audio_bitrate=audio_bitrate,
            )

            # Replace original with graded
            output_path.unlink()
            graded_path.rename(output_path)

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
