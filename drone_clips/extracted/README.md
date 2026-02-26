# extract-clips Demo Variants

All variants use `snowdonia.webm` (75s, 1920×1080, 18 scenes) as the primary source unless noted.

## Results

| Variant | Key flags | Clips | Total duration | What it demonstrates |
|---------|-----------|-------|---------------|----------------------|
| `top3_scored/` | `-n 3 --min-score 60 --json` | 3 | 8.3s | Default behaviour — quality filtering + score ranking. Only clips scoring ≥60 are kept; highest score first. Includes `manifest.json`. |
| `chronological/` | `-n 5 --no-filter --sort chronological --min-score 0` | 5 | 26.7s | Preserve narrative order — all scenes included, ordered by timeline position rather than score. Useful when the sequence matters more than peak quality. |
| `short_clips/` | `-n 5 --max-duration 4 --min-score 0` | 5 | 16.1s | Duration filtering — caps each clip at 4 seconds. Ideal for fast-paced edits or platforms that reward quick cuts. |
| `germia/` | `-i germia_pool.webm -n 3 --json --min-score 60` | 3 | 28.5s | Multi-source — running on a different landscape (Germia Pool, Kosovo). Scores consistently 68–70 due to high-quality footage. |
| `greenland/` | `-i greenland_summit.webm -n 3 --json --min-score 30` | 3 | 23.8s | Low-score source — Greenland summit footage scores 42–44 (hazy/flat light). Lowering `--min-score` to 30 allows extraction where default filtering would over-restrict. |

## Choosing the Right Approach

**Score-sorted (default)** — best for highlight reels where you want only the visually strongest moments. Set `--min-score` higher (60–70) for strict curation, lower (30–40) for hazy or night footage.

**Chronological** — best for documentary-style edits where narrative flow matters. Use `--no-filter --sort chronological` to preserve the original timeline. Combine with `--min-score 0` to include everything.

**Duration-filtered** — best for short-form social content. Use `--max-duration 4` to enforce tight cuts; combine with `--min-duration 1.5` to skip very brief flashes.

**Multi-source** — run `extract-clips` separately on each source video, then feed all output directories into `drone-reel create -i` to build a reel from the best moments across locations.
