"""
Chapter 03 — Scene Detection

Covers: PySceneDetect, --scene-threshold, --analysis-scale,
--motion-energy-method; interactive threshold demo with Gantt timeline.
"""

import json
import re
import tempfile
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="03 Scene Detection", page_icon="", layout="wide")

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import (
    DEMO_OUTPUT_DIR,
    DRONE_REEL_BIN,
    MULTI_SCENE_CLIP,
    run_drone_reel,
    show_command_expander,
    page_footer,
)

with st.sidebar:
    st.title("drone-reel Textbook")
    st.page_link("app.py", label="Home")
    st.page_link("pages/02_drone_footage.py", label="Prev: Drone Footage Formats")
    st.page_link("pages/04_scoring_selection.py", label="Next: Scoring & Selection")

# ---------------------------------------------------------------------------

st.title("Chapter 03 — Scene Detection")

st.info(
    "**What you'll learn:** How PySceneDetect finds cut points, what the "
    "`--scene-threshold` slider actually controls, how `--analysis-scale` trades "
    "accuracy for speed, and how `--motion-energy-method` handles mixed clips."
)

# ---------------------------------------------------------------------------
st.subheader("How scene detection works")

st.markdown(
    """
    drone-reel wraps **PySceneDetect's ContentDetector** which measures the weighted
    mean squared difference (HSV channels) between consecutive frames.
    When this delta exceeds `--scene-threshold`, a new scene boundary is declared.

    ```
    frame_delta = w_H * delta_H + w_S * delta_S + w_V * delta_V
    if frame_delta > threshold:
        new scene boundary
    ```

    After boundary detection, each scene is scored on **5 factors** (motion, composition,
    color, sharpness, brightness — see Chapter 04) using optical-flow analysis at
    `--analysis-scale` resolution.
    """
)

col1, col2 = st.columns(2)
with col1:
    st.markdown(
        """
        **`--scene-threshold`** (1–100, default 27)
        - **Low (5–15):** More scene boundaries — catches subtle color changes and slow pans.
          Risk of over-segmenting static shots.
        - **Default (27):** Balanced for drone footage with smooth motion.
        - **High (40–60):** Fewer boundaries — only hard cuts and major lighting changes.
        """
    )
with col2:
    st.markdown(
        """
        **`--analysis-scale`** (0.25–1.0, default 0.5)
        - Downscales frames before optical-flow analysis.
        - `0.25` = 4× faster, slightly less accurate motion vectors.
        - `1.0` = full resolution (best for 4K).
        - For 1080p footage `0.5` is a good default.

        **`--motion-energy-method`**
        - `mean`: average flow — good for steady pans.
        - `p95`: 95th-percentile — catches peak motion in mixed clips (camera shake + smooth pan).
        """
    )

# ---------------------------------------------------------------------------
st.subheader("Interactive threshold demo")

st.markdown(
    "Adjust the threshold and click **Detect Scenes** to run a real `--preview` pass "
    "on the bundled multi-scene clip and visualize the cut points."
)

threshold = st.slider(
    "--scene-threshold",
    min_value=5,
    max_value=60,
    value=27,
    step=1,
    help="Lower = more scene cuts; higher = fewer, only hard cuts.",
)

analysis_scale = st.select_slider(
    "--analysis-scale",
    options=[0.25, 0.33, 0.5, 0.75, 1.0],
    value=0.5,
)

if st.button("Detect Scenes (preview — no render)"):
    with st.spinner(f"Running scene detection at threshold={threshold}…"):
        out_dir = DEMO_OUTPUT_DIR / f"detect_{threshold}"
        out_dir.mkdir(parents=True, exist_ok=True)

        result = run_drone_reel(
            [
                "split",
                "-i", str(MULTI_SCENE_CLIP),
                "-o", str(out_dir),
                "--scene-threshold", str(threshold),
                "--analysis-scale", str(analysis_scale),
                "--preview",
                "--no-filter",
            ],
            show_error=True,
        )

    show_command_expander(
        result,
        python_snippet="""from utils import run_drone_reel, MULTI_SCENE_CLIP, DEMO_OUTPUT_DIR

result = run_drone_reel([
    "split",
    "-i", str(MULTI_SCENE_CLIP),
    "-o", str(DEMO_OUTPUT_DIR / "detect"),
    "--scene-threshold", "27",
    "--analysis-scale", "0.5",
    "--preview",
    "--no-filter",
])
""",
    )

    if result.ok or result.stdout:
        # Parse preview output: look for lines like "Scene N: 0.00s – 3.45s (score: 72)"
        output_text = result.stdout + result.stderr
        scenes = _parse_preview_output(output_text)

        if scenes:
            st.success(f"Found **{len(scenes)} scenes** at threshold={threshold}")
            _render_gantt(scenes, threshold)

            df = pd.DataFrame(scenes)
            if "score" in df.columns:
                df["score"] = df["score"].round(1)
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("Could not parse scene boundaries from preview output.")
            with st.expander("Raw output"):
                st.code(output_text[:3000], language="text")


