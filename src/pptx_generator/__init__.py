"""Professional PowerPoint presentation generator."""

from pptx_generator.generator import (
    PresentationGenerator,
    GeneratorError,
    ConfigurationError,
    BuildError,
)
from pptx_generator.config.settings import PresentationConfig, SlideConfig
from pptx_generator.parsers.models import ParsedPresentation, SlideContent

__version__ = "0.1.0"

__all__ = [
    "PresentationGenerator",
    "GeneratorError",
    "ConfigurationError",
    "BuildError",
    "PresentationConfig",
    "SlideConfig",
    "ParsedPresentation",
    "SlideContent",
]
