"""Visual element generators (charts, diagrams, infographics)."""

from pptx_generator.visuals.charts import (
    add_bar_chart,
    add_line_chart,
    add_pie_chart,
    add_horizontal_bar_chart,
)
from pptx_generator.visuals.diagrams import (
    add_flow_diagram,
    add_hierarchy_diagram,
    add_cycle_diagram,
    add_process_arrows,
)
from pptx_generator.visuals.infographics import (
    add_stat_card,
    add_stat_row,
    add_progress_bar,
    add_icon_text_pair,
    add_kpi_dashboard,
)
from pptx_generator.visuals.shapes import (
    add_rounded_rectangle,
    add_circle,
    add_arrow,
    add_line,
    add_chevron,
    add_accent_divider,
    add_triangle,
    add_star,
    add_hexagon,
)

__all__ = [
    # Charts
    "add_bar_chart",
    "add_line_chart",
    "add_pie_chart",
    "add_horizontal_bar_chart",
    # Diagrams
    "add_flow_diagram",
    "add_hierarchy_diagram",
    "add_cycle_diagram",
    "add_process_arrows",
    # Infographics
    "add_stat_card",
    "add_stat_row",
    "add_progress_bar",
    "add_icon_text_pair",
    "add_kpi_dashboard",
    # Shapes
    "add_rounded_rectangle",
    "add_circle",
    "add_arrow",
    "add_line",
    "add_chevron",
    "add_accent_divider",
    "add_triangle",
    "add_star",
    "add_hexagon",
]
