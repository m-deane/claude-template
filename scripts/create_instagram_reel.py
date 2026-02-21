#!/usr/bin/env python3
"""
Create Instagram-Worthy Drone Reel

Demonstrates all the new viral-optimized features:
- Enhanced scene detection with camera motion classification
- Hook generator for attention-grabbing first 3 seconds
- Narrative arc sequencing (Hook → Build → Climax → Resolve)
- Diversity-aware scene selection
- Motion continuity optimization
- Speed ramping for cinematic effects
- Multi-platform export presets
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import cv2
import numpy as np
from drone_reel.core.scene_detector import SceneDetector, SceneInfo, EnhancedSceneInfo, MotionType
from drone_reel.core.narrative import HookGenerator, NarrativeSequencer, NarrativeArc, HookPattern
from drone_reel.core.sequence_optimizer import DiversitySelector, MotionContinuityEngine
from drone_reel.core.speed_ramper import SpeedRamper, SpeedRamp
from drone_reel.core.export_presets import Platform, PLATFORM_PRESETS, PlatformExporter
from drone_reel.core.preview import ThumbnailGenerator, PreviewGenerator
from drone_reel.utils.file_utils import find_video_files


def print_header(text: str):
    """Print formatted header."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}")


def print_section(text: str):
    """Print section header."""
    print(f"\n--- {text} ---")


def analyze_footage(video_dir: Path) -> list[EnhancedSceneInfo]:
    """Analyze all footage with enhanced scene detection."""
    print_section("Finding videos")
    video_files = find_video_files(video_dir)
    print(f"Found {len(video_files)} video files")

    print_section("Analyzing footage with enhanced detection")
    detector = SceneDetector()
    all_scenes = []

    for video_path in video_files:
        print(f"  Analyzing {video_path.name}...", end=" ", flush=True)
        try:
            scenes = detector.detect_scenes_enhanced(video_path)
            print(f"{len(scenes)} scenes")

            # Print motion types detected
            motion_types = {}
            for scene in scenes:
                mt = scene.motion_type.value
                motion_types[mt] = motion_types.get(mt, 0) + 1

            for mt, count in motion_types.items():
                print(f"    - {mt}: {count}")

            all_scenes.extend(scenes)
        except Exception as e:
            print(f"Error: {e}")

    return all_scenes


def select_best_scenes(scenes: list[EnhancedSceneInfo], count: int = 10) -> list[EnhancedSceneInfo]:
    """Select scenes with diversity awareness."""
    print_section("Diversity-aware scene selection")

    # Use diversity selector for variety
    selector = DiversitySelector()

    # Convert EnhancedSceneInfo to SceneInfo if needed
    base_scenes = [SceneInfo(
        start_time=s.start_time,
        end_time=s.end_time,
        score=s.score,
        source_file=s.source_file,
        motion_score=s.motion_score,
        composition_score=s.composition_score,
        color_score=s.color_score,
        sharpness_score=s.sharpness_score,
        brightness_score=s.brightness_score,
    ) for s in scenes]

    selected = selector.select(base_scenes, count)
    print(f"Selected {len(selected)} diverse scenes")

    # Map back to enhanced scenes
    selected_enhanced = []
    for sel in selected:
        for orig in scenes:
            if (orig.start_time == sel.start_time and
                orig.source_file == sel.source_file):
                selected_enhanced.append(orig)
                break

    return selected_enhanced


def create_hook_sequence(scenes: list[EnhancedSceneInfo]) -> list[SceneInfo]:
    """Create attention-grabbing hook for first 3 seconds."""
    print_section("Hook generation")

    hook_gen = HookGenerator()

    # Find the best hook scene
    base_scenes = [SceneInfo(
        start_time=s.start_time,
        end_time=s.end_time,
        score=s.score,
        source_file=s.source_file,
        motion_score=s.motion_score,
        composition_score=s.composition_score,
        color_score=s.color_score,
        sharpness_score=s.sharpness_score,
        brightness_score=s.brightness_score,
    ) for s in scenes]

    best_hook = hook_gen.select_hook_scene(base_scenes)
    hook_score = hook_gen.score_hook_potential(best_hook)

    print(f"Best hook scene: {best_hook.source_file.name}")
    print(f"  Time: {best_hook.start_time:.1f}s - {best_hook.end_time:.1f}s")
    print(f"  Hook potential score: {hook_score:.1f}")

    # Create hook sequence (quick cut montage for high energy)
    hook_sequence = hook_gen.create_hook_sequence(
        base_scenes[:5],  # Use top 5 scenes for montage
        pattern=HookPattern.QUICK_CUT_MONTAGE,
        hook_duration=3.0
    )

    print(f"Created {len(hook_sequence)} hook clips (3 seconds total)")
    return hook_sequence


