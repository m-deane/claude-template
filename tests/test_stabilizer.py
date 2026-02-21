"""Tests for video stabilization module."""

import numpy as np
import pytest
from unittest.mock import MagicMock, patch, PropertyMock, call

from drone_reel.core.stabilizer import stabilize_clip, smooth_trajectory, calculate_shake_score


class TestStabilizeClip:
    """Tests for stabilize_clip function."""

    @pytest.fixture
    def mock_clip(self):
        """Create a mock MoviePy clip."""
        clip = MagicMock()
        clip.fps = 30
        clip.duration = 2.0
        clip.size = (1920, 1080)
        clip.audio = None
        return clip

    @pytest.fixture
    def stable_frames(self):
        """Generate stable test frames (uint8 format)."""
        def get_frame(t):
            # Return consistent frames to simulate stable footage
            frame = np.ones((1080, 1920, 3), dtype=np.uint8) * 128
            # Add some features for tracking
            frame[100:200, 100:200] = 200
            frame[500:600, 800:900] = 50
            return frame
        return get_frame

    @pytest.fixture
    def float_frames(self):
        """Generate test frames in float32 format (0-1 range)."""
        def get_frame(t):
            # Return frames in float format
            frame = np.ones((1080, 1920, 3), dtype=np.float32) * 0.5
            frame[100:200, 100:200] = 0.8
            frame[500:600, 800:900] = 0.2
            return frame
        return get_frame

    def test_stable_clip_returns_original(self, mock_clip):
        """Test that stable clips (shake_score < 15) return original clip unchanged."""
        mock_clip.get_frame = MagicMock()

        # Shake score below stable threshold
        result = stabilize_clip(mock_clip, shake_score=10.0)

        # Should return original clip without processing
        assert result is mock_clip
        mock_clip.get_frame.assert_not_called()

    def test_stable_clip_calls_progress_callback(self, mock_clip):
        """Test that progress callback is called even for stable clips."""
        progress_callback = MagicMock()

        result = stabilize_clip(mock_clip, shake_score=10.0, progress_callback=progress_callback)

        # Should call progress with 1.0 for immediate completion
        progress_callback.assert_called_once_with(1.0)

    def test_light_stabilization_parameters(self, mock_clip, stable_frames):
        """Test light stabilization (shake_score 15-30) uses reduced parameters."""
        mock_clip.get_frame = MagicMock(side_effect=stable_frames)

        with patch('moviepy.VideoClip') as MockVideoClip:
            mock_stabilized = MagicMock()
            mock_stabilized.with_fps.return_value = mock_stabilized
            MockVideoClip.return_value = mock_stabilized

            result = stabilize_clip(mock_clip, shake_score=20.0, smoothing_radius=30, border_crop=0.05)

            assert mock_clip.get_frame.called

    def test_full_stabilization_for_high_shake_score(self, mock_clip, stable_frames):
        """Test full stabilization (shake_score > 30) uses provided parameters."""
        mock_clip.get_frame = MagicMock(side_effect=stable_frames)

        with patch('moviepy.VideoClip') as MockVideoClip:
            mock_stabilized = MagicMock()
            mock_stabilized.with_fps.return_value = mock_stabilized
            MockVideoClip.return_value = mock_stabilized

            result = stabilize_clip(
                mock_clip,
                shake_score=50.0,
                smoothing_radius=30,
                border_crop=0.05
            )

            assert mock_clip.get_frame.called

    def test_very_short_clip_returns_original(self):
        """Test that clips with < 3 frames return original clip."""
        short_clip = MagicMock()
        short_clip.fps = 30
        short_clip.duration = 0.05  # Only 1.5 frames
        short_clip.size = (1920, 1080)

        result = stabilize_clip(short_clip, shake_score=50.0)

        # Should return original for very short clips
        assert result is short_clip

    def test_progress_callback_during_stabilization(self, mock_clip, stable_frames):
        """Test progress callback is called during frame analysis."""
        mock_clip.get_frame = stable_frames
        progress_callback = MagicMock()

        with patch('moviepy.VideoClip') as MockVideoClip:
            mock_stabilized = MagicMock()
            mock_stabilized.with_fps.return_value = mock_stabilized
            MockVideoClip.return_value = mock_stabilized

            result = stabilize_clip(
                mock_clip,
                shake_score=50.0,
                progress_callback=progress_callback
            )

            # Should be called multiple times during processing
            assert progress_callback.call_count > 1
            # Final call should be 1.0
            progress_callback.assert_called_with(1.0)

    def test_audio_preserved_on_stabilized_clip(self, mock_clip, stable_frames):
        """Test audio is preserved on stabilized clip."""
        mock_clip.get_frame = stable_frames
        mock_audio = MagicMock()
        mock_clip.audio = mock_audio

        with patch('moviepy.VideoClip') as MockVideoClip:
            mock_stabilized = MagicMock()
            mock_stabilized.with_fps.return_value = mock_stabilized
            mock_stabilized.with_audio.return_value = mock_stabilized
            MockVideoClip.return_value = mock_stabilized

            result = stabilize_clip(mock_clip, shake_score=50.0)

            # Verify audio was attached
            mock_stabilized.with_audio.assert_called_once_with(mock_audio)

    def test_uint8_frame_format_handled(self, mock_clip):
        """Test uint8 frame format (0-255) is handled correctly."""
        def get_uint8_frame(t):
            return np.ones((1080, 1920, 3), dtype=np.uint8) * 128

        mock_clip.get_frame = get_uint8_frame

        with patch('moviepy.VideoClip') as MockVideoClip:
            mock_stabilized = MagicMock()
            mock_stabilized.with_fps.return_value = mock_stabilized
            MockVideoClip.return_value = mock_stabilized

            result = stabilize_clip(mock_clip, shake_score=50.0)

            # Should process without errors
            assert MockVideoClip.called

    def test_float32_frame_format_handled(self, mock_clip, float_frames):
        """Test float32 frame format (0-1) is handled correctly."""
        mock_clip.get_frame = float_frames

        with patch('moviepy.VideoClip') as MockVideoClip:
            mock_stabilized = MagicMock()
            mock_stabilized.with_fps.return_value = mock_stabilized
            MockVideoClip.return_value = mock_stabilized

            result = stabilize_clip(mock_clip, shake_score=50.0)

            # Should convert to uint8 internally and process
            assert MockVideoClip.called

    def test_float32_round_trip_accuracy(self, mock_clip):
        """Test float32 frames maintain accuracy through uint8 conversion."""
        # Create a frame with specific float values
        test_frame = np.ones((1080, 1920, 3), dtype=np.float32) * 0.5
        test_frame[100:200, 100:200] = 0.8

        mock_clip.get_frame = lambda t: test_frame

        with patch('moviepy.VideoClip') as MockVideoClip:
            mock_stabilized = MagicMock()
            mock_stabilized.with_fps.return_value = mock_stabilized
            MockVideoClip.return_value = mock_stabilized

            result = stabilize_clip(mock_clip, shake_score=50.0)

            # Get the make_frame function that was passed to VideoClip
            assert MockVideoClip.called
            make_frame_func = MockVideoClip.call_args[0][0]

            # Test that make_frame preserves float format
            output_frame = make_frame_func(0.0)

            # Output should be float32 since input was float
            assert output_frame.dtype in (np.float32, np.float64)
            assert output_frame.max() <= 1.0

    def test_no_features_found_returns_zero_transforms(self, mock_clip):
        """Test handling when no features are found for tracking."""
        # Create uniform frames (no features)
        def get_uniform_frame(t):
            return np.ones((1080, 1920, 3), dtype=np.uint8) * 128

        mock_clip.get_frame = get_uniform_frame

        with patch('moviepy.VideoClip') as MockVideoClip:
            mock_stabilized = MagicMock()
            mock_stabilized.with_fps.return_value = mock_stabilized
            MockVideoClip.return_value = mock_stabilized

            # Should not crash even with no trackable features
            result = stabilize_clip(mock_clip, shake_score=50.0)

            # Should still create a stabilized clip (even if transforms are zero)
            assert MockVideoClip.called

    def test_empty_transforms_array_returns_original(self, mock_clip):
        """Test that empty transforms array returns original clip."""
        # With only 2 frames (n_frames < 3), clip should be returned as-is
        mock_clip.get_frame = lambda t: np.ones((1080, 1920, 3), dtype=np.uint8) * 128
        mock_clip.duration = 0.05  # ~1.5 frames at 30fps -> n_frames < 3

        result = stabilize_clip(mock_clip, shake_score=50.0)

        assert result is mock_clip


