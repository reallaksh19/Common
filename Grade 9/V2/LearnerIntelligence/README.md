# V2 Learner Intelligence

V2 Learner Intelligence is the descriptive learner-evidence authority defined by #175 and implemented by #184.

```text
LearnerEvidenceLedger
→ ReasoningObservation
→ DiagnosticCase
→ LearnerStateSnapshot
→ ResearchLearnerView
→ PublicationPlanningView
```

Authority separation is strict: Evidence != Observation != Diagnosis != Learner State != Study Decision != Teaching Decision.

This subsystem references canonical capability/reasoning/error/probe IDs but does not define their subject meaning. Missing canonical references fail closed.

Snapshot identity binds filtered evidence, observations, canonical registry version, diagnostic/state policy versions, explicit `as_of`, and temporal-policy version. No wall clock, random ID, branch SHA, or implicit `now` participates.

`ResearchLearnerView` and `PublicationPlanningView` are descriptive only. The publication view is privacy-minimized and contains no raw learner work, Study Synthesis decision, LearningDesign choreography, hint selection, practice count, sequencing, representation prescription, or page-layout decision.

Conservative inference invariants:

- one ordinary failure cannot by itself create `REPAIR_REQUIRED`;
- successful upstream checkpoints remain positive evidence when later work fails;
- guided success is not independent success;
- ambiguity requires a diagnostic probe;
- cross-subject recurrence is a candidate relationship, never a proven psychological cause;
- synthetic fixtures are CI evidence only and never production learner evidence.
