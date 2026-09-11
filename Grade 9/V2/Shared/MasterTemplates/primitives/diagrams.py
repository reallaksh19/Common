"""
Diagrams Module for Grade 9 Visual Primitives.
Provides:
- PlaneGeometryRenderer: Parallel lines & transversals, congruent triangles, and circle subtended angles
- Vector1DDiagram: 1D coordinate reference frames with journey legs and displacement resultant
- FreeBodyDiagramRenderer: Rigid blocks with multi-directional force vectors
- WaveformRenderer: Transverse sinusoidal waves (lambda, A) and longitudinal compression/rarefaction bands
- BohrAtomRenderer: Central nucleus (p, n) with concentric K, L, M electron shells and orbital dots
- ParticleLatticeDiagram: Johnstone submicroscopic Dalton reaction boxes
- OxidationLaneDiagram: Declarative before-and-after redox tracking and agent role assignment
- CombinatorialSlotDiagram: Parameterized decision slots for counting problems
"""

import math
from reportlab.lib import colors
from .base import (FONT_NAME, FONT_BOLD, Palette, draw_card_box, draw_arrow, draw_pill_badge)


class PlaneGeometryRenderer:
    """
    Renders core Euclidean geometry figures for Class 9 Mathematics.
    """
    @staticmethod
    def draw_parallel_transversal(c, x, y, w, h, angle_deg=65,
                                  title="PARALLEL LINES & TRANSVERSAL (ALTERNATE INTERIOR ANGLES)"):
        """Draws two parallel horizontal lines cut by a transversal line."""
        c.saveState()
        draw_card_box(c, x, y, w, h, title=title, title_color=Palette.MATH_DARK)
        
        y1 = y + h * 0.68
        y2 = y + h * 0.32
        x_left = x + 30
        x_right = x + w - 30
        
        # Parallel Line 1 (Line AB)
        c.setStrokeColor(Palette.MATH_DARK)
        c.setLineWidth(1.4)
        c.line(x_left, y1, x_right, y1)
        # Parallel marks (double chevron)
        c.drawString(x_left + 15, y1 + 5, "Line l")
        c.drawString(x_right - 25, y1 + 5, "-->")
        
        # Parallel Line 2 (Line CD)
        c.line(x_left, y2, x_right, y2)
        c.drawString(x_left + 15, y2 + 5, "Line m")
        c.drawString(x_right - 25, y2 + 5, "-->")
        
        # Transversal Line
        rad = math.radians(angle_deg)
        dx = (y1 - y2) / math.tan(rad)
        mid_x = (x_left + x_right) / 2
        
        p1_x = mid_x - dx * 0.7
        p1_y = y + h * 0.85
        p2_x = mid_x + dx * 0.7
        p2_y = y + h * 0.15
        
        c.setStrokeColor(Palette.DANGER)
        c.setLineWidth(1.5)
        c.line(p1_x, p1_y, p2_x, p2_y)
        c.drawString(p1_x + 5, p1_y - 2, "Transversal t")
        
        # Intersection points
        # Intersection with y1:
        int1_x = p1_x + (y1 - p1_y) * (p2_x - p1_x) / (p2_y - p1_y)
        # Intersection with y2:
        int2_x = p1_x + (y2 - p1_y) * (p2_x - p1_x) / (p2_y - p1_y)
        
        # Angle arcs (Alternate Interior Angles: Angle 1 and Angle 2)
        c.setStrokeColor(Palette.MATH_MED)
        c.setLineWidth(1.2)
        
        # Arc at int1 (lower-right quadrant of int1)
        c.arc(int1_x - 14, y1 - 14, int1_x + 14, y1 + 14, 270 + (90 - angle_deg), angle_deg)
        c.setFont(FONT_BOLD, 7.5)
        c.setFillColor(Palette.MATH_DARK)
        c.drawString(int1_x + 10, y1 - 12, f"Angle 1 = {angle_deg} deg")
        
        # Arc at int2 (upper-left quadrant of int2)
        c.arc(int2_x - 14, y2 - 14, int2_x + 14, y2 + 14, 90 + (90 - angle_deg), angle_deg)
        c.drawString(int2_x - 70, y2 + 8, f"Angle 2 = {angle_deg} deg")
        
        # Invariant badge
        badge_text = f"Parallelism Invariant: Angle 1 = Angle 2 = {angle_deg} deg (Alt. Int.)"
        draw_pill_badge(c, x + 25, y + 15, badge_text, colors.HexColor("#EFF6FF"), Palette.MATH_DARK, font_size=7, height=14)
        
        c.restoreState()

    @staticmethod
    def draw_triangle_with_altitude(c, x, y, w, h, base=80, height=50,
                                    title="CONGRUENCE & ALTITUDE IN TRIANGLE ABC"):
        """Draws triangle ABC with perpendicular altitude from A to BC."""
        c.saveState()
        draw_card_box(c, x, y, w, h, title=title, title_color=Palette.MATH_DARK)
        
        cx = x + w / 2
        cy = y + 35
        
        b_x = cx - base / 2
        b_y = cy
        c_x = cx + base / 2
        c_y = cy
        a_x = cx - 10
        a_y = cy + height
        
        # Draw sides
        c.setStrokeColor(Palette.MATH_DARK)
        c.setLineWidth(1.5)
        c.line(b_x, b_y, c_x, c_y) # BC
        c.line(b_x, b_y, a_x, a_y) # AB
        c.line(c_x, c_y, a_x, a_y) # AC
        
        # Vertex Labels
        c.setFont(FONT_BOLD, 8)
        c.setFillColor(Palette.TEXT_PRIMARY)
        c.drawRightString(b_x - 4, b_y - 3, "B")
        c.drawString(c_x + 4, c_y - 3, "C")
        c.drawCentredString(a_x, a_y + 5, "A")
        
        # Altitude AD perpendicular to BC
        d_x = a_x
        d_y = cy
        c.setStrokeColor(Palette.DANGER)
        c.setLineWidth(1.0)
        c.setDash(2, 2)
        c.line(a_x, a_y, d_x, d_y)
        c.setDash()
        
        # Right angle mark at D
        mark_size = 6
        c.setStrokeColor(Palette.TEXT_MUTED)
        c.line(d_x + mark_size, d_y, d_x + mark_size, d_y + mark_size)
        c.line(d_x, d_y + mark_size, d_x + mark_size, d_y + mark_size)
        c.drawString(d_x - 2, d_y - 10, "D")
        
        # Side congruence ticks on AB and AC if isosceles
        # Tick on AB
        mid_ab_x = (a_x + b_x) / 2
        mid_ab_y = (a_y + b_y) / 2
        c.line(mid_ab_x - 3, mid_ab_y - 3, mid_ab_x + 3, mid_ab_y + 3)
        # Tick on AC
        mid_ac_x = (a_x + c_x) / 2
        mid_ac_y = (a_y + c_y) / 2
        c.line(mid_ac_x - 3, mid_ac_y + 3, mid_ac_x + 3, mid_ac_y - 3)
        
        c.setFont(FONT_NAME, 6.8)
        c.setFillColor(Palette.TEXT_MUTED)
        c.drawCentredString(cx, cy - 20, "Altitude AD perpendicular to BC  |  AB = AC  =>  BD = CD")
        
        c.restoreState()

    @staticmethod
    def draw_circle_subtended_angles(c, x, y, w, h, theta_deg=35,
                                    title="CIRCLE THEOREM: ANGLE AT CENTER IS DOUBLE ANGLE AT CIRCUMFERENCE"):
        """Draws a circle with central angle 2*theta and inscribed circumference angle theta."""
        c.saveState()
        draw_card_box(c, x, y, w, h, title=title, title_color=Palette.MATH_DARK)
        
        center_x = x + w / 2
        center_y = y + h * 0.44
        radius = min(w, h) * 0.32
        
        # Circle outline
        c.setStrokeColor(Palette.BORDER_CARD)
        c.setFillColor(colors.HexColor("#FFFFFF"))
        c.setLineWidth(1.2)
        c.circle(center_x, center_y, radius, fill=1, stroke=1)
        
        # Center O
        c.setFillColor(Palette.TEXT_PRIMARY)
        c.circle(center_x, center_y, 2, fill=1, stroke=0)
        c.setFont(FONT_BOLD, 7.5)
        c.drawString(center_x + 4, center_y - 3, "O")
        
        # Arc points A and B at bottom
        ang_a = math.radians(220)
        ang_b = math.radians(320)
        ax = center_x + radius * math.cos(ang_a)
        ay = center_y + radius * math.sin(ang_a)
        bx = center_x + radius * math.cos(ang_b)
        by = center_y + radius * math.sin(ang_b)
        
        # Point P at top of circle
        ang_p = math.radians(95)
        px = center_x + radius * math.cos(ang_p)
        py = center_y + radius * math.sin(ang_p)
        
        # Central angle lines: OA and OB
        c.setStrokeColor(Palette.PHYSICS_DARK)
        c.setLineWidth(1.2)
        c.line(center_x, center_y, ax, ay)
        c.line(center_x, center_y, bx, by)
        
        # Circumference angle lines: PA and PB
        c.setStrokeColor(Palette.MATH_MED)
        c.setLineWidth(1.1)
        c.line(px, py, ax, ay)
        c.line(px, py, bx, by)
        
        # Vertex labels
        c.setFont(FONT_BOLD, 7.5)
        c.setFillColor(Palette.TEXT_PRIMARY)
        c.drawRightString(ax - 4, ay - 4, "A")
        c.drawString(bx + 4, by - 4, "B")
        c.drawCentredString(px, py + 4, "P")
        
        # Labels and theorem badge
        central_angle = 2 * theta_deg
        c.setFont(FONT_BOLD, 7)
        c.setFillColor(Palette.PHYSICS_DARK)
        c.drawCentredString(center_x, center_y - 18, f"Angle AOB = 2*theta = {central_angle} deg")
        
        c.setFillColor(Palette.MATH_MED)
        c.drawCentredString(px, py - 18, f"Angle APB = theta = {theta_deg} deg")
        
        badge = f"Theorem: Angle AOB = 2 * Angle APB ({central_angle} deg = 2 * {theta_deg} deg)"
        draw_pill_badge(c, x + 20, y + 10, badge, colors.HexColor("#EFF6FF"), Palette.MATH_DARK, font_size=6.8, height=13)
        
        c.restoreState()


