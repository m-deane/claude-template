# Implementation Plan: `extract-clips` Command

## Overview

This plan adds a new `drone-reel extract-clips` CLI command that detects and extracts the best scenes from raw drone footage as individual .mp4 files. The implementation touches 4 files (2 modified, 2 new).

**Prerequisites**: Read `.claude_plans/clip_extract_codebase_analysis.md` and `.claude_plans/clip_extract_feature_design.md` for full context on the design rationale.

---

## Step 1: Add `write_clip()` to VideoProcessor

**File**: `src/drone_reel/core/video_processor.py`
**Insert after**: The `extract_clip()` method (line 259), before `_extract_clip_parallel()` (line 261).

### Code to add

```python
    def write_clip(
        self,
        clip: VideoFileClip,
        output_path: Path,
    ) -> Path:
        """
        Write a single clip to disk with configured encoding parameters.

        Uses the same BT.709 color space, faststart, and VBV bitrate enforcement
        as the main stitch_clips pipeline.

        Args:
            clip: MoviePy VideoFileClip to write (from extract_clip()).
            output_path: Destination .mp4 file path. Parent directories
                are created automatically.

        Returns:
            The output_path after successful write.

        Raises:
            RuntimeError: If encoding fails.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Build ffmpeg_params — same block as stitch_clips (lines 483-503)
        ffmpeg_params = [
            "-pix_fmt", "yuv420p",
            "-colorspace", "bt709",
            "-color_primaries", "bt709",
            "-color_trc", "bt709",
            "-movflags", "+faststart",
        ]

        # Add maxrate/bufsize for VBV bitrate enforcement
        if self.video_bitrate:
            numeric_str = self.video_bitrate.rstrip("MmKk")
            try:
                numeric_val = float(numeric_str)
                unit = self.video_bitrate[len(numeric_str):].upper()
                maxrate_val = numeric_val * 1.5
                bufsize_val = numeric_val * 2
                maxrate_str = f"{maxrate_val:.0f}{unit}"
                bufsize_str = f"{bufsize_val:.0f}{unit}"
                ffmpeg_params += ["-maxrate", maxrate_str, "-bufsize", bufsize_str]
            except (ValueError, IndexError):
                pass

        try:
            clip.write_videofile(
                str(output_path),
                fps=self.output_fps,
                codec=self.output_codec,
                audio_codec="aac",
                preset=self.preset,
                threads=self.threads,
                bitrate=self.video_bitrate,
                audio_bitrate=self.audio_bitrate,
                ffmpeg_params=ffmpeg_params,
                logger=None,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to write clip to {output_path}: {e}") from e

        return output_path
```

### Why this location

Immediately after `extract_clip()` and before `_extract_clip_parallel()` creates a natural grouping: extract a clip, then write it. The `stitch_clips()` method follows later as the batch orchestrator.

### Why this implementation

- Reuses the exact same FFmpeg params block from `stitch_clips()` (lines 483-503) for encoding consistency (BT.709 color space, yuv420p, faststart, VBV caps).
- Does NOT manage clip lifecycle (no `clip.close()`) — the caller manages extract/write/close, matching the existing `extract_clip()` pattern where the caller closes.
- Wraps `write_videofile` in try/except to give a clear error message on encoding failure.
- Creates parent directories automatically (`mkdir(parents=True)`) so the CLI command doesn't need to pre-create the output dir.

---

## Step 2: Add `extract-clips` CLI Command

**File**: `src/drone_reel/cli.py`
**Insert after**: The `analyze` command (line 1282), before the `beats` command (line 1284).

### Imports to add

No new imports needed at the top of the file. All required imports (`SceneDetector`, `SceneFilter`, `VideoProcessor`, `analyze_scenes_batch`, `find_video_files`, `console`, `Path`, etc.) are already imported. The only new imports are done inline:
- `gc` — imported inline in the extraction loop
- `json` — imported inline when `--json` is used
- `resource_guard.preflight_check` — imported inline

### Code to add