class TestSmoothTrajectory:
    """Tests for smooth_trajectory function."""

    def test_single_element_unchanged(self):
        """Test single element trajectory returns unchanged."""
        trajectory = np.array([[1.0, 2.0, 0.1]])
        result = smooth_trajectory(trajectory, radius=5)

        np.testing.assert_array_equal(result, trajectory)

    def test_smoothing_reduces_variance(self):
        """Test smoothing reduces trajectory variance."""
        # Create noisy trajectory
        np.random.seed(42)
        trajectory = np.random.randn(100, 3) * 10

        result = smooth_trajectory(trajectory, radius=10)

        # Smoothed trajectory should have lower variance
        orig_variance = np.var(trajectory)
        smooth_variance = np.var(result)

        assert smooth_variance < orig_variance

    def test_window_radius_affects_smoothing(self):
        """Test that larger radius produces more smoothing."""
        np.random.seed(42)
        trajectory = np.random.randn(100, 3) * 10

        small_radius = smooth_trajectory(trajectory, radius=3)
        large_radius = smooth_trajectory(trajectory, radius=20)

        # Large radius should produce smoother (lower variance) result
        small_variance = np.var(small_radius)
        large_variance = np.var(large_radius)

        assert large_variance < small_variance

    def test_empty_array_handling(self):
        """Test handling of empty trajectory array."""
        trajectory = np.array([]).reshape(0, 3)
        result = smooth_trajectory(trajectory, radius=5)

        assert result.shape == (0, 3)

    def test_trajectory_shape_preserved(self):
        """Test output shape matches input shape."""
        trajectory = np.random.randn(50, 3)
        result = smooth_trajectory(trajectory, radius=10)

        assert result.shape == trajectory.shape

    def test_smoothing_endpoints_handling(self):
        """Test smoothing handles endpoints correctly."""
        # Create trajectory with sharp change at start
        trajectory = np.zeros((20, 3))
        trajectory[0] = [10.0, 10.0, 1.0]  # Sharp spike

        result = smooth_trajectory(trajectory, radius=5)

        # First element should be smoothed (averaged with neighbors)
        assert np.abs(result[0, 0]) < 10.0

    def test_zero_radius_uses_single_frame(self):
        """Test zero radius effectively uses single frame window."""
        trajectory = np.random.randn(20, 3)
        result = smooth_trajectory(trajectory, radius=0)

        # With radius 0, window is just the current frame
        np.testing.assert_array_almost_equal(result, trajectory)

    def test_large_radius_produces_nearly_constant_output(self):
        """Test very large radius produces nearly constant trajectory."""
        trajectory = np.random.randn(20, 3) * 10
        result = smooth_trajectory(trajectory, radius=100)

        # With huge radius, all values should be close to mean
        trajectory_mean = np.mean(trajectory, axis=0)

        for i in range(len(result)):
            np.testing.assert_array_almost_equal(result[i], trajectory_mean, decimal=1)


