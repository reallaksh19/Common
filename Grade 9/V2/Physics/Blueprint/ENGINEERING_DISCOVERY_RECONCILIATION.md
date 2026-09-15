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

The catalog may never self-assert `ENGINEERING_GATE_READY`, source legality, pedagogy, learner mastery, transfer legality, or publication authority.

## Global rule

Every PR #383 discovery entry must have an explicit reconciliation disposition. An exact ID must actually exist in the live v3 registry. A reviewed rename/split/merge may use `MAPPED_V3` only with review provenance. Anything else remains `MIGRATION_REQUIRED` and cannot silently become technical authority.

Conversely, every live v3 gate must be reconciled as an exact discovery match, a reviewed mapping target, or a v3-native/refined gate. This prevents both PR #383 breadth and PR #350 refinements from disappearing silently.

## Case isolation

Question IDs, SBA buckets and other case artifacts are stress-test inputs only. They cannot define subject-wide engineering logic or promote source custody. Q15/SBA23 may falsify or exercise the global machinery, but they are not ground truth for the engineering registry and are not a basis for Blueprint branching.

## Normative files

- `contracts/physics-engineering-discovery-catalog.schema.json`
- `policy/physics-engineering-discovery-catalog.pr383.v1.json`
- `engine/validate_engineering_discovery_catalog.py`
- `tests/test_physics_engineering_discovery_catalog.py`
