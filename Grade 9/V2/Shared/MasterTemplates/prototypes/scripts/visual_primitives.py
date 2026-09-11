"""
Visual Primitives Vector Drawing Module for ReportLab.
Generates deterministic, high-fidelity vector graphics for:
- Physics: 1D Number Line, v-t Kinematic Graph with shaded area
- Chemistry: Particle Model, Formula Anatomy, Oxidation State Lane
- Mathematics: 2D Coordinate Grid with Slope, Combinatorial Slot Boxes, Balance Scale
"""

import os
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register TrueType Unicode Fonts (SegoeUI / Arial)
FONT_NAME = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
FONT_OBLIQUE = "Helvetica-Oblique"

for (f_reg, f_path), (b_reg, b_path), (i_reg, i_path) in [
    (('SegoeUI', 'C:\\Windows\\Fonts\\segoeui.ttf'), ('SegoeUI-Bold', 'C:\\Windows\\Fonts\\segoeuib.ttf'), ('SegoeUI-Italic', 'C:\\Windows\\Fonts\\segoeuii.ttf')),
    (('Arial', 'C:\\Windows\\Fonts\\arial.ttf'), ('Arial-Bold', 'C:\\Windows\\Fonts\\arialbd.ttf'), ('Arial-Italic', 'C:\\Windows\\Fonts\\ariali.ttf'))
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


def draw_pill_badge(c, x, y, text, bg_color, text_color, font=None, font_size=8, height=16, padding_x=8):
    """Draws a rounded pill badge."""
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
    return total_w

# ==============================================================================
# PHYSICS PRIMITIVES
# ==============================================================================

def draw_number_line_1d(c, x, y, w, h, title="1D REFERENCE FRAME & DISPLACEMENT STRIP"):
    """Draws a 1D coordinate axis with positive direction, points, path, and displacement arrow."""
    c.saveState()
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.setLineWidth(0.8)
    c.roundRect(x, y, w, h, 6, fill=1, stroke=1)
    
    c.setFont(FONT_BOLD, 8)
    c.setFillColor(colors.HexColor("#0F766E"))
    c.drawString(x + 12, y + h - 16, title)
    
    axis_y = y + 46
    axis_start = x + 30
    axis_end = x + w - 40
    axis_w = axis_end - axis_start
    
    c.setStrokeColor(colors.HexColor("#334155"))
    c.setLineWidth(1.5)
    c.line(axis_start, axis_y, axis_end, axis_y)
    
    c.setFillColor(colors.HexColor("#334155"))
    p = c.beginPath()
    p.moveTo(axis_end, axis_y)
    p.lineTo(axis_end - 8, axis_y + 4)
    p.lineTo(axis_end - 8, axis_y - 4)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    
    c.setFont(FONT_BOLD, 8)
    c.drawString(axis_end - 2, axis_y + 8, "+ x (m) East -->")
    
    ticks = [-3, -2, -1, 0, 1, 2, 3, 4, 5]
    num_ticks = len(ticks)
    tick_spacing = axis_w / (num_ticks + 0.5)
    tick_positions = {}
    
    c.setFont(FONT_NAME, 7.5)
    for i, val in enumerate(ticks):
        tx = axis_start + 15 + i * tick_spacing
        tick_positions[val] = tx
        c.setStrokeColor(colors.HexColor("#475569"))
        c.setLineWidth(1.0 if val != 0 else 1.8)
        c.line(tx, axis_y - 4, tx, axis_y + 4)
        c.setFillColor(colors.HexColor("#0F172A") if val != 0 else colors.HexColor("#0F766E"))
        c.drawCentredString(tx, axis_y - 14, str(val))
    
    x_start = tick_positions[0]
    x_mid = tick_positions[5]
    x_end = tick_positions[2]
    
    # Leg 1
    path_y1 = axis_y + 16
    c.setStrokeColor(colors.HexColor("#2563EB"))
    c.setLineWidth(1.2)
    c.line(x_start, path_y1, x_mid, path_y1)
    c.line(x_mid - 4, path_y1 + 3, x_mid, path_y1)
    c.line(x_mid - 4, path_y1 - 3, x_mid, path_y1)
    c.setFont(FONT_NAME, 7)
    c.setFillColor(colors.HexColor("#1E40AF"))
    c.drawCentredString((x_start + x_mid) / 2, path_y1 + 4, "Leg 1: +5 m (East)")
    
    # Leg 2
    path_y2 = axis_y + 26
    c.setStrokeColor(colors.HexColor("#DC2626"))
    c.line(x_mid, path_y2, x_end, path_y2)
    c.line(x_end + 4, path_y2 + 3, x_end, path_y2)
    c.line(x_end + 4, path_y2 - 3, x_end, path_y2)
    c.setFillColor(colors.HexColor("#991B1B"))
    c.drawCentredString((x_mid + x_end) / 2, path_y2 + 4, "Leg 2: -3 m (West)")
    
    # Displacement Vector
    disp_y = axis_y - 24
    c.setStrokeColor(colors.HexColor("#0D9488"))
    c.setLineWidth(1.5)
    c.setDash(4, 3)
    c.line(x_start, disp_y, x_end, disp_y)
    c.setDash()
    
    c.setFillColor(colors.HexColor("#0D9488"))
    p_disp = c.beginPath()
    p_disp.moveTo(x_end, disp_y)
    p_disp.lineTo(x_end - 6, disp_y + 3)
    p_disp.lineTo(x_end - 6, disp_y - 3)
    p_disp.close()
    c.drawPath(p_disp, fill=1, stroke=0)
    
    c.setFont(FONT_BOLD, 7.5)
    c.drawString(x_start, disp_y - 10, "Start (x=0)")
    c.drawString(x_end + 4, disp_y - 10, "Finish (x=+2)")
    c.drawCentredString((x_start + x_end) / 2, disp_y + 4, "Displacement Delta x = +2 m")
    
    c.restoreState()

def draw_vt_graph(c, x, y, w, h, title="VELOCITY-TIME GRAPH & INTEGRATED DISPLACEMENT"):
    """Draws a v-t graph showing u, v, t, shaded area (ut rectangle + 1/2 at^2 triangle)."""
    c.saveState()
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.setLineWidth(0.8)
    c.roundRect(x, y, w, h, 6, fill=1, stroke=1)
    
    c.setFont(FONT_BOLD, 8)
    c.setFillColor(colors.HexColor("#0F766E"))
    c.drawString(x + 12, y + h - 16, title)
    
    gx = x + 40
    gy = y + 26
    gw = w - 80
    gh = h - 52
    
    u_y = gy + gh * 0.35
    v_y = gy + gh * 0.85
    t_x = gx + gw * 0.75
    
    # Rectangle polygon
    c.setFillColor(colors.HexColor("#E0F2FE"))
    c.setStrokeColor(colors.HexColor("#BAE6FD"))
    c.rect(gx, gy, t_x - gx, u_y - gy, fill=1, stroke=0)
    
    # Triangle polygon
    c.setFillColor(colors.HexColor("#FEF3C7"))
    p_tri = c.beginPath()
    p_tri.moveTo(gx, u_y)
    p_tri.lineTo(t_x, u_y)
    p_tri.lineTo(t_x, v_y)
    p_tri.close()
    c.drawPath(p_tri, fill=1, stroke=0)
    
    # Axes
    c.setStrokeColor(colors.HexColor("#334155"))
    c.setLineWidth(1.2)
    c.line(gx, gy, gx + gw, gy)
    c.line(gx, gy, gx, gy + gh)
    
    c.setFont(FONT_BOLD, 8)
    c.setFillColor(colors.HexColor("#334155"))
    c.drawString(gx + gw + 4, gy - 2, "t (s)")
    c.drawString(gx - 28, gy + gh - 4, "v (m/s)")
    
    c.setFont(FONT_NAME, 7.5)
    c.drawRightString(gx - 4, u_y - 2, "u")
    c.drawRightString(gx - 4, v_y - 2, "v")
    c.drawCentredString(t_x, gy - 12, "t")
    
    c.setStrokeColor(colors.HexColor("#94A3B8"))
    c.setLineWidth(0.8)
    c.setDash(3, 2)
    c.line(gx, u_y, t_x, u_y)
    c.line(gx, v_y, t_x, v_y)
    c.line(t_x, gy, t_x, v_y)
    c.setDash()
    
    c.setStrokeColor(colors.HexColor("#0D9488"))
    c.setLineWidth(1.8)
    c.line(gx, u_y, t_x, v_y)
    
    c.setFont(FONT_BOLD, 7.5)
    c.setFillColor(colors.HexColor("#0369A1"))
    c.drawCentredString((gx + t_x) / 2, (gy + u_y) / 2 - 2, "Rectangle: ut")
    
    c.setFillColor(colors.HexColor("#B45309"))
    c.drawCentredString(gx + (t_x - gx) * 0.65, u_y + (v_y - u_y) * 0.35, "Triangle: 1/2 at^2")
    
    c.setFont(FONT_BOLD, 7.5)
    c.setFillColor(colors.HexColor("#0F172A"))
    c.drawString(t_x + 8, gy + gh * 0.55, "s = ut + 1/2 at^2")
    c.setFont(FONT_NAME, 6.5)
    c.setFillColor(colors.HexColor("#64748B"))
    c.drawString(t_x + 8, gy + gh * 0.55 - 10, "Slope = a = (v-u)/t")
    c.drawString(t_x + 8, gy + gh * 0.55 - 19, "Area = Displacement")
    
    c.restoreState()

# ==============================================================================
# CHEMISTRY PRIMITIVES
# ==============================================================================

def draw_particle_model(c, x, y, w, h, title="SUBMICROSCOPIC PARTICLE MODEL"):
    """Draws particulate view with Dalton spheres showing count and composition conservation."""
    c.saveState()
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.setLineWidth(0.8)
    c.roundRect(x, y, w, h, 6, fill=1, stroke=1)
    
    c.setFont(FONT_BOLD, 8)
    c.setFillColor(colors.HexColor("#065F46"))
    c.drawString(x + 12, y + h - 16, title)
    
    col_w = (w - 40) / 2
    y_mid = y + (h - 20) / 2
    
    # Reactants Box
    c.setStrokeColor(colors.HexColor("#94A3B8"))
    c.setLineWidth(0.8)
    c.rect(x + 12, y + 24, col_w, h - 46, stroke=1, fill=0)
    c.setFont(FONT_BOLD, 7.5)
    c.setFillColor(colors.HexColor("#334155"))
    c.drawString(x + 16, y + h - 34, "Reactants: 2 H2 + O2")
    
    # 2 H2 (4 grey circles)
    c.setFillColor(colors.HexColor("#64748B"))
    c.circle(x + 30, y + 42, 6, fill=1, stroke=0)
    c.circle(x + 42, y + 42, 6, fill=1, stroke=0)
    c.circle(x + 30, y + 58, 6, fill=1, stroke=0)
    c.circle(x + 42, y + 58, 6, fill=1, stroke=0)
    
    # 1 O2 (2 red circles)
    c.setFillColor(colors.HexColor("#DC2626"))
    c.circle(x + 80, y + 50, 8, fill=1, stroke=0)
    c.circle(x + 94, y + 50, 8, fill=1, stroke=0)
    
    # Arrow (Vector Path)
    arr_x = x + 12 + col_w + 3
    c.setStrokeColor(colors.HexColor("#0F766E"))
    c.setLineWidth(1.5)
    c.line(arr_x, y_mid, arr_x + 10, y_mid)
    p_arr = c.beginPath()
    p_arr.moveTo(arr_x + 12, y_mid)
    p_arr.lineTo(arr_x + 8, y_mid + 3)
    p_arr.lineTo(arr_x + 8, y_mid - 3)
    p_arr.close()
    c.setFillColor(colors.HexColor("#0F766E"))
    c.drawPath(p_arr, fill=1, stroke=0)
    
    # Products Box
    c.setStrokeColor(colors.HexColor("#94A3B8"))
    c.rect(x + 28 + col_w, y + 24, col_w, h - 46, stroke=1, fill=0)
    c.setFont(FONT_BOLD, 7.5)
    c.setFillColor(colors.HexColor("#334155"))
    c.drawString(x + 32 + col_w, y + h - 34, "Products: 2 H2O")
    
    px1 = x + 32 + col_w + 25
    c.setFillColor(colors.HexColor("#DC2626"))
    c.circle(px1, y + 50, 8, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#64748B"))
    c.circle(px1 - 7, y + 42, 5, fill=1, stroke=0)
    c.circle(px1 + 7, y + 42, 5, fill=1, stroke=0)
    
    px2 = x + 32 + col_w + 75
    c.setFillColor(colors.HexColor("#DC2626"))
    c.circle(px2, y + 50, 8, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#64748B"))
    c.circle(px2 - 7, y + 42, 5, fill=1, stroke=0)
    c.circle(px2 + 7, y + 42, 5, fill=1, stroke=0)
    
    c.setFont(FONT_NAME, 6.5)
    c.setFillColor(colors.HexColor("#475569"))
    c.drawString(x + 16, y + 12, "Grey = H atom (4 total)  |  Red = O atom (2 total) - 100% Conserved")
    
    c.restoreState()

def draw_formula_anatomy(c, x, y, w, h, title="FORMULA ANATOMY & POSITION-MEANING CONTRACT"):
    """Draws formula anatomy distinguishing coefficient, symbol, subscript, and charge."""
    c.saveState()
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.setLineWidth(0.8)
    c.roundRect(x, y, w, h, 6, fill=1, stroke=1)
    
    c.setFont(FONT_BOLD, 8)
    c.setFillColor(colors.HexColor("#065F46"))
    c.drawString(x + 12, y + h - 16, title)
    
    fx = x + 50
    fy = y + 42
    
    c.setFont(FONT_BOLD, 24)
    c.setFillColor(colors.HexColor("#2563EB"))
    c.drawString(fx, fy, "2")
    
    c.setFont(FONT_BOLD, 24)
    c.setFillColor(colors.HexColor("#0F172A"))
    c.drawString(fx + 22, fy, "S")
    c.drawString(fx + 42, fy, "O")
    
    c.setFont(FONT_BOLD, 15)
    c.setFillColor(colors.HexColor("#D97706"))
    c.drawString(fx + 64, fy - 6, "4")
    
    c.setFillColor(colors.HexColor("#DC2626"))
    c.drawString(fx + 76, fy + 15, "2-")
    
    c.setFont(FONT_BOLD, 7)
    
    # Coefficient callout
    c.setFillColor(colors.HexColor("#2563EB"))
    c.setStrokeColor(colors.HexColor("#2563EB"))
    c.drawString(fx - 46, fy + 26, "COEFFICIENT = 2")
    c.setFont(FONT_NAME, 6.5)
    c.drawString(fx - 46, fy + 18, "Overall species count")
    c.line(fx - 4, fy + 22, fx + 6, fy + 14)
    
    # Subscript callout
    c.setFillColor(colors.HexColor("#D97706"))
    c.setStrokeColor(colors.HexColor("#D97706"))
    c.setFont(FONT_BOLD, 7)
    c.drawString(fx + 38, fy - 20, "SUBSCRIPT = 4")
    c.setFont(FONT_NAME, 6.5)
    c.drawString(fx + 38, fy - 28, "Atoms per sulfate ion")
    c.line(fx + 66, fy - 16, fx + 66, fy - 6)
    
    # Charge callout
    c.setFillColor(colors.HexColor("#DC2626"))
    c.setStrokeColor(colors.HexColor("#DC2626"))
    c.setFont(FONT_BOLD, 7)
    c.drawString(fx + 104, fy + 30, "IONIC CHARGE = 2-")
    c.setFont(FONT_NAME, 6.5)
    c.drawString(fx + 104, fy + 22, "Net ion charge (sum S + 4O)")
    c.line(fx + 102, fy + 22, fx + 90, fy + 16)
    
    c.restoreState()

def draw_oxidation_state_lane(c, x, y, w, h, title="OXIDATION STATE LANE & ROLE ATTACHMENT",
                             reactant_label="Fe^2+ (aq)", reactant_on="+2",
                             product_label="Fe^3+ (aq)", product_on="+3",
                             delta_text="Delta ON = +1 (Oxidation)",
                             electron_text="Loss of 1e- --> Fe^2+ is REDUCING AGENT"):
    """Draws before-and-after oxidation state progression with e- transfer."""
    c.saveState()
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.setLineWidth(0.8)
    c.roundRect(x, y, w, h, 6, fill=1, stroke=1)
    
    c.setFont(FONT_BOLD, 8)
    c.setFillColor(colors.HexColor("#065F46"))
    c.drawString(x + 12, y + h - 16, title)
    
    box_w = 88
    box_h = 44
    bx1 = x + 20
    bx2 = x + w - 20 - box_w
    by = y + 20
    
    c.setFillColor(colors.HexColor("#EFF6FF"))
    c.setStrokeColor(colors.HexColor("#93C5FD"))
    c.roundRect(bx1, by, box_w, box_h, 4, fill=1, stroke=1)
    c.setFont(FONT_BOLD, 8.5)
    c.setFillColor(colors.HexColor("#1E3A8A"))
    c.drawCentredString(bx1 + box_w / 2, by + 26, reactant_label)
    c.setFont(FONT_BOLD, 8)
    c.setFillColor(colors.HexColor("#2563EB"))
    c.drawCentredString(bx1 + box_w / 2, by + 12, f"ON = {reactant_on}")
    c.setFont(FONT_NAME, 6.5)
    c.setFillColor(colors.HexColor("#64748B"))
    c.drawCentredString(bx1 + box_w / 2, by + 3, "REACTANT")
    
    c.setFillColor(colors.HexColor("#ECFDF5"))
    c.setStrokeColor(colors.HexColor("#A7F3D0"))
    c.roundRect(bx2, by, box_w, box_h, 4, fill=1, stroke=1)
    c.setFont(FONT_BOLD, 8.5)
    c.setFillColor(colors.HexColor("#065F46"))
    c.drawCentredString(bx2 + box_w / 2, by + 26, product_label)
    c.setFont(FONT_BOLD, 8)
    c.setFillColor(colors.HexColor("#059669"))
    c.drawCentredString(bx2 + box_w / 2, by + 12, f"ON = {product_on}")
    c.setFont(FONT_NAME, 6.5)
    c.setFillColor(colors.HexColor("#64748B"))
    c.drawCentredString(bx2 + box_w / 2, by + 3, "PRODUCT")
    
    arr_start = bx1 + box_w + 8
    arr_end = bx2 - 8
    c.setStrokeColor(colors.HexColor("#0F766E"))
    c.setLineWidth(1.8)
    c.line(arr_start, by + box_h / 2, arr_end, by + box_h / 2)
    p = c.beginPath()
    p.moveTo(arr_end, by + box_h / 2)
    p.lineTo(arr_end - 6, by + box_h / 2 + 3)
    p.lineTo(arr_end - 6, by + box_h / 2 - 3)
    p.close()
    c.setFillColor(colors.HexColor("#0F766E"))
    c.drawPath(p, fill=1, stroke=0)
    
    c.setFont(FONT_BOLD, 7.5)
    c.drawCentredString((arr_start + arr_end) / 2, by + box_h / 2 + 7, delta_text)
    c.setFont(FONT_NAME, 6.8)
    c.setFillColor(colors.HexColor("#DC2626"))
    c.drawCentredString((arr_start + arr_end) / 2, by + box_h / 2 - 11, electron_text)
    
    c.restoreState()

# ==============================================================================
# MATHEMATICS PRIMITIVES
# ==============================================================================

def draw_coordinate_grid_2d(c, x, y, w, h, title="2D CARTESIAN PLANE & SLOPE TRIANGLE"):
    """Draws a 2D coordinate grid with points (1,2) and (4,6), distance, and slope rise/run."""
    c.saveState()
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.setLineWidth(0.8)
    c.roundRect(x, y, w, h, 6, fill=1, stroke=1)
    
    c.setFont(FONT_BOLD, 8)
    c.setFillColor(colors.HexColor("#1E3A8A"))
    c.drawString(x + 12, y + h - 16, title)
    
    gx = x + 35
    gy = y + 24
    gw = w - 70
    gh = h - 48
    
    c.setStrokeColor(colors.HexColor("#F1F5F9"))
    c.setLineWidth(0.5)
    for i in range(1, 6):
        c.line(gx + i * (gw / 6), gy, gx + i * (gw / 6), gy + gh)
        c.line(gx, gy + i * (gh / 6), gx + gw, gy + i * (gh / 6))
        
    # Axes
    c.setStrokeColor(colors.HexColor("#334155"))
    c.setLineWidth(1.2)
    c.line(gx, gy, gx + gw, gy)
    c.line(gx, gy, gx, gy + gh)
    
    c.setFont(FONT_BOLD, 7.5)
    c.setFillColor(colors.HexColor("#334155"))
    c.drawString(gx + gw - 4, gy - 10, "x")
    c.drawString(gx - 10, gy + gh - 4, "y")
    
    p1_x = gx + gw * 0.25
    p1_y = gy + gh * 0.28
    p2_x = gx + gw * 0.75
    p2_y = gy + gh * 0.78
    
    c.setStrokeColor(colors.HexColor("#93C5FD"))
    c.setLineWidth(1.0)
    c.setDash(3, 2)
    c.line(p1_x, p1_y, p2_x, p1_y)
    c.line(p2_x, p1_y, p2_x, p2_y)
    c.setDash()
    
    c.setStrokeColor(colors.HexColor("#2563EB"))
    c.setLineWidth(1.8)
    c.line(p1_x - 10, p1_y - 8, p2_x + 10, p2_y + 8)
    
    c.setFillColor(colors.HexColor("#1E3A8A"))
    c.circle(p1_x, p1_y, 3.5, fill=1, stroke=0)
    c.circle(p2_x, p2_y, 3.5, fill=1, stroke=0)
    
    c.setFont(FONT_BOLD, 7)
    c.drawString(p1_x - 30, p1_y + 4, "A (x_1, y_1)")
    c.drawString(p2_x + 6, p2_y + 2, "B (x_2, y_2)")
    
    c.setFont(FONT_NAME, 6.5)
    c.setFillColor(colors.HexColor("#0284C7"))
    c.drawCentredString((p1_x + p2_x) / 2, p1_y - 8, "Run Delta x = x_2 - x_1")
    c.drawString(p2_x + 6, (p1_y + p2_y) / 2 - 2, "Rise Delta y = y_2 - y_1")
    
    c.setFont(FONT_BOLD, 7.5)
    c.setFillColor(colors.HexColor("#1E3A8A"))
    c.drawString(gx + gw * 0.3, gy + gh * 0.85, "Slope m = Delta y / Delta x")
    
    c.restoreState()

def draw_combinatorial_slots(c, x, y, w, h, title="COMBINATORIAL SLOT MULTIPLICATION MODEL"):
    """Draws visual slot boxes [_][_][_][_] with restrictions and choice counts."""
    c.saveState()
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.setLineWidth(0.8)
    c.roundRect(x, y, w, h, 6, fill=1, stroke=1)
    
    c.setFont(FONT_BOLD, 8)
    c.setFillColor(colors.HexColor("#1E3A8A"))
    c.drawString(x + 12, y + h - 16, title)
    
    slot_w = 42
    slot_h = 32
    gap = 22
    total_slots_w = 4 * slot_w + 3 * gap
    start_x = x + (w - total_slots_w) / 2
    sy = y + 26
    
    slots_data = [
        {"name": "Thousands", "restr": "No Zero", "choices": "9"},
        {"name": "Hundreds", "restr": "Distinct", "choices": "9"},
        {"name": "Tens", "restr": "Distinct", "choices": "8"},
        {"name": "Units", "restr": "Even (0,2,4,6,8)", "choices": "5"}
    ]
    
    for i, s in enumerate(slots_data):
        curr_x = start_x + i * (slot_w + gap)
        c.setFillColor(colors.HexColor("#EFF6FF"))
        c.setStrokeColor(colors.HexColor("#3B82F6"))
        c.setLineWidth(1.2)
        c.roundRect(curr_x, sy, slot_w, slot_h, 4, fill=1, stroke=1)
        
        c.setFont(FONT_BOLD, 14)
        c.setFillColor(colors.HexColor("#1E3A8A"))
        c.drawCentredString(curr_x + slot_w / 2, sy + 10, s["choices"])
        
        if i < 3:
            c.setFont(FONT_BOLD, 11)
            c.setFillColor(colors.HexColor("#64748B"))
            c.drawCentredString(curr_x + slot_w + gap / 2, sy + 11, "x")
            
        c.setFont(FONT_BOLD, 6.5)
        c.setFillColor(colors.HexColor("#DC2626"))
        c.drawCentredString(curr_x + slot_w / 2, sy + slot_h + 9, s["restr"])
        
        c.setFont(FONT_NAME, 6.5)
        c.setFillColor(colors.HexColor("#475569"))
        c.drawCentredString(curr_x + slot_w / 2, sy - 9, s["name"])
        
    c.restoreState()
