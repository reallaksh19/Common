"""
Shared Graph Engine for Grade 9 V2 (Math, Physics, Chem).
"""
from typing import Any, Dict, List

class GraphEngine:
    """Renders charts and graphs independently of the core subject primitive."""

    @staticmethod
    def draw_bar_chart(backend: Any, bbox_x: float, bbox_y: float, width: float, height: float, params: Dict[str, Any]) -> None:
        """Draws a generic bar chart with semantic visual grounding."""
        title = params.get("title", "Bar Chart")
        categories = params.get("categories", [])
        values = params.get("values", [])
        y_label = params.get("y_label", "Values")
        x_label = params.get("x_label", "Categories")

        labels = [title, y_label, x_label] + categories + [str(v) for v in values]

        backend.draw_rect(bbox_x, bbox_y, width, height, fill="#FFFFFF", stroke="#333333", corner_radius=4.0)
        backend.draw_text(title, bbox_x + 10, bbox_y + height - 20, font_size=14, color="#111111")
        
        ax_x = bbox_x + 40
        ax_y = bbox_y + 30
        chart_w = width - 60
        chart_h = height - 70
        
        # Axes
        backend.draw_line(ax_x, ax_y, ax_x + chart_w, ax_y, stroke="#333333", stroke_width=1.5)
        backend.draw_line(ax_x, ax_y, ax_x, ax_y + chart_h, stroke="#333333", stroke_width=1.5)

        backend.draw_text(y_label, bbox_x + 5, ax_y + chart_h + 10, font_size=10, color="#555555")
        backend.draw_text(x_label, ax_x + chart_w + 10, ax_y - 5, font_size=10, color="#555555")
        
        if not categories or not values:
            backend.record_evidence("SHARED_GRAPH_BAR", params, len(labels), labels)
            return
            
        max_v = max(values) if values else 10
        if max_v == 0: max_v = 1
        
        bar_slot = chart_w / len(categories)
        bar_w = bar_slot * 0.6
        
        for idx, (cat, val) in enumerate(zip(categories, values)):
            bx = ax_x + idx * bar_slot + (bar_slot - bar_w) / 2.0
            bh = (val / max_v) * chart_h
            backend.draw_rect(bx, ax_y, bar_w, bh, fill="#4A90E2", stroke="#111111")
            backend.draw_text(str(val), bx + bar_w/2, ax_y + bh + 5, font_size=10, align="center")
            backend.draw_text(str(cat), bx + bar_w/2, ax_y - 15, font_size=10, align="center")

        backend.record_evidence("SHARED_GRAPH_BAR", params, len(labels), labels)

    @staticmethod
    def draw_line_graph(backend: Any, bbox_x: float, bbox_y: float, width: float, height: float, params: Dict[str, Any]) -> None:
        """Draws a generic line graph (useful for Physics kinematics)."""
        title = params.get("title", "Line Graph")
        x_points = params.get("x_points", [])
        y_points = params.get("y_points", [])
        
        labels = [title] + [str(x) for x in x_points] + [str(y) for y in y_points]
        
        backend.draw_rect(bbox_x, bbox_y, width, height, fill="#FFFFFF", stroke="#333333", corner_radius=4.0)
        backend.draw_text(title, bbox_x + 10, bbox_y + height - 20, font_size=14, color="#111111")
        
        ax_x = bbox_x + 40
        ax_y = bbox_y + 30
        chart_w = width - 60
        chart_h = height - 70
        
        backend.draw_line(ax_x, ax_y, ax_x + chart_w, ax_y, stroke="#333333", stroke_width=1.5)
        backend.draw_line(ax_x, ax_y, ax_x, ax_y + chart_h, stroke="#333333", stroke_width=1.5)
        
        if not x_points or not y_points:
            backend.record_evidence("SHARED_GRAPH_LINE", params, len(labels), labels)
            return
            
        max_x = max(x_points) if max(x_points) > 0 else 1
        max_y = max(y_points) if max(y_points) > 0 else 1
        
        pts = []
        for x, y in zip(x_points, y_points):
            px = ax_x + (x / max_x) * chart_w
            py = ax_y + (y / max_y) * chart_h
            pts.append((px, py))
            backend.draw_circle(px, py, 3.0, fill="#E94E77", stroke="#111111")
            backend.draw_text(f"({x},{y})", px + 5, py + 5, font_size=9, color="#555555")
            
        for i in range(len(pts) - 1):
            backend.draw_line(pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1], stroke="#E94E77", stroke_width=2.0)
            
        backend.record_evidence("SHARED_GRAPH_LINE", params, len(labels), labels)
