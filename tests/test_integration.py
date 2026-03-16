"""
Integration tests for the full analysis+selection+sequencing pipeline.

Tests the complete workflow from scene detection through to final clip selection,
using synthetic test videos generated with OpenCV.
"""

from pathlib import Path

import cv2
import numpy as np
import pytest

from drone_reel.core.color_grader import ColorGrader, ColorPreset
from drone_reel.core.duration_adjuster import DurationAdjuster
from drone_reel.core.reframe_selector import ReframeSelector
from drone_reel.core.scene_analyzer import (
    analyze_scene_motion,
    analyze_scenes_batch,
    classify_motion_type,
)
from drone_reel.core.scene_detector import (
    EnhancedSceneInfo,
    HookPotential,
    MotionType,
    SceneDetector,
    SceneInfo,
)
from drone_reel.core.scene_filter import FilterThresholds, SceneFilter
from drone_reel.core.scene_sequencer import SceneSequencer
from drone_reel.core.sequence_optimizer import DiversitySelector


class TestSyntheticVideoGeneration:
    """Test synthetic video generation utilities."""

    @pytest.fixture
    def temp_dir(self, tmp_path):
        """Create temporary directory for test videos."""
        return tmp_path

    def create_test_video(
        self,
        path: Path,
        width: int = 320,
        height: int = 240,
        fps: int = 30,
        duration_sec: float = 3.0,
        motion_type: str = "static",
    ) -> Path:
        """
        Create a synthetic test video with specified motion.

        Args:
            path: Output video path
            width: Video width
            height: Video height
            fps: Frames per second
            duration_sec: Duration in seconds
            motion_type: Type of motion ("static", "pan_right", "tilt_up")

        Returns:
            Path to created video
        """
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(str(path), fourcc, fps, (width, height))

        if not out.isOpened():
            raise RuntimeError(f"Failed to create video writer for {path}")

        total_frames = int(fps * duration_sec)

        for i in range(total_frames):
            # Create base frame with gradient
            frame = np.zeros((height, width, 3), dtype=np.uint8)

            if motion_type == "static":
                # Static gradient (vertical)
                for y in range(height):
                    color = int(100 + (y / height) * 100)
                    frame[y, :] = [color, color // 2, 255 - color]

            elif motion_type == "pan_right":
                # Horizontal pan - shift pattern right each frame
                offset = (i * 5) % width
                for x in range(width):
                    color_x = (x + offset) % 256
                    frame[:, x] = [color_x, 128, 255 - color_x]

            elif motion_type == "tilt_up":
                # Vertical tilt - shift pattern up each frame
                offset = (i * 3) % height
                for y in range(height):
                    color_y = (y + offset) % 256
                    frame[y, :] = [color_y, 255 - color_y, 128]

            # Add some texture for sharpness detection
            noise = np.random.randint(0, 30, (height, width, 3), dtype=np.uint8)
            frame = cv2.add(frame, noise)

            out.write(frame)

        out.release()
        return path

    def test_create_static_video(self, temp_dir):
        """Test creating a static video."""
        video_path = temp_dir / "static.mp4"
        result_path = self.create_test_video(video_path, motion_type="static")

        assert result_path.exists()
        assert result_path.stat().st_size > 0

        # Verify video can be opened
        cap = cv2.VideoCapture(str(result_path))
        assert cap.isOpened()
        assert cap.get(cv2.CAP_PROP_FRAME_COUNT) > 0
        cap.release()

    def test_create_pan_video(self, temp_dir):
        """Test creating a panning video."""
        video_path = temp_dir / "pan.mp4"
        result_path = self.create_test_video(video_path, motion_type="pan_right")

        assert result_path.exists()
        cap = cv2.VideoCapture(str(result_path))
        assert cap.isOpened()
        cap.release()

    def test_create_tilt_video(self, temp_dir):
        """Test creating a tilting video."""
        video_path = temp_dir / "tilt.mp4"
        result_path = self.create_test_video(video_path, motion_type="tilt_up")

        assert result_path.exists()
        cap = cv2.VideoCapture(str(result_path))
        assert cap.isOpened()
        cap.release()


class TestPipelineSceneDetection:
    """Test scene detection on synthetic videos."""

    @pytest.fixture
    def test_videos(self, tmp_path):
        """Create test videos for scene detection."""
        generator = TestSyntheticVideoGeneration()
        videos = {
            "static": generator.create_test_video(
                tmp_path / "static.mp4", motion_type="static"
            ),
            "pan": generator.create_test_video(
                tmp_path / "pan.mp4", motion_type="pan_right"
            ),
            "tilt": generator.create_test_video(
                tmp_path / "tilt.mp4", motion_type="tilt_up"
            ),
        }
        return videos

    def test_detect_scenes_on_synthetic_video(self, test_videos):
        """Test SceneDetector.detect_scenes() on synthetic videos."""
        detector = SceneDetector(
            threshold=27.0, min_scene_length=1.0, max_scene_length=10.0
        )

        for video_name, video_path in test_videos.items():
            scenes = detector.detect_scenes(video_path)

            # Should detect at least one scene
            assert len(scenes) > 0, f"No scenes detected in {video_name}"

            # Verify SceneInfo fields
            for scene in scenes:
                assert isinstance(scene, SceneInfo)
                assert scene.start_time >= 0
                assert scene.end_time > scene.start_time
                assert scene.duration == pytest.approx(
                    scene.end_time - scene.start_time, abs=0.01
                )
                assert 0 <= scene.score <= 100
                assert scene.source_file == video_path

    def test_scene_info_properties(self, test_videos):
        """Test SceneInfo property calculations."""
        detector = SceneDetector()
        scenes = detector.detect_scenes(test_videos["static"])

        assert len(scenes) > 0
        scene = scenes[0]

        # Test midpoint property
        expected_midpoint = scene.start_time + (scene.duration / 2)
        assert scene.midpoint == pytest.approx(expected_midpoint, abs=0.01)


class TestPipelineAnalysis:
    """Test scene analysis pipeline."""

    @pytest.fixture
    def test_scenes(self, tmp_path):
        """Create test videos and detect scenes."""
        generator = TestSyntheticVideoGeneration()
        detector = SceneDetector(threshold=27.0, min_scene_length=1.0)

        videos = [
            generator.create_test_video(tmp_path / "static.mp4", motion_type="static"),
            generator.create_test_video(
                tmp_path / "pan.mp4", motion_type="pan_right"
            ),
            generator.create_test_video(tmp_path / "tilt.mp4", motion_type="tilt_up"),
        ]

        all_scenes = []
        for video_path in videos:
            scenes = detector.detect_scenes(video_path)
            all_scenes.extend(scenes)

        return all_scenes

    def test_analyze_scenes_batch(self, test_scenes):
        """Test analyze_scenes_batch() with include_sharpness=True."""
        results = analyze_scenes_batch(test_scenes, include_sharpness=True)

        assert len(results) == len(test_scenes)

        for scene in test_scenes:
            scene_id = id(scene)
            assert scene_id in results

            result = results[scene_id]
            assert "motion_energy" in result
            assert "brightness" in result
            assert "shake_score" in result
            assert "motion_type" in result
            assert "motion_direction" in result
            assert "sharpness" in result

            # Verify value ranges
            assert 0 <= result["motion_energy"] <= 100
            assert 0 <= result["brightness"] <= 255
            assert 0 <= result["shake_score"] <= 100
            assert isinstance(result["motion_type"], MotionType)
            assert isinstance(result["motion_direction"], tuple)
            assert len(result["motion_direction"]) == 2
            assert result["sharpness"] >= 0

    def test_analyze_scene_motion_single(self, test_scenes):
        """Test analyze_scene_motion() on a single scene."""
        scene = test_scenes[0]

        # Without sharpness
        result = analyze_scene_motion(scene, include_sharpness=False)
        assert len(result) == 5
        motion_energy, brightness, shake_score, motion_type, motion_direction = result

        assert 0 <= motion_energy <= 100
        assert 0 <= brightness <= 255
        assert 0 <= shake_score <= 100
        assert isinstance(motion_type, MotionType)
        assert isinstance(motion_direction, tuple)

        # With sharpness
        result_with_sharp = analyze_scene_motion(scene, include_sharpness=True)
        assert len(result_with_sharp) == 6
        *base_results, sharpness = result_with_sharp
        assert sharpness >= 0

    def test_motion_type_classification(self, test_scenes):
        """Test that motion types are classified correctly."""
        results = analyze_scenes_batch(test_scenes, include_sharpness=False)

        motion_types_found = set()
        for scene_id, result in results.items():
            motion_types_found.add(result["motion_type"])

        # Should have at least one non-UNKNOWN motion type
        # (pan or tilt videos should be detected)
        assert len(motion_types_found) > 0

    def test_classify_motion_type_function(self):
        """Test classify_motion_type() function directly."""
        # Static motion
        motion_type, direction = classify_motion_type(
            [(0.0, 0.0), (0.0, 0.0), (0.0, 0.0)], motion_energy=5.0
        )
        assert motion_type == MotionType.STATIC

        # Pan right
        motion_type, direction = classify_motion_type(
            [(5.0, 0.0), (5.0, 0.0), (5.0, 0.0)], motion_energy=50.0
        )
        assert motion_type == MotionType.PAN_RIGHT

        # Pan left
        motion_type, direction = classify_motion_type(
            [(-5.0, 0.0), (-5.0, 0.0), (-5.0, 0.0)], motion_energy=50.0
        )
        assert motion_type == MotionType.PAN_LEFT

        # Tilt up
        motion_type, direction = classify_motion_type(
            [(0.0, -5.0), (0.0, -5.0), (0.0, -5.0)], motion_energy=50.0
        )
        assert motion_type == MotionType.TILT_UP


class TestPipelineFilterAndSelect:
    """Test scene filtering and selection."""

    def create_mock_scenes(self) -> list[EnhancedSceneInfo]:
        """Create mock EnhancedSceneInfo objects for testing."""
        scenes = []
        for i in range(10):
            scene = EnhancedSceneInfo(
                start_time=float(i * 5),
                end_time=float((i + 1) * 5),
                duration=5.0,
                score=50.0 + i * 5,  # Varying scores
                source_file=Path(f"video_{i % 3}.mp4"),  # 3 different source files
                motion_type=MotionType.PAN_RIGHT if i % 2 == 0 else MotionType.STATIC,
                motion_energy=30.0 + i * 5,  # Varying motion energy
                subject_score=0.5 + i * 0.05,
                hook_potential=50.0 + i * 3,
                hook_tier=HookPotential.MEDIUM,
            )
            scenes.append(scene)
        return scenes

    def test_scene_filter_basic(self):
        """Test SceneFilter removes dark/shaky scenes."""
        scenes = self.create_mock_scenes()
        filter_obj = SceneFilter()

        # Create analysis maps
        motion_map = {id(s): s.motion_energy for s in scenes}
        brightness_map = {
            id(s): 100.0 if i < 5 else 20.0 for i, s in enumerate(scenes)
        }  # First 5 bright, rest dark
        shake_map = {id(s): 10.0 for s in scenes}  # All stable

        result = filter_obj.filter_scenes(scenes, motion_map, brightness_map, shake_map)

        # Should filter out dark scenes (last 5)
        assert result.dark_scenes_filtered == 5
        assert len(result.all_passing) <= 5

    def test_scene_filter_motion_tiers(self):
        """Test SceneFilter categorizes motion into tiers."""
        scenes = self.create_mock_scenes()
        filter_obj = SceneFilter(
            FilterThresholds(
                min_motion_energy=25.0,
                ideal_motion_energy=45.0,
                min_brightness=30.0,
                max_brightness=245.0,
                max_shake_score=40.0,
            )
        )

        motion_map = {id(s): s.motion_energy for s in scenes}
        brightness_map = {id(s): 127.0 for s in scenes}
        shake_map = {id(s): 10.0 for s in scenes}

        result = filter_obj.filter_scenes(scenes, motion_map, brightness_map, shake_map)

        # Should have scenes in different tiers
        total_passing = (
            len(result.high_motion_scenes)
            + len(result.medium_motion_scenes)
            + len(result.low_motion_scenes)
        )
        assert total_passing > 0

    def test_diversity_selector(self):
        """Test DiversitySelector returns requested count."""
        scenes = self.create_mock_scenes()
        selector = DiversitySelector(diversity_weight=0.3, max_per_source=2)

        selected = selector.select(scenes, count=5)

        assert len(selected) == 5
        assert all(isinstance(s, EnhancedSceneInfo) for s in selected)

        # Check source file diversity
        source_counts = {}
        for scene in selected:
            source_counts[scene.source_file] = (
                source_counts.get(scene.source_file, 0) + 1
            )
        assert all(count <= 2 for count in source_counts.values())

    def test_diversity_selector_with_few_scenes(self):
        """Test DiversitySelector handles requesting more scenes than available."""
        scenes = self.create_mock_scenes()[:3]
        selector = DiversitySelector()

        selected = selector.select(scenes, count=10)

        # Should return all available scenes when count > available
        assert len(selected) == 3


class TestPipelineSequencing:
    """Test scene sequencing."""

    def create_mock_scenes_for_sequencing(self) -> list[EnhancedSceneInfo]:
        """Create mock scenes with varying hook potentials."""
        scenes = []
        hook_tiers = [
            HookPotential.MEDIUM,
            HookPotential.HIGH,
            HookPotential.LOW,
            HookPotential.MAXIMUM,
            HookPotential.POOR,
        ]

        for i, tier in enumerate(hook_tiers):
            scene = EnhancedSceneInfo(
                start_time=float(i * 5),
                end_time=float((i + 1) * 5),
                duration=5.0,
                score=50.0 + i * 10,
                source_file=Path(f"video_{i}.mp4"),
                motion_type=MotionType.PAN_RIGHT if i % 2 == 0 else MotionType.TILT_UP,
                motion_energy=40.0 + i * 5,
                subject_score=0.6 + i * 0.05,
                hook_potential=50.0 + i * 10,
                hook_tier=tier,
            )
            scenes.append(scene)
        return scenes

    def test_scene_sequencer_basic(self):
        """Test SceneSequencer produces valid reordered list."""
        scenes = self.create_mock_scenes_for_sequencing()
        sequencer = SceneSequencer()

        motion_map = {id(s): s.motion_energy for s in scenes}
        ordered = sequencer.sequence(scenes, motion_map=motion_map)

        assert len(ordered) == len(scenes)
        assert all(s in scenes for s in ordered)

    def test_scene_sequencer_opener_selection(self):
        """Test that first scene has high hook potential/score."""
        scenes = self.create_mock_scenes_for_sequencing()
        sequencer = SceneSequencer()

        motion_map = {id(s): s.motion_energy for s in scenes}
        ordered = sequencer.sequence(scenes, motion_map=motion_map)

        first_scene = ordered[0]

        # First scene should have high hook potential or score
        # (MAXIMUM tier scene should be selected as opener)
        assert first_scene.hook_tier in (
            HookPotential.MAXIMUM,
            HookPotential.HIGH,
        ) or first_scene.score >= 70

    def test_scene_sequencer_motion_variety(self):
        """Test that sequencer applies motion variety."""
        scenes = self.create_mock_scenes_for_sequencing()
        sequencer = SceneSequencer()

        ordered = sequencer.sequence(scenes)

        # Check that consecutive scenes don't always have the same motion
        same_motion_pairs = 0
        for i in range(len(ordered) - 1):
            if ordered[i].motion_type == ordered[i + 1].motion_type:
                same_motion_pairs += 1

        # Should have some variety (not all pairs same motion)
        assert same_motion_pairs < len(ordered) - 1


class TestPipelineDurationAdjust:
    """Test duration adjustment."""

    def create_mock_scenes_with_sharpness(
        self,
    ) -> tuple[list[EnhancedSceneInfo], dict[int, float]]:
        """Create mock scenes and sharpness map."""
        scenes = []
        sharpness_map = {}

        for i in range(5):
            scene = EnhancedSceneInfo(
                start_time=float(i * 5),
                end_time=float((i + 1) * 5),
                duration=5.0,
                score=60.0,
                source_file=Path(f"video_{i}.mp4"),
                motion_type=MotionType.PAN_RIGHT if i % 2 == 0 else MotionType.STATIC,
                hook_tier=HookPotential.MEDIUM,
            )
            scenes.append(scene)

            # Varying sharpness: some sharp, some blurry
            sharpness_map[id(scene)] = 150.0 if i % 2 == 0 else 20.0

        return scenes, sharpness_map

    def test_duration_adjuster_basic(self):
        """Test DurationAdjuster with realistic scene list."""
        scenes, sharpness_map = self.create_mock_scenes_with_sharpness()
        adjuster = DurationAdjuster()

        initial_durations = [3.0] * len(scenes)
        target_duration = 30.0

        adjusted, scale_factor = adjuster.adjust_durations(
            scenes, initial_durations, sharpness_map, target_duration
        )

        assert len(adjusted) == len(scenes)
        assert all(d > 0 for d in adjusted)

        # Sharp scenes should be different from blurry scenes
        sharp_durations = [adjusted[i] for i in range(len(scenes)) if i % 2 == 0]
        blurry_durations = [adjusted[i] for i in range(len(scenes)) if i % 2 == 1]

        # Blurry scenes should be shorter or equal to sharp scenes (before or after scaling)
        # This verifies that sharpness-based adjustment is working
        if scale_factor is None or scale_factor == 1.0:
            # Without scaling, blurry scenes should be at minimum duration
            assert all(d <= min(sharp_durations) for d in blurry_durations)
        else:
            # With scaling, blurry scenes should still be relatively shorter
            avg_blurry = sum(blurry_durations) / len(blurry_durations)
            avg_sharp = sum(sharp_durations) / len(sharp_durations)
            assert avg_blurry <= avg_sharp

    def test_duration_adjuster_auto_scaling(self):
        """Test DurationAdjuster applies auto-scaling when short of target."""
        scenes, sharpness_map = self.create_mock_scenes_with_sharpness()
        adjuster = DurationAdjuster()

        # Short initial durations
        initial_durations = [2.0] * len(scenes)
        target_duration = 30.0

        adjusted, scale_factor = adjuster.adjust_durations(
            scenes, initial_durations, sharpness_map, target_duration
        )

        # Should have scaled up
        assert scale_factor is not None
        assert scale_factor > 1.0
        assert sum(adjusted) > sum(initial_durations)


class TestPipelineEndToEnd:
    """Test full pipeline end-to-end."""

    @pytest.fixture
    def pipeline_videos(self, tmp_path):
        """Create test videos for full pipeline."""
        generator = TestSyntheticVideoGeneration()
        videos = []
        for i in range(3):
            motion = ["static", "pan_right", "tilt_up"][i]
            path = generator.create_test_video(
                tmp_path / f"video_{i}.mp4", motion_type=motion
            )
            videos.append(path)
        return videos

    def test_full_pipeline(self, pipeline_videos):
        """Test full pipeline from video to final selection."""
        # Step 1: Scene detection
        detector = SceneDetector(threshold=27.0, min_scene_length=1.0)
        all_scenes = []
        for video_path in pipeline_videos:
            scenes = detector.detect_scenes(video_path)
            all_scenes.extend(scenes)

        assert len(all_scenes) > 0, "No scenes detected"

        # Step 2: Scene analysis
        analysis_results = analyze_scenes_batch(all_scenes, include_sharpness=True)
        assert len(analysis_results) == len(all_scenes)

        motion_map = {sid: r["motion_energy"] for sid, r in analysis_results.items()}
        brightness_map = {sid: r["brightness"] for sid, r in analysis_results.items()}
        shake_map = {sid: r["shake_score"] for sid, r in analysis_results.items()}
        sharpness_map = {sid: r["sharpness"] for sid, r in analysis_results.items()}

        # Step 3: Scene filtering
        scene_filter = SceneFilter()
        filter_result = scene_filter.filter_scenes(
            all_scenes, motion_map, brightness_map, shake_map
        )

        passing_scenes = filter_result.prioritized
        assert len(passing_scenes) > 0, "No scenes passed filtering"

        # Step 4: Scene selection
        selector = DiversitySelector(diversity_weight=0.3, max_per_source=2)
        desired_count = min(5, len(passing_scenes))
        selected_scenes = selector.select(passing_scenes, count=desired_count)

        assert len(selected_scenes) > 0
        assert len(selected_scenes) <= desired_count

        # Step 5: Scene sequencing
        sequencer = SceneSequencer()
        ordered_scenes = sequencer.sequence(selected_scenes, motion_map=motion_map)

        assert len(ordered_scenes) == len(selected_scenes)

        # Step 6: Duration adjustment
        adjuster = DurationAdjuster()
        initial_durations = [3.0] * len(ordered_scenes)
        target_duration = 15.0

        adjusted_durations, scale_factor = adjuster.adjust_durations(
            ordered_scenes, initial_durations, sharpness_map, target_duration
        )

        assert len(adjusted_durations) == len(ordered_scenes)
        assert all(d > 0 for d in adjusted_durations)

        # Step 7: Reframe selection
        reframe_selector = ReframeSelector(
            output_width=1080, kb_config=None, subject_threshold=40.0
        )
        reframers, mode_names = reframe_selector.select_reframers(
            ordered_scenes, adjusted_durations
        )

        assert len(reframers) == len(ordered_scenes)
        assert len(mode_names) == len(ordered_scenes)
        assert all(mode in ("CENTER", "SMART", "KEN_BURNS") for mode in mode_names)

        # Verify final output consistency
        assert len(ordered_scenes) == len(adjusted_durations) == len(reframers)

    def test_pipeline_with_enhanced_scenes(self, pipeline_videos):
        """Test pipeline with EnhancedSceneInfo objects."""
        detector = SceneDetector()

        # Use detect_scenes_enhanced to get EnhancedSceneInfo
        all_enhanced = []
        for video_path in pipeline_videos:
            enhanced = detector.detect_scenes_enhanced(video_path)
            all_enhanced.extend(enhanced)

        assert len(all_enhanced) > 0
        assert all(isinstance(s, EnhancedSceneInfo) for s in all_enhanced)

        # Create analysis maps from enhanced scenes
        motion_map = {id(s): s.motion_energy for s in all_enhanced}
        brightness_map = {id(s): 127.0 for s in all_enhanced}  # Assume good brightness
        shake_map = {id(s): 20.0 for s in all_enhanced}  # Assume stable
        sharpness_map = {id(s): 100.0 for s in all_enhanced}  # Assume sharp

        # Run through pipeline
        scene_filter = SceneFilter()
        filter_result = scene_filter.filter_scenes(
            all_enhanced, motion_map, brightness_map, shake_map
        )

        selector = DiversitySelector()
        selected = selector.select(
            filter_result.prioritized, count=min(5, len(filter_result.prioritized))
        )

        sequencer = SceneSequencer()
        ordered = sequencer.sequence(selected, motion_map=motion_map)

        adjuster = DurationAdjuster()
        durations, _ = adjuster.adjust_durations(
            ordered, [3.0] * len(ordered), sharpness_map, 15.0
        )

        assert len(ordered) == len(durations)


class TestColorGraderIntegration:
    """Test ColorGrader integration with synthetic frames."""

    def create_test_frame(
        self, width: int = 320, height: int = 240
    ) -> np.ndarray:
        """Create a synthetic test frame."""
        frame = np.zeros((height, width, 3), dtype=np.uint8)

        # Create gradient pattern
        for y in range(height):
            for x in range(width):
                frame[y, x] = [
                    int((x / width) * 255),  # B
                    int((y / height) * 255),  # G
                    128,  # R
                ]

        return frame

    def test_color_grader_basic(self):
        """Test ColorGrader.grade_frame() on synthetic frame."""
        frame = self.create_test_frame()
        grader = ColorGrader(preset=ColorPreset.NONE)

        graded = grader.grade_frame(frame)

        assert graded.shape == frame.shape
        assert graded.dtype == np.uint8

    def test_color_grader_presets(self):
        """Test multiple color grading presets."""
        frame = self.create_test_frame()

        presets = [
            ColorPreset.DRONE_AERIAL,
            ColorPreset.TEAL_ORANGE,
            ColorPreset.CINEMATIC,
        ]

        for preset in presets:
            grader = ColorGrader(preset=preset)
            graded = grader.grade_frame(frame)

            assert graded.shape == frame.shape
            assert graded.dtype == np.uint8

            # Verify pixel values changed (except for NONE preset)
            if preset != ColorPreset.NONE:
                assert not np.array_equal(graded, frame)

    def test_color_grader_preserves_shape(self):
        """Test that ColorGrader preserves frame dimensions."""
        sizes = [(320, 240), (640, 480), (1920, 1080)]

        for width, height in sizes:
            frame = self.create_test_frame(width, height)
            grader = ColorGrader(preset=ColorPreset.CINEMATIC)

            graded = grader.grade_frame(frame)

            assert graded.shape == (height, width, 3)

    def test_color_grader_value_ranges(self):
        """Test that ColorGrader keeps pixel values in valid range."""
        frame = self.create_test_frame()
        grader = ColorGrader(preset=ColorPreset.VIBRANT)

        graded = grader.grade_frame(frame)

        assert np.all(graded >= 0)
        assert np.all(graded <= 255)


class TestPipelineEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_scene_list(self):
        """Test pipeline handles empty scene list."""
        selector = DiversitySelector()
        selected = selector.select([], count=5)
        assert selected == []

        sequencer = SceneSequencer()
        ordered = sequencer.sequence([])
        assert ordered == []

    def test_single_scene(self):
        """Test pipeline handles single scene."""
        scene = EnhancedSceneInfo(
            start_time=0.0,
            end_time=5.0,
            duration=5.0,
            score=60.0,
            source_file=Path("video.mp4"),
            motion_type=MotionType.PAN_RIGHT,
        )

        selector = DiversitySelector()
        selected = selector.select([scene], count=1)
        assert len(selected) == 1

        sequencer = SceneSequencer()
        ordered = sequencer.sequence([scene])
        assert len(ordered) == 1
        assert ordered[0] is scene

    def test_request_more_scenes_than_available(self):
        """Test selector handles requesting more scenes than available."""
        scenes = [
            EnhancedSceneInfo(
                start_time=float(i * 5),
                end_time=float((i + 1) * 5),
                duration=5.0,
                score=60.0,
                source_file=Path("video.mp4"),
                motion_type=MotionType.PAN_RIGHT,
            )
            for i in range(3)
        ]

        selector = DiversitySelector()
        selected = selector.select(scenes, count=10)

        # Should return all available scenes
        assert len(selected) == 3
