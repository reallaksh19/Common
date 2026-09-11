# Mathematics V2 — M-F Study Synthesis

Implements #241 after merged M-A through M-E.

M-F joins **learner-independent assessment scope** with **descriptive learner state** without allowing learner evidence to delete assessed content.

```text
M-C Question→Math scope authority
+ M-D problem-family / demand semantics
+ M-E LearnerStateSnapshot (attempt-present or no-attempt)
        ↓
LearnerStudyScope                 learner-independent WHAT is in scope
        +
MathTreatmentPolicy              deterministic treatment rules
        ↓
LearnerStudyModel                learner-conditioned HOW MUCH / WHEN / WHAT BRIDGE
        ↓
longitudinal evidence obligations
```

## Governing invariant

```text
ASSESSMENT SCOPE decides WHAT must be teachable.
LEARNER INTELLIGENCE decides ORDER / DEPTH / BRIDGE / TREATMENT / SUPPORT.
```

`LearnerStudyScope` is therefore computed without learner state. The same assessment must produce the same StudyScope with or without an `AttemptSet`.

## Treatment vocabulary

- `VERIFY_ONLY` — current evidence is sufficient for brief activation plus an independent check; do not reteach for page density.
- `ACTIVE_STUDY` — complete teaching is required because the capability is assessed/supporting and not yet evidenced ready.
- `REPAIR_BEFORE` — a demonstrated developing prerequisite is a repeated-dependency bottleneck and should be repaired before dependent work.
- `REPAIR_IN_UNIT` — a demonstrated developing capability can be repaired inside the relevant unit.
- `PROBE_FIRST` — an unresolved diagnostic case makes treatment choice evidence-dependent; collect decisive evidence first.

No-attempt `UNKNOWN` maps to `ACTIVE_STUDY`, never to repair. `NO_ATTEMPT != WEAK`.

## Scope exceptions

`OUTSIDE_DECLARED_SCOPE` and `PARTIAL_SCOPE_MATCH` items remain present as explicit assessment-scope exceptions. Their mathematical mappings are not silently deleted. `UNMAPPED` remains visible and blocking rather than being invented.

## Longitudinal model

M-F initializes separate evidence obligations for acquisition, independent reconstruction, delayed retention, near transfer, far transfer, mixed discrimination, fluency and timed performance. A current success can contribute current evidence but cannot close delayed or transfer obligations.

## Boundary

M-F owns synthesis of study scope, treatment and future evidence obligations. It does **not** author lesson prose, examples, teaching sequences, hint ladders, Core2 solutions, page layout, renderer primitives, psychometric mastery probabilities, or new learner diagnoses.
