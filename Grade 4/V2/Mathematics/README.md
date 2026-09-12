# Grade 4 Mathematics V2

Canonical Grade-4 Mathematics V2 product implementation.

**New source / scanned-question input:** start with [`START_HERE.md`](START_HERE.md), then copy `Benchmarks/source_sets/_template/`. Do not begin in the PDF renderer.

This tree owns Grade-4-specific authoring, task-level learning design, document-level study design, representation semantics, work surfaces, publication, benchmarks, and acceptance adapters. Reusable Primary/Common infrastructure remains upstream and is copied only with explicit provenance.

Architecture chain:

```text
Scanned/source evidence
  -> faithful source transcription
  -> QuestionEvidence
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

Migration authority: issue #340. Parent architecture history: #328. Authoring history: #336. Learning representation history: #339. StudyJourney gap/fix: #348. Publisher history: #327. Canonical mainline consolidation: #354.

The publisher may realize validated mathematics and the validated study journey; it may not invent pedagogy, reorder teaching intent, silently repair source evidence, or repair missing instruction by renderer-local content.
