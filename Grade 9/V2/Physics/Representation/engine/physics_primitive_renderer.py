#!/usr/bin/env python3
"""P-H Physics teaching-primitive renderer.

Stable interface:

    render_primitive(kind, params, canvas, bbox) -> RenderEvidence

Every primitive is realized as **actual vector graphics** (ReportLab
line / rect / roundRect / circle / arc / path operations). Text labels are
counted separately and can never satisfy a primitive on their own: the
returned evidence carries the real vector-operation count and the real ink
bounding box, measured by instrumenting the canvas while the primitive draws.

Where the vendored shared library at
``Grade 9/V2/Shared/MasterTemplates/primitives`` already provides a routine
(1D signed frame strip, v-t graph with Riemann area, free-body diagram) this
module delegates to it rather than reimplementing. Where it does not
(x-t graph, a-t graph, phase strip, state table, trajectory, timeline,
relative frame, option-graph set, slope/area decoder, diagram-equation bridge)
this module composes the figure from the same shared primitives layer
(``CartesianPlotter2D``, ``draw_card_box``, ``draw_arrow``, ``Palette``) so the
house style stays identical and the shared library can absorb these later.
"""
import math
from pathlib import Path
import sys

_SHARED = Path(__file__).resolve().parents[3] / "Shared" / "MasterTemplates"
if str(_SHARED) not in sys.path:
    sys.path.insert(0, str(_SHARED))

from reportlab.lib import colors  # noqa: E402
from primitives import (  # noqa: E402
    FONT_NAME, FONT_BOLD, Palette, draw_card_box, draw_arrow, draw_pill_badge,
    CartesianPlotter2D, KinematicGraphRenderer, Vector1DDiagram, FreeBodyDiagramRenderer,
    VisualSemanticValidator,
)

VECTOR_METHODS = (
    "line", "lines", "rect", "roundRect", "circle", "ellipse", "arc", "drawPath", "bezier", "grid",
)
TEXT_METHODS = ("drawString", "drawCentredString", "drawRightString", "drawAlignedString")


class UnknownPrimitive(ValueError):
    """Raised when a primitive kind has no renderer binding."""


class TracingCanvas:
    """Canvas proxy that counts real drawing operations and measures the ink box.

    This is what makes ``TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED`` machine
    detectable: vector operations and text operations are counted separately,
    against coordinates the primitive actually emitted, not against a plan.
    """

    def __init__(self, canvas):
        self._c = canvas
        self.vector_ops = 0
        self.text_ops = 0
        self.op_histogram = {}
        self.min_x = self.min_y = float("inf")
        self.max_x = self.max_y = float("-inf")

    # -- bookkeeping ---------------------------------------------------------
    def _note(self, name, vector):
        self.op_histogram[name] = self.op_histogram.get(name, 0) + 1
        if vector:
            self.vector_ops += 1
        else:
            self.text_ops += 1

    def _extend(self, xs, ys):
        for x in xs:
            self.min_x = min(self.min_x, x)
            self.max_x = max(self.max_x, x)
        for y in ys:
            self.min_y = min(self.min_y, y)
            self.max_y = max(self.max_y, y)

    @property
    def ink_bbox(self):
        if self.min_x == float("inf"):
            return None
        return {"x0": self.min_x, "y0": self.min_y, "x1": self.max_x, "y1": self.max_y}

    # -- counted vector operations -------------------------------------------
    def line(self, x1, y1, x2, y2):
        self._note("line", True)
        self._extend([x1, x2], [y1, y2])
        return self._c.line(x1, y1, x2, y2)

    def rect(self, x, y, w, h, **kw):
        self._note("rect", True)
        self._extend([x, x + w], [y, y + h])
        return self._c.rect(x, y, w, h, **kw)

    def roundRect(self, x, y, w, h, r, **kw):
        self._note("roundRect", True)
        self._extend([x, x + w], [y, y + h])
        return self._c.roundRect(x, y, w, h, r, **kw)

    def circle(self, x, y, r, **kw):
        self._note("circle", True)
        self._extend([x - r, x + r], [y - r, y + r])
        return self._c.circle(x, y, r, **kw)

    def ellipse(self, x1, y1, x2, y2, **kw):
        self._note("ellipse", True)
        self._extend([x1, x2], [y1, y2])
        return self._c.ellipse(x1, y1, x2, y2, **kw)

    def arc(self, x1, y1, x2, y2, *a, **kw):
        self._note("arc", True)
        self._extend([x1, x2], [y1, y2])
        return self._c.arc(x1, y1, x2, y2, *a, **kw)

    def drawPath(self, p, **kw):
        self._note("drawPath", True)
        return self._c.drawPath(p, **kw)

    def bezier(self, *a, **kw):
        self._note("bezier", True)
        self._extend([a[0], a[6]], [a[1], a[7]])
        return self._c.bezier(*a, **kw)

    def grid(self, xs, ys):
        self._note("grid", True)
        self._extend(list(xs), list(ys))
        return self._c.grid(xs, ys)

    # -- counted text operations ---------------------------------------------
    def drawString(self, x, y, text, *a, **kw):
        self._note("drawString", False)
        self._extend([x], [y])
        return self._c.drawString(x, y, text, *a, **kw)

    def drawCentredString(self, x, y, text, *a, **kw):
        self._note("drawCentredString", False)
        self._extend([x], [y])
        return self._c.drawCentredString(x, y, text, *a, **kw)

    def drawRightString(self, x, y, text, *a, **kw):
        self._note("drawRightString", False)
        self._extend([x], [y])
        return self._c.drawRightString(x, y, text, *a, **kw)

    def drawAlignedString(self, x, y, text, *a, **kw):
        self._note("drawAlignedString", False)
        self._extend([x], [y])
        return self._c.drawAlignedString(x, y, text, *a, **kw)

    def __getattr__(self, name):
        return getattr(self._c, name)


# ----------------------------------------------------------------- helpers


def _fmt(value, unit=""):
    if isinstance(value, float) and value == int(value):
        value = int(value)
    return f"{value}{(' ' + unit) if unit else ''}"


def _axis_label(params, key, default):
    return params.get(key) or default


def _positive_direction(params):
    return params.get("positive_direction") or "declared +"


def _rows(params, key, default):
    rows = params.get(key)
    return rows if rows else list(default)


def _title(params, default):
    return params.get("title") or default


# ------------------------------------------------------- primitive renderers


