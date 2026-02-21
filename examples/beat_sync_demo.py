"""
Demonstration of the upgraded BeatSync capabilities.

This script shows all the new features:
1. Multi-feature downbeat detection
2. Time signature estimation
3. Dynamic programming cut point optimization
4. Phrase boundary detection
5. Enhanced energy profiles with multiple metrics
6. Continuous transition intensity recommendations
7. Tempo change detection
"""

from pathlib import Path
import numpy as np
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from drone_reel.core.beat_sync import BeatSync


def demonstrate_beat_analysis(audio_path: Path):
    """Demonstrate comprehensive beat analysis."""
    console = Console()

    console.print(Panel.fit(
        "[bold blue]Beat Sync - Enhanced Analysis Demo[/bold blue]\n"
        "Demonstrating upgraded multi-feature beat detection",
        border_style="blue",
    ))

    # Initialize BeatSync
    beat_sync = BeatSync(hop_length=512, min_tempo=60.0, max_tempo=180.0)

    # Analyze audio
    console.print("\n[cyan]Analyzing audio file...[/cyan]")
    beat_info = beat_sync.analyze(audio_path)

    # Display basic tempo information
    console.print(f"\n[green]✓ Analysis complete![/green]")
    console.print(f"  Tempo: [bold]{beat_info.tempo:.1f} BPM[/bold]")
    console.print(f"  Duration: {beat_info.duration:.2f} seconds")
    console.print(f"  Time Signature: [bold]{beat_info.time_signature[0]}/{beat_info.time_signature[1]}[/bold]")
    console.print(f"  Beats detected: {beat_info.beat_count}")
    console.print(f"  Downbeats detected: {len(beat_info.downbeat_times)}")
    console.print(f"  Phrase boundaries: {len(beat_info.phrase_boundaries)}")

    # Display tempo changes if detected
    if beat_info.tempo_changes:
        console.print("\n[yellow]Tempo changes detected:[/yellow]")
        for time, new_tempo in beat_info.tempo_changes:
            console.print(f"  At {time:.2f}s: {new_tempo:.1f} BPM")

    # Display phrase boundaries
    if len(beat_info.phrase_boundaries) > 0:
        console.print("\n[cyan]Phrase boundaries:[/cyan]")
        for i, boundary_time in enumerate(beat_info.phrase_boundaries[:5]):
            console.print(f"  Phrase {i+1}: {boundary_time:.2f}s")
        if len(beat_info.phrase_boundaries) > 5:
            console.print(f"  ... and {len(beat_info.phrase_boundaries) - 5} more")

    # Generate cut points using dynamic programming
    console.print("\n[cyan]Generating optimal cut points...[/cyan]")
    cut_points = beat_sync.get_cut_points(
        beat_info,
        target_duration=30.0,
        min_clip_length=2.0,
        max_clip_length=4.0,
        prefer_downbeats=True,
    )

    # Create table for cut points
    table = Table(title="Optimal Cut Points (Dynamic Programming)")
    table.add_column("Cut #", style="cyan", justify="right")
    table.add_column("Time", style="magenta")
    table.add_column("Strength", style="green")
    table.add_column("Type", style="yellow")
    table.add_column("Transition", style="blue")
    table.add_column("Intensity", style="red")
    table.add_column("Energy", style="white")

    for i, cp in enumerate(cut_points[:10]):
        downbeat_marker = "🎵 " if cp.is_downbeat else "   "
        phrase_marker = "📍" if cp.is_phrase_boundary else "  "
        type_str = f"{downbeat_marker}{phrase_marker}"

        if cp.transition_rec:
            trans_type = cp.transition_rec.transition_type
            intensity = f"{cp.transition_rec.intensity:.2f}"
            gradient = cp.transition_rec.energy_gradient
        else:
            trans_type = "N/A"
            intensity = "N/A"
            gradient = "stable"

        energy = beat_sync.get_energy_at_time(beat_info, cp.time)

        table.add_row(
            str(i + 1),
            f"{cp.time:.2f}s",
            f"{cp.strength:.2f}",
            type_str,
            f"{trans_type} ({gradient})",
            intensity,
            f"{energy:.2f}",
        )

    console.print("\n")
    console.print(table)

    # Display transition recommendations
    console.print("\n[cyan]Transition Recommendations:[/cyan]")
    for i, cp in enumerate(cut_points[:5]):
        if cp.transition_rec:
            rec = cp.transition_rec
            console.print(
                f"  Cut {i+1} at {cp.time:.2f}s: "
                f"[bold]{rec.transition_type}[/bold] "
                f"(intensity: {rec.intensity:.2f}, "
                f"duration: {rec.duration:.2f}s, "
                f"gradient: {rec.energy_gradient})"
            )

    # Calculate clip durations
    durations = beat_sync.calculate_clip_durations(cut_points, target_duration=30.0)
    console.print(f"\n[green]Generated {len(durations)} clips[/green]")
    console.print(f"  Average clip length: {np.mean(durations):.2f}s")
    console.print(f"  Min: {np.min(durations):.2f}s, Max: {np.max(durations):.2f}s")

    # Display energy profile statistics
    console.print("\n[cyan]Energy Profile Analysis:[/cyan]")
    console.print(f"  Overall energy: {np.mean(beat_info.energy_profile):.2f}")
    console.print(f"  Spectral brightness: {np.mean(beat_info.spectral_profile):.2f}")
    console.print(f"  Onset density: {np.mean(beat_info.onset_density):.2f}")
    console.print(f"  Harmonic energy: {np.mean(beat_info.harmonic_energy):.2f}")
    console.print(f"  Percussive energy: {np.mean(beat_info.percussive_energy):.2f}")

    # Show comparison: old vs new method
    console.print("\n[bold]Key Improvements:[/bold]")
    console.print("  ✓ Multi-feature downbeat detection (onset + bass + percussion)")
    console.print("  ✓ Time signature estimation")
    console.print("  ✓ Dynamic programming for globally optimal cuts")
    console.print("  ✓ Phrase boundary detection for natural transitions")
    console.print("  ✓ Continuous intensity values (0-1) vs discrete (hard/medium/soft)")
    console.print("  ✓ Transition type recommendations (cut/fade/crossfade/impact)")
    console.print("  ✓ Energy gradient detection (rising/falling/stable)")
    console.print("  ✓ Tempo change detection")

    return beat_info, cut_points


