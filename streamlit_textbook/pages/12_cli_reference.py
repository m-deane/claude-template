"""
Chapter 12 — CLI Reference

Auto-generated from `drone-reel split --help` and `drone-reel create --help`.
Re-parsed on each app start so it stays in sync with the library.
Rendered as a sortable, filterable dataframe.
"""

import re
import subprocess
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="12 CLI Reference", page_icon="", layout="wide")

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import DRONE_REEL_BIN, page_footer

with st.sidebar:
    st.title("drone-reel Textbook")
    st.page_link("app.py", label="Home")
    st.page_link("pages/11_recipes.py", label="Prev: Recipes")

# ---------------------------------------------------------------------------

st.title("Chapter 12 — CLI Reference")

st.info(
    "**What you'll learn:** Every flag for `create` and `split`, auto-parsed from "
    "`--help` output so this table always reflects the installed version."
)

# ---------------------------------------------------------------------------


@st.cache_data(show_spinner="Parsing CLI help…")
def load_all_flags() -> dict[str, pd.DataFrame]:
    """Load and parse --help for create and split commands."""
    results = {}
    for cmd in ["create", "split", "extract-clips", "analyze"]:
        proc = subprocess.run(
            [str(DRONE_REEL_BIN), cmd, "--help"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        text = proc.stdout + proc.stderr
        rows = _parse_help_text(text, cmd)
        if rows:
            results[cmd] = pd.DataFrame(rows)
    return results


def _parse_help_text(text: str, cmd: str) -> list[dict]:
    """Parse --help output into structured rows."""
    rows = []

    # Split into option blocks (each starts with whitespace + "-")
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        # Option lines start with "-"
        if stripped.startswith("-"):
            # Collect flags and type from this line
            flags_line = stripped
            # Collect description from following indented lines
            desc_parts = []
            i += 1
            while i < len(lines):
                next_line = lines[i]
                next_stripped = next_line.strip()
                # Stop if blank or next option
                if not next_stripped or next_stripped.startswith("-"):
                    break
                desc_parts.append(next_stripped)
                i += 1

            description = " ".join(desc_parts)
            row = _extract_option(flags_line, description, cmd)
            if row:
                rows.append(row)
        else:
            i += 1

    return rows


def _extract_option(flags_line: str, description: str, cmd: str) -> dict | None:
    """Turn a raw option line + description into a structured dict."""
    # flags_line example: "-i, --input PATH  Input directory..."
    # Split off inline description (if on same line)
    # Everything up to 2+ spaces = flags+type, after = inline desc
    parts = re.split(r"\s{2,}", flags_line, maxsplit=1)
    flags_part = parts[0].strip()
    inline_desc = parts[1].strip() if len(parts) > 1 else ""
    full_desc = (inline_desc + " " + description).strip()

    # Extract individual flags
    tokens = flags_part.split()
    long_flag = ""
    short_flag = ""
    type_hint = ""

    for tok in tokens:
        tok_clean = tok.rstrip(",")
        if tok_clean.startswith("--"):
            long_flag = tok_clean
        elif tok_clean.startswith("-") and len(tok_clean) <= 3:
            short_flag = tok_clean
        elif not tok_clean.startswith("-"):
            type_hint = tok_clean

    if not long_flag and not short_flag:
        return None

    # Extract default from description
    default = ""
    m = re.search(r"default[:\s]+([^\s,)\]]+)", full_desc, re.IGNORECASE)
    if m:
        default = m.group(1).rstrip(").")

    # Extract range from description e.g. "[0<=x<=100]"
    range_str = ""
    m2 = re.search(r"\[([^\]]+)\]", full_desc)
    if m2:
        range_str = m2.group(1)

    # Chapter cross-reference
    chapter = _infer_chapter(long_flag or short_flag)

    return {
        "command": cmd,
        "flag": long_flag or short_flag,
        "short": short_flag,
        "type": type_hint,
        "range": range_str,
        "default": default,
        "description": full_desc[:200],
        "chapter": chapter,
    }


def _infer_chapter(flag: str) -> str:
    """Map a flag to its primary textbook chapter."""
    mapping = {
        "--color": "08 Color Grading",
        "--color-intensity": "08 Color Grading",
        "--vignette": "08 Color Grading",
        "--halation": "08 Color Grading",
        "--lut": "08 Color Grading",
        "--letterbox": "08 Color Grading",
        "--chromatic-aberration": "08 Color Grading",
        "--denoise": "08 Color Grading",
        "--haze": "08 Color Grading",
        "--gnd-sky": "08 Color Grading",
        "--input-colorspace": "02 Drone Footage",
        "--reframe": "05 Reframing",
        "--ken-burns": "05 Reframing",
        "--kb-zoom-end": "05 Reframing",
        "--kb-pan-x": "05 Reframing",
        "--kb-pan-y": "05 Reframing",
        "--stabilize": "06 Stabilization",
        "--stab-strength": "06 Stabilization",
        "--smooth-radius": "06 Stabilization",
        "--border-crop": "06 Stabilization",
        "--max-corners": "06 Stabilization",
        "--roll-correction": "06 Stabilization",
        "--gimbal-bounce-recovery": "06 Stabilization",
        "--auto-speed": "07 Speed Correction",
        "--speed-correction-profile": "07 Speed Correction",
        "--pan-speed-high": "07 Speed Correction",
        "--pan-speed-mid": "07 Speed Correction",
        "--tilt-speed": "07 Speed Correction",
        "--fpv-speed": "07 Speed Correction",
        "--ease-speed-ramps": "07 Speed Correction",
        "--correct-orbit": "07 Speed Correction",
        "--vertical-drift-damping": "07 Speed Correction",
        "--scene-threshold": "03 Scene Detection",
        "--analysis-scale": "03 Scene Detection",
        "--motion-energy-method": "03 Scene Detection",
        "--flow-winsize": "03 Scene Detection",
        "--flow-levels": "03 Scene Detection",
        "--score-weights": "04 Scoring",
        "--hook-weights": "04 Scoring",
        "--hook-thresholds": "04 Scoring",
        "--min-score": "04 Scoring",
        "--beat-mode": "09 Beat Sync",
        "--music": "09 Beat Sync",
        "--quality": "10 Encoding",
        "--resolution": "10 Encoding",
        "--platform": "10 Encoding",
        "--aspect": "10 Encoding",
        "--transition": "01 Welcome",
        "--viral": "01 Welcome",
    }
    for key, chapter in mapping.items():
        if flag == key or flag.startswith(key):
            return chapter
    return "General"


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------

all_flags = load_all_flags()

if not all_flags:
    st.error("Could not load CLI help. Is drone-reel installed and on the PATH in the venv?")
    st.stop()

# Command selector
available_cmds = list(all_flags.keys())
selected_cmd = st.selectbox("Command", available_cmds, index=0)

df = all_flags[selected_cmd].copy()

# Search / filter
col1, col2, col3 = st.columns(3)
with col1:
    search_term = st.text_input("Search flags or descriptions", "")
with col2:
    chapters = ["All"] + sorted(df["chapter"].unique().tolist())
    chapter_filter = st.selectbox("Filter by chapter", chapters)
with col3:
    sort_col = st.selectbox("Sort by", ["flag", "chapter", "type"])

# Apply filters
if search_term:
    mask = (
        df["flag"].str.contains(search_term, case=False, na=False)
        | df["description"].str.contains(search_term, case=False, na=False)
    )
    df = df[mask]

if chapter_filter != "All":
    df = df[df["chapter"] == chapter_filter]

df = df.sort_values(sort_col).reset_index(drop=True)

st.markdown(f"Showing **{len(df)}** flags for `drone-reel {selected_cmd}`")

# Render table
display_cols = ["flag", "short", "type", "range", "default", "chapter", "description"]
display_cols = [c for c in display_cols if c in df.columns]
st.dataframe(
    df[display_cols],
    use_container_width=True,
    height=600,
    column_config={
        "flag": st.column_config.TextColumn("Flag", width="medium"),
        "short": st.column_config.TextColumn("Short", width="small"),
        "type": st.column_config.TextColumn("Type", width="small"),
        "range": st.column_config.TextColumn("Range", width="medium"),
        "default": st.column_config.TextColumn("Default", width="small"),
        "chapter": st.column_config.TextColumn("Chapter", width="medium"),
        "description": st.column_config.TextColumn("Description", width="large"),
    },
)

# ---------------------------------------------------------------------------
st.subheader("Raw --help output")

with st.expander(f"View raw `drone-reel {selected_cmd} --help`", expanded=False):
    proc = subprocess.run(
        [str(DRONE_REEL_BIN), selected_cmd, "--help"],
        capture_output=True, text=True, timeout=15,
    )
    st.code(proc.stdout + proc.stderr, language="text")

# ---------------------------------------------------------------------------
st.subheader("Common flag combinations")

st.code(
    """# Minimal split
drone-reel split -i source.mp4 -o ./out/

# Full post-processing split
drone-reel split -i source.mp4 -o ./out/ \\
  --color drone_aerial --color-intensity 0.7 --vignette 0.3 --letterbox 2.35 \\
  --stabilize --auto-speed --speed-correction-profile cinematic \\
  --min-score 45 --min-duration 3 --max-duration 12 \\
  --json

# Viral reel
drone-reel create -i ./clips/ -o reel.mp4 \\
  --viral --color teal_orange --music track.mp3

# Platform-specific
drone-reel create -i ./clips/ -o reel.mp4 \\
  --platform youtube_shorts --duration 60 --quality high
""",
    language="bash",
)

page_footer(None)