def draw_phenomenon_scene(c, x, y, w, h, params):
    draw_card_box(c, x, y, w, h, title=_title(params, "SITUATION: WHAT PHYSICALLY HAPPENS"),
                  title_color=Palette.PHYSICS_DARK)
    ground = y + 26
    c.setStrokeColor(Palette.TEXT_MUTED)
    c.setLineWidth(1.0)
    c.line(x + 24, ground, x + w - 24, ground)
    for hx in range(int(x + 28), int(x + w - 24), 14):
        c.line(hx, ground, hx - 5, ground - 5)

    start_x = x + 52
    end_x = x + w - 60
    body_y = ground + 26
    for label, bx in (("start", start_x), ("end", end_x)):
        c.setStrokeColor(Palette.PHYSICS_DARK)
        c.setLineWidth(1.0)
        c.line(bx, ground, bx, ground + 46)
        c.setFont(FONT_NAME, 6.5)
        c.setFillColor(Palette.TEXT_MUTED)
        c.drawCentredString(bx, ground - 12, label)
    c.setFillColor(colors.HexColor("#F1F5F9"))
    c.setStrokeColor(Palette.TEXT_PRIMARY)
    c.setLineWidth(1.2)
    c.rect(start_x - 12, body_y - 9, 24, 18, fill=1, stroke=1)
    c.setFont(FONT_BOLD, 6.8)
    c.setFillColor(Palette.TEXT_PRIMARY)
    c.drawCentredString(start_x, body_y - 2.5, params.get("body_label", "body"))

    draw_arrow(c, start_x + 18, body_y, end_x - 18, body_y, Palette.PHYSICS_DARK, line_width=1.5)
    c.setFont(FONT_NAME, 6.8)
    c.setFillColor(Palette.PHYSICS_DARK)
    c.drawCentredString((start_x + end_x) / 2, body_y + 7, params.get("event_text", "motion from start to end"))

    events = _rows(params, "events", ["Read what happens first.", "Read what changes.", "Read what is asked."])
    ey = y + h - 30
    for i, text in enumerate(events[:3], 1):
        c.setStrokeColor(Palette.BORDER_CARD)
        c.setLineWidth(0.6)
        c.circle(x + 30, ey - 3, 5.5, fill=0, stroke=1)
        c.setFont(FONT_BOLD, 6)
        c.setFillColor(Palette.PHYSICS_DARK)
        c.drawCentredString(x + 30, ey - 5, str(i))
        c.setFont(FONT_NAME, 6.8)
        c.setFillColor(Palette.TEXT_SECONDARY)
        c.drawString(x + 42, ey - 5, text[:92])
        ey -= 13


def draw_motion_strip(c, x, y, w, h, params):
    draw_card_box(c, x, y, w, h, title=_title(params, "MOTION STRIP: POSITIONS AT EQUAL TIME STEPS"),
                  title_color=Palette.PHYSICS_DARK)
    positions = params.get("positions") or [0.0, 1.0, 2.25, 4.0, 6.25]
    steps = params.get("time_step_label", "equal time steps")
    axis_y = y + 32
    left = x + 34
    right = x + w - 34
    span = right - left
    lo, hi = min(positions), max(positions)
    rng = (hi - lo) or 1.0

    c.setStrokeColor(Palette.TEXT_SECONDARY)
    c.setLineWidth(1.3)
    c.line(left, axis_y, right, axis_y)
    draw_arrow(c, right - 6, axis_y, right, axis_y, Palette.TEXT_SECONDARY, line_width=1.3)

    prev = None
    for i, p in enumerate(positions):
        px = left + (p - lo) / rng * span
        c.setFillColor(Palette.PHYSICS_DARK if i else Palette.PHYSICS_BLUE)
        c.circle(px, axis_y + 18, 4.0, fill=1, stroke=0)
        c.setStrokeColor(Palette.BORDER_CARD)
        c.setLineWidth(0.7)
        c.line(px, axis_y, px, axis_y + 14)
        c.setFont(FONT_NAME, 6.2)
        c.setFillColor(Palette.TEXT_MUTED)
        c.drawCentredString(px, axis_y - 11, f"t{i}")
        if prev is not None:
            c.setStrokeColor(Palette.TEXT_MUTED)
            c.setLineWidth(0.6)
            c.line(prev, axis_y + 30, px, axis_y + 30)
        prev = px
    c.setFont(FONT_NAME, 6.8)
    c.setFillColor(Palette.TEXT_SECONDARY)
    c.drawString(x + 24, y + h - 30, f"Gaps are {steps}; unequal gaps mean the speed is changing.")


def draw_vector_state_view(c, x, y, w, h, params):
    draw_card_box(c, x, y, w, h, title=_title(params, "VECTOR STATE VIEW: DIRECTED QUANTITIES"),
                  title_color=Palette.PHYSICS_DARK)
    vectors = params.get("vectors") or [
        {"name": "v", "value": 1.0, "unit": ""},
        {"name": "a", "value": -1.0, "unit": ""},
    ]
    base_x = x + 70
    top = y + h - 34
    # zero reference: the vertical body line plus a signed horizontal scale
    c.setStrokeColor(Palette.BORDER_CARD)
    c.setLineWidth(0.8)
    c.line(base_x, y + 22, base_x, top)
    c.setStrokeColor(Palette.BORDER_LIGHT)
    c.setLineWidth(0.5)
    c.setDash(2, 2)
    for off in (-78, -39, 39, 78):
        c.line(base_x + off, y + 22, base_x + off, top)
    c.setDash()
    c.setStrokeColor(Palette.TEXT_SECONDARY)
    c.setLineWidth(1.0)
    c.line(base_x - 84, y + 22, base_x + 84, y + 22)
    draw_arrow(c, base_x + 76, y + 22, base_x + 84, y + 22, Palette.TEXT_SECONDARY, line_width=1.0)
    c.setFont(FONT_NAME, 6.2)
    c.setFillColor(Palette.TEXT_MUTED)
    c.drawCentredString(base_x, y + 14, "body")

    row_y = top - 14
    longest = max((abs(float(v.get("value", 1)) or 1) for v in vectors), default=1.0)
    for v in vectors[:4]:
        val = float(v.get("value", 1) or 0)
        length = 26 + 52 * (abs(val) / (longest or 1))
        colour = Palette.PHYSICS_BLUE if val >= 0 else Palette.DANGER
        tip = base_x + length if val >= 0 else base_x - length
        draw_arrow(c, base_x, row_y, tip, row_y, colour, line_width=1.6)
        c.setFont(FONT_BOLD, 6.8)
        c.setFillColor(colour)
        text = f"{v.get('name', '?')} = {_fmt(val, v.get('unit', ''))}"
        if val >= 0:
            c.drawString(tip + 4, row_y - 2.5, text)
        else:
            c.drawRightString(tip - 4, row_y - 2.5, text)
        row_y -= 22
    c.setFont(FONT_NAME, 6.5)
    c.setFillColor(Palette.TEXT_SECONDARY)
    c.drawString(x + 20, y + 12, f"Positive direction: {_positive_direction(params)}. Arrow direction carries the sign.")


