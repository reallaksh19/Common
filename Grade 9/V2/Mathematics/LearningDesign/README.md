# MATH-V2-04 Mathematics Learning Design

Status: fresh-lineage subject proof for issue #209.

This directory owns **how** a frozen Mathematics `LearnerStudyModel` is taught. It does not own canonical truth, learner diagnosis, Study Synthesis treatment, longitudinal scheduling, page/layout realization, or benchmark comparison.

```text
MathLearnerStudyModel
+ PublicationPlanningView interface
+ PublicationTarget interface
+ MathLearningDesignPolicy
→ MathLearningDesignPlan
```

Interactive support is separate:

```text
MathLearningDesignPlan
+ InteractionSupportState
→ SupportSelection
```

## Core invariants

- preserve every StudyModel target, engagement mode, readiness mode and study obligation;
- use demonstrated/ready capabilities as entry points rather than reteaching them;
- `PROBE_FIRST` begins with the required diagnostic probe;
- equality work uses one legal mathematical operation per line;
- `MINIMAL_CONTRAST` holds background structure constant and varies one focal distinction;
- worked → guided → faded → independent support decreases materially;
- independent attempts contain no conceptual hints or pre-completed algebra;
- verification is embedded inside the reasoning path;
- transfer is non-isomorphic, not number substitution;
- substantive teaching is followed by observable learner action;
- static authored design is separate from live support selection;
- no benchmark/reference artifact is a producer input.

All fixtures are `PUBLIC_SYNTHETIC`; no real learner evidence is committed.
