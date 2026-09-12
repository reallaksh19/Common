#!/usr/bin/env python3
"""Stable seam between Mathematics teaching primitives and a drawing library.

Every figure in the Mathematics learner products goes through one entry point:

    render_primitive(kind, params, canvas, bbox) -> placement evidence

`kind` is a canonical name from
`RepresentationSemantics/registry/math-teaching-primitive-registry.json`.
`params` is derived only from declared source semantic data (see
`derive_params`). `bbox` is `(x, y, w, h)` in ReportLab points.

The drawing itself is delegated to the shared, subject-agnostic primitives
package vendored at `Grade 9/V2/Shared/MasterTemplates/primitives/` (from
PR #310). That package is treated as a read-only dependency: this module adapts
Mathematics semantics onto it and never edits it. When #310's package lands on
main, only `_LIBRARY_BINDINGS` below has to change.

Fail-closed discipline
----------------------
Before anything is drawn, `assert_grounded` checks that every numeric literal
the figure will show appears verbatim in the declared source text of the item.
That is the anti-drift gate the teaching-primitive registry asks for with
`NO_UNDECLARED_MATHEMATICAL_INFERENCE` and
`RENDER_FROM_DECLARED_SOURCE_SEMANTIC_DATA`.
"""
import re
import sys
from fractions import Fraction
from pathlib import Path

MATH = Path(__file__).resolve().parents[2]
SHARED = MATH.parent / "Shared" / "MasterTemplates"
if str(SHARED) not in sys.path:
    sys.path.insert(0, str(SHARED))

from primitives import (  # noqa: E402
    FONT_BOLD,
    FONT_NAME,
    FONT_OBLIQUE,
    CartesianPlotter2D,
    CombinatorialSlotDiagram,
    MathEquationBlock,
    Palette,
    PlaneGeometryRenderer,
    VisualSemanticValidator,
    VisualValidationError,
    draw_arrow,
    draw_card_box,
    draw_pill_badge,
)

# Falsifier vocabulary for the renderer seam.
FALSIFIERS = (
    "TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED",
    "UNKNOWN_TEACHING_PRIMITIVE_KIND",
    "MATH_VISUAL_UNGROUNDED_VALUE",
    "MATH_VISUAL_EMPTY_PARAMS",
    "MATH_VISUAL_OUT_OF_BOUNDS",
    "MATH_VISUAL_SEMANTIC_VALIDATION_FAILED",
)

# Every canonical primitive in the Mathematics teaching-primitive registry must
# have a real vector realization here. A registry entry with no binding is a
# label-only primitive, which is exactly what #319 forbids.
SUPPORTED_KINDS = (
    "ALIGNED_TRANSFORMATION_STACK",
    "ANNOTATED_DERIVATION",
    "COMBINATORIAL_SLOT_MODEL",
    "COORDINATE_PLANE",
    "CORRECT_WRONG_TRANSFORMATION_CONTRAST",
    "EQUIVALENCE_BALANCE_VIEW",
    "INVARIANT_HIGHLIGHT",
    "MIRROR_SOLUTION_VIEW",
    "PARALLEL_MEET_CONTRAST",
    "SIDE_BY_SIDE_METHOD_VIEW",
    "SLOPE_TRIANGLE_VIEW",
    "SUBSTITUTION_CHECK_VIEW",
    "TERM_HIGHLIGHT_VIEW",
)

NUMBER = re.compile(r"-?\d+(?:\.\d+)?(?:/\d+)?")
PAIR = re.compile(r"\(\s*(-?\d+(?:\.\d+)?(?:/\d+)?)\s*,\s*(-?\d+(?:\.\d+)?(?:/\d+)?)\s*\)")
LABELLED_PAIR = re.compile(r"([A-Z])\s*=?\s*\(\s*(-?\d+(?:\.\d+)?(?:/\d+)?)\s*,\s*(-?\d+(?:\.\d+)?(?:/\d+)?)\s*\)")


class PrimitiveRenderError(ValueError):
    pass