def draw_phase_boundary_view(c, x, y, w, h, params):
    draw_card_box(c, x, y, w, h, title=_title(params, "PHASE BOUNDARY VIEW: WHAT CARRIES ACROSS"),
                  title_color=Palette.PHYSICS_DARK)
    phases = params.get("phases") or ["P1", "P2"]
    carried = params.get("continuity_states") or []
    left = x + 28
    right = x + w - 28
    band_y = y + h * 0.42
    band_h = 26
    n = max(1, len(phases))
    seg = (right - left) / n
    # time axis beneath the phase band, so a phase is visibly an interval
    c.setStrokeColor(Palette.TEXT_SECONDARY)
    c.setLineWidth(1.1)
    c.line(left, band_y - 30, right, band_y - 30)
    draw_arrow(c, right - 6, band_y - 30, right, band_y - 30, Palette.TEXT_SECONDARY, line_width=1.1)
    for i in range(n + 1):
        tx = left + i * seg
        c.setStrokeColor(Palette.TEXT_MUTED)
        c.setLineWidth(0.8)
        c.line(tx, band_y - 33.5, tx, band_y - 26.5)
    for i, phase in enumerate(phases):
        px = left + i * seg
        c.setFillColor(Palette.PHYSICS_LIGHT if i % 2 == 0 else colors.HexColor("#E0F2FE"))
        c.setStrokeColor(Palette.PHYSICS_MED)
        c.setLineWidth(1.0)
        c.rect(px, band_y, seg, band_h, fill=1, stroke=1)
        c.setFont(FONT_BOLD, 7.2)
        c.setFillColor(Palette.PHYSICS_DARK)
        c.drawCentredString(px + seg / 2, band_y + band_h / 2 - 2.5, str(phase))
        if i:
            c.setStrokeColor(Palette.DANGER)
            c.setLineWidth(1.4)
            c.line(px, band_y - 14, px, band_y + band_h + 14)
            c.setFont(FONT_BOLD, 6.2)
            c.setFillColor(Palette.DANGER)
            c.drawCentredString(px, band_y + band_h + 18, "boundary")
            label = ", ".join(carried) if carried else "state carried across"
            draw_arrow(c, px - 26, band_y - 9, px + 26, band_y - 9, Palette.DANGER, line_width=1.2)
            c.setFont(FONT_NAME, 6.2)
            c.drawCentredString(px, band_y - 20, label[:56])
    c.setFont(FONT_NAME, 6.5)
    c.setFillColor(Palette.TEXT_SECONDARY)
    c.drawString(x + 20, y + 12, "The end state of one phase is the start state of the next; only the rate may jump.")


def draw_trajectory_view(c, x, y, w, h, params):
    draw_card_box(c, x, y, w, h, title=_title(params, "TRAJECTORY VIEW: PATH AGAINST DISPLACEMENT"),
                  title_color=Palette.PHYSICS_DARK)
    cx = x + w / 2
    cy = y + h * 0.36
    r = min(w * 0.22, h * 0.32)
    ax, bx = cx - r, cx + r

    c.setStrokeColor(Palette.PHYSICS_DARK)
    c.setLineWidth(1.6)
    c.arc(cx - r, cy - r, cx + r, cy + r, 0, 180)

    c.setStrokeColor(Palette.DANGER)
    c.setLineWidth(1.4)
    c.setDash(3, 2)
    c.line(ax, cy, bx, cy)
    c.setDash()
    draw_arrow(c, ax, cy, bx, cy, Palette.DANGER, line_width=1.4)

    for label, px in (("A", ax), ("B", bx)):
        c.setFillColor(Palette.TEXT_PRIMARY)
        c.circle(px, cy, 2.6, fill=1, stroke=0)
        c.setStrokeColor(Palette.BORDER_CARD)
        c.setLineWidth(0.6)
        c.line(px, cy - 4, px, cy - 10)
        c.setFont(FONT_BOLD, 7)
        c.drawCentredString(px, cy - 16, label)
    # measurement bracket under the chord makes path and chord separately measurable
    c.setStrokeColor(Palette.DANGER)
    c.setLineWidth(0.8)
    c.line(ax, cy - 22, bx, cy - 22)
    c.line(ax, cy - 25, ax, cy - 19)
    c.line(bx, cy - 25, bx, cy - 19)

    c.setFont(FONT_BOLD, 6.8)
    c.setFillColor(Palette.PHYSICS_DARK)
    c.drawCentredString(cx, cy + r + 6, params.get("path_label", "path travelled (distance)"))
    c.setFillColor(Palette.DANGER)
    c.drawCentredString(cx, cy + 5, params.get("chord_label", "straight A to B (displacement)"))
    c.setFont(FONT_NAME, 6.5)
    c.setFillColor(Palette.TEXT_SECONDARY)
    c.drawString(x + 20, y + 12, "Distance follows the drawn path; displacement follows the dashed chord.")


def _graph_frame(c, x, y, w, h, x_max, y_min, y_max, x_label, y_label):
    plotter = CartesianPlotter2D(
        c, x, y, w, h, x_domain=(0, max(x_max, 1.0)), y_domain=(min(y_min, 0), max(y_max, 1.0)),
        grid=True, pad_left=34, pad_bottom=24, pad_right=16, pad_top=26,
    )
    plotter.draw_axes(
        x_label=x_label, y_label=y_label,
        x_step=max(1, int(max(x_max, 1) / 5)), y_step=max(1, int((max(y_max, 1) - min(y_min, 0)) / 5)),
    )
    return plotter


def draw_position_time_graph(c, x, y, w, h, params):
    draw_card_box(c, x, y, w, h, title=_title(params, "POSITION-TIME GRAPH: SLOPE IS A VELOCITY"),
                  title_color=Palette.PHYSICS_DARK)
    pts = params.get("points") or [(0.0, 0.0), (4.0, 8.0)]
    t_max = max(p[0] for p in pts) * 1.25 or 5.0
    x_max_val = max(p[1] for p in pts) * 1.25 or 10.0
    plotter = _graph_frame(c, x, y, w, h, t_max, 0, x_max_val,
                           _axis_label(params, "x_axis_label", "t (s)"),
                           _axis_label(params, "y_axis_label", "x (m)"))
    for i in range(len(pts) - 1):
        plotter.plot_line_segment(*pts[i], *pts[i + 1], color=Palette.PHYSICS_DARK, width=1.8)
    plotter.plot_slope_triangle(*pts[0], *pts[-1])
    for p in pts:
        plotter.plot_point(p[0], p[1], color=Palette.PHYSICS_DARK, project_axes=False)
    dt = pts[-1][0] - pts[0][0]
    dx = pts[-1][1] - pts[0][1]
    if dt:
        draw_pill_badge(c, x + 22, y + 14, f"slope = dx/dt = {dx:g}/{dt:g} = {dx / dt:.2f} m/s",
                        colors.HexColor("#EFF6FF"), Palette.PHYSICS_DARK, font_size=6.8, height=13, padding_x=6)


