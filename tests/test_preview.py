"""
Tests for thumbnail generation and preview functionality.
"""

import tempfile
from pathlib import Path

import cv2
import numpy as np
import pytest
from moviepy import VideoFileClip

from drone_reel.core.preview import (
    PreviewGenerator,
    ThumbnailGenerator,
    ThumbnailStyle,
)
from drone_reel.core.scene_detector import SceneInfo
from drone_reel.core.video_processor import ClipSegment, TransitionType


@pytest.fixture
def sample_video():
    """Create a sample test video."""
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        video_path = Path(tmp.name)

    # Create a simple test video with colored frames
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    fps = 30
    size = (640, 480)

    out = cv2.VideoWriter(str(video_path), fourcc, fps, size)

    # Generate 90 frames (3 seconds)
    for i in range(90):
        # Create colored frame that changes over time
        frame = np.zeros((size[1], size[0], 3), dtype=np.uint8)

        # Blue to red gradient over time
        progress = i / 90
        frame[:, :] = [int(255 * (1 - progress)), 0, int(255 * progress)]

        # Add some edges for composition testing
        cv2.rectangle(frame, (100, 100), (540, 380), (255, 255, 255), 2)

        out.write(frame)

    out.release()

    yield video_path

    # Cleanup
    try:
        video_path.unlink()
    except Exception:
        pass


@pytest.fixture
def sample_scenes(sample_video):
    """Create sample scene infos for testing."""
    scenes = [
        SceneInfo(
            start_time=0.0,
            end_time=1.0,
            duration=1.0,
            score=75.0,
            source_file=sample_video,
        ),
        SceneInfo(
            start_time=1.0,
            end_time=2.0,
            duration=1.0,
            score=85.0,
            source_file=sample_video,
        ),
        SceneInfo(
            start_time=2.0,
            end_time=3.0,
            duration=1.0,
            score=65.0,
            source_file=sample_video,
        ),
    ]
    return scenes


@pytest.fixture
def sample_segments(sample_scenes):
    """Create sample clip segments for testing."""
    segments = [
        ClipSegment(
            scene=sample_scenes[0],
            start_offset=0.0,
            duration=0.5,
            transition_in=TransitionType.CUT,
            transition_out=TransitionType.CROSSFADE,
        ),
        ClipSegment(
            scene=sample_scenes[1],
            start_offset=0.0,
            duration=0.5,
            transition_in=TransitionType.CROSSFADE,
            transition_out=TransitionType.FADE_BLACK,
        ),
    ]
    return segments


