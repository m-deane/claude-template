#!/usr/bin/env python3
"""
Production batch processor.

Renders every shoot-day directory to multiple output formats in parallel.
Includes pre-flight memory checks and per-render failure recovery.

Expected directory structure:
  ./shoots/
    2024-07-01/   ← one folder per shoot day
      *.mp4
    2024-07-08/
      *.mp4
  ./music/track.mp3

Outputs:
  ./output/2024-07-01/reel_1080p.mp4
  ./output/2024-07-01/reel_4k.mp4     (if --4k flag passed)
  ./output/2024-07-08/reel_1080p.mp4
  ...

Usage:
  python batch_processor.py ./shoots/ ./music/track.mp3
  python batch_processor.py ./shoots/ ./music/track.mp3 --4k --duration 45
"""

import sys
import argparse
import subprocess
import logging
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


def build_render_config(
    shoot_dir: Path,
    music: Path,
    output_dir: Path,
    resolution: str,
    quality: str,
    duration: float,
) -> dict:
    """Build a render task description."""
    return {
        "shoot_dir": shoot_dir,
        "music": music,
        "output": output_dir / shoot_dir.name / f"reel_{resolution}.mp4",
        "resolution": resolution,
        "quality": quality,
        "duration": duration,
    }


def render(config: dict) -> tuple[bool, str]:
    """
    Execute one render task. Returns (success, message).
    Runs in a subprocess so each render is memory-isolated.
    """
    output: Path = config["output"]
    output.parent.mkdir(parents=True, exist_ok=True)

    # Skip already-completed renders
    if output.exists() and output.stat().st_size > 1_000_000:
        return True, f"SKIP   {output.name} (already exists)"

    cmd = [
        "drone-reel", "create",
        "-i", str(config["shoot_dir"]),
        "-m", str(config["music"]),
        "-d", str(int(config["duration"])),
        "--platform", "instagram_reels",
        "--resolution", config["resolution"],
        "--quality", config["quality"],
        "-c", "drone_aerial",
        "--beat-mode", "downbeat",
        "--vignette", "0.30",
        "--halation", "0.20",
        "--gnd-sky", "0.30",
        "--stabilize",
        "-o", str(output),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=7200)

    if result.returncode == 0:
        size_mb = output.stat().st_size / 1_048_576 if output.exists() else 0
        return True, f"OK     {output.name}  ({size_mb:.0f} MB)"
    else:
        # Capture last 600 chars of stderr for diagnostics
        err = result.stderr[-600:].strip() if result.stderr else "(no stderr)"
        return False, f"FAIL   {output.name}\n       {err}"


def check_memory() -> float:
    """Return available system RAM in GB. Returns 999 if psutil not available."""
    try:
        import psutil
        return psutil.virtual_memory().available / 1_073_741_824
    except ImportError:
        return 999.0


def main():
    parser = argparse.ArgumentParser(description="Batch reel renderer")
    parser.add_argument("shoots_dir", type=Path, help="Root directory of shoot folders")
    parser.add_argument("music",      type=Path, help="Music file (.mp3, .wav)")
    parser.add_argument("--output",   type=Path, default=Path("./output"),
                        help="Output root directory (default: ./output)")
    parser.add_argument("--duration", type=float, default=30.0,
                        help="Target reel duration in seconds (default: 30)")
    parser.add_argument("--4k",       dest="render_4k", action="store_true",
                        help="Also render 4K ultra (adds ~1h per shoot day)")
    parser.add_argument("--workers",  type=int, default=2,
                        help="Parallel renders (default: 2; use 1 for 4K)")
    args = parser.parse_args()

    # ── Discover shoot days ──────────────────────────────────────────────
    shoot_dirs = sorted(d for d in args.shoots_dir.iterdir() if d.is_dir())
    if not shoot_dirs:
        log.error("No subdirectories found in %s", args.shoots_dir)
        sys.exit(1)

    log.info("Found %d shoot day(s): %s", len(shoot_dirs),
             ", ".join(d.name for d in shoot_dirs))

    # ── Memory pre-flight ────────────────────────────────────────────────
    available_gb = check_memory()
    log.info("Available RAM: %.1f GB", available_gb)
    if available_gb < 4.0:
        log.warning("Low memory (%.1f GB). Forcing --workers 1.", available_gb)
        args.workers = 1
    if args.render_4k and available_gb < 8.0:
        log.warning(
            "4K renders need ~1 GB each. With %.1f GB available, "
            "forcing --workers 1.", available_gb,
        )
        args.workers = 1

    # ── Build task list ──────────────────────────────────────────────────
    tasks: list[dict] = []
    for shoot in shoot_dirs:
        tasks.append(build_render_config(
            shoot, args.music, args.output, "1080p", "high", args.duration,
        ))
        if args.render_4k:
            tasks.append(build_render_config(
                shoot, args.music, args.output, "4k", "ultra", args.duration,
            ))

    log.info("Queued %d render task(s) across %d worker(s)", len(tasks), args.workers)

    # ── Execute ──────────────────────────────────────────────────────────
    failures: list[str] = []
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(render, task): task for task in tasks}
        for future in as_completed(futures):
            try:
                success, msg = future.result()
                if success:
                    log.info(msg)
                else:
                    log.error(msg)
                    failures.append(msg)
            except Exception as e:
                task = futures[future]
                msg = f"EXCEPTION  {task['output'].name}: {e}"
                log.exception(msg)
                failures.append(msg)

    # ── Summary ──────────────────────────────────────────────────────────
    completed = len(tasks) - len(failures)
    log.info("Completed %d / %d renders", completed, len(tasks))

    if failures:
        log.error("%d render(s) failed:", len(failures))
        for msg in failures:
            log.error("  %s", msg)
        sys.exit(1)


if __name__ == "__main__":
    main()