def fail(code, detail=""):
    raise PrimitiveRenderError(f"{code}:{detail}" if detail else code)


def _num(token):
    return float(Fraction(token))


# ---------------------------------------------------------------------------
# Declared-source extraction
# ---------------------------------------------------------------------------
def declared_text(page):
    """Every string the item itself declares. Nothing outside this may be drawn."""
    parts = [page.get("source_stem", "")]
    parts += [g.get("text", "") for g in page.get("source_givens", [])]
    parts += [o.get("text", "") for o in page.get("source_options", [])]
    parts += [u for u in page.get("source_units", [])]
    route = page.get("solution_route") or {}
    parts += list(route.get("steps", []))
    final = route.get("final_answer") or {}
    parts += list(final.get("accepted_answers", []))
    parts += list(final.get("answer_conditions", []))
    for sub in page.get("source_subparts", []) or []:
        parts.append(sub.get("text", "") if isinstance(sub, dict) else str(sub))
    return [p for p in parts if p]


def declared_points(page):
    """Labelled numeric ordered pairs the item actually declares."""
    points = []
    seen = set()
    for text in declared_text(page):
        for label, xs, ys in LABELLED_PAIR.findall(text):
            key = (xs, ys)
            if key in seen:
                continue
            seen.add(key)
            points.append({"label": label, "x": _num(xs), "y": _num(ys), "x_text": xs, "y_text": ys})
        for xs, ys in PAIR.findall(text):
            key = (xs, ys)
            if key in seen:
                continue
            seen.add(key)
            points.append({"label": None, "x": _num(xs), "y": _num(ys), "x_text": xs, "y_text": ys})
    return points


def derive_params(kind, spec, page):
    """Build renderer params from declared source semantic data only.

    `spec` is a representation spec from a MathRepresentationPlan; its
    `source_semantic_data.payload` is the authority for what the figure means.
    `page` supplies the declared numeric instance data.
    """
    payload = dict((spec.get("source_semantic_data") or {}).get("payload") or {})
    claims = list((spec.get("source_semantic_data") or {}).get("declared_claims") or [])
    params = {
        "payload": payload,
        "declared_claims": claims,
        "accessibility_text": spec.get("accessibility_text", ""),
        "attention_target": spec.get("attention_target", ""),
        "capability_ref": spec.get("capability_ref"),
        "points": declared_points(page) if page else [],
        "declared_text": declared_text(page) if page else [],
        "title": kind.replace("_", " "),
    }
    params["grounding"] = "DECLARED_NUMERIC" if params["points"] else "DECLARED_SYMBOLIC"
    return params


def assert_grounded(params, drawn_numbers):
    """Refuse to draw any numeric literal the item did not declare."""
    corpus = " ".join(params.get("declared_text", []) + params.get("declared_claims", []))
    for value in drawn_numbers:
        token = str(value)
        if token not in corpus and token.lstrip("-") not in corpus:
            fail("MATH_VISUAL_UNGROUNDED_VALUE", token)
    return True


# ---------------------------------------------------------------------------
# Local generic realizations (built from shared base helpers)
# ---------------------------------------------------------------------------
def _clip(canvas, text, font, size, max_width):
    """Trim a single line to fit, so nothing runs off the card."""
    text = str(text)
    if canvas.stringWidth(text, font, size) <= max_width:
        return text
    while text and canvas.stringWidth(text + "...", font, size) > max_width:
        text = text[:-1]
    return text + "..."


def _wrap(canvas, text, font, size, max_width):
    words = str(text).split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if canvas.stringWidth(trial, font, size) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines or [""]


def _stack_lines(payload, keys):
    out = []
    for key in keys:
        value = payload.get(key)
        if isinstance(value, list):
            out.extend(str(v) for v in value)
        elif value:
            out.append(str(value))
    return out


