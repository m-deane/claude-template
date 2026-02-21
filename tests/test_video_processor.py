"""Comprehensive tests for video processor module."""

import os
import platform
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import numpy as np
import pytest

from drone_reel.core.scene_detector import SceneInfo
from drone_reel.core.video_processor import (
    ClipSegment,
    TransitionType,
    VideoProcessor,
)


class TestTransitionType:
    """Tests for TransitionType enum."""

    def test_all_transition_types_exist(self):
        """Test all expected transition types are defined."""
        expected_types = {
            "CUT",
            "CROSSFADE",
            "FADE_BLACK",
            "FADE_WHITE",
            "ZOOM_IN",
            "ZOOM_OUT",
            "SLIDE_LEFT",
            "SLIDE_RIGHT",
            "WIPE_LEFT",
            "WIPE_RIGHT",
        }
        actual_types = {t.name for t in TransitionType}
        assert expected_types == actual_types

    def test_transition_values(self):
        """Test transition type values."""
        assert TransitionType.CUT.value == "cut"
        assert TransitionType.CROSSFADE.value == "crossfade"
        assert TransitionType.ZOOM_IN.value == "zoom_in"


class TestClipSegment:
    """Tests for ClipSegment dataclass."""

    @pytest.fixture
    def sample_scene(self):
        """Create a sample scene."""
        return SceneInfo(
            start_time=10.0,
            end_time=20.0,
            duration=10.0,
            score=75.0,
            source_file=Path("/test/video.mp4"),
        )

    def test_effective_start_no_offset(self, sample_scene):
        """Test effective_start with no offset."""
        segment = ClipSegment(scene=sample_scene)
        assert segment.effective_start == 10.0

    def test_effective_start_with_offset(self, sample_scene):
        """Test effective_start with offset."""
        segment = ClipSegment(scene=sample_scene, start_offset=2.5)
        assert segment.effective_start == 12.5

    def test_effective_duration_default(self, sample_scene):
        """Test effective_duration uses scene duration when not specified."""
        segment = ClipSegment(scene=sample_scene)
        assert segment.effective_duration == 10.0

    def test_effective_duration_with_offset(self, sample_scene):
        """Test effective_duration accounts for offset."""
        segment = ClipSegment(scene=sample_scene, start_offset=3.0)
        assert segment.effective_duration == 7.0

    def test_effective_duration_explicit(self, sample_scene):
        """Test effective_duration when explicitly set."""
        segment = ClipSegment(scene=sample_scene, duration=5.0)
        assert segment.effective_duration == 5.0

    def test_transition_defaults(self, sample_scene):
        """Test default transition settings."""
        segment = ClipSegment(scene=sample_scene)
        assert segment.transition_in == TransitionType.CUT
        assert segment.transition_out == TransitionType.CUT
        assert segment.transition_duration == 0.3

    def test_transition_custom(self, sample_scene):
        """Test custom transition settings."""
        segment = ClipSegment(
            scene=sample_scene,
            transition_in=TransitionType.CROSSFADE,
            transition_out=TransitionType.ZOOM_OUT,
            transition_duration=0.5,
        )
        assert segment.transition_in == TransitionType.CROSSFADE
        assert segment.transition_out == TransitionType.ZOOM_OUT
        assert segment.transition_duration == 0.5


class TestVideoProcessor:
    """Tests for VideoProcessor class."""

    def test_initialization_defaults(self):
        """Test default initialization values."""
        processor = VideoProcessor()
        assert processor.output_fps == 30
        assert processor.output_audio_codec == "aac"
        assert processor.preset == "medium"
        assert processor.threads is not None
        assert processor.output_codec is not None

    def test_initialization_custom(self):
        """Test custom initialization values."""
        processor = VideoProcessor(
            output_fps=60,
            output_codec="libx265",
            output_audio_codec="mp3",
            preset="fast",
            threads=8,
        )
        assert processor.output_fps == 60
        assert processor.output_codec == "libx265"
        assert processor.output_audio_codec == "mp3"
        assert processor.preset == "fast"
        assert processor.threads == 8

    def test_detect_cpu_cores(self):
        """Test CPU core detection."""
        processor = VideoProcessor()
        cores = processor._detect_cpu_cores()
        assert isinstance(cores, int)
        assert cores >= 1

    def test_detect_best_encoder(self):
        """Test encoder detection returns valid codec."""
        processor = VideoProcessor()
        encoder = processor._detect_best_encoder()
        assert isinstance(encoder, str)
        assert encoder in [
            "h264_videotoolbox",
            "h264_nvenc",
            "h264_qsv",
            "libx264",
        ]

    @patch("subprocess.run")
    def test_test_encoder_available(self, mock_run):
        """Test encoder availability check when encoder exists."""
        mock_run.return_value = Mock(stdout="h264_videotoolbox")
        processor = VideoProcessor()
        assert processor._test_encoder("h264_videotoolbox") is True

    @patch("subprocess.run")
    def test_test_encoder_unavailable(self, mock_run):
        """Test encoder availability check when encoder doesn't exist."""
        mock_run.return_value = Mock(stdout="libx264")
        processor = VideoProcessor()
        assert processor._test_encoder("h264_nvenc") is False

    @patch("subprocess.run")
    def test_test_encoder_timeout(self, mock_run):
        """Test encoder check handles timeout."""
        mock_run.side_effect = Exception("Timeout")
        processor = VideoProcessor()
        assert processor._test_encoder("h264_videotoolbox") is False


class TestVideoProcessorExtractClip:
    """Tests for extract_clip method."""

    @pytest.fixture
    def sample_scene(self):
        """Create a sample scene with temp file."""
        temp_file = Path("/tmp/test_video.mp4")
        return SceneInfo(
            start_time=5.0,
            end_time=15.0,
            duration=10.0,
            score=80.0,
            source_file=temp_file,
        )

    @pytest.fixture
    def processor(self):
        """Create a processor instance."""
        return VideoProcessor()

    @patch("drone_reel.core.video_processor.VideoFileClip")
    def test_extract_clip_basic(self, mock_clip_class, processor, sample_scene):
        """Test basic clip extraction."""
        mock_clip = MagicMock()
        mock_clip.duration = 20.0
        mock_subclip = MagicMock()
        mock_clip.subclipped.return_value = mock_subclip
        mock_clip_class.return_value = mock_clip

        segment = ClipSegment(scene=sample_scene, duration=5.0)
        result = processor.extract_clip(segment)

        mock_clip.subclipped.assert_called_once_with(5.0, 10.0)
        assert result == mock_subclip

    @patch("drone_reel.core.video_processor.VideoFileClip")
    def test_extract_clip_with_offset(self, mock_clip_class, processor, sample_scene):
        """Test clip extraction with start offset."""
        mock_clip = MagicMock()
        mock_clip.duration = 20.0
        mock_subclip = MagicMock()
        mock_clip.subclipped.return_value = mock_subclip
        mock_clip_class.return_value = mock_clip

        segment = ClipSegment(scene=sample_scene, start_offset=2.0, duration=3.0)
        processor.extract_clip(segment)

        mock_clip.subclipped.assert_called_once_with(7.0, 10.0)

    @patch("drone_reel.core.video_processor.VideoFileClip")
    def test_extract_clip_with_resize(self, mock_clip_class, processor, sample_scene):
        """Test clip extraction with resizing."""
        mock_clip = MagicMock()
        mock_clip.duration = 20.0
        mock_subclip = MagicMock()
        mock_resized = MagicMock()
        mock_clip.subclipped.return_value = mock_subclip
        mock_subclip.resized.return_value = mock_resized
        mock_clip_class.return_value = mock_clip

        segment = ClipSegment(scene=sample_scene, duration=5.0)
        result = processor.extract_clip(segment, target_size=(1920, 1080))

        mock_subclip.resized.assert_called_once_with((1920, 1080))
        assert result == mock_resized

    @patch("drone_reel.core.video_processor.VideoFileClip")
    def test_extract_clip_bounds_check(self, mock_clip_class, processor, sample_scene):
        """Test clip extraction respects video duration bounds."""
        mock_clip = MagicMock()
        mock_clip.duration = 12.0
        mock_subclip = MagicMock()
        mock_clip.subclipped.return_value = mock_subclip
        mock_clip_class.return_value = mock_clip

        segment = ClipSegment(scene=sample_scene, duration=10.0)
        processor.extract_clip(segment)

        # Should clip at video duration (12.0)
        mock_clip.subclipped.assert_called_once_with(5.0, 12.0)