def sequence_narrative(scenes: list[EnhancedSceneInfo], target_duration: float = 30.0) -> list[SceneInfo]:
    """Arrange scenes into compelling narrative arc."""
    print_section("Narrative arc sequencing")

    sequencer = NarrativeSequencer()

    base_scenes = [SceneInfo(
        start_time=s.start_time,
        end_time=s.end_time,
        score=s.score,
        source_file=s.source_file,
        motion_score=s.motion_score,
        composition_score=s.composition_score,
        color_score=s.color_score,
        sharpness_score=s.sharpness_score,
        brightness_score=s.brightness_score,
    ) for s in scenes]

    sequenced = sequencer.sequence(base_scenes, target_duration=target_duration)

    print(f"Sequenced {len(sequenced)} scenes for {target_duration}s reel")
    print("Narrative structure: Hook → Build → Climax → Resolve")

    # Show energy curve
    energy_curve = sequencer.calculate_energy_curve(sequenced)
    print("Energy curve: ", end="")
    for e in energy_curve:
        bars = int(e / 10)
        print("█" * bars, end=" ")
    print()

    return sequenced


def optimize_motion_continuity(scenes: list[EnhancedSceneInfo]) -> list[EnhancedSceneInfo]:
    """Optimize scene order for smooth motion flow."""
    print_section("Motion continuity optimization")

    engine = MotionContinuityEngine()
    optimized = engine.optimize_sequence(scenes)

    print("Optimized scene transitions for smooth motion flow")
    print("Rules applied:")
    print("  - No jarring pan-left to pan-right cuts")
    print("  - Match orbit directions")
    print("  - Static scenes as buffers")

    return optimized


def suggest_speed_ramps(scenes: list[SceneInfo]) -> list[SpeedRamp]:
    """Suggest speed ramps for cinematic effect."""
    print_section("Speed ramp suggestions")

    ramper = SpeedRamper()
    all_ramps = []

    for i, scene in enumerate(scenes[:3]):  # Demo first 3 scenes
        ramps = ramper.auto_detect_ramp_points(scene)
        if ramps:
            print(f"Scene {i+1}: {len(ramps)} speed ramps suggested")
            for ramp in ramps:
                print(f"  {ramp.start_time:.1f}s-{ramp.end_time:.1f}s: "
                      f"{ramp.start_speed}x → {ramp.end_speed}x ({ramp.easing})")
            all_ramps.extend(ramps)

    return all_ramps


def show_export_presets():
    """Display available export presets."""
    print_section("Export presets")

    exporter = PlatformExporter()

    # Show Instagram Reels preset
    instagram = exporter.get_preset(Platform.INSTAGRAM_REELS)
    print(f"Instagram Reels preset:")
    print(f"  Resolution: {instagram.resolution[0]}x{instagram.resolution[1]}")
    print(f"  FPS: {instagram.fps}")
    print(f"  Optimal duration: {instagram.optimal_duration[0]}-{instagram.optimal_duration[1]}s")
    print(f"  Max duration: {instagram.max_duration}s")

    # Suggest platforms for vertical video
    suggestions = exporter.suggest_platform(
        clip_duration=30.0,
        aspect_ratio=(9, 16),
    )
    print(f"\nRecommended platforms for 30s vertical video:")
    for platform in suggestions[:3]:
        print(f"  - {platform.value}")


def main():
    print_header("Instagram-Worthy Drone Reel Creator")
    print("Demonstrating all viral-optimized features")

    # Find video directory
    project_dir = Path(__file__).parent.parent
    video_dir = project_dir / ".drone_clips"

    if not video_dir.exists():
        print(f"\nError: Video directory not found: {video_dir}")
        print("Please place drone clips in .drone_clips/ directory")
        return

    # Step 1: Enhanced scene detection
    scenes = analyze_footage(video_dir)
    if not scenes:
        print("No scenes detected!")
        return

    print(f"\nTotal scenes analyzed: {len(scenes)}")

    # Step 2: Diversity-aware selection
    selected = select_best_scenes(scenes, count=8)

    # Step 3: Hook generation
    hook_clips = create_hook_sequence(selected)

    # Step 4: Narrative sequencing
    sequenced = sequence_narrative(selected, target_duration=30.0)

    # Step 5: Motion continuity (if we have enhanced scenes)
    if selected and hasattr(selected[0], 'motion_type'):
        optimized = optimize_motion_continuity(selected)

    # Step 6: Speed ramp suggestions
    ramps = suggest_speed_ramps(sequenced)

    # Step 7: Export presets
    show_export_presets()

    # Summary
    print_header("Summary")
    print(f"✓ Analyzed {len(scenes)} scenes from {len(set(s.source_file for s in scenes))} videos")
    print(f"✓ Selected {len(selected)} diverse scenes")
    print(f"✓ Created {len(hook_clips)} hook clips (3s total)")
    print(f"✓ Sequenced {len(sequenced)} scenes with narrative arc")
    print(f"✓ Suggested {len(ramps)} speed ramps")
    print(f"✓ Export preset ready: Instagram Reels (1080x1920, 30fps)")

    print("\n" + "="*60)
    print("To create the actual reel, run:")
    print("  python -m drone_reel create .drone_clips/ -o output/instagram_reel.mp4")
    print("="*60)


if __name__ == "__main__":
    main()