```python
@main.command(name="extract-clips")
@click.option(
    "--input", "-i",
    "input_path",
    type=click.Path(exists=True, path_type=Path),
    required=True,
    help="Video file or directory of videos to extract clips from",
)
@click.option(
    "--output-dir", "-o",
    "output_dir",
    type=click.Path(path_type=Path),
    default="./clips",
    help="Directory for extracted clip files",
)
@click.option(
    "--count", "-n",
    type=click.IntRange(1, 100),
    default=10,
    help="Maximum number of clips to extract (1-100)",
)
@click.option(
    "--min-score",
    type=click.FloatRange(0, 100),
    default=30.0,
    help="Minimum scene score threshold (0-100)",
)
@click.option(
    "--min-duration",
    type=click.FloatRange(0.5, 300),
    default=2.0,
    help="Minimum clip duration in seconds",
)
@click.option(
    "--max-duration",
    type=click.FloatRange(1.0, 300),
    default=10.0,
    help="Maximum clip duration in seconds",
)
@click.option(
    "--quality", "-q",
    type=click.Choice(["low", "medium", "high", "ultra"]),
    default="high",
    help="Output quality (low=5M, medium=10M, high=15M, ultra=25M bitrate)",
)
@click.option(
    "--resolution",
    type=click.Choice(["source", "hd", "2k", "4k"]),
    default="source",
    help="Output resolution (source=keep original)",
)
@click.option(
    "--sort", "-s",
    type=click.Choice(["score", "chronological", "duration"]),
    default="score",
    help="Output ordering / naming order",
)
@click.option(
    "--no-filter",
    is_flag=True,
    default=False,
    help="Skip quality filtering (extract all detected scenes)",
)
@click.option(
    "--enhanced",
    is_flag=True,
    default=False,
    help="Run enhanced analysis (subject detection, hook potential) for better ranking. Slower.",
)
@click.option(
    "--json", "write_json",
    is_flag=True,
    default=False,
    help="Write a sidecar manifest.json with scene metadata",
)
@click.option(
    "--overwrite",
    is_flag=True,
    default=False,
    help="Overwrite existing clips in output directory",
)
def extract_clips(
    input_path,
    output_dir,
    count,
    min_score,
    min_duration,
    max_duration,
    quality,
    resolution,
    sort,
    no_filter,
    enhanced,
    write_json,
    overwrite,
):
    """Extract top scenes from a video file as individual clips."""
    import gc
    import json as json_module

    from drone_reel.utils.file_utils import VIDEO_EXTENSIONS, is_video_file
    from drone_reel.utils.resource_guard import preflight_check
    from drone_reel.core.video_processor import ClipSegment

    # --- Validate parameters ---
    if min_duration >= max_duration:
        console.print(
            f"[red]Error:[/red] --min-duration ({min_duration}s) must be less than "
            f"--max-duration ({max_duration}s)"
        )
        raise SystemExit(1)

    # --- Find video files ---
    if input_path.is_file():
        if not is_video_file(input_path):
            formats = ", ".join(sorted(VIDEO_EXTENSIONS))
            console.print(f"[red]Error:[/red] Not a supported video file: {input_path.name}")
            console.print(f"[dim]Supported formats: {formats}[/dim]")
            raise SystemExit(1)
        video_files = [input_path]
    else:
        video_files = find_video_files(input_path)

    if not video_files:
        formats = ", ".join(sorted(VIDEO_EXTENSIONS))
        console.print(f"[red]Error:[/red] No video files found in input path")
        console.print(f"[dim]Supported formats: {formats}[/dim]")
        raise SystemExit(1)

    # --- Verify output directory is writable ---
    output_dir = Path(output_dir)
    if not output_dir.exists():
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            console.print(f"[red]Error:[/red] Cannot create output directory: {e}")
            raise SystemExit(1)
    elif not os.access(output_dir, os.W_OK):
        console.print(f"[red]Error:[/red] Output directory is not writable: {output_dir}")
        raise SystemExit(1)

    # --- Quality and resolution presets ---
    quality_presets = {
        "low": ("5M", "128k"),
        "medium": ("10M", "192k"),
        "high": ("15M", "192k"),
        "ultra": ("25M", "320k"),
    }
    video_bitrate, audio_bitrate = quality_presets.get(quality, ("15M", "192k"))

    resolution_heights = {"hd": 1080, "2k": 1440, "4k": 2160}
    resolution_height = resolution_heights.get(resolution, 1080)

    # Scale bitrate for higher resolutions
    if resolution == "4k":
        bitrate_map = {"low": "15M", "medium": "25M", "high": "40M", "ultra": "80M"}
        video_bitrate = bitrate_map.get(quality, "40M")
    elif resolution == "2k":
        bitrate_map = {"low": "8M", "medium": "15M", "high": "25M", "ultra": "45M"}
        video_bitrate = bitrate_map.get(quality, "25M")

    # --- Resource preflight check ---
    issues = preflight_check(
        output_path=output_dir / "clip_001.mp4",
        resolution_height=resolution_height,
        fps=30,
        clip_count=count,
        stabilize=False,
        video_bitrate=video_bitrate,
        duration=count * 5.0,
    )

    for issue in issues:
        level = issue["level"]
        msg = issue["message"]
        if level == "error":
            console.print(f"[red]Error:[/red] {msg}")
        else:
            console.print(f"[yellow]Warning:[/yellow] {msg}")

    if any(issue["level"] == "error" for issue in issues):
        raise SystemExit(1)

    # --- Header ---
    file_label = input_path.name if input_path.is_file() else f"{len(video_files)} files"
    console.print(Panel.fit(
        f"[bold blue]Clip Extractor[/bold blue]\n"
        f"Source: {file_label} | Top {count} clips | {quality} quality",
        border_style="blue",
    ))

    # --- Scene detection ---
    scene_detector = SceneDetector()
    all_scenes = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Detecting scenes...", total=len(video_files))

        for video_path in video_files:
            try:
                if enhanced:
                    scenes = scene_detector.detect_scenes_enhanced(video_path)
                else:
                    scenes = scene_detector.detect_scenes(video_path)
                all_scenes.extend(scenes)
            except Exception as e:
                console.print(
                    f"  [yellow]Warning:[/yellow] Skipping {video_path.name}: {e}"
                )
            progress.advance(task)

    if not all_scenes:
        console.print(
            "\n[yellow]Warning:[/yellow] Detected 0 scenes."
        )
        console.print(
            "[dim]Tip: The video may have no distinct scene changes. "
            "Try a lower scene threshold or use a video editing tool "
            "to manually mark segments.[/dim]"
        )
        raise SystemExit(1)

    console.print(f"  Detected {len(all_scenes)} scenes")

    # --- Motion analysis (for filtering) ---
    analysis = analyze_scenes_batch(all_scenes, include_sharpness=True)

    motion_map = {id(s): analysis[id(s)]["motion_energy"] for s in all_scenes}
    brightness_map = {id(s): analysis[id(s)]["brightness"] for s in all_scenes}
    shake_map = {id(s): analysis[id(s)]["shake_score"] for s in all_scenes}

    # --- Filtering ---
    if no_filter:
        candidates = list(all_scenes)
        scenes_filtered = 0
        dark_filtered = 0
        shaky_filtered = 0
    else:
        sf = SceneFilter()
        result = sf.filter_scenes(all_scenes, motion_map, brightness_map, shake_map)
        candidates = result.all_passing
        scenes_filtered = result.dark_scenes_filtered + result.shaky_scenes_filtered
        dark_filtered = result.dark_scenes_filtered
        shaky_filtered = result.shaky_scenes_filtered

    # --- Apply min-score threshold ---
    candidates = [s for s in candidates if s.score >= min_score]

    # --- Apply duration constraints ---
    candidates = [s for s in candidates if s.duration >= min_duration]

    duration_too_short = len(all_scenes) - len(candidates) - scenes_filtered

    # --- Report filtering ---
    filter_details = []
    if dark_filtered > 0:
        filter_details.append(f"{dark_filtered} too dark")
    if shaky_filtered > 0:
        filter_details.append(f"{shaky_filtered} too shaky")
    if duration_too_short > 0:
        filter_details.append(f"{duration_too_short} too short/low score")

    if filter_details:
        console.print(
            f"  Passed filter: {len(candidates)} scenes "
            f"({sum([dark_filtered, shaky_filtered, duration_too_short])} filtered: "
            f"{', '.join(filter_details)})"
        )
    else:
        console.print(f"  Passed filter: {len(candidates)} scenes")

    # --- Check for empty candidates ---
    if not candidates:
        console.print(
            f"\n[yellow]Warning:[/yellow] No scenes passed quality filters."
        )
        console.print(
            f"[dim]Tip: Try --no-filter to extract all scenes, "
            f"or lower --min-score (currently {min_score})[/dim]"
        )
        raise SystemExit(1)

    # --- Sort ---
    if sort == "score":
        candidates.sort(key=lambda s: s.score, reverse=True)
    elif sort == "chronological":
        candidates.sort(key=lambda s: (str(s.source_file), s.start_time))
    elif sort == "duration":
        candidates.sort(key=lambda s: s.duration, reverse=True)

    # --- Limit to count ---
    selected = candidates[:count]

    # --- Extract and write clips ---
    processor = VideoProcessor(
        output_fps=30,
        video_bitrate=video_bitrate,
        audio_bitrate=audio_bitrate,
    )

    extracted_count = 0
    skipped_count = 0
    failed_count = 0
    total_duration = 0.0
    total_size_bytes = 0
    manifest_clips = []

    console.print()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Extracting clips...", total=len(selected))

        for i, scene in enumerate(selected):
            clip_duration = min(scene.duration, max_duration)
            score_int = int(scene.score)
            filename = f"clip_{i + 1:03d}_s{score_int}.mp4"
            output_file = output_dir / filename

            # Check for existing file
            if output_file.exists() and not overwrite:
                console.print(
                    f"  [yellow]Skipping[/yellow] {filename} (already exists)"
                )
                skipped_count += 1
                progress.advance(task)
                continue

            segment = ClipSegment(
                scene=scene,
                start_offset=0.0,
                duration=clip_duration,
            )

            clip = None
            try:
                clip = processor.extract_clip(segment)

                # Resize if resolution is not 'source'
                if resolution != "source":
                    target_height = resolution_heights[resolution]
                    # Calculate width maintaining aspect ratio
                    aspect = clip.w / clip.h
                    target_width = int(target_height * aspect)
                    # Ensure even dimensions for codec compatibility
                    target_width = target_width + (target_width % 2)
                    target_height = target_height + (target_height % 2)
                    clip = clip.resized((target_width, target_height))

                processor.write_clip(clip, output_file)

                file_size = output_file.stat().st_size
                total_size_bytes += file_size
                total_duration += clip_duration
                extracted_count += 1

                console.print(
                    f"  {i + 1:>3}/{len(selected)}  {filename}   "
                    f"{format_duration(scene.start_time)}-{format_duration(scene.end_time)}  "
                    f"{clip_duration:.1f}s  score: {score_int}"
                )

                # Build manifest entry
                manifest_entry = {
                    "filename": filename,
                    "source_file": str(scene.source_file.name),
                    "start_time": round(scene.start_time, 2),
                    "end_time": round(scene.end_time, 2),
                    "duration": round(clip_duration, 2),
                    "score": round(scene.score, 1),
                }
                # Add enhanced fields if available
                if hasattr(scene, "motion_energy"):
                    manifest_entry["motion_energy"] = round(scene.motion_energy, 1)
                if hasattr(scene, "motion_type"):
                    manifest_entry["motion_type"] = scene.motion_type.name
                if hasattr(scene, "hook_tier"):
                    manifest_entry["hook_tier"] = scene.hook_tier.name
                if hasattr(scene, "is_golden_hour"):
                    manifest_entry["is_golden_hour"] = scene.is_golden_hour
                manifest_clips.append(manifest_entry)

            except Exception as e:
                console.print(
                    f"  [red]Failed[/red] {filename}: {e}"
                )
                failed_count += 1
            finally:
                if clip is not None:
                    try:
                        if hasattr(clip, '_source_clip_ref') and clip._source_clip_ref:
                            clip._source_clip_ref.close()
                        clip.close()
                    except Exception:
                        pass
                gc.collect()

            progress.advance(task)

    # --- Summary ---
    total_size_mb = total_size_bytes / (1024 * 1024)

    if extracted_count == 0 and skipped_count > 0:
        console.print(
            f"\n  All {skipped_count} clips already exist in {output_dir}/"
        )
        console.print("  Use --overwrite to replace existing files.")
    elif failed_count > 0:
        console.print(
            f"\n  Extracted {extracted_count} of {len(selected)} clips "
            f"({failed_count} failed). Check disk space."
        )
    else:
        console.print(
            f"\n  Extracted {extracted_count} clips to {output_dir}/ "
            f"(total: {total_duration:.1f}s, {total_size_mb:.1f} MB)"
        )

    # --- Write JSON manifest ---
    if write_json and manifest_clips:
        manifest = {
            "version": 1,
            "source_files": [
                {
                    "path": str(vf.resolve()),
                    "name": vf.name,
                }
                for vf in video_files
            ],
            "extraction_params": {
                "count": count,
                "min_score": min_score,
                "min_duration": min_duration,
                "max_duration": max_duration,
                "quality": quality,
                "resolution": resolution,
                "sort": sort,
                "enhanced": enhanced,
                "filtered": not no_filter,
            },
            "clips": manifest_clips,
            "summary": {
                "total_clips": extracted_count,
                "total_duration": round(total_duration, 1),
                "total_size_mb": round(total_size_mb, 1),
                "avg_score": round(
                    sum(c["score"] for c in manifest_clips) / len(manifest_clips), 1
                ) if manifest_clips else 0,
                "scenes_detected": len(all_scenes),
                "scenes_filtered": scenes_filtered,
            },
        }

        manifest_path = output_dir / "manifest.json"
        with open(manifest_path, "w") as f:
            json_module.dump(manifest, f, indent=2)
        console.print(f"  Manifest written to {manifest_path}")
```

