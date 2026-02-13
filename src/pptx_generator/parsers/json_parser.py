"""JSON parser for converting structured JSON into presentation content.

This module handles parsing of structured JSON input that explicitly defines
slide types, content, and layout information.
"""

from __future__ import annotations

import json
from pathlib import Path

from pptx_generator.parsers.models import ParsedPresentation, SlideContent


class JsonParser:
    """Parse structured JSON input into presentation content.

    The JsonParser accepts JSON documents with explicit slide definitions,
    allowing fine-grained control over slide types and content layout.

    Expected JSON format:
        {
            "title": "Presentation Title",
            "subtitle": "Optional subtitle",
            "author": "Author Name",
            "date": "2024-01-01",
            "slides": [
                {
                    "type": "content",
                    "title": "Slide Title",
                    "bullets": ["Point 1", "Point 2"]
                },
                {
                    "type": "chart",
                    "title": "Revenue Growth",
                    "chart_data": {
                        "labels": ["Q1", "Q2", "Q3"],
                        "values": [100, 150, 200],
                        "chart_type": "bar",
                        "series_name": "Revenue"
                    }
                },
                {
                    "type": "comparison",
                    "title": "Before vs After",
                    "left_title": "Before",
                    "left_bullets": ["Old approach", "Manual process"],
                    "right_title": "After",
                    "right_bullets": ["New approach", "Automated"]
                },
                {
                    "type": "timeline",
                    "title": "Project Timeline",
                    "events": [
                        {"label": "Q1", "description": "Planning"},
                        {"label": "Q2", "description": "Development"}
                    ]
                }
            ]
        }

    Examples:
        >>> parser = JsonParser()
        >>> data = {"title": "My Deck", "slides": [{"type": "content", "title": "Intro"}]}
        >>> result = parser.parse(data)
        >>> result.title
        'My Deck'
    """

    def parse(self, json_data: dict | str) -> ParsedPresentation:
        """Parse JSON (dict or string) into ParsedPresentation.

        Args:
            json_data: Dictionary or JSON string with presentation data

        Returns:
            ParsedPresentation with structured slides

        Raises:
            ValueError: If JSON is invalid or missing required fields
            json.JSONDecodeError: If string is not valid JSON

        Examples:
            >>> parser = JsonParser()
            >>> result = parser.parse('{"title": "Test", "slides": []}')
            >>> result.title
            'Test'
        """
        # Parse string to dict if needed
        if isinstance(json_data, str):
            try:
                data = json.loads(json_data)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON format: {e}") from e
        else:
            data = json_data

        if not isinstance(data, dict):
            raise ValueError("JSON data must be a dictionary")

        # Extract metadata
        title = data.get("title", "Untitled Presentation")
        subtitle = data.get("subtitle", "")
        author = data.get("author", "")
        date = data.get("date", "")
        metadata = data.get("metadata", {})

        # Parse slides
        slides_data = data.get("slides", [])
        if not isinstance(slides_data, list):
            raise ValueError("'slides' field must be a list")

        slides: list[SlideContent] = []

        for idx, slide_data in enumerate(slides_data):
            if not isinstance(slide_data, dict):
                raise ValueError(f"Slide {idx} must be a dictionary")

            try:
                slide = self._parse_slide(slide_data, idx + 1)
                slides.append(slide)
            except Exception as e:
                raise ValueError(f"Error parsing slide {idx}: {e}") from e

        return ParsedPresentation(
            title=title,
            subtitle=subtitle,
            author=author,
            date=date,
            sections=slides,
            metadata=metadata,
        )

    def _parse_slide(self, slide_data: dict, section_number: int) -> SlideContent:
        """Parse a single slide definition.

        Args:
            slide_data: Dictionary with slide content
            section_number: Slide number for ordering

        Returns:
            SlideContent object

        Raises:
            ValueError: If required fields are missing
        """
        slide_type = slide_data.get("type", "content")

        # Common fields
        common_fields = {
            "slide_type": slide_type,
            "title": slide_data.get("title", ""),
            "subtitle": slide_data.get("subtitle", ""),
            "notes": slide_data.get("notes", ""),
            "section_number": section_number,
        }

        # Type-specific fields
        if slide_type in ("content", "title", "agenda"):
            return SlideContent(
                **common_fields,
                bullets=slide_data.get("bullets", []),
            )

        elif slide_type == "comparison":
            return SlideContent(
                **common_fields,
                left_title=slide_data.get("left_title", ""),
                left_bullets=slide_data.get("left_bullets", []),
                right_title=slide_data.get("right_title", ""),
                right_bullets=slide_data.get("right_bullets", []),
            )

        elif slide_type == "chart":
            chart_data = slide_data.get("chart_data")
            if chart_data and not isinstance(chart_data, dict):
                raise ValueError("chart_data must be a dictionary")

            # Validate chart_data structure
            if chart_data:
                required_keys = {"labels", "values"}
                missing = required_keys - set(chart_data.keys())
                if missing:
                    raise ValueError(f"chart_data missing required keys: {missing}")

            return SlideContent(
                **common_fields,
                chart_data=chart_data,
            )

        elif slide_type == "timeline":
            events = slide_data.get("events", [])
            if not isinstance(events, list):
                raise ValueError("events must be a list")

            # Validate event structure
            for event in events:
                if not isinstance(event, dict):
                    raise ValueError("Each event must be a dictionary")
                if "label" not in event:
                    raise ValueError("Each event must have a 'label' field")

            return SlideContent(
                **common_fields,
                events=events,
            )

        elif slide_type == "diagram":
            nodes = slide_data.get("nodes", [])
            if not isinstance(nodes, list):
                raise ValueError("nodes must be a list")

            return SlideContent(
                **common_fields,
                nodes=nodes,
                diagram_type=slide_data.get("diagram_type", "flow"),
            )

        elif slide_type == "closing":
            return SlideContent(
                **common_fields,
                contact=slide_data.get("contact", ""),
                message=slide_data.get("message", ""),
            )

        elif slide_type == "section_divider":
            return SlideContent(**common_fields)

        else:
            # Unknown type, default to content slide
            return SlideContent(
                **common_fields,
                bullets=slide_data.get("bullets", []),
            )

    def parse_file(self, file_path: str) -> ParsedPresentation:
        """Read a JSON file and parse it.

        Args:
            file_path: Path to JSON file

        Returns:
            ParsedPresentation from file content

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If JSON is invalid
            json.JSONDecodeError: If file contains invalid JSON

        Examples:
            >>> parser = JsonParser()
            >>> result = parser.parse_file("/path/to/presentation.json")
            >>> result.title
            'Presentation Title'
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            # Fallback to latin-1 if UTF-8 fails
            content = path.read_text(encoding="latin-1")

        return self.parse(content)
