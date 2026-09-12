# LEGACY — QUARANTINED. Do not wire new work to this directory.

`Grade 9/V2/Physics/Publication/` (`build_semantic_product.py`,
`realize_physics_publication.py`) belongs to the **pre-assessment-gate** Physics chain
built under issues #221–#233. That chain predates P-A/P-B/P-C, so it has no
assessment-intake, item-validity or scope-reconciliation authority above it.

It is kept for repository history and reference only.

## Why it must not be reused

This renderer consumes a plan shape produced before the P-C `PhysicsAssessmentScope`
authority existed. Wiring it into the P-A → P-J chain would reintroduce exactly the defect
issue #320 exists to close: a Physics PDF whose content is not traceable to a reviewed,
scope-reconciled assessment.

PR #276's own description already records this directory as "repository context only".

## What to use instead

| need | use |
|---|---|
| teaching primitives and figures | `../Representation/engine/physics_primitive_renderer.py` |
| physical page custody | `../Representation/engine/physics_page_custody.py` |
| representation realization proof | `../Representation/engine/realize_physics_representations.py` |
| learner product rendering | `../ColdStart/engine/physics_product_renderer.py` |
| running the whole chain | `../ColdStart/engine/physics_cold_start_runner.py` |

## How the quarantine is enforced

`../GENERATION_AUTHORITY_MANIFEST.json` does not declare any file in this directory, and
the P-K validator rejects any runtime read outside the manifest with
`RUNTIME_READ_OUTSIDE_AUTHORITY_MANIFEST`. A future contributor who wires this engine into
the chain will fail the P-K cold-start audit rather than silently ship.