class TestThumbnailGenerator:
    """Test suite for ThumbnailGenerator."""

    def test_init(self):
        """Test ThumbnailGenerator initialization."""
        generator = ThumbnailGenerator()
        assert generator is not None
        assert hasattr(generator, "_font_cache")

    def test_generate_hero_thumbnail(self, sample_scenes, tmp_path):
        """Test hero style thumbnail generation."""
        generator = ThumbnailGenerator()
        output_path = tmp_path / "hero_thumbnail.jpg"

        result_path = generator.generate(
            scenes=sample_scenes,
            output_path=output_path,
            style=ThumbnailStyle.HERO,
            size=(640, 480),
        )

        assert result_path == output_path
        assert output_path.exists()
        assert output_path.stat().st_size > 0

        # Verify image can be loaded
        img = cv2.imread(str(output_path))
        assert img is not None
        assert img.shape == (480, 640, 3)

    def test_generate_composite_thumbnail(self, sample_scenes, tmp_path):
        """Test composite style thumbnail generation."""
        generator = ThumbnailGenerator()
        output_path = tmp_path / "composite_thumbnail.jpg"

        result_path = generator.generate(
            scenes=sample_scenes,
            output_path=output_path,
            style=ThumbnailStyle.COMPOSITE,
            size=(800, 800),
        )

        assert result_path == output_path
        assert output_path.exists()
        assert output_path.stat().st_size > 0

        # Verify image dimensions
        img = cv2.imread(str(output_path))
        assert img is not None
        assert img.shape == (800, 800, 3)

    def test_generate_text_overlay_thumbnail(self, sample_scenes, tmp_path):
        """Test text overlay style thumbnail generation."""
        generator = ThumbnailGenerator()
        output_path = tmp_path / "text_thumbnail.jpg"

        result_path = generator.generate(
            scenes=sample_scenes,
            output_path=output_path,
            style=ThumbnailStyle.TEXT_OVERLAY,
            size=(640, 480),
            text="Awesome Drone Footage",
        )

        assert result_path == output_path
        assert output_path.exists()
        assert output_path.stat().st_size > 0

    def test_generate_empty_scenes_raises_error(self, tmp_path):
        """Test that empty scenes list raises ValueError."""
        generator = ThumbnailGenerator()
        output_path = tmp_path / "thumbnail.jpg"

        with pytest.raises(ValueError, match="No scenes provided"):
            generator.generate(scenes=[], output_path=output_path)

    def test_select_best_frame(self, sample_scenes):
        """Test best frame selection."""
        generator = ThumbnailGenerator()
        scene = sample_scenes[0]

        frame = generator.select_best_frame(scene, criteria="composition")

        assert frame is not None
        assert isinstance(frame, np.ndarray)
        assert frame.shape[2] == 3  # BGR
        assert frame.dtype == np.uint8

    def test_select_best_frame_criteria(self, sample_scenes):
        """Test different selection criteria."""
        generator = ThumbnailGenerator()
        scene = sample_scenes[0]

        # Test each valid criteria
        for criteria in ["composition", "color", "sharpness"]:
            frame = generator.select_best_frame(scene, criteria=criteria)
            assert frame is not None
            assert isinstance(frame, np.ndarray)

    def test_select_best_frame_invalid_criteria(self, sample_scenes):
        """Test invalid criteria raises ValueError."""
        generator = ThumbnailGenerator()
        scene = sample_scenes[0]

        with pytest.raises(ValueError, match="Invalid criteria"):
            generator.select_best_frame(scene, criteria="invalid")

    def test_score_thumbnail_potential(self, sample_scenes):
        """Test thumbnail potential scoring."""
        generator = ThumbnailGenerator()
        scene = sample_scenes[0]

        frame = generator.select_best_frame(scene)
        score = generator.score_thumbnail_potential(frame)

        assert isinstance(score, float)
        assert 0.0 <= score <= 100.0

    def test_score_thumbnail_potential_range(self):
        """Test scoring returns values in valid range."""
        generator = ThumbnailGenerator()

        # Create test frames with different characteristics
        # Black frame (low score)
        black_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        black_score = generator.score_thumbnail_potential(black_frame)
        assert 0.0 <= black_score <= 100.0

        # Colorful frame with edges (higher score)
        color_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        color_score = generator.score_thumbnail_potential(color_frame)
        assert 0.0 <= color_score <= 100.0

    def test_create_composite_thumbnail(self, sample_scenes):
        """Test composite thumbnail creation."""
        generator = ThumbnailGenerator()

        composite = generator.create_composite_thumbnail(
            scenes=sample_scenes, grid_size=(2, 2), output_size=(800, 800)
        )

        assert composite is not None
        assert isinstance(composite, np.ndarray)
        assert composite.shape == (800, 800, 3)

    def test_create_composite_thumbnail_single_scene(self, sample_scenes):
        """Test composite with single scene."""
        generator = ThumbnailGenerator()

        composite = generator.create_composite_thumbnail(
            scenes=[sample_scenes[0]], grid_size=(1, 1), output_size=(400, 400)
        )

        assert composite is not None
        assert composite.shape == (400, 400, 3)

    def test_add_text_to_thumbnail(self):
        """Test text overlay on thumbnail."""
        generator = ThumbnailGenerator()

        # Create test image
        image = np.zeros((480, 640, 3), dtype=np.uint8)

        # Test each position
        for position in ["top", "bottom", "center"]:
            result = generator.add_text_to_thumbnail(
                image, text="Test Text", position=position, style="bold"
            )

            assert result is not None
            assert result.shape == image.shape

    def test_add_text_to_thumbnail_styles(self):
        """Test different text styles."""
        generator = ThumbnailGenerator()
        image = np.zeros((480, 640, 3), dtype=np.uint8)

        for style in ["bold", "outlined", "shadowed"]:
            result = generator.add_text_to_thumbnail(image, text="Test", style=style)
            assert result is not None
            assert result.shape == image.shape

    def test_calculate_grid_size(self):
        """Test grid size calculation."""
        generator = ThumbnailGenerator()

        assert generator._calculate_grid_size(1) == (1, 1)
        assert generator._calculate_grid_size(4) == (2, 2)
        assert generator._calculate_grid_size(6) == (2, 3)
        assert generator._calculate_grid_size(9) == (3, 3)
        assert generator._calculate_grid_size(16) == (4, 4)


