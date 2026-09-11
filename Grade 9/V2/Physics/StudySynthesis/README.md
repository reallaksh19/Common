# Physics V2 — P-F Learner Study Scope, Study Model and longitudinal initialization

Implements issue #254 after the assessment-first P-A → P-E chain.

P-F is the join between **learner-independent assessment authority** and **optional learner evidence**. Its governing invariant is:

```text
ASSESSMENT SCOPE decides WHAT must be teachable.
LEARNER INTELLIGENCE decides ORDER / DEPTH / BRIDGE / TREATMENT / SUPPORT.
```

The source assessment therefore cannot shrink because a learner shows one narrow weakness, and a READY capability cannot be relabelled weak merely to justify a downstream repair.

## Inputs

```text
P-C PhysicsAssessmentScope authority + question/capability bindings
P-D Physics problem-family / reasoning-route / verification semantics
P-E LearnerStateSnapshot             # AttemptSet absent or present
P-F PhysicsTreatmentPolicy
```

`LearnerStudyScope` is derived **without learner state**. The same assessment + P-D semantics must therefore produce the same scope digest in both the no-attempt and attempt-present branches.

## Outputs

```text
PhysicsLearnerStudyScope
PhysicsLearnerStudyModel
per-capability longitudinal initialization
```

Every study-scope capability keeps source traceability plus the Physics structure needed by later authoring:

```text
assessment question refs
prerequisite refs
system / object / frame / sign obligations
state / phase / continuity obligations
model-validity conditions
representation requirements
physical model + law refs
problem-family refs
reasoning-route roles
verification requirements + verification-route refs
```

Learner evidence is applied only after that structure is frozen.

## Treatment states

```text
READY_VERIFY_ONLY
ACTIVE_STUDY
REPAIR_BEFORE
REPAIR_IN_UNIT
PROBE_FIRST
```

- `READY_VERIFY_ONLY`: brief activation plus an independent physical check. Required frame/sign, model-validity and verification obligations remain present, but full reteaching is forbidden.
- `ACTIVE_STUDY`: complete assessed Physics teaching. This is the neutral no-attempt default for UNKNOWN capability state.
- `REPAIR_BEFORE`: a demonstrated difficulty in a prerequisite that supports downstream assessed Physics is repaired before dependent work.
- `REPAIR_IN_UNIT`: a demonstrated localized difficulty is repaired inside the relevant assessed unit.
- `PROBE_FIRST`: mixed or unresolved evidence retains the exact P-E probe requirement before treatment is committed.

`NO_ATTEMPT != PHYSICS_WEAK`. No-attempt UNKNOWN capability state cannot force a repair classification.

## Longitudinal initialization

P-F initializes distinct dimensions rather than one mastery scalar:

```text
acquisition
independent_reconstruction
delayed_retention
near_transfer
far_transfer
mixed_model_discrimination
representation_translation
fluency
timed_performance
```

Current demonstrated evidence may contribute to acquisition or current independent reconstruction. It does **not** close delayed retention, near/far transfer, mixed discrimination, fluency or timed-performance obligations. Physics-specific future obligations include representation shifts, hidden-model stories, phase handoff after delay, sign/frame discrimination, mixed graph/model selection and unprompted physical verification.

## Migration boundary

P-F consumes the shared P-E learner-state contract. The older Physics-only `LearnerIntelligence` proof was retained only as a temporary compatibility surface during P-E; P-F removes that duplicate path after migrating StudySynthesis.

## Non-claims

P-F does not author final Core1 prose, worked examples, teaching primitive rendering, Core2 H1/H2/H3 wording, solutions, PDFs, publication layout, scheduling or psychometric mastery probabilities. It produces the scope/treatment/longitudinal authority those later phases must consume.