### Why this location

After `analyze` and before `beats` — the extraction command is a natural companion to `analyze`. It uses the same scene detection pipeline but goes further by writing clips to disk.

### What this does

1. Validates params (min < max duration, input exists, output writable)
2. Runs resource preflight check
3. Detects scenes (basic or `--enhanced`)
4. Runs motion analysis batch for filtering
5. Filters (unless `--no-filter`), applies min-score and min-duration
6. Sorts by the chosen order, limits to `--count`
7. Extracts each clip sequentially with proper cleanup (close clip + gc.collect)
8. Reports progress and summary
9. Optionally writes manifest.json

---

## Step 3: Write Tests for `write_clip()`

**File**: `tests/test_video_processor.py` (add to existing file)
**Insert after**: The last test in the file.

### Test code to add

```python
class TestWriteClip:
    """Tests for VideoProcessor.write_clip() method."""

    @pytest.fixture
    def processor(self):
        """Create a VideoProcessor with test settings."""
        with patch.object(VideoProcessor, '_detect_best_encoder', return_value='libx264'):
            return VideoProcessor(
                output_fps=30,
                video_bitrate="5M",
                audio_bitrate="128k",
            )

    def test_write_clip_creates_output_file(self, processor, tmp_path):
        """Test that write_clip creates the output file."""
        # Create a minimal synthetic clip
        mock_clip = MagicMock()
        mock_clip.duration = 2.0
        mock_clip.fps = 30

        output_path = tmp_path / "test_clip.mp4"
        mock_clip.write_videofile = MagicMock()

        result = processor.write_clip(mock_clip, output_path)

        assert result == output_path
        mock_clip.write_videofile.assert_called_once()

    def test_write_clip_creates_parent_directories(self, processor, tmp_path):
        """Test that write_clip creates parent directories if missing."""
        mock_clip = MagicMock()
        mock_clip.write_videofile = MagicMock()

        output_path = tmp_path / "sub" / "dir" / "clip.mp4"
        processor.write_clip(mock_clip, output_path)

        assert output_path.parent.exists()

    def test_write_clip_uses_bt709_colorspace(self, processor, tmp_path):
        """Test that write_clip includes BT.709 color space params."""
        mock_clip = MagicMock()
        mock_clip.write_videofile = MagicMock()

        output_path = tmp_path / "clip.mp4"
        processor.write_clip(mock_clip, output_path)

        call_kwargs = mock_clip.write_videofile.call_args
        ffmpeg_params = call_kwargs.kwargs.get("ffmpeg_params", [])
        assert "-colorspace" in ffmpeg_params
        assert "bt709" in ffmpeg_params

    def test_write_clip_uses_faststart(self, processor, tmp_path):
        """Test that write_clip includes faststart for streaming."""
        mock_clip = MagicMock()
        mock_clip.write_videofile = MagicMock()

        output_path = tmp_path / "clip.mp4"
        processor.write_clip(mock_clip, output_path)

        call_kwargs = mock_clip.write_videofile.call_args
        ffmpeg_params = call_kwargs.kwargs.get("ffmpeg_params", [])
        assert "+faststart" in ffmpeg_params

    def test_write_clip_uses_aac_audio(self, processor, tmp_path):
        """Test that write_clip uses AAC audio codec."""
        mock_clip = MagicMock()
        mock_clip.write_videofile = MagicMock()

        output_path = tmp_path / "clip.mp4"
        processor.write_clip(mock_clip, output_path)

        call_kwargs = mock_clip.write_videofile.call_args
        assert call_kwargs.kwargs.get("audio_codec") == "aac"

    def test_write_clip_uses_configured_bitrate(self, processor, tmp_path):
        """Test that write_clip uses the configured bitrate."""
        mock_clip = MagicMock()
        mock_clip.write_videofile = MagicMock()

        output_path = tmp_path / "clip.mp4"
        processor.write_clip(mock_clip, output_path)

        call_kwargs = mock_clip.write_videofile.call_args
        assert call_kwargs.kwargs.get("bitrate") == "5M"

    def test_write_clip_includes_vbv_caps(self, processor, tmp_path):
        """Test that write_clip adds maxrate/bufsize VBV params."""
        mock_clip = MagicMock()
        mock_clip.write_videofile = MagicMock()

        output_path = tmp_path / "clip.mp4"
        processor.write_clip(mock_clip, output_path)

        call_kwargs = mock_clip.write_videofile.call_args
        ffmpeg_params = call_kwargs.kwargs.get("ffmpeg_params", [])
        assert "-maxrate" in ffmpeg_params
        assert "-bufsize" in ffmpeg_params

    def test_write_clip_raises_on_encoding_failure(self, processor, tmp_path):
        """Test that write_clip wraps encoding errors in RuntimeError."""
        mock_clip = MagicMock()
        mock_clip.write_videofile.side_effect = Exception("FFmpeg error")

        output_path = tmp_path / "clip.mp4"
        with pytest.raises(RuntimeError, match="Failed to write clip"):
            processor.write_clip(mock_clip, output_path)

    def test_write_clip_uses_configured_fps(self, processor, tmp_path):
        """Test that write_clip uses the processor's configured FPS."""
        mock_clip = MagicMock()
        mock_clip.write_videofile = MagicMock()

        output_path = tmp_path / "clip.mp4"
        processor.write_clip(mock_clip, output_path)

        call_kwargs = mock_clip.write_videofile.call_args
        assert call_kwargs.kwargs.get("fps") == 30

    def test_write_clip_does_not_close_clip(self, processor, tmp_path):
        """Test that write_clip does NOT close the clip (caller responsibility)."""
        mock_clip = MagicMock()
        mock_clip.write_videofile = MagicMock()

        output_path = tmp_path / "clip.mp4"
        processor.write_clip(mock_clip, output_path)

        mock_clip.close.assert_not_called()
```

