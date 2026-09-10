# Primary Grades 4–5 architecture

This directory is the canonical education-semantic authority for the Grade 4–5 Primary platform.

Tracking issue: https://github.com/reallaksh19/Common/issues/162

Programme roadmap: https://github.com/reallaksh19/Study-Hub/issues/40

Backend/provider roadmap: https://github.com/reallaksh19/Study-Hub/issues/39

## Authority

```text
Common
  educational meaning / pedagogy / learner-state semantics
        ↓
Study-Hub
  orchestration / publication / app-facing transport adapters
        ↓
Kani Game App
  game experience / learner identity / immutable observations
```

The files in this directory define educational semantics. They deliberately do not define SQLite/Firebase storage, Study-Hub UI structure, QR URL shape, or Kani game mechanics.

## Canonical documents

- `PRIMARY_INTEGRATED_ARCHITECTURE.md` — system-level Primary educational architecture.
- `PRIMARY_TEACHER_RUNTIME.md` — runtime loop, learner/session state, diagnosis, teacher moves, support, evidence and mastery dimensions.
- `SEMANTIC_OWNERSHIP.md` — repository and object ownership rules.
- `contracts/v1/primary-learning-semantics.schema.json` — machine-readable v1 semantic vocabulary and core records.
- `contracts/v1/examples/fractions-learning-episode.example.json` — Grade 4 Math example used as the first cross-app contract fixture.

## Existing subject specializations

The existing root schemas remain authoritative subject-specific pedagogy:

- `Grade4MathSchema.md`
- `Grade4EnglishSchema.md`

They specialize this Primary architecture rather than being replaced by it. Grade 5 should extend the same canonical learning objects and runtime semantics instead of cloning a second ontology.

## Non-negotiable boundary

`LearningEpisode`, `TeachingTarget`, `SkillState`, `CurrentLearningState`, `TeacherDecision`, `TeacherMove`, multidimensional learning evidence, source-boundary semantics, conceptual support and access-adjustment semantics are defined here.

Study-Hub may serialize/instantiate them. Kani may observe evidence about them. Neither application may redefine their educational meaning.