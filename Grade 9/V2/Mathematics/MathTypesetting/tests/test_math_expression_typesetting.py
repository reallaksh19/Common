#!/usr/bin/env python3
"""Falsifier suite for the Mathematics semantic math-expression typesetting layer.

Every test below is a *negative* test in the repository's established style: a
correct artifact is mutated in exactly one way and must fail by an exact named
gate. A test that only asserts a happy path would not have caught the PR #323
defect, because the flattened product was structurally green.
"""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

PHASE = Path(__file__).resolve().parents[1]
MATH = PHASE.parent
sys.path.insert(0, str(PHASE / "engine"))

from math_expression import (  # noqa: E402
    FontBinding,
    GlyphRegistry,
    Typesetter,
    aligned,
    audit_expressions,
    call,
    chain,
    detect_flattening,
    expression_signature,
    frac,
    group,
    load,
    num,
    op,
    power,
    radical,
    rel,
    seq,
    setrel,
    sub,
    sym,
    txt,
    typeset_unicode,
)

REG = GlyphRegistry()
SCHEMA = json.loads((PHASE / "contracts" / "math-expression.schema.json").read_text(encoding="utf-8"))
POLICY = load(PHASE / "policies" / "math-typesetting-policy.json")


def corpus() -> dict[str, dict]:
    """Real learner mathematics drawn from two stress-tested topics.

    These are data instances of the subject-wide AST; nothing here is a
    topic-specific schema shape.
    """
    return {
        # Number Systems - surd simplification (the exact PR #323 defect)
        "NUMBER_SYSTEMS/simplify-surd": aligned(
            (radical(num(72)), "EQ", radical(seq(num(36), op("TIMES"), num(2)))),
            (radical(num(72)), "EQ", seq(radical(num(36)), op("TIMES"), radical(num(2)))),
            (radical(num(72)), "EQ", seq(num(6), radical(num(2)))),
        ),
        # Number Systems - rationalising a denominator
        "NUMBER_SYSTEMS/rationalise": chain(
            (frac(num(1), seq(radical(num(7)), op("MINUS"), num(2))), "start from the given surd"),
            (seq(frac(num(1), seq(radical(num(7)), op("MINUS"), num(2))), op("TIMES"),
                 frac(seq(radical(num(7)), op("PLUS"), num(2)),
                      seq(radical(num(7)), op("PLUS"), num(2)))),
             "multiply by the conjugate written as 1"),
            (frac(seq(radical(num(7)), op("PLUS"), num(2)), num(3)),
             "the denominator becomes 7 − 4 by difference of squares"),
        ),
        # Number Systems - the nested number-set inclusion
        "NUMBER_SYSTEMS/number-sets": setrel(
            "SUBSET", sym("NATURALS"), sym("WHOLES"), sym("INTEGERS"),
            sym("RATIONALS"), sym("REALS"),
        ),
        # Polynomials - factor theorem, real substitution
        "POLYNOMIALS/factor-theorem": aligned(
            (call("p", sym("x")), "EQ",
             seq(power(sym("x"), num(3)), op("MINUS"), num(2), power(sym("x"), num(2)),
                 op("MINUS"), sym("x"), op("PLUS"), num(2))),
            (call("p", num(2)), "EQ",
             seq(power(num(2), num(3)), op("MINUS"), num(2), power(num(2), num(2)),
                 op("MINUS"), num(2), op("PLUS"), num(2))),
            (call("p", num(2)), "EQ", num(0), "so (x − 2) is a factor"),
        ),
        # Polynomials - binomial square, subscript identity
        "POLYNOMIALS/binomial-square": aligned(
            (power(group(seq(sym("x"), op("MINUS"), sym("a"))), num(2)), "EQ",
             seq(power(sym("x"), num(2)), op("MINUS"), num(2), sym("a"), sym("x"),
                 op("PLUS"), power(sym("a"), num(2)))),
            (sub(sym("x"), num(1)), "EQ", seq(sym("a"), op("PLUS"), radical(num(3)))),
        ),
    }


