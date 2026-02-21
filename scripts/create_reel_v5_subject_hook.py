#!/usr/bin/env python3
"""
Create Instagram-Worthy Drone Reel V5 (Subject-Aware Hook)

KEY IMPROVEMENT: Prioritizes scenes with SUBJECTS (whales, boats, people)
over plain textures. The most compelling subject footage becomes the hook.

Based on analysis of source clips:
- DJI_20241029174916_0356_D.mov = WHALES (best hook potential)
- DJI_20241029174007_0351_D.MP4 = BOAT (good subject)
- DJI_20241030011347_0341_D.MP4 = MOUNTAIN LANDSCAPE (scenic variety)
"""

import subprocess
import tempfile
import shutil
from pathlib import Path
from dataclasses import dataclass


@dataclass
class SubjectClip:
    """Clip with subject awareness scoring."""
    source_file: Path
    start_time: float
    end_time: float
    subject_score: float  # Higher = more visible subjects
    narrative_role: str = "build"


def get_video_duration(video_path: Path) -> float:
    """Get video duration using ffprobe."""
    cmd = [
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', str(video_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout.strip()) if result.stdout.strip() else 0


def identify_subject_content(video_path: Path) -> list[tuple[float, float, float]]:
    """
    Identify timestamps with subject content based on filename patterns
    and known content analysis.

    Returns list of (start_time, end_time, subject_score) tuples.
    """
    name = video_path.name.lower()
    duration = get_video_duration(video_path)

    segments = []

    # Known content mapping based on frame analysis
    if '0356' in name or '174916' in name:
        # WHALE FOOTAGE - highest priority for hook
        # Whales visible throughout most of the clip
        if duration > 0:
            # Split into 2.5s segments, all high scoring
            for start in range(0, int(duration), 2):
                end = min(start + 2.5, duration)
                if end - start >= 1.5:
                    segments.append((start, end, 95.0))  # Highest score - whales!

    elif '0351' in name or '174007' in name:
        # BOAT FOOTAGE - good subject
        if duration > 0:
            for start in range(0, int(duration), 2):
                end = min(start + 2.5, duration)
                if end - start >= 1.5:
                    segments.append((start, end, 80.0))  # Good score - boat

    elif '0341' in name or '011347' in name:
        # MOUNTAIN LANDSCAPE - scenic, good for variety
        if duration > 0:
            for start in range(0, int(duration), 3):
                end = min(start + 3.0, duration)
                if end - start >= 1.5:
                    segments.append((start, end, 70.0))  # Scenic score

    elif '0346' in name or '011801' in name:
        # Unknown content - lower priority
        if duration > 0:
            for start in range(0, int(duration), 3):
                end = min(start + 3.0, duration)
                if end - start >= 1.5:
                    segments.append((start, end, 50.0))

    elif '0350' in name or '173912' in name:
        # Ocean footage - lower priority (often just texture)
        if duration > 0:
            for start in range(0, int(duration), 3):
                end = min(start + 3.0, duration)
                if end - start >= 1.5:
                    segments.append((start, end, 40.0))

    else:
        # Default scoring
        if duration > 0:
            for start in range(0, int(duration), 3):
                end = min(start + 3.0, duration)
                if end - start >= 1.5:
                    segments.append((start, end, 45.0))

    return segments


def create_reel_v5(location_text: str = "Sardinia, Italy"):
    """Create V5 reel with subject-aware hook selection."""

    print('=' * 70)
    print('  Creating Instagram-Worthy Drone Reel V5')
    print('  SUBJECT-AWARE HOOK: Prioritizing whales/boats over textures')
    print('=' * 70)

    # Find videos
    print('\n[1/5] Finding videos...')
    video_dir = Path('.drone_clips')
    videos = list(video_dir.glob('*.MP4')) + list(video_dir.glob('*.mp4')) + \
             list(video_dir.glob('*.MOV')) + list(video_dir.glob('*.mov'))
    print(f'      Found {len(videos)} videos')

    # Identify subject content in each video
    print('\n[2/5] Analyzing subject content...')
    all_clips = []

    for video in videos:
        print(f'      {video.name}...', end=' ', flush=True)
        segments = identify_subject_content(video)

        for start, end, score in segments:
            all_clips.append(SubjectClip(
                source_file=video,
                start_time=start,
                end_time=end,
                subject_score=score
            ))

        print(f'{len(segments)} segments (max score: {max(s[2] for s in segments) if segments else 0:.0f})')

    print(f'      Total: {len(all_clips)} potential clips')

    # Sort by subject score and select best clips
    print('\n[3/5] Selecting clips with best subjects...')
    all_clips.sort(key=lambda c: c.subject_score, reverse=True)

    # Select with diversity - don't use too many from same source
    selected = []
    used_sources = {}
    target_count = 10

    for clip in all_clips:
        source = clip.source_file.name
        # Allow more from high-subject clips (whales!)
        max_per_source = 4 if clip.subject_score >= 90 else 3 if clip.subject_score >= 70 else 2

        if used_sources.get(source, 0) < max_per_source:
            selected.append(clip)
            used_sources[source] = used_sources.get(source, 0) + 1
            if len(selected) >= target_count:
                break

    print(f'      Selected {len(selected)} clips')
    print('      Top selections:')
    for i, clip in enumerate(selected[:5]):
        print(f'        {i+1}. {clip.source_file.name} [{clip.start_time:.1f}s] score: {clip.subject_score:.0f}')

    # Apply narrative arc
    print('\n[4/5] Applying narrative arc...')

    # Best subject clip is the hook (should be whales)
    hook = selected[0]
    hook.narrative_role = "hook"

    # Second best is climax
    if len(selected) > 1:
        selected[1].narrative_role = "climax"

    # Last is resolve (use scenic)
    if len(selected) > 2:
        # Find a scenic clip for resolve
        for clip in reversed(selected):
            if clip.subject_score < 80:  # Scenic, not action
                clip.narrative_role = "resolve"
                break
        else:
            selected[-1].narrative_role = "resolve"

    # Reorder: Hook -> Build (ascending energy) -> Climax -> Resolve
    hook_clips = [c for c in selected if c.narrative_role == "hook"]
    climax_clips = [c for c in selected if c.narrative_role == "climax"]
    resolve_clips = [c for c in selected if c.narrative_role == "resolve"]
    build_clips = [c for c in selected if c.narrative_role == "build"]

    # Sort build by ascending score
    build_clips.sort(key=lambda c: c.subject_score)

    sequenced = hook_clips + build_clips + climax_clips + resolve_clips

    print('      Sequence:')
    role_icons = {'hook': '🎯', 'build': '📈', 'climax': '⭐', 'resolve': '🎬'}
    for i, clip in enumerate(sequenced):
        icon = role_icons.get(clip.narrative_role, '•')
        print(f'        {i+1}. {icon} [{clip.narrative_role.upper():8}] {clip.source_file.name} '
              f'[{clip.start_time:.1f}s] (subject: {clip.subject_score:.0f})')

    # Render clips
    print('\n[5/5] Rendering clips with smart crop (no color grading)...')
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    temp_dir = Path(tempfile.mkdtemp())

    clip_files = []
    for i, clip in enumerate(sequenced):
        clip_path = temp_dir / f'clip_{i:02d}.mp4'

        # Speed ramps for hook and climax
        speed = ""
        if clip.narrative_role == "hook":
            speed = "setpts=1.15*PTS,"  # Slight slow-mo for dramatic whale reveal
        elif clip.narrative_role == "climax":
            speed = "setpts=1.2*PTS,"  # More slow-mo for climax

        # Smart crop - NO color grading (natural look)
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

        icon = role_icons.get(clip.narrative_role, '•')
        print(f'      {icon} Clip {i+1}/{len(sequenced)}...', end=' ', flush=True)

        result = subprocess.run(cmd, capture_output=True)
        if result.returncode == 0 and clip_path.exists():
            clip_files.append(clip_path)
            print('OK')
        else:
            print(f'FAILED: {result.stderr.decode()[:100]}')

    # Concatenate clips
    concat_file = temp_dir / 'concat.txt'
    with open(concat_file, 'w') as f:
        for clip in clip_files:
            f.write(f"file '{clip}'\n")

    output_path = output_dir / 'instagram_reel_v5.mp4'

    # Add text overlay
    if location_text:
        video_only = temp_dir / 'video.mp4'
        subprocess.run([
            'ffmpeg', '-y', '-hide_banner', '-loglevel', 'error',
            '-f', 'concat', '-safe', '0', '-i', str(concat_file),
            '-c:v', 'h264_videotoolbox', '-b:v', '12M', '-r', '30',
            str(video_only)
        ], capture_output=True)

        # Text overlay (appears 1-4 seconds)
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
        print('  SUCCESS! Instagram-worthy reel V5 created')
        print('=' * 70)
        print(f'  Output: {output_path}')
        print(f'  Duration: {duration:.1f}s')
        print(f'  Size: {size_mb:.1f} MB')
        print(f'  Clips: {len(clip_files)}')
        if duration > 0 and len(clip_files) > 0:
            print(f'  Avg clip: {duration/len(clip_files):.1f}s')
        print('\n  V5 IMPROVEMENTS:')
        print('    🎯 SUBJECT-AWARE HOOK: Whales/boats prioritized over textures')
        print('    ✅ Smart crop (no letterbox)')
        print('    ✅ NO color grading (natural colors)')
        print('    ✅ Speed ramps (hook/climax slow-mo)')
        print('    ✅ Narrative arc (Hook→Build→Climax→Resolve)')
        print('    ✅ Fade transitions (0.25s)')
        if location_text:
            print(f'    ✅ Location text: "{location_text}"')
        print('=' * 70)

        return output_path

    return None


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--location', '-l', default='Sardinia, Italy', help='Location text')
    args = parser.parse_args()
    create_reel_v5(args.location)