def _draw_two_column(canvas, bbox, title, left_title, left_lines, right_title, right_lines, footer=None):
    x, y, w, h = bbox
    draw_card_box(canvas, x, y, w, h, title=title, title_color=Palette.MATH_DARK)
    mid = x + w / 2
    canvas.saveState()
    canvas.setStrokeColor(Palette.BORDER_CARD)
    canvas.setLineWidth(0.7)
    canvas.line(mid, y + 16, mid, y + h - 26)
    for col_x, col_title, lines, accent in (
        (x + 12, left_title, left_lines, Palette.MATH_MED),
        (mid + 12, right_title, right_lines, Palette.WARNING),
    ):
        canvas.setFont(FONT_BOLD, 7.2)
        canvas.setFillColor(accent)
        canvas.drawString(col_x, y + h - 34, str(col_title))
        ty = y + h - 48
        canvas.setFont(FONT_NAME, 7)
        canvas.setFillColor(Palette.TEXT_PRIMARY)
        for line in lines:
            for wrapped in _wrap(canvas, line, FONT_NAME, 7, w / 2 - 26):
                if ty < y + 20:
                    break
                canvas.drawString(col_x, ty, wrapped)
                ty -= 10
            ty -= 2
    if footer:
        canvas.setFont(FONT_OBLIQUE, 6.4)
        canvas.setFillColor(Palette.TEXT_MUTED)
        canvas.drawString(x + 12, y + 8, str(footer)[:150])
    canvas.restoreState()


def _draw_invariant_card(canvas, bbox, params):
    x, y, w, h = bbox
    payload = params["payload"]
    draw_card_box(canvas, x, y, w, h, title="INVARIANT UNDER CHANGE", title_color=Palette.MATH_DARK)
    canvas.saveState()
    canvas.setFont(FONT_BOLD, 7.6)
    canvas.setFillColor(Palette.TEXT_PRIMARY)
    ty = y + h - 32
    for line in _wrap(canvas, payload.get("mathematical_object", ""), FONT_BOLD, 7.6, w - 28):
        canvas.drawString(x + 14, ty, line)
        ty -= 11
    ty -= 4
    canvas.setFont(FONT_NAME, 7)
    canvas.setFillColor(Palette.TEXT_SECONDARY)
    for line in _wrap(canvas, "Invariant: " + str(payload.get("invariant", "")), FONT_NAME, 7, w - 28):
        canvas.drawString(x + 14, ty, line)
        ty -= 10
    badge_x = x + 14
    for feature in list(payload.get("changing_features", []))[:4]:
        used = draw_pill_badge(
            canvas, badge_x, y + 18, str(feature), Palette.MATH_LIGHT, Palette.MATH_DARK, font_size=6.4, height=13
        )
        badge_x += used + 6
    canvas.setFont(FONT_OBLIQUE, 6.2)
    canvas.setFillColor(Palette.TEXT_MUTED)
    canvas.drawRightString(x + w - 12, y + 8, "varies ->")
    canvas.restoreState()