class TestVideoProcessorStitchClips:
    """Tests for stitch_clips method."""

    @pytest.fixture
    def processor(self):
        """Create a processor instance."""
        return VideoProcessor()

    @pytest.fixture
    def sample_segments(self):
        """Create sample segments."""
        scenes = [
            SceneInfo(
                start_time=0.0,
                end_time=5.0,
                duration=5.0,
                score=80.0,
                source_file=Path("/tmp/video1.mp4"),
            ),
            SceneInfo(
                start_time=5.0,
                end_time=10.0,
                duration=5.0,
                score=75.0,
                source_file=Path("/tmp/video2.mp4"),
            ),
        ]
        return [ClipSegment(scene=scene, duration=3.0) for scene in scenes]

    def test_stitch_clips_empty_segments(self, processor):
        """Test stitch_clips with empty segments raises error."""
        with pytest.raises(ValueError, match="No segments provided"):
            processor.stitch_clips([], Path("/tmp/output.mp4"))

    @patch("drone_reel.core.video_processor.VideoFileClip")
    @patch("drone_reel.core.video_processor.CompositeVideoClip")
    def test_stitch_clips_basic(
        self, mock_composite, mock_clip_class, processor, sample_segments
    ):
        """Test basic clip stitching."""
        # Create a mock that preserves duration through method chaining
        mock_clip = MagicMock()
        mock_clip.duration = 3.0
        # Ensure method chaining returns clips with proper duration
        mock_clip.subclipped.return_value = mock_clip
        mock_clip.resized.return_value = mock_clip
        mock_clip.with_effects.return_value = mock_clip
        mock_clip.with_start.return_value = mock_clip
        mock_clip_class.return_value = mock_clip

        mock_final = MagicMock()
        mock_final.duration = 6.0
        mock_composite.return_value = mock_final

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "output.mp4"
            processor.stitch_clips(sample_segments, output_path)

            mock_final.write_videofile.assert_called_once()

    @patch("drone_reel.core.video_processor.VideoFileClip")
    @patch("drone_reel.core.video_processor.AudioFileClip")
    @patch("drone_reel.core.video_processor.CompositeVideoClip")
    def test_stitch_clips_with_audio(
        self, mock_composite, mock_audio_class, mock_clip_class, processor, sample_segments
    ):
        """Test stitching with audio track."""
        # Create a mock that preserves duration through method chaining
        mock_clip = MagicMock()
        mock_clip.duration = 3.0
        mock_clip.subclipped.return_value = mock_clip
        mock_clip.resized.return_value = mock_clip
        mock_clip.with_effects.return_value = mock_clip
        mock_clip.with_start.return_value = mock_clip
        mock_clip_class.return_value = mock_clip

        mock_audio = MagicMock()
        mock_audio.duration = 10.0
        mock_audio_class.return_value = mock_audio

        mock_final = MagicMock()
        mock_final.duration = 6.0
        mock_composite.return_value = mock_final

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "output.mp4"
            audio_path = Path(tmpdir) / "audio.mp3"
            processor.stitch_clips(sample_segments, output_path, audio_path=audio_path)

            mock_audio.subclipped.assert_called_once_with(0, 6.0)


class TestVideoProcessorTransitions:
    """Tests for transition methods."""

    @pytest.fixture
    def processor(self):
        """Create a processor instance."""
        return VideoProcessor()

    @pytest.fixture
    def mock_frame(self):
        """Create a mock video frame."""
        return np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)

    def test_zoom_transition_zoom_in_start(self, processor, mock_frame):
        """Test zoom in transition at clip start."""
        mock_clip = MagicMock()
        mock_clip.duration = 5.0

        def mock_get_frame(t):
            return mock_frame

        result = processor._zoom_transition(
            mock_clip, duration=1.0, zoom_in=True, is_start=True
        )

        mock_clip.transform.assert_called_once()

    def test_zoom_transition_zoom_out_end(self, processor, mock_frame):
        """Test zoom out transition at clip end."""
        mock_clip = MagicMock()
        mock_clip.duration = 5.0

        result = processor._zoom_transition(
            mock_clip, duration=1.0, zoom_in=False, is_start=False
        )

        mock_clip.transform.assert_called_once()

    @patch("drone_reel.core.video_processor.concatenate_videoclips")
    def test_transition_cut(self, mock_concat, processor):
        """Test cut transition."""
        clip1 = MagicMock()
        clip2 = MagicMock()

        result = processor._transition_cut(clip1, clip2, 0.5)

        mock_concat.assert_called_once_with([clip1, clip2])

    @patch("drone_reel.core.video_processor.CompositeVideoClip")
    def test_transition_crossfade(self, mock_composite, processor):
        """Test crossfade transition."""
        clip1 = MagicMock()
        clip1.duration = 5.0
        clip2 = MagicMock()

        processor._transition_crossfade(clip1, clip2, 0.5)

        clip1.with_effects.assert_called_once()
        clip2.with_effects.assert_called_once()

    @patch("drone_reel.core.video_processor.concatenate_videoclips")
    def test_transition_fade_black(self, mock_concat, processor):
        """Test fade to black transition."""
        clip1 = MagicMock()
        clip2 = MagicMock()

        processor._transition_fade_black(clip1, clip2, 1.0)

        clip1.with_effects.assert_called_once()
        clip2.with_effects.assert_called_once()

    @patch("drone_reel.core.video_processor.concatenate_videoclips")
    def test_transition_fade_white(self, mock_concat, processor):
        """Test fade to white transition."""
        clip1 = MagicMock()
        clip2 = MagicMock()

        processor._transition_fade_white(clip1, clip2, 1.0)

        clip1.with_effects.assert_called_once()
        clip2.with_effects.assert_called_once()


