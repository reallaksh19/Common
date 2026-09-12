# Grade 4 Mathematics V2 Architecture

## Ownership

`Grade 4/V2/Mathematics/**` is the canonical Grade-4 product namespace.

`Primary/**` remains the reusable Primary/Common authority. Common code is never silently forked; local copies are recorded in `CommonSnapshot/MANIFEST.json`.

## Product layers

```text
Authority
  -> CoreSkills
  -> LearningDesign
  -> Representation
  -> Publication
  -> Benchmarks / Acceptance
```

## Core invariant

Every learner-facing mathematical statement, visual, hint, workspace, and reasoning step must be justified by a typed semantic or pedagogical object upstream of layout. Layout may position or style mathematics; it may not invent pedagogy.

## Migration compatibility

Temporary compatibility symlinks may remain under `Primary/V2/Mathematics` while consumers migrate. They are not semantic authority.
