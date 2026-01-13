"""Transition presets for different video styles."""

import random
from typing import Optional

from drone_reel.core.video_processor import TransitionType

# Transition presets by style
TRANSITION_PRESETS = {
    "smooth": [
        TransitionType.CROSSFADE,
        TransitionType.FADE_BLACK,
    ],
    "energetic": [
        TransitionType.CUT,
        TransitionType.ZOOM_IN,
        TransitionType.ZOOM_OUT,
    ],
    "cinematic": [
        TransitionType.CROSSFADE,
        TransitionType.FADE_BLACK,
        TransitionType.ZOOM_OUT,
    ],
    "dynamic": [
        TransitionType.CUT,
        TransitionType.CROSSFADE,
        TransitionType.ZOOM_IN,
        TransitionType.FADE_WHITE,
    ],
    "minimal": [
        TransitionType.CUT,
    ],
    "dramatic": [
        TransitionType.FADE_BLACK,
        TransitionType.FADE_WHITE,
        TransitionType.ZOOM_IN,
    ],
}


def get_transitions_for_energy(
    energy_level: float,
    count: int,
    style: str = "dynamic",
) -> list[TransitionType]:
    """
    Get transitions appropriate for the energy level.

    Args:
        energy_level: Energy level 0-1 (from beat analysis)
        count: Number of transitions needed
        style: Base style preset to use

    Returns:
        List of TransitionType for each cut point
    """
    base_transitions = TRANSITION_PRESETS.get(style, TRANSITION_PRESETS["dynamic"])

    transitions = []
    for i in range(count):
        segment_energy = energy_level

        if segment_energy > 0.7:
            choices = [TransitionType.CUT, TransitionType.ZOOM_IN]
        elif segment_energy > 0.4:
            choices = [TransitionType.CROSSFADE, TransitionType.CUT]
        else:
            choices = [TransitionType.CROSSFADE, TransitionType.FADE_BLACK]

        valid_choices = [t for t in choices if t in base_transitions] or choices
        transitions.append(random.choice(valid_choices))

    return transitions


def get_random_transitions(
    count: int,
    style: str = "dynamic",
    seed: Optional[int] = None,
) -> list[TransitionType]:
    """
    Get random transitions from a style preset.

    Args:
        count: Number of transitions needed
        style: Style preset to use
        seed: Optional random seed for reproducibility

    Returns:
        List of TransitionType
    """
    if seed is not None:
        random.seed(seed)

    available = TRANSITION_PRESETS.get(style, TRANSITION_PRESETS["dynamic"])
    return [random.choice(available) for _ in range(count)]


def get_transition_duration(
    transition: TransitionType,
    base_duration: float = 0.3,
    energy_level: float = 0.5,
) -> float:
    """
    Get recommended duration for a transition type.

    Args:
        transition: The transition type
        base_duration: Base duration in seconds
        energy_level: Energy level 0-1 (higher = shorter transitions)

    Returns:
        Recommended duration in seconds
    """
    duration_multipliers = {
        TransitionType.CUT: 0.0,
        TransitionType.CROSSFADE: 1.0,
        TransitionType.FADE_BLACK: 1.2,
        TransitionType.FADE_WHITE: 1.2,
        TransitionType.ZOOM_IN: 0.8,
        TransitionType.ZOOM_OUT: 0.8,
        TransitionType.SLIDE_LEFT: 0.6,
        TransitionType.SLIDE_RIGHT: 0.6,
        TransitionType.WIPE_LEFT: 0.5,
        TransitionType.WIPE_RIGHT: 0.5,
    }

    multiplier = duration_multipliers.get(transition, 1.0)
    energy_factor = 1.0 - (energy_level * 0.4)

    return base_duration * multiplier * energy_factor
