from __future__ import annotations

from pydantic import BaseModel, Field, field_validator

from .colors import PALETTES
from .typography import FONT_STACKS


class SlideConfig(BaseModel):
    """Physical slide dimensions and layout configuration.

    Standard widescreen (16:9) dimensions:
    - Width: 13.333 inches (33.867 cm)
    - Height: 7.5 inches (19.05 cm)
    """

    width_inches: float = Field(
        default=13.333,
        description="Slide width in inches (16:9 widescreen)",
        gt=0
    )
    height_inches: float = Field(
        default=7.5,
        description="Slide height in inches (16:9 widescreen)",
        gt=0
    )
    margin_inches: float = Field(
        default=0.6,
        description="Margin around slide edges in inches",
        ge=0
    )
    content_area_ratio: float = Field(
        default=0.85,
        description="Ratio of slide area available for content (0-1)",
        gt=0,
        le=1
    )


class PresentationConfig(BaseModel):
    """Complete presentation configuration.

    Combines metadata, layout, styling, and behavioral settings.
    """

    # Metadata
    title: str = Field(..., description="Presentation title")
    subtitle: str = Field(default="", description="Presentation subtitle")
    author: str = Field(default="", description="Author name")
    date: str = Field(default="", description="Presentation date")

    # Layout
    slide_config: SlideConfig = Field(
        default_factory=SlideConfig,
        description="Slide dimensions and layout"
    )

    # Styling
    palette_name: str = Field(
        default="corporate",
        description="Color palette identifier"
    )
    font_stack_name: str = Field(
        default="professional",
        description="Typography stack identifier"
    )
    theme_name: str = Field(
        default="corporate",
        description="Overall theme identifier"
    )
    preset_name: str = Field(
        default="executive",
        description="Preset configuration name"
    )

    # Content limits
    max_bullets_per_slide: int = Field(
        default=6,
        description="Maximum bullet points per slide",
        gt=0,
        le=10
    )
    max_words_per_bullet: int = Field(
        default=20,
        description="Maximum words per bullet point",
        gt=0,
        le=50
    )

    # Features
    include_slide_numbers: bool = Field(
        default=True,
        description="Show slide numbers in footer"
    )
    include_agenda: bool = Field(
        default=True,
        description="Generate agenda/table of contents slide"
    )
    include_section_dividers: bool = Field(
        default=True,
        description="Insert section divider slides"
    )

    @field_validator('palette_name')
    @classmethod
    def validate_palette_name(cls, v: str) -> str:
        """Validate that palette_name exists in PALETTES.

        Args:
            v: Palette name to validate

        Returns:
            Validated palette name

        Raises:
            ValueError: If palette name not found in PALETTES
        """
        if v not in PALETTES:
            available = ', '.join(sorted(PALETTES.keys()))
            raise ValueError(
                f"Invalid palette_name '{v}'. "
                f"Available palettes: {available}"
            )
        return v

    @field_validator('font_stack_name')
    @classmethod
    def validate_font_stack_name(cls, v: str) -> str:
        """Validate that font_stack_name exists in FONT_STACKS.

        Args:
            v: Font stack name to validate

        Returns:
            Validated font stack name

        Raises:
            ValueError: If font stack name not found in FONT_STACKS
        """
        if v not in FONT_STACKS:
            available = ', '.join(sorted(FONT_STACKS.keys()))
            raise ValueError(
                f"Invalid font_stack_name '{v}'. "
                f"Available font stacks: {available}"
            )
        return v