class Vector1DDiagram:
    """
    Renders 1D coordinate axis with signed journey legs and displacement resultant.
    """
    @staticmethod
    def draw(c, x, y, w, h, title="1D REFERENCE FRAME & DISPLACEMENT STRIP",
             origin_val=0, ticks=(-3, -2, -1, 0, 1, 2, 3, 4, 5),
             legs=None, resultant_start=0, resultant_end=2):
        c.saveState()
        draw_card_box(c, x, y, w, h, title=title, title_color=Palette.PHYSICS_DARK)
        
        if legs is None:
            legs = [
                {"start": 0, "end": 5, "label": "Leg 1: +5 m (East)", "color": "#2563EB", "y_off": 16},
                {"start": 5, "end": 2, "label": "Leg 2: -3 m (West)", "color": "#DC2626", "y_off": 26}
            ]
            
        axis_y = y + 44
        axis_start = x + 30
        axis_end = x + w - 40
        axis_w = axis_end - axis_start
        
        # Main axis
        c.setStrokeColor(Palette.TEXT_SECONDARY)
        c.setLineWidth(1.5)
        c.line(axis_start, axis_y, axis_end, axis_y)
        draw_arrow(c, axis_end - 6, axis_y, axis_end, axis_y, Palette.TEXT_SECONDARY, line_width=1.5)
        
        c.setFont(FONT_BOLD, 7.5)
        c.setFillColor(Palette.TEXT_PRIMARY)
        c.drawString(axis_end - 2, axis_y + 8, "+ x (m) East -->")
        
        tick_spacing = axis_w / (len(ticks) + 0.5)
        tick_pos = {}
        c.setFont(FONT_NAME, 7)
        for i, val in enumerate(ticks):
            tx = axis_start + 15 + i * tick_spacing
            tick_pos[val] = tx
            c.setStrokeColor(Palette.TEXT_MUTED)
            c.setLineWidth(1.0 if val != origin_val else 1.8)
            c.line(tx, axis_y - 4, tx, axis_y + 4)
            c.setFillColor(Palette.TEXT_PRIMARY if val != origin_val else Palette.PHYSICS_DARK)
            c.drawCentredString(tx, axis_y - 13, str(val))
            
        # Draw journey legs
        for leg in legs:
            sx = tick_pos.get(leg["start"], axis_start)
            ex = tick_pos.get(leg["end"], axis_end)
            ly = axis_y + leg["y_off"]
            leg_color = colors.HexColor(leg["color"])
            
            c.setStrokeColor(leg_color)
            c.setLineWidth(1.2)
            c.line(sx, ly, ex, ly)
            draw_arrow(c, (sx + ex)/2, ly, ex, ly, leg_color, line_width=1.2, head_len=4, head_width=2.5)
            
            c.setFont(FONT_NAME, 6.8)
            c.setFillColor(leg_color)
            c.drawCentredString((sx + ex) / 2, ly + 3.5, leg["label"])
            
        # Resultant displacement vector
        res_sx = tick_pos.get(resultant_start, axis_start)
        res_ex = tick_pos.get(resultant_end, axis_end)
        res_y = axis_y - 25
        
        res_color = Palette.PHYSICS_DARK
        c.setStrokeColor(res_color)
        c.setLineWidth(1.5)
        c.line(res_sx, res_y, res_ex, res_y)
        draw_arrow(c, res_sx, res_y, res_ex, res_y, res_color, line_width=1.5, head_len=5, head_width=2.8)
        
        disp_val = resultant_end - resultant_start
        c.setFont(FONT_BOLD, 7)
        c.setFillColor(res_color)
        c.drawCentredString((res_sx + res_ex) / 2, res_y - 9,
                            f"Resultant Delta x = {disp_val:+g} m (Start: {resultant_start}, End: {resultant_end})")
        
        c.restoreState()


