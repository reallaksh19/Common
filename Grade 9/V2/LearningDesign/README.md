# V2-05 Learning Design

Status: draft implementation for issue #193.

This directory owns **how a frozen LearnerStudyModel is taught**. It does not own canonical truth, learner diagnosis, Study Synthesis treatment decisions, longitudinal scheduling, page/layout realization, or final benchmark validation.

## Producer boundary

```text
LearnerStudyModel
+ PublicationPlanningView
+ PublicationTarget
+ LearningDesignPolicy
-> LearningDesignResult
   -> LearningDesignPlan | explicit LEARNING_DESIGN_GAP
```

Interactive delivery has a separate live boundary:

```text
LearningDesignPlan
+ InteractionSupportState
-> SupportSelection
```

The runtime selector may select only a support rung already approved by the frozen design. It does not mutate the design or StudyModel.

## Core invariants

- every material StudyModel obligation has explicit coverage;
- treatment/readiness from Study Synthesis are preserved, not reclassified;
- `PROBE_FIRST` starts with a diagnostic probe;
- reconstruction carries semantic payload, not a naked formula;
- worked reasoning contains reasoning moves, not answer-only substitution;
- contrasts have controlled shared structure plus a focal difference;
- fading removes meaningful support;
- independent attempts contain no conceptual hint features;
- transfer is non-isomorphic and cannot be number-only;
- representation work states the translation job and invariant;
- substantive teaching is followed by observable learner action;
- conceptual support and access/load support are distinct;
- live attempt state is not an input to the static design builder;
- no benchmark/reference artifact is a producer input.

Synthetic fixtures only; no real learner data is committed.
