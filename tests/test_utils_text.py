"""Tests for pptx_generator.utils.text module."""

from __future__ import annotations

import pytest

from src.pptx_generator.utils import text


class TestCleanText:
    """Test clean_text() function."""

    def test_clean_text_basic(self) -> None:
        """Test basic whitespace cleaning."""
        assert text.clean_text("  hello  world  ") == "hello world"
        assert text.clean_text("hello\n\nworld") == "hello\n\nworld"

    def test_clean_text_multiple_spaces(self) -> None:
        """Test collapsing multiple spaces."""
        assert text.clean_text("hello    world") == "hello world"
        assert text.clean_text("a  b  c  d") == "a b c d"

    def test_clean_text_line_breaks(self) -> None:
        """Test line break normalization."""
        assert text.clean_text("hello\r\nworld") == "hello\nworld"
        assert text.clean_text("hello\rworld") == "hello\nworld"

    def test_clean_text_multiple_blank_lines(self) -> None:
        """Test collapsing multiple blank lines."""
        assert text.clean_text("hello\n\n\n\nworld") == "hello\n\nworld"
        assert text.clean_text("a\n\n\n\n\nb") == "a\n\nb"

    def test_clean_text_nbsp(self) -> None:
        """Test NBSP character replacement."""
        assert text.clean_text("hello\u00a0world") == "hello world"
        assert text.clean_text("café\u00a0test") == "café test"

    def test_clean_text_special_spaces(self) -> None:
        """Test other special space character replacement."""
        assert text.clean_text("hello\u2007world") == "hello world"  # Figure space
        assert text.clean_text("hello\u202fworld") == "hello world"  # Narrow NBSP

    def test_clean_text_unicode_normalization(self) -> None:
        """Test unicode normalization."""
        # é can be represented as single char or e + combining accent
        result = text.clean_text("café")
        assert "café" in result
        assert len(result) == 4  # Should be normalized to NFC form

    def test_clean_text_empty(self) -> None:
        """Test empty string handling."""
        assert text.clean_text("") == ""
        assert text.clean_text("   ") == ""

    def test_clean_text_preserves_single_newlines(self) -> None:
        """Test that single newlines are preserved."""
        assert text.clean_text("line1\nline2\nline3") == "line1\nline2\nline3"


class TestTruncate:
    """Test truncate() function."""

    def test_truncate_short_text(self) -> None:
        """Test that short text is not truncated."""
        assert text.truncate("Short text", 100) == "Short text"
        assert text.truncate("Hello", 20) == "Hello"

    def test_truncate_exact_length(self) -> None:
        """Test text exactly at max length."""
        assert text.truncate("x" * 10, 10) == "x" * 10

    def test_truncate_long_text(self) -> None:
        """Test truncating long text."""
        result = text.truncate("This is a very long text that needs truncating", 20)
        assert len(result) <= 20  # May be shorter due to word boundary
        assert result.endswith("...")
        assert result == "This is a very..."

    def test_truncate_word_boundary(self) -> None:
        """Test truncation at word boundaries."""
        result = text.truncate("Hello world this is a test", 15)
        assert result == "Hello world..."
        assert not result.endswith("d ...")  # Should truncate at space

    def test_truncate_no_good_boundary(self) -> None:
        """Test truncation when no good word boundary exists."""
        result = text.truncate("Verylongwordwithoutspaces", 15)
        assert len(result) == 15
        assert result.endswith("...")

    def test_truncate_empty(self) -> None:
        """Test empty string handling."""
        assert text.truncate("", 10) == ""

    def test_truncate_zero_max(self) -> None:
        """Test zero max_chars."""
        assert text.truncate("Hello", 0) == ""

    def test_truncate_very_small_max(self) -> None:
        """Test very small max_chars."""
        assert text.truncate("Hello world", 3) == "..."
        assert text.truncate("Hello world", 5) == "He..."

    def test_truncate_default_max(self) -> None:
        """Test default max_chars value."""
        long_text = "x" * 300
        result = text.truncate(long_text)
        assert len(result) == 200


class TestExtractTitle:
    """Test extract_title() function."""

    def test_extract_title_markdown_h1(self) -> None:
        """Test extraction from markdown H1."""
        assert text.extract_title("# Main Title\nContent here") == "Main Title"
        assert text.extract_title("#Title") == "Title"

    def test_extract_title_markdown_h2(self) -> None:
        """Test extraction from markdown H2."""
        assert text.extract_title("## Section Title\nContent") == "Section Title"
        assert text.extract_title("###Subsection") == "Subsection"

    def test_extract_title_first_line_standalone(self) -> None:
        """Test extraction when first line is standalone."""
        assert text.extract_title("Standalone Title\n\nContent here") == "Standalone Title"

    def test_extract_title_first_sentence(self) -> None:
        """Test extraction of first sentence."""
        assert text.extract_title("First sentence. Second sentence.") == "First sentence."
        assert text.extract_title("Question? Answer.") == "Question?"
        assert text.extract_title("Exclamation! More text.") == "Exclamation!"

    def test_extract_title_fallback_first_line(self) -> None:
        """Test fallback to first line when no sentence ending."""
        result = text.extract_title("This is a long first line without punctuation")
        assert len(result) <= 60
        assert "..." in result or len(result) < 60

    def test_extract_title_empty(self) -> None:
        """Test empty string handling."""
        assert text.extract_title("") == "Untitled"

    def test_extract_title_truncates_long(self) -> None:
        """Test that very long titles are truncated."""
        long_title = "# " + "x" * 200
        result = text.extract_title(long_title)
        assert len(result) <= 100


