"""
Chapter 11 — Recipes

8 named recipes as copy-pastable shell blocks, each with a
"Run this recipe on a sample clip" button that fires the actual command.
"""

from pathlib import Path

import streamlit as st

st.set_page_config(page_title="11 Recipes", page_icon="", layout="wide")

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import (
    ASSETS_DIR,
    DEMO_OUTPUT_DIR,
    DEFAULT_CLIPS,
    MULTI_SCENE_CLIP,
    run_drone_reel,
    show_command_expander,
    page_footer,
)

with st.sidebar:
    st.title("drone-reel Textbook")
    st.page_link("app.py", label="Home")
    st.page_link("pages/10_encoding.py", label="Prev: Encoding")
    st.page_link("pages/12_cli_reference.py", label="Next: CLI Reference")

# ---------------------------------------------------------------------------

st.title("Chapter 11 — Recipes")

st.info(
    "**What you'll learn:** 8 ready-to-run recipes covering the most common drone-reel "
    "use cases. Each recipe is a copy-pastable shell block with an explanation, "
    "plus a live 'Run on sample clip' button."
)

# ---------------------------------------------------------------------------
# Recipe definitions
# ---------------------------------------------------------------------------

# Pick the smallest bundled clip for live demos (fast)
DEMO_CLIP = list(DEFAULT_CLIPS.values())[0]  # clip_a.mp4 — smallest (~2 MB)
DEMO_MULTI = MULTI_SCENE_CLIP

