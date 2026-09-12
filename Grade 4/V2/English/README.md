# Grade 4 English V2

Canonical Grade-4 English V2 product implementation.

This tree owns Grade-4-specific English source extraction, typed question evidence, source models, learner-evidence boundaries, learning design, representation semantics, publication contracts, benchmarks, and acceptance adapters. Reusable Primary/Common semantics remain upstream and are referenced rather than silently forked.

Architecture chain:

```text
Source scan / question set
  -> faithful SourceEvidence
  -> SourceModel + QuestionEvidence
  -> optional LearnerEvidence
  -> CoreSkills authoring
  -> LearningDesign / LearningRepresentationPlan
  -> Representation primitives + response/work surfaces
  -> Publication
  -> Source-coverage Acceptance
```

## Non-negotiable boundaries

- Source questions define observed assessment demand; they do not automatically prove the complete official syllabus.
- Source wording, categories, defects, and ambiguity are preserved. They are never silently repaired.
- Learner mistakes are evidence about a response, not source truth and not durable learner traits.
- Open English responses are not reduced to answer-string matching. Rubrics, textual evidence, reasoning structure, and teacher/source judgement remain explicit.
- A renderer may position and style validated English learning content; it may not invent a teaching rule, hint, category, misconception diagnosis, or model answer.
- Research may enrich a source model but must never silently replace the assessment source model.

Start with `START_HERE.md` before adding a new scanned source set.