class TypesetPositive(unittest.TestCase):
    def test_every_expression_validates_against_the_ast_contract(self):
        validator = Draft202012Validator(SCHEMA)
        for location, node in corpus().items():
            with self.subTest(location=location):
                validator.validate(node)

    def test_the_pr323_defect_is_gone(self):
        rendered = typeset_unicode(corpus()["NUMBER_SYSTEMS/simplify-surd"], REG)
        self.assertIn("√72 = 6√2", rendered)
        self.assertNotIn("sqrt", rendered.lower())

    def test_scripts_are_real_code_points_not_carets(self):
        rendered = typeset_unicode(corpus()["POLYNOMIALS/binomial-square"], REG)
        self.assertIn("(x − a)²", rendered)
        self.assertIn("x₁", rendered)
        self.assertNotIn("^", rendered)
        self.assertNotIn("_1", rendered)

    def test_set_inclusion_uses_bound_set_glyphs(self):
        rendered = typeset_unicode(corpus()["NUMBER_SYSTEMS/number-sets"], REG)
        self.assertEqual(rendered, "ℕ ⊂ W ⊂ ℤ ⊂ ℚ ⊂ ℝ")

    def test_audit_passes_on_the_real_corpus(self):
        audit = audit_expressions(corpus())
        self.assertEqual(audit["status"], "PASS")
        self.assertNotIn(audit["font_family"], REG.data["font_binding"]["forbidden_fallbacks"])
        for kind in ("RADICAL", "POWER", "SUBSCRIPT", "FRACTION", "SET_NOTATION",
                     "ALIGNED_EQUATION", "TRANSFORMATION_CHAIN"):
            self.assertIn(kind, audit["structural_nodes_exercised"], kind)

    def test_audit_is_deterministic(self):
        self.assertEqual(audit_expressions(corpus())["corpus_digest"],
                         audit_expressions(corpus())["corpus_digest"])

    def test_bound_font_covers_the_entire_declared_glyph_registry(self):
        declared = "".join([
            "".join(REG.operators.values()),
            "".join(REG.relations.values()),
            "".join(REG.set_relations.values()),
            "".join(REG.named_symbols.values()),
            "".join(REG.superscripts.values()),
            "".join(REG.subscripts.values()),
            REG.radical_sign,
            "".join(a + b for a, b in REG.fences.values()),
        ])
        font = REG.bind_font(declared)
        self.assertEqual(font.supports(declared), [])

    def test_measured_boxes_compose(self):
        font = REG.bind_font("√ ² ₁ × − ⊂")
        typesetter = Typesetter(font, REG, POLICY)
        plain = typesetter.measure(num(72), 11.0)
        rooted = typesetter.measure(radical(num(72)), 11.0)
        # a radical is wider and taller than its own radicand: the overbar is real
        self.assertGreater(rooted.width, plain.width)
        self.assertGreater(rooted.ascent, plain.ascent)
        fraction = typesetter.measure(frac(num(1), num(3)), 11.0)
        self.assertGreater(fraction.height, plain.height)

    def test_drawing_the_corpus_emits_real_glyphs_into_a_pdf(self):
        """The rendered page, not the backing JSON, is the release surface.

        Note on the superscript assertions: a genuinely typeset script is drawn as a
        smaller glyph on a *raised baseline*, so PDF text extraction concatenates it
        as ``x2`` rather than ``x²``. The rendered-page evidence for a real script is
        therefore geometric (a smaller span at a higher origin), not textual. What the
        extracted text must still prove is that no ASCII flattening survived.
        """
        from reportlab.pdfgen import canvas as rl_canvas

        font = REG.bind_font("√ ² ₁ × − ⊂ ℕ")
        typesetter = Typesetter(font, REG, POLICY)
        out = Path("/tmp/math-typesetting-smoke.pdf")
        c = rl_canvas.Canvas(str(out))
        y = 760.0
        for node in corpus().values():
            box = typesetter.measure(node, 11.0)
            box.draw(c, 48.0, y - box.ascent)
            y -= box.height + 26.0
        c.showPage()
        c.save()
        self.assertGreater(len(out.read_bytes()), 1000)
        try:
            import fitz  # type: ignore
        except ImportError:  # pragma: no cover - CI installs pymupdf
            return
        document = fitz.open(out)
        page_text = "\n".join(p.get_text() for p in document)
        self.assertIn("√72 = 6√2", page_text)
        self.assertIn("ℕ ⊂ W ⊂ ℤ ⊂ ℚ ⊂ ℝ", page_text)
        self.assertNotIn("sqrt", page_text.lower())
        self.assertNotIn("^", page_text)
        self.assertNotIn("<=", page_text)
        self.assertEqual(detect_flattening(page_text), [])

        # geometric proof that scripts are typeset and not baseline text
        spans = [s for block in document[0].get_text("dict")["blocks"]
                 for line in block.get("lines", []) for s in line.get("spans", [])]
        body = max(s["size"] for s in spans)
        raised = [s for s in spans if s["size"] < body * 0.95]
        self.assertTrue(raised, "no reduced-size span: scripts were not typeset")
        self.assertTrue(any(abs(s["size"] - body * 0.68) < 0.6 for s in raised),
                        "no span at the declared script size ratio")


