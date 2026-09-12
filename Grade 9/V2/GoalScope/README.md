# V2-03 Goal / Scope Authority

V2-03 freezes scope ownership and canonical dependency composition without implementing Study Synthesis.

## Authority split

```text
LearningGoalRequest
  external intent; what was requested

CanonicalTargetScope
  canonical curriculum/exam/topic obligations that satisfy the request

LearnerStudyScope
  downstream Study Synthesis boundary; may alter treatment/active timing, never silently erase obligations

PublicationScope
  one concrete realization; may select a subset only with explicit omission accounting

CanonicalKnowledgeSet
  exact canonical references required for the target scope, including dependency closure
```

Canonical truth is owned by Core1. None of these scope artifacts may define, edit, or embed canonical subject semantics.

## Resolver

`resolver/resolve_scope.py` resolves each required canonical target through a registry snapshot.

Resolution states:

- `REUSE_EXISTING` — same-subject canonical dependency already exists and is active.
- `COMPOSE_DEPENDENCY` — active dependency is owned by another canonical subject authority.
- `REVALIDATE` — an asset exists but status/version/digest requirements are not currently satisfied.
- `CANONICAL_GAP_CANDIDATE` — required canonical asset is absent.

Dependency closure is deterministic, transitive, cycle-safe, and exact-version/digest bound.

## Cross-subject proof

Synthetic Chemistry gas-law scope composes the shared Mathematics proportional-reasoning asset rather than duplicating proportionality semantics into Chemistry. The Mathematics asset itself depends on equality-preserving transformation, proving transitive closure.

No learner data or benchmark artifact is used.