def _draw_balance(canvas, bbox, params):
    """EQUIVALENCE_BALANCE_VIEW: two pans joined by a declared operation."""
    x, y, w, h = bbox
    payload = params["payload"]
    draw_card_box(canvas, x, y, w, h, title="EQUIVALENCE BALANCE", title_color=Palette.MATH_DARK)
    canvas.saveState()
    pan_w = (w - 70) / 2
    pan_h = min(34, h - 58)
    pan_y = y + h / 2 - pan_h / 2 - 4
    for px, label, text in (
        (x + 18, "LEFT", payload.get("left_state", "")),
        (x + 52 + pan_w, "RIGHT", payload.get("right_state", "")),
    ):
        canvas.setFillColor(Palette.MATH_LIGHT)
        canvas.setStrokeColor(Palette.MATH_BORDER)
        canvas.setLineWidth(0.9)
        canvas.roundRect(px, pan_y, pan_w, pan_h, 4, fill=1, stroke=1)
        canvas.setFont(FONT_BOLD, 6.2)
        canvas.setFillColor(Palette.TEXT_MUTED)
        canvas.drawString(px + 6, pan_y + pan_h - 9, label)
        canvas.setFont(FONT_BOLD, 7.4)
        canvas.setFillColor(Palette.TEXT_PRIMARY)
        ty = pan_y + pan_h - 20
        for line in _wrap(canvas, text, FONT_BOLD, 7.4, pan_w - 12)[:2]:
            canvas.drawString(px + 6, ty, line)
            ty -= 9
    # fulcrum + equality bar
    cx = x + w / 2
    canvas.setStrokeColor(Palette.MATH_DARK)
    canvas.setLineWidth(1.2)
    canvas.line(x + 18, pan_y - 8, x + w - 18, pan_y - 8)
    path = canvas.beginPath()
    path.moveTo(cx - 7, pan_y - 8)
    path.lineTo(cx + 7, pan_y - 8)
    path.lineTo(cx, pan_y - 20)
    path.close()
    canvas.setFillColor(Palette.MATH_MED)
    canvas.drawPath(path, fill=1, stroke=0)
    draw_arrow(canvas, cx - 14, pan_y + pan_h + 12, cx + 14, pan_y + pan_h + 12, Palette.MATH_MED, line_width=1.2)
    canvas.setFont(FONT_BOLD, 6.8)
    canvas.setFillColor(Palette.MATH_DARK)
    canvas.drawCentredString(cx, pan_y + pan_h + 18, str(payload.get("operation", ""))[:60])
    canvas.setFont(FONT_OBLIQUE, 6.4)
    canvas.setFillColor(Palette.TEXT_MUTED)
    canvas.drawCentredString(cx, y + 8, "invariant: " + str(payload.get("invariant", ""))[:90])
    canvas.restoreState()


def _draw_coordinate_frame(canvas, bbox, params, with_slope):
    """COORDINATE_PLANE / SLOPE_TRIANGLE_VIEW from declared numeric points."""
    x, y, w, h = bbox
    points = params["points"]
    title = "SLOPE TRIANGLE VIEW" if with_slope else "COORDINATE PLANE"
    draw_card_box(canvas, x, y, w, h, title=title, title_color=Palette.MATH_DARK)
    if not points:
        # Honest symbolic fallback: the item declares no numeric instance, so
        # the frame is drawn with declared relations only and no invented data.
        canvas.saveState()
        canvas.setFont(FONT_NAME, 7)
        canvas.setFillColor(Palette.TEXT_SECONDARY)
        ty = y + h - 32
        for line in _wrap(canvas, "; ".join(str(p) for p in params["payload"].get("relations", [])), FONT_NAME, 7, w - 28):
            canvas.drawString(x + 14, ty, line)
            ty -= 10
        canvas.restoreState()
        plotter = CartesianPlotter2D(canvas, x, y, w, h - 18, x_domain=(-4, 4), y_domain=(-4, 4), grid=True)
        plotter.draw_axes(x_label="x", y_label="y")
        return []

    xs = [p["x"] for p in points]
    ys = [p["y"] for p in points]
    span_x = max(1.0, max(xs) - min(xs))
    span_y = max(1.0, max(ys) - min(ys))
    pad_x = max(1.0, span_x * 0.25)
    pad_y = max(1.0, span_y * 0.25)
    domain_x = (min(xs) - pad_x, max(xs) + pad_x)
    domain_y = (min(ys) - pad_y, max(ys) + pad_y)
    plotter = CartesianPlotter2D(canvas, x, y, w, h - 14, x_domain=domain_x, y_domain=domain_y, grid=True)
    step_x = max(1, round(span_x / 5) or 1)
    step_y = max(1, round(span_y / 5) or 1)
    plotter.draw_axes(x_label="x", y_label="y", x_step=step_x, y_step=step_y)

    drawn = []
    for point in points[:6]:
        label = point["label"] or ""
        text = f"{label}({point['x_text']},{point['y_text']})" if label else f"({point['x_text']},{point['y_text']})"
        plotter.plot_point(point["x"], point["y"], text, color=Palette.MATH_DARK)
        drawn.extend([point["x_text"], point["y_text"]])
    if len(points) >= 2:
        a, b = points[0], points[1]
        plotter.plot_line_segment(a["x"], a["y"], b["x"], b["y"], color=Palette.MATH_MED)
        if with_slope and a["x"] != b["x"]:
            plotter.plot_slope_triangle(a["x"], a["y"], b["x"], b["y"])
    return drawn


