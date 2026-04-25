"""
Chapter 02 — Drone Footage Formats

Covers: D-Log / HLG / Rec.709, HDR→SDR proxies, frame rate vs analysis time.
"""

from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="02 Drone Footage", page_icon="", layout="wide")

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import (
    DEFAULT_CLIPS, MULTI_SCENE_CLIP, clip_selector, page_footer,
    probe_video, video_info,
)

with st.sidebar:
    st.title("drone-reel Textbook")
    st.page_link("app.py", label="Home")
    st.page_link("pages/01_welcome.py", label="Prev: Welcome")
    st.page_link("pages/03_scene_detection.py", label="Next: Scene Detection")

# ---------------------------------------------------------------------------

st.title("Chapter 02 — Drone Footage Formats")

st.info(
    "**What you'll learn:** Why colorspace matters for grading, what D-Log and HLG mean, "
    "when to create a proxy before analysis, and how frame rate affects processing time."
)

# ---------------------------------------------------------------------------
st.subheader("Colorspace 101")

col1, col2 = st.columns(2)
with col1:
    st.markdown(
        """
        ### Rec.709 (SDR)
        The broadcast standard. Most DJI consumer drones default to this.
        What you see is what you get — no grading headroom, but immediately playable.

        **When drone-reel uses it:** All outputs are BT.709.  If your footage is already
        Rec.709, use `--input-colorspace rec709` (or `auto`).
        """
    )
with col2:
    st.markdown(
        """
        ### D-Log / D-Log M / HLG / S-Log3
        Flat/log profiles that trade a "washed out" look for +3–5 stops of dynamic range.
        Must be graded before distribution.

        **drone-reel flag:** `--input-colorspace dlog` (DJI D-Log), `dlog_m` (DJI D-Log M),
        `slog3` (Sony), or `hlg` (Hybrid Log-Gamma).  The grader tone-maps to Rec.709.
        """
    )

st.divider()

# ---------------------------------------------------------------------------
st.subheader("Colorspace comparison table")

colorspace_data = {
    "Colorspace": ["Rec.709", "D-Log", "D-Log M", "HLG", "S-Log3"],
    "Dynamic Range (stops)": ["~8", "~12.8", "~12.8", "~13", "~15.4"],
    "Looks flat?": ["No", "Yes", "Yes (less)", "No (HDR)", "Yes"],
    "drone-reel flag": ["rec709", "dlog", "dlog_m", "auto", "slog3"],
    "Common cameras": [
        "DJI Mini/Air (normal)", "DJI Mavic 3", "DJI Air 3", "DJI O3+", "DJI Inspire/Sony"
    ],
}
st.dataframe(pd.DataFrame(colorspace_data), use_container_width=True)

st.warning(
    "If you grade D-Log footage with `--color drone_aerial` but forget "
    "`--input-colorspace dlog`, the tone-mapping is skipped and your output will look "
    "flat and washed out."
)

# ---------------------------------------------------------------------------
st.subheader("HDR → SDR proxies for 4K HEVC")

st.markdown(
    """
    DJI 4K 60fps HEVC is the most common 'slow analysis' offender.  At native resolution,
    scene analysis can take **40+ minutes** per clip.  A 720p H.264 proxy takes the same
    analysis down to **~11 minutes** with nearly identical cut points.
    """
)

st.code(
    """# Create a 720p proxy — run once per source file
ffmpeg -i DJI_SOURCE.MP4 \\
       -vf scale=1280:720 -r 30 \\
       -c:v libx264 -preset ultrafast -crf 26 -an \\
       proxy_720p.mp4

# Then analyze the proxy (fast)
drone-reel split -i proxy_720p.mp4 -o ./out/ --color drone_aerial --auto-speed""",
    language="bash",
)

# ---------------------------------------------------------------------------
st.subheader("Frame rate vs analysis time")

st.markdown("Use the slider to see how frame rate affects `frame_skip` auto-tuning:")

fps_val = st.slider("Source frame rate (fps)", min_value=24, max_value=120, value=30, step=6)

if fps_val > 35:
    skip = 1
    note = "High-fps source detected — frame_skip auto-set to 1 (analyze every other frame)."
else:
    skip = 0
    note = "Standard fps — all frames analyzed (frame_skip=0)."

st.info(f"fps={fps_val} → frame_skip={skip}. {note}")

analysis_time_est = {
    24: "~3 min/10min clip",
    30: "~4 min/10min clip",
    60: "~9 min/10min clip (use proxy!)",
    120: "~20+ min/10min clip (always use proxy)",
}
fps_display = min(fps_val, 120)
for k in [24, 30, 60, 120]:
    if fps_val <= k:
        fps_display = k
        break
st.metric("Estimated analysis time", analysis_time_est.get(fps_display, "~4 min/10min clip"))

# ---------------------------------------------------------------------------
st.subheader("Probe a bundled clip")

chosen = clip_selector("Select clip to probe")
info = video_info(chosen)
if info.get("width"):
    metric_cols = st.columns(5)
    metric_cols[0].metric("Resolution", f"{info['width']}x{info['height']}")
    metric_cols[1].metric("FPS", info.get("fps", "?"))
    metric_cols[2].metric("Codec", info.get("codec", "?").upper())
    metric_cols[3].metric("Duration", f"{info.get('duration', 0):.1f}s")
    metric_cols[4].metric("Size", f"{info.get('size_mb', 0):.1f} MB")
    st.caption(
        f"Color space: {info.get('color_space', 'unknown')} | "
        f"Transfer: {info.get('color_transfer', 'unknown')}"
    )
else:
    st.warning("Could not probe clip — check ffprobe is installed.")

page_footer("03_scene_detection.py", "Scene Detection")