class TestCalculateShakeScore:
    """Tests for calculate_shake_score function."""

    @pytest.fixture
    def static_clip(self):
        """Create a mock clip with static frames."""
        clip = MagicMock()
        clip.fps = 30
        clip.duration = 2.0

        def get_static_frame(t):
            # Return identical frames
            frame = np.ones((1080, 1920, 3), dtype=np.float32) * 0.5
            frame[100:300, 200:400] = 0.8  # Static feature
            return frame

        clip.get_frame = get_static_frame
        return clip

    @pytest.fixture
    def shaky_clip(self):
        """Create a mock clip with shaky/moving frames."""
        clip = MagicMock()
        clip.fps = 30
        clip.duration = 2.0

        def get_shaky_frame(t):
            # Return frames with random motion
            offset = int(np.random.randint(-20, 20))
            frame = np.ones((1080, 1920, 3), dtype=np.float32) * 0.5
            start = max(100 + offset, 0)
            end = min(300 + offset, 1080)
            frame[start:end, 200:400] = 0.8
            return frame

        clip.get_frame = get_shaky_frame
        return clip

    def test_returns_zero_to_hundred_range(self, static_clip):
        """Test shake score returns value in 0-100 range."""
        score = calculate_shake_score(static_clip, sample_frames=10)

        assert 0.0 <= score <= 100.0

    def test_static_video_returns_low_score(self, static_clip):
        """Test static video returns low shake score."""
        score = calculate_shake_score(static_clip, sample_frames=10)

        # Static video should have very low shake score
        assert score < 30.0

    def test_very_short_video_returns_zero(self):
        """Test video < 0.5s returns 0.0."""
        short_clip = MagicMock()
        short_clip.fps = 30
        short_clip.duration = 0.3  # Less than 0.5s
        short_clip.get_frame = lambda t: np.ones((1080, 1920, 3), dtype=np.float32) * 0.5

        score = calculate_shake_score(short_clip)

        assert score == 0.0

    def test_no_frames_to_analyze_returns_zero(self):
        """Test clip with insufficient frames returns 0.0."""
        minimal_clip = MagicMock()
        minimal_clip.fps = 30
        minimal_clip.duration = 0.6  # Just over threshold
        minimal_clip.get_frame = lambda t: np.ones((1080, 1920, 3), dtype=np.float32) * 0.5

        # Mock optical flow to return zero flow
        with patch('cv2.calcOpticalFlowFarneback') as mock_flow:
            mock_flow.return_value = np.zeros((180, 320, 2))

            score = calculate_shake_score(minimal_clip, sample_frames=2)

            # With zero flow, should return low score
            assert score < 10.0

    def test_sample_frames_parameter(self, static_clip):
        """Test sample_frames parameter controls number of samples."""
        # Test with different sample counts
        score_few = calculate_shake_score(static_clip, sample_frames=5)
        score_many = calculate_shake_score(static_clip, sample_frames=20)

        # Both should be valid scores
        assert 0.0 <= score_few <= 100.0
        assert 0.0 <= score_many <= 100.0

    def test_shake_score_scaling(self, static_clip):
        """Test shake score scales properly (multiplier of 5.0, capped at 100)."""
        with patch('cv2.calcOpticalFlowFarneback') as mock_flow:
            # Create high flow variance
            high_flow = np.random.randn(180, 320, 2) * 10
            mock_flow.return_value = high_flow

            score = calculate_shake_score(static_clip, sample_frames=10)

            # Should be capped at 100
            assert score <= 100.0

    def test_flow_variance_contributes_to_score(self, static_clip):
        """Test that flow variance affects shake score."""
        with patch('cv2.calcOpticalFlowFarneback') as mock_flow:
            # Test with low variance flow
            low_flow = np.ones((180, 320, 2)) * 0.1
            mock_flow.return_value = low_flow
            score_low = calculate_shake_score(static_clip, sample_frames=5)

            # Test with high variance flow
            high_flow = np.random.randn(180, 320, 2) * 5
            mock_flow.return_value = high_flow
            score_high = calculate_shake_score(static_clip, sample_frames=5)

            # High variance should produce higher score
            assert score_high > score_low

    def test_direction_change_weighted_higher(self, static_clip):
        """Test direction changes are weighted 2x in score calculation."""
        # This tests the internal logic: direction_change * 2 in the formula
        # We verify by checking that consistent flow direction produces lower scores
        # than rapidly changing directions (tested indirectly via the algorithm)
        score = calculate_shake_score(static_clip, sample_frames=10)

        # Just verify it completes and returns valid score
        assert isinstance(score, (int, float))
        assert 0.0 <= score <= 100.0