def draw_velocity_time_graph(c, x, y, w, h, params):
    KinematicGraphRenderer.draw_vt_graph(
        c, x, y, w, h,
        title=_title(params, "VELOCITY-TIME GRAPH: SLOPE AND SIGNED AREA"),
        u=float(params.get("u", 0.0)),
        v=float(params.get("v", 10.0)),
        t_accel=float(params.get("t_accel", 5.0)),
        v_unit=params.get("v_unit", "m/s"),
        t_unit=params.get("t_unit", "s"),
    )


def draw_acceleration_time_graph(c, x, y, w, h, params):
    draw_card_box(c, x, y, w, h, title=_title(params, "ACCELERATION-TIME GRAPH: SIGNED LEVEL PER INTERVAL"),
                  title_color=Palette.PHYSICS_DARK)
    intervals = params.get("intervals") or [{"t0": 0.0, "t1": 4.0, "a": 2.0}]
    t_max = max(i["t1"] for i in intervals) * 1.2 or 5.0
    lo = min([i["a"] for i in intervals] + [0.0])
    hi = max([i["a"] for i in intervals] + [0.0])
    plotter = _graph_frame(c, x, y, w, h, t_max, lo * 1.4 if lo < 0 else -1.0, (hi or 1.0) * 1.4,
                           _axis_label(params, "x_axis_label", "t (s)"),
                           _axis_label(params, "y_axis_label", "a (m/s^2)"))
    for seg in intervals:
        cx0, cy0 = plotter.to_canvas(seg["t0"], 0)
        cx1, cy1 = plotter.to_canvas(seg["t1"], seg["a"])
        c.setFillColor(colors.HexColor("#CCFBF1") if seg["a"] >= 0 else colors.HexColor("#FEE2E2"))
        c.setStrokeColor(Palette.PHYSICS_MED if seg["a"] >= 0 else Palette.DANGER)
        c.setLineWidth(1.0)
        c.rect(cx0, min(cy0, cy1), cx1 - cx0, abs(cy1 - cy0), fill=1, stroke=1)
        c.setFont(FONT_BOLD, 6.5)
        c.setFillColor(Palette.PHYSICS_DARK if seg["a"] >= 0 else Palette.DANGER)
        c.drawCentredString((cx0 + cx1) / 2, cy1 + (4 if seg["a"] >= 0 else -9), f"a = {seg['a']:+g}")
    c.setFont(FONT_NAME, 6.5)
    c.setFillColor(Palette.TEXT_SECONDARY)
    c.drawString(x + 22, y + 12, "Signed area under a-t is the change in velocity on that interval.")


def draw_force_diagram(c, x, y, w, h, params):
    FreeBodyDiagramRenderer.draw_fbd(
        c, x, y, w, h,
        forces=params.get("forces"),
        title=_title(params, "FREE BODY DIAGRAM: FORCES ON ONE BODY"),
    )


def draw_sign_frame_overlay(c, x, y, w, h, params):
    """Signed frame strip.

    With source-stated journey legs this delegates to the shared
    ``Vector1DDiagram``. Without them it draws its own schematic frame instead:
    the shared routine substitutes a hard-coded ``+5 m East / -3 m West``
    journey when ``legs`` is omitted, and displaying that on a Physics item that
    never stated it would be exactly the invented-quantity defect this phase
    exists to prevent. (Recorded as gap 2 in the vendored package's
    ``VENDORED.md``; fixed here in the adapter, not in the vendored file.)
    """
    ticks = tuple(params.get("ticks") or (-3, -2, -1, 0, 1, 2, 3, 4, 5))
    legs = params.get("legs")
    title = _title(params, "SIGN AND FRAME STRIP: ORIGIN AND POSITIVE DIRECTION")
    if legs:
        Vector1DDiagram.draw(
            c, x, y, w, h, title=title,
            origin_val=params.get("origin", 0), ticks=ticks, legs=legs,
            resultant_start=params.get("resultant_start", 0),
            resultant_end=params.get("resultant_end", 0),
        )
        c.setFont(FONT_NAME, 6.4)
        c.setFillColor(Palette.TEXT_SECONDARY)
        c.drawString(x + 20, y + 12, f"Declared positive direction: {_positive_direction(params)}.")
        return

    draw_card_box(c, x, y, w, h, title=title, title_color=Palette.PHYSICS_DARK)
    axis_y = y + h * 0.50
    left = x + 40
    right = x + w - 54
    span = right - left
    c.setStrokeColor(Palette.TEXT_SECONDARY)
    c.setLineWidth(1.5)
    c.line(left, axis_y, right, axis_y)
    draw_arrow(c, right - 8, axis_y, right, axis_y, Palette.TEXT_SECONDARY, line_width=1.5)
    c.setFont(FONT_BOLD, 7)
    c.setFillColor(Palette.TEXT_PRIMARY)
    c.drawString(right + 4, axis_y - 2.5, "+ direction")

    origin = params.get("origin", 0)
    step = span / max(1, len(ticks) - 1)
    for i, val in enumerate(ticks):
        tx = left + i * step
        is_origin = val == origin
        c.setStrokeColor(Palette.PHYSICS_DARK if is_origin else Palette.TEXT_MUTED)
        c.setLineWidth(1.8 if is_origin else 1.0)
        c.line(tx, axis_y - 5, tx, axis_y + 5)
        c.setFont(FONT_NAME, 6.4)
        c.setFillColor(Palette.PHYSICS_DARK if is_origin else Palette.TEXT_MUTED)
        c.drawCentredString(tx, axis_y - 15, str(val))
    ox = left + list(ticks).index(origin) * step if origin in ticks else left
    c.setStrokeColor(Palette.PHYSICS_DARK)
    c.setLineWidth(1.0)
    c.circle(ox, axis_y, 4.0, fill=0, stroke=1)
    c.setFont(FONT_BOLD, 6.4)
    c.setFillColor(Palette.PHYSICS_DARK)
    c.drawCentredString(ox, axis_y + 12, "origin")

    # workspace band: the learner writes the signed givens against this frame
    c.setStrokeColor(Palette.BORDER_CARD)
    c.setLineWidth(0.7)
    c.setDash(2, 2)
    c.line(left, y + 22, right, y + 22)
    c.setDash()
    c.setFont(FONT_NAME, 6.4)
    c.setFillColor(Palette.TEXT_SECONDARY)
    declared = _positive_direction(params)
    c.drawString(x + 24, y + 12,
                 f"Declared positive direction: {declared}. Re-sign every given quantity against it here.")


