# Examples

Code examples for common drone-reel workflows.

## Basic Examples

### [basic_reel.py](basic_reel.py)
Create a simple reel from a folder of clips without music.

### [beat_synced_reel.py](beat_synced_reel.py)
Create a reel with cuts synchronized to music beats.

### [custom_workflow.py](custom_workflow.py)
Full control over scene selection, transitions, and processing.

---

## Quick CLI Examples

### Simple reel from folder
```bash
drone-reel create -i ./clips/ -o my_reel.mp4
```

### With music and custom duration
```bash
drone-reel create -i ./clips/ -m ./music.mp3 -d 60 -o reel_60s.mp4
```

### Square format for Instagram feed
```bash
drone-reel create -i ./clips/ --aspect 1:1 --reframe center
```

### Cinematic look (landscape, color graded)
```bash
drone-reel create -i ./clips/ --no-reframe --color cinematic --aspect 16:9
```

### Preview clip selection without processing
```bash
drone-reel create -i ./clips/ -d 30 --preview
```

### Analyze footage before creating reel
```bash
drone-reel analyze -i ./raw_footage.mp4
drone-reel beats -i ./music.mp3
```

---

## Quick Python Examples

### Detect best scenes
```python
from pathlib import Path
from drone_reel import SceneDetector

detector = SceneDetector()
videos = list(Path("./clips").glob("*.mp4"))
best_scenes = detector.get_top_scenes(videos, count=10)

for scene in best_scenes:
    print(f"{scene.source_file.name}: {scene.start_time:.1f}s (score: {scene.score:.0f})")
```

### Analyze music
```python
from pathlib import Path
from drone_reel.core.beat_sync import BeatSync

beat_sync = BeatSync()
beat_info = beat_sync.analyze(Path("music.mp3"))

print(f"Tempo: {beat_info.tempo:.1f} BPM")
print(f"Duration: {beat_info.duration:.1f}s")
print(f"Beat count: {beat_info.beat_count}")
```

### Apply color grading
```python
from pathlib import Path
from drone_reel import ColorGrader
from drone_reel.core.color_grader import ColorPreset

grader = ColorGrader(preset=ColorPreset.CINEMATIC)
grader.grade_video(Path("input.mp4"), Path("graded.mp4"))
```

### Reframe to vertical
```python
from pathlib import Path
from drone_reel import Reframer
from drone_reel.core.reframer import ReframeSettings, AspectRatio, ReframeMode

reframer = Reframer(settings=ReframeSettings(
    target_ratio=AspectRatio.VERTICAL_9_16,
    mode=ReframeMode.SMART
))
reframer.reframe_video(Path("landscape.mp4"), Path("vertical.mp4"))
```
