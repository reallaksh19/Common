"""
Graphs Module for Grade 9 Visual Primitives.
Provides:
- CartesianPlotter2D: Mathematical 2D plotting engine with grid, axes, points, lines, curves, and slope triangles
- KinematicGraphRenderer: Kinematic calculus graphs (s-t, v-t, a-t) with automated Riemann area polygons
- StatisticalPlotter: Continuous class-interval histograms and frequency polygons
- ThermalCurvePlotter: Phase change temperature-time heating/cooling plateau curves
"""

import math
from reportlab.lib import colors
from .base import FONT_NAME, FONT_BOLD, Palette, draw_card_box, draw_arrow, draw_pill_badge


class CartesianPlotter2D:
    """
    Translates mathematical domain [x_min, x_max] x [y_min, y_max]
    to canvas rect [x, x + w] x [y, y + h] with exact linear scaling.
    """
    def __init__(self, c, x, y, w, h, x_domain=(-1, 6), y_domain=(-1, 7),
                 grid=True, pad_left=35, pad_bottom=25, pad_right=15, pad_top=20):
        self.c = c
        self.box_x = x
        self.box_y = y
        self.box_w = w
        self.box_h = h
        self.x_min, self.x_max = x_domain
        self.y_min, self.y_max = y_domain
        self.grid = grid
        
        # Plot viewport inside the bounding box
        self.plot_x = x + pad_left
        self.plot_y = y + pad_bottom
        self.plot_w = w - pad_left - pad_right
        self.plot_h = h - pad_bottom - pad_top
        
    def to_canvas(self, mx, my):
        """Converts mathematical coordinates (mx, my) to canvas coordinates."""
        cx = self.plot_x + (mx - self.x_min) / (self.x_max - self.x_min) * self.plot_w
        cy = self.plot_y + (my - self.y_min) / (self.y_max - self.y_min) * self.plot_h
        return cx, cy
        
    def draw_axes(self, x_label="x", y_label="y", x_step=1, y_step=1):
        """Draws axes with ticks and optional grid."""
        c = self.c
        c.saveState()
        
        # Grid lines
        if self.grid:
            c.setStrokeColor(Palette.BORDER_LIGHT)
            c.setLineWidth(0.5)
            c.setDash(2, 2)
            
            # Vertical grid
            cur_x = math.ceil(self.x_min)
            while cur_x <= self.x_max:
                if cur_x != 0:
                    cx, _ = self.to_canvas(cur_x, 0)
                    c.line(cx, self.plot_y, cx, self.plot_y + self.plot_h)
                cur_x += x_step
                
            # Horizontal grid
            cur_y = math.ceil(self.y_min)
            while cur_y <= self.y_max:
                if cur_y != 0:
                    _, cy = self.to_canvas(0, cur_y)
                    c.line(self.plot_x, cy, self.plot_x + self.plot_w, cy)
                cur_y += y_step
            c.setDash()
            
        # Axis lines (at x=0 and y=0 if in range, else boundary)
        origin_x = 0 if self.x_min <= 0 <= self.x_max else self.x_min
        origin_y = 0 if self.y_min <= 0 <= self.y_max else self.y_min
        
        ax_origin_x, _ = self.to_canvas(origin_x, 0)
        _, ax_origin_y = self.to_canvas(0, origin_y)
        
        # Draw X Axis
        c.setStrokeColor(Palette.TEXT_SECONDARY)
        c.setLineWidth(1.2)
        c.line(self.plot_x, ax_origin_y, self.plot_x + self.plot_w, ax_origin_y)
        # X Arrow
        draw_arrow(c, self.plot_x + self.plot_w - 5, ax_origin_y, 
                   self.plot_x + self.plot_w, ax_origin_y, Palette.TEXT_SECONDARY, line_width=1.2, head_len=5, head_width=2.5)
        c.setFont(FONT_BOLD, 7.5)
        c.setFillColor(Palette.TEXT_PRIMARY)
        c.drawString(self.plot_x + self.plot_w + 3, ax_origin_y - 3, x_label)
        
        # Draw Y Axis
        c.line(ax_origin_x, self.plot_y, ax_origin_x, self.plot_y + self.plot_h)
        # Y Arrow
        draw_arrow(c, ax_origin_x, self.plot_y + self.plot_h - 5,
                   ax_origin_x, self.plot_y + self.plot_h, Palette.TEXT_SECONDARY, line_width=1.2, head_len=5, head_width=2.5)
        c.drawString(ax_origin_x - 3, self.plot_y + self.plot_h + 5, y_label)
        
        # Ticks and numeric labels
        c.setFont(FONT_NAME, 6.5)
        c.setFillColor(Palette.TEXT_MUTED)
        
        cur_x = math.ceil(self.x_min)
        while cur_x <= self.x_max:
            if cur_x != 0:
                cx, cy = self.to_canvas(cur_x, origin_y)
                c.setStrokeColor(Palette.TEXT_MUTED)
                c.setLineWidth(0.8)
                c.line(cx, cy - 2.5, cx, cy + 2.5)
                c.drawCentredString(cx, cy - 9, str(cur_x))
            cur_x += x_step
            
        cur_y = math.ceil(self.y_min)
        while cur_y <= self.y_max:
            if cur_y != 0:
                cx, cy = self.to_canvas(origin_x, cur_y)
                c.setStrokeColor(Palette.TEXT_MUTED)
                c.setLineWidth(0.8)
                c.line(cx - 2.5, cy, cx + 2.5, cy)
                c.drawRightString(cx - 5, cy - 2, str(cur_y))
            cur_y += y_step
            
        # Origin (0,0) label
        if self.x_min <= 0 <= self.x_max and self.y_min <= 0 <= self.y_max:
            cx, cy = self.to_canvas(0, 0)
            c.drawRightString(cx - 4, cy - 9, "O")
            
        c.restoreState()

    def plot_point(self, mx, my, label=None, color=None, radius=2.5, project_axes=True):
        """Plots a single point with projection lines and text label."""
        c = self.c
        c.saveState()
        if color is None:
            color = Palette.MATH_DARK
            
        cx, cy = self.to_canvas(mx, my)
        
        if project_axes:
            c.setStrokeColor(colors.HexColor("#94A3B8"))
            c.setLineWidth(0.7)
            c.setDash(2, 2)
            ox, _ = self.to_canvas(0, 0)
            _, oy = self.to_canvas(0, 0)
            c.line(cx, oy, cx, cy)
            c.line(ox, cy, cx, cy)
            c.setDash()
            
        # Marker dot
        c.setFillColor(color)
        c.circle(cx, cy, radius, fill=1, stroke=0)
        
        # Label
        if label:
            c.setFont(FONT_BOLD, 7)
            c.setFillColor(color)
            c.drawString(cx + 4, cy + 3, label)
            
        c.restoreState()

    def plot_line_segment(self, x1, y1, x2, y2, color=None, width=1.4):
        """Draws a line segment between two math coordinates."""
        if color is None:
            color = Palette.MATH_MED
        cx1, cy1 = self.to_canvas(x1, y1)
        cx2, cy2 = self.to_canvas(x2, y2)
        self.c.saveState()
        self.c.setStrokeColor(color)
        self.c.setLineWidth(width)
        self.c.line(cx1, cy1, cx2, cy2)
        self.c.restoreState()

    def plot_slope_triangle(self, x1, y1, x2, y2, color=None):
        """Draws a rise-run right-angled triangle between (x1, y1) and (x2, y2)."""
        c = self.c
        c.saveState()
        if color is None:
            color = Palette.DANGER
            
        cx1, cy1 = self.to_canvas(x1, y1)
        cx2, cy2 = self.to_canvas(x2, y2)
        corner_x, corner_y = cx2, cy1
        
        # Shaded triangle
        c.setFillColor(colors.HexColor("#FEF2F2"))
        p = c.beginPath()
        p.moveTo(cx1, cy1)
        p.lineTo(corner_x, corner_y)
        p.lineTo(cx2, cy2)
        p.close()
        c.drawPath(p, fill=1, stroke=0)
        
        # Rise and Run lines
        c.setStrokeColor(color)
        c.setLineWidth(1.0)
        c.setDash(3, 2)
        c.line(cx1, cy1, corner_x, corner_y) # Run (dx)
        c.line(corner_x, corner_y, cx2, cy2) # Rise (dy)
        c.setDash()
        
        # Hypotenuse
        c.setStrokeColor(Palette.MATH_DARK)
        c.setLineWidth(1.5)
        c.line(cx1, cy1, cx2, cy2)
        
        # Labels
        c.setFont(FONT_NAME, 6.8)
        c.setFillColor(color)
        run_text = f"dx = {abs(x2 - x1)}"
        rise_text = f"dy = {abs(y2 - y1)}"
        c.drawCentredString((cx1 + corner_x) / 2, corner_y - 8, run_text)
        c.drawString(corner_x + 4, (corner_y + cy2) / 2 - 2, rise_text)
        
        c.restoreState()

    @staticmethod
    def draw_slope_bridge(c, x, y, w, h, title="2D CARTESIAN FRAME & SLOPE-DISTANCE BRIDGE",
                          p1=(1, 2), p2=(4, 6)):
        """Convenience method rendering 2D frame with points, slope triangle, and distance badge."""
        c.saveState()
        draw_card_box(c, x, y, w, h, title=title, title_color=Palette.MATH_DARK)
        
        x1, y1 = p1
        x2, y2 = p2
        dx = x2 - x1
        dy = y2 - y1
        dist = math.sqrt(dx**2 + dy**2)
        slope = dy / dx if dx != 0 else 0
        
        plotter = CartesianPlotter2D(c, x, y, w, h, x_domain=(0, 6), y_domain=(0, 7),
                                     grid=True, pad_left=32, pad_bottom=22, pad_right=14, pad_top=24)
        plotter.draw_axes(x_label="x", y_label="y", x_step=1, y_step=1)
        plotter.plot_slope_triangle(x1, y1, x2, y2)
        plotter.plot_point(x1, y1, f"A ({x1}, {y1})", color=Palette.MATH_DARK)
        plotter.plot_point(x2, y2, f"B ({x2}, {y2})", color=Palette.MATH_DARK)
        
        # Distance & slope badge
        badge = f"m = dy/dx = {dy}/{dx} = {slope:.2f}  |  d = sqrt({dx}^2 + {dy}^2) = {dist:.2f}"
        draw_pill_badge(c, x + w - 195, y + h - 18, badge,
                        colors.HexColor("#EFF6FF"), Palette.MATH_DARK, font_size=6.8, height=14, padding_x=6)
        c.restoreState()


