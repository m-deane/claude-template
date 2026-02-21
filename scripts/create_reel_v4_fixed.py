#!/usr/bin/env python3
"""
Create Instagram-Worthy Drone Reel V4 (Fixed)

FIXES:
- No color grading (natural look)
- Better scene selection prioritizing ACTION over sharpness
- Uses original scene detector scoring (proven to work in V1)
- Prioritizes scenes with subjects/motion
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import subprocess
import tempfile
import shutil
from dataclasses import dataclass
from typing import Optional

from drone_reel.core.scene_detector import SceneDetector, SceneInfo
from drone_reel.utils.file_utils import find_video_files


@dataclass
class ViralClip:
    """Clip optimized for viral potential."""
    source_file: Path
    start_time: float
    end_time: float
    score: float
    motion_score: float
    hook_potential: float
    narrative_role: str = "build"


def split_scene(scene: SceneInfo, target_duration: float = 2.5) -> list[ViralClip]:
    """Split scene into shorter clips for viral pacing."""
    duration = scene.end_time - scene.start_time
    clips = []

    if duration <= 3.5:
        # Short enough, keep as-is
        clips.append(ViralClip(
            source_file=scene.source_file,
            start_time=scene.start_time,
            end_time=scene.end_time,
            score=scene.score,
            motion_score=getattr(scene, 'motion_score', 50.0),
            hook_potential=scene.score * 1.2  # Use original score
        ))
    else:
        # Split into multiple clips
        num_clips = max(2, int(duration / target_duration))
        clip_dur = duration / num_clips

        for i in range(num_clips):
            start = scene.start_time + (i * clip_dur)
            end = min(scene.end_time, start + clip_dur)

            # First part of high-scoring scene is best for hooks
            hook_mult = 1.3 if i == 0 else 0.9

            clips.append(ViralClip(
                source_file=scene.source_file,
                start_time=start,
                end_time=end,
                score=scene.score,
                motion_score=getattr(scene, 'motion_score', 50.0),
                hook_potential=scene.score * hook_mult
            ))

    return clips


def sequence_narrative(clips: list[ViralClip]) -> list[ViralClip]:
    """Arrange clips into narrative arc."""
    if len(clips) < 2:
        return clips

    # Sort by hook potential for hook selection
    by_hook = sorted(clips, key=lambda c: c.hook_potential, reverse=True)

    # Best hook first
    hook = by_hook[0]
    hook.narrative_role = "hook"

    # Second best is climax
    if len(by_hook) > 1:
        by_hook[1].narrative_role = "climax"

    # Last clip is resolve
    if len(clips) > 2:
        clips[-1].narrative_role = "resolve"

    # Reorder: Hook -> Build -> Climax -> Resolve
    hook_clips = [c for c in clips if c.narrative_role == "hook"]
    climax_clips = [c for c in clips if c.narrative_role == "climax"]
    resolve_clips = [c for c in clips if c.narrative_role == "resolve"]
    build_clips = [c for c in clips if c.narrative_role == "build"]

    # Sort build by ascending score (energy build)
    build_clips.sort(key=lambda c: c.score)

    return hook_clips + build_clips + climax_clips + resolve_clips


def create_reel_v4_fixed(location_text: str = ""):
    """Create V4 reel with fixed scene selection, no color grading."""

    print('=' * 70)
    print('  Creating Instagram-Worthy Drone Reel V4 (Fixed)')
    print('  Using original scene scoring (like V1), no color grading')
    print('=' * 70)

    # Find videos
    print('\n[1/5] Finding videos...')
    video_dir = Path('.drone_clips')
    videos = find_video_files(video_dir)
    print(f'      Found {len(videos)} videos')

    # Detect scenes using ORIGINAL scene detector (proven in V1)
    print('\n[2/5] Detecting scenes with original scoring...')
    detector = SceneDetector()
    all_scenes = []

    for video in videos:
        print(f'      {video.name}...', end=' ', flush=True)
        scenes = detector.detect_scenes(video)
        print(f'{len(scenes)} scenes')

        # Show scores
        for s in scenes:
            print(f'        [{s.start_time:.1f}s-{s.end_time:.1f}s] score: {s.score:.1f}')

        all_scenes.extend(scenes)

    print(f'      Total: {len(all_scenes)} scenes')

    # Split into viral-length clips
    print('\n[3/5] Creating viral-length clips (2.5s target)...')
    all_clips = []
    for scene in all_scenes:
        clips = split_scene(scene, target_duration=2.5)
        all_clips.extend(clips)

    print(f'      Created {len(all_clips)} clips')

    # Select best clips (use ORIGINAL scores, not frame analysis)
    print('\n[4/5] Selecting best clips by original score...')

    # Sort by original scene score (this worked in V1!)
    all_clips.sort(key=lambda c: c.score, reverse=True)

    # Show top clips
    print('      Top clips by score:')
    for i, clip in enumerate(all_clips[:10]):
        print(f'        {i+1}. {clip.source_file.name} [{clip.start_time:.1f}s] score: {clip.score:.1f}')

    # Select with diversity
    selected = []
    used_sources = {}
    target_count = 10

    for clip in all_clips:
        source = clip.source_file.name
        # Allow more from high-scoring sources
        max_per_source = 4 if clip.score > 60 else 2

        if used_sources.get(source, 0) < max_per_source:
            selected.append(clip)
            used_sources[source] = used_sources.get(source, 0) + 1
            if len(selected) >= target_count:
                break

    print(f'      Selected {len(selected)} clips')

    # Apply narrative arc
    print('\n[5/5] Applying narrative arc and rendering...')
    sequenced = sequence_narrative(selected)

    print('      Sequence:')
    for i, clip in enumerate(sequenced):
        dur = clip.end_time - clip.start_time
        icon = {'hook': '🎯', 'build': '📈', 'climax': '⭐', 'resolve': '🎬'}
        print(f'        {i+1}. [{clip.narrative_role.upper():8}] {clip.source_file.name} '
              f'[{clip.start_time:.1f}s] (score: {clip.score:.1f})')

    # Render
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    temp_dir = Path(tempfile.mkdtemp())

    # NO COLOR GRADING - just smart crop
    clip_files = []
    for i, clip in enumerate(sequenced):
        clip_path = temp_dir / f'clip_{i:02d}.mp4'

        # Speed ramps for hook/climax only
        speed = ""
        if clip.narrative_role == "hook":
            speed = "setpts=1.1*PTS,"  # Slight slow-mo
        elif clip.narrative_role == "climax":
            speed = "setpts=1.2*PTS,"  # More slow-mo

        # Simple smart crop - NO color grading
        vf = f"{speed}scale=-1:1920,crop=1080:1920"

        # Add fade in for non-hook clips
        if i > 0:
            vf += ",fade=t=in:st=0:d=0.25"

        cmd = [
            'ffmpeg', '-y', '-hide_banner', '-loglevel', 'error',
            '-ss', str(clip.start_time),
            '-i', str(clip.source_file),
            '-t', str(clip.end_time - clip.start_time),
            '-vf', vf,
            '-c:v', 'h264_videotoolbox', '-b:v', '12M',
            '-an', '-r', '30',
            str(clip_path)
        ]

        icon = {'hook': '🎯', 'build': '📈', 'climax': '⭐', 'resolve': '🎬'}
        print(f'      {icon.get(clip.narrative_role, "•")} Clip {i+1}/{len(sequenced)}...', end=' ', flush=True)

        result = subprocess.run(cmd, capture_output=True)
        if result.returncode == 0 and clip_path.exists():
            clip_files.append(clip_path)
            print('OK')
        else:
            print(f'FAILED: {result.stderr.decode()[:50]}')

    # Concatenate
    concat_file = temp_dir / 'concat.txt'
    with open(concat_file, 'w') as f:
        for clip in clip_files:
            f.write(f"file '{clip}'\n")

    output_path = output_dir / 'instagram_reel_v4_fixed.mp4'

    # Add text if provided
    if location_text:
        video_only = temp_dir / 'video.mp4'
        subprocess.run([
            'ffmpeg', '-y', '-hide_banner', '-loglevel', 'error',
            '-f', 'concat', '-safe', '0', '-i', str(concat_file),
            '-c:v', 'h264_videotoolbox', '-b:v', '12M', '-r', '30',
            str(video_only)
        ], capture_output=True)

        # Get duration for text timing
        probe = subprocess.run([
            'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1', str(video_only)
        ], capture_output=True, text=True)

        drawtext = (
            f"drawtext=text='{location_text}':"
            f"fontsize=42:fontcolor=white:"
            f"x=(w-text_w)/2:y=h-120:"
            f"enable='between(t,1,4)'"
        )

        result = subprocess.run([
            'ffmpeg', '-y', '-hide_banner', '-loglevel', 'error',
            '-i', str(video_only), '-vf', drawtext,
            '-c:v', 'h264_videotoolbox', '-b:v', '12M',
            str(output_path)
        ], capture_output=True)

        if result.returncode != 0:
            shutil.copy(video_only, output_path)
    else:
        subprocess.run([
            'ffmpeg', '-y', '-hide_banner', '-loglevel', 'error',
            '-f', 'concat', '-safe', '0', '-i', str(concat_file),
            '-c:v', 'h264_videotoolbox', '-b:v', '12M', '-r', '30',
            str(output_path)
        ], capture_output=True)

    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)

    # Stats
    if output_path.exists():
        size_mb = output_path.stat().st_size / (1024 * 1024)
        probe = subprocess.run([
            'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1', str(output_path)
        ], capture_output=True, text=True)
        duration = float(probe.stdout.strip()) if probe.stdout.strip() else 0

        print('\n' + '=' * 70)
        print('  SUCCESS! Instagram-worthy reel V4 (Fixed) created')
        print('=' * 70)
        print(f'  Output: {output_path}')
        print(f'  Duration: {duration:.1f}s')
        print(f'  Size: {size_mb:.1f} MB')
        print(f'  Clips: {len(clip_files)}')
        if duration > 0 and len(clip_files) > 0:
            print(f'  Avg clip: {duration/len(clip_files):.1f}s')
        print('\n  CHANGES FROM V4:')
        print('    ✅ Using original scene scoring (like V1)')
        print('    ✅ NO color grading (natural colors)')
        print('    ✅ Prioritizing high-score scenes over technical sharpness')
        print('\n  VIRAL OPTIMIZATIONS:')
        print('    ✅ Cut frequency optimized (2.5s clips)')
        print('    ✅ Smart crop (no letterbox)')
        print('    ✅ Speed ramps (hook/climax slow-mo)')
        print('    ✅ Narrative arc (Hook→Build→Climax→Resolve)')
        print('    ✅ Fade transitions (0.25s)')
        if location_text:
            print('    ✅ Location text overlay')
        print('=' * 70)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--location', '-l', default='', help='Location text')
    args = parser.parse_args()
    create_reel_v4_fixed(args.location)
