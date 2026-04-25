"""
Video processing and stitching with transitions.

Handles clip extraction, stitching, and applying various transitions
between clips using MoviePy.
"""

import gc
import os
import platform
import subprocess
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import cv2
import numpy as np
from moviepy import (
    AudioFileClip,
    CompositeVideoClip,
    VideoFileClip,
    afx,
    concatenate_videoclips,
    vfx,
)

from drone_reel.core.reframer import Reframer
from drone_reel.core.scene_detector import EnhancedSceneInfo, MotionType, SceneInfo


class TransitionType(Enum):
    """Available transition types."""

    CUT = "cut"
    CROSSFADE = "crossfade"
    FADE_BLACK = "fade_black"
    FADE_WHITE = "fade_white"
    ZOOM_IN = "zoom_in"
    ZOOM_OUT = "zoom_out"
    SLIDE_LEFT = "slide_left"
    SLIDE_RIGHT = "slide_right"
    WIPE_LEFT = "wipe_left"
    WIPE_RIGHT = "wipe_right"
    WHIP_PAN = "whip_pan"
    GLITCH_RGB = "glitch_rgb"
    IRIS_IN = "iris_in"
    IRIS_OUT = "iris_out"
    FLASH_WHITE = "flash_white"
    LIGHT_LEAK = "light_leak"
    HYPERLAPSE_ZOOM = "hyperlapse_zoom"
    PARALLAX_LEFT = "parallax_left"
    PARALLAX_RIGHT = "parallax_right"
    WIPE_DIAGONAL = "wipe_diagonal"
    WIPE_DIAMOND = "wipe_diamond"
    FOG_PASS = "fog_pass"
    VORTEX_ZOOM = "vortex_zoom"


@dataclass
class ClipSegment:
    """A segment of video to include in the final output."""

    scene: SceneInfo
    start_offset: float = 0.0
    duration: float | None = None
    transition_in: TransitionType = TransitionType.CUT
    transition_out: TransitionType = TransitionType.CUT
    transition_duration: float = 0.3

    @property
    def effective_start(self) -> float:
        """Actual start time in the source video."""
        return self.scene.start_time + self.start_offset

    @property
    def effective_duration(self) -> float:
        """Actual duration to use."""
        if self.duration:
            return self.duration
        return self.scene.duration - self.start_offset