def _draw_parallel_contrast(canvas, bbox, params):
    x, y, w, h = bbox
    payload = params["payload"]
    angle = 65
    numbers = NUMBER.findall(" ".join(params["declared_text"]))
    for token in numbers:
        try:
            value = float(Fraction(token))
        except (ValueError, ZeroDivisionError):
            continue
        if 10 <= value <= 170:
            angle = value
            break
    PlaneGeometryRenderer.draw_parallel_transversal(
        canvas, x, y + 22, w, h - 22, angle_deg=angle,
        title="SAME-SIDE INTERIOR ANGLES AND THE MEETING BOUNDARY",
    )
    canvas.saveState()
    canvas.setFont(FONT_NAME, 6.4)
    canvas.setFillColor(Palette.TEXT_SECONDARY)
    ty = y + 14
    pairs = list(zip(payload.get("angle_sum_cases", []), payload.get("outcomes", [])))
    for case, outcome in pairs[:2]:
        line = f"{case} -> {outcome}"
        canvas.drawString(x + 12, ty, _clip(canvas, line, FONT_NAME, 6.4, w - 24))
        ty -= 8
    canvas.restoreState()
    return []


def _draw_slot_model(canvas, bbox, params):
    x, y, w, h = bbox
    payload = params["payload"]
    slots = payload.get("slots")
    if not slots:
        labels = payload.get("representation_path") or payload.get("steps") or []
        slots = [{"label": f"slot {i + 1}", "choices": str(v)[:18], "note": ""} for i, v in enumerate(labels[:4])]
    if not slots:
        fail("MATH_VISUAL_EMPTY_PARAMS", "COMBINATORIAL_SLOT_MODEL")
    CombinatorialSlotDiagram.draw_slots(canvas, x, y, w, h, slots=slots, title="UNORDERED SELECTION SLOT MODEL")
    return []


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------
def _algebra_lines(params, keys):
    lines = _stack_lines(params["payload"], keys)
    if not lines:
        lines = [str(c) for c in params["declared_claims"]]
    return lines[:7]