class FreeBodyDiagramRenderer:
    """
    Renders rigid block mechanics with labeled vector forces originating from center of mass.
    """
    @staticmethod
    def draw_fbd(c, x, y, w, h, forces=None, title="FREE BODY FORCE DIAGRAM"):
        """
        forces: list of dicts: [{'name': 'Normal Force N', 'dir': 'UP', 'mag': 'mg', 'color': '#2563EB'}, ...]
        """
        c.saveState()
        draw_card_box(c, x, y, w, h, title=title, title_color=Palette.PHYSICS_DARK)
        
        if forces is None:
            forces = [
                {"name": "N", "dir": "UP", "mag": "49 N", "color": "#2563EB"},
                {"name": "W = mg", "dir": "DOWN", "mag": "49 N", "color": "#2563EB"},
                {"name": "F_applied", "dir": "RIGHT", "mag": "20 N", "color": "#059669"},
                {"name": "f_friction", "dir": "LEFT", "mag": "10 N", "color": "#DC2626"}
            ]
            
        cx = x + w / 2
        cy = y + h * 0.45
        bw, bh = 44, 32
        
        # Surface line
        c.setStrokeColor(Palette.TEXT_MUTED)
        c.setLineWidth(1.0)
        c.line(cx - 60, cy - bh / 2, cx + 60, cy - bh / 2)
        # Hatch marks
        for hx in range(int(cx - 55), int(cx + 60), 10):
            c.line(hx, cy - bh / 2, hx - 4, cy - bh / 2 - 4)
            
        # Block
        c.setFillColor(colors.HexColor("#F1F5F9"))
        c.setStrokeColor(Palette.TEXT_PRIMARY)
        c.setLineWidth(1.2)
        c.rect(cx - bw / 2, cy - bh / 2, bw, bh, fill=1, stroke=1)
        c.setFont(FONT_BOLD, 7.5)
        c.setFillColor(Palette.TEXT_PRIMARY)
        c.drawCentredString(cx, cy - 2.5, "m = 5 kg")
        
        # Center of mass dot
        c.circle(cx, cy, 2, fill=1, stroke=0)
        
        # Draw force vectors
        arrow_len = 34
        for f in forces:
            f_color = colors.HexColor(f["color"])
            direction = f["dir"].upper()
            
            if direction == "UP":
                draw_arrow(c, cx, cy + bh / 2, cx, cy + bh / 2 + arrow_len, f_color, line_width=1.5)
                c.setFont(FONT_BOLD, 7)
                c.setFillColor(f_color)
                c.drawCentredString(cx, cy + bh / 2 + arrow_len + 4, f"{f['name']} ({f['mag']})")
            elif direction == "DOWN":
                draw_arrow(c, cx, cy - bh / 2, cx, cy - bh / 2 - arrow_len, f_color, line_width=1.5)
                c.setFont(FONT_BOLD, 7)
                c.setFillColor(f_color)
                c.drawCentredString(cx, cy - bh / 2 - arrow_len - 10, f"{f['name']} ({f['mag']})")
            elif direction == "RIGHT":
                draw_arrow(c, cx + bw / 2, cy, cx + bw / 2 + arrow_len, cy, f_color, line_width=1.5)
                c.setFont(FONT_BOLD, 7)
                c.setFillColor(f_color)
                c.drawString(cx + bw / 2 + arrow_len + 3, cy - 2.5, f"{f['name']} = {f['mag']}")
            elif direction == "LEFT":
                draw_arrow(c, cx - bw / 2, cy, cx - bw / 2 - arrow_len, cy, f_color, line_width=1.5)
                c.setFont(FONT_BOLD, 7)
                c.setFillColor(f_color)
                c.drawRightString(cx - bw / 2 - arrow_len - 3, cy - 2.5, f"{f['name']} = {f['mag']}")
                
        c.restoreState()