def draw_diagram_equation_bridge(c, x, y, w, h, params):
    draw_card_box(c, x, y, w, h, title=_title(params, "DIAGRAM-EQUATION BRIDGE: WHAT EACH SYMBOL NAMES"),
                  title_color=Palette.PHYSICS_DARK)
    bindings = params.get("symbol_bindings") or [
        {"symbol": "u", "feature": "arrow at the start instant"},
        {"symbol": "v", "feature": "arrow at the end instant"},
        {"symbol": "t", "feature": "span between the two instants"},
    ]
    panel_w = (w - 56) / 2
    panel_h = h - 56
    lx = x + 20
    rx = lx + panel_w + 16
    py = y + 26

    c.setFillColor(colors.HexColor("#FFFFFF"))
    c.setStrokeColor(Palette.BORDER_CARD)
    c.setLineWidth(0.9)
    c.rect(lx, py, panel_w, panel_h, fill=1, stroke=1)
    c.rect(rx, py, panel_w, panel_h, fill=1, stroke=1)
    c.setFont(FONT_BOLD, 6.8)
    c.setFillColor(Palette.PHYSICS_DARK)
    c.drawString(lx + 8, py + panel_h - 12, "DIAGRAM FEATURE")
    c.drawString(rx + 8, py + panel_h - 12, "SYMBOL IN THE RELATION")

    # feature side: a small signed axis so the mapping points at real geometry
    ay = py + panel_h * 0.42
    c.setStrokeColor(Palette.TEXT_SECONDARY)
    c.setLineWidth(1.2)
    c.line(lx + 14, ay, lx + panel_w - 14, ay)
    draw_arrow(c, lx + panel_w - 22, ay, lx + panel_w - 14, ay, Palette.TEXT_SECONDARY, line_width=1.2)
    # panel separator and header rules, so the two sides read as one bridge
    c.setStrokeColor(Palette.BORDER_CARD)
    c.setLineWidth(0.7)
    c.line(lx + 8, py + panel_h - 18, lx + panel_w - 8, py + panel_h - 18)
    c.line(rx + 8, py + panel_h - 18, rx + panel_w - 8, py + panel_h - 18)
    c.setDash(2, 2)
    c.line(lx + panel_w + 8, py + 6, lx + panel_w + 8, py + panel_h - 6)
    c.setDash()

    row_y = py + panel_h - 28
    for i, b in enumerate(bindings[:4]):
        mark_x = lx + 22 + i * ((panel_w - 44) / max(1, min(4, len(bindings)) - 1 or 1))
        c.setFillColor(Palette.PHYSICS_BLUE)
        c.circle(mark_x, ay, 3.0, fill=1, stroke=0)
        c.setFont(FONT_NAME, 6.0)
        c.setFillColor(Palette.TEXT_MUTED)
        c.drawCentredString(mark_x, ay - 11, str(b.get("symbol", "?")))

        c.setFont(FONT_BOLD, 7)
        c.setFillColor(Palette.PHYSICS_DARK)
        c.drawString(rx + 10, row_y, str(b.get("symbol", "?")))
        c.setFont(FONT_NAME, 6.4)
        c.setFillColor(Palette.TEXT_SECONDARY)
        c.drawString(rx + 26, row_y, str(b.get("feature", ""))[:56])
        draw_arrow(c, mark_x, ay + 5, rx + 6, row_y + 2, Palette.BORDER_CARD, line_width=0.8, head_len=4, head_width=2)
        row_y -= 14

    relation = params.get("relation_text")
    if relation:
        draw_pill_badge(c, x + 20, y + 14, relation, colors.HexColor("#EFF6FF"),
                        Palette.PHYSICS_DARK, font_size=6.8, height=13, padding_x=6)


def draw_state_table(c, x, y, w, h, params):
    draw_card_box(c, x, y, w, h, title=_title(params, "STATE TABLE: START STATE AND END STATE"),
                  title_color=Palette.PHYSICS_DARK)
    columns = params.get("columns") or ["quantity", "start", "end"]
    rows = params.get("rows") or [
        ["position", "?", "?"], ["velocity", "?", "?"], ["time", "?", "?"],
    ]
    unknown = params.get("unknown")

    left = x + 22
    right = x + w - 22
    top = y + h - 30
    row_h = 14
    n_rows = min(len(rows), max(1, int((top - (y + 24)) / row_h) - 1))
    col_w = (right - left) / len(columns)

    c.setFillColor(colors.HexColor("#EFF6FF"))
    c.setStrokeColor(Palette.BORDER_CARD)
    c.setLineWidth(0.8)
    c.rect(left, top - row_h, right - left, row_h, fill=1, stroke=1)
    c.setFont(FONT_BOLD, 6.6)
    c.setFillColor(Palette.PHYSICS_DARK)
    for i, col in enumerate(columns):
        c.drawString(left + i * col_w + 5, top - row_h + 4.5, str(col))

    ty = top - row_h
    for r in rows[:n_rows]:
        ty -= row_h
        c.setStrokeColor(Palette.BORDER_LIGHT)
        c.setLineWidth(0.6)
        c.rect(left, ty, right - left, row_h, fill=0, stroke=1)
        c.setFont(FONT_NAME, 6.4)
        c.setFillColor(Palette.TEXT_PRIMARY)
        for i, cell in enumerate(list(r)[: len(columns)]):
            text = str(cell)
            if unknown and text == unknown:
                c.setFillColor(Palette.DANGER)
                c.setFont(FONT_BOLD, 6.4)
            c.drawString(left + i * col_w + 5, ty + 4.5, text[:26])
            c.setFillColor(Palette.TEXT_PRIMARY)
            c.setFont(FONT_NAME, 6.4)
    for i in range(1, len(columns)):
        c.setStrokeColor(Palette.BORDER_CARD)
        c.setLineWidth(0.6)
        c.line(left + i * col_w, ty, left + i * col_w, top)
    # outer frame plus a rule separating the header from the body
    c.setStrokeColor(Palette.PHYSICS_MED)
    c.setLineWidth(0.9)
    c.rect(left, ty, right - left, top - ty, fill=0, stroke=1)
    c.line(left, top - row_h, right, top - row_h)
    c.setFont(FONT_NAME, 6.3)
    c.setFillColor(Palette.TEXT_SECONDARY)
    c.drawString(left, y + 12, "Fill both instants first; the empty cell is what the question asks for.")


