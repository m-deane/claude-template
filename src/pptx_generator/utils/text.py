"""Text processing utilities for PowerPoint content generation.

This module provides functions for splitting, cleaning, and analyzing text
content for optimal presentation in PowerPoint slides.
"""

from __future__ import annotations

import re
import unicodedata
from typing import TypedDict


class Section(TypedDict):
    """Represents a text section with title and content."""

    title: str
    content: str
    bullets: list[str]


__all__ = [
    "split_into_bullets",
    "truncate",
    "extract_title",
    "estimate_slide_count",
    "clean_text",
    "split_into_sections",
]


def clean_text(text: str) -> str:
    """Strip extra whitespace and normalize unicode characters.

    Performs the following operations:
    - Normalizes unicode to NFC form
    - Converts NBSP and other special spaces to regular spaces
    - Collapses multiple spaces to single space
    - Removes leading/trailing whitespace
    - Normalizes line breaks to \n

    Args:
        text: Input text to clean

    Returns:
        Cleaned text with normalized whitespace

    Examples:
        >>> clean_text("  Hello    World  \\n\\n  Test  ")
        'Hello World\\n\\nTest'
        >>> clean_text("café\\u00a0test")  # NBSP character
        'café test'
    """
    if not text:
        return ""

    # Normalize unicode to NFC form (canonical composition)
    text = unicodedata.normalize("NFC", text)

    # Replace various types of spaces with regular space
    text = text.replace("\u00a0", " ")  # NBSP
    text = text.replace("\u2007", " ")  # Figure space
    text = text.replace("\u202f", " ")  # Narrow NBSP

    # Normalize line breaks
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Collapse multiple spaces (but preserve line breaks)
    lines = text.split("\n")
    lines = [re.sub(r" +", " ", line.strip()) for line in lines]

    # Join and collapse multiple blank lines to max 2 newlines
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def truncate(text: str, max_chars: int = 200) -> str:
    """Truncate text to maximum character length with ellipsis.

    Intelligently truncates at word boundaries when possible.

    Args:
        text: Text to truncate
        max_chars: Maximum character length (including ellipsis)

    Returns:
        Truncated text with "..." appended if truncated

    Examples:
        >>> truncate("This is a short text", 100)
        'This is a short text'
        >>> truncate("This is a very long text that needs truncating", 20)
        'This is a very...'
    """
    if not text or max_chars <= 0:
        return ""

    if len(text) <= max_chars:
        return text

    # Reserve space for ellipsis
    truncate_at = max_chars - 3

    if truncate_at <= 0:
        return "..."

    # Try to truncate at word boundary
    truncated = text[:truncate_at]
    last_space = truncated.rfind(" ")

    if last_space > truncate_at // 2:  # Only use word boundary if it's past halfway
        truncated = truncated[:last_space]

    return truncated.rstrip() + "..."


def extract_title(text: str) -> str:
    """Extract a title from text by finding first heading or sentence.

    Extraction priority:
    1. Markdown heading (# or ##)
    2. First line if followed by blank line
    3. First sentence (up to period, question mark, or exclamation)
    4. First 60 characters

    Args:
        text: Input text

    Returns:
        Extracted title, cleaned and truncated to 100 chars

    Examples:
        >>> extract_title("# Main Title\\nContent here")
        'Main Title'
        >>> extract_title("First sentence. Second sentence.")
        'First sentence'
    """
    if not text:
        return "Untitled"

    text = clean_text(text)
    lines = text.split("\n")

    # Check for markdown heading
    if lines[0].startswith("#"):
        title = lines[0].lstrip("#").strip()
        return truncate(title, 100)

    # Check if first line is standalone (followed by blank line)
    if len(lines) > 1 and not lines[1].strip():
        return truncate(lines[0], 100)

    # Try to extract first sentence
    first_sentence_match = re.match(r"^([^.!?]+[.!?])", text)
    if first_sentence_match:
        return truncate(first_sentence_match.group(1).strip(), 100)

    # Fall back to first line or truncated text
    first_line = lines[0] if lines else text
    return truncate(first_line, 60)


