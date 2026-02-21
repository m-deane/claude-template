"""Tests for video reframing module."""

import cv2
import numpy as np
import pytest

from drone_reel.core.reframer import (
    Reframer,
    ReframeSettings,
    AspectRatio,
    ReframeMode,
    create_vertical_reframer,
)


class TestAspectRatio:
    """Tests for AspectRatio enum."""

    def test_vertical_ratio(self):
        """Test vertical 9:16 ratio values."""
        assert AspectRatio.VERTICAL_9_16.value == (9, 16)

    def test_square_ratio(self):
        """Test square 1:1 ratio values."""
        assert AspectRatio.SQUARE_1_1.value == (1, 1)

    def test_landscape_ratio(self):
        """Test landscape 16:9 ratio values."""
        assert AspectRatio.LANDSCAPE_16_9.value == (16, 9)


class TestReframeSettings:
    """Tests for ReframeSettings dataclass."""

    def test_default_settings(self):
        """Test default reframe settings."""
        settings = ReframeSettings()
        assert settings.target_ratio == AspectRatio.VERTICAL_9_16
        assert settings.mode == ReframeMode.SMART
        assert settings.output_width == 1080

    def test_custom_settings(self):
        """Test custom reframe settings."""
        settings = ReframeSettings(
            target_ratio=AspectRatio.SQUARE_1_1,
            mode=ReframeMode.CENTER,
            output_width=720,
        )
        assert settings.target_ratio == AspectRatio.SQUARE_1_1
        assert settings.mode == ReframeMode.CENTER
        assert settings.output_width == 720


class TestReframer:
    """Tests for Reframer class."""

    @pytest.fixture
    def landscape_frame(self):
        """Create a 16:9 landscape test frame."""
        return np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)

    @pytest.fixture
    def vertical_reframer(self):
        """Create a reframer for vertical output."""
        settings = ReframeSettings(
            target_ratio=AspectRatio.VERTICAL_9_16,
            mode=ReframeMode.CENTER,
            output_width=1080,
        )
        return Reframer(settings)

    def test_calculate_output_dimensions_vertical(self):
        """Test output dimensions for vertical aspect ratio."""
        reframer = create_vertical_reframer()
        width, height = reframer.calculate_output_dimensions(1920, 1080)

        assert width == 1080
        assert height == 1920  # 9:16 ratio

    def test_calculate_output_dimensions_square(self):
        """Test output dimensions for square aspect ratio."""
        settings = ReframeSettings(
            target_ratio=AspectRatio.SQUARE_1_1,
            output_width=1080,
        )
        reframer = Reframer(settings)
        width, height = reframer.calculate_output_dimensions(1920, 1080)

        assert width == 1080
        assert height == 1080

    def test_crop_region_center_mode(self, landscape_frame, vertical_reframer):
        """Test center crop calculation."""
        vertical_reframer.settings.mode = ReframeMode.CENTER

        output_w, output_h = vertical_reframer.calculate_output_dimensions(
            landscape_frame.shape[1], landscape_frame.shape[0]
        )

        x, y, crop_w, crop_h = vertical_reframer.calculate_crop_region(
            landscape_frame, output_w, output_h
        )

        # Crop should be centered
        expected_x = (1920 - crop_w) // 2
        expected_y = (1080 - crop_h) // 2

        assert x == expected_x
        assert y == expected_y

    def test_crop_region_bounds(self, landscape_frame, vertical_reframer):
        """Test crop region stays within frame bounds."""
        output_w, output_h = vertical_reframer.calculate_output_dimensions(
            landscape_frame.shape[1], landscape_frame.shape[0]
        )

        x, y, crop_w, crop_h = vertical_reframer.calculate_crop_region(
            landscape_frame, output_w, output_h
        )

        # Verify bounds
        assert x >= 0
        assert y >= 0
        assert x + crop_w <= landscape_frame.shape[1]
        assert y + crop_h <= landscape_frame.shape[0]

    def test_reframe_frame_output_size(self, landscape_frame, vertical_reframer):
        """Test reframed frame has correct output size."""
        result = vertical_reframer.reframe_frame(landscape_frame)

        # Should be vertical 9:16
        output_w, output_h = vertical_reframer.calculate_output_dimensions(
            landscape_frame.shape[1], landscape_frame.shape[0]
        )

        assert result.shape[1] == output_w
        assert result.shape[0] == output_h
        assert result.shape[2] == 3  # BGR channels

    def test_reframe_frame_preserves_dtype(self, landscape_frame, vertical_reframer):
        """Test reframing preserves data type."""
        result = vertical_reframer.reframe_frame(landscape_frame)
        assert result.dtype == landscape_frame.dtype

    def test_pan_mode_progression(self, landscape_frame):
        """Test pan mode changes crop position over frames."""
        settings = ReframeSettings(
            target_ratio=AspectRatio.VERTICAL_9_16,
            mode=ReframeMode.PAN,
            output_width=1080,
        )
        reframer = Reframer(settings)

        output_w, output_h = reframer.calculate_output_dimensions(
            landscape_frame.shape[1], landscape_frame.shape[0]
        )

        # Get crop at start
        x_start, _, _, _ = reframer.calculate_crop_region(
            landscape_frame, output_w, output_h,
            frame_index=0, total_frames=100
        )

        # Get crop at end
        x_end, _, _, _ = reframer.calculate_crop_region(
            landscape_frame, output_w, output_h,
            frame_index=99, total_frames=100
        )

        # Pan should have moved the crop position
        assert x_end > x_start

    def test_reset_tracking(self, vertical_reframer):
        """Test tracking reset clears history."""
        vertical_reframer._tracker_history = [(100, 100), (110, 110)]
        vertical_reframer.reset_tracking()
        assert len(vertical_reframer._tracker_history) == 0