def draw_slope_area_decoder(c, x, y, w, h, params):
    draw_card_box(c, x, y, w, h, title=_title(params, "SLOPE OR AREA? DECODING ONE CURVE TWO WAYS"),
                  title_color=Palette.PHYSICS_DARK)
    pts = params.get("points") or [(0.0, 0.0), (5.0, 10.0)]
    half_w = (w - 44) / 2
    inner_h = h - 44
    t_max = max(p[0] for p in pts) * 1.2 or 5.0
    v_max = max(p[1] for p in pts) * 1.25 or 10.0

    left_plot = _graph_frame(c, x + 14, y + 20, half_w, inner_h, t_max, 0, v_max,
                             _axis_label(params, "x_axis_label", "t (s)"),
                             _axis_label(params, "y_axis_label", "v (m/s)"))
    for i in range(len(pts) - 1):
        left_plot.plot_line_segment(*pts[i], *pts[i + 1], color=Palette.PHYSICS_DARK, width=1.6)
    left_plot.plot_slope_triangle(*pts[0], *pts[-1])
    c.setFont(FONT_BOLD, 6.5)
    c.setFillColor(Palette.DANGER)
    c.drawString(x + 20, y + h - 28, "READ AS SLOPE = a rate")

    right_plot = _graph_frame(c, x + 30 + half_w, y + 20, half_w, inner_h, t_max, 0, v_max,
                              _axis_label(params, "x_axis_label", "t (s)"),
                              _axis_label(params, "y_axis_label", "v (m/s)"))
    p = c.beginPath()
    cx0, cy0 = right_plot.to_canvas(pts[0][0], 0)
    p.moveTo(cx0, cy0)
    for pt in pts:
        cxp, cyp = right_plot.to_canvas(*pt)
        p.lineTo(cxp, cyp)
    cxl, cyl = right_plot.to_canvas(pts[-1][0], 0)
    p.lineTo(cxl, cyl)
    p.close()
    c.setFillColor(colors.HexColor("#CCFBF1"))
    c.setStrokeColor(Palette.PHYSICS_MED)
    c.setLineWidth(0.9)
    c.drawPath(p, fill=1, stroke=1)
    for i in range(len(pts) - 1):
        right_plot.plot_line_segment(*pts[i], *pts[i + 1], color=Palette.PHYSICS_DARK, width=1.6)
    c.setFont(FONT_BOLD, 6.5)
    c.setFillColor(Palette.PHYSICS_DARK)
    c.drawString(x + 36 + half_w, y + h - 28, "READ AS SIGNED AREA = a change")


def draw_timeline_interval_view(c, x, y, w, h, params):
    draw_card_box(c, x, y, w, h, title=_title(params, "INTERVAL VIEW: A NAMED INTERVAL IS A DIFFERENCE"),
                  title_color=Palette.PHYSICS_DARK)
    t0 = float(params.get("t0", 4.0))
    t1 = float(params.get("t1", 5.0))
    t_end = float(params.get("t_end", max(t1 * 1.6, t1 + 1)))
    axis_y = y + h * 0.44
    left = x + 34
    right = x + w - 34
    span = right - left

    c.setStrokeColor(Palette.TEXT_SECONDARY)
    c.setLineWidth(1.3)
    c.line(left, axis_y, right, axis_y)
    draw_arrow(c, right - 6, axis_y, right, axis_y, Palette.TEXT_SECONDARY, line_width=1.3)

    steps = max(1, int(t_end))
    for i in range(steps + 1):
        tx = left + (i / t_end) * span
        c.setStrokeColor(Palette.TEXT_MUTED)
        c.setLineWidth(0.8)
        c.line(tx, axis_y - 3.5, tx, axis_y + 3.5)
        c.setFont(FONT_NAME, 6.0)
        c.setFillColor(Palette.TEXT_MUTED)
        c.drawCentredString(tx, axis_y - 12, str(i))

    x0 = left + (t0 / t_end) * span
    x1 = left + (t1 / t_end) * span
    c.setFillColor(colors.HexColor("#FEF3C7"))
    c.setStrokeColor(Palette.WARNING)
    c.setLineWidth(1.0)
    c.rect(x0, axis_y + 6, x1 - x0, 16, fill=1, stroke=1)
    draw_arrow(c, x0, axis_y + 32, x1, axis_y + 32, Palette.WARNING, line_width=1.2)
    draw_arrow(c, x1, axis_y + 32, x0, axis_y + 32, Palette.WARNING, line_width=1.2)
    c.setFont(FONT_BOLD, 6.6)
    c.setFillColor(Palette.WARNING)
    c.drawCentredString((x0 + x1) / 2, axis_y + 36, params.get("interval_label", f"{t0:g} s to {t1:g} s"))
    c.setFont(FONT_NAME, 6.4)
    c.setFillColor(Palette.TEXT_SECONDARY)
    c.drawString(x + 22, y + 12, "Compute the quantity at each bounding instant, then subtract.")


def draw_relative_frame_view(c, x, y, w, h, params):
    draw_card_box(c, x, y, w, h, title=_title(params, "RELATIVE FRAME VIEW: MEASURED FROM WHICH BODY?"),
                  title_color=Palette.PHYSICS_DARK)
    bodies = params.get("bodies") or [
        {"name": "A", "value": -10.0, "unit": "m/s^2"},
        {"name": "B", "value": -10.0, "unit": "m/s^2"},
    ]
    frame_body = params.get("frame_body", bodies[0]["name"] if bodies else "A")
    left = x + 44
    gap = (w - 120) / max(1, len(bodies) - 1 or 1)
    cy = y + h * 0.52

    for i, b in enumerate(bodies[:3]):
        bx = left + i * gap
        c.setFillColor(colors.HexColor("#F1F5F9"))
        c.setStrokeColor(Palette.TEXT_PRIMARY)
        c.setLineWidth(1.1)
        c.circle(bx, cy, 11, fill=1, stroke=1)
        c.setFont(FONT_BOLD, 7)
        c.setFillColor(Palette.TEXT_PRIMARY)
        c.drawCentredString(bx, cy - 2.5, str(b.get("name", "?")))
        val = float(b.get("value", 0) or 0)
        tip_y = cy - 14 - 22 * (1 if val < 0 else 0) if val < 0 else cy + 14 + 22
        draw_arrow(c, bx, cy + (14 if val >= 0 else -14), bx, tip_y,
                   Palette.PHYSICS_BLUE if val >= 0 else Palette.DANGER, line_width=1.5)
        c.setFont(FONT_NAME, 6.3)
        c.setFillColor(Palette.TEXT_SECONDARY)
        c.drawCentredString(bx, tip_y + (4 if val >= 0 else -9), f"{_fmt(val, b.get('unit', ''))}")
        if b.get("name") == frame_body:
            c.setStrokeColor(Palette.PHYSICS_DARK)
            c.setLineWidth(1.0)
            c.setDash(2, 2)
            c.circle(bx, cy, 17, fill=0, stroke=1)
            c.setDash()
            c.setFont(FONT_BOLD, 5.8)
            c.setFillColor(Palette.PHYSICS_DARK)
            c.drawCentredString(bx, cy - 26, "frame body")

    if len(bodies) >= 2:
        a = float(bodies[0].get("value", 0) or 0)
        b2 = float(bodies[1].get("value", 0) or 0)
        rel = b2 - a
        # difference bracket between the two bodies
        bx0, bx1 = left, left + gap
        c.setStrokeColor(Palette.PHYSICS_DARK)
        c.setLineWidth(0.9)
        c.line(bx0, cy - 40, bx1, cy - 40)
        c.line(bx0, cy - 43, bx0, cy - 37)
        c.line(bx1, cy - 43, bx1, cy - 37)
        draw_pill_badge(c, x + 22, y + 14,
                        f"relative value of {bodies[1].get('name')} from {bodies[0].get('name')} = {rel:+g}",
                        colors.HexColor("#EFF6FF"), Palette.PHYSICS_DARK, font_size=6.8, height=13, padding_x=6)


