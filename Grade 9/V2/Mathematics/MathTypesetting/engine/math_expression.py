#!/usr/bin/env python3
"""Mathematics V2 — semantic math-expression typesetting (M-UPGRADE-2 item 1).

Root cause addressed (PR #323 RCA): learner-visible mathematics was passed to the
renderer as an opaque string and then flattened by an ``ascii_safe()`` substitution
table, so ``√72 = 6√2`` reached the learner as ``sqrt(72)=6sqrt(2)``. Layout cannot
recover structure that was destroyed upstream.

This module replaces that path with a structured ``MathExpression`` AST plus a real
typesetter:

* ``typeset_unicode``  -> audit/accessibility string using the exact bound glyphs
* ``measure``/``draw`` -> a measured box tree drawn on a ReportLab canvas with real
  fraction rules, radical overbars and raised/lowered scripts at reduced size
* ``audit_expressions`` -> the fail-closed falsifier set

The AST is subject-wide generic. Number Systems, Polynomials, Coordinate Geometry
and every other topic are *data instances* of these node kinds; no node kind is
topic specific.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

PHASE = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = PHASE / "registry" / "math-glyph-binding-registry.json"
DEFAULT_POLICY = PHASE / "policies" / "math-typesetting-policy.json"

FALSIFIERS = (
    "MATH_EXPRESSION_FLATTENED_TO_PLAIN_TEXT",
    "MATH_FONT_NOT_BOUND",
    "MATH_RELATION_RENDERED_AS_ASCII_FALLBACK",
    "MATH_SCRIPT_NOT_TYPESET",
    "MATH_REQUIRED_GLYPH_MISSING",
    "MATH_SEMANTIC_AST_RENDER_MISMATCH",
    "MATH_TRANSFORMATION_ALIGNMENT_LOST",
    "MATH_TYPESETTING_GATE_FAILED",
)


# --------------------------------------------------------------------------
# deterministic helpers (same convention as the rest of the Mathematics chain)
# --------------------------------------------------------------------------
def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any, omit: str | None = None) -> str:
    item = copy.deepcopy(value)
    if omit and isinstance(item, dict):
        item.pop(omit, None)
    return hashlib.sha256(canonical(item).encode("utf-8")).hexdigest()


def load(path: Path | str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def fail(code: str, detail: str = "") -> None:
    raise ValueError(f"{code}:{detail}" if detail else code)


# --------------------------------------------------------------------------
# AST constructors — keep call sites readable and structurally valid by design
# --------------------------------------------------------------------------
def num(value: Any) -> dict:
    return {"node": "NUMBER", "value": str(value)}


def sym(name: str) -> dict:
    return {"node": "SYMBOL", "name": str(name)}


def txt(text: str) -> dict:
    return {"node": "TEXT", "text": str(text)}


def op(operator: str) -> dict:
    return {"node": "OPERATOR", "operator": operator}


def rel(relation: str) -> dict:
    return {"node": "RELATION", "relation": relation}


def group(child: dict, fence: str = "PAREN") -> dict:
    return {"node": "GROUP", "child": child, "fence": fence}


def seq(*items: dict) -> dict:
    flat = [x for x in items if x is not None]
    return {"node": "SEQUENCE", "items": flat}


def frac(numerator: dict, denominator: dict) -> dict:
    return {"node": "FRACTION", "numerator": numerator, "denominator": denominator}


def radical(radicand: dict, index: dict | None = None) -> dict:
    out = {"node": "RADICAL", "radicand": radicand}
    if index is not None:
        out["index"] = index
    return out


def power(base: dict, exponent: dict) -> dict:
    return {"node": "POWER", "base": base, "exponent": exponent}


def sub(base: dict, subscript: dict) -> dict:
    return {"node": "SUBSCRIPT", "base": base, "subscript": subscript}


def sup(base: dict, superscript: dict) -> dict:
    return {"node": "SUPERSCRIPT", "base": base, "superscript": superscript}


def call(name: str, *arguments: dict) -> dict:
    return {"node": "FUNCTION_CALL", "name": name, "arguments": list(arguments)}


def setrel(relation: str, *operands: dict) -> dict:
    return {"node": "SET_NOTATION", "relation": relation, "operands": list(operands)}


def aligned(*lines: tuple) -> dict:
    out = []
    for line in lines:
        lhs, relation, rhs = line[0], line[1], line[2]
        annotation = line[3] if len(line) > 3 else None
        out.append({"lhs": lhs, "relation": rel(relation) if isinstance(relation, str) else relation,
                    "rhs": rhs, "annotation": annotation})
    return {"node": "ALIGNED_EQUATION", "lines": out}


def chain(*steps: tuple) -> dict:
    return {"node": "TRANSFORMATION_CHAIN",
            "steps": [{"expression": e, "justification": j} for e, j in steps]}


# --------------------------------------------------------------------------
# glyph binding
# --------------------------------------------------------------------------
@dataclass(frozen=True)
class FontBinding:
    """A resolved, math-capable font. Base-14 fallbacks are never acceptable."""

    family: str
    regular_name: str
    bold_name: str
    regular_path: str
    bold_path: str

    def supports(self, text: str) -> list[str]:
        face = pdfmetrics.getFont(self.regular_name).face
        cmap = getattr(face, "charToGlyph", {})
        return sorted({ch for ch in text if ord(ch) not in cmap and ch not in " \n\t"})


class GlyphRegistry:
    """Semantic token -> exact bound code point, plus the portable font policy."""

    def __init__(self, registry: dict | None = None):
        self.data = registry if registry is not None else load(DEFAULT_REGISTRY)
        self.operators = self.data["operators"]
        self.relations = self.data["relations"]
        self.set_relations = self.data["set_relations"]
        self.fences = self.data["fences"]
        self.named_symbols = self.data["named_symbols"]
        self.radical_sign = self.data["radical_sign"]
        self.superscripts = self.data["superscript_digits"]
        self.subscripts = self.data["subscript_digits"]
        self.forbidden = self.data["forbidden_ascii_flattenings"]

    # -- symbol resolution ------------------------------------------------
    def symbol(self, name: str) -> str:
        return self.named_symbols.get(name, name)

    def operator(self, name: str) -> str:
        if name not in self.operators:
            fail("MATH_REQUIRED_GLYPH_MISSING", f"operator:{name}")
        return self.operators[name]

    def relation(self, name: str) -> str:
        if name not in self.relations:
            fail("MATH_REQUIRED_GLYPH_MISSING", f"relation:{name}")
        return self.relations[name]

    def set_relation(self, name: str) -> str:
        if name not in self.set_relations:
            fail("MATH_REQUIRED_GLYPH_MISSING", f"set_relation:{name}")
        return self.set_relations[name]

    def fence(self, name: str) -> tuple[str, str]:
        pair = self.fences.get(name)
        if pair is None:
            fail("MATH_REQUIRED_GLYPH_MISSING", f"fence:{name}")
        return pair[0], pair[1]

    # -- font binding -----------------------------------------------------
    def bind_font(self, required_text: str = "") -> FontBinding:
        binding = self.data["font_binding"]
        for candidate in binding["candidates"]:
            regular, bold = Path(candidate["regular"]), Path(candidate["bold"])
            if not (regular.exists() and bold.exists()):
                continue
            names = (f"MathTypeset-{candidate['family']}-Regular",
                     f"MathTypeset-{candidate['family']}-Bold")
            for name, path in zip(names, (regular, bold)):
                try:
                    pdfmetrics.getFont(name)
                except Exception:
                    pdfmetrics.registerFont(TTFont(name, str(path)))
            bound = FontBinding(candidate["family"], names[0], names[1], str(regular), str(bold))
            missing = bound.supports(required_text) if required_text else []
            if missing:
                continue
            return bound
        fail("MATH_FONT_NOT_BOUND",
             "no portable math-capable font covers the required glyph set; "
             f"forbidden fallbacks={','.join(binding['forbidden_fallbacks'])}")
        raise AssertionError("unreachable")


# --------------------------------------------------------------------------
# UNICODE target
# --------------------------------------------------------------------------
def _script_string(text: str, table: dict[str, str]) -> str | None:
    out = []
    for ch in text:
        mapped = table.get(ch)
        if mapped is None:
            return None
        out.append(mapped)
    return "".join(out)


def typeset_unicode(node: dict, reg: GlyphRegistry | None = None) -> str:
    """Render the AST to the accessibility/audit string with the bound glyphs."""
    reg = reg or GlyphRegistry()
    kind = node.get("node")

    if kind == "NUMBER":
        return str(node["value"]).replace("-", reg.operator("MINUS"))
    if kind == "SYMBOL":
        return reg.symbol(node["name"])
    if kind == "TEXT":
        return str(node["text"])
    if kind == "OPERATOR":
        return f" {reg.operator(node['operator'])} "
    if kind == "RELATION":
        return f" {reg.relation(node['relation'])} "
    if kind == "GROUP":
        left, right = reg.fence(node["fence"])
        return f"{left}{typeset_unicode(node['child'], reg)}{right}"
    if kind == "SEQUENCE":
        return "".join(typeset_unicode(x, reg) for x in node["items"])
    if kind == "FRACTION":
        top = typeset_unicode(node["numerator"], reg)
        bottom = typeset_unicode(node["denominator"], reg)
        return f"{_wrap_if_compound(node['numerator'], top)}⁄{_wrap_if_compound(node['denominator'], bottom)}"
    if kind == "RADICAL":
        index = node.get("index")
        body = typeset_unicode(node["radicand"], reg)
        lead = ""
        if index is not None:
            lead = _script_string(typeset_unicode(index, reg), reg.superscripts) or ""
        # a compound radicand keeps an explicit fence so the scope stays unambiguous
        if _is_compound(node["radicand"]):
            body = f"({body})"
        return f"{lead}{reg.radical_sign}{body}"
    if kind in ("POWER", "SUPERSCRIPT"):
        base = node["base"]
        script_node = node["exponent"] if kind == "POWER" else node["superscript"]
        base_text = typeset_unicode(base, reg)
        if _is_compound(base) and base.get("node") != "GROUP":
            base_text = f"({base_text})"
        script_text = typeset_unicode(script_node, reg)
        scripted = _script_string(script_text, reg.superscripts)
        if scripted is None:
            fail("MATH_SCRIPT_NOT_TYPESET",
                 f"superscript '{script_text}' has no bound superscript code points")
        return f"{base_text}{scripted}"
    if kind == "SUBSCRIPT":
        base_text = typeset_unicode(node["base"], reg)
        script_text = typeset_unicode(node["subscript"], reg)
        scripted = _script_string(script_text, reg.subscripts)
        if scripted is None:
            fail("MATH_SCRIPT_NOT_TYPESET",
                 f"subscript '{script_text}' has no bound subscript code points")
        return f"{base_text}{scripted}"
    if kind == "FUNCTION_CALL":
        args = ", ".join(typeset_unicode(a, reg) for a in node["arguments"])
        return f"{node['name']}({args})"
    if kind == "SET_NOTATION":
        glyph = reg.set_relation(node["relation"])
        return f" {glyph} ".join(typeset_unicode(x, reg) for x in node["operands"])
    if kind == "ALIGNED_EQUATION":
        out = []
        for line in node["lines"]:
            body = (f"{typeset_unicode(line['lhs'], reg)}"
                    f"{typeset_unicode(line['relation'], reg)}"
                    f"{typeset_unicode(line['rhs'], reg)}")
            if line.get("annotation"):
                body = f"{body}    [{line['annotation']}]"
            out.append(body)
        return "\n".join(out)
    if kind == "TRANSFORMATION_CHAIN":
        return "\n".join(
            f"{typeset_unicode(s['expression'], reg)}    [{s['justification']}]"
            for s in node["steps"]
        )
    fail("MATH_SEMANTIC_AST_RENDER_MISMATCH", f"unknown node kind:{kind}")
    raise AssertionError("unreachable")


def _is_compound(node: dict) -> bool:
    return node.get("node") in ("SEQUENCE", "FRACTION", "SET_NOTATION", "ALIGNED_EQUATION",
                                "TRANSFORMATION_CHAIN")


def _wrap_if_compound(node: dict, text: str) -> str:
    return f"({text})" if _is_compound(node) else text


def required_glyphs(node: dict, reg: GlyphRegistry | None = None) -> set[str]:
    reg = reg or GlyphRegistry()
    return {ch for ch in typeset_unicode(node, reg) if ch not in " \n\t"}


def expression_signature(node: dict) -> list[str]:
    """Ordered structural anchors the rendered surface must still contain.

    Used by MATH_SEMANTIC_AST_RENDER_MISMATCH: if a renderer drops a radical, a
    script or a relation, the anchor sequence no longer appears in the output.
    """
    reg = GlyphRegistry()
    anchors: list[str] = []

    def walk(n: dict) -> None:
        kind = n.get("node")
        if kind == "RADICAL":
            anchors.append(reg.radical_sign)
            walk(n["radicand"])
        elif kind in ("POWER", "SUPERSCRIPT"):
            walk(n["base"])
            script = typeset_unicode(n["exponent"] if kind == "POWER" else n["superscript"], reg)
            scripted = _script_string(script, reg.superscripts)
            if scripted:
                anchors.append(scripted)
        elif kind == "SUBSCRIPT":
            walk(n["base"])
            scripted = _script_string(typeset_unicode(n["subscript"], reg), reg.subscripts)
            if scripted:
                anchors.append(scripted)
        elif kind == "RELATION":
            anchors.append(reg.relation(n["relation"]))
        elif kind == "SET_NOTATION":
            for i, operand in enumerate(n["operands"]):
                if i:
                    anchors.append(reg.set_relation(n["relation"]))
                walk(operand)
        elif kind == "OPERATOR":
            anchors.append(reg.operator(n["operator"]))
        elif kind == "SEQUENCE":
            for item in n["items"]:
                walk(item)
        elif kind == "GROUP":
            walk(n["child"])
        elif kind == "FRACTION":
            walk(n["numerator"])
            walk(n["denominator"])
        elif kind == "FUNCTION_CALL":
            for arg in n["arguments"]:
                walk(arg)
        elif kind == "ALIGNED_EQUATION":
            for line in n["lines"]:
                walk(line["lhs"])
                walk(line["relation"])
                walk(line["rhs"])
        elif kind == "TRANSFORMATION_CHAIN":
            for step in n["steps"]:
                walk(step["expression"])
        elif kind in ("NUMBER", "SYMBOL", "TEXT"):
            return
    walk(node)
    return anchors


# --------------------------------------------------------------------------
# TYPESET target — measured boxes drawn on a ReportLab canvas
# --------------------------------------------------------------------------
@dataclass
class Box:
    """A measured typeset box.

    ``ascent``/``descent`` are measured from the box's own baseline so that scripts,
    fractions and radicals compose correctly instead of being placed by guesswork.
    """

    width: float
    ascent: float
    descent: float
    draw: Callable[[Any, float, float], None]

    @property
    def height(self) -> float:
        return self.ascent + self.descent


SCRIPT_RATIO = 0.68
SCRIPT_RAISE = 0.42
SCRIPT_DROP = 0.20
RULE_RATIO = 0.055


class Typesetter:
    """Measure-then-draw typesetting for the MathExpression AST."""

    def __init__(self, font: FontBinding, reg: GlyphRegistry | None = None,
                 policy: dict | None = None):
        self.font = font
        self.reg = reg or GlyphRegistry()
        self.policy = policy if policy is not None else load(DEFAULT_POLICY)
        fp = self.policy["font_policy"]
        self.min_script_ratio = float(fp["min_script_size_ratio"])
        self.min_script_pt = float(fp["min_absolute_script_pt"])

    # -- primitive --------------------------------------------------------
    def _text_box(self, text: str, size: float, bold: bool = False) -> Box:
        name = self.font.bold_name if bold else self.font.regular_name
        missing = self.font.supports(text)
        if missing:
            fail("MATH_REQUIRED_GLYPH_MISSING",
                 f"font={self.font.family} missing={''.join(missing)}")
        width = pdfmetrics.stringWidth(text, name, size)
        ascent = pdfmetrics.getAscent(name, size)
        descent = abs(pdfmetrics.getDescent(name, size))

        def draw(canvas, x: float, y: float) -> None:
            canvas.setFont(name, size)
            canvas.drawString(x, y, text)

        return Box(width, ascent, descent, draw)

    def _script_size(self, size: float) -> float:
        scripted = size * SCRIPT_RATIO
        if scripted < self.min_script_pt or SCRIPT_RATIO < self.min_script_ratio:
            fail("MATH_SCRIPT_NOT_TYPESET",
                 f"script size {scripted:.2f}pt below readable minimum "
                 f"{self.min_script_pt:.2f}pt at body {size:.2f}pt")
        return scripted

    def _row(self, boxes: list[Box], gap: float = 0.0) -> Box:
        boxes = [b for b in boxes if b is not None]
        if not boxes:
            return Box(0.0, 0.0, 0.0, lambda c, x, y: None)
        width = sum(b.width for b in boxes) + gap * (len(boxes) - 1)
        ascent = max(b.ascent for b in boxes)
        descent = max(b.descent for b in boxes)

        def draw(canvas, x: float, y: float) -> None:
            cursor = x
            for b in boxes:
                b.draw(canvas, cursor, y)
                cursor += b.width + gap

        return Box(width, ascent, descent, draw)

    # -- public -----------------------------------------------------------
    def measure(self, node: dict, size: float) -> Box:
        kind = node.get("node")

        if kind in ("NUMBER", "SYMBOL", "TEXT"):
            return self._text_box(typeset_unicode(node, self.reg), size)
        if kind == "OPERATOR":
            return self._text_box(f" {self.reg.operator(node['operator'])} ", size)
        if kind == "RELATION":
            return self._text_box(f" {self.reg.relation(node['relation'])} ", size)
        if kind == "SEQUENCE":
            return self._row([self.measure(x, size) for x in node["items"]])
        if kind == "GROUP":
            left, right = self.reg.fence(node["fence"])
            inner = self.measure(node["child"], size)
            parts = []
            if left:
                parts.append(self._text_box(left, size))
            parts.append(inner)
            if right:
                parts.append(self._text_box(right, size))
            return self._row(parts)
        if kind == "FUNCTION_CALL":
            parts: list[Box] = [self._text_box(f"{node['name']}(", size)]
            for i, arg in enumerate(node["arguments"]):
                if i:
                    parts.append(self._text_box(", ", size))
                parts.append(self.measure(arg, size))
            parts.append(self._text_box(")", size))
            return self._row(parts)
        if kind == "SET_NOTATION":
            glyph = self.reg.set_relation(node["relation"])
            parts = []
            for i, operand in enumerate(node["operands"]):
                if i:
                    parts.append(self._text_box(f" {glyph} ", size))
                parts.append(self.measure(operand, size))
            return self._row(parts)
        if kind == "FRACTION":
            return self._fraction(node, size)
        if kind == "RADICAL":
            return self._radical(node, size)
        if kind in ("POWER", "SUPERSCRIPT"):
            script = node["exponent"] if kind == "POWER" else node["superscript"]
            return self._script(node["base"], script, size, raised=True)
        if kind == "SUBSCRIPT":
            return self._script(node["base"], node["subscript"], size, raised=False)
        if kind == "ALIGNED_EQUATION":
            return self._aligned(node, size)
        if kind == "TRANSFORMATION_CHAIN":
            return self._chain(node, size)
        fail("MATH_SEMANTIC_AST_RENDER_MISMATCH", f"unknown node kind:{kind}")
        raise AssertionError("unreachable")

    # -- structural node builders ----------------------------------------
    def _fraction(self, node: dict, size: float) -> Box:
        top = self.measure(node["numerator"], size * 0.94)
        bottom = self.measure(node["denominator"], size * 0.94)
        pad = size * 0.16
        width = max(top.width, bottom.width) + pad * 2
        rule = max(size * RULE_RATIO, 0.4)
        axis = size * 0.30                       # rule sits on the math axis
        ascent = axis + rule + top.height + size * 0.10
        descent = bottom.height + size * 0.10 - axis
        descent = max(descent, bottom.height * 0.5)

        def draw(canvas, x: float, y: float) -> None:
            rule_y = y + axis
            canvas.setLineWidth(rule)
            canvas.setStrokeColorRGB(0, 0, 0)
            canvas.line(x, rule_y, x + width, rule_y)
            top.draw(canvas, x + (width - top.width) / 2.0, rule_y + rule + top.descent + size * 0.08)
            bottom.draw(canvas, x + (width - bottom.width) / 2.0, rule_y - bottom.ascent - size * 0.08)

        return Box(width, ascent, descent, draw)

    def _radical(self, node: dict, size: float) -> Box:
        body = self.measure(node["radicand"], size)
        sign = self._text_box(self.reg.radical_sign, size)
        index_box = None
        if node.get("index") is not None:
            index_box = self.measure(node["index"], self._script_size(size) * 0.85)
        overbar = max(size * RULE_RATIO, 0.4)
        gap = size * 0.08
        lead = index_box.width * 0.75 if index_box else 0.0
        width = lead + sign.width + body.width + gap
        ascent = max(sign.ascent, body.ascent + overbar + gap)
        if index_box:
            ascent = max(ascent, sign.ascent + index_box.ascent * 0.4)
        descent = max(sign.descent, body.descent)

        def draw(canvas, x: float, y: float) -> None:
            if index_box:
                index_box.draw(canvas, x, y + sign.ascent * 0.45)
            sign.draw(canvas, x + lead, y)
            body_x = x + lead + sign.width
            body.draw(canvas, body_x, y)
            bar_y = y + max(sign.ascent, body.ascent) + gap * 0.5
            canvas.setLineWidth(overbar)
            canvas.setStrokeColorRGB(0, 0, 0)
            canvas.line(body_x - gap * 0.2, bar_y, body_x + body.width + gap * 0.6, bar_y)

        return Box(width, ascent, descent, draw)

    def _script(self, base_node: dict, script_node: dict, size: float, raised: bool) -> Box:
        base = self.measure(base_node, size)
        script_size = self._script_size(size)
        script = self.measure(script_node, script_size)
        shift = size * (SCRIPT_RAISE if raised else -SCRIPT_DROP)
        width = base.width + script.width
        ascent = max(base.ascent, shift + script.ascent)
        descent = max(base.descent, -shift + script.descent)

        def draw(canvas, x: float, y: float) -> None:
            base.draw(canvas, x, y)
            script.draw(canvas, x + base.width, y + shift)

        return Box(width, ascent, descent, draw)

    def _aligned(self, node: dict, size: float) -> Box:
        rows = []
        for line in node["lines"]:
            lhs = self.measure(line["lhs"], size)
            relation = self.measure(line["relation"], size)
            rhs = self.measure(line["rhs"], size)
            note = None
            if line.get("annotation"):
                note = self._text_box(f"   {line['annotation']}", size * 0.82)
            rows.append((lhs, relation, rhs, note))
        anchor = max(r[0].width for r in rows)
        width = anchor + max(r[1].width + r[2].width + (r[3].width if r[3] else 0.0) for r in rows)
        leading = size * 1.62
        ascent = max(r[0].ascent for r in rows) if rows else 0.0
        total = leading * (len(rows) - 1)
        descent = (max(r[0].descent for r in rows) if rows else 0.0) + total

        def draw(canvas, x: float, y: float) -> None:
            cursor_y = y
            for lhs, relation, rhs, note in rows:
                lhs.draw(canvas, x + anchor - lhs.width, cursor_y)
                relation.draw(canvas, x + anchor, cursor_y)
                rhs.draw(canvas, x + anchor + relation.width, cursor_y)
                if note:
                    note.draw(canvas, x + anchor + relation.width + rhs.width, cursor_y)
                cursor_y -= leading

        box = Box(width, ascent, descent, draw)
        box.alignment_anchor = anchor  # type: ignore[attr-defined]
        box.row_count = len(rows)      # type: ignore[attr-defined]
        return box

    def _chain(self, node: dict, size: float) -> Box:
        rows = []
        for step in node["steps"]:
            expr = self.measure(step["expression"], size)
            note = self._text_box(f"   {step['justification']}", size * 0.82)
            rows.append((expr, note))
        width = max(e.width + n.width for e, n in rows)
        leading = size * 1.62
        ascent = max(e.ascent for e, _ in rows)
        descent = max(e.descent for e, _ in rows) + leading * (len(rows) - 1)

        def draw(canvas, x: float, y: float) -> None:
            cursor_y = y
            for expr, note in rows:
                expr.draw(canvas, x, cursor_y)
                note.draw(canvas, x + expr.width, cursor_y)
                cursor_y -= leading

        box = Box(width, ascent, descent, draw)
        box.alignment_anchor = 0.0   # type: ignore[attr-defined]
        box.row_count = len(rows)    # type: ignore[attr-defined]
        return box


# --------------------------------------------------------------------------
# falsifiers
# --------------------------------------------------------------------------
_SCRIPT_CHARS = set("⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿⁱ₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₙₓ")
_ASCII_POWER_RE = re.compile(r"[A-Za-z0-9\)\]]\^\s*-?\d")
_ASCII_SUBSCRIPT_RE = re.compile(r"[A-Za-z]_\d")


def detect_flattening(text: str, reg: GlyphRegistry | None = None) -> list[str]:
    """Return the falsifier codes raised by an already-rendered learner string."""
    reg = reg or GlyphRegistry()
    lowered = str(text).lower()
    found: list[str] = []
    for entry in reg.forbidden:
        pattern = entry["pattern"]
        if pattern == "^":
            if _ASCII_POWER_RE.search(text):
                found.append(f"{entry['falsifier']}:caret_power")
            continue
        if entry.get("regex"):
            # some flattenings need a word boundary: " deg" must catch "90 deg" but
            # must not fire on the ordinary English word "degrees"
            if re.search(entry["regex"], text, re.IGNORECASE):
                found.append(f"{entry['falsifier']}:{pattern.strip()}")
            continue
        if pattern in lowered:
            found.append(f"{entry['falsifier']}:{pattern.strip()}")
    if _ASCII_SUBSCRIPT_RE.search(text):
        found.append("MATH_EXPRESSION_FLATTENED_TO_PLAIN_TEXT:underscore_subscript")
    return sorted(set(found))


def audit_expressions(expressions: dict[str, dict], *, font: FontBinding | None = None,
                      reg: GlyphRegistry | None = None, policy: dict | None = None) -> dict:
    """Fail-closed audit of a corpus of learner-visible MathExpression objects.

    ``expressions`` maps a learner-visible location id (for example
    ``"NUMBER_SYSTEMS/worked-1/step-2"``) to the AST that must be typeset there.
    """
    reg = reg or GlyphRegistry()
    policy = policy if policy is not None else load(DEFAULT_POLICY)
    failures: list[str] = []

    corpus = "".join(sorted(set("".join(
        typeset_unicode(node, reg) for node in expressions.values()
    ))))
    font = font or reg.bind_font(corpus)
    if font.family in reg.data["font_binding"]["forbidden_fallbacks"]:
        failures.append(f"MATH_FONT_NOT_BOUND:{font.family}")
    missing = font.supports(corpus)
    if missing:
        failures.append(f"MATH_REQUIRED_GLYPH_MISSING:{''.join(missing)}")

    typesetter = Typesetter(font, reg, policy)
    structural = set(policy["required_structural_nodes"])
    seen_nodes: set[str] = set()
    tolerance = float(policy["alignment_policy"]["alignment_tolerance_pt"])

    for location, node in sorted(expressions.items()):
        rendered = typeset_unicode(node, reg)
        for code in detect_flattening(rendered, reg):
            failures.append(f"{code}@{location}")
        for anchor in expression_signature(node):
            if anchor.strip() and anchor not in rendered:
                failures.append(f"MATH_SEMANTIC_AST_RENDER_MISMATCH:{anchor}@{location}")
        seen_nodes |= _node_kinds(node)
        if _node_kinds(node) & {"POWER", "SUPERSCRIPT", "SUBSCRIPT"}:
            if not (_SCRIPT_CHARS & set(rendered)):
                failures.append(f"MATH_SCRIPT_NOT_TYPESET:{location}")
        try:
            box = typesetter.measure(node, 11.0)
        except ValueError as exc:
            # keep the audit aggregating: one unmeasurable expression must not hide
            # the rest of the corpus behind a single raised exception
            failures.append(f"{exc}@{location}")
            continue
        if node["node"] in ("ALIGNED_EQUATION", "TRANSFORMATION_CHAIN"):
            anchor_value = getattr(box, "alignment_anchor", None)
            rows = getattr(box, "row_count", 0)
            if anchor_value is None or rows < 2:
                failures.append(f"MATH_TRANSFORMATION_ALIGNMENT_LOST:{location}")
            elif node["node"] == "ALIGNED_EQUATION":
                widths = [typesetter.measure(l["lhs"], 11.0).width for l in node["lines"]]
                if any(w - anchor_value > tolerance for w in widths):
                    failures.append(f"MATH_TRANSFORMATION_ALIGNMENT_LOST:{location}")
        if box.width <= 0 or box.height <= 0:
            failures.append(f"MATH_SEMANTIC_AST_RENDER_MISMATCH:zero_box@{location}")

    if failures:
        fail("MATH_TYPESETTING_GATE_FAILED", "|".join(sorted(set(failures))))

    return {
        "status": "PASS",
        "expression_count": len(expressions),
        "font_family": font.family,
        "font_regular_path": font.regular_path,
        "structural_nodes_exercised": sorted(seen_nodes & structural),
        "structural_nodes_declared": sorted(structural),
        "glyph_corpus_size": len(set(corpus)),
        "corpus_digest": digest(sorted(expressions.items())),
        "checks": [
            "PORTABLE_MATH_FONT_BOUND",
            "ALL_REQUIRED_GLYPHS_PRESENT",
            "NO_ASCII_FLATTENING",
            "NO_ASCII_RELATION_FALLBACK",
            "SCRIPTS_TYPESET",
            "AST_ANCHORS_SURVIVE_RENDER",
            "TRANSFORMATION_ALIGNMENT_PRESERVED",
        ],
        "release_meaning": "PUBLICATION_ENGINEERING only; subject/pedagogy/expert review PENDING",
    }


def _node_kinds(node: Any) -> set[str]:
    kinds: set[str] = set()
    if isinstance(node, dict):
        if "node" in node:
            kinds.add(node["node"])
        for value in node.values():
            kinds |= _node_kinds(value)
    elif isinstance(node, list):
        for item in node:
            kinds |= _node_kinds(item)
    return kinds


def node_kinds(node: dict) -> set[str]:
    return _node_kinds(node)


if __name__ == "__main__":  # pragma: no cover - manual smoke check
    registry = GlyphRegistry()
    demo = {
        "surd": aligned(
            (radical(num(72)), "EQ", seq(radical(seq(num(36), op("TIMES"), num(2))))),
            (radical(num(72)), "EQ", seq(num(6), radical(num(2)))),
        ),
        "number_line": setrel("SUBSET", sym("NATURALS"), sym("WHOLES"), sym("INTEGERS"),
                              sym("RATIONALS"), sym("REALS")),
        "square": power(group(seq(sym("x"), op("MINUS"), sym("a"))), num(2)),
    }
    print(typeset_unicode(demo["surd"], registry))
    print(typeset_unicode(demo["number_line"], registry))
    print(typeset_unicode(demo["square"], registry))
    print(json.dumps(audit_expressions(demo), indent=2, ensure_ascii=False))