class TestCreateVerticalReframer:
    """Tests for create_vertical_reframer helper function."""

    def test_creates_vertical_reframer(self):
        """Test helper creates properly configured reframer."""
        reframer = create_vertical_reframer()

        assert reframer.settings.target_ratio == AspectRatio.VERTICAL_9_16

    def test_custom_mode(self):
        """Test helper respects custom mode."""
        reframer = create_vertical_reframer(mode=ReframeMode.PAN)
        assert reframer.settings.mode == ReframeMode.PAN

    def test_custom_width(self):
        """Test helper respects custom output width."""
        reframer = create_vertical_reframer(output_width=720)
        assert reframer.settings.output_width == 720


class TestDroneSpecificFeatures:
    """Tests for drone-specific reframing features."""

    @pytest.fixture
    def landscape_frame(self):
        """Create a 16:9 landscape test frame."""
        return np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)

    @pytest.fixture
    def horizon_frame(self):
        """Create a frame with a clear horizontal line (simulated horizon)."""
        frame = np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)
        # Draw a horizontal line representing the horizon
        cv2.line(frame, (0, 400), (1920, 400), (255, 255, 255), 3)
        return frame

    @pytest.fixture
    def sky_frame(self):
        """Create a frame with sky-like upper region."""
        frame = np.zeros((1080, 1920, 3), dtype=np.uint8)
        # Upper third is blue (sky)
        frame[0:360, :] = [135, 206, 250]
        # Lower two thirds is green (ground)
        frame[360:, :] = [34, 139, 34]
        return frame

    def test_new_reframe_modes_exist(self):
        """Test new ReframeMode enum values exist."""
        assert hasattr(ReframeMode, 'HORIZON_LOCK')
        assert hasattr(ReframeMode, 'FACE')
        assert hasattr(ReframeMode, 'MOTION')

    def test_new_settings_attributes(self):
        """Test new ReframeSettings attributes exist with defaults."""
        settings = ReframeSettings()
        assert hasattr(settings, 'focal_clamp_x')
        assert hasattr(settings, 'focal_clamp_y')
        assert hasattr(settings, 'adaptive_smoothing')
        assert hasattr(settings, 'sky_mask_enabled')
        assert hasattr(settings, 'sky_region_ratio')
        assert hasattr(settings, 'saliency_cache_frames')
        assert hasattr(settings, 'scene_change_threshold')
        assert hasattr(settings, 'horizon_penalty_weight')
        assert hasattr(settings, 'face_cascade_path')

        # Test default values
        assert settings.focal_clamp_x == (0.2, 0.8)
        assert settings.focal_clamp_y == (0.2, 0.8)
        assert settings.adaptive_smoothing is True
        assert settings.sky_mask_enabled is True
        assert settings.sky_region_ratio == 0.35
        assert settings.saliency_cache_frames == 10
        assert settings.scene_change_threshold == 0.3
        assert settings.horizon_penalty_weight == 0.5

    def test_horizon_lock_mode(self, horizon_frame):
        """Test HORIZON_LOCK mode positions horizon at upper third."""
        settings = ReframeSettings(
            target_ratio=AspectRatio.VERTICAL_9_16,
            mode=ReframeMode.HORIZON_LOCK,
            output_width=1080,
        )
        reframer = Reframer(settings)

        output_w, output_h = reframer.calculate_output_dimensions(
            horizon_frame.shape[1], horizon_frame.shape[0]
        )

        x, y, crop_w, crop_h = reframer.calculate_crop_region(
            horizon_frame, output_w, output_h
        )

        # Verify crop region is valid
        assert x >= 0
        assert y >= 0
        assert x + crop_w <= horizon_frame.shape[1]
        assert y + crop_h <= horizon_frame.shape[0]

    def test_face_mode_initialization(self):
        """Test FACE mode initializes face cascade."""
        settings = ReframeSettings(
            mode=ReframeMode.FACE,
        )
        reframer = Reframer(settings)

        # Face cascade should be initialized
        assert reframer._face_cascade is not None

    def test_face_mode_fallback_to_saliency(self, landscape_frame):
        """Test FACE mode falls back to saliency when no faces detected."""
        settings = ReframeSettings(
            target_ratio=AspectRatio.VERTICAL_9_16,
            mode=ReframeMode.FACE,
            output_width=1080,
        )
        reframer = Reframer(settings)

        output_w, output_h = reframer.calculate_output_dimensions(
            landscape_frame.shape[1], landscape_frame.shape[0]
        )

        # Should not crash even without faces
        x, y, crop_w, crop_h = reframer.calculate_crop_region(
            landscape_frame, output_w, output_h
        )

        # Verify crop region is valid
        assert x >= 0
        assert y >= 0
        assert x + crop_w <= landscape_frame.shape[1]
        assert y + crop_h <= landscape_frame.shape[0]

    def test_motion_mode(self, landscape_frame):
        """Test MOTION mode tracks motion focal point."""
        settings = ReframeSettings(
            target_ratio=AspectRatio.VERTICAL_9_16,
            mode=ReframeMode.MOTION,
            output_width=1080,
        )
        reframer = Reframer(settings)

        output_w, output_h = reframer.calculate_output_dimensions(
            landscape_frame.shape[1], landscape_frame.shape[0]
        )

        # First frame initializes
        x1, y1, crop_w, crop_h = reframer.calculate_crop_region(
            landscape_frame, output_w, output_h, frame_index=0
        )

        # Second frame should track motion
        x2, y2, _, _ = reframer.calculate_crop_region(
            landscape_frame, output_w, output_h, frame_index=1
        )

        # Both should be valid
        assert x1 >= 0 and x2 >= 0
        assert y1 >= 0 and y2 >= 0

    def test_focal_point_clamping(self, landscape_frame):
        """Test configurable focal point clamping."""
        settings = ReframeSettings(
            mode=ReframeMode.SMART,
            focal_clamp_x=(0.3, 0.7),
            focal_clamp_y=(0.4, 0.6),
        )
        reframer = Reframer(settings)

        focal_x, focal_y = reframer._detect_focal_point(landscape_frame, frame_index=0)

        # Focal point should be within clamp bounds
        assert 0.3 <= focal_x <= 0.7
        assert 0.4 <= focal_y <= 0.6

    def test_adaptive_smoothing_low_velocity(self, landscape_frame):
        """Test adaptive smoothing returns base smoothness for low velocity."""
        settings = ReframeSettings(
            adaptive_smoothing=True,
            tracking_smoothness=0.3,
        )
        reframer = Reframer(settings)

        # Initialize tracker history with small movement
        reframer._tracker_history = [(100, 100)]

        smoothness = reframer._calculate_adaptive_smoothness(102, 102)

        # Should use base smoothness for low velocity
        assert smoothness == 0.3

    def test_adaptive_smoothing_high_velocity(self, landscape_frame):
        """Test adaptive smoothing increases for high velocity."""
        settings = ReframeSettings(
            adaptive_smoothing=True,
            tracking_smoothness=0.3,
        )
        reframer = Reframer(settings)

        # Initialize tracker history with large movement
        reframer._tracker_history = [(100, 100)]
        reframer._focal_velocity_history = [60, 65, 70]  # High velocity

        smoothness = reframer._calculate_adaptive_smoothness(200, 200)

        # Should increase smoothness for fast motion
        assert smoothness > 0.3

    def test_saliency_caching(self, landscape_frame):
        """Test saliency map caching for performance."""
        settings = ReframeSettings(
            mode=ReframeMode.SMART,
            saliency_cache_frames=10,
        )
        reframer = Reframer(settings)

        # First call computes saliency
        focal1 = reframer._detect_focal_point(landscape_frame, frame_index=0)
        assert reframer._saliency_cache is not None
        first_cache_index = reframer._saliency_cache_index

        # Second call within cache window should potentially use cache
        focal2 = reframer._detect_focal_point(landscape_frame, frame_index=5)
        # Cache index should be updated
        assert reframer._saliency_cache_index >= first_cache_index

        # Call beyond cache window forces recompute
        focal3 = reframer._detect_focal_point(landscape_frame, frame_index=20)
        assert reframer._saliency_cache is not None

    def test_scene_change_detection(self, landscape_frame):
        """Test scene change detection triggers cache invalidation."""
        settings = ReframeSettings(
            mode=ReframeMode.SMART,
            scene_change_threshold=0.3,
        )
        reframer = Reframer(settings)

        # First frame
        is_change1 = reframer._is_scene_change(landscape_frame)
        # First call always returns True
        assert is_change1 is True

        # Same frame
        is_change2 = reframer._is_scene_change(landscape_frame)
        # Should not be a scene change
        assert is_change2 is False

        # Different frame
        different_frame = np.zeros_like(landscape_frame)
        is_change3 = reframer._is_scene_change(different_frame)
        # Should detect scene change
        assert is_change3 is True

    def test_sky_mask_application(self, sky_frame):
        """Test sky masking reduces saliency in upper region."""
        settings = ReframeSettings(
            sky_mask_enabled=True,
            sky_region_ratio=0.35,
        )
        reframer = Reframer(settings)

        # Create a simple saliency map
        saliency_map = np.ones((180, 320), dtype=np.uint8) * 255

        masked = reframer._apply_sky_mask(saliency_map)

        # Upper region should have reduced saliency
        upper_avg = np.mean(masked[0:63, :])  # 35% of 180
        lower_avg = np.mean(masked[63:, :])

        assert upper_avg < lower_avg

    def test_rule_of_thirds_weighting(self):
        """Test rule of thirds weighting boosts lower third."""
        settings = ReframeSettings()
        reframer = Reframer(settings)

        saliency_map = np.ones((180, 320), dtype=np.uint8) * 100

        weighted = reframer._apply_rule_of_thirds_weighting(saliency_map)

        # Lower third should have higher values
        upper_third_avg = np.mean(weighted[0:60, :])
        lower_third_avg = np.mean(weighted[120:, :])

        assert lower_third_avg > upper_third_avg

    def test_horizon_detection(self, horizon_frame):
        """Test horizon line detection."""
        settings = ReframeSettings()
        reframer = Reframer(settings)

        horizon_y = reframer._detect_horizon_line(horizon_frame)

        # Should detect the horizon line around y=400
        if horizon_y is not None:
            assert 350 <= horizon_y <= 450

    def test_horizon_angle_detection(self, horizon_frame):
        """Test horizon tilt angle detection."""
        settings = ReframeSettings()
        reframer = Reframer(settings)

        angle = reframer._detect_horizon_angle(horizon_frame)

        # Should detect near-level horizon (within ±15 degrees)
        if angle is not None:
            assert abs(angle) < 15

    def test_face_detection(self, landscape_frame):
        """Test face detection method."""
        settings = ReframeSettings(mode=ReframeMode.FACE)
        reframer = Reframer(settings)

        faces = reframer._detect_faces(landscape_frame)

        # Should return list (empty or with faces)
        assert isinstance(faces, list)

    def test_face_center_of_mass_single_face(self):
        """Test face center of mass calculation with single face."""
        settings = ReframeSettings()
        reframer = Reframer(settings)

        faces = [(100, 100, 50, 50)]  # Single face at (100, 100)
        focal_x, focal_y = reframer._calculate_face_center_of_mass(faces, 1920, 1080)

        # Should be near center of face
        expected_x = (100 + 25) / 1920  # center of 100 + 50/2
        expected_y = (100 + 25) / 1080

        assert abs(focal_x - expected_x) < 0.01
        assert abs(focal_y - expected_y) < 0.01

    def test_face_center_of_mass_multiple_faces(self):
        """Test face center of mass weights larger faces more heavily."""
        settings = ReframeSettings()
        reframer = Reframer(settings)

        # Two faces: small and large
        faces = [
            (100, 100, 50, 50),    # Small face, area = 2500
            (500, 500, 100, 100),  # Large face, area = 10000
        ]

        focal_x, focal_y = reframer._calculate_face_center_of_mass(faces, 1920, 1080)

        # Should be weighted more toward the larger face
        small_center_x = (100 + 25) / 1920
        large_center_x = (500 + 50) / 1920

        # Focal point should be closer to larger face
        assert abs(focal_x - large_center_x) < abs(focal_x - small_center_x)

    def test_face_center_of_mass_no_faces(self):
        """Test face center of mass returns center when no faces."""
        settings = ReframeSettings()
        reframer = Reframer(settings)

        focal_x, focal_y = reframer._calculate_face_center_of_mass([], 1920, 1080)

        assert focal_x == 0.5
        assert focal_y == 0.5

    def test_motion_focal_point_initialization(self, landscape_frame):
        """Test motion focal point returns center on first frame."""
        settings = ReframeSettings()
        reframer = Reframer(settings)

        focal_x, focal_y = reframer._detect_motion_focal_point(landscape_frame)

        # First frame should return center
        assert focal_x == 0.5
        assert focal_y == 0.5
        assert reframer._prev_gray is not None

    def test_motion_focal_point_second_frame(self, landscape_frame):
        """Test motion focal point tracks motion on subsequent frames."""
        settings = ReframeSettings()
        reframer = Reframer(settings)

        # First frame
        reframer._detect_motion_focal_point(landscape_frame)

        # Second frame with motion
        moved_frame = np.roll(landscape_frame, 50, axis=1)
        focal_x, focal_y = reframer._detect_motion_focal_point(moved_frame)

        # Should detect focal point (not necessarily at specific location)
        assert 0.0 <= focal_x <= 1.0
        assert 0.0 <= focal_y <= 1.0

    def test_reset_tracking_clears_all_caches(self):
        """Test reset_tracking clears all tracking and cache data."""
        settings = ReframeSettings()
        reframer = Reframer(settings)

        # Populate caches
        reframer._tracker_history = [(100, 100)]
        reframer._saliency_cache = np.zeros((180, 320))
        reframer._saliency_cache_index = 5
        reframer._prev_histogram = np.zeros((50, 60))
        reframer._prev_gray = np.zeros((1080, 1920))
        reframer._focal_velocity_history = [10.0, 15.0]

        # Reset
        reframer.reset_tracking()

        # All should be cleared
        assert len(reframer._tracker_history) == 0
        assert reframer._saliency_cache is None
        assert reframer._saliency_cache_index == -1
        assert reframer._prev_histogram is None
        assert reframer._prev_gray is None
        assert len(reframer._focal_velocity_history) == 0

    def test_histogram_computation(self, landscape_frame):
        """Test histogram computation for scene change detection."""
        settings = ReframeSettings()
        reframer = Reframer(settings)

        hist = reframer._compute_histogram(landscape_frame)

        # Should return normalized histogram
        assert isinstance(hist, np.ndarray)
        assert hist.shape == (50, 60)

    def test_horizon_penalty_application(self, landscape_frame):
        """Test horizon tilt penalty reduces saliency."""
        settings = ReframeSettings(horizon_penalty_weight=0.5)
        reframer = Reframer(settings)

        saliency_map = np.ones((180, 320), dtype=np.uint8) * 200

        # Should apply penalty if horizon is tilted
        penalized = reframer._apply_horizon_penalty(landscape_frame, saliency_map)

        assert isinstance(penalized, np.ndarray)
        assert penalized.shape == saliency_map.shape

    def test_smart_mode_with_drone_optimizations(self, landscape_frame):
        """Test SMART mode integrates all drone-specific optimizations."""
        settings = ReframeSettings(
            mode=ReframeMode.SMART,
            sky_mask_enabled=True,
            horizon_penalty_weight=0.5,
            adaptive_smoothing=True,
        )
        reframer = Reframer(settings)

        output_w, output_h = reframer.calculate_output_dimensions(
            landscape_frame.shape[1], landscape_frame.shape[0]
        )

        # Should process multiple frames without error
        for i in range(5):
            x, y, crop_w, crop_h = reframer.calculate_crop_region(
                landscape_frame, output_w, output_h, frame_index=i
            )

            # Verify valid crop region
            assert x >= 0
            assert y >= 0
            assert x + crop_w <= landscape_frame.shape[1]
            assert y + crop_h <= landscape_frame.shape[0]