class TypesetFalsifiers(unittest.TestCase):
    """One mutation per test; each must fail by its exact named gate."""

    def expect(self, code: str, fn):
        with self.assertRaises(ValueError) as ctx:
            fn()
        self.assertIn(code, str(ctx.exception), f"expected {code}, got {ctx.exception}")

    # 1
    def test_MATH_EXPRESSION_FLATTENED_TO_PLAIN_TEXT(self):
        self.expect("MATH_TYPESETTING_GATE_FAILED",
                    lambda: audit_expressions({"x": txt("sqrt(72) = 6sqrt(2)")}))
        self.assertTrue(any(c.startswith("MATH_EXPRESSION_FLATTENED_TO_PLAIN_TEXT")
                            for c in detect_flattening("sqrt(72)")))

    # 2
    def test_MATH_EXPRESSION_FLATTENED_caret_power(self):
        codes = detect_flattening("(x-a)^2 + x^3")
        self.assertIn("MATH_EXPRESSION_FLATTENED_TO_PLAIN_TEXT:caret_power", codes)

    # 3
    def test_MATH_EXPRESSION_FLATTENED_underscore_subscript(self):
        codes = detect_flattening("x_1 and x_2 are the roots")
        self.assertIn("MATH_EXPRESSION_FLATTENED_TO_PLAIN_TEXT:underscore_subscript", codes)

    # 4
    def test_MATH_RELATION_RENDERED_AS_ASCII_FALLBACK(self):
        for ascii_relation in ("x <= 3", "x >= 3", "x != 3", "x ~= 3", "p => q"):
            codes = detect_flattening(ascii_relation)
            self.assertTrue(any(c.startswith("MATH_RELATION_RENDERED_AS_ASCII_FALLBACK")
                                for c in codes), ascii_relation)

    # 5
    def test_MATH_FONT_NOT_BOUND(self):
        broken = copy.deepcopy(REG.data)
        for candidate in broken["font_binding"]["candidates"]:
            candidate["regular"] = "/nonexistent/NoSuchFont.ttf"
            candidate["bold"] = "/nonexistent/NoSuchFont-Bold.ttf"
        self.expect("MATH_FONT_NOT_BOUND", lambda: GlyphRegistry(broken).bind_font("√"))

    # 6
    def test_MATH_FONT_NOT_BOUND_when_base14_fallback_is_declared(self):
        reg = GlyphRegistry()
        base14 = FontBinding("Helvetica", "Helvetica", "Helvetica-Bold", "", "")
        self.expect("MATH_TYPESETTING_GATE_FAILED",
                    lambda: audit_expressions({"x": radical(num(72))}, font=base14, reg=reg))

    # 7
    def test_MATH_REQUIRED_GLYPH_MISSING(self):
        reg = GlyphRegistry()
        self.expect("MATH_REQUIRED_GLYPH_MISSING", lambda: reg.relation("NOT_A_RELATION"))
        self.expect("MATH_REQUIRED_GLYPH_MISSING", lambda: reg.operator("NOT_AN_OPERATOR"))
        self.expect("MATH_REQUIRED_GLYPH_MISSING", lambda: reg.set_relation("NOT_A_SET_RELATION"))

    # 8
    def test_MATH_SCRIPT_NOT_TYPESET_when_no_script_code_point_exists(self):
        # 'k' has no Unicode superscript form; the layer must refuse rather than
        # silently emit a baseline 'k'.
        self.expect("MATH_SCRIPT_NOT_TYPESET",
                    lambda: typeset_unicode(power(sym("x"), sym("k")), REG))

    # 9
    def test_MATH_SCRIPT_NOT_TYPESET_when_script_would_be_unreadably_small(self):
        font = REG.bind_font("x²")
        tiny_policy = copy.deepcopy(POLICY)
        tiny_policy["font_policy"]["min_absolute_script_pt"] = 24.0
        typesetter = Typesetter(font, REG, tiny_policy)
        self.expect("MATH_SCRIPT_NOT_TYPESET",
                    lambda: typesetter.measure(power(sym("x"), num(2)), 11.0))

    # 10
    def test_MATH_SEMANTIC_AST_RENDER_MISMATCH_on_unknown_node(self):
        self.expect("MATH_SEMANTIC_AST_RENDER_MISMATCH",
                    lambda: typeset_unicode({"node": "NOT_A_NODE"}, REG))

    # 11
    def test_MATH_SEMANTIC_AST_RENDER_MISMATCH_when_a_radical_is_dropped(self):
        """A renderer that erases the radical sign no longer carries the AST anchors."""
        node = radical(num(72))
        anchors = expression_signature(node)
        self.assertIn("√", anchors)
        flattened = typeset_unicode(node, REG).replace("√", "")
        self.assertFalse(all(a in flattened for a in anchors if a.strip()))

    # 12
    def test_MATH_TRANSFORMATION_ALIGNMENT_LOST(self):
        single_line = {"node": "ALIGNED_EQUATION", "lines": [
            {"lhs": num(1), "relation": rel("EQ"), "rhs": num(1), "annotation": None},
        ]}
        self.expect("MATH_TYPESETTING_GATE_FAILED",
                    lambda: audit_expressions({"x": single_line}))

    # 13
    def test_ast_contract_rejects_a_power_without_an_exponent(self):
        validator = Draft202012Validator(SCHEMA)
        with self.assertRaises(Exception):
            validator.validate({"node": "POWER", "base": num(2)})

    # 14
    def test_ast_contract_rejects_a_radical_carrying_a_stray_string(self):
        validator = Draft202012Validator(SCHEMA)
        with self.assertRaises(Exception):
            validator.validate({"node": "RADICAL", "radicand": num(2), "text": "sqrt(2)"})

    # 15
    def test_policy_declares_every_falsifier_the_engine_can_raise(self):
        from math_expression import FALSIFIERS
        self.assertEqual(sorted(POLICY["falsifiers"]), sorted(FALSIFIERS))


if __name__ == "__main__":
    unittest.main(verbosity=2)
