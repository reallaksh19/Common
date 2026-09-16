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
repository-backed mapping review, where needed
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

A `MAPPED_V3` entry is different from direct migration. It requires a repository-backed mapping review that accounts for every source obligation against exact canonical v3 target blobs. A broad source gate may map into several refined canonical gates. An exact source identity and a broader reviewed mapping may legitimately converge on the same canonical target because those are independent source-provenance roles; this does not create a second readiness authority.

A reviewed mapping may also normalize an old broad source structure into an already-governed canonical decomposition. For example, the PR #383 projectile shortcut formulas are reconciled through canonical component displacement relations, the shared event clock and apex velocity evolution, rather than by creating a second shortcut-formula gate.

The PR #383 `PHY-GRAV-FREE-FALL` discovery follows that normalized-mapping pattern. Its universal-gravitation prerequisite is reconciled through the canonical force/field pair, while its old separate `PHY-KIN-1D-MOTION` prerequisite is accounted for by the governed vertical displacement and vertical-velocity relations plus named-event timing. The source `H_max` and same-level flight-time formulas are therefore not imported as duplicate formula authority: maximum height and total return time are reconstructed from the vertical displacement relation, vertical velocity evolution, the apex event and the return-to-level event. The source return-velocity symmetry is covered by the canonical same-height state relation.

The free-fall mapping is deliberately precise about time symmetry. The source statement that ascent time equals descent time is interpreted for the source-declared launch-to-apex and apex-to-return-to-release-level segments under the uniform-g/no-drag model. It does **not** override the canonical same-height representation guard that two same-height states generally need not have equal absolute timestamps.

The PR #383 `PHY-KIN-RELATIVE-2D` discovery is reconciled differently: its river-crossing semantics were not already fully present in the canonical registry, so a new generic source-defined gate, `PHY-M2D-RELATIVE-VELOCITY`, was created. The source's `PHY-KIN-1D-MOTION` prerequisite was not fabricated as a canonical gate. The actual contribution required by this source—`t = d / v_perpendicular` and `x = v_parallel * t`—is explicit in the pinned source model condition and reasoning sequence and is carried directly as typed canonical relations. The mapping review accounts for that prerequisite against those exact relations.

This generic relative-velocity gate has no SBA or question linkage. It is subject-level technical authority. The existing specialised `PHY-M2D-MOVING-LAUNCHER` gate remains separate; a future dependency between the two requires its own repository-backed review and exact closure-custody refresh rather than being inferred from topic similarity.

`v3_native_or_refined_gate_ids` remains exclusive: those gates have no source-backed reconciliation role and therefore may not also be exact or mapped targets.

## What may not be imported as authority

PR #383 fields `technical_readiness` and `release_checklist` are deliberately discarded as control inputs. Canonical v3 does not permit a gate source to self-assert readiness. Mapping reviews likewise fix `readiness_authorized = false` and `source_custody_promoted = false`.

A directly migrated gate remains blocked until the v3 control plane has explicit repository-backed evidence for at least:

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

The pinned PR #383 registry contains 43 discovered subtopics. The current canonical v3 registry contains **24 gates**. Discovery reconciliation currently contains:

- 12 `EXACT_V3_ID` source discoveries;
- 5 reviewed `MAPPED_V3` source discoveries: the broad Newton-laws bundle, universal-gravitation bundle, free-fall discovery, 2D-projectile bundle and 2D-relative-velocity discovery;
- 26 `MIGRATION_REQUIRED` source discoveries;
- 5 canonical v3-native/refined gates with no PR #383 source-backed reconciliation role.

The five canonical NLM targets of `PHY-FORCE-NEWTON-LAWS` are also exact PR #383 identities. That overlap is intentional and means the category counts are provenance-role counts, not a partition whose target counts can be added to derive the 24-gate registry size.

The three canonical M2D targets of `PHY-KIN-2D-PROJECTILE` were previously classified as native/refined. Once the repository-backed mapping review established full source-obligation coverage, they became source-backed mapping targets and were removed from the native/refined set.

`PHY-M2D-SAME-HEIGHT-VELOCITY` likewise moves from native/refined-only classification into a PR #383 source-backed mapping role through the free-fall review. This changes provenance classification, not its canonical gate semantics or readiness derivation.

`PHY-M2D-RELATIVE-VELOCITY` is a newly created canonical target backed by the reviewed PR #383 relative-motion source; it is therefore neither an exact-ID target nor a native/refined gate.

The migration-gap compiler therefore reports **17 reconciled PR #383 discovery entries** and the remaining **26 unresolved discoveries** as:

`BLOCKED_PENDING_V3_ENRICHMENT`

with `promotion_authorized = false`.

The source-only structural preflight also remains fail closed: none of those 26 unresolved source gates independently satisfies all canonical v3 collection minimums, and structural preflight can never grant engineering readiness.

## Q15 boundary

Q15 is a stress fixture only. It is not source truth for this migration layer, it is not a gate-definition input, and no Q15/SBA23 branch exists in the migration compiler. The test suite asserts that Q15 does not appear in the subject-wide migration report or mapping-review authority.
