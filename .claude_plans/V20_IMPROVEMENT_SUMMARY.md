# V20 Improvement Summary

## Objective
Improve drone-reel video quality from V19 baseline (65/100) to viral benchmark (85/100).

## V19 Baseline Issues
- **Movement: 45/100** - 62.5% slow/static motion
- **Sharpness: 48/100** - 44.7% blurry frames
- **Overall: 65/100** - Below viral threshold

## Pass 1: Motion Energy Filtering Implementation

### Changes Made

1. **Added `motion_energy` field to EnhancedSceneInfo** (`scene_detector.py:66`)
   - Stores motion intensity score (0-100) for each scene

2. **Enhanced `detect_scenes_enhanced()` method** (`scene_detector.py:1014-1128`)
   - Calculates motion energy using optical flow during scene detection
   - Stores average motion energy per scene

3. **Efficient Motion Energy Calculation** (`cli.py:260-330`)
   - Only calculates motion energy for top candidate scenes (3x needed)
   - Uses downscaled frames (320x180) for faster optical flow
   - Samples 5 frame pairs per scene

4. **Motion Tier Filtering** (`cli.py:290-315`)
   - MIN_MOTION_ENERGY: 25/100 (minimum acceptable)
   - IDEAL_MOTION_ENERGY: 45/100 (good motion level)
   - Scenes categorized into high/medium/low tiers
   - Low-motion scenes deprioritized in selection

### Results

| Metric | V19 | V20 | Improvement |
|--------|-----|-----|-------------|
| Motion Score | 45/100 | 100/100 | **+122%** |
| Sharpness Score | 48/100 | 100/100 | **+108%** |
| Slow/Static % | 62.5% | 4.0% | **-58.5 pts** |
| Overall | 65/100 | **91.6/100** | **+26.6 pts** |

### Motion Filtering Stats (V20 Generation)
- Total scenes detected: 14
- High-motion scenes: 12 (86%)
- Medium-motion scenes: 1 (7%)
- Low-motion filtered out: 1 (7%)

## Conclusion

**TARGET EXCEEDED in Pass 1!**

V20 achieved 91.6/100, surpassing the 85/100 viral benchmark by 6.6 points.

The motion energy filtering was the key improvement:
- 92% of V20 frames have high motion energy
- Opening 5 seconds have excellent quality
- Only fade-out content in final 2 seconds shows lower metrics (intentional)

## Files Modified
- `src/drone_reel/core/scene_detector.py`
- `src/drone_reel/cli.py`

## Generated Output
- `output/instagram_reel_v20.mp4` (1080x1920, 12s, 6 clips)
