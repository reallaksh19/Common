# Grade 4 Mathematics V2

Canonical Grade-4 Mathematics V2 product implementation.

This tree owns Grade-4-specific authoring, task-level learning design, document-level study design, representation semantics, work surfaces, publication, benchmarks, and acceptance adapters. Reusable Primary/Common infrastructure remains upstream and is copied only with explicit provenance.

Architecture chain:

```text
QuestionEvidence
  -> CoreSkills authoring
  -> LearningDesign / LearningRepresentationPlan
  -> StudyDesign / StudyJourneyPlan
  -> Representation primitives + work surfaces
  -> Publication
  -> Acceptance
```

`LearningRepresentationPlan` answers: **how should this task be supported?**

`StudyJourneyPlan` answers: **what should the learner be taught first, what should be worked, guided, attempted independently, retrieved and transferred, and in what order across the document?**

Several source questions may be synthesized into one teaching concept. A study guide must not default to one source question = one concept = one page.

Migration authority: issue #340. Parent architecture: #328. Authoring: #336. Learning representation: #339. StudyJourney gap/fix: #348. Publisher: #327.

The publisher may realize validated mathematics and the validated study journey; it may not invent pedagogy, reorder teaching intent, or repair missing instruction by renderer-local content.
