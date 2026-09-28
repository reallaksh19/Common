"""
Equations & Typesetting Module for Grade 9 Visual Primitives.
Provides:
- FormulaAnatomyEngine: Chemical formula tokenization with non-overlapping dynamic callout pins
- ValencyCrissCrossEngine: Valency crossover arrows demonstrating chemical formula derivation
- ChemicalReactionEngine: Balanced chemical reaction typesetting with state symbols and conditions
- GeometryProofBlock: Two-column Euclidean Statement | Reason proof tables
- MathEquationBlock: Aligned multi-line algebraic derivations with validation invariant callouts
"""

from reportlab.lib import colors
from .base import (FONT_NAME, FONT_BOLD, FONT_OBLIQUE, Palette, draw_card_box, draw_arrow, draw_pill_badge)


class FormulaAnatomyEngine:
    """
    Renders chemical formulas with non-overlapping dynamic callout pins.
    """
    @staticmethod
    def draw_formula_anatomy(c, x, y, w, h,
                              title="CHEMICAL FORMULA ANATOMY: COEFFICIENTS, SUBSCRIPTS & CHARGES",
                              species="2 SO4^2-"):
        c.saveState()
        draw_card_box(c, x, y, w, h, title=title, title_color=Palette.CHEM_DARK)

        fx = x + w / 2 - 50
        fy = y + h * 0.44

        # 1. Coefficient: "2"
        c.setFont(FONT_BOLD, 22)
        c.setFillColor(colors.HexColor("#2563EB"))
        c.drawString(fx, fy, "2")

        # 2. Base Formula: "SO"
        c.setFillColor(Palette.TEXT_PRIMARY)
        c.drawString(fx + 18, fy, "SO")

        # 3. Subscript: "4"
        c.setFont(FONT_BOLD, 14)
        c.setFillColor(colors.HexColor("#D97706"))
        c.drawString(fx + 55, fy - 6, "4")

        # 4. Ionic Charge: "2-"
        c.setFont(FONT_BOLD, 13)
        c.setFillColor(colors.HexColor("#DC2626"))
        c.drawString(fx + 66, fy + 12, "2-")

        # ----------------- Callout Pins with Leader Lines -----------------
        # Coefficient Callout (Upper Left)
        c.setFillColor(colors.HexColor("#2563EB"))
        c.setStrokeColor(colors.HexColor("#2563EB"))
        c.setFont(FONT_BOLD, 7)
        c.drawString(fx - 72, fy + 32, "COEFFICIENT = 2")
        c.setFont(FONT_NAME, 6.5)
        c.drawString(fx - 72, fy + 24, "Multiplies entire unit")
        c.setLineWidth(1.0)
        c.line(fx - 2, fy + 22, fx + 8, fy + 14)

        # Subscript Callout (Lower Center)
        c.setFillColor(colors.HexColor("#D97706"))
        c.setStrokeColor(colors.HexColor("#D97706"))
        c.setFont(FONT_BOLD, 7)
        c.drawString(fx + 35, fy - 22, "SUBSCRIPT = 4")
        c.setFont(FONT_NAME, 6.5)
        c.drawString(fx + 35, fy - 30, "Atoms per sulfate ion")
        c.line(fx + 60, fy - 18, fx + 60, fy - 8)

        # Ionic Charge Callout (Upper Right)
        c.setFillColor(colors.HexColor("#DC2626"))
        c.setStrokeColor(colors.HexColor("#DC2626"))
        c.setFont(FONT_BOLD, 7)
        c.drawString(fx + 92, fy + 32, "IONIC CHARGE = 2-")
        c.setFont(FONT_NAME, 6.5)
        c.drawString(fx + 92, fy + 24, "Net charge (S + 4 O)")
        c.line(fx + 90, fy + 22, fx + 78, fy + 15)

        c.restoreState()


