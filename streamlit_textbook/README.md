# drone-reel Interactive Textbook

A multi-page Streamlit app that teaches drone-video-processing concepts and
showcases every drone-reel CLI tool with runnable, real demos backed by real
`drone-reel` invocations against bundled sample clips.

## Local launch

```bash
# 1. Install requirements (drone-reel must already be installed in the same venv)
cd /Volumes/LaCie/_p-ai-drone-video/streamlit_textbook
pip install -r requirements.txt

# 2. Launch
streamlit run app.py
# → opens http://localhost:8501
```

Or using the project venv directly:
```bash
/Volumes/LaCie/_p-ai-drone-video/.venv/bin/streamlit run \
  /Volumes/LaCie/_p-ai-drone-video/streamlit_textbook/app.py
```

## Swapping in your own footage

The bundled clips live in `streamlit_textbook/assets/`:
- `clip_a.mp4` — Greenland aerial (2 MB)
- `clip_b.mp4` — desert/coastal scene (3.5 MB)
- `clip_c.mp4` — high-score scene (3.7 MB)
- `multi_scene.mp4` — multi-scene source for detection demos (15 MB)

To use your own footage:
1. Copy or symlink your clips into `assets/`.
2. Open `utils.py` and update `DEFAULT_CLIPS`:

```python
DEFAULT_CLIPS: dict[str, Path] = {
    "My flight 1": ASSETS_DIR / "my_clip1.mp4",
    "My flight 2": ASSETS_DIR / "my_clip2.mp4",
    "My long source": ASSETS_DIR / "my_source.mp4",
}
MULTI_SCENE_CLIP = ASSETS_DIR / "my_source.mp4"
```

3. Restart Streamlit. All demos will pick up the new clips automatically.

## Streamlit Cloud deployment

1. Fork the repo and push to GitHub.
2. Add `drone-reel` to `requirements.txt` for cloud install:

```text
streamlit>=1.30
plotly>=5.0
matplotlib>=3.7
pandas>=2.0
numpy>=1.24
scipy>=1.10
git+https://github.com/YOUR_ORG/drone-reel.git
```

3. Update `DRONE_REEL_BIN` in `utils.py` to use the PATH-installed binary:

```python
DRONE_REEL_BIN = Path("drone-reel")  # relies on PATH
```

4. Upload small bundled clips to `assets/` (keep under 50 MB total for free tier).
5. Deploy via the Streamlit Cloud dashboard pointing at `streamlit_textbook/app.py`.

## Cache and demo outputs

- Thumbnails cached in `.cache/thumbnails/` (keyed on path+mtime+timestamp).
- Demo renders cached in `.cache/demo_outputs/` (keyed on recipe+parameters).
- Delete `.cache/` to force fresh renders.

## Architecture

```
streamlit_textbook/
  app.py              # landing page + sidebar
  utils.py            # subprocess wrapper, probe, thumbnail extractor, helpers
  requirements.txt
  README.md
  pages/
    01_welcome.py     # what drone-reel does, install, command overview
    02_drone_footage.py   # D-Log/HLG/Rec709, proxies, fps
    03_scene_detection.py # PySceneDetect, threshold slider, Gantt timeline
    04_scoring_selection.py # 5-factor scoring, weight sliders, ranking
    05_reframing.py   # smart/pan/thirds/center, side-by-side preview
    06_stabilization.py   # adaptive stab, before/after
    07_speed_correction.py # auto_pan_speed_ramp, profile curves
    08_color_grading.py   # 30 presets, intensity, LUT, film effects
    09_beat_sync.py   # librosa beats, click-track viz, beat mode
    10_encoding.py    # BT.709, faststart, VBV, quality/platform
    11_recipes.py     # 10 named recipes, live run buttons
    12_cli_reference.py   # auto-parsed --help as searchable dataframe
  assets/
    clip_a.mp4        # Greenland aerial (~2 MB)
    clip_b.mp4        # Desert/coastal (~3.5 MB)
    clip_c.mp4        # High-score scene (~3.7 MB)
    multi_scene.mp4   # Multi-scene source (~15 MB)
  .cache/
    thumbnails/       # ffmpeg-extracted JPEG thumbnails
    demo_outputs/     # rendered demo clips (auto-populated on first run)
```
