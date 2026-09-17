# Physics Engineering Discovery Reconciliation

## Purpose

PR #383 is consumed as a **subject-wide discovery and coverage input**, not as a readiness authority. The canonical technical control plane remains the Physics v3 Workbench on PR #350.

```text
PR #383 discovery breadth
  43 Grade 9-11 subtopic identities + curriculum/JEE metadata
        ↓
DISCOVERY RECONCILIATION CATALOG
  EXACT_V3_ID | MAPPED_V3 | MIGRATION_REQUIRED
        ↓
REPOSITORY-BACKED MAPPING REVIEW, where MAPPED_V3
        ↓
CANONICAL v3 ENGINEERING GATE SOURCES
        ×
EXTERNAL INVARIANT PROFILE
        ×
PRODUCTION v3 VALIDATOR
        ↓
DERIVED ENGINEERING READINESS
        ↓
Blueprint downstream gates
```

The catalog or a mapping review may never self-assert `ENGINEERING_GATE_READY`, source legality, pedagogy, learner mastery, transfer legality, or publication authority.

## Global rule

Every PR #383 discovery entry must have an explicit reconciliation disposition. An exact ID must actually exist in the live v3 registry. A reviewed rename, split, merge or broader-to-refined decomposition may use `MAPPED_V3` only with repository-backed review provenance that covers every source obligation against exact canonical target blobs. Anything else remains `MIGRATION_REQUIRED` and cannot silently become technical authority.

Conversely, every live v3 gate must be reconciled as an exact discovery match, a reviewed mapping target, or a v3-native/refined gate. This prevents both PR #383 breadth and PR #350 refinements from disappearing silently.

### Provenance-role overlap

`EXACT_V3_ID` and `MAPPED_V3` describe **source provenance roles**, not mutually exclusive ownership classes for the canonical target. A canonical v3 gate may therefore be both:

- an exact match for one PR #383 discovery identity; and
- a target of another, broader PR #383 discovery that has been independently reviewed and decomposed across refined canonical gates.

This occurs, for example, when a broad curriculum bundle is reconciled into finer canonical engineering gates that also exist as exact source identities. The overlap does not duplicate readiness authority: the canonical gate source, external invariant profile and production v3 validator remain the only technical-readiness control plane.

`v3_native_or_refined_gate_ids` is different. It denotes canonical gates with no source-backed reconciliation role in the catalog, so it must remain disjoint from both exact and mapped target sets.

### Normalization during reviewed mapping

A reviewed mapping may preserve a broad source obligation through a **decomposition already explicit in canonical v3**, rather than by copying the old source structure verbatim. For example, a source shortcut equation may be represented by canonical component relations plus an event constraint, or an old broad prerequisite may be absorbed into governed canonical relations instead of retained as a nonexistent prerequisite ID.

That normalization is allowed only when the review points to exact repository-backed target objects that collectively preserve the source obligation. It may not invent a missing relation, prerequisite, representation, or Physics claim. If the canonical target set cannot account for an obligation, the review must remain blocked and the discovery remains `MIGRATION_REQUIRED`.

A mapping review itself grants neither engineering readiness nor source custody. Its decision is limited to technical discovery reconciliation, and the validator fixes `readiness_authorized = false` and `source_custody_promoted = false`.

## Case isolation

Question IDs, SBA buckets and other case artifacts are stress-test inputs only. They cannot define subject-wide engineering logic or promote source custody. Q15/SBA23 may falsify or exercise the global machinery, but they are not ground truth for the engineering registry and are not a basis for Blueprint branching.

## Normative files

- `contracts/physics-engineering-discovery-catalog.schema.json`
- `contracts/physics-engineering-discovery-mapping-review.schema.json`
- `policy/physics-engineering-discovery-catalog.pr383.v1.json`
- `provenance/pr383/mapping-reviews/*.json`
- `engine/validate_engineering_discovery_catalog.py`
- `engine/validate_engineering_mapping_review.py`
- `tests/test_physics_engineering_discovery_catalog.py`
- `tests/test_physics_engineering_mapping_reviews.py`
