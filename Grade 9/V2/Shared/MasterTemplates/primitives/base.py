"""
Base module for Grade 9 Visual Primitives.
Provides:
- TrueType Unicode font registration with strict ASCII fallbacks
- Unified color palette conforming to ReportLab Color objects
- Common container frames (card boxes, pill badges, vector arrows)
- Bounding box calculations and coordinate transformations
"""

import os
import math
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ------------------------------------------------------------------------------
# 1. TrueType Font Registration (Strict zero-tofu ASCII compatibility)
# ------------------------------------------------------------------------------
FONT_NAME = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
FONT_OBLIQUE = "Helvetica-Oblique"

for (f_reg, f_path), (b_reg, b_path), (i_reg, i_path) in [
    (('SegoeUI', 'C:\\Windows\\Fonts\\segoeui.ttf'),
     ('SegoeUI-Bold', 'C:\\Windows\\Fonts\\segoeuib.ttf'),
     ('SegoeUI-Italic', 'C:\\Windows\\Fonts\\segoeuii.ttf')),
    (('Arial', 'C:\\Windows\\Fonts\\arial.ttf'),
     ('Arial-Bold', 'C:\\Windows\\Fonts\\arialbd.ttf'),
     ('Arial-Italic', 'C:\\Windows\\Fonts\\ariali.ttf'))
]:
    if os.path.exists(f_path) and os.path.exists(b_path):
        try:
            pdfmetrics.registerFont(TTFont(f_reg, f_path))
            pdfmetrics.registerFont(TTFont(b_reg, b_path))
            FONT_NAME = f_reg
            FONT_BOLD = b_reg
            if os.path.exists(i_path):
                pdfmetrics.registerFont(TTFont(i_reg, i_path))
                FONT_OBLIQUE = i_reg
            else:
                FONT_OBLIQUE = f_reg
            break
        except Exception:
            pass

# ------------------------------------------------------------------------------
# 2. Design Palette
# ------------------------------------------------------------------------------
class Palette:
    # Neutrals
    BG_CARD = colors.HexColor("#F8FAFC")
    BORDER_CARD = colors.HexColor("#CBD5E1")
    BORDER_LIGHT = colors.HexColor("#E2E8F0")
    TEXT_PRIMARY = colors.HexColor("#0F172A")
    TEXT_SECONDARY = colors.HexColor("#334155")
    TEXT_MUTED = colors.HexColor("#64748B")

    # Subject Accents
    # Physics - Cyan / Teal / Blue
    PHYSICS_DARK = colors.HexColor("#0F766E")
    PHYSICS_MED = colors.HexColor("#0D9488")
    PHYSICS_LIGHT = colors.HexColor("#CCFBF1")
    PHYSICS_BLUE = colors.HexColor("#2563EB")

    # Chemistry - Emerald / Green
    CHEM_DARK = colors.HexColor("#065F46")
    CHEM_MED = colors.HexColor("#059669")
    CHEM_LIGHT = colors.HexColor("#ECFDF5")
    CHEM_BORDER = colors.HexColor("#A7F3D0")

    # Mathematics - Indigo / Slate / Amber
    MATH_DARK = colors.HexColor("#1E3A8A")
    MATH_MED = colors.HexColor("#3B82F6")
    MATH_LIGHT = colors.HexColor("#EFF6FF")
    MATH_BORDER = colors.HexColor("#93C5FD")

    # Semantic States
    SUCCESS = colors.HexColor("#059669")
    WARNING = colors.HexColor("#D97706")
    DANGER = colors.HexColor("#DC2626")
    INFO = colors.HexColor("#0284C7")

    # Dalton Sphere Elements
    ELEMENT_H = colors.HexColor("#64748B")   # Slate gray
    ELEMENT_O = colors.HexColor("#DC2626")   # Crimson red
    ELEMENT_C = colors.HexColor("#1E293B")   # Charcoal
    ELEMENT_N = colors.HexColor("#2563EB")   # Blue
    ELEMENT_CL = colors.HexColor("#059669")  # Emerald green
    ELEMENT_METAL = colors.HexColor("#94A3B8") # Silver


# ------------------------------------------------------------------------------
# 3. Canvas Container & Vector Helpers
# ------------------------------------------------------------------------------
def draw_card_box(c, x, y, w, h, title=None, title_color=None, bg_color=None, border_color=None, corner_radius=6):
    """Draws a standardized rounded card frame with optional title banner."""
    c.saveState()
    if bg_color is None:
        bg_color = Palette.BG_CARD
    if border_color is None:
        border_color = Palette.BORDER_CARD
    if title_color is None:
        title_color = Palette.PHYSICS_DARK

    c.setFillColor(bg_color)
    c.setStrokeColor(border_color)
    c.setLineWidth(0.8)
    c.roundRect(x, y, w, h, corner_radius, fill=1, stroke=1)

    if title:
        c.setFont(FONT_BOLD, 8)
        c.setFillColor(title_color)
        c.drawString(x + 12, y + h - 16, title)
    c.restoreState()


def draw_pill_badge(c, x, y, text, bg_color, text_color, font=None, font_size=8, height=16, padding_x=8):
    """Draws a rounded pill badge."""
    c.saveState()
    if font is None:
        font = FONT_BOLD
    c.setFont(font, font_size)
    text_width = c.stringWidth(text, font, font_size)
    total_w = text_width + 2 * padding_x
    c.setFillColor(bg_color)
    c.setStrokeColor(bg_color)
    c.roundRect(x, y - height / 2, total_w, height, height / 2, fill=1, stroke=0)
    c.setFillColor(text_color)
    c.drawString(x + padding_x, y - font_size / 2 + 1, text)
    c.restoreState()
    return total_w


def draw_arrow(c, x1, y1, x2, y2, color, line_width=1.5, head_len=6, head_width=3, dashed=False):
    """Draws a line with a triangular arrowhead at (x2, y2)."""
    c.saveState()
    c.setStrokeColor(color)
    c.setFillColor(color)
    c.setLineWidth(line_width)
    if dashed:
        c.setDash(3, 2)
    c.line(x1, y1, x2, y2)
    if dashed:
        c.setDash()

    angle = math.atan2(y2 - y1, x2 - x1)
    p = c.beginPath()
    p.moveTo(x2, y2)
    p.lineTo(x2 - head_len * math.cos(angle) + head_width * math.sin(angle),
             y2 - head_len * math.sin(angle) - head_width * math.cos(angle))
    p.lineTo(x2 - head_len * math.cos(angle) - head_width * math.sin(angle),
             y2 - head_len * math.sin(angle) + head_width * math.cos(angle))
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.restoreState()
