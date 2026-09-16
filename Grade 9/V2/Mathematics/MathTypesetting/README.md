# Mathematics V2 — MathTypesetting (M-UPGRADE-2 item 1)

This phase removes the **root cause** identified by the PR #323 RCA: learner-visible
mathematics reached the renderer as an opaque string and was then flattened by an
`ascii_safe()` substitution table, so

```text
√72 = 6√2        (the mathematics)
sqrt(72)=6sqrt(2)   (what the learner actually received)
```

Layout cannot recover structure that was destroyed upstream. So mathematics now enters
publication as a **semantic AST**, and the renderer *typesets* it.

```text
MathExpression AST                (contracts/math-expression.schema.json)
        |
        +--> typeset_unicode()    audit / accessibility string, exact bound glyphs
        +--> Typesetter.measure() measured box tree (real rules, real overbars, real scripts)
        `--> audit_expressions()  fail-closed falsifier set
```

## The AST is subject-wide generic

Number Systems, Polynomials, Coordinate Geometry, Linear Equations, Euclid's Geometry,
Lines & Angles and Surface Areas & Volumes are **data instances** of one node vocabulary.
No node kind is topic specific:

```text
NUMBER  SYMBOL  TEXT  OPERATOR  RELATION  GROUP  SEQUENCE
FRACTION  RADICAL  POWER  SUBSCRIPT  SUPERSCRIPT
FUNCTION_CALL  SET_NOTATION  ALIGNED_EQUATION  TRANSFORMATION_CHAIN
```

These are semantically distinct objects and stay distinct through publication:

| Mathematics | AST |
| --- | --- |
| `(x − a)²` | `POWER(GROUP(SEQUENCE(x, MINUS, a)), 2)` |
| `x₁` | `SUBSCRIPT(x, 1)` |
| `p(a)` | `FUNCTION_CALL("p", a)` |
| `1⁄(√7 − 2)` | `FRACTION(1, SEQUENCE(RADICAL(7), MINUS, 2))` |
| `ℕ ⊂ W ⊂ ℤ ⊂ ℚ ⊂ ℝ` | `SET_NOTATION(SUBSET, …)` |

## Two render targets, one AST

`typeset_unicode()` is the **audit and accessibility** surface. It emits the exact code
points bound in `registry/math-glyph-binding-registry.json` — real `√`, real `²`, real
`₁`, real `≤`, real `⊂` — never an ASCII approximation.

`Typesetter.measure()` is the **drawn** surface. It returns a measured `Box`
(`width`/`ascent`/`descent` plus a draw closure), so composition is measure-then-draw
rather than fixed-rectangle guesswork:

- a `FRACTION` gets a real rule on the math axis with a centred numerator/denominator;
- a `RADICAL` gets a real overbar spanning its radicand, and an optional raised index;
- a `POWER`/`SUBSCRIPT` is drawn at a reduced size on a shifted baseline, refusing to
  render at all if that size would fall below the readable minimum;
- an `ALIGNED_EQUATION` is aligned on its relation column;
- a `TRANSFORMATION_CHAIN` keeps one justification per line beside its expression.

## Font binding is portable and measured, not assumed

`GlyphRegistry.bind_font()` walks the candidate list (DejaVu → FreeSerif → Noto), checks
the file exists **and** that its `cmap` maps every code point the expression corpus needs,
and fails `MATH_FONT_NOT_BOUND` rather than degrading. The ReportLab base-14 families are
listed as forbidden fallbacks because they are Latin-1 and silently drop every glyph in
the registry — which is exactly how PR #323's product lost its mathematics.

`WHOLES` deliberately binds to the NCERT-conventional `W`. Blackboard-bold `𝕎` (U+1D54E)
*is* present in the bound font, but it lies outside the BMP where PDF text extraction does
not round-trip reliably; a glyph that cannot be read back cannot be gated after rendering,
so it is not the default binding. The decision is recorded in the registry itself.

## Falsifiers

```text
MATH_EXPRESSION_FLATTENED_TO_PLAIN_TEXT      sqrt(, cbrt, x^2, x_1, +/-, " deg"
MATH_FONT_NOT_BOUND                          no portable math-capable font resolved
MATH_RELATION_RENDERED_AS_ASCII_FALLBACK     <=, >=, !=, ~=, =>, ->
MATH_SCRIPT_NOT_TYPESET                      script has no code point, or is unreadably small
MATH_REQUIRED_GLYPH_MISSING                  bound font cannot map a required code point
MATH_SEMANTIC_AST_RENDER_MISMATCH            AST structural anchors do not survive the render
MATH_TRANSFORMATION_ALIGNMENT_LOST           multi-line transformation lost its alignment column
MATH_TYPESETTING_GATE_FAILED                 aggregate fail-closed gate
```

`detect_flattening()` is reusable on **already-rendered** text, so the same vocabulary
gates pre-render JSON and post-render PDF pages.

## Tests

`tests/test_math_expression_typesetting.py` is falsifier-driven: one mutation per test,
each failing by an exact named gate. It also renders the real two-topic corpus
(Number Systems surds/rationalisation/number-sets, Polynomials factor theorem/binomial
square) to a PDF and inspects the page.

One measurement note that matters for every downstream post-render gate: a genuinely
typeset script is a smaller glyph on a **raised baseline**, so PDF text extraction returns
`x2`, not `x²`. Rendered-page evidence for a real script is therefore *geometric* (a
reduced-size span at the declared ratio), while the extracted text is what proves no ASCII
flattening survived. Downstream phases reuse both checks.

## Release meaning

Passing these gates is `PUBLICATION_ENGINEERING` evidence only. Subject, pedagogy,
assessment, visual-usability and expert review all remain `PENDING`, and no PCK is
promoted beyond `PROVISIONAL_PROMOTED` by anything in this phase.
