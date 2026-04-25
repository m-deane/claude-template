"""
Chapter 07 — Speed Correction

Covers: auto_pan_speed_ramp, profile table, --ease-speed-ramps;
speed-vs-time plot for each profile on a synthetic PAN clip.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="07 Speed Correction", page_icon="", layout="wide")

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import (
    DEMO_OUTPUT_DIR,
    clip_selector,
    run_drone_reel,
    show_command_expander,
    page_footer,
)

with st.sidebar:
    st.title("drone-reel Textbook")
    st.page_link("app.py", label="Home")
    st.page_link("pages/06_stabilization.py", label="Prev: Stabilization")
    st.page_link("pages/08_color_grading.py", label="Next: Color Grading")

# ---------------------------------------------------------------------------

st.title("Chapter 07 — Speed Correction")

st.info(
    "**What you'll learn:** Why fast drone pans look bad in social reels, "
    "how `auto_pan_speed_ramp` classifies and corrects motion, the four speed "
    "profiles, and how to visualize speed-vs-time curves."
)

# ---------------------------------------------------------------------------
st.subheader("The problem: pan speed mismatch")

st.markdown(
    """
    Drone gimbals can pan at speeds that feel natural in a 10-minute documentary
    but are jarring in a 30-second reel watched on a phone screen.

    **Rule of thumb:** A comfortable pan speed is roughly **60° in 3–4 seconds**.
    DJI drones at full stick deflection can hit **120° in 1.5s** — 4× too fast.

    `auto_pan_speed_ramp` solves this by detecting motion type and energy via
    optical flow, then applying a **constant-speed multiplier** to the entire clip.
    """
)

# ---------------------------------------------------------------------------
st.subheader("Motion type classification matrix")

matrix_data = {
    "Motion Type": [
        "PAN_LEFT / PAN_RIGHT (energy > 70)",
        "PAN_LEFT / PAN_RIGHT (energy 55–70)",
        "PAN_LEFT / PAN_RIGHT (energy 5–20)",
        "TILT_UP / TILT_DOWN (energy > 65)",
        "FLYOVER (energy > 70)",
        "APPROACH (energy > 70)",
        "FPV (energy > 50)",
        "ORBIT_CW / ORBIT_CCW",
        "STATIC / REVEAL / UNKNOWN",
    ],
    "normal": [
        "0.65×", "0.80×", "1.25× (speed up!)", "0.70×", "0.70×", "0.70×", "0.75×",
        "0.85× (if --correct-orbit)", "no change",
    ],
    "aggressive": [
        "0.55×", "0.70×", "1.25×", "0.60×", "0.60×", "0.60×", "0.65×",
        "0.85×", "no change",
    ],
    "smooth": [
        "0.75×", "0.85×", "1.25×", "0.80×", "0.80×", "0.80×", "0.80×",
        "0.85×", "no change",
    ],
    "cinematic": [
        "0.60×", "0.75×", "1.25×", "0.65×", "0.65×", "0.65×", "0.70×",
        "0.85×", "no change",
    ],
}
st.dataframe(pd.DataFrame(matrix_data), use_container_width=True)

# ---------------------------------------------------------------------------
st.subheader("Speed-vs-time curves")

st.markdown(
    "Compare how each profile transforms a **10-second PAN clip** with energy=75 "
    "(high-energy pan — would normally be corrected to slow down). "
    "Toggle `--ease-speed-ramps` to see the ramped version."
)

ease = st.checkbox("--ease-speed-ramps (smooth in/out around correction)", value=False)
motion_energy = st.slider("Motion energy (0–100)", 0, 100, 75)

profiles = {
    "normal":     {"pan_high": 0.65, "pan_mid": 0.80},
    "aggressive": {"pan_high": 0.55, "pan_mid": 0.70},
    "smooth":     {"pan_high": 0.75, "pan_mid": 0.85},
    "cinematic":  {"pan_high": 0.60, "pan_mid": 0.75},
}

duration = 10.0
t = np.linspace(0, duration, 300)

fig = go.Figure()
colors = ["#2196F3", "#F44336", "#4CAF50", "#FF9800"]

for (profile_name, profile), color in zip(profiles.items(), colors):
    # Determine target speed
    if motion_energy > 70:
        target_speed = profile["pan_high"]
    elif motion_energy > 55:
        target_speed = profile["pan_mid"]
    elif 5 < motion_energy < 20:
        target_speed = 1.25
    else:
        target_speed = 1.0

    if ease and target_speed != 1.0:
        ease_frac = 0.15
        speeds = np.where(
            t < duration * ease_frac,
            1.0 + (target_speed - 1.0) * (t / (duration * ease_frac)),
            np.where(
                t > duration * (1 - ease_frac),
                target_speed + (1.0 - target_speed) * ((t - duration * (1 - ease_frac)) / (duration * ease_frac)),
                target_speed,
            ),
        )
    else:
        speeds = np.full_like(t, target_speed)

    fig.add_trace(
        go.Scatter(
            x=t,
            y=speeds,
            mode="lines",
            name=f"{profile_name} ({target_speed:.2f}×)",
            line=dict(color=color, width=2),
        )
    )

fig.add_hline(y=1.0, line_dash="dot", line_color="gray", annotation_text="1.0× (no change)")
fig.update_layout(
    title=f"Speed multiplier over time — PAN, energy={motion_energy}, ease={ease}",
    xaxis_title="Time (seconds)",
    yaxis_title="Speed multiplier",
    yaxis=dict(range=[0.4, 1.4]),
    legend_title="Profile",
    height=400,
)
st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------
st.subheader("Using auto-speed in practice")

st.code(
    """# Basic auto-speed (normal profile)