---

## Step 4: Write CLI Integration Tests

**File**: `tests/test_extract_clips.py` (new file)

### Complete test file

```python
"""Tests for the extract-clips CLI command."""

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch, PropertyMock

import numpy as np
import pytest
from click.testing import CliRunner

from drone_reel.cli import main
from drone_reel.core.scene_detector import EnhancedSceneInfo, SceneInfo, MotionType, HookPotential


def _make_scene(
    start=0.0, end=5.0, score=70.0, source_file=None, enhanced=False
):
    """Helper to create a SceneInfo or EnhancedSceneInfo for tests."""
    if source_file is None:
        source_file = Path("/tmp/test_video.mp4")

    if enhanced:
        return EnhancedSceneInfo(
            start_time=start,
            end_time=end,
            duration=end - start,
            score=score,
            source_file=source_file,
            motion_energy=50.0,
            motion_type=MotionType.PAN_RIGHT,
            motion_direction=(0.5, 0.0),
            motion_smoothness=80.0,
            color_variance=60.0,
            hook_potential=score,
            hook_tier=HookPotential.HIGH if score >= 65 else HookPotential.MEDIUM,
            subject_score=45.0,
            is_golden_hour=False,
            dominant_colors=[(100, 150, 200)],
            visual_interest_density=0.5,
            depth_score=60.0,
        )
    else:
        return SceneInfo(
            start_time=start,
            end_time=end,
            duration=end - start,
            score=score,
            source_file=source_file,
        )


def _make_analysis_result(scenes):
    """Helper to build analysis results dict keyed by id(scene)."""
    result = {}
    for s in scenes:
        result[id(s)] = {
            "motion_energy": getattr(s, "motion_energy", 50.0),
            "brightness": 127.0,
            "shake_score": 10.0,
            "motion_type": getattr(s, "motion_type", MotionType.STATIC),
            "motion_direction": getattr(s, "motion_direction", (0.0, 0.0)),
            "sharpness": 50.0,
        }
    return result


class TestExtractClipsValidation:
    """Tests for parameter validation in extract-clips command."""

    def test_min_duration_gte_max_duration_fails(self):
        """Test error when --min-duration >= --max-duration."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            # Create a dummy video file
            Path("video.mp4").touch()
            result = runner.invoke(
                main,
                ["extract-clips", "-i", "video.mp4", "--min-duration", "10", "--max-duration", "5"],
            )
            assert result.exit_code != 0
            assert "must be less than" in result.output

    def test_min_duration_equal_max_duration_fails(self):
        """Test error when --min-duration == --max-duration."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            Path("video.mp4").touch()
            result = runner.invoke(
                main,
                ["extract-clips", "-i", "video.mp4", "--min-duration", "5", "--max-duration", "5"],
            )
            assert result.exit_code != 0
            assert "must be less than" in result.output

    def test_nonexistent_input_fails(self):
        """Test error when input path doesn't exist."""
        runner = CliRunner()
        result = runner.invoke(
            main,
            ["extract-clips", "-i", "/nonexistent/path.mp4"],
        )
        assert result.exit_code != 0

    def test_unsupported_file_extension_fails(self):
        """Test error when input file has unsupported extension."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            Path("video.txt").touch()
            result = runner.invoke(
                main,
                ["extract-clips", "-i", "video.txt"],
            )
            assert result.exit_code != 0
            assert "Not a supported video file" in result.output


class TestExtractClipsSceneDetection:
    """Tests for scene detection flow in extract-clips."""

    @patch("drone_reel.cli.analyze_scenes_batch")
    @patch("drone_reel.cli.SceneDetector")
    @patch("drone_reel.utils.resource_guard.check_available_memory_mb", return_value=float("inf"))
    @patch("drone_reel.utils.resource_guard.check_disk_space_mb", return_value=float("inf"))
    def test_zero_scenes_detected(self, mock_disk, mock_mem, mock_detector_cls, mock_analyze):
        """Test handling when zero scenes are detected."""
        mock_detector = MagicMock()
        mock_detector.detect_scenes.return_value = []
        mock_detector_cls.return_value = mock_detector

        runner = CliRunner()
        with runner.isolated_filesystem():
            Path("video.mp4").touch()
            result = runner.invoke(main, ["extract-clips", "-i", "video.mp4"])

        assert result.exit_code != 0
        assert "0 scenes" in result.output

    @patch("drone_reel.cli.analyze_scenes_batch")
    @patch("drone_reel.cli.SceneDetector")
    @patch("drone_reel.utils.resource_guard.check_available_memory_mb", return_value=float("inf"))
    @patch("drone_reel.utils.resource_guard.check_disk_space_mb", return_value=float("inf"))
    def test_all_scenes_filtered_out(self, mock_disk, mock_mem, mock_detector_cls, mock_analyze):
        """Test handling when all scenes are filtered out by min-score."""
        scenes = [_make_scene(score=20.0)]
        mock_detector = MagicMock()
        mock_detector.detect_scenes.return_value = scenes
        mock_detector_cls.return_value = mock_detector
        mock_analyze.return_value = _make_analysis_result(scenes)

        runner = CliRunner()
        with runner.isolated_filesystem():
            Path("video.mp4").touch()
            result = runner.invoke(
                main,
                ["extract-clips", "-i", "video.mp4", "--min-score", "90"],
            )

        assert result.exit_code != 0
        assert "No scenes passed" in result.output

    @patch("drone_reel.cli.analyze_scenes_batch")
    @patch("drone_reel.cli.SceneDetector")
    @patch("drone_reel.utils.resource_guard.check_available_memory_mb", return_value=float("inf"))
    @patch("drone_reel.utils.resource_guard.check_disk_space_mb", return_value=float("inf"))
    def test_corrupted_video_skipped_in_directory(
        self, mock_disk, mock_mem, mock_detector_cls, mock_analyze
    ):
        """Test that corrupted videos in a directory are skipped with warning."""
        mock_detector = MagicMock()

        def detect_side_effect(path):
            if "bad" in str(path):
                raise Exception("Corrupted file")
            return [_make_scene(source_file=path)]

        mock_detector.detect_scenes.side_effect = detect_side_effect
        mock_detector_cls.return_value = mock_detector

        runner = CliRunner()
        with runner.isolated_filesystem():
            Path("good.mp4").touch()
            Path("bad.mp4").touch()
            # Need to patch find_video_files to return these
            with patch("drone_reel.cli.find_video_files") as mock_find:
                mock_find.return_value = [Path("good.mp4"), Path("bad.mp4")]
                good_scenes = [_make_scene(source_file=Path("good.mp4"))]
                mock_analyze.return_value = _make_analysis_result(good_scenes)

                # Also need to patch VideoProcessor to avoid real encoding
                with patch("drone_reel.cli.VideoProcessor") as mock_vp_cls:
                    mock_processor = MagicMock()
                    mock_clip = MagicMock()
                    mock_clip.w = 1920
                    mock_clip.h = 1080
                    mock_clip.duration = 5.0
                    mock_processor.extract_clip.return_value = mock_clip
                    mock_processor.write_clip.return_value = Path("clips/clip_001_s70.mp4")
                    mock_vp_cls.return_value = mock_processor

                    result = runner.invoke(
                        main,
                        ["extract-clips", "-i", ".", "-o", "clips"],
                    )

        assert "Skipping" in result.output or "Warning" in result.output


class TestExtractClipsOutput:
    """Tests for clip output behavior."""

    @patch("drone_reel.cli.analyze_scenes_batch")
    @patch("drone_reel.cli.SceneDetector")
    @patch("drone_reel.cli.VideoProcessor")
    @patch("drone_reel.utils.resource_guard.check_available_memory_mb", return_value=float("inf"))
    @patch("drone_reel.utils.resource_guard.check_disk_space_mb", return_value=float("inf"))
    def test_clips_named_with_score(
        self, mock_disk, mock_mem, mock_vp_cls, mock_detector_cls, mock_analyze
    ):
        """Test that output files are named clip_NNN_sSCORE.mp4."""
        scenes = [
            _make_scene(start=0, end=5, score=85.0),
            _make_scene(start=10, end=15, score=72.0),
        ]
        mock_detector = MagicMock()
        mock_detector.detect_scenes.return_value = scenes
        mock_detector_cls.return_value = mock_detector
        mock_analyze.return_value = _make_analysis_result(scenes)

        mock_processor = MagicMock()
        mock_clip = MagicMock()
        mock_clip.w = 1920
        mock_clip.h = 1080
        mock_clip.duration = 5.0
        mock_processor.extract_clip.return_value = mock_clip

        # Make write_clip create the file so stat() works
        def write_side_effect(clip, path):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"\x00" * 1000)
            return path

        mock_processor.write_clip.side_effect = write_side_effect
        mock_vp_cls.return_value = mock_processor

        runner = CliRunner()
        with runner.isolated_filesystem():
            Path("video.mp4").touch()
            result = runner.invoke(
                main,
                ["extract-clips", "-i", "video.mp4", "-o", "out", "-n", "2"],
            )

        # Check that write_clip was called with correctly named paths
        calls = mock_processor.write_clip.call_args_list
        assert len(calls) == 2
        assert "clip_001_s85" in str(calls[0])
        assert "clip_002_s72" in str(calls[1])

    @patch("drone_reel.cli.analyze_scenes_batch")
    @patch("drone_reel.cli.SceneDetector")
    @patch("drone_reel.cli.VideoProcessor")
    @patch("drone_reel.utils.resource_guard.check_available_memory_mb", return_value=float("inf"))
    @patch("drone_reel.utils.resource_guard.check_disk_space_mb", return_value=float("inf"))
    def test_count_limits_output(
        self, mock_disk, mock_mem, mock_vp_cls, mock_detector_cls, mock_analyze
    ):
        """Test that --count limits the number of extracted clips."""
        scenes = [
            _make_scene(start=i * 5, end=(i + 1) * 5, score=90 - i * 5)
            for i in range(10)
        ]
        mock_detector = MagicMock()
        mock_detector.detect_scenes.return_value = scenes
        mock_detector_cls.return_value = mock_detector
        mock_analyze.return_value = _make_analysis_result(scenes)

        mock_processor = MagicMock()
        mock_clip = MagicMock()
        mock_clip.w = 1920
        mock_clip.h = 1080
        mock_clip.duration = 5.0
        mock_processor.extract_clip.return_value = mock_clip

        def write_side_effect(clip, path):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"\x00" * 1000)
            return path

        mock_processor.write_clip.side_effect = write_side_effect
        mock_vp_cls.return_value = mock_processor

        runner = CliRunner()
        with runner.isolated_filesystem():
            Path("video.mp4").touch()
            result = runner.invoke(
                main,
                ["extract-clips", "-i", "video.mp4", "-n", "3"],
            )

        assert mock_processor.write_clip.call_count == 3

    @patch("drone_reel.cli.analyze_scenes_batch")
    @patch("drone_reel.cli.SceneDetector")
    @patch("drone_reel.cli.VideoProcessor")
    @patch("drone_reel.utils.resource_guard.check_available_memory_mb", return_value=float("inf"))
    @patch("drone_reel.utils.resource_guard.check_disk_space_mb", return_value=float("inf"))
    def test_existing_files_skipped_without_overwrite(
        self, mock_disk, mock_mem, mock_vp_cls, mock_detector_cls, mock_analyze
    ):
        """Test that existing clips are skipped without --overwrite."""
        scenes = [_make_scene(score=80.0)]
        mock_detector = MagicMock()
        mock_detector.detect_scenes.return_value = scenes
        mock_detector_cls.return_value = mock_detector
        mock_analyze.return_value = _make_analysis_result(scenes)

        mock_processor = MagicMock()
        mock_vp_cls.return_value = mock_processor

        runner = CliRunner()
        with runner.isolated_filesystem():
            Path("video.mp4").touch()
            out_dir = Path("clips")
            out_dir.mkdir()
            (out_dir / "clip_001_s80.mp4").write_bytes(b"\x00" * 100)

            result = runner.invoke(
                main,
                ["extract-clips", "-i", "video.mp4", "-o", "clips", "-n", "1"],
            )

        assert "Skipping" in result.output
        mock_processor.extract_clip.assert_not_called()

    @patch("drone_reel.cli.analyze_scenes_batch")
    @patch("drone_reel.cli.SceneDetector")
    @patch("drone_reel.cli.VideoProcessor")
    @patch("drone_reel.utils.resource_guard.check_available_memory_mb", return_value=float("inf"))
    @patch("drone_reel.utils.resource_guard.check_disk_space_mb", return_value=float("inf"))
    def test_overwrite_replaces_existing(
        self, mock_disk, mock_mem, mock_vp_cls, mock_detector_cls, mock_analyze
    ):
        """Test that --overwrite replaces existing clips."""
        scenes = [_make_scene(score=80.0)]
        mock_detector = MagicMock()
        mock_detector.detect_scenes.return_value = scenes
        mock_detector_cls.return_value = mock_detector
        mock_analyze.return_value = _make_analysis_result(scenes)

        mock_processor = MagicMock()
        mock_clip = MagicMock()
        mock_clip.w = 1920
        mock_clip.h = 1080
        mock_clip.duration = 5.0
        mock_processor.extract_clip.return_value = mock_clip

        def write_side_effect(clip, path):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"\x00" * 2000)
            return path

        mock_processor.write_clip.side_effect = write_side_effect
        mock_vp_cls.return_value = mock_processor

        runner = CliRunner()
        with runner.isolated_filesystem():
            Path("video.mp4").touch()
            out_dir = Path("clips")
            out_dir.mkdir()
            (out_dir / "clip_001_s80.mp4").write_bytes(b"\x00" * 100)

            result = runner.invoke(
                main,
                ["extract-clips", "-i", "video.mp4", "-o", "clips", "-n", "1", "--overwrite"],
            )

        mock_processor.extract_clip.assert_called_once()


class TestExtractClipsSorting:
    """Tests for clip sorting behavior."""

    @patch("drone_reel.cli.analyze_scenes_batch")
    @patch("drone_reel.cli.SceneDetector")
    @patch("drone_reel.cli.VideoProcessor")
    @patch("drone_reel.utils.resource_guard.check_available_memory_mb", return_value=float("inf"))
    @patch("drone_reel.utils.resource_guard.check_disk_space_mb", return_value=float("inf"))
    def test_sort_by_score_default(
        self, mock_disk, mock_mem, mock_vp_cls, mock_detector_cls, mock_analyze
    ):
        """Test that clips are sorted by score by default (best first)."""
        scenes = [
            _make_scene(start=0, end=5, score=60.0),
            _make_scene(start=10, end=15, score=90.0),
            _make_scene(start=20, end=25, score=75.0),
        ]
        mock_detector = MagicMock()
        mock_detector.detect_scenes.return_value = scenes
        mock_detector_cls.return_value = mock_detector
        mock_analyze.return_value = _make_analysis_result(scenes)

        mock_processor = MagicMock()
        mock_clip = MagicMock()
        mock_clip.w = 1920
        mock_clip.h = 1080
        mock_clip.duration = 5.0
        mock_processor.extract_clip.return_value = mock_clip

        def write_side_effect(clip, path):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"\x00" * 1000)
            return path

        mock_processor.write_clip.side_effect = write_side_effect
        mock_vp_cls.return_value = mock_processor

        runner = CliRunner()
        with runner.isolated_filesystem():
            Path("video.mp4").touch()
            result = runner.invoke(
                main,
                ["extract-clips", "-i", "video.mp4", "-n", "3"],
            )

        calls = mock_processor.write_clip.call_args_list
        filenames = [str(c[0][1]) for c in calls]
        # Best score (90) should be clip_001
        assert "clip_001_s90" in filenames[0]
        assert "clip_002_s75" in filenames[1]
        assert "clip_003_s60" in filenames[2]


class TestExtractClipsJsonManifest:
    """Tests for JSON manifest output."""

    @patch("drone_reel.cli.analyze_scenes_batch")
    @patch("drone_reel.cli.SceneDetector")
    @patch("drone_reel.cli.VideoProcessor")
    @patch("drone_reel.utils.resource_guard.check_available_memory_mb", return_value=float("inf"))
    @patch("drone_reel.utils.resource_guard.check_disk_space_mb", return_value=float("inf"))
    def test_json_manifest_written(
        self, mock_disk, mock_mem, mock_vp_cls, mock_detector_cls, mock_analyze
    ):
        """Test that --json writes a manifest.json file."""
        scenes = [_make_scene(score=80.0)]
        mock_detector = MagicMock()
        mock_detector.detect_scenes.return_value = scenes
        mock_detector_cls.return_value = mock_detector
        mock_analyze.return_value = _make_analysis_result(scenes)

        mock_processor = MagicMock()
        mock_clip = MagicMock()
        mock_clip.w = 1920
        mock_clip.h = 1080
        mock_clip.duration = 5.0
        mock_processor.extract_clip.return_value = mock_clip

        def write_side_effect(clip, path):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"\x00" * 1000)
            return path

        mock_processor.write_clip.side_effect = write_side_effect
        mock_vp_cls.return_value = mock_processor

        runner = CliRunner()
        with runner.isolated_filesystem():
            Path("video.mp4").touch()
            result = runner.invoke(
                main,
                ["extract-clips", "-i", "video.mp4", "-o", "clips", "--json", "-n", "1"],
            )

            manifest_path = Path("clips") / "manifest.json"
            assert manifest_path.exists()

            with open(manifest_path) as f:
                manifest = json.load(f)

            assert manifest["version"] == 1
            assert len(manifest["clips"]) == 1
            assert manifest["clips"][0]["score"] == 80.0
            assert manifest["summary"]["total_clips"] == 1

    @patch("drone_reel.cli.analyze_scenes_batch")
    @patch("drone_reel.cli.SceneDetector")
    @patch("drone_reel.cli.VideoProcessor")
    @patch("drone_reel.utils.resource_guard.check_available_memory_mb", return_value=float("inf"))
    @patch("drone_reel.utils.resource_guard.check_disk_space_mb", return_value=float("inf"))
    def test_no_json_by_default(
        self, mock_disk, mock_mem, mock_vp_cls, mock_detector_cls, mock_analyze
    ):
        """Test that manifest.json is NOT written without --json flag."""
        scenes = [_make_scene(score=80.0)]
        mock_detector = MagicMock()
        mock_detector.detect_scenes.return_value = scenes
        mock_detector_cls.return_value = mock_detector
        mock_analyze.return_value = _make_analysis_result(scenes)

        mock_processor = MagicMock()
        mock_clip = MagicMock()
        mock_clip.w = 1920
        mock_clip.h = 1080
        mock_clip.duration = 5.0
        mock_processor.extract_clip.return_value = mock_clip

        def write_side_effect(clip, path):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"\x00" * 1000)
            return path

        mock_processor.write_clip.side_effect = write_side_effect
        mock_vp_cls.return_value = mock_processor

        runner = CliRunner()
        with runner.isolated_filesystem():
            Path("video.mp4").touch()
            result = runner.invoke(
                main,
                ["extract-clips", "-i", "video.mp4", "-o", "clips", "-n", "1"],
            )

            manifest_path = Path("clips") / "manifest.json"
            assert not manifest_path.exists()


class TestExtractClipsNoFilter:
    """Tests for --no-filter behavior."""

    @patch("drone_reel.cli.analyze_scenes_batch")
    @patch("drone_reel.cli.SceneDetector")
    @patch("drone_reel.cli.VideoProcessor")
    @patch("drone_reel.utils.resource_guard.check_available_memory_mb", return_value=float("inf"))
    @patch("drone_reel.utils.resource_guard.check_disk_space_mb", return_value=float("inf"))
    def test_no_filter_includes_all_scenes(
        self, mock_disk, mock_mem, mock_vp_cls, mock_detector_cls, mock_analyze
    ):
        """Test that --no-filter bypasses quality filtering."""
        # Include a scene with low motion that would normally be filtered
        scenes = [
            _make_scene(start=0, end=5, score=80.0),
            _make_scene(start=10, end=15, score=50.0),
        ]
        mock_detector = MagicMock()
        mock_detector.detect_scenes.return_value = scenes
        mock_detector_cls.return_value = mock_detector

        # Give second scene very low motion (would be filtered)
        analysis = _make_analysis_result(scenes)
        analysis[id(scenes[1])]["motion_energy"] = 5.0  # Below min threshold
        mock_analyze.return_value = analysis

        mock_processor = MagicMock()
        mock_clip = MagicMock()
        mock_clip.w = 1920
        mock_clip.h = 1080
        mock_clip.duration = 5.0
        mock_processor.extract_clip.return_value = mock_clip

        def write_side_effect(clip, path):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"\x00" * 1000)
            return path

        mock_processor.write_clip.side_effect = write_side_effect
        mock_vp_cls.return_value = mock_processor

        runner = CliRunner()
        with runner.isolated_filesystem():
            Path("video.mp4").touch()
            result = runner.invoke(
                main,
                ["extract-clips", "-i", "video.mp4", "--no-filter", "-n", "10"],
            )

        # Both scenes should be extracted (low motion scene not filtered)
        assert mock_processor.write_clip.call_count == 2


class TestExtractClipsErrorHandling:
    """Tests for error handling during extraction."""

    @patch("drone_reel.cli.analyze_scenes_batch")
    @patch("drone_reel.cli.SceneDetector")
    @patch("drone_reel.cli.VideoProcessor")
    @patch("drone_reel.utils.resource_guard.check_available_memory_mb", return_value=float("inf"))
    @patch("drone_reel.utils.resource_guard.check_disk_space_mb", return_value=float("inf"))
    def test_failed_clip_continues_extraction(
        self, mock_disk, mock_mem, mock_vp_cls, mock_detector_cls, mock_analyze
    ):
        """Test that a failed clip extraction doesn't stop the batch."""
        scenes = [
            _make_scene(start=0, end=5, score=90.0),
            _make_scene(start=10, end=15, score=80.0),
        ]
        mock_detector = MagicMock()
        mock_detector.detect_scenes.return_value = scenes
        mock_detector_cls.return_value = mock_detector
        mock_analyze.return_value = _make_analysis_result(scenes)

        mock_processor = MagicMock()
        call_count = [0]

        def extract_side_effect(segment):
            call_count[0] += 1
            if call_count[0] == 1:
                raise Exception("Extraction failed")
            mock_clip = MagicMock()
            mock_clip.w = 1920
            mock_clip.h = 1080
            mock_clip.duration = 5.0
            return mock_clip

        mock_processor.extract_clip.side_effect = extract_side_effect

        def write_side_effect(clip, path):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"\x00" * 1000)
            return path

        mock_processor.write_clip.side_effect = write_side_effect
        mock_vp_cls.return_value = mock_processor

        runner = CliRunner()
        with runner.isolated_filesystem():
            Path("video.mp4").touch()
            result = runner.invoke(
                main,
                ["extract-clips", "-i", "video.mp4", "-n", "2"],
            )

        assert "Failed" in result.output
        # Second clip should still be extracted
        assert mock_processor.write_clip.call_count == 1

    @patch("drone_reel.utils.resource_guard.check_available_memory_mb", return_value=100.0)
    @patch("drone_reel.utils.resource_guard.check_disk_space_mb", return_value=10.0)
    def test_resource_preflight_blocks_on_error(self, mock_disk, mock_mem):
        """Test that resource preflight errors stop extraction."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            Path("video.mp4").touch()
            result = runner.invoke(
                main,
                ["extract-clips", "-i", "video.mp4", "--quality", "ultra", "-n", "50"],
            )

        # Should fail due to insufficient resources
        assert result.exit_code != 0
```

