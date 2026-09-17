#!/usr/bin/env python3
"""Subject-wide 2D Physics teaching primitives.

The module owns no topic truth. Defaults are structural/schematic only and introduce no
numerical quantities. Rendering uses the same TracingCanvas instrumentation as the base
Physics primitive kit so vector realization is measurable rather than asserted.
"""
from __future__ import annotations

from reportlab.lib import colors
from physics_primitive_renderer import (
    FONT_BOLD, FONT_NAME, Palette, TracingCanvas, draw_arrow, draw_card_box,
)


class Unknown2DPrimitive(ValueError):
    pass


def _axes(c, x, y, w, h):
    ox, oy = x + w * 0.26, y + h * 0.27
    xr, yt = x + w - 24, y + h - 28
    c.setStrokeColor(Palette.TEXT_SECONDARY); c.setLineWidth(1.0)
    c.line(x + 20, oy, xr, oy); c.line(ox, y + 18, ox, yt)
    draw_arrow(c, xr - 7, oy, xr, oy, Palette.TEXT_SECONDARY, line_width=1.0)
    draw_arrow(c, ox, yt - 7, ox, yt, Palette.TEXT_SECONDARY, line_width=1.0)
    c.setFillColor(Palette.PHYSICS_DARK); c.circle(ox, oy, 2.5, fill=1, stroke=0)
    c.setFont(FONT_BOLD, 6.4); c.drawString(xr + 3, oy - 2, "x"); c.drawString(ox + 4, yt - 2, "y")
    c.setFont(FONT_NAME, 5.8); c.setFillColor(Palette.TEXT_MUTED); c.drawString(ox + 4, oy - 10, "origin")
    return ox, oy, xr, yt


def draw_cartesian_frame_2d(c, x, y, w, h, params):
    draw_card_box(c, x, y, w, h, title=params.get("title", "2D FRAME: ONE ORIGIN, TWO PERPENDICULAR AXES"), title_color=Palette.PHYSICS_DARK)
    ox, oy, xr, yt = _axes(c, x + 8, y + 10, w - 16, h - 20)
    c.setStrokeColor(Palette.BORDER_LIGHT); c.setLineWidth(0.5)
    for frac in (0.45, 0.65, 0.85):
        gx = ox + (xr - ox) * frac; c.line(gx, oy - 4, gx, oy + 4)
    for frac in (0.35, 0.60, 0.85):
        gy = oy + (yt - oy) * frac; c.line(ox - 4, gy, ox + 4, gy)
    c.setFont(FONT_NAME, 6.4); c.setFillColor(Palette.TEXT_SECONDARY)
    c.drawString(x + 24, y + 12, "Choose one origin and keep both axes attached to the same physical plane.")


def draw_vector_components_2d(c, x, y, w, h, params):
    draw_card_box(c, x, y, w, h, title=params.get("title", "ONE VECTOR, TWO PERPENDICULAR COMPONENTS"), title_color=Palette.PHYSICS_DARK)
    ox, oy, xr, yt = _axes(c, x + 6, y + 8, w - 12, h - 16)
    px, py = ox + (xr - ox) * 0.58, oy + (yt - oy) * 0.55
    draw_arrow(c, ox, oy, px, py, Palette.PHYSICS_DARK, line_width=1.8)
    draw_arrow(c, ox, oy, px, oy, Palette.PHYSICS_BLUE, line_width=1.3)
    draw_arrow(c, px, oy, px, py, Palette.PHYSICS_MED, line_width=1.3)
    c.setStrokeColor(Palette.BORDER_CARD); c.setLineWidth(0.7); c.setDash(2, 2)
    c.line(ox, py, px, py); c.line(px, oy, px, py); c.setDash()
    c.setFont(FONT_BOLD, 6.2); c.setFillColor(Palette.PHYSICS_DARK)
    c.drawString(px - 10, py + 6, params.get("resultant_label", "vector"))
    c.setFillColor(Palette.PHYSICS_BLUE); c.drawCentredString((ox + px) / 2, oy - 12, params.get("x_component_label", "x component"))
    c.setFillColor(Palette.PHYSICS_MED); c.drawString(px + 5, (oy + py) / 2, params.get("y_component_label", "y component"))


