"""
Chapter 01 — Welcome & Install

Covers: what drone-reel does, installation, and the
create vs split vs extract-clips command distinction.
"""

import subprocess
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="01 Welcome", page_icon="", layout="wide")

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import DRONE_REEL_BIN, run_drone_reel, show_command_expander, page_footer

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title("drone-reel Textbook")
    st.page_link("app.py", label="Home")
    st.page_link("pages/02_drone_footage.py", label="Next: Drone Footage Formats")

# ---------------------------------------------------------------------------

st.title("Chapter 01 — Welcome & Install")

st.info(
    "**What you'll learn:** What drone-reel does end-to-end, how to install it, "
    "and the difference between `create`, `split`, and `extract-clips`."
)

st.markdown(
    """
    **drone-reel** is a Python CLI that turns raw drone footage into polished,
    Instagram-ready vertical reels automatically.  It handles scene detection,
    visual quality scoring, intelligent reframing, shake stabilization, beat-synced
    transitions, and BT.709 SDR encoding — all from a single shell command.
    """
)

# ---------------------------------------------------------------------------
st.subheader("Installation")

st.code(
    """# Clone the repo and install in editable mode
git clone https://github.com/YOUR_ORG/drone-reel.git
cd drone-reel
pip install -e ".[dev]"

# Verify
drone-reel --version
""",
    language="bash",
)

st.warning(
    "macOS + exFAT drives: AppleDouble `._` files leak into glob patterns "
    "and cause ffprobe to choke. drone-reel filters them automatically, "
    "but custom scripts that use `Path.glob('*.mp4')` should add "
    "`if not p.name.startswith('._')`."
)

# ---------------------------------------------------------------------------
st.subheader("The three commands")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        #### `create`
        **Full pipeline** — give it a directory of clips (or a single file) and get back a finished reel.

        ```bash
        drone-reel create \\
          --input ./clips/ \\
          --output reel.mp4 \\
          --duration 30 \\
          -c drone_aerial
        ```

        Internally runs: SceneDetector → SceneFilter → SceneSequencer →
        DiversitySelector → DurationAdjuster → BeatSync → VideoProcessor
        → Stabilizer → Reframer → ColorGrader.
        """
    )

with col2:
    st.markdown(
        """
        #### `split`
        **Per-clip processing** — splits a single video into labelled highlight
        clips, applying grading/stab/speed per-clip before writing.

        ```bash
        drone-reel split \\
          -i source.mp4 -o ./out/ \\
          --color drone_aerial \\
          --auto-speed \\
          --stabilize
        ```

        Pipeline: SceneDetector → SceneFilter → stabilize → speed-ramp
        → color grade → letterbox → write.
        """
    )

with col3:
    st.markdown(
        """
        #### `extract-clips`
        **Library builder** — exports the top-N scored scenes as individual
        files without additional processing.  Great for curating a clip library.

        ```bash
        drone-reel extract-clips \\
          --input source.mp4 \\
          --output ./library/ \\
          -n 10
        ```

        Use this before `create` when you want fine-grained control over which
        clips go into the reel.
        """
    )

# ---------------------------------------------------------------------------
st.subheader("Live version check")

if st.button("Run `drone-reel --version`"):
    result = run_drone_reel(["--version"])
    if result.ok:
        st.success(result.stdout.strip() or result.stderr.strip())
    show_command_expander(
        result,
        python_snippet="""from utils import run_drone_reel
result = run_drone_reel(["--version"])
print(result.stdout)
""",
    )

# ---------------------------------------------------------------------------
st.subheader("Pipeline architecture")

st.markdown(
    """
    ```
    Input clips
        └── SceneDetector          (PySceneDetect + OpenCV optical flow)
            └── SceneFilter        (min score, duration, brightness, shake)
                └── SceneSequencer (narrative ordering)
                    └── DiversitySelector (avoid visual repetition)
                        └── DurationAdjuster (fit target runtime)
                            └── BeatSync   (librosa beat tracking)
                                └── VideoProcessor (stitch, transitions)
                                    └── Stabilizer (Farneback + affine)
                                        └── Reframer (smart/pan/thirds)
                                            └── ColorGrader (LUT + curves)
                                                └── Output MP4 (BT.709 SDR)
    ```

    The `split` command uses a shorter per-clip path:
    `SceneDetector → SceneFilter → stabilize → speed-ramp → grade → letterbox → write`
    """
)

page_footer("02_drone_footage.py", "Drone Footage Formats")
