# Primary learning semantics v1

This directory contains the machine-readable semantic vocabulary for the Grade 4–5 Primary Teacher Runtime.

The schema is canonical educational meaning, not an application transport protocol.

## Authority

- Common owns the semantics.
- Study-Hub may serialize/instantiate these semantics in app-facing contracts.
- Kani may emit observations/evidence that reference these semantics.

## Files

- `primary-learning-semantics.schema.json`
- `examples/fractions-learning-episode.example.json`

## Version rule

Breaking changes to the meaning of learner state, support, evidence dimensions, diagnosis, TeacherDecision, TeacherMove, or LearningEpisode require a deliberate semantic version change.

Adding an app-specific field to Study-Hub/Kani transport does not by itself require this semantic schema to change.

## Forbidden collapse

Do not map this model into a single `masteryScore` or single exclusive `masteryState`.

Do not serialize Teacher Runtime hypotheses as raw Kani observations.