def draw_state_sequence_2d(c, x, y, w, h, params):
    draw_card_box(c, x, y, w, h, title=params.get("title", "2D STATE SEQUENCE: ONE BODY, ONE SHARED CLOCK"), title_color=Palette.PHYSICS_DARK)
    left, right, base, top = x + 34, x + w - 32, y + 42, y + h - 44
    p0 = (left, base); p1 = (left + (right-left)*0.5, top); p2 = (right, base + 5)
    c.setStrokeColor(Palette.PHYSICS_DARK); c.setLineWidth(1.2)
    c.bezier(p0[0], p0[1], left+(right-left)*0.22, top, left+(right-left)*0.32, top, p1[0], p1[1])
    c.bezier(p1[0], p1[1], left+(right-left)*0.68, top, left+(right-left)*0.82, base+(top-base)*0.45, p2[0], p2[1])
    states = [p0, p1, p2]; labels = params.get("state_labels") or ["t0", "event", "t2"]
    for i, (px, py) in enumerate(states):
        c.setFillColor(Palette.PHYSICS_BLUE if i != 1 else Palette.PHYSICS_MED); c.circle(px, py, 3.5, fill=1, stroke=0)
        draw_arrow(c, px, py, px + 28, py, Palette.PHYSICS_BLUE, line_width=1.0)
        vy = 0 if (params.get("middle_vertical_zero", True) and i == 1) else (18 if i == 0 else -18)
        if vy: draw_arrow(c, px, py, px, py + vy, Palette.PHYSICS_MED, line_width=1.0)
        draw_arrow(c, px + 12, py + 24, px + 12, py + 8, Palette.DANGER, line_width=0.9)
        c.setFont(FONT_NAME, 5.9); c.setFillColor(Palette.TEXT_MUTED); c.drawCentredString(px, py - 12, str(labels[i])[:18])
    clock_y = y + 22; c.setStrokeColor(Palette.TEXT_SECONDARY); c.setLineWidth(0.9); c.line(left, clock_y, right, clock_y)
    for px, _ in states: c.line(px, clock_y - 3, px, clock_y + 3)
    c.setFont(FONT_BOLD, 5.9); c.setFillColor(Palette.TEXT_SECONDARY); c.drawCentredString((left+right)/2, y + 10, "one shared clock")


def draw_path_anatomy_2d(c, x, y, w, h, params):
    draw_card_box(c, x, y, w, h, title=params.get("title", "2D PATH ANATOMY: EVENTS AND STATE VECTOR"), title_color=Palette.PHYSICS_DARK)
    left, right, base, apex_y = x + 42, x + w - 36, y + 38, y + h - 48; mid = (left + right) / 2
    c.setStrokeColor(Palette.BORDER_LIGHT); c.line(left - 12, base, right + 12, base); c.line(left, base - 8, left, apex_y + 8)
    c.setStrokeColor(Palette.PHYSICS_DARK); c.setLineWidth(1.2)
    c.bezier(left, base, left+40, apex_y, mid-35, apex_y, mid, apex_y); c.bezier(mid, apex_y, mid+35, apex_y, right-40, apex_y, right, base)
    for label, px, py in (("start", left, base), ("event", mid, apex_y), ("end", right, base)):
        c.setFillColor(Palette.PHYSICS_BLUE); c.circle(px, py, 3.5, fill=1, stroke=0)
        c.setFont(FONT_NAME, 5.9); c.setFillColor(Palette.TEXT_MUTED); c.drawCentredString(px, py - 12, label)
    draw_arrow(c, left, base, left+42, base+34, Palette.PHYSICS_DARK, line_width=1.5)
    draw_arrow(c, left, base, left+42, base, Palette.PHYSICS_BLUE, line_width=1.0)
    draw_arrow(c, left+42, base, left+42, base+34, Palette.PHYSICS_MED, line_width=1.0)
    c.setStrokeColor(Palette.BORDER_CARD); c.setDash(2, 2); c.line(left+42, base, left+42, base+34); c.setDash()
    c.setFont(FONT_NAME, 6.1); c.setFillColor(Palette.TEXT_SECONDARY)
    c.drawString(x + 22, y + 12, "Name path events first; attach each vector to the event where it belongs.")