class VideoProcessor:
    """
    Processes and stitches video clips with transitions.

    Handles extracting segments from source videos, applying transitions,
    and combining everything into a final output.
    """

    def __init__(
        self,
        output_fps: int = 30,
        output_codec: str | None = None,
        output_audio_codec: str = "aac",
        preset: str = "medium",
        threads: int | None = None,
        video_bitrate: str | None = None,
        audio_bitrate: str = "192k",
        stabilize: bool = False,
        stab_strength: str = "adaptive",
        smooth_radius: int = 30,
        stab_border_crop: float = 0.05,
        stab_max_corners: int = 200,
    ):
        """
        Initialize the video processor.

        Args:
            output_fps: Output video frame rate
            output_codec: Video codec for output (auto-detected if None)
            output_audio_codec: Audio codec for output
            preset: FFmpeg encoding preset (ultrafast to veryslow)
            threads: Number of encoding threads (auto-detected if None)
            video_bitrate: Video bitrate (e.g., "8M", "15M", "25M")
            audio_bitrate: Audio bitrate (e.g., "128k", "192k", "320k")
            stabilize: Apply video stabilization to reduce camera shake
            stab_strength: Stabilization mode — "off", "light", "adaptive", or "full".
            smooth_radius: Temporal smoothing window in frames for stabilization.
            stab_border_crop: Fraction of frame edges to crop after stabilization.
            stab_max_corners: Max feature points for goodFeaturesToTrack.
        """
        self.output_fps = output_fps
        self.output_codec = output_codec or self._detect_best_encoder()
        self.output_audio_codec = output_audio_codec
        self.preset = preset
        self.threads = threads or self._detect_cpu_cores()
        self.video_bitrate = video_bitrate or "15M"  # Default 15 Mbps for high quality
        self.audio_bitrate = audio_bitrate
        self.stabilize = stabilize
        self.stab_strength = stab_strength
        self.smooth_radius = smooth_radius
        self.stab_border_crop = stab_border_crop
        self.stab_max_corners = stab_max_corners
        self._transition_funcs: dict[TransitionType, Callable] = {
            TransitionType.CUT: self._transition_cut,
            TransitionType.CROSSFADE: self._transition_crossfade,
            TransitionType.FADE_BLACK: self._transition_fade_black,
            TransitionType.FADE_WHITE: self._transition_fade_white,
            TransitionType.ZOOM_IN: self._transition_zoom_in,
            TransitionType.ZOOM_OUT: self._transition_zoom_out,
            TransitionType.SLIDE_LEFT: self._transition_slide_left,
            TransitionType.SLIDE_RIGHT: self._transition_slide_right,
        }

    def _detect_cpu_cores(self) -> int:
        """
        Auto-detect optimal number of CPU cores for encoding.

        Returns:
            Number of threads to use (capped at half of cores to prevent
            oversubscription when multiple renders run concurrently)
        """
        try:
            cpu_count = os.cpu_count() or 4
            return max(1, min(cpu_count - 1, cpu_count // 2))
        except Exception:
            return 4

    def _detect_best_encoder(self) -> str:
        """
        Detect and return the best available hardware encoder.

        Checks for hardware encoders in this priority:
        1. h264_videotoolbox (macOS)
        2. h264_nvenc (NVIDIA GPUs)
        3. h264_qsv (Intel Quick Sync)
        4. libx264 (software fallback)

        Returns:
            Codec name string
        """
        encoders_to_test = []

        if platform.system() == "Darwin":
            encoders_to_test.append("h264_videotoolbox")

        encoders_to_test.extend(["h264_nvenc", "h264_qsv", "libx264"])

        for encoder in encoders_to_test:
            if self._test_encoder(encoder):
                return encoder

        return "libx264"

    def _test_encoder(self, encoder: str) -> bool:
        """
        Test if an encoder is available in FFmpeg.

        Args:
            encoder: Encoder name to test

        Returns:
            True if encoder is available, False otherwise
        """
        try:
            result = subprocess.run(
                ["ffmpeg", "-hide_banner", "-encoders"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            return encoder in result.stdout
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            return False

    def extract_clip(
        self,
        segment: ClipSegment,
        target_size: tuple[int, int] | None = None,
        reframer: Reframer | None = None,
    ) -> VideoFileClip:
        """
        Extract a clip segment from its source video.

        Args:
            segment: ClipSegment defining what to extract
            target_size: Optional (width, height) to resize to
            reframer: Optional Reframer for proper aspect ratio cropping

        Returns:
            VideoFileClip of the extracted segment

        Note:
            The returned clip keeps a reference to its source video file.
            The caller is responsible for closing the clip when done.
        """
        source_clip = VideoFileClip(str(segment.scene.source_file))

        try:
            end_time = min(
                segment.effective_start + segment.effective_duration, source_clip.duration
            )
            subclip = source_clip.subclipped(segment.effective_start, end_time)

            if reframer:
                # Reset reframer tracking for this new clip
                reframer.reset_tracking()

                # Calculate total frames for this clip
                fps = subclip.fps or 30
                total_frames = int(subclip.duration * fps)

                def reframe_filter(get_frame, t):
                    """Apply reframing to each frame."""
                    frame = get_frame(t)
                    frame_index = int(t * fps)
                    return reframer.reframe_frame(frame, frame_index, total_frames)

                subclip = subclip.transform(reframe_filter)

                # Update clip size to match reframer output
                output_w, output_h = reframer.calculate_output_dimensions(
                    source_clip.w, source_clip.h
                )
                subclip = subclip.with_duration(subclip.duration)

            elif target_size:
                # Legacy resize (may stretch - use reframer for proper aspect ratio)
                subclip = subclip.resized(target_size)

            # Store reference to source clip so it stays open while subclip is used
            # The source will be closed when the subclip is closed
            subclip._source_clip_ref = source_clip

            return subclip
        except Exception:
            source_clip.close()
            raise

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
            "-pix_fmt",
            "yuv420p",
            "-colorspace",
            "bt709",
            "-color_primaries",
            "bt709",
            "-color_trc",
            "bt709",
            # h264_videotoolbox does not write the H.264 SPS VUI for color_primaries
            # or transfer_characteristics, so platforms read those as "unknown" even
            # though we set them on the muxer. h264_metadata bsf rewrites the SPS.
            "-bsf:v",
            "h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1",
            "-movflags",
            "+faststart",
        ]

        # Add maxrate/bufsize for VBV bitrate enforcement
        if self.video_bitrate:
            numeric_str = self.video_bitrate.rstrip("MmKk")
            try:
                numeric_val = float(numeric_str)
                unit = self.video_bitrate[len(numeric_str) :].upper()
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

    def _extract_clip_parallel(
        self,
        segment: ClipSegment,
        target_size: tuple[int, int] | None,
        reframer: Reframer | None = None,
    ) -> VideoFileClip:
        """
        Helper method for parallel clip extraction.

        Args:
            segment: ClipSegment to extract
            target_size: Optional target size for resizing
            reframer: Optional Reframer for proper aspect ratio cropping

        Returns:
            Extracted VideoFileClip
        """
        return self.extract_clip(segment, target_size, reframer)

    def stitch_clips(
        self,
        segments: list[ClipSegment],
        output_path: Path,
        audio_path: Path | None = None,
        target_size: tuple[int, int] | None = None,
        progress_callback: Callable[[float], None] | None = None,
        parallel_extraction: bool = True,
        reframer: Reframer | None = None,
        reframers: list[Reframer] | None = None,
        shake_scores: list[float] | None = None,
        speed_ramps: list[list] | None = None,
        return_clip: bool = False,
    ) -> "Path | VideoFileClip":
        """
        Stitch multiple clip segments into a single video.

        Args:
            segments: List of ClipSegment objects to combine
            output_path: Path for output video file
            audio_path: Optional music track to add
            target_size: Optional (width, height) for output (ignored if reframer provided)
            progress_callback: Optional callback for progress updates
            parallel_extraction: Use parallel extraction for I/O performance
            reframer: Optional single Reframer for all clips
            reframers: Optional list of Reframers (one per clip) for intelligent per-clip reframing
            shake_scores: Optional list of shake scores (0-100) per clip for adaptive stabilization
            speed_ramps: Optional list of SpeedRamp lists per clip for variable speed effects
            return_clip: If True, return the composed clip instead of writing to disk.
                The caller is responsible for writing and closing resources.

        Returns:
            Path to the output video file, or a VideoFileClip if return_clip=True
        """
        if not segments:
            raise ValueError("No segments provided")

        clips = []
        audio = None

        # Use per-clip reframers if provided, otherwise fall back to single reframer
        has_reframing = reframer is not None or reframers is not None

        # Disable parallel extraction when using reframer (has per-clip state)
        use_parallel = parallel_extraction and not has_reframing

        try:
            total_segments = len(segments)

            if use_parallel and len(segments) > 1:
                max_workers = min(4, len(segments))
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    future_to_idx = {
                        executor.submit(self._extract_clip_parallel, seg, target_size, None): i
                        for i, seg in enumerate(segments)
                    }

                    clips_dict = {}
                    for future in as_completed(future_to_idx):
                        idx = future_to_idx[future]
                        try:
                            clip = future.result()
                            clips_dict[idx] = clip

                            if progress_callback:
                                progress_callback((len(clips_dict)) / total_segments * 0.3)
                        except Exception as e:
                            for c in clips_dict.values():
                                try:
                                    if hasattr(c, "_source_clip_ref") and c._source_clip_ref:
                                        c._source_clip_ref.close()
                                    c.close()
                                except Exception:
                                    pass
                            raise RuntimeError(f"Failed to extract clip {idx}: {str(e)}") from e

                    clips = [clips_dict[i] for i in range(len(segments))]
            else:
                for i, segment in enumerate(segments):
                    # Use per-clip reframer if available, otherwise single reframer
                    clip_reframer = None
                    if reframers and i < len(reframers):
                        clip_reframer = reframers[i]
                    elif reframer:
                        clip_reframer = reframer

                    clip = self.extract_clip(segment, target_size, clip_reframer)
                    clips.append(clip)

                    if progress_callback:
                        progress_callback((i + 1) / total_segments * 0.3)

            # Apply adaptive stabilization if enabled
            if self.stabilize:
                from drone_reel.core.stabilizer import stabilize_clip

                pre_stab_clips = list(clips)
                stabilized_clips = []
                stabilized_count = 0
                skipped_count = 0
                for i, clip in enumerate(clips):
                    # Get per-clip shake score for adaptive stabilization
                    clip_shake = shake_scores[i] if shake_scores and i < len(shake_scores) else 50.0
                    try:
                        stabilized = stabilize_clip(
                            clip,
                            smoothing_radius=self.smooth_radius,
                            border_crop=self.stab_border_crop,
                            shake_score=clip_shake,
                            stab_strength=self.stab_strength,
                            max_corners=self.stab_max_corners,
                        )
                        # Track whether stabilization was actually applied
                        if stabilized is clip:
                            skipped_count += 1
                        else:
                            stabilized_count += 1
                        stabilized_clips.append(stabilized)
                    except Exception:
                        # If stabilization fails, use original clip
                        stabilized_clips.append(clip)
                        skipped_count += 1
                    if progress_callback:
                        progress_callback(0.3 + (i + 1) / total_segments * 0.15)
                clips = stabilized_clips

                # Free replaced clips to reclaim memory before encoding
                for i, old_clip in enumerate(pre_stab_clips):
                    if old_clip is not clips[i]:
                        try:
                            old_clip.close()
                        except Exception:
                            pass
                del pre_stab_clips
                gc.collect()

            # Apply speed ramps if provided
            if speed_ramps:
                from drone_reel.core.speed_ramper import SpeedRamper

                ramper = SpeedRamper()
                pre_ramp_clips = list(clips)
                ramped_clips = []
                for i, clip in enumerate(clips):
                    if i < len(speed_ramps) and speed_ramps[i]:
                        try:
                            ramped = ramper.apply_multiple_ramps(clip, speed_ramps[i])
                            ramped_clips.append(ramped)
                        except Exception:
                            ramped_clips.append(clip)
                    else:
                        ramped_clips.append(clip)
                clips = ramped_clips

                # Free replaced clips
                for i, old_clip in enumerate(pre_ramp_clips):
                    if old_clip is not clips[i]:
                        try:
                            old_clip.close()
                        except Exception:
                            pass
                del pre_ramp_clips

            processed_clips = []
            for i, (clip, segment) in enumerate(zip(clips, segments)):
                processed_clip = clip

                if segment.transition_in != TransitionType.CUT:
                    processed_clip = self._apply_transition_in(
                        processed_clip, segment.transition_in, segment.transition_duration
                    )

                if segment.transition_out != TransitionType.CUT:
                    processed_clip = self._apply_transition_out(
                        processed_clip, segment.transition_out, segment.transition_duration
                    )

                processed_clips.append(processed_clip)

                if progress_callback:
                    base_progress = 0.45 if self.stabilize else 0.3
                    progress_callback(base_progress + (i + 1) / total_segments * 0.2)

            final_clip = self._concatenate_with_transitions(processed_clips, segments)

            if audio_path:
                audio = AudioFileClip(str(audio_path))
                if audio.duration > final_clip.duration:
                    audio = audio.subclipped(0, final_clip.duration)
                fade_duration = min(1.0, final_clip.duration * 0.1)
                audio = audio.with_effects([afx.AudioFadeOut(fade_duration)])
                final_clip = final_clip.with_audio(audio)

            # Return clip for further in-memory processing (caller handles write + cleanup)
            if return_clip:
                if progress_callback:
                    progress_callback(0.7)
                # Store clips list on final_clip so caller can clean up later
                final_clip._stitch_source_clips = clips
                final_clip._stitch_audio = audio
                return final_clip

            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Build ffmpeg_params with color space metadata, faststart, and bitrate caps
            ffmpeg_params = [
                "-pix_fmt",
                "yuv420p",
                "-colorspace",
                "bt709",
                "-color_primaries",
                "bt709",
                "-color_trc",
                "bt709",
                # h264_videotoolbox does not write the H.264 SPS VUI for color_primaries
                # or transfer_characteristics, so platforms read those as "unknown" even
                # though we set them on the muxer. h264_metadata bsf rewrites the SPS.
                "-bsf:v",
                "h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1",
                "-movflags",
                "+faststart",
            ]

            # Add maxrate/bufsize for VBV bitrate enforcement
            if self.video_bitrate:
                numeric_str = self.video_bitrate.rstrip("MmKk")
                try:
                    numeric_val = float(numeric_str)
                    unit = self.video_bitrate[len(numeric_str) :].upper()
                    maxrate_val = numeric_val * 1.5
                    bufsize_val = numeric_val * 2
                    maxrate_str = f"{maxrate_val:.0f}{unit}"
                    bufsize_str = f"{bufsize_val:.0f}{unit}"
                    ffmpeg_params += ["-maxrate", maxrate_str, "-bufsize", bufsize_str]
                except (ValueError, IndexError):
                    pass  # Skip bitrate caps if parsing fails

            final_clip.write_videofile(
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

            if progress_callback:
                progress_callback(1.0)

            return output_path

        except Exception as e:
            raise RuntimeError(f"Failed to stitch clips: {str(e)}") from e

        finally:
            # Skip ALL cleanup in return_clip mode - caller manages lifecycle.
            # CompositeVideoClip.close() sets self.bg = None, which breaks
            # subsequent get_frame() calls on the returned clip.
            if not return_clip:
                for clip in clips:
                    try:
                        if hasattr(clip, "_source_clip_ref") and clip._source_clip_ref:
                            clip._source_clip_ref.close()
                        clip.close()
                    except Exception:
                        pass

                if audio:
                    try:
                        audio.close()
                    except Exception:
                        pass

                try:
                    if "final_clip" in locals():
                        final_clip.close()
                except Exception:
                    pass

    def _concatenate_with_transitions(
        self,
        clips: list[VideoFileClip],
        segments: list[ClipSegment],
    ) -> VideoFileClip:
        """
        Concatenate clips, handling crossfade transitions with proper overlap.

        For crossfade transitions, clips must overlap in time to avoid dark frames.
        This method calculates proper start times so fading out and fading in
        clips are composited together during the transition period.
        """
        if len(clips) == 1:
            return clips[0]

        # Transitions that need overlapping compositing
        _overlap_transitions = {
            TransitionType.CROSSFADE,
        }

        # Build timeline with proper overlaps for crossfades
        composed_clips = []
        current_time = 0.0

        for i, clip in enumerate(clips):
            # Set the start time for this clip
            clip_with_start = clip.with_start(current_time)
            composed_clips.append(clip_with_start)

            # Calculate next clip start time based on transition type
            if i + 1 < len(clips):
                if i < len(segments) and segments[i].transition_out in _overlap_transitions:
                    # For crossfade: overlap clips by transition duration
                    # Clamp overlap to max 40% of clip duration to prevent artifacts
                    overlap = min(segments[i].transition_duration, clip.duration * 0.4)
                    current_time += clip.duration - overlap
                else:
                    # For hard cuts and per-clip transitions: no overlap
                    current_time += clip.duration
            else:
                # Last clip: just add duration
                current_time += clip.duration

        return CompositeVideoClip(composed_clips)

    def _apply_transition_in(
        self,
        clip: VideoFileClip,
        transition: TransitionType,
        duration: float,
    ) -> VideoFileClip:
        """
        Apply an entrance transition to a clip.

        Includes safety checks to prevent dark frames from overly long transitions.
        """
        # Safety: clamp duration to max 40% of clip to prevent dark frames
        safe_duration = min(duration, clip.duration * 0.4)
        if safe_duration < 0.1:
            return clip  # Skip transition if clip too short

        if transition == TransitionType.CROSSFADE:
            return clip.with_effects([vfx.CrossFadeIn(safe_duration)])
        elif transition == TransitionType.FADE_BLACK:
            return clip.with_effects([vfx.FadeIn(safe_duration)])
        elif transition == TransitionType.FADE_WHITE:
            return clip.with_effects([vfx.FadeIn(safe_duration, initial_color=(255, 255, 255))])
        elif transition == TransitionType.ZOOM_IN:
            return self._zoom_transition(clip, safe_duration, zoom_in=True, is_start=True)
        elif transition == TransitionType.ZOOM_OUT:
            return self._zoom_transition(clip, safe_duration, zoom_in=False, is_start=True)
        elif transition == TransitionType.WHIP_PAN:
            return self._transition_whip_pan(clip, safe_duration, is_start=True)
        elif transition == TransitionType.GLITCH_RGB:
            return self._transition_glitch_rgb(clip, safe_duration, is_start=True)
        elif transition == TransitionType.IRIS_IN:
            return self._transition_iris(clip, safe_duration, is_start=True, opening=True)
        elif transition == TransitionType.IRIS_OUT:
            return self._transition_iris(clip, safe_duration, is_start=True, opening=False)
        elif transition == TransitionType.FLASH_WHITE:
            return self._transition_flash_white(clip, safe_duration, is_start=True)
        elif transition == TransitionType.LIGHT_LEAK:
            return self._transition_light_leak(clip, safe_duration, is_start=True)
        elif transition == TransitionType.HYPERLAPSE_ZOOM:
            return self._transition_hyperlapse_zoom(clip, safe_duration, is_start=True)
        elif transition == TransitionType.PARALLAX_LEFT:
            return self._transition_parallax(clip, safe_duration, direction="left", is_start=True)
        elif transition == TransitionType.PARALLAX_RIGHT:
            return self._transition_parallax(clip, safe_duration, direction="right", is_start=True)
        elif transition == TransitionType.WIPE_DIAGONAL:
            return self._transition_wipe_diagonal(clip, safe_duration, is_start=True)
        elif transition == TransitionType.WIPE_DIAMOND:
            return self._transition_wipe_diamond(clip, safe_duration, is_start=True)
        elif transition == TransitionType.FOG_PASS:
            return self._transition_fog_pass(clip, safe_duration, is_start=True)
        elif transition == TransitionType.VORTEX_ZOOM:
            return self._transition_vortex_zoom(clip, safe_duration, is_start=True)
        return clip

    def _apply_transition_out(
        self,
        clip: VideoFileClip,
        transition: TransitionType,
        duration: float,
    ) -> VideoFileClip:
        """
        Apply an exit transition to a clip.

        Includes safety checks to prevent dark frames from overly long transitions.
        """
        # Safety: clamp duration to max 40% of clip to prevent dark frames
        safe_duration = min(duration, clip.duration * 0.4)
        if safe_duration < 0.1:
            return clip  # Skip transition if clip too short

        if transition == TransitionType.CROSSFADE:
            return clip.with_effects([vfx.CrossFadeOut(safe_duration)])
        elif transition == TransitionType.FADE_BLACK:
            return clip.with_effects([vfx.FadeOut(safe_duration)])
        elif transition == TransitionType.FADE_WHITE:
            return clip.with_effects([vfx.FadeOut(safe_duration, final_color=(255, 255, 255))])
        elif transition == TransitionType.ZOOM_IN:
            return self._zoom_transition(clip, safe_duration, zoom_in=True, is_start=False)
        elif transition == TransitionType.ZOOM_OUT:
            return self._zoom_transition(clip, safe_duration, zoom_in=False, is_start=False)
        elif transition == TransitionType.WHIP_PAN:
            return self._transition_whip_pan(clip, safe_duration, is_start=False)
        elif transition == TransitionType.GLITCH_RGB:
            return self._transition_glitch_rgb(clip, safe_duration, is_start=False)
        elif transition == TransitionType.IRIS_IN:
            return self._transition_iris(clip, safe_duration, is_start=False, opening=True)
        elif transition == TransitionType.IRIS_OUT:
            return self._transition_iris(clip, safe_duration, is_start=False, opening=False)
        elif transition == TransitionType.FLASH_WHITE:
            return self._transition_flash_white(clip, safe_duration, is_start=False)
        elif transition == TransitionType.LIGHT_LEAK:
            return self._transition_light_leak(clip, safe_duration, is_start=False)
        elif transition == TransitionType.HYPERLAPSE_ZOOM:
            return self._transition_hyperlapse_zoom(clip, safe_duration, is_start=False)
        elif transition == TransitionType.PARALLAX_LEFT:
            return self._transition_parallax(clip, safe_duration, direction="left", is_start=False)
        elif transition == TransitionType.PARALLAX_RIGHT:
            return self._transition_parallax(clip, safe_duration, direction="right", is_start=False)
        elif transition == TransitionType.WIPE_DIAGONAL:
            return self._transition_wipe_diagonal(clip, safe_duration, is_start=False)
        elif transition == TransitionType.WIPE_DIAMOND:
            return self._transition_wipe_diamond(clip, safe_duration, is_start=False)
        elif transition == TransitionType.FOG_PASS:
            return self._transition_fog_pass(clip, safe_duration, is_start=False)
        elif transition == TransitionType.VORTEX_ZOOM:
            return self._transition_vortex_zoom(clip, safe_duration, is_start=False)
        return clip

    def _zoom_transition(
        self,
        clip: VideoFileClip,
        duration: float,
        zoom_in: bool = True,
        is_start: bool = True,
    ) -> VideoFileClip:
        """Create a zoom transition effect."""
        clip_duration = clip.duration

        def zoom_effect(get_frame, t):
            frame = get_frame(t)

            if is_start:
                progress = min(t / duration, 1.0)
            else:
                time_from_end = clip_duration - t
                progress = min(time_from_end / duration, 1.0)

            if zoom_in:
                scale = 1.0 + (1.0 - progress) * 0.2
            else:
                scale = 1.0 + progress * 0.2

            if scale != 1.0:
                h, w = frame.shape[:2]
                new_h, new_w = int(h * scale), int(w * scale)

                scaled = cv2.resize(frame, (new_w, new_h))

                start_y = (new_h - h) // 2
                start_x = (new_w - w) // 2
                cropped = scaled[start_y : start_y + h, start_x : start_x + w]

                return cropped

            return frame

        return clip.transform(zoom_effect)

    def _transition_whip_pan(
        self,
        clip: VideoFileClip,
        duration: float,
        is_start: bool = True,
        horizontal: bool = True,
    ) -> VideoFileClip:
        """Whip pan transition: directional motion blur streak."""
        clip_duration = clip.duration

        def whip_effect(get_frame, t):
            frame = get_frame(t)
            if is_start:
                progress = min(t / duration, 1.0)
                # Blur decreases as clip starts (entering from blur)
                blur_strength = 1.0 - progress
            else:
                time_from_end = clip_duration - t
                progress = min(time_from_end / duration, 1.0)
                # Blur increases as clip ends (exiting to blur)
                blur_strength = 1.0 - progress

            if blur_strength < 0.05:
                return frame

            # Directional motion blur kernel
            kernel_size = max(3, int(blur_strength * 80)) | 1  # Ensure odd
            kernel = np.zeros((kernel_size, kernel_size), dtype=np.float32)
            if horizontal:
                kernel[kernel_size // 2, :] = 1.0 / kernel_size
            else:
                kernel[:, kernel_size // 2] = 1.0 / kernel_size

            blurred = cv2.filter2D(frame, -1, kernel)
            # Blend original and blurred based on strength for smoother falloff
            alpha = blur_strength**1.5  # Ease-in curve
            return np.clip(
                frame.astype(np.float32) * (1 - alpha) + blurred.astype(np.float32) * alpha,
                0,
                255,
            ).astype(np.uint8)

        return clip.transform(whip_effect)

    def _transition_glitch_rgb(
        self,
        clip: VideoFileClip,
        duration: float,
        is_start: bool = True,
    ) -> VideoFileClip:
        """RGB channel split glitch transition."""
        clip_duration = clip.duration

        def glitch_effect(get_frame, t):
            frame = get_frame(t)
            if is_start:
                progress = min(t / duration, 1.0)
                intensity = 1.0 - progress
            else:
                time_from_end = clip_duration - t
                progress = min(time_from_end / duration, 1.0)
                intensity = 1.0 - progress

            if intensity < 0.05:
                return frame

            h, w = frame.shape[:2]
            # Triangle wave: peak at center of transition
            shift = int(intensity * w * 0.06)  # Max 6% of width
            if shift < 1:
                return frame

            result = frame.copy()
            # Shift R channel right, B channel left (frame is RGB from MoviePy)
            if shift > 0:
                result[:, shift:, 0] = frame[:, :-shift, 0]  # R shifts right
                result[:, :shift, 0] = frame[:, :1, 0]  # Fill left edge
                result[:, :-shift, 2] = frame[:, shift:, 2]  # B shifts left
                result[:, -shift:, 2] = frame[:, -1:, 2]  # Fill right edge
            return result

        return clip.transform(glitch_effect)

    def _transition_iris(
        self,
        clip: VideoFileClip,
        duration: float,
        is_start: bool = True,
        opening: bool = True,
    ) -> VideoFileClip:
        """Iris wipe transition: circular reveal/close."""
        clip_duration = clip.duration

        def iris_effect(get_frame, t):
            frame = get_frame(t)
            h, w = frame.shape[:2]

            if is_start:
                progress = min(t / duration, 1.0)
            else:
                time_from_end = clip_duration - t
                progress = min(time_from_end / duration, 1.0)

            if opening:
                # Opening: circle expands from 0 to full frame
                radius_frac = progress
            else:
                # Closing: circle shrinks from full to 0
                radius_frac = 1.0 - progress

            if radius_frac >= 1.0:
                return frame
            if radius_frac <= 0.0:
                return np.zeros_like(frame)

            # Build circular mask with feathered edge
            cy, cx = h / 2, w / 2
            max_radius = np.sqrt(cx**2 + cy**2)
            radius = radius_frac * max_radius

            y_coords = np.arange(h).reshape(-1, 1)
            x_coords = np.arange(w).reshape(1, -1)
            dist = np.sqrt((x_coords - cx) ** 2 + (y_coords - cy) ** 2)

            # Feathered edge (3% of max_radius)
            feather = max(max_radius * 0.03, 2.0)
            mask = np.clip((radius - dist) / feather, 0.0, 1.0).astype(np.float32)
            mask_3d = mask[:, :, np.newaxis]

            return (frame.astype(np.float32) * mask_3d).astype(np.uint8)

        return clip.transform(iris_effect)

    def _transition_flash_white(
        self,
        clip: VideoFileClip,
        duration: float,
        is_start: bool = True,
    ) -> VideoFileClip:
        """Non-linear whiteout flash transition: fast rise, slow fall."""
        clip_duration = clip.duration

        def flash_effect(get_frame, t):
            frame = get_frame(t)
            if is_start:
                progress = min(t / duration, 1.0)
                # Fast fall from white: exponential decay
                flash_intensity = (1.0 - progress) ** 2.5
            else:
                time_from_end = clip_duration - t
                progress = min(time_from_end / duration, 1.0)
                # Fast rise to white: exponential
                flash_intensity = (1.0 - progress) ** 2.5

            if flash_intensity < 0.01:
                return frame

            white = np.full_like(frame, 255, dtype=np.float32)
            blended = frame.astype(np.float32) * (1 - flash_intensity) + white * flash_intensity
            return np.clip(blended, 0, 255).astype(np.uint8)

        return clip.transform(flash_effect)

    def _transition_light_leak(
        self,
        clip: VideoFileClip,
        duration: float,
        is_start: bool = True,
    ) -> VideoFileClip:
        """Light leak transition: diagonal warm gradient sweep."""
        clip_duration = clip.duration

        def leak_effect(get_frame, t):
            frame = get_frame(t)
            h, w = frame.shape[:2]

            if is_start:
                progress = min(t / duration, 1.0)
                sweep = 1.0 - progress  # Leak fades away as clip enters
            else:
                time_from_end = clip_duration - t
                progress = min(time_from_end / duration, 1.0)
                sweep = 1.0 - progress  # Leak grows as clip exits

            if sweep < 0.02:
                return frame

            # Diagonal gradient: top-left to bottom-right
            y_coords = np.linspace(0, 1, h).reshape(-1, 1)
            x_coords = np.linspace(0, 1, w).reshape(1, -1)
            diag = (x_coords + y_coords) / 2.0  # 0..1 diagonal

            # Sweep position (center of the leak band)
            center = sweep
            sigma = 0.15  # Width of the leak band
            leak_mask = np.exp(-((diag - center) ** 2) / (2 * sigma**2)).astype(np.float32)
            leak_mask *= sweep  # Overall intensity

            # Warm amber color (RGB: 255, 180, 60)
            leak_color = np.array([255, 180, 60], dtype=np.float32)
            leak_layer = leak_mask[:, :, np.newaxis] * leak_color

            # Additive blend (screen-like)
            result = frame.astype(np.float32) + leak_layer * 0.7
            return np.clip(result, 0, 255).astype(np.uint8)

        return clip.transform(leak_effect)

    def _transition_hyperlapse_zoom(
        self,
        clip: VideoFileClip,
        duration: float,
        is_start: bool = True,
    ) -> VideoFileClip:
        """Hyperlapse zoom: combined speed ramp + zoom fly-through effect."""
        clip_duration = clip.duration

        def hyperlapse_effect(get_frame, t):
            frame = get_frame(t)
            if is_start:
                progress = min(t / duration, 1.0)
                # Zooming in from wide, decelerating
                zoom = 1.0 + (1.0 - progress) * 0.4  # 1.4x -> 1.0x
            else:
                time_from_end = clip_duration - t
                progress = min(time_from_end / duration, 1.0)
                # Zooming out to wide, accelerating
                zoom = 1.0 + (1.0 - progress) * 0.4

            if zoom <= 1.001:
                return frame

            h, w = frame.shape[:2]
            new_h, new_w = int(h * zoom), int(w * zoom)
            scaled = cv2.resize(frame, (new_w, new_h))
            start_y = (new_h - h) // 2
            start_x = (new_w - w) // 2
            cropped = scaled[start_y : start_y + h, start_x : start_x + w]

            # Add subtle radial blur for motion feel
            if zoom > 1.1:
                blur_strength = (zoom - 1.0) * 0.3
                kernel_size = max(3, int(blur_strength * 20)) | 1
                blurred = cv2.GaussianBlur(cropped, (kernel_size, kernel_size), 0)
                # Only blur edges, keep center sharp
                cy, cx = h / 2, w / 2
                y_c = np.arange(h).reshape(-1, 1)
                x_c = np.arange(w).reshape(1, -1)
                dist = np.sqrt(((x_c - cx) / cx) ** 2 + ((y_c - cy) / cy) ** 2)
                edge_mask = np.clip(dist - 0.5, 0, 1).astype(np.float32)[:, :, np.newaxis]
                cropped = (
                    cropped.astype(np.float32) * (1 - edge_mask)
                    + blurred.astype(np.float32) * edge_mask
                ).astype(np.uint8)

            return cropped

        return clip.transform(hyperlapse_effect)

    def _transition_parallax(
        self,
        clip: VideoFileClip,
        duration: float,
        direction: str = "left",
        is_start: bool = True,
    ) -> VideoFileClip:
        """Parallax slide: differential speed slide creating depth illusion."""
        clip_duration = clip.duration

        def parallax_effect(get_frame, t):
            frame = get_frame(t)
            if is_start:
                progress = min(t / duration, 1.0)
            else:
                time_from_end = clip_duration - t
                progress = min(time_from_end / duration, 1.0)

            if progress >= 1.0:
                return frame

            h, w = frame.shape[:2]
            # Two layers slide at different speeds (parallax depth)
            mid_y = h // 2
            ease = 1.0 - progress  # 1 -> 0

            # Top half (sky/background) moves slower
            bg_shift = int(ease * w * 0.15)
            # Bottom half (foreground) moves faster
            fg_shift = int(ease * w * 0.35)

            if direction == "right":
                bg_shift, fg_shift = -bg_shift, -fg_shift

            result = frame.copy()
            # Shift top half
            if bg_shift != 0:
                result[:mid_y] = np.roll(frame[:mid_y], bg_shift, axis=1)
            # Shift bottom half
            if fg_shift != 0:
                result[mid_y:] = np.roll(frame[mid_y:], fg_shift, axis=1)

            return result

        return clip.transform(parallax_effect)

    def _transition_wipe_diagonal(
        self,
        clip: VideoFileClip,
        duration: float,
        is_start: bool = True,
    ) -> VideoFileClip:
        """Diagonal wipe: 45-degree line sweep reveal."""
        clip_duration = clip.duration

        def diagonal_effect(get_frame, t):
            frame = get_frame(t)
            if is_start:
                progress = min(t / duration, 1.0)
            else:
                time_from_end = clip_duration - t
                progress = min(time_from_end / duration, 1.0)

            if progress >= 1.0:
                return frame

            h, w = frame.shape[:2]
            # Diagonal coordinate: project (x, y) onto 45-degree line
            y_coords = np.arange(h).reshape(-1, 1).astype(np.float32) / h
            x_coords = np.arange(w).reshape(1, -1).astype(np.float32) / w
            diagonal = (x_coords + y_coords) / 2.0  # 0 at top-left, 1 at bottom-right

            # Feathered edge
            feather = 0.05
            if is_start:
                mask = np.clip((diagonal - (1.0 - progress)) / feather + 0.5, 0, 1)
            else:
                mask = np.clip(((1.0 - progress) - diagonal) / feather + 0.5, 0, 1)

            mask = mask[:, :, np.newaxis].astype(np.float32)
            black = np.zeros_like(frame, dtype=np.float32)
            result = frame.astype(np.float32) * mask + black * (1 - mask)
            return result.astype(np.uint8)

        return clip.transform(diagonal_effect)

    def _transition_wipe_diamond(
        self,
        clip: VideoFileClip,
        duration: float,
        is_start: bool = True,
    ) -> VideoFileClip:
        """Diamond wipe: L1 distance expanding diamond from center."""
        clip_duration = clip.duration

        def diamond_effect(get_frame, t):
            frame = get_frame(t)
            if is_start:
                progress = min(t / duration, 1.0)
            else:
                time_from_end = clip_duration - t
                progress = min(time_from_end / duration, 1.0)

            if progress >= 1.0:
                return frame

            h, w = frame.shape[:2]
            cy, cx = h / 2, w / 2
            y_coords = np.abs(np.arange(h).reshape(-1, 1) - cy) / cy
            x_coords = np.abs(np.arange(w).reshape(1, -1) - cx) / cx
            # L1 distance (diamond shape)
            dist = x_coords + y_coords  # 0 at center, 2 at corners

            max_dist = 2.0
            threshold = progress * max_dist
            feather = 0.06 * max_dist

            mask = np.clip((threshold - dist) / feather, 0, 1)
            mask = mask[:, :, np.newaxis].astype(np.float32)

            black = np.zeros_like(frame, dtype=np.float32)
            result = frame.astype(np.float32) * mask + black * (1 - mask)
            return result.astype(np.uint8)

        return clip.transform(diamond_effect)

    def _transition_fog_pass(
        self,
        clip: VideoFileClip,
        duration: float,
        is_start: bool = True,
    ) -> VideoFileClip:
        """Fog pass: procedural fog obscures then reveals clip."""
        clip_duration = clip.duration

        def fog_effect(get_frame, t):
            frame = get_frame(t)
            if is_start:
                progress = min(t / duration, 1.0)
            else:
                time_from_end = clip_duration - t
                progress = min(time_from_end / duration, 1.0)

            if progress >= 1.0:
                return frame

            h, w = frame.shape[:2]
            # Fog density peaks at progress=0 and fades to clear at progress=1
            fog_density = (1.0 - progress) ** 1.5

            # Multi-frequency fog pattern using sine waves
            y = np.arange(h, dtype=np.float32).reshape(-1, 1)
            x = np.arange(w, dtype=np.float32).reshape(1, -1)
            # Low freq base + medium freq detail
            fog_pattern = (
                np.sin(x / w * 3.14 * 2 + progress * 5) * 0.3
                + np.sin(y / h * 3.14 * 3 + progress * 3) * 0.2
                + np.sin((x + y) / (w + h) * 3.14 * 5) * 0.15
                + 0.5
            )
            fog_pattern = np.clip(fog_pattern * fog_density, 0, 1)
            fog_pattern = fog_pattern[:, :, np.newaxis].astype(np.float32)

            # Fog color: white-gray
            fog_color = np.full_like(frame, 220, dtype=np.float32)
            result = frame.astype(np.float32) * (1 - fog_pattern) + fog_color * fog_pattern
            return np.clip(result, 0, 255).astype(np.uint8)

        return clip.transform(fog_effect)

    def _transition_vortex_zoom(
        self,
        clip: VideoFileClip,
        duration: float,
        is_start: bool = True,
    ) -> VideoFileClip:
        """Vortex zoom: radial zoom blur tunnel effect for FPV footage."""
        clip_duration = clip.duration

        def vortex_effect(get_frame, t):
            frame = get_frame(t)
            if is_start:
                progress = min(t / duration, 1.0)
            else:
                time_from_end = clip_duration - t
                progress = min(time_from_end / duration, 1.0)

            if progress >= 1.0:
                return frame

            h, w = frame.shape[:2]
            intensity = (1.0 - progress) ** 2  # Ease out

            if intensity < 0.01:
                return frame

            # Iterative zoom + average for radial blur
            zoom_step = 1.0 + intensity * 0.08
            result = frame.astype(np.float32)
            n_steps = 3
            for i in range(1, n_steps + 1):
                z = 1.0 + (zoom_step - 1.0) * i / n_steps
                new_h, new_w = int(h * z), int(w * z)
                if new_h <= h or new_w <= w:
                    continue
                scaled = cv2.resize(frame, (new_w, new_h))
                sy = (new_h - h) // 2
                sx = (new_w - w) // 2
                result += scaled[sy : sy + h, sx : sx + w].astype(np.float32)

            result /= n_steps + 1
            return np.clip(result, 0, 255).astype(np.uint8)

        return clip.transform(vortex_effect)

    def _transition_cut(self, clip1: VideoFileClip, clip2: VideoFileClip, duration: float):
        """Simple cut transition (no effect)."""
        return concatenate_videoclips([clip1, clip2])

    def _transition_crossfade(self, clip1: VideoFileClip, clip2: VideoFileClip, duration: float):
        """Crossfade transition between clips."""
        clip1 = clip1.with_effects([vfx.CrossFadeOut(duration)])
        clip2 = clip2.with_effects([vfx.CrossFadeIn(duration)])

        clip2 = clip2.with_start(clip1.duration - duration)

        return CompositeVideoClip([clip1, clip2])

    def _transition_fade_black(self, clip1: VideoFileClip, clip2: VideoFileClip, duration: float):
        """Fade to black transition."""
        clip1 = clip1.with_effects([vfx.FadeOut(duration / 2)])
        clip2 = clip2.with_effects([vfx.FadeIn(duration / 2)])
        return concatenate_videoclips([clip1, clip2])

    def _transition_fade_white(self, clip1: VideoFileClip, clip2: VideoFileClip, duration: float):
        """Fade to white transition."""
        clip1 = clip1.with_effects([vfx.FadeOut(duration / 2, final_color=(255, 255, 255))])
        clip2 = clip2.with_effects([vfx.FadeIn(duration / 2, initial_color=(255, 255, 255))])
        return concatenate_videoclips([clip1, clip2])

    def _transition_zoom_in(self, clip1: VideoFileClip, clip2: VideoFileClip, duration: float):
        """Zoom in transition."""
        clip1 = self._zoom_transition(clip1, duration, zoom_in=True, is_start=False)
        return concatenate_videoclips([clip1, clip2])

    def _transition_zoom_out(self, clip1: VideoFileClip, clip2: VideoFileClip, duration: float):
        """Zoom out transition."""
        clip2 = self._zoom_transition(clip2, duration, zoom_in=False, is_start=True)
        return concatenate_videoclips([clip1, clip2])

    def _transition_slide_left(self, clip1: VideoFileClip, clip2: VideoFileClip, duration: float):
        """Slide left transition - clip2 slides in from right."""
        from moviepy import CompositeVideoClip

        w, h = clip1.w, clip1.h

        # Trim clips to overlap
        clip1_trimmed = clip1.subclipped(0, clip1.duration)
        clip2_trimmed = clip2.subclipped(0, min(duration, clip2.duration))

        # Animate clip2 sliding from right
        def slide_position(t):
            progress = t / duration
            x = int(w * (1 - progress))  # Slide from right to center
            return (x, 0)

        clip2_sliding = clip2_trimmed.with_position(slide_position)

        # Composite during transition, then continue with clip2
        transition = CompositeVideoClip(
            [clip1_trimmed.subclipped(clip1.duration - duration), clip2_sliding], size=(w, h)
        ).with_duration(duration)
        clip2_rest = clip2.subclipped(duration) if clip2.duration > duration else None

        if clip2_rest:
            return concatenate_videoclips(
                [clip1.subclipped(0, clip1.duration - duration), transition, clip2_rest]
            )
        return concatenate_videoclips([clip1.subclipped(0, clip1.duration - duration), transition])

    def _transition_slide_right(self, clip1: VideoFileClip, clip2: VideoFileClip, duration: float):
        """Slide right transition - clip2 slides in from left."""
        from moviepy import CompositeVideoClip

        w, h = clip1.w, clip1.h

        # Trim clips to overlap
        clip1_trimmed = clip1.subclipped(0, clip1.duration)
        clip2_trimmed = clip2.subclipped(0, min(duration, clip2.duration))

        # Animate clip2 sliding from left
        def slide_position(t):
            progress = t / duration
            x = int(-w * (1 - progress))  # Slide from left to center
            return (x, 0)

        clip2_sliding = clip2_trimmed.with_position(slide_position)

        # Composite during transition
        transition = CompositeVideoClip(
            [clip1_trimmed.subclipped(clip1.duration - duration), clip2_sliding], size=(w, h)
        ).with_duration(duration)
        clip2_rest = clip2.subclipped(duration) if clip2.duration > duration else None

        if clip2_rest:
            return concatenate_videoclips(
                [clip1.subclipped(0, clip1.duration - duration), transition, clip2_rest]
            )
        return concatenate_videoclips([clip1.subclipped(0, clip1.duration - duration), transition])

    def _are_motion_directions_aligned(
        self,
        dir1: tuple[float, float],
        dir2: tuple[float, float],
        threshold: float = 0.7,
    ) -> bool:
        """
        Check if two motion direction vectors are aligned (similar direction).

        Args:
            dir1: First motion direction (x, y)
            dir2: Second motion direction (x, y)
            threshold: Cosine similarity threshold (0.7 = ~45 degrees)

        Returns:
            True if motion directions are aligned
        """
        # Handle zero vectors
        mag1 = np.sqrt(dir1[0] ** 2 + dir1[1] ** 2)
        mag2 = np.sqrt(dir2[0] ** 2 + dir2[1] ** 2)

        if mag1 < 0.01 or mag2 < 0.01:
            return False  # Static scenes

        # Normalize
        norm1 = (dir1[0] / mag1, dir1[1] / mag1)
        norm2 = (dir2[0] / mag2, dir2[1] / mag2)

        # Cosine similarity
        dot = norm1[0] * norm2[0] + norm1[1] * norm2[1]
        return dot >= threshold

    def _are_motion_speeds_similar(
        self,
        dir1: tuple[float, float],
        dir2: tuple[float, float],
        tolerance: float = 0.5,
    ) -> bool:
        """
        Check if two motion direction vectors have similar magnitude (speed).

        Args:
            dir1: First motion direction (x, y)
            dir2: Second motion direction (x, y)
            tolerance: Relative difference threshold

        Returns:
            True if motion speeds are similar
        """
        mag1 = np.sqrt(dir1[0] ** 2 + dir1[1] ** 2)
        mag2 = np.sqrt(dir2[0] ** 2 + dir2[1] ** 2)

        if mag1 < 0.01 and mag2 < 0.01:
            return True  # Both static

        max_mag = max(mag1, mag2)
        if max_mag < 0.01:
            return True

        rel_diff = abs(mag1 - mag2) / max_mag
        return rel_diff <= tolerance

    def select_motion_matched_transition(
        self,
        scene1: SceneInfo,
        scene2: SceneInfo,
        default_duration: float = 0.3,
    ) -> tuple[TransitionType, float]:
        """
        Select the best transition type based on motion matching between scenes.

        Motion-matched cuts follow these principles:
        - Same direction, similar speed -> Hard cut (seamless continuation)
        - Same direction, different speed -> Quick crossfade (0.2s)
        - Different direction -> Longer crossfade (0.4s)
        - Static scenes -> Default crossfade (0.3s)
        - High-energy FPV/fast motion -> Glitch RGB, Vortex Zoom, or Whip Pan
        - Reveal/dramatic entries -> Iris In
        - Tilt/golden hour scenes -> Light Leak
        - Orbit scenes -> Diamond wipe
        - Altitude changes -> Fog pass

        Args:
            scene1: First scene (outgoing)
            scene2: Second scene (incoming)
            default_duration: Default transition duration

        Returns:
            Tuple of (TransitionType, duration)
        """
        # Check if scenes have enhanced motion info
        if not isinstance(scene1, EnhancedSceneInfo) or not isinstance(scene2, EnhancedSceneInfo):
            return TransitionType.CROSSFADE, default_duration

        dir1 = scene1.motion_direction
        dir2 = scene2.motion_direction

        # Check for static scenes
        mag1 = np.sqrt(dir1[0] ** 2 + dir1[1] ** 2)
        mag2 = np.sqrt(dir2[0] ** 2 + dir2[1] ** 2)

        if mag1 < 0.01 and mag2 < 0.01:
            # Both static - use default crossfade
            return TransitionType.CROSSFADE, default_duration

        # Check if motion directions are aligned
        directions_aligned = self._are_motion_directions_aligned(dir1, dir2)
        speeds_similar = self._are_motion_speeds_similar(dir1, dir2)

        if directions_aligned and speeds_similar:
            # Matching motion - hard cut for seamless continuation
            return TransitionType.CUT, 0.0

        if directions_aligned:
            # Same direction but different speed - quick crossfade
            return TransitionType.CROSSFADE, 0.2

        # Check for horizontal pan motion - use whip pan for dramatic effect

        # Fast pan exits -> whip pan (the #1 viral transition)
        if (
            isinstance(scene1, EnhancedSceneInfo)
            and scene1.motion_type in (MotionType.PAN_RIGHT, MotionType.PAN_LEFT)
            and mag1 > 0.03
        ):
            return TransitionType.WHIP_PAN, 0.3

        # FPV or high-energy motion -> vortex zoom or glitch RGB
        if isinstance(scene1, EnhancedSceneInfo) and scene1.motion_type == MotionType.FPV:
            if mag1 > 0.05:
                return TransitionType.VORTEX_ZOOM, 0.3
            return TransitionType.GLITCH_RGB, 0.2

        # Scene1 panning right + Scene2 different -> parallax or slide
        if isinstance(scene1, EnhancedSceneInfo) and scene1.motion_type == MotionType.PAN_RIGHT:
            if mag1 > 0.02:
                return TransitionType.PARALLAX_LEFT, 0.4
            return TransitionType.SLIDE_LEFT, 0.4

        # Scene1 panning left + Scene2 different -> parallax or slide
        if isinstance(scene1, EnhancedSceneInfo) and scene1.motion_type == MotionType.PAN_LEFT:
            if mag1 > 0.02:
                return TransitionType.PARALLAX_RIGHT, 0.4
            return TransitionType.SLIDE_RIGHT, 0.4

        # Orbit scenes -> diamond wipe (geometric match)
        if isinstance(scene1, EnhancedSceneInfo) and scene1.motion_type in (
            MotionType.ORBIT_CW,
            MotionType.ORBIT_CCW,
        ):
            return TransitionType.WIPE_DIAMOND, 0.4

        # Use iris in for reveal/dramatic motion types
        if isinstance(scene2, EnhancedSceneInfo) and scene2.motion_type == MotionType.REVEAL:
            return TransitionType.IRIS_IN, 0.4

        # Tilt up -> light leak (natural sun direction)
        if isinstance(scene1, EnhancedSceneInfo) and scene1.motion_type == MotionType.TILT_UP:
            return TransitionType.LIGHT_LEAK, 0.4

        # Tilt down -> fog pass (descending through clouds)
        if isinstance(scene1, EnhancedSceneInfo) and scene1.motion_type == MotionType.TILT_DOWN:
            return TransitionType.FOG_PASS, 0.5

        # Flyover/approach exits -> hyperlapse zoom
        if isinstance(scene1, EnhancedSceneInfo) and scene1.motion_type in (MotionType.FLYOVER,):
            return TransitionType.HYPERLAPSE_ZOOM, 0.4

        # Different motion directions - diagonal wipe for visual variety
        if mag1 > 0.02 and mag2 > 0.02:
            return TransitionType.WIPE_DIAGONAL, 0.4

        # Default - longer crossfade for smooth transition
        return TransitionType.CROSSFADE, 0.4

    def create_segments_from_scenes(
        self,
        scenes: list[SceneInfo],
        clip_durations: list[float],
        transitions: list[TransitionType] | None = None,
        transition_duration: float = 0.3,
    ) -> list[ClipSegment]:
        """
        Create ClipSegments from scenes with specified durations.

        Args:
            scenes: List of SceneInfo objects
            clip_durations: Duration for each clip
            transitions: Optional list of transitions between clips
            transition_duration: Duration of each transition

        Returns:
            List of ClipSegment objects ready for stitching
        """
        if len(scenes) != len(clip_durations):
            min_len = min(len(scenes), len(clip_durations))
            scenes = scenes[:min_len]
            clip_durations = clip_durations[:min_len]

        if transitions is None:
            transitions = [TransitionType.CROSSFADE] * (len(scenes) - 1)
            transitions.append(TransitionType.FADE_BLACK)

        segments = []
        for i, (scene, duration) in enumerate(zip(scenes, clip_durations)):
            center_offset = max(0, (scene.duration - duration) / 2)

            transition_in = TransitionType.CUT
            if i > 0 and i - 1 < len(transitions):
                transition_in = transitions[i - 1]

            transition_out = TransitionType.CUT
            if i < len(transitions):
                transition_out = transitions[i]

            segment = ClipSegment(
                scene=scene,
                start_offset=center_offset,
                duration=duration,
                transition_in=transition_in,
                transition_out=transition_out,
                transition_duration=transition_duration,
            )
            segments.append(segment)

        return segments

    def create_motion_matched_segments(
        self,
        scenes: list[SceneInfo],
        clip_durations: list[float],
        default_transition_duration: float = 0.3,
    ) -> list[ClipSegment]:
        """
        Create ClipSegments with automatically selected motion-matched transitions.

        This method analyzes the motion characteristics of adjacent scenes and
        selects the optimal transition type and duration:
        - Aligned motion + similar speed → Hard cut (seamless)
        - Aligned motion + different speed → Quick crossfade (0.2s)
        - Different motion → Longer crossfade (0.4s)
        - Static scenes → Default crossfade

        Args:
            scenes: List of SceneInfo objects (EnhancedSceneInfo for best results)
            clip_durations: Duration for each clip
            default_transition_duration: Fallback transition duration

        Returns:
            List of ClipSegment objects with motion-matched transitions
        """
        if len(scenes) != len(clip_durations):
            min_len = min(len(scenes), len(clip_durations))
            scenes = scenes[:min_len]
            clip_durations = clip_durations[:min_len]

        segments = []
        for i, (scene, duration) in enumerate(zip(scenes, clip_durations)):
            center_offset = max(0, (scene.duration - duration) / 2)

            # Determine transition in (from previous segment)
            transition_in = TransitionType.CUT
            transition_in_duration = default_transition_duration
            if i > 0:
                trans_type, trans_dur = self.select_motion_matched_transition(
                    scenes[i - 1], scene, default_transition_duration
                )
                transition_in = trans_type
                transition_in_duration = trans_dur

            # Determine transition out (to next segment)
            transition_out = TransitionType.CUT
            transition_out_duration = default_transition_duration
            if i < len(scenes) - 1:
                trans_type, trans_dur = self.select_motion_matched_transition(
                    scene, scenes[i + 1], default_transition_duration
                )
                transition_out = trans_type
                transition_out_duration = trans_dur
            else:
                # Last clip - fade out
                transition_out = TransitionType.FADE_BLACK
                transition_out_duration = 0.5

            # Use the longer of in/out durations for consistent look
            effective_duration = max(transition_in_duration, transition_out_duration)

            segment = ClipSegment(
                scene=scene,
                start_offset=center_offset,
                duration=duration,
                transition_in=transition_in,
                transition_out=transition_out,
                transition_duration=effective_duration,
            )
            segments.append(segment)

        return segments

    def get_video_info(self, video_path: Path) -> dict:
        """Get information about a video file."""
        clip = VideoFileClip(str(video_path))
        try:
            info = {
                "duration": clip.duration,
                "fps": clip.fps,
                "size": clip.size,
                "width": clip.w,
                "height": clip.h,
            }
        finally:
            clip.close()
        return info
