"""
Command-line interface for drone-reel.

Usage:
    drone-reel --input ./clips/ --music ./track.mp3 --output reel.mp4
    drone-reel --input ./clips/ --duration 30 --preset cinematic
"""

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
from drone_reel.core.reframer import Reframer, ReframeSettings, AspectRatio, ReframeMode
from drone_reel.core.scene_detector import SceneDetector
from drone_reel.core.video_processor import VideoProcessor, TransitionType
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
def create(
    input_path: Path,
    music_path: Optional[Path],
    output_path: Path,
    duration: float,
    color: str,
    reframe: str,
    aspect: str,
    transition: str,
    clips: Optional[int],
    no_reframe: bool,
    no_color: bool,
    preview: bool,
):
    """Create a reel from drone footage."""
    config = load_config()
    config = merge_cli_args(
        config,
        output_duration=duration,
        color_preset=color,
        reframe_mode=reframe,
        aspect_ratio=aspect,
        transition_type=transition,
    )

    console.print(Panel.fit(
        "[bold blue]Drone Reel Creator[/bold blue]\n"
        f"Creating {duration}s reel with {color} color grade",
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

        # Step 1: Analyze scenes
        task = progress.add_task("[cyan]Analyzing scenes...", total=len(video_files))

        scene_detector = SceneDetector(
            threshold=config.scene_threshold,
            min_scene_length=config.min_scene_length,
            max_scene_length=config.max_scene_length,
        )

        all_scenes = []
        for video_file in video_files:
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

        # Step 3: Select best scenes
        num_clips_needed = len(clip_durations)
        selected_scenes = scene_detector.get_top_scenes(
            video_files,
            count=num_clips_needed,
            min_per_video=1,
        )

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

        # Calculate actual duration
        actual_duration = sum(clip_durations)

        # Preview mode - show plan and exit
        if preview:
            _show_preview(selected_scenes, clip_durations, config, beat_info)
            return

        # Step 4: Generate transitions
        if beat_info and cut_points:
            energy_levels = [
                beat_sync.get_energy_at_time(beat_info, cp.time)
                for cp in cut_points[:-1]
            ]
            avg_energy = sum(energy_levels) / len(energy_levels) if energy_levels else 0.5
            transitions = get_transitions_for_energy(
                avg_energy,
                len(selected_scenes),
                style="dynamic",
            )
        else:
            transitions = [TransitionType(transition)] * len(selected_scenes)

        # Step 5: Create clip segments
        video_processor = VideoProcessor(
            output_fps=config.output_fps,
            threads=config.threads,
            preset=config.preset,
        )

        segments = video_processor.create_segments_from_scenes(
            selected_scenes,
            clip_durations,
            transitions,
            config.transition_duration,
        )

        # Step 6: Determine output dimensions
        output_w, output_h = config.get_output_dimensions()
        target_size = (output_w, output_h) if not no_reframe else None

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
            target_size=target_size,
            progress_callback=update_progress,
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

    console.print(Panel.fit(
        f"[bold green]Reel created successfully![/bold green]\n\n"
        f"Output: [cyan]{output_path}[/cyan]\n"
        f"Duration: {duration_info}\n"
        f"Resolution: {output_w}x{output_h}\n"
        f"Clips: {len(selected_scenes)}",
        border_style="green",
    ))


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
