---
name: grade9-physics
description: Apply Grade 9 Physics model selection, representation translation, graph/vector reasoning, units, assumptions, experimental interpretation, physical validation, difficulty calibration, and concept-book pedagogy to textbooks and question banks. Use for motion, force, work/energy, gravitation, pressure, sound/waves, light, electricity, measurements, experiments, HOTS, competitive-foundation physics, and SEE -> REALIZE -> UNDERSTAND concept-book work within the Grade 9 learning workflow.
---

# Grade 9 Physics

Provide the subject-specific physical reasoning layer for the shared Grade 9 workflow.

## Physics fingerprint

For each question record as applicable:

- phenomenon;
- physical system;
- frame of reference;
- known and target variables;
- governing model/law;
- assumptions and model-validity conditions;
- verbal/diagram/graph/equation representations;
- required representation translations;
- units;
- minimum expert solution path;
- validation checks.

## Difficulty vector

Use 0-10 dimensions:

- `physical_model_selection`
- `conceptual_reasoning`
- `representation_translation`
- `vector_spatial_reasoning`
- `equation_construction`
- `experimental_data_reasoning`
- `constraints_cases`

Store separately:

- algebra burden;
- arithmetic burden;
- unit-conversion burden.

Long calculation alone must not make a candidate equivalent to a conceptually difficult anchor.

## Required solution structure

When quantitative:

1. identify the system;
2. state assumptions/model validity;
3. choose frame/sign convention where relevant;
4. represent the situation with diagram/graph/table if useful;
5. list knowns and unknowns;
6. select the governing law;
7. solve symbolically where practical;
8. substitute values with units;
9. check dimensions;
10. check sign, magnitude, limiting behavior, conservation, or graph consistency as relevant;
11. interpret the result physically.

## Representation principle

Treat translation among verbal, diagrammatic, graphical, and mathematical representations as a major source of difficulty. Two problems with identical formulas may not be same-level if one requires model/graph inference and the other gives the equation directly.

## Model-status metadata

Where useful classify scientific statements as:

- `EXACT_LAW`
- `IDEALIZED_MODEL`
- `EMPIRICAL_RULE`
- `QUALITATIVE_TREND`
- `APPROXIMATION`
- `SCHOOL_LEVEL_MODEL`

Record conditions/limitations so a school simplification does not become a later misconception.

## Physics misconceptions

Prefer causal models, e.g. `velocity zero -> acceleration zero`, treating action/reaction as forces on the same body, confusing mass and weight, treating graph height as distance when area/slope is relevant, or ignoring sign convention.

Use the shared question-bank and enrichment skills for calibration, hints, and diagnostics.

## Concept-book mode

For Grade 9 Physics concept-book work, read `references/concept-book-see-realize-understand.md` before authoring.

Use the core learning sequence:

`SEE THE EQUATION -> REALIZE -> UNDERSTAND -> CONNECT`

`CONNECT` is traceability/navigation, not a fourth cognitive stage.

Required behavior:

1. Ground the concept architecture to the supplied source/questions before drafting.
2. Maintain a source-coverage ledger; no source question may be orphaned.
3. Do not introduce a naked equation. Establish a physical situation, diagram, graph, numerical pattern, timeline, experiment, area model, or thought experiment first.
4. In `REALIZE`, explain the physical meaning of every term and require a plain-language statement of the equation.
5. In `UNDERSTAND`, include as applicable:
   - derivation or reconstruction;
   - assumptions and validity conditions;
   - frame/sign convention;
   - dimensional/unit check;
   - limiting and special cases;
   - graph equivalence;
   - proportional/scaling reasoning;
   - misconception contrast;
   - prediction before calculation;
   - transfer to unfamiliar source-style questions.
6. Grade 9 depth must extend beyond elementary intuition. Require symbolic reasoning, representation translation, model selection, proportional reasoning, and reconstruction from earlier principles.
7. Preserve ambiguity, defects, or missing assumptions in source material explicitly. Never silently repair source authority.
8. Use source question IDs in every `CONNECT` section.
9. For equations with unusual mathematical features, explain why the feature exists: e.g. `1/2`, `t^2`, squared velocity, negative sign, square-root scaling, nth-interval subtraction.
10. Concept-book success criterion: the learner can recognize, explain, reconstruct, predict, and transfer.

For Motion, read `references/motion-concept-book-example.md` as the worked exemplar. The chapter-specific authority is under `Grade 9/Physics/Motion/`.

## Publication handoff

When concept content is sent to the textbook publisher:

- preserve the SEE -> REALIZE -> UNDERSTAND sequence visually;
- use math-capable fonts with complete glyph coverage for superscripts, subscripts, arrows, Greek letters, and operators;
- reject missing-glyph boxes, substituted symbols, clipped equations, or rasterized low-resolution mathematics;
- verify equation legibility at normal A4 reading size;
- retain source-question traceability in authoring metadata even if some links are hidden from the student-facing layout.
