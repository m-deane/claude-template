"""
Chapter 04 — Scoring & Selection

Covers: 5-factor scoring + hook tiers; sliders for --score-weights / --hook-weights.
"""

import json
import re
import tempfile
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="04 Scoring", page_icon="", layout="wide")

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import (
    DEMO_OUTPUT_DIR,
    MULTI_SCENE_CLIP,
    clip_selector,
    run_drone_reel,
    show_command_expander,
    page_footer,
)

with st.sidebar:
    st.title("drone-reel Textbook")
    st.page_link("app.py", label="Home")
    st.page_link("pages/03_scene_detection.py", label="Prev: Scene Detection")
    st.page_link("pages/05_reframing.py", label="Next: Reframing")

# ---------------------------------------------------------------------------

st.title("Chapter 04 — Scoring & Selection")

st.info(
    "**What you'll learn:** How each of the 5 score components is calculated, "
    "what hook tiers mean, and how to tune `--score-weights` and `--hook-weights` "
    "for different footage styles."
)

# ---------------------------------------------------------------------------
st.subheader("The 5-factor scoring model")

st.markdown(
    """
    Every detected scene receives a composite score (0–100) from five sub-scores.
    The final score is a weighted sum; default weights sum to 1.0.
    """
)

factor_data = {
    "Factor": ["motion", "comp", "color", "sharp", "bright"],
    "Default Weight": [0.30, 0.20, 0.20, 0.15, 0.15],
    "What it measures": [
        "Optical-flow energy — how much camera/subject movement",
        "Rule-of-thirds balance, horizon straightness, depth",
        "Color saturation, variance, golden-hour detection",
        "Laplacian variance — focus/sharpness of key subjects",
        "Mean luminance — well-lit vs under/over-exposed",
    ],
    "Flag": [
        "--score-weights motion=X",
        "--score-weights comp=X",
        "--score-weights color=X",
        "--score-weights sharp=X",
        "--score-weights bright=X",
    ],
}
st.dataframe(pd.DataFrame(factor_data), use_container_width=True)

# ---------------------------------------------------------------------------
st.subheader("Interactive score-weight tuner")

st.markdown(
    "Adjust the five component weights below. They must sum to 1.0 — the app "
    "re-normalises automatically. Then click **Score Scenes** to run a real "
    "`drone-reel split --no-filter --json` with your weights."
)

col1, col2 = st.columns([1, 1])
with col1:
    w_motion = st.slider("motion weight", 0.0, 1.0, 0.30, 0.05)
    w_comp = st.slider("comp weight", 0.0, 1.0, 0.20, 0.05)
    w_color = st.slider("color weight", 0.0, 1.0, 0.20, 0.05)
with col2:
    w_sharp = st.slider("sharp weight", 0.0, 1.0, 0.15, 0.05)
    w_bright = st.slider("bright weight", 0.0, 1.0, 0.15, 0.05)

total = w_motion + w_comp + w_color + w_sharp + w_bright
if abs(total - 1.0) > 0.01:
    # Re-normalise
    scale = 1.0 / total if total > 0 else 1.0
    w_motion_n = round(w_motion * scale, 4)
    w_comp_n = round(w_comp * scale, 4)
    w_color_n = round(w_color * scale, 4)
    w_sharp_n = round(w_sharp * scale, 4)
    w_bright_n = round(w_bright * scale, 4)
    st.warning(
        f"Weights sum to {total:.2f} — re-normalised to sum=1.0: "
        f"motion={w_motion_n}, comp={w_comp_n}, color={w_color_n}, "
        f"sharp={w_sharp_n}, bright={w_bright_n}"
    )
else:
    w_motion_n, w_comp_n, w_color_n, w_sharp_n, w_bright_n = (
        w_motion, w_comp, w_color, w_sharp, w_bright,
    )

weight_str = (
    f"motion={w_motion_n},"
    f"comp={w_comp_n},"
    f"color={w_color_n},"
    f"sharp={w_sharp_n},"
    f"bright={w_bright_n}"
)
st.caption(f"Effective weights: `{weight_str}`")

# Weight distribution pie chart
fig_pie = px.pie(
    names=["motion", "comp", "color", "sharp", "bright"],
    values=[w_motion_n, w_comp_n, w_color_n, w_sharp_n, w_bright_n],
    title="Score weight distribution",
    color_discrete_sequence=px.colors.qualitative.Set2,
)
fig_pie.update_traces(textposition="inside", textinfo="percent+label")
st.plotly_chart(fig_pie, use_container_width=True)