class TestPreviewGenerator:
    """Test suite for PreviewGenerator."""

    def test_init(self):
        """Test PreviewGenerator initialization."""
        generator = PreviewGenerator(preview_scale=0.5, preview_fps=20)
        assert generator.preview_scale == 0.5
        assert generator.preview_fps == 20

    def test_init_invalid_scale(self):
        """Test invalid scale raises ValueError."""
        with pytest.raises(ValueError, match="preview_scale must be between 0 and 1"):
            PreviewGenerator(preview_scale=1.5)

        with pytest.raises(ValueError, match="preview_scale must be between 0 and 1"):
            PreviewGenerator(preview_scale=0.0)

    def test_generate_preview(self, sample_segments, tmp_path):
        """Test preview video generation."""
        generator = PreviewGenerator(preview_scale=0.25, preview_fps=15)
        output_path = tmp_path / "preview.mp4"

        result_path = generator.generate_preview(
            segments=sample_segments, output_path=output_path, include_transitions=True
        )

        assert result_path == output_path
        assert output_path.exists()
        assert output_path.stat().st_size > 0

        # Verify video can be loaded
        clip = VideoFileClip(str(output_path))
        assert clip.duration > 0
        clip.close()

    def test_generate_preview_no_transitions(self, sample_segments, tmp_path):
        """Test preview without transitions."""
        generator = PreviewGenerator(preview_scale=0.25, preview_fps=15)
        output_path = tmp_path / "preview_no_trans.mp4"

        result_path = generator.generate_preview(
            segments=sample_segments, output_path=output_path, include_transitions=False
        )

        assert result_path == output_path
        assert output_path.exists()

    def test_generate_preview_empty_segments_raises_error(self, tmp_path):
        """Test empty segments raises ValueError."""
        generator = PreviewGenerator()
        output_path = tmp_path / "preview.mp4"

        with pytest.raises(ValueError, match="No segments provided"):
            generator.generate_preview(segments=[], output_path=output_path)

    def test_generate_storyboard(self, sample_segments, tmp_path):
        """Test storyboard generation."""
        generator = PreviewGenerator()
        output_path = tmp_path / "storyboard.jpg"

        result_path = generator.generate_storyboard(
            segments=sample_segments,
            output_path=output_path,
            frames_per_segment=3,
            grid_columns=4,
        )

        assert result_path == output_path
        assert output_path.exists()
        assert output_path.stat().st_size > 0

        # Verify image can be loaded
        img = cv2.imread(str(output_path))
        assert img is not None
        assert len(img.shape) == 3

    def test_generate_storyboard_single_frame(self, sample_segments, tmp_path):
        """Test storyboard with single frame per segment."""
        generator = PreviewGenerator()
        output_path = tmp_path / "storyboard_single.jpg"

        result_path = generator.generate_storyboard(
            segments=sample_segments, output_path=output_path, frames_per_segment=1
        )

        assert result_path == output_path
        assert output_path.exists()

    def test_generate_storyboard_empty_segments_raises_error(self, tmp_path):
        """Test empty segments raises ValueError."""
        generator = PreviewGenerator()
        output_path = tmp_path / "storyboard.jpg"

        with pytest.raises(ValueError, match="No segments provided"):
            generator.generate_storyboard(segments=[], output_path=output_path)

    def test_generate_storyboard_invalid_frames_raises_error(self, sample_segments, tmp_path):
        """Test invalid frames_per_segment raises ValueError."""
        generator = PreviewGenerator()
        output_path = tmp_path / "storyboard.jpg"

        with pytest.raises(ValueError, match="frames_per_segment must be at least 1"):
            generator.generate_storyboard(
                segments=sample_segments, output_path=output_path, frames_per_segment=0
            )

    def test_estimate_preview_time(self, sample_segments):
        """Test preview time estimation."""
        generator = PreviewGenerator()
        estimated_time = generator.estimate_preview_time(sample_segments)

        assert isinstance(estimated_time, float)
        assert estimated_time > 0

    def test_estimate_preview_time_proportional(self, sample_segments):
        """Test estimation scales with content."""
        generator = PreviewGenerator()

        # Short segment list
        time_short = generator.estimate_preview_time(sample_segments[:1])

        # Longer segment list
        time_long = generator.estimate_preview_time(sample_segments)

        assert time_long > time_short

    def test_create_comparison_side_by_side(self, sample_video, tmp_path):
        """Test side-by-side comparison video."""
        generator = PreviewGenerator(preview_scale=0.5, preview_fps=15)
        output_path = tmp_path / "comparison_sbs.mp4"

        result_path = generator.create_comparison(
            original=sample_video,
            edited=sample_video,  # Using same video for testing
            output_path=output_path,
            mode="side_by_side",
        )

        assert result_path == output_path
        assert output_path.exists()
        assert output_path.stat().st_size > 0

        # Verify video
        clip = VideoFileClip(str(output_path))
        assert clip.duration > 0
        clip.close()

    def test_create_comparison_overlay(self, sample_video, tmp_path):
        """Test overlay comparison video."""
        generator = PreviewGenerator(preview_scale=0.5, preview_fps=15)
        output_path = tmp_path / "comparison_overlay.mp4"

        result_path = generator.create_comparison(
            original=sample_video,
            edited=sample_video,
            output_path=output_path,
            mode="overlay",
        )

        assert result_path == output_path
        assert output_path.exists()

    def test_create_comparison_split(self, sample_video, tmp_path):
        """Test split screen comparison video."""
        generator = PreviewGenerator(preview_scale=0.5, preview_fps=15)
        output_path = tmp_path / "comparison_split.mp4"

        result_path = generator.create_comparison(
            original=sample_video,
            edited=sample_video,
            output_path=output_path,
            mode="split",
        )

        assert result_path == output_path
        assert output_path.exists()

    def test_create_comparison_invalid_mode_raises_error(self, sample_video, tmp_path):
        """Test invalid comparison mode raises ValueError."""
        generator = PreviewGenerator()
        output_path = tmp_path / "comparison.mp4"

        with pytest.raises(ValueError, match="Invalid mode"):
            generator.create_comparison(
                original=sample_video,
                edited=sample_video,
                output_path=output_path,
                mode="invalid_mode",
            )


