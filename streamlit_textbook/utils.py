"""
Shared helpers for the drone-reel Streamlit textbook.

Provides subprocess wrappers, thumbnail extraction, clip probing,
and path constants used across all chapter pages.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import time
from pathlib import Path
from typing import Any

import streamlit as st

# ---------------------------------------------------------------------------
# Path constants
# ---------------------------------------------------------------------------

TEXTBOOK_DIR = Path(__file__).parent.resolve()
ASSETS_DIR = TEXTBOOK_DIR / "assets"
CACHE_DIR = TEXTBOOK_DIR / ".cache"
THUMB_DIR = CACHE_DIR / "thumbnails"
DEMO_OUTPUT_DIR = CACHE_DIR / "demo_outputs"

VENV_BIN = Path("/Volumes/LaCie/_p-ai-drone-video/.venv/bin")
DRONE_REEL_BIN = VENV_BIN / "drone-reel"
FFMPEG_BIN = "ffmpeg"
FFPROBE_BIN = "ffprobe"

# Create dirs on import
THUMB_DIR.mkdir(parents=True, exist_ok=True)
DEMO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Default clips bundled in assets/
DEFAULT_CLIPS: dict[str, Path] = {
    "Greenland aerial (short)": ASSETS_DIR / "clip_a.mp4",
    "Desert/coastal scene": ASSETS_DIR / "clip_b.mp4",
    "High-score scene": ASSETS_DIR / "clip_c.mp4",
}

MULTI_SCENE_CLIP = ASSETS_DIR / "multi_scene.mp4"


# ---------------------------------------------------------------------------
# Subprocess wrapper
# ---------------------------------------------------------------------------

class RunResult:
    """Structured result from a drone-reel subprocess call."""

    def __init__(
        self,
        args: list[str],
        returncode: int,
        stdout: str,
        stderr: str,
        elapsed: float,
    ) -> None:
        self.args = args
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        self.elapsed = elapsed
        self.ok = returncode == 0

    def command_str(self) -> str:
        """Return the shell command as a formatted string."""
        return " ".join(str(a) for a in self.args)


def run_drone_reel(
    args: list[str | Path],
    timeout: int = 300,
    show_error: bool = True,
) -> RunResult:
    """
    Run drone-reel with *args* and return a RunResult.

    Args:
        args: Arguments after the ``drone-reel`` binary (e.g. ``["split", "-i", path]``).
        timeout: Seconds before the process is killed (default 300).
        show_error: If True and the process fails, call ``st.error`` with the stderr.

    Returns:
        RunResult with stdout, stderr, returncode, elapsed.
    """
    full_args = [str(DRONE_REEL_BIN)] + [str(a) for a in args]
    t0 = time.perf_counter()
    try:
        proc = subprocess.run(
            full_args,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        result = RunResult(full_args, -1, "", f"Timed out after {timeout}s", time.perf_counter() - t0)
        if show_error:
            st.error(f"Command timed out after {timeout}s")
        return result
    except FileNotFoundError:
        msg = f"drone-reel binary not found at {DRONE_REEL_BIN}"
        result = RunResult(full_args, -1, "", msg, 0.0)
        if show_error:
            st.error(msg)
        return result

    elapsed = time.perf_counter() - t0
    result = RunResult(full_args, proc.returncode, proc.stdout, proc.stderr, elapsed)

    if not result.ok and show_error:
        st.error(f"drone-reel exited with code {proc.returncode}")
        with st.expander("stderr details"):
            st.code(proc.stderr or "(empty)", language="text")

    return result


# ---------------------------------------------------------------------------
# Thumbnail extractor
# ---------------------------------------------------------------------------

def _thumb_cache_key(video_path: Path, t_seconds: float) -> str:
    mtime = video_path.stat().st_mtime if video_path.exists() else 0
    raw = f"{video_path}|{mtime}|{t_seconds:.3f}"
    return hashlib.sha1(raw.encode()).hexdigest()


def extract_thumb(video_path: Path, t_seconds: float = 1.0) -> Path | None:
    """
    Extract a thumbnail at *t_seconds* from *video_path*.

    Caches results under ``.cache/thumbnails/`` keyed on (path, mtime, t).
    Uses ``ffmpeg -ss`` for fast seeking.

    Returns:
        Path to the JPEG thumbnail, or None on failure.
    """
    if not video_path.exists():
        return None

    key = _thumb_cache_key(video_path, t_seconds)
    out_path = THUMB_DIR / f"{key}.jpg"
    if out_path.exists():
        return out_path

    cmd = [
        FFMPEG_BIN,
        "-ss", str(t_seconds),
        "-i", str(video_path),
        "-vframes", "1",
        "-q:v", "3",
        "-y",
        str(out_path),
    ]
    try:
        subprocess.run(cmd, capture_output=True, timeout=30, check=False)
    except Exception:
        return None

    return out_path if out_path.exists() else None


# ---------------------------------------------------------------------------
# Video probe / metadata
# ---------------------------------------------------------------------------

@st.cache_data(show_spinner=False)
def probe_video(video_path_str: str) -> dict[str, Any]:
    """
    Return ffprobe metadata for *video_path_str* (JSON).

    Cached by Streamlit so repeated calls are instant.
    """
    cmd = [
        FFPROBE_BIN,
        "-v", "quiet",
        "-print_format", "json",
        "-show_streams",
        "-show_format",
        video_path_str,
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        return json.loads(proc.stdout) if proc.returncode == 0 else {}
    except Exception:
        return {}


def video_info(video_path: Path) -> dict[str, Any]:
    """Return a simplified dict of video properties."""
    raw = probe_video(str(video_path))
    info: dict[str, Any] = {"path": str(video_path), "exists": video_path.exists()}
    if not raw:
        return info

    fmt = raw.get("format", {})
    info["duration"] = float(fmt.get("duration", 0))
    info["size_mb"] = int(fmt.get("size", 0)) / 1_048_576
    info["bitrate_kbps"] = int(fmt.get("bit_rate", 0)) // 1000

    for stream in raw.get("streams", []):
        if stream.get("codec_type") == "video":
            info["width"] = stream.get("width", 0)
            info["height"] = stream.get("height", 0)
            info["codec"] = stream.get("codec_name", "")
            # Parse frame rate "30/1" or "30000/1001"
            r = stream.get("r_frame_rate", "0/1").split("/")
            try:
                info["fps"] = round(int(r[0]) / int(r[1]), 2)
            except (ZeroDivisionError, ValueError):
                info["fps"] = 0
            info["color_space"] = stream.get("color_space", "unknown")
            info["color_transfer"] = stream.get("color_transfer", "unknown")
            break

    return info


# ---------------------------------------------------------------------------
# drone-reel --help parser
# ---------------------------------------------------------------------------

@st.cache_data(show_spinner=False)
def parse_help(subcommand: str) -> list[dict[str, str]]:
    """
    Parse ``drone-reel <subcommand> --help`` into a list of option dicts.

    Each dict has keys: flag, type, default, description.
    """
    proc = subprocess.run(
        [str(DRONE_REEL_BIN), subcommand, "--help"],
        capture_output=True, text=True, timeout=15,
    )
    text = proc.stdout + proc.stderr
    rows: list[dict[str, str]] = []
    current_flags = ""
    current_lines: list[str] = []

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("-") or stripped.startswith("--"):
            if current_flags:
                rows.append(_parse_option_block(current_flags, current_lines))
            current_flags = stripped
            current_lines = []
        elif current_flags and stripped:
            current_lines.append(stripped)

    if current_flags:
        rows.append(_parse_option_block(current_flags, current_lines))

    return rows


def _parse_option_block(flags_line: str, desc_lines: list[str]) -> dict[str, str]:
    """Turn a raw option block into a structured dict."""
    description = " ".join(desc_lines)
    # Extract type hint if present in brackets like [0<=x<=100]
    type_hint = ""
    default = ""

    parts = flags_line.split()
    flag = parts[0] if parts else flags_line
    if len(parts) > 1:
        # e.g. "--scene-threshold FLOAT RANGE"
        type_hint = " ".join(parts[1:])

    # Try to find "(default: X)" in description
    if "default" in description.lower():
        import re
        m = re.search(r"default[:\s]+([^\s,)]+)", description, re.IGNORECASE)
        if m:
            default = m.group(1).rstrip(")")

    return {
        "flag": flag,
        "type": type_hint,
        "default": default,
        "description": description[:160],
    }


# ---------------------------------------------------------------------------
# Shared UI helpers
# ---------------------------------------------------------------------------

def show_command_expander(cmd: RunResult | list[str], python_snippet: str = "") -> None:
    """
    Render a 'Show the code' expander with the shell command and optional Python snippet.
    """
    with st.expander("Show the code", expanded=False):
        if isinstance(cmd, RunResult):
            st.code(cmd.command_str(), language="bash")
        else:
            st.code(" ".join(str(a) for a in cmd), language="bash")
        if python_snippet:
            st.code(python_snippet, language="python")


def clip_selector(label: str = "Choose a bundled clip") -> Path:
    """Render a selectbox for bundled clips and return the chosen Path."""
    names = list(DEFAULT_CLIPS.keys())
    choice = st.selectbox(label, names)
    return DEFAULT_CLIPS[choice]


def page_footer(next_page: str | None = None, next_label: str = "Next chapter") -> None:
    """Render a consistent footer with optional forward link."""
    st.divider()
    if next_page:
        st.page_link(f"pages/{next_page}", label=f"Try next: {next_label}")
