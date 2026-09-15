# Mathematics V2 — Instructional Knowledge (M-G)

Tracking: #242 under Mathematics catch-up roadmap #235; promotion mechanism per #319.

This authority owns the **Mathematics PCK lifecycle**, not learner treatment and not page rendering.

## Promotion pipeline

The promotion mechanism is generic over `capability_ref` / `problem_family_ref`. Topic
instances are data carried by the bound asset; there is no per-topic schema.

```text
PCK_CANDIDATE
  -> EVIDENCE_PROVENANCE_REVIEW      (AI_ASSISTED_REFERENCE_REVIEW)
  -> PEDAGOGICAL_REVIEW              (AI_ASSISTED_REFERENCE_REVIEW)
  -> SUBJECT_REVIEW                  (AI_ASSISTED_REFERENCE_REVIEW)
  -> SCOPE_REVIEW                    (REPOSITORY_SCOPE_AUTHORITY)
  -> PROMOTED_INSTRUCTIONAL_KNOWLEDGE
```

Each promoted entry binds `evidence_class`, `provenance`, `subject_scope`,
`capability_refs[]`, `applicability_conditions`, `known_limitations`,
`review_authority`, `promoted_version` and `promotion_digest`, plus the full
stage-by-stage `review_pipeline` and the current `expert_review_state`.

Run it with:

```bash
python 'Grade 9/V2/Mathematics/InstructionalKnowledge/engine/promote_math_pck.py' \
  --pck-candidates 'Grade 9/V2/Mathematics/InstructionalKnowledge/registry/math-pck-candidates.json' \
  --out 'Grade 9/V2/Mathematics/InstructionalKnowledge/registry/math-pck-promotion-registry.json'
```

The committed promotion registry is byte-reproducible from that command, and
`contracts/validate_contracts.py` fails closed if it drifts.

## Two authorities, never interchangeable

| Authority | What it can establish | Resulting promotion |
| --- | --- | --- |
| `AI_ASSISTED_REFERENCE_REVIEW` / `REPOSITORY_SCOPE_AUTHORITY` | digest custody, structural pedagogical completeness, cross-registry referential correctness, subject-scope admissibility | `PROVISIONAL_PROMOTED` — `authoring_legal=true`, `producer_legal=false`, `release_legal=false`, `expert_review_state` `PENDING` |
| `SUBJECT_EXPERT_PASS` + `PEDAGOGY_EXPERT_PASS` | that the mathematics and the teaching design are actually right | `PROMOTED` — `producer_legal=true`, `release_legal=true` |

An AI agent or CI job cannot manufacture the second row. `expert_records()`
accepts only a `REAL` / release-eligible Shared HumanReview intake result bound
to the exact asset digest; anything else is rejected as
`TEST_ONLY_REVIEW_USED_AS_EXPERT_EVIDENCE` or `PCK_PROMOTION_EVIDENCE_UNBOUND`.

## Current repository state

```text
candidates                 20  (lifecycle CANDIDATE, review PENDING_HUMAN_REVIEW)
promotions                 20  (all PROVISIONAL_PROMOTED)
producer-legal promotions   0
SUBJECT_EXPERT_PASS         PENDING
PEDAGOGY_EXPERT_PASS        PENDING
```

This is the honest state, not a completeness claim. Downstream consequences:

* `Core1Authoring` materializes a real study plan with
  `release_class = PROVISIONAL_PENDING_EXPERT_REVIEW` and
  `pck_authority.release_legal = false`.
* `Core2Transfer` reports `core1_linkage_mode = MATERIALIZED_PROVISIONAL`.
* `ColdStart` reports `release_status = PROVISIONAL_PENDING_PCK_EXPERT_REVIEW`
  with the blocker `M-G/#242:PCK_EXPERT_REVIEW_PENDING`.
* `Validation/MatureGate` (M-L) can never reach
  `V2_MATURE_INSTRUCTIONAL_PRODUCT` while `pck_release_legal` is false.

#242 stays open until authorized subject and pedagogy review evidence exists.

## Candidate coverage

The candidate set covers every assessment-scope capability that requires a full
teaching treatment, so the previous `PCK_CANDIDATE_COVERAGE` gap is closed:

```text
EQUALITY_PRESERVATION              AXIS_CONSTRAINT_SEMANTICS
EXPRESSION_IDENTITY                EUCLID_STATEMENT_STATUS
BINOMIAL_SQUARE_RECONSTRUCTION     LINE_EQUATION_CONSTRUCTION
ORDERED_PAIR_SEMANTICS             LINEAR_TREND_EXTRAPOLATION
SLOPE_AS_RATE_OF_CHANGE            PARALLEL_CRITERION_ANGLE_SUM
COLLINEARITY_BY_COMMON_DIRECTION   PARAMETER_SUFFICIENCY_CONDITION
SIMULTANEOUS_EQUATION_ELIMINATION  QUADRANT_SIGN_MAP
GEOMETRY_TO_ALGEBRA_BRIDGE         RATIONAL_OPERATION_MEANING
SOLUTION_VERIFICATION              RELATIVE_RATE_COMPOSITION
WORD_TO_EQUATION_MODELLING         UNORDERED_PAIR_COUNT
```

Each candidate carries capability refs, applicability conditions, anchor,
representation path, ordinary-language bridge, reconstruction route, controlled
contrast, worked-example family, misconception discriminator, repair route,
verification method, fading dimensions, transfer family, limitations,
provenance, review state, and digest.

This directory does not decide `VERIFY_ONLY`, `ACTIVE_STUDY`, `REPAIR_BEFORE`,
`REPAIR_IN_UNIT`, or `PROBE_FIRST`. Those remain upstream Study Synthesis
decisions.

## Falsifiers

```text
PCK_PROMOTION_STAGE_SKIPPED
PCK_PROMOTION_STAGE_ORDER_VIOLATION
FABRICATED_EXPERT_REVIEW_AUTHORITY
PROVISIONAL_PROMOTION_CLAIMED_PRODUCER_LEGAL
PCK_PROMOTION_EVIDENCE_UNBOUND
PCK_PROMOTION_CAPABILITY_OUT_OF_SUBJECT_SCOPE
PCK_PROMOTION_FAMILY_UNRESOLVED
PCK_PEDAGOGICAL_STRUCTURE_INCOMPLETE
PCK_PROVENANCE_UNDECLARED
PCK_PROMOTION_DIGEST_MISMATCH
PCK_PROMOTION_REGISTRY_DIGEST_MISMATCH
PCK_PROMOTION_UNKNOWN_ASSET
TOPIC_SPECIFIC_PROMOTION_RECORD
TEST_ONLY_REVIEW_USED_AS_EXPERT_EVIDENCE
```

## Validation

```bash
python 'Grade 9/V2/Mathematics/InstructionalKnowledge/contracts/validate_contracts.py'
python 'Grade 9/V2/Mathematics/InstructionalKnowledge/tests/test_math_pck_promotion.py'
```

Test-only promotion fixtures live downstream under `Core1Authoring/fixtures/`
and are structurally non-releaseable.
