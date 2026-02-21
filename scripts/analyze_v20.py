#!/usr/bin/env python3
"""
V20 Reel Frame-by-Frame Quality Analysis

Performs comprehensive analysis:
1. Motion Energy Score using optical flow
2. Sharpness Score using Laplacian variance
3. Quality timeline across video duration
4. Comparison to V19 baseline
"""

import cv2
import numpy as np
import json
from pathlib import Path
from datetime import datetime

# Configuration
VIDEO_PATH = "/Users/matthewdeane/Documents/Data Science/python/_projects/_p-ai-drone-video/output/instagram_reel_v20.mp4"
OUTPUT_DIR = Path("/Users/matthewdeane/Documents/Data Science/python/_projects/_p-ai-drone-video/.claude/frame_analysis/v20")
SAMPLE_INTERVAL = 0.5  # seconds between samples

# V19 Baseline for comparison
V19_BASELINE = {
    "motion_score": 45,
    "sharpness_score": 48,
    "slow_static_pct": 62.5,
    "blurry_pct": 44.7,
    "overall_score": 70
}


def analyze_video():
    """Main analysis function."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print(f"ERROR: Cannot open video: {VIDEO_PATH}")
        return

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = frame_count / fps

    print("=" * 80)
    print("V20 INSTAGRAM REEL ANALYSIS")
    print("=" * 80)
    print(f"\nVideo: {VIDEO_PATH}")
    print(f"Duration: {duration:.2f}s | Resolution: {width}x{height} | FPS: {fps:.2f}")
    print(f"Total Frames: {frame_count}")
    print(f"Sample Interval: {SAMPLE_INTERVAL}s")
    print()

    # Calculate sample frames
    sample_times = np.arange(0, duration, SAMPLE_INTERVAL)
    sample_frames = [int(t * fps) for t in sample_times]

    print(f"Analyzing {len(sample_frames)} sample points...")
    print("-" * 80)

    # Storage for metrics
    motion_scores = []
    sharpness_scores = []
    brightness_values = []
    timeline_data = []

    prev_gray = None

    for i, frame_num in enumerate(sample_frames):
        time_s = sample_times[i]
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = cap.read()

        if not ret:
            print(f"  [{time_s:.1f}s] Frame {frame_num}: READ ERROR")
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 1. SHARPNESS: Laplacian variance
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        sharpness = laplacian.var()
        sharpness_scores.append(sharpness)

        # 2. MOTION: Optical flow (Farneback)
        motion_magnitude = 0
        if prev_gray is not None:
            flow = cv2.calcOpticalFlowFarneback(
                prev_gray, gray, None,
                pyr_scale=0.5, levels=3, winsize=15,
                iterations=3, poly_n=5, poly_sigma=1.2, flags=0
            )
            magnitude, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
            motion_magnitude = np.mean(magnitude)

        motion_scores.append(motion_magnitude)
        prev_gray = gray.copy()

        # 3. BRIGHTNESS
        brightness = np.mean(gray)
        brightness_values.append(brightness)

        # Categorize
        if motion_magnitude > 2.0:
            motion_cat = "HIGH"
        elif motion_magnitude > 1.0:
            motion_cat = "MEDIUM"
        else:
            motion_cat = "LOW"

        sharpness_cat = "SHARP" if sharpness >= 40 else "BLURRY"

        timeline_data.append({
            "time": round(time_s, 2),
            "frame": frame_num,
            "motion": round(motion_magnitude, 3),
            "motion_cat": motion_cat,
            "sharpness": round(sharpness, 2),
            "sharpness_cat": sharpness_cat,
            "brightness": round(brightness, 2)
        })

        # Save sample frame
        frame_path = OUTPUT_DIR / f"frame_{time_s:.1f}s.jpg"
        cv2.imwrite(str(frame_path), frame, [cv2.IMWRITE_JPEG_QUALITY, 90])

        print(f"  [{time_s:5.1f}s] Motion: {motion_magnitude:6.3f} ({motion_cat:6s}) | "
              f"Sharpness: {sharpness:8.2f} ({sharpness_cat:6s}) | Brightness: {brightness:6.2f}")

    cap.release()

    # Calculate summary statistics
    motion_scores_valid = [m for m in motion_scores if m > 0]  # Exclude first frame (no previous)

    if motion_scores_valid:
        avg_motion = np.mean(motion_scores_valid)
        max_motion = np.max(motion_scores_valid)
        min_motion = np.min(motion_scores_valid)
    else:
        avg_motion = max_motion = min_motion = 0

    avg_sharpness = np.mean(sharpness_scores)
    max_sharpness = np.max(sharpness_scores)
    min_sharpness = np.min(sharpness_scores)

    # Motion categorization percentages
    high_motion = sum(1 for d in timeline_data if d["motion_cat"] == "HIGH")
    med_motion = sum(1 for d in timeline_data if d["motion_cat"] == "MEDIUM")
    low_motion = sum(1 for d in timeline_data if d["motion_cat"] == "LOW")
    total_samples = len(timeline_data)

    high_motion_pct = (high_motion / total_samples) * 100 if total_samples else 0
    med_motion_pct = (med_motion / total_samples) * 100 if total_samples else 0
    low_motion_pct = (low_motion / total_samples) * 100 if total_samples else 0
    slow_static_pct = low_motion_pct  # LOW = slow/static

    # Sharpness categorization
    blurry_count = sum(1 for d in timeline_data if d["sharpness_cat"] == "BLURRY")
    sharp_count = sum(1 for d in timeline_data if d["sharpness_cat"] == "SHARP")
    blurry_pct = (blurry_count / total_samples) * 100 if total_samples else 0
    sharp_pct = (sharp_count / total_samples) * 100 if total_samples else 0

    # Normalize to 0-100 scores
    # Motion: scale based on typical drone footage ranges (0-5 pixels/frame movement)
    motion_score_100 = min(100, (avg_motion / 3.0) * 100)

    # Sharpness: typical Laplacian variance ranges 0-500+ for sharp, <40 blurry
    sharpness_score_100 = min(100, (avg_sharpness / 200) * 100)

    print()
    print("=" * 80)
    print("ANALYSIS RESULTS")
    print("=" * 80)

    print(f"\n1. MOTION ENERGY ANALYSIS")
    print("-" * 40)
    print(f"   Average Motion:    {avg_motion:.3f} pixels/frame")
    print(f"   Max Motion:        {max_motion:.3f}")
    print(f"   Min Motion:        {min_motion:.3f}")
    print(f"   Motion Score:      {motion_score_100:.1f}/100")
    print()
    print(f"   Motion Distribution:")
    print(f"     HIGH (>2.0):     {high_motion:3d} frames ({high_motion_pct:5.1f}%)")
    print(f"     MEDIUM (1.0-2.0):{med_motion:3d} frames ({med_motion_pct:5.1f}%)")
    print(f"     LOW (<1.0):      {low_motion:3d} frames ({low_motion_pct:5.1f}%) [static/slow]")

    print(f"\n2. SHARPNESS ANALYSIS")
    print("-" * 40)
    print(f"   Average Sharpness: {avg_sharpness:.2f} (Laplacian variance)")
    print(f"   Max Sharpness:     {max_sharpness:.2f}")
    print(f"   Min Sharpness:     {min_sharpness:.2f}")
    print(f"   Sharpness Score:   {sharpness_score_100:.1f}/100")
    print()
    print(f"   Sharpness Distribution:")
    print(f"     SHARP (>=40):    {sharp_count:3d} frames ({sharp_pct:5.1f}%)")
    print(f"     BLURRY (<40):    {blurry_count:3d} frames ({blurry_pct:5.1f}%)")

    print(f"\n3. QUALITY TIMELINE")
    print("-" * 40)
    print(f"   Timeline shows quality distribution across {duration:.2f}s video:")
    print()

    # Group by sections
    section_size = 5  # seconds
    sections = []
    for start in np.arange(0, duration, section_size):
        end = min(start + section_size, duration)
        section_data = [d for d in timeline_data if start <= d["time"] < end]
        if section_data:
            sect_motion_avg = np.mean([d["motion"] for d in section_data])
            sect_sharpness_avg = np.mean([d["sharpness"] for d in section_data])
            sect_blurry = sum(1 for d in section_data if d["sharpness_cat"] == "BLURRY")
            sect_static = sum(1 for d in section_data if d["motion_cat"] == "LOW")
            sections.append({
                "start": start,
                "end": end,
                "motion_avg": sect_motion_avg,
                "sharpness_avg": sect_sharpness_avg,
                "blurry_count": sect_blurry,
                "static_count": sect_static,
                "sample_count": len(section_data)
            })

            quality_bar = ""
            # Motion bar
            motion_level = min(10, int(sect_motion_avg * 5))
            sharpness_level = min(10, int(sect_sharpness_avg / 50))

            print(f"   [{start:5.1f}s-{end:5.1f}s] Motion: {'#' * motion_level:10s} ({sect_motion_avg:.2f}) | "
                  f"Sharpness: {'#' * sharpness_level:10s} ({sect_sharpness_avg:.1f})")

    # Identify quality drops
    print(f"\n   Quality Drops Detected:")
    quality_drops = []
    for d in timeline_data:
        if d["sharpness"] < 30 or (d["motion"] < 0.5 and d["time"] > 1):
            quality_drops.append(d)
            issue = []
            if d["sharpness"] < 30:
                issue.append(f"low sharpness ({d['sharpness']:.1f})")
            if d["motion"] < 0.5:
                issue.append(f"static ({d['motion']:.2f})")
            print(f"     - {d['time']:.1f}s: {', '.join(issue)}")

    if not quality_drops:
        print(f"     None detected!")

    print()
    print("=" * 80)
    print("COMPARISON TO V19 BASELINE")
    print("=" * 80)

    motion_change = motion_score_100 - V19_BASELINE["motion_score"]
    sharpness_change = sharpness_score_100 - V19_BASELINE["sharpness_score"]
    slow_static_change = slow_static_pct - V19_BASELINE["slow_static_pct"]
    blurry_change = blurry_pct - V19_BASELINE["blurry_pct"]

    def format_change(val):
        if val > 0:
            return f"+{val:.1f}"
        return f"{val:.1f}"

    print(f"\n   Metric                    V19        V20        Change")
    print(f"   {'-' * 55}")
    print(f"   Motion Score (0-100)      {V19_BASELINE['motion_score']:5.1f}      {motion_score_100:5.1f}      {format_change(motion_change):>6s} {'IMPROVED' if motion_change > 0 else 'DECLINED' if motion_change < 0 else 'SAME'}")
    print(f"   Sharpness Score (0-100)   {V19_BASELINE['sharpness_score']:5.1f}      {sharpness_score_100:5.1f}      {format_change(sharpness_change):>6s} {'IMPROVED' if sharpness_change > 0 else 'DECLINED' if sharpness_change < 0 else 'SAME'}")
    print(f"   Slow/Static Frames (%)    {V19_BASELINE['slow_static_pct']:5.1f}      {slow_static_pct:5.1f}      {format_change(-slow_static_change):>6s} {'IMPROVED' if slow_static_change < 0 else 'DECLINED' if slow_static_change > 0 else 'SAME'}")
    print(f"   Blurry Frames (%)         {V19_BASELINE['blurry_pct']:5.1f}      {blurry_pct:5.1f}      {format_change(-blurry_change):>6s} {'IMPROVED' if blurry_change < 0 else 'DECLINED' if blurry_change > 0 else 'SAME'}")

    # Calculate overall improvement
    motion_improvement = (motion_score_100 - V19_BASELINE["motion_score"]) / V19_BASELINE["motion_score"] * 100 if V19_BASELINE["motion_score"] > 0 else 0
    sharpness_improvement = (sharpness_score_100 - V19_BASELINE["sharpness_score"]) / V19_BASELINE["sharpness_score"] * 100 if V19_BASELINE["sharpness_score"] > 0 else 0

    print()
    print(f"   Relative Improvements:")
    print(f"     Motion:    {motion_improvement:+.1f}% {'(better)' if motion_improvement > 0 else '(worse)' if motion_improvement < 0 else ''}")
    print(f"     Sharpness: {sharpness_improvement:+.1f}% {'(better)' if sharpness_improvement > 0 else '(worse)' if sharpness_improvement < 0 else ''}")

    # Estimate overall score
    # Weighted: sharpness 35%, motion 30%, pacing/variety carry from V19 35%
    estimated_overall = (sharpness_score_100 * 0.35 + motion_score_100 * 0.30 + 76 * 0.35)  # 76 is V19's visual variety + pacing average
    estimated_change = estimated_overall - V19_BASELINE["overall_score"]

    print()
    print("=" * 80)
    print("ESTIMATED V20 OVERALL SCORE")
    print("=" * 80)
    print(f"\n   V19 Overall:      {V19_BASELINE['overall_score']}/100")
    print(f"   V20 Estimated:    {estimated_overall:.1f}/100")
    print(f"   Change:           {format_change(estimated_change)}")

    if estimated_change > 5:
        verdict = "SIGNIFICANT IMPROVEMENT"
    elif estimated_change > 0:
        verdict = "MINOR IMPROVEMENT"
    elif estimated_change == 0:
        verdict = "NO CHANGE"
    elif estimated_change > -5:
        verdict = "MINOR REGRESSION"
    else:
        verdict = "SIGNIFICANT REGRESSION"

    print(f"   Verdict:          {verdict}")

    print()
    print("=" * 80)

    # Save results to JSON
    # Convert numpy floats for JSON serialization
    def to_native(obj):
        if isinstance(obj, (np.floating, np.integer)):
            return float(obj)
        elif isinstance(obj, dict):
            return {k: to_native(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [to_native(x) for x in obj]
        return obj

    results = {
        "video": VIDEO_PATH,
        "analyzed_at": datetime.now().isoformat(),
        "video_info": {
            "duration": float(duration),
            "resolution": f"{width}x{height}",
            "fps": float(fps),
            "total_frames": int(frame_count)
        },
        "motion_analysis": {
            "score": float(round(motion_score_100, 1)),
            "average": float(round(avg_motion, 3)),
            "max": float(round(max_motion, 3)),
            "min": float(round(min_motion, 3)),
            "high_pct": float(round(high_motion_pct, 1)),
            "medium_pct": float(round(med_motion_pct, 1)),
            "low_pct": float(round(low_motion_pct, 1))
        },
        "sharpness_analysis": {
            "score": float(round(sharpness_score_100, 1)),
            "average": float(round(avg_sharpness, 2)),
            "max": float(round(max_sharpness, 2)),
            "min": float(round(min_sharpness, 2)),
            "sharp_pct": float(round(sharp_pct, 1)),
            "blurry_pct": float(round(blurry_pct, 1))
        },
        "v19_comparison": {
            "motion_change": float(round(motion_change, 1)),
            "sharpness_change": float(round(sharpness_change, 1)),
            "estimated_overall": float(round(estimated_overall, 1)),
            "overall_change": float(round(estimated_change, 1))
        },
        "timeline": to_native(timeline_data),
        "sections": to_native(sections)
    }

    results_path = OUTPUT_DIR / "v20_analysis.json"
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: {results_path}")
    print(f"Sample frames saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    analyze_video()