class WaveformRenderer:
    """
    Renders transverse sinusoidal wave profiles and longitudinal compression/rarefaction bands.
    """
    @staticmethod
    def draw_transverse_wave(c, x, y, w, h, cycles=2.0, wavelength_label="lambda = 2.0 m",
                             amplitude_label="A = 0.5 m", title="TRANSVERSE WAVE: PROFILE & KINEMATICS"):
        c.saveState()
        draw_card_box(c, x, y, w, h, title=title, title_color=Palette.PHYSICS_DARK)
        
        mid_y = y + h * 0.46
        start_x = x + 35
        end_x = x + w - 30
        wave_len_px = end_x - start_x
        amp_px = 24
        
        # Equilibrium line
        c.setStrokeColor(Palette.BORDER_CARD)
        c.setLineWidth(0.8)
        c.setDash(3, 2)
        c.line(start_x, mid_y, end_x, mid_y)
        c.setDash()
        
        # Sine wave path
        c.setStrokeColor(Palette.PHYSICS_DARK)
        c.setLineWidth(1.6)
        
        num_points = 120
        p = c.beginPath()
        for i in range(num_points + 1):
            t = i / num_points
            curr_x = start_x + t * wave_len_px
            angle = t * cycles * 2 * math.pi
            curr_y = mid_y + amp_px * math.sin(angle)
            if i == 0:
                p.moveTo(curr_x, curr_y)
            else:
                p.lineTo(curr_x, curr_y)
        c.drawPath(p, fill=0, stroke=1)
        
        # Crest and Trough markers
        first_crest_x = start_x + (0.25 / cycles) * wave_len_px
        second_crest_x = start_x + (1.25 / cycles) * wave_len_px
        first_trough_x = start_x + (0.75 / cycles) * wave_len_px
        
        c.setFont(FONT_BOLD, 7)
        c.setFillColor(Palette.PHYSICS_DARK)
        c.drawCentredString(first_crest_x, mid_y + amp_px + 4, "Crest")
        c.drawCentredString(first_trough_x, mid_y - amp_px - 10, "Trough")
        
        # Wavelength dimension span between 1st and 2nd crest
        c.setStrokeColor(Palette.PHYSICS_BLUE)
        c.setLineWidth(1.0)
        span_y = mid_y + amp_px + 12
        c.line(first_crest_x, span_y, second_crest_x, span_y)
        draw_arrow(c, (first_crest_x + second_crest_x)/2, span_y, second_crest_x, span_y, Palette.PHYSICS_BLUE, line_width=1.0)
        draw_arrow(c, (first_crest_x + second_crest_x)/2, span_y, first_crest_x, span_y, Palette.PHYSICS_BLUE, line_width=1.0)
        c.setFont(FONT_BOLD, 6.8)
        c.setFillColor(Palette.PHYSICS_BLUE)
        c.drawCentredString((first_crest_x + second_crest_x) / 2, span_y + 3, wavelength_label)
        
        # Amplitude dimension span
        c.setStrokeColor(Palette.DANGER)
        amp_x = start_x + 15
        c.line(amp_x, mid_y, amp_x, mid_y + amp_px)
        draw_arrow(c, amp_x, mid_y, amp_x, mid_y + amp_px, Palette.DANGER, line_width=1.0)
        c.setFont(FONT_BOLD, 6.8)
        c.setFillColor(Palette.DANGER)
        c.drawRightString(amp_x - 3, mid_y + amp_px / 2 - 2, amplitude_label)
        
        c.restoreState()