def draw_event_compare_2d(c, x, y, w, h, params):
    draw_card_box(c, x, y, w, h, title=params.get("title", "2D EVENT COMPARE: SAME BOUNDARY, DIFFERENT PATH"), title_color=Palette.PHYSICS_DARK)
    left, right, base = x + 40, x + w - 40, y + 42
    c.setStrokeColor(Palette.BORDER_CARD); c.setLineWidth(0.9)
    c.line(left-12, base, right+12, base)
    # Explicit shared-boundary geometry: both endpoints and their common level are visible.
    c.setDash(2, 2); c.line(left, base-9, left, base+11); c.line(right, base-9, right, base+11); c.line(left, base-9, right, base-9); c.setDash()
    c.setStrokeColor(Palette.PHYSICS_DARK); c.setLineWidth(1.2)
    c.bezier(left, base, left+55, y+h-58, right-90, y+h-58, right, base)
    c.setStrokeColor(Palette.PHYSICS_MED); c.bezier(left, base, left+85, y+h-92, right-65, y+h-92, right, base)
    for px, label in ((left, "common start"), (right, "common event")):
        c.setFillColor(Palette.PHYSICS_BLUE); c.circle(px, base, 4, fill=1, stroke=0)
        c.setFont(FONT_NAME, 5.8); c.setFillColor(Palette.TEXT_MUTED); c.drawCentredString(px, base - 20, label)
    c.setFont(FONT_BOLD, 6.0); c.setFillColor(Palette.PHYSICS_DARK); c.drawString(left + 28, y+h-42, "case A")
    c.setFillColor(Palette.PHYSICS_MED); c.drawRightString(right - 28, y+h-70, "case B")
    c.setFont(FONT_NAME, 6.1); c.setFillColor(Palette.TEXT_SECONDARY)
    c.drawString(x + 22, y + 12, "Hold the boundary event fixed; compare the one feature that changes between cases.")


def draw_parametric_elimination_bridge_2d(c, x, y, w, h, params):
    draw_card_box(c, x, y, w, h, title=params.get("title", "PARAMETRIC BRIDGE: REMOVE THE SHARED PARAMETER"), title_color=Palette.PHYSICS_DARK)
    gap = 12; pw = (w - 52 - 2*gap) / 3; py = y + 36; ph = h - 70
    xs = [x + 20, x + 20 + pw + gap, x + 20 + 2*(pw+gap)]
    titles = params.get("stage_labels") or ["x(t) and y(t)", "isolate the shared t", "direct y(x) relation"]
    for i, px in enumerate(xs):
        c.setFillColor(colors.white); c.setStrokeColor(Palette.BORDER_CARD); c.setLineWidth(0.8); c.roundRect(px, py, pw, ph, 5, fill=1, stroke=1)
        c.setFont(FONT_BOLD, 6.1); c.setFillColor(Palette.PHYSICS_DARK); c.drawCentredString(px + pw/2, py + ph - 14, str(titles[i])[:30])
        c.setStrokeColor(Palette.BORDER_LIGHT); c.line(px+8, py+ph-20, px+pw-8, py+ph-20)
    draw_arrow(c, xs[0]+pw+2, py+ph/2, xs[1]-2, py+ph/2, Palette.PHYSICS_MED, line_width=1.1)
    draw_arrow(c, xs[1]+pw+2, py+ph/2, xs[2]-2, py+ph/2, Palette.PHYSICS_MED, line_width=1.1)
    ox, oy, xr, yt = xs[2] + 18, py + 20, xs[2] + pw - 12, py + ph - 28
    c.setStrokeColor(Palette.TEXT_MUTED); c.line(ox, oy, xr, oy); c.line(ox, oy, ox, yt)
    c.setStrokeColor(Palette.PHYSICS_DARK); c.bezier(ox, oy+4, ox+pw*0.2, yt, xr-pw*0.2, yt, xr, oy+4)
    c.setFont(FONT_NAME, 5.7); c.setFillColor(Palette.TEXT_MUTED)
    c.drawString(x + 22, y + 12, "Same parameter in both coordinates -> isolate -> substitute -> read the path relation.")