RECIPES: list[dict] = [
    {
        "id": "quick_reel",
        "title": "01 — Quick Instagram Reel (30s)",
        "description": (
            "The simplest possible reel. Pulls the best scenes from a clip directory, "
            "reframes to 9:16, applies the `drone_aerial` color grade, and encodes for "
            "Instagram Reels. No music, no stab — just fast."
        ),
        "shell": """\
drone-reel create \\
  --input ./clips/ \\
  --output reel.mp4 \\
  --platform instagram_reels \\
  --duration 30 \\
  --color drone_aerial \\
  --reframe smart
""",
        "demo_args": [
            "create",
            "-i", str(DEMO_CLIP),
            "-o", str(DEMO_OUTPUT_DIR / "r01_quick_reel.mp4"),
            "--platform", "instagram_reels",
            "--duration", "5",
            "--color", "drone_aerial",
            "--reframe", "smart",
            "--clips", "1",
        ],
    },
    {
        "id": "viral_preset",
        "title": "02 — Viral Preset",
        "description": (
            "The `--viral` flag applies a curated combination: 15s duration, 60% color "
            "intensity, speed ramping, Instagram Reels format. Pair with a track at 120+ BPM."
        ),
        "shell": """\
drone-reel create \\
  --input ./clips/ \\
  --output viral.mp4 \\
  --viral \\
  --color teal_orange \\
  --music track.mp3
""",
        "demo_args": [
            "create",
            "-i", str(DEMO_CLIP),
            "-o", str(DEMO_OUTPUT_DIR / "r02_viral.mp4"),
            "--viral",
            "--color", "teal_orange",
            "--clips", "1",
        ],
    },
    {
        "id": "cinematic_split",
        "title": "03 — Cinematic Split with Full Post-Processing",
        "description": (
            "Split a source video into graded highlight clips ready to hand off to an editor. "
            "Applies stabilization, speed correction, anamorphic letterbox, and cinematic grade."
        ),
        "shell": """\
drone-reel split \\
  -i source.mp4 \\
  -o ./highlights/ \\
  --color cinematic \\
  --color-intensity 0.7 \\
  --vignette 0.3 \\
  --letterbox 2.35 \\
  --stabilize \\
  --stab-strength adaptive \\
  --auto-speed \\
  --speed-correction-profile cinematic \\
  --ease-speed-ramps \\
  --min-score 50 \\
  --min-duration 3 \\
  --max-duration 12
""",
        "demo_args": [
            "split",
            "-i", str(DEMO_MULTI),
            "-o", str(DEMO_OUTPUT_DIR / "r03_cinematic_split/"),
            "--color", "cinematic",
            "--color-intensity", "0.7",
            "--vignette", "0.3",
            "--letterbox", "2.35",
            "--auto-speed",
            "--speed-correction-profile", "cinematic",
            "--min-score", "40",
            "--count", "2",
            "--preview",
        ],
        "demo_note": "Demo runs --preview (no render) to keep it fast.",
    },
    {
        "id": "golden_hour",
        "title": "04 — Golden Hour Landscape Reel",
        "description": (
            "Optimised for warm-light aerial footage. Boosts the golden-hour grade, "
            "uses pan reframing to follow the horizon, and keeps clips to 4–8s for breathing room."
        ),
        "shell": """\
drone-reel create \\
  --input ./golden_clips/ \\
  --output golden_hour_reel.mp4 \\
  --color golden_hour \\
  --color-intensity 0.85 \\
  --halation 0.25 \\
  --vignette 0.4 \\
  --reframe pan \\
  --aspect 9:16 \\
  --duration 45 \\
  --quality high
""",
        "demo_args": [
            "split",
            "-i", str(DEMO_MULTI),
            "-o", str(DEMO_OUTPUT_DIR / "r04_golden/"),
            "--color", "golden_hour",
            "--color-intensity", "0.85",
            "--halation", "0.25",
            "--vignette", "0.4",
            "--count", "2",
            "--preview",
        ],
        "demo_note": "Demo runs --preview (no render) to keep it fast.",
    },
    {
        "id": "proxy_workflow",
        "title": "05 — 4K HEVC Proxy Workflow",
        "description": (
            "DJI 4K 60fps HEVC takes 40+ minutes to analyse at native resolution. "
            "Build a 720p proxy with ffmpeg first, run split on the proxy, then "
            "use the detected timestamps to extract from the original if needed."
        ),
        "shell": """\
# Step 1: Create proxy (run once)
ffmpeg -i DJI_0341.MP4 \\
  -vf scale=1280:720 -r 30 \\
  -c:v libx264 -preset ultrafast -crf 26 -an \\
  proxy_0341.mp4

# Step 2: Analyse proxy (fast — ~11 min instead of 40+)
drone-reel split \\
  -i proxy_0341.mp4 \\
  -o ./highlights/ \\
  --color drone_aerial \\
  --auto-speed \\
  --json \\
  --min-score 50
""",
        "demo_args": None,  # no live demo (needs user footage)
    },
    {
        "id": "dlog_grade",
        "title": "06 — D-Log Footage Grading Pipeline",
        "description": (
            "If your DJI drone shoots D-Log or D-Log M, you must tell drone-reel the "
            "input colorspace so it tone-maps correctly before applying the grade."
        ),
        "shell": """\
drone-reel split \\
  -i dlog_footage.mp4 \\
  -o ./graded/ \\
  --input-colorspace dlog \\
  --color drone_aerial \\
  --color-intensity 0.75 \\
  --auto-wb \\
  --denoise 0.2 \\
  --min-score 45
""",
        "demo_args": None,  # needs D-Log source
    },
    {
        "id": "highlight_library",
        "title": "07 — Build a Highlight Library",
        "description": (
            "Extract the top-10 scenes from every flight as timestamped clips, "
            "then assemble a reel from the library. Separates curation from grading."
        ),
        "shell": """\
# Extract top-10 scenes per source file (no grading)
for f in ./raw/*.mp4; do
  name=$(basename "$f" .mp4)
  drone-reel extract-clips \\
    --input "$f" \\
    --output "./library/$name/" \\
    -n 10 \\
    --min-score 45
done

# Assemble reel from library
drone-reel create \\
  --input ./library/ \\
  --output final_reel.mp4 \\
  --color drone_aerial \\
  --duration 60 \\
  --platform youtube
""",
        "demo_args": None,  # multi-step, needs user footage
    },
    {
        "id": "preview_then_render",
        "title": "08 — Preview Scenes Before Rendering",
        "description": (
            "Always preview first on long source files. `--preview` runs the full "
            "detection and scoring pipeline but writes no video files, giving you "
            "the scene manifest in seconds."
        ),
        "shell": """\
# Preview: see all scenes and scores, no render
drone-reel split \\
  -i source.mp4 \\
  -o ./out/ \\
  --preview \\
  --no-filter \\
  --scene-threshold 20 \\
  --json

# If happy with the manifest, render with identical flags (remove --preview)
drone-reel split \\
  -i source.mp4 \\
  -o ./out/ \\
  --no-filter \\
  --scene-threshold 20 \\
  --json \\
  --color drone_aerial
""",
        "demo_args": [
            "split",
            "-i", str(DEMO_MULTI),
            "-o", str(DEMO_OUTPUT_DIR / "r08_preview/"),
            "--preview",
            "--no-filter",
            "--scene-threshold", "20",
        ],
    },
    {
        "id": "score_weight_tune",
        "title": "09 — Score-Weight Tuning for FPV Footage",
        "description": (
            "FPV footage has very high motion energy but often poor composition. "
            "Boost `motion` weight and reduce `comp` + `sharp` thresholds so the "
            "most dynamic shots win even if they're slightly soft."
        ),
        "shell": """\
drone-reel split \\
  -i fpv_footage.mp4 \\
  -o ./out/ \\
  --score-weights "motion=0.50,comp=0.10,color=0.15,sharp=0.10,bright=0.15" \\
  --hook-weights "subject=0.20,motion=0.45,color=0.15,comp=0.10,unique=0.10" \\
  --min-score 35 \\
  --shake-tolerance 60 \\
  --stab-strength light \\
  --color high_contrast \\
  --auto-speed \\
  --speed-correction-profile smooth
""",
        "demo_args": [
            "split",
            "-i", str(DEMO_MULTI),
            "-o", str(DEMO_OUTPUT_DIR / "r09_fpv/"),
            "--score-weights", "motion=0.50,comp=0.10,color=0.15,sharp=0.10,bright=0.15",
            "--min-score", "35",
            "--preview",
        ],
        "demo_note": "Demo runs --preview to keep it fast.",
    },
    {
        "id": "auto_color_match",
        "title": "10 — Color-Match Across Multiple Cameras",
        "description": (
            "When mixing clips from different drones or lighting conditions, "
            "`--auto-color-match` normalises exposure and colour using histogram "
            "matching before the grade is applied."
        ),
        "shell": """\
drone-reel create \\
  --input ./mixed_clips/ \\
  --output matched_reel.mp4 \\
  --auto-color-match \\
  --color cinematic \\
  --color-intensity 0.6 \\
  --reframe smart \\
  --duration 45 \\
  --platform instagram_reels
""",
        "demo_args": None,
    },
]