class BohrAtomRenderer:
    """
    Renders Bohr atomic models: nucleus with p and n counts, and concentric K, L, M electron shells.
    """
    @staticmethod
    def draw_bohr_atom(c, x, y, w, h, symbol="Na", name="Sodium", protons=11, neutrons=12,
                       shells=(2, 8, 1), title="BOHR ATOMIC MODEL: SHELL STRUCTURE"):
        c.saveState()
        draw_card_box(c, x, y, w, h, title=title, title_color=Palette.CHEM_DARK)
        
        cx = x + w / 2
        cy = y + h * 0.46
        
        # Nucleus
        nuc_radius = 16
        c.setFillColor(colors.HexColor("#FEF3C7"))
        c.setStrokeColor(Palette.WARNING)
        c.setLineWidth(1.2)
        c.circle(cx, cy, nuc_radius, fill=1, stroke=1)
        
        c.setFont(FONT_BOLD, 7)
        c.setFillColor(Palette.TEXT_PRIMARY)
        c.drawCentredString(cx, cy + 2, f"{protons}p")
        c.setFont(FONT_NAME, 6.5)
        c.setFillColor(Palette.TEXT_MUTED)
        c.drawCentredString(cx, cy - 7, f"{neutrons}n")
        
        # Shells
        shell_names = ["K", "L", "M", "N"]
        shell_base_r = 28
        shell_gap = 14
        
        c.setStrokeColor(Palette.BORDER_CARD)
        c.setLineWidth(0.8)
        c.setDash(2, 2)
        
        for idx, num_e in enumerate(shells):
            r = shell_base_r + idx * shell_gap
            # Circular shell orbit
            c.circle(cx, cy, r, fill=0, stroke=1)
            
            # Shell label at top
            s_name = shell_names[idx] if idx < len(shell_names) else f"n={idx+1}"
            c.setFont(FONT_BOLD, 6)
            c.setFillColor(Palette.CHEM_MED)
            c.drawString(cx + 2, cy + r + 2, f"{s_name} ({num_e}e-)")
            
            # Electron dots
            for e_idx in range(num_e):
                e_ang = 2 * math.pi * e_idx / num_e
                ex = cx + r * math.cos(e_ang)
                ey = cy + r * math.sin(e_ang)
                c.setFillColor(Palette.CHEM_DARK)
                c.circle(ex, ey, 2.5, fill=1, stroke=0)
                
        c.setDash()
        
        # Atom descriptor badge
        config_str = ", ".join(str(s) for s in shells)
        badge = f"{name} ({symbol}): Z={protons}, A={protons+neutrons} | Config: [{config_str}]"
        draw_pill_badge(c, x + 25, y + 10, badge, colors.HexColor("#ECFDF5"), Palette.CHEM_DARK, font_size=7, height=14)
        
        c.restoreState()