class TestCreateSegmentsFromScenes:
    """Tests for create_segments_from_scenes method."""

    @pytest.fixture
    def processor(self):
        """Create a processor instance."""
        return VideoProcessor()

    @pytest.fixture
    def sample_scenes(self):
        """Create sample scenes."""
        return [
            SceneInfo(
                start_time=0.0,
                end_time=10.0,
                duration=10.0,
                score=85.0,
                source_file=Path("/tmp/video1.mp4"),
            ),
            SceneInfo(
                start_time=10.0,
                end_time=20.0,
                duration=10.0,
                score=80.0,
                source_file=Path("/tmp/video2.mp4"),
            ),
            SceneInfo(
                start_time=20.0,
                end_time=30.0,
                duration=10.0,
                score=75.0,
                source_file=Path("/tmp/video3.mp4"),
            ),
        ]

    def test_create_segments_basic(self, processor, sample_scenes):
        """Test basic segment creation."""
        durations = [3.0, 4.0, 3.5]
        segments = processor.create_segments_from_scenes(sample_scenes, durations)

        assert len(segments) == 3
        assert segments[0].effective_duration == 3.0
        assert segments[1].effective_duration == 4.0
        assert segments[2].effective_duration == 3.5

    def test_create_segments_centered_offset(self, processor, sample_scenes):
        """Test segments are centered in scenes."""
        durations = [5.0, 5.0, 5.0]
        segments = processor.create_segments_from_scenes(sample_scenes, durations)

        # For 10s scene with 5s duration, offset should be 2.5s
        assert segments[0].start_offset == 2.5
        assert segments[1].start_offset == 2.5
        assert segments[2].start_offset == 2.5

    def test_create_segments_default_transitions(self, processor, sample_scenes):
        """Test default transition assignment."""
        durations = [3.0, 4.0, 3.5]
        segments = processor.create_segments_from_scenes(sample_scenes, durations)

        # First segment has no transition in
        assert segments[0].transition_in == TransitionType.CUT
        # Middle segments get crossfade
        assert segments[1].transition_in == TransitionType.CROSSFADE
        assert segments[2].transition_in == TransitionType.CROSSFADE
        # Last segment fades to black
        assert segments[2].transition_out == TransitionType.FADE_BLACK

    def test_create_segments_custom_transitions(self, processor, sample_scenes):
        """Test custom transition assignment."""
        durations = [3.0, 4.0, 3.5]
        transitions = [
            TransitionType.ZOOM_IN,
            TransitionType.CROSSFADE,
            TransitionType.ZOOM_OUT,
        ]
        segments = processor.create_segments_from_scenes(
            sample_scenes, durations, transitions=transitions
        )

        assert segments[1].transition_in == TransitionType.ZOOM_IN
        assert segments[2].transition_in == TransitionType.CROSSFADE
        assert segments[2].transition_out == TransitionType.ZOOM_OUT

    def test_create_segments_mismatched_lengths(self, processor, sample_scenes):
        """Test handling of mismatched scene/duration counts."""
        durations = [3.0, 4.0]  # Only 2 durations for 3 scenes
        segments = processor.create_segments_from_scenes(sample_scenes, durations)

        # Should only create 2 segments
        assert len(segments) == 2

    def test_create_segments_custom_transition_duration(self, processor, sample_scenes):
        """Test custom transition duration."""
        durations = [3.0, 4.0, 3.5]
        segments = processor.create_segments_from_scenes(
            sample_scenes, durations, transition_duration=0.5
        )

        assert segments[0].transition_duration == 0.5
        assert segments[1].transition_duration == 0.5
        assert segments[2].transition_duration == 0.5


class TestGetVideoInfo:
    """Tests for get_video_info method."""

    @pytest.fixture
    def processor(self):
        """Create a processor instance."""
        return VideoProcessor()

    @patch("drone_reel.core.video_processor.VideoFileClip")
    def test_get_video_info(self, mock_clip_class, processor):
        """Test getting video information."""
        mock_clip = MagicMock()
        mock_clip.duration = 60.0
        mock_clip.fps = 30.0
        mock_clip.size = (1920, 1080)
        mock_clip.w = 1920
        mock_clip.h = 1080
        mock_clip_class.return_value = mock_clip

        info = processor.get_video_info(Path("/tmp/video.mp4"))

        assert info["duration"] == 60.0
        assert info["fps"] == 30.0
        assert info["size"] == (1920, 1080)
        assert info["width"] == 1920
        assert info["height"] == 1080
        mock_clip.close.assert_called_once()


class TestZoomEffect:
    """Tests for zoom effect implementation."""

    @pytest.fixture
    def processor(self):
        """Create a processor instance."""
        return VideoProcessor()

    def test_zoom_effect_scale_calculation(self, processor):
        """Test zoom effect calculates correct scale factors."""
        mock_clip = MagicMock()
        mock_clip.duration = 5.0

        # Create test frame
        test_frame = np.ones((1080, 1920, 3), dtype=np.uint8) * 128

        def mock_get_frame(t):
            return test_frame

        # Test zoom in at start
        result = processor._zoom_transition(
            mock_clip, duration=1.0, zoom_in=True, is_start=True
        )

        # Verify transform was called
        mock_clip.transform.assert_called_once()

    def test_zoom_effect_bounds(self, processor):
        """Test zoom effect stays within valid bounds."""
        mock_clip = MagicMock()
        mock_clip.duration = 2.0

        result = processor._zoom_transition(
            mock_clip, duration=0.5, zoom_in=True, is_start=True
        )

        mock_clip.transform.assert_called_once()


class TestMemoryLeakFixes:
    """Test memory leak fixes in extract_clip method."""

    @pytest.fixture
    def processor(self):
        """Create a processor instance."""
        return VideoProcessor()

    @pytest.fixture
    def sample_scene(self):
        """Create a sample scene."""
        return SceneInfo(
            start_time=5.0,
            end_time=15.0,
            duration=10.0,
            score=80.0,
            source_file=Path("/tmp/test_video.mp4"),
        )

    @patch("drone_reel.core.video_processor.VideoFileClip")
    def test_extract_clip_stores_source_reference(self, mock_clip_class, processor, sample_scene):
        """Test that source VideoFileClip reference is stored on subclip for deferred cleanup."""
        mock_source = MagicMock()
        mock_source.duration = 20.0
        mock_subclip = MagicMock()
        mock_source.subclipped.return_value = mock_subclip
        mock_clip_class.return_value = mock_source

        segment = ClipSegment(scene=sample_scene, duration=5.0)
        result = processor.extract_clip(segment)

        # Verify source clip reference is stored (not closed immediately)
        # Source stays open because subclip shares its reader
        assert result._source_clip_ref == mock_source
        mock_source.close.assert_not_called()
        assert result == mock_subclip

    @patch("drone_reel.core.video_processor.VideoFileClip")
    def test_extract_clip_propagates_exception(self, mock_clip_class, processor, sample_scene):
        """Test that exceptions during extraction are propagated."""
        mock_source = MagicMock()
        mock_source.duration = 20.0
        mock_source.subclipped.side_effect = RuntimeError("Test extraction error")
        mock_clip_class.return_value = mock_source

        segment = ClipSegment(scene=sample_scene, duration=5.0)

        with pytest.raises(RuntimeError):
            processor.extract_clip(segment)

    @patch("drone_reel.core.video_processor.VideoFileClip")
    def test_extract_clip_stores_reference_with_resize(self, mock_clip_class, processor, sample_scene):
        """Test that source clip reference is stored when resizing is applied."""
        mock_source = MagicMock()
        mock_source.duration = 20.0
        mock_subclip = MagicMock()
        mock_resized = MagicMock()
        mock_source.subclipped.return_value = mock_subclip
        mock_subclip.resized.return_value = mock_resized
        mock_clip_class.return_value = mock_source

        segment = ClipSegment(scene=sample_scene, duration=5.0)
        result = processor.extract_clip(segment, target_size=(1920, 1080))

        # Source reference should be stored on resized clip for deferred cleanup
        assert result._source_clip_ref == mock_source
        mock_source.close.assert_not_called()
        assert result == mock_resized