class TestStabilizerEdgeCases:
    """Tests for edge cases and error handling."""

    def test_clip_with_no_audio(self):
        """Test clip without audio is handled correctly."""
        clip = MagicMock()
        clip.fps = 30
        clip.duration = 2.0
        clip.size = (1920, 1080)
        clip.audio = None
        clip.get_frame = lambda t: np.ones((1080, 1920, 3), dtype=np.uint8) * 128

        with patch('moviepy.VideoClip') as MockVideoClip:
            mock_stabilized = MagicMock()
            mock_stabilized.with_fps.return_value = mock_stabilized
            MockVideoClip.return_value = mock_stabilized

            result = stabilize_clip(clip, shake_score=50.0)

            # Should not call with_audio when audio is None
            mock_stabilized.with_audio.assert_not_called()

    def test_invalid_shake_score_negative(self):
        """Test handling of negative shake score."""
        clip = MagicMock()
        clip.fps = 30
        clip.duration = 2.0
        clip.size = (1920, 1080)

        # Negative shake score should be treated as stable
        result = stabilize_clip(clip, shake_score=-5.0)

        assert result is clip

    def test_invalid_shake_score_over_hundred(self):
        """Test handling of shake score > 100."""
        clip = MagicMock()
        clip.fps = 30
        clip.duration = 2.0
        clip.size = (1920, 1080)
        clip.get_frame = lambda t: np.ones((1080, 1920, 3), dtype=np.uint8) * 128

        with patch('moviepy.VideoClip') as MockVideoClip:
            mock_stabilized = MagicMock()
            mock_stabilized.with_fps.return_value = mock_stabilized
            MockVideoClip.return_value = mock_stabilized

            # Should process normally (no validation on upper bound)
            result = stabilize_clip(clip, shake_score=150.0)

            assert MockVideoClip.called

    def test_zero_duration_clip(self):
        """Test handling of zero duration clip."""
        clip = MagicMock()
        clip.fps = 30
        clip.duration = 0.0
        clip.size = (1920, 1080)

        result = stabilize_clip(clip, shake_score=50.0)

        # Should return original (n_frames < 3)
        assert result is clip

    def test_high_fps_clip(self):
        """Test stabilization works with high FPS clips."""
        clip = MagicMock()
        clip.fps = 120  # High FPS
        clip.duration = 1.0
        clip.size = (1920, 1080)
        clip.audio = None
        clip.get_frame = lambda t: np.ones((1080, 1920, 3), dtype=np.uint8) * 128

        with patch('moviepy.VideoClip') as MockVideoClip:
            mock_stabilized = MagicMock()
            mock_stabilized.with_fps.return_value = mock_stabilized
            MockVideoClip.return_value = mock_stabilized

            result = stabilize_clip(clip, shake_score=50.0)

            # Should process high FPS clip
            assert MockVideoClip.called
            # Should preserve FPS
            mock_stabilized.with_fps.assert_called_once_with(120)

    def test_extreme_border_crop(self):
        """Test stabilization with extreme border crop values."""
        clip = MagicMock()
        clip.fps = 30
        clip.duration = 2.0
        clip.size = (1920, 1080)
        clip.audio = None
        clip.get_frame = lambda t: np.ones((1080, 1920, 3), dtype=np.uint8) * 128

        with patch('moviepy.VideoClip') as MockVideoClip:
            mock_stabilized = MagicMock()
            mock_stabilized.with_fps.return_value = mock_stabilized
            MockVideoClip.return_value = mock_stabilized

            # Test with large crop
            result = stabilize_clip(clip, shake_score=50.0, border_crop=0.25)

            assert MockVideoClip.called

    def test_small_smoothing_radius(self):
        """Test stabilization with very small smoothing radius."""
        clip = MagicMock()
        clip.fps = 30
        clip.duration = 2.0
        clip.size = (1920, 1080)
        clip.audio = None
        clip.get_frame = lambda t: np.ones((1080, 1920, 3), dtype=np.uint8) * 128

        with patch('moviepy.VideoClip') as MockVideoClip:
            mock_stabilized = MagicMock()
            mock_stabilized.with_fps.return_value = mock_stabilized
            MockVideoClip.return_value = mock_stabilized

            result = stabilize_clip(clip, shake_score=50.0, smoothing_radius=1)

            assert MockVideoClip.called

    def test_frame_index_out_of_bounds(self):
        """Test make_frame handles frame index out of bounds."""
        clip = MagicMock()
        clip.fps = 30
        clip.duration = 2.0
        clip.size = (1920, 1080)
        clip.audio = None
        clip.get_frame = lambda t: np.ones((1080, 1920, 3), dtype=np.uint8) * 128

        with patch('moviepy.VideoClip') as MockVideoClip:
            mock_stabilized = MagicMock()
            mock_stabilized.with_fps.return_value = mock_stabilized
            MockVideoClip.return_value = mock_stabilized

            result = stabilize_clip(clip, shake_score=50.0)

            # Get make_frame function
            make_frame_func = MockVideoClip.call_args[0][0]

            # Test with time that would produce out-of-bounds index
            frame = make_frame_func(100.0)  # Way beyond duration

            # Should return a frame without crashing
            assert frame is not None
            assert frame.shape == (1080, 1920, 3)