def draw_option_graph_set_view(c, x, y, w, h, params):
    draw_card_box(c, x, y, w, h, title=_title(params, "CANDIDATE GRAPHS ON IDENTICAL AXES"),
                  title_color=Palette.PHYSICS_DARK)
    options = params.get("options") or [
        {"label": "A", "points": [(0, 0), (4, 8)]},
        {"label": "B", "points": [(0, 8), (4, 8)]},
        {"label": "C", "points": [(0, 0), (2, 2), (4, 8)]},
    ]
    n = min(len(options), 4)
    cell_w = (w - 28 - (n - 1) * 8) / n
    cell_h = h - 50
    for i, opt in enumerate(options[:n]):
        ox = x + 14 + i * (cell_w + 8)
        oy = y + 26
        c.setStrokeColor(Palette.BORDER_CARD)
        c.setLineWidth(0.8)
        c.rect(ox, oy, cell_w, cell_h, fill=0, stroke=1)
        pts = opt.get("points") or [(0, 0), (4, 8)]
        t_max = max(p[0] for p in pts) or 4
        v_max = max(p[1] for p in pts) or 8
        px0, py0 = ox + 12, oy + 12
        pw, ph = cell_w - 20, cell_h - 24
        c.setStrokeColor(Palette.TEXT_SECONDARY)
        c.setLineWidth(1.0)
        c.line(px0, py0, px0 + pw, py0)
        c.line(px0, py0, px0, py0 + ph)
        for k in (0.25, 0.5, 0.75):
            c.setStrokeColor(Palette.BORDER_LIGHT)
            c.setLineWidth(0.5)
            c.line(px0 + k * pw, py0 - 2.5, px0 + k * pw, py0 + 2.5)
        c.setStrokeColor(Palette.PHYSICS_DARK)
        c.setLineWidth(1.5)
        for j in range(len(pts) - 1):
            ax = px0 + pts[j][0] / t_max * pw
            ay = py0 + pts[j][1] / (v_max or 1) * ph
            bx = px0 + pts[j + 1][0] / t_max * pw
            by = py0 + pts[j + 1][1] / (v_max or 1) * ph
            c.line(ax, ay, bx, by)
        c.setFont(FONT_BOLD, 6.8)
        c.setFillColor(Palette.PHYSICS_DARK)
        c.drawCentredString(ox + cell_w / 2, oy + cell_h + 4, str(opt.get("label", "?")))
    c.setFont(FONT_NAME, 6.3)
    c.setFillColor(Palette.TEXT_SECONDARY)
    c.drawString(x + 16, y + 12, params.get("decisive_feature", "Reject each option by naming the feature it gets wrong."))