def compare_old_vs_new_intensity(audio_path: Path):
    """Compare old and new transition intensity methods."""
    console = Console()

    console.print("\n" + "="*70)
    console.print(Panel.fit(
        "[bold yellow]Transition Intensity Comparison[/bold yellow]\n"
        "Old: 3-level discrete (hard/medium/soft)\n"
        "New: Continuous 0-1 with type and gradient",
        border_style="yellow",
    ))

    beat_sync = BeatSync()
    beat_info = beat_sync.analyze(audio_path)
    cut_points = beat_sync.get_cut_points(
        beat_info,
        target_duration=20.0,
        min_clip_length=2.0,
        max_clip_length=4.0,
    )

    table = Table(title="Intensity Method Comparison")
    table.add_column("Cut", style="cyan", justify="right")
    table.add_column("Time", style="magenta")
    table.add_column("Old Method", style="yellow")
    table.add_column("New Intensity", style="green")
    table.add_column("Type", style="blue")
    table.add_column("Gradient", style="red")

    for i, cp in enumerate(cut_points[:8]):
        old_intensity = beat_sync.suggest_transition_intensity(beat_info, cp)

        if cp.transition_rec:
            new_intensity = f"{cp.transition_rec.intensity:.3f}"
            trans_type = cp.transition_rec.transition_type
            gradient = cp.transition_rec.energy_gradient
        else:
            new_intensity = "N/A"
            trans_type = "N/A"
            gradient = "N/A"

        table.add_row(
            str(i + 1),
            f"{cp.time:.2f}s",
            old_intensity,
            new_intensity,
            trans_type,
            gradient,
        )

    console.print("\n")
    console.print(table)


def demonstrate_phrase_boundaries(audio_path: Path):
    """Demonstrate phrase boundary detection."""
    console = Console()

    console.print("\n" + "="*70)
    console.print(Panel.fit(
        "[bold magenta]Phrase Boundary Detection[/bold magenta]\n"
        "Using spectral clustering to find musical sections",
        border_style="magenta",
    ))

    beat_sync = BeatSync()
    beat_info = beat_sync.analyze(audio_path)

    console.print(f"\n[green]Detected {len(beat_info.phrase_boundaries)} phrase boundaries[/green]")

    # Show phrase boundaries with surrounding context
    table = Table(title="Phrase Boundaries")
    table.add_column("Phrase #", style="cyan", justify="right")
    table.add_column("Start Time", style="magenta")
    table.add_column("Energy", style="green")
    table.add_column("Spectral", style="yellow")
    table.add_column("Notes", style="white")

    for i, boundary_time in enumerate(beat_info.phrase_boundaries[:10]):
        energy = beat_sync.get_energy_at_time(beat_info, boundary_time)

        # Get spectral centroid at this time
        idx = int(boundary_time / beat_info.duration * len(beat_info.spectral_profile))
        idx = max(0, min(idx, len(beat_info.spectral_profile) - 1))
        spectral = beat_info.spectral_profile[idx]

        # Check if it's also a downbeat
        is_downbeat = np.any(np.abs(beat_info.downbeat_times - boundary_time) < 0.1)
        notes = "🎵 Downbeat" if is_downbeat else "Regular boundary"

        table.add_row(
            str(i + 1),
            f"{boundary_time:.2f}s",
            f"{energy:.2f}",
            f"{spectral:.2f}",
            notes,
        )

    console.print("\n")
    console.print(table)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        console = Console()
        console.print("[red]Usage:[/red] python beat_sync_demo.py <audio_file.mp3>")
        console.print("\nExample: python beat_sync_demo.py music/track.mp3")
        sys.exit(1)

    audio_path = Path(sys.argv[1])

    if not audio_path.exists():
        console = Console()
        console.print(f"[red]Error:[/red] File not found: {audio_path}")
        sys.exit(1)

    # Run all demonstrations
    beat_info, cut_points = demonstrate_beat_analysis(audio_path)
    compare_old_vs_new_intensity(audio_path)
    demonstrate_phrase_boundaries(audio_path)

    console = Console()
    console.print("\n" + "="*70)
    console.print("[bold green]✓ Demo complete![/bold green]")
    console.print(f"\nProcessed: {audio_path.name}")
    console.print(f"Total duration: {beat_info.duration:.2f}s")
    console.print(f"Optimal cuts generated: {len(cut_points)}")