---

## Step 5: Implementation Order

Execute these steps in order. After each step, verify the tests pass before moving on.

### Step 5.1: Add `write_clip()` to VideoProcessor

1. Open `src/drone_reel/core/video_processor.py`
2. Insert the `write_clip()` method from Step 1 after `extract_clip()` (after line 259, before `_extract_clip_parallel()` at line 261)
3. Run: `pytest tests/test_video_processor.py -x -v` to verify no regressions

### Step 5.2: Add `write_clip()` tests

1. Open `tests/test_video_processor.py`
2. Add the `TestWriteClip` class from Step 3 at the end of the file
3. Run: `pytest tests/test_video_processor.py::TestWriteClip -x -v`
4. Verify: All 10 tests pass

### Step 5.3: Add `extract-clips` CLI command

1. Open `src/drone_reel/cli.py`
2. Insert the `extract_clips` command from Step 2 after the `analyze` command (after line 1282, before the `beats` command definition)
3. Run: `drone-reel extract-clips --help` to verify the command appears
4. Run: `drone-reel --help` to verify extract-clips is listed

### Step 5.4: Add CLI integration tests

1. Create `tests/test_extract_clips.py` with the content from Step 4
2. Run: `pytest tests/test_extract_clips.py -x -v`
3. Verify: All tests pass

