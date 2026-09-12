# Grade 4 Mathematics V2

Canonical Grade-4 Mathematics V2 product implementation.

This tree owns Grade-4-specific authoring, learning design, representation semantics, work surfaces, publication, benchmarks, and acceptance adapters. Reusable Primary/Common infrastructure remains upstream and is copied only with explicit provenance.

Architecture chain:

```text
QuestionEvidence
  -> CoreSkills authoring
  -> LearningDesign / LearningRepresentationPlan
  -> Representation primitives + work surfaces
  -> Publication
  -> Acceptance
```

Migration authority: issue #340. Parent architecture: #328. Authoring: #336. Learning representation: #339. Publisher: #327.

The publisher may realize validated mathematics; it may not invent the teaching route.