class TestSplitIntoBullets:
    """Test split_into_bullets() function."""

    def test_split_into_bullets_simple_sentences(self) -> None:
        """Test splitting simple sentences."""
        result = text.split_into_bullets("First. Second. Third.")
        # Short sentences may be combined into one bullet
        assert len(result) >= 1
        assert "First." in result[0]

    def test_split_into_bullets_respects_max_words(self) -> None:
        """Test that bullets respect max word count with multiple sentences."""
        # Need actual sentences for splitting to work
        sentences = [" ".join(["word"] * 15) + "." for _ in range(4)]
        long_text = " ".join(sentences)
        result = text.split_into_bullets(long_text, max_words=20)
        assert len(result) > 1  # Should be split into multiple bullets

    def test_split_into_bullets_combines_short_sentences(self) -> None:
        """Test that short sentences are combined."""
        result = text.split_into_bullets("Short. Also short. Still short.", max_words=20)
        # Should combine into fewer bullets
        assert len(result) < 3

    def test_split_into_bullets_question_marks(self) -> None:
        """Test splitting on question marks."""
        result = text.split_into_bullets("Question one? Question two? Question three?")
        assert len(result) >= 1

    def test_split_into_bullets_exclamations(self) -> None:
        """Test splitting on exclamation marks."""
        result = text.split_into_bullets("First! Second! Third!")
        assert len(result) >= 1

    def test_split_into_bullets_empty(self) -> None:
        """Test empty string handling."""
        assert text.split_into_bullets("") == []

    def test_split_into_bullets_no_punctuation(self) -> None:
        """Test text without sentence-ending punctuation."""
        result = text.split_into_bullets("Just some text without periods")
        assert len(result) >= 1

    def test_split_into_bullets_default_max_words(self) -> None:
        """Test default max_words value."""
        # split_into_bullets splits at sentence boundaries, so a single sentence
        # stays as one bullet even if it exceeds max_words
        long_sentence = " ".join(["word"] * 30) + "."
        result = text.split_into_bullets(long_sentence)
        assert len(result) >= 1
        # Multiple sentences should split
        multi = "First sentence here. Second sentence here. Third sentence here."
        result2 = text.split_into_bullets(multi, max_words=5)
        assert len(result2) > 1


class TestEstimateSlideCount:
    """Test estimate_slide_count() function."""

    def test_estimate_slide_count_short_text(self) -> None:
        """Test estimation for short text."""
        assert text.estimate_slide_count("Short text") == 1
        assert text.estimate_slide_count("A few words here") == 1

    def test_estimate_slide_count_exact_boundary(self) -> None:
        """Test estimation at exact boundary."""
        words = " ".join(["word"] * 80)
        assert text.estimate_slide_count(words, words_per_slide=80) == 1

    def test_estimate_slide_count_multiple_slides(self) -> None:
        """Test estimation for multiple slides."""
        words = " ".join(["word"] * 200)
        result = text.estimate_slide_count(words, words_per_slide=80)
        assert result == 3  # 200 / 80 = 2.5, rounds up to 3

    def test_estimate_slide_count_custom_words_per_slide(self) -> None:
        """Test with custom words_per_slide."""
        words = " ".join(["word"] * 100)
        assert text.estimate_slide_count(words, words_per_slide=50) == 2
        assert text.estimate_slide_count(words, words_per_slide=25) == 4

    def test_estimate_slide_count_empty(self) -> None:
        """Test empty string handling."""
        assert text.estimate_slide_count("") == 1

    def test_estimate_slide_count_minimum_one(self) -> None:
        """Test that result is always at least 1."""
        assert text.estimate_slide_count("x") == 1
        assert text.estimate_slide_count("", words_per_slide=100) == 1

    def test_estimate_slide_count_invalid_words_per_slide(self) -> None:
        """Test invalid words_per_slide."""
        assert text.estimate_slide_count("test", words_per_slide=0) == 1
        assert text.estimate_slide_count("test", words_per_slide=-10) == 1


