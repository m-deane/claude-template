"""
Video processing and stitching with transitions.

Handles clip extraction, stitching, and applying various transitions
between clips using MoviePy.
"""

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

from drone_reel.core.scene_detector import SceneInfo


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
        output_codec: str = "libx264",
        output_audio_codec: str = "aac",
        preset: str = "medium",
        threads: int = 4,
    ):
        """
        Initialize the video processor.

        Args:
            output_fps: Output video frame rate
            output_codec: Video codec for output
            output_audio_codec: Audio codec for output
            preset: FFmpeg encoding preset (ultrafast to veryslow)
            threads: Number of encoding threads
        """
        self.output_fps = output_fps
        self.output_codec = output_codec
        self.output_audio_codec = output_audio_codec
        self.preset = preset
        self.threads = threads
        self._transition_funcs: dict[TransitionType, Callable] = {
            TransitionType.CUT: self._transition_cut,
            TransitionType.CROSSFADE: self._transition_crossfade,
            TransitionType.FADE_BLACK: self._transition_fade_black,
            TransitionType.FADE_WHITE: self._transition_fade_white,
            TransitionType.ZOOM_IN: self._transition_zoom_in,
            TransitionType.ZOOM_OUT: self._transition_zoom_out,
        }

    def extract_clip(
        self,
        segment: ClipSegment,
        target_size: Optional[tuple[int, int]] = None,
    ) -> VideoFileClip:
        """
        Extract a clip segment from its source video.

        Args:
            segment: ClipSegment defining what to extract
            target_size: Optional (width, height) to resize to

        Returns:
            VideoFileClip of the extracted segment
        """
        clip = VideoFileClip(str(segment.scene.source_file))

        end_time = min(segment.effective_start + segment.effective_duration, clip.duration)
        subclip = clip.subclipped(segment.effective_start, end_time)

        if target_size:
            subclip = subclip.resized(target_size)

        return subclip

    def stitch_clips(
        self,
        segments: list[ClipSegment],
        output_path: Path,
        audio_path: Optional[Path] = None,
        target_size: Optional[tuple[int, int]] = None,
        progress_callback: Optional[Callable[[float], None]] = None,
    ) -> Path:
        """
        Stitch multiple clip segments into a single video.

        Args:
            segments: List of ClipSegment objects to combine
            output_path: Path for output video file
            audio_path: Optional music track to add
            target_size: Optional (width, height) for output
            progress_callback: Optional callback for progress updates

        Returns:
            Path to the output video file
        """
        if not segments:
            raise ValueError("No segments provided")

        clips = []
        total_segments = len(segments)

        for i, segment in enumerate(segments):
            clip = self.extract_clip(segment, target_size)

            if segment.transition_in != TransitionType.CUT:
                clip = self._apply_transition_in(
                    clip, segment.transition_in, segment.transition_duration
                )

            if segment.transition_out != TransitionType.CUT:
                clip = self._apply_transition_out(
                    clip, segment.transition_out, segment.transition_duration
                )

            clips.append(clip)

            if progress_callback:
                progress_callback((i + 1) / total_segments * 0.5)

        final_clip = self._concatenate_with_transitions(clips, segments)

        if audio_path:
            audio = AudioFileClip(str(audio_path))
            if audio.duration > final_clip.duration:
                audio = audio.subclipped(0, final_clip.duration)
            # Apply fade out to audio
            fade_duration = min(1.0, final_clip.duration * 0.1)
            audio = audio.with_effects([afx.AudioFadeOut(fade_duration)])
            final_clip = final_clip.with_audio(audio)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        final_clip.write_videofile(
            str(output_path),
            fps=self.output_fps,
            codec=self.output_codec,
            audio_codec=self.output_audio_codec,
            preset=self.preset,
            threads=self.threads,
            logger=None,
        )

        for clip in clips:
            clip.close()
        final_clip.close()

        if progress_callback:
            progress_callback(1.0)

        return output_path

    def _concatenate_with_transitions(
        self,
        clips: list[VideoFileClip],
        segments: list[ClipSegment],
    ) -> VideoFileClip:
        """Concatenate clips, handling crossfade transitions."""
        if len(clips) == 1:
            return clips[0]

        processed_clips = []
        for i, clip in enumerate(clips):
            if i < len(segments) and segments[i].transition_out == TransitionType.CROSSFADE:
                if i + 1 < len(clips):
                    processed_clips.append(clip)
                else:
                    processed_clips.append(clip)
            else:
                processed_clips.append(clip)

        return concatenate_videoclips(processed_clips, method="compose")

    def _apply_transition_in(
        self,
        clip: VideoFileClip,
        transition: TransitionType,
        duration: float,
    ) -> VideoFileClip:
        """Apply an entrance transition to a clip."""
        if transition == TransitionType.CROSSFADE:
            return clip.with_effects([vfx.CrossFadeIn(duration)])
        elif transition == TransitionType.FADE_BLACK:
            return clip.with_effects([vfx.FadeIn(duration)])
        elif transition == TransitionType.FADE_WHITE:
            return clip.with_effects([vfx.FadeIn(duration, initial_color=(255, 255, 255))])
        elif transition == TransitionType.ZOOM_IN:
            return self._zoom_transition(clip, duration, zoom_in=True, is_start=True)
        elif transition == TransitionType.ZOOM_OUT:
            return self._zoom_transition(clip, duration, zoom_in=False, is_start=True)
        return clip

    def _apply_transition_out(
        self,
        clip: VideoFileClip,
        transition: TransitionType,
        duration: float,
    ) -> VideoFileClip:
        """Apply an exit transition to a clip."""
        if transition == TransitionType.CROSSFADE:
            return clip.with_effects([vfx.CrossFadeOut(duration)])
        elif transition == TransitionType.FADE_BLACK:
            return clip.with_effects([vfx.FadeOut(duration)])
        elif transition == TransitionType.FADE_WHITE:
            return clip.with_effects([vfx.FadeOut(duration, final_color=(255, 255, 255))])
        elif transition == TransitionType.ZOOM_IN:
            return self._zoom_transition(clip, duration, zoom_in=True, is_start=False)
        elif transition == TransitionType.ZOOM_OUT:
            return self._zoom_transition(clip, duration, zoom_in=False, is_start=False)
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

    def get_video_info(self, video_path: Path) -> dict:
        """Get information about a video file."""
        clip = VideoFileClip(str(video_path))
        info = {
            "duration": clip.duration,
            "fps": clip.fps,
            "size": clip.size,
            "width": clip.w,
            "height": clip.h,
        }
        clip.close()
        return info