class KinematicGraphRenderer:
    """
    Renders deterministic kinematic graphs (v-t, s-t, a-t) with shaded Riemann integral areas.
    """
    @staticmethod
    def draw_vt_graph(c, x, y, w, h, title="VELOCITY-TIME (v-t) GRAPH & INTEGRAL AREA",
                      u=0.0, v=20.0, t_accel=5.0, t_const=0.0,
                      v_unit="m/s", t_unit="s",
                      color_rect="#DBEAFE", color_tri="#CCFBF1"):
        """
        Draws a complete velocity-time graph with decomposed displacement area.
        Displacement s = u*t + 0.5*(v-u)*t
        """
        c.saveState()
        draw_card_box(c, x, y, w, h, title=title, title_color=Palette.PHYSICS_DARK)
        
        t_total = t_accel + t_const
        y_max = max(v * 1.2, 10.0)
        x_max = max(t_total * 1.2, 6.0)
        
        plotter = CartesianPlotter2D(c, x, y, w, h,
                                     x_domain=(0, x_max), y_domain=(0, y_max),
                                     grid=True, pad_left=32, pad_bottom=22, pad_right=14, pad_top=24)
        plotter.draw_axes(x_label=f"t ({t_unit})", y_label=f"v ({v_unit})",
                          x_step=max(1, int(t_total / 5)), y_step=max(2, int(y_max / 5)))
        
        # Shaded areas
        # 1. Rectangle (u * t_accel) if u > 0
        if u > 0:
            c.setFillColor(colors.HexColor(color_rect))
            c.setStrokeColor(colors.HexColor("#93C5FD"))
            c.setLineWidth(0.8)
            cx0, cy0 = plotter.to_canvas(0, 0)
            cxt, cyu = plotter.to_canvas(t_accel, u)
            p = c.beginPath()
            p.moveTo(cx0, cy0)
            p.lineTo(cxt, cy0)
            p.lineTo(cxt, cyu)
            p.lineTo(cx0, cyu)
            p.close()
            c.drawPath(p, fill=1, stroke=1)
            
            c.setFont(FONT_NAME, 6.8)
            c.setFillColor(colors.HexColor("#1E40AF"))
            c.drawCentredString((cx0 + cxt) / 2, (cy0 + cyu) / 2 - 2, f"Area 1 = u*t = {u*t_accel:.1f} m")
            
        # 2. Triangle (0.5 * (v - u) * t_accel)
        c.setFillColor(colors.HexColor(color_tri))
        c.setStrokeColor(colors.HexColor("#99F6E4"))
        c.setLineWidth(0.8)
        cx0, cyu = plotter.to_canvas(0, u)
        cxt, cy0 = plotter.to_canvas(t_accel, 0)
        cxt, cyv = plotter.to_canvas(t_accel, v)
        cxt, cyu_right = plotter.to_canvas(t_accel, u)
        
        p = c.beginPath()
        p.moveTo(cx0, cyu)
        p.lineTo(cxt, cyu_right)
        p.lineTo(cxt, cyv)
        p.close()
        c.drawPath(p, fill=1, stroke=1)
        
        tri_area = 0.5 * (v - u) * t_accel
        c.setFont(FONT_NAME, 6.8)
        c.setFillColor(colors.HexColor("#0F766E"))
        c.drawCentredString((cx0 + cxt * 2) / 3, (cyu * 2 + cyv) / 3 - 2, f"Area 2 = 1/2*a*t^2 = {tri_area:.1f} m")
        
        # Velocity slope line
        c.setStrokeColor(Palette.PHYSICS_DARK)
        c.setLineWidth(1.8)
        c.line(cx0, cyu, cxt, cyv)
        
        # Total displacement badge
        total_disp = u * t_accel + tri_area
        accel = (v - u) / t_accel if t_accel > 0 else 0
        badge_text = f"a = {accel:.1f} m/s^2  |  s_total = {total_disp:.1f} m"
        draw_pill_badge(c, x + w - 170, y + h - 18, badge_text,
                        colors.HexColor("#EFF6FF"), Palette.PHYSICS_DARK, font_size=7, height=14, padding_x=6)
        
        # Markers
        plotter.plot_point(0, u, label=f"u={u:g}", color=Palette.PHYSICS_DARK, project_axes=True)
        plotter.plot_point(t_accel, v, label=f"({t_accel:g}, {v:g})", color=Palette.PHYSICS_DARK, project_axes=True)
        
        c.restoreState()


