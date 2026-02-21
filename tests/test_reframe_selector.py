"""Tests for reframe_selector module."""

from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from drone_reel.core.reframe_selector import ReframeSelector, KenBurnsConfig
from drone_reel.core.reframer import ReframeMode, AspectRatio, ReframeSettings
from drone_reel.core.scene_detector import (
    EnhancedSceneInfo,
    HookPotential,
    MotionType,
    SceneInfo,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _scene(start=0.0, end=5.0, score=80.0):
    """Create a basic SceneInfo."""
    return SceneInfo(
        start_time=start,
        end_time=end,
        duration=end - start,
        score=score,
        source_file=Path("clip.mp4"),
    )


def _enhanced_scene(
    start=0.0,
    end=5.0,
    score=80.0,
    motion_type=MotionType.STATIC,
    hook_tier=HookPotential.MEDIUM,
    subject_score=0.0,
):
    """Create an EnhancedSceneInfo."""
    return EnhancedSceneInfo(
        start_time=start,
        end_time=end,
        duration=end - start,
        score=score,
        source_file=Path("clip.mp4"),
        motion_type=motion_type,
        hook_tier=hook_tier,
        subject_score=subject_score,
    )


# ===========================================================================
# KenBurnsConfig tests
# ===========================================================================


class TestKenBurnsConfig:
    """Tests for KenBurnsConfig dataclass."""

    def test_defaults(self):
        cfg = KenBurnsConfig()
        assert cfg.zoom_end == 1.05
        assert cfg.pan_x == 0.05
        assert cfg.pan_y == 0.02

    def test_custom_values(self):
        cfg = KenBurnsConfig(zoom_end=1.1, pan_x=0.1, pan_y=0.05)
        assert cfg.zoom_end == 1.1
        assert cfg.pan_x == 0.1
        assert cfg.pan_y == 0.05


# ===========================================================================
# ReframeSelector initialization tests
# ===========================================================================


class TestReframeSelectorInit:
    """Tests for ReframeSelector initialization."""

    def test_default_values(self):
        selector = ReframeSelector()
        assert selector.output_width == 1080
        assert selector.kb_config is None
        assert selector.subject_threshold == 40.0

    def test_custom_output_width(self):
        selector = ReframeSelector(output_width=720)
        assert selector.output_width == 720

    def test_with_ken_burns_config(self):
        kb = KenBurnsConfig()
        selector = ReframeSelector(kb_config=kb)
        assert selector.kb_config is kb

    def test_custom_subject_threshold(self):
        selector = ReframeSelector(subject_threshold=60.0)
        assert selector.subject_threshold == 60.0


# ===========================================================================
# ReframeSelector.select_reframers tests
# ===========================================================================


class TestSelectReframersSmartMode:
    """Tests for SMART mode selection."""

    @patch("drone_reel.core.reframe_selector.Reframer")
    def test_high_subject_no_movement_gets_smart(self, mock_reframer_cls):
        """High subject score + no camera movement -> SMART mode."""
        mock_reframer_cls.return_value = MagicMock()
        selector = ReframeSelector()
        scene = _enhanced_scene(
            subject_score=50.0,  # Above threshold of 40
            motion_type=MotionType.STATIC,
        )

        reframers, mode_names = selector.select_reframers([scene], [3.0])

        assert len(reframers) == 1
        assert mode_names[0] == "SMART"
        # Verify SMART settings were passed
        call_args = mock_reframer_cls.call_args
        settings = call_args[0][0]
        assert settings.mode == ReframeMode.SMART
        assert settings.smooth_tracking is True
        assert settings.target_ratio == AspectRatio.VERTICAL_9_16

    @patch("drone_reel.core.reframe_selector.Reframer")
    def test_high_subject_with_unknown_motion_gets_smart(self, mock_reframer_cls):
        """High subject + UNKNOWN motion (not in MOVING list) -> SMART."""
        mock_reframer_cls.return_value = MagicMock()
        selector = ReframeSelector()
        scene = _enhanced_scene(
            subject_score=50.0,
            motion_type=MotionType.UNKNOWN,
        )

        _, mode_names = selector.select_reframers([scene], [3.0])

        assert mode_names[0] == "SMART"

    @patch("drone_reel.core.reframe_selector.Reframer")
    def test_smart_tracking_smoothness_scales_with_duration(self, mock_reframer_cls):
        """SMART mode tracking smoothness scales with clip duration."""
        mock_reframer_cls.return_value = MagicMock()
        selector = ReframeSelector()
        scene = _enhanced_scene(subject_score=50.0, motion_type=MotionType.STATIC)

        selector.select_reframers([scene], [6.0])

        settings = mock_reframer_cls.call_args[0][0]
        # duration_scale = min(6.0 / 3.0, 1.5) = 1.5
        expected_smoothness = 0.003 * 1.5
        assert settings.tracking_smoothness == pytest.approx(expected_smoothness, abs=0.0001)


class TestSelectReframersCenterMode:
    """Tests for CENTER mode selection."""

    @patch("drone_reel.core.reframe_selector.Reframer")
    def test_camera_moving_gets_center(self, mock_reframer_cls):
        """Camera movement detected -> CENTER mode."""
        mock_reframer_cls.return_value = MagicMock()
        selector = ReframeSelector()

        for motion_type in ReframeSelector.MOVING_MOTION_TYPES:
            scene = _enhanced_scene(
                subject_score=50.0,  # High subject, but camera is moving
                motion_type=motion_type,
            )

            _, mode_names = selector.select_reframers([scene], [3.0])

            assert mode_names[0] == "CENTER", f"Expected CENTER for {motion_type}"

    @patch("drone_reel.core.reframe_selector.Reframer")
    def test_low_subject_no_kb_gets_center(self, mock_reframer_cls):
        """Low subject score + no KB config -> CENTER mode."""
        mock_reframer_cls.return_value = MagicMock()
        selector = ReframeSelector()  # No kb_config
        scene = _enhanced_scene(
            subject_score=10.0,  # Below threshold
            motion_type=MotionType.STATIC,
        )

        _, mode_names = selector.select_reframers([scene], [3.0])

        assert mode_names[0] == "CENTER"

    @patch("drone_reel.core.reframe_selector.Reframer")
    def test_center_settings_correct(self, mock_reframer_cls):
        """CENTER mode uses correct settings."""
        mock_reframer_cls.return_value = MagicMock()
        selector = ReframeSelector(output_width=720)
        scene = _enhanced_scene(
            subject_score=10.0,
            motion_type=MotionType.STATIC,
        )

        selector.select_reframers([scene], [3.0])

        settings = mock_reframer_cls.call_args[0][0]
        assert settings.mode == ReframeMode.CENTER
        assert settings.output_width == 720
        assert settings.target_ratio == AspectRatio.VERTICAL_9_16


class TestSelectReframersKenBurnsMode:
    """Tests for KEN_BURNS mode selection."""

    @patch("drone_reel.core.reframe_selector.Reframer")
    def test_landscape_with_kb_config_gets_ken_burns(self, mock_reframer_cls):
        """Low subject + static + KenBurnsConfig present -> KEN_BURNS mode."""
        mock_reframer_cls.return_value = MagicMock()
        kb = KenBurnsConfig(zoom_end=1.1, pan_x=0.08, pan_y=0.04)
        selector = ReframeSelector(kb_config=kb)
        scene = _enhanced_scene(
            subject_score=10.0,  # Low subject
            motion_type=MotionType.STATIC,
        )

        _, mode_names = selector.select_reframers([scene], [3.0])

        assert mode_names[0] == "KEN_BURNS"

    @patch("drone_reel.core.reframe_selector.Reframer")
    def test_ken_burns_settings_correct(self, mock_reframer_cls):
        """KEN_BURNS mode passes correct KB config values."""
        mock_reframer_cls.return_value = MagicMock()
        kb = KenBurnsConfig(zoom_end=1.08, pan_x=0.06, pan_y=0.03)
        selector = ReframeSelector(kb_config=kb)
        scene = _enhanced_scene(
            subject_score=10.0,
            motion_type=MotionType.STATIC,
        )

        selector.select_reframers([scene], [3.0])

        settings = mock_reframer_cls.call_args[0][0]
        assert settings.mode == ReframeMode.KEN_BURNS
        assert settings.ken_burns_zoom_start == 1.0
        assert settings.ken_burns_zoom_end == 1.08
        assert settings.ken_burns_pan_direction == (0.06, 0.03)
        assert settings.ken_burns_ease_curve == "ease_in_out"

    @patch("drone_reel.core.reframe_selector.Reframer")
    def test_landscape_no_kb_config_gets_center(self, mock_reframer_cls):
        """Low subject + static + no KenBurnsConfig -> CENTER mode."""
        mock_reframer_cls.return_value = MagicMock()
        selector = ReframeSelector()  # No kb_config
        scene = _enhanced_scene(
            subject_score=10.0,
            motion_type=MotionType.STATIC,
        )

        _, mode_names = selector.select_reframers([scene], [3.0])

        assert mode_names[0] == "CENTER"


class TestSelectReframersModePriority:
    """Tests for mode selection priority."""

    @patch("drone_reel.core.reframe_selector.Reframer")
    def test_moving_camera_overrides_high_subject(self, mock_reframer_cls):
        """Camera movement takes priority over high subject score."""
        mock_reframer_cls.return_value = MagicMock()
        selector = ReframeSelector()
        scene = _enhanced_scene(
            subject_score=90.0,  # Very high subject
            motion_type=MotionType.PAN_LEFT,  # But camera is moving
        )

        _, mode_names = selector.select_reframers([scene], [3.0])

        assert mode_names[0] == "CENTER"

    @patch("drone_reel.core.reframe_selector.Reframer")
    def test_moving_camera_overrides_kb_config(self, mock_reframer_cls):
        """Camera movement takes priority over Ken Burns config."""
        mock_reframer_cls.return_value = MagicMock()
        kb = KenBurnsConfig()
        selector = ReframeSelector(kb_config=kb)
        scene = _enhanced_scene(
            subject_score=10.0,
            motion_type=MotionType.FLYOVER,
        )

        _, mode_names = selector.select_reframers([scene], [3.0])

        assert mode_names[0] == "CENTER"

    @patch("drone_reel.core.reframe_selector.Reframer")
    def test_high_subject_overrides_kb_config(self, mock_reframer_cls):
        """High subject with static camera -> SMART, even with KB config."""
        mock_reframer_cls.return_value = MagicMock()
        kb = KenBurnsConfig()
        selector = ReframeSelector(kb_config=kb)
        scene = _enhanced_scene(
            subject_score=50.0,
            motion_type=MotionType.STATIC,
        )

        _, mode_names = selector.select_reframers([scene], [3.0])

        assert mode_names[0] == "SMART"


class TestSelectReframersMultipleScenes:
    """Tests for multiple scene selection."""

    @patch("drone_reel.core.reframe_selector.Reframer")
    def test_returns_correct_count(self, mock_reframer_cls):
        """Returns correct number of reframers matching scenes count."""
        mock_reframer_cls.return_value = MagicMock()
        selector = ReframeSelector()
        scenes = [
            _enhanced_scene(subject_score=50.0, motion_type=MotionType.STATIC),
            _enhanced_scene(subject_score=10.0, motion_type=MotionType.PAN_LEFT),
            _enhanced_scene(subject_score=10.0, motion_type=MotionType.STATIC),
        ]
        durations = [3.0, 3.0, 3.0]

        reframers, mode_names = selector.select_reframers(scenes, durations)

        assert len(reframers) == 3
        assert len(mode_names) == 3

    @patch("drone_reel.core.reframe_selector.Reframer")
    def test_mixed_modes(self, mock_reframer_cls):
        """Different scenes get different modes based on characteristics."""
        mock_reframer_cls.return_value = MagicMock()
        kb = KenBurnsConfig()
        selector = ReframeSelector(kb_config=kb)
        scenes = [
            _enhanced_scene(subject_score=50.0, motion_type=MotionType.STATIC),  # SMART
            _enhanced_scene(subject_score=10.0, motion_type=MotionType.PAN_LEFT),  # CENTER
            _enhanced_scene(subject_score=10.0, motion_type=MotionType.STATIC),  # KEN_BURNS
        ]
        durations = [3.0, 3.0, 3.0]

        _, mode_names = selector.select_reframers(scenes, durations)

        assert mode_names[0] == "SMART"
        assert mode_names[1] == "CENTER"
        assert mode_names[2] == "KEN_BURNS"

    @patch("drone_reel.core.reframe_selector.Reframer")
    def test_missing_duration_defaults_to_3(self, mock_reframer_cls):
        """When clip_durations is shorter than scenes, default to 3.0."""
        mock_reframer_cls.return_value = MagicMock()
        selector = ReframeSelector()
        scenes = [
            _enhanced_scene(subject_score=50.0, motion_type=MotionType.STATIC),
            _enhanced_scene(subject_score=50.0, motion_type=MotionType.STATIC),
        ]
        durations = [4.0]  # Only one duration for two scenes

        reframers, mode_names = selector.select_reframers(scenes, durations)

        assert len(reframers) == 2
        assert len(mode_names) == 2


class TestSelectReframersEdgeCases:
    """Edge case tests for select_reframers."""

    @patch("drone_reel.core.reframe_selector.Reframer")
    def test_empty_scenes_list(self, mock_reframer_cls):
        """Empty scenes list returns empty results."""
        selector = ReframeSelector()

        reframers, mode_names = selector.select_reframers([], [])

        assert reframers == []
        assert mode_names == []

    @patch("drone_reel.core.reframe_selector.Reframer")
    def test_single_scene(self, mock_reframer_cls):
        """Single scene returns single reframer."""
        mock_reframer_cls.return_value = MagicMock()
        selector = ReframeSelector()
        scene = _enhanced_scene(subject_score=50.0, motion_type=MotionType.STATIC)

        reframers, mode_names = selector.select_reframers([scene], [3.0])

        assert len(reframers) == 1
        assert len(mode_names) == 1

    @patch("drone_reel.core.reframe_selector.Reframer")
    def test_basic_scene_info_gets_center(self, mock_reframer_cls):
        """Basic SceneInfo (not Enhanced) defaults to CENTER."""
        mock_reframer_cls.return_value = MagicMock()
        selector = ReframeSelector()
        scene = _scene()  # Not EnhancedSceneInfo

        _, mode_names = selector.select_reframers([scene], [3.0])

        # subject_score=0 and motion_type=STATIC -> falls through to CENTER (no kb_config)
        assert mode_names[0] == "CENTER"

    @patch("drone_reel.core.reframe_selector.Reframer")
    def test_basic_scene_with_kb_gets_ken_burns(self, mock_reframer_cls):
        """Basic SceneInfo with KB config falls through to KEN_BURNS."""
        mock_reframer_cls.return_value = MagicMock()
        kb = KenBurnsConfig()
        selector = ReframeSelector(kb_config=kb)
        scene = _scene()  # Not EnhancedSceneInfo

        _, mode_names = selector.select_reframers([scene], [3.0])

        # subject_score=0 (default) and motion_type=STATIC (default) -> KEN_BURNS
        assert mode_names[0] == "KEN_BURNS"

    @patch("drone_reel.core.reframe_selector.Reframer")
    def test_subject_at_exact_threshold(self, mock_reframer_cls):
        """Subject score exactly at threshold gets SMART mode."""
        mock_reframer_cls.return_value = MagicMock()
        selector = ReframeSelector(subject_threshold=40.0)
        scene = _enhanced_scene(subject_score=40.0, motion_type=MotionType.STATIC)

        _, mode_names = selector.select_reframers([scene], [3.0])

        assert mode_names[0] == "SMART"

    @patch("drone_reel.core.reframe_selector.Reframer")
    def test_subject_just_below_threshold(self, mock_reframer_cls):
        """Subject score just below threshold does NOT get SMART mode."""
        mock_reframer_cls.return_value = MagicMock()
        selector = ReframeSelector(subject_threshold=40.0)
        scene = _enhanced_scene(subject_score=39.9, motion_type=MotionType.STATIC)

        _, mode_names = selector.select_reframers([scene], [3.0])

        assert mode_names[0] != "SMART"

    @patch("drone_reel.core.reframe_selector.Reframer")
    def test_output_width_propagated(self, mock_reframer_cls):
        """Output width is propagated to all reframer settings."""
        mock_reframer_cls.return_value = MagicMock()
        selector = ReframeSelector(output_width=2160)
        scenes = [
            _enhanced_scene(subject_score=50.0, motion_type=MotionType.STATIC),  # SMART
            _enhanced_scene(subject_score=10.0, motion_type=MotionType.PAN_LEFT),  # CENTER
        ]

        selector.select_reframers(scenes, [3.0, 3.0])

        for call in mock_reframer_cls.call_args_list:
            settings = call[0][0]
            assert settings.output_width == 2160


class TestMovingMotionTypes:
    """Tests for the MOVING_MOTION_TYPES classification."""

    def test_all_moving_types_listed(self):
        """All expected motion types are in the MOVING list."""
        expected = {
            MotionType.PAN_LEFT, MotionType.PAN_RIGHT,
            MotionType.TILT_UP, MotionType.TILT_DOWN,
            MotionType.ORBIT_CW, MotionType.ORBIT_CCW,
            MotionType.FLYOVER, MotionType.REVEAL, MotionType.FPV,
        }
        assert set(ReframeSelector.MOVING_MOTION_TYPES) == expected

    def test_static_not_in_moving(self):
        """STATIC is not in MOVING_MOTION_TYPES."""
        assert MotionType.STATIC not in ReframeSelector.MOVING_MOTION_TYPES

    def test_unknown_not_in_moving(self):
        """UNKNOWN is not in MOVING_MOTION_TYPES."""
        assert MotionType.UNKNOWN not in ReframeSelector.MOVING_MOTION_TYPES

    def test_approach_not_in_moving(self):
        """APPROACH is not in MOVING_MOTION_TYPES."""
        assert MotionType.APPROACH not in ReframeSelector.MOVING_MOTION_TYPES
