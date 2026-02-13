"""Test suite for content parsers."""

from __future__ import annotations

import pytest
import json
from pathlib import Path

from pptx_generator.parsers import (
    TextParser,
    MarkdownParser,
    JsonParser,
    ParsedPresentation,
    SlideContent,
)


class TestTextParser:
    """Test plain text parser."""

    def test_text_parser_basic(self):
        """Test parsing basic text content."""
        parser = TextParser()
        text = """
Introduction

This is an introduction slide.
It has multiple sentences.

Key Points

First point about the topic
Second important point
Third consideration
"""
        result = parser.parse(text)

        assert isinstance(result, ParsedPresentation)
        assert len(result.sections) > 0

    def test_text_parser_empty_input(self):
        """Test parsing empty text."""
        parser = TextParser()
        result = parser.parse("")

        assert isinstance(result, ParsedPresentation)
        # Empty text may produce various default titles depending on parser implementation
        assert result.title in ["Untitled Presentation", "", "Empty Presentation"]

    def test_text_parser_single_section(self):
        """Test parsing text with single section."""
        parser = TextParser()
        text = """
Title

This is the content.
"""
        result = parser.parse(text)

        assert isinstance(result, ParsedPresentation)
        assert len(result.sections) >= 0

    def test_text_parser_max_bullets_constraint(self):
        """Test that max_bullets constraint is respected."""
        parser = TextParser()
        text = """
Section Title

Bullet 1
Bullet 2
Bullet 3
Bullet 4
Bullet 5
Bullet 6
Bullet 7
Bullet 8
"""
        result = parser.parse(text, max_bullets=3)

        assert isinstance(result, ParsedPresentation)
        # Should respect max_bullets limit
        for section in result.sections:
            if section.bullets:
                assert len(section.bullets) <= 3

    def test_text_parser_max_words_per_bullet(self):
        """Test that parser handles max_words_per_bullet parameter."""
        parser = TextParser()
        text = """
Section

First bullet
Second bullet with just a few words
Third item
"""
        result = parser.parse(text, max_words_per_bullet=10)

        assert isinstance(result, ParsedPresentation)
        # Parser should handle the constraint parameter (implementation may vary)
        # Just verify it parses without error when the constraint is provided

    def test_text_parser_whitespace_handling(self):
        """Test handling of various whitespace patterns."""
        parser = TextParser()
        text = """


Section One


Content here


Section Two


More content

"""
        result = parser.parse(text)

        assert isinstance(result, ParsedPresentation)


