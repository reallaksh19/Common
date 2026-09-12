"""
Shared Diagram Engine for Grade 9 V2.
"""
from typing import Any, Dict

class DiagramEngine:
    """Renders vectors, forces, flowcharts, and generic diagrams."""

    @staticmethod
    def draw_vector_force(backend: Any, bbox_x: float, bbox_y: float, width: float, height: float, params: Dict[str, Any]) -> None:
        """Draws a central object with force vectors (useful for Physics free body diagrams)."""
        object_name = params.get("object_name", "Mass")
        forces = params.get("forces", [])  # list of dicts: {"magnitude": 10, "direction": "UP", "label": "Normal Force"}
        
        labels = [object_name]
        
        cx = bbox_x + width / 2.0
        cy = bbox_y + height / 2.0
        
        backend.draw_rect(bbox_x, bbox_y, width, height, fill="#FAFAFA", stroke="#DDDDDD")
        backend.draw_rect(cx - 30, cy - 30, 60, 60, fill="#CCCCCC", stroke="#333333", corner_radius=5.0)
        backend.draw_text(object_name, cx, cy - 5, font_size=12, align="center")
        
        for f in forces:
            mag = f.get("magnitude", 0)
            d = f.get("direction", "UP").upper()
            lbl = str(f.get("label", f"{mag}N"))
            labels.append(lbl)
            labels.append(str(mag))
            
            vec_len = min(mag * 5.0, min(width, height)/2.0 - 40)
            
            if d == "UP":
                backend.draw_arrow(cx, cy + 30, cx, cy + 30 + vec_len, stroke="#E94E77", stroke_width=2.0)
                backend.draw_text(lbl, cx + 10, cy + 30 + vec_len + 5, font_size=10, color="#E94E77")
            elif d == "DOWN":
                backend.draw_arrow(cx, cy - 30, cx, cy - 30 - vec_len, stroke="#E94E77", stroke_width=2.0)
                backend.draw_text(lbl, cx + 10, cy - 30 - vec_len - 15, font_size=10, color="#E94E77")
            elif d == "LEFT":
                backend.draw_arrow(cx - 30, cy, cx - 30 - vec_len, cy, stroke="#E94E77", stroke_width=2.0)
                backend.draw_text(lbl, cx - 30 - vec_len, cy + 10, font_size=10, color="#E94E77", align="right")
            elif d == "RIGHT":
                backend.draw_arrow(cx + 30, cy, cx + 30 + vec_len, cy, stroke="#E94E77", stroke_width=2.0)
                backend.draw_text(lbl, cx + 30 + vec_len, cy + 10, font_size=10, color="#E94E77", align="left")

        backend.record_evidence("SHARED_DIAGRAM_FORCE", params, len(labels), labels)
