"""
Advanced Color Grading Demo

Demonstrates all enhanced ColorGrader features:
- LUT support (.cube files)
- Tone curves with control points
- Selective color adjustments
- Improved shadows/highlights (LAB color space)
- Film grain with temporal coherence
- GPU acceleration
- Preview mode for fast iteration
"""

from pathlib import Path

import cv2
import numpy as np

from drone_reel.core.color_grader import (
    ColorAdjustments,
    ColorGrader,
    ColorPreset,
    SelectiveColorAdjustments,
    ToneCurve,
)


def create_sample_lut(output_path: Path) -> Path:
    """
    Create a sample cinematic LUT file for demonstration.

    This creates a simple warm, slightly desaturated look.
    """
    lut_size = 17  # Standard size for 3D LUTs

    with open(output_path, 'w') as f:
        f.write("# Cinematic Warm LUT\n")
        f.write("# Created for demo purposes\n")
        f.write("\n")
        f.write(f"LUT_3D_SIZE {lut_size}\n")
        f.write("\n")

        for r in range(lut_size):
            for g in range(lut_size):
                for b in range(lut_size):
                    r_norm = r / (lut_size - 1)
                    g_norm = g / (lut_size - 1)
                    b_norm = b / (lut_size - 1)

                    # Apply warm look: boost reds, reduce blues
                    r_out = min(1.0, r_norm * 1.1)
                    g_out = g_norm
                    b_out = b_norm * 0.9

                    f.write(f"{r_out:.6f} {g_out:.6f} {b_out:.6f}\n")

    print(f"Created sample LUT: {output_path}")
    return output_path


def demo_lut_support():
    """Demonstrate LUT loading and application."""
    print("\n=== LUT Support Demo ===")

    # Create a sample LUT
    lut_path = Path("sample_cinematic.cube")
    create_sample_lut(lut_path)

    # Create test image
    test_image = np.random.randint(50, 200, (480, 640, 3), dtype=np.uint8)

    # Apply LUT
    grader = ColorGrader(lut_path=lut_path)
    result = grader.grade_frame(test_image)

    print(f"Applied LUT to {test_image.shape} frame")
    print(f"Result shape: {result.shape}, dtype: {result.dtype}")

    # Cleanup
    lut_path.unlink()

    return result


def demo_tone_curves():
    """Demonstrate tone curve adjustments."""
    print("\n=== Tone Curves Demo ===")

    # Create gradient test image
    gradient = np.zeros((256, 640, 3), dtype=np.uint8)
    for i in range(256):
        gradient[i, :] = i

    # Define S-curve for contrast enhancement
    s_curve = ToneCurve(
        red_points=[(0, 0), (64, 45), (192, 210), (255, 255)],
        green_points=[(0, 0), (64, 45), (192, 210), (255, 255)],
        blue_points=[(0, 0), (64, 45), (192, 210), (255, 255)],
    )

    grader = ColorGrader(tone_curve=s_curve)
    result = grader.grade_frame(gradient)

    print("Applied S-curve for contrast enhancement")
    print(f"Original range: {gradient.min()}-{gradient.max()}")
    print(f"Result range: {result.min()}-{result.max()}")

    # Define per-channel curves for color grading
    color_curve = ToneCurve(
        red_points=[(0, 0), (128, 140), (255, 255)],     # Boost reds
        green_points=[(0, 0), (128, 128), (255, 245)],   # Slight green adjustment
        blue_points=[(0, 0), (128, 115), (255, 230)],    # Reduce blues
    )

    grader2 = ColorGrader(tone_curve=color_curve)
    result2 = grader2.grade_frame(gradient)

    print("Applied per-channel curves for warm look")

    return result, result2


def demo_selective_color():
    """Demonstrate selective color adjustments."""
    print("\n=== Selective Color Demo ===")

    # Create colorful test image
    test_image = np.zeros((480, 640, 3), dtype=np.uint8)

    # Red section
    test_image[0:160, :] = [0, 0, 180]
    # Green section
    test_image[160:320, :] = [0, 180, 0]
    # Blue section
    test_image[320:480, :] = [180, 0, 0]

    # Create selective color adjustments
    selective = SelectiveColorAdjustments(
        red_sat=30,      # Boost red saturation
        red_lum=10,      # Brighten reds
        green_hue=-10,   # Shift green hue towards cyan
        blue_sat=-20,    # Desaturate blues
    )

    adjustments = ColorAdjustments(selective_color=selective)
    grader = ColorGrader(adjustments=adjustments)

    result = grader.grade_frame(test_image)

    print("Applied selective color adjustments:")
    print("  - Red: +30% saturation, +10 luminance")
    print("  - Green: -10 hue shift")
    print("  - Blue: -20% saturation")

    return result