if st.button("Score Scenes with these weights"):
    out_dir = DEMO_OUTPUT_DIR / "scoring"
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = out_dir / "manifest.json"

    with st.spinner("Running split --no-filter --json …"):
        result = run_drone_reel(
            [
                "split",
                "-i", str(MULTI_SCENE_CLIP),
                "-o", str(out_dir),
                "--no-filter",
                "--preview",
                "--score-weights", weight_str,
            ],
            show_error=True,
        )

    show_command_expander(
        result,
        python_snippet=f"""from utils import run_drone_reel, MULTI_SCENE_CLIP, DEMO_OUTPUT_DIR

result = run_drone_reel([
    "split",
    "-i", str(MULTI_SCENE_CLIP),
    "-o", str(DEMO_OUTPUT_DIR / "scoring"),
    "--no-filter",
    "--preview",
    "--score-weights", "{weight_str}",
])
""",
    )

    # Try to read manifest if it was written
    rows = _parse_scores_from_output(result.stdout + result.stderr)
    if rows:
        df = pd.DataFrame(rows).sort_values("score", ascending=False)
        st.success(f"Scored {len(df)} scenes. Ranked by composite score:")
        st.dataframe(
            df.style.background_gradient(subset=["score"], cmap="RdYlGn"),
            use_container_width=True,
        )
        # Bar chart
        fig = px.bar(
            df.head(20),
            x="scene",
            y="score",
            color="score",
            color_continuous_scale="RdYlGn",
            title="Scene scores (top 20)",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        with st.expander("Raw output"):
            st.code((result.stdout + result.stderr)[:3000], language="text")


def _parse_scores_from_output(text: str) -> list[dict]:
    """Extract scene scores from preview output."""
    scenes = []
    # Try JSON manifest first
    try:
        data = json.loads(text)
        if isinstance(data, list):
            for i, item in enumerate(data):
                scenes.append({
                    "scene": i + 1,
                    "score": item.get("score", 0),
                    "duration_s": item.get("duration", 0),
                    "start_s": item.get("start_time", 0),
                })
            return scenes
    except (json.JSONDecodeError, TypeError):
        pass

    # Parse text lines: "#1  0.00s  4.12s  score=71"
    pat = re.compile(
        r"(?:Scene\s*)?#?(\d+).*?(\d+\.?\d+)s?\s*[-–]?\s*(\d+\.?\d+)s?.*?score[=:\s]+(\d+\.?\d*)",
        re.IGNORECASE,
    )
    for m in pat.finditer(text):
        try:
            scenes.append({
                "scene": int(m.group(1)),
                "start_s": float(m.group(2)),
                "end_s": float(m.group(3)),
                "duration_s": round(float(m.group(3)) - float(m.group(2)), 2),
                "score": float(m.group(4)),
            })
        except ValueError:
            continue

    return scenes


# ---------------------------------------------------------------------------
st.subheader("Hook potential tiers")

st.markdown(
    """
    On top of the composite score, drone-reel classifies each scene into a **hook tier**
    for social-media virality assessment:
    """
)

hook_data = {
    "Tier": ["MAXIMUM", "HIGH", "MEDIUM", "LOW", "POOR"],
    "Score range": ["80–100", "65–79", "45–64", "25–44", "0–24"],
    "Example content": [
        "Wildlife close-up, sharp FPV flythrough, high-contrast golden hour",
        "Moving boat, dramatic reveal, glassy ocean reflection",
        "Static scenic mountain, coastline panorama, smooth orbit",
        "Empty ocean, distant subjects, flat midday light",
        "Overexposed sky, out-of-focus, no focal point",
    ],
    "flag": [
        "--hook-thresholds maximum=80",
        "--hook-thresholds high=65",
        "--hook-thresholds medium=45",
        "--hook-thresholds low=25",
        "(below low)",
    ],
}
st.dataframe(pd.DataFrame(hook_data), use_container_width=True)

st.markdown(
    """
    **`--hook-weights`** controls how the five sub-scores contribute to hook potential
    (separate from the composite score):

    ```bash
    drone-reel split -i footage.mp4 -o ./out/ \\
      --hook-weights "subject=0.40,motion=0.25,color=0.20,comp=0.10,unique=0.05"
    ```
    """
)

page_footer("05_reframing.py", "Reframing")
