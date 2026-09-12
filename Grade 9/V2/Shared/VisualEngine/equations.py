"""
Shared Equation Engine for Grade 9 V2.
"""
from typing import Any, Dict

class EquationEngine:
    """Renders mathematical and chemical equations."""

    @staticmethod
    def draw_chemical_equation(backend: Any, bbox_x: float, bbox_y: float, width: float, height: float, params: Dict[str, Any]) -> None:
        """Draws a chemical equation (e.g. 2H2 + O2 -> 2H2O)."""
        reactants = params.get("reactants", [])
        products = params.get("products", [])
        conditions = params.get("conditions", "")
        
        labels = [conditions] + [r.get("compound", "") for r in reactants] + [p.get("compound", "") for p in products]
        for r in reactants:
            if "coefficient" in r: labels.append(str(r["coefficient"]))
        for p in products:
            if "coefficient" in p: labels.append(str(p["coefficient"]))
            
        backend.draw_rect(bbox_x, bbox_y, width, height, fill="#FAFAFA", stroke="#DDDDDD")
        
        cx = bbox_x + 20
        cy = bbox_y + height / 2.0
        
        def render_compound(comp: Dict[str, Any], x: float) -> float:
            coef = str(comp.get("coefficient", ""))
            if coef == "1": coef = ""
            formula = comp.get("compound", "")
            state = f"({comp.get('state', 'g')})"
            
            if coef:
                backend.draw_text(coef, x, cy, font_size=16, color="#E94E77")
                x += len(coef) * 10
                
            backend.draw_text(formula, x, cy, font_size=14, color="#111111")
            x += len(formula) * 9
            
            backend.draw_text(state, x, cy - 5, font_size=10, color="#555555")
            x += 25
            return x

        for i, r in enumerate(reactants):
            cx = render_compound(r, cx)
            if i < len(reactants) - 1:
                backend.draw_text("+", cx, cy, font_size=14, color="#333333")
                cx += 20
                
        # Draw yield arrow
        cx += 10
        backend.draw_arrow(cx, cy + 5, cx + 40, cy + 5, stroke="#333333", stroke_width=2.0)
        if conditions:
            backend.draw_text(conditions, cx + 20, cy + 15, font_size=10, color="#555555", align="center")
        cx += 50
        
        for i, p in enumerate(products):
            cx = render_compound(p, cx)
            if i < len(products) - 1:
                backend.draw_text("+", cx, cy, font_size=14, color="#333333")
                cx += 20

        backend.record_evidence("SHARED_CHEM_EQUATION", params, len(labels), labels)