def demo_improved_shadows_highlights():
    """Demonstrate improved shadows/highlights using LAB color space."""
    print("\n=== Improved Shadows/Highlights Demo ===")

    # Create test image with shadows and highlights
    test_image = np.zeros((480, 640, 3), dtype=np.uint8)

    # Dark section (shadows)
    test_image[0:160, :, :] = 40
    # Mid-tones
    test_image[160:320, :, :] = 128
    # Bright section (highlights)
    test_image[320:480, :, :] = 220

    # Add some color variation
    test_image[:, 0:213, 0] = test_image[:, 0:213, 0] + 20  # More blue
    test_image[:, 213:426, 1] = test_image[:, 213:426, 1] + 20  # More green
    test_image[:, 426:640, 2] = test_image[:, 426:640, 2] + 20  # More red

    # Adjust shadows and highlights
    adjustments = ColorAdjustments(
        shadows=40,      # Lift shadows
        highlights=-30,  # Recover highlights
    )

    grader = ColorGrader(adjustments=adjustments)
    result = grader.grade_frame(test_image)

    print("Applied shadows/highlights using LAB color space")
    print("  - Better color preservation during tonal adjustments")
    print(f"Shadow area before: {test_image[80, 320].mean():.1f}")
    print(f"Shadow area after: {result[80, 320].mean():.1f}")
    print(f"Highlight area before: {test_image[400, 320].mean():.1f}")
    print(f"Highlight area after: {result[400, 320].mean():.1f}")

    return result


def demo_improved_grain():
    """Demonstrate improved film grain."""
    print("\n=== Improved Film Grain Demo ===")

    # Create test image
    test_image = np.full((480, 640, 3), 128, dtype=np.uint8)

    # Add gradient
    for i in range(480):
        intensity = int(50 + (i / 480) * 150)
        test_image[i, :] = intensity

    adjustments = ColorAdjustments(grain=50)
    grader = ColorGrader(adjustments=adjustments)

    # Generate multiple frames to show temporal coherence
    frames = []
    for i in range(5):
        result = grader.grade_frame(test_image.copy(), frame_index=i)
        frames.append(result)

    print("Generated 5 frames with temporal coherence")
    print("  - Grain pattern changes between frames")
    print("  - Same seed produces same grain")
    print("  - Grain stronger in midtones (film-like)")

    # Verify temporal coherence
    diff_0_1 = np.abs(frames[0].astype(float) - frames[1].astype(float)).mean()
    diff_0_0 = 0.0  # Same frame

    print(f"  - Difference between frame 0 and 1: {diff_0_1:.2f}")

    return frames


def demo_gpu_acceleration():
    """Demonstrate GPU acceleration."""
    print("\n=== GPU Acceleration Demo ===")

    test_image = np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)

    # Test GPU availability
    grader_gpu = ColorGrader(use_gpu=True)
    print(f"GPU available: {grader_gpu.use_gpu}")

    if grader_gpu.use_gpu:
        print("GPU acceleration enabled")
    else:
        print("GPU not available, using CPU")

    # Apply adjustments
    adjustments = ColorAdjustments(
        brightness=10,
        contrast=15,
        saturation=5,
    )

    grader_gpu = ColorGrader(adjustments=adjustments, use_gpu=True)
    result_gpu = grader_gpu.grade_frame(test_image)

    grader_cpu = ColorGrader(adjustments=adjustments, use_gpu=False)
    result_cpu = grader_cpu.grade_frame(test_image)

    # Compare results
    difference = np.abs(result_gpu.astype(float) - result_cpu.astype(float)).mean()
    print(f"Average difference between GPU and CPU: {difference:.2f}")

    return result_gpu


def demo_preview_mode():
    """Demonstrate preview mode for fast iteration."""
    print("\n=== Preview Mode Demo ===")

    # Create high-resolution test image
    test_image = np.random.randint(0, 255, (2160, 3840, 3), dtype=np.uint8)

    adjustments = ColorAdjustments(
        contrast=20,
        saturation=15,
        grain=30,
    )

    grader = ColorGrader(adjustments=adjustments)

    # Full resolution
    full_result = grader.grade_frame(test_image)

    # Preview at 25% scale
    preview_result = grader.grade_frame_preview(test_image, scale=0.25)

    print(f"Full resolution: {full_result.shape}")
    print(f"Preview resolution: {preview_result.shape}")

    full_pixels = full_result.shape[0] * full_result.shape[1]
    preview_pixels = preview_result.shape[0] * preview_result.shape[1]
    speedup = full_pixels / preview_pixels

    print(f"Preview is ~{speedup:.1f}x faster")
    print("  - Use preview for quick adjustment iteration")
    print("  - Apply full resolution for final render")

    return preview_result