class ValencyCrissCrossEngine:
    """
    Renders valency criss-cross arrow diagrams demonstrating chemical formula derivation.
    Example: Al^3+ and O^2- -> Al2O3
    """
    @staticmethod
    def draw_criss_cross(c, x, y, w, h,
                         cation_sym="Al", cation_val="3+",
                         anion_sym="O", anion_val="2-",
                         result_formula="Al2O3",
                         title="CRISS-CROSS VALENCY METHOD FOR FORMULA WRITING"):
        c.saveState()
        draw_card_box(c, x, y, w, h, title=title, title_color=Palette.CHEM_DARK)

        cx = x + w / 2 - 50
        cy = y + h * 0.52
        gap = 70

        # Cation Symbol & Valency
        c.setFont(FONT_BOLD, 18)
        c.setFillColor(Palette.CHEM_DARK)
        c.drawCentredString(cx, cy, cation_sym)
        c.setFont(FONT_BOLD, 11)
        c.setFillColor(Palette.PHYSICS_BLUE)
        c.drawCentredString(cx, cy + 22, cation_val)
        c.setFont(FONT_NAME, 6.5)
        c.setFillColor(Palette.TEXT_MUTED)
        c.drawCentredString(cx, cy - 12, "Cation")

        # Anion Symbol & Valency
        c.setFont(FONT_BOLD, 18)
        c.setFillColor(Palette.CHEM_DARK)
        c.drawCentredString(cx + gap, cy, anion_sym)
        c.setFont(FONT_BOLD, 11)
        c.setFillColor(Palette.DANGER)
        c.drawCentredString(cx + gap, cy + 22, anion_val)
        c.setFont(FONT_NAME, 6.5)
        c.setFillColor(Palette.TEXT_MUTED)
        c.drawCentredString(cx + gap, cy - 12, "Anion")

        # Diagonal Criss-Cross Arrows
        # Cation valency (top left) to Anion subscript (bottom right)
        draw_arrow(c, cx + 8, cy + 18, cx + gap - 8, cy - 10, Palette.PHYSICS_BLUE, line_width=1.2, head_len=5, head_width=2.5)
        # Anion valency (top right) to Cation subscript (bottom left)
        draw_arrow(c, cx + gap - 8, cy + 18, cx + 8, cy - 10, Palette.DANGER, line_width=1.2, head_len=5, head_width=2.5)

        # Arrow pointing to resulting formula
        draw_arrow(c, cx + gap + 25, cy, cx + gap + 55, cy, Palette.CHEM_MED, line_width=1.5, head_len=6)

        # Resulting Formula Box
        res_x = cx + gap + 65
        res_w = 64
        res_h = 32
        c.setFillColor(colors.HexColor("#ECFDF5"))
        c.setStrokeColor(Palette.CHEM_BORDER)
        c.roundRect(res_x, cy - res_h / 2, res_w, res_h, 4, fill=1, stroke=1)
        c.setFont(FONT_BOLD, 12)
        c.setFillColor(Palette.CHEM_DARK)
        c.drawCentredString(res_x + res_w / 2, cy - 4, result_formula)
        c.setFont(FONT_NAME, 6)
        c.setFillColor(Palette.TEXT_MUTED)
        c.drawCentredString(res_x + res_w / 2, cy - 13, "Formula")

        c.setFont(FONT_NAME, 6.8)
        c.setFillColor(Palette.TEXT_MUTED)
        c.drawCentredString(x + w / 2, y + 10, f"Rule: Charges swap to become subscripts without signs -> {result_formula}")

        c.restoreState()