def draw_minimal_physics_contrast(c, x, y, w, h, params):
    draw_card_box(c, x, y, w, h, title=_title(params, "MINIMAL CONTRAST: ONE DECISIVE FEATURE"),
                  title_color=Palette.PHYSICS_DARK)
    cases = params.get("cases") or [
        {"label": "shortcut works here", "note": ""},
        {"label": "shortcut fails here", "note": ""},
    ]
    panel_w = (w - 52) / 2
    panel_h = h - 54
    for i, case in enumerate(cases[:2]):
        px = x + 20 + i * (panel_w + 12)
        py = y + 26
        c.setFillColor(colors.HexColor("#F8FAFC") if i == 0 else colors.HexColor("#FEF2F2"))
        c.setStrokeColor(Palette.BORDER_CARD if i == 0 else Palette.DANGER)
        c.setLineWidth(1.0)
        c.rect(px, py, panel_w, panel_h, fill=1, stroke=1)
        c.setFont(FONT_BOLD, 6.8)
        c.setFillColor(Palette.TEXT_PRIMARY if i == 0 else Palette.DANGER)
        c.drawString(px + 8, py + panel_h - 12, f"CASE {chr(65 + i)}")
        c.setFont(FONT_NAME, 6.3)
        c.setFillColor(Palette.TEXT_SECONDARY)
        words = str(case.get("label", ""))
        for j in range(0, min(len(words), 160), 44):
            c.drawString(px + 8, py + panel_h - 26 - (j // 44) * 10, words[j:j + 44])
        mid = py + panel_h * 0.35
        c.setStrokeColor(Palette.TEXT_SECONDARY)
        c.setLineWidth(1.1)
        c.line(px + 12, mid, px + panel_w - 12, mid)
        draw_arrow(c, px + 12, mid, px + panel_w - 12, mid,
                   Palette.PHYSICS_DARK if i == 0 else Palette.DANGER, line_width=1.1)
        # marker showing where the decisive feature sits in each case
        c.setFillColor(Palette.PHYSICS_DARK if i == 0 else Palette.DANGER)
        c.circle(px + panel_w * (0.45 if i == 0 else 0.72), mid, 3.2, fill=1, stroke=0)
        c.setStrokeColor(Palette.BORDER_CARD)
        c.setLineWidth(0.6)
        c.line(px + panel_w * (0.45 if i == 0 else 0.72), mid - 6,
               px + panel_w * (0.45 if i == 0 else 0.72), py + 10)
    c.setFont(FONT_BOLD, 6.4)
    c.setFillColor(Palette.DANGER)
    c.drawString(x + 20, y + 12, "Decisive feature: " + str(params.get("decisive_feature", "exactly one feature differs"))[:88])


def draw_verification_check_strip(c, x, y, w, h, params):
    draw_card_box(c, x, y, w, h, title=_title(params, "PHYSICAL CHECK: MUST BE ABLE TO FAIL"),
                  title_color=Palette.PHYSICS_DARK)
    checks = params.get("checks") or ["VERIFY_DIMENSIONS"]
    # the result panel the checks are run against, so a check has something to reject
    c.setFillColor(colors.HexColor("#FFFFFF"))
    c.setStrokeColor(Palette.BORDER_CARD)
    c.setLineWidth(0.9)
    c.rect(x + 20, y + h - 40, w - 40, 16, fill=1, stroke=1)
    c.setFont(FONT_BOLD, 6.4)
    c.setFillColor(Palette.PHYSICS_DARK)
    c.drawString(x + 26, y + h - 35, "result under test")
    c.setStrokeColor(Palette.PHYSICS_MED)
    c.setLineWidth(1.0)
    c.line(x + 20, y + h - 46, x + w - 20, y + h - 46)
    cy = y + h - 58
    for check in checks[:5]:
        c.setStrokeColor(Palette.PHYSICS_DARK)
        c.setLineWidth(0.9)
        c.rect(x + 22, cy - 6, 9, 9, fill=0, stroke=1)
        draw_arrow(c, x + 34, cy - 1.5, x + 36, cy - 1.5, Palette.BORDER_CARD,
                   line_width=0.7, head_len=3, head_width=2)
        c.setFont(FONT_NAME, 6.6)
        c.setFillColor(Palette.TEXT_SECONDARY)
        c.drawString(x + 40, cy - 4, str(check).replace("_", " ").lower()[:88])
        cy -= 14
    c.setFont(FONT_NAME, 6.2)
    c.setFillColor(Palette.TEXT_MUTED)
    c.drawString(x + 22, y + 12, "Tick only after the check has actually been carried out on the result.")


def draw_model_validity_gate(c, x, y, w, h, params):
    draw_card_box(c, x, y, w, h, title=_title(params, "MODEL VALIDITY GATE: CHECK BEFORE USING"),
                  title_color=Palette.PHYSICS_DARK)
    conditions = params.get("conditions") or ["assumption stated by the situation"]
    model = params.get("model_label", "selected model")
    gy = y + h - 32
    c.setFillColor(colors.HexColor("#EFF6FF"))
    c.setStrokeColor(Palette.PHYSICS_MED)
    c.setLineWidth(1.0)
    c.rect(x + 20, gy - 4, w - 40, 14, fill=1, stroke=1)
    c.setFont(FONT_BOLD, 6.6)
    c.setFillColor(Palette.PHYSICS_DARK)
    c.drawString(x + 26, gy + 0.5, f"model: {model}"[:86])
    gy -= 20
    for cond in conditions[:5]:
        c.setStrokeColor(Palette.BORDER_CARD)
        c.setLineWidth(0.8)
        c.rect(x + 26, gy - 5, 8, 8, fill=0, stroke=1)
        c.setLineWidth(0.5)
        c.line(x + 40, gy - 7.5, x + w - 96, gy - 7.5)
        c.setFont(FONT_NAME, 6.4)
        c.setFillColor(Palette.TEXT_SECONDARY)
        c.drawString(x + 40, gy - 3.5, str(cond).replace("_", " ").lower()[:76])
        c.setFont(FONT_NAME, 5.8)
        c.setFillColor(Palette.TEXT_MUTED)
        c.drawRightString(x + w - 26, gy - 3.5, "stated / implied / absent")
        gy -= 13
    # gate bracket: the relation below the line is unreachable until every box is ticked
    c.setStrokeColor(Palette.DANGER)
    c.setLineWidth(1.2)
    c.line(x + 20, y + 22, x + w - 20, y + 22)
    c.line(x + 20, y + 22, x + 20, y + 30)
    c.line(x + w - 20, y + 22, x + w - 20, y + 30)
    c.setFont(FONT_BOLD, 6.3)
    c.setFillColor(Palette.DANGER)
    c.drawString(x + 22, y + 12, "If any condition is absent the relation below this line may not be used.")


RENDERERS = {
    "PHENOMENON_SCENE": draw_phenomenon_scene,
    "MOTION_STRIP": draw_motion_strip,
    "VECTOR_STATE_VIEW": draw_vector_state_view,
    "PHASE_BOUNDARY_VIEW": draw_phase_boundary_view,
    "TRAJECTORY_VIEW": draw_trajectory_view,
    "POSITION_TIME_GRAPH": draw_position_time_graph,
    "VELOCITY_TIME_GRAPH": draw_velocity_time_graph,
    "ACCELERATION_TIME_GRAPH": draw_acceleration_time_graph,
    "FORCE_DIAGRAM": draw_force_diagram,
    "SIGN_FRAME_OVERLAY": draw_sign_frame_overlay,
    "DIAGRAM_EQUATION_BRIDGE": draw_diagram_equation_bridge,
    "STATE_TABLE": draw_state_table,
    "SLOPE_AREA_DECODER": draw_slope_area_decoder,
    "TIMELINE_INTERVAL_VIEW": draw_timeline_interval_view,
    "RELATIVE_FRAME_VIEW": draw_relative_frame_view,
    "OPTION_GRAPH_SET_VIEW": draw_option_graph_set_view,
    "MINIMAL_PHYSICS_CONTRAST": draw_minimal_physics_contrast,
    "VERIFICATION_CHECK_STRIP": draw_verification_check_strip,
    "MODEL_VALIDITY_GATE": draw_model_validity_gate,
}


def supported_kinds():
    return sorted(RENDERERS)


def pre_render_validate(kind, item_data, params):
    """Run the shared fail-closed semantic gates that apply to this kind.

    The shared ``VisualSemanticValidator.validate`` dispatcher matches on
    substrings of the primitive name, which would misroute Physics ids that
    happen to contain ``ATOM`` or ``CIRCLE``, so the specific gates are called
    directly instead.
    """
    if kind in {"VELOCITY_TIME_GRAPH", "SLOPE_AREA_DECODER"}:
        spec = {
            "u": params.get("u", 0.0),
            "v": params.get("v", params.get("u", 0.0) or 1.0),
            "t_accel": params.get("t_accel", 1.0),
        }
        VisualSemanticValidator.validate_kinematic_graph(item_data or {}, spec)
    if kind == "SIGN_FRAME_OVERLAY" and params.get("legs"):
        VisualSemanticValidator.validate_vector_1d(
            item_data or {},
            {
                "legs": params["legs"],
                "resultant_start": params.get("resultant_start", 0),
                "resultant_end": params.get("resultant_end", 0),
            },
        )
    return True


def render_primitive(kind, params, canvas, bbox, item_data=None):
    """Render one teaching primitive and return measured render evidence.

    ``bbox`` is ``(x, y, w, h)`` in PDF points. The returned evidence records
    the real vector/text operation counts and the real ink bounding box, so a
    caller can prove the primitive was realized rather than merely labelled.
    """
    if kind not in RENDERERS:
        raise UnknownPrimitive(f"UNKNOWN_TEACHING_PRIMITIVE: {kind}")
    params = dict(params or {})
    pre_render_validate(kind, item_data, params)
    x, y, w, h = bbox
    tracer = TracingCanvas(canvas)
    tracer.saveState()
    try:
        RENDERERS[kind](tracer, x, y, w, h, params)
    finally:
        tracer.restoreState()
    return {
        "primitive_id": kind,
        "bbox": {"x0": x, "y0": y, "x1": x + w, "y1": y + h},
        "ink_bbox": tracer.ink_bbox,
        "vector_ops": tracer.vector_ops,
        "text_ops": tracer.text_ops,
        "op_histogram": dict(sorted(tracer.op_histogram.items())),
        "realized": tracer.vector_ops > 0,
    }
