# P-F methodology

P-F has two sequential authority layers.

1. **Derive `PhysicsLearnerStudyScope` without learner state.** Use P-C question/capability bindings and P-D problem semantics to close prerequisite capability dependencies and preserve item trace, system/frame/sign, state/phase, model-validity, representation, problem-family and verification obligations.
2. **Apply P-E learner state only to treatment.** Map evidence state to READY/ACTIVE/REPAIR/PROBE treatment without modifying the frozen scope structure.

The critical safety check is structural equality: every capability record in `PhysicsLearnerStudyModel` must retain the exact scope-owned structural fields from `PhysicsLearnerStudyScope`. Any deletion or mutation is a release-blocking error.

## Learner-state interpretation

```text
DEMONSTRATED           -> READY_VERIFY_ONLY
UNKNOWN                -> ACTIVE_STUDY
EVIDENCE_OF_DIFFICULTY -> REPAIR_IN_UNIT
EVIDENCE_OF_DIFFICULTY + prerequisite dependency -> REPAIR_BEFORE
MIXED / unresolved diagnostic evidence -> PROBE_FIRST
```

A `PROBE_FIRST` decision must carry the P-E probe requirement. No P-F rule may invent a diagnosis.

## Longitudinal rule

Current evidence is episode-local. Delayed retention, transfer, mixed discrimination, fluency and timed performance remain future evidence obligations even after a current success. P-F initializes those obligations; later longitudinal phases own closure or promotion.