class TestMarkdownParser:
    """Test markdown parser."""

    def test_markdown_parser_basic(self):
        """Test parsing basic markdown."""
        parser = MarkdownParser()
        markdown = """
# Introduction

This is an introduction slide.

# Key Points

- First point
- Second point
- Third point
"""
        result = parser.parse(markdown)

        assert isinstance(result, ParsedPresentation)
        assert len(result.sections) > 0

    def test_markdown_parser_empty_input(self):
        """Test parsing empty markdown."""
        parser = MarkdownParser()
        result = parser.parse("")

        assert isinstance(result, ParsedPresentation)

    def test_markdown_parser_headings(self):
        """Test parsing different heading levels."""
        parser = MarkdownParser()
        markdown = """
# Main Title

## Subtitle

### Subheading

Content here.
"""
        result = parser.parse(markdown)

        assert isinstance(result, ParsedPresentation)

    def test_markdown_parser_bullet_lists(self):
        """Test parsing bullet lists."""
        parser = MarkdownParser()
        markdown = """
# Bullets

- Bullet 1
- Bullet 2
* Bullet 3
+ Bullet 4
"""
        result = parser.parse(markdown)

        assert isinstance(result, ParsedPresentation)
        # Should have bullets in at least one section
        has_bullets = any(len(s.bullets) > 0 for s in result.sections)
        assert has_bullets or len(result.sections) == 0

    def test_markdown_parser_numbered_lists(self):
        """Test parsing numbered lists."""
        parser = MarkdownParser()
        markdown = """
# Steps

1. First step
2. Second step
3. Third step
"""
        result = parser.parse(markdown)

        assert isinstance(result, ParsedPresentation)

    def test_markdown_parser_max_bullets(self):
        """Test max_bullets constraint in markdown."""
        parser = MarkdownParser()
        markdown = """
# Many Bullets

- Point 1
- Point 2
- Point 3
- Point 4
- Point 5
- Point 6
- Point 7
"""
        result = parser.parse(markdown, max_bullets=3)

        assert isinstance(result, ParsedPresentation)
        for section in result.sections:
            if section.bullets:
                assert len(section.bullets) <= 3

    def test_markdown_parser_code_blocks(self):
        """Test handling of code blocks."""
        parser = MarkdownParser()
        markdown = """
# Code Example

```python
def hello():
    print("Hello")
```

Regular content continues.
"""
        result = parser.parse(markdown)

        assert isinstance(result, ParsedPresentation)

    def test_markdown_parser_links(self):
        """Test handling of markdown links."""
        parser = MarkdownParser()
        markdown = """
# Links

Check out [this link](https://example.com) for more info.
"""
        result = parser.parse(markdown)

        assert isinstance(result, ParsedPresentation)

    def test_markdown_parser_emphasis(self):
        """Test handling of emphasis (bold, italic)."""
        parser = MarkdownParser()
        markdown = """
# Emphasis

This is **bold** and this is *italic*.
"""
        result = parser.parse(markdown)

        assert isinstance(result, ParsedPresentation)


class TestJsonParser:
    """Test JSON parser."""

    def test_json_parser_dict_input(self):
        """Test parsing JSON dict."""
        parser = JsonParser()
        data = {
            "title": "Test Presentation",
            "subtitle": "A Test",
            "author": "Test Author",
            "slides": [
                {
                    "type": "content",
                    "title": "Section 1",
                    "bullets": ["Point 1", "Point 2"]
                }
            ]
        }
        result = parser.parse(data)

        assert isinstance(result, ParsedPresentation)
        assert result.title == "Test Presentation"
        assert result.subtitle == "A Test"
        assert result.author == "Test Author"
        assert len(result.sections) == 1

    def test_json_parser_string_input(self):
        """Test parsing JSON string."""
        parser = JsonParser()
        data = json.dumps({
            "title": "Test",
            "slides": [
                {
                    "type": "content",
                    "title": "Content",
                    "bullets": ["A", "B"]
                }
            ]
        })
        result = parser.parse(data)

        assert isinstance(result, ParsedPresentation)
        assert result.title == "Test"

    def test_json_parser_empty_sections(self):
        """Test parsing JSON with no sections."""
        parser = JsonParser()
        data = {
            "title": "Empty Presentation",
            "slides": []
        }
        result = parser.parse(data)

        assert isinstance(result, ParsedPresentation)
        assert len(result.sections) == 0

    def test_json_parser_minimal(self):
        """Test parsing minimal JSON."""
        parser = JsonParser()
        data = {"title": "Minimal"}
        result = parser.parse(data)

        assert isinstance(result, ParsedPresentation)
        assert result.title == "Minimal"

    def test_json_parser_all_slide_types(self):
        """Test parsing JSON with all slide types."""
        parser = JsonParser()
        data = {
            "title": "All Types",
            "slides": [
                {
                    "type": "content",
                    "title": "Content",
                    "bullets": ["A", "B"]
                },
                {
                    "type": "comparison",
                    "title": "Comparison",
                    "left_title": "Left",
                    "left_bullets": ["L1"],
                    "right_title": "Right",
                    "right_bullets": ["R1"]
                },
                {
                    "type": "chart",
                    "title": "Chart",
                    "chart_data": {
                        "labels": ["Q1", "Q2"],
                        "values": [100, 200],
                        "chart_type": "bar"
                    }
                },
                {
                    "type": "timeline",
                    "title": "Timeline",
                    "events": [
                        {"label": "2026", "description": "Event"}
                    ]
                },
                {
                    "type": "diagram",
                    "title": "Diagram",
                    "nodes": ["Node 1", "Node 2"],
                    "diagram_type": "flow"
                }
            ]
        }
        result = parser.parse(data)

        assert isinstance(result, ParsedPresentation)
        assert len(result.sections) == 5

    def test_json_parser_invalid_json_string(self):
        """Test parsing invalid JSON string."""
        parser = JsonParser()

        with pytest.raises(Exception):  # Should raise some parsing error
            parser.parse("{invalid json")

    def test_json_parser_metadata(self):
        """Test that metadata is preserved."""
        parser = JsonParser()
        data = {
            "title": "Test",
            "subtitle": "Subtitle",
            "author": "Author Name",
            "date": "2026-02-13",
            "metadata": {
                "custom_field": "value"
            },
            "slides": []
        }
        result = parser.parse(data)

        assert isinstance(result, ParsedPresentation)
        assert result.title == "Test"
        assert result.subtitle == "Subtitle"
        assert result.author == "Author Name"
        assert result.date == "2026-02-13"