### Step 5.5: Full test suite

1. Run: `pytest -x` — verify all existing tests still pass
2. Run: `pytest --tb=short` — check for any warnings or deprecation issues
3. Expected: 1148+ existing tests pass, ~30 new tests pass

---

## Step 6: Integration Verification

### Manual verification with real video

After all tests pass, verify end-to-end behavior with a real video file:

```bash
# Basic extraction
drone-reel extract-clips -i /path/to/drone_video.mp4 -o ./test_clips -n 5

# Expected output:
# - 5 files in ./test_clips/: clip_001_s{N}.mp4 through clip_005_s{N}.mp4
# - Files are playable in QuickTime/VLC
# - Console shows progress with scene scores

# With JSON manifest
drone-reel extract-clips -i /path/to/drone_video.mp4 -o ./test_clips --json -n 5

# Expected: manifest.json in ./test_clips/ with version, clips, summary

# No-filter mode
drone-reel extract-clips -i /path/to/drone_video.mp4 --no-filter --sort chronological -n 20

# Expected: More clips than filtered mode, ordered by time in video

# Enhanced analysis
drone-reel extract-clips -i /path/to/drone_video.mp4 --enhanced --json -n 5

# Expected: manifest.json contains motion_type, hook_tier fields
```

### Quality checks

1. **File sizes**: Each clip should be ~5-20 MB for 5s at high quality
2. **Scene scores**: First clip (clip_001) should have the highest score when sorted by score
3. **Playability**: All clips should play without artifacts in QuickTime/VLC
4. **Color space**: Verify BT.709 metadata with `ffprobe -v quiet -show_streams clip_001_s85.mp4 | grep color`

---

## Summary of Changes

| File | Change Type | Lines Added (est.) |
|------|-------------|-------------------|
| `src/drone_reel/core/video_processor.py` | Modified — add `write_clip()` | ~50 |
| `src/drone_reel/cli.py` | Modified — add `extract_clips` command | ~230 |
| `tests/test_video_processor.py` | Modified — add `TestWriteClip` class | ~100 |
| `tests/test_extract_clips.py` | New file — CLI integration tests | ~400 |
| **Total** | | **~780** |
