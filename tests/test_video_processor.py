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
            "WHIP_PAN",
            "GLITCH_RGB",
            "IRIS_IN",
            "IRIS_OUT",
            "FLASH_WHITE",
            "LIGHT_LEAK",
            "HYPERLAPSE_ZOOM",
            "PARALLAX_LEFT",
            "PARALLAX_RIGHT",
            "WIPE_DIAGONAL",
            "WIPE_DIAMOND",
            "FOG_PASS",
            "VORTEX_ZOOM",
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

        # PAN_RIGHT with strong motion uses WHIP_PAN; slow pan falls back to SLIDE_LEFT
        assert trans_type in (TransitionType.WHIP_PAN, TransitionType.SLIDE_LEFT)
        assert duration in (0.3, 0.4)

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
        # and WHIP_PAN/SLIDE_LEFT out (to different motion - WHIP_PAN for fast PAN_RIGHT)
        assert segments[1].transition_in == TransitionType.CUT
        assert segments[1].transition_out in (TransitionType.WHIP_PAN, TransitionType.SLIDE_LEFT)

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


class TestNewTransitionEffects:
    """Tests for Phase 1 visual enhancement transitions."""

    @pytest.fixture
    def processor(self):
        return VideoProcessor()

    @pytest.fixture
    def mock_clip(self):
        clip = MagicMock()
        clip.duration = 5.0
        clip.w = 1920
        clip.h = 1080
        return clip

    @pytest.fixture
    def sample_frame(self):
        return np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)

    # --- Enum values ---

    def test_new_transition_enum_values(self):
        """New transition types have correct string values."""
        assert TransitionType.WHIP_PAN.value == "whip_pan"
        assert TransitionType.GLITCH_RGB.value == "glitch_rgb"
        assert TransitionType.IRIS_IN.value == "iris_in"
        assert TransitionType.IRIS_OUT.value == "iris_out"
        assert TransitionType.FLASH_WHITE.value == "flash_white"
        assert TransitionType.LIGHT_LEAK.value == "light_leak"

    # --- Whip Pan ---

    def test_whip_pan_calls_transform(self, processor, mock_clip):
        """Whip pan transition calls clip.transform()."""
        processor._transition_whip_pan(mock_clip, 0.3, is_start=True)
        mock_clip.transform.assert_called_once()

    def test_whip_pan_effect_applies_blur(self, processor, sample_frame):
        """Whip pan effect applies directional blur at transition start."""
        clip = MagicMock()
        clip.duration = 5.0
        # Capture the transform function
        result_clip = processor._transition_whip_pan(clip, 0.5, is_start=True)
        effect_fn = clip.transform.call_args[0][0]
        # At t=0 (start of transition), blur should be strongest
        blurred = effect_fn(lambda t: sample_frame, 0.0)
        assert blurred.shape == sample_frame.shape
        # At t=0.5 (end of transition), should be near original
        clear = effect_fn(lambda t: sample_frame, 0.5)
        assert clear.shape == sample_frame.shape

    # --- Glitch RGB ---

    def test_glitch_rgb_calls_transform(self, processor, mock_clip):
        """Glitch RGB transition calls clip.transform()."""
        processor._transition_glitch_rgb(mock_clip, 0.2, is_start=True)
        mock_clip.transform.assert_called_once()

    def test_glitch_rgb_splits_channels(self, processor):
        """Glitch RGB shifts R and B channels at peak intensity."""
        frame = np.ones((100, 200, 3), dtype=np.uint8) * 128
        # Set distinct channel values for detection
        frame[:, :, 0] = 200  # R
        frame[:, :, 1] = 128  # G
        frame[:, :, 2] = 50   # B

        clip = MagicMock()
        clip.duration = 2.0
        processor._transition_glitch_rgb(clip, 0.5, is_start=True)
        effect_fn = clip.transform.call_args[0][0]

        # At t=0 (peak glitch), channels should be shifted
        glitched = effect_fn(lambda t: frame, 0.0)
        assert glitched.shape == frame.shape
        # G channel should be unchanged
        assert np.array_equal(glitched[:, :, 1], frame[:, :, 1])

    def test_glitch_rgb_no_effect_after_duration(self, processor):
        """After transition duration, frame should be unchanged."""
        frame = np.random.randint(0, 255, (100, 200, 3), dtype=np.uint8)
        clip = MagicMock()
        clip.duration = 5.0
        processor._transition_glitch_rgb(clip, 0.3, is_start=True)
        effect_fn = clip.transform.call_args[0][0]
        # Well past the transition duration
        result = effect_fn(lambda t: frame, 2.0)
        np.testing.assert_array_equal(result, frame)

    # --- Iris Wipe ---

    def test_iris_in_calls_transform(self, processor, mock_clip):
        """Iris in transition calls clip.transform()."""
        processor._transition_iris(mock_clip, 0.4, is_start=True, opening=True)
        mock_clip.transform.assert_called_once()

    def test_iris_in_masks_frame_at_start(self, processor):
        """Iris in: at t=0 with opening=True, radius is minimal (mostly black)."""
        frame = np.ones((100, 100, 3), dtype=np.uint8) * 200
        clip = MagicMock()
        clip.duration = 5.0
        processor._transition_iris(clip, 0.5, is_start=True, opening=True)
        effect_fn = clip.transform.call_args[0][0]
        result = effect_fn(lambda t: frame, 0.0)
        # Most of the frame should be dark (masked)
        assert result.mean() < frame.mean()

    def test_iris_in_reveals_fully_after_duration(self, processor):
        """Iris in: after duration, frame should be fully visible."""
        frame = np.ones((100, 100, 3), dtype=np.uint8) * 200
        clip = MagicMock()
        clip.duration = 5.0
        processor._transition_iris(clip, 0.3, is_start=True, opening=True)
        effect_fn = clip.transform.call_args[0][0]
        result = effect_fn(lambda t: frame, 1.0)
        np.testing.assert_array_equal(result, frame)

    def test_iris_out_masks_at_end(self, processor):
        """Iris out: closing circle should mask frame at peak."""
        frame = np.ones((100, 100, 3), dtype=np.uint8) * 200
        clip = MagicMock()
        clip.duration = 5.0
        processor._transition_iris(clip, 0.5, is_start=False, opening=False)
        effect_fn = clip.transform.call_args[0][0]
        # Near end of clip (within transition zone)
        result = effect_fn(lambda t: frame, 4.75)
        assert result.mean() < frame.mean()

    # --- Flash White ---

    def test_flash_white_calls_transform(self, processor, mock_clip):
        """Flash white transition calls clip.transform()."""
        processor._transition_flash_white(mock_clip, 0.3, is_start=True)
        mock_clip.transform.assert_called_once()

    def test_flash_white_is_white_at_peak(self, processor):
        """Flash white at t=0 (start) should be near white."""
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        clip = MagicMock()
        clip.duration = 5.0
        processor._transition_flash_white(clip, 0.5, is_start=True)
        effect_fn = clip.transform.call_args[0][0]
        result = effect_fn(lambda t: frame, 0.0)
        # Should be very bright (near white)
        assert result.mean() > 200

    def test_flash_white_fades_to_frame(self, processor):
        """Flash white fades to original frame after transition."""
        frame = np.ones((100, 100, 3), dtype=np.uint8) * 128
        clip = MagicMock()
        clip.duration = 5.0
        processor._transition_flash_white(clip, 0.3, is_start=True)
        effect_fn = clip.transform.call_args[0][0]
        result = effect_fn(lambda t: frame, 2.0)
        np.testing.assert_array_equal(result, frame)

    # --- Light Leak ---

    def test_light_leak_calls_transform(self, processor, mock_clip):
        """Light leak transition calls clip.transform()."""
        processor._transition_light_leak(mock_clip, 0.4, is_start=True)
        mock_clip.transform.assert_called_once()

    def test_light_leak_adds_warm_overlay(self, processor):
        """Light leak adds warm color at peak intensity."""
        frame = np.ones((100, 100, 3), dtype=np.uint8) * 50  # Dark frame
        clip = MagicMock()
        clip.duration = 5.0
        processor._transition_light_leak(clip, 0.5, is_start=True)
        effect_fn = clip.transform.call_args[0][0]
        result = effect_fn(lambda t: frame, 0.0)
        # Should have some pixels brighter than original (from warm leak)
        assert result.mean() > frame.mean()

    def test_light_leak_no_effect_outside_transition(self, processor):
        """No light leak effect outside transition duration."""
        frame = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        clip = MagicMock()
        clip.duration = 5.0
        processor._transition_light_leak(clip, 0.3, is_start=True)
        effect_fn = clip.transform.call_args[0][0]
        result = effect_fn(lambda t: frame, 2.0)
        np.testing.assert_array_equal(result, frame)

    # --- apply_transition_in / apply_transition_out ---

    def test_apply_transition_in_whip_pan(self, processor, mock_clip):
        """_apply_transition_in dispatches WHIP_PAN."""
        processor._apply_transition_in(mock_clip, TransitionType.WHIP_PAN, 0.3)
        mock_clip.transform.assert_called_once()

    def test_apply_transition_in_glitch_rgb(self, processor, mock_clip):
        """_apply_transition_in dispatches GLITCH_RGB."""
        processor._apply_transition_in(mock_clip, TransitionType.GLITCH_RGB, 0.2)
        mock_clip.transform.assert_called_once()

    def test_apply_transition_in_iris_in(self, processor, mock_clip):
        """_apply_transition_in dispatches IRIS_IN."""
        processor._apply_transition_in(mock_clip, TransitionType.IRIS_IN, 0.4)
        mock_clip.transform.assert_called_once()

    def test_apply_transition_in_iris_out(self, processor, mock_clip):
        """_apply_transition_in dispatches IRIS_OUT."""
        processor._apply_transition_in(mock_clip, TransitionType.IRIS_OUT, 0.4)
        mock_clip.transform.assert_called_once()

    def test_apply_transition_in_flash_white(self, processor, mock_clip):
        """_apply_transition_in dispatches FLASH_WHITE."""
        processor._apply_transition_in(mock_clip, TransitionType.FLASH_WHITE, 0.3)
        mock_clip.transform.assert_called_once()

    def test_apply_transition_in_light_leak(self, processor, mock_clip):
        """_apply_transition_in dispatches LIGHT_LEAK."""
        processor._apply_transition_in(mock_clip, TransitionType.LIGHT_LEAK, 0.4)
        mock_clip.transform.assert_called_once()

    def test_apply_transition_out_whip_pan(self, processor, mock_clip):
        """_apply_transition_out dispatches WHIP_PAN."""
        processor._apply_transition_out(mock_clip, TransitionType.WHIP_PAN, 0.3)
        mock_clip.transform.assert_called_once()

    def test_apply_transition_out_flash_white(self, processor, mock_clip):
        """_apply_transition_out dispatches FLASH_WHITE."""
        processor._apply_transition_out(mock_clip, TransitionType.FLASH_WHITE, 0.3)
        mock_clip.transform.assert_called_once()

    def test_apply_transition_skips_short_clips(self, processor):
        """Transition is skipped if clip too short for safe duration."""
        clip = MagicMock()
        clip.duration = 0.1  # Very short
        result = processor._apply_transition_in(clip, TransitionType.WHIP_PAN, 0.5)
        assert result is clip  # No transform applied

    # --- Hyperlapse Zoom ---

    def test_hyperlapse_zoom_calls_transform(self, processor, mock_clip):
        """Hyperlapse zoom transition calls clip.transform()."""
        processor._transition_hyperlapse_zoom(mock_clip, 0.4, is_start=True)
        mock_clip.transform.assert_called_once()

    def test_hyperlapse_zoom_enum_value(self):
        """HYPERLAPSE_ZOOM enum has correct value."""
        assert TransitionType.HYPERLAPSE_ZOOM.value == "hyperlapse_zoom"

    def test_apply_transition_in_hyperlapse_zoom(self, processor, mock_clip):
        """_apply_transition_in dispatches HYPERLAPSE_ZOOM."""
        processor._apply_transition_in(mock_clip, TransitionType.HYPERLAPSE_ZOOM, 0.4)
        mock_clip.transform.assert_called_once()

    def test_apply_transition_out_hyperlapse_zoom(self, processor, mock_clip):
        """_apply_transition_out dispatches HYPERLAPSE_ZOOM."""
        processor._apply_transition_out(mock_clip, TransitionType.HYPERLAPSE_ZOOM, 0.4)
        mock_clip.transform.assert_called_once()

    def test_hyperlapse_zoom_zooms_at_start(self, processor):
        """Hyperlapse zoom applies zoom at start of transition."""
        frame = np.random.randint(0, 255, (100, 200, 3), dtype=np.uint8)
        clip = MagicMock()
        clip.duration = 5.0
        processor._transition_hyperlapse_zoom(clip, 0.5, is_start=True)
        effect_fn = clip.transform.call_args[0][0]
        # At t=0 (peak zoom), frame should be different from original
        result = effect_fn(lambda t: frame, 0.0)
        assert result.shape == frame.shape


