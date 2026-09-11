# Physics V2 — P-C Assessment Scope / Question→Physics Authority

Implements **#251** under Physics assessment-first parent **#248** / programme **#234**. It consumes the merged P-A source-fidelity authority and P-B assessment-safety authority, then resolves assessment scope **before any learner evidence is interpreted**.

```text
QuestionSet                    = what the source actually assesses
DeclaredTopicScope             = stated curriculum / assessment boundary
Canonical Physics              = physical meaning / dependency authority
P-B AssessmentReviewBundle     = safe validity / diagnostic-use boundary
                               ↓
                    P-C scope reconciliation
                               ↓
PhysicsAssessmentScopeModel
PhysicsAssessmentCoverageMatrix
ScopeReconciliationReport
PhysicsPrerequisiteClosure
```

## Non-overwrite rule

None of the three scope authorities may silently replace another. A question outside the declared boundary remains visible as question evidence. A declared topic not evidenced by any question remains visible. Canonical Physics supplies meaning and validity conditions; it does not rewrite the source.

P-C deliberately accepts **no AttemptSet, learner state, diagnosis, hint state, or treatment input**.

## Physics closure per item

Every question/subpart has an explicit mapping state and, when mapped, carries:

- declared-topic references;
- canonical concepts and capabilities;
- explicit prerequisite closure;
- system/object roles;
- reference frame and sign convention;
- state variables and phase structure;
- physical model and governing-law identities;
- model-validity conditions;
- problem-family identity only (semantics owned by P-D);
- representation demands and exact source-representation refs;
- verification obligations and expected reasoning roles.

A formula name alone is never sufficient scope metadata.

## Canonical Physics binding

`physics-assessment-scope-authority.json` is digest-bound to `Canonical/registry/capabilities.json`. P-C scope capabilities may refine assessment-specific identity, but every one must point to one or more established Physics Canonical capability foundations.

The question-binding registry is itself digest-bound to the exact scope-authority digest, so extending a registered reasoning-role identity cannot silently leave stale Question→Physics custody behind.

## Pilot behavior

The P-A/P-B Motion fixture yields **17 zero-loss coverage rows**: Q1–Q14 plus Q14.a/b/c.

Reference cases:

- Q8 keeps its exact `FIG-Q8-VT` dependency and identifies signed-area graph demand.
- Q9 is only `PARTIAL_SCOPE_MATCH`: moving-release Physics is identifiable, but the source item itself is incomplete.
- Q10 is `PARTIAL_SCOPE_MATCH`: multi-phase structure is identifiable, but P-B already proved the assessment target is underdetermined.
- Q12 preserves option-graph discrimination explicitly: `COMPARE` is a registered scope-level reasoning-role identity rather than an unbound prose label.
- Q13 stays `BLOCKED` because the required graph is missing/truncated; frame/sign and graph demand are not invented.
- Q14 and Q14.a/b/c stay `BLOCKED` because P-B requires rendered-source inspection before source fidelity can be certified.

## Mismatch findings

The report supports:

```text
QUESTION_OUTSIDE_DECLARED_SCOPE
DECLARED_TOPIC_NOT_ASSESSED
UNMAPPED_QUESTION
PARTIAL_SCOPE_MATCH
QUESTION_REQUIRES_UNDECLARED_PREREQUISITE
MODEL_ASSUMPTION_NOT_IN_DECLARED_SCOPE
REPRESENTATION_DEPENDENCY_UNRESOLVED
```

Items are never dropped merely because they are underdetermined, review-required, source-damaged, or excluded from negative learner diagnosis.

## P-C / P-D boundary

Problem-family IDs are bound here only as stable identities:

```text
identity_status = BOUND_IDENTITY
semantic_owner_phase = P-D
```

P-C does **not** own semantic reasoning routes, verification routes, demand vectors, difficulty, hints, solutions, learner treatment, Core1/Core2 authoring, or publication layout.

## Validation

CI re-runs P-A and P-B first, then validates P-C contracts, runs mutation falsifiers, and proves deterministic replay. The exit gate is the closed-or-failed-closed chain:

```text
Question
↔ Topic/Subtopic
↔ Concept
↔ Capability / prerequisite
↔ System / Frame / State / Phase / Model / Law
↔ ProblemFamily identity
↔ Representation / verification obligations
```

Next phase after merge: **#252 / P-D — Physics problem families, ReasoningRoute, model-validity and multidimensional demand semantics**.
