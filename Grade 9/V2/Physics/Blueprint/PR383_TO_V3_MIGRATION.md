# PR #383 to canonical v3 migration

## Purpose

PR #383 is a repository-backed discovery and breadth input for Grade 9–11 Physics engineering gates. It is not the canonical technical-readiness control plane.

The canonical authority order is:

```text
PR #383 exact pinned source bytes
        ↓
source-schema validation
        ↓
discovery reconciliation
        ↓
v3 migration-gap compilation
        ↓
reviewed v3 gate source(s)
        ×
external v3 invariant profile
        ×
production v3 validator
        ↓
derived ENGINEERING_GATE_READY / blocked state
        ↓
Blueprint downstream gates
```

A case artifact, assessment item, SBA bucket, learner product, or stress fixture may exercise this machinery but may not define or modify the engineering-gate logic.

## Exact provenance custody

The PR #383 head used for migration is pinned at:

`e92481f6e03a8bb49a55f568b03cba7c12fb942a`

Exact repository blobs are retained under `provenance/pr383/`:

- `physics-technical-engineering-gates.v1.json` — Git blob `89b009c31c79ad4b2009577220705d2711eadc4b`;
- `physics-technical-engineering-gate.schema.json` — Git blob `3aece88e05b22c550155515b8b43fdf8f4788f1f`;
- `source-snapshot.manifest.json` — binds the original PR, commit and blob identities.

`compile_pr383_v3_migration_gaps.py` recomputes Git blob identities before reading the snapshot. Any byte drift fails closed.

## What may be preserved

For a gate still marked `MIGRATION_REQUIRED`, the compiler may preserve source-backed discovery material such as identity, title, curriculum/JEE metadata, provenance, prerequisites, concepts, equation text, representations, model-condition statements, reasoning steps, transformations, misconceptions, verification statements, problem-family descriptions, engineering difficulty and falsification descriptions.

Preservation does **not** mean v3 readiness.

## What may not be imported as authority

PR #383 fields `technical_readiness` and `release_checklist` are deliberately discarded as control inputs. Canonical v3 does not permit a gate source to self-assert readiness.

A migrated gate remains blocked until the v3 control plane has explicit repository-backed evidence for at least:

- reviewed `scope_state`;
- applicable Core roles;
- external required-invariant profile;
- typed relation-symbol semantics;
- model-condition relation bindings and failure model;
- representation semantic/binding/primitive requirements;
- dependency-aware reasoning bindings;
- stable transformation identities;
- misconception representation repair and verification;
- problem-family hidden invariants, capabilities and transfer dimensions;
- stable production-validator falsification failure codes.

These are enrichment obligations, not permission to infer missing Physics content. Missing semantics remain blocked until repository-backed authority supplies them.

## Current state

The pinned PR #383 registry contains 43 discovered subtopics. The current canonical v3 registry contains 23 gates. Discovery reconciliation currently recognizes 12 exact v3 identities and holds 31 PR #383 discoveries for explicit v3 migration. The current v3 registry also contains 11 native/refined gates that are not forced into PR #383 naming.

The migration-gap compiler therefore reports the 31 unresolved discoveries as:

`BLOCKED_PENDING_V3_ENRICHMENT`

with `promotion_authorized = false`.

## Q15 boundary

Q15 is a stress fixture only. It is not source truth for this migration layer, it is not a gate-definition input, and no Q15/SBA23 branch exists in the migration compiler. The test suite asserts that Q15 does not appear in the subject-wide migration report.
