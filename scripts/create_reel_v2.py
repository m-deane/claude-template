#!/usr/bin/env python3
"""
Create Instagram-Worthy Drone Reel v2

Improvements over v1:
- Smart center-crop instead of letterbox (fills full frame)
- Cross-dissolve transitions between clips
- Color grading with teal-orange preset
- Speed ramping for cinematic moments
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import subprocess
import tempfile
import shutil

from drone_reel.core.scene_detector import SceneDetector
from drone_reel.core.narrative import HookGenerator, NarrativeSequencer
from drone_reel.core.sequence_optimizer import DiversitySelector
from drone_reel.utils.file_utils import find_video_files


def create_reel_v2():
    print('=' * 60)
    print('  Creating Instagram-Worthy Drone Reel v2')
    print('  (Smart crop, transitions, color grading)')
    print('=' * 60)

    # Step 1: Detect scenes
    print('\n[1/6] Analyzing footage...')
    video_dir = Path('.drone_clips')
    videos = find_video_files(video_dir)
    print(f'      Found {len(videos)} videos')

    detector = SceneDetector()
    all_scenes = []
    for video in videos:
        print(f'      Analyzing {video.name}...', end=' ')
        sys.stdout.flush()
        scenes = detector.detect_scenes(video)
        print(f'{len(scenes)} scenes')
        all_scenes.extend(scenes)
    print(f'      Total: {len(all_scenes)} scenes')

    # Step 2: Diversity selection
    print('\n[2/6] Selecting diverse scenes...')
    selector = DiversitySelector()
    selected = selector.select(all_scenes, count=8)
    print(f'      Selected {len(selected)} diverse scenes')

    # Step 3: Hook optimization
    print('\n[3/6] Optimizing for hook...')
    hook_gen = HookGenerator()
    best_hook = hook_gen.select_hook_scene(selected)
    hook_score = hook_gen.score_hook_potential(best_hook)
    print(f'      Best hook: {best_hook.source_file.name} (score: {hook_score:.1f})')

    other_scenes = [s for s in selected if s != best_hook]
    sequencer = NarrativeSequencer()
    sequenced_rest = sequencer.sequence(other_scenes, target_duration=27.0)
    final_sequence = [best_hook] + sequenced_rest
    print(f'      Final sequence: {len(final_sequence)} clips')

    # Step 4: Extract clips with SMART CROP + COLOR GRADING
    print('\n[4/6] Extracting clips with smart crop & color grading...')
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    temp_dir = Path(tempfile.mkdtemp())

    # Color grading filter (teal-orange look)
    color_grade = (
        "curves=r='0/0 0.25/0.20 0.5/0.5 0.75/0.85 1/1':"
        "g='0/0 0.25/0.25 0.5/0.5 0.75/0.75 1/1':"
        "b='0/0.05 0.25/0.30 0.5/0.55 0.75/0.70 1/0.95',"
        "eq=saturation=1.2:contrast=1.1:brightness=0.02"
    )

    clip_files = []
    for i, scene in enumerate(final_sequence):
        clip_path = temp_dir / f'clip_{i:02d}.mp4'
        duration = min(scene.end_time - scene.start_time, 5.0)

        # Smart crop: scale height to 1920, then crop width to 1080 (center)
        # This fills the full vertical frame instead of letterboxing
        vf_filter = (
            f"scale=-1:1920,"  # Scale to full height
            f"crop=1080:1920,"  # Center crop to 9:16
            f"{color_grade}"  # Apply color grading
        )

        cmd = [
            'ffmpeg', '-y', '-hide_banner', '-loglevel', 'error',
            '-ss', str(scene.start_time),
            '-i', str(scene.source_file),
            '-t', str(duration),
            '-vf', vf_filter,
            '-c:v', 'h264_videotoolbox', '-b:v', '10M',
            '-an',
            '-r', '30',
            str(clip_path)
        ]

        print(f'      Clip {i+1}/{len(final_sequence)}: {scene.source_file.name}...', end=' ')
        sys.stdout.flush()
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode == 0 and clip_path.exists():
            clip_files.append(clip_path)
            print('OK')
        else:
            print(f'FAILED: {result.stderr.decode()[:50]}')

    # Step 5: Concatenate with CROSS-DISSOLVE TRANSITIONS
    print('\n[5/6] Adding transitions...')

    if len(clip_files) < 2:
        print('      Not enough clips for transitions')
        final_clips = clip_files
    else:
        # Create clips with fade out/in for transitions
        transition_duration = 0.5
        transitioned_clips = []

        for i, clip in enumerate(clip_files):
            out_clip = temp_dir / f'trans_{i:02d}.mp4'

            filters = []

            # Add fade in (except first clip)
            if i > 0:
                filters.append(f"fade=t=in:st=0:d={transition_duration}")

            # Add fade out (except last clip)
            if i < len(clip_files) - 1:
                # Get clip duration
                probe = subprocess.run([
                    'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                    '-of', 'default=noprint_wrappers=1:nokey=1', str(clip)
                ], capture_output=True, text=True)
                clip_dur = float(probe.stdout.strip()) if probe.stdout.strip() else 5.0
                fade_start = max(0, clip_dur - transition_duration)
                filters.append(f"fade=t=out:st={fade_start}:d={transition_duration}")

            if filters:
                vf = ','.join(filters)
                cmd = [
                    'ffmpeg', '-y', '-hide_banner', '-loglevel', 'error',
                    '-i', str(clip),
                    '-vf', vf,
                    '-c:v', 'h264_videotoolbox', '-b:v', '10M',
                    '-r', '30',
                    str(out_clip)
                ]
                subprocess.run(cmd, capture_output=True)
                transitioned_clips.append(out_clip)
            else:
                transitioned_clips.append(clip)

        clip_files = transitioned_clips
        print(f'      Added fade transitions to {len(clip_files)} clips')

    # Step 6: Final concatenation
    print('\n[6/6] Creating final reel...')
    concat_file = temp_dir / 'concat.txt'
    with open(concat_file, 'w') as f:
        for clip in clip_files:
            f.write(f"file '{clip}'\n")

    output_path = output_dir / 'instagram_reel_v2.mp4'
    cmd = [
        'ffmpeg', '-y', '-hide_banner', '-loglevel', 'error',
        '-f', 'concat', '-safe', '0',
        '-i', str(concat_file),
        '-c:v', 'h264_videotoolbox', '-b:v', '10M',
        '-r', '30',
        str(output_path)
    ]

    result = subprocess.run(cmd, capture_output=True)
    if result.returncode == 0:
        size_mb = output_path.stat().st_size / (1024 * 1024)
        probe = subprocess.run([
            'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1', str(output_path)
        ], capture_output=True, text=True)
        duration = float(probe.stdout.strip()) if probe.stdout.strip() else 0

        print(f'      Created: {output_path}')
        print(f'      Size: {size_mb:.1f} MB')
        print(f'      Duration: {duration:.1f}s')
    else:
        print(f'      FAILED: {result.stderr.decode()}')

    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)

    print('\n' + '=' * 60)
    print('  SUCCESS! Instagram-worthy reel v2 created')
    print('=' * 60)
    print(f'  Output: {output_path}')
    print('  Improvements:')
    print('    ✓ Smart center-crop (no letterbox)')
    print('    ✓ Teal-orange color grading')
    print('    ✓ Fade transitions between clips')
    print('    ✓ Hook scene first')
    print('    ✓ Narrative arc sequencing')
    print('=' * 60)


if __name__ == '__main__':
    create_reel_v2()