class StatisticalPlotter:
    """
    Renders continuous class-interval histograms and frequency polygons.
    """
    @staticmethod
    def draw_histogram(c, x, y, w, h, intervals, title="FREQUENCY DISTRIBUTION HISTOGRAM",
                       x_label="Class Interval", y_label="Frequency"):
        """
        intervals: list of tuples: (lower, upper, frequency)
        e.g. [(0, 10, 5), (10, 20, 12), (20, 30, 8), (30, 40, 3)]
        """
        c.saveState()
        draw_card_box(c, x, y, w, h, title=title, title_color=Palette.MATH_DARK)
        
        x_min = min(i[0] for i in intervals)
        x_max = max(i[1] for i in intervals)
        y_max = max(i[2] for i in intervals) * 1.2
        
        plotter = CartesianPlotter2D(c, x, y, w, h,
                                     x_domain=(x_min, x_max), y_domain=(0, y_max),
                                     grid=True, pad_left=32, pad_bottom=22, pad_right=14, pad_top=24)
        plotter.draw_axes(x_label=x_label, y_label=y_label,
                          x_step=int((intervals[0][1] - intervals[0][0])), y_step=max(1, int(y_max / 5)))
        
        # Draw Bars
        for (low, high, freq) in intervals:
            cx_low, cy_0 = plotter.to_canvas(low, 0)
            cx_high, cy_f = plotter.to_canvas(high, freq)
            bar_w = cx_high - cx_low
            bar_h = cy_f - cy_0
            
            c.setFillColor(colors.HexColor("#EFF6FF"))
            c.setStrokeColor(Palette.MATH_MED)
            c.setLineWidth(1.0)
            c.rect(cx_low, cy_0, bar_w, bar_h, fill=1, stroke=1)
            
            # Frequency count on top of bar
            c.setFont(FONT_BOLD, 7)
            c.setFillColor(Palette.MATH_DARK)
            c.drawCentredString(cx_low + bar_w / 2, cy_f + 3, str(freq))
            
        c.restoreState()


