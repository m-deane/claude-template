"""Simplified test suite for visual elements."""

from __future__ import annotations

import pytest
from pptx import Presentation
from pptx.util import Inches

from pptx_generator.config.colors import ColorPalette, PALETTES


def make_prs():
    """Create a presentation with standard dimensions."""
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    return prs


def get_test_palette():
    """Get a test color palette."""
    return ColorPalette(**PALETTES["corporate"])


class TestVisualsImport:
    """Test that visual modules can be imported."""

    def test_import_charts(self):
        """Test importing chart functions."""
        from pptx_generator.visuals import (
            add_bar_chart,
            add_line_chart,
            add_pie_chart,
            add_horizontal_bar_chart,
        )

        assert callable(add_bar_chart)
        assert callable(add_line_chart)
        assert callable(add_pie_chart)
        assert callable(add_horizontal_bar_chart)

    def test_import_diagrams(self):
        """Test importing diagram functions."""
        from pptx_generator.visuals import (
            add_flow_diagram,
            add_hierarchy_diagram,
            add_cycle_diagram,
            add_process_arrows,
        )

        assert callable(add_flow_diagram)
        assert callable(add_hierarchy_diagram)
        assert callable(add_cycle_diagram)
        assert callable(add_process_arrows)

    def test_import_infographics(self):
        """Test importing infographic functions."""
        from pptx_generator.visuals import (
            add_stat_card,
            add_stat_row,
            add_progress_bar,
            add_icon_text_pair,
            add_kpi_dashboard,
        )

        assert callable(add_stat_card)
        assert callable(add_stat_row)
        assert callable(add_progress_bar)
        assert callable(add_icon_text_pair)
        assert callable(add_kpi_dashboard)

    def test_import_shapes(self):
        """Test importing shape functions."""
        from pptx_generator.visuals import (
            add_rounded_rectangle,
            add_circle,
            add_arrow,
            add_line,
            add_chevron,
            add_accent_divider,
        )

        assert callable(add_rounded_rectangle)
        assert callable(add_circle)
        assert callable(add_arrow)
        assert callable(add_line)
        assert callable(add_chevron)
        assert callable(add_accent_divider)


class TestVisualsModulesExist:
    """Test that visual modules exist and can be loaded."""

    def test_charts_module(self):
        """Test charts module can be imported."""
        import pptx_generator.visuals.charts as charts_module
        assert charts_module is not None

    def test_diagrams_module(self):
        """Test diagrams module can be imported."""
        import pptx_generator.visuals.diagrams as diagrams_module
        assert diagrams_module is not None

    def test_infographics_module(self):
        """Test infographics module can be imported."""
        import pptx_generator.visuals.infographics as infographics_module
        assert infographics_module is not None

    def test_shapes_module(self):
        """Test shapes module can be imported."""
        import pptx_generator.visuals.shapes as shapes_module
        assert shapes_module is not None