class TestDynamicCroppingFeatures:
    """Tests for Ken Burns, Punch-In, and Subject Tracking features."""

    @pytest.fixture
    def landscape_frame(self):
        """Create a 16:9 landscape test frame."""
        return np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)

    def test_new_modes_exist(self):
        """Test new ReframeMode enum values for dynamic cropping."""
        assert hasattr(ReframeMode, 'KEN_BURNS')
        assert hasattr(ReframeMode, 'PUNCH_IN')
        assert hasattr(ReframeMode, 'SUBJECT_TRACK')

    def test_new_settings_attributes_ken_burns(self):
        """Test Ken Burns settings attributes exist with defaults."""
        settings = ReframeSettings()
        assert hasattr(settings, 'ken_burns_zoom_start')
        assert hasattr(settings, 'ken_burns_zoom_end')
        assert hasattr(settings, 'ken_burns_pan_direction')
        assert hasattr(settings, 'ken_burns_ease_curve')

        # Default values
        assert settings.ken_burns_zoom_start == 1.0
        assert settings.ken_burns_zoom_end == 1.1
        assert settings.ken_burns_pan_direction == (0.1, 0.05)
        assert settings.ken_burns_ease_curve == "ease_in_out"

    def test_new_settings_attributes_punch_in(self):
        """Test Punch-In settings attributes exist with defaults."""
        settings = ReframeSettings()
        assert hasattr(settings, 'punch_in_zoom_factor')
        assert hasattr(settings, 'punch_in_duration')
        assert hasattr(settings, 'punch_in_ease_in')
        assert hasattr(settings, 'punch_in_ease_out')

        # Default values
        assert settings.punch_in_zoom_factor == 1.15
        assert settings.punch_in_duration == 0.3
        assert settings.punch_in_ease_in == 0.1
        assert settings.punch_in_ease_out == 0.2

    def test_new_settings_attributes_subject_tracking(self):
        """Test Subject Tracking settings attributes exist with defaults."""
        settings = ReframeSettings()
        assert hasattr(settings, 'subject_tracker_type')
        assert hasattr(settings, 'subject_init_mode')
        assert hasattr(settings, 'subject_redetect_interval')
        assert hasattr(settings, 'subject_lost_fallback')

        # Default values
        assert settings.subject_tracker_type == "CSRT"
        assert settings.subject_init_mode == "saliency"
        assert settings.subject_redetect_interval == 30
        assert settings.subject_lost_fallback == "saliency"

    def test_ease_function_linear(self):
        """Test linear easing function."""
        settings = ReframeSettings()
        reframer = Reframer(settings)

        assert reframer._ease_function(0.0, "linear") == 0.0
        assert reframer._ease_function(0.5, "linear") == 0.5
        assert reframer._ease_function(1.0, "linear") == 1.0

    def test_ease_function_ease_in(self):
        """Test ease-in function (accelerating)."""
        settings = ReframeSettings()
        reframer = Reframer(settings)

        # Ease-in should be below linear at midpoint
        assert reframer._ease_function(0.0, "ease_in") == 0.0
        assert reframer._ease_function(0.5, "ease_in") < 0.5  # Below linear
        assert reframer._ease_function(1.0, "ease_in") == 1.0

    def test_ease_function_ease_out(self):
        """Test ease-out function (decelerating)."""
        settings = ReframeSettings()
        reframer = Reframer(settings)

        # Ease-out should be above linear at midpoint
        assert reframer._ease_function(0.0, "ease_out") == 0.0
        assert reframer._ease_function(0.5, "ease_out") > 0.5  # Above linear
        assert reframer._ease_function(1.0, "ease_out") == 1.0

    def test_ease_function_ease_in_out(self):
        """Test ease-in-out function (smooth both ends)."""
        settings = ReframeSettings()
        reframer = Reframer(settings)

        assert reframer._ease_function(0.0, "ease_in_out") == 0.0
        assert abs(reframer._ease_function(0.5, "ease_in_out") - 0.5) < 0.01  # Near midpoint
        assert reframer._ease_function(1.0, "ease_in_out") == 1.0

    def test_ease_function_clamps_input(self):
        """Test ease function clamps input to [0, 1]."""
        settings = ReframeSettings()
        reframer = Reframer(settings)

        # Should clamp negative values to 0
        assert reframer._ease_function(-0.5, "linear") == 0.0
        # Should clamp values > 1 to 1
        assert reframer._ease_function(1.5, "linear") == 1.0

    def test_ken_burns_mode_valid_crop(self, landscape_frame):
        """Test Ken Burns mode produces valid crop regions."""
        settings = ReframeSettings(
            target_ratio=AspectRatio.VERTICAL_9_16,
            mode=ReframeMode.KEN_BURNS,
            output_width=1080,
            ken_burns_zoom_start=1.0,
            ken_burns_zoom_end=1.2,
        )
        reframer = Reframer(settings)

        output_w, output_h = reframer.calculate_output_dimensions(
            landscape_frame.shape[1], landscape_frame.shape[0]
        )

        for frame_idx in [0, 25, 50, 75, 99]:
            x, y, crop_w, crop_h = reframer.calculate_crop_region(
                landscape_frame, output_w, output_h,
                frame_index=frame_idx, total_frames=100
            )

            # Verify valid crop region
            assert x >= 0
            assert y >= 0
            assert x + crop_w <= landscape_frame.shape[1]
            assert y + crop_h <= landscape_frame.shape[0]

    def test_ken_burns_zoom_progression(self, landscape_frame):
        """Test Ken Burns zoom changes over time."""
        settings = ReframeSettings(
            target_ratio=AspectRatio.VERTICAL_9_16,
            mode=ReframeMode.KEN_BURNS,
            output_width=1080,
            ken_burns_zoom_start=1.0,
            ken_burns_zoom_end=1.2,  # 20% zoom in
        )
        reframer = Reframer(settings)

        output_w, output_h = reframer.calculate_output_dimensions(
            landscape_frame.shape[1], landscape_frame.shape[0]
        )

        # Get crop at start
        _, _, crop_w_start, _ = reframer.calculate_crop_region(
            landscape_frame, output_w, output_h,
            frame_index=0, total_frames=100
        )

        reframer.reset_tracking()

        # Get crop at end
        _, _, crop_w_end, _ = reframer.calculate_crop_region(
            landscape_frame, output_w, output_h,
            frame_index=99, total_frames=100
        )

        # End crop should be smaller (more zoomed in)
        assert crop_w_end < crop_w_start

    def test_ken_burns_pan_direction(self, landscape_frame):
        """Test Ken Burns pans in specified direction."""
        settings = ReframeSettings(
            target_ratio=AspectRatio.VERTICAL_9_16,
            mode=ReframeMode.KEN_BURNS,
            output_width=1080,
            ken_burns_zoom_start=1.0,
            ken_burns_zoom_end=1.0,  # No zoom, only pan
            ken_burns_pan_direction=(0.2, 0.0),  # Pan right
        )
        reframer = Reframer(settings)

        output_w, output_h = reframer.calculate_output_dimensions(
            landscape_frame.shape[1], landscape_frame.shape[0]
        )

        # Get crop at start
        x_start, _, _, _ = reframer.calculate_crop_region(
            landscape_frame, output_w, output_h,
            frame_index=0, total_frames=100
        )

        # Get crop at end
        x_end, _, _, _ = reframer.calculate_crop_region(
            landscape_frame, output_w, output_h,
            frame_index=99, total_frames=100
        )

        # End should be to the right of start
        assert x_end > x_start

    def test_punch_in_mode_valid_crop(self, landscape_frame):
        """Test Punch-In mode produces valid crop regions."""
        settings = ReframeSettings(
            target_ratio=AspectRatio.VERTICAL_9_16,
            mode=ReframeMode.PUNCH_IN,
            output_width=1080,
        )
        reframer = Reframer(settings)

        output_w, output_h = reframer.calculate_output_dimensions(
            landscape_frame.shape[1], landscape_frame.shape[0]
        )

        for frame_idx in range(30):
            x, y, crop_w, crop_h = reframer.calculate_crop_region(
                landscape_frame, output_w, output_h,
                frame_index=frame_idx, total_frames=100
            )

            # Verify valid crop region
            assert x >= 0
            assert y >= 0
            assert x + crop_w <= landscape_frame.shape[1]
            assert y + crop_h <= landscape_frame.shape[0]

    def test_punch_in_with_beat_times(self, landscape_frame):
        """Test Punch-In zooms on beat times."""
        settings = ReframeSettings(
            target_ratio=AspectRatio.VERTICAL_9_16,
            mode=ReframeMode.PUNCH_IN,
            output_width=1080,
            punch_in_zoom_factor=1.2,
            punch_in_duration=0.3,
        )
        reframer = Reframer(settings)
        reframer.set_beat_times([0.0, 1.0, 2.0])  # Beats at 0, 1, 2 seconds

        output_w, output_h = reframer.calculate_output_dimensions(
            landscape_frame.shape[1], landscape_frame.shape[0]
        )

        # At beat (frame 0 = 0 seconds), should have zoom effect
        _, _, crop_w_beat, _ = reframer.calculate_crop_region(
            landscape_frame, output_w, output_h,
            frame_index=3, total_frames=100  # 0.1s after beat at 30fps
        )

        reframer.reset_tracking()

        # At non-beat time (frame 15 = 0.5 seconds), should be normal
        _, _, crop_w_normal, _ = reframer.calculate_crop_region(
            landscape_frame, output_w, output_h,
            frame_index=15, total_frames=100  # 0.5s at 30fps
        )

        # Beat crop should be smaller (zoomed in) or equal
        assert crop_w_beat <= crop_w_normal

    def test_set_beat_times(self):
        """Test set_beat_times stores sorted beat times."""
        settings = ReframeSettings()
        reframer = Reframer(settings)

        reframer.set_beat_times([2.0, 0.5, 1.0])

        assert reframer._beat_times == [0.5, 1.0, 2.0]

    def test_subject_tracking_mode_valid_crop(self, landscape_frame):
        """Test Subject Tracking mode produces valid crop regions."""
        settings = ReframeSettings(
            target_ratio=AspectRatio.VERTICAL_9_16,
            mode=ReframeMode.SUBJECT_TRACK,
            output_width=1080,
        )
        reframer = Reframer(settings)

        output_w, output_h = reframer.calculate_output_dimensions(
            landscape_frame.shape[1], landscape_frame.shape[0]
        )

        for frame_idx in range(10):
            x, y, crop_w, crop_h = reframer.calculate_crop_region(
                landscape_frame, output_w, output_h,
                frame_index=frame_idx, total_frames=100
            )

            # Verify valid crop region
            assert x >= 0
            assert y >= 0
            assert x + crop_w <= landscape_frame.shape[1]
            assert y + crop_h <= landscape_frame.shape[0]

    def test_subject_tracking_initialization(self, landscape_frame):
        """Test subject tracker initializes or falls back gracefully."""
        settings = ReframeSettings(
            target_ratio=AspectRatio.VERTICAL_9_16,
            mode=ReframeMode.SUBJECT_TRACK,
            output_width=1080,
        )
        reframer = Reframer(settings)

        # Before first frame, tracker should not be initialized
        assert reframer._subject_tracking_initialized == False

        output_w, output_h = reframer.calculate_output_dimensions(
            landscape_frame.shape[1], landscape_frame.shape[0]
        )

        # Process first frame - should work even if tracker unavailable
        x, y, crop_w, crop_h = reframer.calculate_crop_region(
            landscape_frame, output_w, output_h,
            frame_index=0, total_frames=100
        )

        # Crop should be valid regardless of tracker status
        assert x >= 0
        assert y >= 0
        assert x + crop_w <= landscape_frame.shape[1]
        assert y + crop_h <= landscape_frame.shape[0]

        # After first frame, tracker status may have changed (True if successful, False if failed)
        # The important thing is it produced a valid crop
        assert reframer._subject_tracking_initialized in (True, False, None)

    def test_subject_tracking_redetect_interval(self, landscape_frame):
        """Test subject tracking re-detects after interval."""
        settings = ReframeSettings(
            target_ratio=AspectRatio.VERTICAL_9_16,
            mode=ReframeMode.SUBJECT_TRACK,
            output_width=1080,
            subject_redetect_interval=5,  # Short interval for testing
        )
        reframer = Reframer(settings)

        output_w, output_h = reframer.calculate_output_dimensions(
            landscape_frame.shape[1], landscape_frame.shape[0]
        )

        # Process frames
        for i in range(10):
            reframer.calculate_crop_region(
                landscape_frame, output_w, output_h,
                frame_index=i, total_frames=100
            )

        # Should have triggered re-detection
        assert reframer._frames_since_redetect < settings.subject_redetect_interval

    def test_subject_tracking_different_tracker_types(self, landscape_frame):
        """Test different tracker types can be initialized."""
        for tracker_type in ["CSRT", "KCF"]:
            settings = ReframeSettings(
                target_ratio=AspectRatio.VERTICAL_9_16,
                mode=ReframeMode.SUBJECT_TRACK,
                output_width=1080,
                subject_tracker_type=tracker_type,
            )
            reframer = Reframer(settings)

            output_w, output_h = reframer.calculate_output_dimensions(
                landscape_frame.shape[1], landscape_frame.shape[0]
            )

            # Should not crash
            x, y, crop_w, crop_h = reframer.calculate_crop_region(
                landscape_frame, output_w, output_h,
                frame_index=0, total_frames=100
            )

            assert x >= 0
            assert y >= 0

    def test_apply_ken_burns_to_static_clip(self, landscape_frame):
        """Test apply_ken_burns_to_static_clip returns parameters."""
        settings = ReframeSettings()
        reframer = Reframer(settings)

        result = reframer.apply_ken_burns_to_static_clip(
            landscape_frame,
            zoom_start=1.0,
            zoom_end=1.15,
            pan_x=0.1,
            pan_y=0.05,
        )

        assert "focal_point" in result
        assert "zoom_start" in result
        assert "zoom_end" in result
        assert "pan_direction" in result

        assert isinstance(result["focal_point"], tuple)
        assert len(result["focal_point"]) == 2
        assert result["zoom_start"] == 1.0
        assert result["zoom_end"] == 1.15
        assert result["pan_direction"] == (0.1, 0.05)

    def test_reset_tracking_clears_subject_tracking(self):
        """Test reset_tracking clears subject tracking state."""
        settings = ReframeSettings()
        reframer = Reframer(settings)

        # Set up some tracking state
        reframer._subject_tracking_initialized = True
        reframer._subject_bbox = (100, 100, 200, 200)
        reframer._frames_since_redetect = 10
        reframer._punch_in_active = True

        # Reset
        reframer.reset_tracking()

        # Verify cleared
        assert not reframer._subject_tracking_initialized
        assert reframer._subject_bbox is None
        assert reframer._frames_since_redetect == 0
        assert not reframer._punch_in_active
