# LEGACY / REFERENCE ONLY — not part of the M-A→M-L chain

`Grade 9/V2/Mathematics/LearningDesign/` belongs to the **MATH-V2-01..07** lineage
(issues #197/#209, PRs #160/#161/#202). That was a parallel architecture attempt
that predates the Core1/Core2 split and was never wired to the live chain.

The production Mathematics chain is:

```text
M-A AssessmentIntake      M-G InstructionalKnowledge
M-B AssessmentReview      M-H Core1Authoring + RepresentationSemantics
M-C AssessmentScope       M-I Core2Transfer
M-D ProblemSemantics      M-J CoverageClosure
M-E LearnerIntelligence   M-K ColdStart
M-F StudySynthesis        M-L Validation/MatureGate + Publication (core products)
```

`ColdStart/engine/math_cold_start_runner.py` imports exactly those phases. It
does **not** import anything from this directory.

## Status

* Retained for reference: its `MathLearningDesignPlan` choreography and support
  selection remain useful prior art.
* **Do not** extend it, and do not treat its outputs as release evidence.
* Its useful engineering — material custody, `PublicationStructure`,
  `PhysicalPageMap`, ReportLab placement instrumentation and exact PDF hash
  binding — has been **adopted**, not rebuilt, by
  `Publication/engine/realize_math_core_products.py`, which consumes real
  `MathCore1StudyPlan` / `MathCore2TransferPlan` JSON instead.

Tracking: #319.