class ParticleLatticeDiagram:
    """
    Renders Johnstone submicroscopic reaction chambers with color-coded Dalton spheres.
    """
    @staticmethod
    def draw_reaction_chamber(c, x, y, w, h, title="PARTICULATE DALTON REACTION MODEL: 2 H2 + O2 --> 2 H2O"):
        c.saveState()
        draw_card_box(c, x, y, w, h, title=title, title_color=Palette.CHEM_DARK)
        
        chamber_w = 95
        chamber_h = 58
        cy = y + 26
        
        c1_x = x + 16
        c2_x = x + w - 16 - chamber_w
        
        # Reactant Chamber
        c.setFillColor(colors.HexColor("#F8FAFC"))
        c.setStrokeColor(Palette.BORDER_CARD)
        c.roundRect(c1_x, cy, chamber_w, chamber_h, 4, fill=1, stroke=1)
        c.setFont(FONT_BOLD, 7)
        c.setFillColor(Palette.CHEM_DARK)
        c.drawString(c1_x + 6, cy + chamber_h - 11, "Reactants (4 H + 2 O)")
        
        # Draw 2 H2 molecules
        def draw_h2(cx, cy_pos):
            c.setFillColor(Palette.ELEMENT_H)
            c.circle(cx - 5, cy_pos, 4.5, fill=1, stroke=0)
            c.circle(cx + 5, cy_pos, 4.5, fill=1, stroke=0)
            c.setFont(FONT_BOLD, 5.5)
            c.setFillColor(colors.white)
            c.drawCentredString(cx - 5, cy_pos - 2, "H")
            c.drawCentredString(cx + 5, cy_pos - 2, "H")
            
        draw_h2(c1_x + 25, cy + 32)
        draw_h2(c1_x + 25, cy + 14)
        
        # Draw 1 O2 molecule
        c.setFillColor(Palette.ELEMENT_O)
        c.circle(c1_x + 68, cy + 24, 7, fill=1, stroke=0)
        c.circle(c1_x + 80, cy + 24, 7, fill=1, stroke=0)
        c.setFont(FONT_BOLD, 6.5)
        c.setFillColor(colors.white)
        c.drawCentredString(c1_x + 68, cy + 22, "O")
        c.drawCentredString(c1_x + 80, cy + 22, "O")
        
        # Reaction Arrow
        arr_sx = c1_x + chamber_w + 6
        arr_ex = c2_x - 6
        draw_arrow(c, arr_sx, cy + chamber_h / 2, arr_ex, cy + chamber_h / 2, Palette.CHEM_MED, line_width=1.8, head_len=6)
        c.setFont(FONT_BOLD, 6.8)
        c.setFillColor(Palette.CHEM_MED)
        c.drawCentredString((arr_sx + arr_ex) / 2, cy + chamber_h / 2 + 5, "Reaction")
        
        # Product Chamber (2 H2O molecules)
        c.setFillColor(colors.HexColor("#F8FAFC"))
        c.setStrokeColor(Palette.BORDER_CARD)
        c.roundRect(c2_x, cy, chamber_w, chamber_h, 4, fill=1, stroke=1)
        c.setFont(FONT_BOLD, 7)
        c.setFillColor(Palette.CHEM_DARK)
        c.drawString(c2_x + 6, cy + chamber_h - 11, "Products (2 H2O)")
        
        def draw_h2o(cx, cy_pos):
            # Oxygen center
            c.setFillColor(Palette.ELEMENT_O)
            c.circle(cx, cy_pos, 7.5, fill=1, stroke=0)
            c.setFont(FONT_BOLD, 6.5)
            c.setFillColor(colors.white)
            c.drawCentredString(cx, cy_pos - 2, "O")
            # Hydrogens attached at 104.5 deg
            c.setFillColor(Palette.ELEMENT_H)
            c.circle(cx - 7, cy_pos + 6, 4.5, fill=1, stroke=0)
            c.circle(cx + 7, cy_pos + 6, 4.5, fill=1, stroke=0)
            c.setFont(FONT_BOLD, 5.5)
            c.drawCentredString(cx - 7, cy_pos + 4, "H")
            c.drawCentredString(cx + 7, cy_pos + 4, "H")
            
        draw_h2o(c2_x + 30, cy + 22)
        draw_h2o(c2_x + 72, cy + 22)
        
        # Conservation note
        c.setFont(FONT_NAME, 6.5)
        c.setFillColor(Palette.TEXT_MUTED)
        c.drawCentredString(x + w / 2, y + 10, "Mass Conservation Invariant: 4 H atoms + 2 O atoms on both sides")
        
        c.restoreState()