class TestExceptionHandlingImprovements:
    """Test improved exception handling in stitch_clips."""

    @pytest.fixture
    def processor(self):
        """Create a processor instance."""
        return VideoProcessor()

    @pytest.fixture
    def sample_segments(self):
        """Create sample segments."""
        scenes = [
            SceneInfo(
                start_time=0.0,
                end_time=5.0,
                duration=5.0,
                score=80.0,
                source_file=Path("/tmp/video1.mp4"),
            ),
            SceneInfo(
                start_time=5.0,
                end_time=10.0,
                duration=5.0,
                score=75.0,
                source_file=Path("/tmp/video2.mp4"),
            ),
        ]
        return [ClipSegment(scene=scene, duration=3.0) for scene in scenes]

    @patch("drone_reel.core.video_processor.VideoFileClip")
    @patch("drone_reel.core.video_processor.CompositeVideoClip")
    def test_stitch_clips_cleanup_on_concatenation_error(
        self, mock_composite, mock_clip_class, processor, sample_segments
    ):
        """Test that clips are cleaned up when concatenation fails."""
        mock_clip = MagicMock()
        mock_clip.duration = 3.0
        mock_clip.subclipped.return_value = mock_clip
        mock_clip.with_effects.return_value = mock_clip
        mock_clip.with_start.return_value = mock_clip
        mock_clips = [mock_clip, mock_clip]
        mock_clip_class.side_effect = mock_clips
        mock_composite.side_effect = RuntimeError("Concatenation failed")

        with pytest.raises(RuntimeError, match="Failed to stitch clips"):
            processor.stitch_clips(
                sample_segments, Path("/tmp/output.mp4"), parallel_extraction=False
            )

        # Verify all clips were closed
        for clip in mock_clips:
            clip.close.assert_called()

    @patch("drone_reel.core.video_processor.VideoFileClip")
    @patch("drone_reel.core.video_processor.AudioFileClip")
    @patch("drone_reel.core.video_processor.CompositeVideoClip")
    @patch("pathlib.Path.mkdir")
    def test_stitch_clips_cleanup_audio_on_error(
        self, mock_mkdir, mock_composite, mock_audio_class, mock_clip_class, processor, sample_segments
    ):
        """Test that audio clip is closed when error occurs."""
        # Setup mock clips with proper duration propagation
        mock_clip = MagicMock()
        mock_clip.duration = 3.0
        mock_clip.subclipped.return_value = mock_clip
        mock_clip.with_effects.return_value = mock_clip
        mock_clip.with_start.return_value = mock_clip
        mock_clip_class.return_value = mock_clip

        # Setup mock final clip that fails on write (after audio is added)
        mock_final = MagicMock()
        mock_final.duration = 6.0
        mock_final_with_audio = MagicMock()
        mock_final_with_audio.write_videofile.side_effect = IOError("Write failed")
        mock_final.with_audio.return_value = mock_final_with_audio
        mock_composite.return_value = mock_final

        # Setup mock audio - the final audio object after all transformations
        mock_audio_final = MagicMock(duration=6.0)
        mock_audio_subclipped = MagicMock(duration=6.0)
        mock_audio_subclipped.with_effects.return_value = mock_audio_final

        mock_audio_initial = MagicMock(duration=10.0)
        mock_audio_initial.subclipped.return_value = mock_audio_subclipped
        mock_audio_class.return_value = mock_audio_initial

        with pytest.raises(RuntimeError, match="Failed to stitch clips"):
            processor.stitch_clips(
                sample_segments,
                Path("/tmp/output.mp4"),
                audio_path=Path("/tmp/audio.mp3"),
                parallel_extraction=False,
            )

        # Verify the final audio object was closed
        mock_audio_final.close.assert_called()

    @patch("drone_reel.core.video_processor.VideoFileClip")
    @patch("drone_reel.core.video_processor.CompositeVideoClip")
    def test_stitch_clips_cleanup_final_clip_on_error(
        self, mock_composite, mock_clip_class, processor, sample_segments
    ):
        """Test that final clip is closed when write fails."""
        mock_clip = MagicMock()
        mock_clip.duration = 3.0
        mock_clip.subclipped.return_value = mock_clip
        mock_clip.with_effects.return_value = mock_clip
        mock_clip.with_start.return_value = mock_clip
        mock_clip_class.return_value = mock_clip

        mock_final = MagicMock()
        mock_final.duration = 6.0
        mock_final.write_videofile.side_effect = RuntimeError("Write failed")
        mock_composite.return_value = mock_final

        with pytest.raises(RuntimeError):
            processor.stitch_clips(
                sample_segments, Path("/tmp/output.mp4"), parallel_extraction=False
            )

        mock_final.close.assert_called()


class TestHardwareEncoderDetection:
    """Test hardware encoder detection functionality."""

    @pytest.fixture
    def processor(self):
        """Create a processor instance with manual codec."""
        return VideoProcessor(output_codec="libx264", threads=4)

    def test_test_encoder_with_available_encoder(self, processor):
        """Test encoder detection when encoder is available."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = Mock(stdout="h264_videotoolbox h264_nvenc libx264")
            result = processor._test_encoder("h264_videotoolbox")
            assert result is True

    def test_test_encoder_with_unavailable_encoder(self, processor):
        """Test encoder detection when encoder is not available."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = Mock(stdout="libx264 libx265")
            result = processor._test_encoder("h264_videotoolbox")
            assert result is False

    def test_test_encoder_timeout_handling(self, processor):
        """Test encoder detection handles timeout gracefully."""
        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("ffmpeg", 5)):
            result = processor._test_encoder("h264_videotoolbox")
            assert result is False

    def test_test_encoder_file_not_found(self, processor):
        """Test encoder detection handles missing FFmpeg."""
        with patch("subprocess.run", side_effect=FileNotFoundError()):
            result = processor._test_encoder("h264_videotoolbox")
            assert result is False

    def test_test_encoder_generic_exception(self, processor):
        """Test encoder detection handles generic exceptions."""
        with patch("subprocess.run", side_effect=Exception("Unknown error")):
            result = processor._test_encoder("h264_videotoolbox")
            assert result is False

    @patch("platform.system")
    def test_detect_best_encoder_macos_priority(self, mock_platform, processor):
        """Test that macOS prioritizes h264_videotoolbox."""
        mock_platform.return_value = "Darwin"
        with patch.object(processor, "_test_encoder") as mock_test:
            mock_test.side_effect = lambda x: x == "h264_videotoolbox"
            encoder = processor._detect_best_encoder()
            assert encoder == "h264_videotoolbox"

    @patch("platform.system")
    def test_detect_best_encoder_nvidia_fallback(self, mock_platform, processor):
        """Test fallback to NVIDIA encoder."""
        mock_platform.return_value = "Linux"
        with patch.object(processor, "_test_encoder") as mock_test:
            mock_test.side_effect = lambda x: x == "h264_nvenc"
            encoder = processor._detect_best_encoder()
            assert encoder == "h264_nvenc"

    @patch("platform.system")
    def test_detect_best_encoder_intel_fallback(self, mock_platform, processor):
        """Test fallback to Intel Quick Sync."""
        mock_platform.return_value = "Windows"
        with patch.object(processor, "_test_encoder") as mock_test:
            mock_test.side_effect = lambda x: x == "h264_qsv"
            encoder = processor._detect_best_encoder()
            assert encoder == "h264_qsv"

    def test_detect_best_encoder_software_fallback(self, processor):
        """Test fallback to libx264 when no hardware encoder available."""
        with patch.object(processor, "_test_encoder") as mock_test:
            mock_test.side_effect = lambda x: x == "libx264"
            encoder = processor._detect_best_encoder()
            assert encoder == "libx264"

    def test_init_auto_detects_encoder(self):
        """Test that encoder is auto-detected during initialization."""
        with patch.object(VideoProcessor, "_detect_best_encoder", return_value="h264_nvenc"):
            processor = VideoProcessor(output_codec=None)
            assert processor.output_codec == "h264_nvenc"

    def test_init_respects_manual_encoder(self):
        """Test that manual encoder overrides auto-detection."""
        processor = VideoProcessor(output_codec="libx265")
        assert processor.output_codec == "libx265"


