"""
Video processing and stitching with transitions.

Handles clip extraction, stitching, and applying various transitions
between clips using MoviePy.
"""

import gc
import os
import platform
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Callable, Optional

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

from drone_reel.core.scene_detector import EnhancedSceneInfo, MotionType, SceneInfo
from drone_reel.core.reframer import Reframer


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


@dataclass
class ClipSegment:
    """A segment of video to include in the final output."""

    scene: SceneInfo
    start_offset: float = 0.0
    duration: Optional[float] = None
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
        output_codec: Optional[str] = None,
        output_audio_codec: str = "aac",
        preset: str = "medium",
        threads: Optional[int] = None,
        video_bitrate: Optional[str] = None,
        audio_bitrate: str = "192k",
        stabilize: bool = False,
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
        """
        self.output_fps = output_fps
        self.output_codec = output_codec or self._detect_best_encoder()
        self.output_audio_codec = output_audio_codec
        self.preset = preset
        self.threads = threads or self._detect_cpu_cores()
        self.video_bitrate = video_bitrate or "15M"  # Default 15 Mbps for high quality
        self.audio_bitrate = audio_bitrate
        self.stabilize = stabilize
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
        target_size: Optional[tuple[int, int]] = None,
        reframer: Optional[Reframer] = None,
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

    def _extract_clip_parallel(
        self,
        segment: ClipSegment,
        target_size: Optional[tuple[int, int]],
        reframer: Optional[Reframer] = None,
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
        audio_path: Optional[Path] = None,
        target_size: Optional[tuple[int, int]] = None,
        progress_callback: Optional[Callable[[float], None]] = None,
        parallel_extraction: bool = True,
        reframer: Optional[Reframer] = None,
        reframers: Optional[list[Reframer]] = None,
        shake_scores: Optional[list[float]] = None,
        speed_ramps: Optional[list[list]] = None,
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
                                    if hasattr(c, '_source_clip_ref') and c._source_clip_ref:
                                        c._source_clip_ref.close()
                                    c.close()
                                except Exception:
                                    pass
                            raise RuntimeError(
                                f"Failed to extract clip {idx}: {str(e)}"
                            ) from e

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
                            smoothing_radius=15,
                            border_crop=0.04,
                            shake_score=clip_shake,
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
                        if hasattr(clip, '_source_clip_ref') and clip._source_clip_ref:
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

        # Build timeline with proper overlaps for crossfades
        composed_clips = []
        current_time = 0.0

        for i, clip in enumerate(clips):
            # Set the start time for this clip
            clip_with_start = clip.with_start(current_time)
            composed_clips.append(clip_with_start)

            # Calculate next clip start time based on transition type
            if i + 1 < len(clips):
                if i < len(segments) and segments[i].transition_out == TransitionType.CROSSFADE:
                    # For crossfade: overlap clips by transition duration
                    # Clamp overlap to max 40% of clip duration to prevent artifacts
                    overlap = min(segments[i].transition_duration, clip.duration * 0.4)
                    current_time += clip.duration - overlap
                else:
                    # For hard cuts: no overlap
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

    def _transition_cut(self, clip1: VideoFileClip, clip2: VideoFileClip, duration: float):
        """Simple cut transition (no effect)."""
        return concatenate_videoclips([clip1, clip2])

    def _transition_crossfade(
        self, clip1: VideoFileClip, clip2: VideoFileClip, duration: float
    ):
        """Crossfade transition between clips."""
        clip1 = clip1.with_effects([vfx.CrossFadeOut(duration)])
        clip2 = clip2.with_effects([vfx.CrossFadeIn(duration)])

        clip2 = clip2.with_start(clip1.duration - duration)

        return CompositeVideoClip([clip1, clip2])

    def _transition_fade_black(
        self, clip1: VideoFileClip, clip2: VideoFileClip, duration: float
    ):
        """Fade to black transition."""
        clip1 = clip1.with_effects([vfx.FadeOut(duration / 2)])
        clip2 = clip2.with_effects([vfx.FadeIn(duration / 2)])
        return concatenate_videoclips([clip1, clip2])

    def _transition_fade_white(
        self, clip1: VideoFileClip, clip2: VideoFileClip, duration: float
    ):
        """Fade to white transition."""
        clip1 = clip1.with_effects([vfx.FadeOut(duration / 2, final_color=(255, 255, 255))])
        clip2 = clip2.with_effects([vfx.FadeIn(duration / 2, initial_color=(255, 255, 255))])
        return concatenate_videoclips([clip1, clip2])

    def _transition_zoom_in(
        self, clip1: VideoFileClip, clip2: VideoFileClip, duration: float
    ):
        """Zoom in transition."""
        clip1 = self._zoom_transition(clip1, duration, zoom_in=True, is_start=False)
        return concatenate_videoclips([clip1, clip2])

    def _transition_zoom_out(
        self, clip1: VideoFileClip, clip2: VideoFileClip, duration: float
    ):
        """Zoom out transition."""
        clip2 = self._zoom_transition(clip2, duration, zoom_in=False, is_start=True)
        return concatenate_videoclips([clip1, clip2])

    def _transition_slide_left(
        self, clip1: VideoFileClip, clip2: VideoFileClip, duration: float
    ):
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
        transition = CompositeVideoClip([clip1_trimmed.subclipped(clip1.duration - duration), clip2_sliding], size=(w, h)).with_duration(duration)
        clip2_rest = clip2.subclipped(duration) if clip2.duration > duration else None

        if clip2_rest:
            return concatenate_videoclips([clip1.subclipped(0, clip1.duration - duration), transition, clip2_rest])
        return concatenate_videoclips([clip1.subclipped(0, clip1.duration - duration), transition])

    def _transition_slide_right(
        self, clip1: VideoFileClip, clip2: VideoFileClip, duration: float
    ):
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
        transition = CompositeVideoClip([clip1_trimmed.subclipped(clip1.duration - duration), clip2_sliding], size=(w, h)).with_duration(duration)
        clip2_rest = clip2.subclipped(duration) if clip2.duration > duration else None

        if clip2_rest:
            return concatenate_videoclips([clip1.subclipped(0, clip1.duration - duration), transition, clip2_rest])
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
        - Same direction, similar speed → Hard cut (seamless continuation)
        - Same direction, different speed → Quick crossfade (0.2s)
        - Different direction → Longer crossfade (0.4s)
        - Static scenes → Default crossfade (0.3s)

        Args:
            scene1: First scene (outgoing)
            scene2: Second scene (incoming)
            default_duration: Default transition duration

        Returns:
            Tuple of (TransitionType, duration)
        """
        # Check if scenes have enhanced motion info
        if not isinstance(scene1, EnhancedSceneInfo) or not isinstance(
            scene2, EnhancedSceneInfo
        ):
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

        # Check for horizontal pan motion - use slide transitions
        from drone_reel.core.scene_detector import MotionType

        # Scene1 panning right + Scene2 different → slide from right (SLIDE_LEFT)
        if isinstance(scene1, EnhancedSceneInfo) and scene1.motion_type == MotionType.PAN_RIGHT:
            return TransitionType.SLIDE_LEFT, 0.4

        # Scene1 panning left + Scene2 different → slide from left (SLIDE_RIGHT)
        if isinstance(scene1, EnhancedSceneInfo) and scene1.motion_type == MotionType.PAN_LEFT:
            return TransitionType.SLIDE_RIGHT, 0.4

        # Use zoom transitions for reveal/dramatic motion types
        if isinstance(scene2, EnhancedSceneInfo) and scene2.motion_type == MotionType.REVEAL:
            return TransitionType.ZOOM_IN, 0.3

        if isinstance(scene1, EnhancedSceneInfo) and scene1.motion_type in (
            MotionType.FLYOVER, MotionType.FPV
        ):
            return TransitionType.ZOOM_OUT, 0.3

        # Different motion directions - longer crossfade for smooth transition
        return TransitionType.CROSSFADE, 0.4

    def create_segments_from_scenes(
        self,
        scenes: list[SceneInfo],
        clip_durations: list[float],
        transitions: Optional[list[TransitionType]] = None,
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