def draw_observer_line_of_sight_2d(c, x, y, w, h, params):
    draw_card_box(c, x, y, w, h, title=params.get("title", "OBSERVER VIEW: LINE OF SIGHT IN A PLANE"), title_color=Palette.PHYSICS_DARK)
    ground, observer_x, target_x, target_y = y + 36, x + 70, x + w - 70, y + h - 58
    c.setStrokeColor(Palette.TEXT_SECONDARY); c.setLineWidth(1.0); c.line(x + 24, ground, x + w - 24, ground)
    c.setFillColor(colors.white); c.setStrokeColor(Palette.PHYSICS_DARK); c.circle(observer_x, ground + 10, 7, fill=1, stroke=1)
    c.line(observer_x, ground + 3, observer_x, ground - 8); c.line(observer_x, ground - 3, observer_x-7, ground-12); c.line(observer_x, ground - 3, observer_x+7, ground-12)
    c.setFillColor(Palette.PHYSICS_BLUE); c.circle(target_x, target_y, 4, fill=1, stroke=0)
    c.setStrokeColor(Palette.PHYSICS_DARK); c.setLineWidth(1.3); c.line(observer_x, ground+10, target_x, target_y)
    c.setStrokeColor(Palette.BORDER_CARD); c.setLineWidth(0.8); c.setDash(2, 2)
    c.line(observer_x, ground+10, target_x, ground+10); c.line(target_x, ground+10, target_x, target_y); c.setDash()
    c.setStrokeColor(Palette.PHYSICS_MED); c.arc(observer_x-4, ground+6, observer_x+42, ground+52, startAng=0, extent=35)
    c.setFont(FONT_BOLD, 6.0); c.setFillColor(Palette.PHYSICS_DARK); c.drawString(observer_x-18, ground+23, "observer"); c.drawString(target_x+6, target_y-2, "target")
    c.setFont(FONT_NAME, 6.0); c.setFillColor(Palette.TEXT_SECONDARY)
    c.drawString(x + 22, y + 12, "The observed angle belongs to this observer's sight line, not directly to path range.")


RENDERERS_2D = {
    "CARTESIAN_FRAME_2D": draw_cartesian_frame_2d,
    "VECTOR_COMPONENTS_2D": draw_vector_components_2d,
    "STATE_SEQUENCE_2D": draw_state_sequence_2d,
    "PATH_ANATOMY_2D": draw_path_anatomy_2d,
    "EVENT_COMPARE_2D": draw_event_compare_2d,
    "PARAMETRIC_ELIMINATION_BRIDGE_2D": draw_parametric_elimination_bridge_2d,
    "OBSERVER_LINE_OF_SIGHT_2D": draw_observer_line_of_sight_2d,
}


def supported_kinds_2d():
    return sorted(RENDERERS_2D)


def render_primitive_2d(kind, params, canvas, bbox):
    if kind not in RENDERERS_2D:
        raise Unknown2DPrimitive("UNKNOWN_2D_TEACHING_PRIMITIVE: " + str(kind))
    x, y, w, h = bbox; tracer = TracingCanvas(canvas); tracer.saveState()
    try: RENDERERS_2D[kind](tracer, x, y, w, h, dict(params or {}))
    finally: tracer.restoreState()
    return {
        "primitive_id": kind,
        "bbox": {"x0": x, "y0": y, "x1": x+w, "y1": y+h},
        "ink_bbox": tracer.ink_bbox,
        "vector_ops": tracer.vector_ops,
        "text_ops": tracer.text_ops,
        "op_histogram": dict(sorted(tracer.op_histogram.items())),
        "realized": tracer.vector_ops > 0,
        "quantitative_grounding": "SCHEMATIC_STRUCTURE_ONLY",
    }
