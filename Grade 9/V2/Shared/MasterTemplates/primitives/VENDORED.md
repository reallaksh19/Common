# Vendored shared visual primitives

This package is a **read-only vendored copy** of
`Grade 9/V2/Shared/MasterTemplates/primitives/` taken from PR #310
(`v2/grade9-master-templates-intake-tasks`) at commit `88d3a719`.

PR #310 is marked DO NOT MERGE because it also bundles large binary
TASK-input/output files. The primitives package itself is the piece the subject
renderers need, so it is vendored here at the same shared path. Physics and
Chemistry upgrade PRs vendor the identical subtree, so the copies are byte-equal
and will not conflict when #310's own package lands.

## Rules

* **Do not edit these files in a subject PR.** Fix bugs upstream in #310.
* Subject-specific adaptation belongs in the subject's adapter, e.g.
  `Grade 9/V2/Mathematics/Publication/engine/math_primitive_adapter.py`.
* When #310 (or its successor) lands on main, delete this note and rely on the
  published package; the only subject-side change needed is the
  `_LIBRARY_BINDINGS` table in each adapter.

## Known upstream issues observed while integrating (for #310, not fixed here)

1. `base.py` registers TrueType fonts from Windows-only paths
   (`C:\Windows\Fonts\...`). On Linux it falls back to Helvetica, so output is
   correct but the registration loop is dead code there, and any non-Latin-1
   glyph must be transliterated by the caller.
2. `diagrams.CombinatorialSlotDiagram.draw_slots` prints a hardcoded footer
   (`"Total Combinations = 5 * 4 * 3 * 1 = 60 valid outcomes"`) regardless of the
   `slots` argument. Callers cannot parameterize it, so the footer can contradict
   the data actually drawn.
3. `graphs.CartesianPlotter2D.plot_slope_triangle` places the rise label at
   `corner_x + 4`, which can collide with the y-axis when the triangle's vertical
   leg sits near `x = 0`.
4. `diagrams.PlaneGeometryRenderer.draw_parallel_transversal` has no parameter
   for the second interior angle, so only one angle can be driven by real data.
5. `validator.VisualSemanticValidator.validate` has no gate for coordinate-plane
   or algebraic-derivation primitives; its dispatch returns `True` for them.
   Mathematics therefore adds its own `assert_grounded` gate in the adapter.
