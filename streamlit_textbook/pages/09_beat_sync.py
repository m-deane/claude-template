"""
Chapter 09 — Beat Sync

Covers: librosa beat tracking, --beat-mode all vs downbeat,
synthetic click-track visualization.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="09 Beat Sync", page_icon="", layout="wide")

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import page_footer

with st.sidebar:
    st.title("drone-reel Textbook")
    st.page_link("app.py", label="Home")
    st.page_link("pages/08_color_grading.py", label="Prev: Color Grading")
    st.page_link("pages/10_encoding.py", label="Next: Encoding")

# ---------------------------------------------------------------------------

st.title("Chapter 09 — Beat Sync")

st.info(
    "**What you'll learn:** How librosa extracts beats from a music track, "
    "the difference between `--beat-mode all` and `downbeat`, and how to "
    "align clip transitions to the music."
)

# ---------------------------------------------------------------------------
st.subheader("How beat tracking works")

st.markdown(
    """
    drone-reel's `BeatSync` class uses **librosa** to analyse the music track:

    1. **Onset envelope** — `librosa.onset.onset_strength()` computes the spectral
       flux at each frame.
    2. **Beat tracking** — `librosa.beat.beat_track()` finds the grid of beat positions
       by maximising an accumulated onset strength along a recurrence matrix.
    3. **Downbeat detection** — every Nth beat is classified as a downbeat (bar start)
       using the beat period and onset energy.

    The result is a list of **beat timestamps** and **downbeat timestamps** that the
    `SceneSequencer` uses to snap clip boundaries to.
    """
)

# ---------------------------------------------------------------------------
st.subheader("Beat mode comparison")

col1, col2 = st.columns(2)
with col1:
    st.markdown(
        """
        ### `--beat-mode all`
        Cuts on **every detected beat**.

        - Typical cuts: every 0.5–1.0s at 120 BPM
        - Great for fast-paced action reels
        - Can feel frenetic with long clips (they get trimmed aggressively)
        """
    )
with col2:
    st.markdown(
        """
        ### `--beat-mode downbeat` (recommended)
        Cuts only on **bar starts** (every 4th beat at 4/4 time).

        - Typical cuts: every 2–4s
        - More cinematic, less frenetic
        - Leaves enough of each scene to appreciate the imagery
        """
    )

# ---------------------------------------------------------------------------
st.subheader("Synthetic beat visualizer")

st.markdown(
    "This interactive demo synthesizes a click-track at your chosen BPM and shows "
    "where cuts would land under `all` vs `downbeat` modes for a 30-second reel."
)

bpm = st.slider("BPM", 60, 180, 120, step=5)
duration = st.slider("Reel duration (seconds)", 10, 60, 30, step=5)
beat_mode = st.radio("Beat mode", ["all", "downbeat"], horizontal=True)
beats_per_bar = st.selectbox("Time signature (beats per bar)", [4, 3, 2], index=0)

beat_period = 60.0 / bpm
beats = np.arange(0, duration, beat_period)
downbeats = beats[::beats_per_bar]

if beat_mode == "all":
    cut_times = beats
else:
    cut_times = downbeats

n_clips = len(cut_times)
avg_clip_len = duration / n_clips if n_clips > 0 else duration

st.metric("Number of cuts", n_clips)
st.metric("Average clip length", f"{avg_clip_len:.2f}s")

# Build timeline figure
fig = go.Figure()

# Background: reel duration bar
fig.add_shape(
    type="rect",
    x0=0, x1=duration, y0=0.2, y1=0.8,
    fillcolor="#ECEFF1", line_color="#90A4AE",
)

# All beats (faint)
for b in beats:
    fig.add_shape(
        type="line",
        x0=b, x1=b, y0=0.2, y1=0.8,
        line=dict(color="#B0BEC5", width=1, dash="dot"),
    )

# Cut points (bold)
for c in cut_times:
    fig.add_shape(
        type="line",
        x0=c, x1=c, y0=0.15, y1=0.85,
        line=dict(color="#1565C0", width=2),
    )
    fig.add_annotation(
        x=c, y=0.9,
        text=f"{c:.1f}s",
        showarrow=False,
        font=dict(size=8),
        textangle=-45,
    )

fig.update_layout(
    title=f"Cut points — {beat_mode} mode, {bpm} BPM, {n_clips} cuts",
    xaxis=dict(title="Time (seconds)", range=[-0.5, duration + 0.5]),
    yaxis=dict(visible=False, range=[0, 1.1]),
    height=220,
    margin=dict(t=50, b=10),
)
st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------
st.subheader("Using beat sync with drone-reel create")

st.code(
    """# Beat-sync using every beat (120 BPM track → cut every 0.5s)
drone-reel create --input ./clips/ --output reel.mp4 \\
  --music track.mp3 \\
  --beat-mode all \\
  --duration 30

# Downbeat only (cuts every ~2s) — more cinematic
drone-reel create --input ./clips/ --output reel.mp4 \\
  --music track.mp3 \\
  --beat-mode downbeat \\
  --duration 30

# Analyse a track standalone
drone-reel beats --input track.mp3
""",
    language="bash",
)

# ---------------------------------------------------------------------------
st.subheader("No music? Supply your own")

uploaded_music = st.file_uploader(
    "Upload an MP3 or WAV to analyse (path shown below — run CLI manually)",
    type=["mp3", "wav", "m4a"],
)
if uploaded_music:
    import tempfile, os
    with tempfile.NamedTemporaryFile(suffix=Path(uploaded_music.name).suffix, delete=False) as f:
        f.write(uploaded_music.getbuffer())
        tmp_path = Path(f.name)
    st.info(f"Saved to: `{tmp_path}`")
    st.code(f"drone-reel beats --input {tmp_path}", language="bash")

st.warning(
    "Beat sync only activates when you pass `--music <track>` to `drone-reel create`. "
    "The `split` command does NOT support beat sync — it is a per-clip operation only."
)

page_footer("10_encoding.py", "Encoding & Output")