class TestThumbnailScoringMethods:
    """Test individual scoring methods."""

    def test_score_composition(self):
        """Test composition scoring."""
        generator = ThumbnailGenerator()

        # Create frame with edges at rule of thirds
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        # Add rectangle at rule of thirds intersection
        cv2.rectangle(frame, (200, 150), (440, 330), (255, 255, 255), 2)

        score = generator._score_composition(frame)

        assert isinstance(score, float)
        assert 0.0 <= score <= 100.0

    def test_score_color_richness(self):
        """Test color richness scoring."""
        generator = ThumbnailGenerator()

        # Black frame (low color)
        black_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        black_score = generator._score_color_richness(black_frame)
        assert black_score < 20.0

        # Colorful frame (high color)
        color_frame = np.random.randint(100, 255, (480, 640, 3), dtype=np.uint8)
        color_score = generator._score_color_richness(color_frame)
        assert color_score > black_score

    def test_score_sharpness(self):
        """Test sharpness scoring."""
        generator = ThumbnailGenerator()

        # Blurry frame
        blurry_frame = np.ones((480, 640, 3), dtype=np.uint8) * 128
        blurry_score = generator._score_sharpness(blurry_frame)

        # Sharp frame with edges
        sharp_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.rectangle(sharp_frame, (100, 100), (540, 380), (255, 255, 255), 2)
        sharp_score = generator._score_sharpness(sharp_frame)

        assert sharp_score > blurry_score

    def test_score_focal_point(self):
        """Test focal point scoring."""
        generator = ThumbnailGenerator()

        # Frame with center focus
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.circle(frame, (320, 240), 50, (255, 255, 255), -1)

        score = generator._score_focal_point(frame)

        assert isinstance(score, float)
        assert 0.0 <= score <= 100.0


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_thumbnail_single_scene(self, sample_scenes, tmp_path):
        """Test thumbnail generation with single scene."""
        generator = ThumbnailGenerator()
        output_path = tmp_path / "single_scene.jpg"

        result = generator.generate(
            scenes=[sample_scenes[0]], output_path=output_path, style=ThumbnailStyle.HERO
        )

        assert result == output_path
        assert output_path.exists()

    def test_thumbnail_many_scenes(self, sample_scenes, tmp_path):
        """Test thumbnail with many scenes."""
        generator = ThumbnailGenerator()
        output_path = tmp_path / "many_scenes.jpg"

        # Create more scenes
        many_scenes = sample_scenes * 10

        result = generator.generate(
            scenes=many_scenes, output_path=output_path, style=ThumbnailStyle.COMPOSITE
        )

        assert result == output_path
        assert output_path.exists()

    def test_preview_single_segment(self, sample_segments, tmp_path):
        """Test preview with single segment."""
        generator = PreviewGenerator(preview_scale=0.25, preview_fps=15)
        output_path = tmp_path / "single_segment.mp4"

        result = generator.generate_preview(
            segments=[sample_segments[0]], output_path=output_path
        )

        assert result == output_path
        assert output_path.exists()

    def test_storyboard_many_segments(self, sample_segments, tmp_path):
        """Test storyboard with many segments."""
        generator = PreviewGenerator()
        output_path = tmp_path / "many_segments.jpg"

        # Create more segments
        many_segments = sample_segments * 10

        result = generator.generate_storyboard(
            segments=many_segments, output_path=output_path, frames_per_segment=2
        )

        assert result == output_path
        assert output_path.exists()

    def test_thumbnail_creates_parent_directory(self, sample_scenes, tmp_path):
        """Test thumbnail generation creates parent directories."""
        generator = ThumbnailGenerator()
        output_path = tmp_path / "nested" / "dir" / "thumbnail.jpg"

        result = generator.generate(scenes=sample_scenes, output_path=output_path)

        assert result == output_path
        assert output_path.exists()
        assert output_path.parent.exists()

    def test_preview_creates_parent_directory(self, sample_segments, tmp_path):
        """Test preview generation creates parent directories."""
        generator = PreviewGenerator(preview_scale=0.25, preview_fps=15)
        output_path = tmp_path / "nested" / "preview.mp4"

        result = generator.generate_preview(segments=sample_segments, output_path=output_path)

        assert result == output_path
        assert output_path.exists()
        assert output_path.parent.exists()
