"""
Demonstration of enhanced scene detection with camera motion classification.

This example shows how to use the SceneDetector.detect_scenes_enhanced() method
to analyze drone footage with detailed motion classification and visual analysis.
"""

from pathlib import Path
from drone_reel.core import SceneDetector, MotionType

def analyze_drone_footage(video_path: Path) -> None:
    """
    Analyze drone footage with enhanced scene detection.

    Args:
        video_path: Path to drone video file
    """
    detector = SceneDetector(
        threshold=27.0,
        min_scene_length=2.0,
        max_scene_length=8.0
    )

    print(f"Analyzing video: {video_path.name}")
    print("-" * 60)

    enhanced_scenes = detector.detect_scenes_enhanced(video_path)

    for i, scene in enumerate(enhanced_scenes, 1):
        print(f"\nScene {i}:")
        print(f"  Time: {scene.start_time:.1f}s - {scene.end_time:.1f}s ({scene.duration:.1f}s)")
        print(f"  Quality Score: {scene.score:.1f}/100")
        print(f"  Motion Type: {scene.motion_type.value}")
        print(f"  Motion Direction: ({scene.motion_direction[0]:.2f}, {scene.motion_direction[1]:.2f})")
        print(f"  Motion Smoothness: {scene.motion_smoothness:.1f}/100")
        print(f"  Golden Hour: {'Yes' if scene.is_golden_hour else 'No'}")
        print(f"  Depth Score: {scene.depth_score:.1f}/100")

        if scene.dominant_colors:
            print(f"  Dominant Colors: {len(scene.dominant_colors)} colors")
            for j, color in enumerate(scene.dominant_colors, 1):
                print(f"    Color {j}: RGB({color[2]}, {color[1]}, {color[0]})")

    print("\n" + "=" * 60)
    print("Motion Type Distribution:")
    motion_counts = {}
    for scene in enhanced_scenes:
        motion_type = scene.motion_type.value
        motion_counts[motion_type] = motion_counts.get(motion_type, 0) + 1

    for motion_type, count in sorted(motion_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(enhanced_scenes)) * 100
        print(f"  {motion_type}: {count} ({percentage:.1f}%)")

    golden_hour_count = sum(1 for s in enhanced_scenes if s.is_golden_hour)
    print(f"\nGolden Hour Scenes: {golden_hour_count}/{len(enhanced_scenes)}")

    avg_smoothness = sum(s.motion_smoothness for s in enhanced_scenes) / len(enhanced_scenes)
    print(f"Average Motion Smoothness: {avg_smoothness:.1f}/100")

    avg_depth = sum(s.depth_score for s in enhanced_scenes) / len(enhanced_scenes)
    print(f"Average Depth Score: {avg_depth:.1f}/100")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python enhanced_scene_detection_demo.py <video_path>")
        print("\nExample:")
        print("  python enhanced_scene_detection_demo.py drone_footage.mp4")
        sys.exit(1)

    video_path = Path(sys.argv[1])

    if not video_path.exists():
        print(f"Error: Video file not found: {video_path}")
        sys.exit(1)

    analyze_drone_footage(video_path)
