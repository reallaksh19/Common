# Mathematics V2 — M-C Assessment Scope Reconciliation

Implements issue #238 under the assessment-first Mathematics roadmap #235.

## Authority boundary

M-C reconciles three independent authorities:

```text
QuestionSet          = evidence of what is actually assessed
DeclaredTopicScope   = stated curriculum / assessment boundary
Math Scope Authority = concept/capability/dependency identity
```

None silently overwrites another.

M-C consumes the merged M-A source-fidelity contracts and the merged M-B item-safety review. It does **not** consume an `AttemptSet`, learner state, diagnosis, StudyModel treatment, Core1 authoring, Core2 hints, difficulty badges, or publication layout.

The local `MathAssessmentScopeAuthority` owns only the identity/dependency layer needed for scope resolution:

```text
concept identity
capability identity
prerequisite edges
problem-family identity
representation identity
verification-obligation identity
reasoning-role expectation identity
```

Full problem-family semantics, reasoning routes, verification routes and multidimensional demand are intentionally deferred to **M-D / #239**.

## Runtime

```text
M-A QuestionSet + DeclaredTopicScope
        +
M-B AssessmentItemReview
        +
M-C MathAssessmentScopeAuthority
        +
QuestionScopeBindingRegistry
        ↓
ScopeReconciliationReport
MathAssessmentScopeModel
MathAssessmentCoverageMatrix
MathPrerequisiteClosure
```

Every question and subpart remains visible in the coverage matrix, including underdetermined, multiple-solution, outside-scope and future `UNMAPPED` items.

## Mapping states

```text
MAPPED
PARTIAL_SCOPE_MATCH
OUTSIDE_DECLARED_SCOPE
UNMAPPED
```

`OUTSIDE_DECLARED_SCOPE` preserves the question's mathematical mapping while emitting an explicit boundary finding. `UNMAPPED` fails closed without inventing concepts/capabilities.

## Reconciliation findings

```text
QUESTION_OUTSIDE_DECLARED_SCOPE
DECLARED_TOPIC_NOT_ASSESSED
UNMAPPED_QUESTION
PARTIAL_SCOPE_MATCH
QUESTION_MAPS_TO_UNDECLARED_PREREQUISITE
```

The reference fixture deliberately proves:

- Q6 remains mapped to pair-counting mathematics but is outside the supplied topic boundary;
- Q9 remains in coverage as an underdetermined M-B item and has only a parent-topic partial match;
- Q12 explicitly records a geometric-modelling prerequisite outside the supplied topic list;
- an unassessed declared subtopic remains visible rather than silently disappearing.

## Invariants

- M-B review runs before scope derivation.
- Every source item/subpart has exactly one mapping state.
- Every canonical/prerequisite/problem-family/representation/verification/role ref resolves.
- Prerequisite closure is transitive, deterministic and explicitly recorded.
- `AttemptSet`/learner fields are forbidden inputs to this phase.
- Scope derivation is deterministic and independent of learner evidence.
- M-C does not claim psychometric difficulty or author hint/solution text.