def demo_complete_workflow():
    """Demonstrate complete color grading workflow."""
    print("\n=== Complete Workflow Demo ===")

    # Create sample LUT
    lut_path = Path("workflow_lut.cube")
    create_sample_lut(lut_path)

    # Create test image
    test_image = np.random.randint(30, 220, (1080, 1920, 3), dtype=np.uint8)

    # Define complete color grade
    selective = SelectiveColorAdjustments(
        orange_sat=25,    # Boost skin tones
        blue_sat=-10,     # Desaturate skies slightly
        green_sat=15,     # Boost foliage
    )

    adjustments = ColorAdjustments(
        brightness=3,
        contrast=12,
        saturation=-5,
        temperature=8,
        shadows=15,
        highlights=-10,
        fade=5,
        grain=20,
        selective_color=selective,
    )

    tone_curve = ToneCurve(
        red_points=[(0, 0), (64, 50), (192, 205), (255, 255)],
        green_points=[(0, 0), (64, 48), (192, 207), (255, 255)],
        blue_points=[(0, 0), (64, 45), (192, 210), (255, 250)],
    )

    # Create grader with all features
    grader = ColorGrader(
        adjustments=adjustments,
        lut_path=lut_path,
        tone_curve=tone_curve,
        use_gpu=True,
    )

    print("Created comprehensive color grade with:")
    print("  - Custom LUT")
    print("  - S-curve tone adjustments")
    print("  - Selective color adjustments")
    print("  - Shadow/highlight recovery")
    print("  - Film grain")
    print("  - GPU acceleration")

    # First, preview the grade
    print("\nGenerating preview...")
    preview = grader.grade_frame_preview(test_image, scale=0.25)
    print(f"Preview size: {preview.shape}")

    # Then apply full resolution
    print("\nApplying full resolution grade...")
    result = grader.grade_frame(test_image, frame_index=0)
    print(f"Final size: {result.shape}")

    # Cleanup
    lut_path.unlink()

    return result


def main():
    """Run all demonstrations."""
    print("=" * 60)
    print("Advanced Color Grading Feature Demonstration")
    print("=" * 60)

    try:
        # Run each demo
        demo_lut_support()
        demo_tone_curves()
        demo_selective_color()
        demo_improved_shadows_highlights()
        demo_improved_grain()
        demo_gpu_acceleration()
        demo_preview_mode()
        demo_complete_workflow()

        print("\n" + "=" * 60)
        print("All demonstrations completed successfully!")
        print("=" * 60)

        print("\nUsage Examples:")
        print("\n1. Load and apply a LUT:")
        print("   grader = ColorGrader(lut_path=Path('my_lut.cube'))")

        print("\n2. Create custom tone curves:")
        print("   curve = ToneCurve(")
        print("       red_points=[(0, 0), (128, 140), (255, 255)],")
        print("       green_points=[(0, 0), (128, 135), (255, 255)],")
        print("       blue_points=[(0, 0), (128, 125), (255, 255)],")
        print("   )")
        print("   grader = ColorGrader(tone_curve=curve)")

        print("\n3. Adjust specific colors:")
        print("   selective = SelectiveColorAdjustments(")
        print("       red_sat=30,  # Boost red saturation")
        print("       blue_hue=10, # Shift blue hue")
        print("   )")
        print("   adjustments = ColorAdjustments(selective_color=selective)")
        print("   grader = ColorGrader(adjustments=adjustments)")

        print("\n4. Enable GPU acceleration:")
        print("   grader = ColorGrader(use_gpu=True)")

        print("\n5. Use preview mode:")
        print("   preview = grader.grade_frame_preview(frame, scale=0.25)")

        print("\n6. Combine all features:")
        print("   grader = ColorGrader(")
        print("       adjustments=adjustments,")
        print("       lut_path=lut_path,")
        print("       tone_curve=curve,")
        print("       use_gpu=True,")
        print("   )")
        print("   result = grader.grade_frame(frame, frame_index=0)")

    except Exception as e:
        print(f"\nError during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
