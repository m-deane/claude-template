"""Text parser for converting plain text into presentation content.

This module handles parsing of unstructured text documents, research notes,
and other plain text content into structured slide presentations.
"""

from __future__ import annotations

from pathlib import Path

from pptx_generator.parsers.models import ParsedPresentation, SlideContent
from pptx_generator.utils.text import (
    clean_text,
    extract_title,
    split_into_sections,
)


class TextParser:
    """Parse plain text or research notes into presentation content.

    The TextParser converts unstructured text into structured slides by:
    1. Extracting a title from the first heading or sentence
    2. Splitting content into logical sections
    3. Converting each section into one or more slides
    4. Breaking up sections with too many bullets across multiple slides

    Examples:
        >>> parser = TextParser()
        >>> presentation = parser.parse("Introduction\\n\\nThis is content.")
        >>> presentation.title
        'Introduction'
        >>> len(presentation.sections)
        1
    """

    def parse(
        self,
        text: str,
        max_bullets: int = 6,
        max_words_per_bullet: int = 20,
    ) -> ParsedPresentation:
        """Parse plain text into structured presentation content.

        Args:
            text: Input text to parse
            max_bullets: Maximum bullet points per slide before splitting
            max_words_per_bullet: Maximum words per bullet point

        Returns:
            ParsedPresentation with title and structured slides

        Examples:
            >>> parser = TextParser()
            >>> result = parser.parse("# Title\\n\\n## Section 1\\nContent here.")
            >>> result.title
            'Title'
        """
        if not text:
            return ParsedPresentation(
                title="Empty Presentation",
                raw_text="",
            )

        cleaned = clean_text(text)

        # Extract presentation title from first line or heading
        title = extract_title(cleaned)

        # Split text into sections
        sections = split_into_sections(cleaned)

        slides: list[SlideContent] = []

        # Add title slide
        slides.append(
            SlideContent(
                slide_type="title",
                title=title,
                subtitle="",
            )
        )

        # Process each section
        for idx, section in enumerate(sections, start=1):
            section_title = section["title"]
            bullets = section["bullets"]

            # If section has too many bullets, split across multiple slides
            if len(bullets) > max_bullets:
                # Split bullets into chunks
                for chunk_idx, i in enumerate(range(0, len(bullets), max_bullets)):
                    chunk_bullets = bullets[i : i + max_bullets]

                    # Add continuation indicator if not first chunk
                    chunk_title = section_title
                    if chunk_idx > 0:
                        chunk_title = f"{section_title} (cont.)"

                    slides.append(
                        SlideContent(
                            slide_type="content",
                            title=chunk_title,
                            bullets=chunk_bullets,
                            section_number=idx,
                        )
                    )
            else:
                # Single slide for this section
                slides.append(
                    SlideContent(
                        slide_type="content",
                        title=section_title,
                        bullets=bullets,
                        section_number=idx,
                    )
                )

        return ParsedPresentation(
            title=title,
            sections=slides,
            raw_text=cleaned,
        )

    def parse_file(
        self,
        file_path: str,
        **kwargs,
    ) -> ParsedPresentation:
        """Read a text file and parse it.

        Args:
            file_path: Path to text file
            **kwargs: Additional arguments passed to parse()

        Returns:
            ParsedPresentation from file content

        Raises:
            FileNotFoundError: If file doesn't exist
            IOError: If file cannot be read

        Examples:
            >>> parser = TextParser()
            >>> result = parser.parse_file("/path/to/document.txt")
            >>> result.title
            'Document Title'
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            # Fallback to latin-1 if UTF-8 fails
            text = path.read_text(encoding="latin-1")

        return self.parse(text, **kwargs)
