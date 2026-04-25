"""
Chapter 08 — Color Grading

Covers: 30 presets, --color-intensity, LUTs, vignette/halation/letterbox.
"""

from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="08 Color Grading", page_icon="", layout="wide")

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import (
    DEMO_OUTPUT_DIR,
    clip_selector,
    extract_thumb,
    run_drone_reel,
    show_command_expander,
    page_footer,
)

with st.sidebar:
    st.title("drone-reel Textbook")
    st.page_link("app.py", label="Home")
    st.page_link("pages/07_speed_correction.py", label="Prev: Speed Correction")
    st.page_link("pages/09_beat_sync.py", label="Next: Beat Sync")

# ---------------------------------------------------------------------------

st.title("Chapter 08 — Color Grading")

st.info(
    "**What you'll learn:** All 30 color presets and what they do, how `--color-intensity` "
    "blends the grade, how to supply a custom LUT, and the film-effect flags "
    "(vignette, halation, chromatic-aberration, letterbox)."
)

# ---------------------------------------------------------------------------
st.subheader("Preset catalogue")

presets = {
    "General": [
        "none", "cinematic", "warm_sunset", "cool_blue", "vintage",
        "high_contrast", "muted", "vibrant", "teal_orange", "black_white",
        "drone_aerial",
    ],
    "Time of day": [
        "golden_hour", "blue_hour", "harsh_midday", "overcast", "night_city",
    ],
    "Terrain": [
        "ocean_coastal", "forest_jungle", "urban_city", "desert_arid",
        "snow_mountain", "autumn_foliage",
    ],
    "Film emulation": [
        "kodak_2383", "fujifilm_3513", "technicolor_2strip",
    ],
    "Social-media trends": [
        "desaturated_moody", "warm_pastel", "cyberpunk_neon",
        "hyper_natural", "film_emulation",
    ],
}

preset_notes = {
    "none": "Raw — no grading applied",
    "cinematic": "Lifted blacks, slight teal shadows, warm highlights",
    "warm_sunset": "Orange push, boosted reds, -saturation blues",
    "cool_blue": "Cyan-teal grade, cooled highlights",
    "vintage": "Faded look, warm mids, reduced contrast",
    "high_contrast": "Crushed blacks, boosted contrast, punchy colour",
    "muted": "Desaturated, lifted blacks — Scandinavian moodiness",
    "vibrant": "Full saturation, punchy colours — social media pop",
    "teal_orange": "Hollywood blockbuster split-tone",
    "black_white": "Luminosity-weighted B&W conversion",
    "drone_aerial": "Optimised for overhead/perspective shots: sky blue, terrain warm",
    "golden_hour": "Amber/orange lift, boosted warmth — magic hour look",
    "blue_hour": "Blue-cyan grade, twilight atmosphere",
    "harsh_midday": "Neutral, high contrast, white sky handling",
    "overcast": "Flat but detailed — brings out texture in diffuse light",
    "night_city": "Boosted highlights, blue shadows, neon emphasis",
    "ocean_coastal": "Cyan water, warm sand, horizon contrast",
    "forest_jungle": "Green push, dark shadows, high clarity",
    "urban_city": "Cool neutrals, elevated contrast",
    "desert_arid": "Orange/red push, dust haze",
    "snow_mountain": "Cool whites, shadow detail",
    "autumn_foliage": "Orange/red/amber — leaf colour emphasis",
    "kodak_2383": "Warm film print emulation",
    "fujifilm_3513": "Slightly cooler, skin-tone faithful",
    "technicolor_2strip": "Complementary two-strip process — red/green split",
    "desaturated_moody": "Muted, lifted blacks — dark moody",
    "warm_pastel": "Soft pastel palette — warm fades",
    "cyberpunk_neon": "Neon highlights, dark teal/purple shadows",
    "hyper_natural": "Over-sharp, heavily saturated — nature doc style",
    "film_emulation": "Generic analogue film curve + grain",
}

for category, preset_list in presets.items():
    with st.expander(f"{category} ({len(preset_list)} presets)", expanded=(category == "General")):
        rows = []
        for p in preset_list:
            rows.append({"preset": p, "description": preset_notes.get(p, "")})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# ---------------------------------------------------------------------------
st.subheader("Interactive grade preview")