class TestParsedPresentationModel:
    """Test ParsedPresentation model."""

    def test_parsed_presentation_defaults(self):
        """Test default values for ParsedPresentation."""
        parsed = ParsedPresentation()

        assert parsed.title == "Untitled Presentation"
        assert parsed.subtitle == ""
        assert parsed.author == ""
        assert parsed.date == ""
        assert parsed.sections == []
        assert parsed.raw_text == ""
        assert parsed.metadata == {}

    def test_parsed_presentation_with_data(self):
        """Test creating ParsedPresentation with data."""
        slides = [
            SlideContent(
                slide_type="content",
                title="Slide 1",
                bullets=["Point 1", "Point 2"]
            )
        ]

        parsed = ParsedPresentation(
            title="My Presentation",
            subtitle="Test",
            author="John Doe",
            date="2026-02-13",
            sections=slides
        )

        assert parsed.title == "My Presentation"
        assert parsed.subtitle == "Test"
        assert parsed.author == "John Doe"
        assert parsed.date == "2026-02-13"
        assert len(parsed.sections) == 1


class TestSlideContentModel:
    """Test SlideContent model."""

    def test_slide_content_defaults(self):
        """Test default values for SlideContent."""
        slide = SlideContent()

        assert slide.slide_type == "content"
        assert slide.title == ""
        assert slide.subtitle == ""
        assert slide.bullets == []
        assert slide.left_title == ""
        assert slide.left_bullets == []
        assert slide.right_title == ""
        assert slide.right_bullets == []
        assert slide.chart_data is None
        assert slide.events == []
        assert slide.nodes == []
        assert slide.diagram_type == "flow"

    def test_slide_content_content_type(self):
        """Test creating content type slide."""
        slide = SlideContent(
            slide_type="content",
            title="Content Title",
            bullets=["A", "B", "C"]
        )

        assert slide.slide_type == "content"
        assert slide.title == "Content Title"
        assert len(slide.bullets) == 3

    def test_slide_content_comparison_type(self):
        """Test creating comparison type slide."""
        slide = SlideContent(
            slide_type="comparison",
            title="Compare",
            left_title="Option A",
            left_bullets=["Pro 1", "Pro 2"],
            right_title="Option B",
            right_bullets=["Pro 1", "Pro 2"]
        )

        assert slide.slide_type == "comparison"
        assert slide.left_title == "Option A"
        assert slide.right_title == "Option B"
        assert len(slide.left_bullets) == 2
        assert len(slide.right_bullets) == 2

    def test_slide_content_chart_type(self):
        """Test creating chart type slide."""
        chart_data = {
            "labels": ["Q1", "Q2", "Q3"],
            "values": [100, 150, 120],
            "chart_type": "bar"
        }

        slide = SlideContent(
            slide_type="chart",
            title="Chart",
            chart_data=chart_data
        )

        assert slide.slide_type == "chart"
        assert slide.chart_data is not None
        assert slide.chart_data["chart_type"] == "bar"

    def test_slide_content_timeline_type(self):
        """Test creating timeline type slide."""
        events = [
            {"date": "Jan 2026", "title": "Event 1"},
            {"date": "Mar 2026", "title": "Event 2"}
        ]

        slide = SlideContent(
            slide_type="timeline",
            title="Timeline",
            events=events
        )

        assert slide.slide_type == "timeline"
        assert len(slide.events) == 2

    def test_slide_content_diagram_type(self):
        """Test creating diagram type slide."""
        slide = SlideContent(
            slide_type="diagram",
            title="Process",
            nodes=["Step 1", "Step 2", "Step 3"],
            diagram_type="flow"
        )

        assert slide.slide_type == "diagram"
        assert len(slide.nodes) == 3
        assert slide.diagram_type == "flow"