class OxidationLaneDiagram:
    """
    Renders declarative before-and-after oxidation state progression.
    NO hardcoded fallback entities: inputs must be strictly specified.
    """
    @staticmethod
    def draw_lane(c, x, y, w, h, reactant_label, reactant_on,
                  product_label, product_on, delta_text, electron_text,
                  title="OXIDATION STATE LANE & ROLE ATTACHMENT"):
        c.saveState()
        draw_card_box(c, x, y, w, h, title=title, title_color=Palette.CHEM_DARK)
        
        box_w = 90
        box_h = 44
        bx1 = x + 20
        bx2 = x + w - 20 - box_w
        by = y + 20
        
        # Reactant Box
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
        c.setFillColor(Palette.TEXT_MUTED)
        c.drawCentredString(bx1 + box_w / 2, by + 3, "REACTANT")
        
        # Product Box
        c.setFillColor(colors.HexColor("#ECFDF5"))
        c.setStrokeColor(colors.HexColor("#A7F3D0"))
        c.roundRect(bx2, by, box_w, box_h, 4, fill=1, stroke=1)
        c.setFont(FONT_BOLD, 8.5)
        c.setFillColor(Palette.CHEM_DARK)
        c.drawCentredString(bx2 + box_w / 2, by + 26, product_label)
        c.setFont(FONT_BOLD, 8)
        c.setFillColor(Palette.CHEM_MED)
        c.drawCentredString(bx2 + box_w / 2, by + 12, f"ON = {product_on}")
        c.setFont(FONT_NAME, 6.5)
        c.setFillColor(Palette.TEXT_MUTED)
        c.drawCentredString(bx2 + box_w / 2, by + 3, "PRODUCT")
        
        # Progression Arrow
        arr_start = bx1 + box_w + 8
        arr_end = bx2 - 8
        draw_arrow(c, arr_start, by + box_h / 2, arr_end, by + box_h / 2, Palette.PHYSICS_DARK, line_width=1.8, head_len=6)
        
        c.setFont(FONT_BOLD, 7.5)
        c.setFillColor(Palette.TEXT_PRIMARY)
        c.drawCentredString((arr_start + arr_end) / 2, by + box_h / 2 + 7, delta_text)
        c.setFont(FONT_NAME, 6.8)
        c.setFillColor(Palette.DANGER)
        c.drawCentredString((arr_start + arr_end) / 2, by + box_h / 2 - 11, electron_text)
        
        c.restoreState()


