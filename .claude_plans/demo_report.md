# drone-reel `extract-clips` Feature Demo Report

**Date:** 2026-02-24
**Summary:** End-to-end demonstration of the `extract-clips` command — scene detection, score-ranked clip extraction with JSON manifest, and downstream reel creation from extracted clips.

---

## Overview

The `extract-clips` command analyzes raw drone footage, detects scene boundaries, scores each scene on visual quality (sharpness, color variance, brightness, motion), and exports the top N clips as individual MP4 files. It solves the "large raw footage" problem: instead of manually scrubbing through long recordings to find the best moments, the tool automatically identifies and extracts the highest-quality segments, ready to feed into `drone-reel create` or any other editor.

## Demo Environment

- **Source video:** Synthetic 40-second clip, 1920x1080, 30fps, 5 distinct scenes
- **Platform:** macOS Darwin 23.6.0
- **Tool version:** drone-reel (development install)

---

## Step-by-Step Results

### Step 1 — Analyze source video

Verify scene detection on the raw footage before extraction.

```bash
drone-reel analyze -i /tmp/drone_demo/raw_footage.mp4
```

```
 Scene │ Start │ End   │ Duration │ Score
 1     │ 00:00 │ 00:08 │ 8.0s     │ 33.3
 2     │ 00:08 │ 00:16 │ 8.0s     │ 33.2
 3     │ 00:16 │ 00:24 │ 8.0s     │ 32.7
 4     │ 00:24 │ 00:32 │ 8.0s     │ 27.8
 5     │ 00:32 │ 00:40 │ 8.0s     │ 38.8
Total scenes: 5
```

All 5 scenes detected with scores ranging from 27.8 to 38.8.

### Step 2 — Extract top 5 clips (score-sorted, with JSON manifest)

Extract the best clips ranked by quality score, outputting a machine-readable manifest.

```bash
drone-reel extract-clips -i /tmp/drone_demo/raw_footage.mp4 \
  -o /tmp/drone_demo/clips -n 5 --json --min-score 0
```

```
  Detected 5 scenes
  Passed filter: 5 scenes

  1/5  clip_001_s38.mp4   00:32-00:40  8.0s  score: 38
  2/5  clip_002_s33.mp4   00:00-00:08  8.0s  score: 33
  3/5  clip_003_s33.mp4   00:08-00:16  8.0s  score: 33
  4/5  clip_004_s32.mp4   00:16-00:24  8.0s  score: 32
  5/5  clip_005_s27.mp4   00:24-00:32  8.0s  score: 27

  Extracted 5 clips to /tmp/drone_demo/clips/ (total: 40.0s, 3.4 MB)
  Manifest written to /tmp/drone_demo/clips/manifest.json
```

Clips are numbered by rank (highest score first) with the score embedded in the filename for quick identification.

### Step 3 — List extracted clips

Verify the output directory contents.

```bash
ls -lh /tmp/drone_demo/clips/
```

```
-rw-r--r--  1.2M  clip_001_s38.mp4
-rw-r--r--  638K  clip_002_s33.mp4
-rw-r--r--  396K  clip_003_s33.mp4
-rw-r--r--  631K  clip_004_s32.mp4
-rw-r--r--  610K  clip_005_s27.mp4
-rw-r--r--  1.4K  manifest.json
```

Five clip files plus the JSON manifest, totaling 3.4 MB.

### Step 4 — Show manifest

Inspect the structured metadata produced by `--json`.

```bash
cat /tmp/drone_demo/clips/manifest.json
```