def split_into_bullets(text: str, max_words: int = 20) -> list[str]:
    """Split text into bullet points, breaking at sentence boundaries.

    Args:
        text: Input text to split
        max_words: Maximum words per bullet point

    Returns:
        List of bullet point strings

    Examples:
        >>> split_into_bullets("First point. Second point. Third point.")
        ['First point.', 'Second point.', 'Third point.']
    """
    if not text:
        return []

    text = clean_text(text)

    # Split into sentences using regex
    sentence_pattern = r"(?<=[.!?])\s+"
    sentences = re.split(sentence_pattern, text)
    sentences = [s.strip() for s in sentences if s.strip()]

    bullets: list[str] = []
    current_bullet: list[str] = []
    current_word_count = 0

    for sentence in sentences:
        sentence_words = len(sentence.split())

        # If adding this sentence exceeds max_words and we have content, start new bullet
        if current_bullet and current_word_count + sentence_words > max_words:
            bullets.append(" ".join(current_bullet))
            current_bullet = [sentence]
            current_word_count = sentence_words
        else:
            current_bullet.append(sentence)
            current_word_count += sentence_words

    # Add remaining content
    if current_bullet:
        bullets.append(" ".join(current_bullet))

    return bullets


def estimate_slide_count(text: str, words_per_slide: int = 80) -> int:
    """Estimate number of slides needed for given text.

    Args:
        text: Input text
        words_per_slide: Average words per slide (default: 80)

    Returns:
        Estimated number of slides (minimum 1)

    Examples:
        >>> estimate_slide_count("Short text")
        1
        >>> estimate_slide_count(" ".join(["word"] * 200), words_per_slide=80)
        3
    """
    if not text or words_per_slide <= 0:
        return 1

    text = clean_text(text)
    word_count = len(text.split())

    if word_count == 0:
        return 1

    # Round up to ensure we have enough slides
    return max(1, (word_count + words_per_slide - 1) // words_per_slide)


def split_into_sections(text: str) -> list[Section]:
    """Split text into sections based on headers or paragraphs.

    Sections are identified by:
    1. Markdown headers (## or #)
    2. Blank-line separated paragraphs if no headers exist

    Args:
        text: Input text to split

    Returns:
        List of section dictionaries with keys: title, content, bullets

    Examples:
        >>> sections = split_into_sections("## Title\\nContent here.\\n\\n## Title 2\\nMore content.")
        >>> len(sections)
        2
        >>> sections[0]['title']
        'Title'
    """
    if not text:
        return []

    text = clean_text(text)
    lines = text.split("\n")

    sections: list[Section] = []
    current_title = ""
    current_content: list[str] = []

    def finalize_section() -> None:
        """Helper to finalize and add current section."""
        if current_content or current_title:
            content_text = "\n".join(current_content).strip()
            sections.append(
                {
                    "title": current_title or extract_title(content_text),
                    "content": content_text,
                    "bullets": split_into_bullets(content_text) if content_text else [],
                }
            )

    # Check if document has markdown headers
    has_headers = any(line.strip().startswith("#") for line in lines)

    if has_headers:
        # Split by markdown headers
        for line in lines:
            stripped = line.strip()

            if stripped.startswith("#"):
                # Finalize previous section
                finalize_section()

                # Start new section
                current_title = stripped.lstrip("#").strip()
                current_content = []
            else:
                if stripped:  # Skip blank lines at section start
                    current_content.append(line)
                elif current_content:  # Preserve blank lines within content
                    current_content.append(line)

        # Finalize last section
        finalize_section()

    else:
        # Split by blank-line separated paragraphs
        paragraph: list[str] = []

        for line in lines:
            if line.strip():
                paragraph.append(line)
            elif paragraph:
                # End of paragraph
                paragraph_text = "\n".join(paragraph).strip()
                sections.append(
                    {
                        "title": extract_title(paragraph_text),
                        "content": paragraph_text,
                        "bullets": split_into_bullets(paragraph_text),
                    }
                )
                paragraph = []

        # Add last paragraph
        if paragraph:
            paragraph_text = "\n".join(paragraph).strip()
            sections.append(
                {
                    "title": extract_title(paragraph_text),
                    "content": paragraph_text,
                    "bullets": split_into_bullets(paragraph_text),
                }
            )

    return sections
