# Primary Math V2 Release Boundary

## 1. Three acceptance states

Every candidate tracks independently:

```text
semantic_status
artifact_status
human_review_status
```

No single green status may stand in for the others.

## 2. Machine / engineering gates

Examples:

```text
CONTRACT_VALIDITY
SCOPE_PROVENANCE
WORK_EVIDENCE_PROVENANCE
CONCEPT_GRAPH_VALIDITY
LEARNING_DESIGN_VALIDITY
VISUAL_SEMANTIC_VALIDITY
PRIMITIVE_REALIZATION
CORE1_CORE2_LINK_VALIDITY
LAYOUT_BOUNDS
PHYSICAL_PAGE_CUSTODY
LEARNER_SURFACE_GUARD
ARTIFACT_HASH_BINDING
DETERMINISTIC_CANONICAL_REBUILD
INDEPENDENT_BENCHMARK_ORACLE
```

## 3. Human gates

Required exact-artifact review states:

```text
SUBJECT_CORRECTNESS
PEDAGOGICAL_DESIGN
ASSESSMENT_DESIGN
VISUAL_USABILITY
CHILD_USABILITY
MATURE_DESIGN_QUALITY
```

An AI pre-review may be recorded separately but may not be labelled as an authorized human pass.

## 4. Evidence classes

Candidate evidence must distinguish:

```text
TEST_FIXTURE
REAL_CANDIDATE
```

Synthetic positive fixtures may validate the oracle but can never be promoted into production release evidence.

## 5. Exact artifact custody

Canonical CI should bind:

```text
Core1 PDF SHA256
Core2 PDF SHA256
PhysicalPageMap digest(s)
semantic-plan digest(s)
representation-plan digest
registry/version digest
validation-report digest(s)
neutral candidate-export digest
```

## 6. Determinism

Require byte determinism in one pinned canonical build environment.

Cross-platform builds should satisfy semantic/layout/visual-equivalence expectations but are not required to be byte-identical across different PDF/font stacks.

## 7. Release honesty

Forbidden claims while required gates are pending/failing:

```text
MATURE
RELEASE_READY
PEDAGOGICALLY_VALIDATED
CHILD_VALIDATED
REFERENCE_QUALITY
```

## 8. Benchmark independence

#324 produces a neutral candidate export.

#325 independently recomputes benchmark assertions and does not trust producer-emitted `PASS` values.

#324 may not modify benchmark expectations inside the same renderer fix merely to make a candidate pass.

## 9. Page-image review

Per #182, child-facing review is based on rendered page images/exact artifacts, not source code or extracted text alone.

## 10. Stop conditions

A candidate is blocked if any applicable condition holds:

```text
scope provenance unresolved in a material way
required semantic validation fails
required representation is label-only / unrealized
learner work provenance is fabricated or collapsed
Core1/Core2 semantic links are broken
content is outside page bounds
learner-facing internal IDs leak
artifact hashes do not bind exact candidate
independent benchmark fails
required human gate is FAIL/BLOCKED for a release claim
```
