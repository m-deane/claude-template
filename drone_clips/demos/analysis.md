# Demo Video Analysis

## Test Suite

```
pytest -x --tb=short -q
1175 passed, 3 skipped, 6 warnings in 134.37s
Required test coverage of 70% reached. Total coverage: 77.81%
```

No regressions introduced by the demo workflow.

---

## Scene Analysis Results

`drone-reel analyze` run on each demo video. Note: the scene detector works on the final encoded output, so transitions and colour grading affect how scene boundaries are perceived. The letterbox demo scores lower because black bars reduce the measured sharpness/brightness metrics.

| Filename | Scenes | Score range | Avg score | File size | Notes |
|----------|--------|-------------|-----------|-----------|-------|
| `demo_baseline.mp4` | 2 | 61.6–62.2 | 61.9 | 24 MB | Reference output |
| `demo_drone_aerial.mp4` | 2 | 60.1–62.0 | 61.1 | 24 MB | Colour boost preserved scores |
| `demo_golden_hour.mp4` | 1 | 61.8 | 61.8 | 19 MB | Warm grade, scene merging |
| `demo_film_emulation.mp4` | 1 | 59.8 | 59.8 | 19 MB | Slight desaturation lowers score |
| `demo_vignette.mp4` | 1 | 55.1 | 55.1 | 19 MB | Dark border reduces avg brightness score |
| `demo_letterbox.mp4` | 1 | 40.5 | 40.5 | 13 MB | Black bars significantly cut sharpness metric |
| `demo_stabilized.mp4` | 1 | 59.5 | 59.5 | 19 MB | Stabilization crops frame slightly |
| `demo_viral.mp4` | 2 | 47.8–60.7 | 54.3 | 20 MB | Speed ramp transition detected as scene |
| `demo_long_30s.mp4` | 2 | 55.7–59.4 | 57.6 | 30 MB | 27s actual (source material limited) |
| `demo_caption.mp4` | 1 | 63.0 | 63.0 | 19 MB | Caption overlay slightly boosts perceived sharpness |

### Observations

- **Letterbox** drops the quality score the most (40.5 vs 61.9 baseline) — black bars are counted as dark/flat pixels
- **Caption** scores highest (63.0) — the text adds high-frequency edges that the sharpness metric rewards
- **Vignette** reduces score by ~6 points — the darkened border lowers mean brightness and colour variance
- **Stabilization** is nearly score-neutral (59.5 vs 61.9) — slight crop is the only effect
- **Long 30s** reaches 27s not 30s because the source clips total ~57s of material (not enough for 2.5× scaling)
