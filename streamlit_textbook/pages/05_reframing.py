"""
Chapter 05 — Reframing

Covers: smart / pan / thirds / center reframe modes, saliency, sky mask,
rule of thirds. Side-by-side st.video() previews.
"""

import tempfile
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="05 Reframing", page_icon="", layout="wide")

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import (
    DEMO_OUTPUT_DIR,
    DEFAULT_CLIPS,
    clip_selector,
    extract_thumb,
    run_drone_reel,
    show_command_expander,
    page_footer,
)

with st.sidebar:
    st.title("drone-reel Textbook")
    st.page_link("app.py", label="Home")
    st.page_link("pages/04_scoring_selection.py", label="Prev: Scoring")
    st.page_link("pages/06_stabilization.py", label="Next: Stabilization")

# ---------------------------------------------------------------------------

st.title("Chapter 05 — Reframing")

st.info(
    "**What you'll learn:** How each `--reframe` mode crops horizontal drone footage "
    "to 9:16 vertical, what 'smart' actually computes, and when to use each mode."
)

# ---------------------------------------------------------------------------
st.subheader("Why reframe at all?")

st.markdown(
    """
    Drone cameras shoot 16:9 landscape.  Instagram Reels, TikTok, and YouTube Shorts
    all prefer **9:16 portrait** (or at minimum 4:5).  Naive center-crop loses ~44% of
    the frame horizontally.  drone-reel's reframe modes try to keep the most visually
    interesting content in the crop window.
    """
)

# ---------------------------------------------------------------------------
st.subheader("Reframe mode comparison")

modes_data = {
    "Mode": ["smart", "pan", "thirds", "center"],
    "Algorithm": [
        "Saliency map + sky detection → tracks subject horizontally",
        "Optical-flow → crops to follow camera motion direction",
        "Rule-of-thirds grid → bias crop toward grid intersections",
        "Fixed center crop — fast, no analysis",
    ],
    "Best for": [
        "Moving subjects, people, boats — keeps them in frame",
        "Panning shots — crop tracks the motion smoothly",
        "Landscape / scenery — compositional balance",
        "Symmetric scenes, fast preview, uniform sky shots",
    ],
    "flag": [
        "--reframe smart",
        "--reframe pan",
        "--reframe thirds",
        "--reframe center",
    ],
    "Speed": ["Slow", "Medium", "Medium", "Fast"],
}

import pandas as pd
st.dataframe(pd.DataFrame(modes_data), use_container_width=True)

# ---------------------------------------------------------------------------
st.subheader("How 'smart' reframing works")

col1, col2 = st.columns(2)
with col1:
    st.markdown(
        """
        **Step 1 — Sky mask**
        OpenCV detects the sky region by thresholding high-value,
        low-saturation pixels from the top portion of the frame.
        The crop avoids pulling exclusively into featureless sky.

        **Step 2 — Saliency map**
        OpenCV's `StaticSaliencySpectralResidual` highlights
        visually conspicuous regions (high spatial frequency, distinct
        colour from surroundings).
        """
    )
with col2:
    st.markdown(
        """
        **Step 3 — Crop centre**
        The horizontal crop centre is set to the weighted average of
        saliency mass below the sky line.

        **Step 4 — Temporal smoothing**
        Crop positions are smoothed over a rolling window so the crop
        doesn't jump between frames — giving a stable, stable feel.

        Combine with `--ken-burns moderate` for a gentle animated zoom
        that fills the static vertical frame.
        """
    )

# ---------------------------------------------------------------------------
st.subheader("Live reframe preview")

st.markdown(
    "Select a bundled clip and reframe mode, then click **Generate Preview** "
    "to create a short reframed clip. Due to full encode time, previews use "
    "a 5-second extract."
)

chosen_path = clip_selector("Select source clip")
reframe_mode = st.selectbox("--reframe mode", ["smart", "pan", "thirds", "center"])

col_a, col_b = st.columns(2)
with col_a:
    st.video(str(chosen_path))
    st.caption("Original (16:9)")

if st.button(f"Generate {reframe_mode} reframe preview"):
    out_dir = DEMO_OUTPUT_DIR / "reframe"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"reframe_{reframe_mode}_{chosen_path.stem}.mp4"

    if not out_path.exists():
        with st.spinner(f"Rendering {reframe_mode} reframe (first time only — cached after)…"):
            result = run_drone_reel(
                [
                    "create",
                    "-i", str(chosen_path),
                    "-o", str(out_path),
                    "--duration", "5",
                    "--reframe", reframe_mode,
                    "--no-color",
                    "--quality", "low",
                    "--clips", "1",
                ],
                timeout=120,
                show_error=True,
            )
        show_command_expander(
            result,
            python_snippet=f"""from utils import run_drone_reel

result = run_drone_reel([
    "create",
    "-i", str(chosen_path),
    "-o", "reframe_output.mp4",
    "--duration", "5",
    "--reframe", "{reframe_mode}",
    "--no-color",
    "--quality", "low",
    "--clips", "1",
])
""",
        )
    else:
        st.info("Using cached preview — delete `.cache/demo_outputs/reframe/` to re-render.")

    if out_path.exists():
        with col_b:
            st.video(str(out_path))
            st.caption(f"Reframed: --reframe {reframe_mode} (9:16)")
    else:
        st.warning(
            "Preview not generated. This may need your own footage — "
            "upload a clip below to try with user footage."
        )

# ---------------------------------------------------------------------------
st.subheader("Ken Burns for panoramic shots")

st.markdown(
    """
    For static or slow-pan drone shots that end up as a still crop, the
    `--ken-burns` flag adds a subtle animated zoom/pan.

    ```bash
    drone-reel create --input ./clips/ --output reel.mp4 \\
      --reframe smart \\
      --ken-burns moderate \\
      --kb-zoom-end 1.15 \\
      --kb-pan-x 0.08
    ```

    | Mode | End zoom | Pan |
    |---|---|---|
    | off | 1.0 (none) | 0 |
    | conservative | 1.05 | 0.03 |
    | moderate | 1.10 | 0.06 |
    | cinematic | 1.20 | 0.12 |
    """
)

page_footer("06_stabilization.py", "Stabilization")
