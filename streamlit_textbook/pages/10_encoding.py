"""
Chapter 10 — Encoding & Output

Covers: BT.709 SDR, +faststart, h264_metadata bsf, VBV bitrate caps.
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="10 Encoding", page_icon="", layout="wide")

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import (
    DEFAULT_CLIPS,
    clip_selector,
    probe_video,
    video_info,
    page_footer,
)

with st.sidebar:
    st.title("drone-reel Textbook")
    st.page_link("app.py", label="Home")
    st.page_link("pages/09_beat_sync.py", label="Prev: Beat Sync")
    st.page_link("pages/11_recipes.py", label="Next: Recipes")

# ---------------------------------------------------------------------------

st.title("Chapter 10 — Encoding & Output")

st.info(
    "**What you'll learn:** Why all outputs use BT.709 SDR, what `+faststart` does "
    "for streaming, how VBV rate-control prevents buffering, and the "
    "`--quality` / `--resolution` / `--platform` flags."
)

# ---------------------------------------------------------------------------
st.subheader("BT.709 SDR — the universal output standard")

st.markdown(
    """
    All drone-reel outputs are forced to **Rec.709 BT.709 SDR** regardless of the
    input colorspace.  This is intentional:

    - **Compatibility:** Every device and platform (Instagram, TikTok, YouTube) expects BT.709.
      HDR content on SDR players looks washed out or clipped.
    - **Metadata triplet:** drone-reel always writes `-colorspace bt709 -color_primaries bt709
      -color_trc bt709` so platforms don't have to guess.
    - **yuv420p pixel format:** Required for H.264 compatibility on iOS/Android hardware decoders.
    """
)

st.code(
    """# What drone-reel applies internally to every output:
ffmpeg -i input.mp4 \\
  -c:v libx264 \\
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 \\
  -pix_fmt yuv420p \\
  -movflags +faststart \\
  -maxrate 22500k -bufsize 45000k \\
  -c:a aac -b:a 192k \\
  output.mp4
""",
    language="bash",
)

# ---------------------------------------------------------------------------
st.subheader("`+faststart` — what it means for streaming")

st.markdown(
    """
    MP4 files have a **moov atom** (index) that tells the player where every frame lives.
    By default, ffmpeg writes the moov atom **at the end** — the player must download the
    entire file before it can start playing.

    `-movflags +faststart` **relocates the moov atom to the front** of the file.
    Effect:
    - Instagram/TikTok/YouTube can start playing **before the upload finishes**.
    - Progressive web players begin playing at the first byte.
    - No functional change for local playback (players seek freely).
    """
)

# ---------------------------------------------------------------------------
st.subheader("VBV rate control")

st.markdown(
    """
    **VBV (Video Buffer Verifier)** prevents the encoder from writing a single huge
    frame that would stall a streaming decoder.  drone-reel sets:

    | Parameter | Formula | Purpose |
    |-----------|---------|---------|
    | `-b:v` target | quality-dependent | Average bitrate goal |
    | `-maxrate` | 1.5× target | Peak bitrate cap |
    | `-bufsize` | 2× target | VBV buffer window |

    Without VBV, a single frame on a scene cut (high I-frame) can spike to 10×
    the average bitrate and cause re-buffering on mobile networks.
    """
)

# ---------------------------------------------------------------------------
st.subheader("Quality presets")

quality_df = pd.DataFrame(
    {
        "Preset (--quality)": ["low", "medium", "high", "ultra"],
        "Target bitrate": ["5 Mbps", "10 Mbps", "15 Mbps", "25 Mbps"],
        "Max bitrate": ["7.5 Mbps", "15 Mbps", "22.5 Mbps", "37.5 Mbps"],
        "Bufsize": ["10 Mbps", "20 Mbps", "30 Mbps", "50 Mbps"],
        "Best for": [
            "Preview / draft renders",
            "Instagram / TikTok upload",
            "YouTube / portfolio",
            "Master file / future re-encode",
        ],
    }
)
st.dataframe(quality_df, use_container_width=True)

# Visual bitrate comparison
fig = px.bar(
    quality_df,
    x="Preset (--quality)",
    y=["Target bitrate", "Max bitrate"],
    barmode="group",
    title="Bitrate by quality preset",
    labels={"value": "Bitrate (Mbps)", "variable": ""},
    color_discrete_sequence=["#1976D2", "#F57C00"],
)
# Convert string values to numbers for chart
fig.data[0].y = [5, 10, 15, 25]
fig.data[1].y = [7.5, 15, 22.5, 37.5]
st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------
st.subheader("Platform presets")

platform_df = pd.DataFrame(
    {
        "Platform (--platform)": [
            "instagram_reels", "instagram_feed", "tiktok",
            "youtube_shorts", "youtube", "youtube_4k",
            "pinterest", "twitter", "vertical_4k",
        ],
        "Aspect ratio": [
            "9:16", "4:5", "9:16", "9:16", "16:9", "16:9",
            "1:1", "16:9", "9:16",
        ],
        "Max resolution": [
            "1080×1920", "1080×1350", "1080×1920", "1080×1920",
            "1920×1080", "3840×2160", "1080×1080", "1920×1080",
            "2160×3840",
        ],
    }
)
st.dataframe(platform_df, use_container_width=True)

st.code(
    """# Instagram Reels (9:16, quality auto)
drone-reel create --input ./clips/ --output reel.mp4 \\
  --platform instagram_reels --duration 30

# YouTube (16:9, keep source aspect)
drone-reel create --input ./clips/ --output video.mp4 \\
  --platform youtube --no-reframe --duration 60
""",
    language="bash",
)

# ---------------------------------------------------------------------------
st.subheader("Probe output metadata")

chosen = clip_selector("Select a clip to inspect encoding metadata")
info = video_info(chosen)
if info.get("codec"):
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Codec", info["codec"].upper())
    c2.metric("Bitrate", f"{info.get('bitrate_kbps', 0)} kbps")
    c3.metric("Color space", info.get("color_space", "?"))
    c4.metric("Color transfer", info.get("color_transfer", "?"))

page_footer("11_recipes.py", "Recipes")