Full manifest content shown in the [manifest.json section below](#manifestjson).

### Step 5 — No-filter chronological extract

Extract all scenes in timeline order (no quality filtering, no score sorting).

```bash
drone-reel extract-clips -i /tmp/drone_demo/raw_footage.mp4 \
  -o /tmp/drone_demo/clips_all --no-filter --sort chronological --min-score 0
```

```
  1/5  clip_001_s33.mp4   00:00-00:08  8.0s  score: 33
  2/5  clip_002_s33.mp4   00:08-00:16  8.0s  score: 33
  3/5  clip_003_s32.mp4   00:16-00:24  8.0s  score: 32
  4/5  clip_004_s27.mp4   00:24-00:32  8.0s  score: 27
  5/5  clip_005_s38.mp4   00:32-00:40  8.0s  score: 38

  Extracted 5 clips to /tmp/drone_demo/clips_all/ (total: 40.0s, 3.4 MB)
```

Clips are now ordered by timeline position rather than score, useful for preserving narrative flow.

### Step 6 — List chronological clips

```bash
ls -lh /tmp/drone_demo/clips_all/
```

```
-rw-r--r--  638K  clip_001_s33.mp4
-rw-r--r--  396K  clip_002_s33.mp4
-rw-r--r--  631K  clip_003_s32.mp4
-rw-r--r--  610K  clip_004_s27.mp4
-rw-r--r--  1.2M  clip_005_s38.mp4
```

Same 5 clips, different ordering — the highest-scored clip (s38) is now last since it occurs at the end of the source video.

### Step 7 — Create reel from extracted clips

Feed the score-sorted clips into `drone-reel create` to produce a final reel.

```bash
drone-reel create -i /tmp/drone_demo/clips/ \
  -m /tmp/drone_demo/music.wav -o /tmp/drone_demo/reel.mp4 \
  --duration 15 --color drone_aerial --color-intensity 0.5
```

```
Found 5 video file(s)
Detected 5 scenes
Detected tempo: 120.0 BPM
Duration adjustment: Scaled clips by 1.50x -> 15s
Color grade: drone_aerial @ 50% intensity

  Reel created successfully!
  Output: /tmp/drone_demo/reel.mp4
  Duration: 00:15
  Resolution: 1080x1920
  Clips: 5
```

15-second vertical reel produced from the 5 extracted clips with drone_aerial color grading at 50% intensity.

### Step 8 — Verify reel

Confirm the output file and analyze its structure.

```bash
ls -lh /tmp/drone_demo/reel.mp4
drone-reel analyze -i /tmp/drone_demo/reel.mp4
```

```
-rw-r--r--  2.8M  /tmp/drone_demo/reel.mp4

 Scene │ Start │ End   │ Duration │ Score
 1     │ 00:00 │ 00:05 │ 5.4s     │ 34.8
 2     │ 00:05 │ 00:08 │ 2.7s     │ 31.2
 3     │ 00:08 │ 00:13 │ 5.6s     │ 31.2
Total scenes: 3
```

The final reel contains 3 detected scenes (transitions merged some adjacent clips), with a 2.8 MB file size suitable for social media upload.

---

## manifest.json

```json
{
  "version": 1,
  "source_files": [
    {
      "path": "/private/tmp/drone_demo/raw_footage.mp4",
      "name": "raw_footage.mp4"
    }
  ],
  "extraction_params": {
    "count": 5,
    "min_score": 0.0,
    "min_duration": 2.0,
    "max_duration": 10.0,
    "quality": "high",
    "resolution": "source",
    "sort": "score",
    "enhanced": false,
    "filtered": true
  },
  "clips": [
    {
      "filename": "clip_001_s38.mp4",
      "source_file": "raw_footage.mp4",
      "start_time": 32.0,
      "end_time": 40.0,
      "duration": 8.0,
      "score": 38.8
    },
    {
      "filename": "clip_002_s33.mp4",
      "source_file": "raw_footage.mp4",
      "start_time": 0.0,
      "end_time": 8.0,
      "duration": 8.0,
      "score": 33.3
    },
    {
      "filename": "clip_003_s33.mp4",
      "source_file": "raw_footage.mp4",
      "start_time": 8.0,
      "end_time": 16.0,
      "duration": 8.0,
      "score": 33.2
    },
    {
      "filename": "clip_004_s32.mp4",
      "source_file": "raw_footage.mp4",
      "start_time": 16.0,
      "end_time": 24.0,
      "duration": 8.0,
      "score": 32.7
    },
    {
      "filename": "clip_005_s27.mp4",
      "source_file": "raw_footage.mp4",
      "start_time": 24.0,
      "end_time": 32.0,
      "duration": 8.0,
      "score": 27.8
    }
  ],
  "summary": {
    "total_clips": 5,
    "total_duration": 40.0,
    "total_size_mb": 3.4,
    "avg_score": 33.2,
    "scenes_detected": 5,
    "scenes_filtered": 0
  }
}
```

---

## End-to-End Workflow Summary

The full raw-footage-to-reel workflow is two commands:

```bash
# Step 1: Extract the best clips from raw footage
drone-reel extract-clips -i raw_footage.mp4 -o ./clips -n 5 --json

# Step 2: Create a reel from the extracted clips
drone-reel create -i ./clips/ -m music.wav -o reel.mp4 --duration 15
```

**Step 1** detects scenes, scores them, extracts the top N as individual files, and writes a JSON manifest with metadata (scores, timestamps, extraction parameters).

**Step 2** takes the clip directory as input and produces a vertical reel with beat-synced transitions, color grading, and platform-optimized encoding.

---

## Verified Outputs

| File | Size |
|------|------|
| `raw_footage.mp4` (source) | 40s, 1920x1080 |
| `clips/clip_001_s38.mp4` | 1.2 MB |
| `clips/clip_002_s33.mp4` | 638 KB |
| `clips/clip_003_s33.mp4` | 396 KB |
| `clips/clip_004_s32.mp4` | 631 KB |
| `clips/clip_005_s27.mp4` | 610 KB |
| `clips/manifest.json` | 1.4 KB |
| `reel.mp4` (final output) | 2.8 MB, 15s, 1080x1920 |

---

## Conclusion

The `extract-clips` feature works end-to-end: raw footage is analyzed, scenes are detected and scored, the best clips are extracted as individual files with a structured JSON manifest, and those clips feed directly into `drone-reel create` to produce a finished reel. All 8 demo steps completed successfully with no errors.
