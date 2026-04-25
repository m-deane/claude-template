"""
Thumbnail generation and video preview functionality for drone-reel.

Provides tools to generate eye-catching thumbnails and quick preview videos
for rapid iteration and quality verification before full render.
"""

from enum import Enum
from pathlib import Path

import cv2
import numpy as np
from moviepy import VideoFileClip, concatenate_videoclips, vfx
from PIL import Image, ImageDraw, ImageFont

from drone_reel.core.scene_detector import SceneInfo
from drone_reel.core.video_processor import ClipSegment


class ThumbnailStyle(Enum):
    """Thumbnail generation styles."""

    HERO = "hero"  # Single best frame
    COMPOSITE = "composite"  # Grid of multiple frames
    TEXT_OVERLAY = "text_overlay"  # Best frame with text


class ThumbnailGenerator:
    """
    Generate high-quality thumbnails from video scenes.

    Uses advanced scoring to identify the most visually compelling frames
    and creates various styles of thumbnails suitable for social media.
    """

    def __init__(self):
        """Initialize the thumbnail generator."""
        self._font_cache: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}

    def generate(
        self,
        scenes: list[SceneInfo],
        output_path: Path,
        style: ThumbnailStyle = ThumbnailStyle.HERO,
        size: tuple[int, int] = (1080, 1920),
        text: str | None = None,
    ) -> Path:
        """
        Generate thumbnail image from scenes.

        Args:
            scenes: List of SceneInfo objects to select from
            output_path: Path to save thumbnail image
            style: ThumbnailStyle to use
            size: Output size (width, height)
            text: Optional text for TEXT_OVERLAY style

        Returns:
            Path to generated thumbnail

        Raises:
            ValueError: If scenes list is empty or invalid parameters
            RuntimeError: If thumbnail generation fails
        """
        if not scenes:
            raise ValueError("No scenes provided for thumbnail generation")

        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            if style == ThumbnailStyle.HERO:
                thumbnail = self._generate_hero_thumbnail(scenes, size)
            elif style == ThumbnailStyle.COMPOSITE:
                thumbnail = self._generate_composite_thumbnail(scenes, size)
            elif style == ThumbnailStyle.TEXT_OVERLAY:
                thumbnail = self._generate_text_overlay_thumbnail(scenes, size, text)
            else:
                raise ValueError(f"Unknown thumbnail style: {style}")

            # Convert BGR to RGB for PIL
            thumbnail_rgb = cv2.cvtColor(thumbnail, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(thumbnail_rgb)
            img.save(str(output_path), quality=95, optimize=True)

            return output_path

        except Exception as e:
            raise RuntimeError(f"Failed to generate thumbnail: {str(e)}") from e

    def _generate_hero_thumbnail(
        self, scenes: list[SceneInfo], size: tuple[int, int]
    ) -> np.ndarray:
        """Generate single best frame thumbnail."""
        best_frame = None
        best_score = -1.0

        for scene in scenes:
            frame = self.select_best_frame(scene, criteria="composition")
            score = self.score_thumbnail_potential(frame)

            if score > best_score:
                best_score = score
                best_frame = frame

        if best_frame is None:
            raise RuntimeError("Failed to extract best frame")

        return cv2.resize(best_frame, size, interpolation=cv2.INTER_LANCZOS4)

    def _generate_composite_thumbnail(
        self, scenes: list[SceneInfo], size: tuple[int, int]
    ) -> np.ndarray:
        """Generate composite grid thumbnail."""
        grid_size = self._calculate_grid_size(len(scenes))
        return self.create_composite_thumbnail(scenes, grid_size, size)

    def _generate_text_overlay_thumbnail(
        self, scenes: list[SceneInfo], size: tuple[int, int], text: str | None
    ) -> np.ndarray:
        """Generate thumbnail with text overlay."""
        hero = self._generate_hero_thumbnail(scenes, size)

        if text:
            hero = self.add_text_to_thumbnail(hero, text, position="bottom", style="bold")

        return hero

    def _calculate_grid_size(self, scene_count: int) -> tuple[int, int]:
        """Calculate optimal grid dimensions for scene count."""
        if scene_count <= 1:
            return (1, 1)
        elif scene_count <= 4:
            return (2, 2)
        elif scene_count <= 6:
            return (2, 3)
        elif scene_count <= 9:
            return (3, 3)
        elif scene_count <= 12:
            return (3, 4)
        else:
            return (4, 4)

    def select_best_frame(
        self, scene: SceneInfo, criteria: str = "composition"
    ) -> np.ndarray:
        """
        Select best frame from a scene for thumbnail.

        Args:
            scene: SceneInfo to extract frame from
            criteria: Selection criteria ("composition", "color", "sharpness")

        Returns:
            Best frame as numpy array (BGR)

        Raises:
            ValueError: If invalid criteria specified
            RuntimeError: If frame extraction fails
        """
        valid_criteria = {"composition", "color", "sharpness"}
        if criteria not in valid_criteria:
            raise ValueError(f"Invalid criteria: {criteria}. Must be one of {valid_criteria}")

        cap = cv2.VideoCapture(str(scene.source_file))
        fps = cap.get(cv2.CAP_PROP_FPS)

        start_frame = int(scene.start_time * fps)
        end_frame = int(scene.end_time * fps)

        # Sample frames throughout scene
        sample_count = min(20, end_frame - start_frame)
        sample_interval = max(1, (end_frame - start_frame) // sample_count)

        best_frame = None
        best_score = -1.0

        try:
            for frame_num in range(start_frame, end_frame, sample_interval):
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
                ret, frame = cap.read()

                if not ret:
                    continue

                score = self._score_by_criteria(frame, criteria)

                if score > best_score:
                    best_score = score
                    best_frame = frame.copy()

        finally:
            cap.release()

        if best_frame is None:
            raise RuntimeError(f"Failed to extract frame from scene at {scene.source_file}")

        return best_frame

    def _score_by_criteria(self, frame: np.ndarray, criteria: str) -> float:
        """Score frame by specific criteria."""
        if criteria == "composition":
            return self._score_composition(frame)
        elif criteria == "color":
            return self._score_color_richness(frame)
        elif criteria == "sharpness":
            return self._score_sharpness(frame)
        return 0.0

    def score_thumbnail_potential(self, frame: np.ndarray) -> float:
        """
        Score frame's potential as thumbnail (0-100).

        Combines multiple visual quality metrics:
        - Composition score (rule of thirds) - 30%
        - Color saturation - 25%
        - Sharpness - 25%
        - Clear subject/focal point - 20%

        Args:
            frame: Frame to score (BGR)

        Returns:
            Score from 0-100, higher is better
        """
        composition_score = self._score_composition(frame)
        color_score = self._score_color_richness(frame)
        sharpness_score = self._score_sharpness(frame)
        focus_score = self._score_focal_point(frame)

        total_score = (
            composition_score * 0.30
            + color_score * 0.25
            + sharpness_score * 0.25
            + focus_score * 0.20
        )

        return min(total_score, 100.0)

    def _score_composition(self, frame: np.ndarray) -> float:
        """Score composition using rule of thirds."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)

        height, width = edges.shape
        h_third = height // 3
        w_third = width // 3

        # Score edge density at rule of thirds intersections
        tolerance = int(min(width, height) * 0.05)

        # Four key intersection points
        intersections = [
            (w_third, h_third),
            (2 * w_third, h_third),
            (w_third, 2 * h_third),
            (2 * w_third, 2 * h_third),
        ]

        total_density = 0.0
        for x, y in intersections:
            y_start = max(0, y - tolerance)
            y_end = min(height, y + tolerance)
            x_start = max(0, x - tolerance)
            x_end = min(width, x + tolerance)

            region = edges[y_start:y_end, x_start:x_end]
            density = np.sum(region) / (region.size * 255.0 + 1e-6)
            total_density += density

        # Average and normalize
        avg_density = total_density / len(intersections)
        return min(avg_density * 500, 100.0)

    def _score_color_richness(self, frame: np.ndarray) -> float:
        """Score color richness and vibrancy."""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        saturation = hsv[:, :, 1]

        mean_sat = np.mean(saturation)
        std_sat = np.std(saturation)

        # High mean saturation = vibrant colors
        # High std = variety of colors
        vibrancy_score = (mean_sat / 255.0) * 60
        variety_score = (std_sat / 128.0) * 40

        return min(vibrancy_score + variety_score, 100.0)

    def _score_sharpness(self, frame: np.ndarray) -> float:
        """Score image sharpness using Laplacian variance."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        variance = laplacian.var()

        # Normalize variance to 0-100 scale
        # Typical sharp images have variance > 500
        return min((variance / 500.0) * 100, 100.0)

    def _score_focal_point(self, frame: np.ndarray) -> float:
        """Score presence of clear focal point."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Use edge detection to find strong features
        edges = cv2.Canny(gray, 100, 200)

        height, width = edges.shape
        center_y, center_x = height // 2, width // 2

        # Create gaussian weight map centered on image
        y_coords, x_coords = np.ogrid[:height, :width]
        distances = np.sqrt((x_coords - center_x) ** 2 + (y_coords - center_y) ** 2)
        max_distance = np.sqrt(center_x**2 + center_y**2)
        weights = np.exp(-distances / (max_distance * 0.3))

        # Weighted edge density - higher score if edges concentrated in center
        weighted_edges = edges * weights
        center_score = np.sum(weighted_edges) / (np.sum(weights) * 255.0 + 1e-6)

        return min(center_score * 500, 100.0)

    def create_composite_thumbnail(
        self,
        scenes: list[SceneInfo],
        grid_size: tuple[int, int] = (2, 2),
        output_size: tuple[int, int] = (1080, 1080),
    ) -> np.ndarray:
        """
        Create grid composite of multiple scenes.

        Args:
            scenes: List of scenes to include
            grid_size: Grid dimensions (rows, cols)
            output_size: Output image size (width, height)

        Returns:
            Composite thumbnail as numpy array (BGR)
        """
        rows, cols = grid_size
        total_cells = rows * cols

        # Limit scenes to grid capacity
        scenes_to_use = scenes[:total_cells]

        # Calculate cell dimensions
        cell_width = output_size[0] // cols
        cell_height = output_size[1] // rows

        # Create blank canvas
        composite = np.zeros((output_size[1], output_size[0], 3), dtype=np.uint8)

        # Fill grid with best frames from each scene
        for idx, scene in enumerate(scenes_to_use):
            row = idx // cols
            col = idx % cols

            frame = self.select_best_frame(scene, criteria="composition")
            resized = cv2.resize(
                frame, (cell_width, cell_height), interpolation=cv2.INTER_LANCZOS4
            )

            y_start = row * cell_height
            y_end = y_start + cell_height
            x_start = col * cell_width
            x_end = x_start + cell_width

            composite[y_start:y_end, x_start:x_end] = resized

        # Add subtle grid lines
        grid_color = (50, 50, 50)
        for i in range(1, rows):
            y = i * cell_height
            cv2.line(composite, (0, y), (output_size[0], y), grid_color, 2)

        for i in range(1, cols):
            x = i * cell_width
            cv2.line(composite, (x, 0), (x, output_size[1]), grid_color, 2)

        return composite

    def add_text_to_thumbnail(
        self,
        image: np.ndarray,
        text: str,
        position: str = "bottom",
        style: str = "bold",
    ) -> np.ndarray:
        """
        Add text overlay to thumbnail.

        Args:
            image: Input image (BGR)
            text: Text to add
            position: Text position ("top", "bottom", "center")
            style: Text style ("bold", "outlined", "shadowed")

        Returns:
            Image with text overlay (BGR)
        """
        # Convert to PIL for better text rendering
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb)
        draw = ImageDraw.Draw(pil_img)

        height, width = image.shape[:2]

        # Calculate font size based on image size
        font_size = max(24, width // 20)
        font = self._get_font(font_size, bold=(style == "bold"))

        # Get text bounding box
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Calculate position
        if position == "bottom":
            x = (width - text_width) // 2
            y = height - text_height - int(height * 0.05)
        elif position == "top":
            x = (width - text_width) // 2
            y = int(height * 0.05)
        elif position == "center":
            x = (width - text_width) // 2
            y = (height - text_height) // 2
        else:
            x = (width - text_width) // 2
            y = height - text_height - int(height * 0.05)

        # Add text with effects
        if style == "outlined":
            # Draw outline
            outline_width = max(2, font_size // 20)
            for dx in range(-outline_width, outline_width + 1):
                for dy in range(-outline_width, outline_width + 1):
                    if dx != 0 or dy != 0:
                        draw.text((x + dx, y + dy), text, font=font, fill=(0, 0, 0, 255))
            # Draw main text
            draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))

        elif style == "shadowed":
            # Draw shadow
            shadow_offset = max(2, font_size // 20)
            draw.text(
                (x + shadow_offset, y + shadow_offset), text, font=font, fill=(0, 0, 0, 200)
            )
            # Draw main text
            draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))

        else:  # bold or default
            # Add semi-transparent background bar
            padding = int(height * 0.03)
            bar_height = text_height + 2 * padding
            bar_y = y - padding

            # Create semi-transparent overlay
            overlay = pil_img.copy()
            overlay_draw = ImageDraw.Draw(overlay)
            overlay_draw.rectangle(
                [(0, bar_y), (width, bar_y + bar_height)], fill=(0, 0, 0, 180)
            )

            # Blend overlay
            pil_img = Image.blend(pil_img, overlay, 0.7)
            draw = ImageDraw.Draw(pil_img)

            # Draw text
            draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))

        # Convert back to BGR numpy array
        result = np.array(pil_img)
        return cv2.cvtColor(result, cv2.COLOR_RGB2BGR)

    def _get_font(self, size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
        """Get or load font with caching."""
        cache_key = ("default", size)

        if cache_key in self._font_cache:
            return self._font_cache[cache_key]

        # Try to load system fonts
        font_paths = [
            "/System/Library/Fonts/Helvetica.ttc",  # macOS
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux
            "C:\\Windows\\Fonts\\arial.ttf",  # Windows
        ]

        font = None
        for font_path in font_paths:
            try:
                font = ImageFont.truetype(font_path, size)
                break
            except OSError:
                continue

        if font is None:
            # Fallback to default font
            font = ImageFont.load_default()

        self._font_cache[cache_key] = font
        return font


class PreviewGenerator:
    """
    Generate quick preview videos and storyboards for rapid iteration.

    Creates low-resolution preview videos for fast review of edit decisions
    before committing to full-quality render.
    """

    def __init__(self, preview_scale: float = 0.25, preview_fps: int = 15):
        """
        Initialize preview generator.

        Args:
            preview_scale: Scale factor for preview resolution (0.25 = quarter res)
            preview_fps: Frame rate for preview videos
        """
        if preview_scale <= 0 or preview_scale > 1:
            raise ValueError("preview_scale must be between 0 and 1")

        self.preview_scale = preview_scale
        self.preview_fps = preview_fps

    def generate_preview(
        self,
        segments: list[ClipSegment],
        output_path: Path,
        include_transitions: bool = True,
    ) -> Path:
        """
        Generate quick low-resolution preview.

        Args:
            segments: List of ClipSegment objects to preview
            output_path: Path for preview video
            include_transitions: Whether to include transitions

        Returns:
            Path to generated preview video

        Raises:
            ValueError: If segments list is empty
            RuntimeError: If preview generation fails
        """
        if not segments:
            raise ValueError("No segments provided for preview")

        output_path.parent.mkdir(parents=True, exist_ok=True)

        source_clips = []
        preview_clips = []

        try:
            for segment in segments:
                source_clip = VideoFileClip(str(segment.scene.source_file))
                source_clips.append(source_clip)

                # Extract segment
                start = segment.effective_start
                end = min(start + segment.effective_duration, source_clip.duration)
                subclip = source_clip.subclipped(start, end)

                # Downscale for preview
                new_size = (
                    int(subclip.w * self.preview_scale),
                    int(subclip.h * self.preview_scale),
                )
                preview_clip = subclip.resized(new_size)

                # Add transitions if requested
                if include_transitions and segment.transition_in.value != "cut":
                    preview_clip = preview_clip.with_effects(
                        [vfx.CrossFadeIn(segment.transition_duration)]
                    )

                if include_transitions and segment.transition_out.value != "cut":
                    preview_clip = preview_clip.with_effects(
                        [vfx.CrossFadeOut(segment.transition_duration)]
                    )

                preview_clips.append(preview_clip)

            # Concatenate all clips
            final_preview = concatenate_videoclips(preview_clips, method="compose")

            # Write preview with fast settings
            final_preview.write_videofile(
                str(output_path),
                fps=self.preview_fps,
                codec="libx264",
                preset="ultrafast",
                audio_codec="aac",
                logger=None,
            )

            return output_path

        except Exception as e:
            raise RuntimeError(f"Failed to generate preview: {str(e)}") from e

        finally:
            # Clean up
            try:
                if "final_preview" in locals():
                    final_preview.close()
            except Exception:
                pass

            for clip in preview_clips:
                try:
                    clip.close()
                except Exception:
                    pass

            for clip in source_clips:
                try:
                    clip.close()
                except Exception:
                    pass

    def generate_storyboard(
        self,
        segments: list[ClipSegment],
        output_path: Path,
        frames_per_segment: int = 3,
        grid_columns: int = 4,
    ) -> Path:
        """
        Generate storyboard grid image showing edit plan.

        Args:
            segments: List of ClipSegment objects
            output_path: Path to save storyboard image
            frames_per_segment: Number of frames to extract per segment
            grid_columns: Number of columns in grid

        Returns:
            Path to generated storyboard

        Raises:
            ValueError: If invalid parameters
            RuntimeError: If storyboard generation fails
        """
        if not segments:
            raise ValueError("No segments provided for storyboard")

        if frames_per_segment < 1:
            raise ValueError("frames_per_segment must be at least 1")

        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            frames = []

            for segment in segments:
                cap = cv2.VideoCapture(str(segment.scene.source_file))
                fps = cap.get(cv2.CAP_PROP_FPS)

                start_frame = int(segment.effective_start * fps)
                end_frame = int((segment.effective_start + segment.effective_duration) * fps)
                duration_frames = end_frame - start_frame

                # Extract evenly spaced frames
                frame_indices = np.linspace(start_frame, end_frame - 1, frames_per_segment, dtype=int)

                for frame_idx in frame_indices:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                    ret, frame = cap.read()

                    if ret:
                        frames.append(frame)

                cap.release()

            if not frames:
                raise RuntimeError("Failed to extract frames for storyboard")

            # Calculate grid dimensions
            total_frames = len(frames)
            grid_rows = (total_frames + grid_columns - 1) // grid_columns

            # Determine cell size based on first frame
            first_frame_height, first_frame_width = frames[0].shape[:2]
            aspect_ratio = first_frame_width / first_frame_height

            # Standard cell size
            cell_width = 320
            cell_height = int(cell_width / aspect_ratio)

            # Create storyboard canvas
            canvas_width = cell_width * grid_columns
            canvas_height = cell_height * grid_rows
            storyboard = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)

            # Place frames in grid
            for idx, frame in enumerate(frames):
                row = idx // grid_columns
                col = idx % grid_columns

                resized = cv2.resize(frame, (cell_width, cell_height), interpolation=cv2.INTER_AREA)

                y_start = row * cell_height
                y_end = y_start + cell_height
                x_start = col * cell_width
                x_end = x_start + cell_width

                storyboard[y_start:y_end, x_start:x_end] = resized

                # Add frame number
                cv2.putText(
                    storyboard,
                    f"#{idx + 1}",
                    (x_start + 10, y_start + 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2,
                )

            # Add grid lines
            grid_color = (100, 100, 100)
            for i in range(1, grid_rows):
                y = i * cell_height
                cv2.line(storyboard, (0, y), (canvas_width, y), grid_color, 2)

            for i in range(1, grid_columns):
                x = i * cell_width
                cv2.line(storyboard, (x, 0), (x, canvas_height), grid_color, 2)

            # Save storyboard
            cv2.imwrite(str(output_path), storyboard, [cv2.IMWRITE_JPEG_QUALITY, 90])

            return output_path

        except Exception as e:
            raise RuntimeError(f"Failed to generate storyboard: {str(e)}") from e

    def estimate_preview_time(self, segments: list[ClipSegment]) -> float:
        """
        Estimate time to generate preview in seconds.

        Args:
            segments: List of segments to preview

        Returns:
            Estimated time in seconds
        """
        total_duration = sum(seg.effective_duration for seg in segments)

        # Empirical formula: processing time ~= 0.1x for low-res preview
        base_time = total_duration * 0.1

        # Add overhead for I/O and setup
        overhead = len(segments) * 0.5

        return base_time + overhead

    def create_comparison(
        self,
        original: Path,
        edited: Path,
        output_path: Path,
        mode: str = "side_by_side",
    ) -> Path:
        """
        Create comparison video of before/after.

        Args:
            original: Path to original video
            edited: Path to edited video
            output_path: Path for comparison video
            mode: Comparison mode ("side_by_side", "overlay", "split")

        Returns:
            Path to comparison video

        Raises:
            ValueError: If invalid mode
            RuntimeError: If comparison generation fails
        """
        valid_modes = {"side_by_side", "overlay", "split"}
        if mode not in valid_modes:
            raise ValueError(f"Invalid mode: {mode}. Must be one of {valid_modes}")

        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            original_clip = VideoFileClip(str(original))
            edited_clip = VideoFileClip(str(edited))

            # Match durations
            min_duration = min(original_clip.duration, edited_clip.duration)
            original_clip = original_clip.subclipped(0, min_duration)
            edited_clip = edited_clip.subclipped(0, min_duration)

            if mode == "side_by_side":
                comparison = self._create_side_by_side(original_clip, edited_clip)
            elif mode == "overlay":
                comparison = self._create_overlay(original_clip, edited_clip)
            elif mode == "split":
                comparison = self._create_split_screen(original_clip, edited_clip)
            else:
                raise ValueError(f"Unsupported mode: {mode}")

            # Write comparison video
            comparison.write_videofile(
                str(output_path),
                fps=self.preview_fps,
                codec="libx264",
                preset="medium",
                audio_codec="aac",
                logger=None,
            )

            return output_path

        except Exception as e:
            raise RuntimeError(f"Failed to create comparison: {str(e)}") from e

        finally:
            try:
                original_clip.close()
                edited_clip.close()
                if "comparison" in locals():
                    comparison.close()
            except Exception:
                pass

    def _create_side_by_side(
        self, clip1: VideoFileClip, clip2: VideoFileClip
    ) -> VideoFileClip:
        """Create side-by-side comparison."""
        from moviepy import CompositeVideoClip

        # Resize both to half width
        w, h = clip1.size
        resized1 = clip1.resized((w // 2, h))
        resized2 = clip2.resized((w // 2, h))

        # Position side by side
        resized2 = resized2.with_position((w // 2, 0))

        return CompositeVideoClip([resized1, resized2], size=(w, h))

    def _create_overlay(self, clip1: VideoFileClip, clip2: VideoFileClip) -> VideoFileClip:
        """Create overlay comparison with transparency."""
        from moviepy import CompositeVideoClip

        # Make edited clip semi-transparent
        clip2_transparent = clip2.with_opacity(0.5)

        return CompositeVideoClip([clip1, clip2_transparent])

    def _create_split_screen(
        self, clip1: VideoFileClip, clip2: VideoFileClip
    ) -> VideoFileClip:
        """Create vertical split screen comparison."""
        w, h = clip1.size

        def make_frame(t):
            frame1 = clip1.get_frame(t)
            frame2 = clip2.get_frame(t)

            # Split vertically down the middle
            result = np.zeros_like(frame1)
            result[:, : w // 2] = frame1[:, : w // 2]
            result[:, w // 2 :] = frame2[:, w // 2 :]

            # Add vertical line in the middle
            result[:, w // 2 - 2 : w // 2 + 2] = [255, 255, 255]

            return result

        from moviepy import VideoClip

        return VideoClip(make_frame, duration=clip1.duration).with_fps(clip1.fps)