# ---------------------------------------------------------------------------
# Render recipes
# ---------------------------------------------------------------------------

for recipe in RECIPES:
    with st.expander(recipe["title"], expanded=False):
        st.markdown(recipe["description"])
        st.code(recipe["shell"], language="bash")

        demo_args = recipe.get("demo_args")
        demo_note = recipe.get("demo_note", "")

        if demo_args is None:
            st.info(
                "**Needs your footage** — no bundled sample clip suitable for this recipe. "
                "Copy the command above, adjust the paths, and run it in your terminal."
            )
        else:
            if demo_note:
                st.caption(demo_note)
            if st.button(f"Run on sample clip", key=f"btn_{recipe['id']}"):
                # Check if output already exists
                out_arg_idx = None
                for i, a in enumerate(demo_args):
                    if str(a).endswith(".mp4") and i > 0:
                        out_arg_idx = i
                        break

                with st.spinner(f"Running recipe '{recipe['title']}'…"):
                    result = run_drone_reel(
                        [str(a) for a in demo_args],  # includes subcommand as first element
                        timeout=180,
                        show_error=True,
                    )

                show_command_expander(result)

                if result.ok:
                    st.success(f"Completed in {result.elapsed:.1f}s")
                    # Show output video if it exists
                    for a in demo_args:
                        a_str = str(a)
                        if a_str.endswith(".mp4"):
                            p = Path(a_str)
                            if p.exists():
                                st.video(str(p))
                                break
                else:
                    with st.expander("stdout"):
                        st.code(result.stdout[:2000], language="text")


# ---------------------------------------------------------------------------
st.divider()
st.subheader("Mix and match flags")

st.markdown(
    """
    All the flags shown in the recipes are composable.  A production command might look like:

    ```bash
    drone-reel split -i source.mp4 -o ./out/ \\
      --input-colorspace dlog \\
      --color drone_aerial --color-intensity 0.7 \\
      --vignette 0.3 --halation 0.2 --letterbox 2.35 \\
      --stabilize --stab-strength adaptive --smooth-radius 40 \\
      --roll-correction 0.3 \\
      --auto-speed --speed-correction-profile cinematic --ease-speed-ramps \\
      --gimbal-bounce-recovery \\
      --min-score 50 --min-duration 3 --max-duration 10 \\
      --scene-threshold 22 --analysis-scale 0.5 \\
      --quality high --json
    ```

    See **Chapter 12** for the full searchable flag reference.
    """
)

page_footer("12_cli_reference.py", "CLI Reference")
