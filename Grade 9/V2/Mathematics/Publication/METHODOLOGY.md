# MATH-V2-05 Methodology

## 1. Generate semantics from the merged design

The end-to-end workflow first runs the merged MATH-V2-04 design engine. `build_semantic_product.py` consumes that exact result and refuses missing required step IDs. Learner-facing semantic items therefore retain explicit `learning_design_refs` rather than becoming a second teaching authority.

## 2. Freeze learner-facing semantic content before layout

`LearnerSemanticProduct` contains the material learner jobs and explanatory payload. Publication may group/place these items but may not rewrite them during rendering.

## 3. Preserve meaningful support differences

Guided, faded and independent workspaces have materially different support payloads. The independent workspace contains no conceptual hint or preselected operation.

## 4. Probe before explanation

The ordered-pair/slope item is a diagnostic probe. No slope explanation/reteach material is allowed before it in the semantic sequence.

## 5. Actual physical evidence comes from drawing

The renderer records each content placement at the same moment it draws the corresponding panel. A planned page assignment cannot substitute for `actual_placement_evidence=true`.

## 6. Render -> verify

CI renders `candidate.pdf` to PNG pages and checks that every expected page produces a non-empty raster. This is engineering preflight only; it is not visual-usability approval.

## 7. Seal exact bytes after rendering

The exact PDF SHA256 is bound into PhysicalPageMap, audit, manifest and result. The package digest is computed from artifact descriptors and excludes itself.
