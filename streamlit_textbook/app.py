"""
drone-reel Interactive Textbook — Landing Page
"""

import streamlit as st

st.set_page_config(
    page_title="drone-reel Textbook",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------

with st.sidebar:
    st.title("drone-reel Textbook")
    st.caption("v1.0 — Interactive Python CLI guide")

    st.markdown("**Chapters**")
    chapters = [
        ("01_welcome.py", "01 Welcome & Install"),
        ("02_drone_footage.py", "02 Drone Footage Formats"),
        ("03_scene_detection.py", "03 Scene Detection"),
        ("04_scoring_selection.py", "04 Scoring & Selection"),
        ("05_reframing.py", "05 Reframing"),
        ("06_stabilization.py", "06 Stabilization"),
        ("07_speed_correction.py", "07 Speed Correction"),
        ("08_color_grading.py", "08 Color Grading"),
        ("09_beat_sync.py", "09 Beat Sync"),
        ("10_encoding.py", "10 Encoding & Output"),
        ("11_recipes.py", "11 Recipes"),
        ("12_cli_reference.py", "12 CLI Reference"),
    ]
    for page_file, label in chapters:
        st.page_link(f"pages/{page_file}", label=label)

    st.divider()
    st.markdown("**About**")
    st.caption("drone-reel 1.0.0")
    st.page_link("pages/12_cli_reference.py", label="Full CLI Reference")

# ---------------------------------------------------------------------------
# Landing content
# ---------------------------------------------------------------------------

st.title("drone-reel Interactive Textbook")
st.markdown(
    """
    Welcome to the interactive textbook for **drone-reel** — a Python CLI that turns raw drone
    footage into polished, beat-synced vertical reels with a single command.
    """
)

col1, col2, col3 = st.columns(3)
with col1:
    st.info("**12 chapters** covering theory and practice — from colorspace to CLI flags.")
with col2:
    st.info("**Live demos** backed by real `drone-reel` subprocess calls on bundled clips.")
with col3:
    st.info("**Interactive widgets** — sliders, selectors, and upload widgets for your own footage.")

st.markdown("---")
st.subheader("Quick start")

st.code(
    """pip install -e ".[dev]"   # from parent directory

# Create a 30-second reel
drone-reel create --input ./clips/ --output reel.mp4 --duration 30

# Split a source video into graded highlight clips
drone-reel split -i source.mp4 -o ./out/ --color drone_aerial --auto-speed

# Preview scenes without rendering
drone-reel split -i source.mp4 -o ./out/ --preview
""",
    language="bash",
)

st.subheader("How to navigate")
st.markdown(
    """
Use the **sidebar** to jump to any chapter. Chapters build on each other but each is also
self-contained — jump straight to [Color Grading](pages/08_color_grading.py) or
[Recipes](pages/11_recipes.py) if you know what you need.

Every chapter has:
- A **"What you'll learn"** callout at the top.
- **Interactive widgets** that re-run real `drone-reel` commands.
- A **"Show the code"** expander revealing the exact shell command.
- **Warnings** for common gotchas (4K HEVC proxies, macOS AppleDouble files, etc.).
"""
)

st.subheader("Three core commands")

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("### `create`")
    st.markdown(
        "Full pipeline: detects scenes, scores them, reframes to vertical, "
        "beats-syncs transitions, and writes a finished reel."
    )
    st.page_link("pages/01_welcome.py", label="Learn more")
with c2:
    st.markdown("### `split`")
    st.markdown(
        "Splits a single source video into labelled highlight clips with optional "
        "color grading, stabilization, and speed correction applied per-clip."
    )
    st.page_link("pages/03_scene_detection.py", label="Learn more")
with c3:
    st.markdown("### `extract-clips`")
    st.markdown(
        "Extracts the top-N scenes from a video as individual files — "
        "handy for building a curated library before assembling a reel."
    )
    st.page_link("pages/01_welcome.py", label="Learn more")

st.divider()
st.caption(
    "drone-reel Textbook | Python 3.10+ | Streamlit 1.30+ | "
    "All demos run real CLI commands against bundled footage."
)