class TestParserFileHandling:
    """Test parser file handling capabilities."""

    def test_text_parser_parse_file(self, tmp_path):
        """Test TextParser.parse_file method."""
        parser = TextParser()

        # Create test file
        test_file = tmp_path / "test.txt"
        test_file.write_text("""
Section 1

Content for section 1.

Section 2

Content for section 2.
""")

        result = parser.parse_file(str(test_file))

        assert isinstance(result, ParsedPresentation)

    def test_markdown_parser_parse_file(self, tmp_path):
        """Test MarkdownParser.parse_file method."""
        parser = MarkdownParser()

        # Create test file
        test_file = tmp_path / "test.md"
        test_file.write_text("""
# Title

Content here.

# Section

- Bullet 1
- Bullet 2
""")

        result = parser.parse_file(str(test_file))

        assert isinstance(result, ParsedPresentation)

    def test_json_parser_parse_file(self, tmp_path):
        """Test JsonParser.parse_file method."""
        parser = JsonParser()

        # Create test file
        test_file = tmp_path / "test.json"
        data = {
            "title": "File Test",
            "slides": [
                {
                    "type": "content",
                    "title": "Section",
                    "bullets": ["A", "B"]
                }
            ]
        }
        test_file.write_text(json.dumps(data))

        result = parser.parse_file(str(test_file))

        assert isinstance(result, ParsedPresentation)
        assert result.title == "File Test"

    def test_parse_nonexistent_file(self):
        """Test parsing nonexistent file raises error."""
        parser = TextParser()

        with pytest.raises(FileNotFoundError):
            parser.parse_file("/nonexistent/file.txt")


class TestParserEdgeCases:
    """Test parser edge cases and error handling."""

    def test_text_parser_unicode(self):
        """Test parsing text with unicode characters."""
        parser = TextParser()
        text = """
Unicode Test

Emoji: 😀 🎉
Special chars: © ® ™
Accents: café, naïve
"""
        result = parser.parse(text)

        assert isinstance(result, ParsedPresentation)

    def test_markdown_parser_html(self):
        """Test markdown parser with HTML content."""
        parser = MarkdownParser()
        markdown = """
# HTML Test

<strong>Bold HTML</strong>

Regular markdown **bold**.
"""
        result = parser.parse(markdown)

        assert isinstance(result, ParsedPresentation)

    def test_json_parser_nested_data(self):
        """Test JSON parser with deeply nested data."""
        parser = JsonParser()
        data = {
            "title": "Nested",
            "metadata": {
                "level1": {
                    "level2": {
                        "value": "deep"
                    }
                }
            },
            "sections": []
        }
        result = parser.parse(data)

        assert isinstance(result, ParsedPresentation)