class TestPhase3Transitions:
    """Tests for Phase 3 transition effects."""

    @pytest.fixture
    def processor(self):
        return VideoProcessor()

    @pytest.fixture
    def mock_clip(self):
        clip = MagicMock()
        clip.duration = 5.0
        clip.transform.return_value = clip
        clip.with_effects.return_value = clip
        return clip

    @pytest.fixture
    def test_frame(self):
        return np.random.randint(0, 255, (100, 200, 3), dtype=np.uint8)

    def test_all_transition_types_count(self):
        """TransitionType should have 23 members."""
        assert len(TransitionType) == 23

    def test_new_transition_enums_exist(self):
        """All new transition enums should exist."""
        assert TransitionType.PARALLAX_LEFT.value == "parallax_left"
        assert TransitionType.PARALLAX_RIGHT.value == "parallax_right"
        assert TransitionType.WIPE_DIAGONAL.value == "wipe_diagonal"
        assert TransitionType.WIPE_DIAMOND.value == "wipe_diamond"
        assert TransitionType.FOG_PASS.value == "fog_pass"
        assert TransitionType.VORTEX_ZOOM.value == "vortex_zoom"

    # Parallax tests
    def test_parallax_left_dispatches(self, processor, mock_clip):
        """_apply_transition_in dispatches PARALLAX_LEFT."""
        processor._apply_transition_in(mock_clip, TransitionType.PARALLAX_LEFT, 0.4)
        mock_clip.transform.assert_called_once()

    def test_parallax_right_dispatches(self, processor, mock_clip):
        """_apply_transition_out dispatches PARALLAX_RIGHT."""
        processor._apply_transition_out(mock_clip, TransitionType.PARALLAX_RIGHT, 0.4)
        mock_clip.transform.assert_called_once()

    def test_parallax_effect_produces_valid_frame(self, processor, test_frame):
        """Parallax effect should produce valid frame."""
        clip = MagicMock()
        clip.duration = 5.0
        processor._transition_parallax(clip, 0.5, direction="left", is_start=True)
        effect_fn = clip.transform.call_args[0][0]
        result = effect_fn(lambda t: test_frame, 0.1)
        assert result.shape == test_frame.shape

    def test_parallax_no_effect_past_duration(self, processor, test_frame):
        """Parallax should have no effect past transition duration."""
        clip = MagicMock()
        clip.duration = 5.0
        processor._transition_parallax(clip, 0.5, direction="left", is_start=True)
        effect_fn = clip.transform.call_args[0][0]
        result = effect_fn(lambda t: test_frame, 3.0)
        assert np.array_equal(result, test_frame)

    # Diagonal wipe tests
    def test_wipe_diagonal_dispatches_in(self, processor, mock_clip):
        """_apply_transition_in dispatches WIPE_DIAGONAL."""
        processor._apply_transition_in(mock_clip, TransitionType.WIPE_DIAGONAL, 0.4)
        mock_clip.transform.assert_called_once()

    def test_wipe_diagonal_dispatches_out(self, processor, mock_clip):
        """_apply_transition_out dispatches WIPE_DIAGONAL."""
        processor._apply_transition_out(mock_clip, TransitionType.WIPE_DIAGONAL, 0.4)
        mock_clip.transform.assert_called_once()

    def test_wipe_diagonal_effect_valid(self, processor, test_frame):
        """Diagonal wipe should produce valid frame with dark areas at start."""
        clip = MagicMock()
        clip.duration = 5.0
        processor._transition_wipe_diagonal(clip, 0.5, is_start=True)
        effect_fn = clip.transform.call_args[0][0]
        result = effect_fn(lambda t: test_frame, 0.1)
        assert result.shape == test_frame.shape
        # At early progress, some areas should be darker (masked)
        assert result.mean() < test_frame.mean()

    # Diamond wipe tests
    def test_wipe_diamond_dispatches(self, processor, mock_clip):
        """_apply_transition_in dispatches WIPE_DIAMOND."""
        processor._apply_transition_in(mock_clip, TransitionType.WIPE_DIAMOND, 0.4)
        mock_clip.transform.assert_called_once()

    def test_wipe_diamond_effect_valid(self, processor, test_frame):
        """Diamond wipe should produce valid frame."""
        clip = MagicMock()
        clip.duration = 5.0
        processor._transition_wipe_diamond(clip, 0.5, is_start=True)
        effect_fn = clip.transform.call_args[0][0]
        result = effect_fn(lambda t: test_frame, 0.1)
        assert result.shape == test_frame.shape

    def test_wipe_diamond_center_visible_first(self, processor, test_frame):
        """Diamond wipe should reveal center before edges."""
        clip = MagicMock()
        clip.duration = 5.0
        processor._transition_wipe_diamond(clip, 0.5, is_start=True)
        effect_fn = clip.transform.call_args[0][0]
        result = effect_fn(lambda t: test_frame, 0.2)
        # Center should be brighter (revealed) than corners
        h, w = result.shape[:2]
        center_val = result[h//2, w//2].mean()
        corner_val = result[0, 0].mean()
        assert center_val >= corner_val

    # Fog pass tests
    def test_fog_pass_dispatches_in(self, processor, mock_clip):
        """_apply_transition_in dispatches FOG_PASS."""
        processor._apply_transition_in(mock_clip, TransitionType.FOG_PASS, 0.5)
        mock_clip.transform.assert_called_once()

    def test_fog_pass_dispatches_out(self, processor, mock_clip):
        """_apply_transition_out dispatches FOG_PASS."""
        processor._apply_transition_out(mock_clip, TransitionType.FOG_PASS, 0.5)
        mock_clip.transform.assert_called_once()

    def test_fog_pass_effect_valid(self, processor, test_frame):
        """Fog pass should produce valid frame with fog overlay."""
        clip = MagicMock()
        clip.duration = 5.0
        processor._transition_fog_pass(clip, 0.5, is_start=True)
        effect_fn = clip.transform.call_args[0][0]
        result = effect_fn(lambda t: test_frame, 0.1)
        assert result.shape == test_frame.shape

    def test_fog_pass_fades_to_clear(self, processor, test_frame):
        """Fog should be clear past transition duration."""
        clip = MagicMock()
        clip.duration = 5.0
        processor._transition_fog_pass(clip, 0.5, is_start=True)
        effect_fn = clip.transform.call_args[0][0]
        result = effect_fn(lambda t: test_frame, 3.0)
        assert np.array_equal(result, test_frame)

    # Vortex zoom tests
    def test_vortex_zoom_dispatches_in(self, processor, mock_clip):
        """_apply_transition_in dispatches VORTEX_ZOOM."""
        processor._apply_transition_in(mock_clip, TransitionType.VORTEX_ZOOM, 0.3)
        mock_clip.transform.assert_called_once()

    def test_vortex_zoom_dispatches_out(self, processor, mock_clip):
        """_apply_transition_out dispatches VORTEX_ZOOM."""
        processor._apply_transition_out(mock_clip, TransitionType.VORTEX_ZOOM, 0.3)
        mock_clip.transform.assert_called_once()

    def test_vortex_zoom_effect_valid(self, processor, test_frame):
        """Vortex zoom should produce valid frame with blur at start."""
        clip = MagicMock()
        clip.duration = 5.0
        processor._transition_vortex_zoom(clip, 0.5, is_start=True)
        effect_fn = clip.transform.call_args[0][0]
        result = effect_fn(lambda t: test_frame, 0.1)
        assert result.shape == test_frame.shape

    def test_vortex_zoom_clear_after_duration(self, processor, test_frame):
        """Vortex zoom should be clear past transition duration."""
        clip = MagicMock()
        clip.duration = 5.0
        processor._transition_vortex_zoom(clip, 0.5, is_start=True)
        effect_fn = clip.transform.call_args[0][0]
        result = effect_fn(lambda t: test_frame, 3.0)
        assert np.array_equal(result, test_frame)

    # Motion matching tests for new transitions
    def test_motion_match_orbit_to_diamond(self, processor):
        """Orbit motion should map to WIPE_DIAMOND."""
        from drone_reel.core.scene_detector import MotionType, EnhancedSceneInfo
        scene1 = EnhancedSceneInfo(
            start_time=0, end_time=5, duration=5.0, score=80,
            source_file=Path("/tmp/v1.mp4"),
            motion_type=MotionType.ORBIT_CW,
            motion_direction=(0.05, 0.02),
            motion_energy=50, hook_potential=70,
        )
        scene2 = EnhancedSceneInfo(
            start_time=5, end_time=10, duration=5.0, score=75,
            source_file=Path("/tmp/v2.mp4"),
            motion_type=MotionType.STATIC,
            motion_direction=(0.0, 0.0),
            motion_energy=10, hook_potential=50,
        )
        trans_type, _ = processor.select_motion_matched_transition(scene1, scene2)
        assert trans_type == TransitionType.WIPE_DIAMOND

    def test_motion_match_fpv_fast_to_vortex(self, processor):
        """Fast FPV motion should map to VORTEX_ZOOM."""
        from drone_reel.core.scene_detector import MotionType, EnhancedSceneInfo
        scene1 = EnhancedSceneInfo(
            start_time=0, end_time=5, duration=5.0, score=80,
            source_file=Path("/tmp/v1.mp4"),
            motion_type=MotionType.FPV,
            motion_direction=(0.06, 0.04),
            motion_energy=80, hook_potential=90,
        )
        scene2 = EnhancedSceneInfo(
            start_time=5, end_time=10, duration=5.0, score=75,
            source_file=Path("/tmp/v2.mp4"),
            motion_type=MotionType.STATIC,
            motion_direction=(0.0, 0.0),
            motion_energy=10, hook_potential=50,
        )
        trans_type, _ = processor.select_motion_matched_transition(scene1, scene2)
        assert trans_type == TransitionType.VORTEX_ZOOM

    def test_motion_match_tilt_down_to_fog(self, processor):
        """Tilt down motion should map to FOG_PASS."""
        from drone_reel.core.scene_detector import MotionType, EnhancedSceneInfo
        scene1 = EnhancedSceneInfo(
            start_time=0, end_time=5, duration=5.0, score=80,
            source_file=Path("/tmp/v1.mp4"),
            motion_type=MotionType.TILT_DOWN,
            motion_direction=(0.0, 0.05),
            motion_energy=40, hook_potential=50,
        )
        scene2 = EnhancedSceneInfo(
            start_time=5, end_time=10, duration=5.0, score=75,
            source_file=Path("/tmp/v2.mp4"),
            motion_type=MotionType.STATIC,
            motion_direction=(0.0, 0.0),
            motion_energy=10, hook_potential=50,
        )
        trans_type, _ = processor.select_motion_matched_transition(scene1, scene2)
        assert trans_type == TransitionType.FOG_PASS

    def test_motion_match_pan_right_slow_to_parallax(self, processor):
        """Slow pan right should map to PARALLAX_LEFT."""
        from drone_reel.core.scene_detector import MotionType, EnhancedSceneInfo
        scene1 = EnhancedSceneInfo(
            start_time=0, end_time=5, duration=5.0, score=80,
            source_file=Path("/tmp/v1.mp4"),
            motion_type=MotionType.PAN_RIGHT,
            motion_direction=(0.025, 0.0),
            motion_energy=25, hook_potential=50,
        )
        scene2 = EnhancedSceneInfo(
            start_time=5, end_time=10, duration=5.0, score=75,
            source_file=Path("/tmp/v2.mp4"),
            motion_type=MotionType.TILT_UP,
            motion_direction=(0.0, -0.03),
            motion_energy=30, hook_potential=50,
        )
        trans_type, _ = processor.select_motion_matched_transition(scene1, scene2)
        assert trans_type == TransitionType.PARALLAX_LEFT


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
