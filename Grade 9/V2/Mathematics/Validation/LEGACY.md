# Two lineages live under `Validation/`

## `Validation/MatureGate/` — LIVE (M-L)

This is the Mathematics M-L release gate (#247, #313, #319). It is the only
authority that may classify a candidate `V2_MATURE_INSTRUCTIONAL_PRODUCT`, and
it fails closed on every missing or failing review. It consumes the M-K
cold-start report and the rendered two-product package from
`Publication/engine/realize_math_core_products.py`.

## Everything else under `Validation/` — LEGACY / REFERENCE ONLY

The top-level `Validation/` contracts, engine and fixtures belong to the
**MATH-V2-07** lineage (issue #214, PR #202 and predecessors). They validate the
candidate produced by the abandoned `LearningDesign` → old-`Publication` path.

* Retained for reference: `REFERENCE_POLICY.md` states the
  final-comparative-validation-only rule that M-L's
  `raw_reference_runtime_policy` re-implements.
* **Do not** extend them, and do not treat their results as M-L release
  evidence.

Tracking: #319.