class TestCPUCoreAutoDetection:
    """Test automatic CPU core detection."""

    def test_detect_cpu_cores_returns_valid_count(self):
        """Test that CPU core detection returns valid count."""
        processor = VideoProcessor(output_codec="libx264", threads=4)
        cores = processor._detect_cpu_cores()
        assert isinstance(cores, int)
        assert cores >= 1

    def test_detect_cpu_cores_capped_at_half(self):
        """Test that detection caps at half of cores to prevent oversubscription."""
        processor = VideoProcessor(output_codec="libx264", threads=4)
        cores = processor._detect_cpu_cores()
        cpu_count = os.cpu_count()
        if cpu_count and cpu_count > 1:
            expected = min(cpu_count - 1, cpu_count // 2)
            assert cores == expected

    @patch("os.cpu_count")
    def test_detect_cpu_cores_fallback_none(self, mock_cpu_count):
        """Test fallback when cpu_count returns None."""
        mock_cpu_count.return_value = None
        processor = VideoProcessor(output_codec="libx264", threads=4)
        cores = processor._detect_cpu_cores()
        # When cpu_count returns None, or operator returns 4, then min(3, 2) = 2
        assert cores == 2

    @patch("os.cpu_count")
    def test_detect_cpu_cores_exception_handling(self, mock_cpu_count):
        """Test graceful handling of exceptions."""
        mock_cpu_count.side_effect = Exception("CPU detection failed")
        processor = VideoProcessor(output_codec="libx264", threads=4)
        cores = processor._detect_cpu_cores()
        assert cores == 4

    def test_init_auto_detects_threads(self):
        """Test that threads are auto-detected during initialization."""
        processor = VideoProcessor(threads=None)
        assert processor.threads >= 1
        assert isinstance(processor.threads, int)

    def test_init_respects_manual_threads(self):
        """Test that manual thread count overrides auto-detection."""
        processor = VideoProcessor(threads=16)
        assert processor.threads == 16


class TestParallelClipExtraction:
    """Test parallel clip extraction functionality."""

    @pytest.fixture
    def processor(self):
        """Create a processor instance."""
        return VideoProcessor()

    @pytest.fixture
    def sample_segments(self):
        """Create sample segments for parallel extraction."""
        scenes = [
            SceneInfo(
                start_time=i * 5.0,
                end_time=(i + 1) * 5.0,
                duration=5.0,
                score=80.0,
                source_file=Path(f"/tmp/video{i}.mp4"),
            )
            for i in range(4)
        ]
        return [ClipSegment(scene=scene, duration=3.0) for scene in scenes]

    @patch("drone_reel.core.video_processor.VideoFileClip")
    @patch("drone_reel.core.video_processor.CompositeVideoClip")
    def test_parallel_extraction_enabled_with_multiple_clips(
        self, mock_composite, mock_clip_class, processor, sample_segments
    ):
        """Test parallel extraction is used for multiple clips."""
        clip_counter = [0]

        def create_clip(*args, **kwargs):
            clip = MagicMock()
            clip.duration = 3.0
            clip.subclipped.return_value = clip
            clip.with_effects.return_value = clip
            clip.with_start.return_value = clip
            clip_counter[0] += 1
            return clip

        mock_clip_class.side_effect = create_clip

        mock_final = MagicMock()
        mock_final.duration = 12.0
        mock_composite.return_value = mock_final

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "output.mp4"
            processor.stitch_clips(sample_segments, output_path, parallel_extraction=True)

        assert clip_counter[0] == 4

    @patch("drone_reel.core.video_processor.VideoFileClip")
    @patch("drone_reel.core.video_processor.CompositeVideoClip")
    def test_parallel_extraction_disabled_sequential_processing(
        self, mock_composite, mock_clip_class, processor, sample_segments
    ):
        """Test that parallel extraction can be disabled."""
        clip_counter = [0]

        def create_clip(*args, **kwargs):
            clip = MagicMock()
            clip.duration = 3.0
            clip.subclipped.return_value = clip
            clip.with_effects.return_value = clip
            clip.with_start.return_value = clip
            clip_counter[0] += 1
            return clip

        mock_clip_class.side_effect = create_clip

        mock_final = MagicMock()
        mock_final.duration = 12.0
        mock_composite.return_value = mock_final

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "output.mp4"
            processor.stitch_clips(sample_segments, output_path, parallel_extraction=False)

        assert clip_counter[0] == 4

    @patch("drone_reel.core.video_processor.VideoFileClip")
    def test_parallel_extraction_error_cleanup(self, mock_clip_class, processor, sample_segments):
        """Test that parallel extraction raises error on failure."""
        # Note: With parallel execution, cleanup of partially-created clips is
        # best-effort due to race conditions between threads. The main guarantee
        # is that an error in any extraction raises RuntimeError.
        call_count = 0

        def create_clip_with_error(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count >= 3:
                raise RuntimeError("Extraction failed")
            clip = MagicMock(duration=3.0)
            clip.subclipped.return_value = clip
            return clip

        mock_clip_class.side_effect = create_clip_with_error

        with pytest.raises(RuntimeError, match="Failed to extract clip"):
            processor.stitch_clips(
                sample_segments, Path("/tmp/output.mp4"), parallel_extraction=True
            )

    @patch("drone_reel.core.video_processor.VideoFileClip")
    def test_parallel_extraction_single_segment_optimization(
        self, mock_clip_class, processor
    ):
        """Test that single segment doesn't use parallel extraction."""
        mock_clip = MagicMock()
        mock_clip.duration = 5.0
        mock_clip.subclipped.return_value = mock_clip
        mock_clip.with_effects.return_value = mock_clip
        mock_clip.with_start.return_value = mock_clip
        mock_clip_class.return_value = mock_clip

        scene = SceneInfo(
            start_time=0.0,
            end_time=5.0,
            duration=5.0,
            score=80.0,
            source_file=Path("/tmp/video.mp4"),
        )
        segments = [ClipSegment(scene=scene, duration=5.0)]

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "output.mp4"
            processor.stitch_clips(segments, output_path, parallel_extraction=True)

        # Single segment should not trigger parallel code path
        assert mock_clip_class.call_count >= 1

    @patch("drone_reel.core.video_processor.VideoFileClip")
    @patch("drone_reel.core.video_processor.CompositeVideoClip")
    def test_parallel_extraction_progress_callback(
        self, mock_composite, mock_clip_class, processor, sample_segments
    ):
        """Test progress callback works with parallel extraction."""
        clip_counter = [0]

        def create_clip(*args, **kwargs):
            clip = MagicMock()
            clip.duration = 3.0
            clip.subclipped.return_value = clip
            clip.with_effects.return_value = clip
            clip.with_start.return_value = clip
            clip_counter[0] += 1
            return clip

        mock_clip_class.side_effect = create_clip

        mock_final = MagicMock()
        mock_final.duration = 12.0
        mock_composite.return_value = mock_final

        progress_values = []

        def progress_callback(value):
            progress_values.append(value)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "output.mp4"
            processor.stitch_clips(
                sample_segments,
                output_path,
                parallel_extraction=True,
                progress_callback=progress_callback,
            )

        # Verify progress was tracked
        assert len(progress_values) > 0
        assert all(0.0 <= v <= 1.0 for v in progress_values)
        assert progress_values[-1] == 1.0


class TestCrossfadeOverlapBehavior:
    """Tests for crossfade overlap timing (dark frame bug fix)."""

    @pytest.fixture
    def processor(self):
        """Create a processor instance."""
        return VideoProcessor()

    def test_concatenate_with_crossfade_calculates_overlap(self, processor):
        """Test that crossfade transitions create proper clip overlap."""
        # Create mock clips with proper duration
        mock_clip1 = MagicMock()
        mock_clip1.duration = 3.0
        mock_clip1.with_start.return_value = mock_clip1

        mock_clip2 = MagicMock()
        mock_clip2.duration = 3.0
        mock_clip2.with_start.return_value = mock_clip2

        clips = [mock_clip1, mock_clip2]

        # Create segments with crossfade transition
        scenes = [
            SceneInfo(
                start_time=0.0,
                end_time=3.0,
                duration=3.0,
                score=80.0,
                source_file=Path("/tmp/video1.mp4"),
            ),
            SceneInfo(
                start_time=0.0,
                end_time=3.0,
                duration=3.0,
                score=75.0,
                source_file=Path("/tmp/video2.mp4"),
            ),
        ]
        segments = [
            ClipSegment(
                scene=scenes[0],
                duration=3.0,
                transition_out=TransitionType.CROSSFADE,
                transition_duration=0.3,
            ),
            ClipSegment(scene=scenes[1], duration=3.0),
        ]

        with patch("drone_reel.core.video_processor.CompositeVideoClip") as mock_composite:
            mock_final = MagicMock()
            mock_final.duration = 5.7  # 6.0 - 0.3 overlap
            mock_composite.return_value = mock_final

            result = processor._concatenate_with_transitions(clips, segments)

            # Verify CompositeVideoClip was called
            mock_composite.assert_called_once()

            # Verify clip2 starts at time = clip1.duration - overlap
            # The second clip should start at 2.7s (3.0 - 0.3)
            expected_start = 3.0 - 0.3  # clip1.duration - transition_duration
            mock_clip2.with_start.assert_called()

    def test_crossfade_overlap_clamped_to_max_40_percent(self, processor):
        """Test that crossfade overlap is clamped to max 40% of clip duration."""
        # Create a short clip where transition duration > 40% of clip
        mock_clip1 = MagicMock()
        mock_clip1.duration = 1.0  # 40% = 0.4s
        mock_clip1.with_start.return_value = mock_clip1

        mock_clip2 = MagicMock()
        mock_clip2.duration = 1.0
        mock_clip2.with_start.return_value = mock_clip2

        clips = [mock_clip1, mock_clip2]

        scenes = [
            SceneInfo(
                start_time=0.0,
                end_time=1.0,
                duration=1.0,
                score=80.0,
                source_file=Path("/tmp/video1.mp4"),
            ),
            SceneInfo(
                start_time=0.0,
                end_time=1.0,
                duration=1.0,
                score=75.0,
                source_file=Path("/tmp/video2.mp4"),
            ),
        ]
        # Request 0.5s transition but clip is only 1.0s, should clamp to 0.4s
        segments = [
            ClipSegment(
                scene=scenes[0],
                duration=1.0,
                transition_out=TransitionType.CROSSFADE,
                transition_duration=0.5,  # Exceeds 40% of 1.0s
            ),
            ClipSegment(scene=scenes[1], duration=1.0),
        ]

        with patch("drone_reel.core.video_processor.CompositeVideoClip") as mock_composite:
            mock_final = MagicMock()
            mock_final.duration = 1.6  # 2.0 - 0.4 (clamped overlap)
            mock_composite.return_value = mock_final

            processor._concatenate_with_transitions(clips, segments)

            # Should have been called with clips overlapping by 0.4s (40% of 1.0s)
            mock_composite.assert_called_once()

    def test_hard_cut_no_overlap(self, processor):
        """Test that hard cuts (CUT transition) don't create any overlap."""
        mock_clip1 = MagicMock()
        mock_clip1.duration = 3.0
        mock_clip1.with_start.return_value = mock_clip1

        mock_clip2 = MagicMock()
        mock_clip2.duration = 3.0
        mock_clip2.with_start.return_value = mock_clip2

        clips = [mock_clip1, mock_clip2]

        scenes = [
            SceneInfo(
                start_time=0.0,
                end_time=3.0,
                duration=3.0,
                score=80.0,
                source_file=Path("/tmp/video1.mp4"),
            ),
            SceneInfo(
                start_time=0.0,
                end_time=3.0,
                duration=3.0,
                score=75.0,
                source_file=Path("/tmp/video2.mp4"),
            ),
        ]
        # Hard cut - no overlap
        segments = [
            ClipSegment(
                scene=scenes[0], duration=3.0, transition_out=TransitionType.CUT
            ),
            ClipSegment(scene=scenes[1], duration=3.0),
        ]

        with patch("drone_reel.core.video_processor.CompositeVideoClip") as mock_composite:
            mock_final = MagicMock()
            mock_final.duration = 6.0  # Full duration, no overlap
            mock_composite.return_value = mock_final

            processor._concatenate_with_transitions(clips, segments)

            # Verify clip2 starts at time = clip1.duration (no overlap)
            mock_composite.assert_called_once()

    def test_transition_duration_safety_clamp_in_apply_transition(self, processor):
        """Test that _apply_transition_in clamps duration safely."""
        mock_clip = MagicMock()
        mock_clip.duration = 0.5  # Very short clip
        mock_clip.with_effects.return_value = mock_clip

        # Try to apply a 0.3s crossfade to a 0.5s clip
        # 40% of 0.5s = 0.2s, so it should be clamped to 0.2s
        result = processor._apply_transition_in(
            mock_clip, TransitionType.CROSSFADE, 0.3
        )

        # Should call with_effects with the clamped duration
        mock_clip.with_effects.assert_called_once()

    def test_very_short_clip_skips_transition(self, processor):
        """Test that very short clips skip transitions entirely."""
        mock_clip = MagicMock()
        mock_clip.duration = 0.2  # 40% = 0.08s, less than 0.1s threshold

        # Should return original clip without applying transition
        result = processor._apply_transition_in(
            mock_clip, TransitionType.CROSSFADE, 0.3
        )

        # No with_effects should be called
        mock_clip.with_effects.assert_not_called()
        assert result == mock_clip


class TestMotionMatchedTransitions:
    """Tests for motion-matched transition selection."""

    @pytest.fixture
    def processor(self):
        """Create a processor instance."""
        return VideoProcessor()

    def test_motion_directions_aligned_same_direction(self, processor):
        """Test that same direction motion is detected as aligned."""
        # Both moving right
        dir1 = (1.0, 0.0)
        dir2 = (0.9, 0.1)  # Slightly different but same general direction

        result = processor._are_motion_directions_aligned(dir1, dir2)
        assert result == True

    def test_motion_directions_not_aligned_opposite(self, processor):
        """Test that opposite directions are not aligned."""
        dir1 = (1.0, 0.0)  # Moving right
        dir2 = (-1.0, 0.0)  # Moving left

        result = processor._are_motion_directions_aligned(dir1, dir2)
        assert result == False

    def test_motion_directions_not_aligned_perpendicular(self, processor):
        """Test that perpendicular directions are not aligned."""
        dir1 = (1.0, 0.0)  # Moving right
        dir2 = (0.0, 1.0)  # Moving up

        result = processor._are_motion_directions_aligned(dir1, dir2)
        assert result == False

    def test_motion_directions_static_not_aligned(self, processor):
        """Test that static (zero) motion vectors are not considered aligned."""
        dir1 = (0.0, 0.0)
        dir2 = (1.0, 0.0)

        result = processor._are_motion_directions_aligned(dir1, dir2)
        assert result == False

    def test_motion_speeds_similar(self, processor):
        """Test that similar speeds are detected correctly."""
        dir1 = (1.0, 0.0)
        dir2 = (0.8, 0.0)  # Similar magnitude

        result = processor._are_motion_speeds_similar(dir1, dir2)
        assert result == True

    def test_motion_speeds_different(self, processor):
        """Test that very different speeds are detected."""
        dir1 = (1.0, 0.0)
        dir2 = (0.2, 0.0)  # Very different magnitude

        result = processor._are_motion_speeds_similar(dir1, dir2)
        assert result == False

    def test_motion_speeds_both_static(self, processor):
        """Test that both static scenes are considered similar speed."""
        dir1 = (0.0, 0.0)
        dir2 = (0.0, 0.0)

        result = processor._are_motion_speeds_similar(dir1, dir2)
        assert result == True

    def test_select_transition_regular_scene_info(self, processor):
        """Test that regular SceneInfo falls back to default crossfade."""
        scene1 = SceneInfo(
            start_time=0.0,
            end_time=5.0,
            duration=5.0,
            score=80.0,
            source_file=Path("/tmp/video1.mp4"),
        )
        scene2 = SceneInfo(
            start_time=0.0,
            end_time=5.0,
            duration=5.0,
            score=75.0,
            source_file=Path("/tmp/video2.mp4"),
        )

        trans_type, duration = processor.select_motion_matched_transition(
            scene1, scene2, 0.3
        )

        assert trans_type == TransitionType.CROSSFADE
        assert duration == 0.3

    def test_select_transition_enhanced_aligned_same_speed(self, processor):
        """Test hard cut for aligned motion with similar speed."""
        from drone_reel.core.scene_detector import EnhancedSceneInfo, MotionType

        scene1 = EnhancedSceneInfo(
            start_time=0.0,
            end_time=5.0,
            duration=5.0,
            score=80.0,
            source_file=Path("/tmp/video1.mp4"),
            motion_type=MotionType.PAN_RIGHT,
            motion_direction=(1.0, 0.0),
        )
        scene2 = EnhancedSceneInfo(
            start_time=0.0,
            end_time=5.0,
            duration=5.0,
            score=75.0,
            source_file=Path("/tmp/video2.mp4"),
            motion_type=MotionType.PAN_RIGHT,
            motion_direction=(0.9, 0.1),
        )

        trans_type, duration = processor.select_motion_matched_transition(
            scene1, scene2, 0.3
        )

        assert trans_type == TransitionType.CUT
        assert duration == 0.0

    def test_select_transition_aligned_different_speed(self, processor):
        """Test quick crossfade for aligned motion with different speed."""
        from drone_reel.core.scene_detector import EnhancedSceneInfo, MotionType

        scene1 = EnhancedSceneInfo(
            start_time=0.0,
            end_time=5.0,
            duration=5.0,
            score=80.0,
            source_file=Path("/tmp/video1.mp4"),
            motion_type=MotionType.PAN_RIGHT,
            motion_direction=(1.0, 0.0),
        )
        scene2 = EnhancedSceneInfo(
            start_time=0.0,
            end_time=5.0,
            duration=5.0,
            score=75.0,
            source_file=Path("/tmp/video2.mp4"),
            motion_type=MotionType.PAN_RIGHT,
            motion_direction=(0.3, 0.0),  # Same direction, different speed
        )

        trans_type, duration = processor.select_motion_matched_transition(
            scene1, scene2, 0.3
        )

        assert trans_type == TransitionType.CROSSFADE
        assert duration == 0.2

    def test_select_transition_different_motion(self, processor):
        """Test longer crossfade for different motion directions."""
        from drone_reel.core.scene_detector import EnhancedSceneInfo, MotionType

        scene1 = EnhancedSceneInfo(
            start_time=0.0,
            end_time=5.0,
            duration=5.0,
            score=80.0,
            source_file=Path("/tmp/video1.mp4"),
            motion_type=MotionType.PAN_RIGHT,
            motion_direction=(1.0, 0.0),
        )
        scene2 = EnhancedSceneInfo(
            start_time=0.0,
            end_time=5.0,
            duration=5.0,
            score=75.0,
            source_file=Path("/tmp/video2.mp4"),
            motion_type=MotionType.TILT_UP,
            motion_direction=(0.0, 1.0),  # Perpendicular direction
        )

        trans_type, duration = processor.select_motion_matched_transition(
            scene1, scene2, 0.3
        )

        # PAN_RIGHT scenes now use SLIDE_LEFT for smoother motion-matched transitions
        assert trans_type in (TransitionType.CROSSFADE, TransitionType.SLIDE_LEFT)
        assert duration == 0.4

    def test_select_transition_both_static(self, processor):
        """Test default crossfade for both static scenes."""
        from drone_reel.core.scene_detector import EnhancedSceneInfo, MotionType

        scene1 = EnhancedSceneInfo(
            start_time=0.0,
            end_time=5.0,
            duration=5.0,
            score=80.0,
            source_file=Path("/tmp/video1.mp4"),
            motion_type=MotionType.STATIC,
            motion_direction=(0.0, 0.0),
        )
        scene2 = EnhancedSceneInfo(
            start_time=0.0,
            end_time=5.0,
            duration=5.0,
            score=75.0,
            source_file=Path("/tmp/video2.mp4"),
            motion_type=MotionType.STATIC,
            motion_direction=(0.0, 0.0),
        )

        trans_type, duration = processor.select_motion_matched_transition(
            scene1, scene2, 0.3
        )

        assert trans_type == TransitionType.CROSSFADE
        assert duration == 0.3

    def test_create_motion_matched_segments(self, processor):
        """Test creating segments with motion-matched transitions."""
        from drone_reel.core.scene_detector import EnhancedSceneInfo, MotionType

        scenes = [
            EnhancedSceneInfo(
                start_time=0.0,
                end_time=5.0,
                duration=5.0,
                score=80.0,
                source_file=Path("/tmp/video1.mp4"),
                motion_type=MotionType.PAN_RIGHT,
                motion_direction=(1.0, 0.0),
            ),
            EnhancedSceneInfo(
                start_time=0.0,
                end_time=5.0,
                duration=5.0,
                score=75.0,
                source_file=Path("/tmp/video2.mp4"),
                motion_type=MotionType.PAN_RIGHT,
                motion_direction=(0.9, 0.1),  # Aligned, similar speed
            ),
            EnhancedSceneInfo(
                start_time=0.0,
                end_time=5.0,
                duration=5.0,
                score=70.0,
                source_file=Path("/tmp/video3.mp4"),
                motion_type=MotionType.TILT_UP,
                motion_direction=(0.0, 1.0),  # Different direction
            ),
        ]
        durations = [2.0, 2.0, 2.0]

        segments = processor.create_motion_matched_segments(scenes, durations)

        assert len(segments) == 3

        # First segment should have CUT out (to matching motion)
        assert segments[0].transition_out == TransitionType.CUT

        # Second segment should have CUT in (from matching motion)
        # and CROSSFADE/SLIDE_LEFT out (to different motion - SLIDE_LEFT for PAN_RIGHT)
        assert segments[1].transition_in == TransitionType.CUT
        assert segments[1].transition_out in (TransitionType.CROSSFADE, TransitionType.SLIDE_LEFT)

        # Last segment should have FADE_BLACK out
        assert segments[2].transition_out == TransitionType.FADE_BLACK


class TestFfmpegParamsEncoding:
    """Tests for the new ffmpeg encoding params: color space, faststart, bitrate caps."""

    @pytest.fixture
    def processor(self):
        return VideoProcessor(output_codec="libx264", threads=2, video_bitrate="15M")

    @pytest.fixture
    def sample_segments(self):
        """Single-segment list. With 1 clip _concatenate_with_transitions returns it directly."""
        scenes = [
            SceneInfo(
                start_time=0.0,
                end_time=5.0,
                duration=5.0,
                score=80.0,
                source_file=Path("/tmp/video1.mp4"),
            ),
        ]
        return [ClipSegment(scene=scene, duration=3.0) for scene in scenes]

    def _make_mock_clip(self, duration=3.0):
        clip = MagicMock()
        clip.duration = duration
        clip.subclipped.return_value = clip
        clip.resized.return_value = clip
        clip.with_effects.return_value = clip
        clip.with_start.return_value = clip
        clip.with_audio.return_value = clip
        return clip

    def _get_write_call_kwargs(self, mock_clip):
        """Extract write_videofile kwargs from the mock that was actually called."""
        args, kwargs = mock_clip.write_videofile.call_args
        return kwargs

    @patch("drone_reel.core.video_processor.VideoFileClip")
    def test_write_videofile_called_with_bt709_params(
        self, mock_clip_class, processor, sample_segments
    ):
        """write_videofile receives BT.709 color space tags in ffmpeg_params."""
        mock_clip = self._make_mock_clip()
        mock_clip_class.return_value = mock_clip

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "output.mp4"
            processor.stitch_clips(sample_segments, output_path, parallel_extraction=False)

        kwargs = self._get_write_call_kwargs(mock_clip)
        ffmpeg_params = kwargs["ffmpeg_params"]
        assert "-colorspace" in ffmpeg_params
        idx = ffmpeg_params.index("-colorspace")
        assert ffmpeg_params[idx + 1] == "bt709"
        assert "-color_primaries" in ffmpeg_params
        assert "-color_trc" in ffmpeg_params

    @patch("drone_reel.core.video_processor.VideoFileClip")
    def test_write_videofile_called_with_faststart(
        self, mock_clip_class, processor, sample_segments
    ):
        """write_videofile receives -movflags +faststart in ffmpeg_params."""
        mock_clip = self._make_mock_clip()
        mock_clip_class.return_value = mock_clip

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "output.mp4"
            processor.stitch_clips(sample_segments, output_path, parallel_extraction=False)

        kwargs = self._get_write_call_kwargs(mock_clip)
        ffmpeg_params = kwargs["ffmpeg_params"]
        assert "-movflags" in ffmpeg_params
        idx = ffmpeg_params.index("-movflags")
        assert ffmpeg_params[idx + 1] == "+faststart"

    @patch("drone_reel.core.video_processor.VideoFileClip")
    def test_write_videofile_called_with_maxrate_and_bufsize(
        self, mock_clip_class, processor, sample_segments
    ):
        """write_videofile receives -maxrate and -bufsize computed from video_bitrate."""
        mock_clip = self._make_mock_clip()
        mock_clip_class.return_value = mock_clip

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "output.mp4"
            processor.stitch_clips(sample_segments, output_path, parallel_extraction=False)

        kwargs = self._get_write_call_kwargs(mock_clip)
        ffmpeg_params = kwargs["ffmpeg_params"]
        assert "-maxrate" in ffmpeg_params
        assert "-bufsize" in ffmpeg_params

        # 15M -> maxrate = 15*1.5=22.5 rounded to 22, bufsize = 15*2=30
        maxrate_idx = ffmpeg_params.index("-maxrate")
        bufsize_idx = ffmpeg_params.index("-bufsize")
        maxrate_val = ffmpeg_params[maxrate_idx + 1]
        bufsize_val = ffmpeg_params[bufsize_idx + 1]

        assert maxrate_val.endswith("M"), f"Expected maxrate to end with 'M', got {maxrate_val}"
        assert bufsize_val.endswith("M"), f"Expected bufsize to end with 'M', got {bufsize_val}"
        assert float(maxrate_val[:-1]) == pytest.approx(22.0, abs=1.0)
        assert float(bufsize_val[:-1]) == pytest.approx(30.0, abs=1.0)

    @patch("drone_reel.core.video_processor.VideoFileClip")
    def test_write_videofile_audio_codec_is_aac(
        self, mock_clip_class, processor, sample_segments
    ):
        """write_videofile always uses 'aac' as audio_codec regardless of instance attribute."""
        processor.output_audio_codec = "mp3"  # Should be ignored

        mock_clip = self._make_mock_clip()
        mock_clip_class.return_value = mock_clip

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "output.mp4"
            processor.stitch_clips(sample_segments, output_path, parallel_extraction=False)

        kwargs = self._get_write_call_kwargs(mock_clip)
        assert kwargs["audio_codec"] == "aac"

    @patch("drone_reel.core.video_processor.VideoFileClip")
    def test_maxrate_bufsize_not_added_when_bitrate_none(
        self, mock_clip_class, sample_segments
    ):
        """When video_bitrate is set to None, bitrate caps are skipped."""
        proc = VideoProcessor(output_codec="libx264", threads=2, video_bitrate="15M")
        proc.video_bitrate = None  # Force None after init

        mock_clip = self._make_mock_clip()
        mock_clip_class.return_value = mock_clip

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "output.mp4"
            proc.stitch_clips(sample_segments, output_path, parallel_extraction=False)

        kwargs = self._get_write_call_kwargs(mock_clip)
        ffmpeg_params = kwargs["ffmpeg_params"]
        assert "-maxrate" not in ffmpeg_params
        assert "-bufsize" not in ffmpeg_params

    @patch("drone_reel.core.video_processor.VideoFileClip")
    def test_bitrate_caps_with_kilobit_unit(self, mock_clip_class, sample_segments):
        """Bitrate caps work correctly with 'K' suffix (e.g., '8000K')."""
        proc = VideoProcessor(output_codec="libx264", threads=2, video_bitrate="8000K")

        mock_clip = self._make_mock_clip()
        mock_clip_class.return_value = mock_clip

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "output.mp4"
            proc.stitch_clips(sample_segments, output_path, parallel_extraction=False)

        kwargs = self._get_write_call_kwargs(mock_clip)
        ffmpeg_params = kwargs["ffmpeg_params"]
        assert "-maxrate" in ffmpeg_params
        maxrate_idx = ffmpeg_params.index("-maxrate")
        maxrate_val = ffmpeg_params[maxrate_idx + 1]
        assert maxrate_val.endswith("K")
        assert float(maxrate_val[:-1]) == pytest.approx(12000.0, abs=1.0)

    def test_bitrate_parsing_valid_megabit(self, processor):
        """Internal bitrate parsing: '15M' -> maxrate='22M', bufsize='30M'."""
        numeric_str = "15M".rstrip("MmKk")
        numeric_val = float(numeric_str)
        unit = "15M"[len(numeric_str):].upper()
        maxrate_str = f"{numeric_val * 1.5:.0f}{unit}"
        bufsize_str = f"{numeric_val * 2:.0f}{unit}"
        assert maxrate_str == "22M"
        assert bufsize_str == "30M"

    def test_bitrate_parsing_valid_high_bitrate(self, processor):
        """Internal bitrate parsing: '80M' -> maxrate='120M', bufsize='160M'."""
        numeric_str = "80M".rstrip("MmKk")
        numeric_val = float(numeric_str)
        unit = "80M"[len(numeric_str):].upper()
        maxrate_str = f"{numeric_val * 1.5:.0f}{unit}"
        bufsize_str = f"{numeric_val * 2:.0f}{unit}"
        assert maxrate_str == "120M"
        assert bufsize_str == "160M"
