#!/usr/bin/env python3
"""Create Instagram-worthy drone reel with all new features."""

import sys
sys.path.insert(0, str(__file__).rsplit('/', 2)[0] + '/src')

from pathlib import Path
import subprocess
import tempfile
import shutil

from drone_reel.core.scene_detector import SceneDetector
from drone_reel.core.narrative import HookGenerator, NarrativeSequencer
from drone_reel.core.sequence_optimizer import DiversitySelector
from drone_reel.utils.file_utils import find_video_files


def main():
    print('=' * 60)
    print('  Creating Instagram-Worthy Drone Reel')
    print('=' * 60)

    # Step 1: Detect scenes
    print('\n[1/5] Analyzing footage...')
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
    print('\n[2/5] Selecting diverse scenes...')
    selector = DiversitySelector()
    selected = selector.select(all_scenes, count=8)
    print(f'      Selected {len(selected)} diverse scenes')

    # Step 3: Hook optimization
    print('\n[3/5] Optimizing for hook...')
    hook_gen = HookGenerator()
    best_hook = hook_gen.select_hook_scene(selected)
    hook_score = hook_gen.score_hook_potential(best_hook)
    print(f'      Best hook: {best_hook.source_file.name} (score: {hook_score:.1f})')

    # Reorder: put hook first, then sequence rest
    other_scenes = [s for s in selected if s != best_hook]
    sequencer = NarrativeSequencer()
    sequenced_rest = sequencer.sequence(other_scenes, target_duration=27.0)

    # Final sequence: hook + rest
    final_sequence = [best_hook] + sequenced_rest
    print(f'      Final sequence: {len(final_sequence)} clips')

    # Step 4: Extract clips with FFmpeg
    print('\n[4/5] Extracting clips...')
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    temp_dir = Path(tempfile.mkdtemp())

    clip_files = []
    for i, scene in enumerate(final_sequence):
        clip_path = temp_dir / f'clip_{i:02d}.mp4'
        duration = min(scene.end_time - scene.start_time, 5.0)  # Max 5s per clip

        cmd = [
            'ffmpeg', '-y', '-hide_banner', '-loglevel', 'error',
            '-ss', str(scene.start_time),
            '-i', str(scene.source_file),
            '-t', str(duration),
            '-vf', 'scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2',
            '-c:v', 'h264_videotoolbox', '-b:v', '8M',
            '-an',
            '-r', '30',
            str(clip_path)
        ]

        print(f'      Clip {i+1}/{len(final_sequence)}: {scene.source_file.name} [{scene.start_time:.1f}s-{scene.start_time+duration:.1f}s]...', end=' ')
        sys.stdout.flush()
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode == 0 and clip_path.exists():
            clip_files.append(clip_path)
            print('OK')
        else:
            print(f'FAILED')

    # Step 5: Concatenate clips
    print('\n[5/5] Creating final reel...')
    concat_file = temp_dir / 'concat.txt'
    with open(concat_file, 'w') as f:
        for clip in clip_files:
            f.write(f"file '{clip}'\n")

    output_path = output_dir / 'instagram_reel.mp4'
    cmd = [
        'ffmpeg', '-y', '-hide_banner', '-loglevel', 'error',
        '-f', 'concat', '-safe', '0',
        '-i', str(concat_file),
        '-c:v', 'h264_videotoolbox', '-b:v', '8M',
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
    print('  SUCCESS! Instagram-worthy reel created')
    print('=' * 60)
    print(f'  Output: {output_path}')
    print(f'  Format: 1080x1920 (9:16 vertical)')
    print(f'  Hook scene: {best_hook.source_file.name} (first clip)')
    print(f'  Clips: {len(clip_files)}')
    print('=' * 60)


if __name__ == '__main__':
    main()