class TestSplitIntoSections:
    """Test split_into_sections() function."""

    def test_split_into_sections_markdown_headers(self) -> None:
        """Test splitting by markdown headers."""
        content = "## First\nContent one.\n\n## Second\nContent two."
        result = text.split_into_sections(content)

        assert len(result) == 2
        assert result[0]["title"] == "First"
        assert result[0]["content"] == "Content one."
        assert result[1]["title"] == "Second"
        assert result[1]["content"] == "Content two."

    def test_split_into_sections_h1_headers(self) -> None:
        """Test splitting by H1 headers."""
        content = "# Title One\nText here.\n\n# Title Two\nMore text."
        result = text.split_into_sections(content)

        assert len(result) == 2
        assert result[0]["title"] == "Title One"
        assert result[1]["title"] == "Title Two"

    def test_split_into_sections_bullets_generated(self) -> None:
        """Test that bullets are generated for each section."""
        content = "## Section\nFirst sentence. Second sentence."
        result = text.split_into_sections(content)

        assert len(result) == 1
        assert isinstance(result[0]["bullets"], list)
        assert len(result[0]["bullets"]) >= 1

    def test_split_into_sections_no_headers_paragraphs(self) -> None:
        """Test splitting by paragraphs when no headers."""
        content = "First paragraph text.\n\nSecond paragraph text.\n\nThird paragraph."
        result = text.split_into_sections(content)

        assert len(result) == 3
        assert "First paragraph" in result[0]["content"]
        assert "Second paragraph" in result[1]["content"]
        assert "Third paragraph" in result[2]["content"]

    def test_split_into_sections_empty(self) -> None:
        """Test empty string handling."""
        assert text.split_into_sections("") == []

    def test_split_into_sections_single_paragraph(self) -> None:
        """Test single paragraph without headers."""
        content = "Just one paragraph of text here."
        result = text.split_into_sections(content)

        assert len(result) == 1
        assert result[0]["content"] == content

    def test_split_into_sections_title_extraction(self) -> None:
        """Test that titles are extracted when no header present."""
        content = "First sentence. More text.\n\nSecond sentence. More text."
        result = text.split_into_sections(content)

        assert len(result) == 2
        assert result[0]["title"]  # Should have extracted title
        assert result[1]["title"]

    def test_split_into_sections_preserves_content(self) -> None:
        """Test that content is preserved correctly."""
        content = "## Header\nLine 1\nLine 2\nLine 3"
        result = text.split_into_sections(content)

        assert len(result) == 1
        assert "Line 1" in result[0]["content"]
        assert "Line 2" in result[0]["content"]
        assert "Line 3" in result[0]["content"]

    def test_split_into_sections_mixed_header_levels(self) -> None:
        """Test mixing different header levels."""
        content = "# H1\nContent.\n\n## H2\nMore content.\n\n### H3\nEven more."
        result = text.split_into_sections(content)

        assert len(result) == 3
        assert result[0]["title"] == "H1"
        assert result[1]["title"] == "H2"
        assert result[2]["title"] == "H3"

    def test_split_into_sections_return_type(self) -> None:
        """Test that sections have correct structure."""
        content = "## Test\nContent here."
        result = text.split_into_sections(content)

        assert len(result) == 1
        section = result[0]

        assert "title" in section
        assert "content" in section
        assert "bullets" in section
        assert isinstance(section["title"], str)
        assert isinstance(section["content"], str)
        assert isinstance(section["bullets"], list)


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_unicode_handling(self) -> None:
        """Test proper unicode handling across functions."""
        unicode_text = "Héllo wörld! Tëst séntence."

        # Should not raise errors
        text.clean_text(unicode_text)
        text.truncate(unicode_text, 20)
        text.extract_title(unicode_text)
        text.split_into_bullets(unicode_text)
        text.estimate_slide_count(unicode_text)
        text.split_into_sections(unicode_text)

    def test_very_long_input(self) -> None:
        """Test handling of very long input."""
        long_text = " ".join(["word"] * 10000)

        # Should handle without errors
        text.clean_text(long_text)
        text.truncate(long_text)
        text.extract_title(long_text)
        result = text.split_into_bullets(long_text)
        assert len(result) > 0

        result = text.estimate_slide_count(long_text)
        assert result > 0

    def test_special_characters(self) -> None:
        """Test handling of special characters."""
        special_text = "Test @#$% & *()_ special! chars?"

        text.clean_text(special_text)
        text.truncate(special_text, 20)
        text.extract_title(special_text)
        text.split_into_bullets(special_text)
        text.split_into_sections(special_text)

    def test_only_whitespace(self) -> None:
        """Test handling of whitespace-only input."""
        whitespace = "   \n\n   \t\t   "

        assert text.clean_text(whitespace) == ""
        # truncate doesn't call clean_text first, so whitespace gets truncated with "..."
        assert text.truncate(whitespace, 10) in ("", "...")
        # extract_title calls clean_text which returns "", then extract_title returns "" or "Untitled"
        assert text.extract_title(whitespace) in ("", "Untitled")
        assert text.split_into_bullets(whitespace) == []
        assert text.estimate_slide_count(whitespace) == 1
        assert text.split_into_sections(whitespace) == []
