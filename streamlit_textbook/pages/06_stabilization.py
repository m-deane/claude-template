"""
Chapter 06 — Stabilization

Covers: adaptive stab, --stab-strength, --roll-correction, --gimbal-bounce-recovery,
before/after preview.
"""

from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="06 Stabilization", page_icon="", layout="wide")

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import (
    DEMO_OUTPUT_DIR,
    DEFAULT_CLIPS,
    clip_selector,
    run_drone_reel,
    show_command_expander,
    page_footer,
)

with st.sidebar:
    st.title("drone-reel Textbook")
    st.page_link("app.py", label="Home")
    st.page_link("pages/05_reframing.py", label="Prev: Reframing")
    st.page_link("pages/07_speed_correction.py", label="Next: Speed Correction")

# ---------------------------------------------------------------------------

st.title("Chapter 06 — Stabilization")

st.info(
    "**What you'll learn:** How drone-reel detects camera shake, how the Farneback "
    "optical-flow stabilizer works, what each `--stab-strength` mode does, and "
    "when to use `--roll-correction` and `--gimbal-bounce-recovery`."
)

# ---------------------------------------------------------------------------
st.subheader("How shake detection works")

st.markdown(
    """
    During scene scoring, drone-reel computes a **shake score** (0–100) per clip:

    1. **Optical flow field** — Farneback dense flow is computed between consecutive frames.
    2. **Translation variance** — mean and std-dev of the flow vectors.  High std-dev = shaky.
    3. **Shake score** — normalised to 0–100 (higher = shakier).

    If the shake score exceeds `--shake-tolerance` (default 40), the scene is filtered
    out by `SceneFilter` — unless `--stab-strength` is set or `--stabilize-all` is used.
    """
)

# ---------------------------------------------------------------------------
st.subheader("Stabilization modes")

modes_df = pd.DataFrame(
    {
        "Mode": ["off", "light", "adaptive", "full"],
        "Flag": [
            "--stab-strength off",
            "--stab-strength light",
            "--stab-strength adaptive",
            "--stab-strength full",
        ],
        "What it does": [
            "No stabilization applied. Clips with shake > shake-tolerance are still filtered.",
            "Applies a single-pass affine warp with a 15-frame smoothing window. Fast.",
            "Detects shake score per-clip; only stabilizes clips above the threshold (default). "
            "Equivalent to --stabilize flag.",
            "Forces full stabilization on every clip regardless of shake score. Use with "
            "--stabilize-all.",
        ],
        "Best for": [
            "Already-stabilized gimbal footage / EIS-corrected video",
            "Mild hand-held shake or gentle prop vibration",
            "Mixed footage — stable and shaky clips in same batch",
            "All handheld or windy-day footage",
        ],
    }
)
st.dataframe(modes_df, use_container_width=True)

# ---------------------------------------------------------------------------
st.subheader("Key stabilization parameters")

col1, col2 = st.columns(2)
with col1:
    st.markdown(
        """
        **`--smooth-radius N`** (5–120, default 30)
        Temporal window size for trajectory smoothing.
        - 5–15: Light touch — preserves intentional camera moves like pans
        - 30: Default — balances stability vs motion preservation
        - 60–120: Aggressive — nearly locks the frame; may crop intentional pans
        """
    )
    st.markdown(
        """
        **`--border-crop F`** (0.0–0.15, default 0.05)
        Fraction of frame edges cropped after stabilization to hide
        black borders introduced by the affine warp.
        Increase to 0.10–0.12 for heavily stabilized footage.
        """
    )
with col2:
    st.markdown(
        """
        **`--max-corners N`** (50–500, default 200)
        Number of Shi-Tomasi feature points tracked per frame.
        - Lower (50–100): Better for sky/water with few features
        - Higher (300–500): Better for urban/forest with many features
        """
    )
    st.markdown(
        """
        **`--roll-correction F`** (0.0–1.0, default 0.0)
        Corrects per-frame rotation (roll) derived from optical flow.
        Useful for horizon tilt from propeller imbalance.
        `0.3` = subtle, `1.0` = full inverse roll correction.
        """
    )

# ---------------------------------------------------------------------------
st.subheader("Gimbal bounce recovery")

st.markdown(
    """
    **`--gimbal-bounce-recovery`** injects a 0.95× speed ramp around detected
    motion-reversal events (sign flip in dx/dy flow with magnitude > 2.0 px/frame).
    This is a 0.4s window centred on each bounce — enough to smooth the visual jolt
    without making the overall clip feel slow.

    Use with `--auto-speed` (Chapter 07) for the full correction pipeline:

    ```bash
    drone-reel split -i footage.mp4 -o ./out/ \\
      --stabilize \\
      --smooth-radius 40 \\
      --roll-correction 0.3 \\
      --auto-speed \\
      --gimbal-bounce-recovery
    ```
    """
)

# ---------------------------------------------------------------------------
st.subheader("Before / after stabilization preview")

chosen_path = clip_selector("Select clip to stabilize")
stab_mode = st.selectbox("--stab-strength", ["light", "adaptive", "full"])
smooth_r = st.slider("--smooth-radius", 5, 120, 30)

if st.button("Generate stabilized preview"):
    out_dir = DEMO_OUTPUT_DIR / "stab"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"stab_{stab_mode}_r{smooth_r}_{chosen_path.stem}.mp4"

    col_left, col_right = st.columns(2)
    with col_left:
        st.video(str(chosen_path))
        st.caption("Original")

    if not out_path.exists():
        with st.spinner("Stabilizing (first render — cached after)…"):
            result = run_drone_reel(
                [
                    "split",
                    "-i", str(chosen_path),
                    "-o", str(out_dir),
                    "--stab-strength", stab_mode,
                    "--smooth-radius", str(smooth_r),
                    "--no-filter",
                    "--count", "1",
                    "--overwrite",
                ],
                timeout=180,
                show_error=True,
            )
        show_command_expander(
            result,
            python_snippet=f"""from utils import run_drone_reel

result = run_drone_reel([
    "split", "-i", "input.mp4", "-o", "./out/",
    "--stab-strength", "{stab_mode}",
    "--smooth-radius", "{smooth_r}",
    "--no-filter", "--count", "1",
])
""",
        )

        # Find the written output file
        written = sorted(out_dir.glob("*.mp4"), key=lambda p: p.stat().st_mtime)
        if written and written[-1] != out_path:
            import shutil
            shutil.copy(written[-1], out_path)

    if out_path.exists():
        with col_right:
            st.video(str(out_path))
            st.caption(f"Stabilized: {stab_mode}, smooth-radius={smooth_r}")
    else:
        st.info(
            "Stabilized file not found — the clip may already be very stable "
            "(adaptive mode skips stable clips). Try `--stab-strength full`."
        )

st.warning(
    "Heavy stabilization (`smooth-radius ≥ 60`) may crop intentional pans "
    "and make them look 'locked off'.  Use `adaptive` (default) unless you know "
    "the footage is shaky."
)

page_footer("07_speed_correction.py", "Speed Correction")