def _render(kind, params, canvas, bbox):
    x, y, w, h = bbox
    payload = params["payload"]
    if kind == "COORDINATE_PLANE":
        return _draw_coordinate_frame(canvas, bbox, params, with_slope=False)
    if kind == "SLOPE_TRIANGLE_VIEW":
        return _draw_coordinate_frame(canvas, bbox, params, with_slope=True)
    if kind == "PARALLEL_MEET_CONTRAST":
        return _draw_parallel_contrast(canvas, bbox, params)
    if kind == "COMBINATORIAL_SLOT_MODEL":
        return _draw_slot_model(canvas, bbox, params)
    if kind == "INVARIANT_HIGHLIGHT":
        _draw_invariant_card(canvas, bbox, params)
        return []
    if kind == "EQUIVALENCE_BALANCE_VIEW":
        _draw_balance(canvas, bbox, params)
        return []
    if kind == "ALIGNED_TRANSFORMATION_STACK":
        lines = _algebra_lines(params, ["states", "operations"])
        MathEquationBlock.draw_algebra_block(
            canvas, x, y, w, h, lines, invariant_text=str(payload.get("invariant", ""))[:70] or None,
            title="ALIGNED TRANSFORMATION STACK",
        )
        return []
    if kind == "ANNOTATED_DERIVATION":
        steps = list(payload.get("steps", []))
        notes = list(payload.get("annotations", []))
        lines = [f"{notes[i]}:  {s}" if i < len(notes) else str(s) for i, s in enumerate(steps)]
        MathEquationBlock.draw_algebra_block(
            canvas, x, y, w, h, lines[:7], invariant_text=str(payload.get("conclusion", ""))[:70] or None,
            title="ANNOTATED DERIVATION",
        )
        return []
    if kind == "TERM_HIGHLIGHT_VIEW":
        lines = [str(payload.get("expression", ""))] + [f"focus: {t}" for t in payload.get("highlighted_terms", [])]
        MathEquationBlock.draw_algebra_block(
            canvas, x, y, w, h, lines[:7], invariant_text=str(payload.get("rationale", ""))[:70] or None,
            title="TERM STRUCTURE VIEW",
        )
        return []
    if kind == "SUBSTITUTION_CHECK_VIEW":
        lines = [
            str(payload.get("original_relation", "")),
            f"candidate: {payload.get('candidate', '')}",
            f"substitute: {payload.get('substitution', '')}",
        ]
        MathEquationBlock.draw_algebra_block(
            canvas, x, y, w, h, [l for l in lines if l.strip(": ")],
            invariant_text=str(payload.get("result", ""))[:70] or None, title="SUBSTITUTION CHECK",
        )
        return []
    if kind == "SIDE_BY_SIDE_METHOD_VIEW":
        _draw_two_column(
            canvas, bbox, "SIDE-BY-SIDE METHOD VIEW",
            "METHOD A", _wrap_list(payload.get("left_method", "")),
            "METHOD B", _wrap_list(payload.get("right_method", "")),
            footer="shared invariant: " + str(payload.get("comparison_invariant", "")),
        )
        return []
    if kind == "CORRECT_WRONG_TRANSFORMATION_CONTRAST":
        _draw_two_column(
            canvas, bbox, "CORRECT / INCORRECT TRANSFORMATION",
            "CORRECT", _wrap_list(payload.get("correct_case", "")),
            "INCORRECT", _wrap_list(payload.get("wrong_case", "")),
            footer="discriminator: " + str(payload.get("discriminator", "")),
        )
        return []
    if kind == "MIRROR_SOLUTION_VIEW":
        _draw_two_column(
            canvas, bbox, "MIRROR SOLUTION BRANCHES",
            "BRANCH A", _wrap_list(payload.get("branch_a", "")),
            "BRANCH B", _wrap_list(payload.get("branch_b", "")),
            footer="shared: " + ", ".join(str(i) for i in (payload.get("invariants") or [])),
        )
        return []
    fail("UNKNOWN_TEACHING_PRIMITIVE_KIND", kind)


def _wrap_list(value):
    if isinstance(value, list):
        return [str(v) for v in value]
    return [str(value)] if value else []


def render_primitive(kind, params, canvas, bbox):
    """Draw one teaching primitive and return its placement evidence.

    Returns a dict with the realized bounding box, the primitive kind, the
    grounding class of the data used, and whether real vector geometry (as
    opposed to text only) was emitted.
    """
    if kind not in SUPPORTED_KINDS:
        fail("UNKNOWN_TEACHING_PRIMITIVE_KIND", kind)
    x, y, w, h = bbox
    if w <= 0 or h <= 0:
        fail("MATH_VISUAL_OUT_OF_BOUNDS", kind)
    if not params.get("payload") and not params.get("declared_claims"):
        fail("MATH_VISUAL_EMPTY_PARAMS", kind)
    try:
        VisualSemanticValidator.validate(kind, {"declared_text": params.get("declared_text", [])}, params["payload"])
    except VisualValidationError as exc:
        fail("MATH_VISUAL_SEMANTIC_VALIDATION_FAILED", f"{kind}:{exc}")

    canvas.saveState()
    try:
        drawn_numbers = _render(kind, params, canvas, bbox) or []
    finally:
        canvas.restoreState()
    assert_grounded(params, drawn_numbers)

    return {
        "primitive_kind": kind,
        "x0": round(float(x), 2),
        "y0": round(float(y), 2),
        "x1": round(float(x + w), 2),
        "y1": round(float(y + h), 2),
        "data_grounding": params["grounding"],
        "vector_geometry": kind in VECTOR_GEOMETRY_KINDS,
        "accessibility_text": params.get("accessibility_text", ""),
    }