class ThermalCurvePlotter:
    """
    Renders temperature vs time heating/cooling curves with latent heat plateaus.
    """
    @staticmethod
    def draw_heating_curve(c, x, y, w, h, melting_pt=0.0, boiling_pt=100.0,
                           title="HEATING CURVE & PHASE CHANGE PLATEAUS"):
        c.saveState()
        draw_card_box(c, x, y, w, h, title=title, title_color=Palette.CHEM_DARK)
        
        plotter = CartesianPlotter2D(c, x, y, w, h,
                                     x_domain=(0, 10), y_domain=(-20, 130),
                                     grid=True, pad_left=35, pad_bottom=22, pad_right=14, pad_top=24)
        plotter.draw_axes(x_label="Time (min)", y_label="Temp (deg C)", x_step=2, y_step=25)
        
        # Segments:
        # 1. Solid heating: (0, -15) -> (2, melting_pt)
        # 2. Melting plateau: (2, melting_pt) -> (4, melting_pt)
        # 3. Liquid heating: (4, melting_pt) -> (6, boiling_pt)
        # 4. Boiling plateau: (6, boiling_pt) -> (8, boiling_pt)
        # 5. Gas heating: (8, boiling_pt) -> (10, 125)
        pts = [
            (0, -15),
            (2, melting_pt),
            (4, melting_pt),
            (6, boiling_pt),
            (8, boiling_pt),
            (10, 125)
        ]
        
        # Draw curve
        c.setStrokeColor(Palette.CHEM_MED)
        c.setLineWidth(1.8)
        for i in range(len(pts) - 1):
            cx1, cy1 = plotter.to_canvas(*pts[i])
            cx2, cy2 = plotter.to_canvas(*pts[i+1])
            c.line(cx1, cy1, cx2, cy2)
            
        # Draw Plateaus callouts
        # Melting
        cx_m1, cy_m = plotter.to_canvas(2, melting_pt)
        cx_m2, _ = plotter.to_canvas(4, melting_pt)
        c.setFont(FONT_BOLD, 6.8)
        c.setFillColor(Palette.CHEM_DARK)
        c.drawCentredString((cx_m1 + cx_m2) / 2, cy_m + 4, f"Melting ({melting_pt:g} C)")
        
        # Boiling
        cx_b1, cy_b = plotter.to_canvas(6, boiling_pt)
        cx_b2, _ = plotter.to_canvas(8, boiling_pt)
        c.drawCentredString((cx_b1 + cx_b2) / 2, cy_b + 4, f"Boiling ({boiling_pt:g} C)")
        
        c.restoreState()