class CombinatorialSlotDiagram:
    """
    Renders combinatorial decision boxes with choices and constraint badges.
    """
    @staticmethod
    def draw_slots(c, x, y, w, h, slots=None, title="COMBINATORIAL SLOT MODEL: MULTIPLICATION PRINCIPLE"):
        c.saveState()
        draw_card_box(c, x, y, w, h, title=title, title_color=Palette.MATH_DARK)
        
        if slots is None:
            slots = [
                {"label": "Thousands", "choices": "5 choices", "note": "Digits {1..5}"},
                {"label": "Hundreds", "choices": "4 choices", "note": "Remaining"},
                {"label": "Tens", "choices": "3 choices", "note": "Remaining"},
                {"label": "Units", "choices": "1 choice", "note": "Even constraint {0}"}
            ]
            
        n_slots = len(slots)
        slot_w = min(54, (w - 60) / (n_slots * 1.3))
        slot_h = 42
        gap = (w - 60 - n_slots * slot_w) / (n_slots - 1) if n_slots > 1 else 0
        sy = y + 26
        
        cur_x = x + 30
        for i, s in enumerate(slots):
            # Box
            c.setFillColor(colors.HexColor("#EFF6FF"))
            c.setStrokeColor(Palette.MATH_BORDER)
            c.roundRect(cur_x, sy, slot_w, slot_h, 4, fill=1, stroke=1)
            
            c.setFont(FONT_BOLD, 7.5)
            c.setFillColor(Palette.MATH_DARK)
            c.drawCentredString(cur_x + slot_w / 2, sy + slot_h - 12, s["label"])
            
            c.setFont(FONT_BOLD, 8)
            c.setFillColor(Palette.DANGER)
            c.drawCentredString(cur_x + slot_w / 2, sy + slot_h / 2 - 3, s["choices"])
            
            c.setFont(FONT_NAME, 6)
            c.setFillColor(Palette.TEXT_MUTED)
            c.drawCentredString(cur_x + slot_w / 2, sy + 4, s["note"])
            
            # Multiplication symbol between slots
            if i < n_slots - 1:
                cross_x = cur_x + slot_w + gap / 2
                c.setFont(FONT_BOLD, 11)
                c.setFillColor(Palette.TEXT_MUTED)
                c.drawCentredString(cross_x, sy + slot_h / 2 - 4, "*")
                
            cur_x += slot_w + gap
            
        c.setFont(FONT_NAME, 6.8)
        c.setFillColor(Palette.TEXT_SECONDARY)
        c.drawCentredString(x + w / 2, y + 10, "Total Combinations = 5 * 4 * 3 * 1 = 60 valid outcomes")
        
        c.restoreState()
