"""Markdown parser for converting markdown documents into presentation content.

This module handles parsing of markdown-formatted text with support for
headers, lists, code blocks, tables, and other markdown features.
"""

from __future__ import annotations

import re
from pathlib import Path

from pptx_generator.parsers.models import ParsedPresentation, SlideContent
from pptx_generator.utils.text import clean_text, split_into_bullets


class MarkdownParser:
    """Parse markdown content into presentation content.

    The MarkdownParser converts markdown documents into structured slides,
    respecting markdown syntax and converting it to appropriate slide layouts.

    Markdown features supported:
    - # H1 -> Presentation title
    - ## H2 -> Individual slide titles
    - ### H3 -> Subsection titles or emphasized content
    - Bullet lists (- or *) -> Slide bullets
    - Numbered lists (1. 2. 3.) -> Ordered slide bullets
    - Bold text (**text**) -> Preserved in bullets
    - Code blocks (```) -> Formatted as content with monospace note
    - Horizontal rules (---) -> Section divider slides
    - Tables -> Converted to comparison slides or content

    Examples:
        >>> parser = MarkdownParser()
        >>> md = "# Title\\n\\n## Slide 1\\n- Point A\\n- Point B"
        >>> result = parser.parse(md)
        >>> result.title
        'Title'
        >>> len(result.sections)
        2
    """

    def parse(
        self,
        markdown_text: str,
        max_bullets: int = 6,
    ) -> ParsedPresentation:
        """Parse markdown into structured presentation content.

        Args:
            markdown_text: Markdown-formatted input text
            max_bullets: Maximum bullets per slide before splitting

        Returns:
            ParsedPresentation with parsed slides

        Examples:
            >>> parser = MarkdownParser()
            >>> result = parser.parse("# My Presentation\\n\\n## Introduction")
            >>> result.title
            'My Presentation'
        """
        if not markdown_text:
            return ParsedPresentation(
                title="Empty Presentation",
                raw_text="",
            )

        cleaned = clean_text(markdown_text)
        lines = cleaned.split("\n")

        # Extract presentation title and metadata
        title, author, date, start_idx = self._extract_metadata(lines)

        # Parse slides from remaining content
        slides = self._parse_slides(lines[start_idx:], max_bullets)

        # Add title slide if we have a title
        if title and title != "Untitled Presentation":
            slides.insert(
                0,
                SlideContent(
                    slide_type="title",
                    title=title,
                    subtitle="",
                ),
            )

        return ParsedPresentation(
            title=title,
            subtitle="",
            author=author,
            date=date,
            sections=slides,
            raw_text=cleaned,
        )

    def _extract_metadata(
        self,
        lines: list[str],
    ) -> tuple[str, str, str, int]:
        """Extract title, author, date from markdown.

        Args:
            lines: Lines of markdown text

        Returns:
            Tuple of (title, author, date, start_line_index)
        """
        title = "Untitled Presentation"
        author = ""
        date = ""
        start_idx = 0

        # Look for H1 as title
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("# "):
                title = stripped[2:].strip()
                start_idx = idx + 1
                break

        # Look for author/date in next few lines (common markdown pattern)
        for i in range(start_idx, min(start_idx + 3, len(lines))):
            line = lines[i].strip()
            if line.lower().startswith("author:"):
                author = line.split(":", 1)[1].strip()
                start_idx = i + 1
            elif line.lower().startswith("date:"):
                date = line.split(":", 1)[1].strip()
                start_idx = i + 1

        return title, author, date, start_idx

    def _parse_slides(
        self,
        lines: list[str],
        max_bullets: int,
    ) -> list[SlideContent]:
        """Parse slide content from markdown lines.

        Args:
            lines: Lines of markdown content (after title)
            max_bullets: Maximum bullets per slide

        Returns:
            List of SlideContent objects
        """
        slides: list[SlideContent] = []
        current_slide: dict = {}
        in_code_block = False
        code_content: list[str] = []

        idx = 0
        while idx < len(lines):
            line = lines[idx]
            stripped = line.strip()

            # Handle code blocks
            if stripped.startswith("```"):
                if not in_code_block:
                    in_code_block = True
                    code_content = []
                else:
                    in_code_block = False
                    # Add code as a bullet or note
                    if current_slide:
                        code_text = "\n".join(code_content)
                        current_slide.setdefault("bullets", []).append(
                            f"[Code] {code_text[:100]}..."
                        )
                idx += 1
                continue

            if in_code_block:
                code_content.append(line)
                idx += 1
                continue

            # Handle horizontal rules (section dividers)
            if stripped in ("---", "***", "___"):
                # Finalize current slide
                if current_slide:
                    slides.append(self._create_slide(current_slide))
                    current_slide = {}

                # Add section divider
                slides.append(
                    SlideContent(
                        slide_type="section_divider",
                        title="",
                    )
                )
                idx += 1
                continue

            # Handle H2 headers (new slide)
            if stripped.startswith("## "):
                # Finalize previous slide
                if current_slide:
                    slides.append(self._create_slide(current_slide))

                # Start new slide
                current_slide = {
                    "title": stripped[3:].strip(),
                    "bullets": [],
                }
                idx += 1
                continue

            # Handle H3 headers (subsection within slide)
            if stripped.startswith("### "):
                subsection = stripped[4:].strip()
                if current_slide:
                    current_slide.setdefault("bullets", []).append(f"**{subsection}**")
                idx += 1
                continue

            # Handle bullet lists (unordered)
            if re.match(r"^[-*+]\s+", stripped):
                bullet = re.sub(r"^[-*+]\s+", "", stripped)
                bullet = self._process_inline_markdown(bullet)

                if not current_slide:
                    current_slide = {
                        "title": "Content",
                        "bullets": [],
                    }

                current_slide.setdefault("bullets", []).append(bullet)
                idx += 1
                continue

            # Handle numbered lists (ordered)
            if re.match(r"^\d+\.\s+", stripped):
                bullet = re.sub(r"^\d+\.\s+", "", stripped)
                bullet = self._process_inline_markdown(bullet)

                if not current_slide:
                    current_slide = {
                        "title": "Content",
                        "bullets": [],
                    }

                current_slide.setdefault("bullets", []).append(bullet)
                idx += 1
                continue

            # Handle tables
            if "|" in stripped and stripped.count("|") >= 2:
                table_lines, table_end_idx = self._extract_table(lines, idx)
                if table_lines:
                    # Finalize current slide
                    if current_slide:
                        slides.append(self._create_slide(current_slide))
                        current_slide = {}

                    # Create comparison slide from table
                    table_slide = self._parse_table(table_lines)
                    slides.append(table_slide)
                    idx = table_end_idx
                    continue

            # Regular content (convert to bullet if we have a current slide)
            if stripped and current_slide:
                # Accumulate content as bullets
                content_bullets = split_into_bullets(stripped, max_words=20)
                current_slide.setdefault("bullets", []).extend(content_bullets)

            idx += 1

        # Finalize last slide
        if current_slide:
            slides.append(self._create_slide(current_slide))

        # Split slides with too many bullets
        final_slides: list[SlideContent] = []
        for slide in slides:
            if len(slide.bullets) > max_bullets:
                # Split into multiple slides
                for i in range(0, len(slide.bullets), max_bullets):
                    chunk = slide.bullets[i : i + max_bullets]
                    chunk_title = slide.title
                    if i > 0:
                        chunk_title = f"{slide.title} (cont.)"

                    final_slides.append(
                        SlideContent(
                            slide_type=slide.slide_type,
                            title=chunk_title,
                            bullets=chunk,
                        )
                    )
            else:
                final_slides.append(slide)

        return final_slides

    def _create_slide(self, slide_data: dict) -> SlideContent:
        """Create SlideContent from parsed data.

        Args:
            slide_data: Dictionary with slide fields

        Returns:
            SlideContent object
        """
        return SlideContent(
            slide_type="content",
            title=slide_data.get("title", ""),
            bullets=slide_data.get("bullets", []),
        )

    def _process_inline_markdown(self, text: str) -> str:
        """Process inline markdown formatting.

        Converts bold (**text**), italic (*text*), and inline code (`code`)
        to plain text since PowerPoint formatting is applied separately.

        Args:
            text: Text with markdown formatting

        Returns:
            Plain text with formatting removed
        """
        # Remove bold (keep the text)
        text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
        text = re.sub(r"__(.+?)__", r"\1", text)

        # Remove italic (keep the text)
        text = re.sub(r"\*(.+?)\*", r"\1", text)
        text = re.sub(r"_(.+?)_", r"\1", text)

        # Remove inline code (keep the text)
        text = re.sub(r"`(.+?)`", r"\1", text)

        # Remove links, keep link text
        text = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", text)

        return text.strip()

    def _extract_table(
        self,
        lines: list[str],
        start_idx: int,
    ) -> tuple[list[str], int]:
        """Extract markdown table lines.

        Args:
            lines: All lines
            start_idx: Starting index

        Returns:
            Tuple of (table_lines, end_index)
        """
        table_lines: list[str] = []
        idx = start_idx

        while idx < len(lines):
            line = lines[idx].strip()
            if "|" in line:
                table_lines.append(line)
                idx += 1
            else:
                break

        return table_lines, idx

    def _parse_table(self, table_lines: list[str]) -> SlideContent:
        """Parse markdown table into comparison slide.

        Args:
            table_lines: Lines containing markdown table

        Returns:
            SlideContent with comparison layout
        """
        if len(table_lines) < 2:
            return SlideContent(
                slide_type="content",
                title="Table",
                bullets=["[Table content]"],
            )

        # Parse header row
        header = [cell.strip() for cell in table_lines[0].split("|")[1:-1]]

        # Skip separator row (---) if present
        data_start = 2 if len(table_lines) > 2 and "-" in table_lines[1] else 1

        # Parse data rows
        rows: list[list[str]] = []
        for line in table_lines[data_start:]:
            cells = [cell.strip() for cell in line.split("|")[1:-1]]
            if cells:
                rows.append(cells)

        # Convert to comparison slide if 2 columns
        if len(header) == 2:
            left_items = []
            right_items = []

            for row in rows:
                if len(row) >= 1:
                    left_items.append(row[0])
                if len(row) >= 2:
                    right_items.append(row[1])

            return SlideContent(
                slide_type="comparison",
                title="Comparison",
                left_title=header[0] if len(header) > 0 else "Left",
                left_bullets=left_items,
                right_title=header[1] if len(header) > 1 else "Right",
                right_bullets=right_items,
            )
        else:
            # Convert to content slide with bullets
            bullets = []
            for row in rows:
                bullet = " | ".join(row)
                bullets.append(bullet)

            return SlideContent(
                slide_type="content",
                title=" | ".join(header),
                bullets=bullets,
            )

    def parse_file(
        self,
        file_path: str,
        **kwargs,
    ) -> ParsedPresentation:
        """Read a markdown file and parse it.

        Args:
            file_path: Path to markdown file
            **kwargs: Additional arguments passed to parse()

        Returns:
            ParsedPresentation from file content

        Raises:
            FileNotFoundError: If file doesn't exist
            IOError: If file cannot be read

        Examples:
            >>> parser = MarkdownParser()
            >>> result = parser.parse_file("/path/to/document.md")
            >>> result.title
            'Document Title'
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            # Fallback to latin-1 if UTF-8 fails
            content = path.read_text(encoding="latin-1")

        return self.parse(content, **kwargs)
