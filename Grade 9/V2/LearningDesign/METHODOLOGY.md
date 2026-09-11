# Learning Design methodology

## 1. Preserve the StudyModel

For every target, carry forward the exact `study_treatment` and `readiness` values. Learning Design may elaborate *how* an obligation is taught but may not delete, weaken, replace, or reclassify the obligation.

Each material obligation must appear in `obligation_coverage` and must be realized by one or more choreography steps.

## 2. Design from semantic obligations

A useful step has three parts:

1. the StudyModel obligation it realizes;
2. the learner cognitive job;
3. enough instructional payload to make the role meaningful.

Role labels without payload are invalid.

## 3. Required sufficiency rules

- `RECONSTRUCT`: relation/object meaning, term origins, conditions, and reconstruction route.
- `WORKED_REASONING`: at least three named reasoning moves and an explicit self-check.
- `REPRESENTATION_TRANSLATE`: source representation, destination representation, learner translation job, and invariant to preserve.
- `MINIMAL_CONTRAST`: controlled shared features, one focal difference, and prediction before resolution.
- `GUIDED_ATTEMPT -> FADED_ATTEMPT -> INDEPENDENT_ATTEMPT`: meaningful support must monotonically reduce; independent conceptual supports are empty.
- `TRANSFER`: change at least one structural dimension beyond number change and require non-isomorphic reasoning.
- `COMPLETION_EVIDENCE`: state the observable independent evidence expected.

## 4. Probe-first rule

A target marked `PROBE_FIRST` begins with `DIAGNOSTIC_PROBE`. Explanation/reteach before the probe is a boundary violation.

## 5. Teaching followed by action

Substantive authored teaching (`RECONSTRUCT`, `WORKED_REASONING`, `MINIMAL_CONTRAST`, `MISCONCEPTION_REPAIR`) must be followed by an observable learner-action step before another block of substantive teaching or before completion is claimed.

## 6. Static vs runtime

The authored plan consumes only frozen `PublicationPlanningView`. Live current-attempt information belongs to `InteractionSupportState` and is used only by the runtime selector.

The plan pre-approves support rungs. Runtime may choose among them; it may not author a new hint, mutate the plan, diagnose the learner, or change StudyModel readiness.

## 7. Support classes

`CONCEPTUAL` support changes the learner's reasoning assistance.
`ACCESS` support changes access/load without supplying the conceptual solution route.

They are tracked separately.

After repeated same-route failure, runtime may select only an approved rung marked `ROUTE_CHANGE`.