drone-reel split -i footage.mp4 -o ./out/ --auto-speed

# Cinematic profile with ease-in/out
drone-reel split -i footage.mp4 -o ./out/ \\
  --auto-speed \\
  --speed-correction-profile cinematic \\
  --ease-speed-ramps

# Fine-tune individual motion types
drone-reel split -i footage.mp4 -o ./out/ \\
  --auto-speed \\
  --pan-speed-high 0.58 \\
  --tilt-speed 0.72 \\
  --fpv-speed 0.70 \\
  --gimbal-bounce-recovery
""",
    language="bash",
)

# ---------------------------------------------------------------------------
st.subheader("Live speed-correction demo")

chosen_path = clip_selector("Select clip to apply speed correction")
profile_choice = st.selectbox(
    "--speed-correction-profile",
    ["normal", "aggressive", "smooth", "cinematic"],
)
ease_flag = st.checkbox("--ease-speed-ramps", value=False, key="live_ease")

if st.button("Apply speed correction"):
    out_dir = DEMO_OUTPUT_DIR / "speed"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"speed_{profile_choice}_ease{ease_flag}_{chosen_path.stem}.mp4"

    if not out_path.exists():
        args = [
            "split",
            "-i", str(chosen_path),
            "-o", str(out_dir),
            "--auto-speed",
            "--speed-correction-profile", profile_choice,
            "--no-filter",
            "--count", "1",
            "--overwrite",
        ]
        if ease_flag:
            args.append("--ease-speed-ramps")

        with st.spinner("Applying speed correction…"):
            result = run_drone_reel(args, timeout=180, show_error=True)
        show_command_expander(result)

        # Move latest output to named path
        written = sorted(out_dir.glob("*.mp4"), key=lambda p: p.stat().st_mtime)
        if written and written[-1] != out_path:
            import shutil
            shutil.copy(written[-1], out_path)
    else:
        st.info("Using cached output.")

    if out_path.exists():
        col1, col2 = st.columns(2)
        with col1:
            st.video(str(chosen_path))
            st.caption("Original speed")
        with col2:
            st.video(str(out_path))
            st.caption(f"Speed-corrected: {profile_choice}{', eased' if ease_flag else ''}")

page_footer("08_color_grading.py", "Color Grading")
