# Vendored shared visual-primitives package

This directory is a **vendored, read-only copy** of the shared Grade 9 visual-primitives
package developed in draft PR #310 (`v2/grade9-master-templates-intake-tasks`), taken at
commit `88d3a719`.

PR #310 itself is marked DO NOT MERGE (it bundles large binary TASK input/output files).
The Mathematics, Chemistry and Physics V2 upgrade branches each vendor this same subtree
from the same commit, at this same shared path, so the copies converge rather than conflict.

## Rules for this directory

- **Do not modify these files inside a subject upgrade PR.** Fix bugs and gaps upstream in
  PR #310 and re-vendor.
- Subject phases import it as a normal package:

  ```python
  import sys
  sys.path.insert(0, "<repo>/Grade 9/V2/Shared/MasterTemplates")
  from primitives import Vector1DDiagram, KinematicGraphRenderer, VisualSemanticValidator
  ```

- Subject-specific adaptation belongs in the subject's own renderer adapter, not here.
  Physics P-H wraps this package behind the stable interface
  `render_primitive(kind, params, canvas, bbox)` in
  `Grade 9/V2/Physics/Representation/engine/physics_primitive_renderer.py`.

## Contents

| module | exports |
|---|---|
| `base.py` | `FONT_NAME`, `FONT_BOLD`, `FONT_OBLIQUE`, `Palette`, `draw_card_box`, `draw_pill_badge`, `draw_arrow` |
| `graphs.py` | `CartesianPlotter2D`, `KinematicGraphRenderer`, `StatisticalPlotter`, `ThermalCurvePlotter` |
| `diagrams.py` | `PlaneGeometryRenderer`, `Vector1DDiagram`, `FreeBodyDiagramRenderer`, `WaveformRenderer`, `BohrAtomRenderer`, `ParticleLatticeDiagram`, `OxidationLaneDiagram`, `CombinatorialSlotDiagram` |
| `equations.py` | `FormulaAnatomyEngine`, `ValencyCrissCrossEngine`, `ChemicalReactionEngine`, `GeometryProofBlock`, `MathEquationBlock` |
| `validator.py` | `VisualSemanticValidator` plus 10 typed fail-closed exceptions |

## Known gaps observed while vendoring (report upstream to #310, do not patch here)

1. `KinematicGraphRenderer` exposes only `draw_vt_graph`. There is no `draw_xt_graph` or
   `draw_at_graph`, although the module docstring advertises `s-t` and `a-t`. Physics P-H
   therefore composes x–t and a–t views directly from `CartesianPlotter2D`.
2. `Vector1DDiagram.draw` maps a leg endpoint through `tick_pos.get(value, axis_start)`, so a
   leg endpoint that is not an exact declared tick silently collapses to the axis origin
   instead of failing. Physics P-H pre-checks that every leg endpoint is a declared tick.
3. `FreeBodyDiagramRenderer.draw_fbd` hard-codes the block label `m = 5 kg` regardless of the
   `forces` argument, so the mass shown is not driven by caller data.
4. `CombinatorialSlotDiagram.draw_slots` hard-codes the total-combinations footer
   (`5 * 4 * 3 * 1 = 60`) irrespective of the `slots` argument.
5. `VisualSemanticValidator.validate` dispatches on substring matching of the primitive name,
   so a Physics primitive whose id contains `ATOM` or `CIRCLE` would be routed to a Chemistry
   or Geometry gate. Physics P-H calls the specific `validate_*` classmethods directly rather
   than the substring dispatcher.
6. `base.py` only attempts to register Windows-path TrueType fonts and otherwise falls back to
   the Helvetica Type1 core font, which is not Unicode-capable on Linux CI.