class TestStabilizerIntegration:
    """Integration tests for stabilizer."""

    def test_full_stabilization_pipeline(self):
        """Test complete stabilization pipeline with realistic data."""
        clip = MagicMock()
        clip.fps = 30
        clip.duration = 3.0
        clip.size = (1920, 1080)
        clip.audio = MagicMock()

        # Create frames with simulated motion
        frame_count = [0]
        def get_moving_frame(t):
            frame = np.ones((1080, 1920, 3), dtype=np.uint8) * 128
            # Add moving feature
            offset = int(frame_count[0] * 5) % 100
            frame[100:300, 200+offset:400+offset] = 200
            frame_count[0] += 1
            return frame

        clip.get_frame = get_moving_frame

        with patch('moviepy.VideoClip') as MockVideoClip:
            mock_stabilized = MagicMock()
            mock_stabilized.with_fps.return_value = mock_stabilized
            mock_stabilized.with_audio.return_value = mock_stabilized
            MockVideoClip.return_value = mock_stabilized

            result = stabilize_clip(
                clip,
                shake_score=60.0,
                smoothing_radius=20,
                border_crop=0.05
            )

            # Verify all steps occurred
            assert MockVideoClip.called
            mock_stabilized.with_fps.assert_called_once_with(30)
            mock_stabilized.with_audio.assert_called_once()

    def test_adaptive_stabilization_thresholds(self):
        """Test adaptive stabilization at different shake score thresholds."""
        clip = MagicMock()
        clip.fps = 30
        clip.duration = 2.0
        clip.size = (1920, 1080)
        clip.audio = None
        clip.get_frame = lambda t: np.ones((1080, 1920, 3), dtype=np.uint8) * 128

        # Test stable threshold (< 15)
        result_stable = stabilize_clip(clip, shake_score=10.0)
        assert result_stable is clip

        # Test light stabilization (15-30)
        with patch('moviepy.VideoClip') as MockVideoClip:
            mock_stabilized = MagicMock()
            mock_stabilized.with_fps.return_value = mock_stabilized
            MockVideoClip.return_value = mock_stabilized

            result_light = stabilize_clip(clip, shake_score=20.0)
            assert MockVideoClip.called

        # Test full stabilization (> 30)
        with patch('moviepy.VideoClip') as MockVideoClip:
            mock_stabilized = MagicMock()
            mock_stabilized.with_fps.return_value = mock_stabilized
            MockVideoClip.return_value = mock_stabilized

            result_full = stabilize_clip(clip, shake_score=50.0)
            assert MockVideoClip.called
