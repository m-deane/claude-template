from __future__ import annotations

from typing import Dict

from pydantic import BaseModel, Field
from pptx.dml.color import RGBColor


class ColorPalette(BaseModel):
    """Color palette configuration for presentations.

    All colors are specified as hex strings (e.g., '#1A2B3C').
    """

    primary: str = Field(..., description="Primary brand/theme color")
    secondary: str = Field(..., description="Secondary supporting color")
    accent: str = Field(..., description="Accent color for highlights and CTAs")
    background: str = Field(..., description="Main background color")
    text_dark: str = Field(..., description="Dark text color for light backgrounds")
    text_light: str = Field(..., description="Light text color for dark backgrounds")
    success: str = Field(..., description="Success/positive indicator color")
    warning: str = Field(..., description="Warning/caution indicator color")
    danger: str = Field(..., description="Danger/error indicator color")
    neutral: str = Field(..., description="Neutral gray for borders and dividers")
    gradient_start: str = Field(..., description="Starting color for gradients")
    gradient_end: str = Field(..., description="Ending color for gradients")

    def to_rgb(self, color_hex: str) -> RGBColor:
        """Convert hex color string to pptx RGBColor object.

        Args:
            color_hex: Hex color string with or without '#' prefix

        Returns:
            RGBColor object for use with python-pptx

        Example:
            >>> palette = ColorPalette(**PALETTES['corporate'])
            >>> rgb = palette.to_rgb(palette.primary)
            >>> rgb = palette.to_rgb('#1A2B3C')
        """
        hex_color = color_hex.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return RGBColor(r, g, b)

    def get_color_map(self) -> Dict[str, RGBColor]:
        """Get all palette colors as RGBColor objects.

        Returns:
            Dictionary mapping color names to RGBColor objects
        """
        return {
            'primary': self.to_rgb(self.primary),
            'secondary': self.to_rgb(self.secondary),
            'accent': self.to_rgb(self.accent),
            'background': self.to_rgb(self.background),
            'text_dark': self.to_rgb(self.text_dark),
            'text_light': self.to_rgb(self.text_light),
            'success': self.to_rgb(self.success),
            'warning': self.to_rgb(self.warning),
            'danger': self.to_rgb(self.danger),
            'neutral': self.to_rgb(self.neutral),
            'gradient_start': self.to_rgb(self.gradient_start),
            'gradient_end': self.to_rgb(self.gradient_end),
        }


PALETTES: Dict[str, Dict[str, str]] = {
    "corporate": {
        "primary": "#1E3A5F",          # Navy blue - trust and professionalism
        "secondary": "#2E5984",         # Medium blue - depth
        "accent": "#E8B44F",            # Gold - premium feel
        "background": "#FFFFFF",        # White - clean
        "text_dark": "#1A1A1A",         # Near black - readability
        "text_light": "#F5F5F5",        # Off-white - soft contrast
        "success": "#2E7D32",           # Forest green
        "warning": "#F57C00",           # Dark orange
        "danger": "#C62828",            # Deep red
        "neutral": "#9E9E9E",           # Medium gray
        "gradient_start": "#1E3A5F",    # Navy
        "gradient_end": "#2E5984",      # Medium blue
    },
    "modern": {
        "primary": "#00897B",           # Teal - fresh and modern
        "secondary": "#26A69A",         # Light teal - harmony
        "accent": "#FF6F61",            # Coral - vibrant energy
        "background": "#FAFAFA",        # Almost white - spacious
        "text_dark": "#212121",         # Charcoal - strong contrast
        "text_light": "#ECEFF1",        # Light gray-blue
        "success": "#43A047",           # Green
        "warning": "#FB8C00",           # Orange
        "danger": "#E53935",            # Red
        "neutral": "#757575",           # Gray
        "gradient_start": "#00897B",    # Teal
        "gradient_end": "#FF6F61",      # Coral
    },
    "dark": {
        "primary": "#BB86FC",           # Light purple - modern dark theme
        "secondary": "#3700B3",         # Deep purple - depth
        "accent": "#03DAC6",            # Cyan - pop of color
        "background": "#121212",        # Dark gray - OLED friendly
        "text_dark": "#E1E1E1",         # Light gray - readability on dark
        "text_light": "#FFFFFF",        # White - maximum contrast
        "success": "#03DAC6",           # Cyan (reuse accent)
        "warning": "#CF6679",           # Pink-red
        "danger": "#FF5252",            # Bright red
        "neutral": "#3C3C3C",           # Dark gray
        "gradient_start": "#3700B3",    # Deep purple
        "gradient_end": "#BB86FC",      # Light purple
    },
    "minimal": {
        "primary": "#2C2C2C",           # Charcoal - sophisticated
        "secondary": "#5C5C5C",         # Medium gray - subtle depth
        "accent": "#0066CC",            # Pure blue - singular focus
        "background": "#FFFFFF",        # White - maximum clarity
        "text_dark": "#1A1A1A",         # Near black
        "text_light": "#F8F8F8",        # Off-white
        "success": "#0066CC",           # Blue (reuse accent)
        "warning": "#666666",           # Gray - understated
        "danger": "#2C2C2C",            # Charcoal (reuse primary)
        "neutral": "#E0E0E0",           # Light gray
        "gradient_start": "#5C5C5C",    # Medium gray
        "gradient_end": "#2C2C2C",      # Charcoal
    },
    "finance": {
        "primary": "#003D5B",           # Deep navy - stability
        "secondary": "#005F73",         # Teal-blue - growth
        "accent": "#00B4D8",            # Bright blue - clarity
        "background": "#F7F9FB",        # Light blue-gray - professional
        "text_dark": "#1B2631",         # Dark blue-gray
        "text_light": "#ECF0F1",        # Light gray
        "success": "#2E7D32",           # Green - profit
        "warning": "#EF6C00",           # Orange - caution
        "danger": "#B71C1C",            # Deep red - loss
        "neutral": "#90A4AE",           # Blue-gray
        "gradient_start": "#003D5B",    # Deep navy
        "gradient_end": "#005F73",      # Teal-blue
    },
    "tech": {
        "primary": "#6200EA",           # Deep purple - innovation
        "secondary": "#7C4DFF",         # Medium purple - creativity
        "accent": "#00E5FF",            # Cyan - cutting edge
        "background": "#F5F5F5",        # Light gray - modern
        "text_dark": "#212121",         # Near black
        "text_light": "#FAFAFA",        # Almost white
        "success": "#00C853",           # Bright green
        "warning": "#FFD600",           # Yellow - attention
        "danger": "#FF1744",            # Bright red
        "neutral": "#9E9E9E",           # Gray
        "gradient_start": "#6200EA",    # Deep purple
        "gradient_end": "#00E5FF",      # Cyan
    },
}