def _parse_preview_output(text: str) -> list[dict]:
    """Extract scene info from drone-reel --preview stdout."""
    scenes = []
    # Patterns: "Scene 1: 0.00s – 4.12s" or "  #1  0.000s  4.120s  score=71"
    # Try multiple patterns
    patterns = [
        # "Scene  1: 0.00s - 4.12s  score: 71"
        re.compile(r"Scene\s+(\d+).*?(\d+\.?\d*)s\s*[-–]\s*(\d+\.?\d*)s.*?score[:\s]+(\d+)", re.IGNORECASE),
        # "#1  0.000  4.120  score=71"
        re.compile(r"#(\d+)\s+(\d+\.?\d+)\s+(\d+\.?\d+).*?(?:score[=:\s]+(\d+))?", re.IGNORECASE),
        # Plain time ranges "0.00s - 3.45s"
        re.compile(r"(\d+\.?\d+)s?\s*[-–]+\s*(\d+\.?\d+)s?"),
    ]

    for pat in patterns:
        matches = list(pat.finditer(text))
        if matches and len(matches) >= 2:
            for i, m in enumerate(matches):
                groups = m.groups()
                try:
                    if len(groups) >= 3:
                        idx = int(groups[0]) if groups[0] else i + 1
                        start = float(groups[1])
                        end = float(groups[2])
                        score = float(groups[3]) if len(groups) > 3 and groups[3] else 50.0
                    else:
                        idx = i + 1
                        start = float(groups[0])
                        end = float(groups[1])
                        score = 50.0

                    if end > start:
                        scenes.append({
                            "scene": idx,
                            "start_s": round(start, 2),
                            "end_s": round(end, 2),
                            "duration_s": round(end - start, 2),
                            "score": score,
                        })
                except (ValueError, IndexError):
                    continue
            if scenes:
                break

    return scenes


def _render_gantt(scenes: list[dict], threshold: int) -> None:
    """Render a Plotly Gantt-style timeline of scene cuts."""
    import datetime

    rows = []
    for s in scenes:
        rows.append({
            "Scene": f"Scene {s['scene']}",
            "Start": datetime.datetime(2000, 1, 1, 0, 0, 0) + datetime.timedelta(seconds=s["start_s"]),
            "End": datetime.datetime(2000, 1, 1, 0, 0, 0) + datetime.timedelta(seconds=s["end_s"]),
            "Score": s.get("score", 50),
            "Duration": f"{s['duration_s']:.2f}s",
        })

    if not rows:
        return

    df = pd.DataFrame(rows)
    fig = px.timeline(
        df,
        x_start="Start",
        x_end="End",
        y="Scene",
        color="Score",
        color_continuous_scale="RdYlGn",
        hover_data=["Duration", "Score"],
        title=f"Scene Timeline — threshold={threshold} ({len(scenes)} scenes)",
    )
    fig.update_layout(
        xaxis_title="Time (seconds from start)",
        yaxis_title="Scene",
        height=max(300, len(scenes) * 30 + 100),
        xaxis=dict(
            tickformat="%S.%L",
        ),
    )
    st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------------------------
st.subheader("Threshold sensitivity guide")

thresh_df = pd.DataFrame(
    {
        "Threshold": [5, 10, 15, 27, 35, 50],
        "Typical scene count (10min clip)": [80, 50, 35, 20, 12, 6],
        "Best for": [
            "Time-lapses, hard cuts",
            "Fast-paced edit, many cuts",
            "Music video style",
            "Drone default (smooth transitions)",
            "Documentary / slow pans",
            "Long static landscape shots",
        ],
    }
)
st.dataframe(thresh_df, use_container_width=True)

st.warning(
    "DJI 4K 60fps HEVC: `SceneDetector.frame_skip` is auto-set to 1 for >35fps sources. "
    "For best results, build a 720p proxy first (see Chapter 02)."
)

page_footer("04_scoring_selection.py", "Scoring & Selection")
