# Learner Intelligence ↔ Two-Core Integration Contract

**Status:** DRAFT / PHASE 4
**Depends on:** Phases 1–3, PR #160 architecture boundary, PR #161 Core (2) boundary

## 1. Integration principle

Do not move learner diagnosis into Core (1) and do not make Core (2) rediscover learner diagnosis.

```text
Core (1) Research
  -> ResearchBundle + canonical reasoning/capability references

Learner Intelligence
  -> LearnerStateSnapshot
  -> scoped LearnerStateView

Core (2) Publisher
  <- ResearchBundle
  <- LearnerStateView
  <- PublicationTarget
```

Core (1) and Learner Intelligence may reference the same canonical concept/capability/misconception IDs, but learner evidence/state MUST NOT affect ResearchBundle semantic or package identity.

## 2. Core (1) integration

Core (1) remains responsible for subject truth and project verification. It MAY include/reference, where material to the project:

```text
canonical capability IDs
subject reasoning-contract IDs
canonical misconception IDs
error-signature IDs
diagnostic-probe IDs
prerequisite capability edges
```

These are properties of subject/problem reasoning, not assertions about a particular learner.

Core (1) MUST NOT contain:

```text
learner attempts
learner diagnostic cases
learner capability state
learner Bxx derived from evidence
```

## 3. Learner Intelligence integration

Learner Intelligence consumes canonical IDs plus learner evidence. It owns:

```text
attempt/evidence custody
reasoning observations
diagnostic cases
capability state
cross-capability RCA
state snapshots
scoped state views
Bxx projection policy
```

It does not create new mathematical/scientific truth. Missing subject semantics are a canonical/research gap, not a local learner-state invention.

## 4. Core (2) integration

Core (2) learner input evolves from:

```text
ResearchBundle + LearnerProfile(Bxx) + PublicationTarget
```

toward:

```text
ResearchBundle + LearnerInput + PublicationTarget
```

where `LearnerInput` is exactly one of:

```text
LEGACY_BASELINE: LearnerProfile
EVIDENCE_BACKED: LearnerStateView
```

During migration, both modes are supported. A state view may carry a Bxx projection for existing profile logic, but Core (2) should prefer capability state and diagnostic/probe obligations where available.

## 5. Teaching-decision boundary

Learner Intelligence answers:

```text
what is demonstrated?
what failed?
what remains ambiguous?
which capability needs repair/probing?
```

Core (2) answers:

```text
how should this be taught?
what representation should be used?
how much support is appropriate?
how should support fade?
what practice/transfer should be published?
```

A diagnostic hypothesis MUST NOT directly prescribe page/layout/rendering choices.

## 6. Bxx migration

Bxx is retained for compatibility and cold start.

```text
Cold start:
LearnerProfile.user/fallback Bxx -> Core (2)

Evidence-backed:
LearnerStateSnapshot -> BxxProjectionPolicy -> LearnerStateView.bxx_projection
```

A derived Bxx is a publication adaptation score under a named policy; it MUST NOT be described as a psychometric mastery percentage.

## 7. Fail-closed behavior

Core (2) MUST fail or route explicitly when:

- the requested learner-state view references unknown canonical capabilities;
- a required diagnostic probe is ignored while the target publication claims misconception repair;
- learner-state evidence requires subject semantics absent from the ResearchBundle/canonical registry;
- state-view snapshot digest/custody is invalid where exact state custody is required.

Learner Intelligence MUST emit a subject/canonical gap instead of inventing a reasoning contract.

## 8. PR #160 / #161 migration rule

This Phase 4 PR freezes the **interface contract only**. It does not rewrite PR #160 or PR #161 while those PRs remain independently reviewable.

After upstream phases are accepted:

1. Core (1) receives a narrow registry/reference integration change.
2. Core (2) receives a narrow `LearnerInput` adapter using the already-frozen Phase 4 contract.
3. Existing `LearnerProfile` replays remain regression fixtures until the migration is proven.

## 9. Integration gates

```text
LEARNER_STATE_OUTSIDE_RESEARCH_BUNDLE_IDENTITY = PASS
CORE1_DOES_NOT_OWN_LEARNER_DIAGNOSIS = PASS
CORE2_DOES_NOT_INVENT_DIAGNOSIS = PASS
LEGACY_LEARNER_PROFILE_COMPATIBILITY = PASS
EVIDENCE_BACKED_LEARNER_STATE_VIEW_SUPPORTED = PASS
BXX_PROJECTION_HAS_POLICY_AND_PROVENANCE = PASS
UNKNOWN_CANONICAL_CAPABILITY_FAILS_CLOSED = PASS
```