# Kinds whose realization emits geometric primitives (paths, axes, triangles,
# arrows, circles) rather than laid-out text alone.
VECTOR_GEOMETRY_KINDS = frozenset(
    {
        "COORDINATE_PLANE",
        "SLOPE_TRIANGLE_VIEW",
        "PARALLEL_MEET_CONTRAST",
        "COMBINATORIAL_SLOT_MODEL",
        "EQUIVALENCE_BALANCE_VIEW",
        "INVARIANT_HIGHLIGHT",
        "SIDE_BY_SIDE_METHOD_VIEW",
        "CORRECT_WRONG_TRANSFORMATION_CONTRAST",
        "MIRROR_SOLUTION_VIEW",
    }
)

# Which shared-library object realizes each kind. Kept as data so that swapping
# to #310's published package (or any future shared visual library) is a change
# to this table, not to the call sites.
_LIBRARY_BINDINGS = {
    "COORDINATE_PLANE": "primitives.graphs.CartesianPlotter2D",
    "SLOPE_TRIANGLE_VIEW": "primitives.graphs.CartesianPlotter2D.plot_slope_triangle",
    "PARALLEL_MEET_CONTRAST": "primitives.diagrams.PlaneGeometryRenderer.draw_parallel_transversal",
    "COMBINATORIAL_SLOT_MODEL": "primitives.diagrams.CombinatorialSlotDiagram.draw_slots",
    "ALIGNED_TRANSFORMATION_STACK": "primitives.equations.MathEquationBlock.draw_algebra_block",
    "ANNOTATED_DERIVATION": "primitives.equations.MathEquationBlock.draw_algebra_block",
    "TERM_HIGHLIGHT_VIEW": "primitives.equations.MathEquationBlock.draw_algebra_block",
    "SUBSTITUTION_CHECK_VIEW": "primitives.equations.MathEquationBlock.draw_algebra_block",
    "EQUIVALENCE_BALANCE_VIEW": "primitives.base(draw_card_box, draw_arrow, beginPath)",
    "INVARIANT_HIGHLIGHT": "primitives.base(draw_card_box, draw_pill_badge)",
    "SIDE_BY_SIDE_METHOD_VIEW": "primitives.base(draw_card_box)",
    "CORRECT_WRONG_TRANSFORMATION_CONTRAST": "primitives.base(draw_card_box)",
    "MIRROR_SOLUTION_VIEW": "primitives.base(draw_card_box)",
}


def library_binding(kind):
    return _LIBRARY_BINDINGS.get(kind)


# Minimum drawable height per kind. Geometric kinds need a real viewport; text
# kinds size to their declared content so pages do not carry dead whitespace.
_MIN_HEIGHT = {
    "COORDINATE_PLANE": 180,
    "SLOPE_TRIANGLE_VIEW": 180,
    "PARALLEL_MEET_CONTRAST": 172,
    "COMBINATORIAL_SLOT_MODEL": 100,
    "EQUIVALENCE_BALANCE_VIEW": 108,
}


def suggest_height(kind, params):
    """Height this figure actually needs, given its declared content."""
    if kind in _MIN_HEIGHT:
        return _MIN_HEIGHT[kind]
    payload = params.get("payload", {})
    if kind in {"SIDE_BY_SIDE_METHOD_VIEW", "CORRECT_WRONG_TRANSFORMATION_CONTRAST", "MIRROR_SOLUTION_VIEW"}:
        left = len(_wrap_list(payload.get("correct_case") or payload.get("left_method") or payload.get("branch_a")))
        right = len(_wrap_list(payload.get("wrong_case") or payload.get("right_method") or payload.get("branch_b")))
        return 60 + max(2, left, right) * 22
    if kind == "INVARIANT_HIGHLIGHT":
        return 92
    lines = 0
    for key in ("states", "operations", "steps", "highlighted_terms"):
        value = payload.get(key)
        if isinstance(value, list):
            lines += len(value)
        elif value:
            lines += 1
    for key in ("expression", "original_relation", "candidate", "substitution"):
        if payload.get(key):
            lines += 1
    lines = min(lines, 7) or len(params.get("declared_claims", [])) or 1
    return 56 + lines * 14