class ChemicalReactionEngine:
    """
    Typesets chemical reactions with state symbols, conditions, and stoichiometric numbers.
    """
    @staticmethod
    def draw_reaction(c, x, y, w, h,
                      reactants="2 H2 (g) + O2 (g)",
                      arrow="-->", condition="Spark / Pt",
                      products="2 H2O (l)",
                      title="BALANCED CHEMICAL EQUATION"):
        c.saveState()
        draw_card_box(c, x, y, w, h, title=title, title_color=Palette.CHEM_DARK)

        cx = x + w / 2
        cy = y + h * 0.44

        # Reaction string display
        c.setFont(FONT_BOLD, 10.5)
        c.setFillColor(Palette.TEXT_PRIMARY)

        # Measure parts
        r_w = c.stringWidth(reactants, FONT_BOLD, 10.5)
        p_w = c.stringWidth(products, FONT_BOLD, 10.5)
        arr_len = 36

        start_rx = cx - (r_w + arr_len + p_w + 20) / 2

        # Reactants
        c.drawString(start_rx, cy, reactants)

        # Arrow
        arr_sx = start_rx + r_w + 10
        arr_ex = arr_sx + arr_len
        draw_arrow(c, arr_sx, cy + 3.5, arr_ex, cy + 3.5, Palette.CHEM_MED, line_width=1.5, head_len=5)

        # Condition above arrow
        if condition:
            c.setFont(FONT_BOLD, 6.5)
            c.setFillColor(Palette.CHEM_DARK)
            c.drawCentredString((arr_sx + arr_ex) / 2, cy + 9, condition)

        # Products
        c.setFont(FONT_BOLD, 10.5)
        c.setFillColor(Palette.TEXT_PRIMARY)
        c.drawString(arr_ex + 10, cy, products)

        # State key badge
        badge = "State Symbols: (s) solid | (l) liquid | (g) gas | (aq) aqueous solution"
        draw_pill_badge(c, x + 25, y + 10, badge, colors.HexColor("#F1F5F9"), Palette.TEXT_MUTED, font_size=6.5, height=13)

        c.restoreState()


class GeometryProofBlock:
    """
    Renders structured two-column Euclidean Statement | Reason tables.
    """
    @staticmethod
    def draw_proof(c, x, y, w, h, steps, title="EUCLIDEAN GEOMETRIC PROOF: STATEMENT & REASON"):
        """
        steps: list of tuples: [("1. In Triangle ABC and Triangle PQR, AB = PQ", "Given"), ...]
        """
        c.saveState()
        draw_card_box(c, x, y, w, h, title=title, title_color=Palette.MATH_DARK)

        table_top = y + h - 28
        col1_w = (w - 24) * 0.62
        col2_w = (w - 24) * 0.38

        # Header bar
        c.setFillColor(colors.HexColor("#EFF6FF"))
        c.rect(x + 12, table_top - 16, w - 24, 16, fill=1, stroke=0)
        c.setFont(FONT_BOLD, 7.5)
        c.setFillColor(Palette.MATH_DARK)
        c.drawString(x + 18, table_top - 12, "STATEMENT")
        c.drawString(x + 12 + col1_w + 8, table_top - 12, "REASON / AXIOM")

        # Divider line
        c.setStrokeColor(Palette.BORDER_CARD)
        c.setLineWidth(0.8)
        c.line(x + 12, table_top - 16, x + w - 12, table_top - 16)

        # Rows
        row_y = table_top - 28
        for stmt, reason in steps:
            c.setFont(FONT_NAME, 7)
            c.setFillColor(Palette.TEXT_PRIMARY)
            c.drawString(x + 18, row_y, stmt)

            c.setFont(FONT_OBLIQUE, 6.8)
            c.setFillColor(Palette.TEXT_MUTED)
            c.drawString(x + 12 + col1_w + 8, row_y, reason)

            # Subtle row line
            c.setStrokeColor(Palette.BORDER_LIGHT)
            c.setLineWidth(0.5)
            c.line(x + 16, row_y - 4, x + w - 16, row_y - 4)
            row_y -= 14

        c.restoreState()


class MathEquationBlock:
    """
    Formats multi-line algebraic derivations with aligned equals signs and invariant verification checkmarks.
    """
    @staticmethod
    def draw_algebra_block(c, x, y, w, h, lines, invariant_text=None,
                           title="ALGEBRAIC DERIVATION & INVARIANT VERIFICATION"):
        """
        lines: list of strings, e.g. ["2x + 5 = 15", "2x = 10", "x = 5"]
        """
        c.saveState()
        draw_card_box(c, x, y, w, h, title=title, title_color=Palette.MATH_DARK)

        start_y = y + h - 34
        for line in lines:
            c.setFont(FONT_BOLD, 8)
            c.setFillColor(Palette.TEXT_PRIMARY)
            c.drawString(x + 24, start_y, line)
            start_y -= 14

        if invariant_text:
            badge = f"[VALIDATED INVARIANT] {invariant_text}"
            draw_pill_badge(c, x + 20, y + 10, badge, colors.HexColor("#ECFDF5"), Palette.SUCCESS, font_size=6.8, height=14)

        c.restoreState()