chosen_path = clip_selector("Select clip")
preset_flat = [p for plist in presets.values() for p in plist]
chosen_preset = st.selectbox("--color preset", preset_flat, index=preset_flat.index("drone_aerial"))
intensity = st.slider("--color-intensity", 0.0, 1.0, 0.8, 0.05)
vignette = st.slider("--vignette", 0.0, 1.0, 0.0, 0.05)
halation = st.slider("--halation", 0.0, 1.0, 0.0, 0.05)
letterbox = st.selectbox("--letterbox", ["off", "2.35", "1.85", "2.39"])

if st.button("Apply grade"):
    out_dir = DEMO_OUTPUT_DIR / "grade"
    out_dir.mkdir(parents=True, exist_ok=True)
    tag = f"{chosen_preset}_i{int(intensity*100)}_v{int(vignette*10)}_lb{letterbox}"
    out_path = out_dir / f"grade_{tag}_{chosen_path.stem}.mp4"

    if not out_path.exists():
        args = [
            "split",
            "-i", str(chosen_path),
            "-o", str(out_dir),
            "--color", chosen_preset,
            "--color-intensity", str(intensity),
            "--vignette", str(vignette),
            "--halation", str(halation),
            "--letterbox", letterbox,
            "--no-filter",
            "--count", "1",
            "--overwrite",
        ]
        with st.spinner("Rendering graded clip…"):
            result = run_drone_reel(args, timeout=180, show_error=True)
        show_command_expander(
            result,
            python_snippet=f"""drone-reel split -i input.mp4 -o ./out/ \\
  --color {chosen_preset} \\
  --color-intensity {intensity} \\
  --vignette {vignette} \\
  --halation {halation} \\
  --letterbox {letterbox}
""",
        )
        written = sorted(out_dir.glob("*.mp4"), key=lambda p: p.stat().st_mtime)
        if written and written[-1] != out_path:
            import shutil
            shutil.copy(written[-1], out_path)
    else:
        st.info("Using cached render.")

    col1, col2 = st.columns(2)
    with col1:
        st.video(str(chosen_path))
        st.caption("Original")
    if out_path.exists():
        with col2:
            st.video(str(out_path))
            st.caption(f"{chosen_preset} @ {intensity:.0%}")
    else:
        st.warning("Graded clip not found.")

# ---------------------------------------------------------------------------
st.subheader("Custom LUT (bring your own)")

st.markdown(
    """
    Supply a `.cube` 3D LUT file to apply professional grades from DaVinci Resolve,
    Lightroom, or other tools:

    ```bash
    drone-reel split -i footage.mp4 -o ./out/ \\
      --lut /path/to/my_grade.cube \\
      --color-intensity 0.7
    ```

    The LUT is applied **before** any preset.  Use `--color none` to apply only the LUT.
    `--color-intensity` controls the blend ratio between original and LUT output.
    """
)

st.file_uploader(
    "Upload a .cube LUT to preview (path shown — run CLI manually)",
    type=["cube"],
    help="This widget shows the file path; pass it to --lut in the shell command.",
)

# ---------------------------------------------------------------------------
st.subheader("Film effect parameters")

effects_df = pd.DataFrame(
    {
        "Flag": [
            "--vignette",
            "--halation",
            "--chromatic-aberration",
            "--letterbox",
            "--denoise",
            "--haze",
            "--gnd-sky",
        ],
        "Range": [
            "0.0–1.0",
            "0.0–1.0",
            "0.0–1.0",
            "off / 2.35 / 1.85 / 2.39",
            "0.0–1.0",
            "0.0–1.0",
            "0.0–1.0",
        ],
        "What it does": [
            "Edge darkening. 0.3=subtle, 0.6=cinematic, 1.0=heavy",
            "Warm glow around highlights — halation film effect. 0.3=subtle",
            "RGB fringing on high-contrast edges — analogue film look",
            "Black bars: 2.35:1 anamorphic, 1.85:1 flat, 2.39:1 scope",
            "Temporal noise reduction. 0.3=subtle, 0.8=strong",
            "Atmospheric haze / depth fog simulation",
            "Graduated ND darkening of sky region",
        ],
    }
)
st.dataframe(effects_df, use_container_width=True)

page_footer("09_beat_sync.py", "Beat Sync")
